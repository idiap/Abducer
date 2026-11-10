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
| 1 | st.thm.unitary-group-implies-self-adjoint-generator | theorem | Current Bridge Agenda | 0.8212 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero | 11 | 9 |
| 2 | st.thm.self-adjoint-implies-unitary-group | theorem | Current Bridge Agenda | 0.7935 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group | 12 | 8 |
| 3 | st.thm.stone-correspondence | theorem | Current Bridge Agenda | 0.7636 | unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group, spectral-theorem-enables-unitary-functional-calculus | 10 | 9 |
| 4 | st.thm.spectral-theorem-functional-calculus | theorem | Current Bridge Agenda | 0.7215 | resolvent-approximants-converge-to-generated-semigroup, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space | 10 | 8 |
| 5 | st.def.self-adjoint-operator | definition | Current Bridge Agenda | 0.7149 | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, stone-self-adjoint-correspondence | 10 | 9 |
| 6 | st.def.unitary-group | definition | Foundational Gauge-Theoretic Definitions | 0.6521 | strongly-continuous-unitary-group, unitary-group-definition, operator-theoretic-Hilbert-space, Hilbert-space | 11 | 9 |
| 7 | st.prop.generator-domain-regularity | proposition | Current Bridge Agenda | 0.6238 | c0-generation-implies-closed-dense-generator, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup | 2 | 8 |
| 8 | st.app.schrodinger-time-evolution | application | Additional KB-Specific Phases | 0.5209 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group | 4 | 6 |
| 9 | st.prop.generator-symmetry | proposition | Additional KB-Specific Phases | 0.5087 | differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, symmetric-generator, unitary-group-definition | 2 | 6 |
| 10 | st.ex.translation-group-on-l2 | example | Additional KB-Specific Phases | 0.4352 | strongly-continuous-unitary-group, stone-self-adjoint-correspondence, stone-unitary-group-correspondence, unitary-group-definition | 2 | 8 |

## Concept Tracks

### Current Bridge Agenda
- `st.thm.unitary-group-implies-self-adjoint-generator` (theorem), score=0.8212
- `st.thm.self-adjoint-implies-unitary-group` (theorem), score=0.7935
- `st.thm.stone-correspondence` (theorem), score=0.7636

### Foundational Gauge-Theoretic Definitions
- `st.def.unitary-group` (definition), score=0.6521

### Additional KB-Specific Phases
- `st.app.schrodinger-time-evolution` (application), score=0.5209
- `st.prop.generator-symmetry` (proposition), score=0.5087
- `st.ex.translation-group-on-l2` (example), score=0.4352

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
