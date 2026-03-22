# HTML -> SVG -> PPTX 管线兼容性规则

本文档汇总所有管线兼容性约束。**HTML 设计稿生成时必须遵守，在源头规避转换问题。**

---

## 管线三层模型（为什么要有这些规则）

```
HTML 设计稿           dom-to-svg              svg2pptx.py
(浏览器渲染)    --->   (SVG 矢量)     --->    (OOXML 原生形状)
   全 CSS              SVG 子集               PPTX 子集
```

每一层都会丢失上一层的部分能力。**核心策略：从最终消费端（PPTX）倒推，只生成整条管线都支持的 HTML 写法。**

| 层级 | 工具 | 能力边界 |
|------|------|---------|
| **第 1 层：HTML** | 浏览器 | 全 CSS 支持，无限制 |
| **第 2 层：SVG** | dom-to-svg | 不认伪元素、不认 mask-image、不认 conic-gradient、CSS Variables 有 bug |
| **第 3 层：PPTX** | svg2pptx.py | 只认 rect/circle/ellipse/line/path(M/L/H/V/C/Z)/text/image/linearGradient/radialGradient |

**规则制定逻辑**：第 3 层不支持 -> 第 2 层生成出来也没用 -> 第 1 层就不要写。

---

## 1. CSS 禁止清单

### 1.1 完全禁止（dom-to-svg 无法转换或 svg2pptx 无法解析）

| 禁止特性 | 转换后现象 | 正确替代写法 |
|---------|---------|-----------|
| `background-clip: text` | 渐变变色块 + 白色文字 | `color: var(--accent-1)` 直接上色 |
| `-webkit-text-fill-color` | 文字颜色丢失 | 标准 `color` 属性 |
| `mask-image` / `-webkit-mask-image` | 图片完全消失 | `<div>` 遮罩层（linear-gradient 背景） |
| `::before` / `::after`（视觉装饰用） | 内容消失 | 真实 `<div>` / `<span>` |
| `conic-gradient` | 不渲染 | 内联 SVG `<circle>` + stroke-dasharray |
| CSS border 三角形 (width:0 trick) | 形状丢失 | 内联 SVG `<polygon>` |
| `mix-blend-mode` | 不支持 | `opacity` 叠加 |
| `filter: blur()` | 光栅化变位图，svg2pptx 无法解析 | `opacity` 或 `box-shadow` |
| `filter: drop-shadow()` | 光栅化 | `box-shadow`（dom-to-svg 支持） |
| `content: '文字'` | 文字消失 | 真实 `<span>` |
| CSS `background-image: url(...)` | dom-to-svg 忽略 | `<img>` 标签 |
| `clip-path`（CSS 属性） | dom-to-svg 可能保留为 SVG clipPath，但 svg2pptx 不处理 clipPath | `overflow:hidden` + 容器裁切，或 `border-radius` |
| `backdrop-filter` | dom-to-svg 不支持 | 半透明 `<div>` 背景色模拟 |
| CSS `animation` / `@keyframes` | 不影响转换但 PPTX 无动画 | 可用于 HTML 预览，不影响管线（安全） |
| `writing-mode: vertical-*` | dom-to-svg 文字方向可能异常 | 用多个水平 `<span>` 逐字堆叠模拟 |

html2svg.py 兜底覆盖（共 13 种）：background-clip:text / -webkit-text-fill-color / 伪元素 / conic-gradient / border 三角形 / mask-image / background-image:url() / clip-path / backdrop-filter / filter:blur()/drop-shadow() / mix-blend-mode / **内联 SVG text 自动提取为 HTML 叠加层** / **use 元素自动展开**。兜底降低了"LLM 犯错就翻车"的风险，但正确写法仍优于兜底。

### 1.2 有条件安全（正确使用时可通过管线）

