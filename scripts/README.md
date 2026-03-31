# Scripts Index

本目录包含 PPT 工作流的全部执行脚本。

## 核心调度

| 脚本 | 用途 | 调用方 |
|------|------|--------|
| `prompt_harness.py` | 模板变量填充，生成 subagent prompt | 主 agent |
| `resource_loader.py` | 资源路由器（menu 菜单 / resolve 按需加载） | subagent |

## 校验工具

| 脚本 | 用途 | 调用方 |
|------|------|--------|
| `contract_validator.py` | 合同校验（interview/search/outline/style/review/manifest） | 主 agent |
| `planning_validator.py` | Step 4 planning JSON 单页/全量验证 | subagent 自审 |
| `progress_validator.py` | progress.json 生命周期校验 | 主 agent |
| `milestone_check.py` | 按里程碑阶段验收 | 主 agent |

## 导出工具

| 脚本 | 用途 |
|------|------|
| `html_packager.py` | 生成 preview.html |
| `html2png.py` | HTML -> PNG 截图 |
| `html2svg.py` | HTML -> SVG 转换 |
| `png2pptx.py` | PNG -> PPTX 导出 |
| `svg2pptx.py` | SVG -> PPTX 导出 |

## 辅助

| 脚本 | 用途 |
|------|------|
| `workflow_versions.py` | 统一 workflow/schema version 常量 |

## 依赖关系

```
prompt_harness.py       -- 独立
resource_loader.py      -- 独立
contract_validator.py   -> planning_validator.py -> workflow_versions.py
progress_validator.py   -- 独立
milestone_check.py      -- 独立
```
