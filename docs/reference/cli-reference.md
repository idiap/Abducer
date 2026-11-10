<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# CLI Reference

This reference covers the maintained KB theorem-assistance scripts and the canonical
discovery entrypoint below. Run commands from the repository root using the locked
environment. Workflow-local scripts retain their own `--help` and runbook contracts;
this page is not an exhaustive list of every validator or research utility.

## Ingestion and Parsing

### `latex-kb-ingest/scripts/chunk_sources.py`

```bash
python3 skills/ingest/latex-kb-ingest/scripts/chunk_sources.py \
  --source <url-or-path> [--source <url-or-path> ...] \
  --output artifacts/<slug>/chunks.jsonl \
  [--source-file sources.txt] \
  [--chunk-size 2200] \
  [--overlap 250] \
  [--timeout 20] \
  [--manifest artifacts/<slug>/source-manifest.json]
```

### `latex-kb-ingest/scripts/kb_writeback.py`

```bash
python3 skills/ingest/latex-kb-ingest/scripts/kb_writeback.py \
  --kb KB/<problem>.kb.md \
  --statements artifacts/<slug>/statements.json \
  [--section-policy status|canonical|derived] \
  [--change-note "..."] \
  [--dry-run]
```

### `pvsnp-kb-parser/scripts/parse_report.py`

```bash
python3 skills/ingest/pvsnp-kb-parser/scripts/parse_report.py \
  --input /path/to/deep-research-report.md \
  --output-statements artifacts/p-vs-np/deep-research-report.statements.json \
  [--source-id src.001] \
  [--citation /path/to/source] \
  [--max-informal-chars 280] \
  [--kb KB/p-vs-np.kb.md] \
  [--init-kb-from-template KB/problem-template.kb.md] \
  [--section-policy status|canonical|derived] \
  [--change-note "..."] \
  [--writeback-script skills/ingest/latex-kb-ingest/scripts/kb_writeback.py] \
  [--dry-run]
```

## Relational Analysis and Hypothesis Generation

### `kb-proof-connector/scripts/analyze_kb_graph.py`

```bash
python3 skills/discovery/kb-proof-connector/scripts/analyze_kb_graph.py \
  --kb KB/<problem>.kb.md \
  [--top-k 15] \
  [--min-similarity 0.12] \
  [--max-connections 40] \
  [--loop-rounds 3] \
  [--include-status accepted] [--include-status tentative] \
  [--output-json artifacts/<slug>/connection-analysis.json] \
  [--output-md artifacts/<slug>/connection-analysis.md]
```

### `kb-proof-connector/scripts/generate_phyp.py`

```bash
python3 skills/discovery/kb-proof-connector/scripts/generate_phyp.py \
  --analysis artifacts/<slug>/connection-analysis.json \
  --kb KB/<problem>.kb.md \
  --output phyp/<slug>.proof-hypotheses.yaml \
  [--top-links 20] \
  [--top-interventions 10] \
  [--top-conceptual 12]
```

### `kb-coherence-evaluator/scripts/evaluate_coherence.py`

```bash
python3 skills/discovery/kb-coherence-evaluator/scripts/evaluate_coherence.py \
  --kb KB/<problem>.kb.md \
  --analysis artifacts/<slug>/connection-analysis.json \
  --phyp phyp/<slug>.proof-hypotheses.yaml \
  [--output-json artifacts/<slug>/coherence-report.json] \
  [--output-md artifacts/<slug>/coherence-report.md]
```

## Entrypoint and Pathway Synthesis

### `kb-entrypoint-finder/scripts/recommend_entrypoints.py`

```bash
python3 skills/discovery/kb-entrypoint-finder/scripts/recommend_entrypoints.py \
  --kb KB/<problem>.kb.md \
  --concept artifacts/<slug>/concept-evolution.md \
  --analysis artifacts/<slug>/connection-analysis.json \
  --phyp phyp/<slug>.proof-hypotheses.yaml \
  [--coherence-report artifacts/<slug>/coherence-report.json] \
  [--include-status accepted] [--include-status tentative] \
  [--top-k 20] \
  [--output-json artifacts/<slug>/entrypoints.json] \
  [--output-md artifacts/<slug>/entrypoints.md]
```

### `kb-entrypoint-pathfinder/scripts/synthesize_pathways.py`

