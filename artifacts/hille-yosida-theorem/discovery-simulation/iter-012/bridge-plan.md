# Essential Concept Bridge Plan

## Stats

- Input connection candidates: 40
- Bridge programs: 20
- Concept axes: 13

## Top Bridge Programs

| bridge_id | from_id | to_id | type | tier | score | expl | coh | concept | commit | concept_evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| bridge.002 | st.def.generator | st.thm.hille-yosida-general | structural support bridge | B | 0.5858 | 0.561 | 0.0095 | 0.1951 | 1.0 | unbounded-generator-graph, unbounded-operator-domain-control, operator-theoretic-Banach-space, domain-closure-density |
| bridge.003 | st.def.c0-semigroup | st.thm.hille-yosida-general | structural support bridge | B | 0.5754 | 0.5338 | 0.0095 | 0.1464 | 1.0 | operator-theoretic-Banach-space, semigroup-generation, unbounded-operator, C0-semigroup-model |
| bridge.001 | st.def.c0-semigroup | st.thm.cauchy-problem-equivalence | structural support bridge | B | 0.5649 | 0.591 | 0.0096 | 0.1986 | 1.0 | operator-theoretic-Banach-space, semigroup-generation, C0-semigroup-model, laplace-transform |
| bridge.009 | st.thm.hille-yosida-general | st.thm.hille-yosida-contraction | structural support bridge | B | 0.5447 | 0.4778 | 0.0091 | 0.4075 | 1.0 | c0-generation-implies-closed-dense-generator, resolvent-approximants-converge-to-generated-semigroup, bounded-generator-approximation-scheme, unbounded-operator-domain-control |
| bridge.004 | st.def.generator | st.thm.cauchy-problem-equivalence | structural support bridge | B | 0.5428 | 0.5662 | 0.0095 | 0.185 | 1.0 | unbounded-operator-domain-control, operator-theoretic-Banach-space, semigroup-generation, C0-semigroup-model |
| bridge.011 | st.def.resolvent | st.thm.hille-yosida-general | structural support bridge | B | 0.5081 | 0.3624 | 0.009 | 0.2853 | 1.0 | resolvent-approximants-converge-to-generated-semigroup, bounded-generator-approximation-scheme, yosida-approximation-convergence, resolvent-family-at-large-lambda |
| bridge.005 | st.def.c0-semigroup | st.thm.lumer-phillips | proof-complexity bridge | B | 0.5061 | 0.4582 | 0.0093 | 0.1332 | 1.0 | operator-theoretic-Banach-space, semigroup-generation, unbounded-operator, C0-semigroup-model |
| bridge.007 | st.def.c0-semigroup | st.thm.hille-yosida-contraction | structural support bridge | B | 0.5034 | 0.5166 | 0.0092 | 0.0995 | 1.0 | c0-semigroup-definition, semigroup-generation, C0-semigroup-model, C0-semigroup |
| bridge.006 | st.def.generator | st.thm.lumer-phillips | proof-complexity bridge | B | 0.5022 | 0.4291 | 0.0093 | 0.186 | 1.0 | unbounded-generator-graph, unbounded-operator-domain-control, operator-theoretic-Banach-space, domain-closure-density |
| bridge.008 | st.def.generator | st.thm.hille-yosida-contraction | structural support bridge | B | 0.4892 | 0.4769 | 0.0091 | 0.136 | 1.0 | unbounded-operator-domain-control, c0-semigroup-definition, domain-closure-density, semigroup-generation |
| bridge.012 | st.def.generator | st.prop.generator-closed-dense | structural support bridge | B | 0.4826 | 0.4673 | 0.009 | 0.2879 | 1.0 | unbounded-generator-graph, unbounded-operator-domain-control, domain-closure-density, semigroup-generation |
| bridge.015 | st.thm.hille-yosida-general | st.ex.translation-semigroup | structural support bridge | B | 0.4769 | 0.2939 | 0.0089 | 0.143 | 1.0 | unbounded-generator-graph, unbounded-operator-domain-control, semigroup-generation, generator-analysis |
| bridge.014 | st.thm.hille-yosida-general | st.ex.multiplication-semigroup | structural support bridge | B | 0.4695 | 0.3053 | 0.0089 | 0.2027 | 0.75 | unbounded-generator-graph, unbounded-operator-domain-control, resolvent-generation-criterion, semigroup-generation |
| bridge.010 | st.def.c0-semigroup | st.ex.heat-semigroup-lp | structural support bridge | C | 0.4484 | 0.3531 | 0.0091 | 0.1233 | 0.75 | semigroup-generation, C0-semigroup-model, laplace-transform, C0-semigroup |
| bridge.016 | st.def.generator | st.der.generator-uniqueness | structural support bridge | C | 0.4451 | 0.3059 | 0.0089 | 0.2302 | 1.0 | unbounded-generator-graph, semigroup-generation, generator-analysis, C0-semigroup-model |
| bridge.013 | st.thm.cauchy-problem-equivalence | st.thm.lumer-phillips | proof-complexity bridge | C | 0.4391 | 0.2641 | 0.009 | 0.1262 | 1.0 | unbounded-operator-domain-control, operator-theoretic-Banach-space, semigroup-generation, C0-semigroup-model |
| bridge.023 | st.thm.hille-yosida-general | st.der.yosida-approximation | proof-complexity bridge | C | 0.4007 | 0.3804 | 0.0 | 0.4227 | 0.0 | unbounded-generator-graph, resolvent-approximants-converge-to-generated-semigroup, bounded-generator-approximation-scheme, unbounded-operator-domain-control |
| bridge.022 | st.prop.generator-closed-dense | st.thm.hille-yosida-general | structural support bridge | C | 0.3948 | 0.3778 | 0.0 | 0.3525 | 0.0 | c0-generation-implies-closed-dense-generator, unbounded-generator-graph, unbounded-operator-domain-control, closed-densely-defined-generator |
| bridge.025 | st.thm.hille-yosida-general | st.thm.lumer-phillips | proof-complexity bridge | C | 0.3607 | 0.2459 | 0.0 | 0.1714 | 0.0 | unbounded-generator-graph, unbounded-operator-domain-control, operator-theoretic-Banach-space, domain-closure-density |
| bridge.031 | st.thm.hille-yosida-general | st.der.generator-uniqueness | structural support bridge | C | 0.3353 | 0.167 | 0.0 | 0.119 | 0.0 | unbounded-generator-graph, semigroup-generation, generator-analysis, C0-semigroup-model |

