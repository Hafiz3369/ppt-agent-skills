#!/usr/bin/env python3
"""Validate presearch context contract used before Step 1 questionnaire.

Usage:
  python3 scripts/presearch_validator.py OUTPUT_DIR/runtime/presearch-context.json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

CONFIDENCE_VALUES = {"high", "medium", "low", "unknown"}


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


def is_string_or_null(value: Any) -> bool:
    return value is None or isinstance(value, str)


def load_payload(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("payload must be a JSON object")
    wrapped = data.get("presearch_context")
    if isinstance(wrapped, dict):
        return wrapped
    return data


def validate_presearch(path: Path, min_queries: int, min_dimensions: int, min_question_hints: int) -> tuple[ValidationResult, dict[str, Any]]:
    result = ValidationResult()
    data = load_payload(path)

    for field_name in ("topic", "generated_at", "search_enabled", "queries", "findings", "question_hints", "no_search_reason"):
        if field_name not in data:
            result.error(f"missing required field: {field_name}")

    if result.errors:
        return result, {"errors": len(result.errors), "warnings": len(result.warnings)}

    if not is_non_empty_string(data.get("topic")):
        result.error("topic: must be a non-empty string")
    if not is_non_empty_string(data.get("generated_at")):
        result.error("generated_at: must be a non-empty string")

    search_enabled = data.get("search_enabled")
    if not isinstance(search_enabled, bool):
        result.error("search_enabled: must be boolean")
        search_enabled = False

    no_search_reason = data.get("no_search_reason")
    if not is_string_or_null(no_search_reason):
        result.error("no_search_reason: must be string or null")

    queries = data.get("queries")
    dimensions: set[str] = set()
    if not isinstance(queries, list):
        result.error("queries: must be a list")
        queries = []
    else:
        for index, entry in enumerate(queries, start=1):
            label = f"queries[{index}]"
            if not isinstance(entry, dict):
                result.error(f"{label}: must be an object")
                continue
            for field_name in ("dimension", "query", "tool_used"):
                if not is_non_empty_string(entry.get(field_name)):
                    result.error(f"{label}.{field_name}: must be a non-empty string")
            dim = entry.get("dimension")
            if is_non_empty_string(dim):
                dimensions.add(str(dim).strip())

    findings = data.get("findings")
    if not isinstance(findings, list):
        result.error("findings: must be a list")
        findings = []
    else:
        for index, finding in enumerate(findings, start=1):
            label = f"findings[{index}]"
            if not isinstance(finding, dict):
                result.error(f"{label}: must be an object")
                continue
            if not is_non_empty_string(finding.get("insight")):
                result.error(f"{label}.insight: must be a non-empty string")
            if not is_string_or_null(finding.get("source")):
                result.error(f"{label}.source: must be string or null")
            confidence = finding.get("confidence")
            if not is_non_empty_string(confidence):
                result.error(f"{label}.confidence: must be a non-empty string")
            elif str(confidence).strip() not in CONFIDENCE_VALUES:
                result.warn(f"{label}.confidence: unexpected value {confidence!r}")

    question_hints = data.get("question_hints")
    if not isinstance(question_hints, list):
        result.error("question_hints: must be a list")
        question_hints = []
    else:
        for index, item in enumerate(question_hints, start=1):
            if not is_non_empty_string(item):
                result.error(f"question_hints[{index}]: must be a non-empty string")

    if search_enabled:
        if len(queries) < min_queries:
            result.error(f"queries: require at least {min_queries} entries when search_enabled=true")
        if len(dimensions) < min_dimensions:
            result.error(f"queries: require at least {min_dimensions} unique dimensions when search_enabled=true")
        if is_non_empty_string(no_search_reason):
            result.warn("no_search_reason: should be null when search_enabled=true")
    else:
        if not is_non_empty_string(no_search_reason):
            result.error("no_search_reason: required when search_enabled=false")
        if queries:
            result.warn("queries: should usually be empty when search_enabled=false")

    if len(question_hints) < min_question_hints:
        result.error(f"question_hints: require at least {min_question_hints} hints")

    summary = {
        "search_enabled": bool(search_enabled),
        "total_queries": len(queries),
        "total_dimensions": len(dimensions),
        "total_findings": len(findings),
        "total_question_hints": len(question_hints),
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
    parser = argparse.ArgumentParser(description="Validate presearch context before questionnaire")
    parser.add_argument("path", help="Path to presearch-context.json")
    parser.add_argument("--min-queries", type=int, default=3, help="Minimum queries when search_enabled=true")
    parser.add_argument("--min-dimensions", type=int, default=3, help="Minimum unique dimensions when search_enabled=true")
    parser.add_argument("--min-question-hints", type=int, default=3, help="Minimum question hints")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--report", help="Optional JSON report path")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"ERROR: path not found: {target}", file=sys.stderr)
        return 1

    try:
        result, summary = validate_presearch(
            target,
            min_queries=max(1, int(args.min_queries)),
            min_dimensions=max(1, int(args.min_dimensions)),
            min_question_hints=max(1, int(args.min_question_hints)),
        )
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
            "command": "presearch",
            "ok": ok,
            "summary": summary,
            "errors": result.errors,
            "warnings": result.warnings,
        },
    )

    if result.errors:
        return 1
    if args.strict and result.warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
