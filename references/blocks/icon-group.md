# icon_group（图标组块）

> 多图标+标题+描述的网格排列。推荐跨列使用。

## cards[] 中的 JSON 结构

```json
{
  "card_type": "icon_group",
  "position": "full-width",
  "title": "核心优势",
  "items": [
    {"icon": "Lightbulb", "icon_source": "content-concepts", "title": "特性名", "description": "描述（40-60字）"}
  ]
}
```

## 设计要点

- 内部 grid: `repeat(3, 1fr)` 或 `repeat(2, 1fr)`
- 每格：图标(40px SVG, accent 色) + 标题(18px 700) + 描述(13px secondary)
- 每格有 card-bg 背景 + 圆角 12px + padding 24px
- 图标从 `icons/*.md` 选取
- 4-9 个特性为宜
- 推荐 `grid-column: 1 / -1` 跨全宽
