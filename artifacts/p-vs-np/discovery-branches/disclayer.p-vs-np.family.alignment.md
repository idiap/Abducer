# Discovery Branch disclayer.p-vs-np.family.alignment

- KB ref: p-vs-np
- Status: completed
- Kind: breakthrough-family
- Target: Alignment Theorem Prompt
- Routing priority: 2.222
- Dispatch rank: 12

## Why This Branch Exists

Spawn a dedicated `alignment` discovery layer because obstruction `target-alignment` carries repeated pressure across the blocked frontier.

Identify or prove an equivalence between the current carrier class and the object class required by the target theorem.

## Discovery Contract

- Required move: Identify or prove an equivalence between the current carrier class and the object class required by the target theorem.
- Abstraction required: An alignment theorem, correspondence theorem, or mediating normal form linking the local carrier to the target's sparse-problem or distinguisher objects.
- Minimal theorem shape: Every admissible carrier C from the local route induces an object D in the target theorem's class, and D preserves the quantitative property needed to activate the target theorem.
- Linked queue IDs: proofq.p-vs-np.003, proofq.p-vs-np.011, proofq.p-vs-np.023
- Linked breakthrough families: alignment

## System Prompt

You are aligning a local carrier class with the object class demanded by an existing target theorem. Topical similarity is not enough. Search for equivalence, correspondence, or a mediating normal form.

## User Task

Describe the object-class map from the current carrier to the target theorem's object class, including the quantitative property that must survive the correspondence.

## Required Questions

- What is the target theorem's exact object class?
- How does the local carrier induce an object in that class?
- Which parameter or sparsity threshold is hardest to preserve?

## Expected Deliverables

- State one theorem-shaped candidate centered on `alignment` satisfying `Every admissible carrier C from the local route induces an object D in the target theorem's class, and D preserves the quantitative property needed to activate the target theorem.`.
- Make `An alignment theorem, correspondence theorem, or mediating normal form linking the local carrier to the target's sparse-problem or distinguisher objects.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `treating topical similarity as object equivalence`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `alignment` remains purely schematic after the first explicit object or theorem candidate.

## Search Modes

- object-class correspondence search
- normal-form mediation
- dual characterization of the target object

## Anti-Patterns

- treating topical similarity as object equivalence
- adding a stronger carrier without specifying the target object class map

## Lens Artifacts

- Epistemic lens: 

## Sample Theorem Targets

- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant exponential-lower-bound witness complexity and yields There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for....
- An adequate `canonical-obstruction-family` bridge concept for `bridge.016` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `nonuniform-circuit-exponential-lower-bound`, preserves `exponential-lower-bound witness complexity`, and is strong enough to force `exponential-lower-bound`.

## Knowledge Source Invocation Policy

- Stage: discovery
- Target: Alignment Theorem Prompt
- Target kind: breakthrough-family

### Source Order

- `InformalMathLib` | role=local theorem, definition, barrier, and prior-result retrieval | default=query-first
  Invoke when: The current breakthrough-family may already be locally grounded for `Alignment Theorem Prompt`. A named theorem, route lemma, barrier, or prior negative result might already exist locally. Novelty or prior-art status cannot be assessed without checking local memory first.
  Do not use for: inventing a new bridge object by analogy alone claiming closure when the local hit is only topically related
  Success condition: Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.
  Current signal: current_mathlib_hits=0
- `IDE generative search` | role=local candidate generation for bridge objects, invariants, decompositions, and representation shifts | default=use-after-local-grounding
  Invoke when: Local KB and InformalMathLib ground `Alignment Theorem Prompt`, but the missing move is still conceptual rather than factual. The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate. The output can remain conjectural until independently grounded or refuted.
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

- Program ID: disclayer.p-vs-np.family.alignment
- Kind: discovery-branch
- Stage: discovery
- Target: Every admissible carrier C from the local route induces an object D in the target theorem's class, and D preserves the quantitative property needed to activate the target theorem.
- Nexus: Identify or prove an equivalence between the current carrier class and the object class required by the target theorem.
- Bridge object: An alignment theorem, correspondence theorem, or mediating normal form linking the local carrier to the target's sparse-problem or distinguisher objects. (breakthrough-family)
- Positive route: Every admissible carrier C from the local route induces an object D in the target theorem's class, and D preserves the quantitative property needed to activate the target theorem.
- Negative route: Avoid anti-patterns and branch-local dead ends while sharpening the theorem shape.

Anchors:
- queue-frontier: proofq.p-vs-np.003 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.alignment`.
- queue-frontier: proofq.p-vs-np.011 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.alignment`.
- queue-frontier: proofq.p-vs-np.023 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.alignment`.
- discovery-target: alignment | Alignment Theorem Prompt

Tensions:
- target-alignment
- general-magnification
- Required move: Identify or prove an equivalence between the current carrier class and the object class required by the target theorem.
- Abstraction required: An alignment theorem, correspondence theorem, or mediating normal form linking the local carrier to the target's sparse-problem or distinguisher objects.
- Minimal theorem shape: Every admissible carrier C from the local route induces an object D in the target theorem's class, and D preserves the quantitative property needed to activate the target theorem.

Proof debt:
- What is the target theorem's exact object class?
- How does the local carrier induce an object in that class?
- Which parameter or sparsity threshold is hardest to preserve?
- State one theorem-shaped candidate centered on `alignment` satisfying `Every admissible carrier C from the local route induces an object D in the target theorem's class, and D preserves the quantitative property needed to activate the target theorem.`.
- Make `An alignment theorem, correspondence theorem, or mediating normal form linking the local carrier to the target's sparse-problem or distinguisher objects.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

Decision gates:
- Branch stop criteria: Stop immediately if the branch collapses into the anti-pattern `treating topical similarity as object equivalence`.; Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.; Stop after one explicit positive candidate and one explicit failure probe have both been recorded.; Escalate if `alignment` remains purely schematic after the first explicit object or theorem candidate. -> Stop or re-route when the branch fails to produce a theorem-shaped gain.
- External framework search: targeted-foundation-search -> Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.

## External Framework Search Heuristic

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: sparse-object and distinguisher frameworks, duality or correspondence theorems, representation-theoretic normal forms

## Local Prerequisites Before Browsing

- Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
- State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
- Reject at least one purely topical analogy before searching for an external framework.

## Query Templates

- mathematical framework for Alignment Theorem Prompt with preserved invariant and bridge theorem
- Alignment Theorem Prompt correspondence theorem transport invariant
- Alignment Theorem Prompt framework Identify or prove an equivalence between the current carrier class and the object class required by the target theorem. theorem
- theorem or framework matching: Every admissible carrier C from the local route induces an object D in the target theorem's class, and D preserves the quantitative property needed to activate the target theorem.
