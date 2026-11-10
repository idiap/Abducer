# Essential Concept Bridge Plan

## Stats

- Input connection candidates: 28
- Bridge programs: 20
- Concept axes: 20

## Top Bridge Programs

| bridge_id | from_id | to_id | type | tier | score | expl | coh | concept | commit | concept_evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| bridge.007 | st.thm.markov-kakutani | st.ex.interval-commuting-projections | structural support bridge | B | 0.5306 | 0.5888 | 0.0088 | 0.7708 | 1.0 | finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family |
| bridge.001 | st.def.compact-convex-set | st.thm.markov-kakutani | structural support bridge | B | 0.5094 | 0.5602 | 0.0089 | 0.2795 | 1.0 | locally-convex-topological-vector-space, topological-vector-space-analysis, finite-intersection-compactness, nonempty-compact-convex-subset |
| bridge.003 | st.lem.finite-family-common-fixed-point | st.thm.markov-kakutani | structural support bridge | B | 0.509 | 0.5056 | 0.0088 | 0.6457 | 1.0 | finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family |
| bridge.008 | st.lem.cesaro-averages | st.lem.single-map-fixed-point | structural support bridge | B | 0.4917 | 0.6666 | 0.0088 | 0.3605 | 1.0 | continuous-affine-self-map-on-compact-convex-set, single-map-fixed-point-extraction, nonempty-compact-convex-subset, compact-convex-set-definition |
| bridge.006 | st.def.compact-convex-set | st.lem.single-map-fixed-point | structural support bridge | B | 0.4769 | 0.6432 | 0.0088 | 0.2169 | 1.0 | finite-intersection-compactness, nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset |
| bridge.002 | st.lem.single-map-fixed-point | st.thm.markov-kakutani | structural support bridge | B | 0.4764 | 0.3917 | 0.0088 | 0.4788 | 1.0 | finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family |
| bridge.004 | st.def.compact-convex-set | st.lem.cesaro-averages | structural support bridge | B | 0.4592 | 0.6485 | 0.0088 | 0.2885 | 1.0 | nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset, affine-map-analysis |
| bridge.016 | st.lem.single-map-fixed-point | st.ex.interval-commuting-projections | structural support bridge | C | 0.4373 | 0.4512 | 0.0086 | 0.4941 | 1.0 | finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family |
| bridge.011 | st.prop.fixed-point-subset-structure | st.thm.markov-kakutani | structural support bridge | C | 0.4303 | 0.3564 | 0.0086 | 0.2737 | 1.0 | finite-intersection-compactness, nonempty-compact-convex-subset, compact-convex-set-definition, invariant-subset-propagation |
| bridge.009 | st.lem.commuting-preserves-fixed-point-subset | st.thm.markov-kakutani | structural support bridge | C | 0.4288 | 0.3175 | 0.0087 | 0.2676 | 1.0 | commuting-affine-family-on-compact-convex-set, commuting-affine-family-definition, commuting-affine-self-map-family, invariant-subset-propagation |
| bridge.005 | st.lem.cesaro-averages | st.thm.markov-kakutani | structural support bridge | C | 0.4245 | 0.2511 | 0.0087 | 0.2228 | 1.0 | nonempty-compact-convex-subset, compact-convex-set-definition, single-affine-self-map, compact-convex-subset |
| bridge.015 | st.lem.single-map-fixed-point | st.lem.finite-family-common-fixed-point | structural support bridge | C | 0.4141 | 0.341 | 0.0086 | 0.3737 | 1.0 | finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family |
| bridge.012 | st.def.compact-convex-set | st.prop.fixed-point-subset-structure | structural support bridge | C | 0.3814 | 0.3053 | 0.0086 | 0.2842 | 1.0 | finite-intersection-compactness, nonempty-compact-convex-subset, compact-convex-set-definition, invariant-fixed-point-subset |
| bridge.014 | st.def.compact-convex-set | st.lem.finite-family-common-fixed-point | structural support bridge | C | 0.3763 | 0.2431 | 0.0086 | 0.0833 | 1.0 | finite-intersection-compactness, invariant-fixed-point-subset, affine-map-analysis, compactness-method |
| bridge.010 | st.def.compact-convex-set | st.ex.interval-commuting-projections | structural support bridge | C | 0.3695 | 0.3133 | 0.0086 | 0.2394 | 1.0 | finite-intersection-compactness, nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset |
| bridge.018 | st.lem.single-map-fixed-point | st.prop.fixed-point-subset-structure | structural support bridge | C | 0.3599 | 0.385 | 0.0 | 0.3727 | 0.0 | single-map-fixed-point-implies-invariant-fixed-point-subset, single-affine-self-map-on-compact-convex-set, nonempty-compact-convex-fixed-point-subset, finite-intersection-compactness |
| bridge.017 | st.lem.commuting-preserves-fixed-point-subset | st.lem.finite-family-common-fixed-point | structural support bridge | C | 0.3541 | 0.3685 | 0.0 | 0.3325 | 0.0 | commuting-affine-family-on-compact-convex-set, commuting-affine-family-definition, commuting-affine-self-map-family, invariant-subset-propagation |
| bridge.025 | st.lem.finite-family-common-fixed-point | st.ex.interval-commuting-projections | structural support bridge | C | 0.3465 | 0.4429 | 0.0 | 0.6063 | 0.0 | finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family |
| bridge.013 | st.def.compact-convex-set | st.lem.commuting-preserves-fixed-point-subset | structural support bridge | C | 0.3425 | 0.2723 | 0.0086 | 0.0446 | 1.0 | invariant-fixed-point-subset, affine-map-analysis, affine-self-map |
| bridge.019 | st.prop.fixed-point-subset-structure | st.lem.commuting-preserves-fixed-point-subset | structural support bridge | C | 0.3306 | 0.3878 | 0.0 | 0.2937 | 0.0 | single-affine-self-map-on-compact-convex-set, invariant-fixed-point-subset-definition, invariant-subset-propagation, invariant-fixed-point-subset |

