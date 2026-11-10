# Discovery Branch State Delta: discexec.p-vs-np.023

- KB ref: p-vs-np
- Branch: disclayer.p-vs-np.family.explicitness
- Generated (UTC): 2026-03-18T06:33:22.989432+00:00
- Status: completed-state-delta

## Branch

- Kind: breakthrough-family
- Epistemic lens: 
- Target: Explicitness Upgrade Prompt
- Routing priority: 2.107
- Required move: Upgrade a semantic or existential algebraic object into an explicit algorithmic derandomization premise.
- Abstraction required: An explicit generator, certificate family, or algebraic witness system that is constructive enough for PIT rather than merely semantic.
- Minimal theorem shape: If semantic object C exists for the relevant circuit class, then one can uniformly and efficiently extract an explicit structure G that yields deterministic PIT for that class.
- Spawn reason: Spawn a dedicated `explicitness` discovery layer because obstruction `pit-upgrade` carries repeated pressure across the blocked frontier.
- Rationale: Upgrade a semantic or existential algebraic object into an explicit algorithmic derandomization premise.

## Local Frontier

- Linked queue items: 3

### proofq.p-vs-np.016

- Bridge: bridge.013
- Priority: 0.686
- Claim type: abstraction-conjecture
- Candidate object: PIT certificate family
- Invariant: PIT semantic object
- Route lemma: Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Conjecture: An adequate `algebraic-certificate` bridge concept for `bridge.013` is a `checkable certificate map or algebraic witness relation` named `PIT certificate family` that absorbs `PIT-derandomization-assumption`, preserves `PIT semantic object`, and is strong enough to force `NEXP-vs-P/poly-or-Permanent-lower-bound`.

### proofq.p-vs-np.017

- Bridge: bridge.013
- Priority: 0.656
- Claim type: repair-lemma
- Candidate object: PIT certificate family
- Invariant: PIT semantic object
- Route lemma: Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Conjecture: Prove an upgrade theorem turning the semantic black-box PIT object behind `PIT certificate family` into an algorithmic PIT-derandomization premise strong enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.

### proofq.p-vs-np.008

- Bridge: bridge.013
- Priority: 0.409
- Claim type: route-conjecture
- Candidate object: PIT witness family
- Invariant: PIT semantic object
- Route lemma: Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Conjecture: There exists an admissible PIT witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by... holds for PIT in black-box-PIT, the object organizes the source-side mathematical content while preserving the invariant PIT semantic object across the transfer black-box-PIT -> arithmetic-circuits and yields If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard... for PIT in arithmetic-circuits.

## Local InformalMathLib Hints

- `mathlib.p-vs-np.blocked.proofq-p-vs-np-017` | PIT Upgrade Lemma: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard... | blocked
  Summary: The PIT upgrade lemma is blocked: the current artifacts still provide only semantic black-box PIT objects, not a local theorem converting them into the algorithmic derandomization premise required by the target theorem.
  Artifact: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\negative-results\mathlib.p-vs-np.blocked.proofq-p-vs-np-017-pit-upgrade-lemma-if-mathrm-pit-in-pclass-or-even-suitable-infinitely-often-dera.md
- `mathlibref.p-vs-np.004` | Hitting-Set Generators Yield Black-Box PIT | external_reference
  Summary: The PIT route is not blocked by the total absence of a hitting-set-to-PIT connection; it is blocked by the lack of an explicit generator or certificate object for the right class.
  Artifact: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.004-hitting-set-generators-yield-black-box-pit.md

## Execution Summary

- Executed discovery branch `disclayer.p-vs-np.family.explicitness` for `Explicitness Upgrade Prompt` over 3 linked blocked queue items. The run keeps the search on `Upgrade a semantic or existential algebraic object into an explicit algorithmic derandomization premise.` and uses obstruction classes `pit-upgrade, explicitness-gap` as the local pressure map.

## State Delta

