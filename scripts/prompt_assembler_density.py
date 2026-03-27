"""Density contract, scene execution, and render density utilities.

Extracted from prompt_assembler.py to keep the main module under 500 lines.
All public functions are re-exported by prompt_assembler for backward compatibility.
"""

from __future__ import annotations

from typing import Any

VALID_AMBITION_LEVELS = {"quiet", "assertive", "dramatic"}
DENSE_SCENE_MODES = {"report", "academic", "technical", "training"}
PAYLOAD_HEAVY_CARD_TYPES = {
    "data", "data_highlight", "comparison", "process", "timeline",
    "diagram", "matrix_chart", "list", "quote", "people",
}

# card_type -> 推荐装饰密度档位
# 当页面包含多种 card_type 时，取最低档位（内容优先原则）
CARD_TYPE_DECORATION_BUDGET: dict[str, str] = {
    # 数据密集型 -> 装饰克制
    "data": "low",
    "data_highlight": "medium",
    "comparison": "low",
    "matrix_chart": "low",
    # 结构展示型 -> 中等装饰
    "process": "medium",
    "timeline": "medium",
    "diagram": "medium",
    # 内容承载型 -> 根据上下文
    "text": "medium",
    "list": "low",
    "tag_cloud": "medium",
    # 叙事/情绪型 -> 可偏装饰
    "quote": "medium",
    "people": "medium",
    "image_hero": "generous",
}

DECORATION_BUDGET_RANK: dict[str, int] = {
    "minimal": 0,
    "low": 1,
    "medium": 2,
    "generous": 3,
}

PAGE_TYPE_DECORATION_BUDGET: dict[str, str] = {
    "cover": "generous",
    "section": "generous",
    "toc": "low",
    "end": "generous",
}


def _lowest_budget(*budgets: str) -> str:
    """取多个装饰预算中最低的一个（内容优先原则）。"""
    if not budgets:
        return "medium"
    return min(budgets, key=lambda b: DECORATION_BUDGET_RANK.get(b, 2))


def infer_decoration_budget(
    page_type: str,
    card_types: list[str],
    scene_mode: str,
    information_pressure: str,
    negative_space: float,
) -> str:
    """根据页面类型、card_type 组合、scene_mode 和信息压力推断装饰密度。"""
    # 1. 先看页面类型有没有强制默认
    page_default = PAGE_TYPE_DECORATION_BUDGET.get(page_type)
    if page_default and page_type != "content":
        # 非 content 页直接用页面类型默认
        # 但 dense scene 仍然需要压低
        if scene_mode in DENSE_SCENE_MODES or information_pressure == "high":
            return _lowest_budget(page_default, "low")
        return page_default

    # 2. 如果是 dense scene 或高信息压力，基础上限是 low
    if scene_mode in DENSE_SCENE_MODES or information_pressure == "high":
        ceiling = "low"
    elif negative_space >= 0.40:
        # 高留白页 -> 允许更丰富装饰
        ceiling = "generous"
    elif negative_space >= 0.34:
        ceiling = "medium"
    else:
        ceiling = "medium"

    # 3. 收集所有 card_type 的推荐装饰密度
    card_budgets = [CARD_TYPE_DECORATION_BUDGET.get(ct, "medium") for ct in card_types if ct]
    if card_budgets:
        card_floor = _lowest_budget(*card_budgets)
        # card 视角 vs 上下文 ceiling，取更低的
        return _lowest_budget(card_floor, ceiling)

    return ceiling
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
        "render_rule": '必须写成机制判断或诊断表达，强调"更像什么/意味着什么/不是单纯什么"，不要伪装成硬统计。',
        "qualifier_examples": ["更像", "意味着", "说明", "提示", "本质上", "不是单纯", "核心问题是"],
        "avoid_phrases": ["数据证明", "已经验证", "最终结论", "全面达成"],
    },
}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def compact_text(value: Any, limit: int = 96) -> str:
    if value is None:
        return "N/A"
    text = " ".join(str(value).split())
    if not text:
        return "N/A"
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "..."


