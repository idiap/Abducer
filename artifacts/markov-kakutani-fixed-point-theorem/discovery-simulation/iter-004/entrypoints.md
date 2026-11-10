# Conceptual Entry Points

## Stats

- Statements analyzed: 8
- Ranked entry points: 8
- Connector interventions used: 8
- Connector links used: 28
- Proof hypotheses used: 54
- Coherence signals used: 54

## Top Entry Points

| rank | statement_id | kind | phase | entry_score | concepts | hyp_count | bridge_count |
|---|---|---|---|---|---|---|---|
| 1 | st.thm.markov-kakutani | theorem | Active Fixed-Point Bridge Agenda | 0.8496 | finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset | 15 | 7 |
| 2 | st.lem.finite-family-common-fixed-point | lemma | Active Fixed-Point Bridge Agenda | 0.7924 | finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, common-fixed-point-for-finite-commuting-family | 12 | 7 |
| 3 | st.lem.single-map-fixed-point | lemma | Active Fixed-Point Bridge Agenda | 0.7758 | single-map-fixed-point-implies-invariant-fixed-point-subset, finite-intersection-property-implies-common-fixed-point, continuous-affine-self-map-on-compact-convex-set, commuting-affine-family-on-compact-convex-set | 14 | 7 |
| 4 | st.prop.fixed-point-subset-structure | proposition | Active Fixed-Point Bridge Agenda | 0.7058 | single-map-fixed-point-implies-invariant-fixed-point-subset, single-affine-self-map-on-compact-convex-set, single-affine-self-map-with-fixed-point, nonempty-compact-convex-subset | 11 | 7 |
| 5 | st.lem.cesaro-averages | lemma | Active Fixed-Point Bridge Agenda | 0.6701 | affine-averaging-implies-single-map-fixed-point, continuous-affine-self-map-on-compact-convex-set, nonempty-compact-convex-subset, affine-orbit-averages-in-compact-convex-set | 11 | 7 |
| 6 | st.def.compact-convex-set | definition | Foundational Definitions | 0.5829 | nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset, locally-convex-topological-vector-space | 15 | 7 |
| 7 | st.ex.interval-commuting-projections | example | Active Fixed-Point Bridge Agenda | 0.5676 | finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset | 11 | 7 |
| 8 | st.lem.commuting-preserves-fixed-point-subset | lemma | Commuting Invariance | 0.5381 | commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, invariant-fixed-point-subset, invariant-fixed-point-subset-definition | 11 | 7 |

## Concept Tracks

### Active Fixed-Point Bridge Agenda
- `st.thm.markov-kakutani` (theorem), score=0.8496
- `st.lem.finite-family-common-fixed-point` (lemma), score=0.7924
- `st.lem.single-map-fixed-point` (lemma), score=0.7758

### Foundational Definitions
- `st.def.compact-convex-set` (definition), score=0.5829

### Commuting Invariance
- `st.lem.commuting-preserves-fixed-point-subset` (lemma), score=0.5381

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
