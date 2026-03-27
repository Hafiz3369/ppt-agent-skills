---
name: ppt-agent
description: 专业 PPT 演示文稿全流程 AI 生成助手。模拟顶级 PPT 设计公司的完整工作流（需求调研 -> 资料搜集 -> 大纲策划 -> 策划稿 -> 设计稿），输出高质量 HTML 格式演示文稿。当用户提到制作 PPT、做演示文稿、做 slides、做幻灯片、做汇报材料、做培训课件、做路演 deck、做产品介绍页面时触发此技能。即使用户只说"帮我做个关于 X 的介绍"或"我要给老板汇报 Y"，只要暗示需要结构化的多页演示内容，都应该触发。也适用于用户说"帮我把这篇文档做成 PPT"、"把这个主题做成演示"等需要将内容转化为演示格式的场景。
---

# PPT Agent -- 主控制台合同

## 1. 主控制台原则

这份 `SKILL.md` 只负责四件事：

1. 定义主状态机
2. 定义每一步硬门槛
3. 定义正式产物合同
4. 定义失败回退与恢复规则

主 agent 是**控制台**，不是内容生产者。主 agent 只做：

- 列计划并更新步骤状态
- 校验节点文件是否存在、是否合法、是否可进入下一步
- 调用脚本组装 sub-agent prompt / packet
- 拉起、监控、传递文件、回收、关闭 / 终止 sub-agent
- 与用户交互：问卷、planning 确认、preview 确认、导出选择

主 agent 不做：

- 代替 Step 2 / Step 3 / Step 4 / Step 5c / Step 5d 直接产出内容
- 在主线程里深读 playbook 然后口头转述给 sub-agent
- 在 `SKILL.md` 里内嵌或复述 sub-agent prompt 模板
- 通过“我看起来差不多”来判断能否进入下一步

**硬规则**：

- 主进程推进节点是否放行，只依赖：
  - 节点文件存在性
  - validator / harness exit code
  - 计数一致性
  - 用户确认
- sub-agent 发送材料以脚本组装为基座：
  - `scripts/subagent_prompt_assembler.py`
  - `scripts/prompt_assembler.py`
  - `scripts/final_review_harness.py`
- 主 agent 可以在脚本组装结果上追加**必要运行上下文**，例如：
  - 当前轮次 / 批次边界
  - 最新用户反馈
  - validator / harness 报错摘要
  - 本轮返工目标
  - 优先级提醒
- 主 agent 追加信息的边界：
  - 可以补充运行信息，不能覆盖正式文件真源
  - 不能口头改写 `requirements / outline / planning / style` 合同
  - 不能用追加信息替代节点校验
- `SKILL.md` 不再承载 sub-agent prompt 正文

---

## 2. 环境感知

开始前检查可用能力：

| 能力 | 要求 | 降级规则 |
|------|------|---------|
| 信息获取 | 尽量有 | 缺失时依赖用户材料 |
| 文件输出 | 必须有 | 无则停止 |
| Python 脚本执行 | 必须有 | 无则停止标准工作流 |
| Node.js | 导出时尽量有 | 无则只能停在 HTML / 建议改管线 |
| Planning 工具 | 有则必用 | 无则在对话中列等价计划 |
| Sub-agent 能力 | 有且用户已授权时必用 | 无或未授权则停止标准工作流，不静默退回主 agent 代做 |

**最前置动作（强制）**：

- 进入 Step 0 前，必须先向用户明确请求 sub-agent 使用授权，并获得明确同意。
- 未获授权时，流程停在授权等待态；不得创建任何 sub-agent，不得进入 Step 0 及后续步骤。

**授权口径**：

- 只有同时满足“环境可调 sub-agent” + “用户明确授权 delegation / subagent / 并行代理”，Step 2 / Step 3 / Step 4 / Step 5a / Step 5b / Step 5c / Step 5d 才能按标准工作流执行。
- 一旦满足授权，返工必须新开干净 sub-agent，不复用旧会话。

---

## 3. 路径约定

| 变量 | 含义 |
|------|------|
| `SKILL_DIR` | 当前 skill 根目录 |
| `ROOT_OUTPUT_DIR` | 用户工作目录下的 `ppt-output/` |
| `RUN_ID` | 本次运行唯一标识（建议：`YYYYMMDD-HHMMSS-主题slug`） |
| `OUTPUT_DIR` | `ROOT_OUTPUT_DIR/runs/{RUN_ID}` |

