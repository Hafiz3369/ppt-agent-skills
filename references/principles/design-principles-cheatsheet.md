# PPTX 设计原则操作手册 -- planning JSON 字段级指导

> **本文件将 6 大设计原则直接映射到 planning JSON 的具体字段操作。**
> 不是告诉你"什么是好设计"，而是告诉你"planning JSON 中每个字段怎么填才是好设计"。

---

## 一、视觉层级 -> 操作 `cards[]` 的 `card_style` 和 `card_type`

**核心原则**：每页只有 1 个视觉锚点。观众闭眼睁开第一个看到的 = 最重要的信息。

**怎么做**：

1. **确定锚点卡片**：在 `cards[]` 中找到承载该页最重要信息的那张卡片
   - 如果最重要的是一个数字 -> 锚点卡片 = `data` 或 `data_highlight` 类型
   - 如果最重要的是一个结论 -> 锚点卡片 = `text` 类型，且该卡片放在布局的主区域
   - 如果最重要的是一个对比 -> 锚点卡片 = `comparison` 类型

2. **用 `card_style` 拉开层级**：
   - 锚点卡片设为 `accent` 或 `elevated`（视觉最突出）
   - 其他卡片设为 `filled` / `transparent` / `outline`（视觉退后）
   - **禁止**同页出现 2 个 `accent` 卡片（= 2 个锚点在争夺注意力）

3. **用 `emphasis_keywords` 标记关键词**：
   - 锚点卡片的 `emphasis_keywords[]` 放 1-3 个最核心的词/数字
   - 非锚点卡片的 `emphasis_keywords[]` 最多 1 个或为空

**JSON 示例**（锚点是核心 KPI 数字）：
```json
{
  "cards": [
    {"card_type": "data", "card_style": "accent", "chart_type": "kpi",
     "title": "全球市场总规模", "data_points": ["2,847 亿美元"],
     "emphasis_keywords": ["2,847"]},
    {"card_type": "list", "card_style": "filled", "title": "三大细分市场",
     "emphasis_keywords": []},
    {"card_type": "data", "card_style": "transparent", "chart_type": "sparkline",
     "title": "增速最快赛道", "emphasis_keywords": []}
  ]
}
```

---

## 二、认知负荷 -> 操作 `goal`、`cards[]` 数量、内容字数

**核心原则**：人一次处理 5-9 个信息块。每页能用一句话总结。

**怎么做**：

1. **写 `goal` 字段时的自检**：
   - 写完 `goal` 后数一下有没有"和"字或"以及"
   - 有 -> 说明这页塞了 2 个核心观点，**必须拆成 2 页**
   - 正确的 goal：`"让观众知道 AI 基础设施市场正在爆发式增长"`
   - 错误的 goal：`"让观众知道市场在增长和竞争格局在变化"` -> 拆页

2. **`cards[]` 数量控制**：
   - content 页：3-5 张卡片（不是 2 张也不是 7 张）
   - 封面/章节封面/结束页：1-2 张卡片
   - 如果你发现需要 6+ 张卡片 -> 内容太多，拆成 2 页或合并同类卡片

3. **每张卡片的 `content` 字数限制**（硬性上限）：
   - text 卡片：标题 12 字 + 正文 150 字
   - data 卡片：解读 80 字
   - list 卡片：每条 30 字，最多 6 条
   - 超限 -> 拆为多张卡片，不要硬塞

---

## 三、构图与留白 -> 操作 `layout_hint` 和 `cards[].position`

**核心原则**：重要元素放画布 1/3 线交叉点，留白三层级递增。

**怎么做**：

1. **选 `layout_hint` 的决策逻辑**：

   | 你这页有什么 | 选什么 layout_hint | 锚点放哪里 |
   |------------|-------------------|-----------|
   | 1 个核心论点/金句 | 单一焦点 | 画布中心偏上 |
   | 1 个主体 + 2-3 个辅助 | 主次结合 / 英雄式 | 主体占上 1/3 或左 2/3 |
   | 2 个对比概念 | 50/50 对称 / 非对称两栏 | 各占一半 |
   | 3 个并列概念 | 三栏等宽 | 中间栏或用 accent 卡片突出其一 |
   | 4-6 个子项 | 混合网格 / L 型 / T 型 / 瀑布流 | 最重要的子项放左上或跨列 |

2. **`cards[].position` 填写规则**：
   - 锚点卡片的 position 放在布局的"最佳视觉位置"（通常是 `top-left`、`top-full`、或跨列区域）
   - 辅助卡片填满剩余区域
   - 不要所有卡片都居中（除封面/金句页）

3. **布局多样性硬性检查**：
   - 和前一页的 `layout_hint` 一样吗？ -> **必须换**
   - 全 PPT 中同一个 `layout_hint` 用了超过 30% 的页面？ -> 换别的

---

## 四、色彩 -> 操作 `card_style` 组合和 `decoration_hints`

**核心原则**：60% 背景 + 30% 内容载体 + 10% 强调色。

**怎么做**：

