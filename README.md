<div align="center">
  <img src="assets/logo.png" alt="PPT Agent Logo" width="160" />
  <h1>PPT Agent</h1>
  <p><strong>AI-Powered Presentation Design Workflow</strong></p>
  <p>
    模拟万元/页级别 PPT 设计公司的完整工作流<br/>
    输出高质量 HTML 演示文稿 + 可选双管线 PPTX
  </p>

  <p>
    <a href="#-快速开始"><img src="https://img.shields.io/badge/Quick_Start-blue?style=for-the-badge" alt="Quick Start" /></a>
    <a href="README_EN.md"><img src="https://img.shields.io/badge/English_Docs-gray?style=for-the-badge" alt="English" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" /></a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Pipeline-6_Steps-4f7df5?style=flat-square" alt="Pipeline" />
    <img src="https://img.shields.io/badge/Styles-8_Themes-ff6b35?style=flat-square" alt="Styles" />
    <img src="https://img.shields.io/badge/Layouts-10_Types-00d4ff?style=flat-square" alt="Layouts" />
    <img src="https://img.shields.io/badge/Charts-13_Templates-8b5cf6?style=flat-square" alt="Charts" />
    <img src="https://img.shields.io/badge/Blocks-8_Components-22c55e?style=flat-square" alt="Blocks" />
    <img src="https://img.shields.io/badge/Scripts-8_Tools-f59e0b?style=flat-square" alt="Scripts" />
  </p>
</div>

---

## 效果展示

> 以「Linux Do 社区深度解析」为主题的示例输出（暗黑科技风格）：

<div align="center">
  <img src="assets/screenshots/slide1.png" width="32%" />
  <img src="assets/screenshots/slide2.png" width="32%" />
  <img src="assets/screenshots/slide3.png" width="32%" />
  <img src="assets/screenshots/slide4.png" width="32%" />
  <img src="assets/screenshots/slide5.png" width="32%" />
  <img src="assets/screenshots/slide6.png" width="32%" />
  <img src="assets/screenshots/slide7.png" width="32%" />
  <img src="assets/screenshots/slide8.png" width="32%" />
  <img src="assets/screenshots/slide9.png" width="32%" />
  <img src="assets/screenshots/slide10.png" width="32%" />
  <img src="assets/screenshots/slide11.png" width="32%" />
  <img src="assets/screenshots/slide12.png" width="32%" />
  <img src="assets/screenshots/slide13.png" width="32%" />
</div>

---

## 设计理念

这不是一个「套模板填内容」的工具，而是一个**模拟专业设计公司完整工作流**的 AI Agent Skill。

核心差异在于 3 个设计决策：

### 1. 策划与设计分离 -- 先想清楚再动手

```
传统做法：拿到主题 → 直接生成 PPT（内容和排版混在一起）
本项目：  拿到主题 → 调研 → 大纲 → 策划稿(JSON) → 设计稿(HTML)
```

策划稿是纯结构化的 JSON，决定了「每页放什么内容、用什么布局、什么卡片类型」。设计稿只负责把策划稿变成漂亮的 HTML。两个阶段互不干扰，各司其职。

### 2. 资源按需加载 -- 不浪费一个 token

项目有 60+ 个参考文件（布局、图表、设计原则...），但每页 HTML 只需要其中很少一部分。解法是一套**三层决策树**：

| 层级 | 时机 | 决定什么 |
|------|------|---------|
| 第一层 | 用户采访后 | 全局开关（要不要配图、什么风格、什么语言） |
| 第二层 | 大纲确定后 | 叙事节奏模板（按页数选不同模板） |
| 第三层 | 每页生成前 | prompt_assembler.py 自动组装该页所需的全部资源 |

LLM 每页只需 `view_file` 一个 `prompt-ready-{n}.txt`，就获得完整的设计上下文。

### 3. 自动化质量保障 -- 机器能干的不靠人

| 环节 | 自动化工具 | 作用 |
|------|----------|------|
| 策划稿写完 | `planning_validator.py` | 校验 JSON 字段完整性、枚举值合法性、资源路径存在性 |
| HTML 生成前 | `prompt_assembler.py` | 自动组装完整 prompt，杜绝「忘记读资源」 |
| HTML 生成后 | 6 项自检清单 | 内容完整 / 布局无重叠 / 管线安全 / 不溢出 / 色彩规范 / 资源已消费 |
| 全量完成后 | 跨页验证 | 布局多样性 / 视觉密度节奏 / 配图用法多样性 |

