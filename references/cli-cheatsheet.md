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

## Step 1 分支确认

主 agent 直接执行（无 subagent）：

1. 识别用户是否已提供现成资料（文件/文本/pptx）
2. 向用户确认分支选择：
   - **research 分支**：联网搜索后制作（→ Step 2A）
   - **非 research 分支**：基于用户现有资料制作（→ Step 2B）
3. 回填 `requirements-interview.txt` 中的 `分支` 字段：

```bash
# 用实际分支值替换 BRANCH_VALUE（research 或 非research）
# 直接在文件中找到 "- 分支：" 这一行并更新它
```

Gate 校验：

```bash
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
  --var TOOLS_AVAILABLE="由主 agent 根据感知结果动态填入可用的检索工具及其功能简述" \
  --var MAX_SEARCH_ROUNDS="主 agent 根据主题复杂度预估：简单2/中等3/高复杂4" \
  --var TARGET_PAGES="目标页数（来自采访）" \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/research-synth-playbook.md \
  --output OUTPUT_DIR/runtime/prompt-research-synth.md
```

Gate 校验通过后，主代理：
`唤起/创建 ResearchSynth Subagent 并显性赋予其参数 --model MAIN_MODEL`
`RUN OUTPUT_DIR/runtime/prompt-research-synth.md`

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py search OUTPUT_DIR/search.txt
python3 SKILL_DIR/scripts/contract_validator.py search-brief OUTPUT_DIR/search-brief.txt
```

> `CURRENT_BRIEF_PATH`（后续步骤用）= `OUTPUT_DIR/search-brief.txt`

---


## Step 2B 非 Search 分支（用户现有资料整合）

Prompt 生成：

```bash
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/tpl-source-synth.md \
  --var REQUIREMENTS_PATH=OUTPUT_DIR/requirements-interview.txt \
  --var SOURCE_INPUT=用户资料路径（目录或文件） \
  --var BRIEF_OUTPUT=OUTPUT_DIR/source-brief.txt \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/source-synth-playbook.md \
  --output OUTPUT_DIR/runtime/prompt-source-synth.md
```

主代理执行：
`依据《Subagent 操作手册》唤起/创建 SourceSynth Subagent 并显性赋予主要模型参数 --model MAIN_MODEL`
`对该代理发送 RUN OUTPUT_DIR/runtime/prompt-source-synth.md 指令`

Gate 校验：

```bash
python3 SKILL_DIR/scripts/contract_validator.py source-brief OUTPUT_DIR/source-brief.txt
```

> `CURRENT_BRIEF_PATH`（后续步骤用）= `OUTPUT_DIR/source-brief.txt`



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
主代理：
`唤起/创建 Outline Subagent 并显性赋予其参数 --model MAIN_MODEL`
`RUN OUTPUT_DIR/runtime/prompt-outline.md`

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

## Step 4 单页生产（双模式：按环境感知选择执行后端）

> **模式判定**：Section 3.1 环境感知时确定，写入《Subagent 操作手册》。
> - **Codex 模式**：subagent 支持 session 续写 → 4A/4B/4C 分三次注入同一 session
> - **Claude 模式**：subagent 不支持可靠续写 → 三份 prompt 合并为单次 PageAgent 端到端完成

---

### 4A. Planning 阶段

**生成 prompt 文件：**

```bash
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/step4/tpl-page-planning.md \
  --var PAGE_NUM=N \
  --var TOTAL_PAGES=TOTAL \
  --var REQUIREMENTS_PATH=OUTPUT_DIR/requirements-interview.txt \
  --var OUTLINE_PATH=OUTPUT_DIR/outline.txt \
  --var BRIEF_PATH=CURRENT_BRIEF_PATH \
  --var STYLE_PATH=OUTPUT_DIR/style.json \
  --var IMAGES_DIR=OUTPUT_DIR/images \
  --var PLANNING_OUTPUT=OUTPUT_DIR/planning/planningN.json \
  --var SKILL_DIR=SKILL_DIR \
  --var REFS_DIR=SKILL_DIR/references \
  --inject-file PRINCIPLES_CHEATSHEET=SKILL_DIR/references/principles/design-principles-cheatsheet.md \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/step4/page-planning-playbook.md \
  --output OUTPUT_DIR/runtime/prompt-page-planning-N.md
