# Stage 2: Page HTML Production -- 第 {{PAGE_NUM}} 页（共 {{TOTAL_PAGES}} 页）

> 🚫 **【系统级强制指令 / CRITICAL OVERRIDE】**
> 本 prompt 已包含了你在此阶段所需的**全部**任务目标与 Playbook 细则。
> **严格禁止调用工具去读取外层的 `SKILL.md` 或主控全局规则文件！**
>
> ⚙️ **这是同一 session 的第 2 阶段。你在上一阶段已完成 planning JSON，现在执行 HTML 生成。**
> 完成 HTML 后发送 FINALIZE，然后**继续等待**——主 agent 会发送第 3 阶段（Review）指令。

这是你为第 {{PAGE_NUM}} 页执行的**第二阶段核心任务**：HTML 设计稿生成。
你的策划稿（`{{PLANNING_OUTPUT}}`）是本阶段的主要输入，严格忠实还原其骨架。

---

## Playbook（执行细则）

{{PLAYBOOK}}

---

## 任务包

| 项目 | 路径/值 |
|------|--------|
| 页码 | {{PAGE_NUM}} / {{TOTAL_PAGES}} |
| 策划稿 | `{{PLANNING_OUTPUT}}` |
| 风格规范 | `{{STYLE_PATH}}` |
| 输出 HTML | `{{SLIDE_OUTPUT}}` |
| SKILL 目录 | `{{SKILL_DIR}}` |
| 资源目录 | `{{REFS_DIR}}` |
| 图片素材目录 | `{{IMAGES_DIR}}` |

---

## 执行链路（固定顺序，不得跳步）

1. 读取 `{{PLANNING_OUTPUT}}`，提取完整骨架（layout_hint、cards、image.mode、handoff_to_design.non_negotiables 等）
2. 读取 `{{STYLE_PATH}}`，提取 `css_variables`、`font_family`、`design_soul`、`variation_strategy`、`decoration_dna`
3. **必须执行** —— 获取 planning 引用资源的**正文层实现细节**（不能跳过，里面有组件级 CSS 参数和骨架建议）：
   ```bash
   python3 {{SKILL_DIR}}/scripts/resource_loader.py resolve --refs-dir {{REFS_DIR}} --planning {{PLANNING_OUTPUT}}
   ```
   输出的实现细节必须真正落实到 HTML/CSS 结构中，不得忽略。
4. 核对图片素材，确认 `image.source_hint` 路径可访问：
   ```bash
   python3 {{SKILL_DIR}}/scripts/resource_loader.py images --images-dir {{IMAGES_DIR}}
   ```
5. 按以下**画布物理红线**生成自包含 HTML（不可违反）：
   - `body { width: 1280px; height: 720px; overflow: hidden; }` —— 不得写 100% 或其他尺寸
   - 禁止 `transform: scale()` 缩放 hack
   - 所有 CSS 内联在 `<style>` 标签中，禁止引用外部 CSS 文件
   - 字体从 `style.json` 的 `font_family` 取值，通过 Google Fonts 或系统字体栈引入
6. 按 `image.mode` 处理图片：
   - `generate` / `provided`：将 `source_hint` 路径绑定到 `src` 或 `background`
   - `manual_slot`：渲染明确可替换的图片占位区，不得删除
   - `decorate`：使用内联 SVG、色块、渐变、字体装饰替代，不得留空白大洞
7. 将完整 HTML 写入 `{{SLIDE_OUTPUT}}`
8. 发送 FINALIZE 信号，格式：`FINALIZE: HTML 完成，产物路径 {{SLIDE_OUTPUT}}`
9. **等待主 agent 发送下一阶段（图审 Review）指令，不要自行结束 session。**

---

## 阶段边界

- 本阶段：只写 HTML，不截图，不做 QA
- 下一阶段：等待主 agent 发来 Review 指令后执行截图和图审
- 资源消费规则：本阶段读资源**正文层**（步骤 3），而非 planning 阶段用过的菜单摘要层