def effective_density_contract(page: dict[str, Any]) -> dict[str, Any]:
    explicit = page.get("density_contract") if isinstance(page.get("density_contract"), dict) else {}
    if explicit:
        return explicit

    page_type = str(page.get("page_type") or "content")
    density_label = str(page.get("density_label") or "standard")
    page_text_strategy = str(page.get("page_text_strategy") or "")
    narrative_role = str(page.get("narrative_role") or "")
    cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
    card_roles = [str(card.get("role")) for card in cards if isinstance(card.get("role"), str)]
    card_types = [str(card.get("card_type")) for card in cards if isinstance(card.get("card_type"), str)]
    chart_types = []
    for card in cards:
        chart = card.get("chart") if isinstance(card.get("chart"), dict) else None
        chart_type = chart.get("chart_type") if isinstance(chart, dict) else None
        if isinstance(chart_type, str):
            chart_types.append(chart_type)

    if page_type in {"cover", "section"}:
        scene_mode = "launch"
    elif page_type in {"toc", "end"}:
        scene_mode = "business"
    elif (
        page_text_strategy in {"metric-led", "contrast-led"}
        or any(card_type in {"data", "data_highlight", "comparison", "matrix_chart"} for card_type in card_types)
        or bool(chart_types)
    ):
        scene_mode = "report"
    elif narrative_role in {"process", "framework"} or any(card_type in {"process", "diagram", "timeline"} for card_type in card_types):
        scene_mode = "technical"
    else:
        scene_mode = "business"

    if density_label == "explosion":
        information_pressure = "high"
    elif page_type == "content" and (len(cards) >= 3 or page_text_strategy in {"metric-led", "contrast-led", "multi-point"}):
        information_pressure = "high"
    elif density_label == "breath":
        information_pressure = "low"
    else:
        information_pressure = "medium"

    if page_type == "content":
        minimum_card_count = max(2, len(cards)) if cards else (3 if information_pressure == "high" else 2)
    else:
        minimum_card_count = max(1, len(cards)) if cards else 1

    must_have_roles = []
    for role in ("anchor", "support", "context"):
        if role in card_roles:
            must_have_roles.append(role)
    if not must_have_roles:
        must_have_roles = ["anchor"] if page_type != "content" else ["anchor", "support"]
    elif page_type == "content" and "anchor" in must_have_roles and len(cards) > 1 and "support" not in must_have_roles:
        must_have_roles.append("support")

    required_payloads: list[str] = []
    if any(card_type in {"data", "data_highlight"} for card_type in card_types) or page_text_strategy == "metric-led":
        required_payloads.append("metric")
    if any(card_type == "comparison" for card_type in card_types) or any(chart_type == "comparison_bar" for chart_type in chart_types) or page_text_strategy == "contrast-led":
        required_payloads.append("comparison_axis")
    if any(card_type in {"process", "timeline"} for card_type in card_types) or narrative_role == "process":
        required_payloads.append("method_step")
    if any(card_type in {"diagram", "matrix_chart"} for card_type in card_types) or narrative_role == "framework":
        required_payloads.append("framework_element")
    if any(card_type in {"people", "quote"} for card_type in card_types) or narrative_role in {"case", "quote"}:
        required_payloads.append("case_fact")
    if cards and "evidence_point" not in required_payloads and page_type == "content":
        required_payloads.append("evidence_point")
    if not required_payloads and page_type != "content":
        required_payloads.append("headline_signal")

    content_floor = {
        "launch": "至少让主命题、主锚点和最必要的支撑信息同时成立，不能只剩气氛。",
        "business": "至少让判断、依据和行动含义三者同时可见。",
        "report": "至少让关键指标/比较轴和管理判读同时可见，不能只剩标题态度。",
        "academic": "至少让定义、证据和结论边界同时可见。",
        "technical": "至少让机制/结构或步骤与关键约束同时可见。",
        "training": "至少让步骤、要点和执行提示同时可见。",
    }[scene_mode]
    decorative_ceiling = {
        "launch": "允许有较强舞台气氛，但装饰不能盖过主锚点和必要支撑信息。",
        "business": "装饰只能辅助层次，不得抢走判断与依据。",
        "report": "装饰必须退后，不能压过指标、比较和管理结论。",
        "academic": "装饰应极克制，不能影响论证阅读。",
        "technical": "装饰只服务结构理解，不能制造额外噪声。",
        "training": "装饰只做导航与分层，不能削弱可执行信息。",
    }[scene_mode]

    return {
        "scene_mode": scene_mode,
        "information_pressure": information_pressure,
        "minimum_card_count": minimum_card_count,
        "must_have_roles": must_have_roles,
        "required_payloads": required_payloads,
        "content_floor": content_floor,
        "decorative_ceiling": decorative_ceiling,
        "underfill_rule": "如果页面偏空，优先补证据、比较、步骤或结构信息，不要补气氛装饰。",
        "overflow_strategy": "如果页面偏满，先压缩修辞和辅助说明，再保住 anchor 与关键 support 的信息完整性。",
        "derived_from": "page_contract_fallback",
    }


