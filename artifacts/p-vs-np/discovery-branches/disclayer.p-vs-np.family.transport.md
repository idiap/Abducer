# Discovery Branch disclayer.p-vs-np.family.transport

- KB ref: p-vs-np
- Status: completed
- Kind: breakthrough-family
- Target: Transport Principle Prompt
- Routing priority: 5.610
- Dispatch rank: 8

## Why This Branch Exists

Spawn a dedicated `transport` discovery layer because obstruction `formula-size-transport` carries repeated pressure across the blocked frontier.

Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.

## Discovery Contract

- Required move: Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.
- Abstraction required: A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift.
- Minimal theorem shape: For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021
- Linked breakthrough families: transport

## System Prompt

You are searching for an invariant-preserving transport theorem across a model shift. Do not strengthen the source theorem unless it changes the transport mechanism. Focus on the cross-model map and the preserved quantitative parameter.

## User Task

State the strongest plausible transport law, compilation theorem, or normal form that could move the current carrier into the target model without losing the invariant needed for the payoff.

## Required Questions

- What exact quantity must be preserved across the model shift?
- What transformed carrier should live in the target model?
- What is the first obstruction showing why naive transport fails?

## Expected Deliverables

- State one theorem-shaped candidate centered on `transport` satisfying `For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.`.
- Make `A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `assuming the target theorem already provides the transport`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `transport` remains purely schematic after the first explicit object or theorem candidate.

## Search Modes

- cross-model transport principle
- invariant-preserving compilation theorem
- representation normal form for formula-size transfer

## Anti-Patterns

- assuming the target theorem already provides the transport
- strengthening the source lower bound without addressing the model shift

## Lens Artifacts

- Epistemic lens: 

## Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for... holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.

## Knowledge Source Invocation Policy

- Stage: discovery
- Target: Transport Principle Prompt
- Target kind: breakthrough-family

### Source Order

- `InformalMathLib` | role=local theorem, definition, barrier, and prior-result retrieval | default=query-first
  Invoke when: The current breakthrough-family may already be locally grounded for `Transport Principle Prompt`. A named theorem, route lemma, barrier, or prior negative result might already exist locally. Novelty or prior-art status cannot be assessed without checking local memory first.
  Do not use for: inventing a new bridge object by analogy alone claiming closure when the local hit is only topically related
  Success condition: Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.
  Current signal: current_mathlib_hits=0
- `IDE generative search` | role=local candidate generation for bridge objects, invariants, decompositions, and representation shifts | default=use-after-local-grounding
  Invoke when: Local KB and InformalMathLib ground `Transport Principle Prompt`, but the missing move is still conceptual rather than factual. The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate. The output can remain conjectural until independently grounded or refuted.
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

- Program ID: disclayer.p-vs-np.family.transport
- Kind: discovery-branch
- Stage: discovery
- Target: For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.
- Nexus: Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.
- Bridge object: A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift. (breakthrough-family)
- Positive route: For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.
- Negative route: Avoid anti-patterns and branch-local dead ends while sharpening the theorem shape.

Anchors:
- queue-frontier: proofq.p-vs-np.001 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.transport`.
- queue-frontier: proofq.p-vs-np.005 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.transport`.
- queue-frontier: proofq.p-vs-np.009 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.transport`.
- queue-frontier: proofq.p-vs-np.010 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.transport`.
- queue-frontier: proofq.p-vs-np.013 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.transport`.
- queue-frontier: proofq.p-vs-np.018 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.transport`.
- queue-frontier: proofq.p-vs-np.020 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.transport`.
- queue-frontier: proofq.p-vs-np.021 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.transport`.
- discovery-target: transport | Transport Principle Prompt

Tensions:
- formula-size-transport
- Required move: Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.
- Abstraction required: A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift.
- Minimal theorem shape: For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.

Proof debt:
- What exact quantity must be preserved across the model shift?
- What transformed carrier should live in the target model?
- What is the first obstruction showing why naive transport fails?
- State one theorem-shaped candidate centered on `transport` satisfying `For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.`.
- Make `A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

Decision gates:
- Branch stop criteria: Stop immediately if the branch collapses into the anti-pattern `assuming the target theorem already provides the transport`.; Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.; Stop after one explicit positive candidate and one explicit failure probe have both been recorded.; Escalate if `transport` remains purely schematic after the first explicit object or theorem candidate. -> Stop or re-route when the branch fails to produce a theorem-shaped gain.
- External framework search: targeted-foundation-search -> Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.

## External Framework Search Heuristic

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: formula lower-bound transfer frameworks, communication complexity model-transfer methods, representation/normal-form theorems in circuit complexity

## Local Prerequisites Before Browsing

- Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
- State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
- Reject at least one purely topical analogy before searching for an external framework.

## Query Templates

- mathematical framework for Transport Principle Prompt with preserved invariant and bridge theorem
- Transport Principle Prompt correspondence theorem transport invariant
- Transport Principle Prompt framework Find a theorem that preserves the relevant invariant across a cross-model move into formula-size. theorem
- theorem or framework matching: For every admissible carrier C in the nonuniform-circuit regime, there is a transformed carrier C' in the formula-size regime preserving invariant I and retaining enough quantitative strength to imply target T.
