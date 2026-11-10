# Entry Point Pathways

## Stats

- Pathways: 8
- Entry points considered: 8

## Ranked Pathways

### path.001 - st.thm.positive-functional-implies-measure
- Rank: 1
- Phase: Current Bridge Agenda
- Entry concepts: regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional
- Entry score: 0.7838
- Pathway score: 0.6205
- Goal: Develop a proof pathway centered on st.thm.positive-functional-implies-measure.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.022 (intervention-focus, priority=0.756)
  - phyp.riesz-markov-kakutani-representation-theorem.001 (bridge-link, priority=0.4518)
  - phyp.riesz-markov-kakutani-representation-theorem.031 (definition-introduction, priority=0.4405)
  - phyp.riesz-markov-kakutani-representation-theorem.004 (bridge-link, priority=0.4206)
- Supporting links:
  - st.def.cc-space -> st.thm.positive-functional-implies-measure (score=0.3909)
  - st.lem.uniqueness-from-cc-separation -> st.thm.positive-functional-implies-measure (score=0.3562)
  - st.def.lch-space -> st.thm.positive-functional-implies-measure (score=0.3548)
- Execution plan:
  - Run kb-abduce on target st.thm.positive-functional-implies-measure using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.positive-functional-implies-measure in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.002 - st.thm.riesz-markov-kakutani
- Rank: 2
- Phase: Current Bridge Agenda
- Entry concepts: regular-measure-implies-positive-functional, positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-representation
- Entry score: 0.7549
- Pathway score: 0.6086
- Goal: Develop a proof pathway centered on st.thm.riesz-markov-kakutani.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.021 (intervention-focus, priority=0.8014)
  - phyp.riesz-markov-kakutani-representation-theorem.002 (bridge-link, priority=0.4409)
  - phyp.riesz-markov-kakutani-representation-theorem.003 (bridge-link, priority=0.4366)
  - phyp.riesz-markov-kakutani-representation-theorem.032 (definition-introduction, priority=0.4306)
- Supporting links:
  - st.def.cc-space -> st.thm.riesz-markov-kakutani (score=0.3788)
  - st.def.lch-space -> st.thm.riesz-markov-kakutani (score=0.374)
  - st.thm.positive-functional-implies-measure -> st.thm.riesz-markov-kakutani (score=0.3416)
- Execution plan:
  - Run kb-abduce on target st.thm.riesz-markov-kakutani using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.riesz-markov-kakutani in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.003 - st.def.cc-space
- Rank: 3
- Phase: Current Bridge Agenda
- Entry concepts: positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition, compactly-supported-continuous-functions
- Entry score: 0.6955
- Pathway score: 0.5712
- Goal: Develop a proof pathway centered on st.def.cc-space.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.025 (intervention-focus, priority=0.6797)
  - phyp.riesz-markov-kakutani-representation-theorem.001 (bridge-link, priority=0.4518)
  - phyp.riesz-markov-kakutani-representation-theorem.002 (bridge-link, priority=0.4409)
  - phyp.riesz-markov-kakutani-representation-theorem.031 (definition-introduction, priority=0.4405)
- Supporting links:
  - st.def.cc-space -> st.thm.positive-functional-implies-measure (score=0.3909)
  - st.def.cc-space -> st.thm.riesz-markov-kakutani (score=0.3788)
  - st.def.cc-space -> st.def.positive-linear-functional (score=0.317)
- Execution plan:
  - Run kb-abduce on target st.def.cc-space using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.cc-space in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.004 - st.prop.integration-defines-functional
- Rank: 4
- Phase: Current Bridge Agenda
- Entry concepts: regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional
- Entry score: 0.6175
- Pathway score: 0.5101
- Goal: Develop a proof pathway centered on st.prop.integration-defines-functional.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.023 (intervention-focus, priority=0.7044)
  - phyp.riesz-markov-kakutani-representation-theorem.006 (bridge-link, priority=0.4151)
  - phyp.riesz-markov-kakutani-representation-theorem.036 (barrier-escape-principle, priority=0.4071)
  - phyp.riesz-markov-kakutani-representation-theorem.014 (bridge-link, priority=0.3636)
- Supporting links:
  - st.prop.integration-defines-functional -> st.thm.positive-functional-implies-measure (score=0.3501)
  - st.prop.integration-defines-functional -> st.thm.riesz-markov-kakutani (score=0.2929)
  - st.def.cc-space -> st.prop.integration-defines-functional (score=0.2503)
- Execution plan:
  - Run kb-abduce on target st.prop.integration-defines-functional using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.prop.integration-defines-functional in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.005 - st.lem.uniqueness-from-cc-separation
