# 智能配图系统

> 在需求调研（Step 1 第 7 题）中确认用户的配图偏好后执行。如果用户选择"不需要配图"则跳过。

## 配图时机

在生成每页 HTML **之前**，先为该页生成配图。每页至少 1 张（封面页、章节封面必须有），生成后保存到 `OUTPUT_DIR/images/`。

## 核心原则

- 配图的目标是**精准表达该页内容的核心概念**，而不是生成一张"好看但空洞"的装饰图
- **prompt 由策划阶段生成**：策划师拥有最丰富的上下文（主题/受众/搜索素材/每页内容/布局），因此在 Step 4 策划每页时就将 prompt 写入 `planning{n}.json` 的 `image.prompt` 字段
- **usage 由策划阶段决定**：图片在页面中扮演什么角色（背景/内容/装饰）写入 `image.usage` 字段
- Step 5b 只是按 `image.prompt` 调用 `generate_image`，Step 5c 按 `image.usage` 消费图片

---

## generate_image 调用规范

调用 `generate_image` 时：
- **Prompt**：按下方 6 维度公式构造，英文输出（图片生成模型对英文 prompt 效果最佳）
- **ImageName**：使用描述性命名，如 `cover_molecular_structure`、`section2_market_growth`

## Prompt 构造公式（6 维度）

```
[场景叙事] + [核心对象] + [视觉风格] + [构图与比例] + [光影氛围] + [质量锚定]
```

**每个维度的构造方法**：

| 维度 | 权重 | 构造来源 | 说明 |
|------|------|---------|------|
| **场景叙事** | 最高 | 该页策划稿的 `goal` + `core_argument` | 描述一个具体的、可视化的场景，让图片"讲故事"而不是堆概念。要从抽象概念翻译成具象画面 |
| **核心对象** | 高 | 该页策划稿的 `emphasis_keywords` + `data_highlights` | 图片中必须出现的主体对象，具体到材质、形态、数量 |
| **视觉风格** | 中 | style.json 的配色方案和情感基调 | 确保图片色调与 PPT 整体风格协调 |
| **构图与比例** | 中 | 该图在页面中的放置方式（融入技法）决定 | 预留融入区域，确保图片裁切后主体不丢失 |
| **光影氛围** | 中 | 页面情感目标 + 风格基调 | 光线方向、明暗对比、景深，决定图片的"情绪" |
| **质量锚定** | 固定 | 每个 prompt 尾部必须追加 | 确保输出达到最高质量 |

## 质量锚定后缀（每个 prompt 必须附加）

```
8K resolution, ultra-detailed, photorealistic, cinematic lighting, masterpiece quality, no text, no watermark, no logo, no signature, sharp focus, professional photography
```

> 这段后缀是图片质量的保底措施。AI 图片生成模型对 "8K"、"ultra-detailed"、"masterpiece" 等关键词敏感度极高，能显著提升输出质量。

---

## 场景叙事的翻译方法（抽象 -> 具象）

这是最关键的维度。大多数 PPT 页面的概念是抽象的（"市场增长"、"技术架构"），但图片必须是具象的。AI 生成的图片质量 80% 取决于这一步描述得是否足够具体和有画面感。

**翻译对照表**（不要直接用左列的抽象词，而是翻译成右列的具象场景）：

| 抽象概念 | 具象场景翻译 |
|---------|-----------|
| 市场增长 | soaring glass skyscrapers reflecting golden sunrise, aerial cityscape view showing urban expansion |
| 技术架构 | intricate circuit board pathways glowing with data streams, macro photography of silicon wafer |
| 团队协作 | diverse hands assembling a complex jigsaw puzzle on a glass table, overhead shot |
| 用户体验 | person's hands interacting with a floating holographic interface, warm ambient lighting |
| 数据安全 | crystalline vault door with biometric scanner, cool blue steel environment |
| 可持续发展 | aerial view of solar farm merging into lush green forest, golden hour |
| 化学分析 | close-up of laboratory glassware with colored liquid refracting light, bokeh background |
| 供应链 | vast automated warehouse with robotic arms, precise geometric patterns, industrial scale |
| 创新突破 | shattered glass ceiling with brilliant light pouring through, dynamic particle effects |

