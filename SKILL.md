---
name: ppt-agent
description: 专业 PPT 演示文稿全流程 AI 生成助手。模拟顶级 PPT 设计公司的完整工作流（需求调研 -> 资料搜集 -> 大纲策划 -> 策划稿 -> 设计稿），输出高质量 HTML 格式演示文稿。当用户提到制作 PPT、做演示文稿、做 slides、做幻灯片、做汇报材料、做培训课件、做路演 deck、做产品介绍页面时触发此技能。即使用户只说"帮我做个关于 X 的介绍"或"我要给老板汇报 Y"，只要暗示需要结构化的多页演示内容，都应该触发。也适用于用户说"帮我把这篇文档做成 PPT"、"把这个主题做成演示"等需要将内容转化为演示格式的场景。
---

# PPT Agent -- 专业演示文稿全流程生成

## 核心理念

模仿专业 PPT 设计公司（报价万元/页级别）的完整工作流，而非"给个大纲套模板"：

1. **先调研后生成** -- 用真实数据填充内容，不凭空杜撰
2. **策划与设计分离** -- 先验证信息结构，再做视觉包装
3. **内容驱动版式** -- Bento Grid 卡片式布局，每页由内容决定版式
4. **全局风格一致** -- 先定风格再逐页生成，保证跨页统一
5. **智能配图** -- 利用图片生成能力为每页配插图（绝大多数环境都有此能力）

---

## 环境感知

开始工作前自省 agent 拥有的工具能力：

| 能力 | 降级策略 |
|------|---------|
| **信息获取**（搜索/URL/文档/知识库） | 全部缺失 -> 依赖用户提供材料 |
| **图片生成**（绝大多数环境都有） | 缺失 -> 纯 CSS 装饰替代 |
| **文件输出** | 必须有 |
| **脚本执行**（Python/Node.js） | 缺失 -> 跳过自动打包和 SVG 转换 |

**原则**：检查实际可调用的工具列表，有什么用什么。

---

## 路径约定

整个流程中反复用到以下路径，在 Step 1 完成后立即确定：

| 变量 | 含义 | 获取方式 |
|------|------|---------|
| `SKILL_DIR` | 本 SKILL.md 所在目录的绝对路径 | 即触发 Skill 时读取 SKILL.md 的目录 |
| `OUTPUT_DIR` | 产物输出根目录 | 用户当前工作目录下的 `ppt-output/`（首次使用时 `mkdir -p` 创建） |

后续所有路径均基于这两个变量，不再重复说明。

---

## 输入模式与复杂度判断

### 入口判断

| 入口 | 示例 | 从哪步开始 |
|------|------|-----------| 
| 纯主题 | "做一个 Dify 企业介绍 PPT" | Step 1 完整流程 |
| 主题 + 需求 | "15 页 AI 安全 PPT，暗黑风" | Step 1（跳部分已知问题）|
| 源材料 | "把这篇报告做成 PPT" | Step 1（材料为主）|
| 已有大纲 | "我有大纲了，生成设计稿" | Step 4 或 5 |

### 跳步规则

跳过前置步骤时，必须补全对应依赖产物：

| 起始步骤 | 缺失依赖 | 补全方式 |
|---------|---------|---------|
| Step 4 | 每页内容文本 | 先用 Prompt #3 为每页生成内容分配 |
| Step 5 | 策划稿 JSON | 用户提供或先执行 Step 4 |

### 复杂度自适应

根据目标页数自动调整流程粒度：

| 规模 | 页数 | 调研 | 搜索 | 策划 | 生成 |
|------|------|------|------|------|------|
| **轻量** | <= 8 页 | 3 题精简版（场景+受众+补充信息） | 3-5 个查询 | 整体生成（Step 3 可与 Step 4 合并） | 逐页生成 |
| **标准** | 9-18 页 | 完整 7 题 | 8-12 个查询 | 逐页生成 | 逐页生成 |
| **大型** | > 18 页 | 完整 7 题 | 10-15 个查询 | 逐页生成 | 逐页生成 |

**复杂度判断时机**：
1. **预判**（Step 1 开始前）：根据用户初始描述估算。若用户明确说了页数（如"做 5 页"）或暗示简短（如"简单介绍一下"），直接预判为轻量并精简提问
2. **确认**（Step 1 结束后）：根据 Q7 回答的页数正式确认 `complexity_level`（light / standard / large），写入 `progress.json`
3. **传递**：后续各步骤从 `progress.json` 读取 complexity_level，据此调整搜索查询数、策划深度等参数

---

## 6 步 Pipeline

### Step 1: 需求调研 [STOP -- 必须等用户回复]

> **禁止跳过。** 无论主题多简单，都必须提问并等用户回复后才能继续。不替用户做决定。

**执行**：使用 `references/prompts/prompt-1-research.md`
1. 搜索主题背景资料（3-5 条）
2. 根据复杂度选择完整 7 题或精简 3 题，一次性发给用户
3. **等待用户回复**（阻断点）
4. 整理为需求 JSON

**7 题三层递进结构**（轻量模式只问第 1、2、7 题）：

