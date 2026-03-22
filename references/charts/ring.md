# 环形百分比（必须用内联 SVG，禁止 conic-gradient）

`chart_type: ring`

> **管线兼容**：中心文字用 HTML position:absolute 叠加，禁止在 SVG 中写 `<text>` 元素（见 `pipeline-compat.md` 2.3 节）。

```html
<div style="position:relative; width:80px; height:80px;">
  <svg width="80" height="80" viewBox="0 0 80 80">
    <circle cx="40" cy="40" r="32" fill="none"
            stroke="var(--card-bg-from)" stroke-width="10"/>
    <circle cx="40" cy="40" r="32" fill="none"
            stroke="var(--accent-1)" stroke-width="10"
            stroke-dasharray="180.96 201.06" stroke-linecap="round"
            transform="rotate(-90 40 40)"/>
  </svg>
  <!-- 中心文字用 HTML 叠加，不用 SVG text -->
  <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
      font-size:16px; font-weight:700; color:var(--text-primary);">90%</div>
</div>
```

计算公式: dasharray 第一个值 = 2 * PI * r * (百分比/100), 第二个值 = 2 * PI * r
