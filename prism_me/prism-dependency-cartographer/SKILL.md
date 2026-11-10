---
name: prism-dependency-cartographer
description: Map dependencies according to the Prism way of managing them. Use when a request needs an evidence-backed dependency picture covering uv bundles, runtime dependencies, reference KBs, backend profiles, workspace mounts, capability source paths, and hidden setup risks before planning or release.
---

# Prism Dependency Cartographer

This skill turns repository and runtime evidence into a Prism-style dependency map.

Read:

- [../agents.md](../agents.md)
- [../shared/references/prism-alignment.md](../shared/references/prism-alignment.md)
- [../shared/references/dependency-discipline.md](../shared/references/dependency-discipline.md)
- [../shared/references/release-gates.md](../shared/references/release-gates.md)
- [../shared/references/workspace-convention.md](../shared/references/workspace-convention.md)
- [../shared/templates/03b-dependency-map.md](../shared/templates/03b-dependency-map.md)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)
- `.prism/<request-slug>/01-spec.md`
- `.prism/<request-slug>/02-agent-contract.yaml`
- `.prism/<request-slug>/02b-quality-criteria.md`
- `.prism/<request-slug>/03-repo-map.md`

If the request starts from external code or skills, also read:

- `.prism/<request-slug>/02c-external-surface.md`
- `.prism/<request-slug>/02d-external-capabilities.md`
- `.prism/<request-slug>/02e-agentic-shape.md`

## Workflow

1. Read the current spec, contract, quality criteria, and repo map together.
2. Inventory dependency surfaces from code, config, docs, tests, scripts, and preserved runtimes.
3. Normalize the findings into Prism-style classes: `uv` bundles, runtime dependencies, reference KBs, backend profiles, runtime adapter surfaces, and dependency edges.
4. Mark each important dependency as `existing`, `reused`, `new`, `proposed`, or `external-only`.
5. Mark each important dependency as `declared`, `inferred`, or `hidden`.
6. Record which slices, tests, docs, or runtime adapters depend on each dependency.
7. Record verification commands or checks for important dependencies, including bundle status or dry-run commands when relevant.
8. Flag hidden, manual, version-coupled, or environment-coupled dependencies as risks.
9. Write or update `.prism/<request-slug>/03b-dependency-map.md`.
10. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Do not reduce the map to package names or a copied requirements file.
- Do not hide workspace mounts, backend choices, KB requirements, or preserved runtime roots inside prose.
- Keep evidence explicit: file paths, commands, config fields, or source artifacts.
- Keep declared facts separate from inference.
- If implementation later changes dependency reality, the dependency map must be updated.

## Output Contract

Produce a dependency map with:

- bundle alignment
- runtime dependency inventory
- reference KB and backend mapping
- runtime adapter and workspace mapping
- dependency edges into slices, tests, docs, and handoff
- hidden dependency risks
- verification plan