---

## 6 步 Pipeline

```
Step 1       Step 2       Step 3        Step 4         Step 5          Step 6
需求调研 ──→ 资料搜集 ──→ 大纲策划 ──→ 逐页策划稿 ──→ 风格+配图+HTML ──→ 后处理
[等用户]                [金字塔原理]  [JSON/页]      [逐页生成]       [PNG/SVG→PPTX]
                                      [验证器校验]   [prompt自动组装]
```

| 步骤 | 做什么 | 关键设计 |
|------|--------|---------|
| **Step 1** 需求调研 | 7 题三层递进采访（场景/内容/执行） | **阻断点** -- 必须等用户回复，不替用户做决定 |
| **Step 2** 资料搜集 | 多维度并行搜索，结果按可信度分级 | 只有 high/medium 可信度的数据才能进策划稿 |
| **Step 3** 大纲策划 | 金字塔原理 + 叙事弧线 + 论证策略 | 每 Part >= 2 页，Part 间有明确的逻辑递进 |
| **Step 4** 策划稿 | 逐页生成 JSON，每页独立文件 | 写入后立即 `planning_validator.py` 验证 |
| **Step 5** 设计稿 | 5a 风格 → 5b 配图 → 5c 逐页 HTML | `prompt_assembler.py` 自动组装完整 prompt |
| **Step 6** 后处理 | 用户选管线 → 转换 → 输出 PPTX | PNG 管线（最大兼容）或 SVG 管线（文字可编辑） |

---

## 核心特性

<table>
<tr>
<td width="50%">

### 丰富的视觉系统
- **8 种预置风格** -- 暗黑科技 / 小米橙 / 蓝白商务 / 朱红宫墙 / 清新自然 / 紫金奢华 / 极简灰白 / 活力彩虹
- **10 种布局** -- Bento Grid + 对称/非对称/L型/T型/瀑布流/英雄区等
- **6 种卡片风格** -- filled / transparent / outline / accent / glass / elevated

</td>
<td width="50%">

### 数据可视化 & 构建块
- **13 种图表** -- 进度条 / 环形图 / 迷你折线 / 点阵图 / KPI 卡 / 雷达图 / 漏斗图等
- **7 种构建块** -- 时间线 / 人物卡 / 对比 / 矩阵 / 引用 / 大图英雄等

</td>
</tr>
<tr>
<td>

### 智能配图策略
策划阶段即决定配图用途、提示词与位置，设计阶段精准执行。7 种视觉融入技法：渐隐融合 / 色调蒙版 / 氛围底图 / 分屏内容 / 卡片内嵌 / 装饰浮层 / 纯背景

</td>
<td>

### 双管线 PPTX 输出

```
HTML ─┬─ PNG Pipeline → PPTX (最大兼容)
      └─ SVG Pipeline → PPTX (文字可编辑)
```

用户自选管线，不替用户做决定

</td>
</tr>
<tr>
<td>

### 自动化工具链
- **prompt_assembler.py** -- 自动组装完整设计 prompt
- **resource_assembler.py** -- 自动组装资源块
- **planning_validator.py** -- 策划稿 JSON 验证（单页+跨页）
- **html_packager.py** -- 多页 HTML 合并翻页预览

</td>
<td>

### 中断恢复
`progress.json` 记录每步进度，长流程中断后可从断点继续。前序步骤产物缺失时自动回退重新生成。

</td>
</tr>
</table>

<details>
<summary><strong>查看完整特性列表</strong></summary>

| 特性 | 说明 |
|------|------|
| **排版系统** | 7 级字号阶梯 + 间距层级 + 中英文混排规则 |
| **色彩比例** | 60-30-10 法则 + accent 色使用约束 |
| **设计原则库** | 6 大设计原则参考（认知负荷/色彩心理/构图/数据可视化/叙事弧/视觉层次） |
| **叙事节奏** | 密度交替 / 章节色彩递进 / 封面-结尾呼应 / 3 种页数标准模板（10/15/20 页） |
| **管线兼容** | 详尽的 CSS 禁止清单 + SVG 安全子集 + 三层模型（浏览器/dom-to-svg/OOXML） |
| **质量基线** | 独立质量检查清单，每页最低标准明确定义 |
| **资源注册表** | `resource-registry.md` 统一管理所有资源映射，单一权威来源 |
| **复杂度自适应** | 按页数自动调整流程粒度（轻量/标准/大型三档） |
| **页面模板** | 封面/目录/章节封面/结束页结构规范 |
| **CSS 动画库** | 渐入/计数/填充/描边等动画效果（HTML 预览用） |

