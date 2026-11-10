---
name: prism-agentic-shape-forger
description: Deliver the Prism agentic shape for external code or skills. Use when scoped external capabilities should be turned into candidate agent surfaces with organization group, lifecycle stage, role, semantic folder, runtime adapter notes, reasoning-log expectations, preserved assets, and bundle layout.
---

# Prism Agentic Shape Forger

This skill turns external capabilities into Prism-shaped agent surfaces.

Read:

- [../agents.md](../agents.md)
- [../shared/references/dependency-discipline.md](../shared/references/dependency-discipline.md)
- [../shared/references/external-harmonization.md](../shared/references/external-harmonization.md)
- [../shared/references/prism-alignment.md](../shared/references/prism-alignment.md)
- [../shared/templates/02e-agentic-shape.md](../shared/templates/02e-agentic-shape.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)
- `.prism/<request-slug>/02c-external-surface.md`
- `.prism/<request-slug>/02d-external-capabilities.md`

## Workflow

1. Choose the overall import strategy: preservation-first, adapter-first, native-wrapping target, or mixed.
2. For each candidate capability, define the Prism-shaped agent surface.
3. Record organization group, lifecycle stage, role, entrypoints, semantic folder, runtime adapter notes, reasoning-log notes, and preserved assets.
4. Capture dependency-shape notes for likely bundles, KBs, backends, workspace mounts, or capability source paths that later stages should map formally.
5. Sketch the bundle layout, example usage, and integration test surfaces needed later.
6. Record open design decisions rather than burying them in prose.
7. Write or update `.prism/<request-slug>/02e-agentic-shape.md`.
8. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Do not pretend external runtime truth has disappeared just because a Prism shape now exists.
- Prefer explicit adapter notes over vague "wrap later" language.
- The result should be usable by the later contract author, planner, and bundle builder.

## Output Contract

Produce an agentic shape plan with:

- import strategy
- candidate agent surfaces
- dependency-shape notes
- bundle layout ideas
- open design decisions
