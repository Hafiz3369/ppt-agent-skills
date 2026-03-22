# 点阵图 Waffle Chart（百分比直觉化）

`chart_type: waffle`

```html
<div style="display:grid; grid-template-columns:repeat(10,1fr); gap:3px; width:100px;">
  <!-- 67 个填充点 + 33 个空点 = 67% -->
  <div style="width:8px; height:8px; border-radius:2px; background:var(--accent-1);"></div>
  <!-- 重复填充点... -->
  <div style="width:8px; height:8px; border-radius:2px; background:var(--card-bg-from);"></div>
  <!-- 重复空点... -->
</div>
```

10x10 = 100 格，填充数量 = 百分比值。比进度条更直觉。
