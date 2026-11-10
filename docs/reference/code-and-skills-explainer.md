<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Code and Skills Explainer

This document is a practical code-level guide to the repository. It explains:

- the conceptual model behind the project,
- the purpose of each skill,
- how the main scripts implement the reasoning workflow,
- where to annotate or extend behavior safely.

## 1) Conceptual Model

The project is an informal theorem-assistant workflow over Markdown KB files.

Core idea:

- represent mathematical knowledge as structured statement blocks in [`KB/*.kb.md`](../../KB),
- generate and evaluate hypotheses in [`phyp/*.yaml`](../../phyp),
- orchestrate reasoning loops across multiple skills,
- track every step with auditable internal reasoning logs, surfaced conceptual reasoning views, and process/dynamics artifacts.

Reasoning modes supported:

- explanatory (`kb-explain`)
- deductive (`kb-deduce`)
- abductive (`kb-abduce`)
- inductive (`kb-induce`, scoped to late-stage proof-route generalization)
- inference-quality probing (`premise-completeness-prober`, `entailment-gap-auditor`, `regime-shift-auditor`, `counterfactual-route-prober`, `counterexample-hunter`)
- coherentist evaluation and belief revision (`kb-coherence-evaluator`, `kb-revision-loop`)

Shared prompt design for bridge planning, conjecture, and proof-sketching is documented in [`../research-methods/epistemic-prompt-framework.md`](../research-methods/epistemic-prompt-framework.md); those stages now separate bridge-object shaping from positive/negative proof-space assessment.

## 2) Core Data Objects

Primary object families:

- `statement`: definition/theorem/lemma/axiom/conjecture entries parsed from KB fenced YAML blocks.
- `hypothesis`: bridge/intervention/conceptual candidates in `phyp`.
- `analysis`: connector output (`connection-analysis.json`) with intervention scores and cross-component candidates.
- `coherence report`: typed coherence graph + global/local signals.
- `loop artifacts`: evaluation, refutation-loop, revision-loop, bridge plan, strategy portfolio.
- `reasoning logs`: per-agent internal markdown traces under `artifacts/reasoning-logs/`.
- `reasoning surfaces`: per-agent human-facing markdown and JSON conceptual traces under `artifacts/reasoning-surfaces/`, now optionally carrying proof-discovery-language programs plus material-inference operations and judgments.

## 3) Skill Catalog (Concept and Purpose)

