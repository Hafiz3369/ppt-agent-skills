<div align="center">
  <img src="assets/logo.png" alt="PPT Agent Logo" width="160" />
  <h1>PPT Agent</h1>
  <p><strong>像构建软件工程一样生成演示文稿。</strong></p>

  <p>
    <a href="#快速开始"><img src="https://img.shields.io/badge/Quick_Start-blue?style=for-the-badge" alt="Quick Start" /></a>
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

PPT Agent 是一个基于代码驱动的演示文稿生成流框架。本项目将“内容策划”与“视觉排版”完全解耦，通过严格的数据结构规划和按需加载的资产库，生成高保真 HTML 与可二次编辑的 PPTX，从根本上解决大模型长提示词所带来的排版错乱与幻觉问题。

## 核心特性

- **架构与设计分离**：先生成并校验表述单页结构的 `JSON`，再将其渲染为 `HTML`。
- **细粒度的按需加载**：拥有 60+ 模块资产，但通过多级树干仅注入“当前页”必要的组件上下文，节约 Token 的同时避免指令冲突。
- **构建前校验 (QA)**：通过内部脚本在写入时实时校验 JSON，自动挂载预置资源组装 Prompt，人工只需负责审阅与需求定义。
- **双引擎输出**：渲染最终结果时，提供最大平台兼容性的 PNG 图片流构建管线，以及保留矢量和文字可编辑性的 SVG 构建管线。
- **状态持久化**：超长生成任务节点实时快照至 `progress.json`，无缝支持中断与断点续做。

## 效果展示

_主题预览（片段）：_

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

## 工作流

标准生成过程遵循严格的 6 步定制生产线：

1. **需求访谈**：阻断式问询，提取受众与场景。
2. **并发搜索**：执行多维度信息检索与数据交叉验证。
3. **金字塔大纲**：规划基础叙事轨迹和论证策略。
4. **单页结构化 (JSON)**：确认布局分布与信息封装点。
5. **视图装配 (HTML)**：装载 CSS 变量并渲染终端界面。
6. **产物打包 (PPTX)**：脚本回调并组装原生 OOXML 文稿。

## 快速开始

本项目为零配置的 AI 原生技能（Agent Skill），无需任何手动环境配置或前置安装，运行依赖在执行管线中由智能体全自动补齐。

### 运行机制

项目目前以 Skill 形式存在。在交互窗口中直接传入需求即可触发 Agent 完整装配流：

> _"生成一份关于 AI 大模型算力消耗趋势的 15 页路演 Deck。"_ 

生成产物将自动写入根目录下的 `ppt-output/`，包含浏览器可翻页版 `preview.html` 以及 `presentation.pptx`。

## 架构

```text
ppt-agent-skill/
├── SKILL.md                 # Agent 中枢指引与调度策略
├── scripts/                 # 自动化装配执行器 (Prompt / SVG 注入、格式挂载)
└── references/              # 可插拔静态系统库
    ├── blocks/              # 预设卡片系统
    ├── layouts/             # Bento 等网格骨架法则
    ├── charts/              # 无图表框架的纯 SVG 统计类库
    └── styles/              # 符合设计准则的 8 项色谱规则
```

## 证书

[MIT License](LICENSE)
