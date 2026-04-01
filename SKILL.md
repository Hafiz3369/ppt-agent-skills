---
name: ppt-agent
description: 专业 PPT 演示文稿全流程 AI 生成助手。模拟顶级 PPT 设计公司的完整工作流（需求调研到资料搜集到大纲策划到策划稿到设计稿），输出高质量 HTML 格式演示文稿。当用户提到制作 PPT、做演示文稿、做 slides、做幻灯片、做汇报材料、做培训课件、做路演 deck、做产品介绍页面时触发此技能。即使用户只说"帮我做个关于 X 的介绍"或"我要给老板汇报 Y"，只要暗示需要结构化的多页演示内容，都应该触发。也适用于用户说"帮我把这篇文档做成 PPT"、"把这个主题做成演示"等需要将内容转化为演示格式的场景。英文场景同样适用："make a presentation about..."、"create slides for..."、"build a pitch deck"、"I need a keynote for..."。隐式意图也应触发："帮我把这个数据可视化一下给老板看"、"我需要一份能拿去路演的东西"、"把这个报告做得好看点能展示"、"beautify my existing PPT"、"redesign these slides"。改善或美化现有 PPT 也属于此技能范畴。
---

# PPT Agent v4 -- 主控制台合同

## 1. 目标与边界

本文件定义：

1. 主状态机（Step 0 到 Step 5）
2. 每步硬门槛（Gate）
3. 正式产物链
4. Prompt 模板化与 harness 调度协议
5. 失败回退与恢复规则

### 主 agent 是控制台，不是内容生产者

主 agent 只做：

- 维护计划（`update_plan`）和步骤状态
- 调用 `prompt_harness.py` 生成 subagent prompt
- 拉起 / 发送 RUN / 轮询 STATUS / 回收 FINALIZE / 关闭 subagent
- 检查 gate（文件存在性 + validator exit code + 计数一致性）
- 与用户交互（采访、分支选择、大纲确认、预览确认）

主 agent 不做：

- 代写任何正式产物（research、outline、planning、html）
- 用口头判断替代 validator / harness
- 在 `SKILL.md` 内复述 playbook 的逐步执行正文
- 手写 subagent prompt（必须通过 `prompt_harness.py` 填充模板）

## 2. 全局硬规则

### 2.1 计划工具

- 计划工具调用权只属于主 agent
- 进入 skill 后第一项动作：主 agent 创建 canonical plan
- 同一时刻最多一个 `in_progress` 步骤
- 仅在状态变化时更新计划

### 2.2 Subagent 生命周期

- 显式生命周期：`create -> RUN -> STATUS... -> FINALIZE -> close`
- 默认不继承父线程上下文
- **子代理模型强制显式指定**：创建任何 subagent 时，必须在 `create` 调用中显式设置 model 参数为 `MAIN_MODEL`（见 3.1.1）；禁止省略 model 参数依赖系统默认值；若创建工具不支持 model 参数则在 prompt 首行注明期望模型
- 任一 subagent 完成且不再复用时，必须立即关闭
- 单页 subagent 失败只回退该页，不阻塞其他页
- 若图片模式为 `generate`，且用户明确需要 AI 文生图，主 agent 可额外创建 `ImageGen` 子代理；PageAgent 不直接承担文生图执行
- **subagent 调用方式以环境感知阶段（Section 3.1.1）输出的《Subagent 操作手册》为准，禁止用其他方式替代**
- **凡是 Canonical Plan 标注了 subagent 的步骤（P2A/P3/P3.5/P4），主 agent 禁止内联执行内容生产；若主 agent 直接写入任何正式产物，视为合同违规**

### 2.3 Prompt 模板化（强制）

- 所有 subagent prompt 必须通过 `prompt_harness.py` 从模板生成
- 主 agent 禁止手写 prompt 正文，只传参数
- 模板文件位于 `references/prompts/tpl-*.md`
- Harness 输出的运行时 prompt 位于 `OUTPUT_DIR/runtime/prompt-*.md`

### 2.4 通信协议

主 agent 与 subagent 仅三类指令：

| 指令 | 方向 | 内容 |
|------|------|------|
| **RUN** | 主 -> 子 | prompt 文件路径（一行路径，不发正文） |
| **STATUS** | 子 -> 主 | 固定格式：进度、阻塞项、下一动作 |
| **FINALIZE** | 子 -> 主 | 完成信号 + 产物路径列表 |

