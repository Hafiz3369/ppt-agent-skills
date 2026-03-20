# PPT Agent Skill

**[English](#english) | [中文](#中文)**

---

<a id="english"></a>

## English

> A professional AI-powered presentation generation assistant that simulates the complete workflow of a top-tier PPT design company (quoted at $1,000+/page), outputting high-quality HTML presentations + editable vector PPTX files.

### Workflow Overview

```
Requirements Interview → Research → Outline → Planning Draft → Style + Images + HTML Design → Post-processing (SVG + PPTX)
```

### Key Features

| Feature | Description |
|---------|-------------|
| **5-Step Pipeline** | Requirements → Research → Outline → Planning → Design, mimicking professional PPT companies |
| **8 Preset Styles** | Dark Tech / Xiaomi Orange / Blue White / Royal Red / Fresh Green / Luxury Purple / Minimal Gray / Vibrant Rainbow |
| **Bento Grid Layout** | 7 flexible card-based layouts driven by content, not templates |
| **Smart Illustrations** | AI-generated images with 5 visual fusion techniques (fade blend, tinted overlay, ambient background, etc.) |
| **Typography System** | 7-level font scale + spacing hierarchy + Chinese-English mixed typesetting rules |
| **Color Proportion** | 60-30-10 rule enforcement + accent color constraints |
| **Data Visualization** | 8 pure CSS/SVG chart types (progress bars, ring charts, sparklines, waffle charts, KPI cards, etc.) |
| **Cross-page Narrative** | Density alternation, chapter color progression, cover-ending visual echo |
| **Footer System** | Unified footer with chapter info + page numbers across all slides |
| **PPTX Compatible** | HTML → SVG → PPTX pipeline, right-click "Convert to Shape" in PPT 365 for full editing |

### Output Files

| File | Description |
|------|-------------|
| `preview.html` | Browser-based paginated preview (auto-generated) |
| `presentation.pptx` | PPTX file, right-click "Convert to Shape" in PPT 365 for editing |
| `svg/*.svg` | Per-page vector SVG, drag into PPT directly |
| `slides/*.html` | Per-page HTML source files |

### Requirements

#### Required

- **Node.js** >= 18 (Puppeteer + dom-to-svg)
- **Python** >= 3.8 (script execution)
- **python-pptx** (PPTX generation)

#### Auto-installed (on first run)

- `puppeteer` — Headless Chrome
- `dom-to-svg` — DOM to SVG conversion (preserves editable `<text>`)
- `esbuild` — Bundles dom-to-svg for browser use

#### Quick Install

```bash
# Python dependencies
pip install python-pptx lxml Pillow

# Node.js dependencies (auto-installed on first script run, or install manually)
npm install puppeteer dom-to-svg
```

### Directory Structure

```
ppt-agent-skill/
  SKILL.md                    # Main workflow instructions (Agent entry point)
  README.md                   # This file
  references/
    prompts.md                # 5 Prompt templates
    style-system.md           # 8 preset styles + CSS variables
    bento-grid.md             # 7 layout specs + card types
    method.md                 # Core methodology
  scripts/
    html_packager.py          # Merge multi-page HTML into paginated preview
    html2svg.py               # HTML → SVG (dom-to-svg, preserves editable text)
    svg2pptx.py               # SVG → PPTX (OOXML native SVG embedding)
```

### Script Usage

```bash
# Merge preview
python3 scripts/html_packager.py <slides_dir> -o preview.html

# HTML to SVG
python3 scripts/html2svg.py <slides_dir> -o <svg_dir>

# SVG to PPTX
python3 scripts/svg2pptx.py <svg_dir> -o output.pptx --html-dir <slides_dir>
```

### Technical Architecture

```
HTML slides
  |
  v
[Puppeteer] opens HTML → [dom-to-svg] DOM direct to SVG
  |                         (preserves <text> elements, editable)
  |                         (base64 inline images)
  v
SVG files
  |
  v
[python-pptx + lxml] OOXML svgBlip embedding
  |                    (PNG fallback for older Office)
  v
presentation.pptx
```

### Trigger Phrases

In a Claude conversation, these expressions will trigger this Skill:

- "Help me make a PPT" / "Create a presentation about X"
- "Make slides" / "Make a deck" / "Make training materials"
- "Turn this document into a PPT"

---

<a id="中文"></a>

## 中文

> 模仿万元/页级别 PPT 设计公司的完整工作流，输出高质量 HTML 演示文稿 + 可编辑矢量 PPTX。

### 工作流概览

```
需求调研 → 资料搜集 → 大纲策划 → 策划稿 → 风格+配图+HTML设计稿 → 后处理(SVG+PPTX)
```

### 核心特性

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

### 输出产物

| 文件 | 说明 |
|------|------|
| `preview.html` | 浏览器翻页预览（自动生成） |
| `presentation.pptx` | PPTX 文件，PPT 365 中右键"转换为形状"可编辑 |
| `svg/*.svg` | 单页矢量 SVG，可直接拖入 PPT |
| `slides/*.html` | 单页 HTML 源文件 |

### 环境依赖

#### 必须

- **Node.js** >= 18（Puppeteer + dom-to-svg 需要）
- **Python** >= 3.8（脚本执行）
- **python-pptx**（PPTX 生成）

#### 自动安装（首次运行自动处理）

- `puppeteer` — Headless Chrome
- `dom-to-svg` — DOM 转 SVG（保留 `<text>` 可编辑）
- `esbuild` — 将 dom-to-svg 打包为浏览器 bundle

#### 一键安装

```bash
# Python 依赖
pip install python-pptx lxml Pillow

# Node.js 依赖（首次运行脚本时自动安装，也可手动提前安装）
npm install puppeteer dom-to-svg
```

### 目录结构

```
ppt-agent-skill/
  SKILL.md                    # 主工作流指令（Agent 入口）
  README.md                   # 本文件
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

### 脚本用法

```bash
# 合并预览
python3 scripts/html_packager.py <slides_dir> -o preview.html

# HTML 转 SVG
python3 scripts/html2svg.py <slides_dir> -o <svg_dir>

# SVG 转 PPTX
python3 scripts/svg2pptx.py <svg_dir> -o output.pptx --html-dir <slides_dir>
```

### 触发方式

在 Claude 对话中，以下表达会触发此 Skill：

- "帮我做个 PPT" / "做一个关于 X 的演示"
- "做 slides" / "做幻灯片" / "做汇报材料"
- "把这篇文档做成 PPT"
- "做培训课件" / "做路演 deck"
