# KB Connection Analysis: `artifacts/hille-yosida-theorem/kb.revised.md`

## Stats

- Ontology profile: generic-mathematics
- Included statuses: accepted, tentative
- Statements: 19
- Filtered out statements: 0
- Dependency edges: 28
- Components: 1
- Candidate generation mode: intra-component-fallback
- Cross-component candidates (pre-trim): 0
- Intra-component candidates (pre-trim): 87
- Missing dependencies: 0
- Avg semantic connection score: 0.3582
- Avg concept alignment: 0.2273
- Avg specificity alignment: 0.4521
- Concept profile coverage: 0.7368
- Specific profile coverage: 0.7368
- Concept graph nodes: 59

## Top Intervention Points

| statement_id | kind | score | unresolved | downstream | theory_relevance | specificity | concept_focus | partner |
|---|---|---|---|---|---|---|---|---|
| st.thm.hille-yosida-general | theorem | 0.6994 | 0 | 8 | 1.0 | 1.0 | equivalence-schema, local-hypothesis-bundle, equivalence, group-theoretic-structure | - |
| st.thm.hille-yosida-contraction | theorem | 0.4938 | 0 | 4 | 0.9428 | 0.8846 | equivalence-schema, unconditional, equivalence, group-theoretic-structure | - |
| st.def.c0-semigroup | definition | 0.4774 | 0 | 17 | 0.3166 | 0.2308 | group-theoretic-structure, operator-theoretic-model, laplace-transform | - |
| st.thm.lumer-phillips | theorem | 0.4701 | 0 | 1 | 1.0 | 1.0 | equivalence-schema, unconditional, equivalence, group-theoretic-structure | - |
| st.def.generator | definition | 0.4216 | 0 | 16 | 0.2869 | 0.1154 | group-theoretic-structure, laplace-transform | - |
| st.thm.cauchy-problem-equivalence | theorem | 0.3873 | 0 | 2 | 0.659 | 0.7436 | unconditional, equivalence, group-theoretic-structure, operator-theoretic-model | - |
| st.ex.translation-semigroup | example | 0.2582 | 0 | 0 | 0.5932 | 0.5256 | equivalence-schema, equivalence, group-theoretic-structure, laplace-transform | - |
| st.prop.generator-closed-dense | proposition | 0.2481 | 0 | 10 | 0.2676 | 0.1154 | group-theoretic-structure, laplace-transform, barrier, domain-regularity | - |
| st.def.resolvent | definition | 0.2427 | 0 | 9 | 0.2869 | 0.1154 | operator-theoretic-model, resolvent-estimate | - |
| st.der.yosida-approximation | derived-construction | 0.2263 | 0 | 0 | 0.3369 | 0.3846 | equivalence, group-theoretic-structure, operator-theoretic-model, resolvent-estimate | - |
| st.ex.multiplication-semigroup | example | 0.1764 | 0 | 0 | 0.2698 | 0.2308 | group-theoretic-structure, operator-theoretic-model, resolvent-estimate | - |
| st.ex.heat-semigroup-lp | example | 0.1464 | 0 | 0 | 0.2676 | 0.1154 | group-theoretic-structure, laplace-transform, resolvent-estimate, barrier | - |
| st.der.contraction-resolvent-monotonicity | corollary | 0.1435 | 0 | 0 | 0.4733 | 0.2949 | unconditional, group-theoretic-structure | - |
| st.der.generator-uniqueness | corollary | 0.133 | 0 | 0 | 0.4733 | 0.2949 | unconditional, group-theoretic-structure | - |
| st.rev.split.st.prop.generator-closed-dense | definition | 0.0309 | 0 | 0 | 0.2572 | 0.0 |  | - |
| st.rev.split.st.thm.cauchy-problem-equivalence | definition | 0.0309 | 0 | 0 | 0.2572 | 0.0 |  | - |
| st.rev.split.st.thm.hille-yosida-contraction | definition | 0.0309 | 0 | 0 | 0.2572 | 0.0 |  | - |
| st.rev.split.st.thm.hille-yosida-general | definition | 0.0309 | 0 | 0 | 0.2572 | 0.0 |  | - |
| st.rev.split.st.thm.lumer-phillips | definition | 0.0309 | 0 | 0 | 0.2572 | 0.0 |  | - |

## Mathematical Concept Profiles (Interventions)

### st.thm.hille-yosida-general
- Concept focus: equivalence-schema, local-hypothesis-bundle, equivalence, group-theoretic-structure, operator-theoretic-model
- Claim signatures: equivalence
- Antecedent signatures: local-hypothesis-bundle
- Consequence signatures: equivalence
- Model signatures: group-theoretic-structure, operator-theoretic-model
- Reduction signatures: 
- Implication signatures: equivalence-schema
- Complexity classes: 
- Core problems: 
- Proof regimes: laplace-transform, resolvent-estimate
- Barrier signals: barrier, powers-of-resolvent-verification

