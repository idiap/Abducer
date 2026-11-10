<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reasoning Progress Log

- Target: `yang-mills-existence-and-mass-gap-target`
- Events: 12

## Progression

### Yang-Mills target spine is active

The active analysis is anchored to the Clay Yang-Mills target: construct a nontrivial four-dimensional compact-gauge quantum field theory and prove a positive mass gap in that same theory. Every later claim must preserve the gauge-field object, OS/Wightman adequacy, continuum limit, nontriviality, and spectral gap.

- Phase: `target-spine`
- Type: `target_spine`
- Epistemic status: `evidence-backed`
- Conceptual move: Make the physical target object explicit before considering construction or spectral mechanisms.
- Target commitments: `existence, nontriviality, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Evidence: `KB/yang-mills-existence-and-mass-gap.kb.md, agentic/state/essential_target_ledgers/yang-mills-existence-and-mass-gap.json, agentic/state/current_target.json`
- Proof obligations:
  - Preserve existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap in every active route.
- Uncertainty: The target spine is controlled, but no mathematical proof route is promoted by this event.

### Dependency frontier exposes unresolved mathematical interfaces

The active dependency graph exposes 76 unresolved mathematical interfaces among 97 tracked objects: definitions of the gauge theory, OS reconstruction, continuum passage, nontriviality witnesses, and spectral-gap transfer. These are not administrative tasks; they are the places where the physics mechanism can fail.

- Phase: `dependency-frontier`
- Type: `dependency_frontier`
- Epistemic status: `proof-obligation`
- Conceptual move: Expose which mathematical interfaces must be supplied before a Yang-Mills gap claim has physical meaning.
- Target commitments: `existence, nontriviality, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Evidence: `agentic/state/dependency_graphs/yang-mills-existence-and-mass-gap.json, agentic/reports/dependency_closure/yang-mills-existence-and-mass-gap.md`
- Proof obligations:
  - Resolve or demote 76 open frontier nodes.
- Uncertainty: Frontier nodes are route obligations, not proof dependencies, until later validation discharges them.

### Conceptual pressure has been extracted from the frontier

The exploration layer isolated 22 tensions and 16 candidate mechanisms in the Yang-Mills space. The useful tensions are physical ones: ultraviolet construction versus infrared mass generation, Euclidean positivity versus Hamiltonian reconstruction, and lattice evidence versus continuum same-theory transfer.

- Phase: `conceptual-pressure`
- Type: `conceptual_pressure`
- Epistemic status: `conjectural`
- Conceptual move: Turn unresolved physics interfaces into explicit mechanism candidates with failure conditions.
- Target commitments: `existence, nontriviality, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Evidence: `artifacts/hegelian/hypothesis_exploration_map.json, artifacts/hegelian/failure_signal_cartography.json`
- Proof obligations:
  - Attach each generated route to target commitments and disconfirming observations before continuation.
- Uncertainty: Creative pressure can widen the search space but must be filtered by target relevance and validation gates.

### Route candidate 1: proof_obligation_factorization -> proof_queue

This candidate treats multiscale Yang-Mills control as a construction question: can regulated non-Abelian gauge-field measures be controlled through ultraviolet cutoff removal so that a non-Gaussian, reflection-positive continuum vacuum sector remains? Operationally it is marked `proof_queue` only to control sequencing; the substantive question is whether the named objects, observables, limiting regime, and transfer theorem can be made same-theory.

- Phase: `candidate-01`
- Type: `route_ranking`
- Epistemic status: `proof-obligation`
- Conceptual move: Translate a route candidate into a same-theory mechanism question about construction, observables, limits, and spectrum.
- Target commitments: `existence, nontriviality, continuum-limit, positive-mass-gap`
- Evidence: `artifacts/hegelian/candidate_rankings.json, artifacts/hegelian/mediation_candidates.json, artifacts/hegelian/validation_packets.json`
- Proof obligations:
  - Preserve compact simple gauge-group Yang-Mills structure through the RG block-spin/effective-action construction.
  - Name the exact Balaban estimates that would produce constructive existence rather than only small-field or cutoff control.
  - Show that the limiting measure is interacting and non-Gaussian, not a trivial ultraviolet fixed point.
  - Explain how ultraviolet stability plus effective-action convergence addresses the four-dimensional continuum-limit bottleneck.
- Uncertainty: The ranking is only a sequencing device; physical progress requires the bridge assumptions and failure tests to be discharged.

### Route candidate 2: proof_obligation_factorization -> proof_queue

This candidate treats Euclidean decay as a spectral question: can gauge-invariant time correlations in the same continuum vacuum have spectral measures with support bounded away from zero, and can that exclusion survive OS reconstruction into the Hamiltonian spectrum? Operationally it is marked `proof_queue` only to control sequencing; the substantive question is whether the named objects, observables, limiting regime, and transfer theorem can be made same-theory.

- Phase: `candidate-02`
- Type: `route_ranking`
- Epistemic status: `proof-obligation`
- Conceptual move: Translate a route candidate into a same-theory mechanism question about construction, observables, limits, and spectrum.
- Target commitments: `existence, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Evidence: `artifacts/hegelian/candidate_rankings.json, artifacts/hegelian/mediation_candidates.json, artifacts/hegelian/validation_packets.json`
- Proof obligations:
  - Preserve the Clay target by keeping OS/Wightman reconstruction, nontriviality, continuum limit, and Delta > 0 explicit.
  - Specify which Schwinger functions or gauge-invariant local observables witness exponential Euclidean time decay.
  - Show the decay statement is not a strong-coupling lattice-only artifact and survives as a nontrivial continuum theory.
  - State the cutoff-uniform estimates needed before the transfer-matrix gap can pass to the continuum limit.
