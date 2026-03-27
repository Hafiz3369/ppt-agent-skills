# 智能配图系统

> 在需求调研（Step 1 语言与配图偏好）中确认用户的配图偏好后执行。如果用户选择"不需要配图"则跳过。

## 配图时机

在生成每页 HTML **之前**，先为该页生成配图。每页至少 1 张（封面页、章节封面必须有），生成后保存到 `OUTPUT_DIR/images/`。

## 核心原则

- 配图的目标是**精准表达该页内容的核心概念**，而不是生成一张"好看但空洞"的装饰图
- **图片语义合同由策划阶段生成**：策划师拥有最丰富的上下文（主题/受众/搜索素材/每页内容/布局），因此 Step 4 先写 card 级 `image` 语义字段：`needed` / `usage` / `placement` / `content_description` / `source_hint`
- **usage 由策划阶段决定**：图片在页面中扮演什么角色（背景/内容/装饰）写入 `image.usage` 字段
- Step 5b 基于上述语义合同和风格上下文派生真正的英文图片 prompt，再调用 `generate_image`；Step 5c 按 `image.usage` 消费图片

### 当前字段约定

- Step 4 planning 阶段必须先写：`needed` / `usage` / `placement` / `content_description` / `source_hint`
- Step 5b 配图阶段在此基础上补写：`path`
- 如果调用方能拿到更完整的生成元信息，也可继续补写：`prompt` / `alt_text` / `dimensions` / `aspect_ratio` / `format` / `style`
- Step 5c 只消费最终回填后的 `image` 对象，不要求重新猜测图片路径或生成参数

### 术语说明

- `image.usage` 是**运行时稳定枚举**，当前以 `prompt-3-planning.md` 中的字段定义为准
- `hero-blend`、`tint-overlay`、`atmosphere`、`split-content`、`card-inset`、`card-header`、`circle-badge` 这些词，在本文件中表示**设计技法名/构图昵称**
- 换句话说：`usage` 决定“这张图在页面里扮演什么角色”，技法名决定“这张图具体怎么融进去”
- 不要把技法名直接抄进 `image.usage` 字段，除非上游 schema 明确支持

---

## generate_image 调用规范

调用 `generate_image` 时：
- **Prompt**：由 Step 5b 根据 `content_description`、页面语义、图片角色和风格上下文按下方 6 维度公式构造，英文输出（图片生成模型对英文 prompt 效果最佳）
- **ImageName**：使用描述性命名，如 `cover_molecular_structure`、`section2_market_growth`

## Prompt 构造公式（6 维度）

```
[场景叙事] + [核心对象] + [视觉风格] + [构图与比例] + [光影氛围] + [质量锚定]
```

| 维度 | 权重 | 构造来源 | 说明 |
|------|------|---------|------|
| **场景叙事** | 最高 | 该页的 `goal` + `core_argument` | 从抽象概念翻译成具象画面。这是 prompt 质量的决定性维度 |
| **核心对象** | 高 | `emphasis_keywords` + `data_highlights` | 图片中必须出现的主体，具体到材质、形态、数量 |
| **视觉风格** | 中 | style.json 的配色方案和情感基调 | 确保图片色调与 PPT 整体风格协调 |
| **构图与比例** | 中 | 该图的 usage 类型决定 | 预留融入区域，确保裁切后主体不丢失 |
| **光影氛围** | 中 | 页面情感目标 + 风格基调 | 光线方向、明暗对比、景深，决定图片的"情绪" |
| **质量锚定** | 固定 | 每个 prompt 尾部必须追加 | 确保输出达到最高质量 |

## 质量锚定后缀（每个 prompt 必须附加）

```
8K resolution, ultra-detailed, photorealistic, cinematic lighting, masterpiece quality, no text, no watermark, no logo, no signature, sharp focus, professional photography
```

---

## 场景叙事的翻译方法（抽象 -> 具象）

这是最关键的维度。大多数 PPT 页面的概念是抽象的，但图片必须是具象的。以下是翻译思路的示范（不是固定映射，每次都应根据具体内容创造新的具象场景）：

| 抽象概念 | 具象化思路 |
|---------|----------|
| 增长/扩张 | 俯瞰城市天际线、破土而出的植物、向上延伸的阶梯 |
| 技术/架构 | 电路板微距、硅晶圆纹理、数据流光效 |
| 协作/团队 | 多人拼合的动作、交汇的光线、齿轮咬合 |
| 安全/信任 | 金属质感的穹顶、生物识别的光圈、水晶棱镜 |
| 创新/突破 | 破碎的玻璃天花板、穿越云层的光束、蝶变瞬间 |

> 每次翻译都应该独创 -- 如果所有"增长"类页面都用城市天际线，配图就失去了灵魂。

---

## 基于技法的构图自适应

不同技法对图片构图有不同要求。策划阶段构造 prompt 时，根据准备采用的融入技法调整构图描述：

