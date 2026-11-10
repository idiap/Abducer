# Prior-Art Pass Report

- KB ref: p-vs-np
- Generated (UTC): 2026-03-17T11:03:23.431288+00:00
- Imported references: 8
- Blocked queue items: 24
- Covered blocked queue items: 24
- Uncovered blocked queue items: 0

## Search Justification

The local queue is exhausted through route conjectures, abstraction repairs, and repair lemmas, so browsing is justified only for named missing lemmas that materially affect novelty or barrier judgments.

## Key Findings

- The imported references ground most target-side theorems and barriers, but none closes the missing carrier-realization or formula-size transport lemmas.
- The PIT route sharpens from a vague semantic-to-algorithmic gap into an explicitness gap: known results already connect explicit hitting sets to black-box PIT and PIT derandomization to lower bounds.
- The Cook-Reckhow route is not discovering a new target theorem; the real gap is the bridge from the local definitional object to the existing NP=coNP characterization.
- The MCSP local-reduction route is now barrier-aware because prior art already shows non-NP-hardness under local reductions and strong consequences for harder reductions.
- The general magnification route is literature-backed, but the unresolved step remains object-class alignment between the MCSP-specific carrier and the sparse-problem or distinguisher framework.

## Imported References

### Hardness Magnification for Natural Problems

- Result ID: mathlibref.p-vs-np.001
- Type: theorem
- Statement: For natural problems including MCSP variants, sufficiently mild lower bounds in weak models can already imply strong consequences such as NP not in P/poly or strong formula lower bounds.
- Canonical citation: Igor C. Oliveira and Rahul Santhanam. Hardness Magnification for Natural Problems. Theory of Computing 14(13), 2018.
- Source: Theory of Computing
- URL: https://theoryofcomputing.org/articles/v014a013/
- Search query: Hardness Magnification for Natural Problems theory of computing
- Used for: Grounds the target side of the main MCSP magnification programme and shows that magnification itself is existing prior art.
- What changed: The leading MCSP route is no longer novel at the level of magnification-as-such; the open step is the typed carrier or realization theorem that would instantiate the route inside the current proof state.
- Linked queue ids: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.009, proofq.p-vs-np.018
- Obstruction classes: carrier-realization, mcsp-magnification
- InformalMathLib file: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.001-hardness-magnification-for-natural-problems.md

### Hardness Magnification Near State-of-the-Art Lower Bounds

- Result ID: mathlibref.p-vs-np.002
- Type: theorem
- Statement: Near-threshold lower bounds for suitable Gap-MCSP variants can already imply major consequences such as NP not in P/poly.
- Canonical citation: Igor C. Oliveira, Jan Pich, and Rahul Santhanam. Hardness Magnification Near State-of-the-Art Lower Bounds. Theory of Computing 17(11), 2021.
- Source: Theory of Computing
- URL: https://theoryofcomputing.org/articles/v017a011/
- Search query: Hardness Magnification Near State-of-the-Art Lower Bounds theory of computing
- Used for: Pins down the near-threshold MCSP theorem family underlying bridge.001 and bridge.010.
- What changed: The bridge.001 target is externally grounded, so the remaining novelty claim shifts to how the current framework realizes a usable MCSP carrier rather than to the target theorem itself.
- Linked queue ids: proofq.p-vs-np.001, proofq.p-vs-np.005, proofq.p-vs-np.010, proofq.p-vs-np.009, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021
- Obstruction classes: carrier-realization, formula-size-transport, mcsp-magnification
- InformalMathLib file: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.002-hardness-magnification-near-state-of-the-art-lower-bounds.md

### MCSP Is Not NP-Hard Under Local Reductions

