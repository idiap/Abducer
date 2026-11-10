# KB Connection Analysis: `/Users/user/files/abducer/abducer/artifacts/riesz-markov-kakutani-representation-theorem/discovery-simulation/working-kb/riesz-markov-kakutani-representation-theorem.kb.md`

## Stats

- Ontology profile: functional-analysis-measure-representation
- Included statuses: accepted, tentative
- Statements: 10
- Filtered out statements: 0
- Dependency edges: 16
- Components: 1
- Candidate generation mode: intra-component-fallback
- Cross-component candidates (pre-trim): 0
- Intra-component candidates (pre-trim): 45
- Missing dependencies: 0
- Avg semantic connection score: 0.3035
- Avg concept alignment: 0.2611
- Avg specificity alignment: 0.2871
- Concept profile coverage: 1.0
- Specific profile coverage: 1.0
- Concept graph nodes: 95

## Top Intervention Points

| statement_id | kind | score | unresolved | downstream | theory_relevance | specificity | concept_focus | partner |
|---|---|---|---|---|---|---|---|---|
| st.thm.riesz-markov-kakutani | theorem | 0.6704 | 0 | 2 | 1.0 | 1.0 | positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-representation | - |
| st.prop.integration-defines-functional | proposition | 0.5466 | 0 | 3 | 0.7865 | 1.0 | regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration | - |
| st.def.cc-space | definition | 0.5443 | 0 | 8 | 0.5651 | 0.7778 | positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition | - |
| st.thm.positive-functional-implies-measure | theorem | 0.5436 | 0 | 3 | 0.7397 | 0.7778 | positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-definition, positive-functional-definition | - |
| st.lem.uniqueness-from-cc-separation | lemma | 0.5144 | 0 | 3 | 0.9418 | 1.0 | function-separation-implies-measure-uniqueness, compact-open-approximation-on-lch-space, regular-borel-measure-on-lch-space, unique-representing-measure | - |
| st.def.positive-linear-functional | definition | 0.5098 | 0 | 4 | 0.8253 | 1.0 | positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-representation, functional-measure-correspondence | - |
| st.lem.compact-open-approximation | lemma | 0.4807 | 0 | 5 | 0.9418 | 1.0 | compact-open-approximation-supports-regularity, compact-open-approximation-on-lch-space, compact-open-regularity-witness, locally-compact-hausdorff-definition | - |
| st.def.lch-space | definition | 0.4513 | 0 | 9 | 0.4884 | 0.4667 | locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space | - |
| st.cor.c0-dual-representation | corollary | 0.3781 | 0 | 0 | 0.9418 | 1.0 | c0-dual-implies-signed-regular-measure, total-variation-equals-dual-norm, regular-borel-measure-on-lch-space, continuous-linear-functional-on-c0 | - |
| st.ex.dirac-measure-evaluation | example | 0.1978 | 0 | 0 | 0.4021 | 0.3667 | dirac-evaluation-example, cc-space-definition, compactly-supported-continuous-functions, C_c-space | - |

## Mathematical Concept Profiles (Interventions)

### st.thm.riesz-markov-kakutani
- Concept focus: positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-representation, functional-measure-correspondence
- Claim signatures: riesz-markov-kakutani-correspondence, locally-compact-hausdorff-definition, regular-borel-measure-definition, positive-functional-definition, cc-space-definition
- Antecedent signatures: positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space
- Consequence signatures: positive-linear-functional-on-cc-space, regular-borel-measure-representation, regular-borel-measure-on-lch-space, functional-measure-correspondence, unique-representing-measure
- Model signatures: compactly-supported-continuous-functions, integration-pairing-model, locally-compact-Hausdorff-space, measure-representation-correspondence, positive-functional-model, regular-Borel-measure-model
- Reduction signatures: 
- Implication signatures: positive-functional-implies-regular-measure
- Complexity classes: 
- Core problems: C_c-space, Riesz-Markov-Kakutani, integration-pairing, locally-compact-Hausdorff-space, positive-linear-functional, regular-Borel-measure
- Proof regimes: compact-open-approximation, duality-method, function-space-duality, integration-representation, measure-representation, positivity-method, regularity-reconstruction, topological-regularity
- Barrier signals: topological-regularity-reconstruction

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

### st.thm.positive-functional-implies-measure
- Concept focus: positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-definition, positive-functional-definition, cc-space-definition
- Claim signatures: regular-borel-measure-definition, positive-functional-definition, cc-space-definition
- Antecedent signatures: positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space
- Consequence signatures: positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space
- Model signatures: compactly-supported-continuous-functions, integration-pairing-model, positive-functional-model, regular-Borel-measure-model
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: C_c-space, integration-pairing, positive-linear-functional, regular-Borel-measure
- Proof regimes: compact-open-approximation, duality-method, function-space-duality, measure-representation, positivity-method, regularity-reconstruction
- Barrier signals: barrier, positivity-to-sigma-additivity, topological-regularity-reconstruction