1. **`card_style` 组合规则（每页）**：
   - `accent` 类型：**最多 1 个**（它是注意力聚焦点）
   - `elevated` 类型：**最多 1 个**（它带阴影，太多页面"漂浮感"过强）
   - 剩余卡片从 `filled` / `transparent` / `outline` / `glass` 中选
   - **每页至少 2 种 card_style**（禁止所有卡片都 filled）
   - 推荐组合：`accent` + `transparent` + `filled` 或 `elevated` + `outline` + `transparent`

2. **`decoration_hints` 中的色彩控制**：
   - `background` 层的装饰用主色/辅色，不用 accent 色
   - `page_accent` 层（水印、分隔线）可以用 accent 色，但 opacity 必须极低（0.04-0.08）
   - `card_style` 层的装饰（左侧竖线、顶部色带）可以用 accent 色

---

## 五、数据可视化 -> 操作 `data` / `data_highlight` 卡片的所有字段

**核心原则**：观众 3 秒内理解结论。数字 + 对比才有意义。

**怎么做**：

1. **选 `chart_type` 前先问自己这个问题**：

   | 你想让观众 3 秒内得出什么结论 | 选什么 chart_type |
   |---------------------------|-----------------|
   | "XX 占了大头" | `ring` / `stacked_bar` / `treemap` |
   | "XX 在快速增长" | `sparkline` |
   | "XX 比 YY 强很多" | `comparison_bar` / `radar` |
   | "XX 达到了 N" | `kpi` / `metric_row` |
   | "XX 完成了 80%" | `progress_bar` / `rating` |
   | "XX 经历了这些阶段" | `timeline` |
   | "XX 在逐步流失" | `funnel` |

2. **`data_points` 必须带上下文**：
   - 错误：`["37%"]`（一个裸数字，观众不知道是高是低）
   - 正确：`["37%（行业均值 22%）"]` 或 `["37%", "同比 +15%"]`
   - `data_highlights` 中每个对象**必须填 `interpretation`**：
     ```json
     {"value": "2,847 亿", "label": "全球 TAM", "interpretation": "同比增长 34.2%，远超 GDP 增速"}
     ```

3. **`design_notes` 中标注数据属性**：
   - 如果 data_points 中有预测/估算数据 -> 写 `"注意：XXX 为预测值，设计时用虚线/浅色区分"`
   - 如果数字来源可信度为 medium -> 写 `"数据来源为行业媒体，非权威机构"`

---

## 六、叙事节奏 -> 操作 `visual_weight` 和页面排列顺序

**核心原则**：全 PPT 的密度形成波浪曲线，禁止连续 3 页同密度。

**怎么做**：

1. **`visual_weight` 赋值规则**：

   | 你这页的 page_type + 内容密度 | visual_weight 填多少 |
   |---------------------------|-------------------|
   | 封面页 | 8 |
   | 目录页 | 4 |
   | 章节封面 | 2 |
   | 结束页 | 6 |
   | 只有 1-2 张卡片的内容页 | 5 |
   | 3-4 张卡片的标准内容页 | 7 |
   | 5+ 张卡片 / 数据密集 / 混合网格 | 9 |
   | 对比页（50/50） | 6 |

2. **填完 visual_weight 后必须检查**：
   - 和前一页的差值超过 5 吗？-> 中间必须插一页过渡（如 vw=5 的单一焦点页）
   - 连续 3 页 vw >= 7 吗？-> 第 3 页必须降到 6 以下（换成对比页/金句页/章节封面）
   - 连续 3 页 vw <= 4 吗？-> 第 3 页必须升到 5 以上（增加内容密度）

3. **每个 Part 内的推荐 visual_weight 走势**：
   ```
   章节封面(2) -> 总览页(7) -> 数据页(9) -> 内容页(7) -> 小结(5~6)
   ```
   Part 只有 2-3 页时：`章节封面(2) -> 核心页(7~9) -> 结论页(5~6)`

---

## 逐页体检单（每页 planning JSON 完成后必须过一遍）

| # | 检查什么 | 看 JSON 的哪个字段 | 不通过怎么改 |
|---|---------|-----------------|------------|
| 1 | goal 是否"一句话一个核心"（不含"和"） | `goal` | 拆成 2 页，每页一个核心观点 |
| 2 | 谁是视觉锚点？只有 1 个吗？ | `cards[].card_style` | 确保只有 1 个 `accent` 卡片 |
| 3 | cards 数量 3-5，card_type >= 2 种 | `cards[]` 长度和类型 | 太多 -> 拆页或合并；太少 -> 补充卡片；类型单一 -> 替换为更合适的类型 |
| 4 | 锚点卡片的 position 在布局最佳位置 | `cards[].position` + `layout_hint` | 锚点移到 top-left / top-full / 跨列区域 |
| 5 | accent 类型 card_style <= 1 个 | `cards[].card_style` | 多余的 accent 改为 elevated 或 filled |
| 6 | data 卡片数字有上下文对比 | `data_points` / `data_highlights[].interpretation` | 裸数字加上对比参照（行业均值/同比/环比） |
| 7 | visual_weight 和前后页形成波浪 | `visual_weight` | 调整页面密度（加/减卡片，换 layout） |
| 8 | decoration_hints 和上一页至少 1 维不同 | `decoration_hints` 三个子字段 | 换其中一个维度的技法 |
