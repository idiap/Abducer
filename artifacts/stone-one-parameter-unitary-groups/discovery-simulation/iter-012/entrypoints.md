# Conceptual Entry Points

## Stats

- Statements analyzed: 10
- Ranked entry points: 10
- Connector interventions used: 10
- Connector links used: 40
- Proof hypotheses used: 34
- Coherence signals used: 34

## Top Entry Points

| rank | statement_id | kind | phase | entry_score | concepts | hyp_count | bridge_count |
|---|---|---|---|---|---|---|---|
| 1 | st.thm.unitary-group-implies-self-adjoint-generator | theorem | Current Bridge Agenda | 0.8253 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero | 10 | 9 |
| 2 | st.thm.self-adjoint-implies-unitary-group | theorem | Current Bridge Agenda | 0.7977 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group | 10 | 8 |
| 3 | st.thm.stone-correspondence | theorem | Current Bridge Agenda | 0.7677 | unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group, spectral-theorem-enables-unitary-functional-calculus | 9 | 9 |
| 4 | st.def.self-adjoint-operator | definition | Current Bridge Agenda | 0.7146 | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, stone-self-adjoint-correspondence | 8 | 9 |
| 5 | st.thm.spectral-theorem-functional-calculus | theorem | Current Bridge Agenda | 0.7127 | resolvent-approximants-converge-to-generated-semigroup, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space | 7 | 8 |
| 6 | st.def.unitary-group | definition | Foundational Gauge-Theoretic Definitions | 0.6557 | strongly-continuous-unitary-group, unitary-group-definition, operator-theoretic-Hilbert-space, Hilbert-space | 8 | 9 |
| 7 | st.prop.generator-domain-regularity | proposition | Current Bridge Agenda | 0.6266 | c0-generation-implies-closed-dense-generator, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup | 2 | 8 |
| 8 | st.app.schrodinger-time-evolution | application | Additional KB-Specific Phases | 0.5225 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group | 2 | 6 |
| 9 | st.prop.generator-symmetry | proposition | Additional KB-Specific Phases | 0.4936 | differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, symmetric-generator, unitary-group-definition | 1 | 6 |
| 10 | st.ex.translation-group-on-l2 | example | Additional KB-Specific Phases | 0.4131 | strongly-continuous-unitary-group, stone-self-adjoint-correspondence, stone-unitary-group-correspondence, unitary-group-definition | 1 | 8 |

## Concept Tracks

### Current Bridge Agenda
- `st.thm.unitary-group-implies-self-adjoint-generator` (theorem), score=0.8253
- `st.thm.self-adjoint-implies-unitary-group` (theorem), score=0.7977
- `st.thm.stone-correspondence` (theorem), score=0.7677

### Foundational Gauge-Theoretic Definitions
- `st.def.unitary-group` (definition), score=0.6557

### Additional KB-Specific Phases
- `st.app.schrodinger-time-evolution` (application), score=0.5225
- `st.prop.generator-symmetry` (proposition), score=0.4936
- `st.ex.translation-group-on-l2` (example), score=0.4131

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
