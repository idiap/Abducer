# Entry Point Pathways

## Stats

- Pathways: 10
- Entry points considered: 10

## Ranked Pathways

### path.001 - st.thm.riesz-markov-kakutani
- Rank: 1
- Phase: Current Bridge Agenda
- Entry concepts: positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-representation, functional-measure-correspondence
- Entry score: 0.858
- Pathway score: 0.6642
- Goal: Develop a proof pathway centered on st.thm.riesz-markov-kakutani.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.021 (intervention-focus, priority=0.8204)
  - phyp.riesz-markov-kakutani-representation-theorem.002 (bridge-link, priority=0.4465)
  - phyp.riesz-markov-kakutani-representation-theorem.003 (bridge-link, priority=0.4398)
  - phyp.riesz-markov-kakutani-representation-theorem.032 (definition-introduction, priority=0.4357)
- Supporting links:
  - st.def.cc-space -> st.thm.riesz-markov-kakutani (score=0.385)
  - st.def.lch-space -> st.thm.riesz-markov-kakutani (score=0.3776)
  - st.def.positive-linear-functional -> st.thm.riesz-markov-kakutani (score=0.3552)
- Execution plan:
  - Run kb-abduce on target st.thm.riesz-markov-kakutani using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.riesz-markov-kakutani in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.002 - st.thm.positive-functional-implies-measure
- Rank: 2
- Phase: Current Bridge Agenda
- Entry concepts: positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-definition, positive-functional-definition, cc-space-definition
- Entry score: 0.7761
- Pathway score: 0.6137
- Goal: Develop a proof pathway centered on st.thm.positive-functional-implies-measure.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.024 (intervention-focus, priority=0.6936)
  - phyp.riesz-markov-kakutani-representation-theorem.001 (bridge-link, priority=0.4606)
  - phyp.riesz-markov-kakutani-representation-theorem.031 (definition-introduction, priority=0.4486)
  - phyp.riesz-markov-kakutani-representation-theorem.004 (bridge-link, priority=0.4226)
- Supporting links:
  - st.def.cc-space -> st.thm.positive-functional-implies-measure (score=0.4007)
  - st.def.lch-space -> st.thm.positive-functional-implies-measure (score=0.3584)
  - st.def.positive-linear-functional -> st.thm.positive-functional-implies-measure (score=0.3475)
- Execution plan:
  - Run kb-abduce on target st.thm.positive-functional-implies-measure using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.positive-functional-implies-measure in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.003 - st.def.cc-space
- Rank: 3
- Phase: Current Bridge Agenda
- Entry concepts: positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition, compactly-supported-continuous-functions
- Entry score: 0.7032
- Pathway score: 0.5804
- Goal: Develop a proof pathway centered on st.def.cc-space.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.023 (intervention-focus, priority=0.6943)
  - phyp.riesz-markov-kakutani-representation-theorem.001 (bridge-link, priority=0.4606)
  - phyp.riesz-markov-kakutani-representation-theorem.031 (definition-introduction, priority=0.4486)
  - phyp.riesz-markov-kakutani-representation-theorem.002 (bridge-link, priority=0.4465)
- Supporting links:
  - st.def.cc-space -> st.thm.positive-functional-implies-measure (score=0.4007)
  - st.def.cc-space -> st.thm.riesz-markov-kakutani (score=0.385)
  - st.def.cc-space -> st.def.positive-linear-functional (score=0.34)
- Execution plan:
  - Run kb-abduce on target st.def.cc-space using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.cc-space in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.004 - st.def.positive-linear-functional
- Rank: 4
- Phase: Current Bridge Agenda
- Entry concepts: positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-representation, functional-measure-correspondence, unique-representing-measure
- Entry score: 0.635
- Pathway score: 0.5298
- Goal: Develop a proof pathway centered on st.def.positive-linear-functional.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.026 (intervention-focus, priority=0.6598)
  - phyp.riesz-markov-kakutani-representation-theorem.005 (bridge-link, priority=0.4197)
  - phyp.riesz-markov-kakutani-representation-theorem.006 (bridge-link, priority=0.4127)
  - phyp.riesz-markov-kakutani-representation-theorem.035 (definition-introduction, priority=0.4113)
- Supporting links:
  - st.def.positive-linear-functional -> st.thm.riesz-markov-kakutani (score=0.3552)
  - st.def.positive-linear-functional -> st.thm.positive-functional-implies-measure (score=0.3475)
  - st.def.cc-space -> st.def.positive-linear-functional (score=0.34)
- Execution plan:
  - Run kb-abduce on target st.def.positive-linear-functional using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.positive-linear-functional in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.005 - st.prop.integration-defines-functional
- Rank: 5
- Phase: Current Bridge Agenda
- Entry concepts: regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional
- Entry score: 0.615
- Pathway score: 0.5191
- Goal: Develop a proof pathway centered on st.prop.integration-defines-functional.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.022 (intervention-focus, priority=0.6966)
  - phyp.riesz-markov-kakutani-representation-theorem.013 (bridge-link, priority=0.406)
  - phyp.riesz-markov-kakutani-representation-theorem.015 (bridge-link, priority=0.406)
  - phyp.riesz-markov-kakutani-representation-theorem.018 (bridge-link, priority=0.406)
- Supporting links:
  - st.prop.integration-defines-functional -> st.thm.riesz-markov-kakutani (score=0.34)
  - st.def.cc-space -> st.prop.integration-defines-functional (score=0.34)
  - st.def.lch-space -> st.prop.integration-defines-functional (score=0.34)
- Execution plan:
  - Run kb-abduce on target st.prop.integration-defines-functional using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.prop.integration-defines-functional in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.006 - st.lem.uniqueness-from-cc-separation
