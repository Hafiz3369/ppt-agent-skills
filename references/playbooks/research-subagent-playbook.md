# 资料收集 Sub-agent Playbook

## 何时读取

- 当你被主 agent 指派为资料收集 sub-agent 时必读
- Step 1 需求问卷前的预检索触发（`mode=presearch`）
- Step 2 正式资料搜集触发（`mode=full`）

## 目标

在不同模式下执行搜索并沉淀可复用原始素材：

- `presearch`：基于主题做初级背景检索，服务 Step 1 提问设计
- `full`：基于 `requirements.json` 做完整资料搜集，并合并 presearch 结果

你是信息猎人，不是分析师。职责是**尽可能多地搜回有价值的原始素材**，不做可信度评估和结构化整理（那是资料准备 sub-agent 的工作）。宁可多搜一条没用的，不可漏掉一条有用的。

## 运行模式

| 模式 | 触发阶段 | 输入 | 输出 |
|------|----------|------|------|
| `presearch` | Step 1 问卷前 | `topic`（必填） | `OUTPUT_DIR/runtime/presearch-raw-research.json` |
| `full` | Step 2 正式搜集 | `requirements.json`（必填），可选 `seed raw research` | `OUTPUT_DIR/raw-research.json` |

## 输入包（full 模式）

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

`presearch` 模式查询数量固定为 3-5（用于生成问卷线索，不追求 full 覆盖）。

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

写入 `OUTPUT_DIR/raw-research.json`（presearch 模式写入 `OUTPUT_DIR/runtime/presearch-raw-research.json`，结构相同）：

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
| 查询数量 | full: >= complexity_level 对应下限；presearch: 3-5 |
| 维度覆盖 | full: 6 个维度各至少 1 个查询；presearch: 覆盖关键维度即可 |
| 必含内容 | full 模式下 content_must_include 每项至少 1 个专门查询 |
| 内容质量 | 每条 finding 有 content，不只是 URL |
| 数据精确 | 数字精确记录 |
| 过滤 | full 模式不含 content_must_avoid 的内容 |

## presearch 合并规则（Step 2）

- `full` 模式若收到 `seed raw research`，必须先读取并合并。
- 合并时对 `query + source_url + content` 做去重，避免重复素材污染统计。
- 不得覆盖掉 seed 中已有的高价值条目；只允许补充与去重。

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
