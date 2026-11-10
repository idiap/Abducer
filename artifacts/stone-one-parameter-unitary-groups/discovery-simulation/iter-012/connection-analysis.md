# KB Connection Analysis: `/Users/user/files/abducer/abducer/artifacts/stone-one-parameter-unitary-groups/discovery-simulation/working-kb/stone-one-parameter-unitary-groups.kb.md`

## Stats

- Ontology profile: functional-analysis-semigroup
- Included statuses: accepted, tentative
- Statements: 10
- Filtered out statements: 0
- Dependency edges: 13
- Components: 1
- Candidate generation mode: intra-component-fallback
- Cross-component candidates (pre-trim): 0
- Intra-component candidates (pre-trim): 44
- Missing dependencies: 0
- Avg semantic connection score: 0.3374
- Avg concept alignment: 0.3123
- Avg specificity alignment: 0.3007
- Concept profile coverage: 1.0
- Specific profile coverage: 1.0
- Concept graph nodes: 94

## Top Intervention Points

| statement_id | kind | score | unresolved | downstream | theory_relevance | specificity | concept_focus | partner |
|---|---|---|---|---|---|---|---|---|
| st.thm.stone-correspondence | theorem | 0.6842 | 0 | 2 | 1.0 | 1.0 | unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group, spectral-theorem-enables-unitary-functional-calculus | - |
| st.thm.unitary-group-implies-self-adjoint-generator | theorem | 0.6625 | 0 | 3 | 1.0 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero | - |
| st.thm.self-adjoint-implies-unitary-group | theorem | 0.6315 | 0 | 3 | 1.0 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group | - |
| st.thm.spectral-theorem-functional-calculus | theorem | 0.5357 | 0 | 4 | 1.0 | 1.0 | resolvent-approximants-converge-to-generated-semigroup, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space | - |
| st.def.self-adjoint-operator | definition | 0.498 | 0 | 5 | 0.5651 | 0.7778 | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, stone-self-adjoint-correspondence | - |
| st.prop.generator-domain-regularity | proposition | 0.4928 | 0 | 4 | 0.7865 | 1.0 | c0-generation-implies-closed-dense-generator, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup | - |
| st.app.schrodinger-time-evolution | application | 0.4341 | 0 | 0 | 0.7865 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group | - |
| st.def.unitary-group | definition | 0.4309 | 0 | 6 | 0.5094 | 0.6444 | strongly-continuous-unitary-group, unitary-group-definition, operator-theoretic-Hilbert-space, Hilbert-space | - |
| st.prop.generator-symmetry | proposition | 0.4058 | 0 | 4 | 0.5263 | 0.7778 | differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, symmetric-generator, unitary-group-definition | - |
| st.ex.translation-group-on-l2 | example | 0.3036 | 0 | 0 | 0.5034 | 0.7778 | strongly-continuous-unitary-group, stone-self-adjoint-correspondence, stone-unitary-group-correspondence, unitary-group-definition | - |

## Mathematical Concept Profiles (Interventions)

### st.thm.stone-correspondence
- Concept focus: unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus
- Claim signatures: self-adjoint-generator-characterization, spectral-calculus-unitary-realization, stone-unitary-group-correspondence, self-adjoint-operator-definition, unitary-group-definition
- Antecedent signatures: spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group
- Consequence signatures: self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, strongly-continuous-unitary-group, stone-self-adjoint-correspondence, unique-self-adjoint-generator
- Model signatures: self-adjoint-spectral-calculus, spectral-functional-calculus, strongly-continuous-unitary-group, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group, spectral-theorem-enables-unitary-functional-calculus
- Complexity classes: 
- Core problems: Stone-correspondence, functional-calculus, generator, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, unitary-group
- Proof regimes: functional-calculus, generator-analysis, spectral-analysis, stone-correspondence, unitary-group-analysis
- Barrier signals: spectral-calculus-interface

### st.thm.unitary-group-implies-self-adjoint-generator
- Concept focus: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group
- Claim signatures: self-adjoint-generator-characterization, spectral-calculus-unitary-realization, self-adjoint-operator-definition, unitary-group-definition
- Antecedent signatures: spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group
- Consequence signatures: self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, strongly-continuous-unitary-group, unique-self-adjoint-generator
- Model signatures: self-adjoint-spectral-calculus, spectral-functional-calculus, strongly-continuous-unitary-group, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: spectral-theorem-enables-unitary-functional-calculus
- Complexity classes: 
- Core problems: Stone-correspondence, generator, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group
- Proof regimes: domain-regularity, generator-analysis, spectral-analysis, stone-correspondence, unitary-group-analysis
- Barrier signals: barrier, orbit-differentiability-control, unbounded-operator-domain-control

