# Discovery Breakthrough Profile

- KB ref: p-vs-np
- Generated (UTC): 2026-03-18T06:33:02.113311+00:00
- Breakthrough profiles: 11
- Covered queue items: 24

## Discovery Diagnosis

The local queue is exhausted through route conjectures, abstraction repairs, and repair lemmas, so browsing is justified only for named missing lemmas that materially affect novelty or barrier judgments.

## Summary

- The discovery layer should stop restating blocked lemmas as if they were already search strategies.
- Most frontier pressure is now in bridge-layer breakthroughs: realization, transport, alignment, explicitness, and semantic bridging.
- Target-grounded routes should be treated as activation-theorem searches, not as target-theorem discovery.
- The highest-pressure breakthrough family is `abstraction-search` via obstruction class `mcsp-magnification`.

## Breakthrough Profiles

### mcsp-magnification

- Breakthrough family: abstraction-search
- Pressure score: 5.818
- Top queue priority: 0.779
- Required move: Find a sharper abstraction that turns the blocked route into a typed, inspectable theorem target.
- Abstraction required: A theorem-family-specific carrier, invariant, or bridge law that adds new mathematical content.
- Minimal theorem shape: State a route-specific theorem that would resolve the blocked interface and make the next proof obligation materially sharper.
- Major subresult type: exploratory-conjecture
- Queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021
- Reference IDs: mathlibref.p-vs-np.001, mathlibref.p-vs-np.002

#### Search Modes

- typed abstraction search
- bridge split
- counterfactual sharpening

#### Anti-Patterns

- repeating the same blocked statement without new typed structure

#### Effect Notes

- The leading MCSP route is no longer novel at the level of magnification-as-such; the open step is the typed carrier or realization theorem that would instantiate the route inside the current proof state.
- The bridge.001 target is externally grounded, so the remaining novelty claim shifts to how the current framework realizes a usable MCSP carrier rather than to the target theorem itself.

#### Sample Frontier Statements

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for... holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

### carrier-realization

- Breakthrough family: realization
- Pressure score: 5.818
- Top queue priority: 0.779
- Required move: Turn a typed but schematic carrier into an explicit mathematical object family with admissibility conditions and a forcing theorem.
- Abstraction required: An explicit obstruction family, witness family, surrogate promise problem, or quantitative measure that is realized from the source theorem rather than only named by role.
- Minimal theorem shape: If source theorem S holds in regime R, then one can construct an explicit carrier C with admissibility conditions A such that C preserves invariant I and supports a route-specific forcing lemma to target T.
- Major subresult type: bridge object/tool
- Queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021
- Reference IDs: mathlibref.p-vs-np.001, mathlibref.p-vs-np.002

#### Search Modes

- explicit carrier construction
- equivalence search between live carrier encodings
- surrogate problem design with forcing semantics

#### Anti-Patterns

- renaming the carrier without adding realizability conditions
- adding more obligations without exhibiting a concrete carrier family

#### Effect Notes

- The leading MCSP route is no longer novel at the level of magnification-as-such; the open step is the typed carrier or realization theorem that would instantiate the route inside the current proof state.
- The bridge.001 target is externally grounded, so the remaining novelty claim shifts to how the current framework realizes a usable MCSP carrier rather than to the target theorem itself.

#### Sample Frontier Statements

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for... holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

### formula-size-transport

- Breakthrough family: transport
- Pressure score: 5.060
- Top queue priority: 0.779
- Required move: Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.
- Abstraction required: A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift.
- Minimal theorem shape: For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.
- Major subresult type: transfer principle
- Queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021
- Reference IDs: mathlibref.p-vs-np.002

#### Search Modes

- cross-model transport principle
- invariant-preserving compilation theorem
- representation normal form for formula-size transfer

#### Anti-Patterns

- assuming the target theorem already provides the transport
- strengthening the source lower bound without addressing the model shift

#### Effect Notes

- The bridge.001 target is externally grounded, so the remaining novelty claim shifts to how the current framework realizes a usable MCSP carrier rather than to the target theorem itself.

#### Sample Frontier Statements

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for... holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.
- An adequate `canonical-obstruction-family` bridge concept for `bridge.001` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `nonuniform-circuit-exponential-lower-bound`, preserves `MCSP complexity profile in nonuniform-circuits`, and is strong enough to force `NP-not-in-P/poly`.

### target-grounding

