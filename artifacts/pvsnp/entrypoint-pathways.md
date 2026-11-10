# Entry Point Pathways

## Stats

- Pathways: 8
- Entry points considered: 8

## Ranked Pathways

### path.001 - st.def.item-2
- Rank: 1
- Phase: 1) Foundational language of complexity
- Entry score: 0.6197
- Pathway score: 0.6025
- Goal: Develop a proof pathway centered on st.def.item-2.
- Supporting hypotheses:
  - phyp.p-vs-np.001 (bridge-link, priority=0.6201)
  - phyp.p-vs-np.005 (bridge-link, priority=0.5986)
  - phyp.p-vs-np.009 (bridge-link, priority=0.5949)
  - phyp.p-vs-np.033 (definition-introduction, priority=0.5939)
- Supporting links:
  - st.def.item -> st.def.item-2 (score=0.5779)
  - st.def.item-2 -> st.def.item-4 (score=0.554)
  - st.def.item-2 -> st.def.polynomial-time-many-one-karp-reduction (score=0.5499)
- Execution plan:
  - Run kb-abduce on target st.def.item-2 using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.item-2 in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.003 - st.def.item
- Rank: 3
- Phase: 1) Foundational language of complexity
- Entry score: 0.5626
- Pathway score: 0.5744
- Goal: Develop a proof pathway centered on st.def.item.
- Supporting hypotheses:
  - phyp.p-vs-np.001 (bridge-link, priority=0.6201)
  - phyp.p-vs-np.002 (bridge-link, priority=0.6123)
  - phyp.p-vs-np.033 (definition-introduction, priority=0.5939)
  - phyp.p-vs-np.034 (definition-introduction, priority=0.5867)
- Supporting links:
  - st.def.item -> st.def.item-2 (score=0.5779)
  - st.def.item -> st.def.item-4 (score=0.5692)
  - st.def.item -> st.def.polynomial-hierarchy (score=0.5351)
- Execution plan:
  - Run kb-abduce on target st.def.item using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.item in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.002 - st.def.item-3
- Rank: 2
- Phase: 1) Foundational language of complexity
- Entry score: 0.5708
- Pathway score: 0.5686
- Goal: Develop a proof pathway centered on st.def.item-3.
- Supporting hypotheses:
  - phyp.p-vs-np.006 (bridge-link, priority=0.5979)
  - phyp.p-vs-np.012 (bridge-link, priority=0.5846)
  - phyp.p-vs-np.017 (bridge-link, priority=0.578)
  - phyp.p-vs-np.038 (definition-introduction, priority=0.5736)
- Supporting links:
  - st.def.exponential-time-classes -> st.def.item-3 (score=0.5532)
  - st.def.item-2 -> st.def.item-3 (score=0.5384)
  - st.def.item-3 -> st.def.np-completeness (score=0.5311)
- Execution plan:
  - Run kb-abduce on target st.def.item-3 using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.item-3 in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.004 - st.def.polynomially-bounded-proof-system
- Rank: 4
- Phase: Paragraph: Proof complexity.
- Entry score: 0.5191
- Pathway score: 0.5465
- Goal: Develop a proof pathway centered on st.def.polynomially-bounded-proof-system.
- Supporting hypotheses:
  - phyp.p-vs-np.003 (bridge-link, priority=0.6094)
  - phyp.p-vs-np.010 (bridge-link, priority=0.5887)
  - phyp.p-vs-np.035 (definition-introduction, priority=0.5841)
  - phyp.p-vs-np.042 (definition-introduction, priority=0.5653)
- Supporting links:
  - st.def.polynomially-bounded-proof-system -> st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 (score=0.566)
  - st.def.cook-reckhow-propositional-proof-system -> st.def.polynomially-bounded-proof-system (score=0.543)
- Execution plan:
  - Run kb-abduce on target st.def.polynomially-bounded-proof-system using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.polynomially-bounded-proof-system in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.008 - st.thm.cook-reckhow-proof-systems-and-cookreckhow1979
