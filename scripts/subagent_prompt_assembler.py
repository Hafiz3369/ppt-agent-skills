#!/usr/bin/env python3
"""Assemble runtime prompt files for isolated sub-agents.

Main agent should stay as console/orchestrator:
- verify node files
- assemble prompt packets
- dispatch / monitor / close sub-agents
"""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "references"
PROMPTS = REFS / "prompts"
PLAYBOOKS = REFS / "playbooks"
RUNTIME = REFS / "runtime"


def append_extra_context(lines: list[str], args: argparse.Namespace) -> list[str]:
    extra_notes = list(getattr(args, "extra_note", []) or [])
    notes_file = getattr(args, "extra_notes_file", None)
    if notes_file:
        note_path = Path(notes_file).resolve()
        if note_path.exists():
            content = note_path.read_text(encoding="utf-8").strip()
            if content:
                extra_notes.append(content)
    if extra_notes:
        lines += [
            "",
            "主 agent 追加运行上下文：",
        ]
        for note in extra_notes:
            cleaned = str(note).strip()
            if cleaned:
                lines.append(f"- {cleaned}")
        lines += [
            "",
            "追加上下文边界：",
            "- 只能补充当前轮次、批次边界、用户最新反馈、validator/harness 错误、回退原因、优先级提醒",
            "- 不得覆盖正式文件真源，不得口头改写 requirements / outline / planning / style 合同",
        ]
    return lines


def write_prompt(output: Path, lines: list[str], args: argparse.Namespace) -> int:
    lines = append_extra_context(lines, args)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"Done: prompt assembled -> {output}")
    return 0


def cmd_research(args: argparse.Namespace) -> int:
    lines = [
        "# Research Sub-agent Prompt",
        "",
        "你是隔离资料收集 sub-agent。",
        f"先读取 playbook：`{PLAYBOOKS / 'research-subagent-playbook.md'}`",
        "",
        "只做搜索与原始素材收集，不做可信度评估，不做结构化打包。",
        "",
        "读取输入：",
        f"- requirements: `{Path(args.requirements).resolve()}`",
        "",
        "写出产物：",
        f"- raw research: `{Path(args.output).resolve()}`",
        "",
        "硬规则：",
        "- 只负责 research，不兼任 material-prep",
        "- 如果 requirements 缺字段，直接报缺口，不要脑补",
        "- 完成后立即交回主链，由主 agent 回收并关闭你",
    ]
    return write_prompt(Path(args.prompt), lines, args)


def cmd_material_prep(args: argparse.Namespace) -> int:
    lines = [
        "# Material Prep Sub-agent Prompt",
        "",
        "你是隔离资料整理 sub-agent。",
        f"先读取 playbook：`{PLAYBOOKS / 'material-prep-subagent-playbook.md'}`",
        "",
        "只做清洗、分类、可信度评估和缺口打包，不做搜索。",
        "",
        "读取输入：",
        f"- requirements: `{Path(args.requirements).resolve()}`",
        f"- raw research: `{Path(args.raw_research).resolve()}`",
        "",
        "写出产物：",
        f"- research package: `{Path(args.output).resolve()}`",
        "",
        "硬规则：",
        "- 必须显式写 gaps，不能假装搜到了",
        "- 完成后立即交回主链，由主 agent 回收并关闭你",
    ]
    return write_prompt(Path(args.prompt), lines, args)


def cmd_outline(args: argparse.Namespace) -> int:
    lines = [
        "# Outline Sub-agent Prompt",
        "",
        "你是隔离大纲编写 sub-agent。",
        f"先读取 playbook：`{PLAYBOOKS / 'outline-subagent-playbook.md'}`",
        f"再读取 prompt：`{PROMPTS / 'prompt-2-outline.md'}`",
        "",
        "只负责生成或修订大纲，不负责审查。",
        "",
        "读取输入：",
        f"- requirements: `{Path(args.requirements).resolve()}`",
        f"- research package: `{Path(args.research_package).resolve()}`",
    ]
    if args.issues:
        lines.append(f"- fix issues: `{Path(args.issues).resolve()}`")
    lines += [
        "",
        "写出产物：",
        f"- outline: `{Path(args.output).resolve()}`",
        "",
        "硬规则：",
        "- 如果是返工，只修 issues 指向的问题，不整稿推翻",
        "- 完成后立即交回主链，由主 agent 回收并关闭你",
    ]
    return write_prompt(Path(args.prompt), lines, args)


