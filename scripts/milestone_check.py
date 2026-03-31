#!/usr/bin/env python3
"""Milestone checker for the PPT workflow.

Usage examples:
  python3 scripts/milestone_check.py 0
  python3 scripts/milestone_check.py 3
  python3 scripts/milestone_check.py 5c
  python3 scripts/milestone_check.py preview
  python3 scripts/milestone_check.py 6 --output-dir /path/to/ppt-output
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from planning_validator import load_planning_pages


STAGE_ORDER = ("0", "1", "2", "3", "4", "5a", "5b", "5c", "5d", "preview", "6")
STAGE_ALIAS = {
    "0": "0",
    "step0": "0",
    "step_0": "0",
    "step-0": "0",
    "1": "1",
    "step1": "1",
    "step_1": "1",
    "step-1": "1",
    "2": "2",
    "step2": "2",
    "step_2": "2",
    "step-2": "2",
    "3": "3",
    "step3": "3",
    "step_3": "3",
    "step-3": "3",
    "4": "4",
    "step4": "4",
    "step_4": "4",
    "step-4": "4",
    "5a": "5a",
    "step5a": "5a",
    "step_5a": "5a",
    "step-5a": "5a",
    "5b": "5b",
    "step5b": "5b",
    "step_5b": "5b",
    "step-5b": "5b",
    "5c": "5c",
    "step5c": "5c",
    "step_5c": "5c",
    "step-5c": "5c",
    "5d": "5d",
    "step5d": "5d",
    "step_5d": "5d",
    "step-5d": "5d",
    "5p": "preview",
    "preview": "preview",
    "step5p": "preview",
    "step_5p": "preview",
    "step-5p": "preview",
    "step5preview": "preview",
    "step_5preview": "preview",
    "step-5preview": "preview",
    "6": "6",
    "step6": "6",
    "step_6": "6",
    "step-6": "6",
}


def natural_sort_key(path: Path) -> tuple[object, ...]:
    parts = re.split(r"(\d+)", path.name)
    key: list[object] = []
    for part in parts:
        key.append(int(part) if part.isdigit() else part.lower())
    return tuple(key)


class Checker:
    def __init__(self, skill_dir: Path, output_dir: Path, target: str, quiet: bool = False):
        self.skill_dir = skill_dir
        self.output_dir = output_dir
        self.target = target
        self.target_idx = STAGE_ORDER.index(target)
        self.python = sys.executable or "python3"
        self.quiet = quiet
        self.pages: int | None = None

    def reached(self, stage: str) -> bool:
        return self.target_idx >= STAGE_ORDER.index(stage)

    def echo(self, message: str) -> None:
        if not self.quiet:
            print(message)

    def fail(self, message: str) -> None:
        raise RuntimeError(message)

    def must_file(self, path: Path) -> None:
        if not path.is_file():
            self.fail(f"missing file: {path}")

    def must_dir(self, path: Path) -> None:
        if not path.is_dir():
            self.fail(f"missing dir: {path}")

    def run_cmd(self, cmd: list[str], title: str) -> None:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            return
        details: list[str] = [f"{title} failed: {' '.join(cmd)}"]
        out = proc.stdout.strip()
        err = proc.stderr.strip()
        if out:
            details.append(f"stdout:\n{out}")
        if err:
            details.append(f"stderr:\n{err}")
        self.fail("\n".join(details))

    def latest(self, pattern: str) -> Path:
        matches = sorted(self.output_dir.glob(pattern), key=natural_sort_key)
        if not matches:
            self.fail(f"missing {pattern} in {self.output_dir}")
        return matches[-1]

    def check_step0(self) -> None:
        self.echo("== Step 0 ==")
        progress = self.output_dir / "progress.json"
        self.must_file(progress)
        cmd = [self.python, str(self.skill_dir / "scripts/progress_validator.py"), str(progress)]
        if self.target == "0":
            cmd.append("--require-pre-step1")
        self.run_cmd(cmd, "progress_validator")
        self.echo("[OK] step 0")

    def check_step1(self) -> None:
        self.echo("== Step 1 ==")
        interview = self.output_dir / "interview-qa.txt"
        requirements = self.output_dir / "requirements-interview.txt"
        self.must_file(interview)
        self.must_file(requirements)
        self.run_cmd(
            [
                self.python,
                str(self.skill_dir / "scripts/contract_validator.py"),
                "interview",
                str(interview),
            ],
            "contract_validator interview",
        )
        self.run_cmd(
            [
                self.python,
                str(self.skill_dir / "scripts/contract_validator.py"),
                "requirements-interview",
                str(requirements),
            ],
            "contract_validator requirements-interview",
        )
        self.echo("[OK] step 1")

    def check_step2(self) -> None:
        self.echo("== Step 2 ==")
        search = self.output_dir / "search.txt"
        search_brief = self.output_dir / "search-brief.txt"
        self.must_file(search)
        self.must_file(search_brief)
        self.run_cmd(
            [
                self.python,
                str(self.skill_dir / "scripts/contract_validator.py"),
                "search",
                str(search),
            ],
            "contract_validator search",
        )
        self.run_cmd(
            [
                self.python,
                str(self.skill_dir / "scripts/contract_validator.py"),
                "search-brief",
                str(search_brief),
            ],
            "contract_validator search-brief",
        )
        self.echo("[OK] step 2")

    def check_step3(self) -> None:
        self.echo("== Step 3 ==")
        outline = self.output_dir / "outline.txt"
        self.must_file(outline)
        self.run_cmd(
            [
                self.python,
                str(self.skill_dir / "scripts/contract_validator.py"),
                "outline",
                str(outline),
            ],
            "contract_validator outline",
        )
        self.echo("[OK] step 3")

    def check_step4(self) -> None:
        self.echo("== Step 4 ==")
        planning_dir = self.output_dir / "planning"
        self.must_dir(planning_dir)
        self.run_cmd(
            [
                self.python,
                str(self.skill_dir / "scripts/planning_validator.py"),
                str(planning_dir),
                "--refs",
                str(self.skill_dir / "references"),
            ],
            "planning_validator",
        )
        self.run_cmd(
            [
                self.python,
                str(self.skill_dir / "scripts/contract_validator.py"),
                "images",
                str(planning_dir),
            ],
            "contract_validator images (step4)",
        )
        pages = load_planning_pages(planning_dir)
        if not pages:
            self.fail("planning pages must be > 0")
        self.pages = len(pages)
        self.echo(f"[OK] step 4 (pages={self.pages})")

    def ensure_pages(self) -> int:
        if self.pages is not None:
            return self.pages
        planning_dir = self.output_dir / "planning"
        self.must_dir(planning_dir)
        pages = load_planning_pages(planning_dir)
        if not pages:
            self.fail("planning pages must be > 0")
        self.pages = len(pages)
        return self.pages

    def check_step5a(self) -> None:
        self.echo("== Step 5a ==")
        style = self.output_dir / "style.json"
        self.must_file(style)
        self.run_cmd(
            [
                self.python,
                str(self.skill_dir / "scripts/contract_validator.py"),
                "style",
                str(style),
            ],
            "contract_validator style",
        )
        self.echo("[OK] step 5a")

    def check_step5b(self) -> None:
        self.echo("== Step 5b ==")
        images_dir = self.output_dir / "images"
        planning_dir = self.output_dir / "planning"
        self.must_dir(images_dir)
        self.must_dir(planning_dir)
        self.run_cmd(
            [
                self.python,
                str(self.skill_dir / "scripts/contract_validator.py"),
                "images",
                str(planning_dir),
                "--require-paths",
            ],
            "contract_validator images --require-paths",
        )
        self.echo("[OK] step 5b")

    def check_step5c(self) -> None:
        self.echo("== Step 5c ==")
        pages = self.ensure_pages()
        slides_dir = self.output_dir / "slides"
        png_dir = self.output_dir / "png"
        self.must_dir(slides_dir)
        slides = sorted(slides_dir.glob("slide-*.html"), key=natural_sort_key)
        if len(slides) != pages:
            self.fail(f"slide count={len(slides)} != planning pages={pages}")
        # PNG screenshots should exist for each page
        if png_dir.is_dir():
            pngs = sorted(png_dir.glob("slide-*.png"), key=natural_sort_key)
            if len(pngs) != pages:
                self.fail(f"png count={len(pngs)} != planning pages={pages}")
        self.echo("[OK] step 5c")

    def check_step5d(self) -> None:
        self.echo("== Step 5d ==")
        pages = self.ensure_pages()
        png_dir = self.output_dir / "png"
        self.must_dir(png_dir)
        # Verify all pages have review-pass markers or PNG files
        pngs = sorted(png_dir.glob("slide-*.png"), key=natural_sort_key)
        if len(pngs) != pages:
            self.fail(f"png count={len(pngs)} != planning pages={pages} (review incomplete)")
        self.echo("[OK] step 5d")

    def check_preview(self) -> None:
        self.echo("== Step 5d 后预览 ==")
        self.must_file(self.output_dir / "preview.html")
        self.echo("[OK] preview")

    def check_step6(self) -> None:
        self.echo("== Step 6 ==")
        self.must_file(self.output_dir / "presentation.pptx")
        pngs = list((self.output_dir / "png").glob("*.png")) if (self.output_dir / "png").is_dir() else []
        svgs = list((self.output_dir / "svg").glob("*.svg")) if (self.output_dir / "svg").is_dir() else []
        if not pngs and not svgs:
            self.fail("neither png/*.png nor svg/*.svg found")
        self.echo("[OK] step 6")

    def run(self) -> None:
        required_scripts = [
            self.skill_dir / "scripts/progress_validator.py",
            self.skill_dir / "scripts/contract_validator.py",
            self.skill_dir / "scripts/planning_validator.py",
        ]
        for path in required_scripts:
            self.must_file(path)

        if self.reached("0"):
            self.check_step0()
        if self.reached("1"):
            self.check_step1()
        if self.reached("2"):
            self.check_step2()
        if self.reached("3"):
            self.check_step3()
        if self.reached("4"):
            self.check_step4()
        if self.reached("5a"):
            self.check_step5a()
        if self.reached("5b"):
            self.check_step5b()
        if self.reached("5c"):
            self.check_step5c()
        if self.reached("5d"):
            self.check_step5d()
        if self.reached("preview"):
            self.check_preview()
        if self.reached("6"):
            self.check_step6()

        self.echo("[PASS] milestone checks passed")


def normalize_stage(raw: str) -> str:
    key = raw.strip().lower().replace(" ", "")
    stage = STAGE_ALIAS.get(key)
    if not stage:
        raise ValueError(f"unsupported stage: {raw!r}; expected one of {STAGE_ORDER}")
    return stage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run milestone acceptance checks for the PPT workflow")
    parser.add_argument("stage", help="Milestone target: 0/1/2/3/4/5a/5b/5c/5d/preview/6")
    parser.add_argument(
        "--skill-dir",
        default=str(Path(__file__).resolve().parent.parent),
        help="Skill root directory (default: auto-detected from this script)",
    )
    parser.add_argument(
        "--output-dir",
        default="ppt-output",
        help="Workflow output directory (default: ./ppt-output)",
    )
    parser.add_argument("--quiet", action="store_true", help="Only print failures")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        target = normalize_stage(args.stage)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    skill_dir = Path(args.skill_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    checker = Checker(skill_dir=skill_dir, output_dir=output_dir, target=target, quiet=bool(args.quiet))
    try:
        checker.run()
    except Exception as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
