#!/usr/bin/env python3
"""Final Review Harness -- 组装精简 reviewer prompt + 验证 harness 终审结果

用法:
  # 组装精简 prompt（只列路径，不内联大文件，极省 tokens）
  python3 scripts/final_review_harness.py assemble OUTPUT_DIR -o OUTPUT_DIR/reviews/reviewer-prompt.txt
  python3 scripts/final_review_harness.py assemble OUTPUT_DIR --review-mode source

  # 验证 harness reviewer 输出
  python3 scripts/final_review_harness.py validate OUTPUT_DIR/reviews/final-review-round-1.json --pages 15
"""

import argparse
import json
import pathlib
import re
import sys

# ── 评分标准（与 harness/review-subagent 协议保持同步）──────────

PAGE_DIMENSIONS = {
    "info_density":           {"weight": 0.20, "label": "信息密度"},
    "visual_impact":          {"weight": 0.25, "label": "视觉冲击力"},
    "layout_precision":       {"weight": 0.15, "label": "布局精度"},
    "color_execution":        {"weight": 0.10, "label": "色彩执行"},
    "resource_consumption":   {"weight": 0.10, "label": "资源消费"},
    "narrative_contribution": {"weight": 0.20, "label": "叙事贡献"},
}

GLOBAL_DIMENSIONS = ["narrative_coherence", "visual_rhythm", "style_consistency"]

PASS_THRESHOLD = 9.0


def natural_sort_key(path: pathlib.Path):
    parts = re.split(r"(\d+)", path.name)
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def resolve_review_mode(requested: str, has_png: bool) -> str:
    if requested == "auto":
        return "vision" if has_png else "source"
    return requested


# ── assemble: 精简 prompt（路径清单 + 评分标准，不内联大文件）───

