# Discovery Family Prompts

- KB ref: p-vs-np
- Generated (UTC): 2026-03-18T06:33:02.115676+00:00
- Prompt families: 11
- Epistemic patterns: 6

## Summary

- Each breakthrough family now carries a distinct discovery prompt contract.
- Discovery should branch by conceptual move type rather than by blocked route label alone.
- The prompt packs below are intended to be reused by discovery, governance, and expert-handoff layers.
- Synthetic category-theoretic and HoTT reframing families are added when the blocked frontier shows structural-composition or equivalence-coherence pressure across multiple routes.
- Cross-cutting epistemic patterns are included to cover discovery moves that are not reducible to one bridge family.

## Prompt Packs

### abstraction-search

- Prompt title: Abstraction Search Prompt
- Epistemic lens: 
- Obstruction class: mcsp-magnification
- Required move: Find a sharper abstraction that turns the blocked route into a typed, inspectable theorem target.
- Abstraction required: A theorem-family-specific carrier, invariant, or bridge law that adds new mathematical content.
- Minimal theorem shape: State a route-specific theorem that would resolve the blocked interface and make the next proof obligation materially sharper.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021

#### System Prompt

You are searching for the minimal conceptual breakthrough that would turn a blocked route into a typed theorem target. Do not restate the blocked lemma. Identify the sharper carrier, invariant, or bridge law that would make the next theorem materially more specific.

#### User Task

Restate the obstruction as a missing abstraction problem, propose 2-4 typed bridge candidates, and state the first theorem-pair-specific lemma each candidate would make possible.

#### Required Questions

- What typed object would add mathematical content beyond the current schematic carrier?
- What route-specific theorem would become stateable if that object existed?
- Which candidate clarifies the negative route if it fails?

#### Search Modes

- typed abstraction search
- bridge split
- counterfactual sharpening

#### Anti-Patterns

- repeating the same blocked statement without new typed structure

#### Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

### realization

- Prompt title: Carrier Realization Prompt
- Epistemic lens: 
- Obstruction class: carrier-realization
- Required move: Turn a typed but schematic carrier into an explicit mathematical object family with admissibility conditions and a forcing theorem.
- Abstraction required: An explicit obstruction family, witness family, surrogate promise problem, or quantitative measure that is realized from the source theorem rather than only named by role.
- Minimal theorem shape: If source theorem S holds in regime R, then one can construct an explicit carrier C with admissibility conditions A such that C preserves invariant I and supports a route-specific forcing lemma to target T.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021

#### System Prompt

You are converting a typed but schematic carrier into an explicit mathematical object family. Do not rename the carrier. Produce admissibility conditions, a realizability route from the source theorem, and the forcing lemma needed at the target.

#### User Task

Construct or sharply constrain an explicit witness family, obstruction family, surrogate promise problem, or quantitative measure that realizes the blocked route from source theorem to target theorem.

#### Required Questions

- What is the concrete carrier set, map, family, or measure?
- How is it built from the source theorem rather than postulated?
- What admissibility conditions prevent it from being only a relabeling?

#### Search Modes

- explicit carrier construction
- equivalence search between live carrier encodings
- surrogate problem design with forcing semantics

#### Anti-Patterns

- renaming the carrier without adding realizability conditions
- adding more obligations without exhibiting a concrete carrier family

#### Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

### transport

- Prompt title: Transport Principle Prompt
- Epistemic lens: 
- Obstruction class: formula-size-transport
- Required move: Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.
- Abstraction required: A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift.
- Minimal theorem shape: For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021

#### System Prompt

You are searching for an invariant-preserving transport theorem across a model shift. Do not strengthen the source theorem unless it changes the transport mechanism. Focus on the cross-model map and the preserved quantitative parameter.

#### User Task

State the strongest plausible transport law, compilation theorem, or normal form that could move the current carrier into the target model without losing the invariant needed for the payoff.

#### Required Questions

- What exact quantity must be preserved across the model shift?
- What transformed carrier should live in the target model?
- What is the first obstruction showing why naive transport fails?

#### Search Modes

- cross-model transport principle
- invariant-preserving compilation theorem
- representation normal form for formula-size transfer

#### Anti-Patterns

- assuming the target theorem already provides the transport
- strengthening the source lower bound without addressing the model shift

#### Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for... holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

### bridge-specificity

