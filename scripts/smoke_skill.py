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


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT_DIR / "scripts"
REFERENCES_DIR = ROOT_DIR / "references"
PLAYBOOK_PATH = REFERENCES_DIR / "playbooks/step4/page-planning-playbook.md"


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

        prompt_specs = [
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
