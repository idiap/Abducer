# KB Connection Analysis: `KB\p-vs-np.kb.md`

## Stats

- Ontology profile: computational-complexity
- Included statuses: accepted, tentative
- Statements: 64
- Filtered out statements: 0
- Dependency edges: 0
- Components: 64
- Candidate generation mode: cross-component
- Cross-component candidates (pre-trim): 1209
- Intra-component candidates (pre-trim): 0
- Missing dependencies: 0
- Avg semantic connection score: 0.428
- Avg concept alignment: 0.309
- Avg specificity alignment: 0.321
- Concept profile coverage: 1.0
- Specific profile coverage: 0.9531
- Concept graph nodes: 256

## Top Intervention Points

| statement_id | kind | score | unresolved | downstream | theory_relevance | specificity | concept_focus | partner |
|---|---|---|---|---|---|---|---|---|
| st.thm.oliveira-santhanam-hardness-magnification-for-na | theorem | 0.5398 | 0 | 0 | 0.9634 | 0.9 | mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-superpolynomial-lower-bound, NP-not-in-P/poly | st.thm.oliveira-pich-santhanam-magnification-near-state |
| st.thm.oliveira-pich-santhanam-magnification-near-state | theorem | 0.5187 | 0 | 0 | 0.9408 | 0.81 | mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-exponential-lower-bound, NP-not-in-P/poly | st.def.hardness-magnification-phenomenon-programme-leve |
| st.def.hardness-magnification-phenomenon-programme-leve | definition | 0.5152 | 0 | 0 | 0.7808 | 0.81 | mild-lower-bounds-imply-major-separation, nonuniform-circuit-exponential-lower-bound, MCSP-nonuniform-circuits-lower-bound, NP-not-in-P/poly | st.thm.oliveira-pich-santhanam-magnification-near-state |
| st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a | theorem | 0.4769 | 0 | 0 | 1.0 | 0.9 | IPS-lower-bounds-imply-arithmetic-lower-bounds, proof-lower-bounds-imply-circuit-lower-bounds, IPS-superpolynomial-lower-bound, PIT-derandomization-assumption | st.thm.razborov-rudich-natural-proofs-barrier-razborovr |
| st.thm.kabanets-impagliazzo-pit-derandomisation-implies | theorem | 0.4685 | 0 | 0 | 1.0 | 0.9 | PIT-in-P-implies-lower-bounds, proof-lower-bounds-imply-circuit-lower-bounds, PIT-derandomization-assumption, PIT-in-P | st.def.hitting-set-for-pit-black-box |
| st.def.item-5 | definition | 0.4375 | 0 | 0 | 0.4444 | 0.47 | nonuniform-circuit-lower-bound, lower-bound, nonuniform-circuits, E | st.thm.adleman-adleman1978 |
| st.thm.impagliazzo-wigderson-e-hardness-nonuniform-form | theorem | 0.4125 | 0 | 0 | 0.9257 | 1.0 | E-hardness-implies-BPP-equals-P, hardness-yields-BPP-derandomization, E-exponential-hardness, explicit-hard-function | st.def.circuit-family-s-n |
| st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo | theorem | 0.4116 | 0 | 0 | 0.9172 | 0.82 | local-reductions-preclude-MCSP-NP-completeness, local-reduction-to-MCSP, local-reduction, MCSP-hardness-transfer | st.thm.karp-many-natural-problems-are-np-complete-karp1 |
| st.thm.nisan-wigderson-hardness-vs-randomness-nisanwigd | theorem | 0.4043 | 0 | 0 | 0.9519 | 1.0 | hardness-implies-PRG, worst-case-to-average-case-hardness, PRG-for-poly-size-circuits, exponential-lower-bound | st.thm.kabanets-impagliazzo-pit-derandomisation-implies |
| st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | theorem | 0.3923 | 0 | 0 | 0.8845 | 0.69 | poly-bounded-proofs-iff-NP-equals-coNP, poly-bounded-proof-system, TAUT-proof-system-characterization, NP-equals-coNP | st.def.cook-reckhow-propositional-proof-system |
| st.thm.karp-many-natural-problems-are-np-complete-karp1 | theorem | 0.3822 | 0 | 0 | 0.6119 | 0.5 | unconditional, NP-complete-classification, NP-completeness, many-one-reduction | st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo |
| st.thm.williams-improved-exhaustive-search-circuit-lowe | theorem | 0.3597 | 0 | 0 | 0.6464 | 0.7 | unconditional, nonuniform-circuit-superpolynomial-lower-bound, nonuniform-circuit-exponential-lower-bound, SAT-nonuniform-circuits-lower-bound | st.def.item-5 |
| st.def.standard-restricted-circuit-classes | definition | 0.3588 | 0 | 0 | 0.4146 | 0.56 | nonuniform-circuit-exponential-lower-bound, AC0[p]-exponential-lower-bound, AC0[p]-lower-bound, ACC0-lower-bound | st.thm.razborov-smolensky-0-p |
| st.thm.williams-nonuniform-0-lower-bounds-for-williams2 | theorem | 0.356 | 0 | 0 | 0.6621 | 0.7 | unconditional, NEXP-not-in-ACC0, ACC0-lower-bound, NEXP-vs-ACC0 | st.thm.adleman-adleman1978 |
| st.thm.razborov-rudich-natural-proofs-barrier-razborovr | theorem | 0.3542 | 0 | 0 | 0.7092 | 0.7 | assumption-bundle, nonuniform-circuit-superpolynomial-lower-bound, nonuniform-circuit-lower-bound, hardness-vs-randomness | st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a |
| st.thm.hirahara-ilango-np-hardness-of-mcsp-from-well-st | theorem | 0.3437 | 0 | 0 | 0.8921 | 0.72 | assumptions-imply-MCSP-NP-hardness, cryptographic-and-complexity-assumptions, MCSP-hardness-transfer, MCSP-NP-hardness | st.thm.allender-das-szk-reduces-to-mcsp-bpp-reductions- |
| st.thm.aaronson-wigderson-algebrisation-barrier-aaronso | theorem | 0.3421 | 0 | 0 | 0.6831 | 0.7 | unconditional, P-not-equal-NP, P-vs-NP-separation, algebrization-barrier | st.def.algebrising-proof-technique-informal |
| st.thm.adleman-adleman1978 | theorem | 0.33 | 0 | 0 | 0.6621 | 0.7 | unconditional, nonuniform-circuit-lower-bound, lower-bound, nonuniform-circuits | st.def.item-5 |
| st.thm.cook-levin-sat-is-np-complete-cook1971 | theorem | 0.3288 | 0 | 0 | 0.6238 | 0.61 | unconditional, NP-complete-classification, NP-completeness, SAT-NP-complete | st.def.np-completeness |
| st.def.pseudorandom-function-prf-informal | definition | 0.3271 | 0 | 0 | 0.4136 | 0.66 | almost-all-functions-are-hard, hardness-vs-randomness, lower-bound, nonuniform-circuit-lower-bound | st.thm.kabanets-impagliazzo-pit-derandomisation-implies |