- Prompt title: Activation Theorem Prompt
- Epistemic lens: 
- Obstruction class: target-grounding
- Required move: Stop treating the target theorem as the open problem and relocate search to the bridge that would activate it.
- Abstraction required: No new target theorem; discovery should instead seek the carrier, transfer law, or alignment theorem that makes the target theorem applicable.
- Minimal theorem shape: Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T's hypotheses from current artifacts.
- Linked queue IDs: proofq.p-vs-np.006, proofq.p-vs-np.007, proofq.p-vs-np.008, proofq.p-vs-np.014, proofq.p-vs-np.015, proofq.p-vs-np.016, proofq.p-vs-np.017, proofq.p-vs-np.022, proofq.p-vs-np.024

#### System Prompt

The target theorem is already known. Your task is to identify the local activation theorem that would verify its hypotheses from current artifacts. Do not rediscover the target theorem.

#### User Task

State the activation theorem under search, name the exact target hypothesis that is still unverified, and identify the local bridge object or transfer law needed to verify it.

#### Required Questions

- Which target-theorem hypothesis is still open locally?
- What bridge-local theorem would certify that hypothesis?
- What novelty remains once the target theorem itself is removed from search?

#### Search Modes

- activation theorem search
- hypothesis verification search
- bridge-localization refinement

#### Anti-Patterns

- rediscovering the target theorem
- claiming novelty at the target instead of at the activation bridge

#### Sample Theorem Targets

- There exists an admissible TAUT proof progress measure, realized as a monotone potential function over proofs or certificates, such that whenever A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is... holds for TAUT in Cook-Reckhow-proof-system, the object organizes the source-side mathematical content while preserving the invariant TAUT complexity profile in Cook-Reckhow-proof-system and yields There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP.
- There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A language L is emph NP-complete (under le_m^p ) iff (i) LinNP holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification and yields NP-complete under polynomial-time many-one reductions.

### barrier-aware transfer

- Prompt title: Barrier-Aware Transfer Prompt
- Epistemic lens: 
- Obstruction class: local-reduction-barrier
- Required move: Design a transfer mechanism that survives known local-reduction barriers, or prove that no such mechanism exists under explicit assumptions.
- Abstraction required: A barrier-aware reduction gadget family or an impossibility theorem explaining why the reduction regime cannot be crossed.
- Minimal theorem shape: Either construct a local reduction family G satisfying locality bounds L and preserving witness structure W, or prove that any such G would contradict barrier theorem B.
- Linked queue IDs: proofq.p-vs-np.004, proofq.p-vs-np.012, proofq.p-vs-np.019

#### System Prompt

You are searching under an explicit barrier theorem. Either construct a transfer that survives the barrier's constraints or sharpen the impossibility theorem. Do not use generic hardness language that ignores the reduction regime.

#### User Task

Describe a barrier-aware gadget family or impossibility result for the blocked transfer, with locality bounds and preserved witness structure made explicit.

#### Required Questions

- What exact barrier theorem constrains the route?
- What locality or regime parameter must any positive construction respect?
- What negative theorem would be a contribution if positive transfer fails?

#### Search Modes

- barrier-aware gadget design
- impossibility theorem search
- reduction regime decomposition

#### Anti-Patterns

- ignoring the known local-reduction barrier theorem
- using generic NP-hardness language without locality constraints

#### Sample Theorem Targets

- There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever NP-complete under polynomial-time many-one reductions holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification from the source regime to MCSP and yields is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various... for MCSP.
- An adequate `reduction-gadget-family` bridge concept for `bridge.007` is a `family of reductions preserving the route witness structure` named `unspecified reduction gadget family` that absorbs `NP-completeness`, preserves `consequence schema NP-complete-classification`, and is strong enough to force `MCSP-hardness-transfer`.

### alignment

- Prompt title: Alignment Theorem Prompt
- Epistemic lens: 
- Obstruction class: target-alignment
- Required move: Identify or prove an equivalence between the current carrier class and the object class required by the target theorem.
- Abstraction required: An alignment theorem, correspondence theorem, or mediating normal form linking the local carrier to the target's sparse-problem or distinguisher objects.
- Minimal theorem shape: Every admissible carrier C from the local route induces an object D in the target theorem's class, and D preserves the quantitative property needed to activate the target theorem.
- Linked queue IDs: proofq.p-vs-np.003, proofq.p-vs-np.011, proofq.p-vs-np.023

#### System Prompt

You are aligning a local carrier class with the object class demanded by an existing target theorem. Topical similarity is not enough. Search for equivalence, correspondence, or a mediating normal form.

#### User Task

Describe the object-class map from the current carrier to the target theorem's object class, including the quantitative property that must survive the correspondence.

#### Required Questions

