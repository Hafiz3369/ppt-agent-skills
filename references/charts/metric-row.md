# 指标行（数字+标签+进度条 组合）

辅助组件，可与其他图表搭配使用。

```html
<div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
  <span style="font-size:24px; font-weight:800; color:var(--accent-1);
               font-variant-numeric:tabular-nums; min-width:60px;">87%</span>
  <div style="flex:1;">
    <div style="font-size:12px; color:var(--text-secondary); margin-bottom:4px;">用户满意度</div>
    <div class="progress-bar"><div class="fill" style="width:87%"></div></div>
  </div>
</div>
```