## Mathematical Commitments

### bridge.007 (st.thm.markov-kakutani -> st.ex.interval-commuting-projections)
- Antecedent schema: commuting-affine-family-on-compact-convex-set
- Target consequence: common-fixed-point-for-finite-commuting-family
- Preserved invariant: finite-intersection lift in common-fixed-point-correspondence
- Barrier scope: barrier + finite-intersection-compactness + invariant-subset-propagation
- Invariant basis: finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family, markov-kakutani-common-fixed-point, commuting-affine-family-definition

### bridge.001 (st.def.compact-convex-set -> st.thm.markov-kakutani)
- Antecedent schema: nonempty-compact-convex-subset
- Target consequence: common-fixed-point-for-finite-commuting-family
- Preserved invariant: nonempty compact-convex fixed-point subset in locally-convex-topological-vector-space
- Barrier scope: barrier + finite-intersection-compactness + invariant-subset-propagation
- Invariant basis: common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, locally-convex-topological-vector-space, common-fixed-point-for-commuting-family, nonempty-compact-convex-subset, compact-convex-set-definition

### bridge.003 (st.lem.finite-family-common-fixed-point -> st.thm.markov-kakutani)
- Antecedent schema: commuting-affine-family-on-compact-convex-set
- Target consequence: common-fixed-point-for-finite-commuting-family
- Preserved invariant: finite-intersection lift in common-fixed-point-correspondence
- Barrier scope: barrier + finite-intersection-compactness + invariant-subset-propagation
- Invariant basis: finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family, markov-kakutani-common-fixed-point, commuting-affine-family-definition

