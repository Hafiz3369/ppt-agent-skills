# Step 4 资源菜单

> 这是页面策划阶段的速查卡，作用是防止长链路生成时“知道有资源，但忘了用”。

---

## 1. 布局候选

| `layout_hint` | 适合什么内容 | 最常见失误 |
|--------------|------------|-----------|
| `single-focus` | 单个论点 / 单个数据 / 金句 | 做成一个居中大卡片 |
| `symmetric` | 两个对等概念对比 | 左右完全一样重 |
| `asymmetric` | 主论点 + 注解 | 仍然平均分配注意力 |
| `three-column` | 三个并列维度 | 三栏等宽等高像产品说明书 |
| `primary-secondary` | 1 核心 + 2 支撑 | 三张卡片都想当主角 |
| `hero-top` | 总览 + 3-4 子展开 | 顶部 hero 太弱，像普通标题栏 |
| `mixed-grid` | 4-6 个异构信息 | 全部做成小方块九宫格 |
| `l-shape` | 主体 + 侧证 + 收束 | L 形不明显，退回普通网格 |
| `t-shape` | 顶部总览 + 下方深挖 | 上下都满，缺少呼吸 |
| `waterfall` | 多级重要性 / 递减节奏 | 仍然强行对齐成等高卡片 |

非 content 页：
- `free-cover`
- `toc-route`
- `free-section`
- `free-end`

---

## 2. card_type 速查

| `card_type` | 适用场景 | 推荐存在方式 |
|------------|---------|-------------|
| `text` | 解释、定义、结论 | `filled` / `outline` |
| `data` | 指标、趋势、分析 | `filled` / `accent` |
| `list` | 并列要点 | `filled` / `outline` |
| `process` | 步骤、流程 | `filled` / `transparent` |
| `tag_cloud` | 标签、关键词场 | `transparent` / `glass` |
| `data_highlight` | 超级 KPI | `transparent` / `accent` |
| `timeline` | 时间线 / 里程碑 | `transparent` |
| `diagram` | 架构 / 框架 | `transparent` |
| `quote` | 金句 / 引述 | `transparent` |
| `comparison` | 对比分析 | `outline` |
| `people` | 人物介绍 | `transparent` |
| `image_hero` | 大图叠字 | `transparent` / `glass` |
| `matrix_chart` | 象限矩阵 | `transparent` |

---

## 3. card_style 速查

| `card_style` | 空间存在感 | 使用提醒 |
|-------------|-----------|---------|
| `accent` | 燃烧的主角 | 每页最多 1 个 |
| `elevated` | 浮起的主角 | 每页最多 1 个 |
| `filled` | 稳定承载面 | 禁止全页都用 |
| `outline` | 辅助边界 | 适合次要信息 |
| `glass` | 氛围浮层 | 图像页更适合 |
| `transparent` | 裸露在空间里 | 最能体现 PPTX 呼吸感 |

最低要求：
- 2 张及以上 card 时，至少 2 种 `card_style`

---

## 4. 图表类型

| `chart_type` | 何时优先选 |
|-------------|-----------|
| `kpi` | 单个关键指标 |
| `metric_row` | 多个并列指标 |
| `sparkline` | 时间趋势，适合铺底 |
| `comparison_bar` | 两项对比 |
| `ring` | 百分比 / 完成度 |
| `stacked_bar` | 分类占比 |
| `timeline` | 历史节点 |
| `funnel` | 转化漏斗 |
| `radar` | 多维能力 |
| `treemap` | 层级面积 |
| `waffle` | 让比例更直觉 |
| `progress_bar` | 目标进度 |
| `rating` | 评分场景 |

---

## 5. 技法牌（T）选牌建议

| 技法 | 适合页面 | 常见作用 |
|-----|---------|---------|
| `T1` | 封面 / 章节 / 金句 / 数据 | 巨型水印识别度 |
| `T2` | 数据页 | 极致字号反差 |
| `T3` | 对比 / 混合网格 | Z 轴叠压 |
| `T4` | 浅色内容页 | 浮岛凸起 |
| `T5` | 目录 / 流程 / 科技风 | 斜切导向线 |
| `T6` | 氛围页 / 架构页 | 底纹穿透 |
| `T7` | 金句 / 章节 / 封面 | 留白压迫 |
| `T8` | 对比 / 封面 / 叙事冲突 | 非对称重力 |
| `T9` | 时间线 / 数据节点 | 锚点标记 |
| `T10` | 数据卡 | 图表铺底 |

规则：
- 每页 2-3 张
- 相邻页组合不应完全相同

---

## 6. CSS 武器（W）选牌建议

| 武器 | 适合区域 | 用途 |
|-----|---------|-----|
| `W1` | 标题 / 数字 | 渐变文字 |
| `W2` | 卡片 / 色块 | 几何裁切 |
| `W3` | 背景 | 穿孔遮罩 |
| `W4` | 图表 | 环形进度 |
| `W5` | 卡片 | 毛玻璃 |
| `W6` | 水印 / 装饰 | 混合模式 |
| `W7` | 主卡片 | 多层阴影 |
| `W8` | 角标 / 分隔 | 伪元素精修 |
| `W9` | 空间结构 | 脱框 / 出血 / 消融 |
| `W10` | 背景材质 | 颗粒 / 扫描线 / 拟态 |
| `W11` | 页面角落 | HUD 边角框定 |
| `W12` | 页脚 / 导航 | 叙事化页脚 |

---

## 7. 页面策划最小决策顺序

1. 先定 `page_goal`
2. 再定 `narrative_role`
3. 再定 `visual_weight`
4. 再选 `layout_hint`
5. 再拆 `cards[]`
6. 再写 `director_command`
7. 查 `decoration_recommendation`（packet 中已按 card_type 计算好推荐 T/W 和密度档位）
8. 最后补 `decoration_hints`（以推荐为起点，可按页面情绪微调，不可完全抛开推荐自由发挥）

如果顺序反了，通常会出现“先想样子，再硬塞内容”的问题。
