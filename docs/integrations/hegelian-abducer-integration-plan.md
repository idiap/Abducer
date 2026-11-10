<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Solver Integration Plan

## Source Snapshot

The Hegelian Solver archive from `/Users/afreitas/Downloads/hegelian-solver.zip`
has been extracted as a clean source snapshot at:

- `external/hegelian-solver/`

The extraction intentionally excludes nested `.git`, `.venv`, `.pytest_cache`,
`__pycache__`, `__MACOSX`, and macOS `._*` files. The snapshot is source
material, not a runtime dependency.

## Integration Thesis

Hegelian Solver should not enter Abducer as an insular project, a second CLI, or
a parallel agent stack. Its useful contribution is a typed conceptual-control
layer for the exact place where Abducer already struggles: converting blocked
routes, bridge pressure, failed obligations, and conceptual gaps into disciplined
successor hypotheses, validation obligations, and continuation choices.

The native Abducer pipeline remains the main pipeline:

```text
KB grounding
  -> relational discovery
  -> bridge and abstraction planning
  -> proof-sketch and proof-queue compilation
  -> prove/disprove cycle
  -> InformalMathLib and blocked-result memory
  -> work-loop and Looper target governance
```

Hegelian Solver ideas should be adapted into this pipeline as:

```text
Abducer frontier or blocker
  -> hypothesis exploration map
  -> conceptual pressure packet
  -> failure / discovery signal / crisis formalization
  -> creative mediation or transformation hypothesis
  -> validation obligations and hard gates
  -> proof queue, discovery branch queue, or revision loop
  -> Looper dependency graph and release evidence
```

## Main Aim Alignment

The integration should sharpen Abducer's main aim: governed theorem discovery
through explicit exploration of a hypothesis space. The visible object is not a
generic philosophical reflection loop. It is an inspectable space of possible
mathematical continuations around a target:

- active conjectures and theorem-shaped route candidates,
- missing bridge objects and preservation lemmas,
- abstractions that may compress several routes into one concept,
- regime restrictions, weakenings, strengthenings, and counterexamples,
- proof obligations, source obligations, and disconfirming observations,
- blocked, quarantined, rejected, and promoted continuations.

Hegelian Solver contributes a discipline for moving through this space when the
current concepts are under pressure. Abducer contributes the target governance,
KB grounding, proof queue, evidence gates, and Looper visibility that keep this
creativity from becoming ungrounded narrative.

## Hypothesis Exploration And Conceptual Creativity

The adapted layer should represent conceptual creativity as controlled
transformations over Abducer artifacts. A candidate is creative only if it changes
the navigable hypothesis space in a way that can be inspected, challenged, and
validated.

Core creative operations should include:

| Operation | Abducer meaning | Required validation pressure |
| --- | --- | --- |
| Bridge invention | Introduce a relation, map, invariant, or mediator between disconnected KB regions. | Preservation obligations, non-collapse checks, source grounding, and proof-queue readiness. |
| Abstraction formation | Replace several repeated proof shapes or route fragments with a reusable concept. | Coverage witnesses, excluded cases, and entailment-gap analysis. |
| Regime restriction | Make a conjecture tractable by narrowing parameters, complexity classes, encodings, or assumptions. | Explicit lost generality, route value estimate, and counterfactual route check. |
| Theorem weakening | Relax an overstrong target into a provable or testable successor. | Proof relevance to the parent target and no hidden claim promotion. |
| Theorem strengthening | Add an invariant or sharper conclusion when evidence supports a stronger route. | Barrier compatibility and proof/disproof stress tests. |
| Carrier introduction | Introduce a new object that carries structure across proof stages. | Definition sufficiency, construction evidence, and downstream obligation fit. |
| Negative-route inversion | Turn a failed proof or counterexample into a successor hypothesis. | Failure certificate fidelity and repair-target specificity. |
| Analogy transport | Move a pattern from a source theorem family into the current target. | Source-domain limits, mismatch inventory, and non-collapse obligations. |
| Proof-obligation factorization | Split an opaque blocker into smaller lemmas, evidence tasks, or discovery branches. | Dependency graph update and stop-condition preservation. |
| Representation shift | Change the local ontology or proof vocabulary when existing concepts cannot express the route. | Revision trace, backward compatibility, and rejected-alternative record. |

The hypothesis exploration map should carry each candidate's creative role, the
pressure that motivated it, the artifact IDs it touches, the obligations it
creates, and the routing decision it changed. This makes conceptual creativity a
first-class Abducer control signal rather than a free-text explanation after the
fact.

## What To Reuse