- Result ID: mathlibref.p-vs-np.003
- Type: theorem
- Statement: MCSP is not NP-hard under sufficiently local reductions, and stronger NP-hardness assumptions for MCSP would imply unexpected complexity-class consequences.
- Canonical citation: Cody Murray and Ryan Williams. On the (Non) NP-Hardness of Computing Circuit Complexity. Theory of Computing 13(4), 2017.
- Source: Theory of Computing
- URL: https://theoryofcomputing.org/articles/v013a004/
- Search query: On the (Non) NP-Hardness of Computing Circuit Complexity theory of computing
- Used for: Grounds the barrier side of the local-reduction route and sharpens what a successful reduction-gadget lemma would have to overcome.
- What changed: The local-reduction route is now explicitly barrier-aware: the missing gadget lemma must overcome known non-hardness and consequence results, not just fill an arbitrary construction gap.
- Linked queue ids: proofq.p-vs-np.004, proofq.p-vs-np.012, proofq.p-vs-np.019
- Obstruction classes: local-reduction-barrier
- InformalMathLib file: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.003-mcsp-is-not-np-hard-under-local-reductions.md

### Hitting-Set Generators Yield Black-Box PIT

- Result ID: mathlibref.p-vs-np.004
- Type: theorem
- Statement: If a generator hits a polynomial class, then one can build a deterministic black-box identity test for that class by evaluating over a suitable grid.
- Canonical citation: R. J. Anderson, D. van Melkebeek, and I. Volkovich. Non-Black-Box Hitting Sets From Restriction-Based Lower Bounds. ECCC TR11-188, 2011, Proposition 2.4.
- Source: Electronic Colloquium on Computational Complexity
- URL: https://eccc.weizmann.ac.il/report/2011/188/
- Search query: Non-Black-Box Hitting Sets From Restriction-Based Lower Bounds Proposition 2.4
- Used for: Clarifies the semantic-to-algorithmic direction on the PIT route by grounding the hitting-set to black-box-PIT implication.
- What changed: The PIT route is not blocked by the total absence of a hitting-set-to-PIT connection; it is blocked by the lack of an explicit generator or certificate object for the right class.
- Linked queue ids: proofq.p-vs-np.016, proofq.p-vs-np.017
- Obstruction classes: pit-upgrade, explicitness-gap
- InformalMathLib file: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.004-hitting-set-generators-yield-black-box-pit.md

### Derandomizing Polynomial Identity Tests Means Proving Circuit Lower Bounds

- Result ID: mathlibref.p-vs-np.005
- Type: theorem
- Statement: If polynomial identity testing over the integers is in polynomial time, then either NEXP is not in P/poly or Permanent has no polynomial-size arithmetic circuits.
- Canonical citation: Valentine Kabanets and Russell Impagliazzo. Derandomizing Polynomial Identity Tests Means Proving Circuit Lower Bounds. Computational Complexity 13(1-2):1-46, 2004.
- Source: Computational Complexity
- URL: https://doi.org/10.1007/s00037-004-0182-6
- Search query: Derandomizing Polynomial Identity Tests Means Proving Circuit Lower Bounds exact theorem
- Used for: Grounds the target side of the PIT derandomization route and separates that established target from the missing premise.
- What changed: The PIT route's target theorem is prior art; the remaining open step is the current framework's inability to produce the required derandomization premise from its local PIT carrier.
- Linked queue ids: proofq.p-vs-np.008, proofq.p-vs-np.016, proofq.p-vs-np.017
- Obstruction classes: pit-upgrade, target-grounding
- InformalMathLib file: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.005-derandomizing-polynomial-identity-tests-means-proving-circuit-lower-bounds.md

### Many Natural Problems Are NP-Complete

