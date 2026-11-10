# Discovery Branch disclayer.p-vs-np.family.equivalence-coherence-reframing

- KB ref: p-vs-np
- Status: completed
- Kind: breakthrough-family
- Target: Equivalence / Coherence Reframing Prompt
- Routing priority: 0.880
- Dispatch rank: 17

## Why This Branch Exists

Spawn a dedicated `equivalence-coherence-reframing` discovery layer because obstruction `equivalence-coherence-gap` carries repeated pressure across the blocked frontier.

Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge.

## Discovery Contract

- Required move: Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge.
- Abstraction required: A typed account of active formulations as types and terms, an explicit equivalence witness or non-equivalence diagnosis, and the transport law needed to move invariants and theorem hypotheses across that equivalence.
- Minimal theorem shape: Either exhibit an equivalence E between the live formulations and prove that the target-relevant invariant transports coherently along E, or prove that no such equivalence witness exists in the current regime.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.003, proofq.p-vs-np.011, proofq.p-vs-np.023
- Linked breakthrough families: realization, transport, alignment, explicitness, semantic bridge

## System Prompt

Use HoTT as an equivalence and coherence discovery lens, not as a replacement foundation. Type the active concepts and bridge objects, ask whether two formulations are equal, equivalent, or only analogous, search for transportable invariants, and classify failure as no equivalence witness, incoherent transport, or weak equivalence where strict identity is needed.

## User Task

Reframe the blocked frontier as a problem about sameness, equivalence, transport, and coherence. State the candidate equivalence claims, the transport obligations they would induce, and the coherence failures that currently block the route.

## Required Questions

- Which active concepts should be treated as types, and which concrete witnesses should be treated as terms?
- Are the live operationalizations equal, equivalent, incomparable, or only analogous?
- What invariant or theorem hypothesis must transport along the proposed equivalence?
- Where does coherence fail when the same route is identified in two different ways?

## Expected Deliverables

- State one theorem-shaped candidate centered on `equivalence-coherence-reframing` satisfying `Either exhibit an equivalence E between the live formulations and prove that the target-relevant invariant transports coherently along E, or prove that no such equivalence witness exists in the current regime.`.
- Make `A typed account of active formulations as types and terms, an explicit equivalence witness or non-equivalence diagnosis, and the transport law needed to move invariants and theorem hypotheses across that equivalence.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `treating topical similarity as equivalence`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `equivalence-coherence-reframing` remains purely schematic after the first explicit object or theorem candidate.

## Search Modes

- equivalence witness search
- transport-law search
- coherence checking
- identity-vs-equivalence discrimination

## Anti-Patterns

- treating topical similarity as equivalence
- using representation changes without stating what transports and what fails to transport

## Lens Artifacts

- Routing heuristic: recommended=True | score=5/3
- Decision rule: Route to the HoTT pathway only if at least three equivalence/coherence criteria are active and the frontier is not merely a single local construction task.
- Rationale: Route to the HoTT lens when the discovery burden is really about equivalence, transport, and coherence between live formulations.
- Active criteria:
  - The frontier is asking whether two formulations are the same, equivalent, or only analogous.
  - The route depends on transporting invariants or claims across an equivalence or representation shift.
  - Several operationalizations or route interfaces are live at once, so sameness and interoperability matter.
  - The frontier risks confusing strict identity with weaker equivalence or analogy.
  - Discovery needs a principled account of what transports, what fails to transport, and where coherence breaks.
- Epistemic lens: hott
- Equivalence claims:
  - Equivalence claim: determine whether the live carrier for `carrier-realization` is identical to, equivalent to, or only analogous with the target-side object class.
  - Equivalence claim: determine whether the live carrier for `formula-size-transport` is identical to, equivalent to, or only analogous with the target-side object class.
  - Equivalence claim: determine whether the live carrier for `target-alignment` is identical to, equivalent to, or only analogous with the target-side object class.
- Transport obligations:
  - Transport obligation: move the invariant across the proposed equivalence for `carrier-realization` without changing the target claim.
  - Transport obligation: move the invariant across the proposed equivalence for `formula-size-transport` without changing the target claim.
  - Transport obligation: move the invariant across the proposed equivalence for `target-alignment` without changing the target claim.
- Coherence failures:
  - Coherence failure probe: check whether different identifications of the carrier for `carrier-realization` induce the same transported statement.
  - Coherence failure probe: check whether different identifications of the carrier for `formula-size-transport` induce the same transported statement.
  - Coherence failure probe: check whether different identifications of the carrier for `target-alignment` induce the same transported statement.
- Negative outputs:
  - no_equivalence_witness
  - transport_incoherent
  - weak_equivalence_only
  - identity_mismatch

## Sample Theorem Targets

- Exhibit an equivalence witness between the two live carrier formulations and prove that the target-relevant invariant transports coherently; otherwise prove that only weak equivalence is available.

## Knowledge Source Invocation Policy

- Stage: discovery
- Target: Equivalence / Coherence Reframing Prompt
- Target kind: breakthrough-family

### Source Order

- `InformalMathLib` | role=local theorem, definition, barrier, and prior-result retrieval | default=query-first
  Invoke when: The current breakthrough-family may already be locally grounded for `Equivalence / Coherence Reframing Prompt`. A named theorem, route lemma, barrier, or prior negative result might already exist locally. Novelty or prior-art status cannot be assessed without checking local memory first.
  Do not use for: inventing a new bridge object by analogy alone claiming closure when the local hit is only topically related
  Success condition: Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.
  Current signal: current_mathlib_hits=0
- `IDE generative search` | role=local candidate generation for bridge objects, invariants, decompositions, and representation shifts | default=use-after-local-grounding
  Invoke when: Local KB and InformalMathLib ground `Equivalence / Coherence Reframing Prompt`, but the missing move is still conceptual rather than factual. The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate. The output can remain conjectural until independently grounded or refuted.
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

- Program ID: disclayer.p-vs-np.family.equivalence-coherence-reframing
- Kind: discovery-branch
- Stage: discovery
- Target: Either exhibit an equivalence E between the live formulations and prove that the target-relevant invariant transports coherently along E, or prove that no such equivalence witness exists in the current regime.
- Nexus: Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge.
- Bridge object: A typed account of active formulations as types and terms, an explicit equivalence witness or non-equivalence diagnosis, and the transport law needed to move invariants and theorem hypotheses across that equivalence. (breakthrough-family)
- Positive route: Either exhibit an equivalence E between the live formulations and prove that the target-relevant invariant transports coherently along E, or prove that no such equivalence witness exists in the current regime.
- Negative route: Avoid anti-patterns and branch-local dead ends while sharpening the theorem shape.

Anchors:
- queue-frontier: proofq.p-vs-np.001 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- queue-frontier: proofq.p-vs-np.002 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- queue-frontier: proofq.p-vs-np.005 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- queue-frontier: proofq.p-vs-np.009 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- queue-frontier: proofq.p-vs-np.010 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- queue-frontier: proofq.p-vs-np.013 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- queue-frontier: proofq.p-vs-np.018 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- queue-frontier: proofq.p-vs-np.020 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- queue-frontier: proofq.p-vs-np.021 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- queue-frontier: proofq.p-vs-np.003 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- queue-frontier: proofq.p-vs-np.011 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- queue-frontier: proofq.p-vs-np.023 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.equivalence-coherence-reframing`.
- discovery-target: equivalence-coherence-reframing | Equivalence / Coherence Reframing Prompt

