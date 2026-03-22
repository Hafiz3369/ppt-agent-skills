# 清新自然 (fresh_green) -- "有机"感

适用场景：环保/可持续发展、健康/医疗/养生、食品/农业、美妆/护肤

## JSON 定义

```json
{
  "style_name": "清新自然 (Fresh Green)",
  "style_id": "fresh_green",
  "background": { "primary": "#F0FDF4", "gradient_to": "#ECFDF5" },
  "card": { "gradient_from": "#FFFFFF", "gradient_to": "#F0FDF4", "border": "rgba(22,163,74,0.12)", "border_radius": 16 },
  "text": { "primary": "#14532D", "secondary": "#4B5563", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#16A34A", "#059669"], "secondary": ["#F59E0B", "#D97706"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "轻柔圆角、叶片图标、自然渐变色块，清新透气感" }
}
```

## CSS 变量

```css
:root {
  --bg-primary: #F0FDF4;
  --bg-secondary: #ECFDF5;
  --card-bg-from: #FFFFFF;
  --card-bg-to: #F0FDF4;
  --card-border: rgba(22,163,74,0.12);
  --card-radius: 16px;
  --text-primary: #14532D;
  --text-secondary: #4B5563;
  --accent-1: #16A34A;
  --accent-2: #059669;
  --accent-3: #F59E0B;
  --accent-4: #D97706;
}
```

## 装饰 DNA -- "有机"感

| 装饰元素 | 实现方式 |
|---------|---------|
| 叶片装饰 | 内联 SVG 叶片（`path d="M12 22c4-4 8-8 8-12A8 8 0 0 0 4 10c0 4 4 8 8 12z"`），放在页面角落或卡片装饰 |
| 波浪分隔线 | SVG path 波浪线替代直线分隔（`path d="M0,8 Q30,0 60,8 Q90,16 120,8" stroke="#16A34A" stroke-width="1.5" fill="none"`） |
| 卡片边框 | 圆角加大到 16px，边框用绿色低透明度 |
| 编号样式 | 叶片形状内的数字（用 SVG 叶片 + HTML 叠加数字） |
| 背景渐变 | 极浅的绿到白渐变（`linear-gradient(180deg, #F0FDF4, #FFFFFF)`） |
| 禁止 | 禁止直角、禁止深色阴影、禁止冷色调元素 |
| 整体感觉 | 阳光透过树叶的温暖感，圆润柔和，适合健康/环保主题 |
