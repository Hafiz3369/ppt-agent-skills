# 漏斗图 Funnel（转化流程）

`chart_type: funnel`

用 CSS 宽度递减模拟漏斗，适合销售漏斗、转化率、筛选流程。

```html
<div style="display:flex; flex-direction:column; align-items:center; gap:2px;">
  <!-- 第1层（最宽） -->
  <div style="width:100%; height:40px; background:var(--accent-1); border-radius:4px;
      display:flex; align-items:center; justify-content:space-between; padding:0 16px;">
    <span style="font-size:13px; font-weight:600; color:var(--bg-primary);">访问用户</span>
    <span style="font-size:16px; font-weight:800; color:var(--bg-primary);">100,000</span>
  </div>
  <!-- 第2层 -->
  <div style="width:78%; height:40px; background:var(--accent-2); border-radius:4px;
      display:flex; align-items:center; justify-content:space-between; padding:0 16px;">
    <span style="font-size:13px; font-weight:600; color:white;">注册用户</span>
    <span style="font-size:16px; font-weight:800; color:white;">42,000</span>
  </div>
  <!-- 第3层 -->
  <div style="width:52%; height:40px; background:var(--accent-3); border-radius:4px;
      display:flex; align-items:center; justify-content:space-between; padding:0 14px;">
    <span style="font-size:12px; font-weight:600; color:var(--bg-primary);">付费用户</span>
    <span style="font-size:15px; font-weight:800; color:var(--bg-primary);">12,600</span>
  </div>
  <!-- 第4层（最窄） -->
  <div style="width:30%; height:40px; background:var(--accent-4); border-radius:4px;
      display:flex; align-items:center; justify-content:center; padding:0 12px; gap:8px;">
    <span style="font-size:12px; font-weight:600; color:var(--bg-primary);">VIP</span>
    <span style="font-size:15px; font-weight:800; color:var(--bg-primary);">3,780</span>
  </div>
  <!-- 转化率标注 -->
  <div style="display:flex; gap:24px; margin-top:8px; font-size:11px; color:var(--text-secondary);">
    <span>注册率 42%</span>
    <span>付费率 30%</span>
    <span>VIP 率 30%</span>
  </div>
</div>
```

每层宽度按实际转化比例递减。颜色用 accent-1 到 accent-4 递进。
