# KB Connection Analysis: `/Users/user/files/abducer/abducer/artifacts/riesz-markov-kakutani-representation-theorem/discovery-simulation/working-kb/riesz-markov-kakutani-representation-theorem.kb.md`

## Stats

- Ontology profile: functional-analysis-measure-representation
- Included statuses: accepted, tentative
- Statements: 10
- Filtered out statements: 0
- Dependency edges: 15
- Components: 1
- Candidate generation mode: intra-component-fallback
- Cross-component candidates (pre-trim): 0
- Intra-component candidates (pre-trim): 43
- Missing dependencies: 0
- Avg semantic connection score: 0.3324
- Avg concept alignment: 0.3189
- Avg specificity alignment: 0.3496
- Concept profile coverage: 1.0
- Specific profile coverage: 1.0
- Concept graph nodes: 92

## Top Intervention Points

| statement_id | kind | score | unresolved | downstream | theory_relevance | specificity | concept_focus | partner |
|---|---|---|---|---|---|---|---|---|
| st.thm.riesz-markov-kakutani | theorem | 0.6514 | 0 | 2 | 1.0 | 1.0 | regular-measure-implies-positive-functional, positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space | - |
| st.thm.positive-functional-implies-measure | theorem | 0.606 | 0 | 3 | 1.0 | 1.0 | regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration | - |
| st.prop.integration-defines-functional | proposition | 0.5544 | 0 | 3 | 0.7865 | 1.0 | regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration | - |
| st.lem.uniqueness-from-cc-separation | lemma | 0.5362 | 0 | 3 | 0.9418 | 1.0 | regular-measure-implies-positive-functional, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional | - |
| st.def.cc-space | definition | 0.5297 | 0 | 8 | 0.5651 | 0.7778 | positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition | - |
| st.def.positive-linear-functional | definition | 0.4561 | 0 | 4 | 0.8253 | 1.0 | positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-representation, functional-measure-correspondence | - |
| st.def.lch-space | definition | 0.4232 | 0 | 9 | 0.4884 | 0.4667 | locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space | - |
| st.cor.c0-dual-representation | corollary | 0.4006 | 0 | 0 | 0.9418 | 1.0 | regular-measure-implies-positive-functional, c0-dual-implies-signed-regular-measure, total-variation-equals-dual-norm, regular-borel-measure-on-lch-space | - |
| st.lem.compact-open-approximation | lemma | 0.3954 | 0 | 5 | 0.6815 | 0.7778 | unconditional, locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions | - |
| st.ex.dirac-measure-evaluation | example | 0.3304 | 0 | 0 | 0.739 | 0.9 | regular-measure-implies-positive-functional, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional | - |

## Mathematical Concept Profiles (Interventions)

### st.thm.riesz-markov-kakutani
- Concept focus: regular-measure-implies-positive-functional, positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-representation
- Claim signatures: integration-defines-positive-functional, riesz-markov-kakutani-correspondence, locally-compact-hausdorff-definition, regular-borel-measure-definition, positive-functional-definition, cc-space-definition
- Antecedent signatures: positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space
- Consequence signatures: positive-linear-functional-on-cc-space, regular-borel-measure-representation, positive-functional-via-integration, regular-borel-measure-on-lch-space, functional-measure-correspondence, unique-representing-measure
- Model signatures: compactly-supported-continuous-functions, integration-pairing-model, locally-compact-Hausdorff-space, measure-representation-correspondence, positive-functional-model, regular-Borel-measure-model
- Reduction signatures: 
- Implication signatures: regular-measure-implies-positive-functional, positive-functional-implies-regular-measure
- Complexity classes: 
- Core problems: C_c-space, Riesz-Markov-Kakutani, integration-pairing, locally-compact-Hausdorff-space, positive-linear-functional, regular-Borel-measure
- Proof regimes: compact-open-approximation, duality-method, function-space-duality, integration-representation, measure-representation, positivity-method, regularity-reconstruction, topological-regularity
- Barrier signals: topological-regularity-reconstruction

