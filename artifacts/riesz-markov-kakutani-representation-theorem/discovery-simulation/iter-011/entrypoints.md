# Conceptual Entry Points

## Stats

- Statements analyzed: 10
- Ranked entry points: 10
- Connector interventions used: 10
- Connector links used: 40
- Proof hypotheses used: 42
- Coherence signals used: 42

## Top Entry Points

| rank | statement_id | kind | phase | entry_score | concepts | hyp_count | bridge_count |
|---|---|---|---|---|---|---|---|
| 1 | st.thm.positive-functional-implies-measure | theorem | Current Bridge Agenda | 0.7838 | regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration | 14 | 9 |
| 2 | st.thm.riesz-markov-kakutani | theorem | Current Bridge Agenda | 0.7549 | regular-measure-implies-positive-functional, positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space | 11 | 9 |
| 3 | st.def.cc-space | definition | Current Bridge Agenda | 0.6955 | positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition | 12 | 9 |
| 4 | st.prop.integration-defines-functional | proposition | Current Bridge Agenda | 0.6175 | regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration | 5 | 8 |
| 5 | st.lem.uniqueness-from-cc-separation | lemma | Current Bridge Agenda | 0.6099 | regular-measure-implies-positive-functional, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional | 6 | 9 |
| 6 | st.def.positive-linear-functional | definition | Current Bridge Agenda | 0.605 | positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-representation, functional-measure-correspondence | 7 | 8 |
| 7 | st.def.lch-space | definition | Foundational Gauge-Theoretic Definitions | 0.5702 | locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space | 11 | 9 |
| 8 | st.cor.c0-dual-representation | corollary | Additional KB-Specific Phases | 0.5275 | regular-measure-implies-positive-functional, c0-dual-implies-signed-regular-measure, total-variation-equals-dual-norm, regular-borel-measure-on-lch-space | 3 | 7 |
| 9 | st.lem.compact-open-approximation | lemma | Additional KB-Specific Phases | 0.47 | unconditional, locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions | 4 | 6 |
| 10 | st.ex.dirac-measure-evaluation | example | Additional KB-Specific Phases | 0.3585 | regular-measure-implies-positive-functional, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional | 1 | 6 |

## Concept Tracks

### Current Bridge Agenda
- `st.thm.positive-functional-implies-measure` (theorem), score=0.7838
- `st.thm.riesz-markov-kakutani` (theorem), score=0.7549
- `st.def.cc-space` (definition), score=0.6955

### Foundational Gauge-Theoretic Definitions
- `st.def.lch-space` (definition), score=0.5702

### Additional KB-Specific Phases
- `st.cor.c0-dual-representation` (corollary), score=0.5275
- `st.lem.compact-open-approximation` (lemma), score=0.47
- `st.ex.dirac-measure-evaluation` (example), score=0.3585

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
