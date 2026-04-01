# Page HTML Playbook -- 单页 HTML 设计稿

## 目标

忠实还原 planning JSON 里的骨架与精神，运用 `resource_loader.py resolve` 的解析能力，将抽象组件组装成极具高级设计感的**单页自包含 HTML**。

---

## Phase 1：骨架理解（不得跳过）

读取 `planning{n}.json` 的以下字段作为本阶段的硬约束：

| 字段 | HTML 阶段的含义 |
|------|--------------|
| `page_type` / `layout_hint` | 决定整体骨架与页面自由度 |
| `focus_zone` | 决定哪个卡片/区域应该有最大视觉权重 |
| `negative_space_target` | 决定留白比例（high=宽松 / medium=适中 / low=密集）|
| `cards[].role` / `cards[].card_style` | 决定主次顺序与卡片存在感 |
| `cards[].card_id` | 要在 HTML 中逐一落地，并映射到 `data-card-id` |
| `cards[].content_budget` | 限制每张卡片的承载量，防止溢出 |
| `director_command` / `decoration_hints` | 决定镜头感、装饰层次和实现边界 |
| `source_guidance` / `must_avoid` | 决定证据呈现方式与禁止动作 |
| `image.mode` | 严格按下面第 3 条执行 |

---

## Phase 2：资源正文消费（强制执行，不得跳过）

```bash
python3 SKILL_DIR/scripts/resource_loader.py resolve --refs-dir REFS_DIR --planning PLANNING_OUTPUT
```

脚本返回 planning 中引用的每个资源的**完整正文实现**，包含：
- 组件的 HTML 结构骨架（含 class 命名示例）
- 推荐的 CSS 参数（间距、字号、颜色变量用法）
- 数据格式要求（如 chart 的 data 格式）

**你必须照着实现，细节可微调，结构不得绕过。**

特别注意：
- 若 resolve 返回了组件的**语义类锚点**，必须保留这些锚点；你可以附加 page-local modifier class，但不要替换掉核心结构。
- 若 planning 的 `resources.*_refs` 与 `card.resource_ref.*` 同时存在，优先保证两者都被消费，不要只看其中一层。
- `process` 这类没有独立 block 文件的 card_type，优先从 `layout_refs`、`principle_refs`、`director_command` 和相关 chart 资源中组装实现。

---

## Phase 3：图片模式严格执行

| image.mode | HTML 要做什么 | 绝对禁止 |
|-----------|-------------|---------|
| `generate` / `provided` | 用 `source_hint` 路径渲染 `<img src>` 或 `background-image: url()` | 不得用占位色块替代真实图 |
| `manual_slot` | 渲染明确尺寸的图片占位框（带虚线边框 + 文字说明"[图片替换位]"）| 不得删掉或做成看不出来的空白 |
| `decorate` | 使用内联 SVG、CSS 渐变、几何色块、大字水印、圆圈装饰等内部视觉语言补足氛围 | 不得留空白大洞，不得放空的 `<div>` |

---

## Phase 4：卡片落地对账（强制）

- `planning.cards[]` 中的每一张卡都必须有一个对应的 HTML 根节点。
- 每个根节点都要带 `data-card-id="<card_id>"`，便于 Review 阶段与 planning 对账。
- `role = anchor` 的卡必须成为全页第一视觉落点；`support/context` 退后，但不能消失。
- 若卡片带 `chart.chart_type`，最终图表类型必须与 planning 保持一致；不要把 `comparison_bar` 偷换成普通 list。
- 若 `source_guidance` 要求保留来源，至少在卡片 footer / caption / 注释位中给出来源提示。

---

## Phase 5：画布物理红线（不可违反）

```css
body {
  width: 1280px;
  height: 720px;
  overflow: hidden;
  margin: 0;
  padding: 0;
}
```

- **禁止** `width: 100%; height: 100%` 然后依赖父容器
- **禁止** `transform: scale()` 缩放 hack
- **禁止** 引用外部 CSS 文件（如 `common.css`、`deck.css`）
- 标题区：顶部 40px 留白，高度不超过 60px
- 内容区：左右各 40px padding，可用宽度 1200px，可用高度约 580px
- 页脚区：底部 40px 内，高度 20px

---

## Phase 6：风格变量严格绑定

从 `style.json` 的 `css_variables` 提取所有变量，写入 HTML 的 `:root`：

```css
:root {
  --bg-primary: [从 style.json 取];
  --bg-secondary: [从 style.json 取];
  --card-bg-from: [从 style.json 取];
  --card-bg-to: [从 style.json 取];
  --card-border: [从 style.json 取];
  --card-radius: [从 style.json 取];
  --text-primary: [从 style.json 取];
  --text-secondary: [从 style.json 取];
  --accent-1: [从 style.json 取];
  --accent-2: [从 style.json 取];
  --accent-3: [从 style.json 取];
  --accent-4: [从 style.json 取];
  --font-primary: [从 style.json font_family 取];
}
```

- `design_soul`：用来校准情绪，不得直接抄成页面文案
- `variation_strategy`：控制这一页的变化幅度，避免与相邻页同构复制
- `decoration_dna.forbidden`：硬边界，违反即自动不达标
- `decoration_dna.recommended_combos`：优先采用
- `decoration_dna.signature_move`：跨页识别锚点，必须出现

---

## Phase 7：设计多样性要求

- 页面级 wrapper、modifier class 应该带有本页差异性，避免连续两页像复制模板
- **但**如果 resolve 提供了核心结构或语义类锚点，必须保留，不得为了“全都自定义”而破坏资源合同
- CSS 实现方式每页独立设计，但仍需服从 `style.json`、`director_command` 与资源正文的共同约束
- 同一套 deck 中每页都应有视觉差异感（不同色块比例/不同排版中心/不同装饰位置）

---

## Phase 8：完成条件

写入 `{{SLIDE_OUTPUT}}` 后：
- 文件非空
- 无语法错误（HTML 标签闭合完整）
- 没有明显乱码或缺失的 CSS 变量引用
- `planning.cards[]` 全部能在 HTML 中找到对应的 `data-card-id`

发送 FINALIZE 信号，然后等待 Review 阶段指令。