```bash
python3 skills/discovery/kb-entrypoint-pathfinder/scripts/synthesize_pathways.py \
  --recommendations artifacts/<slug>/entrypoints.json \
  --phyp phyp/<slug>.proof-hypotheses.yaml \
  --analysis artifacts/<slug>/connection-analysis.json \
  [--top-entrypoints 8] \
  [--max-hypotheses-per-path 4] \
  [--max-links-per-path 3] \
  [--output-json artifacts/<slug>/entrypoint-pathways.json] \
  [--output-md artifacts/<slug>/entrypoint-pathways.md]
```

## Hardness, Bridges, Strategies

### `kb-epistemic-hardness/scripts/articulate_hardness.py`

```bash
python3 skills/discovery/kb-epistemic-hardness/scripts/articulate_hardness.py \
  --problem "P vs NP" \
  --kb KB/p-vs-np.kb.md \
  --concept artifacts/p-vs-np/concept-evolution.md \
  --analysis artifacts/p-vs-np/connection-analysis.json \
  --entrypoints artifacts/p-vs-np/entrypoints.json \
  --pathways artifacts/p-vs-np/entrypoint-pathways.json \
  --phyp phyp/p-vs-np.proof-hypotheses.yaml \
  [--output-json artifacts/p-vs-np/epistemic-hardness.json] \
  [--output-md artifacts/p-vs-np/epistemic-hardness.md]
```

### `kb-concept-bridge-planner/scripts/plan_bridges.py`

```bash
python3 skills/discovery/kb-concept-bridge-planner/scripts/plan_bridges.py \
  --analysis artifacts/<slug>/connection-analysis.json \
  --entrypoints artifacts/<slug>/entrypoints.json \
  --pathways artifacts/<slug>/entrypoint-pathways.json \
  --phyp phyp/<slug>.proof-hypotheses.yaml \
  --concept artifacts/<slug>/concept-evolution.md \
  [--coherence-report artifacts/<slug>/coherence-report.json] \
  [--top-k 20] \
  [--output-json artifacts/<slug>/bridge-plan.json] \
  [--output-md artifacts/<slug>/bridge-plan.md]
```

### `kb-gap-abstraction-conjecturer/scripts/conjecture_gap_abstractions.py`

```bash
python3 skills/discovery/kb-gap-abstraction-conjecturer/scripts/conjecture_gap_abstractions.py \
  --analysis artifacts/<slug>/connection-analysis.json \
  --entrypoints artifacts/<slug>/entrypoints.json \
  --pathways artifacts/<slug>/entrypoint-pathways.json \
  --bridges artifacts/<slug>/bridge-plan.json \
  --phyp phyp/<slug>.proof-hypotheses.yaml \
  [--hardness artifacts/<slug>/epistemic-hardness.json] \
  [--top-bridges 12] \
  [--max-conjectures-per-bridge 3] \
  [--output-json artifacts/<slug>/concept-gap-abstractions.json] \
  [--output-md artifacts/<slug>/concept-gap-abstractions.md]
```

### `kb-novel-proof-strategist/scripts/design_strategies.py`

```bash
python3 skills/discovery/kb-novel-proof-strategist/scripts/design_strategies.py \
  --entrypoints artifacts/<slug>/entrypoints.json \
  --pathways artifacts/<slug>/entrypoint-pathways.json \
  --bridges artifacts/<slug>/bridge-plan.json \
  --phyp phyp/<slug>.proof-hypotheses.yaml \
  [--coherence-report artifacts/<slug>/coherence-report.json] \
  [--conjectures artifacts/<slug>/concept-gap-abstractions.json] \
  [--top-k 6] \
  [--output-json artifacts/<slug>/proof-strategies.json] \
  [--output-md artifacts/<slug>/proof-strategies.md] \
  [--output-prompt artifacts/<slug>/novelty-maximizing-prompt.txt]
```

### `kb-proof-sketcher/scripts/generate_proof_sketches.py`

