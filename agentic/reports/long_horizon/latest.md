<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Long-Horizon Yang-Mills Probe

- Target: `yang-mills-existence-and-mass-gap-target`
- Quality gate: `pass`
- Critical findings: 0

## Metrics

- `reasoning_events`: 12
- `frontier_total`: 76
- `candidate_routes`: 16
- `proof_obligations`: 247
- `proof_queue_budget`: 2
- `proof_queue_count`: 2
- `discovery_branch_count`: 11
- `missing_evidence_count`: 0
- `stale_critical_findings`: 0
- `subgoal_control_count`: 16
- `stale_repeated_blockers`: 0
- `machinery_selection_count`: 16

## Active Mechanism Candidates

### candidate.99d7c53a3321

- Operation: `proof_obligation_factorization`
- Route family: `Balaban RG continuum-control route`
- Physics story: Regulated non-Abelian gauge fields must remain controlled under scale integration so that cutoff removal leaves a non-Gaussian, reflection-positive continuum vacuum sector with gauge-invariant observables that can witness interaction.
- Physical failure mode: The mechanism fails if the limit is only finite-volume/fixed-cutoff, if reflection positivity is not closed in the limiting topology, if all connected gauge-invariant observable witnesses collapse to a Gaussian/free theory, or if no same-theory spectral witness can be extracted.
- Target relevance: `0.97`
- Commitments: `existence, nontriviality, continuum-limit, positive-mass-gap`
- Domain terms: `continuum limit, mass gap, balaban, renormalisation, renormalization`
- Transformation: Test the Balaban renormalisation-group mechanism: scale-by-scale control of regulated non-Abelian gauge fields must survive ultraviolet cutoff removal as a non-Gaussian, OS-positive continuum Yang-Mills object, and that same object must still supply a gauge-invariant spectral witness for the mass gap.
- Source witness: cross-component structural bridge with st.rem.continuum-limit-bottleneck; concept focus: multiscale-renormalization-control, rigorous-Yang-Mills-construction, positive-mass-gap, constructive-existence
- First obligations:
  - Preserve compact simple gauge-group Yang-Mills structure through the RG block-spin/effective-action construction.
  - Name the exact Balaban estimates that would produce constructive existence rather than only small-field or cutoff control.
  - Show that the limiting measure is interacting and non-Gaussian, not a trivial ultraviolet fixed point.
  - Explain how ultraviolet stability plus effective-action convergence addresses the four-dimensional continuum-limit bottleneck.

### candidate.3e9a722a8615

- Operation: `proof_obligation_factorization`
- Route family: `Euclidean correlator-decay to spectral-gap route`
- Physics story: Gauge-invariant Euclidean time correlations in the continuum Yang-Mills object must have spectral measures with support bounded away from zero, and the same observable family must survive OS reconstruction densely enough to control the physical excitation sector.
- Physical failure mode: The mechanism fails if decay constants vanish under cutoff removal, if the observables are not gauge invariant or spectrally determining, or if the gap only exists in a regulated lattice Hilbert space.
- Target relevance: `0.97`
- Commitments: `existence, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Domain terms: `transfer matrix, lattice continuum, wightman, mass gap, correlator decay, constructive qft`
- Transformation: Test the Euclidean spectral mechanism: gauge-invariant Schwinger-function correlations must decay with cutoff-uniform rates, reflection positivity must reconstruct the physical Hilbert space, and the corresponding spectral measures must have support bounded away from zero in the vacuum-orthogonal sector.
- Source witness: cross-component structural bridge with st.def.mass-gap; concept focus: lattice-continuum-control-implies-constructive-QFT, transfer-matrix-gap-implies-correlator-decay, correlator-decay-signals-mass-gap, OS-axioms-imply-Wightman-QFT
- First obligations:
  - Preserve the Clay target by keeping OS/Wightman reconstruction, nontriviality, continuum limit, and Delta > 0 explicit.
  - Specify which Schwinger functions or gauge-invariant local observables witness exponential Euclidean time decay.
  - Show the decay statement is not a strong-coupling lattice-only artifact and survives as a nontrivial continuum theory.
  - State the cutoff-uniform estimates needed before the transfer-matrix gap can pass to the continuum limit.

## Discovery Branches Held By Sequencing Budget

- `candidate.ad2de78c31a3` `proof_obligation_factorization` score `0.97` terms `reflection positivity, transfer matrix, continuum limit, lattice continuum, correlator decay, renormalization, constructive qft`
- `candidate.10e1e3bfea64` `proof_obligation_factorization` score `0.93` terms `reflection positivity, os reconstruction, wightman, mass gap`
- `candidate.2204023252aa` `proof_obligation_factorization` score `0.93` terms `wightman, mass gap, hamiltonian, constructive qft`
- `candidate.751b5542b03c` `proof_obligation_factorization` score `0.9` terms `wightman, mass gap, constructive qft`
- `candidate.517bf48d1bbc` `proof_obligation_factorization` score `0.9` terms `os reconstruction, wightman, mass gap`
- `candidate.c5b0aecb2355` `proof_obligation_factorization` score `0.9` terms `reflection positivity, transfer matrix, wightman, mass gap, hamiltonian, correlator decay`

## Commitment Coverage

- Required: `existence, nontriviality, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Covered by active proof queue: `continuum-limit, existence, nontriviality, os-wightman-adequacy, positive-mass-gap`
- Missing: `none`