### st.thm.hille-yosida-contraction
- Concept focus: equivalence-schema, unconditional, equivalence, group-theoretic-structure, resolvent-estimate
- Claim signatures: equivalence
- Antecedent signatures: unconditional
- Consequence signatures: equivalence
- Model signatures: group-theoretic-structure
- Reduction signatures: 
- Implication signatures: equivalence-schema
- Complexity classes: 
- Core problems: 
- Proof regimes: resolvent-estimate
- Barrier signals: 

### st.def.c0-semigroup
- Concept focus: group-theoretic-structure, operator-theoretic-model, laplace-transform
- Claim signatures: 
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: group-theoretic-structure, operator-theoretic-model
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: 
- Proof regimes: laplace-transform
- Barrier signals: 

### st.thm.lumer-phillips
- Concept focus: equivalence-schema, unconditional, equivalence, group-theoretic-structure, operator-theoretic-model
- Claim signatures: equivalence
- Antecedent signatures: unconditional
- Consequence signatures: equivalence
- Model signatures: group-theoretic-structure, operator-theoretic-model
- Reduction signatures: 
- Implication signatures: equivalence-schema
- Complexity classes: 
- Core problems: 
- Proof regimes: dissipativity
- Barrier signals: barrier, domain-closure-density

### st.def.generator
- Concept focus: group-theoretic-structure, laplace-transform
- Claim signatures: 
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: group-theoretic-structure
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: 
- Proof regimes: laplace-transform
- Barrier signals: 

### st.thm.cauchy-problem-equivalence
- Concept focus: unconditional, equivalence, group-theoretic-structure, operator-theoretic-model, laplace-transform
- Claim signatures: equivalence
- Antecedent signatures: unconditional
- Consequence signatures: equivalence
- Model signatures: group-theoretic-structure, operator-theoretic-model
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: 
- Proof regimes: laplace-transform
- Barrier signals: 

### st.ex.translation-semigroup
- Concept focus: equivalence-schema, equivalence, group-theoretic-structure, laplace-transform
- Claim signatures: equivalence
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: group-theoretic-structure
- Reduction signatures: 
- Implication signatures: equivalence-schema
- Complexity classes: 
- Core problems: 
- Proof regimes: laplace-transform
- Barrier signals: 

### st.prop.generator-closed-dense
- Concept focus: group-theoretic-structure, laplace-transform, barrier, domain-regularity
- Claim signatures: 
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: group-theoretic-structure
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: 
- Proof regimes: laplace-transform
- Barrier signals: barrier, domain-regularity

### st.def.resolvent
- Concept focus: operator-theoretic-model, resolvent-estimate
- Claim signatures: 
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: operator-theoretic-model
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: 
- Proof regimes: resolvent-estimate
- Barrier signals: 

### st.der.yosida-approximation
- Concept focus: equivalence, group-theoretic-structure, operator-theoretic-model, resolvent-estimate, barrier
- Claim signatures: equivalence
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: group-theoretic-structure, operator-theoretic-model
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: 
- Proof regimes: resolvent-estimate
- Barrier signals: barrier, powers-of-resolvent-verification

### st.ex.multiplication-semigroup
- Concept focus: group-theoretic-structure, operator-theoretic-model, resolvent-estimate
- Claim signatures: 
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: group-theoretic-structure, operator-theoretic-model
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: 
- Proof regimes: resolvent-estimate
- Barrier signals: 

### st.ex.heat-semigroup-lp
- Concept focus: group-theoretic-structure, laplace-transform, resolvent-estimate, barrier, domain-closure-density
- Claim signatures: 
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: group-theoretic-structure
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: 
- Proof regimes: laplace-transform, resolvent-estimate
- Barrier signals: barrier, domain-closure-density

## Top Connection Candidates

