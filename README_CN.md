# PPT Agent Skill

**[English](README.md)**

> 模仿万元/页级别 PPT 设计公司的完整工作流，输出高质量 HTML 演示文稿 + 可编辑矢量 PPTX。

## 工作流概览

```
需求调研 → 资料搜集 → 大纲策划 → 策划稿 → 风格+配图+HTML设计稿 → 后处理(SVG+PPTX)
```

## 核心特性

| 特性 | 说明 |
|------|------|
| **6步Pipeline** | 需求 → 搜索 → 大纲 → 策划 → 设计 → 后处理，模拟专业 PPT 公司工作流 |
| **8种预置风格** | 暗黑科技 / 小米橙 / 蓝白商务 / 朱红宫墙 / 清新自然 / 紫金奢华 / 极简灰白 / 活力彩虹 |
| **Bento Grid 布局** | 7 种卡片式灵活布局，内容驱动版式 |
| **智能配图** | AI 生成配图 + 5 种视觉融入技法（渐隐融合/色调蒙版/氛围底图等） |
| **排版系统** | 7 级字号阶梯 + 间距层级 + 中英文混排规则 |
| **色彩比例** | 60-30-10 法则 + accent 色使用约束 |
| **数据可视化** | 8 种纯 CSS/SVG 图表（进度条/环形图/迷你折线/点阵图/KPI 卡等） |
| **跨页叙事** | 密度交替节奏 / 章节色彩递进 / 封面-结尾呼应 / 渐进揭示 |
| **页脚系统** | 统一页脚（章节信息 + 页码），跨页导航 |
| **PPTX 兼容** | HTML → SVG → PPTX 管线，PPT 365 中右键"转换为形状"即可编辑 |

## 输出产物

| 文件 | 说明 |
|------|------|
| `preview.html` | 浏览器翻页预览（自动生成） |
| `presentation.pptx` | PPTX 文件，PPT 365 中右键"转换为形状"可编辑 |
| `svg/*.svg` | 单页矢量 SVG，可直接拖入 PPT |
| `slides/*.html` | 单页 HTML 源文件 |

## 环境依赖

**必须：**
- **Node.js** >= 18（Puppeteer + dom-to-svg）
- **Python** >= 3.8
- **python-pptx**（PPTX 生成）

**一键安装：**
```bash
pip install python-pptx lxml Pillow
npm install puppeteer dom-to-svg
```

## 目录结构

```
ppt-agent-skill/
  SKILL.md                    # 主工作流指令（Agent 入口）
  README.md                   # English documentation
  README_CN.md                # 本文件
  references/
    prompts.md                # 5 套 Prompt 模板
    style-system.md           # 8 种预置风格 + CSS 变量
    bento-grid.md             # 7 种布局规格 + 卡片类型
    method.md                 # 核心方法论
  scripts/
    html_packager.py          # 多页 HTML 合并为翻页预览
    html2svg.py               # HTML → SVG（dom-to-svg，保留文字可编辑）
    svg2pptx.py               # SVG → PPTX（OOXML 原生 SVG 嵌入）
```

## 脚本用法

```bash
# 合并预览
python3 scripts/html_packager.py <slides_dir> -o preview.html

# HTML 转 SVG
python3 scripts/html2svg.py <slides_dir> -o <svg_dir>

# SVG 转 PPTX
python3 scripts/svg2pptx.py <svg_dir> -o output.pptx --html-dir <slides_dir>
```

## 触发方式

在对话中，以下表达会触发此 Skill：

- "帮我做个 PPT" / "做一个关于 X 的演示"
- "做 slides" / "做幻灯片" / "做汇报材料"
- "把这篇文档做成 PPT" / "做培训课件" / "做路演 deck"

## 许可证

[MIT](LICENSE)
