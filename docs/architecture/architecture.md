<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# System Architecture

## Core Idea

This system is not best described as KB-first anymore.

It is better described as a problem-centered, stateful discovery-and-proof architecture.
The KB is one important grounding layer, but the active research state is distributed across several persistent objects:

- the problem KB in [`KB/*.kb.md`](../../KB),
- prior and newly learned mathematical memory in [`InformalMathLib/`](../../InformalMathLib),
- queued theorem targets in [`artifacts/<kb-ref>/proof-queue.*`](../../artifacts),
- discovery branches and routed search layers in [`artifacts/<kb-ref>/discovery-branch-queue.*`](../../artifacts),
- proof attempts in [`artifacts/<kb-ref>/proof-attempts/`](../../artifacts),
- work/meta governance state in [`artifacts/<kb-ref>/work-state.*`](../../artifacts),
- internal and surfaced reasoning traces in [`artifacts/reasoning-logs/`](../../artifacts/reasoning-logs) and [`artifacts/reasoning-surfaces/`](../../artifacts/reasoning-surfaces).

The core unit is therefore not just a statement store.
It is a governed discovery program that moves between:

1. grounded mathematical anchors,
2. conceptual tensions,
3. bridge objects and abstractions,
4. proof and disproof attempts,
5. persistent learned results,
6. reflective control over what to try next.

That logic is made explicit in the proof-discovery language implementation at [`skills/common/proof_discovery_language.py`](../../skills/common/proof_discovery_language.py).

## Architectural Thesis

The architecture exists to coordinate several kinds of epistemic work at once:

- theorem grounding,
- relational discovery,
- conjecture formation,
- proof/disproof work,
- barrier localization,
- memory consolidation,
- governance of loops and stopping,
- meta-level interpretation of what changed.

So the system should be read as a research operating system, not as a single theorem prover.

## High-Level Process

```text
Sources / prior art / local artifacts
  -> grounding and normalization
  -> relational discovery and tension mapping
  -> bridge / abstraction / route generation
  -> theorem-shaped queue formation
  -> prove / disprove attempts
  -> InformalMathLib persistence and blocked-result memory
  -> governance, plausibility, and continuation control
  -> meta reflection and live surfaced reasoning
```

## Core State Objects

### Problem KB

The KB is the canonical source of local theorem bodies, definitions, symbols, and gaps.
It is where source-side mathematical content becomes stable enough for later discovery and proof stages.

Primary files:

- [`KB/problem-template.kb.md`](../../KB/problem-template.kb.md)
- [`KB/p-vs-np.kb.md`](../../KB/p-vs-np.kb.md)

### InformalMathLib

InformalMathLib is not just imported prior art.
It is the persistent memory of the local research process: positive results, blocked local theorems, external references, and produced papers.

Primary implementation:

- [`skills/common/problem_mathlib.py`](../../skills/common/problem_mathlib.py)

### Proof Queue

The proof queue is the theorem-shaped frontier between discovery and prove.
It is where discovery outputs become concrete claims that can be consumed by the prove cycle.

Primary implementation:

- [`skills/common/proof_queue.py`](../../skills/common/proof_queue.py)
- [`skills/discovery/kb-discovery-cycle/scripts/enqueue_proof_candidates.py`](../../skills/discovery/kb-discovery-cycle/scripts/enqueue_proof_candidates.py)
- [`skills/discovery/kb-discovery-cycle/scripts/enqueue_discovery_programmes.py`](../../skills/discovery/kb-discovery-cycle/scripts/enqueue_discovery_programmes.py)

### Discovery Branch Queue

The discovery branch queue stores routed conceptual search branches when the frontier is not yet theorem-ready.
This is how the system avoids collapsing all search into a single depth-first route.

Primary implementation:

- [`skills/common/discovery_branch_queue.py`](../../skills/common/discovery_branch_queue.py)
- [`skills/discovery/kb-discovery-cycle/scripts/execute_discovery_branches.py`](../../skills/discovery/kb-discovery-cycle/scripts/execute_discovery_branches.py)

