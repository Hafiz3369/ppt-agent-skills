# 设计规格书（A/B/C/D/E -- 稳定参考，由 `scripts/resource_loader.py` 自动注入 GLOBAL_RESOURCES）

> 本文件包含画布规范、排版阶梯、卡片规则、色彩装饰、页面类型设计和输出规范。
> 内容稳定且不需要每次都在 LLM 上下文中占位，由 assembler 机械化注入。

---

## A. 画布与排版

### 画布规范（不可修改）

- 固定尺寸: width=1280px, height=720px, overflow=hidden
- 标题区: 左上 40px 边距, y=20~70, 最大高度 50px
- 内容区: padding 40px, y 从 80px 起, 可用高度 580px, 可用宽度 1200px
- 页脚区: 底部 40px 边距内，高度 20px

### 排版阶梯（拉开分层 -- 字号反差是设计力的核心指标）

| 层级 | 用途 | 字号 | 字重 | 行高 | 颜色 | 设计建议 |
|------|------|------|------|------|------|---------|
| H0 | 封面主标题 | 48-160px | 900 | 0.85-1.1 | --text-primary | 尽量让封面标题 >= 80px，奠定气场 |
| H1 | 页面主标题 | 26-32px | 700 | 1.2 | --text-primary | 推荐用渐变文字填充 |
| H2 | 卡片标题 | 16-20px | 700 | 1.3 | --text-primary | - |
| Body | 正文段落 | 13-14px | 400 | 1.8 | --text-secondary | - |
| Caption | 辅助标注 | 9-12px | 400 | 1.5 | --text-secondary, opacity 0.4-0.6 | - |
| Overline | PART 标识 | 10-12px | 700, letter-spacing: 2-4px | 1.0 | --accent-1 | 推荐给内容页加上 overline，提升空间层次 |
| Data-Hero | **核心 KPI（视觉锚点）** | **64-120px** | 900 | 0.85-1.0 | --accent-1 | **建议在数据页设置至少一个 64px+ 的超级数字** |
| Data-Sub | 辅助指标 | 28-40px | 800 | 1.0 | --accent-2/--accent-4 | 辅助数据应该拉开与核心 KPI 的大小反差 |

> **字号反差的极佳张力点**：建议每页最大字号与最小字号的**倍数比最好 >= 5 倍**。

### 间距是情绪变量（至少 2 种不同间距/页）

| 内容关系 | 间距 |
|---------|------|
| 数字 + 注解（紧密共生） | gap:2-4px |
| 同组卡片之间 | gap:16-20px |
| 不同主题区域 | gap:32-48px |
| 核心论点孤立 | padding:48-80px |

### Bento Grid：重力参考，不是物理枷锁

1. **骨架是重力场不是牢笼** -- 用骨架确定大致方位，再用技法牌打破硬切割
2. **极力制造密度不均匀** -- 即使骨架对称，视觉重量也应该引导为一重一轻
3. **消除盒子感** -- 同主题卡片间的视觉边界要模糊化

#### 消除盒子感的手段

> **唯一的安全底线**：卡片**内部内容**不溢出卡片自身边界（每张卡片 `overflow:hidden`，正文 `-webkit-line-clamp` 截断）。卡片**本身**可以随意摆放、倾斜、重叠。

**鼓励使用的破界手段**：

```css
/* 负 margin 叠压 */ .card-overlap { margin-top: -20px; position: relative; z-index: 3; }
/* 出血定位 */ .bleed-element { position: absolute; left: -40px; width: calc(100% + 80px); }
/* 斜切裁剪 */ .card-sliced { clip-path: polygon(0 0, 100% 0, 100% 90%, 0 100%); }
/* 绝对定位 */ .card-free { position: absolute; top: 120px; left: 60px; width: 480px; }
/* 跨区域装饰 */ .deco-cross { position: absolute; z-index: 5; pointer-events: none; }
/* 背景色融合 */ .card-merged { background: transparent; border-right: 1px solid var(--card-border); }
```

> **布局方式完全自由**：CSS Grid、Flexbox、position:absolute、混合使用均可。

### 五层景深架构

