---
name: ppt-agent
description: 专业 PPT 演示文稿全流程 AI 生成助手。模拟顶级 PPT 设计公司的完整工作流（需求调研到资料搜集到大纲策划到策划稿到设计稿），输出高质量 HTML 格式演示文稿。当用户提到制作 PPT、做演示文稿、做 slides、做幻灯片、做汇报材料、做培训课件、做路演 deck、做产品介绍页面时触发此技能。即使用户只说"帮我做个关于 X 的介绍"或"我要给老板汇报 Y"，只要暗示需要结构化的多页演示内容，都应该触发。也适用于用户说"帮我把这篇文档做成 PPT"、"把这个主题做成演示"等需要将内容转化为演示格式的场景。英文场景同样适用："make a presentation about..."、"create slides for..."、"build a pitch deck"、"I need a keynote for..."。隐式意图也应触发："帮我把这个数据可视化一下给老板看"、"我需要一份能拿去路演的东西"、"把这个报告做得好看点能展示"、"beautify my existing PPT"、"redesign these slides"。改善或美化现有 PPT 也属于此技能范畴。
---

# PPT Agent v4 — 主控制台合同

## 1. 主 Agent 角色

**只做**：维护计划、调用 harness、管理 subagent 生命周期、校验 Gate、与用户交互。

**不做**：代写任何正式产物；手写 subagent prompt；内联执行 P2A/P3/P3.5/P4 内容生产；用口头判断替代 validator。

## 2. 全局规则

### 2.1 步骤控制

- 主链：`P0 → P1 → (P2A|P2B) → P3 → P3.5 → P4 → P5`；分支二选一，进入后不得混跑
- 每步进入前前序 Gate 必须通过；完成后 Gate exit=0 才标 `completed`
- 失败只允许 `RETRY_CURRENT_STEP` 或 `ROLLBACK→StepID`；禁止跳步或保留损坏产物推进
- `WAIT_USER` / `WAIT_AGENT` 是硬等待点；未收到输入/FINALIZE 前禁止推进

### 2.2 Subagent 生命周期

- 显式周期：`create → RUN → STATUS… → FINALIZE → close`；完成即关，不复用
- 创建时**必须**显式传 `--model MAIN_MODEL`；禁止省略依赖默认值
- P2A/P3/P3.5/P4 步骤：主 agent 禁止内联执行内容生产，违反视为合同违规
- 图片模式 `generate` 且用户需要文生图时，额外创建 `ImageGen` 子代理；PageAgent 不承担文生图
- 所有 subagent 操作以 Section 3.1 输出的《Subagent 操作手册》为准

### 2.3 Prompt 生成

- 所有 subagent prompt 必须通过 `prompt_harness.py` 从模板生成；禁止手写
- 所有 `{{VAR}}` 必须填充，残留即 ERROR；输出固定落 `OUTPUT_DIR/runtime/`
- 模板/playbook 仅通过 `--inject-file` 注入；主 agent 不手动预读正文

### 2.4 通信协议

| 指令 | 方向 | 内容 |
|------|------|------|
| **RUN** | 主→子 | prompt 文件路径（一行，不发正文）|
| **STATUS** | 子→主 | 进度、阻塞项、下一动作 |
| **FINALIZE** | 子→主 | 完成信号 + 产物路径列表 |

仅里程碑通信；任何修复直接改文件并回传路径。

### 2.5 校验双保险

subagent FINALIZE 前自审；主 agent 回收后再跑同一 validator 复检。自审通过不等于主链放行。

### 2.6 执行纪律

- 进入 skill 后第一条对外消息必须是 Step 0 采访问题；禁止先做任何探索或读取汇报
- 主 agent **可读内容仅限**：`OUTPUT_DIR/**`、用户输入文件、`cli-cheatsheet.md`
- 脚本是执行对象：仅允许 `python3 ...` 执行；禁止 `--help`、禁止读源码；接口已固化在 cheatsheet
- 命令失败 → 查 cheatsheet 核对参数 → 仍不解决则 `BLOCKED_SCRIPT_INTERFACE` 请求用户决策
- 汇报格式：当前步骤、已执行命令、Gate 结果、下一动作（禁止 "Explored/Read…" 式清单）

### 2.7 资源双层消费

资源文件结构：`# 标题` + `> 一句话定位（引用层）` + 正文层。消费规则：

- planning 阶段：`resource_loader.py menu` 加载标题+引用层组成菜单
- html 阶段：`resource_loader.py resolve` 按 planning JSON 字段动态加载正文层
- 字段路由：`layout_hint→layouts/`、`card_type→blocks/`、`chart_type→charts/`

命令见 cheatsheet 资源路由节。

## 3. 环境、路径与产物合同

### 3.1 Step 0 前环境感知（强制）

**执行顺序（不可跳过）：**

