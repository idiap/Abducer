<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
-->

# Orchestration and Loops

## Deterministic Orchestrator

Canonical executable orchestrator:

- `skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py`

It resolves artifact defaults from KB slug and runs stage scripts in sequence.
By default it exports Markdown documents under `phyp/` into `.tex` and `.pdf`.
After execution it generates a run-level reasoning-log index.

Artifact storage is canonicalized and enforced by KB reference name:

- `KB/<slug>.kb.md` is bound to `artifacts/<slug>/`.
- Example: `KB/p-vs-np.kb.md` -> `artifacts/p-vs-np/`.
- Non-canonical alternatives (for example `artifacts/pvsnp/`) are rejected by the orchestrator.

## Intent Routing

### `cohere`

Prereqs: KB.

Runs:

1. `kb-proof-connector/scripts/analyze_kb_graph.py`
2. `kb-proof-connector/scripts/generate_phyp.py`
3. `kb-coherence-evaluator/scripts/evaluate_coherence.py`

Outputs:

- `artifacts/<slug>/connection-analysis.json`
- `artifacts/<slug>/connection-analysis.md`
- `phyp/<slug>.proof-hypotheses.yaml`
- `artifacts/<slug>/coherence-report.json`
- `artifacts/<slug>/coherence-report.md`

This is the preferred inference-mode name when the user wants the relational connector stage and immediate coherence formation in one routed step.

### `connect`

Runs:

1. `kb-proof-connector/scripts/analyze_kb_graph.py`
2. `kb-proof-connector/scripts/generate_phyp.py`

Outputs:

- `artifacts/<slug>/connection-analysis.json`
- `artifacts/<slug>/connection-analysis.md`
- `phyp/<slug>.proof-hypotheses.yaml`

### `coherence-eval`

Prereqs: analysis, phyp.

Runs:

1. `kb-coherence-evaluator/scripts/evaluate_coherence.py`

Outputs:

- `artifacts/<slug>/coherence-report.json`
- `artifacts/<slug>/coherence-report.md`

### `entrypoints`

Prereqs: concept evolution, analysis, phyp.

Runs:

1. `kb-entrypoint-finder/scripts/recommend_entrypoints.py`
2. `kb-entrypoint-pathfinder/scripts/synthesize_pathways.py`

If `coherence-report.json` exists, it is consumed automatically.

Outputs:

- `artifacts/<slug>/entrypoints.json`
- `artifacts/<slug>/entrypoints.md`
- `artifacts/<slug>/entrypoint-pathways.json`
- `artifacts/<slug>/entrypoint-pathways.md`

### `hardness`

Prereqs: concept, analysis, entrypoints, pathways, phyp.

Runs:

1. `kb-epistemic-hardness/scripts/articulate_hardness.py`

Outputs:

- `artifacts/<slug>/epistemic-hardness.json`
- `artifacts/<slug>/epistemic-hardness.md`

### `bridge-plan`

Prereqs: analysis, entrypoints, pathways, phyp, concept.

Runs:

1. `kb-concept-bridge-planner/scripts/plan_bridges.py`

If `coherence-report.json` exists, it is consumed automatically.

Outputs:

- `artifacts/<slug>/bridge-plan.json`
- `artifacts/<slug>/bridge-plan.md`

### `conjecture`

Prereqs: analysis, entrypoints, pathways, bridges, phyp.

Runs:

1. `kb-gap-abstraction-conjecturer/scripts/conjecture_gap_abstractions.py`

Optional inputs:

- `epistemic-hardness.json`

Outputs:

- `artifacts/<slug>/concept-gap-abstractions.json`
- `artifacts/<slug>/concept-gap-abstractions.md`

### `strategies`

Prereqs: entrypoints, pathways, bridges, phyp.

Runs:

1. `kb-novel-proof-strategist/scripts/design_strategies.py`