</details>

---

## 快速开始

### 环境依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| Node.js | >= 18 | Puppeteer + dom-to-svg |
| Python | >= 3.8 | 脚本运行 |
| python-pptx | latest | PPTX 生成 |

### 一键安装

```bash
# Python 依赖
pip install python-pptx lxml Pillow

# Node.js 依赖
npm install puppeteer dom-to-svg
```

### 使用方式

在对话中直接描述你的需求即可触发，Agent 会自动执行完整 6 步工作流：

```
你："帮我做一个关于 X 的 PPT"
  → Agent 提问调研需求（等你回复）
  → 自动搜索资料 → 生成大纲 → 逐页策划稿（含配图策略）
  → prompt_assembler 自动组装 → 逐页设计 HTML
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

> 全程无需手动执行任何脚本，所有后处理由 Agent 在 Step 6 自动完成。

---

## 输出产物

```
ppt-output/
  preview.html         # 浏览器翻页预览
  presentation.pptx    # 最终 PPTX
  slides/              # 每页 HTML 源文件
  planning/            # 每页策划稿 JSON（可手动编辑）
  prompts-ready/       # 自动组装的完整 prompt（调试用）
  images/              # AI 配图
  png/                 # PNG 截图（PNG 管线产物）
  svg/                 # 矢量 SVG（SVG 管线产物）
  style.json           # 风格定义
  outline.json         # 大纲
  progress.json        # 进度日志（中断恢复用）
```

---

## 项目结构

```
ppt-agent-skill/
  SKILL.md                        # 主工作流指令（Agent 入口，675 行）
  references/
    resource-registry.md          # 资源注册表（所有映射的唯一权威来源）
    quality-baseline.md           # 质量基线检查清单
    narrative-rhythm.md           # 叙事节奏（3 种页数模板 + 色彩递进 + 规则冲突优先级）
    image-generation.md           # 配图策略（6 维 prompt 公式 + 融入技法 + 装饰工具箱）
    pipeline-compat.md            # 管线兼容性（三层模型 + CSS/SVG 禁止清单）
    prompts/                      # 模块化提示词（5 个 prompt + 动画库）
      prompt-1-research.md        #   调研（7 题三层递进）
      prompt-2-outline.md         #   大纲（金字塔原理 + 叙事弧线 v3.0）
      prompt-3-planning.md        #   策划（14 种 card_type + decoration_hints）
      prompt-4-design.md          #   设计模板（prompt_assembler 自动填充占位符）
      prompt-5-notes.md           #   演讲备注
      animations.md               #   CSS 动画效果库
    styles/                       # 8 种预置风格（独立文件 + 装饰工具箱 + 决策规则）
    layouts/                      # 10 种布局（独立文件 + HTML 骨架 + 画布参数）
    charts/                       # 13 种图表模板（独立文件 + 数据类型映射）
    blocks/                       # 7 种构建块 + 6 种卡片视觉风格
    page-templates/               # 封面/目录/章节封面/结束页结构规范
    principles/                   # 6 大设计原则（认知负荷/色彩心理/构图等）
  scripts/
    prompt_assembler.py           # prompt 自动组装（模板+风格+策划+资源+配图 → 开箱即用）
    resource_assembler.py         # 资源块组装（布局+组件+图表+原则 → [RESOURCES]）
    planning_validator.py         # 策划稿验证（字段/枚举/路径/跨页规则）
    html_packager.py              # 多页 HTML 合并为翻页预览
    html2png.py                   # HTML → PNG（Puppeteer 截图）
    html2svg.py                   # HTML → SVG（dom-to-svg，保留文字可编辑）
    png2pptx.py                   # PNG → PPTX（最大兼容）
    svg2pptx.py                   # SVG → PPTX（OOXML 原生 SVG 嵌入）
```

---

## 技术架构

```
                          ┌─────────────────────────────────────┐
                          │          PPT Agent Workflow          │
                          └──────────────┬──────────────────────┘
                                         │
            ┌────────┬────────┬──────────┼──────────┬────────┐
            ▼        ▼        ▼          ▼          ▼        ▼
        Step 1   Step 2   Step 3     Step 4      Step 5   Step 6
        需求调研  资料搜集  大纲策划   策划稿      设计稿   后处理
                                   (逐页JSON)   (HTML)
                                       │            │
                         planning_validator    prompt_assembler
                         (写入即验证)          (自动组装prompt)
                                                    │
                                         ┌──────────┴──────────┐
                                         ▼                     ▼
                                    PNG Pipeline          SVG Pipeline
                                    html2png.py           html2svg.py
                                         │                     │
                                         ▼                     ▼
                                    png2pptx.py           svg2pptx.py
                                         │                     │
                                         └──────────┬──────────┘
                                                    ▼
                                             presentation.pptx