- Rank: 6
- Phase: Current Bridge Agenda
- Entry concepts: function-separation-implies-measure-uniqueness, compact-open-approximation-on-lch-space, regular-borel-measure-on-lch-space, unique-representing-measure, uniqueness-from-cc-separation
- Entry score: 0.6009
- Pathway score: 0.5091
- Goal: Develop a proof pathway centered on st.lem.uniqueness-from-cc-separation.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.025 (intervention-focus, priority=0.6644)
  - phyp.riesz-markov-kakutani-representation-theorem.011 (bridge-link, priority=0.406)
  - phyp.riesz-markov-kakutani-representation-theorem.014 (bridge-link, priority=0.406)
  - phyp.riesz-markov-kakutani-representation-theorem.041 (barrier-escape-principle, priority=0.3988)
- Supporting links:
  - st.lem.uniqueness-from-cc-separation -> st.thm.riesz-markov-kakutani (score=0.34)
  - st.def.cc-space -> st.lem.uniqueness-from-cc-separation (score=0.34)
  - st.lem.compact-open-approximation -> st.lem.uniqueness-from-cc-separation (score=0.34)
- Execution plan:
  - Run kb-abduce on target st.lem.uniqueness-from-cc-separation using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.lem.uniqueness-from-cc-separation in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.007 - st.def.lch-space
- Rank: 7
- Phase: Foundational Gauge-Theoretic Definitions
- Entry concepts: locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space, C_c-space
- Entry score: 0.582
- Pathway score: 0.5047
- Goal: Develop a proof pathway centered on st.def.lch-space.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.028 (intervention-focus, priority=0.6013)
  - phyp.riesz-markov-kakutani-representation-theorem.003 (bridge-link, priority=0.4398)
  - phyp.riesz-markov-kakutani-representation-theorem.033 (definition-introduction, priority=0.4296)
  - phyp.riesz-markov-kakutani-representation-theorem.004 (bridge-link, priority=0.4226)
- Supporting links:
  - st.def.lch-space -> st.thm.riesz-markov-kakutani (score=0.3776)
  - st.def.lch-space -> st.thm.positive-functional-implies-measure (score=0.3584)
  - st.def.lch-space -> st.lem.compact-open-approximation (score=0.34)
- Execution plan:
  - Run kb-abduce on target st.def.lch-space using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.lch-space in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.008 - st.lem.compact-open-approximation
- Rank: 8
- Phase: Additional KB-Specific Phases
- Entry concepts: compact-open-approximation-supports-regularity, compact-open-approximation-on-lch-space, compact-open-regularity-witness, locally-compact-hausdorff-definition, compact-open-approximation-lemma
- Entry score: 0.5802
- Pathway score: 0.4968
- Goal: Develop a proof pathway centered on st.lem.compact-open-approximation.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.027 (intervention-focus, priority=0.6307)
  - phyp.riesz-markov-kakutani-representation-theorem.008 (bridge-link, priority=0.406)
  - phyp.riesz-markov-kakutani-representation-theorem.012 (bridge-link, priority=0.406)
  - phyp.riesz-markov-kakutani-representation-theorem.017 (bridge-link, priority=0.406)
- Supporting links:
  - st.def.lch-space -> st.lem.compact-open-approximation (score=0.34)
  - st.def.cc-space -> st.lem.compact-open-approximation (score=0.34)
  - st.lem.compact-open-approximation -> st.thm.positive-functional-implies-measure (score=0.34)
- Execution plan:
  - Run kb-abduce on target st.lem.compact-open-approximation using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.lem.compact-open-approximation in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.009 - st.cor.c0-dual-representation
- Rank: 9
- Phase: Additional KB-Specific Phases
- Entry concepts: c0-dual-implies-signed-regular-measure, total-variation-equals-dual-norm, regular-borel-measure-on-lch-space, continuous-linear-functional-on-c0, signed-regular-measure-duality
- Entry score: 0.5546
- Pathway score: 0.4737
- Goal: Develop a proof pathway centered on st.cor.c0-dual-representation.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.029 (intervention-focus, priority=0.5281)
  - phyp.riesz-markov-kakutani-representation-theorem.016 (bridge-link, priority=0.406)
- Supporting links:
  - st.thm.riesz-markov-kakutani -> st.cor.c0-dual-representation (score=0.34)
  - st.def.lch-space -> st.cor.c0-dual-representation (score=0.2563)
  - st.def.cc-space -> st.cor.c0-dual-representation (score=0.248)
- Execution plan:
  - Run kb-abduce on target st.cor.c0-dual-representation using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.cor.c0-dual-representation in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.010 - st.ex.dirac-measure-evaluation
- Rank: 10
- Phase: Additional KB-Specific Phases
- Entry concepts: dirac-evaluation-example, cc-space-definition, compactly-supported-continuous-functions, C_c-space, integration-pairing
- Entry score: 0.3272
- Pathway score: 0.3406
- Goal: Develop a proof pathway centered on st.ex.dirac-measure-evaluation.
- Supporting hypotheses:
  - phyp.riesz-markov-kakutani-representation-theorem.019 (bridge-link, priority=0.406)
  - phyp.riesz-markov-kakutani-representation-theorem.020 (bridge-link, priority=0.406)
  - phyp.riesz-markov-kakutani-representation-theorem.030 (intervention-focus, priority=0.3478)
- Supporting links:
  - st.thm.riesz-markov-kakutani -> st.ex.dirac-measure-evaluation (score=0.34)
  - st.prop.integration-defines-functional -> st.ex.dirac-measure-evaluation (score=0.34)
  - st.def.lch-space -> st.ex.dirac-measure-evaluation (score=0.2347)
- Execution plan:
  - Run kb-abduce on target st.ex.dirac-measure-evaluation using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.ex.dirac-measure-evaluation in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.
