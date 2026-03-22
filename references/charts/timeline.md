# 时间轴 Timeline（水平版）

`chart_type: timeline`

用 flex 水平排列，适合展示历史沿革、产品迭代、项目里程碑。

```html
<div style="display:flex; flex-direction:column; gap:0;">
  <!-- 时间轴线 + 节点 -->
  <div style="display:flex; align-items:center; padding:0 20px;">
    <div style="flex:1; height:2px; background:rgba(255,255,255,0.1);"></div>
    <div style="width:12px; height:12px; border-radius:50%; background:var(--accent-1);
        border:3px solid var(--bg-primary); margin:0 -1px; position:relative; z-index:1;"></div>
    <div style="flex:1; height:2px; background:rgba(255,255,255,0.1);"></div>
    <div style="width:12px; height:12px; border-radius:50%; background:var(--accent-2);
        border:3px solid var(--bg-primary); margin:0 -1px; position:relative; z-index:1;"></div>
    <div style="flex:1; height:2px; background:rgba(255,255,255,0.1);"></div>
    <div style="width:12px; height:12px; border-radius:50%; background:var(--accent-3);
        border:3px solid var(--bg-primary); margin:0 -1px; position:relative; z-index:1;"></div>
    <div style="flex:1; height:2px; background:rgba(255,255,255,0.1);"></div>
    <div style="width:14px; height:14px; border-radius:50%; background:var(--accent-4);
        border:3px solid var(--bg-primary); margin:0 -1px; position:relative; z-index:1;"></div>
    <div style="flex:1; height:2px; background:rgba(255,255,255,0.1);"></div>
  </div>
  <!-- 标签行 -->
  <div style="display:flex; margin-top:12px; text-align:center;">
    <div style="flex:1; padding:0 8px;">
      <div style="font-size:13px; font-weight:700; color:var(--accent-1);">2020</div>
      <div style="font-size:11px; color:var(--text-secondary); margin-top:4px; line-height:1.4;">
        单卡训练<br>参数 &lt; 1B
      </div>
    </div>
    <div style="flex:1; padding:0 8px;">
      <div style="font-size:13px; font-weight:700; color:var(--accent-2);">2022</div>
      <div style="font-size:11px; color:var(--text-secondary); margin-top:4px; line-height:1.4;">
        千卡集群<br>100B+ 参数
      </div>
    </div>
    <div style="flex:1; padding:0 8px;">
      <div style="font-size:13px; font-weight:700; color:var(--accent-3);">2024</div>
      <div style="font-size:11px; color:var(--text-secondary); margin-top:4px; line-height:1.4;">
        超算融合<br>MoE 1T+
      </div>
    </div>
    <div style="flex:1; padding:0 8px;">
      <div style="font-size:13px; font-weight:700; color:var(--accent-4);">2026</div>
      <div style="font-size:11px; color:var(--text-secondary); margin-top:4px; line-height:1.4;">
        边缘智能<br>端云协同
      </div>
    </div>
  </div>
</div>
```

最后一个节点稍大（14px vs 12px）突出"当前/未来"状态。
