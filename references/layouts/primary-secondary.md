# 主次结合布局 (大 + 两小)

适用: 层级关系。**推荐：信息层次丰富时优先选择。** 一个核心论点 + 两个辅助数据。

## CSS Grid 定义

```css
.content-area {
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
}
/* 主: 790x580 (跨两行) | 辅1: 390x280 | 辅2: 390x280 */
```

## HTML 骨架（关键：主卡片必须写 grid-row: 1 / -1）

```html
<div class="content-area" style="position:absolute; left:40px; top:80px; width:1200px; height:580px;
     display:grid; grid-template-columns:2fr 1fr; grid-template-rows:1fr 1fr; gap:20px;">

  <!-- 卡片 1: 主区域（左，跨两行） -->
  <!-- ★ 必须写 grid-row: 1 / -1 ★ -->
  <div class="card" style="grid-row: 1 / -1;
       /* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-1);"></div>
      <h3 style="font-size:20px; font-weight:700; color:var(--text-primary);">核心论点</h3>
    </div>
    <!-- 主卡片内容：核心论述 + 数据可视化 + 详细解读 -->
  </div>

  <!-- 卡片 2: 右上辅助 -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-2);"></div>
      <h3 style="font-size:16px; font-weight:700; color:var(--text-primary);">辅助数据 A</h3>
    </div>
    <!-- 辅助卡片：KPI/环形图/简要数据 -->
  </div>

  <!-- 卡片 3: 右下辅助 -->
  <div class="card" style="/* ← card_style CSS (见 blocks/card-styles.md) */
       border-radius:12px;
       padding:24px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">
    <div style="display:flex; align-items:center; gap:8px;">
      <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-3);"></div>
      <h3 style="font-size:16px; font-weight:700; color:var(--text-primary);">辅助数据 B</h3>
    </div>
    <!-- 辅助卡片：KPI/列表/标签云 -->
  </div>

</div>
```

## 易错点

| 错误 | 正确 |
|------|------|
| 主卡片没写 `grid-row: 1 / -1` 导致只占一行 | 主卡片**必须**写 `grid-row: 1 / -1` 跨两行 |
| 辅助卡片写了 `grid-row` 导致布局崩溃 | 辅助卡片**不写** `grid-row`，自动排列即可 |

## 设计要点

- 主卡片（790px 宽）承载核心内容，辅助卡片（390px 宽、280px 高）承载补充数据
- 辅助卡片空间有限，内容要紧凑：标题 16px（比主卡片小），gap 14px（比主卡片小）
- 辅助卡片适合放 KPI、环形图、进度条等简洁数据展示
