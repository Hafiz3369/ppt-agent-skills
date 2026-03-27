# Global Design Guide

This file is the deck-level design DNA used by `scripts/prompt_assembler.py` when
building self-contained `prompt-ready-{n}.txt` files.

## Priorities

1. Content fidelity before visual flourish
2. Clear hierarchy before decorative detail
3. Spatial drama only after the contract is stable
4. Mood/detail only after payload visibility is secured

## Non-Negotiables

- Each slide must have exactly one dominant visual anchor.
- Preserve `page_type`, `layout_hint`, `visual_weight`, card ids, and card roles.
- Use CSS variables for theme colors; avoid ad hoc hard-coded theme colors.
- Regular content pages need at least 3 readable visual layers; section/toc can drop to 2.
- When space is tight, compress copy before collapsing hierarchy.

## Dense Scene Guardrails

- `report`: metrics + comparison/delta + management readout
- `academic`: question/definition + evidence/method + boundary/limitation
- `technical`: structure/step + constraints/dependencies + risk/fallback
- `training`: steps + checkpoints + warning/fallback

Dense scenes cannot be solved by atmosphere, whitespace, or slogan-first hero compositions.

## Variation Rules

- Adjacent slides should vary in at least 2 dimensions:
  - focus placement
  - whitespace ratio
  - card-style mix
  - technique mix
  - material treatment
- Reuse the same visual gene, not the same answer.
- If a layout reappears, shift emphasis, texture, or composition so it does not feel cloned.

## Anti-Patterns

- Symmetric web-section layouts unless planning explicitly requires them
- Multiple equal-weight anchors on one page
- Dense pages rendered as keynote hero / cover pages
- Decorative noise used to mask missing payload
- Turning qualified/derived claims into hard proof