仅里程碑通信，减少对话往返。任何修复必须直接改文件并回传路径。
若某页触发 `generate` 图片模式，PageAgent 应通过 STATUS 告知主 agent 进入 `WAIT_IMAGE_SUBAGENT`；`ImageGen` 子代理完成后，由其以 FINALIZE 把图片路径通知主 agent，再由主 agent 放行该页继续执行。

### 2.5 资源型 Prompt 双层消费（规范）

资源文件采用 blockquote 分层结构：

```markdown
# 子资源名称
> 一句话定位：适用场景、数据类型匹配、核心策略。（引用层）

精炼但强大的完整实现细节。（正文层）
```

消费规则（脚本驱动）：

- planning 阶段：`resource_loader.py menu` 加载所有资源的 `# 标题` + `> 引用` 组成菜单
- html 阶段：`resource_loader.py resolve` 按 planning JSON 字段动态加载对应资源正文
- planning / html 阶段：`resource_loader.py images` 读取 `OUTPUT_DIR/images` 本地图片清单，用于 `image.source_hint` 纠错
- 字段路由：`layout_hint` -> layouts/、`card_type` -> blocks/、`chart_type` -> charts/
- 新增资源文件自动进入菜单，无需改代码
- `> 引用` 必须精准到数据类型、适用场景、约束条件，不能是正文复述

### 2.6 校验双保险

- 阶段内自审：subagent 在 FINALIZE 前自行校验
- 主链 gate 复检：主 agent 回收后再跑同一 validator
- subagent 内校验通过不等于自动放行

### 2.7 执行纪律（严管，禁止乱读）

- 默认策略是"执行优先"：到达某一步后，直接执行该步命令，不先做无关探索
- 进入流程后的第一条对外消息必须是 Step 0 采访问题组；不得先做资料探索或脚本 / 参考读取汇报
- `interview-qa.txt` 与 `requirements-interview.txt` 任一缺失或校验失败时，禁止进入 Step 1+
- 未到对应步骤时，禁止读取 `scripts/*.py`、`references/**`、`README.md`、validator 源码
- 脚本是执行对象，不是阅读对象：仅允许 `python3 ...` 执行；禁止 `python3 ... --help`，所有接口已固化在 `references/cli-cheatsheet.md`
- 模板与 playbook 仅通过 `prompt_harness.py --inject-file` 注入，主 agent 不手动读取正文
- 主 agent 允许读取的内容仅限：`OUTPUT_DIR/**`、用户输入文件、`references/cli-cheatsheet.md`
- 若命令失败，先查 `references/cli-cheatsheet.md` 核对参数；仍不能解决则标记 `BLOCKED_SCRIPT_INTERFACE` 并请求用户决策；不得通过读源码或 `--help` 排障
- 过程汇报禁止"Explored / Read ..."式预读清单；只汇报"当前步骤、已执行命令、Gate 结果、下一动作"

### 2.8 CLI 固定步骤锁（强制）

- CLI agent 必须严格执行 Canonical Plan 的固定 StepID；禁止新增、删减、改名、重排步骤
- 仅允许以下主链迁移：`P0 -> P1 -> (P2A | P2B) -> P3 -> P3.5 -> P4 -> P5`
- 分支迁移只允许二选一：进入 `P2A.*` 后不得再跑 `P2B.*`；进入 `P2B.*` 后不得再跑 `P2A.*`
- 每个 Step 进入前必须满足前序 Gate 已通过；未通过时禁止推进并标记 `BLOCKED_SEQUENCE`
- 每个 Step 完成必须执行对应 Gate 校验（exit code = 0）后，才能标记 `completed`
- 任何失败只允许两种动作：`RETRY_CURRENT_STEP` 或 `ROLLBACK->StepID`；禁止"跳到后续步骤试试看"
- `WAIT_USER` 与 `WAIT_AGENT` 是硬等待点；未收到输入 / FINALIZE 前禁止执行后续步骤
- Step 4 允许并行仅限页内子链路；每页仍必须固定执行 `P4.NN.01 -> 02 -> 03 -> 04 -> 05`
- 若检测到越序、跳步、跨分支混跑，立即停止并回报 `BLOCKED_SEQUENCE`

## 3. 环境、路径与正式产物合同

### 3.1 环境感知（强制，Step 0 前必须完成）

