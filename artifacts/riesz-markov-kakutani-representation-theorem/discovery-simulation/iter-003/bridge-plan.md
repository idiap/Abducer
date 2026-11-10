# Essential Concept Bridge Plan

## Stats

- Input connection candidates: 46
- Bridge programs: 20
- Concept axes: 13

## Top Bridge Programs

| bridge_id | from_id | to_id | type | tier | score | expl | coh | concept | commit | concept_evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| bridge.007 | st.thm.positive-functional-implies-measure | st.thm.riesz-markov-kakutani | structural support bridge | B | 0.5145 | 0.5682 | 0.007 | 0.4874 | 1.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, topological-regularity-reconstruction, regular-borel-measure-on-lch-space |
| bridge.005 | st.def.positive-linear-functional | st.thm.riesz-markov-kakutani | structural support bridge | B | 0.508 | 0.4324 | 0.007 | 0.5771 | 1.0 | positive-functional-implies-regular-measure, compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, measure-representation-correspondence |
| bridge.002 | st.def.cc-space | st.thm.riesz-markov-kakutani | structural support bridge | B | 0.5037 | 0.4473 | 0.0071 | 0.366 | 1.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space |
| bridge.001 | st.def.cc-space | st.thm.positive-functional-implies-measure | structural support bridge | B | 0.5027 | 0.524 | 0.0071 | 0.3845 | 1.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positivity-to-sigma-additivity, positive-functional-definition |
| bridge.013 | st.prop.integration-defines-functional | st.thm.riesz-markov-kakutani | structural support bridge | B | 0.4997 | 0.4729 | 0.007 | 0.469 | 1.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, topological-regularity-reconstruction, regular-borel-measure-on-lch-space |
| bridge.003 | st.def.lch-space | st.thm.riesz-markov-kakutani | structural support bridge | B | 0.4945 | 0.4902 | 0.0071 | 0.2086 | 1.0 | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, compact-open-approximation |
| bridge.011 | st.lem.uniqueness-from-cc-separation | st.thm.riesz-markov-kakutani | OS-reconstruction bridge | B | 0.4938 | 0.5215 | 0.007 | 0.311 | 1.0 | compactly-supported-continuous-functions, topological-regularity-reconstruction, regular-borel-measure-on-lch-space, regular-borel-measure-definition |
| bridge.006 | st.def.positive-linear-functional | st.thm.positive-functional-implies-measure | structural support bridge | B | 0.4916 | 0.5941 | 0.007 | 0.3568 | 1.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positivity-to-sigma-additivity, positive-functional-definition |
| bridge.010 | st.def.lch-space | st.def.cc-space | structural support bridge | B | 0.4831 | 0.6782 | 0.007 | 0.334 | 1.0 | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, compact-open-approximation |
| bridge.009 | st.def.cc-space | st.def.positive-linear-functional | structural support bridge | B | 0.4812 | 0.6126 | 0.007 | 0.4258 | 1.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positivity-to-sigma-additivity, positive-functional-definition |
| bridge.016 | st.thm.riesz-markov-kakutani | st.cor.c0-dual-representation | structural support bridge | B | 0.4658 | 0.3595 | 0.007 | 0.2445 | 1.0 | topological-regularity-reconstruction, measure-representation-correspondence, regular-borel-measure-on-lch-space, regular-borel-measure-definition |
| bridge.012 | st.def.cc-space | st.lem.compact-open-approximation | structural support bridge | B | 0.4649 | 0.5882 | 0.007 | 0.264 | 1.0 | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, compact-open-approximation |
| bridge.008 | st.def.lch-space | st.lem.compact-open-approximation | structural support bridge | B | 0.4576 | 0.6115 | 0.007 | 0.4187 | 1.0 | compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, compact-open-approximation |
| bridge.004 | st.def.lch-space | st.thm.positive-functional-implies-measure | structural support bridge | B | 0.456 | 0.4329 | 0.0071 | 0.1461 | 1.0 | compactly-supported-continuous-functions, compact-open-approximation, regularity-reconstruction, measure-representation |
| bridge.019 | st.thm.riesz-markov-kakutani | st.ex.dirac-measure-evaluation | structural support bridge | B | 0.4558 | 0.3595 | 0.007 | 0.1189 | 1.0 | compactly-supported-continuous-functions, integration-representation, measure-representation, regular-Borel-measure |
| bridge.017 | st.lem.compact-open-approximation | st.thm.positive-functional-implies-measure | structural support bridge | C | 0.4496 | 0.4495 | 0.007 | 0.1189 | 1.0 | compactly-supported-continuous-functions, compact-open-approximation, regularity-reconstruction, cc-space-definition |
| bridge.015 | st.def.cc-space | st.prop.integration-defines-functional | structural support bridge | C | 0.4443 | 0.4028 | 0.007 | 0.3312 | 1.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positivity-to-sigma-additivity, positive-functional-definition |
| bridge.014 | st.def.cc-space | st.lem.uniqueness-from-cc-separation | OS-reconstruction bridge | C | 0.4286 | 0.4028 | 0.007 | 0.1349 | 1.0 | compactly-supported-continuous-functions, compact-open-approximation, measure-representation, regular-Borel-measure |
| bridge.018 | st.def.lch-space | st.prop.integration-defines-functional | structural support bridge | C | 0.4149 | 0.4262 | 0.007 | 0.1221 | 1.0 | compactly-supported-continuous-functions, regularity-reconstruction, measure-representation, regular-Borel-measure |
| bridge.022 | st.thm.positive-functional-implies-measure | st.prop.integration-defines-functional | structural support bridge | C | 0.4116 | 0.5941 | 0.0 | 0.6332 | 0.0 | compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, topological-regularity-reconstruction, regular-borel-measure-on-lch-space |

