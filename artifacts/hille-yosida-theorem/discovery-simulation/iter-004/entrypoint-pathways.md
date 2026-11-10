# Entry Point Pathways

## Stats

- Pathways: 8
- Entry points considered: 8

## Ranked Pathways

### path.001 - st.thm.hille-yosida-general
- Rank: 1
- Phase: Current Bridge Agenda
- Entry concepts: c0-generation-implies-closed-dense-generator, resolvent-approximants-converge-to-generated-semigroup, closed-dense-plus-resolvent-powers-imply-c0-generation, closed-dense-operator-with-resolvent-power-bounds, resolvent-family-at-large-lambda
- Entry score: 0.792
- Pathway score: 0.7136
- Goal: Develop a proof pathway centered on st.thm.hille-yosida-general.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.031 (intervention-focus, priority=0.7922)
  - phyp.hille-yosida-theorem.002 (bridge-link, priority=0.6538)
  - phyp.hille-yosida-theorem.003 (bridge-link, priority=0.6468)
  - phyp.hille-yosida-theorem.044 (intermediate-invariant, priority=0.6245)
- Supporting links:
  - st.def.generator -> st.thm.hille-yosida-general (score=0.6153)
  - st.def.c0-semigroup -> st.thm.hille-yosida-general (score=0.6075)
  - st.thm.hille-yosida-general -> st.thm.hille-yosida-contraction (score=0.4835)
- Execution plan:
  - Run kb-abduce on target st.thm.hille-yosida-general using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.hille-yosida-general in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.002 - st.def.generator
- Rank: 2
- Phase: Current Bridge Agenda
- Entry concepts: c0-semigroup-definition, generator-definition, C0-semigroup-model, operator-theoretic-Banach-space, unbounded-generator-graph
- Entry score: 0.719
- Pathway score: 0.6702
- Goal: Develop a proof pathway centered on st.def.generator.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.032 (intervention-focus, priority=0.6854)
  - phyp.hille-yosida-theorem.002 (bridge-link, priority=0.6538)
  - phyp.hille-yosida-theorem.004 (bridge-link, priority=0.6331)
  - phyp.hille-yosida-theorem.044 (intermediate-invariant, priority=0.6245)
- Supporting links:
  - st.def.generator -> st.thm.hille-yosida-general (score=0.6153)
  - st.def.generator -> st.thm.cauchy-problem-equivalence (score=0.5923)
  - st.def.generator -> st.thm.lumer-phillips (score=0.5312)
- Execution plan:
  - Run kb-abduce on target st.def.generator using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.generator in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.003 - st.def.c0-semigroup
- Rank: 3
- Phase: Current Bridge Agenda
- Entry concepts: c0-semigroup-definition, C0-semigroup-model, operator-theoretic-Banach-space, Banach-space, C0-semigroup
- Entry score: 0.7055
- Pathway score: 0.6699
- Goal: Develop a proof pathway centered on st.def.c0-semigroup.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.001 (bridge-link, priority=0.6777)
  - phyp.hille-yosida-theorem.033 (intervention-focus, priority=0.6646)
  - phyp.hille-yosida-theorem.003 (bridge-link, priority=0.6468)
  - phyp.hille-yosida-theorem.043 (representation-shift, priority=0.6464)
- Supporting links:
  - st.def.c0-semigroup -> st.thm.cauchy-problem-equivalence (score=0.6419)
  - st.def.c0-semigroup -> st.thm.hille-yosida-general (score=0.6075)
  - st.def.c0-semigroup -> st.thm.lumer-phillips (score=0.5427)
- Execution plan:
  - Run kb-abduce on target st.def.c0-semigroup using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.c0-semigroup in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.004 - st.thm.cauchy-problem-equivalence
- Rank: 4
- Phase: Current Bridge Agenda
- Entry concepts: c0-generation-iff-cauchy-well-posedness, closed-operator-or-semigroup-generator, well-posed-abstract-cauchy-problem, cauchy-problem-equivalence, C0-semigroup-model
- Entry score: 0.626
- Pathway score: 0.617
- Goal: Develop a proof pathway centered on st.thm.cauchy-problem-equivalence.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.001 (bridge-link, priority=0.6777)
  - phyp.hille-yosida-theorem.043 (representation-shift, priority=0.6464)
  - phyp.hille-yosida-theorem.004 (bridge-link, priority=0.6331)
  - phyp.hille-yosida-theorem.035 (intervention-focus, priority=0.611)
- Supporting links:
  - st.def.c0-semigroup -> st.thm.cauchy-problem-equivalence (score=0.6419)
  - st.def.generator -> st.thm.cauchy-problem-equivalence (score=0.5923)
  - st.thm.cauchy-problem-equivalence -> st.thm.lumer-phillips (score=0.4362)
- Execution plan:
  - Run kb-abduce on target st.thm.cauchy-problem-equivalence using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.cauchy-problem-equivalence in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.005 - st.thm.hille-yosida-contraction
