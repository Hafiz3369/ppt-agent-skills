# 活力彩虹 (vibrant_rainbow) -- "创意"感

适用场景：社交/娱乐平台、营销/推广材料、年轻品牌、创意方案

## JSON 定义

```json
{
  "style_name": "活力彩虹 (Vibrant Rainbow)",
  "style_id": "vibrant_rainbow",
  "background": { "primary": "#FFFFFF", "gradient_to": "#FFF7ED" },
  "card": { "gradient_from": "#FFFFFF", "gradient_to": "#FFF1E6", "border": "rgba(251,146,60,0.15)", "border_radius": 20 },
  "text": { "primary": "#1C1917", "secondary": "#57534E", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#F97316", "#EC4899"], "secondary": ["#8B5CF6", "#06B6D4"] },
  "font_family": "'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "多彩渐变色块、圆润大圆角、活力四溢的卡片配色（每张卡片可用不同 accent 色）" }
}
```

## CSS 变量

```css
:root {
  --bg-primary: #FFFFFF;
  --bg-secondary: #FFF7ED;
  --card-bg-from: #FFFFFF;
  --card-bg-to: #FFF1E6;
  --card-border: rgba(251,146,60,0.15);
  --card-radius: 20px;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --accent-1: #F97316;
  --accent-2: #EC4899;
  --accent-3: #8B5CF6;
  --accent-4: #06B6D4;
}
```

## 装饰 DNA -- "创意"感

| 装饰元素 | 实现方式 |
|---------|---------|
| 多彩渐变色块 | 每张卡片可使用不同 accent 色作为标题竖线/徽标颜色 |
| 圆润大圆角 | 卡片 `border-radius:20px`（比其他风格大一圈） |
| 彩色圆点标记 | 列表项用 4 种 accent 色交替的圆点（而非统一颜色） |
| 渐变标题 | 标题下划线用多色渐变（`linear-gradient(90deg, #F97316, #EC4899, #8B5CF6, #06B6D4)`） |
| 标签颜色 | tag_cloud 中每个标签随机使用不同 accent 色的边框 |
| 禁止 | 禁止阴影、禁止暗色调、禁止严肃的装饰线 |
| 整体感觉 | 明快、活泼、年轻，像 Instagram/TikTok 的品牌风格 |
