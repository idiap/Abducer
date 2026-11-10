# Conceptual Entry Points

## Stats

- Statements analyzed: 14
- Ranked entry points: 14
- Connector interventions used: 14
- Connector links used: 40
- Proof hypotheses used: 44
- Coherence signals used: 44

## Top Entry Points

| rank | statement_id | kind | phase | entry_score | concepts | hyp_count | bridge_count |
|---|---|---|---|---|---|---|---|
| 1 | st.thm.hille-yosida-general | theorem | Current Bridge Agenda | 0.8 | equivalence-schema, local-hypothesis-bundle, equivalence, group-theoretic-structure | 10 | 10 |
| 2 | st.def.c0-semigroup | definition | Current Bridge Agenda | 0.6886 | group-theoretic-structure, operator-theoretic-model, laplace-transform | 14 | 12 |
| 3 | st.def.generator | definition | Current Bridge Agenda | 0.6664 | group-theoretic-structure, laplace-transform | 14 | 11 |
| 4 | st.thm.cauchy-problem-equivalence | theorem | Current Bridge Agenda | 0.5455 | unconditional, equivalence, group-theoretic-structure, operator-theoretic-model | 7 | 7 |
| 5 | st.thm.hille-yosida-contraction | theorem | Current Bridge Agenda | 0.5321 | equivalence-schema, unconditional, equivalence, group-theoretic-structure | 9 | 6 |
| 6 | st.thm.lumer-phillips | theorem | Current Bridge Agenda | 0.4888 | equivalence-schema, unconditional, equivalence, group-theoretic-structure | 5 | 6 |
| 7 | st.def.resolvent | definition | Foundational Gauge-Theoretic Definitions | 0.4509 | operator-theoretic-model, resolvent-estimate | 5 | 7 |
| 8 | st.prop.generator-closed-dense | proposition | Additional KB-Specific Phases | 0.3757 | group-theoretic-structure, laplace-transform, barrier, domain-regularity | 4 | 3 |
| 9 | st.ex.translation-semigroup | example | Additional KB-Specific Phases | 0.3635 | equivalence-schema, equivalence, group-theoretic-structure, laplace-transform | 3 | 4 |
| 10 | st.der.yosida-approximation | derived-construction | Additional KB-Specific Phases | 0.3215 | equivalence, group-theoretic-structure, operator-theoretic-model, resolvent-estimate | 1 | 4 |
| 11 | st.ex.multiplication-semigroup | example | Additional KB-Specific Phases | 0.3145 | group-theoretic-structure, operator-theoretic-model, resolvent-estimate | 2 | 4 |
| 12 | st.ex.heat-semigroup-lp | example | Additional KB-Specific Phases | 0.3039 | group-theoretic-structure, laplace-transform, resolvent-estimate, barrier | 2 | 3 |
| 13 | st.der.contraction-resolvent-monotonicity | corollary | Constructive Models and Rigorous Existence Results | 0.1535 | unconditional, group-theoretic-structure | 0 | 2 |
| 14 | st.der.generator-uniqueness | corollary | Constructive Models and Rigorous Existence Results | 0.1407 | unconditional, group-theoretic-structure | 0 | 1 |

## Concept Tracks

### Current Bridge Agenda
- `st.thm.hille-yosida-general` (theorem), score=0.8
- `st.def.c0-semigroup` (definition), score=0.6886
- `st.def.generator` (definition), score=0.6664

### Foundational Gauge-Theoretic Definitions
- `st.def.resolvent` (definition), score=0.4509

### Additional KB-Specific Phases
- `st.prop.generator-closed-dense` (proposition), score=0.3757
- `st.ex.translation-semigroup` (example), score=0.3635
- `st.der.yosida-approximation` (derived-construction), score=0.3215

### Constructive Models and Rigorous Existence Results
- `st.der.contraction-resolvent-monotonicity` (corollary), score=0.1535
- `st.der.generator-uniqueness` (corollary), score=0.1407

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