| CSS 特性 | 条件 | 说明 |
|---------|------|------|
| `box-shadow` | 仅实色阴影 | dom-to-svg 转为 SVG filter，svg2pptx 跳过 filter，阴影丢失但不影响布局 |
| `border-radius` | 任意值 | dom-to-svg 正确转换，svg2pptx 的 `roundRect` preset 支持 |
| `opacity` | 0-1 任意值 | 全管线支持，svg2pptx 通过 `a:alpha` 元素实现 |
| `overflow: hidden` | 仅作裁切用 | dom-to-svg 保留视觉效果，但 svg2pptx 不处理 clipPath，超出部分可能在 PPTX 中可见。实际影响较小因为 dom-to-svg 已裁切了视觉内容 |
| `transform: rotate()` | 仅内联 SVG 上的 transform 属性 | svg2pptx 支持 SVG transform（translate/scale/rotate/matrix），但不支持 CSS transform 到 SVG 的精确映射 |
| `linear-gradient()` | 作为背景色 | dom-to-svg 转为 SVG linearGradient，svg2pptx 支持 |
| `radial-gradient()` | 作为背景色 | dom-to-svg 转为 SVG radialGradient，svg2pptx 支持 |
| `text-decoration` | 下划线/删除线 | dom-to-svg 可能转为额外 rect/line，svg2pptx 能处理 |

---

## 2. CSS 安全白名单（推荐使用）

以下 CSS 特性经过全管线验证，可以放心使用：

### 2.1 布局类（全部安全）

| 特性 | PPTX 最终效果 |
|------|-------------|
| `display: flex` + 全部 flex 属性 | dom-to-svg 精确计算布局位置 |
| `display: grid` + 全部 grid 属性 | dom-to-svg 精确计算布局位置 |
| `position: absolute/relative` | dom-to-svg 精确计算坐标 |
| `width/height/margin/padding` | 精确映射 |
| `gap` | flex/grid gap 精确映射 |

### 2.2 视觉类（管线验证安全）

| 特性 | PPTX 最终效果 |
|------|-------------|
| `background-color`（纯色/渐变） | 转为 OOXML solidFill / gradFill |
| `linear-gradient()` | 转为 OOXML a:lin 渐变 |
| `radial-gradient()` | 转为 OOXML path:circle 渐变 |
| `border`（实色描边） | 转为 OOXML a:ln 描边 |
| `border-radius` | 转为 roundRect preset + adj 值 |
| `opacity` | 转为 OOXML a:alpha 透明度 |
| `color`（纯色） | 转为 OOXML a:solidFill 文字色 |
| `font-size / font-weight / font-family` | 转为 OOXML a:rPr 文字属性 |

### 2.3 元素类（管线验证安全）

| HTML 元素 | PPTX 最终效果 |
|----------|-------------|
| `<div>` / `<span>` / `<p>` 等块/行内元素 | dom-to-svg 转为 SVG rect/text，svg2pptx 转为形状/文本框 |
| `<img>` 标签（绝对/相对路径） | html2svg 内联为 data URI，svg2pptx 转为 add_picture |
| 内联 `<svg>` + 基础图形元素 | 直接传入 svg2pptx 处理 |
| `<strong>` / `<em>` | 转为字重/字号变化 |

---

## 3. 防偏移写法（关键章节）

svg2pptx 的文本定位基于 SVG text 元素的坐标，但 PPTX textbox 的坐标系与 SVG 不同（SVG text y = baseline，PPTX y = textbox 顶部）。以下写法可从 HTML 源头避免偏移：

### 3.1 内联 SVG 中的文本标注 -- 用 HTML 叠加替代 SVG text

**问题**：内联 SVG 中的 `<text>` 元素经过 dom-to-svg 转换后坐标是 viewBox 坐标系，svg2pptx 在处理 baseline 偏移和 text-anchor 居中时有精度损失（约 +/- 3-5px），导致标注位置偏移。

**HTML 防偏移写法**：把文字标注从 SVG `<text>` 移出来，用 HTML `<div>` 绝对定位叠加在 SVG 上方。HTML div 由 dom-to-svg 精确定位，不经过 viewBox 坐标转换，偏移风险为零。

```html
<!-- 正确：HTML div 叠加标注，零偏移 -->
<div class="chart-container" style="position: relative;">
  <svg viewBox="0 0 660 340" style="width:100%; height:100%;">
    <!-- 只画柱子、线条等图形元素，不写 <text> -->
    <rect x="80" y="100" width="60" height="200" fill="#FF6900"/>
  </svg>
  <!-- 标注用 HTML 绝对定位叠加 -->
  <span style="position:absolute; left:12.5%; top:25%; font-size:14px; color:#fff;">720</span>
  <span style="position:absolute; left:12.5%; bottom:5%; font-size:12px; color:rgba(255,255,255,0.6);">标准版</span>
</div>
```

