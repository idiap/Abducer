<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Abductive Loop Protocol

## Objective

Systematically traverse the KB and prioritize the highest-informative intervention points that can unlock useful proof pathways.

## Loop Stages

0. **Entrypoint selection (recommended)**
Run `kb-entrypoint-finder` and `kb-entrypoint-pathfinder` to choose top conceptual anchors before looping.

1. **Relational scan**
Run `kb-proof-connector` and collect:
- `top_interventions`
- `connection_candidates`
- `concept_graph`

2. **Coherentist baseline**
Run `kb-coherence-evaluator` to compute:
- global coherence profile
- per-hypothesis explanatory power and coherence deltas

3. **Hypothesis generation**
For each top intervention point, run `kb-abduce` to produce minimal premise/link hypotheses.
Persist hypothesis candidates in `phyp/<kb-slug>.proof-hypotheses.yaml`.

4. **Consequence test**
Run `kb-deduce` on each hypothesis set and classify outcomes as:
- `entailed`
- `conditionally-entailed`
- `not-derived`

5. **Hypothesis evaluation**
Run `kb-hypothesis-evaluator` to classify each hypothesis as:
- `supported`
- `refuted`
- `inconclusive`

6. **Iteration over unresolved hypotheses**
Run `kb-hypothesis-refutation-loop` over unresolved hypotheses to converge toward support/refutation.
Feed round evidence (`round-<n>.json|yaml`) from abduce/deduce outcomes when available.
Apply coherence-aware belief revision after each round.

7. **Ontology and representation revision**
Run `kb-revision-loop` when unresolved clusters persist to trigger concept splitting, definition repair, regime switching, and KB re-encoding actions.

8. **Retention and pruning**
Keep hypotheses that maximize coverage, deductive yield, and non-negative coherence contribution; prune low-yield or contradictory links.

9. **Process instrumentation**
Run `kb-orchestrator/generate_process_graph.py` then `kb-orchestrator/generate_reasoning_dynamics.py` to capture typed inferential process evolution and metric dynamics.

## Stopping Criteria

Stop when any condition holds:

- No improvement in intervention score after one full round.
- Global coherence does not improve and no revision action resolves stalled clusters.
- No new conditionally-entailed claims are produced.
- No new round evidence is available for unresolved hypotheses.
- Round budget reached (default: 3).

## Tracking Fields

Track per round:

- Number of targets evaluated
- Number of hypotheses proposed
- Number of hypotheses supported
- Number of hypotheses refuted
- Number of hypotheses retained
- Number of new derived statements
- Highest-yield intervention point
- Global coherence
- Number of belief-revision actions
- Number of revision-loop actions accepted

## Artifact Paths

- Connector analysis JSON: `artifacts/<kb-slug>/connection-analysis.json`
- Connector analysis Markdown: `artifacts/<kb-slug>/connection-analysis.md`
- Entrypoint ranking: `artifacts/<kb-slug>/entrypoints.json`
- Entrypoint pathways: `artifacts/<kb-slug>/entrypoint-pathways.json`
- Proof hypotheses: `phyp/<kb-slug>.proof-hypotheses.yaml`
- Coherence report: `artifacts/<kb-slug>/coherence-report.json`
- Hypothesis evaluation: `artifacts/<kb-slug>/hypothesis-evaluation.json`
- Hypothesis refutation loop: `artifacts/<kb-slug>/hypothesis-refutation-loop.json`
- Revision loop: `artifacts/<kb-slug>/revision-loop.json`
- Process graph: `artifacts/<kb-slug>/process-graph.json`
- Process graph evolution: `artifacts/<kb-slug>/process-graph-evolution.json`
- Reasoning dynamics: `artifacts/<kb-slug>/reasoning-dynamics.json`
- Reasoning dynamics report: `artifacts/<kb-slug>/reasoning-dynamics.md`
- Reasoning dynamics dashboard: `artifacts/<kb-slug>/reasoning-dynamics.html`
