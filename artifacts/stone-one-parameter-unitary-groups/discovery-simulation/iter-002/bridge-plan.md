# Essential Concept Bridge Plan

## Stats

- Input connection candidates: 40
- Bridge programs: 20
- Concept axes: 10

## Top Bridge Programs

| bridge_id | from_id | to_id | type | tier | score | expl | coh | concept | commit | concept_evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| bridge.004 | st.thm.unitary-group-implies-self-adjoint-generator | st.thm.stone-correspondence | structural support bridge | B | 0.5265 | 0.5857 | 0.0086 | 0.644 | 1.0 | unbounded-generator-graph, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-generator-characterization |
| bridge.009 | st.thm.self-adjoint-implies-unitary-group | st.thm.stone-correspondence | structural support bridge | B | 0.5127 | 0.5521 | 0.0085 | 0.62 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.007 | st.thm.spectral-theorem-functional-calculus | st.thm.self-adjoint-implies-unitary-group | structural support bridge | B | 0.4972 | 0.5879 | 0.0086 | 0.488 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.011 | st.thm.self-adjoint-implies-unitary-group | st.thm.unitary-group-implies-self-adjoint-generator | structural support bridge | B | 0.4944 | 0.5005 | 0.0085 | 0.6288 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.001 | st.def.self-adjoint-operator | st.thm.self-adjoint-implies-unitary-group | structural support bridge | B | 0.4922 | 0.5825 | 0.0086 | 0.3045 | 1.0 | self-adjoint-operator-on-hilbert-space, stone-unitary-group-correspondence, strongly-continuous-unitary-group, stone-self-adjoint-correspondence |
| bridge.013 | st.thm.self-adjoint-implies-unitary-group | st.app.schrodinger-time-evolution | structural support bridge | B | 0.4916 | 0.5461 | 0.0084 | 0.6816 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.003 | st.def.self-adjoint-operator | st.thm.unitary-group-implies-self-adjoint-generator | structural support bridge | B | 0.4838 | 0.5009 | 0.0086 | 0.3158 | 1.0 | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, unbounded-operator-domain-control, strongly-continuous-unitary-group |
| bridge.005 | st.def.unitary-group | st.thm.unitary-group-implies-self-adjoint-generator | structural support bridge | B | 0.4827 | 0.5754 | 0.0086 | 0.1902 | 1.0 | strongly-continuous-unitary-group, unitary-group-definition, unitary-group-analysis, stone-correspondence |
| bridge.006 | st.def.unitary-group | st.thm.stone-correspondence | structural support bridge | B | 0.4715 | 0.4849 | 0.0086 | 0.1683 | 1.0 | strongly-continuous-unitary-group, unitary-group-definition, unitary-group-analysis, stone-correspondence |
| bridge.008 | st.def.self-adjoint-operator | st.thm.stone-correspondence | structural support bridge | B | 0.4681 | 0.4096 | 0.0086 | 0.3047 | 1.0 | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, stone-unitary-group-correspondence, strongly-continuous-unitary-group |
| bridge.002 | st.def.unitary-group | st.thm.self-adjoint-implies-unitary-group | structural support bridge | B | 0.463 | 0.4554 | 0.0086 | 0.1953 | 1.0 | strongly-continuous-unitary-group, unitary-group-definition, unitary-group-analysis, stone-correspondence |
| bridge.010 | st.def.self-adjoint-operator | st.thm.spectral-theorem-functional-calculus | structural support bridge | B | 0.4573 | 0.6174 | 0.0085 | 0.2009 | 1.0 | self-adjoint-operator-on-hilbert-space, self-adjoint-operator-definition, self-adjoint-spectral-calculus, unitary-group-analysis |
| bridge.016 | st.prop.generator-domain-regularity | st.thm.unitary-group-implies-self-adjoint-generator | structural support bridge | B | 0.4559 | 0.4616 | 0.0084 | 0.3945 | 1.0 | unbounded-generator-graph, self-adjoint-operator-on-hilbert-space, unbounded-operator-domain-control, strongly-continuous-unitary-group |
| bridge.014 | st.thm.spectral-theorem-functional-calculus | st.thm.stone-correspondence | structural support bridge | B | 0.4515 | 0.3594 | 0.0084 | 0.3721 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.015 | st.thm.spectral-theorem-functional-calculus | st.thm.unitary-group-implies-self-adjoint-generator | structural support bridge | C | 0.4414 | 0.342 | 0.0084 | 0.3871 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.018 | st.thm.spectral-theorem-functional-calculus | st.app.schrodinger-time-evolution | structural support bridge | C | 0.4299 | 0.413 | 0.0084 | 0.4775 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.012 | st.def.unitary-group | st.thm.spectral-theorem-functional-calculus | structural support bridge | C | 0.4166 | 0.4828 | 0.0085 | 0.0347 | 1.0 | unitary-group-analysis, unitary-group, generator |
| bridge.019 | st.def.self-adjoint-operator | st.app.schrodinger-time-evolution | structural support bridge | C | 0.4138 | 0.4057 | 0.0083 | 0.358 | 1.0 | self-adjoint-operator-on-hilbert-space, stone-unitary-group-correspondence, unbounded-operator-domain-control, strongly-continuous-unitary-group |
| bridge.020 | st.def.unitary-group | st.prop.generator-symmetry | structural support bridge | C | 0.4076 | 0.4575 | 0.0083 | 0.362 | 1.0 | strongly-continuous-unitary-group, operator-theoretic-Hilbert-space, unitary-group-definition, unitary-group-analysis |
| bridge.017 | st.def.unitary-group | st.ex.translation-group-on-l2 | structural support bridge | C | 0.3971 | 0.4042 | 0.0084 | 0.3557 | 0.85 | strongly-continuous-unitary-group, unitary-group-definition, unitary-group-analysis, stone-correspondence |