If `coherence-report.json` exists, it is consumed automatically.
If `concept-gap-abstractions.json` exists, it is consumed automatically.

Outputs:

- `artifacts/<slug>/proof-strategies.json`
- `artifacts/<slug>/proof-strategies.md`
- `artifacts/<slug>/novelty-maximizing-prompt.txt`

### `proof-sketch`

Prereqs: conjectures, strategies, bridges, phyp.

Runs:

1. `kb-proof-sketcher/scripts/generate_proof_sketches.py`

Optional inputs:

- `connection-analysis.json`
- `coherence-report.json`
- `epistemic-hardness.json`

Outputs:

- `artifacts/<slug>/proof-sketches.json`
- `artifacts/<slug>/proof-sketches.md`
- `artifacts/<slug>/paper-style-argument.md`

### `expert-paper`

Prereqs: final-stage artifacts for target KB (at minimum `phyp`).

Runs:

1. `kb-expert-paper-generator/scripts/generate_expert_paper.py`

Outputs:

- `artifacts/<slug>/expert-hypothesis-paper.json`
- `artifacts/<slug>/expert-hypothesis-paper.md`
- `artifacts/<slug>/expert-hypothesis-paper.tex`

This stage is bridge-first: it explains the main conceptual bridges, the proof sketches attached to them, and then situates supporting hypotheses inside that bridge portfolio.

### `hypothesis-eval`

Prereqs: analysis, phyp.

Runs:

1. `kb-hypothesis-evaluator/scripts/evaluate_hypotheses.py`

If `coherence-report.json` exists, it is consumed automatically.

Outputs:

- `artifacts/<slug>/hypothesis-evaluation.json`
- `artifacts/<slug>/hypothesis-evaluation.md`
- `phyp/<slug>.hypotheses-evaluated.md`

### `hypothesis-loop`

Prereqs: analysis, phyp.

Runs:

1. `kb-hypothesis-refutation-loop/scripts/iterate_hypotheses.py`

If `coherence-report.json` exists, it is consumed automatically.

Outputs:

- `artifacts/<slug>/hypothesis-refutation-loop.json`
- `artifacts/<slug>/hypothesis-refutation-loop.md`
- `phyp/<slug>.hypotheses-reviewed.md`
- `phyp/<slug>.hypotheses-reviewed.yaml`

### `revision-loop`

Prereqs: hypothesis-loop output.

Runs:

1. `kb-revision-loop/scripts/revise_ontology.py`

Optional inputs:

- `coherence-report.json`
- `epistemic-hardness.json`

Outputs:

- `artifacts/<slug>/revision-loop.json`
- `artifacts/<slug>/revision-loop.md`
- `artifacts/<slug>/kb.revised.md` (executable KB patch for next round)
- `artifacts/<slug>/phyp.revised.yaml` (executable hypothesis patch for next round)

### `interpretation-reports`

Prereqs: any subset of stage artifacts in `artifacts/<slug>/`.

Runs:

1. `kb-orchestrator/scripts/generate_interpretation_reports.py`

Outputs:

- `artifacts/<slug>/reasoning-process-report.md`
- `artifacts/<slug>/discovery-interpretation-report.md`

### `process-graph`

Prereqs: reasoning logs for target KB/run.

Runs:

1. `kb-orchestrator/scripts/generate_process_graph.py`

Outputs:

- `artifacts/<slug>/process-graph.json`
- `artifacts/<slug>/process-graph-evolution.json`
- `artifacts/<slug>/process-graph.html`
- `artifacts/<slug>/process-graph-states/state-*.json`

### `reasoning-dynamics`

Prereqs: process-graph evolution for target KB/run.

Runs:

1. `kb-orchestrator/scripts/generate_reasoning_dynamics.py`

Outputs:

- `artifacts/<slug>/reasoning-dynamics.json`
- `artifacts/<slug>/reasoning-dynamics.md`
- `artifacts/<slug>/reasoning-dynamics.html`

