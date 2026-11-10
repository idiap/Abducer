# Epistemic Hardness: yang-mills-existence-and-mass-gap

## Summary

yang-mills-existence-and-mass-gap is hard in this KB because global targets are framed across multiple incompatible proof regimes, barrier theorems restrict generic techniques, and explicit dependencies are sparse, forcing hypothesis-driven bridge construction.

## KB Stats

- Statements: 36
- Dependency edges: 16
- Missing dependency refs: 0
- Top entry points considered: 10
- Concept phases in top entry points: 4
- Conceptual hypotheses: 12
- Barrier families: 1

## Concept Communication Trace

- Phase pressure (top entrypoints): Current Bridge Agenda=6, Foundational Gauge-Theoretic Definitions=1, Mass-Gap and Spectral Transfer=1

### Entrypoint Concept Anchors
- `st.def.wightman-qft` [definition] phase=Current Bridge Agenda score=0.7082
  - concept: A Wightman QFT is the standard Minkowski-space axiomatic formulation of a quantum field theory with locality, vacuum, and spectral conditions.
- `st.def.mass-gap` [definition] phase=Current Bridge Agenda score=0.6731
  - concept: A mass gap means the vacuum is isolated and the first excitation energy is at least some positive Delta.
- `st.def.os-euclidean-qft` [definition] phase=Current Bridge Agenda score=0.6632
  - concept: An OS Euclidean QFT is the Euclidean axiomatic formulation that supports reconstruction of a Minkowski theory when reflection positivity and the other OS conditions hold.
- `st.def.compact-simple-gauge-group` [definition] phase=Foundational Gauge-Theoretic Definitions score=0.6521
  - concept: The gauge group in the Clay problem is a compact simple Lie group equipped with the invariant structure needed to define Yang-Mills theory.
- `st.def.osterwalder-schrader-os-euclidean-qft` [definition] phase=Current Bridge Agenda score=0.5843
  - concept: An emph OS Euclidean QFT is specified by a collection of Euclidean n -point Schwinger functions (S_n)_ nge 0 (tempered distributions on R^ 4n ) satisfying: Euclidean invariance, symmetry, reflection positivity, regula...
- `st.thm.os-reconstruction-and-equivalence-with-wightman-` [theorem] phase=Current Bridge Agenda score=0.5658
  - concept: If (S_n) satisfy the OS axioms, then there exists a corresponding Wightman QFT on Minkowski space whose Wightman distributions analytically continue to (S_n) . Conversely, (under standard hypotheses) Wightman theories...

### Intervention Concept Anchors
- `st.def.os-euclidean-qft` [definition] score=0.5208 partner=st.def.osterwalder-schrader-os-euclidean-qft
  - rationale: supports 3 downstream statements; cross-component structural bridge with st.def.osterwalder-schrader-os-euclidean-qft; concept focus: OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-...
  - concepts: OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction
- `st.def.mass-gap` [definition] score=0.5123 partner=st.def.mass-gap-in-hamiltonian-wightman-terms
  - rationale: supports 2 downstream statements; high bridge centrality; cross-component structural bridge with st.def.mass-gap-in-hamiltonian-wightman-terms; concept focus: transfer-matrix-gap-implies-correlator-decay, correlator-d...
  - concepts: transfer-matrix-gap-implies-correlator-decay, correlator-decay-signals-mass-gap, reflection-positivity-and-transfer-matrix, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction
- `st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu` [theorem] score=0.4735 partner=st.def.mass-gap
  - rationale: cross-component structural bridge with st.def.mass-gap; concept focus: lattice-continuum-control-implies-constructive-QFT, transfer-matrix-gap-implies-correlator-decay, correlator-decay-signals-mass-gap, OS-axioms-imp...
  - concepts: lattice-continuum-control-implies-constructive-QFT, transfer-matrix-gap-implies-correlator-decay, correlator-decay-signals-mass-gap, OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix
- `st.def.osterwalder-schrader-os-euclidean-qft` [definition] score=0.4692 partner=st.def.os-euclidean-qft
  - rationale: cross-component structural bridge with st.def.os-euclidean-qft; concept focus: OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamilt...
  - concepts: OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction
- `st.thm.os-reconstruction-and-equivalence-with-wightman-` [theorem] score=0.4626 partner=st.def.os-euclidean-qft
  - rationale: cross-component structural bridge with st.def.os-euclidean-qft; concept focus: lattice-continuum-control-implies-constructive-QFT, OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and...
  - concepts: lattice-continuum-control-implies-constructive-QFT, OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, multiscale-renormalization-control
- `st.def.wightman-qft` [definition] score=0.4573 partner=st.thm.constructive-qft-in-low-dimension-examples-with-
  - rationale: supports 4 downstream statements; cross-component structural bridge with st.thm.constructive-qft-in-low-dimension-examples-with-; concept focus: rigorous-Yang-Mills-construction, constructive-existence, Hamiltonian-ma...
  - concepts: rigorous-Yang-Mills-construction, constructive-existence, Hamiltonian-mass-gap, Wightman-QFT, classical-Yang-Mills-PDE

### Pathway Concept Anchors
- `path.001` phase=Current Bridge Agenda score=0.6441 entry=st.def.wightman-qft
  - goal: Develop a proof pathway centered on st.def.wightman-qft.
- `path.003` phase=Current Bridge Agenda score=0.6308 entry=st.def.os-euclidean-qft
  - goal: Develop a proof pathway centered on st.def.os-euclidean-qft.
- `path.002` phase=Current Bridge Agenda score=0.6228 entry=st.def.mass-gap
  - goal: Develop a proof pathway centered on st.def.mass-gap.
