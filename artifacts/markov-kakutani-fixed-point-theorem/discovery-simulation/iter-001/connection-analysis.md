# KB Connection Analysis: `/Users/user/files/abducer/abducer/artifacts/markov-kakutani-fixed-point-theorem/discovery-simulation/working-kb/markov-kakutani-fixed-point-theorem.kb.md`

## Stats

- Ontology profile: functional-analysis-convex-fixed-point
- Included statuses: accepted, tentative
- Statements: 8
- Filtered out statements: 0
- Dependency edges: 10
- Components: 1
- Candidate generation mode: intra-component-fallback
- Cross-component candidates (pre-trim): 0
- Intra-component candidates (pre-trim): 28
- Missing dependencies: 0
- Avg semantic connection score: 0.3223
- Avg concept alignment: 0.3015
- Avg specificity alignment: 0.2806
- Concept profile coverage: 1.0
- Specific profile coverage: 1.0
- Concept graph nodes: 91

## Top Intervention Points

| statement_id | kind | score | unresolved | downstream | theory_relevance | specificity | concept_focus | partner |
|---|---|---|---|---|---|---|---|---|
| st.lem.single-map-fixed-point | lemma | 0.6948 | 0 | 5 | 0.9418 | 1.0 | single-map-fixed-point-implies-invariant-fixed-point-subset, finite-intersection-property-implies-common-fixed-point, continuous-affine-self-map-on-compact-convex-set, commuting-affine-family-on-compact-convex-set | - |
| st.thm.markov-kakutani | theorem | 0.6149 | 0 | 1 | 1.0 | 1.0 | finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset | - |
| st.prop.fixed-point-subset-structure | proposition | 0.6019 | 0 | 4 | 0.7865 | 1.0 | single-map-fixed-point-implies-invariant-fixed-point-subset, single-affine-self-map-on-compact-convex-set, single-affine-self-map-with-fixed-point, nonempty-compact-convex-subset | - |
| st.lem.finite-family-common-fixed-point | lemma | 0.5811 | 0 | 2 | 0.9418 | 1.0 | finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, common-fixed-point-for-finite-commuting-family | - |
| st.lem.cesaro-averages | lemma | 0.536 | 0 | 6 | 0.9418 | 1.0 | affine-averaging-implies-single-map-fixed-point, continuous-affine-self-map-on-compact-convex-set, nonempty-compact-convex-subset, affine-orbit-averages-in-compact-convex-set | - |
| st.ex.interval-commuting-projections | example | 0.49 | 0 | 0 | 0.7865 | 1.0 | finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset | - |
| st.def.compact-convex-set | definition | 0.4374 | 0 | 7 | 0.5322 | 0.6444 | nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset, locally-convex-topological-vector-space | - |
| st.lem.commuting-preserves-fixed-point-subset | lemma | 0.3937 | 0 | 3 | 0.6815 | 0.7778 | commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, invariant-fixed-point-subset, invariant-fixed-point-subset-definition | - |

## Mathematical Concept Profiles (Interventions)

### st.lem.single-map-fixed-point
- Concept focus: single-map-fixed-point-implies-invariant-fixed-point-subset, finite-intersection-property-implies-common-fixed-point, continuous-affine-self-map-on-compact-convex-set, commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set
- Claim signatures: markov-kakutani-common-fixed-point, single-affine-map-fixed-point, compact-convex-set-definition
- Antecedent signatures: continuous-affine-self-map-on-compact-convex-set, commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset
- Consequence signatures: common-fixed-point-for-finite-commuting-family, nonempty-compact-convex-fixed-point-subset, common-fixed-point-for-commuting-family, nonempty-compact-convex-subset, single-map-fixed-point
- Model signatures: common-fixed-point-correspondence, compact-convex-subset, single-affine-self-map
- Reduction signatures: 
- Implication signatures: single-map-fixed-point-implies-invariant-fixed-point-subset, finite-intersection-property-implies-common-fixed-point
- Complexity classes: 
- Core problems: Cesaro-averaging, affine-self-map, common-fixed-point, commuting-affine-family, compact-convex-set
- Proof regimes: affine-averaging, affine-map-analysis, compactness-method, convex-geometry, fixed-point-analysis, separation-method
- Barrier signals: barrier, finite-intersection-compactness, single-map-fixed-point-extraction