Hegelian Solver has several ideas that fit Abducer directly.

| Hegelian idea | Abducer-native adaptation |
| --- | --- |
| `ConceptNode` | A typed view over a KB target, bridge object, theorem family, route concept, or proof-program state. |
| `FailureCertificate` | A formal blocker for proof debt, failed bridge transport, barrier mismatch, overstrong conjecture, or missing preservation lemma. |
| `DiscoverySignal` | A typed positive pressure from repeated proof shapes, shared abstractions, invariant patterns, or high-reward branch signals. |
| `TransformationCandidate` | A proposed route repair, bridge abstraction, regime restriction, strengthened theorem, weakened theorem, or new mediation object. |
| `Obligation` / `ValidationPacket` | Existing Abducer proof obligations plus hard gates: preservation, target activation, non-collapse, barrier compatibility, source grounding, and proof-queue readiness. |
| `RankingDecision` | A continuation decision for `work`: accept as proof queue, accept as discovery branch, defer, reject, or quarantine. |
| Reflective refinement loop | Bounded continuation over open obligations in `work`, not an unbounded retry loop. |
| Mechanism packets | A disciplined abductive layer for "what mediator would have to exist" before a bridge or abstraction can be treated as real. |
| Graph trace serializer | Extend Abducer process/dependency graphs with candidate, rejected, residual-limit, and mechanism edges. |

## What Not To Reuse Directly

- Do not import the Hegelian Solver CLI as the main entrypoint.
- Do not duplicate Abducer's skill tree under `agents/`.
- Do not make Pydantic a required dependency for the Looper proof gate unless
  the repo deliberately adopts it later.
- Do not treat Hegelian `accept` / `accept_as_branch` as mathematical proof.
- Do not use generic Hegelian operator names when Abducer has more precise
  mathematical route objects, proof obligations, or barrier labels.
- Do not let mechanism hypotheses bypass proof/disproof or source grounding.

## Native Abducer Insertion Points

### 1. Target And Dependency Closure

`agentic/scripts/build_target_dependency_graph.py` should gain typed
conceptual-pressure nodes derived from:

- open dependency frontier nodes,
- blocked proof queue entries,
- failed proof attempts,
- concept-gap abstractions,
- bridge-plan obligations,
- revision-loop blockers,
- InformalMathLib blocked local results.

This makes Hegelian-style pressure visible to Looper without a separate graph.

### 2. Relational Discovery

`kb-proof-connector`, `kb-coherence-evaluator`, and `kb-entrypoint-*` already
surface disconnected components, high-pressure links, and route candidates. The
integration should add a thin adapter that turns those outputs into:

- discovery signals,
- determinate failure certificates,
- preservation requirements,
- non-collapse risks.

This adapter should live in Abducer's `skills/discovery/` or `skills/evaluation/`
hierarchy, not under `external/`.

### 3. Bridge And Abstraction Planning

`kb-concept-bridge-planner` and `kb-gap-abstraction-conjecturer` are the most
natural homes for Hegelian mechanism reasoning. A candidate bridge should expose:

- commitments it preserves,
- incompatibility it mediates,
- missing relation or process,
- new predicates or maps,
- material or proof preconditions,
- disconfirming observations,
- validation obligations.

The output should still be Abducer artifacts: `bridge-plan.json`,
`concept-gap-abstractions.json`, and follow-on proof queue entries.

### 4. Proof Queue Compilation

`kb-discovery-cycle` should compile accepted conceptual candidates into
theorem-shaped units only when obligations are explicit enough. The rule should
be:

- candidate has proof-form obligations -> proof queue;
- candidate has missing mediator / unclear object -> discovery branch queue;
- candidate has hard-gate failure -> blocked result or revision loop;
- candidate depends on external/current evidence -> prior-art or evidence
  acquisition route.

### 5. Prove / Disprove Cycle

`kb-prove-cycle` and `work` already represent blocked routes and negative
arguments. Hegelian failure certificates should become a structured layer over
that material:

- failed obligation,
- witness,
- severity,
- repair target,
- unknowns,
- candidate successor route.

This gives the work loop better continuation choices than "try another proof"
or "stop".

### 6. Work Loop And Looper Governance

The bounded reflective refinement loop should be owned by Abducer's `work`
skill, not by the Hegelian orchestrator. The loop should reuse Abducer stop
conditions:

- resolved by proof/disproof,
- no candidates,
- no refinement triggers,
- plateau,
- max cycles,
- high-reward extension,
- Looper gate quarantine.

Looper should see each iteration as skill applications and dependency graph
updates, not as opaque external solver state.