| 层级 | 问题 | 决定什么 |
|------|------|---------|
| 场景层 | 1. 演示场景（现场/自阅/培训） | 信息密度和视觉风格 |
| 场景层 | 2. 核心受众（动态生成画像） | 专业深度和说服策略 |
| 场景层 | 3. 期望行动（决策/理解/执行/改变认知） | 内容编排的最终导向 |
| 内容层 | 4. 叙事结构（问题->方案/科普/对比/时间线） | 大纲骨架逻辑 |
| 内容层 | 5. 内容侧重（搜索结果动态生成，可多选） | 各 Part 主题权重 |
| 内容层 | 6. 说服力要素（数据/案例/权威/方法，可多选） | 卡片内容类型偏好 |
| 执行层 | 7. 补充信息（演讲人/品牌色/必含/必避/页数/配图偏好） | 具体执行细节 |

**产物**：需求 JSON（topic + requirements）

---

### Step 2: 资料搜集

> 盘点所有信息获取能力，全部用上。搜索质量直接决定后续内容是"言之有物"还是"空洞废话"。

**执行**：

**2a. 查询规划**

根据主题和用户需求，规划多维度搜索查询（数量参考复杂度表）：

| 查询维度 | 示例 | 目的 |
|---------|------|------|
| 核心定义 | "{主题} 是什么 / 定义 / 核心概念" | 确保基础事实准确 |
| 市场数据 | "{主题} 市场规模 / 增长率 / 行业报告 2024-2026" | 数据卡片填充 |
| 竞品/对比 | "{主题} vs {竞品} / 对比分析 / 优劣势" | 对比论证素材 |
| 案例/应用 | "{主题} 客户案例 / 应用场景 / 成功案例" | 故事化说服 |
| 趋势/展望 | "{主题} 发展趋势 / 未来展望 / 技术路线图" | 结尾展望素材 |
| 权威观点 | "{主题} 专家评价 / 行业报告 / 白皮书" | 权威背书 |

> 不要所有查询都是同一个维度的换词。每个维度至少 1 个查询，核心维度可多个。

**2b. 并行搜索**

用所有可用的信息获取工具并行搜索，包括但不限于：搜索引擎、URL 读取、文档解析、知识库查询。

**2c. 结果整理**

每组搜索结果必须结构化整理为以下格式，不要只贴原文：

```json
{
  "query": "搜索查询",
  "findings": [
    {
      "fact": "一句话核心发现",
      "data": "具体数据/数字（如有）",
      "source": "来源（网站/报告名/作者）",
      "reliability": "high | medium | low",
      "relevance": "与大纲哪个 Part 最相关"
    }
  ]
}
```

**可信度判定**：
- **high**：权威机构报告（Gartner/IDC/政府统计）、学术论文、官方文档
- **medium**：行业媒体报道、企业博客、分析师个人观点
- **low**：论坛讨论、自媒体、无来源数据

> 只有 high/medium 的数据才能进入策划稿的 data_highlights。low 可信度数据仅作参考，不用于关键数据展示。

**产物**：搜索结果集合 JSON

---

### Step 3: 大纲策划

**执行**：使用 `references/prompts/prompt-2-outline.md`（大纲架构师 v3.0 -- Strategic Architect）

**方法论**：
- **金字塔原理** -- 结论先行、以上统下、归类分组、逻辑递进
- **叙事弧线** -- 根据 Step 1 第 4 题选择的叙事结构，确定 Part 排列的情感轨迹
- **论证策略** -- 每 Part 选择论证策略（data_driven/case_study/comparison/framework/step_by_step/authority）

**大纲架构师的 5 步思考过程**（prompt 内置，自动执行）：
1. 提炼全局核心论点（1 句话 core_thesis）
2. 确定 Part 数量和主题（含 Part 间逻辑关系标注）
3. 为每 Part 选择论证策略
4. 分配页面并确定每页论点
5. 标注每页数据需求和搜索覆盖情况

**自检**：
- 页数符合要求
- 每 Part >= 2 页（单页 Part 必须合并或扩充）
- Part 之间有明确的逻辑递进关系（不是主题并列）
- 要点有搜索数据支撑（缺失数据诚实标注 `found_in_search: false`）
- `design_rationale` 字段完整（核心论点 / 叙事结构 / 情感弧线 / 逻辑链 / 页数分配理由）

**产物**：`[PPT_OUTLINE]` JSON（含 `design_rationale` 和 Part 间 `transition_from_previous`）

---

### Step 4: 内容分配 + 策划稿 [建议等用户确认]

> 将内容分配和策划稿生成合为一步。在思考每页应该放什么内容的同时，决定布局和卡片类型，更自然高效。
> 策划稿必须是 AI 逐页思考的内容创作产物。

#### 4a. 资源菜单预读（首页策划前强制执行，仅一次）

> **先看菜单才能点菜。** 不知道有哪些组件/图表/布局/原则可选，策划时就只会用最基础的 text/data/list，浪费了丰富的设计能力。

策划第一页前，必须读取以下索引文件（每份只需读 README，不读具体文件）：

