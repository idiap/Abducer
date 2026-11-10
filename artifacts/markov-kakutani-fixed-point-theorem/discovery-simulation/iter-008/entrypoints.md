# Conceptual Entry Points

## Stats

- Statements analyzed: 8
- Ranked entry points: 8
- Connector interventions used: 8
- Connector links used: 28
- Proof hypotheses used: 40
- Coherence signals used: 40

## Top Entry Points

| rank | statement_id | kind | phase | entry_score | concepts | hyp_count | bridge_count |
|---|---|---|---|---|---|---|---|
| 1 | st.thm.markov-kakutani | theorem | Active Fixed-Point Bridge Agenda | 0.8496 | finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset | 15 | 7 |
| 2 | st.lem.finite-family-common-fixed-point | lemma | Active Fixed-Point Bridge Agenda | 0.779 | finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, common-fixed-point-for-finite-commuting-family | 6 | 7 |
| 3 | st.lem.single-map-fixed-point | lemma | Active Fixed-Point Bridge Agenda | 0.7758 | single-map-fixed-point-implies-invariant-fixed-point-subset, finite-intersection-property-implies-common-fixed-point, continuous-affine-self-map-on-compact-convex-set, commuting-affine-family-on-compact-convex-set | 11 | 7 |
| 4 | st.prop.fixed-point-subset-structure | proposition | Active Fixed-Point Bridge Agenda | 0.6916 | single-map-fixed-point-implies-invariant-fixed-point-subset, single-affine-self-map-on-compact-convex-set, single-affine-self-map-with-fixed-point, nonempty-compact-convex-subset | 7 | 7 |
| 5 | st.lem.cesaro-averages | lemma | Active Fixed-Point Bridge Agenda | 0.6702 | affine-averaging-implies-single-map-fixed-point, continuous-affine-self-map-on-compact-convex-set, nonempty-compact-convex-subset, affine-orbit-averages-in-compact-convex-set | 7 | 7 |
| 6 | st.def.compact-convex-set | definition | Foundational Definitions | 0.5829 | nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset, locally-convex-topological-vector-space | 13 | 7 |
| 7 | st.ex.interval-commuting-projections | example | Active Fixed-Point Bridge Agenda | 0.5676 | finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset | 6 | 7 |
| 8 | st.lem.commuting-preserves-fixed-point-subset | lemma | Commuting Invariance | 0.5331 | commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, invariant-fixed-point-subset, invariant-fixed-point-subset-definition | 7 | 7 |

## Concept Tracks

### Active Fixed-Point Bridge Agenda
- `st.thm.markov-kakutani` (theorem), score=0.8496
- `st.lem.finite-family-common-fixed-point` (lemma), score=0.779
- `st.lem.single-map-fixed-point` (lemma), score=0.7758

### Foundational Definitions
- `st.def.compact-convex-set` (definition), score=0.5829

### Commuting Invariance
- `st.lem.commuting-preserves-fixed-point-subset` (lemma), score=0.5331

## Tactical Next Step

Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.
