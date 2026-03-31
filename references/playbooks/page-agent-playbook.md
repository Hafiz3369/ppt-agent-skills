# Page Agent Playbook -- 单页全链路

## 何时读取

- 当主 agent 为你分配一页 PPT 的完整生产任务时必读
- 你是该页从策划到终审的唯一负责人

## 目标

在一个 subagent 内完成单页的全链路生产：

```text
planning{n}.json -> planning 自审修复 -> slide-{n}.html -> slide-{n}.png -> 第1轮图审修复 -> 第2轮图审修复 -> 通过 -> FINALIZE
```

## 输入

所有输入在 prompt 中通过 harness 预填充路径：

| 文件 | 用途 |
|------|------|
| `requirements-interview.txt` | 用户需求 |
| `outline.txt` | 大纲（你只关注分配给你的那一页） |
| `search-brief.txt` / `source-brief.txt` | 素材摘要 |
| `style.json` | 全局风格合同（必须遵守） |
| Prompt 中的页码与总页数 | 你的边界 |

## 职责边界

### 你负责

- 读取大纲中你那一页的定义，生成 planning JSON
- 基于 planning 生成 HTML
- 截图并自审
- 修复不达标的部分
- 所有产物直接写文件

### 你不负责

- 其他页面（一个 subagent 只负责一页）
- 修改全局文件（requirements / outline / style）
- 与其他页面 subagent 通信

---

## Phase 1: Planning（策划稿）

### 输入

- `requirements-interview.txt` 的用户需求 + `outline.txt` 中你这一页的定义
- `search-brief.txt` 的素材
- `style.json` 的风格合同

### 资源消费规则

planning 阶段通过脚本加载资源菜单（所有资源的 `# 标题` + `> 引用`）：

```bash
python3 SKILL_DIR/scripts/resource_loader.py menu --refs-dir SKILL_DIR/references
```

- 菜单告诉你每个资源适用什么数据类型、什么场景
- 根据菜单选择资源，填入 planning JSON 的 `resources` 字段
- 不读正文（那是 html 阶段的事）

### 必须决定的字段

- `layout_hint` -- 布局
- `focus_zone` -- 视觉焦点
- `negative_space_target` -- 留白目标
- `page_text_strategy` -- 文字策略
- `cards[]` -- 卡片定义（类型、内容、主次关系）
- `resource_rationale` -- 为什么选这些资源
- `handoff_to_design` -- 给 HTML 阶段的不可推翻项

### 不可改写

- 页目标（来自 outline）
- 核心论证方向
- 用户明确禁止的内容

### 产物

写入 `planning/{PAGE_NUM}.json`

### 自审

生成后立即运行：

```bash
python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning --refs SKILL_DIR/references --page PAGE_NUM
```

ERROR 必须修完再进入下一阶段。WARNING 建议修复。

---

## Phase 2: HTML（设计稿）

### 输入

- 你刚生成的 `planning{n}.json`
- `style.json`
- `references/` 下的资源文件

### 资源消费规则

html 阶段通过脚本按 planning JSON 字段动态加载对应资源的正文：

```bash
python3 SKILL_DIR/scripts/resource_loader.py resolve --refs-dir SKILL_DIR/references --planning PLANNING_OUTPUT
```

- 脚本读 planning JSON 的 `layout_hint`/`card_type`/`chart_type` 等字段
- 只加载被引用的资源正文（不是全部）
- 自动包含 card-styles 和数据类型映射表
- 不读 `>` 引用（那是 planning 阶段已用过的）

### 执行原则

- 统一语法，不统一长相
- 忠实执行 planning，不重做 planning
- 页面要有设计感，不像普通前端页面
- 必须使用 `style.json` 的 CSS 变量

### 继承自 planning 的不可改项

- `page_type`
- `layout_hint`
- `focus_zone`
- `visual_weight`
- `cards[]` 的主次关系
- `handoff_to_design.non_negotiables`

### 可以发挥的空间

- 构图比例
- 层次深度
- 材质、遮罩、裁切、装饰组织
- 同类卡片之间的微差异

### 产物

写入 `slides/slide-{PAGE_NUM}.html`

---

## Phase 3: 截图

生成 HTML 后执行：

```bash
python3 SKILL_DIR/scripts/html2png.py OUTPUT_DIR/slides/slide-{PAGE_NUM}.html -o OUTPUT_DIR/png --scale 2
```

产物：`png/slide-{PAGE_NUM}.png`

---

## Phase 4: 图审（双轮）

### 第 1 轮图审

读取 `png/slide-{PAGE_NUM}.png`，对照以下维度评分：

| 维度 | 9 分通过线 |
|------|----------|
| 信息密度 | 每张卡片有标题+正文+数据，无空卡 |
| 视觉冲击力 | 有明确设计感，不像普通前端页面 |
| 布局精度 | 无重叠、无溢出、grid 定位正确 |
| 色彩执行 | 全部通过 CSS 变量 |
| 资源消费 | planning 指定的资源在 HTML 中体现 |
| 叙事贡献 | 该页角色清晰 |

任一维度 < 9 分 -> 直接修改 HTML 文件 -> 重新截图

### 第 2 轮图审

重新读取修改后的 PNG，确认修复生效。

如果仍有 < 9 分的维度，标注问题但允许通过（单页最多 2 轮图审）。

---

## Phase 5: FINALIZE

双轮图审完成后：

1. 确认以下产物都已写入：
   - `planning/planning{PAGE_NUM}.json`
   - `slides/slide-{PAGE_NUM}.html`
   - `png/slide-{PAGE_NUM}.png`
2. 发送 FINALIZE 信号给主 agent
3. 等待主 agent 关闭你

---

## 质量底线

| 检查项 | 标准 |
|--------|------|
| planning 存在 | `planning/planning{n}.json` 非空 |
| planning 合法 | planning_validator 无 ERROR |
| HTML 存在 | `slides/slide-{n}.html` 非空 |
| PNG 存在 | `png/slide-{n}.png` 存在（图审执行证据） |
| 图审完成 | 至少 1 轮图审 |

## 生命周期

- 一个 PageAgent 只负责一页，不跨页
- 完成全链路后 FINALIZE
- 主 agent 回收后立即关闭
- 返工必须新开 PageAgent