| # | 读取什么 | 获得什么 | 影响策划的什么决策 |
|---|---------|---------|----------------|
| 1 | `layouts/README.md` | 10 种布局骨架 + 决策矩阵 | 每页的 `layout_hint` 选择 |
| 2 | `blocks/README.md` | 8 种复合组件 + 选择指南 | 每页的 `card_type` 组合方式 |
| 3 | `blocks/card-styles.md` | 6 种卡片视觉变体 + 搭配规则 | 每张卡片的 `card_style` 选择 |
| 4 | `charts/README.md` | 13 种图表 + 数据类型映射 | data 卡片的 `chart_type` 选择 |
| 5 | `icons/README.md` | 4 类 SVG 图标 | 图标类卡片的 icon 选择 |
| 6 | `principles/README.md` | 6 大设计原则索引 | 策划时就考虑原则 |
| 7 | `styles/README.md` 的**装饰技法工具箱**章节 | 3 层装饰技法（背景层/卡片层/页面层各 5 种）+ 管线安全底线 | 每页 `decoration_hints` 的选择 |
| 8 | `image-generation.md`（**需要配图时**） | prompt 6 维度构造公式 + 场景叙事翻译表 + 风格关键词表 + 构图自适应表 | 每页 `image.prompt` 的构造 + `image.usage` 的选择 |

> 第 8 项仅在 Q7 配图偏好 != A（不需要）时读取。策划师要写 `image.prompt`，就必须先掌握 prompt 构造方法、场景翻译技巧和各风格的关键词——没有这些上下文就是"没见过食材长什么样就要写菜谱"。
>
> 第 7 项的 `styles/README.md` 只读"装饰技法工具箱"章节（L100-141），**不读**风格决策流程和调色板信息（那些留给 Step 5a）。策划师需要知道"有哪些装饰手法可选"，但不需要此刻决定具体配色。

> 预读后，策划师就知道自己的"工具箱"里有什么。后续逐页策划时，根据内容特征从工具箱中选择最合适的组件，而非只用最熟悉的几种。

#### 4b. 逐页策划

**执行**：使用 `references/prompts/prompt-3-planning.md`（内容分配与策划稿）

**要点**：
- 将搜索素材精准映射到每页
- 为每页设计多层次内容结构（主内容 40-100 字 + 数据亮点 + 辅助要点）
- 每页选择布局（`layout_hint`，从预读的 10 种布局中选择）
- 每个区域自由组合 14 种 card_type（从预读的 6 种基础 + 8 种复合中选择）
- 复合类型卡片（timeline/diagram/quote/comparison/people/icon_group/image_hero/matrix_chart）可跨列跨行，与基础卡片自由混搭
- data 卡片需指定 `chart_type`（从预读的 13 种图表中选择）
- 叙事节奏参考 `references/narrative-rhythm.md` 的视觉重量规则
- 每页 planning JSON 带 `visual_weight` 分数
- **每页必须填写 `required_resources`**：将 layout_hint / card_type / chart_type / page_type 翻译为具体文件路径（映射关系已在 4a 预读阶段掌握），供 Step 5c 按清单加载
- **每页必须填写 `image`**：选择配图用法（`usage`）、构造图片生成 prompt、指定放置位置。策划阶段上下文最丰富，配图决策必须在此完成。整个 PPT 中 `split-content` 和 `card-inset` 各至少使用 1 次（总页数 >= 8 时）

#### 逐页生成策划稿（一页一文件）

> **核心原则：一个 planning JSON 对应一个 HTML。** 每页策划稿写入 `planning/planning{n}.json`（n = 页码），轻量独立，便于用户逐页编辑和 Step 5c 按需读取。

**生成节奏**：

```
── 第 1 页 ──────────────────────────────
生成：用 Prompt #3 为第 1 页生成策划 JSON
写入：write_to_file -> OUTPUT_DIR/planning/planning1.json
验证：python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning/planning1.json --refs SKILL_DIR/references

── 第 2 页 ──────────────────────────────
生成：用 Prompt #3 为第 2 页生成策划 JSON
      注入上下文：上一页 JSON（保证衔接）
写入：write_to_file -> OUTPUT_DIR/planning/planning2.json
验证：python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning/planning2.json --refs SKILL_DIR/references

── 第 3, 4, 5... 页 重复 ──────────────
每页都是：生成 -> write_to_file -> 验证 -> 下一页
```

> **验证是写入流程的一部分，不是事后审查。** 每页 JSON 写入后立即运行 `planning_validator.py` 单页验证。validator 检查：字段完整性、枚举值合法性、资源文件路径存在性、card_style 多样性。有 ERROR 时必须修正后再继续下一页。

**操作边界**：
1. 每次只在 Prompt #3 中请求**一页**的策划（封面/目录/章节封面等极简页可 2-3 页一起，但仍然每页独立文件）
2. 每页生成后**必须**立即写入 `planning/planning{n}.json`
3. 写入后立即运行 `planning_validator.py` 验证（ERROR = 必须修正，WARNING = 建议修正）
4. 验证通过后才开始下一页
5. 不要用 Python 脚本操作 JSON 文件
6. 不要尝试一次输出全部页面

**上下文传递**：每页生成时注入上一页的完整 JSON，保证内容衔接和节奏递进。

所有策划稿完成后：
1. 运行全量验证（含跨页规则：布局多样性 + visual_weight 节奏 + image usage 多样性）：
   ```bash
   python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning/ --refs SKILL_DIR/references
   ```