## Mathematical Commitments

### bridge.004 (st.thm.unitary-group-implies-self-adjoint-generator -> st.thm.stone-correspondence)
- Antecedent schema: spectral-theorem-and-functional-calculus
- Target consequence: self-adjoint-operator-on-hilbert-space
- Preserved invariant: self-adjoint generator recovery in unbounded-generator-graph
- Barrier scope: barrier + orbit-differentiability-control + spectral-calculus-interface
- Invariant basis: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-generator-characterization, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, spectral-calculus-unitary-realization

### bridge.009 (st.thm.self-adjoint-implies-unitary-group -> st.thm.stone-correspondence)
- Antecedent schema: spectral-theorem-and-functional-calculus
- Target consequence: self-adjoint-operator-on-hilbert-space
- Preserved invariant: spectral functional-calculus realization in strongly-continuous-unitary-group
- Barrier scope: barrier + spectral-calculus-interface
- Invariant basis: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, spectral-calculus-unitary-realization, stone-unitary-group-correspondence

### bridge.007 (st.thm.spectral-theorem-functional-calculus -> st.thm.self-adjoint-implies-unitary-group)
- Antecedent schema: spectral-theorem-and-functional-calculus
- Target consequence: self-adjoint-operator-on-hilbert-space
- Preserved invariant: spectral functional-calculus realization in self-adjoint-spectral-calculus
- Barrier scope: barrier + spectral-calculus-interface
- Invariant basis: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, spectral-calculus-unitary-realization, strongly-continuous-unitary-group

### bridge.011 (st.thm.self-adjoint-implies-unitary-group -> st.thm.unitary-group-implies-self-adjoint-generator)
- Antecedent schema: spectral-theorem-and-functional-calculus
- Target consequence: self-adjoint-operator-on-hilbert-space
- Preserved invariant: spectral functional-calculus realization in strongly-continuous-unitary-group
- Barrier scope: barrier + orbit-differentiability-control + spectral-calculus-interface
- Invariant basis: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, spectral-calculus-unitary-realization, strongly-continuous-unitary-group

### bridge.001 (st.def.self-adjoint-operator -> st.thm.self-adjoint-implies-unitary-group)
- Antecedent schema: self-adjoint-operator-on-hilbert-space
- Target consequence: self-adjoint-operator-on-hilbert-space
- Preserved invariant: spectral functional-calculus realization in self-adjoint-spectral-calculus
- Barrier scope: barrier + spectral-calculus-interface + unbounded-operator-domain-control
- Invariant basis: self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, differentiable-unitary-orbit-at-zero, stone-unitary-group-correspondence, strongly-continuous-unitary-group, stone-self-adjoint-correspondence

### bridge.013 (st.thm.self-adjoint-implies-unitary-group -> st.app.schrodinger-time-evolution)
- Antecedent schema: spectral-theorem-and-functional-calculus
- Target consequence: self-adjoint-operator-on-hilbert-space
- Preserved invariant: spectral functional-calculus realization in self-adjoint-spectral-calculus
- Barrier scope: barrier + spectral-calculus-interface + unbounded-operator-domain-control
- Invariant basis: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, spectral-calculus-unitary-realization, stone-unitary-group-correspondence

