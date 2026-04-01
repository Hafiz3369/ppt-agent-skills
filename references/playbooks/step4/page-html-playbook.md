# Page HTML Playbook -- 单页 HTML 设计稿

## 目标

忠实还原 planning JSON 里的骨架与精神，运用 `resource_loader.py resolve` 的解析能力，将抽象组件组装成极具高级设计感的**单页自包含 HTML**。

---

## Phase 1：骨架理解（不得跳过）

读取 `planning{n}.json` 的以下字段作为本阶段的硬约束：

| 字段 | HTML 阶段的含义 |
|------|--------------|
| `layout_hint` | 决定 grid/flex 结构的整体骨架 |
| `focus_zone` | 决定哪个卡片/区域应该有最大视觉权重 |
| `negative_space_target` | 决定留白比例（high=宽松 / medium=适中 / low=密集）|
| `cards[].visual_weight` | primary 卡片用最大字号+最强对比度，secondary 次之 |
| `handoff_to_design.non_negotiables` | 这些设计决策不得修改，必须照做 |
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

---

## Phase 3：图片模式严格执行

| image.mode | HTML 要做什么 | 绝对禁止 |
|-----------|-------------|---------|
| `generate` / `provided` | 用 `source_hint` 路径渲染 `<img src>` 或 `background-image: url()` | 不得用占位色块替代真实图 |
| `manual_slot` | 渲染明确尺寸的图片占位框（带虚线边框 + 文字说明"[图片替换位]"）| 不得删掉或做成看不出来的空白 |
| `decorate` | 使用内联 SVG、CSS 渐变、几何色块、大字水印、圆圈装饰等内部视觉语言补足氛围 | 不得留空白大洞，不得放空的 `<div>` |

---

## Phase 4：画布物理红线（不可违反）

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

## Phase 5：风格变量严格绑定

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

## Phase 6：设计多样性要求

- 每张卡片的 class 命名**全部独立自定义**，禁止复用上一页的 class 结构
- CSS 实现方式每页独立设计，不套模板
- 同一套 deck 中每页都应有视觉差异感（不同色块比例/不同排版中心/不同装饰位置）

---

## Phase 7：完成条件

写入 `{{SLIDE_OUTPUT}}` 后：
- 文件非空
- 无语法错误（HTML 标签闭合完整）
- 没有明显乱码或缺失的 CSS 变量引用

发送 FINALIZE 信号，然后等待 Review 阶段指令。
