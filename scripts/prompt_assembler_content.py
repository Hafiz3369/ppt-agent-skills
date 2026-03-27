"""Page content, source guidance, design intent, and budget utilities.

Extracted from prompt_assembler.py to keep the main module under 500 lines.
All public functions are re-exported by prompt_assembler for backward compatibility.
"""

from __future__ import annotations

import json
from typing import Any

from prompt_assembler_density import (
    DENSE_SCENE_MODES,
    SOURCE_CONFIDENCE_RULES,
    as_list,
    effective_density_contract,
    build_density_contract_brief,
)


def pretty_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def compact_text(value: Any, limit: int = 96) -> str:
    if value is None:
        return "N/A"
    text = " ".join(str(value).split())
    if not text:
        return "N/A"
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "..."


def first_anchor_card(page: dict[str, Any]) -> dict[str, Any] | None:
    for card in as_list(page.get("cards")):
        if isinstance(card, dict) and card.get("role") == "anchor":
            return card
    return None


def build_card_budget(card: dict[str, Any], page: dict[str, Any]) -> dict[str, int]:
    explicit_budget = card.get("content_budget") if isinstance(card.get("content_budget"), dict) else {}
    if explicit_budget:
        required = {
            "headline_max_chars": "title_chars",
            "max_body_lines": "body_lines",
            "max_chars_per_line": "line_chars",
            "max_bullets": "bullet_count",
            "max_data_points": "data_points",
        }
        if all(isinstance(explicit_budget.get(source), int) for source in required):
            return {
                target: int(explicit_budget[source])
                for source, target in required.items()
            }

    page_type = str(page.get("page_type") or "content")
    density = str(page.get("density_label") or "standard")
    role = str(card.get("role") or "support")

    base = {
        "title_chars": 16,
        "body_lines": 2,
        "line_chars": 18,
        "bullet_count": 3,
        "data_points": 3,
    }
    if page_type == "cover":
        base.update({"title_chars": 18, "body_lines": 2, "line_chars": 16, "bullet_count": 2})
    elif page_type == "toc":
        base.update({"title_chars": 18, "body_lines": 4, "line_chars": 18, "bullet_count": 5})
    elif page_type == "section":
        base.update({"title_chars": 18, "body_lines": 1, "line_chars": 22, "bullet_count": 1})
    elif page_type == "end":
        base.update({"title_chars": 18, "body_lines": 3, "line_chars": 18, "bullet_count": 4})
    elif density == "breath":
        base.update({"title_chars": 18, "body_lines": 2, "line_chars": 18, "bullet_count": 2})
    elif density == "explosion":
        base.update({"title_chars": 22, "body_lines": 4, "line_chars": 22, "bullet_count": 5, "data_points": 5})
    else:
        base.update({"title_chars": 20, "body_lines": 3, "line_chars": 20, "bullet_count": 4, "data_points": 4})

    if role == "anchor":
        base["title_chars"] += 4
        base["body_lines"] += 1
        base["line_chars"] += 2
        base["data_points"] += 1
    elif role == "context":
        base["body_lines"] = max(1, base["body_lines"] - 1)
        base["bullet_count"] = max(1, base["bullet_count"] - 1)
        base["line_chars"] = max(12, base["line_chars"] - 2)

    return base


