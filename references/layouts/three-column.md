# 三栏等宽布局

适用: 3 个并列比较（三大优势、三个阶段、三个产品）

## CSS Grid 定义

```css
.content-area {
  grid-template: 1fr / repeat(3, 1fr);
}
/* 卡1: 387x580 | 卡2: 387x580 | 卡3: 386x580 */
```

## HTML 骨架

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:repeat(3, 1fr); gap:20px;">

  <!-- 卡片 1 -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-1);"></div>
      <h3 style="font-size:18px; font-weight:700; color:var(--text-primary);">项目 A</h3>
    </div>
    <!-- 内容 -->
  </div>

  <!-- 卡片 2 -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-2);"></div>
      <h3 style="font-size:18px; font-weight:700; color:var(--text-primary);">项目 B</h3>
    </div>
    <!-- 内容 -->
  </div>

  <!-- 卡片 3 -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-3);"></div>
      <h3 style="font-size:18px; font-weight:700; color:var(--text-primary);">项目 C</h3>
    </div>
    <!-- 内容 -->
  </div>

</div>
```

## 设计要点

- 三张卡片内部结构保持对称（同样的标题位置、同样的内容排列）
- 各卡片用不同 accent 色竖线区分
- 387px 宽度下内容要紧凑，正文 13px、列表项控制在 4 条以内
- 不需要 `grid-row` / `grid-column` 指定