| 层 | z-index | 内容 | 典型 CSS |
|----|---------|------|----------|
| **L0 背景层** | 0 | 背景色/渐变/氛围底图 | `background`, `background-image` |
| **L1 装饰底纹层** | 1 | 破界水印(T1)、底纹穿透(T6) | `position:absolute`, opacity 0.03-0.08 |
| **L2 内容承载层** | 2 | 卡片主体 | Grid 主要子元素 |
| **L3 强调浮层** | 3 | elevated/accent 卡片 | `box-shadow`, `transform:translateY(-4px)` |
| **L4 焦点层** | 4 | 超大数据数字(T2)、脉冲锚点(T9) | `position:relative; z-index:4` |

每页至少激活 3 层。

### 构图锚点与视觉动线

| 动线 | 适用页面 | 核心构图手段 |
|------|---------|-------------|
| **Z 型** | 标准内容页 | 左上标题 -> 右上数据 -> 左下论据 -> 右下结论 |
| **F 型** | 列表/文字密集页 | 标题横扫 -> 纵向快速扫描 |
| **焦点放射** | 单一数据/金句页 | 焦点居中或偏心，装饰从焦点向外扩散 |

**三分法锚点**：4 个交叉点（约 427,240 / 853,240 / 427,480 / 853,480）是视觉强点。画布正中央是最无聊的位置。

### 留白与视觉焦点

| 页面类型 | 内容填充率 |
|---------|-----------|
| 封面页 | 40-55% |
| 章节封面 | 25-40% |
| 标准内容 | 60-75% |
| 数据密集 | 70-80% |
| 结束页 | 35-50% |

---

## B. 内容与卡片

### 6 种基础卡片内容底线

| 卡片类型 | 最低内容要求 |
|---------|------------|
| text | 标题 + 至少 2 段正文或 3-5 条要点 |
| data | 核心数字 + 单位 + 趋势 + 解读 + 可视化 |
| list | 至少 4 条，每条 15-30 字 |
| process | 至少 3 步，每步标题 + 描述 |
| tag_cloud | 至少 5 个标签，胶囊形 |
| data_highlight | 超大数字 + 副标题 + 补充数据行 |

### 卡片视觉变体（card_style）

- **追求层次反差**：一页至少 2 种 card_style
- `accent`：视觉爆裂点，通常一页 1 个
- `transparent`：推荐给复合组件（timeline/diagram/quote）
- `elevated`：悬浮锚点，多层阴影
- `filled`/`outline`/`glass`：自由搭配

### 微细节武器库

| 细节类别 | 手法 |
|---------|------|
| 标题装饰线 | accent 色 3px 短线（每页不同手法） |
| 关键词高亮 | 正文核心词用 accent 色/加粗/底色药丸 |
| 数据趋势标记 | 数字旁微小趋势箭头 |
| 卡片角标 | 序号/类别标记 |
| 精致分隔 | 渐变线/虚线替代硬切割 gap |
| 图标化要点 | list 每条前用不同色圆点/方块 |
| 数据来源标注 | 底部极小字标注 |

**使用密度**：每页至少 3 种微细节手法。

### 元素韵律

| 节奏模式 | 适用场景 |
|---------|---------|
| **主副** | 1 个核心 + 2-3 个辅助，核心占 2fr |
| **递减** | 重要性递减，第一张跨 2 列 |
| **交错** | 等重要但需节奏感 |
| **孤岛+群落** | 核心独占 40-60%，辅助群紧密排列 |

**避免均等**：不要让所有卡片等宽等高排成一行。

---

## C. 色彩与装饰

### 60-30-10 色彩节奏

| 比例 | 角色 | 应用范围 |
|------|------|---------|
| 60% | 主色（背景） | --bg-primary |
| 30% | 辅色（内容区） | --card-bg-from/to |
| 10% | 强调色（点缀） | --accent-1 ~ --accent-4 |

> accent 色同页 1-2 种效果最佳。多色需求（如 tag_cloud）可灵活使用 accent-1 到 accent-4。

### 装饰元素

每页 2-3 种装饰。来源于策划稿 `decoration_hints` 三维度。

