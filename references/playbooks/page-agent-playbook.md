# Page Agent Playbook -- 单页全链路

## 何时读取

- 当主 agent 为你分配一页 PPT 的完整生产任务时必读
- 你是该页从策划到终审的唯一负责人

## 目标

在一个 subagent 内完成单页的全链路生产：

```text
planning{n}.json -> planning 自审修复 -> 图片阶段 -> slide-{n}.html -> slide-{n}.png -> 第1轮图审修复 -> 第2轮图审修复 -> 通过 -> FINALIZE
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

使用 `style.json` 时遵守以下分工：

- planning 阶段至少消费 `mood_keywords`、`variation_strategy`、`decoration_dna`
- HTML 阶段强制消费 `css_variables`、`font_family`，并把 `design_soul` 作为情绪锚点
- 若存在 `css_snippets`，只把它当作局部样式锚点，不把它当整页骨架

### 资源消费规则

planning 阶段通过脚本加载资源菜单（所有资源的 `# 标题` + `> 引用`）：

```bash
python3 SKILL_DIR/scripts/resource_loader.py menu --refs-dir SKILL_DIR/references
```

- 菜单告诉你每个资源适用什么数据类型、什么场景
- 根据菜单选择资源，填入 planning JSON 的 `resources` 字段
- 不读正文（那是 html 阶段的事）

planning 阶段同时必须读取本地图片资产清单：

```bash
python3 SKILL_DIR/scripts/resource_loader.py images --images-dir OUTPUT_DIR/images
```

- 若用户已提供图片，优先从清单中绑定
- 若该页后续准备 AI 文生图，planning 可先规划目标路径，图片阶段再实际生成落盘

### 必须决定的字段

- `layout_hint` -- 布局
- `focus_zone` -- 视觉焦点
- `negative_space_target` -- 留白目标
- `page_text_strategy` -- 文字策略
- `cards[]` -- 卡片定义（类型、内容、主次关系）
- `resource_rationale` -- 为什么选这些资源
- `handoff_to_design` -- 给 HTML 阶段的不可推翻项
- `image.mode` -- 本页图片模式（`generate` / `provided` / `manual_slot` / `decorate`）

### 不可改写

- 页目标（来自 outline）
- 核心论证方向
- 用户明确禁止的内容

### 产物

写入 `planning/{PAGE_NUM}.json`

### 图片策略决策

planning 阶段不是只决定“要不要图”，还要先决定这页图片怎么来：

- `generate`
  适合封面、章节封面、核心案例页。
  做法：`image.needed=true`，写明 `usage / placement / content_description / source_hint`，并额外写英文 `image.prompt` 供图片子步骤消费。
  注意：你只负责把生成需求写清楚，不直接执行文生图。

- `provided`
  适合用户已给图片、品牌图库、项目截图。
  做法：`image.needed=true`，`source_hint` 直接绑定本地真实路径。

- `manual_slot`
  适合用户后续自己补图，但当前流程先继续。
  做法：`image.needed=false`，在 `handoff_to_design` 里说明图片槽位的位置、比例、裁切方式和替换建议。

- `decorate`
  适合数据页、纯逻辑页、或不希望引入外部图片的页面。
  做法：`image.needed=false`，在 `handoff_to_design` 中说明要用什么内部视觉语言补足氛围，例如 SVG 图形、字体装饰、编号水印、渐变纹理、几何图层。

### 自审

生成后立即运行：

```bash
python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning --refs SKILL_DIR/references --page PAGE_NUM
```

ERROR 必须修完再进入下一阶段。WARNING 建议修复。

---

## Phase 1.5: 图片阶段（轻量，不单独升级为主链步骤）

planning 通过后，根据 `image.mode` 做一次轻量资源准备：

- `generate`
  先向主 agent 发送 STATUS `WAIT_IMAGE_SUBAGENT`，带上 `image.prompt`、目标 `image.source_hint` 和当前阻塞项。
  若环境具备文生图能力且用户需要 AI 出图，主 agent 会创建独立的 `ImageGen` 子代理生成图片；主 agent 确认图片落盘后，你再继续进入 HTML。
  若环境不具备文生图能力，你必须回写 planning：将 `image.mode` 降级为 `manual_slot` 或 `decorate`，同步修正 `image.needed` / `image.source_hint` / `handoff_to_design`，并重新运行 planning validator，通过后再进入 HTML。

