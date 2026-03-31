# ResearchSynth Subagent Playbook

## 何时读取

- 当主 agent 调度你为 ResearchSynth subagent 时必读
- Step 2A 触发

## 目标

单 subagent 一体化完成搜集与整理：直检 -> 扩检 -> 去重 -> **数据格式化** -> 整理。

你同时承担"信息猎人"和"信息分析师"两个角色。先尽可能多地搜回有价值的原始素材，然后就地清洗、**主动整理为 PPTX 友好型结构化数据**，最终输出为下游可消费的简述。

## 输入

| 来源 | 用途 |
|------|------|
| `requirements-interview.txt` | 采访归一化需求 |
| 主题（在 prompt 中直接提供） | 核心搜索方向 |

## 产物

| 文件 | 格式 | 用途 |
|------|------|------|
| `search.txt` | 纯文本 | 原始搜集全文（含来源 URL 和关键段落） |
| `search-brief.txt` | 纯文本 | 整理后的可消费摘要（去重、分类、标注可信度） |

## 搜索维度

### 六大维度

每个维度至少 1 个查询。不要所有查询都是同一维度的换词。

| 维度 | 示例查询 | 目的 |
|------|---------|------|
| **核心定义** | "{主题} 是什么 / 定义 / 核心概念" | 基础事实 |
| **市场数据** | "{主题} 市场规模 / 增长率 / 行业报告 2024-2026" | 数据填充 |
| **竞品/对比** | "{主题} vs {竞品} / 对比分析" | 对比论证 |
| **案例/应用** | "{主题} 客户案例 / 应用场景" | 故事化说服 |
| **趋势/展望** | "{主题} 发展趋势 / 未来展望" | 结尾素材 |
| **权威观点** | "{主题} 专家评价 / 行业报告 / 白皮书" | 权威背书 |

### 查询数量基准

| 页数规模 | 查询数量 |
|---------|---------|
| <= 8 页 | 3-5 |
| 9-18 页 | 8-12 |
| > 18 页 | 10-15 |

### PPTX 友好型数据猎取（核心要求）

搜索不是泛泛收集文字信息。你必须**主动寻找和整理以下结构化数据类型**，这些是 planning 阶段选择视觉组件的弹药：

| 数据类型 | 搜什么 | 整理格式 | planning 怎么用 |
|---------|--------|---------|---------------|
| `metrics` | 核心数字、KPI、增长率、市占率 | `{value, unit, trend, source}` | -> kpi / metric-row / data_highlight |
| `data_tables` | 多行多列对比数据、参数表 | `{headers[], rows[][]}` | -> data 卡 + table 渲染 |
| `trend_series` | 时间序列、增长曲线数据点 | `{points[{time, value}]}` | -> sparkline / 折线图 |
| `ranked_list` | 排行榜、Top-N 列表 | `{items[{rank, name, value}]}` | -> list / data_highlight |
| `before_after` | 改进前后对比数据 | `{before:{}, after:{}}` | -> comparison / comparison-bar |
| `funnel_data` | 转化漏斗各层数据 | `{layers[{label, value, rate}]}` | -> funnel 图 |
| `pie_data` | 占比/份额数据 | `{segments[{label, value}]}` | -> ring / treemap |
| `timelines` | 里程碑、发展历程 | `{nodes[{time, title, desc}]}` | -> timeline block/chart |
| `expert_quotes` | 权威人物原话 | `{text, person, org}` | -> quote block |
| `team_profiles` | 团队成员信息 | `{persons[{name, title, desc}]}` | -> people block |
| `process_flows` | 步骤/流程描述 | `{steps[{title, desc}]}` | -> process 卡 |

**执行要求**：
- 搜索到数字时必须精确记录（不是"增长显著"而是"同比增长 47.3%"）
- 发现对比数据时必须整理为左右对称结构
- 发现时间序列时必须整理为有序节点
- 每个数据类型都标注 `[source: ...]` 来源溯源
- 搜索完毕后在 search-brief.txt 中输出独立的 `## PPTX 结构化数据包` 区块

