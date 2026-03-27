#!/usr/bin/env python3
"""Prompt assembly utilities for planning and design stages.

This script closes the handoff between:
- outline -> planning prompt
- planning -> design prompt

It injects style soul, variation strategy, page-level director commands,
technique cards, CSS weapons, selected reference resources, and the global
HTML design guide into the final prompt text consumed by the model.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import resource_registry as rr
from workflow_versions import build_workflow_metadata

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "references"
PROMPTS = REFS / "prompts"
PAGE_REQUIRED_FIELDS = {"slide_number", "page_type", "title", "cards"}

SCENE_LABELS = {
    "live_speech": "现场演讲",
    "self_read": "自阅文档",
    "training": "培训教学",
    "other": "其他",
}
PURPOSE_LABELS = {
    "decision": "做决策",
    "understand": "理解并记住",
    "execute": "学会并执行",
    "shift_perception": "改变认知",
    "other": "其他",
}
NARRATIVE_LABELS = {
    "problem_solution_effect": "问题 -> 方案 -> 效果",
    "what_why_how": "是什么 -> 为什么 -> 怎么做",
    "panorama_focus_action": "全景 -> 聚焦 -> 行动",
    "comparison": "对比论证",
    "timeline": "时间线",
    "custom": "自定义",
}
PERSUASION_LABELS = {
    "hard_data": "硬数据",
    "case_story": "案例故事",
    "authority": "权威背书",
    "process_method": "流程方法",
    "mixed": "混合",
}
LANGUAGE_LABELS = {
    "zh": "中文",
    "en": "英文",
    "zh_en_mix": "中英混排",
    "other": "其他",
}
IMAGE_PREFERENCE_LABELS = {
    "none": "不需要",
    "key_pages": "关键页配图",
    "every_page": "每页配图",
    "user_provided": "用户提供素材",
}
DECK_MODE_LABELS = {
    "launch": "发布会/品牌展示型",
    "business": "商务汇报型",
    "report": "报告/复盘型",
    "academic": "学术型",
    "technical": "技术型",
    "training": "培训讲义型",
}
PRESSURE_LABELS = {
    "low": "低",
    "medium": "中",
    "high": "高",
}
DECORATIVE_TOLERANCE_LABELS = {
    "low": "低",
    "moderate": "中",
    "high": "高",
}
COMPLEXITY_LABELS = {
    "light": "轻量",
    "standard": "标准",
    "large": "大型",
}

GLOBAL_RESOURCE_FILES = rr.stage_bundle_paths("design_global_resources")

PAGE_TEMPLATE_MAP = rr.page_template_map()

VALID_AMBITION_LEVELS = {"quiet", "assertive", "dramatic"}
DENSE_SCENE_MODES = {"report", "academic", "technical", "training"}
PAYLOAD_HEAVY_CARD_TYPES = {
    "data", "data_highlight", "comparison", "process", "timeline",
    "diagram", "matrix_chart", "list", "quote", "people",
}
SOURCE_CONFIDENCE_RULES = {
    "hard": {
        "render_rule": "可以直接陈述，但仍要忠实于 planning，不额外夸大范围或收益。",
        "qualifier_examples": ["直接陈述", "明确动作", "具体对象"],
        "avoid_phrases": ["全面验证", "显著提升", "已经彻底解决"],
    },
    "qualified": {
        "render_rule": "必须保留限定语，写成当前观察、阶段性现象或可见趋势，避免绝对化判断。",
        "qualifier_examples": ["正在", "持续", "当前", "往往", "通常", "阶段性", "可见"],
        "avoid_phrases": ["已经证实", "全面实现", "必然", "显著", "彻底"],
    },
    "derived": {
        "render_rule": "必须写成机制判断或诊断表达，强调“更像什么/意味着什么/不是单纯什么”，不要伪装成硬统计。",
        "qualifier_examples": ["更像", "意味着", "说明", "提示", "本质上", "不是单纯", "核心问题是"],
        "avoid_phrases": ["数据证明", "已经验证", "最终结论", "全面达成"],
    },
}


@dataclass
class ResourceSection:
    title: str
    items: list[tuple[str, str]]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def compact_markdown(
    text: str,
    *,
    max_lines: int = 16,
    max_chars: int = 900,
    keep_first_code_block: bool = False,
    max_code_lines: int = 8,
) -> str:
    """Keep only high-signal markdown lines so prompt-ready stays executable."""
    lines: list[str] = []
    in_code_block = False
    keeping_code_block = False
    code_block_kept = False
    code_lines = 0
    table_rows = 0

    def append_candidate(candidate: str) -> bool:
        if not candidate:
            return True
        if lines and candidate == lines[-1]:
            return True
        projected = "\n".join(lines + [candidate])
        if len(lines) >= max_lines or len(projected) > max_chars:
            return False
        lines.append(candidate)
        return True

    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            if keep_first_code_block and not code_block_kept:
                if not append_candidate(stripped):
                    break
                if not in_code_block:
                    keeping_code_block = True
                    code_lines = 0
                else:
                    keeping_code_block = False
                    code_block_kept = True
            in_code_block = not in_code_block
            continue
        if in_code_block:
            if keeping_code_block and code_lines < max_code_lines:
                if not append_candidate(raw_line.rstrip()):
                    break
                code_lines += 1
            continue
        if not stripped or stripped.startswith("![]("):
            continue

        if stripped.startswith("|"):
            if table_rows >= 6:
                continue
            table_rows += 1
            candidate = stripped
        elif re.match(r"^#{1,6}\s+", stripped):
            candidate = stripped
        elif re.match(r"^[-*]\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
            candidate = stripped
        else:
            candidate = stripped[:140]

        if not append_candidate(candidate):
            break
    return "\n".join(lines).strip() or "N/A"


def compact_lines(text: str, *, max_lines: int = 18, max_chars: int = 1200) -> str:
    """Trim structured line-oriented payloads without changing field order."""
    output: list[str] = []
    total = 0
    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        line = raw_line.rstrip()
        projected = total + len(line) + (1 if output else 0)
        if len(output) >= max_lines or projected > max_chars:
            break
        output.append(line)
        total = projected
    return "\n".join(output).strip() or "N/A"


def extract_wrapped_json(text: str) -> Any:
    text = text.strip()
    if not text:
        raise ValueError("Empty JSON input")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)
    if fenced:
        return json.loads(fenced.group(1))

    for tag in ("PPT_OUTLINE", "PPT_PLANNING", "REQUIREMENTS_JSON"):
        pattern = rf"\[{tag}\]\s*```json\s*(\{{.*?\}})\s*```\s*\[/{tag}\]"
        match = re.search(pattern, text, re.S)
        if match:
            return json.loads(match.group(1))

    first = text.find("{")
    last = text.rfind("}")
    if first != -1 and last != -1 and last > first:
        return json.loads(text[first:last + 1])
    raise ValueError("Could not parse JSON payload")


def load_jsonish(path: Path) -> Any:
    return extract_wrapped_json(read_text(path))


def unwrap_payload(data: Any, primary_key: str) -> dict[str, Any]:
    if isinstance(data, dict) and primary_key in data:
        value = data[primary_key]
        if not isinstance(value, dict):
            raise ValueError(f"Top-level key {primary_key} must map to an object")
        return value
    if isinstance(data, dict):
        return data
    raise ValueError(f"Unexpected payload type: {type(data).__name__}")


def pretty_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def as_str_list(value: Any) -> list[str]:
    items = as_list(value)
    output: list[str] = []
    for item in items:
        if item is None:
            continue
        text = str(item).strip()
        if text:
            output.append(text)
    return output


def first_non_empty(*values: Any) -> Any:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        if isinstance(value, (list, dict)) and not value:
            continue
        return value
    return None


def format_value(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, str):
        return value.strip() or "N/A"
    if isinstance(value, (list, dict)):
        return pretty_json(value)
    return str(value)


def format_enum(value: Any, labels: dict[str, str]) -> str:
    if value is None:
        return "N/A"
    text = str(value).strip()
    if not text:
        return "N/A"
    label = labels.get(text)
    return f"{text}（{label}）" if label else text


def normalize_complexity(value: Any) -> str:
    mapping = {"heavy": "large", "large": "large", "standard": "standard", "light": "light"}
    if value is None:
        return "standard"
    return mapping.get(str(value).strip().lower(), str(value).strip() or "standard")


def normalize_information_pressure(value: Any) -> str:
    mapping = {
        "sparse": "low",
        "少而精": "low",
        "low": "low",
        "moderate": "medium",
        "适中": "medium",
        "medium": "medium",
        "dense": "high",
        "信息量大": "high",
        "high": "high",
    }
    if value is None:
        return "medium"
    return mapping.get(str(value).strip().lower(), mapping.get(str(value).strip(), str(value).strip() or "medium"))


def normalize_decorative_tolerance(value: Any) -> str:
    mapping = {
        "极低": "low",
        "low": "low",
        "适中": "moderate",
        "moderate": "moderate",
        "可适度表现": "high",
        "high": "high",
    }
    if value is None:
        return "moderate"
    return mapping.get(str(value).strip().lower(), mapping.get(str(value).strip(), str(value).strip() or "moderate"))


def infer_default_content_floor(deck_mode: str, information_pressure: str) -> str:
    floors = {
        "launch": {
            "low": "每页至少有 1 个明确判断或记忆点，避免只剩情绪口号。",
            "medium": "每页至少有 1 个主判断 + 1 组支撑信息或案例，不可只有视觉气氛。",
            "high": "每页至少有 1 个主判断 + 1 组数据/案例/对比支撑，不能退化成英雄页。",
        },
        "business": {
            "low": "每页至少有 1 个可复述的业务判断和简明支撑。",
            "medium": "每页至少有 1 个业务判断 + 1 组依据或行动含义。",
            "high": "每页至少有 1 个业务判断 + 1 组证据/比较 + 1 个行动含义。",
        },
        "report": {
            "low": "每页至少有明确指标或事实，不可只做标题陈述。",
            "medium": "每页至少有指标/事实 + 对应解读，信息承载优先。",
            "high": "每页至少有指标/比较轴 + 管理解读或行动含义，禁止空心排版。",
        },
        "academic": {
            "low": "每页至少有定义、问题或结论中的一种明确内容。",
            "medium": "每页至少有定义/问题 + 证据或方法说明。",
            "high": "每页至少同时覆盖定义/问题、证据/方法、边界/限制三类内容。",
        },
        "technical": {
            "low": "每页至少说明结构、步骤或约束中的一种，不可只讲概念。",
            "medium": "每页至少有结构/步骤 + 约束或依赖说明。",
            "high": "每页至少同时覆盖结构/步骤、约束/依赖、风险/回退三类内容。",
        },
        "training": {
            "low": "每页至少有一个可执行步骤或操作提示。",
            "medium": "每页至少有步骤 + 检查点或注意事项。",
            "high": "每页至少同时覆盖步骤、检查点、警示/回退，保证可执行性。",
        },
    }
    mode = deck_mode if deck_mode in floors else "business"
    pressure = information_pressure if information_pressure in floors[mode] else "medium"
    return floors[mode][pressure]


def normalize_requirements_payload(payload: dict[str, Any]) -> dict[str, Any]:
    page_requirements = payload.get("page_requirements") if isinstance(payload.get("page_requirements"), dict) else {}
    if not page_requirements:
        page_requirements = {
            "page_range": payload.get("page_count"),
            "density": payload.get("info_density"),
        }

    content_constraints = payload.get("content_constraints") if isinstance(payload.get("content_constraints"), dict) else {}
    if not content_constraints:
        content_constraints = {
            "must_include": as_str_list(payload.get("content_must_include")),
            "must_avoid": as_str_list(payload.get("content_must_avoid")),
        }

    brand_info = payload.get("brand_info") if isinstance(payload.get("brand_info"), dict) else {}
    if brand_info and "logo" not in brand_info and brand_info.get("logo_path") is not None:
        brand_info = {**brand_info, "logo": brand_info.get("logo_path")}

    scene = first_non_empty(payload.get("scene"), "other")
    density = normalize_information_pressure(
        first_non_empty(
            payload.get("page_information_pressure"),
            page_requirements.get("density"),
            payload.get("info_density"),
        )
    )
    decorative_tolerance = normalize_decorative_tolerance(page_requirements.get("decorative_tolerance"))

    deck_mode_raw = payload.get("deck_mode")
    if not isinstance(deck_mode_raw, str) or not deck_mode_raw.strip():
        tendency = first_non_empty(page_requirements.get("page_type_tendency"), page_requirements.get("page_type"))
        tendency_map = {
            "发布会/品牌展示型": "launch",
            "launch": "launch",
            "business": "business",
            "商务汇报型": "business",
            "report": "report",
            "报告/复盘型": "report",
            "academic": "academic",
            "学术/技术型": "academic",
            "technical": "technical",
            "技术型": "technical",
            "training": "training",
            "培训讲义型": "training",
        }
        if isinstance(tendency, str) and tendency.strip():
            deck_mode_raw = tendency_map.get(tendency.strip(), tendency_map.get(tendency.strip().lower(), ""))
        if not deck_mode_raw:
            scene_map = {
                "training": "training",
                "培训教学": "training",
                "培训": "training",
                "self_read": "report",
                "自阅文档": "report",
                "live_speech": "business",
                "现场演讲": "business",
            }
            deck_mode_raw = scene_map.get(str(scene).strip(), "business")

    deck_mode = str(deck_mode_raw).strip() or "business"
    complexity = normalize_complexity(payload.get("complexity_level"))

    return {
        "topic": payload.get("topic"),
        "scene": scene,
        "audience": payload.get("audience"),
        "purpose": first_non_empty(payload.get("purpose"), payload.get("expected_outcome")),
        "narrative_structure": payload.get("narrative_structure"),
        "emphasis": as_str_list(first_non_empty(payload.get("emphasis"), payload.get("content_emphasis"))),
        "persuasion_style": first_non_empty(payload.get("persuasion_style"), payload.get("persuasion_styles")),
        "style_choice": first_non_empty(payload.get("style_choice"), payload.get("visual_direction")),
        "page_requirements": page_requirements,
        "brand_info": brand_info,
        "content_constraints": content_constraints,
        "language": payload.get("language"),
        "image_preference": payload.get("image_preference"),
        "dynamic_answers": payload.get("dynamic_answers") if isinstance(payload.get("dynamic_answers"), dict) else {},
        "deck_mode": deck_mode,
        "page_information_pressure": density,
        "decorative_tolerance": decorative_tolerance,
        "default_content_floor": first_non_empty(
            payload.get("default_content_floor"),
            infer_default_content_floor(deck_mode, density),
        ),
        "complexity_level": complexity,
    }


def load_requirements_payload(path: Path) -> dict[str, Any]:
    payload = load_jsonish(path)
    if not isinstance(payload, dict):
        raise ValueError(f"Unexpected requirements payload type: {type(payload).__name__}")
    nested = payload.get("requirements") or payload.get("requirement")
    if isinstance(nested, dict):
        payload = nested
    return normalize_requirements_payload(payload)


def build_outline_audience_brief(audience: Any) -> str:
    if isinstance(audience, dict):
        profile = audience.get("profile")
        concern = audience.get("primary_concern")
        return pretty_json({
            "profile": profile,
            "primary_concern": concern,
        })
    return format_value(audience)


def build_outline_persuasion_brief(value: Any) -> str:
    if isinstance(value, list):
        return pretty_json([format_enum(item, PERSUASION_LABELS) for item in value])
    return format_enum(value, PERSUASION_LABELS)


def build_outline_page_requirements(req: dict[str, Any]) -> str:
    page_requirements = req.get("page_requirements") if isinstance(req.get("page_requirements"), dict) else {}
    payload = {
        "page_range": page_requirements.get("page_range"),
        "density": format_enum(req.get("page_information_pressure"), PRESSURE_LABELS),
        "page_type_tendency": page_requirements.get("page_type_tendency"),
        "decorative_tolerance": format_enum(req.get("decorative_tolerance"), DECORATIVE_TOLERANCE_LABELS),
    }
    return pretty_json(payload)


def build_scene_density_profile(req: dict[str, Any]) -> str:
    payload = {
        "deck_mode": format_enum(req.get("deck_mode"), DECK_MODE_LABELS),
        "page_information_pressure": format_enum(req.get("page_information_pressure"), PRESSURE_LABELS),
        "decorative_tolerance": format_enum(req.get("decorative_tolerance"), DECORATIVE_TOLERANCE_LABELS),
        "default_content_floor": req.get("default_content_floor"),
    }
    return pretty_json(payload)


def build_content_constraints(req: dict[str, Any]) -> str:
    constraints = req.get("content_constraints") if isinstance(req.get("content_constraints"), dict) else {}
    payload = {
        "must_include": as_str_list(constraints.get("must_include")),
        "must_avoid": as_str_list(constraints.get("must_avoid")),
    }
    return pretty_json(payload)


def build_outline_research_agenda(req: dict[str, Any], research: dict[str, Any]) -> str:
    constraints = req.get("content_constraints") if isinstance(req.get("content_constraints"), dict) else {}
    payload = {
        "topic": req.get("topic"),
        "priority_emphasis": req.get("emphasis", []),
        "persuasion_bias": build_outline_persuasion_brief(req.get("persuasion_style")),
        "must_answer": as_str_list(constraints.get("must_include")),
        "must_avoid": as_str_list(constraints.get("must_avoid")),
        "audience_primary_concern": (
            req.get("audience", {}).get("primary_concern")
            if isinstance(req.get("audience"), dict)
            else None
        ),
        "dynamic_answers": req.get("dynamic_answers", {}),
        "research_gaps": [
            gap.get("description")
            for gap in as_list(research.get("gaps"))
            if isinstance(gap, dict) and gap.get("description")
        ],
    }
    return pretty_json(payload)


def coverage_status_for_item(item: str, research: dict[str, Any]) -> str:
    coverage = (
        research.get("meta", {}).get("coverage_report", {}).get("content_must_include_coverage", {})
        if isinstance(research.get("meta"), dict)
        else {}
    )
    if isinstance(coverage, dict) and item in coverage:
        return "covered" if coverage.get(item) else "missing"

    token = item.lower()
    matched = False
    for material in as_list(research.get("materials")):
        if not isinstance(material, dict):
            continue
        haystacks: list[str] = []
        for field in ("fact", "data", "source", "source_url"):
            value = material.get(field)
            if isinstance(value, str):
                haystacks.append(value.lower())
        for value in as_str_list(material.get("categories")):
            haystacks.append(value.lower())
        for value in as_str_list(material.get("relevance_to")):
            haystacks.append(value.lower())
        if any(token in haystack for haystack in haystacks):
            matched = True
            if str(material.get("reliability", "")).strip().lower() in {"high", "medium"}:
                return "covered"
    return "partial" if matched else "unknown"


def build_user_concern_matrix(req: dict[str, Any], research: dict[str, Any]) -> str:
    concerns: list[dict[str, Any]] = []
    audience = req.get("audience") if isinstance(req.get("audience"), dict) else {}
    primary_concern = audience.get("primary_concern")
    if primary_concern:
        concerns.append({
            "concern": primary_concern,
            "answer_route": "优先在开篇或首个内容 Part 给出直接回应。",
            "evidence_status": coverage_status_for_item(str(primary_concern), research),
        })
    for item in req.get("emphasis", []):
        concerns.append({
            "concern": item,
            "answer_route": "在对应 Part 里作为主线展开，不要平均稀释。",
            "evidence_status": coverage_status_for_item(item, research),
        })
    constraints = req.get("content_constraints") if isinstance(req.get("content_constraints"), dict) else {}
    for item in as_str_list(constraints.get("must_include")):
        concerns.append({
            "concern": item,
            "answer_route": "必须在大纲中有明确落点，且标明证据强弱。",
            "evidence_status": coverage_status_for_item(item, research),
        })
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for concern in concerns:
        key = str(concern.get("concern", "")).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(concern)
    payload = {
        "audience_profile": audience.get("profile") if audience else format_value(req.get("audience")),
        "purpose": format_enum(req.get("purpose"), PURPOSE_LABELS),
        "concerns": deduped,
    }
    return pretty_json(payload)


def build_evidence_coverage(req: dict[str, Any], research: dict[str, Any]) -> str:
    meta = research.get("meta") if isinstance(research.get("meta"), dict) else {}
    coverage = meta.get("coverage_report") if isinstance(meta.get("coverage_report"), dict) else {}
    payload = {
        "by_reliability": meta.get("by_reliability"),
        "by_category": meta.get("by_category"),
        "content_must_include_coverage": coverage.get("content_must_include_coverage"),
        "thin_dimensions": coverage.get("thin_dimensions"),
        "gaps": [
            {
                "description": gap.get("description"),
                "dimension": gap.get("dimension"),
                "impact": gap.get("impact"),
            }
            for gap in as_list(research.get("gaps"))
            if isinstance(gap, dict)
        ],
        "complexity_level": format_enum(req.get("complexity_level"), COMPLEXITY_LABELS),
    }
    return pretty_json(payload)


def build_search_results_summary(research: dict[str, Any]) -> str:
    materials = [item for item in as_list(research.get("materials")) if isinstance(item, dict)]
    reliability_rank = {"high": 0, "medium": 1, "low": 2}
    selected = sorted(
        materials,
        key=lambda item: (
            reliability_rank.get(str(item.get("reliability", "")).strip().lower(), 3),
            str(item.get("id", "")),
        ),
    )[:12]
    payload = {
        "meta": research.get("meta"),
        "selected_materials": [
            {
                "id": item.get("id"),
                "fact": item.get("fact"),
                "data": item.get("data"),
                "source": item.get("source"),
                "reliability": item.get("reliability"),
                "categories": item.get("categories"),
                "relevance_to": item.get("relevance_to"),
            }
            for item in selected
        ],
        "gaps": research.get("gaps"),
    }
    return pretty_json(payload)


def normalize_ref_name(name: str) -> str:
    return name.strip().lower().replace("_", "-")


def split_markdown_sections(text: str, prefix: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    pattern = re.compile(rf"^##\s+({re.escape(prefix)}\d+[a-z]?)\.\s+.*$", re.M)
    matches = list(pattern.finditer(text))
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections[match.group(1)] = text[start:end].strip()
    return sections


def natural_sort_key(path: Path) -> tuple[Any, ...]:
    parts = re.split(r"(\d+)", path.name)
    key: list[Any] = []
    for part in parts:
        key.append(int(part) if part.isdigit() else part)
    return tuple(key)


def is_page_like(data: Any) -> bool:
    return isinstance(data, dict) and PAGE_REQUIRED_FIELDS.issubset(data.keys())


TECHNIQUE_CARDS_PATH = rr.declared_path("runtime/technique-cards.md")
CSS_WEAPONS_PATH = rr.declared_path("design-runtime/css-weapons.md")
TECHNIQUE_SECTIONS = split_markdown_sections(read_text(TECHNIQUE_CARDS_PATH), "T")
WEAPON_SECTIONS = split_markdown_sections(read_text(CSS_WEAPONS_PATH), "W")


def coerce_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def extract_ids(values: list[Any], prefix: str) -> list[str]:
    found: list[str] = []
    for value in values:
        if isinstance(value, str):
            matches = re.findall(rf"{prefix}\d+[a-z]?", value, flags=re.I)
            found.extend(match.upper() for match in matches)
        elif isinstance(value, dict):
            for nested in value.values():
                found.extend(extract_ids(coerce_list(nested), prefix))

    deduped: list[str] = []
    seen: set[str] = set()
    for item in found:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def infer_compact_detail_level(page: dict[str, Any]) -> str:
    page_type = str(page.get("page_type") or "content")
    cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
    chart_count = 0
    heavy_card_count = 0
    for card in cards:
        card_type = str(card.get("card_type") or "")
        chart = card.get("chart")
        if isinstance(chart, dict) and chart.get("chart_type"):
            chart_count += 1
        if card_type in {"data", "comparison", "timeline", "diagram", "matrix_chart", "process", "people"}:
            heavy_card_count += 1
    if page_type in {"cover", "section", "toc", "end"}:
        return "medium"
    if chart_count >= 1 or heavy_card_count >= 2 or len(cards) >= 4:
        return "medium"
    return "low"


def load_outline_payload(path: Path) -> dict[str, Any]:
    return unwrap_payload(load_jsonish(path), "ppt_outline")


def load_planning_payload(path: Path) -> dict[str, Any]:
    if path.is_dir():
        pages: list[dict[str, Any]] = []
        rationale: dict[str, Any] | None = None
        candidates = sorted(
            [item for item in path.iterdir() if item.is_file() and item.suffix.lower() in {".json", ".md", ".txt"}],
            key=natural_sort_key,
        )
        if not candidates:
            raise ValueError(f"No planning files found in directory: {path}")

        for file_path in candidates:
            payload = load_jsonish(file_path)
            if isinstance(payload, dict) and "ppt_planning" in payload:
                deck = unwrap_payload(payload, "ppt_planning")
                if rationale is None and isinstance(deck.get("planning_rationale"), dict):
                    rationale = deck.get("planning_rationale")
                for page in as_list(deck.get("pages")):
                    if isinstance(page, dict):
                        pages.append(page)
                continue
            if is_page_like(payload):
                pages.append(payload)
                continue
            if isinstance(payload, dict):
                nested_page = payload.get("page") or payload.get("planning_page")
                if is_page_like(nested_page):
                    pages.append(nested_page)
                    continue
            raise ValueError(f"Unsupported planning payload in {file_path}")

        pages.sort(key=lambda item: item.get("slide_number", 0))
        return {
            "planning_rationale": rationale or {
                "three_core_contract": {},
                "deck_rhythm_summary": "Assembled from page-level planning files",
                "variation_strategy": "See page-level variation_guardrails",
                "risk_watchouts": [],
            },
            "pages": pages,
        }

    payload = load_jsonish(path)
    if isinstance(payload, dict) and "ppt_planning" in payload:
        return unwrap_payload(payload, "ppt_planning")
    if is_page_like(payload):
        return {
            "planning_rationale": {
                "three_core_contract": {},
                "deck_rhythm_summary": "Single-page planning payload",
                "variation_strategy": "Single-page mode",
                "risk_watchouts": [],
            },
            "pages": [payload],
        }
    if isinstance(payload, dict):
        nested_page = payload.get("page") or payload.get("planning_page")
        if is_page_like(nested_page):
            return {
                "planning_rationale": {
                    "three_core_contract": {},
                    "deck_rhythm_summary": "Single-page planning payload",
                    "variation_strategy": "Single-page mode",
                    "risk_watchouts": [],
                },
                "pages": [nested_page],
            }
    raise ValueError(f"Unsupported planning payload: {path}")


def build_style_definition(style: dict[str, Any], *, inline_assets: bool) -> str:
    lines = [
        "[STYLE_BRIEF]",
        f"style_id: {style.get('style_id', 'unknown')}",
        f"style_name: {style.get('style_name', 'unknown')}",
        f"design_soul: {style.get('design_soul', 'N/A')}",
        f"variation_strategy: {style.get('variation_strategy', 'N/A')}",
        f"mood_keywords: {', '.join(style.get('mood_keywords', [])) or 'N/A'}",
        f"font_family: {style.get('font_family', 'N/A')}",
    ]
    decoration = style.get("decoration_dna", {}) if isinstance(style.get("decoration_dna"), dict) else {}
    lines.extend(
        [
            f"signature_move: {decoration.get('signature_move', 'N/A')}",
            f"forbidden: {', '.join(decoration.get('forbidden', [])) or 'N/A'}",
            f"recommended_combos: {' | '.join(decoration.get('recommended_combos', [])) or 'N/A'}",
        ]
    )

    css_variables = style.get("css_variables") if isinstance(style.get("css_variables"), dict) else {}
    if css_variables:
        lines.extend(["", "[STYLE_VARIABLES]"])
        for key, value in css_variables.items():
            lines.append(f"{key}: {value}")

    if inline_assets:
        css_snippets = style.get("css_snippets") if isinstance(style.get("css_snippets"), dict) else {}
        if css_snippets:
            lines.extend(["", "[CSS_SNIPPETS]"])
            for key, value in css_snippets.items():
                lines.append(f"{key}: {value}")
    return "\n".join(lines).strip()


def assemble_outline_prompt(args: argparse.Namespace) -> int:
    requirements = load_requirements_payload(Path(args.requirements))
    research = load_jsonish(Path(args.research))
    if not isinstance(research, dict):
        raise ValueError("Research package must be a JSON object")

    template = read_text(Path(args.template or PROMPTS / "prompt-2-outline.md"))
    brand_info = requirements.get("brand_info") if isinstance(requirements.get("brand_info"), dict) else {}
    mapping = {
        "TOPIC": format_value(requirements.get("topic")),
        "SCENE": format_enum(requirements.get("scene"), SCENE_LABELS),
        "AUDIENCE": build_outline_audience_brief(requirements.get("audience")),
        "PURPOSE": format_enum(requirements.get("purpose"), PURPOSE_LABELS),
        "NARRATIVE_STRUCTURE": format_enum(requirements.get("narrative_structure"), NARRATIVE_LABELS),
        "EMPHASIS": pretty_json(requirements.get("emphasis", [])),
        "PERSUASION_STYLE": build_outline_persuasion_brief(requirements.get("persuasion_style")),
        "PAGE_REQUIREMENTS": build_outline_page_requirements(requirements),
        "SCENE_DENSITY_PROFILE": build_scene_density_profile(requirements),
        "COMPLEXITY_LEVEL": format_enum(requirements.get("complexity_level"), COMPLEXITY_LABELS),
        "BRAND_INFO": pretty_json(brand_info),
        "CONTENT_CONSTRAINTS": build_content_constraints(requirements),
        "RESEARCH_AGENDA": build_outline_research_agenda(requirements, research),
        "USER_CONCERN_MATRIX": build_user_concern_matrix(requirements, research),
        "EVIDENCE_COVERAGE": build_evidence_coverage(requirements, research),
        "SEARCH_RESULTS": build_search_results_summary(research),
    }
    output = replace_tokens(template, mapping)
    write_text(Path(args.output), output)
    print(Path(args.output))
    return 0


def build_global_design_guide(*, inline_assets: bool) -> str:
    summary = "\n".join(
        [
            "[GLOBAL_DESIGN_BRIEF]",
            "priority: P0 content fidelity > P1 hierarchy > P2 spatial drama > P3 mood/detail",
            "single_anchor: each slide must have exactly one visual anchor",
            "design_intent: PAGE_DESIGN_INTENT defines page force, memory point, and main contrast axis",
            "source_fidelity: keep qualified/derived claims cautious; do not upgrade them into hard proof",
            "layering: use at least 3 explicit layers on regular pages; section/toc can drop to 2",
            "contrast: max/min type scale >= 5x; avoid equal-weight cards",
            "anti_webpage: do not default to symmetric web sections unless planning explicitly asks for it",
            "preserve_contract: do not change page_type, layout_hint, visual_weight, card ids, or card roles",
            "variation: adjacent pages should vary in at least 2 dimensions",
            "repair_bias: when space is tight, shorten copy before collapsing hierarchy",
            "density_contract: obey page-level density_contract first; satisfy content floor before decorative polish",
            "dense_scene_rule: dense scenes cannot be solved by atmosphere + whitespace alone",
            "dense_scene_payloads: report=metrics+deltas+readout; academic=question/evidence/boundary; technical=structure/constraints/fallback; training=steps/checkpoints/warnings",
            "anti_launch_drift: dense scenes must avoid keynote hero or slogan-first composition",
        ]
    )
    return summary


# --- Density, scene execution, card execution (delegated to prompt_assembler_density) ---
from prompt_assembler_density import (  # noqa: E402, F811
    effective_density_contract,
    build_density_contract_brief,
    build_render_density_plan,
    build_scene_execution_brief,
    build_card_execution_contract,
)







# --- Page content, source guidance, design intent, budgets (delegated to prompt_assembler_content) ---
from prompt_assembler_content import (  # noqa: E402, F811
    build_card_budget,
    build_content_budget,
    build_content_budget_compact,
    first_anchor_card,
    infer_design_intent,
    build_page_design_intent,
    build_page_card_manifest,
    build_page_card_manifest_compact,
    build_page_source_guidance,
    build_page_source_guidance_compact,
    build_image_info,
)
from prompt_assembler_content import build_page_content as _build_page_content_raw  # noqa: E402


def build_page_content(page: dict[str, Any]) -> str:
    """Wrapper that injects the resource plan function into the content builder."""
    return _build_page_content_raw(page, page_resource_plan_fn=page_resource_plan)

def render_lookup_block(
    title: str,
    identifiers: list[str],
    lookup: dict[str, str],
    *,
    compact: bool = False,
    detail_level: str = "medium",
) -> str:
    if not identifiers:
        return ""
    line_limit = 10 if detail_level == "low" else 14
    char_limit = 500 if detail_level == "low" else 700
    chunks: list[str] = [f"[{title}]"]
    for identifier in identifiers:
        content = lookup.get(identifier)
        if not content:
            chunks.append(f"### {identifier}\nMISSING_REFERENCE")
            continue
        payload = (
            compact_markdown(
                content,
                max_lines=line_limit,
                max_chars=char_limit,
                keep_first_code_block=title in {"TECHNIQUES", "CSS_WEAPONS"},
                max_code_lines=10 if title == "CSS_WEAPONS" else 8,
            )
            if compact
            else content
        )
        chunks.append(f"### {identifier}\n{payload}")
    return "\n\n".join(chunks).strip()


def render_runtime_lookup(title: str, identifiers: list[str], source_path: Path, *, description: str) -> str:
    lines = [f"[{title}]"]
    if identifiers:
        lines.append(f"required_ids: {', '.join(identifiers)}")
    else:
        lines.append("required_ids: N/A")
    lines.append(f"source_path: {source_path.relative_to(ROOT).as_posix()}")
    lines.append(f"runtime_rule: {description}")
    return "\n".join(lines)


def page_resource_plan(page: dict[str, Any]) -> dict[str, Any]:
    explicit = page.get("resources", {}) if isinstance(page.get("resources"), dict) else {}
    suggested = rr.recommended_resource_plan(page)
    merged: dict[str, Any] = {
        "page_template": explicit.get("page_template") or suggested.get("page_template"),
        "layout_refs": [],
        "block_refs": [],
        "chart_refs": [],
        "principle_refs": [],
        "route_notes": suggested.get("route_notes", []),
    }
    for group in ("layout_refs", "block_refs", "chart_refs", "principle_refs"):
        seen: set[str] = set()
        values: list[str] = []
        for source in (explicit.get(group), suggested.get(group)):
            for item in source if isinstance(source, list) else []:
                if not isinstance(item, str):
                    continue
                normalized = normalize_ref_name(item)
                if normalized in seen:
                    continue
                seen.add(normalized)
                values.append(normalized)
        merged[group] = values
    return merged


def resource_path_for_group(group: str, ref_name: str) -> Path:
    return rr.resolve_resource_ref(group, normalize_ref_name(ref_name))


def build_resource_sections(
    page: dict[str, Any],
    *,
    inline_assets: bool,
    compact: bool = False,
    detail_level: str = "medium",
) -> str:
    resources = page_resource_plan(page)
    sections: list[ResourceSection] = []
    global_line_limit = 8 if detail_level == "low" else 12
    global_char_limit = 420 if detail_level == "low" else 650
    page_template_line_limit = 8 if detail_level == "low" else 10
    page_template_char_limit = 420 if detail_level == "low" else 500
    resource_line_limit = 6 if detail_level == "low" else 8
    resource_char_limit = 320 if detail_level == "low" else 420

    if not compact:
        global_items = []
        for path in GLOBAL_RESOURCE_FILES:
            if path.exists():
                if inline_assets:
                    payload = (
                        compact_markdown(read_text(path), max_lines=global_line_limit, max_chars=global_char_limit)
                        if compact
                        else read_text(path)
                    )
                else:
                    payload = "read at runtime if needed"
                global_items.append((path.relative_to(ROOT).as_posix(), payload))
        sections.append(ResourceSection("GLOBAL_RESOURCES", global_items))

    page_template = resources.get("page_template")
    if isinstance(page_template, str) and page_template in PAGE_TEMPLATE_MAP and PAGE_TEMPLATE_MAP[page_template].exists():
        if inline_assets:
            payload = (
                compact_markdown(
                    read_text(PAGE_TEMPLATE_MAP[page_template]),
                    max_lines=page_template_line_limit,
                    max_chars=page_template_char_limit,
                )
                if compact
                else read_text(PAGE_TEMPLATE_MAP[page_template])
            )
        else:
            payload = "read at runtime before composing the page shell"
        sections.append(
            ResourceSection(
                "PAGE_TEMPLATE",
                [(PAGE_TEMPLATE_MAP[page_template].relative_to(ROOT).as_posix(), payload)],
            )
        )

    group_map = {
        "LAYOUT": "layout_refs",
        "BLOCKS": "block_refs",
        "CHARTS": "chart_refs",
        "PRINCIPLES": "principle_refs",
    }
    for title, group in group_map.items():
        items: list[tuple[str, str]] = []
        refs = resources.get(group)
        for ref in refs if isinstance(refs, list) else []:
            path = resource_path_for_group(group, ref)
            if path.exists():
                if inline_assets:
                    payload = (
                        compact_markdown(
                            read_text(path),
                            max_lines=resource_line_limit,
                            max_chars=resource_char_limit,
                        )
                        if compact
                        else read_text(path)
                    )
                else:
                    payload = "read at runtime only if this reference is needed"
                items.append((path.relative_to(ROOT).as_posix(), payload))
        if items:
            sections.append(ResourceSection(title, items))

    parts: list[str] = []
    if not inline_assets:
        parts.append("[RESOURCE_EXECUTION_RULES]")
        parts.append("Read only the files listed below. Do not bulk-load unrelated references.")
        parts.append("Read order: PAGE_TEMPLATE -> LAYOUT -> BLOCKS/CHARTS -> PRINCIPLES.")
    for section in sections:
        parts.append(f"[{section.title}]")
        for label, content in section.items:
            parts.append(f"### {label}\n{content}")
    route_notes = resources.get("route_notes")
    if isinstance(route_notes, list) and route_notes:
        parts.append("[RESOURCE_ROUTE_NOTES]")
        parts.extend(f"- {item}" for item in route_notes if isinstance(item, str))
    return "\n\n".join(parts).strip()


def replace_tokens(template: str, mapping: dict[str, str]) -> str:
    result = template
    for key, value in mapping.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def summarize_previous_pages(planning_payload: dict[str, Any]) -> str:
    rows: list[str] = []
    for page in as_list(planning_payload.get("pages")):
        director = page.get("director_command") or {}
        rows.append(
            "slide {n}: {title} | type={ptype} | weight={weight} | layout={layout} | techniques={techs}".format(
                n=page.get("slide_number"),
                title=page.get("title", "N/A"),
                ptype=page.get("page_type", "N/A"),
                weight=page.get("visual_weight", "N/A"),
                layout=page.get("layout_hint", "N/A"),
                techs=",".join(as_list(director.get("techniques"))) or "N/A",
            )
        )
    return "\n".join(rows).strip()


def build_deck_coherence_summary(
    pages: list[dict[str, Any]],
    current_slide: int,
) -> dict[str, Any]:
    """Build deck-level visual coherence summary for the HTML agent.

    Gives the HTML agent a bird's-eye view of what has ALREADY been used
    across the entire deck, so it can avoid distant repetition and maintain
    rhythm even when local continuity (prev/next) looks fine.
    """
    from collections import Counter

    layout_counter: Counter[str] = Counter()
    focus_counter: Counter[str] = Counter()
    technique_counter: Counter[str] = Counter()
    card_style_counter: Counter[str] = Counter()
    weight_trace: list[dict[str, Any]] = []

    for page in pages:
        if not isinstance(page, dict):
            continue
        sn = page.get("slide_number")
        pt = str(page.get("page_type") or "content")
        lh = page.get("layout_hint")
        fz = page.get("focus_zone")
        vw = page.get("visual_weight")

        if isinstance(lh, str) and lh.strip():
            layout_counter[lh.strip()] += 1
        if isinstance(fz, str) and fz.strip():
            focus_counter[fz.strip()] += 1

        director = page.get("director_command") if isinstance(page.get("director_command"), dict) else {}
        for tech in as_list(director.get("techniques")):
            if isinstance(tech, str) and tech.strip():
                technique_counter[tech.strip()] += 1

        for card in as_list(page.get("cards")):
            if isinstance(card, dict):
                cs = card.get("card_style")
                if isinstance(cs, str) and cs.strip():
                    card_style_counter[cs.strip()] += 1

        weight_trace.append({
            "slide": sn,
            "type": pt,
            "weight": vw,
            "is_current": sn == current_slide,
        })

    # Flag overused items (>= 3 times across deck)
    overused_layouts = [k for k, v in layout_counter.items() if v >= 3]
    overused_techniques = [k for k, v in technique_counter.items() if v >= 3]

    return {
        "total_slides": len(pages),
        "layout_usage": dict(layout_counter.most_common(8)),
        "focus_usage": dict(focus_counter.most_common(6)),
        "technique_usage": dict(technique_counter.most_common(8)),
        "card_style_usage": dict(card_style_counter.most_common(6)),
        "weight_trace": weight_trace,
        "overused_warning": {
            "layouts": overused_layouts,
            "techniques": overused_techniques,
        },
        "coherence_rules": [
            "Same layout_hint should not appear > 3 times unless the deck has > 15 slides.",
            "If technique appears > 3 times, vary its parameters (scale, color, position) or combine with a different W weapon.",
            "Weight trace should show wave pattern; avoid 3+ consecutive high (>=7) or 3+ consecutive low (<=3).",
            "Overused items should be avoided on the current page unless semantically required.",
        ],
    }


def summarize_page_for_continuity(page: dict[str, Any]) -> dict[str, Any]:
    director = page.get("director_command") if isinstance(page.get("director_command"), dict) else {}
    cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
    intent = infer_design_intent(page)
    return {
        "slide_number": page.get("slide_number"),
        "title": page.get("title"),
        "page_type": page.get("page_type"),
        "layout_hint": page.get("layout_hint"),
        "focus_zone": page.get("focus_zone"),
        "visual_weight": page.get("visual_weight"),
        "rhythm_action": page.get("rhythm_action"),
        "ambition_level": intent.get("ambition_level"),
        "memory_point": intent.get("memory_point"),
        "techniques": as_list(director.get("techniques")),
        "card_styles": [card.get("card_style") for card in cards if isinstance(card.get("card_style"), str)],
    }


def build_local_continuity(planning_payload: dict[str, Any], slide_number: int) -> str:
    pages = [page for page in as_list(planning_payload.get("pages")) if isinstance(page, dict)]
    previous_page = None
    current_page = None
    next_page = None
    for idx, page in enumerate(pages):
        if page.get("slide_number") != slide_number:
            continue
        current_page = page
        previous_page = pages[idx - 1] if idx > 0 else None
        next_page = pages[idx + 1] if idx + 1 < len(pages) else None
        break
    payload = {
        "workflow_metadata": build_workflow_metadata("html_local_continuity", slide_number=slide_number),
        "previous_page": summarize_page_for_continuity(previous_page) if isinstance(previous_page, dict) else None,
        "current_page": summarize_page_for_continuity(current_page) if isinstance(current_page, dict) else None,
        "next_page": summarize_page_for_continuity(next_page) if isinstance(next_page, dict) else None,
        "deck_coherence": build_deck_coherence_summary(pages, slide_number),
        "rule": "If a nearby page reuses a similar structure, shift at least 2 axes: focus, whitespace, card-style mix, technique mix, or material treatment. Check deck_coherence.overused_warning and deck_coherence.weight_trace to avoid distant repetition and rhythm monotony.",
    }
    return pretty_json(payload)


def build_local_continuity_brief(planning_payload: dict[str, Any], slide_number: int) -> str:
    pages = [page for page in as_list(planning_payload.get("pages")) if isinstance(page, dict)]
    previous_page = None
    current_page = None
    next_page = None
    for idx, page in enumerate(pages):
        if page.get("slide_number") != slide_number:
            continue
        current_page = page
        previous_page = pages[idx - 1] if idx > 0 else None
        next_page = pages[idx + 1] if idx + 1 < len(pages) else None
        break

    def row(label: str, page: dict[str, Any] | None) -> str:
        if not isinstance(page, dict):
            return f"{label}: N/A"
        summary = summarize_page_for_continuity(page)
        return (
            f"{label}: slide {summary.get('slide_number')} | {summary.get('title')} | "
            f"layout={summary.get('layout_hint')} | focus={summary.get('focus_zone')} | "
            f"weight={summary.get('visual_weight')} | techniques={','.join(summary.get('techniques', [])) or 'N/A'}"
        )

    coherence = build_deck_coherence_summary(pages, slide_number)
    overused = coherence.get("overused_warning", {})
    overused_layouts = overused.get("layouts", [])
    overused_techniques = overused.get("techniques", [])
    overused_line = ""
    if overused_layouts or overused_techniques:
        parts = []
        if overused_layouts:
            parts.append(f"layouts: {','.join(overused_layouts)}")
        if overused_techniques:
            parts.append(f"techniques: {','.join(overused_techniques)}")
        overused_line = f"overused_warning: {' | '.join(parts)}"

    weight_trace = coherence.get("weight_trace", [])
    weights_str = " -> ".join(
        f"{'[' if w.get('is_current') else ''}{w.get('slide')}:{w.get('weight', '?')}{']' if w.get('is_current') else ''}"
        for w in weight_trace
    ) or "N/A"

    lines = [
        "[LOCAL_CONTINUITY_BRIEF]",
        row("previous", previous_page),
        row("current", current_page),
        row("next", next_page),
        f"deck_layout_usage: {', '.join(f'{k}({v})' for k, v in coherence.get('layout_usage', {}).items()) or 'N/A'}",
        f"deck_weight_trace: {weights_str}",
    ]
    if overused_line:
        lines.append(overused_line)
    lines.append(
        "rule: if a nearby page uses a similar structure, shift at least 2 axes: focus, whitespace, card-style mix, technique mix, or material treatment. Avoid overused layouts/techniques unless semantically required."
    )

    return "\n".join(lines).strip()


def build_page_contract_json(page: dict[str, Any]) -> str:
    cards_payload: list[dict[str, Any]] = []
    for card in as_list(page.get("cards")):
        if not isinstance(card, dict):
            continue
        entry: dict[str, Any] = {
            "card_id": card.get("card_id"),
            "role": card.get("role"),
            "card_type": card.get("card_type"),
            "card_style": card.get("card_style"),
            "visual_weight": card.get("visual_weight"),
            "layout_span": card.get("layout_span"),
            "headline": card.get("headline"),
            "body": as_list(card.get("body"))[:4],
            "content_focus": card.get("content_focus"),
            "micro_detail_plan": as_list(card.get("micro_detail_plan"))[:4],
        }
        data_points = []
        for item in as_list(card.get("data_points"))[:4]:
            if not isinstance(item, dict):
                continue
            data_points.append(
                {
                    "label": item.get("label"),
                    "value": item.get("value"),
                    "source": item.get("source"),
                    "proves": item.get("proves"),
                }
            )
        if data_points:
            entry["data_points"] = data_points
        chart = card.get("chart")
        if isinstance(chart, dict) and chart.get("chart_type"):
            entry["chart"] = {
                "chart_type": chart.get("chart_type"),
                "purpose": chart.get("purpose"),
            }
        image = card.get("image")
        if isinstance(image, dict) and image.get("needed"):
            entry["image"] = {
                "needed": image.get("needed"),
                "usage": image.get("usage"),
                "placement": image.get("placement"),
                "path": image.get("path"),
                "content_description": image.get("content_description"),
            }
        cards_payload.append(entry)

    director = page.get("director_command") if isinstance(page.get("director_command"), dict) else {}
    handoff = page.get("handoff_to_design") if isinstance(page.get("handoff_to_design"), dict) else {}
    variation = page.get("variation_guardrails") if isinstance(page.get("variation_guardrails"), dict) else {}
    payload = {
        "slide_number": page.get("slide_number"),
        "page_type": page.get("page_type"),
        "title": page.get("title"),
        "page_goal": page.get("page_goal"),
        "layout_hint": page.get("layout_hint"),
        "focus_zone": page.get("focus_zone"),
        "negative_space_target": page.get("negative_space_target"),
        "page_text_strategy": page.get("page_text_strategy"),
        "visual_weight": page.get("visual_weight"),
        "audience_takeaway": page.get("audience_takeaway"),
        "density_label": page.get("density_label"),
        "rhythm_action": page.get("rhythm_action"),
        "must_avoid": as_list(page.get("must_avoid")),
        "director_command": {
            "techniques": as_list(director.get("techniques"))[:6],
            "anchor_treatment": director.get("anchor_treatment"),
            "contrast_pair": director.get("contrast_pair"),
        },
        "handoff_to_design": {
            "non_negotiables": as_list(handoff.get("non_negotiables"))[:6],
            "creative_freedom": as_list(handoff.get("creative_freedom"))[:6],
        },
        "variation_guardrails": {
            "avoid_repeating": as_list(variation.get("avoid_repeating"))[:6],
        },
        "cards": cards_payload,
    }
    return pretty_json(payload)


def build_style_runtime_brief(style: dict[str, Any]) -> str:
    decoration = style.get("decoration_dna", {}) if isinstance(style.get("decoration_dna"), dict) else {}
    css_variables = style.get("css_variables") if isinstance(style.get("css_variables"), dict) else {}
    key_vars = []
    for key in ("--color-bg", "--color-surface", "--color-text", "--color-accent"):
        value = css_variables.get(key)
        if isinstance(value, str):
            key_vars.append(f"{key}={value}")
    lines = [
        "[STYLE_RUNTIME_BRIEF]",
        f"style_id: {style.get('style_id', 'unknown')}",
        f"style_name: {style.get('style_name', 'unknown')}",
        f"design_soul: {style.get('design_soul', 'N/A')}",
        f"variation_strategy: {style.get('variation_strategy', 'N/A')}",
        f"signature_move: {decoration.get('signature_move', 'N/A')}",
        f"forbidden: {' | '.join(as_list(decoration.get('forbidden'))) or 'N/A'}",
        f"key_css_vars: {' | '.join(key_vars) or 'N/A'}",
    ]
    return "\n".join(lines).strip()


def build_resource_runtime_brief(page: dict[str, Any]) -> str:
    plan = page_resource_plan(page)
    lines = [
        "[RESOURCE_RUNTIME_BRIEF]",
        f"page_template: {plan.get('page_template') or 'N/A'}",
        f"layout_refs: {' | '.join(plan.get('layout_refs', [])) or 'N/A'}",
        f"block_refs: {' | '.join(plan.get('block_refs', [])) or 'N/A'}",
        f"chart_refs: {' | '.join(plan.get('chart_refs', [])) or 'N/A'}",
        f"principle_refs: {' | '.join(plan.get('principle_refs', [])) or 'N/A'}",
        f"route_notes: {' || '.join(plan.get('route_notes', [])) or 'N/A'}",
    ]
    return "\n".join(lines).strip()


def build_page_route_brief(page: dict[str, Any]) -> str:
    cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
    anchor = next((card for card in cards if card.get("role") == "anchor"), None)
    support_ids = [str(card.get("card_id")) for card in cards if card.get("role") == "support" and card.get("card_id")]
    handoff = page.get("handoff_to_design") if isinstance(page.get("handoff_to_design"), dict) else {}
    variation = page.get("variation_guardrails") if isinstance(page.get("variation_guardrails"), dict) else {}
    non_negotiables = [item for item in as_list(handoff.get("non_negotiables")) if isinstance(item, str)]
    creative_freedom = [item for item in as_list(handoff.get("creative_freedom")) if isinstance(item, str)]
    avoid_repeat = [item for item in as_list(variation.get("avoid_repeating")) if isinstance(item, str)]
    lines = [
        "[PAGE_ROUTE]",
        f"slide_number: {page.get('slide_number')}",
        f"page_type: {page.get('page_type')}",
        f"title: {page.get('title')}",
        f"page_goal: {page.get('page_goal')}",
        f"layout_hint: {page.get('layout_hint')}",
        f"focus_zone: {page.get('focus_zone', 'N/A')}",
        f"negative_space_target: {page.get('negative_space_target', 'N/A')}",
        f"page_text_strategy: {page.get('page_text_strategy', 'N/A')}",
        f"visual_weight: {page.get('visual_weight')}",
        build_density_contract_brief(page, compact=True),
        f"anchor_card: {anchor.get('card_id') if isinstance(anchor, dict) else 'N/A'}",
        f"support_cards: {' | '.join(support_ids) or 'N/A'}",
        f"must_avoid: {' | '.join(page.get('must_avoid', [])) or 'N/A'}",
        f"non_negotiables: {' | '.join(non_negotiables[:4]) or 'N/A'}",
        f"creative_freedom: {' | '.join(creative_freedom[:4]) or 'N/A'}",
        f"avoid_repeating: {' | '.join(avoid_repeat[:4]) or 'N/A'}",
    ]
    return "\n".join(lines).strip()


def build_html_metadata_contract(page: dict[str, Any]) -> str:
    cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
    lines = [
        "[HTML_METADATA_CONTRACT]",
        "body_required_attrs:",
        f"- data-slide-number={page.get('slide_number')}",
        f"- data-page-type={page.get('page_type')}",
        f"- data-layout={page.get('layout_hint')}",
        f"- data-visual-weight={page.get('visual_weight')}",
        "- data-techniques=<comma-separated techniques when available>",
        "card_container_rule: every planning card must render as one visible wrapper element carrying all three attrs below",
    ]
    for card in cards:
        lines.extend(
            [
                f"- {card.get('card_id', 'unknown')}",
                f"  data-card-id: {card.get('card_id', 'unknown')}",
                f"  data-card-role: {card.get('role', 'N/A')}",
                f"  data-card-type: {card.get('card_type', 'N/A')}",
                f"  data-card-style: {card.get('card_style', 'N/A')}",
            ]
        )
    lines.extend(
        [
            "failure_rule: missing body data-* or missing card wrapper data-* is a contract failure even if the page looks good",
            "schema_rule: treat this as structural contract, not optional polish",
        ]
    )
    return "\n".join(lines).strip()


def build_design_runtime_brief(style: dict[str, Any], page: dict[str, Any], planning_payload: dict[str, Any]) -> str:
    image_info = build_image_info(page) or "N/A"
    lines = [
        "## 4. HTML 设计稿生成",
        "",
        "你是【PPTX 视效总监】。输出一页完整 HTML 幻灯片，不要解释。",
        "",
        "这个文件是 runtime routing brief，不是主资料包。",
        "默认把本文件当作主执行简报；只有外部调用方明确额外提供 `html-packet` 时，才把它当补充资料参考。",
        "",
        "## 执行定位",
        "- `prompt-ready` 是当前主上下文",
        "- `html-packet` 仅在外部调用方额外提供时作为补充资料",
        "- 不要依赖聊天历史或未写明的记忆",
        "",
        "## 全局简报",
        build_global_design_guide(inline_assets=False),
        "",
        "## 风格摘要",
        build_style_runtime_brief(style),
        "",
        "## 页面契约",
        build_page_route_brief(page),
        "",
        "## HTML 元数据合同",
        build_html_metadata_contract(page),
        "",
        "## 页面设计意图",
        build_page_design_intent(page),
        "",
        "## 邻页连续性",
        build_local_continuity_brief(planning_payload, int(page.get("slide_number"))),
        "",
        "## 页面内容摘要",
        build_page_card_manifest(page),
        "",
        "## 内容预算",
        build_content_budget(page),
        "",
        "## 卡片执行合同",
        build_card_execution_contract(page),
        "",
        "## 密度执行计划",
        build_render_density_plan(page),
        "",
        "## 场景解题方式",
        build_scene_execution_brief(page),
        "",
        "## 配图信息",
        image_info,
        "",
        "## 资源导航",
        build_resource_runtime_brief(page),
        "",
        "## 最终提醒",
        "- 先满足 density_contract，再做装饰",
        "- body 与 card wrapper 的 data-* 合同必须完整落地",
        "- 让每张 planning 卡片都保持可感知 payload，不要压成空壳",
        "- 先保 page_goal / anchor / card roles，再做风格变化",
        "- 普通内容页不能靠留白和气氛交差",
        "- 空间紧张时先压缩文案和装饰，不删核心 payload",
        "- 只输出完整 HTML",
    ]
    return "\n".join(lines).strip() + "\n"

def assemble_planning_prompt(args: argparse.Namespace) -> int:
    outline = load_outline_payload(Path(args.outline))
    style = unwrap_payload(load_jsonish(Path(args.style)), "style") if args.style else {}
    previous_summary = ""
    if args.previous_planning:
        previous = load_planning_payload(Path(args.previous_planning))
        previous_summary = summarize_previous_pages(previous)

    template = read_text(Path(args.template or PROMPTS / "prompt-3-planning.md"))
    mapping = {
        "OUTLINE_JSON": pretty_json(outline),
        "STYLE_DEFINITION": build_style_definition(style, inline_assets=True) if style else "N/A",
        "PREVIOUS_PAGES": previous_summary or "N/A",
        "NARRATIVE_RHYTHM": read_text(REFS / "runtime" / "narrative-rhythm.md"),
        "DESIGN_PRINCIPLES_CHEATSHEET": read_text(REFS / "principles" / "design-principles-cheatsheet.md"),
        "RESOURCE_MENU": read_text(REFS / "runtime" / "resource-menu.md"),
    }
    output = replace_tokens(template, mapping)
    write_text(Path(args.output), output)
    print(Path(args.output))
    return 0


def validate_slide_lookup(planning_payload: dict[str, Any], slide_number: int) -> dict[str, Any]:
    for page in as_list(planning_payload.get("pages")):
        if page.get("slide_number") == slide_number:
            return page
    raise ValueError(f"Slide {slide_number} not found in planning payload")


def build_design_prompt(
    template_path: Path,
    style: dict[str, Any],
    page: dict[str, Any],
    *,
    self_contained: bool,
    compact: bool,
    planning_payload: dict[str, Any],
) -> str:
    template = read_text(template_path)
    if not self_contained:
        return build_design_runtime_brief(style, page, planning_payload)

    detail_level = infer_compact_detail_level(page) if compact else "medium"
    page_json = build_page_contract_json(page) if compact else pretty_json(page)
    page_route = build_page_route_brief(page)
    page_content = build_page_card_manifest_compact(page) if compact else build_page_content(page)
    image_info = build_image_info(page) or "N/A"
    content_budget = build_content_budget_compact(page) if compact else build_content_budget(page)
    density_contract = build_density_contract_brief(page, compact=compact)
    scene_execution_brief = build_scene_execution_brief(page, compact=compact)
    render_density_plan = build_render_density_plan(page, compact=compact)
    card_execution_contract = build_card_execution_contract(page, compact=compact)
    source_guidance = build_page_source_guidance_compact(page) if compact else build_page_source_guidance(page)
    local_continuity = build_local_continuity(planning_payload, int(page.get("slide_number")))
    if compact:
        local_continuity = build_local_continuity_brief(planning_payload, int(page.get("slide_number")))
        image_info = compact_lines(image_info, max_lines=10, max_chars=700) if image_info != "N/A" else "N/A"

    director = page.get("director_command") if isinstance(page.get("director_command"), dict) else {}
    technique_values = as_list(director.get("techniques"))
    technique_ids = extract_ids(technique_values, "T") or [item for item in technique_values if isinstance(item, str)]

    decoration = page.get("decoration_hints") if isinstance(page.get("decoration_hints"), dict) else {}
    weapon_ids: list[str] = []
    for section in decoration.values():
        if isinstance(section, dict):
            weapon_ids.extend(extract_ids(coerce_list(section.get("weapons")), "W"))

    deduped_weapons: list[str] = []
    seen: set[str] = set()
    for weapon in weapon_ids:
        if weapon not in seen:
            seen.add(weapon)
            deduped_weapons.append(weapon)

    mapping = {
        "GLOBAL_DESIGN_GUIDE": build_global_design_guide(inline_assets=self_contained),
        "STYLE_DEFINITION": build_style_definition(style, inline_assets=self_contained),
        "PLANNING_JSON": page_json,
        "DENSITY_CONTRACT": density_contract,
        "SCENE_EXECUTION_BRIEF": scene_execution_brief,
        "RENDER_DENSITY_PLAN": render_density_plan,
        "CARD_EXECUTION_CONTRACT": card_execution_contract,
        "SOURCE_GUIDANCE": source_guidance,
        "PAGE_DESIGN_INTENT": build_page_design_intent(page),
        "LOCAL_CONTINUITY": local_continuity,
        "PAGE_CONTENT": page_content,
        "CONTENT_BUDGET": content_budget,
        "IMAGE_INFO": image_info,
        "TECHNIQUE_CARDS": (
            render_lookup_block(
                "TECHNIQUES",
                technique_ids,
                TECHNIQUE_SECTIONS,
                compact=compact,
                detail_level=detail_level,
            )
            if self_contained
            else render_runtime_lookup(
                "TECHNIQUES",
                technique_ids,
                TECHNIQUE_CARDS_PATH,
                description="Read only these technique sections if you need exact CSS atoms or parameter ranges.",
            )
        ) or "N/A",
        "CSS_WEAPONS": (
            render_lookup_block(
                "CSS_WEAPONS",
                deduped_weapons,
                WEAPON_SECTIONS,
                compact=compact,
                detail_level=detail_level,
            )
            if self_contained
            else render_runtime_lookup(
                "CSS_WEAPONS",
                deduped_weapons,
                CSS_WEAPONS_PATH,
                description="Read only these weapon sections if you need exact CSS implementation details.",
            )
        ) or "N/A",
        "RESOURCES": build_resource_sections(
            page,
            inline_assets=self_contained,
            compact=compact,
            detail_level=detail_level,
        ) or "N/A",
    }
    return replace_tokens(template, mapping)


def assemble_design_prompt(args: argparse.Namespace) -> int:
    planning = load_planning_payload(Path(args.planning))
    style = unwrap_payload(load_jsonish(Path(args.style)), "style")
    if args.template:
        template = Path(args.template)
    elif args.compact:
        template = PROMPTS / "prompt-4-design-compact.md"
    else:
        template = PROMPTS / "prompt-4-design.md"

    out_dir = Path(args.output_dir) if args.output_dir else None
    if args.all:
        if out_dir is None:
            raise ValueError("--output-dir is required when using --all")
        written: list[str] = []
        for page in as_list(planning.get("pages")):
            slide_number = page.get("slide_number")
            if not isinstance(slide_number, int):
                raise ValueError("Each page must have an integer slide_number")
            content = build_design_prompt(
                template,
                style,
                page,
                self_contained=args.self_contained,
                compact=args.compact,
                planning_payload=planning,
            )
            output = out_dir / f"prompt-ready-{slide_number:02d}.txt"
            write_text(output, content)
            written.append(str(output))
        print("\n".join(written))
        return 0

    if args.slide is None:
        raise ValueError("--slide is required unless --all is used")
    page = validate_slide_lookup(planning, args.slide)
    content = build_design_prompt(
        template,
        style,
        page,
        self_contained=args.self_contained,
        compact=args.compact,
        planning_payload=planning,
    )
    output = Path(args.output or f"prompt-ready-{args.slide:02d}.txt")
    write_text(output, content)
    print(output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Assemble prompt-ready files for planning and design stages")
    subparsers = parser.add_subparsers(dest="command", required=True)

    outline = subparsers.add_parser("outline", help="Assemble a Step 3 outline prompt")
    outline.add_argument("--requirements", required=True, help="Path to requirement(s) JSON or wrapped requirements markdown")
    outline.add_argument("--research", required=True, help="Path to research-package JSON")
    outline.add_argument("--template", help="Optional outline prompt template path")
    outline.add_argument("--output", required=True, help="Output prompt path")
    outline.set_defaults(func=assemble_outline_prompt)

    planning = subparsers.add_parser("planning", help="Assemble a Step 4 planning prompt")
    planning.add_argument("--outline", required=True, help="Path to outline JSON or wrapped outline markdown")
    planning.add_argument("--style", help="Path to style JSON")
    planning.add_argument("--previous-planning", help="Optional prior planning JSON or directory for summary injection")
    planning.add_argument("--template", help="Optional prompt template path")
    planning.add_argument("--output", required=True, help="Output prompt path")
    planning.set_defaults(func=assemble_planning_prompt)

    design = subparsers.add_parser("design", help="Assemble Step 5 design prompts")
    design.add_argument("--planning", required=True, help="Path to planning JSON, single-page file, or planning directory")
    design.add_argument("--style", required=True, help="Path to style JSON")
    design.add_argument("--template", help="Optional design prompt template path")
    design.add_argument("--slide", type=int, help="Single slide number to assemble")
    design.add_argument("--all", action="store_true", help="Assemble all slides")
    design.add_argument("--output", help="Single output path")
    design.add_argument("--output-dir", help="Output directory for --all")
    design.add_argument("--self-contained", action="store_true", help="Inline full guides/resources into each prompt-ready file")
    design.add_argument("--compact", action="store_true", help="Emit compact digests and a slimmer planning contract for Step 5c")
    design.set_defaults(func=assemble_design_prompt)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except Exception as exc:  # pragma: no cover - CLI path
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