隔离规则（同目录多次运行）：

- 每次新开工必须新建 `RUN_ID`，不得复用旧 `OUTPUT_DIR`。
- 全部正式产物与运行文件只允许写入当前 `OUTPUT_DIR`。
- 仅在用户明确要求“恢复某次运行”时，才允许绑定到既有 `RUN_ID`。
- 未指定恢复目标时，默认使用 `ROOT_OUTPUT_DIR/latest`（软链接或等价记录）指向最近一次运行。

正式产物真源固定为：

```text
requirements.json
  -> raw-research.json
  -> research-package.json
  -> outline.json
  -> outline-review-round-{n}.json
  -> planning/planning{n}.json
  -> style.json
  -> images/*
  -> prompts-ready/prompt-ready-{NN}.txt
  -> slides/slide-{NN}.html
  -> reviews/final-review-round-{n}.json
  -> preview.html
  -> presentation.pptx
```

`progress.json` 是必需运行账本：Step 1 开始前必须存在并通过 `scripts/progress_validator.py --require-pre-step1`。
它用于恢复与进度审计；是否放行下一节点仍以正式产物 + validator / harness 结果为准，不替代主链真源。

---

## 4. 计划工具

如果当前模型带 planning / `update_plan` 能力，开工前必须创建固定 canonical plan，并在状态变化时更新。

固定步骤：

1. `Step -1 获取用户 sub-agent 使用授权`
2. `Step 0 生成 RUN_ID / 初始化 progress.json 并校验`
3. `Step 1 搜索准备与需求问卷生成`
4. `等待用户回复需求问卷`
5. `写入 requirements.json`
6. `Step 2 research sub-agent -> raw-research.json`
7. `Step 2 material-prep sub-agent -> research-package.json`
8. `Step 3 outline sub-agent -> outline.json`
9. `Step 3 outline-review sub-agent -> outline-review-round-{n}.json`
10. `Step 4 planning sub-agent -> planning/*.json`
11. `等待用户确认 / 修改 planning`
12. `Step 5a 风格决策 -> style.json`
13. `Step 5b 配图生成（如需要）`
14. `Step 5c html sub-agent -> slides/*.html`
15. `Step 5d reviewer sub-agent -> reviews/final-review-round-{n}.json`
16. `生成 preview.html 并等待用户确认`
17. `Step 6 管线选择与导出交付`

规则：

- 不得合并步骤，不得删除前序步骤
- 同一时刻只能有一个 `in_progress`
- 拉起 sub-agent 前，先把对应 step 标成 `in_progress`

---

## 5. 复杂度与调度

| 复杂度 | 页数 | 调研 | 搜索 | Step 4 | Step 5c |
|------|------|------|------|--------|---------|
| `light` | `<= 8` | 5 题精简版 | 3-5 查询 | 允许只拆 1 个批次；若拆成多批次，则批次之间并行 | 允许只开 1 个批次；若拆成多批次，则批次之间并行 |
| `standard` | `9-18` | 完整问卷 | 8-12 查询 | 按 Part 分组 | 默认并行 |
| `large` | `> 18` | 完整问卷 | 10-15 查询 | 按 Part 分组 | 默认并行 |

轻量任务可以减少批次数，但**不能断业务闭环**。一旦拆成多批次，批次之间默认并行；不得把多批次串行化。`Step 3` 大纲审查与 `Step 5d` 终审始终保留。

---

## 6. 主流程

### Step -1: 获取 sub-agent 使用授权（必须）

**目标**：在任何业务步骤开始前，拿到用户对 sub-agent 的明确授权

**执行**：

- 主 agent 必须先询问用户是否授权使用 sub-agent（delegation / subagent / 并行代理）
- 仅在用户明确同意后，才允许进入 Step 0

通过条件：

- 用户明确授权 sub-agent

失败回退：

- 未授权时停在 Step -1
- 不得创建 sub-agent
- 不得进入 Step 0 及后续步骤

---

### Step 0: 开工前门槛（必须）

**目标**：为本次任务绑定隔离目录，并确保 `OUTPUT_DIR/progress.json` 已初始化且可恢复

**执行**：

- 新任务：生成新 `RUN_ID`，并设置 `OUTPUT_DIR=ROOT_OUTPUT_DIR/runs/{RUN_ID}`
- 恢复任务：使用用户指定 `RUN_ID`，或默认绑定 `ROOT_OUTPUT_DIR/latest` 所指向的运行目录
- 更新 `ROOT_OUTPUT_DIR/latest` 指向当前运行目录（软链接或等价记录）

