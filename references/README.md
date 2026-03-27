# References Index

本目录现在只保留“按职责分层后的 markdown 真源”。根目录不再堆放 playbook、runtime、design/runtime 规则和 ops 文档。

## 热路径

主控制台或被调用脚本会直接命中的第一层入口：

- `ops/workflow-ops.md`
- `ops/resource-registry.md`
- `runtime/resource-menu.md`
- `runtime/image-generation.md`
- `runtime/narrative-rhythm.md`
- `runtime/technique-cards.md`
- `prompts/prompt-1-research.md`
- `prompts/prompt-2-outline.md`
- `prompts/prompt-3-planning.md`
- `prompts/prompt-4-design.md`
- `playbooks/*.md`

理解仓库时，先读这些，不要从资源库细项开始。

## 1. Playbooks

sub-agent 执行细则真源：

- `playbooks/research-subagent-playbook.md`
- `playbooks/material-prep-subagent-playbook.md`
- `playbooks/outline-subagent-playbook.md`
- `playbooks/outline-review-subagent-playbook.md`
- `playbooks/planning-subagent-playbook.md`
- `playbooks/html-subagent-playbook.md`
- `playbooks/review-subagent-playbook.md`

## 2. Runtime

运行期共享合同和主链参考：

- `runtime/resource-menu.md`
- `runtime/image-generation.md`
- `runtime/narrative-rhythm.md`
- `runtime/technique-cards.md`

## 3. Design Runtime

设计/运行规则补充：

- `design-runtime/design-specs.md`
- `design-runtime/css-weapons.md`
- `design-runtime/director-command-rules.md`
- `design-runtime/director-command-examples.md`
- `design-runtime/data-type-visual-mapping.md`
- `design-runtime/data-type-decoration-mapping.md`

## 4. Ops

运行辅助与资源映射：

- `ops/workflow-ops.md`
- `ops/resource-registry.md`

## 5. Prompts

- `prompts/prompt-1-research.md`
- `prompts/prompt-2-outline.md`
- `prompts/prompt-3-planning.md`
- `prompts/prompt-4-design.md`
- `prompts/prompt-4-design-global.md`
- `prompts/prompt-4-design-compact.md`

## 6. Resource Libraries

- `layouts/`
- `blocks/`
- `charts/`
- `page-templates/`
- `styles/`
- `principles/`

这些目录是 `scripts/prompt_assembler.py`、`scripts/planning_validator.py`、`scripts/resource_registry.py` 的静态资源来源。它们数量多，但不是主链入口。

## 目录边界

不应再出现：

- `copy/` 里的 markdown 备份进入 runtime
- `scripts/` 下的 markdown 镜像副本目录（例如历史上的 scripts references 镜像目录）
- 与当前主链无关的历史 prompt 或过时 playbook 混回根目录

如果新增 markdown：

1. 先判断职责是 `playbooks / runtime / design-runtime / ops / prompts / resource library`
2. 根目录只保留 `README.md`
3. 入口文档放对应职责子目录，不再回到 `references/` 根目录
4. 不要再复制一份到 `scripts/` 或 `copy/`

## 当前阅读顺序建议

1. `SKILL.md`
2. `references/README.md`
3. `scripts/README.md`
4. `references/ops/` 与 `references/playbooks/`
5. `references/runtime/` 与 `references/prompts/`
6. 最后才是 `layouts/`、`blocks/`、`charts/`、`styles/`、`principles/`
