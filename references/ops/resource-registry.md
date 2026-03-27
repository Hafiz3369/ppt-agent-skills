# 资源注册表（唯一权威映射源）

> **维护规则**：新增/删除/重命名任何资源文件时，只需修改本文件。所有上游文件通过引用本文件获取映射，不再内联重复。
>
> **资源哲学**：所有资源文件提供的是**设计灵魂和思路框架**，而非可复制粘贴的 HTML/CSS 代码。LLM 读取后应获得"设计方向感"而非"固定模板"。

---

## 1. 风格（styles/）

| style_id | 中文名 | 文件路径 |
|----------|-------|---------|
| `blue_white` | 蓝白商务 | `styles/blue-white.md` |
| `minimal_gray` | 极简灰白 | `styles/minimal-gray.md` |
| `warm_earth` | 暖色大地 | `styles/warm-earth.md` |
| `fresh_green` | 清新自然 | `styles/fresh-green.md` |
| `royal_red` | 朱红宫墙 | `styles/royal-red.md` |
| `dark_tech` | 暗黑科技 | `styles/dark-tech.md` |
| `luxury_purple` | 紫金奢华 | `styles/luxury-purple.md` |
| `vibrant_rainbow` | 活力彩虹 | `styles/vibrant-rainbow.md` |

**主链决策规则**：`styles/runtime-style-rules.md`（风格字段合同 + 失败模式 + 创新自由区）

**非默认创意工作簿**：`styles/README.md`（仅供人工调试 / 灵感探索，不进入默认 runtime）

---

## 2. 布局（layouts/）

| layout_hint 值 | 中文名 | 文件路径 | 卡片数 |
|---------------|-------|---------|-------|
| 单一焦点 | 单一焦点 | `layouts/single-focus.md` | 1 |
| 50/50 对称 | 对称两栏 | `layouts/symmetric.md` | 2 |
| 非对称两栏 | 非对称两栏 | `layouts/asymmetric.md` | 2 |
| 三栏等宽 | 三栏等宽 | `layouts/three-column.md` | 3 |
| 主次结合 | 主次结合 | `layouts/primary-secondary.md` | 3 |
| 英雄式 / 顶部英雄式 | 英雄式 | `layouts/hero-top.md` | 4-5 |
| 混合网格 | 混合网格 | `layouts/mixed-grid.md` | 4-6 |
| L 型 | L 型布局 | `layouts/l-shape.md` | 4 |
| T 型 | T 型布局 | `layouts/t-shape.md` | 4 |
| 瀑布流 | 瀑布流 | `layouts/waterfall.md` | 4-6 |

**决策矩阵**：`layouts/README.md`（内容特征 -> 推荐布局）

---

## 3. 图表（charts/）

| chart_type 值 | 中文名 | 文件路径 | 适用数据类型 |
|--------------|-------|---------|------------|
| `progress_bar` | 进度条 | `charts/progress-bar.md` | 百分比/完成度 |
| `ring` | 环形百分比 | `charts/ring.md` | 百分比/完成度 |
| `comparison_bar` | 对比柱 | `charts/comparison-bar.md` | 两项对比 |
| `sparkline` | 迷你折线图 | `charts/sparkline.md` | 时间趋势 |
| `waffle` | 点阵图 | `charts/waffle.md` | 比例直觉化 |
| `kpi` | KPI 指标卡 | `charts/kpi.md` | 核心 KPI |
| `metric_row` | 指标行 | `charts/metric-row.md` | 多指标并排 |
| `rating` | 评分指示器 | `charts/rating.md` | 评级/评分 |
| `radar` | 雷达图 | `charts/radar.md` | 多维度能力 |
| `stacked_bar` | 堆叠条形图 | `charts/stacked-bar.md` | 多分类占比 |
| `treemap` | 矩形树图 | `charts/treemap.md` | 层级面积 |
| `timeline` | 时间轴 | `charts/timeline.md` | 历史沿革/里程碑 |
| `funnel` | 漏斗图 | `charts/funnel.md` | 转化漏斗 |

> chart_type 值用下划线，文件名用连字符。

**主链选择规则**：`charts/runtime-chart-rules.md`（图表选择矩阵 + 最低内容合同 + 失败模式）

**非默认创意工作簿**：`charts/README.md`（仅供人工调试 / 定向参考，不进入默认 runtime）

---

## 4. 页面结构规范（page-templates/）