def build_content_budget(page: dict[str, Any]) -> str:
    cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
    page_budget = page.get("content_budget") if isinstance(page.get("content_budget"), dict) else {}
    contract = effective_density_contract(page)
    scene_mode = str(contract.get("scene_mode") or "business")
    information_pressure = str(contract.get("information_pressure") or "medium")
    dense_scene = scene_mode in DENSE_SCENE_MODES or information_pressure == "high"
    page_title_max_chars = page_budget.get("page_title_max_chars")
    page_body_max_lines = page_budget.get("page_body_max_lines")
    page_keywords_max = page_budget.get("page_keywords_max")
    compression_rule = page_budget.get("compression_rule")
    compression_priority = " -> ".join(item for item in as_list(page.get("compression_priority")) if isinstance(item, str)) or "context -> support -> anchor"
    lines = [
        "[CONTENT_BUDGET]",
        "hard_rule: if content exceeds budget, compress wording before shrinking hierarchy",
        f"page_title_max_chars: {page_title_max_chars if isinstance(page_title_max_chars, int) else (18 if page.get('page_type') in {'cover', 'section', 'end'} else 22)}",
        f"page_body_max_lines: {page_body_max_lines if isinstance(page_body_max_lines, int) else 'N/A'}",
        f"page_keywords_max: {page_keywords_max if isinstance(page_keywords_max, int) else 'N/A'}",
        f"card_count_expected: {len(cards)}",
        f"compression_priority: {compression_priority}",
        f"compression_rule: {compression_rule if isinstance(compression_rule, str) else 'Compress support/context before weakening the anchor hierarchy.'}",
        "global_rules: short declaratives / no filler absent from planning / anchor first / compress support before anchor",
    ]
    if dense_scene:
        lines.extend(
            [
                f"dense_scene_mode: {scene_mode}",
                "dense_scene_rules: support cards carry payload / anchor carries structure-evidence-step-comparison context / fill payload before atmosphere / avoid keynote-hero solution",
            ]
        )
    lines.extend(["", "[CARD_BUDGETS]"])
    for card in cards:
        budget = build_card_budget(card, page)
        lines.extend(
            [
                f"- {card.get('card_id', 'unknown')}",
                f"  role: {card.get('role', 'N/A')}",
                f"  headline_max_chars: {budget['title_chars']}",
                f"  max_body_lines: {budget['body_lines']}",
                f"  max_chars_per_line: {budget['line_chars']}",
                f"  max_bullets: {budget['bullet_count']}",
                f"  max_data_points: {budget['data_points']}",
            ]
        )
    return "\n".join(lines).strip()


def build_content_budget_compact(page: dict[str, Any]) -> str:
    cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
    page_budget = page.get("content_budget") if isinstance(page.get("content_budget"), dict) else {}
    contract = effective_density_contract(page)
    scene_mode = str(contract.get("scene_mode") or "business")
    information_pressure = str(contract.get("information_pressure") or "medium")
    page_title_max_chars = page_budget.get("page_title_max_chars")
    page_body_max_lines = page_budget.get("page_body_max_lines")
    page_keywords_max = page_budget.get("page_keywords_max")
    compression_priority = " -> ".join(
        item for item in as_list(page.get("compression_priority")) if isinstance(item, str)
    ) or "context -> support -> anchor"
    lines = [
        "[CONTENT_BUDGET]",
        f"page_title_max_chars: {page_title_max_chars if isinstance(page_title_max_chars, int) else (18 if page.get('page_type') in {'cover', 'section', 'end'} else 22)}",
        f"page_body_max_lines: {page_body_max_lines if isinstance(page_body_max_lines, int) else 'N/A'}",
        f"page_keywords_max: {page_keywords_max if isinstance(page_keywords_max, int) else 'N/A'}",
        f"card_count_expected: {len(cards)}",
        f"compression_priority: {compression_priority}",
        f"compression_rule: {compact_text(page_budget.get('compression_rule') or 'Compress support/context before weakening the anchor hierarchy.', 120)}",
        f"dense_scene: {scene_mode}/{information_pressure}",
        "[CARD_BUDGETS]",
    ]
    for card in cards:
        budget = build_card_budget(card, page)
        lines.append(
            (
                f"- {card.get('card_id', 'unknown')} | role={card.get('role', 'N/A')} | "
                f"h={budget['title_chars']} | body={budget['body_lines']}x{budget['line_chars']} | "
                f"bullets={budget['bullet_count']} | data={budget['data_points']}"
            )
        )
    return "\n".join(lines).strip()


