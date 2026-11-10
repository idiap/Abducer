# Conceptual Entry Points

## Stats

- Statements analyzed: 14
- Ranked entry points: 14
- Connector interventions used: 14
- Connector links used: 40
- Proof hypotheses used: 52
- Coherence signals used: 52

## Top Entry Points

| rank | statement_id | kind | phase | entry_score | concepts | hyp_count | bridge_count |
|---|---|---|---|---|---|---|---|
| 1 | st.thm.hille-yosida-general | theorem | Current Bridge Agenda | 0.8206 | c0-generation-implies-closed-dense-generator, resolvent-approximants-converge-to-generated-semigroup, closed-dense-plus-resolvent-powers-imply-c0-generation, closed-dense-operator-with-resolvent-power-bounds | 14 | 11 |
| 2 | st.def.generator | definition | Current Bridge Agenda | 0.6801 | c0-semigroup-definition, generator-definition, C0-semigroup-model, operator-theoretic-Banach-space | 13 | 10 |
| 3 | st.def.c0-semigroup | definition | Current Bridge Agenda | 0.6649 | c0-semigroup-definition, C0-semigroup-model, operator-theoretic-Banach-space, Banach-space | 16 | 10 |
| 4 | st.thm.cauchy-problem-equivalence | theorem | Current Bridge Agenda | 0.6594 | c0-generation-iff-cauchy-well-posedness, closed-operator-or-semigroup-generator, well-posed-abstract-cauchy-problem, cauchy-problem-equivalence | 8 | 9 |
| 5 | st.thm.hille-yosida-contraction | theorem | Current Bridge Agenda | 0.6062 | c0-generation-implies-closed-dense-generator, closed-dense-plus-first-resolvent-bound-imply-contraction-generation, resolvent-approximants-converge-to-generated-semigroup, closed-dense-operator-with-first-resolvent-bound | 8 | 7 |
| 6 | st.thm.lumer-phillips | theorem | Current Bridge Agenda | 0.5308 | closed-dense-plus-first-resolvent-bound-imply-contraction-generation, dissipativity-plus-range-condition-imply-contraction-generation, densely-defined-dissipative-operator-with-surjective-shift, closed-dense-operator-with-first-resolvent-bound | 7 | 5 |
| 7 | st.prop.generator-closed-dense | proposition | Additional KB-Specific Phases | 0.518 | c0-generation-implies-closed-dense-generator, generator-of-c0-semigroup, closed-densely-defined-generator, generator-closed-dense | 5 | 4 |
| 8 | st.def.resolvent | definition | Foundational Gauge-Theoretic Definitions | 0.4618 | resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme, yosida-approximation-convergence | 5 | 4 |
| 9 | st.der.yosida-approximation | derived-construction | Additional KB-Specific Phases | 0.4433 | resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, contraction-semigroup-generator, bounded-generator-approximation-scheme | 3 | 3 |
| 10 | st.ex.heat-semigroup-lp | example | Additional KB-Specific Phases | 0.4154 | C0-semigroup-model, abstract-cauchy-evolution, resolvent-generation-criterion, Banach-space | 4 | 3 |
| 11 | st.der.contraction-resolvent-monotonicity | corollary | Constructive Models and Rigorous Existence Results | 0.3772 | contraction-semigroup-generator, resolvent-monotonicity, contraction-resolvent-monotonicity, contraction-generation-regime | 2 | 5 |
| 12 | st.der.generator-uniqueness | corollary | Constructive Models and Rigorous Existence Results | 0.3731 | shared-semigroup-orbit-data, unique-generator-for-semigroup, generator-uniqueness, C0-semigroup-model | 3 | 4 |
| 13 | st.ex.multiplication-semigroup | example | Additional KB-Specific Phases | 0.3569 | C0-semigroup-model, resolvent-generation-criterion, unbounded-generator-graph, C0-semigroup | 2 | 3 |
| 14 | st.ex.translation-semigroup | example | Additional KB-Specific Phases | 0.344 | c0-semigroup-definition, generator-definition, C0-semigroup-model, unbounded-generator-graph | 2 | 2 |

## Concept Tracks

### Current Bridge Agenda
- `st.thm.hille-yosida-general` (theorem), score=0.8206
- `st.def.generator` (definition), score=0.6801
- `st.def.c0-semigroup` (definition), score=0.6649

### Additional KB-Specific Phases
- `st.prop.generator-closed-dense` (proposition), score=0.518
- `st.der.yosida-approximation` (derived-construction), score=0.4433
- `st.ex.heat-semigroup-lp` (example), score=0.4154

### Foundational Gauge-Theoretic Definitions
- `st.def.resolvent` (definition), score=0.4618

### Constructive Models and Rigorous Existence Results
- `st.der.contraction-resolvent-monotonicity` (corollary), score=0.3772
- `st.der.generator-uniqueness` (corollary), score=0.3731

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
