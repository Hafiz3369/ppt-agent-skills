# 50/50 对称布局

适用: 对比、并列概念（A vs B、优势 vs 劣势、方案 A vs 方案 B）

## CSS Grid 定义

```css
.content-area {
  grid-template: 1fr / 1fr 1fr;
}
/* 左: 590x580 | 右: 590x580 */
```

## HTML 骨架

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:1fr 1fr; gap:20px;">

  <!-- 卡片 1: 左侧 -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-1);"></div>
      <h3 style="font-size:18px; font-weight:700; color:var(--text-primary);">左侧标题</h3>
    </div>
    <!-- 卡片内容区 -->
  </div>

  <!-- 卡片 2: 右侧 -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-2);"></div>
      <h3 style="font-size:18px; font-weight:700; color:var(--text-primary);">右侧标题</h3>
    </div>
    <!-- 卡片内容区 -->
  </div>

</div>
```

## 设计要点

- 两张卡片用不同 accent 色竖线区分（左 accent-1，右 accent-2）
- 对比型内容建议左右卡片内部结构对称（同样的字号、同样的数据展示方式）
- 不需要额外的 `grid-row` / `grid-column` 指定，CSS Grid 自动排列