### Work / Meta State

The outer loop keeps persistent control over alternating discovery and prove, stop conditions, meta checkpoints, and high-reward continuation.

Primary implementation:

- [`skills/orchestration/work/scripts/run_work_cycle.py`](../../skills/orchestration/work/scripts/run_work_cycle.py)
- [`skills/control-plane/meta/scripts/generate_meta_reflection_report.py`](../../skills/control-plane/meta/scripts/generate_meta_reflection_report.py)

## Layered Architecture

## 1) Grounding Layer

### Conceptual Role

This layer turns raw mathematical material into inspectable local anchors.
Its job is not yet discovery.
Its job is to create stable theorem bodies, definitions, and source references that later stages can actually reason over.

### Main components

- [`skills/ingest/latex-kb-ingest/scripts/chunk_sources.py`](../../skills/ingest/latex-kb-ingest/scripts/chunk_sources.py)
- [`skills/ingest/latex-kb-ingest/scripts/kb_writeback.py`](../../skills/ingest/latex-kb-ingest/scripts/kb_writeback.py)
- [`skills/ingest/pvsnp-kb-parser/scripts/parse_report.py`](../../skills/ingest/pvsnp-kb-parser/scripts/parse_report.py)
- [`skills/ingest/theorem-body-normalizer/SKILL.md`](../../skills/ingest/theorem-body-normalizer/SKILL.md)
- [`skills/common/statement_text.py`](../../skills/common/statement_text.py)

### Why it matters

Without this layer, later stages operate on topic resemblance or free-form prose.
With it, later stages can refer to theorem bodies, regimes, targets, and excerpts in a reusable way.

## 2) Relational Discovery Layer

### Conceptual Role

This layer maps the local mathematical terrain.
It asks:

- what depends on what,
- where bridge pressure is highest,
- which components are disconnected,
- where a statement is structurally central versus mathematically leverageful.

### Main components

- [`skills/discovery/kb-proof-connector/scripts/analyze_kb_graph.py`](../../skills/discovery/kb-proof-connector/scripts/analyze_kb_graph.py)
- [`skills/discovery/kb-proof-connector/scripts/generate_phyp.py`](../../skills/discovery/kb-proof-connector/scripts/generate_phyp.py)
- [`skills/discovery/kb-coherence-evaluator/scripts/evaluate_coherence.py`](../../skills/discovery/kb-coherence-evaluator/scripts/evaluate_coherence.py)
- [`skills/evaluation/hub-bias-auditor/SKILL.md`](../../skills/evaluation/hub-bias-auditor/SKILL.md)

### Why it matters

This is the first place where discovery pressure becomes explicit.
It does not yet prove anything.
It turns raw grounded material into a structured landscape of tensions, links, and candidate interventions.

## Hypothesis Exploration And Conceptual Creativity Layer

Abducer now has a Looper-visible hypothesis exploration layer for moments when
the frontier contains conceptual pressure rather than a theorem-ready next step.
The layer is implemented as native Abducer artifacts, not as a separate Hegelian
runtime:

- [`artifacts/hegelian/hypothesis_exploration_map.json`](../../artifacts/hegelian/hypothesis_exploration_map.json)
- [`artifacts/hegelian/failure_signal_cartography.json`](../../artifacts/hegelian/failure_signal_cartography.json)
- [`artifacts/hegelian/mediation_candidates.json`](../../artifacts/hegelian/mediation_candidates.json)
- [`artifacts/hegelian/validation_packets.json`](../../artifacts/hegelian/validation_packets.json)
- [`artifacts/hegelian/candidate_rankings.json`](../../artifacts/hegelian/candidate_rankings.json)
- [`artifacts/hegelian/conceptual_refinement_trace.json`](../../artifacts/hegelian/conceptual_refinement_trace.json)

The layer turns blocked routes, bridge pressure, and positive discovery signals
into creative operations such as bridge invention, abstraction formation, theorem
weakening, carrier introduction, analogy transport, proof-obligation
factorization, and representation shift. Each operation must create validation
obligations before it can alter the work loop.

