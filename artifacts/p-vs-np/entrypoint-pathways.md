# Entry Point Pathways

## Stats

- Pathways: 8
- Entry points considered: 8

## Ranked Pathways

### path.002 - st.def.hardness-magnification-phenomenon-programme-leve
- Rank: 2
- Phase: Current Bridge Agenda
- Entry concepts: mild-lower-bounds-imply-major-separation, nonuniform-circuit-exponential-lower-bound, MCSP-nonuniform-circuits-lower-bound, NP-not-in-P/poly, major-separation
- Entry score: 0.6142
- Pathway score: 0.6434
- Goal: Develop a proof pathway centered on st.def.hardness-magnification-phenomenon-programme-leve.
- Supporting hypotheses:
  - phyp.p-vs-np.001 (bridge-link, priority=0.7345)
  - phyp.p-vs-np.033 (definition-introduction, priority=0.6981)
  - phyp.p-vs-np.002 (bridge-link, priority=0.6818)
  - phyp.p-vs-np.023 (intervention-focus, priority=0.6652)
- Supporting links:
  - st.def.hardness-magnification-phenomenon-programme-leve -> st.thm.oliveira-pich-santhanam-magnification-near-state (score=0.705)
  - st.def.hardness-magnification-phenomenon-programme-leve -> st.thm.oliveira-santhanam-hardness-magnification-for-na (score=0.6464)
  - st.def.hardness-magnification-phenomenon-programme-leve -> st.thm.atserias-m-uller-simple-general-magnification-fr (score=0.5663)
- Execution plan:
  - Run kb-abduce on target st.def.hardness-magnification-phenomenon-programme-leve using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.hardness-magnification-phenomenon-programme-leve in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.003 - st.thm.oliveira-pich-santhanam-magnification-near-state
- Rank: 3
- Phase: Current Bridge Agenda
- Entry concepts: mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-exponential-lower-bound, NP-not-in-P/poly, major-separation
- Entry score: 0.5937
- Pathway score: 0.6293
- Goal: Develop a proof pathway centered on st.thm.oliveira-pich-santhanam-magnification-near-state.
- Supporting hypotheses:
  - phyp.p-vs-np.001 (bridge-link, priority=0.7345)
  - phyp.p-vs-np.033 (definition-introduction, priority=0.6981)
  - phyp.p-vs-np.022 (intervention-focus, priority=0.6687)
  - phyp.p-vs-np.010 (bridge-link, priority=0.6203)
- Supporting links:
  - st.def.hardness-magnification-phenomenon-programme-leve -> st.thm.oliveira-pich-santhanam-magnification-near-state (score=0.705)
  - st.thm.oliveira-pich-santhanam-magnification-near-state -> st.thm.oliveira-santhanam-hardness-magnification-for-na (score=0.5781)
- Execution plan:
  - Run kb-abduce on target st.thm.oliveira-pich-santhanam-magnification-near-state using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.oliveira-pich-santhanam-magnification-near-state in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.001 - st.def.item-5
- Rank: 1
- Phase: Current Bridge Agenda
- Entry concepts: nonuniform-circuit-lower-bound, lower-bound, nonuniform-circuits, E, P/poly
- Entry score: 0.6154
- Pathway score: 0.6159
- Goal: Develop a proof pathway centered on st.def.item-5.
- Supporting hypotheses:
  - phyp.p-vs-np.004 (bridge-link, priority=0.6593)
  - phyp.p-vs-np.005 (bridge-link, priority=0.6317)
  - phyp.p-vs-np.036 (definition-introduction, priority=0.6296)
  - phyp.p-vs-np.017 (bridge-link, priority=0.6089)
- Supporting links:
  - st.def.item-5 -> st.thm.adleman-adleman1978 (score=0.6215)
  - st.def.item-5 -> st.thm.williams-improved-exhaustive-search-circuit-lowe (score=0.5908)
  - st.def.item-5 -> st.thm.williams-nonuniform-0-lower-bounds-for-williams2 (score=0.5655)
- Execution plan:
  - Run kb-abduce on target st.def.item-5 using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.def.item-5 in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.004 - st.thm.oliveira-santhanam-hardness-magnification-for-na
- Rank: 4
- Phase: Current Bridge Agenda
- Entry concepts: mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-superpolynomial-lower-bound, NP-not-in-P/poly, major-separation
- Entry score: 0.572
- Pathway score: 0.6018
- Goal: Develop a proof pathway centered on st.thm.oliveira-santhanam-hardness-magnification-for-na.
- Supporting hypotheses:
  - phyp.p-vs-np.021 (intervention-focus, priority=0.6898)
  - phyp.p-vs-np.002 (bridge-link, priority=0.6818)
  - phyp.p-vs-np.034 (definition-introduction, priority=0.65)
  - phyp.p-vs-np.010 (bridge-link, priority=0.6203)
- Supporting links:
  - st.def.hardness-magnification-phenomenon-programme-leve -> st.thm.oliveira-santhanam-hardness-magnification-for-na (score=0.6464)
  - st.thm.oliveira-pich-santhanam-magnification-near-state -> st.thm.oliveira-santhanam-hardness-magnification-for-na (score=0.5781)
  - st.def.item-5 -> st.thm.oliveira-santhanam-hardness-magnification-for-na (score=0.5398)