---

## 基于 usage 的构图自适应

不同 usage 对图片的构图有不同要求。策划阶段构造 prompt 时，根据所选 usage 在 prompt 中明确描述构图方向：

| image.usage | 推荐构图 | 在 prompt 中添加 |
|-------------|---------|-----------------|
| `hero-blend` | 主体偏右，左侧留空渐隐区 | "main subject positioned on the right side, left side fading to empty space, wide panoramic composition, 16:9 aspect ratio" |
| `atmosphere` | 极低对比度，纹理质感 | "subtle texture, low contrast, ambient pattern, seamless, 16:9 aspect ratio" |
| `tint-overlay` | 均匀分布，无强视觉焦点 | "evenly distributed composition, atmospheric, suitable as background with overlay, 16:9 aspect ratio" |
| `split-content` | 标准构图，主体居中或偏一侧 | "balanced composition, main subject clearly visible, 4:3 aspect ratio" |
| `card-inset` | 标准构图，上下可裁切 | "centered composition, main subject in middle third, 4:3 aspect ratio" |
| `card-header` | 水平延展，上下可裁切 | "wide horizontal composition, important elements centered vertically, panoramic strip, 3:1 aspect ratio" |
| `circle-badge` | 中心对称，主体居中 | "centered composition, circular framing, subject fills frame, 1:1 square aspect ratio" |

---

## 风格与配图关键词对应

| PPT 风格 | 配图风格关键词 | 光影指导 |
|---------|--------------|---------|
| 蓝白商务 | clean professional, soft blue tones, corporate, minimal, bright studio lighting | soft diffused daylight, gentle gradients, clinical precision |
| 极简灰白 | minimal, monochrome, clean geometric, academic, architectural | flat even lighting, no dramatic shadows, high key |
| 小米橙 | minimal dark background, warm orange accent, clean product shot, studio | single strong side light, warm rim lighting, product photography |
| 清新自然 | fresh green, organic, nature, soft light, watercolor, botanical | golden hour, dappled sunlight through leaves, soft backlight |
| 朱红宫墙 | traditional Chinese aesthetic, elegant red and gold, ink wash painting, silk texture | warm candlelight, lantern glow, atmospheric haze |
| 暗黑科技 | dark tech background, neon glow, futuristic, digital, cyberpunk | neon rim lighting, deep shadows, volumetric light rays |
| 紫金奢华 | luxury, deep purple and gold, premium, elegant, metallic surfaces | dramatic chiaroscuro, golden specular highlights, studio glamour |
| 活力彩虹 | colorful, vibrant, energetic, playful, gradient, pop art, dynamic | bright even lighting, saturated colors, no harsh shadows |

---

## 按页面类型调整

| 页面类型 | 图片情感目标 | Prompt 额外关键词 |
|---------|-----------|-----------------|
| 封面页 | 视觉冲击、第一印象 | "hero image, dramatic composition, cinematic wide shot, awe-inspiring scale, epic atmosphere" |
| 章节封面 | 该章主题的象征性意象 | "symbolic, metaphorical, conceptual art, single powerful visual metaphor, contemplative mood" |
| 内容页 | 辅助理解，不喧宾夺主 | "supporting illustration, subtle detail, informative, explanatory visual" |
| 数据页 | 抽象数据的情感化表达 | "abstract data visualization aesthetic, flowing luminous lines, digital particle streams, mathematical beauty" |
| 结束页 | 总结回顾、展望未来 | "hopeful horizon, open vista, expansive sky, sense of possibility and accomplishment" |

---

## Prompt 正反面示例

**封面页 -- 主题"DMSO 在生物医药中的应用"，清新自然风格**

| | 示例 |
|---|------|
| **差** | "DMSO molecule, green background, medical, nature" |
| **好** | "Crystal clear laboratory flask containing purified DMSO solution refracting prismatic light, surrounded by fresh green botanical specimens and delicate molecular structure models floating in soft bokeh, close-up macro photography, golden hour sunlight streaming through clean glass, scientific elegance meets natural beauty, 16:9 aspect ratio, 8K resolution, ultra-detailed, photorealistic, cinematic lighting, masterpiece quality, no text, no watermark, sharp focus, professional photography" |

