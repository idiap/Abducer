<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reference Source Index

This directory preserves the source specs and examples used to design the Hegelian solver skill method.

## Files

- `hegelian_concept_solver_spec.md`: Core solver formalization. Defines concept tuples, tasks, failure certificates as determinate negations, transformation operators, proof obligations, solver loop, ranking, minimal DSL, architecture, number-system example, JSON trace shape, and Lean-oriented sketch.
- `hegelian_logic_mathematical_concepts.tex`: Mathematical/philosophical bridge. Explains determinate negation, mathematical Aufhebung, number systems, geometry, functions, equality, infinity, mathematical negation types, and preservation-through-transformation.
- `dialectical_concept_solver_refined_with_discovery.md`: Refined solver model. Adds examples, invariants, concept history, discovery signals, branching concept graph, richer proof obligations, data schemas, operator specifications, discovery mechanisms, and candidate scoring.
- `dialectical_concept_solver_physics_examples.md`: Physics extension. Adds physical concept schemas, empirical residuals, regimes of validity, measurement maps, limiting-case recovery, mixed formal/empirical obligations, physics operators, anti-ad-hoc checks, and benchmark traces.
- `dialectical_concept_solver_physics_examples (1).md`: Duplicate copy of `dialectical_concept_solver_physics_examples.md` retained because it was attached separately.
- `dialectical_concept_solver_language_model_evolution.md`: Language-model/system extension. Adds model-system concept schemas, LM-specific failures, transformation templates such as retrieval/tool use/agentification/governance, trace evidence, risk obligations, architecture, and minimal implementation phases.

## Interpretation

The combined references define the solver as a graph-building engine rather than a single chain generator. A concept develops when a typed failure or discovery signal creates pressure for a constructive successor. A successor is accepted only when it preserves protected predecessor structure, resolves or relocates the trigger, avoids collapse, declares residual limits, and satisfies domain-specific validation gates.

The implementation should therefore treat Hegelian terminology as operational metadata:

- `Concept`: structured theory, physical model, language-model system, or generic interface with tasks and protected meanings.
- `Determinate negation`: typed failure certificate with witness, failed obligation, dependency trace, repair target, and severity.
- `Discovery`: signal from shared interfaces, invariants, proof compression, universality, anomaly clusters, latent ontology, or system traces.
- `Aufhebung`: verified transformation, not a loose synonym for improvement.
- `Mediation`: explicit map or edge connecting stages: embedding, quotient, completion, limiting map, measurement map, retrieval/tool/governance layer, or concept-graph edge.

## Skill Routing

The skills under `../agents/` are intentionally granular:

- `hegelian-solver-orchestrator` coordinates the full run.
- `hegelian-domain-adapter` selects math, physics, language-model, or generic validation profiles.
- `hegelian-concept-formalizer` builds concept nodes.
- `hegelian-task-evidence-curator` builds task and evidence packets.
- `hegelian-failure-classifier` emits determinate negation certificates.
- `hegelian-discovery-signal-miner` emits discovery signals.
- `hegelian-transformation-proposer` emits candidate successors.
- `hegelian-obligation-verifier` emits validation packets.
- `hegelian-candidate-ranker` ranks, gates, and branches candidates.
- `hegelian-graph-trace-serializer` emits concept graph and trace artifacts.
- `hegelian-dialectic-explainer` produces human-facing explanations grounded in certificates.
