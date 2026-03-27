# 资料准备 Sub-agent Playbook

## 何时读取

- 当资料收集 sub-agent 完成后，主 agent 调度你时必读
- 你的输入是 `raw-research.json`，不是搜索工具

## 目标

将原始搜索结果转化为高信噪比的结构化素材包，为下游的大纲策划和内容分配提供坚实数据支撑。

你是信息分析师，不是搜索者。职责是**清洗、评估、分类、打包**，让每一条数据都带着可信度标签和下游消费建议到达大纲架构师手中。

## 输入包

| 文件 | 来源 | 用途 |
|------|------|------|
| `OUTPUT_DIR/raw-research.json` | 资料收集 sub-agent 产物 | 原始搜索结果 |
| `OUTPUT_DIR/requirements.json` | Step 1 产物 | 分类维度和过滤规则 |

## 执行流程

### 1. 去重与合并

- 同一事实被多个来源提到 → 合并为一条，保留所有来源（增加可信度）
- 矛盾数据 → 保留两者，标注 `conflicting_with` 对方 ID
- 同一来源的多条信息保持独立（一条来源可能同时贡献定义和数据）

### 2. 可信度评估

| 等级 | 标准 | 下游使用 |
|------|------|---------|
| **high** | 权威机构报告（Gartner/IDC/政府统计）、学术论文、官方文档 | 可用于 data_highlights、关键论据 |
| **medium** | 行业媒体报道、企业博客、分析师观点 | 可用于辅助论据、趋势描述 |
| **low** | 论坛讨论、自媒体、无来源数据 | 仅作参考，不用于关键数据展示 |

判定依据：
- 来源机构的权威性
- 数据是否有明确出处和时间
- 是否有独立可验证的引用链
- 是否被多个独立来源交叉验证

### 3. 素材分类

| 分类 key | 说明 | 典型下游消费 |
|----------|------|-------------|
| `definition` | 定义、概念、原理 | 大纲开篇/概述 |
| `market_data` | 市场规模、增长率、份额 | data 卡片、图表 |
| `comparison` | 竞品对比、优劣势 | comparison 卡片 |
| `case_study` | 客户案例、应用场景 | quote/案例卡片 |
| `trend` | 趋势、展望、路线图 | 结尾展望 |
| `authority` | 专家观点、权威报告结论 | quote 卡片、权威背书 |
| `technical` | 技术细节、架构、原理 | 技术说明页 |

一条素材可以有多个分类（如一条权威报告中的数据同时属于 `market_data` + `authority`）。

### 4. 关联映射

标注每条素材与 `requirements.json` 的关联：
- `emphasis`（Q5 内容侧重）-- 哪些素材支撑用户关注的重点
- `persuasion_style`（Q6 说服力要素）-- 哪些素材匹配用户的说服策略
- `content_must_include`（Q10 必含内容）-- 哪些素材满足硬性要求

### 5. 覆盖缺口分析

检查并报告：
- `content_must_include` 中哪些项目没有 high/medium 素材覆盖
- 6 大搜索维度中哪些维度素材稀薄（< 2 条 high/medium）
- 缺口对大纲的潜在影响

## 产物格式

写入 `OUTPUT_DIR/research-package.json`：

```json
{
  "meta": {
    "topic": "主题",
    "total_materials": 35,
    "by_reliability": {"high": 12, "medium": 18, "low": 5},
    "by_category": {"definition": 4, "market_data": 8, "comparison": 3, "case_study": 6, "trend": 5, "authority": 4, "technical": 5},
    "coverage_report": {
      "content_must_include_coverage": {"项目A": true, "项目B": false},
      "thin_dimensions": ["竞品对比"]
    },
    "timestamp": "ISO 时间戳"
  },
  "materials": [
    {
      "id": "M001",
      "fact": "一句话核心发现",
      "data": "具体数据/数字（如有）",
      "source": "来源名称",
      "source_url": "来源 URL",
      "reliability": "high | medium | low",
      "categories": ["market_data", "authority"],
      "relevance_to": ["emphasis.技术细节", "content_must_include.市场份额"],
      "potential_card_types": ["data", "quote"],
      "conflicting_with": null
    }
  ],
  "gaps": [
    {
      "description": "缺少 XX 领域的权威数据",
      "dimension": "市场数据",
      "content_must_include_item": "XX 市场份额（如适用）",
      "impact": "大纲中 XX 部分可能缺乏数据支撑",
      "suggestion": "建议补搜 XX 相关报告"
    }
  ]
}
```

## 质量底线

| 检查项 | 标准 |
|--------|------|
| 每条素材 | 必须有 `fact` + `source` + `reliability` + `categories` |
| 必含覆盖 | content_must_include 每项至少 1 条 high/medium 素材 |
| 缺口报告 | 有覆盖缺口必须在 `gaps` 中标注 |
| low 比例 | low 可信度素材不超过总量 30% |
| 冲突标注 | 矛盾数据必须标注 `conflicting_with` |
| 分类准确 | 每条素材至少有 1 个 category |

## Sub-agent Prompt 模板

```text
你是 PPT 资料分析师，负责将原始搜索结果整理为高质量结构化素材包。

先读取 SKILL_DIR/references/playbooks/material-prep-subagent-playbook.md。

你的唯一任务是清洗、评估、分类、打包素材。不做大纲策划，不做搜索。

读取：
1. OUTPUT_DIR/raw-research.json（原始搜索结果）
2. `OUTPUT_DIR/requirements.json`（分类和过滤依据）

执行流程：
1. 去重合并（同一事实多来源 → 合并保留所有来源）
2. 可信度评估（high/medium/low，判定依据见 playbook）
3. 素材分类（7 大类别）
4. 关联映射（与 `requirements.json` 的 emphasis/persuasion_style/content_must_include）
5. 覆盖缺口分析
6. 输出写入 OUTPUT_DIR/research-package.json
```

## 主 agent 的回收职责

- 检查 `research-package.json` 存在性和 `meta` 完整性
- 重点关注 `gaps` -- 如果 `content_must_include` 有覆盖缺口：
  1. 可调度资料收集 sub-agent 补搜（轻量补搜，只针对缺口）
  2. 补搜结果追加到 `raw-research.json`，再让资料准备 sub-agent 增量更新
  3. 或标注缺口，告知大纲编写 sub-agent 在对应部分标注 `found_in_search: false`
- 将 `research-package.json` 路径传给大纲编写 sub-agent
