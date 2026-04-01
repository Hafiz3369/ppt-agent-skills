# Page Planning Playbook -- 单页策划稿

## 目标

制定一张从布局、字体、配图策略到卡片组织的 1280x720 物理画幅精细蓝图。**本阶段只写 JSON，不写 HTML。**

---

## Phase 1：理解当前页定位

从 `outline.txt` 中找到第 N 页的定义，明确：
- `page_goal`：这一页的核心论点（一句话，不含"和"字）
- `narrative_role`：叙事角色（封面/章节/数据/案例/结尾等）
- `proof_type`：论证方式（数据驱动/案例/对比/框架/步骤）

---

## Phase 2：资源选择（菜单层消费）

运行 `resource_loader.py menu` 获取可用组件摘要后，结合本页 proof_type 和数据类型做选择：

| 数据类型 | 推荐 `layout_hint` | 推荐 `card_type` / `chart.chart_type` |
|---------|---------------------|--------------------------------------|
| 单一核心数字 | `hero-top` / `single-focus` | `data_highlight` + `kpi` / `metric_row` |
| 多项比较 | `symmetric` / `three-column` | `comparison` + `comparison_bar` |
| 时间线 | `l-shape` / `waterfall` | `timeline` + `timeline` |
| 步骤流程 | `l-shape` / `t-shape` / `waterfall` | `process` / `diagram` + `funnel` / `progress_bar`（有明确进度数据时） |
| 排行/列表 | `asymmetric` / `l-shape` | `list` / `data_highlight` |
| 图文并茂 | `primary-secondary` / `asymmetric` | `image_hero` / `text` / `data` |
| 大段文字 | `single-focus` / `asymmetric` | `quote` / `text` |
| 数据图表 | `primary-secondary` / `single-focus` | `data` + `sparkline` / `ring` / `radar` / `treemap` / `stacked_bar` / `waffle` |
| 多卡片并列 | `mixed-grid` / `three-column` | `text` / `data` / `list` |

**填写 `resources` 字段时必须说明为什么选择该组件**（`resource_rationale` 字段）。

### 命名合同（必须区分 schema 枚举 与 资源文件 stem）

- `layout_hint` / `page_type`：写 validator 认可的值。`layout_hint` 推荐使用真实文件 stem，如 `hero-top`、`mixed-grid`、`l-shape`。
- `card_type`：写 validator 认可的枚举，如 `data_highlight`、`image_hero`、`matrix_chart`。
- `chart.chart_type`：写 validator 认可的枚举，**使用下划线命名**，如 `metric_row`、`comparison_bar`、`stacked_bar`、`progress_bar`。
- `resources.*_refs` 与 `card.resource_ref.*`：推荐写 `references/` 中的真实文件 stem，如 `metric-row`、`comparison-bar`、`visual-hierarchy`；`resource_loader.py` 会自动做下划线/连字符归一化。
- `process` 是 schema 原生 `card_type`，但当前没有 `blocks/process.md`。若使用它，必须同时给出更强的 `layout_refs`、`principle_refs`、`director_command` 和必要的 `chart_refs` / `resource_ref`，不要假设会有专属 block 正文可加载。

### principle_refs 指导（重要：设计原则文件按场景选用）

`resources.principle_refs[]` 字段决定 HTML 阶段能否收到设计原则正文。按以下规则填写：

| 本页特征 | 应引用 |
|---------|--------|
| 数据图表主导页 | `data-visualization` |
| 多卡片排版，需要层次感 | `visual-hierarchy` |
| 封面/章节页，需要情绪校准 | `color-psychology` |
| 信息超密、担心认知负担 | `cognitive-load` |
| 叙事转折页（从问题到方案）| `narrative-arc` |
| 任何页面的排版构图优化 | `composition` |
| 不确定选哪个 | `design-principles-cheatsheet`（综合速查）|

在 planning JSON 中写法示例：
```json
"resources": {
  "principle_refs": ["visual-hierarchy", "composition"],
  "layout_refs": ["hero-top"],
  "block_refs": [],
  "chart_refs": ["kpi"]
}
```

填写后，`resource_loader.py resolve` 会自动把对应原则文件的完整正文注入 HTML 阶段的上下文。

---

## Phase 3：`planningN.json` 结构合同（强制）

你的输出必须是**可直接被 `planning_validator.py` 校验的 JSON**。推荐写成单页对象：

