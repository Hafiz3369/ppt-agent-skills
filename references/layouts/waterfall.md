# 瀑布流布局 (3 列不等高)

适用：多条信息块、FAQ、特性列表。**推荐：4-6 个不等高信息块自然排列。**

## CSS Grid 定义

```css
.content-area {
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: auto;
  align-content: start;
}
/* 卡片自然排列，高度由内容决定 */
/* 整体用 align-content:start 确保从顶部开始排列 */
```

## HTML 骨架

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:repeat(3, 1fr); grid-auto-rows:auto;
     align-content:start; gap:20px; overflow:hidden;">

  <!-- 卡片按顺序自动从左到右、从上到下排列 -->
  <!-- 不需要写 grid-row/grid-column -->

  <!-- 卡片 1 -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-1);"></div>
      <h3 style="font-size:16px; font-weight:700; color:var(--text-primary);">要点 A</h3>
    </div>
    <p style="font-size:13px; color:var(--text-secondary); line-height:1.7;">内容文字...</p>
  </div>

  <!-- 卡片 2 (可以更高) -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">
    <!-- 内容可以比卡片1多 -->
  </div>

  <!-- 卡片 3-6: 同样的结构，不同的内容长度 -->
  <!-- ... -->

</div>
```

## 设计要点

- 瀑布流的关键是 `grid-auto-rows: auto` + `align-content: start`
- 卡片高度由内容决定，不同卡片可以有不同高度
- 3 列布局下每张卡片约 387px 宽，内容要紧凑
- 外层容器 `overflow:hidden` 防止内容溢出 580px 高度限制
- 不需要任何 `grid-row` / `grid-column` 指定
- 瀑布流适合 FAQ、多特性列表、多维度分析等场景
