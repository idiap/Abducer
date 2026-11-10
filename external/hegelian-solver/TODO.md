<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# TODO: Multi-Agent Skill Method for the Hegelian Solver

## Interpretation

The attached references point to a solver that turns conceptual development into a typed, checkable workflow:

```text
concept -> task/evidence -> failure or discovery signal -> candidate transformation -> obligations -> ranking -> concept graph edge -> explanation
```

The key implementation choice is to model development as a branching concept graph. Math nodes emphasize signatures, axioms, examples, invariants, proof obligations, embeddings, completions, quotients, abstractions, and universal properties. Physics nodes add regimes of validity, measurement maps, empirical residuals, limiting-case recovery, effective-theory status, and anti-ad-hoc checks. Language-model nodes add traces, tools, retrieval, deployment, safety, monitoring, governance, and regression obligations.

## Current Repository Setup

- [x] Copy source references into `refs/`.
- [x] Add `refs/source_index.md` with source interpretation and skill routing.
- [x] Create granular skill folders under `agents/`.
- [x] Seed each skill with a focused `SKILL.md` and UI metadata.

## Phase 1: Project Skeleton

- [x] Decide runtime package shape, for example `hegelian_solver/` with `schemas/`, `skills_runtime/`, `operators/`, `validators/`, `graph/`, `examples/`, and `cli/`.
- [x] Add a Python project file and dependency policy.
- [x] Add a test layout with unit tests, fixture tests, and end-to-end trace tests.
- [x] Define canonical artifact directories: `data/concepts/`, `data/traces/`, `data/graphs/`, `data/candidates/`, `data/certificates/`, and `data/run_ledgers/`.

## Phase 2: Schemas

- [x] Implement `ConceptNode` with signature, axioms/constraints, models, tasks, interface, preservation constraints, examples, invariants, equivalences, representation maps, history, allowed operators, status, assumptions, and unknowns.
- [x] Implement `PhysicalConcept` extension with state space, observables, dynamics, symmetries, parameters/units, measurement model, regime, evidence, anomalies, limiting cases, and maturity status.
- [x] Implement `LanguageModelConcept` extension with representation, architecture, data, objective, interaction, tools, evaluation, safety, governance, traces, and deployment context.
- [x] Implement `Task`, `Evidence`, `FailureCertificate`, `DiscoverySignal`, `TransformationCandidate`, `ValidationPacket`, `RankingDecision`, `ConceptGraphNode`, `ConceptGraphEdge`, and `SolverTrace`.
- [x] Export JSON Schema for every public artifact.
- [x] Add fixtures for `Naturals -> Integers`, `MetricSpace -> TopologicalSpace`, `NewtonianMechanics -> SpecialRelativity`, and `Assistant -> GroundedAssistant`.

## Phase 3: Skill Runtime

- [x] Define a common skill I/O contract so each agent skill can be called independently or by the orchestrator.
- [x] Implement a local orchestrator that executes the skill sequence from `hegelian-solver-orchestrator`.
- [x] Add validation that every stage receives the fields it requires and emits the expected artifact type.
- [x] Add a run ledger that stores intermediate packets and supports resuming a run.
- [x] Add deterministic IDs for concepts, failures, signals, candidates, validation packets, and graph edges.

## Phase 4: Domain Adapter

- [x] Implement domain detection for mathematical, physical, language-model, and generic concepts.
- [x] Attach domain-specific required fields and validation gates.
- [x] Ensure physics tasks require regimes/tolerances when predictions or measurements are involved.
- [x] Ensure language-model tasks separate model output, retrieved source, tool result, human preference, policy decision, and benchmark evidence.
- [x] Add tests showing the same raw phrase can route differently depending on context.

## Phase 5: Formalization and Evidence

