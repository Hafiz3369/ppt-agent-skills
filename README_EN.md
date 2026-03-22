# PPT Agent Skill

**[中文文档](README.md)**

<div align="center">
  <img src="assets/logo.png" alt="PPT Agent Logo" width="160" />
  <h1>PPT Agent</h1>
  <p><strong>AI-Powered Presentation Design Workflow</strong></p>
  <p>
    Simulates the complete workflow of a top-tier PPT design company ($1,000+/page)<br/>
    Outputs high-quality HTML presentations + Optional dual-pipeline PPTX
  </p>

  <p>
    <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick_Start-blue?style=for-the-badge" alt="Quick Start" /></a>
    <a href="README.md"><img src="https://img.shields.io/badge/Chinese_Docs-red?style=for-the-badge" alt="Chinese" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" /></a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Pipeline-6_Steps-4f7df5?style=flat-square" alt="Pipeline" />
    <img src="https://img.shields.io/badge/Styles-8_Themes-ff6b35?style=flat-square" alt="Styles" />
    <img src="https://img.shields.io/badge/Layouts-10_Types-00d4ff?style=flat-square" alt="Layouts" />
    <img src="https://img.shields.io/badge/Charts-13_Templates-8b5cf6?style=flat-square" alt="Charts" />
    <img src="https://img.shields.io/badge/Blocks-8_Components-22c55e?style=flat-square" alt="Blocks" />
    <img src="https://img.shields.io/badge/Scripts-8_Tools-f59e0b?style=flat-square" alt="Scripts" />
  </p>
</div>

---

## Showcase

> Example output themed "Linux Do Community In-depth Analysis" (Dark Tech Style):

<div align="center">
  <img src="assets/screenshots/slide1.png" width="32%" />
  <img src="assets/screenshots/slide2.png" width="32%" />
  <img src="assets/screenshots/slide3.png" width="32%" />
  <img src="assets/screenshots/slide4.png" width="32%" />
  <img src="assets/screenshots/slide5.png" width="32%" />
  <img src="assets/screenshots/slide6.png" width="32%" />
  <img src="assets/screenshots/slide7.png" width="32%" />
  <img src="assets/screenshots/slide8.png" width="32%" />
  <img src="assets/screenshots/slide9.png" width="32%" />
  <img src="assets/screenshots/slide10.png" width="32%" />
  <img src="assets/screenshots/slide11.png" width="32%" />
  <img src="assets/screenshots/slide12.png" width="32%" />
  <img src="assets/screenshots/slide13.png" width="32%" />
</div>

---

## Design Philosophy

This is not a "template filling" tool, but an AI Agent Skill that **simulates the complete workflow of a professional design agency**.

The core difference lies in 3 design decisions:

### 1. Separation of Planning & Design -- Think before you act

```
Traditional: Topic → Generate PPT (Content & Layout mixed)
This Project: Topic → Research → Outline → Planning Draft (JSON) → Design Draft (HTML)
```

The planning draft is pure structured JSON, deciding "what content, which layout, which card type" for each page. The design draft only focuses on turning the planning draft into beautiful HTML. The two stages are decoupled and specialized.

### 2. On-demand Resource Loading -- Zero token waste

The project has 60+ reference files (layouts, charts, principles...), but each HTML page only needs a few. The solution is a **three-layer decision tree**:

| Layer | Timing | Decision |
|------|------|---------|
| Layer 1 | After Interview | Global toggles (Image usage, style, language) |
| Layer 2 | After Outline | Narrative rhythm template (Choose template by page count) |
| Layer 3 | Before Each Page | `prompt_assembler.py` auto-assembles all resources needed for that page |

The LLM only needs to `view_file` one `prompt-ready-{n}.txt` per page to get the full design context.

### 3. Automated Quality Assurance -- Machine-driven reliability

| Phase | Automation Tool | Function |
|------|----------|------|
| After Planning | `planning_validator.py` | Validates JSON schema, enum values, and resource path existence |
| Before HTML | `prompt_assembler.py` | Auto-assembles full prompt, preventing "missing resources" |
| After HTML | 6-item Checklist | Content integrity / No overlap / Pipeline safety / No overflow / Color specs / Resource usage |
| After All | Cross-page Validation | Layout diversity / Visual weight rhythm / Image usage diversity |