## Mathematical Concept Profiles (Interventions)

### st.thm.oliveira-santhanam-hardness-magnification-for-na
- Concept focus: mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-superpolynomial-lower-bound, NP-not-in-P/poly, major-separation
- Claim signatures: MCSP-formula-size-lower-bound, NP-vs-P/poly-separation, exponential-lower-bound, formula-size-lower-bound, hardness-magnification, lower-bound, near-threshold-lower-bound, nonuniform-circuit-lower-bound
- Antecedent signatures: MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-superpolynomial-lower-bound
- Consequence signatures: NP-not-in-P/poly, major-separation
- Model signatures: formula-size, nonuniform-circuits
- Reduction signatures: 
- Implication signatures: mild-lower-bounds-imply-major-separation
- Complexity classes: E, NP, P/poly
- Core problems: MCSP
- Proof regimes: algebraic-method, circuit-complexity, hardness-magnification, meta-complexity
- Barrier signals: 

### st.thm.oliveira-pich-santhanam-magnification-near-state
- Concept focus: mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-exponential-lower-bound, NP-not-in-P/poly, major-separation
- Claim signatures: MCSP-nonuniform-circuits-lower-bound, NP-vs-P/poly-separation, exponential-lower-bound, hardness-magnification, lower-bound, near-threshold-lower-bound, nonuniform-circuit-lower-bound
- Antecedent signatures: MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-exponential-lower-bound
- Consequence signatures: NP-not-in-P/poly, major-separation
- Model signatures: nonuniform-circuits
- Reduction signatures: 
- Implication signatures: mild-lower-bounds-imply-major-separation
- Complexity classes: E, NP, P/poly
- Core problems: MCSP
- Proof regimes: circuit-complexity, hardness-magnification
- Barrier signals: 

