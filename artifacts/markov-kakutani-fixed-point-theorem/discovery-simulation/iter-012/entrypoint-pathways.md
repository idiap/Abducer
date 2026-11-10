# Entry Point Pathways

## Stats

- Pathways: 8
- Entry points considered: 8

## Ranked Pathways

### path.001 - st.thm.markov-kakutani
- Rank: 1
- Phase: Current Bridge Agenda
- Entry concepts: finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset, common-fixed-point-for-finite-commuting-family
- Entry score: 0.8167
- Pathway score: 0.6368
- Goal: Develop a proof pathway centered on st.thm.markov-kakutani.
- Supporting hypotheses:
  - phyp.markov-kakutani-fixed-point-theorem.018 (intervention-focus, priority=0.7649)
  - phyp.markov-kakutani-fixed-point-theorem.001 (bridge-link, priority=0.4624)
  - phyp.markov-kakutani-fixed-point-theorem.025 (barrier-escape-principle, priority=0.4502)
  - phyp.markov-kakutani-fixed-point-theorem.003 (bridge-link, priority=0.406)
- Supporting links:
  - st.def.compact-convex-set -> st.thm.markov-kakutani (score=0.4027)
  - st.lem.finite-family-common-fixed-point -> st.thm.markov-kakutani (score=0.34)
  - st.thm.markov-kakutani -> st.ex.interval-commuting-projections (score=0.34)
- Execution plan:
  - Run kb-abduce on target st.thm.markov-kakutani using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.markov-kakutani in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.003 - st.lem.single-map-fixed-point
- Rank: 3
- Phase: Current Bridge Agenda
- Entry concepts: single-map-fixed-point-implies-invariant-fixed-point-subset, finite-intersection-property-implies-common-fixed-point, continuous-affine-self-map-on-compact-convex-set, commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set
- Entry score: 0.7417
- Pathway score: 0.593
- Goal: Develop a proof pathway centered on st.lem.single-map-fixed-point.
- Supporting hypotheses:
  - phyp.markov-kakutani-fixed-point-theorem.017 (intervention-focus, priority=0.8448)
  - phyp.markov-kakutani-fixed-point-theorem.006 (bridge-link, priority=0.406)
  - phyp.markov-kakutani-fixed-point-theorem.008 (bridge-link, priority=0.406)
  - phyp.markov-kakutani-fixed-point-theorem.030 (barrier-escape-principle, priority=0.3988)
- Supporting links:
  - st.def.compact-convex-set -> st.lem.single-map-fixed-point (score=0.34)
  - st.lem.cesaro-averages -> st.lem.single-map-fixed-point (score=0.34)
  - st.lem.single-map-fixed-point -> st.prop.fixed-point-subset-structure (score=0.34)
- Execution plan:
  - Run kb-abduce on target st.lem.single-map-fixed-point using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.lem.single-map-fixed-point in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.002 - st.lem.finite-family-common-fixed-point
- Rank: 2
- Phase: Current Bridge Agenda
- Entry concepts: finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, common-fixed-point-for-finite-commuting-family, common-fixed-point-for-commuting-family
- Entry score: 0.746
- Pathway score: 0.5802
- Goal: Develop a proof pathway centered on st.lem.finite-family-common-fixed-point.
- Supporting hypotheses:
  - phyp.markov-kakutani-fixed-point-theorem.020 (intervention-focus, priority=0.7311)
  - phyp.markov-kakutani-fixed-point-theorem.003 (bridge-link, priority=0.406)
  - phyp.markov-kakutani-fixed-point-theorem.027 (barrier-escape-principle, priority=0.3988)
  - phyp.markov-kakutani-fixed-point-theorem.014 (bridge-link, priority=0.3201)
- Supporting links:
  - st.lem.finite-family-common-fixed-point -> st.thm.markov-kakutani (score=0.34)
  - st.lem.commuting-preserves-fixed-point-subset -> st.lem.finite-family-common-fixed-point (score=0.34)
  - st.prop.fixed-point-subset-structure -> st.lem.finite-family-common-fixed-point (score=0.34)
- Execution plan:
  - Run kb-abduce on target st.lem.finite-family-common-fixed-point using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.lem.finite-family-common-fixed-point in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.004 - st.prop.fixed-point-subset-structure
- Rank: 4
- Phase: Current Bridge Agenda
- Entry concepts: single-map-fixed-point-implies-invariant-fixed-point-subset, single-affine-self-map-on-compact-convex-set, single-affine-self-map-with-fixed-point, nonempty-compact-convex-subset, nonempty-compact-convex-fixed-point-subset
- Entry score: 0.6402
- Pathway score: 0.5296
- Goal: Develop a proof pathway centered on st.prop.fixed-point-subset-structure.
- Supporting hypotheses:
  - phyp.markov-kakutani-fixed-point-theorem.019 (intervention-focus, priority=0.7519)
  - phyp.markov-kakutani-fixed-point-theorem.011 (bridge-link, priority=0.3345)
  - phyp.markov-kakutani-fixed-point-theorem.012 (bridge-link, priority=0.3287)
- Supporting links:
  - st.lem.single-map-fixed-point -> st.prop.fixed-point-subset-structure (score=0.34)
  - st.prop.fixed-point-subset-structure -> st.lem.commuting-preserves-fixed-point-subset (score=0.34)
  - st.prop.fixed-point-subset-structure -> st.lem.finite-family-common-fixed-point (score=0.34)