### st.thm.self-adjoint-implies-unitary-group
- Concept focus: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, unitary-group-via-functional-calculus
- Claim signatures: spectral-calculus-unitary-realization, stone-unitary-group-correspondence, self-adjoint-operator-definition, unitary-group-definition
- Antecedent signatures: spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group
- Consequence signatures: self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, strongly-continuous-unitary-group, stone-self-adjoint-correspondence
- Model signatures: self-adjoint-spectral-calculus, spectral-functional-calculus, strongly-continuous-unitary-group
- Reduction signatures: 
- Implication signatures: spectral-theorem-enables-unitary-functional-calculus
- Complexity classes: 
- Core problems: Stone-correspondence, functional-calculus, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, unitary-group
- Proof regimes: functional-calculus, spectral-analysis, stone-correspondence, unitary-group-analysis
- Barrier signals: barrier, spectral-calculus-interface

### st.thm.spectral-theorem-functional-calculus
- Concept focus: resolvent-approximants-converge-to-generated-semigroup, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, resolvent-family-at-large-lambda
- Claim signatures: spectral-calculus-unitary-realization, yosida-approximation-convergence, self-adjoint-operator-definition
- Antecedent signatures: spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, resolvent-family-at-large-lambda
- Consequence signatures: self-adjoint-operator-on-hilbert-space, bounded-generator-approximation-scheme, unitary-group-via-functional-calculus
- Model signatures: Yosida-approximation-scheme, self-adjoint-spectral-calculus, spectral-functional-calculus
- Reduction signatures: 
- Implication signatures: resolvent-approximants-converge-to-generated-semigroup, spectral-theorem-enables-unitary-functional-calculus
- Complexity classes: 
- Core problems: functional-calculus, generator, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator, unitary-group
- Proof regimes: functional-calculus, spectral-analysis, unitary-group-analysis
- Barrier signals: barrier, spectral-calculus-interface

### st.def.self-adjoint-operator
- Concept focus: self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, stone-self-adjoint-correspondence, symmetric-generator
- Claim signatures: stone-unitary-group-correspondence, self-adjoint-operator-definition, generator-symmetry
- Antecedent signatures: self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group
- Consequence signatures: self-adjoint-operator-on-hilbert-space, stone-self-adjoint-correspondence, symmetric-generator
- Model signatures: operator-theoretic-Banach-space, self-adjoint-spectral-calculus
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: Stone-correspondence, generator, self-adjoint-operator, spectral-measure, unbounded-operator, unitary-group
- Proof regimes: domain-regularity, spectral-analysis, stone-correspondence, unitary-group-analysis
- Barrier signals: unbounded-operator-domain-control

### st.prop.generator-domain-regularity
- Concept focus: c0-generation-implies-closed-dense-generator, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup, closed-densely-defined-generator
- Claim signatures: self-adjoint-operator-definition, unitary-group-definition, generator-closed-dense
- Antecedent signatures: self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup
- Consequence signatures: self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, closed-densely-defined-generator
- Model signatures: self-adjoint-spectral-calculus, strongly-continuous-unitary-group, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: c0-generation-implies-closed-dense-generator
- Complexity classes: 
- Core problems: generator, self-adjoint-operator, unitary-group
- Proof regimes: domain-regularity, generator-analysis, unitary-group-analysis
- Barrier signals: barrier, domain-closure-density, orbit-differentiability-control, unbounded-operator-domain-control

### st.app.schrodinger-time-evolution
- Concept focus: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, unitary-group-via-functional-calculus
- Claim signatures: spectral-calculus-unitary-realization, stone-unitary-group-correspondence, self-adjoint-operator-definition, quantum-time-evolution
- Antecedent signatures: spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group
- Consequence signatures: self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, stone-self-adjoint-correspondence, Hamiltonian-time-evolution-model
- Model signatures: self-adjoint-spectral-calculus, spectral-functional-calculus
- Reduction signatures: 
- Implication signatures: spectral-theorem-enables-unitary-functional-calculus
- Complexity classes: 
- Core problems: Hamiltonian, Stone-correspondence, functional-calculus, generator, self-adjoint-operator, spectral-measure, spectral-theorem, unbounded-operator
- Proof regimes: domain-regularity, functional-calculus, spectral-analysis, stone-correspondence, unitary-group-analysis
- Barrier signals: spectral-calculus-interface, unbounded-operator-domain-control

