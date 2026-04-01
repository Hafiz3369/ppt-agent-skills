# References Index

本目录包含 PPT 工作流的资源真源。主控制台通过 `prompt_harness.py` 定向注入 playbook / runtime 规则；页面阶段再由 `resource_loader.py` 动态加载版式、组件与图表正文。

## 目录结构

```
references/
  playbooks/          -- subagent 执行细则（5 个 + step4/ 下 3 个）
  prompts/            -- prompt 模板（6 个 tpl-*.md + step4/ 下 3 个）
  layouts/            -- 版式资源（10 种）
  blocks/             -- 区域展示组件（8 种 + card-styles）
  charts/             -- 图表组件（13 种 + runtime-chart-rules）
  styles/             -- 风格主题（8 种 + runtime-style-rules + runtime-style-palette-index）
  principles/         -- 设计原则（7 种 + runtime-failure-modes）
  page-templates/     -- 页面结构模板（cover/toc/section/end）
  design-runtime/     -- 数据类型映射 + 设计规格 + CSS 武器库
```

## 核心入口

先读这些，再看资源库细项：

1. `SKILL.md` -- 主控制台合同：状态机、统一调度骨架、Gate、恢复规则
2. `playbooks/research-synth-playbook.md` -- Step 2A 搜集整理执行细则
3. `playbooks/source-synth-playbook.md` -- Step 2B 本地资料整合执行细则
4. `playbooks/outline-subagent-playbook.md` -- Step 3 大纲 + 自审执行细则
5. `playbooks/style-subagent-playbook.md` -- Step 3.5 全局风格合同执行细则
6. `playbooks/page-agent-playbook.md` -- Step 4 单页全链路执行细则（总览）
7. `playbooks/step4/page-planning-playbook.md` -- Step 4A 页面规划执行细则
8. `playbooks/step4/page-html-playbook.md` -- Step 4B HTML 落地执行细则
9. `playbooks/step4/page-review-playbook.md` -- Step 4C 图审修复执行细则
10. `styles/runtime-style-rules.md` -- Step 3.5 runtime 风格字段合同
11. `styles/runtime-style-palette-index.md` -- Step 3.5 预置风格基底入口

## Prompt 模板

`tpl-*.md` 文件由 `scripts/prompt_harness.py` 填充 `{{VAR}}` 变量后发给 subagent：

| 模板 | 阶段 | 变量 |
|------|------|------|
| `tpl-interview.md` | Step 0 采访 | TOPIC, USER_CONTEXT |
| `tpl-research-synth.md` | Step 2A 搜集 | TOPIC, REQUIREMENTS_PATH, SEARCH_OUTPUT, BRIEF_OUTPUT, TOOLS_AVAILABLE, MAX_SEARCH_ROUNDS, TARGET_PAGES |
| `tpl-source-synth.md` | Step 2B 资料整合 | REQUIREMENTS_PATH, SOURCE_INPUT, BRIEF_OUTPUT |
| `tpl-outline.md` | Step 3 大纲 | REQUIREMENTS_PATH, BRIEF_PATH, OUTLINE_OUTPUT |
| `tpl-style.md` | Step 3.5 风格 | REQUIREMENTS_PATH, OUTLINE_PATH, SKILL_DIR, STYLE_OUTPUT |
| `tpl-page-agent.md` | ~~Step 4 单页~~ **DEPRECATED** | 已被 step4/ 下三阶段模板取代 |
| `step4/tpl-page-planning.md` | Step 4A 页面规划 | PAGE_NUM, TOTAL_PAGES, REQUIREMENTS_PATH, OUTLINE_PATH, BRIEF_PATH, STYLE_PATH, IMAGES_DIR, PLANNING_OUTPUT, SKILL_DIR, REFS_DIR |
| `step4/tpl-page-html.md` | Step 4B HTML 落地 | PAGE_NUM, TOTAL_PAGES, PLANNING_OUTPUT, SLIDE_OUTPUT, IMAGES_DIR, STYLE_PATH, SKILL_DIR, REFS_DIR |
| `step4/tpl-page-review.md` | Step 4C 图审修复 | PAGE_NUM, TOTAL_PAGES, PLANNING_OUTPUT, SLIDE_OUTPUT, PNG_OUTPUT, STYLE_PATH, SKILL_DIR |

## 资源库

`scripts/resource_loader.py` 管理 7 个运行期资源目录：

- **menu 模式**：提取所有 `# 标题` + `> 引用`（多行 blockquote）-> planning 阶段消费
- **resolve 模式**：按 planning JSON 字段路由加载对应资源正文 -> html 阶段消费

字段路由表：

| planning 字段 | 资源目录 |
|---------------|---------|
| `layout_hint` | `layouts/` |
| `card_type` | `blocks/` |
| `chart_type` | `charts/` |
| `page_type` | `page-templates/` |
| `resources.*_refs` | 对应目录 |

## Design Runtime

数据到视觉的桥梁文件：

| 文件 | 用途 |
|------|------|
| `data-type-visual-mapping.md` | 数据类型 -> card_type + layout + CSS 实现参考 |
| `data-type-decoration-mapping.md` | 数据类型 -> 装饰技法(T) + 武器(W) + 密度 |
| `design-specs.md` | 画布规范、排版阶梯、卡片规则 |
| `css-weapons.md` | CSS 高级武器库 W1-W12 |
| `director-command-rules.md` | director_command 运行规则 |
| `director-command-examples.md` | 10 种页面类型示例库 |

## Style Runtime

风格目录同时包含两类材料：

- 预置风格参考：`blue-white.md`、`dark-tech.md` 等 8 个风格文件
- runtime 风格合同：`runtime-style-rules.md` 与 `runtime-style-palette-index.md`

其中：

- Step 3.5 默认直接注入 runtime 风格合同与预置风格入口
- 具体预置风格文件只在 style subagent 需要细看某个候选基底时按需读取
- `runtime-*` 文件不是页面 planning / html 阶段的 menu 资源

## 维护规则

- 新增资源文件放到对应目录，`resource_loader.py` 自动发现
- 每个资源文件必须有 `# 标题` + `> 多行引用`（数据类型、适用场景、约束）
- 不要在根目录放文件，不要创建新的子目录
- `runtime-*` 前缀的文件被 resource_loader 的 menu / resolve 流程跳过（仅供主链或特定 runtime 阶段直接读取）