### st.def.hardness-magnification-phenomenon-programme-leve
- Concept focus: mild-lower-bounds-imply-major-separation, nonuniform-circuit-exponential-lower-bound, MCSP-nonuniform-circuits-lower-bound, NP-not-in-P/poly, major-separation
- Claim signatures: MCSP-nonuniform-circuits-lower-bound, NP-vs-P/poly-separation, exponential-lower-bound, hardness-magnification, lower-bound, nonuniform-circuit-lower-bound
- Antecedent signatures: nonuniform-circuit-exponential-lower-bound, MCSP-nonuniform-circuits-lower-bound
- Consequence signatures: NP-not-in-P/poly, major-separation
- Model signatures: nonuniform-circuits
- Reduction signatures: 
- Implication signatures: mild-lower-bounds-imply-major-separation
- Complexity classes: E, NP, P/poly
- Core problems: MCSP
- Proof regimes: circuit-complexity, hardness-magnification, meta-complexity
- Barrier signals: 

### st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a
- Concept focus: IPS-lower-bounds-imply-arithmetic-lower-bounds, proof-lower-bounds-imply-circuit-lower-bounds, IPS-superpolynomial-lower-bound, PIT-derandomization-assumption, Permanent-arithmetic-circuit-lower-bound
- Claim signatures: IPS-size-lower-bound, PIT-arithmetic-circuits-lower-bound, PIT-lower-bound-interface, arithmetic-circuit-lower-bound, exponential-lower-bound, hardness-vs-randomness, lower-bound, proof-size-lower-bound
- Antecedent signatures: IPS-superpolynomial-lower-bound, PIT-derandomization-assumption
- Consequence signatures: Permanent-arithmetic-circuit-lower-bound
- Model signatures: Cook-Reckhow-proof-system, IPS, arithmetic-circuits
- Reduction signatures: 
- Implication signatures: IPS-lower-bounds-imply-arithmetic-lower-bounds, proof-lower-bounds-imply-circuit-lower-bounds
- Complexity classes: E, VNP, VP
- Core problems: PIT, Permanent
- Proof regimes: algebraic-method, circuit-complexity, derandomization, proof-complexity
- Barrier signals: 

### st.thm.kabanets-impagliazzo-pit-derandomisation-implies
- Concept focus: PIT-in-P-implies-lower-bounds, proof-lower-bounds-imply-circuit-lower-bounds, PIT-derandomization-assumption, PIT-in-P, NEXP-vs-P/poly-or-Permanent-lower-bound
- Claim signatures: NEXP-circuit-separation, PIT-lower-bound-interface, PIT-nonuniform-circuits-lower-bound, arithmetic-circuit-lower-bound, exponential-lower-bound, hardness-vs-randomness, lower-bound, nonuniform-circuit-lower-bound
- Antecedent signatures: PIT-derandomization-assumption, PIT-in-P
- Consequence signatures: NEXP-vs-P/poly-or-Permanent-lower-bound
- Model signatures: arithmetic-circuits, nonuniform-circuits
- Reduction signatures: 
- Implication signatures: PIT-in-P-implies-lower-bounds, proof-lower-bounds-imply-circuit-lower-bounds
- Complexity classes: E, NEXP, P, P/poly
- Core problems: PIT, Permanent
- Proof regimes: algebraic-method, circuit-complexity, derandomization
- Barrier signals: 

### st.def.item-5
- Concept focus: nonuniform-circuit-lower-bound, lower-bound, nonuniform-circuits, E, P/poly
- Claim signatures: lower-bound, nonuniform-circuit-lower-bound
- Antecedent signatures: 
- Consequence signatures: nonuniform-circuit-lower-bound
- Model signatures: nonuniform-circuits
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: E, P/poly
- Core problems: 
- Proof regimes: algebraic-method, circuit-complexity
- Barrier signals: 