- Result ID: mathlibref.p-vs-np.008
- Type: theorem
- Statement: Many classic combinatorial problems are NP-complete under polynomial-time many-one reductions, giving concrete natural examples beyond the abstract definition of NP-completeness.
- Canonical citation: Richard M. Karp. Reducibility Among Combinatorial Problems. In Complexity of Computer Computations, 1972.
- Source: Springer
- URL: https://link.springer.com/chapter/10.1007/978-3-540-68279-0_8
- Search query: Reducibility Among Combinatorial Problems Karp many natural problems are NP-complete
- Used for: Grounds the target side of the schema-to-examples route and turns the remaining gap into a construction or transfer problem rather than a missing target theorem.
- What changed: The NP-complete examples route is now target-grounded: the open step is constructing or transferring explicit examples from the local abstraction, not discovering that natural NP-complete problems exist.
- Linked queue ids: proofq.p-vs-np.007, proofq.p-vs-np.015, proofq.p-vs-np.022
- Obstruction classes: schema-to-examples, target-grounding
- InformalMathLib file: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.008-many-natural-problems-are-np-complete.md

### Polynomially Bounded Proof Systems Characterize NP Equals coNP

- Result ID: mathlibref.p-vs-np.006
- Type: theorem
- Statement: TAUT has a polynomially bounded propositional proof system if and only if NP is closed under complement, equivalently if and only if NP equals coNP.
- Canonical citation: Stephen A. Cook and Robert A. Reckhow. The Relative Efficiency of Propositional Proof Systems. Journal of Symbolic Logic 44(1):36-50, 1979.
- Source: University of Toronto
- URL: https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf
- Search query: The Relative Efficiency of Propositional Proof Systems polynomially bounded proof system iff NP coNP
- Used for: Grounds the target side of the Cook-Reckhow route and shows that the target theorem is prior art rather than a missing destination theorem.
- What changed: The Cook-Reckhow route is now clearly a bridge problem, not a target-theorem problem: the open step is the semantic bridge from the local definitional object to this existing characterization theorem.
- Linked queue ids: proofq.p-vs-np.006, proofq.p-vs-np.014, proofq.p-vs-np.024
- Obstruction classes: characterization-bridge, target-grounding
- InformalMathLib file: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.006-polynomially-bounded-proof-systems-characterize-np-equals-conp.md

### A Simple and General Hardness Magnification Theorem

- Result ID: mathlibref.p-vs-np.007
- Type: theorem
- Statement: Slightly superlinear formula-size lower bounds for approximating any sufficiently sparse NP problem imply fixed-polynomial formula-size lower bounds for NP, yielding a general magnification route beyond problem-specific MCSP statements.
- Canonical citation: Albert Atserias and Moritz Muller. A Simple and General Hardness Magnification Theorem. arXiv:2503.18477, 2025.
- Source: arXiv
- URL: https://arxiv.org/pdf/2503.18477
- Search query: A Simple and General Hardness Magnification Theorem sparse NP problem formula-size
- Used for: Grounds the target side of the Atserias-Muller route and clarifies the object class that the current MCSP-specific carrier would need to align with.
- What changed: The general magnification route is literature-backed, but its live gap is an alignment theorem from the MCSP obstruction family to the sparse-problem or distinguisher object class required by the general theorem.
- Linked queue ids: proofq.p-vs-np.003, proofq.p-vs-np.011, proofq.p-vs-np.023
- Obstruction classes: target-alignment, general-magnification
- InformalMathLib file: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.007-a-simple-and-general-hardness-magnification-theorem.md

## Obstruction Map

### carrier-realization

- Reference IDs: mathlibref.p-vs-np.001, mathlibref.p-vs-np.002
- Reference titles: Hardness Magnification Near State-of-the-Art Lower Bounds, Hardness Magnification for Natural Problems
- Queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021
- Queue titles: MCSP witness family: major consequences such as NP not in P/poly, MCSP witness family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., MCSP witness family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., MCSP obstruction family: major consequences such as NP not in P/poly, MCSP obstruction family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., MCSP obstruction family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., Carrier Realization Lemma: major consequences such as NP not in P/poly, Formula-Size Transport Lemma: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., Formula-Size Transport Lemma: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...