---

## 6-Step Pipeline

```
Step 1       Step 2       Step 3        Step 4         Step 5          Step 6
Interview ──→ Research ──→ Outline ──→ Page Planning ──→ Style+Image+HTML ──→ Post-processing
[Wait User]              [Pyramid]     [JSON/Page]     [Iterative Gen]  [PNG/SVG→PPTX]
                                       [Validator]     [Auto-Assembler]
```

| Step | What to do | Key Design |
|------|--------|---------|
| **Step 1** Interview | 7-question 3-layer progressive interview | **Blocker** -- Must wait for user reply; no assumptions made |
| **Step 2** Research | Multi-dimensional parallel search | Only high/medium confidence data enters the planning draft |
| **Step 3** Outline | Pyramid Principle + Narrative Arc + Logic Chain | Min 2 pages per Part, clear logical progression between Parts |
| **Step 4** Planning | Per-page JSON generation | Immediate `planning_validator.py` check after writing |
| **Step 5** Design | 5a Style → 5b Images → 5c Per-page HTML | `prompt_assembler.py` auto-assembles full prompt |
| **Step 6** Post-processing | User selects pipeline → Conversion → Output | PNG Pipeline (Max compatibility) or SVG Pipeline (Editable text) |

---

## Core Features

<table>
<tr>
<td width="50%">

### Rich Visual System
- **8 Preset Styles** -- Dark Tech / Xiaomi Orange / Blue White / Royal Red / Fresh Green / Luxury Purple / Minimal Gray / Vibrant Rainbow
- **10 Layouts** -- Bento Grid + Symmetric/Asymmetric/L-shape/T-shape/Waterfall/Hero variants
- **6 Card Styles** -- filled / transparent / outline / accent / glass / elevated

</td>
<td width="50%">

### Data Viz & Building Blocks
- **13 Charts** -- Progress bars / Ring charts / Sparklines / Waffle / KPI / Radar / Funnel, etc.
- **7 Blocks** -- Timeline / People Card / Comparison / Matrix / Quotes / Image Hero, etc.

</td>
</tr>
<tr>
<td>

### Smart Image Strategy
Decide image usage, prompt, and placement at planning stage. 7 visual fusion techniques: Fade blend / Tinted overlay / Ambient background / Split-content / Card-inset / Decorative layer / Pure background.

</td>
<td>

### Dual Pipeline PPTX Output

```
HTML ─┬─ PNG Pipeline → PPTX (Max Compatibility)
      └─ SVG Pipeline → PPTX (Editable Text)
```

User selects the pipeline; Agent doesn't decide for the user.

</td>
</tr>
<tr>
<td>

### Automation Toolchain
- **prompt_assembler.py** -- Auto-assembles full design prompt
- **resource_assembler.py** -- Auto-assembles resource blocks
- **planning_validator.py** -- Planning JSON validation (single & cross-page)
- **html_packager.py** -- Merges HTML pages for preview

</td>
<td>

### Interruption Recovery
`progress.json` tracks steps. Resumes from breakpoint after long process interruption. Auto-rollbacks if previous artifacts are missing.

</td>
</tr>
</table>

<details>
<summary><strong>View Full Feature List</strong></summary>

| Feature | Description |
|------|------|
| **Typography** | 7-level font scale + spacing hierarchy + CJK mixed rules |
| **Color Ratio** | 60-30-10 rule + accent color constraints |
| **Principle Library** | 6 Design Principles (Cognitive Load/Color Psych/Composition/Data Viz/Narrative Arc/Hierarchy) |
| **Narrative Rhythm** | Density alternation / Chapter color progression / Cover-End echo / 3 Std Templates (10/15/20 pages) |
| **Compatibility** | Detailed CSS blacklist + SVG safe subset + Three-layer model (Browser/dom-to-svg/OOXML) |
| **Quality Baseline** | Independent checklist defining minimum per-page standards |
| **Resource Registry** | `resource-registry.md` - Single source of truth for all mappings |
| **Adaptive Complexity** | Adjusts workflow granularity by page count (Light/Standard/Large) |
| **Page Templates** | Structural specs for Cover/TOC/Section/End pages |
| **CSS Animations** | Fade-in / Count-up / Fill / Stroke animations (for HTML preview) |