```

---

## 更新日志

### v3.0 -- 自动化质量保障 + 大纲重构 + 管线兼容性深化 (2026-03-22)

<details>
<summary><strong>自动化工具链（核心升级）</strong></summary>

- **prompt_assembler.py**：自动读取设计模板，替换 5 个占位符（风格/策划/内容/配图/资源），输出开箱即用的完整 prompt 文件。LLM 每页只需 `view_file` 一个文件，从根本上消除「忘记读资源」
- **resource_assembler.py**：自动解析 planning JSON 的 `required_resources` 字段，组装 `[RESOURCES]` 文本块（布局骨架 + 组件模板 + 图表模板 + 设计原则），被 prompt_assembler 内部调用
- **planning_validator.py**：策划稿写入即验证（单页：字段完整性 / 枚举值合法性 / 资源路径存在性 / card_style 多样性；全量：布局多样性 / visual_weight 节奏 / image usage 多样性）

</details>

<details>
<summary><strong>大纲架构师 v3.0</strong></summary>

- prompt-2-outline.md 重构为「Strategic Architect」，内置 5 步思考过程
- 新增 `design_rationale` 字段（核心论点 / 叙事结构 / 情感弧线 / 逻辑链 / 页数分配理由）
- Part 间逻辑关系标注（`transition_from_previous`），杜绝主题并列的扁平大纲
- 每 Part >= 2 页的硬约束 + 数据搜索覆盖标注

</details>

<details>
<summary><strong>管线兼容性深化</strong></summary>

- pipeline-compat.md 从基础清单扩展为三层模型文档（浏览器渲染 / dom-to-svg / OOXML）
- 新增 SVG 元素安全子集、CSS transform 约束、字体处理、形状过滤规则
- svg2pptx.py 大幅增强（+181 行），修复多项转换 bug

</details>

<details>
<summary><strong>叙事节奏优化 + 策划稿增强</strong></summary>

- narrative-rhythm.md 新增 3 种页数标准模板（10/15/20 页）+ 规则冲突优先级 + 边缘场景处理
- prompt-3-planning.md 增强 `decoration_hints` 和 `required_resources` 的卡片级绑定
- html2svg.py 新增 +162 行转换逻辑优化

</details>

### v2.0 -- 模块化重构 + 配图策略升级 (2026-03-22)

<details>
<summary><strong>架构级重构</strong></summary>

- **模块化提示词体系**：原单体 `prompts.md`(900+行) 拆分为 5 个独立提示词模块 + 动画库，按需加载
- **资源注册表**：新增 `resource-registry.md` 作为所有资源映射的唯一权威来源，消除散落各处的重复引用
- **质量基线**：新增 `quality-baseline.md` 独立质量检查清单

</details>

<details>
<summary><strong>新增资源库（6大模块）</strong></summary>

- **构建块库** `blocks/`：7 种可复用 HTML 构建块（时间线、人物卡、对比表、矩阵图、引用、大图英雄等）
- **设计原则库** `principles/`：6 大设计原则参考（认知负荷、色彩心理、构图、数据可视化、叙事弧、视觉层次）
- **图表模板库** `charts/`：13 种纯 CSS/SVG 图表独立模板文件
- **布局参考库** `layouts/`：10 种布局参考独立文件（对称/非对称/L型/T型/英雄区/瀑布流等）
- **风格系统** `styles/`：8 种预置风格独立文件 + README 决策规则

</details>

<details>
<summary><strong>配图策略 + 多元卡片 + 双管线</strong></summary>

- 策划阶段 Step 4 新增 `image` 字段：策划时即决定配图用途/提示词/位置
- 新增 `card_style` 字段：6 种卡片视觉风格（filled/transparent/outline/accent/glass/elevated）
- 新增 PNG 管线：`html2png.py` + `png2pptx.py`，最大兼容性
- SVG 管线保留：`html2svg.py` + `svg2pptx.py`，文字可编辑

</details>

---

## 许可证

[MIT](LICENSE)

---

<div align="center">
  <sub>Built with passion for beautiful presentations</sub>
</div>
