<div align="center">
  <img src="assets/logo.png" alt="PPT Agent Logo" width="180" />
  <h1>PPT Agent</h1>
  <p><strong>基于软件工程理念的演示文稿生成框架。</strong></p>

  <p>
    <a href="#作为-agent-技能运行指南"><img src="https://img.shields.io/badge/Quick_Start-blue?style=for-the-badge" alt="Quick Start" /></a>
    <a href="README_EN.md"><img src="https://img.shields.io/badge/English_Docs-gray?style=for-the-badge" alt="English" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" /></a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Pipeline-6_Stages-4f7df5?style=flat-square" alt="Pipeline" />
    <img src="https://img.shields.io/badge/Styles-8_Themes-ff6b35?style=flat-square" alt="Styles" />
    <img src="https://img.shields.io/badge/Layouts-10_Types-00d4ff?style=flat-square" alt="Layouts" />
    <img src="https://img.shields.io/badge/Charts-13_Templates-8b5cf6?style=flat-square" alt="Charts" />
    <img src="https://img.shields.io/badge/Blocks-8_Components-22c55e?style=flat-square" alt="Blocks" />
    <img src="https://img.shields.io/badge/Scripts-14_Tools-f59e0b?style=flat-square" alt="Scripts" />
  </p>
</div>

---

**PPT Agent** 是一个基于 Agentic 工作流与代码驱动的演示文稿（PPT）生成引擎。

区别于传统的大模型一键生成工具，PPT Agent 通过架构的严谨解耦，解决生成流中的幻觉重叠与布局错乱问题。

系统采用基于隔离阶段的 Subagent 编排、严格的数据验证合同，以及基于机器的像素级视觉验证（Visual QA）。该框架旨在将结构化的逻辑内容推导为高保真、支持深度二次编辑的跨平台 PPTX 文件。

## 核心架构特性

本项目针对大模型结构化生成过程中的上下文边界与渲染稳定性问题，进行了如下架构优化：

### 阶段隔离的 Subagent 编排
项目摒弃了单体 Playbook 的设计模式。在资料检索 (Research)、逻辑大纲 (Outline)、视觉风格设定 (Style) 以及页面排版 (Planning) 等独立流转节点中，引擎提供隔离的执行上下文，利用阶段专属 Prompt 分发指令。系统在完整控制链路中传递预设的 `MAIN_MODEL` 参数，以规避大上下文环境带来的状态疲劳与模型污染。

### 闭环的像素级视觉验证 (Visual QA)
针对前端渲染中的元素重叠问题，系统引入了自动化的截图校验机制。当单页 HTML 构建完成后，后端进程将拦截渲染管线，截取低分辨率快照并返还给大模型进行视觉审计。一旦检测到布局溢出或元素重叠，Agent 将进行 DOM 结构与 CSS 规则的整体重构，以消除冲突，而非依赖简单的间距调整。

### 无状态的基建设计 (Stateless Infrastructure)
项目移除了类似 `progress.json` 的全局状态追踪器。长耗时管线的中断恢复机制完全基于磁盘文件系统中的实际产物（例如 `outline.md` 和 `style.json`）进行阶段推断。本设计大幅提高了系统的容灾能力与运行韧性。

### 数据层与渲染层的边界隔离
每个生成的页面视图均被约束于独立的 JSON 合同中。在结构化数据通过 UI 组件转换为 HTML 之前，内置的验证脚本将进行离线的语法合法性和变量一致性校验，拦截潜在的标签错误与数据遗漏。

---

## 跨端双引擎输出

为保障项目的多端兼容性和文件可编辑性，编译层支持双重原生管线：
- **PNG 渲染流 (`presentation-png.pptx`)**: 通过无头浏览器直出光栅化图层，保证高级 CSS 滤镜与自定义字体的 100% 还原与全平台兼容。
- **SVG 矢量流 (`presentation-svg.pptx`)**: 依托矢量组件导出协议，保证图形的无限缩放，并保留核心文本的二次修改权限。

<details>
  <summary><b>点击展开：渲染产物参照</b></summary>
  <div align="center">
    <br/>
    <img src="assets/screenshots/slide1.png" width="48%" />
    <img src="assets/screenshots/slide2.png" width="48%" />
    <img src="assets/screenshots/slide3.png" width="48%" />
    <img src="assets/screenshots/slide4.png" width="48%" />
  </div>
</details>

---

## 六阶段标准化生成管线

系统的自动化流水线严格遵循以下生命周期：

1. **需求意图探针**：利用大模型定位输出边界，并规划研报抓取方向。
2. **全网数据检索**：经由 Search-lite 获取能够支撑核心骨架的客观知识参考。
3. **结构化叙事建模**：梳理逻辑脉络，建立符合金字塔原理的严谨 Markdown 大纲。
4. **全局视觉公约映射**：确定主题色盘与字体规范，生成全局 `style.json` 规则链。
5. **视图装配与 Visual QA**：循环处理每个子视图槽，单页挂载组件、灌入数据内容，并执行截图审计与冲突重排。
6. **文件编译打包**：生成便于浏览的网页画廊（Web Preview），同步激活后端 `pptx` 双输出管线。

---

## 作为 Agent 技能运行指南

本框架目前作为智能化代理平台的原生 **Skill（技能插件）** 挂载运行。

使用者无需进行手动服务配置，可在代理界面的对话框内发出一句话指令实现端到端的流程触发。示例指令：

> *"我下周需要汇报 2026年 AI 具身智能发展趋势。请生成一份 15 页的分析材料，整体设计要求采用暗色系科技风格。"*

管线生成期间会自动流转各项 QA 拦截，最终交付物将会整理导出至本地相对路径：
📁 `ppt-output/runs/<RUN_ID>/` 

---

## 物理依赖结构

代码库的拓扑设计严格映射阶段隔离原则：

```text
ppt-agent-skill/
├── SKILL.md                 # 主控制器：定义工作流状态转移图、失败回退矩阵与终止边界。
├── scripts/                 # 脚本运行时：仅提供系统级的 IO 处理与 Python/Node 校验节点，无自决策能力。
├── references/              # 静态知识库：存放由各子代理阶段独立挂载的 Markdown 参考源。
│   ├── playbooks/           # 按阶段解耦的运行指导手册 (Outline, Style, Planning 等)
│   ├── prompts/             # 各流水节点的上下文模板片段
│   ├── layout & charts ...  # 组件架构骨牌指南与数据格式规范
│   └── README.md            
├── assets/                  # 演示画廊静态用图
└── ...
```

## 证书

[MIT License](LICENSE)