```json
{
  "page": {
    "slide_number": 3,
    "page_type": "content",
    "narrative_role": "evidence",
    "title": "页标题",
    "page_goal": "这一页只讲一个判断",
    "audience_takeaway": "观众带走什么",
    "visual_weight": 7,
    "layout_hint": "hero-top",
    "layout_variation_note": "与上一页至少两个维度不同",
    "focus_zone": "右上 1/3 作为视觉锚点",
    "negative_space_target": "medium",
    "page_text_strategy": "标题强、正文短、数据做锚点",
    "rhythm_action": "推进",
    "must_avoid": ["禁止平均分栏", "禁止所有卡片同一种 card_style"],
    "variation_guardrails": {
      "same_gene_as_deck": "保留统一字体、边角和 signature_move",
      "different_from_previous": ["重心从上移到右", "card_style 组合改为 accent+outline+transparent"]
    },
    "director_command": {
      "mood": "判断感强、结论先行",
      "spatial_strategy": "主锚占据第一视线，支撑内容围绕其展开",
      "anchor_treatment": "用尺度断层和对比色强化主锚",
      "techniques": ["T1", "W3"],
      "prose": "保持证据链清晰，避免装饰压过论点"
    },
    "decoration_hints": {
      "background": {"feel": "轻微渐变底", "restraint": "不抢文字对比", "techniques": ["T1"]},
      "floating": {"feel": "局部辅助装饰", "restraint": "只服务锚点动线", "techniques": ["W3"]},
      "page_accent": {"feel": "强调色集中在锚点附近", "restraint": "accent 只用 1-2 种", "techniques": ["T9"]}
    },
    "source_guidance": {
      "brief_sections": ["关键数据清单", "PPTX 结构化数据包 > metrics"],
      "citation_expectation": "有数字就保留来源",
      "strictness": "不得超出 brief 结论边界"
    },
    "resources": {
      "page_template": null,
      "layout_refs": ["hero-top"],
      "block_refs": [],
      "chart_refs": ["kpi", "metric-row"],
      "principle_refs": ["visual-hierarchy", "composition"],
      "resource_rationale": "用 hero-top 放大单一结论，再用 KPI 组件承托数据锚点"
    },
    "cards": [
      {
        "card_id": "s03-anchor",
        "role": "anchor",
        "card_type": "data_highlight",
        "card_style": "accent",
        "argument_role": "claim",
        "headline": "核心指标",
        "body": ["一句解释它为什么重要", "一句说明对业务的影响"],
        "data_points": [
          {"label": "同比增长", "value": "47.3", "unit": "%", "source": "search-brief metrics[2]"}
        ],
        "chart": {"chart_type": "kpi"},
        "content_budget": {"headline_max_chars": 12, "body_max_bullets": 2, "body_max_lines": 4},
        "image": {
          "mode": "decorate",
          "needed": false,
          "usage": null,
          "placement": null,
          "content_description": null,
          "source_hint": null,
          "decorate_brief": "用内联 SVG 和轻量几何装饰填满留白，不抢主锚"
        },
        "resource_ref": {"chart": "kpi", "principle": "visual-hierarchy"}
      },
      {
        "card_id": "s03-support-1",
        "role": "support",
        "card_type": "data",
        "card_style": "outline",
        "argument_role": "evidence",
        "headline": "增长原因",
        "body": ["增长主要来自高客单区域放量", "老客复购提升让同比增速更稳"],
        "data_points": [
          {"label": "高客单区域占比", "value": "31", "unit": "%", "source": "search-brief metrics[4]"}
        ],
        "chart": {"chart_type": "metric_row"},
        "content_budget": {"headline_max_chars": 12, "body_max_bullets": 2, "body_max_lines": 4},
        "image": {
          "mode": "decorate",
          "needed": false,
          "usage": null,
          "placement": null,
          "content_description": null,
          "source_hint": null,
          "decorate_brief": "用低对比度辅助线和轻微数据底纹承托信息"
        },
        "resource_ref": {"chart": "metric-row", "principle": "composition"}
      }
    ],
    "workflow_metadata": {
      "stage": "planning",
      "workflow_version": "2026.03.31-v4",
      "planning_schema_version": "4.0",
      "planning_packet_version": "4.0",
      "planning_continuity_version": "4.0"
    }
  }
}
```

### 必填字段与枚举底线