**硬门槛**：

```bash
python3 SKILL_DIR/scripts/progress_validator.py \
  OUTPUT_DIR/progress.json \
  --require-pre-step1
```

通过条件：

- `OUTPUT_DIR` 已绑定到唯一运行目录
- `progress.json` 存在
- validator exit code = 0

失败回退：

- 不得进入 Step 1
- 运行目录冲突（新任务误用旧目录）时，重新生成 `RUN_ID`
- 缺文件或校验失败时，先修复 `progress.json`（字段补齐、状态归零）后重试

---

### Step 1: 需求调研

**目标**：产出 `OUTPUT_DIR/requirements.json`

**执行**：

- 必须读取 `references/prompts/prompt-1-research.md`
- 必须提问并等待用户回复
- 问题包必须覆盖：
  - 场景
  - 受众
  - 目的
  - 叙事结构
  - 内容侧重
  - 说服力要素
  - 风格选择
  - 页数 / 信息密度
  - 品牌信息
  - 必含 / 必避
  - 语言
  - 配图偏好
  - 0-3 个动态追问

**轻量模式**：

- 只问 `Q1 + Q2 + Q7 + Q8 + Q12`

**硬门槛**：

```bash
python3 SKILL_DIR/scripts/contract_validator.py requirements OUTPUT_DIR/requirements.json
```

通过条件：

- `requirements.json` 存在
- validator exit code = 0

失败回退：

- 留在 Step 1，补问或补字段，不得进入 Step 2

---

### Step 2: 资料搜集

**目标**：

- `OUTPUT_DIR/raw-research.json`
- `OUTPUT_DIR/research-package.json`

**主控制台动作**：

1. 先验证 Step 1 已通过
2. 用脚本组装 research sub-agent prompt
3. 拉起 `research` sub-agent
4. 回收并关闭
5. 校验 `raw-research.json`
6. 用脚本组装 material-prep sub-agent prompt
7. 拉起 `material-prep` sub-agent
8. 回收并关闭
9. 校验 `research-package.json`

**组装入口**：

```bash
python3 SKILL_DIR/scripts/subagent_prompt_assembler.py research \
  --requirements OUTPUT_DIR/requirements.json \
  --output OUTPUT_DIR/raw-research.json \
  --prompt OUTPUT_DIR/runtime/research-prompt.txt

python3 SKILL_DIR/scripts/subagent_prompt_assembler.py material-prep \
  --requirements OUTPUT_DIR/requirements.json \
  --raw-research OUTPUT_DIR/raw-research.json \
  --output OUTPUT_DIR/research-package.json \
  --prompt OUTPUT_DIR/runtime/material-prep-prompt.txt
```

**硬门槛**：

```bash
python3 SKILL_DIR/scripts/contract_validator.py raw-research OUTPUT_DIR/raw-research.json
python3 SKILL_DIR/scripts/contract_validator.py research-package OUTPUT_DIR/research-package.json
```

通过条件：

- 两个节点文件都存在
- 两个 validator 都通过

失败回退：

- `raw-research` 不合法 -> 回退到 research sub-agent
- `research-package` 不合法 -> 回退到 material-prep sub-agent

---

### Step 3: 大纲策划

**目标**：

- `OUTPUT_DIR/outline.json`
- `OUTPUT_DIR/outline-review-round-{n}.json`

**主控制台动作**：

1. 先验证 Step 2 已通过
2. 组装 outline sub-agent prompt
3. 拉起 `outline` sub-agent，生成 `outline.json`
4. 回收并关闭
5. 组装 outline-review sub-agent prompt
6. 拉起 `outline-review` sub-agent
7. 回收并关闭
8. 校验 review 结果
9. 不通过则新开 outline / outline-review 回路

**组装入口**：

```bash
python3 SKILL_DIR/scripts/subagent_prompt_assembler.py outline \
  --requirements OUTPUT_DIR/requirements.json \
  --research-package OUTPUT_DIR/research-package.json \
  --output OUTPUT_DIR/outline.json \
  --prompt OUTPUT_DIR/runtime/outline-prompt.txt

python3 SKILL_DIR/scripts/subagent_prompt_assembler.py outline-review \
  --requirements OUTPUT_DIR/requirements.json \
  --research-package OUTPUT_DIR/research-package.json \
  --outline OUTPUT_DIR/outline.json \
  --output OUTPUT_DIR/outline-review-round-1.json \
  --prompt OUTPUT_DIR/runtime/outline-review-prompt.txt
```

