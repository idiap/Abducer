# Essential Concept Bridge Plan

## Stats

- Input connection candidates: 40
- Bridge programs: 20
- Concept axes: 5

## Top Bridge Programs

| bridge_id | from_id | to_id | type | tier | score | expl | coh |
|---|---|---|---|---|---|---|---|
| bridge.001 | st.def.item | st.def.item-2 | structural support bridge | B | 0.5345 | 0.5691 | 0.0063 |
| bridge.005 | st.def.item-2 | st.def.item-4 | structural support bridge | B | 0.5221 | 0.5571 | 0.0063 |
| bridge.009 | st.def.item-2 | st.def.polynomial-time-many-one-karp-reduction | structural support bridge | B | 0.52 | 0.5551 | 0.0063 |
| bridge.011 | st.def.item-2 | st.def.polynomial-hierarchy | structural support bridge | B | 0.5164 | 0.5515 | 0.0062 |
| bridge.002 | st.def.item | st.def.item-4 | structural support bridge | B | 0.5157 | 0.5647 | 0.0063 |
| bridge.012 | st.def.item-2 | st.def.item-3 | structural support bridge | B | 0.5141 | 0.5494 | 0.0062 |
| bridge.006 | st.def.exponential-time-classes | st.def.item-3 | structural support bridge | B | 0.5086 | 0.5567 | 0.0063 |
| bridge.003 | st.def.polynomially-bounded-proof-system | st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | proof-complexity bridge | B | 0.5023 | 0.5631 | 0.0035 |
| bridge.015 | st.def.exponential-time-classes | st.def.item-2 | structural support bridge | B | 0.4984 | 0.4552 | 0.0062 |
| bridge.010 | st.def.cook-reckhow-propositional-proof-system | st.def.polynomially-bounded-proof-system | proof-complexity bridge | B | 0.4916 | 0.5517 | 0.0146 |
| bridge.004 | st.def.cook-reckhow-propositional-proof-system | st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | proof-complexity bridge | B | 0.4911 | 0.5589 | 0.0035 |
| bridge.007 | st.def.np-completeness | st.thm.cook-levin-sat-is-np-complete-cook1971 | structural support bridge | B | 0.4898 | 0.5556 | 0.0062 |
| bridge.014 | st.def.item | st.def.polynomial-hierarchy | structural support bridge | B | 0.4843 | 0.4555 | 0.0062 |
| bridge.017 | st.def.item-3 | st.def.np-completeness | structural support bridge | B | 0.4833 | 0.4534 | 0.0062 |
| bridge.016 | st.def.item | st.def.polynomial-time-many-one-karp-reduction | structural support bridge | B | 0.4825 | 0.4536 | 0.0062 |
| bridge.019 | st.def.exponential-time-classes | st.def.item | structural support bridge | B | 0.4801 | 0.45 | 0.0173 |
| bridge.020 | st.def.item-3 | st.def.polynomial-hierarchy | structural support bridge | B | 0.4773 | 0.4472 | 0.0062 |
| bridge.018 | st.def.exponential-time-classes | st.def.np-completeness | structural support bridge | B | 0.466 | 0.4511 | 0.0062 |
| bridge.008 | st.def.deterministic-communication-complexity | st.def.deterministic-decision-tree-complexity | lifting bridge | C | 0.421 | 0.5553 | 0.0146 |
| bridge.029 | st.def.item-2 | st.thm.karp-many-natural-problems-are-np-complete-karp1 | structural support bridge | C | 0.4068 | 0.2891 | 0.0 |

## Bridge Axes

### 1) Foundational language of complexity -> 1) Foundational language of complexity
- Count: 14
- bridge.001: st.def.item -> st.def.item-2 (score=0.5345)
- bridge.005: st.def.item-2 -> st.def.item-4 (score=0.5221)
- bridge.009: st.def.item-2 -> st.def.polynomial-time-many-one-karp-reduction (score=0.52)

### Unspecified -> 8) Proof complexity as a parallel route
- Count: 2
- bridge.003: st.def.polynomially-bounded-proof-system -> st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 (score=0.5023)
- bridge.004: st.def.cook-reckhow-propositional-proof-system -> st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 (score=0.4911)

### Unspecified -> Unspecified
- Count: 1
- bridge.010: st.def.cook-reckhow-propositional-proof-system -> st.def.polynomially-bounded-proof-system (score=0.4916)

### 1) Foundational language of complexity -> 2) First major milestone: NP-completeness landscape
- Count: 2
- bridge.007: st.def.np-completeness -> st.thm.cook-levin-sat-is-np-complete-cook1971 (score=0.4898)
- bridge.029: st.def.item-2 -> st.thm.karp-many-natural-problems-are-np-complete-karp1 (score=0.4068)

### 10) Communication/lifting unification layer -> 10) Communication/lifting unification layer
- Count: 1
- bridge.008: st.def.deterministic-communication-complexity -> st.def.deterministic-decision-tree-complexity (score=0.421)

## Recommended Run Order

1. bridge.001
2. bridge.005
3. bridge.009
4. bridge.011
5. bridge.002
6. bridge.012