```bash
python3 skills/discovery/kb-proof-sketcher/scripts/generate_proof_sketches.py \
  --conjectures artifacts/<slug>/concept-gap-abstractions.json \
  --strategies artifacts/<slug>/proof-strategies.json \
  --bridges artifacts/<slug>/bridge-plan.json \
  --phyp phyp/<slug>.proof-hypotheses.yaml \
  [--kb KB/<problem>.kb.md] \
  [--analysis artifacts/<slug>/connection-analysis.json] \
  [--coherence-report artifacts/<slug>/coherence-report.json] \
  [--hardness artifacts/<slug>/epistemic-hardness.json] \
  [--top-k 6] \
  [--output-json artifacts/<slug>/proof-sketches.json] \
  [--output-md artifacts/<slug>/proof-sketches.md] \
  [--output-paper-md artifacts/<slug>/paper-style-argument.md]
```

### `kb-expert-paper-generator/scripts/generate_expert_paper.py`

```bash
python3 skills/reporting/kb-expert-paper-generator/scripts/generate_expert_paper.py \
  --kb KB/<problem>.kb.md \
  [--kb-ref <kb-ref>] \
  [--artifacts-dir artifacts/<slug>] \
  [--phyp phyp/<slug>.proof-hypotheses.yaml] \
  [--top-k 8] \
  [--min-score 0.52] \
  [--output-json artifacts/<slug>/expert-hypothesis-paper.json] \
  [--output-md artifacts/<slug>/expert-hypothesis-paper.md] \
  [--output-tex artifacts/<slug>/expert-hypothesis-paper.tex]
```

This report is bridge-first: it explains the main conceptual bridges and their proof sketches before turning to supporting hypothesis recommendations.

### `kb-framework-state-formalizer/scripts/generate_framework_state_formalization.py`

```bash
python3 skills/discovery/kb-framework-state-formalizer/scripts/generate_framework_state_formalization.py \
  [--readme README.md] \
  [--architecture docs/architecture/architecture.md] \
  [--orchestration docs/architecture/orchestration.md] \
  [--skills-doc docs/reference/skills.md] \
  [--example-report artifacts/markov-kakutani-fixed-point-theorem/discovery-simulation/simulation-report.md] \
  [--example-concept-evolution artifacts/markov-kakutani-fixed-point-theorem/discovery-simulation/iter-008/concept-evolution.md] \
  [--output-json artifacts/framework/framework-state-formalization.json] \
  [--output-tex docs/publications/framework-state-formalization.tex]
```

### `kb-novel-proof-strategist/scripts/run_integrated_pvsnp.py`

```bash
python3 skills/discovery/kb-novel-proof-strategist/scripts/run_integrated_pvsnp.py
```

## Hypothesis Evaluation and Loop

### `kb-hypothesis-evaluator/scripts/evaluate_hypotheses.py`

```bash
python3 skills/evaluation/kb-hypothesis-evaluator/scripts/evaluate_hypotheses.py \
  --kb KB/<problem>.kb.md \
  --phyp phyp/<slug>.proof-hypotheses.yaml \
  [--analysis artifacts/<slug>/connection-analysis.json] \
  [--coherence-report artifacts/<slug>/coherence-report.json] \
  [--evidence-json artifacts/<slug>/evidence.json] \
  [--support-threshold 0.62] \
  [--refute-threshold 0.62] \
  [--margin 0.08] \
  [--force-resolution | --no-force-resolution] \
  [--output-json artifacts/<slug>/hypothesis-evaluation.json] \
  [--output-md artifacts/<slug>/hypothesis-evaluation.md] \
  [--output-phyp-md phyp/<slug>.hypotheses-evaluated.md] \
  [--output-phyp phyp/<slug>.hypotheses-evaluated.yaml]
```

### `kb-hypothesis-refutation-loop/scripts/iterate_hypotheses.py`

```bash
python3 skills/evaluation/kb-hypothesis-refutation-loop/scripts/iterate_hypotheses.py \
  --kb KB/<problem>.kb.md \
  --phyp phyp/<slug>.proof-hypotheses.yaml \
  [--analysis artifacts/<slug>/connection-analysis.json] \
  [--coherence-report artifacts/<slug>/coherence-report.json] \
  [--rounds 3] \
  [--start-support-threshold 0.66] \
  [--start-refute-threshold 0.66] \
  [--threshold-step 0.05] \
  [--margin 0.08] \
  [--min-coherence-keep 0.0] \
  [--severe-negative-coherence -0.12] \
  [--round-evidence-dir artifacts/<slug>/round-evidence] \
  [--anneal-without-new-evidence | --no-anneal-without-new-evidence] \
  [--force-final-resolution | --no-force-final-resolution] \
  [--output-json artifacts/<slug>/hypothesis-refutation-loop.json] \
  [--output-md artifacts/<slug>/hypothesis-refutation-loop.md] \
  [--output-phyp-md phyp/<slug>.hypotheses-reviewed.md] \
  [--output-phyp phyp/<slug>.hypotheses-reviewed.yaml]
```

