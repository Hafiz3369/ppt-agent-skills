---
name: ppt-agent
description: 专业 PPT 演示文稿全流程 AI 生成助手。模拟顶级 PPT 设计公司的完整工作流（需求调研 -> 资料搜集 -> 大纲策划 -> 策划稿 -> 设计稿），输出高质量 HTML 格式演示文稿。当用户提到制作 PPT、做演示文稿、做 slides、做幻灯片、做汇报材料、做培训课件、做路演 deck、做产品介绍页面时触发此技能。即使用户只说"帮我做个关于 X 的介绍"或"我要给老板汇报 Y"，只要暗示需要结构化的多页演示内容，都应该触发。也适用于用户说"帮我把这篇文档做成 PPT"、"把这个主题做成演示"等需要将内容转化为演示格式的场景。
---

# PPT Agent v4 -- 主控制台合同

## 1. 目标与边界

本文件定义：

1. 主状态机（Step0-Step5）
2. 每步硬门槛（Gate）
3. 正式产物链
4. Prompt 模板化与 harness 调度协议
5. 失败回退与恢复

### 主 agent 是控制台，不是内容生产者

主 agent 只做：

- 维护计划（`update_plan`）和步骤状态
- 调用 `prompt_harness.py` 生成 subagent prompt
- 拉起 / 发送 RUN / 轮询 STATUS / 回收 FINALIZE / 关闭 subagent
- 检查 gate（文件存在性 + validator exit code + 计数一致性）
- 与用户交互（采访、分支选择、大纲确认、预览确认）

主 agent 不做：

- 代写任何正式产物（research、outline、planning、html）
- 用口头判断替代 validator/harness
- 在 `SKILL.md` 内复述 playbook 执行细节
- 手写 subagent prompt（必须通过 prompt_harness.py 填充模板）

---

## 2. 全局硬规则

### 计划工具

- 计划工具调用权只属于主 agent
- 进入 skill 后第一项动作：主 agent 创建 canonical plan
- 同一时刻最多一个 `in_progress` 步骤
- 仅在状态变化时更新计划

### Subagent 生命周期

- 显式生命周期：`create -> RUN -> STATUS... -> FINALIZE -> close`
- 默认不继承父线程上下文
- 子代理模型默认继承主 agent
- 任一 subagent 完成且不再复用时，必须立即关闭
- 单页 subagent 失败只回退该页，不阻塞其他页

### Prompt 模板化（强制）

- 所有 subagent prompt 必须通过 `prompt_harness.py` 从模板生成
- 主 agent 禁止手写 prompt 正文，只传参数
- 模板文件位于 `references/prompts/tpl-*.md`，预埋 `{{VARIABLE}}` 占位符
- Harness 输出的运行时 prompt 位于 `OUTPUT_DIR/runtime/prompt-*.md`

### 通信协议

主 agent 与 subagent 仅三类指令：

| 指令 | 方向 | 内容 |
|------|------|------|
| **RUN** | 主 -> 子 | prompt 文件路径（一行路径，不发正文） |
| **STATUS** | 子 -> 主 | 固定格式：进度、阻塞项、下一动作 |
| **FINALIZE** | 子 -> 主 | 完成信号 + 产物路径列表 |

仅里程碑通信，减少对话往返。任何修复必须直接改文件并回传路径。

### 资源型 Prompt 双层消费（规范）

资源文件采用 blockquote 分层结构：

```markdown
# 子资源名称
> 一句话定位：适用场景、数据类型匹配、核心策略。（引用层）

精炼但强大的完整实现细节。（正文层）
```

消费规则（脚本驱动）：

- planning 阶段：`resource_loader.py menu` 加载所有资源的 `# 标题` + `> 引用` 组成菜单
- html 阶段：`resource_loader.py resolve` 按 planning JSON 字段动态加载对应资源正文
- 字段路由：`layout_hint` -> layouts/、`card_type` -> blocks/、`chart_type` -> charts/
- 新增资源文件自动进入菜单，无需改代码
- `> 引用` 必须精准到数据类型、适用场景、约束条件，不能是正文的复述

