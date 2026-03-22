# 小米橙 (xiaomi_orange) -- "产品发布会"感

适用场景：硬件产品、IoT 设备、消费电子、智能家居

## JSON 定义

```json
{
  "style_name": "小米橙 (Xiaomi Orange)",
  "style_id": "xiaomi_orange",
  "background": { "primary": "#1A1A1A", "gradient_to": "#111111" },
  "card": { "gradient_from": "#2A2A2A", "gradient_to": "#1A1A1A", "border": "rgba(255,105,0,0.15)", "border_radius": 16 },
  "text": { "primary": "#FFFFFF", "secondary": "rgba(255,255,255,0.65)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#FF6900", "#FF8C00"], "secondary": ["#FFFFFF", "#E0E0E0"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "纯净简约，大面积留白，圆形图标元素" }
}
```

## CSS 变量

```css
:root {
  --bg-primary: #1A1A1A;
  --bg-secondary: #111111;
  --card-bg-from: #2A2A2A;
  --card-bg-to: #1A1A1A;
  --card-border: rgba(255,105,0,0.15);
  --card-radius: 16px;
  --text-primary: #FFFFFF;
  --text-secondary: rgba(255,255,255,0.65);
  --accent-1: #FF6900;
  --accent-2: #FF8C00;
  --accent-3: #FFFFFF;
  --accent-4: #E0E0E0;
}
```

## 装饰 DNA -- "产品发布会"感

| 装饰元素 | 实现方式 |
|---------|---------|
| 标题装饰 | 橙色细横线（2px 高, 40px 宽） |
| 卡片边框 | **无边框**，用微妙背景色差区分卡片和背景（卡片稍亮 5%） |
| 圆形图标载体 | 48px 圆形 + 10% 透明度橙色背景 + 居中 Lucide 图标（白色 stroke） |
| 留白 | 比其他风格增加 30% 内边距（padding:32px 而非 24px） |
| 产品数字 | 超大字号（80px+），极细字重旁边的单位小字（`font-weight:300`） |
| 禁止 | 禁止网格点阵、禁止角标线、禁止渐变色块（极简至上） |
| 整体感觉 | 黑底橙字，极致留白，每页只聚焦一个核心信息 |
