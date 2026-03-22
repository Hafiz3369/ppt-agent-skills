# T 型布局 (1 宽顶部 + 1 大底左 + 2 小底右)

适用：总览 + 详细展开 + 侧面数据。与"英雄式"的区别在于底部是非均分的。

## CSS Grid 定义

```css
.content-area {
  grid-template-columns: 2fr 1fr;
  grid-template-rows: auto 1fr 1fr;
}
/* 顶部横条: grid-row:1, grid-column:1/-1 -> 1200x200 */
/* 底左大卡: grid-row:2/4, grid-column:1 -> 790x360 */
/* 底右上: grid-row:2, grid-column:2 -> 390x170 */
/* 底右下: grid-row:3, grid-column:2 -> 390x170 */
```

## HTML 骨架（关键：顶部跨列 + 底左跨行）

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:2fr 1fr; grid-template-rows:auto 1fr 1fr; gap:20px;">

  <!-- 卡片 1: 顶部横条（跨两列） -->
  <!-- ★ 必须写 grid-column: 1 / -1 ★ -->
  <div class="card" style="grid-row: 1; grid-column: 1 / -1;
       /* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-1);"></div>
      <h3 style="font-size:20px; font-weight:700; color:var(--text-primary);">总览</h3>
    </div>
    <!-- 总览内容：概述 + 关键指标行 -->
  </div>

  <!-- 卡片 2: 底左大卡（跨后两行） -->
  <!-- ★ 必须写 grid-row: 2 / 4 ★ -->
  <div class="card" style="grid-row: 2 / 4; grid-column: 1;
       /* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-2);"></div>
      <h3 style="font-size:18px; font-weight:700; color:var(--text-primary);">详细展开</h3>
    </div>
    <!-- 详细内容：图表 + 文字解读 -->
  </div>

  <!-- 卡片 3: 底右上 -->
  <div class="card" style="grid-row: 2; grid-column: 2;
       /* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-3);"></div>
      <h3 style="font-size:15px; font-weight:700; color:var(--text-primary);">侧面数据 A</h3>
    </div>
    <!-- 紧凑数据 -->
  </div>

  <!-- 卡片 4: 底右下 -->
  <div class="card" style="grid-row: 3; grid-column: 2;
       /* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-4);"></div>
      <h3 style="font-size:15px; font-weight:700; color:var(--text-primary);">侧面数据 B</h3>
    </div>
    <!-- 紧凑数据 -->
  </div>

</div>
```

## 易错点

| 错误 | 正确 |
|------|------|
| 顶部横条没写 `grid-column: 1 / -1` | 必须写，否则只占一列 |
| 底左大卡没写 `grid-row: 2 / 4` | 必须写，否则只占一行 |
| 所有卡片只写了 grid-column 但没写 grid-row | T 型布局**每个卡片都需要明确的 grid-row + grid-column** |

## 设计要点

- 顶部横条高度由内容决定（auto），适合放概述文字 + 横向指标
- 底左大卡约 790x360，适合详细论述 + 可视化
- 底右小卡约 390x170，空间紧凑，用 padding:20px + gap:12px + 标题 15px
