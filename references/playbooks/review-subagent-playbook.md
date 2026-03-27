# Final Review Sub-agent Playbook

## 目录

- 何时读取
- 目标
- 审查合同
- 资料包（6 层上下文链）
- 评分维度与标准
- 打回诊断规则
- 通信与生命周期
- Reviewer Sub-agent 执行边界
- Reviewer Sub-agent Prompt 模板
- 主 agent 的回收职责

## 何时读取

- 当 Step 5c 所有 slide HTML 生成完毕后，**立即进入 Step 5d 强制终审**时读取
- 当当前运行的是 harness 终审模式时必读
- 当打回修复后需要重新审查时回读

## 目标

从零读取完整的上下文链（需求 -> 大纲 -> 策划 -> 风格 -> HTML），以独立第三方视角执行高标准质量审查。

这份 playbook 的重点不是"检查 CSS 对不对"，而是：

1. 怎样利用完整上下文链精准定位问题出在哪一层
2. 怎样用高标准评分区分"及格"和"万元级"
3. 怎样对不达标的页面直接修改（你已有完整上下文，修改最精准）

## 审查合同

### 你是谁

你是独立质量审查员。你与生成者完全隔离，没有任何生成阶段的记忆。你从文件中从零读取所有资料，然后独立判断。

### 你的判断标准

9 分 = 通过线。你的默认心态是“这份 PPT 应该值万元/页”，给分要手紧，不要因为“整体还行”就放水。

### 你的职责

这是一个**独立的 harness 终审回路**，位于用户预览确认之前，是 SKILL.md Step 5d 的强制步骤。主 agent 把当前产物送入该回路后，你立即接管终审。

一旦进入该回路，**终审必须由隔离 reviewer sub-agent 执行**。主 agent 不得自己兼任 reviewer，也不得跳过 harness 组装/校验步骤。

在这个 harness 回路中，你既审又改 -- 评分后，对不达标的页面**直接修改对应文件**（planning JSON / slide HTML / style.json）。你已有完整上下文链，修改比主 agent 做中间人更精准。

修改后不自检（自己改自己检毫无意义），主 agent 会另起一个新的 reviewer sub-agent 从零审查你的修改。

## PPT 生产 Pipeline（你需要知道的上下游关系）

```
Step 1: 需求调研 → requirements.json（默认文件名，兼容旧 requirement.json；用户要什么、受众、场景）
Step 3: 大纲策划 → outline.json（叙事结构、Part 划分、页面目标）
Step 4: 逐页策划 → planning/*.json（每页的内容、布局、卡片、数据）
Step 5a: 风格决策 → style.json（配色、装饰、字体）
Step 5c: HTML 生成 → slides/*.html（最终视觉产物）
截图:   HTML → PNG → png/*.png（有读图能力时的默认审查输入）
或
源码:   slides/*.html（无读图能力时的强制 fallback 审查输入）
```

**问题定位逻辑**：
- 看 PNG 觉得**内容空洞** → 问题可能在 planning（没写内容）或 HTML（没渲染）→ 先读 planning，再读 HTML
- 看 PNG 觉得**叙事断裂** → 问题可能在 outline（结构设计）或 planning（衔接丢失）→ 先读 outline，再读 planning
- 看 PNG 觉得**布局难看** → 问题在 HTML → 读 planning（看设计意图）+ HTML（看实现）
- 看 PNG 觉得**配色奇怪** → 问题可能在 style.json 或 HTML → 读 style.json + HTML
- **最终修改都落在 HTML 上**（改 planning 后也要重生 HTML）

## 资料包（精简 prompt + 按需 view_file）

> **不把所有文件塞进上下文（tokens 爆炸）。** prompt 只内联评分标准 + 文件路径清单。你通过 `view_file` 按需读取文件。

### prompt 中已有的内容（不需要额外读取）