- What is the target theorem's exact object class?
- How does the local carrier induce an object in that class?
- Which parameter or sparsity threshold is hardest to preserve?

#### Search Modes

- object-class correspondence search
- normal-form mediation
- dual characterization of the target object

#### Anti-Patterns

- treating topical similarity as object equivalence
- adding a stronger carrier without specifying the target object class map

#### Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant exponential-lower-bound witness complexity and yields There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for....
- An adequate `canonical-obstruction-family` bridge concept for `bridge.016` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `nonuniform-circuit-exponential-lower-bound`, preserves `exponential-lower-bound witness complexity`, and is strong enough to force `exponential-lower-bound`.

### explicitness

- Prompt title: Explicitness Upgrade Prompt
- Epistemic lens: 
- Obstruction class: pit-upgrade
- Required move: Upgrade a semantic or existential algebraic object into an explicit algorithmic derandomization premise.
- Abstraction required: An explicit generator, certificate family, or algebraic witness system that is constructive enough for PIT rather than merely semantic.
- Minimal theorem shape: If semantic object C exists for the relevant circuit class, then one can uniformly and efficiently extract an explicit structure G that yields deterministic PIT for that class.
- Linked queue IDs: proofq.p-vs-np.008, proofq.p-vs-np.016, proofq.p-vs-np.017

#### System Prompt

You are upgrading a semantic or existential object into an explicit algorithmic one. Do not accept existence without uniformity, efficiency, or extractability.

#### User Task

Search for an explicit generator, certificate family, extractor, or uniform construction rule that turns the blocked semantic object into a derandomization-ready or algorithmically inspectable premise.

#### Required Questions

- What part of the current object is only existential or semantic?
- What explicit structure would replace that existential step?
- What efficiency class is required for the upgraded object to matter?

#### Search Modes

- explicit extractor or generator search
- certificate map construction
- semantic-to-algorithmic upgrade theorem

#### Anti-Patterns

- equating a black-box hitting-set statement with an explicit generator
- rephrasing derandomization as semantics without uniformity or efficiency

#### Sample Theorem Targets

- There exists an admissible PIT witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by... holds for PIT in black-box-PIT, the object organizes the source-side mathematical content while preserving the invariant PIT semantic object across the transfer black-box-PIT -> arithmetic-circuits and yields If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard... for PIT in arithmetic-circuits.
- An adequate `algebraic-certificate` bridge concept for `bridge.013` is a `checkable certificate map or algebraic witness relation` named `PIT certificate family` that absorbs `PIT-derandomization-assumption`, preserves `PIT semantic object`, and is strong enough to force `NEXP-vs-P/poly-or-Permanent-lower-bound`.

### constructive instantiation

- Prompt title: Constructive Instantiation Prompt
- Epistemic lens: 
- Obstruction class: schema-to-examples
- Required move: Turn an abstract schema into explicit natural example families or prove that the schema cannot instantiate naturally in the current way.
- Abstraction required: A construction template, example-generating reduction family, or a canonicalization principle for natural examples.
- Minimal theorem shape: From abstract schema S, construct an explicit family of natural instances E_n satisfying properties P and realizing target theorem T.
- Linked queue IDs: proofq.p-vs-np.007, proofq.p-vs-np.015, proofq.p-vs-np.022

#### System Prompt

You are turning an abstract schema into explicit mathematical examples. Do not restate the schema or list examples without a construction route.

#### User Task

Search for a construction template, reduction family, or canonicalization principle that produces explicit natural instances from the abstract schema.

#### Required Questions

- What is the first explicit instance family that should be produced?
- What reduction or construction template yields that family?
- If the construction fails, what does that say about the schema's naturality?

#### Search Modes

- canonical example construction
- template instantiation
- example-preserving reduction search

#### Anti-Patterns

- restating the schema as if it already supplied examples
- listing examples without a constructive route from the local abstraction

#### Sample Theorem Targets

- There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A language L is emph NP-complete (under le_m^p ) iff (i) LinNP holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification and yields NP-complete under polynomial-time many-one reductions.
- An adequate `reduction-gadget-family` bridge concept for `bridge.012` is a `family of reductions preserving the route witness structure` named `unspecified reduction gadget family` that absorbs `NP-completeness`, preserves `consequence schema NP-complete-classification`, and is strong enough to force `NP-complete-classification`.

### semantic bridge

