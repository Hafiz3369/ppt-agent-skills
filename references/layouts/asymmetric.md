# 非对称两栏布局 (2/3 + 1/3)

适用: 主次关系。**最常用的布局 -- 一个核心论点 + 一个辅助数据区。**

## CSS Grid 定义

```css
.content-area {
  grid-template: 1fr / 2fr 1fr;
}
/* 主: 790x580 | 辅: 390x580 */
```

## HTML 骨架

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:2fr 1fr; gap:20px;">

  <!-- 卡片 1: 主区域（左，宽 ~790px） -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-1);"></div>
      <h3 style="font-size:20px; font-weight:700; color:var(--text-primary);">核心论点标题</h3>
    </div>
    <!-- 主卡片：放置核心论述、大段文字、主要数据可视化 -->
  </div>

  <!-- 卡片 2: 辅助区域（右，宽 ~390px） -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-2);"></div>
      <h3 style="font-size:18px; font-weight:700; color:var(--text-primary);">辅助数据</h3>
    </div>
    <!-- 辅助卡片：放置 KPI、环形图、列表等补充信息 -->
  </div>

</div>
```

## 设计要点

- 主卡片（左）承载核心内容，视觉重心在左
- 辅助卡片（右）承载补充数据/列表，字号可比主卡片小 1-2px
- 不需要额外的 `grid-row` / `grid-column` 指定