进入任何业务步骤前，主 agent 必须执行以下感知并将结果**显式输出到对话**中。

#### 3.1.1 Subagent 操作手册

主 agent 必须：

1. 自检当前环境中所有与 agent/subagent 创建、管理、通信相关的工具或 API
2. **识别当前主 agent 的模型标识**，记录为 `MAIN_MODEL` 变量并输出到对话中（例：`MAIN_MODEL = claude-sonnet-4-20250514`）；若无法自动获取，则从 USER_SETTINGS 或环境变量中读取；仍无法确定时向用户询问
3. 以表格形式输出到对话中（标题固定为 `## Subagent 操作手册`）：工具名、功能描述、关键参数（必须包含 model 参数说明）、调用示例（示例中必须体现 `model=MAIN_MODEL` 的显式传参）
4. 若找不到任何 subagent 管理工具，标记 `BLOCKED_NO_SUBAGENT` 并停止流程

后续所有 subagent 操作必须严格按此手册执行，不得用其他方式（包括内联执行）替代。**每次 `create` 调用必须显式携带 `model=MAIN_MODEL`，禁止省略让系统自选模型。**

#### 3.1.2 Search 工具清单

主 agent 必须：

1. 自检当前环境中所有与 web search、URL 读取相关的工具和 skill
2. 按优先级排序：用户自定义 skill（如 grok-search） > 内置工具（如 search_web、read_url_content）
3. 以表格形式整理好工具名、参数、功能描述，输出到对话中（标题固定为 `## Search 工具清单`）

Step 2A 的 harness 调用中，主 agent 必须**直接将环境感知到的可用工具列表及概要描述**，内联拼接进 `TOOLS_AVAILABLE` 变量传给子代理。

#### 3.1.3 其他能力检查

| 能力 | 要求 | 降级规则 |
|------|------|---------|
| 文件读写 | 必须有 | 无则停止 |
| Python 执行 | 必须有 | 无则停止 |
| 信息检索 | 尽量有 | 缺失时依赖用户材料（走 Step 2B） |
| 文生图能力 | 可选 | 缺失时不创建图片生成 subagent，降级为 `manual_slot` 或 `decorate` |
| Node.js | 导出时尽量有 | 无则停在 HTML |
| Planning 工具 | 必须有且必用 | 无则停止，进度由 planning 工具自身跟踪 |

最前置顺序（强制）：

1. 主 agent 执行 `update_plan`，创建 canonical plan
2. 读取 `references/cli-cheatsheet.md` 建立 CLI 接口认知
3. 执行环境感知（3.1.1 + 3.1.2 + 3.1.3），输出到对话
4. 进入 Step 0

### 3.2 路径变量

| 变量 | 含义 |
|------|------|
| `SKILL_DIR` | 当前 skill 根目录 |
| `ROOT_OUTPUT_DIR` | 用户工作目录下 `ppt-output/` |
| `RUN_ID` | 本次运行唯一标识（`YYYYMMDD-HHMMSS-topic`） |
| `OUTPUT_DIR` | `ROOT_OUTPUT_DIR/runs/{RUN_ID}` |

隔离规则：

- 新任务必须新建 `RUN_ID`
- 正式产物和 runtime 文件只写入当前 `OUTPUT_DIR`
- 恢复任务仅在用户明确指定后绑定旧 `RUN_ID`

### 3.3 正式产物链

```text
interview-qa.txt
  -> requirements-interview.txt
  -> search.txt + search-brief.txt（research 分支）
  -> source-brief.txt（非 research 分支）
  -> outline.txt
  -> style.json
  -> planning/planning{n}.json
  -> slides/slide-{n}.html
  -> png/slide-{n}.png
  -> preview.html
  -> presentation-png.pptx
  -> presentation-svg.pptx
  -> delivery-manifest.json
```

运行时文件位于 `OUTPUT_DIR/runtime/prompt-*.md`。

## 4. Canonical Plan

必须按照次固定步骤结构（按 PRD Section 17）执行：

