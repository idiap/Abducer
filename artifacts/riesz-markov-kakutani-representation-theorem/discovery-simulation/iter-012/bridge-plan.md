# Essential Concept Bridge Plan

## Stats

- Input connection candidates: 40
- Bridge programs: 20
- Concept axes: 11

## Top Bridge Programs

| bridge_id | from_id | to_id | type | tier | score | expl | coh | concept | commit | concept_evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| bridge.006 | st.prop.integration-defines-functional | st.thm.positive-functional-implies-measure | structural support bridge | B | 0.55 | 0.6872 | 0.0081 | 0.8727 | 1.0 | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-linear-functional-on-cc-space |
| bridge.004 | st.lem.uniqueness-from-cc-separation | st.thm.positive-functional-implies-measure | structural support bridge | B | 0.5192 | 0.578 | 0.0082 | 0.6525 | 1.0 | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, topological-regularity-reconstruction |
| bridge.009 | st.thm.positive-functional-implies-measure | st.thm.riesz-markov-kakutani | structural support bridge | B | 0.503 | 0.5344 | 0.0081 | 0.5897 | 1.0 | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-linear-functional-on-cc-space |
| bridge.001 | st.def.cc-space | st.thm.positive-functional-implies-measure | structural support bridge | B | 0.4989 | 0.5191 | 0.0082 | 0.3492 | 1.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positivity-to-sigma-additivity, positive-functional-definition |
| bridge.008 | st.def.positive-linear-functional | st.thm.positive-functional-implies-measure | structural support bridge | B | 0.4878 | 0.5713 | 0.0081 | 0.335 | 1.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positivity-to-sigma-additivity, positive-functional-definition |
| bridge.014 | st.prop.integration-defines-functional | st.thm.riesz-markov-kakutani | structural support bridge | B | 0.4776 | 0.5258 | 0.008 | 0.5966 | 1.0 | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-linear-functional-on-cc-space |
| bridge.002 | st.def.cc-space | st.thm.riesz-markov-kakutani | structural support bridge | B | 0.4762 | 0.4442 | 0.0082 | 0.3443 | 1.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space |
| bridge.003 | st.def.lch-space | st.thm.riesz-markov-kakutani | structural support bridge | B | 0.4689 | 0.4885 | 0.0082 | 0.1963 | 1.0 | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, compact-open-approximation |
| bridge.010 | st.def.positive-linear-functional | st.thm.riesz-markov-kakutani | structural support bridge | B | 0.4647 | 0.3904 | 0.0081 | 0.4653 | 1.0 | positive-functional-implies-regular-measure, compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, measure-representation-correspondence |
| bridge.005 | st.def.lch-space | st.thm.positive-functional-implies-measure | structural support bridge | B | 0.4569 | 0.4311 | 0.0082 | 0.1368 | 1.0 | compactly-supported-continuous-functions, compact-open-approximation, regularity-reconstruction, measure-representation |
| bridge.007 | st.def.lch-space | st.lem.compact-open-approximation | structural support bridge | B | 0.453 | 0.5927 | 0.0081 | 0.48 | 1.0 | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, compact-open-approximation |
| bridge.013 | st.lem.uniqueness-from-cc-separation | st.thm.riesz-markov-kakutani | structural support bridge | B | 0.4509 | 0.4172 | 0.008 | 0.4315 | 1.0 | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, topological-regularity-reconstruction |
| bridge.011 | st.def.cc-space | st.def.positive-linear-functional | structural support bridge | C | 0.4496 | 0.4762 | 0.0081 | 0.4258 | 1.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positivity-to-sigma-additivity, positive-functional-definition |
| bridge.012 | st.def.lch-space | st.def.cc-space | structural support bridge | C | 0.4447 | 0.5004 | 0.0081 | 0.334 | 1.0 | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, compact-open-approximation |
| bridge.015 | st.def.cc-space | st.lem.compact-open-approximation | structural support bridge | C | 0.4258 | 0.4452 | 0.008 | 0.2944 | 1.0 | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, compact-open-approximation |
| bridge.016 | st.def.lch-space | st.lem.uniqueness-from-cc-separation | structural support bridge | C | 0.376 | 0.2958 | 0.008 | 0.1897 | 1.0 | compactly-supported-continuous-functions, compact-open-approximation, regularity-reconstruction, measure-representation |
| bridge.026 | st.prop.integration-defines-functional | st.lem.uniqueness-from-cc-separation | structural support bridge | C | 0.3424 | 0.5312 | 0.0 | 0.6421 | 0.0 | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, topological-regularity-reconstruction |
| bridge.017 | st.thm.positive-functional-implies-measure | st.cor.c0-dual-representation | structural support bridge | C | 0.3381 | 0.3189 | 0.0 | 0.3596 | 0.0 | regular-measure-implies-positive-functional, integration-defines-positive-functional, topological-regularity-reconstruction, positive-functional-via-integration |
| bridge.030 | st.thm.positive-functional-implies-measure | st.ex.dirac-measure-evaluation | structural support bridge | C | 0.3356 | 0.3394 | 0.0 | 0.4305 | 0.0 | regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-functional-via-integration |
| bridge.021 | st.thm.riesz-markov-kakutani | st.cor.c0-dual-representation | structural support bridge | C | 0.3239 | 0.3202 | 0.0 | 0.3149 | 0.0 | regular-measure-implies-positive-functional, integration-defines-positive-functional, topological-regularity-reconstruction, measure-representation-correspondence |

