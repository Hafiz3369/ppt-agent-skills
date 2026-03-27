#!/usr/bin/env python3
"""Validate progress.json lifecycle contracts.

Usage:
  python3 scripts/progress_validator.py OUTPUT_DIR/progress.json
  python3 scripts/progress_validator.py OUTPUT_DIR/progress.json --require-pre-step1
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from planning_validator import load_jsonish


STATUS_VALUES = {"done", "in_progress", "pending"}
COMPLEXITY_VALUES = {"light", "standard", "large"}
STEP_KEYS = (
    "step_1",
    "step_2",
    "step_3",
    "step_4",
    "step_5a",
    "step_5b",
    "step_5c",
    "step_5d",
    "step_6",
)
REVIEW_MODE_VALUES = {"auto", "vision", "source"}


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def ok(self) -> bool:
        return not self.errors


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def parse_iso_timestamp(label: str, value: Any, result: ValidationResult) -> datetime | None:
    if not is_non_empty_string(value):
        result.error(f"{label}: must be a non-empty ISO timestamp string")
        return None
    raw = str(value).strip()
    normalized = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        result.error(f"{label}: invalid ISO timestamp {value!r}")
        return None


def validate_page_list(
    value: Any,
    label: str,
    total_pages: int | None,
    result: ValidationResult,
) -> list[int]:
    if not isinstance(value, list):
        result.error(f"{label}: must be a list")
        return []
    pages: list[int] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, int):
            result.error(f"{label}[{index}]: must be an integer")
            continue
        if item < 1:
            result.error(f"{label}[{index}]: must be >= 1")
            continue
        if total_pages is not None and item > total_pages:
            result.error(f"{label}[{index}]: exceeds total_pages={total_pages}")
            continue
        pages.append(item)
    if len(set(pages)) != len(pages):
        result.error(f"{label}: duplicate page indexes are not allowed")
    return pages


def read_payload(path: Path) -> dict[str, Any]:
    payload = load_jsonish(path)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    if isinstance(payload.get("progress"), dict):
        return payload["progress"]
    return payload


def validate_status_entry(
    steps: dict[str, Any],
    step_key: str,
    result: ValidationResult,
) -> dict[str, Any]:
    entry = steps.get(step_key)
    if not isinstance(entry, dict):
        result.error(f"steps.{step_key}: must be an object")
        return {}
    status = entry.get("status")
    if status not in STATUS_VALUES:
        result.error(f"steps.{step_key}.status: must be one of {sorted(STATUS_VALUES)}")
    return entry


def is_nullish(value: Any) -> bool:
    return value in (None, "", "null")


def validate_pre_step1(
    steps: dict[str, Any],
    step_entries: dict[str, dict[str, Any]],
    result: ValidationResult,
) -> None:
    for step_key in STEP_KEYS:
        status = steps.get(step_key, {}).get("status")
        if status != "pending":
            result.error(f"--require-pre-step1: steps.{step_key}.status must be 'pending'")

    step4 = step_entries.get("step_4", {})
    if step4.get("completed_pages") not in (None, []):
        result.error("--require-pre-step1: steps.step_4.completed_pages must be []")
    if not is_nullish(step4.get("current_page")):
        result.error("--require-pre-step1: steps.step_4.current_page must be null")

    for step_key in ("step_5b", "step_5c"):
        entry = step_entries.get(step_key, {})
        if entry.get("completed_pages") not in (None, []):
            result.error(f"--require-pre-step1: steps.{step_key}.completed_pages must be []")

    step5d = step_entries.get("step_5d", {})
    if step5d.get("round") not in (None, 0):
        result.error("--require-pre-step1: steps.step_5d.round must be 0")
    if not is_nullish(step5d.get("mode")):
        result.error("--require-pre-step1: steps.step_5d.mode must be null")

    step6 = step_entries.get("step_6", {})
    if not is_nullish(step6.get("pipeline")):
        result.error("--require-pre-step1: steps.step_6.pipeline must be null")


def validate_progress(path: Path, require_pre_step1: bool) -> tuple[ValidationResult, dict[str, Any]]:
    result = ValidationResult()
    data = read_payload(path)

    for field_name in ("version", "topic", "complexity", "total_pages", "started_at", "last_updated", "steps"):
        if field_name not in data:
            result.error(f"missing required field: {field_name}")

    if result.errors:
        return result, {"errors": len(result.errors), "warnings": 0}

    if not is_non_empty_string(data.get("version")):
        result.error("version: must be a non-empty string")
    if not is_non_empty_string(data.get("topic")):
        result.error("topic: must be a non-empty string")

    complexity = data.get("complexity")
    if complexity not in COMPLEXITY_VALUES:
        result.error(f"complexity: must be one of {sorted(COMPLEXITY_VALUES)}")

    total_pages_raw = data.get("total_pages")
    total_pages: int | None = None
    if not isinstance(total_pages_raw, int) or total_pages_raw <= 0:
        result.error("total_pages: must be a positive integer")
    else:
        total_pages = total_pages_raw

    started_at = parse_iso_timestamp("started_at", data.get("started_at"), result)
    last_updated = parse_iso_timestamp("last_updated", data.get("last_updated"), result)
    if started_at and last_updated and last_updated < started_at:
        result.error("last_updated: must be >= started_at")

    steps = data.get("steps")
    if not isinstance(steps, dict):
        result.error("steps: must be an object")
        return result, {"errors": len(result.errors), "warnings": len(result.warnings)}

    missing_steps = [key for key in STEP_KEYS if key not in steps]
    if missing_steps:
        result.error(f"steps missing keys: {missing_steps}")

    extra_steps = [key for key in steps.keys() if key not in STEP_KEYS]
    if extra_steps:
        result.warn(f"steps has unknown keys: {extra_steps}")

    step_entries: dict[str, dict[str, Any]] = {}
    in_progress_steps: list[str] = []
    for step_key in STEP_KEYS:
        if step_key not in steps:
            continue
        entry = validate_status_entry(steps, step_key, result)
        step_entries[step_key] = entry
        if entry.get("status") == "in_progress":
            in_progress_steps.append(step_key)

    if len(in_progress_steps) > 1:
        result.error(f"at most one step can be in_progress, got: {in_progress_steps}")

    step4 = step_entries.get("step_4", {})
    step4_pages = validate_page_list(step4.get("completed_pages", []), "steps.step_4.completed_pages", total_pages, result)
    current_page = step4.get("current_page")
    if not is_nullish(current_page):
        if not isinstance(current_page, int):
            result.error("steps.step_4.current_page: must be integer or null")
        elif current_page < 1:
            result.error("steps.step_4.current_page: must be >= 1")
        elif total_pages is not None and current_page > total_pages:
            result.error(f"steps.step_4.current_page: exceeds total_pages={total_pages}")
    if step4.get("status") == "done" and total_pages is not None and len(step4_pages) != total_pages:
        result.warn("steps.step_4.status=done but completed_pages does not cover all pages")

    for step_key in ("step_5b", "step_5c"):
        entry = step_entries.get(step_key, {})
        pages = validate_page_list(entry.get("completed_pages", []), f"steps.{step_key}.completed_pages", total_pages, result)
        if entry.get("status") == "done" and total_pages is not None and len(pages) != total_pages:
            result.warn(f"steps.{step_key}.status=done but completed_pages does not cover all pages")

    step5d = step_entries.get("step_5d", {})
    round_value = step5d.get("round")
    if not isinstance(round_value, int) or round_value < 0:
        result.error("steps.step_5d.round: must be an integer >= 0")
    mode = step5d.get("mode")
    if not is_nullish(mode) and mode not in REVIEW_MODE_VALUES:
        result.error(f"steps.step_5d.mode: must be null or one of {sorted(REVIEW_MODE_VALUES)}")

    step6 = step_entries.get("step_6", {})
    pipeline = step6.get("pipeline")
    if not is_nullish(pipeline) and not is_non_empty_string(pipeline):
        result.error("steps.step_6.pipeline: must be null or non-empty string")

    if require_pre_step1:
        validate_pre_step1(steps, step_entries, result)

    summary = {
        "version": data.get("version"),
        "complexity": data.get("complexity"),
        "total_pages": total_pages,
        "in_progress_steps": in_progress_steps,
        "require_pre_step1": require_pre_step1,
        "errors": len(result.errors),
        "warnings": len(result.warnings),
    }
    return result, summary


def print_messages(result: ValidationResult) -> None:
    for item in result.errors:
        print(f"ERROR: {item}")
    for item in result.warnings:
        print(f"WARN:  {item}")


def write_report(path: str | None, payload: dict[str, Any]) -> None:
    if not path:
        return
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate progress.json lifecycle contracts")
    parser.add_argument("path", help="Path to progress.json")
    parser.add_argument(
        "--require-pre-step1",
        action="store_true",
        help="Fail unless progress.json is in initialized pre-Step-1 state",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--report", help="Optional JSON report path")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"ERROR: path not found: {target}", file=sys.stderr)
        return 1

    try:
        result, summary = validate_progress(target, bool(args.require_pre_step1))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print_messages(result)
    if not result.errors and not result.warnings:
        print("OK")

    ok = result.ok and (not args.strict or not result.warnings)
    write_report(
        args.report,
        {
            "command": "progress",
            "ok": ok,
            "summary": summary,
            "errors": result.errors,
            "warnings": result.warnings,
        },
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