```text
P0.01  采访问题组装
P0.02  [WAIT_USER] 获取采访回答
P0.03  写入 interview-qa.txt
P0.04  归一化需求 -> requirements-interview.txt

P1.01  输入识别
P1.02  [WAIT_USER] 分支选择（research / 非research）

P2A.01 [如选 research] harness 生成 ResearchSynth prompt
P2A.02 创建 ResearchSynth subagent
P2A.03 [WAIT_AGENT] 等待 FINALIZE
P2A.04 回收校验（search.txt + search-brief.txt）
P2A.05 [可选] 补检索
P2A.06 关闭 ResearchSynth

P2B.01 [如选非research] 文本化预处理
P2B.02 写入 source-brief.txt
P2B.03 [如 pptx] [WAIT_USER] 模式确认（美化/重构/美化+重构）

P3.01  harness 生成 Outline prompt
P3.02  创建 Outline subagent
P3.03  [WAIT_AGENT] 等待 FINALIZE（含自审）
P3.04  回收校验 outline.txt
P3.05  关闭 Outline subagent

P3.5.01 harness 生成 Style prompt
P3.5.02 创建 Style subagent
P3.5.03 [WAIT_AGENT] 等待 FINALIZE
P3.5.04 回收校验 style.json
P3.5.05 关闭 Style subagent

P4.NN.01 创建 PageAgent-NN subagent
P4.NN.02 harness 生成 Planning prompt -> 发送 RUN -> 回收 planning{NN}.json
P4.NN.03 harness 生成 HTML prompt -> 发送 RUN -> 回收 slide-{NN}.html
P4.NN.04 harness 生成 Review prompt -> 发送 RUN -> 自动闭环图审修复 -> 回收并验证
P4.NN.05 关闭 PageAgent-NN subagent
（所有页并行或流式推进，各自独立拥有一个生命周期跨越 3 阶段的 PageAgent）

P5.01  生成 preview.html
P5.02  PNG 导出 -> presentation-png.pptx
P5.03  SVG 导出 -> presentation-svg.pptx
P5.04  写入 delivery-manifest.json
```

更新规则：

- 仅在状态变化时更新计划
- 等待同一 subagent 时禁止重复写等价 plan
- 并行页必须逐页追踪，不可合并成"大步骤"
- create / wait / close 必须拆开
- generate / validate 必须拆开
- 每次回退显式标记 `ROLLBACK->StepID`
- Canonical StepID 是流程合同的一部分，不可动态改写
- 非恢复模式下禁止跳过任何中间 StepID

## 5. 统一调度骨架

本节只定义所有 subagent 共用的调度骨架；各阶段只补本阶段的差异。

### 5.1 统一 Subagent 调度骨架

除 Step 0、Step 1、Step 2B、Step 5 外，所有 subagent 阶段（P2A/P3/P3.5/P4）默认沿用以下骨架，无需各步骤重复声明：

1. 主 agent 查阅 `cli-cheatsheet.md` 对应步骤，执行 harness 生成 prompt 文件
2. 按《Subagent 操作手册》（Section 3.1.1 输出）创建对应 subagent
3. 发送 `RUN`，内容只是一行 prompt 路径
4. 轮询 `STATUS`
5. 收到 `FINALIZE`
6. 主 agent 执行本阶段 gate 复检（命令见 `cli-cheatsheet.md`）
7. subagent 不再复用时立即 `close`

阶段内自审由 subagent 自己完成；主 agent 只认回收后的 gate 结果。

Harness 统一规则：

- 所有 `{{VAR}}` 必须被填充，残留即 ERROR
- `--inject-file` 将文件内容内联嵌入模板对应位置
- 输出路径固定在 `OUTPUT_DIR/runtime/`
- Harness 不做调度、不做 subagent 管理，只做纯文本变换

### 5.2 模板、playbook 与 style 真源

模板文件：

| 模板 | 路径 | 对应阶段 |
|------|------|---------|
| 采访 | `references/prompts/tpl-interview.md` | Step 0 |
| Research | `references/prompts/tpl-research-synth.md` | Step 2A |
| 大纲 | `references/prompts/tpl-outline.md` | Step 3 |
| 风格 | `references/prompts/tpl-style.md` | Step 3.5 |
| 单页 | `references/prompts/tpl-page-agent.md` | Step 4 |

执行细则真源：

- `references/playbooks/research-synth-playbook.md`
- `references/playbooks/outline-subagent-playbook.md`
- `references/playbooks/style-subagent-playbook.md`
- `references/playbooks/step4/page-planning-playbook.md`
- `references/playbooks/step4/page-html-playbook.md`
- `references/playbooks/step4/page-review-playbook.md`

Style 真源：

- `references/styles/runtime-style-rules.md`
- `references/styles/runtime-style-palette-index.md`