| from_id | to_id | score | structural_similarity | semantic | concept_alignment | specific_alignment | relation | concept_evidence |
|---|---|---|---|---|---|---|---|---|
| st.def.c0-semigroup | st.thm.cauchy-problem-equivalence | 0.4504 | 0.5129 | 0.4754 | 0.246 | 0.5 | definitional-expansion | group-theoretic-structure, operator-theoretic-model |
| st.def.generator | st.thm.cauchy-problem-equivalence | 0.4125 | 0.4511 | 0.3962 | 0.164 | 0.25 | definitional-expansion | group-theoretic-structure |
| st.def.c0-semigroup | st.thm.hille-yosida-general | 0.3988 | 0.3662 | 0.3582 | 0.2033 | 0.4 | definitional-expansion | group-theoretic-structure, operator-theoretic-model |
| st.def.generator | st.thm.hille-yosida-general | 0.3814 | 0.3514 | 0.3235 | 0.1222 | 0.2 | definitional-expansion | group-theoretic-structure |
| st.def.c0-semigroup | st.def.generator | 0.357 | 0.6075 | 0.5506 | 0.1667 | 0.5 | definitional-expansion | group-theoretic-structure |
| st.def.c0-semigroup | st.thm.lumer-phillips | 0.3548 | 0.2334 | 0.2615 | 0.1622 | 0.4 | definitional-expansion | group-theoretic-structure, operator-theoretic-model |
| st.def.generator | st.prop.generator-closed-dense | 0.3473 | 0.609 | 0.5988 | 0.245 | 1.0 | definitional-expansion | group-theoretic-structure |
| st.thm.hille-yosida-general | st.thm.hille-yosida-contraction | 0.3461 | 0.5493 | 0.5036 | 0.564 | 0.5 | implication-schema-transfer | group-theoretic-structure, equivalence-schema, equivalence |
| st.def.resolvent | st.thm.hille-yosida-contraction | 0.3454 | 0.4192 | 0.3426 | 0.0817 | 0.0 | definitional-expansion | resolvent-estimate |
| st.def.resolvent | st.thm.hille-yosida-general | 0.3258 | 0.3345 | 0.309 | 0.1222 | 0.2 | definitional-expansion | operator-theoretic-model |
| st.def.generator | st.thm.hille-yosida-contraction | 0.3242 | 0.1833 | 0.2059 | 0.1617 | 0.25 | definitional-expansion | group-theoretic-structure |
| st.def.c0-semigroup | st.thm.hille-yosida-contraction | 0.322 | 0.166 | 0.1817 | 0.0814 | 0.2 | definitional-expansion | group-theoretic-structure |
| st.def.generator | st.thm.lumer-phillips | 0.3189 | 0.1742 | 0.1889 | 0.0811 | 0.2 | definitional-expansion | group-theoretic-structure |
| st.def.generator | st.ex.translation-semigroup | 0.311 | 0.5203 | 0.4678 | 0.245 | 0.3333 | definitional-expansion | group-theoretic-structure |
| st.thm.cauchy-problem-equivalence | st.thm.lumer-phillips | 0.308 | 0.3711 | 0.4209 | 0.5444 | 0.8 | potential-equivalence | group-theoretic-structure, operator-theoretic-model, unconditional, equivalence |
| st.def.c0-semigroup | st.ex.translation-semigroup | 0.3046 | 0.4962 | 0.4337 | 0.164 | 0.25 | definitional-expansion | group-theoretic-structure |
| st.def.c0-semigroup | st.prop.generator-closed-dense | 0.3031 | 0.477 | 0.4392 | 0.164 | 0.5 | definitional-expansion | group-theoretic-structure |
| st.def.generator | st.ex.heat-semigroup-lp | 0.3029 | 0.4419 | 0.4735 | 0.204 | 1.0 | definitional-expansion | group-theoretic-structure |
| st.thm.hille-yosida-general | st.thm.cauchy-problem-equivalence | 0.3029 | 0.4154 | 0.3916 | 0.484 | 0.5 | model-transfer | group-theoretic-structure, operator-theoretic-model, equivalence |
| st.def.c0-semigroup | st.ex.multiplication-semigroup | 0.2941 | 0.3747 | 0.4322 | 0.165 | 1.0 | definitional-expansion | group-theoretic-structure, operator-theoretic-model |

## Abductive Loop Plan

### Round 1
- Objective: Prioritize intervention targets by graph influence and unresolved dependencies.
- Targets: st.thm.hille-yosida-general, st.thm.hille-yosida-contraction, st.def.c0-semigroup, st.thm.lumer-phillips, st.def.generator, st.thm.cauchy-problem-equivalence
- Action: Run kb-abduce on each target to propose missing-premise hypotheses.

### Round 2
- Objective: Test high-value intra-component transfer links (fallback mode) as abductive support hypotheses.
- Candidate connections: st.def.c0-semigroup->st.thm.cauchy-problem-equivalence (0.4504), st.def.generator->st.thm.cauchy-problem-equivalence (0.4125), st.def.c0-semigroup->st.thm.hille-yosida-general (0.3988), st.def.generator->st.thm.hille-yosida-general (0.3814), st.def.c0-semigroup->st.def.generator (0.357), st.def.c0-semigroup->st.thm.lumer-phillips (0.3548)
- Action: Convert top links into conjectural dependencies and run kb-deduce for consequence checks.

### Round 3
- Objective: Refine and retain only hypotheses with best explanatory and deductive payoff.
- Action: Re-score interventions, drop contradicted links, and keep top surviving pathways.