```html
<!-- 禁止：SVG text 在 PPTX 中会偏移 -->
<svg viewBox="0 0 660 340">
  <rect x="80" y="100" width="60" height="200" fill="#FF6900"/>
  <text x="110" y="90" text-anchor="middle" fill="#fff">720</text>
</svg>
```

### 3.2 不同字号混排 -- 必须用 flex 独立元素

**问题**：大小字号内嵌（`<div class="big">3.08<span class="small">s</span></div>`）经 dom-to-svg 转为独立 tspan 后，svg2pptx 给每个 tspan 按各自字号做 baseline 偏移，小字会上移。

```html
<!-- 正确：flex baseline 对齐 -->
<div style="display:flex; align-items:baseline; gap:4px;">
  <span style="font-size:48px;">3.08</span>
  <span style="font-size:18px;">s</span>
</div>
```

```html
<!-- 禁止：内嵌不同字号 span -->
<div class="big">3.08<span class="small">s</span></div>
```

### 3.3 环形图（圆弧进度条）-- SVG 画弧 + HTML 叠加文字

```html
<!-- 正确：环形图最佳实践 -->
<div class="ring-container" style="position: relative; width:120px; height:120px;">
  <!-- SVG 只画圆环弧线 -->
  <svg viewBox="0 0 120 120" style="width:100%; height:100%;">
    <!-- 底圈 -->
    <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="8"/>
    <!-- 弧线：用 dasharray 两值格式，禁止 dashoffset -->
    <circle cx="60" cy="60" r="50" fill="none" stroke="#FF6900" stroke-width="8"
            stroke-dasharray="235 314" stroke-linecap="round"
            transform="rotate(-90 60 60)"/>
  </svg>
  <!-- 中心文字用 HTML 叠加，不用 SVG text -->
  <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); text-align:center;">
    <div style="font-size:22px; font-weight:700; color:#fff;">15</div>
    <div style="font-size:10px; color:rgba(255,255,255,0.6);">分钟</div>
  </div>
</div>
```

### 3.4 图例标签 -- 用 HTML flex 布局

```html
<!-- 正确：HTML flex 图例，不用 SVG text -->
<div style="display:flex; gap:16px; font-size:12px;">
  <div style="display:flex; align-items:center; gap:4px;">
    <span style="display:inline-block; width:12px; height:12px; background:#999; border-radius:2px;"></span>
    <span style="color:rgba(255,255,255,0.6);">初代SU7</span>
  </div>
  <div style="display:flex; align-items:center; gap:4px;">
    <span style="display:inline-block; width:12px; height:12px; background:#FF6900; border-radius:2px;"></span>
    <span style="color:rgba(255,255,255,0.6);">新一代SU7</span>
  </div>
</div>
```

### 3.5 x 轴标签（标准版/Pro/Max）-- 用 HTML 容器

```html
<!-- 正确: x 轴标签用 HTML -->
<div style="display:flex; justify-content:space-around; padding:0 10%;">
  <span style="font-size:13px; color:rgba(255,255,255,0.6);">标准版</span>
  <span style="font-size:13px; color:rgba(255,255,255,0.6);">Pro</span>
  <span style="font-size:13px; color:rgba(255,255,255,0.6);">Max</span>
</div>
```

---

## 4. 图片路径与处理

| 场景 | 错误写法 | 正确写法 |
|------|---------|---------| 
| img src 引用 | 依赖浏览器 resolve | html2svg 以 HTML 文件所在目录为基准 resolve 相对路径 |
| CSS background-image | 会被 dom-to-svg 忽略 | 用 `<img>` 标签 |
| 远程 URL 图片 | `<img src="https://...">` | html2svg 无法获取，必须先下载到本地 |

**图片在 PPTX 中的行为**：svg2pptx 实现了 `object-fit: cover` 等效效果（通过 srcRect 裁剪），但不支持 `object-fit: contain` 或 `object-position` 偏移。如需精确控制图片裁剪区域，用 `<div>` 容器 + `overflow:hidden` + 图片定位。

---

## 5. SVG circle 环形图属性

| 属性 | svg2pptx 支持 | 说明 |
|------|-------------|------|
| `stroke-dasharray="arc gap"` | 支持 | 用两个值：弧线长度 + 间隔长度 |
| `stroke-dashoffset` | **不支持** | 禁止使用，改用 dasharray 的两值格式 |
| `stroke-linecap="round"` | 支持 | 圆角弧端 |
| `transform="rotate(-90 cx cy)"` | 支持 | 从12点钟方向开始 |