### 5.3 CURRENT_BRIEF_PATH 统一约定

以下阶段使用相同的素材摘要选择规则：

```text
CURRENT_BRIEF_PATH
  research      -> OUTPUT_DIR/search-brief.txt
  非 research   -> OUTPUT_DIR/source-brief.txt
```

适用阶段：Step 3 大纲、Step 4 单页生产。

## 6. 主流程状态机

### 6.1 Step 全景表

| Step | 核心动作 | 关键产物 | Gate 校验 | 通过条件 | 失败回退 |
|------|---------|---------|----------|---------|---------|
| `P0` | 采访并归一化需求 | `interview-qa.txt` / `requirements-interview.txt` | `contract_validator.py interview` + `requirements-interview` | 双文件存在且字段完整 | 补问，不进 Step 1 |
| `P1` | 识别输入并确定分支 | 分支记录回 `requirements-interview.txt` | 逻辑判断 | 分支选择明确且已记录 | `WAIT_USER` |
| `P2A` | 检索并压缩外部资料 | `search.txt` / `search-brief.txt` | `contract_validator.py search` + `search-brief` | 双文件通过；brief 含 >=3 种数据类型 | 同 ResearchSynth 追加检索 |
| `P2B` | 压缩用户现有资料 | `source-brief.txt` | `contract_validator.py source-brief` | 文件存在且通过 | 回 Step 2B 重写 |
| `P3` | 生成大纲并自审 | `outline.txt` | `contract_validator.py outline` | outline 完成且含自审通过标记 | 同 subagent 修复，最多 2 轮 |
| `P3.5` | 固定全局风格 | `style.json` | `contract_validator.py style` | style.json 合法 | 回 Step 3.5 |
| `P4` | 按页并行生产 | `planning{n}.json` / `slide-{n}.html` / `slide-{n}.png` | `planning_validator.py` + 文件存在性 | 三件套 + 图片策略闭环 | 只回退该页 |
| `P5` | 导出与打包交付 | `preview.html` / 双 pptx / `delivery-manifest.json` | `contract_validator.py delivery-manifest` | 全部存在 | 只回退导出，不回退内容 |

所有 Prompt 生成命令与 Gate 校验命令的完整参数见 `references/cli-cheatsheet.md`。

### 6.2 Step 0 用户采访（必经 Gate）

目标：生成 `OUTPUT_DIR/interview-qa.txt` 与 `OUTPUT_DIR/requirements-interview.txt`。

不可跳过规则：即使用户在触发消息中已提供了充足的主题信息，采访仍然不可跳过。采访的目的不仅是收集主题内容，更是确认用户往往不会主动提供的隐含选项（配图模式、页数密度、品牌规范、必避内容等）。允许精简问题（已知信息可跳过对应问项），但必须至少确认所有隐含选项。

执行：

1. 主 agent 用 harness 生成 prompt（命令见 cheatsheet Step 0）或直接参考 `tpl-interview.md` 组装采访问题
2. 采访必须覆盖：场景、受众、目标动作、页数与密度、风格、品牌、必含、必避、语言、配图模式（AI 文生图 / 手动补图 / 不用外部图）、资料使用策略
3. 收到回答后写入 `interview-qa.txt`
4. 归一化需求写入 `requirements-interview.txt`

### 6.3 Step 1 输入识别与分流

目标：确定执行分支。

执行：

1. 识别输入类型：大段文本、单文件、多文件、doc / ppt / pptx
2. 强制询问分支：需要 research / 直接基于现有资料制作
3. 记录分支到 `requirements-interview.txt`

### 6.4 Step 2A Search-Lite（单 Subagent）

目标：生成 `OUTPUT_DIR/search.txt` 与 `OUTPUT_DIR/search-brief.txt`。

阶段特有规则：

- 若 search 质量不足，允许回同一 ResearchSynth 追加检索后再关闭
- `search-brief.txt` 必须包含独立的 PPTX 结构化数据包区块（metrics / comparisons / timelines 等至少 3 种数据类型）

### 6.5 Step 2B 非 Search 分支

目标：生成 `OUTPUT_DIR/source-brief.txt`。

执行：

1. 大段文本先写入临时文件
2. 多文件优先文本化（markitdown）
3. 每个文本先读取前 1000 字做主题建立
4. 写入 `source-brief.txt`
5. 若输入为 pptx：强制询问模式（美化 / 重构 / 美化+重构）