</details>

---

## Quick Start

### Prerequisites

| Dependency | Version | Purpose |
|------|------|------|
| Node.js | >= 18 | Puppeteer + dom-to-svg |
| Python | >= 3.8 | Script execution |
| python-pptx | latest | PPTX generation |

### One-Click Install

```bash
# Python dependencies
pip install python-pptx lxml Pillow

# Node.js dependencies
npm install puppeteer dom-to-svg
```

### Usage

Simply describe your needs in the conversation. The Agent will execute the 6-step workflow:

```
You: "Make a PPT about X"
  → Agent interviews for requirements (waits for reply)
  → Auto research → Generate outline → Per-page planning (with image strategy)
  → prompt_assembler auto-assembles → Per-page HTML design
  → Auto post-processing: HTML → PNG/SVG → PPTX
  → All artifacts saved to ppt-output/
```

**Trigger Examples**:

| Scenario | What to Say |
|----------|-------------|
| Pure Topic | "Make a PPT about X" / "Create a presentation on Y" |
| With Material | "Turn this document into a PPT" / "Make slides from this report" |
| With Requirements | "15-page dark tech style AI safety report" |
| Implicit Trigger | "I need to present Y to my boss" / "Make training courseware" / "Roadshow deck" |

> No manual script execution needed. All post-processing is automated in Step 6.

---

## Output Artifacts

```
ppt-output/
  preview.html         # Browser-based paginated preview
  presentation.pptx    # Final PPTX file
  slides/              # Per-page HTML source files
  planning/            # Per-page JSON (Manually editable)
  prompts-ready/       # Auto-assembled full prompts (For debugging)
  images/              # AI-generated images
  png/                 # PNG screenshots (PNG Pipeline)
  svg/                 # Vector SVG (SVG Pipeline)
  style.json           # Style definition
  outline.json         # Outline
  progress.json        # Progress log (For recovery)
```

---

## Project Structure

```
ppt-agent-skill/
  SKILL.md                        # Master workflow instructions (Agent Entry)
  references/
    resource-registry.md          # Resource Registry (Single source of truth)
    quality-baseline.md           # Quality baseline checklist
    narrative-rhythm.md           # Narrative rhythm (Templates + Color progression + Conflict priority)
    image-generation.md           # Image strategy (6D prompt formula + Fusion techniques)
    pipeline-compat.md            # Pipeline compatibility (Three-layer model + Blacklist)
    prompts/                      # Modular prompts
      prompt-1-research.md        #   Research (7-question progressive)
      prompt-2-outline.md         #   Outline (Pyramid Principle + Narrative Arc v3.0)
      prompt-3-planning.md        #   Planning (14 card_types + decoration_hints)
      prompt-4-design.md          #   Design (Template for prompt_assembler)
      prompt-5-notes.md           #   Speaker Notes
      animations.md               #   CSS animation library
    styles/                       # 8 Preset styles (Individual files)
    layouts/                      # 10 Layouts (Individual files + HTML skeletons)
    charts/                       # 13 Chart templates (Individual files)
    blocks/                       # 7 Building blocks + 6 Card visual styles
    page-templates/               # Cover/TOC/Section/End specs
    principles/                   # 6 Design principles
  scripts/
    prompt_assembler.py           # Auto-assembles full prompt (Styles+Plan+Content+Images+Res)
    resource_assembler.py         # Assembles resources (Layouts+Blocks+Charts+Principles)
    planning_validator.py         # Planning JSON validation
    html_packager.py              # Merges HTML for preview
    html2png.py                   # HTML → PNG (Puppeteer)
    html2svg.py                   # HTML → SVG (dom-to-svg)
    png2pptx.py                   # PNG → PPTX (Max compatibility)
    svg2pptx.py                   # SVG → PPTX (OOXML native SVG)
```

---

## Technical Architecture

