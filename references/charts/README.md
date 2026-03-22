# 数据可视化图表模板

> 设计 data 类型卡片时，根据数据特征选择合适的可视化类型，然后读取对应的模板文件。
>
> **使用时机**：每个 data 卡片至少配一个可视化元素。不要只放一个大数字。

## 选择指南

| 数据类型 | 推荐图表 | 文件 | chart_type |
|---------|---------|------|-----------|
| 百分比/完成度 | 进度条 | `progress-bar.md` | progress_bar |
| 百分比/完成度 | 环形百分比 | `ring.md` | ring |
| 两项对比 | 对比柱 | `comparison-bar.md` | comparison_bar |
| 时间趋势 | 迷你折线图 | `sparkline.md` | sparkline |
| 比例直觉化 | 点阵图 | `waffle.md` | waffle |
| 核心 KPI | KPI 指标卡 | `kpi.md` | kpi |
| 多指标并排 | 指标行 | `metric-row.md` | -- (辅助) |
| 评级/评分 | 评分指示器 | `rating.md` | rating |
| 多维度对比 | 雷达图 | `radar.md` | radar |
| 多分类占比 | 堆叠条形图 | `stacked-bar.md` | stacked_bar |
| 层级占比 | 矩形树图 | `treemap.md` | treemap |
| 历史/里程碑 | 时间轴 | `timeline.md` | timeline |
| 转化流程 | 漏斗图 | `funnel.md` | funnel |