### 校验双保险

- 阶段内自审：subagent 在 FINALIZE 前自行校验
- 主链 gate 复检：主 agent 回收后再跑同一 validator
- sub-agent 内校验通过不等于自动放行

---

## 3. 环境与前置

开始前检查：

| 能力 | 要求 | 降级规则 |
|------|------|---------|
| 文件读写 | 必须有 | 无则停止 |
| Python 执行 | 必须有 | 无则停止 |
| 信息检索 | 尽量有 | 缺失时依赖用户材料（走 Step2B） |
| Node.js | 导出时尽量有 | 无则停在 HTML |
| Planning 工具 | 必须有且必用 | 无则停止 |
| Sub-agent 能力 | 必须有 | 无则停止 |

最前置顺序（强制）：

1. 主 agent 执行 `update_plan`，创建 canonical plan
2. 确认环境能力
3. 进入 Step 0

---

## 4. 路径与正式产物合同

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

正式产物链：

```text
interview-qa.txt
  -> requirements-interview.txt
  -> search.txt / source-brief.txt
  -> search-brief.txt（仅 research 分支）
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

运行时文件（非正式产物）：

```text
OUTPUT_DIR/runtime/
  prompt-interview.md
  prompt-research-synth.md
  prompt-outline.md
  prompt-style.md
  prompt-page-{n}.md
```

`progress.json` 是必需运行账本，Step 0 后必须存在。

---

## 5. Canonical Plan

固定步骤结构（按 PRD Section 17）：

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

P4.NN.01 harness 生成 PageAgent-NN prompt
P4.NN.02 创建 PageAgent-NN subagent
P4.NN.03 [WAIT_AGENT] 等待 FINALIZE
P4.NN.04 回收校验（planning{NN}.json + slide-{NN}.html + slide-{NN}.png + 图审通过）
P4.NN.05 关闭 PageAgent-NN
（所有页并行，流式推进）

P5.01  生成 preview.html
P5.02  PNG 导出 -> presentation-png.pptx
P5.03  SVG 导出 -> presentation-svg.pptx
P5.04  写入 delivery-manifest.json
```

更新规则：

- 仅在状态变化时更新计划
- 等待同一 subagent 时禁止重复写等价 plan
- 并行页必须逐页追踪，不可合并成"大步骤"
- create/wait/close 必须拆开
- generate/validate 必须拆开
- 每次回退显式标记 `ROLLBACK->StepID`

---

## 6. Prompt Harness 调度规范

### 调度流程（每个 subagent 统一）

```bash
# 1. 主 agent 调用 harness 填充模板
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/tpl-{TYPE}.md \
  --var KEY1=VALUE1 \
  --var KEY2=VALUE2 \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/{TYPE}-playbook.md \
  --output OUTPUT_DIR/runtime/prompt-{TYPE}.md

# 2. 主 agent 创建 subagent，传入 prompt 路径
# 3. 发送 RUN 指令
# 4. 轮询 STATUS
# 5. 收到 FINALIZE
# 6. 执行 gate 校验
# 7. close subagent
```

### 模板文件索引

| 模板 | 路径 | 对应阶段 |
|------|------|---------|
| 采访 | `prompts/tpl-interview.md` | Step 0 |
| Research | `prompts/tpl-research-synth.md` | Step 2A |
| 大纲 | `prompts/tpl-outline.md` | Step 3 |
| 风格 | `prompts/tpl-style.md` | Step 3.5 |
| 单页 | `prompts/tpl-page-agent.md` | Step 4 |

### Harness 硬规则

- 所有 `{{VAR}}` 必须被填充，残留即 ERROR
- `--inject-file` 将文件内容内联嵌入模板对应位置
- 输出路径固定在 `OUTPUT_DIR/runtime/`
- Harness 不做调度、不做 subagent 管理 -- 纯文本变换

---

## 7. 主流程状态机

### Step 0 用户采访（必经 Gate）

目标：

- `OUTPUT_DIR/interview-qa.txt`
- `OUTPUT_DIR/requirements-interview.txt`

执行：