```
                          ┌─────────────────────────────────────┐
                          │          PPT Agent Workflow          │
                          └──────────────┬──────────────────────┘
                                         │
            ┌────────┬────────┬──────────┼──────────┬────────┐
            ▼        ▼        ▼          ▼          ▼        ▼
        Step 1   Step 2   Step 3     Step 4      Step 5   Step 6
       Interview Research Outline    Planning     Design   Post-proc
                                    (JSON/Page)   (HTML)
                                        │            │
                          planning_validator    prompt_assembler
                          (Validate on write)   (Auto-assemble prompt)
                                                     │
                                          ┌──────────┴──────────┐
                                          ▼                     ▼
                                     PNG Pipeline          SVG Pipeline
                                     html2png.py           html2svg.py
                                          │                     │
                                          ▼                     ▼
                                     png2pptx.py           svg2pptx.py
                                          │                     │
                                          └──────────┬──────────┘
                                                     ▼
                                              presentation.pptx
```

---

## Changelog

### v3.0 -- Quality Automation + Outline Refactor + Pipeline Compatibility (2026-03-22)

<details>
<summary><strong>Automation Toolchain (Core Upgrade)</strong></summary>

- **prompt_assembler.py**: Auto-reads design templates, replaces 5 placeholders (Style/Planning/Content/Images/Resources), outputs ready-to-use prompt file. LLM only needs one `view_file` per page, fundamentally eliminating "missing resources".
- **resource_assembler.py**: Auto-parses `required_resources` from planning JSON, assembles `[RESOURCES]` block (Layouts + Blocks + Charts + Principles), called by prompt_assembler.
- **planning_validator.py**: Validate on write (Single page: Schema/Enums/Paths/Diversity; Full set: Layout diversity/Visual weight/Image variety).

</details>

<details>
<summary><strong>Strategic Architect v3.0 (Outline)</strong></summary>

- prompt-2-outline.md refactored to "Strategic Architect" with a 5-step deep thinking process.
- New `design_rationale` field (Core claim/Narrative structure/Emotion arc/Logic chain/Page allocation).
- Part-to-part logical labeling (`transition_from_previous`), preventing flat parallel outlines.
- Strict constraint: Min 2 pages per Part + Search data coverage markers.

</details>

<details>
<summary><strong>Pipeline Compatibility Deepening</strong></summary>

- pipeline-compat.md expanded into a Three-layer Model document (Browser Rendering / dom-to-svg / OOXML).
- Added SVG element safe subset, CSS transform constraints, font handling, and shape filtering rules.
- `svg2pptx.py` significantly enhanced (+181 lines), fixing multiple conversion bugs.

</details>

<details>
<summary><strong>Narrative Rhythm & Planning Enhancement</strong></summary>

- narrative-rhythm.md adds 3 standard templates (10/15/20 pages) + conflict priority + edge case handling.
- prompt-3-planning.md enhanced with `decoration_hints` and card-level `required_resources` binding.
- `html2svg.py` conversion logic optimization (+162 lines).

</details>

### v2.0 -- Modular Refactor + Image Strategy Upgrade (2026-03-22)

<details>
<summary><strong>Architectural Refactor</strong></summary>

- **Modular Prompt System**: Monolithic `prompts.md` (900+ lines) split into 5 independent modules + animation lib, loaded on demand.
- **Resource Registry**: Added `resource-registry.md` as the single source of truth for all resource mappings.
- **Quality Baseline**: Added `quality-baseline.md` independent quality checklist.

</details>

<details>
<summary><strong>Six New Resource Modules</strong></summary>

- **Building Blocks** `blocks/`: 7 reusable HTML blocks (Timeline, People, Comparison, Matrix, Quote, Hero, etc.).
- **Design Principles** `principles/`: 6 design principle references (Cognitive Load, Color Psych, etc.).
- **Chart Templates** `charts/`: 13 pure CSS/SVG chart template files.
- **Layout Reference** `layouts/`: 10 layout files (Symmetric, Asymmetric, Bento, etc.).
- **Style System** `styles/`: 8 preset style files + Decision rules.

</details>

<details>
<summary><strong>Image Strategy + Card Styles + Dual Pipeline</strong></summary>

- Step 4 Planning adds `image` field: decide usage/prompt/placement during planning.
- Added `card_style` field: 6 visual styles (filled/transparent/outline/accent/glass/elevated).
- New PNG Pipeline: `html2png.py` + `png2pptx.py` for maximum compatibility.
- SVG Pipeline retained: `html2svg.py` + `svg2pptx.py` for editable text.

</details>

---

## License

[MIT](LICENSE)

---

<div align="center">
  <sub>Built with passion for beautiful presentations</sub>
</div>
