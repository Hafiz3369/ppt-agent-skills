# L 型布局 (1 大 + 2 小右侧 + 1 宽底部)

适用：核心展示区 + 辅助数据 + 底部总结/标签条。**推荐：主论点 + 侧面佐证 + 底部结论。**

## CSS Grid 定义

```css
.content-area {
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr auto;
}
/* 主卡片: grid-row:1/3, grid-column:1 -> 790x360 */
/* 右上: grid-row:1, grid-column:2 -> 390x170 */
/* 右下: grid-row:2, grid-column:2 -> 390x170 */
/* 底部横条: grid-row:3, grid-column:1/-1 -> 1200x180 */
```

## HTML 骨架（关键：主卡片跨行 + 底部横条跨列）

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:2fr 1fr; grid-template-rows:1fr 1fr auto; gap:20px;">

  <!-- 卡片 1: 主区域（左，跨前两行） -->
  <!-- ★ 必须写 grid-row: 1 / 3 ★ -->
  <div class="card" style="grid-row: 1 / 3; grid-column: 1;
       /* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-1);"></div>
      <h3 style="font-size:20px; font-weight:700; color:var(--text-primary);">核心论点</h3>
    </div>
    <!-- 主卡片：核心论述 + 主要数据可视化 -->
  </div>

  <!-- 卡片 2: 右上辅助 -->
  <div class="card" style="grid-row: 1; grid-column: 2;
       /* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-2);"></div>
      <h3 style="font-size:15px; font-weight:700; color:var(--text-primary);">辅助 A</h3>
    </div>
    <!-- 紧凑数据：KPI / 简要指标 -->
  </div>

  <!-- 卡片 3: 右下辅助 -->
  <div class="card" style="grid-row: 2; grid-column: 2;
       /* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-3);"></div>
      <h3 style="font-size:15px; font-weight:700; color:var(--text-primary);">辅助 B</h3>
    </div>
    <!-- 紧凑数据：环形图 / 进度指标 -->
  </div>

  <!-- 卡片 4: 底部横条（跨两列） -->
  <!-- ★ 必须写 grid-column: 1 / -1 ★ -->
  <div class="card" style="grid-row: 3; grid-column: 1 / -1;
       /* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:20px; display:flex; align-items:center; gap:24px; overflow:hidden;">
    <!-- 底部摘要条：标签云 / 要点总结 / 补充指标行 -->
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-4);"></div>
      <h3 style="font-size:15px; font-weight:700; color:var(--text-primary);">总结</h3>
    </div>
    <!-- 横向排列的标签/指标 -->
  </div>

</div>
```

## 易错点

| 错误 | 正确 |
|------|------|
| 主卡片没写 `grid-row: 1 / 3` | 必须写，否则只占一行 |
| 底部横条没写 `grid-column: 1 / -1` | 必须写，否则只占一列 |
| 所有卡片都不写 grid 位置 | L 型布局**每个卡片都需要明确的 grid-row + grid-column** |

## 设计要点

- 主卡片约 790x360，空间较大，适合核心论述 + 图表组合
- 右侧辅助卡片约 390x170，空间紧凑，用 padding:20px + gap:12px + 标题 15px
- 底部横条高度由内容决定（auto），适合放横向排列的标签云或指标行