### bridge.003 (st.def.self-adjoint-operator -> st.thm.unitary-group-implies-self-adjoint-generator)
- Antecedent schema: self-adjoint-operator-on-hilbert-space
- Target consequence: self-adjoint-operator-on-hilbert-space
- Preserved invariant: self-adjoint generator recovery in self-adjoint-spectral-calculus
- Barrier scope: barrier + orbit-differentiability-control + unbounded-operator-domain-control
- Invariant basis: self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, self-adjoint-operator-definition, self-adjoint-spectral-calculus

### bridge.005 (st.def.unitary-group -> st.thm.unitary-group-implies-self-adjoint-generator)
- Antecedent schema: strongly-continuous-unitary-group
- Target consequence: self-adjoint-operator-on-hilbert-space
- Preserved invariant: unitary orbit infinitesimal control in strongly-continuous-unitary-group
- Barrier scope: barrier + orbit-differentiability-control + unbounded-operator-domain-control
- Invariant basis: self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, strongly-continuous-unitary-group, unique-self-adjoint-generator, unitary-group-definition, Stone-correspondence

### bridge.006 (st.def.unitary-group -> st.thm.stone-correspondence)
- Antecedent schema: strongly-continuous-unitary-group
- Target consequence: self-adjoint-operator-on-hilbert-space
- Preserved invariant: unitary orbit infinitesimal control in strongly-continuous-unitary-group
- Barrier scope: spectral-calculus-interface
- Invariant basis: self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, strongly-continuous-unitary-group, stone-self-adjoint-correspondence, unique-self-adjoint-generator, unitary-group-definition

### bridge.008 (st.def.self-adjoint-operator -> st.thm.stone-correspondence)
- Antecedent schema: self-adjoint-operator-on-hilbert-space
- Target consequence: self-adjoint-operator-on-hilbert-space
- Preserved invariant: self-adjoint generator recovery in self-adjoint-spectral-calculus
- Barrier scope: spectral-calculus-interface + unbounded-operator-domain-control
- Invariant basis: self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, differentiable-unitary-orbit-at-zero, stone-unitary-group-correspondence, strongly-continuous-unitary-group, stone-self-adjoint-correspondence

## Bridge Axes

### stone-correspondence -> stone-correspondence
- Count: 3
- bridge.004: st.thm.unitary-group-implies-self-adjoint-generator -> st.thm.stone-correspondence (score=0.5265)
- bridge.009: st.thm.self-adjoint-implies-unitary-group -> st.thm.stone-correspondence (score=0.5127)
- bridge.011: st.thm.self-adjoint-implies-unitary-group -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.4944)

### spectral-functional-calculus -> stone-correspondence
- Count: 3
- bridge.007: st.thm.spectral-theorem-functional-calculus -> st.thm.self-adjoint-implies-unitary-group (score=0.4972)
- bridge.014: st.thm.spectral-theorem-functional-calculus -> st.thm.stone-correspondence (score=0.4515)
- bridge.015: st.thm.spectral-theorem-functional-calculus -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.4414)

### foundational-definitions -> stone-correspondence
- Count: 6
- bridge.001: st.def.self-adjoint-operator -> st.thm.self-adjoint-implies-unitary-group (score=0.4922)
- bridge.003: st.def.self-adjoint-operator -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.4838)
- bridge.005: st.def.unitary-group -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.4827)

### stone-correspondence -> applications
- Count: 1
- bridge.013: st.thm.self-adjoint-implies-unitary-group -> st.app.schrodinger-time-evolution (score=0.4916)

### foundational-definitions -> spectral-functional-calculus
- Count: 2
- bridge.010: st.def.self-adjoint-operator -> st.thm.spectral-theorem-functional-calculus (score=0.4573)
- bridge.012: st.def.unitary-group -> st.thm.spectral-theorem-functional-calculus (score=0.4166)

### generator-regularity -> stone-correspondence
- Count: 1
- bridge.016: st.prop.generator-domain-regularity -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.4559)

### spectral-functional-calculus -> applications
- Count: 1
- bridge.018: st.thm.spectral-theorem-functional-calculus -> st.app.schrodinger-time-evolution (score=0.4299)

### foundational-definitions -> applications
- Count: 1
- bridge.019: st.def.self-adjoint-operator -> st.app.schrodinger-time-evolution (score=0.4138)

### foundational-definitions -> generator-regularity
- Count: 1
- bridge.020: st.def.unitary-group -> st.prop.generator-symmetry (score=0.4076)

### foundational-definitions -> canonical-examples
- Count: 1
- bridge.017: st.def.unitary-group -> st.ex.translation-group-on-l2 (score=0.3971)

## Recommended Run Order

1. bridge.004
2. bridge.009
3. bridge.007
4. bridge.011
5. bridge.001
6. bridge.013