## Findings

None.

## Pipeline Observations

- Active mechanism candidates must survive a physics/math interpretation pass: they must name gauge-field objects, observables, limits, and spectral meaning.
- The proof-queue budget is a sequencing control; it is not the explanation. The explanation lives in whether the RG and decay mechanisms can meet in one continuum theory.
- The active monitor remains stale-safe when missing evidence and stale critical findings are zero, but mathematical progress still depends on same-theory bridge lemmas.
- Reorientation control should diagnose physical obstruction types: cutoff leakage, loss of reflection positivity, Gaussian collapse, weak observable sector, or vanishing decay scale.
- Skill use is maximal only when the current physical obstruction triggers the right evidence, review, proof, or reporting skill, not when every skill is invoked indiscriminately.

## Skill Ecosystem Coherence

- Status: `pass`
- Critical findings: `0`
- Policy: Maximal skill use means phase-complete composition with conditional dispatch, not firing every skill in every iteration. Control-plane skills govern the target loop; discovery/evaluation/reasoning skills act in conceptual refinement; ingest, review, and reporting skills remain available as triggered evidence, stress-test, and handoff pools.
- `projected_skill_count`: 200
- `direct_workflow_skill_count`: 94
- `projected_conditional_skill_count`: 106
- `workflow_count`: 6
- Phase `target_navigation` via `target-navigation-control-plane`: `role-complete`
  - Why consistent: This phase controls goals, dependencies, hooks, validation, release, and handoff; it should stay lean and not run every discovery/review skill directly.
  - Skills: `looper-target-goal-enricher, looper-target-dependency-cartographer, looper-workflow-contract-governor, looper-hook-policy-maintainer, looper-release-promoter, kb-orchestrator, work`
- Phase `conceptual_refinement` via `conceptual-obstruction-refinement`: `role-complete`
  - Why consistent: This phase carries the dense discovery stack: conceptual pressure, failure signals, induction, abduction, deduction, bridge planning, obligation gates, counterfactual probes, ledgers, proof critique, ranking, and work-loop handoff.
  - Skills: `looper-workflow-contract-governor, looper-target-dependency-cartographer, abducer-conceptual-pressure-formalizer, abducer-failure-signal-cartographer, kb-induce, kb-abduce, kb-deduce, kb-contradiction-strategist, kb-concept-bridge-planner, kb-gap-abstraction-conjecturer, abducer-mediation-candidate-generator, kb-promising-direction-assessor`
- Phase `conditional_pools` via `triggered-by-frontier-or-handoff`: `available`
  - Why consistent: These skills should be invoked when the route demands prior-art intake, persona stress testing, or expert-facing compression, rather than bloating every control-plane cycle.
  - Review pool: `review-reasoner, review-reasoner-concept-logician, review-reasoner-discovery-scientist, review-reasoner-epistemologist, review-reasoner-fields-medalist, review-reasoner-radical-designer`
  - Ingest pool: `evidence-acquisition-planner, latex-kb-ingest, prior-art-importer, pvsnp-kb-parser, target-literature-source-curator, theorem-body-normalizer`
  - Reporting pool: `endpoint-worked-calculation-packager, expert-handoff, finite-theorem-section-packager, kb-expert-paper-generator, kb-macro-proof-paper-writer, prior-art-positioning-packager, scientific-contribution-paper-handoff, subgoal-enablement-handoff-packager, target-literature-evolution-narrator, timeline-claim-boundary-auditor, timeline-contribution-explainer, timeline-contribution-stater, timeline-cycle-latex-translator, timeline-definition-assumption-elicitor, timeline-failed-route-interpreter, timeline-formal-physics-deriver, timeline-narrative-coherence-guard, timeline-organizing-diagram-builder, timeline-paper-argument-architect, timeline-paper-cross-section-reconciler, timeline-paper-section-synthesizer, timeline-paper-workflow-orchestrator, timeline-problem-literature-latex-translator, timeline-problem-space-narrator, timeline-reference-manager, timeline-report-evidence-ingestor, timeline-report-latex-composer, timeline-story-latex-translator, timeline-summary-latex-translator`

