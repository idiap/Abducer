# Discovery Branch Execution: discexec.p-vs-np.008

- KB ref: p-vs-np
- Branch: disclayer.p-vs-np.family.transport
- Generated (UTC): 2026-03-17T13:42:01.702110+00:00
- Status: completed-local-pass

## Branch

- Kind: breakthrough-family
- Target: Transport Principle Prompt
- Routing priority: 5.610
- Required move: Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.
- Abstraction required: A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift.
- Minimal theorem shape: For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.
- Spawn reason: Spawn a dedicated `transport` discovery layer because obstruction `formula-size-transport` carries repeated pressure across the blocked frontier.
- Rationale: Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.

## Local Frontier

- Linked queue items: 8

### proofq.p-vs-np.001

- Bridge: bridge.001
- Priority: 0.779
- Claim type: route-conjecture
- Candidate object: MCSP witness family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.
- Conjecture: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.

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

### proofq.p-vs-np.020

- Bridge: bridge.002
- Priority: 0.615
- Claim type: repair-lemma
- Candidate object: MCSP obstruction family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route lemma: Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Conjecture: Prove a theorem transporting `MCSP obstruction family` from the nonuniform-circuits regime into the formula-size regime while preserving `MCSP complexity profile in nonuniform-circuits` strongly enough to lift `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.

## Local InformalMathLib Hints

- `mathlibref.p-vs-np.002` | Hardness Magnification Near State-of-the-Art Lower Bounds | external_reference
  Summary: The bridge.001 target is externally grounded, so the remaining novelty claim shifts to how the current framework realizes a usable MCSP carrier rather than to the target theorem itself.
  Artifact: C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\external-references\mathlibref.p-vs-np.002-hardness-magnification-near-state-of-the-art-lower-bounds.md

## Execution Summary

- Executed discovery branch `disclayer.p-vs-np.family.transport` for `Transport Principle Prompt` over 8 linked blocked queue items. The run keeps the search on `Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.` and uses obstruction classes `formula-size-transport` as the local pressure map.

## Candidate Claims

- For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.
- For bridge.001 toward st.thm.oliveira-pich-santhanam-magnification-near-state, isolate the executable discovery claim `Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.` through the branch focus `transport`.

## Required Questions

- What exact quantity must be preserved across the model shift?
- What transformed carrier should live in the target model?
- What is the first obstruction showing why naive transport fails?

## Expected Deliverables

- State one theorem-shaped candidate centered on `transport` satisfying `For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.`.
- Make `A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

## Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for... holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `assuming the target theorem already provides the transport`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `transport` remains purely schematic after the first explicit object or theorem candidate.

## External Framework Search Gate

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: formula lower-bound transfer frameworks, communication complexity model-transfer methods, representation/normal-form theorems in circuit complexity
- Local prerequisites before browsing:
  - Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
  - State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
  - Reject at least one purely topical analogy before searching for an external framework.
