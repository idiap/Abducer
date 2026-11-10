# Entry Point Pathways

## Stats

- Pathways: 8
- Entry points considered: 8

## Ranked Pathways

### path.001 - st.thm.hille-yosida-general
- Rank: 1
- Phase: Current Bridge Agenda
- Entry concepts: equivalence-schema, local-hypothesis-bundle, equivalence, group-theoretic-structure, operator-theoretic-model
- Entry score: 0.8
- Pathway score: 0.6385
- Goal: Develop a proof pathway centered on st.thm.hille-yosida-general.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.021 (intervention-focus, priority=0.8408)
  - phyp.hille-yosida-theorem.003 (bridge-link, priority=0.4589)
  - phyp.hille-yosida-theorem.035 (definition-introduction, priority=0.447)
  - phyp.hille-yosida-theorem.004 (bridge-link, priority=0.4406)
- Supporting links:
  - st.def.c0-semigroup -> st.thm.hille-yosida-general (score=0.3988)
  - st.def.generator -> st.thm.hille-yosida-general (score=0.3785)
  - st.thm.hille-yosida-general -> st.thm.hille-yosida-contraction (score=0.3398)
- Execution plan:
  - Run kb-abduce on target st.thm.hille-yosida-general using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.hille-yosida-general in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.002 - st.def.c0-semigroup
- Rank: 2
- Phase: Current Bridge Agenda
- Entry concepts: group-theoretic-structure, operator-theoretic-model, laplace-transform
- Entry score: 0.6886
- Pathway score: 0.5808
- Goal: Develop a proof pathway centered on st.def.c0-semigroup.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.022 (intervention-focus, priority=0.6274)
  - phyp.hille-yosida-theorem.001 (bridge-link, priority=0.5054)
  - phyp.hille-yosida-theorem.033 (definition-introduction, priority=0.4893)
  - phyp.hille-yosida-theorem.003 (bridge-link, priority=0.4589)
- Supporting links:
  - st.def.c0-semigroup -> st.thm.cauchy-problem-equivalence (score=0.4504)
  - st.def.c0-semigroup -> st.thm.hille-yosida-general (score=0.3988)
  - st.def.c0-semigroup -> st.def.generator (score=0.357)
- Execution plan:
  - Run kb-abduce on target st.def.c0-semigroup using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.c0-semigroup in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.003 - st.def.generator
- Rank: 3
- Phase: Current Bridge Agenda
- Entry concepts: group-theoretic-structure, laplace-transform
- Entry score: 0.6664
- Pathway score: 0.5545
- Goal: Develop a proof pathway centered on st.def.generator.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.025 (intervention-focus, priority=0.5676)
  - phyp.hille-yosida-theorem.002 (bridge-link, priority=0.4686)
  - phyp.hille-yosida-theorem.034 (definition-introduction, priority=0.4559)
  - phyp.hille-yosida-theorem.004 (bridge-link, priority=0.4406)
- Supporting links:
  - st.def.generator -> st.thm.cauchy-problem-equivalence (score=0.4096)
  - st.def.generator -> st.thm.hille-yosida-general (score=0.3785)
  - st.def.c0-semigroup -> st.def.generator (score=0.357)
- Execution plan:
  - Run kb-abduce on target st.def.generator using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.generator in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.004 - st.thm.cauchy-problem-equivalence
- Rank: 4
- Phase: Current Bridge Agenda
- Entry concepts: unconditional, equivalence, group-theoretic-structure, operator-theoretic-model, laplace-transform
- Entry score: 0.5455
- Pathway score: 0.4996
- Goal: Develop a proof pathway centered on st.thm.cauchy-problem-equivalence.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.026 (intervention-focus, priority=0.5265)
  - phyp.hille-yosida-theorem.001 (bridge-link, priority=0.5054)
  - phyp.hille-yosida-theorem.033 (definition-introduction, priority=0.4893)
  - phyp.hille-yosida-theorem.002 (bridge-link, priority=0.4686)
- Supporting links:
  - st.def.c0-semigroup -> st.thm.cauchy-problem-equivalence (score=0.4504)
  - st.def.generator -> st.thm.cauchy-problem-equivalence (score=0.4096)
  - st.thm.cauchy-problem-equivalence -> st.thm.lumer-phillips (score=0.304)