Primary implementation:

- [`agentic/scripts/build_hypothesis_exploration_map.py`](../../agentic/scripts/build_hypothesis_exploration_map.py)
- [`agentic/scripts/validate_hypothesis_exploration.py`](../../agentic/scripts/validate_hypothesis_exploration.py)
- [`skills/discovery/abducer-mediation-candidate-generator/SKILL.md`](../../skills/discovery/abducer-mediation-candidate-generator/SKILL.md)
- [`skills/evaluation/abducer-obligation-gatekeeper/SKILL.md`](../../skills/evaluation/abducer-obligation-gatekeeper/SKILL.md)
- [`skills/orchestration/abducer-refinement-route-ranker/SKILL.md`](../../skills/orchestration/abducer-refinement-route-ranker/SKILL.md)

Validation is deliberately layered: deterministic schema and replay checks,
generative quality probes, metamorphic evidence-removal checks, ablation checks,
and proof-queue safety tests. This keeps conceptual creativity productive without
letting it bypass source grounding, non-collapse, barrier compatibility, or
proof-readiness gates.

## 3) Conceptual Planning Layer

### Conceptual Role

This layer turns relational pressure into candidate research programs.
It asks:

- where should one enter the problem,
- what bridge object or abstraction would change the state,
- what kind of proof route is even worth articulating,
- which barriers or anti-barriers define the live frontier.

### Main components

- [`skills/discovery/kb-entrypoint-finder/scripts/recommend_entrypoints.py`](../../skills/discovery/kb-entrypoint-finder/scripts/recommend_entrypoints.py)
- [`skills/discovery/kb-entrypoint-pathfinder/scripts/synthesize_pathways.py`](../../skills/discovery/kb-entrypoint-pathfinder/scripts/synthesize_pathways.py)
- [`skills/discovery/kb-epistemic-hardness/scripts/articulate_hardness.py`](../../skills/discovery/kb-epistemic-hardness/scripts/articulate_hardness.py)
- [`skills/discovery/kb-concept-bridge-planner/scripts/plan_bridges.py`](../../skills/discovery/kb-concept-bridge-planner/scripts/plan_bridges.py)
- [`skills/discovery/kb-gap-abstraction-conjecturer/scripts/conjecture_gap_abstractions.py`](../../skills/discovery/kb-gap-abstraction-conjecturer/scripts/conjecture_gap_abstractions.py)
- [`skills/discovery/kb-novel-proof-strategist/scripts/design_strategies.py`](../../skills/discovery/kb-novel-proof-strategist/scripts/design_strategies.py)
- [`skills/discovery/kb-proof-sketcher/scripts/generate_proof_sketches.py`](../../skills/discovery/kb-proof-sketcher/scripts/generate_proof_sketches.py)

### Why it matters

This is where the system stops being a graph analyzer and starts becoming a discovery engine.
The outputs are still often conceptual or theorem-programmatic rather than prove-ready, but they are closer to actual mathematical action.

## 4) Discovery Compilation Layer

### Conceptual Role

This layer compiles broad discovery material into theorem-shaped units.
Its central question is:

What exactly should now enter prove, and what should remain in discovery?

### Main components

- [`skills/discovery/kb-discovery-cycle/scripts/enqueue_proof_candidates.py`](../../skills/discovery/kb-discovery-cycle/scripts/enqueue_proof_candidates.py)
- [`skills/discovery/kb-discovery-cycle/scripts/execute_discovery_branches.py`](../../skills/discovery/kb-discovery-cycle/scripts/execute_discovery_branches.py)
- [`skills/discovery/kb-discovery-cycle/scripts/generate_discovery_branch_synthesis.py`](../../skills/discovery/kb-discovery-cycle/scripts/generate_discovery_branch_synthesis.py)
- [`skills/discovery/kb-discovery-cycle/scripts/generate_expert_conjectures.py`](../../skills/discovery/kb-discovery-cycle/scripts/generate_expert_conjectures.py)
- [`skills/evaluation/kb-discovery-breakthrough-profiler/scripts/generate_discovery_breakthrough_profile.py`](../../skills/evaluation/kb-discovery-breakthrough-profiler/scripts/generate_discovery_breakthrough_profile.py)
- [`skills/common/discovery_lens_heuristic.py`](../../skills/common/discovery_lens_heuristic.py)

