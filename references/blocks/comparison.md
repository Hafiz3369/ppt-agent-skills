# comparison（对比块）

> A vs B 双面板对比。推荐跨列使用。

## cards[] 中的 JSON 结构

```json
{
  "card_type": "comparison",
  "position": "full-width",
  "title": "传统方式 vs 新方案",
  "left": {"label": "方案A / 现状", "points": ["对比维度1", "对比维度2", "对比维度3"], "accent": "neutral"},
  "right": {"label": "方案B / 目标", "points": ["对比维度1", "对比维度2", "对比维度3"], "accent": "primary"},
  "verdict": "底部总结句（可选）"
}
```

## 设计要点

- 内部 grid: `grid-template-columns: 1fr 1fr; gap:0`
- 左面板中性色背景 + 左侧圆角，右面板 accent 边框/背景 + 右侧圆角
- 对比维度上下对齐，形成视觉对应
- 可选中间 VS 分隔符（圆形 div + "VS" 文字）
- 每面板 3-5 个对比维度
- verdict 跨两列居中
- 推荐 `grid-column: 1 / -1` 跨全宽
