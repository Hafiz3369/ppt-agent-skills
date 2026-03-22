# diagram（图解块）

> 架构图/流程图/金字塔/中心辐射/分层/循环。推荐跨列使用。

## cards[] 中的 JSON 结构

```json
{
  "card_type": "diagram",
  "position": "full-width",
  "title": "技术架构",
  "diagram_type": "pyramid | flowchart | hub-spoke | layers | cycle",
  "nodes": [
    {"id": "1", "label": "节点名", "description": "描述（20字内）", "level": 1, "connects_to": ["2","3"]}
  ]
}
```

## 子类型设计要点

| diagram_type | 实现方式 | 推荐节点数 |
|-------------|---------|----------|
| pyramid | 梯形 div 逐层变宽，`clip-path:polygon()` | 3-5 层 |
| flowchart | flex/grid 排列 + SVG 连线箭头 | 4-8 步 |
| hub-spoke | 中心大圆(120px) + 周围小圆(80px) + SVG `<line>` | 1+4~6 |
| layers | 全宽 div 上下堆叠，颜色渐变 | 3-5 层 |
| cycle | 节点沿圆形排列，SVG 弧线连接 | 4-6 步 |

## 通用规则

- 节点间关系用内联 SVG 连线（禁止 CSS border 三角形）
- 文字标注全部用 HTML 元素（禁止 SVG `<text>`）
- 节点用 accent 色背景或边框
- 推荐 `grid-column: 1 / -1` 跨全宽
