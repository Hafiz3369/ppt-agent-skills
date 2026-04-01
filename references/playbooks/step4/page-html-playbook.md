# Page HTML Playbook

## 目标
忠实还原 planning JSON 里的骨架与精神，运用 `resource_loader.py` 的解析能力，将抽象组件组装成极具高级设计感的单页自包含 HTML。

## 执行准则

1. 画布物理红线不可违反：body 必须 `width: 1280px; height: 720px; overflow: hidden;`，绝对不用 100% 然后外层缩放。
2. 所有组件的正文必须通过下述命令获取：
   `python3 SKILL_DIR/scripts/resource_loader.py resolve --refs-dir REFS_DIR --planning PLANNING_OUTPUT`
   里面有着最精确的骨架建议和 CSS 参数，照做但可微调。
3. 从 `style.json` 拉取颜色和全局氛围，写在 HTML head 内。坚决保证单文件自闭环。不准外挂 CSS。
4. 如果 Planning 中的 `image.mode` 是 generate 或 provided，这意味着图片清单 (`resource_loader.py images`) 中**必然应该有图**供你绑在 `src` 或 `background` 上。如果 `image.mode` 是 decorate，坚决不留空白狗皮膏药图，必须内联 SVG、色块、甚至纯文字排版。

## 结束
文件生成并落盘后即可提交结果。你不负责做图审与截图（那是 Review/QA Agent 的活）。只要确信你的 HTML 代码没有任何缺漏、乱码、缺合规标签的小毛病即可放行。
