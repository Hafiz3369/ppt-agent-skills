# PPT Agent Skill

**[中文文档](README_CN.md)**

> A professional AI-powered presentation generation assistant that simulates the complete workflow of a top-tier PPT design company (quoted at $1,000+/page), outputting high-quality HTML presentations + editable vector PPTX files.

## Workflow

```
Requirements Interview → Research → Outline → Planning Draft → Style + Images + HTML Design → Post-processing (SVG + PPTX)
```

## Key Features

| Feature | Description |
|---------|-------------|
| **6-Step Pipeline** | Requirements → Research → Outline → Planning → Design → Post-processing |
| **8 Preset Styles** | Dark Tech / Xiaomi Orange / Blue White / Royal Red / Fresh Green / Luxury Purple / Minimal Gray / Vibrant Rainbow |
| **Bento Grid Layout** | 7 flexible card-based layouts driven by content, not templates |
| **Smart Illustrations** | AI-generated images with 5 visual fusion techniques (fade blend, tinted overlay, ambient background, etc.) |
| **Typography System** | 7-level font scale + spacing hierarchy + CJK mixed typesetting rules |
| **Color Proportion** | 60-30-10 rule enforcement + accent color constraints |
| **Data Visualization** | 8 pure CSS/SVG chart types (progress bars, ring charts, sparklines, waffle charts, KPI cards, etc.) |
| **Cross-page Narrative** | Density alternation, chapter color progression, cover-ending visual echo |
| **Footer System** | Unified footer with chapter info + page numbers across all slides |
| **PPTX Compatible** | HTML → SVG → PPTX pipeline, right-click "Convert to Shape" in PPT 365 for full editing |

## Output

| File | Description |
|------|-------------|
| `preview.html` | Browser-based paginated preview (auto-generated) |
| `presentation.pptx` | PPTX file, right-click "Convert to Shape" in PPT 365 for editing |
| `svg/*.svg` | Per-page vector SVG, drag into PPT directly |
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
  README.md                   # This file
  README_CN.md                # Chinese documentation
  references/
    prompts.md                # 5 Prompt templates
    style-system.md           # 8 preset styles + CSS variables
    bento-grid.md             # 7 layout specs + card types
    method.md                 # Core methodology
  scripts/
    html_packager.py          # Merge multi-page HTML into paginated preview
    html2svg.py               # HTML → SVG (dom-to-svg, preserves editable text)
    svg2pptx.py               # SVG → PPTX (OOXML native SVG embedding)
```

## Script Usage

```bash
# Merge preview
python3 scripts/html_packager.py <slides_dir> -o preview.html

# HTML to SVG
python3 scripts/html2svg.py <slides_dir> -o <svg_dir>

# SVG to PPTX
python3 scripts/svg2pptx.py <svg_dir> -o output.pptx --html-dir <slides_dir>
```

## Technical Architecture

```
HTML slides
  → [Puppeteer] → [dom-to-svg] → SVG (editable <text>)
  → [python-pptx + lxml] → PPTX (OOXML svgBlip + PNG fallback)
```

## License

[MIT](LICENSE)
