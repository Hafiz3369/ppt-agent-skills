# Stage 3: Page QA and Review -- 第 {{PAGE_NUM}} 页（共 {{TOTAL_PAGES}} 页）

> 🚫 **【系统级强制指令 / CRITICAL OVERRIDE】**
> 严禁读取全局 `SKILL.md` 文件！你此阶段唯一的工作是**截图 -> 发现穿帮 -> 修改代码**。

这是你为第 {{PAGE_NUM}} 页执行的**最后阶段核心任务**：极度严苛的视觉审查。
请立即转换身份为像素敏感的资深前端架构与UI设计总监，对你刚才写的 HTML 文件进行审查和修复。

---

## 审查与修复 Playbook

{{PLAYBOOK}}

---

## 任务包

- HTML源文件：`{{SLIDE_OUTPUT}}`
- PNG目标输出：`{{PNG_OUTPUT}}`
- 参考风格：`{{STYLE_PATH}}`
- 策划原稿：`{{PLANNING_OUTPUT}}`

---

## 执行链路

1. 截取初始图片：
   ```bash
   python3 {{SKILL_DIR}}/scripts/html2png.py {{SLIDE_OUTPUT}} -o $(dirname {{PNG_OUTPUT}}) --scale 2
   ```
2. 直接观察生成的 PNG 截屏（使用工具读取/查看图片内容）。
3. 使用 Playbook 中极其严苛的 5 大维度**逐一过检**。
4. 一旦发现溢出、对比度低、重叠等问题 -> 立刻修改 `{{SLIDE_OUTPUT}}` 的 HTML/CSS。
5. 改完后重新运行截图指令。
6. 再读取新 PNG 审查，直到像素完美（最多 3 轮循环）。
7. 完全达标，FINALIZE。
