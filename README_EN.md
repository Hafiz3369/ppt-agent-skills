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

Executions follow a strict 6-step lifecycle:

1. **Discovery**: Extrapolates necessary scopes and audience profiling.
2. **Aggregated Search**: Parses data with cross-reference validations.
3. **Outlining**: Establishes structural narrative paths using the Pyramid Principle.
4. **Draft Generation (JSON)**: Establishes container skeletons and metric encapsulation.
5. **View Assembly (HTML)**: Scaffolds CSS rules and injects visual blocks.
6. **Binaries Compile (PPTX)**: Executes Node.js/Python post-processors yielding presentation formats.

## Getting Started

As an AI-native Agent Skill, PPT Agent requires strictly zero manual environment setup. All dependencies and runtimes are provisioned automatically by the agent pipeline during execution.

### Execution 

In a prompt-enabled Agent IDE, instruct the instance to trigger the workflow natively:

> _"Assemble a 15-page deck regarding LLM computation footprints."_

Rendered assemblies output entirely towards `ppt-output/`, including standard executables `.pptx` and a local-browser preview state.

## Repository Layout

The repository now follows the control-console model defined by `SKILL.md`. Only three areas are runtime sources of truth:

```text
ppt-agent-skill/
├── SKILL.md                 # Main state machine, gates, rollback rules
├── scripts/                 # Runtime script entrypoints
│   └── README.md            # Script index
├── references/              # Markdown sources of truth
│   ├── playbooks/           # sub-agent execution guides
│   ├── runtime/             # runtime shared contracts
│   ├── design-runtime/      # design/runtime supplemental rules
│   ├── ops/                 # ops notes and resource map
│   └── README.md            # Reference index
├── assets/                  # Logo and README screenshots
├── copy/                    # Manual backup area, not runtime
└── ppt-output/              # Runtime outputs (git-ignored)
```

### Directory Boundaries

- `SKILL.md`: control-console contract only; no embedded sub-agent prompt templates.
- `scripts/`: executable workflow utilities only; no mirrored markdown copies.
- `references/`: markdown sources of truth used by the live workflow; the root now stays index-only and grouped docs live in subdirectories.
- `copy/`: backup only; never treated as a runtime source.
- `ppt-output/`: generated artifacts only.

### Entry Index

- Control console: `SKILL.md`
- Script index: `scripts/README.md`
- Markdown/reference index: `references/README.md`

## License

[MIT License](LICENSE)
