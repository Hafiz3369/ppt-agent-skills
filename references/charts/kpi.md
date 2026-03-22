# KPI 指标卡（数字+趋势箭头+标签）

`chart_type: kpi`

```html
<div style="display:flex; align-items:baseline; gap:8px;">
  <span style="font-size:40px; font-weight:800; color:var(--accent-1);
               font-variant-numeric:tabular-nums;">2.4M</span>
  <!-- 上升箭头（绿色=好） -->
  <svg width="16" height="16" viewBox="0 0 16 16">
    <polygon points="8,2 14,10 2,10" fill="#16A34A"/>
  </svg>
  <span style="font-size:14px; color:#16A34A; font-weight:600;">+12.3%</span>
</div>
<div style="font-size:12px; color:var(--text-secondary); margin-top:4px;">月活跃用户数</div>
```

趋势箭头颜色：上升用绿色 #16A34A，下降用红色 #DC2626，持平用 text-secondary。
