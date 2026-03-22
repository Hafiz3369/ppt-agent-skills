# 矩形树图 Treemap（层级结构占比）

`chart_type: treemap`

用 CSS grid 模拟，适合展示有层级关系的面积对比。

```html
<div style="display:grid; grid-template-columns:3fr 2fr; grid-template-rows:3fr 2fr; gap:3px;
    height:160px; border-radius:8px; overflow:hidden;">
  <!-- 最大块 -->
  <div style="background:var(--accent-1); padding:10px; display:flex; flex-direction:column;
      justify-content:flex-end; grid-row:1/3;">
    <div style="font-size:20px; font-weight:800; color:var(--bg-primary);">47.3%</div>
    <div style="font-size:11px; color:rgba(0,0,0,0.6);">GPU 集群</div>
  </div>
  <!-- 第二大 -->
  <div style="background:var(--accent-2); padding:8px; display:flex; flex-direction:column;
      justify-content:flex-end;">
    <div style="font-size:16px; font-weight:700; color:white;">28.1%</div>
    <div style="font-size:10px; color:rgba(255,255,255,0.7);">训练平台</div>
  </div>
  <!-- 第三 -->
  <div style="background:var(--accent-3); padding:8px; display:flex; flex-direction:column;
      justify-content:flex-end;">
    <div style="font-size:14px; font-weight:700; color:var(--bg-primary);">15.6%</div>
    <div style="font-size:10px; color:rgba(0,0,0,0.5);">推理服务</div>
  </div>
</div>
```

面积比例通过 `grid-template-columns` 和 `grid-template-rows` 的 fr 值控制。