def infer_design_intent(page: dict[str, Any]) -> dict[str, Any]:
    explicit = page.get("design_intent") if isinstance(page.get("design_intent"), dict) else {}
    page_type = str(page.get("page_type") or "content")
    layout_hint = str(page.get("layout_hint") or "unknown")
    weight = page.get("visual_weight")
    weight = weight if isinstance(weight, int) else 5
    anchor = first_anchor_card(page) or {}
    director = page.get("director_command") if isinstance(page.get("director_command"), dict) else {}
    anchor_treatment = director.get("anchor_treatment") if isinstance(director.get("anchor_treatment"), str) else "主锚点必须承担画面记忆"
    audience_takeaway = page.get("audience_takeaway") if isinstance(page.get("audience_takeaway"), str) else page.get("page_goal")
    title = page.get("title") if isinstance(page.get("title"), str) else "本页主命题"

    if page_type == "cover":
        default_ambition = "dramatic" if weight >= 8 else "assertive"
        default_primary_impact = "在前三秒内立住整套 deck 的气质和主命题，不像普通汇报封面。"
        default_memory_point = f"观众一眼之后仍记得：{title} 这句主命题和它的封面气场。"
        default_contrast = "用主标题尺度、留白和单一强调色建立断层，不靠堆装饰。"
        default_secondary_anchor = "元信息只能做舞台边缘的陪衬，不能与标题争主角。"
    elif page_type == "section":
        default_ambition = "assertive"
        default_primary_impact = f"让观众一秒看懂：下面要讲什么，与上一节有什么不同。"
        default_memory_point = f"章节标题 {title} 必须留下空间记忆。"
        default_contrast = "用字号断层和大面积留白制造节奏切换感。"
        default_secondary_anchor = "章节封面不需要第二支点。"
    elif page_type in {"toc", "end"}:
        default_ambition = "quiet"
        default_primary_impact = "让观众从容理解结构或收束信息，不争夺注意力。"
        default_memory_point = "结构清晰或收束干脆即可，不需要爆发。"
        default_contrast = "保持整体和谐，不刻意制造断层。"
        default_secondary_anchor = "N/A"
    elif weight >= 8:
        default_ambition = "dramatic"
        default_primary_impact = f"让观众前三秒被主锚点击中，不是被装饰分散。{anchor_treatment}"
        default_memory_point = f"翻页之后仍然记得：{audience_takeaway or title}。"
        default_contrast = "用断层字号和焦点色压住一处，其余退后。"
        default_secondary_anchor = "第二支点只做佐证，面积不超过主锚点的 40%。"
    elif weight >= 5:
        default_ambition = "assertive"
        default_primary_impact = f"让观众第一时间抓住核心论点：{audience_takeaway or title}。"
        default_memory_point = f"核心判断必须留下：{title}。"
        default_contrast = "层级拉清楚，但不需要戏剧张力。"
        default_secondary_anchor = "如果有第二支点，必须明确它是 support 而不是平行 anchor。"
    else:
        default_ambition = "quiet"
        default_primary_impact = "让信息可读、层级可辨。"
        default_memory_point = f"让观众知道：{title}。"
        default_contrast = "保持层次清晰即可。"
        default_secondary_anchor = "N/A"

    anti_flatness_rules = as_list(explicit.get("anti_flatness_rules"))
    if not anti_flatness_rules:
        anti_flatness_rules = [
            f"不要做成标准 {layout_hint} 模板的默认长相",
            "不要让所有卡片面积相等、间距相等",
            "不要让装饰把主角淹没",
        ]

    return {
        "ambition_level": explicit.get("ambition_level") or default_ambition,
        "primary_impact": explicit.get("primary_impact") or default_primary_impact,
        "memory_point": explicit.get("memory_point") or default_memory_point,
        "contrast_strategy": explicit.get("contrast_strategy") or default_contrast,
        "secondary_anchor_strategy": explicit.get("secondary_anchor_strategy") or default_secondary_anchor,
        "anti_flatness_rules": anti_flatness_rules,
    }


