# PPT Agent Skill

**[English](README_EN.md)**

> 模仿万元/页级别 PPT 设计公司的完整工作流，输出高质量 HTML 演示文稿 + 可选双管线 PPTX。

## 工作流概览

```
需求调研 → 资料搜集 → 大纲策划 → 策划稿(含配图策略) → 风格+配图+HTML设计稿 → 后处理(PNG/SVG → PPTX)
```

## 效果展示

> 以「新一代小米SU7发布」为主题的示例输出（小米橙风格）：

| 封面页 | 配置对比页 |
|:---:|:---:|
| ![封面页](ppt-output/png/slide_01_cover.png) | ![配置对比](ppt-output/png/slide_02_models.png) |

| 动力续航页 | 智驾安全页 |
|:---:|:---:|
| ![动力续航](ppt-output/png/slide_03_power.png) | ![智驾安全](ppt-output/png/slide_04_smart.png) |

| 结束页 |
|:---:|
| ![结束页](ppt-output/png/slide_05_end.png) |


## 核心特性

| 特性 | 说明 |
|------|------|
| **6步Pipeline** | 需求 → 搜索 → 大纲 → 策划 → 设计 → 后处理，模拟专业 PPT 公司工作流 |
| **模块化提示词体系** | 5 个独立提示词模块（调研/大纲/策划/设计/备注），按需加载避免 token 浪费 |
| **资源注册表** | `resource-registry.md` 统一管理所有资源映射，单一权威来源 |
| **8种预置风格** | 暗黑科技 / 小米橙 / 蓝白商务 / 朱红宫墙 / 清新自然 / 紫金奢华 / 极简灰白 / 活力彩虹 |
| **10种布局系统** | Bento Grid 卡片式布局 + 对称/非对称/L型/T型/瀑布流/英雄区等 |
| **多元卡片风格** | 6 种 card_style（filled/transparent/outline/accent/glass/elevated），打破视觉单调 |
| **智能配图策略** | 策划阶段即决定配图用途(background/split-content/card-inset)、提示词与位置，设计阶段精准执行 |
| **装饰技法工具箱** | 5 种视觉融入技法（渐隐融合/色调蒙版/氛围底图/分屏内容/卡片内嵌） |
| **排版系统** | 7 级字号阶梯 + 间距层级 + 中英文混排规则 |
| **色彩比例** | 60-30-10 法则 + accent 色使用约束 |
| **数据可视化** | 13 种纯 CSS/SVG 图表（进度条/环形图/迷你折线/点阵图/KPI 卡/雷达图/漏斗图等） |
| **构建块库** | 9 种可复用 HTML 构建块（时间线/人物卡/对比/矩阵/引用/图标组等） |
| **设计原则库** | 6 大设计原则参考（认知负荷/色彩心理/构图/数据可视化/叙事弧/视觉层次） |
| **跨页叙事** | 密度交替节奏 / 章节色彩递进 / 封面-结尾呼应 / 渐进揭示 |
| **质量基线** | 独立质量检查清单，确保输出一致性 |
| **双管线 PPTX** | PNG 管线（最大兼容）+ SVG 管线（文字可编辑），用户可选 |

## 输出产物

| 文件 | 说明 |
|------|------|
| `preview.html` | 浏览器翻页预览（自动生成） |
| `presentation.pptx` | PPTX 文件（PNG 管线：直接可用；SVG 管线：PPT 365 右键"转换为形状"可编辑） |
| `png/*.png` | 单页 PNG 截图（PNG 管线产物） |
| `svg/*.svg` | 单页矢量 SVG（SVG 管线产物） |
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
  README.md                   # 本文件
  README_EN.md                # English documentation
  references/
    resource-registry.md      # 资源注册表（所有资源映射的唯一权威来源）
    quality-baseline.md       # 质量基线检查清单
    narrative-rhythm.md       # 叙事节奏与视觉重量
    image-generation.md       # 配图策略 + 融入技法 + 装饰技法工具箱
    pipeline-compat.md        # 管线兼容性约束
    prompts/                  # 模块化提示词（5个独立模块）
      prompt-1-research.md    #   调研提示词
      prompt-2-outline.md     #   大纲提示词
      prompt-3-planning.md    #   策划提示词（含 image 字段规范）
      prompt-4-design.md      #   设计提示词（含动画库 + 资源菜单）
      prompt-5-notes.md       #   演讲备注提示词
      animations.md           #   动画效果库
    styles/                   # 8 种预置风格（每种独立文件 + README 决策规则）
    layouts/                  # 10 种布局（每种独立文件 + README 画布参数）
    charts/                   # 13 种图表模板（每种独立文件 + README 选择指南）
    icons/                    # 4 类 SVG 图标（每类独立文件 + README 使用规则）
    blocks/                   # 9 种构建块（时间线/人物卡/对比/矩阵/引用等）
    page-templates/           # 封面/目录/章节封面/结束页模板
    principles/               # 6 大设计原则（认知负荷/色彩心理/构图等）
  scripts/
    html_packager.py          # 多页 HTML 合并为翻页预览
    html2svg.py               # HTML → SVG（dom-to-svg，保留文字可编辑）
    html2png.py               # HTML → PNG（Puppeteer 截图）
    svg2pptx.py               # SVG → PPTX（OOXML 原生 SVG 嵌入）
    png2pptx.py               # PNG → PPTX（图片嵌入，最大兼容）