## Mathematical Commitments

### bridge.002 (st.def.generator -> st.thm.hille-yosida-general)
- Antecedent schema: c0-semigroup-definition
- Target consequence: generator-of-exponentially-bounded-c0-semigroup
- Preserved invariant: Yosida approximation convergence in unbounded-generator-graph
- Barrier scope: approximation-limit-control + barrier + domain-closure-density
- Invariant basis: generator-of-exponentially-bounded-c0-semigroup, bounded-generator-approximation-scheme, closed-densely-defined-generator, operator-theoretic-Banach-space, unbounded-generator-graph, C0-semigroup-model

### bridge.003 (st.def.c0-semigroup -> st.thm.hille-yosida-general)
- Antecedent schema: c0-semigroup-definition
- Target consequence: generator-of-exponentially-bounded-c0-semigroup
- Preserved invariant: Yosida approximation convergence in operator-theoretic-Banach-space
- Barrier scope: barrier + domain-closure-density + powers-of-resolvent-verification
- Invariant basis: generator-of-exponentially-bounded-c0-semigroup, bounded-generator-approximation-scheme, closed-densely-defined-generator, operator-theoretic-Banach-space, unbounded-operator, C0-semigroup-model

### bridge.001 (st.def.c0-semigroup -> st.thm.cauchy-problem-equivalence)
- Antecedent schema: c0-semigroup-definition
- Target consequence: well-posed-abstract-cauchy-problem
- Preserved invariant: generator-to-well-posed-evolution correspondence
- Barrier scope: unbounded-operator-domain-control
- Invariant basis: well-posed-abstract-cauchy-problem, operator-theoretic-Banach-space, C0-semigroup-model, C0-semigroup, Banach-space, generator

### bridge.009 (st.thm.hille-yosida-general -> st.thm.hille-yosida-contraction)
- Antecedent schema: closed-dense-operator-with-resolvent-power-bounds
- Target consequence: bounded-generator-approximation-scheme
- Preserved invariant: Yosida approximation convergence in resolvent-generation-criterion
- Barrier scope: barrier + domain-closure-density + powers-of-resolvent-verification
- Invariant basis: resolvent-approximants-converge-to-generated-semigroup, closed-dense-operator-with-resolvent-power-bounds, c0-generation-implies-closed-dense-generator, bounded-generator-approximation-scheme, generator-of-contraction-c0-semigroup, yosida-approximation-convergence

### bridge.004 (st.def.generator -> st.thm.cauchy-problem-equivalence)
- Antecedent schema: c0-semigroup-definition
- Target consequence: well-posed-abstract-cauchy-problem
- Preserved invariant: generator-to-well-posed-evolution correspondence
- Barrier scope: approximation-limit-control + domain-closure-density + unbounded-operator-domain-control
- Invariant basis: well-posed-abstract-cauchy-problem, operator-theoretic-Banach-space, C0-semigroup-model, C0-semigroup, generator

### bridge.011 (st.def.resolvent -> st.thm.hille-yosida-general)
- Antecedent schema: resolvent-family-at-large-lambda
- Target consequence: generator-of-exponentially-bounded-c0-semigroup
- Preserved invariant: resolvent growth control in resolvent-generation-criterion
- Barrier scope: barrier + domain-closure-density + powers-of-resolvent-verification
- Invariant basis: resolvent-approximants-converge-to-generated-semigroup, generator-of-exponentially-bounded-c0-semigroup, bounded-generator-approximation-scheme, yosida-approximation-convergence, resolvent-family-at-large-lambda, closed-densely-defined-generator

