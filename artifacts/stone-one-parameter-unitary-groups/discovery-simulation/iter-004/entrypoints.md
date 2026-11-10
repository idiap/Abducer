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
| 1 | st.thm.stone-correspondence | theorem | Current Bridge Agenda | 0.8321 | unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group, spectral-theorem-enables-unitary-functional-calculus | 13 | 9 |
| 2 | st.thm.unitary-group-implies-self-adjoint-generator | theorem | Current Bridge Agenda | 0.7573 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero | 16 | 9 |
| 3 | st.thm.self-adjoint-implies-unitary-group | theorem | Current Bridge Agenda | 0.7315 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group | 13 | 8 |
| 4 | st.thm.spectral-theorem-functional-calculus | theorem | Current Bridge Agenda | 0.6633 | resolvent-approximants-converge-to-generated-semigroup, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space | 13 | 8 |
| 5 | st.def.self-adjoint-operator | definition | Current Bridge Agenda | 0.658 | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, stone-self-adjoint-correspondence | 12 | 9 |
| 6 | st.def.unitary-group | definition | Foundational Gauge-Theoretic Definitions | 0.6012 | strongly-continuous-unitary-group, unitary-group-definition, operator-theoretic-Hilbert-space, Hilbert-space | 15 | 9 |
| 7 | st.prop.generator-domain-regularity | proposition | Current Bridge Agenda | 0.5844 | c0-generation-implies-closed-dense-generator, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup | 6 | 8 |
| 8 | st.prop.generator-symmetry | proposition | Additional KB-Specific Phases | 0.5116 | differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, symmetric-generator, unitary-group-definition | 5 | 6 |
| 9 | st.app.schrodinger-time-evolution | application | Additional KB-Specific Phases | 0.4964 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group | 9 | 6 |
| 10 | st.ex.translation-group-on-l2 | example | Additional KB-Specific Phases | 0.4088 | strongly-continuous-unitary-group, stone-self-adjoint-correspondence, stone-unitary-group-correspondence, unitary-group-definition | 4 | 8 |

## Concept Tracks

### Current Bridge Agenda
- `st.thm.stone-correspondence` (theorem), score=0.8321
- `st.thm.unitary-group-implies-self-adjoint-generator` (theorem), score=0.7573
- `st.thm.self-adjoint-implies-unitary-group` (theorem), score=0.7315

### Foundational Gauge-Theoretic Definitions
- `st.def.unitary-group` (definition), score=0.6012

### Additional KB-Specific Phases
- `st.prop.generator-symmetry` (proposition), score=0.5116
- `st.app.schrodinger-time-evolution` (application), score=0.4964
- `st.ex.translation-group-on-l2` (example), score=0.4088

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
