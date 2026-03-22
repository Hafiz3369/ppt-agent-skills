# 区域展示组件库

> 扩展 card_type 的复合组件。每个组件是 cards[] 中一个独立的卡片，可通过 grid-row/grid-column 跨行跨列。

## 组件总表

| card_type | 中文名 | 文件 | 推荐跨度 |
|----------|--------|------|---------|
| `timeline` | 时间线块 | `timeline.md` | 跨列（full-width） |
| `diagram` | 图解块 | `diagram.md` | 跨列或跨行 |
| `quote` | 引用/金句块 | `quote.md` | 跨列 |
| `comparison` | 对比块 | `comparison.md` | 跨列 |
| `people` | 人物组块 | `people.md` | 跨列 |
| `image_hero` | 大图+叠加文字块 | `image-hero.md` | 跨列或跨行 |
| `matrix_chart` | 象限矩阵块 | `matrix-chart.md` | 跨列跨行 |

## 与基础 card_type 的关系

基础类型（text/data/list/process/tag_cloud/data_highlight）在 prompt-4 中内联定义。
复合类型（上表 7 种）从本目录按需加载。两者在 cards[] 中平等共存，可自由组合。

## 选择指南

| 内容特征 | 推荐 card_type |
|---------|---------------|
| 需要展开论述 | text |
| 有具体数字要突出 | data / data_highlight |
| 多个并列要点 | list |
| 有先后顺序的步骤 | process |
| 关键词/技术栈展示 | tag_cloud |
| 时间顺序的事件序列（4-8个） | **timeline**（推荐跨列） |
| 架构/流程/金字塔/关系 | **diagram**（推荐跨列） |
| 权威引用/核心观点/金句 | **quote** |
| A vs B 对比 | **comparison**（推荐跨列） |
| 团队/人物介绍（3-8人） | **people**（推荐跨列） |
| 配图+叠加文字（情感冲击） | **image_hero**（推荐跨列/跨行） |
| 2x2象限/定位分析 | **matrix_chart**（推荐跨列跨行） |

## 自由组合原则

- 一页可以混合使用任意基础类型和复合类型
- 复合类型可以和基础类型在同一个 CSS Grid 布局中共存
- 复合类型推荐占据较大的 grid 区域（跨列/跨行），基础类型填充剩余空间
- 同一页不宜超过 1 个跨列跨行的复合组件（否则布局拥挤）
- 风格统一由 CSS 变量保证，组件只控制区域内的信息组织方式