### st.def.unitary-group
- Concept focus: strongly-continuous-unitary-group, unitary-group-definition, operator-theoretic-Hilbert-space, Hilbert-space, Stone-correspondence
- Claim signatures: unitary-group-definition
- Antecedent signatures: strongly-continuous-unitary-group
- Consequence signatures: strongly-continuous-unitary-group
- Model signatures: operator-theoretic-Hilbert-space, strongly-continuous-unitary-group
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: Hilbert-space, Stone-correspondence, generator, unitary-group
- Proof regimes: hilbert-space-analysis, stone-correspondence, unitary-group-analysis
- Barrier signals: 

### st.prop.generator-symmetry
- Concept focus: differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, symmetric-generator, unitary-group-definition, generator-symmetry
- Claim signatures: unitary-group-definition, generator-symmetry
- Antecedent signatures: differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group
- Consequence signatures: strongly-continuous-unitary-group, symmetric-generator
- Model signatures: operator-theoretic-Banach-space, operator-theoretic-Hilbert-space, strongly-continuous-unitary-group, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: Hilbert-space, generator, unbounded-operator, unitary-group
- Proof regimes: generator-analysis, hilbert-space-analysis, unitary-group-analysis
- Barrier signals: barrier, orbit-differentiability-control, unbounded-operator-domain-control

### st.ex.translation-group-on-l2
- Concept focus: strongly-continuous-unitary-group, stone-self-adjoint-correspondence, stone-unitary-group-correspondence, unitary-group-definition, unitary-group-example
- Claim signatures: stone-unitary-group-correspondence, unitary-group-definition, unitary-group-example
- Antecedent signatures: strongly-continuous-unitary-group
- Consequence signatures: strongly-continuous-unitary-group, stone-self-adjoint-correspondence
- Model signatures: strongly-continuous-unitary-group, unbounded-generator-graph
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: Stone-correspondence, generator, unbounded-operator, unitary-group
- Proof regimes: generator-analysis, stone-correspondence, unitary-group-analysis
- Barrier signals: 

## Top Connection Candidates

