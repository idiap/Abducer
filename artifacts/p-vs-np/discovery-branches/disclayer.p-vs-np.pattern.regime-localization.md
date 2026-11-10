# Discovery Branch disclayer.p-vs-np.pattern.regime-localization

- KB ref: p-vs-np
- Status: completed
- Kind: epistemic-pattern
- Target: Regime Localization Prompt
- Routing priority: 6.758
- Dispatch rank: 3

## Why This Branch Exists

Spawn `regime-localization` as a cross-cutting discovery layer because the blocked frontier spans multiple breakthrough families and needs a broader reframing.

The frontier repeatedly crosses model or threshold boundaries, so discovery should search for the smallest regime in which the route first becomes true.

## Discovery Contract

- Required move: The frontier repeatedly crosses model or threshold boundaries, so discovery should search for the smallest regime in which the route first becomes true.
- Abstraction required: Localize the frontier by proposing restricted regimes, threshold windows, or case splits where the target theorem may first activate, and explain what each localized success would imply for the broader programme.
- Minimal theorem shape: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.006
- Linked breakthrough families: abstraction-search, realization, transport, bridge-specificity, barrier-aware transfer, alignment, constructive instantiation

## System Prompt

You are searching for the smallest model, threshold, asymptotic regime, or promise-gap setting in which the route might first become true. Do not ask for the full theorem immediately if a more local regime would already be a major contribution.

## User Task

Localize the frontier by proposing restricted regimes, threshold windows, or case splits where the target theorem may first activate, and explain what each localized success would imply for the broader programme.

## Required Questions

- Which regime change most plausibly removes the current obstruction without trivializing the result?
- What is the first nontrivial threshold at which the route may become true?
- Would a localized theorem already count as an independently valuable subresult?

## Expected Deliverables

- Produce one reframing under `regime-localization` that changes the search state rather than restating the blocked lemma.
- Connect the reframing back to a theorem-shaped objective compatible with `There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.`.
- Record one stop condition showing when the pattern has become superficial rather than discovery-bearing.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `adding more obligations without exhibiting a concrete carrier family`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `regime-localization` only re-labels the blocked frontier instead of reducing proof debt or changing the representation.

## Search Modes

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

## Anti-Patterns

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

## Lens Artifacts

- Epistemic lens: 

## Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

## Knowledge Source Invocation Policy

- Stage: discovery
- Target: Regime Localization Prompt
- Target kind: epistemic-pattern

### Source Order

- `InformalMathLib` | role=local theorem, definition, barrier, and prior-result retrieval | default=query-first
  Invoke when: The current epistemic-pattern may already be locally grounded for `Regime Localization Prompt`. A named theorem, route lemma, barrier, or prior negative result might already exist locally. Novelty or prior-art status cannot be assessed without checking local memory first.
  Do not use for: inventing a new bridge object by analogy alone claiming closure when the local hit is only topically related
  Success condition: Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.
  Current signal: current_mathlib_hits=0
- `IDE generative search` | role=local candidate generation for bridge objects, invariants, decompositions, and representation shifts | default=use-after-local-grounding
  Invoke when: Local KB and InformalMathLib ground `Regime Localization Prompt`, but the missing move is still conceptual rather than factual. The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate. The output can remain conjectural until independently grounded or refuted.
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

- Program ID: disclayer.p-vs-np.pattern.regime-localization
- Kind: discovery-branch
- Stage: discovery
- Target: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Nexus: The frontier repeatedly crosses model or threshold boundaries, so discovery should search for the smallest regime in which the route first becomes true.
- Bridge object: Localize the frontier by proposing restricted regimes, threshold windows, or case splits where the target theorem may first activate, and explain what each localized success would imply for the broader programme. (epistemic-pattern)
- Positive route: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Negative route: Avoid anti-patterns and branch-local dead ends while sharpening the theorem shape.

Anchors:
- queue-frontier: proofq.p-vs-np.001 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.regime-localization`.
- queue-frontier: proofq.p-vs-np.002 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.regime-localization`.
- queue-frontier: proofq.p-vs-np.005 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.regime-localization`.
- queue-frontier: proofq.p-vs-np.009 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.regime-localization`.
- queue-frontier: proofq.p-vs-np.010 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.regime-localization`.
- queue-frontier: proofq.p-vs-np.013 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.regime-localization`.
- queue-frontier: proofq.p-vs-np.018 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.regime-localization`.
- queue-frontier: proofq.p-vs-np.020 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.regime-localization`.
- queue-frontier: proofq.p-vs-np.021 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.regime-localization`.
- queue-frontier: proofq.p-vs-np.006 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.regime-localization`.
- discovery-target: regime-localization | Regime Localization Prompt

Tensions:
- mcsp-magnification
- carrier-realization
- formula-size-transport
- target-grounding
- local-reduction-barrier
- general-magnification
- schema-to-examples
- Required move: The frontier repeatedly crosses model or threshold boundaries, so discovery should search for the smallest regime in which the route first becomes true.
- Abstraction required: Localize the frontier by proposing restricted regimes, threshold windows, or case splits where the target theorem may first activate, and explain what each localized success would imply for the broader programme.
- Minimal theorem shape: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.

Proof debt:
- Which regime change most plausibly removes the current obstruction without trivializing the result?
- What is the first nontrivial threshold at which the route may become true?
- Would a localized theorem already count as an independently valuable subresult?
- Produce one reframing under `regime-localization` that changes the search state rather than restating the blocked lemma.
- Connect the reframing back to a theorem-shaped objective compatible with `There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.`.
- Record one stop condition showing when the pattern has become superficial rather than discovery-bearing.

Decision gates:
- Branch stop criteria: Stop immediately if the branch collapses into the anti-pattern `adding more obligations without exhibiting a concrete carrier family`.; Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.; Stop after one explicit positive candidate and one explicit failure probe have both been recorded.; Escalate if `regime-localization` only re-labels the blocked frontier instead of reducing proof debt or changing the representation. -> Stop or re-route when the branch fails to produce a theorem-shaped gain.
- External framework search: targeted-foundation-search -> Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.

## External Framework Search Heuristic

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: threshold and regime-restriction frameworks, restricted-model lower-bound programmes, proof complexity, pseudorandomness / derandomization, coding-theoretic hardness surrogates

## Local Prerequisites Before Browsing

- Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
- State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
- Reject at least one purely topical analogy before searching for an external framework.

## Query Templates

- mathematical framework for Regime Localization Prompt with preserved invariant and bridge theorem
- Regime Localization Prompt correspondence theorem transport invariant
- Regime Localization Prompt framework The frontier repeatedly crosses model or threshold boundaries, so discovery should search for the smallest regime in which the route first becomes true. theorem
- theorem or framework matching: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
