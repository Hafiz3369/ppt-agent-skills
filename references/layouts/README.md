# Bento Grid 布局系统

## 画布参数

```
固定画布: width=1280px, height=720px
标题区: x=40, y=20, w=1200, h=50
内容区: x=40, y=80, w=1200, h=580
卡片间距: gap=20px
卡片圆角: border-radius=12px
卡片内边距: padding=24px
```

## 骨架与 card_style 的职责分离

> **骨架只管 Grid 位置和大小，不管卡片长什么样。**

每个布局文件的 HTML 骨架中，卡片的 `background` / `border` / `box-shadow` 留空为 `/* ← card_style CSS */` 注释。生成 HTML 时：

1. 复制骨架的 Grid 结构（grid-template-columns/rows、grid-column/row）
2. 根据策划稿中每张卡片的 `card_style` 字段，从 `blocks/card-styles.md` 查找对应 CSS 填入
3. **每页至少 2 种 card_style**（硬性要求）

`card_style` -> CSS 速查（完整定义见 `blocks/card-styles.md`）：

| card_style | 填入位置 |
|-----------|---------|
| `filled` | `background:linear-gradient(135deg, var(--card-bg-from), var(--card-bg-to)); border:1px solid var(--card-border);` |
| `transparent` | `background:transparent; border:none;` |
| `outline` | `background:transparent; border:1px solid rgba(var(--accent-1-rgb), 0.2);` |
| `accent` | `background:linear-gradient(135deg, var(--accent-1), var(--accent-2)); color:#fff;` |
| `glass` | `background:rgba(var(--card-bg-rgb), 0.4); backdrop-filter:blur(12px);` |
| `elevated` | `background:linear-gradient(135deg, var(--card-bg-from), var(--card-bg-to)); box-shadow:0 8px 32px rgba(0,0,0,0.12);` |

## CSS Grid 实现

所有布局通过 CSS Grid 精确实现。内容区容器统一定义：

```css
.content-area {
  position: absolute;
  left: 40px; top: 80px;
  width: 1200px; height: 580px;
  display: grid;
  gap: 20px;
}
```

### 骨架使用总则

每个布局文件（如 `hero-top.md`、`primary-secondary.md`）都包含**完整的 HTML 骨架代码**，标注了每个卡片需要的 `grid-row` 和 `grid-column` 属性。生成 HTML 时：

1. 读取对应布局文件的 HTML 骨架
2. 以骨架为起点，只替换卡片内部内容（标题、正文、数据、图表）
3. 跨行/跨列的 `grid-row: 1 / -1` 或 `grid-column: 1 / -1` 等属性不可删除
4. 简单布局（对称、非对称、三栏、瀑布流）不需要额外的 grid 定位；复杂布局（主次、英雄、L型、T型、混合网格的跨列变体）需要严格按骨架标注

## 页面类型布局

### 封面页 (cover)
- 大标题居中或左对齐, font-size=48-56px, accent-primary 色
- 副标题 font-size=24px
- 演讲人/日期/公司 底部小号文字 font-size=16px
- 装饰: 品牌色块、几何线条、配图（渐隐融合技法）
- **不使用 Bento Grid**，自由排版

### 目录页 (toc)
- 2-5 个等大卡片网格

| 卡片数 | grid-template-columns | 单卡尺寸 |
|-------|----------------------|---------|
| 2 | 1fr 1fr | 590x540 |
| 3 | repeat(3, 1fr) | 387x540 |
| 4 | 1fr 1fr / 1fr 1fr (2x2) | 590x260 |
| 5 | repeat(3, 1fr) / repeat(2, 1fr) (3+2) | 混合 |

### 章节封面 (section)
- "PART 0X" font-size=20px, accent-primary, letter-spacing=2px
- 标题 font-size=44px, font-weight=700
- 导语 font-size=18px, color=text-secondary
- 大量留白，营造呼吸感
- **不使用 Bento Grid**，居中排版

### 结束页 (end)
- 标题 font-size=44px 居中
- 核心要点 3-5 个, font-size=18px
- 联系方式/CTA 底部

---

## 布局决策矩阵

| 内容特征 | 推荐布局 | 文件 | 卡片数 |
|---------|---------|------|-------|
| 1 个核心论点/数据 | 单一焦点 | `single-focus.md` | 1 |
| 2 个对比/并列 | 50/50 对称 | `symmetric.md` | 2 |
| 主概念 + 补充 | 非对称两栏 | `asymmetric.md` | 2 |
| 3 个并列要素 | 三栏等宽 | `three-column.md` | 3 |
| 1 核心 + 2 辅助 | 主次结合 | `primary-secondary.md` | 3 |
| 综述 + 3-4 子项 | 顶部英雄式 | `hero-top.md` | 4-5 |
| 4-6 异构块 | 混合网格 | `mixed-grid.md` | 4-6 |
| 主区 + 侧栏 + 底部总结 | L 型 | `l-shape.md` | 4 |
| 总览 + 展开 + 侧面数据 | T 型 | `t-shape.md` | 4 |
| 多条不等高信息 | 瀑布流 | `waterfall.md` | 4-6 |

**选择优先级**：避免"单一焦点"（除非确实只有一个全屏内容）。内容>=3块时，优先选择主次结合/英雄式/混合网格。

---

## 6 种卡片内容类型

### text（文本卡片）
- 标题: h3, 18-20px, 700 weight
- 正文: p, 13-14px, line-height 1.8
- 关键词用 `<strong>` 或 `<span class="highlight">` 高亮
- **最低要求**: 标题 + 至少 2 段正文（每段 30-50 字）

### data（数据卡片）
- 核心数字: 36-48px, 800 weight, accent 色
- 单位/标签: 14-16px, text-secondary
- 补充解读: 13px
- 推荐搭配一个 CSS 可视化（进度条/对比柱/环形图）
- **最低要求**: 核心数字 + 单位 + 趋势 + 解读 + 可视化

### list（列表卡片）
- 圆点: 6-8px 圆点, accent 色
- 文字: 13px, line-height 1.6
- 交替使用不同 accent 色圆点增加层次感
- **最低要求**: 至少 4 条列表项，每条 15-30 字

### tag_cloud（标签云）
- 容器: flex-wrap, gap=8px
- 标签: 圆角胶囊形, 12px, accent 色边框
- **最低要求**: 至少 5 个标签

### process（流程卡片）
- 节点: 32px 圆形, accent 色, 居中步骤数字
- 连线: **真实 `<div>` 元素**（禁止 ::before/::after）
- 箭头: **内联 SVG `<polygon>`**（禁止 CSS border 三角形）
- **最低要求**: 至少 3 个步骤，每步标题 + 一句描述

### data_highlight（大数据高亮区）
- 用于封面或重点页的超大数据展示
- 数字: 64-80px, 900 weight, accent 色
- 副标题 + 补充数据行
- **最低要求**: 1 个超大数字 + 副标题 + 补充数据行
