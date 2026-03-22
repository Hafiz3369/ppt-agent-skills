# PPT 设计原则

> 这些是演示设计领域公认的底层原则。理解"为什么"才能在没有具体规则覆盖时做出正确判断。

## 原则索引

| 文件 | 核心原则 | 来源/理论 |
|------|---------|----------|
| `visual-hierarchy.md` | 视觉层级与 CRAP | Robin Williams《写给大家看的设计书》 |
| `cognitive-load.md` | 认知负荷与信息密度 | Miller's Law / Mayer 多媒体学习理论 |
| `composition.md` | 构图与留白 | 三分法 / 格式塔心理学 |
| `color-psychology.md` | 色彩心理与运用 | 60-30-10 法则 / 色彩情感映射 |
| `data-visualization.md` | 数据可视化原则 | Edward Tufte / Stephen Few |
| `narrative-arc.md` | 叙事结构与节奏 | 金字塔原理 / SCQA / 故事弧线 |

## 何时读取

- **Step 4（策划阶段）首页前**：读取 `README.md`（本文件）建立原则意识
- **Step 5c（设计阶段）**：遇到设计决策犹豫时，按需读取对应原则文件
- 不需要每次全部读取，原则是**指导框架**而非逐条检查清单

## 与具体规则的关系

```
原则层（principles/）   = "为什么这样做"  -> 指导判断
规则层（prompt-4）       = "怎么做"        -> 具体执行
组件层（blocks/charts/） = "用什么做"      -> 工具选择
```

原则指导规则，规则约束执行。当规则没有覆盖的场景出现时，回到原则层思考。