**内容页 -- 主题"市场规模达到 45 亿美元"，蓝白商务风格，用于色调蒙版**

| | 示例 |
|---|------|
| **差** | "market growth, business, blue, professional" |
| **好** | "Aerial view of a modern financial district at dawn, glass towers reflecting soft blue sky, subtle golden light on building tops suggesting growth and prosperity, clean geometric urban landscape, atmospheric perspective with gentle morning mist, evenly distributed composition suitable as background with overlay, 16:9 aspect ratio, 8K resolution, ultra-detailed, photorealistic, cinematic lighting, masterpiece quality, no text, no watermark, sharp focus, professional photography" |

---

## 配图融入设计（HTML 中如何嵌入配图）

配图不能像贴纸一样硬塞在页面里。必须通过**视觉融入技法**让图片与内容浑然一体。

**核心原则**：图片是**氛围的一部分**，不是独立的内容块。

> **SVG 管线兼容警告**：所有渐隐/遮罩效果必须用 **真实 `<div>` 遮罩层** 实现（`linear-gradient` 背景的 div 叠加在图片上方）。**禁止使用 CSS `mask-image` / `-webkit-mask-image`**，该属性在 dom-to-svg 转换中完全丢失。

### 5 种融入技法（全部管线安全）

#### 1. 渐隐融合 -- 封面页/章节封面的首选

图片占页面右半部分，左侧边缘用渐变遮罩渐隐到背景色，让图片"消融"在背景中。

```html
<div style="position:absolute; right:0; top:0; width:55%; height:100%; overflow:hidden;">
  <img src="..." style="width:100%; height:100%; object-fit:cover; opacity:0.35;">
  <!-- 左侧渐隐遮罩(真实div) -->
  <div style="position:absolute; left:0; top:0; width:60%; height:100%;
              background:linear-gradient(90deg, var(--bg-primary) 0%, transparent 100%);"></div>
</div>
```

#### 2. 色调蒙版 -- 内容页大卡片

图片上覆盖半透明色调层，让图片染上主题色，同时降低视觉干扰。

```html
<div style="position:relative; overflow:hidden; border-radius:var(--card-radius);">
  <img src="..." style="width:100%; height:100%; object-fit:cover; position:absolute; top:0; left:0;">
  <!-- 主题色蒙版 -->
  <div style="position:absolute; top:0; left:0; width:100%; height:100%;
              background:linear-gradient(135deg, rgba(11,17,32,0.85), rgba(15,23,42,0.6));"></div>
  <!-- 内容在蒙版之上 -->
  <div style="position:relative; z-index:1; padding:24px;">
    <!-- 文字内容 -->
  </div>
</div>
```

#### 3. 氛围底图 -- 章节封面/数据页

图片作为整页超低透明度背景，营造氛围感。

```html
<img src="..." style="position:absolute; top:0; left:0; width:100%; height:100%;
     object-fit:cover; opacity:0.08; pointer-events:none;">
```

#### 4. 裁切视窗 -- 小卡片顶部

图片作为卡片头部的"窗口"，用圆角裁切，底部渐隐到卡片背景。

```html
<div style="position:relative; height:120px; overflow:hidden;
            border-radius:var(--card-radius) var(--card-radius) 0 0;">
  <img src="..." style="width:100%; height:100%; object-fit:cover;">
  <div style="position:absolute; bottom:0; left:0; width:100%; height:50%;
              background:linear-gradient(0deg, var(--card-bg-from), transparent);"></div>
</div>
```

#### 5. 圆形/异形裁切 -- 数据卡片辅助

图片裁切为圆形或其他形状，作为装饰元素。

```html
<img src="..." style="width:80px; height:80px; border-radius:50%;
     object-fit:cover; border:3px solid var(--accent-1);">
```

#### 6. 图文分栏 -- 内容页「图片作为独立内容区」

图片作为 Bento Grid 中的一个独立 Grid 子元素，与文字卡片并排。在策划稿中用 `image_hero` card_type 占位。

```html
<!-- split-content: 图片作为一个 Grid 子元素，与其他卡片并排 -->
<div class="card" style="grid-row: 1 / -1; border-radius:12px; overflow:hidden; padding:0;">
  <img src="..." style="width:100%; height:100%; object-fit:cover;">
</div>
```