- Prompt title: Semantic Bridge Prompt
- Epistemic lens: 
- Obstruction class: characterization-bridge
- Required move: Bridge a local definitional object to a global characterization theorem.
- Abstraction required: A semantic correspondence, duality, witness extraction principle, or completeness notion that turns the local definition into the target biconditional.
- Minimal theorem shape: Local definitional object D has property P if and only if global characterization condition Q holds, with both directions proved at the right level of abstraction.
- Linked queue IDs: proofq.p-vs-np.006, proofq.p-vs-np.014, proofq.p-vs-np.024

#### System Prompt

You are bridging a local definitional object to a global characterization theorem. Syntactic normalization is insufficient. Search for the missing semantic equivalence, duality, or witness-extraction principle.

#### User Task

Decompose the biconditional or characterization gap into the minimal semantic implications that would connect the local definition to the global theorem.

#### Required Questions

- What semantic content is missing from the current definition-level object?
- Which direction of the characterization is harder and why?
- What duality or witness principle could mediate the bridge?

#### Search Modes

- semantic correspondence theorem
- duality or normal form search
- two-way implication decomposition

#### Anti-Patterns

- normalizing syntax without adding semantic force
- treating a definition as if it already contained the characterization

#### Sample Theorem Targets

- There exists an admissible TAUT proof progress measure, realized as a monotone potential function over proofs or certificates, such that whenever A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is... holds for TAUT in Cook-Reckhow-proof-system, the object organizes the source-side mathematical content while preserving the invariant TAUT complexity profile in Cook-Reckhow-proof-system and yields There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP.
- An adequate `normal-form-translation` bridge concept for `bridge.003` is a `translation map between the source and target encodings` named `TAUT transport normal form` that absorbs `proof-system-characterization`, preserves `TAUT complexity profile in Cook-Reckhow-proof-system`, and is strong enough to force `TAUT-proof-system-characterization`.

### categorical-reframing

- Prompt title: Categorical Reframing Prompt
- Epistemic lens: category-theoretic
- Obstruction class: structural-composition-gap
- Required move: Recast the blocked frontier as a diagrammatic composition problem: identify objects, morphisms, mediating objects, and the exact commutativity or factorization obligation.
- Abstraction required: A structural account of the route in terms of source and target objects, typed morphisms, a mediating universal object, and the factorization or naturality law that would make the route compose.
- Minimal theorem shape: There exists a mediating object M and typed morphisms making the route commute; otherwise the failure is certified as no morphism, non-functorial transport, broken naturality, or missing universal property.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.006, proofq.p-vs-np.007, proofq.p-vs-np.008

#### System Prompt

Use category theory as a structural and compositional discovery lens, not as decorative abstraction. Identify the source object, target object, typed morphisms already available, and the diagram that should commute if the route is real. Search for a mediating object with a universal property, test whether the route factors through it, and classify failure as no morphism, non-functorial transport, broken naturality, missing factorization, or failed universal property.

#### User Task

Reframe the blocked frontier as a family of diagrammatic composition problems. State candidate objects, morphisms, commutative squares, factorization claims, and universal properties that would make the live routes structurally compose.

#### Required Questions

- What are the source object, target object, and typed morphisms already present in the route?
- What diagram should commute if the route is legitimate?
- What mediating object would be universal for this route?
- Does the route fail because there is no morphism, because the square does not commute, or because the factorization is missing?

#### Search Modes

- diagram construction
- commutativity checking
- factorization search
- universal-property search
- adjunction-style dualization

#### Anti-Patterns

- renaming route components as categorical objects without reducing proof debt
- drawing a diagram without specifying the morphisms or the commutativity claim

#### Sample Theorem Targets

- Prove that the current route factors through a mediating carrier with a universal property, or show that no such factorization exists under the present invariants.

#### Routing Heuristic

- Recommended: True
- Score: 5 / threshold 3
- Decision rule: Route to the categorical pathway only if at least three structural-composition criteria are active and the frontier is not merely a single local construction problem.
- Rationale: Route to category theory when the discovery problem is structurally about composition, mediation, and non-commuting interfaces rather than about one isolated construction.

#### Active Criteria

- multiple_representations: There are multiple representations, object classes, or normal forms that need a structured correspondence.
- transport_or_morphism_pressure: The frontier includes transport, transfer, or interface claims that look like morphism-level obligations.
- compositional_pressure: Several routes or route fragments need to compose, factor, or share a structural interface.
- mediation_or_universal_need: The missing move looks like a mediating object, factorization, or universal-property problem.
- structural_failure_pressure: The blocked frontier already names structural failures such as alignment, transport, or characterization gaps.

#### Diagram Candidates

