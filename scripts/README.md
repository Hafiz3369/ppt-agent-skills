# Scripts Index

本目录只保留主链实际执行脚本。先看热路径，再看分组。

## 热路径

主控制台直接调用的脚本只有这些：

- `contract_validator.py`
- `progress_validator.py`
- `milestone_check.py`
- `subagent_prompt_assembler.py`
- `planning_validator.py`
- `prompt_assembler.py`
- `final_review_harness.py`
- `html_packager.py`
- `html2png.py`
- `html2svg.py`
- `png2pptx.py`
- `svg2pptx.py`

理解主链时先看这 12 个，不要先钻依赖子模块。

## 1. 主链 gate / 调度

- `contract_validator.py`
  - 节点合法性校验
  - 覆盖：`requirements` / `raw-research` / `research-package` / `outline-review` / `style` / `images`
- `progress_validator.py`
  - `progress.json` 生命周期与 Step 0 开工门槛校验
  - 支持 `--require-pre-step1` 启动前硬校验
- `milestone_check.py`
  - 按里程碑验收（只校验到指定 Step，不强求后续产物）
- `subagent_prompt_assembler.py`
  - 组装 research / material-prep / outline / outline-review / planning / style / image / html 的 runtime prompt 基座
  - 允许主 agent 追加运行上下文
- `workflow_versions.py`
  - 统一 workflow/schema version 常量

## 2. 策划与设计装配

- `planning_validator.py`
  - Step 4 planning JSON 单页 / 全量验证
- `prompt_assembler.py`
  - Step 5c 设计 prompt 装配
- `prompt_assembler_content.py`
  - `prompt_assembler.py` 的内容装配子模块
- `prompt_assembler_density.py`
  - `prompt_assembler.py` 的密度/场景装配子模块
- `resource_registry.py`
  - references 资源映射与 stage bundle 路由

这些属于依赖层，不应被误读为主控制台入口。

## 3. 终审与预览

- `final_review_harness.py`
  - Step 5d reviewer packet 组装与结果校验
- `html_packager.py`
  - 生成 `preview.html`

## 4. 导出

- `html2png.py`
- `html2svg.py`
- `png2pptx.py`
- `svg2pptx.py`

## 当前依赖关系

- `contract_validator.py` -> `planning_validator.py`
- `planning_validator.py` -> `resource_registry.py`, `workflow_versions.py`
- `prompt_assembler.py` -> `prompt_assembler_content.py`, `prompt_assembler_density.py`, `resource_registry.py`, `workflow_versions.py`

## 不应再出现的内容

以下内容不应再放在 `scripts/` 目录内：

- `scripts/` 下的 markdown 镜像副本目录（例如历史上的 scripts references 镜像目录）
- 历史 `orchestrator / packet_builder / dispatcher` 死代码
- 手工 copy 备份
- runtime 缓存（`__pycache__`）
