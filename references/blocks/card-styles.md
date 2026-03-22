# 卡片视觉变体（card_style）

> card_type 决定卡片"内容做什么"，card_style 决定卡片"长什么样"。
> 同一页必须使用至少 2 种 card_style，打破"一堆同色方块"的单调感。

## 6 种变体

### filled（默认）
```css
background: var(--card-bg);
border-radius: 12px;
padding: 24px;
```
- 标准卡片，大多数内容的默认选择
- 不需要在策划稿中明确写出（省略 card_style 时默认为 filled）

### transparent（透明/裸露）
```css
background: transparent;
border: none;
padding: 24px;
```
- **无背景、无边框**，内容直接暴露在页面上
- 适合：大号数据数字、标题区、引用金句、独立图标组
- 视觉效果：内容"浮"在页面上，靠间距和对齐表达分组
- 常搭配 card_type: `data_highlight` / `quote` / `image_hero`

### outline（描边）
```css
background: transparent;
border: 1px solid rgba(var(--accent-1-rgb), 0.2);
border-radius: 12px;
padding: 24px;
```
- 无背景，只有轻微描边暗示边界
- 适合：辅助信息、次要内容、与 filled 卡片形成层次对比
- 比 filled 更轻量，比 transparent 更有边界感

### accent（强调）
```css
background: linear-gradient(135deg, var(--accent-1), var(--accent-2, var(--accent-1)));
border-radius: 12px;
padding: 24px;
color: #ffffff;
```
- accent 色渐变背景 + 白色文字
- **一页最多 1 个**（否则强调效果失效）
- 适合：核心数据、CTA、本页最重要的一个论点
- 常搭配 card_type: `data` / `data_highlight` / `text`（核心论点）

### glass（毛玻璃）
```css
background: rgba(var(--card-bg-rgb), 0.4);
backdrop-filter: blur(12px);
-webkit-backdrop-filter: blur(12px);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 12px;
padding: 24px;
```
- 半透明毛玻璃效果
- 适合：有底图/渐变背景的页面，卡片叠加在视觉层之上
- 常搭配 card_type: `image_hero`（大图背景上叠加信息卡片）
- 注意：backdrop-filter 在部分浏览器需要 -webkit- 前缀

### elevated（悬浮）
```css
background: var(--card-bg);
border-radius: 12px;
padding: 24px;
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.08);
transform: translateY(-2px);
```
- 有明显阴影的悬浮卡片，视觉上"凸出"页面
- 适合：页面的视觉锚点、最重要的一张卡片
- **一页最多 1 个**（与 accent 同理）
- 和 transparent/outline 卡片组合时形成强烈层次对比

## 使用规则

1. **每页至少 2 种 card_style**（打破视觉单调是硬性要求）
2. **accent 和 elevated 各最多 1 个/页**（强调过多 = 没有强调）
3. 省略 card_style 时默认为 `filled`
4. 推荐组合（层次感从强到弱）：
   - `accent` + `transparent` + `filled`（最强对比）
   - `elevated` + `outline` + `transparent`（层次丰富）
   - `filled` + `outline`（温和对比）
   - `glass` + `transparent`（有底图时）

## 与 card_type 的推荐搭配

| card_type | 推荐 card_style | 说明 |
|----------|----------------|------|
| data_highlight | `transparent` / `accent` | 大数字不需要方块包裹，或用 accent 强调 |
| quote | `transparent` | 金句直接暴露在页面上更有力量感 |
| image_hero | `transparent` / `glass` | 大图不需要卡片边框 |
| timeline | `transparent` / `outline` | 时间线本身有线条结构，不需要额外方块 |
| diagram | `transparent` | 图解自带视觉结构 |
| comparison | `outline` | 描边区分两个面板 |
| data | `filled` / `accent`（核心指标） | 数据卡片用标准或强调 |
| text | `filled` / `outline` | 文本卡片用标准或描边 |
| list | `filled` | 列表适合在明确边界内 |