### st.thm.markov-kakutani
- Concept focus: finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset, common-fixed-point-for-finite-commuting-family
- Claim signatures: markov-kakutani-common-fixed-point, commuting-affine-family-definition, compact-convex-set-definition
- Antecedent signatures: commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset
- Consequence signatures: common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family, nonempty-compact-convex-subset
- Model signatures: common-fixed-point-correspondence, commuting-affine-self-map-family, compact-convex-subset, locally-convex-topological-vector-space, single-affine-self-map
- Reduction signatures: 
- Implication signatures: finite-intersection-property-implies-common-fixed-point
- Complexity classes: 
- Core problems: Markov-Kakutani, affine-self-map, common-fixed-point, commuting-affine-family, compact-convex-set, invariant-fixed-point-subset
- Proof regimes: affine-map-analysis, commuting-family-analysis, commuting-fixed-point, compactness-method, convex-geometry, fixed-point-analysis, invariant-subset-method, topological-vector-space-analysis
- Barrier signals: barrier, finite-intersection-compactness, invariant-subset-propagation

### st.prop.fixed-point-subset-structure
- Concept focus: single-map-fixed-point-implies-invariant-fixed-point-subset, single-affine-self-map-on-compact-convex-set, single-affine-self-map-with-fixed-point, nonempty-compact-convex-subset, nonempty-compact-convex-fixed-point-subset
- Claim signatures: invariant-fixed-point-subset-definition, compact-convex-set-definition, fixed-point-subset-structure
- Antecedent signatures: single-affine-self-map-on-compact-convex-set, single-affine-self-map-with-fixed-point, nonempty-compact-convex-subset
- Consequence signatures: nonempty-compact-convex-fixed-point-subset, nonempty-compact-convex-subset, invariant-fixed-point-subset
- Model signatures: compact-convex-subset, invariant-fixed-point-subset, single-affine-self-map
- Reduction signatures: 
- Implication signatures: single-map-fixed-point-implies-invariant-fixed-point-subset
- Complexity classes: 
- Core problems: affine-self-map, common-fixed-point, compact-convex-set, invariant-fixed-point-subset
- Proof regimes: affine-map-analysis, compactness-method, convex-geometry, fixed-point-analysis, invariant-subset-method
- Barrier signals: barrier, finite-intersection-compactness, invariant-subset-propagation

### st.lem.finite-family-common-fixed-point
- Concept focus: finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, common-fixed-point-for-finite-commuting-family, common-fixed-point-for-commuting-family
- Claim signatures: markov-kakutani-common-fixed-point, commuting-affine-family-definition, finite-family-common-fixed-point
- Antecedent signatures: commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily
- Consequence signatures: common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family
- Model signatures: common-fixed-point-correspondence, commuting-affine-self-map-family, single-affine-self-map
- Reduction signatures: 
- Implication signatures: finite-intersection-property-implies-common-fixed-point
- Complexity classes: 
- Core problems: affine-self-map, common-fixed-point, commuting-affine-family, compact-convex-set, invariant-fixed-point-subset
- Proof regimes: affine-map-analysis, commuting-family-analysis, compactness-method, fixed-point-analysis, induction-on-family-size, invariant-subset-method
- Barrier signals: barrier, finite-intersection-compactness, invariant-subset-propagation

### st.lem.cesaro-averages
- Concept focus: affine-averaging-implies-single-map-fixed-point, continuous-affine-self-map-on-compact-convex-set, nonempty-compact-convex-subset, affine-orbit-averages-in-compact-convex-set, single-map-fixed-point
- Claim signatures: compact-convex-set-definition, cesaro-average-preservation
- Antecedent signatures: continuous-affine-self-map-on-compact-convex-set, nonempty-compact-convex-subset
- Consequence signatures: affine-orbit-averages-in-compact-convex-set, nonempty-compact-convex-subset, single-map-fixed-point
- Model signatures: cesaro-averaging-scheme, compact-convex-subset, single-affine-self-map
- Reduction signatures: 
- Implication signatures: affine-averaging-implies-single-map-fixed-point
- Complexity classes: 
- Core problems: Cesaro-averaging, affine-self-map, common-fixed-point, compact-convex-set
- Proof regimes: affine-averaging, affine-map-analysis, compactness-method, convex-geometry, fixed-point-analysis
- Barrier signals: barrier, single-map-fixed-point-extraction