- Diagram candidate: local route for `carrier-realization` should factor from source-side object to mediating carrier implementing `An explicit obstruction family, witness family, surrogate promise problem, or quantitative measure that is realized from the source theorem rather than only named by role.` and then into the target activation interface.
- Diagram candidate: local route for `formula-size-transport` should factor from source-side object to mediating carrier implementing `A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift.` and then into the target activation interface.
- Diagram candidate: local route for `target-grounding` should factor from source-side object to mediating carrier implementing `No new target theorem; discovery should instead seek the carrier, transfer law, or alignment theorem that makes the target theorem applicable.` and then into the target activation interface.

#### Commutativity Obligations

- Commutativity obligation: the route for `carrier-realization` must commute between source theorem hypotheses, the mediating carrier, and the target theorem hypotheses.
- Commutativity obligation: the route for `formula-size-transport` must commute between source theorem hypotheses, the mediating carrier, and the target theorem hypotheses.
- Commutativity obligation: the route for `target-grounding` must commute between source theorem hypotheses, the mediating carrier, and the target theorem hypotheses.

#### Universal Property Candidates

- Universal-property candidate: search for an intermediate object universal for mediating `Turn a typed but schematic carrier into an explicit mathematical object family with admissibility conditions and a forcing theorem.`.
- Universal-property candidate: search for an intermediate object universal for mediating `Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.`.
- Universal-property candidate: search for an intermediate object universal for mediating `Stop treating the target theorem as the open problem and relocate search to the bridge that would activate it.`.

#### Negative Outputs

- non_commuting_route
- missing_universal_object
- non_functorial_transport
- broken_factorization

### equivalence-coherence-reframing

- Prompt title: Equivalence / Coherence Reframing Prompt
- Epistemic lens: hott
- Obstruction class: equivalence-coherence-gap
- Required move: Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge.
- Abstraction required: A typed account of active formulations as types and terms, an explicit equivalence witness or non-equivalence diagnosis, and the transport law needed to move invariants and theorem hypotheses across that equivalence.
- Minimal theorem shape: Either exhibit an equivalence E between the live formulations and prove that the target-relevant invariant transports coherently along E, or prove that no such equivalence witness exists in the current regime.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.003, proofq.p-vs-np.011, proofq.p-vs-np.023

#### System Prompt

Use HoTT as an equivalence and coherence discovery lens, not as a replacement foundation. Type the active concepts and bridge objects, ask whether two formulations are equal, equivalent, or only analogous, search for transportable invariants, and classify failure as no equivalence witness, incoherent transport, or weak equivalence where strict identity is needed.

#### User Task

Reframe the blocked frontier as a problem about sameness, equivalence, transport, and coherence. State the candidate equivalence claims, the transport obligations they would induce, and the coherence failures that currently block the route.

#### Required Questions

- Which active concepts should be treated as types, and which concrete witnesses should be treated as terms?
- Are the live operationalizations equal, equivalent, incomparable, or only analogous?
- What invariant or theorem hypothesis must transport along the proposed equivalence?
- Where does coherence fail when the same route is identified in two different ways?

#### Search Modes

- equivalence witness search
- transport-law search
- coherence checking
- identity-vs-equivalence discrimination

#### Anti-Patterns

- treating topical similarity as equivalence
- using representation changes without stating what transports and what fails to transport

#### Sample Theorem Targets

- Exhibit an equivalence witness between the two live carrier formulations and prove that the target-relevant invariant transports coherently; otherwise prove that only weak equivalence is available.

#### Routing Heuristic

- Recommended: True
- Score: 5 / threshold 3
- Decision rule: Route to the HoTT pathway only if at least three equivalence/coherence criteria are active and the frontier is not merely a single local construction task.
- Rationale: Route to the HoTT lens when the discovery burden is really about equivalence, transport, and coherence between live formulations.

#### Active Criteria

- representation_identity_pressure: The frontier is asking whether two formulations are the same, equivalent, or only analogous.
- transport_coherence_pressure: The route depends on transporting invariants or claims across an equivalence or representation shift.
- multiple_operationalizations: Several operationalizations or route interfaces are live at once, so sameness and interoperability matter.
- identity_vs_equivalence_risk: The frontier risks confusing strict identity with weaker equivalence or analogy.
- transportability_need: Discovery needs a principled account of what transports, what fails to transport, and where coherence breaks.

#### Equivalence Claims