- Uncertainty: The ranking is only a sequencing device; physical progress requires the bridge assumptions and failure tests to be discharged.

### Route candidate 3: proof_obligation_factorization -> discovery_branch

This candidate treats multiscale Yang-Mills control as a construction question: can regulated non-Abelian gauge-field measures be controlled through ultraviolet cutoff removal so that a non-Gaussian, reflection-positive continuum vacuum sector remains? Operationally it is marked `discovery_branch` only to control sequencing; the substantive question is whether the named objects, observables, limiting regime, and transfer theorem can be made same-theory.

- Phase: `candidate-03`
- Type: `validation_gate`
- Epistemic status: `conjectural`
- Conceptual move: Translate a route candidate into a same-theory mechanism question about construction, observables, limits, and spectrum.
- Target commitments: `existence, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Evidence: `artifacts/hegelian/candidate_rankings.json, artifacts/hegelian/mediation_candidates.json, artifacts/hegelian/validation_packets.json`
- Proof obligations:
  - Preserve compact simple gauge-group Yang-Mills structure through the RG block-spin/effective-action construction.
  - Name the exact Balaban estimates that would produce constructive existence rather than only small-field or cutoff control.
  - Show that the limiting measure is interacting and non-Gaussian, not a trivial ultraviolet fixed point.
  - Explain how ultraviolet stability plus effective-action convergence addresses the four-dimensional continuum-limit bottleneck.
- Uncertainty: The ranking is only a sequencing device; physical progress requires the bridge assumptions and failure tests to be discharged.

### Route candidate 4: proof_obligation_factorization -> discovery_branch

This candidate asks whether Euclidean Schwinger functions can be carried through reflection positivity into a positive-norm quantum Hilbert space before any spectral-gap claim is made. Operationally it is marked `discovery_branch` only to control sequencing; the substantive question is whether the named objects, observables, limiting regime, and transfer theorem can be made same-theory.

- Phase: `candidate-04`
- Type: `validation_gate`
- Epistemic status: `conjectural`
- Conceptual move: Translate a route candidate into a same-theory mechanism question about construction, observables, limits, and spectrum.
- Target commitments: `existence, nontriviality, os-wightman-adequacy, positive-mass-gap`
- Evidence: `artifacts/hegelian/candidate_rankings.json, artifacts/hegelian/mediation_candidates.json, artifacts/hegelian/validation_packets.json`
- Proof obligations:
  - Keep OS/Wightman adequacy as an explicit construction target rather than a post-hoc interpretation.
  - Name the Schwinger-function family and reconstruction theorem obligations needed for Yang-Mills on R^4.
  - Track nontriviality of the reconstructed field algebra and vacuum sector.
  - Show the Schwinger functions arise after the four-dimensional continuum limit, not only from a regulated model.
- Uncertainty: The ranking is only a sequencing device; physical progress requires the bridge assumptions and failure tests to be discharged.

### Formal subgoals are under explicit continuation control

Every active route now carries a control decision: persist by adaptation only while failure teaches a sharper premise, object, regime, or bridge; backtrack when a formula assumes an unbuilt premise; pivot after repeated certified failure; quarantine evidence or analogy routes; and stop subgoals that no longer teach the target loop.

- Phase: `formal-subgoal-control`
- Type: `subgoal_control_decision`
- Epistemic status: `proof-obligation`
- Conceptual move: Turn formula persistence into a public work-loop decision with blocker, learning-from-failure, next action, and demotion triggers.
- Target commitments: `existence, nontriviality, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Evidence: `agentic/spec/formal_subgoal_control.schema.json, docs/research-methods/formal-subgoal-control-policy.md, artifacts/hegelian/formal_subgoal_controls.json, artifacts/hegelian/candidate_rankings.json`
- Proof obligations:
  - persist_adapt: Adapt the Balaban RG continuum-control route into the next typed lemma by naming assumptions, constructed objects, validity regime, and the certification artifact that would change the route state.
  - persist_adapt: Adapt the Euclidean correlator-decay to spectral-gap route into the next typed lemma by naming assumptions, constructed objects, validity regime, and the certification artifact that would change the route state.
  - persist_adapt: Adapt the Balaban RG continuum-control route into the next typed lemma by naming assumptions, constructed objects, validity regime, and the certification artifact that would change the route state.
  - persist_adapt: Adapt the OS reconstruction and reflection-positivity bridge into the next typed lemma by naming assumptions, constructed objects, validity regime, and the certification artifact that would change the route state.
  - persist_adapt: Adapt the Constructive QFT existence route into the next typed lemma by naming assumptions, constructed objects, validity regime, and the certification artifact that would change the route state.