| page_type 值 | 文件路径 | 说明 |
|-------------|---------|------|
| `cover` | `page-templates/cover.md` | 灵魂驱动设计指引（唯一必须：醒目标题，其余元素均为可选叙事工具） |
| `toc` | `page-templates/toc.md` | 灵魂驱动设计指引（唯一必须：Part 结构展示） |
| `section` | `page-templates/section.md` | 灵魂驱动设计指引（唯一必须：章节标题，连续章节封面必须变化构图） |
| `end` | `page-templates/end.md` | 灵魂驱动设计指引（唯一必须：核心结论，与封面形成收束镜像） |

---

## 5. Prompt 文件（prompts/）

| Step | 文件路径 | 用途 |
|------|---------|------|
| Step 1 | `prompts/prompt-1-research.md` | 需求调研（内容需求单，默认 8-10 题 + 0-2 动态追问 + requirements.json schema） |
| Step 3 | `prompts/prompt-2-outline.md` | 大纲架构师 v3.0（含叙事弧线 + 论证策略 + Part 间逻辑关系） |
| Step 4 | `prompts/prompt-3-planning.md` | 内容分配与策划稿（逐页生成） |
| Step 5c | `prompts/prompt-4-design-global.md` | HTML 设计全局合同（全局视觉规则 / 执行边界） |
| Step 5c | `prompts/prompt-4-design.md` | HTML 设计稿生成（逐页设计） |
| 可选 | `prompts/animations.md` | CSS 动画 |

---

## 6. 区域展示组件（blocks/）

| card_type 值 | 中文名 | 文件路径 | 推荐跨度 |
|-------------|-------|---------|---------|
| `timeline` | 时间线块 | `blocks/timeline.md` | 跨列 |
| `diagram` | 图解块 | `blocks/diagram.md` | 跨列或跨行 |
| `quote` | 引用/金句块 | `blocks/quote.md` | 跨列 |
| `comparison` | 对比块 | `blocks/comparison.md` | 跨列 |
| `people` | 人物组块 | `blocks/people.md` | 跨列 |
| `image_hero` | 大图+叠加文字块 | `blocks/image-hero.md` | 跨列或跨行 |
| `matrix_chart` | 象限矩阵块 | `blocks/matrix-chart.md` | 跨列跨行 |

**选择指南**：`blocks/README.md`（内容特征 -> 推荐 card_type）
**视觉变体**：`blocks/card-styles.md`（6 种 card_style 的空间存在感哲学 + 搭配规则）

---

## 7. 设计原则（principles/）

| 文件路径 | 原则领域 | 核心理论 |
|---------|---------|---------|
| **`principles/design-principles-cheatsheet.md`** | **6 大原则 -> JSON 字段操作手册 + 逐页 8 项体检单** | **Step 4 第 0 号必读项。通过 `{{DESIGN_PRINCIPLES_CHEATSHEET}}` 注入 prompt-3 上下文** |
| `principles/visual-hierarchy.md` | 视觉层级 | CRAP 四原则 / 视觉重量阶梯 |
| `principles/cognitive-load.md` | 认知负荷 | Miller's Law / 信噪比 / 一页一观点 |
| `principles/composition.md` | 构图与留白 | 格式塔原则 / 三分法 / 三层级留白 |
| `principles/color-psychology.md` | 色彩心理 | 60-30-10 / 色彩情感映射 / 对比度安全 |
| `principles/data-visualization.md` | 数据可视化 | Tufte 数据墨水比 / Few 仪表盘原则 |
| `principles/narrative-arc.md` | 叙事结构 | 金字塔原理 / SCQA / 注意力曲线 |

**总览**：`principles/README.md`（原则索引 + 操作手册定位 + 读取时机 + 与规则层的关系）

---

## 8. 共享运行资源

