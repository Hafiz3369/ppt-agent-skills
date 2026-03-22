# 单一焦点布局

适用: 一个核心论点/一张全屏图表/一个关键数据。**极少使用 -- 除非该页确实只有一个全屏内容。**

## CSS Grid 定义

```css
.content-area {
  grid-template: 1fr / 1fr;
}
/* 单卡: 1200x580 */
```

## HTML 骨架

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:1fr; gap:20px;">

  <!-- 唯一卡片: 全幅 -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:32px; display:flex; flex-direction:column; gap:20px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-1);"></div>
      <h3 style="font-size:22px; font-weight:700; color:var(--text-primary);">焦点标题</h3>
    </div>
    <!-- 大面积内容区：可放全屏图表、大段论述、核心数据展示 -->
    <!-- 内部可用 flex/grid 进一步分区 -->
  </div>

</div>
```

## 设计要点

- 卡片内部可用 CSS Grid 二次分区（如左文字右图表）
- padding 可以用 32px（比标准 24px 稍大），因为空间充裕
- 适合放一个大型 SVG 数据可视化 + 解读文字