- Change: The leading MCSP route is no longer novel at the level of magnification-as-such; the open step is the typed carrier or realization theorem that would instantiate the route inside the current proof state.
- Change: The bridge.001 target is externally grounded, so the remaining novelty claim shifts to how the current framework realizes a usable MCSP carrier rather than to the target theorem itself.

### characterization-bridge

- Reference IDs: mathlibref.p-vs-np.006
- Reference titles: Polynomially Bounded Proof Systems Characterize NP Equals coNP
- Queue IDs: proofq.p-vs-np.006, proofq.p-vs-np.014, proofq.p-vs-np.024
- Queue titles: TAUT proof progress measure: There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP, TAUT transport normal form: There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP, Characterization Bridge Lemma: There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP

- Change: The Cook-Reckhow route is now clearly a bridge problem, not a target-theorem problem: the open step is the semantic bridge from the local definitional object to this existing characterization theorem.

### explicitness-gap

- Reference IDs: mathlibref.p-vs-np.004
- Reference titles: Hitting-Set Generators Yield Black-Box PIT
- Queue IDs: proofq.p-vs-np.016, proofq.p-vs-np.017
- Queue titles: PIT certificate family: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard..., PIT Upgrade Lemma: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...

- Change: The PIT route is not blocked by the total absence of a hitting-set-to-PIT connection; it is blocked by the lack of an explicit generator or certificate object for the right class.

### formula-size-transport

- Reference IDs: mathlibref.p-vs-np.002
- Reference titles: Hardness Magnification Near State-of-the-Art Lower Bounds
- Queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021
- Queue titles: MCSP witness family: major consequences such as NP not in P/poly, MCSP witness family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., MCSP obstruction family: major consequences such as NP not in P/poly, MCSP obstruction family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., MCSP obstruction family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., Carrier Realization Lemma: major consequences such as NP not in P/poly, Formula-Size Transport Lemma: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., Formula-Size Transport Lemma: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...

- Change: The bridge.001 target is externally grounded, so the remaining novelty claim shifts to how the current framework realizes a usable MCSP carrier rather than to the target theorem itself.

### general-magnification

- Reference IDs: mathlibref.p-vs-np.007
- Reference titles: A Simple and General Hardness Magnification Theorem
- Queue IDs: proofq.p-vs-np.003, proofq.p-vs-np.011, proofq.p-vs-np.023
- Queue titles: MCSP witness family: There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for..., MCSP obstruction family: There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for..., Target Alignment Lemma: There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for...

- Change: The general magnification route is literature-backed, but its live gap is an alignment theorem from the MCSP obstruction family to the sparse-problem or distinguisher object class required by the general theorem.

### local-reduction-barrier

- Reference IDs: mathlibref.p-vs-np.003
- Reference titles: MCSP Is Not NP-Hard Under Local Reductions
- Queue IDs: proofq.p-vs-np.004, proofq.p-vs-np.012, proofq.p-vs-np.019
- Queue titles: unspecified witness family: is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various..., unspecified reduction gadget family: is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various..., Local Reduction Gadget Lemma: is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...

- Change: The local-reduction route is now explicitly barrier-aware: the missing gadget lemma must overcome known non-hardness and consequence results, not just fill an arbitrary construction gap.

### mcsp-magnification

- Reference IDs: mathlibref.p-vs-np.001, mathlibref.p-vs-np.002
- Reference titles: Hardness Magnification Near State-of-the-Art Lower Bounds, Hardness Magnification for Natural Problems
- Queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021
- Queue titles: MCSP witness family: major consequences such as NP not in P/poly, MCSP witness family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., MCSP witness family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., MCSP obstruction family: major consequences such as NP not in P/poly, MCSP obstruction family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., MCSP obstruction family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., Carrier Realization Lemma: major consequences such as NP not in P/poly, Formula-Size Transport Lemma: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter..., Formula-Size Transport Lemma: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...

- Change: The leading MCSP route is no longer novel at the level of magnification-as-such; the open step is the typed carrier or realization theorem that would instantiate the route inside the current proof state.
- Change: The bridge.001 target is externally grounded, so the remaining novelty claim shifts to how the current framework realizes a usable MCSP carrier rather than to the target theorem itself.

