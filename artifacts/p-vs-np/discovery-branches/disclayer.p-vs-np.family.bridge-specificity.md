# Discovery Branch disclayer.p-vs-np.family.bridge-specificity

- KB ref: p-vs-np
- Status: completed
- Kind: breakthrough-family
- Target: Activation Theorem Prompt
- Routing priority: 5.669
- Dispatch rank: 6

## Why This Branch Exists

Spawn a dedicated `bridge-specificity` discovery layer because obstruction `target-grounding` carries repeated pressure across the blocked frontier.

Stop treating the target theorem as the open problem and relocate search to the bridge that would activate it.

## Discovery Contract

- Required move: Stop treating the target theorem as the open problem and relocate search to the bridge that would activate it.
- Abstraction required: No new target theorem; discovery should instead seek the carrier, transfer law, or alignment theorem that makes the target theorem applicable.
- Minimal theorem shape: Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T's hypotheses from current artifacts.
- Linked queue IDs: proofq.p-vs-np.006, proofq.p-vs-np.007, proofq.p-vs-np.008, proofq.p-vs-np.014, proofq.p-vs-np.015, proofq.p-vs-np.016, proofq.p-vs-np.017, proofq.p-vs-np.022, proofq.p-vs-np.024
- Linked breakthrough families: bridge-specificity

## System Prompt

The target theorem is already known. Your task is to identify the local activation theorem that would verify its hypotheses from current artifacts. Do not rediscover the target theorem.

## User Task

State the activation theorem under search, name the exact target hypothesis that is still unverified, and identify the local bridge object or transfer law needed to verify it.

## Required Questions

- Which target-theorem hypothesis is still open locally?
- What bridge-local theorem would certify that hypothesis?
- What novelty remains once the target theorem itself is removed from search?

## Expected Deliverables

