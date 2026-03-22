# 极简灰白 (minimal_gray) -- "学术论文"感

适用场景：学术/研究报告、法务/合规、咨询/顾问报告、数据分析

## JSON 定义

```json
{
  "style_name": "极简灰白 (Minimal Gray)",
  "style_id": "minimal_gray",
  "background": { "primary": "#FAFAFA", "gradient_to": "#F5F5F5" },
  "card": { "gradient_from": "#FFFFFF", "gradient_to": "#FAFAFA", "border": "rgba(0,0,0,0.08)", "border_radius": 8 },
  "text": { "primary": "#171717", "secondary": "#737373", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#171717", "#404040"], "secondary": ["#DC2626", "#B91C1C"] },
  "font_family": "'Inter', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "纯净无装饰、大量留白、精确排版、红色仅用于关键数据强调" }
}
```

## CSS 变量

```css
:root {
  --bg-primary: #FAFAFA;
  --bg-secondary: #F5F5F5;
  --card-bg-from: #FFFFFF;
  --card-bg-to: #FAFAFA;
  --card-border: rgba(0,0,0,0.08);
  --card-radius: 8px;
  --text-primary: #171717;
  --text-secondary: #737373;
  --accent-1: #171717;
  --accent-2: #404040;
  --accent-3: #DC2626;
  --accent-4: #B91C1C;
}
```

## 装饰 DNA -- "学术论文"感

| 装饰元素 | 实现方式 |
|---------|---------|
| 标题装饰 | **无装饰线**，标题用 font-weight:800 + 大号字自身的视觉重量即可 |
| 卡片边框 | **纯细线**（`border:1px solid rgba(0,0,0,0.08)`），无阴影，无圆角（`border-radius:4px`） |
| 分隔线 | **单线**（1px, `rgba(0,0,0,0.06)`） |
| 强调方式 | 只用红色（`--accent-3: #DC2626`）强调关键数据，其余全灰/黑 |
| 编号样式 | 小号数字 + 圆点（`8px 圆点, #171717`） |
| 禁止 | 禁止渐变、禁止光晕、禁止装饰 SVG、禁止彩色标签 |
| 整体感觉 | Helvetica 式的纯净，信息优先，零视觉噪音 |
