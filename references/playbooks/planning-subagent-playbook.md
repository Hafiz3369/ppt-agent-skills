# Step 4 Planning Sub-agent Playbook

## 目录

- 何时读取
- 目标
- 前置准备
- 三层合同
- 一致性与灵动的分工
- 输入包设计
- Continuity State
- 通信与生命周期
- Planning Sub-agent 的执行边界
- 验证合同
- 串行与并行
- Planning Sub-agent Prompt 模板
- 主 agent 的回收职责

## 何时读取

- 当 Step 4 进入逐页 planning 阶段时读取
- 当准备把 planning 交给一个或多个 planning sub-agent 时必读
- 当你发现 planning 容易失去整体感，或页面开始趋同、失真、越权时回读

## 目标

把 Step 3 的语义合同稳定翻译为 Step 4 的空间合同，同时做到两件事：

1. 让 sub-agent 始终知道整套 deck 的总体方向，不在单页里迷路
2. 不把“整体一致性”误写成“每页都长一个样”

## 前置准备

在写第 1 页 planning 之前，主 agent 必须先准备最小运行资料：

- `references/principles/design-principles-cheatsheet.md`
- `references/runtime/resource-menu.md`
- 如当前 deck 需要配图，再追加 `references/runtime/image-generation.md`

这三者的职责不同：

- `design-principles-cheatsheet.md` 负责字段级决策与逐页体检
- `runtime/resource-menu.md` 负责避免后半程退化成只会用少数卡型
- `runtime/image-generation.md` 负责把页面语义合同翻译成图片合同

如果这些资料未准备好，不应开始 Step 4。

## 三层合同

### 1. 全局合同

由主 agent 准备，只描述整套 deck 不能偏离的东西：

- `OUTPUT_DIR/requirements.json`
- `outline.json` 的 `core_thesis` / `design_rationale` / 全局节奏
- 已确认的风格方向与用户禁忌
- 整套 deck 的统一基因

全局合同只锁这些内容：

- 受众与目的
- 叙事弧线
- 统一视觉语法
- 绝对不能碰的内容边界

全局合同不锁：

- 每页都用同一种布局
- 每页都用同一种重心
- 每页都用同一种装饰手法

### 2. 分章合同

由主 agent 按 Part 拆好，交给每个 planning sub-agent：

- 当前 Part 的主题与任务
- 当前 Part 与上一 Part / 下一 Part 的逻辑关系
- 当前 Part 的节奏角色
- 本章建议强化的论证方式

分章合同的作用是保证章节内连贯，而不是让整章页面模板化。

分章合同应该说明：

- 本章偏“建立认知 / 证明 / 对比 / 收束”中的哪一种
- 本章是高压、平衡还是呼吸段
- 本章允许的视觉跨度有多大
- 本章与前后章节怎样交接

### 3. 单页合同

这是 planning sub-agent 真正逐页生产的对象。

单页合同必须明确：

- 这页为什么存在
- 这页要证明什么
- 第一视觉锚点在哪里
- 文字容量上限在哪里
- 资源为什么选这些，不选别的
- 这一页优先吃哪一类来源，哪些来源不能被伪装成硬证据
- 哪条 claim 该绑定哪个 `source_id`
- 哪条 claim 在 HTML 里应该落在哪张卡、用什么语气写、避开什么过硬措辞
- 哪些决策设计层不能推翻
- 哪些地方要主动与上一页做出变化

## 一致性与灵动的分工

### 必须统一的是“语法”

- 色彩家族
- 字体气质
- 装饰 DNA
- 图像语气
- 叙事节奏

### 必须变化的是“措辞”

- 布局重心
- 焦点位置
- 留白比例
- card 组合
- 主次落差
- 技法组合

一句话：同宗，不同脸。

## 输入包设计

不要把全部原始资料直接塞给 planning sub-agent。主 agent 需要先打包成高信噪比输入。
如果当前环境没有专门的 packet/harness，就用 `outline.json`、`requirements.json`、研究摘要和上一页 planning 结果构成最小输入包；不要把 `raw-sources/` 原文直接塞进主干上下文。