- Execution plan:
  - Run kb-abduce on target st.thm.cauchy-problem-equivalence using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.cauchy-problem-equivalence in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.005 - st.thm.hille-yosida-contraction
- Rank: 5
- Phase: Current Bridge Agenda
- Entry concepts: equivalence-schema, unconditional, equivalence, group-theoretic-structure, resolvent-estimate
- Entry score: 0.5321
- Pathway score: 0.4705
- Goal: Develop a proof pathway centered on st.thm.hille-yosida-contraction.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.023 (intervention-focus, priority=0.6195)
  - phyp.hille-yosida-theorem.008 (bridge-link, priority=0.4078)
  - phyp.hille-yosida-theorem.009 (bridge-link, priority=0.4058)
  - phyp.hille-yosida-theorem.040 (definition-introduction, priority=0.4004)
- Supporting links:
  - st.def.resolvent -> st.thm.hille-yosida-contraction (score=0.342)
  - st.thm.hille-yosida-general -> st.thm.hille-yosida-contraction (score=0.3398)
  - st.def.c0-semigroup -> st.thm.hille-yosida-contraction (score=0.322)
- Execution plan:
  - Run kb-abduce on target st.thm.hille-yosida-contraction using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.hille-yosida-contraction in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.006 - st.thm.lumer-phillips
- Rank: 6
- Phase: Current Bridge Agenda
- Entry concepts: equivalence-schema, unconditional, equivalence, group-theoretic-structure, operator-theoretic-model
- Entry score: 0.4888
- Pathway score: 0.4445
- Goal: Develop a proof pathway centered on st.thm.lumer-phillips.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.024 (intervention-focus, priority=0.5867)
  - phyp.hille-yosida-theorem.006 (bridge-link, priority=0.4193)
  - phyp.hille-yosida-theorem.038 (definition-introduction, priority=0.4109)
  - phyp.hille-yosida-theorem.013 (bridge-link, priority=0.3844)
- Supporting links:
  - st.def.c0-semigroup -> st.thm.lumer-phillips (score=0.3548)
  - st.def.generator -> st.thm.lumer-phillips (score=0.316)
  - st.thm.cauchy-problem-equivalence -> st.thm.lumer-phillips (score=0.304)
- Execution plan:
  - Run kb-abduce on target st.thm.lumer-phillips using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.lumer-phillips in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.007 - st.def.resolvent
- Rank: 7
- Phase: Foundational Gauge-Theoretic Definitions
- Entry concepts: operator-theoretic-model, resolvent-estimate
- Entry score: 0.4509
- Pathway score: 0.406
- Goal: Develop a proof pathway centered on st.def.resolvent.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.008 (bridge-link, priority=0.4078)
  - phyp.hille-yosida-theorem.040 (definition-introduction, priority=0.4004)
  - phyp.hille-yosida-theorem.010 (bridge-link, priority=0.3901)
  - phyp.hille-yosida-theorem.028 (intervention-focus, priority=0.388)
- Supporting links:
  - st.def.resolvent -> st.thm.hille-yosida-contraction (score=0.342)
  - st.def.resolvent -> st.thm.hille-yosida-general (score=0.3223)
  - st.def.c0-semigroup -> st.def.resolvent (score=0.2601)
- Execution plan:
  - Run kb-abduce on target st.def.resolvent using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.resolvent in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.008 - st.prop.generator-closed-dense
- Rank: 8
- Phase: Additional KB-Specific Phases
- Entry concepts: group-theoretic-structure, laplace-transform, barrier, domain-regularity
- Entry score: 0.3757
- Pathway score: 0.3647
- Goal: Develop a proof pathway centered on st.prop.generator-closed-dense.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.007 (bridge-link, priority=0.4105)
  - phyp.hille-yosida-theorem.039 (definition-introduction, priority=0.4029)
  - phyp.hille-yosida-theorem.030 (intervention-focus, priority=0.376)
  - phyp.hille-yosida-theorem.017 (bridge-link, priority=0.3728)
- Supporting links:
  - st.def.generator -> st.prop.generator-closed-dense (score=0.345)
  - st.def.c0-semigroup -> st.prop.generator-closed-dense (score=0.3031)
  - st.prop.generator-closed-dense -> st.thm.cauchy-problem-equivalence (score=0.2478)
- Execution plan:
  - Run kb-abduce on target st.prop.generator-closed-dense using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.prop.generator-closed-dense in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.
