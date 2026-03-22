# PPT Agent Skill

**[中文文档](README.md)**

> A professional AI-powered presentation generation assistant that simulates the complete workflow of a top-tier PPT design company (quoted at $1,000+/page), outputting high-quality HTML presentations + dual-pipeline PPTX.

## Workflow

```
Requirements Interview → Research → Outline → Planning Draft (with Image Strategy) → Style + Images + HTML Design → Post-processing (PNG/SVG → PPTX)
```

## Key Features

| Feature | Description |
|---------|-------------|
| **6-Step Pipeline** | Requirements → Research → Outline → Planning → Design → Post-processing |
| **Modular Prompt System** | 5 independent prompt modules (Research/Outline/Planning/Design/Notes), loaded on demand |
| **Resource Registry** | `resource-registry.md` — single source of truth for all resource mappings |
| **8 Preset Styles** | Dark Tech / Xiaomi Orange / Blue White / Royal Red / Fresh Green / Luxury Purple / Minimal Gray / Vibrant Rainbow |
| **10 Layout System** | Bento Grid card-based layouts + symmetric/asymmetric/L-shape/T-shape/waterfall/hero variants |
| **Multi Card Styles** | 6 card_style options (filled/transparent/outline/accent/glass/elevated) to break visual monotony |
| **Smart Image Strategy** | Image usage (background/split-content/card-inset), prompts & placement decided at planning stage |
| **Decoration Toolkit** | 5 visual fusion techniques (fade blend, tinted overlay, ambient background, split-content, card-inset) |
| **Typography System** | 7-level font scale + spacing hierarchy + CJK mixed typesetting rules |
| **Color Proportion** | 60-30-10 rule enforcement + accent color constraints |
| **Data Visualization** | 13 pure CSS/SVG chart types (progress bars, ring charts, sparklines, waffle, KPI, radar, funnel, etc.) |
| **Building Blocks** | 9 reusable HTML blocks (timeline, people cards, comparison, matrix, quotes, icon groups, etc.) |
| **Design Principles** | 6 design principle references (cognitive load, color psychology, composition, data viz, narrative arc, visual hierarchy) |
| **Cross-page Narrative** | Density alternation, chapter color progression, cover-ending visual echo |
| **Quality Baseline** | Independent quality checklist for consistent output |
| **Dual Pipeline PPTX** | PNG pipeline (max compatibility) + SVG pipeline (editable text), user-selectable |

## Output

| File | Description |
|------|-------------|
| `preview.html` | Browser-based paginated preview (auto-generated) |
| `presentation.pptx` | PPTX file (PNG pipeline: ready to use; SVG pipeline: right-click "Convert to Shape" in PPT 365) |
| `png/*.png` | Per-page PNG screenshots (PNG pipeline output) |
| `svg/*.svg` | Per-page vector SVG (SVG pipeline output) |
| `slides/*.html` | Per-page HTML source files |

## Requirements

**Required:**
- **Node.js** >= 18 (Puppeteer + dom-to-svg)
- **Python** >= 3.8
- **python-pptx** (PPTX generation)

**Quick Install:**
```bash
pip install python-pptx lxml Pillow
npm install puppeteer dom-to-svg
```

## Directory Structure

```
ppt-agent-skill/
  SKILL.md                    # Main workflow instructions (Agent entry point)
  README.md                   # Chinese documentation (default)
  README_EN.md                # This file
  references/
    resource-registry.md      # Resource registry (single source of truth)
    quality-baseline.md       # Quality baseline checklist
    narrative-rhythm.md       # Narrative rhythm & visual weight
    image-generation.md       # Image strategy + fusion techniques + decoration toolkit
    pipeline-compat.md        # Pipeline compatibility constraints
    prompts/                  # Modular prompts (5 independent modules)
      prompt-1-research.md    #   Research prompt
      prompt-2-outline.md     #   Outline prompt
      prompt-3-planning.md    #   Planning prompt (with image field spec)
      prompt-4-design.md      #   Design prompt (with animation lib + resource menu)
      prompt-5-notes.md       #   Speaker notes prompt
      animations.md           #   Animation effects library
    styles/                   # 8 preset styles (individual files + README decision rules)
    layouts/                  # 10 layouts (individual files + README canvas params)
    charts/                   # 13 chart templates (individual files + README selection guide)
    icons/                    # 4 SVG icon categories (individual files + README usage rules)
    blocks/                   # 9 building blocks (timeline, people, comparison, matrix, etc.)
    page-templates/           # Cover/TOC/Section/End page templates
    principles/               # 6 design principles (cognitive load, color psychology, etc.)
  scripts/
    html_packager.py          # Merge multi-page HTML into paginated preview
    html2svg.py               # HTML → SVG (dom-to-svg, preserves editable text)
    html2png.py               # HTML → PNG (Puppeteer screenshot)
    svg2pptx.py               # SVG → PPTX (OOXML native SVG embedding)
    png2pptx.py               # PNG → PPTX (image embedding, max compatibility)
```