- Breakthrough family: bridge-specificity
- Pressure score: 5.014
- Top queue priority: 0.686
- Required move: Stop treating the target theorem as the open problem and relocate search to the bridge that would activate it.
- Abstraction required: No new target theorem; discovery should instead seek the carrier, transfer law, or alignment theorem that makes the target theorem applicable.
- Minimal theorem shape: Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T's hypotheses from current artifacts.
- Major subresult type: research recommendation
- Queue IDs: proofq.p-vs-np.006, proofq.p-vs-np.007, proofq.p-vs-np.008, proofq.p-vs-np.014, proofq.p-vs-np.015, proofq.p-vs-np.016, proofq.p-vs-np.017, proofq.p-vs-np.022, proofq.p-vs-np.024
- Reference IDs: mathlibref.p-vs-np.005, mathlibref.p-vs-np.006, mathlibref.p-vs-np.008

#### Search Modes

- activation theorem search
- hypothesis verification search
- bridge-localization refinement

#### Anti-Patterns

- rediscovering the target theorem
- claiming novelty at the target instead of at the activation bridge

#### Effect Notes

- The PIT route's target theorem is prior art; the remaining open step is the current framework's inability to produce the required derandomization premise from its local PIT carrier.
- The NP-complete examples route is now target-grounded: the open step is constructing or transferring explicit examples from the local abstraction, not discovering that natural NP-complete problems exist.
- The Cook-Reckhow route is now clearly a bridge problem, not a target-theorem problem: the open step is the semantic bridge from the local definitional object to this existing characterization theorem.

#### Sample Frontier Statements

- There exists an admissible TAUT proof progress measure, realized as a monotone potential function over proofs or certificates, such that whenever A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is... holds for TAUT in Cook-Reckhow-proof-system, the object organizes the source-side mathematical content while preserving the invariant TAUT complexity profile in Cook-Reckhow-proof-system and yields There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP.
- There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A language L is emph NP-complete (under le_m^p ) iff (i) LinNP holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification and yields NP-complete under polynomial-time many-one reductions.
- There exists an admissible PIT witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by... holds for PIT in black-box-PIT, the object organizes the source-side mathematical content while preserving the invariant PIT semantic object across the transfer black-box-PIT -> arithmetic-circuits and yields If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard... for PIT in arithmetic-circuits.

### local-reduction-barrier

- Breakthrough family: barrier-aware transfer
- Pressure score: 1.984
- Top queue priority: 0.715
- Required move: Design a transfer mechanism that survives known local-reduction barriers, or prove that no such mechanism exists under explicit assumptions.
- Abstraction required: A barrier-aware reduction gadget family or an impossibility theorem explaining why the reduction regime cannot be crossed.
- Minimal theorem shape: Either construct a local reduction family G satisfying locality bounds L and preserving witness structure W, or prove that any such G would contradict barrier theorem B.
- Major subresult type: barrier result
- Queue IDs: proofq.p-vs-np.004, proofq.p-vs-np.012, proofq.p-vs-np.019
- Reference IDs: mathlibref.p-vs-np.003

#### Search Modes

- barrier-aware gadget design
- impossibility theorem search
- reduction regime decomposition

#### Anti-Patterns

- ignoring the known local-reduction barrier theorem
- using generic NP-hardness language without locality constraints

#### Effect Notes

- The local-reduction route is now explicitly barrier-aware: the missing gadget lemma must overcome known non-hardness and consequence results, not just fill an arbitrary construction gap.

#### Sample Frontier Statements

- There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever NP-complete under polynomial-time many-one reductions holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification from the source regime to MCSP and yields is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various... for MCSP.
- An adequate `reduction-gadget-family` bridge concept for `bridge.007` is a `family of reductions preserving the route witness structure` named `unspecified reduction gadget family` that absorbs `NP-completeness`, preserves `consequence schema NP-complete-classification`, and is strong enough to force `MCSP-hardness-transfer`.
- Construct and verify an explicit local reduction gadget family witnessing how `NP-complete under polynomial-time many-one reductions` transfers into the MCSP local-reduction regime while preserving `consequence schema NP-complete-classification`.

### target-alignment

- Breakthrough family: alignment
- Pressure score: 1.897
- Top queue priority: 0.722
- Required move: Identify or prove an equivalence between the current carrier class and the object class required by the target theorem.
- Abstraction required: An alignment theorem, correspondence theorem, or mediating normal form linking the local carrier to the target's sparse-problem or distinguisher objects.
- Minimal theorem shape: Every admissible carrier C from the local route induces an object D in the target theorem's class, and D preserves the quantitative property needed to activate the target theorem.
- Major subresult type: transfer principle
- Queue IDs: proofq.p-vs-np.003, proofq.p-vs-np.011, proofq.p-vs-np.023
- Reference IDs: mathlibref.p-vs-np.007

#### Search Modes

- object-class correspondence search
- normal-form mediation
- dual characterization of the target object

#### Anti-Patterns

