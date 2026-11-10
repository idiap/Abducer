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
| 1 | st.thm.hille-yosida-general | theorem | Current Bridge Agenda | 0.792 | c0-generation-implies-closed-dense-generator, resolvent-approximants-converge-to-generated-semigroup, closed-dense-plus-resolvent-powers-imply-c0-generation, closed-dense-operator-with-resolvent-power-bounds | 11 | 11 |
| 2 | st.def.generator | definition | Current Bridge Agenda | 0.719 | c0-semigroup-definition, generator-definition, C0-semigroup-model, operator-theoretic-Banach-space | 13 | 12 |
| 3 | st.def.c0-semigroup | definition | Current Bridge Agenda | 0.7055 | c0-semigroup-definition, C0-semigroup-model, operator-theoretic-Banach-space, Banach-space | 13 | 13 |
| 4 | st.thm.cauchy-problem-equivalence | theorem | Current Bridge Agenda | 0.626 | c0-generation-iff-cauchy-well-posedness, closed-operator-or-semigroup-generator, well-posed-abstract-cauchy-problem, cauchy-problem-equivalence | 7 | 7 |
| 5 | st.thm.hille-yosida-contraction | theorem | Current Bridge Agenda | 0.5547 | c0-generation-implies-closed-dense-generator, closed-dense-plus-first-resolvent-bound-imply-contraction-generation, resolvent-approximants-converge-to-generated-semigroup, closed-dense-operator-with-first-resolvent-bound | 7 | 5 |
| 6 | st.thm.lumer-phillips | theorem | Current Bridge Agenda | 0.5081 | closed-dense-plus-first-resolvent-bound-imply-contraction-generation, dissipativity-plus-range-condition-imply-contraction-generation, densely-defined-dissipative-operator-with-surjective-shift, closed-dense-operator-with-first-resolvent-bound | 6 | 4 |
| 7 | st.prop.generator-closed-dense | proposition | Additional KB-Specific Phases | 0.4506 | c0-generation-implies-closed-dense-generator, generator-of-c0-semigroup, closed-densely-defined-generator, generator-closed-dense | 4 | 3 |
| 8 | st.def.resolvent | definition | Foundational Gauge-Theoretic Definitions | 0.445 | resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme, yosida-approximation-convergence | 3 | 3 |
| 9 | st.der.yosida-approximation | derived-construction | Additional KB-Specific Phases | 0.424 | resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, contraction-semigroup-generator, bounded-generator-approximation-scheme | 1 | 3 |
| 10 | st.ex.heat-semigroup-lp | example | Additional KB-Specific Phases | 0.4123 | C0-semigroup-model, abstract-cauchy-evolution, resolvent-generation-criterion, Banach-space | 3 | 3 |
| 11 | st.ex.translation-semigroup | example | Additional KB-Specific Phases | 0.3823 | c0-semigroup-definition, generator-definition, C0-semigroup-model, unbounded-generator-graph | 3 | 4 |
| 12 | st.ex.multiplication-semigroup | example | Additional KB-Specific Phases | 0.3783 | C0-semigroup-model, resolvent-generation-criterion, unbounded-generator-graph, C0-semigroup | 1 | 5 |
| 13 | st.der.generator-uniqueness | corollary | Constructive Models and Rigorous Existence Results | 0.3691 | shared-semigroup-orbit-data, unique-generator-for-semigroup, generator-uniqueness, C0-semigroup-model | 3 | 4 |
| 14 | st.der.contraction-resolvent-monotonicity | corollary | Constructive Models and Rigorous Existence Results | 0.3218 | contraction-semigroup-generator, resolvent-monotonicity, contraction-resolvent-monotonicity, contraction-generation-regime | 1 | 3 |

## Concept Tracks

### Current Bridge Agenda
- `st.thm.hille-yosida-general` (theorem), score=0.792
- `st.def.generator` (definition), score=0.719
- `st.def.c0-semigroup` (definition), score=0.7055

### Additional KB-Specific Phases
- `st.prop.generator-closed-dense` (proposition), score=0.4506
- `st.der.yosida-approximation` (derived-construction), score=0.424
- `st.ex.heat-semigroup-lp` (example), score=0.4123

### Foundational Gauge-Theoretic Definitions
- `st.def.resolvent` (definition), score=0.445

### Constructive Models and Rigorous Existence Results
- `st.der.generator-uniqueness` (corollary), score=0.3691
- `st.der.contraction-resolvent-monotonicity` (corollary), score=0.3218

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