### `kb-revision-loop/scripts/revise_ontology.py`

```bash
python3 skills/evaluation/kb-revision-loop/scripts/revise_ontology.py \
  --kb KB/<problem>.kb.md \
  --phyp phyp/<slug>.hypotheses-reviewed.yaml \
  --hypothesis-loop artifacts/<slug>/hypothesis-refutation-loop.json \
  [--coherence-report artifacts/<slug>/coherence-report.json] \
  [--hardness artifacts/<slug>/epistemic-hardness.json] \
  [--apply-actions | --no-apply-actions] \
  [--output-json artifacts/<slug>/revision-loop.json] \
  [--output-md artifacts/<slug>/revision-loop.md] \
  [--output-patched-kb artifacts/<slug>/kb.revised.md] \
  [--output-patched-phyp artifacts/<slug>/phyp.revised.yaml]
```

## Orchestration

### `kb-orchestrator/scripts/run_orchestrator.py`

```bash
python3 skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent cohere|connect|coherence-eval|interpretation-reports|process-graph|reasoning-dynamics|conceptual-dynamics|entrypoints|hardness|bridge-plan|conjecture|strategies|proof-sketch|expert-paper|hypothesis-eval|hypothesis-loop|revision-loop|abductive-loop|pipeline \
  --kb KB/<problem>.kb.md \
  [--concept artifacts/<slug>/concept-evolution.md] \
  [--analysis artifacts/<slug>/connection-analysis.json] \
  [--entrypoints artifacts/<slug>/entrypoints.json] \
  [--pathways artifacts/<slug>/entrypoint-pathways.json] \
  [--phyp phyp/<slug>.proof-hypotheses.yaml] \
  [--coherence artifacts/<slug>/coherence-report.json] \
  [--bridges artifacts/<slug>/bridge-plan.json] \
  [--artifacts-dir artifacts/<slug>] \
  [--round-evidence-dir artifacts/<slug>/round-evidence] \
  [--rounds 3] \
  [--export-phyp-docs | --no-export-phyp-docs] \
  [--phyp-doc-pattern "*.md"] \
  [--phyp-pdf-engine xelatex] \
  [--python /path/to/python]
```

`cohere` runs `connect` followed immediately by `coherence-eval`; use it when the goal is inference over a coherent relational theory rather than connector output alone.

`run_orchestrator.py` enforces canonical artifact routing from the reference KB name:

- `KB/<slug>.kb.md` -> `artifacts/<slug>/`
- for `KB/p-vs-np.kb.md`, canonical path is `artifacts/p-vs-np/`
- passing a non-canonical `--artifacts-dir` is rejected.

### `kb-orchestrator/scripts/generate_interpretation_reports.py`

```bash
python3 skills/orchestration/kb-orchestrator/scripts/generate_interpretation_reports.py \
  --artifacts-dir artifacts/<slug> \
  [--kb KB/<problem>.kb.md] \
  [--output-process-md artifacts/<slug>/reasoning-process-report.md] \
  [--output-discovery-md artifacts/<slug>/discovery-interpretation-report.md]
```

### `kb-orchestrator/scripts/generate_reasoning_log_index.py`

```bash
python3 skills/orchestration/kb-orchestrator/scripts/generate_reasoning_log_index.py \
  --artifacts-dir artifacts/<slug> \
  [--kb KB/<problem>.kb.md] \
  [--reasoning-log-root artifacts/reasoning-logs] \
  [--run-id <run-id>] \
  [--expected-agent kb-orchestrator] [--expected-agent kb-proof-connector] \
  [--expected-stage connect.analyze] [--expected-stage coherence-eval] \
  [--exclude-log-path artifacts/reasoning-logs/<agent>/<timestamp>-<pid>.md] \
  [--output-json artifacts/<slug>/reasoning-log-index.json] \
  [--output-md artifacts/<slug>/reasoning-log-index.md]
```

