# Structured UI Mode -- CLI 原生结构化采访

## 核心指令

如果当前 CLI 具备结构化向用户提问的原生能力，就必须使用它。

能力判断看是否支持一组 `question/header/id/options` 风格的对象，而不是看固定工具名。

常见形态包括：

- `AskUserQuestion(...)`
- `request_user_input(...)`
- `ask_user_question(...)`
- `ui.form(...)`

## 执行方式

- 优先把高信号字段做成单选或有限选项
- 问题过多时，拆成 2 轮
- 保持稳定 `id`
- 若支持推荐项，把推荐项放第一个

## 可识别对象骨架

```text
questions: [
  {
    header: "...",
    id: "...",
    question: "...",
    options: [
      { label: "...", description: "..." }
    ]
  }
]
```

## 禁止项

- 不要明明支持结构化 UI，还退化成大段文本提问
- 不要把工具名字当白名单，按能力识别即可