2. 修正全量验证发现的跨页问题（如有）
3. 向用户展示策划稿概览
4. **[STOP -- 等待用户确认]**：告知用户可以直接编辑对应的 `planning/planning{n}.json` 修改任意页面的内容/布局/卡片结构。修改完成后回复确认，再进入 Step 5。

**产物**：每页独立的策划 JSON -> `OUTPUT_DIR/planning/planning{n}.json`（n = 1, 2, 3...）

---

### Step 5: 风格决策 + 设计稿生成

分三个子步骤，**顺序不可颠倒**：

#### 5a. 风格决策

**执行**：阅读 `references/styles/README.md`，按其决策流程选择或自创配色方案，然后只读对应参考调色板文件（如 `references/styles/blue-white.md`）。

> 风格的装饰工具箱已在 `styles/README.md` 中定义，首页生成前读取一次即可。**风格产物（style.json）只保存纯 CSS 变量**，不包含装饰描述，避免每页 Prompt 中重复注入相同的装饰指令导致千篇一律。

8 种参考调色板及其文件路径见 `resource-registry.md` 第 1 节。

**产物**：`OUTPUT_DIR/style.json`（纯 CSS 变量）

#### 5b. 配图生成（可选）

> **prompt 已由 Step 4 策划阶段生成**，写入 `planning{n}.json` 的 `image.prompt` 字段。Step 5b 只需读取并调用 `generate_image`。

**执行流程**：

1. 读取 `planning{n}.json` 的 `image` 对象
2. 如果 `image.usage` = `none`，跳过该页
3. 调用 `generate_image`：Prompt = `image.prompt`，ImageName = 基于页码和 `image.alt` 生成描述性命名
4. 保存到 `OUTPUT_DIR/images/`

**关键要点**：
- 配图时机：在生成每页 HTML **之前**先生成该页配图
- `image-generation.md` 的融入技法和 HTML 模板已在 4a 预读阶段读取（供 Step 5c 使用）
- 所有融入技法均为管线安全（禁止 CSS mask-image）

**产物**：`OUTPUT_DIR/images/` 下的配图文件

#### 5c. 逐页 HTML 设计稿生成（一个 planning 对应一个 HTML）

> 每页 HTML 都从对应的 `planning{n}.json` 生成。读取 `OUTPUT_DIR/planning/planning{n}.json` -> 生成 `OUTPUT_DIR/slides/slide-{NN}.html`，一对一消费，无上下文负担。

##### 资源按需加载决策树

> **核心理念：用户采访后获得的信息已经足以确定后续需要读取哪些资源。** 不要一口气读完所有参考文件，按以下三层决策树精确加载。

**第一层：采访后全局决策（Step 1 完成后立即执行，全流程只做一次）**

根据 Step 1 的 7 题答案，确定整个 PPT 生命周期内的资源加载策略：

| 采访答案 | 触发的加载决策 |
|---------|--------------| 
| Q7 配图偏好 = A（不需要） | 整个流程**跳过** `image-generation.md`，Step 5b 全部跳过 |
| Q7 配图偏好 = B/C/D | 标记**需要配图**，4a 预读阶段读取 `image-generation.md`（prompt 构造公式 + 风格关键词表 + 构图自适应表），Step 4 每页策划时填写 `image` 字段，Step 5b 执行 |
| Q7 风格偏好 = 明确指定 | Step 5a 直接读取对应 style_id 的文件（style_id -> 文件路径映射见 `resource-registry.md` 第 1 节），跳过其他风格 |
| Q7 风格偏好 = 未指定 | 先读 `styles/README.md` 的决策规则，确定风格后只读命中风格的独立文件 |
| Q7 语言偏好 = B/C/D（非纯中文） | 标记**多语言模式**，Step 5a 额外读取 `styles/README.md` 的"多语言排版优化"章节 |
| Q6 说服力要素 = 数据为主 | 标记**数据密集型**，Step 4 每页 data 卡片比例提高 |
| Q4 叙事结构 = 时间线 | 标记**时间线叙事**，Step 4 中更倾向使用 timeline chart_type |

**第二层：大纲后节奏决策（Step 3 完成后执行，全流程只做一次）**

| 大纲信息 | 触发的加载决策 |
|---------|------|
| 总页数 <= 12 | 读取 `narrative-rhythm.md` 的 **10 页标准模板** |
| 总页数 13-17 | 读取 `narrative-rhythm.md` 的 **15 页标准模板** |
| 总页数 >= 18 | 读取 `narrative-rhythm.md` 的 **20 页标准模板** |
| Part 数量确定后 | 读取 `narrative-rhythm.md` 的**章节色彩递进规则** |

**第三层：脚本自动组装资源（每页 HTML 生成前必须执行）**

> **禁止手动逐个 view_file 资源文件，禁止跳过此步。** 资源组装已自动化为 `resource_assembler.py` 脚本，LLM 只需执行两个操作：运行脚本 + view_file 输出文件。这彻底消除了"偷懒不读资源自己瞎猜"的可能性。

