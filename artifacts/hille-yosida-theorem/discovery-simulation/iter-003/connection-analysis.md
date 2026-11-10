# KB Connection Analysis: `/Users/user/files/abducer/abducer/artifacts/hille-yosida-theorem/discovery-simulation/working-kb/hille-yosida-theorem.kb.md`

## Stats

- Ontology profile: functional-analysis-semigroup
- Included statuses: accepted, tentative
- Statements: 14
- Filtered out statements: 0
- Dependency edges: 7
- Components: 9
- Candidate generation mode: hybrid
- Cross-component candidates (pre-trim): 80
- Intra-component candidates (pre-trim): 9
- Missing dependencies: 0
- Avg semantic connection score: 0.2785
- Avg concept alignment: 0.1797
- Avg specificity alignment: 0.19
- Concept profile coverage: 1.0
- Specific profile coverage: 1.0
- Concept graph nodes: 111

## Top Intervention Points

| statement_id | kind | score | unresolved | downstream | theory_relevance | specificity | concept_focus | partner |
|---|---|---|---|---|---|---|---|---|
| st.thm.hille-yosida-general | theorem | 0.6385 | 0 | 1 | 1.0 | 1.0 | c0-generation-implies-closed-dense-generator, resolvent-approximants-converge-to-generated-semigroup, closed-dense-plus-resolvent-powers-imply-c0-generation, closed-dense-operator-with-resolvent-power-bounds | st.def.generator |
| st.thm.hille-yosida-contraction | theorem | 0.5783 | 0 | 0 | 1.0 | 1.0 | c0-generation-implies-closed-dense-generator, closed-dense-plus-first-resolvent-bound-imply-contraction-generation, resolvent-approximants-converge-to-generated-semigroup, closed-dense-operator-with-first-resolvent-bound | st.thm.hille-yosida-general |
| st.def.generator | definition | 0.5354 | 0 | 2 | 0.4884 | 0.4667 | c0-semigroup-definition, generator-definition, C0-semigroup-model, operator-theoretic-Banach-space | st.thm.hille-yosida-general |
| st.def.c0-semigroup | definition | 0.511 | 0 | 3 | 0.4326 | 0.3333 | c0-semigroup-definition, C0-semigroup-model, operator-theoretic-Banach-space, Banach-space | st.ex.heat-semigroup-lp |
| st.thm.cauchy-problem-equivalence | theorem | 0.4798 | 0 | 1 | 0.9671 | 0.8667 | c0-generation-iff-cauchy-well-posedness, closed-operator-or-semigroup-generator, well-posed-abstract-cauchy-problem, cauchy-problem-equivalence | st.def.generator |
| st.der.yosida-approximation | derived-construction | 0.4696 | 0 | 0 | 0.7865 | 1.0 | resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, contraction-semigroup-generator, bounded-generator-approximation-scheme | st.ex.multiplication-semigroup |
| st.thm.lumer-phillips | theorem | 0.4692 | 0 | 0 | 1.0 | 1.0 | closed-dense-plus-first-resolvent-bound-imply-contraction-generation, dissipativity-plus-range-condition-imply-contraction-generation, densely-defined-dissipative-operator-with-surjective-shift, closed-dense-operator-with-first-resolvent-bound | st.def.generator |
| st.prop.generator-closed-dense | proposition | 0.424 | 0 | 0 | 0.7537 | 0.8667 | c0-generation-implies-closed-dense-generator, generator-of-c0-semigroup, closed-densely-defined-generator, generator-closed-dense | st.def.generator |
| st.def.resolvent | definition | 0.3873 | 0 | 0 | 0.774 | 1.0 | resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme, yosida-approximation-convergence | st.ex.multiplication-semigroup |
| st.ex.translation-semigroup | example | 0.3504 | 0 | 0 | 0.4495 | 0.4667 | c0-semigroup-definition, generator-definition, C0-semigroup-model, unbounded-generator-graph | st.thm.hille-yosida-general |
| st.der.generator-uniqueness | corollary | 0.318 | 0 | 0 | 0.5973 | 0.6444 | shared-semigroup-orbit-data, unique-generator-for-semigroup, generator-uniqueness, C0-semigroup-model | st.ex.translation-semigroup |
| st.ex.multiplication-semigroup | example | 0.301 | 0 | 0 | 0.3838 | 0.2 | C0-semigroup-model, resolvent-generation-criterion, unbounded-generator-graph, C0-semigroup | st.ex.heat-semigroup-lp |
| st.der.contraction-resolvent-monotonicity | corollary | 0.2817 | 0 | 0 | 0.6258 | 0.6444 | contraction-semigroup-generator, resolvent-monotonicity, contraction-resolvent-monotonicity, contraction-generation-regime | st.ex.multiplication-semigroup |
| st.ex.heat-semigroup-lp | example | 0.2793 | 0 | 0 | 0.3838 | 0.2 | C0-semigroup-model, abstract-cauchy-evolution, resolvent-generation-criterion, Banach-space | st.ex.multiplication-semigroup |