- `path.004` phase=Foundational Gauge-Theoretic Definitions score=0.6138 entry=st.def.compact-simple-gauge-group
  - goal: Develop a proof pathway centered on st.def.compact-simple-gauge-group.
- `path.006` phase=Current Bridge Agenda score=0.5766 entry=st.thm.os-reconstruction-and-equivalence-with-wightman-
  - goal: Develop a proof pathway centered on st.thm.os-reconstruction-and-equivalence-with-wightman-.

### Barrier Connection Fronts
- barrier `st.thm.os-reconstruction-and-equivalence-with-wightman-` <-> entry `st.def.os-euclidean-qft` (score=0.5811, type=bridge)
- barrier `st.thm.donaldson-s-gauge-theoretic-constraints-on-smoot` <-> entry `st.def.compact-simple-gauge-group` (score=0.5666, type=bridge)
- barrier `st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu` <-> entry `st.def.os-euclidean-qft` (score=0.5629, type=bridge)
- barrier `st.thm.constructive-qft-in-low-dimension-examples-with-` <-> entry `st.def.wightman-qft` (score=0.5629, type=bridge)
- barrier `st.thm.os-reconstruction-and-equivalence-with-wightman-` <-> entry `st.def.wightman-qft` (score=0.562, type=bridge)
- barrier `st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu` <-> entry `st.def.mass-gap` (score=0.5518, type=bridge)

## Essential Elements

| element | severity | score | key evidence |
|---|---|---|---|
| Barrier Stack Constraints | high | 1.0 | barrier_theorems=17, total_theorems=17 |
| Bridge-Hypothesis Dependence | high | 1.0 | connection_candidates=40, proof_hypotheses=44, pathway_count=8 |
| Sparse Explicit Dependency Structure | medium | 0.5556 | statement_count=36, dependency_edges=16, missing_dependency_refs=0 |
| Plural, Underdetermined Strategy Space | medium | 0.5 | distinct_top_entrypoint_phases=['Bottlenecks, Barriers, and Open Gaps', 'Current Bridge Agenda', 'Foundational Gauge-Theoretic Definitions', 'Mass-Gap and Spectral Transfer'], top_entrypoints_used=10 |
| Asymmetric Lower-Bound Evidence | moderate | 0.0 | restricted_lower_bounds=0, grand_target_related_theorems=0 |

### Barrier Stack Constraints
- Severity: high (1.0)
- Diagnosis: Multiple barrier theorems constrain broad proof templates and force barrier-aware method design.
- Evidence IDs: st.thm.os-reconstruction, st.thm.bpst-instanton-existence-prototype-instanton, st.thm.adhm-classification-all-instantons-on-s-4, st.thm.uhlenbeck-gauge-fixing-and-compactness, st.thm.existence-of-minimisers-for-yang-mills-functiona, st.thm.global-classical-well-posedness-in-3-1-dimension, st.thm.yang-mills-on-riemann-surfaces-atiyah-bott, st.thm.donaldson-s-gauge-theoretic-constraints-on-smoot

### Bridge-Hypothesis Dependence
- Severity: high (1.0)
- Diagnosis: Progress currently depends on conjectural bridges/hypotheses to connect otherwise weakly linked conceptual regions.
- Evidence IDs: st.def.os-euclidean-qft, st.def.mass-gap, st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu, st.def.osterwalder-schrader-os-euclidean-qft, st.thm.os-reconstruction-and-equivalence-with-wightman-, st.def.wightman-qft

### Sparse Explicit Dependency Structure
- Severity: medium (0.5556)
- Diagnosis: Most canonical statements are not yet wired by formal depends_on links, so proof navigation is underdetermined.

### Plural, Underdetermined Strategy Space
- Severity: medium (0.5)
- Diagnosis: Top entry points span multiple conceptual phases, indicating no single dominant route and high epistemic underdetermination.
- Evidence IDs: st.def.wightman-qft, st.def.mass-gap, st.def.os-euclidean-qft, st.def.compact-simple-gauge-group, st.def.osterwalder-schrader-os-euclidean-qft, st.thm.os-reconstruction-and-equivalence-with-wightman-, st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu, st.thm.reflection-positivity-and-transfer-matrix-for-la

### Asymmetric Lower-Bound Evidence
- Severity: moderate (0.0)
- Diagnosis: The KB has strong restricted-model lower bounds but relatively fewer direct bridges to full separation targets.

## Anti-Barrier Programs

### anti-barrier.001 - untyped-barrier
- Barrier IDs: st.thm.os-reconstruction, st.thm.bpst-instanton-existence-prototype-instanton, st.thm.adhm-classification-all-instantons-on-s-4, st.thm.uhlenbeck-gauge-fixing-and-compactness, st.thm.existence-of-minimisers-for-yang-mills-functiona, st.thm.global-classical-well-posedness-in-3-1-dimension, st.thm.yang-mills-on-riemann-surfaces-atiyah-bott, st.thm.donaldson-s-gauge-theoretic-constraints-on-smoot
- Minimal conceptual changes:
  - Introduce intermediate invariant that is not preserved by the barrier regime.
  - Search for representation-shift that maps target to a non-barrier proof model.
  - Use analogy-transfer from a neighboring regime with stronger lower-bound behavior.
- Research program:
  - Generate barrier-escape-principle hypotheses tied to top unresolved targets.
  - Run deduction checks on re-encoded target statements in scratch KB branches.
  - Retain only changes with non-negative coherence delta and positive entailment gain.

## Recommended Focus

1. Prioritize top-2 high-severity elements first in the abductive loop.
2. Convert top bridge hypotheses into scratch dependency tests and run deduce checks.
3. Backfill explicit depends_on links for highest-ranked entrypoint clusters.
4. For each barrier family, run the paired anti-barrier program and keep only coherence-positive re-encodings.
