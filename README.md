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
    <img src="https://img.shields.io/badge/Blocks-7_Components-22c55e?style=flat-square" alt="Blocks" />
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
- **可恢复产物链**：主链严格落盘中间产物，长流程可基于正式产物恢复，而不是依赖单一运行时状态文件。

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

生成产物将自动写入根目录下的 `ppt-output/`：Step 5c 会生成浏览器可翻页版 `preview.html`，用户确认 HTML 并完成 Step 6 转换后产出 `presentation.pptx`。

## 仓库结构

当前仓库按 `SKILL.md` 的主控制台模型组织，真正的运行入口只有三类：

```text
ppt-agent-skill/
├── SKILL.md                 # 主状态机、硬门槛、失败回退
├── scripts/                 # 主链脚本入口（validator / assembler / export）
│   └── README.md            # 脚本索引
├── references/              # markdown 真源
│   ├── playbooks/           # sub-agent 执行细则
│   ├── runtime/             # 运行期共享合同
│   ├── design-runtime/      # 设计/运行规则补充
│   ├── ops/                 # 运维与资源映射
│   └── README.md            # references 索引
├── assets/                  # logo 与 README 截图
├── copy/                    # 手工备份区，不参与 runtime
└── ppt-output/              # 运行产物目录（忽略提交）
```

### 目录边界

- `SKILL.md`：只负责主控制台合同，不再内嵌 sub-agent prompt 模板。
- `scripts/`：只保留主链实际执行脚本，不放 markdown 镜像副本。
- `references/`：只保留当前主链引用的 markdown 真源，根目录只放索引，职责文档进入分组子目录。
- `copy/`：只做备份，不作为任何脚本或 agent 的执行入口。
- `ppt-output/`：只放运行产物，不放代码和文档真源。

### 入口索引

- 主控制台入口：`SKILL.md`
- 脚本入口总表：`scripts/README.md`
- markdown 入口总表：`references/README.md`

## 证书

[MIT License](LICENSE)