- Uncertainty: The control packet governs route continuation; it does not prove the mathematical subgoal. Generative review still has to judge whether the rationale is mathematically substantive.

### Previous workflow artifacts are isolated as historical

The stale-workflow preflight found 1018 historical artifacts but 0 critical active-state mismatches.

- Phase: `stale-workflow-guard`
- Type: `drift_guard`
- Epistemic status: `evidence-backed`
- Conceptual move: Keep old runs available as evidence without letting them masquerade as the current mathematical route.
- Target commitments: `existence, nontriviality, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Evidence: `agentic/reports/stale_workflows/latest.json, agentic/reports/stale_workflows/latest.md`
- Proof obligations:
  - Continue blocking report generation if active target IDs diverge.
- Uncertainty: Historical artifacts remain in the repository and must stay visually separated from active Yang-Mills reasoning.

### Proof-by-contradiction branches expose route pressure

The reductio branches now have physical carriers: a negative reflection form would block Hilbert-space reconstruction, triviality collapse would kill connected gauge-invariant cumulants, and no-gap would place spectral weight arbitrarily close to zero in the vacuum-orthogonal sector. Each branch asks whether those worlds are incompatible with one same continuum Yang-Mills object.

- Phase: `proof-by-contradiction`
- Type: `contradiction_route`
- Epistemic status: `proof-obligation`
- Conceptual move: Use contradiction as a controlled discovery instrument: exact negation, same-theory carrier, conflict target, proof obligations, and auditor handoff.
- Target commitments: `existence, nontriviality, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Evidence: `agentic/reports/yang_mills_bridge_lemma_packets/latest.json, agentic/reports/yang_mills_bridge_lemma_packets/latest.md, agentic/reports/proof_by_contradiction_validation/latest.json, skills/reasoning/kb-contradiction-strategist/SKILL.md, skills/evaluation/contradiction-route-auditor/SKILL.md`
- Proof obligations:
  - Audit each reductio branch before proof-queue promotion.
  - Reject branches that change cutoff, Hilbert space, observable algebra, or limiting object.
  - Record whether failed branches point to missing density, closedness, nontriviality, or uniform-decay input.
- Uncertainty: These branches are not proofs. They are high-value pressure tests whose success depends on density, closedness, nontriviality, and cutoff-uniform transfer obligations.

### Theoretical obligations spawned closely related empirical evidence requests

Empirical and numerical evidence is requested only when it is tied to a named Yang-Mills object: Wilson-loop or string-tension data for nontriviality, glueball correlators for spectral scale, reflection-positive lattice actions for OS transfer, or negative extrapolation evidence for cutoff leakage.

- Phase: `empirical-evidence-requests`
- Type: `evidence_request`
- Epistemic status: `evidence-backed`
- Conceptual move: Use empirical evidence to guide witness selection, calibrate plausibility, find negative evidence, or trigger demotion while preserving the theorem/proof boundary.
- Target commitments: `existence, nontriviality, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Evidence: `agentic/reports/empirical_evidence_requests/latest.json, agentic/reports/empirical_evidence_requests/latest.md, skills/ingest/evidence-acquisition-planner/SKILL.md`
- Proof obligations:
  - Keep empirical evidence behind explicit transfer-gap and proof-boundary fields.
  - Demote fixed-cutoff, finite-volume, non-gauge-invariant, or analogy-only evidence.
  - Use supportive empirical evidence to prioritize witness and uniformity obligations, not to mark proof success.
- Uncertainty: Empirical evidence can guide observable choice and stress-test transfer assumptions, but continuum Yang-Mills proof obligations remain live until same-theory transfer theorems are supplied.

### Reasoning monitor generation is controlled by packet and HTML gates

The Yang-Mills monitor is generated from a stable packet contract and then validated as a self-contained HTML artifact. This keeps the visible dashboard tied to the active target, evidence ledger, physics-facing route interpretations, stale-workflow preflight, and open mathematical obligations.

- Phase: `reasoning-monitor-gate`
- Type: `validation_gate`
- Epistemic status: `evidence-backed`
- Conceptual move: Treat the report as a controlled observability surface rather than an informal rendering of hidden state.
- Target commitments: `existence, nontriviality, os-wightman-adequacy, continuum-limit, positive-mass-gap`
- Evidence: `agentic/spec/reasoning_monitor_packet.schema.json, agentic/scripts/build_reasoning_monitor_packet.py, agentic/scripts/generate_reasoning_monitor_html.py, agentic/scripts/validate_reasoning_monitor.py, agentic/reports/reasoning_monitor/latest.json, agentic/reports/reasoning_monitor/latest.html, tests/reporting/test_reasoning_monitor_html.py, tests/generative/test_reasoning_monitor_visual_quality.md, docs/reference/reasoning-monitor-visual-grammar.md, docs/operations/reasoning-monitor-runbook.md`
- Proof obligations:
  - Regenerate and validate the monitor whenever the active reasoning loop advances.
- Uncertainty: The monitor can show controlled progress and open mathematical obligations, but it must never be read as theorem completion.