- treating topical similarity as object equivalence
- adding a stronger carrier without specifying the target object class map

#### Effect Notes

- The general magnification route is literature-backed, but its live gap is an alignment theorem from the MCSP obstruction family to the sparse-problem or distinguisher object class required by the general theorem.

#### Sample Frontier Statements

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant exponential-lower-bound witness complexity and yields There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for....
- An adequate `canonical-obstruction-family` bridge concept for `bridge.016` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `nonuniform-circuit-exponential-lower-bound`, preserves `exponential-lower-bound witness complexity`, and is strong enough to force `exponential-lower-bound`.
- Prove an alignment theorem identifying `MCSP obstruction family` with the target object class needed to lift `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for...`.

### general-magnification

- Breakthrough family: alignment
- Pressure score: 1.897
- Top queue priority: 0.722
- Required move: Map a problem-specific carrier into a general magnification framework without losing the quantitative threshold that matters.
- Abstraction required: A general-purpose sparse-problem or distinguisher formulation that faithfully receives the local carrier.
- Minimal theorem shape: Problem-specific object C induces general object G with preserved sparsity or approximation parameters sufficient to trigger the general magnification theorem.
- Major subresult type: transfer principle
- Queue IDs: proofq.p-vs-np.003, proofq.p-vs-np.011, proofq.p-vs-np.023
- Reference IDs: mathlibref.p-vs-np.007

#### Search Modes

- generalization by faithful embedding
- parameter-preserving reformulation
- problem-specific to generic theorem bridge

#### Anti-Patterns

- moving to the generic theorem without a preserved parameter map
- using the general theorem only as motivation rather than as a typed target

#### Effect Notes

- The general magnification route is literature-backed, but its live gap is an alignment theorem from the MCSP obstruction family to the sparse-problem or distinguisher object class required by the general theorem.

#### Sample Frontier Statements

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant exponential-lower-bound witness complexity and yields There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for....
- An adequate `canonical-obstruction-family` bridge concept for `bridge.016` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `nonuniform-circuit-exponential-lower-bound`, preserves `exponential-lower-bound witness complexity`, and is strong enough to force `exponential-lower-bound`.
- Prove an alignment theorem identifying `MCSP obstruction family` with the target object class needed to lift `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for...`.

### pit-upgrade

- Breakthrough family: explicitness
- Pressure score: 1.752
- Top queue priority: 0.686
- Required move: Upgrade a semantic or existential algebraic object into an explicit algorithmic derandomization premise.
- Abstraction required: An explicit generator, certificate family, or algebraic witness system that is constructive enough for PIT rather than merely semantic.
- Minimal theorem shape: If semantic object C exists for the relevant circuit class, then one can uniformly and efficiently extract an explicit structure G that yields deterministic PIT for that class.
- Major subresult type: bridge object/tool
- Queue IDs: proofq.p-vs-np.008, proofq.p-vs-np.016, proofq.p-vs-np.017
- Reference IDs: mathlibref.p-vs-np.004, mathlibref.p-vs-np.005

#### Search Modes

- explicit extractor or generator search
- certificate map construction
- semantic-to-algorithmic upgrade theorem

#### Anti-Patterns

- equating a black-box hitting-set statement with an explicit generator
- rephrasing derandomization as semantics without uniformity or efficiency

#### Effect Notes

- The PIT route is not blocked by the total absence of a hitting-set-to-PIT connection; it is blocked by the lack of an explicit generator or certificate object for the right class.
- The PIT route's target theorem is prior art; the remaining open step is the current framework's inability to produce the required derandomization premise from its local PIT carrier.

#### Sample Frontier Statements

- There exists an admissible PIT witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by... holds for PIT in black-box-PIT, the object organizes the source-side mathematical content while preserving the invariant PIT semantic object across the transfer black-box-PIT -> arithmetic-circuits and yields If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard... for PIT in arithmetic-circuits.
- An adequate `algebraic-certificate` bridge concept for `bridge.013` is a `checkable certificate map or algebraic witness relation` named `PIT certificate family` that absorbs `PIT-derandomization-assumption`, preserves `PIT semantic object`, and is strong enough to force `NEXP-vs-P/poly-or-Permanent-lower-bound`.
- Prove an upgrade theorem turning the semantic black-box PIT object behind `PIT certificate family` into an algorithmic PIT-derandomization premise strong enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.

### schema-to-examples