def build_density_contract_brief(page: dict[str, Any], *, compact: bool = False) -> str:
    contract = effective_density_contract(page)
    if not contract:
        return "density_contract: N/A"
    if compact:
        return (
            "density_contract: "
            f"{contract.get('scene_mode', 'N/A')} / "
            f"{contract.get('information_pressure', 'N/A')} / "
            f"min_cards={contract.get('minimum_card_count', 'N/A')} / "
            f"payloads={' | '.join(as_list(contract.get('required_payloads'))) or 'N/A'} / "
            f"derived_from={contract.get('derived_from', 'planning')}"
        )
    must_have_roles = " | ".join(item for item in as_list(contract.get("must_have_roles")) if isinstance(item, str)) or "N/A"
    required_payloads = " | ".join(item for item in as_list(contract.get("required_payloads")) if isinstance(item, str)) or "N/A"
    return "\n".join(
        [
            "[DENSITY_CONTRACT]",
            f"scene_mode: {contract.get('scene_mode', 'N/A')}",
            f"information_pressure: {contract.get('information_pressure', 'N/A')}",
            f"minimum_card_count: {contract.get('minimum_card_count', 'N/A')}",
            f"must_have_roles: {must_have_roles}",
            f"required_payloads: {required_payloads}",
            f"content_floor: {contract.get('content_floor', 'N/A')}",
            f"decorative_ceiling: {contract.get('decorative_ceiling', 'N/A')}",
            f"underfill_rule: {contract.get('underfill_rule', 'N/A')}",
            f"overflow_strategy: {contract.get('overflow_strategy', 'N/A')}",
            f"derived_from: {contract.get('derived_from', 'planning')}",
        ]
    ).strip()