设计要点：
- 图片卡片 `padding:0`，图片贴边铺满
- 推荐用非对称两栏或主次结合布局，图片占一侧，另一侧放文字卡片
- 图片跨行（`grid-row: 1 / -1`）保持与所有卧卡片同高
- 图片透明度 1.0（不降透，作为内容展示）
- 圆角跟随卡片（`border-radius:12px + overflow:hidden`）

#### 7. 卡片内嵌配图 -- 内容页「图片+说明」

图片嵌在卡片上半部作为内容展示，下半部是标题+生成。与 card-header 的差异：图片占卡片面积更大（40-60%），是"内容展示"而非"装饰条"。

```html
<div class="card" style="border-radius:12px; overflow:hidden; padding:0;
                         display:flex; flex-direction:column;">
  <!-- 图片区，占卡片上半 -->
  <div style="height:55%; overflow:hidden;">
    <img src="..." style="width:100%; height:100%; object-fit:cover;">
  </div>
  <!-- 内容区，占卡片下半 -->
  <div style="padding:20px; flex:1;">
    <h3 style="margin:0 0 8px; font-size:18px;">...标题...</h3>
    <p style="margin:0; font-size:13px; color:var(--text-secondary);">...说明...</p>
  </div>
</div>
```

设计要点：
- 卡片 `padding:0`，图片贴边
- 图片区占卡片 40-60% 高度
- 内容区有独立的 `padding:20px`
- 图片透明度 1.0（内容展示用途）
- 适合案例展示、产品截图、场景照片等

### usage -> 技法快速映射

| image.usage 值 | 对应技法 | opacity 范围 | 典型场景 |
|----------------|---------|-------------|----------|
| `hero-blend` | 渐隐融合 | 0.25-0.40 | 封面页/章节封面 |
| `atmosphere` | 氛围底图 | 0.05-0.15 | 章节封面/数据页 |
| `tint-overlay` | 色调蒙版 | 0.15-0.30 | 英雄卡片/大卡片 |
| `split-content` | 图文分栏 | 0.8-1.0 | 内容页图文并排 |
| `card-inset` | 卡片内嵌 | 0.8-1.0 | 案例/产品/场景展示 |
| `card-header` | 裁切视窗 | 0.8-1.0 | 小卡片顶部装饰 |
| `circle-badge` | 圆形裁切 | 0.8-1.0 | 小装饰元素 |

> **多样性约束**：整个 PPT 中，背景类（hero-blend/atmosphere/tint-overlay）和内容类（split-content/card-inset）都应出现。不要所有页都用同一种 usage。

### 图片 HTML 规范
- 使用真实 `<img>` 标签（禁用 CSS background-image）
- 渐变遮罩用**真实 `<div>`**（禁用 ::before/::after）
- `object-fit: cover`，`border-radius` 与容器一致
- 图片使用**绝对路径**（由 agent 生成图片后填入）
- 底层氛围图的 opacity 必须足够低（0.05-0.15），尺寸限制在容器的 45-60%，避免遮挡前景内容

**禁止**：
- 禁止使用 CSS `mask-image` / `-webkit-mask-image`（SVG 转换后完全丢失，必须用 div 遮罩层替代）
- 禁止使用 `-webkit-background-clip: text`（SVG 中渐变变色块，必须用 `color` 直接上色）
- 禁止使用 `-webkit-text-fill-color`（SVG 不识别，必须用标准 `color` 属性）
- 禁止图片直接裸露在卡片角落（无融入效果）
- 禁止图片占据整个卡片且无蒙版（文字不可读）
- 禁止图片与背景色有明显的矩形边界线

---

## 禁止事项
- 禁止图片中出现文字（AI 生成的文字质量差）
- 禁止与页面配色冲突的颜色（暗色主题配暗色图，亮色主题配亮色图）
- 禁止与内容无关的装饰图（每张图必须与该页内容有语义关联）
- 禁止重复使用相同 prompt（每页图片必须独特）
- 禁止模糊泛指的 prompt（如"business illustration"、"technology background"）-- 每个 prompt 必须包含至少 3 个具象物体/场景细节
- 禁止省略质量锚定后缀
