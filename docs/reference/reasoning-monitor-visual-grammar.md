<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reasoning Monitor Visual Grammar

The reasoning monitor is an observability console for mathematical work. It should make target commitments, frontier pressure, route creativity, validation gates, proof debt, and stale-workflow protection visible without implying that visual progress is theorem progress.

## Surface Model

- Target spine: fixed commitments that every active route must preserve.
- Dependency frontier: live mathematical work queue, shown as tension rather than success.
- Conceptual pressure: places where the current frame creates route-changing opportunities or failures.
- Candidate routes: speculative transformations with target relevance, drift risk, and validation packets.
- Validation gates: hard checks that separate a promising route from a promoted obligation.
- Proof debt: unresolved work, intentionally prominent.
- Evidence ledger: artifact paths that ground each claim.
- Drift guard: stale-workflow and historical-artifact isolation.

## Dark Theme

Use a dark graphite base with several distinct accent families, avoiding a one-note blue or purple surface.

- Page base: `#090d12`
- Panel base: `#111821`
- Raised surface: `#17202b`
- Hairline: `#263241`
- Text primary: `#eef4f8`
- Text secondary: `#a9b5c2`
- Target gold: `#f2c94c`
- Frontier cyan: `#4cc9f0`
- Pressure magenta: `#d65db1`
- Route green: `#64d68a`
- Validation blue: `#7aa2ff`
- Drift amber: `#ffb454`
- Failure rose: `#ff6678`

## Tokens

Map every visual emphasis to the monitor packet rather than ad hoc styling.

| Token | Use |
| --- | --- |
| `target-gold` | Non-disposable target commitments |
| `frontier-cyan` | Dependency frontier, graph work, live unresolved nodes |
| `pressure-magenta` | Conceptual pressure and creativity signals |
| `route-green` | Candidate routes with proof-queue disposition |
| `route-blue` | Discovery branch or exploratory candidates |
| `guard-amber` | Stale-workflow isolation and drift risk |
| `failure-rose` | Blocks, critical findings, high drift risk |

## Status Semantics

- `evidence-backed`: grounded in artifacts, still not proof unless the event says so.
- `proof-obligation`: promising only as a named obligation; unresolved by default.
- `conjectural`: idea-generating, not action-worthy without validation.
- `blocked`: cannot progress without repair.
- `watch/archive`: valid to remember, not worth active horizon budget.

## Layout Rules

- First viewport must show active target ID, target commitments, frontier count, candidate count, proof debt, stale findings, and the filter controls.
- Keep report sections as operational tabs: Overview, Timeline, Frontier, Candidates, Proof Debt, Evidence, Drift.
- Do not hide uncertainty inside tooltips; show uncertainty and proof obligations in expandable details.
- Preserve dense reading: compact headings, stable cards, no marketing hero, no decorative background orbs.
- Mobile layout stacks panels in a single column with filters above the content.

## Failure Cases

Reject a report if it makes all routes look equally successful, omits proof debt, hides stale-workflow findings, fails to expose evidence paths, or uses decorative polish that obscures target relevance and uncertainty.
