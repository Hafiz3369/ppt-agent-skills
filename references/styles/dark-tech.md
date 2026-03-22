# 暗黑科技 (dark_tech) -- "发布会"感

适用场景：技术产品发布、开发者工具演示、AI/ML 模型展示。注意：仅当主题**明确**是技术产品展示、开发者工具、深度技术架构讲解时才选用。

## JSON 定义

```json
{
  "style_name": "暗黑科技 (Dark Tech)",
  "style_id": "dark_tech",
  "background": { "primary": "#0B1120", "gradient_to": "#0F172A" },
  "card": { "gradient_from": "#1E293B", "gradient_to": "#0F172A", "border": "rgba(255,255,255,0.05)", "border_radius": 12 },
  "text": { "primary": "#FFFFFF", "secondary": "rgba(255,255,255,0.7)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#22D3EE", "#3B82F6"], "secondary": ["#FDE047", "#F59E0B"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": true, "size": 40, "dot_radius": 1, "dot_color": "#FFFFFF", "dot_opacity": 0.05 },
  "decorations": { "corner_lines": true, "glow_effects": true, "description": "角落装饰线条 + 强调色模糊光晕" }
}
```

## CSS 变量

```css
:root {
  --bg-primary: #0B1120;
  --bg-secondary: #0F172A;
  --card-bg-from: #1E293B;
  --card-bg-to: #0F172A;
  --card-border: rgba(255,255,255,0.05);
  --card-radius: 12px;
  --text-primary: #FFFFFF;
  --text-secondary: rgba(255,255,255,0.7);
  --accent-1: #22D3EE;
  --accent-2: #3B82F6;
  --accent-3: #FDE047;
  --accent-4: #F59E0B;
}
```

## 装饰 DNA -- "发布会"感

| 装饰元素 | 实现方式 |
|---------|---------|
| 网格点阵 | `radial-gradient(circle, rgba(255,255,255,0.03) 1px, transparent 1px), background-size:40px 40px` |
| 角标装饰线 | L 形 SVG path（`border-top + border-left`），accent 色 20% 透明度 |
| 光晕效果 | radial-gradient 超大半透明圆(400-600px)，accent 色 5-8% 透明度 |
| 半透明数字水印 | 120-160px 超大数字，accent 色 opacity 0.03-0.05 |
| 卡片分隔线 | 1px solid rgba(255,255,255,0.05) |
| 脉冲圆点 | 6px accent 色圆点 + 外圈 14px 10% 透明度圆环（双圈效果） |
| 整体感觉 | 深空科技、精密仪器感，像 Apple/NVIDIA 的产品发布会 |