### st.thm.impagliazzo-wigderson-e-hardness-nonuniform-form
- Concept focus: E-hardness-implies-BPP-equals-P, hardness-yields-BPP-derandomization, E-exponential-hardness, explicit-hard-function, hardness-assumption
- Claim signatures: exponential-lower-bound, lower-bound, nonuniform-circuit-lower-bound
- Antecedent signatures: E-exponential-hardness, explicit-hard-function, hardness-assumption
- Consequence signatures: BPP-derandomization, BPP-equals-P
- Model signatures: PRG-construction, nonuniform-circuits, randomized-computation
- Reduction signatures: worst-case-to-average-case
- Implication signatures: E-hardness-implies-BPP-equals-P, hardness-yields-BPP-derandomization
- Complexity classes: BPP, E, P
- Core problems: 
- Proof regimes: circuit-complexity, nonuniform-model
- Barrier signals: 

### st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo
- Concept focus: local-reductions-preclude-MCSP-NP-completeness, local-reduction-to-MCSP, local-reduction, MCSP-hardness-transfer, MCSP-not-NP-complete
- Claim signatures: MCSP-NP-complete, MCSP-NP-hard, MCSP-NP-hardness, MCSP-local-nonhardness, NP-completeness, NP-hardness
- Antecedent signatures: local-reduction-to-MCSP, local-reduction
- Consequence signatures: MCSP-hardness-transfer, MCSP-not-NP-complete, NP-complete-classification
- Model signatures: 
- Reduction signatures: local-reduction
- Implication signatures: local-reductions-preclude-MCSP-NP-completeness
- Complexity classes: E, NP
- Core problems: MCSP
- Proof regimes: algebraic-method, completeness-framework, reduction-framework
- Barrier signals: 

### st.thm.nisan-wigderson-hardness-vs-randomness-nisanwigd
- Concept focus: hardness-implies-PRG, worst-case-to-average-case-hardness, PRG-for-poly-size-circuits, exponential-lower-bound, hardness-vs-randomness
- Claim signatures: exponential-lower-bound, hardness-vs-randomness, lower-bound, nonuniform-circuit-lower-bound
- Antecedent signatures: worst-case-to-average-case-hardness
- Consequence signatures: PRG-for-poly-size-circuits
- Model signatures: PRG-construction, nonuniform-circuits, randomized-computation
- Reduction signatures: worst-case-to-average-case
- Implication signatures: hardness-implies-PRG
- Complexity classes: BPP, E, P
- Core problems: 
- Proof regimes: algebraic-method, circuit-complexity, derandomization, randomness
- Barrier signals: 

### st.thm.cook-reckhow-proof-systems-and-cookreckhow1979
- Concept focus: poly-bounded-proofs-iff-NP-equals-coNP, poly-bounded-proof-system, TAUT-proof-system-characterization, NP-equals-coNP, proof-system-characterization
- Claim signatures: proof-system-characterization
- Antecedent signatures: poly-bounded-proof-system
- Consequence signatures: TAUT-proof-system-characterization, NP-equals-coNP
- Model signatures: Cook-Reckhow-proof-system
- Reduction signatures: 
- Implication signatures: poly-bounded-proofs-iff-NP-equals-coNP
- Complexity classes: E, NP, coNP
- Core problems: TAUT
- Proof regimes: algebraic-method, proof-complexity
- Barrier signals: 

### st.thm.karp-many-natural-problems-are-np-complete-karp1
- Concept focus: unconditional, NP-complete-classification, NP-completeness, many-one-reduction, E
- Claim signatures: NP-completeness
- Antecedent signatures: unconditional
- Consequence signatures: NP-complete-classification
- Model signatures: 
- Reduction signatures: many-one-reduction
- Implication signatures: 
- Complexity classes: E, NP
- Core problems: 
- Proof regimes: algebraic-method, completeness-framework, reduction-framework
- Barrier signals: 