```

## 使用方式

在对话中直接描述你的需求即可触发，Agent 会自动执行完整 6 步工作流：

```
你："帮我做一个关于 X 的 PPT"
  → Agent 提问调研需求（等你回复）
  → 自动搜索资料 → 生成大纲 → 策划稿（含配图策略）
  → 逐页设计 HTML（根据策划稿中的配图策略生成配图并融入）
  → 自动后处理：HTML → PNG/SVG → PPTX
  → 输出全部产物到 ppt-output/
```

**触发示例**：

| 场景 | 说法 |
|------|------|
| 纯主题 | "帮我做个 PPT" / "做一个关于 X 的演示" |
| 带素材 | "把这篇文档做成 PPT" / "用这份报告做 slides" |
| 带要求 | "做 15 页暗黑风的 AI 安全汇报材料" |
| 隐式触发 | "我要给老板汇报 Y" / "做个培训课件" / "做路演 deck" |

> 全程无需手动执行任何脚本，所有后处理（预览合并、PNG/SVG 转换、PPTX 生成）由 Agent 在 Step 6 自动完成。

## 技术架构

```
HTML slides
  ├─ [PNG 管线] → Puppeteer 截图 → PNG → python-pptx 嵌入 → PPTX（最大兼容）
  └─ [SVG 管线] → dom-to-svg → SVG → python-pptx + lxml → PPTX（文字可编辑）
```

## 更新日志

### v2.0 — 模块化重构 + 配图策略升级 (2026-03-22)

**架构级重构：**
- **模块化提示词体系**：原单体 `prompts.md`(900+行) 拆分为 5 个独立提示词模块 + 动画库，按需加载
- **资源注册表**：新增 `resource-registry.md` 作为所有资源映射的唯一权威来源，消除散落各处的重复引用
- **质量基线**：新增 `quality-baseline.md` 独立质量检查清单

**新增资源库（6大模块）：**
- **构建块库** `blocks/`：9 种可复用 HTML 构建块（时间线、人物卡、对比表、矩阵图、引用、图标组等）
- **设计原则库** `principles/`：6 大设计原则参考（认知负荷、色彩心理、构图、数据可视化、叙事弧、视觉层次）
- **图标参考库** `icons/`：4 类 SVG 图标分类（内容概念、数据分析、行业场景、流程结构）
- **图表模板库** `charts/`：13 种纯 CSS/SVG 图表独立模板文件
- **布局参考库** `layouts/`：10 种布局参考独立文件（对称/非对称/L型/T型/英雄区/瀑布流等）
- **风格系统** `styles/`：8 种预置风格独立文件 + README 决策规则

**配图策略升级：**
- 策划阶段（Step 4）新增 `image` 字段：在策划稿中即决定每页的配图用途(usage)、提示词(prompt)、位置(placement)、替代文字(alt)
- 新增配图用途类型：`split-content`（分屏内容）、`card-inset`（卡片内嵌），打破纯背景配图模式
- `image_paths` 升级为 `image_info`：携带完整配图元数据（用途、位置、提示词）注入设计阶段
- 装饰技法工具箱资源菜单补充至设计提示词

**多元卡片风格：**
- 新增 `card_style` 字段：6 种卡片视觉风格（filled/transparent/outline/accent/glass/elevated）
- 策划阶段即决定每页卡片风格，打破全填充的视觉单调

**双管线 PPTX：**
- 新增 PNG 管线：`html2png.py` + `png2pptx.py`，Puppeteer 截图 + python-pptx 嵌入，最大兼容性
- SVG 管线保留：`html2svg.py` + `svg2pptx.py`，dom-to-svg + OOXML 原生 SVG 嵌入，文字可编辑
- 用户可在 Step 6 选择管线

**工作流强化：**
- 资源消耗检查：Step 4 前读资源菜单、Step 5c 前读具体参考文件，确保资源被充分利用
- 分组生成：超过 12 页的演示文稿强制分组生成，避免 token 超限
- 已废弃文件清理：移除 `method.md`、旧 `style-system.md`、`bento-grid.md`

## 许可证

[MIT](LICENSE)
