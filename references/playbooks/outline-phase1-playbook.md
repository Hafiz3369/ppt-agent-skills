# Outline Phase 1 Playbook -- 大纲编写思路与结构生成

## 目标

基于结构化素材和用户需求，设计一份具有说服力的叙事大纲。你是大纲架构师，职责是**构建叙事骨架**，而不是填充具体内容代码。

---

## 方法论

### 三大支柱

1. **金字塔原理** -- 结论先行、以上统下、归类分组、逻辑递进
2. **叙事弧线** -- 情感轨迹有起伏（开场抓人、中间详实、结尾升华）
3. **论证策略** -- 每 Part 选择极其匹配的论证方式

### 5 步思考过程

1. **提炼全局核心论点** -- 纵观全盘，写出 1 句话灵魂
2. **确定 Part 数量和主题** -- 含 Part 间逻辑关系（递进/转折/因果）
3. **为每 Part 选择论证策略** -- data_driven / case_study / comparison / framework / step_by_step / authority
4. **分配页面并确定每页论点** -- **每页只有一句话 page_goal，绝不能含"和"字**（如果有"和"，说明这页装了两个目标，必须拆分成两页）
5. **标注每页数据需求** -- 对照素材摘要（`search-brief`或`source-brief`），指出这页需要什么数据支撑，有没有现成的

---

## outline.txt 强制格式骨架

你的输出必须严格遵守以下层级与字段，下游的 Step 4 将会逐行解析你的输出。不要随意更改键名（如 `页目标` 不能改成 `页面目的`）。

```text
# 大纲
核心论点：{一句话灵魂，贯穿全篇的中心论断}
叙事结构：{问题->方案->效果 / 是什么->为什么->怎么做 / 全景->聚焦->行动 / 对比论证 / 时间线 / 其他}
总页数：{N}

---

## Part 1: {part_title}
Part 目标：{part_goal}
论证策略：{data_driven / case_study / comparison / framework / step_by_step / authority}
与上一 Part 的关系：{无（首Part）/ 递进 / 转折 / 因果 / 并列}

### 第 1 页：{page_title}
- 页目标：{page_goal，一句话，不含"和"字}
- 叙事角色：{cover / chapter / data / case / comparison / process / summary / cta}
- 论证方式：{proof_type}
- 数据需求：{这一页需要什么数据来支撑论点}
- 素材来源：{found_in_brief: true/false，若 false 标注缺口_说明为何缺失却仍需此页}

### 第 2 页：{page_title}
...

---

## Part 2: ...
```

**字段枚举约束**：
- `叙事角色` 必须从 `{cover, chapter, data, case, comparison, process, summary, cta}` 中静态选择。