```

**[Codex 模式] 启动 PageAgent-N（新建 session）：**

主代理执行：
`依据《Subagent 操作手册》唤起/创建 PageAgent-N 并显性赋予主要模型参数 --model MAIN_MODEL`
`对该代理发送 RUN OUTPUT_DIR/runtime/prompt-page-planning-N.md 指令`

**[Claude 模式] 见底部「Claude 模式：单次 PageAgent 端到端」节。**

Gate 校验（Codex 模式收到 FINALIZE 后执行；Claude 模式在整页终检时统一执行）：

```bash
test -s OUTPUT_DIR/planning/planningN.json
python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning --refs SKILL_DIR/references --page N
```

---

### 4B. HTML 阶段

**生成 prompt 文件：**

```bash
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/step4/tpl-page-html.md \
  --var PAGE_NUM=N \
  --var TOTAL_PAGES=TOTAL \
  --var PLANNING_OUTPUT=OUTPUT_DIR/planning/planningN.json \
  --var SLIDE_OUTPUT=OUTPUT_DIR/slides/slide-N.html \
  --var IMAGES_DIR=OUTPUT_DIR/images \
  --var STYLE_PATH=OUTPUT_DIR/style.json \
  --var SKILL_DIR=SKILL_DIR \
  --var REFS_DIR=SKILL_DIR/references \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/step4/page-html-playbook.md \
  --output OUTPUT_DIR/runtime/prompt-page-html-N.md
```

**[Codex 模式] 对同一 PageAgent-N session 续写发送后续指令：**

主代理执行：
`针对当前 PageAgent-N session 发送后续指令`
`RUN OUTPUT_DIR/runtime/prompt-page-html-N.md`

Gate 校验：

```bash
test -s OUTPUT_DIR/slides/slide-N.html
```

---

### 4C. Review 阶段

**生成 prompt 文件：**

```bash
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/step4/tpl-page-review.md \
  --var PAGE_NUM=N \
  --var TOTAL_PAGES=TOTAL \
  --var PLANNING_OUTPUT=OUTPUT_DIR/planning/planningN.json \
  --var SLIDE_OUTPUT=OUTPUT_DIR/slides/slide-N.html \
  --var PNG_OUTPUT=OUTPUT_DIR/png/slide-N.png \
  --var STYLE_PATH=OUTPUT_DIR/style.json \
  --var SKILL_DIR=SKILL_DIR \
  --inject-file PLAYBOOK=SKILL_DIR/references/playbooks/step4/page-review-playbook.md \
  --inject-file FAILURE_MODES=SKILL_DIR/references/principles/runtime-failure-modes.md \
  --output OUTPUT_DIR/runtime/prompt-page-review-N.md
```

**[Codex 模式] 对同一 PageAgent-N session 再次续写发送审查指令：**

主代理执行：
`针对当前 PageAgent-N session 发送后续审查指令`
`RUN OUTPUT_DIR/runtime/prompt-page-review-N.md`

Gate 校验：

```bash
test -s OUTPUT_DIR/png/slide-N.png
```

---

### Claude 模式：渐进式上下文注入（单次 PageAgent 端到端）

> 当环境感知判定为 Claude 模式时，**跳过上面的分段注入流程**，改用以下方式。
> 核心区别：不把三份 prompt 全文一次性塞给 subagent，而是通过轻量 orchestrator 让 subagent **内部自主按阶段读取**。

**第一步**：依次执行上面 4A/4B/4C 三个 harness 命令，生成三份阶段 prompt 文件：
- `OUTPUT_DIR/runtime/prompt-page-planning-N.md`
- `OUTPUT_DIR/runtime/prompt-page-html-N.md`
- `OUTPUT_DIR/runtime/prompt-page-review-N.md`

**第二步**：生成 orchestrator 调度 prompt（轻量，只含路径和执行协议）：

```bash
python3 SKILL_DIR/scripts/prompt_harness.py \
  --template SKILL_DIR/references/prompts/step4/tpl-page-orchestrator.md \
  --var PAGE_NUM=N \
  --var TOTAL_PAGES=TOTAL \
  --var PLANNING_PROMPT_PATH=OUTPUT_DIR/runtime/prompt-page-planning-N.md \
  --var HTML_PROMPT_PATH=OUTPUT_DIR/runtime/prompt-page-html-N.md \
  --var REVIEW_PROMPT_PATH=OUTPUT_DIR/runtime/prompt-page-review-N.md \
  --var PLANNING_OUTPUT=OUTPUT_DIR/planning/planningN.json \
  --var SLIDE_OUTPUT=OUTPUT_DIR/slides/slide-N.html \
  --var PNG_OUTPUT=OUTPUT_DIR/png/slide-N.png \
  --output OUTPUT_DIR/runtime/prompt-page-orchestrator-N.md
