# 紫金奢华 (luxury_purple) -- "高定"感

适用场景：时尚/奢侈品、高端服务/地产、设计/创意行业、品牌发布会

## JSON 定义

```json
{
  "style_name": "紫金奢华 (Luxury Purple)",
  "style_id": "luxury_purple",
  "background": { "primary": "#120A2E", "gradient_to": "#1A0B3D" },
  "card": { "gradient_from": "#2D1B69", "gradient_to": "#1A0B3D", "border": "rgba(192,132,252,0.1)", "border_radius": 12 },
  "text": { "primary": "#F5F3FF", "secondary": "rgba(245,243,255,0.7)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#A855F7", "#7C3AED"], "secondary": ["#F59E0B", "#D97706"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": true, "size": 50, "dot_radius": 1, "dot_color": "#A855F7", "dot_opacity": 0.03 },
  "decorations": { "corner_lines": true, "glow_effects": true, "description": "紫色光晕、金色点缀、钻石切割线条装饰，极致奢华感" }
}
```

## CSS 变量

```css
:root {
  --bg-primary: #120A2E;
  --bg-secondary: #1A0B3D;
  --card-bg-from: #2D1B69;
  --card-bg-to: #1A0B3D;
  --card-border: rgba(192,132,252,0.1);
  --card-radius: 12px;
  --text-primary: #F5F3FF;
  --text-secondary: rgba(245,243,255,0.7);
  --accent-1: #A855F7;
  --accent-2: #7C3AED;
  --accent-3: #F59E0B;
  --accent-4: #D97706;
}
```

## 装饰 DNA -- "高定"感

| 装饰元素 | 实现方式 |
|---------|---------|
| 紫色光晕 | 大面积 radial-gradient，紫色 5% 透明度，比暗黑科技更弥漫 |
| 金色点缀 | 数据数字用 `--accent-3`（金色 #F59E0B），标签边框用金色 10% |
| 钻石切割线 | 菱形 SVG pattern 作为底部装饰条（45度旋转的小方块连续排列） |
| 卡片效果 | `box-shadow:0 4px 24px rgba(0,0,0,0.3)` 强阴影营造浮起效果 |
| 编号样式 | 金色描边圆圈内数字（`border:2px solid #F59E0B; border-radius:50%`） |
| 禁止 | 禁止大面积白色/浅色区域（破坏奢华暗调） |
| 整体感觉 | 深紫 + 金色的极致奢华，每个细节都有"重量感" |
