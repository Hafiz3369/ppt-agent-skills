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
   **resolve 输出的 HTML 结构骨架、CSS 类名、参数规范是强制执行的实现合同，不是参考建议。** 你可以在细节上微调（间距±5px、圆角±2px），但结构、类名、数据格式不得自行发明替代方案。如果 resolve 返回了某个组件的 HTML 骨架，你的最终 HTML 必须包含该骨架的核心结构。
4. 核对图片素材，确认 `image.source_hint` 路径可访问：
   ```bash
   python3 {{SKILL_DIR}}/scripts/resource_loader.py images --images-dir {{IMAGES_DIR}}
   ```
5. **执行摘要（必须先写再动手）**——用 3 句话总结本页的核心策略，输出到对话中后再开始写 HTML：
   - 第 1 句：本页的核心论点和视觉焦点是什么
   - 第 2 句：使用什么布局结构和主要组件
   - 第 3 句：风格锚点（design_soul 如何体现在这一页）
6. 按以下**画布物理红线**生成自包含 HTML（不可违反）：
   - `body { width: 1280px; height: 720px; overflow: hidden; }` —— 不得写 100% 或其他尺寸
   - 禁止 `transform: scale()` 缩放 hack
   - 所有 CSS 内联在 `<style>` 标签中，禁止引用外部 CSS 文件
   - 字体从 `style.json` 的 `font_family` 取值，通过 Google Fonts 或系统字体栈引入
6. 按 `image.mode` 处理图片（**mode 在 planning 阶段已锁定，此处不得临时变更**）：
   - `generate` / `provided`（`image.needed=true`）：将 `source_hint` 路径绑定到 `<img src>` 或 `background-image`，图片必须实际渲染
   - `manual_slot`（`image.needed=false`）：渲染明确可替换的图片占位区（带边框/提示文字），不得偷偷删除占位区
   - `decorate`（`image.needed=false`）：不使用外部图片，用内联 SVG、色块、渐变、字体装饰补足视觉氛围，不得留空白大洞
7. **720px 高度内的视觉节奏**（设计要求，非可选建议）：
   - 标题区（y=20~70）：大字+强对比度，一眼抓住主题
   - 焦点区（y=70~450）：承载 primary 卡片，视觉权重最大
   - 支撑区（y=450~640）：secondary 卡片或补充数据，字号缩小、对比度降低
   - 装饰层：signature_move 锚点 + 渐变/几何点缀，不占用内容空间
   - **禁止平铺直叙**：不得让所有卡片等大小、等间距、等字号排列，必须有主次层级
8. 将完整 HTML 写入 `{{SLIDE_OUTPUT}}`
9. 发送 FINALIZE 信号，格式：`FINALIZE: HTML 完成，产物路径 {{SLIDE_OUTPUT}}`
10. **等待主 agent 发送下一阶段（图审 Review）指令，不要自行结束 session。**

---

## 阶段边界

- 本阶段：只写 HTML，不截图，不做 QA
- 下一阶段：等待主 agent 发来 Review 指令后执行截图和图审
- 资源消费规则：本阶段读资源**正文层**（步骤 3），而非 planning 阶段用过的菜单摘要层
