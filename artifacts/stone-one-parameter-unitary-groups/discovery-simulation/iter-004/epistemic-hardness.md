# Epistemic Hardness: stone-one-parameter-unitary-groups

## Summary

stone-one-parameter-unitary-groups is hard in this KB because global targets are framed across multiple incompatible proof regimes, barrier theorems restrict generic techniques, and explicit dependencies are sparse, forcing hypothesis-driven bridge construction.

## KB Stats

- Statements: 10
- Dependency edges: 13
- Missing dependency refs: 0
- Top entry points considered: 10
- Concept phases in top entry points: 3
- Conceptual hypotheses: 18
- Barrier families: 3

## Concept Communication Trace

- Phase pressure (top entrypoints): Current Bridge Agenda=6, Foundational Gauge-Theoretic Definitions=1, Additional KB-Specific Phases=1

### Entrypoint Concept Anchors
- `st.thm.stone-correspondence` [theorem] phase=Current Bridge Agenda score=0.8321
  - concept: Stone's theorem identifies strongly continuous one-parameter unitary groups with unique self-adjoint generators.
- `st.thm.unitary-group-implies-self-adjoint-generator` [theorem] phase=Current Bridge Agenda score=0.7573
  - concept: Strongly continuous unitary dynamics determines a unique [hidden bridge concept].
- `st.thm.self-adjoint-implies-unitary-group` [theorem] phase=Current Bridge Agenda score=0.7315
  - concept: Every self-adjoint operator exponentiates to a strongly continuous unitary time-evolution family.
- `st.thm.spectral-theorem-functional-calculus` [theorem] phase=Current Bridge Agenda score=0.6633
  - concept: The spectral theorem and functional calculus let one exponentiate a self-adjoint operator into a unitary one-parameter family.
- `st.def.self-adjoint-operator` [definition] phase=Current Bridge Agenda score=0.658
  - concept: Self-adjoint operators are the operator-theoretic objects that support real spectral calculus and unitary evolution.
- `st.def.unitary-group` [definition] phase=Foundational Gauge-Theoretic Definitions score=0.6012
  - concept: A one-parameter unitary group is a strongly continuous unitary time-evolution family.

### Intervention Concept Anchors
- `st.thm.stone-correspondence` [theorem] score=0.6842 partner=None
  - rationale: supports 2 downstream statements; high bridge centrality; concept focus: unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group,...
  - concepts: unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus
- `st.thm.unitary-group-implies-self-adjoint-generator` [theorem] score=0.6625 partner=None
  - rationale: supports 3 downstream statements; high bridge centrality; concept focus: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differen...
  - concepts: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group
- `st.thm.self-adjoint-implies-unitary-group` [theorem] score=0.6315 partner=None
  - rationale: supports 3 downstream statements; high bridge centrality; concept focus: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly...
  - concepts: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, unitary-group-via-functional-calculus
- `st.thm.spectral-theorem-functional-calculus` [theorem] score=0.5357 partner=None
  - rationale: supports 4 downstream statements; concept focus: resolvent-approximants-converge-to-generated-semigroup, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-ope...
  - concepts: resolvent-approximants-converge-to-generated-semigroup, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, resolvent-family-at-large-lambda
- `st.def.self-adjoint-operator` [definition] score=0.498 partner=None
  - rationale: supports 5 downstream statements; concept focus: self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, stone-self-adjoint-correspondence; barrier-interface re...
  - concepts: self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, stone-self-adjoint-correspondence, symmetric-generator
- `st.prop.generator-domain-regularity` [proposition] score=0.4928 partner=None
  - rationale: supports 4 downstream statements; concept focus: c0-generation-implies-closed-dense-generator, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup; barrier-interface re...
  - concepts: c0-generation-implies-closed-dense-generator, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup, closed-densely-defined-generator

### Pathway Concept Anchors
- `path.001` phase=Current Bridge Agenda score=0.6499 entry=st.thm.stone-correspondence
  - goal: Develop a proof pathway centered on st.thm.stone-correspondence.
- `path.002` phase=Current Bridge Agenda score=0.6144 entry=st.thm.unitary-group-implies-self-adjoint-generator
  - goal: Develop a proof pathway centered on st.thm.unitary-group-implies-self-adjoint-generator.
- `path.003` phase=Current Bridge Agenda score=0.6005 entry=st.thm.self-adjoint-implies-unitary-group
  - goal: Develop a proof pathway centered on st.thm.self-adjoint-implies-unitary-group.
- `path.005` phase=Current Bridge Agenda score=0.5532 entry=st.def.self-adjoint-operator
  - goal: Develop a proof pathway centered on st.def.self-adjoint-operator.
- `path.004` phase=Current Bridge Agenda score=0.5461 entry=st.thm.spectral-theorem-functional-calculus
  - goal: Develop a proof pathway centered on st.thm.spectral-theorem-functional-calculus.

