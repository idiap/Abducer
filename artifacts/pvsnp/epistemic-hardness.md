# Epistemic Hardness: p-vs-np

## Summary

p-vs-np is hard in this KB because global targets are framed across multiple incompatible proof regimes, barrier theorems restrict generic techniques, and explicit dependencies are sparse, forcing hypothesis-driven bridge construction.

## KB Stats

- Statements: 64
- Dependency edges: 0
- Missing dependency refs: 0
- Top entry points considered: 10
- Concept phases in top entry points: 3
- Conceptual hypotheses: 12
- Barrier families: 3

## Essential Elements

| element | severity | score | key evidence |
|---|---|---|---|
| Sparse Explicit Dependency Structure | high | 1.0 | statement_count=64, dependency_edges=0, missing_dependency_refs=0 |
| Asymmetric Lower-Bound Evidence | medium | 0.6667 | restricted_lower_bounds=4, grand_target_related_theorems=6 |
| Bridge-Hypothesis Dependence | medium | 0.6562 | connection_candidates=40, proof_hypotheses=44, pathway_count=8 |
| Plural, Underdetermined Strategy Space | moderate | 0.375 | distinct_top_entrypoint_phases=['1) Foundational language of complexity', '8) Proof complexity as a parallel route', 'Paragraph: Proof complexity.'], top_entrypoints_used=10 |
| Barrier Stack Constraints | moderate | 0.1071 | barrier_theorems=3, total_theorems=28 |

### Sparse Explicit Dependency Structure
- Severity: high (1.0)
- Diagnosis: Most canonical statements are not yet wired by formal depends_on links, so proof navigation is underdetermined.

### Asymmetric Lower-Bound Evidence
- Severity: medium (0.6667)
- Diagnosis: The KB has strong restricted-model lower bounds but relatively fewer direct bridges to full separation targets.
- Evidence IDs: st.thm.h-stad-near-optimal-0-lower-bounds-for-parity-ha, st.thm.monotone-lower-bounds-for-clique-exemplar-razbor, st.thm.resolution-php-lower-bounds-exemplar-buss1988, st.thm.bounded-depth-frege-php-lower-bounds-beamepitass, st.thm.cook-levin-sat-is-np-complete-cook1971, st.thm.karp-many-natural-problems-are-np-complete-karp1, st.thm.nonuniform-separation-target, st.thm.karp-lipton-np-in-collapses-karplipton1980, st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo

### Bridge-Hypothesis Dependence
- Severity: medium (0.6562)
- Diagnosis: Progress currently depends on conjectural bridges/hypotheses to connect otherwise weakly linked conceptual regions.
- Evidence IDs: st.def.item, st.def.item-2, st.def.item-4, st.def.item-3, st.def.exponential-time-classes, st.def.polynomial-time-many-one-karp-reduction

### Plural, Underdetermined Strategy Space
- Severity: moderate (0.375)
- Diagnosis: Top entry points span multiple conceptual phases, indicating no single dominant route and high epistemic underdetermination.
- Evidence IDs: st.def.item-2, st.def.item-3, st.def.item, st.def.polynomially-bounded-proof-system, st.def.np-completeness, st.def.polynomial-time-many-one-karp-reduction, st.def.exponential-time-classes, st.thm.cook-reckhow-proof-systems-and-cookreckhow1979

### Barrier Stack Constraints
- Severity: moderate (0.1071)
- Diagnosis: Multiple barrier theorems constrain broad proof templates and force barrier-aware method design.
- Evidence IDs: st.thm.baker-gill-solovay-relativisation-barrier-bakerg, st.thm.razborov-rudich-natural-proofs-barrier-razborovr, st.thm.aaronson-wigderson-algebrisation-barrier-aaronso

## Anti-Barrier Programs

### anti-barrier.001 - relativization
- Barrier IDs: st.thm.baker-gill-solovay-relativisation-barrier-bakerg
- Minimal conceptual changes:
  - Introduce intermediate invariant that is not preserved by the barrier regime.
  - Search for representation-shift that maps target to a non-barrier proof model.
  - Use analogy-transfer from a neighboring regime with stronger lower-bound behavior.
- Research program:
  - Generate barrier-escape-principle hypotheses tied to top unresolved targets.
  - Run deduction checks on re-encoded target statements in scratch KB branches.
  - Retain only changes with non-negative coherence delta and positive entailment gain.

### anti-barrier.002 - natural-proofs
- Barrier IDs: st.thm.razborov-rudich-natural-proofs-barrier-razborovr
- Minimal conceptual changes:
  - Introduce intermediate invariant that is not preserved by the barrier regime.
  - Search for representation-shift that maps target to a non-barrier proof model.
  - Use analogy-transfer from a neighboring regime with stronger lower-bound behavior.
- Research program:
  - Generate barrier-escape-principle hypotheses tied to top unresolved targets.
  - Run deduction checks on re-encoded target statements in scratch KB branches.
  - Retain only changes with non-negative coherence delta and positive entailment gain.

### anti-barrier.003 - algebrization
- Barrier IDs: st.thm.aaronson-wigderson-algebrisation-barrier-aaronso
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