### st.thm.positive-functional-implies-measure
- Concept focus: regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional
- Claim signatures: integration-defines-positive-functional, regular-borel-measure-definition, positive-functional-definition, cc-space-definition
- Antecedent signatures: positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space
- Consequence signatures: positive-linear-functional-on-cc-space, positive-functional-via-integration, regular-borel-measure-on-lch-space
- Model signatures: compactly-supported-continuous-functions, integration-pairing-model, positive-functional-model, regular-Borel-measure-model
- Reduction signatures: 
- Implication signatures: regular-measure-implies-positive-functional
- Complexity classes: 
- Core problems: C_c-space, integration-pairing, positive-linear-functional, regular-Borel-measure
- Proof regimes: compact-open-approximation, duality-method, function-space-duality, measure-representation, positivity-method, regularity-reconstruction
- Barrier signals: barrier, positivity-to-sigma-additivity, topological-regularity-reconstruction

### st.prop.integration-defines-functional
- Concept focus: regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional
- Claim signatures: integration-defines-positive-functional, regular-borel-measure-definition, positive-functional-definition, cc-space-definition
- Antecedent signatures: positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space
- Consequence signatures: positive-linear-functional-on-cc-space, positive-functional-via-integration, regular-borel-measure-on-lch-space
- Model signatures: compactly-supported-continuous-functions, integration-pairing-model, positive-functional-model, regular-Borel-measure-model
- Reduction signatures: 
- Implication signatures: regular-measure-implies-positive-functional
- Complexity classes: 
- Core problems: C_c-space, integration-pairing, positive-linear-functional, regular-Borel-measure
- Proof regimes: duality-method, function-space-duality, integration-representation, measure-representation, positivity-method, regularity-reconstruction
- Barrier signals: positivity-to-sigma-additivity, topological-regularity-reconstruction

### st.lem.uniqueness-from-cc-separation
- Concept focus: regular-measure-implies-positive-functional, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional, regular-borel-measure-definition
- Claim signatures: integration-defines-positive-functional, regular-borel-measure-definition, cc-space-definition
- Antecedent signatures: regular-borel-measure-on-lch-space
- Consequence signatures: positive-functional-via-integration, regular-borel-measure-on-lch-space
- Model signatures: compactly-supported-continuous-functions, integration-pairing-model, regular-Borel-measure-model
- Reduction signatures: 
- Implication signatures: regular-measure-implies-positive-functional
- Complexity classes: 
- Core problems: C_c-space, integration-pairing, regular-Borel-measure
- Proof regimes: compact-open-approximation, integration-representation, measure-representation, regularity-reconstruction
- Barrier signals: barrier, compact-open-approximation, topological-regularity-reconstruction

### st.def.cc-space
- Concept focus: positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition, compactly-supported-continuous-functions
- Claim signatures: locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition
- Antecedent signatures: positive-linear-functional-on-cc-space
- Consequence signatures: positive-linear-functional-on-cc-space
- Model signatures: compactly-supported-continuous-functions, locally-compact-Hausdorff-space, positive-functional-model
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: C_c-space, locally-compact-Hausdorff-space, positive-linear-functional, regular-Borel-measure
- Proof regimes: compact-open-approximation, duality-method, function-space-duality, measure-representation, positivity-method
- Barrier signals: compact-open-approximation, positivity-to-sigma-additivity

### st.def.positive-linear-functional
- Concept focus: positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-representation, functional-measure-correspondence, unique-representing-measure
- Claim signatures: riesz-markov-kakutani-correspondence, positive-functional-definition, cc-space-definition
- Antecedent signatures: positive-linear-functional-on-cc-space
- Consequence signatures: positive-linear-functional-on-cc-space, regular-borel-measure-representation, functional-measure-correspondence, unique-representing-measure
- Model signatures: compactly-supported-continuous-functions, measure-representation-correspondence, positive-functional-model
- Reduction signatures: 
- Implication signatures: positive-functional-implies-regular-measure
- Complexity classes: 
- Core problems: C_c-space, Riesz-Markov-Kakutani, positive-linear-functional, regular-Borel-measure
- Proof regimes: duality-method, function-space-duality, measure-representation, positivity-method
- Barrier signals: barrier, positivity-to-sigma-additivity

### st.def.lch-space
- Concept focus: locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space, C_c-space
- Claim signatures: locally-compact-hausdorff-definition, cc-space-definition
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: compactly-supported-continuous-functions, locally-compact-Hausdorff-space
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: C_c-space, locally-compact-Hausdorff-space, regular-Borel-measure
- Proof regimes: compact-open-approximation, measure-representation, regularity-reconstruction, topological-regularity
- Barrier signals: compact-open-approximation