- Kind: theorem-candidate
- Has state delta: True
- Promotable theorem candidates: 8
- Concept revisions: 0
- Max concretization score: 5
- Summary: This branch pass emitted at least one concrete theorem candidate ready for prove promotion.

## Candidate Claims

- If semantic object C exists for the relevant circuit class, then one can uniformly and efficiently extract an explicit structure G that yields deterministic PIT for that class.
- For bridge.013 toward st.thm.kabanets-impagliazzo-pit-derandomisation-implies, isolate the executable discovery claim `Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.` through the branch focus `explicitness`.

## Theorem Candidates

### Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.

- Statement: There exists an admissible `PIT certificate family` such that `A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by some circuit in mathcal C , there exists mathbf a in H with p(mathbf a )neq 0.` can be organized into a route preserving `PIT semantic object` and thereby supports `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.`.
- Candidate object: PIT certificate family
- Invariant: PIT semantic object
- Origin: heuristic-lens
- Search shape: 
- Concretization: concrete (5)
- Motivation: Upgrade a semantic or existential algebraic object into an explicit algorithmic derandomization premise.

- Quantifier signature: For every admissible `PIT certificate family` on the route from `st.def.hitting-set-for-pit-black-box` to `st.thm.kabanets-impagliazzo-pit-derandomisation-implies`.
- LaTeX theorem: \forall W,\ \mathrm{Adm}(W) \to \exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w).
- Lean-style scaffold: prove_that_a_hitting_set_or_pseudorandom_generator_family_preserves_pit_semantic_object_while_transporting_the_route_from_the_black_box_pit_regime_to_the_arithmetic_circuits_regime_strongly_enough_to_derive_if_mathrm_pit_in_pclass_or_even_suitable_infinitely_often_derandomisations_in_nondeterministic_subexponential_time_in_standard

### Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.

- Statement: There exists an admissible `PIT witness family` such that `A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by some circuit in mathcal C , there exists mathbf a in H with p(mathbf a )neq 0.` can be organized into a route preserving `PIT semantic object` and thereby supports `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.`.
- Candidate object: PIT witness family
- Invariant: PIT semantic object
- Origin: heuristic-lens
- Search shape: 
- Concretization: concrete (5)
- Motivation: Upgrade a semantic or existential algebraic object into an explicit algorithmic derandomization premise.

- Quantifier signature: For every admissible `PIT witness family` on the route from `st.def.hitting-set-for-pit-black-box` to `st.thm.kabanets-impagliazzo-pit-derandomisation-implies`.
- LaTeX theorem: \forall W,\ \mathrm{Adm}(W) \to \exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w).
- Lean-style scaffold: prove_that_a_hitting_set_or_pseudorandom_generator_family_preserves_pit_semantic_object_while_transporting_the_route_from_the_black_box_pit_regime_to_the_arithmetic_circuits_regime_strongly_enough_to_derive_if_mathrm_pit_in_pclass_or_even_suitable_infinitely_often_derandomisations_in_nondeterministic_subexponential_time_in_standard

### Transport theorem for PIT certificate family

- Statement: For every admissible `PIT certificate family`, there is a transport law from `black-box-PIT` to `arithmetic-circuits` that preserves `PIT semantic object` and retains enough strength to activate `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.`.
- Candidate object: PIT certificate family
- Invariant: PIT semantic object
- Origin: lean-bounded-search
- Search shape: transport
- Concretization: concrete (5)
- Motivation: The source and target regimes differ (`black-box-PIT` -> `arithmetic-circuits`), so bounded search should test typed transport laws before asking the LLM for new abstractions.

- Quantifier signature: For every admissible `PIT certificate family` on the route from `st.def.hitting-set-for-pit-black-box` to `st.thm.kabanets-impagliazzo-pit-derandomisation-implies`.
- LaTeX theorem: \forall W,\ \mathrm{Adm}(W) \to \exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w).
- Lean-style scaffold: transport_theorem_for_pit_certificate_family