| from_id | to_id | score | structural_similarity | semantic | concept_alignment | specific_alignment | relation | concept_evidence |
|---|---|---|---|---|---|---|---|---|
| st.def.self-adjoint-operator | st.thm.self-adjoint-implies-unitary-group | 0.3911 | 0.405 | 0.3907 | 0.3045 | 0.375 | definitional-expansion | self-adjoint-operator-on-hilbert-space, stone-unitary-group-correspondence, strongly-continuous-unitary-group, stone-self-adjoint-correspondence |
| st.def.unitary-group | st.thm.self-adjoint-implies-unitary-group | 0.3835 | 0.3397 | 0.3171 | 0.1953 | 0.1538 | definitional-expansion | strongly-continuous-unitary-group, unitary-group-definition |
| st.def.self-adjoint-operator | st.thm.unitary-group-implies-self-adjoint-generator | 0.3811 | 0.3854 | 0.3652 | 0.3158 | 0.2632 | definitional-expansion | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, self-adjoint-operator-definition |
| st.thm.unitary-group-implies-self-adjoint-generator | st.thm.stone-correspondence | 0.3773 | 0.6148 | 0.5813 | 0.644 | 0.7368 | model-transfer | unbounded-generator-graph, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-generator-characterization |
| st.def.unitary-group | st.thm.unitary-group-implies-self-adjoint-generator | 0.3768 | 0.3103 | 0.2992 | 0.1902 | 0.1333 | definitional-expansion | strongly-continuous-unitary-group, unitary-group-definition |
| st.def.unitary-group | st.thm.stone-correspondence | 0.3691 | 0.3001 | 0.2804 | 0.1683 | 0.1 | definitional-expansion | strongly-continuous-unitary-group, unitary-group-definition |
| st.thm.spectral-theorem-functional-calculus | st.thm.self-adjoint-implies-unitary-group | 0.3617 | 0.5397 | 0.4802 | 0.488 | 0.4706 | implication-schema-transfer | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| st.def.self-adjoint-operator | st.thm.stone-correspondence | 0.3584 | 0.3202 | 0.3179 | 0.3047 | 0.3182 | definitional-expansion | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, stone-unitary-group-correspondence, strongly-continuous-unitary-group |
| st.thm.self-adjoint-implies-unitary-group | st.thm.stone-correspondence | 0.3568 | 0.5669 | 0.5239 | 0.62 | 0.6316 | model-transfer | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| st.def.self-adjoint-operator | st.thm.spectral-theorem-functional-calculus | 0.3475 | 0.2964 | 0.2809 | 0.2009 | 0.15 | definitional-expansion | self-adjoint-operator-on-hilbert-space, self-adjoint-operator-definition, self-adjoint-spectral-calculus |
| st.thm.self-adjoint-implies-unitary-group | st.thm.unitary-group-implies-self-adjoint-generator | 0.3402 | 0.4998 | 0.4854 | 0.6288 | 0.625 | implication-schema-transfer | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| st.def.unitary-group | st.thm.spectral-theorem-functional-calculus | 0.3247 | 0.1937 | 0.1777 | 0.0347 | 0.0 | definitional-expansion | unitary-group-analysis, unitary-group, generator |
| st.thm.self-adjoint-implies-unitary-group | st.app.schrodinger-time-evolution | 0.3183 | 0.5722 | 0.5461 | 0.6816 | 0.7857 | implication-schema-transfer | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| st.thm.spectral-theorem-functional-calculus | st.thm.stone-correspondence | 0.316 | 0.4067 | 0.3594 | 0.3721 | 0.3333 | model-transfer | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| st.thm.spectral-theorem-functional-calculus | st.thm.unitary-group-implies-self-adjoint-generator | 0.3076 | 0.366 | 0.342 | 0.3871 | 0.4211 | implication-schema-transfer | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| st.prop.generator-domain-regularity | st.thm.unitary-group-implies-self-adjoint-generator | 0.2997 | 0.5031 | 0.4327 | 0.3945 | 0.3333 | model-transfer | unbounded-generator-graph, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, self-adjoint-operator-definition |
| st.def.unitary-group | st.ex.translation-group-on-l2 | 0.2914 | 0.4212 | 0.4042 | 0.3557 | 0.2857 | definitional-expansion | strongly-continuous-unitary-group, unitary-group-definition |
| st.thm.spectral-theorem-functional-calculus | st.app.schrodinger-time-evolution | 0.2898 | 0.4529 | 0.413 | 0.4775 | 0.4444 | implication-schema-transfer | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| st.def.self-adjoint-operator | st.app.schrodinger-time-evolution | 0.275 | 0.4291 | 0.4057 | 0.358 | 0.3529 | definitional-expansion | self-adjoint-operator-on-hilbert-space, stone-unitary-group-correspondence, strongly-continuous-unitary-group, stone-self-adjoint-correspondence |
| st.def.unitary-group | st.prop.generator-symmetry | 0.2729 | 0.3559 | 0.3572 | 0.362 | 0.375 | definitional-expansion | strongly-continuous-unitary-group, operator-theoretic-Hilbert-space, unitary-group-definition |

## Abductive Loop Plan

### Round 1
- Objective: Prioritize intervention targets by graph influence and unresolved dependencies.
- Targets: st.thm.stone-correspondence, st.thm.unitary-group-implies-self-adjoint-generator, st.thm.self-adjoint-implies-unitary-group, st.thm.spectral-theorem-functional-calculus, st.def.self-adjoint-operator, st.prop.generator-domain-regularity
- Action: Run kb-abduce on each target to propose missing-premise hypotheses.

### Round 2
- Objective: Test high-value intra-component transfer links (fallback mode) as abductive support hypotheses.
- Candidate connections: st.def.self-adjoint-operator->st.thm.self-adjoint-implies-unitary-group (0.3911), st.def.unitary-group->st.thm.self-adjoint-implies-unitary-group (0.3835), st.def.self-adjoint-operator->st.thm.unitary-group-implies-self-adjoint-generator (0.3811), st.thm.unitary-group-implies-self-adjoint-generator->st.thm.stone-correspondence (0.3773), st.def.unitary-group->st.thm.unitary-group-implies-self-adjoint-generator (0.3768), st.def.unitary-group->st.thm.stone-correspondence (0.3691)
- Action: Convert top links into conjectural dependencies and run kb-deduce for consequence checks.

### Round 3
- Objective: Refine and retain only hypotheses with best explanatory and deductive payoff.
- Action: Re-score interventions, drop contradicted links, and keep top surviving pathways.