**原理**：`resource_assembler.py` 读取 `planning{n}.json`，自动提取两层资源声明——页面级 `required_resources`（layout / page_template / principles[]）和卡片级 `cards[].resource_ref`（block / chart / icon / principle），读取每个资源文件的完整内容，按 `[RESOURCES]` 块格式组装输出到文本文件。

**每页 HTML 生成前的强制执行流程**：

```bash
# Step 1: 运行脚本组装资源（机械化，无需 LLM 判断）
python3 SKILL_DIR/scripts/resource_assembler.py \
  OUTPUT_DIR/planning/planning{n}.json \
  --refs SKILL_DIR/references \
  -o OUTPUT_DIR/resources/resources-{n}.txt

# Step 2: 读取组装后的资源文件（view_file）
view_file OUTPUT_DIR/resources/resources-{n}.txt
```

> 首页 HTML 生成前，可选用批量模式一次性为所有页面组装资源：
> ```bash
> python3 SKILL_DIR/scripts/resource_assembler.py \
>   OUTPUT_DIR/planning/ \
>   --refs SKILL_DIR/references \
>   -o OUTPUT_DIR/resources/
> ```
> 之后每页生成前只需 `view_file OUTPUT_DIR/resources/resources-{n}.txt` 即可。

**输出的 [RESOURCES] 块包含**（按两层分区组织，无内容的分区自动省略）：

| 分区 | 来源 | 内容 |
|------|------|------|
| `=== LAYOUT ===` | `required_resources.layout` | 布局文件的完整 HTML 骨架（Grid 结构 + card_style 映射表） |
| `=== PAGE_TEMPLATE ===` | `required_resources.page_template` | 页面结构规范（封面/目录/章节/结束页） |
| `=== PAGE_PRINCIPLES ===` | `required_resources.principles[]` | 页面级设计原则完整内容 |
| `=== CARD_RESOURCES ===` | `cards[].resource_ref` | 按卡片序号分组：每个卡片的 [block]/[chart]/[icon]/[principle] 资源完整内容 |

> 脚本输出会显示资源统计和 WARNING（文件未找到时），方便快速发现 planning JSON 中的路径错误。

**首页生成前必须完整读取的全局资源**（仅一次，全局生效）：
- `references/prompts/prompt-4-design.md` -- 设计规则基础
- `references/pipeline-compat.md` -- 管线约束硬性规则
- `references/styles/README.md` -- 装饰技法工具箱 + 色彩原则
- `references/blocks/card-styles.md` -- **6 种卡片视觉变体的 CSS 实现**（每页都用到）
- `references/principles/README.md` -- 设计原则索引
- `references/blocks/README.md` -- 复合组件索引

> 页面类型专属规范：封面/目录/章节封面/结束页的结构规范已通过 `required_resources.page_template` 指定路径（如 `page-templates/cover.md`），无需另行查映射。**规范只定义"必须有哪些区域"，不提供具体 HTML 代码**。每次生成时，构图方式、排版比例、装饰元素必须根据所选风格的装饰 DNA 自由变化。

> 叙事节奏：整体 PPT 的视觉密度起伏须遵循 `references/narrative-rhythm.md` 的节奏规则和标准模板。

> CSS 动画（可选）：HTML 预览可嵌入渐入/计数/填充/描边动画，见 `references/prompts/animations.md`。不影响 PPTX 输出。

> **禁止跳过策划稿直接生成。** 每页必须先有 Step 4 的结构 JSON。

> **视觉完成度基准**：每页必须达到 `references/quality-baseline.md` 定义的视觉丰富度 checklist。每页最低标准 -- 必须包含：页面标题区、3-5 张混合类型卡片、至少 1 个数据可视化、装饰元素（至少 2 种，且匹配所选风格的装饰 DNA）、完整页脚。

**每页 Prompt 组装公式**：
```
Prompt #4 模板
+ CSS 变量定义（5a 产物）[必须]
+ 该页策划稿 JSON（Step 4 产物，含 cards[]/card_type/chart_type/position/layout_hint）[必须]
+ 该页内容文本（Step 4 产物）[必须]
+ [RESOURCES] 块：view_file resources-{n}.txt 的完整内容（resource_assembler.py 自动组装）[必须]
+ 配图信息（usage + 路径 + placement，来自 planning JSON 的 image 字段 + 5b 产物路径）[可选 -- usage=none 时省略 IMAGE_INFO 块]
```

> **装饰手法不在每页 Prompt 中重复注入。** 装饰工具箱（`styles/README.md`）在首页生成前读取一次，模型每页自由组合不同装饰技法，而不是被同一份装饰说明反复引导。

**核心设计约束**（完整清单见 Prompt #4 内部）：
- 画布 1280x720px，overflow:hidden
- 所有颜色通过 CSS 变量引用，禁止硬编码
- 凡视觉可见元素必须是真实 DOM 节点，图形优先用内联 SVG
- 禁止 `::before`/`::after` 伪元素用于视觉装饰、禁止 `conic-gradient`、禁止 CSS border 三角形
- 配图融入设计：按 `planning{n}.json` 的 `image.usage` 决定融入技法（7 种用法详见 `image-generation.md`）

