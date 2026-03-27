# Workflow Ops Appendix

本文件承载运行辅助信息，不参与主链判定。

主链真源始终是：

- `SKILL.md` 中的主状态机与合同
- `references/playbooks/` 下各步骤对应的 `*-subagent-playbook.md`
- 对应脚本的实际行为

## 1. 恢复原则

恢复依赖正式产物链，而不是依赖单一状态文件。

恢复前应按顺序检查：

1. `progress.json` 是否存在，且 `scripts/progress_validator.py` 校验通过
2. 前序产物是否存在
3. 前序产物是否字段完整、可被下一步消费
4. 若存在多层产物，是否彼此匹配

如果任一检查失败，回退到该产物所属步骤重新生成。

## 2. `progress.json` 参考结构

`progress.json` 是主流程必需运行账本：Step 1 开始前必须存在，且必须通过 `scripts/progress_validator.py --require-pre-step1`。
它不能替代正式产物链，只用于恢复与进度审计。

```json
{
  "version": "2.0",
  "topic": "PPT 主题",
  "complexity": "light | standard | large",
  "total_pages": 15,
  "started_at": "ISO 时间戳",
  "last_updated": "ISO 时间戳",
  "steps": {
    "step_1": {"status": "done | in_progress | pending"},
    "step_2": {"status": "done | in_progress | pending"},
    "step_3": {"status": "done | in_progress | pending"},
    "step_4": {"status": "done | in_progress | pending", "completed_pages": [1, 2], "current_page": 3},
    "step_5a": {"status": "done | in_progress | pending"},
    "step_5b": {"status": "done | in_progress | pending", "completed_pages": []},
    "step_5c": {"status": "done | in_progress | pending", "completed_pages": []},
    "step_5d": {"status": "done | in_progress | pending", "round": 0, "mode": null},
    "step_6": {"status": "done | in_progress | pending", "pipeline": null}
  }
}
```

## 3. 强制写入时机

| 事件 | 必须更新内容 |
|------|-------------|
| Step 1 完成 | topic / complexity / `step_1=done` |
| Step 2 完成 | `step_2=done` |
| Step 3 完成 | `step_3=done` |
| Step 4 每页落盘 | 追加 `completed_pages` |
| Step 5a 完成 | `step_5a=done` |
| Step 5b / 5c 每页完成 | 追加对应 `completed_pages` |
| Step 5d 每轮完成 | 记录 round / mode |
| Step 6 用户选择管线 | 记录 `pipeline` |
| Step 6 完成 | `step_6=done` |

## 4. 输出目录结构

```text
ppt-output/
  requirements.json
  raw-research.json
  research-package.json
  outline.json
  outline-review-round-{n}.json
  style.json
  runtime/
    research-prompt.txt
    material-prep-prompt.txt
    outline-prompt.txt
    outline-review-prompt.txt
    planning-prompt.txt
    style-prompt.txt
    image-prompt.txt
    html-page-{NN}-prompt.txt
  planning/
    planning{n}.json
  images/
  prompts-ready/
    prompt-ready-{n}.txt
  slides/
    slide-{NN}.html
  reviews/
    final-review-round-{n}.json
  preview.html
  png/
  svg/
  presentation.pptx
  progress.json
```

## 5. 主链依赖关系

```text
requirements.json
  -> raw-research.json
  -> research-package.json
  -> outline.json
  -> planning/*.json
  -> style.json
  -> runtime/*.txt
  -> prompts-ready/*.txt
  -> slides/*.html
  -> reviews/final-review-round-{n}.json
  -> preview.html
  -> presentation.pptx
```

## 6. 参考入口索引

只列主 agent 常用入口：

| 文件 | 用途 |
|------|------|
| `prompts/prompt-1-research.md` | Step 1 需求调研 |
| `prompts/prompt-2-outline.md` | Step 3 大纲生成 |
| `prompts/prompt-3-planning.md` | Step 4 逐页策划 |
| `prompts/prompt-4-design.md` | Step 5c HTML 模板源 |
| `playbooks/planning-subagent-playbook.md` | Step 4 执行细节 |
| `playbooks/html-subagent-playbook.md` | Step 5c 执行细节 |
| `playbooks/review-subagent-playbook.md` | Step 5d 执行细节 |
| `playbooks/outline-subagent-playbook.md` | Step 3 编写细节 |
| `playbooks/outline-review-subagent-playbook.md` | Step 3 审查细节 |
| `runtime/resource-menu.md` | Step 4 资源菜单 |
| `principles/design-principles-cheatsheet.md` | Step 4 设计原则速查 |
| `styles/README.md` | Step 5a 风格决策 |
| `runtime/image-generation.md` | Step 5b 配图合同 |
| `scripts/planning_validator.py` | Step 4 validator |
| `scripts/progress_validator.py` | Step 0 / 恢复 gate validator |
| `scripts/contract_validator.py` | Step 1/2/3 review result/5a/5b 合法性 validator |
| `scripts/subagent_prompt_assembler.py` | Step 2/3/4/5a/5b/5c runtime prompt 基座组装；主 agent 可附加必要运行上下文 |
| `scripts/prompt_assembler.py` | Step 5c 组装 `prompt-ready` |
| `scripts/final_review_harness.py` | Step 5d harness |
| `scripts/html_packager.py` | 生成 `preview.html` |
| `ops/resource-registry.md` | 维护时的资源总映射 |