## Reorientation Control

Physically, the active routes are not competing stories about different problems. They are two incomplete views of one Yang-Mills mechanism. The Balaban/RG route asks whether the non-Abelian gauge-field ensemble can be controlled from the ultraviolet cutoff to a non-Gaussian continuum vacuum with reflection-positive Schwinger functions. The correlator route asks whether gauge-invariant observables in that same vacuum have Euclidean time spectral measures whose support stays away from zero, which would exclude arbitrarily light physical excitations after reconstruction. Neither view is disposable: RG without an infrared spectral witness constructs no gap, while decay without continuum object identity and observable density may only describe a regulated or too-small sector. The correct next motion is a bridge-focused restrategy that proves or falsifies same-theory transfer across cutoff removal, OS reconstruction, nontriviality, and spectral support.

- Current recommendation: `restrategize_without_wholesale_pivot`
  - Rationale: Do not pivot away from the current routes merely because the mathematical obstruction is hard. The live physical question is whether scale-controlled gauge-field construction can feed a Euclidean spectral measure argument in the same continuum theory. The honest move is to type that bridge: source objects, observable algebra, limiting regime, spectral measure, and disqualifying failure modes.
  - Pivot guard: Pivot only after the relevant physical obstruction has repeated under certification: no continuum object, no reflection positivity, no nontrivial connected sector, no observable density, or no cutoff-uniform spectral lower bound.
- Max reflection passes before action: `2`
  - Stop reflecting when: the next action is only a paraphrase of the previous action
  - Stop reflecting when: no route-level obstruction type changes after two passes
  - Stop reflecting when: the loop cannot name a same-theory object connecting construction, reconstruction, and spectral claims
- Route `candidate.99d7c53a3321` -> `restrategize`
  - Obstruction: construction-to-reconstruction bridge missing
  - Next probe: Name the exact regulated input objects, limiting Schwinger-function output, and reflection-positivity preservation theorem.
- Route `candidate.3e9a722a8615` -> `restrategize-with-pivot-test`
  - Obstruction: spectral witness lacks cutoff-uniform transfer
  - Next probe: Formulate the decay-to-gap lemma with OS positivity, spectral measure support, observable density, and cutoff-uniform constants.
- `restrategize` `reorient-01-bridge-rg-to-os`: Formulate the bridge lemma from Balaban-style RG control to OS-positive continuum Schwinger functions.
  - Why now: It is the shared missing hinge between construction and spectral-gap routes.
  - Success condition: The lemma names assumptions, output objects, failure tests, and the same-theory invariant.
- `backtrack` `reorient-02-backtrack-hamiltonian-premises`: Move every Hamiltonian spectral claim behind explicit OS reconstruction premises.
  - Why now: The Hamiltonian route is a useful endpoint but becomes misleading if H_YM is assumed.
  - Success condition: Every occurrence of H, Omega, and P_perp has a reconstruction source or is marked as an open premise.
- `pivot-test` `reorient-03-pivot-test-correlator-uniformity`: Probe whether correlator decay can be made cutoff-uniform; if not, pivot priority toward construction/nontriviality.
  - Why now: A nonuniform decay estimate would be a beautiful dead end for the Clay target.
  - Success condition: The loop records whether constants remain bounded below through cutoff removal.
- `quarantine` `reorient-04-quarantine-analogies`: Keep lattice-only, strong-coupling, or lower-dimensional analogies out of the proof queue unless they carry transfer certificates.
  - Why now: These ideas are valuable for intuition but dangerous for target drift.
  - Success condition: Every analogy is stored as an evidence task with explicit transfer obligations.

## Formal Subgoal Control

- Active controls: `16`
- Decision counts: `{'persist_adapt': 13, 'backtrack': 2, 'pivot': 0, 'quarantine': 1, 'stop': 0}`
- Stale repeated blockers: `0`
- `persist_adapt` Balaban RG continuum-control route acting on intervention:st.thm.balaban-s-rigorous-renormalisation-group-analysi
  - Learning: The current obstruction is informative because it identifies the next missing bridge rather than invalidating the route family.
  - Next action: Adapt the Balaban RG continuum-control route into the next typed lemma by naming assumptions, constructed objects, validity regime, and the certification artifact that would change the route state.