正确弧线写法：`stroke-dasharray="235 314"` （弧长=235, 圆周=2*pi*50=314）

---

## 6. 内联 SVG 元素支持矩阵

> svg2pptx.py 逐元素遍历 SVG 并转为 OOXML 形状。以下是精确的支持情况（源自 svg2pptx.py 源码逆向分析）。

### 6.1 完全支持的 SVG 元素

| SVG 元素 | OOXML 映射 | 支持的属性 |
|----------|-----------|-----------|
| `<rect>` | `prstGeom: rect/roundRect` | x, y, width, height, rx, ry, fill, stroke, stroke-width, opacity |
| `<circle>` | `prstGeom: ellipse` | cx, cy, r, fill, stroke, stroke-width, opacity, stroke-dasharray, transform |
| `<ellipse>` | `prstGeom: ellipse` | cx, cy, rx, ry, fill, opacity |
| `<line>` | `prstGeom: line` | x1, y1, x2, y2, stroke, stroke-width |
| `<text>` + `<tspan>` | `p:sp txBox` | x, y, font-size, font-weight, font-family, fill/color, text-anchor, dominant-baseline, textLength, opacity |
| `<image>` | `add_picture` | x, y, width, height, href/xlink:href (data URI / file:// / 相对路径), opacity |
| `<g>` | 递归遍历子元素 | transform (translate/scale/matrix), opacity（累积传递） |
| `<linearGradient>` | `a:gradFill + a:lin` | x1, y1, x2, y2, stop (offset + stop-color + stop-opacity) |
| `<radialGradient>` | `a:gradFill + path:circle` | stop (offset + stop-color + stop-opacity) |

### 6.2 部分支持的 SVG path 命令

| path 命令 | svg2pptx 支持 | OOXML 映射 |
|-----------|-------------|-----------|
| M / m (moveTo) | 支持 | `a:moveTo` |
| L / l (lineTo) | 支持 | `a:lnTo` |
| H / h (横向线) | 支持 | `a:lnTo`（补全 y 坐标） |
| V / v (纵向线) | 支持 | `a:lnTo`（补全 x 坐标） |
| C / c (三次贝塞尔) | 支持 | `a:cubicBezTo` |
| Z / z (闭合) | 支持 | `a:close` |
| **S / s** (平滑贝塞尔) | **跳过** | 曲线丢失 |
| **Q / q** (二次贝塞尔) | **跳过** | 曲线丢失 |
| **T / t** (平滑二次) | **跳过** | 曲线丢失 |
| **A / a** (弧线) | **跳过** | 弧线丢失 |

**HTML 写法约束**：
- 内联 SVG 中的 `<path>` 只用 M/L/H/V/C/Z 命令
- 需要弧线时，用 `<circle>` + stroke-dasharray 替代 `<path>` 的 A 命令
- 需要平滑曲线时，将 S/Q/T 转为等价的 C（三次贝塞尔）命令
- 实际影响较小：dom-to-svg 生成的 path 通常自动使用 M/L/C/Z 组合

### 6.3 不支持的 SVG 元素（svg2pptx 静默跳过）

| SVG 元素 | 处理方式 | HTML 替代方案 |
|----------|---------|-------------|
| `<foreignObject>` | 完全忽略 | 不要在内联 SVG 中嵌入 HTML |
| `<clipPath>` | 忽略（定义在 defs 中） | 用 CSS `overflow:hidden` + 容器裁切 |
| `<filter>` | 忽略 | 用 CSS `opacity` / `box-shadow` 替代 |
| `<mask>` | 忽略 | 用 `<div>` 遮罩层 + opacity 替代 |
| `<pattern>` | 忽略 | 用实色或渐变替代 |
| `<use>` | 不展开引用 | 直接写出完整元素，不用 `<use>` 引用 |
| `<marker>` | 忽略 | 用 `<polygon>` 手动画箭头 |
| `<symbol>` | 忽略 | 直接写出完整元素 |
| `<textPath>` | 忽略 | 用 HTML 定位文字替代 |
| `<animate>` / `<animateTransform>` | 忽略 | PPTX 无 SVG 动画 |

---

## 7. 渐变使用约束

### 7.1 填充渐变（安全）

svg2pptx 完全支持 linearGradient 和 radialGradient 的**填充**用途：

```html
<!-- 安全：渐变填充 -->
<rect fill="url(#myGrad)" ... />
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e);">
```

### 7.2 描边渐变（降级）

svg2pptx 处理渐变描边时**只取第一个 stop 颜色**作为实色描边：

```html
<!-- 有风险：渐变描边会降级为实色 -->
<circle stroke="url(#gradStroke)" ... />
<!-- 在 PPTX 中变为第一个 stop 颜色的实色描边 -->
```

**HTML 写法约束**：如果描边颜色很重要，直接用实色。渐变描边仅用于"降级后也能接受"的装饰场景。

### 7.3 渐变 stop 数量

svg2pptx 支持任意数量的 stop，但 PPTX 渐变在复杂 stop 时渲染可能与浏览器有细微差异。建议：

- 2-3 个 stop：完美
- 4-5 个 stop：可接受
- 6+ 个 stop：可能有视觉差异，建议简化

---

## 8. 字体约束

### 8.1 svg2pptx 字体回退映射

svg2pptx 内建以下字体映射，HTML 使用这些字体时会自动回退为 PPTX 可用字体：

| 浏览器字体 | PPTX 回退 |
|-----------|----------|
| PingFang SC | Microsoft YaHei |
| SF Pro Display | Arial |
| Helvetica Neue | Arial |
| Helvetica | Arial |
| system-ui | Microsoft YaHei |
| sans-serif | Microsoft YaHei |

### 8.2 HTML 字体选择约束

- **中文内容**：优先用 `'Microsoft YaHei', sans-serif`（直接命中目标，减少映射环节）
- **英文数据数字**：可用 `'Inter', 'DIN', Arial, sans-serif`
- **禁止使用**：Google Fonts 等在线字体（dom-to-svg 可能无法加载外部资源）
- **font-family 声明**：始终提供 fallback chain，末尾包含通用族名

### 8.3 文字尺寸约束

svg2pptx 的文本框尺寸基于字符宽度估算（CJK 字符 ~0.95em，拉丁字符 ~0.6em）。以下场景可能导致文本框宽度不精确：

- **极长文本行**（单行 > 60 字符）：累积误差可能导致末尾被裁
- **极小字号**（< 10px）：分辨率丢失
- **极大字号**（> 80px）：ascent 补偿系数可能偏移

**建议**：正文 12-16px，标题 18-56px，数据数字 36-80px。在此范围内偏移风险最低。

---

## 9. 形状数量与性能约束

### 9.1 svg2pptx 的过滤规则

svg2pptx 会静默丢弃以下元素：

| 过滤条件 | 行为 |
|---------|------|
| `<rect>` 面积 < 4px x 4px | 跳过（stats['skipped']++） |
| `<circle>` r < 2px | 跳过 |
| `<path>` bounding box < 4px x 4px | 跳过 |
| `<rect>` fill=全透明 且 无 stroke | 跳过 |
| 第一个全屏 rect (>=1270x710) | 转为幻灯片背景色（不创建形状） |

**HTML 写法约束**：
- 装饰性小点/线如需保留，确保尺寸 >= 4px
- 如需 2-3px 的细线装饰，用 `<div>` 而非内联 SVG 的 `<rect>` / `<line>`

### 9.2 性能约束

每页 SVG 经过 svg2pptx 后会生成大量 OOXML 形状。形状越多，PowerPoint 打开越慢：

| 每页形状数 | 性能表现 |
|-----------|---------|
| < 100 | 流畅 |
| 100-200 | 正常 |
| 200-500 | 略卡（复杂页面可接受） |
| > 500 | 明显卡顿 |

**HTML 写法约束**：
- 避免大量重复的微小装饰元素（如 100 个小圆点组成的背景网格）
- 背景网格/点阵装饰优先用 CSS `background-image: radial-gradient()` 实现（dom-to-svg 作为单个 rect 的填充处理），但注意 CSS background-image url() 被禁用
- 如需背景点阵：用一个低 opacity 的 `<div>` + 内联 SVG 画少量代表性点（< 30 个），而非逐像素绘制

---

## 10. CSS transform 约束

### 10.1 SVG transform（安全）

svg2pptx 支持以下 SVG transform 属性：

| transform 值 | 支持情况 |
|-------------|---------|
| `translate(dx, dy)` | 完全支持（坐标偏移累积） |
| `scale(sx, sy)` | 完全支持（尺寸缩放累积） |
| `matrix(a,b,c,d,e,f)` | 支持（提取 translate + scale） |
| `rotate(angle cx cy)` | 支持（环形图角度计算） |

### 10.2 CSS transform（部分安全）

dom-to-svg 会将 CSS transform 转为计算后的坐标位置。以下用法安全：

| CSS transform 用法 | 安全性 |
|-------------------|--------|
| `transform: translate(-50%, -50%)` + absolute 居中 | 安全（dom-to-svg 精确计算） |
| `transform: scale(1.05)` hover 效果 | 安全（静态时 scale=1，不影响） |
| `transform: rotate(45deg)` 单独旋转 | 安全（dom-to-svg 计算最终坐标） |
| `transform: rotate() scale() translate()` 多重组合 | **有风险**（累积计算可能偏移） |

**HTML 写法约束**：CSS transform 尽量只用于简单的单一变换（居中定位最常见）。复杂的多重变换组合可能导致 dom-to-svg 计算偏移。

---

## 11. 底层氛围图

| 项目 | 规则 |
|------|------|
| opacity | 0.05 - 0.10（卡片内）/ 0.25 - 0.40（封面页） |
| 尺寸 | 限制在容器 40-60%，不要全覆盖 |
| z-index | 必须为 0 或 -1 |
| 实现方式 | 极低 opacity：直接 `<img>` + opacity |
| | 封面级渐隐：`<div>` 容器内 img + 遮罩 div |
| **禁止** | div 遮罩在 PPTX 中层叠不可靠时，回退到纯 opacity |

---

## 12. 配图技法管线安全等级

| 技法 | 管线安全 | 原因 |
|------|---------|------|
| 渐隐融合（div遮罩） | 安全 | 真实 div + linear-gradient |
| 色调蒙版 | 安全 | 真实 div + 半透明背景 |
| 氛围底图 | 最安全 | 纯 opacity |
| 裁切视窗 | 安全 | overflow:hidden + div 渐变 |
| 圆形裁切 | 安全 | border-radius |
| ~~CSS mask-image~~ | **禁止** | dom-to-svg 不支持 |

---

## 13. 总结：HTML 设计稿全管线 checklist

生成每页 HTML 时，对照以下分层清单：

### 13.1 管线红线（违反 = PPTX 输出异常）

- [ ] CSS 禁止清单中的特性未使用（第 1 节完整清单）
- [ ] 所有图片用 `<img>` 标签，不用 CSS background-image url()
- [ ] 内联 SVG 中**不含 `<text>` 元素**，所有文字标注用 HTML div 叠加
- [ ] 不同字号混排用 flex + 独立 span，不用嵌套 span
- [ ] 环形图用 stroke-dasharray 两值格式，不用 dashoffset
- [ ] 图例、x轴标签、数据标注全部用 HTML 元素，不用 SVG text
- [ ] 伪元素 `::before`/`::after` 装饰已用真实元素替代
- [ ] 内联 SVG path 只用 M/L/H/V/C/Z 命令，不用 S/Q/T/A
- [ ] 未使用 `<use>` / `<symbol>` / `<marker>` / `<pattern>` / `<clipPath>` / `<filter>` / `<mask>` 等不支持的 SVG 元素
- [ ] 未使用 clip-path CSS 属性
- [ ] 渐变 stroke 只用于"降级后也能接受"的装饰场景，关键描边用实色

### 13.2 精度约束（违反 = 可能偏移或丢失）

- [ ] 装饰性小元素尺寸 >= 4px（否则被 svg2pptx 静默丢弃）
- [ ] CSS transform 只用于简单单一变换（居中定位等），避免多重组合
- [ ] 字体 font-family 提供 fallback chain，末尾含通用族名
- [ ] 文字字号在 10-80px 范围内（超出范围偏移风险增大）
- [ ] 渐变 stop 数量 <= 5 个
- [ ] 底层配图用低 opacity `<img>` 或 div 遮罩

### 13.3 性能约束（违反 = PPTX 卡顿）

- [ ] 单页内联 SVG 图形元素总数 < 200
- [ ] 避免大量重复微小装饰元素（如 100+ 个背景圆点）
- [ ] 背景网格用 CSS 渐变实现，不用逐个 SVG 元素绘制