def build_render_density_plan(page: dict[str, Any], *, compact: bool = False) -> str:
    contract = effective_density_contract(page)
    cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
    card_roles = [str(card.get("role") or "") for card in cards]
    card_types = [str(card.get("card_type") or "") for card in cards]
    scene_mode = str(contract.get("scene_mode") or "business")
    information_pressure = str(contract.get("information_pressure") or "medium")
    proof_type = str(page.get("proof_type") or "")
    narrative_role = str(page.get("narrative_role") or "")
    negative_space = page.get("negative_space_target")
    negative_space = float(negative_space) if isinstance(negative_space, (int, float)) else 0.28
    minimum_card_count = int(contract.get("minimum_card_count") or max(1, len(cards) or 1))
    meaningful_card_count = min(max(1, minimum_card_count), max(1, len(cards) or minimum_card_count))
    page_type = str(page.get("page_type") or "content")

    if scene_mode in DENSE_SCENE_MODES or information_pressure == "high":
        space_mode = "content-first"
    elif page_type in {"cover", "section"} or negative_space >= 0.34:
        space_mode = "heroic"
    else:
        space_mode = "balanced"

    decoration_budget = infer_decoration_budget(
        page_type, card_types, scene_mode, information_pressure, negative_space,
    )

    occupancy_floor = max(0.36, round(1 - min(0.46, negative_space + 0.06), 2))
    anchor_role = "anchor" if "anchor" in card_roles else "primary"
    required_payloads = " | ".join(item for item in as_list(contract.get("required_payloads")) if isinstance(item, str)) or "N/A"
    support_required = "support" in as_list(contract.get("must_have_roles"))
    payload_heavy = any(card_type in PAYLOAD_HEAVY_CARD_TYPES for card_type in card_types)
    process_dense = (
        (proof_type == "process" or narrative_role == "process")
        and (scene_mode in DENSE_SCENE_MODES or information_pressure == "high")
    )
    comparison_dense = (
        (proof_type == "comparison" or narrative_role == "comparison" or page.get("page_text_strategy") == "contrast-led")
        and (scene_mode in DENSE_SCENE_MODES or information_pressure == "high")
    )
    framework_dense = (
        (proof_type == "framework" or narrative_role == "framework")
        and (scene_mode in DENSE_SCENE_MODES or information_pressure == "high")
    )
    metric_report_dense = (
        scene_mode == "report"
        and (
            page.get("page_text_strategy") == "metric-led"
            or any(card_type in {"data", "data_highlight"} for card_type in card_types)
        )
    )
    sparse_layout_ban = (
        "No hero-only whitespace solution; support cards must stay visibly readable."
        if scene_mode in DENSE_SCENE_MODES or information_pressure == "high"
        else "Do not let decoration replace the named support cards."
    )
    support_visibility_rule = (
        "Support cards must remain legible at first glance and carry explicit facts/steps/comparisons."
        if support_required or payload_heavy
        else "If support cards exist, they must read as information, not ornament."
    )
    if framework_dense:
        support_visibility_rule = (
            "Support cards must stay compact but payload-dense; use grouped risk/boundary/governance blocks instead of decorative bullets."
        )
    elif process_dense:
        support_visibility_rule = (
            "Support cards must carry executable step payloads such as checkpoints, warnings, dependencies, or fallback actions; do not let them collapse into decorative step captions."
        )
    elif comparison_dense:
        support_visibility_rule = (
            "Support cards must expose comparison axes, deltas, verdict rationale, or consequence blocks; do not let them degrade into decorative summaries."
        )
    elif metric_report_dense:
        support_visibility_rule = (
            "Support cards must expose deltas, trend direction, management readout, or action implication; do not let report/data pages degrade into small KPI islands floating in whitespace."
        )

    if compact:
        return (
            "render_density: "
            f"{space_mode} / meaningful_cards>={meaningful_card_count} / "
            f"occupancy_floor~={occupancy_floor} / decoration={decoration_budget} / "
            f"payloads={required_payloads}"
        )

    lines = [
            "[RENDER_DENSITY_PLAN]",
            f"space_mode: {space_mode}",
            f"scene_mode: {scene_mode}",
            f"information_pressure: {information_pressure}",
            f"minimum_meaningful_cards: {meaningful_card_count}",
            f"content_occupancy_floor: {occupancy_floor}",
            f"decoration_budget: {decoration_budget}",
            f"anchor_visibility_rule: let the {anchor_role} card claim the first read without hiding support payloads",
            f"support_visibility_rule: {support_visibility_rule}",
            (
                "surface_fill_rule: on dense scenes, prefer filled cards, denser surface coverage, tighter gutters, and explicit board/rail/strip shapes over transparent cards floating on atmosphere"
                if scene_mode in DENSE_SCENE_MODES or information_pressure == "high"
                else "surface_fill_rule: let surfaces breathe, but avoid invisible card boundaries"
            ),
            f"required_payloads: {required_payloads}",
            f"sparse_layout_ban: {sparse_layout_ban}",
            f"underfill_action: {contract.get('underfill_rule', '先补内容 payload，再补气氛。')}",
            (
                "framework_density_rule: keep support cards compact and grouped; if space gets tight, compress support wording before weakening the anchor structure"
                if framework_dense
                else None
            ),
            (
                "matrix_density_rule: matrix/framework anchors must expose labeled axes plus per-cell trigger snippets; dense support cards should carry minutes / owners / fallback / observation payloads, not generic summaries"
                if framework_dense and any(card_type == "matrix_chart" for card_type in card_types)
                else None
            ),
            (
                "dense_training_fill_rule: use a real training board with visible rails/strips/checkpoint blocks; avoid transparent bottom notes or airy poster spacing"
                if scene_mode == "training" and (framework_dense or process_dense or comparison_dense)
                else None
            ),
            (
                "process_density_rule: keep step flow explicit and support cards execution-bearing; if space gets tight, compress prose before removing checkpoints, warnings, or fallback actions"
                if process_dense
                else None
            ),
            (
                "comparison_density_rule: keep the comparison axis explicit and support cards evidence-bearing; if space gets tight, compress commentary before removing deltas or consequence blocks"
                if comparison_dense
                else None
            ),
            (
                "metric_density_rule: on metric-led report pages, make numbers, deltas, trend cues, and management interpretation visibly carry the page; if space gets tight, compress ornament before shrinking the metric board"
                if metric_report_dense
                else None
            ),
        ]
    return "\n".join(line for line in lines if line).strip()


