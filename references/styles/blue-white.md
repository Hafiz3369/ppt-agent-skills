# 蓝白商务 (blue_white) -- 最通用的默认风格

适用场景：企业介绍、培训课件、教育材料、医疗/金融行业、一般性汇报、未明确指定风格的大多数场景

## JSON 定义

```json
{
  "style_name": "蓝白商务 (Blue White Business)",
  "style_id": "blue_white",
  "background": { "primary": "#FFFFFF", "gradient_to": "#F8FAFC" },
  "card": { "gradient_from": "#F1F5F9", "gradient_to": "#E2E8F0", "border": "rgba(37,99,235,0.12)", "border_radius": 12 },
  "text": { "primary": "#1E293B", "secondary": "#64748B", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#2563EB", "#1D4ED8"], "secondary": ["#059669", "#047857"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "清爽简洁，蓝色标题装饰条，卡片带浅色背景和细边框" }
}
```

## CSS 变量

```css
:root {
  --bg-primary: #FFFFFF;
  --bg-secondary: #F8FAFC;
  --card-bg-from: #F1F5F9;
  --card-bg-to: #E2E8F0;
  --card-border: rgba(37,99,235,0.12);
  --card-radius: 12px;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --accent-1: #2563EB;
  --accent-2: #1D4ED8;
  --accent-3: #059669;
  --accent-4: #047857;
}
```

## 装饰 DNA -- "McKinsey 报告"感

| 装饰元素 | 实现方式 |
|---------|---------|
| 标题装饰 | **蓝色渐变横条**放在标题下方（4px 高, 80px 宽, `linear-gradient(90deg, #2563EB, #1D4ED8)`） |
| 卡片边框 | **细线边框**（`border:1px solid rgba(37,99,235,0.12)`）+ **微妙阴影**（`box-shadow:0 1px 3px rgba(0,0,0,0.05)`） |
| 分隔线 | **双细线分隔**（两条 1px 线，间距 3px，颜色 `rgba(0,0,0,0.06)`） |
| 编号样式 | 蓝色实心方块编号（`border-radius:4px`，不是圆形） |
| 禁止 | 禁止光晕效果、禁止网格点阵、禁止角标装饰线（太"科技感"） |
| 整体感觉 | 干净、可信、机构级专业感，像一份顶级咨询公司的正式报告 |
