# quote（引用/金句块）

> 大段引用或核心观点，适合节奏舒缓。

## cards[] 中的 JSON 结构

```json
{
  "card_type": "quote",
  "position": "top / full-width",
  "content": "引用内容（50-150字）",
  "attribution": {"name": "人名", "title": "职位/机构"},
  "avatar": true
}
```

## 设计要点

- 引用文字 24-28px，font-weight:500，line-height:1.6
- 引号装饰：大号 div（80-120px `"` 字符），accent 色 15% 透明度
- 来源：头像(48px 圆形) + 姓名(16px 700) + 职位(13px secondary)
- 左侧 3px accent 竖线或居中排列均可
- 留白充足，组件内 padding 较大（32px+）
