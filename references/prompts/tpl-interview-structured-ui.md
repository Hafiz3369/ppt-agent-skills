# 采访问卷（Structured UI）

主题：{{TOPIC}}
用户背景：{{USER_CONTEXT}}

---

## 当前执行模式

当前环境已确认支持原生结构化采访 UI。你必须优先使用 CLI 自带的结构化提问能力，而不是直接输出长段普通文本问题。

{{INTERVIEW_MODE_MODULE}}

---

## 共享采访核心

{{INTERVIEW_CORE}}

---

## 最终要求

- 优先一次收集高信号维度；若题数受限，可拆成 2 轮
- 优先把 `presentation_scenario`、`core_audience`、`target_action`、`page_density`、`visual_style`、`language_mode`、`imagery_strategy`、`materials_strategy` 做成结构化选择
- 开放项放到第二轮或通过 freeform 补充
- 收集完成后，主 agent 再写 `interview-qa.txt` 与 `requirements-interview.txt`
