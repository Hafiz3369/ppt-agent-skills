# 顶部英雄式布局

适用: 总分关系。**推荐：总分结构清晰时优先选择。** 一个总览区 + 下方 2-4 个子项。

## 3 子项版（最常用）

```css
.content-area {
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto 1fr;
}
/* 英雄: 1200x260 (跨3列) | 子1-3: 387x300 */
```

### HTML 骨架（只定义 Grid 结构，卡片样式由 card_style 决定）

> **骨架只管位置和大小，不管卡片长什么样。** 每张卡片的 background/border/shadow 由策划稿的 card_style 字段决定，参照 `blocks/card-styles.md` 的 CSS 实现。

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:repeat(3, 1fr); grid-template-rows:auto 1fr; gap:20px;">

  <!-- 英雄卡片: 顶部横条（跨所有列） -->
  <!-- ★ 必须写 grid-column: 1 / -1 ★ -->
  <!-- ★ 卡片样式由 card_style 字段决定（见下方样式映射） ★ -->
  <div class="card" style="grid-column: 1 / -1;
       /* ← 此处填入 card_style 对应的 CSS（见 blocks/card-styles.md）*/
       border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">
    <!-- 英雄区内容 -->
  </div>

  <!-- 子卡片 1 -->
  <!-- ★ 不写 grid-column，自动排列 ★ -->
  <div class="card" style="/* ← card_style CSS */
       border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">
    <!-- 内容 -->
  </div>

  <!-- 子卡片 2 -->
  <div class="card" style="/* ← card_style CSS */
       border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">
    <!-- 内容 -->
  </div>

  <!-- 子卡片 3 -->
  <div class="card" style="/* ← card_style CSS */
       border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">
    <!-- 内容 -->
  </div>

</div>
```

### card_style 样式映射（每张卡片根据策划稿的 card_style 值填入）

| card_style | 填入骨架 `/* ← card_style CSS */` 处的代码 |
|-----------|----------------------------------------|
| `filled` | `background:linear-gradient(135deg, var(--card-bg-from), var(--card-bg-to)); border:1px solid var(--card-border);` |
| `transparent` | `background:transparent; border:none;` |
| `outline` | `background:transparent; border:1px solid rgba(var(--accent-1-rgb), 0.2);` |
| `accent` | `background:linear-gradient(135deg, var(--accent-1), var(--accent-2, var(--accent-1))); color:#fff;` |
| `glass` | `background:rgba(var(--card-bg-rgb), 0.4); backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); border:1px solid rgba(255,255,255,0.08);` |
| `elevated` | `background:linear-gradient(135deg, var(--card-bg-from), var(--card-bg-to)); box-shadow:0 8px 32px rgba(0,0,0,0.12);` |

## 4 子项版

```css
.content-area {
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: auto 1fr;
}
/* 英雄: 1200x260 (跨4列) | 子1-4: 285x300 */
```

英雄卡片写 `grid-column: 1 / -1;`，4 个子卡片不写 grid-column 自动排列。

## 2 子项版

```css
.content-area {
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto 1fr;
}
/* 英雄: 1200x280 (跨2列) | 子1-2: 590x280 */
```

英雄卡片写 `grid-column: 1 / -1;`。

## 易错点

| 错误 | 正确 |
|------|------|
| 英雄卡片没写 `grid-column: 1 / -1` | 英雄卡片**必须**写 `grid-column: 1 / -1` 跨所有列 |
| 子卡片也写了 `grid-column` | 子卡片**不写** `grid-column`，自动排列 |
| `grid-template-rows: 1fr 1fr` | 应该用 `auto 1fr`，让英雄区高度由内容决定 |
| 所有卡片都用 filled 样式 | 根据 card_style 字段应用不同样式（至少 2 种） |

## 设计要点

- 英雄区高度由内容决定（`auto`），剩余空间分给子卡片（`1fr`）
- 子卡片空间较小（尤其 4 子项版只有 285px 宽），内容要精简
- 子卡片适合放 data/KPI/列表等紧凑内容
- **英雄区推荐 `transparent` 或 `accent` card_style**（让它视觉上区别于子卡片）
- **子卡片之间推荐混合 `filled` + `outline`**（避免一排同色方块）