| 技法名 | 构图方向 | prompt 中添加的构图关键词 |
|-------|---------|------------------------|
| `hero-blend` | 主体偏右，左侧留空渐隐区 | "main subject on right, left fading to empty, panoramic, 16:9" |
| `atmosphere` | 极低对比度，纹理质感 | "subtle texture, low contrast, ambient pattern, seamless, 16:9" |
| `tint-overlay` | 均匀分布，无强视觉焦点 | "evenly distributed, atmospheric background, 16:9" |
| `split-content` | 标准构图，主体清晰可见 | "balanced composition, main subject clearly visible, 4:3" |
| `card-inset` | 标准构图，上下可裁切 | "centered, main subject in middle third, 4:3" |
| `card-header` | 水平延展，上下可裁切 | "wide horizontal panoramic strip, elements centered vertically, 3:1" |
| `circle-badge` | 中心对称，主体居中 | "centered, circular framing, 1:1 square" |

---

## 风格与配图关键词对应

| PPT 风格 | 配图风格关键词 | 光影指导 |
|---------|--------------|---------| 
| 蓝白商务 | clean professional, soft blue tones, corporate | soft diffused daylight, gentle gradients |
| 极简灰白 | minimal, monochrome, geometric, academic | flat even lighting, high key |
| 暖色大地 | warm earth tones, cream and tan, terracotta, organic | soft ambient lighting, golden hour warmth |
| 清新自然 | fresh green, organic, nature, botanical | golden hour, dappled sunlight |
| 朱红宫墙 | traditional Chinese aesthetic, red and gold, ink wash | warm candlelight, atmospheric haze |
| 暗黑科技 | dark tech, neon glow, futuristic, cyberpunk | neon rim lighting, deep shadows |
| 紫金奢华 | luxury, deep purple and gold, metallic | dramatic chiaroscuro, golden highlights |
| 活力彩虹 | colorful, vibrant, energetic, pop art | bright even lighting, saturated colors |

---

## 配图融入设计 -- 7 种视觉融入技法

配图不能像贴纸一样硬塞在页面里。必须通过视觉融入技法让图片与内容浑然一体。

**核心原则**：图片是氛围的一部分，不是独立的内容块。

### 1. 渐隐融合 (`hero-blend`) -- 封面页/章节封面首选
图片占页面一侧，边缘用渐变遮罩层渐隐到背景色，让图片"消融"在背景中。图片不是被"放在"页面里，而是从页面边缘自然生长出来。

### 2. 色调蒙版 (`tint-overlay`) -- 内容页大卡片
图片上覆盖半透明色调层，让图片染上主题色，同时降低视觉干扰。文字在蒙版之上悬浮。

### 3. 氛围底图 (`atmosphere`) -- 章节封面/数据页
图片作为整页超低透明度背景（opacity 0.05-0.15），营造若有若无的氛围感。观众不会主动注意到它，但它在无意识层面营造了情绪底色。

### 4. 裁切视窗 (`card-header`) -- 小卡片顶部
图片作为卡片头部的"窗口"，底部渐隐到卡片背景。图片是卡片的"屋顶风景"。

### 5. 圆形/异形裁切 (`circle-badge`) -- 数据卡片辅助
图片裁切为圆形或其他形状，作为小型装饰元素。

### 6. 图文分栏 (`split-content`) -- 图片作为独立内容区
图片作为 Grid 中的一个独立子元素，与文字卡片并排。图片本身就是"内容"而非"装饰"。

### 7. 卡片内嵌 (`card-inset`) -- 图片+说明组合
图片嵌在卡片上半部分作为内容展示，下半部分是标题+说明。适合案例展示、产品截图、场景照片。

### 运行时 `usage` -> 可选技法速查

| `image.usage` 值 | 常见技法 | opacity 范围 | 典型场景 |
|------------------|---------|-------------|----------|
| `hero-background` | `hero-blend` / `tint-overlay` / `atmosphere` | 0.05-0.40 | 封面页 / 章节封面 / 大背景 |
| `data-visualization-bg` | `atmosphere` / `tint-overlay` | 0.05-0.30 | 数据页 / 英雄卡片背景 |
| `inline-illustration` | `split-content` / `card-inset` / `card-header` | 0.8-1.0 | 内容页图文并排 / 案例展示 / 卡片头图 |
| `icon-accent` | `circle-badge` | 0.8-1.0 | 小装饰元素 / 辅助视觉锚点 |

> **多样性约束**：整个 PPT 中，背景类和内容类 `usage` 都应出现；同一种 `usage` 之下也不要总是复用同一种技法。

---

## 图片 HTML 规范

- 图片可用 `<img>` 标签或 CSS `background-image`，按场景选择最佳方式
- 遮罩方式不限：`<div>` 遮罩层、`::before`/`::after` 伪元素、`mask-image` 均可
- `object-fit: cover`，`border-radius` 与容器一致
- 图片使用**绝对路径**（由 agent 生成图片后填入）

**避免**：
- 图片直接裸露无融入效果
- 图片占满卡片且无蒙版（文字不可读）
- 图片中出现文字（AI 生成的文字质量差）
- 与页面配色冲突的颜色
- 与内容无关的装饰图
- 重复使用相同 prompt
- 模糊泛指的 prompt -- 每个 prompt 必须包含至少 3 个具象物体/场景细节
- 省略质量锚定后缀