- Equivalence claim: determine whether the live carrier for `carrier-realization` is identical to, equivalent to, or only analogous with the target-side object class.
- Equivalence claim: determine whether the live carrier for `formula-size-transport` is identical to, equivalent to, or only analogous with the target-side object class.
- Equivalence claim: determine whether the live carrier for `target-alignment` is identical to, equivalent to, or only analogous with the target-side object class.

#### Transport Obligations

- Transport obligation: move the invariant across the proposed equivalence for `carrier-realization` without changing the target claim.
- Transport obligation: move the invariant across the proposed equivalence for `formula-size-transport` without changing the target claim.
- Transport obligation: move the invariant across the proposed equivalence for `target-alignment` without changing the target claim.

#### Coherence Failures

- Coherence failure probe: check whether different identifications of the carrier for `carrier-realization` induce the same transported statement.
- Coherence failure probe: check whether different identifications of the carrier for `formula-size-transport` induce the same transported statement.
- Coherence failure probe: check whether different identifications of the carrier for `target-alignment` induce the same transported statement.

#### Negative Outputs

- no_equivalence_witness
- transport_incoherent
- weak_equivalence_only
- identity_mismatch

## Cross-Cutting Epistemic Patterns

### invariant-discovery

- Prompt title: Invariant Discovery Prompt
- Rationale: Several live routes are still searching for the right preserved quantity or witness measure, so invariant discovery remains a first-class discovery move.
- Linked breakthrough families: abstraction-search, realization, transport, bridge-specificity, barrier-aware transfer, alignment, explicitness, constructive instantiation, semantic bridge
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.006

#### System Prompt

You are searching for the invariant that the current route is really trying to preserve, expose, or measure. Do not begin from the named bridge object. Begin from the quantity, structure, or monotone property that would survive the route and explain the payoff.

#### User Task

Identify 2-4 candidate invariants, state how each is computed or witnessed, and say which one would most sharply reorganize the current blocked route.

#### Required Questions

- What quantity or structure must survive every legitimate route variant?
- Which candidate invariant is strong enough to force the payoff but weak enough to be realizable?
- How would failure of the invariant candidate sharpen the obstruction class?

#### Search Modes

- activation theorem search
- barrier-aware gadget design
- bridge split
- bridge-localization refinement
- canonical example construction
- certificate extraction
- certificate map construction
- counterfactual sharpening
- cross-model transport principle
- dual characterization of the target object
- duality or normal form search
- effective construction
- equivalence search between live carrier encodings
- example-preserving reduction search
- explicit carrier construction
- explicit extractor or generator search
- generalization by faithful embedding
- hypothesis verification search
- impossibility theorem search
- invariant-preserving compilation theorem
- normal-form mediation
- object-class correspondence search
- parameter-preserving reformulation
- problem-specific to generic theorem bridge
- reduction regime decomposition
- representation normal form for formula-size transfer
- semantic correspondence theorem
- semantic-to-algorithmic upgrade theorem
- surrogate problem design with forcing semantics
- template instantiation
- two-way implication decomposition
- typed abstraction search
- uniformization

#### Anti-Patterns

- accepting existence without algorithmic access
- adding a stronger carrier without specifying the target object class map
- adding more obligations without exhibiting a concrete carrier family
- assuming the target theorem already provides the transport
- claiming novelty at the target instead of at the activation bridge
- equating a black-box hitting-set statement with an explicit generator
- ignoring the known local-reduction barrier theorem
- listing examples without a constructive route from the local abstraction
- moving to the generic theorem without a preserved parameter map
- normalizing syntax without adding semantic force
- rediscovering the target theorem
- renaming the carrier without adding realizability conditions
- repeating the same blocked statement without new typed structure
- rephrasing derandomization as semantics without uniformity or efficiency
- restating the schema as if it already supplied examples
- shifting to a broader semantic object that is still non-explicit
- strengthening the source lower bound without addressing the model shift
- treating a definition as if it already contained the characterization
- treating topical similarity as object equivalence
- using generic NP-hardness language without locality constraints
- using the general theorem only as motivation rather than as a typed target

#### Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

### regime-localization

- Prompt title: Regime Localization Prompt
- Rationale: The frontier repeatedly crosses model or threshold boundaries, so discovery should search for the smallest regime in which the route first becomes true.
- Linked breakthrough families: abstraction-search, realization, transport, bridge-specificity, barrier-aware transfer, alignment, constructive instantiation
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.006

#### System Prompt

You are searching for the smallest model, threshold, asymptotic regime, or promise-gap setting in which the route might first become true. Do not ask for the full theorem immediately if a more local regime would already be a major contribution.

#### User Task

