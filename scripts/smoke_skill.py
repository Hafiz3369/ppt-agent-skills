#!/usr/bin/env python3
"""Minimal end-to-end smoke test for the PPT workflow skill.

This script intentionally stays within the current markdown/code architecture.
It exercises the most failure-prone integration points:
1. Step 4 planning example -> planning_validator.py
2. resource_loader.py menu / resolve / images
3. prompt_harness.py for the Step 4 prompt chain
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from workflow_versions import (  # noqa: E402
    PLANNING_CONTINUITY_VERSION,
    PLANNING_PACKET_VERSION,
    PLANNING_SCHEMA_VERSION,
    WORKFLOW_VERSION,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT_DIR / "scripts"
REFERENCES_DIR = ROOT_DIR / "references"
PLAYBOOK_PATH = REFERENCES_DIR / "playbooks/step4/page-planning-playbook.md"
PAGE_TEMPLATE_EXPECTATIONS = {
    "cover": "# 封面页 -- 演讲的第一声呼吸",
    "toc": "# 目录页 -- 演讲的地图俯瞰",
    "section": "# 章节封面页 -- 演讲中的呼吸",
    "end": "# 结束页 -- 演讲的最后一个视觉印记",
}


@dataclass
class SmokeResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def note(self, message: str) -> None:
        self.steps.append(message)


def run_cmd(label: str, args: list[str], result: SmokeResult, cwd: Path = ROOT_DIR) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        result.error(
            f"{label}: exit={proc.returncode}\n"
            f"cmd={' '.join(args)}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )
    else:
        result.note(f"{label}: ok")
    return proc


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def extract_planning_example() -> str:
    text = PLAYBOOK_PATH.read_text(encoding="utf-8")
    anchor = text.find("推荐写成单页对象")
    if anchor == -1:
        raise ValueError("planning example anchor not found")
    match = re.search(r"```json\s*(\{.*?\})\s*```", text[anchor:], re.S)
    if not match:
        raise ValueError("planning example JSON block not found")
    return match.group(1).strip()


def assert_contains(label: str, haystack: str, needles: list[str], result: SmokeResult) -> None:
    missing = [needle for needle in needles if needle not in haystack]
    if missing:
        result.error(f"{label}: missing expected content {missing}")


def assert_no_unfilled_vars(label: str, text: str, result: SmokeResult) -> None:
    leftovers = sorted(set(re.findall(r"\{\{[A-Z_][A-Z0-9_]*\}\}", text)))
    if leftovers:
        result.error(f"{label}: unfilled template vars remain: {leftovers}")


def build_non_content_page(page_type: str) -> dict[str, object]:
    return {
        "page": {
            "slide_number": 1,
            "page_type": page_type,
            "narrative_role": "opening" if page_type == "cover" else "transition",
            "title": f"Smoke {page_type}",
            "page_goal": f"验证 {page_type} 页面模板路由",
            "audience_takeaway": f"{page_type} page template resolve",
            "visual_weight": 7,
            "focus_zone": "center",
            "negative_space_target": "medium",
            "page_text_strategy": "短句为主",
            "rhythm_action": "推进",
            "must_avoid": [],
            "variation_guardrails": {
                "same_gene_as_deck": "保留统一风格变量",
                "different_from_previous": ["验证 page template 路由"],
            },
            "director_command": {
                "mood": "测试态",
                "spatial_strategy": "居中聚焦",
                "anchor_treatment": "标题优先",
                "techniques": ["T1"],
                "prose": "用于验证非 content 页的模板消费链。",
            },
            "decoration_hints": {
                "background": {"feel": "轻量背景", "restraint": "不抢主标题", "techniques": ["T1"]},
                "floating": {"feel": "弱装饰", "restraint": "仅做陪衬", "techniques": []},
                "page_accent": {"feel": "少量强调色", "restraint": "仅一处强调", "techniques": []},
            },
            "resources": {
                "page_template": None,
                "layout_refs": [],
                "block_refs": [],
                "chart_refs": [],
                "principle_refs": [],
                "resource_rationale": "验证 page_type 自动路由到 page-templates/",
            },
            "cards": [
                {
                    "card_id": "s01-anchor",
                    "role": "anchor",
                    "card_type": "text",
                    "card_style": "accent",
                    "headline": f"{page_type} smoke",
                    "body": ["最小非 content 页冒烟样例"],
                    "content_budget": {"headline_max_chars": 12, "body_max_bullets": 1, "body_max_lines": 2},
                    "image": {
                        "mode": "decorate",
                        "needed": False,
                        "usage": None,
                        "placement": None,
                        "content_description": None,
                        "source_hint": None,
                        "decorate_brief": "只做轻量占位，不引入外部图片。",
                    },
                }
            ],
            "workflow_metadata": {
                "stage": "planning",
                "workflow_version": WORKFLOW_VERSION,
                "planning_schema_version": PLANNING_SCHEMA_VERSION,
                "planning_packet_version": PLANNING_PACKET_VERSION,
                "planning_continuity_version": PLANNING_CONTINUITY_VERSION,
            },
        }
    }


def build_fixture_tree(tmp_dir: Path) -> dict[str, Path]:
    fixtures = {
        "requirements": tmp_dir / "requirements-interview.txt",
        "outline": tmp_dir / "outline.txt",
        "brief": tmp_dir / "search-brief.txt",
        "style": tmp_dir / "style.json",
        "planning": tmp_dir / "planning/planning3.json",
        "slide": tmp_dir / "slides/slide-3.html",
        "png": tmp_dir / "png/slide-3.png",
        "images": tmp_dir / "images",
        "runtime": tmp_dir / "runtime",
        "prompt_style_phase1": tmp_dir / "runtime/prompt-style-phase1.md",
        "prompt_planning": tmp_dir / "runtime/prompt-page-planning-3.md",
        "prompt_html": tmp_dir / "runtime/prompt-page-html-3.md",
        "prompt_review": tmp_dir / "runtime/prompt-page-review-3.md",
        "prompt_orchestrator": tmp_dir / "runtime/prompt-page-orchestrator-3.md",
    }

    write_text(
        fixtures["requirements"],
        "# 需求归一化\n\n## 基本信息\n- 主题：Smoke Test\n- 项目类型：演示文稿\n- 语言：中文\n- 输入类型：示例\n- 分支：research\n",
    )
    write_text(fixtures["outline"], "# 大纲\n\n## Part 1: Demo\n\n### 第 3 页：增长判断\n- 页目标：增长成立\n")
    write_text(fixtures["brief"], "# Research Brief\n\n## 核心发现\n1. 示例发现 [来源: smoke]\n")
    write_text(
        fixtures["style"],
        json.dumps(
            {
                "style_id": "smoke",
                "style_name": "Smoke",
                "mood_keywords": ["clear", "structured", "modern"],
                "design_soul": "清晰、克制、强调论点主次。",
                "variation_strategy": "统一色彩与边角，允许每页在布局重心和装饰位置上变化。",
                "decoration_dna": {
                    "signature_move": "轻微几何线条",
                    "forbidden": ["过强噪点"],
                    "recommended_combos": ["outline + accent"],
                },
                "font_family": "Noto Sans SC",
                "css_variables": {
                    "--bg-primary": "#0f172a",
                    "--bg-secondary": "#111827",
                    "--card-bg-from": "#1f2937",
                    "--card-bg-to": "#111827",
                    "--card-border": "#334155",
                    "--card-radius": "24px",
                    "--text-primary": "#f8fafc",
                    "--text-secondary": "#cbd5e1",
                    "--accent-1": "#38bdf8",
                    "--accent-2": "#22c55e",
                    "--accent-3": "#f59e0b",
                    "--accent-4": "#a78bfa",
                    "--font-primary": "Noto Sans SC",
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
    )
    fixtures["images"].mkdir(parents=True, exist_ok=True)
    write_text(fixtures["planning"], extract_planning_example())
    return fixtures


def run_smoke() -> SmokeResult:
    result = SmokeResult()
    with tempfile.TemporaryDirectory(prefix="ppt-skill-smoke-") as tmp:
        tmp_dir = Path(tmp)
        fx = build_fixture_tree(tmp_dir)
        py = sys.executable

        validator = run_cmd(
            "planning-validator",
            [
                py,
                str(SCRIPTS_DIR / "planning_validator.py"),
                str(fx["planning"].parent),
                "--refs",
                str(REFERENCES_DIR),
                "--page",
                "3",
            ],
            result,
        )
        if validator.returncode == 0:
            assert_contains("planning-validator", validator.stdout, ["OK"], result)

        menu = run_cmd(
            "resource-loader-menu",
            [py, str(SCRIPTS_DIR / "resource_loader.py"), "menu", "--refs-dir", str(REFERENCES_DIR)],
            result,
        )
        if menu.returncode == 0:
            assert_contains("resource-loader-menu", menu.stdout, ["### layouts/", "#### hero-top", "### blocks/"], result)

        resolve = run_cmd(
            "resource-loader-resolve",
            [
                py,
                str(SCRIPTS_DIR / "resource_loader.py"),
                "resolve",
                "--refs-dir",
                str(REFERENCES_DIR),
                "--planning",
                str(fx["planning"]),
            ],
            result,
        )
        if resolve.returncode == 0:
            assert_contains(
                "resource-loader-resolve",
                resolve.stdout,
                [
                    "# 顶部英雄式版式",
                    "# KPI 指标卡（数字+趋势箭头+标签）",
                    "# 指标行（数字+标签+进度条 组合）",
                    "# 视觉层级与 CRAP 原则",
                    "# 构图与留白",
                    "# Director Command Runtime Rules",
                ],
                result,
            )
            assert_no_unfilled_vars("resource-loader-resolve", resolve.stdout, result)

        images = run_cmd(
            "resource-loader-images",
            [
                py,
                str(SCRIPTS_DIR / "resource_loader.py"),
                "images",
                "--images-dir",
                str(fx["images"]),
            ],
            result,
        )
        if images.returncode == 0:
            assert_contains("resource-loader-images", images.stdout, ["count: 0", "(empty)"], result)

        for page_type, expected_title in PAGE_TEMPLATE_EXPECTATIONS.items():
            planning_dir = tmp_dir / f"planning-{page_type}"
            planning_path = planning_dir / "planning1.json"
            write_text(planning_path, json.dumps(build_non_content_page(page_type), ensure_ascii=False, indent=2))
            non_content_validate = run_cmd(
                f"planning-validator-{page_type}",
                [
                    py,
                    str(SCRIPTS_DIR / "planning_validator.py"),
                    str(planning_dir),
                    "--refs",
                    str(REFERENCES_DIR),
                    "--page",
                    "1",
                ],
                result,
            )
            if non_content_validate.returncode == 0:
                assert_contains(f"planning-validator-{page_type}", non_content_validate.stdout, ["OK"], result)

            non_content_resolve = run_cmd(
                f"resource-loader-resolve-{page_type}",
                [
                    py,
                    str(SCRIPTS_DIR / "resource_loader.py"),
                    "resolve",
                    "--refs-dir",
                    str(REFERENCES_DIR),
                    "--planning",
                    str(planning_path),
                ],
                result,
            )
            if non_content_resolve.returncode == 0:
                assert_contains(f"resource-loader-resolve-{page_type}", non_content_resolve.stdout, [expected_title], result)
                assert_no_unfilled_vars(f"resource-loader-resolve-{page_type}", non_content_resolve.stdout, result)

        prompt_specs = [
            (
                "prompt-style-phase1",
                fx["prompt_style_phase1"],
                [
                    py,
                    str(SCRIPTS_DIR / "prompt_harness.py"),
                    "--template",
                    str(REFERENCES_DIR / "prompts/tpl-style-phase1.md"),
                    "--var",
                    f"REQUIREMENTS_PATH={fx['requirements']}",
                    "--var",
                    f"OUTLINE_PATH={fx['outline']}",
                    "--var",
                    f"SKILL_DIR={ROOT_DIR}",
                    "--var",
                    f"STYLE_OUTPUT={fx['style']}",
                    "--inject-file",
                    f"STYLE_RUNTIME_RULES={REFERENCES_DIR / 'styles/runtime-style-rules.md'}",
                    "--inject-file",
                    f"STYLE_PRESET_INDEX={REFERENCES_DIR / 'styles/runtime-style-palette-index.md'}",
                    "--inject-file",
                    f"PLAYBOOK={REFERENCES_DIR / 'playbooks/style-phase1-playbook.md'}",
                    "--output",
                    str(fx["prompt_style_phase1"]),
                ],
            ),
            (
                "prompt-page-planning",
                fx["prompt_planning"],
                [
                    py,
                    str(SCRIPTS_DIR / "prompt_harness.py"),
                    "--template",
                    str(REFERENCES_DIR / "prompts/step4/tpl-page-planning.md"),
                    "--var",
                    "PAGE_NUM=3",
                    "--var",
                    "TOTAL_PAGES=8",
                    "--var",
                    f"REQUIREMENTS_PATH={fx['requirements']}",
                    "--var",
                    f"OUTLINE_PATH={fx['outline']}",
                    "--var",
                    f"BRIEF_PATH={fx['brief']}",
                    "--var",
                    f"STYLE_PATH={fx['style']}",
                    "--var",
                    f"IMAGES_DIR={fx['images']}",
                    "--var",
                    f"PLANNING_OUTPUT={fx['planning']}",
                    "--var",
                    f"SKILL_DIR={ROOT_DIR}",
                    "--var",
                    f"REFS_DIR={REFERENCES_DIR}",
                    "--inject-file",
                    f"PRINCIPLES_CHEATSHEET={REFERENCES_DIR / 'principles/design-principles-cheatsheet.md'}",
                    "--inject-file",
                    f"PLAYBOOK={REFERENCES_DIR / 'playbooks/step4/page-planning-playbook.md'}",
                    "--output",
                    str(fx["prompt_planning"]),
                ],
            ),
            (
                "prompt-page-html",
                fx["prompt_html"],
                [
                    py,
                    str(SCRIPTS_DIR / "prompt_harness.py"),
                    "--template",
                    str(REFERENCES_DIR / "prompts/step4/tpl-page-html.md"),
                    "--var",
                    "PAGE_NUM=3",
                    "--var",
                    "TOTAL_PAGES=8",
                    "--var",
                    f"PLANNING_OUTPUT={fx['planning']}",
                    "--var",
                    f"SLIDE_OUTPUT={fx['slide']}",
                    "--var",
                    f"IMAGES_DIR={fx['images']}",
                    "--var",
                    f"STYLE_PATH={fx['style']}",
                    "--var",
                    f"SKILL_DIR={ROOT_DIR}",
                    "--var",
                    f"REFS_DIR={REFERENCES_DIR}",
                    "--inject-file",
                    f"PLAYBOOK={REFERENCES_DIR / 'playbooks/step4/page-html-playbook.md'}",
                    "--output",
                    str(fx["prompt_html"]),
                ],
            ),
            (
                "prompt-page-review",
                fx["prompt_review"],
                [
                    py,
                    str(SCRIPTS_DIR / "prompt_harness.py"),
                    "--template",
                    str(REFERENCES_DIR / "prompts/step4/tpl-page-review.md"),
                    "--var",
                    "PAGE_NUM=3",
                    "--var",
                    "TOTAL_PAGES=8",
                    "--var",
                    f"PLANNING_OUTPUT={fx['planning']}",
                    "--var",
                    f"SLIDE_OUTPUT={fx['slide']}",
                    "--var",
                    f"PNG_OUTPUT={fx['png']}",
                    "--var",
                    f"STYLE_PATH={fx['style']}",
                    "--var",
                    f"SKILL_DIR={ROOT_DIR}",
                    "--inject-file",
                    f"PLAYBOOK={REFERENCES_DIR / 'playbooks/step4/page-review-playbook.md'}",
                    "--inject-file",
                    f"FAILURE_MODES={REFERENCES_DIR / 'principles/runtime-failure-modes.md'}",
                    "--output",
                    str(fx["prompt_review"]),
                ],
            ),
            (
                "prompt-page-orchestrator",
                fx["prompt_orchestrator"],
                [
                    py,
                    str(SCRIPTS_DIR / "prompt_harness.py"),
                    "--template",
                    str(REFERENCES_DIR / "prompts/step4/tpl-page-orchestrator.md"),
                    "--var",
                    "PAGE_NUM=3",
                    "--var",
                    "TOTAL_PAGES=8",
                    "--var",
                    f"PLANNING_PROMPT_PATH={fx['prompt_planning']}",
                    "--var",
                    f"HTML_PROMPT_PATH={fx['prompt_html']}",
                    "--var",
                    f"REVIEW_PROMPT_PATH={fx['prompt_review']}",
                    "--var",
                    f"PLANNING_OUTPUT={fx['planning']}",
                    "--var",
                    f"SLIDE_OUTPUT={fx['slide']}",
                    "--var",
                    f"PNG_OUTPUT={fx['png']}",
                    "--output",
                    str(fx["prompt_orchestrator"]),
                ],
            ),
        ]

        for label, output_path, args in prompt_specs:
            proc = run_cmd(label, args, result)
            if proc.returncode == 0:
                rendered = output_path.read_text(encoding="utf-8")
                assert_no_unfilled_vars(label, rendered, result)
                if label == "prompt-style-phase1":
                    assert_contains(
                        label,
                        rendered,
                        [
                            "# Runtime Style Rules",
                            "# Runtime Style Palette Index",
                            "# Style Phase 1 Playbook -- 风格合同的定义与输出",
                        ],
                        result,
                    )
                if label == "prompt-page-planning":
                    assert_contains(
                        label,
                        rendered,
                        ["# Page Planning Playbook -- 单页策划稿", "# 设计原则速查表 -- Step 4 字段级操作手册"],
                        result,
                    )
                if label == "prompt-page-html":
                    assert_contains(label, rendered, ["# Page HTML Playbook -- 单页 HTML 设计稿"], result)
                if label == "prompt-page-review":
                    assert_contains(
                        label,
                        rendered,
                        ["# Page Visual Review & Fix Playbook -- 单页图审与 HTML 修复", "# Runtime Failure Modes"],
                        result,
                    )

    return result


def print_messages(title: str, messages: list[str]) -> None:
    if not messages:
        return
    print(title)
    for item in messages:
        print(f"- {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal end-to-end smoke test for the PPT skill")
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="treat warnings as failures",
    )
    args = parser.parse_args()

    result = run_smoke()
    print("PPT skill smoke test")
    print(f"errors: {len(result.errors)}")
    print(f"warnings: {len(result.warnings)}")
    print_messages("Steps", result.steps)
    print_messages("Errors", result.errors)
    print_messages("Warnings", result.warnings)

    if result.errors:
        return 1
    if args.strict_warnings and result.warnings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
