# Entry Point Pathways

## Stats

- Pathways: 10
- Entry points considered: 10

## Ranked Pathways

### path.001 - st.thm.unitary-group-implies-self-adjoint-generator
- Rank: 1
- Phase: Current Bridge Agenda
- Entry concepts: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group
- Entry score: 0.8212
- Pathway score: 0.6463
- Goal: Develop a proof pathway centered on st.thm.unitary-group-implies-self-adjoint-generator.
- Supporting hypotheses:
  - phyp.stone-one-parameter-unitary-groups.022 (intervention-focus, priority=0.8125)
  - phyp.stone-one-parameter-unitary-groups.003 (bridge-link, priority=0.443)
  - phyp.stone-one-parameter-unitary-groups.004 (bridge-link, priority=0.4396)
  - phyp.stone-one-parameter-unitary-groups.005 (bridge-link, priority=0.4391)
- Supporting links:
  - st.def.self-adjoint-operator -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.3811)
  - st.thm.unitary-group-implies-self-adjoint-generator -> st.thm.stone-correspondence (score=0.3773)
  - st.def.unitary-group -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.3768)
- Execution plan:
  - Run kb-abduce on target st.thm.unitary-group-implies-self-adjoint-generator using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.unitary-group-implies-self-adjoint-generator in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.002 - st.thm.self-adjoint-implies-unitary-group
- Rank: 2
- Phase: Current Bridge Agenda
- Entry concepts: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, unitary-group-via-functional-calculus
- Entry score: 0.7935
- Pathway score: 0.6315
- Goal: Develop a proof pathway centered on st.thm.self-adjoint-implies-unitary-group.
- Supporting hypotheses:
  - phyp.stone-one-parameter-unitary-groups.023 (intervention-focus, priority=0.7815)
  - phyp.stone-one-parameter-unitary-groups.001 (bridge-link, priority=0.452)
  - phyp.stone-one-parameter-unitary-groups.002 (bridge-link, priority=0.4452)
  - phyp.stone-one-parameter-unitary-groups.031 (definition-introduction, priority=0.4407)
- Supporting links:
  - st.def.self-adjoint-operator -> st.thm.self-adjoint-implies-unitary-group (score=0.3911)
  - st.def.unitary-group -> st.thm.self-adjoint-implies-unitary-group (score=0.3835)
  - st.thm.spectral-theorem-functional-calculus -> st.thm.self-adjoint-implies-unitary-group (score=0.3617)
- Execution plan:
  - Run kb-abduce on target st.thm.self-adjoint-implies-unitary-group using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.self-adjoint-implies-unitary-group in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.003 - st.thm.stone-correspondence
- Rank: 3
- Phase: Current Bridge Agenda
- Entry concepts: unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus
- Entry score: 0.7636
- Pathway score: 0.6156
- Goal: Develop a proof pathway centered on st.thm.stone-correspondence.
- Supporting hypotheses:
  - phyp.stone-one-parameter-unitary-groups.021 (intervention-focus, priority=0.8342)
  - phyp.stone-one-parameter-unitary-groups.004 (bridge-link, priority=0.4396)
  - phyp.stone-one-parameter-unitary-groups.006 (bridge-link, priority=0.4322)
  - phyp.stone-one-parameter-unitary-groups.034 (barrier-escape-principle, priority=0.4294)
- Supporting links:
  - st.thm.unitary-group-implies-self-adjoint-generator -> st.thm.stone-correspondence (score=0.3773)
  - st.def.unitary-group -> st.thm.stone-correspondence (score=0.3691)
  - st.def.self-adjoint-operator -> st.thm.stone-correspondence (score=0.3584)
- Execution plan:
  - Run kb-abduce on target st.thm.stone-correspondence using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.stone-correspondence in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.005 - st.def.self-adjoint-operator