## Mathematical Commitments

### bridge.007 (st.thm.positive-functional-implies-measure -> st.thm.riesz-markov-kakutani)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, regular-borel-measure-representation, regular-borel-measure-on-lch-space, functional-measure-correspondence, regular-borel-measure-definition

### bridge.005 (st.def.positive-linear-functional -> st.thm.riesz-markov-kakutani)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction
- Invariant basis: positive-functional-implies-regular-measure, compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, measure-representation-correspondence, riesz-markov-kakutani-correspondence, regular-borel-measure-representation

### bridge.002 (st.def.cc-space -> st.thm.riesz-markov-kakutani)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: compact-open-approximation + positivity-to-sigma-additivity + topological-regularity-reconstruction
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, regular-borel-measure-representation, locally-compact-hausdorff-definition, regular-borel-measure-on-lch-space, functional-measure-correspondence

### bridge.001 (st.def.cc-space -> st.thm.positive-functional-implies-measure)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: positive-linear-functional-on-cc-space
- Preserved invariant: compact-open regularity control in compactly-supported-continuous-functions
- Barrier scope: barrier + compact-open-approximation + positivity-to-sigma-additivity
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-definition, positive-linear-functional, positive-functional-model

### bridge.013 (st.prop.integration-defines-functional -> st.thm.riesz-markov-kakutani)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: positivity-to-sigma-additivity + topological-regularity-reconstruction
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, regular-borel-measure-representation, regular-borel-measure-on-lch-space, functional-measure-correspondence, regular-borel-measure-definition

### bridge.003 (st.def.lch-space -> st.thm.riesz-markov-kakutani)
- Antecedent schema: locally-compact-hausdorff-definition
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: compact-open-approximation + topological-regularity-reconstruction
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, regular-borel-measure-representation, locally-compact-hausdorff-definition, regular-borel-measure-on-lch-space, functional-measure-correspondence

### bridge.011 (st.lem.uniqueness-from-cc-separation -> st.thm.riesz-markov-kakutani)
- Antecedent schema: compact-open-approximation-on-lch-space
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: barrier + compact-open-approximation + topological-regularity-reconstruction
- Invariant basis: compactly-supported-continuous-functions, compact-open-approximation-on-lch-space, positive-linear-functional-on-cc-space, regular-borel-measure-representation, regular-borel-measure-on-lch-space, functional-measure-correspondence

### bridge.006 (st.def.positive-linear-functional -> st.thm.positive-functional-implies-measure)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: positive-linear-functional-on-cc-space
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-definition, positive-linear-functional, positive-functional-model