**硬门槛**：

```bash
python3 SKILL_DIR/scripts/contract_validator.py outline-review \
  OUTPUT_DIR/outline-review-round-1.json \
  --require-pass
```

通过条件：

- `outline.json` 存在
- 最新一轮 `outline-review-round-{n}.json` 存在
- review validator 通过且 `verdict = pass`

失败回退：

- 回退到 outline 编写者
- 最多 2 轮
- 第 2 轮仍不通过，展示问题给用户决定

---

### Step 4: 内容分配与策划稿

**目标**：

- `OUTPUT_DIR/planning/planning{n}.json`

**执行细则**：

- 由 `references/playbooks/planning-subagent-playbook.md` 与 `references/prompts/prompt-3-planning.md` 承担
- 主控制台不再手读 planning prompt 细节

**主控制台动作**：

1. 验证 Step 3 已通过
2. 按复杂度决定页范围与批次数
3. 用脚本组装 planning sub-agent prompt
4. 若拆成多个页范围批次，批次之间并行拉起 planning sub-agent
5. 回收并关闭
6. 运行单页 / 全量 validator
7. 展示 planning 给用户确认

**组装入口**：

```bash
python3 SKILL_DIR/scripts/subagent_prompt_assembler.py planning \
  --requirements OUTPUT_DIR/requirements.json \
  --research-package OUTPUT_DIR/research-package.json \
  --outline OUTPUT_DIR/outline.json \
  --output-dir OUTPUT_DIR/planning \
  --page-range 1-8 \
  --prompt OUTPUT_DIR/runtime/planning-prompt.txt
```

**硬门槛**：

```bash
python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning --refs SKILL_DIR/references
python3 SKILL_DIR/scripts/contract_validator.py images OUTPUT_DIR/planning
```

通过条件：

- `planning/` 存在且包含全部页面
- `scripts/planning_validator.py` exit code = 0
- image contract validator exit code = 0
- 用户确认或修改完 planning

失败回退：

- validator 失败 -> 回退到 planning sub-agent
- 用户改动后 -> 重新跑 validator，再进 Step 5

---

### Step 5a: 风格决策

**目标**：

- `OUTPUT_DIR/style.json`

**主控制台动作**：

1. 验证 Step 4 已通过
2. 组装 style sub-agent prompt
3. 拉起 style sub-agent
4. 回收并关闭
5. 校验 `style.json`

**组装入口**：

```bash
python3 SKILL_DIR/scripts/subagent_prompt_assembler.py style \
  --requirements OUTPUT_DIR/requirements.json \
  --outline OUTPUT_DIR/outline.json \
  --output OUTPUT_DIR/style.json \
  --prompt OUTPUT_DIR/runtime/style-prompt.txt
```

**硬门槛**：

```bash
python3 SKILL_DIR/scripts/contract_validator.py style OUTPUT_DIR/style.json
```

通过条件：

- `style.json` 存在
- validator exit code = 0

失败回退：

- 回退到 style sub-agent

---

### Step 5b: 配图生成（条件执行）

**目标**：

- `OUTPUT_DIR/images/*`

**主控制台动作**：

- 只在 `image_preference != none / 不需要` 时执行
- 先检查 planning 中的 image contract
- 组装 image sub-agent prompt
- 拉起 image sub-agent
- 回收并关闭
- 生成后再检查 path 是否已回填且文件存在

**组装入口**：

```bash
python3 SKILL_DIR/scripts/subagent_prompt_assembler.py image \
  --planning OUTPUT_DIR/planning \
  --style OUTPUT_DIR/style.json \
  --output-dir OUTPUT_DIR/images \
  --prompt OUTPUT_DIR/runtime/image-prompt.txt
```

**硬门槛**：

```bash
python3 SKILL_DIR/scripts/contract_validator.py images OUTPUT_DIR/planning
python3 SKILL_DIR/scripts/contract_validator.py images OUTPUT_DIR/planning --require-paths
```

通过条件：

- 如需要配图：两次 image validator 都通过
- 如不需要配图：Step 5b 标记 `skipped`

失败回退：