### Why it matters

This layer is the compiler from conceptual search into prove-ready conjecture packages.
It is also where category-theoretic and HoTT-inspired reframing lenses now enter as complementary discovery pathways rather than foundation replacements.

## 5) Prove / Disprove Layer

### Conceptual Role

This layer consumes theorem-shaped queue items and turns them into local proof or disproof dossiers.
Its purpose is not only to prove.
It also localizes obstructions, produces blocked local theorems, and identifies when a route should be reformulated rather than pursued further.

### Main components

- [`skills/discovery/kb-prove-cycle/scripts/start_proof_cycle.py`](../../skills/discovery/kb-prove-cycle/scripts/start_proof_cycle.py)
- [`skills/discovery/kb-prove-cycle/scripts/finalize_proof_cycle.py`](../../skills/discovery/kb-prove-cycle/scripts/finalize_proof_cycle.py)
- [`skills/discovery/kb-prove-cycle/scripts/generate_proof_cycle_summary.py`](../../skills/discovery/kb-prove-cycle/scripts/generate_proof_cycle_summary.py)
- [`skills/discovery/kb-prove-cycle/scripts/generate_proof_queue_report.py`](../../skills/discovery/kb-prove-cycle/scripts/generate_proof_queue_report.py)
- [`skills/common/negative_route_heuristic.py`](../../skills/common/negative_route_heuristic.py)
- [`skills/common/knowledge_source_policy.py`](../../skills/common/knowledge_source_policy.py)

### Why it matters

This is where mathematical commitment becomes explicit.
The layer forces theorem statement, route lemma, tactic structure, critique, terminal verdict, and memory persistence into one local object.

## 6) Memory and Persistence Layer

### Conceptual Role

This layer prevents rediscovery and preserves the epistemic cost of failed routes.
It is what makes the system cumulative rather than session-local.

### Main components

- [`skills/common/problem_mathlib.py`](../../skills/common/problem_mathlib.py)
- [`skills/common/high_reward_watch.py`](../../skills/common/high_reward_watch.py)
- [`skills/discovery/kb-prior-art-pass/scripts/generate_prior_art_pass_report.py`](../../skills/discovery/kb-prior-art-pass/scripts/generate_prior_art_pass_report.py)

### Why it matters

A discovery system without durable memory repeatedly rediscovers the same local failures.
This layer keeps positive, negative, imported, and high-value intermediate results available to later cycles.

## 7) Governance and Critique Layer

### Conceptual Role

This layer decides whether the current programme is worth continuing, revising, or stopping.
It is where epistemic discipline enters:

- plausibility scoring,
- drift control,
- major-subresult recognition,
- continuation or stop conditions,
- contradiction/impossibility routing,
- high-reward continuation.

### Main components

- [`skills/evaluation/kb-discovery-governor/SKILL.md`](../../skills/evaluation/kb-discovery-governor/SKILL.md)
- [`skills/evaluation/kb-end-to-end-proof-critic/scripts/generate_end_to_end_plausibility_report.py`](../../skills/evaluation/kb-end-to-end-proof-critic/scripts/generate_end_to_end_plausibility_report.py)
- [`skills/common/end_to_end_plausibility.py`](../../skills/common/end_to_end_plausibility.py)
- [`skills/orchestration/work/scripts/run_work_cycle.py`](../../skills/orchestration/work/scripts/run_work_cycle.py)

### Why it matters

Without governance, discovery becomes uncontrolled search and prove becomes infinite scaffolding.
This layer is what turns many skills into one research loop.

