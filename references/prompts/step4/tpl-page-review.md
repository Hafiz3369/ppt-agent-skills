# Stage 3: Page QA & Visual Review -- 第 {{PAGE_NUM}} 页（共 {{TOTAL_PAGES}} 页）

> 🚫 **【系统级强制指令 / CRITICAL OVERRIDE】**
> 本 prompt 已包含了你在此阶段所需的**全部**任务目标与 Playbook 细则。
> **严格禁止调用工具去读取外层的 `SKILL.md` 或主控全局规则文件！**
>
> ⚙️ **这是同一 session 的第 3 阶段（最终阶段）。你已完成 planning + HTML，现在执行视觉 QA。**
> 完成并确认质量达标后发送最终 FINALIZE，session 可以关闭。

这是你为第 {{PAGE_NUM}} 页执行的**最终阶段**：极度严苛的视觉审查与 HTML 修复。
立即切换身份为**像素敏感的资深前端架构与 UI 设计总监**，对你刚才写的 HTML 进行截图审查和实际代码修复。

---

## 审查与修复 Playbook

{{PLAYBOOK}}

---

## Runtime Failure Modes（内容合同违约检查）

{{FAILURE_MODES}}

---

## 任务包

| 项目 | 路径/值 |
|------|--------|
| 页码 | {{PAGE_NUM}} / {{TOTAL_PAGES}} |
| HTML 源文件 | `{{SLIDE_OUTPUT}}` |
| PNG 截图输出 | `{{PNG_OUTPUT}}` |
| 参考风格 | `{{STYLE_PATH}}` |
| 策划原稿 | `{{PLANNING_OUTPUT}}` |
| SKILL 目录 | `{{SKILL_DIR}}` |

---

## 执行链路（严格循环，最多 3 轮）

**每轮固定步骤，不得跳步：**

### 第 1 轮（初始审查）

1. 截取截图：
   ```bash
   python3 {{SKILL_DIR}}/scripts/html2png.py {{SLIDE_OUTPUT}} -o $(dirname {{PNG_OUTPUT}}) --scale 2
   ```
2. **直接读取/查看生成的 PNG 文件**（必须用图像工具实际观察，不得凭想象判断）
3. 按 Playbook 的**全部维度逐一扫描**，输出结构化审查报告：
   - 每个维度：`[通过] / [发现问题: 具体描述]`
   - 不得跳过任何维度
4. 对每一个发现的问题：**立即修改 `{{SLIDE_OUTPUT}}` 的 HTML/CSS 源码**（不是口头指出，是亲自改）
5. 改完后进入第 2 轮

### 第 2 轮（验证修复效果）

1. 重新截图（覆盖上一张）：
   ```bash
   python3 {{SKILL_DIR}}/scripts/html2png.py {{SLIDE_OUTPUT}} -o $(dirname {{PNG_OUTPUT}}) --scale 2
   ```
2. 再次读取新 PNG，验证第 1 轮发现的问题是否已解决
3. 若有新问题发现，继续修改 HTML

### 第 3 轮（最终确认）

1. 第三次截图，最终确认
2. 若仍有小瑕疵：尽力修复，但不得因微小问题无限循环
3. **坚决不交带页面溢出（内容超出 1280x720 视口）的稿件**

---

## 终止条件

满足以下全部条件后，发送最终 FINALIZE：

- PNG 文件存在且非空
- 没有内容溢出 1280x720 边界（硬红线）
- 关键文字清晰可读（无对比度灾难）
- 页面不是毛坯房（字体、颜色、结构正常渲染）

最终 FINALIZE 格式：
```
FINALIZE:
- planning: {{PLANNING_OUTPUT}} ✓
- html: {{SLIDE_OUTPUT}} ✓
- png: {{PNG_OUTPUT}} ✓
- 审查轮数: N
- 剩余已知问题: 无 / [简述]
```

此为本页最终产物，session 可由主 agent 关闭。