### `kb-orchestrator/scripts/generate_reasoning_surface_index.py`

```bash
python3 skills/orchestration/kb-orchestrator/scripts/generate_reasoning_surface_index.py \
  --artifacts-dir artifacts/<slug> \
  [--kb KB/<problem>.kb.md] \
  [--reasoning-surface-root artifacts/reasoning-surfaces] \
  [--run-id <run-id>] \
  [--expected-agent kb-orchestrator] [--expected-agent kb-proof-sketcher] \
  [--exclude-surface-path artifacts/reasoning-surfaces/<agent>/<timestamp>-<pid>.json] \
  [--output-json artifacts/<slug>/reasoning-surface-index.json] \
  [--output-md artifacts/<slug>/reasoning-surface-index.md]
```

### `kb-orchestrator/scripts/generate_process_graph.py`

```bash
python3 skills/orchestration/kb-orchestrator/scripts/generate_process_graph.py \
  --artifacts-dir artifacts/<slug> \
  [--reasoning-log-root artifacts/reasoning-logs] \
  [--kb KB/<problem>.kb.md] \
  [--run-id <run-id>] \
  [--include-agent kb-orchestrator] \
  [--exclude-agent kb-process-graph-visualizer] \
  [--exclude-log-path artifacts/reasoning-logs/<agent>/<timestamp>-<pid>.md] \
  [--output-json artifacts/<slug>/process-graph.json] \
  [--output-evolution-json artifacts/<slug>/process-graph-evolution.json] \
  [--output-html artifacts/<slug>/process-graph.html] \
  [--states-dir artifacts/<slug>/process-graph-states]
```

If `--run-id` is not provided, selection defaults to the latest end-to-end KB orchestrator run (`pipeline`/`abductive-loop`), then falls back to the latest orchestrator run for that KB if no end-to-end run is available.

### `kb-orchestrator/scripts/generate_reasoning_dynamics.py`

```bash
python3 skills/orchestration/kb-orchestrator/scripts/generate_reasoning_dynamics.py \
  --artifacts-dir artifacts/<slug> \
  [--process-graph-evolution artifacts/<slug>/process-graph-evolution.json] \
  [--output-json artifacts/<slug>/reasoning-dynamics.json] \
  [--output-md artifacts/<slug>/reasoning-dynamics.md] \
  [--output-html artifacts/<slug>/reasoning-dynamics.html]
```

### `kb-orchestrator/scripts/generate_conceptual_dynamics.py`

```bash
python3 skills/orchestration/kb-orchestrator/scripts/generate_conceptual_dynamics.py \
  --artifacts-dir artifacts/<slug> \
  [--kb KB/<problem>.kb.md] \
  [--kb-ref <slug>] \
  [--reasoning-surface-root artifacts/reasoning-surfaces] \
  [--run-id <run-id>] \
  [--output-json artifacts/<slug>/conceptual-dynamics.json] \
  [--output-md artifacts/<slug>/conceptual-dynamics.md] \
  [--output-html artifacts/<slug>/conceptual-dynamics.html]
```

### `kb-orchestrator/scripts/export_phyp_docs.py`

```bash
python3 skills/orchestration/kb-orchestrator/scripts/export_phyp_docs.py \
  [--phyp-dir phyp] \
  [--pattern "*.md"] \
  [--include-readme | --no-include-readme] \
  [--pdf-engine xelatex]
```

## Canonical discovery runtime

The theory-first discovery cycle is a separate surface from the KB orchestrator:

```bash
uv run python agentic/scripts/run_canonical_discovery_cycle.py --help
```

Required options are `--request` (exact cycle-request JSON) and `--state-root`
(canonical transaction store). Optional `--workspace` bounds artifact access and
`--output` writes a projection. The request must already bind the target, run, state,
operator requests, receipts, and semantic role map. The command validates and commits
that evidence; it does not replace the producer stages or accept a plain-language
request as a ready cycle. Do not use a working canonical state root as a smoke test.

Read [execution surfaces](../getting-started/execution-surfaces.md),
[named workflows](../architecture/named-workflows.md), and
[canonical publication](../architecture/canonical-discovery-publication.md) before
execution. The transaction store remains authoritative over the optional projection.
