# 堆叠条形图（多分类占比对比）

`chart_type: stacked_bar`

用 CSS flex 横向堆叠，适合展示多个分类在总量中的占比。

```html
<div style="display:flex; flex-direction:column; gap:12px;">
  <!-- 条目1 -->
  <div>
    <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
      <span style="color:var(--text-primary); font-weight:600;">GPU 集群</span>
      <span style="color:var(--text-secondary);">$1,347B</span>
    </div>
    <div style="display:flex; height:16px; border-radius:4px; overflow:hidden;">
      <div style="width:47%; background:var(--accent-1);"></div>
      <div style="width:28%; background:var(--accent-2);"></div>
      <div style="width:15%; background:var(--accent-3);"></div>
      <div style="width:10%; background:rgba(255,255,255,0.1);"></div>
    </div>
  </div>
  <!-- 条目2 -->
  <div>
    <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
      <span style="color:var(--text-primary); font-weight:600;">训练平台</span>
      <span style="color:var(--text-secondary);">$800B</span>
    </div>
    <div style="display:flex; height:16px; border-radius:4px; overflow:hidden;">
      <div style="width:35%; background:var(--accent-1);"></div>
      <div style="width:40%; background:var(--accent-2);"></div>
      <div style="width:25%; background:var(--accent-3);"></div>
    </div>
  </div>
  <!-- 图例 -->
  <div style="display:flex; gap:16px; font-size:11px; color:var(--text-secondary); margin-top:4px;">
    <div style="display:flex; align-items:center; gap:4px;">
      <span style="width:10px; height:10px; border-radius:2px; background:var(--accent-1);"></span>北美
    </div>
    <div style="display:flex; align-items:center; gap:4px;">
      <span style="width:10px; height:10px; border-radius:2px; background:var(--accent-2);"></span>亚太
    </div>
    <div style="display:flex; align-items:center; gap:4px;">
      <span style="width:10px; height:10px; border-radius:2px; background:var(--accent-3);"></span>欧洲
    </div>
  </div>
</div>
```