**布局骨架引用（防错位核心机制）**：每个布局文件（如 `layouts/hero-top.md`）包含完整的 HTML 骨架代码。生成 content 页时，`resources-{n}.txt` 的 LAYOUT 分区已包含完整骨架代码，以此为起点填充内容。跨行/跨列卡片的 `grid-row` / `grid-column` 属性必须与骨架保持一致。详见 Prompt #4 的"布局骨架使用方法"章节。

**逐页生成**：每次只读取 `OUTPUT_DIR/resources/resources-{n}.txt`（已包含该页所有资源），生成该页 HTML 后写入 `OUTPUT_DIR/slides/slide-{NN}.html`，再生成下一页。无需批量处理，每页都是轻量独立操作。

##### 并行生成接口（subagent 预留）

> 当前单 agent 环境下仍逐页串行。此接口定义了并行生成的输入契约，以便将来有 subagent 能力时可直接分发。

每页 HTML 的生成输入**完全自包含**，页面之间无运行时依赖：

```
并行单元输入:
  page_number:       页码
  planning_json:     OUTPUT_DIR/planning/planning{n}.json 的内容
  style_json:        OUTPUT_DIR/style.json 的内容（全局共享，只读）
  image_info:        该页配图信息（usage + path + placement，来自 planning JSON 的 image 字段 + 5b 产物路径，可为空）
  global_resources:  首页前已读取的全局资源（prompt-4 / pipeline-compat / styles/README / principles/README / blocks/README / card-styles.md）
  resources_txt:     resource_assembler.py 为该页生成的 resources-{n}.txt 完整内容（包含页面级+卡片级所有资源）
```

> **简化说明**：`resource_assembler.py` 已将资源组装完全自动化。调度者只需为每页运行一次脚本生成 `resources-{n}.txt`，然后将文件内容作为 `resources_txt` 字段注入即可。

**并行策略**（subagent 可用时）：
- 按 Part 分组（同一 Part 的页面分给同一 subagent，保证章节内视觉一致性）
- 每个 subagent 接收该组所有页面的上述输入，串行生成组内页面
- 不同 Part 的 subagent 可并行执行

##### 每页生成后 6 项自检（必做 -- 写入文件前对照）

每页 HTML 生成后、写入文件前，快速过一遍以下 6 项。如有不通过项，立即修正后再写入：

| # | 检查项 | 判定标准 | 不通过时的修正动作 |
|---|--------|---------|------------------|
| 1 | **内容完整** | 每张卡片有标题 + 正文/数据/列表（无空卡）；data 卡片有可视化元素 | 补充缺失内容，空卡填满 |
| 2 | **布局无重叠** | 所有卡片通过 CSS Grid 自动排列或明确 grid-row/grid-column 定位；跨行/跨列卡片的 span 属性与布局文件一致 | 对照所选布局的 HTML 骨架修正 grid 定位 |
| 3 | **管线安全** | 无 `::before`/`::after` 装饰、无 `conic-gradient`、无 `-webkit-background-clip:text`、无 `mask-image`、无 `clip-path`、无 CSS border 三角形、无 `background-image:url()`；内联 SVG 中无 `<text>` 元素、无 `<use>`/`<symbol>`/`<clipPath>`/`<filter>` 元素；SVG path 只用 M/L/H/V/C/Z 命令（完整清单见 `pipeline-compat.md` 第 1、6 节） | 替换为管线安全写法（真实 DOM / 内联 SVG） |
| 4 | **不溢出画布** | 内容区 `overflow:hidden`；每张卡片 `overflow:hidden`；图表容器有明确 `height`；正文有 `-webkit-line-clamp` 截断 | 缩减内容（缩短正文 > 减少列表项 > 移除装饰） |
| 5 | **色彩规范** | 所有颜色通过 `var(--xxx)` 引用（除 transparent 和 rgba(255,255,255,0.x)）；accent 色不超过同页 2 种 | 替换硬编码颜色为 CSS 变量 |
| 6 | **资源已消费** | `resources-{n}.txt` 中的资源已在 HTML 中体现：布局来自 LAYOUT 分区的骨架；每个卡片的复合组件/图表/图标符合 CARD_RESOURCES 分区中该卡片 [block]/[chart]/[icon] 的设计要点和模板；PAGE_PRINCIPLES 和卡片级 [principle] 在设计决策中被考虑 | 回读 `resources-{n}.txt` 对照修正 |

> 自检不是事后审查，而是生成流程的一部分。把 6 项检查融入"生成 -> 检查 -> 修正 -> 写入"的循环中。

**跨页视觉叙事**：按 `references/narrative-rhythm.md` 的节奏规则和章节色彩递进规则执行，确保密度交替、章节色彩递进、封面-结尾呼应。

**产物**：每页一个 HTML 文件 -> `OUTPUT_DIR/slides/`

##### HTML 自检中断点 [STOP -- 等待用户确认]

> **所有页面 HTML 生成完毕后，暂停等用户自检。** 出错概率低，因此统一自检而非逐页中断。

所有 `slide-XX.html` 写入完成后：

1. 运行 `html_packager.py` 生成 `preview.html`（合并预览，方便用户一次性审阅）
   ```bash
   python3 SKILL_DIR/scripts/html_packager.py OUTPUT_DIR/slides/ -o OUTPUT_DIR/preview.html
   ```
