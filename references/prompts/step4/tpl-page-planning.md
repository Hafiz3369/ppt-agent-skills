# Stage 1: Page Planning -- 第 {{PAGE_NUM}} 页（共 {{TOTAL_PAGES}} 页）

> **【系统级强制指令 / CRITICAL OVERRIDE】**
> 本 prompt 已包含了你在此阶段所需的**全部**任务目标与 Playbook 细则。
> **严格禁止调用工具去读取外层的 `SKILL.md` 或主控全局规则文件！**
>
> 本阶段的唯一目标：产出 `{{PLANNING_OUTPUT}}`。字段名和枚举值**以 validator 合同为准**，不要自创别名。
> 若外层 orchestrator 已提供阶段推进协议，则外层协议优先于本 prompt 中的完成信号描述。

这是你为第 {{PAGE_NUM}} 页执行的**第一阶段核心任务**：策划定骨稿。
你暂时不要写 HTML 代码，全力填好并校验 `{{PLANNING_OUTPUT}}`。

---

## Playbook（执行细则）

{{PLAYBOOK}}

---

## Design Principles Quick Reference

{{PRINCIPLES_CHEATSHEET}}

---

## 任务包

| 项目 | 路径/值 |
|------|--------|
| 页码 | {{PAGE_NUM}} / {{TOTAL_PAGES}} |
| 需求 | `{{REQUIREMENTS_PATH}}` |
| 大纲 | `{{OUTLINE_PATH}}` |
| 素材 | `{{BRIEF_PATH}}` |
| 风格 | `{{STYLE_PATH}}` |
| 图片素材目录 | `{{IMAGES_DIR}}` |
| SKILL 目录 | `{{SKILL_DIR}}` |
| 资源目录 | `{{REFS_DIR}}` |

---

## 产物路径

- 策划稿 JSON：`{{PLANNING_OUTPUT}}`
- 文件内容必须是**纯 JSON 对象**（可直接写对象，也可包在 ```json fenced block 中），不要夹杂说明性 prose。

---

## 执行链路（固定顺序，不得跳步）

1. 读取 `{{OUTLINE_PATH}}` 中第 {{PAGE_NUM}} 页的定义（只关注你这一页）
2. 读取 `{{REQUIREMENTS_PATH}}` 掌握用户需求和边界约束
3. 读取 `{{BRIEF_PATH}}` 获取可用素材
4. 读取 `{{STYLE_PATH}}` 提取 `mood_keywords`、`variation_strategy`、`decoration_dna` 做情绪定调
5. 加载本地已有的外部**图片清单**：
   ```bash
   python3 {{SKILL_DIR}}/scripts/resource_loader.py images --images-dir {{IMAGES_DIR}}
   ```
6. 加载支持的**组件/图表菜单**说明（菜单层，只含标题+引用摘要）：
   ```bash
   python3 {{SKILL_DIR}}/scripts/resource_loader.py menu --refs-dir {{REFS_DIR}}
   ```
7. **按下方映射表做资源选择决策**，然后决定 `page_type`、`layout_hint`、`cards[].card_type`、`chart.chart_type`、`resource_ref`、`image.mode`、排版策略等。

### 数据类型 → 推荐资源映射（决策辅助）

根据本页的 `proof_type` 和实际数据类型，优先按以下映射选择资源：

| 本页数据特征 | 推荐 layout_hint | 推荐 `card_type` / `chart.chart_type` | 选择理由 |
|------------|-----------------|--------------------------------------|---------|
| 单一核心数字/KPI | `hero-top` / `single-focus` | `data_highlight` + `kpi` / `metric_row` | 大字突出，视觉锚点清晰 |
| 多项横向比较 | `symmetric` / `three-column` | `comparison` + `comparison_bar` | 左右对称利于对比 |
| 时间线/里程碑 | `l-shape` / `waterfall` | `timeline` + `timeline` | 自带时序叙事 |
| 步骤/流程 | `l-shape` / `t-shape` / `waterfall` | `process` / `diagram` + `funnel` / `progress_bar`（如有明确数据） | 顺序清晰，可带流程骨架 |
| 排行榜/Top-N | `asymmetric` / `l-shape` | `list` / `data_highlight` + `comparison_bar`（如需） | 层级视觉明确 |
| 图文并茂 | `primary-secondary` / `asymmetric` | `image_hero` / `text` / `data` | 图文互补，主次分明 |
| 大段引言/金句 | `single-focus` / `asymmetric` | `quote` | 聚焦单一信息 |
| 数据图表 | `primary-secondary` / `single-focus` | `data` + `sparkline` / `ring` / `radar` / `treemap` / `stacked_bar` / `waffle` | 图表主导，论据可视化 |
| 多卡片并列信息 | `mixed-grid` / `three-column` | `text` / `data` / `list` | 模块化呈现 |

**填写 `resources` 字段时必须说明选择理由**（推荐写入 `resources.resource_rationale`），例如："本页展示 3 个 KPI 指标对比，选择 hero-top + metric-row 强化主次层级"。
8. 将完整 planning 写入 `{{PLANNING_OUTPUT}}`。
9. 自审（必须执行，不得跳过）：
   ```bash
   python3 {{SKILL_DIR}}/scripts/planning_validator.py $(dirname {{PLANNING_OUTPUT}}) --refs {{REFS_DIR}} --page {{PAGE_NUM}}
   ```
10. 修复所有 ERROR（WARNING 建议修复）。
11. 完成信号规则：
   - **若本阶段由主 agent 直接下发（Codex 模式 4A）**：发送 `FINALIZE: planning 完成，产物路径 {{PLANNING_OUTPUT}}`
   - **若本阶段由 Page orchestrator 在同一 session 内渐进调度（Claude 模式）**：只输出 `--- STAGE 1 COMPLETE: {{PLANNING_OUTPUT}} ---`，然后按外层协议继续
12. 不要把当前阶段的完成信号误当作整页任务结束。

---

## 阶段边界

- 本阶段：只写 planning JSON，不写 HTML
- 下一阶段：按调度模式推进到 HTML 生成
- 消费规则：planning 阶段只读资源的 `> 引用层`（菜单），HTML 阶段才读正文层