- 前置 image contract 不合法 -> 回退到 Step 4
- 图片已生成但 path / 文件缺失 -> 回退到 image sub-agent

---

### Step 5c: HTML 设计稿生成

**目标**：

- `OUTPUT_DIR/prompts-ready/prompt-ready-{NN}.txt`
- `OUTPUT_DIR/slides/slide-{NN}.html`

**主控制台动作**：

1. 验证 Step 4 / Step 5a / Step 5b 已通过
2. 运行 `scripts/prompt_assembler.py design`
3. 检查 `prompt-ready` 数量是否与 planning 页数一致
4. 用脚本组装 HTML sub-agent prompt
5. 若拆成多个 HTML 批次，批次之间并行拉起 HTML sub-agent
6. 回收并关闭
7. 检查 `slides` 数量是否与 planning 页数一致

**组装入口**：

```bash
python3 SKILL_DIR/scripts/prompt_assembler.py design \
  --planning OUTPUT_DIR/planning \
  --style OUTPUT_DIR/style.json \
  --all \
  --output-dir OUTPUT_DIR/prompts-ready \
  --self-contained

python3 SKILL_DIR/scripts/subagent_prompt_assembler.py html \
  --page 1 \
  --prompt-ready OUTPUT_DIR/prompts-ready/prompt-ready-01.txt \
  --planning OUTPUT_DIR/planning/planning1.json \
  --output OUTPUT_DIR/slides/slide-01.html \
  --prompt OUTPUT_DIR/runtime/html-page-01-prompt.txt
```

**硬门槛**：

- `prompts-ready/` 存在
- `prompt-ready` 文件数 = planning 页数
- `slides/` 存在
- `slide` 文件数 = planning 页数

轻量任务可以只开 1 个 HTML 批次；一旦拆成多批次，批次之间并行。主 agent 仍然只做控制台，不亲自写页面。

失败回退：

- `prompt-ready` 缺页 -> 回退到 `scripts/prompt_assembler.py`
- `slides` 缺页 -> 回退到对应 HTML sub-agent

---

### Step 5d: 强制终审

**目标**：

- `OUTPUT_DIR/reviews/reviewer-prompt.txt`
- `OUTPUT_DIR/reviews/final-review-round-{n}.json`

**主控制台动作**：

1. 尽量先生成 PNG
2. 用 harness 组装 reviewer prompt
3. 拉起 reviewer sub-agent
4. 回收并关闭
5. 用 harness validate
6. 若需修复则重新 assemble，换新 reviewer

**组装入口**：

```bash
python3 SKILL_DIR/scripts/html2png.py OUTPUT_DIR/slides -o OUTPUT_DIR/png --scale 2

python3 SKILL_DIR/scripts/final_review_harness.py assemble \
  OUTPUT_DIR \
  -o OUTPUT_DIR/reviews/reviewer-prompt.txt \
  --review-mode auto

python3 SKILL_DIR/scripts/final_review_harness.py validate \
  OUTPUT_DIR/reviews/final-review-round-1.json \
  --pages 15
```

**硬门槛**：

- 终审必须隔离 reviewer 执行
- 终审优先 PNG；没有 PNG 时自动退回 source 审查
- `scripts/final_review_harness.py validate` 必须通过
- 只有 Step 5d 通过后，才允许生成 `preview.html`

失败回退：

- 留在 Step 5d
- reviewer 每轮回收后必须关闭
- 不得让同一 reviewer 自检

---

### Step 5d 后：用户预览

```bash
python3 SKILL_DIR/scripts/html_packager.py OUTPUT_DIR/slides -o OUTPUT_DIR/preview.html
```

通过条件：

- `preview.html` 存在
- 用户确认 HTML，或修改后重新进入 Step 5d

---

### Step 6: 导出交付

**目标**：

- `OUTPUT_DIR/presentation.pptx`

**规则**：

- 用户必须在 PNG / SVG 管线中明确选择
- 不允许跳过导出直接结束

**PNG 管线**：

```bash
python3 SKILL_DIR/scripts/html2png.py OUTPUT_DIR/slides -o OUTPUT_DIR/png --scale 2
python3 SKILL_DIR/scripts/png2pptx.py OUTPUT_DIR/png -o OUTPUT_DIR/presentation.pptx
```

**SVG 管线**：

