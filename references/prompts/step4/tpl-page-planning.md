# Stage 1: Page Planning -- 第 {{PAGE_NUM}} 页（共 {{TOTAL_PAGES}} 页）

> 🚫 **【系统级强制指令 / CRITICAL OVERRIDE】**
> 本 prompt 已包含了你在此阶段所需的**全部**任务目标与 Playbook 细则。
> **严格禁止调用工具去读取外层的 `SKILL.md` 或主控全局规则文件！**
>
> ⚙️ **本 session 将执行三阶段任务（Planning → HTML → Review），你现在执行第 1 阶段。**
> 完成 Planning 后发送 FINALIZE，然后**保持等待**——主 agent 会发送下一阶段的指令，不要自行退出。

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
7. 按 Playbook 细则决定 `image.mode`、`layout_hint`、`card_type`、排版策略等。
8. 将完整 planning 写入 `{{PLANNING_OUTPUT}}`。
9. 自审（必须执行，不得跳过）：
   ```bash
   python3 {{SKILL_DIR}}/scripts/planning_validator.py $(dirname {{PLANNING_OUTPUT}}) --refs {{REFS_DIR}} --page {{PAGE_NUM}}
   ```
10. 修复所有 ERROR（WARNING 建议修复）。
11. 发送 FINALIZE 信号，格式：`FINALIZE: planning 完成，产物路径 {{PLANNING_OUTPUT}}`
12. **等待主 agent 发送下一阶段（HTML 生成）指令，不要自行结束 session。**

---

## 阶段边界

- 本阶段：只写 planning JSON，不写 HTML
- 下一阶段：等待主 agent 发来 HTML 生成指令后执行
- 消费规则：planning 阶段只读资源的 `> 引用层`（菜单），HTML 阶段才读正文层