### st.lem.uniqueness-from-cc-separation
- Concept focus: function-separation-implies-measure-uniqueness, compact-open-approximation-on-lch-space, regular-borel-measure-on-lch-space, unique-representing-measure, uniqueness-from-cc-separation
- Claim signatures: uniqueness-from-cc-separation, regular-borel-measure-definition, cc-space-definition
- Antecedent signatures: compact-open-approximation-on-lch-space, regular-borel-measure-on-lch-space
- Consequence signatures: regular-borel-measure-on-lch-space, unique-representing-measure
- Model signatures: compactly-supported-continuous-functions, integration-pairing-model, regular-Borel-measure-model
- Reduction signatures: 
- Implication signatures: function-separation-implies-measure-uniqueness
- Complexity classes: 
- Core problems: C_c-space, integration-pairing, regular-Borel-measure
- Proof regimes: compact-open-approximation, integration-representation, measure-representation, regularity-reconstruction
- Barrier signals: barrier, compact-open-approximation, topological-regularity-reconstruction

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

### st.lem.compact-open-approximation
- Concept focus: compact-open-approximation-supports-regularity, compact-open-approximation-on-lch-space, compact-open-regularity-witness, locally-compact-hausdorff-definition, compact-open-approximation-lemma
- Claim signatures: locally-compact-hausdorff-definition, compact-open-approximation-lemma, cc-space-definition
- Antecedent signatures: compact-open-approximation-on-lch-space
- Consequence signatures: compact-open-regularity-witness
- Model signatures: compactly-supported-continuous-functions, locally-compact-Hausdorff-space
- Reduction signatures: 
- Implication signatures: compact-open-approximation-supports-regularity
- Complexity classes: 
- Core problems: C_c-space, locally-compact-Hausdorff-space
- Proof regimes: compact-open-approximation, regularity-reconstruction, topological-regularity
- Barrier signals: barrier, compact-open-approximation

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
- Concept focus: c0-dual-implies-signed-regular-measure, total-variation-equals-dual-norm, regular-borel-measure-on-lch-space, continuous-linear-functional-on-c0, signed-regular-measure-duality
- Claim signatures: regular-borel-measure-definition, c0-dual-measure-representation, total-variation-norm-identity
- Antecedent signatures: regular-borel-measure-on-lch-space, continuous-linear-functional-on-c0
- Consequence signatures: regular-borel-measure-on-lch-space, signed-regular-measure-duality, dual-norm-total-variation
- Model signatures: integration-pairing-model, measure-representation-correspondence, positive-functional-model, regular-Borel-measure-model, signed-measure-decomposition, vanishing-at-infinity-function-space
- Reduction signatures: 
- Implication signatures: c0-dual-implies-signed-regular-measure, total-variation-equals-dual-norm
- Complexity classes: 
- Core problems: C0-dual, integration-pairing, positive-linear-functional, regular-Borel-measure, total-variation
- Proof regimes: duality-method, function-space-duality, integration-representation, measure-representation, regularity-reconstruction, signed-measure-decomposition
- Barrier signals: barrier, signed-decomposition-control, topological-regularity-reconstruction

### st.ex.dirac-measure-evaluation
- Concept focus: dirac-evaluation-example, cc-space-definition, compactly-supported-continuous-functions, C_c-space, integration-pairing
- Claim signatures: dirac-evaluation-example, cc-space-definition
- Antecedent signatures: 
- Consequence signatures: 
- Model signatures: compactly-supported-continuous-functions
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: C_c-space, integration-pairing, regular-Borel-measure
- Proof regimes: integration-representation, measure-representation
- Barrier signals: 

## Top Connection Candidates