def build_scene_execution_brief(page: dict[str, Any], *, compact: bool = False) -> str:
    contract = effective_density_contract(page)
    scene_mode = str(contract.get("scene_mode") or "business")
    information_pressure = str(contract.get("information_pressure") or "medium")
    proof_type = str(page.get("proof_type") or "")
    narrative_role = str(page.get("narrative_role") or "")
    page_text_strategy = str(page.get("page_text_strategy") or "")

    scene_defaults = {
        "launch": {
            "solving_mode": "hero-stage",
            "primary_job": "use one dominant anchor to establish mood and thesis quickly",
            "support_job": "support cards stay sparse and ceremonial",
            "anti_pattern": "do not turn the page into a dense dashboard or a generic web hero",
        },
        "business": {
            "solving_mode": "decision-board",
            "primary_job": "show the judgment first, then the reason, then the action implication",
            "support_job": "support cards explain basis or next step without competing with the decision",
            "anti_pattern": "do not let atmosphere outrun the business judgment",
        },
        "report": {
            "solving_mode": "evidence-board",
            "primary_job": "make the key metric/comparison readable before decoration",
            "support_job": "support cards must hold numbers, labels, differences, or management interpretation",
            "anti_pattern": "do not use poster whitespace or launch-style hero composition to hide thin evidence",
        },
        "academic": {
            "solving_mode": "argument-board",
            "primary_job": "make claim, evidence, and conclusion boundary readable in one scan",
            "support_job": "support cards should carry definition, method, caveat, or evidence slices",
            "anti_pattern": "do not replace argument structure with atmosphere or ornamental shapes",
        },
        "technical": {
            "solving_mode": "system-board",
            "primary_job": "make mechanism, steps, or structure understandable without narration",
            "support_job": "support cards should carry sequence, constraints, interfaces, or component roles",
            "anti_pattern": "do not hide process logic behind product-marketing visuals",
        },
        "training": {
            "solving_mode": "teaching-board",
            "primary_job": "make the step path and operator cues immediately executable",
            "support_job": "support cards should carry checklist items, warnings, or execution tips",
            "anti_pattern": "do not make the page look inspirational when it needs to teach execution",
        },
    }
    payload = scene_defaults.get(scene_mode, scene_defaults["business"]).copy()

    metric_report_dense = scene_mode == "report" and page_text_strategy == "metric-led"

    if proof_type == "comparison" or narrative_role == "comparison" or page_text_strategy == "contrast-led":
        payload["composition_hint"] = "show the comparison axis explicitly; opposing blocks or aligned rows are better than floating decoration"
        payload["comparison_execution_rule"] = (
            "anchor should make the verdict and comparison axis explicit; support cards should carry deltas, dimensions, consequence, caveat, or metric evidence"
        )
        payload["support_shape_rule"] = (
            "prefer aligned rows, compact contrast blocks, metric strips, or paired evidence groups over generic bullets"
        )
    elif proof_type == "process" or narrative_role == "process":
        payload["composition_hint"] = "show clear directional step flow; sequence must be visible without reading long paragraphs"
        payload["process_execution_rule"] = (
            "anchor should expose the main step path or operator sequence; support cards should carry checkpoints, warnings, dependencies, handoff conditions, or fallback actions"
        )
        payload["support_shape_rule"] = (
            "prefer timelines, numbered step boards, checkpoint strips, or grouped execution blocks over decorative arrows and generic bullets"
        )
    elif proof_type == "framework" or narrative_role == "framework":
        payload["composition_hint"] = "show labeled structure and boundaries; readers should understand the taxonomy at a glance"
        payload["framework_execution_rule"] = (
            "anchor should expose named structure elements plus role/boundary snippets; support cards should carry risk, boundary, governance, rollback, or implementation payloads"
        )
        payload["support_shape_rule"] = (
            "prefer compact payload boards, grouped short blocks, or 2x2 support structures over long prose lists"
        )
        if any(str(card.get("card_type") or "") == "matrix_chart" for card in as_list(page.get("cards")) if isinstance(card, dict)):
            payload["framework_execution_rule"] = (
                "matrix anchor should expose named axes plus per-cell trigger snippets; support cards should carry minute-level actions, owners, fallback, or observation payloads on the same page"
            )
            payload["support_shape_rule"] = (
                "prefer matrix board + compact action rail + fallback/observation strip over sparse poster composition or decorative bullets"
            )
    elif proof_type in {"case", "quote"} or narrative_role in {"case", "quote"}:
        payload["composition_hint"] = "show the case fact or quoted judgment as anchor, then decode why it matters"
    elif page_text_strategy == "metric-led":
        payload["composition_hint"] = "make numbers and labels do the heavy lifting; decorative forms should only support grouping"
    else:
        payload["composition_hint"] = "solve the page through explicit hierarchy and readable card grouping, not abstract scenery"

    if metric_report_dense:
        payload["metric_execution_rule"] = (
            "anchor should expose the primary metric board or chart with explicit labels/deltas; support cards should carry trend, variance reason, management readout, or next-step implication"
        )
        payload["support_shape_rule"] = (
            "prefer metric boards, delta strips, compact trend rows, or chart-plus-readout groupings over isolated numbers floating in whitespace"
        )

    if scene_mode in DENSE_SCENE_MODES or information_pressure == "high":
        payload["density_bias"] = "prefer structured multi-card readability over dramatic emptiness"
        payload["completion_rule"] = "dense scenes are only complete when support cards visibly carry the page payload instead of acting as ornamental scaffolding"
        payload["launch_drift_guard"] = "do not default to keynote hero, product-poster framing, or slogan-first composition"
        payload["surface_fill_bias"] = "prefer board-like surface coverage, visible card boundaries, and tighter gaps over transparent atmosphere-heavy staging"
    else:
        payload["density_bias"] = "balance force and breathing room, but keep support cards meaningful"
        payload["completion_rule"] = "keep support cards meaningful even when the page breathes"
        payload["launch_drift_guard"] = "N/A"
        payload["surface_fill_bias"] = "N/A"

    if compact:
        return (
            "scene_execution: "
            f"{payload['solving_mode']} / "
            f"{payload['density_bias']} / "
            f"{payload['composition_hint']}"
        )

    lines = [
            "[SCENE_EXECUTION_BRIEF]",
            f"scene_mode: {scene_mode}",
            f"information_pressure: {information_pressure}",
            f"solving_mode: {payload['solving_mode']}",
            f"primary_job: {payload['primary_job']}",
            f"support_job: {payload['support_job']}",
            f"composition_hint: {payload['composition_hint']}",
            f"density_bias: {payload['density_bias']}",
            f"surface_fill_bias: {payload['surface_fill_bias']}",
            f"completion_rule: {payload['completion_rule']}",
            f"anti_pattern: {payload['anti_pattern']}",
            f"launch_drift_guard: {payload['launch_drift_guard']}",
            (
                f"process_execution_rule: {payload['process_execution_rule']}"
                if payload.get("process_execution_rule")
                else None
            ),
            (
                f"comparison_execution_rule: {payload['comparison_execution_rule']}"
                if payload.get("comparison_execution_rule")
                else None
            ),
            (
                f"metric_execution_rule: {payload['metric_execution_rule']}"
                if payload.get("metric_execution_rule")
                else None
            ),
            (
                f"framework_execution_rule: {payload['framework_execution_rule']}"
                if payload.get("framework_execution_rule")
                else None
            ),
            (
                f"support_shape_rule: {payload['support_shape_rule']}"
                if payload.get("support_shape_rule")
                else None
            ),
        ]
    return "\n".join(line for line in lines if line).strip()


