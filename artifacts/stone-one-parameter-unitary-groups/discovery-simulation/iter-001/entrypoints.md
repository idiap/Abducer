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
| 1 | st.thm.stone-correspondence | theorem | Current Bridge Agenda | 0.7848 | unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group, spectral-theorem-enables-unitary-functional-calculus | 10 | 9 |
| 2 | st.thm.unitary-group-implies-self-adjoint-generator | theorem | Current Bridge Agenda | 0.7571 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero | 11 | 9 |
| 3 | st.thm.self-adjoint-implies-unitary-group | theorem | Current Bridge Agenda | 0.7315 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group | 12 | 8 |
| 4 | st.thm.spectral-theorem-functional-calculus | theorem | Current Bridge Agenda | 0.6633 | resolvent-approximants-converge-to-generated-semigroup, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space | 10 | 8 |
| 5 | st.def.self-adjoint-operator | definition | Current Bridge Agenda | 0.658 | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, stone-self-adjoint-correspondence | 10 | 9 |
| 6 | st.def.unitary-group | definition | Foundational Gauge-Theoretic Definitions | 0.6012 | strongly-continuous-unitary-group, unitary-group-definition, operator-theoretic-Hilbert-space, Hilbert-space | 11 | 9 |
| 7 | st.prop.generator-domain-regularity | proposition | Current Bridge Agenda | 0.5733 | c0-generation-implies-closed-dense-generator, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup | 2 | 8 |
| 8 | st.app.schrodinger-time-evolution | application | Additional KB-Specific Phases | 0.4809 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group | 4 | 6 |
| 9 | st.prop.generator-symmetry | proposition | Additional KB-Specific Phases | 0.4669 | differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, symmetric-generator, unitary-group-definition | 2 | 6 |
| 10 | st.ex.translation-group-on-l2 | example | Additional KB-Specific Phases | 0.3977 | strongly-continuous-unitary-group, stone-self-adjoint-correspondence, stone-unitary-group-correspondence, unitary-group-definition | 2 | 8 |

## Concept Tracks

### Current Bridge Agenda
- `st.thm.stone-correspondence` (theorem), score=0.7848
- `st.thm.unitary-group-implies-self-adjoint-generator` (theorem), score=0.7571
- `st.thm.self-adjoint-implies-unitary-group` (theorem), score=0.7315

### Foundational Gauge-Theoretic Definitions
- `st.def.unitary-group` (definition), score=0.6012

### Additional KB-Specific Phases
- `st.app.schrodinger-time-evolution` (application), score=0.4809
- `st.prop.generator-symmetry` (proposition), score=0.4669
- `st.ex.translation-group-on-l2` (example), score=0.3977

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