| from_id | to_id | score | structural_similarity | semantic | concept_alignment | specific_alignment | relation | concept_evidence |
|---|---|---|---|---|---|---|---|---|
| st.def.cc-space | st.thm.positive-functional-implies-measure | 0.4007 | 0.4085 | 0.4034 | 0.3845 | 0.4545 | definitional-expansion | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positive-functional-definition, positive-functional-model |
| st.def.cc-space | st.thm.riesz-markov-kakutani | 0.385 | 0.3627 | 0.3661 | 0.366 | 0.4118 | definitional-expansion | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space |
| st.def.lch-space | st.thm.riesz-markov-kakutani | 0.3776 | 0.3303 | 0.3104 | 0.2086 | 0.2353 | definitional-expansion | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, cc-space-definition |
| st.def.lch-space | st.thm.positive-functional-implies-measure | 0.3584 | 0.2837 | 0.265 | 0.1461 | 0.1818 | definitional-expansion | compactly-supported-continuous-functions, cc-space-definition |
| st.def.positive-linear-functional | st.thm.riesz-markov-kakutani | 0.3552 | 0.3935 | 0.4308 | 0.5771 | 0.6471 | definitional-expansion | positive-functional-implies-regular-measure, compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, measure-representation-correspondence |
| st.def.positive-linear-functional | st.thm.positive-functional-implies-measure | 0.3475 | 0.4063 | 0.3952 | 0.3568 | 0.3333 | declared-dependency | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positive-functional-definition, positive-functional-model |
| st.thm.positive-functional-implies-measure | st.thm.riesz-markov-kakutani | 0.34 | 0.5591 | 0.5018 | 0.4874 | 0.5294 | declared-dependency | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-definition |
| st.def.lch-space | st.lem.compact-open-approximation | 0.34 | 0.3908 | 0.401 | 0.4187 | 0.5 | declared-dependency | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, cc-space-definition |
| st.def.cc-space | st.def.positive-linear-functional | 0.34 | 0.5035 | 0.4762 | 0.4258 | 0.3846 | declared-dependency | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positive-functional-definition, positive-functional-model |
| st.def.lch-space | st.def.cc-space | 0.34 | 0.4336 | 0.4454 | 0.334 | 0.5714 | declared-dependency | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, cc-space-definition |
| st.lem.uniqueness-from-cc-separation | st.thm.riesz-markov-kakutani | 0.34 | 0.431 | 0.3766 | 0.311 | 0.35 | declared-dependency | compactly-supported-continuous-functions, regular-borel-measure-on-lch-space, regular-borel-measure-definition, unique-representing-measure |
| st.def.cc-space | st.lem.compact-open-approximation | 0.34 | 0.2881 | 0.3055 | 0.264 | 0.3636 | declared-dependency | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, cc-space-definition |
| st.prop.integration-defines-functional | st.thm.riesz-markov-kakutani | 0.34 | 0.533 | 0.4729 | 0.469 | 0.45 | declared-dependency | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-definition |
| st.def.cc-space | st.lem.uniqueness-from-cc-separation | 0.34 | 0.2167 | 0.2114 | 0.1349 | 0.1333 | declared-dependency | compactly-supported-continuous-functions, cc-space-definition |
| st.def.cc-space | st.prop.integration-defines-functional | 0.34 | 0.3176 | 0.3234 | 0.3312 | 0.3571 | declared-dependency | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positive-functional-definition, positive-functional-model |
| st.thm.riesz-markov-kakutani | st.cor.c0-dual-representation | 0.34 | 0.3378 | 0.2916 | 0.2445 | 0.2308 | declared-dependency | measure-representation-correspondence, regular-borel-measure-on-lch-space, regular-borel-measure-definition, regular-Borel-measure-model |
| st.lem.compact-open-approximation | st.thm.positive-functional-implies-measure | 0.34 | 0.1776 | 0.1556 | 0.1189 | 0.1333 | declared-dependency | compactly-supported-continuous-functions, cc-space-definition |
| st.def.lch-space | st.prop.integration-defines-functional | 0.34 | 0.2102 | 0.2057 | 0.1221 | 0.1429 | declared-dependency | compactly-supported-continuous-functions, cc-space-definition |
| st.thm.riesz-markov-kakutani | st.ex.dirac-measure-evaluation | 0.34 | 0.267 | 0.2208 | 0.1189 | 0.1111 | declared-dependency | compactly-supported-continuous-functions, cc-space-definition |
| st.prop.integration-defines-functional | st.ex.dirac-measure-evaluation | 0.34 | 0.24 | 0.28 | 0.3 | 0.25 | declared-dependency | compactly-supported-continuous-functions, integration-representation, measure-representation, regular-Borel-measure |

## Abductive Loop Plan

### Round 1
- Objective: Prioritize intervention targets by graph influence and unresolved dependencies.
- Targets: st.thm.riesz-markov-kakutani, st.prop.integration-defines-functional, st.def.cc-space, st.thm.positive-functional-implies-measure, st.lem.uniqueness-from-cc-separation, st.def.positive-linear-functional
- Action: Run kb-abduce on each target to propose missing-premise hypotheses.

### Round 2
- Objective: Test high-value intra-component transfer links (fallback mode) as abductive support hypotheses.
- Candidate connections: st.def.cc-space->st.thm.positive-functional-implies-measure (0.4007), st.def.cc-space->st.thm.riesz-markov-kakutani (0.385), st.def.lch-space->st.thm.riesz-markov-kakutani (0.3776), st.def.lch-space->st.thm.positive-functional-implies-measure (0.3584), st.def.positive-linear-functional->st.thm.riesz-markov-kakutani (0.3552), st.def.positive-linear-functional->st.thm.positive-functional-implies-measure (0.3475)
- Action: Convert top links into conjectural dependencies and run kb-deduce for consequence checks.

### Round 3
- Objective: Refine and retain only hypotheses with best explanatory and deductive payoff.
- Action: Re-score interventions, drop contradicted links, and keep top surviving pathways.