1. `update_plan` 创建 canonical plan；读取 `cli-cheatsheet.md`
2. **模型感知**：识别当前模型版本，固化为 `MAIN_MODEL`，输出 `## 模型感知结果`
3. **Subagent 操作手册**（输出 `## Subagent 操作手册`）：自检所有 agent 创建/管理工具，确认 `--model` 穿透支持；找不到则 `BLOCKED_NO_SUBAGENT`
4. **Search 工具清单**（输出 `## Search 工具清单`）：按优先级列出（自定义 skill > 内置工具）；结果内联进 Step 2A 的 `TOOLS_AVAILABLE`
5. 能力检查：

| 能力 | 要求 | 降级 |
|------|------|------|
| 文件读写 / Python / Planning 工具 | 必须 | 缺失即停止 |
| 信息检索 | 尽量 | 缺失走 Step 2B |
| 文生图 | 可选 | 降级为 `manual_slot` / `decorate` |
| Node.js | 导出用 | 无则停在 HTML |

### 3.2 路径变量

| 变量 | 值 |
|------|----|
| `SKILL_DIR` | 当前 skill 根目录 |
| `ROOT_OUTPUT_DIR` | 用户工作目录下 `ppt-output/` |
| `RUN_ID` | `YYYYMMDD-HHMMSS-topic` |
| `OUTPUT_DIR` | `ROOT_OUTPUT_DIR/runs/{RUN_ID}` |

新任务必须新建 RUN_ID；恢复任务仅在用户明确指定后绑定旧 RUN_ID。

### 3.3 正式产物链

```text
interview-qa.txt → requirements-interview.txt
  → search.txt + search-brief.txt（research）| source-brief.txt（非 research）
  → outline.txt → style.json
  → planning/planningN.json → slides/slide-N.html → png/slide-N.png
  → preview.html → presentation-{png,svg}.pptx → delivery-manifest.json
```

运行时 prompt 落 `OUTPUT_DIR/runtime/prompt-*.md`。

## 4. Canonical Plan

```text
P0.01  采访问题组装
P0.02  [WAIT_USER] 获取回答
P0.03  写入 interview-qa.txt
P0.04  归一化 → requirements-interview.txt

P1.01  输入识别
P1.02  [WAIT_USER] 分支选择（research / 非research）

P2A.01 harness → ResearchSynth prompt
P2A.02 创建 ResearchSynth subagent
P2A.03 [WAIT_AGENT] FINALIZE
P2A.04 回收校验（search.txt + search-brief.txt）
P2A.05 [可选] 补检索
P2A.06 关闭

P2B.01 文本化预处理
P2B.02 写入 source-brief.txt
P2B.03 [如 pptx][WAIT_USER] 模式确认

P3.01  harness → Outline prompt
P3.02  创建 Outline subagent
P3.03  [WAIT_AGENT] FINALIZE（含自审）
P3.04  回收校验 outline.txt
P3.05  关闭

P3.5.01 harness → Style prompt
P3.5.02 创建 Style subagent
P3.5.03 [WAIT_AGENT] FINALIZE
P3.5.04 回收校验 style.json
P3.5.05 关闭

P4.NN.01 创建 PageAgent-NN（4A 新建 session）
P4.NN.02 harness → Planning prompt → RUN → 回收 planningNN.json
P4.NN.03 harness → HTML prompt → resume --last → 回收 slide-NN.html
P4.NN.04 harness → Review prompt → resume --last → 审查修复 → 回收验证
P4.NN.05 关闭 PageAgent-NN
（所有页并行推进）

P5.01  生成 preview.html
P5.02  PNG 导出 → presentation-png.pptx
P5.03  SVG 导出 → presentation-svg.pptx
P5.04  写入 delivery-manifest.json
```

**Plan 更新规则**：仅状态变化时更新；并行页逐页追踪不合并；create/wait/close 拆开；generate/validate 拆开；回退显式标记 `ROLLBACK→StepID`。

## 5. 调度骨架与真源

### 5.1 统一 Subagent 调度骨架（P2A/P3/P3.5/P4 共用）

1. 查 cheatsheet 对应步骤 → harness 生成 prompt 文件
2. 按《Subagent 操作手册》创建 subagent（必须传 `--model MAIN_MODEL`）
3. 发送 `RUN`（一行 prompt 路径）→ 轮询 STATUS → 收到 FINALIZE
4. 主 agent 执行 gate 复检 → 不再复用时立即 close

### 5.2 真源索引

| 类别 | 路径 | 消费方式 |
|------|------|---------|
| Prompt 模板 | `references/prompts/tpl-*.md` | 传路径给 harness，不手动预读 |
| 执行细则 | `references/playbooks/*-playbook.md` | `--inject-file` 注入 |
| 风格真源 | `references/styles/runtime-style-*.md` | Step 3.5 注入 |
| CLI 命令 | `references/cli-cheatsheet.md` | Step 0 前读取，后续直接引用 |

`CURRENT_BRIEF_PATH`：research → `search-brief.txt`；非 research → `source-brief.txt`（Step 3/4 共用）。

## 6. 主流程状态机

### 6.1 Step 全景表

