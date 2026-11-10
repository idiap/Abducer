# Discovery Branch disclayer.p-vs-np.family.abstraction-search

- KB ref: p-vs-np
- Status: completed
- Kind: breakthrough-family
- Target: Abstraction Search Prompt
- Routing priority: 6.443
- Dispatch rank: 2

## Why This Branch Exists

Spawn a dedicated `abstraction-search` discovery layer because obstruction `mcsp-magnification` carries repeated pressure across the blocked frontier.

Find a sharper abstraction that turns the blocked route into a typed, inspectable theorem target.

## Discovery Contract

- Required move: Find a sharper abstraction that turns the blocked route into a typed, inspectable theorem target.
- Abstraction required: A theorem-family-specific carrier, invariant, or bridge law that adds new mathematical content.
- Minimal theorem shape: State a route-specific theorem that would resolve the blocked interface and make the next proof obligation materially sharper.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021
- Linked breakthrough families: abstraction-search

## System Prompt

You are searching for the minimal conceptual breakthrough that would turn a blocked route into a typed theorem target. Do not restate the blocked lemma. Identify the sharper carrier, invariant, or bridge law that would make the next theorem materially more specific.

## User Task

Restate the obstruction as a missing abstraction problem, propose 2-4 typed bridge candidates, and state the first theorem-pair-specific lemma each candidate would make possible.

## Required Questions

- What typed object would add mathematical content beyond the current schematic carrier?
- What route-specific theorem would become stateable if that object existed?
- Which candidate clarifies the negative route if it fails?

## Expected Deliverables

- State one theorem-shaped candidate centered on `abstraction-search` satisfying `State a route-specific theorem that would resolve the blocked interface and make the next proof obligation materially sharper.`.
- Make `A theorem-family-specific carrier, invariant, or bridge law that adds new mathematical content.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `repeating the same blocked statement without new typed structure`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `abstraction-search` remains purely schematic after the first explicit object or theorem candidate.

## Search Modes

- typed abstraction search
- bridge split
- counterfactual sharpening

## Anti-Patterns

- repeating the same blocked statement without new typed structure

## Lens Artifacts

- Epistemic lens: 

## Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

## Knowledge Source Invocation Policy

- Stage: discovery
- Target: Abstraction Search Prompt
- Target kind: breakthrough-family

### Source Order

- `InformalMathLib` | role=local theorem, definition, barrier, and prior-result retrieval | default=query-first
  Invoke when: The current breakthrough-family may already be locally grounded for `Abstraction Search Prompt`. A named theorem, route lemma, barrier, or prior negative result might already exist locally. Novelty or prior-art status cannot be assessed without checking local memory first.
  Do not use for: inventing a new bridge object by analogy alone claiming closure when the local hit is only topically related
  Success condition: Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.
  Current signal: current_mathlib_hits=0
- `IDE generative search` | role=local candidate generation for bridge objects, invariants, decompositions, and representation shifts | default=use-after-local-grounding
  Invoke when: Local KB and InformalMathLib ground `Abstraction Search Prompt`, but the missing move is still conceptual rather than factual. The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate. The output can remain conjectural until independently grounded or refuted.
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

- Program ID: disclayer.p-vs-np.family.abstraction-search
- Kind: discovery-branch
- Stage: discovery
- Target: State a route-specific theorem that would resolve the blocked interface and make the next proof obligation materially sharper.
- Nexus: Find a sharper abstraction that turns the blocked route into a typed, inspectable theorem target.
- Bridge object: A theorem-family-specific carrier, invariant, or bridge law that adds new mathematical content. (breakthrough-family)
- Positive route: State a route-specific theorem that would resolve the blocked interface and make the next proof obligation materially sharper.
- Negative route: Avoid anti-patterns and branch-local dead ends while sharpening the theorem shape.

Anchors:
- queue-frontier: proofq.p-vs-np.001 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.abstraction-search`.
- queue-frontier: proofq.p-vs-np.002 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.abstraction-search`.
- queue-frontier: proofq.p-vs-np.005 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.abstraction-search`.
- queue-frontier: proofq.p-vs-np.009 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.abstraction-search`.
- queue-frontier: proofq.p-vs-np.010 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.abstraction-search`.
- queue-frontier: proofq.p-vs-np.013 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.abstraction-search`.
- queue-frontier: proofq.p-vs-np.018 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.abstraction-search`.
- queue-frontier: proofq.p-vs-np.020 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.abstraction-search`.
- queue-frontier: proofq.p-vs-np.021 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.abstraction-search`.
- discovery-target: abstraction-search | Abstraction Search Prompt

Tensions:
- mcsp-magnification
- Required move: Find a sharper abstraction that turns the blocked route into a typed, inspectable theorem target.
- Abstraction required: A theorem-family-specific carrier, invariant, or bridge law that adds new mathematical content.
- Minimal theorem shape: State a route-specific theorem that would resolve the blocked interface and make the next proof obligation materially sharper.

Proof debt:
- What typed object would add mathematical content beyond the current schematic carrier?
- What route-specific theorem would become stateable if that object existed?
- Which candidate clarifies the negative route if it fails?
- State one theorem-shaped candidate centered on `abstraction-search` satisfying `State a route-specific theorem that would resolve the blocked interface and make the next proof obligation materially sharper.`.
- Make `A theorem-family-specific carrier, invariant, or bridge law that adds new mathematical content.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

Decision gates:
- Branch stop criteria: Stop immediately if the branch collapses into the anti-pattern `repeating the same blocked statement without new typed structure`.; Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.; Stop after one explicit positive candidate and one explicit failure probe have both been recorded.; Escalate if `abstraction-search` remains purely schematic after the first explicit object or theorem candidate. -> Stop or re-route when the branch fails to produce a theorem-shaped gain.
- External framework search: targeted-foundation-search -> Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.

## External Framework Search Heuristic

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: proof complexity, pseudorandomness / derandomization, coding-theoretic hardness surrogates

## Local Prerequisites Before Browsing

- Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
- State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
- Reject at least one purely topical analogy before searching for an external framework.

## Query Templates

- mathematical framework for Abstraction Search Prompt with preserved invariant and bridge theorem
- Abstraction Search Prompt correspondence theorem transport invariant
- Abstraction Search Prompt framework Find a sharper abstraction that turns the blocked route into a typed, inspectable theorem target. theorem
- theorem or framework matching: State a route-specific theorem that would resolve the blocked interface and make the next proof obligation materially sharper.
