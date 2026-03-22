# PPT Agent

> Software engineering principles applied to presentation generation.

[中文文档](README.md)

PPT Agent is a code-driven presentation generation framework. By strictly decoupling content planning from visual design, it relies on structured data formatting and dynamic asset loading to output high-fidelity HTML and PPTX files. This engineered approach solves the typical hallucinations and aesthetic chaos inherent in long-prompt, single-pass LLM solutions.

## Features

- **Separation of Concerns**: Generates and validates a strictly structured `JSON` draft defining content mapping before applying any rendering logic to `HTML`.
- **On-Demand Context Injection**: Owns a massive library of 60+ assets but injects only what the current slide targets. Saves LLM tokens and prevents context overload conflicts.
- **Automated Validation**: Syntaxes and module variables are validated automatically during IO write cycles.
- **Dual-Engine Export**: Offers two export pipelines for PPTX compiling: a pixel-perfect universal PNG rendering path, and a scalable, text-editable SVG vector path.
- **Persistent State**: Lengthy generation tasks snapshot safely into `progress.json`, offering seamless pause and resume capabilities for massive slide counts.

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

```text
ppt-agent-skill/
├── SKILL.md                 # Cognitive router and orchestrator context
├── scripts/                 # Utility processors (HTML injections / Validators)
└── references/              # Pluggable modular assets
    ├── blocks/              # DOM container components
    ├── layouts/             # Grid alignment primitives
    ├── charts/              # Native CSS/SVG chart templates
    └── styles/              # Baseline aesthetic boundaries & palettes
```

## License

[MIT License](LICENSE)