### bridge.008 (st.lem.cesaro-averages -> st.lem.single-map-fixed-point)
- Antecedent schema: continuous-affine-self-map-on-compact-convex-set
- Target consequence: common-fixed-point-for-finite-commuting-family
- Preserved invariant: averaged affine orbit stabilization in single-affine-self-map
- Barrier scope: barrier + finite-intersection-compactness + single-map-fixed-point-extraction
- Invariant basis: continuous-affine-self-map-on-compact-convex-set, common-fixed-point-for-finite-commuting-family, nonempty-compact-convex-fixed-point-subset, common-fixed-point-for-commuting-family, nonempty-compact-convex-subset, compact-convex-set-definition

### bridge.006 (st.def.compact-convex-set -> st.lem.single-map-fixed-point)
- Antecedent schema: nonempty-compact-convex-subset
- Target consequence: common-fixed-point-for-finite-commuting-family
- Preserved invariant: nonempty compact-convex fixed-point subset in compact-convex-subset
- Barrier scope: barrier + finite-intersection-compactness + single-map-fixed-point-extraction
- Invariant basis: common-fixed-point-for-finite-commuting-family, nonempty-compact-convex-fixed-point-subset, common-fixed-point-for-commuting-family, nonempty-compact-convex-subset, compact-convex-set-definition, single-map-fixed-point

### bridge.002 (st.lem.single-map-fixed-point -> st.thm.markov-kakutani)
- Antecedent schema: continuous-affine-self-map-on-compact-convex-set
- Target consequence: common-fixed-point-for-finite-commuting-family
- Preserved invariant: nonempty compact-convex fixed-point subset in common-fixed-point-correspondence
- Barrier scope: barrier + finite-intersection-compactness + invariant-subset-propagation
- Invariant basis: finite-intersection-property-implies-common-fixed-point, continuous-affine-self-map-on-compact-convex-set, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, common-fixed-point-for-commuting-family

### bridge.004 (st.def.compact-convex-set -> st.lem.cesaro-averages)
- Antecedent schema: nonempty-compact-convex-subset
- Target consequence: single-map-fixed-point
- Preserved invariant: averaged affine orbit stabilization in compact-convex-subset
- Barrier scope: barrier + finite-intersection-compactness + single-map-fixed-point-extraction
- Invariant basis: affine-orbit-averages-in-compact-convex-set, nonempty-compact-convex-subset, compact-convex-set-definition, single-map-fixed-point, compact-convex-subset, compact-convex-set

### bridge.016 (st.lem.single-map-fixed-point -> st.ex.interval-commuting-projections)
- Antecedent schema: continuous-affine-self-map-on-compact-convex-set
- Target consequence: common-fixed-point-for-finite-commuting-family
- Preserved invariant: nonempty compact-convex fixed-point subset in common-fixed-point-correspondence
- Barrier scope: barrier + finite-intersection-compactness + single-map-fixed-point-extraction
- Invariant basis: finite-intersection-property-implies-common-fixed-point, continuous-affine-self-map-on-compact-convex-set, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, common-fixed-point-for-commuting-family

### bridge.011 (st.prop.fixed-point-subset-structure -> st.thm.markov-kakutani)
- Antecedent schema: single-affine-self-map-on-compact-convex-set
- Target consequence: common-fixed-point-for-finite-commuting-family
- Preserved invariant: nonempty compact-convex fixed-point subset in single-affine-self-map
- Barrier scope: barrier + finite-intersection-compactness + invariant-subset-propagation
- Invariant basis: common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, single-affine-self-map-with-fixed-point, common-fixed-point-for-commuting-family, nonempty-compact-convex-subset

### bridge.009 (st.lem.commuting-preserves-fixed-point-subset -> st.thm.markov-kakutani)
- Antecedent schema: commuting-affine-family-on-compact-convex-set
- Target consequence: common-fixed-point-for-finite-commuting-family
- Preserved invariant: nonempty compact-convex fixed-point subset in commuting-affine-self-map-family
- Barrier scope: barrier + finite-intersection-compactness + invariant-subset-propagation
- Invariant basis: common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, common-fixed-point-for-commuting-family, commuting-affine-family-definition, commuting-affine-self-map-family