### st.ex.interval-commuting-projections
- Concept focus: finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset, common-fixed-point-for-finite-commuting-family
- Claim signatures: markov-kakutani-common-fixed-point, commuting-affine-family-definition, compact-convex-set-definition, common-fixed-point-example
- Antecedent signatures: commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset
- Consequence signatures: common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family, nonempty-compact-convex-subset
- Model signatures: common-fixed-point-correspondence, commuting-affine-self-map-family, compact-convex-subset, single-affine-self-map
- Reduction signatures: 
- Implication signatures: finite-intersection-property-implies-common-fixed-point
- Complexity classes: 
- Core problems: Markov-Kakutani, affine-self-map, common-fixed-point, commuting-affine-family, compact-convex-set
- Proof regimes: affine-map-analysis, commuting-family-analysis, commuting-fixed-point, compactness-method, convex-geometry, fixed-point-analysis
- Barrier signals: finite-intersection-compactness

### st.def.compact-convex-set
- Concept focus: nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset, locally-convex-topological-vector-space, affine-self-map
- Claim signatures: compact-convex-set-definition
- Antecedent signatures: nonempty-compact-convex-subset
- Consequence signatures: nonempty-compact-convex-subset
- Model signatures: compact-convex-subset, locally-convex-topological-vector-space
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: affine-self-map, compact-convex-set, invariant-fixed-point-subset
- Proof regimes: affine-map-analysis, compactness-method, convex-geometry, topological-vector-space-analysis
- Barrier signals: finite-intersection-compactness

### st.lem.commuting-preserves-fixed-point-subset
- Concept focus: commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, invariant-fixed-point-subset, invariant-fixed-point-subset-definition, commuting-affine-family-definition
- Claim signatures: invariant-fixed-point-subset-definition, commuting-affine-family-definition
- Antecedent signatures: commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set
- Consequence signatures: commuting-affine-family-on-compact-convex-set, invariant-fixed-point-subset
- Model signatures: commuting-affine-self-map-family, invariant-fixed-point-subset, single-affine-self-map
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: 
- Core problems: affine-self-map, common-fixed-point, commuting-affine-family, invariant-fixed-point-subset
- Proof regimes: affine-map-analysis, commuting-family-analysis, fixed-point-analysis, invariant-subset-method
- Barrier signals: barrier, invariant-subset-propagation

## Top Connection Candidates

