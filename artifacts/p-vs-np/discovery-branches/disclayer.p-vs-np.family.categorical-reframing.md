# Discovery Branch disclayer.p-vs-np.family.categorical-reframing

- KB ref: p-vs-np
- Status: completed
- Kind: breakthrough-family
- Target: Categorical Reframing Prompt
- Routing priority: 0.910
- Dispatch rank: 16

## Why This Branch Exists

Spawn a dedicated `categorical-reframing` discovery layer because obstruction `structural-composition-gap` carries repeated pressure across the blocked frontier.

Recast the blocked frontier as a diagrammatic composition problem: identify objects, morphisms, mediating objects, and the exact commutativity or factorization obligation.

## Discovery Contract

- Required move: Recast the blocked frontier as a diagrammatic composition problem: identify objects, morphisms, mediating objects, and the exact commutativity or factorization obligation.
- Abstraction required: A structural account of the route in terms of source and target objects, typed morphisms, a mediating universal object, and the factorization or naturality law that would make the route compose.
- Minimal theorem shape: There exists a mediating object M and typed morphisms making the route commute; otherwise the failure is certified as no morphism, non-functorial transport, broken naturality, or missing universal property.
- Linked queue IDs: proofq.p-vs-np.001, proofq.p-vs-np.002, proofq.p-vs-np.005, proofq.p-vs-np.009, proofq.p-vs-np.010, proofq.p-vs-np.013, proofq.p-vs-np.018, proofq.p-vs-np.020, proofq.p-vs-np.021, proofq.p-vs-np.006, proofq.p-vs-np.007, proofq.p-vs-np.008
- Linked breakthrough families: realization, transport, bridge-specificity, barrier-aware transfer, alignment, constructive instantiation, semantic bridge

## System Prompt

Use category theory as a structural and compositional discovery lens, not as decorative abstraction. Identify the source object, target object, typed morphisms already available, and the diagram that should commute if the route is real. Search for a mediating object with a universal property, test whether the route factors through it, and classify failure as no morphism, non-functorial transport, broken naturality, missing factorization, or failed universal property.

## User Task

Reframe the blocked frontier as a family of diagrammatic composition problems. State candidate objects, morphisms, commutative squares, factorization claims, and universal properties that would make the live routes structurally compose.

## Required Questions

- What are the source object, target object, and typed morphisms already present in the route?
- What diagram should commute if the route is legitimate?
- What mediating object would be universal for this route?
- Does the route fail because there is no morphism, because the square does not commute, or because the factorization is missing?

## Expected Deliverables