def build_card_execution_contract(page: dict[str, Any], *, compact: bool = False) -> str:
    cards = [card for card in as_list(page.get("cards")) if isinstance(card, dict)]
    if not cards:
        return "[CARD_EXECUTION_CONTRACT]\n- N/A"

    lines = ["[CARD_EXECUTION_CONTRACT]"]
    for card in cards:
        budget = card.get("content_budget") if isinstance(card.get("content_budget"), dict) else {}
        body = [item for item in as_list(card.get("body")) if isinstance(item, str)]
        micro_detail_plan = [item for item in as_list(card.get("micro_detail_plan")) if isinstance(item, str)]
        card_type = str(card.get("card_type") or "unknown")
        role = str(card.get("role") or "unknown")
        visible_body_floor = min(len(body), max(1, int(budget.get("max_body_lines") or len(body) or 1)))
        if card_type in {"matrix_chart", "comparison", "process"}:
            visible_body_floor = max(visible_body_floor, min(3, len(body) or 1))
        if compact:
            body_shape = " || ".join(compact_text(item, 64) for item in body) if body else "N/A"
            micro_summary = " || ".join(compact_text(item, 56) for item in micro_detail_plan) if micro_detail_plan else "N/A"
            lines.extend(
                [
                    (
                        f"- {card.get('card_id', 'unknown')} | role={role} | type={card_type} | "
                        f"floor={visible_body_floor} | headline={compact_text(card.get('headline'), 56)}"
                    ),
                    f"  focus: {compact_text(card.get('content_focus'), 88)}",
                    f"  body_shape: {body_shape}",
                    f"  micro_detail_plan: {micro_summary}",
                ]
            )
            continue
        lines.extend(
            [
                f"- {card.get('card_id', 'unknown')} | role={role} | type={card_type}",
                f"  headline: {card.get('headline', 'N/A')}",
                f"  focus: {card.get('content_focus', 'N/A')}",
                f"  visible_body_floor: {visible_body_floor} planned lines should remain perceptible",
                f"  body_shape: {' | '.join(body) if body else 'N/A'}",
                f"  micro_detail_plan: {' | '.join(micro_detail_plan) if micro_detail_plan else 'N/A'}",
            ]
        )
    return "\n".join(lines).strip()