| 文件路径 | 何时读取 | 内容 |
|---------|---------|------|
| `runtime/narrative-rhythm.md` | Step 3 完成后（仅一次） | 叙事节奏原则 + 灵动节奏变奏指引（无固定页数模板） |
| `runtime/resource-menu.md` | Step 4 每页策划时（通过 `{{RESOURCE_MENU}}` 注入 prompt-3） | 资源菜单速查卡（布局/卡片/图表/card_style/装饰技法完整选项）。防止上下文衰减导致后半程策划退化 |
| `runtime/image-generation.md` | Step 5b（如需配图） | 配图 Prompt 公式 + 7 种融入技法（灵魂描述，非代码模板） |
| `design-runtime/design-specs.md` | Step 5c 首页前 | 全局视觉设计规则、风格底线与 HTML 表现要求 |
| `design-runtime/director-command-rules.md` | Step 4 写 `director_command` 时 | director_command 字段职责、写法边界、选择规则与 failure modes |
| `principles/runtime-failure-modes.md` | Step 4 / Step 5 默认读取 | planning 与 design 共用的主链 failure modes 与修复顺序 |
| `runtime/technique-cards.md` | Step 5c 按需 | T1-T10 技法牌完整定义（CSS 原子代码 + ADAPT 参数） |
| `design-runtime/css-weapons.md` | Step 5c 按需 | CSS 武器库；只有确需具体实现时才展开 |
| `playbooks/planning-subagent-playbook.md` | Step 4 sub-agent 准备前 | planning sub-agent 的合同分层、输入包设计、并行/串行规则 |
| `playbooks/html-subagent-playbook.md` | Step 5c sub-agent 准备前 | HTML sub-agent 的合同消费顺序、packet 关系、变奏规则 |
| `design-runtime/data-type-visual-mapping.md` | Step 2/4 数据格式化与策划 | 数据类型 -> card_type / layout_hint / CSS 实现参考 |
| `design-runtime/data-type-decoration-mapping.md` | Step 4 策划装饰时 | 数据类型 -> 推荐 T 技法 / W 武器 / 装饰密度档位（1:N 推荐，内容优先原则） |
| `ops/resource-registry.md` | 本文件，维护时查阅 | 全局资源映射唯一权威源 |

---

## 9. 阶段资源包（stage bundles）

> 这些 bundle 是给 harness 用的默认读取策略。新增默认 preload / global resource 时，优先改这里，而不是改脚本。

| bundle_id | 文件路径 | why | condition |
|----------|---------|-----|-----------|
| `planning_preload_core` | `principles/design-principles-cheatsheet.md` | 把设计原则翻译成 planning 字段操作规则 | always |
| `planning_preload_core` | `runtime/resource-menu.md` | 避免后半程退化成只会 text/data/list | always |
| `planning_preload_core` | `layouts/README.md` | 看布局选择面，不提前锁死 HTML | always |
| `planning_preload_core` | `blocks/README.md` | 看复合组件的使用边界 | always |
| `planning_preload_core` | `blocks/card-styles.md` | 控制 card_style 层次，不要平均切块 | always |
| `planning_preload_core` | `charts/runtime-chart-rules.md` | 让 data 卡片优先走可视化，并补齐图表最低内容合同 | always |
| `planning_preload_core` | `styles/runtime-style-rules.md` | 提供风格字段合同、变奏边界与失败模式 | always |
| `planning_preload_core` | `design-runtime/director-command-rules.md` | 约束 director_command 写法，防止 prose 代替结构 | always |
| `planning_preload_core` | `principles/runtime-failure-modes.md` | 提前暴露 underfill / support collapse / decorative substitution 等主链失败模式 | always |
| `planning_preload_core` | `design-runtime/data-type-decoration-mapping.md` | 为每种 card_type 提供推荐 T/W 组合和装饰密度档位，确保装饰选择有据可循 | always |
| `planning_preload_image` | `runtime/image-generation.md` | 在 planning 阶段写清图片语义合同，并为 Step 5b 的 prompt/path 派生提供规则 | image_preference_enabled |
| `design_global_resources` | `design-runtime/design-specs.md` | 提供 Step 5c 的全局视觉设计底线 | always |
| `design_global_resources` | `styles/runtime-style-rules.md` | 提供风格字段合同、创新自由区与执行边界 | always |
| `design_global_resources` | `layouts/README.md` | 提供布局骨架索引与使用总则 | always |
| `design_global_resources` | `blocks/README.md` | 提供复合组件选择指南 | always |
| `design_global_resources` | `charts/runtime-chart-rules.md` | 提供图表选择规则、信息角色与失败边界 | always |
| `design_global_resources` | `principles/README.md` | 提供设计原则总览，帮助 HTML 保持层级与节奏 | always |
| `design_global_resources` | `principles/design-principles-cheatsheet.md` | 6 大原则的字段级操作手册，帮助 HTML agent 自检视觉层级、认知负荷和装饰克制 | always |
| `design_global_resources` | `principles/runtime-failure-modes.md` | 统一内容未完成与视觉失真类 failure modes 的修复顺序 | always |

---

## 10. 非默认示例资源（human/debug only）

> 以下文档保留在仓库中，但不进入默认 bundle，不建议直接注入 runtime 子代理上下文。

| 文件路径 | 定位 | 规则 |
|---------|------|------|
| `styles/README.md` | human-only creative workbook | 仅供人工灵感探索 / 调试，不进入 planning/html 默认上下文 |
| `charts/README.md` | human-only chart workbook | 仅供人工定向参考，不进入 planning/html 默认上下文 |
| `design-runtime/director-command-examples.md` | human-only calibration library | 仅供人工校准与对照，不进入 planning runtime preload |