def build_page_design_intent(page: dict[str, Any]) -> str:
    intent = infer_design_intent(page)
    lines = [
        "[PAGE_DESIGN_INTENT]",
        f"ambition_level: {intent['ambition_level']}",
        f"primary_impact: {intent['primary_impact']}",
        f"memory_point: {intent['memory_point']}",
        f"contrast_strategy: {intent['contrast_strategy']}",
        f"secondary_anchor_strategy: {intent['secondary_anchor_strategy']}",
        "anti_flatness_rules:",
    ]
    lines.extend(f"- {item}" for item in intent["anti_flatness_rules"])
    return "\n".join(lines).strip()


def build_page_content(page: dict[str, Any], *, page_resource_plan_fn: Any = None) -> str:
    resource_rationale = page.get("resource_rationale") if isinstance(page.get("resource_rationale"), dict) else {}
    resource_plan = page_resource_plan_fn(page) if page_resource_plan_fn else {}
    source_guidance = page.get("source_guidance") if isinstance(page.get("source_guidance"), dict) else {}
    review_focus = source_guidance.get("review_focus") if isinstance(source_guidance.get("review_focus"), dict) else {}
    lines = [
        f"slide_number: {page.get('slide_number')}",
        f"page_type: {page.get('page_type')}",
        f"narrative_role: {page.get('narrative_role')}",
        f"title: {page.get('title')}",
        f"page_goal: {page.get('page_goal')}",
        f"focus_zone: {page.get('focus_zone', 'N/A')}",
        f"negative_space_target: {page.get('negative_space_target', 'N/A')}",
        f"page_text_strategy: {page.get('page_text_strategy', 'N/A')}",
        f"compression_priority: {' | '.join(as_list(page.get('compression_priority'))) or 'N/A'}",
        f"audience_takeaway: {page.get('audience_takeaway', 'N/A')}",
        f"visual_weight: {page.get('visual_weight')}",
        f"density_label: {page.get('density_label')}",
        f"emotion_label: {page.get('emotion_label')}",
        f"rhythm_action: {page.get('rhythm_action')}",
        f"layout_hint: {page.get('layout_hint')}",
        build_density_contract_brief(page, compact=True),
    ]
    # --- page_narrative_context: where this page sits in the information flow ---
    pnc = page.get("page_narrative_context") if isinstance(page.get("page_narrative_context"), dict) else None
    if pnc:
        prev_conclusion = pnc.get("previous_page_conclusion")
        next_needs = pnc.get("next_page_needs")
        mission = pnc.get("current_page_mission") if isinstance(pnc.get("current_page_mission"), dict) else {}
        chain = pnc.get("argument_chain")
        lines.append(f"narrative_position: {pnc.get('position_in_part', 'N/A')} in Part '{pnc.get('part_title', 'N/A')}'")
        if isinstance(prev_conclusion, dict):
            lines.append(f"previous_page_established: {prev_conclusion.get('goal', 'N/A')}")
        if isinstance(mission, dict) and mission.get("instruction"):
            lines.append(f"current_page_mission: {mission['instruction']}")
        if isinstance(next_needs, dict):
            lines.append(f"next_page_needs: {next_needs.get('prerequisite', 'N/A')}")
        if isinstance(chain, list) and len(chain) > 1:
            lines.append(f"argument_chain: {' -> '.join(chain)}")
    lines.extend([
        f"review_focus.primary_concern_ids: {' | '.join(as_list(review_focus.get('primary_concern_ids'))) or 'N/A'}",
        f"review_focus.page_completion_rule: {review_focus.get('page_completion_rule', 'N/A')}",
        f"must_avoid: {' | '.join(page.get('must_avoid', [])) or 'N/A'}",
        f"resource_rationale.layout_refs: {resource_rationale.get('layout_refs', 'N/A')}",
        f"resource_rationale.block_refs: {resource_rationale.get('block_refs', 'N/A')}",
        f"resource_rationale.chart_refs: {resource_rationale.get('chart_refs', 'N/A')}",
        f"resource_rationale.principle_refs: {resource_rationale.get('principle_refs', 'N/A')}",
        f"effective_resources.page_template: {resource_plan.get('page_template') or 'N/A'}",
        f"effective_resources.layout_refs: {' | '.join(resource_plan.get('layout_refs', [])) or 'N/A'}",
        f"effective_resources.block_refs: {' | '.join(resource_plan.get('block_refs', [])) or 'N/A'}",
        f"effective_resources.chart_refs: {' | '.join(resource_plan.get('chart_refs', [])) or 'N/A'}",
        f"effective_resources.principle_refs: {' | '.join(resource_plan.get('principle_refs', [])) or 'N/A'}",
        f"resource_route_notes: {' || '.join(resource_plan.get('route_notes', [])) or 'N/A'}",
        "",
        "[CARDS]",
    ])
    for idx, card in enumerate(as_list(page.get("cards")), start=1):
        lines.extend(
            [
                f"- card {idx}: {card.get('card_id', 'unknown')}",
                f"  role: {card.get('role')}",
                f"  card_type: {card.get('card_type')}",
                f"  card_style: {card.get('card_style')}",
                f"  visual_weight: {card.get('visual_weight')}",
                f"  layout_span: {card.get('layout_span')}",
                f"  content_focus: {card.get('content_focus')}",
                f"  argument_role: {card.get('argument_role', 'N/A')}",
                f"  content_budget: {pretty_json(card.get('content_budget')) if isinstance(card.get('content_budget'), dict) else 'N/A'}",
                f"  headline: {card.get('headline', 'N/A')}",
                f"  body: {' | '.join(card.get('body', [])) or 'N/A'}",
                f"  micro_detail_plan: {' | '.join(card.get('micro_detail_plan', [])) or 'N/A'}",
            ]
        )
        for item in as_list(card.get("data_points")):
            if isinstance(item, dict):
                proves = item.get("proves", "")
                proves_str = f" | proves: {proves}" if proves else ""
                lines.append(
                    "  data_point: "
                    f"{item.get('label', 'N/A')} = {item.get('value', 'N/A')} | source: {item.get('source', 'N/A')}{proves_str}"
                )
        chart = card.get("chart") or {}
        if isinstance(chart, dict) and chart.get("chart_type"):
            lines.append(f"  chart: {chart.get('chart_type')} | purpose: {chart.get('purpose', 'N/A')}")
    return "\n".join(lines).strip()