2. **通知用户**：告知用户打开 `preview.html` 翻页审阅所有页面
3. **等待用户反馈**（阻断点），用户可以：
   - **A) 直接确认**：回复"OK"或"没问题"，进入 Step 6
   - **B) 自行编辑 HTML**：直接修改 `slides/slide-XX.html` 文件，改完后回复确认
   - **C) 指示 agent 修改**：告诉 agent 哪些页面需要改什么（如"第 3 页标题颜色太淡"、"第 7 页布局太空"），agent 修改后重新生成 `preview.html` 供再次审阅
4. 确认通过后，进入 Step 6

> 如果用户选择 C，agent 修改 HTML 后必须重新运行 `html_packager.py` 更新预览，然后再次等用户确认。循环直到用户满意。

---

### Step 6: 管线选择 + 后处理 [必做 -- 用户确认 HTML 后立即执行]

> **禁止跳过。** 用户确认 HTML 后必须执行完整的转换管线，不要停在 preview.html 就结束。

#### 6a. 管线选择 [STOP -- 等待用户选择]

> 两条管线各有优劣，**必须让用户选择**，不要替用户做决定。

向用户展示以下选项：

| 管线 | 路径 | 优势 | 劣势 |
|------|------|------|------|
| **A) PNG 管线** | HTML -> PNG -> PPTX | 兼容性极好（任何版本 PPT / WPS / Keynote / Google Slides）；所有 CSS 效果完美保留 | 文字不可编辑（成为像素） |
| **B) SVG 管线** | HTML -> SVG -> PPTX | 文字可编辑（右键"转换为形状"）；矢量无损缩放 | 需要 Microsoft 365 / PPT 2021+；复杂 CSS 可能转换失真 |

**等待用户回复**（阻断点）。

#### 6b. 执行转换

**依赖检查**（首次运行自动执行）：
```bash
pip install python-pptx lxml Pillow 2>/dev/null
```

##### 管线 A：PNG 管线（HTML -> PNG -> PPTX）

```
slides/*.html --> png/*.png --> presentation.pptx
```

1. **PNG 截图** -- 运行 `html2png.py`（Puppeteer 截图，2x 高清）
   ```bash
   python3 SKILL_DIR/scripts/html2png.py OUTPUT_DIR/slides/ -o OUTPUT_DIR/png/ --scale 2
   ```
   **降级**：如果 Node.js 不可用或 Puppeteer 安装失败，跳过并告知用户手动安装 Node.js。

2. **PPTX 生成** -- 运行 `png2pptx.py`（全屏图片嵌入）
   ```bash
   python3 SKILL_DIR/scripts/png2pptx.py OUTPUT_DIR/png/ -o OUTPUT_DIR/presentation.pptx
   ```

##### 管线 B：SVG 管线（HTML -> SVG -> PPTX）

```
slides/*.html --> svg/*.svg --> presentation.pptx
```

1. **SVG 转换** -- 运行 `html2svg.py`（DOM 直接转 SVG，保留 `<text>` 可编辑）
   > **重要**：HTML 设计稿必须遵守 `references/pipeline-compat.md` 中的管线兼容性规则，否则转换后会出现元素丢失、位置错位等问题。
   ```bash
   python3 SKILL_DIR/scripts/html2svg.py OUTPUT_DIR/slides/ -o OUTPUT_DIR/svg/
   ```
   底层用 dom-to-svg（自动安装），首次运行会 esbuild 打包。
   **降级**：如果 Node.js 不可用或 dom-to-svg 安装失败，告知用户并建议改用 PNG 管线。

2. **PPTX 生成** -- 运行 `svg2pptx.py`（OOXML 原生形状解析，PPT 365 可编辑）
   ```bash
   python3 SKILL_DIR/scripts/svg2pptx.py OUTPUT_DIR/svg/ -o OUTPUT_DIR/presentation.pptx --html-dir OUTPUT_DIR/slides/
   ```

#### 6c. 通知用户

告知产物位置和使用方式：
- `preview.html` -- 浏览器打开即可翻页预览（Step 5c 自检阶段已生成）
- `presentation.pptx` -- 最终 PPTX 文件
- **PNG 管线产物**：
  - `png/` -- 每页截图，可直接插入任何演示软件
  - 文字为像素，不可在 PPT 中直接编辑
- **SVG 管线产物**：
  - `svg/` -- 每个 SVG 也可单独拖入 PPT
  - 右键 -> "转换为形状" 即可编辑文字和形状
  - **版本要求**："转换为形状"功能需要 **Microsoft 365 / PowerPoint 2021+**。较低版本（2019 及以下）只能将 SVG 作为不可编辑的图片显示
- **如果转换被降级跳过**，说明原因并告知用户手动安装 Node.js 后可重新运行