## Mathematical Concept Profiles (Interventions)

### st.thm.hille-yosida-general
- Concept focus: c0-generation-implies-closed-dense-generator, resolvent-approximants-converge-to-generated-semigroup, closed-dense-plus-resolvent-powers-imply-c0-generation, closed-dense-operator-with-resolvent-power-bounds, resolvent-family-at-large-lambda
- Claim signatures: semigroup-generation-characterization, yosida-approximation-convergence, generator-closed-dense
- Antecedent signatures: closed-dense-operator-with-resolvent-power-bounds, resolvent-family-at-large-lambda, generator-of-c0-semigroup
- Consequence signatures: generator-of-exponentially-bounded-c0-semigroup, bounded-generator-approximation-scheme, closed-densely-defined-generator
- Model signatures: C0-semigroup-model, Yosida-approximation-scheme, operator-theoretic-Banach-space, resolvent-generation-criterion, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: c0-generation-implies-closed-dense-generator, resolvent-approximants-converge-to-generated-semigroup, closed-dense-plus-resolvent-powers-imply-c0-generation
- Complexity classes: 
- Core problems: Banach-space, C0-semigroup, Yosida-approximation, generator, resolvent, unbounded-operator
- Proof regimes: domain-regularity, generator-analysis, laplace-transform, resolvent-estimate, semigroup-generation, yosida-approximation
- Barrier signals: barrier, domain-closure-density, powers-of-resolvent-verification, unbounded-operator-domain-control

### st.thm.hille-yosida-contraction
- Concept focus: c0-generation-implies-closed-dense-generator, closed-dense-plus-first-resolvent-bound-imply-contraction-generation, resolvent-approximants-converge-to-generated-semigroup, closed-dense-operator-with-first-resolvent-bound, resolvent-family-at-large-lambda
- Claim signatures: contraction-generation-characterization, contraction-resolvent-monotonicity, yosida-approximation-convergence, c0-semigroup-definition, generator-closed-dense, resolvent-definition
- Antecedent signatures: closed-dense-operator-with-first-resolvent-bound, resolvent-family-at-large-lambda, contraction-semigroup-generator, generator-of-c0-semigroup
- Consequence signatures: bounded-generator-approximation-scheme, generator-of-contraction-c0-semigroup, closed-densely-defined-generator, resolvent-monotonicity
- Model signatures: C0-semigroup-model, Yosida-approximation-scheme, contraction-generation-regime, resolvent-generation-criterion
- Reduction signatures: 
- Implication signatures: c0-generation-implies-closed-dense-generator, closed-dense-plus-first-resolvent-bound-imply-contraction-generation, resolvent-approximants-converge-to-generated-semigroup
- Complexity classes: 
- Core problems: C0-semigroup, Yosida-approximation, contraction-semigroup, generator, resolvent
- Proof regimes: contraction-theory, domain-regularity, resolvent-estimate, semigroup-generation, yosida-approximation
- Barrier signals: domain-closure-density, unbounded-operator-domain-control

### st.def.generator
- Concept focus: c0-semigroup-definition, generator-definition, C0-semigroup-model, operator-theoretic-Banach-space, unbounded-generator-graph
- Claim signatures: c0-semigroup-definition, generator-definition
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: C0-semigroup-model, operator-theoretic-Banach-space, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: C0-semigroup, generator
- Proof regimes: domain-regularity, generator-analysis, laplace-transform, semigroup-generation
- Barrier signals: approximation-limit-control, domain-closure-density, unbounded-operator-domain-control