- Rank: 5
- Phase: Current Bridge Agenda
- Entry concepts: regular-measure-implies-positive-functional, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional, regular-borel-measure-definition
- Entry score: 0.6099
- Pathway score: 0.5089
- Goal: Develop a proof pathway centered on st.lem.uniqueness-from-cc-separation.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.024 (intervention-focus, priority=0.6862)
  - phyp.riesz-markov-kakutani-representation-theorem.004 (bridge-link, priority=0.4206)
  - phyp.riesz-markov-kakutani-representation-theorem.034 (barrier-escape-principle, priority=0.4121)
  - phyp.riesz-markov-kakutani-representation-theorem.013 (bridge-link, priority=0.368)
- Supporting links:
  - st.lem.uniqueness-from-cc-separation -> st.thm.positive-functional-implies-measure (score=0.3562)
  - st.lem.uniqueness-from-cc-separation -> st.thm.riesz-markov-kakutani (score=0.2978)
  - st.def.lch-space -> st.lem.uniqueness-from-cc-separation (score=0.2822)
- Execution plan:
  - Run kb-abduce on target st.lem.uniqueness-from-cc-separation using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.lem.uniqueness-from-cc-separation in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.006 - st.def.positive-linear-functional
- Rank: 6
- Phase: Current Bridge Agenda
- Entry concepts: positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-representation, functional-measure-correspondence, unique-representing-measure
- Entry score: 0.605
- Pathway score: 0.5056
- Goal: Develop a proof pathway centered on st.def.positive-linear-functional.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.026 (intervention-focus, priority=0.6061)
  - phyp.riesz-markov-kakutani-representation-theorem.008 (bridge-link, priority=0.4076)
  - phyp.riesz-markov-kakutani-representation-theorem.010 (bridge-link, priority=0.4061)
  - phyp.riesz-markov-kakutani-representation-theorem.038 (definition-introduction, priority=0.4003)
- Supporting links:
  - st.def.positive-linear-functional -> st.thm.positive-functional-implies-measure (score=0.3418)
  - st.def.positive-linear-functional -> st.thm.riesz-markov-kakutani (score=0.3401)
  - st.def.cc-space -> st.def.positive-linear-functional (score=0.317)
- Execution plan:
  - Run kb-abduce on target st.def.positive-linear-functional using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.positive-linear-functional in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.007 - st.def.lch-space
- Rank: 7
- Phase: Foundational Gauge-Theoretic Definitions
- Entry concepts: locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space, C_c-space
- Entry score: 0.5702
- Pathway score: 0.4957
- Goal: Develop a proof pathway centered on st.def.lch-space.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.027 (intervention-focus, priority=0.5732)
  - phyp.riesz-markov-kakutani-representation-theorem.003 (bridge-link, priority=0.4366)
  - phyp.riesz-markov-kakutani-representation-theorem.033 (definition-introduction, priority=0.4267)
  - phyp.riesz-markov-kakutani-representation-theorem.005 (bridge-link, priority=0.4193)
- Supporting links:
  - st.def.lch-space -> st.thm.riesz-markov-kakutani (score=0.374)
  - st.def.lch-space -> st.thm.positive-functional-implies-measure (score=0.3548)
  - st.def.lch-space -> st.lem.compact-open-approximation (score=0.3423)
- Execution plan:
  - Run kb-abduce on target st.def.lch-space using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.lch-space in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.008 - st.cor.c0-dual-representation
- Rank: 8
- Phase: Additional KB-Specific Phases
- Entry concepts: regular-measure-implies-positive-functional, c0-dual-implies-signed-regular-measure, total-variation-equals-dual-norm, regular-borel-measure-on-lch-space, continuous-linear-functional-on-c0
- Entry score: 0.5275
- Pathway score: 0.4363
- Goal: Develop a proof pathway centered on st.cor.c0-dual-representation.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.028 (intervention-focus, priority=0.5506)
  - phyp.riesz-markov-kakutani-representation-theorem.017 (bridge-link, priority=0.334)
  - phyp.riesz-markov-kakutani-representation-theorem.018 (bridge-link, priority=0.3307)
- Supporting links:
  - st.thm.positive-functional-implies-measure -> st.cor.c0-dual-representation (score=0.26)
  - st.def.lch-space -> st.cor.c0-dual-representation (score=0.2563)
  - st.thm.riesz-markov-kakutani -> st.cor.c0-dual-representation (score=0.2485)
- Execution plan:
  - Run kb-abduce on target st.cor.c0-dual-representation using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.cor.c0-dual-representation in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.
