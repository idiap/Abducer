# Discovery Branch disclayer.p-vs-np.family.barrier-aware-transfer

- KB ref: p-vs-np
- Status: completed
- Kind: breakthrough-family
- Target: Barrier-Aware Transfer Prompt
- Routing priority: 2.309
- Dispatch rank: 10

## Why This Branch Exists

Spawn a dedicated `barrier-aware transfer` discovery layer because obstruction `local-reduction-barrier` carries repeated pressure across the blocked frontier.

Design a transfer mechanism that survives known local-reduction barriers, or prove that no such mechanism exists under explicit assumptions.

## Discovery Contract

- Required move: Design a transfer mechanism that survives known local-reduction barriers, or prove that no such mechanism exists under explicit assumptions.
- Abstraction required: A barrier-aware reduction gadget family or an impossibility theorem explaining why the reduction regime cannot be crossed.
- Minimal theorem shape: Either construct a local reduction family G satisfying locality bounds L and preserving witness structure W, or prove that any such G would contradict barrier theorem B.
- Linked queue IDs: proofq.p-vs-np.004, proofq.p-vs-np.012, proofq.p-vs-np.019
- Linked breakthrough families: barrier-aware transfer

## System Prompt

You are searching under an explicit barrier theorem. Either construct a transfer that survives the barrier's constraints or sharpen the impossibility theorem. Do not use generic hardness language that ignores the reduction regime.

## User Task

Describe a barrier-aware gadget family or impossibility result for the blocked transfer, with locality bounds and preserved witness structure made explicit.

## Required Questions

- What exact barrier theorem constrains the route?
- What locality or regime parameter must any positive construction respect?
- What negative theorem would be a contribution if positive transfer fails?

## Expected Deliverables

- State one theorem-shaped candidate centered on `barrier-aware transfer` satisfying `Either construct a local reduction family G satisfying locality bounds L and preserving witness structure W, or prove that any such G would contradict barrier theorem B.`.
- Make `A barrier-aware reduction gadget family or an impossibility theorem explaining why the reduction regime cannot be crossed.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `ignoring the known local-reduction barrier theorem`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `barrier-aware transfer` remains purely schematic after the first explicit object or theorem candidate.

## Search Modes

- barrier-aware gadget design
- impossibility theorem search
- reduction regime decomposition

## Anti-Patterns

- ignoring the known local-reduction barrier theorem
- using generic NP-hardness language without locality constraints

## Lens Artifacts

- Epistemic lens: 

## Sample Theorem Targets

- There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever NP-complete under polynomial-time many-one reductions holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification from the source regime to MCSP and yields is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various... for MCSP.
- An adequate `reduction-gadget-family` bridge concept for `bridge.007` is a `family of reductions preserving the route witness structure` named `unspecified reduction gadget family` that absorbs `NP-completeness`, preserves `consequence schema NP-complete-classification`, and is strong enough to force `MCSP-hardness-transfer`.

## Knowledge Source Invocation Policy

- Stage: discovery
- Target: Barrier-Aware Transfer Prompt
- Target kind: breakthrough-family

### Source Order

- `InformalMathLib` | role=local theorem, definition, barrier, and prior-result retrieval | default=query-first
  Invoke when: The current breakthrough-family may already be locally grounded for `Barrier-Aware Transfer Prompt`. A named theorem, route lemma, barrier, or prior negative result might already exist locally. Novelty or prior-art status cannot be assessed without checking local memory first.
  Do not use for: inventing a new bridge object by analogy alone claiming closure when the local hit is only topically related
  Success condition: Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.
  Current signal: current_mathlib_hits=0
- `IDE generative search` | role=local candidate generation for bridge objects, invariants, decompositions, and representation shifts | default=use-after-local-grounding
  Invoke when: Local KB and InformalMathLib ground `Barrier-Aware Transfer Prompt`, but the missing move is still conceptual rather than factual. The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate. The output can remain conjectural until independently grounded or refuted.
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

- Program ID: disclayer.p-vs-np.family.barrier-aware-transfer
- Kind: discovery-branch
- Stage: discovery
- Target: Either construct a local reduction family G satisfying locality bounds L and preserving witness structure W, or prove that any such G would contradict barrier theorem B.
- Nexus: Design a transfer mechanism that survives known local-reduction barriers, or prove that no such mechanism exists under explicit assumptions.
- Bridge object: A barrier-aware reduction gadget family or an impossibility theorem explaining why the reduction regime cannot be crossed. (breakthrough-family)
- Positive route: Either construct a local reduction family G satisfying locality bounds L and preserving witness structure W, or prove that any such G would contradict barrier theorem B.
- Negative route: Avoid anti-patterns and branch-local dead ends while sharpening the theorem shape.

Anchors:
- queue-frontier: proofq.p-vs-np.004 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.barrier-aware-transfer`.
- queue-frontier: proofq.p-vs-np.012 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.barrier-aware-transfer`.
- queue-frontier: proofq.p-vs-np.019 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.barrier-aware-transfer`.
- discovery-target: barrier-aware transfer | Barrier-Aware Transfer Prompt

Tensions:
- local-reduction-barrier
- Required move: Design a transfer mechanism that survives known local-reduction barriers, or prove that no such mechanism exists under explicit assumptions.
- Abstraction required: A barrier-aware reduction gadget family or an impossibility theorem explaining why the reduction regime cannot be crossed.
- Minimal theorem shape: Either construct a local reduction family G satisfying locality bounds L and preserving witness structure W, or prove that any such G would contradict barrier theorem B.

Proof debt:
- What exact barrier theorem constrains the route?
- What locality or regime parameter must any positive construction respect?
- What negative theorem would be a contribution if positive transfer fails?
- State one theorem-shaped candidate centered on `barrier-aware transfer` satisfying `Either construct a local reduction family G satisfying locality bounds L and preserving witness structure W, or prove that any such G would contradict barrier theorem B.`.
- Make `A barrier-aware reduction gadget family or an impossibility theorem explaining why the reduction regime cannot be crossed.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

Decision gates:
- Branch stop criteria: Stop immediately if the branch collapses into the anti-pattern `ignoring the known local-reduction barrier theorem`.; Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.; Stop after one explicit positive candidate and one explicit failure probe have both been recorded.; Escalate if `barrier-aware transfer` remains purely schematic after the first explicit object or theorem candidate. -> Stop or re-route when the branch fails to produce a theorem-shaped gain.
- External framework search: targeted-foundation-search -> Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.

## External Framework Search Heuristic

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: lower-bound barrier frameworks, local-reduction impossibility theory, gadget and locality-preservation frameworks

## Local Prerequisites Before Browsing

- Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
- State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
- Reject at least one purely topical analogy before searching for an external framework.

## Query Templates

- mathematical framework for Barrier-Aware Transfer Prompt with preserved invariant and bridge theorem
- Barrier-Aware Transfer Prompt correspondence theorem transport invariant
- Barrier-Aware Transfer Prompt framework Design a transfer mechanism that survives known local-reduction barriers, or prove that no such mechanism exists under explicit assumptions. theorem
- theorem or framework matching: Either construct a local reduction family G satisfying locality bounds L and preserving witness structure W, or prove that any such G would contradict barrier theorem B.