### st.thm.williams-improved-exhaustive-search-circuit-lowe
- Concept focus: unconditional, nonuniform-circuit-superpolynomial-lower-bound, nonuniform-circuit-exponential-lower-bound, SAT-nonuniform-circuits-lower-bound, exponential-lower-bound
- Claim signatures: SAT-nonuniform-circuits-lower-bound, exponential-lower-bound, lower-bound, nonuniform-circuit-lower-bound, superpolynomial-lower-bound
- Antecedent signatures: unconditional
- Consequence signatures: nonuniform-circuit-superpolynomial-lower-bound, nonuniform-circuit-exponential-lower-bound
- Model signatures: nondeterministic-verifier, nonuniform-circuits
- Reduction signatures: 
- Implication signatures: 
- Complexity classes: E
- Core problems: SAT
- Proof regimes: algebraic-method, circuit-complexity, nonuniform-model
- Barrier signals: 

## Top Connection Candidates

| from_id | to_id | score | structural_similarity | semantic | concept_alignment | specific_alignment | relation | concept_evidence |
|---|---|---|---|---|---|---|---|---|
| st.def.hardness-magnification-phenomenon-programme-leve | st.thm.oliveira-pich-santhanam-magnification-near-state | 0.705 | 0.7037 | 0.7059 | 0.8494 | 0.8462 | definitional-expansion | nonuniform-circuit-exponential-lower-bound, mild-lower-bounds-imply-major-separation, NP-vs-P/poly-separation, NP-not-in-P/poly |
| st.def.hardness-magnification-phenomenon-programme-leve | st.thm.oliveira-santhanam-hardness-magnification-for-na | 0.6464 | 0.5878 | 0.579 | 0.676 | 0.5 | definitional-expansion | mild-lower-bounds-imply-major-separation, NP-vs-P/poly-separation, NP-not-in-P/poly, nonuniform-circuit-lower-bound |
| st.def.cook-reckhow-propositional-proof-system | st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | 0.6268 | 0.5742 | 0.5461 | 0.555 | 0.5 | definitional-expansion | TAUT-proof-system-characterization, proof-system-characterization, Cook-Reckhow-proof-system |
| st.def.item-5 | st.thm.adleman-adleman1978 | 0.6215 | 0.5561 | 0.5373 | 0.5137 | 0.6 | definitional-expansion | nonuniform-circuit-lower-bound, nonuniform-circuits, lower-bound |
| st.def.item-5 | st.thm.williams-improved-exhaustive-search-circuit-lowe | 0.5908 | 0.5118 | 0.458 | 0.2591 | 0.3 | definitional-expansion | nonuniform-circuit-lower-bound, nonuniform-circuits, lower-bound |
| st.def.algebrising-proof-technique-informal | st.thm.aaronson-wigderson-algebrisation-barrier-aaronso | 0.5882 | 0.4959 | 0.4647 | 0.4 | 0.4286 | definitional-expansion | algebrization-barrier, extension-oracle, oracle-model |
| st.thm.karp-many-natural-problems-are-np-complete-karp1 | st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo | 0.5881 | 0.5288 | 0.4419 | 0.2468 | 0.1429 | potential-equivalence | NP-complete-classification, NP-completeness |
| st.def.standard-restricted-circuit-classes | st.thm.razborov-smolensky-0-p | 0.5836 | 0.4902 | 0.4563 | 0.3667 | 0.4167 | definitional-expansion | AC0[p]-exponential-lower-bound, AC0[p]-lower-bound, exponential-lower-bound, AC0[p]-circuits |
| st.def.np-completeness | st.thm.cook-levin-sat-is-np-complete-cook1971 | 0.583 | 0.4838 | 0.4637 | 0.325 | 0.4 | potential-equivalence | NP-complete-classification, NP-completeness |
| st.thm.oliveira-pich-santhanam-magnification-near-state | st.thm.oliveira-santhanam-hardness-magnification-for-na | 0.5781 | 0.6223 | 0.5761 | 0.7077 | 0.6111 | implication-schema-transfer | MCSP-near-threshold-nonuniform-circuit-lower-bound, mild-lower-bounds-imply-major-separation, NP-vs-P/poly-separation, NP-not-in-P/poly |
| st.def.standard-restricted-circuit-classes | st.thm.williams-improved-exhaustive-search-circuit-lowe | 0.5771 | 0.4837 | 0.4375 | 0.2996 | 0.3125 | definitional-expansion | nonuniform-circuit-exponential-lower-bound, nonuniform-circuit-lower-bound, exponential-lower-bound, nonuniform-circuits |
| st.def.np-completeness | st.thm.karp-many-natural-problems-are-np-complete-karp1 | 0.5749 | 0.4306 | 0.4537 | 0.44 | 0.5 | potential-equivalence | NP-complete-classification, NP-completeness |
| st.def.hitting-set-for-pit-black-box | st.thm.kabanets-impagliazzo-pit-derandomisation-implies | 0.5742 | 0.4822 | 0.4271 | 0.2585 | 0.2353 | definitional-expansion | PIT-lower-bound-interface, PIT-derandomization-assumption, hardness-vs-randomness, lower-bound |
| st.def.standard-restricted-circuit-classes | st.thm.williams-nonuniform-0-lower-bounds-for-williams2 | 0.5709 | 0.4648 | 0.432 | 0.3081 | 0.4286 | definitional-expansion | nonuniform-circuit-lower-bound, ACC0-lower-bound, exponential-lower-bound, nonuniform-circuits |
| st.def.minimum-circuit-size-problem-mcsp | st.thm.counting-lower-bound-almost-all-functions-are-ha | 0.5691 | 0.4654 | 0.4201 | 0.15 | 0.4 | definitional-expansion | exponential-lower-bound, lower-bound |
| st.def.hardness-magnification-phenomenon-programme-leve | st.thm.atserias-m-uller-simple-general-magnification-fr | 0.5663 | 0.4678 | 0.4109 | 0.1794 | 0.25 | definitional-expansion | exponential-lower-bound, hardness-magnification, lower-bound |
| st.def.item-5 | st.thm.williams-nonuniform-0-lower-bounds-for-williams2 | 0.5655 | 0.4603 | 0.4158 | 0.2427 | 0.3333 | definitional-expansion | nonuniform-circuit-lower-bound, nonuniform-circuits, lower-bound |
| st.def.item-5 | st.thm.monotone-lower-bounds-for-clique-exemplar-razbor | 0.5621 | 0.4639 | 0.3951 | 0.1629 | 0.1111 | definitional-expansion | lower-bound |
| st.def.minimum-circuit-size-problem-mcsp | st.thm.h-stad-near-optimal-0-lower-bounds-for-parity-ha | 0.5605 | 0.4494 | 0.4055 | 0.2227 | 0.3333 | definitional-expansion | exponential-lower-bound, lower-bound |
| st.def.minimum-circuit-size-problem-mcsp | st.thm.atserias-m-uller-simple-general-magnification-fr | 0.5603 | 0.411 | 0.409 | 0.2643 | 0.5 | definitional-expansion | exponential-lower-bound, lower-bound |