- 顶层页字段至少要有：`slide_number`、`page_type`、`title`、`page_goal`、`cards`、`visual_weight`、`director_command`、`decoration_hints`、`resources`、`workflow_metadata`。
- `page_type`：`cover` / `toc` / `section` / `content` / `end`
- `narrative_role` 推荐使用：`opening` / `orientation` / `transition` / `setup` / `evidence` / `comparison` / `framework` / `process` / `case` / `quote` / `breath` / `close` / `cta`
- 内容页必须有 `layout_hint`，并从 validator 认可的集合中选，如 `single-focus`、`symmetric`、`asymmetric`、`three-column`、`primary-secondary`、`hero-top`、`mixed-grid`、`l-shape`、`t-shape`、`waterfall`
- `cards[].role`：`anchor` / `support` / `context`
- `cards[].card_style`：`accent` / `elevated` / `filled` / `outline` / `glass` / `transparent`
- `cards[].body` 必须是**字符串数组**，不要写成单个字符串
- `cards[].data_points` 必须是对象数组；有数字时尽量带 `source`
- `cards[].content_budget` 必须是对象；哪怕是最小对象也要显式写出
- `cards[].image.needed = true` 时，`usage` / `placement` / `content_description` / `source_hint` 都必须填写；否则这些字段应为 `null`

---

## Phase 4：图片策略决策（必须明确，不得含糊）

| 模式 | 适用场景 | 必填字段 |
|------|---------|---------|
| `generate` | 封面页、章节页、需要强视觉冲击的核心页 | `image.needed=true`、`usage`、`placement`、`content_description`、`source_hint`（目标落盘路径）、`image.prompt`（英文图生图提示词） |
| `provided` | 用户已提供图片/品牌图库/截图 | `image.needed=true`、`source_hint`（真实本地路径）|
| `manual_slot` | 用户后续自己补图，先占位 | `image.needed=false`、`image.slot_note` 说明槽位位置、比例、替换建议 |
| `decorate` | 数据页、逻辑页、纯排版页 | `image.needed=false`、`image.decorate_brief` 说明内部视觉语言（SVG/渐变/色块/水印/字体装饰）|

**禁止留模棱两可的 mode。选定后不得在 HTML 阶段临时改变。**

---

## Phase 5：layout 多样性约束

相邻页面（N-1 和 N+1）**禁止使用相同的 `layout_hint`**。整套 deck 中：
- `mixed-grid` 最多占 40%
- 同一 layout 不得连续出现超过 2 次
- 若上一页是文字为主，本页优先考虑数据/图片为主的布局

---

## Phase 6：cards 字段填充规范

每张卡片必须包含：
- `card_id`：稳定唯一，建议 `s{页码}-{anchor|support|context}-{序号}`
- `role`：`anchor` / `support` / `context`
- `card_type`：validator 枚举值，如 `text` / `data` / `list` / `process` / `data_highlight` / `timeline` / `diagram` / `quote` / `comparison` / `people` / `image_hero` / `matrix_chart`
- `card_style`：6 种合法视觉变体之一
- `headline`：标题（精炼，不超过 12 字）
- `body`：正文字符串数组，不能为空
- `data_points`：如有数值则填对象数组
- `content_budget`：内容预算对象
- `image`：完整图片合同对象，带 `mode`
- `resource_ref`：需要定向绑定某个 block/chart/principle 时写这里
- `image.slot_note` / `image.decorate_brief` / `image.prompt`：按图片模式按需补充

可选但推荐：
- `argument_role`
- `chart`

**不得出现空 `body` 的卡片。**

---

## Phase 7：不可推翻项要落在哪些字段

不要再单独造一套 `handoff_to_design` 私有协议。把“不能被 HTML 阶段推翻”的信息落进下面这些**已有合同字段**：

- `focus_zone`：锁定主锚位置
- `must_avoid`：明确禁止的模板化风险
- `director_command`：给出结构、锚点、技法方向
- `decoration_hints`：约束装饰强度与层次
- `source_guidance`：约束证据边界与引用期望
- `resources` / `resource_ref`：锁定必须消费的资源正文

---

## Phase 8：自审（强制）

运行 `planning_validator.py`，直到零 ERROR：

```bash
python3 SKILL_DIR/scripts/planning_validator.py $(dirname PLANNING_OUTPUT) --refs REFS_DIR --page PAGE_NUM
```

- ERROR 必须全部修复才能 FINALIZE
- WARNING 建议修复，不强制
- 自审通过后立即发送 FINALIZE，然后等待 HTML 阶段指令
