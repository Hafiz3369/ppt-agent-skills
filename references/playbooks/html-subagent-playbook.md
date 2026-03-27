# Step 5c HTML Sub-agent Playbook

## 目录

- 何时读取
- 目标
- 三层消费顺序
- 自包含 `prompt-ready` 与扩展 packet 的关系
- Step 5c GATE 合同
- 一致性与变奏的平衡规则
- 通信与生命周期
- HTML Sub-agent 执行边界
- 串行 / 自包含 / 并行
- HTML Sub-agent Prompt 模板
- 主 agent 的回收职责

## 何时读取

- 当 Step 5c 进入资料包模式或并行模式时读取
- 当 HTML 生成交给 sub-agent 时必读
- 当页面开始模板化，或相邻页越来越像时回读

## 目标

让 HTML sub-agent 只专注于一件事：在不改写 planning 合同的前提下，把页面做得精美、稳定、像真正的 PPT。

这份 playbook 的重点不是“怎样写 div”，而是：

1. 怎样只吃该吃的上下文
2. 怎样保持整套 deck 的统一语法
3. 怎样避免因为全局一致性而牺牲单页表现力

## 三层消费顺序

HTML sub-agent 读取资料时，必须按这个顺序理解：

### 1. 全局视觉合同

来源：

- `style.json`
- `prompt-ready-{n}.txt` 中的 `GLOBAL_DESIGN_GUIDE`
- Global Brief 中的统一视觉基因

作用：

- 锁定字体、色彩、装饰 DNA、情绪温度
- 告诉你这套 deck 属于哪一种“视觉语法”

### 2. 分章执行合同

来源：

- 主 agent 在 sub-agent 任务中显式附带的 Part / 页码范围
- 相邻页 continuity 摘要
- `prompt-ready-{n}.txt` 中的 `LOCAL_CONTINUITY`

作用：

- 锁定本章的节奏角色
- 保证章节内呼吸感与连续性
- 告诉你这几页是“同章兄弟”，不是“同页复制”

### 3. 单页执行合同

来源：

- `prompt-ready-{n}.txt`
- `planning/planning{n}.json`（需要核对原始合同或做精修时）

作用：

- 锁定本页主锚点、主次关系、容量、资源与不可推翻项
- 给出单页具体执行所需信息

## 自包含 `prompt-ready` 与扩展 packet 的关系

### `prompt-ready`

它在当前 workflow 中是**主执行资料**。

它应该解决：

- 这一页先看什么
- 这一页有哪些关键约束
- 这一页有哪些资源要消费
- 这一页有哪些来源语气、密度和 continuity 规则

当 `scripts/prompt_assembler.py` 以 `--self-contained` 运行时，`prompt-ready` 会直接内联：

- 全局设计 guide
- style 定义
- planning JSON
- density / source guidance / continuity
- 技法牌与 CSS weapons
- 页面级资源（layout / blocks / charts / principles）

### `html-packet`（可选扩展）

如果未来 harness 恢复 packet/orchestrator，`html-packet` 可以作为更轻量的执行资料包存在。

但在当前仓库里：

- **不要把 `html-packet` 视为默认前置**
- **不要等待历史 orchestrator 准备步骤才开始**
- 优先使用自包含 `prompt-ready-{n}.txt`

一句话：

- 当前主链里，`prompt-ready` 同时负责路由和落地
- `planning/planning{n}.json` 是兜底原合同
- `LOCAL_CONTINUITY` 负责提醒你邻页已经用了什么，避免局部克隆

## Step 5c GATE 合同

在任何 HTML sub-agent 开始工作之前，主 agent 必须先满足以下条件：

1. 已运行 `scripts/prompt_assembler.py`
2. `prompt-ready-{n}.txt` 已为目标页面落盘
3. Step 4 planning 已确认可消费

主执行口径：

- `prompt-ready-{n}.txt` 是 HTML 阶段的主执行资料
- 非人工调试时，不再手动拼接散落的 `references/` 资料文件
- 如果 `prompt-ready` 缺失、为空、或与 planning 明显冲突，应立即报错并交回主 agent，而不是自行脑补

## 通信与生命周期

### 主 agent 与 HTML sub-agent 如何通信

- 通过 `prompt-ready-{n}.txt`、`planning/planning{n}.json` 与页码范围说明通信
- 不默认通过主线程反复解释“这一页想要什么感觉”
- 如果 HTML sub-agent 发现 `prompt-ready` 与 planning 冲突，应该报出具体页码、字段和冲突点，而不是自行脑补

### 生命周期规则：一页完成即立刻终止