def cmd_assemble(args):
    reviewer_codename = "NightOwl"
    out_dir = pathlib.Path(args.output_dir)
    out_file = pathlib.Path(args.output) if args.output else out_dir / "reviews" / "reviewer-prompt.txt"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    errors = []

    # ── 检查必要文件 ──
    outline = out_dir / "outline.json"
    if not outline.exists():
        errors.append(f"缺失: {outline}")

    style = out_dir / "style.json"
    if not style.exists():
        errors.append(f"缺失: {style}")

    planning_dir = out_dir / "planning"
    planning_files = sorted(planning_dir.glob("planning*.json"), key=natural_sort_key) if planning_dir.exists() else []
    if not planning_files:
        errors.append("缺失: planning/*.json")

    slides_dir = out_dir / "slides"
    slide_files = sorted(slides_dir.glob("slide-*.html"), key=natural_sort_key) if slides_dir.exists() else []
    if not slide_files:
        errors.append("缺失: slides/*.html")

    png_dir = out_dir / "png"
    png_files = sorted(png_dir.glob("slide-*.png"), key=natural_sort_key) if png_dir.exists() else []
    review_mode = resolve_review_mode(args.review_mode, bool(png_files))
    if review_mode == "vision" and not png_files:
        errors.append("缺失: png/*.png（vision review 需要先运行 scripts/html2png.py 截图；若当前环境无读图能力，请改用 --review-mode source）")

    if args.requirement:
        req_file = pathlib.Path(args.requirement)
        has_requirement = req_file.exists()
    else:
        requirement_candidates = [
            out_dir / "requirement.json",
            out_dir / "requirements.json",
        ]
        req_file = next((path for path in requirement_candidates if path.exists()), requirement_candidates[0])
        has_requirement = req_file.exists()

    if errors:
        print("ERROR: 资料包不完整，无法组装 reviewer prompt:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    # ── 组装精简 prompt ──
    parts = []

    parts.append(f"# Final Review -- Reviewer Sub-agent Prompt ({reviewer_codename})")
    parts.append("")
    parts.append(f"你是严格的 PPT 质量审查员（代号：{reviewer_codename}）。你与生成者完全隔离，从零审查。")
    parts.append("这是 SKILL.md Step 5d 的强制终审回路，发生在 HTML 生成之后、用户预览与导出之前。")
    parts.append("只有当主 agent 明确把当前产物送入该终审回路时，你才接管评分与修复。")
    parts.append("一旦进入该回路，终审必须由隔离 reviewer sub-agent 执行；主 agent 不得自己兼任 reviewer。")
    parts.append("在这个 harness 回路中，你既审又改：评分后对不达标页面直接修改对应文件。")
    parts.append("修改后不自检，主 agent 会另起新 reviewer 从零审查你的修改。")
    parts.append(f"当前审查模式：`{review_mode}`。")
    parts.append("")

    # ── PPT 生产 pipeline（让 reviewer 知道上下游关系）──
    parts.append("## PPT 生产 Pipeline（你需要知道的上下游关系）")
    parts.append("")
    parts.append("```")
    parts.append("Step 1: 需求调研 → requirements.json（默认文件名，兼容旧 requirement.json；用户要什么、受众、场景）")
    parts.append("Step 3: 大纲策划 → outline.json（叙事结构、Part 划分、页面目标）")
    parts.append("Step 4: 逐页策划 → planning/*.json（每页的内容、布局、卡片、数据）")
    parts.append("Step 5a: 风格决策 → style.json（配色、装饰、字体）")
    parts.append("Step 5c: HTML 生成 → slides/*.html（最终视觉产物）")
    parts.append("Step 5d: 强制终审 → reviews/*.json（隔离 reviewer 评分、修复、复审）")
    if review_mode == "vision":
        parts.append("截图:   HTML → PNG → png/*.png（你看到的截图）")
    else:
        parts.append("源码审查: slides/*.html（当前环境按 HTML 源码 + planning/style 合同执行终审）")
    parts.append("```")
    parts.append("")
    parts.append("**问题定位逻辑**：")
    if review_mode == "vision":
        parts.append("- 看 PNG 觉得**内容空洞** → 问题可能在 planning（没写内容）或 HTML（没渲染）→ 先读 planning，再读 HTML")
        parts.append("- 看 PNG 觉得**叙事断裂** → 问题可能在 outline（结构设计）或 planning（衔接丢失）→ 先读 outline，再读 planning")
        parts.append("- 看 PNG 觉得**布局丑陋** → 问题在 HTML → 读 planning（看设计意图）+ HTML（看实现）")
        parts.append("- 看 PNG 觉得**配色奇怪** → 问题可能在 style.json 或 HTML → 读 style.json + HTML")
    else:
        parts.append("- 先读每页 HTML，看可见正文是否完整承载 planning 合同，而不是把规则/说明渲染进页面")
        parts.append("- 再对照 planning 判断：是 planning 空，还是 HTML 没把合同真正落地")
        parts.append("- 色彩/风格问题先对照 style.json，再看 HTML 是否遵守 CSS 变量与装饰 DNA")
        parts.append("- 源码审查模式下，低分页必须直接修改 HTML；如根因在 planning/style，则按回滚层级修改并重生 HTML")
    parts.append("- **最终修改都落在 HTML 上**（改 planning 后也要重生 HTML）")
    parts.append("")

    # ── 工作流程 ──
    parts.append("## 工作流程（按需读取，极省 tokens）")
    parts.append("")
    parts.append("```")
    parts.append("逐页循环：")
    if review_mode == "vision":
        parts.append("  1. view_file PNG 截图 → 看图，按 6 维度评分")
    else:
        parts.append("  1. view_file slide HTML → 检查页面正文、层级、布局、data-* 合同、规则泄漏")
    parts.append("  2. 全部 >= 9？→ 记录分数，下一页（零文件读取）")
    parts.append("  3. 有 < 9 的维度？→ 按上方「问题定位逻辑」view_file 对应层文件")
    parts.append("  4. 诊断根因 → 直接修改文件 → 记录 modifications")
    parts.append("     改 planning → 重跑 scripts/prompt_assembler.py → 重新生成 HTML")
    parts.append("     改 style.json → 重新生成相关 HTML")
    parts.append("     改 HTML → 直接改")
    parts.append("")
    parts.append("逐页完成后：综合评 3 维全局（叙事连贯性/视觉节奏/风格统一）")
    parts.append("```")
    parts.append("")

    # ── 评分标准 ──
    parts.append("## 评分标准（9 分通过线，不给人情分）")
    parts.append("")
    parts.append("### 逐页评分（6 维度，每维 1-10 分）")
    parts.append("")
    parts.append("| 维度 | key | 权重 | 9 分 = 通过 | 低分特征 |")
    parts.append("|------|-----|------|------|------|")
    parts.append("| **信息密度** | `info_density` | 20% | 每张卡片有标题+正文+数据，无空卡 | 空卡/废话/数据缺失 |")
    parts.append("| **视觉冲击力** | `visual_impact` | 25% | 有设计感，达到万元/页级水准 | 普通前端排版 |")
    parts.append("| **布局精度** | `layout_precision` | 15% | 无重叠无溢出，grid 正确 | 卡片错位/溢出画布 |")
    parts.append("| **色彩执行** | `color_execution` | 10% | 全部 CSS 变量，accent <= 2 种 | 硬编码颜色 |")
    parts.append("| **资源消费** | `resource_consumption` | 10% | planning 指定的资源在 HTML 中体现 | 资源未消费 |")
    parts.append("| **叙事贡献** | `narrative_contribution` | 20% | 该页角色清晰，与前后页衔接 | 孤立/断裂 |")
    parts.append("")
    parts.append("### 全局评分（3 维度，每维 1-10 分）")
    parts.append("")
    parts.append("| 维度 | key |")
    parts.append("|------|-----|")
    parts.append("| **叙事连贯性** | `narrative_coherence` |")
    parts.append("| **视觉节奏** | `visual_rhythm` |")
    parts.append("| **风格统一** | `style_consistency` |")
    parts.append("")

    # ── 输出格式 ──
    parts.append("## 输出格式（严格 JSON，不要输出 JSON 之外的内容）")
    parts.append("")
    output_schema = {
        "timestamp": "ISO",
        "round": 1,
        "page_scores": [
            {
                "page": "N",
                "scores": {k: "1-10" for k in PAGE_DIMENSIONS},
                "weighted_total": "加权总分",
                "verdict": "pass|fail",
                "issues": [{"dimension": "key", "detail": "问题", "rollback_to": "planning|html|style"}],
                "modifications": [{"layer": "planning|html|style", "file": "路径", "action": "做了什么", "then": "后续操作"}]
            }
        ],
        "global_scores": {d: "1-10" for d in GLOBAL_DIMENSIONS},
        "overall_verdict": "pass|needs_fix",
        "total_modifications": 0
    }
    parts.append("```json")
    parts.append(json.dumps(output_schema, ensure_ascii=False, indent=2))
    parts.append("```")
    parts.append("")
    parts.append("> weighted_total = 各维度 * 权重之和。>= 9 为 pass，< 9 为 fail。")
    parts.append("> 达标页的 issues 和 modifications 为空数组。")
    parts.append("> **防偷懒：fail 页面的 modifications 不能为空。评分低但不改 = harness 报错退回，要求重新执行。**")
    parts.append("> 不给人情分。")
    parts.append("")

    # ── 文件路径清单 ──
    parts.append("---")
    parts.append("")
    parts.append(f"## 文件路径清单（OUTPUT_DIR = `{out_dir}`）")
    parts.append("")
    if review_mode == "vision":
        parts.append("> **先看 PNG 评分，只对不达标页面按需读取对应层文件。**")
    else:
        parts.append("> **先看 HTML 源码评分；如果需要定位根因，再按需读取 planning/style/outline。**")
    parts.append("")

    if review_mode == "vision":
        parts.append(f"### PNG 截图（{len(png_files)} 张 -- 每页必看）")
        parts.append("")
        for pf in png_files:
            parts.append(f"- `{pf}`")
        parts.append("")

    parts.append(f"### slide HTML（{len(slide_files)} 页 -- {'按需读取' if review_mode == 'vision' else '每页必读'}）")
    parts.append("")
    for sf in slide_files:
        parts.append(f"- `{sf}`")
    parts.append("")

    parts.append(f"### 策划稿 JSON（{len(planning_files)} 页 -- 按需读取）")
    parts.append("")
    for pf in planning_files:
        parts.append(f"- `{pf}`")
    parts.append("")

    parts.append("### 其他文件（按需读取）")
    parts.append("")
    parts.append(f"- 大纲：`{outline}`")
    parts.append(f"- 风格：`{style}`")
    if has_requirement:
        parts.append(f"- 需求：`{req_file}`")
    parts.append("")

    # ── 写入 ──
    prompt_text = "\n".join(parts)
    out_file.write_text(prompt_text, "utf-8")

    print(f"Done: reviewer prompt assembled (精简模式)")
    if review_mode == "vision":
        print(f"  模式: vision")
        print(f"  文件清单: {len(png_files)} PNG + {len(planning_files)} planning + {len(slide_files)} slides")
    else:
        print(f"  模式: source")
        print(f"  文件清单: {len(planning_files)} planning + {len(slide_files)} slides")
    print(f"  输出: {out_file}")
    print(f"  大小: {len(prompt_text):,} 字符（不含大文件内容）")


# ── validate: 验证 reviewer 输出 ──────────────────────────────

def cmd_validate(args):
    review_file = pathlib.Path(args.review_file)

    if not review_file.exists():
        print(f"ERROR: {review_file} 不存在")
        sys.exit(1)

    try:
        data = json.loads(review_file.read_text("utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON 解析失败: {e}")
        sys.exit(1)

    errors = []
    warnings = []

    # ── 顶层字段 ──
    for field in ["timestamp", "round", "page_scores", "global_scores", "overall_verdict", "total_modifications"]:
        if field not in data:
            errors.append(f"缺失顶层字段: {field}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(1)

    # ── page_scores ──
    total_pages = len(data["page_scores"])
    if args.pages and total_pages != args.pages:
        warnings.append(f"页数不匹配: 期望 {args.pages}，实际 {total_pages}")

    fail_pages = []
    total_mods = 0
    for ps in data["page_scores"]:
        page = ps.get("page", "?")

        scores = ps.get("scores", {})
        for dim in PAGE_DIMENSIONS:
            if dim not in scores:
                errors.append(f"第 {page} 页缺失维度: {dim}")
            elif not isinstance(scores[dim], (int, float)):
                errors.append(f"第 {page} 页 {dim} 不是数字: {scores[dim]}")
            elif not (1 <= scores[dim] <= 10):
                errors.append(f"第 {page} 页 {dim} 超出范围 [1-10]: {scores[dim]}")

        # 验证加权总分
        if scores and all(isinstance(scores.get(d), (int, float)) for d in PAGE_DIMENSIONS):
            expected = sum(scores[d] * PAGE_DIMENSIONS[d]["weight"] for d in PAGE_DIMENSIONS)
            actual = ps.get("weighted_total", 0)
            if abs(expected - actual) > 0.2:
                warnings.append(f"第 {page} 页加权总分偏差: 期望 {expected:.1f}，实际 {actual}")

        # verdict 一致性
        weighted = ps.get("weighted_total", 0)
        expected_verdict = "pass" if weighted >= PASS_THRESHOLD else "fail"
        if ps.get("verdict") != expected_verdict:
            warnings.append(f"第 {page} 页 verdict 不一致: 总分 {weighted}，应为 {expected_verdict}，实际 {ps.get('verdict')}")

        if weighted < PASS_THRESHOLD:
            fail_pages.append(page)
            if not ps.get("issues"):
                errors.append(f"第 {page} 页不达标（{weighted:.1f}）但缺少 issues 诊断")
            else:
                for issue in ps.get("issues", []):
                    rt = issue.get("rollback_to")
                    if rt not in ("planning", "html", "style"):
                        errors.append(f"第 {page} 页 issue rollback_to 非法: {rt}")

        # 统计修改数 + 防偷懒检测
        mods = ps.get("modifications", [])
        total_mods += len(mods)
        for mod in mods:
            if mod.get("layer") not in ("planning", "html", "style"):
                errors.append(f"第 {page} 页 modification layer 非法: {mod.get('layer')}")

        # 防偷懒：fail 但 modifications 为空 = reviewer 只评不改，失职
        if weighted < PASS_THRESHOLD and not mods:
            errors.append(f"第 {page} 页不达标（{weighted:.1f}）但 modifications 为空 -- reviewer 只评不改，必须重新执行修改")

    # ── global_scores ──
    gs = data.get("global_scores", {})
    global_fail = []
    for dim in GLOBAL_DIMENSIONS:
        if dim not in gs:
            errors.append(f"缺失全局维度: {dim}")
        elif not isinstance(gs[dim], (int, float)):
            errors.append(f"全局 {dim} 不是数字: {gs[dim]}")
        elif not (1 <= gs[dim] <= 10):
            errors.append(f"全局 {dim} 超出范围 [1-10]: {gs[dim]}")
        elif gs[dim] < PASS_THRESHOLD:
            global_fail.append(dim)

    # ── 输出结果 ──
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    # ── 每页评分表 ──
    print(f"\n{'='*60}")
    print(f"  Final Review Round {data.get('round', '?')} 摘要")
    print(f"{'='*60}")
    print(f"  {'页码':>4} | {'总分':>5} | {'判定':>6} | {'信息':>4} | {'视觉':>4} | {'布局':>4} | {'色彩':>4} | {'资源':>4} | {'叙事':>4}")
    print(f"  {'-'*4}-+-{'-'*5}-+-{'-'*6}-+-{'-'*4}-+-{'-'*4}-+-{'-'*4}-+-{'-'*4}-+-{'-'*4}-+-{'-'*4}")
    for ps in data["page_scores"]:
        p = ps.get("page", "?")
        s = ps.get("scores", {})
        wt = ps.get("weighted_total", 0)
        v = ps.get("verdict", "?")
        dim_keys = list(PAGE_DIMENSIONS.keys())
        vals = [str(s.get(k, "?")) for k in dim_keys]
        print(f"  {p:>4} | {wt:>5.1f} | {v:>6} | {'  |  '.join(vals)}")

    print(f"\n  全局: " + " / ".join(f"{d}={gs.get(d, '?')}" for d in GLOBAL_DIMENSIONS))
    if global_fail:
        print(f"  全局不达标: {global_fail}")
    print(f"  本轮修改: {total_mods} 处")
    print(f"  整体判定: {data.get('overall_verdict', '?')}")
    print(f"{'='*60}")

    if errors:
        sys.exit(1)
    elif data.get("overall_verdict") == "needs_fix" or total_mods > 0:
        sys.exit(2)  # 有修改，需要换人审查
    else:
        print("All passed!")
        sys.exit(0)


# ── CLI ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Final Review Harness -- 组装精简 reviewer prompt + 验证 harness 终审结果"
    )
    subparsers = parser.add_subparsers(dest="command")

    p_asm = subparsers.add_parser("assemble", help="组装精简 prompt（路径清单，不内联大文件）")
    p_asm.add_argument("output_dir", help="产物输出根目录（ppt-output/）")
    p_asm.add_argument("-o", "--output", help="输出文件路径")
    p_asm.add_argument("--requirement", help="需求 JSON 文件路径（可选；默认优先使用 requirements.json，并兼容旧 requirement.json）")
    p_asm.add_argument("--review-mode", choices=["auto", "vision", "source"], default="auto", help="auto=有 PNG 则 vision，否则 source")

    p_val = subparsers.add_parser("validate", help="验证 reviewer 输出的评分 JSON")
    p_val.add_argument("review_file", help="final-review-round-N.json 路径")
    p_val.add_argument("--pages", type=int, help="期望页数（用于校验）")

    args = parser.parse_args()

    if args.command == "assemble":
        cmd_assemble(args)
    elif args.command == "validate":
        cmd_validate(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
