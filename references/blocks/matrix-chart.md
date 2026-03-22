# matrix_chart（象限矩阵块）

> 2x2 象限图。推荐跨列跨行使用。

## cards[] 中的 JSON 结构

```json
{
  "card_type": "matrix_chart",
  "position": "center / full-width",
  "title": "市场定位分析",
  "x_label": "X轴含义（如：执行难度）",
  "y_label": "Y轴含义（如：业务价值）",
  "quadrants": [
    {"position": "top-right", "title": "优先执行", "items": ["项目A","项目B"], "highlight": true},
    {"position": "top-left", "title": "长期投资", "items": ["项目C"], "highlight": false},
    {"position": "bottom-right", "title": "快速见效", "items": ["项目D"], "highlight": false},
    {"position": "bottom-left", "title": "低优先级", "items": ["项目E"], "highlight": false}
  ]
}
```

## 设计要点

- 十字轴：2px 线，text-secondary 20% 透明度
- 轴标签在四端（12px，letter-spacing:1px）
- 象限用不同透明度区分（highlight 15%，其他 5%）
- 象限标题 16px 700，项目用胶囊标签
- 整体居中，推荐 `grid-column: 1 / -1; grid-row: 1 / -1` 跨全幅