### st.def.c0-semigroup
- Concept focus: c0-semigroup-definition, C0-semigroup-model, operator-theoretic-Banach-space, Banach-space, C0-semigroup
- Claim signatures: c0-semigroup-definition
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: C0-semigroup-model, operator-theoretic-Banach-space
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: Banach-space, C0-semigroup, generator, unbounded-operator
- Proof regimes: laplace-transform, semigroup-generation
- Barrier signals: 

### st.thm.cauchy-problem-equivalence
- Concept focus: c0-generation-iff-cauchy-well-posedness, closed-operator-or-semigroup-generator, well-posed-abstract-cauchy-problem, cauchy-problem-equivalence, C0-semigroup-model
- Claim signatures: cauchy-problem-equivalence
- Antecedent signatures: closed-operator-or-semigroup-generator
- Consequence signatures: well-posed-abstract-cauchy-problem
- Model signatures: C0-semigroup-model, abstract-cauchy-evolution, operator-theoretic-Banach-space
- Reduction signatures: 
- Implication signatures: c0-generation-iff-cauchy-well-posedness
- Complexity classes: 
- Core problems: Banach-space, C0-semigroup, abstract-Cauchy-problem, generator
- Proof regimes: abstract-cauchy-problem, domain-regularity, laplace-transform, semigroup-generation
- Barrier signals: unbounded-operator-domain-control

### st.der.yosida-approximation
- Concept focus: resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, contraction-semigroup-generator, bounded-generator-approximation-scheme, resolvent-monotonicity
- Claim signatures: contraction-resolvent-monotonicity, yosida-approximation-convergence, resolvent-definition
- Antecedent signatures: resolvent-family-at-large-lambda, contraction-semigroup-generator
- Consequence signatures: bounded-generator-approximation-scheme, resolvent-monotonicity
- Model signatures: Yosida-approximation-scheme, operator-theoretic-Banach-space, resolvent-generation-criterion, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: resolvent-approximants-converge-to-generated-semigroup
- Complexity classes: 
- Core problems: C0-semigroup, Yosida-approximation, generator, resolvent, unbounded-operator
- Proof regimes: generator-analysis, resolvent-estimate, semigroup-generation, yosida-approximation
- Barrier signals: barrier, powers-of-resolvent-verification, unbounded-operator-domain-control

### st.thm.lumer-phillips
- Concept focus: closed-dense-plus-first-resolvent-bound-imply-contraction-generation, dissipativity-plus-range-condition-imply-contraction-generation, densely-defined-dissipative-operator-with-surjective-shift, closed-dense-operator-with-first-resolvent-bound, contraction-semigroup-via-dissipativity
- Claim signatures: contraction-generation-characterization, dissipativity-characterization
- Antecedent signatures: densely-defined-dissipative-operator-with-surjective-shift, closed-dense-operator-with-first-resolvent-bound
- Consequence signatures: contraction-semigroup-via-dissipativity, generator-of-contraction-c0-semigroup
- Model signatures: C0-semigroup-model, contraction-generation-regime, dissipative-range-condition, operator-theoretic-Banach-space, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: closed-dense-plus-first-resolvent-bound-imply-contraction-generation, dissipativity-plus-range-condition-imply-contraction-generation
- Complexity classes: 
- Core problems: Banach-space, C0-semigroup, contraction-semigroup, dissipativity, generator, unbounded-operator
- Proof regimes: contraction-theory, dissipativity, domain-regularity, generator-analysis, semigroup-generation
- Barrier signals: barrier, domain-closure-density, unbounded-operator-domain-control

### st.prop.generator-closed-dense
- Concept focus: c0-generation-implies-closed-dense-generator, generator-of-c0-semigroup, closed-densely-defined-generator, generator-closed-dense, C0-semigroup-model
- Claim signatures: generator-closed-dense
- Antecedent signatures: generator-of-c0-semigroup
- Consequence signatures: closed-densely-defined-generator
- Model signatures: C0-semigroup-model, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: c0-generation-implies-closed-dense-generator
- Complexity classes: 
- Core problems: C0-semigroup, generator
- Proof regimes: domain-regularity, generator-analysis, laplace-transform, semigroup-generation
- Barrier signals: barrier, domain-closure-density, domain-regularity, unbounded-operator-domain-control