### pit-upgrade

- Reference IDs: mathlibref.p-vs-np.004, mathlibref.p-vs-np.005
- Reference titles: Derandomizing Polynomial Identity Tests Means Proving Circuit Lower Bounds, Hitting-Set Generators Yield Black-Box PIT
- Queue IDs: proofq.p-vs-np.008, proofq.p-vs-np.016, proofq.p-vs-np.017
- Queue titles: PIT witness family: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard..., PIT certificate family: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard..., PIT Upgrade Lemma: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...

- Change: The PIT route is not blocked by the total absence of a hitting-set-to-PIT connection; it is blocked by the lack of an explicit generator or certificate object for the right class.
- Change: The PIT route's target theorem is prior art; the remaining open step is the current framework's inability to produce the required derandomization premise from its local PIT carrier.

### schema-to-examples

- Reference IDs: mathlibref.p-vs-np.008
- Reference titles: Many Natural Problems Are NP-Complete
- Queue IDs: proofq.p-vs-np.007, proofq.p-vs-np.015, proofq.p-vs-np.022
- Queue titles: unspecified witness family: NP-complete under polynomial-time many-one reductions, unspecified reduction gadget family: NP-complete under polynomial-time many-one reductions, Schema-To-Examples Construction Lemma: NP-complete under polynomial-time many-one reductions

- Change: The NP-complete examples route is now target-grounded: the open step is constructing or transferring explicit examples from the local abstraction, not discovering that natural NP-complete problems exist.

### target-alignment

- Reference IDs: mathlibref.p-vs-np.007
- Reference titles: A Simple and General Hardness Magnification Theorem
- Queue IDs: proofq.p-vs-np.003, proofq.p-vs-np.011, proofq.p-vs-np.023
- Queue titles: MCSP witness family: There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for..., MCSP obstruction family: There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for..., Target Alignment Lemma: There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for...

- Change: The general magnification route is literature-backed, but its live gap is an alignment theorem from the MCSP obstruction family to the sparse-problem or distinguisher object class required by the general theorem.

### target-grounding

- Reference IDs: mathlibref.p-vs-np.005, mathlibref.p-vs-np.006, mathlibref.p-vs-np.008
- Reference titles: Derandomizing Polynomial Identity Tests Means Proving Circuit Lower Bounds, Many Natural Problems Are NP-Complete, Polynomially Bounded Proof Systems Characterize NP Equals coNP
- Queue IDs: proofq.p-vs-np.006, proofq.p-vs-np.007, proofq.p-vs-np.008, proofq.p-vs-np.014, proofq.p-vs-np.015, proofq.p-vs-np.016, proofq.p-vs-np.017, proofq.p-vs-np.022, proofq.p-vs-np.024
- Queue titles: TAUT proof progress measure: There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP, unspecified witness family: NP-complete under polynomial-time many-one reductions, PIT witness family: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard..., TAUT transport normal form: There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP, unspecified reduction gadget family: NP-complete under polynomial-time many-one reductions, PIT certificate family: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard..., PIT Upgrade Lemma: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard..., Schema-To-Examples Construction Lemma: NP-complete under polynomial-time many-one reductions, Characterization Bridge Lemma: There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP

- Change: The PIT route's target theorem is prior art; the remaining open step is the current framework's inability to produce the required derandomization premise from its local PIT carrier.
- Change: The NP-complete examples route is now target-grounded: the open step is constructing or transferring explicit examples from the local abstraction, not discovering that natural NP-complete problems exist.
- Change: The Cook-Reckhow route is now clearly a bridge problem, not a target-theorem problem: the open step is the semantic bridge from the local definitional object to this existing characterization theorem.

## Still Uncovered

- All currently blocked queue items are linked to at least one imported prior-art reference.
