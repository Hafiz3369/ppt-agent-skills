# 对比柱（两项对比）

`chart_type: comparison_bar`

```html
<!-- 整个对比柱组件必须用容器包裹，分为图表区和标签区 -->
<div style="display:flex; flex-direction:column; gap:0;">
  <!-- 图表区：柱体 -->
  <div style="display:flex; gap:8px; align-items:flex-end; height:80px;">
    <div style="flex:1; border-radius:4px 4px 0 0; background:var(--card-bg-from);
                height:40%;">
    </div>
    <div style="flex:1; border-radius:4px 4px 0 0; background:var(--accent-1);
                height:80%;">
    </div>
  </div>
  <!-- 标签区：独立行，与柱体用 margin-top 隔开 -->
  <div style="display:flex; gap:8px; margin-top:8px;">
    <span style="flex:1; text-align:center; font-size:12px;
                 color:var(--text-secondary);">标签A</span>
    <span style="flex:1; text-align:center; font-size:12px;
                 color:var(--text-secondary);">标签B</span>
  </div>
</div>
```
