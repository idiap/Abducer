<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
-->

# Abducer Skill Catalog

This catalog describes the repository-local Abducer skill tree. It was updated with the proof-depth control stack, conceptual-abstraction revision layer, Yang-Mills physical-relevance impact gate, literature-gap preinvestment gate, failure-archaeology premortem layer, and visual conceptualization reflection layer on 2026-07-21.

The catalog treats each skill as an operational capability: what it is for, how it contributes to the discovery workflow, whether it is prompt-only or backed by scripts/agents, and which artifacts or validation handoffs it expects.

## Reasoning Capability Access

The control plane exposes reasoning capabilities through two deliberately
different entry points:

- [`route`](../../skills/orchestration/route/SKILL.md) rigidly compiles a fixed
  `.prism` reasoning program into registered skill bindings. It fails closed on
  gaps or mismatches and never replans.
- [`orch`](../../skills/orchestration/orch/SKILL.md) dynamically diagnoses the
  current epistemic need, selects a reasoning type, filters its compatible
  materializers, and delegates the concrete binding back to `route`.

Both are non-epistemic control skills: successful selection or routing creates
no scientific warrant and cannot promote the status of child outputs.

## Proof Depth Control Stack

The proof-depth stack prevents theorem-shaped cycles from being promoted when
they are shallow, fragmented, definition-built, or locally valid without moving
a hard gate. It forces each cycle to expose conceptual pressure, critical value,
hard-gate movement, nontriviality, transfer substance, same-domain status,
inference-level learning, and a release decision. The deterministic validators
and reports live under `agentic/scripts/validate_proof_depth_control.py`,
`agentic/scripts/build_proof_learning_ledger.py`, and
`agentic/scripts/build_proof_lockin_report.py`.

Publication consolidation is bounded: once a subgoal enters lock-in, the
default limit is four completion cycles and recursion depth one. The lock-in
report must keep the local publication subgoal and the larger target problem
separate, name budget-exhaustion stop conditions, and release the workflow back
to conceptual exploration before any fresh consolidation window starts.

- [`proof-depth-pressure-formalizer`](../../skills/evaluation/proof-depth-pressure-formalizer/SKILL.md)
- [`proof-hard-gate-selector`](../../skills/orchestration/proof-hard-gate-selector/SKILL.md)
- [`proof-nontriviality-auditor`](../../skills/evaluation/proof-nontriviality-auditor/SKILL.md)
- [`proof-conceptual-quality-heuristic-rater`](../../skills/evaluation/proof-conceptual-quality-heuristic-rater/SKILL.md)
- [`proof-transfer-substance-auditor`](../../skills/evaluation/proof-transfer-substance-auditor/SKILL.md)
- [`proof-same-domain-transfer-certifier`](../../skills/evaluation/proof-same-domain-transfer-certifier/SKILL.md)
- [`proof-bridge-object-forger`](../../skills/reasoning/proof-bridge-object-forger/SKILL.md)
- [`proof-creative-variant-prober`](../../skills/reasoning/proof-creative-variant-prober/SKILL.md)
- [`proof-inference-learning-extractor`](../../skills/evaluation/proof-inference-learning-extractor/SKILL.md)
- [`proof-learning-ledger-maintainer`](../../skills/evaluation/proof-learning-ledger-maintainer/SKILL.md)
- [`proof-exploration-critical-mass-assessor`](../../skills/evaluation/proof-exploration-critical-mass-assessor/SKILL.md)
- [`proof-strategy-lockin-orchestrator`](../../skills/orchestration/proof-strategy-lockin-orchestrator/SKILL.md)
- [`proof-depth-release-gate`](../../skills/evaluation/proof-depth-release-gate/SKILL.md)

## Conceptual Abstraction Revision Layer

This layer is now part of the main discovery workflow. It runs before another
branch is promoted when a route feels shallow, definition-built, fragmented, or
locked into the wrong representation. Its required product is a declarative
tension, an abstraction-fit verdict, and efficient-representation requirements:
what objects must be represented, which invariants must survive, which
operations must be cheap, what equivalence relation is allowed, what transfer
interface is needed, and what falsifier would demote the representation.

- [`mathematical-concept-gap-revisitor`](../../skills/evaluation/mathematical-concept-gap-revisitor/SKILL.md)
- [`abstraction-fit-gap-auditor`](../../skills/evaluation/abstraction-fit-gap-auditor/SKILL.md)
- [`efficient-representation-requirements-elicitor`](../../skills/reasoning/efficient-representation-requirements-elicitor/SKILL.md)

## Theory-First Reflective Conceptual Discovery Core

Reflective conceptual discovery is the central controller of the canonical
discovery cycle. Its objective is not rapid truth filtering alone, but the
generation and convergence of theories with high target relevance, unification
power, conceptual depth, and philosophical intelligibility. The cycle rebases
on the newest target-scoped literature before hypothesis generation, deliberately
opens aggressive high-risk conceptual corners, matures independent branches in
parallel without cross-branch contamination, and then performs conflict-preserving
reflective synthesis. Literature can revise the conceptual frame at every cycle;
it is not a one-time bibliography pass.

Dynamic symbolic reasoning and simulation are conditional support operators.
They answer a mature question selected by the reflective theory cycle, preserve
theory-versus-probe provenance, and may calibrate, discriminate, or falsify a
route; experiment output cannot select or silently promote the governing theory.

- Central parent: [`reflective-conceptual-discovery`](../../skills/orchestration/reflective-conceptual-discovery/SKILL.md)
- Current-literature rebase: [`frontier-literature-assimilator`](../../skills/reasoning/frontier-literature-assimilator/SKILL.md)
- High-risk/high-reward divergence: [`high-risk-hypothesis-forger`](../../skills/reasoning/high-risk-hypothesis-forger/SKILL.md)
- Parallel isolated maturation and reducer merge: [`parallel-hypothesis-portfolio`](../../skills/orchestration/parallel-hypothesis-portfolio/SKILL.md)
- Philosophical and theoretical convergence: [`reflective-theory-synthesizer`](../../skills/reasoning/reflective-theory-synthesizer/SKILL.md)
- Blind plural conceptual convergence: [`blind-conceptual-preference-adjudicator`](../../skills/evaluation/blind-conceptual-preference-adjudicator/SKILL.md)
- Theory-requested symbolic/simulation support: [`dynamic-symbolic-simulation-experimenter`](../../skills/reasoning/dynamic-symbolic-simulation-experimenter/SKILL.md)

## Yang-Mills Representational Dynamics Overlay

## Category/HoTT Consequence-Bearing Abstraction Layer

The abstraction layer activates category theory or HoTT only from witnessed
structural pressure. [`categorical-concept-forger`](../../skills/discovery/categorical-concept-forger/SKILL.md)
and [`hott-equivalence-coherence-forger`](../../skills/discovery/hott-equivalence-coherence-forger/SKILL.md)
reuse the shared discovery-lens heuristic, require an exact noncommutativity or
noncoherence witness, and compare the same obligation with and without the new
abstraction. [`ym-categorical-hott-physics-bridge`](../../skills/yang_mills/ym-categorical-hott-physics-bridge/SKILL.md)
then restores Yang--Mills carriers, quantifiers, calibration cases, continuum/OS
burdens, and a physical refinement-or-demotion decision. The generic forge packet v4 and Yang--Mills bridge v6 replay
finite category actions/laws and cone scope, finite HoTT term/fiber transport
and coherence boundaries, registry-bound countermodels, source-specific finite evidence, an absence-only continuum-authority gate, a fourteen-row physics handback, and nine registered YM calibration runners. The shared five-arm executor runs actual condition forgers
over the same sealed cases with request/seed/cell/source/output receipts. It is
still internal protocol calibration because the repository authors the forgers,
cases, rubric, and evaluator; it cannot authorize conceptual value, high physics
reward, a theorem, or truth.

See [`../case-studies/yang-mills/categorical-hott-conceptual-discovery-plan.md`](../case-studies/yang-mills/categorical-hott-conceptual-discovery-plan.md)
for the parallel route, typed boundaries, and negative-control matrix.

## Yang-Mills Representational Dynamics Overlay

The Yang-Mills representational dynamics overlay is target-scoped to
`yang-mills-existence-and-mass-gap-target`. It adapts 17 imported programme
skills and three source-preserving conditional proof skills into
`skills/yang_mills/`, then wires them into the discovery marathon as a
representation-aware workflow layer. The overlay forces exact Clay target
freezing, observable-core discipline, representation calculus, regulator/RG
obligations, basin-entry pressure, continuum/OS transfer boundaries,
restricted-model calibration, mechanized finite cores, and conservative
frontier audits.

The overlay is not a Clay proof. It treats the imported package as a restricted
theorem suite and research programme whose finite or conditional outputs must
carry claim level, hypotheses, non-claims, hard gate, falsifier, and demotion
trigger before affecting a marathon cycle.

- [`ym-freeze-clay-target`](../../skills/yang_mills/ym-freeze-clay-target/SKILL.md)
- [`ym-build-observable-core`](../../skills/yang_mills/ym-build-observable-core/SKILL.md)
- [`ym-build-representation-calculus`](../../skills/yang_mills/ym-build-representation-calculus/SKILL.md)
- [`ym-define-relational-rigidity`](../../skills/yang_mills/ym-define-relational-rigidity/SKILL.md)
- [`ym-design-regulator-atlas`](../../skills/yang_mills/ym-design-regulator-atlas/SKILL.md)
- [`ym-build-gauge-covariant-rg`](../../skills/yang_mills/ym-build-gauge-covariant-rg/SKILL.md)
- [`ym-design-infrared-basin`](../../skills/yang_mills/ym-design-infrared-basin/SKILL.md)
- [`ym-control-large-fields-and-topology`](../../skills/yang_mills/ym-control-large-fields-and-topology/SKILL.md)
- [`ym-prove-basin-entry`](../../skills/yang_mills/ym-prove-basin-entry/SKILL.md)
- [`ym-prove-rg-to-rigidity`](../../skills/yang_mills/ym-prove-rg-to-rigidity/SKILL.md)
- [`ym-prove-continuum-coherence`](../../skills/yang_mills/ym-prove-continuum-coherence/SKILL.md)
- [`ym-prove-rigidity-transfer`](../../skills/yang_mills/ym-prove-rigidity-transfer/SKILL.md)
- [`ym-reconstruct-os-gap`](../../skills/yang_mills/ym-reconstruct-os-gap/SKILL.md)
- [`ym-calibrate-restricted-models`](../../skills/yang_mills/ym-calibrate-restricted-models/SKILL.md)
- [`ym-mechanize-proof-core`](../../skills/yang_mills/ym-mechanize-proof-core/SKILL.md)
- [`ym-audit-frontier`](../../skills/yang_mills/ym-audit-frontier/SKILL.md)
- [`ym-run-clay-program`](../../skills/yang_mills/ym-run-clay-program/SKILL.md)

The three imported `2026-07-21` proof operators below retain exact target and
source-version scope. They produce finite or conditional proof packets, require
the newest literature snapshot and assimilation receipt, and cannot promote a
continuum or mass-gap claim by themselves.

- [`ym-prove-adaptive-block-domination`](../../skills/yang_mills/ym-prove-adaptive-block-domination/SKILL.md)
- [`ym-prove-conditional-partition-ratio`](../../skills/yang_mills/ym-prove-conditional-partition-ratio/SKILL.md)
- [`ym-prove-state-weighted-defect-transfer`](../../skills/yang_mills/ym-prove-state-weighted-defect-transfer/SKILL.md)

Primary validation handoff:
`python3 agentic/scripts/validate_ym_workflow_integration.py`.

## Physical Relevance And General Impact Gate

The Yang-Mills workflow now separates rigorous local mathematics from
physics-facing impact. A finite lemma, algebraic identity, Schur complement,
endpoint calculation, or restricted-model result is support-only unless it
names the physical carrier, the same-theory handoff, the continuum/OS/spectral
target gate, the field-facing understanding it changes, and its unification
power: which previously separate physics or proof pressures one mechanism,
carrier, estimate, or representation compresses. Future YM cycles attach a
deterministic `physical_relevance_impact` packet, and cycle `0352+` must expose
the packet before promotion.

- [`physical-relevance-impact-auditor`](../../skills/evaluation/physical-relevance-impact-auditor/SKILL.md)

## Literature Gap Preinvestment Gate

Every major new proof avenue now requires a target-scoped literature-gap warrant
before broad branch exploration. The warrant names the smallest honest claim,
closest known results, precise gap, novelty boundary, field or physics impact,
unification power, route-decision power, disqualifiers, explicit unknowns,
allowed next modes, and investment decision. The gate blocks incremental,
shallow, or rediscovered avenues unless they can plausibly become a major
publication or route-deciding result; otherwise they are routed to artifact
sprints, literature reframing, prior-art stop, or quarantine.

- [`literature-gap-relevance-auditor`](../../skills/evaluation/literature-gap-relevance-auditor/SKILL.md)

## Failure Archaeology And Failed-Hypothesis Premortem

Major failed, demoted, quarantined, artifact-blocked, or repeated-blocker
cycle sets now produce a target-scoped failure archaeology packet. The packet
explains why the problem was genuinely hard in physics and mathematics, why
the attempted route failed, why the failure was not anticipated, and which
declarative prompt heuristics should guard the next cycle. Future branch
prompts must also name at least one anticipatable failure signature before
ordinary proof search continues.

- [`failure-archaeology-explainer`](../../skills/evaluation/failure-archaeology-explainer/SKILL.md)
- [`failed-hypothesis-anticipator`](../../skills/evaluation/failed-hypothesis-anticipator/SKILL.md)

## Visual Conceptualization Reflection

Deep reflection cycles can now explain theorem mechanisms and conceptual
obstructions through visual metaphors, but only under property-preservation
discipline. A metaphor must name the formal objects, key invariants, symmetries,
positivity or sign structure, limiting behavior, physical carrier, proof
obligations, distortions, and any hypothesis it inspires. Visual analogies are
reflection artifacts unless a preservation audit promotes a concrete route
mutation, missing artifact, falsifier, counterfactual variant, or representation
requirement.

- [`visual-theorem-conceptualizer`](../../skills/evaluation/visual-theorem-conceptualizer/SKILL.md)
- [`visual-analogy-preservation-auditor`](../../skills/evaluation/visual-analogy-preservation-auditor/SKILL.md)

## P vs NP Inference-Quality Control

The P vs NP workflow now has a dedicated quality-control stack for theorem-shaped, transfer-shaped, contradiction, no-go, barrier, proof-complexity, and meta-complexity claims. See [`P vs NP Inference Quality Criteria`](../case-studies/pvsnp/pvsnp-inference-quality.md).

- [`pvsnp-inference-quality-controller`](../../skills/orchestration/pvsnp-inference-quality-controller/SKILL.md)
- [`pvsnp-proof-derivation-builder`](../../skills/reasoning/pvsnp-proof-derivation-builder/SKILL.md)
- [`pvsnp-reduction-consistency-reviewer`](../../skills/evaluation/pvsnp-reduction-consistency-reviewer/SKILL.md)
- [`pvsnp-quantifier-uniformity-reviewer`](../../skills/evaluation/pvsnp-quantifier-uniformity-reviewer/SKILL.md)
- [`pvsnp-barrier-specificity-reviewer`](../../skills/evaluation/pvsnp-barrier-specificity-reviewer/SKILL.md)
- [`pvsnp-proof-complexity-transfer-reviewer`](../../skills/evaluation/pvsnp-proof-complexity-transfer-reviewer/SKILL.md)
- [`pvsnp-meta-complexity-carrier-reviewer`](../../skills/evaluation/pvsnp-meta-complexity-carrier-reviewer/SKILL.md)

## Proof Delivery Subworkflows

Proof delivery skills are invoked when a queue item has become theorem-shaped and should stop producing strategy prose. They force a bounded proof outcome: proved theorem, conditional theorem, blocked named lemma, countermodel/no-go theorem, or quarantine.

- [`proof-delivery-workflow-orchestrator`](../../skills/proof_delivery/proof-delivery-workflow-orchestrator/SKILL.md)
- [`proof-obligation-formalizer`](../../skills/proof_delivery/proof-obligation-formalizer/SKILL.md)
- [`lemma-chain-proof-builder`](../../skills/proof_delivery/lemma-chain-proof-builder/SKILL.md)
- [`proof-gap-countermodel-splitter`](../../skills/proof_delivery/proof-gap-countermodel-splitter/SKILL.md)
- [`proof-quality-gatekeeper`](../../skills/proof_delivery/proof-quality-gatekeeper/SKILL.md)
- [`pvsnp-forcedrows-proof-workflow`](../../skills/proof_delivery/pvsnp-forcedrows-proof-workflow/SKILL.md)

## Named Workflow Integration Skills

These skills provide the conceptual and formal handoffs used by the named,
opt-in workflows. Their presence here records that the capability is
catalogued; it does not by itself claim that the skill was routed, executed,
consumed, or allowed to change workflow state.

- [`theory-atlas-defect-compiler`](../../skills/discovery/theory-atlas-defect-compiler/SKILL.md)
  turns source-bounded theory fragments into typed categorical defects and
  finite completion obligations before a Category/HoTT forge is considered.
- [`central-formal-conceptual-routes`](../../skills/orchestration/central-formal-conceptual-routes/SKILL.md)
  compares Category, HoTT, both ordered compositions, and a capable nonformal
  route under matched inputs and a common physics-facing handback.
- [`conceptual-frontier-deepening`](../../skills/orchestration/conceptual-frontier-deepening/SKILL.md)
  coordinates an expensive, theory-first search over a blocked conceptual
  frontier while retaining plural candidates, failures, and authority limits.
- [`pvsnp-negative-tactic-selector`](../../skills/orchestration/pvsnp-negative-tactic-selector/SKILL.md)
  chooses a bounded P-vs-NP negative tactic only when the active obstruction
  and target regime justify it.
- [`formal-claim-producer`](../../skills/reasoning/formal-claim-producer/SKILL.md)
  compiles a sealed formalization seed into a typed ready-or-not-ready claim
  packet without inventing a theorem or asserting proof authority.
- [`literature-conditioned-invention-forger`](../../skills/reasoning/literature-conditioned-invention-forger/SKILL.md)
  makes current bounded literature a causal input to pre-taxonomy invention
  while preserving counterfactual, provenance, and non-authority boundaries.

## Skill Hierarchy

- **control-plane**: Looper governance, target control, hook policy, promotion decisions, and meta-reflection over the discovery process.
- **ingest**: Source acquisition and conversion into KB-ready statements, literature packets, and normalized theorem bodies.
- **reasoning**: Generative mathematical, complexity-theoretic, and physical reasoning skills: abduction, deduction, induction, contradiction, qualitative relation analysis, impossibility/no-go formation, and Gedanken design.
- **discovery**: KB graph navigation, bridge discovery, entrypoint selection, proof strategy formation, and discovery-cycle queue construction.
- **proof_delivery**: theorem-shaped queue subworkflows that formalize proof obligations, build lemma chains, split gaps into countermodels or blocked lemmas, gate proof quality, and hand off paper-ready proof packets.
- **evaluation**: Epistemic, mathematical, literature-gap, physical-relevance, failure-archaeology, failed-hypothesis premortem, visual-analogy preservation, adversarial, contribution, payoff, and falsification checks that decide whether a route should continue, pivot, or stop.
- **orchestration**: Workflow-level routing, long-horizon branch control, queue ranking, and run/report coordination.
- **reporting**: Expert handoff, contribution packaging, paper construction, timeline-to-LaTeX translation, references, diagrams, and formal derivation surfaces.
- **results_ellaboration**: independent paper-result expansion and Route A paper-attack workflow for interpreting drafts, extracting result-extension needs and open modules, planning self-contained TODOs, separating deterministic/generative regimes, certifying theorem scope, formalizing finite objects, deriving proof packets, auditing prior-art/disqualifier boundaries, gatekeeping paper readiness, actively attacking paper-specific proof obligations, and integrating validated results into manuscript narrative without process jargon.
- **yang_mills**: target-scoped representational dynamics overlay for Yang-Mills Clay-target freezing, observable and representation calculus, regulator/RG design, basin-entry and continuum/spectral transfer gates, restricted-model calibration, mechanization, and frontier audit.
- **review**: Multi-persona review skills for logic, epistemology, discovery science, mathematical depth, and system design.
- **common modules**: shared Python support library used by executable skills; these modules are not directly invocable skills.

## Inventory Summary

| Group | Skills | Purpose |
|---|---:|---|
| `control-plane` | 6 | Looper governance, target control, hook policy, promotion decisions, and meta-reflection over the discovery process. |
| `ingest` | 6 | Source acquisition and conversion into KB-ready statements, literature packets, and normalized theorem bodies. |
| `reasoning` | 25 | Generative mathematical, complexity-theoretic, symbolic, and physical reasoning skills: abduction, deduction, induction, contradiction, P vs NP Gedanken design, pressure-to-bridge abstraction, efficient-representation requirement elicitation, qualitative relation analysis, exact transfer auditing, impossibility/no-go formation, and Gedanken design. |
| `discovery` | 16 | KB graph navigation, bridge discovery, entrypoint selection, proof strategy formation, and discovery-cycle queue construction. |
| `proof_delivery` | 6 | Theorem-shaped proof subworkflows that convert high-priority queue items into formal proof packets, conditional theorems, named blocked lemmas, countermodels, or quarantine decisions. |
| `evaluation` | 38 | Epistemic, mathematical, literature-gap, physical-relevance, failure-archaeology, failed-hypothesis premortem, visual-analogy preservation, adversarial, contribution, payoff, enablement, conceptual-abstraction revision, and falsification checks that decide whether a route should continue, pivot, or stop. |
| `orchestration` | 15 | Workflow-level routing, long-horizon branch control, queue ranking, and run/report coordination. |
| `reporting` | 29 | Expert handoff, contribution and enablement packaging, paper construction, timeline-to-LaTeX translation, definition/assumption elicitation, references, diagrams, and formal derivation surfaces. |
| `results_ellaboration` | 28 | Independent paper-result expansion workflow plus recurring paper-subgoal certification, theorem-scope control, finite-object formalization, proof-packet derivation, prior-art/disqualifier audit, paper-readiness gatekeeping, Route A paper-attack, and second-wave open-point skills for draft markers, open modules, collar redesign, edge validation, same-theory normalization, symbolic/CAS audits, coefficient extraction, finite margins, endpoint certification, continuum/gap gatekeeping, and result-safe narrative integration. |
| `yang_mills` | 20 | Target-scoped representational dynamics overlay for claim-leveled Yang-Mills source integration, skill dispatch, restricted-model calibration, conditional proof-object construction, and conservative frontier audit. |
| `review` | 6 | Multi-persona review skills for logic, epistemology, discovery science, mathematical depth, and system design. |
| `common` | 21 modules | Shared contracts, graph utilities, reasoning logs, queues, and mathematical support functions. |

## Quick Index