| Step | 核心动作 | 关键产物 | Gate | 失败回退 |
|------|---------|---------|------|---------|
| P0 | 采访并归一化需求 | interview-qa.txt / requirements-interview.txt | `contract_validator interview` + `requirements-interview` | 补问，不进 P1 |
| P1 | 识别输入确定分支 | 分支写入 requirements-interview.txt | 逻辑判断 | WAIT_USER |
| P2A | 检索并压缩资料 | search.txt / search-brief.txt | `contract_validator search` + `search-brief` | 同 agent 追加检索 |
| P2B | 压缩用户现有资料 | source-brief.txt | `contract_validator source-brief` | 回 P2B 重写 |
| P3 | 生成大纲（内部自审） | outline.txt | `contract_validator outline` | 同 agent 修复，最多 2 轮 |
| P3.5 | 固定全局风格 | style.json | `contract_validator style` | 回 P3.5 |
| P4 | 并行生产各页 | planningN.json / slide-N.html / slide-N.png | `planning_validator` + 文件存在性 | 只回退该页，整页重跑 |
| P5 | 导出交付 | preview.html / 双 pptx / delivery-manifest.json | `contract_validator delivery-manifest` | 只回退导出 |

> 所有命令完整参数见 `cli-cheatsheet.md`。

### 6.2 Step 0 采访（不可跳过）

必须覆盖：场景、受众、目标动作、页数与密度、风格、品牌、必含、必避、语言、配图模式（AI 文生图/手动补图/无外部图）、资料使用策略。允许精简已知项，但隐含选项不可省略。

### 6.3 Step 1 分流

识别输入类型（大段文本/单文件/多文件/pptx）→ 询问分支 → 写入 requirements-interview.txt。

### 6.4 Step 2A Research

`search-brief.txt` 必须含 PPTX 结构化数据包（metrics/comparisons/timelines 等 ≥3 种类型）。质量不足时允许回同一 subagent 追加检索后再关闭。

### 6.5 Step 2B 非 Research

大段文本写临时文件 → 多文件文本化（markitdown）→ 读前 1000 字建立主题 → 写 source-brief.txt。若 pptx 输入：强制询问模式（美化/重构/美化+重构）。

### 6.6 Step 3 大纲

subagent 内部完成：初稿 → 自审 → 修复 → FINALIZE；自审不通过直接改文件，主 agent 不另开审查 subagent。

### 6.7 Step 3.5 风格

输入：需求 + 大纲 + runtime 风格规则 + 预置风格入口。输出：planning 与 html 可稳定消费的完整 `style.json`。

### 6.8 Step 4 页面生产（并行 + 三阶段解耦）

每页一个 `PageAgent-NN`，三阶段共用同一 session（保留设计记忆）：

| 阶段 | 操作 | 产物 |
|------|------|------|
| 4A Planning | `codex exec -m MAIN_MODEL` 新建 session | planningN.json（自审过）|
| 4B HTML | `codex exec resume --last` 续接 | slide-N.html |
| 4C Review | `codex exec resume --last` 续接；按 10 维度审查，最多 3 轮修复 | slide-N.png |

- **所有页并行推进**；前置阶段 FINALIZE + Gate 通过才发下一阶段指令
- **subagent 死亡 = 上下文全无**：触发重试时 session 不可续接，整页并行重跑（见 Section 7）
- 通过条件：三件套存在 + `planning_validator` 通过 + 图片策略闭环

### 6.9 Step 5 交付

双管线（PNG/SVG）并行；导出失败只回退导出，不回退内容生产。命令见 cheatsheet Step 5。

## 7. 重试与恢复

**原则：只信文件与 Gate 校验，不信口头记忆或 session 状态。**

### 7.1 Step 4 重试（两步走）

**第一步：侦查** — 扫描所有页，收集触发条件（任一成立）的页号：
- `slide-N.html` 不存在或为空
- `slide-N.png` 视觉审查不通过

**第二步：并行重跑** — 收集完毕后，一次性并行启动所有缺失页：清三件套 → 并行 `codex exec`（各自新建 session，4A→4B→4C）。

单页连续 3 次失败 → 标记 `BLOCKED_PAGE_N`，先跳过推进其余页，最后集中处理。

### 7.2 跨对话断点恢复

触发：用户说「继续/恢复」并提供 RUN_ID（或默认取最新目录）。

1. `update_plan` 重建 canonical plan；绑定旧 RUN_ID
2. 里程碑探测（从高到低，第一个 exit=0 为最高通过点）：

```bash
contract_validator.py delivery-manifest ...                  # P5
planning_validator.py ...                                    # P4
contract_validator.py style ...                              # P3.5
contract_validator.py outline ...                            # P3
contract_validator.py search-brief ... | source-brief ...   # P2
contract_validator.py requirements-interview ...             # P0/P1
```

3. 从下一未完成 step 继续；前序 Gate 失败则回退重做
4. Step 4：读 `outline.txt` 确认总页数 → 侦查所有页三件套 → 并行重跑缺失页（旧 session 全部失效）

**禁止**：依赖旧 session、跳过侦查、串行逐页处理、恢复时新建 RUN_ID（除非用户要求全新开始）。