### bridge.010 (st.def.lch-space -> st.def.cc-space)
- Antecedent schema: locally-compact-hausdorff-definition
- Target consequence: positive-linear-functional-on-cc-space
- Preserved invariant: compact-open regularity control in compactly-supported-continuous-functions
- Barrier scope: compact-open-approximation + positivity-to-sigma-additivity
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, regular-Borel-measure, cc-space-definition

### bridge.009 (st.def.cc-space -> st.def.positive-linear-functional)
- Antecedent schema: positive-linear-functional-on-cc-space
- Target consequence: regular-borel-measure-representation
- Preserved invariant: regular-Borel representation in compactly-supported-continuous-functions
- Barrier scope: barrier + compact-open-approximation + positivity-to-sigma-additivity
- Invariant basis: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, regular-borel-measure-representation, functional-measure-correspondence, positive-functional-definition, unique-representing-measure

## Bridge Axes

### measure-construction -> riesz-markov-kakutani-correspondence
- Count: 1
- bridge.007: st.thm.positive-functional-implies-measure -> st.thm.riesz-markov-kakutani (score=0.5145)

### foundational-definitions -> riesz-markov-kakutani-correspondence
- Count: 3
- bridge.005: st.def.positive-linear-functional -> st.thm.riesz-markov-kakutani (score=0.508)
- bridge.002: st.def.cc-space -> st.thm.riesz-markov-kakutani (score=0.5037)
- bridge.003: st.def.lch-space -> st.thm.riesz-markov-kakutani (score=0.4945)

### foundational-definitions -> measure-construction
- Count: 3
- bridge.001: st.def.cc-space -> st.thm.positive-functional-implies-measure (score=0.5027)
- bridge.006: st.def.positive-linear-functional -> st.thm.positive-functional-implies-measure (score=0.4916)
- bridge.004: st.def.lch-space -> st.thm.positive-functional-implies-measure (score=0.456)

### measure-to-functional -> riesz-markov-kakutani-correspondence
- Count: 1
- bridge.013: st.prop.integration-defines-functional -> st.thm.riesz-markov-kakutani (score=0.4997)

### regularity-reconstruction -> riesz-markov-kakutani-correspondence
- Count: 1
- bridge.011: st.lem.uniqueness-from-cc-separation -> st.thm.riesz-markov-kakutani (score=0.4938)

### foundational-definitions -> foundational-definitions
- Count: 2
- bridge.010: st.def.lch-space -> st.def.cc-space (score=0.4831)
- bridge.009: st.def.cc-space -> st.def.positive-linear-functional (score=0.4812)

### riesz-markov-kakutani-correspondence -> duality-extension
- Count: 1
- bridge.016: st.thm.riesz-markov-kakutani -> st.cor.c0-dual-representation (score=0.4658)

### foundational-definitions -> topological-approximation
- Count: 2
- bridge.012: st.def.cc-space -> st.lem.compact-open-approximation (score=0.4649)
- bridge.008: st.def.lch-space -> st.lem.compact-open-approximation (score=0.4576)

### riesz-markov-kakutani-correspondence -> canonical-examples
- Count: 1
- bridge.019: st.thm.riesz-markov-kakutani -> st.ex.dirac-measure-evaluation (score=0.4558)

### topological-approximation -> measure-construction
- Count: 1
- bridge.017: st.lem.compact-open-approximation -> st.thm.positive-functional-implies-measure (score=0.4496)

### foundational-definitions -> measure-to-functional
- Count: 2
- bridge.015: st.def.cc-space -> st.prop.integration-defines-functional (score=0.4443)
- bridge.018: st.def.lch-space -> st.prop.integration-defines-functional (score=0.4149)

### foundational-definitions -> regularity-reconstruction
- Count: 1
- bridge.014: st.def.cc-space -> st.lem.uniqueness-from-cc-separation (score=0.4286)

### measure-construction -> measure-to-functional
- Count: 1
- bridge.022: st.thm.positive-functional-implies-measure -> st.prop.integration-defines-functional (score=0.4116)

## Recommended Run Order

1. bridge.007
2. bridge.005
3. bridge.002
4. bridge.001
5. bridge.013
6. bridge.003