- State one theorem-shaped candidate centered on `categorical-reframing` satisfying `There exists a mediating object M and typed morphisms making the route commute; otherwise the failure is certified as no morphism, non-functorial transport, broken naturality, or missing universal property.`.
- Make `A structural account of the route in terms of source and target objects, typed morphisms, a mediating universal object, and the factorization or naturality law that would make the route compose.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `renaming route components as categorical objects without reducing proof debt`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `categorical-reframing` remains purely schematic after the first explicit object or theorem candidate.

## Search Modes

- diagram construction
- commutativity checking
- factorization search
- universal-property search
- adjunction-style dualization

## Anti-Patterns

- renaming route components as categorical objects without reducing proof debt
- drawing a diagram without specifying the morphisms or the commutativity claim

## Lens Artifacts

- Routing heuristic: recommended=True | score=5/3
- Decision rule: Route to the categorical pathway only if at least three structural-composition criteria are active and the frontier is not merely a single local construction problem.
- Rationale: Route to category theory when the discovery problem is structurally about composition, mediation, and non-commuting interfaces rather than about one isolated construction.
- Active criteria:
  - There are multiple representations, object classes, or normal forms that need a structured correspondence.
  - The frontier includes transport, transfer, or interface claims that look like morphism-level obligations.
  - Several routes or route fragments need to compose, factor, or share a structural interface.
  - The missing move looks like a mediating object, factorization, or universal-property problem.
  - The blocked frontier already names structural failures such as alignment, transport, or characterization gaps.
- Epistemic lens: category-theoretic
- Diagram candidates:
  - Diagram candidate: local route for `carrier-realization` should factor from source-side object to mediating carrier implementing `An explicit obstruction family, witness family, surrogate promise problem, or quantitative measure that is realized from the source theorem rather than only named by role.` and then into the target activation interface.
  - Diagram candidate: local route for `formula-size-transport` should factor from source-side object to mediating carrier implementing `A transport law, compilation theorem, or complexity measure that is stable under the source-to-target model shift.` and then into the target activation interface.
  - Diagram candidate: local route for `target-grounding` should factor from source-side object to mediating carrier implementing `No new target theorem; discovery should instead seek the carrier, transfer law, or alignment theorem that makes the target theorem applicable.` and then into the target activation interface.
- Commutativity obligations:
  - Commutativity obligation: the route for `carrier-realization` must commute between source theorem hypotheses, the mediating carrier, and the target theorem hypotheses.
  - Commutativity obligation: the route for `formula-size-transport` must commute between source theorem hypotheses, the mediating carrier, and the target theorem hypotheses.
  - Commutativity obligation: the route for `target-grounding` must commute between source theorem hypotheses, the mediating carrier, and the target theorem hypotheses.
- Universal property candidates:
  - Universal-property candidate: search for an intermediate object universal for mediating `Turn a typed but schematic carrier into an explicit mathematical object family with admissibility conditions and a forcing theorem.`.
  - Universal-property candidate: search for an intermediate object universal for mediating `Find a theorem that preserves the relevant invariant across a cross-model move into formula-size.`.
  - Universal-property candidate: search for an intermediate object universal for mediating `Stop treating the target theorem as the open problem and relocate search to the bridge that would activate it.`.
- Negative outputs:
  - non_commuting_route
  - missing_universal_object
  - non_functorial_transport
  - broken_factorization

## Sample Theorem Targets

- Prove that the current route factors through a mediating carrier with a universal property, or show that no such factorization exists under the present invariants.

## Knowledge Source Invocation Policy

- Stage: discovery
- Target: Categorical Reframing Prompt
- Target kind: breakthrough-family

### Source Order

- `InformalMathLib` | role=local theorem, definition, barrier, and prior-result retrieval | default=query-first
  Invoke when: The current breakthrough-family may already be locally grounded for `Categorical Reframing Prompt`. A named theorem, route lemma, barrier, or prior negative result might already exist locally. Novelty or prior-art status cannot be assessed without checking local memory first.
  Do not use for: inventing a new bridge object by analogy alone claiming closure when the local hit is only topically related
  Success condition: Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.
  Current signal: current_mathlib_hits=0
- `IDE generative search` | role=local candidate generation for bridge objects, invariants, decompositions, and representation shifts | default=use-after-local-grounding
  Invoke when: Local KB and InformalMathLib ground `Categorical Reframing Prompt`, but the missing move is still conceptual rather than factual. The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate. The output can remain conjectural until independently grounded or refuted.
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

- Program ID: disclayer.p-vs-np.family.categorical-reframing
- Kind: discovery-branch
- Stage: discovery
- Target: There exists a mediating object M and typed morphisms making the route commute; otherwise the failure is certified as no morphism, non-functorial transport, broken naturality, or missing universal property.
- Nexus: Recast the blocked frontier as a diagrammatic composition problem: identify objects, morphisms, mediating objects, and the exact commutativity or factorization obligation.
- Bridge object: A structural account of the route in terms of source and target objects, typed morphisms, a mediating universal object, and the factorization or naturality law that would make the route compose. (breakthrough-family)
- Positive route: There exists a mediating object M and typed morphisms making the route commute; otherwise the failure is certified as no morphism, non-functorial transport, broken naturality, or missing universal property.
- Negative route: Avoid anti-patterns and branch-local dead ends while sharpening the theorem shape.

Anchors:
- queue-frontier: proofq.p-vs-np.001 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- queue-frontier: proofq.p-vs-np.002 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- queue-frontier: proofq.p-vs-np.005 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- queue-frontier: proofq.p-vs-np.009 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- queue-frontier: proofq.p-vs-np.010 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- queue-frontier: proofq.p-vs-np.013 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- queue-frontier: proofq.p-vs-np.018 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- queue-frontier: proofq.p-vs-np.020 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- queue-frontier: proofq.p-vs-np.021 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- queue-frontier: proofq.p-vs-np.006 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- queue-frontier: proofq.p-vs-np.007 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- queue-frontier: proofq.p-vs-np.008 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.categorical-reframing`.
- discovery-target: categorical-reframing | Categorical Reframing Prompt

Tensions:
- structural-composition-gap
- Required move: Recast the blocked frontier as a diagrammatic composition problem: identify objects, morphisms, mediating objects, and the exact commutativity or factorization obligation.
- Abstraction required: A structural account of the route in terms of source and target objects, typed morphisms, a mediating universal object, and the factorization or naturality law that would make the route compose.
- Minimal theorem shape: There exists a mediating object M and typed morphisms making the route commute; otherwise the failure is certified as no morphism, non-functorial transport, broken naturality, or missing universal property.

Proof debt:
- What are the source object, target object, and typed morphisms already present in the route?
- What diagram should commute if the route is legitimate?
- What mediating object would be universal for this route?
- Does the route fail because there is no morphism, because the square does not commute, or because the factorization is missing?
- State one theorem-shaped candidate centered on `categorical-reframing` satisfying `There exists a mediating object M and typed morphisms making the route commute; otherwise the failure is certified as no morphism, non-functorial transport, broken naturality, or missing universal property.`.
- Make `A structural account of the route in terms of source and target objects, typed morphisms, a mediating universal object, and the factorization or naturality law that would make the route compose.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

Decision gates:
- Branch stop criteria: Stop immediately if the branch collapses into the anti-pattern `renaming route components as categorical objects without reducing proof debt`.; Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.; Stop after one explicit positive candidate and one explicit failure probe have both been recorded.; Escalate if `categorical-reframing` remains purely schematic after the first explicit object or theorem candidate. -> Stop or re-route when the branch fails to produce a theorem-shaped gain.
- External framework search: targeted-foundation-search -> Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.

## External Framework Search Heuristic

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: sparse-object and distinguisher frameworks, duality or correspondence theorems, representation-theoretic normal forms, lower-bound barrier frameworks, local-reduction impossibility theory

## Local Prerequisites Before Browsing

- Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
- State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
- Reject at least one purely topical analogy before searching for an external framework.

## Query Templates

- mathematical framework for Categorical Reframing Prompt with preserved invariant and bridge theorem
- Categorical Reframing Prompt correspondence theorem transport invariant
- Categorical Reframing Prompt framework Recast the blocked frontier as a diagrammatic composition problem: identify objects, morphisms, mediating objects, and the exact commutativity or factorization obligation. theorem
- theorem or framework matching: There exists a mediating object M and typed morphisms making the route commute; otherwise the failure is certified as no morphism, non-functorial transport, broken naturality, or missing universal property.