### `conceptual-dynamics`

Prereqs: surfaced reasoning logs for target KB/run plus whatever stage artifacts are already available.

Runs:

1. `kb-orchestrator/scripts/generate_conceptual_dynamics.py`

Outputs:

- `artifacts/<slug>/conceptual-dynamics.json`
- `artifacts/<slug>/conceptual-dynamics.md`
- `artifacts/<slug>/conceptual-dynamics.html`

## Automatic Log Index

For all orchestrator intents, a run-level reasoning-log index is generated:

- `artifacts/<slug>/reasoning-log-index.json`
- `artifacts/<slug>/reasoning-log-index.md`

This index groups logs by `Run ID`, summarizes status by agent, and flags missing expected stage logs.

A parallel human-facing surfaced index is also generated:

- `artifacts/<slug>/reasoning-surface-index.json`
- `artifacts/<slug>/reasoning-surface-index.md`

This surfaced index summarizes conceptual movement, dominant foci, and the human-readable reasoning timeline across agents.

A second human-facing dashboard is generated in parallel:

- `artifacts/<slug>/conceptual-dynamics.json`
- `artifacts/<slug>/conceptual-dynamics.md`
- `artifacts/<slug>/conceptual-dynamics.html`

This dashboard tracks concept counts, target-concept evolution, hypothesis lifecycles, reasoning-type diversity, proof-strategy families, and surfaced conceptual moves over time.

## Process Graph Visualization

Use the process-graph generator to get a dynamic typed graph and intermediary state snapshots of workflow evolution:

- `skills/orchestration/kb-orchestrator/scripts/generate_process_graph.py`

Outputs:

- `artifacts/<slug>/process-graph.json` (final typed graph)
- `artifacts/<slug>/process-graph-evolution.json` (state timeline + final graph)
- `artifacts/<slug>/process-graph.html` (interactive replay: slider + playback)
- `artifacts/<slug>/process-graph-states/state-*.json` (intermediary graph states)

## Reasoning Dynamics Dashboard

Use the reasoning-dynamics generator to quantify and visualize inferential behavior over the process graph timeline:

- `skills/orchestration/kb-orchestrator/scripts/generate_reasoning_dynamics.py`

Outputs:

- `artifacts/<slug>/reasoning-dynamics.json` (machine-readable metric timeline + summary)
- `artifacts/<slug>/reasoning-dynamics.md` (human-readable interpretation)
- `artifacts/<slug>/reasoning-dynamics.html` (interactive dashboard with replay)

## Conceptual Dynamics Dashboard

Use the conceptual-dynamics generator to monitor the evolution of concepts, bridge objects, hypotheses, proof strategies, and surfaced prompt-level taxonomy over the active run:

- `skills/orchestration/kb-orchestrator/scripts/generate_conceptual_dynamics.py`

Outputs:

- `artifacts/<slug>/conceptual-dynamics.json` (machine-readable conceptual timeline + summary)
- `artifacts/<slug>/conceptual-dynamics.md` (human-readable conceptual summary)
- `artifacts/<slug>/conceptual-dynamics.html` (interactive replay dashboard)

### `abductive-loop`

Runs deterministic pieces of the abductive cycle:

1. `connect`
2. `coherence-eval`
3. prompt checkpoint for `kb-abduce` + `kb-deduce`
4. `hypothesis-eval`
5. `hypothesis-loop`
6. `revision-loop`
7. `interpretation-reports`
8. `process-graph`
9. `reasoning-dynamics`
10. `conceptual-dynamics`

### `pipeline`

Runs full deterministic chain:

1. connect
2. coherence-eval
3. entrypoints
4. hardness
5. bridge-plan
6. conjecture
7. strategies
8. proof-sketch
9. hypothesis-eval
10. hypothesis-loop
11. revision-loop
12. interpretation-reports
13. process-graph
14. reasoning-dynamics
15. conceptual-dynamics
16. expert-paper