def build_page_card_manifest(page: dict[str, Any]) -> str:
    lines = ["[CARD_MANIFEST]"]
    for idx, card in enumerate(as_list(page.get("cards")), start=1):
        if not isinstance(card, dict):
            continue
        lines.extend(
            [
                f"- card {idx}: {card.get('card_id', 'unknown')}",
                f"  role: {card.get('role')}",
                f"  card_type: {card.get('card_type')}",
                f"  card_style: {card.get('card_style')}",
                f"  headline: {card.get('headline', 'N/A')}",
                f"  body: {' | '.join(card.get('body', [])) or 'N/A'}",
                f"  content_focus: {card.get('content_focus', 'N/A')}",
            ]
        )
        data_points = [item for item in as_list(card.get("data_points")) if isinstance(item, dict)]
        if data_points:
            lines.append(
                "  data_points: "
                + " | ".join(
                    f"{item.get('label', 'N/A')}={item.get('value', 'N/A')}"
                    for item in data_points[:4]
                )
            )
        chart = card.get("chart") or {}
        if isinstance(chart, dict) and chart.get("chart_type"):
            lines.append(f"  chart: {chart.get('chart_type')} | purpose: {chart.get('purpose', 'N/A')}")
    if len(lines) == 1:
        lines.append("- N/A")
    return "\n".join(lines).strip()


