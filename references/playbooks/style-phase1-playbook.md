# Style Phase 1 Playbook -- 风格合同的定义与输出

## 目标

基于用户需求、大纲结构和 runtime 风格规则，输出一份可被 planning/html 稳定消费的 `style.json` 全局风格合同，而不是任何单页的 HTML 代码。

---

## 阶段执行流程

### Phase 1: 提炼风格约束

1. 读取 `requirements-interview.txt`
2. 抽取高优先级信号：品牌色、品牌禁区、受众、正式度、语言、配图策略。绝不允许在不知情的情况下选错受众（如给技术向听众做可爱风）。
3. 读取大纲 `outline.txt`
4. 判断整套 deck 的节奏类型：稳态推进 / 波浪起伏 / 发布会式冲刺 / 培训式均匀展开，以决定你的变化策略基调。

### Phase 2: 选择风格基底

按以下优先级决策你的核心风格取向：

1. **绝对优先**：用户指定的风格或品牌约束
2. 次优先：主题和受众最强的情绪倾向
3. 再次：预置风格中最接近的一种
4. 若都不贴合，则从最接近的预置风格出发深度自定义

**预置风格使用约束**：
- 先用 `Runtime Style Palette Index` 锁定候选。
- 若需复用或借鉴某个预置风格，去读取对应的具体的单一预置文件。
- **最多参考 1-2 个预置文件**，绝对禁止把整个风格目录全量读入引起上下文污染。

### Phase 3: 生成 style.json 合同

你必须输出一份严格遵守下列字段要求的 JSON 合同文件：

*   `style_id` / `style_name`
*   `mood_keywords`
*   `design_soul`：描述整套 deck 的设计目标，**绝对不可以**写成某一页的成品描述或构图指导。
*   `variation_strategy`：必须同时说明“哪些元素允许变”和“哪些元素锁死不动”。不能写成逐页执行指令。
*   `decoration_dna.signature_move` / `.forbidden` / `.recommended_combos`
*   `font_family`

#### css_variables 键命名与数量规范（强制红线）

这 13 个变量是基石，必须定义并且键名**不能更改一个字母**：

```json
{
  "--bg-primary": "#...",
  "--bg-secondary": "#...",
  "--card-bg-from": "#...",
  "--card-bg-to": "#...",
  "--card-border": "#...",
  "--card-radius": "...px",
  "--text-primary": "#...",
  "--text-secondary": "#...",
  "--accent-1": "#...",
  "--accent-2": "#...",
  "--accent-3": "#...",
  "--accent-4": "#...",
  "--font-primary": "..."
}
```

- key 必须带 `--` 前缀，禁止自创这 13 个核心命门。
- 如果需要增加（如 `--accent-succ` 或 `--chart-line-1`）可以随意增加，但这 13 个必填项不可少、不可改名。
- `--font-primary` 必须与顶层 `font_family` 保持一致。
- 确有必要时，可附加 `css_snippets` 固化跨页重复的局部样式锚点（例如定义某类卡片的阴影），但绝对不能包含能驱动整页骨架排版的 CSS。