- 一个 HTML sub-agent 只负责一个明确产物：**单页 `slide-{NN}.html`**
- 该页完成、HTML 已被主 agent 回收后，必须**立即关闭**该 sub-agent
- 不存在“同任务边界内继续补页/重做后再说”的口径；返工也必须新开一个干净 sub-agent
- 只要当前 HTML sub-agent 还活着，就不允许再额外拉起一个同职责、同页码边界的 HTML sub-agent
- 如果 Step 4 planning 重写过、style 合同更新过、或 `prompt-ready` 重新生成过，旧会话一律视为污染，必须丢弃并新开
- 如果 sub-agent 已经开始记住过期的设计决定、旧页面结构、旧来源语气，视为污染，必须丢弃并新开

一句话：**一页一 agent，回收即关闭，返工重开。**

## 一致性与变奏的平衡规则

### HTML 层必须继承的东西

- `style.json` 的 CSS 变量
- planning 定下的 `page_type`
- `layout_hint`
- `focus_zone`
- `visual_weight`
- `cards[]` 的主次关系
- `handoff_to_design.non_negotiables`
- `source_guidance` 的证据语气和来源提示要求

### HTML 层必须主动创造的东西

- 同布局下的不同构图落点
- 同风格下的不同材质表达
- 卡片内部的微差异
- 装饰元素的密度变化
- 同章内的呼应与转场

### 禁止把一致性做成这些样子

- 每页都用同一标题装饰
- 每页都用同一主视觉站位
- 每页都用同一背景做法
- 每页都把信息平均切成几张边框卡片

## HTML Sub-agent 执行边界

### 你不能改

- `page_goal`
- 页面类型
- 主要信息层级
- 关键卡片的角色
- 资源选择逻辑

### 你可以发挥

- 构图比例
- 大标题与辅助信息的张力
- 层次深度
- 材质、遮罩、裁切、装饰组织
- 同类卡片之间的微差异

## 串行 / 自包含 / 并行

### 串行模式

适用于：

- `light` deck
- 主 agent 选择按页顺序调度多个单页 HTML sub-agent，而不是分章并行

读取顺序：

1. `prompt-ready-{n}.txt`
2. 如需核对原始合同，再读 `planning/planning{n}.json`

> 串行指的是 **主 agent 逐页调度多个 HTML sub-agent**，不是主 agent 自己写 HTML。

### 自包含模式

当前仓库的主执行模式。

读取顺序：

1. `prompt-ready-{n}.txt`
2. 仅在需要检查原始字段时再读 `planning/planning{n}.json`
3. 仅在怀疑资源注入有误时再回读对应的 `references/` 资料文件

### 并行模式

适用于：

- 标准 / 大型 deck 默认启用
- 轻量 deck 在主 agent 判断有收益时也可启用
- `prompt-ready` 已由 `scripts/prompt_assembler.py design --all --self-contained` 生成完成

执行原则：

- 页面之间可以并行
- 每个 sub-agent 只读自己的 `prompt-ready-{n}.txt`
- 不存在“一个 sub-agent 负责一组页码”的模式

**硬规则**：

- 无论 deck 大小，Step 5c 都必须由 HTML sub-agent 执行
- 主 agent 只能决定调度批次与并发度，不能自己写页面
- 一个 HTML sub-agent 只负责一页，回收后立即关闭；返工必须新开

## HTML Sub-agent Prompt 模板

```text
你是 PPT HTML 设计师，只负责第 {page} 页。

先读合同层级：
1. 全局视觉合同：统一视觉语法
2. 分章执行合同：本页与邻页的节奏与交接关系
3. 单页执行合同：当前页 prompt-ready / planning

执行原则：
- 统一语法，不统一长相
- 忠实执行 planning，不重做 planning
- 本页要与邻页连贯，同时保持变奏
- 如果同布局再次出现，必须改变重心、层次或材质表达

执行流程：
1. 先读 `prompt-ready-{page}.txt`
2. 必要时再读 `planning/planning{page}.json`
3. 找出唯一 anchor
4. 先搭页面骨架，再填卡片，再做装饰
5. 写入 `slides/slide-{NN}.html`
6. 完成后立即交回主链，由主 agent 回收并关闭你

禁止：
- 不读 `prompt-ready` 就直接写 HTML
- 改写页面目标和主次关系
- 把 `qualified` / `derived` 的主张写成像已经全面证实的硬结论
- 把页面做成标准网页说明书
```

## 主 agent 的回收职责

- 检查所有 `slide-XX.html` 是否存在
- 抽检 Part 交界页是否仍同宗不同脸
- 触发强制 reviewer
- 只在 reviewer 通过后更新 `preview.html`

如果问题来自单页执行失误，修 HTML。
如果问题来自 planning 合同模糊，回退 Step 4。
