# Conceptual Entry Points

## Stats

- Statements analyzed: 14
- Ranked entry points: 14
- Connector interventions used: 14
- Connector links used: 60
- Proof hypotheses used: 44
- Coherence signals used: 44

## Top Entry Points

| rank | statement_id | kind | phase | entry_score | concepts | hyp_count | bridge_count |
|---|---|---|---|---|---|---|---|
| 1 | st.thm.hille-yosida-general | theorem | Current Bridge Agenda | 0.7908 | c0-generation-implies-closed-dense-generator, resolvent-approximants-converge-to-generated-semigroup, closed-dense-plus-resolvent-powers-imply-c0-generation, closed-dense-operator-with-resolvent-power-bounds | 11 | 11 |
| 2 | st.def.generator | definition | Current Bridge Agenda | 0.7278 | c0-semigroup-definition, generator-definition, C0-semigroup-model, operator-theoretic-Banach-space | 13 | 13 |
| 3 | st.def.c0-semigroup | definition | Current Bridge Agenda | 0.7041 | c0-semigroup-definition, C0-semigroup-model, operator-theoretic-Banach-space, Banach-space | 13 | 13 |
| 4 | st.thm.cauchy-problem-equivalence | theorem | Current Bridge Agenda | 0.6542 | c0-generation-iff-cauchy-well-posedness, closed-operator-or-semigroup-generator, well-posed-abstract-cauchy-problem, cauchy-problem-equivalence | 7 | 10 |
| 5 | st.thm.hille-yosida-contraction | theorem | Current Bridge Agenda | 0.6483 | c0-generation-implies-closed-dense-generator, closed-dense-plus-first-resolvent-bound-imply-contraction-generation, resolvent-approximants-converge-to-generated-semigroup, closed-dense-operator-with-first-resolvent-bound | 7 | 11 |
| 6 | st.thm.lumer-phillips | theorem | Additional KB-Specific Phases | 0.5674 | closed-dense-plus-first-resolvent-bound-imply-contraction-generation, dissipativity-plus-range-condition-imply-contraction-generation, densely-defined-dissipative-operator-with-surjective-shift, closed-dense-operator-with-first-resolvent-bound | 6 | 9 |
| 7 | st.def.resolvent | definition | Foundational Gauge-Theoretic Definitions | 0.5023 | resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme, yosida-approximation-convergence | 3 | 7 |
| 8 | st.der.yosida-approximation | derived-construction | Current Bridge Agenda | 0.4986 | resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, contraction-semigroup-generator, bounded-generator-approximation-scheme | 1 | 7 |
| 9 | st.prop.generator-closed-dense | proposition | Additional KB-Specific Phases | 0.4835 | c0-generation-implies-closed-dense-generator, generator-of-c0-semigroup, closed-densely-defined-generator, generator-closed-dense | 4 | 5 |
| 10 | st.ex.translation-semigroup | example | Additional KB-Specific Phases | 0.4468 | c0-semigroup-definition, generator-definition, C0-semigroup-model, unbounded-generator-graph | 3 | 9 |
| 11 | st.ex.heat-semigroup-lp | example | Additional KB-Specific Phases | 0.4348 | C0-semigroup-model, abstract-cauchy-evolution, resolvent-generation-criterion, Banach-space | 3 | 5 |
| 12 | st.ex.multiplication-semigroup | example | Additional KB-Specific Phases | 0.4216 | C0-semigroup-model, resolvent-generation-criterion, unbounded-generator-graph, C0-semigroup | 2 | 9 |
| 13 | st.der.generator-uniqueness | corollary | Constructive Models and Rigorous Existence Results | 0.3926 | shared-semigroup-orbit-data, unique-generator-for-semigroup, generator-uniqueness, C0-semigroup-model | 3 | 6 |
| 14 | st.der.contraction-resolvent-monotonicity | corollary | Constructive Models and Rigorous Existence Results | 0.2421 | contraction-semigroup-generator, resolvent-monotonicity, contraction-resolvent-monotonicity, contraction-generation-regime | 0 | 5 |

## Concept Tracks

### Current Bridge Agenda
- `st.thm.hille-yosida-general` (theorem), score=0.7908
- `st.def.generator` (definition), score=0.7278
- `st.def.c0-semigroup` (definition), score=0.7041

### Additional KB-Specific Phases
- `st.thm.lumer-phillips` (theorem), score=0.5674
- `st.prop.generator-closed-dense` (proposition), score=0.4835
- `st.ex.translation-semigroup` (example), score=0.4468

### Foundational Gauge-Theoretic Definitions
- `st.def.resolvent` (definition), score=0.5023

### Constructive Models and Rigorous Existence Results
- `st.der.generator-uniqueness` (corollary), score=0.3926
- `st.der.contraction-resolvent-monotonicity` (corollary), score=0.2421

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
