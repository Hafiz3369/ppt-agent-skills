# 采访问卷共享核心

> 本文件是 Step 0 的共享采访内容合同，不直接作为运行时 prompt 发给主 agent。
> 运行时应按能力选择：
> - `tpl-interview-structured-ui.md`
> - `tpl-interview-text-fallback.md`

## 采访目标

- 用尽量少的轮次拿到足够稳定的 PPT 生产输入
- 优先收集会影响大纲、风格、配图、分支选择的高信号维度
- 已知信息只做确认，不机械重复
- 即使是 text-fallback，也必须保持字段化和分组感

## 必须覆盖的 4 组维度

### A. 场景与目标

- `presentation_scenario`：这份 PPT 用于什么场景
  推荐选项：新人介绍 / 内部汇报 / 社区宣讲 / 招商合作 / 其他
- `core_audience`：谁会看，关注点是什么
  推荐选项：社区新人 / 技术同好 / 团队管理者 / 合作方 / 混合受众
- `target_action`：希望观众看完后做什么
  推荐选项：建立认知 / 愿意加入 / 愿意传播 / 愿意合作 / 仅完成汇报

### B. 内容与边界

- `page_density`：页数与密度
  推荐选项：少而精 / 适中 / 信息量大
- `must_include`：必须出现的信息
- `must_avoid`：必须回避的信息
- `materials_strategy`：资料使用策略与分支
  推荐选项：research / 非 research

### C. 风格与素材

- `visual_style`：整体风格
  推荐选项：科技社区感 / 极客感 / 简洁商务感 / 自动匹配
- `brand_constraints`：品牌色、logo、禁忌风格等限制
- `language_mode`：语言
  推荐选项：中文 / 英文 / 中英混排
- `imagery_strategy`：配图策略
  推荐选项：decorate / generate / provided / manual_slot
- `presenter_meta`：封面署名、日期、组织信息等

### D. 成功标准与执行

- `success_criteria`：用户如何判断这份 PPT 成功
- `subagent_model_strategy`：子代理模型是否跟主代理一致

## 归一化落点

- `interview-qa.txt`：保留原始问答语境
- `requirements-interview.txt`：写成机器消费格式

`requirements-interview.txt` 至少要能稳定落到这些字段：

- `场景`
- `受众`
- `目标动作`
- `页数与密度`
- `风格`
- `品牌`
- `必含内容`
- `必避内容`
- `配图`
- `资料使用策略`
- `备注/交付预期`
