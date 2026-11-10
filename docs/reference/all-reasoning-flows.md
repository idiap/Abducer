<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# All reasoning flows

This single-file reference contains every canonical workflow represented in the Essential Reasoning Flow Language (ERFL). It is generated from the canonical flow catalog and the `.prism` sources; edit those sources rather than this file. Concrete illustrations are maintained in the physics-example registry.

Catalog coverage: **19 canonical flows**.

An underscore occurrence (`_`) is an unresolved projection gap. A gap-bearing flow is descriptive and non-executable; it does not license an inferred reasoning type.

Each interpreted line is paired with a concrete mathematical-physics example from `agentic/registries/reasoning_flow_physics_examples.yaml`. The examples illustrate semantics; they are not evidence that the stated physics result holds.

These are independent workflow illustrations, not one continuous research run. Gauge group, regulator, dimension, and claim scope must not be transported from one example to another unless explicitly restated.

## Reading long KB-grounded routes

The preamble binds a concrete KB for reading and versioned persistence. The steps must then consume the local handle explicitly. A trailing `...` continues the same logical statement, while indentation is visual only:

```text
erfl 0.3
@KB kb0 connect(file("KB/yang-mills-existence-and-mass-gap.kb.md"))
reasoning kb_grounded_route {
  goal "calibrate a KB-grounded route" -> reviewed
  steps e0:E[kb0,source->ground] -constrain> ...
      a0:A[ground->route] -assume> ...
      d0:D[route->claim] -test> ...
      r0:R[claim->verdict] -calibrate> ...
      e1:E[claim,verdict->status]
  e0 <-query- kb0
  e1 -persist-> kb0
  on e1.reviewed => accept
}
```

The KB declaration does not itself read, write, or validate any member. The inverted query arrow records consumption; the regular persistence arrow authorizes a calibrated successor. The five step lines parse as one statement; `...` changes only layout, not warrant.

## Reflective reasoning example

Reflection takes the system's own trace, claims, and obligations as its object. It is represented as calibration of the current reasoning state, abductive formation of a repair, and calibration of what the reflection actually supports:

```text
erfl 0.3
reasoning reflective_route_review {
  goal "explain why the active route stalled and propose a bounded repair" -> reflected
  steps e0:E[trace,claims,obligations->self_model] -revise> ...
        a0:A[self_model->repair] -calibrate> ...
        e1:E[self_model,repair->reflection_status]
  on e1.reflected => accept
  on e1.no_discriminating_repair => stop
}
```

Physics example: after repeated failure to obtain a cutoff-uniform spectral estimate, the system identifies hidden dependence on lattice spacing as the recurring failure pattern and proposes a bounded norm-uniformity audit. The repair remains abductive until tested.

## Meta-reasoning example

Meta-reasoning compares reasoning strategies and governs which one should run next. It evaluates a portfolio and its history rather than directly proving the object-level scientific claim:

```text
erfl 0.3
@KB kb0 connect(file("KB/yang-mills-existence-and-mass-gap.kb.md"))
reasoning meta_strategy_review {
  goal "select, revise, or stop the current reasoning strategy" -> governed
  steps e0:E[kb0,portfolio,trace->strategy_state] -constrain> ...
        (r0:R[strategy_state->defeaters] & a0:A[strategy_state->repairs]) -calibrate> ...
        e1:E[defeaters,repairs->meta_status]
  e0 <-search- kb0
  e1 -persist-> kb0
  on e1.strategy_selected => accept
  on e1.stop_justified => stop
}
```

Physics example: the meta layer compares a transfer-matrix route, a correlation-decay route, and a representation-first route against accumulated failures. It selects another bounded cycle only when a discriminating test and measurable obligation reduction are available.

Reflective and meta are higher-order roles here, not ninth and tenth primitive reasoning symbols. Their higher-order status comes from what their inputs denote and how the essential operations are composed.

## Whole-system predicate map

This projection collapses each detailed `steps` expression to its relation
signature. Named outputs mediate every connection to another reasoning
program. Indented arrows visually attach each output transition to the
reasoning program immediately above it:

```text
map abducer {
  reasoning::target_navigation_loop -requires> output::target_navigation_loop.target_status
       -> output::target_navigation_loop.target_status -> reasoning::abducer_work_loop
       -> output::target_navigation_loop.target_status -> reasoning::release_promotion_loop

  reasoning::discovery_marathon_loop -constrain, probe, test, calibrate> output::discovery_marathon_loop.discovery_status
       -> output::discovery_marathon_loop.discovery_status -> reasoning::release_promotion_loop
       -> output::discovery_marathon_loop.discovery_status -> reasoning::conceptual_hypothesis_exploration_loop
       -> output::discovery_marathon_loop.discovery_status -> reasoning::target_navigation_loop

  reasoning::abducer_work_loop -assume, test, calibrate> output::abducer_work_loop.work_status
       -> output::abducer_work_loop.work_status -> reasoning::release_promotion_loop
       -> output::abducer_work_loop.work_status -> reasoning::conceptual_hypothesis_exploration_loop
       -> output::abducer_work_loop.work_status -> reasoning::target_navigation_loop

  reasoning::conceptual_hypothesis_exploration_loop -constrain, transfer, assume, test, calibrate> output::conceptual_hypothesis_exploration_loop.refinement_status
       -> output::conceptual_hypothesis_exploration_loop.refinement_status -> reasoning::abducer_work_loop
       -> output::conceptual_hypothesis_exploration_loop.refinement_status -> reasoning::release_promotion_loop

  reasoning::release_promotion_loop -requires> output::release_promotion_loop.release_status
       -> output::release_promotion_loop.release_status -> reasoning::target_navigation_loop
       -> output::release_promotion_loop.release_status -> reasoning::conceptual_hypothesis_exploration_loop

  reasoning::evidence_to_proof_route_onramp -constrain, assume, calibrate, revise, test> output::evidence_to_proof_route_onramp.calibrated_route
       -> output::evidence_to_proof_route_onramp.calibrated_route -> reasoning::theorem_proof_delivery
       -> output::evidence_to_proof_route_onramp.calibrated_route -> reasoning::conceptual_hypothesis_exploration_loop

  reasoning::conceptual_frontier_deepening -constrain, test, calibrate, revise, assume> output::conceptual_frontier_deepening.calibrated_candidate
       -> output::conceptual_frontier_deepening.calibrated_candidate -> reasoning::theorem_proof_delivery
       -> output::conceptual_frontier_deepening.calibrated_candidate -> reasoning::conceptual_hypothesis_exploration_loop

  reasoning::theorem_proof_delivery -test, calibrate> output::theorem_proof_delivery.calibrated_proof_status
       -> output::theorem_proof_delivery.calibrated_proof_status -> reasoning::scientific_contribution_cultivation
       -> output::theorem_proof_delivery.calibrated_proof_status -> reasoning::conceptual_hypothesis_exploration_loop

  reasoning::scientific_contribution_cultivation -test, calibrate> output::scientific_contribution_cultivation.calibrated_contribution
       -> output::scientific_contribution_cultivation.calibrated_contribution -> reasoning::manuscript_result_elaboration

  reasoning::manuscript_result_elaboration -constrain, test, calibrate> output::manuscript_result_elaboration.calibrated_manuscript
       -> output::manuscript_result_elaboration.calibrated_manuscript -> reasoning::theorem_proof_delivery

  reasoning::deep_review_and_reorientation -constrain, calibrate> output::deep_review_and_reorientation.calibrated_reorientation
       -> output::deep_review_and_reorientation.calibrated_reorientation -> reasoning::target_navigation_loop
       -> output::deep_review_and_reorientation.calibrated_reorientation -> reasoning::conceptual_hypothesis_exploration_loop

  reasoning::timeline-paper-independent-workflow -requires> output::timeline-paper-independent-workflow.paper_status
       -> output::timeline-paper-independent-workflow.paper_status -> terminal

  reasoning::ym-representational-dynamics-overlay -requires> output::ym-representational-dynamics-overlay.overlay_status
       -> output::ym-representational-dynamics-overlay.overlay_status -> terminal

  reasoning::cohere_fast -requires> output::cohere_fast.calibrated_domain_result
       -> output::cohere_fast.calibrated_domain_result -> reasoning::cohere_fast_scope_and_ground

  reasoning::cohere_fast_scope_and_ground -requires> output::cohere_fast_scope_and_ground.scope_status
       -> output::cohere_fast_scope_and_ground.scope_status -> reasoning::cohere_fast_adaptive_frontier

  reasoning::cohere_fast_adaptive_frontier -requires> output::cohere_fast_adaptive_frontier.frontier_status
       -> output::cohere_fast_adaptive_frontier.frontier_status -> reasoning::cohere_fast_derivation_and_proof

  reasoning::cohere_fast_derivation_and_proof -requires> output::cohere_fast_derivation_and_proof.derivation_status
       -> output::cohere_fast_derivation_and_proof.derivation_status -> reasoning::cohere_fast_independent_audit

  reasoning::cohere_fast_independent_audit -calibrate> output::cohere_fast_independent_audit.audit_status
       -> output::cohere_fast_independent_audit.audit_status -> reasoning::cohere_fast_manuscript_release

  reasoning::cohere_fast_manuscript_release -requires> output::cohere_fast_manuscript_release.release_status
       -> output::cohere_fast_manuscript_release.release_status -> terminal
}
```

The predicate map is generated from the same canonical programs. Its focused reference is `docs/reference/reasoning-predicate-map.md`.

## Index

