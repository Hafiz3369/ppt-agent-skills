# people（人物组块）

> 多人物头像+姓名+职位排列。推荐跨列使用。

## cards[] 中的 JSON 结构

```json
{
  "card_type": "people",
  "position": "full-width",
  "title": "核心团队",
  "members": [
    {"name": "姓名", "title": "职位", "bio": "简介（30字内）", "avatar": true}
  ]
}
```

## 设计要点

- 内部 grid: `repeat(N, 1fr)`，3-4 人一行
- 头像 80px 圆形裁切，`border:3px solid var(--accent-1)`
- 无头像时：首字母占位圆（accent 背景 + 白色字母 32px）
- 姓名 16px 700 居中 + 职位 13px accent + 简介 12px secondary
- 3-8 人为宜
- 推荐 `grid-column: 1 / -1` 跨全宽