1. 主 agent 用 `tpl-interview.md` 组装采访问题（或直接发问）
2. 采访必须覆盖：场景、受众、目标动作、页数与密度、风格、品牌、必含、必避、语言、配图、资料使用策略
3. 收到回答后写入 `interview-qa.txt`
4. 归一化需求写入 `requirements-interview.txt`

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py interview OUTPUT_DIR/interview-qa.txt
python3 SKILL_DIR/scripts/contract_validator.py requirements-interview OUTPUT_DIR/requirements-interview.txt
```

通过条件：双文件存在且字段完整。

失败回退：未完成采访 gate 不得进入 Step 1。

---

### Step 1 输入识别与分流

目标：确定执行分支。

执行：

1. 识别输入类型：大段文本、单文件、多文件、doc/ppt/pptx
2. 强制询问分支：需要 research / 直接基于现有资料制作
3. 记录分支到 `requirements-interview.txt`

通过条件：分支选择明确且已记录。

失败回退：未决策时进入 `WAIT_USER`。

---

### Step 2A Search-Lite（单 Subagent）

目标：

- `OUTPUT_DIR/search.txt`
- `OUTPUT_DIR/search-brief.txt`

执行：

```bash
# 1. 生成 prompt
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/tpl-research-synth.md \
  --var TOPIC="主题" \
  --var REQUIREMENTS_PATH=OUTPUT_DIR/requirements-interview.txt \
  --var SEARCH_OUTPUT=OUTPUT_DIR/search.txt \
  --var BRIEF_OUTPUT=OUTPUT_DIR/search-brief.txt \
  --var TOOLS_AVAILABLE="search_web,read_url_content,grok-search" \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/research-synth-playbook.md \
  --output OUTPUT_DIR/runtime/prompt-research-synth.md

# 2. 创建 ResearchSynth subagent
# 3. 发送 RUN（prompt 路径）
# 4. 等待 FINALIZE
# 5. Gate 校验
```

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py search OUTPUT_DIR/search.txt
python3 SKILL_DIR/scripts/contract_validator.py search-brief OUTPUT_DIR/search-brief.txt
```

通过条件：两份产物都存在且通过 validator。

失败回退：search 质量不足 -> 回同 ResearchSynth 追加检索。补完后关闭。

---

### Step 2B 非 Search 分支

目标：

- `OUTPUT_DIR/source-brief.txt`

执行：

1. 大段文本先写入临时文件
2. 多文件优先文本化（markitdown）
3. 每个文本先读取前 1000 字做主题建立
4. 写入 `source-brief.txt`
5. 若输入为 pptx：强制询问模式（美化/重构/美化+重构）

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py source-brief OUTPUT_DIR/source-brief.txt
```

通过条件：`source-brief.txt` 存在且通过 validator。

---

### Step 3 大纲处理（同 Agent 自审）

目标：

- `OUTPUT_DIR/outline.txt`

执行：

```bash
# 1. 生成 prompt
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/tpl-outline.md \
  --var REQUIREMENTS_PATH=OUTPUT_DIR/requirements-interview.txt \
  --var BRIEF_PATH=OUTPUT_DIR/search-brief.txt \
  --var OUTLINE_OUTPUT=OUTPUT_DIR/outline.txt \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/outline-subagent-playbook.md \
  --output OUTPUT_DIR/runtime/prompt-outline.md

# 2. 创建 Outline subagent
# 3. 发送 RUN
# 4. subagent 内部完成：初稿 -> 严格自审 -> 修复 -> 交回
# 5. 等待 FINALIZE
# 6. Gate 校验
# 7. 关闭
```

自审规则（subagent 内部）：

- 自审不通过时直接改 `outline.txt`
- 自审通过后回传 FINALIZE
- 主 agent 不另开审查 subagent

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py outline OUTPUT_DIR/outline.txt
```

通过条件：`outline.txt` 完成且包含自审通过标记。

失败回退：outline 不合格 -> 回同 subagent 修复（最多 2 轮，之后交用户决策）。

---

### Step 3.5 风格决策（全局前置）

目标：

- `OUTPUT_DIR/style.json`

