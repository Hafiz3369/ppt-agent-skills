# SourceSynth Phase 1 Playbook -- 资料读取与结构化提炼

## 目标

将用户提供的现有资料（文档、文本、数据表、PPT等）提炼成结构化素材摘要 `source-brief.txt`，使其能被大纲和策划阶段稳定消费。

---

## 策略识别（基于需求）

从 `requirements-interview.txt` 的 `资料使用策略` 字段识别你的阅读和摘取模式：

| 策略 | 处理方式 |
|------|---------|
| 全量吸收 | 读取所有资料，尽可能提取每份文件的核心要点 |
| 择优引用 | 只提取与 PPT 目标最相关的内容，低相关内容跳过 |
| 仅背景参考 | 仅提炼背景信息，不直接引用原文作为论据 |
| 严格基于原文 | 不得补充、推断或扩写，所有内容必须原文可查 |

---

## 格式感知处理指南

遇到不同格式的参考文件时，按以下优先级提取：

| 格式 | 处理方式 | 重点提取 |
|------|---------|---------| 
| PDF | 用 pdf-reader 或 markitdown 解析 | 图表数据、结论段落、脚注引用 |
| Word (.docx) | 用 markitdown 转换后读取 | 章节结构、核心论点、嵌入表格 |
| Excel (.xlsx) | 用 markitdown 转换后读取 | 数据表格->直接转为结构化数据包格式 |
| PPT (.pptx) | 用 markitdown 提取文本和结构 | 每页标题+要点、speaker notes、数据图表 |
| 纯文本/Markdown | 直接读取 | 按语义分块提取 |
| 代码文件 | 直接读取 | 架构说明、注释、README 中的描述 |
| 图片 | 用图像识别描述内容 | 图表数据、截图内容、品牌元素 |

---

## 结构化数据狩猎（核心任务）

在阅读用户资料时，除了提取宏观点，必须**主动寻找以下 11 种 PPTX 可用的结构化数据**：

| 数据类型 | 输出格式规范 | 对应 PPT 组件 |
|-----------|-------------|---------------|
| `metrics` | `{value} {unit} ({trend}) [来源: FileX]` | `kpi` / `metric-row` |
| `data_tables` | 多行多列的 md table，附 `[来源]` | `table` 卡片 |
| `trend_series`| `{time_1}: {value} \n {time_2}: {value}...` 换行平铺，带 `[来源]` | `sparkline` 折线 |
| `ranked_list` | `1. {name}: {value} \n 2. {name}...` | `list` / `data_highlight` |
| `before_after`| `Before: {x} -> After: {y} (差值: {diff}) [来源]` | `comparison` 卡片 |
| `funnel_data` | `{label1}: {val} -> {label2}: {val} (流失: {rate})` | `funnel` 图 |
| `pie_data`    | `{seg_1}: {percentage}%, {seg_2}... [来源]` | `ring` / `treemap` |
| `timelines`   | `{year/date}: {milestone_desc} [来源]` | `timeline` 区块 |
| `expert_quotes`| `"{quote_text}" -- {person/title}, {org} [来源]` | `quote` 大字引言 |
| `team_profiles`| `{name} ({title}): {desc}` | `people` 人物卡 |
| `process_flows`| `Step 1: {x} -> Step 2: {y}...` | `process` 流程图 |

---

## source-brief.txt 产出骨架

综合所有资料，按以下结构输出到目标路径，不要在此阶段做审查修补：

```text
# 资料摘要

## 基本信息
- 来源类型：用户现有资料（非联网搜索）
- 资料文件数：N
- 覆盖主题：...

## 核心论点与数据
（按主题分组，每条数据标注来源文件名）

### [主题1]
- [论点/数据] — 来源：[文件名]
- ...

## 关键数据清单
（所有可被直接引用的数据、统计、案例）
- [数据] — 来源：[文件名]

## PPTX 结构化数据包
### metrics
- 47.3 % (上升) [来源: ...]
... （至少提取 3 种不同的大块数据）

## 素材边界
- 覆盖完整的内容：...
- 资料中缺失的内容（PPT 可能需要但资料未覆盖）：...
- 数据矛盾项（如果有多个文件数据打架）：...

## 资料使用建议
- 强论据（直接引用）：...
- 辅助背景（间接参考）：...
```