### 包 1：Global Brief

最小必需字段：

- `topic`
- `audience`
- `purpose`
- `narrative_structure`
- `content_must_include`
- `content_must_avoid`
- `style_choice`
- `page_count`
- `core_thesis`
- `deck_rhythm_summary`
- `design_soul`
- `variation_strategy`
- 研究摘要或来源地图（至少说明哪些 source_id 适合 framing，哪些只适合页级证据）

### 包 2：Part Brief

最小必需字段：

- `part_number`
- `part_title`
- `part_goal`
- `argument_mode`
- `transition_from_previous`
- `density_contract`
- `expected_emotion`
- `pages_in_part`
- `evidence_packet`

### 包 3：Page Seed

由 outline 中对应页面提供：

- `slide_number`
- `outline_page_title`
- `page_goal`
- `narrative_role`
- `proof_type`
- `audience_hook`
- `decision_basis`
- `evidence_packet.source_trace`
- `planning_focus`
- `suggested_cards`
- `density_label`
- `page_emotion`
- `payload_expectation.scene_board_type`
- `payload_expectation.required_scene_payload_groups`
- `payload_expectation.content_focus_tag_rule`

### 包 4：Continuity State

优先使用当前已落地的连续性来源：

- 上一页完整 planning JSON
- 主 agent 提供的上一 Part 最后一页摘要
- 当前 Part 已完成页面的布局 / 焦点 / 技法简表

它不是主合同，但它能告诉 sub-agent：

- 本章已经实际用了哪些 `layout_hint`
- 最近 1-2 页的 `focus_zone` / `card_style` / `techniques`
- 下一页最该主动避开的重复答案
- 本章与前后组的交接提醒

## 通信与生命周期

### 主 agent 与 planning sub-agent 如何通信

- 默认通过 `requirements.json`、`outline.json`、研究摘要、上一页 planning / Part 交界摘要通信
- 不默认通过长对话反复补口头上下文
- 如果输入包不够，sub-agent 应回报具体缺口：
  - 缺哪个文件
  - 缺哪个字段
  - 哪条合同互相冲突
- dense scene 的 `support` 卡不能是态度卡或 slogan 卡；如果大纲已经给了 scene payload group，必须把它落到 card 级
- 对 `academic / technical / training / report` 的 content 页，完成标准不是“已经写出 planning JSON”，而是 scene payload group 已经全部被真实 card 承担

### dense scene 完成定义

当大纲或输入摘要提供 `payload_expectation.required_scene_payload_groups` 时，你必须把它当成页面完成定义，而不是可选提示。

- 先确认本页要求哪些 group
- 再确认每个 group 由哪张 `card_id` 承担
- 再确认该 card 的 `content_focus`、`body`、`data_points`、`chart` 能看出该组的真实 payload

如果出现下面任一情况，视为未完成，应该先修 planning：
- `definition_or_question` 只在标题态度里隐约出现，没有进入 card 内容
- `constraint_or_dependency` 只存在于图形关系想象中，没有被文本或数据承接
- `checkpoint_payload` 没有独立承载，只剩“注意事项”类泛句
- 试图用 `director_command.prose`、`layout_hint`、`design_intent` 替代缺失的 payload group

### 生命周期规则：任务完成即立刻终止

- 一个 planning sub-agent 只负责一次明确分配的任务边界
- 该边界完成、产物已被主 agent 回收后，必须立即关闭该 sub-agent
- 不存在“先留着待命、稍后补页/补改”的选项；需要返工或补充时，必须新开一个干净 planning sub-agent
- 只要当前 planning sub-agent 还保留着，就不允许再额外拉起一个同职责、同任务边界的 planning sub-agent
- 如果 `outline.json`、研究摘要、Part 目标、或 continuity 策略发生更新，旧会话视为污染，必须丢弃并新开
- 如果 sub-agent 已经开始依赖聊天历史理解任务，而不是依赖明确输入文件，视为污染，必须丢弃并新开

