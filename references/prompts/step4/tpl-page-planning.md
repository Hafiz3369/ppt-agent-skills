# Stage 1: Page Planning -- 第 {{PAGE_NUM}} 页（共 {{TOTAL_PAGES}} 页）

> 🚫 **【系统级强制指令 / CRITICAL OVERRIDE】**
> 本 prompt 已包含了你在此阶段所需的**全部**任务目标与 Playbook 细则。
> **严格禁止调用工具去读取外层的 `SKILL.md` 或主控全局规则文件！**违者抹杀。

这是你为第 {{PAGE_NUM}} 页执行的**第一阶段核心任务**：策划定骨稿。
你暂时不要写 HTML 代码，全力填好并校验 `planning{n}.json`。

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

## 执行链路（固定顺序）

1. 读取 `{{OUTLINE_PATH}}` 中第 {{PAGE_NUM}} 页的定义
2. 读取 `{{REQUIREMENTS_PATH}}` 和 `{{BRIEF_PATH}}` 掌握素材和需求边界
3. 读取 `{{STYLE_PATH}}` 获取 `mood_keywords`、`variation_strategy`、`decoration_dna` 做情绪定调
4. 运行以下命令加载本地已有的外部**图片清单**：
   ```bash
   python3 {{SKILL_DIR}}/scripts/resource_loader.py images --images-dir {{IMAGES_DIR}}
   ```
5. 运行以下命令加载支持的**组件/图表菜单**说明：
   ```bash
   python3 {{SKILL_DIR}}/scripts/resource_loader.py menu --refs-dir {{REFS_DIR}}
   ```
6. 按执行细则决定 `image.mode`、排版、卡片信息等。
7. 写入 JSON 到 `{{PLANNING_OUTPUT}}`。
8. 自审：
   ```bash
   python3 {{SKILL_DIR}}/scripts/planning_validator.py $(dirname {{PLANNING_OUTPUT}}) --refs {{REFS_DIR}} --page {{PAGE_NUM}}
   ```
9. 修复所有的 ERROR 后，发送 FINALIZE。