## Mathematical Commitments

### bridge.006 (st.prop.integration-defines-functional -> st.thm.positive-functional-implies-measure)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: positive-linear-functional-on-cc-space
- Preserved invariant: compact-open regularity control in compactly-supported-continuous-functions
- Barrier scope: barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction
- Invariant basis: regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-linear-functional-on-cc-space, positive-functional-via-integration, regular-borel-measure-on-lch-space

### bridge.004 (st.lem.uniqueness-from-cc-separation -> st.thm.positive-functional-implies-measure)
- Antecedent schema: regular-borel-measure-on-lch-space
- Target consequence: positive-linear-functional-on-cc-space
- Preserved invariant: compact-open regularity control in compactly-supported-continuous-functions
- Barrier scope: barrier + compact-open-approximation + positivity-to-sigma-additivity
- Invariant basis: regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-linear-functional-on-cc-space, positive-functional-via-integration, regular-borel-measure-on-lch-space

### bridge.009 (st.thm.positive-functional-implies-measure -> st.thm.riesz-markov-kakutani)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction
- Invariant basis: regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-representation, positive-functional-via-integration

### bridge.001 (st.def.cc-space -> st.thm.positive-functional-implies-measure)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: positive-linear-functional-on-cc-space
- Preserved invariant: compact-open regularity control in compactly-supported-continuous-functions
- Barrier scope: barrier + compact-open-approximation + positivity-to-sigma-additivity
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positive-functional-via-integration, regular-borel-measure-on-lch-space, positive-functional-definition, positive-linear-functional

### bridge.008 (st.def.positive-linear-functional -> st.thm.positive-functional-implies-measure)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: positive-linear-functional-on-cc-space
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positive-functional-via-integration, regular-borel-measure-on-lch-space, positive-functional-definition, positive-linear-functional

### bridge.014 (st.prop.integration-defines-functional -> st.thm.riesz-markov-kakutani)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: positivity-to-sigma-additivity + topological-regularity-reconstruction
- Invariant basis: regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-representation, positive-functional-via-integration

### bridge.002 (st.def.cc-space -> st.thm.riesz-markov-kakutani)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: compact-open-approximation + positivity-to-sigma-additivity + topological-regularity-reconstruction
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, regular-borel-measure-representation, locally-compact-hausdorff-definition, positive-functional-via-integration, regular-borel-measure-on-lch-space