| Skill | Conceptual purpose | Primary script(s) |
|---|---|---|
| `latex-kb-ingest` | Turn source text into KB-ready statement chunks and perform structured KB writeback. | [chunk_sources.py](../../skills/ingest/latex-kb-ingest/scripts/chunk_sources.py), [kb_writeback.py](../../skills/ingest/latex-kb-ingest/scripts/kb_writeback.py) |
| `pvsnp-kb-parser` | Convert a deep-research report into normalized P vs NP statement objects. | [parse_report.py](../../skills/ingest/pvsnp-kb-parser/scripts/parse_report.py) |
| `kb-proof-connector` | Build dependency/topology/semantic connection analysis and intervention ranking. | [analyze_kb_graph.py](../../skills/discovery/kb-proof-connector/scripts/analyze_kb_graph.py), [generate_phyp.py](../../skills/discovery/kb-proof-connector/scripts/generate_phyp.py) |
| `kb-coherence-evaluator` | Build a typed coherence graph and score explanatory/coherence effects of hypotheses. | [evaluate_coherence.py](../../skills/discovery/kb-coherence-evaluator/scripts/evaluate_coherence.py) |
| `kb-entrypoint-finder` | Rank high-leverage conceptual starting points. | [recommend_entrypoints.py](../../skills/discovery/kb-entrypoint-finder/scripts/recommend_entrypoints.py) |
| `kb-entrypoint-pathfinder` | Turn entrypoints into explicit pathway agendas. | [synthesize_pathways.py](../../skills/discovery/kb-entrypoint-pathfinder/scripts/synthesize_pathways.py) |
| `kb-epistemic-hardness` | Explain why the target problem is hard and expose barrier structure. | [articulate_hardness.py](../../skills/discovery/kb-epistemic-hardness/scripts/articulate_hardness.py) |
| `kb-concept-bridge-planner` | Produce prioritized bridge programs between concepts/results. | [plan_bridges.py](../../skills/discovery/kb-concept-bridge-planner/scripts/plan_bridges.py) |
| `kb-gap-abstraction-conjecturer` | Diagnose concept gaps and conjecture the bridge-filling mathematical objects or abstractions that would make a route testable. | [conjecture_gap_abstractions.py](../../skills/discovery/kb-gap-abstraction-conjecturer/scripts/conjecture_gap_abstractions.py) |
| `kb-novel-proof-strategist` | Produce strategy portfolio and novelty-maximizing prompts. | [design_strategies.py](../../skills/discovery/kb-novel-proof-strategist/scripts/design_strategies.py) |
| `kb-proof-sketcher` | Turn top conjectures into structured proof sketches with obligations, lemmas, barrier checkpoints, and abort conditions. | [generate_proof_sketches.py](../../skills/discovery/kb-proof-sketcher/scripts/generate_proof_sketches.py) |
| `kb-expert-paper-generator` | Convert final artifacts into a bridge-first scientific paper draft that explains the main conceptual bridges, attached proof sketches, and supporting high-potential hypotheses for expert review with transparent score decomposition. | [generate_expert_paper.py](../../skills/reporting/kb-expert-paper-generator/scripts/generate_expert_paper.py) |
| `kb-hypothesis-evaluator` | Score each hypothesis and classify support/refutation state. | [evaluate_hypotheses.py](../../skills/evaluation/kb-hypothesis-evaluator/scripts/evaluate_hypotheses.py) |
| `kb-hypothesis-refutation-loop` | Iterate unresolved hypotheses with threshold/belief-revision logic. | [iterate_hypotheses.py](../../skills/evaluation/kb-hypothesis-refutation-loop/scripts/iterate_hypotheses.py) |
| `kb-revision-loop` | Generate concept/ontology/representation repairs when loops stall. | [revise_ontology.py](../../skills/evaluation/kb-revision-loop/scripts/revise_ontology.py) |
| `kb-orchestrator` | Deterministic stage routing, reporting, logging coverage, process graph, reasoning dynamics. | [run_orchestrator.py](../../skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py) plus orchestration utilities |
| `show-reasoning` | Live terminal dashboard for surfaced reasoning, PDL state, and material-inference operations. | [show_reasoning.py](../../skills/orchestration/show-reasoning/scripts/show_reasoning.py) |
| `kb-explain` | Prompt-only explanatory synthesis grounded in statement IDs. | [SKILL.md](../../skills/reasoning/kb-explain/SKILL.md) |
| `kb-deduce` | Prompt-only conservative consequence derivation. | [SKILL.md](../../skills/reasoning/kb-deduce/SKILL.md) |
| `kb-abduce` | Prompt-only missing-premise proposal and ranking. | [SKILL.md](../../skills/reasoning/kb-abduce/SKILL.md) |
| `kb-induce` | Prompt-only generalization of recurring bridge, strategy, lemma, or proof-sketch structures after other skills have isolated a theorem family. | [SKILL.md](../../skills/reasoning/kb-induce/SKILL.md) |
| `premise-completeness-prober` | Prompt-only audit of explicit versus hidden premises at one inference step. | [SKILL.md](../../skills/evaluation/premise-completeness-prober/SKILL.md) |
| `entailment-gap-auditor` | Prompt-only separation of true entailment from support-only evidence. | [SKILL.md](../../skills/evaluation/entailment-gap-auditor/SKILL.md) |
| `regime-shift-auditor` | Prompt-only audit of quantifier, model, and representation preservation. | [SKILL.md](../../skills/evaluation/regime-shift-auditor/SKILL.md) |
| `counterfactual-route-prober` | Prompt-only minimal-perturbation robustness check for routes and theorem moves. | [SKILL.md](../../skills/evaluation/counterfactual-route-prober/SKILL.md) |
| `counterexample-hunter` | Prompt-only local adversarial probe for barriers, nearby failures, and counterexamples. | [SKILL.md](../../skills/evaluation/counterexample-hunter/SKILL.md) |
| `bridge-object-equivalence-checker` | Prompt-only carrier equivalence audit for representation-shift-heavy routes. | [SKILL.md](../../skills/evaluation/bridge-object-equivalence-checker/SKILL.md) |
| `epistemic-status-ledger` | Prompt-only ledger that prevents live routes from being mistaken for proved claims. | [SKILL.md](../../skills/evaluation/epistemic-status-ledger/SKILL.md) |

