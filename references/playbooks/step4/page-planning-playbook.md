# Page Planning Playbook

## 目标
制定一张从布局、字体、配图策略到卡片组织的 1280x720 物理画幅的精细蓝图。不写 HTML。

## 执行准则
1. 你的任务是填写完整的 `planning{n}.json`。
2. 调用 `resource_loader.py menu` 来理解各图表、布局组件能干什么，选出最合适的 `layout_hint`。
3. 如果本页需 AI 绘图，选择 `image.mode=generate` 并填入提示词供主控拦截（注意：你不能自己去画，你只是下单）。
4. 如果纯排版，选择 `image.mode=decorate`，必须指示下一环节的接引人如何用排版代替图。
5. 所有文本提炼后的内容需要填充在 JSON 中。

## 自审
- 你必须执行 `planning_validator.py`。
- 如果输出 ERROR 你的任务就不算完结，必须重新修复本地的 JSON 再测，直到完全消灭 ERROR（警告视情况可忽略）。