执行：

```bash
# 1. 生成 prompt
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/tpl-style.md \
  --var REQUIREMENTS_PATH=OUTPUT_DIR/requirements-interview.txt \
  --var OUTLINE_PATH=OUTPUT_DIR/outline.txt \
  --var STYLE_OUTPUT=OUTPUT_DIR/style.json \
  --inject-file STYLES_REF=SKILL_DIR/references/styles/README.md \
  --output OUTPUT_DIR/runtime/prompt-style.md

# 2. 创建 Style subagent
# 3. RUN -> FINALIZE -> Gate -> close
```

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py style OUTPUT_DIR/style.json
```

通过条件：`style.json` 合法。

失败回退：回 Step 3.5。

---

### Step 4 页面并行生产（核心执行层）

目标：

- `OUTPUT_DIR/planning/planning{n}.json`
- `OUTPUT_DIR/slides/slide-{n}.html`
- `OUTPUT_DIR/png/slide-{n}.png`
- 每页双轮图审通过

执行（每页独立）：

```bash
# 对每页 N 并行执行：

# 1. 生成单页 prompt
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/tpl-page-agent.md \
  --var PAGE_NUM=N \
  --var TOTAL_PAGES=TOTAL \
  --var REQUIREMENTS_PATH=OUTPUT_DIR/requirements-interview.txt \
  --var OUTLINE_PATH=OUTPUT_DIR/outline.txt \
  --var BRIEF_PATH=OUTPUT_DIR/search-brief.txt \
  --var STYLE_PATH=OUTPUT_DIR/style.json \
  --var PLANNING_OUTPUT=OUTPUT_DIR/planning/planningN.json \
  --var SLIDE_OUTPUT=OUTPUT_DIR/slides/slide-N.html \
  --var PNG_OUTPUT=OUTPUT_DIR/png/slide-N.png \
  --var SKILL_DIR=SKILL_DIR \
  --var REFS_DIR=SKILL_DIR/references \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/page-agent-playbook.md \
  --output OUTPUT_DIR/runtime/prompt-page-N.md

# 2. 创建 PageAgent-N subagent
# 3. 发送 RUN
# 4. 等待 FINALIZE
```

单页 subagent 内部链路（固定顺序）：

```text
1. planning{n}.json    -- 策划稿生成
2. planning 自审修复    -- 运行 planning_validator.py
3. slide-{n}.html      -- HTML 设计稿生成
4. slide-{n}.png       -- 截图（html2png.py）
5. 第 1 轮图审修复     -- 对照 PNG 审查并修复
6. 第 2 轮图审修复     -- 二次审查确认
7. 通过 -> FINALIZE    -- 交回产物路径
```

调度规则：

- 按页创建 subagent，一个 subagent 负责一页全链路
- 采用流式并行，不等待全部页完成
- 任一页失败只回退该页，不阻塞其他页推进
- 先完成先推进

Gate 校验（每页）：

```bash
# planning 存在
test -s OUTPUT_DIR/planning/planningN.json
python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning --refs SKILL_DIR/references --page N

# html 存在
test -s OUTPUT_DIR/slides/slide-N.html

# png 存在（图审已执行的证据）
test -s OUTPUT_DIR/png/slide-N.png
```

通过条件：每页的 planning + html + png 三件套存在，planning validator 通过。

失败回退：单页失败只回退该页步骤。

---

### Step 5 自动交付

目标：

- `OUTPUT_DIR/preview.html`
- `OUTPUT_DIR/presentation-png.pptx`
- `OUTPUT_DIR/presentation-svg.pptx`
- `OUTPUT_DIR/delivery-manifest.json`

执行：

```bash
# 1. 预览
python3 SKILL_DIR/scripts/html_packager.py OUTPUT_DIR/slides -o OUTPUT_DIR/preview.html

# 2. PNG 管线（与 SVG 并行）
python3 SKILL_DIR/scripts/html2png.py OUTPUT_DIR/slides -o OUTPUT_DIR/png --scale 2
python3 SKILL_DIR/scripts/png2pptx.py OUTPUT_DIR/png -o OUTPUT_DIR/presentation-png.pptx

