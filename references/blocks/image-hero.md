# image_hero（大图+叠加文字块）

> 配图铺满区域 + 半透明遮罩 + 文字叠加。推荐跨列或跨行使用。

## cards[] 中的 JSON 结构

```json
{
  "card_type": "image_hero",
  "position": "top / full-width",
  "title": "核心标题（28-44px）",
  "subtitle": "补充说明（80字内，可选）",
  "image_prompt": "配图描述（用于生成配图）",
  "data_highlights": [
    {"value": "87%", "label": "市场渗透率"}
  ]
}
```

## 设计要点

- 配图 `object-fit:cover` 铺满卡片区域
- 遮罩层：真实 `<div>` 半透明渐变（禁止 mask-image）
- 文字层：标题大号 + 副标题 + 可选数据亮点条
- 卡片无内边距（图片贴边），文字层有 padding
- 圆角跟随卡片（border-radius:12px + overflow:hidden）
- 推荐 `grid-column: 1 / -1` 跨全宽，高度占内容区的 40-60%