- Rank: 5
- Phase: Current Bridge Agenda
- Entry concepts: self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, stone-self-adjoint-correspondence, symmetric-generator
- Entry score: 0.7149
- Pathway score: 0.5816
- Goal: Develop a proof pathway centered on st.def.self-adjoint-operator.
- Supporting hypotheses:
  - phyp.stone-one-parameter-unitary-groups.025 (intervention-focus, priority=0.648)
  - phyp.stone-one-parameter-unitary-groups.001 (bridge-link, priority=0.452)
  - phyp.stone-one-parameter-unitary-groups.003 (bridge-link, priority=0.443)
  - phyp.stone-one-parameter-unitary-groups.031 (definition-introduction, priority=0.4407)
- Supporting links:
  - st.def.self-adjoint-operator -> st.thm.self-adjoint-implies-unitary-group (score=0.3911)
  - st.def.self-adjoint-operator -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.3811)
  - st.def.self-adjoint-operator -> st.thm.stone-correspondence (score=0.3584)
- Execution plan:
  - Run kb-abduce on target st.def.self-adjoint-operator using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.self-adjoint-operator in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.004 - st.thm.spectral-theorem-functional-calculus
- Rank: 4
- Phase: Current Bridge Agenda
- Entry concepts: resolvent-approximants-converge-to-generated-semigroup, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, resolvent-family-at-large-lambda
- Entry score: 0.7215
- Pathway score: 0.5752
- Goal: Develop a proof pathway centered on st.thm.spectral-theorem-functional-calculus.
- Supporting hypotheses:
  - phyp.stone-one-parameter-unitary-groups.024 (intervention-focus, priority=0.6857)
  - phyp.stone-one-parameter-unitary-groups.007 (bridge-link, priority=0.4255)
  - phyp.stone-one-parameter-unitary-groups.037 (barrier-escape-principle, priority=0.4166)
  - phyp.stone-one-parameter-unitary-groups.010 (bridge-link, priority=0.4127)
- Supporting links:
  - st.thm.spectral-theorem-functional-calculus -> st.thm.self-adjoint-implies-unitary-group (score=0.3617)
  - st.def.self-adjoint-operator -> st.thm.spectral-theorem-functional-calculus (score=0.3475)
  - st.def.unitary-group -> st.thm.spectral-theorem-functional-calculus (score=0.3247)
- Execution plan:
  - Run kb-abduce on target st.thm.spectral-theorem-functional-calculus using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.spectral-theorem-functional-calculus in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.006 - st.def.unitary-group
- Rank: 6
- Phase: Foundational Gauge-Theoretic Definitions
- Entry concepts: strongly-continuous-unitary-group, unitary-group-definition, operator-theoretic-Hilbert-space, Hilbert-space, Stone-correspondence
- Entry score: 0.6521
- Pathway score: 0.5438
- Goal: Develop a proof pathway centered on st.def.unitary-group.
- Supporting hypotheses:
  - phyp.stone-one-parameter-unitary-groups.028 (intervention-focus, priority=0.5809)
  - phyp.stone-one-parameter-unitary-groups.002 (bridge-link, priority=0.4452)
  - phyp.stone-one-parameter-unitary-groups.005 (bridge-link, priority=0.4391)
  - phyp.stone-one-parameter-unitary-groups.032 (definition-introduction, priority=0.4345)
- Supporting links:
  - st.def.unitary-group -> st.thm.self-adjoint-implies-unitary-group (score=0.3835)
  - st.def.unitary-group -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.3768)
  - st.def.unitary-group -> st.thm.stone-correspondence (score=0.3691)
- Execution plan:
  - Run kb-abduce on target st.def.unitary-group using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.unitary-group in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.007 - st.prop.generator-domain-regularity
- Rank: 7
- Phase: Current Bridge Agenda
- Entry concepts: c0-generation-implies-closed-dense-generator, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup, closed-densely-defined-generator
- Entry score: 0.6238
- Pathway score: 0.5153
- Goal: Develop a proof pathway centered on st.prop.generator-domain-regularity.
- Supporting hypotheses:
  - phyp.stone-one-parameter-unitary-groups.026 (intervention-focus, priority=0.6428)
  - phyp.stone-one-parameter-unitary-groups.016 (bridge-link, priority=0.3697)