```

**第三步**：创建单个 PageAgent-N，**只发送 orchestrator prompt**：

主代理执行：
`依据《Subagent 操作手册》唤起/创建 PageAgent-N 并显性赋予主要模型参数 --model MAIN_MODEL`
`RUN OUTPUT_DIR/runtime/prompt-page-orchestrator-N.md`

> subagent 内部会按 orchestrator 的指示自主渐进：
> 1. 先读 planning prompt → 完成策划 → 产出 planningN.json
> 2. 自主读 html prompt → 完成设计稿 → 产出 slide-N.html
> 3. 自主读 review prompt → 截图审查修复 → 产出 slide-N.png
> 4. 三件套齐全后 FINALIZE

**第四步**：回收 FINALIZE 后，主 agent 执行**整页终检**：

```bash
test -s OUTPUT_DIR/planning/planningN.json
python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning --refs SKILL_DIR/references --page N
test -s OUTPUT_DIR/slides/slide-N.html
test -s OUTPUT_DIR/png/slide-N.png
```

---

### Step 4 失败重试指南

**触发条件（任一成立）：**
- `slide-N.html` 不存在或为空
- `slide-N.png` 视觉审查不通过

**无论同对话还是跨对话，统一两步走：**

**第一步：侦查** — 读 `outline.txt` 确认总页数，遍历所有页收集缺失页列表：

```bash
# 对每页 1..N：
test -s OUTPUT_DIR/planning/planningN.json && \
test -s OUTPUT_DIR/slides/slide-N.html && \
test -s OUTPUT_DIR/png/slide-N.png && \
python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning --refs SKILL_DIR/references --page N
# exit≠0 → 加入缺失页列表
```

**第二步：并行重跑** — 收集完毕，一次性并行启动所有缺失页（不串行逐页）：

```bash
# 对缺失页列表 [N1, N2, ...] 中每页，清理旧产物：
python3 -c "import os; [os.remove(p) for p in ['OUTPUT_DIR/planning/planningN.json','OUTPUT_DIR/slides/slide-N.html','OUTPUT_DIR/png/slide-N.png'] if os.path.exists(p)]"
# 基于《Subagent 操作手册》并行发起所有对应的 PageAgent-N（各自新建 session，4A→4B→4C）
```

> session 一律视为不可续接（subagent 死亡=上下文全无），整页从 4A 开始重跑。  
> 跨对话恢复时旧 session 全部失效，逻辑相同。

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
# 主 agent 按以下 schema 写入 delivery-manifest.json
```

**delivery-manifest.json 必填 schema**：

```json
{
  "run_id": "RUN_ID（与 OUTPUT_DIR 对应）",
  "generated_at": "ISO 8601 时间戳（如 2026-04-01T14:30:00Z）",
  "summary": {
    "total_pages": 页数（正整数）
  },
  "artifacts": {
    "preview_html": "preview.html（相对于 OUTPUT_DIR 的路径）",
    "presentation_png_pptx": "presentation-png.pptx",
    "presentation_svg_pptx": "presentation-svg.pptx"
  },
  "pages": [
    { "page": 1, "planning": "planning/planning1.json", "html": "slides/slide-1.html", "png": "png/slide-1.png" }
  ]
}
```

> `run_id`、`generated_at`、`artifacts`（含三个路径）为 validator 强制校验字段；`summary` 和 `pages` 建议填写。

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