## 3.1) Inference-Quality Probe Stack

The repository now treats spurious-inference control as a multi-probe problem rather than a single critic pass.

Recommended order:

1. `premise-completeness-prober`: are all premises actually present?
2. `entailment-gap-auditor`: do the cited premises entail the claim or only motivate it?
3. `regime-shift-auditor`: did the route smuggle a model, threshold, or quantifier shift?
4. `counterfactual-route-prober`: does the route survive minimal perturbations?
5. `counterexample-hunter`: is there a nearby failure witness or barrier analog already local?
6. `bridge-object-equivalence-checker`: are the carriers genuinely interchangeable?
7. `epistemic-status-ledger`: after all probes, what is still grounded versus conjectural?

## 4) Code Map by Layer

Shared utilities:

- [reasoning_log.py](../../skills/common/reasoning_log.py): paired internal-log and surfaced-reasoning persistence.
- [proof_discovery_language.py](../../skills/common/proof_discovery_language.py): shared proof-discovery-language schema, program serializers, and material-inference notation.
- [contracts.py](../../skills/common/contracts.py): schema validation across skill outputs.
- [hypothesis_eval.py](../../skills/common/hypothesis_eval.py): reusable hypothesis-scoring logic and helpers.

Graph and coherence layer:

- [analyze_kb_graph.py](../../skills/discovery/kb-proof-connector/scripts/analyze_kb_graph.py): statement graph + semantic connection candidates.
- [evaluate_coherence.py](../../skills/discovery/kb-coherence-evaluator/scripts/evaluate_coherence.py): typed coherence graph and local/global scoring.

Loop execution and control:

- [run_orchestrator.py](../../skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py): stage orchestration and artifact routing.
- [evaluate_hypotheses.py](../../skills/evaluation/kb-hypothesis-evaluator/scripts/evaluate_hypotheses.py): first-pass hypothesis triage.
- [iterate_hypotheses.py](../../skills/evaluation/kb-hypothesis-refutation-loop/scripts/iterate_hypotheses.py): iterative loop refinement.
- [revise_ontology.py](../../skills/evaluation/kb-revision-loop/scripts/revise_ontology.py): revision action generation.

Interpretability and observability:

- [generate_interpretation_reports.py](../../skills/orchestration/kb-orchestrator/scripts/generate_interpretation_reports.py): human-readable process/discovery reports.
- [generate_reasoning_log_index.py](../../skills/orchestration/kb-orchestrator/scripts/generate_reasoning_log_index.py): run-level log coverage index.
- [generate_process_graph.py](../../skills/orchestration/kb-orchestrator/scripts/generate_process_graph.py): typed process graph replay.
- [generate_reasoning_dynamics.py](../../skills/orchestration/kb-orchestrator/scripts/generate_reasoning_dynamics.py): graph/process/concept dynamics metrics and dashboard.
- [generate_discovery_graph_explorer.py](../../skills/orchestration/kb-orchestrator/scripts/generate_discovery_graph_explorer.py): stage-aware conceptual discovery graph explorer over statements, hypotheses, bridges, abstractions, and hardness signals.

## 5) Detailed Walkthrough: Coherence Evaluator

File: [evaluate_coherence.py](../../skills/discovery/kb-coherence-evaluator/scripts/evaluate_coherence.py)

High-level flow:

1. Parse KB statements from fenced YAML blocks.
2. Validate connector analysis + phyp contracts.
3. Build typed graph with node families:
   - statements
   - concepts (symbols/roles)
   - methods
   - barriers
   - hypotheses
4. Build edge families:
   - structural (`supports`, `generalizes`, `defines`, `uses`)
   - barrier constraints (`blocks`, `obstructs`)
   - connector-derived semantic edges (`explains`, `reframes`, `supports`)
   - hypothesis-induced edges from kind semantics
5. Compute coherence profile:
   - `consistency`: positive-vs-negative weight balance
   - `integration`: connectedness of positive subgraph
   - `explanatory_unification`: proportion of nodes receiving multiple positive supports
   - `tension`: conflict proportion
   - `global_coherence`: weighted aggregate
6. For each hypothesis:
   - estimate local explanatory power,
   - compare global coherence with/without that hypothesis edges,
   - produce `coherence_delta_global`.