### Obstruction theorem for PIT certificate family

- Statement: No admissible `PIT certificate family` can simultaneously preserve `PIT semantic object` and realize `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.` under the current route commitments.
- Candidate object: PIT certificate family
- Invariant: PIT semantic object
- Origin: lean-bounded-search
- Search shape: obstruction
- Concretization: concrete (5)
- Motivation: Negative pressure is explicit, so symbolic search should test a theorem-shaped impossibility candidate instead of only refining the constructive route.

- Quantifier signature: For every admissible `PIT certificate family` on the route from `st.def.hitting-set-for-pit-black-box` to `st.thm.kabanets-impagliazzo-pit-derandomisation-implies`.
- LaTeX theorem: \forall W,\ \mathrm{Adm}(W) \to \neg \exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w).
- Lean-style scaffold: obstruction_theorem_for_pit_certificate_family

### Realization theorem for PIT certificate family

- Statement: There exists an admissible `PIT certificate family` whose realization internalizes `A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by some circuit in mathcal C , there exists mathbf a in H with p(mathbf a )neq 0.` while preserving `PIT semantic object` strongly enough to support `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.`.
- Candidate object: PIT certificate family
- Invariant: PIT semantic object
- Origin: lean-bounded-search
- Search shape: realization
- Concretization: concrete (4)
- Motivation: The carrier is already named, so the first bounded search step is to test a realization theorem rather than ask for another abstraction.

- Quantifier signature: For every admissible `PIT certificate family` on the route from `st.def.hitting-set-for-pit-black-box` to `st.thm.kabanets-impagliazzo-pit-derandomisation-implies`.
- LaTeX theorem: \forall W,\ \mathrm{Adm}(W) \to \exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w).
- Lean-style scaffold: realization_theorem_for_pit_certificate_family

### Transport theorem for PIT witness family

- Statement: For every admissible `PIT witness family`, there is a transport law from `black-box-PIT` to `arithmetic-circuits` that preserves `PIT semantic object` and retains enough strength to activate `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.`.
- Candidate object: PIT witness family
- Invariant: PIT semantic object
- Origin: lean-bounded-search
- Search shape: transport
- Concretization: concrete (5)
- Motivation: The source and target regimes differ (`black-box-PIT` -> `arithmetic-circuits`), so bounded search should test typed transport laws before asking the LLM for new abstractions.

- Quantifier signature: For every admissible `PIT witness family` on the route from `st.def.hitting-set-for-pit-black-box` to `st.thm.kabanets-impagliazzo-pit-derandomisation-implies`.
- LaTeX theorem: \forall W,\ \mathrm{Adm}(W) \to \exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w).
- Lean-style scaffold: transport_theorem_for_pit_witness_family

### Obstruction theorem for PIT witness family

- Statement: No admissible `PIT witness family` can simultaneously preserve `PIT semantic object` and realize `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.` under the current route commitments.
- Candidate object: PIT witness family
- Invariant: PIT semantic object
- Origin: lean-bounded-search
- Search shape: obstruction
- Concretization: concrete (5)
- Motivation: Negative pressure is explicit, so symbolic search should test a theorem-shaped impossibility candidate instead of only refining the constructive route.

- Quantifier signature: For every admissible `PIT witness family` on the route from `st.def.hitting-set-for-pit-black-box` to `st.thm.kabanets-impagliazzo-pit-derandomisation-implies`.
- LaTeX theorem: \forall W,\ \mathrm{Adm}(W) \to \neg \exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w).
- Lean-style scaffold: obstruction_theorem_for_pit_witness_family

### Realization theorem for PIT witness family

- Statement: There exists an admissible `PIT witness family` whose realization internalizes `A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by some circuit in mathcal C , there exists mathbf a in H with p(mathbf a )neq 0.` while preserving `PIT semantic object` strongly enough to support `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.`.
- Candidate object: PIT witness family
- Invariant: PIT semantic object
- Origin: lean-bounded-search
- Search shape: realization
- Concretization: concrete (4)
- Motivation: The carrier is already named, so the first bounded search step is to test a realization theorem rather than ask for another abstraction.