def build_page_card_manifest_compact(page: dict[str, Any]) -> str:
    lines = ["[CARD_MANIFEST]"]
    for idx, card in enumerate(as_list(page.get("cards")), start=1):
        if not isinstance(card, dict):
            continue
        body = " || ".join(compact_text(item, 52) for item in as_list(card.get("body")) if isinstance(item, str)) or "N/A"
        line = (
            f"- card {idx}: {card.get('card_id', 'unknown')} | role={card.get('role', 'N/A')} | "
            f"type={card.get('card_type', 'N/A')} | style={card.get('card_style', 'N/A')} | "
            f"headline={compact_text(card.get('headline'), 48)}"
        )
        lines.append(line)
        lines.append(f"  body: {body}")
        lines.append(f"  focus: {compact_text(card.get('content_focus'), 96)}")
        data_points = [item for item in as_list(card.get("data_points")) if isinstance(item, dict)]
        if data_points:
            lines.append(
                "  data_points: "
                + " | ".join(
                    compact_text(f"{item.get('label', 'N/A')}={item.get('value', 'N/A')}", 42)
                    for item in data_points[:4]
                )
            )
        chart = card.get("chart") or {}
        if isinstance(chart, dict) and chart.get("chart_type"):
            lines.append(
                f"  chart: {chart.get('chart_type')} | purpose: {compact_text(chart.get('purpose'), 72)}"
            )
    if len(lines) == 1:
        lines.append("- N/A")
    return "\n".join(lines).strip()


def build_page_source_guidance(page: dict[str, Any]) -> str:
    guidance = page.get("source_guidance") if isinstance(page.get("source_guidance"), dict) else {}
    review_focus = guidance.get("review_focus") if isinstance(guidance.get("review_focus"), dict) else {}
    cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
    anchor_cards = [card for card in cards if card.get("role") == "anchor"]
    support_cards = [card for card in cards if card.get("role") == "support"]

    def target_card_for_usage(usage_mode: str) -> str:
        if usage_mode == "anchor" and anchor_cards:
            return str(anchor_cards[0].get("card_id") or "anchor-card")
        if usage_mode == "support" and support_cards:
            return str(support_cards[0].get("card_id") or "support-card")
        if cards:
            return str(cards[0].get("card_id") or "page-card")
        return "page-card"

    lines = [
        "[SOURCE_GUIDANCE]",
        f"primary_source_ids: {' | '.join(as_list(guidance.get('primary_source_ids'))) or 'N/A'}",
        f"supporting_source_ids: {' | '.join(as_list(guidance.get('supporting_source_ids'))) or 'N/A'}",
        f"citation_rule: {guidance.get('citation_rule', 'N/A')}",
        "",
        "[SOURCE_EXECUTION_RULES]",
        "- Do not turn qualified / derived claims into hard proof.",
        "- Let the anchor card carry the main claim wording; support cards unpack why or how.",
        "- If wording becomes too absolute, weaken the sentence before weakening hierarchy.",
        "- Minimal source hints are enough when needed; do not dump citations into the layout.",
        "confidence_ladder:",
        f"- hard: {SOURCE_CONFIDENCE_RULES['hard']['render_rule']}",
        f"- qualified: {SOURCE_CONFIDENCE_RULES['qualified']['render_rule']}",
        f"- derived: {SOURCE_CONFIDENCE_RULES['derived']['render_rule']}",
        "",
        "claim_binding:",
    ]
    claim_binding = as_list(guidance.get("claim_binding"))
    if not claim_binding:
        lines.append("- N/A")
    else:
        for item in claim_binding:
            if not isinstance(item, dict):
                continue
            confidence = str(item.get("confidence") or "qualified")
            usage_mode = str(item.get("usage_mode") or "support")
            render_intent = item.get("render_intent") if isinstance(item.get("render_intent"), dict) else {}
            rule = SOURCE_CONFIDENCE_RULES.get(confidence, SOURCE_CONFIDENCE_RULES["qualified"])
            render_rule = str(render_intent.get("render_rule") or rule["render_rule"])
            preferred_phrases = [
                value for value in as_list(render_intent.get("preferred_phrases")) if isinstance(value, str)
            ] or list(rule["qualifier_examples"])
            avoid_phrases = [
                value for value in as_list(render_intent.get("avoid_phrases")) if isinstance(value, str)
            ] or list(rule["avoid_phrases"])
            target_card = str(render_intent.get("target_card") or target_card_for_usage(usage_mode))
            lines.append(
                "- "
                f"claim: {item.get('claim', 'N/A')} | "
                f"source_id: {item.get('source_id', 'N/A')} | "
                f"usage_mode: {usage_mode} | "
                f"confidence: {confidence}"
            )
            lines.append(f"  target_card: {target_card}")
            lines.append(f"  render_rule: {render_rule}")
            lines.append(f"  preferred_phrases: {' | '.join(preferred_phrases)}")
            lines.append(f"  avoid_phrases: {' | '.join(avoid_phrases)}")
    lines.extend(
        [
            "",
            "[REVIEW_FOCUS]",
            f"primary_concern_ids: {' | '.join(as_list(review_focus.get('primary_concern_ids'))) or 'N/A'}",
            f"page_completion_rule: {review_focus.get('page_completion_rule', 'N/A')}",
            f"html_rule: {review_focus.get('html_rule', 'N/A')}",
            "items:",
        ]
    )
    focus_items = as_list(review_focus.get("items"))
    if not focus_items:
        lines.append("- N/A")
    else:
        for item in focus_items:
            if not isinstance(item, dict):
                continue
            lines.append(
                "- "
                f"concern_id: {item.get('concern_id', 'N/A')} | "
                f"must_answer_by: {item.get('must_answer_by', 'N/A')} | "
                f"coverage_status: {item.get('coverage_status', 'N/A')}"
            )
            lines.append(f"  question: {item.get('question', 'N/A')}")
            lines.append(f"  failure_if_missing: {item.get('failure_if_missing', 'N/A')}")
            lines.append(f"  gap_note: {item.get('gap_note', 'N/A')}")
            support = [value for value in as_list(item.get('best_available_support')) if isinstance(value, str)]
            lines.append(f"  best_available_support: {' | '.join(support) or 'N/A'}")
    return "\n".join(lines).strip()


