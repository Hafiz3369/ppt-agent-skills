# 朱红宫墙 (royal_red) -- "国风"感

适用场景：文化/历史主题、政务汇报、品牌故事、中国风

## JSON 定义

```json
{
  "style_name": "朱红宫墙 (Royal Red)",
  "style_id": "royal_red",
  "background": { "primary": "#8B0000", "gradient_to": "#5C0000" },
  "card": { "gradient_from": "#A52A2A", "gradient_to": "#7A0000", "border": "rgba(255,215,0,0.15)", "border_radius": 8 },
  "text": { "primary": "#FFF8E7", "secondary": "rgba(255,248,231,0.75)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#FFD700", "#FFA500"], "secondary": ["#FFF8E7", "#F5E6C8"] },
  "font_family": "PingFang SC, STSong, SimSun, Microsoft YaHei, serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": true, "glow_effects": false, "description": "金色角饰、祥云纹理，传统纹样装饰边框" }
}
```

## CSS 变量

```css
:root {
  --bg-primary: #8B0000;
  --bg-secondary: #5C0000;
  --card-bg-from: #A52A2A;
  --card-bg-to: #7A0000;
  --card-border: rgba(255,215,0,0.15);
  --card-radius: 8px;
  --text-primary: #FFF8E7;
  --text-secondary: rgba(255,248,231,0.75);
  --accent-1: #FFD700;
  --accent-2: #FFA500;
  --accent-3: #FFF8E7;
  --accent-4: #F5E6C8;
}
```

## 装饰 DNA -- "国风"感

| 装饰元素 | 实现方式 |
|---------|---------|
| 金色角饰 | 内联 SVG 中式角纹（L 形 + 回纹细节），放在页面四角和卡片角落 |
| 祥云纹理 | 内联 SVG 祥云纹样，6-8% 透明度作为页面底部装饰 |
| 印章编号 | 方框内数字（`border:2px solid #FFD700; border-radius:4px; padding:4px 8px`）模拟印章效果 |
| 分隔线 | 金色渐隐线（`linear-gradient(90deg, transparent, #FFD700, transparent)` 30% opacity） |
| 标题装饰 | 标题左侧竖线加粗到 4px，使用金色 |
| 字体偏好 | 衬线字体优先（`STSong, SimSun` 排在 font-family 前面给中文优雅的书法感） |
| 禁止 | 禁止科技感元素（网格点阵/光晕/角标线）、禁止蓝色/紫色系颜色 |
| 整体感觉 | 故宫红墙 + 金色浮雕的庄重感，传统中有精致 |