### bridge.003 (st.def.lch-space -> st.thm.riesz-markov-kakutani)
- Antecedent schema: locally-compact-hausdorff-definition
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: compact-open-approximation + topological-regularity-reconstruction
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, regular-borel-measure-representation, locally-compact-hausdorff-definition, positive-functional-via-integration, regular-borel-measure-on-lch-space

### bridge.010 (st.def.positive-linear-functional -> st.thm.riesz-markov-kakutani)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction
- Invariant basis: positive-functional-implies-regular-measure, compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, measure-representation-correspondence, riesz-markov-kakutani-correspondence, regular-borel-measure-representation

### bridge.005 (st.def.lch-space -> st.thm.positive-functional-implies-measure)
- Antecedent schema: locally-compact-hausdorff-definition
- Target consequence: positive-linear-functional-on-cc-space
- Preserved invariant: compact-open regularity control in compactly-supported-continuous-functions
- Barrier scope: barrier + compact-open-approximation + positivity-to-sigma-additivity
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positive-functional-via-integration, regular-borel-measure-on-lch-space, regular-Borel-measure, cc-space-definition

## Bridge Axes

### measure-to-functional -> measure-construction
- Count: 2
- bridge.006: st.prop.integration-defines-functional -> st.thm.positive-functional-implies-measure (score=0.55)
- bridge.026: st.prop.integration-defines-functional -> st.lem.uniqueness-from-cc-separation (score=0.3424)

### measure-construction -> measure-construction
- Count: 1
- bridge.004: st.lem.uniqueness-from-cc-separation -> st.thm.positive-functional-implies-measure (score=0.5192)

### measure-construction -> riesz-markov-kakutani-correspondence
- Count: 2
- bridge.009: st.thm.positive-functional-implies-measure -> st.thm.riesz-markov-kakutani (score=0.503)
- bridge.013: st.lem.uniqueness-from-cc-separation -> st.thm.riesz-markov-kakutani (score=0.4509)

### foundational-definitions -> measure-construction
- Count: 4
- bridge.001: st.def.cc-space -> st.thm.positive-functional-implies-measure (score=0.4989)
- bridge.008: st.def.positive-linear-functional -> st.thm.positive-functional-implies-measure (score=0.4878)
- bridge.005: st.def.lch-space -> st.thm.positive-functional-implies-measure (score=0.4569)

### measure-to-functional -> riesz-markov-kakutani-correspondence
- Count: 1
- bridge.014: st.prop.integration-defines-functional -> st.thm.riesz-markov-kakutani (score=0.4776)

### foundational-definitions -> riesz-markov-kakutani-correspondence
- Count: 3
- bridge.002: st.def.cc-space -> st.thm.riesz-markov-kakutani (score=0.4762)
- bridge.003: st.def.lch-space -> st.thm.riesz-markov-kakutani (score=0.4689)
- bridge.010: st.def.positive-linear-functional -> st.thm.riesz-markov-kakutani (score=0.4647)

### foundational-definitions -> topological-approximation
- Count: 2
- bridge.007: st.def.lch-space -> st.lem.compact-open-approximation (score=0.453)
- bridge.015: st.def.cc-space -> st.lem.compact-open-approximation (score=0.4258)

### foundational-definitions -> foundational-definitions
- Count: 2
- bridge.011: st.def.cc-space -> st.def.positive-linear-functional (score=0.4496)
- bridge.012: st.def.lch-space -> st.def.cc-space (score=0.4447)

### measure-construction -> duality-extension
- Count: 1
- bridge.017: st.thm.positive-functional-implies-measure -> st.cor.c0-dual-representation (score=0.3381)

### measure-construction -> canonical-examples
- Count: 1
- bridge.030: st.thm.positive-functional-implies-measure -> st.ex.dirac-measure-evaluation (score=0.3356)

### riesz-markov-kakutani-correspondence -> duality-extension
- Count: 1
- bridge.021: st.thm.riesz-markov-kakutani -> st.cor.c0-dual-representation (score=0.3239)

## Recommended Run Order

1. bridge.006
2. bridge.004
3. bridge.009
4. bridge.001
5. bridge.008
6. bridge.014