# 3. SVG 管线（与 PNG 并行）
python3 SKILL_DIR/scripts/html2svg.py OUTPUT_DIR/slides -o OUTPUT_DIR/svg
python3 SKILL_DIR/scripts/svg2pptx.py OUTPUT_DIR/svg -o OUTPUT_DIR/presentation-svg.pptx --html-dir OUTPUT_DIR/slides

# 4. 交付清单
# 主 agent 写入 delivery-manifest.json
```

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py delivery-manifest OUTPUT_DIR/delivery-manifest.json --base-dir OUTPUT_DIR
```

通过条件：preview + 双 pptx + 清单全存在。

失败回退：导出失败只回退导出步骤，不回退内容生产。双管线独立重试。

---

## 8. 校验与验收 Gate 总览

| Gate | 校验命令 | 通过条件 |
|------|---------|---------|
| 采访 | `contract_validator.py interview` + `requirements-interview` | 双文件存在且字段完整 |
| 分支 | 逻辑判断 | 分支选择明确且已记录 |
| Search | `contract_validator.py search` + `search-brief` | 两文件存在且通过 |
| 大纲 | `contract_validator.py outline` | outline.txt 完成且通过自审 |
| 风格 | `contract_validator.py style` | style.json 合法 |
| 单页 | `planning_validator.py` + 文件存在性 | planning + html + png 三件套 + 双轮图审通过 |
| 导出 | `contract_validator.py delivery-manifest` | preview + 双pptx + 清单存在 |

---

## 9. 回退与异常处理

| 异常 | 回退目标 | 规则 |
|------|---------|------|
| 采访信息不足 | Step 0 补问 | 不进入 Step 1 |
| Search 质量不足 | 同 ResearchSynth 追加检索 | 补完后关闭 |
| 大纲不合格 | 同 Outline subagent 修复 | 最多 2 轮自审 |
| 单页失败 | 只回退该页 | 不阻塞其他页 |
| 导出失败 | 只回退导出步骤 | 不回退内容生产 |

恢复策略：基于文件真源与 gate 结果自动定位续跑点。

---

## 10. 恢复规则（中断续跑）

恢复时只信文件与校验，不信口头记忆：

1. 绑定目标 `RUN_ID`（用户指定优先，否则 `latest`）
2. 校验 `progress.json`：

```bash
python3 SKILL_DIR/scripts/progress_validator.py OUTPUT_DIR/progress.json
```

3. 从高到低探测已完成里程碑（`5 -> 4 -> 3.5 -> 3 -> 2 -> 1 -> 0`），找到最高可通过 stage
4. 从下一个未完成 step 继续
5. 若任一前序 gate 失败，直接回退到该 step 重做

---

## 11. 运行入口索引

核心调度工具：

- **Prompt 填充**：`scripts/prompt_harness.py`
- **资源路由**：`scripts/resource_loader.py`
- **模板文件**：`references/prompts/tpl-*.md`

校验工具：

- 合同校验：`scripts/contract_validator.py`
- Planning 校验：`scripts/planning_validator.py`
- Progress 校验：`scripts/progress_validator.py`
- 里程碑总验收：`scripts/milestone_check.py`

导出工具：

- 预览打包：`scripts/html_packager.py`
- HTML->PNG：`scripts/html2png.py`
- HTML->SVG：`scripts/html2svg.py`
- PNG->PPTX：`scripts/png2pptx.py`
- SVG->PPTX：`scripts/svg2pptx.py`

执行细则真源：

- `references/playbooks/research-synth-playbook.md`
- `references/playbooks/outline-subagent-playbook.md`
- `references/playbooks/page-agent-playbook.md`

Prompt 模板真源：

- `references/prompts/tpl-interview.md`
- `references/prompts/tpl-research-synth.md`
- `references/prompts/tpl-outline.md`
- `references/prompts/tpl-style.md`
- `references/prompts/tpl-page-agent.md`

主控制台只引用这些真源，不在 `SKILL.md` 中重复内嵌执行细节。