### st.def.resolvent
- Concept focus: resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme, yosida-approximation-convergence, resolvent-definition
- Claim signatures: yosida-approximation-convergence, resolvent-definition
- Antecedent signatures: resolvent-family-at-large-lambda
- Consequence signatures: bounded-generator-approximation-scheme
- Model signatures: Yosida-approximation-scheme, resolvent-generation-criterion
- Reduction signatures: 
- Implication signatures: resolvent-approximants-converge-to-generated-semigroup
- Complexity classes: 
- Core problems: generator, resolvent, unbounded-operator
- Proof regimes: resolvent-estimate
- Barrier signals: 

### st.ex.translation-semigroup
- Concept focus: c0-semigroup-definition, generator-definition, C0-semigroup-model, unbounded-generator-graph, C0-semigroup
- Claim signatures: c0-semigroup-definition, generator-definition
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: C0-semigroup-model, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: C0-semigroup, generator
- Proof regimes: generator-analysis, laplace-transform, semigroup-generation
- Barrier signals: unbounded-operator-domain-control

### st.der.generator-uniqueness
- Concept focus: shared-semigroup-orbit-data, unique-generator-for-semigroup, generator-uniqueness, C0-semigroup-model, unbounded-generator-graph
- Claim signatures: generator-uniqueness
- Antecedent signatures: shared-semigroup-orbit-data
- Consequence signatures: unique-generator-for-semigroup
- Model signatures: C0-semigroup-model, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: C0-semigroup, generator
- Proof regimes: generator-analysis, semigroup-generation
- Barrier signals: 

### st.ex.multiplication-semigroup
- Concept focus: C0-semigroup-model, resolvent-generation-criterion, unbounded-generator-graph, C0-semigroup, generator
- Claim signatures: 
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: C0-semigroup-model, resolvent-generation-criterion, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: C0-semigroup, generator, resolvent, unbounded-operator
- Proof regimes: generator-analysis, resolvent-estimate, semigroup-generation
- Barrier signals: unbounded-operator-domain-control

## Top Connection Candidates

