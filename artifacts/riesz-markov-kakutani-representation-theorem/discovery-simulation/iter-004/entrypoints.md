# Conceptual Entry Points

## Stats

- Statements analyzed: 10
- Ranked entry points: 10
- Connector interventions used: 10
- Connector links used: 40
- Proof hypotheses used: 58
- Coherence signals used: 58

## Top Entry Points

| rank | statement_id | kind | phase | entry_score | concepts | hyp_count | bridge_count |
|---|---|---|---|---|---|---|---|
| 1 | st.thm.riesz-markov-kakutani | theorem | Current Bridge Agenda | 0.8583 | positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-representation | 17 | 9 |
| 2 | st.thm.positive-functional-implies-measure | theorem | Current Bridge Agenda | 0.7761 | positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-definition, positive-functional-definition | 14 | 9 |
| 3 | st.def.cc-space | definition | Current Bridge Agenda | 0.7032 | positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition | 16 | 9 |
| 4 | st.def.positive-linear-functional | definition | Current Bridge Agenda | 0.635 | positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-representation, functional-measure-correspondence | 8 | 9 |
| 5 | st.prop.integration-defines-functional | proposition | Current Bridge Agenda | 0.6315 | regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration | 9 | 7 |
| 6 | st.lem.uniqueness-from-cc-separation | lemma | Current Bridge Agenda | 0.6112 | function-separation-implies-measure-uniqueness, compact-open-approximation-on-lch-space, regular-borel-measure-on-lch-space, unique-representing-measure | 8 | 9 |
| 7 | st.def.lch-space | definition | Foundational Gauge-Theoretic Definitions | 0.582 | locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space | 15 | 9 |
| 8 | st.lem.compact-open-approximation | lemma | Additional KB-Specific Phases | 0.5802 | compact-open-approximation-supports-regularity, compact-open-approximation-on-lch-space, compact-open-regularity-witness, locally-compact-hausdorff-definition | 9 | 7 |
| 9 | st.cor.c0-dual-representation | corollary | Additional KB-Specific Phases | 0.5711 | c0-dual-implies-signed-regular-measure, total-variation-equals-dual-norm, regular-borel-measure-on-lch-space, continuous-linear-functional-on-c0 | 6 | 6 |
| 10 | st.ex.dirac-measure-evaluation | example | Additional KB-Specific Phases | 0.3272 | dirac-evaluation-example, cc-space-definition, compactly-supported-continuous-functions, C_c-space | 4 | 6 |

## Concept Tracks

### Current Bridge Agenda
- `st.thm.riesz-markov-kakutani` (theorem), score=0.8583
- `st.thm.positive-functional-implies-measure` (theorem), score=0.7761
- `st.def.cc-space` (definition), score=0.7032

### Foundational Gauge-Theoretic Definitions
- `st.def.lch-space` (definition), score=0.582

### Additional KB-Specific Phases
- `st.lem.compact-open-approximation` (lemma), score=0.5802
- `st.cor.c0-dual-representation` (corollary), score=0.5711
- `st.ex.dirac-measure-evaluation` (example), score=0.3272

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
