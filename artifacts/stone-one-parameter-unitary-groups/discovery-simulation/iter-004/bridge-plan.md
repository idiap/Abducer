# Essential Concept Bridge Plan

## Stats

- Input connection candidates: 40
- Bridge programs: 20
- Concept axes: 7

## Top Bridge Programs

| bridge_id | from_id | to_id | type | tier | score | expl | coh | concept | commit | concept_evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| bridge.004 | st.thm.unitary-group-implies-self-adjoint-generator | st.thm.stone-correspondence | structural support bridge | B | 0.5368 | 0.5857 | 0.0075 | 0.644 | 1.0 | unbounded-generator-graph, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-generator-characterization |
| bridge.009 | st.thm.self-adjoint-implies-unitary-group | st.thm.stone-correspondence | structural support bridge | B | 0.523 | 0.5521 | 0.0075 | 0.62 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.007 | st.thm.spectral-theorem-functional-calculus | st.thm.self-adjoint-implies-unitary-group | structural support bridge | B | 0.4971 | 0.5879 | 0.0075 | 0.488 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.011 | st.thm.self-adjoint-implies-unitary-group | st.thm.unitary-group-implies-self-adjoint-generator | structural support bridge | B | 0.4943 | 0.5005 | 0.0074 | 0.6288 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.001 | st.def.self-adjoint-operator | st.thm.self-adjoint-implies-unitary-group | structural support bridge | B | 0.4921 | 0.5825 | 0.0076 | 0.3045 | 1.0 | self-adjoint-operator-on-hilbert-space, stone-unitary-group-correspondence, strongly-continuous-unitary-group, stone-self-adjoint-correspondence |
| bridge.013 | st.thm.self-adjoint-implies-unitary-group | st.app.schrodinger-time-evolution | structural support bridge | B | 0.4915 | 0.5461 | 0.0074 | 0.6816 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.003 | st.def.self-adjoint-operator | st.thm.unitary-group-implies-self-adjoint-generator | structural support bridge | B | 0.4838 | 0.5009 | 0.0076 | 0.3158 | 1.0 | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, unbounded-operator-domain-control, strongly-continuous-unitary-group |
| bridge.005 | st.def.unitary-group | st.thm.unitary-group-implies-self-adjoint-generator | structural support bridge | B | 0.4826 | 0.5754 | 0.0075 | 0.1902 | 1.0 | strongly-continuous-unitary-group, unitary-group-definition, unitary-group-analysis, stone-correspondence |
| bridge.006 | st.def.unitary-group | st.thm.stone-correspondence | structural support bridge | B | 0.4818 | 0.4849 | 0.0075 | 0.1683 | 1.0 | strongly-continuous-unitary-group, unitary-group-definition, unitary-group-analysis, stone-correspondence |
| bridge.008 | st.def.self-adjoint-operator | st.thm.stone-correspondence | structural support bridge | B | 0.4784 | 0.4096 | 0.0075 | 0.3047 | 1.0 | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, stone-unitary-group-correspondence, strongly-continuous-unitary-group |
| bridge.016 | st.prop.generator-domain-regularity | st.thm.unitary-group-implies-self-adjoint-generator | structural support bridge | B | 0.4725 | 0.5803 | 0.0073 | 0.3945 | 1.0 | unbounded-generator-graph, self-adjoint-operator-on-hilbert-space, unbounded-operator-domain-control, strongly-continuous-unitary-group |
| bridge.014 | st.thm.spectral-theorem-functional-calculus | st.thm.stone-correspondence | structural support bridge | B | 0.472 | 0.4317 | 0.0074 | 0.3721 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.021 | st.thm.stone-correspondence | st.app.schrodinger-time-evolution | structural support bridge | B | 0.4663 | 0.453 | 0.0072 | 0.4857 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.002 | st.def.unitary-group | st.thm.self-adjoint-implies-unitary-group | structural support bridge | B | 0.4628 | 0.4554 | 0.0076 | 0.1953 | 1.0 | strongly-continuous-unitary-group, unitary-group-definition, unitary-group-analysis, stone-correspondence |
| bridge.015 | st.thm.spectral-theorem-functional-calculus | st.thm.unitary-group-implies-self-adjoint-generator | structural support bridge | B | 0.458 | 0.4609 | 0.0073 | 0.3871 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.010 | st.def.self-adjoint-operator | st.thm.spectral-theorem-functional-calculus | structural support bridge | B | 0.4572 | 0.6174 | 0.0075 | 0.2009 | 1.0 | self-adjoint-operator-on-hilbert-space, self-adjoint-operator-definition, self-adjoint-spectral-calculus, unitary-group-analysis |
| bridge.022 | st.thm.unitary-group-implies-self-adjoint-generator | st.app.schrodinger-time-evolution | structural support bridge | C | 0.4455 | 0.3999 | 0.0072 | 0.5306 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.018 | st.thm.spectral-theorem-functional-calculus | st.app.schrodinger-time-evolution | structural support bridge | C | 0.4298 | 0.413 | 0.0073 | 0.4775 | 1.0 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus |
| bridge.024 | st.prop.generator-symmetry | st.thm.unitary-group-implies-self-adjoint-generator | structural support bridge | C | 0.4224 | 0.4332 | 0.0072 | 0.2638 | 1.0 | unbounded-generator-graph, differentiable-unitary-orbit-at-zero, unbounded-operator-domain-control, strongly-continuous-unitary-group |
| bridge.012 | st.def.unitary-group | st.thm.spectral-theorem-functional-calculus | structural support bridge | C | 0.4165 | 0.4828 | 0.0074 | 0.0347 | 1.0 | unitary-group-analysis, unitary-group, generator |

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
- bridge.004: st.thm.unitary-group-implies-self-adjoint-generator -> st.thm.stone-correspondence (score=0.5368)
- bridge.009: st.thm.self-adjoint-implies-unitary-group -> st.thm.stone-correspondence (score=0.523)
- bridge.011: st.thm.self-adjoint-implies-unitary-group -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.4943)