- 评分标准（6 维逐页 + 3 维全局）
- 修改规则 + 输出格式
- `OUTPUT_DIR` 路径 + 文件路径清单

### 你按需 view_file 的文件

| 资料 | 路径 | 何时读取 |
|------|------|----------|
| **PNG 截图** | `png/slide-{NN}.png` | **vision 模式下每页必看** -- 看图评分，不读源码 |
| **大纲 JSON** | `outline.json` | 内容/叙事问题时（信息密度/叙事贡献 < 9） |
| **策划稿 JSON** | `planning/planning{n}.json` | 设计/内容问题时（视觉冲击力/信息密度 < 9） |
| **style.json** | `style.json` | 色彩/风格问题时（色彩执行/风格统一 < 9） |
| **slide HTML** | `slides/slide-{NN}.html` | **需要修改时才读取** -- 最终修改都落在 HTML |
| **需求 JSON** | 默认 `requirements.json`（兼容旧 `requirement.json`） | 受众/场景问题时 |

### 工作流程（按需读取，极省 tokens）

```
逐页循环：
  vision 模式：
    1. view_file png/slide-{NN}.png
    2. 全部 >= 9？→ 记录分数，下一页
    3. 有 < 9 的维度？→ 按诊断需要读取 planning/style/html

  source 模式：
    1. view_file slides/slide-{NN}.html
    2. 检查页面正文是否完整承载 planning 合同、是否存在规则泄漏、布局/层级/data-* 是否成立
    3. 有 < 9 的维度？→ 按诊断需要读取 planning/style/outline

  通用修复：
    - 修改 planning → 重跑 prompt_assembler → 重新生成 HTML
    - 修改 style.json → 重新生成相关 HTML
    - 修改 HTML → 直接改
    - 所有修改最终都落在 HTML 上

全局评分：逐页完成后，综合评 3 维全局（叙事连贯性/视觉节奏/风格统一）
```

> **Token 效率**：15 页 PPT，12 页达标 3 页不达标 = 15 张 PNG + 3 页的源文件。比全量内联省 80%+ tokens。
>
> **当前实现注意**：`scripts/final_review_harness.py assemble` 支持 `--review-mode vision|source|auto`。有 PNG 就优先 `vision`；无读图能力时必须改用 `source`，不能跳过终审。

## 评分维度与标准

### 逐页评分（6 维度，每维 1-10 分）

| 维度 | key | 权重 | 9 分标准（通过线） | 10 分标准（无懈可击） |
|------|-----|------|---------|----------|
| **信息密度** | `info_density` | 20% | 每张卡片有标题+正文+数据，无空卡 | 数据精准有力，每个要点都有 source 背书，信息量匹配受众认知水平 |
| **视觉冲击力** | `visual_impact` | 25% | 有明确设计感，不像普通前端页面 | 布局灵动、装饰有呼吸感、一眼看出是万元/页级专业 PPT |
| **布局精度** | `layout_precision` | 15% | 无重叠、无溢出、grid 定位正确 | 骨架消费精准，跨行跨列流畅，留白比例恰到好处 |
| **色彩执行** | `color_execution` | 10% | 全部通过 CSS 变量，accent <= 2 种 | 色彩层次丰富，60-30-10 法则执行完美 |
| **资源消费** | `resource_consumption` | 10% | planning 中指定的 layout/card_type/chart_type 在 HTML 中体现 | prompt-ready 中 `[PAGE_TEMPLATE]` / `[LAYOUT]` / `[BLOCKS]` / `[CHARTS]` / `[PRINCIPLES]` 资源分区都被深度消费 |
| **叙事贡献** | `narrative_contribution` | 20% | 该页角色清晰，与前后页有逻辑衔接 | 情感弧线贡献显著，过渡自然，读者被"推着走" |

### 全局评分（3 维度，每维 1-10 分）

