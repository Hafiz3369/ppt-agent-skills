#!/usr/bin/env python3
"""Validate workflow contracts that are lighter than full review gates.

Supported contracts:
- requirements.json
- style.json
- planning image contracts
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from planning_validator import (
    VALID_IMAGE_PLACEMENTS,
    VALID_IMAGE_USAGES,
    as_list,
    load_jsonish,
    load_planning_pages,
)


REQUIREMENTS_REQUIRED_FIELDS = (
    "topic",
    "scene",
    "audience",
    "purpose",
    "narrative_structure",
    "emphasis",
    "persuasion_style",
    "style_choice",
    "style_detail",
    "page_count",
    "info_density",
    "brand_info",
    "content_must_include",
    "content_must_avoid",
    "language",
    "image_preference",
    "dynamic_answers",
    "complexity_level",
)
REQUIREMENTS_BRAND_FIELDS = ("presenter", "date", "company", "brand_color", "logo_path")
STYLE_REQUIRED_FIELDS = (
    "style_id",
    "style_name",
    "mood_keywords",
    "design_soul",
    "variation_strategy",
    "decoration_dna",
    "css_variables",
    "font_family",
)
STYLE_CSS_VARIABLES = (
    "bg_primary",
    "bg_secondary",
    "card_bg_from",
    "card_bg_to",
    "card_border",
    "card_radius",
    "text_primary",
    "text_secondary",
    "accent_1",
    "accent_2",
    "accent_3",
    "accent_4",
)
STYLE_CSS_SNIPPETS = (
    "title_style",
    "list_marker",
    "body_text",
    "page_number",
    "card_padding",
    "section_gap",
)
COMPLEXITY_VALUES = {"light", "standard", "large"}
SCENE_VALUES = {"live_speech", "self_read", "training", "other", "现场演讲", "自阅文档", "培训教学", "其他"}
PURPOSE_VALUES = {"decision", "understand", "execute", "shift_perception", "other", "做决策", "理解并记住", "学会并执行", "改变认知", "其他"}
NARRATIVE_VALUES = {
    "problem_solution_effect",
    "what_why_how",
    "panorama_focus_action",
    "comparison",
    "timeline",
    "custom",
    "问题->方案->效果",
    "问题 -> 方案 -> 效果",
    "是什么->为什么->怎么做",
    "是什么 -> 为什么 -> 怎么做",
    "全景->聚焦->行动",
    "全景 -> 聚焦 -> 行动",
    "对比论证",
    "时间线",
    "自定义",
}
LANGUAGE_VALUES = {"zh", "en", "zh_en_mix", "other", "中文", "英文", "中英混排", "其他"}
IMAGE_PREFERENCE_VALUES = {"none", "key_pages", "every_page", "user_provided", "不需要", "关键页配图", "每页配图", "用户提供素材"}
RAW_RESEARCH_QUERY_FIELDS = ("dimension", "query", "tool_used", "raw_findings")
RAW_FINDING_FIELDS = ("content", "source_url", "source_name")
RESEARCH_PACKAGE_META_FIELDS = ("topic", "total_materials", "by_reliability", "by_category", "coverage_report", "timestamp")
RESEARCH_MATERIAL_FIELDS = ("id", "fact", "source", "reliability", "categories", "relevance_to")
RELIABILITY_VALUES = {"high", "medium", "low"}
OUTLINE_REVIEW_SCORE_KEYS = (
    "narrative_structure",
    "argument_strategy",
    "material_consumption",
    "page_design",
    "requirement_fidelity",
)


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


def unwrap_payload(path: Path, primary_key: str, legacy_key: str | None = None) -> dict[str, Any]:
    payload = load_jsonish(path)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    if isinstance(payload.get(primary_key), dict):
        return payload[primary_key]
    if legacy_key and isinstance(payload.get(legacy_key), dict):
        return payload[legacy_key]
    return payload


def validate_enum(label: str, value: Any, allowed: set[str], result: ValidationResult) -> None:
    if not is_non_empty_string(value):
        result.error(f"{label}: must be a non-empty string")
    elif str(value).strip() not in allowed:
        result.warn(f"{label}: unexpected value {value!r}")


def validate_requirements(path: Path) -> tuple[ValidationResult, dict[str, Any]]:
    result = ValidationResult()
    data = unwrap_payload(path, "requirements", "requirement")

    for field_name in REQUIREMENTS_REQUIRED_FIELDS:
        if field_name not in data:
            result.error(f"missing required field: {field_name}")

    if result.errors:
        return result, data

    for field_name in ("topic", "audience", "style_choice", "info_density"):
        if not is_non_empty_string(data.get(field_name)):
            result.error(f"{field_name}: must be a non-empty string")

    for label, field_name, allowed in (
        ("scene", "scene", SCENE_VALUES),
        ("purpose", "purpose", PURPOSE_VALUES),
        ("narrative_structure", "narrative_structure", NARRATIVE_VALUES),
        ("language", "language", LANGUAGE_VALUES),
        ("image_preference", "image_preference", IMAGE_PREFERENCE_VALUES),
    ):
        validate_enum(label, data.get(field_name), allowed, result)

    complexity = data.get("complexity_level")
    if complexity not in COMPLEXITY_VALUES:
        result.error(f"complexity_level: must be one of {sorted(COMPLEXITY_VALUES)}")

    style_detail = data.get("style_detail")
    if not is_string_or_null(style_detail):
        result.error("style_detail: must be string or null")

    page_count = data.get("page_count")
    if page_count is not None and not isinstance(page_count, int):
        result.error("page_count: must be integer or null")
    elif isinstance(page_count, int) and page_count <= 0:
        result.error("page_count: must be > 0 when provided")

    for list_field in ("emphasis", "persuasion_style", "content_must_include", "content_must_avoid"):
        value = data.get(list_field)
        if not isinstance(value, list):
            result.error(f"{list_field}: must be a list")
        elif any(not is_non_empty_string(item) for item in value):
            result.error(f"{list_field}: entries must be non-empty strings")

    dynamic_answers = data.get("dynamic_answers")
    if not isinstance(dynamic_answers, dict):
        result.error("dynamic_answers: must be an object")
    else:
        for key, value in dynamic_answers.items():
            if not is_non_empty_string(key):
                result.error("dynamic_answers: question keys must be non-empty strings")
                break
            if not is_string_or_null(value):
                result.error("dynamic_answers: answers must be string or null")
                break

    brand_info = data.get("brand_info")
    if not isinstance(brand_info, dict):
        result.error("brand_info: must be an object")
    else:
        for field_name in REQUIREMENTS_BRAND_FIELDS:
            if field_name not in brand_info:
                result.error(f"brand_info missing field: {field_name}")
            elif not is_string_or_null(brand_info.get(field_name)):
                result.error(f"brand_info.{field_name}: must be string or null")

    if isinstance(page_count, int):
        expected = "light" if page_count <= 8 else "standard" if page_count <= 18 else "large"
        if complexity in COMPLEXITY_VALUES and complexity != expected:
            result.warn(f"complexity_level={complexity!r} but page_count={page_count} suggests {expected!r}")

    return result, data


def validate_style(path: Path) -> tuple[ValidationResult, dict[str, Any]]:
    result = ValidationResult()
    data = unwrap_payload(path, "style")

    for field_name in STYLE_REQUIRED_FIELDS:
        if field_name not in data:
            result.error(f"missing required field: {field_name}")

    if result.errors:
        return result, data

    for field_name in ("style_id", "style_name", "design_soul", "variation_strategy", "font_family"):
        if not is_non_empty_string(data.get(field_name)):
            result.error(f"{field_name}: must be a non-empty string")

    mood_keywords = data.get("mood_keywords")
    if not isinstance(mood_keywords, list):
        result.error("mood_keywords: must be a list")
    else:
        cleaned = [item for item in mood_keywords if is_non_empty_string(item)]
        if len(cleaned) != len(mood_keywords):
            result.error("mood_keywords: entries must be non-empty strings")
        if not 3 <= len(cleaned) <= 5:
            result.error("mood_keywords: must contain 3-5 items")

    decoration = data.get("decoration_dna")
    if not isinstance(decoration, dict):
        result.error("decoration_dna: must be an object")
    else:
        if not is_non_empty_string(decoration.get("signature_move")):
            result.error("decoration_dna.signature_move: must be a non-empty string")
        forbidden = decoration.get("forbidden")
        if not isinstance(forbidden, list):
            result.error("decoration_dna.forbidden: must be a list")
        elif any(not is_non_empty_string(item) for item in forbidden):
            result.error("decoration_dna.forbidden: entries must be non-empty strings")
        recommended = decoration.get("recommended_combos")
        if not isinstance(recommended, list):
            result.error("decoration_dna.recommended_combos: must be a list")
        elif any(not is_non_empty_string(item) for item in recommended):
            result.error("decoration_dna.recommended_combos: entries must be non-empty strings")
        elif not recommended:
            result.error("decoration_dna.recommended_combos: must contain at least one combo")

    css_variables = data.get("css_variables")
    if not isinstance(css_variables, dict):
        result.error("css_variables: must be an object")
    else:
        for field_name in STYLE_CSS_VARIABLES:
            value = css_variables.get(field_name)
            if not is_non_empty_string(value):
                result.error(f"css_variables.{field_name}: must be a non-empty string")

    css_snippets = data.get("css_snippets")
    if css_snippets is None:
        result.warn("css_snippets: missing (prompt_assembler can run, but cross-page typographic anchors will be weaker)")
    elif not isinstance(css_snippets, dict):
        result.error("css_snippets: must be an object when provided")
    else:
        for field_name in STYLE_CSS_SNIPPETS:
            if field_name not in css_snippets:
                result.warn(f"css_snippets.{field_name}: missing")
            elif not is_non_empty_string(css_snippets.get(field_name)):
                result.error(f"css_snippets.{field_name}: must be a non-empty string")

    return result, data


def validate_raw_research(path: Path) -> tuple[ValidationResult, dict[str, Any]]:
    result = ValidationResult()
    data = unwrap_payload(path, "raw_research")
    meta = data.get("meta")
    queries = data.get("queries")

    if not isinstance(meta, dict):
        result.error("meta: must be an object")
    else:
        for field_name in ("topic", "total_queries", "total_findings", "queries_by_dimension", "search_tools_used", "timestamp"):
            if field_name not in meta:
                result.error(f"meta missing field: {field_name}")
        if not is_non_empty_string(meta.get("topic")):
            result.error("meta.topic: must be a non-empty string")
        if not isinstance(meta.get("total_queries"), int) or meta.get("total_queries", 0) <= 0:
            result.error("meta.total_queries: must be a positive integer")
        if not isinstance(meta.get("total_findings"), int) or meta.get("total_findings", 0) < 0:
            result.error("meta.total_findings: must be a non-negative integer")
        if not isinstance(meta.get("queries_by_dimension"), dict):
            result.error("meta.queries_by_dimension: must be an object")
        if not isinstance(meta.get("search_tools_used"), list):
            result.error("meta.search_tools_used: must be a list")

    if not isinstance(queries, list) or not queries:
        result.error("queries: must be a non-empty list")
    else:
        for index, entry in enumerate(queries, start=1):
            label = f"queries[{index}]"
            if not isinstance(entry, dict):
                result.error(f"{label}: must be an object")
                continue
            for field_name in RAW_RESEARCH_QUERY_FIELDS:
                if field_name not in entry:
                    result.error(f"{label}: missing field {field_name}")
            if not is_non_empty_string(entry.get("dimension")):
                result.error(f"{label}.dimension: must be a non-empty string")
            if not is_non_empty_string(entry.get("query")):
                result.error(f"{label}.query: must be a non-empty string")
            if not is_non_empty_string(entry.get("tool_used")):
                result.error(f"{label}.tool_used: must be a non-empty string")
            findings = entry.get("raw_findings")
            if not isinstance(findings, list) or not findings:
                result.error(f"{label}.raw_findings: must be a non-empty list")
            else:
                for finding_index, finding in enumerate(findings, start=1):
                    finding_label = f"{label}.raw_findings[{finding_index}]"
                    if not isinstance(finding, dict):
                        result.error(f"{finding_label}: must be an object")
                        continue
                    for field_name in RAW_FINDING_FIELDS:
                        if not is_non_empty_string(finding.get(field_name)):
                            result.error(f"{finding_label}.{field_name}: must be a non-empty string")

    user_materials = data.get("user_materials")
    if user_materials is not None and not isinstance(user_materials, list):
        result.error("user_materials: must be a list when provided")

    summary = {
        "total_queries": len(queries) if isinstance(queries, list) else 0,
        "total_findings": sum(len(as_list(item.get("raw_findings"))) for item in queries if isinstance(item, dict)) if isinstance(queries, list) else 0,
        "errors": len(result.errors),
        "warnings": len(result.warnings),
    }
    return result, summary


def validate_research_package(path: Path) -> tuple[ValidationResult, dict[str, Any]]:
    result = ValidationResult()
    data = unwrap_payload(path, "research_package")
    meta = data.get("meta")
    materials = data.get("materials")
    gaps = data.get("gaps", [])

    if not isinstance(meta, dict):
        result.error("meta: must be an object")
    else:
        for field_name in RESEARCH_PACKAGE_META_FIELDS:
            if field_name not in meta:
                result.error(f"meta missing field: {field_name}")
        if not is_non_empty_string(meta.get("topic")):
            result.error("meta.topic: must be a non-empty string")
        if not isinstance(meta.get("total_materials"), int) or meta.get("total_materials", 0) < 0:
            result.error("meta.total_materials: must be a non-negative integer")
        for field_name in ("by_reliability", "by_category", "coverage_report"):
            if not isinstance(meta.get(field_name), dict):
                result.error(f"meta.{field_name}: must be an object")

    if not isinstance(materials, list):
        result.error("materials: must be a list")
    else:
        for index, material in enumerate(materials, start=1):
            label = f"materials[{index}]"
            if not isinstance(material, dict):
                result.error(f"{label}: must be an object")
                continue
            for field_name in RESEARCH_MATERIAL_FIELDS:
                if field_name not in material:
                    result.error(f"{label}: missing field {field_name}")
            for field_name in ("id", "fact", "source"):
                if not is_non_empty_string(material.get(field_name)):
                    result.error(f"{label}.{field_name}: must be a non-empty string")
            reliability = material.get("reliability")
            if reliability not in RELIABILITY_VALUES:
                result.error(f"{label}.reliability: must be one of {sorted(RELIABILITY_VALUES)}")
            for field_name in ("categories", "relevance_to"):
                value = material.get(field_name)
                if not isinstance(value, list) or any(not is_non_empty_string(item) for item in value):
                    result.error(f"{label}.{field_name}: must be a list of non-empty strings")

    if not isinstance(gaps, list):
        result.error("gaps: must be a list when provided")

    summary = {
        "total_materials": len(materials) if isinstance(materials, list) else 0,
        "total_gaps": len(gaps) if isinstance(gaps, list) else 0,
        "errors": len(result.errors),
        "warnings": len(result.warnings),
    }
    return result, summary


def validate_outline_review(path: Path, require_pass: bool) -> tuple[ValidationResult, dict[str, Any]]:
    result = ValidationResult()
    data = unwrap_payload(path, "outline_review")

    verdict = data.get("verdict")
    if verdict not in {"pass", "needs_fix"}:
        result.error("verdict: must be 'pass' or 'needs_fix'")

    scores = data.get("scores")
    if not isinstance(scores, dict):
        result.error("scores: must be an object")
    else:
        for key in OUTLINE_REVIEW_SCORE_KEYS:
            value = scores.get(key)
            if not isinstance(value, (int, float)) or not (1 <= value <= 10):
                result.error(f"scores.{key}: must be a number in [1,10]")

    if verdict == "pass":
        if not is_string_or_null(data.get("comments")):
            result.error("comments: must be string or null when verdict=pass")
    elif verdict == "needs_fix":
        issues = data.get("issues")
        if not isinstance(issues, list) or not issues:
            result.error("issues: must be a non-empty list when verdict=needs_fix")
        else:
            for index, issue in enumerate(issues, start=1):
                label = f"issues[{index}]"
                if not isinstance(issue, dict):
                    result.error(f"{label}: must be an object")
                    continue
                for field_name in ("dimension", "problem", "diagnosis", "fix_instruction"):
                    if not is_non_empty_string(issue.get(field_name)):
                        result.error(f"{label}.{field_name}: must be a non-empty string")

    if require_pass and verdict != "pass":
        result.error("outline review has not passed yet")

    summary = {
        "verdict": verdict,
        "errors": len(result.errors),
        "warnings": len(result.warnings),
    }
    return result, summary


def resolve_image_base(target: Path) -> Path:
    if target.is_dir():
        return target.parent if target.name == "planning" else target
    if target.parent.name == "planning":
        return target.parent.parent
    return target.parent


def resolve_image_path(base_dir: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def validate_images(path: Path, require_paths: bool) -> tuple[ValidationResult, dict[str, Any]]:
    result = ValidationResult()
    pages = load_planning_pages(path)
    base_dir = resolve_image_base(path)
    summary: dict[str, Any] = {
        "total_pages": len(pages),
        "pages_with_required_images": 0,
        "image_cards": 0,
        "errors": 0,
        "warnings": 0,
    }

    for page in pages:
        slide_number = page.get("slide_number")
        label = f"slide {slide_number if slide_number is not None else '?'}"
        cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
        page_required_images = 0

        for index, card in enumerate(cards, start=1):
            image = card.get("image")
            card_label = f"{label} card[{index}]"
            if not isinstance(image, dict):
                result.error(f"{card_label}: missing image contract")
                continue

            needed = image.get("needed")
            if not isinstance(needed, bool):
                result.error(f"{card_label}: image.needed must be boolean")
                continue

            summary["image_cards"] += 1
            if needed:
                page_required_images += 1
                for field_name in ("usage", "placement", "content_description", "source_hint"):
                    if not is_non_empty_string(image.get(field_name)):
                        result.error(f"{card_label}: image.{field_name} must be a non-empty string when needed=true")
                if image.get("usage") not in VALID_IMAGE_USAGES:
                    result.error(f"{card_label}: invalid image.usage {image.get('usage')!r}")
                if image.get("placement") not in VALID_IMAGE_PLACEMENTS:
                    result.error(f"{card_label}: invalid image.placement {image.get('placement')!r}")

                raw_path = image.get("path")
                if require_paths:
                    if not is_non_empty_string(raw_path):
                        result.error(f"{card_label}: image.path must be present after Step 5b")
                    else:
                        resolved = resolve_image_path(base_dir, str(raw_path))
                        if not resolved.exists():
                            result.error(f"{card_label}: image.path not found: {raw_path}")
            else:
                for field_name in ("usage", "placement", "content_description", "source_hint", "prompt", "path"):
                    value = image.get(field_name)
                    if value not in (None, "", "null"):
                        result.warn(f"{card_label}: image.needed=false so image.{field_name} should be empty")

        if page_required_images:
            summary["pages_with_required_images"] += 1
        elif page.get("page_type") in {"cover", "section"}:
            result.warn(f"{label}: {page.get('page_type')} page has no image contract")

    summary["errors"] = len(result.errors)
    summary["warnings"] = len(result.warnings)
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
    parser = argparse.ArgumentParser(description="Validate workflow contracts")
    subparsers = parser.add_subparsers(dest="command")

    for name in ("requirements", "style", "raw-research", "research-package", "outline-review"):
        sub = subparsers.add_parser(name, help=f"Validate {name}.json")
        sub.add_argument("path", help="Path to the JSON file")
        sub.add_argument("--strict", action="store_true", help="Treat warnings as failures")
        sub.add_argument("--report", help="Optional JSON report path")
        if name == "outline-review":
            sub.add_argument("--require-pass", action="store_true", help="Fail unless verdict=pass")

    images = subparsers.add_parser("images", help="Validate planning image contracts")
    images.add_argument("path", help="Planning JSON file or planning directory")
    images.add_argument("--require-paths", action="store_true", help="Require image.path to exist for needed=true cards")
    images.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    images.add_argument("--report", help="Optional JSON report path")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    target = Path(args.path)
    if not target.exists():
        print(f"ERROR: path not found: {target}", file=sys.stderr)
        return 1

    try:
        if args.command == "requirements":
            result, payload = validate_requirements(target)
        elif args.command == "style":
            result, payload = validate_style(target)
        elif args.command == "raw-research":
            result, payload = validate_raw_research(target)
        elif args.command == "research-package":
            result, payload = validate_research_package(target)
        elif args.command == "outline-review":
            result, payload = validate_outline_review(target, bool(args.require_pass))
        else:
            result, payload = validate_images(target, bool(args.require_paths))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print_messages(result)
    if not result.errors and not result.warnings:
        print("OK")

    write_report(
        args.report,
        {
            "command": args.command,
            "ok": result.ok and (not args.strict or not result.warnings),
            "summary": payload,
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