Tensions:
- equivalence-coherence-gap
- Required move: Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge.
- Abstraction required: A typed account of active formulations as types and terms, an explicit equivalence witness or non-equivalence diagnosis, and the transport law needed to move invariants and theorem hypotheses across that equivalence.
- Minimal theorem shape: Either exhibit an equivalence E between the live formulations and prove that the target-relevant invariant transports coherently along E, or prove that no such equivalence witness exists in the current regime.

Proof debt:
- Which active concepts should be treated as types, and which concrete witnesses should be treated as terms?
- Are the live operationalizations equal, equivalent, incomparable, or only analogous?
- What invariant or theorem hypothesis must transport along the proposed equivalence?
- Where does coherence fail when the same route is identified in two different ways?
- State one theorem-shaped candidate centered on `equivalence-coherence-reframing` satisfying `Either exhibit an equivalence E between the live formulations and prove that the target-relevant invariant transports coherently along E, or prove that no such equivalence witness exists in the current regime.`.
- Make `A typed account of active formulations as types and terms, an explicit equivalence witness or non-equivalence diagnosis, and the transport law needed to move invariants and theorem hypotheses across that equivalence.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

Decision gates:
- Branch stop criteria: Stop immediately if the branch collapses into the anti-pattern `treating topical similarity as equivalence`.; Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.; Stop after one explicit positive candidate and one explicit failure probe have both been recorded.; Escalate if `equivalence-coherence-reframing` remains purely schematic after the first explicit object or theorem candidate. -> Stop or re-route when the branch fails to produce a theorem-shaped gain.
- External framework search: targeted-foundation-search -> Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.

## External Framework Search Heuristic

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: sparse-object and distinguisher frameworks, duality or correspondence theorems, representation-theoretic normal forms, derandomization and generator frameworks, algebraic certificate constructions

## Local Prerequisites Before Browsing

- Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
- State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
- Reject at least one purely topical analogy before searching for an external framework.

## Query Templates

- mathematical framework for Equivalence / Coherence Reframing Prompt with preserved invariant and bridge theorem
- Equivalence / Coherence Reframing Prompt correspondence theorem transport invariant
- Equivalence / Coherence Reframing Prompt framework Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge. theorem
- theorem or framework matching: Either exhibit an equivalence E between the live formulations and prove that the target-relevant invariant transports coherently along E, or prove that no such equivalence witness exists in the current regime.
