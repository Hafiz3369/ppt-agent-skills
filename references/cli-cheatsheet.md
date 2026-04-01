# CLI 速查表

> 按步骤组织的完整命令手册。执行时用实际路径替换 `SKILL_DIR` / `OUTPUT_DIR` 等变量。
> 主 agent 进入 Step 0 前必须读取此文件建立接口认知。禁止对任何脚本跑 `--help`。

---

## Step 0 采访

Prompt 生成（可选，主 agent 也可直接发问）：

```bash
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/tpl-interview.md \
  --var TOPIC="用户主题" \
  --var USER_CONTEXT="用户已提供的背景信息" \
  --output OUTPUT_DIR/runtime/prompt-interview.md
```

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py interview OUTPUT_DIR/interview-qa.txt
python3 SKILL_DIR/scripts/contract_validator.py requirements-interview OUTPUT_DIR/requirements-interview.txt
```

---

## Step 2A Research

Prompt 生成：

```bash
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/tpl-research-synth.md \
  --var TOPIC="主题" \
  --var REQUIREMENTS_PATH=OUTPUT_DIR/requirements-interview.txt \
  --var SEARCH_OUTPUT=OUTPUT_DIR/search.txt \
  --var BRIEF_OUTPUT=OUTPUT_DIR/search-brief.txt \
  --var TOOLS_AVAILABLE="从环境感知 Search 工具清单取值，如: search_web,read_url_content,grok-search" \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/research-synth-playbook.md \
  --output OUTPUT_DIR/runtime/prompt-research-synth.md
```

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py search OUTPUT_DIR/search.txt
python3 SKILL_DIR/scripts/contract_validator.py search-brief OUTPUT_DIR/search-brief.txt
```

---

## Step 2B 非 Search 分支

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py source-brief OUTPUT_DIR/source-brief.txt
```

---

## Step 3 大纲

Prompt 生成：

```bash
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/tpl-outline.md \
  --var REQUIREMENTS_PATH=OUTPUT_DIR/requirements-interview.txt \
  --var BRIEF_PATH=CURRENT_BRIEF_PATH \
  --var OUTLINE_OUTPUT=OUTPUT_DIR/outline.txt \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/outline-subagent-playbook.md \
  --output OUTPUT_DIR/runtime/prompt-outline.md
```

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py outline OUTPUT_DIR/outline.txt
```

---

## Step 3.5 风格

Prompt 生成：

```bash
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/tpl-style.md \
  --var REQUIREMENTS_PATH=OUTPUT_DIR/requirements-interview.txt \
  --var OUTLINE_PATH=OUTPUT_DIR/outline.txt \
  --var SKILL_DIR=SKILL_DIR \
  --var STYLE_OUTPUT=OUTPUT_DIR/style.json \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/style-subagent-playbook.md \
  --inject-file STYLE_RUNTIME_RULES=SKILL_DIR/references/styles/runtime-style-rules.md \
  --inject-file STYLE_PRESET_INDEX=SKILL_DIR/references/styles/runtime-style-palette-index.md \
  --output OUTPUT_DIR/runtime/prompt-style.md
```

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py style OUTPUT_DIR/style.json
```

---

## Step 4 单页生产

Prompt 生成（每页一次，N 替换为页码，TOTAL 替换为总页数）：

```bash
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/tpl-page-agent.md \
  --var PAGE_NUM=N \
  --var TOTAL_PAGES=TOTAL \
  --var REQUIREMENTS_PATH=OUTPUT_DIR/requirements-interview.txt \
  --var OUTLINE_PATH=OUTPUT_DIR/outline.txt \
  --var BRIEF_PATH=CURRENT_BRIEF_PATH \
  --var STYLE_PATH=OUTPUT_DIR/style.json \
  --var IMAGES_DIR=OUTPUT_DIR/images \
  --var PLANNING_OUTPUT=OUTPUT_DIR/planning/planningN.json \
  --var SLIDE_OUTPUT=OUTPUT_DIR/slides/slide-N.html \
  --var PNG_OUTPUT=OUTPUT_DIR/png/slide-N.png \
  --var SKILL_DIR=SKILL_DIR \
  --var REFS_DIR=SKILL_DIR/references \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/page-agent-playbook.md \
  --output OUTPUT_DIR/runtime/prompt-page-N.md
```

Gate 校验（每页）：

```bash
test -s OUTPUT_DIR/planning/planningN.json
python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning --refs SKILL_DIR/references --page N
test -s OUTPUT_DIR/slides/slide-N.html
test -s OUTPUT_DIR/png/slide-N.png
```

---

## Step 5 导出

执行管线：

```bash
# 1. 预览
python3 SKILL_DIR/scripts/html_packager.py OUTPUT_DIR/slides -o OUTPUT_DIR/preview.html

# 2. PNG 管线（与 SVG 并行）
python3 SKILL_DIR/scripts/html2png.py OUTPUT_DIR/slides -o OUTPUT_DIR/png --scale 2
python3 SKILL_DIR/scripts/png2pptx.py OUTPUT_DIR/png -o OUTPUT_DIR/presentation-png.pptx

# 3. SVG 管线（与 PNG 并行）
python3 SKILL_DIR/scripts/html2svg.py OUTPUT_DIR/slides -o OUTPUT_DIR/svg
python3 SKILL_DIR/scripts/svg2pptx.py OUTPUT_DIR/svg -o OUTPUT_DIR/presentation-svg.pptx --html-dir OUTPUT_DIR/slides

# 4. 交付清单
# 主 agent 写入 delivery-manifest.json
```

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py delivery-manifest OUTPUT_DIR/delivery-manifest.json --base-dir OUTPUT_DIR
```

---

## 资源路由

菜单（planning 阶段）：

```bash
python3 SKILL_DIR/scripts/resource_loader.py menu --refs-dir SKILL_DIR/references
```

解析（html 阶段）：

```bash
python3 SKILL_DIR/scripts/resource_loader.py resolve --refs-dir SKILL_DIR/references --planning OUTPUT_DIR/planning/planningN.json
```

图片清单（planning / html 阶段）：

```bash
python3 SKILL_DIR/scripts/resource_loader.py images --images-dir OUTPUT_DIR/images
```

---

## 里程碑总验收

```bash
python3 SKILL_DIR/scripts/milestone_check.py <stage> --output-dir OUTPUT_DIR
```

---

## 合同校验器 contract-type 列表

`interview` / `requirements-interview` / `search` / `search-brief` / `source-brief` / `outline` / `style` / `images` / `page-review` / `delivery-manifest`

通用格式：

```bash
python3 SKILL_DIR/scripts/contract_validator.py <contract-type> <target-file> [--base-dir OUTPUT_DIR]
```
