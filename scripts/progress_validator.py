#!/usr/bin/env python3
"""Validate progress.json for the PPT workflow v4.

Usage:
  python3 scripts/progress_validator.py OUTPUT_DIR/progress.json
  python3 scripts/progress_validator.py OUTPUT_DIR/progress.json --require-pre-step1
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from planning_validator import load_jsonish


STEP_STATUS_VALUES = {
    "pending",
    "in_progress",
    "wait_user",
    "wait_agent",
    "done",
    "failed",
    "rolled_back",
}
RUN_STATE_VALUES = {"RUNNING", "WAIT_USER", "WAIT_AGENT", "ROLLBACK", "DONE", "FAILED"}
WAIT_TYPE_VALUES = {"WAIT_USER", "WAIT_AGENT"}
BRANCH_VALUES = {"research", "direct"}
PAGE_STATUS_VALUES = {"pending", "in_progress", "failed", "done", "rolled_back"}
PAGE_PHASE_VALUES = {
    "planning",
    "planning_review",
    "html",
    "render_png",
    "image_review_round1",
    "image_review_round2",
    "closed",
}


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


def read_payload(path: Path) -> dict[str, Any]:
    payload = load_jsonish(path)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    if isinstance(payload.get("progress"), dict):
        return payload["progress"]
    return payload


def normalize_state(value: Any) -> str | None:
    if not is_non_empty_string(value):
        return None
    return str(value).strip().upper()


def normalize_branch(value: Any) -> str | None:
    if value in (None, "", "null"):
        return None
    if not isinstance(value, str):
        return str(value)
    return value.strip().lower()


def validate_step_id(step_id: str, result: ValidationResult) -> None:
    pattern = r"^P(?:0|1|2A|2B|3|4|5)\.\d{2}(?:\[(?:WAIT_USER|WAIT_AGENT)\])?$"
    if not re.match(pattern, step_id):
        result.warn(
            f"steps[].id={step_id!r}: non-canonical id format; expected e.g. P4.03 or P1.02[WAIT_USER]"
        )


def normalize_steps(raw_steps: Any, result: ValidationResult) -> list[dict[str, Any]]:
    if isinstance(raw_steps, list):
        steps = [item for item in raw_steps if isinstance(item, dict)]
        if len(steps) != len(raw_steps):
            result.error("steps: list entries must be objects")
        return steps

    if isinstance(raw_steps, dict):
        steps: list[dict[str, Any]] = []
        for step_id, entry in raw_steps.items():
            if not isinstance(entry, dict):
                result.error(f"steps.{step_id}: must be an object")
                continue
            merged = dict(entry)
            merged.setdefault("id", str(step_id))
            steps.append(merged)
        return steps

    result.error("steps: must be a list or object")
    return []


def validate_steps(steps: list[dict[str, Any]], result: ValidationResult) -> dict[str, Any]:
    ids: set[str] = set()
    status_counts: dict[str, int] = {key: 0 for key in STEP_STATUS_VALUES}
    in_progress: list[str] = []
    wait_user: list[str] = []
    wait_agent: list[str] = []
    rolled_back: list[str] = []

    for index, step in enumerate(steps, start=1):
        label = f"steps[{index}]"
        step_id_raw = step.get("id")
        if not is_non_empty_string(step_id_raw):
            result.error(f"{label}.id: must be a non-empty string")
            continue
        step_id = str(step_id_raw).strip()
        validate_step_id(step_id, result)

        if step_id in ids:
            result.error(f"{label}.id: duplicate step id {step_id!r}")
            continue
        ids.add(step_id)

        action = step.get("action")
        if not is_non_empty_string(action):
            result.error(f"{label}.action: must be a non-empty string")

        status = str(step.get("status") or "").strip().lower()
        if status not in STEP_STATUS_VALUES:
            result.error(f"{label}.status: must be one of {sorted(STEP_STATUS_VALUES)}")
            continue

        status_counts[status] = status_counts.get(status, 0) + 1
        if status == "in_progress":
            in_progress.append(step_id)
        elif status == "wait_user":
            wait_user.append(step_id)
        elif status == "wait_agent":
            wait_agent.append(step_id)
        elif status == "rolled_back":
            rolled_back.append(step_id)

        wait_type = step.get("wait_type")
        if status in {"wait_user", "wait_agent"}:
            if not is_non_empty_string(wait_type):
                result.error(f"{label}.wait_type: required when status={status}")
            else:
                wait_type_norm = str(wait_type).strip().upper()
                if wait_type_norm not in WAIT_TYPE_VALUES:
                    result.error(f"{label}.wait_type: must be one of {sorted(WAIT_TYPE_VALUES)}")
                elif status == "wait_user" and wait_type_norm != "WAIT_USER":
                    result.error(f"{label}.wait_type must be WAIT_USER when status=wait_user")
                elif status == "wait_agent" and wait_type_norm != "WAIT_AGENT":
                    result.error(f"{label}.wait_type must be WAIT_AGENT when status=wait_agent")
        elif wait_type not in (None, "", "null"):
            result.warn(f"{label}.wait_type: should be empty when status={status}")

        rollback_to = step.get("rollback_to")
        if status == "rolled_back" and not is_non_empty_string(rollback_to):
            result.error(f"{label}.rollback_to: required when status=rolled_back")
        if status != "rolled_back" and rollback_to not in (None, "", "null"):
            result.warn(f"{label}.rollback_to: should be empty when status={status}")

        updated_at = step.get("updated_at")
        if updated_at not in (None, "", "null"):
            parse_iso_timestamp(f"{label}.updated_at", updated_at, result)

        if "[WAIT_USER]" in step_id and status != "wait_user":
            result.error(f"{label}: step id suffix [WAIT_USER] requires status=wait_user")
        if "[WAIT_AGENT]" in step_id and status != "wait_agent":
            result.error(f"{label}: step id suffix [WAIT_AGENT] requires status=wait_agent")

    if len(in_progress) > 1:
        result.error(f"at most one step can be in_progress, got: {in_progress}")

    return {
        "step_ids": ids,
        "status_counts": status_counts,
        "in_progress": in_progress,
        "wait_user": wait_user,
        "wait_agent": wait_agent,
        "rolled_back": rolled_back,
    }


def validate_page_items(pages_obj: dict[str, Any], result: ValidationResult) -> dict[str, Any]:
    total_raw = pages_obj.get("total")
    if not isinstance(total_raw, int) or total_raw <= 0:
        result.error("pages.total: must be a positive integer")
        total = None
    else:
        total = total_raw

    items_raw = pages_obj.get("items")
    if not isinstance(items_raw, list):
        result.error("pages.items: must be a list")
        items: list[dict[str, Any]] = []
    else:
        items = [item for item in items_raw if isinstance(item, dict)]
        if len(items) != len(items_raw):
            result.error("pages.items: each entry must be an object")

    seen_pages: set[int] = set()
    completed_pages: list[int] = []
    in_progress_pages: list[int] = []
    failed_pages: list[int] = []

    for index, item in enumerate(items, start=1):
        label = f"pages.items[{index}]"
        page = item.get("page")
        if not isinstance(page, int) or page <= 0:
            result.error(f"{label}.page: must be a positive integer")
            continue
        if total is not None and page > total:
            result.error(f"{label}.page: exceeds pages.total={total}")
        if page in seen_pages:
            result.error(f"{label}.page: duplicate page index {page}")
            continue
        seen_pages.add(page)

        status = str(item.get("status") or "").strip().lower()
        if status not in PAGE_STATUS_VALUES:
            result.error(f"{label}.status: must be one of {sorted(PAGE_STATUS_VALUES)}")
        elif status == "done":
            completed_pages.append(page)
        elif status == "in_progress":
            in_progress_pages.append(page)
        elif status == "failed":
            failed_pages.append(page)

        phase = item.get("current_phase")
        if not is_non_empty_string(phase):
            result.error(f"{label}.current_phase: must be a non-empty string")
        else:
            phase_norm = str(phase).strip().lower()
            if phase_norm not in PAGE_PHASE_VALUES:
                result.error(f"{label}.current_phase: must be one of {sorted(PAGE_PHASE_VALUES)}")
            if status == "done" and phase_norm != "closed":
                result.warn(f"{label}: status=done but current_phase is {phase_norm!r}, expected 'closed'")

        artifacts = item.get("artifacts")
        if artifacts is not None and not isinstance(artifacts, dict):
            result.error(f"{label}.artifacts: must be an object when provided")

    if total is not None and len(items) > total:
        result.error("pages.items: entry count cannot exceed pages.total")

    return {
        "total": total,
        "items": len(items),
        "completed_pages": sorted(completed_pages),
        "in_progress_pages": sorted(in_progress_pages),
        "failed_pages": sorted(failed_pages),
    }


def validate_pre_step1(data: dict[str, Any], steps: list[dict[str, Any]], page_summary: dict[str, Any], result: ValidationResult) -> None:
    for index, step in enumerate(steps, start=1):
        step_id = str(step.get("id") or "")
        status = str(step.get("status") or "").strip().lower()
        if step_id.startswith("P0."):
            continue
        if status != "pending":
            result.error(f"--require-pre-step1: steps[{index}] ({step_id}) must be pending")

    current_step = data.get("current_step")
    if current_step not in (None, "", "null") and not str(current_step).startswith("P0."):
        result.error("--require-pre-step1: current_step must be empty or a P0.* step")

    branch = normalize_branch(data.get("branch"))
    if branch in BRANCH_VALUES:
        result.error("--require-pre-step1: branch must be empty before Step 1 decision")

    for name in ("completed_pages", "in_progress_pages", "failed_pages"):
        values = page_summary.get(name) or []
        if values:
            result.error(f"--require-pre-step1: pages.{name} must be empty")


def validate_progress(path: Path, require_pre_step1: bool) -> tuple[ValidationResult, dict[str, Any]]:
    result = ValidationResult()
    data = read_payload(path)

    required_fields = (
        "version",
        "run_id",
        "topic",
        "state",
        "started_at",
        "last_updated",
        "steps",
    )
    for field_name in required_fields:
        if field_name not in data:
            result.error(f"missing required field: {field_name}")

    if result.errors:
        return result, {"errors": len(result.errors), "warnings": 0}

    if not is_non_empty_string(data.get("version")):
        result.error("version: must be a non-empty string")
    if not is_non_empty_string(data.get("run_id")):
        result.error("run_id: must be a non-empty string")
    if not is_non_empty_string(data.get("topic")):
        result.error("topic: must be a non-empty string")

    state = normalize_state(data.get("state"))
    if state not in RUN_STATE_VALUES:
        result.error(f"state: must be one of {sorted(RUN_STATE_VALUES)}")

    branch = normalize_branch(data.get("branch"))
    if branch is not None and branch not in BRANCH_VALUES:
        result.error(f"branch: must be null or one of {sorted(BRANCH_VALUES)}")

    started_at = parse_iso_timestamp("started_at", data.get("started_at"), result)
    last_updated = parse_iso_timestamp("last_updated", data.get("last_updated"), result)
    if started_at and last_updated and last_updated < started_at:
        result.error("last_updated: must be >= started_at")

    steps = normalize_steps(data.get("steps"), result)
    if not steps:
        result.error("steps: must contain at least one step")

    step_summary = validate_steps(steps, result)
    step_ids = step_summary.get("step_ids", set())

    current_step = data.get("current_step")
    if current_step not in (None, "", "null"):
        if not is_non_empty_string(current_step):
            result.error("current_step: must be string or null")
        elif str(current_step).strip() not in step_ids:
            result.error("current_step: must match an existing steps[].id")

    page_summary = {
        "total": None,
        "items": 0,
        "completed_pages": [],
        "in_progress_pages": [],
        "failed_pages": [],
    }
    pages = data.get("pages")
    if pages is not None:
        if not isinstance(pages, dict):
            result.error("pages: must be an object when provided")
        else:
            page_summary = validate_page_items(pages, result)

    if state == "WAIT_USER" and not step_summary.get("wait_user"):
        result.error("state=WAIT_USER but no step has status=wait_user")
    if state == "WAIT_AGENT" and not step_summary.get("wait_agent"):
        result.error("state=WAIT_AGENT but no step has status=wait_agent")
    if state == "ROLLBACK" and not step_summary.get("rolled_back"):
        result.error("state=ROLLBACK but no step has status=rolled_back")
    if state == "DONE":
        if step_summary.get("in_progress") or step_summary.get("wait_user") or step_summary.get("wait_agent"):
            result.error("state=DONE requires no in_progress/wait_* steps")

    if require_pre_step1:
        validate_pre_step1(data, steps, page_summary, result)

    summary = {
        "version": data.get("version"),
        "run_id": data.get("run_id"),
        "state": state,
        "branch": branch,
        "current_step": data.get("current_step"),
        "step_count": len(steps),
        "status_counts": step_summary.get("status_counts", {}),
        "pages": page_summary,
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
    parser = argparse.ArgumentParser(description="Validate progress.json lifecycle contracts (v4)")
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
