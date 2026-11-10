---
name: hegelian-solver-orchestrator
description: Coordinate a multi-agent Hegelian concept solver run across input typology, optional web expansion, area conceptual trace building, field tension elicitation, conceptual crisis formalization, abductive mechanism reasoning, retrospective evolution formalization, domain selection, concept formalization, task and evidence curation, failure classification, discovery mining, transformation proposal, obligation verification, candidate ranking, conceptual creativity reasoning, graph serialization, and dialectical explanation. Use when Codex needs to plan or execute the full dialectical solver workflow rather than one isolated stage.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Solver Orchestrator

## Overview

Coordinate the granular Hegelian solver skills as a typed pipeline from heterogeneous input to certified concept-graph updates. Keep input classification, tension elicitation, crisis formalization, abductive mechanism reasoning, retrospective reconstruction, source expansion, repair-driven development, and discovery-driven development explicit until candidates are ranked.

## Reference Routing

Use root references only as needed:

- `../../refs/source_index.md` for the source map and interpretation.
- `../../refs/hegelian_concept_solver_spec.md` for the minimal solver loop.
- `../../refs/dialectical_concept_solver_refined_with_discovery.md` for graph, discovery, operators, schemas, and ranking.
- Domain-specific refs when the task is clearly mathematical, physical, or language-model oriented.

## Pipeline

1. Invoke `hegelian-input-typology` to classify the incoming material, temporal scope, evidence state, web-search need, and downstream route.
2. If the intake packet marks web expansion as `required` or `recommended`, invoke `hegelian-web-expansion-scout` to plan source expansion and convert findings into bounded evidence.
3. If the primary input kind is `area_trace_request`, invoke `hegelian-area-concept-trace-builder` first to research and write an informal `area_conceptual_trace`, then continue per its `recommended_next_step` (typically `hegelian-retrospective-evolution-formalizer` on that trace).
4. If the primary input kind is `retrospective_evolution_text`, invoke `hegelian-retrospective-evolution-formalizer` to produce stages, transitions, evidence refs, and graph seeds before normal concept formalization.
5. If the primary input kind is `field_tension_request`, invoke `hegelian-field-tension-elicitor`, then `hegelian-tension-evidence-cartographer`, then `hegelian-conceptual-crisis-formalizer` to produce the exact tension formalization before normal failure and discovery work.
6. If a `tension_formalization_packet` exists and the user asks how the crisis might be addressed, invoke `hegelian-abductive-mechanism-hypothesizer`, `hegelian-mechanism-requirements-formalizer`, `hegelian-mechanism-counterfactual-critic`, and `hegelian-mechanism-todo-elicitor` before proposing successor concepts.
7. Invoke `hegelian-domain-adapter` to decide the active schema family and domain-specific validation gates for each seed concept, retrospective stage, formalized tension, or mechanism requirement packet.
8. Invoke `hegelian-concept-formalizer` to normalize seed concepts, retrospective stages, crisis packets, mechanism requirement packets, or successor concepts into concept nodes.
9. Invoke `hegelian-task-evidence-curator` to create tasks, examples, counterexamples, traces, web evidence, mechanism TODO evidence, and evidence packets.
10. Run both trigger paths:
    - `hegelian-failure-classifier` for determinate negations from failed tasks.
    - `hegelian-discovery-signal-miner` for discovery pressure from patterns, compression, anomalies, or repeated structures.
11. Invoke `hegelian-transformation-proposer` for each prioritized failure or discovery signal.
12. Invoke `hegelian-obligation-verifier` to generate and check candidate obligations.
13. Invoke `hegelian-candidate-ranker` to score, gate, and maintain a Pareto frontier when candidates optimize different goals.
14. Invoke `hegelian-use-case-motivation-writer`, `hegelian-conceptual-creativity-reasoner`, and `hegelian-full-explanation-builder` to produce the report's narrative layers: why the case matters, whether each candidate is a creative move or a repair, and the full reader-facing explanation of what happened.
15. Invoke `hegelian-graph-trace-serializer` to emit accepted, provisional, retrospective, crisis, mechanism, and rejected edges with certificates.
16. Invoke `hegelian-dialectic-explainer` for the human-facing explanation and residual-limit report.

## Control Rules

- Treat `Unknown` as a separate result, not as a failure.
- Do not skip input typology for prose, historical, mixed, or source-sensitive material.
- Do not treat a field controversy as a crisis until the minimal incompatible commitments and material conditions have been named.
- Do not browse when the user forbids search; mark the boundary in the web expansion plan.
- Do not call a successor an `Aufhebung` until preservation, resolution, and non-collapse checks are at least explicitly planned and no hard gate has failed.
- Preserve predecessor successes as protected constraints, including limiting-case recovery for physics and regression behavior for language-model systems.
- Keep source evidence distinct from model claims, hypotheses, measurements, formal proofs, benchmark scores, and human preferences.
- Keep retrospective chronology, causal explanation, and formal reconstruction separate.
- Keep field tension, exact crisis, evidence map, and candidate repair as distinct artifacts.
- Keep abductive mechanism hypotheses distinct from validated mechanisms; requirements are not proof of feasibility.
- Do not call a candidate creative unless it claims a new affordance beyond the four core obligations (preservation, resolution, non-collapse, residual-limit reporting); a move that only restores those is a repair, not a creative act.
- Record residual limits for every accepted successor so the concept graph remains open-ended.
- Prefer graph growth over a single linear chain when multiple valid transformations or abstractions exist.

## Epistemic Discipline

- Separate formal validity from material adequacy.
- Name evidence, assumptions, uncertainty, residual limits, and possible falsifiers.
- Distinguish verified, provisional, and speculative claims.

## Output Contract

Return a run packet with:

- `domain_profile`
- `input_intake_packet`
- `web_expansion_plan` when applicable
- `area_conceptual_trace` when applicable
- `retrospective_evolution_packet` when applicable
- `field_tension_elicitation_packet` when applicable
- `tension_evidence_map` when applicable
- `tension_formalization_packet` when applicable
- `mechanism_abduction_packet` when applicable
- `mechanism_requirements_packet` when applicable
- `mechanism_counterfactual_critique` when applicable
- `mechanism_todo_packet` when applicable
- `seed_concept_node`
- `task_and_evidence_packet`
- `failures`
- `discovery_signals`
- `transformation_candidates`
- `validation_packets`
- `ranking_decision`
- `conceptual_creativity_analysis` per candidate
- `graph_updates`
- `dialectical_explanation`
- `open_questions`
