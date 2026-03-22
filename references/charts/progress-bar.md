# 进度条（百分比/完成度）

`chart_type: progress_bar`

```css
.progress-bar {
  height: 8px; border-radius: 4px;
  background: var(--card-bg-from);
  overflow: hidden;
}
.progress-bar .fill {
  height: 100%; border-radius: 4px;
  background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
  /* width 用内联 style 设置百分比 */
}
```
