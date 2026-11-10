# Entry Point Pathways

## Stats

- Pathways: 8
- Entry points considered: 8

## Ranked Pathways

### path.001 - st.def.wightman-qft
- Rank: 1
- Phase: Current Bridge Agenda
- Entry concepts: rigorous-Yang-Mills-construction, constructive-existence, Hamiltonian-mass-gap, Wightman-QFT, classical-Yang-Mills-PDE
- Entry score: 0.7082
- Pathway score: 0.6441
- Goal: Develop a proof pathway centered on st.def.wightman-qft.
- Supporting hypotheses:
  - phyp.yang-mills-existence-and-mass-gap.026 (intervention-focus, priority=0.6073)
  - phyp.yang-mills-existence-and-mass-gap.004 (bridge-link, priority=0.6066)
  - phyp.yang-mills-existence-and-mass-gap.005 (bridge-link, priority=0.6058)
  - phyp.yang-mills-existence-and-mass-gap.036 (representation-shift, priority=0.5816)
- Supporting links:
  - st.def.wightman-qft -> st.thm.constructive-qft-in-low-dimension-examples-with- (score=0.5629)
  - st.def.wightman-qft -> st.thm.os-reconstruction-and-equivalence-with-wightman- (score=0.562)
  - st.def.wightman-qft -> st.thm.balaban-s-rigorous-renormalisation-group-analysi (score=0.5242)
- Execution plan:
  - Run kb-abduce on target st.def.wightman-qft using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.wightman-qft in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.003 - st.def.os-euclidean-qft
- Rank: 3
- Phase: Current Bridge Agenda
- Entry concepts: OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction
- Entry score: 0.6632
- Pathway score: 0.6308
- Goal: Develop a proof pathway centered on st.def.os-euclidean-qft.
- Supporting hypotheses:
  - phyp.yang-mills-existence-and-mass-gap.021 (intervention-focus, priority=0.6708)
  - phyp.yang-mills-existence-and-mass-gap.001 (bridge-link, priority=0.623)
  - phyp.yang-mills-existence-and-mass-gap.003 (bridge-link, priority=0.6066)
  - phyp.yang-mills-existence-and-mass-gap.033 (representation-shift, priority=0.5965)
- Supporting links:
  - st.def.os-euclidean-qft -> st.thm.os-reconstruction-and-equivalence-with-wightman- (score=0.5811)
  - st.def.os-euclidean-qft -> st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu (score=0.5629)
  - st.def.os-euclidean-qft -> st.def.osterwalder-schrader-os-euclidean-qft (score=0.5354)
- Execution plan:
  - Run kb-abduce on target st.def.os-euclidean-qft using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.os-euclidean-qft in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.002 - st.def.mass-gap
- Rank: 2
- Phase: Current Bridge Agenda
- Entry concepts: transfer-matrix-gap-implies-correlator-decay, correlator-decay-signals-mass-gap, reflection-positivity-and-transfer-matrix, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction
- Entry score: 0.6731
- Pathway score: 0.6228
- Goal: Develop a proof pathway centered on st.def.mass-gap.
- Supporting hypotheses:
  - phyp.yang-mills-existence-and-mass-gap.022 (intervention-focus, priority=0.6623)
  - phyp.yang-mills-existence-and-mass-gap.006 (bridge-link, priority=0.5966)
  - phyp.yang-mills-existence-and-mass-gap.038 (intermediate-invariant, priority=0.5725)
  - phyp.yang-mills-existence-and-mass-gap.012 (bridge-link, priority=0.5697)
- Supporting links:
  - st.def.mass-gap -> st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu (score=0.5518)
  - st.def.mass-gap -> st.thm.strong-coupling-exponential-decay-and-a-lattice- (score=0.5219)
  - st.def.mass-gap -> st.thm.os-reconstruction-and-equivalence-with-wightman- (score=0.5193)
- Execution plan:
  - Run kb-abduce on target st.def.mass-gap using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.mass-gap in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.004 - st.def.compact-simple-gauge-group
- Rank: 4
- Phase: Foundational Gauge-Theoretic Definitions
- Entry concepts: compact-simple-gauge-group, Yang-Mills, gauge-theory, geometric-analysis
- Entry score: 0.6521
- Pathway score: 0.6138
- Goal: Develop a proof pathway centered on st.def.compact-simple-gauge-group.
- Supporting hypotheses:
  - phyp.yang-mills-existence-and-mass-gap.002 (bridge-link, priority=0.6099)
  - phyp.yang-mills-existence-and-mass-gap.007 (bridge-link, priority=0.5897)
  - phyp.yang-mills-existence-and-mass-gap.008 (bridge-link, priority=0.5856)
  - phyp.yang-mills-existence-and-mass-gap.034 (intermediate-invariant, priority=0.5846)
- Supporting links:
  - st.def.compact-simple-gauge-group -> st.thm.donaldson-s-gauge-theoretic-constraints-on-smoot (score=0.5666)
  - st.def.compact-simple-gauge-group -> st.thm.adhm-classification-all-instantons-on-s-4 (score=0.5441)
  - st.def.compact-simple-gauge-group -> st.thm.uhlenbeck-gauge-fixing-and-compactness (score=0.5396)