- [x] Implement concept formalization from YAML/JSON input.
- [x] Add a prose-to-draft adapter that creates explicit `unknowns` rather than hallucinated fields.
- [x] Implement task and evidence curation from concept nodes and source fixtures.
- [x] Add stress-task generation for closure, solvability, completeness, invariance, rigidity, consistency, representability, transfer, compositionality, and residual-limit checks.
- [x] Add physics-specific limiting-case and measurement-interface tasks.
- [x] Add LM-specific provenance, tool-use, prompt-injection, safety, governance, and cost/latency tasks.

## Phase 6: Failure and Discovery

- [x] Implement failure classifiers for core mathematical labels.
- [x] Implement physics classifiers for empirical anomaly, overextension, noncovariance, scale mismatch, measurement gap, no limiting case, and representation dependence.
- [x] Implement LM classifiers for hallucination, no provenance, prompt injection, tool misuse, over-refusal, planning myopia, compute inefficiency, and governance gap.
- [x] Implement discovery signal detectors for shared interface, invariant pattern, proof compression, representation redundancy, equivalence pressure, universal pattern, functoriality, duality, parameter generalization, and anomaly clusters.
- [x] Add guardrails for latent ontology: constrained properties, multiple linked signals, testable consequences, and anti-overfit penalties.

## Phase 7: Transformation Library

- [x] Implement core candidate templates: `GroupCompletion`, `FieldOfFractions`, `Completion`, `AlgebraicAdjunction`, `Invariantize`, `Quotient`, `WeakenEquivalence`, `AbstractInterface`, `WeakenAxioms`, `TypeStratify`, `Categorify`, and `Functorialize`.
- [x] Implement physics templates: `RestrictRegime`, `InvariantizeKinematics`, `GeometrizeInteraction`, `FieldifyActionAtDistance`, `QuantizeObservableAlgebra`, `IntroduceLatentCarrier`, `GaugeQuotient`, `LocalizeSymmetry`, `CoarseGrain`, `Renormalize`, and `IntroduceOrderParameter`.
- [x] Implement LM templates: `InstructionTune`, `PreferenceOptimize`, `Retrieve`, `Verify`, `Toolify`, `Agentify`, `ReasonAtInference`, `Govern`, `SecureRAG`, `TaintTracking`, `CalibrateSafetyPolicy`, and `AddState`.
- [x] Ensure every candidate includes preservation map, resolution mechanism, changed structure, expected obligations, residual limits, assumptions, and rejected alternatives.

## Phase 8: Obligations and Validators

- [x] Implement obligation generation for preservation, resolution, non-collapse, conservativity, universality, transfer, adequacy, and residual-limit reporting.
- [x] Add pluggable backends for proof plans, SMT/model-finder checks, theorem prover hooks, unit tests, simulations, benchmark runs, and human review.
- [x] Implement physics validators for dimensional consistency, covariance, gauge independence, conservation, limiting-case recovery, residual reduction, uncertainty, measurement validity, and anti-overfit checks.
- [x] Implement LM validators for source support, citation accuracy, tool schema validity, observation use, side-effect safety, injection resistance, refusal calibration, latency/cost bounds, and governance documentation.
- [x] Treat `planned` and `unknown` as non-passing statuses.

## Phase 9: Ranking and Branching

- [x] Implement hard gates before scoring.
- [x] Implement transparent weighted scoring for generic/math, physics, and LM candidates.
- [x] Implement Pareto frontier handling so valid candidates can branch instead of forcing one winner.
- [x] Add candidate statuses: `accept`, `accept_as_branch`, `provisional`, `defer`, and `reject`.
- [x] Store rejected candidates with reasons and failed gates.

## Phase 10: Graph and Trace Store

- [x] Implement concept graph node and edge storage in JSON/YAML.
- [x] Support edge relations such as `embeds`, `abstracts`, `completes`, `quotients`, `limits_to`, `effective_of`, `coarse_grains_to`, `quantizes`, `gauge_quotients`, `toolifies`, `retrieves`, `agentifies`, and `governs`.
- [x] Persist complete solver traces for every run.
- [x] Include source refs, evidence refs, trigger IDs, operator IDs, validation packets, ranking decisions, and residual limits on every edge.
- [x] Add graph query helpers for predecessors, successors, open residual limits, rejected candidates, and active frontier nodes.

