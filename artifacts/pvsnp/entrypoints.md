# Conceptual Entry Points

## Stats

- Statements analyzed: 64
- Ranked entry points: 20
- Connector interventions used: 20
- Connector links used: 40
- Proof hypotheses used: 44
- Coherence signals used: 44

## Top Entry Points

| rank | statement_id | kind | phase | entry_score | hyp_count | bridge_count |
|---|---|---|---|---|---|---|
| 1 | st.def.item-2 | definition | 1) Foundational language of complexity | 0.6197 | 12 | 8 |
| 2 | st.def.item-3 | definition | 1) Foundational language of complexity | 0.5708 | 7 | 7 |
| 3 | st.def.item | definition | 1) Foundational language of complexity | 0.5626 | 8 | 6 |
| 4 | st.def.polynomially-bounded-proof-system | definition | Paragraph: Proof complexity. | 0.5191 | 5 | 2 |
| 5 | st.def.np-completeness | definition | 1) Foundational language of complexity | 0.5138 | 4 | 5 |
| 6 | st.def.polynomial-time-many-one-karp-reduction | definition | 1) Foundational language of complexity | 0.5094 | 4 | 7 |
| 7 | st.def.exponential-time-classes | definition | 1) Foundational language of complexity | 0.4917 | 6 | 7 |
| 8 | st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | theorem | 8) Proof complexity as a parallel route | 0.4901 | 5 | 2 |
| 9 | st.def.polynomial-hierarchy | definition | 1) Foundational language of complexity | 0.4852 | 5 | 6 |
| 10 | st.def.item-4 | definition | 1) Foundational language of complexity | 0.4765 | 5 | 5 |
| 11 | st.def.cook-reckhow-propositional-proof-system | definition | Paragraph: Proof complexity. | 0.4369 | 5 | 2 |
| 12 | st.def.deterministic-decision-tree-complexity | definition | 10) Communication/lifting unification layer | 0.4204 | 3 | 1 |
| 13 | st.thm.cook-levin-sat-is-np-complete-cook1971 | theorem | 2) First major milestone: NP-completeness landscape | 0.4163 | 2 | 3 |
| 14 | st.def.deterministic-communication-complexity | definition | 10) Communication/lifting unification layer | 0.4045 | 3 | 1 |
| 15 | st.def.relativising-proof-technique-informal | definition | Paragraph: Barrier notions. | 0.3966 | 1 | 1 |
| 16 | st.def.algebrising-proof-technique-informal | definition | Paragraph: Barrier notions. | 0.3128 | 1 | 1 |
| 17 | st.thm.karp-many-natural-problems-are-np-complete-karp1 | theorem | 2) First major milestone: NP-completeness landscape | 0.2349 | 0 | 4 |
| 18 | st.thm.bounded-depth-frege-php-lower-bounds-beamepitass | theorem | 8) Proof complexity as a parallel route | 0.2085 | 0 | 0 |
| 19 | st.thm.resolution-php-lower-bounds-exemplar-buss1988 | theorem | 8) Proof complexity as a parallel route | 0.1995 | 0 | 0 |
| 20 | st.thm.oliveira-santhanam-hardness-magnification-for-na | theorem | 9) Meta-complexity and hardness magnification phase | 0.1957 | 0 | 0 |

## Concept Tracks

### 1) Foundational language of complexity
- `st.def.item-2` (definition), score=0.6197
- `st.def.item-3` (definition), score=0.5708
- `st.def.item` (definition), score=0.5626

### Paragraph: Proof complexity.
- `st.def.polynomially-bounded-proof-system` (definition), score=0.5191
- `st.def.cook-reckhow-propositional-proof-system` (definition), score=0.4369

### 8) Proof complexity as a parallel route
- `st.thm.cook-reckhow-proof-systems-and-cookreckhow1979` (theorem), score=0.4901
- `st.thm.bounded-depth-frege-php-lower-bounds-beamepitass` (theorem), score=0.2085
- `st.thm.resolution-php-lower-bounds-exemplar-buss1988` (theorem), score=0.1995

### 10) Communication/lifting unification layer
- `st.def.deterministic-decision-tree-complexity` (definition), score=0.4204
- `st.def.deterministic-communication-complexity` (definition), score=0.4045

### 2) First major milestone: NP-completeness landscape
- `st.thm.cook-levin-sat-is-np-complete-cook1971` (theorem), score=0.4163
- `st.thm.karp-many-natural-problems-are-np-complete-karp1` (theorem), score=0.2349

### Paragraph: Barrier notions.
- `st.def.relativising-proof-technique-informal` (definition), score=0.3966
- `st.def.algebrising-proof-technique-informal` (definition), score=0.3128

### 9) Meta-complexity and hardness magnification phase
- `st.thm.oliveira-santhanam-hardness-magnification-for-na` (theorem), score=0.1957

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