### bridge.005 (st.def.c0-semigroup -> st.thm.lumer-phillips)
- Antecedent schema: c0-semigroup-definition
- Target consequence: contraction-semigroup-via-dissipativity
- Preserved invariant: dissipative range-surjectivity criterion
- Barrier scope: barrier + domain-closure-density + unbounded-operator-domain-control
- Invariant basis: contraction-semigroup-via-dissipativity, generator-of-contraction-c0-semigroup, operator-theoretic-Banach-space, unbounded-operator, C0-semigroup-model, C0-semigroup

### bridge.007 (st.def.c0-semigroup -> st.thm.hille-yosida-contraction)
- Antecedent schema: c0-semigroup-definition
- Target consequence: bounded-generator-approximation-scheme
- Preserved invariant: Yosida approximation convergence in C0-semigroup-model
- Barrier scope: domain-closure-density + unbounded-operator-domain-control
- Invariant basis: bounded-generator-approximation-scheme, generator-of-contraction-c0-semigroup, closed-densely-defined-generator, c0-semigroup-definition, resolvent-monotonicity, C0-semigroup-model

### bridge.006 (st.def.generator -> st.thm.lumer-phillips)
- Antecedent schema: c0-semigroup-definition
- Target consequence: contraction-semigroup-via-dissipativity
- Preserved invariant: dissipative range-surjectivity criterion
- Barrier scope: approximation-limit-control + barrier + domain-closure-density
- Invariant basis: contraction-semigroup-via-dissipativity, generator-of-contraction-c0-semigroup, operator-theoretic-Banach-space, unbounded-generator-graph, C0-semigroup-model, C0-semigroup

### bridge.008 (st.def.generator -> st.thm.hille-yosida-contraction)
- Antecedent schema: c0-semigroup-definition
- Target consequence: bounded-generator-approximation-scheme
- Preserved invariant: Yosida approximation convergence in C0-semigroup-model
- Barrier scope: approximation-limit-control + domain-closure-density + unbounded-operator-domain-control
- Invariant basis: bounded-generator-approximation-scheme, generator-of-contraction-c0-semigroup, closed-densely-defined-generator, c0-semigroup-definition, resolvent-monotonicity, C0-semigroup-model

## Bridge Axes

### foundational-definitions -> core-generation-theorem
- Count: 5
- bridge.002: st.def.generator -> st.thm.hille-yosida-general (score=0.5858)
- bridge.003: st.def.c0-semigroup -> st.thm.hille-yosida-general (score=0.5754)
- bridge.011: st.def.resolvent -> st.thm.hille-yosida-general (score=0.5081)

### foundational-definitions -> problem-semantics
- Count: 2
- bridge.001: st.def.c0-semigroup -> st.thm.cauchy-problem-equivalence (score=0.5649)
- bridge.004: st.def.generator -> st.thm.cauchy-problem-equivalence (score=0.5428)

### core-generation-theorem -> core-generation-theorem
- Count: 1
- bridge.009: st.thm.hille-yosida-general -> st.thm.hille-yosida-contraction (score=0.5447)

### foundational-definitions -> equivalent-characterizations
- Count: 2
- bridge.005: st.def.c0-semigroup -> st.thm.lumer-phillips (score=0.5061)
- bridge.006: st.def.generator -> st.thm.lumer-phillips (score=0.5022)

### foundational-definitions -> foundational-regularity
- Count: 1
- bridge.012: st.def.generator -> st.prop.generator-closed-dense (score=0.4826)

### core-generation-theorem -> canonical-examples
- Count: 2
- bridge.015: st.thm.hille-yosida-general -> st.ex.translation-semigroup (score=0.4769)
- bridge.014: st.thm.hille-yosida-general -> st.ex.multiplication-semigroup (score=0.4695)

### foundational-definitions -> canonical-examples
- Count: 1
- bridge.010: st.def.c0-semigroup -> st.ex.heat-semigroup-lp (score=0.4484)

### foundational-definitions -> Constructive Models and Rigorous Existence Results
- Count: 1
- bridge.016: st.def.generator -> st.der.generator-uniqueness (score=0.4451)

### problem-semantics -> equivalent-characterizations
- Count: 1
- bridge.013: st.thm.cauchy-problem-equivalence -> st.thm.lumer-phillips (score=0.4391)

### core-generation-theorem -> proof-technology
- Count: 1
- bridge.023: st.thm.hille-yosida-general -> st.der.yosida-approximation (score=0.4007)

### foundational-regularity -> core-generation-theorem
- Count: 1
- bridge.022: st.prop.generator-closed-dense -> st.thm.hille-yosida-general (score=0.3948)

### core-generation-theorem -> equivalent-characterizations
- Count: 1
- bridge.025: st.thm.hille-yosida-general -> st.thm.lumer-phillips (score=0.3607)

### core-generation-theorem -> Constructive Models and Rigorous Existence Results
- Count: 1
- bridge.031: st.thm.hille-yosida-general -> st.der.generator-uniqueness (score=0.3353)

## Recommended Run Order

1. bridge.002
2. bridge.003
3. bridge.001
4. bridge.009
5. bridge.004
6. bridge.011