---

## 11. 资源路由策略（resource routing policies）

> 这层策略只负责兜底补齐明显缺失的 refs，不替代 planning 的主动选择。

| scope | field | value | resource_group | resource_ref | why |
|------|------|------|---------------|-------------|-----|
| `page` | `page_type` | `cover` | `page_template` | `cover` | 封面页至少要带封面模板语义 |
| `page` | `page_type` | `toc` | `page_template` | `toc` | 目录页至少要带目录模板语义 |
| `page` | `page_type` | `section` | `page_template` | `section` | 章节页至少要带章节模板语义 |
| `page` | `page_type` | `end` | `page_template` | `end` | 结尾页至少要带结尾模板语义 |
| `page` | `page_type` | `cover` | `principle_refs` | `visual-hierarchy` | 封面要优先建立强锚点 |
| `page` | `page_type` | `toc` | `principle_refs` | `narrative-arc` | 目录页要清晰表达叙事路线 |
| `page` | `page_type` | `section` | `principle_refs` | `composition` | 章节页需要更强构图变化 |
| `page` | `page_type` | `end` | `principle_refs` | `narrative-arc` | 结尾页要做收束与回响 |
| `page` | `layout_hint` | `single-focus` | `layout_refs` | `single-focus` | 布局真源应直达对应布局说明 |
| `page` | `layout_hint` | `symmetric` | `layout_refs` | `symmetric` | 布局真源应直达对应布局说明 |
| `page` | `layout_hint` | `asymmetric` | `layout_refs` | `asymmetric` | 布局真源应直达对应布局说明 |
| `page` | `layout_hint` | `three-column` | `layout_refs` | `three-column` | 布局真源应直达对应布局说明 |
| `page` | `layout_hint` | `primary-secondary` | `layout_refs` | `primary-secondary` | 布局真源应直达对应布局说明 |
| `page` | `layout_hint` | `hero-top` | `layout_refs` | `hero-top` | 布局真源应直达对应布局说明 |
| `page` | `layout_hint` | `mixed-grid` | `layout_refs` | `mixed-grid` | 布局真源应直达对应布局说明 |
| `page` | `layout_hint` | `l-shape` | `layout_refs` | `l-shape` | 布局真源应直达对应布局说明 |
| `page` | `layout_hint` | `t-shape` | `layout_refs` | `t-shape` | 布局真源应直达对应布局说明 |
| `page` | `layout_hint` | `waterfall` | `layout_refs` | `waterfall` | 布局真源应直达对应布局说明 |
| `card` | `card_type` | `comparison` | `block_refs` | `comparison` | 对比类卡片应有对应 block 参考 |
| `card` | `card_type` | `diagram` | `block_refs` | `diagram` | 图解类卡片应有对应 block 参考 |
| `card` | `card_type` | `quote` | `block_refs` | `quote` | 引言类卡片应有对应 block 参考 |
| `card` | `card_type` | `people` | `block_refs` | `people` | 人物类卡片应有对应 block 参考 |
| `card` | `card_type` | `image_hero` | `block_refs` | `image-hero` | 大图叠字类卡片应有对应 block 参考 |
| `card` | `card_type` | `matrix_chart` | `block_refs` | `matrix-chart` | 象限卡片应有对应 block 参考 |
| `card` | `card_type` | `timeline` | `block_refs` | `timeline` | 时间线卡片应有对应 block 参考 |
| `card` | `chart_type` | `progress_bar` | `chart_refs` | `progress-bar` | 图表类型应映射到对应 chart 参考 |
| `card` | `chart_type` | `comparison_bar` | `chart_refs` | `comparison-bar` | 图表类型应映射到对应 chart 参考 |
| `card` | `chart_type` | `metric_row` | `chart_refs` | `metric-row` | 图表类型应映射到对应 chart 参考 |
| `card` | `chart_type` | `stacked_bar` | `chart_refs` | `stacked-bar` | 图表类型应映射到对应 chart 参考 |
| `card` | `chart_type` | `progress_bar` | `principle_refs` | `data-visualization` | 数据图表页要带数据可视化原则 |
| `card` | `chart_type` | `comparison_bar` | `principle_refs` | `data-visualization` | 数据图表页要带数据可视化原则 |
| `card` | `chart_type` | `metric_row` | `principle_refs` | `data-visualization` | 数据图表页要带数据可视化原则 |
| `card` | `chart_type` | `stacked_bar` | `principle_refs` | `data-visualization` | 数据图表页要带数据可视化原则 |
