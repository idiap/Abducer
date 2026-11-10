# Discovery Branch disclayer.p-vs-np.pattern.counterexample-led-concept-formation

- KB ref: p-vs-np
- Status: completed
- Kind: epistemic-pattern
- Target: Counterexample-Led Concept Formation Prompt
- Routing priority: 6.658
- Dispatch rank: 7

## Why This Branch Exists

Spawn `counterexample-led-concept-formation` as a cross-cutting discovery layer because the blocked frontier spans multiple breakthrough families and needs a broader reframing.

The frontier is heavily blocked, so near-counterexamples and barrier analogs should be used to induce better concepts rather than only to reject claims.

## Discovery Contract

- Required move: The frontier is heavily blocked, so near-counterexamples and barrier analogs should be used to induce better concepts rather than only to reject claims.
- Abstraction required: Identify the strongest nearby failure patterns, describe what they invalidate, and derive a refined concept or admissibility condition from those failures.
- Minimal theorem shape: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.004
- Linked breakthrough families: abstraction-search, realization, transport, barrier-aware transfer, alignment, semantic bridge

## System Prompt

Use failure as a discovery tool. Search for near-counterexamples, barrier analogs, and route-breaking examples, then ask what concept would separate the surviving cases from the failures.

## User Task

Identify the strongest nearby failure patterns, describe what they invalidate, and derive a refined concept or admissibility condition from those failures.

## Required Questions

- What is the nearest counterexample or barrier analog to the current route?
- Which current concept fails to distinguish the positive and negative cases?
- What new concept becomes visible only after inspecting the failure pattern?

## Expected Deliverables

- Produce one reframing under `counterexample-led-concept-formation` that changes the search state rather than restating the blocked lemma.
- Connect the reframing back to a theorem-shaped objective compatible with `There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.`.
- Record one stop condition showing when the pattern has become superficial rather than discovery-bearing.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `adding a stronger carrier without specifying the target object class map`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `counterexample-led-concept-formation` only re-labels the blocked frontier instead of reducing proof debt or changing the representation.

## Search Modes

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

## Anti-Patterns

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

## Lens Artifacts

- Epistemic lens: 

## Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

## Knowledge Source Invocation Policy

- Stage: discovery
- Target: Counterexample-Led Concept Formation Prompt
- Target kind: epistemic-pattern

### Source Order

- `InformalMathLib` | role=local theorem, definition, barrier, and prior-result retrieval | default=query-first
  Invoke when: The current epistemic-pattern may already be locally grounded for `Counterexample-Led Concept Formation Prompt`. A named theorem, route lemma, barrier, or prior negative result might already exist locally. Novelty or prior-art status cannot be assessed without checking local memory first.
  Do not use for: inventing a new bridge object by analogy alone claiming closure when the local hit is only topically related
  Success condition: Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.
  Current signal: current_mathlib_hits=0
- `IDE generative search` | role=local candidate generation for bridge objects, invariants, decompositions, and representation shifts | default=use-after-local-grounding
  Invoke when: Local KB and InformalMathLib ground `Counterexample-Led Concept Formation Prompt`, but the missing move is still conceptual rather than factual. The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate. The output can remain conjectural until independently grounded or refuted.
  Do not use for: claiming prior art fabricating exact theorem statements or bibliographic facts promoting analogy directly into InformalMathLib without proof relevance
  Success condition: A generative suggestion is admissible only if it sharpens the theorem shape, negative route, or abstraction type; it is not evidence by itself.
- `web search` | role=external exact theorem, prior-art, or framework retrieval | default=last-resort-decisive-only
  Invoke when: A decisive exact theorem statement, prior-art fact, threshold, or barrier is still missing after local KB and InformalMathLib lookup. A local-search failure has been recorded and materially blocks the proof or novelty decision. The query can be stated concretely as a named theorem, paper, author, framework, or model-specific fact.
  Do not use for: generic background reading decorative references replacing local conceptual search with unbounded browsing
  Success condition: If an external theorem, definition, axiom, or named framework becomes proof-relevant, record the exact query and import the result into InformalMathLib.

### Consistency Rules

- Query local KB and InformalMathLib before any web search.
- Use IDE/generative search only after theorem grounding is explicit enough to state what kind of missing move is under search.
- Do not treat generative candidates as evidence; they remain conjectural until grounded, refuted, or externally validated.
- Do not claim novelty until both local memory and any required decisive prior-art gate have been checked.
- If browsing changes the proof state, record what exact statement changed and import proof-relevant external results into InformalMathLib.