- Rank: 5
- Phase: Current Bridge Agenda
- Entry concepts: c0-generation-implies-closed-dense-generator, closed-dense-plus-first-resolvent-bound-imply-contraction-generation, resolvent-approximants-converge-to-generated-semigroup, closed-dense-operator-with-first-resolvent-bound, resolvent-family-at-large-lambda
- Entry score: 0.5547
- Pathway score: 0.5484
- Goal: Develop a proof pathway centered on st.thm.hille-yosida-contraction.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.034 (intervention-focus, priority=0.6382)
  - phyp.hille-yosida-theorem.007 (bridge-link, priority=0.5675)
  - phyp.hille-yosida-theorem.049 (intermediate-invariant, priority=0.546)
  - phyp.hille-yosida-theorem.008 (bridge-link, priority=0.538)
- Supporting links:
  - st.def.c0-semigroup -> st.thm.hille-yosida-contraction (score=0.5195)
  - st.def.generator -> st.thm.hille-yosida-contraction (score=0.4867)
  - st.thm.hille-yosida-general -> st.thm.hille-yosida-contraction (score=0.4835)
- Execution plan:
  - Run kb-abduce on target st.thm.hille-yosida-contraction using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.hille-yosida-contraction in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.006 - st.thm.lumer-phillips
- Rank: 6
- Phase: Current Bridge Agenda
- Entry concepts: closed-dense-plus-first-resolvent-bound-imply-contraction-generation, dissipativity-plus-range-condition-imply-contraction-generation, densely-defined-dissipative-operator-with-surjective-shift, closed-dense-operator-with-first-resolvent-bound, contraction-semigroup-via-dissipativity
- Entry score: 0.5081
- Pathway score: 0.5272
- Goal: Develop a proof pathway centered on st.thm.lumer-phillips.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.005 (bridge-link, priority=0.5884)
  - phyp.hille-yosida-theorem.006 (bridge-link, priority=0.5781)
  - phyp.hille-yosida-theorem.036 (intervention-focus, priority=0.5678)
  - phyp.hille-yosida-theorem.047 (intermediate-invariant, priority=0.565)
- Supporting links:
  - st.def.c0-semigroup -> st.thm.lumer-phillips (score=0.5427)
  - st.def.generator -> st.thm.lumer-phillips (score=0.5312)
  - st.thm.cauchy-problem-equivalence -> st.thm.lumer-phillips (score=0.4362)
- Execution plan:
  - Run kb-abduce on target st.thm.lumer-phillips using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.lumer-phillips in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.007 - st.prop.generator-closed-dense
- Rank: 7
- Phase: Additional KB-Specific Phases
- Entry concepts: c0-generation-implies-closed-dense-generator, generator-of-c0-semigroup, closed-densely-defined-generator, generator-closed-dense, C0-semigroup-model
- Entry score: 0.496
- Pathway score: 0.4772
- Goal: Develop a proof pathway centered on st.prop.generator-closed-dense.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.037 (intervention-focus, priority=0.5434)
  - phyp.hille-yosida-theorem.012 (bridge-link, priority=0.4936)
  - phyp.hille-yosida-theorem.054 (barrier-escape-principle, priority=0.4786)
  - phyp.hille-yosida-theorem.019 (bridge-link, priority=0.4572)
- Supporting links:
  - st.def.generator -> st.prop.generator-closed-dense (score=0.4373)
  - st.def.c0-semigroup -> st.prop.generator-closed-dense (score=0.3969)
  - st.prop.generator-closed-dense -> st.thm.hille-yosida-general (score=0.3843)
- Execution plan:
  - Run kb-abduce on target st.prop.generator-closed-dense using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.prop.generator-closed-dense in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.008 - st.def.resolvent
- Rank: 8
- Phase: Foundational Gauge-Theoretic Definitions
- Entry concepts: resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme, yosida-approximation-convergence, resolvent-definition
- Entry score: 0.445
- Pathway score: 0.4449
- Goal: Develop a proof pathway centered on st.def.resolvent.
- Supporting hypotheses:
  - phyp.hille-yosida-theorem.011 (bridge-link, priority=0.5079)
  - phyp.hille-yosida-theorem.053 (intermediate-invariant, priority=0.4916)
  - phyp.hille-yosida-theorem.039 (intervention-focus, priority=0.4863)
  - phyp.hille-yosida-theorem.027 (bridge-link, priority=0.4307)
- Supporting links:
  - st.def.resolvent -> st.thm.hille-yosida-general (score=0.4532)
  - st.def.c0-semigroup -> st.def.resolvent (score=0.3675)
  - st.def.resolvent -> st.thm.hille-yosida-contraction (score=0.3586)
- Execution plan:
  - Run kb-abduce on target st.def.resolvent using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.resolvent in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.