## Phase 11: Explanations

- [x] Implement dialectical explanation generation from graph edges and validation packets.
- [x] Distinguish verified `Aufhebung` from provisional candidate repair.
- [x] Include preservation, elevation/resolution, mediation, non-collapse, residual limits, and future graph seeds.
- [x] Add concise and detailed explanation modes.

## Phase 12: CLI and API

- [x] Add `hegelian-solver run <concept-file>` to execute a full orchestrated pass.
- [x] Add `hegelian-solver classify-failure`, `mine-discovery`, `propose`, `verify`, `rank`, and `explain` subcommands for granular agent use.
- [x] Add `hegelian-solver graph inspect` and `graph export`.
- [x] Add machine-readable output and human-readable summaries.

## Phase 13: Tests and Benchmarks

- [x] Unit-test every schema and validator.
- [x] Fixture-test the number-system chain: `Naturals -> Integers -> Rationals -> Reals -> Complex`.
- [x] Fixture-test abstraction discovery from group-like examples.
- [x] Fixture-test physics limiting-case recovery with symbolic examples.
- [x] Fixture-test an LM trace where hallucination/no-provenance maps to retrieval and verification candidates.
- [x] Regression-test that invalid candidates fail hard gates.
- [x] Validate all skill folders with the Codex skill validator.

## Phase 14: Documentation and Handoff

- [x] Replace the placeholder `README.md` with a project-specific overview.
- [x] Document artifact schemas and example runs.
- [x] Document how to add a new domain adapter, failure label, discovery signal, operator, validator, and ranking feature.
- [x] Add a minimal tutorial using the `Naturals -> Integers` example.
- [x] Add a roadmap for theorem-prover, SMT, CAS, simulation, and benchmark integrations.

## Phase 15: Spec Use-Case Instantiation and Epistemic Prompt Refinement

- [x] Instantiate 65 spec-derived use cases across mathematical concepts, physics examples, and language-model evolution traces.
- [x] Require every use case to carry formal analysis, material analysis, source refs, and an epistemic profile.
- [x] Extend concept schemas and reasoning logs so formal/material/epistemic fields remain machine-readable.
- [x] Add a use-case manifest loader, validator, and suite runner.
- [x] Add CLI commands for listing, validating, and running the use-case suite.
- [x] Add tests covering the manifest, suite runner, and CLI.
- [x] Refine every agent skill prompt with explicit epistemic discipline: evidence, assumptions, uncertainty, possible falsifiers, and residual limits.

## Phase 16: Retrospective Input and Web Expansion Skills

- [x] Reflect the solver input typology as a dedicated `hegelian-input-typology` skill.
- [x] Add `hegelian-retrospective-evolution-formalizer` for historical prose about concept evolution.
- [x] Add `hegelian-web-expansion-scout` to decide when search is required, recommended, unnecessary, or forbidden.
- [x] Integrate input typology, web expansion, and retrospective formalization into the orchestrator flow.
- [x] Document the new input modes and skills.

## Phase 17: Field Tension and Conceptual Crisis Formalization

- [x] Add `hegelian-field-tension-elicitor` to surface opposed commitments, stakes, and pressure points.
- [x] Add `hegelian-tension-evidence-cartographer` to map decisive claims, evidence states, counterevidence, and failed mediations.
- [x] Add `hegelian-conceptual-crisis-formalizer` to produce exact `tension_formalization_packet` artifacts.
- [x] Integrate field-tension requests into the input typology and orchestrator flow.
- [x] Add realistic, non-toy crisis formalization examples.
- [x] Add tests covering skill integration and example packet structure.

## Phase 18: Abductive Mechanism Reasoning From Conceptual Crisis