- [`target_navigation_loop`](#target-navigation-loop)
- [`discovery_marathon_loop`](#discovery-marathon-loop)
- [`abducer_work_loop`](#abducer-work-loop)
- [`conceptual_hypothesis_exploration_loop`](#conceptual-hypothesis-exploration-loop)
- [`release_promotion_loop`](#release-promotion-loop)
- [`evidence_to_proof_route_onramp`](#evidence-to-proof-route-onramp)
- [`conceptual_frontier_deepening`](#conceptual-frontier-deepening)
- [`theorem_proof_delivery`](#theorem-proof-delivery)
- [`scientific_contribution_cultivation`](#scientific-contribution-cultivation)
- [`manuscript_result_elaboration`](#manuscript-result-elaboration)
- [`deep_review_and_reorientation`](#deep-review-and-reorientation)
- [`timeline-paper-independent-workflow`](#timeline-paper-independent-workflow)
- [`ym-representational-dynamics-overlay`](#ym-representational-dynamics-overlay)
- [`cohere_fast`](#cohere-fast)
- [`cohere_fast_scope_and_ground`](#cohere-fast-scope-and-ground)
- [`cohere_fast_adaptive_frontier`](#cohere-fast-adaptive-frontier)
- [`cohere_fast_derivation_and_proof`](#cohere-fast-derivation-and-proof)
- [`cohere_fast_independent_audit`](#cohere-fast-independent-audit)
- [`cohere_fast_manuscript_release`](#cohere-fast-manuscript-release)

## target_navigation_loop

**Function:** calibrate a target and its dependency frontier, then route work or release

**Aliases:** `target-navigation-control-plane`, `p-vs-np-target-navigation-run`

**Projection status:** `gap_bearing_curated_abstraction`

**Source references:** `agentic/registries/workflow_contracts.yaml`, `registry/tasks/target-navigation/task_registry.json`, `registry/tasks/p-vs-np-target-navigation/task_registry.json`

**Fictional worked example:** A researcher starts with “explain a stable spectral
scale in a regulated gauge model.” This workflow turns that broad request into
explicit construction, uniformity, and reconstruction obligations; once the
dependency frontier is precise, `work_ready` transfers it to
`abducer_work_loop` without claiming that the target has been solved.

```erfl
erfl 0.2
reasoning target_navigation_loop {
  goal "produce a calibrated target and dependency frontier" -> target_status
  steps pre:_[raw_target->dependency_state] -requires> ...
        e0:E[dependency_state->target_status]
  on e0.work_ready => switch @abducer_work_loop
  on e0.release_candidate => switch @release_promotion_loop
  on reasoning.stalled => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following target_navigation_loop example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning target_navigation_loop {`

   Begins the canonical reasoning program named `target_navigation_loop`.

   **Physics context:** A four-dimensional SU(3) Yang–Mills programme must turn the broad mass-gap problem into a dependency frontier involving reflection positivity, a transfer operator, a uniform spectral estimate, and a controlled continuum limit.

3. `goal "produce a calibrated target and dependency frontier" -> target_status`

   Sets the epistemic objective to “produce a calibrated target and dependency frontier” and names the required resulting state `target_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The continuum target is a mass gap for the reconstructed infinite-volume theory. For a specified reflection-positive action, immediate lattice work defines Delta(a,L) = -a_t^{-1} log(lambda_1/lambda_0) in the gauge-invariant physical sector and seeks a positive lower bound uniform in spatial volume and cutoff along a stated bare-coupling trajectory, with continuum Osterwalder–Schrader reconstruction kept separate.

4. `steps pre:_[raw_target->dependency_state] -requires> e0:E[dependency_state->target_status]`

   Defines the main epistemic steps: `pre` marks an unresolved reasoning region that carries `raw_target` into `dependency_state`; no reasoning type is inferred for it; it then requires the next occurrence structurally; this dependency adds no evidential warrant, after which `e0` performs epistemic status calibration, consuming `dependency_state` and producing `target_status`.

   **Concrete physics example:** The unresolved target-analysis work converts the Clay Millennium existence-and-mass-gap target into an explicit dependency graph; that construction remains intentionally unclassified, and only the final status calibration is typed.

5. `on e0.work_ready => switch @abducer_work_loop`

   When `e0` (epistemic status calibration) reports `work_ready` (work ready), control switches to `abducer_work_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** For the Wilson action at fixed cutoff, reflection positivity and a positive self-adjoint transfer operator are established; proof work starts only after the physical sector, boundary conditions, energy normalization, volume limit, cutoff trajectory, and reconstruction obligations are explicit.

6. `on e0.release_candidate => switch @release_promotion_loop`

   When `e0` (epistemic status calibration) reports `release_candidate` (release candidate), control switches to `release_promotion_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** A rigorous finite-lattice spectral bound is complete and worth releasing as a bounded result, although it is not yet the continuum mass gap.

7. `on reasoning.stalled => stop`

   When the reasoning program as a whole reports `stalled` (stalled), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** No defensible bridge from finite lattice spacing to a uniform continuum estimate has been identified, so navigation stops instead of relabelling numerical evidence as proof.

8. `}`

   Ends the `target_navigation_loop` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## discovery_marathon_loop

**Function:** generate, probe, contrast, test, and calibrate bounded discovery candidates

**Aliases:** `discovery-marathon-control-loop`

**Projection status:** `curated_abstraction`

**Source references:** `agentic/registries/workflow_contracts.yaml`, `registry/tasks/discovery-marathon/task_registry.json`

**Fictional worked example:** A bounded run compares a disorder hypothesis and
a transfer-operator hypothesis using sampled patterns, a toy model, and a
controlled contrast. A failed discriminating prediction returns the candidate
to `conceptual_hypothesis_exploration_loop`; a surviving candidate proceeds to
`release_promotion_loop` only at its calibrated status.

```erfl
erfl 0.2
reasoning discovery_marathon_loop {
  goal "find a discriminating candidate across bounded discovery cycles" -> discovery_status
  steps e0:E[run_context->scope] -constrain> ...
        (a0:A[scope->candidate] & i0:I[scope->pattern]) -probe> ...
        (m0:M[candidate,pattern->model_result] & c0:C[candidate,pattern->contrast_result]) -test> ...
        r0:R[model_result,contrast_result->verdict] -calibrate> ...
        e1:E[candidate,pattern,verdict->discovery_status]
  on e1.promotable => switch @release_promotion_loop
  on e1.reorient => switch @conceptual_hypothesis_exploration_loop
  on e1.target_reset => switch @target_navigation_loop
  on reasoning.stalled => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following discovery_marathon_loop example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning discovery_marathon_loop {`

   Begins the canonical reasoning program named `discovery_marathon_loop`.

   **Physics context:** A hypothetical Yang–Mills discovery run compares gauge-invariant center-vortex or disorder observables, a precisely defined monopole-disorder construction, and gauge-fixed functional-renormalization-group propagator behavior as non-equivalent mechanism indicators rather than proofs of a physical mass gap.

3. `goal "find a discriminating candidate across bounded discovery cycles" -> discovery_status`

   Sets the epistemic objective to “find a discriminating candidate across bounded discovery cycles” and names the required resulting state `discovery_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The run seeks a candidate mechanism predicting decay of specified gauge-invariant connected correlators with finite-volume and cutoff dependence exposed, rather than merely restating confinement or a gauge-fixed propagator mass scale.

4. `steps e0:E[run_context->scope] -constrain> (a0:A[scope->candidate] & i0:I[scope->pattern]) -probe> (m0:M[candidate,pattern->model_result] & c0:C[candidate,pattern->contrast_result]) -test> r0:R[model_result,contrast_result->verdict] -calibrate> e1:E[candidate,pattern,verdict->discovery_status]`

   Defines the main epistemic steps: `e0` performs epistemic status calibration, consuming `run_context` and producing `scope`; it then uses the preceding state to narrow what the next occurrence may produce, after which all of these branches are required—branch 1: `a0` performs abductive hypothesis formation, consuming `scope` and producing `candidate`; branch 2: `i0` performs inductive generalization, consuming `scope` and producing `pattern`; it then examines the preceding candidate through a model or controlled contrast, after which all of these branches are required—branch 1: `m0` performs model-based reasoning, consuming `candidate` and `pattern` and producing `model_result`; branch 2: `c0` performs contrastive counterfactual reasoning, consuming `candidate` and `pattern` and producing `contrast_result`; it then subjects the preceding claim or candidate to critical testing, after which `r0` performs critical refutational testing, consuming `model_result` and `contrast_result` and producing `verdict`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e1` performs epistemic status calibration, consuming `candidate`, `pattern` and `verdict` and producing `discovery_status`.

   **Concrete physics example:** Prior evidence fixes SU(3), lattice spacing, volume, and observables; abduction proposes center-vortex disorder as the candidate; induction extracts volume-stable correlation-length scaling across ensembles; a reduced Z3 gauge model predicts a model correlation curve; a counterfactual suppresses vortex density while holding coupling and volume fixed and predicts the resulting change; refutation compares both predictions with the declared data; calibration records the bounded verdict.

5. `on e1.promotable => switch @release_promotion_loop`

   When `e1` (epistemic status calibration) reports `promotable` (promotable), control switches to `release_promotion_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** Across the declared lattice sizes, the measured gauge-invariant correlators are consistent with an upper correlation-length bound after statistical and systematic uncertainties; this is bounded nonrefutation and supports promotion only as an empirical candidate, not a volume-uniform theorem.

6. `on e1.reorient => switch @conceptual_hypothesis_exploration_loop`

   When `e1` (epistemic status calibration) reports `reorient` (reorient), control switches to `conceptual_hypothesis_exploration_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The candidate fits Wilson-loop data but fails its preregistered prediction for energies extracted from a gauge-invariant time-correlator matrix, so the programme returns to conceptual reorientation.

7. `on e1.target_reset => switch @target_navigation_loop`

   When `e1` (epistemic status calibration) reports `target_reset` (target reset), control switches to `target_navigation_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The proposed observable measures string tension rather than the required spectral gap, so the target definition itself must be repaired.

8. `on reasoning.stalled => stop`

   When the reasoning program as a whole reports `stalled` (stalled), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** All three mechanisms reproduce the same coarse observables and no discriminating test remains within budget, so the run stops with the ambiguity preserved.

9. `}`

   Ends the `discovery_marathon_loop` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## abducer_work_loop

**Function:** advance an active proof obligation from hypothesis through derivation and refutation

**Aliases:** None

**Projection status:** `curated_abstraction`

**Source references:** `agentic/registries/workflow_contracts.yaml`

**Fictional worked example:** A proof attempt lacks a bridge from correlation
decay to a sectoral energy bound. Abduction proposes a norm-controlled bridge,
deduction derives its conditional consequence, and refutation finds that one
boundary condition breaks it. The workflow therefore switches to conceptual
reframing instead of treating the attractive route as a theorem.

```erfl
erfl 0.2
reasoning abducer_work_loop {
  goal "advance or close the active proof obligation" -> work_status
  steps a0:A[proof_gap->route] -assume> ...
        d0:D[route->claim] -test> ...
        r0:R[claim->verdict] -calibrate> ...
        e0:E[claim,verdict->work_status]
  on e0.release_candidate => switch @release_promotion_loop
  on e0.reframe => switch @conceptual_hypothesis_exploration_loop
  on e0.retarget => switch @target_navigation_loop
  on r0.refuted => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following abducer_work_loop example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning abducer_work_loop {`

   Begins the canonical reasoning program named `abducer_work_loop`.

   **Physics context:** The active proof obligation is to derive a positive lower bound in physical energy units for the vacuum-orthogonal gauge-invariant transfer-operator spectrum, uniformly in spatial volume and as the cutoff is removed along a stated coupling trajectory.

3. `goal "advance or close the active proof obligation" -> work_status`

   Sets the epistemic objective to “advance or close the active proof obligation” and names the required resulting state `work_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The loop must either advance the uniform spectral-gap lemma, expose a counterexample or missing premise, or close the obligation at its honest claim level.

4. `steps a0:A[proof_gap->route] -assume> d0:D[route->claim] -test> r0:R[claim->verdict] -calibrate> e0:E[claim,verdict->work_status]`

   Defines the main epistemic steps: `a0` performs abductive hypothesis formation, consuming `proof_gap` and producing `route`; it then retains the preceding candidate explicitly as a premise for conditional reasoning, after which `d0` performs deductive entailment, consuming `route` and producing `claim`; it then subjects the preceding claim or candidate to critical testing, after which `r0` performs critical refutational testing, consuming `claim` and producing `verdict`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e0` performs epistemic status calibration, consuming `claim` and `verdict` and producing `work_status`.

   **Concrete physics example:** Abduction proposes a coercive or Poincare-type estimate for the physical transfer operator; deduction derives its conditional spectral consequence; refutation tests anisotropic spacings, boundary conditions, rough-plaquette regions, and configurations outside any declared small-plaquette chart; calibration records the exact usable regime.

5. `on e0.release_candidate => switch @release_promotion_loop`

   When `e0` (epistemic status calibration) reports `release_candidate` (release candidate), control switches to `release_promotion_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The estimate is proved at fixed cutoff and finite spatial volume under an explicit gauge-invariant small-plaquette or admissibility assumption, so it is releasable only as a conditional restricted estimate.

6. `on e0.reframe => switch @conceptual_hypothesis_exploration_loop`

   When `e0` (epistemic status calibration) reports `reframe` (reframe), control switches to `conceptual_hypothesis_exploration_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The estimate fails outside the declared admissibility bound; no topological interpretation is attached unless sectors were separately defined under that bound.

7. `on e0.retarget => switch @target_navigation_loop`

   When `e0` (epistemic status calibration) reports `retarget` (retarget), control switches to `target_navigation_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** Navigation should seek a uniform physical-sector contraction estimate or norm-controlled time-correlation bounds for a sufficiently comprehensive observable class; decay of one observable is not enough for a full gap.

8. `on r0.refuted => stop`

   When `r0` (critical refutational testing) reports `refuted` (refuted), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** A family of rough-plaquette configurations outside the weak-field chart violates the proposed coercive estimate, so this exact hypothesis is stopped and retained as a negative result.

9. `}`

   Ends the `abducer_work_loop` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## conceptual_hypothesis_exploration_loop

**Function:** replace a structural obstruction with a mediated, testable route

**Aliases:** `conceptual-obstruction-refinement`

**Projection status:** `curated_abstraction`

**Source references:** `agentic/registries/workflow_contracts.yaml`, `registry/tasks/hegelian-abducer-integration/task_registry.json`

**Fictional worked example:** Repeated proofs fail because they transport a
finite-volume invariant into the continuum without a preservation theorem.
The workflow proposes a new observable-algebra mediator, checks its transfer
conditions, and sends it to `abducer_work_loop` only after it becomes a
specific, testable bridge.

```erfl
erfl 0.2
reasoning conceptual_hypothesis_exploration_loop {
  goal "replace a structural obstruction with a testable mediated route" -> refinement_status
  steps e0:E[failure_state->pressure] -constrain> ...
        a0:A[pressure->candidate] -transfer> ...
        t0:T[candidate->bridge] -assume> ...
        d0:D[bridge->consequence] -test> ...
        r0:R[consequence->verdict] -calibrate> ...
        e1:E[bridge,verdict->refinement_status]
  on e1.work_ready => switch @abducer_work_loop
  on e1.release_candidate => switch @release_promotion_loop
  on r0.refuted => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following conceptual_hypothesis_exploration_loop example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning conceptual_hypothesis_exploration_loop {`

   Begins the canonical reasoning program named `conceptual_hypothesis_exploration_loop`.

   **Physics context:** An attempted inference from Wilson-loop area law to a continuum mass gap has failed: the area law controls external-probe free energy, but no theorem supplied decay of time-separated local gauge-invariant correlators with enough state-space coverage to control the reconstructed spectrum.

3. `goal "replace a structural obstruction with a testable mediated route" -> refinement_status`

   Sets the epistemic objective to “replace a structural obstruction with a testable mediated route” and names the required resulting state `refinement_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The workflow seeks reflection-positive, gauge-invariant time-correlation estimates with explicit norm dependence and constants uniform in the required volume and cutoff limits, sufficient for a stated sectoral spectral claim.

4. `steps e0:E[failure_state->pressure] -constrain> a0:A[pressure->candidate] -transfer> t0:T[candidate->bridge] -assume> d0:D[bridge->consequence] -test> r0:R[consequence->verdict] -calibrate> e1:E[bridge,verdict->refinement_status]`

   Defines the main epistemic steps: `e0` performs epistemic status calibration, consuming `failure_state` and producing `pressure`; it then uses the preceding state to narrow what the next occurrence may produce, after which `a0` performs abductive hypothesis formation, consuming `pressure` and producing `candidate`; it then attempts a structural transfer while retaining correspondence and side-condition obligations, after which `t0` performs structural analogy and transfer, consuming `candidate` and producing `bridge`; it then retains the preceding candidate explicitly as a premise for conditional reasoning, after which `d0` performs deductive entailment, consuming `bridge` and producing `consequence`; it then subjects the preceding claim or candidate to critical testing, after which `r0` performs critical refutational testing, consuming `consequence` and producing `verdict`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e1` performs epistemic status calibration, consuming `bridge` and `verdict` and producing `refinement_status`.

   **Concrete physics example:** Calibration isolates the failed area-law-to-gap inference; abduction proposes a reflection-positive correlation-decay certificate; structural transfer attempts the Euclidean-correlator to transfer-operator correspondence while retaining positivity, reconstruction, and uniformity as obligations; deduction derives a conditional spectral consequence; refutation tests those side conditions; calibration judges the replacement route.

5. `on e1.work_ready => switch @abducer_work_loop`

   When `e1` (epistemic status calibration) reports `work_ready` (work ready), control switches to `abducer_work_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The certificate has explicit positivity and uniformity obligations, making it precise enough for a proof attempt.

6. `on e1.release_candidate => switch @release_promotion_loop`

   When `e1` (epistemic status calibration) reports `release_candidate` (release candidate), control switches to `release_promotion_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The bridge is justified for a named reflection-positive solvable lattice model and specified operator channel, so it may be released only as a model-specific transfer-spectrum result without a four-dimensional particle interpretation.

7. `on r0.refuted => stop`

   When `r0` (critical refutational testing) reports `refuted` (refuted), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** Reflection positivity is unavailable for the proposed lattice action, so this transfer-operator inference is unlicensed; the spectral conclusion itself is not thereby refuted.

8. `}`

   Ends the `conceptual_hypothesis_exploration_loop` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## release_promotion_loop

**Function:** issue a claim-conserving promotion, repair, or rejection disposition

**Aliases:** None

**Projection status:** `gap_bearing_curated_abstraction`

**Source references:** `agentic/registries/workflow_contracts.yaml`

**Fictional worked example:** An audited lemma proves a fixed-cutoff bound, but
its draft title claims a continuum result. The release workflow preserves the
lemma, rejects the overbroad title, and switches to `target_navigation_loop`
for target repair; the valid bounded result is not discarded or promoted.

```erfl
erfl 0.2
reasoning release_promotion_loop {
  goal "issue a claim-conserving release disposition" -> release_status
  steps pre:_[run_evidence->release_candidate] -requires> ...
        e0:E[release_candidate->release_status]
  on e0.promoted => accept
  on e0.repair_target => switch @target_navigation_loop
  on e0.repair_concept => switch @conceptual_hypothesis_exploration_loop
  on e0.rejected => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following release_promotion_loop example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning release_promotion_loop {`

   Begins the canonical reasoning program named `release_promotion_loop`.

   **Physics context:** A programme presents a candidate exponential-clustering result for a finite-volume SU(2) lattice gauge theory with fixed cutoff and must decide what, if anything, may enter the durable result record.

3. `goal "issue a claim-conserving release disposition" -> release_status`

   Sets the epistemic objective to “issue a claim-conserving release disposition” and names the required resulting state `release_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The release decision must preserve the finite-volume and fixed-cutoff scope instead of promoting the theorem into a continuum Yang–Mills mass-gap result.

4. `steps pre:_[run_evidence->release_candidate] -requires> e0:E[release_candidate->release_status]`

   Defines the main epistemic steps: `pre` marks an unresolved reasoning region that carries `run_evidence` into `release_candidate`; no reasoning type is inferred for it; it then requires the next occurrence structurally; this dependency adds no evidential warrant, after which `e0` performs epistemic status calibration, consuming `release_candidate` and producing `release_status`.

   **Concrete physics example:** Unresolved release checks assemble the purported proof, assumptions, provenance, and open continuum obligations; those checks remain intentionally unclassified, and only calibration is typed when it produces a promotion, repair, or rejection status.

5. `on e0.promoted => accept`

   When `e0` (epistemic status calibration) reports `promoted` (promoted), the program accepts the calibrated result for workflow purposes. Acceptance does not create additional scientific warrant.

   **Concrete physics example:** The finite-volume connected-correlator decay estimate is promoted exactly with its cutoff, gauge group, and boundary assumptions.

6. `on e0.repair_target => switch @target_navigation_loop`

   When `e0` (epistemic status calibration) reports `repair_target` (repair target), control switches to `target_navigation_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The stated target incorrectly says continuum mass gap, so target navigation must narrow it to the theorem actually proved.

7. `on e0.repair_concept => switch @conceptual_hypothesis_exploration_loop`

   When `e0` (epistemic status calibration) reports `repair_concept` (repair concept), control switches to `conceptual_hypothesis_exploration_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The manuscript interprets one operator channel's inverse decay length as the full physical mass gap without verified spectral representation and sufficient state-space coverage, so conceptual repair is required.

8. `on e0.rejected => stop`

   When `e0` (epistemic status calibration) reports `rejected` (rejected), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** The purported theorem lacks a complete proof artifact and independent audit, so it is rejected as a promotable result.

9. `}`

   Ends the `release_promotion_loop` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## evidence_to_proof_route_onramp

**Function:** turn grounded evidence into a falsification-aware route to a proof obligation

**Aliases:** `evidence-to-proof-route-onramp`, `kb-route-onramp`

**Projection status:** `hypothesized_degraded_summary`

**Source references:** `agentic/registries/named_workflow_contracts.yaml`

**Fictional worked example:** A source bundle supports reflection positivity
and a transfer operator but not the advertised continuum conclusion. The
workflow constructs a narrower falsifiable route, exposes the missing
uniformity lemma, and hands that exact obligation to `theorem_proof_delivery`.

```erfl
erfl 0.2
reasoning evidence_to_proof_route_onramp {
  goal "produce a falsification-aware proof route" -> calibrated_route
  steps e0:E[source->ground] -constrain> ...
        a0:A[ground->route] -assume> ...
        d0:D[route->consequence] -calibrate> ...
        e1:E[consequence->assessment] -revise> ...
        a1:A[assessment->entrypoint] -test> ...
        r0:R[entrypoint->verdict] -calibrate> ...
        e2:E[entrypoint,verdict->status]
  on e2.route_ready => switch @theorem_proof_delivery
  on r0.refuted => stop
  on e2.requires_conceptual_refinement => switch @conceptual_hypothesis_exploration_loop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following evidence_to_proof_route_onramp example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning evidence_to_proof_route_onramp {`

   Begins the canonical reasoning program named `evidence_to_proof_route_onramp`.

   **Physics context:** A source bundle contains rigorous reflection-positivity results, transfer-matrix constructions, and numerical correlation data for lattice gauge theories.

3. `goal "produce a falsification-aware proof route" -> calibrated_route`

   Sets the epistemic objective to “produce a falsification-aware proof route” and names the required resulting state `calibrated_route`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The workflow must extract a falsifiable route from those sources to a precise spectral-gap obligation with explicit assumptions.

4. `steps e0:E[source->ground] -constrain> a0:A[ground->route] -assume> d0:D[route->consequence] -calibrate> e1:E[consequence->assessment] -revise> a1:A[assessment->entrypoint] -test> r0:R[entrypoint->verdict] -calibrate> e2:E[entrypoint,verdict->status]`

   Defines the main epistemic steps: `e0` performs epistemic status calibration, consuming `source` and producing `ground`; it then uses the preceding state to narrow what the next occurrence may produce, after which `a0` performs abductive hypothesis formation, consuming `ground` and producing `route`; it then retains the preceding candidate explicitly as a premise for conditional reasoning, after which `d0` performs deductive entailment, consuming `route` and producing `consequence`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e1` performs epistemic status calibration, consuming `consequence` and producing `assessment`; it then uses the preceding assessment to initiate a revised reasoning occurrence, after which `a1` performs abductive hypothesis formation, consuming `assessment` and producing `entrypoint`; it then subjects the preceding claim or candidate to critical testing, after which `r0` performs critical refutational testing, consuming `entrypoint` and producing `verdict`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e2` performs epistemic status calibration, consuming `entrypoint` and `verdict` and producing `status`.

   **Concrete physics example:** Evidence is calibrated for scope and provenance; abduction proposes the broad route area law -> correlation decay -> spectral gap; deduction exposes its claimed consequence; intermediate calibration rejects the underlicensed area-law-to-decay step; revision replaces it with the narrower entry lemma uniform reflection-positive correlation decay -> transfer-operator gap; refutation tests that lemma's side conditions; final calibration decides whether the revised route is proof-ready.

5. `on e2.route_ready => switch @theorem_proof_delivery`

   When `e2` (epistemic status calibration) reports `route_ready` (route ready), control switches to `theorem_proof_delivery`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The sources support a fixed-cutoff lemma turning a norm-controlled correlation estimate for a dense vacuum-orthogonal physical-state class into a transfer-operator contraction bound; volume uniformity, cutoff uniformity, and continuum reconstruction remain separate obligations.

6. `on r0.refuted => stop`

   When `r0` (critical refutational testing) reports `refuted` (refuted), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** A cited positivity theorem applies only to an action different from the one under study, invalidating the proposed entry route.

7. `on e2.requires_conceptual_refinement => switch @conceptual_hypothesis_exploration_loop`

   When `e2` (epistemic status calibration) reports `requires_conceptual_refinement` (requires conceptual refinement), control switches to `conceptual_hypothesis_exploration_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The literature provides correlation decay and confinement separately but no licensed bridge between them, so conceptual exploration is required.

8. `}`

   Ends the `evidence_to_proof_route_onramp` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## conceptual_frontier_deepening

**Function:** seek a discriminating conceptual bridge that is ready for formal work

**Aliases:** `conceptual-frontier-deepening`, `deep-conceptual-search`

**Projection status:** `hypothesized_degraded_summary`

**Source references:** `agentic/registries/named_workflow_contracts.yaml`

**Fictional worked example:** Existing confinement narratives predict the same
coarse observable. The workflow invents a bridge based on time-separated
gauge-invariant correlators, derives a prediction that distinguishes it from
the rivals, and advances it to `theorem_proof_delivery` only if adversarial
testing leaves a formalizable candidate.

```erfl
erfl 0.2
reasoning conceptual_frontier_deepening {
  goal "obtain a formal-ready discriminating conceptual candidate" -> calibrated_candidate
  steps e0:E[context->ground] -constrain> ...
        a0:A[ground->hypothesis] -test> ...
        r0:R[hypothesis->verdict] -calibrate> ...
        e1:E[hypothesis,verdict->selection] -revise> ...
        t0:T[selection->bridge] -assume> ...
        d0:D[bridge->claim] -calibrate> ...
        e2:E[claim->status]
  on e2.formal_ready => switch @theorem_proof_delivery
  on r0.refuted => stop
  on e2.candidate_not_ready_or_non_dominated => switch @conceptual_hypothesis_exploration_loop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following conceptual_frontier_deepening example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning conceptual_frontier_deepening {`

   Begins the canonical reasoning program named `conceptual_frontier_deepening`.

   **Physics context:** Standard confinement mechanisms do not yet yield a formal continuum spectral statement, so the programme compares center symmetry, disorder operators, and transfer-operator rigidity as deeper organizing concepts.

3. `goal "obtain a formal-ready discriminating conceptual candidate" -> calibrated_candidate`

   Sets the epistemic objective to “obtain a formal-ready discriminating conceptual candidate” and names the required resulting state `calibrated_candidate`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The desired output is a discriminating conceptual bridge whose premises and observables can be formalized rather than another qualitative confinement narrative.

4. `steps e0:E[context->ground] -constrain> a0:A[ground->hypothesis] -test> r0:R[hypothesis->verdict] -calibrate> e1:E[hypothesis,verdict->selection] -revise> t0:T[selection->bridge] -assume> d0:D[bridge->claim] -calibrate> e2:E[claim->status]`

   Defines the main epistemic steps: `e0` performs epistemic status calibration, consuming `context` and producing `ground`; it then uses the preceding state to narrow what the next occurrence may produce, after which `a0` performs abductive hypothesis formation, consuming `ground` and producing `hypothesis`; it then subjects the preceding claim or candidate to critical testing, after which `r0` performs critical refutational testing, consuming `hypothesis` and producing `verdict`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e1` performs epistemic status calibration, consuming `hypothesis` and `verdict` and producing `selection`; it then uses the preceding assessment to initiate a revised reasoning occurrence, after which `t0` performs structural analogy and transfer, consuming `selection` and producing `bridge`; it then retains the preceding candidate explicitly as a premise for conditional reasoning, after which `d0` performs deductive entailment, consuming `bridge` and producing `claim`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e2` performs epistemic status calibration, consuming `claim` and producing `status`.

   **Concrete physics example:** Context calibration fixes the physical regime; abduction proposes observable-algebra rigidity; refutation tests related solvable limits; calibration revises the original qualitative rigidity claim into a bounded correlation-decay candidate; structural transfer then attempts the Euclidean-to-transfer-operator correspondence while retaining positivity and reconstruction obligations; deduction obtains a conditional theorem; final calibration judges formal readiness.

5. `on e2.formal_ready => switch @theorem_proof_delivery`

   When `e2` (epistemic status calibration) reports `formal_ready` (formal ready), control switches to `theorem_proof_delivery`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The rigidity hypothesis now specifies the gauge-invariant observable class, operator channel, norm dependence, and volume/cutoff uniformity required of its correlator bounds, yielding a candidate transfer with explicit preservation obligations.

6. `on r0.refuted => stop`

   When `r0` (critical refutational testing) reports `refuted` (refuted), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** The hypothesis predicts a nonzero gap in a related gauge theory or solvable regime known to exhibit Coulomb-phase behavior, so the overgeneral candidate is refuted.

7. `on e2.candidate_not_ready_or_non_dominated => switch @conceptual_hypothesis_exploration_loop`

   When `e2` (epistemic status calibration) reports `candidate_not_ready_or_non_dominated` (candidate not ready or non dominated), control switches to `conceptual_hypothesis_exploration_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** Two mechanisms remain empirically indistinguishable and neither dominates on mathematical tractability, so both are handed to conceptual hypothesis exploration as retained learning rather than a forced winner.

8. `}`

   Ends the `conceptual_frontier_deepening` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## theorem_proof_delivery

**Function:** derive, refute, and calibrate an exact theorem under explicit premises

**Aliases:** `theorem-proof-delivery`, `proof-delivery`

**Projection status:** `hypothesized_degraded_summary`

**Source references:** `agentic/registries/named_workflow_contracts.yaml`

**Fictional worked example:** Under explicit positivity and contraction
premises, the workflow derives a finite-lattice spectral estimate, searches
for a violating configuration, and calibrates the surviving statement. An
accepted bounded proof moves to `scientific_contribution_cultivation`; a
counterexample produces a failure certificate and conceptual reorientation.

```erfl
erfl 0.2
reasoning theorem_proof_delivery {
  goal "settle the exact theorem under explicit premises" -> calibrated_proof_status
  steps d0:D[premises->claim] -test> ...
        r0:R[claim->verdict] -calibrate> ...
        e0:E[claim,verdict->status]
  on e0.proof_accepted => switch @scientific_contribution_cultivation
  on e0.failure_certificate_issued => switch @conceptual_hypothesis_exploration_loop
  on e0.quarantined => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following theorem_proof_delivery example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning theorem_proof_delivery {`

   Begins the canonical reasoning program named `theorem_proof_delivery`.

   **Physics context:** At fixed cutoff, reflection positivity constructs a physical Hilbert space and transfer operator T. The theorem candidate states that a norm-controlled exponential estimate for a norm-dense subset of the vacuum-orthogonal physical Hilbert space implies the corresponding operator contraction and sectoral spectral gap; a continuum gap still requires uniform volume/cutoff control and reconstruction.

3. `goal "settle the exact theorem under explicit premises" -> calibrated_proof_status`

   Sets the epistemic objective to “settle the exact theorem under explicit premises” and names the required resulting state `calibrated_proof_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The workflow must prove the implication under the stated premises or issue an explicit failure certificate.

4. `steps d0:D[premises->claim] -test> r0:R[claim->verdict] -calibrate> e0:E[claim,verdict->status]`

   Defines the main epistemic steps: `d0` performs deductive entailment, consuming `premises` and producing `claim`; it then subjects the preceding claim or candidate to critical testing, after which `r0` performs critical refutational testing, consuming `claim` and producing `verdict`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e0` performs epistemic status calibration, consuming `claim` and `verdict` and producing `status`.

   **Concrete physics example:** Deduction constructs the implication and its lemma chain; refutation checks boundary conditions, quantifiers, and reconstruction assumptions; calibration records accepted, failed, or quarantined proof status.

5. `on e0.proof_accepted => switch @scientific_contribution_cultivation`

   When `e0` (epistemic status calibration) reports `proof_accepted` (proof accepted), control switches to `scientific_contribution_cultivation`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** Observable coverage, norm dependence, physical sector, boundary conditions, and constants are explicit, and the fixed-cutoff operator estimate follows with a checked physical-energy scale, so the theorem enters contribution assessment at unchanged scope.

6. `on e0.failure_certificate_issued => switch @conceptual_hypothesis_exploration_loop`

   When `e0` (epistemic status calibration) reports `failure_certificate_issued` (failure certificate issued), control switches to `conceptual_hypothesis_exploration_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The proof uses a volume-uniform constant established only at fixed volume, so the failure certificate sends the programme to conceptual exploration of a genuinely volume-uniform bridge.

7. `on e0.quarantined => stop`

   When `e0` (epistemic status calibration) reports `quarantined` (quarantined), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** A crucial reconstruction lemma lacks a verified source and cannot yet be independently checked, so the proof is quarantined.

8. `}`

   Ends the `theorem_proof_delivery` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## scientific_contribution_cultivation

**Function:** test what scientific contribution is actually supported by a result

**Aliases:** `scientific-contribution-cultivation`, `contribution-cultivation`

**Projection status:** `hypothesized_degraded_summary`

**Source references:** `agentic/registries/named_workflow_contracts.yaml`

**Fictional worked example:** A correct technical lemma appears new but may not
change the scientific frontier. The workflow tests novelty, explanatory
importance, and dependence on known results, then forwards only the supported
contribution statement—not the authors' aspirations—to
`manuscript_result_elaboration`.

```erfl
erfl 0.2
reasoning scientific_contribution_cultivation {
  goal "determine the supported scientific contribution" -> calibrated_contribution
  steps a0:A[result->candidate] -test> ...
        r0:R[candidate->verdict] -calibrate> ...
        e0:E[candidate,verdict->status]
  on e0.paper_ready => switch @manuscript_result_elaboration
  on r0.refuted => stop
  on reasoning.stalled => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following scientific_contribution_cultivation example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning scientific_contribution_cultivation {`

   Begins the canonical reasoning program named `scientific_contribution_cultivation`.

   **Physics context:** A new theorem establishes a quantitative finite-volume correlation bound for a reflection-positive lattice gauge model but does not control the continuum limit.

3. `goal "determine the supported scientific contribution" -> calibrated_contribution`

   Sets the epistemic objective to “determine the supported scientific contribution” and names the required resulting state `calibrated_contribution`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The workflow must determine the smallest honest contribution: a reusable finite-volume theorem, a methodological certificate, or no publishable advance.

4. `steps a0:A[result->candidate] -test> r0:R[candidate->verdict] -calibrate> e0:E[candidate,verdict->status]`

   Defines the main epistemic steps: `a0` performs abductive hypothesis formation, consuming `result` and producing `candidate`; it then subjects the preceding claim or candidate to critical testing, after which `r0` performs critical refutational testing, consuming `candidate` and producing `verdict`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e0` performs epistemic status calibration, consuming `candidate` and `verdict` and producing `status`.

   **Concrete physics example:** Abduction proposes the contribution claim; refutation compares it against counterexamples, prior results, and the missing continuum step; calibration decides its supported value and scope.

5. `on e0.paper_ready => switch @manuscript_result_elaboration`

   When `e0` (epistemic status calibration) reports `paper_ready` (paper ready), control switches to `manuscript_result_elaboration`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The bound improves the known volume dependence and supplies a reusable lemma, supporting a focused mathematical-physics paper.

6. `on r0.refuted => stop`

   When `r0` (critical refutational testing) reports `refuted` (refuted), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** An earlier theorem already proves the same bound under weaker assumptions, refuting the novelty claim.

7. `on reasoning.stalled => stop`

   When the reasoning program as a whole reports `stalled` (stalled), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** The result is correct but its relationship to existing cluster-expansion bounds cannot be resolved from available sources, so publication assessment stops.

8. `}`

   Ends the `scientific_contribution_cultivation` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## manuscript_result_elaboration

**Function:** extend a result into a scope-safe and evidence-aligned manuscript

**Aliases:** `manuscript-result-elaboration`, `results-elaboration`

**Projection status:** `hypothesized_degraded_summary`

**Source references:** `agentic/registries/named_workflow_contracts.yaml`

**Fictional worked example:** A manuscript grows from a finite-volume theorem.
The workflow adds comparisons and implications while marking a proposed
continuum extension as an open obligation. If elaboration exposes missing
proof support, control returns to `theorem_proof_delivery` rather than hiding
the gap in prose.

```erfl
erfl 0.2
reasoning manuscript_result_elaboration {
  goal "produce a scope-safe evidence-aligned manuscript" -> calibrated_manuscript
  steps e0:E[result->scope] -constrain> ...
        a0:A[scope->extension] -test> ...
        r0:R[extension->verdict] -calibrate> ...
        e1:E[extension,verdict->paper_status]
  on e1.proof_required => switch @theorem_proof_delivery
  on e1.paper_ready => accept
  on reasoning.stalled => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following manuscript_result_elaboration example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning manuscript_result_elaboration {`

   Begins the canonical reasoning program named `manuscript_result_elaboration`.

   **Physics context:** A draft paper contains a finite-volume connected-correlator decay theorem and must explain how it constrains—but does not solve—the continuum Yang–Mills mass-gap programme.

3. `goal "produce a scope-safe evidence-aligned manuscript" -> calibrated_manuscript`

   Sets the epistemic objective to “produce a scope-safe evidence-aligned manuscript” and names the required resulting state `calibrated_manuscript`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The manuscript should present the theorem, proof boundary, physical interpretation, and open continuum obligations without claim inflation.

4. `steps e0:E[result->scope] -constrain> a0:A[scope->extension] -test> r0:R[extension->verdict] -calibrate> e1:E[extension,verdict->paper_status]`

   Defines the main epistemic steps: `e0` performs epistemic status calibration, consuming `result` and producing `scope`; it then uses the preceding state to narrow what the next occurrence may produce, after which `a0` performs abductive hypothesis formation, consuming `scope` and producing `extension`; it then subjects the preceding claim or candidate to critical testing, after which `r0` performs critical refutational testing, consuming `extension` and producing `verdict`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e1` performs epistemic status calibration, consuming `extension` and `verdict` and producing `paper_status`.

   **Concrete physics example:** Calibration fixes the supported result; abduction proposes a bounded extension such as a corollary for susceptibility; refutation tests the extension; final calibration decides whether the paper is ready or needs another theorem.

5. `on e1.proof_required => switch @theorem_proof_delivery`

   When `e1` (epistemic status calibration) reports `proof_required` (proof required), control switches to `theorem_proof_delivery`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** A claimed infinite-volume susceptibility bound needs existence of the thermodynamic limit and a volume-uniform summable majorant for the connected correlator, neither yet proved, so it is sent to theorem delivery.

6. `on e1.paper_ready => accept`

   When `e1` (epistemic status calibration) reports `paper_ready` (paper ready), the program accepts the calibrated result for workflow purposes. Acceptance does not create additional scientific warrant.

   **Concrete physics example:** The draft clearly separates the rigorous finite-volume theorem from the conjectural continuum interpretation and is ready for expert review.

7. `on reasoning.stalled => stop`

   When the reasoning program as a whole reports `stalled` (stalled), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** The narrative still relies on an unresolved model-to-target analogy, so elaboration stops rather than masking the gap with exposition.

8. `}`

   Ends the `manuscript_result_elaboration` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## deep_review_and_reorientation

**Function:** compare defeaters and repairs to select a governed reorientation or stop

**Aliases:** `deep-review-and-reorientation`, `deep-review`

**Projection status:** `hypothesized_degraded_summary`

**Source references:** `agentic/registries/named_workflow_contracts.yaml`

**Fictional worked example:** Three independent reviews agree that a route
silently changes regulator, while one repair preserves the regulator and adds
a testable universality obligation. The workflow records both the defeater and
the repair, then sends the repaired target to `target_navigation_loop` instead
of restarting the same failed derivation.

```erfl
erfl 0.2
reasoning deep_review_and_reorientation {
  goal "identify a governed repair or justified stop" -> calibrated_reorientation
  steps e0:E[evidence->state] -constrain> ...
        (r0:R[state->defeaters] & a0:A[state->repairs]) -calibrate> ...
        e1:E[defeaters,repairs->decision]
  on e1.repair_workflow_assigned => switch @target_navigation_loop
  on e1.conceptual_reorientation_required => switch @conceptual_hypothesis_exploration_loop
  on reasoning.stalled => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following deep_review_and_reorientation example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning deep_review_and_reorientation {`

   Begins the canonical reasoning program named `deep_review_and_reorientation`.

   **Physics context:** Independent reviewers assess a Yang–Mills programme whose finite-lattice estimates are sound but whose continuum uniformity argument repeatedly fails.

3. `goal "identify a governed repair or justified stop" -> calibrated_reorientation`

   Sets the epistemic objective to “identify a governed repair or justified stop” and names the required resulting state `calibrated_reorientation`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The review must select a governed repair, a conceptual reorientation, or a justified stop while preserving dissent and negative evidence.

4. `steps e0:E[evidence->state] -constrain> (r0:R[state->defeaters] & a0:A[state->repairs]) -calibrate> e1:E[defeaters,repairs->decision]`

   Defines the main epistemic steps: `e0` performs epistemic status calibration, consuming `evidence` and producing `state`; it then uses the preceding state to narrow what the next occurrence may produce, after which all of these branches are required—branch 1: `r0` performs critical refutational testing, consuming `state` and producing `defeaters`; branch 2: `a0` performs abductive hypothesis formation, consuming `state` and producing `repairs`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e1` performs epistemic status calibration, consuming `defeaters` and `repairs` and producing `decision`.

   **Concrete physics example:** Calibration assembles the evidence state; parallel refutation identifies fatal defects while abduction proposes repairs; final calibration compares both branches and assigns the next disposition.

5. `on e1.repair_workflow_assigned => switch @target_navigation_loop`

   When `e1` (epistemic status calibration) reports `repair_workflow_assigned` (repair workflow assigned), control switches to `target_navigation_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** Reviewers decompose the target into construction of continuum infinite-volume Schwinger functions satisfying the required Osterwalder–Schrader axioms and a physical-sector spectral estimate uniform in volume and cutoff.

6. `on e1.conceptual_reorientation_required => switch @conceptual_hypothesis_exploration_loop`

   When `e1` (epistemic status calibration) reports `conceptual_reorientation_required` (conceptual reorientation required), control switches to `conceptual_hypothesis_exploration_loop`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The same continuum obstruction defeats every cutoff route examined in this review, motivating—but not validating—a candidate gauge-invariant observable-algebra reformulation.

7. `on reasoning.stalled => stop`

   When the reasoning program as a whole reports `stalled` (stalled), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** The reviews disagree about whether the obstruction is technical or structural and no discriminating test is available, so the programme stops with dissent recorded.

8. `}`

   Ends the `deep_review_and_reorientation` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## timeline-paper-independent-workflow

**Function:** produce a claim-bounded presentation of accumulated reasoning

**Aliases:** None

**Projection status:** `gap_bearing_curated_abstraction`

**Source references:** `registry/tasks/timeline-paper-workflow/task_registry.json`

**Fictional worked example:** A paper reconstructs ten cycles containing two
proved lemmas, four failed hypotheses, and one unresolved bridge. The workflow
orders them chronologically and labels their statuses separately; it stops
rather than describing the unresolved bridge as the culmination of a proof.

```erfl
erfl 0.2
reasoning timeline-paper-independent-workflow {
  goal "produce a claim-bounded presentation of accumulated reasoning" -> paper_status
  steps pre:_[source_outputs->claim_set] -requires> ...
        e0:E[claim_set->paper_status]
  on e0.paper_ready => accept
  on e0.claim_boundary_failure => stop
  on reasoning.stalled => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following timeline-paper-independent-workflow example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning timeline-paper-independent-workflow {`

   Begins the canonical reasoning program named `timeline-paper-independent-workflow`.

   **Physics context:** A paper traces the evolution of a Yang–Mills mass-gap programme from lattice reflection positivity through finite-volume spectral estimates to the unresolved continuum-uniformity barrier.

3. `goal "produce a claim-bounded presentation of accumulated reasoning" -> paper_status`

   Sets the epistemic objective to “produce a claim-bounded presentation of accumulated reasoning” and names the required resulting state `paper_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The output should be a historically and logically ordered account that labels proved theorems, failed routes, simulations, and conjectural bridges separately.

4. `steps pre:_[source_outputs->claim_set] -requires> e0:E[claim_set->paper_status]`

   Defines the main epistemic steps: `pre` marks an unresolved reasoning region that carries `source_outputs` into `claim_set`; no reasoning type is inferred for it; it then requires the next occurrence structurally; this dependency adds no evidential warrant, after which `e0` performs epistemic status calibration, consuming `claim_set` and producing `paper_status`.

   **Concrete physics example:** Unresolved document synthesis selects and orders source outputs; the synthesis remains intentionally unclassified, and only calibration is typed when it audits every statement against its authoritative proof status.

5. `on e0.paper_ready => accept`

   When `e0` (epistemic status calibration) reports `paper_ready` (paper ready), the program accepts the calibrated result for workflow purposes. Acceptance does not create additional scientific warrant.

   **Concrete physics example:** Every historical claim cites its source and the conclusion states only that the work isolates the continuum obstruction, not that it solves the mass gap.

6. `on e0.claim_boundary_failure => stop`

   When `e0` (epistemic status calibration) reports `claim_boundary_failure` (claim boundary failure), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** The draft describes finite-lattice exponential decay as a continuum theorem, so release stops at the claim-boundary gate.

7. `on reasoning.stalled => stop`

   When the reasoning program as a whole reports `stalled` (stalled), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** Two incompatible reconstructions of an earlier failed proof cannot be reconciled, so the timeline remains incomplete.

8. `}`

   Ends the `timeline-paper-independent-workflow` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## ym-representational-dynamics-overlay

**Function:** calibrate a Yang-Mills candidate while preserving the continuum claim boundary

**Aliases:** None

**Projection status:** `gap_bearing_curated_abstraction`

**Source references:** `registry/tasks/discovery-marathon/task_registry.json`

**Fictional worked example:** A proposed representation makes gauge invariance
explicit but assumes the continuum state it is meant to construct. The overlay
queries the target KB, detects the circularity during calibration, and persists
a quarantined representation record without changing any other workflow.

```erfl
erfl 0.3
@KB kb0 connect(file("KB/yang-mills-existence-and-mass-gap.kb.md"))
reasoning ym-representational-dynamics-overlay {
  goal "return a calibrated Yang-Mills candidate without crossing the continuum boundary" -> overlay_status
  steps pre:_[kb0,target_context->audit_input] -requires> ...
        audit:E[audit_input->overlay_status]
  pre <-query- kb0
  audit -persist-> kb0
  on audit.accepted => accept
  on audit.quarantined => stop
  on reasoning.stalled => stop
}
```

### Line-by-line interpretation

1. `erfl 0.3`

   Declares that this program uses ERFL version `0.3`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following ym-representational-dynamics-overlay example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `@KB kb0 connect(file("KB/yang-mills-existence-and-mass-gap.kb.md"))`

   Connects external KB symbol `kb0` to file-backed resource `KB/yang-mills-existence-and-mass-gap.kb.md` before reasoning begins.

   **Physics context:** The reasoning uses the authoritative Yang–Mills KB as an external resource.

3. `reasoning ym-representational-dynamics-overlay {`

   Begins the canonical reasoning program named `ym-representational-dynamics-overlay`.

   **Physics context:** A Yang–Mills overlay evaluates whether a gauge-invariant observable-algebra representation improves the route from lattice measures to continuum spectral statements.

4. `goal "return a calibrated Yang-Mills candidate without crossing the continuum boundary" -> overlay_status`

   Sets the epistemic objective to “return a calibrated Yang-Mills candidate without crossing the continuum boundary” and names the required resulting state `overlay_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The overlay may return a calibrated candidate representation, but it may not claim the continuum mass gap without the missing reconstruction and uniformity proofs.

5. `steps pre:_[kb0,target_context->audit_input] -requires> audit:E[audit_input->overlay_status]`

   Defines the main epistemic steps: `pre` marks an unresolved reasoning region that carries `kb0` and `target_context` into `audit_input`; no reasoning type is inferred for it; it then requires the next occurrence structurally; this dependency adds no evidential warrant, after which `audit` performs epistemic status calibration, consuming `audit_input` and producing `overlay_status`.

   **Concrete physics example:** Unresolved domain-specific analysis constructs an audit input from the target context; that construction remains intentionally unclassified, and only calibration is typed when it accepts or quarantines the representation under the continuum claim ceiling.

6. `pre <-query- kb0`

   Occurrence `pre` queries KB `kb0`; the inverted arrow records information flowing from the KB into reasoning.

   **Physics context:** The occurrence reads only the KB material named in its input interface.

7. `audit -persist-> kb0`

   Calibrated occurrence `audit` persists a successor of KB `kb0` without promoting member authority.

   **Physics context:** Only the calibrated result may create a versioned KB successor.

8. `on audit.accepted => accept`

   When `audit` (epistemic status calibration) reports `accepted` (accepted), the program accepts the calibrated result for workflow purposes. Acceptance does not create additional scientific warrant.

   **Concrete physics example:** The construction uses a gauge-invariant observable algebra and exposes the required positive state, time evolution, thermodynamic limit, and continuum-reconstruction obligations, so it is accepted only as candidate kinematics.

9. `on audit.quarantined => stop`

   When `audit` (epistemic status calibration) reports `quarantined` (quarantined), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** The representation assumes the very continuum measure whose existence is at issue, so it is quarantined for circularity.

10. `on reasoning.stalled => stop`

   When the reasoning program as a whole reports `stalled` (stalled), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** No test distinguishes the new representation from the standard transfer-matrix formulation on available models, so the overlay stops.

11. `}`

   Ends the `ym-representational-dynamics-overlay` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## cohere_fast

**Function:** coordinate an isolated domain-bound path to independent calibration

**Aliases:** `cohere-fast`

**Projection status:** `gap_bearing_degraded_summary`

**Source references:** `agentic/registries/cohere_fast_ym_workflow.yaml`, `registry/tasks/cohere-fast/task_registry.json`, `docs/workflows/cohere-fast.md`

**Fictional worked example:** The explicit command `cohere-fast ym` asks for a
rapid assessment of a block-spin construction. The isolated parent checks that
the domain and candidate-level ceiling are present, then starts
`cohere_fast_scope_and_ground`; it never inserts the request into the main
discovery workflows.

```erfl
erfl 0.2
reasoning cohere_fast {
  goal "reach a domain-bound independently calibrated disposition" -> calibrated_domain_result
  steps pre:_[domain_input->scope_request] -requires> ...
        intake:E[scope_request->intake_status]
  on intake.ready => switch @cohere_fast_scope_and_ground
  on intake.blocked => stop
  on reasoning.stalled => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following cohere_fast example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning cohere_fast {`

   Begins the canonical reasoning program named `cohere_fast`.

   **Physics context:** An explicitly invoked cohere-fast Yang–Mills run receives a request to examine a gauge-covariant renormalization route under a candidate-level claim ceiling.

3. `goal "reach a domain-bound independently calibrated disposition" -> calibrated_domain_result`

   Sets the epistemic objective to “reach a domain-bound independently calibrated disposition” and names the required resulting state `calibrated_domain_result`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The parent must initiate the isolated five-stage domain workflow and cannot accept a result before independent audit and manuscript release.

4. `steps pre:_[domain_input->scope_request] -requires> intake:E[scope_request->intake_status]`

   Defines the main epistemic steps: `pre` marks an unresolved reasoning region that carries `domain_input` into `scope_request`; no reasoning type is inferred for it; it then requires the next occurrence structurally; this dependency adds no evidential warrant, after which `intake` performs epistemic status calibration, consuming `scope_request` and producing `intake_status`.

   **Concrete physics example:** Unresolved intake work converts the domain request into a scoping request; intake construction remains intentionally unclassified, and only calibration is typed when it decides readiness for the isolated physics workflow.

5. `on intake.ready => switch @cohere_fast_scope_and_ground`

   When `intake` (epistemic status calibration) reports `ready` (ready), control switches to `cohere_fast_scope_and_ground`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The gauge group, dimension, regularization, target observable, sources, and candidate claim ceiling are explicit, so scope-and-ground begins.

6. `on intake.blocked => stop`

   When `intake` (epistemic status calibration) reports `blocked` (blocked), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** The request asks for a continuum proof while supplying only simulation plots and no reconstruction assumptions, so intake blocks it.

7. `on reasoning.stalled => stop`

   When the reasoning program as a whole reports `stalled` (stalled), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** The target action and observable remain ambiguous after intake, so the parent stops without activating another workflow.

8. `}`

   Ends the `cohere_fast` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## cohere_fast_scope_and_ground

**Function:** bind the target, sources, domain, and claim ceiling

**Aliases:** `cohere_fast:scope-and-ground`

**Projection status:** `gap_bearing_degraded_summary`

**Source references:** `agentic/registries/cohere_fast_subworkflows.yaml`

**Fictional worked example:** The stage freezes four-dimensional SU(3), a
specified lattice action, named observables, admissible sources, and a
candidate-only ceiling. A request mixing SU(2) evidence with an SU(3) target is
blocked; a coherent scope proceeds to `cohere_fast_adaptive_frontier`.

```erfl
erfl 0.2
reasoning cohere_fast_scope_and_ground {
  goal "bind target, sources, domain, and claim ceiling" -> scope_status
  steps pre:_[domain_request->scope_candidate] -requires> ...
        e0:E[scope_candidate->scope_status]
  on e0.accepted => switch @cohere_fast_adaptive_frontier
  on e0.blocked => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following cohere_fast_scope_and_ground example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning cohere_fast_scope_and_ground {`

   Begins the canonical reasoning program named `cohere_fast_scope_and_ground`.

   **Physics context:** The cohere-fast run scopes four-dimensional SU(3) Yang–Mills with Wilson action, a fixed family of Wilson-loop and correlator observables, and a candidate-level ceiling.

3. `goal "bind target, sources, domain, and claim ceiling" -> scope_status`

   Sets the epistemic objective to “bind target, sources, domain, and claim ceiling” and names the required resulting state `scope_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The stage must bind the target, admissible sources, regulator regime, observables, and forbidden continuum conclusions.

4. `steps pre:_[domain_request->scope_candidate] -requires> e0:E[scope_candidate->scope_status]`

   Defines the main epistemic steps: `pre` marks an unresolved reasoning region that carries `domain_request` into `scope_candidate`; no reasoning type is inferred for it; it then requires the next occurrence structurally; this dependency adds no evidential warrant, after which `e0` performs epistemic status calibration, consuming `scope_candidate` and producing `scope_status`.

   **Concrete physics example:** Unresolved domain grounding produces a scope candidate; grounding remains intentionally unclassified, and only calibration is typed when it checks the physics question and claim ceiling.

5. `on e0.accepted => switch @cohere_fast_adaptive_frontier`

   When `e0` (epistemic status calibration) reports `accepted` (accepted), control switches to `cohere_fast_adaptive_frontier`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The target is fixed to constructing a regulator-consistent candidate mechanism, so the adaptive-frontier stage may explore it.

6. `on e0.blocked => stop`

   When `e0` (epistemic status calibration) reports `blocked` (blocked), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** The request mixes SU(2) numerical inputs with an SU(3) theorem target without a transfer argument, so grounding blocks the run.

7. `}`

   Ends the `cohere_fast_scope_and_ground` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## cohere_fast_adaptive_frontier

**Function:** form a bounded domain frontier without epistemic promotion

**Aliases:** `cohere_fast:adaptive-frontier`

**Projection status:** `gap_bearing_degraded_summary`

**Source references:** `agentic/registries/cohere_fast_subworkflows.yaml`

**Fictional worked example:** The frontier generates three distinct candidates:
a character-expansion bound, a gauge-covariant coarse-graining map, and an
observable-algebra reformulation. It keeps them as alternatives, quarantines a
map that breaks covariance, and sends the bounded survivors to
`cohere_fast_derivation_and_proof`.

```erfl
erfl 0.2
reasoning cohere_fast_adaptive_frontier {
  goal "form a bounded domain frontier without epistemic promotion" -> frontier_status
  steps pre:_[scope_state->frontier_candidate] -requires> ...
        e0:E[frontier_candidate->frontier_status]
  on e0.accepted => switch @cohere_fast_derivation_and_proof
  on e0.quarantined => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following cohere_fast_adaptive_frontier example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning cohere_fast_adaptive_frontier {`

   Begins the canonical reasoning program named `cohere_fast_adaptive_frontier`.

   **Physics context:** The adaptive frontier compares character or heat-kernel bounds applied explicitly to the Wilson plaquette weight, gauge-covariant block-spin maps, and gauge-invariant observable-algebra formulations; changing to a heat-kernel lattice action would be a different regulator requiring a universality bridge.

3. `goal "form a bounded domain frontier without epistemic promotion" -> frontier_status`

   Sets the epistemic objective to “form a bounded domain frontier without epistemic promotion” and names the required resulting state `frontier_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The stage should produce a bounded portfolio of physically distinct candidate constructions without promoting any to a validated continuum mechanism.

4. `steps pre:_[scope_state->frontier_candidate] -requires> e0:E[frontier_candidate->frontier_status]`

   Defines the main epistemic steps: `pre` marks an unresolved reasoning region that carries `scope_state` into `frontier_candidate`; no reasoning type is inferred for it; it then requires the next occurrence structurally; this dependency adds no evidential warrant, after which `e0` performs epistemic status calibration, consuming `frontier_candidate` and producing `frontier_status`.

   **Concrete physics example:** Unresolved domain reasoning assembles the frontier candidates; candidate construction remains intentionally unclassified, and only calibration is typed when it checks scope, novelty, tractability, and claim-ceiling compliance.

5. `on e0.accepted => switch @cohere_fast_derivation_and_proof`

   When `e0` (epistemic status calibration) reports `accepted` (accepted), control switches to `cohere_fast_derivation_and_proof`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** Character-expansion bounds for the Wilson weight and an observable-algebra route survive as distinct candidates; a different heat-kernel action remains separate until a regulator-transfer argument is supplied.

6. `on e0.quarantined => stop`

   When `e0` (epistemic status calibration) reports `quarantined` (quarantined), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** A block-spin proposal breaks gauge covariance at the coarse-graining boundary, so the frontier packet is quarantined.

7. `}`

   Ends the `cohere_fast_adaptive_frontier` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## cohere_fast_derivation_and_proof

**Function:** produce a conditional derivation packet while retaining open obligations

**Aliases:** `cohere_fast:derivation-and-proof`

**Projection status:** `gap_bearing_degraded_summary`

**Source references:** `agentic/registries/cohere_fast_subworkflows.yaml`

**Fictional worked example:** The selected candidate yields a finite-block
estimate whose constant may depend on volume. The stage derives everything
that follows conditionally, records volume uniformity as open, and forwards the
packet to `cohere_fast_independent_audit` without calling it a continuum proof.

```erfl
erfl 0.2
reasoning cohere_fast_derivation_and_proof {
  goal "produce a conditional derivation packet with open obligations retained" -> derivation_status
  steps pre:_[frontier_state->derivation_candidate] -requires> ...
        e0:E[derivation_candidate->derivation_status]
  on e0.accepted => switch @cohere_fast_independent_audit
  on e0.quarantined => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following cohere_fast_derivation_and_proof example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning cohere_fast_derivation_and_proof {`

   Begins the canonical reasoning program named `cohere_fast_derivation_and_proof`.

   **Physics context:** The derivation stage develops conditional character-expansion bounds for the Wilson plaquette weight and a gauge-invariant correlation estimate; any result using a different heat-kernel action remains regulator-specific until a universality bridge is proved.

3. `goal "produce a conditional derivation packet with open obligations retained" -> derivation_status`

   Sets the epistemic objective to “produce a conditional derivation packet with open obligations retained” and names the required resulting state `derivation_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The output must be a conditional derivation packet with premises, lemmas, failed branches, and open uniformity obligations visible.

4. `steps pre:_[frontier_state->derivation_candidate] -requires> e0:E[derivation_candidate->derivation_status]`

   Defines the main epistemic steps: `pre` marks an unresolved reasoning region that carries `frontier_state` into `derivation_candidate`; no reasoning type is inferred for it; it then requires the next occurrence structurally; this dependency adds no evidential warrant, after which `e0` performs epistemic status calibration, consuming `derivation_candidate` and producing `derivation_status`.

   **Concrete physics example:** Unresolved domain proof work produces a derivation candidate; that work remains intentionally unclassified, and only calibration is typed when it verifies that each conclusion remains conditional on its cutoff and reconstruction assumptions.

5. `on e0.accepted => switch @cohere_fast_independent_audit`

   When `e0` (epistemic status calibration) reports `accepted` (accepted), control switches to `cohere_fast_independent_audit`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** The finite-block estimate is internally derived and the continuum-limit lemma remains explicitly open, so the packet may enter independent audit.

6. `on e0.quarantined => stop`

   When `e0` (epistemic status calibration) reports `quarantined` (quarantined), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** A claimed uniform constant depends secretly on lattice volume, so the derivation is quarantined rather than presented as scale-independent.

7. `}`

   Ends the `cohere_fast_derivation_and_proof` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## cohere_fast_independent_audit

**Function:** adversarially test and calibrate the bounded domain derivation

**Aliases:** `cohere_fast:independent-audit`

**Projection status:** `degraded_summary`

**Source references:** `agentic/registries/cohere_fast_subworkflows.yaml`

**Fictional worked example:** An independent audit searches rough-field and
boundary configurations and finds that the purported uniform constant diverges
in one declared regime. Refutation records the witness, calibration quarantines
the derivation, and manuscript release is not activated.

```erfl
erfl 0.2
reasoning cohere_fast_independent_audit {
  goal "adversarially assess the bounded domain derivation" -> audit_status
  steps r0:R[derivation_candidate->verdict] -calibrate> ...
        e0:E[derivation_candidate,verdict->audit_status]
  on e0.accepted => switch @cohere_fast_manuscript_release
  on e0.quarantined => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following cohere_fast_independent_audit example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning cohere_fast_independent_audit {`

   Begins the canonical reasoning program named `cohere_fast_independent_audit`.

   **Physics context:** An independent auditor stress-tests the derivation against rough-plaquette configurations outside weak-field assumptions, boundary conditions, explicitly defined admissible or topological sectors, gauge-fixing and Gribov dependence in intermediate steps, and scaling with volume and lattice spacing.

3. `goal "adversarially assess the bounded domain derivation" -> audit_status`

   Sets the epistemic objective to “adversarially assess the bounded domain derivation” and names the required resulting state `audit_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The audit must classify the bounded derivation as acceptable or quarantined without granting continuum-proof authority; any refutation remains explicit inside r0's verdict.

4. `steps r0:R[derivation_candidate->verdict] -calibrate> e0:E[derivation_candidate,verdict->audit_status]`

   Defines the main epistemic steps: `r0` performs critical refutational testing, consuming `derivation_candidate` and producing `verdict`; it then uses the preceding findings to update epistemic status without creating a new substantive claim, after which `e0` performs epistemic status calibration, consuming `derivation_candidate` and `verdict` and producing `audit_status`.

   **Concrete physics example:** Critical refutation produces a verdict on the derivation candidate; calibration combines the candidate and verdict into an audit status.

5. `on e0.accepted => switch @cohere_fast_manuscript_release`

   When `e0` (epistemic status calibration) reports `accepted` (accepted), control switches to `cohere_fast_manuscript_release`. The switch is operational: it must preserve scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant.

   **Concrete physics example:** No declared adversarial case refutes the finite-volume estimates and all continuum obligations remain visible, so the packet is accepted for handoff at unchanged claim status.

6. `on e0.quarantined => stop`

   When `e0` (epistemic status calibration) reports `quarantined` (quarantined), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** An explicitly defined admissible-sector boundary or rough-plaquette family violates a required estimate, and the derivation does not delimit that regime, so the packet is quarantined.

7. `}`

   Ends the `cohere_fast_independent_audit` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.

## cohere_fast_manuscript_release

**Function:** authorize presentation without changing the authority of its claims

**Aliases:** `cohere_fast:manuscript-release`

**Projection status:** `gap_bearing_degraded_summary`

**Source references:** `agentic/registries/cohere_fast_subworkflows.yaml`

**Fictional worked example:** An audited packet contains a valid finite-volume
estimate and an unresolved continuum step. The release stage accepts a report
whose title and abstract preserve that boundary, but stops a draft claiming the
full mass-gap theorem. Presentation changes no epistemic status.

```erfl
erfl 0.2
reasoning cohere_fast_manuscript_release {
  goal "authorize a presentation without changing claim authority" -> release_status
  steps pre:_[audit_status->presentation_candidate] -requires> ...
        e0:E[presentation_candidate->release_status]
  on e0.accepted => accept
  on e0.stopped => stop
}
```

### Line-by-line interpretation

1. `erfl 0.2`

   Declares that this program uses ERFL version `0.2`, fixing the grammar and validation rules used to read the remaining lines.

   **Physics context:** The following cohere_fast_manuscript_release example is expressed under the same ERFL semantics, so its physics content cannot gain authority from control flow.

2. `reasoning cohere_fast_manuscript_release {`

   Begins the canonical reasoning program named `cohere_fast_manuscript_release`.

   **Physics context:** The final cohere-fast stage prepares a Yang–Mills report presenting the audited finite-volume derivation and its unresolved continuum obligations.

3. `goal "authorize a presentation without changing claim authority" -> release_status`

   Sets the epistemic objective to “authorize a presentation without changing claim authority” and names the required resulting state `release_status`. Reaching a control state alone does not establish the scientific claim.

   **Concrete physics example:** The report may communicate an independently audited candidate result but may not upgrade it to a proof of the Yang–Mills existence and mass-gap theorem.

4. `steps pre:_[audit_status->presentation_candidate] -requires> e0:E[presentation_candidate->release_status]`

   Defines the main epistemic steps: `pre` marks an unresolved reasoning region that carries `audit_status` into `presentation_candidate`; no reasoning type is inferred for it; it then requires the next occurrence structurally; this dependency adds no evidential warrant, after which `e0` performs epistemic status calibration, consuming `presentation_candidate` and producing `release_status`.

   **Concrete physics example:** Unresolved manuscript construction transforms the audit status into a presentation candidate; construction remains intentionally unclassified, and only calibration is typed when it checks wording, provenance, obligations, and release eligibility.

5. `on e0.accepted => accept`

   When `e0` (epistemic status calibration) reports `accepted` (accepted), the program accepts the calibrated result for workflow purposes. Acceptance does not create additional scientific warrant.

   **Concrete physics example:** The paper labels the result as a finite-volume conditional bound, cites the audit, and states the missing continuum theorem, so release is accepted.

6. `on e0.stopped => stop`

   When `e0` (epistemic status calibration) reports `stopped` (stopped), the program stops. This is a workflow disposition and does not by itself prove the negation of a claim.

   **Concrete physics example:** The abstract says the mass gap has been established even though uniformity is open, so release is stopped.

7. `}`

   Ends the `cohere_fast_manuscript_release` reasoning definition.

   **Physics context:** This closes the physics example with every claim still limited by the scope, premises, negative findings, and open obligations stated above.
