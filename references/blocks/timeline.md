# timeline（时间线块）

> 横向或纵向时间线，4-8 个节点。推荐跨列使用。

## cards[] 中的 JSON 结构

```json
{
  "card_type": "timeline",
  "position": "top / full-width",
  "title": "发展历程",
  "orientation": "horizontal | vertical",
  "nodes": [
    {"time": "2020", "title": "事件标题", "description": "简述（30字内）", "highlight": false},
    {"time": "2022", "title": "里程碑", "description": "关键突破", "highlight": true}
  ]
}
```

## 设计要点

- 轴线：3px，accent 色 30% 透明度
- 节点：16px 圆点（highlight 用 accent 实心，普通用描边）
- 横向：描述交替上下排列增加层次感
- 纵向：左侧时间标签 + 右侧描述
- 4-8 个节点为宜，超过 8 个拆为多个 timeline 块或拆页
- 连线用真实 `<div>`（禁止伪元素），箭头用内联 SVG
- 推荐 `grid-column: 1 / -1` 跨全宽
