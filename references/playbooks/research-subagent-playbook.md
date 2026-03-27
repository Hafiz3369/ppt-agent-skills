# 资料收集 Sub-agent Playbook

## 何时读取

- 当你被主 agent 指派为资料收集 sub-agent 时必读
- Step 1 需求调研完成后触发

## 目标

基于 `OUTPUT_DIR/requirements.json` 规划并执行多维度搜索，最大化搜集与主题相关的高质量原始信息。

你是信息猎人，不是分析师。职责是**尽可能多地搜回有价值的原始素材**，不做可信度评估和结构化整理（那是资料准备 sub-agent 的工作）。宁可多搜一条没用的，不可漏掉一条有用的。

## 输入包

主 agent 提供（从 `requirements.json` 中提取）：

| 字段 | 用途 |
|------|------|
| `topic` | 核心搜索主题 |
| `audience` | 决定搜索深度（专业受众需更深入的技术/学术资料） |
| `emphasis` (Q5) | 搜索维度权重分配 |
| `persuasion_style` (Q6) | 搜索重心倾斜 |
| `content_must_include` (Q10) | 必搜内容（每项至少 1 个专门查询） |
| `content_must_avoid` (Q10) | 搜索过滤 |
| `complexity_level` | 查询数量基准 |
| `dynamic_answers` (Q13-15) | 补充搜索方向 |

## 搜索维度规划

### 六大搜索维度

每个维度至少 1 个查询，`emphasis` 指定的重点维度可多个。不要所有查询都是同一维度的换词。

| 维度 | 示例查询 | 目的 |
|------|---------|------|
| **核心定义** | "{主题} 是什么 / 定义 / 核心概念" | 基础事实 |
| **市场数据** | "{主题} 市场规模 / 增长率 / 行业报告 2024-2026" | 数据填充 |
| **竞品/对比** | "{主题} vs {竞品} / 对比分析" | 对比论证 |
| **案例/应用** | "{主题} 客户案例 / 应用场景" | 故事化说服 |
| **趋势/展望** | "{主题} 发展趋势 / 未来展望" | 结尾素材 |
| **权威观点** | "{主题} 专家评价 / 行业报告 / 白皮书" | 权威背书 |

### 查询数量基准

一旦 `requirements.json` 已经写出 `complexity_level`，就直接按该字段执行，不再重复猜测页数；下表只是 Step 1 判定复杂度时的默认阈值参考。

| 复杂度 | 查询数量 |
|--------|---------|
| light（<= 8 页） | 3-5 |
| standard（9-18 页） | 8-12 |
| large（> 18 页） | 10-15 |

### 维度权重分配（根据 persuasion_style）

| persuasion_style | 加权维度 |
|-----------------|---------|
| 数据驱动 | 市场数据 x2、权威观点 x1.5 |
| 案例驱动 | 案例/应用 x2 |
| 权威背书 | 权威观点 x2、市场数据 x1.5 |
| 方法论 | 核心定义 x1.5、案例/应用 x1.5 |

## 执行规则

### 工具使用

盘点当前可用的信息获取工具，全部用上：

| 工具类型 | 用途 | 优先级 |
|---------|------|--------|
| **搜索引擎**（search_web / grok-search） | 广撒网 | 首选 |
| **URL 读取**（read_url_content） | 深挖高价值页面 | 发现高价值 URL 时用 |
| **文档解析**（markitdown / pdf-reader） | 用户源材料 | 有源材料时必用 |

### 并行原则

- 独立查询之间**必须并行**，不要串行
- URL 深挖可与其他搜索并行

### 信息提取规则

- 必须提取**关键段落**，不是只贴 URL
- 数字/数据精确记录，不概括为"增长了很多"
- 引用观点记录原话或精确转述
- 多个页面说同一件事，记录最权威/最详细的，保留所有来源

### 搜索深度

- 初始搜索揭示新重要线索时，可追加 1-2 个补充查询（不超过总数 30%）
- 高价值来源值得 read_url_content 深挖
- 总搜索不超过 2 轮，不要无限递归

## 产物格式

写入 `OUTPUT_DIR/raw-research.json`：

```json
{
  "meta": {
    "topic": "搜索主题",
    "total_queries": 8,
    "total_findings": 42,
    "queries_by_dimension": {"核心定义": 2, "市场数据": 3, "竞品对比": 1, "案例应用": 1, "趋势展望": 1, "权威观点": 1},
    "search_tools_used": ["search_web", "read_url_content"],
    "timestamp": "ISO 时间戳"
  },
  "queries": [
    {
      "dimension": "核心定义 | 市场数据 | 竞品对比 | 案例应用 | 趋势展望 | 权威观点",
      "query": "实际搜索查询文本",
      "tool_used": "search_web | read_url_content | ...",
      "raw_findings": [
        {
          "content": "提取的关键段落（精华摘要，非全文）",
          "source_url": "来源 URL",
          "source_name": "来源名称",
          "has_data": true,
          "data_snippet": "具体数字：市场规模 156 亿美元（2025）"
        }
      ]
    }
  ],
  "user_materials": [
    {
      "file_path": "用户提供的源材料路径",
      "summary": "材料内容摘要",
      "key_extracts": ["提取的关键段落"]
    }
  ]
}
```

## 质量底线

| 检查项 | 标准 |
|--------|------|
| 查询数量 | >= complexity_level 对应下限 |
| 维度覆盖 | 6 个维度各至少 1 个查询 |
| 必含内容 | content_must_include 每项至少 1 个专门查询 |
| 内容质量 | 每条 finding 有 content，不只是 URL |
| 数据精确 | 数字精确记录 |
| 过滤 | 不含 content_must_avoid 的内容 |

## Sub-agent Prompt 模板

```text
你是 PPT 资料收集专员，负责为主题 "{topic}" 搜集原始素材。

先读取 SKILL_DIR/references/playbooks/research-subagent-playbook.md。

你的唯一任务是搜索和收集信息，不做可信度评估或结构化分析。

输入包：
{主 agent 注入 requirements.json 相关字段}

执行流程：
1. 规划多维度查询（6 大维度全覆盖，按 persuasion_style 加权）
2. content_must_include 每项必须有专门查询
3. 用所有可用搜索工具并行执行
4. 提取关键段落，精确记录数据
5. 不搜 content_must_avoid 中的内容
6. 结果写入 OUTPUT_DIR/raw-research.json
```

## 主 agent 的回收职责

- 检查 `raw-research.json` 存在性
- 读取 `meta` 验证查询数量和维度覆盖
- 如果 `content_must_include` 有覆盖缺口，要求补搜
- 不做可信度判断（下一个 sub-agent 的事）
