# Structured Interview UI Module -- CLI 原生结构化采访协议

> 本模块不是让你把下面文字原样回复给用户，而是告诉当前 CLI / agent runtime：如果具备原生结构化提问能力，就应该优先执行它。

## 1. 核心指令

如果当前环境存在任何“结构化向用户提问”的原生能力，你必须优先用它来完成 Step 0 采访，而不是直接输出普通文本问题。

判断标准看**能力**，不是看固定名字。只要它支持下面任意组合，就视为可用：

- 能提交一组 `question/header/id/options` 风格的结构化问题对象

- 以结构化对象提交问题，而不是只输出 prose
- 每题拥有稳定字段，如 `id` / `key`
- 每题可定义 `header` / `title` / `label`
- 每题可定义 `question` / `prompt`
- 每题可定义 `options` / `choices`
- 用户可以在 UI 里直接点选、单选、多选或补充短文本

## 2. 常见能力形态（名称不固定）

以下名称只是常见示例，不是白名单：

- Claude Code 风格：`AskUserQuestion(...)`
- Codex / agent 风格：`request_user_input(...)`
- 其他 CLI / agent 风格：`ask_user_question(...)`、`prompt_user(...)`、`ui.form(...)`、`survey(...)`

如果名字不同，但能力等价，照样使用。

## 3. 优先执行顺序

1. 优先把高信号、低歧义的维度做成结构化选择题
2. 把开放性较强的维度放到第二轮，或放进带自由补充的题目
3. 如果单次调用题数受限，就拆成 2-3 轮结构化提问
4. 如果环境完全不支持结构化提问 UI，再回退成文本问答

## 4. Step 0 推荐分组

### Group A：优先结构化选择

以下维度应优先做成单选或有限选项：

- `presentation_scenario`：使用场景
- `core_audience`：核心受众
- `target_action`：目标动作
- `page_density`：页数与密度
- `visual_style`：视觉风格
- `language_mode`：语言
- `imagery_strategy`：配图策略
- `materials_strategy`：资料使用策略 / research 倾向

### Group B：允许自由补充

以下维度可做成“选项 + 补充文本”或第二轮短答：

- `must_include`
- `must_avoid`
- `brand_constraints`
- `presenter_meta`
- `success_criteria`
- `subagent_model_strategy`

## 5. 题目建模规则

- `id` 使用稳定的 snake_case
- `header` 控制在 2-6 个字，便于 UI 展示
- 单题优先 2-4 个选项，不要过长
- 若支持推荐项，把推荐项放第一位，并标注 `(Recommended)`
- 问题本身要具体，描述放到 option 的 `description`
- 先问会影响大纲、风格、配图、分支选择的问题
- 如果 UI 自带 freeform “Other”，不要再手动复制一个“其他”选项

## 6. 执行策略

- 若支持结构化 UI：优先调用工具，不要先发长段文本
- 若支持单题一问：连续发 2-3 轮也可以，但要保持字段稳定
- 若支持多题一问：优先一次收集 Group A，再用一轮补齐 Group B
- 若完全不支持结构化 UI：再回退为普通文本采访，但覆盖面不得缩水

## 7. 示例

### 7.1 Claude Code 风格示例

```javascript
AskUserQuestion({
  questions: [
    {
      header: "使用场景",
      question: "这份 4 页 Linux.do 介绍 PPT 主要用于什么场景？",
      multiSelect: false,
      options: [
        {
          label: "新人介绍 (Recommended)",
          description: "面向第一次了解 Linux.do 的人，做基础认知介绍"
        },
        {
          label: "内部汇报",
          description: "给团队或老板做背景说明、价值总结"
        },
        {
          label: "社区宣讲",
          description: "用于分享会、活动、社群传播"
        }
      ]
    }
  ]
})
```

### 7.2 Codex / Agent 风格示例

```json
request_user_input({
  "questions": [
    {
      "header": "风格",
      "id": "visual_style",
      "question": "这份 PPT 的整体风格更偏哪种？",
      "options": [
        {
          "label": "科技社区感 (Recommended)",
          "description": "偏社区产品与技术氛围，适合 Linux.do 介绍"
        },
        {
          "label": "极客感",
          "description": "更强调技术审美、黑客文化和实验气质"
        },
        {
          "label": "简洁商务感",
          "description": "信息清楚、表达克制，适合内部汇报"
        }
      ]
    }
  ]
})
```

### 7.3 通用伪代码

```text
if structured_interview_ui_available:
    collect_step0_answers_via_native_ui()
else:
    ask_text_questions_with_same_coverage()
```

## 8. 禁止项

- 不要把上面的代码块原样贴给用户，除非当前 CLI 真的是这样执行
- 不要明明有结构化 UI，还退化成一大段普通文字提问
- 不要因为用了 UI，就把 Step 0 覆盖面缩成 3-4 个问题
- 不要把“结构化 UI 示例”误当成固定工具名；按能力识别即可