**产物**：preview.html + (png/*.png 或 svg/*.svg) + presentation.pptx

---

## 中断恢复机制

> 长流程（15+ 页 PPT）中途中断时，通过 `progress.json` 记录进度，下次从中断点继续。

### progress.json 结构

```json
{
  "version": "1.0",
  "topic": "PPT 主题",
  "complexity": "light | standard | large",
  "total_pages": 15,
  "started_at": "ISO 时间戳",
  "last_updated": "ISO 时间戳",
  "steps": {
    "step_1": {"status": "done | in_progress | pending"},
    "step_2": {"status": "done"},
    "step_3": {"status": "done"},
    "step_4": {"status": "in_progress", "completed_pages": [1,2,3,4,5], "current_page": 6},
    "step_5a": {"status": "pending"},
    "step_5b": {"status": "pending", "completed_pages": []},
    "step_5c": {"status": "pending", "completed_pages": []},
    "step_6": {"status": "pending", "pipeline": null}
  }
}
```

### 写入时机

| 事件 | 更新内容 |
|------|--------|
| Step 1 完成 | 创建 `progress.json`，写入 topic + complexity + step_1=done |
| Step 2 完成 | step_2=done |
| Step 3 完成 | step_3=done, total_pages |
| Step 4 每页写入 | step_4.completed_pages 追加页码 |
| Step 5a 完成 | step_5a=done |
| Step 5b/5c 每页完成 | 对应 completed_pages 追加页码 |
| Step 6a 用户选择管线 | step_6.pipeline = "png" 或 "svg" |
| Step 6 完成 | step_6=done |

### 恢复流程

流程开始时检查 `OUTPUT_DIR/progress.json` 是否存在：
1. 不存在 -> 全新开始
2. 存在 -> 读取并展示当前进度，询问用户"继续"或"重新开始"
3. 用户选择继续 -> 跳到第一个非 done 的步骤，补全缺失产物
4. 用户选择重新开始 -> 删除 progress.json，全新开始

**恢复时的产物校验**：跳到中断步骤前，检查前序步骤的产物文件是否存在（如 outline.json、planning/*.json、style.json）。缺失则回退到该步骤重新生成。

---

## 输出目录结构

```
ppt-output/
  progress.json        # 进度日志（中断恢复用）
  slides/              # 每页 HTML
  resources/           # resource_assembler.py 组装的资源文本块（每页一个）
  png/                 # PNG 截图（PNG 管线产物）
  svg/                 # 矢量 SVG（SVG 管线产物，可导入 PPT 编辑）
  images/              # AI 配图
  preview.html         # 可翻页预览
  presentation.pptx    # 最终 PPTX
  outline.json         # 大纲
  style.json           # 风格定义
  planning/            # 策划稿目录
    planning1.json     # 第 1 页策划稿
    planning2.json     # 第 2 页策划稿
    planning{n}.json   # 第 n 页策划稿（每页独立文件）
```

---

## 质量自检（全局级 -- 与 Step 5c 逐页自检互补）

| 维度 | 检查项 |
|------|-------|
| 全局一致 | CSS 变量跨页一致 / 配色统一 / 配图风格统一 |
| 叙事节奏 | 相邻页 visual_weight 差 <= 5 / 不连续 3 页高密度 / 规则冲突时内容完整性 > 节奏美感 |
| 管线安全 | 所有 HTML 无 `pipeline-compat.md` 禁止清单中的 CSS |

---

## Reference 文件索引

> 完整映射见 `resource-registry.md`。

| 文件 | 何时读 | 内容 |
|------|-------|------|
| `prompts/prompt-1-research.md` | Step 1 | 需求调研 |
| `prompts/prompt-2-outline.md` | Step 3 | 大纲架构 v3.0（叙事弧线 + 论证策略 + Part 逻辑关系） |
| `prompts/prompt-3-planning.md` | Step 4 | 策划稿（含 14 种 card_type + decoration_hints） |
| `prompts/prompt-4-design.md` | Step 5c 首页前 | HTML 设计稿 |
| `blocks/README.md` | Step 4 首页前 | 复合组件选择指南 + 总表 |
| `blocks/{type}.md` | Step 4 + 5c 按需 | 8 种复合区域展示组件 |
| `principles/README.md` | Step 4 首页前 | 6 大设计原则索引 |
| `principles/{name}.md` | 按需 | 视觉层级/认知负荷/构图/色彩/数据可视化/叙事 |
| `styles/README.md` | Step 5a + 5c 首页前 | 色彩原则 + 装饰工具箱 |
| `styles/{id}.md` | Step 5a | 8 个参考调色板 |
| `layouts/README.md` | Step 5c 首页前 | 骨架使用总则 |
| `layouts/{layout}.md` | Step 5c 按需 | 10 种布局骨架 |
| `charts/{type}.md` | Step 5c 按需 | 13 种图表模板 |
| `icons/{category}.md` | Step 5c 按需 | 4 类 SVG 图标 |
| `page-templates/{type}.md` | Step 5c 按需 | 页面结构建议 |
| `narrative-rhythm.md` | Step 3 后 | 节奏 + 色彩递进 + 规则冲稁优先级 + 边缘场景 |
| `pipeline-compat.md` | Step 5c 首页前 | CSS 禁止清单 |
| `quality-baseline.md` | Step 5c 首页前 | 视觉完成度 checklist |
| `resource-registry.md` | 维护时 | **全局映射唯一权威源** |
| `scripts/resource_assembler.py` | Step 5c 每页生成前 | 自动组装 [RESOURCES] 文本块 |
| `scripts/planning_validator.py` | Step 4 每页写入后 + 全量验证 | 策划稿 JSON 格式与规则验证（单页+跨页） |
