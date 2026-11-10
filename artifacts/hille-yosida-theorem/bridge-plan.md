# Essential Concept Bridge Plan

## Stats

- Input connection candidates: 40
- Bridge programs: 20
- Concept axes: 10

## Top Bridge Programs

| bridge_id | from_id | to_id | type | tier | score | expl | coh | concept | commit | concept_evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| bridge.009 | st.thm.hille-yosida-general | st.thm.hille-yosida-contraction | structural support bridge | B | 0.4999 | 0.5103 | 0.0068 | 0.564 | 1.0 | group-theoretic-structure, resolvent-estimate, equivalence-schema, equivalence |
| bridge.003 | st.def.c0-semigroup | st.thm.hille-yosida-general | structural support bridge | B | 0.4852 | 0.5697 | 0.007 | 0.2033 | 0.75 | group-theoretic-structure, operator-theoretic-model, laplace-transform |
| bridge.004 | st.def.generator | st.thm.hille-yosida-general | structural support bridge | B | 0.4734 | 0.5829 | 0.0069 | 0.1222 | 0.75 | group-theoretic-structure, laplace-transform |
| bridge.001 | st.def.c0-semigroup | st.thm.cauchy-problem-equivalence | structural support bridge | B | 0.4674 | 0.5288 | 0.0071 | 0.246 | 0.6 | group-theoretic-structure, operator-theoretic-model, laplace-transform |
| bridge.019 | st.thm.hille-yosida-general | st.thm.cauchy-problem-equivalence | structural support bridge | B | 0.4617 | 0.3916 | 0.0067 | 0.484 | 1.0 | group-theoretic-structure, operator-theoretic-model, laplace-transform, equivalence |
| bridge.010 | st.def.resolvent | st.thm.hille-yosida-general | structural support bridge | C | 0.4464 | 0.5316 | 0.0068 | 0.1222 | 0.75 | operator-theoretic-model, resolvent-estimate |
| bridge.002 | st.def.generator | st.thm.cauchy-problem-equivalence | structural support bridge | C | 0.4375 | 0.5085 | 0.007 | 0.164 | 0.6 | group-theoretic-structure, laplace-transform |
| bridge.007 | st.def.generator | st.prop.generator-closed-dense | structural support bridge | C | 0.4279 | 0.5988 | 0.0068 | 0.245 | 0.5 | group-theoretic-structure, laplace-transform |
| bridge.005 | st.def.c0-semigroup | st.def.generator | structural support bridge | C | 0.4267 | 0.6255 | 0.0069 | 0.1667 | 0.35 | group-theoretic-structure, laplace-transform |
| bridge.016 | st.thm.cauchy-problem-equivalence | st.thm.lumer-phillips | proof-complexity bridge | C | 0.4163 | 0.4209 | 0.0068 | 0.5444 | 1.0 | group-theoretic-structure, operator-theoretic-model, unconditional, equivalence |
| bridge.006 | st.def.c0-semigroup | st.thm.lumer-phillips | proof-complexity bridge | C | 0.4162 | 0.3878 | 0.0069 | 0.1622 | 0.75 | group-theoretic-structure, operator-theoretic-model |
| bridge.014 | st.def.generator | st.ex.translation-semigroup | structural support bridge | C | 0.4027 | 0.4678 | 0.0068 | 0.245 | 0.6 | group-theoretic-structure, laplace-transform |
| bridge.015 | st.def.c0-semigroup | st.ex.translation-semigroup | structural support bridge | C | 0.3961 | 0.4337 | 0.0068 | 0.164 | 0.6 | group-theoretic-structure, laplace-transform |
| bridge.011 | st.def.c0-semigroup | st.thm.hille-yosida-contraction | structural support bridge | C | 0.3936 | 0.4187 | 0.0068 | 0.0814 | 0.6 | group-theoretic-structure |
| bridge.018 | st.def.generator | st.ex.heat-semigroup-lp | structural support bridge | C | 0.3914 | 0.4735 | 0.0068 | 0.204 | 0.5 | group-theoretic-structure, laplace-transform |
| bridge.017 | st.def.c0-semigroup | st.prop.generator-closed-dense | structural support bridge | C | 0.3905 | 0.4401 | 0.0068 | 0.164 | 0.5 | group-theoretic-structure, laplace-transform |
| bridge.012 | st.def.generator | st.thm.hille-yosida-contraction | structural support bridge | C | 0.3884 | 0.3811 | 0.0068 | 0.1617 | 0.6 | group-theoretic-structure |
| bridge.020 | st.def.c0-semigroup | st.ex.multiplication-semigroup | structural support bridge | C | 0.3773 | 0.4322 | 0.0067 | 0.165 | 0.35 | group-theoretic-structure, operator-theoretic-model |
| bridge.021 | st.thm.hille-yosida-general | st.thm.lumer-phillips | proof-complexity bridge | C | 0.3741 | 0.3633 | 0.0 | 0.6175 | 0.0 | group-theoretic-structure, operator-theoretic-model, equivalence-schema, equivalence |
| bridge.013 | st.def.generator | st.thm.lumer-phillips | proof-complexity bridge | C | 0.3735 | 0.2702 | 0.0068 | 0.0811 | 0.75 | group-theoretic-structure |

## Mathematical Commitments

### bridge.009 (st.thm.hille-yosida-general -> st.thm.hille-yosida-contraction)
- Antecedent schema: equivalence-schema
- Target consequence: equivalence
- Preserved invariant: consequence schema equivalence
- Barrier scope: barrier + powers-of-resolvent-verification
- Invariant basis: equivalence, group-theoretic-structure, equivalence-schema, equivalence