### st.cor.c0-dual-representation
- Concept focus: regular-measure-implies-positive-functional, c0-dual-implies-signed-regular-measure, total-variation-equals-dual-norm, regular-borel-measure-on-lch-space, continuous-linear-functional-on-c0
- Claim signatures: integration-defines-positive-functional, regular-borel-measure-definition, c0-dual-measure-representation, total-variation-norm-identity
- Antecedent signatures: regular-borel-measure-on-lch-space, continuous-linear-functional-on-c0
- Consequence signatures: positive-functional-via-integration, regular-borel-measure-on-lch-space, signed-regular-measure-duality, dual-norm-total-variation
- Model signatures: integration-pairing-model, measure-representation-correspondence, positive-functional-model, regular-Borel-measure-model, signed-measure-decomposition, vanishing-at-infinity-function-space
- Reduction signatures: 
- Implication signatures: regular-measure-implies-positive-functional, c0-dual-implies-signed-regular-measure, total-variation-equals-dual-norm
- Complexity classes: 
- Core problems: C0-dual, integration-pairing, positive-linear-functional, regular-Borel-measure, total-variation
- Proof regimes: duality-method, function-space-duality, integration-representation, measure-representation, regularity-reconstruction, signed-measure-decomposition
- Barrier signals: barrier, signed-decomposition-control, topological-regularity-reconstruction

### st.lem.compact-open-approximation
- Concept focus: unconditional, locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space
- Claim signatures: locally-compact-hausdorff-definition, cc-space-definition
- Antecedent signatures: unconditional
- Consequence signatures: locally-compact-hausdorff-definition, cc-space-definition
- Model signatures: compactly-supported-continuous-functions, locally-compact-Hausdorff-space
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: C_c-space, locally-compact-Hausdorff-space
- Proof regimes: compact-open-approximation, regularity-reconstruction, topological-regularity
- Barrier signals: barrier, compact-open-approximation

### st.ex.dirac-measure-evaluation
- Concept focus: regular-measure-implies-positive-functional, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional, dirac-evaluation-example
- Claim signatures: integration-defines-positive-functional, dirac-evaluation-example, cc-space-definition
- Antecedent signatures: regular-borel-measure-on-lch-space
- Consequence signatures: positive-functional-via-integration
- Model signatures: compactly-supported-continuous-functions
- Reduction signatures: 
- Implication signatures: regular-measure-implies-positive-functional
- Complexity classes: 
- Core problems: C_c-space, integration-pairing, regular-Borel-measure
- Proof regimes: integration-representation, measure-representation
- Barrier signals: 

## Top Connection Candidates

