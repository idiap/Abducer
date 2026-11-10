<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# External Harmonization

Use this guide when the request starts from external code, external skills, upstream docs, or a preserved runtime that should be shaped into Prism-like agent surfaces.

## Goal

Go through external material systematically so the result can acquire the agentic shape of Prism without flattening away provenance or runtime boundaries.

## Core Rules

1. Preserve provenance.
   Keep source project, original paths, and preserved asset boundaries explicit.

2. Preserve runtime truth.
   If the external system is script-backed, runtime-backed, or workspace-backed, model that honestly instead of pretending it is already a native Prism skill.

3. Extract capabilities before writing contracts.
   First identify what the external code can actually do, then decide how that maps to Prism agent surfaces.

4. Distinguish shape from implementation.
   The Prism shape includes lifecycle stage, organization group, agent role, typed inputs and outputs, runtime adapter, reasoning-log expectations, and bundle layout.

5. Map dependencies in Prism terms.
   Track the preserved runtime, candidate `uv` bundles, reference KBs, backend profiles, workspace mounts, and capability source paths that the later Prism-facing shape will need.

6. Prefer adapter layers over destructive rewrites.
   The first good shape is usually preservation-first harmonization plus an explicit Prism-facing wrapper.

## Recommended External Route

1. `prism-external-reference-scoper`
2. `prism-external-capability-extractor`
3. `prism-agentic-shape-forger`
4. `prism-agent-contract-author`
5. `prism-quality-criteria-elicitor`
6. `prism-repo-cartographer`
7. `prism-dependency-cartographer`
8. `prism-slice-planner`
9. `prism-implementation-driver`
10. `prism-reflective-refinement-loop`
11. `prism-spec-verification-critic`

## Questions To Answer

- What source project and source paths are being preserved?
- What are the real entrypoints and runtime dependencies?
- Which dependencies should later become Prism bundle ids, reference KB ids, backend profiles, or workspace mounts?
- Which external capabilities deserve separate agent surfaces?
- Which capabilities are inference, maintenance, evaluation, or imported-runtime boundaries?
- What inputs and outputs are actually durable?
- What reasoning-log or artifact conventions already exist upstream?
- What should remain external, and what should later become more native?