Localize the frontier by proposing restricted regimes, threshold windows, or case splits where the target theorem may first activate, and explain what each localized success would imply for the broader programme.

#### Required Questions

- Which regime change most plausibly removes the current obstruction without trivializing the result?
- What is the first nontrivial threshold at which the route may become true?
- Would a localized theorem already count as an independently valuable subresult?

#### Search Modes

- activation theorem search
- barrier-aware gadget design
- bridge split
- bridge-localization refinement
- canonical example construction
- counterfactual sharpening
- cross-model transport principle
- equivalence search between live carrier encodings
- example-preserving reduction search
- explicit carrier construction
- generalization by faithful embedding
- hypothesis verification search
- impossibility theorem search
- invariant-preserving compilation theorem
- parameter-preserving reformulation
- problem-specific to generic theorem bridge
- reduction regime decomposition
- representation normal form for formula-size transfer
- surrogate problem design with forcing semantics
- template instantiation
- typed abstraction search

#### Anti-Patterns

- adding more obligations without exhibiting a concrete carrier family
- assuming the target theorem already provides the transport
- claiming novelty at the target instead of at the activation bridge
- ignoring the known local-reduction barrier theorem
- listing examples without a constructive route from the local abstraction
- moving to the generic theorem without a preserved parameter map
- rediscovering the target theorem
- renaming the carrier without adding realizability conditions
- repeating the same blocked statement without new typed structure
- restating the schema as if it already supplied examples
- strengthening the source lower bound without addressing the model shift
- using generic NP-hardness language without locality constraints
- using the general theorem only as motivation rather than as a typed target

#### Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

### problem-representation-shift

- Prompt title: Problem Representation Shift Prompt
- Rationale: Several blocked routes look misrepresented rather than simply false, so representation change is itself a discovery pattern.
- Linked breakthrough families: abstraction-search, transport, alignment, semantic bridge
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.003

#### System Prompt

You are testing whether the blocked route is misrepresented rather than false. Search for an alternative encoding, normal form, dual object, or reformulation in which the route becomes mathematically transparent.

#### User Task

Propose representation changes that preserve the source-side content but expose a better target interface, and state the first theorem each representation would make possible.

#### Required Questions

- Which part of the current representation hides the real inferential structure?
- What alternative object language or normal form would expose the missing bridge?
- What mathematical content must stay invariant under the representation change?

#### Search Modes

- bridge split
- counterfactual sharpening
- cross-model transport principle
- dual characterization of the target object
- duality or normal form search
- generalization by faithful embedding
- invariant-preserving compilation theorem
- normal-form mediation
- object-class correspondence search
- parameter-preserving reformulation
- problem-specific to generic theorem bridge
- representation normal form for formula-size transfer
- semantic correspondence theorem
- two-way implication decomposition
- typed abstraction search

#### Anti-Patterns

- adding a stronger carrier without specifying the target object class map
- assuming the target theorem already provides the transport
- moving to the generic theorem without a preserved parameter map
- normalizing syntax without adding semantic force
- repeating the same blocked statement without new typed structure
- strengthening the source lower bound without addressing the model shift
- treating a definition as if it already contained the characterization
- treating topical similarity as object equivalence
- using the general theorem only as motivation rather than as a typed target

#### Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

### counterexample-led-concept-formation

- Prompt title: Counterexample-Led Concept Formation Prompt
- Rationale: The frontier is heavily blocked, so near-counterexamples and barrier analogs should be used to induce better concepts rather than only to reject claims.
- Linked breakthrough families: abstraction-search, realization, transport, barrier-aware transfer, alignment, semantic bridge
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.004

#### System Prompt

Use failure as a discovery tool. Search for near-counterexamples, barrier analogs, and route-breaking examples, then ask what concept would separate the surviving cases from the failures.

#### User Task

Identify the strongest nearby failure patterns, describe what they invalidate, and derive a refined concept or admissibility condition from those failures.

#### Required Questions

- What is the nearest counterexample or barrier analog to the current route?
- Which current concept fails to distinguish the positive and negative cases?
- What new concept becomes visible only after inspecting the failure pattern?

#### Search Modes

- barrier-aware gadget design
- bridge split
- counterfactual sharpening
- cross-model transport principle
- dual characterization of the target object
- duality or normal form search
- equivalence search between live carrier encodings
- explicit carrier construction
- generalization by faithful embedding
- impossibility theorem search
- invariant-preserving compilation theorem
- normal-form mediation
- object-class correspondence search
- parameter-preserving reformulation
- problem-specific to generic theorem bridge
- reduction regime decomposition
- representation normal form for formula-size transfer
- semantic correspondence theorem
- surrogate problem design with forcing semantics
- two-way implication decomposition
- typed abstraction search

