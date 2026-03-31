# References Index

本目录包含 PPT 工作流的全部资源文件。由 `resource_loader.py` 动态加载到 subagent 上下文中。

## 目录结构

```
references/
  playbooks/          -- subagent 执行细则（3 个）
  prompts/            -- prompt 模板（5 个 tpl-*.md）
  layouts/            -- 版式资源（10 种）
  blocks/             -- 区域展示组件（8 种 + card-styles）
  charts/             -- 图表组件（13 种 + runtime-chart-rules）
  styles/             -- 风格主题（8 种 + runtime-style-rules）
  principles/         -- 设计原则（7 种 + runtime-failure-modes）
  page-templates/     -- 页面结构模板（cover/toc/section/end）
  design-runtime/     -- 数据类型映射 + 设计规格 + CSS 武器库
```

## 核心入口

先读这些，再看资源库细项：

1. `SKILL.md` -- 编排合同（唯一真源）
2. `playbooks/page-agent-playbook.md` -- 单页全链路执行细则
3. `playbooks/research-synth-playbook.md` -- 搜集整理执行细则
4. `playbooks/outline-subagent-playbook.md` -- 大纲+自审执行细则

## Prompt 模板

`tpl-*.md` 文件由 `scripts/prompt_harness.py` 填充 `{{VAR}}` 变量后发给 subagent：

| 模板 | 阶段 | 变量 |
|------|------|------|
| `tpl-interview.md` | Step 1 采访 | TOPIC |
| `tpl-research-synth.md` | Step 2A 搜集 | TOPIC, REQUIREMENTS_PATH, TOOLS_AVAILABLE |
| `tpl-outline.md` | Step 3 大纲 | REQUIREMENTS_PATH, BRIEF_PATH, OUTLINE_OUTPUT |
| `tpl-style.md` | Step 3.5 风格 | REQUIREMENTS_PATH, OUTLINE_PATH, STYLE_OUTPUT |
| `tpl-page-agent.md` | Step 4-5 单页 | PAGE_NUM, PLANNING_OUTPUT, SLIDE_OUTPUT, ... |

## 资源库

6 个资源目录由 `scripts/resource_loader.py` 管理：

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

## 维护规则

- 新增资源文件放到对应目录，`resource_loader.py` 自动发现
- 每个资源文件必须有 `# 标题` + `> 多行引用`（数据类型、适用场景、约束）
- 不要在根目录放文件，不要创建新的子目录
- `runtime-*` 前缀的文件被 resource_loader 跳过（仅供主链直接读取）
