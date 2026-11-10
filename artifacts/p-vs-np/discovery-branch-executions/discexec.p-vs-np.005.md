# Discovery Branch Execution: discexec.p-vs-np.005

- KB ref: p-vs-np
- Branch: disclayer.p-vs-np.pattern.hybridization-of-partial-bridges
- Generated (UTC): 2026-03-17T13:42:01.691601+00:00
- Status: completed-local-pass

## Branch

- Kind: epistemic-pattern
- Target: Hybrid Bridge Synthesis Prompt
- Routing priority: 6.728
- Required move: Some blocked routes sit at the intersection of multiple breakthrough families, which is evidence that one bridge object may be insufficient and a composed route should be explored.
- Abstraction required: Identify complementary partial bridges, specify their composition order, and state the intermediate theorem that would let them work together.
- Minimal theorem shape: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Spawn reason: Spawn `hybridization-of-partial-bridges` as a cross-cutting discovery layer because the blocked frontier spans multiple breakthrough families and needs a broader reframing.
- Rationale: Some blocked routes sit at the intersection of multiple breakthrough families, which is evidence that one bridge object may be insufficient and a composed route should be explored.

## Local Frontier

- Linked queue items: 10

### proofq.p-vs-np.001

- Bridge: bridge.001
- Priority: 0.779
- Claim type: route-conjecture
- Candidate object: MCSP witness family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.
- Conjecture: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.

### proofq.p-vs-np.002

- Bridge: bridge.002
- Priority: 0.758
- Claim type: route-conjecture
- Candidate object: MCSP witness family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route lemma: Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Conjecture: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

### proofq.p-vs-np.009

- Bridge: bridge.001
- Priority: 0.665
- Claim type: abstraction-conjecture
- Candidate object: MCSP obstruction family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.
- Conjecture: An adequate `canonical-obstruction-family` bridge concept for `bridge.001` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `nonuniform-circuit-exponential-lower-bound`, preserves `MCSP complexity profile in nonuniform-circuits`, and is strong enough to force `NP-not-in-P/poly`.

### proofq.p-vs-np.010

- Bridge: bridge.002
- Priority: 0.645
- Claim type: abstraction-conjecture
- Candidate object: MCSP obstruction family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route lemma: Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Conjecture: An adequate `canonical-obstruction-family` bridge concept for `bridge.002` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `nonuniform-circuit-exponential-lower-bound`, preserves `MCSP complexity profile in nonuniform-circuits`, and is strong enough to force `NP-not-in-P/poly`.

### proofq.p-vs-np.013

- Bridge: bridge.010
- Priority: 0.635
- Claim type: abstraction-conjecture
- Candidate object: MCSP obstruction family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route lemma: Prove that a MCSP witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Conjecture: An adequate `canonical-obstruction-family` bridge concept for `bridge.010` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `MCSP-near-threshold-nonuniform-circuit-lower-bound`, preserves `MCSP complexity profile in nonuniform-circuits`, and is strong enough to force `NP-not-in-P/poly`.

### proofq.p-vs-np.018

- Bridge: bridge.001
- Priority: 0.635
- Claim type: repair-lemma
- Candidate object: MCSP obstruction family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.
- Conjecture: Construct an explicit realization theorem for `MCSP obstruction family` showing how it absorbs `A barely-nontrivial lower bound for an explicit problem Q in a weak model`, preserves `MCSP complexity profile in nonuniform-circuits`, and materially forces `major consequences such as NP not in P/poly` on the route `bridge.001`.

## Local InformalMathLib Hints

- `mathlibref.p-vs-np.002` | Hardness Magnification Near State-of-the-Art Lower Bounds | external_reference
  Summary: The bridge.001 target is externally grounded, so the remaining novelty claim shifts to how the current framework realizes a usable MCSP carrier rather than to the target theorem itself.
  Artifact: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.002-hardness-magnification-near-state-of-the-art-lower-bounds.md
- `mathlibref.p-vs-np.006` | Polynomially Bounded Proof Systems Characterize NP Equals coNP | external_reference
  Summary: The Cook-Reckhow route is now clearly a bridge problem, not a target-theorem problem: the open step is the semantic bridge from the local definitional object to this existing characterization theorem.
  Artifact: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.006-polynomially-bounded-proof-systems-characterize-np-equals-conp.md
- `mathlibref.p-vs-np.004` | Hitting-Set Generators Yield Black-Box PIT | external_reference
  Summary: The PIT route is not blocked by the total absence of a hitting-set-to-PIT connection; it is blocked by the lack of an explicit generator or certificate object for the right class.
  Artifact: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.004-hitting-set-generators-yield-black-box-pit.md
- `mathlibref.p-vs-np.001` | Hardness Magnification for Natural Problems | external_reference
  Summary: The leading MCSP route is no longer novel at the level of magnification-as-such; the open step is the typed carrier or realization theorem that would instantiate the route inside the current proof state.
  Artifact: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.001-hardness-magnification-for-natural-problems.md

## Execution Summary

- Executed discovery branch `disclayer.p-vs-np.pattern.hybridization-of-partial-bridges` for `Hybrid Bridge Synthesis Prompt` over 10 linked blocked queue items. The run keeps the search on `Some blocked routes sit at the intersection of multiple breakthrough families, which is evidence that one bridge object may be insufficient and a composed route should be explored.` and uses obstruction classes `mcsp-magnification, carrier-realization, mcsp-magnification` as the local pressure map.

## Candidate Claims

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- For bridge.001 toward st.thm.oliveira-pich-santhanam-magnification-near-state, isolate the executable discovery claim `Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.` through the branch focus `hybridization-of-partial-bridges`.
- For bridge.002 toward st.thm.oliveira-santhanam-hardness-magnification-for-na, isolate the executable discovery claim `Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.` through the branch focus `hybridization-of-partial-bridges`.

## Required Questions

- Which blocked routes solve different parts of the same theorem pair?
- What intermediate object or theorem would allow the partial bridges to compose?
- What failure would show that the hybrid route is illegitimate rather than merely incomplete?

## Expected Deliverables

- Produce one reframing under `hybridization-of-partial-bridges` that changes the search state rather than restating the blocked lemma.
- Connect the reframing back to a theorem-shaped objective compatible with `There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.`.
- Record one stop condition showing when the pattern has become superficial rather than discovery-bearing.

## Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `accepting existence without algorithmic access`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `hybridization-of-partial-bridges` only re-labels the blocked frontier instead of reducing proof debt or changing the representation.

## External Framework Search Gate

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: composed transfer frameworks, hybrid argument methods, multi-interface reduction theories, proof complexity, pseudorandomness / derandomization
- Local prerequisites before browsing:
  - Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
  - State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
  - Reject at least one purely topical analogy before searching for an external framework.