| from_id | to_id | score | structural_similarity | semantic | concept_alignment | specific_alignment | relation | concept_evidence |
|---|---|---|---|---|---|---|---|---|
| st.def.compact-convex-set | st.thm.markov-kakutani | 0.4027 | 0.3788 | 0.3641 | 0.2795 | 0.2857 | declared-dependency | locally-convex-topological-vector-space, nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset |
| st.lem.single-map-fixed-point | st.thm.markov-kakutani | 0.3308 | 0.4062 | 0.3917 | 0.4788 | 0.55 | implication-schema-transfer | finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family |
| st.lem.finite-family-common-fixed-point | st.thm.markov-kakutani | 0.34 | 0.4812 | 0.4685 | 0.6457 | 0.6667 | declared-dependency | finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family |
| st.def.compact-convex-set | st.lem.cesaro-averages | 0.34 | 0.3227 | 0.3222 | 0.2885 | 0.2727 | declared-dependency | nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset |
| st.lem.cesaro-averages | st.thm.markov-kakutani | 0.2975 | 0.2881 | 0.2511 | 0.2228 | 0.2 | method-transfer | nonempty-compact-convex-subset, compact-convex-set-definition, single-affine-self-map, compact-convex-subset |
| st.def.compact-convex-set | st.lem.single-map-fixed-point | 0.34 | 0.3127 | 0.2961 | 0.2169 | 0.1667 | declared-dependency | nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset |
| st.thm.markov-kakutani | st.ex.interval-commuting-projections | 0.34 | 0.6074 | 0.5888 | 0.7708 | 0.8667 | declared-dependency | finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family |
| st.lem.cesaro-averages | st.lem.single-map-fixed-point | 0.34 | 0.4676 | 0.4004 | 0.3605 | 0.2857 | declared-dependency | continuous-affine-self-map-on-compact-convex-set, nonempty-compact-convex-subset, compact-convex-set-definition, single-map-fixed-point |
| st.lem.commuting-preserves-fixed-point-subset | st.thm.markov-kakutani | 0.273 | 0.3702 | 0.3175 | 0.2676 | 0.2353 | method-transfer | commuting-affine-family-on-compact-convex-set, commuting-affine-family-definition, commuting-affine-self-map-family, single-affine-self-map |
| st.def.compact-convex-set | st.ex.interval-commuting-projections | 0.2618 | 0.3276 | 0.3133 | 0.2394 | 0.2 | definitional-expansion | nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset |
| st.prop.fixed-point-subset-structure | st.thm.markov-kakutani | 0.2605 | 0.4288 | 0.3564 | 0.2737 | 0.1905 | method-transfer | nonempty-compact-convex-subset, compact-convex-set-definition, single-affine-self-map, compact-convex-subset |
| st.def.compact-convex-set | st.prop.fixed-point-subset-structure | 0.2541 | 0.3059 | 0.2988 | 0.2842 | 0.25 | definitional-expansion | nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset |
| st.def.compact-convex-set | st.lem.commuting-preserves-fixed-point-subset | 0.2457 | 0.1658 | 0.1569 | 0.0446 | 0.0 | definitional-expansion | invariant-fixed-point-subset, affine-map-analysis, affine-self-map |
| st.def.compact-convex-set | st.lem.finite-family-common-fixed-point | 0.2445 | 0.1687 | 0.1575 | 0.0833 | 0.0 | definitional-expansion | finite-intersection-compactness, invariant-fixed-point-subset, affine-map-analysis, compactness-method |
| st.lem.single-map-fixed-point | st.lem.finite-family-common-fixed-point | 0.2441 | 0.3655 | 0.341 | 0.3737 | 0.4 | implication-schema-transfer | finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family |
| st.lem.single-map-fixed-point | st.ex.interval-commuting-projections | 0.241 | 0.4841 | 0.4512 | 0.4941 | 0.55 | implication-schema-transfer | finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family |
| st.lem.commuting-preserves-fixed-point-subset | st.lem.finite-family-common-fixed-point | 0.34 | 0.4293 | 0.3685 | 0.3325 | 0.2857 | declared-dependency | commuting-affine-family-on-compact-convex-set, commuting-affine-family-definition, commuting-affine-self-map-family, single-affine-self-map |
| st.lem.single-map-fixed-point | st.prop.fixed-point-subset-structure | 0.34 | 0.4378 | 0.385 | 0.3727 | 0.3333 | declared-dependency | single-map-fixed-point-implies-invariant-fixed-point-subset, single-affine-self-map-on-compact-convex-set, nonempty-compact-convex-fixed-point-subset, nonempty-compact-convex-subset |
| st.prop.fixed-point-subset-structure | st.lem.commuting-preserves-fixed-point-subset | 0.34 | 0.4508 | 0.3878 | 0.2937 | 0.2857 | declared-dependency | single-affine-self-map-on-compact-convex-set, invariant-fixed-point-subset-definition, invariant-fixed-point-subset, single-affine-self-map |
| st.lem.single-map-fixed-point | st.lem.commuting-preserves-fixed-point-subset | 0.2094 | 0.2555 | 0.2176 | 0.1444 | 0.1429 | potential-support | commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, single-affine-self-map |

## Abductive Loop Plan

### Round 1
- Objective: Prioritize intervention targets by graph influence and unresolved dependencies.
- Targets: st.lem.single-map-fixed-point, st.thm.markov-kakutani, st.prop.fixed-point-subset-structure, st.lem.finite-family-common-fixed-point, st.lem.cesaro-averages, st.ex.interval-commuting-projections
- Action: Run kb-abduce on each target to propose missing-premise hypotheses.

### Round 2
- Objective: Test high-value intra-component transfer links (fallback mode) as abductive support hypotheses.
- Candidate connections: st.def.compact-convex-set->st.thm.markov-kakutani (0.4027), st.lem.single-map-fixed-point->st.thm.markov-kakutani (0.3308), st.lem.finite-family-common-fixed-point->st.thm.markov-kakutani (0.34), st.def.compact-convex-set->st.lem.cesaro-averages (0.34), st.lem.cesaro-averages->st.thm.markov-kakutani (0.2975), st.def.compact-convex-set->st.lem.single-map-fixed-point (0.34)
- Action: Convert top links into conjectural dependencies and run kb-deduce for consequence checks.

### Round 3
- Objective: Refine and retain only hypotheses with best explanatory and deductive payoff.
- Action: Re-score interventions, drop contradicted links, and keep top surviving pathways.
