# 大纲编写 + 自审 Playbook

## 何时读取

- 当主 agent 调度你编写大纲时必读
- 你同时负责编写和自审（不再有独立审查 subagent）

## 目标

基于结构化素材和用户需求，设计一份具有说服力的叙事大纲，并在交回前完成严格自审。

你是大纲架构师兼质量门卫。职责是**构建叙事骨架** + **自审验收**。

## 输入

| 文件 | 用途 |
|------|------|
| `requirements-interview.txt` | 用户需求完整描述 |
| `search-brief.txt` / `source-brief.txt` | 素材摘要 |

## 产物

| 文件 | 格式 |
|------|------|
| `outline.txt` | 纯文本大纲（含自审通过标记） |

## 方法论

### 三大支柱

1. **金字塔原理** -- 结论先行、以上统下、归类分组、逻辑递进
2. **叙事弧线** -- 情感轨迹有起伏
3. **论证策略** -- 每 Part 选择匹配的论证方式

### 5 步思考过程

1. **提炼全局核心论点** -- 1 句话灵魂
2. **确定 Part 数量和主题** -- 含 Part 间逻辑关系
3. **为每 Part 选择论证策略** -- data_driven / case_study / comparison / framework / step_by_step / authority
4. **分配页面并确定每页论点** -- 每页一句话 page_goal（不含"和"字）
5. **标注每页数据需求** -- 对照素材摘要

## 执行流程

### Phase 1: 编写大纲

1. 读取 `requirements-interview.txt`
2. 读取素材摘要（search-brief / source-brief）
3. 按 5 步思考过程推导大纲
4. 写入 `outline.txt`

### Phase 2: 严格自审

大纲写完后，立即切换到审查者视角，逐项检查：

| # | 检查项 | 标准 | 不通过的处理 |
|---|--------|------|-------------|
| 1 | 页数 | 符合需求中的 page_count | 调整页面数量 |
| 2 | Part 规模 | 每 Part >= 2 页 | 合并或扩充 |
| 3 | Part 逻辑 | Part 之间有明确逻辑递进，不是主题并列 | 调整 Part 顺序或合并 |
| 4 | 数据支撑 | 核心论据在素材摘要中有支撑 | 标注"素材未覆盖" |
| 5 | page_goal | 每页 goal 一句话，不含"和" | 拆页 |
| 6 | 叙事弧线 | 情感强度有起伏 | 调整密度分配 |
| 7 | 核心论点 | 有明确的 core_thesis | 补全 |

### Phase 3: 修复

- 自审不通过时，**直接修改 outline.txt**
- 不是另写一份，是在原稿上精准修改
- 修改后重新自审（最多 2 轮）

### Phase 4: 交回

- 在 `outline.txt` 末尾追加自审通过标记：

```text
---
SELF_REVIEW_PASS
自审轮数：{n}
自审时间：{timestamp}
```

- 发送 FINALIZE

## outline.txt 格式

```text
# 大纲
核心论点：{core_thesis}
叙事结构：{narrative_structure}
总页数：{total_pages}

---

## Part 1: {part_title}
Part 目标：{part_goal}
论证策略：{argument_mode}
与上一 Part 的关系：{transition}

### 第 1 页：{page_title}
- 页目标：{page_goal}
- 叙事角色：{narrative_role}
- 论证方式：{proof_type}
- 数据需求：{data_requirements}
- 素材来源：{found_in_search: true/false}

### 第 2 页：...

---

## Part 2: ...

---

SELF_REVIEW_PASS
自审轮数：1
自审时间：{timestamp}
```

## 质量底线

| 检查项 | 标准 |
|--------|------|
| 格式 | 包含核心论点、Part 结构、页面定义 |
| 自审标记 | 包含 SELF_REVIEW_PASS |
| 页数 | 符合需求 |
| Part 完整 | 每 Part >= 2 页 |

## 生命周期

- 编写 + 自审 + 修复在同一 agent 内完成
- 自审通过后 FINALIZE
- 主 agent 回收并关闭
- 如果主 agent gate 不通过，会新开 agent 重做（不复用）