```bash
python3 SKILL_DIR/scripts/html2svg.py OUTPUT_DIR/slides -o OUTPUT_DIR/svg
python3 SKILL_DIR/scripts/svg2pptx.py OUTPUT_DIR/svg -o OUTPUT_DIR/presentation.pptx --html-dir OUTPUT_DIR/slides
```

通过条件：

- 目标管线产物存在
- `presentation.pptx` 存在

失败回退：

- 管线依赖缺失 -> 告知用户并建议改用另一条管线

---

## 7. 失败回退总表

| 当前节点 | 检查方式 | 失败回退 |
|---------|---------|---------|
| sub-agent 授权 | 用户明确同意 | Step -1 |
| 运行目录隔离 | `OUTPUT_DIR` 与 `RUN_ID` 一一对应 | Step 0 |
| `progress.json` | `scripts/progress_validator.py --require-pre-step1` | Step 0 |
| `requirements.json` | `scripts/contract_validator.py requirements` | Step 1 |
| `raw-research.json` | `scripts/contract_validator.py raw-research` | research sub-agent |
| `research-package.json` | `scripts/contract_validator.py research-package` | material-prep sub-agent |
| `outline-review-round-{n}.json` | `scripts/contract_validator.py outline-review --require-pass` | Step 3 |
| `planning/*.json` | `scripts/planning_validator.py` | Step 4 |
| planning image 合同 | `scripts/contract_validator.py images` | Step 4 |
| `style.json` | `scripts/contract_validator.py style` | Step 5a |
| 图片 path | `scripts/contract_validator.py images --require-paths` | Step 5b |
| `prompts-ready/*` | 文件数校验 | `scripts/prompt_assembler.py` |
| `slides/*` | 文件数校验 | Step 5c |
| `final-review-round-{n}.json` | `scripts/final_review_harness.py validate` | Step 5d |
| `preview.html` | 文件存在 + 用户确认 | Step 5d |
| `presentation.pptx` | 文件存在 | Step 6 |

---

## 8. 恢复规则

中断恢复时，主控制台只做以下检查：

1. 是否已有用户明确的 sub-agent 授权；无授权时回到 Step -1
2. 绑定目标 `RUN_ID`（用户指定优先；否则 `latest`）
3. `progress.json` 是否存在且 `scripts/progress_validator.py` 通过
4. 前序正式产物是否存在
5. 对应 validator / harness 是否能通过
6. 找到第一个未完成节点并从那里继续

若任一前序节点不合法，直接回退到该节点重做，不依赖口头记忆。

恢复辅助说明见：

- `references/ops/workflow-ops.md`

---

## 9. 运行入口索引

主控制台常用入口只保留这些：

- 用户问卷：`references/prompts/prompt-1-research.md`
- research prompt 组装：`scripts/subagent_prompt_assembler.py` 的 `research` 子命令
- material-prep prompt 组装：`scripts/subagent_prompt_assembler.py` 的 `material-prep` 子命令
- outline / outline-review prompt 组装：`scripts/subagent_prompt_assembler.py` 的 `outline` / `outline-review` 子命令
- planning prompt 组装：`scripts/subagent_prompt_assembler.py` 的 `planning` 子命令
- style / image prompt 组装：`scripts/subagent_prompt_assembler.py` 的 `style` / `image` 子命令
- planning 合法性：`scripts/planning_validator.py`
- progress 合法性：`scripts/progress_validator.py`
- requirements / research / style / image / outline-review 合法性：`scripts/contract_validator.py`
- design prompt 组装：`scripts/prompt_assembler.py` 的 `design` 子命令
- html sub-agent prompt 组装：`scripts/subagent_prompt_assembler.py` 的 `html` 子命令
- reviewer packet：`scripts/final_review_harness.py` 的 `assemble` / `validate` 子命令
- preview 打包：`scripts/html_packager.py`
- 导出：`scripts/html2png.py` / `scripts/html2svg.py` / `scripts/png2pptx.py` / `scripts/svg2pptx.py`

执行细则真源在：

- `references/playbooks/research-subagent-playbook.md`
- `references/playbooks/material-prep-subagent-playbook.md`
- `references/playbooks/outline-subagent-playbook.md`
- `references/playbooks/outline-review-subagent-playbook.md`
- `references/playbooks/planning-subagent-playbook.md`
- `references/playbooks/html-subagent-playbook.md`
- `references/playbooks/review-subagent-playbook.md`

主控制台只引用这些文件，不在 `SKILL.md` 里重复抄执行细节。
