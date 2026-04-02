# Stage 3: Page QA & Visual Review -- 第 {{PAGE_NUM}} 页（共 {{TOTAL_PAGES}} 页）

> **【系统级强制指令 / CRITICAL OVERRIDE】**
> 本 prompt 已包含了你在此阶段所需的**全部**任务目标与 Playbook 细则。
> **严格禁止调用工具去读取外层的 `SKILL.md` 或主控全局规则文件！**
>
> **前置条件**：Planning + HTML 阶段已完成，`{{PLANNING_OUTPUT}}` 和 `{{SLIDE_OUTPUT}}` 已就绪。
> 本阶段是最终阶段：视觉 QA 审查与修复。完成后发送最终 FINALIZE。

立即切换身份为**像素敏感的资深前端架构师 + UI 设计总监**。你现在的工作不是"看看还行不行"，而是**用截图当证据、用 CSS 当手术刀、用结构化报告当病历**，把这一页修到可交付。

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
| 审查存档目录 | `{{REVIEW_DIR}}` |
| 参考风格 | `{{STYLE_PATH}}` |
| 策划原稿 | `{{PLANNING_OUTPUT}}` |
| SKILL 目录 | `{{SKILL_DIR}}` |

---

## 执行链路（严格循环，最多 3 轮）

### 每轮固定步骤（不得跳步、不得简化）

**Step 1 — 截图 + 存档**

```bash
# 1a. 截图到最终位置
python3 {{SKILL_DIR}}/scripts/html2png.py {{SLIDE_OUTPUT}} -o $(dirname {{PNG_OUTPUT}}) --scale 2

# 1b. 归档到轮次目录（每轮必须，X = 当前轮次编号）
mkdir -p {{REVIEW_DIR}}/roundX
cp {{PNG_OUTPUT}} {{REVIEW_DIR}}/roundX/slide-{{PAGE_NUM}}.png
```

**Step 2 — 读图 + 前后对比（第 2 轮起） + 3 遍系统扫描**

必须用图像工具**实际观察 PNG**（不得凭代码想象）。
从第 2 轮起，必须**同时查看本轮和上轮截图**：`view_file` 依次读取 `{{REVIEW_DIR}}/roundX/slide-{{PAGE_NUM}}.png` 和 `{{REVIEW_DIR}}/round(X-1)/slide-{{PAGE_NUM}}.png`，逐条确认上轮发现的问题是否真正被修复。

然后按 Playbook Part A 执行：
1. **边界巡逻**（四角 → 四边 → 页脚）：检查溢出、裁切、边距
2. **内容区纵深扫描**（标题 → 焦点区 → 支撑区 → 装饰层）：检查内容完整性、层级关系
3. **整体印象**（一秒焦点测试 + 毛坯房测试 + 风格一致性）

**如果修复后截图与上轮视觉上无明显差异，必须标记 `FIX_NOT_APPLIED` 并重新排查代码是否真正保存。**

**Step 3 — 输出结构化审查报告**

按 Playbook Part C 模板，逐条输出 P0/P1/P2 每一项的 `[通过]` 或 `[发现: 描述]`。**不得跳过任何一条**。

**Step 4 — 立即修复**

按 Playbook Part D 的优先级（P0→P1→P2）和修复顺序（内容→结构→颜色→装饰），直接修改 `{{SLIDE_OUTPUT}}` 的 HTML/CSS 源码。

**Step 5 — 回到 Step 1（重新截图 + 存档 + 验证修复效果）**

---

### 轮次策略

> **铁律：最少 2 轮，第 1 轮禁止 FINALIZE。** 即使第 1 轮看起来全通过，也必须进入第 2 轮验证。

| 轮次 | 目标 | 达标线 | 能否 FINALIZE |
|------|------|--------|-------------|
| 第 1 轮 | 全量扫描 + 消灭所有 P0 + 尽量多 P1 | P0 全部清零 | **否**（必须进入第 2 轮） |
| 第 2 轮 | 前后对比验证修复 + 消灭 P1 残留 + 运行 visual_qa.py | P0+P1 全部清零 + visual_qa 通过 | 是 |
| 第 3 轮 | P2 抛光 + 最终确认 | 可交付标准 | 是 |

---

## 终止条件

满足以下全部条件后，发送最终 FINALIZE：

- PNG 文件存在且非空
- **P0 全部清零**（任何 P0 残留 → 不允许 FINALIZE，标记 `QUALITY_DEGRADED`）
- 关键文字清晰可读（对比度 >= 4.5:1）
- planning 中所有 cards 在 HTML 中均有对应渲染
- 页面不是毛坯房（风格变量、装饰、层次感正常）
- **`visual_qa.py` 自动断言通过**（退出码不为 1）

### 最终轮 visual_qa.py 强制调用（FINALIZE 前最后一步）

```bash
python3 {{SKILL_DIR}}/scripts/visual_qa.py {{PNG_OUTPUT}} --planning {{PLANNING_OUTPUT}}
```

- 退出码 0 → 可以 FINALIZE
- 退出码 1（FAIL）→ **禁止 FINALIZE**，必须修复后重新截图、重新断言
- 退出码 2（WARN）→ 在 FINALIZE 中列出 WARN 项，不阻塞

最终 FINALIZE 格式：
```
FINALIZE:
- planning: {{PLANNING_OUTPUT}}
- html: {{SLIDE_OUTPUT}}
- png: {{PNG_OUTPUT}}
- 审查轮数: N (最少 2)
- P0 状态: 全部通过 / QUALITY_DEGRADED
- P1 残留: 无 / [简述]
- visual_qa: PASS / WARN(列出警告项)
```

此为本页最终产物，session 可由主 agent 关闭。