| 维度 | key | 9 分标准 | 10 分标准 |
|------|-----|---------|----------|
| **叙事连贯性** | `narrative_coherence` | 页间有逻辑递进，结尾有收束 | 金字塔原理贯穿，情感弧线完整，结尾呼应开头让人想鼓掌 |
| **视觉节奏** | `visual_rhythm` | 不连续 3 页高密度，布局不全重复 | 密度交替像呼吸，重心跳变像音乐，visual_weight 起伏自然 |
| **风格统一** | `style_consistency` | 跨页配色/字体不走形 | 装饰 DNA 贯穿始终，变奏策略清晰可感，整体像一个品牌出品 |

## 打回诊断规则

> 问题在哪层就打回哪层，不做无效返工。

### 诊断方法

对每个 < 9 分的维度，按以下逻辑诊断：

1. **先看 planning JSON**：planning 中该维度相关的字段（content / cards / layout_hint / data_highlights）是否充实？
   - 如果 planning 就空洞/缺失 -> `rollback_to: "planning"`
   - 如果 planning 充实但 HTML 没体现 -> `rollback_to: "html"`

2. **再看 style.json**：配色/装饰/字体是否与 style.json 定义一致？
   - 如果 style.json 定义本身就有问题（配色不协调、灵魂宣言与实际不符）-> `rollback_to: "style"`
   - 如果 style.json 没问题但 HTML 没遵守 -> `rollback_to: "html"`

3. **跨页问题**：叙事断裂/风格走形等全局问题
   - 叙事断裂且大纲就没设计好 -> 标注但不打回（大纲已确认不宜再改）
   - 风格整体偏离 style.json -> `rollback_to: "style"`

### 打回层级对照表

| `rollback_to` | 修复范围 | 修复后需要 |
|---------------|---------|-----------|
| `planning` | 修改 planning JSON -> 重跑 `scripts/prompt_assembler.py` -> 重新生成该页 HTML | 仅审查被修改的页面 |
| `html` | 只修改 HTML，不动 planning | 仅审查被修改的页面 |
| `style` | 修改 style.json -> 全部 HTML 重新生成 | 全量重新审查 |

### 打回阈值

- 单页加权总分 < 9 分：该页必须修正
- 全局任一维度 < 9 分：全局问题必须修正
- 所有页 >= 9 分且全局 >= 9 分：通过

### 约束

- **单页最多被修改 3 次**（跨轮累计）。第 3 轮仍不达标，标注问题和当前分数后交给用户决定
- **每轮评分独立记录**，不覆盖：`final-review-round-{n}.json`
- 修改后**不自检** -- 主 agent 会另起新 reviewer 从零审查

## 通信与生命周期

### 主 agent 与 reviewer sub-agent 的通信

- 通过 `OUTPUT_DIR/reviews/reviewer-prompt.txt`（harness assemble 产物）传入完整上下文
- reviewer 输出写入 `OUTPUT_DIR/reviews/final-review-round-{n}.json`
- 不通过对话补口头上下文
- 如果资料包不完整，reviewer 必须在输出 JSON 中标注缺失项，而不是猜测

### 生命周期（多轮换人模式）

> 以下流程只描述 **harness 终审回路** 本身；是否在最终交付前向用户展示，由主 agent 按主流程决定。**但只要进入该回路，就必须完整执行，不允许半途改回主 agent 自审。**
>
> **硬规则**：每一轮 reviewer sub-agent 只负责一轮终审。结果被主 agent 回收后，必须立即关闭。不存在“同一轮补充资料后继续复用旧 reviewer”的选项。