| from_id | to_id | score | structural_similarity | semantic | concept_alignment | specific_alignment | relation | concept_evidence |
|---|---|---|---|---|---|---|---|---|
| st.def.c0-semigroup | st.thm.cauchy-problem-equivalence | 0.6419 | 0.3565 | 0.337 | 0.1986 | 0.25 | definitional-expansion | operator-theoretic-Banach-space, C0-semigroup-model |
| st.def.generator | st.thm.hille-yosida-general | 0.6153 | 0.4121 | 0.3697 | 0.1951 | 0.1579 | definitional-expansion | unbounded-generator-graph, operator-theoretic-Banach-space, C0-semigroup-model |
| st.def.c0-semigroup | st.thm.hille-yosida-general | 0.6075 | 0.2857 | 0.2678 | 0.1464 | 0.1111 | definitional-expansion | operator-theoretic-Banach-space, C0-semigroup-model |
| st.def.generator | st.thm.cauchy-problem-equivalence | 0.5923 | 0.3595 | 0.3305 | 0.185 | 0.2 | definitional-expansion | operator-theoretic-Banach-space, C0-semigroup-model |
| st.def.c0-semigroup | st.thm.lumer-phillips | 0.5427 | 0.2454 | 0.2416 | 0.1332 | 0.1429 | definitional-expansion | operator-theoretic-Banach-space, C0-semigroup-model |
| st.def.generator | st.thm.lumer-phillips | 0.5312 | 0.333 | 0.3115 | 0.186 | 0.2 | definitional-expansion | unbounded-generator-graph, operator-theoretic-Banach-space, C0-semigroup-model |
| st.def.c0-semigroup | st.thm.hille-yosida-contraction | 0.5195 | 0.2028 | 0.1985 | 0.0995 | 0.0909 | definitional-expansion | c0-semigroup-definition, C0-semigroup-model |
| st.def.generator | st.thm.hille-yosida-contraction | 0.4867 | 0.2366 | 0.2245 | 0.136 | 0.0833 | definitional-expansion | c0-semigroup-definition, C0-semigroup-model |
| st.thm.hille-yosida-general | st.thm.hille-yosida-contraction | 0.4835 | 0.5437 | 0.4778 | 0.4075 | 0.4074 | implication-schema-transfer | c0-generation-implies-closed-dense-generator, resolvent-approximants-converge-to-generated-semigroup, bounded-generator-approximation-scheme, yosida-approximation-convergence |
| st.def.c0-semigroup | st.ex.heat-semigroup-lp | 0.4654 | 0.3951 | 0.3531 | 0.1233 | 0.2 | definitional-expansion | C0-semigroup-model |
| st.def.resolvent | st.thm.hille-yosida-general | 0.4532 | 0.2904 | 0.3061 | 0.2853 | 0.3333 | definitional-expansion | resolvent-approximants-converge-to-generated-semigroup, bounded-generator-approximation-scheme, yosida-approximation-convergence, resolvent-family-at-large-lambda |
| st.def.generator | st.prop.generator-closed-dense | 0.4373 | 0.529 | 0.4673 | 0.2879 | 0.2222 | definitional-expansion | unbounded-generator-graph, C0-semigroup-model |
| st.thm.cauchy-problem-equivalence | st.thm.lumer-phillips | 0.4362 | 0.2979 | 0.2641 | 0.1262 | 0.1111 | potential-equivalence | operator-theoretic-Banach-space, C0-semigroup-model |
| st.thm.hille-yosida-general | st.ex.multiplication-semigroup | 0.4276 | 0.3611 | 0.3053 | 0.2027 | 0.1765 | model-transfer | unbounded-generator-graph, resolvent-generation-criterion, C0-semigroup-model |
| st.thm.hille-yosida-general | st.ex.translation-semigroup | 0.4242 | 0.3661 | 0.2939 | 0.143 | 0.1053 | model-transfer | unbounded-generator-graph, C0-semigroup-model |
| st.def.generator | st.der.generator-uniqueness | 0.4082 | 0.3195 | 0.3059 | 0.2302 | 0.25 | definitional-expansion | unbounded-generator-graph, C0-semigroup-model |
| st.thm.cauchy-problem-equivalence | st.ex.translation-semigroup | 0.4034 | 0.3067 | 0.2502 | 0.155 | 0.1 | method-transfer | C0-semigroup-model |
| st.def.c0-semigroup | st.der.generator-uniqueness | 0.4007 | 0.1981 | 0.1939 | 0.1229 | 0.1429 | definitional-expansion | C0-semigroup-model |
| st.def.c0-semigroup | st.prop.generator-closed-dense | 0.3969 | 0.3067 | 0.2795 | 0.136 | 0.125 | definitional-expansion | C0-semigroup-model |
| st.def.generator | st.ex.heat-semigroup-lp | 0.3965 | 0.2923 | 0.2714 | 0.1138 | 0.1429 | definitional-expansion | C0-semigroup-model |

## Abductive Loop Plan

### Round 1
- Objective: Prioritize intervention targets by graph influence and unresolved dependencies.
- Targets: st.thm.hille-yosida-general, st.thm.hille-yosida-contraction, st.def.generator, st.def.c0-semigroup, st.thm.cauchy-problem-equivalence, st.der.yosida-approximation
- Action: Run kb-abduce on each target to propose missing-premise hypotheses.

### Round 2
- Objective: Test high-value cross-component links as abductive support hypotheses.
- Candidate connections: st.def.c0-semigroup->st.thm.cauchy-problem-equivalence (0.6419), st.def.generator->st.thm.hille-yosida-general (0.6153), st.def.c0-semigroup->st.thm.hille-yosida-general (0.6075), st.def.generator->st.thm.cauchy-problem-equivalence (0.5923), st.def.c0-semigroup->st.thm.lumer-phillips (0.5427), st.def.generator->st.thm.lumer-phillips (0.5312)
- Action: Convert top links into conjectural dependencies and run kb-deduce for consequence checks.

### Round 3
- Objective: Refine and retain only hypotheses with best explanatory and deductive payoff.
- Action: Re-score interventions, drop contradicted links, and keep top surviving pathways.