- [x] Add `hegelian-abductive-mechanism-hypothesizer` to infer possible mediating mechanisms from a formalized crisis.
- [x] Add `hegelian-mechanism-requirements-formalizer` to convert mechanism hypotheses into formal, material, interface, epistemic, safety, and regime requirements.
- [x] Add `hegelian-mechanism-counterfactual-critic` to probe mechanism requirements with removal, regime-shift, proxy-capture, authority-gap, incentive, and non-collapse tests.
- [x] Add `hegelian-mechanism-todo-elicitor` to turn unresolved mechanism requirements into ordered proof, evidence, design, implementation, validation, and decision TODOs.
- [x] Integrate mechanism abduction into the orchestrator after `tension_formalization_packet` and before successor-concept proposal.
- [x] Teach graph serialization to store mechanism hypotheses, requirements, critiques, and TODOs as provisional artifacts rather than accepted repair edges.
- [x] Add realistic mechanism examples for clinical AI, agentic AI governance, and low-carbon grid reliability.
- [x] Add tests covering mechanism skill integration and example packet structure.
- [x] Promote mechanism packets to first-class Pydantic schemas after the example shape stabilizes.
- [x] Add CLI commands for mechanism abduction, requirements formalization, counterfactual critique, and TODO extraction.
- [x] Render mechanism packets as a dedicated section in the HTML report.
- [x] Link mechanism TODOs to future `ValidationPacket` generation.

## Phase 19: Workflow Review and Representation Hardening

Findings from a full review of the deterministic pipeline (`domain.py`, `failures.py`,
`discovery.py`, `operators/library.py`, `validators/core.py`, `ranker.py`) now that 65
use cases exercise it across math/physics/LM domains.

- [x] Audit whether every reasoning stage is controllably invoked both end-to-end
      (`run_solver`) and standalone (CLI subcommands `classify-failure`, `mine-discovery`,
      `propose`, `verify`, `rank`, `explain`, `mechanism *`) — confirmed all are.
- [x] Identify that mechanism dossiers were a parallel, unconsumed track: attachable to the
      HTML report but never fed back into candidate generation or validation. Documented as
      a known gap (see "Integrate mechanism dossiers" below); not yet wired into `run_solver`.
- [x] Implement a bounded reflective refinement loop in `run_solver`: each iteration treats
      the best candidate's open, non-core obligations as new determinate negations of its
      own target concept and re-proposes against it, with stopping criteria `resolved`,
      `no_candidates`, `no_refinement_triggers`, `plateau` (score does not improve by more
      than `SCORE_IMPROVEMENT_EPS`), and a `max_iterations` safety net. Exposed via
      `SolverHooks` (`hegelian_solver/hooks.py`) and a new `reflective_refinement` reasoning
      step / HTML report panel. See `hegelian_solver/orchestrator.py` module docstring for
      the stopping-criteria rationale, validated against all 65 use cases (43 plateau, 22
      resolve in one pass, none currently exhaust `max_iterations` or hit
      `no_refinement_triggers` in practice — those paths are unit-tested directly).
- [ ] Unify the failure-label -> operator/repair-target mapping. `failures.REPAIR_TARGETS`
      and `operators.library.FAILURE_TO_OPERATORS` are two separately maintained copies of
      the same taxonomy and have already drifted (`NoLimitingCase` maps to the nonexistent
      operator name `"RejectCandidate"` in `failures.py` but to `"RestrictRegime"` in
      `operators/library.py`; `CaseExplosion` differs too). Move to one source of truth.
- [ ] Wire `DomainProfile.validation_gates` into `validators/core.py` dynamically. Today the
      hard-gate set is hardcoded per `kind` string in `_status_for`/`generate_validation_packet`
      and ignores the domain profile entirely, so declared gates like physics'
      `anti_overfit` or LM's `governance`/`efficiency` are descriptive only and never
      actually block a decision.
- [ ] Make `_ranking_features` (operators/library.py) sensitive to the concept's own
      evidence strength instead of fixed per-operator/per-domain constants. Right now two
      candidates with the same operator in the same domain always get identical ranking
      features regardless of how strong the underlying evidence is, so the ranker can't
      differentiate well-evidenced from thin candidates within an operator class.