```
主 agent:
  1. python3 scripts/final_review_harness.py assemble OUTPUT_DIR
  2. 另起 reviewer-1 sub-agent，传入 OUTPUT_DIR/reviews/reviewer-prompt.txt
  3. reviewer-1 评分 + 直接修改不达标页面，输出 OUTPUT_DIR/reviews/final-review-round-1.json
  4. python3 scripts/final_review_harness.py validate OUTPUT_DIR/reviews/final-review-round-1.json
  5. 回收结果后，立即关闭 reviewer-1
  6. exit code 0？→ 该终审回路通过，回到主 agent 决定后续展示/流转
     exit code 2？→ 重新 assemble（收集被修改后的文件）
  7. 另起 reviewer-2 sub-agent（与 reviewer-1 完全隔离）
  8. reviewer-2 从零读取更新后的资料包，重新评分 + 修改
  9. 单页最多 3 轮，分数达标即停
```

## Reviewer Sub-agent 执行边界

### 你必须输出

- 每页 6 维度评分（1-10 整数）
- 每页加权总分（1 位小数）
- 每页 verdict（pass / fail）
- 每个 fail 页面的 issues（dimension / detail / rollback_to）
- 每个 fail 页面的 **modifications**（实际修改日志：layer / file / action / then）
- 全局 3 维度评分
- overall_verdict（pass / needs_fix）
- total_modifications（本轮修改总数）

> **防偷懒硬规则：** 如果一个页面 verdict = fail，那么该页的 `modifications` 数组**不能为空**。评分低但不改 = 失职。harness validate 会机器检测这一点，检测到会报错退回。

### 你能做的事

- **评分**：逐页 + 全局
- **直接修改文件**：planning JSON / slide HTML / style.json
- **重跑脚本**：修改 planning 后重跑 `scripts/prompt_assembler.py` + 重新生成 HTML

### 你不能做的事

- 不跳过任何页面
- 不给人情分（"差不多 9 分就算了"= 绝对禁止）
- 不修改大纲（outline.json 已确认，不宜再改）
- **不允许“只评不改”**：如果你给了 fail，你就必须改。不能说“建议修改 XXX”然后什么都不做。你有完整的文件访问权限，没有借口不改。

### 评分时必须的内心独白

每页打分前，问自己：

1. 如果这是一家万元/页的 PPT 公司交付给客户的，客户会满意吗？
2. 如果我是演讲者，站在台上翻到这一页，我有信心吗？
3. 对照 planning JSON，这页是忠实执行了还是偷工减料了？

## Reviewer Sub-agent Prompt 模板

```text
你是独立 PPT 质量审查员。你与生成者完全隔离，从零读取所有资料后独立打分。

## 审查规则
1. 先读评分标准和修改规则
2. 再读需求 JSON（默认 `requirements.json`，兼容 `requirement.json`）+ 大纲 JSON（理解用户要什么）
3. 再读 style.json（理解风格基因）
4. 逐页：先读 planning{n}.json，再读 slide-{NN}.html，对照评分
5. 每个 < 9 分的维度必须诊断 rollback_to（planning / html / style）
6. **直接修改对应文件**，并在 modifications 中记录修改行为
7. 如修改了 planning，重跑 `scripts/prompt_assembler.py` + 重新生成该页 HTML

## 评分标准
{评分标准部分由 harness assemble 自动注入}

## 输出格式
输出严格 JSON，包含评分 + 修改日志（见 harness 组装的输出格式定义）。
不要输出 JSON 之外的任何内容。

## 资料包
{以下部分由 harness assemble 自动注入}
```

## 主 agent 的回收职责

- 运行 `scripts/final_review_harness.py validate` 验证 reviewer 输出格式
- 如果 validate 报 ERROR，要求 reviewer 重新输出（格式问题）
- 如果 exit code = 0（全部通过），标记该 harness 终审回路通过，并按主流程决定后续展示/交付
- 如果 exit code = 2（有修改，需换人审查）：
  1. 重新 `assemble`（收集被 reviewer 修改后的文件，组装新资料包）
  2. 另起新 reviewer sub-agent（与前一个完全隔离）
  3. 新 reviewer 从零读取更新后的资料包，重新评分 + 修改
- 分数达标即停，单页最多 3 轮。第 3 轮仍不达标，标注问题并交由主 agent 按主流程决定是否展示给用户