## Abductive Loop Plan

### Round 1
- Objective: Prioritize intervention targets by graph influence and unresolved dependencies.
- Targets: st.thm.oliveira-santhanam-hardness-magnification-for-na, st.thm.oliveira-pich-santhanam-magnification-near-state, st.def.hardness-magnification-phenomenon-programme-leve, st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a, st.thm.kabanets-impagliazzo-pit-derandomisation-implies, st.def.item-5
- Action: Run kb-abduce on each target to propose missing-premise hypotheses.

### Round 2
- Objective: Test high-value cross-component links as abductive support hypotheses.
- Candidate connections: st.def.hardness-magnification-phenomenon-programme-leve->st.thm.oliveira-pich-santhanam-magnification-near-state (0.705), st.def.hardness-magnification-phenomenon-programme-leve->st.thm.oliveira-santhanam-hardness-magnification-for-na (0.6464), st.def.cook-reckhow-propositional-proof-system->st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 (0.6268), st.def.item-5->st.thm.adleman-adleman1978 (0.6215), st.def.item-5->st.thm.williams-improved-exhaustive-search-circuit-lowe (0.5908), st.def.algebrising-proof-technique-informal->st.thm.aaronson-wigderson-algebrisation-barrier-aaronso (0.5882)
- Action: Convert top links into conjectural dependencies and run kb-deduce for consequence checks.

### Round 3
- Objective: Refine and retain only hypotheses with best explanatory and deductive payoff.
- Action: Re-score interventions, drop contradicted links, and keep top surviving pathways.
