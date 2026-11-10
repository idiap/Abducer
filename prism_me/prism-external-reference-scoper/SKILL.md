---
name: prism-external-reference-scoper
description: Scope external references, code, skills, or upstream runtimes before harmonizing them into Prism. Use when a request starts from material outside the local Prism-shaped pack and needs a systematic source inventory, provenance record, runtime truth map, and preserved-asset view.
---

# Prism External Reference Scoper

This skill is the first pass over external material.

Read:

- [../agents.md](../agents.md)
- [../shared/references/dependency-discipline.md](../shared/references/dependency-discipline.md)
- [../shared/references/external-harmonization.md](../shared/references/external-harmonization.md)
- [../shared/references/prism-alignment.md](../shared/references/prism-alignment.md)
- [../shared/templates/02c-external-surface.md](../shared/templates/02c-external-surface.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)
- `.prism/<request-slug>/01-spec.md`

## Workflow

1. Record the source project, source archive or repo, and local preserved paths.
2. Inventory the key docs, scripts, prompts, examples, tests, and runtime dependencies.
3. Identify the real execution model, backend touch points, and any persistent workspace expectations.
4. Mark the assets, preserved roots, and dependency-bearing boundaries that must remain explicit during harmonization.
5. Record risks and unknowns before any Prism shaping starts.
6. Write or update `.prism/<request-slug>/02c-external-surface.md`.
7. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Do not flatten upstream structure during scoping.
- Do not guess that prose-only assets are executable or that executable assets are prompt-only.
- Keep the runtime truth visible even if it is awkward.

## Output Contract

Produce an external surface map with:

- source provenance
- surface inventory
- runtime truth
- preserved assets
- dependency-bearing runtime surfaces
- risks and unknowns