## Proposed Artifact Contracts

The first integration should define lightweight JSON contracts under
`agentic/spec/` or `artifacts/<kb-ref>/`:

- `hypothesis_exploration_map`
- `conceptual_pressure_packet`
- `abducer_failure_certificate`
- `abducer_discovery_signal`
- `abducer_mediation_candidate`
- `conceptual_creativity_analysis`
- `abducer_validation_packet`
- `abducer_candidate_ranking`
- `conceptual_refinement_trace`

These contracts should be intentionally smaller than the Hegelian Pydantic
models. They should cite Abducer-native IDs: KB statement IDs, bridge IDs,
proof-queue IDs, dependency node IDs, InformalMathLib result IDs, and artifact paths.

## Skill Adaptation Plan

Do not copy all Hegelian agents. Instead, adapt their roles into a small set of
Abducer-native skills:

1. `abducer-conceptual-pressure-formalizer`
   - Converts frontier nodes and blocked proof results into typed pressure
     packets.
2. `abducer-failure-signal-cartographer`
   - Separates failure certificates from positive discovery signals.
3. `abducer-mediation-candidate-generator`
   - Proposes bridge, abstraction, regime, weakening, strengthening, or carrier
     candidates from pressure packets.
4. `abducer-obligation-gatekeeper`
   - Turns candidates into proof/source/transport/non-collapse obligations.
5. `abducer-refinement-route-ranker`
   - Chooses proof queue, discovery branch, revision, evidence acquisition,
     quarantine, or stop.

Existing skills remain primary:

- `kb-concept-bridge-planner`
- `kb-gap-abstraction-conjecturer`
- `kb-discovery-cycle`
- `kb-prove-cycle`
- `kb-revision-loop`
- `kb-end-to-end-proof-critic`
- `work`
- Looper control-plane skills

## Migration Sequence

### Phase 1: Source Mapping And Contracts

Inventory Hegelian schemas, agents, examples, and tests; map each useful concept
to an Abducer artifact and reject the rest explicitly. Define minimal Abducer
schemas and fixtures, including the hypothesis exploration map and conceptual
creativity analysis.

### Phase 2: Adapter Over Existing Artifacts

Build deterministic adapters that read existing Abducer artifacts and produce
conceptual pressure packets, failure certificates, discovery signals, and
validation packets without changing the proof pipeline.

### Phase 3: Skill-Level Generative Integration

Add focused prompt skills for interpreting pressure, candidate mediation, and
obligation sufficiency. These skills must cite Abducer artifacts and never
promote a candidate on narrative plausibility alone.

### Phase 4: Work Loop Routing

Teach `work` to consume candidate rankings and route each item to proof queue,
discovery branch queue, revision loop, evidence acquisition, or quarantine.

### Phase 5: Looper Visibility And Gates

Extend Looper dependency graphs, workflow manifests, skill logs, and promotion
gates so conceptual-refinement iterations are visible and auditable.

### Phase 6: Evaluation

Add deterministic and generative tests over P vs NP fixtures and at least one
small mathematical example. Acceptance requires improved routing of blocked
routes, not just new reports.

Validation must cover complex reasoning steps, not only schema shape:

- deterministic contract checks for required IDs, paths, blocker links, and
  Looper-visible dependency edges;
- replay checks showing the same evidence yields the same route disposition;
- metamorphic checks showing removed evidence demotes or quarantines a candidate;
- adversarial generative probes for attractive but ungrounded mediators;
- ablation checks comparing routes with and without the creativity layer;
- proof-queue safety checks confirming no creative candidate bypasses proof,
  source, non-collapse, or barrier obligations;
- reviewer-facing traces showing why a routing decision changed.

## Acceptance Bar

The integration is successful only when:

- Hegelian source material is traceable but not required as a separate runtime.
- New artifacts cite Abducer-native IDs and paths.
- Work-loop decisions change based on typed failure/signal/candidate evidence.
- The hypothesis exploration map records creative operations, obligations, and
  route dispositions as first-class objects.
- Proof queue and discovery branch queue receive better typed inputs.
- Looper dependency closure shows conceptual-refinement edges.
- Promotion gates reject candidates with unmet hard obligations.
- Tests demonstrate that blocked proof debt becomes either a refined proof
  target, a discovery branch, a revision TODO, an evidence task, or a justified
  stop condition.

## Immediate Deliverables

The structured TODO backlog lives at:

- `agentic/todos/hegelian_integration_todos.yaml`

The visible workflow registry entry lives at:

- `registry/tasks/hegelian-abducer-integration/task_registry.json`