### 6.6 Step 3 大纲处理（同 Agent 自审）

目标：生成 `OUTPUT_DIR/outline.txt`。

阶段特有规则：

- `BRIEF_PATH` 必须遵守 5.3 CURRENT_BRIEF_PATH 统一约定
- subagent 内部完成：初稿 -> 严格自审 -> 修复 -> FINALIZE
- 自审不通过时直接改 `outline.txt`
- 主 agent 不另开审查 subagent

### 6.7 Step 3.5 风格决策（全局前置）

目标：生成 `OUTPUT_DIR/style.json`。

阶段特有规则：

- 风格阶段的输入由需求、大纲、runtime 风格规则和预置风格入口共同组成
- 输出必须是可被 planning 与 html 稳定消费的完整 `style.json`

### 6.8 Step 4 页面生产（核心执行层 - 同代理多阶段解耦）

目标：为每页生成 `planning{n}.json`、`slide-{n}.html`、`slide-{n}.png`。

为了防止大语言模型**注意力分散**，本阶段将业务解耦为三个阶段的 Prompt，但**共用同一个 `PageAgent-NN` subagent** 实例，由主代理分阶段将上下文注入并触发动作。这样子代理就保留着前一阶段的对话记忆和设计推理。

1. **4A. Planning 阶段**：主代理解析 `tpl-page-planning.md` 并 RUN，子代理负责写出自审过的 `planning{n}.json`，不写 HTML。
2. **4B. HTML 阶段**：主代理解析 `tpl-page-html.md` 并 RUN，子代理基于记忆中的策划稿和刚拿到的 HTML 指引，严格获取资源并输出单页 HTML。
3. **4C. Review 阶段**：主代理解析 `tpl-page-review.md` 并 RUN，子代理转变为 QA 角色，跑截图后利用 5 大视觉红线审查，亲自修改自己刚才写的 HTML 源码直到完美（最多改 3 轮）。

执行：
- 多页可并行操作。单页仅创建一次 `PageAgent`。
- 只有前置阶段的 Prompt 收到 `FINALIZE` 并在此侧完成 Gate 校验，主 Agent 才能 Harness 生成并发送下一阶段的指令给该子代理。

通过条件：

- 每页的 planning + html + png 三件套存在
- planning validator 通过
- 若 `image.mode` 为 `generate` / `provided`，则 `source_hint` 对应图片可访问
- 若 `image.mode` 为 `manual_slot` / `decorate`，则 HTML 已落地对应槽位或装饰策略

### 6.9 Step 5 自动交付

目标：生成 `OUTPUT_DIR/preview.html`、`OUTPUT_DIR/presentation-png.pptx`、`OUTPUT_DIR/presentation-svg.pptx` 与 `OUTPUT_DIR/delivery-manifest.json`。

执行管线与 Gate 校验命令见 `cli-cheatsheet.md` Step 5。双管线（PNG/SVG）可并行；导出失败只回退导出步骤，不回退内容生产。

## 7. 恢复规则（中断续跑）

恢复时只信文件与校验，不信口头记忆：

1. 绑定目标 `RUN_ID`（用户指定优先，否则 `latest`）
2. 从高到低探测已完成里程碑（`5 -> 4 -> 3.5 -> 3 -> 2 -> 1 -> 0`），找到最高可通过 stage
3. 从下一个未完成 step 继续
4. 若任一前序 gate 失败，直接回退到该 step 重做

## 8. 运行入口索引

完整 CLI 命令速查见 `references/cli-cheatsheet.md`。进入 Step 0 前必须读取此文件建立接口认知，后续步骤直接引用，禁止对任何脚本跑 `--help`。

真源文件索引：

| 类别 | 路径 | 消费方式 |
|------|------|----------|
| Prompt 模板 | `references/prompts/tpl-*.md` | 传路径给 harness，不手动预读 |
| 执行细则 | `references/playbooks/*-playbook.md` | 通过 `--inject-file` 注入，不手动预读 |
| 风格真源 | `references/styles/runtime-style-*.md` | Step 3.5 注入 |
| CLI 命令 | `references/cli-cheatsheet.md` | Step 0 前读取，后续直接引用 |

主控制台只引用这些真源，不在 `SKILL.md` 中重复内嵌执行细节，也不做脚本源码阅读。
