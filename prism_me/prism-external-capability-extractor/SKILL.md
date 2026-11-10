---
name: prism-external-capability-extractor
description: Extract candidate Prism-facing capabilities from external code or skills. Use when the source material has already been scoped and now needs a systematic mapping of upstream entrypoints, purposes, inputs, outputs, dependencies, and likely Prism roles or lifecycle stages.
---

# Prism External Capability Extractor

This skill turns an external surface into candidate agent capabilities.

Read:

- [../agents.md](../agents.md)
- [../shared/references/dependency-discipline.md](../shared/references/dependency-discipline.md)
- [../shared/references/external-harmonization.md](../shared/references/external-harmonization.md)
- [../shared/templates/02d-external-capabilities.md](../shared/templates/02d-external-capabilities.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)
- `.prism/<request-slug>/02c-external-surface.md`

## Workflow

1. Identify the distinct capabilities exposed by the external source.
2. For each capability, record purpose, entrypoint, inputs, outputs, dependencies, and likely Prism role.
3. Where possible, distinguish dependency classes such as bundle-level, backend-level, KB-level, or workspace-level requirements.
4. Decide which capabilities should stay bundled and which should split into separate agent surfaces.
5. Note capabilities that should remain external-only for now.
6. Record risks and gaps in the candidate decomposition.
7. Write or update `.prism/<request-slug>/02d-external-capabilities.md`.
8. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Do not confuse one repo with one capability.
- Prefer capability boundaries that match real handoffs, not just directory names.
- Keep external-only limitations explicit.

## Output Contract

Produce an external capability map with:

- candidate capabilities
- Prism grouping guesses
- bundling or splitting notes
- dependency-class notes
- risks and gaps