### Escalation Rules

- Stay in InformalMathLib/local mode when the issue is retrieval of a known local dependency.
- Escalate to IDE/generative search when the issue is missing abstraction or representation, not missing factual attribution.
- Escalate to web search only when the issue is exact external prior art, exact theorem text, or a missing external framework foundation that local artifacts cannot settle.

## PDL Program

- Program ID: disclayer.p-vs-np.pattern.counterexample-led-concept-formation
- Kind: discovery-branch
- Stage: discovery
- Target: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Nexus: The frontier is heavily blocked, so near-counterexamples and barrier analogs should be used to induce better concepts rather than only to reject claims.
- Bridge object: Identify the strongest nearby failure patterns, describe what they invalidate, and derive a refined concept or admissibility condition from those failures. (epistemic-pattern)
- Positive route: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Negative route: Avoid anti-patterns and branch-local dead ends while sharpening the theorem shape.

Anchors:
- queue-frontier: proofq.p-vs-np.001 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.counterexample-led-concept-formation`.
- queue-frontier: proofq.p-vs-np.002 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.counterexample-led-concept-formation`.
- queue-frontier: proofq.p-vs-np.005 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.counterexample-led-concept-formation`.
- queue-frontier: proofq.p-vs-np.009 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.counterexample-led-concept-formation`.
- queue-frontier: proofq.p-vs-np.010 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.counterexample-led-concept-formation`.
- queue-frontier: proofq.p-vs-np.013 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.counterexample-led-concept-formation`.
- queue-frontier: proofq.p-vs-np.018 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.counterexample-led-concept-formation`.
- queue-frontier: proofq.p-vs-np.020 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.counterexample-led-concept-formation`.
- queue-frontier: proofq.p-vs-np.021 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.counterexample-led-concept-formation`.
- queue-frontier: proofq.p-vs-np.004 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.counterexample-led-concept-formation`.
- discovery-target: counterexample-led-concept-formation | Counterexample-Led Concept Formation Prompt

Tensions:
- mcsp-magnification
- carrier-realization
- formula-size-transport
- local-reduction-barrier
- target-alignment
- general-magnification
- characterization-bridge
- Required move: The frontier is heavily blocked, so near-counterexamples and barrier analogs should be used to induce better concepts rather than only to reject claims.
- Abstraction required: Identify the strongest nearby failure patterns, describe what they invalidate, and derive a refined concept or admissibility condition from those failures.
- Minimal theorem shape: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.

Proof debt:
- What is the nearest counterexample or barrier analog to the current route?
- Which current concept fails to distinguish the positive and negative cases?
- What new concept becomes visible only after inspecting the failure pattern?
- Produce one reframing under `counterexample-led-concept-formation` that changes the search state rather than restating the blocked lemma.
- Connect the reframing back to a theorem-shaped objective compatible with `There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.`.
- Record one stop condition showing when the pattern has become superficial rather than discovery-bearing.

Decision gates:
- Branch stop criteria: Stop immediately if the branch collapses into the anti-pattern `adding a stronger carrier without specifying the target object class map`.; Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.; Stop after one explicit positive candidate and one explicit failure probe have both been recorded.; Escalate if `counterexample-led-concept-formation` only re-labels the blocked frontier instead of reducing proof debt or changing the representation. -> Stop or re-route when the branch fails to produce a theorem-shaped gain.
- External framework search: targeted-foundation-search -> Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.

## External Framework Search Heuristic

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: barrier and impossibility frameworks, minimal obstruction and forbidden-configuration theories, proof complexity, pseudorandomness / derandomization, coding-theoretic hardness surrogates

## Local Prerequisites Before Browsing

- Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
- State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
- Reject at least one purely topical analogy before searching for an external framework.

## Query Templates

- mathematical framework for Counterexample-Led Concept Formation Prompt with preserved invariant and bridge theorem
- Counterexample-Led Concept Formation Prompt correspondence theorem transport invariant
- Counterexample-Led Concept Formation Prompt framework The frontier is heavily blocked, so near-counterexamples and barrier analogs should be used to induce better concepts rather than only to reject claims. theorem
- theorem or framework matching: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