## Bridge Axes

### common-fixed-point-theorem -> examples-and-interpretation
- Count: 1
- bridge.007: st.thm.markov-kakutani -> st.ex.interval-commuting-projections (score=0.5306)

### foundational-definitions -> common-fixed-point-theorem
- Count: 1
- bridge.001: st.def.compact-convex-set -> st.thm.markov-kakutani (score=0.5094)

### finite-family-lift -> common-fixed-point-theorem
- Count: 1
- bridge.003: st.lem.finite-family-common-fixed-point -> st.thm.markov-kakutani (score=0.509)

### affine-averaging -> single-map-fixed-point
- Count: 1
- bridge.008: st.lem.cesaro-averages -> st.lem.single-map-fixed-point (score=0.4917)

### foundational-definitions -> single-map-fixed-point
- Count: 1
- bridge.006: st.def.compact-convex-set -> st.lem.single-map-fixed-point (score=0.4769)

### single-map-fixed-point -> common-fixed-point-theorem
- Count: 1
- bridge.002: st.lem.single-map-fixed-point -> st.thm.markov-kakutani (score=0.4764)

### foundational-definitions -> affine-averaging
- Count: 1
- bridge.004: st.def.compact-convex-set -> st.lem.cesaro-averages (score=0.4592)

### single-map-fixed-point -> examples-and-interpretation
- Count: 1
- bridge.016: st.lem.single-map-fixed-point -> st.ex.interval-commuting-projections (score=0.4373)

### invariant-fixed-point-subset -> common-fixed-point-theorem
- Count: 1
- bridge.011: st.prop.fixed-point-subset-structure -> st.thm.markov-kakutani (score=0.4303)

### commuting-invariance -> common-fixed-point-theorem
- Count: 1
- bridge.009: st.lem.commuting-preserves-fixed-point-subset -> st.thm.markov-kakutani (score=0.4288)

### affine-averaging -> common-fixed-point-theorem
- Count: 1
- bridge.005: st.lem.cesaro-averages -> st.thm.markov-kakutani (score=0.4245)

### single-map-fixed-point -> finite-family-lift
- Count: 1
- bridge.015: st.lem.single-map-fixed-point -> st.lem.finite-family-common-fixed-point (score=0.4141)

### foundational-definitions -> invariant-fixed-point-subset
- Count: 1
- bridge.012: st.def.compact-convex-set -> st.prop.fixed-point-subset-structure (score=0.3814)

### foundational-definitions -> finite-family-lift
- Count: 1
- bridge.014: st.def.compact-convex-set -> st.lem.finite-family-common-fixed-point (score=0.3763)

### foundational-definitions -> examples-and-interpretation
- Count: 1
- bridge.010: st.def.compact-convex-set -> st.ex.interval-commuting-projections (score=0.3695)

### single-map-fixed-point -> invariant-fixed-point-subset
- Count: 1
- bridge.018: st.lem.single-map-fixed-point -> st.prop.fixed-point-subset-structure (score=0.3599)

### commuting-invariance -> finite-family-lift
- Count: 1
- bridge.017: st.lem.commuting-preserves-fixed-point-subset -> st.lem.finite-family-common-fixed-point (score=0.3541)

### finite-family-lift -> examples-and-interpretation
- Count: 1
- bridge.025: st.lem.finite-family-common-fixed-point -> st.ex.interval-commuting-projections (score=0.3465)

### foundational-definitions -> commuting-invariance
- Count: 1
- bridge.013: st.def.compact-convex-set -> st.lem.commuting-preserves-fixed-point-subset (score=0.3425)

### invariant-fixed-point-subset -> commuting-invariance
- Count: 1
- bridge.019: st.prop.fixed-point-subset-structure -> st.lem.commuting-preserves-fixed-point-subset (score=0.3306)

## Recommended Run Order

1. bridge.007
2. bridge.001
3. bridge.003
4. bridge.008
5. bridge.006
6. bridge.002