- Execution plan:
  - Run kb-abduce on target st.prop.fixed-point-subset-structure using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.prop.fixed-point-subset-structure in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.005 - st.lem.cesaro-averages
- Rank: 5
- Phase: Current Bridge Agenda
- Entry concepts: affine-averaging-implies-single-map-fixed-point, continuous-affine-self-map-on-compact-convex-set, nonempty-compact-convex-subset, affine-orbit-averages-in-compact-convex-set, single-map-fixed-point
- Entry score: 0.6372
- Pathway score: 0.526
- Goal: Develop a proof pathway centered on st.lem.cesaro-averages.
- Supporting hypotheses:
  - phyp.markov-kakutani-fixed-point-theorem.021 (intervention-focus, priority=0.686)
  - phyp.markov-kakutani-fixed-point-theorem.004 (bridge-link, priority=0.406)
  - phyp.markov-kakutani-fixed-point-theorem.008 (bridge-link, priority=0.406)
  - phyp.markov-kakutani-fixed-point-theorem.028 (barrier-escape-principle, priority=0.3988)
- Supporting links:
  - st.def.compact-convex-set -> st.lem.cesaro-averages (score=0.34)
  - st.lem.cesaro-averages -> st.lem.single-map-fixed-point (score=0.34)
  - st.lem.cesaro-averages -> st.thm.markov-kakutani (score=0.2975)
- Execution plan:
  - Run kb-abduce on target st.lem.cesaro-averages using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.lem.cesaro-averages in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.006 - st.def.compact-convex-set
- Rank: 6
- Phase: Foundational Gauge-Theoretic Definitions
- Entry concepts: nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset, locally-convex-topological-vector-space, affine-self-map
- Entry score: 0.583
- Pathway score: 0.5066
- Goal: Develop a proof pathway centered on st.def.compact-convex-set.
- Supporting hypotheses:
  - phyp.markov-kakutani-fixed-point-theorem.023 (intervention-focus, priority=0.5874)
  - phyp.markov-kakutani-fixed-point-theorem.001 (bridge-link, priority=0.4624)
  - phyp.markov-kakutani-fixed-point-theorem.025 (barrier-escape-principle, priority=0.4502)
  - phyp.markov-kakutani-fixed-point-theorem.004 (bridge-link, priority=0.406)
- Supporting links:
  - st.def.compact-convex-set -> st.thm.markov-kakutani (score=0.4027)
  - st.def.compact-convex-set -> st.lem.cesaro-averages (score=0.34)
  - st.def.compact-convex-set -> st.lem.single-map-fixed-point (score=0.34)
- Execution plan:
  - Run kb-abduce on target st.def.compact-convex-set using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.compact-convex-set in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.007 - st.ex.interval-commuting-projections
- Rank: 7
- Phase: Current Bridge Agenda
- Entry concepts: finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset, common-fixed-point-for-finite-commuting-family
- Entry score: 0.5346
- Pathway score: 0.457
- Goal: Develop a proof pathway centered on st.ex.interval-commuting-projections.
- Supporting hypotheses:
  - phyp.markov-kakutani-fixed-point-theorem.022 (intervention-focus, priority=0.64)
  - phyp.markov-kakutani-fixed-point-theorem.007 (bridge-link, priority=0.406)
  - phyp.markov-kakutani-fixed-point-theorem.031 (barrier-escape-principle, priority=0.3988)
  - phyp.markov-kakutani-fixed-point-theorem.010 (bridge-link, priority=0.3356)
- Supporting links:
  - st.thm.markov-kakutani -> st.ex.interval-commuting-projections (score=0.34)
  - st.def.compact-convex-set -> st.ex.interval-commuting-projections (score=0.2618)
  - st.lem.single-map-fixed-point -> st.ex.interval-commuting-projections (score=0.241)
- Execution plan:
  - Run kb-abduce on target st.ex.interval-commuting-projections using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.ex.interval-commuting-projections in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.008 - st.lem.commuting-preserves-fixed-point-subset
- Rank: 8
- Phase: Additional KB-Specific Phases
- Entry concepts: commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, invariant-fixed-point-subset, invariant-fixed-point-subset-definition, commuting-affine-family-definition
- Entry score: 0.5092
- Pathway score: 0.4392
- Goal: Develop a proof pathway centered on st.lem.commuting-preserves-fixed-point-subset.
- Supporting hypotheses:
  - phyp.markov-kakutani-fixed-point-theorem.024 (intervention-focus, priority=0.5437)
  - phyp.markov-kakutani-fixed-point-theorem.009 (bridge-link, priority=0.3457)
  - phyp.markov-kakutani-fixed-point-theorem.013 (bridge-link, priority=0.3211)
- Supporting links:
  - st.lem.commuting-preserves-fixed-point-subset -> st.lem.finite-family-common-fixed-point (score=0.34)
  - st.prop.fixed-point-subset-structure -> st.lem.commuting-preserves-fixed-point-subset (score=0.34)
  - st.lem.commuting-preserves-fixed-point-subset -> st.thm.markov-kakutani (score=0.273)
- Execution plan:
  - Run kb-abduce on target st.lem.commuting-preserves-fixed-point-subset using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.lem.commuting-preserves-fixed-point-subset in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.