- Execution plan:
  - Run kb-abduce on target st.thm.oliveira-santhanam-hardness-magnification-for-na using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.oliveira-santhanam-hardness-magnification-for-na in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.005 - st.thm.cook-reckhow-proof-systems-and-cookreckhow1979
- Rank: 5
- Phase: Additional KB-Specific Phases
- Entry concepts: poly-bounded-proofs-iff-NP-equals-coNP, poly-bounded-proof-system, TAUT-proof-system-characterization, NP-equals-coNP, proof-system-characterization
- Entry score: 0.5696
- Pathway score: 0.5873
- Goal: Develop a proof pathway centered on st.thm.cook-reckhow-proof-systems-and-cookreckhow1979.
- Supporting hypotheses:
  - phyp.p-vs-np.003 (bridge-link, priority=0.6641)
  - phyp.p-vs-np.035 (definition-introduction, priority=0.634)
  - phyp.p-vs-np.030 (intervention-focus, priority=0.5423)
- Supporting links:
  - st.def.cook-reckhow-propositional-proof-system -> st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 (score=0.6268)
  - st.def.polynomially-bounded-proof-system -> st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 (score=0.5575)
- Execution plan:
  - Run kb-abduce on target st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.006 - st.thm.karp-many-natural-problems-are-np-complete-karp1
- Rank: 6
- Phase: Additional KB-Specific Phases
- Entry concepts: unconditional, NP-complete-classification, NP-completeness, many-one-reduction, E
- Entry score: 0.5572
- Pathway score: 0.5765
- Goal: Develop a proof pathway centered on st.thm.karp-many-natural-problems-are-np-complete-karp1.
- Supporting hypotheses:
  - phyp.p-vs-np.007 (bridge-link, priority=0.6293)
  - phyp.p-vs-np.012 (bridge-link, priority=0.6174)
  - phyp.p-vs-np.039 (normal-form-reduction, priority=0.6022)
  - phyp.p-vs-np.044 (definition-introduction, priority=0.5914)
- Supporting links:
  - st.thm.karp-many-natural-problems-are-np-complete-karp1 -> st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo (score=0.5881)
  - st.def.np-completeness -> st.thm.karp-many-natural-problems-are-np-complete-karp1 (score=0.5749)
  - st.def.polynomial-time-many-one-karp-reduction -> st.thm.karp-many-natural-problems-are-np-complete-karp1 (score=0.5595)
- Execution plan:
  - Run kb-abduce on target st.thm.karp-many-natural-problems-are-np-complete-karp1 using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.karp-many-natural-problems-are-np-complete-karp1 in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.007 - st.thm.kabanets-impagliazzo-pit-derandomisation-implies
- Rank: 7
- Phase: Current Bridge Agenda
- Entry concepts: PIT-in-P-implies-lower-bounds, proof-lower-bounds-imply-circuit-lower-bounds, PIT-derandomization-assumption, PIT-in-P, NEXP-vs-P/poly-or-Permanent-lower-bound
- Entry score: 0.5304
- Pathway score: 0.5622
- Goal: Develop a proof pathway centered on st.thm.kabanets-impagliazzo-pit-derandomisation-implies.
- Supporting hypotheses:
  - phyp.p-vs-np.025 (intervention-focus, priority=0.6185)
  - phyp.p-vs-np.013 (bridge-link, priority=0.6168)
- Supporting links:
  - st.def.hitting-set-for-pit-black-box -> st.thm.kabanets-impagliazzo-pit-derandomisation-implies (score=0.5742)
  - st.def.polynomial-identity-testing-pit -> st.thm.kabanets-impagliazzo-pit-derandomisation-implies (score=0.5558)
  - st.def.pseudorandom-function-prf-informal -> st.thm.kabanets-impagliazzo-pit-derandomisation-implies (score=0.5463)
- Execution plan:
  - Run kb-abduce on target st.thm.kabanets-impagliazzo-pit-derandomisation-implies using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.kabanets-impagliazzo-pit-derandomisation-implies in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.

### path.008 - st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a
- Rank: 8
- Phase: Current Bridge Agenda
- Entry concepts: IPS-lower-bounds-imply-arithmetic-lower-bounds, proof-lower-bounds-imply-circuit-lower-bounds, IPS-superpolynomial-lower-bound, PIT-derandomization-assumption, Permanent-arithmetic-circuit-lower-bound
- Entry score: 0.5153
- Pathway score: 0.557
- Goal: Develop a proof pathway centered on st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a.
- Supporting hypotheses:
  - phyp.p-vs-np.024 (intervention-focus, priority=0.6269)
- Supporting links:
  - st.def.hitting-set-for-pit-black-box -> st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a (score=0.5583)
  - st.def.polynomial-identity-testing-pit -> st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a (score=0.5567)
  - st.def.ideal-proof-system-ips-high-level -> st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a (score=0.5536)
- Execution plan:
  - Run kb-abduce on target st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a using top related hypotheses as seeds.
  - Inject top 1-2 tentative links touching st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a in a scratch KB and run kb-deduce.
  - Keep only hypothesis/link sets that improve conditional entailment coverage.
  - If no improvement, move to next-ranked pathway.