- Rank: 8
- Phase: 8) Proof complexity as a parallel route
- Entry score: 0.4901
- Pathway score: 0.5353
- Goal: Develop a proof pathway centered on st.thm.cook-reckhow-proof-systems-and-cookreckhow1979.
- Supporting hypotheses:
  - phyp.p-vs-np.003 (bridge-link, priority=0.6094)
  - phyp.p-vs-np.004 (bridge-link, priority=0.6018)
  - phyp.p-vs-np.035 (definition-introduction, priority=0.5841)
  - phyp.p-vs-np.036 (definition-introduction, priority=0.5772)
- Supporting links:
  - st.def.polynomially-bounded-proof-system -> st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 (score=0.566)
  - st.def.cook-reckhow-propositional-proof-system -> st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 (score=0.5576)
- Execution plan:
  - Run kb-abduce on target st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.005 - st.def.np-completeness
- Rank: 5
- Phase: 1) Foundational language of complexity
- Entry score: 0.5138
- Pathway score: 0.5307
- Goal: Develop a proof pathway centered on st.def.np-completeness.
- Supporting hypotheses:
  - phyp.p-vs-np.017 (bridge-link, priority=0.578)
  - phyp.p-vs-np.018 (bridge-link, priority=0.5742)
  - phyp.p-vs-np.039 (definition-introduction, priority=0.5718)
  - phyp.p-vs-np.007 (bridge-link, priority=0.4959)
- Supporting links:
  - st.def.np-completeness -> st.thm.cook-levin-sat-is-np-complete-cook1971 (score=0.551)
  - st.def.item-3 -> st.def.np-completeness (score=0.5311)
  - st.def.exponential-time-classes -> st.def.np-completeness (score=0.5269)
- Execution plan:
  - Run kb-abduce on target st.def.np-completeness using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.np-completeness in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.007 - st.def.exponential-time-classes
- Rank: 7
- Phase: 1) Foundational language of complexity
- Entry score: 0.4917
- Pathway score: 0.528
- Goal: Develop a proof pathway centered on st.def.exponential-time-classes.
- Supporting hypotheses:
  - phyp.p-vs-np.006 (bridge-link, priority=0.5979)
  - phyp.p-vs-np.015 (bridge-link, priority=0.5812)
  - phyp.p-vs-np.018 (bridge-link, priority=0.5742)
  - phyp.p-vs-np.038 (definition-introduction, priority=0.5736)
- Supporting links:
  - st.def.exponential-time-classes -> st.def.item-3 (score=0.5532)
  - st.def.exponential-time-classes -> st.def.item-2 (score=0.5347)
  - st.def.exponential-time-classes -> st.def.np-completeness (score=0.5269)
- Execution plan:
  - Run kb-abduce on target st.def.exponential-time-classes using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.exponential-time-classes in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.006 - st.def.polynomial-time-many-one-karp-reduction
- Rank: 6
- Phase: 1) Foundational language of complexity
- Entry score: 0.5094
- Pathway score: 0.513
- Goal: Develop a proof pathway centered on st.def.polynomial-time-many-one-karp-reduction.
- Supporting hypotheses:
  - phyp.p-vs-np.009 (bridge-link, priority=0.5949)
  - phyp.p-vs-np.016 (bridge-link, priority=0.5784)
  - phyp.p-vs-np.041 (definition-introduction, priority=0.5709)
  - phyp.p-vs-np.026 (intervention-focus, priority=0.2795)
- Supporting links:
  - st.def.item-2 -> st.def.polynomial-time-many-one-karp-reduction (score=0.5499)
  - st.def.item -> st.def.polynomial-time-many-one-karp-reduction (score=0.5316)
  - st.def.item-4 -> st.def.polynomial-time-many-one-karp-reduction (score=0.5163)
- Execution plan:
  - Run kb-abduce on target st.def.polynomial-time-many-one-karp-reduction using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.polynomial-time-many-one-karp-reduction in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.
