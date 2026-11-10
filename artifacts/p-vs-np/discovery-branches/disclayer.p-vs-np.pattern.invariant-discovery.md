# Discovery Branch disclayer.p-vs-np.pattern.invariant-discovery

- KB ref: p-vs-np
- Status: completed
- Kind: epistemic-pattern
- Target: Invariant Discovery Prompt
- Routing priority: 6.868
- Dispatch rank: 1

## Why This Branch Exists

Spawn `invariant-discovery` as a cross-cutting discovery layer because the blocked frontier spans multiple breakthrough families and needs a broader reframing.

Several live routes are still searching for the right preserved quantity or witness measure, so invariant discovery remains a first-class discovery move.

## Discovery Contract

- Required move: Several live routes are still searching for the right preserved quantity or witness measure, so invariant discovery remains a first-class discovery move.
- Abstraction required: Identify 2-4 candidate invariants, state how each is computed or witnessed, and say which one would most sharply reorganize the current blocked route.
- Minimal theorem shape: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.006
- Linked breakthrough families: abstraction-search, realization, transport, bridge-specificity, barrier-aware transfer, alignment, explicitness, constructive instantiation, semantic bridge

## System Prompt

You are searching for the invariant that the current route is really trying to preserve, expose, or measure. Do not begin from the named bridge object. Begin from the quantity, structure, or monotone property that would survive the route and explain the payoff.

## User Task

Identify 2-4 candidate invariants, state how each is computed or witnessed, and say which one would most sharply reorganize the current blocked route.

## Required Questions

- What quantity or structure must survive every legitimate route variant?
- Which candidate invariant is strong enough to force the payoff but weak enough to be realizable?
- How would failure of the invariant candidate sharpen the obstruction class?

## Expected Deliverables

- Produce one reframing under `invariant-discovery` that changes the search state rather than restating the blocked lemma.
- Connect the reframing back to a theorem-shaped objective compatible with `There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.`.
- Record one stop condition showing when the pattern has become superficial rather than discovery-bearing.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `accepting existence without algorithmic access`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `invariant-discovery` only re-labels the blocked frontier instead of reducing proof debt or changing the representation.

## Search Modes

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

## Anti-Patterns

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

## Lens Artifacts

- Epistemic lens: 

## Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

## Knowledge Source Invocation Policy

- Stage: discovery
- Target: Invariant Discovery Prompt
- Target kind: epistemic-pattern

### Source Order

- `InformalMathLib` | role=local theorem, definition, barrier, and prior-result retrieval | default=query-first
  Invoke when: The current epistemic-pattern may already be locally grounded for `Invariant Discovery Prompt`. A named theorem, route lemma, barrier, or prior negative result might already exist locally. Novelty or prior-art status cannot be assessed without checking local memory first.
  Do not use for: inventing a new bridge object by analogy alone claiming closure when the local hit is only topically related
  Success condition: Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.
  Current signal: current_mathlib_hits=0
- `IDE generative search` | role=local candidate generation for bridge objects, invariants, decompositions, and representation shifts | default=use-after-local-grounding
  Invoke when: Local KB and InformalMathLib ground `Invariant Discovery Prompt`, but the missing move is still conceptual rather than factual. The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate. The output can remain conjectural until independently grounded or refuted.
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

- Program ID: disclayer.p-vs-np.pattern.invariant-discovery
- Kind: discovery-branch
- Stage: discovery
- Target: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Nexus: Several live routes are still searching for the right preserved quantity or witness measure, so invariant discovery remains a first-class discovery move.
- Bridge object: Identify 2-4 candidate invariants, state how each is computed or witnessed, and say which one would most sharply reorganize the current blocked route. (epistemic-pattern)
- Positive route: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Negative route: Avoid anti-patterns and branch-local dead ends while sharpening the theorem shape.

Anchors:
- queue-frontier: proofq.p-vs-np.001 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.invariant-discovery`.
- queue-frontier: proofq.p-vs-np.002 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.invariant-discovery`.
- queue-frontier: proofq.p-vs-np.005 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.invariant-discovery`.
- queue-frontier: proofq.p-vs-np.009 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.invariant-discovery`.
- queue-frontier: proofq.p-vs-np.010 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.invariant-discovery`.
- queue-frontier: proofq.p-vs-np.013 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.invariant-discovery`.
- queue-frontier: proofq.p-vs-np.018 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.invariant-discovery`.
- queue-frontier: proofq.p-vs-np.020 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.invariant-discovery`.
- queue-frontier: proofq.p-vs-np.021 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.invariant-discovery`.
- queue-frontier: proofq.p-vs-np.006 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.pattern.invariant-discovery`.
- discovery-target: invariant-discovery | Invariant Discovery Prompt

Tensions:
- mcsp-magnification
- carrier-realization
- formula-size-transport
- target-grounding
- local-reduction-barrier
- target-alignment
- general-magnification
- pit-upgrade
- schema-to-examples
- characterization-bridge
- explicitness-gap
- Required move: Several live routes are still searching for the right preserved quantity or witness measure, so invariant discovery remains a first-class discovery move.
- Abstraction required: Identify 2-4 candidate invariants, state how each is computed or witnessed, and say which one would most sharply reorganize the current blocked route.
- Minimal theorem shape: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.

Proof debt:
- What quantity or structure must survive every legitimate route variant?
- Which candidate invariant is strong enough to force the payoff but weak enough to be realizable?
- How would failure of the invariant candidate sharpen the obstruction class?
- Produce one reframing under `invariant-discovery` that changes the search state rather than restating the blocked lemma.
- Connect the reframing back to a theorem-shaped objective compatible with `There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.`.
- Record one stop condition showing when the pattern has become superficial rather than discovery-bearing.

Decision gates:
- Branch stop criteria: Stop immediately if the branch collapses into the anti-pattern `accepting existence without algorithmic access`.; Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.; Stop after one explicit positive candidate and one explicit failure probe have both been recorded.; Escalate if `invariant-discovery` only re-labels the blocked frontier instead of reducing proof debt or changing the representation. -> Stop or re-route when the branch fails to produce a theorem-shaped gain.
- External framework search: targeted-foundation-search -> Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.

## External Framework Search Heuristic

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: potential / energy method frameworks, monotone measure frameworks, certificate-complexity and witness-measure theories, proof complexity, pseudorandomness / derandomization

## Local Prerequisites Before Browsing

- Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
- State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
- Reject at least one purely topical analogy before searching for an external framework.

## Query Templates

- mathematical framework for Invariant Discovery Prompt with preserved invariant and bridge theorem
- Invariant Discovery Prompt correspondence theorem transport invariant
- Invariant Discovery Prompt framework Several live routes are still searching for the right preserved quantity or witness measure, so invariant discovery remains a first-class discovery move. theorem
- theorem or framework matching: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