- Quantifier signature: For every admissible `PIT witness family` on the route from `st.def.hitting-set-for-pit-black-box` to `st.thm.kabanets-impagliazzo-pit-derandomisation-implies`.
- LaTeX theorem: \forall W,\ \mathrm{Adm}(W) \to \exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w).
- Lean-style scaffold: realization_theorem_for_pit_witness_family

## Lean Search

- Engine: lean-via-lake
- Available: True
- Build ok: True
- Module: AbducerFormal.Generated.PVsNp.DiscexecPVsNp023
- Module path: C:\files\projects\abducer\abducer\AbducerFormal\Generated\PVsNp\DiscexecPVsNp023.lean
- Stdout: Build completed successfully (5 jobs). "READINESS|proofq.p-vs-np.016|10" "SHAPES|proofq.p-vs-np.016|realization,transport,obstruction" "READINESS|proofq.p-vs-np.017|10" "SHAPES|proofq.p-vs-np.017|realization,transport,obstruction" "READINESS|proofq.p-vs-np.008|10" "SHAPES|proofq.p-vs-np.008|realization,transport,obstruction"
- Stderr: 

- Queue proofq.p-vs-np.016: readiness=symbolic-search-ready (score=10) | shapes=realization, transport, obstruction | candidates=3
- Queue proofq.p-vs-np.017: readiness=symbolic-search-ready (score=10) | shapes=realization, transport, obstruction | candidates=3
- Queue proofq.p-vs-np.008: readiness=symbolic-search-ready (score=10) | shapes=realization, transport, obstruction | candidates=3

## Concept Revisions

- No concept revisions were emitted in this pass.

## Native Mathematical Packet Contract

- Required: True
- Applies when: the branch emits a theorem-sized claim, theorem candidate, or route-local lemma
- Representation kind: informal-latex-lean-style
- Required layers: informal, latex, lean_style
- Required fields: quantifier_signature, object_signature, symbol_ledger, latex.theorem_statement, lean_style.scaffold
- Lean-style status: non-executable-scaffold-unless-explicitly-formalized
- Notation rule: Do not use equivalence, transport, coherence, factorization, or commutativity language without naming the carrier, witness/map, invariant-preservation law, and theorem type in notation.

## Required Questions

- What part of the current object is only existential or semantic?
- What explicit structure would replace that existential step?
- What efficiency class is required for the upgraded object to matter?

## Expected Deliverables

- State one theorem-shaped candidate centered on `explicitness` satisfying `If semantic object C exists for the relevant circuit class, then one can uniformly and efficiently extract an explicit structure G that yields deterministic PIT for that class.`.
- Make `An explicit generator, certificate family, or algebraic witness system that is constructive enough for PIT rather than merely semantic.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

## Sample Theorem Targets

- There exists an admissible PIT witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by... holds for PIT in black-box-PIT, the object organizes the source-side mathematical content while preserving the invariant PIT semantic object across the transfer black-box-PIT -> arithmetic-circuits and yields If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard... for PIT in arithmetic-circuits.
- An adequate `algebraic-certificate` bridge concept for `bridge.013` is a `checkable certificate map or algebraic witness relation` named `PIT certificate family` that absorbs `PIT-derandomization-assumption`, preserves `PIT semantic object`, and is strong enough to force `NEXP-vs-P/poly-or-Permanent-lower-bound`.

## Lens Artifacts


## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `equating a black-box hitting-set statement with an explicit generator`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `explicitness` remains purely schematic after the first explicit object or theorem candidate.

## External Framework Search Gate

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: derandomization and generator frameworks, algebraic certificate constructions, extractor / hitter frameworks
- Local prerequisites before browsing:
  - Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
  - State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
  - Reject at least one purely topical analogy before searching for an external framework.