## Usage

Just describe your needs in the conversation to trigger the skill. The Agent will automatically execute the full 6-step workflow:

```
You: "Make a PPT about X"
  → Agent interviews you for requirements (waits for your reply)
  → Auto research → outline → planning draft (with image strategy)
  → Per-page HTML design (generates images per planning strategy)
  → Auto post-processing: HTML → PNG/SVG → PPTX
  → All outputs saved to ppt-output/
```

**Trigger Examples**:

| Scenario | What to Say |
|----------|-------------|
| Topic only | "Make a PPT about X" / "Create a presentation on Y" |
| With source material | "Turn this document into slides" / "Make a PPT from this report" |
| With requirements | "15-page dark tech style AI safety presentation" |
| Implicit trigger | "I need to present to my boss about Y" / "Make training materials" |

> No manual script execution needed. All post-processing (preview merge, PNG/SVG conversion, PPTX generation) is handled automatically by the Agent in Step 6.

## Technical Architecture

```
HTML slides
  ├─ [PNG Pipeline] → Puppeteer screenshot → PNG → python-pptx embed → PPTX (max compatibility)
  └─ [SVG Pipeline] → dom-to-svg → SVG → python-pptx + lxml → PPTX (editable text)
```

## Changelog

### v2.0 — Modular Refactor + Image Strategy Upgrade (2026-03-22)

**Architecture-level Refactor:**
- **Modular Prompt System**: Monolithic `prompts.md` (900+ lines) split into 5 independent prompt modules + animation library, loaded on demand
- **Resource Registry**: New `resource-registry.md` as single source of truth for all resource mappings, eliminating scattered duplicate references
- **Quality Baseline**: New `quality-baseline.md` independent quality checklist

**New Resource Libraries (6 modules):**
- **Building Blocks** `blocks/`: 9 reusable HTML blocks (timeline, people cards, comparison, matrix, quotes, icon groups, etc.)
- **Design Principles** `principles/`: 6 design principle references (cognitive load, color psychology, composition, data visualization, narrative arc, visual hierarchy)
- **Icon Reference** `icons/`: 4 SVG icon categories (content concepts, data analytics, industry scenarios, process structure)
- **Chart Templates** `charts/`: 13 pure CSS/SVG chart individual template files
- **Layout Reference** `layouts/`: 10 layout reference files (symmetric, asymmetric, L-shape, T-shape, hero, waterfall, etc.)
- **Style System** `styles/`: 8 preset style individual files + README decision rules

**Image Strategy Upgrade:**
- Planning stage (Step 4) adds `image` field: decide image usage, prompt, placement, and alt text per page at planning time
- New image usage types: `split-content` and `card-inset`, breaking away from background-only image patterns
- `image_paths` upgraded to `image_info`: carries full image metadata (usage, placement, prompt) into design stage
- Decoration toolkit resource menu added to design prompt

**Multi Card Styles:**
- New `card_style` field: 6 card visual styles (filled/transparent/outline/accent/glass/elevated)
- Card style decided at planning stage, breaking monolithic filled-card monotony

**Dual Pipeline PPTX:**
- New PNG pipeline: `html2png.py` + `png2pptx.py`, Puppeteer screenshot + python-pptx embed, maximum compatibility
- SVG pipeline retained: `html2svg.py` + `svg2pptx.py`, dom-to-svg + OOXML native SVG embed, editable text
- User selects pipeline at Step 6

**Workflow Enhancements:**
- Resource consumption checks: read resource menu before Step 4, read specific references before Step 5c
- Grouped generation: presentations over 12 pages force grouped generation to avoid token limits
- Deprecated file cleanup: removed `method.md`, old `style-system.md`, `bento-grid.md`

## License

[MIT](LICENSE)