一句话：**任务完成就关，返工重开。**

## Planning Sub-agent 的执行边界

### 你必须决定

- `layout_hint`
- `focus_zone`
- `negative_space_target`
- `page_text_strategy`
- `compression_priority`
- `content_budget`
- `cards[]`
- `resource_rationale`
- `source_guidance`
  这里不只要有 `claim/source_id/confidence`，还要为每条 claim 提供 `render_intent`
  `render_intent` 至少要写清楚 `target_card`、`render_rule`、`preferred_phrases`、`avoid_phrases`
- `variation_guardrails`
- `handoff_to_design`

### 你不能改写

- 页目标
- 章节角色
- 核心论证方向
- 用户明确禁止的内容

### 你必须主动制造的差异

相邻页至少改变 2 个维度：

- `layout_hint`
- `focus_zone`
- `negative_space_target`
- `page_text_strategy`
- `card_style` 组合
- `visual_weight`

如果当前页与上一页任务相似，也不能靠“换个文字”冒充变化。

## 验证合同

验证是写入流程的一部分，不是事后补救。

- 每页 `planning/planning{n}.json` 写入后，立即运行单页验证
- 单页验证未收口前，不进入下一页
- 全部页面完成后，必须再运行一次全量验证，检查跨页规则
- 全量验证未收口前，不进入 Step 5

当前 validator 入口：

- `scripts/planning_validator.py`

## 串行与并行

### 串行模式

适用于：

- `light` deck
- 主 agent 选择降低并发度时
- 只启动 1 个 planning sub-agent 串行负责整套 deck 或单个 Part

执行原则：

- 一次只策划 1 页
- 当前页读取上一页完整 planning 结果
- 生成后立即写入与验证
- 串行指的是 **sub-agent 内串行产页**，不是退回主 agent 代做

### 并行模式

适用于：

- 标准 / 大型 deck 默认启用
- 轻量 deck 在主 agent 判断有收益时也可启用
- Part 已经清晰成立

执行原则：

- 按 Part 分组
- 组内串行，组间并行
- 每个 sub-agent 只负责自己章节
- 主 agent 负责分发、回收、交界处抽检
- 每页写完后更新 continuity state；组内下一页生成前必须重读

**硬规则**：

- 无论 deck 大小，Step 4 都必须由 planning sub-agent 执行
- 主 agent 只能决定并发度，不能把 planning 收回自己做
- 每个 planning sub-agent 完成后立即关闭；返工必须新开

## Planning Sub-agent Prompt 模板

```text
你是 PPT 页面策划师，只负责第 {start_page} ~ {end_page} 页。

先读合同层级：
1. Global Brief：整套 deck 的统一基因、受众、叙事与禁区
2. Part Brief：你负责章节的任务、节奏、论证方式与交接关系
3. Page Seed：当前页的语义职责

你的目标不是复制模板，而是把语义合同翻译为空间合同。

必须统一的是：
- 整套 deck 的视觉语法
- 本章的节奏角色

必须变化的是：
- 相邻页布局重心
- 焦点位置
- 留白比例
- 卡片组合方式

执行规则：
1. 严格遵循 prompt-3-planning.md
2. 每页单独产出一个 planning JSON
3. 写入 `planning/planning{n}.json`
4. 写入后立即运行单页 validator；未收口前不得继续下一页
5. 回读 continuity state，确认没有把上一页的布局和重心直接复制过来
6. 组内串行，禁止一次吐出整章所有页面
7. 整个 Part 完成后，等待主 agent 做全量验证与用户确认
```

## 主 agent 的回收职责

- 检查每个 Part 是否都完成
- 对每页和全量运行 validator
- 重点抽检 Part 交界页
- 向用户展示策划稿概览并等待确认
- 如果交界处失真，优先修 Part 合同，再修单页，不要直接丢给 HTML 层补救
