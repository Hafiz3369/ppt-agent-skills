# 雷达图 / 蜘蛛网图（多维度对比）

`chart_type: radar`

用 SVG polygon 绘制。适合展示 3-6 个维度的能力/指标对比。

```html
<div style="position:relative; width:200px; height:200px;">
  <svg width="200" height="200" viewBox="0 0 200 200">
    <!-- 网格线（3层） -->
    <polygon points="100,20 166,55 166,145 100,180 34,145 34,55"
             fill="none" stroke="var(--card-border)" stroke-width="1"/>
    <polygon points="100,47 144,68 144,132 100,153 56,132 56,68"
             fill="none" stroke="var(--card-border)" stroke-width="1"/>
    <polygon points="100,73 122,82 122,118 100,127 78,118 78,82"
             fill="none" stroke="var(--card-border)" stroke-width="1"/>
    <!-- 轴线 -->
    <line x1="100" y1="20" x2="100" y2="180" stroke="var(--card-border)" stroke-width="1"/>
    <line x1="34" y1="55" x2="166" y2="145" stroke="var(--card-border)" stroke-width="1"/>
    <line x1="34" y1="145" x2="166" y2="55" stroke="var(--card-border)" stroke-width="1"/>
    <!-- 数据区域 -->
    <polygon points="100,35 155,65 150,140 100,165 50,120 45,60"
             fill="var(--accent-1)" opacity="0.15"
             stroke="var(--accent-1)" stroke-width="2"/>
    <!-- 数据点 -->
    <circle cx="100" cy="35" r="4" fill="var(--accent-1)"/>
    <circle cx="155" cy="65" r="4" fill="var(--accent-1)"/>
    <circle cx="150" cy="140" r="4" fill="var(--accent-1)"/>
    <circle cx="100" cy="165" r="4" fill="var(--accent-1)"/>
    <circle cx="50" cy="120" r="4" fill="var(--accent-1)"/>
    <circle cx="45" cy="60" r="4" fill="var(--accent-1)"/>
  </svg>
  <!-- 维度标签用 HTML 叠加（禁止 SVG text） -->
  <span style="position:absolute; top:2px; left:50%; transform:translateX(-50%);
      font-size:11px; color:var(--text-secondary);">性能</span>
  <span style="position:absolute; top:22%; right:5%; font-size:11px; color:var(--text-secondary);">安全</span>
  <span style="position:absolute; bottom:22%; right:5%; font-size:11px; color:var(--text-secondary);">成本</span>
  <span style="position:absolute; bottom:2px; left:50%; transform:translateX(-50%);
      font-size:11px; color:var(--text-secondary);">易用</span>
  <span style="position:absolute; bottom:22%; left:5%; font-size:11px; color:var(--text-secondary);">扩展</span>
  <span style="position:absolute; top:22%; left:5%; font-size:11px; color:var(--text-secondary);">生态</span>
</div>
```

维度标签坐标需根据多边形顶点位置微调。6 维以上不推荐（标签太挤）。