- Execution plan:
  - Run kb-abduce on target st.def.compact-simple-gauge-group using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.compact-simple-gauge-group in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.006 - st.thm.os-reconstruction-and-equivalence-with-wightman-
- Rank: 6
- Phase: Current Bridge Agenda
- Entry concepts: lattice-continuum-control-implies-constructive-QFT, OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, multiscale-renormalization-control
- Entry score: 0.5658
- Pathway score: 0.5766
- Goal: Develop a proof pathway centered on st.thm.os-reconstruction-and-equivalence-with-wightman-.
- Supporting hypotheses:
  - phyp.yang-mills-existence-and-mass-gap.001 (bridge-link, priority=0.623)
  - phyp.yang-mills-existence-and-mass-gap.025 (intervention-focus, priority=0.6126)
  - phyp.yang-mills-existence-and-mass-gap.005 (bridge-link, priority=0.6058)
  - phyp.yang-mills-existence-and-mass-gap.033 (representation-shift, priority=0.5965)
- Supporting links:
  - st.def.os-euclidean-qft -> st.thm.os-reconstruction-and-equivalence-with-wightman- (score=0.5811)
  - st.def.wightman-qft -> st.thm.os-reconstruction-and-equivalence-with-wightman- (score=0.562)
  - st.def.mass-gap -> st.thm.os-reconstruction-and-equivalence-with-wightman- (score=0.5193)
- Execution plan:
  - Run kb-abduce on target st.thm.os-reconstruction-and-equivalence-with-wightman- using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.os-reconstruction-and-equivalence-with-wightman- in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.005 - st.def.osterwalder-schrader-os-euclidean-qft
- Rank: 5
- Phase: Current Bridge Agenda
- Entry concepts: OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction
- Entry score: 0.5843
- Pathway score: 0.5726
- Goal: Develop a proof pathway centered on st.def.osterwalder-schrader-os-euclidean-qft.
- Supporting hypotheses:
  - phyp.yang-mills-existence-and-mass-gap.024 (intervention-focus, priority=0.6192)
  - phyp.yang-mills-existence-and-mass-gap.009 (bridge-link, priority=0.5819)
  - phyp.yang-mills-existence-and-mass-gap.013 (bridge-link, priority=0.5694)
  - phyp.yang-mills-existence-and-mass-gap.041 (representation-shift, priority=0.559)
- Supporting links:
  - st.def.os-euclidean-qft -> st.def.osterwalder-schrader-os-euclidean-qft (score=0.5354)
  - st.def.osterwalder-schrader-os-euclidean-qft -> st.thm.os-reconstruction (score=0.5216)
- Execution plan:
  - Run kb-abduce on target st.def.osterwalder-schrader-os-euclidean-qft using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.osterwalder-schrader-os-euclidean-qft in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.007 - st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu
- Rank: 7
- Phase: Current Bridge Agenda
- Entry concepts: lattice-continuum-control-implies-constructive-QFT, transfer-matrix-gap-implies-correlator-decay, correlator-decay-signals-mass-gap, OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix
- Entry score: 0.5615
- Pathway score: 0.5695
- Goal: Develop a proof pathway centered on st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu.
- Supporting hypotheses:
  - phyp.yang-mills-existence-and-mass-gap.023 (intervention-focus, priority=0.6235)
  - phyp.yang-mills-existence-and-mass-gap.003 (bridge-link, priority=0.6066)
  - phyp.yang-mills-existence-and-mass-gap.006 (bridge-link, priority=0.5966)
  - phyp.yang-mills-existence-and-mass-gap.035 (intermediate-invariant, priority=0.5816)
- Supporting links:
  - st.def.os-euclidean-qft -> st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu (score=0.5629)
  - st.def.mass-gap -> st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu (score=0.5518)
  - st.def.wightman-qft -> st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu (score=0.5074)
- Execution plan:
  - Run kb-abduce on target st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.euclidean-correlator-decay-as-a-mass-gap-signatu in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.008 - st.thm.reflection-positivity-and-transfer-matrix-for-la
- Rank: 8
- Phase: Mass-Gap and Spectral Transfer
- Entry concepts: lattice-continuum-control-implies-constructive-QFT, transfer-matrix-gap-implies-correlator-decay, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, multiscale-renormalization-control
- Entry score: 0.5404
- Pathway score: 0.5453
- Goal: Develop a proof pathway centered on st.thm.reflection-positivity-and-transfer-matrix-for-la.
- Supporting hypotheses:
  - phyp.yang-mills-existence-and-mass-gap.027 (intervention-focus, priority=0.5956)
  - phyp.yang-mills-existence-and-mass-gap.016 (bridge-link, priority=0.5627)
- Supporting links:
  - st.def.os-euclidean-qft -> st.thm.reflection-positivity-and-transfer-matrix-for-la (score=0.5141)
  - st.def.mass-gap -> st.thm.reflection-positivity-and-transfer-matrix-for-la (score=0.5044)
  - st.def.wightman-qft -> st.thm.reflection-positivity-and-transfer-matrix-for-la (score=0.5015)
- Execution plan:
  - Run kb-abduce on target st.thm.reflection-positivity-and-transfer-matrix-for-la using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.reflection-positivity-and-transfer-matrix-for-la in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.