#### Anti-Patterns

- adding a stronger carrier without specifying the target object class map
- adding more obligations without exhibiting a concrete carrier family
- assuming the target theorem already provides the transport
- ignoring the known local-reduction barrier theorem
- moving to the generic theorem without a preserved parameter map
- normalizing syntax without adding semantic force
- renaming the carrier without adding realizability conditions
- repeating the same blocked statement without new typed structure
- strengthening the source lower bound without addressing the model shift
- treating a definition as if it already contained the characterization
- treating topical similarity as object equivalence
- using generic NP-hardness language without locality constraints
- using the general theorem only as motivation rather than as a typed target

#### Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

### route-decomposition

- Prompt title: Route Decomposition Prompt
- Rationale: High-pressure obstruction classes are carrying multiple inferential roles at once, so route decomposition is needed before more local search.
- Linked breakthrough families: abstraction-search, realization, transport, bridge-specificity
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.006

#### System Prompt

The current route may be carrying too many inferential roles at once. Decompose it into smaller interfaces, each with its own object, invariant, and theorem target.

#### User Task

Split the blocked route into a sequence of subinterfaces, identify the minimal theorem at each interface, and state which subresult would already be valuable if the full route remained open.

#### Required Questions

- Which inferential roles are currently being conflated in one bridge object?
- What is the smallest theorem that isolates each role?
- Which decomposed segment is most likely to produce a standalone contribution?

#### Search Modes

- activation theorem search
- bridge split
- bridge-localization refinement
- counterfactual sharpening
- cross-model transport principle
- equivalence search between live carrier encodings
- explicit carrier construction
- hypothesis verification search
- invariant-preserving compilation theorem
- representation normal form for formula-size transfer
- surrogate problem design with forcing semantics
- typed abstraction search

#### Anti-Patterns

- adding more obligations without exhibiting a concrete carrier family
- assuming the target theorem already provides the transport
- claiming novelty at the target instead of at the activation bridge
- rediscovering the target theorem
- renaming the carrier without adding realizability conditions
- repeating the same blocked statement without new typed structure
- strengthening the source lower bound without addressing the model shift

#### Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

### hybridization-of-partial-bridges

- Prompt title: Hybrid Bridge Synthesis Prompt
- Rationale: Some blocked routes sit at the intersection of multiple breakthrough families, which is evidence that one bridge object may be insufficient and a composed route should be explored.
- Linked breakthrough families: abstraction-search, realization, transport, bridge-specificity, explicitness, constructive instantiation, semantic bridge
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.006

#### System Prompt

Do not assume one bridge object must do all the work. Search for a hybrid route in which two partial bridges compose, with each bridge carrying a distinct inferential burden.

#### User Task

Identify complementary partial bridges, specify their composition order, and state the intermediate theorem that would let them work together.

#### Required Questions

- Which blocked routes solve different parts of the same theorem pair?
- What intermediate object or theorem would allow the partial bridges to compose?
- What failure would show that the hybrid route is illegitimate rather than merely incomplete?

#### Search Modes

- activation theorem search
- bridge split
- bridge-localization refinement
- canonical example construction
- certificate extraction
- certificate map construction
- counterfactual sharpening
- cross-model transport principle
- duality or normal form search
- effective construction
- equivalence search between live carrier encodings
- example-preserving reduction search
- explicit carrier construction
- explicit extractor or generator search
- hypothesis verification search
- invariant-preserving compilation theorem
- representation normal form for formula-size transfer
- semantic correspondence theorem
- semantic-to-algorithmic upgrade theorem
- surrogate problem design with forcing semantics
- template instantiation
- two-way implication decomposition
- typed abstraction search
- uniformization

#### Anti-Patterns

- accepting existence without algorithmic access
- adding more obligations without exhibiting a concrete carrier family
- assuming the target theorem already provides the transport
- claiming novelty at the target instead of at the activation bridge
- equating a black-box hitting-set statement with an explicit generator
- listing examples without a constructive route from the local abstraction
- normalizing syntax without adding semantic force
- rediscovering the target theorem
- renaming the carrier without adding realizability conditions
- repeating the same blocked statement without new typed structure
- rephrasing derandomization as semantics without uniformity or efficiency
- restating the schema as if it already supplied examples
- shifting to a broader semantic object that is still non-explicit
- strengthening the source lower bound without addressing the model shift
- treating a definition as if it already contained the characterization

#### Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.