- `provided`
  校验绑定图片可访问，然后直接进 HTML。

- `manual_slot`
  不等待图片文件，直接进 HTML，但页面里必须保留一个真实可替换的图片区位。

- `decorate`
  不等待图片文件，直接进 HTML，但页面必须用内部 SVG / 字体 / 形状装饰完成视觉表达。

这一步只是单页链路里的过渡动作，不额外抽出新的主链 Stage。
文生图始终由独立的 `ImageGen` 子代理负责，而不是由你直接完成。

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

html 阶段开始前必须再次读取图片资产清单并核对 `image.source_hint`：

```bash
python3 SKILL_DIR/scripts/resource_loader.py images --images-dir OUTPUT_DIR/images
```

- 若 `image.mode=generate` 或 `provided`，HTML 必须渲染 `source_hint` 对应的真实图片
- 若 `image.mode=manual_slot`，HTML 必须保留手动替换位，不得擅自删掉图片区
- 若 `image.mode=decorate`，HTML 必须以内部图形/文字/装饰替代外部图片，而不是留空

### 文件独立性（硬约束）

- 每个 slide HTML 必须是**完全独立的自包含单文件**
- 所有 CSS 通过 `<style>` 标签内联在 `<head>` 中，禁止引用外部 CSS 文件（如 `deck.css`、`common.css`）
- 禁止跨页共享 CSS class 定义；每页的 class 命名和样式实现应完全独立
- CSS 变量统一从 `style.json` 的 `css_variables` 复制到 `:root`，这是唯一允许的跨页一致性
- 理由：每页是一幅独立的画面设计，共享 CSS 会导致 LLM 反复套用预定义 class 而丧失设计多样性

### 画布尺寸（不可违反的物理约束）

- **body 必须设置 `width: 1280px; height: 720px; overflow: hidden;`**
- 禁止使用 1600x900、1920x1080 或任何其他尺寸
- 禁止使用 `width: 100%; height: 100%` 然后依赖外部容器或 transform scale 缩放
- 禁止创建独立的 frame/wrapper 容器使用不同尺寸再 scale 回来
- 所有内容区域的绝对定位、padding、grid 尺寸必须基于 1280x720 画布计算
- 标题区: 左上 40px 边距, 最大高度 50px
- 内容区: padding 40px, 可用高度 580px, 可用宽度 1200px
- 页脚区: 底部 40px 边距内, 高度 20px
- 截图工具 html2png.py 的视口固定为 1280x720，超出部分将被裁切不可见

### 执行原则

- 统一语法，不统一长相
- 忠实执行 planning，不重做 planning
- 页面要有设计感，不像普通前端页面
- 必须使用 `style.json` 的 CSS 变量和字体栈
- `design_soul` 用来校准情绪，不可直接抄成文案
- `variation_strategy` 用来控制这一页的变化幅度，避免 deck 内同构复制
- `decoration_dna.forbidden` 是硬边界，`recommended_combos` 是优先组合，`signature_move` 是跨页识别锚点

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
- Grid 结构、class 命名、CSS 实现方式（每页独立设计，无需沿用其他页的写法）

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
| **画布合规** | body 为 1280x720 + overflow:hidden，无 scale hack，内容未超出视口边界 |
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
| **HTML 画布合规** | body 声明 `width:1280px; height:720px; overflow:hidden`，无 scale hack |
| PNG 存在 | `png/slide-{n}.png` 存在（图审执行证据） |
| 图片合同 | `generate` / `provided` 时 `source_hint` 可访问；`manual_slot` / `decorate` 时 HTML 落地策略明确 |
| 图审完成 | 至少 1 轮图审 |

## 生命周期

- 一个 PageAgent 只负责一页，不跨页
- 完成全链路后 FINALIZE
- 主 agent 回收后立即关闭
- 返工必须新开 PageAgent

## 画布合同（1280x720 物理红线）

- body 的 width/height 必须是 1280px/720px，overflow: hidden
- 禁止使用任何其他画布尺寸（如 1600x900）
- 禁止通过 transform: scale() 缩放 hack 来间接匹配画布
- 图审阶段若发现内容溢出 1280x720 视口，图审自动不通过