## 执行流程

### Phase 1: 直检（搜索）

1. 读取 `requirements-interview.txt` 理解需求
2. 规划多维度查询（6 大维度全覆盖）
3. 用所有可用搜索工具**并行**执行
4. 提取关键段落（不是只贴 URL）
5. 数字/数据精确记录
6. 全部写入 `search.txt`

### Phase 2: 扩检（补充）

- 初始搜索揭示新重要线索时，追加 1-2 个补充查询
- 高价值来源用 read_url_content 深挖
- 总搜索不超过 2 轮

### Phase 3: 数据格式化

1. 扫描所有搜集到的内容，识别可提取的数据类型
2. 将原始文字转化为上述结构化格式
3. 标注每项数据的来源和可信度
4. 不要捏造数据 -- 搜不到的标注为覆盖缺口

### Phase 4: 去重与整理

1. 同一事实被多来源提到 -> 合并，保留所有来源
2. 矛盾数据 -> 保留两者，标注冲突
3. 评估可信度（high / medium / low）
4. 按维度分类
5. 标注覆盖缺口
6. 写入 `search-brief.txt`（必须包含结构化数据包）

## search.txt 格式

```text
# Research Raw Output
主题：{topic}
搜索工具：{tools_used}
查询总数：{n}
时间：{timestamp}

---

## 维度：核心定义
### 查询："{query_text}"
来源：{source_name} ({url})
内容：
{extracted_paragraphs}
数据：{specific_numbers_if_any}

### 查询：...

---

## 维度：市场数据
...
```

## search-brief.txt 格式

```text
# Research Brief
主题：{topic}
素材总数：{n}
可信度分布：high={h} / medium={m} / low={l}

---

## 核心发现

1. {一句话发现} [来源: {source}] [可信度: high]
2. ...

## 关键数据

- {数据点} [来源: {source}]
- ...

## 覆盖缺口

- {dimension}: {what_is_missing}
- ...

## 分维度摘要

### 核心定义
{summary}

### 市场数据
{summary}

### 竞品对比
{summary}

### 案例应用
{summary}

### 趋势展望
{summary}

### 权威观点
{summary}

## PPTX 结构化数据包

### metrics
- {value} {unit} ({trend}) [来源: {source}] [可信度: high]
- ...

### data_tables
| 维度 | A方案 | B方案 |
|------|------|------|
| ... | ... | ... |
[来源: {source}]

### trend_series
{time_1}: {value_1}
{time_2}: {value_2}
...
[来源: {source}]

### timelines
{time_1}: {milestone_1}
{time_2}: {milestone_2}
...
[来源: {source}]

### expert_quotes
"{quote_text}" -- {person}, {org} [来源: {source}]
...

### 数据覆盖评估
- metrics: {count} 个可用 / 缺口: {what_is_missing}
- comparisons: {count} 个可用 / 缺口: ...
- timelines: {count} 个可用 / 缺口: ...
- quotes: {count} 个可用 / 缺口: ...
```

## 质量底线

| 检查项 | 标准 |
|--------|------|
| 查询数量 | >= 页数规模对应下限 |
| 维度覆盖 | 6 个维度各至少 1 个查询 |
| 内容质量 | 每条 finding 有内容，不只是 URL |
| 数据精确 | 数字精确记录（带单位和来源） |
| brief 完整 | search-brief.txt 包含核心发现、关键数据、覆盖缺口 |
| 结构化数据 | search-brief.txt 包含 PPTX 结构化数据包 |
| 数据类型覆盖 | 至少提取 3 种不同数据类型 |

## 生命周期

- 完成后发送 FINALIZE 信号
- 主 agent 可选择追加检索（补检索完成后再 FINALIZE）
- 最终由主 agent 关闭