### bridge.003 (st.def.c0-semigroup -> st.thm.hille-yosida-general)
- Antecedent schema: unconditional
- Target consequence: equivalence
- Preserved invariant: group-theoretic-structure mathematical structure
- Barrier scope: barrier + powers-of-resolvent-verification
- Invariant basis: group-theoretic-structure, group-theoretic-structure, operator-theoretic-model

### bridge.004 (st.def.generator -> st.thm.hille-yosida-general)
- Antecedent schema: unconditional
- Target consequence: equivalence
- Preserved invariant: group-theoretic-structure mathematical structure
- Barrier scope: barrier + powers-of-resolvent-verification
- Invariant basis: group-theoretic-structure, group-theoretic-structure

### bridge.001 (st.def.c0-semigroup -> st.thm.cauchy-problem-equivalence)
- Antecedent schema: unconditional
- Target consequence: equivalence
- Preserved invariant: group-theoretic-structure mathematical structure
- Barrier scope: none
- Invariant basis: group-theoretic-structure, group-theoretic-structure, operator-theoretic-model

### bridge.019 (st.thm.hille-yosida-general -> st.thm.cauchy-problem-equivalence)
- Antecedent schema: equivalence
- Target consequence: equivalence
- Preserved invariant: consequence schema equivalence
- Barrier scope: barrier + powers-of-resolvent-verification
- Invariant basis: equivalence, group-theoretic-structure, operator-theoretic-model, equivalence

### bridge.010 (st.def.resolvent -> st.thm.hille-yosida-general)
- Antecedent schema: unconditional
- Target consequence: equivalence
- Preserved invariant: operator-theoretic-model mathematical structure
- Barrier scope: barrier + powers-of-resolvent-verification
- Invariant basis: operator-theoretic-model, operator-theoretic-model

### bridge.002 (st.def.generator -> st.thm.cauchy-problem-equivalence)
- Antecedent schema: unconditional
- Target consequence: equivalence
- Preserved invariant: group-theoretic-structure mathematical structure
- Barrier scope: none
- Invariant basis: group-theoretic-structure, group-theoretic-structure

### bridge.007 (st.def.generator -> st.prop.generator-closed-dense)
- Antecedent schema: unconditional
- Target consequence: statement-conclusion
- Preserved invariant: group-theoretic-structure mathematical structure
- Barrier scope: barrier + domain-regularity
- Invariant basis: group-theoretic-structure, group-theoretic-structure

### bridge.005 (st.def.c0-semigroup -> st.def.generator)
- Antecedent schema: unconditional
- Target consequence: statement-conclusion
- Preserved invariant: group-theoretic-structure mathematical structure
- Barrier scope: none
- Invariant basis: group-theoretic-structure, group-theoretic-structure

### bridge.016 (st.thm.cauchy-problem-equivalence -> st.thm.lumer-phillips)
- Antecedent schema: equivalence
- Target consequence: equivalence
- Preserved invariant: consequence schema equivalence
- Barrier scope: barrier + domain-closure-density
- Invariant basis: equivalence, group-theoretic-structure, operator-theoretic-model, unconditional, equivalence

## Bridge Axes

### core-generation-theorem -> core-generation-theorem
- Count: 1
- bridge.009: st.thm.hille-yosida-general -> st.thm.hille-yosida-contraction (score=0.4999)

### foundational-definitions -> core-generation-theorem
- Count: 5
- bridge.003: st.def.c0-semigroup -> st.thm.hille-yosida-general (score=0.4852)
- bridge.004: st.def.generator -> st.thm.hille-yosida-general (score=0.4734)
- bridge.010: st.def.resolvent -> st.thm.hille-yosida-general (score=0.4464)

### foundational-definitions -> problem-semantics
- Count: 2
- bridge.001: st.def.c0-semigroup -> st.thm.cauchy-problem-equivalence (score=0.4674)
- bridge.002: st.def.generator -> st.thm.cauchy-problem-equivalence (score=0.4375)

### problem-semantics -> core-generation-theorem
- Count: 1
- bridge.019: st.thm.hille-yosida-general -> st.thm.cauchy-problem-equivalence (score=0.4617)

### foundational-definitions -> foundational-regularity
- Count: 2
- bridge.007: st.def.generator -> st.prop.generator-closed-dense (score=0.4279)
- bridge.017: st.def.c0-semigroup -> st.prop.generator-closed-dense (score=0.3905)

### foundational-definitions -> foundational-definitions
- Count: 1
- bridge.005: st.def.c0-semigroup -> st.def.generator (score=0.4267)

### problem-semantics -> equivalent-characterizations
- Count: 1
- bridge.016: st.thm.cauchy-problem-equivalence -> st.thm.lumer-phillips (score=0.4163)

### foundational-definitions -> equivalent-characterizations
- Count: 2
- bridge.006: st.def.c0-semigroup -> st.thm.lumer-phillips (score=0.4162)
- bridge.013: st.def.generator -> st.thm.lumer-phillips (score=0.3735)

### foundational-definitions -> canonical-examples
- Count: 4
- bridge.014: st.def.generator -> st.ex.translation-semigroup (score=0.4027)
- bridge.015: st.def.c0-semigroup -> st.ex.translation-semigroup (score=0.3961)
- bridge.018: st.def.generator -> st.ex.heat-semigroup-lp (score=0.3914)

### core-generation-theorem -> equivalent-characterizations
- Count: 1
- bridge.021: st.thm.hille-yosida-general -> st.thm.lumer-phillips (score=0.3741)

## Recommended Run Order

1. bridge.009
2. bridge.003
3. bridge.004
4. bridge.001
5. bridge.019
6. bridge.010
