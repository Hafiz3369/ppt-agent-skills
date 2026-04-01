# Stage 1: Page Planning -- 第 {{PAGE_NUM}} 页（共 {{TOTAL_PAGES}} 页）

> **【系统级强制指令 / CRITICAL OVERRIDE】**
> 本 prompt 已包含了你在此阶段所需的**全部**任务目标与 Playbook 细则。
> **严格禁止调用工具去读取外层的 `SKILL.md` 或主控全局规则文件！**
>
> 本阶段的唯一目标：产出 `{{PLANNING_OUTPUT}}`。完成后发送 FINALIZE 信号。
> 后续阶段的推进方式取决于调度模式（Codex session-resume / Claude 自主渐进），你不需要关心。

这是你为第 {{PAGE_NUM}} 页执行的**第一阶段核心任务**：策划定骨稿。
你暂时不要写 HTML 代码，全力填好并校验 `{{PLANNING_OUTPUT}}`。

---

## Playbook（执行细则）

{{PLAYBOOK}}

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
7. **按下方映射表做资源选择决策**，然后决定 `image.mode`、`layout_hint`、`card_type`、排版策略等。

### 数据类型 → 推荐资源映射（决策辅助）

根据本页的 `proof_type` 和实际数据类型，优先按以下映射选择资源：

| 本页数据特征 | 推荐 layout_hint | 推荐 card_type / chart_type | 选择理由 |
|------------|-----------------|---------------------------|---------|
| 单一核心数字/KPI | hero / split-left | kpi、metric-row | 大字突出，视觉冲击 |
| 多项横向比较 | bento-grid / columns | comparison、comparison-bar | 左右对称利于对比 |
| 时间线/里程碑 | timeline-flow | timeline | 自带时序叙事 |
| 步骤/流程 | steps-horizontal / steps-vertical | process | 顺序清晰 |
| 排行榜/Top-N | list-ranked | data_highlight、list | 层级视觉 |
| 图文并茂 | split-left / split-right | image + text | 图文互补 |
| 大段引言/金句 | centered-statement | quote | 聚焦单一信息 |
| 数据图表 | chart-focus | bar、line、pie、ring | 图表主导 |
| 多卡片并列信息 | bento-grid | feature-card、info-card | 模块化呈现 |

**填写 `resources` 字段时必须说明选择理由**（`resource_rationale` 字段），例如："本页展示 3 个 KPI 指标对比，选择 bento-grid + metric-row 实现模块化数据呈现"。
8. 将完整 planning 写入 `{{PLANNING_OUTPUT}}`。
9. 自审（必须执行，不得跳过）：
   ```bash
   python3 {{SKILL_DIR}}/scripts/planning_validator.py $(dirname {{PLANNING_OUTPUT}}) --refs {{REFS_DIR}} --page {{PAGE_NUM}}
   ```
10. 修复所有 ERROR（WARNING 建议修复）。
11. 发送 FINALIZE 信号，格式：`FINALIZE: planning 完成，产物路径 {{PLANNING_OUTPUT}}`
12. 发送 FINALIZE 信号后，按调度模式的指示推进（Codex 模式等待主 agent 续写；Claude 渐进模式自主读取下一阶段 prompt）。

---

## 阶段边界

- 本阶段：只写 planning JSON，不写 HTML
- 下一阶段：按调度模式推进到 HTML 生成
- 消费规则：planning 阶段只读资源的 `> 引用层`（菜单），HTML 阶段才读正文层