- [ ] Replace first-match keyword substring classification (`failures._label_from_text`,
      `domain.detect_domain`) with a more robust deterministic signal (e.g. scored
      multi-marker matching) now that the corpus spans many phrasings; first-match keyword
      search risks systematically under-using most of the failure taxonomy and misrouting
      concepts whose free text happens to contain another domain's marker word.
- [ ] Integrate mechanism dossiers into the orchestrated flow itself (not just the report):
      allow `run_solver`/CLI to accept a mechanism dossier and fold its requirements/critique
      into validation or candidate generation for the concept the crisis was formalized from.
- [ ] Guard `rank_candidates` against silently dropping candidates that have no matching
      validation packet; log or surface this instead of silent omission.
- [ ] Deepen `target_concept` synthesis in `operators/library.py` so successor concepts
      carry real structural change derived from the trigger rather than a renamed copy of
      the source. This is acceptable for demonstrating the pipeline's shape but is the
      weakest link in the framework's claim to representational depth at 65-scenario scale.

## Phase 20: Area Conceptual Trace Building

- [x] Add `hegelian-area-concept-trace-builder` to research and write an informal,
      natural-language retrospective trace of an area's key concepts from a topic name
      (rather than already-supplied prose), with per-claim web-search triage instead of
      broad topic search.
- [x] Add the `area_trace_request` input kind to `hegelian-input-typology` and route it to
      the new skill before optional formal staging by `hegelian-retrospective-evolution-formalizer`.
- [x] Integrate the new skill into the orchestrator pipeline and output contract.
- [x] Add a test asserting the new skill's integration into typology/orchestrator.
- [x] Use the skill to build a real conceptual trace of cancer-mechanism understanding and
      emerging therapeutic interventions, and store it as a worked example
      (`hegelian_solver/examples/area_traces/cancer_mechanisms_and_therapeutics.yaml`, 11
      key concepts from 19th-century tissue-level disease models through CAR-T cell
      therapy, with targeted web search used for precise dates/names and explicitly marked
      lower-confidence entries left unsearched per the skill's triage discipline).

## Phase 21: Systematic Conceptual Creativity Reasoning

- [x] Define a typed `conceptual_creativity` artifact (`ConceptualCreativityAnalysis` in
      `hegelian_solver/schemas/creativity.py`) with fields for latent tension, creative
      reframing, new constructive resource, preservation under transformation, generative
      payoff, creative risks, and why the move is creative rather than merely corrective.
- [x] Add a `hegelian-conceptual-creativity-reasoner` skill (and a deterministic
      `hegelian_solver/creativity.py` builder implementing the same discipline) that grounds
      every creativity claim in trace artifacts, separates repair from affordance creation,
      and names the preserved invariant plus the residual risk.
- [x] Introduce a conceptual-operation taxonomy so creativity can be compared across cases:
      closure completion, abstraction/interface discovery, invariance/reparameterization,
      quotienting/redundancy removal, localization/regime restriction, externalization or
      tooling, bridge mediation, latent carrier introduction, and governance/safety scaffold.
      Every name in `operators.library.ALL_OPERATOR_NAMES` is classified (enforced by a
      coverage test); validated against all 65 use cases (181 analyses, all 9 operations
      exercised: 107 abstraction/interface discovery down to 1 closure completion).
- [x] Render a `Conceptual Creativity Analysis` section before concrete concept evolution
      and formal notation, with readable prose first and the full structured payload in
      collapsible details. Replaces the earlier `Conceptual Creativity TODOs` placeholder
      that scaffolded this phase.
- [x] Add validation criteria for creativity explanations: source pressure, operation,
      new affordance, preserved invariant, risk/tradeoff, and downstream concept seeds must
      be explicit; unsupported claims become residual TODOs (`validate_creativity_analysis`,
      also exposed via `hegelian-solver creativity <trace> --validate`). Confirmed zero
      missing-required-field instances across all 65 use cases.
