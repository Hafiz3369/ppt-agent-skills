<div align="center">
  <img src="assets/logo.png" alt="PPT Agent Logo" width="160" />
  <h1>PPT Agent</h1>
  <p><strong>Software engineering principles applied to presentation generation.</strong></p>

  <p>
    <a href="#quick-start"><img src="https://img.shields.io/badge/Quick_Start-blue?style=for-the-badge" alt="Quick Start" /></a>
    <a href="README.md"><img src="https://img.shields.io/badge/Chinese_Docs-red?style=for-the-badge" alt="Chinese" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" /></a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Pipeline-6_Steps-4f7df5?style=flat-square" alt="Pipeline" />
    <img src="https://img.shields.io/badge/Styles-8_Themes-ff6b35?style=flat-square" alt="Styles" />
    <img src="https://img.shields.io/badge/Layouts-10_Types-00d4ff?style=flat-square" alt="Layouts" />
    <img src="https://img.shields.io/badge/Charts-13_Templates-8b5cf6?style=flat-square" alt="Charts" />
    <img src="https://img.shields.io/badge/Blocks-7_Components-22c55e?style=flat-square" alt="Blocks" />
    <img src="https://img.shields.io/badge/Scripts-8_Tools-f59e0b?style=flat-square" alt="Scripts" />
  </p>
</div>

---

PPT Agent is a code-driven presentation generation framework. By strictly decoupling content planning from visual design, it relies on structured data formatting and dynamic asset loading to output high-fidelity HTML and PPTX files. This engineered approach solves the typical hallucinations and aesthetic chaos inherent in long-prompt, single-pass LLM solutions.

## Features

- **Separation of Concerns**: Generates and validates a strictly structured `JSON` draft defining content mapping before applying any rendering logic to `HTML`.
- **On-Demand Context Injection**: Owns a massive library of 60+ assets but injects only what the current slide targets. Saves LLM tokens and prevents context overload conflicts.
- **Automated Validation**: Syntaxes and module variables are validated automatically during IO write cycles.
- **Dual-Engine Export**: Offers two export pipelines for PPTX compiling: a pixel-perfect universal PNG rendering path, and a scalable, text-editable SVG vector path.
- **Recoverable Artifact Chain**: Long runs resume from formal intermediate artifacts on disk instead of relying on a single runtime state file.

## Showcase

_Preview rendering samples:_

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

## Workflow Architecture

At a high level, the system can still be understood as a 6-stage production line, but the control console now orchestrates it strictly as `Step 0 -> Step 5`:

1. **Interview and Routing**: collect requirements, normalize them, and decide between the research and non-research branches.
2. **Material Preparation**: run Search-Lite or compress user-provided source materials.
3. **Pyramid Outline**: build the narrative structure and complete self-review.
4. **Global Style First**: generate a `style.json` contract that downstream planning and HTML stages can consume reliably.
5. **Per-Slide Planning and Rendering**: produce planning JSON, HTML, PNG, and visual review for each slide.
6. **Delivery Packaging**: generate `preview.html`, PNG/SVG PPTX exports, and the delivery manifest.

## Getting Started

This project runs as an Agent Skill. The main workflow assumes the current environment provides file I/O, Python execution, Planning tools, and sub-agent capabilities; information retrieval and image generation can degrade by stage when unavailable.

### Execution 

In a prompt-enabled Agent IDE, instruct the instance to trigger the workflow natively:

> _"Assemble a 15-page deck regarding LLM computation footprints."_

Rendered outputs are written to `ppt-output/runs/<RUN_ID>/`, including browser-previewable `preview.html` and both `presentation-png.pptx` and `presentation-svg.pptx`.

## Repository Layout

The repository now follows the control-console model defined by `SKILL.md`. The runtime sources of truth are organized as:

```text
ppt-agent-skill/
├── SKILL.md                 # Main state machine, gates, rollback rules
├── scripts/                 # Runtime script entrypoints
│   └── README.md            # Script index
├── references/              # Markdown sources of truth
│   ├── playbooks/           # sub-agent execution guides
│   ├── prompts/             # prompt templates
│   ├── styles/              # preset styles + runtime style contracts
│   ├── layouts/             # layout resources
│   ├── blocks/              # component resources
│   ├── charts/              # chart resources
│   ├── principles/          # design principles
│   ├── page-templates/      # cover / toc / section / end templates
│   ├── design-runtime/      # data-to-visual bridge rules
│   └── README.md            # Reference index
├── assets/                  # Logo and README screenshots
├── README.md
└── README_EN.md
```

### Directory Boundaries

- `SKILL.md`: the control-console contract only, defining the state machine, orchestration skeleton, gates, and recovery rules.
- `scripts/`: executable workflow utilities and interface indexes only.
- `references/`: markdown sources of truth consumed by the main chain or subagents on demand.
- `assets/`: logo and showcase screenshots only.
- `ppt-output/`: created dynamically in the user's working directory at runtime; not treated as repository source of truth.

### Entry Index

- Control console: `SKILL.md`
- Script index: `scripts/README.md`
- Markdown/reference index: `references/README.md`

## License

[MIT License](LICENSE)
