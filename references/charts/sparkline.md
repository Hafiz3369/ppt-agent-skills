# 迷你折线图 Sparkline（趋势方向）

`chart_type: sparkline`

```html
<svg width="120" height="40" viewBox="0 0 120 40">
  <!-- 面积填充 -->
  <path d="M0,35 L20,28 L40,30 L60,20 L80,15 L100,10 L120,5 L120,40 L0,40 Z"
        fill="var(--accent-1)" opacity="0.1"/>
  <!-- 折线 -->
  <polyline points="0,35 20,28 40,30 60,20 80,15 100,10 120,5"
            fill="none" stroke="var(--accent-1)" stroke-width="2" stroke-linecap="round"/>
  <!-- 终点圆点 -->
  <circle cx="120" cy="5" r="3" fill="var(--accent-1)"/>
</svg>
```

用在数据数字旁边，占位小但信息量大。数据点坐标根据实际趋势调整 y 值（高=好 -> y 值小）。