- Breakthrough family: constructive instantiation
- Pressure score: 1.641
- Top queue priority: 0.628
- Required move: Turn an abstract schema into explicit natural example families or prove that the schema cannot instantiate naturally in the current way.
- Abstraction required: A construction template, example-generating reduction family, or a canonicalization principle for natural examples.
- Minimal theorem shape: From abstract schema S, construct an explicit family of natural instances E_n satisfying properties P and realizing target theorem T.
- Major subresult type: standalone theorem
- Queue IDs: proofq.p-vs-np.007, proofq.p-vs-np.015, proofq.p-vs-np.022
- Reference IDs: mathlibref.p-vs-np.008

#### Search Modes

- canonical example construction
- template instantiation
- example-preserving reduction search

#### Anti-Patterns

- restating the schema as if it already supplied examples
- listing examples without a constructive route from the local abstraction

#### Effect Notes

- The NP-complete examples route is now target-grounded: the open step is constructing or transferring explicit examples from the local abstraction, not discovering that natural NP-complete problems exist.

#### Sample Frontier Statements

- There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A language L is emph NP-complete (under le_m^p ) iff (i) LinNP holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification and yields NP-complete under polynomial-time many-one reductions.
- An adequate `reduction-gadget-family` bridge concept for `bridge.012` is a `family of reductions preserving the route witness structure` named `unspecified reduction gadget family` that absorbs `NP-completeness`, preserves `consequence schema NP-complete-classification`, and is strong enough to force `NP-complete-classification`.
- Construct a reduction family that turns the abstract schema `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` into concrete natural examples realizing `NP-complete under polynomial-time many-one reductions`.

### characterization-bridge

- Breakthrough family: semantic bridge
- Pressure score: 1.621
- Top queue priority: 0.590
- Required move: Bridge a local definitional object to a global characterization theorem.
- Abstraction required: A semantic correspondence, duality, witness extraction principle, or completeness notion that turns the local definition into the target biconditional.
- Minimal theorem shape: Local definitional object D has property P if and only if global characterization condition Q holds, with both directions proved at the right level of abstraction.
- Major subresult type: transfer principle
- Queue IDs: proofq.p-vs-np.006, proofq.p-vs-np.014, proofq.p-vs-np.024
- Reference IDs: mathlibref.p-vs-np.006

#### Search Modes

- semantic correspondence theorem
- duality or normal form search
- two-way implication decomposition

#### Anti-Patterns

- normalizing syntax without adding semantic force
- treating a definition as if it already contained the characterization

#### Effect Notes

- The Cook-Reckhow route is now clearly a bridge problem, not a target-theorem problem: the open step is the semantic bridge from the local definitional object to this existing characterization theorem.

#### Sample Frontier Statements

- There exists an admissible TAUT proof progress measure, realized as a monotone potential function over proofs or certificates, such that whenever A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is... holds for TAUT in Cook-Reckhow-proof-system, the object organizes the source-side mathematical content while preserving the invariant TAUT complexity profile in Cook-Reckhow-proof-system and yields There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP.
- An adequate `normal-form-translation` bridge concept for `bridge.003` is a `translation map between the source and target encodings` named `TAUT transport normal form` that absorbs `proof-system-characterization`, preserves `TAUT complexity profile in Cook-Reckhow-proof-system`, and is strong enough to force `TAUT-proof-system-characterization`.
- Prove the semantic bridge needed to turn the definitional source statement `A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is...` into the characterization `There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP`, rather than only normalizing encodings.

### explicitness-gap

- Breakthrough family: explicitness
- Pressure score: 1.342
- Top queue priority: 0.686
- Required move: Add uniform, explicit, efficiently constructible content to an otherwise semantic object.
- Abstraction required: A uniform construction rule, extractor, or explicit family indexed by input length and class parameters.
- Minimal theorem shape: For every length parameter n, the existential object C_n can be constructed or certified explicitly in time class X while preserving property P.
- Major subresult type: bridge object/tool
- Queue IDs: proofq.p-vs-np.016, proofq.p-vs-np.017
- Reference IDs: mathlibref.p-vs-np.004

#### Search Modes

- uniformization
- effective construction
- certificate extraction

#### Anti-Patterns

- accepting existence without algorithmic access
- shifting to a broader semantic object that is still non-explicit

#### Effect Notes

- The PIT route is not blocked by the total absence of a hitting-set-to-PIT connection; it is blocked by the lack of an explicit generator or certificate object for the right class.

#### Sample Frontier Statements

- An adequate `algebraic-certificate` bridge concept for `bridge.013` is a `checkable certificate map or algebraic witness relation` named `PIT certificate family` that absorbs `PIT-derandomization-assumption`, preserves `PIT semantic object`, and is strong enough to force `NEXP-vs-P/poly-or-Permanent-lower-bound`.
- Prove an upgrade theorem turning the semantic black-box PIT object behind `PIT certificate family` into an algorithmic PIT-derandomization premise strong enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