### Barrier Connection Fronts
- barrier `st.thm.self-adjoint-implies-unitary-group` <-> entry `st.def.self-adjoint-operator` (score=0.3911, type=bridge)
- barrier `st.thm.self-adjoint-implies-unitary-group` <-> entry `st.def.unitary-group` (score=0.3835, type=bridge)
- barrier `st.thm.unitary-group-implies-self-adjoint-generator` <-> entry `st.def.self-adjoint-operator` (score=0.3811, type=bridge)
- barrier `st.thm.unitary-group-implies-self-adjoint-generator` <-> entry `st.thm.stone-correspondence` (score=0.3773, type=bridge)
- barrier `st.thm.unitary-group-implies-self-adjoint-generator` <-> entry `st.def.unitary-group` (score=0.3768, type=bridge)
- barrier `st.thm.stone-correspondence` <-> entry `st.def.unitary-group` (score=0.3691, type=bridge)

## Essential Elements

| element | severity | score | key evidence |
|---|---|---|---|
| Barrier Stack Constraints | high | 1.0 | barrier_theorems=4, total_theorems=4 |
| Bridge-Hypothesis Dependence | high | 1.0 | connection_candidates=40, proof_hypotheses=58, pathway_count=8 |
| Plural, Underdetermined Strategy Space | moderate | 0.375 | distinct_top_entrypoint_phases=['Additional KB-Specific Phases', 'Current Bridge Agenda', 'Foundational Gauge-Theoretic Definitions'], top_entrypoints_used=10 |
| Sparse Explicit Dependency Structure | moderate | 0.0 | statement_count=10, dependency_edges=13, missing_dependency_refs=0 |
| Asymmetric Lower-Bound Evidence | moderate | 0.0 | restricted_lower_bounds=0, grand_target_related_theorems=0 |

### Barrier Stack Constraints
- Severity: high (1.0)
- Diagnosis: Multiple barrier theorems constrain broad proof templates and force barrier-aware method design.
- Evidence IDs: st.thm.spectral-theorem-functional-calculus, st.thm.unitary-group-implies-self-adjoint-generator, st.thm.self-adjoint-implies-unitary-group, st.thm.stone-correspondence

### Bridge-Hypothesis Dependence
- Severity: high (1.0)
- Diagnosis: Progress currently depends on conjectural bridges/hypotheses to connect otherwise weakly linked conceptual regions.
- Evidence IDs: st.thm.stone-correspondence, st.thm.unitary-group-implies-self-adjoint-generator, st.thm.self-adjoint-implies-unitary-group, st.thm.spectral-theorem-functional-calculus, st.def.self-adjoint-operator, st.prop.generator-domain-regularity

### Plural, Underdetermined Strategy Space
- Severity: moderate (0.375)
- Diagnosis: Top entry points span multiple conceptual phases, indicating no single dominant route and high epistemic underdetermination.
- Evidence IDs: st.thm.stone-correspondence, st.thm.unitary-group-implies-self-adjoint-generator, st.thm.self-adjoint-implies-unitary-group, st.thm.spectral-theorem-functional-calculus, st.def.self-adjoint-operator, st.def.unitary-group, st.prop.generator-domain-regularity, st.prop.generator-symmetry

### Sparse Explicit Dependency Structure
- Severity: moderate (0.0)
- Diagnosis: Most canonical statements are not yet wired by formal depends_on links, so proof navigation is underdetermined.

### Asymmetric Lower-Bound Evidence
- Severity: moderate (0.0)
- Diagnosis: The KB has strong restricted-model lower bounds but relatively fewer direct bridges to full separation targets.

## Anti-Barrier Programs

### anti-barrier.001 - spectral-calculus-interface
- Barrier IDs: st.thm.spectral-theorem-functional-calculus, st.thm.self-adjoint-implies-unitary-group
- Minimal conceptual changes:
  - Introduce intermediate invariant that is not preserved by the barrier regime.
  - Search for representation-shift that maps target to a non-barrier proof model.
  - Use analogy-transfer from a neighboring regime with stronger lower-bound behavior.
- Research program:
  - Generate barrier-escape-principle hypotheses tied to top unresolved targets.
  - Run deduction checks on re-encoded target statements in scratch KB branches.
  - Retain only changes with non-negative coherence delta and positive entailment gain.

### anti-barrier.002 - orbit-differentiability-control
- Barrier IDs: st.thm.unitary-group-implies-self-adjoint-generator
- Minimal conceptual changes:
  - Introduce intermediate invariant that is not preserved by the barrier regime.
  - Search for representation-shift that maps target to a non-barrier proof model.
  - Use analogy-transfer from a neighboring regime with stronger lower-bound behavior.
- Research program:
  - Generate barrier-escape-principle hypotheses tied to top unresolved targets.
  - Run deduction checks on re-encoded target statements in scratch KB branches.
  - Retain only changes with non-negative coherence delta and positive entailment gain.

### anti-barrier.003 - untyped-barrier
- Barrier IDs: st.thm.stone-correspondence
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