- **control-plane**: [`looper-hook-policy-maintainer`](#looper-hook-policy-maintainer), [`looper-release-promoter`](#looper-release-promoter), [`looper-target-dependency-cartographer`](#looper-target-dependency-cartographer), [`looper-target-goal-enricher`](#looper-target-goal-enricher), [`looper-workflow-contract-governor`](#looper-workflow-contract-governor), [`meta`](#meta)
- **ingest**: [`evidence-acquisition-planner`](#evidence-acquisition-planner), [`latex-kb-ingest`](#latex-kb-ingest), [`prior-art-importer`](#prior-art-importer), [`pvsnp-kb-parser`](#pvsnp-kb-parser), [`target-literature-source-curator`](#target-literature-source-curator), [`theorem-body-normalizer`](#theorem-body-normalizer)
- **reasoning**: [`efficient-representation-requirements-elicitor`](#efficient-representation-requirements-elicitor), [`gedanken-counterfactual-variant-builder`](#gedanken-counterfactual-variant-builder), [`gedanken-situation-designer`](#gedanken-situation-designer), [`kb-abduce`](#kb-abduce), [`kb-contradiction-strategist`](#kb-contradiction-strategist), [`kb-deduce`](#kb-deduce), [`kb-explain`](#kb-explain), [`kb-induce`](#kb-induce), [`monotonicity-sensitivity-prober`](#monotonicity-sensitivity-prober), [`physics-regime-map-builder`](#physics-regime-map-builder), [`pvsnp-gedanken-complexity-lab`](#pvsnp-gedanken-complexity-lab), [`pvsnp-impossibility-theorem-forger`](#pvsnp-impossibility-theorem-forger), [`pvsnp-pressure-bridge-forger`](#pvsnp-pressure-bridge-forger), [`pvsnp-qualitative-complexity-reasoner`](#pvsnp-qualitative-complexity-reasoner), [`pvsnp-symbolic-complexity-auditor`](#pvsnp-symbolic-complexity-auditor), [`qualitative-toy-model-builder`](#qualitative-toy-model-builder), [`qualitative-variable-isolator`](#qualitative-variable-isolator), [`scale-asymptotic-reasoner`](#scale-asymptotic-reasoner)
- **discovery**: [`abducer-mediation-candidate-generator`](#abducer-mediation-candidate-generator), [`kb-coherence-evaluator`](#kb-coherence-evaluator), [`kb-concept-bridge-planner`](#kb-concept-bridge-planner), [`kb-discovery-cycle`](#kb-discovery-cycle), [`kb-entrypoint-finder`](#kb-entrypoint-finder), [`kb-entrypoint-pathfinder`](#kb-entrypoint-pathfinder), [`kb-epistemic-hardness`](#kb-epistemic-hardness), [`kb-framework-state-formalizer`](#kb-framework-state-formalizer), [`kb-gap-abstraction-conjecturer`](#kb-gap-abstraction-conjecturer), [`kb-main-conjecture-grounder`](#kb-main-conjecture-grounder), [`kb-novel-proof-strategist`](#kb-novel-proof-strategist), [`kb-prior-art-pass`](#kb-prior-art-pass), [`kb-promising-direction-assessor`](#kb-promising-direction-assessor), [`kb-proof-connector`](#kb-proof-connector), [`kb-proof-sketcher`](#kb-proof-sketcher), [`kb-prove-cycle`](#kb-prove-cycle)
- **proof_delivery**: [`lemma-chain-proof-builder`](#lemma-chain-proof-builder), [`proof-delivery-workflow-orchestrator`](#proof-delivery-workflow-orchestrator), [`proof-gap-countermodel-splitter`](#proof-gap-countermodel-splitter), [`proof-obligation-formalizer`](#proof-obligation-formalizer), [`proof-quality-gatekeeper`](#proof-quality-gatekeeper), [`pvsnp-forcedrows-proof-workflow`](#pvsnp-forcedrows-proof-workflow)
- **yang_mills**: [`ym-freeze-clay-target`](../../skills/yang_mills/ym-freeze-clay-target/SKILL.md), [`ym-build-observable-core`](../../skills/yang_mills/ym-build-observable-core/SKILL.md), [`ym-build-representation-calculus`](../../skills/yang_mills/ym-build-representation-calculus/SKILL.md), [`ym-run-clay-program`](../../skills/yang_mills/ym-run-clay-program/SKILL.md), plus the remaining target-scoped YM overlay skills listed above.
- **evaluation**: [`abducer-conceptual-pressure-formalizer`](#abducer-conceptual-pressure-formalizer), [`abducer-failure-signal-cartographer`](#abducer-failure-signal-cartographer), [`abducer-obligation-gatekeeper`](#abducer-obligation-gatekeeper), [`abstraction-fit-gap-auditor`](#abstraction-fit-gap-auditor), [`bridge-object-equivalence-checker`](#bridge-object-equivalence-checker), [`completed-subgoal-enablement-auditor`](#completed-subgoal-enablement-auditor), [`contradiction-route-auditor`](#contradiction-route-auditor), [`contribution-value-assessor`](#contribution-value-assessor), [`counterexample-hunter`](#counterexample-hunter), [`counterfactual-route-prober`](#counterfactual-route-prober), [`dimensional-symmetry-constraint-checker`](#dimensional-symmetry-constraint-checker), [`entailment-gap-auditor`](#entailment-gap-auditor), [`epistemic-status-ledger`](#epistemic-status-ledger), [`failed-hypothesis-anticipator`](#failed-hypothesis-anticipator), [`failure-archaeology-explainer`](#failure-archaeology-explainer), [`gedanken-need-assessor`](#gedanken-need-assessor), [`gedanken-transfer-guard`](#gedanken-transfer-guard), [`hub-bias-auditor`](#hub-bias-auditor), [`kb-discovery-breakthrough-profiler`](#kb-discovery-breakthrough-profiler), [`kb-discovery-governor`](#kb-discovery-governor), [`kb-end-to-end-proof-critic`](#kb-end-to-end-proof-critic), [`kb-hypothesis-evaluator`](#kb-hypothesis-evaluator), [`kb-hypothesis-refutation-loop`](#kb-hypothesis-refutation-loop), [`kb-revision-loop`](#kb-revision-loop), [`limit-convergence-behavior-auditor`](#limit-convergence-behavior-auditor), [`literature-gap-relevance-auditor`](#literature-gap-relevance-auditor), [`main-problem-alignment-auditor`](#main-problem-alignment-auditor), [`mathematical-concept-gap-revisitor`](#mathematical-concept-gap-revisitor), [`paper-contribution-readiness-judge`](#paper-contribution-readiness-judge), [`physical-relevance-impact-auditor`](#physical-relevance-impact-auditor), [`premise-completeness-prober`](#premise-completeness-prober), [`progression-payoff-judge`](#progression-payoff-judge), [`pvsnp-conceptual-pressure-localizer`](#pvsnp-conceptual-pressure-localizer), [`qualitative-physics-falsifier`](#qualitative-physics-falsifier), [`regime-shift-auditor`](#regime-shift-auditor), [`scientific-contribution-detector`](#scientific-contribution-detector), [`visual-analogy-preservation-auditor`](#visual-analogy-preservation-auditor), [`visual-theorem-conceptualizer`](#visual-theorem-conceptualizer)
- **orchestration**: [`abducer-refinement-route-ranker`](#abducer-refinement-route-ranker), [`contribution-oriented-subgoal-manager`](#contribution-oriented-subgoal-manager), [`gedanken-followup-planner`](#gedanken-followup-planner), [`kb-orchestrator`](#kb-orchestrator), [`long-horizon-route-portfolio-manager`](#long-horizon-route-portfolio-manager), [`next-experiment-queue-ranker`](#next-experiment-queue-ranker), [`result-atlas-maintainer`](#result-atlas-maintainer), [`show-reasoning`](#show-reasoning), [`work`](#work)
- **reporting**: [`endpoint-worked-calculation-packager`](#endpoint-worked-calculation-packager), [`expert-handoff`](#expert-handoff), [`finite-theorem-section-packager`](#finite-theorem-section-packager), [`kb-expert-paper-generator`](#kb-expert-paper-generator), [`kb-macro-proof-paper-writer`](#kb-macro-proof-paper-writer), [`prior-art-positioning-packager`](#prior-art-positioning-packager), [`scientific-contribution-paper-handoff`](#scientific-contribution-paper-handoff), [`subgoal-enablement-handoff-packager`](#subgoal-enablement-handoff-packager), [`target-literature-evolution-narrator`](#target-literature-evolution-narrator), [`timeline-claim-boundary-auditor`](#timeline-claim-boundary-auditor), [`timeline-contribution-explainer`](#timeline-contribution-explainer), [`timeline-contribution-stater`](#timeline-contribution-stater), [`timeline-cycle-latex-translator`](#timeline-cycle-latex-translator), [`timeline-definition-assumption-elicitor`](#timeline-definition-assumption-elicitor), [`timeline-failed-route-interpreter`](#timeline-failed-route-interpreter), [`timeline-formal-physics-deriver`](#timeline-formal-physics-deriver), [`timeline-narrative-coherence-guard`](#timeline-narrative-coherence-guard), [`timeline-organizing-diagram-builder`](#timeline-organizing-diagram-builder), [`timeline-paper-argument-architect`](#timeline-paper-argument-architect), [`timeline-paper-cross-section-reconciler`](#timeline-paper-cross-section-reconciler), [`timeline-paper-section-synthesizer`](#timeline-paper-section-synthesizer), [`timeline-paper-workflow-orchestrator`](#timeline-paper-workflow-orchestrator), [`timeline-problem-literature-latex-translator`](#timeline-problem-literature-latex-translator), [`timeline-problem-space-narrator`](#timeline-problem-space-narrator), [`timeline-reference-manager`](#timeline-reference-manager), [`timeline-report-evidence-ingestor`](#timeline-report-evidence-ingestor), [`timeline-report-latex-composer`](#timeline-report-latex-composer), [`timeline-story-latex-translator`](#timeline-story-latex-translator), [`timeline-summary-latex-translator`](#timeline-summary-latex-translator)
- **results_ellaboration**: [`results-context-interpreter`](#results-context-interpreter), [`results-critical-self-refiner`](#results-critical-self-refiner), [`results-elaboration-workflow-orchestrator`](#results-elaboration-workflow-orchestrator), [`results-expansion-validator`](#results-expansion-validator), [`results-extension-need-extractor`](#results-extension-need-extractor), [`results-extension-strategy-planner`](#results-extension-strategy-planner), [`results-finite-object-formalizer`](#results-finite-object-formalizer), [`results-narrative-integrator`](#results-narrative-integrator), [`results-open-module-decomposer`](#results-open-module-decomposer), [`results-paper-readiness-gatekeeper`](#results-paper-readiness-gatekeeper), [`results-prior-art-disqualifier-auditor`](#results-prior-art-disqualifier-auditor), [`results-proof-packet-deriver`](#results-proof-packet-deriver), [`results-theorem-scope-certifier`](#results-theorem-scope-certifier), [`routea-collar-redesign-forger`](#routea-collar-redesign-forger), [`routea-continuum-gap-gatekeeper`](#routea-continuum-gap-gatekeeper), [`routea-endpoint-error-budget-certifier`](#routea-endpoint-error-budget-certifier), [`routea-endpoint-local-integral-calculator`](#routea-endpoint-local-integral-calculator), [`routea-finite-margin-evaluator`](#routea-finite-margin-evaluator), [`routea-geometric-coefficient-extractor`](#routea-geometric-coefficient-extractor), [`routea-geometric-collar-builder`](#routea-geometric-collar-builder), [`routea-margin-endpoint-certifier`](#routea-margin-endpoint-certifier), [`routea-open-point-orchestrator`](#routea-open-point-orchestrator), [`routea-paper-attack-orchestrator`](#routea-paper-attack-orchestrator), [`routea-paper-result-integrator`](#routea-paper-result-integrator), [`routea-same-theory-factorization-hunter`](#routea-same-theory-factorization-hunter), [`routea-same-theory-normalization-certifier`](#routea-same-theory-normalization-certifier), [`routea-second-wave-manuscript-integrator`](#routea-second-wave-manuscript-integrator), [`routea-symbolic-cas-auditor`](#routea-symbolic-cas-auditor)
- **review**: [`review-reasoner`](#review-reasoner), [`review-reasoner-concept-logician`](#review-reasoner-concept-logician), [`review-reasoner-discovery-scientist`](#review-reasoner-discovery-scientist), [`review-reasoner-epistemologist`](#review-reasoner-epistemologist), [`review-reasoner-fields-medalist`](#review-reasoner-fields-medalist), [`review-reasoner-radical-designer`](#review-reasoner-radical-designer)

## Skill Details

### control-plane

Looper governance, target control, hook policy, promotion decisions, and meta-reflection over the discovery process.

#### `looper-hook-policy-maintainer`

- **Skill file:** [Open skill](../../skills/control-plane/looper-hook-policy-maintainer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Maintain transparent deterministic hook policy for Abducer's Looper control plane. Use when UserPromptSubmit, PreSkillUse, PostSkillUse, PreToolUse, or Stop hooks need review, repair, or extension.
- **Conceptual role:** This skill keeps hooks small, deterministic, and visible. Hooks may log, warn, or block. They must not hide target navigation or proof-search reasoning.
- **Workflow shape:** Check that each hook has a deterministic event, script, and test fixture.; Reject hook behavior that performs hidden orchestration, generative; Ensure warning and blocking decisions cite concrete policy reasons.; Require Stop hooks to protect current target, dependency frontier,; Produce repair instructions and fixtures when a hook changes.
- **Agent config:** [openai.yaml](../../skills/control-plane/looper-hook-policy-maintainer/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/control-plane/looper-hook-policy-maintainer/references/prompt-template.md)
- **Outputs:** Return: decision, cited evidence paths or explicit unknowns, unresolved mathematical debt, rollback/quarantine condition, and next validator. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote or quarantine on uncited artifacts, missing target packet IDs, hidden hooks, stale gates, unsupported proof claims, or drift from essential target commitments.

#### `looper-release-promoter`

- **Skill file:** [Open skill](../../skills/control-plane/looper-release-promoter/SKILL.md)
- **Mode:** Generative agent
- **Description:** Interpret compliance, drift, dependency, workflow, hook, and validation evidence to promote, quarantine, roll back, or escalate a controlled Abducer iteration. Use at the end of target-navigation and Looper-controlled work-loop slices.
- **Conceptual role:** This skill is the generative release interpretation layer. Deterministic reports count evidence; this skill decides what the evidence means for promotion, quarantine, rollback, or escalation.
- **Workflow shape:** Identify the controlled iteration and target.; Summarize what changed and which workflow executed.; Check whether all blocking gates have evidence.; Separate passing evidence from fragile, missing, waived, or drift-risk; Recommend promote, quarantine, rollback, or escalate.; State rollback path and open blockers.
- **Agent config:** [openai.yaml](../../skills/control-plane/looper-release-promoter/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/control-plane/looper-release-promoter/references/prompt-template.md)
- **Outputs:** Return: decision, cited evidence paths or explicit unknowns, unresolved mathematical debt, rollback/quarantine condition, and next validator. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote or quarantine on uncited artifacts, missing target packet IDs, hidden hooks, stale gates, unsupported proof claims, or drift from essential target commitments.

#### `looper-target-dependency-cartographer`

- **Skill file:** [Open skill](../../skills/control-plane/looper-target-dependency-cartographer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Recursively cartograph all proof, premise, route, bridge, queue, InformalMathLib, and evidence dependencies for a validated Abducer target packet. Use when a target must become goal-oriented and dependency-controlled.
- **Conceptual role:** This skill is the generative interpretation layer over the deterministic dependency graph. It decides which open dependency nodes matter, how they should be grouped into proof work, and where Abducer should continue, revise, or stop.
- **Workflow shape:** Read the target packet and its acceptance gates.; Inspect the generated dependency graph, not just the raw artifact list.; Classify unresolved nodes by mathematical role: missing premise, bridge; Identify the next frontier that best serves the target rather than merely the; Recommend the next Abducer workflow route and the skill sequence required.; Produce a dependency-closure report and frontier update.
- **Agent config:** [openai.yaml](../../skills/control-plane/looper-target-dependency-cartographer/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/control-plane/looper-target-dependency-cartographer/references/prompt-template.md)
- **Outputs:** Return: decision, cited evidence paths or explicit unknowns, unresolved mathematical debt, rollback/quarantine condition, and next validator. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote or quarantine on uncited artifacts, missing target packet IDs, hidden hooks, stale gates, unsupported proof claims, or drift from essential target commitments.

#### `looper-target-goal-enricher`

- **Skill file:** [Open skill](../../skills/control-plane/looper-target-goal-enricher/SKILL.md)
- **Mode:** Generative agent
- **Description:** Enrich a raw mathematical target into a validated Abducer target packet with output type, quality criteria, acceptance gates, constraints, unknowns, validation targets, and evidence paths. Use before controlled target-navigation or recursive dependency closure.
- **Conceptual role:** This skill is the generative intake layer for Abducer's Looper control plane. It converts a raw mathematical ambition into a target packet that can be validated, recursively expanded, and governed.
- **Workflow shape:** Identify the concrete mathematical target and distinguish it from broad; Resolve the target to one or more KB statement IDs when possible.; Infer the output type: proof route, proof sketch, refutation, dependency map,; Select quality criteria that are task-specific and measurable.; Create acceptance gates that can block release.; Preserve hard constraints exactly, including source policy, local-only gates,; State unknowns as decision-relevant gaps rather than generic questions.; Emit a target packet conforming to `agentic/spec/target_packet_schema.json`.
- **Agent config:** [openai.yaml](../../skills/control-plane/looper-target-goal-enricher/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/control-plane/looper-target-goal-enricher/references/prompt-template.md)
- **Outputs:** Return: decision, cited evidence paths or explicit unknowns, unresolved mathematical debt, rollback/quarantine condition, and next validator. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote or quarantine on uncited artifacts, missing target packet IDs, hidden hooks, stale gates, unsupported proof claims, or drift from essential target commitments.

#### `looper-workflow-contract-governor`

- **Skill file:** [Open skill](../../skills/control-plane/looper-workflow-contract-governor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Govern visible Abducer workflows by checking composed skills, deterministic hooks, required artifacts, validators, gate decisions, and handoffs. Use when target-navigation or work-loop routes must be controlled by explicit workflow contracts.
- **Conceptual role:** This skill keeps workflows as the visible unit. It interprets whether a run is properly composed from skills, hooks, artifacts, validators, and gate decisions.
- **Workflow shape:** Read the active task manifest from its `visible_workflows` section first.; Verify that every named skill, hook, workflow reference, artifact, and; Interpret gate decisions using the shared gate policy.; Identify lifecycle gaps, invalid waivers, orphan skills, and stale handoffs.; Recommend whether the workflow may continue, must warn, must block, or must
- **Agent config:** [openai.yaml](../../skills/control-plane/looper-workflow-contract-governor/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/control-plane/looper-workflow-contract-governor/references/prompt-template.md)
- **Outputs:** Return: decision, cited evidence paths or explicit unknowns, unresolved mathematical debt, rollback/quarantine condition, and next validator. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote or quarantine on uncited artifacts, missing target packet IDs, hidden hooks, stale gates, unsupported proof claims, or drift from essential target commitments.

#### `meta`

- **Skill file:** [Open skill](../../skills/control-plane/meta/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Reflect on the nature of the current mathematical discovery process from a chosen perspective, explain why the original problem remains hard, interpret the present proof state and intermediate results, and identify what has genuinely shifted or persisted in understanding. Use when the user asks for meta-analysis, reflective interpretation of the discovery process, or how the current search changed the problem framing.
- **Conceptual role:** This is the meta-analytical reflection layer for the platform. It does not ask only which route is best. It asks what the current search has actually taught us about the problem, what remains structurally hard, and how the present bridge and proof artifacts changed the research perspective.
- **Use when:** `epistemic-hardness.json`; `macro-proof-state.json`; `macro-strategy-report.json`; `proof-cycle-summary.json`; `end-to-end-proof-plausibility.json`; why the original problem is hard and whether that changed;
- **Workflow shape:** Read the current hardness, macro-proof, macro-strategy, proof-cycle, proof-critic, promising-directions, and search-space-tree artifacts.; Choose a perspective from [perspectives.md](../../skills/control-plane/meta/references/perspectives.md).; Interpret the current state through that perspective:; Classify each major change as:; Emit a meta reflection report with explicit references and a final meta-judgment.
- **Scripts:** [archive_legacy_reports.py](../../skills/control-plane/meta/scripts/archive_legacy_reports.py), [generate_discovery_process_slides.py](../../skills/control-plane/meta/scripts/generate_discovery_process_slides.py), [generate_epistemic_process_map.py](../../skills/control-plane/meta/scripts/generate_epistemic_process_map.py), [generate_meta_reflection_report.py](../../skills/control-plane/meta/scripts/generate_meta_reflection_report.py), [generate_proof_discovery_language_report.py](../../skills/control-plane/meta/scripts/generate_proof_discovery_language_report.py), [generate_report_hub.py](../../skills/control-plane/meta/scripts/generate_report_hub.py)
- **Agent config:** [openai.yaml](../../skills/control-plane/meta/agents/openai.yaml)
- **References:** [perspectives.md](../../skills/control-plane/meta/references/perspectives.md), [prompt-template.md](../../skills/control-plane/meta/references/prompt-template.md), [shift-taxonomy.md](../../skills/control-plane/meta/references/shift-taxonomy.md)
- **Outputs:** Return: decision, cited evidence paths or explicit unknowns, unresolved mathematical debt, rollback/quarantine condition, and next validator. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote or quarantine on uncited artifacts, missing target packet IDs, hidden hooks, stale gates, unsupported proof claims, or drift from essential target commitments.

### ingest

Source acquisition and conversion into KB-ready statements, literature packets, and normalized theorem bodies.

#### `evidence-acquisition-planner`

- **Skill file:** [Open skill](../../skills/ingest/evidence-acquisition-planner/SKILL.md)
- **Mode:** Generative agent
- **Description:** For each unresolved hypothesis, proof obligation, contradiction route, or theoretical bridge, propose the cheapest decisive local, prior-art, empirical, lattice, numerical, or web-backed evidence test. Use when a theoretical step requires closely related empirical evidence without letting empirical support replace proof.
- **Conceptual role:** This skill turns unresolved conjectures and theoretical proof obligations into concrete evidence plans. It can request empirical, numerical, simulation, lattice, phenomenological, or experimental evidence when such evidence is closely related to a proof step. Its core job is to keep that evidence useful without confusing it with a theorem.
- **Agent config:** [openai.yaml](../../skills/ingest/evidence-acquisition-planner/agents/openai.yaml)
- **References:** [empirical-evidence-gating.md](../../skills/ingest/evidence-acquisition-planner/references/empirical-evidence-gating.md), [prompt-template.md](../../skills/ingest/evidence-acquisition-planner/references/prompt-template.md)
- **Outputs:** Return: evidence request ID, linked theoretical obligation, evidence mode, empirical observable or source statement, proximity class, search plan, acceptable sources, support/refutation criteria, transfer gap, proof boundary, source IDs, explicit unknowns, artifact paths, validation result, and next repair. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote malformed, uncited, ambiguous, stale, non-proximate, or lossy intake to repair/evidence task instead of using it as reasoning evidence. Quarantine any empirical evidence that is fixed-cutoff, finite-volume, non-gauge-invariant, or analogy-only when the theoretical obligation requires continuum Yang-Mills.

#### `latex-kb-ingest`

- **Skill file:** [Open skill](../../skills/ingest/latex-kb-ingest/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Build or update a single-file mathematical knowledge base from informal LaTeX sources. Use when the user provides web pages, PDFs, notes, or pasted text and asks to extract definitions, axioms, theorems, lemmas, assumptions, or symbol meanings into a structured KB file in the `KB/` folder.
- **Conceptual role:** This skill ingests source documents or extracted statement payloads and writes them back into the KB in the framework's canonical statement format.
- **Framework contribution:** It contributes the disciplined acquisition layer that turns external mathematical material into reusable KB statements.
- **Workflow shape:** Confirm the target KB file.; Build the source index first.; Extract candidate statements from each source chunk.; Normalize and deduplicate.; Commit accepted statements.; Close with a consistency pass.
- **Scripts:** [chunk_sources.py](../../skills/ingest/latex-kb-ingest/scripts/chunk_sources.py), [kb_writeback.py](../../skills/ingest/latex-kb-ingest/scripts/kb_writeback.py)
- **Agent config:** [openai.yaml](../../skills/ingest/latex-kb-ingest/agents/openai.yaml)
- **References:** [kb-schema.md](../../skills/ingest/latex-kb-ingest/references/kb-schema.md), [prompt-template.md](../../skills/ingest/latex-kb-ingest/references/prompt-template.md), [script-usage.md](../../skills/ingest/latex-kb-ingest/references/script-usage.md)
- **Outputs:** KB file path.; Number of sources indexed.; Number of statements added/updated by `kind`.; Number of unresolved gaps.; Highest-risk uncertainty (one sentence).
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote malformed, uncited, ambiguous, or lossy intake to repair/evidence task instead of using it as reasoning evidence.

#### `prior-art-importer`

- **Skill file:** [Open skill](../../skills/ingest/prior-art-importer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Convert externally referenced theorems, definitions, and axioms into InformalMathLib-ready records after justified search. Use when a proof or novelty decision relies on prior art.
- **Conceptual role:** This skill converts externally sourced mathematics into persistent local records.
- **Agent config:** [openai.yaml](../../skills/ingest/prior-art-importer/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/ingest/prior-art-importer/references/prompt-template.md)
- **Outputs:** Return: normalized statements, source IDs, explicit unknowns, parse failures, artifact paths, validation result, and next repair. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote malformed, uncited, ambiguous, or lossy intake to repair/evidence task instead of using it as reasoning evidence.

#### `pvsnp-kb-parser`

- **Skill file:** [Open skill](../../skills/ingest/pvsnp-kb-parser/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Parse LaTeX-heavy P vs NP research reports into structured KB statements and write them into `KB/p-vs-np.kb.md`. Use when the user provides files like `deep-research-report.md` containing `\begin{definition}`/`\begin{theorem}` style environments and asks to ingest them into a PvsNP knowledge base.
- **Conceptual role:** This skill parses structured research notes or deep-research reports into candidate mathematical statements for KB population.
- **Framework contribution:** It contributes extraction discipline by separating raw source text from canonicalized statement blocks before ingestion.
- **Workflow shape:** Ensure target KB exists.; Parse report environments.; Normalize and write back.; Validate output.; Report ingest summary.
- **Scripts:** [parse_report.py](../../skills/ingest/pvsnp-kb-parser/scripts/parse_report.py)
- **Agent config:** [openai.yaml](../../skills/ingest/pvsnp-kb-parser/agents/openai.yaml)
- **References:** [mapping-rules.md](../../skills/ingest/pvsnp-kb-parser/references/mapping-rules.md), [script-usage.md](../../skills/ingest/pvsnp-kb-parser/references/script-usage.md)
- **Outputs:** Input report path.; Output JSON path.; Total parsed statements.; Counts by environment type.; KB file updated and number of canonical vs derived additions.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote malformed, uncited, ambiguous, or lossy intake to repair/evidence task instead of using it as reasoning evidence.

#### `target-literature-source-curator`

- **Skill file:** [Open skill](../../skills/ingest/target-literature-source-curator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Curate cited primary and expert sources for a target problem's historical and conceptual literature evolution. Use when a report needs to explain the major problem, where it came from, how the literature evolved, and which references justify each stage.
- **Conceptual role:** Use this skill to build a source-backed reference spine for a target problem. The goal is not a decorative bibliography. The source set must explain how the problem became well-posed, why it is hard, what the main route families are, and how the active Abducer run inherits obligations from the literature.
- **Agent config:** [openai.yaml](../../skills/ingest/target-literature-source-curator/agents/openai.yaml)
- **Outputs:** `Target`: target id, problem name, and official statement source.; `Reference Spine`: cited records with role, year, authors, title, venue, URL, supported claim, and limitation.; `Evolution Stages`: chronological stages, each tied to references and conceptual shift.; `Open Obligations`: what the literature leaves unresolved for the active workflow.; `Validation Handoff`: run `python agentic/scripts/build_target_literature_evolution.py` and `python agentic/scripts/validate_target_literature_evolution.py`.
- **Failure/demotion:** Demote the packet if references are uncited, if the story uses generic history instead of target obligations, if speculative solution claims are treated as established literature, or if source limitations are omitted.

#### `theorem-body-normalizer`

- **Skill file:** [Open skill](../../skills/ingest/theorem-body-normalizer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Normalize theorem-like statements into typed hypotheses, conclusion, quantifier regime, model assumptions, and assertion license. Use when discovery or proof work is drifting on topical labels rather than statement bodies.
- **Conceptual role:** This skill is the mandatory Phase 0 epistemic gate. It turns raw statements into theorem-body form before bridge planning, pathway ranking, or proof claims.
- **Workflow shape:** Extract the raw statement text.; Separate hypotheses, conclusion, quantifier regime, model assumptions, and thresholds.; State the claim type and assertion license.; Record overturn conditions and decisive progress conditions.
- **Agent config:** [openai.yaml](../../skills/ingest/theorem-body-normalizer/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/ingest/theorem-body-normalizer/references/prompt-template.md)
- **Outputs:** normalized theorem body; typed hypotheses; typed conclusion; quantifier and model regime; claim type and assertion license; overturn conditions
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote malformed, uncited, ambiguous, or lossy intake to repair/evidence task instead of using it as reasoning evidence.

### reasoning

Generative mathematical and physical reasoning skills: abduction, deduction, induction, contradiction, qualitative physics, and Gedanken design.

#### `efficient-representation-requirements-elicitor`

- **Skill file:** [Open skill](../../skills/reasoning/efficient-representation-requirements-elicitor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Declaratively elicit the requirements for an efficient mathematical representation of a proof gap. Use when a route needs to state which objects, invariants, operations, equivalence relations, locality/complexity constraints, transfer interfaces, and falsifiers a representation must support before new abstraction design or proof search continues.
- **Conceptual role:** Converts vague calls for better concepts into an explicit requirements packet: objects to encode, invariants to preserve, operations to support, allowed quotients, forbidden collapses, transfer interface, and demotion tests.
- **Agent config:** [openai.yaml](../../skills/reasoning/efficient-representation-requirements-elicitor/agents/openai.yaml)
- **Outputs:** `representation_goal`; `target_pressure`; `objects_to_encode`; `primitive_operations`; `preserved_invariants`; `forbidden_collapses`; `equivalence_policy`; `efficiency_requirements`; `transfer_interface`; `acceptance_criteria`; `epistemic_status`; `evidence`; `validation_handoff`.
- **Failure/demotion:** Demote packets that omit invariants, edge cases, counterexamples, or source/target semantic separation. Quarantine requirements that make the theorem true by definition.

#### `gedanken-counterfactual-variant-builder`

- **Skill file:** [Open skill](../../skills/reasoning/gedanken-counterfactual-variant-builder/SKILL.md)
- **Mode:** Generative agent
- **Description:** Generate counterfactual variants of a Gedanken experiment to test which variable, assumption, regime, or mechanism is actually responsible for the expected observation. Use when a thought experiment needs sharper contrasts before it can guide a follow-up cycle.
- **Conceptual role:** Use this skill after a candidate situation exists. The goal is to prevent one-story explanations by changing one condition at a time and predicting how the observation should change. Variants reveal whether the claimed insight depends on a phase, cutoff, boundary condition, hidden variable, observable sector, limit order, or transfer assumption.
- **Workflow shape:** Identify the baseline situation and its expected observation.; Select one condition to change: variable value, held-fixed assumption, regime, symmetry, boundary, observable, or limit order.; Predict the changed observation and the reason.; Say whether the variant sharpens, disconfirms, or quarantines the baseline situation.; Add the variant to the Gedanken packet and any qualitative graph edge it challenges.
- **Agent config:** [openai.yaml](../../skills/reasoning/gedanken-counterfactual-variant-builder/agents/openai.yaml)
- **Outputs:** `Baseline`: packet or situation being varied.; `Changed Condition`: exactly one change and why it matters.; `Held Fixed`: what remains unchanged.; `Predicted Change`: expected observation shift.; `Diagnostic Value`: what this teaches about mechanism or transfer.; `Demotion Trigger`: what result would challenge the baseline.; `Graph Consequence`: whether the variant should `challenge_edge`, `revise_edge`, `annotate_edge`, `needs_probe`, or `quarantine`.; `Validation Handoff`: updated packet and validator command.
- **Validation handoff:** Run `python agentic/scripts/validate_gedanken_experiment_packets.py` after adding variants. If a variant suggests a concrete calculation, hand it to `qualitative-toy-model-builder` or the ranked next-experiment queue.
- **Failure/demotion:** Demote variants that alter the target problem, change too many assumptions, have no predicted observational difference, or only make the story more vivid. Falsify a baseline if the decisive observation persists after the purported mechanism is removed.

#### `gedanken-situation-designer`

- **Skill file:** [Open skill](../../skills/reasoning/gedanken-situation-designer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Design concrete imagined situations that isolate variables, mechanisms, regimes, and expected observations for follow-up discovery cycles. Use when Abducer needs a high-information Gedanken experiment rather than another generic hypothesis or deterministic placeholder.
- **Conceptual role:** Use this skill to design an imagined but mathematically concrete situation. The situation should feel like a small laboratory for the concept: enough structure to force an observation, but not so much structure that it quietly changes the target problem.
- **Workflow shape:** Name the conceptual pressure: hidden variable, ambiguous mechanism, limit-order issue, transfer risk, or competing explanation.; Choose the minimal mathematical carrier that can make the pressure visible.; State what is varied and what is held fixed.; Predict an observation pattern and what would disconfirm it.; Add at least one counterfactual variant that changes one condition.; State what transfers, what does not transfer, and what certificate is needed.; Name originating cycle IDs, branch IDs, affected graph nodes or edges, and the intended `graph_update_action`.; Emit a packet compatible with `agentic/spec/gedanken_experiment_packet.schema.json`.
- **Agent config:** [openai.yaml](../../skills/reasoning/gedanken-situation-designer/agents/openai.yaml)
- **Outputs:** `Situation`: title, purpose, minimal world, mathematical carrier, controlled contrast, informativeness rationale, and non-claims.; `Variables And Controls`: variables, roles, held-fixed assumptions, and validity regimes.; `Interventions`: operations, varied variables, predicted direction, and decision value.; `Expected Observations`: observable patterns, what they teach, and what disconfirms them.; `Variants`: counterfactual changes and predicted shifts.; `Transfer Scope`: `transfer_verdict`, transfers, does not transfer, certificate needed.; `Graph Linkage`: `affected_node_ids`, `affected_edge_ids`, `graph_update_action`, and `proposed_graph_updates`.; `Follow-Up Tasks`: derive, compute, falsify, formalize, update graph, rank next experiment, backtrack, or quarantine.
- **Validation handoff:** Write or inspect `agentic/reports/gedanken_experiments/latest.json`, then run `python agentic/scripts/validate_gedanken_experiment_packets.py`. Pass accepted follow-up tasks to `gedanken-followup-planner`.
- **Failure/demotion:** Demote if the design is just an analogy, if variables are not controlled, if the expected observation cannot affect a later cycle, or if the situation cannot be connected to the active target. Quarantine if the carrier solves a different problem. Falsify the design if the proposed variant does not change anything relevant.

#### `kb-abduce`

- **Skill file:** [Open skill](../../skills/reasoning/kb-abduce/SKILL.md)
- **Mode:** Generative agent
- **Description:** Generate and rank explanatory hypotheses for observations or target claims that are not fully derivable from the current KB. Use when the user asks for plausible missing premises, best explanations, repair hypotheses, or assumption discovery over `KB/*.kb.md`.
- **Conceptual role:** This skill operationalizes abductive reasoning over a single KB by proposing minimal missing premises that would make a target statement or bridge mathematically viable.
- **Framework contribution:** It contributes the hypothesis-generation step that turns structural gaps into explicit, testable assumptions for the next deductive or coherence pass.
- **Workflow shape:** Define abduction target.; Compute failure boundary.; Propose hypothesis sets.; Rank hypotheses.; Emit falsification tests.; Optional KB update.
- **Agent config:** [openai.yaml](../../skills/reasoning/kb-abduce/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/reasoning/kb-abduce/references/prompt-template.md)
- **Outputs:** `Target`; `Deduction Failure Boundary`; `Hypothesis Sets`; `Ranking Rationale`; `Falsification Tests`; `Recommended Next Step`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on circular support, missing premise, invalid entailment, over-generalized induction, counterexample, or uncited evidence.

#### `kb-contradiction-strategist`

- **Skill file:** [Open skill](../../skills/reasoning/kb-contradiction-strategist/SKILL.md)
- **Mode:** Generative agent
- **Description:** Build disciplined proof-by-contradiction routes for KB targets. Use when direct construction stalls, when a negated target may expose a spectral, compactness, density, positivity, nontriviality, or same-theory conflict, or when the discovery loop needs a reductio branch with explicit mathematical obligations.
- **Conceptual role:** This skill turns proof by contradiction from a vague tactic into a controlled discovery route. It assumes the exact negation of a target, preserves the ambient mathematical commitments, and searches for a contradiction that is visible as a theorem-shaped conflict rather than a narrative discomfort.
- **Workflow shape:** State the target and exact negation.; Preserve the commitments.; Choose a contradiction carrier.; Generate the impossible consequence.; Expose the proof obligations.; Route the branch.
- **Agent config:** [openai.yaml](../../skills/reasoning/kb-contradiction-strategist/agents/openai.yaml)
- **References:** [contradiction-route-template.md](../../skills/reasoning/kb-contradiction-strategist/references/contradiction-route-template.md)
- **Outputs:** `target_claim`: the target statement and source evidence.; `exact_negation`: the formal negated assumption, including quantifiers.; `preserved_commitments`: definitions, KB IDs, artifacts, and invariants that; `contradiction_carrier`: the object expected to carry the contradiction.; `derived_consequence`: the consequence generated from the negated assumption.; `conflict_target`: the theorem, axiom, KB claim, validator-backed artifact,; `proof_obligations`: lemmas needed to make the contradiction valid.; `failure_modes`: ways the route could fail or be demoted.
- **Validation handoff:** Hand off each route to `contradiction-route-auditor` before proof-queue promotion. If the route is Yang-Mills-specific, also attach it to the active bridge-lemma packet or long-horizon target report so the next recursive loop can decide whether to pursue, repair, pivot, or backtrack.
- **Failure/demotion:** Demote on non-exact negation, object mismatch, hidden premise shift, broken same-theory invariant, conflict against an unaccepted target, unsupported limit exchange, vacuous contradiction, or absence of a falsifiable next obligation.

#### `kb-deduce`

- **Skill file:** [Open skill](../../skills/reasoning/kb-deduce/SKILL.md)
- **Mode:** Generative agent
- **Description:** Derive logically implied consequences from statements in a mathematical KB file. Use when the user asks what follows from current definitions/axioms/theorems, requests forward or backward chaining, or wants candidate corollaries with explicit dependency traces in `KB/*.kb.md`.
- **Conceptual role:** This skill operationalizes deductive reasoning over the informal KB by asking what consequences follow once a selected set of premises or hypotheses is provisionally accepted.
- **Framework contribution:** It contributes consequence-tracing and pruning: bridges or hypotheses that yield no useful entailment can be deprioritized in later loops.
- **Workflow shape:** Fix the reasoning scope.; Build the rule pool.; Run constrained chaining.; Classify output.; `entailed`: derivable with available premises.; `conditionally-entailed`: derivable if listed missing premises are added.; `not-derived`: cannot be proven from current KB.; Write back derived results when asked.
- **Agent config:** [openai.yaml](../../skills/reasoning/kb-deduce/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/reasoning/kb-deduce/references/prompt-template.md)
- **Outputs:** Return a table with columns:
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on circular support, missing premise, invalid entailment, over-generalized induction, counterexample, or uncited evidence.

#### `kb-explain`

- **Skill file:** [Open skill](../../skills/reasoning/kb-explain/SKILL.md)
- **Mode:** Generative agent
- **Description:** Explain mathematical statements from a KB file in layered natural language while staying grounded in statement IDs and dependencies. Use when the user asks for intuition, restatement, concept linking, or stepwise explanation of definitions, axioms, theorems, or proof sketches stored in `KB/*.kb.md`.
- **Conceptual role:** This skill translates structured KB artifacts into human-readable mathematical explanations for users inspecting concepts, dependencies, and proof attempts.
- **Framework contribution:** It contributes interpretability by turning internal graph and hypothesis structures into explicit mathematical narratives.
- **Workflow shape:** Select the target statement IDs.; Build a dependency slice.; Produce three layers.; Plain-language intuition.; Semi-formal reasoning chain.; LaTeX-level restatement tied to IDs.; Cite every nontrivial claim.; Declare uncertainty.
- **Agent config:** [openai.yaml](../../skills/reasoning/kb-explain/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/reasoning/kb-explain/references/prompt-template.md)
- **Outputs:** `Summary`; `Dependency Path`; `Detailed Explanation`; `Missing Support`; `Referenced IDs`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on circular support, missing premise, invalid entailment, over-generalized induction, counterexample, or uncited evidence.

#### `kb-induce`

- **Skill file:** [Open skill](../../skills/reasoning/kb-induce/SKILL.md)
- **Mode:** Generative agent
- **Description:** Generalize successful bridge, strategy, lemma, or proof-sketch patterns into reusable theorem schemas. Use when the user asks to abstract a proof route, infer a reusable bridge template, or consolidate repeated strategy-level structures over `KB/*.kb.md`.
- **Conceptual role:** This skill performs scoped induction over existing bridge, strategy, and proof artifacts to recover reusable higher-level patterns.
- **Framework contribution:** It contributes late-stage abstraction by generalizing already-isolated proof motifs rather than mining the raw KB for loose similarities.
- **Workflow shape:** Select induction corpus.; Extract structural features.; Cluster patterns.; Propose generalizations.; Stress test each conjecture.; Optional KB update.
- **Agent config:** [openai.yaml](../../skills/reasoning/kb-induce/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/reasoning/kb-induce/references/prompt-template.md)
- **Outputs:** `Pattern Clusters`; `Candidate Generalizations`; `Support and Counterexample Risk`; `Validation Plan`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on circular support, missing premise, invalid entailment, over-generalized induction, counterexample, or uncited evidence.

#### `monotonicity-sensitivity-prober`

- **Skill file:** [Open skill](../../skills/reasoning/monotonicity-sensitivity-prober/SKILL.md)
- **Mode:** Generative agent
- **Description:** Analyze how one physics quantity changes when another is varied, including increasing, decreasing, saturating, diverging, converging, sign-changing, threshold, nonmonotone, or ambiguous behavior. Use when Abducer needs directional qualitative understanding with explicit held-fixed variables and valid regimes.
- **Conceptual role:** Use this skill to infer the directional behavior of one quantity under a controlled variation. It should answer "if this variable changes, what changes, in what direction, at what rate class, under what assumptions, and where can that statement fail?"
- **Workflow shape:** Select one varied variable, one response variable, and the held-fixed conditions.; State the candidate relation as `response` versus `driver` within a named regime.; Reason through the sign or direction using equations, scaling, variational principles, conservation, convexity, positivity, spectral representation, or a toy calculation.; Classify the behavior: increasing, decreasing, saturating, divergent, convergent, thresholded, sign-changing, nonmonotone, hysteretic, or unknown.; Estimate the rate class when meaningful: linear, sublinear, polynomial, logarithmic, exponential, stretched exponential, bounded, or singular.; Identify sensitivity amplifiers and dampers: hidden couplings, near-criticality, small denominators, degeneracy, normalization, or cutoff effects.; Name disconfirming observations and hand unresolved claims to a concrete probe, falsifier, or graph update.
- **Agent config:** [openai.yaml](../../skills/reasoning/monotonicity-sensitivity-prober/agents/openai.yaml)
- **Outputs:** `Controlled Variation`: driver, response, held-fixed controls, and validity regime.; `Direction Claim`: sign, monotonicity class, rate class, and reasoning.; `Sensitivity Mechanism`: why the response changes, including amplifiers or dampers.; `Failure Modes`: threshold, saturation, sign reversal, nonmonotonicity, hidden coupling, or boundary-regime failure.; `Disconfirming Observation`: what would falsify or demote the relation.; `Graph Edge`: source node, target node, relation type, regime, epistemic status, and evidence.; `Validation Handoff`: relation packet, toy model, falsifier, graph validator, or next experiment.
- **Validation handoff:** Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after producing graph-ready sensitivity edges.
- **Failure/demotion:** Demote when no held-fixed controls are named, the response variable is not typed, the direction is unsupported, or the relation is asserted globally from local reasoning. Quarantine sensitivity claims that depend on analogy-only transfer.

#### `physics-regime-map-builder`

- **Skill file:** [Open skill](../../skills/reasoning/physics-regime-map-builder/SKILL.md)
- **Mode:** Generative agent
- **Description:** Map physical regimes, scale ranges, cutoff and volume status, boundary conditions, perturbative status, and order-of-limit assumptions for qualitative physics relations. Use when a relation might change behavior across UV/IR, finite/continuum, weak/strong, linear/nonlinear, or long-time regimes.
- **Conceptual role:** Use this skill when a relation may be true in one regime and false, meaningless, or unlicensed in another. Its purpose is to carve the problem into validity regions before the loop spends proof budget on a qualitative claim.
- **Workflow shape:** Start from the typed variable frame or infer one if absent.; Identify regime axes: cutoff, volume, coupling, scale separation, time, temperature, dimension, observable sector, boundary condition, linearity, perturbative status, and limiting order.; Partition the space into validity regions and name the transition surfaces or unknown boundaries.; For each region, state which equations, estimates, monotonicity claims, symmetries, and observables are valid.; Identify regime crossings where qualitative behavior can change sign, saturate, diverge, become nonuniform, or lose transfer.; Emit graph annotations that attach relation edges to validity regimes rather than global claims.; Hand fragile regime crossings to `limit-convergence-behavior-auditor`, `scale-asymptotic-reasoner`, or `qualitative-physics-falsifier`.
- **Agent config:** [openai.yaml](../../skills/reasoning/physics-regime-map-builder/agents/openai.yaml)
- **Outputs:** `Regime Axes`: each axis, possible values, mathematical meaning, and why it matters.; `Regime Cells`: valid, invalid, unknown, and transition regimes.; `Local Relations`: which qualitative claims hold only in which cells.; `Cross-Regime Risks`: nonuniformity, noncommuting limits, phase transitions, proxy drift, or boundary-condition dependence.; `Graph Updates`: regime-qualified nodes, edges, and relation statuses.; `Failure Modes`: edge cases and counterexample regimes.; `Validation Handoff`: next skill, relation packet, graph validator, or queue item.
- **Validation handoff:** Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after regime-qualified relation updates.
- **Failure/demotion:** Demote when a map has no axes, no transition conditions, no invalid regimes, or no order-of-limit statement. Quarantine global claims that are supported only in a local regime.

#### `pvsnp-gedanken-complexity-lab`

- **Skill file:** [Open skill](../../skills/reasoning/pvsnp-gedanken-complexity-lab/SKILL.md)
- **Mode:** Generative thought-experiment design + deterministic packet builder
- **Description:** Design concrete P vs NP Gedanken experiments and extract essential conclusions. Use when a P vs NP branch, bridge candidate, pressure report, or marathon cycle needs a small complexity-theoretic situation that elicits intuition about oracle substitution, beta/exponent windows, MCSP/MKtP certificates, proof-complexity carriers, natural-proof pressure, advice leakage, padding/projection debt, all-exponent quantifiers, or no-go boundaries.
- **Conceptual role:** Build small controlled complexity-theory worlds that expose a hidden mechanism, then extract decisive intuition, formal lesson, route-control consequence, and next action without treating the thought experiment as proof evidence.
- **Workflow shape:** Start from a live pressure or bridge.; Choose a minimal carrier such as SAT-oracle substitution, searchable certificates, sparse property toggles, all-exponent families, or proof-system lower-bound tautologies.; Isolate variables and held-fixed conditions.; Specify controlled contrast and diagnostic variant.; Predict observations and disconfirmers.; Extract essential conclusions.; Emit a Gedanken packet with transfer scope and follow-up tasks.
- **Scripts:** [build_pvsnp_gedanken_packets.py](../../skills/reasoning/pvsnp-gedanken-complexity-lab/scripts/build_pvsnp_gedanken_packets.py)
- **Agent config:** [openai.yaml](../../skills/reasoning/pvsnp-gedanken-complexity-lab/agents/openai.yaml)
- **Outputs:** Pressure or bridge source; concrete situation; variables and controls; expected observation; variant; essential conclusions; transfer scope; follow-up tasks.
- **Validation handoff:** Validate with `agentic/scripts/validate_pvsnp_gedanken_conclusions.py` and `agentic/scripts/validate_gedanken_experiment_packets.py`.
- **Failure/demotion:** Demote analogy-only cases, cases without branch-specific variables, missing conclusions, missing variants, or premature transfer to theorem progress.

#### `pvsnp-impossibility-theorem-forger`

- **Skill file:** [Open skill](../../skills/reasoning/pvsnp-impossibility-theorem-forger/SKILL.md)
- **Mode:** Generative agent
- **Description:** Forge proof-by-contradiction and impossibility/no-go theorem candidates for P vs NP strategy branches. Use when black-box substitution, padding/projection, natural-proof, relativization, algebrization, advice-leakage, or meta-complexity routes may be more valuable as obstruction theorems than as direct proof attempts.
- **Conceptual role:** Turn failed or suspicious route families into precise contradiction routes or no-go theorem statements with assumptions, conclusion, proof skeleton, escape conditions, and non-claim boundary.
- **Workflow shape:** State the route family.; Choose contradiction, impossibility theorem, obstruction lemma, or barrier audit.; Formalize assumptions and quantifiers.; Derive the obstruction.; State theorem-shaped result and escape conditions.; Send the candidate to contradiction audit before promotion.
- **Agent config:** [openai.yaml](../../skills/reasoning/pvsnp-impossibility-theorem-forger/agents/openai.yaml)
- **Outputs:** Route family; logic form; formal statement; proof skeleton; escape conditions; proof obligations; disposition; validation handoff.
- **Validation handoff:** Hand candidates to `contradiction-route-auditor`, then to `paper-contribution-readiness-judge` if contribution-shaped.
- **Failure/demotion:** Demote rhetorical impossibility claims, overbroad no-go statements, missing quantifiers, unaccepted conflict targets, or barrier restatements without route-specific obstruction.

#### `pvsnp-pressure-bridge-forger`

- **Skill file:** [Open skill](../../skills/reasoning/pvsnp-pressure-bridge-forger/SKILL.md)
- **Mode:** Generative abstraction design + deterministic pressure-signal scouting
- **Description:** Forge target-preserving bridge abstractions from P vs NP conceptual pressures and difficulty hypotheses. Use when pressure localization has named bottlenecks such as hardness magnification ceilings, black-box substitution caps, MCSP/MKtP carrier debt, proof-complexity transfer, natural-proof pressure, relativization/algebrization barriers, advice leakage, padding/projection debt, or bounded-exponent windows.
- **Conceptual role:** Convert "why this is hard" into "which bridge abstraction could carry the difficulty without changing the theorem", with source object, target object, controlled interface, proof obligation, falsifier, persist/pivot criteria, and paper-safe narrative.
- **Workflow shape:** Read the pressure packet.; State the difficulty hypothesis in P vs NP objects.; Forge bridge abstractions such as subpolynomial nonblackbox interfaces, searchable meta-complexity certificates, proof-complexity certificates, sparse non-natural properties, all-exponent quantifier lifts, or route-specific impossibility bridges.; Type the interface and invariants.; Attach proof obligations and falsifiers.; Route the result to symbolic, qualitative, no-go, contradiction, queue, or contribution skills.
- **Scripts:** [build_pressure_bridges.py](../../skills/reasoning/pvsnp-pressure-bridge-forger/scripts/build_pressure_bridges.py)
- **Agent config:** [openai.yaml](../../skills/reasoning/pvsnp-pressure-bridge-forger/agents/openai.yaml)
- **Outputs:** Pressure source; difficulty hypothesis; bridge abstraction; proof obligation; falsifiers and stop conditions; validation handoff; paper-safe narrative.
- **Validation handoff:** Validate generated bridge artifacts with `agentic/scripts/validate_pvsnp_pressure_bridges.py`.
- **Failure/demotion:** Demote bridge candidates that only restate known barriers, cannot name source and target objects, hide quantifiers, lack falsifiers, or keep a branch alive without a typed bridge obligation.

#### `pvsnp-qualitative-complexity-reasoner`

- **Skill file:** [Open skill](../../skills/reasoning/pvsnp-qualitative-complexity-reasoner/SKILL.md)
- **Mode:** Generative agent
- **Description:** Build qualitative complexity-theoretic relation maps for P vs NP routes. Use when a branch needs to isolate variables, monotonicities, exponent transfers, threshold behavior, density/naturalness conditions, verifier overhead, advice leakage, padding/projection growth, or meta-complexity carrier behavior.
- **Conceptual role:** Give the loop a qualitative sense of how complexity quantities move together: which variables are independent, which are derived, where thresholds occur, and which regime change invalidates the target claim.
- **Workflow shape:** Identify carrier and observable.; Build variable frame.; Separate independent knobs from derived responses.; Derive directional relations.; Map regimes and noncommuting limits.; Emit graph-ready relations.
- **Agent config:** [openai.yaml](../../skills/reasoning/pvsnp-qualitative-complexity-reasoner/agents/openai.yaml)
- **Outputs:** Carrier and target; variable frame; qualitative relations; transfer formula sketch; mechanistic graph update; falsifiers; validation handoff.
- **Validation handoff:** Hand no-go candidates to `pvsnp-impossibility-theorem-forger`, pressure gaps to `pvsnp-conceptual-pressure-localizer`, and graph/report updates to the marathon validators.
- **Failure/demotion:** Demote relation packets that confuse `n` and `N`, omit held-fixed conditions, suppress uniform/nonuniform status, or replace the target separation with a proxy.

#### `pvsnp-symbolic-complexity-auditor`

- **Skill file:** [Open skill](../../skills/reasoning/pvsnp-symbolic-complexity-auditor/SKILL.md)
- **Mode:** Generative interpretation + exact symbolic/CAS-backed probe
- **Description:** Perform exact symbolic and CAS-assisted audits for P vs NP discovery routes. Use when a branch needs exponent-transfer algebra, padding/projection bookkeeping, finite truth-table or circuit-count sanity checks, natural-proof largeness/constructivity tests, advice/uniformity accounting, oracle/barrier signature ledgers, or bounded symbolic probes.
- **Conceptual role:** Make route claims exact enough to decide whether a branch has a target-preserving transfer, a bounded no-go theorem, or a hidden model switch.
- **Workflow shape:** Select symbolic carrier.; State variables and quantifiers.; Choose exact rational, SymPy, finite enumeration, or barrier-ledger mode.; Run bounded computation only after typing the claim.; Interpret the result generatively.; Hand off to qualitative, impossibility, conceptual-pressure, or queue-ranking skills.
- **Scripts:** [audit_transfer.py](../../skills/reasoning/pvsnp-symbolic-complexity-auditor/scripts/audit_transfer.py)
- **Agent config:** [openai.yaml](../../skills/reasoning/pvsnp-symbolic-complexity-auditor/agents/openai.yaml)
- **Outputs:** Symbolic carrier; variable ledger; transfer formula; CAS or exact probe; conceptual interpretation; barrier and model ledger; disposition; validation handoff.
- **Validation handoff:** Hand parameter relations to `pvsnp-qualitative-complexity-reasoner`, no-go statements to `pvsnp-impossibility-theorem-forger`, pressure explanations to `pvsnp-conceptual-pressure-localizer`, and queue decisions to `next-experiment-queue-ranker`.
- **Failure/demotion:** Demote calculations that hide quantifiers, conflate fixed-exponent and all-polynomial claims, suppress advice/uniformity status, or present CAS output as proof without a theorem statement.

#### `qualitative-toy-model-builder`

- **Skill file:** [Open skill](../../skills/reasoning/qualitative-toy-model-builder/SKILL.md)
- **Mode:** Generative agent
- **Description:** Choose and solve small concrete models that calibrate qualitative physics intuition, such as finite matrices, spectral measures, heat kernels, simple RG maps, noncommuting limits, or finite-volume probes. Use when a qualitative relation is underdetermined and needs a bounded concrete setting.
- **Conceptual role:** Use this skill when conceptual reasoning is underdetermined and a small solved setting can reveal a sign, scaling class, failure mode, or transfer boundary. The toy model is a microscope, not a substitute target.
- **Workflow shape:** State the unresolved qualitative question and the target mechanism it is meant to probe.; Choose a minimal mathematical carrier: finite matrix, two-state system, spectral measure, scalar kernel, small graph, recurrence, ODE, RG map, constrained optimization problem, or finite-volume lattice sketch.; Name variables, controls, observables, and the regime the toy model represents.; Solve analytically when possible; otherwise run a small bounded computation and inspect the result.; Compare baseline and at least one variant that removes or reverses the proposed mechanism.; Extract only qualitative lessons: direction, threshold, saturation, asymptotic class, obstruction, or falsifier.; State the transfer certificate required before the lesson can affect proof obligations or graph edges.
- **Agent config:** [openai.yaml](../../skills/reasoning/qualitative-toy-model-builder/agents/openai.yaml)
- **Outputs:** `Probe Question`: the qualitative ambiguity and target mechanism.; `Toy Carrier`: chosen model, variables, observables, controls, and why it is minimal.; `Solution Or Execution`: derivation or executed command plus inspected artifact.; `Baseline And Variant`: what changes and what remains fixed.; `Qualitative Lesson`: direction, threshold, asymptotic class, obstruction, or falsifier.; `Transfer Boundary`: what transfers, what does not, and certificate needed.; `Graph/Queue Handoff`: relation update, falsifier, next experiment, or quarantine.
- **Validation handoff:** Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after converting a toy lesson into a relation packet or graph update.
- **Failure/demotion:** Demote when the toy model is decorative, unsolved, changes the target mechanism, lacks a variant, or claims proof progress. Quarantine if the result is analogy-only.

#### `qualitative-variable-isolator`

- **Skill file:** [Open skill](../../skills/reasoning/qualitative-variable-isolator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Extract typed variables, controls, observables, hidden scales, dependent quantities, constraints, and unresolved unknowns before qualitative physics relation claims. Use when a physics or mathematical-physics branch needs to know what can vary independently, what is held fixed, and what is only a derived response.
- **Conceptual role:** Use this skill before any qualitative relation is asserted. Its job is to turn a vague phrase such as "the gap depends on the scale" into a typed variable frame: independent knobs, dependent responses, hidden couplings, observables, constraints, regimes, and held-fixed assumptions.
- **Workflow shape:** Name the mathematical object and the observable being discussed.; Build a variable table with `symbol`, `meaning`, `role`, `units_or_scaling`, `allowed_range`, `held_fixed_when`, and `depends_on`.; Separate independent variables from response variables, constraints, gauge choices, cutoff parameters, limiting parameters, and purely descriptive labels.; Identify hidden couplings: a variable that appears independent but changes another quantity through a definition, conservation law, normalization, boundary condition, or order of limits.; State which variables are safe to vary one at a time and which require a regime map before variation.; Emit graph-ready node candidates and relation stubs only after roles are typed.; Recommend the next qualitative skill: `physics-regime-map-builder`, `monotonicity-sensitivity-prober`, `limit-convergence-behavior-auditor`, or `qualitative-toy-model-builder`.
- **Agent config:** [openai.yaml](../../skills/reasoning/qualitative-variable-isolator/agents/openai.yaml)
- **Outputs:** `Object And Observable`: carrier, target quantity, branch obligation, and source artifact.; `Variable Frame`: independent variables, dependent responses, hidden couplings, controls, constraints, and unknowns.; `Held-Fixed Conditions`: what must remain unchanged for each proposed variation.; `Safe Variations`: one-variable moves that are meaningful, plus constrained variations that require a path.; `Graph Seeds`: graph-ready node IDs, possible edge directions, and why they remain stubs.; `Failure Modes`: proxy drift, hidden dependence, dimension mismatch, untyped regime, or noncommuting-limit risk.; `Validation Handoff`: packet, graph, validator, or next qualitative skill.
- **Validation handoff:** Use `python agentic/scripts/validate_qualitative_relation_packets.py` after relation packets exist, then `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>` and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after graph updates.
- **Failure/demotion:** Demote when the output lists nouns without roles, omits held-fixed assumptions, treats all quantities as independently variable, or fails to name a mathematical object. Quarantine graph seeds when a proxy observable replaces the target object.

#### `scale-asymptotic-reasoner`

- **Skill file:** [Open skill](../../skills/reasoning/scale-asymptotic-reasoner/SKILL.md)
- **Mode:** Generative agent
- **Description:** Infer qualitative scale behavior, dominant balance, asymptotic class, transition scales, and breakdown conditions. Use when a physics branch needs to compare linear, polynomial, logarithmic, exponential, stretched-exponential, threshold, saturation, or RG-style scale behavior.
- **Conceptual role:** Use this skill when the key question is how a quantity behaves as a scale changes or tends to a limit. It should identify dominant balances, crossover scales, asymptotic classes, and failure regimes rather than simply saying "large" or "small".
- **Workflow shape:** Identify the scale variable, response quantity, regime, and limiting direction.; List candidate asymptotic forms: constant, linear, polynomial, logarithmic, exponential, stretched exponential, power law with corrections, threshold, saturation, or divergent.; Derive or motivate dominant balance using dimensions, equations, spectral representations, RG flow, estimates, comparison principles, or a toy model.; Identify crossover scales and the parameter combinations that control them.; State what is uniform in the asymptotic statement and what is only pointwise or finite-regime.; Compare at least two asymptotic alternatives and name an observation that discriminates them.; Emit graph edges only as regime-qualified asymptotic relations.
- **Agent config:** [openai.yaml](../../skills/reasoning/scale-asymptotic-reasoner/agents/openai.yaml)
- **Outputs:** `Scale Setup`: scale variable, response quantity, limiting direction, and held-fixed controls.; `Candidate Asymptotics`: plausible forms and why each is possible or excluded.; `Dominant Balance`: controlling terms, mechanisms, and crossover scales.; `Uniformity Statement`: pointwise, uniform, fixed-regime, continuum, infinite-volume, or unknown.; `Discriminating Probe`: observation, calculation, or estimate that separates alternatives.; `Failure Modes`: pre-asymptotic trap, nonuniformity, hidden scale, phase transition, or proxy drift.; `Validation Handoff`: relation packet, limit auditor, toy model, graph validator, or next experiment.
- **Validation handoff:** Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` for graph-ready asymptotic claims.
- **Failure/demotion:** Demote when no scale variable is isolated, the asymptotic class is guessed without a mechanism, uniformity is missing, or finite-scale behavior is promoted to a limiting claim. Quarantine analogy-only scaling stories.

### discovery

KB graph navigation, bridge discovery, entrypoint selection, proof strategy formation, and discovery-cycle queue construction.

#### `abducer-mediation-candidate-generator`

- **Skill file:** [Open skill](../../skills/discovery/abducer-mediation-candidate-generator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Generate grounded Abducer mediation candidates and creative hypothesis transformations from pressure packets. Use when the workflow needs bridge invention, abstraction formation, regime restriction, theorem weakening or strengthening, carrier introduction, negative-route inversion, analogy transport, proof-obligation factorization, or representation shift candidates.
- **Conceptual role:** Generate creative but controlled transformations over the hypothesis exploration space. A candidate is useful only when it changes route options and creates validation obligations.
- **Workflow shape:** Read pressure packets and classification artifacts.; Generate multiple candidate classes when the pressure supports them.; Cite source pressure IDs, affected dependency nodes, KB IDs, and artifact paths.; State the proposed transformation, expected route value, and disconfirming observations.; List validation requirements before recommending a disposition.
- **Agent config:** [openai.yaml](../../skills/discovery/abducer-mediation-candidate-generator/agents/openai.yaml)
- **Outputs:** Emit `abducer_mediation_candidate` and `conceptual_creativity_analysis` objects. Run `agentic/scripts/build_hypothesis_exploration_map.py` for deterministic seeds and `agentic/scripts/validate_hypothesis_exploration.py` before promotion.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-coherence-evaluator`

- **Skill file:** [Open skill](../../skills/discovery/kb-coherence-evaluator/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Build a typed coherence graph over statements, concepts, and hypotheses, then compute global coherence and local explanatory-power/coherence-delta signals per hypothesis. Use when the user asks for coherentist assessment, global theory consistency checks, explanatory power scoring, or belief-revision guidance over `KB/*.kb.md` and `phyp/*.yaml`.
- **Conceptual role:** This skill implements the coherentist layer of the framework by scoring how well candidate hypotheses fit into the global web of claims, supports, tensions, and explanations.
- **Framework contribution:** It contributes theory-level selection pressure so the workflow does not optimize only local bridge quality or isolated statement similarity.
- **Workflow shape:** Parse KB statements and dependency structure.; Ingest connector analysis and phyp hypotheses.; Build typed nodes and edges across statements, hypotheses, concepts, methods, and barriers.; Compute global coherence profile.; Compute per-hypothesis:; `explanatory_power_local`; `coherence_delta_global`; Emit revision guidance for low-coherence hypotheses.
- **Scripts:** [evaluate_coherence.py](../../skills/discovery/kb-coherence-evaluator/scripts/evaluate_coherence.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-coherence-evaluator/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/discovery/kb-coherence-evaluator/references/prompt-template.md), [script-usage.md](../../skills/discovery/kb-coherence-evaluator/references/script-usage.md)
- **Outputs:** `typed_coherence_graph`; `coherence_profile`; `hypothesis_coherence`; `belief_revision_recommendations`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-concept-bridge-planner`

- **Skill file:** [Open skill](../../skills/discovery/kb-concept-bridge-planner/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Given intermediate KB artifacts, systematically identify and rank how to bridge essential concepts across phases. Use when the user asks how to connect key concepts/results, design bridge programs, or prioritize cross-concept linkage tests.
- **Conceptual role:** This skill turns ranked statements and connector evidence into explicit bridge programs that specify where a proof route should try to pass through the KB.
- **Framework contribution:** It contributes a bridge-level research agenda by converting abstract connectivity into typed bridge families, commitments, and intervention sequences.
- **Workflow shape:** Ingest intermediate results (`analysis`, `entrypoints`, `pathways`, `phyp`, `concept`).; Score bridge candidates and classify bridge types.; For the top bridges, state both the missing bridge object/transport law and the main positive vs negative proof-space opportunities.; If the bridge object is still schematic, convert the gap into a declarative search profile and search for bridge objects beyond the immediate area.; Group bridges by conceptual axes (phase -> phase).; Emit prioritized run order with validation protocol.
- **Scripts:** [plan_bridges.py](../../skills/discovery/kb-concept-bridge-planner/scripts/plan_bridges.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-concept-bridge-planner/agents/openai.yaml)
- **References:** [bridge-criteria.md](../../skills/discovery/kb-concept-bridge-planner/references/bridge-criteria.md), [non-immediate-bridge-search.md](../../skills/discovery/kb-concept-bridge-planner/references/non-immediate-bridge-search.md), [prompt-template.md](../../skills/discovery/kb-concept-bridge-planner/references/prompt-template.md), [script-usage.md](../../skills/discovery/kb-concept-bridge-planner/references/script-usage.md)
- **Outputs:** `Stats`; `Top Bridge Programs`; `Bridge Axes`; `Recommended Run Order`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-discovery-cycle`

- **Skill file:** [Open skill](../../skills/discovery/kb-discovery-cycle/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Run the discovery cycle that turns completed reasoning artifacts into a persistent proof queue of concrete prove-or-disprove targets. Use when the user wants to queue the next informal proof tasks, prioritize discovery outputs into a file-backed queue, or prepare theorem-pair-specific claims for later proof work.
- **Conceptual role:** This skill converts the output of discovery-stage artifacts into a persistent queue of concrete proof targets. Each queued item should read as a self-contained conjecture, with the route lemma recorded as the specific step to test.
- **Use when:** `expert-hypothesis-paper.json`; `search-space-tree.json`; create or refresh a queue of proof targets;; turn promising directions into explicit prove-or-disprove tasks;; avoid rediscovering the same next-step proof agenda repeatedly.
- **Workflow shape:** Read the final bridge-first artifacts.; Keep only theorem-pair-specific targets with a clear claim under test.; State each queued item as a self-contained conjecture rather than an internal route fragment.; If the bridge object is still only a placeholder, escalate back to non-immediate bridge search before promoting the route.; Preserve the missing route lemma and supporting obligations as proof context beneath the conjecture.; Materialize the queue in `artifacts/<kb-ref>/proof-queue.json` and `proof-queue.md`.; Preserve prior queue state so completed or blocked items are not recreated as fresh work.; When the queue is locally exhausted, emit `discovery-breakthrough-profile.*`, `discovery-family-prompts.*`,
- **Scripts:** [enqueue_discovery_programmes.py](../../skills/discovery/kb-discovery-cycle/scripts/enqueue_discovery_programmes.py), [enqueue_proof_candidates.py](../../skills/discovery/kb-discovery-cycle/scripts/enqueue_proof_candidates.py), [execute_discovery_branches.py](../../skills/discovery/kb-discovery-cycle/scripts/execute_discovery_branches.py), [generate_discovery_branch_synthesis.py](../../skills/discovery/kb-discovery-cycle/scripts/generate_discovery_branch_synthesis.py), [generate_expert_conjectures.py](../../skills/discovery/kb-discovery-cycle/scripts/generate_expert_conjectures.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-discovery-cycle/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/discovery/kb-discovery-cycle/references/prompt-template.md), [queue-policy.md](../../skills/discovery/kb-discovery-cycle/references/queue-policy.md)
- **Outputs:** Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-entrypoint-finder`

- **Skill file:** [Open skill](../../skills/discovery/kb-entrypoint-finder/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Identify and rank the best conceptual entry points for proof progress by combining KB structure, concept-evolution phases, connector analysis, and proof hypotheses. Use when the user asks where to start, highest-impact intervention points, or best conceptual on-ramps for a specific KB.
- **Conceptual role:** This skill identifies the most informative conceptual entry points into a hard mathematical problem by combining graph position, concept evolution, and coherence signals.
- **Framework contribution:** It contributes prioritization so later stages start from statements with the highest expected proof payoff rather than arbitrary canonical definitions or theorems.
- **Workflow shape:** Load context artifacts.; Compute entry-point score.; Rank and cluster.; Recommend first actions.
- **Scripts:** [recommend_entrypoints.py](../../skills/discovery/kb-entrypoint-finder/scripts/recommend_entrypoints.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-entrypoint-finder/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/discovery/kb-entrypoint-finder/references/prompt-template.md), [scoring.md](../../skills/discovery/kb-entrypoint-finder/references/scoring.md), [script-usage.md](../../skills/discovery/kb-entrypoint-finder/references/script-usage.md)
- **Outputs:** `Stats`; `Top Entry Points`; `Concept Tracks`; `Tactical Next Step`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-entrypoint-pathfinder`

- **Skill file:** [Open skill](../../skills/discovery/kb-entrypoint-pathfinder/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Convert ranked conceptual entry points into concrete proof-pathway agendas with hypotheses, supporting links, and execution plans. Use when the user asks how to operationalize entry points into actionable abductive/deductive search tracks.
- **Conceptual role:** This skill synthesizes short proof-oriented pathways from the ranked entry points into surrounding bridge and hypothesis structure.
- **Framework contribution:** It contributes local route planning by showing how an entry point can be expanded into a usable sequence of nearby inferential moves.
- **Workflow shape:** Load ranked entry points.; Attach hypothesis and link context.; Build pathway agendas.; Rank pathways.
- **Scripts:** [synthesize_pathways.py](../../skills/discovery/kb-entrypoint-pathfinder/scripts/synthesize_pathways.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-entrypoint-pathfinder/agents/openai.yaml)
- **References:** [pathway-scoring.md](../../skills/discovery/kb-entrypoint-pathfinder/references/pathway-scoring.md), [prompt-template.md](../../skills/discovery/kb-entrypoint-pathfinder/references/prompt-template.md), [script-usage.md](../../skills/discovery/kb-entrypoint-pathfinder/references/script-usage.md)
- **Outputs:** `Stats`; `Ranked Pathways`; `Execution Plan` (per pathway)
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-epistemic-hardness`

- **Skill file:** [Open skill](../../skills/discovery/kb-epistemic-hardness/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Explain epistemologically why a hard problem is difficult using the current KB and intermediate artifacts. Use when the user asks why a problem (e.g., P vs NP) is hard, what the essential epistemic bottlenecks are, or which structural constraints block straightforward proof progress.
- **Conceptual role:** This skill articulates why a target problem is hard in epistemic and conceptual terms, not just by restating that it is open or technically difficult.
- **Framework contribution:** It contributes barrier analysis, asymmetry diagnosis, and research-program pressure points that explain which kinds of conceptual innovation are actually needed.
- **Workflow shape:** Load target KB and intermediate artifacts.; Quantify structural signals (dependency sparsity, barrier pressure, bridge dependence, phase dispersion).; Synthesize essential epistemic elements with explicit evidence IDs.; Produce concise actionable focus recommendations.
- **Scripts:** [articulate_hardness.py](../../skills/discovery/kb-epistemic-hardness/scripts/articulate_hardness.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-epistemic-hardness/agents/openai.yaml)
- **References:** [essential-elements.md](../../skills/discovery/kb-epistemic-hardness/references/essential-elements.md), [prompt-template.md](../../skills/discovery/kb-epistemic-hardness/references/prompt-template.md), [script-usage.md](../../skills/discovery/kb-epistemic-hardness/references/script-usage.md)
- **Outputs:** `Summary`; `KB Stats`; `Essential Elements`; `Recommended Focus`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-framework-state-formalizer`

- **Skill file:** [Open skill](../../skills/discovery/kb-framework-state-formalizer/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Formalize the current state of the Abducer reasoning framework as a concise LaTeX system description with typed state, inference operators, orchestration composition, scoring semantics, and logging contracts. Use when the user asks to formalize the framework itself, summarize the architecture mathematically, or generate a succinct `.tex` document describing the current reasoning pipeline.
- **Conceptual role:** This skill turns the current framework implementation into a concise formal system description.
- **Framework contribution:** It makes the framework itself inspectable as a typed reasoning architecture rather than only as a collection of scripts.
- **Workflow shape:** Read the current framework sources: `README.md`, `docs/architecture/architecture.md`, `docs/architecture/orchestration.md`, and `docs/reference/skills.md`.; Recover current primary inference modes, orchestrator intents, and skill inventory.; Map the implemented stages into a concise typed operator algebra.; Render a short LaTeX document that states the framework signature, stage composition, and observability contract.; Write a machine-readable manifest and the `.tex` file, and log the generation step.
- **Scripts:** [generate_framework_state_formalization.py](../../skills/discovery/kb-framework-state-formalizer/scripts/generate_framework_state_formalization.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-framework-state-formalizer/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/discovery/kb-framework-state-formalizer/references/prompt-template.md), [script-usage.md](../../skills/discovery/kb-framework-state-formalizer/references/script-usage.md)
- **Outputs:** `metadata`; `framework_signature`; `inference_modes`; `operators`; `latex_path`; `latex_source`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-gap-abstraction-conjecturer`

- **Skill file:** [Open skill](../../skills/discovery/kb-gap-abstraction-conjecturer/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Given connector, pathway, bridge-plan, hardness, and phyp artifacts, investigate concept gaps and conjecture which mathematical abstraction or object types could close them. Use when the user asks for conjecture mode, concept-gap analysis, bridge-filling abstractions, missing intermediate mathematical objects, or a systematic search for abstractions that would make a proof bridge testable.
- **Conceptual role:** This skill implements the conjecture mode: it studies concept gaps around promising bridges and proposes mathematical objects or abstractions that could close those gaps.
- **Framework contribution:** It contributes conceptual discovery by generating bridge-filling abstraction families, definitional profiles, and counterfactual probes.
- **Workflow shape:** Load structured artifacts only: `analysis`, `entrypoints`, `pathways`, `bridges`, `phyp`, and optional `hardness`.; Diagnose concept gaps per bridge: model mismatch, implication lift, missing invariant, transfer mechanism, barrier pressure, regime mismatch.; Conjecture abstraction families that could fill those gaps.; Derive necessary attributes, sufficient attribute sets, and counterfactual probes for each conjectured bridge concept.; Assess both constructive payoff and negative/impossibility pressure for each object hypothesis.; Emit human-readable construction templates and validation questions.
- **Scripts:** [conjecture_gap_abstractions.py](../../skills/discovery/kb-gap-abstraction-conjecturer/scripts/conjecture_gap_abstractions.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-gap-abstraction-conjecturer/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/discovery/kb-gap-abstraction-conjecturer/references/prompt-template.md), [script-usage.md](../../skills/discovery/kb-gap-abstraction-conjecturer/references/script-usage.md)
- **Outputs:** `metadata`; `gap_clusters`; `abstraction_conjectures`; `recommended_run_order`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-main-conjecture-grounder`

- **Skill file:** [Open skill](../../skills/discovery/kb-main-conjecture-grounder/SKILL.md)
- **Mode:** Generative agent
- **Description:** Ground current KB artifacts in the central theorem or conjecture under study and explain, in mathematical narrative form, how the active routes bear on that conjecture. Use when the user asks how the current bridges, proof sketches, or queue relate to the main conjecture itself, for example how a route in the P vs NP workspace bears on the claim P != NP.
- **Conceptual role:** This skill turns a route-level artifact set into a conjecture-centered argument. It explains not only what the current bridge program is, but why that program is relevant to the main mathematical claim.
- **Use when:** grounding of current artifacts in the main conjecture;; a logical implication chain from a route payoff to the central claim;; a narrative distinction between direct proof, stronger conditional target, and current frontier.
- **Workflow shape:** Identify the main conjecture explicitly.; Pull the local KB statements that define the ambient classes, target consequences, and known implication targets.; State the implication chain from the current leading route to the main conjecture.; Separate:; Write the result as a mathematical narrative, not as a pipeline changelog.
- **Agent config:** [openai.yaml](../../skills/discovery/kb-main-conjecture-grounder/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/discovery/kb-main-conjecture-grounder/references/prompt-template.md)
- **Outputs:** Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-novel-proof-strategist`

- **Skill file:** [Open skill](../../skills/discovery/kb-novel-proof-strategist/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Build a diversified proof-strategy portfolio from intermediate results and generate a systematic prompt that maximizes novelty under rigor constraints. Use when the user asks for distinct proof strategies, strategy portfolios, or novelty-maximizing planning prompts.
- **Conceptual role:** This skill designs proof strategies that combine current bridges, conjectured abstractions, and coherence diagnostics into distinct research programs.
- **Framework contribution:** It contributes strategic diversification and novelty pressure so the framework explores more than one local connector route.
- **Workflow shape:** Load intermediate artifacts.; Build strategy candidates from pathways and support context.; Select a diverse strategy set (phase diversity + low overlap).; Generate novelty-maximizing systematic prompt.
- **Scripts:** [design_strategies.py](../../skills/discovery/kb-novel-proof-strategist/scripts/design_strategies.py), [run_integrated_pvsnp.py](../../skills/discovery/kb-novel-proof-strategist/scripts/run_integrated_pvsnp.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-novel-proof-strategist/agents/openai.yaml)
- **References:** [novelty-policy.md](../../skills/discovery/kb-novel-proof-strategist/references/novelty-policy.md), [prompt-template.md](../../skills/discovery/kb-novel-proof-strategist/references/prompt-template.md), [script-usage.md](../../skills/discovery/kb-novel-proof-strategist/references/script-usage.md)
- **Outputs:** `Stats`; `Strategies`; `Novelty-Maximizing Prompt`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-prior-art-pass`

- **Skill file:** [Open skill](../../skills/discovery/kb-prior-art-pass/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Run a targeted prior-art / InformalMathLib pass over blocked routes or missing lemmas, import decisive external theorem references into InformalMathLib, and generate a content-first report of what the literature changes about the current proof state.
- **Conceptual role:** This skill runs a targeted literature pass once the local discovery/prove process has localized a set of missing lemmas or barrier classes.
- **Use when:** the queue has stalled on named missing lemmas or repair lemmas;; a route may already be partly covered by prior art;; the next step is to distinguish a genuinely missing theorem from a theorem that already exists in the literature;; `InformalMathLib/<kb-ref>` is too thin to support novelty or barrier judgments.
- **Workflow shape:** Start from the blocked proof queue, proof-cycle summary, and current InformalMathLib.; Record the local-search failure that justifies browsing.; Identify the smallest set of missing lemmas or barrier classes that actually matter.; If the blocked frontier suggests a missing foundation rather than a missing exact lemma, search for a mathematical framework with the same structural role before broadening to generic literature.; Search only for decisive theorem, definition, or axiom level references.; Import those references into InformalMathLib as external-reference entries.; Emit a report explaining:
- **Scripts:** [generate_prior_art_pass_report.py](../../skills/discovery/kb-prior-art-pass/scripts/generate_prior_art_pass_report.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-prior-art-pass/agents/openai.yaml)
- **Outputs:** Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-promising-direction-assessor`

- **Skill file:** [Open skill](../../skills/discovery/kb-promising-direction-assessor/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Summarize the most promising mathematical directions from final KB artifacts, explain the content-level novelty argument of each leading route, assess the next best direction to explore, and generate a report in Markdown, LaTeX, and PDF. Use when the user asks which routes are strongest, why they are novel in mathematical content, or what should be explored next from a completed run.
- **Conceptual role:** This skill turns final run artifacts into a compact research-assessment report centered on leading bridge routes, their mathematical novelty, and the next route that should be explored.
- **Use when:** `expert-hypothesis-paper.json`; `hypothesis-evaluation.json`; what the most promising directions are;; what is genuinely novel in content, not only in scoring;; what the next best direction to explore should be;; for a report artifact in `.md`, `.tex`, or `.pdf`.
- **Workflow shape:** Read the final expert paper and hypothesis evaluation artifacts.; Rank the bridge portfolio by route priority.; Summarize the top directions in content-first terms:; Explain novelty as mathematical-program novelty unless the artifacts already support a stronger claim.; Select the next best direction by preferring an adjacent high-priority route that stress-tests the same carrier in a harder regime.; Emit Markdown, LaTeX, and PDF outputs.
- **Scripts:** [generate_promising_directions_report.py](../../skills/discovery/kb-promising-direction-assessor/scripts/generate_promising_directions_report.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-promising-direction-assessor/agents/openai.yaml)
- **Outputs:** Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-proof-connector`

- **Skill file:** [Open skill](../../skills/discovery/kb-proof-connector/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Build a relational graph over KB statements and identify the highest-informative intervention points for proof discovery. Use when the user asks to connect definitions/theorems/axioms, discover high-value bridge links, prioritize abductive targets, map proof pathways, or surface concept/method/barrier structure across `KB/*.kb.md`.
- **Conceptual role:** This skill analyzes a KB as a structured relational graph and proposes the highest-value connections, intervention points, and proof hypotheses.
- **Framework contribution:** It contributes the core connective tissue of the framework by exposing potential support links, inferential commitments, and bridge-worthy concept structure.
- **Workflow shape:** Load target KB graph.; Quantify graph structure.; Propose cross-component links.; Build concept graph.; Rank intervention points.; Prepare abductive loop seeds.
- **Scripts:** [analyze_kb_graph.py](../../skills/discovery/kb-proof-connector/scripts/analyze_kb_graph.py), [generate_phyp.py](../../skills/discovery/kb-proof-connector/scripts/generate_phyp.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-proof-connector/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/discovery/kb-proof-connector/references/prompt-template.md), [scoring-model.md](../../skills/discovery/kb-proof-connector/references/scoring-model.md), [script-usage.md](../../skills/discovery/kb-proof-connector/references/script-usage.md)
- **Outputs:** `Stats`; `Top Intervention Points`; `Top Connection Candidates`; `Concept Graph`; `Abductive Loop Plan`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-proof-sketcher`

- **Skill file:** [Open skill](../../skills/discovery/kb-proof-sketcher/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Given conjecture, strategy, bridge, and hypothesis artifacts, outline structured proof sketches for the strongest conjectures. Use when the user asks for proof-sketch mode, conjecture-targeted proof outlines, sketching how a bridge concept could be proved, or defining proof-strategy families for a conjectured mathematical object.
- **Conceptual role:** This skill transforms promising conjectures and strategies into structured proof sketches with obligations, lemmas, checkpoints, and failure modes.
- **Framework contribution:** It contributes near-proof organization by turning bridge programs into ordered mathematical argument templates.
- **Workflow shape:** Load structured artifacts only: `conjectures`, `strategies`, `bridges`, `phyp`, and optional `analysis`, `coherence`, `hardness`.; Match conjectured bridge concepts to the most relevant strategy anchors and bridge programs.; Select a proof-strategy family: invariant lift, surrogate reduction, barrier escape, contradiction/collapse, derandomization transfer, or regime split.; Derive both constructive and negative/impossibility proof-space assessments for the bridge object.; Derive proof obligations, candidate lemmas, barrier checkpoints, and abort conditions.; Emit a human-readable proof outline for each prioritized conjecture.; When the KB is available, translate the strongest final pathway into a paper-style mathematical argument artifact.
- **Scripts:** [generate_proof_sketches.py](../../skills/discovery/kb-proof-sketcher/scripts/generate_proof_sketches.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-proof-sketcher/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/discovery/kb-proof-sketcher/references/prompt-template.md), [script-usage.md](../../skills/discovery/kb-proof-sketcher/references/script-usage.md)
- **Outputs:** `metadata`; `proof_sketches`; `recommended_execution_order`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

#### `kb-prove-cycle`

- **Skill file:** [Open skill](../../skills/discovery/kb-prove-cycle/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Run the prove cycle over the persistent proof queue: consume one queued claim, attempt an informal proof or disproof, apply systematic critique judges, use web search only under a parsimonious gate, and persist terminal positive or negative results into a problem-scoped InformalMathLib plus a summary report.
- **Conceptual role:** This skill turns one queued proof target into an auditable informal proof or disproof attempt.
- **Use when:** consume the next proof target from the queue;; attempt an informal proof or negative result;; run systematic critique over each proof step;; persist proved/disproved results into a problem-scoped InformalMathLib.
- **Workflow shape:** Start from the persistent queue.; Work locally first.; Attempt an informal proof or disproof.; Run critique judges.; Apply the web-search gate parsimoniously.; Finalize.
- **Scripts:** [finalize_proof_cycle.py](../../skills/discovery/kb-prove-cycle/scripts/finalize_proof_cycle.py), [generate_proof_cycle_summary.py](../../skills/discovery/kb-prove-cycle/scripts/generate_proof_cycle_summary.py), [generate_proof_queue_report.py](../../skills/discovery/kb-prove-cycle/scripts/generate_proof_queue_report.py), [start_proof_cycle.py](../../skills/discovery/kb-prove-cycle/scripts/start_proof_cycle.py)
- **Agent config:** [openai.yaml](../../skills/discovery/kb-prove-cycle/agents/openai.yaml)
- **References:** [critique-judges.md](../../skills/discovery/kb-prove-cycle/references/critique-judges.md), [prompt-template.md](../../skills/discovery/kb-prove-cycle/references/prompt-template.md), [web-search-policy.md](../../skills/discovery/kb-prove-cycle/references/web-search-policy.md)
- **Outputs:** Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

### proof_delivery

Theorem-shaped proof subworkflows that convert high-priority queue items into formal proof packets, conditional theorems, named blocked lemmas, countermodels, or quarantine decisions.

#### `lemma-chain-proof-builder`

- **Skill file:** [Open skill](../../skills/proof_delivery/lemma-chain-proof-builder/SKILL.md)
- **Mode:** Generative agent
- **Description:** Build and attempt dependency-typed lemma chains for proof-delivery queue items. Use when a formalized theorem, transfer result, no-go theorem, finite criterion, or paper subgoal needs an actual proof attempt with established lemmas, conditional lemmas, blocked lemmas, proof steps, edge cases, and counterexample checks.
- **Conceptual role:** Turns a formal theorem obligation into ordered, dependency-aware proof work with explicit parameter propagation and failure localization.
- **Validation handoff:** Requires a proof packet with theorem, lemma chain, parameter ledger, proof assembly, blocked lemmas, counterexample checks, and epistemic status.

#### `proof-delivery-workflow-orchestrator`

- **Skill file:** [Open skill](../../skills/proof_delivery/proof-delivery-workflow-orchestrator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Orchestrate proof-delivery subworkflows for theorem-shaped queue items. Use when a discovery, result-elaboration, P vs NP, Yang-Mills, or general mathematical queue item is no longer asking for exploration but for a delivered proof packet, including theorem statement, definitions, lemma chain, proof attempt, inference-quality review, proof gap localization, and paper/report handoff.
- **Conceptual role:** Keeps proof delivery bounded: proved theorem, conditional theorem, blocked named lemma, countermodel/no-go, or quarantine.
- **Validation handoff:** Requires a proof-delivery target, subworkflow plan, proof artifact requirements, stop conditions, and paper/report handoff.

#### `proof-gap-countermodel-splitter`

- **Skill file:** [Open skill](../../skills/proof_delivery/proof-gap-countermodel-splitter/SKILL.md)
- **Mode:** Generative agent
- **Description:** Split blocked proof gaps into repair lemmas, countermodels, no-go theorems, or quarantine decisions. Use when a proof-delivery run cannot complete a lemma and needs to decide whether to adapt the statement, prove a smaller lemma, construct a counterexample, convert the branch into an impossibility theorem, or stop.
- **Conceptual role:** Prevents infinite proof-churning by turning a stalled lemma into a repair, countermodel, no-go candidate, prior-art request, quarantine, or return-to-discovery decision.
- **Validation handoff:** Requires a named blocked lemma, gap type, countermodel search, repair candidate, no-go candidate, disposition, and next proof action.

#### `proof-obligation-formalizer`

- **Skill file:** [Open skill](../../skills/proof_delivery/proof-obligation-formalizer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Formalize theorem-shaped proof obligations before proof attempts. Use when a queue item, paper subgoal, no-go route, transfer lemma, or mathematical claim needs precise definitions, assumptions, quantifiers, model conventions, validity conditions, non-claims, and proof obligations before derivation can begin.
- **Conceptual role:** Prevents vague proof work by typing objects, quantifiers, assumptions, validity regimes, non-claims, named obligations, and falsifiers before derivation.
- **Validation handoff:** Requires a formal statement, definition ledger, quantifier/model ledger, assumptions, non-claims, named proof obligations, falsifiers, and readiness decision.

#### `proof-quality-gatekeeper`

- **Skill file:** [Open skill](../../skills/proof_delivery/proof-quality-gatekeeper/SKILL.md)
- **Mode:** Generative agent
- **Description:** Gate proof packets before they are promoted into a report, paper, result-elaboration artifact, or accepted queue completion. Use when a proof-delivery artifact must be checked for definition completeness, quantifier discipline, model preservation, lemma validity, counterexample coverage, inference-quality review, novelty boundary, and paper-ready non-claims.
- **Conceptual role:** Stops narrative proof packets from being promoted unless the theorem, definitions, lemmas, assumptions, non-claims, countermodel checks, and insertion target are coherent.
- **Validation handoff:** Requires a gate decision, accepted claims, rejected or overstated claims, required repairs, reviewer handoffs, paper/report handoff, and residual risk.

#### `pvsnp-forcedrows-proof-workflow`

- **Skill file:** [Open skill](../../skills/proof_delivery/pvsnp-forcedrows-proof-workflow/SKILL.md)
- **Mode:** Generative agent
- **Description:** Deliver the P vs NP EF+SAT_U occurrence-row ForcedRows proof packet. Use when the highest-priority P vs NP queue item asks to formalize Psys=EF+SAT_U^{occ}, extract Q_pi from a proof transcript, define ForcedRows(Q_pi), prove acceptance transcript invariance under private occurrence-label perturbations A_Q, and decide whether the beta-zero XOR row-forcing obstruction becomes a scoped no-go theorem or a blocked extraction obligation for full EF+SAT_U.
- **Conceptual role:** Provides the domain-specific proof chain for the current P vs NP decisive subgoal: parser lemma, transcript invariance lemma, sparse patch lemma, row-forcing obstruction theorem, and full EF+SAT_U boundary lemma.
- **Validation handoff:** Requires ForcedRows theorem statement, definition ledger, lemma chain, proof attempt, full EF+SAT_U escape boundary, inference-quality packet, paper insertion target, and final disposition.

### evaluation

Epistemic, mathematical, adversarial, contribution, payoff, and falsification checks that decide whether a route should continue, pivot, or stop.

#### `abducer-conceptual-pressure-formalizer`

- **Skill file:** [Open skill](../../skills/evaluation/abducer-conceptual-pressure-formalizer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Formalize Abducer dependency frontier nodes, blocked proof results, bridge gaps, and repeated route pressure into conceptual pressure packets. Use when hypothesis-space exploration needs typed failure, opportunity, open-question, or discovery-signal inputs before creative candidate generation.
- **Conceptual role:** Convert Abducer artifacts into typed conceptual pressure packets. Treat pressure as a control signal over the hypothesis exploration space, not as an explanation after the route has already been chosen.
- **Workflow shape:** Identify the exact source node or artifact that creates pressure.; Classify the pressure as `failure`, `discovery_signal`, `opportunity`, or `open_question`.; Preserve the witness text and source artifact paths.; State the repair target and unknowns.; Name successor hooks such as bridge invention, obligation factorization, theorem weakening, or representation shift.
- **Agent config:** [openai.yaml](../../skills/evaluation/abducer-conceptual-pressure-formalizer/agents/openai.yaml)
- **Outputs:** Emit objects conforming to `agentic/spec/conceptual_pressure_packet.schema.json`. Use `agentic/scripts/build_hypothesis_exploration_map.py` for deterministic seeded packets and `agentic/scripts/validate_hypothesis_exploration.py` before promotion.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `abducer-failure-signal-cartographer`

- **Skill file:** [Open skill](../../skills/evaluation/abducer-failure-signal-cartographer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Separate Abducer conceptual pressure packets into failure certificates, discovery signals, opportunities, and open questions with witnesses, falsifiers, and successor hooks. Use when blocked routes must be distinguished from positive structural pressure before hypothesis generation.
- **Conceptual role:** Build the classification layer between pressure formalization and creative hypothesis generation.
- **Workflow shape:** Read pressure packets and their source artifacts.; Emit failure certificates for blocked or missing obligations.; Emit discovery signals for repeated structures, bridge opportunities, or route patterns.; Preserve opportunity and open-question items when neither failure nor signal is justified.; Attach falsifiers and demotion conditions to every classification.
- **Agent config:** [openai.yaml](../../skills/evaluation/abducer-failure-signal-cartographer/agents/openai.yaml)
- **Outputs:** Emit `abducer_failure_certificate` and `abducer_discovery_signal` objects. Validate with `agentic/scripts/validate_hypothesis_exploration.py`.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `abducer-obligation-gatekeeper`

- **Skill file:** [Open skill](../../skills/evaluation/abducer-obligation-gatekeeper/SKILL.md)
- **Mode:** Generative agent
- **Description:** Convert creative Abducer hypothesis candidates into hard validation obligations and route-safety gates. Use when bridge, abstraction, regime, weakening, strengthening, carrier, analogy, inversion, factorization, or representation-shift candidates need preservation, activation, non-collapse, barrier, source, and proof-readiness checks.
- **Conceptual role:** Prevent conceptual creativity from bypassing proof discipline. Every candidate must become a validation packet before ranking or queue promotion.
- **Workflow shape:** Read candidate and creativity-analysis objects.; Emit one validation packet per candidate.; Add obligations for every hard gate.; Force quarantine or rejection when hard-gate failure remains.; Distinguish proof-queue candidates from discovery branches and revision items.
- **Agent config:** [openai.yaml](../../skills/evaluation/abducer-obligation-gatekeeper/agents/openai.yaml)
- **Outputs:** Emit objects conforming to `agentic/spec/abducer_validation_packet.schema.json`.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `abstraction-fit-gap-auditor`

- **Skill file:** [Open skill](../../skills/evaluation/abstraction-fit-gap-auditor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Compare current, available, and possible new abstractions against a major conceptual proof gap. Use when a proof route may be using the wrong carrier, quotient, invariant, interface, model, or bridge object and needs a critical fit verdict before promotion, lock-in, or another discovery cycle.
- **Conceptual role:** Audits whether an abstraction preserves the target-relevant structure, exposes the hard tension, and creates nontrivial proof obligations rather than defining success into existence.
- **Agent config:** [openai.yaml](../../skills/evaluation/abstraction-fit-gap-auditor/agents/openai.yaml)
- **Outputs:** `gap_statement`; `objects_compared`; `fit_matrix`; `fit_verdict`; `best_next_abstraction`; `requirements_missing`; `disconfirming_tests`; `epistemic_status`; `validation_handoff`.
- **Failure/demotion:** Demote comparisons that only rank labels, ignore broken invariants, omit edge cases, or skip available local/literature candidates. Quarantine definition-built candidates.

#### `bridge-object-equivalence-checker`

- **Skill file:** [Open skill](../../skills/evaluation/bridge-object-equivalence-checker/SKILL.md)
- **Mode:** Generative agent
- **Description:** Determine whether multiple candidate bridge objects are equivalent, incomparable, or route-breaking. Use when a proof route shifts between carriers such as a witness family and a promise problem.
- **Conceptual role:** This skill audits whether two or more bridge objects are mathematically the same program, merely related, or incompatible.
- **Agent config:** [openai.yaml](../../skills/evaluation/bridge-object-equivalence-checker/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/evaluation/bridge-object-equivalence-checker/references/prompt-template.md)
- **Outputs:** Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `contradiction-route-auditor`

- **Skill file:** [Open skill](../../skills/evaluation/contradiction-route-auditor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Audit proof-by-contradiction routes before they enter proof queue. Use when a reductio branch needs checks for exact negation, same-theory preservation, valid conflict targets, excluded cases, and non-vacuous mathematical content.
- **Conceptual role:** This skill is the adversarial gate for reductio routes. It asks whether a proof-by-contradiction branch really contradicts something accepted in the same mathematical world, or whether it only sounds decisive because the route changed objects, strengthened the negation, or imported a conflict target from outside the active theory.
- **Agent config:** [openai.yaml](../../skills/evaluation/contradiction-route-auditor/agents/openai.yaml)
- **References:** [audit-checklist.md](../../skills/evaluation/contradiction-route-auditor/references/audit-checklist.md)
- **Outputs:** `audited_route`: route ID, target, and source artifact.; `negation_check`: pass, repair, or fail with exact mismatch if any.; `same_theory_check`: pass, repair, or fail with preserved and broken; `carrier_check`: whether the carrier can support the claimed contradiction.; `conflict_target_check`: accepted, conjectural, missing, incompatible, or; `excluded_cases`: edge cases, counterexample classes, and boundary regimes.; `proof_obligations`: obligations required before promotion.; `disconfirming_observations`: what would demote or reject the route.
- **Validation handoff:** When a route passes, hand it to the relevant bridge-lemma packet, proof queue, or long-horizon report with the remaining proof obligations attached. When it fails, hand it to `kb-revision-loop`, `counterexample-hunter`, `premise-completeness-prober`, or a TODO card that names the exact repair.
- **Failure/demotion:** Demote on non-exact negation, hidden premise shift, object mismatch, broken same-theory invariant, conflict against a merely desired theorem, unhandled edge case or counterexample class, unsupported density claim, or missing validation handoff.

#### `contribution-value-assessor`

- **Skill file:** [Open skill](../../skills/evaluation/contribution-value-assessor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Qualify the value of a scientific contribution candidate by conceptual novelty, explanatory power, implications, generality, robustness, and validation burden. Use when a subgoal has been detected as contribution-shaped and needs a rigorous value assessment rather than a generic breakthrough score.
- **Conceptual role:** Use this skill after a candidate contribution has been detected. Its job is to judge the quality of the contribution, not merely whether it is exciting.
- **Agent config:** [openai.yaml](../../skills/evaluation/contribution-value-assessor/agents/openai.yaml)
- **Outputs:** `Candidate Summary`: smallest honest claim and contribution type.; `Value Matrix`: conceptual novelty, explanatory power, implications, generality, robustness, and certification readiness.; `Evidence For Each Dimension`: artifacts, equations, source cycles, validators, source references, or explicit unknowns.; `Implication Map`: immediate, route-level, and paper-level consequences.; `Validation Burden`: what remains to certify or demote the contribution.; `Overclaim Boundary`: exactly what the contribution does not prove.; `Final Disposition`: certify, near-certify, develop, watch, quarantine, or reject.
- **Validation handoff:** Use `python agentic/scripts/build_scientific_contribution_monitor.py` and `python agentic/scripts/validate_scientific_contribution_monitor.py`; for prior-art uncertainty, hand off to `prior-art-importer` or `evidence-acquisition-planner`.
- **Failure/demotion:** Demote if the assessment uses generic praise, collapses novelty into usefulness, hides prior-art risk, lacks evidence citations, or fails to state what would disconfirm or demote the contribution.

#### `completed-subgoal-enablement-auditor`

- **Skill file:** [Open skill](../../skills/evaluation/completed-subgoal-enablement-auditor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Audit whether a completed, achieved, handoff-ready, or claimed subgoal genuinely enables progress on the larger Abducer target problem. Use when a result atlas entry, proof object, marathon cycle window, paper section, or queue item is being interpreted as a completed subgoal for P vs NP, Yang-Mills, or another target and the workflow must decide whether it is a necessary gate, reusable bridge, local-only result, side contribution, or overclaimed proxy.
- **Conceptual role:** Decide whether completion opens a target gate, enables a bridge, decides a route, enables validation or paper handoff, remains local-only, or is being overclaimed.
- **Agent config:** [openai.yaml](../../skills/evaluation/completed-subgoal-enablement-auditor/agents/openai.yaml)
- **Outputs:** `Completed Subgoal`; `Bigger Problem Link`; `Before/After Gate`; `Enablement Class`; `Enablement Mechanism`; `Residual Blockers`; `Overclaim Boundary`; `Next Action`; `Atlas Update`; `Validation Handoff`.
- **Validation handoff:** Hand off to the result atlas, proof-delivery queue, timeline paper, validator, paper section, or self-explanatory TODO that should consume the completed subgoal.
- **Failure/demotion:** Demote to `local_value_only` or `proxy_or_overclaim` when the audit cannot name a target commitment, source object, target object, transfer map, postcondition, evidence path, or next consuming proof step.

#### `counterexample-hunter`

- **Skill file:** [Open skill](../../skills/evaluation/counterexample-hunter/SKILL.md)
- **Mode:** Generative agent
- **Description:** Search locally for barrier analogs, model mismatches, and failure witnesses before a route is promoted. Use when a positive argument needs adversarial pressure.
- **Conceptual role:** This skill is the local adversarial pass for discovery and prove.
- **Agent config:** [openai.yaml](../../skills/evaluation/counterexample-hunter/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/evaluation/counterexample-hunter/references/prompt-template.md)
- **Outputs:** Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `counterfactual-route-prober`

- **Skill file:** [Open skill](../../skills/evaluation/counterfactual-route-prober/SKILL.md)
- **Mode:** Generative agent
- **Description:** Stress-test an inference by minimally perturbing assumptions, carrier choices, or nearby theorem variants and checking whether the conclusion survives. Use when a route looks clean but may be brittle or spuriously phrased.
- **Conceptual role:** This skill tests whether an inference is robust or only accidentally true under one wording or carrier choice.
- **Agent config:** [openai.yaml](../../skills/evaluation/counterfactual-route-prober/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/evaluation/counterfactual-route-prober/references/prompt-template.md)
- **Outputs:** Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `dimensional-symmetry-constraint-checker`

- **Skill file:** [Open skill](../../skills/evaluation/dimensional-symmetry-constraint-checker/SKILL.md)
- **Mode:** Generative agent
- **Description:** Check qualitative physics relation claims against dimensions, scaling, symmetry, conservation, positivity, convexity, boundedness, and invariance. Use when a variable relation, monotonicity claim, asymptotic claim, or transfer claim may be physically impossible or underconstrained.
- **Conceptual role:** Use this skill as a hard plausibility filter before a qualitative relation is promoted. It asks whether the proposed relation is even compatible with dimensions, scaling, symmetries, conservation laws, positivity, convexity, boundedness, or invariance.
- **Workflow shape:** Restate the mathematical object, source variable, target variable, regime, and claimed relation.; Check units or scaling dimensions for every term and parameter.; Check symmetry and invariance: gauge invariance, translation/rotation, parity, time reversal, boundary invariance, or problem-specific transformations.; Check conservation, normalization, positivity, convexity, spectral support, boundedness, and monotonicity constraints.; Identify whether the relation uses a variable that cannot change independently because of a constraint.; Produce a verdict: pass, needs retyping, needs regime split, challenged, invalidated, or proof obligation.; Convert failures into graph challenges, falsifiers, or queue tasks.
- **Agent config:** [openai.yaml](../../skills/evaluation/dimensional-symmetry-constraint-checker/agents/openai.yaml)
- **Outputs:** `Claim Under Test`: relation, variables, regime, and source.; `Dimensional Check`: units, scaling dimensions, and mismatches.; `Symmetry/Invariance Check`: transformations preserved or violated.; `Constraint Check`: conservation, positivity, convexity, boundedness, and normalization.; `Verdict`: pass, challenged, invalidated, retype, split regime, or proof obligation.; `Failure Modes`: counterexamples, impossible signs, missing invariants, or proxy shifts.; `Validation Handoff`: graph challenge, relation packet, falsifier, queue item, or validator.
- **Validation handoff:** Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after constraint-driven graph changes.
- **Failure/demotion:** Demote claims that fail dimensions, violate symmetry, ignore conservation, or use an impossible sign. Quarantine if the relation can only be made valid by changing the mathematical object or target observable.

#### `entailment-gap-auditor`

- **Skill file:** [Open skill](../../skills/evaluation/entailment-gap-auditor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Determine whether the cited evidence actually entails a claim, only supports it heuristically, or is irrelevant. Use when coherence, analogy, novelty, or plausibility may be getting mistaken for derivation.
- **Conceptual role:** This skill separates true local entailment from merely suggestive support.
- **Agent config:** [openai.yaml](../../skills/evaluation/entailment-gap-auditor/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/evaluation/entailment-gap-auditor/references/prompt-template.md)
- **Outputs:** Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `epistemic-status-ledger`

- **Skill file:** [Open skill](../../skills/evaluation/epistemic-status-ledger/SKILL.md)
- **Mode:** Generative agent
- **Description:** Build a ledger over active claims, labeling them as grounded, conditional, conjectural, refuted, prior-art, or blocked. Use when the workflow is conflating coherence or novelty with evidence.
- **Conceptual role:** This skill turns a live route portfolio into an explicit claim ledger. It makes the epistemic status of each active claim inspectable.
- **Workflow shape:** Collect active claims from the current artifacts.; Label each claim with one status class.; Record evidence used, assertion license, overturn conditions, and next test.
- **Agent config:** [openai.yaml](../../skills/evaluation/epistemic-status-ledger/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/evaluation/epistemic-status-ledger/references/prompt-template.md)
- **Outputs:** Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `failed-hypothesis-anticipator`

- **Skill file:** [Open skill](../../skills/evaluation/failed-hypothesis-anticipator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Run a prompt-based premortem for proof hypotheses and proof pathways before investing major cycle budget. Use when a discovery marathon, Yang-Mills workflow, mathematical-physics branch, P vs NP route, result-atlas candidate, or publication-consolidation subgoal must anticipate likely failure modes, shallow/incremental drift, missing artifacts, proxy shifts, hidden transfer assumptions, low physics reward, or non-publication-worthy hypotheses before proof-search cycles continue.
- **Workflow shape:** Ask for the smallest success claim, source object, target object, carrier, transfer interface, missing artifact, hidden assumption, earliest failing gate, quickest falsifier, and publication reward.
- **Agent config:** [openai.yaml](../../skills/evaluation/failed-hypothesis-anticipator/agents/openai.yaml)
- **Outputs:** `hypothesis_id`; `target_id`; `candidate_claim`; `premortem_questions`; `declared_failure_signatures`; `earliest_decisive_test`; `artifact_debt`; `publication_reward_assessment`; `recommended_disposition`; `prompt_heuristic_for_next_cycle`; `validation_handoff`.
- **Validation handoff:** Use `python3 agentic/scripts/build_cycle_failure_archaeology.py --target <target>` and `python3 agentic/scripts/validate_cycle_failure_archaeology.py <packet.json>` when the premortem is attached to a failed cycle set.
- **Failure/demotion:** Demote, reframe, quarantine, or stop when the route has missing carrier, proxy shift, finite-to-global gap, uniformity gap, definitional transfer, artifact debt, no falsifier, low publication reward, literature collision, or noncommuting limits.

#### `failure-archaeology-explainer`

- **Skill file:** [Open skill](../../skills/evaluation/failure-archaeology-explainer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Build a deep post-failure explanation for a major proof or discovery cycle set. Use when a Yang-Mills, mathematical-physics, P vs NP, or other proof-search marathon stalls, fails a hard gate, repeats a blocker, gets demoted/quarantined, or needs to explain why the failed hypothesis was genuinely hard, why it failed, why the failure was not anticipated, and what future hypotheses should learn from it.
- **Workflow shape:** Identify the failed cycle set; state the smallest honest failed hypothesis; explain physics, mathematical, and representation hardness; explain why the route failed; explain why the failure was not anticipated; extract premortem heuristics; emit a route disposition.
- **Agent config:** [openai.yaml](../../skills/evaluation/failure-archaeology-explainer/agents/openai.yaml)
- **Outputs:** `cycle_set`; `failure_detected`; `smallest_honest_failed_hypothesis`; `hard_problem_diagnosis`; `why_failed`; `why_not_anticipated`; `anticipation_heuristics`; `learning_for_future_cycles`; `required_workflow_change`; `route_disposition`; `evidence_paths`; `validation_handoff`.
- **Validation handoff:** Use `python3 agentic/scripts/validate_cycle_failure_archaeology.py <packet.json>`.
- **Failure/demotion:** Reject postmortems that say only "the proof is hard" without naming the object, hard gate, failed bridge, missing evidence, anticipation heuristic, and next control action.

#### `visual-analogy-preservation-auditor`

- **Skill file:** [Open skill](../../skills/evaluation/visual-analogy-preservation-auditor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Audit theorem-level visual analogies for property preservation, mathematical distortion, physical relevance, and proof-search value. Use before a visual metaphor can influence branch selection, hypothesis promotion, report claims, or deep-reflection cycle decisions.
- **Workflow shape:** Reconstruct source and target; check invariants, symmetries, gauge or equivalence-class structure, locality/globality, sign or positivity, limiting behavior, physical carrier, and proof-obligation correspondence; assign a route disposition.
- **Agent config:** [openai.yaml](../../skills/evaluation/visual-analogy-preservation-auditor/agents/openai.yaml)
- **Outputs:** `audit_verdict`; `preserved_properties`; `distorted_properties`; `false_friend_risks`; `physical_relevance_verdict`; `proof_search_value`; `allowed_route_consequence`; `required_revision`; `non_claim_boundary`.
- **Validation handoff:** Use `python3 agentic/scripts/validate_visual_conceptualization_packet.py <packet.json>`.
- **Failure/demotion:** Quarantine or reject analogies that are intuitive but do not preserve named properties, hide proxy shifts, lack physical carriers, or fail to produce a concrete artifact, falsifier, route mutation, or representation requirement.

#### `visual-theorem-conceptualizer`

- **Skill file:** [Open skill](../../skills/evaluation/visual-theorem-conceptualizer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Explain theorems, proof routes, obstructions, and scientific concepts with property-preserving visual metaphors. Use when a deep reflection cycle needs a theorem-level analogy that names the main objects, key properties, physical carrier, proof pressure, distortions, and hypothesis-generating consequences.
- **Workflow shape:** Identify formal objects and proof pressure; choose a visual metaphor family; emit a preservation table and distortion ledger; then decide whether the analogy is explanation-only, hypothesis-seeding, audit-required, or quarantined.
- **Agent config:** [openai.yaml](../../skills/evaluation/visual-theorem-conceptualizer/agents/openai.yaml)
- **Outputs:** `target_id`; `source_context`; `formal_focus`; `main_concepts`; `key_properties`; `visual_metaphor`; `property_preservation_table`; `distortion_ledger`; `hypothesis_inspiration`; `non_claim_boundary`; `recommended_audit`.
- **Validation handoff:** Use `python3 agentic/scripts/build_visual_conceptualization_packet.py --target <target>` and `python3 agentic/scripts/validate_visual_conceptualization_packet.py <packet.json>`.
- **Failure/demotion:** Keep analogies explanation-only unless they preserve properties and generate a concrete route consequence; reject metaphors that smuggle in easier source domains.

#### `gedanken-need-assessor`

- **Skill file:** [Open skill](../../skills/evaluation/gedanken-need-assessor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Decide when Abducer should run a Gedanken experiment: an imagined but concrete situation that can expose a hidden assumption, variable dependence, regime shift, counterfactual contrast, or transfer boundary. Use before spending discovery budget on a thought experiment or when a branch is conceptually underdetermined.
- **Conceptual role:** Use this skill to decide whether a branch needs a Gedanken experiment. A Gedanken experiment is warranted when ordinary deduction, qualitative graph reasoning, or direct concrete probes have not yet made the decisive mechanism visible, but an imagined controlled situation could isolate the missing variable, contrast, or failure mode.
- **Agent config:** [openai.yaml](../../skills/evaluation/gedanken-need-assessor/agents/openai.yaml)
- **Outputs:** `Need Decision`: one of `design_now`, `run_concrete_probe_first`, `defer_until_variable_typed`, `defer_until_regime_typed`, `quarantine_as_analogy`, or `not_needed`.; `Need Assessment`: a schema-ready object with `decision`, `criteria_met`, `criteria_missing`, `rejected_alternatives`, and `why_not_direct_derivation_or_probe`.; `Candidate Contrast`: the variables or mechanisms the situation should separate.; `Required Preconditions`: variables, regimes, or transfer certificate needed before design.; `Expected Follow-Up Value`: what later cycle could do with the insight.; `Packet Provenance`: originating cycle IDs, branch IDs, affected node or edge IDs if already known.; `Validation Handoff`: `agentic/spec/gedanken_experiment_packet.schema.json` and `python agentic/scripts/validate_gedanken_experiment_packets.py`.
- **Validation handoff:** When design is licensed, hand off to `gedanken-situation-designer`. When the packet is produced, run `python agentic/scripts/validate_gedanken_experiment_packets.py` and feed the follow-up task to `gedanken-followup-planner` or the ranked queue.
- **Failure/demotion:** Demote when the proposed situation is generic inspiration, lacks a target object, cannot identify held-fixed variables, has no disconfirming observation, or would be a proxy problem. Quarantine if it is analogy-only. Reject any output that says the thought experiment proves the theorem.

#### `gedanken-transfer-guard`

- **Skill file:** [Open skill](../../skills/evaluation/gedanken-transfer-guard/SKILL.md)
- **Mode:** Generative agent
- **Description:** Evaluate whether insight from a Gedanken experiment can transfer to the active target without analogy drift, proxy substitution, or proof overclaim. Use before a thought-experiment insight is promoted into a branch decision or follow-up cycle.
- **Conceptual role:** Use this skill to protect the discovery loop from seductive imagined cases. A Gedanken experiment can reveal a mechanism, but transfer to the active target requires a certificate: same object family, same relation type, compatible regime, same-theory map, or a clear statement that the result is only conceptual guidance.
- **Agent config:** [openai.yaml](../../skills/evaluation/gedanken-transfer-guard/agents/openai.yaml)
- **Outputs:** `Transfer Verdict`: ready, needs certificate, conceptual only, quarantine, or invalidated.; `What Transfers`: mechanism, relation shape, falsifier, variable dependence, or follow-up task.; `What Does Not Transfer`: numerical value, proof status, continuum claim, target existence, or same-theory result.; `Certificate Needed`: artifact, derivation, computation, prior-art source, or validator.; `Graph Update Action`: one of `none`, `needs_probe`, `challenge_edge`, `revise_edge`, `annotate_edge`, or `quarantine`.; `Affected Branch Decision`: continue, adapt, backtrack, quarantine, or stop candidate.; `Validation Handoff`: packet validator, qualitative graph update, or next-experiment queue item.
- **Validation handoff:** Use `python agentic/scripts/validate_gedanken_experiment_packets.py` for packet integrity and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` when a transferred insight updates graph edges.
- **Failure/demotion:** Demote when the carrier is a proxy, the target observable is missing, regimes differ, variables are not aligned, or the situation has no disconfirming variant. Quarantine analogy-only insights until a transfer certificate exists. Reject any claim that the Gedanken experiment proves the target.

#### `hub-bias-auditor`

- **Skill file:** [Open skill](../../skills/evaluation/hub-bias-auditor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Audit whether entrypoints, pathways, or routes are being ranked because they are central ontology hubs rather than mathematically leverageful statements. Use when discovery is drifting structurally.
- **Conceptual role:** This skill detects graph-centrality drift in discovery artifacts.
- **Agent config:** [openai.yaml](../../skills/evaluation/hub-bias-auditor/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/evaluation/hub-bias-auditor/references/prompt-template.md)
- **Outputs:** Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `kb-discovery-breakthrough-profiler`

- **Skill file:** [Open skill](../../skills/evaluation/kb-discovery-breakthrough-profiler/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Profile the conceptual breakthrough or abstraction required by the current blocked frontier. Use when the question is no longer which theorem is missing, but what kind of conceptual move discovery must make next.
- **Conceptual role:** This skill sits above missing-lemma analysis. Its job is to classify blocked routes by the kind of conceptual breakthrough they require: realization, transport, alignment, explicitness, semantic bridging, or constructive instantiation. It also emits broader epistemic discovery patterns such as invariant discovery, regime localization, representation shifts, counterexample-led concept formation, route decomposition, and hybrid bridge synthesis. It now also spawns a routed discovery layer per family and per cross-cutting pattern, so the output is not just a report but an explicit search plan over distinct discovery branches. Each routed layer carries a local-first heuristic for when it is worth searching externally for a mathematical framework with similar structural properties that could serve as a foundation.
- **Use when:** the proof queue is exhausted or repeatedly blocked;; a prior-art pass shows that the targets are already known and the novelty locus has moved into the bridge layer;; discovery needs to search for a kind of abstraction rather than another theorem-shaped restatement.
- **Workflow shape:** Read the blocked proof frontier and the prior-art pass.; Group blocked routes by obstruction class.; For each class, determine:; Rank the classes by pressure on the current programme.; Emit family-specific prompt packs and cross-cutting epistemic-pattern prompts.; Spawn routed discovery layers that alternate targeted family work with broader reframing patterns.; Materialize those routed layers into `discovery-branch-queue.*` plus one dossier per branch under `artifacts/<kb-ref>/discovery-branches/`.; Emit a dispatch order and stop criteria so discovery does not collapse into one depth-first branch.
- **Scripts:** [generate_discovery_breakthrough_profile.py](../../skills/evaluation/kb-discovery-breakthrough-profiler/scripts/generate_discovery_breakthrough_profile.py)
- **Agent config:** [openai.yaml](../../skills/evaluation/kb-discovery-breakthrough-profiler/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/evaluation/kb-discovery-breakthrough-profiler/references/prompt-template.md)
- **Outputs:** Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `kb-discovery-governor`

- **Skill file:** [Open skill](../../skills/evaluation/kb-discovery-governor/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Govern mathematical discovery so search does not drift into unbounded depth-first exploration. Use when the user asks which routes deserve deeper investment, which subresults would already count as major contributions, or how to score the value of conjectures objectively from current artifacts.
- **Conceptual role:** This skill is the epistemic control layer for discovery. It does not try to prove the main conjecture directly. It decides which routes deserve deeper search, which routes should be lateralized or frozen, and which partial results already qualify as major contributions even without solving the main problem.
- **Use when:** `search-space-tree.json`; `expert-hypothesis-paper.json`; `proof-sketches.json`; `proof-queue.json`; `hypothesis-evaluation.json`; whether discovery is drifting into an indeterminate depth-first search;
- **Workflow shape:** Build the active route frontier from current artifacts.; Diagnose drift using explicit signals:; Classify possible subresults as:; Apply the major-contribution criteria.; Apply the conjecture-value rubric.; Decide for each route:
- **Scripts:** [generate_discovery_governor_report.py](../../skills/evaluation/kb-discovery-governor/scripts/generate_discovery_governor_report.py)
- **Agent config:** [openai.yaml](../../skills/evaluation/kb-discovery-governor/agents/openai.yaml)
- **References:** [conjecture-value-rubric.md](../../skills/evaluation/kb-discovery-governor/references/conjecture-value-rubric.md), [governance-criteria.md](../../skills/evaluation/kb-discovery-governor/references/governance-criteria.md), [prompt-template.md](../../skills/evaluation/kb-discovery-governor/references/prompt-template.md)
- **Outputs:** `Drift Diagnosis`; `Search Allocation Decision`; `Major Subresult Candidates`; `Conjecture Value Table`; `Recommended Next Actions`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `kb-end-to-end-proof-critic`

- **Skill file:** [Open skill](../../skills/evaluation/kb-end-to-end-proof-critic/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Assess whether the current artifact chain supports a plausible end-to-end proof of the main conjecture. Use when the user asks if the current route is close to a real solution, what still blocks end-to-end plausibility, or whether the system should stop because a plausible solution has been found.
- **Conceptual role:** This skill is the stop-rule and plausibility layer for the whole proof programme. It does not ask whether a route is interesting. It asks whether the current artifact chain is strong enough to count as a plausible end-to-end proof candidate.
- **Use when:** `macro-proof-state.json`; `macro-strategy-report.json`; `proof-cycle-summary.json`; `InformalMathLib/<kb-ref>/index.json`; terminal proof attempts, if any; whether the main problem may already have a plausible solution;
- **Workflow shape:** Read the macro-proof and macro-strategy artifacts.; Read the proof-cycle summary, InformalMathLib, and terminal proof attempts.; Apply the critic panel from [critic-panel.md](../../skills/evaluation/kb-end-to-end-proof-critic/references/critic-panel.md).; Evaluate the mandatory stop gates:; Emit a plausibility report and stop decision.
- **Scripts:** [generate_end_to_end_plausibility_report.py](../../skills/evaluation/kb-end-to-end-proof-critic/scripts/generate_end_to_end_plausibility_report.py)
- **Agent config:** [openai.yaml](../../skills/evaluation/kb-end-to-end-proof-critic/agents/openai.yaml)
- **References:** [critic-panel.md](../../skills/evaluation/kb-end-to-end-proof-critic/references/critic-panel.md), [prompt-template.md](../../skills/evaluation/kb-end-to-end-proof-critic/references/prompt-template.md)
- **Outputs:** Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `kb-hypothesis-evaluator`

- **Skill file:** [Open skill](../../skills/evaluation/kb-hypothesis-evaluator/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Evaluate proof hypotheses generated in `phyp/*.proof-hypotheses.yaml` and classify each as supported, refuted, or inconclusive using KB structure, connector evidence, and optional coherence/explanatory signals. Use when the user asks to test hypotheses, validate bridge links, decide which hypotheses to promote, or produce hypothesis-level outcome reports after proof-hypothesis generation.
- **Conceptual role:** This skill evaluates generated proof hypotheses against connector, coherence, and KB evidence to classify them as supported, refuted, or inconclusive.
- **Framework contribution:** It contributes disciplined triage so the workflow can retain only hypotheses that improve the inferential state of the theory.
- **Workflow shape:** Load KB + phyp payload.; Compute support/refutation signals.; Classify outcomes.; Emit actionable outputs.
- **Scripts:** [evaluate_hypotheses.py](../../skills/evaluation/kb-hypothesis-evaluator/scripts/evaluate_hypotheses.py)
- **Agent config:** [openai.yaml](../../skills/evaluation/kb-hypothesis-evaluator/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/evaluation/kb-hypothesis-evaluator/references/prompt-template.md), [scoring-rubric.md](../../skills/evaluation/kb-hypothesis-evaluator/references/scoring-rubric.md), [script-usage.md](../../skills/evaluation/kb-hypothesis-evaluator/references/script-usage.md)
- **Outputs:** `Stats`; `Verdict Counts`; `Per-Hypothesis Results`; `Recommended Actions`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `kb-hypothesis-refutation-loop`

- **Skill file:** [Open skill](../../skills/evaluation/kb-hypothesis-refutation-loop/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Run iterative hypothesis-validation rounds after `phyp` generation to drive hypotheses toward supported/refuted outcomes. Use when the user asks for multi-round testing, convergence over hypotheses, pruning low-yield hypotheses, or systematic refutation loops over `phyp/*.proof-hypotheses.yaml`.
- **Conceptual role:** This skill iterates over current proof hypotheses to support, weaken, refine, or refute them across multiple rounds.
- **Framework contribution:** It contributes persistence and theory revision pressure by preventing the system from leaving generated hypotheses unevaluated after a single pass.
- **Workflow shape:** Initialize loop state.; Evaluate unresolved hypotheses per round.; Update statuses.; Tighten or relax decision policy.; Emit loop artifacts.
- **Scripts:** [iterate_hypotheses.py](../../skills/evaluation/kb-hypothesis-refutation-loop/scripts/iterate_hypotheses.py)
- **Agent config:** [openai.yaml](../../skills/evaluation/kb-hypothesis-refutation-loop/agents/openai.yaml)
- **References:** [loop-policy.md](../../skills/evaluation/kb-hypothesis-refutation-loop/references/loop-policy.md), [prompt-template.md](../../skills/evaluation/kb-hypothesis-refutation-loop/references/prompt-template.md), [script-usage.md](../../skills/evaluation/kb-hypothesis-refutation-loop/references/script-usage.md)
- **Outputs:** `Round Summaries`; `Final Status Counts`; `Promotion Candidates`; `Refutation Candidates`; `Updated Hypothesis File`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `kb-revision-loop`

- **Skill file:** [Open skill](../../skills/evaluation/kb-revision-loop/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Generate ontology and representation revision actions from loop/coherence/hardness artifacts. Use when unresolved hypotheses remain after iterative testing and the workflow should trigger concept splitting, definition repair, regime switching, or KB re-encoding.
- **Conceptual role:** This skill proposes executable revisions to the KB or hypothesis set when the current ontology or concept structure blocks progress.
- **Framework contribution:** It contributes closed-loop repair by making failure trigger ontology changes rather than mere reranking of existing paths.
- **Scripts:** [revise_ontology.py](../../skills/evaluation/kb-revision-loop/scripts/revise_ontology.py)
- **Agent config:** [openai.yaml](../../skills/evaluation/kb-revision-loop/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/evaluation/kb-revision-loop/references/prompt-template.md), [script-usage.md](../../skills/evaluation/kb-revision-loop/references/script-usage.md)
- **Outputs:** `revision_actions`; `priority_program`; `revision_summary`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `limit-convergence-behavior-auditor`

- **Skill file:** [Open skill](../../skills/evaluation/limit-convergence-behavior-auditor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Audit qualitative claims about limits, convergence, divergence, saturation, noncommuting limits, and uniformity. Use when a physics branch moves from fixed cutoff, finite volume, finite time, toy setting, or local estimate to continuum, infinite-volume, long-time, or spectral conclusions.
- **Conceptual role:** Use this skill whenever a qualitative claim crosses a limit. Its job is to decide whether the relation survives the passage from fixed regulator, finite volume, finite time, toy model, or pointwise estimate to the target limiting object.
- **Workflow shape:** Name the source object, target limiting object, limit parameters, and order of limits.; Classify the convergence claim: pointwise, uniform, weak, distributional, norm, tightness, subsequential, limsup/liminf, or unknown.; State which qualitative relation is being transported across the limit.; Audit uniformity: constants, estimates, positivity, observable density, support bounds, or decay rates that must not vanish or blow up.; Check noncommuting limits by swapping order or holding one parameter fixed.; Identify leakage: mass to zero, spectral weight escaping, loss of compactness, boundary effects, renormalization drift, or observable collapse.; Emit a verdict and next proof obligation.
- **Agent config:** [openai.yaml](../../skills/evaluation/limit-convergence-behavior-auditor/agents/openai.yaml)
- **Outputs:** `Limit Map`: source family, target object, parameters, topology, and order of limits.; `Transported Relation`: qualitative claim being moved across the limit.; `Uniformity Audit`: constants, estimates, support, density, positivity, or decay that must survive.; `Noncommuting-Limit Test`: swapped order, fixed-parameter trap, or missing comparison.; `Leakage Modes`: what can vanish, escape, blow up, or change object.; `Verdict`: limit safe, needs uniformity, pointwise only, blocked, challenged, or invalidated.; `Validation Handoff`: proof obligation, graph status, falsifier, toy model, or queue item.
- **Validation handoff:** Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after limit-audited relation updates.
- **Failure/demotion:** Demote when a claim moves from finite to infinite or cutoff to continuum without topology, uniformity, or order-of-limit control. Quarantine results that are only fixed-regime evidence.

#### `literature-gap-relevance-auditor`

- **Skill file:** [Open skill](../../skills/evaluation/literature-gap-relevance-auditor/SKILL.md)
- **Mode:** Generative agent with deterministic validator handoff
- **Description:** Audit whether a proof avenue has a precise literature-positioned research gap, novelty boundary, field or physics impact, unification power, route-decision power, and enough major-publication reward to justify broad investment.
- **Conceptual role:** This skill prevents the marathon from drifting into incremental, rediscovered, or weakly target-facing avenues. It decides whether to invest, run only a bounded artifact sprint, reframe the gap, stop for prior-art collision, or quarantine low-relevance work.
- **Workflow shape:** Read target literature and current reports.; Name closest known results and exact limitations.; State the smallest honest claim and novelty boundary.; Score field impact, unification power, and route-decision power.; Emit an avenue warrant validated by `agentic/scripts/validate_avenue_literature_gap_warrant.py`.

#### `main-problem-alignment-auditor`

- **Skill file:** [Open skill](../../skills/evaluation/main-problem-alignment-auditor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Audit whether current Abducer strategies, subgoals, equations, probes, analogies, and contribution candidates remain aligned with the main target problem. Use during marathon reports, strategy evaluation, pivot decisions, paper-contribution assessment, or whenever a branch risks becoming a proxy problem, finite-regulator artifact, analogy without transfer, or workflow-only result.
- **Workflow shape:** Extract the target commitments from the problem statement and literature evolution.; For the active branch, name:; source object,; target object,; transfer map or reconstruction map,; assumptions,; validation handoff,; falsifiers.
- **Agent config:** [openai.yaml](../../skills/evaluation/main-problem-alignment-auditor/agents/openai.yaml)
- **Outputs:** `alignment_class`; `target_commitments_touched`; `source_to_target_handoff`; `proxy_or_transfer_risk`; `alignment_gain`; `alignment_loss`; `repair_action`; `decision_effect`: how this should change priority, stop criteria, or paper-readiness judgement.
- **Failure/demotion:** Demote, quarantine, backtrack, or pivot when the branch cannot name a source object, target object, transfer condition, validation handoff, or falsifier. Do not demote solely because the branch is intermediate; demote because the handoff to the main target is absent or refuted.

#### `mathematical-concept-gap-revisitor`

- **Skill file:** [Open skill](../../skills/evaluation/mathematical-concept-gap-revisitor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Critically revisit deep mathematical concepts, conceptual tensions, and major gaps in a proof route. Use when a theorem-shaped cycle, marathon branch, KB bridge, or report feels shallow, definitional, fragmented, stuck in local lemmas, or representation-limited and must diagnose whether the current concepts are the right ones before more proof search.
- **Conceptual role:** Re-opens the conceptual substrate of a route and asks which object, invariant, representation, or literature mismatch is actually blocking target-level progress.
- **Agent config:** [openai.yaml](../../skills/evaluation/mathematical-concept-gap-revisitor/agents/openai.yaml)
- **Outputs:** `target_pressure`; `concept_under_review`; `declarative_tension`; `current_abstraction_failure`; `major_gap_hypotheses`; `available_abstractions_to_revisit`; `new_abstraction_trigger`; `efficient_representation_handoff`; `falsifiers`; `epistemic_status`; `evidence`; `validation_handoff`.
- **Failure/demotion:** Demote diagnoses that say only "needs deeper concepts" without naming tension, mathematical object, invariant, alternatives, and falsifier. Quarantine diagnoses that change the target or treat definitional transfer as progress.

#### `paper-contribution-readiness-judge`

- **Skill file:** [Open skill](../../skills/evaluation/paper-contribution-readiness-judge/SKILL.md)
- **Mode:** Generative agent
- **Description:** Assess whether a current Abducer subgoal is close to a paper-level scientific contribution. Use when a discovery branch, obstruction, bridge lemma, qualitative mechanism, finite probe, literature synthesis, or workflow method might stand as an independent result and needs evaluation for novelty, explanatory power, implications, validation burden, and paper packaging readiness.
- **Workflow shape:** Name the smallest honest contribution claim.; Identify the contribution type: theorem/lemma, obstruction, finite falsifier, calculational method, conceptual reframing, benchmark/probe, literature synthesis, or workflow method.; Compare it against the target problem and historical development:; What known bottleneck does it address?; Why is the result not merely an internal workflow artifact?; What prior route or conceptual ambiguity does it clarify?; Evaluate readiness dimensions from 0 to 5:; `conceptual_novelty`
- **Agent config:** [openai.yaml](../../skills/evaluation/paper-contribution-readiness-judge/agents/openai.yaml)
- **Outputs:** `candidate_title`; `smallest_honest_claim`; `paper_contribution_type`; `readiness_level`: not_ready, developing, near_paper_note, paper_note_ready, or paper_argument_ready.; `dimension_scores`; `novelty_argument`; `explanatory_power`; `main_problem_implication`
- **Failure/demotion:** Reject, demote, or quarantine a paper-readiness claim when novelty is unsupported, the mathematical object is unstable, the proof sketch has no validator, the result only repackages workflow bookkeeping, or the overclaim boundary cannot protect the main theorem.

#### `physical-relevance-impact-auditor`

- **Skill file:** [Open skill](../../skills/evaluation/physical-relevance-impact-auditor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Audit whether a mathematical-physics subgoal has physical relevance and general field impact rather than only incremental mathematical progress. Use for Yang-Mills discovery cycles, Route A finite results, representational-dynamics branches, paper-readiness checks, result-atlas promotion, or any mathematical-physics contribution candidate that must name its physical carrier, same-theory handoff, continuum or spectral gate, field-facing consequence, and unification-power payoff before promotion.
- **Workflow shape:** Name the smallest honest mathematical claim.; Name the physical carrier.; Name the larger target gate touched.; Explain what a mathematical physicist or constructive QFT reader would understand differently.; Explain the unification power by naming the constraints, carriers, estimates, representations, or routes compressed by one mechanism.; Separate support-only mathematics from physics impact.; State the next physical-relevance test that promotes, demotes, pivots, or quarantines the branch.
- **Agent config:** [openai.yaml](../../skills/evaluation/physical-relevance-impact-auditor/agents/openai.yaml)
- **Outputs:** `smallest_honest_claim`; `physical_carrier`; `target_commitments_touched`; `general_impact_vector`; `relevance_decision`; `major_publication_gate`; `general_impact_claim`; `incremental_math_drift_risk`; `next_physical_relevance_test`; `overclaim_boundary`; `evidence`; `validation_handoff`.
- **Failure/demotion:** Demote when the branch cannot name a physical carrier, same-theory handoff, continuum or spectral interface, nontriviality witness, field-facing understanding gain, unification gain, or falsifier-backed route decision.

#### `premise-completeness-prober`

- **Skill file:** [Open skill](../../skills/evaluation/premise-completeness-prober/SKILL.md)
- **Mode:** Generative agent
- **Description:** Enumerate the exact explicit and implicit premises needed for an inference step, and identify the smallest missing premise set. Use when a route or proof step may rely on unstated assumptions, omitted theorem bodies, or hidden imports.
- **Conceptual role:** This skill audits whether an inference step is actually locally supported by the premises that are present.
- **Agent config:** [openai.yaml](../../skills/evaluation/premise-completeness-prober/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/evaluation/premise-completeness-prober/references/prompt-template.md)
- **Outputs:** Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `progression-payoff-judge`

- **Skill file:** [Open skill](../../skills/evaluation/progression-payoff-judge/SKILL.md)
- **Mode:** Generative agent
- **Description:** Judge whether an Abducer discovery strategy is making real progress, still has payoff potential, should be adapted, or should be stopped. Use after bounded cycle windows, marathon runs, strategy pivots, contribution-monitor updates, or whenever current outputs must be evaluated against problem history, current mathematical content, future direction, and anti-drift controls.
- **Workflow shape:** Read the target problem statement and literature evolution.; Read the latest discovery cycles, current physics/mathematical story, macro strategies, qualitative graph, and contribution monitor.; Identify the active strategy family and the exact object it is trying to move: lemma, obstruction, construction, estimate, falsifier, analogy, simulation, or paper handoff.; Ask what changed in the last completed window:; A new mathematical object was defined.; A previously vague dependency became a typed obligation.; A calculation, derivation, or falsifier became executable.; A route was demoted because it failed a content-specific test.
- **Agent config:** [openai.yaml](../../skills/evaluation/progression-payoff-judge/agents/openai.yaml)
- **Outputs:** `window`: cycle IDs and count judged.; `evidence_sources`: report paths or cycle IDs used.; `current_strategy`: concise route family and active object.; `what_progressed`: concrete changes, each tied to evidence.; `what_did_not_progress`: blocked or repetitive elements.; `payoff_potential`: high, medium, watch, or low, with why.; `decision`: continue, adapt, backtrack, pivot, handoff, or quarantine.; `next_decisive_test`: the bounded analysis that would most change the decision.
- **Failure/demotion:** Recommend demotion, quarantine, backtrack, or pivot when a branch fails a named falsifier, cannot identify its mathematical object, loses target alignment, repeats without new evidence, or cannot state a validation handoff.

#### `pvsnp-conceptual-pressure-localizer`

- **Skill file:** [Open skill](../../skills/evaluation/pvsnp-conceptual-pressure-localizer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Localize conceptual pressures that make a P vs NP branch hard. Use before another analysis when the loop must explain verification/search pressure, source-to-target transfer, quantifier strength, model choice, relativization, natural proofs, algebrization, advice leakage, padding/projection debt, or meta-complexity carrier pressure.
- **Conceptual role:** Convert vague difficulty language into typed pressure packets that state what object would have to be lower-bounded, what transfer must preserve the target, which barrier applies, and where proof debt is being moved.
- **Workflow shape:** Name target and branch.; Localize the pressure source.; State why it is essentially hard.; Preserve model and quantifier discipline.; Separate route value from target proof.; Emit persist/adapt/backtrack/pivot/quarantine controls.
- **Agent config:** [openai.yaml](../../skills/evaluation/pvsnp-conceptual-pressure-localizer/agents/openai.yaml)
- **Outputs:** Target and branch; conceptual pressure map; barrier and model audit; debt relocation check; progress criterion; branch control; validation handoff.
- **Validation handoff:** Hand relation variables to `pvsnp-qualitative-complexity-reasoner`, no-go opportunities to `pvsnp-impossibility-theorem-forger`, and ranking decisions to `next-experiment-queue-ranker`.
- **Failure/demotion:** Demote outputs that only recite famous barriers, omit source/target objects, ignore quantifiers, or confuse a diagnostic obstruction with proof of `P != NP`.

#### `qualitative-physics-falsifier`

- **Skill file:** [Open skill](../../skills/evaluation/qualitative-physics-falsifier/SKILL.md)
- **Mode:** Generative agent
- **Description:** Generate relation-specific edge cases, counter-regimes, and falsifiers for qualitative physics claims. Use when a variable relation needs tests for sign reversal, nonmonotonicity, nonuniform convergence, singular perturbation, hidden variables, symmetry violation, positivity failure, or proxy drift.
- **Conceptual role:** Use this skill to attack a qualitative relation before the loop relies on it. It should generate the smallest counter-regime, variant, or disconfirming observation that would demote the claim.
- **Workflow shape:** Restate the relation claim, variables, regime, graph edge, and evidence basis.; Identify the weakest premise the claim depends on.; Generate falsifier families: sign reversal, nonmonotonicity, threshold failure, singular perturbation, hidden coupling, symmetry violation, positivity failure, boundary-condition dependence, nonuniform limit, or proxy drift.; For each falsifier, state the concrete observation or calculation that would trigger demotion.; Rank falsifiers by discriminating power and feasibility.; Decide branch effect: adapt, backtrack, quarantine, stop candidate after repeat failure, or keep as proof obligation.; Emit graph update advice and queue-ready next experiment when a falsifier is high value.
- **Agent config:** [openai.yaml](../../skills/evaluation/qualitative-physics-falsifier/agents/openai.yaml)
- **Outputs:** `Claim Under Attack`: relation, variables, regime, edge, and evidence.; `Weakest Premises`: assumptions that would collapse the relation if false.; `Falsifier Set`: concrete counter-regimes, variants, or observations.; `Disconfirmation Criteria`: exact result that demotes, quarantines, or invalidates the claim.; `Priority`: which falsifier should be tested first and why.; `Branch/Graph Effect`: adapt, backtrack, challenge edge, quarantine, or stop candidate with rescue condition.; `Validation Handoff`: validator, toy model, queue item, or graph update.
- **Validation handoff:** Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after falsifier-driven graph updates.
- **Failure/demotion:** Demote falsifier plans that are generic, impossible to observe, unrelated to the target relation, or require changing the mathematical object. Quarantine analogy-only attacks separately from same-target counterexamples.

#### `regime-shift-auditor`

- **Skill file:** [Open skill](../../skills/evaluation/regime-shift-auditor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Verify that quantifiers, regimes, models, thresholds, and representation shifts preserve the intended conclusion. Use when an inference crosses nearby but non-identical formulations and may be smuggling a model shift.
- **Conceptual role:** This skill checks whether an inference survives the exact shifts it claims to survive.
- **Agent config:** [openai.yaml](../../skills/evaluation/regime-shift-auditor/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/evaluation/regime-shift-auditor/references/prompt-template.md)
- **Outputs:** Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

#### `scientific-contribution-detector`

- **Skill file:** [Open skill](../../skills/evaluation/scientific-contribution-detector/SKILL.md)
- **Mode:** Generative agent
- **Description:** Identify whether a completed or nearly completed subgoal is a standalone scientific contribution candidate. Use when a discovery loop, report, milestone archive, or branch review needs to decide whether a result is independently publishable as a bridge lemma, obstruction, method, benchmark, negative result, conceptual reframing, or reusable evidence packet even if the main target remains open.
- **Conceptual role:** Use this skill to detect contribution-shaped subgoals inside a long-horizon discovery process. A contribution candidate is a completed or bounded subresult that could matter to another scientist without requiring the entire target theorem to be solved.
- **Agent config:** [openai.yaml](../../skills/evaluation/scientific-contribution-detector/agents/openai.yaml)
- **Outputs:** `Subgoal`: name, contribution type, mathematical object, source cycles, and current status.; `Smallest Honest Claim`: the minimal scientific claim the subgoal could support.; `Why It Could Stand Alone`: independent usefulness, audience, reusable object, and target relation.; `Evidence Basis`: artifacts, equations, cycles, validators, sources, or explicit unknowns.; `Disqualifiers`: prior-art, proxy drift, missing validation, hidden premise, boundary regime, or overclaiming risks.; `Certification Path`: what would promote the candidate to a certified contribution.; `Validation Handoff`: validator, report, TODO, source search, paper draft, or stop/quarantine condition.
- **Validation handoff:** Use `python agentic/scripts/build_scientific_contribution_monitor.py` and `python agentic/scripts/validate_scientific_contribution_monitor.py` after adding or changing contribution candidates.
- **Failure/demotion:** Demote or quarantine when the candidate cannot name a mathematical object, has no evidence citation, only restates local workflow progress, lacks implications beyond the current run, or depends on an unacknowledged shift to a weaker problem.

### orchestration

Workflow-level routing, long-horizon branch control, queue ranking, and run/report coordination.

#### `abducer-refinement-route-ranker`

- **Skill file:** [Open skill](../../skills/orchestration/abducer-refinement-route-ranker/SKILL.md)
- **Mode:** Generative agent
- **Description:** Rank validated Abducer creative candidates into proof queue, discovery branch, revision loop, evidence task, quarantine, rejection, or stop dispositions. Use when hypothesis-space exploration must become work-loop actions and Looper-visible route decisions.
- **Conceptual role:** Choose continuation routes from validation evidence. Ranking is a control-plane decision over the hypothesis exploration space, not a proof of the candidate.
- **Workflow shape:** Read candidates, validation packets, epistemic statuses, and source pressure.; Score expected target contribution, validation strength, risk, and tractability.; Select one disposition: `proof_queue`, `discovery_branch`, `revision_loop`, `evidence_task`, `quarantine`, `reject`, or `stop`.; Record whether the candidate changed routing behavior.; Emit work-loop and Looper graph evidence.
- **Agent config:** [openai.yaml](../../skills/orchestration/abducer-refinement-route-ranker/agents/openai.yaml)
- **Outputs:** Emit `abducer_candidate_ranking` objects and update `conceptual_refinement_trace` through `agentic/scripts/build_hypothesis_exploration_map.py`.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote routes that exceed budget, omit commitment citations, skip validators, or drift into low-value hypotheses.

#### `contribution-oriented-subgoal-manager`

- **Skill file:** [Open skill](../../skills/orchestration/contribution-oriented-subgoal-manager/SKILL.md)
- **Mode:** Generative agent
- **Description:** Keep a long-horizon Abducer workflow always aiming at at least one independently valuable scientific subgoal. Use when branch scheduling, next-analysis queues, or marathon loops need metrics for contribution potential, conceptual novelty, explanatory power, implication payoff, and certification progress.
- **Conceptual role:** Use this skill to make standalone scientific contribution production a standing loop objective. The loop should always know which active subgoal could become a contribution, what type of contribution it is, what would certify it, and which metric is currently blocking it.
- **Workflow shape:** Load current story beats, ranked next analyses, qualitative graph, big-deal archive, and contribution monitor if present.; Ensure at least one active next analysis is explicitly tied to a contribution candidate or a contribution-disqualifying test.; Route branches so the best candidate receives budget unless target relevance, validation, or drift risk fails.; If no candidate exists, force a contribution-search move: bridge lemma search, obstruction search, reusable probe, conceptual reframing, or method paper handoff.; If a candidate is good enough, stop exploratory cycling on that branch and hand it to validation, prior-art, or paper packaging.; Promote, adapt, backtrack, quarantine, or stop contribution candidates using evidence and disqualifiers, not enthusiasm.
- **Agent config:** [openai.yaml](../../skills/orchestration/contribution-oriented-subgoal-manager/agents/openai.yaml)
- **Outputs:** `Contribution Portfolio`: active candidates, contribution types, scores, and statuses.; `Loop Objective`: which candidate or contribution-search move should guide the next cycles.; `Metrics`: contribution score, novelty, explanatory power, implications, validation gap, and staleness.; `Good Enough Boundary`: the smallest contribution claim, handoff threshold, remaining bounded validation, and why further exploration would or would not be waste.; `Routing Decision`: continue, adapt, backtrack, pivot, quarantine, stop, handoff, or launch contribution search.; `Evidence And Unknowns`: artifacts and explicit unknowns behind every metric.; `Validation Handoff`: contribution monitor, queue update, paper handoff, prior-art pass, or TODO.
- **Validation handoff:** Run `python agentic/scripts/validate_scientific_contribution_monitor.py` after changing contribution metrics or route priorities.
- **Failure/demotion:** Demote a candidate or route when metrics are high only because of generic wording, when no evidence changed, when target relevance is absent, when prior-art risk is unexamined, or when validation gaps remain unbounded.

#### `gedanken-followup-planner`

- **Skill file:** [Open skill](../../skills/orchestration/gedanken-followup-planner/SKILL.md)
- **Mode:** Generative agent
- **Description:** Convert accepted Gedanken experiment insights into concrete follow-up discovery-cycle tasks, ranked queue items, graph updates, or branch-control decisions. Use after a thought experiment has passed transfer guarding and needs to affect the workflow.
- **Conceptual role:** Use this skill to make Gedanken experiments operational. The output is not a story; it is a follow-up plan that tells the discovery loop what to derive, compute, falsify, formalize, search, update, backtrack, quarantine, or rank next.
- **Agent config:** [openai.yaml](../../skills/orchestration/gedanken-followup-planner/agents/openai.yaml)
- **Outputs:** `Follow-Up Queue Items`: action, description, packet ID, target branch, and priority rationale.; `Success Criteria`: what result would promote or persist/adapt.; `Failure/Demotion Criteria`: what result would backtrack, quarantine, or stop after repeat low payoff.; `Required Skills`: skill sequence and why.; `Queue Provenance`: `packet_id`, `situation_title`, `transfer_verdict`, originating cycle ID, originating branch ID, and affected graph edge when available.; `Graph/Packet Updates`: relation edge or packet artifact to update.; `Branch Control`: continue, adapt, backtrack, quarantine, watch/archive, or stop candidate.; `Validation Handoff`: exact report or validator.
- **Validation handoff:** The handoff is the ranked next-experiment queue, `agentic/reports/gedanken_experiments/latest.json`, and the validators `python agentic/scripts/validate_gedanken_experiment_packets.py` plus `python agentic/scripts/validate_discovery_marathon_report.py` when queue ranking changes.
- **Failure/demotion:** Demote plans that lack criteria, do not reference a packet, cannot affect a branch decision, or use the thought experiment as proof. Quarantine tasks when transfer guard says the insight is analogy-only. Falsify the plan if validators reject packet shape or report queue criteria.

#### `kb-orchestrator`

- **Skill file:** [Open skill](../../skills/orchestration/kb-orchestrator/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Orchestrate end-to-end informal theorem-assistant workflows across the KB skill set. Use when a user asks for a full pipeline, multi-step session, relational proof-connection analysis, conceptual entry-point discovery, coherentist/explanatory-power analysis, epistemic-hardness articulation, concept-bridge planning, conjecture-mode gap analysis, novelty strategy synthesis, proof-sketch generation, expert-paper synthesis with high-potential hypothesis recommendation, hypothesis evaluation/refutation loops, ontology revision loops, human-readable interpretation reports, process-graph/dynamics visualizations, reasoning-log coverage verification, or automatic routing between ingestion and reasoning modes (cohere, connect, coherence-eval, interpretation-reports, process-graph, reasoning-dynamics, entrypoints, hardness, bridge-plan, conjecture, strategies, proof-sketch, expert-paper, hypothesis-eval, hypothesis-loop, revision-loop, explain, deduce, abduce, induce, abductive-loop) over `KB/*.kb.md`. `induce` is routed only as a scoped late-stage synthesis mode over existing bridge/strategy/proof artifacts.
- **Conceptual role:** This skill coordinates the full KB reasoning workflow by routing intents, enforcing stage order, and preserving artifact/log consistency for each KB.
- **Framework contribution:** It contributes end-to-end reproducibility and makes the multi-skill framework behave like one coherent reasoning system instead of a loose collection of scripts.
- **Workflow shape:** Detect primary intent.; Resolve KB target.; Build minimal execution plan.; `ingest` -> `latex-kb-ingest`; `cohere` -> `kb-proof-connector` -> `kb-coherence-evaluator`; `connect` -> `kb-proof-connector`; `coherence-eval` -> `kb-coherence-evaluator`; `interpretation-reports` -> `kb-orchestrator/generate_interpretation_reports.py`
- **Scripts:** [execute_recommended_focus.py](../../skills/orchestration/kb-orchestrator/scripts/execute_recommended_focus.py), [export_phyp_docs.py](../../skills/orchestration/kb-orchestrator/scripts/export_phyp_docs.py), [generate_concept_evolution.py](../../skills/orchestration/kb-orchestrator/scripts/generate_concept_evolution.py), [generate_conceptual_dynamics.py](../../skills/orchestration/kb-orchestrator/scripts/generate_conceptual_dynamics.py), [generate_conceptual_space_animation.py](../../skills/orchestration/kb-orchestrator/scripts/generate_conceptual_space_animation.py), [generate_discovery_graph_explorer.py](../../skills/orchestration/kb-orchestrator/scripts/generate_discovery_graph_explorer.py), [generate_interpretation_reports.py](../../skills/orchestration/kb-orchestrator/scripts/generate_interpretation_reports.py), [generate_js_graph_visualization.py](../../skills/orchestration/kb-orchestrator/scripts/generate_js_graph_visualization.py), [generate_process_graph.py](../../skills/orchestration/kb-orchestrator/scripts/generate_process_graph.py), [generate_reasoning_dynamics.py](../../skills/orchestration/kb-orchestrator/scripts/generate_reasoning_dynamics.py), [generate_reasoning_log_index.py](../../skills/orchestration/kb-orchestrator/scripts/generate_reasoning_log_index.py), [generate_reasoning_surface_index.py](../../skills/orchestration/kb-orchestrator/scripts/generate_reasoning_surface_index.py), [generate_search_space_tree.py](../../skills/orchestration/kb-orchestrator/scripts/generate_search_space_tree.py), [run_orchestrator.py](../../skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py), [simulate_theorem_discovery.py](../../skills/orchestration/kb-orchestrator/scripts/simulate_theorem_discovery.py)
- **Agent config:** [openai.yaml](../../skills/orchestration/kb-orchestrator/agents/openai.yaml)
- **References:** [abductive-loop.md](../../skills/orchestration/kb-orchestrator/references/abductive-loop.md), [phyp-doc-export.md](../../skills/orchestration/kb-orchestrator/references/phyp-doc-export.md), [prompt-template.md](../../skills/orchestration/kb-orchestrator/references/prompt-template.md), [routing-matrix.md](../../skills/orchestration/kb-orchestrator/references/routing-matrix.md), [script-usage.md](../../skills/orchestration/kb-orchestrator/references/script-usage.md)
- **Outputs:** `Intent Classification`; `Selected KB`; `Skill Route`; `Execution Summary`; `Updated IDs`; `Top Intervention Points`; `Open Risks`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote routes that exceed budget, omit commitment citations, skip validators, or drift into low-value hypotheses.

#### `long-horizon-route-portfolio-manager`

- **Skill file:** [Open skill](../../skills/orchestration/long-horizon-route-portfolio-manager/SKILL.md)
- **Mode:** Generative agent
- **Description:** Manage Abducer long-horizon hypothesis exploration as a target-relevance portfolio. Use when a route set, discovery loop, or candidate ranking must preserve essential target commitments, avoid low-value drift, budget active branches, and decide whether hypotheses enter proof queue, discovery branch, revision loop, watch/archive, quarantine, or rejection.
- **Conceptual role:** Use this skill to keep creative exploration tied to the target spine. Treat generated hypotheses as disposable portfolio items, but treat essential target commitments as non-disposable constraints that must be cited before a branch receives active attention.
- **Workflow shape:** Resolve the active target ledger and list its essential commitments.; For each candidate, name the mathematical object, route family, cited commitments, target-relevance score, drift risk, and active budget consumed.; Promote only candidates whose cited commitments cover the route's required target commitments and whose drift risk is not high.; Send low-relevance but valid ideas to `watch_archive`; send high-drift or uncited ideas to `quarantine` or `reject`.; Preserve conceptual creativity by keeping speculative branches visible, but prevent them from consuming proof-queue budget until they produce commitment-specific evidence.
- **Agent config:** [openai.yaml](../../skills/orchestration/long-horizon-route-portfolio-manager/agents/openai.yaml)
- **Outputs:** `Target Spine`: commitment IDs, source evidence, and forbidden drift patterns.; `Portfolio Table`: candidate ID, route family, target-relevance score, drift risk, cited commitments, and routing decision.; `Promotion Decisions`: proof queue, discovery branch, revision loop, evidence task, watch/archive, quarantine, reject, or stop.; `Preserved Invariants`: commitments and mathematical objects that survived the route transformation.; `Broken/Unknown Invariants`: missing commitments, edge cases, counterexamples, or unvalidated representation shifts.; `Unresolved Obligations`: proof, source, validation, or target-relevance work needed before more budget is allocated.
- **Validation handoff:** After making or changing a portfolio decision, run the target relevance validator and hand off unresolved failures as TODOs or validation packets rather than leaving them as narrative caveats.
- **Failure/demotion:** Demote a route when it has no cited commitment IDs, target-relevance score below the active threshold, high drift risk with active routing, uncited source evidence, broken invariants, or a forbidden weakening. Falsify a portfolio decision if a later validator shows the branch no longer preserves an essential commitment.

#### `next-experiment-queue-ranker`

- **Skill file:** [Open skill](../../skills/orchestration/next-experiment-queue-ranker/SKILL.md)
- **Mode:** Generative agent
- **Description:** Rank Abducer next-experiment queues by target payoff, discriminating power, execution readiness, and anti-drift controls. Use when a discovery marathon, long-horizon loop, report tab, or branch scheduler needs to decide which queued experiment should run next and what concrete payoff criteria would justify promotion, adaptation, backtracking, quarantine, or stop.
- **Conceptual role:** Use this skill to turn an accumulated queue of possible next experiments into an ordered control surface. The queue is not a todo list in chronological order; it is a portfolio of possible interventions on the current proof or discovery state.
- **Agent config:** [openai.yaml](../../skills/orchestration/next-experiment-queue-ranker/agents/openai.yaml)
- **Outputs:** `Ranked Queue`: rank, cycle ID, branch, priority score or band, and epistemic status.; `Why This Target`: the target-relevance and decision-value reason for each high-ranked item.; `Payoff Criteria`: concrete success, failure, and anti-drift criteria.; `Required Skills`: skills to invoke before or during the experiment.; `Branch Continuation Decision`: continue, adapt, backtrack, pivot, watch/archive, quarantine candidate, or stop candidate.; `Premature-Stop Guard`: explicit conditions under which the branch must not be stopped yet.; `Stop Criteria`: repeat-evidence conditions required before stopping is licensed.; `Demotion/Backtrack Triggers`: what would lower the item, quarantine it, or force a pivot.
- **Validation handoff:** End by naming the next validator or artifact that controls the queue. For marathon reports, the handoff is `agentic/scripts/validate_discovery_marathon_report.py` plus the ranked queue embedded in `agentic/reports/discovery_marathon/full_timeline.html`. For future cycles, the handoff is the `branch_selection` dispatch phase and the next persisted cycle packet.
- **Failure/demotion:** Demote a queue item when it lacks a target object, has no falsifiable payoff criterion, repeats a previous blocker without new mathematical learning, requires unbounded exploration, shifts to another theory, or only promises generic literature/background value. Quarantine an item when its success would solve a different problem than the active target. Mark an item as a stop candidate only after repeat low-payoff evidence and a failed sharpening attempt. Falsify the ranking if a later validator shows missing payoff criteria, missing required skills, missing premature-stop guards, or sorted priority disagreement in the report payload.

#### `result-atlas-maintainer`

- **Skill file:** [Open skill](../../skills/orchestration/result-atlas-maintainer/SKILL.md)
- **Mode:** Generative orchestration
- **Description:** Maintain Abducer's cumulative result and subgoal atlas. Use when a discovery workflow needs to persist achieved results, derivations, obstructions, falsifiers, bridge candidates, open obligations, target-specific problem-map status, or report-facing cumulative scientific memory across P vs NP, Yang-Mills, or other target runs.
- **Conceptual role:** Turn timeline-local learning into durable result objects. The skill keeps track of what was achieved, what remains open, what belongs to which subgoal, and which future cycles would add real value instead of restating prior work.
- **Workflow shape:** Preserve target identity.; Normalize contribution candidates, pressure bridges, negative tactics, derivations, falsifiers, and milestones into stable result entries.; Map entries to target-specific route families.; Separate achievements from queued intentions.; Link derivations, assumptions, equations, proof steps, blocking gaps, and non-claims.; Feed the atlas back into branch prompts, queue ranking, and report rendering.
- **Agent config:** [openai.yaml](../../skills/orchestration/result-atlas-maintainer/agents/openai.yaml)
- **Outputs:** `agentic/reports/result_subgoal_atlas/latest.json`; `agentic/reports/problem_space_map/latest.json`; `agentic/reports/derivation_vault/latest.json`; matching Markdown reports; target-scoped report tab content.
- **Validation handoff:** Run `python agentic/scripts/build_result_subgoal_atlas.py`, `python agentic/scripts/validate_result_subgoal_atlas.py`, `python agentic/scripts/build_problem_space_map.py`, `python agentic/scripts/validate_problem_space_map.py`, `python agentic/scripts/build_derivation_vault.py`, and `python agentic/scripts/validate_derivation_vault.py`.
- **Failure/demotion:** Reject cross-target leakage, result entries without evidence or validation state, handoff-ready claims without non-claim boundaries, and branches that repeat archived claims without closing an obligation.

#### `show-reasoning`

- **Skill file:** [Open skill](../../skills/orchestration/show-reasoning/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Display the current surfaced reasoning process as a live terminal dashboard over `artifacts/reasoning-surfaces`, with proof-discovery-language programs and material-inference operations shown directly in the UI. Use when the user asks to watch reasoning live, inspect the current epistemic state while `work` or other skills run, or render the latest reasoning state for one problem or run id.
- **Conceptual role:** This skill is the live observability layer for the reasoner. It reads the surfaced reasoning channel rather than raw internal logs and renders the current epistemic process as a terminal dashboard.
- **Use when:** `work` or another scripted stage is running and you want to inspect the current reasoning state live;; you want a problem-scoped view over recent surfaced moments, agents, and PDL structure;; you want to inspect a specific `run_id`;; you want the latest reasoning state rendered with LaTeX-style notation mapped into terminal math symbols.
- **Workflow shape:** Read surfaced reasoning JSON files from `artifacts/reasoning-surfaces/*/*.json`.; Filter by `kb_ref`, `run_id`, or `agent` when needed.; Build a current snapshot from:; Render the snapshot as a Rich terminal dashboard.
- **Scripts:** [show_reasoning.py](../../skills/orchestration/show-reasoning/scripts/show_reasoning.py)
- **Agent config:** [openai.yaml](../../skills/orchestration/show-reasoning/agents/openai.yaml)
- **Outputs:** Return: selected route, target-relevance and drift-risk evidence, skill sequence, executed commands if any, produced artifacts, unresolved obligations, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote routes that exceed budget, omit commitment citations, skip validators, or drift into low-value hypotheses.

#### `work`

- **Skill file:** [Open skill](../../skills/orchestration/work/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Run the persistent outer work loop that alternates discovery and prove cycles, refreshes end-to-end proof plausibility after each step, and stops either when a maximum cycle budget is reached or when the current artifacts support a plausible solution to the main problem.
- **Conceptual role:** This is the outer control skill for the whole programme. It alternates between:
- **Use when:** keep working through discovery/prove cycles;; alternate automatically between frontier expansion and proof work;; stop after a fixed number of cycles;; stop early if the main problem looks plausibly solved.
- **Workflow shape:** Load the persistent work state from `artifacts/<kb-ref>/work-state.json`.; Refresh the end-to-end plausibility report.; If the stop criteria in [stop-criteria.md](../../skills/orchestration/work/references/stop-criteria.md) already fire, stop.; Otherwise run exactly one phase:; After the phase, refresh the plausibility report again.; If the auto-meta trigger fires, generate `meta-reflection-report.*`.; Persist the updated work state and next phase.
- **Scripts:** [run_work_cycle.py](../../skills/orchestration/work/scripts/run_work_cycle.py)
- **Agent config:** [openai.yaml](../../skills/orchestration/work/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/orchestration/work/references/prompt-template.md), [stop-criteria.md](../../skills/orchestration/work/references/stop-criteria.md)
- **Outputs:** Return: selected route, target-relevance and drift-risk evidence, skill sequence, executed commands if any, produced artifacts, unresolved obligations, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote routes that exceed budget, omit commitment citations, skip validators, or drift into low-value hypotheses.

### reporting

Expert handoff, contribution packaging, paper construction, timeline-to-LaTeX translation, references, diagrams, and formal derivation surfaces.

#### `endpoint-worked-calculation-packager`

- **Skill file:** [Open skill](../../skills/reporting/endpoint-worked-calculation-packager/SKILL.md)
- **Mode:** Generative agent
- **Description:** Turn a concrete endpoint, finite-block, or local model calculation into a paper-ready worked example. Use when a paper needs an explicit table, color/geometric factors, sign or eigenvalue test, numerical/symbolic bound, and reproducible calculation notes rather than open-ended theoretical exploration.
- **Workflow shape:** Identify the concrete finite geometry, regulator, variables, and observables.; Build the incidence/sign table or finite matrix used in the calculation.; Separate universal positive terms, cancelling terms, and dangerous residual terms.; Compute or bound the decisive scalar, determinant, eigenvalue, or sign condition.; Record how the calculation can be reproduced symbolically or numerically.; State exactly what the worked example validates, falsifies, or leaves open.
- **Agent config:** [openai.yaml](../../skills/reporting/endpoint-worked-calculation-packager/agents/openai.yaml)
- **Outputs:** Return: calculation target, setup, tables/matrices, formula derivation, computed value or bound, reproducibility notes, validation decision, and unresolved assumptions.
- **Validation handoff:** Hand off reproducibility artifacts: finite inputs, formula sequence, symbolic simplification notes, numerical tolerance if used, sign or eigenvalue criterion, and falsifiers. The calculation is successful only when another agent can rerun or independently check the decisive scalar, determinant, spectrum, or bound.
- **Failure/demotion:** Demote the calculation if it only restates the route, omits the finite inputs, hides regulator assumptions, lacks a sign/eigenvalue test, or cannot be reproduced.

#### `expert-handoff`

- **Skill file:** [Open skill](../../skills/reporting/expert-handoff/SKILL.md)
- **Mode:** Generative agent
- **Description:** Turn a route, proof attempt, or bridge program into a compact expert-facing inspection dossier. Use when a human mathematician needs to inspect the precise live claims and burdens.
- **Conceptual role:** This skill compresses the current state into claims a human expert can actually inspect.
- **Agent config:** [openai.yaml](../../skills/reporting/expert-handoff/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/reporting/expert-handoff/references/prompt-template.md)
- **Outputs:** Return: claims with evidence paths or unknowns, epistemic status, target relevance, unresolved debt, demotion triggers, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote or annotate claims when evidence is missing, status is conjectural, disconfirmation is unresolved, or report prose overstates proof progress.

#### `finite-theorem-section-packager`

- **Skill file:** [Open skill](../../skills/reporting/finite-theorem-section-packager/SKILL.md)
- **Mode:** Generative agent
- **Description:** Package a discovered finite theorem or obstruction criterion into a self-contained paper section. Use when a result needs definitions, hypotheses, theorem statement, proof skeleton, validity regime, and proof-obligation boundaries rather than further discovery.
- **Workflow shape:** Name the finite mathematical object and the ambient category where it lives.; State every hypothesis before the theorem, including normalization, quotient, topology, and remainder conditions.; Write the theorem as a local result independent of the main open problem.; Give a proof skeleton with lemmas, reductions, and where each assumption is used.; State what the theorem proves locally and what it does not prove globally.; Produce a checklist of missing details needed before publication.
- **Agent config:** [openai.yaml](../../skills/reporting/finite-theorem-section-packager/agents/openai.yaml)
- **Outputs:** Return: section title, definitions, hypotheses, theorem statement, proof skeleton, local conclusion, non-claims, validation checklist, and next edit.
- **Validation handoff:** Hand off to theorem/proof validators by providing a checklist that includes definition completeness, hypothesis use, proof-gap localization, counterexample search, and boundary comparison against the global target. The section is publication-ready only when a reader can verify the theorem without reading the discovery timeline.
- **Failure/demotion:** Demote the section if it hides a main-theorem assumption, uses undefined objects, lacks a proof route, or presents a local finite result as a global theorem.

#### `kb-expert-paper-generator`

- **Skill file:** [Open skill](../../skills/reporting/kb-expert-paper-generator/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Transform final KB reasoning artifacts into a bridge-first expert report that explains the main conceptual bridges, their proof sketches, and the supporting high-potential hypotheses using transparent generative justification. Use when the user asks for a final scientific report, an expert-facing explanation of the leading bridge programs, or a rigorous explanation of why specific bridges/hypotheses deserve expert attention.
- **Conceptual role:** This skill converts the final inferential state into a paper-level argument centered on conceptual bridges and the proof sketches attached to them, together with a ranked expert recommendation portfolio over hypotheses.
- **Framework contribution:** It operationalizes an explicit generative function for expert hypothesis selection, and a complementary bridge-priority model that balances bridge strength, abstraction maturity, proof-sketch quality, linked support, and proof readiness.
- **Workflow shape:** Load final artifacts (`coherence`, `entrypoints`, `pathways`, `hardness`, `strategies`, `proof-sketches`, `hypothesis-eval`, `hypothesis-loop`, `revision-loop`, `phyp`).; Build per-hypothesis feature vectors from typed signals only.; Compute potential and risk with the generative function.; Synthesize a bridge-first portfolio from bridge-plan, abstraction conjectures, and proof sketches.; Rank and tier hypotheses for expert review.; Write detailed bridge justifications, proof-sketch interpretations, and expert action plans.; Render scientific paper artifacts (`.md`, `.tex`) and full JSON provenance.
- **Scripts:** [generate_expert_paper.py](../../skills/reporting/kb-expert-paper-generator/scripts/generate_expert_paper.py)
- **Agent config:** [openai.yaml](../../skills/reporting/kb-expert-paper-generator/agents/openai.yaml)
- **References:** [generative-function.md](../../skills/reporting/kb-expert-paper-generator/references/generative-function.md), [prompt-template.md](../../skills/reporting/kb-expert-paper-generator/references/prompt-template.md), [script-usage.md](../../skills/reporting/kb-expert-paper-generator/references/script-usage.md)
- **Outputs:** `metadata`; `generative_function`; `bridge_selection_function`; `bridge_portfolio`; `recommended_bridges`; `hypothesis_scores`; `recommended_hypotheses`; `paper_markdown`
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote or annotate claims when evidence is missing, status is conjectural, disconfirmation is unresolved, or report prose overstates proof progress.

#### `kb-macro-proof-paper-writer`

- **Skill file:** [Open skill](../../skills/reporting/kb-macro-proof-paper-writer/SKILL.md)
- **Mode:** Scripted + generative agent
- **Description:** Write the current macro-proof state as a mathematical paper-style narrative grounded in the main conjecture, and render it as Markdown, LaTeX, and PDF. Use when the user asks for a conjecture-centered current-state note, a macro-proof paper for a problem such as P vs NP, or a publication-style synthesis of the leading route, supporting routes, and proof frontier.
- **Conceptual role:** This skill converts the current artifact frontier into a paper-style macro-proof note. The note is not a claim of proof. It is a conjecture-centered state report that explains the strongest current route, how it bears on the main conjecture, what supporting routes exist, and what remains to be proved.
- **Workflow shape:** Ground the leading route in the main conjecture.; State the logical implication chain from the current strongest payoff to the conjecture.; Present the leading bridge program in theorem-pair form.; Add the strongest supporting routes.; Add the current prove frontier from the queue.; End with an honest status assessment.; When the user asks what is still missing for completion, generate the macro-strategy report that isolates the unresolved proof package.
- **Scripts:** [generate_macro_proof_state_report.py](../../skills/reporting/kb-macro-proof-paper-writer/scripts/generate_macro_proof_state_report.py), [generate_macro_strategy_report.py](../../skills/reporting/kb-macro-proof-paper-writer/scripts/generate_macro_strategy_report.py)
- **Agent config:** [openai.yaml](../../skills/reporting/kb-macro-proof-paper-writer/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/reporting/kb-macro-proof-paper-writer/references/prompt-template.md), [script-usage.md](../../skills/reporting/kb-macro-proof-paper-writer/references/script-usage.md)
- **Outputs:** Return: claims with evidence paths or unknowns, epistemic status, target relevance, unresolved debt, demotion triggers, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote or annotate claims when evidence is missing, status is conjectural, disconfirmation is unresolved, or report prose overstates proof progress.

#### `prior-art-positioning-packager`

- **Skill file:** [Open skill](../../skills/reporting/prior-art-positioning-packager/SKILL.md)
- **Mode:** Generative agent
- **Description:** Build the prior-art and novelty-positioning section for a scoped mathematical or physics contribution. Use when a paper needs to compare its theorem, worked example, obstruction, method, or negative result against literature without overstating novelty.
- **Workflow shape:** State the candidate contribution in its smallest honest form.; Identify the closest known theorem families, techniques, and negative-result traditions.; Separate reused standard machinery from new object, new calculation, new bridge, or new obstruction.; Record what must be cited before novelty can be claimed.; State the novelty claim conditionally, with explicit limitations and non-claims.; Produce a reference-acquisition queue if sources are missing.
- **Agent config:** [openai.yaml](../../skills/reporting/prior-art-positioning-packager/agents/openai.yaml)
- **Outputs:** Return: smallest honest contribution, comparison axes, closest prior-art families, novelty boundary, required citations, non-claims, and reference-acquisition queue.
- **Validation handoff:** Hand off a reference queue with search terms, expected comparator families, must-cite results, and novelty risks. The positioning is acceptable only when it states what the contribution adds, what it reuses, what it does not settle, and which sources could force demotion.
- **Failure/demotion:** Demote the novelty claim if it lacks close comparators, confuses implementation with contribution, ignores known methods, or depends on uncited literature memory.

#### `scientific-contribution-paper-handoff`

- **Skill file:** [Open skill](../../skills/reporting/scientific-contribution-paper-handoff/SKILL.md)
- **Mode:** Generative agent
- **Description:** Turn a certified or near-certified contribution candidate into a scoped paper-argument handoff. Use when a subgoal has enough novelty, explanatory power, implications, and evidence to deserve a standalone note, section, workshop paper, method paper, negative-result note, or expert handoff while preserving unresolved main-target obligations.
- **Conceptual role:** Use this skill when a contribution candidate is ready to be written as a scoped scientific argument. The goal is not to inflate a subgoal into the main theorem. The goal is to package exactly what was learned, why it is new or useful, what it explains, what it implies, and what remains open.
- **Agent config:** [openai.yaml](../../skills/reporting/scientific-contribution-paper-handoff/agents/openai.yaml)
- **Outputs:** `Title And Claim`: smallest honest title, abstract claim, and contribution type.; `Argument Spine`: stepwise scientific argument.; `Novelty And Explanation`: what is new, what it explains, and what would be known without it.; `Implications`: next analyses, broader route portfolio, and possible external audience.; `Evidence Table`: claim-to-artifact mapping.; `Disqualifiers And Limits`: prior-art risk, proxy risk, validation gaps, and main-target boundary.; `Draft Sections`: suggested sections for Markdown/LaTeX.; `Validation Handoff`: required monitor, prior-art pass, validator, or TODO before publication.
- **Validation handoff:** Use `python agentic/scripts/build_scientific_contribution_monitor.py`, `python agentic/scripts/validate_scientific_contribution_monitor.py`, and, when a candidate is near-certified, `prior-art-importer` plus `kb-expert-paper-generator` or `kb-macro-proof-paper-writer`.
- **Failure/demotion:** Demote to `do_not_write` if the claim is only workflow progress, if evidence is absent, if novelty is unqualified, if prior-art risk is high and unsearched, or if the draft would imply the main theorem has been solved.

#### `subgoal-enablement-handoff-packager`

- **Skill file:** [Open skill](../../skills/reporting/subgoal-enablement-handoff-packager/SKILL.md)
- **Mode:** Generative agent
- **Description:** Package an enablement audit for a completed subgoal into report, atlas, timeline, proof-queue, or paper-facing language. Use after completed-subgoal-enablement-auditor, contribution-value-assessor, result-atlas-maintainer, or proof-delivery workflows decide that a subgoal is achieved, handoff-ready, locally valuable, route-deciding, or overclaimed and the repository needs a self-explanatory handoff for the bigger problem.
- **Conceptual role:** Turn an enablement judgment into durable report or paper language while preserving residual blockers and the main-target non-claim boundary.
- **Agent config:** [openai.yaml](../../skills/reporting/subgoal-enablement-handoff-packager/agents/openai.yaml)
- **Outputs:** `Packaging Target`; `Enablement Summary`; `Surface Block`; `Machine-Readable Fields`; `Evidence Map`; `Residual Blockers And Non-Claims`; `Validation Handoff`.
- **Validation handoff:** Hand off to the atlas, timeline note, proof queue, paper section, HTML summary, or TODO queue surface that should carry the enablement relation.
- **Failure/demotion:** Demote the handoff if the enablement class is absent, evidence is uncited, the next consumer is unnamed, residual blockers are hidden, or the text would make the completed subgoal sound like a proof of the full target.

#### `target-literature-evolution-narrator`

- **Skill file:** [Open skill](../../skills/reporting/target-literature-evolution-narrator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Write an understandable, cited narrative explaining a target major problem and how the literature evolved around it. Use when a report or timeline needs a user-facing tab that connects the problem statement, historical stages, conceptual shifts, and active workflow obligations.
- **Conceptual role:** Use this skill after a cited reference spine exists. The output should help an expert or motivated reader understand why the target problem has its current shape, why the obvious routes are insufficient, and how the active discovery loop relates to the historical literature.
- **Agent config:** [openai.yaml](../../skills/reporting/target-literature-evolution-narrator/agents/openai.yaml)
- **Outputs:** `Problem In One Page`: accessible statement, why it matters, and what would count as a solution.; `Literature Evolution`: chronological conceptual stages with cited references.; `What The Literature Teaches The Workflow`: route obligations, pitfalls, and useful abstractions.; `Open Problems Still Alive`: construction, nontriviality, OS/Wightman adequacy, continuum limit, and mass gap.; `References`: compact cited bibliography with URLs.; `Validation Handoff`: report artifact plus validator.
- **Validation handoff:** Use `python agentic/scripts/build_target_literature_evolution.py`, `python agentic/scripts/validate_target_literature_evolution.py`, and the discovery-marathon HTML validator.
- **Failure/demotion:** Demote if the narrative is a generic encyclopedia summary, has no citations, hides unresolved obligations, treats numerical or lattice evidence as proof, or fails to connect the literature to current workflow decisions.

#### `timeline-claim-boundary-auditor`

- **Skill file:** [Open skill](../../skills/reporting/timeline-claim-boundary-auditor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Audit timeline-derived paper claims against evidence, mathematical scope, transfer conditions, non-claims, and overclaim boundaries. Use when a paper section, contribution statement, derivation, or conclusion needs claim-safety review before TeX/PDF rendering.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-claim-boundary-auditor/agents/openai.yaml)
- **Outputs:** Return: accepted claims, rewritten claims, demoted claims, overclaim findings, missing evidence citations, unresolved obligations, non-claims, source-unit IDs, epistemic status, and validation handoff.
- **Failure/demotion:** Falsify or quarantine a claim if it lacks a source object, target object, validation handoff, evidence citation, or overclaim boundary. Demote conclusions that imply the main target is solved when only a local obstruction, calculation, or method note is supported.

#### `timeline-contribution-explainer`

- **Skill file:** [Open skill](../../skills/reporting/timeline-contribution-explainer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Explain paper contributions from timeline evidence in expert physics/mathematics language. Use when a timeline paper needs mechanism-level exposition, why a strategy paid off or failed, what the key mathematical objects do, and how current outputs change the route landscape.
- **Workflow shape:** Start from the active narrative goal lock and preserve its thesis.; Identify the mechanism and mathematical object.; Explain the pressure that led to it in the timeline.; Explain why earlier route formulations were insufficient.; Explain what the contribution changes for next analyses.; Name failure regimes and validation debt.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-contribution-explainer/agents/openai.yaml)
- **Outputs:** Return: mechanism narrative, evidence chain, failed-strategy learning, route-level implication, validation debt, epistemic status, and validation handoff.
- **Validation handoff:** Check that each contribution explanation names a mathematical object, at least one timeline cycle, and at least one failure or validation condition.
- **Failure/demotion:** Demote the explanation if it becomes bureaucratic summary, hides the mathematics, ignores failures, or cannot name the object whose behavior is being explained.

#### `timeline-contribution-stater`

- **Skill file:** [Open skill](../../skills/reporting/timeline-contribution-stater/SKILL.md)
- **Mode:** Generative agent
- **Description:** Motivate and state specific contribution claims from timeline, contribution-monitor, and strategy-judge artifacts. Use when a paper draft needs a crisp contribution list, novelty boundary, smallest honest claims, validation burden, and main-problem alignment rather than broad claims of progress.
- **Workflow shape:** Read the active narrative goal lock and reject candidates outside its paper subgoal.; Name the strongest contribution candidate.; State the smallest honest claim.; Explain why it is independently valuable even if the main problem remains open.; State what would validate or falsify it.; State the overclaim boundary.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-contribution-stater/agents/openai.yaml)
- **Outputs:** Return: contribution list, novelty argument, explanatory power, implications, validation burden, overclaim boundary, evidence citations, epistemic status, and validation handoff.
- **Validation handoff:** Require the paper validator to find at least three stated contributions with explicit evidence and at least one overclaim boundary.
- **Failure/demotion:** Demote a contribution when it has no precise object, no validation path, no target alignment, no novelty boundary, or only repeats workflow mechanics.

#### `timeline-cycle-latex-translator`

- **Skill file:** [Open skill](../../skills/reporting/timeline-cycle-latex-translator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Translate discovery-marathon timeline cycle entries into compact, paper-safe LaTeX. Use when cycle-level entries, branch outputs, equations, falsifiers, blocking gaps, or next experiments from the timeline report need to become a LaTeX timeline table, appendix section, or evidence-backed chronology without turning every cycle into paper body prose.
- **Workflow shape:** Select only cycles that change the mathematical object, proof obligation, falsifier, computation target, or paper claim boundary.; Translate each selected cycle into a compact LaTeX row or paragraph with cycle ID, branch title, learning, key equation, blocking gap, and next action.; Preserve equation validity conditions and avoid naked formulas.; Compress repeated cycles into one progression statement instead of copying chronology.; Mark whether the cycle belongs in the paper body, appendix, or archive.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-cycle-latex-translator/agents/openai.yaml)
- **Outputs:** Return: LaTeX section title, selected cycle IDs, one LaTeX table or enumerated timeline, equations with validity regimes, appendix/body placement, epistemic status for each entry, source artifact citations, non-claims, and validation handoff.
- **Validation handoff:** The LaTeX must compile, contain cycle references, avoid unescaped special characters, and keep mathematical claims linked to source cycles and validation-needed obligations.
- **Failure/demotion:** Demote the translation if it becomes a log dump, omits cycle IDs, strips equation assumptions, hides failed/pending obligations, or presents repeated route restatements as new results.

#### `timeline-definition-assumption-elicitor`

- **Skill file:** [Open skill](../../skills/reporting/timeline-definition-assumption-elicitor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Elicit and surface missing definitions, assumptions, validity regimes, and non-claim boundaries for Abducer discovery timeline entries. Use when marathon cycles, timeline reports, paper timelines, equations, derivation steps, candidate lemmas, or story beats need to be self-contained for an expert reader instead of relying on hidden context.
- **Conceptual role:** This skill makes timeline entries readable as mathematics. It names what symbols denote, which assumptions make a step valid, which regime is in force, and what the entry does not prove.
- **Workflow shape:** Detect definition pressure.; Detect assumption pressure.; Attach validity regimes.; Name non-claims.; Convert missing definitions and assumptions into next-analysis obligations.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-definition-assumption-elicitor/agents/openai.yaml)
- **Outputs:** `definitions_needed`; `assumptions_needed`; `validity_regime`; `non_claim_boundary`; `timeline_patch`; `next_obligation`; `evidence`; `validation_handoff`.
- **Validation handoff:** Use `python agentic/scripts/validate_discovery_marathon_cycle.py`, `python agentic/scripts/generate_discovery_marathon_html.py`, and `python agentic/scripts/validate_discovery_marathon_report.py`.
- **Failure/demotion:** Demote timeline entries that use formulas without definitions, derive conclusions without assumptions, hide a model switch, omit a validity regime, or turn a restricted/proxy statement into a main-problem claim.

#### `timeline-failed-route-interpreter`

- **Skill file:** [Open skill](../../skills/reporting/timeline-failed-route-interpreter/SKILL.md)
- **Mode:** Generative agent
- **Description:** Interpret failed, narrowed, or demoted strategies from the timeline report as scientific learning for a paper narrative. Use when a paper needs to explain why earlier routes did not pay off, what was learned mathematically, and how failures justify the current object without becoming workflow chronology.
- **Workflow shape:** Read failure-learning units from the paper interpretation IR.; Compress route history into conceptual beats: original route, pressure, failure reason, learned invariant, current narrowed object.; State the mathematical object or invariant that survived the failure.; State what was demoted, quarantined, or moved to future work.; Hand off only claim-bearing learning to the paper section synthesizer.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-failed-route-interpreter/agents/openai.yaml)
- **Outputs:** Return: compressed route-learning beats, surviving mathematical objects, demoted assumptions, source citations, contribution relevance, epistemic status, and validation handoff.
- **Failure/demotion:** Demote a route-learning paragraph if it is generic history, lacks evidence citation, has no mathematical object, cannot state what failed, or overclaims a failed branch as proof progress.

#### `timeline-formal-physics-deriver`

- **Skill file:** [Open skill](../../skills/reporting/timeline-formal-physics-deriver/SKILL.md)
- **Mode:** Generative agent
- **Description:** Build formal physics derivation sections from timeline outputs, equations, strategy-judge conclusions, and mathematical assumptions. Use when a timeline-derived paper needs a self-contained derivation with definitions, assumptions, validity conditions, obstruction criteria, and proof-obligation boundaries.
- **Workflow shape:** Read the narrative goal lock and derive only the mathematics needed by the locked paper subgoal.; Define the mathematical objects and validity regime.; State assumptions explicitly.; Present equations with stated conditions.; Derive the finite obstruction or bridge criterion step by step.; State what is proved locally and what remains a Yang-Mills proof obligation.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-formal-physics-deriver/agents/openai.yaml)
- **Outputs:** Return: definitions, assumptions, propositions, derivation steps, equations, validity conditions, unresolved obligations, epistemic status, and validation handoff.
- **Validation handoff:** The TeX/PDF validator must compile the derivation and find definitions, assumptions, equations, proposition, proof sketch, and unresolved obligations.
- **Failure/demotion:** Demote the derivation if equations lack assumptions, if a finite object is confused with a continuum theorem, if a proxy replaces the target theory, or if the proof-obligation boundary is missing.

#### `timeline-narrative-coherence-guard`

- **Skill file:** [Open skill](../../skills/reporting/timeline-narrative-coherence-guard/SKILL.md)
- **Mode:** Generative agent
- **Description:** Guard timeline-derived paper drafts against infinite exploration sprawl. Use when a discovery timeline, contribution monitor, or strategy judge must be compressed into a bounded paper subgoal with a coherent narrative spine, detail budget, demotion rules, and decisive next-work criteria.
- **Workflow shape:** Name the bounded paper subgoal in one sentence.; State the coherent narrative thesis that the paper can honestly defend now.; Build a narrative spine from problem pressure to mathematical object, theorem/example, transfer debt, and contribution claim.; Classify every candidate detail as body, appendix/future work, or quarantine.; Admit only details that strengthen the theorem, worked example, transfer certificate, prior-art boundary, or honest contribution claim.; State the decisive next work and the exact conditions under which continued exploration should stop, demote, or pivot.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-narrative-coherence-guard/agents/openai.yaml)
- **Outputs:** Return: bounded subgoal, narrative thesis, narrative spine, included-material policy, excluded-detail policy, detail budget, decisive next work, stop/demote criteria, do-not-stop-prematurely criteria, coherence checks, epistemic status, and validation handoff.
- **Validation handoff:** The timeline-paper validator must find a `paper_narrative_goal_lock` in the JSON artifact and a visible "Paper Narrative Goal Lock" section in the Markdown and TeX outputs.
- **Failure/demotion:** Demote the paper draft if it cannot name its subgoal, if the body is organized as run chronology rather than argument, if details do not support the theorem/example/transfer/claim spine, or if the conclusion implies a stronger result than the validated subgoal.

#### `timeline-organizing-diagram-builder`

- **Skill file:** [Open skill](../../skills/reporting/timeline-organizing-diagram-builder/SKILL.md)
- **Mode:** Generative agent
- **Description:** Build a paper-ready organizing diagram from timeline report structure, strategy families, contribution candidates, validation handoffs, and formal derivation dependencies. Use when a paper draft needs a conceptual map, TikZ diagram, route schematic, or source-to-target flow rather than a prose-only narrative.
- **Workflow shape:** Identify source objects, bridge objects, target commitments, falsifiers, and validation handoffs.; Arrange them as a route flow from problem commitments through timeline outputs to paper contributions.; Encode demotion or failure edges distinctly from constructive edges.; Emit TikZ-compatible diagram source and a caption that states the interpretation.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-organizing-diagram-builder/agents/openai.yaml)
- **Outputs:** Return: diagram nodes, edges, TikZ source, caption, evidence citations, epistemic status, and validation handoff.
- **Validation handoff:** The paper validator must compile the TikZ diagram and find source, bridge, contribution, and validation nodes.
- **Failure/demotion:** Demote the diagram if it has unnamed nodes, decorative arrows, no validation handoffs, or hides the distinction between proof, obstruction, and conjectural route pressure.

#### `timeline-paper-argument-architect`

- **Skill file:** [Open skill](../../skills/reporting/timeline-paper-argument-architect/SKILL.md)
- **Mode:** Generative agent
- **Description:** Build a coherent physics-paper argument blueprint from interpreted timeline report evidence. Use when paper creation needs a primary paper mode, thesis, contribution-to-evidence matrix, section responsibilities, non-claims, body/appendix/archive partition, and narrative budget before TeX drafting.
- **Workflow shape:** Read `agentic/reports/timeline_paper_interpretation/latest.json`.; Choose one primary paper mode: theorem note, worked-calculation note, obstruction note, method note, negative-result note, or survey-positioning note.; State the main thesis, smallest honest contribution claims, mathematical object, and overclaim boundary.; Map each contribution to evidence units, novelty-boundary units, validation-burden units, and non-claims.; Assign section responsibilities and narrative budget before any prose section is written.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-paper-argument-architect/agents/openai.yaml)
- **Outputs:** Return: blueprint ID, paper mode, title, abstract claim, main thesis, primary mathematical object, contribution claims, section plan, body/appendix/future/quarantine partitions, claim-reference map, non-claims, narrative budget, epistemic status, and validation handoff.
- **Failure/demotion:** Demote or quarantine the paper draft if no smallest honest claim can be stated, if no mathematical object is source-backed, if references are decorative, if validation burdens are absent, or if the body plan becomes raw chronology.

#### `timeline-paper-cross-section-reconciler`

- **Skill file:** [Open skill](../../skills/reporting/timeline-paper-cross-section-reconciler/SKILL.md)
- **Mode:** Generative agent
- **Description:** Reconcile timeline-derived paper sections for duplicate definitions, contradictory claims, dangling references, unresolved obligations, and narrative-budget violations. Use after section synthesis and before final TeX/PDF rendering.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-paper-cross-section-reconciler/agents/openai.yaml)
- **Outputs:** Return: duplicate definitions, conflicting claims, dangling references, accepted claims, demoted claims, unresolved obligations, narrative-budget findings, section repair actions, epistemic status, and validation handoff.
- **Failure/demotion:** Demote or block rendering if sections disagree on the mathematical object, if a claim is stronger in the conclusion than in the derivation, if references are decorative, if formulas lack assumptions, or if raw chronology exceeds the narrative budget.

#### `timeline-paper-section-synthesizer`

- **Skill file:** [Open skill](../../skills/reporting/timeline-paper-section-synthesizer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Synthesize coherent paper sections from the timeline paper blueprint, interpreted evidence units, formal derivation artifact, references, and diagrams. Use when the workflow needs main-body prose that follows a physics-paper argument rather than dumping report tabs or chronology.
- **Workflow shape:** Read the paper blueprint and section responsibilities.; For each section, use only assigned evidence units and source artifacts.; Write prose in the function of the section: motivation, related work, route learning, formal core, worked calculation, mechanism, discussion, or appendix.; Keep definitions, assumptions, propositions, and validation boundaries explicit.; Emit section-level source unit IDs, accepted claims, demoted claims, unresolved obligations, and TeX.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-paper-section-synthesizer/agents/openai.yaml)
- **Outputs:** Return: section ID, title, purpose, responsible skill, source unit IDs, body prose, LaTeX, accepted claims, demoted claims, unresolved obligations, epistemic status, and validation handoff.
- **Failure/demotion:** Demote a section if it is a report dump, repeats chronology, lacks mathematical object definitions, has no evidence citations, hides validation debt, or introduces claims outside the blueprint.

#### `timeline-paper-workflow-orchestrator`

- **Skill file:** [Open skill](../../skills/reporting/timeline-paper-workflow-orchestrator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Orchestrate an independent timeline-report-to-paper workflow that parses Abducer discovery timeline artifacts and assembles a paper-style narrative, TeX source, PDF, evidence packet, and validation handoff. Use when timeline report elements should become a standalone scientific paper draft independent from the main discovery loop.
- **Workflow shape:** Invoke `timeline-report-evidence-ingestor` to parse the full timeline report into source-backed evidence units, argument roles, and report-family coverage.; Invoke `timeline-paper-argument-architect` to choose the paper mode, thesis, contribution matrix, non-claims, section responsibilities, and narrative budget.; Invoke `timeline-narrative-coherence-guard` to verify the bounded paper subgoal and demote details outside the paper spine.; Invoke `finite-theorem-section-packager` when the paper hinges on a bounded finite theorem, obstruction criterion, or local proof packet.; Invoke `endpoint-worked-calculation-packager` when the paper needs the first explicit finite calculation, table, spectrum, sign test, or reproducibility witness.; Invoke `prior-art-positioning-packager` and `timeline-reference-manager` before novelty language is allowed into the contribution section.; Invoke `timeline-problem-space-narrator`, `timeline-contribution-stater`, and `timeline-contribution-explainer` against the blueprint, not raw tabs.; Invoke `timeline-failed-route-interpreter` to compress route failures into scientific learning.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-paper-workflow-orchestrator/agents/openai.yaml)
- **Outputs:** Return the produced artifact paths, section map, invoked skills, finite theorem section status, worked calculation status, prior-art positioning status, source artifacts, epistemic status, validation handoff, unresolved obligations, and demotion triggers.
- **Validation handoff:** Run the standalone workflow runner and validators after generation:
- **Failure/demotion:** Demote the draft if it cannot state a contribution, cites no evidence, uses decorative references, lacks a formal derivation, turns a local obstruction into an overclaimed proof, or keeps adding exploration details without improving the locked paper subgoal.

#### `timeline-problem-literature-latex-translator`

- **Skill file:** [Open skill](../../skills/reporting/timeline-problem-literature-latex-translator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Translate target-problem and literature-evolution report content into LaTeX. Use when the report's problem/literature tab, target history, references, macro strategy context, or related-work notes need to become a paper introduction, background, or related-work section with citations and bounded novelty claims.
- **Workflow shape:** State the target problem in theorem/body form before giving history.; Organize literature evolution by conceptual pressure, not by decorative chronology.; Separate established literature, internal artifact evidence, and conjectural positioning.; Use citations for every external comparison and artifact references for internal timeline evidence.; End with the precise gap the current paper subgoal addresses and what it does not address.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-problem-literature-latex-translator/agents/openai.yaml)
- **Outputs:** Return: LaTeX introduction/background/related-work section, theorem-shaped target statement, literature stages, comparator families, citation keys or source paths, novelty boundary, non-claims, epistemic status, and validation handoff.
- **Validation handoff:** The LaTeX must compile, include citation commands or artifact references, and explicitly distinguish the main problem from the scoped contribution.
- **Failure/demotion:** Demote the section if it lacks citations, confuses internal artifacts with literature, overclaims novelty, omits closest comparator families, or fails to connect the literature to the current finite paper subgoal.

#### `timeline-problem-space-narrator`

- **Skill file:** [Open skill](../../skills/reporting/timeline-problem-space-narrator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Describe the target problem space and related work from Abducer timeline and literature artifacts. Use when a timeline-based paper needs an introduction, historical development section, problem statement, route landscape, and source-backed explanation of why the current problem remains hard.
- **Workflow shape:** States the problem in accessible and formal terms.; Explains how the literature made the problem precise.; Names the historical route families and their unresolved obligations.; Connects the active timeline work to those obligations.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-problem-space-narrator/agents/openai.yaml)
- **Outputs:** Return: problem statement, related-work chronology, route landscape, unresolved obligations, source citations, epistemic status, and validation handoff.
- **Validation handoff:** Check that cited references exist in `agentic/reports/target_literature_evolution/latest.json` and that timeline claims cite cycle IDs or report paths.
- **Failure/demotion:** Demote the section if it becomes generic history, omits references, hides unresolved obligations, or treats the active route as established literature.

#### `timeline-reference-manager`

- **Skill file:** [Open skill](../../skills/reporting/timeline-reference-manager/SKILL.md)
- **Mode:** Generative agent
- **Description:** Manage references for timeline-derived paper drafts by curating cited literature, report artifacts, cycle evidence, and bibliography entries. Use when a paper workflow needs non-decorative references, consistent citation keys, provenance, and source limits from timeline and literature reports.
- **Workflow shape:** Load literature references from the target literature report.; Add artifact references for timeline, strategy judge, contribution monitor, macro strategy, qualitative graph, and derivation packets.; Deduplicate by reference ID or URL.; Create bibliography keys and TeX bibliography entries.; State what each reference supports and what it does not support.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-reference-manager/agents/openai.yaml)
- **Outputs:** Return: cited references, artifact references, BibTeX or TeX bibliography block, support/limitation notes, epistemic status, and validation handoff.
- **Validation handoff:** The validator must confirm that all paper citation keys resolve to bibliography entries and that at least one artifact reference supports each major contribution.
- **Failure/demotion:** Demote the bibliography if it cites unused sources, omits support roles, lacks URLs for literature entries, or uses sources to support claims beyond their limitations.

#### `timeline-report-evidence-ingestor`

- **Skill file:** [Open skill](../../skills/reporting/timeline-report-evidence-ingestor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Parse the full Abducer discovery timeline report and companion artifacts into a typed paper evidence interpretation IR. Use when a timeline-derived paper needs systematic use of all report tabs, source-unit IDs, argument roles, body/appendix/future/quarantine dispositions, and coverage accounting before paper drafting.
- **Workflow shape:** Load the embedded `marathon-data` payload from `agentic/reports/discovery_marathon/full_timeline.html`.; Load companion source artifacts: contribution monitor, target literature, macro strategy, strategy judge, parsimonious probes, formal derivation candidates, and timeline paper status.; Convert report elements into typed evidence units with mathematical object, source artifact, cycle ID when available, epistemic status, and argument role.; Assign each unit to exactly one disposition: main body, appendix, future work, or quarantine.; Emit coverage accounting for every report family so no populated tab is silently ignored.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-report-evidence-ingestor/agents/openai.yaml)
- **Outputs:** Return: interpretation ID, source report path, typed evidence units, mathematical object candidates, report-family coverage, missing-material warnings, disposition counts, epistemic status, validation handoff, and artifact paths.
- **Failure/demotion:** Demote the paper workflow if the interpretation cannot name an active mathematical object, contribution candidate, formal derivation material, or validation boundary. Quarantine units that only restate workflow mechanics, lack evidence citation, overclaim, or cannot affect the paper argument.

#### `timeline-report-latex-composer`

- **Skill file:** [Open skill](../../skills/reporting/timeline-report-latex-composer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Compose timeline report tabs into a coherent LaTeX packet by coordinating timeline-cycle-latex-translator, timeline-story-latex-translator, timeline-problem-literature-latex-translator, and timeline-summary-latex-translator. Use when full timeline report content including timeline, story, problem/literature, summary, queue, and contribution state must become TeX sections or a paper draft input.
- **Workflow shape:** Load the report JSON/HTML payload and identify available tabs: summary, timeline, accumulated story, problem/literature, macro strategies, paper status, and queues.; Prefer the interpretation IR and blueprint when they exist; raw tab translation is appendix evidence, not the paper spine.; Invoke `timeline-summary-latex-translator` for abstract/conclusion/status material.; Invoke `timeline-problem-literature-latex-translator` for introduction/background/related work.; Invoke `timeline-story-latex-translator` for strategy progression and conceptual narrative.; Invoke `timeline-cycle-latex-translator` for selected timeline evidence rows or appendix material.; Compose the sections into one LaTeX packet with a section map, citation map, non-claims, source-unit IDs, body/appendix roles, and validation handoff.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-report-latex-composer/agents/openai.yaml)
- **Outputs:** Return: section map, composed LaTeX packet, source artifact map, citation map, selected cycle IDs, appendix/body split, current claim boundary, non-claims, epistemic status, and validation handoff.
- **Validation handoff:** Run the timeline LaTeX-section builder and validator when available. The output must compile, include all four content families, and preserve bounded paper claims.
- **Failure/demotion:** Demote the packet if it fails to compile, has duplicate or contradictory sections, omits citations, hides uncertainty, or lets low-value timeline details overwhelm the coherent paper argument.

#### `timeline-story-latex-translator`

- **Skill file:** [Open skill](../../skills/reporting/timeline-story-latex-translator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Translate the accumulated timeline story or physics/conceptual narrative into LaTeX. Use when the report's story tab, accumulated physics story, strategy movement, route learning, why-strategies-failed notes, or pivot/backtrack narrative need to become a coherent LaTeX narrative section for a paper or appendix.
- **Workflow shape:** Identify the story arc: initial route, failure pressure, restrategy, current object, and decisive next test.; Translate the arc into physics/mathematical prose, not workflow administration.; Explain why abandoned or narrowed strategies did not pay off and what they taught.; Preserve the current strategy as a claim-bounded narrative, with explicit stop/pivot criteria.; End with the smallest current paper contribution and what remains blocked.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-story-latex-translator/agents/openai.yaml)
- **Outputs:** Return: LaTeX narrative section, route chronology compressed into conceptual beats, strategy-failure learning, current mathematical object, decisive next test, non-claims, source citations, epistemic status, and validation handoff.
- **Validation handoff:** The LaTeX must compile and read as an expert scientific narrative. It must include the current object, why earlier strategies narrowed, what would count as progress, and why the paper claim remains bounded.
- **Failure/demotion:** Demote the section if it is bureaucratic, generic, cycle-by-cycle without conceptual compression, missing why-strategies-failed explanations, or stronger than the evidence.

#### `timeline-summary-latex-translator`

- **Skill file:** [Open skill](../../skills/reporting/timeline-summary-latex-translator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Translate timeline-report summaries, current queue, contribution readiness, strategy judgement, success milestones, and next-analysis state into LaTeX. Use when the report summary tab or executive state needs to become a paper-safe abstract, conclusion, status section, or next-work section.
- **Workflow shape:** Extract the current claim boundary, major contribution candidate, readiness state, and decisive next action.; Translate queues into next analyses, not operational task lists.; State success milestones and stop/pivot criteria in content-specific terms.; Preserve non-claims and unresolved obligations.; Write summary LaTeX suitable for abstract, conclusion, or future-work sections.
- **Agent config:** [openai.yaml](../../skills/reporting/timeline-summary-latex-translator/agents/openai.yaml)
- **Outputs:** Return: LaTeX abstract/conclusion/status section, current contribution statement, readiness class, decisive next analyses, success criteria, stop/pivot criteria, non-claims, source citations, epistemic status, and validation handoff.
- **Validation handoff:** The LaTeX must compile and name the current contribution candidate, the strongest next analysis, and the reason the result is or is not paper-ready.
- **Failure/demotion:** Demote the section if it uses generic queue language, omits what is claimable now, hides unresolved obligations, or makes paper readiness sound stronger than the validation state.

### results_ellaboration

Independent paper-result expansion skills for turning a marked-up paper draft into a bounded result-elaboration plan. This workflow is deliberately separate from discovery marathons: it reads a manuscript, interprets its result context, extracts expansion needs, plans self-contained TODOs, defines local workflow hooks, validates claim boundaries, and explains how each expansion would strengthen the paper narrative. The Route A skills are a focused attack layer for the SU(2) Wilson-block paper: they try to resolve the highlighted open modules as mathematical obligations rather than merely expanding their prose.

#### `routea-open-point-orchestrator`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-open-point-orchestrator/SKILL.md)
- **Mode:** Generative orchestration
- **Description:** Coordinate second-wave Route A paper-result work after the paper-attack pass without invoking discovery-marathon workflows.
- **Conceptual role:** Selects the next valid open-point capability from the current finite theorem state while enforcing dependency gates between collar geometry, normalization, coefficients, margins, endpoints, and continuum handoffs.
- **Workflow shape:** Read the attack-integrated paper and completion JSON; classify the current state; select attempt, promote, demote, quarantine, defer, or integrate_no_claim_change; name the paper insertion target and validator.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-open-point-orchestrator/agents/openai.yaml)
- **Outputs:** Return: active open point, selected skill/script, dependency status, mathematical reason, expected artifact, paper insertion target, validation commands, and next handoff.
- **Failure/demotion:** Demote if it routes into discovery marathons, bypasses missing collar prerequisites, or emits task-management prose.

#### `routea-collar-redesign-forger`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-collar-redesign-forger/SKILL.md)
- **Mode:** Generative geometry design + deterministic handoff
- **Description:** Forge alternative Route A geometric collar families after the current transverse-width hairpin obstruction.
- **Conceptual role:** Responds to the concrete obstruction by proposing central-channel and common-footprint redesigns with explicit edge-list validation targets.
- **Workflow shape:** Restate the obstruction; compare symmetric triplet, temporal-transverse, plaquette, lollipop, and quotient-observable collar families; rank a top candidate; hand off to edge-list validation.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-collar-redesign-forger/agents/openai.yaml)
- **References:** [collar-design-patterns.md](../../skills/results_ellaboration/routea-collar-redesign-forger/references/collar-design-patterns.md)
- **Outputs:** Return: candidate families, top candidate, validation payload, normalization risks, promotion/demotion condition, and paper insertion target.
- **Failure/demotion:** Demote if it repeats the known failed \(s=m_k(\delta)\) move or lacks cutoff-indexed lattice paths.

#### `routea-same-theory-factorization-hunter`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-same-theory-factorization-hunter/SKILL.md)
- **Mode:** Generative proof search + finite matrix checks
- **Description:** Search for same-theory realizations of Route A normalization factors.
- **Conceptual role:** Turns the normalization gate into an active factorization search and prevents pair-dependent quotients from being smuggled into a positivity argument.
- **Workflow shape:** Classify factors; run PSD and entrywise-inverse checks; search for observable rescaling, congruence, positive-kernel, or reflected-Gram realization; emit proposition or obstruction.
- **Scripts:** [check_schur_factor_candidates.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/check_schur_factor_candidates.py)
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-same-theory-factorization-hunter/agents/openai.yaml)
- **Outputs:** Return: factor inventory, finite checks, same-theory realization attempt, admissibility verdict, manuscript result or obstruction, and next repair.
- **Failure/demotion:** Demote if finite PSD is treated as a same-theory realization or if entrywise division is assumed harmless.

#### `routea-symbolic-cas-auditor`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-symbolic-cas-auditor/SKILL.md)
- **Mode:** Exact symbolic/CAS audit + generative paper interpretation
- **Description:** Perform exact symbolic and CAS-assisted audits for the Route A SU(2) reflected Wilson-block paper. Use when finite Schur--Feshbach source-collision algebra, geometric-collar coefficient extraction, same-theory normalization, endpoint incidence, finite margin certificates, or manuscript integration needs exact matrix algebra, determinant/eigenvalue checks, two-sided endpoint inequality logic, or proof-obligation extraction.
- **Conceptual role:** Keeps symbolic computation tied to the paper's claim boundary: finite source-collision certificates can be promoted, while geometric-collar, endpoint, continuum, and spectral claims remain obligations unless their own same-theory data are supplied.
- **Workflow shape:** Identify symbolic target.; State matrix family and finite/geometric/endpoint status.; Run the narrow symbolic audit.; Inspect the JSON artifact.; Translate into theorem/proposition/lemma/certificate/demotion language.; Hand off locally to Route A coefficient, normalization, endpoint, or paper-integration skills.
- **Scripts:** [audit_routea_symbolic_cas.py](../../skills/results_ellaboration/routea-symbolic-cas-auditor/scripts/audit_routea_symbolic_cas.py)
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-symbolic-cas-auditor/agents/openai.yaml)
- **Outputs:** Symbolic target; definitions and assumptions; CAS or exact audit; paper-level interpretation; claim boundary; proof obligations; validation handoff.
- **Validation handoff:** Validate the generated report with `agentic/scripts/validate_routea_symbolic_cas_audit.py`, then route formulas to `routea-geometric-coefficient-extractor`, normalization obstructions to `routea-same-theory-normalization-certifier`, endpoint algebra to `routea-endpoint-local-integral-calculator` or `routea-endpoint-error-budget-certifier`, and prose to `routea-paper-result-integrator`.
- **Failure/demotion:** Demote if CAS output is not inspected, if source-collision variables are reused as geometric coefficients, if finite algebra is promoted into continuum evidence, or if manuscript prose contains process language.

#### `routea-finite-margin-evaluator`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-finite-margin-evaluator/SKILL.md)
- **Mode:** Deterministic certificate + generative interpretation
- **Description:** Evaluate or certify finite Route A source-collision margins \(\sigma\) and \(\tau\) with explicit uncertainty.
- **Conceptual role:** Strengthens the existing finite theorem by supporting concrete finite examples while preserving the non-claim about cutoff-uniform or continuum nonvanishing.
- **Workflow shape:** Validate lattice/action/path parameters; consume same-regulator Wilson expectation intervals or certified estimates; classify strict finite positivity, inconclusive intervals, or missing estimator.
- **Scripts:** [evaluate_routea_finite_margins.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/evaluate_routea_finite_margins.py)
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-finite-margin-evaluator/agents/openai.yaml)
- **Outputs:** Return: certificate status, sigma/tau intervals, uncertainty budget, finite-only nonclaims, and paper insertion target.
- **Failure/demotion:** Demote if estimates lack uncertainty, use a non-Wilson proxy, or imply continuum nonvanishing.

#### `routea-endpoint-local-integral-calculator`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-endpoint-local-integral-calculator/SKILL.md)
- **Mode:** Deterministic incidence extraction + generative local integral derivation
- **Description:** Derive endpoint incidence and local heat-kernel \(SU(2)\) ingredients from actual paths.
- **Conceptual role:** Turns the schematic endpoint expression into regulator-defined endpoint boxes, source variables, color conventions, and incidence weights.
- **Workflow shape:** Read validated paths; compute endpoint boxes and null-channel weights; state color/singlet conventions; choose exact group integration, character expansion, or local cumulant expansion.
- **Scripts:** [derive_routea_endpoint_incidence.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/derive_routea_endpoint_incidence.py)
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-endpoint-local-integral-calculator/agents/openai.yaml)
- **Outputs:** Return: endpoint boxes, incidence tensor, null-channel weights, color convention, local integral form, and sign-claim boundary.
- **Failure/demotion:** Demote if endpoint signs are inferred from the template or color normalization is absent.

#### `routea-endpoint-error-budget-certifier`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-endpoint-error-budget-certifier/SKILL.md)
- **Mode:** Interval certificate + analytic estimate planning
- **Description:** Certify two-sided Route A endpoint error budgets.
- **Conceptual role:** Decides whether an endpoint estimator gives a positive, negative, or inconclusive finite certificate, and rejects one-sided negative evidence.
- **Workflow shape:** Propagate margin, estimator, and error intervals; classify positive, negative, inconclusive, or invalid missing two-sided control; name missing constants.
- **Scripts:** [certify_routea_endpoint_error_budget.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/certify_routea_endpoint_error_budget.py)
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-endpoint-error-budget-certifier/agents/openai.yaml)
- **Outputs:** Return: total error interval, certificate class, missing constants, theorem eligibility, and paper-safe wording.
- **Failure/demotion:** Demote if a lower bound is used as a negative certificate or any error class is omitted.

#### `routea-second-wave-manuscript-integrator`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-second-wave-manuscript-integrator/SKILL.md)
- **Mode:** TeX integration + claim-boundary audit
- **Description:** Integrate second-wave Route A open-point results into the SU(2) Wilson-block manuscript.
- **Conceptual role:** Updates the manuscript only when result artifacts are validated and keeps paper prose free of process language.
- **Workflow shape:** Read result schema; insert theorem/proposition/lemma/certificate/obstruction blocks; scan forbidden language; compile; emit a revision manifest.
- **Scripts:** [integrate_routea_second_wave_results.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/integrate_routea_second_wave_results.py)
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-second-wave-manuscript-integrator/agents/openai.yaml)
- **Outputs:** Return: integrated TeX path, revision manifest, changed claims, unchanged nonclaims, forbidden-language audit, and compile status.
- **Failure/demotion:** Demote if the TeX block contains planning language, overclaims, or breaks labels/references.

#### `routea-paper-attack-orchestrator`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-paper-attack-orchestrator/SKILL.md)
- **Mode:** Generative orchestration
- **Description:** Orchestrate an active mathematical attack on the open modules of the Route A SU(2) Wilson-block paper. Use when the finite source-collision paper has already been narratively expanded and the next task is to resolve, demote, or sharpen G1-G4, E1-E2, M1, and M2 into paper-ready results.
- **Conceptual role:** This is the dependency controller for the last paper. It prevents endpoint, continuum, or spectral prose from moving ahead of the geometric-collar obligations.
- **Workflow shape:** Load the latest Route A draft and open-module report; select the highest-priority unresolved module; invoke the relevant specialist; require a theorem, certificate, estimate, or obstruction; route any manuscript edit through `routea-paper-result-integrator`; update the paper attack TODO queue.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-paper-attack-orchestrator/agents/openai.yaml)
- **Outputs:** Return: active module, dependency status, mathematical move, deterministic/generative split, promotion or demotion, paper insertion target, result-integration status, and next TODOs.
- **Failure/demotion:** Demote if it restates the open module, imports source-collision formulas as geometric proof, writes paper prose before the mathematical object is stable, or leaks process language into the paper.

#### `routea-paper-result-integrator`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-paper-result-integrator/SKILL.md)
- **Mode:** Result integration + TeX audit
- **Description:** Integrate validated Route A module results back into the SU(2) Wilson-block paper as theorem, proposition, lemma, certificate, or demotion text. Use after a Route A paper-attack skill produces a mathematical artifact and the manuscript must be updated without leaking workflow, pipeline, TODO, or process-management language.
- **Conceptual role:** This is the paper-safety bridge between result artifacts and manuscript prose. It ensures the paper speaks in mathematical results, not in task-management narration.
- **Workflow shape:** Choose the smallest honest result form; insert definitions before claims; state assumptions and validity regimes; update abstract/introduction/table/conclusion only when the claim changes; compile TeX; scan for forbidden process terms.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-paper-result-integrator/agents/openai.yaml)
- **Outputs:** Return: result form, insertion point, manuscript patch, forbidden-language audit, compile status, and unresolved obligations.
- **Failure/demotion:** Demote if the artifact is only a plan, if the patch describes work management instead of mathematics, or if the conclusion becomes stronger than the theorem.

#### `routea-geometric-collar-builder`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-geometric-collar-builder/SKILL.md)
- **Mode:** Generative construction + deterministic checks
- **Description:** Attack Route A module G1 by constructing or refuting a cutoff-indexed geometric collar family for the SU(2) Wilson-block paper.
- **Conceptual role:** This is the first decisive bottleneck: without explicit paths, positive-time support, reflection pairing, and locked footprint, the paper cannot upgrade from source collision to geometric collar.
- **Workflow shape:** Reconstruct coordinates; propose edge lists; verify support, footprint, reflection, and scaling; emit a paper lemma or obstruction.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-geometric-collar-builder/agents/openai.yaml)
- **Outputs:** Return: edge lists, support check, footprint check, reflection check, promotion or obstruction, and manuscript patch.
- **Failure/demotion:** Demote if no explicit edge lists exist or if support, footprint locking, and reflection pairing cannot be satisfied simultaneously.

#### `routea-same-theory-normalization-certifier`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-same-theory-normalization-certifier/SKILL.md)
- **Mode:** Generative proof + matrix audit
- **Description:** Attack Route A module G2 by certifying that geometric-collar normalization is same-theory and positivity preserving.
- **Conceptual role:** This skill protects the reflected Gram interpretation by separating legitimate congruences and positive-kernel factors from inadmissible pair-dependent entrywise quotients.
- **Workflow shape:** Inventory normalization factors; classify them; prove congruence or positive-kernel realization; demote uncertified quotients.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-same-theory-normalization-certifier/agents/openai.yaml)
- **Outputs:** Return: factor inventory, same-theory certificate, inadmissible factors, promotion or demotion, and manuscript patch.
- **Failure/demotion:** Demote if normalization changes theory or assumes entrywise division preserves positivity without proof.

#### `routea-geometric-coefficient-extractor`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-geometric-coefficient-extractor/SKILL.md)
- **Mode:** Generative derivation + symbolic audit
- **Description:** Attack Route A module G3 by deriving first and second geometric-collar coefficients \(H_k,K_k\) and the operator-norm remainder from the same normalized Wilson block.
- **Conceptual role:** This skill decides whether the paper can state a genuine geometric Schur--Feshbach coefficient theorem.
- **Workflow shape:** Define entries; choose direct or log expansion; compute first and second variations; subtract the rank-one Schur correction; prove or demote the remainder.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-geometric-coefficient-extractor/agents/openai.yaml)
- **Outputs:** Return: \(H_k\), \(K_k\), remainder bound, reduced forms, proof status, and manuscript patch.
- **Failure/demotion:** Demote if coefficients are imported from the source-amplitude model or the remainder is only formal.

#### `routea-margin-endpoint-certifier`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-margin-endpoint-certifier/SKILL.md)
- **Mode:** Generative estimate design + certificate audit
- **Description:** Attack Route A modules G4, E1, and E2 by seeking strict reduced-margin certificates and regulator-derived endpoint estimates with two-sided error bounds.
- **Conceptual role:** This skill turns strictness and endpoint claims into explicit lower-bound, color-factor, cumulant, and tail-bound obligations.
- **Workflow shape:** Define cutoff-dependent margins; choose lower-bound route; derive endpoint boxes and color/incidence factors; prove two-sided endpoint error; classify certificates as positive, negative, or inconclusive.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-margin-endpoint-certifier/agents/openai.yaml)
- **Outputs:** Return: margin certificate, endpoint derivation, two-sided error bound, certificate classification, and manuscript patch.
- **Failure/demotion:** Demote if nonnegativity is treated as strict positivity, endpoint signs are ansatz-derived, or one-sided bounds are used as negative certificates.

#### `routea-continuum-gap-gatekeeper`

- **Skill file:** [Open skill](../../skills/results_ellaboration/routea-continuum-gap-gatekeeper/SKILL.md)
- **Mode:** Claim-boundary audit
- **Description:** Guard Route A modules M1 and M2 by testing whether any finite, geometric, or endpoint result can legitimately feed into OS reconstruction or a Hamiltonian spectral-gap claim.
- **Conceptual role:** This skill keeps the finite paper honest about the Clay-level commitments.
- **Workflow shape:** Name source and target objects; test transfer theorem status; list missing OS axioms; audit circularity; emit paper-safe wording.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/routea-continuum-gap-gatekeeper/agents/openai.yaml)
- **Outputs:** Return: source object, target object, transfer status, missing axioms, circularity audit, and paper-safe wording.
- **Failure/demotion:** Demote if finite positivity is promoted into reconstruction, endpoint estimates are promoted into mass gap, or the same continuum theory is not identified.

#### `results-context-interpreter`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-context-interpreter/SKILL.md)
- **Mode:** Generative agent
- **Description:** Interpret a paper draft as a result-bearing argument context. Use when a marked manuscript needs its theorem spine, claim boundary, section roles, expansion slots, non-claims, and mathematical objects made explicit before any result expansion is attempted.
- **Conceptual role:** This is the paper-context grounding skill. It prevents the expansion workflow from treating every marker as an isolated TODO by first asking what contribution the manuscript is actually trying to make.
- **Workflow shape:** Extract title, abstract, contribution statement, theorem spine, non-claims, result slots, and section roles; distinguish proved finite results from conditional application claims; identify which manuscript claims depend on each expansion marker; return a context packet that downstream skills can cite.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-context-interpreter/agents/openai.yaml)
- **Outputs:** Return: paper identity, bounded contribution, explicit non-claims, mathematical objects, section map, expansion markers, slot dependencies, and context warnings.
- **Validation handoff:** Hand off to `results-extension-need-extractor`; the context packet is valid only if every expansion marker can be located in the manuscript and every non-claim is preserved.
- **Failure/demotion:** Demote the context if it silently upgrades conditional claims into theorems, merges finite and continuum claims, or cannot name the local mathematical object of the paper.

#### `results-open-module-decomposer`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-open-module-decomposer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Decompose paper open-module environments or forward-work blocks into precise result-extension obligations. Use when a manuscript already contains a finite result and names open modules such as geometric family, normalization, coefficient extraction, endpoint bounds, continuum reconstruction, or spectral gap.
- **Conceptual role:** This skill handles mature manuscripts where the key task is not slot filling but disciplined conversion of open modules into publishable next-result targets.
- **Workflow shape:** Extract every open module; classify it by mathematical role; split deterministic checks from generative proof work; generate self-contained TODOs with validation handoffs, paper insertion targets, and explicit demotion boundaries.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-open-module-decomposer/agents/openai.yaml)
- **Outputs:** Return: extracted modules, module taxonomy, deterministic checks, generative proof-plan tasks, dependency graph, ordered TODOs, paper insertion targets, critical self-refinement prompts, and validation handoff.
- **Validation handoff:** Hand off to `results-critical-self-refiner` and `results-expansion-validator`.
- **Failure/demotion:** Demote any module plan that promotes finite source-collision algebra into geometric collar collapse, finite reflection positivity into OS reconstruction, or endpoint estimates into spectral claims.

#### `results-critical-self-refiner`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-critical-self-refiner/SKILL.md)
- **Mode:** Generative agent
- **Description:** Critically self-refine a result-elaboration plan by testing whether TODOs are paper-specific, mathematically typed, regime-separated, claim-bounded, and capable of feeding back into the manuscript narrative.
- **Conceptual role:** This is the reflective quality gate that prevents polished TODOs from becoming generic worklists or overclaiming routes.
- **Workflow shape:** For each TODO, identify the mathematical object changed by success; split deterministic validation from generative proof work; audit paper insertion points; test for source-collision/geometric-collar, finite/continuum, endpoint/spectral, and reflection-positivity/mass-gap overclaims.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-critical-self-refiner/agents/openai.yaml)
- **Outputs:** Return: refined TODOs, rejected/generic TODOs, claim-boundary warnings, deterministic/generative split audit, paper-integration audit, and next executable validation command.
- **Validation handoff:** Hand off to `results-expansion-validator` and, when applicable, TeX compilation or exact symbolic scripts.
- **Failure/demotion:** Reject TODOs whose acceptance criterion is only "expand this section" or "prove the needed theorem" without naming the object, estimate, certificate, and manuscript insertion point.

#### `results-extension-need-extractor`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-extension-need-extractor/SKILL.md)
- **Mode:** Generative agent
- **Description:** Convert manuscript expansion markers into typed result-extension needs. Use after context interpretation when slots, placeholders, or editorial markers must become precise obligations with required inputs, evidence standards, and replacement criteria.
- **Conceptual role:** This skill turns vague expansion markers into research-editing obligations: theorem completion, coefficient extraction, same-theory transfer, finite application, prior-art boundary, narrative integration, or submission cleanup.
- **Workflow shape:** Read the interpreted paper context; classify each marker by result type; identify the missing theorem, calculation, definition, literature boundary, or narrative bridge; state the minimum artifact that would replace the marker; record dependencies and validation handoffs.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-extension-need-extractor/agents/openai.yaml)
- **Outputs:** Return: typed extension needs, source markers, required inputs, acceptable evidence, replacement criteria, dependency hints, and claim-boundary risks.
- **Validation handoff:** Hand off to `results-extension-strategy-planner`; every need must be traceable to a source marker and have an explicit completion criterion.
- **Failure/demotion:** Demote any need that is generic, lacks a source marker, cannot state what manuscript text would replace it, or asks the discovery loop to solve a new open-ended problem.

#### `results-extension-strategy-planner`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-extension-strategy-planner/SKILL.md)
- **Mode:** Generative agent
- **Description:** Order typed extension needs into a self-contained result-elaboration plan. Use when a paper draft needs concrete TODOs with dependencies, local hooks, validation criteria, and stop or quarantine conditions.
- **Conceptual role:** This is the planning layer for manuscript-result completion. It decides which expansion should be attempted first because it unlocks the paper contribution, and which work should remain conditional or quarantined.
- **Workflow shape:** Rank extension needs by paper payoff, dependency depth, and claim-boundary risk; generate detailed TODOs with subtasks, expected artifacts, validation handoffs, and local workflow hooks; keep proof-completion tasks separate from narrative and prior-art tasks; explicitly avoid discovery-marathon hooks.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-extension-strategy-planner/agents/openai.yaml)
- **Outputs:** Return: ordered TODO queue, dependencies, acceptance criteria, validation handoffs, stop/quarantine conditions, local hook points, and skill handoffs.
- **Validation handoff:** Hand off to `results-expansion-validator`; every TODO must be actionable without hidden prior context and must preserve the manuscript's bounded contribution.
- **Failure/demotion:** Demote plans that depend on long-horizon discovery queues, lack artifact-level acceptance criteria, or turn a paper expansion into an unbounded research program.

#### `results-theorem-scope-certifier`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-theorem-scope-certifier/SKILL.md)
- **Mode:** Generative agent
- **Description:** Certify the smallest honest theorem or proposition that a result-elaboration effort can claim. Use when a manuscript, report, or nearly completed subgoal risks drifting from a local finite theorem, obstruction, method, or transfer lemma into a main-problem claim.
- **Conceptual role:** This is the claim-boundary skill for recurring result work. It turns "this looks paper-like" into a precise theorem-scope packet with covered cases, excluded cases, hypotheses, non-claims, and promotion boundaries.
- **Workflow shape:** Read the candidate result and its evidence; identify the theorem object, ambient setting, quantifiers, hypotheses, conclusion, and non-claims; separate finite/local/conditional claims from continuum/global/main-problem claims; state what extra proof debt is needed before any stronger claim is licensed.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-theorem-scope-certifier/agents/openai.yaml)
- **Outputs:** Return: theorem-scope ID, smallest honest claim, covered domain, excluded domain, assumptions, non-claims, proof obligations, promotion boundary, demotion triggers, and manuscript insertion target.
- **Validation handoff:** Hand off to `results-finite-object-formalizer` and `results-proof-packet-deriver`; fail if the claim cannot name its mathematical object, quantifiers, hypotheses, or evidence basis.
- **Failure/demotion:** Demote any scope packet that quietly turns a method-class theorem into a full proof-system theorem, a finite obstruction into a target-problem result, or a conditional construction into an unconditional claim.

#### `results-finite-object-formalizer`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-finite-object-formalizer/SKILL.md)
- **Mode:** Generative agent with deterministic validation handoff
- **Description:** Formalize the finite, local, or computable object that carries a result claim. Use when a paper-subgoal depends on a matrix, graph, gadget, transfer instance, obstruction witness, finite algebraic certificate, toy model, or minimal example that must be definition-ready before proof writing.
- **Conceptual role:** This skill prevents the argument from floating at the level of prose. It names the carrier object, admissible data, invariants, edge cases, and exact symbolic or computational checks needed for the proof packet.
- **Workflow shape:** Extract the candidate object; define its inputs, parameters, equivalence relations, allowed transformations, invariants, examples, counterexamples, deterministic checks, and generative interpretation; separate exact calculation from conceptual explanation.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-finite-object-formalizer/agents/openai.yaml)
- **Outputs:** Return: formal object definition, parameter table, invariant list, example family, edge-case tests, deterministic calculation hooks, proof obligations enabled by the object, and narrative role in the manuscript.
- **Validation handoff:** Hand off to symbolic/CAS scripts, exact calculators, or `results-proof-packet-deriver`; fail if the object cannot be instantiated, checked, or linked to the scoped theorem.
- **Failure/demotion:** Demote objects that are only analogies, hide regulator or model choices, lack invariant-preservation conditions, or cannot state what calculation or proof step they support.

#### `results-proof-packet-deriver`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-proof-packet-deriver/SKILL.md)
- **Mode:** Generative proof skill with deterministic check handoff
- **Description:** Derive a proof packet for a scoped result. Use when a theorem-scope packet and formal object exist and the next recurring work is to produce lemma order, proof skeleton, exact derivations, local calculations, contradiction/impossibility branches, and explicit remaining proof debt.
- **Conceptual role:** This is the proof-construction bridge between result planning and manuscript writing. It forces the work to become lemmas, equations, cases, estimates, and falsifiers rather than narrative confidence.
- **Workflow shape:** Build the lemma spine; identify definitions used at each step; derive the central calculation or implication; mark deterministic checks; generate contradiction or impossibility subroutes when direct proof is brittle; localize unresolved steps and state exactly whether they block publication.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-proof-packet-deriver/agents/openai.yaml)
- **Outputs:** Return: theorem restatement, lemma spine, derivation steps, exact calculations or symbolic obligations, contradiction branches, unresolved gaps, proof-debt severity, and manuscript-ready proof insertion plan.
- **Validation handoff:** Hand off to `results-prior-art-disqualifier-auditor`, deterministic proof/calculation scripts, and `results-paper-readiness-gatekeeper`.
- **Failure/demotion:** Demote packets that skip definitions, depend on unstated generic principles, hide quantifier changes, or cannot distinguish a proved lemma from a plausible proof strategy.

#### `results-prior-art-disqualifier-auditor`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-prior-art-disqualifier-auditor/SKILL.md)
- **Mode:** Generative review skill
- **Description:** Audit a scoped result against prior art, known barriers, disqualifiers, and near-duplicate claims. Use before calling a subgoal publishable, especially when the contribution may be a finite obstruction, method transfer, negative result, benchmark, proof-system lemma, or conceptual reframing.
- **Conceptual role:** This is the novelty and humility gate. It asks whether the result is actually new, whether it is merely a restatement of known machinery, and which barrier or non-claim must be visible in the paper.
- **Workflow shape:** State the claimed novelty; compare it against adjacent known results and standard methods; identify disqualifiers, barrier collisions, overclaim risks, and missing references; decide whether the contribution survives as a theorem, note, appendix, benchmark, or should be demoted.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-prior-art-disqualifier-auditor/agents/openai.yaml)
- **Outputs:** Return: novelty claim, closest prior-art classes, disqualifier matrix, barrier status, citation targets, surviving contribution statement, demotion language, and next verification needs.
- **Validation handoff:** Hand off to citation/reference tooling when available and to `results-paper-readiness-gatekeeper`; fail if the claim has no named novelty axis or no explicit prior-art boundary.
- **Failure/demotion:** Demote claims that are subsumed by standard theorems, collapse under known barriers, require uncited folklore, or need a stronger theorem than the proof packet actually establishes.

#### `results-paper-readiness-gatekeeper`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-paper-readiness-gatekeeper/SKILL.md)
- **Mode:** Generative gatekeeper
- **Description:** Decide whether a scoped result is ready to become a paper section, short note, appendix result, or still needs repair. Use after theorem scope, formal object, proof packet, and prior-art audit are available.
- **Conceptual role:** This is the final recurring paper-subgoal gate. It prevents infinite elaboration while also preventing premature claims: good enough means bounded, proved or explicitly conditional, novel enough, narratively coherent, and clear about what it does not solve.
- **Workflow shape:** Inspect theorem scope, proof completeness, object formalization, novelty, explanatory value, manuscript integration, and open debt; assign a readiness verdict; prescribe the smallest next repair set or the manuscript handoff structure.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-paper-readiness-gatekeeper/agents/openai.yaml)
- **Outputs:** Return: readiness verdict, required repairs, paper form, contribution paragraph, section outline, unresolved-debt disclosure, stop/continue decision, and handoff instructions for narrative integration.
- **Validation handoff:** Hand off to `results-narrative-integrator`, TeX compilation, and result-specific validators; fail if the result cannot be explained as a bounded contribution to an expert reader.
- **Failure/demotion:** Demote to exploratory note or internal result if the proof packet is incomplete, novelty is unclear, the object is underdefined, or the claimed value depends on solving a stronger open problem.

#### `results-narrative-integrator`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-narrative-integrator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Integrate result extensions into a coherent explanatory paper narrative. Use when theorem, computation, transfer, prior-art, and application expansions need to improve the manuscript rather than merely fill slots.
- **Conceptual role:** This skill protects the scientific story of the paper. It explains why each expansion matters, where it belongs in the argument, and how it changes the abstract, introduction, theorem statement, application section, or conclusion.
- **Workflow shape:** Build a narrative spine from the context packet; assign each TODO to a manuscript role; state how completing or demoting each expansion changes the paper's claim; define explanatory transitions between finite theorem, Wilson application, same-theory transfer, coefficients, remainders, and non-claims.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-narrative-integrator/agents/openai.yaml)
- **Outputs:** Return: narrative spine, section-level integration plan, contribution consequences, abstract/introduction/conclusion updates, and demotion language for unresolved expansions.
- **Validation handoff:** Hand off to `results-expansion-validator`; narrative integration is valid only when a reader can understand the contribution without seeing the expansion markers.
- **Failure/demotion:** Demote narrative edits that read like a task list, hide proof debt, omit explanatory motivation, or make the paper sound more complete than the validated results allow.

#### `results-expansion-validator`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-expansion-validator/SKILL.md)
- **Mode:** Generative agent
- **Description:** Validate the result-elaboration packet for marker coverage, TODO self-containment, local-hook compliance, claim-boundary preservation, and narrative coherence. Use before accepting a paper-result expansion plan or using it to edit a manuscript.
- **Conceptual role:** This is the quality gate for the separate result-elaboration workflow. It ensures that expansion planning is rigorous without accidentally coupling to the discovery control plane.
- **Workflow shape:** Check that every marker has a typed need and TODO; verify that every TODO has dependencies, subtasks, acceptance criteria, validation handoff, and stop/quarantine condition; audit forbidden discovery couplings; test whether the narrative spine preserves non-claims and bounded contribution.
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-expansion-validator/agents/openai.yaml)
- **Outputs:** Return: pass/fail decision, coverage table, missing fields, claim-boundary risks, hook-compliance verdict, and required repairs.
- **Validation handoff:** Run the deterministic validator when a JSON report exists, then perform a generative check for narrative and claim-boundary quality.
- **Failure/demotion:** Fail the packet if any expansion marker is uncovered, TODOs are not self-contained, local hooks are missing, forbidden discovery hooks are present, or paper claims exceed evidence.

#### `results-elaboration-workflow-orchestrator`

- **Skill file:** [Open skill](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/SKILL.md)
- **Mode:** Scripted + generative workflow
- **Description:** Coordinate the independent result-elaboration workflow over a paper draft. Use when a manuscript with expansion markers needs a complete interpretation, typed extension-needs extraction, ordered TODO generation, narrative integration, and validation.
- **Conceptual role:** This is the standalone workflow entrypoint. It invokes the result-elaboration skills in order and writes inspectable reports without mutating discovery workflows or marathon queues.
- **Workflow shape:** Run context interpretation; extract typed extension needs; plan ordered TODOs; integrate the paper narrative; validate coverage and hook compliance; write Markdown and JSON reports under the result-elaboration report directory.
- **Scripts:** [analyze_result_expansion.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/analyze_result_expansion.py), [validate_result_expansion_report.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/validate_result_expansion_report.py), [analyze_openmodule_expansion.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/analyze_openmodule_expansion.py), [validate_openmodule_expansion_report.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/validate_openmodule_expansion_report.py), [compute_three_hairpin_certificate.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/compute_three_hairpin_certificate.py), [implement_result_todos.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/implement_result_todos.py), [verify_routea_three_hairpin_block.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/verify_routea_three_hairpin_block.py), [integrate_routea_certificate.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/integrate_routea_certificate.py), [implement_routea_openmodule_todos.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/implement_routea_openmodule_todos.py), [implement_routea_paper_attack_todos.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/implement_routea_paper_attack_todos.py), [validate_routea_edge_paths.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/validate_routea_edge_paths.py), [render_routea_path_diagram.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/render_routea_path_diagram.py), [check_schur_factor_candidates.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/check_schur_factor_candidates.py), [evaluate_routea_finite_margins.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/evaluate_routea_finite_margins.py), [derive_routea_endpoint_incidence.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/derive_routea_endpoint_incidence.py), [certify_routea_endpoint_error_budget.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/certify_routea_endpoint_error_budget.py), [integrate_routea_second_wave_results.py](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/integrate_routea_second_wave_results.py)
- **Agent config:** [openai.yaml](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/agents/openai.yaml)
- **References:** [workflow-hooks.md](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/references/workflow-hooks.md), [todo-taxonomy.md](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/references/todo-taxonomy.md)
- **Outputs:** Return: report paths, context packet, extension needs, ordered TODOs, narrative spine, local hook map, forbidden-coupling audit, and validation result.
- **Validation handoff:** Run the report validator and inspect the generated Markdown for self-contained TODOs and manuscript-specific narrative consequences.
- **Failure/demotion:** Demote the workflow if it omits markers, emits generic tasks, lacks local hooks, couples to discovery workflows, or fails to state what completing each TODO would change in the manuscript.

### review

Multi-persona review skills for logic, epistemology, discovery science, mathematical depth, and system design.

#### `review-reasoner`

- **Skill file:** [Open skill](../../skills/review/review-reasoner/SKILL.md)
- **Mode:** Generative agent
- **Description:** Run a multi-perspective, code-first review of the reasoner under five critical lenses: an epistemologist of mathematical discovery, a Fields Medalist mathematician, a DeepMind-style mathematical discovery scientist, a concept-discovery logician, and a radically out-of-the-box systems designer. Use when the user wants a deep review of how the reasoner actually works, where it fails, how the epistemic process is encoded in code, or how the architecture should change.
- **Conceptual role:** This is the macro review skill for the reasoner as an implemented system. It is not a document reviewer. It is a code-and-state reviewer.
- **Workflow shape:** Inspect the actual control path:; Review the reasoner through all five lenses listed in [reviewer-stack.md](../../skills/review/review-reasoner/references/reviewer-stack.md).; For each lens:; Compare the lenses:; End with a prioritized redesign agenda:
- **Agent config:** [openai.yaml](../../skills/review/review-reasoner/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/review/review-reasoner/references/prompt-template.md), [reviewer-stack.md](../../skills/review/review-reasoner/references/reviewer-stack.md)
- **Outputs:** present findings first, ordered by severity;; cite actual files, modules, tests, and artifacts;; separate epistemic defects from mathematical defects from systems defects;; distinguish implemented capability from aspirational documentation;; end with convergence, disagreement, and recommended next interventions.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote claims on unsupported evidence, broken invariants, hidden assumptions, counterexamples, or scope overreach.

#### `review-reasoner-concept-logician`

- **Skill file:** [Open skill](../../skills/review/review-reasoner-concept-logician/SKILL.md)
- **Mode:** Generative agent
- **Description:** Review the reasoner as an epistemology and logic expert in concept discovery. Use when the user wants a code-first assessment of how the system forms, revises, types, compares, and stabilizes concepts, bridge objects, abstractions, representation shifts, and semantic equivalences.
- **Conceptual role:** Review the reasoner as a machine for concept discovery and abstraction control.
- **Agent config:** [openai.yaml](../../skills/review/review-reasoner-concept-logician/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/review/review-reasoner-concept-logician/references/prompt-template.md)
- **Outputs:** whether concepts are genuinely discovered or merely renamed gaps;; how equivalence and incompatibility are handled;; where representation shifts are needed;; what the system currently cannot conceptualize.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote claims on unsupported evidence, broken invariants, hidden assumptions, counterexamples, or scope overreach.

#### `review-reasoner-discovery-scientist`

- **Skill file:** [Open skill](../../skills/review/review-reasoner-discovery-scientist/SKILL.md)
- **Mode:** Generative agent
- **Description:** Review the reasoner as a DeepMind-style scientist of mathematical discovery systems. Use when the user wants a code-first assessment of the search decomposition, routing, memory, evaluation, branch execution, reward signals, and overall research-system design behind the reasoner.
- **Conceptual role:** Review the reasoner as an implemented research system for mathematical discovery.
- **Agent config:** [openai.yaml](../../skills/review/review-reasoner-discovery-scientist/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/review/review-reasoner-discovery-scientist/references/prompt-template.md)
- **Outputs:** search quality;; branch diversity and replay;; memory reuse;; evaluation discipline;; what the architecture learns versus what it only stores.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote claims on unsupported evidence, broken invariants, hidden assumptions, counterexamples, or scope overreach.

#### `review-reasoner-epistemologist`

- **Skill file:** [Open skill](../../skills/review/review-reasoner-epistemologist/SKILL.md)
- **Mode:** Generative agent
- **Description:** Review the reasoner as an epistemologist specialized in mathematical discovery. Use when the user wants a code-first assessment of whether the system earns its claims, licenses assertions correctly, distinguishes evidence from organization, and applies enough falsification pressure in discovery and proof.
- **Conceptual role:** Review the reasoner as a system of mathematical knowledge production. Inspect whether it is actually learning, or just building structured stories.
- **Workflow shape:** Inspect how theorem grounding and assertion licensing are implemented.; Inspect where evidence is gathered, scored, imported, or merely inferred.; Inspect whether blocked results, negative findings, and counterexample pressure materially change the search.; Inspect stop rules, continuation rules, and reward-sensitive control.; Judge whether the system mistakes coherence, novelty, or rich artifacts for evidence.
- **Agent config:** [openai.yaml](../../skills/review/review-reasoner-epistemologist/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/review/review-reasoner-epistemologist/references/prompt-template.md)
- **Outputs:** what the reasoner genuinely knows how to justify;; where it overclaims;; where epistemic discipline is strongest;; where the system still lacks decisive tests.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote claims on unsupported evidence, broken invariants, hidden assumptions, counterexamples, or scope overreach.

#### `review-reasoner-fields-medalist`

- **Skill file:** [Open skill](../../skills/review/review-reasoner-fields-medalist/SKILL.md)
- **Mode:** Generative agent
- **Description:** Review the reasoner as a Fields Medalist mathematician. Use when the user wants a code-first assessment of whether the mathematical objects, proof burdens, abstractions, route lemmas, and generated claims are mathematically substantive rather than merely schematic.
- **Conceptual role:** Review the reasoner as an expert mathematician would: is there real mathematics here, or only scaffolding around open problems?
- **Agent config:** [openai.yaml](../../skills/review/review-reasoner-fields-medalist/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/review/review-reasoner-fields-medalist/references/prompt-template.md)
- **Outputs:** mathematical sharpness of objects and lemmas;; whether subresults would interest experts independently;; where the route collapses into placeholders;; what mathematical strengthening is needed next.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote claims on unsupported evidence, broken invariants, hidden assumptions, counterexamples, or scope overreach.

#### `review-reasoner-radical-designer`

- **Skill file:** [Open skill](../../skills/review/review-reasoner-radical-designer/SKILL.md)
- **Mode:** Generative agent
- **Description:** Review the reasoner as a radically out-of-the-box systems designer. Use when the user wants a code-first critique of the agent ecology, interaction language, control loops, visualization strategy, hidden state, and overall design assumptions, together with bold but technically grounded redesign proposals.
- **Conceptual role:** Review the reasoner as a system that may be constrained by its own interface language, control decomposition, and visibility choices.
- **Agent config:** [openai.yaml](../../skills/review/review-reasoner-radical-designer/agents/openai.yaml)
- **References:** [prompt-template.md](../../skills/review/review-reasoner-radical-designer/references/prompt-template.md)
- **Outputs:** hidden design assumptions;; alternative decompositions of the process;; better ways to represent debt, branches, and conceptual change;; bold redesigns that still preserve inspectability.
- **Validation handoff:** End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
- **Failure/demotion:** Demote claims on unsupported evidence, broken invariants, hidden assumptions, counterexamples, or scope overreach.

## Shared Common Modules

These modules are not invocable skills. They provide typed contracts, queue logic, logging, discovery calculus, KB parsing helpers, and proof/discovery support used by the executable skill layer.

| Module | Description | Public API Snapshot |
|---|---|---|
| [abstraction_formal_reasoning.py](../../skills/common/abstraction_formal_reasoning.py) | Finite executable category, HoTT term/fiber, physical-diagram, countermodel, and five-arm condition-forger semantics. | functions: `callable_digest`, `build_negative_witness`, `validate_negative_witness`, `build_category_model_and_witness`, `validate_category_model`, `build_hott_model_and_witness`, `validate_hott_model`, `build_physical_diagram_and_witness`, `validate_physical_diagram`, `run_condition_forger`, `validate_condition_forger_result` |
| [abstraction_parallel_evaluation.py](../../skills/common/abstraction_parallel_evaluation.py) | Same-suite isolated five-arm abstraction calibration with replayable request, seed, cell, executable, output, evaluator, failure, dissent, and authority bindings. | functions: `blinded_structural_projection`, `blinded_structural_score`, `run_abstraction_parallel_evaluation`, `validate_abstraction_parallel_evaluation` |
| [contracts.py](../../skills/common/contracts.py) | Lightweight artifact contract validation for KB skill interoperability. | functions: `validate_phyp`, `validate_connection_analysis`, `validate_entrypoints`, `validate_pathways`, `validate_bridges`, `validate_coherence_report`, `validate_conjecture_report`, `validate_strategy_report`, `validate_proof_sketch_report` |
| [discovery_branch_queue.py](../../skills/common/discovery_branch_queue.py) | Persistent discovery-branch state for routed conceptual search layers. | functions: `discovery_branch_paths`, `discovery_branch_dossier_dir`, `default_discovery_branch_state`, `load_discovery_branch_state`, `render_discovery_branch_markdown`, `save_discovery_branch_state`, `select_discovery_branches`, `record_discovery_branch_execution`, `materialize_discovery_branches`, `build_discovery_branch_dossier`, `render_discovery_branch_dossier_markdown`, `write_discovery_branch_dossiers` |
| [discovery_calculus.py](../../skills/common/discovery_calculus.py) | Typed discovery-calculus prototype for bounded non-LLM search. | classes: `BridgeShape`, `RouteSignature`, `SearchReadiness`, `DiscoveryCandidate`; functions: `assess_symbolic_search_readiness`, `enumerate_bridge_shapes`, `build_candidates_for_shapes`, `bounded_bridge_search` |
| [discovery_lens_heuristic.py](../../skills/common/discovery_lens_heuristic.py) | Heuristics for routing discovery into category-theoretic or HoTT lenses. | functions: `build_categorical_pathway_heuristic`, `build_hott_pathway_heuristic` |
| [end_to_end_plausibility.py](../../skills/common/end_to_end_plausibility.py) | Shared end-to-end proof plausibility assessment utilities. | functions: `load_attempts`, `load_plausibility_inputs`, `build_plausibility_report`, `build_plausibility_report_from_artifacts`, `render_plausibility_markdown` |
| [expert_packet_fields.py](../../skills/common/expert_packet_fields.py) | Shared normalization helpers for expert-grade theorem packets. | functions: `normalize_expert_packet_fields` |
| [high_reward_watch.py](../../skills/common/high_reward_watch.py) | Persistent watch-state for high-value intermediate results that justify continued work. | functions: `high_reward_watch_paths`, `default_high_reward_watch`, `load_high_reward_watch`, `render_high_reward_watch_markdown`, `save_high_reward_watch`, `append_high_reward_signal`, `update_signal_status`, `signal_live_followups`, `select_high_reward_signal_for_continuation` |
| [hypothesis_eval.py](../../skills/common/hypothesis_eval.py) | Shared utilities for evaluating proof hypotheses against KB artifacts. | functions: `load_hypothesis_evidence`, `load_coherence_signals`, `classify_verdict`, `load_kb_statements`, `load_hypothesis_payload`, `load_analysis_scores`, `evaluate_hypotheses`, `apply_results_to_payload`, `is_resolved_status` |
| [inference_diagnosis.py](../../skills/common/inference_diagnosis.py) | Shared context-vs-inference diagnosis utilities for persisted artifacts. | functions: `build_queue_inference_diagnosis`, `refresh_attempt_inference_diagnosis`, `summarize_inference_diagnoses` |
| [kb_context.py](../../skills/common/kb_context.py) | Utilities for resolving canonical KB references and artifact roots. | functions: `normalize_kb_ref`, `kb_ref_from_kb_filename`, `read_front_matter_kb_id`, `resolve_kb_reference`, `canonical_artifacts_dir`, `kb_ref_from_artifacts_dir` |
| [knowledge_source_policy.py](../../skills/common/knowledge_source_policy.py) | Shared policy for when to invoke local memory, local generative search, and external search. | functions: `build_knowledge_source_policy`, `render_knowledge_source_policy_markdown` |
| [lean_discovery.py](../../skills/common/lean_discovery.py) | Lean/Lake bridge for bounded discovery search. | functions: `ensure_lake_package`, `write_generated_search_module`, `run_lean_search` |
| [ym_abstraction_calibrations.py](../../skills/common/ym_abstraction_calibrations.py) | Registry-bound executable local YM false-positive and boundary calibration runners with planned-commission discipline and exact replay receipts. | functions: `run_ym_calibration`, `run_ym_calibration_matrix`, `validate_ym_calibration` |
| [mathematical_layers.py](../../skills/common/mathematical_layers.py) | Build parallel mathematical representations for theorem packets. | functions: `build_mathematical_layers` |
| [negative_route_heuristic.py](../../skills/common/negative_route_heuristic.py) | Shared heuristic for deciding when contradiction, negation, or impossibility routes are epistemically justified. | functions: `build_negative_route_heuristic` |
| [problem_mathlib.py](../../skills/common/problem_mathlib.py) | Problem-scoped InformalMathLib storage for informal proof cycles. | functions: `mathlib_root`, `mathlib_paths`, `default_mathlib`, `load_mathlib_index`, `save_mathlib_index`, `append_mathlib_result`, `write_mathlib_entry_file`, `write_mathlib_result_file`, `render_mathlib_catalog`, `search_mathlib` |
| [proof_discovery_language.py](../../skills/common/proof_discovery_language.py) | Shared specification for a proof-discovery language. | functions: `serialize_queue_entry_as_pdl`, `serialize_discovery_branch_as_pdl`, `serialize_proof_attempt_as_pdl`, `render_pdl_program_markdown`, `build_language_spec`, `render_markdown`, `render_latex` |
| [proof_queue.py](../../skills/common/proof_queue.py) | Persistent proof-queue utilities for discovery/prove cycles. | functions: `proof_queue_paths`, `default_queue`, `load_proof_queue`, `save_proof_queue`, `queue_entry_selection_sort_key`, `make_queue_key`, `enqueue_entries`, `consume_next_entry`, `finalize_queue_entry`, `render_proof_queue_markdown` |
| [queue_entry_interpretability.py](../../skills/common/queue_entry_interpretability.py) | Assess whether a proof-queue entry is self-contained enough for LLM use. | functions: `assess_queue_entry_interpretability` |
| [reasoning_log.py](../../skills/common/reasoning_log.py) | Shared reasoning log utility for skill scripts. | classes: `ReasoningLogger` |
| [search_space_tree.py](../../skills/common/search_space_tree.py) | Shared helpers for persistent search-space tree signatures and history. | functions: `build_route_dimensions`, `route_signature`, `route_content_fingerprint`, `default_search_space_state`, `load_search_space_state`, `compute_revisit_signal` |
| [statement_text.py](../../skills/common/statement_text.py) | Utilities for normalizing theorem text and extracting theorem-body-grounded claim foci. | functions: `normalize_math_text`, `humanize_schema_label`, `statement_excerpt`, `statement_focus`, `load_statement_index` |

## Isolated Cohere-fast Orchestrator

- [`cohere-fast-orchestrator`](../../skills/cohere_fast/cohere-fast-orchestrator/SKILL.md) is an explicit-only control skill for the separate `cohere-fast <domain> [subworkflow]` route. Domain-private children are catalogued through `agentic/registries/domain_skill_bundles.yaml`, not exposed as global default skills.

## How To Read This Catalog

- **Mode** identifies whether the skill is mainly prompt-only, agent-backed, script-backed, or a hybrid.
- **Conceptual role** says why the skill exists in the epistemic workflow, not just what file it runs.
- **Framework contribution** states what pressure or control it adds to the long-horizon discovery system.
- **Validation handoff** names the next artifact, validator, proof obligation, or stop condition that should control the following loop when the skill itself describes one.
- Common modules are listed separately because they support skills but are not themselves invoked by users.
