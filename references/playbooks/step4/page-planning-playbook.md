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

| 数据类型 | 推荐 layout_hint | 推荐 card_type / chart_type |
|---------|-----------------|---------------------------|
| 单一核心数字 | hero / split-left | kpi、metric-row |
| 多项比较 | bento-grid / columns | comparison、comparison-bar |
| 时间线 | timeline-flow | timeline |
| 步骤流程 | steps-horizontal / steps-vertical | process |
| 排行/列表 | list-ranked | data_highlight、list |
| 图文并茂 | split-left / split-right | image + text |
| 大段文字 | centered-statement | quote |
| 数据图表 | chart-focus | bar、line、pie、ring |
| 多卡片并列 | bento-grid | feature-card、info-card |

**填写 `resources` 字段时必须说明为什么选择该组件**（`resource_rationale` 字段）。

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
  "block_refs": ["kpi"],
  "chart_refs": []
}
```

填写后，`resource_loader.py resolve` 会自动把对应原则文件的完整正文注入 HTML 阶段的上下文。

---

## Phase 3：图片策略决策（必须明确，不得含糊）

| 模式 | 适用场景 | 必填字段 |
|------|---------|---------|
| `generate` | 封面页、章节页、需要强视觉冲击的核心页 | `image.needed=true`、`usage`、`placement`、`content_description`、`source_hint`（目标落盘路径）、`image.prompt`（英文图生图提示词） |
| `provided` | 用户已提供图片/品牌图库/截图 | `image.needed=true`、`source_hint`（真实本地路径）|
| `manual_slot` | 用户后续自己补图，先占位 | `image.needed=false`、`handoff_to_design` 说明槽位位置、比例、替换建议 |
| `decorate` | 数据页、逻辑页、纯排版页 | `image.needed=false`、`handoff_to_design` 说明用什么内部视觉语言（SVG/渐变/色块/水印/字体装饰）|

**禁止留模棱两可的 mode。选定后不得在 HTML 阶段临时改变。**

---

## Phase 4：layout 多样性约束

相邻页面（N-1 和 N+1）**禁止使用相同的 `layout_hint`**。整套 deck 中：
- bento-grid 最多占 40%
- 同一 layout 不得连续出现超过 2 次
- 若上一页是文字为主，本页优先考虑数据/图片为主的布局

---

## Phase 5：cards 字段填充规范

每张卡片必须包含：
- `type`：组件类型
- `title`：标题（精炼，不超过 12 字）
- `body`：正文内容（具体数据/事实/论点，不得空着）
- `data`：如有数值则填结构化数据
- `visual_weight`：primary / secondary / accent（决定视觉层级）
- `image`：完整的图片合同对象

**不得出现空 `body` 的卡片。**

---

## Phase 6：handoff_to_design 不可推翻项

填写 `handoff_to_design.non_negotiables`，列出 HTML 阶段不得改变的设计决策：
- 布局区域划分（标题区/内容区/装饰区的比例）
- 焦点区位置（`focus_zone` 坐标）
- 图片放置方式（左置/右置/背景/点缀）
- 禁止使用的视觉元素（来自 style.json 的 `decoration_dna.forbidden`）

---

## Phase 7：自审（强制）

运行 `planning_validator.py`，直到零 ERROR：

```bash
python3 SKILL_DIR/scripts/planning_validator.py $(dirname PLANNING_OUTPUT) --refs REFS_DIR --page PAGE_NUM
```

- ERROR 必须全部修复才能 FINALIZE
- WARNING 建议修复，不强制
- 自审通过后立即发送 FINALIZE，然后等待 HTML 阶段指令