- `persist_adapt` Euclidean correlator-decay to spectral-gap route acting on intervention:st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu
  - Learning: The current obstruction is informative because it identifies the next missing bridge rather than invalidating the route family.
  - Next action: Adapt the Euclidean correlator-decay to spectral-gap route into the next typed lemma by naming assumptions, constructed objects, validity regime, and the certification artifact that would change the route state.
- `persist_adapt` Balaban RG continuum-control route acting on intervention:st.rem.continuum-limit-bottleneck
  - Learning: The current obstruction is informative because it identifies the next missing bridge rather than invalidating the route family.
  - Next action: Adapt the Balaban RG continuum-control route into the next typed lemma by naming assumptions, constructed objects, validity regime, and the certification artifact that would change the route state.
- `persist_adapt` OS reconstruction and reflection-positivity bridge acting on intervention:st.prob.yang-mills-existence-mass-gap
  - Learning: The current obstruction is informative because it identifies the next missing bridge rather than invalidating the route family.
  - Next action: Adapt the OS reconstruction and reflection-positivity bridge into the next typed lemma by naming assumptions, constructed objects, validity regime, and the certification artifact that would change the route state.
- `persist_adapt` Constructive QFT existence route acting on intervention:st.def.wightman-qft
  - Learning: The current obstruction is informative because it identifies the next missing bridge rather than invalidating the route family.
  - Next action: Adapt the Constructive QFT existence route into the next typed lemma by naming assumptions, constructed objects, validity regime, and the certification artifact that would change the route state.
- `persist_adapt` Constructive QFT existence route acting on intervention:st.thm.constructive-qft-in-low-dimension-examples-with-
  - Learning: The current obstruction is informative because it identifies the next missing bridge rather than invalidating the route family.
  - Next action: Adapt the Constructive QFT existence route into the next typed lemma by naming assumptions, constructed objects, validity regime, and the certification artifact that would change the route state.

## Machinery Portfolio

- Interpretation: The route portfolio is coherent only when construction, transfer, witness, and validation roles are all visible. For Yang-Mills this means RG construction cannot replace OS transfer, correlator decay cannot replace continuum construction, and Hamiltonian language remains endpoint validation unless reconstruction premises are supplied.
- Selection count: `16`
- Role counts: `{'construction': 3, 'representation': 7, 'invariant_preservation': 0, 'transfer': 14, 'witness': 7, 'obstruction': 2, 'validation': 16}`
- Missing core roles: `none`
- `construction` renormalisation group and multiscale control
  - Controlled interface: regulated gauge-field measures or effective actions -> continuum Schwinger-function object
  - Bridge obligation: RG-to-OS bridge lemma with topology, limiting objects, positivity preservation, and nontriviality witness.
- `witness` Euclidean correlator decay and spectral-measure analysis
  - Controlled interface: gauge-invariant Euclidean time correlations -> Hamiltonian spectral support away from zero
  - Bridge obligation: Decay-to-gap lemma with OS reconstruction, observable density, and cutoff-uniform constants.
- `construction` renormalisation group and multiscale control
  - Controlled interface: regulated gauge-field measures or effective actions -> continuum Schwinger-function object
  - Bridge obligation: RG-to-OS bridge lemma with topology, limiting objects, positivity preservation, and nontriviality witness.
- `transfer` Osterwalder-Schrader reconstruction
  - Controlled interface: OS-positive Schwinger functions -> Hilbert space, vacuum, observables, and Hamiltonian
  - Bridge obligation: OS reconstruction packet with positivity, domain, vacuum, and spectral semantics.
- `obstruction` target-led abstraction refinement
  - Controlled interface: untyped route pressure -> typed bridge obligation
  - Bridge obligation: Machinery-classification lemma naming the controlled interface and invalid-use modes.
- `obstruction` target-led abstraction refinement
  - Controlled interface: untyped route pressure -> typed bridge obligation
  - Bridge obligation: Machinery-classification lemma naming the controlled interface and invalid-use modes.

## Residual Weak Zones

- The Balaban/RG mechanism still has to show that scale control produces OS-positive continuum Schwinger functions rather than merely stable cutoff actions.
- The correlator-decay mechanism still has to show cutoff-uniform spectral support away from zero for a gauge-invariant observable family dense enough to see physical excitations.
- The nontriviality witness must be a connected gauge-invariant observable in the same limiting Schwinger family used for reconstruction and gap analysis.
- The next Yang-Mills pass should trigger ingest, review, or reporting skills only when a bridge lemma names a precise theorem target, observable family, or expert-checkable claim.
