# 大纲审查 Sub-agent Playbook

## 何时读取

- 当大纲编写 sub-agent 完成后，主 agent 调度你审查时必读
- 你与大纲编写者完全隔离，没有生成阶段的记忆

## 目标

以独立第三方视角审查大纲质量，确保叙事结构、逻辑链和素材消费达到"万元/页级"PPT 的标准。

你是质量门卫，不是优化师。你只做两件事：
1. **评分** -- 按 5 个维度逐一打分
2. **给出修改指令** -- 如果不通过，指出具体问题和修改要求（你不修改 outline.json，修改由大纲编写 sub-agent 执行）

> 与 **Step 5d 强制终审** 的 reviewer sub-agent（`playbooks/review-subagent-playbook.md`）不同：大纲审查员**不直接修改文件**，而是输出修改指令交回给编写者。因为大纲是叙事骨架，修改需要架构师的全局视角重新推导，审查员只负责诊断。

## 输入包

| 文件 | 用途 |
|------|------|
| `OUTPUT_DIR/requirements.json` | 用户需求（场景、受众、目的、页数等） |
| `OUTPUT_DIR/research-package.json` | 素材包（验证数据支撑） |
| `OUTPUT_DIR/outline.json` | 待审查的大纲 |

## 评分维度（5 维度，每维 1-10 分）

| 维度 | key | 9 分标准（通过线） | 10 分（无懈可击） |
|------|-----|---------|----------|
| **叙事结构** | `narrative_structure` | Part 之间有明确逻辑递进，不是主题并列；叙事弧线有起伏 | 金字塔原理贯穿，情感弧线完整自然，每个 Part 的存在都不可替代 |
| **论证策略** | `argument_strategy` | 每 Part 有明确的论证方式，且论证方式不全相同 | 论证方式与内容完美匹配，多种策略形成互补合力 |
| **素材消费** | `material_consumption` | 核心论据有 research-package 中 high/medium 素材支撑；缺口已诚实标注 | 素材分配精准，每条 high 素材都被安排在最能发挥价值的位置 |
| **页面设计** | `page_design` | 每页 goal 明确（一句话无"和"字）；每 Part >= 2 页；总页数符合需求 | 页间有节奏变化，每页角色不可替代，任意删一页都会破坏叙事 |
| **需求忠实** | `requirement_fidelity` | 场景/受众/目的/必含内容/必避内容都被响应 | 每个需求字段都能在大纲中找到精确消费点 |

### 通过标准

- **单维度通过**：每个维度 >= 9 分
- **整体通过**：所有 5 个维度都 >= 9 分
- **任一维度 < 9**：打回，给出修改指令

## 审查流程

### 1. 需求对照

先读 `OUTPUT_DIR/requirements.json`，建立"用户要什么"的认知：
- 场景 + 受众 → 信息密度和专业深度应该在什么水平
- 目的 → 叙事终点应该导向什么行动
- 叙事结构 → Part 编排应该遵循什么逻辑
- 页数 → 总量是否符合
- 必含/必避 → 是否被响应

### 2. 素材对照

读 research-package.json，建立"家底多厚"的认知：
- `by_reliability` → high/medium 有多少，能支撑多少数据密集页
- `gaps` → 哪些维度有缺口，大纲是否回避了缺口或降级处理
- `materials[].categories` → 各类别素材分布是否与大纲 Part 分配匹配

### 3. 大纲逐维度评分

读 outline.json，按 5 个维度逐一评分。

每个维度打分时的内心独白：
- **叙事结构**：如果我是观众，翻完 Part 1 会不会自然想看 Part 2？每个 Part 之间的 transition 是否有逻辑动力？
- **论证策略**：这个 Part 的内容用 data_driven 最合适还是 case_study？当前选择是最优的吗？
- **素材消费**：这页的核心论据在 research-package 里有对应素材吗？缺口有没有被诚实标注？
- **页面设计**：每页 goal 是否清晰独立？有没有一页想说太多东西？
- **需求忠实**：content_must_include 的每一项是否都在大纲中有明确落点？

## 产物格式

### 通过时

```json
{
  "verdict": "pass",
  "scores": {
    "narrative_structure": 9,
    "argument_strategy": 10,
    "material_consumption": 9,
    "page_design": 9,
    "requirement_fidelity": 9
  },
  "comments": "整体评价（简要）"
}
```

### 打回时

```json
{
  "verdict": "needs_fix",
  "round": 1,
  "scores": {
    "narrative_structure": 8,
    "argument_strategy": 9,
    "material_consumption": 7,
    "page_design": 9,
    "requirement_fidelity": 9
  },
  "issues": [
    {
      "dimension": "narrative_structure",
      "score": 8,
      "problem": "Part 2 和 Part 3 之间缺乏逻辑递进，更像主题并列",
      "diagnosis": "Part 2 讲技术架构，Part 3 讲应用场景，但没有从'因为技术好所以应用广'的因果链连接",
      "fix_instruction": "在 Part 2 结尾添加一页'技术能力总结'作为桥接，或在 Part 3 开头的 transition_from_previous 中建立因果关系"
    },
    {
      "dimension": "material_consumption",
      "score": 7,
      "problem": "第 6 页声称'市场规模超 500 亿'，但 research-package 中没有对应的 high 可信度素材",
      "diagnosis": "该数据来源不明或未被收集到",
      "fix_instruction": "要么找到 research-package 中的对应素材 ID 并引用，要么标注 found_in_search: false，要么降低数据密度改为定性描述"
    }
  ]
}
```

### 修改指令的质量要求

每条 `fix_instruction` 必须：
- **具体** -- 指出哪个 Part、哪一页、哪个字段需要改
- **可执行** -- 给出具体的修改方向，不是"请改进"
- **不越界** -- 不重新设计大纲（那是架构师的事），只指出问题和期望结果
- **有依据** -- 引用 `requirements.json` 或 research-package 中的具体字段/素材 ID

## 多轮机制

- **第 1 轮**：完整 5 维度评分 + 所有问题的修改指令
- **第 2 轮**（如果第 1 轮打回后重修）：
  - 只重新评分被打回的维度 + 受修改影响的维度
  - 已通过且未受影响的维度保持原分
  - 如果仍有 < 9 的维度，标注问题但交给用户决定（不再打回）
- **最多 2 轮审查**

## Sub-agent Prompt 模板

```text
你是独立大纲审查员，与大纲编写者完全隔离，从零读取所有资料后独立评分。

先读取 SKILL_DIR/references/playbooks/outline-review-subagent-playbook.md。

读取顺序：
1. `OUTPUT_DIR/requirements.json`（理解用户要什么）
2. OUTPUT_DIR/research-package.json（理解素材家底）
3. OUTPUT_DIR/outline.json（审查对象）

按 5 个维度评分（每维 1-10，9 分通过线）：
- 叙事结构 / 论证策略 / 素材消费 / 页面设计 / 需求忠实

全部 >= 9 → verdict: pass
任一 < 9 → verdict: needs_fix，给出具体、可执行的 fix_instruction

输出严格 JSON 格式。
```

## 主 agent 的回收职责

- 收到审查结果 JSON
- `verdict: pass` → 进入 Step 4（策划稿）
- `verdict: needs_fix` → 将 `issues` 数组作为修改指令传给大纲编写 sub-agent
- 第 2 轮仍 needs_fix → 展示问题给用户，让用户决定是否接受当前大纲
- 每轮审查结果保存为 `OUTPUT_DIR/outline-review-round-{n}.json`