## Abductive Loop Semantics

Core objective:

- search the KB for highest informative intervention points,
- propose and test bridge and conceptual hypotheses,
- retain hypotheses that improve derivability and global coherence.

Round logic in `iterate_hypotheses.py`:

- pending hypotheses are those not hard-resolved (`supported|refuted`),
- per-round thresholds can anneal,
- optional per-round evidence is loaded from:
  - `<round-evidence-dir>/round-<n>.json`
  - `<round-evidence-dir>/round-<n>.yaml`,
- default policy stops after round 1 if no new evidence and annealing is disabled,
- optional force mode yields provisional, not hard, resolution,
- belief-revision step demotes or rejects coherence-negative hypotheses based on configured thresholds.

## Typical Commands

### Full pipeline

```bash
python3 skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent pipeline \
  --kb KB/p-vs-np.kb.md \
  --concept artifacts/p-vs-np/concept-evolution.md \
  --rounds 3 \
  --export-phyp-docs \
  --phyp-doc-pattern "*.md" \
  --phyp-pdf-engine xelatex
```

### Coherence-only stage

```bash
python3 skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent coherence-eval \
  --kb KB/p-vs-np.kb.md \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml
```

### Hypothesis loop with round evidence

```bash
python3 skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent hypothesis-loop \
  --kb KB/p-vs-np.kb.md \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  --coherence artifacts/p-vs-np/coherence-report.json \
  --round-evidence-dir artifacts/p-vs-np/round-evidence \
  --rounds 3
```

### Revision loop only

```bash
python3 skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent revision-loop \
  --kb KB/p-vs-np.kb.md \
  --phyp phyp/p-vs-np.hypotheses-reviewed.yaml \
  --coherence artifacts/p-vs-np/coherence-report.json
```

### Generate human-readable interpretation reports only

```bash
python3 skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent interpretation-reports \
  --kb KB/p-vs-np.kb.md
```

### Generate process graph + reasoning dynamics only

```bash
python3 skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent reasoning-dynamics \
  --kb KB/p-vs-np.kb.md \
  --no-export-phyp-docs
```

### Export phyp Markdown to LaTeX and PDF only

```bash
python3 skills/orchestration/kb-orchestrator/scripts/export_phyp_docs.py \
  --phyp-dir phyp \
  --pattern "*.md" \
  --pdf-engine xelatex
```

## Integrated P vs NP Runner

Direct integrated test:

```bash
python3 skills/discovery/kb-novel-proof-strategist/scripts/run_integrated_pvsnp.py
```

This script runs:

1. coherence evaluator
2. hardness
3. bridge planner
4. strategist
5. hypothesis evaluator
6. refutation loop
7. revision loop
8. phyp document export
9. interpretation reports

## P vs NP Parallel API Marathon

The discovery-marathon runner can execute independent P vs NP branch agents in
parallel through Azure/OpenAI-compatible Responses APIs. This is not a parallel
state machine: branch workers generate candidate packets concurrently, then the
cycle reducer restores scheduler order and writes state only after all packets
validate.

```bash
python agentic/scripts/run_discovery_marathon_job.py \
  --target p-vs-np-target \
  --duration-seconds 7200 \
  --branch-engine api \
  --min-cycle-seconds 600 \
  --max-active-branches 3 \
  --parallel-branches \
  --api-max-workers 3 \
  --api-request-spacing-seconds 2
```

Each parallel cycle includes `parallel_execution` and `parallel_synthesis`.
The synthesis cites branch IDs in scheduler order, states common proof
obligations, detects cross-branch conflicts, records no-go opportunities, and
promotes the next analyses with pressure-specific payoff tests.

Validation:

```bash
python agentic/scripts/validate_parallel_api_marathon.py
python agentic/scripts/validate_discovery_marathon_state.py
```