def cmd_outline_review(args: argparse.Namespace) -> int:
    lines = [
        "# Outline Review Sub-agent Prompt",
        "",
        "你是隔离大纲审查 sub-agent。",
        f"先读取 playbook：`{PLAYBOOKS / 'outline-review-subagent-playbook.md'}`",
        "",
        "只负责评分和输出修改指令，不直接修改 outline.json。",
        "",
        "读取输入：",
        f"- requirements: `{Path(args.requirements).resolve()}`",
        f"- research package: `{Path(args.research_package).resolve()}`",
        f"- outline: `{Path(args.outline).resolve()}`",
        "",
        "写出产物：",
        f"- review result: `{Path(args.output).resolve()}`",
        "",
        "硬规则：",
        "- 9 分是通过线，任一维度 < 9 就 needs_fix",
        "- 完成后立即交回主链，由主 agent 回收并关闭你",
    ]
    return write_prompt(Path(args.prompt), lines, args)


def cmd_planning(args: argparse.Namespace) -> int:
    lines = [
        "# Planning Sub-agent Prompt",
        "",
        "你是隔离策划 sub-agent。",
        f"先读取 playbook：`{PLAYBOOKS / 'planning-subagent-playbook.md'}`",
        f"再读取 prompt：`{PROMPTS / 'prompt-3-planning.md'}`",
        "",
        "只负责指定页范围的 planning JSON，不负责 HTML。",
        "",
        "读取输入：",
        f"- requirements: `{Path(args.requirements).resolve()}`",
        f"- research package: `{Path(args.research_package).resolve()}`",
        f"- outline: `{Path(args.outline).resolve()}`",
        f"- page range: `{args.page_range}`",
    ]
    if args.continuity:
        lines.append(f"- continuity note: `{Path(args.continuity).resolve()}`")
    lines += [
        "",
        "写出产物：",
        f"- planning dir: `{Path(args.output_dir).resolve()}`",
        "",
        "写入后必须执行：",
        f"- `python3 {Path(args.validator).resolve()} {Path(args.output_dir).resolve()} --refs {REFS.resolve()}`",
        "",
        "硬规则：",
        "- 只负责自己页范围",
        "- ERROR 必须修完再交回主链",
        "- 完成后立即交回主链，由主 agent 回收并关闭你",
    ]
    return write_prompt(Path(args.prompt), lines, args)


def cmd_style(args: argparse.Namespace) -> int:
    lines = [
        "# Style Sub-agent Prompt",
        "",
        "你是隔离风格决策 sub-agent。",
        f"先读取资料：`{REFS / 'styles' / 'README.md'}`",
        "",
        "只负责生成 style.json，不负责 planning、HTML、review。",
        "",
        "读取输入：",
        f"- requirements: `{Path(args.requirements).resolve()}`",
    ]
    if args.outline:
        lines.append(f"- outline: `{Path(args.outline).resolve()}`")
    lines += [
        "",
        "写出产物：",
        f"- style: `{Path(args.output).resolve()}`",
        "",
        "硬规则：",
        "- 必须输出完整 style 合同，而不是只给颜色",
        "- 完成后立即交回主链，由主 agent 回收并关闭你",
    ]
    return write_prompt(Path(args.prompt), lines, args)


def cmd_image(args: argparse.Namespace) -> int:
    lines = [
        "# Image Sub-agent Prompt",
        "",
        "你是隔离配图 sub-agent。",
        f"先读取资料：`{RUNTIME / 'image-generation.md'}`",
        "",
        "只负责读取 planning 中的 image 合同、生成图片、回填 image.path。",
        "",
        "读取输入：",
        f"- planning: `{Path(args.planning).resolve()}`",
    ]
    if args.style:
        lines.append(f"- style: `{Path(args.style).resolve()}`")
    lines += [
        "",
        "写出产物：",
        f"- images dir: `{Path(args.output_dir).resolve()}`",
        "",
        "硬规则：",
        "- 只处理 image.needed=true 的条目",
        "- 生成后必须把 image.path 回填到对应 planning 文件",
        "- 完成后立即交回主链，由主 agent 回收并关闭你",
    ]
    return write_prompt(Path(args.prompt), lines, args)