### spectral-functional-calculus -> stone-correspondence
- Count: 3
- bridge.007: st.thm.spectral-theorem-functional-calculus -> st.thm.self-adjoint-implies-unitary-group (score=0.4971)
- bridge.014: st.thm.spectral-theorem-functional-calculus -> st.thm.stone-correspondence (score=0.472)
- bridge.015: st.thm.spectral-theorem-functional-calculus -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.458)

### foundational-definitions -> stone-correspondence
- Count: 6
- bridge.001: st.def.self-adjoint-operator -> st.thm.self-adjoint-implies-unitary-group (score=0.4921)
- bridge.003: st.def.self-adjoint-operator -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.4838)
- bridge.005: st.def.unitary-group -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.4826)

### stone-correspondence -> applications
- Count: 3
- bridge.013: st.thm.self-adjoint-implies-unitary-group -> st.app.schrodinger-time-evolution (score=0.4915)
- bridge.021: st.thm.stone-correspondence -> st.app.schrodinger-time-evolution (score=0.4663)
- bridge.022: st.thm.unitary-group-implies-self-adjoint-generator -> st.app.schrodinger-time-evolution (score=0.4455)

### generator-regularity -> stone-correspondence
- Count: 2
- bridge.016: st.prop.generator-domain-regularity -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.4725)
- bridge.024: st.prop.generator-symmetry -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.4224)

### foundational-definitions -> spectral-functional-calculus
- Count: 2
- bridge.010: st.def.self-adjoint-operator -> st.thm.spectral-theorem-functional-calculus (score=0.4572)
- bridge.012: st.def.unitary-group -> st.thm.spectral-theorem-functional-calculus (score=0.4165)

### spectral-functional-calculus -> applications
- Count: 1
- bridge.018: st.thm.spectral-theorem-functional-calculus -> st.app.schrodinger-time-evolution (score=0.4298)

## Recommended Run Order

1. bridge.004
2. bridge.009
3. bridge.007
4. bridge.011
5. bridge.001
6. bridge.013
