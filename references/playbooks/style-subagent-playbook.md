# Style Subagent Playbook -- 全局风格合同

## 何时读取

- 当主 agent 在 Step 3.5 调度你生成 `style.json` 时必读
- 你负责定义整套 deck 的全局风格合同，不负责任何单页 HTML

## 目标

基于用户需求、大纲结构和 runtime 风格规则，输出一份可被 planning/html 稳定消费的 `style.json`。

## 输入

| 输入 | 用途 |
|------|------|
| `requirements-interview.txt` | 用户的风格偏好、品牌约束、语言语境 |
| `outline.txt` | 内容结构、节奏切换、叙事弧线 |
| `Runtime Style Rules` | `style.json` 字段合同与失败边界 |
| `Runtime Style Palette Index` | 预置风格选择入口与默认顺序 |

## 产物

| 文件 | 格式 |
|------|------|
| `style.json` | JSON，全局风格合同 |

## 执行流程

### Phase 1: 提炼风格约束

1. 读取 `requirements-interview.txt`
2. 抽取高优先级信号：品牌色、品牌禁区、受众、正式度、语言、配图策略
3. 读取 `outline.txt`
4. 判断整套 deck 的节奏类型：稳态推进 / 波浪起伏 / 发布会式冲刺 / 培训式均匀展开

### Phase 2: 选择风格基底

按以下优先级决策：

1. 用户明确指定的风格或品牌约束
2. 主题和受众最强的情绪倾向
3. 预置风格中最接近的一种
4. 若都不贴合，则从最接近的预置风格出发自定义

选择预置风格时：

- 先用 `Runtime Style Palette Index` 锁定候选
- 若需要复用某个预置风格的变量体系或轻微改造，可再读取 `Runtime Style Palette Index` 里列出的对应单个预置文件
- 最多参考 1-2 个预置文件，不要把整个风格目录全量读入

### Phase 3: 输出 style.json

输出必须遵守 runtime 字段合同，至少包括：

- `style_id`
- `style_name`
- `mood_keywords`
- `design_soul`
- `variation_strategy`
- `decoration_dna.signature_move`
- `decoration_dna.forbidden`
- `decoration_dna.recommended_combos`
- `css_variables`
- `font_family`

若确有必要，可附加 `css_snippets` 固化跨页重复的局部样式锚点。

### Phase 4: 自审

在发送 FINALIZE 前逐项自审：

1. `design_soul` 是否描述整套 deck 的设计目标，而不是某一页成品
2. `variation_strategy` 是否同时说明“可变什么”和“不可变什么”
3. `decoration_dna.forbidden` 是否真的能阻止风格漂移
4. `recommended_combos` 是否写的是组合语法，不是页面脚本
5. `css_variables` 是否足够完整，能直接驱动下游页面
6. `css_snippets` 若存在，是否只锚定局部样式，而不是整页骨架

自审通过后发送 FINALIZE。

## 硬规则

- 不输出“只有颜色、没有风格边界”的半成品
- 不把 `variation_strategy` 写成逐页执行脚本
- 不把 `design_soul` 写成封面图描述、镜头描写或单页构图提示
- 不做 planning、不做 HTML、不做 research
- 若复用预置风格，保持 `style_id` 稳定且与实际基底一致
