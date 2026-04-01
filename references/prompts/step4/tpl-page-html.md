# Stage 2: Page HTML Production -- 第 {{PAGE_NUM}} 页（共 {{TOTAL_PAGES}} 页）

> 🚫 **【系统级强制指令 / CRITICAL OVERRIDE】**
> 本 prompt 已包含了你在此阶段所需的**全部**任务目标与 Playbook 细则。
> **严格禁止调用工具去读取外层的 `SKILL.md` 或主控全局规则文件！**违者抹杀。

这是你为第 {{PAGE_NUM}} 页执行的**第二阶段核心任务**：HTML 生成。
你现在需要回忆并读取你刚才在上一阶段写好的策划稿（JSON），将其转化为高设计感的单页自包含 HTML。

---

## Playbook（执行细则）

{{PLAYBOOK}}

---

## 任务包

| 项目 | 路径/值 |
|------|--------|
| 返回的策划稿 | `{{PLANNING_OUTPUT}}` |
| 页面风格规范 | `{{STYLE_PATH}}` |
| 输出HTML | `{{SLIDE_OUTPUT}}` |
| SKILL 目录 | `{{SKILL_DIR}}` |
| 资源目录 | `{{REFS_DIR}}` |
| 图片素材目录 | `{{IMAGES_DIR}}` |

---

## 执行链路

1. 读取 `{{PLANNING_OUTPUT}}` 提取骨架和文案，读取 `{{STYLE_PATH}}` 获取字体和色值。
2. 运行脚本获取 planning 中引用的模块**正文代码实现**（这非常重要，里面有实现细节！）：
   ```bash
   python3 {{SKILL_DIR}}/scripts/resource_loader.py resolve --refs-dir {{REFS_DIR}} --planning {{PLANNING_OUTPUT}}
   ```
3. 检查是否有图片素材引用：
   ```bash
   python3 {{SKILL_DIR}}/scripts/resource_loader.py images --images-dir {{IMAGES_DIR}}
   ```
4. 严格按照 1280x720 的红线生成不可变尺寸的自包含 HTML，写入 `{{SLIDE_OUTPUT}}`。
5. 确保在本地浏览器打开不溢出后，发送 FINALIZE。