- Supporting links:
  - st.prop.generator-domain-regularity -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.2997)
  - st.prop.generator-domain-regularity -> st.prop.generator-symmetry (score=0.2388)
  - st.def.unitary-group -> st.prop.generator-domain-regularity (score=0.2344)
- Execution plan:
  - Run kb-abduce on target st.prop.generator-domain-regularity using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.prop.generator-domain-regularity in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.008 - st.app.schrodinger-time-evolution
- Rank: 8
- Phase: Additional KB-Specific Phases
- Entry concepts: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, unitary-group-via-functional-calculus
- Entry score: 0.5209
- Pathway score: 0.4452
- Goal: Develop a proof pathway centered on st.app.schrodinger-time-evolution.
- Supporting hypotheses:
  - phyp.stone-one-parameter-unitary-groups.027 (intervention-focus, priority=0.5841)
  - phyp.stone-one-parameter-unitary-groups.013 (bridge-link, priority=0.3865)
  - phyp.stone-one-parameter-unitary-groups.018 (bridge-link, priority=0.3608)
  - phyp.stone-one-parameter-unitary-groups.019 (bridge-link, priority=0.3475)
- Supporting links:
  - st.thm.self-adjoint-implies-unitary-group -> st.app.schrodinger-time-evolution (score=0.3183)
  - st.thm.spectral-theorem-functional-calculus -> st.app.schrodinger-time-evolution (score=0.2898)
  - st.def.self-adjoint-operator -> st.app.schrodinger-time-evolution (score=0.275)
- Execution plan:
  - Run kb-abduce on target st.app.schrodinger-time-evolution using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.app.schrodinger-time-evolution in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.009 - st.prop.generator-symmetry
- Rank: 9
- Phase: Additional KB-Specific Phases
- Entry concepts: differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, symmetric-generator, unitary-group-definition, generator-symmetry
- Entry score: 0.5087
- Pathway score: 0.4402
- Goal: Develop a proof pathway centered on st.prop.generator-symmetry.
- Supporting hypotheses:
  - phyp.stone-one-parameter-unitary-groups.029 (intervention-focus, priority=0.5558)
  - phyp.stone-one-parameter-unitary-groups.020 (bridge-link, priority=0.3456)
- Supporting links:
  - st.def.unitary-group -> st.prop.generator-symmetry (score=0.2729)
  - st.prop.generator-symmetry -> st.thm.unitary-group-implies-self-adjoint-generator (score=0.2457)
  - st.prop.generator-symmetry -> st.def.self-adjoint-operator (score=0.2405)
- Execution plan:
  - Run kb-abduce on target st.prop.generator-symmetry using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.prop.generator-symmetry in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.010 - st.ex.translation-group-on-l2
- Rank: 10
- Phase: Additional KB-Specific Phases
- Entry concepts: strongly-continuous-unitary-group, stone-self-adjoint-correspondence, stone-unitary-group-correspondence, unitary-group-definition, unitary-group-example
- Entry score: 0.4352
- Pathway score: 0.3906
- Goal: Develop a proof pathway centered on st.ex.translation-group-on-l2.
- Supporting hypotheses:
  - phyp.stone-one-parameter-unitary-groups.030 (intervention-focus, priority=0.4536)
  - phyp.stone-one-parameter-unitary-groups.017 (bridge-link, priority=0.3623)
- Supporting links:
  - st.def.unitary-group -> st.ex.translation-group-on-l2 (score=0.2914)
  - st.thm.unitary-group-implies-self-adjoint-generator -> st.ex.translation-group-on-l2 (score=0.2385)
  - st.thm.stone-correspondence -> st.ex.translation-group-on-l2 (score=0.23)
- Execution plan:
  - Run kb-abduce on target st.ex.translation-group-on-l2 using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.ex.translation-group-on-l2 in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.