### 解构的导航体系

底部辅助信息（章节、页码、品牌）可多样化：极高竖行文本、极端大小反差、分散放置、叙事化页脚（W12）等。

### 渐变使用指引

- 同一页渐变方向保持和谐
- 渐变色彩从 CSS 变量取值

### 色彩与可读性

- 正文文字与背景对比度保持可读
- accent 色优先用于标题/标签/数据，不用于大段正文
- 颜色优先通过 `var(--xxx)` 引用

### 特殊字符

温度用 `°C`，化学式用 `<sub>`/`<sup>`，微米用 `μm`。

---

## D. 页面类型专属设计

### 封面页
- H0 标题 80px+，配图可采用 `hero-blend` 渐隐融合技法（运行时通常落在 `hero-background` usage）
- 景深：L0(渐变底) + L1(品牌水印) + L4(超大标题)
- 字号断层：主标题 80-160px vs 副标题 14-16px

### 目录页
- 3 秒让观众理解路线，Part 标题是唯一主角
- 避免 Word 式居中编号列表

### 章节封面
- 70%+ 留白，标题极度偏心
- PART 编号 120px+ opacity 0.04 铺背景
- 景深仅 L0+L1 两层极度克制

### 数据仪表盘页
- 核心 KPI 脱框（position:absolute, 80-120px）
- 辅助指标潜伏在小卡片中（28-40px）
- 景深：L0(暗色控制台底) + L1(数据铺底) + L2(辅助卡片) + L3(脱框数字) + L4(高亮标注)

### 对比分析页
- 推荐方案 accent 光晕隆起，被弃方案蜷伏灰暗
- 跨中缝 VS 徽章 / 对角渐变带破僵局

### 流程/时间线页
- 时间线/流程线是画面骨架
- 推荐 transparent card_style

### 金句/引言页
- 填充率 < 30%，留白 >= 70%
- 金句偏心放置，T7 留白压迫
- 景深：L0 + L1(破界水印 opacity 0.02) + L4(金句)

### 结束页
- 封面的收束镜像（不是复制粘贴）
- 呼应维度选 1-2 种：色调/构图镜像/元素回声/情绪闭环

---

## E. 输出规范

### HTML 骨架参考

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280">
<title>Slide {NN} - {TITLE}</title>
<style>
:root { /* 从 style.json 展开完整 CSS 变量 */ }
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
body {
  width:1280px; height:720px; overflow:hidden;
  background: var(--bg-primary);
  font-family: 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;
  position:relative; color:var(--text-primary);
}
</style>
</head>
<body>
<!-- 你的设计从这里开始 -->
</body>
</html>
```

### 隐形物理法则（5 条技术红线）

| # | 物理法则 | 设计意义 |
|---|--------|------|
| 1 | 1280x720px 画布，`body overflow:hidden` | 画布边界即视口 |
| 2 | 全局 `font-family` 统一 | 秩序的基石 |
| 3 | 全局依赖 CSS 变量 | 色彩锁定同一宇宙 |
| 4 | 容器内文字不溢出（`overflow:hidden` + `line-clamp`） | 容器壳可随意移动叠压 |
| 5 | 只使用纯静态视觉（无 `@keyframes`/`animation`/`transition`） | PPTX 导出不支持动画 |

### CSS 能力释放

可自由使用：`background-clip:text` / `clip-path` / `mask-image` / `conic-gradient` / `backdrop-filter` / `mix-blend-mode` / 多层 `box-shadow` / 伪元素 / `writing-mode` / `filter`。禁止 `@keyframes`/`animation`/`transition`。

### 设计倾向

| 平庸倾向 | 更好的选择 |
|---------|-----------|
| 标题 `text-align:center` | 偏心定位 + 装饰线 |
| 所有卡片同 padding | 核心更大，辅助更紧凑 |
| 全页 `flex; center; center` | 三分法偏心 + 对角线张力 |
| 所有卡片等大等高 | 主副节奏 / 递减 / 孤岛+群落 |
| 只用 1 层 box-shadow | 3-4 层渐进阴影 |
