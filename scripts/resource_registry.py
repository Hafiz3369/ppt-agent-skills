#!/usr/bin/env python3
"""Machine-readable accessors for references/ops/resource-registry.md."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "references"
REGISTRY_PATH = REFS / "ops" / "resource-registry.md"

GROUP_SECTION_TITLES = {
    "layout_refs": "布局（layouts/）",
    "block_refs": "区域展示组件（blocks/）",
    "chart_refs": "图表（charts/）",
    "principle_refs": "设计原则（principles/）",
}

RESOURCE_GROUP_DIRS = {
    "layout_refs": REFS / "layouts",
    "block_refs": REFS / "blocks",
    "chart_refs": REFS / "charts",
    "principle_refs": REFS / "principles",
}
RESOURCE_PLAN_GROUPS = {"layout_refs", "block_refs", "chart_refs", "principle_refs"}


def read_registry() -> str:
    return REGISTRY_PATH.read_text(encoding="utf-8")


def normalize_key(value: str) -> str:
    return value.strip().lower().replace("_", "-")


def clean_cell(value: str) -> str:
    cleaned = value.strip()
    cleaned = re.sub(r"^\*\*(.+)\*\*$", r"\1", cleaned)
    cleaned = cleaned.strip().strip("`").strip()
    return cleaned


def parse_table(lines: list[str]) -> list[dict[str, str]]:
    if len(lines) < 2:
        return []
    headers = [clean_cell(cell) for cell in lines[0].strip().strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        values = [clean_cell(cell) for cell in line.strip().strip("|").split("|")]
        if len(values) != len(headers):
            continue
        rows.append(dict(zip(headers, values)))
    return rows


@lru_cache(maxsize=1)
def section_tables() -> dict[str, list[dict[str, str]]]:
    text = read_registry()
    pattern = re.compile(r"^##\s+\d+\.\s+(.+)$", re.M)
    matches = list(pattern.finditer(text))
    sections: dict[str, list[dict[str, str]]] = {}
    for idx, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        block = text[start:end]
        table_lines: list[str] = []
        in_table = False
        for raw_line in block.splitlines():
            line = raw_line.rstrip()
            if line.strip().startswith("|"):
                table_lines.append(line)
                in_table = True
                continue
            if in_table:
                break
        sections[title] = parse_table(table_lines)
    return sections


@lru_cache(maxsize=1)
def declared_relative_paths() -> set[str]:
    text = read_registry()
    declared = {
        match.group(1).strip()
        for match in re.finditer(r"`([^`\n]+\.[A-Za-z0-9]+)`", text)
    }
    for rows in section_tables().values():
        for row in rows:
            rel = row.get("文件路径")
            if isinstance(rel, str) and rel.strip():
                declared.add(clean_cell(rel))
    return declared


def declared_path(relative_path: str) -> Path:
    if relative_path not in declared_relative_paths():
        raise KeyError(f"{relative_path} is not declared in {REGISTRY_PATH.relative_to(ROOT).as_posix()}")
    if relative_path.startswith("scripts/"):
        return ROOT / relative_path
    return ROOT / "references" / relative_path


def declared_paths(relative_paths: list[str]) -> list[Path]:
    return [declared_path(item) for item in relative_paths]


@lru_cache(maxsize=8)
def resource_ref_map(group: str) -> dict[str, Path]:
    section_title = GROUP_SECTION_TITLES[group]
    rows = section_tables().get(section_title, [])
    refs: dict[str, Path] = {}
    for row in rows:
        rel = row.get("文件路径")
        if not isinstance(rel, str) or not rel.strip():
            continue
        path = ROOT / "references" / rel.strip().strip("`")
        key = normalize_key(path.stem)
        refs[key] = path
    return refs


def valid_resource_refs(group: str) -> set[str]:
    return set(resource_ref_map(group).keys())


def resolve_resource_ref(group: str, ref_name: str) -> Path:
    refs = resource_ref_map(group)
    key = normalize_key(ref_name)
    if key in refs:
        return refs[key]
    raise KeyError(f"Unknown {group} ref '{ref_name}' (normalized: '{key}'). Declare it in {REGISTRY_PATH.relative_to(ROOT).as_posix()} first.")


@lru_cache(maxsize=1)
def page_template_map() -> dict[str, Path]:
    rows = section_tables().get("页面结构规范（page-templates/）", [])
    templates: dict[str, Path] = {}
    for row in rows:
        page_type = row.get("page_type 值")
        rel = row.get("文件路径")
        if not isinstance(page_type, str) or not isinstance(rel, str):
            continue
        templates[page_type.strip().strip("`")] = ROOT / "references" / rel.strip().strip("`")
    return templates


def valid_page_templates() -> set[str]:
    return set(page_template_map().keys())


def resolve_page_template(page_type: str) -> Path | None:
    return page_template_map().get(page_type)


@lru_cache(maxsize=1)
def stage_bundle_rows() -> list[dict[str, str]]:
    return section_tables().get("阶段资源包（stage bundles）", [])


def stage_bundle_entries(bundle_id: str) -> list[dict[str, str | Path]]:
    entries: list[dict[str, str | Path]] = []
    for row in stage_bundle_rows():
        if row.get("bundle_id", "").strip().strip("`") != bundle_id:
            continue
        rel = row.get("文件路径", "").strip().strip("`")
        if not rel:
            continue
        entries.append(
            {
                "bundle_id": bundle_id,
                "path": declared_path(rel),
                "why": row.get("why", "").strip(),
                "condition": row.get("condition", "").strip(),
            }
        )
    return entries


def stage_bundle_paths(bundle_id: str) -> list[Path]:
    return [entry["path"] for entry in stage_bundle_entries(bundle_id) if isinstance(entry.get("path"), Path)]


@lru_cache(maxsize=1)
def routing_policy_rows() -> list[dict[str, str]]:
    return section_tables().get("资源路由策略（resource routing policies）", [])


def _append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def recommended_resource_plan(page: dict[str, object]) -> dict[str, object]:
    plan: dict[str, object] = {
        "page_template": None,
        "layout_refs": [],
        "block_refs": [],
        "chart_refs": [],
        "principle_refs": [],
        "route_notes": [],
    }
    for row in routing_policy_rows():
        scope = clean_cell(row.get("scope", ""))
        field = clean_cell(row.get("field", ""))
        expected = clean_cell(row.get("value", ""))
        resource_group = clean_cell(row.get("resource_group", ""))
        resource_ref = clean_cell(row.get("resource_ref", ""))
        why = clean_cell(row.get("why", ""))

        matched = False
        if scope == "page":
            actual = page.get(field)
            matched = isinstance(actual, str) and normalize_key(actual) == normalize_key(expected)
        elif scope == "card":
            cards = page.get("cards")
            if isinstance(cards, list):
                for card in cards:
                    if not isinstance(card, dict):
                        continue
                    if field == "chart_type":
                        chart = card.get("chart")
                        actual = chart.get("chart_type") if isinstance(chart, dict) else None
                    else:
                        actual = card.get(field)
                    if isinstance(actual, str) and normalize_key(actual) == normalize_key(expected):
                        matched = True
                        break
        if not matched:
            continue

        if resource_group == "page_template":
            if not plan["page_template"]:
                plan["page_template"] = resource_ref
        elif resource_group in RESOURCE_PLAN_GROUPS:
            items = plan[resource_group]
            if isinstance(items, list):
                _append_unique(items, normalize_key(resource_ref))

        note = f"{scope}.{field}={expected} -> {resource_group}:{resource_ref}"
        if why:
            note += f" | {why}"
        route_notes = plan["route_notes"]
        if isinstance(route_notes, list):
            route_notes.append(note)
    return plan