7. Emit revision recommendations for coherence-negative/low-explanatory hypotheses.

Output semantics:

- `typed_coherence_graph`: graph object suitable for reasoning audits.
- `coherence_profile`: global quality signal.
- `hypothesis_coherence`: per-hypothesis local/global impact.
- `belief_revision_recommendations`: actionable pruning/reframing guidance.

## 6) Detailed Walkthrough: Connector

File: [analyze_kb_graph.py](../../skills/discovery/kb-proof-connector/scripts/analyze_kb_graph.py)

Connector scoring combines:

- lexical overlap,
- symbol-role alignment,
- method-tag overlap,
- theorem-family signature overlap,
- equivalence/reduction signal,
- definitional expansion signal,
- topological gain (cross-component merge potential),
- premise-target compatibility.

Outputs:

- top intervention points (information leverage),
- connection candidates (candidate bridge edges),
- concept graph (concept/method/barrier relational web),
- abductive loop seed plan.

## 7) Detailed Walkthrough: Hypothesis Evaluation

File: [hypothesis_eval.py](../../skills/common/hypothesis_eval.py) (reused by evaluation scripts)

Design:

- hypothesis-type-specific evaluators:
  - bridge-link
  - intervention-focus
  - conceptual kinds (`representation-shift`, `intermediate-invariant`, etc.)
- each evaluator computes:
  - base support score
  - base refute score
  - evidence adjustments
  - coherence adjustments
- final verdict policy:
  - `supported` / `refuted` when threshold + margin is met,
  - otherwise `inconclusive`,
  - optional provisional classification with forced resolution.

This module is the central place for calibrating triage behavior.

## 8) Detailed Walkthrough: Orchestrator

File: [run_orchestrator.py](../../skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py)

Responsibilities:

- parse intent,
- resolve artifact defaults from KB slug,
- execute stage scripts in deterministic order,
- propagate run IDs (`ABDUCER_RUN_ID`) to child processes,
- capture child `[LOG]` markers,
- record expected agents for coverage checks,
- generate log index and interpretation/visualization artifacts.

Intents include:

- stage-level: `cohere`, `connect`, `coherence-eval`, `entrypoints`, `hardness`, `bridge-plan`, `conjecture`, `strategies`, `proof-sketch`, `hypothesis-eval`, `hypothesis-loop`, `revision-loop`
- observability-level: `interpretation-reports`, `process-graph`, `reasoning-dynamics`, `conceptual-dynamics`
- composite: `abductive-loop`, `pipeline`

## 9) Observability and Discovery Interpretation

Artifacts for understanding reasoning behavior:

- process-level:
  - `reasoning-process-report.md`
  - `discovery-interpretation-report.md`
- graph-level:
  - `process-graph.json`
  - `process-graph-evolution.json`
  - `process-graph.html`
- dynamics-level:
  - `reasoning-dynamics.json`
  - `reasoning-dynamics.md`
- live terminal-level:
  - `show-reasoning` over `artifacts/reasoning-surfaces/*/*.json`
  - PDL-aware current-state rendering of the latest substantive surfaced moment
  - `reasoning-dynamics.html`
- conceptual-monitoring-level:
  - `conceptual-dynamics.json`
  - `conceptual-dynamics.md`
  - `conceptual-dynamics.html`
- logging-level:
  - `reasoning-log-index.json`
  - `reasoning-log-index.md`

## 10) Extension Guidance

Where to add new reasoning behavior:

- add new hypothesis kind: update [generate_phyp.py](../../skills/discovery/kb-proof-connector/scripts/generate_phyp.py), [hypothesis_eval.py](../../skills/common/hypothesis_eval.py), and [evaluate_coherence.py](../../skills/discovery/kb-coherence-evaluator/scripts/evaluate_coherence.py).
- add new global metric: update [generate_reasoning_dynamics.py](../../skills/orchestration/kb-orchestrator/scripts/generate_reasoning_dynamics.py) and report templates.
- add new stage to orchestration: extend [run_orchestrator.py](../../skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py), docs, and expected-agent mapping.

Safe extension checklist:

- keep output contracts stable or version them,
- emit reasoning logs with declared outputs,
- add/update tests in [`tests/`](../../tests),
- update [`cli-reference.md`](cli-reference.md), [`skills.md`](skills.md), and relevant runbook sections.