- State one theorem-shaped candidate centered on `bridge-specificity` satisfying `Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T's hypotheses from current artifacts.`.
- Make `No new target theorem; discovery should instead seek the carrier, transfer law, or alignment theorem that makes the target theorem applicable.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

## Stop Criteria

- Stop immediately if the branch collapses into the anti-pattern `rediscovering the target theorem`.
- Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.
- Stop after one explicit positive candidate and one explicit failure probe have both been recorded.
- Escalate if `bridge-specificity` remains purely schematic after the first explicit object or theorem candidate.

## Search Modes

- activation theorem search
- hypothesis verification search
- bridge-localization refinement

## Anti-Patterns

- rediscovering the target theorem
- claiming novelty at the target instead of at the activation bridge

## Lens Artifacts

- Epistemic lens: 

## Sample Theorem Targets

- There exists an admissible TAUT proof progress measure, realized as a monotone potential function over proofs or certificates, such that whenever A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is... holds for TAUT in Cook-Reckhow-proof-system, the object organizes the source-side mathematical content while preserving the invariant TAUT complexity profile in Cook-Reckhow-proof-system and yields There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP.
- There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A language L is emph NP-complete (under le_m^p ) iff (i) LinNP holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification and yields NP-complete under polynomial-time many-one reductions.

## Knowledge Source Invocation Policy

- Stage: discovery
- Target: Activation Theorem Prompt
- Target kind: breakthrough-family

### Source Order

- `InformalMathLib` | role=local theorem, definition, barrier, and prior-result retrieval | default=query-first
  Invoke when: The current breakthrough-family may already be locally grounded for `Activation Theorem Prompt`. A named theorem, route lemma, barrier, or prior negative result might already exist locally. Novelty or prior-art status cannot be assessed without checking local memory first.
  Do not use for: inventing a new bridge object by analogy alone claiming closure when the local hit is only topically related
  Success condition: Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.
  Current signal: current_mathlib_hits=0
- `IDE generative search` | role=local candidate generation for bridge objects, invariants, decompositions, and representation shifts | default=use-after-local-grounding
  Invoke when: Local KB and InformalMathLib ground `Activation Theorem Prompt`, but the missing move is still conceptual rather than factual. The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate. The output can remain conjectural until independently grounded or refuted.
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

- Program ID: disclayer.p-vs-np.family.bridge-specificity
- Kind: discovery-branch
- Stage: discovery
- Target: Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T's hypotheses from current artifacts.
- Nexus: Stop treating the target theorem as the open problem and relocate search to the bridge that would activate it.
- Bridge object: No new target theorem; discovery should instead seek the carrier, transfer law, or alignment theorem that makes the target theorem applicable. (breakthrough-family)
- Positive route: Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T's hypotheses from current artifacts.
- Negative route: Avoid anti-patterns and branch-local dead ends while sharpening the theorem shape.

Anchors:
- queue-frontier: proofq.p-vs-np.006 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.bridge-specificity`.
- queue-frontier: proofq.p-vs-np.007 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.bridge-specificity`.
- queue-frontier: proofq.p-vs-np.008 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.bridge-specificity`.
- queue-frontier: proofq.p-vs-np.014 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.bridge-specificity`.
- queue-frontier: proofq.p-vs-np.015 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.bridge-specificity`.
- queue-frontier: proofq.p-vs-np.016 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.bridge-specificity`.
- queue-frontier: proofq.p-vs-np.017 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.bridge-specificity`.
- queue-frontier: proofq.p-vs-np.022 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.bridge-specificity`.
- queue-frontier: proofq.p-vs-np.024 | Blocked or active route linked to discovery branch `disclayer.p-vs-np.family.bridge-specificity`.
- discovery-target: bridge-specificity | Activation Theorem Prompt

Tensions:
- target-grounding
- Required move: Stop treating the target theorem as the open problem and relocate search to the bridge that would activate it.
- Abstraction required: No new target theorem; discovery should instead seek the carrier, transfer law, or alignment theorem that makes the target theorem applicable.
- Minimal theorem shape: Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T's hypotheses from current artifacts.

Proof debt:
- Which target-theorem hypothesis is still open locally?
- What bridge-local theorem would certify that hypothesis?
- What novelty remains once the target theorem itself is removed from search?
- State one theorem-shaped candidate centered on `bridge-specificity` satisfying `Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T's hypotheses from current artifacts.`.
- Make `No new target theorem; discovery should instead seek the carrier, transfer law, or alignment theorem that makes the target theorem applicable.` explicit enough that an expert could inspect the object or transfer law.
- Record one decisive negative route explaining what would fail if this discovery layer does not land.

Decision gates:
- Branch stop criteria: Stop immediately if the branch collapses into the anti-pattern `rediscovering the target theorem`.; Stop if the branch yields no theorem-shaped claim, carrier, transport principle, invariant, or representation change.; Stop after one explicit positive candidate and one explicit failure probe have both been recorded.; Escalate if `bridge-specificity` remains purely schematic after the first explicit object or theorem candidate. -> Stop or re-route when the branch fails to produce a theorem-shaped gain.
- External framework search: targeted-foundation-search -> Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.

## External Framework Search Heuristic

- Recommended: True
- Mode: targeted-foundation-search
- Justification: Search externally for a mathematical framework with similar structural properties only after local routes, InformalMathLib, and explicit negative probes fail to provide the missing carrier, invariant, transfer law, or correspondence theorem.
- Candidate framework regions: activation-theorem frameworks, hypothesis-verification templates from neighboring areas

## Local Prerequisites Before Browsing

- Record the failed local theorem lookup, InformalMathLib lookup, and negative probe that justify leaving local search.
- State the missing operation concretely: carrier realization, transport, alignment, explicitness, characterization, or invariant discovery.
- Reject at least one purely topical analogy before searching for an external framework.

## Query Templates

- mathematical framework for Activation Theorem Prompt with preserved invariant and bridge theorem
- Activation Theorem Prompt correspondence theorem transport invariant
- Activation Theorem Prompt framework Stop treating the target theorem as the open problem and relocate search to the bridge that would activate it. theorem
- theorem or framework matching: Target theorem T is fixed. The real theorem under search is the local activation theorem A that verifies T's hypotheses from current artifacts.