def build_page_source_guidance_compact(page: dict[str, Any]) -> str:
    guidance = page.get("source_guidance") if isinstance(page.get("source_guidance"), dict) else {}
    review_focus = guidance.get("review_focus") if isinstance(guidance.get("review_focus"), dict) else {}
    cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
    anchor_cards = [card for card in cards if card.get("role") == "anchor"]
    support_cards = [card for card in cards if card.get("role") == "support"]

    def target_card_for_usage(usage_mode: str) -> str:
        if usage_mode == "anchor" and anchor_cards:
            return str(anchor_cards[0].get("card_id") or "anchor-card")
        if usage_mode == "support" and support_cards:
            return str(support_cards[0].get("card_id") or "support-card")
        if cards:
            return str(cards[0].get("card_id") or "page-card")
        return "page-card"

    lines = [
        "[SOURCE_GUIDANCE]",
        f"primary_source_ids: {' | '.join(as_list(guidance.get('primary_source_ids'))) or 'N/A'}",
        f"supporting_source_ids: {' | '.join(as_list(guidance.get('supporting_source_ids'))) or 'N/A'}",
        f"citation_rule: {compact_text(guidance.get('citation_rule'), 140)}",
        "[CLAIM_BINDING]",
    ]
    claim_binding = as_list(guidance.get("claim_binding"))
    if not claim_binding:
        lines.append("- N/A")
    else:
        for item in claim_binding:
            if not isinstance(item, dict):
                continue
            confidence = str(item.get("confidence") or "qualified")
            usage_mode = str(item.get("usage_mode") or "support")
            render_intent = item.get("render_intent") if isinstance(item.get("render_intent"), dict) else {}
            rule = SOURCE_CONFIDENCE_RULES.get(confidence, SOURCE_CONFIDENCE_RULES["qualified"])
            render_rule = compact_text(render_intent.get("render_rule") or rule["render_rule"], 120)
            preferred_phrases = [
                value for value in as_list(render_intent.get("preferred_phrases")) if isinstance(value, str)
            ] or list(rule["qualifier_examples"])
            avoid_phrases = [
                value for value in as_list(render_intent.get("avoid_phrases")) if isinstance(value, str)
            ] or list(rule["avoid_phrases"])
            target_card = str(render_intent.get("target_card") or target_card_for_usage(usage_mode))
            lines.append(
                (
                    f"- claim: {compact_text(item.get('claim'), 88)} | source_id: {item.get('source_id', 'N/A')} | "
                    f"usage_mode: {usage_mode} | confidence: {confidence} | target_card: {target_card}"
                )
            )
            lines.append(f"  render_rule: {render_rule}")
            lines.append(
                f"  preferred_phrases: {' | '.join(compact_text(value, 24) for value in preferred_phrases) or 'N/A'}"
            )
            lines.append(
                f"  avoid_phrases: {' | '.join(compact_text(value, 24) for value in avoid_phrases) or 'N/A'}"
            )

    lines.extend(
        [
            "[REVIEW_FOCUS]",
            f"primary_concern_ids: {' | '.join(as_list(review_focus.get('primary_concern_ids'))) or 'N/A'}",
            f"page_completion_rule: {compact_text(review_focus.get('page_completion_rule'), 140)}",
            f"html_rule: {compact_text(review_focus.get('html_rule'), 140)}",
            "items:",
        ]
    )
    focus_items = as_list(review_focus.get("items"))
    if not focus_items:
        lines.append("- N/A")
    else:
        for item in focus_items:
            if not isinstance(item, dict):
                continue
            lines.append(
                (
                    f"- concern_id: {item.get('concern_id', 'N/A')} | must_answer_by: {item.get('must_answer_by', 'N/A')} | "
                    f"coverage_status: {item.get('coverage_status', 'N/A')}"
                )
            )
            lines.append(f"  question: {compact_text(item.get('question'), 120)}")
            lines.append(f"  failure_if_missing: {compact_text(item.get('failure_if_missing'), 120)}")
            lines.append(f"  gap_note: {compact_text(item.get('gap_note'), 120)}")
            support = [value for value in as_list(item.get('best_available_support')) if isinstance(value, str)]
            lines.append(
                f"  best_available_support: {' | '.join(compact_text(value, 40) for value in support) or 'N/A'}"
            )
    return "\n".join(lines).strip()


