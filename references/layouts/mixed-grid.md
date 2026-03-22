# 混合网格布局

适用: 高信息密度, 4-6个异构块。**推荐：信息密度最高时优先选择。**

## 2x3 网格（6 卡片）

```css
.content-area {
  grid-template-columns: 1fr 1fr;
  grid-template-rows: repeat(3, 1fr);
}
/* 6个卡片: 各 590x180 */
```

可通过 `grid-row`/`grid-column` 的 span 让个别卡片跨行/跨列，形成大小混搭效果。

### HTML 骨架

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:1fr 1fr; grid-template-rows:repeat(3, 1fr); gap:20px;">

  <!-- 6 个卡片，自动排列（左上 -> 右上 -> 左中 -> 右中 -> 左下 -> 右下） -->
  <!-- 不需要写 grid-row/grid-column，自动填充 -->
  <div class="card" style="..."><!-- 卡片1 --></div>
  <div class="card" style="..."><!-- 卡片2 --></div>
  <div class="card" style="..."><!-- 卡片3 --></div>
  <div class="card" style="..."><!-- 卡片4 --></div>
  <div class="card" style="..."><!-- 卡片5 --></div>
  <div class="card" style="..."><!-- 卡片6 --></div>
</div>
```

## 2+1+2 网格（5 卡片，大小交错）

```css
.content-area {
  grid-template-columns: 1fr 1fr;
  grid-template-rows: repeat(3, 1fr);
}
```

### HTML 骨架（关键：中间卡片必须跨两列）

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:1fr 1fr; grid-template-rows:repeat(3, 1fr); gap:20px;">

  <!-- 卡片1: 左上（自动排列到 row 1, col 1） -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">
    <!-- 590x180 -->
  </div>

  <!-- 卡片2: 右上（自动排列到 row 1, col 2） -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">
    <!-- 590x180 -->
  </div>

  <!-- 卡片3: 中间横条（跨两列） -->
  <!-- ★ 必须写 grid-column: 1 / -1 ★ -->
  <div class="card" style="grid-column: 1 / -1;
       /* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; align-items:center; gap:24px; overflow:hidden;">
    <!-- 1200x180 横向排列内容 -->
  </div>

  <!-- 卡片4: 左下（自动排列到 row 3, col 1） -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">
    <!-- 590x180 -->
  </div>

  <!-- 卡片5: 右下（自动排列到 row 3, col 2） -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">
    <!-- 590x180 -->
  </div>
</div>
```

## 1+2+1 重点突出（4 卡片）

```css
.content-area {
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto 1fr auto;
}
```

### HTML 骨架

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:1fr 1fr; grid-template-rows:auto 1fr auto; gap:20px;">

  <!-- 顶部大卡（跨两列） -->
  <!-- ★ grid-column: 1 / -1 ★ -->
  <div class="card" style="grid-column: 1 / -1; ...">
    <!-- 1200x~200 -->
  </div>

  <!-- 左（自动排列） -->
  <div class="card" style="..."><!-- 590x~260 --></div>

  <!-- 右（自动排列） -->
  <div class="card" style="..."><!-- 590x~260 --></div>

  <!-- 底部大卡（跨两列） -->
  <!-- ★ grid-column: 1 / -1 ★ -->
  <div class="card" style="grid-column: 1 / -1; ...">
    <!-- 1200x~100 -->
  </div>
</div>
```

## 易错点

| 错误 | 正确 |
|------|------|
| 2+1+2 的中间卡片没写 `grid-column: 1 / -1` | 必须写，否则不跨列 |
| 1+2+1 的顶部/底部卡片没写 `grid-column: 1 / -1` | 必须写 |
| 6 卡片网格里某个卡片写了 span 导致后续卡片错位 | 纯 6 等分时**不要**写任何 span |

## 设计要点

- 混合网格卡片尺寸较小（590x180 或更小），content 要极度精简
- 每张卡片 padding:20px（比标准 24px 小），gap:12px，标题 15-16px
- 数据卡片的大数字不超过 36px（空间限制）
- **关键约束**: 所有卡片不得超出内容区边界（x+w<=1240, y+h<=660），间距>=20px