## 8) Reflection and Interpretation Layer

### Conceptual Role

This layer interprets what the process has actually learned.
It distinguishes:

- improved organization,
- sharpened bottlenecks,
- true mathematical progress,
- persistent hardness,
- misleading internal coherence.

### Main components

- [`skills/control-plane/meta/scripts/generate_meta_reflection_report.py`](../../skills/control-plane/meta/scripts/generate_meta_reflection_report.py)
- [`skills/control-plane/meta/scripts/generate_discovery_process_slides.py`](../../skills/control-plane/meta/scripts/generate_discovery_process_slides.py)
- [`skills/review/review-reasoner/SKILL.md`](../../skills/review/review-reasoner/SKILL.md)

### Why it matters

The system produces many artifacts.
This layer asks what they mean, not just whether they exist.

## 9) Observability Layer

### Conceptual Role

This layer makes the reasoning process inspectable while it is happening and after the fact.
It is not only debugging infrastructure.
It is part of the epistemic design because the system needs to expose its own reasoning moves, state transitions, and material inferences.

### Main components

- [`skills/common/reasoning_log.py`](../../skills/common/reasoning_log.py)
- [`skills/orchestration/show-reasoning/scripts/show_reasoning.py`](../../skills/orchestration/show-reasoning/scripts/show_reasoning.py)
- [`skills/orchestration/kb-orchestrator/scripts/generate_reasoning_log_index.py`](../../skills/orchestration/kb-orchestrator/scripts/generate_reasoning_log_index.py)
- [`skills/orchestration/kb-orchestrator/scripts/generate_reasoning_surface_index.py`](../../skills/orchestration/kb-orchestrator/scripts/generate_reasoning_surface_index.py)
- [`skills/orchestration/kb-orchestrator/scripts/generate_reasoning_dynamics.py`](../../skills/orchestration/kb-orchestrator/scripts/generate_reasoning_dynamics.py)
- [`skills/control-plane/meta/scripts/generate_epistemic_process_map.py`](../../skills/control-plane/meta/scripts/generate_epistemic_process_map.py)

### Why it matters

This is where the system becomes legible as a process.
The surfaced reasoning channel now carries proof-discovery-language state and material-inference operations, and the live viewer exposes that state directly.

## 10) Orchestration Layer

### Conceptual Role

This layer composes the whole system into deterministic execution paths.
It is the bridge between individual skills and a coherent run.

### Main components

- [`skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py`](../../skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py)
- [`skills/orchestration/kb-orchestrator/scripts/generate_interpretation_reports.py`](../../skills/orchestration/kb-orchestrator/scripts/generate_interpretation_reports.py)
- [`skills/orchestration/kb-orchestrator/scripts/export_phyp_docs.py`](../../skills/orchestration/kb-orchestrator/scripts/export_phyp_docs.py)

### Why it matters

This layer ensures artifact flow, run IDs, coverage tracking, and deterministic stage composition.
It is operational glue, but it is also epistemic glue because it defines which stages are allowed to interact and in what order.

## Prompt and Logic Layer

The architecture is not only scripts.
It also depends on shared reasoning contracts.

Primary documents:

- [`docs/research-methods/epistemic-prompt-framework.md`](../research-methods/epistemic-prompt-framework.md)
- [`skills/common/proof_discovery_language.py`](../../skills/common/proof_discovery_language.py)

Conceptually:

- the epistemic prompt framework defines what kinds of claims are licensed and how discovery should be governed;
- the proof-discovery language defines the runtime logic for anchors, tensions, bridge objects, material inferences, proof debt, and control objects.

## Revised Summary

The most accurate short description of the system is:

> A multi-layer research architecture for informal mathematical discovery and proof work, organized around persistent state objects, governed discovery/prove loops, explicit memory, and surfaced epistemic reasoning.

The KB remains foundational, but it is no longer the whole picture.
The real architecture is the interaction among grounding, discovery compilation, prove/disprove, memory, governance, reflection, and observability.