| from_id | to_id | score | structural_similarity | semantic | concept_alignment | specific_alignment | relation | concept_evidence |
|---|---|---|---|---|---|---|---|---|
| st.def.cc-space | st.thm.positive-functional-implies-measure | 0.3909 | 0.3899 | 0.3771 | 0.3492 | 0.3571 | definitional-expansion | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positive-functional-definition, positive-functional-model |
| st.def.cc-space | st.thm.riesz-markov-kakutani | 0.3788 | 0.351 | 0.3495 | 0.3443 | 0.35 | definitional-expansion | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space |
| st.def.lch-space | st.thm.riesz-markov-kakutani | 0.374 | 0.3236 | 0.301 | 0.1963 | 0.2 | definitional-expansion | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, cc-space-definition |
| st.lem.uniqueness-from-cc-separation | st.thm.positive-functional-implies-measure | 0.3562 | 0.6084 | 0.578 | 0.6525 | 0.75 | implication-schema-transfer | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-functional-via-integration |
| st.def.lch-space | st.thm.positive-functional-implies-measure | 0.3548 | 0.277 | 0.2553 | 0.1368 | 0.1429 | definitional-expansion | compactly-supported-continuous-functions, cc-space-definition |
| st.prop.integration-defines-functional | st.thm.positive-functional-implies-measure | 0.3501 | 0.7047 | 0.6872 | 0.8727 | 1.0 | implication-schema-transfer | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-linear-functional-on-cc-space |
| st.def.lch-space | st.lem.compact-open-approximation | 0.3423 | 0.4413 | 0.4734 | 0.48 | 0.8 | definitional-expansion | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, cc-space-definition |
| st.def.positive-linear-functional | st.thm.positive-functional-implies-measure | 0.3418 | 0.3954 | 0.3798 | 0.335 | 0.2778 | definitional-expansion | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positive-functional-definition, positive-functional-model |
| st.thm.positive-functional-implies-measure | st.thm.riesz-markov-kakutani | 0.3416 | 0.5833 | 0.5344 | 0.5897 | 0.6 | implication-schema-transfer | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-linear-functional-on-cc-space |
| st.def.positive-linear-functional | st.thm.riesz-markov-kakutani | 0.3401 | 0.3643 | 0.3904 | 0.4653 | 0.55 | definitional-expansion | positive-functional-implies-regular-measure, compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, measure-representation-correspondence |
| st.def.cc-space | st.def.positive-linear-functional | 0.317 | 0.5035 | 0.4762 | 0.4258 | 0.3846 | definitional-expansion | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positive-functional-definition, positive-functional-model |
| st.def.lch-space | st.def.cc-space | 0.3143 | 0.4336 | 0.4454 | 0.334 | 0.5714 | definitional-expansion | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, cc-space-definition |
| st.lem.uniqueness-from-cc-separation | st.thm.riesz-markov-kakutani | 0.2978 | 0.4605 | 0.4172 | 0.4315 | 0.45 | implication-schema-transfer | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-functional-via-integration |
| st.prop.integration-defines-functional | st.thm.riesz-markov-kakutani | 0.2929 | 0.5718 | 0.5258 | 0.5966 | 0.6 | implication-schema-transfer | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-linear-functional-on-cc-space |
| st.def.cc-space | st.lem.compact-open-approximation | 0.2917 | 0.3114 | 0.3388 | 0.2944 | 0.5 | definitional-expansion | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, cc-space-definition |
| st.def.lch-space | st.lem.uniqueness-from-cc-separation | 0.2822 | 0.2976 | 0.2755 | 0.1897 | 0.1818 | definitional-expansion | compactly-supported-continuous-functions, cc-space-definition |
| st.thm.positive-functional-implies-measure | st.cor.c0-dual-representation | 0.26 | 0.3446 | 0.3189 | 0.3596 | 0.3636 | model-transfer | regular-measure-implies-positive-functional, integration-defines-positive-functional, positive-functional-via-integration, regular-borel-measure-on-lch-space |
| st.def.lch-space | st.cor.c0-dual-representation | 0.2563 | 0.2072 | 0.1869 | 0.0322 | 0.0 | definitional-expansion | regularity-reconstruction, measure-representation, regular-Borel-measure |
| st.def.cc-space | st.lem.uniqueness-from-cc-separation | 0.2521 | 0.2194 | 0.2145 | 0.135 | 0.1429 | definitional-expansion | compactly-supported-continuous-functions, cc-space-definition |
| st.def.cc-space | st.prop.integration-defines-functional | 0.2503 | 0.3176 | 0.3234 | 0.3312 | 0.3571 | definitional-expansion | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positive-functional-definition, positive-functional-model |

## Abductive Loop Plan

### Round 1
- Objective: Prioritize intervention targets by graph influence and unresolved dependencies.
- Targets: st.thm.riesz-markov-kakutani, st.thm.positive-functional-implies-measure, st.prop.integration-defines-functional, st.lem.uniqueness-from-cc-separation, st.def.cc-space, st.def.positive-linear-functional
- Action: Run kb-abduce on each target to propose missing-premise hypotheses.

### Round 2
- Objective: Test high-value intra-component transfer links (fallback mode) as abductive support hypotheses.
- Candidate connections: st.def.cc-space->st.thm.positive-functional-implies-measure (0.3909), st.def.cc-space->st.thm.riesz-markov-kakutani (0.3788), st.def.lch-space->st.thm.riesz-markov-kakutani (0.374), st.lem.uniqueness-from-cc-separation->st.thm.positive-functional-implies-measure (0.3562), st.def.lch-space->st.thm.positive-functional-implies-measure (0.3548), st.prop.integration-defines-functional->st.thm.positive-functional-implies-measure (0.3501)
- Action: Convert top links into conjectural dependencies and run kb-deduce for consequence checks.

### Round 3
- Objective: Refine and retain only hypotheses with best explanatory and deductive payoff.
- Action: Re-score interventions, drop contradicted links, and keep top surviving pathways.
