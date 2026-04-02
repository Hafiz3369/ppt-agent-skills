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

这 12 个变量是基石，必须定义并且键名**不能更改一个字母**：

```json
{
  "bg_primary": "#...",
  "bg_secondary": "#...",
  "card_bg_from": "#...",
  "card_bg_to": "#...",
  "card_border": "#...",
  "card_radius": "...px",
  "text_primary": "#...",
  "text_secondary": "#...",
  "accent_1": "#...",
  "accent_2": "#...",
  "accent_3": "#...",
  "accent_4": "#...",
  "css_snippets": {
    "example_class": "font-weight: 700;"
  }
}
```

- key 必须使用下划线（无 `--` 前缀），对应校验合同要求。
- 必须严格保留这 12 个基础变量名，禁止改名。如需自定义增加可以增加，但这 12 个不可少。
- `css_snippets` 必须是对象 (Object)，格式为 `"键名": "值"`，**绝对不能是数组 (Array)！** 确有必要时可用它固化跨页重复的局部样式结构（如阴影），但绝对不能包含能驱动整页骨架布局的 CSS。