def cmd_html(args: argparse.Namespace) -> int:
    lines = [
        "# HTML Sub-agent Prompt",
        "",
        "你是隔离 HTML sub-agent。",
        f"先读取 playbook：`{PLAYBOOKS / 'html-subagent-playbook.md'}`",
        "",
        f"只负责第 {args.page} 页 HTML，不负责其他页面。",
        "",
        "读取输入：",
        f"- prompt-ready: `{Path(args.prompt_ready).resolve()}`",
        f"- planning: `{Path(args.planning).resolve()}`",
        "",
        "写出产物：",
        f"- slide html: `{Path(args.output).resolve()}`",
        "",
        "硬规则：",
        "- 先读 prompt-ready，再按需核对 planning",
        "- 不允许跳过 prompt-ready 直接写 HTML",
        "- 完成后立即交回主链，由主 agent 回收并关闭你",
    ]
    return write_prompt(Path(args.prompt), lines, args)


def add_common_prompt_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--extra-note", action="append", help="Optional runtime context appended by main agent")
    parser.add_argument("--extra-notes-file", help="Optional file containing extra runtime context")


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble sub-agent prompt packets")
    subparsers = parser.add_subparsers(dest="command")

    research = subparsers.add_parser("research", help="Assemble research sub-agent prompt")
    research.add_argument("--requirements", required=True)
    research.add_argument("--output", required=True)
    research.add_argument("--prompt", required=True)
    add_common_prompt_args(research)
    research.set_defaults(func=cmd_research)

    material = subparsers.add_parser("material-prep", help="Assemble material-prep sub-agent prompt")
    material.add_argument("--requirements", required=True)
    material.add_argument("--raw-research", required=True)
    material.add_argument("--output", required=True)
    material.add_argument("--prompt", required=True)
    add_common_prompt_args(material)
    material.set_defaults(func=cmd_material_prep)

    outline = subparsers.add_parser("outline", help="Assemble outline sub-agent prompt")
    outline.add_argument("--requirements", required=True)
    outline.add_argument("--research-package", required=True)
    outline.add_argument("--output", required=True)
    outline.add_argument("--prompt", required=True)
    outline.add_argument("--issues")
    add_common_prompt_args(outline)
    outline.set_defaults(func=cmd_outline)

    outline_review = subparsers.add_parser("outline-review", help="Assemble outline-review sub-agent prompt")
    outline_review.add_argument("--requirements", required=True)
    outline_review.add_argument("--research-package", required=True)
    outline_review.add_argument("--outline", required=True)
    outline_review.add_argument("--output", required=True)
    outline_review.add_argument("--prompt", required=True)
    add_common_prompt_args(outline_review)
    outline_review.set_defaults(func=cmd_outline_review)

    planning = subparsers.add_parser("planning", help="Assemble planning sub-agent prompt")
    planning.add_argument("--requirements", required=True)
    planning.add_argument("--research-package", required=True)
    planning.add_argument("--outline", required=True)
    planning.add_argument("--output-dir", required=True)
    planning.add_argument("--page-range", required=True)
    planning.add_argument("--validator", default=str(Path(__file__).resolve().parent / "planning_validator.py"))
    planning.add_argument("--prompt", required=True)
    planning.add_argument("--continuity")
    add_common_prompt_args(planning)
    planning.set_defaults(func=cmd_planning)

    style = subparsers.add_parser("style", help="Assemble style sub-agent prompt")
    style.add_argument("--requirements", required=True)
    style.add_argument("--output", required=True)
    style.add_argument("--prompt", required=True)
    style.add_argument("--outline")
    add_common_prompt_args(style)
    style.set_defaults(func=cmd_style)

    image = subparsers.add_parser("image", help="Assemble image sub-agent prompt")
    image.add_argument("--planning", required=True)
    image.add_argument("--output-dir", required=True)
    image.add_argument("--prompt", required=True)
    image.add_argument("--style")
    add_common_prompt_args(image)
    image.set_defaults(func=cmd_image)

    html = subparsers.add_parser("html", help="Assemble HTML sub-agent prompt")
    html.add_argument("--page", required=True)
    html.add_argument("--prompt-ready", required=True)
    html.add_argument("--planning", required=True)
    html.add_argument("--output", required=True)
    html.add_argument("--prompt", required=True)
    add_common_prompt_args(html)
    html.set_defaults(func=cmd_html)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