def build_image_info(page: dict[str, Any]) -> str:
    rows: list[str] = []
    for card in as_list(page.get("cards")):
        image = card.get("image") if isinstance(card, dict) else None
        if not isinstance(image, dict) or not image.get("needed"):
            continue
        card_id = card.get("card_id", "unknown")
        has_path = bool(image.get("path"))
        status = "[READY]" if has_path else "[PENDING]"
        parts = [
            f"card: {card_id} {status}",
            f"usage: {image.get('usage', 'N/A')}",
            f"placement: {image.get('placement', 'N/A')}",
        ]
        # Planning 层字段（内容意图）
        if image.get("content_description"):
            parts.append(f"content_description: {image['content_description']}")
        if image.get("source_hint"):
            parts.append(f"source_hint: {image['source_hint']}")
        # Step 5b 回填的生成规格（如有）
        if image.get("dimensions"):
            parts.append(f"dimensions: {image['dimensions']}")
        if image.get("aspect_ratio"):
            parts.append(f"aspect_ratio: {image['aspect_ratio']}")
        if image.get("format"):
            parts.append(f"format: {image['format']}")
        if image.get("style"):
            parts.append(f"style: {image['style']}")
        if image.get("prompt"):
            parts.append(f"prompt: {image['prompt']}")
        if image.get("alt_text"):
            parts.append(f"alt_text: {image['alt_text']}")
        if has_path:
            parts.append(f"path: {image['path']}")
        rows.append("\n  ".join(parts))
    return "\n".join(rows).strip()
