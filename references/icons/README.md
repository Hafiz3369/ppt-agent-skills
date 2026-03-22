# 内联 SVG 图标库

> 图标设计风格来源：[Lucide Icons](https://lucide.dev/)（MIT 开源）。所有图标已转为管线安全的内联 SVG path data，不依赖 CDN/字体文件/外部引用。
>
> **使用方式**：复制图标 SVG 代码，嵌入卡片标题左侧或列表项前方。统一容器尺寸为 20x20px（标题旁）或 16x16px（列表项旁）。

## 使用规则

1. **卡片标题图标**：放在标题竖线右侧、文字左侧，gap=8px
2. **列表项图标**：替代圆点标记，gap=10px
3. **颜色**：统一使用 `var(--accent-1)` 或对应章节的 accent 色
4. **stroke-width**：标题旁用 2，小尺寸用 1.5
5. **禁止**：不要在一张卡片内使用超过 3 个不同图标（视觉混乱）

## 图标分类索引

| 分类 | 文件 | 包含图标 |
|------|------|---------|
| 数据 & 分析 | `data-analytics.md` | TrendingUp, TrendingDown, BarChart3, LineChart, PieChart, Database |
| 内容 & 概念 | `content-concepts.md` | Lightbulb, Target, CircleCheck, AlertTriangle, Star, Rocket, Shield |
| 流程 & 结构 | `process-structure.md` | Workflow, Layers, Settings, Network |
| 行业 & 场景 | `industry-scenarios.md` | Building, FlaskConical, Code, Globe, Users, DollarSign, HeartPulse, Clock, Trophy |

## 卡片标题中的使用示例

```html
<!-- 带图标的卡片标题 -->
<div style="font-size:14px; font-weight:700; color:var(--text-primary);
    display:flex; align-items:center; gap:8px;">
  <div style="width:3px; height:16px; border-radius:2px; background:var(--accent-1);"></div>
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent-1)"
      stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>
    <polyline points="16 7 22 7 22 13"/>
  </svg>
  增长趋势分析
</div>
```

```html
<!-- 带图标的列表项 -->
<div style="display:flex; align-items:flex-start; gap:10px; margin-bottom:10px;">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-1)"
      stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="min-width:16px; margin-top:2px;">
    <circle cx="12" cy="12" r="10"/>
    <path d="m9 12 2 2 4-4"/>
  </svg>
  <span style="font-size:13px; color:var(--text-secondary); line-height:1.6;">
    市场份额同比增长 12.3%，超越行业均值 3.5 个百分点
  </span>
</div>
```
