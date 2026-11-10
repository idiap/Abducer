<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Local Reduction Gadget Lemma: is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...

- Result ID: mathlib.p-vs-np.blocked.proofq-p-vs-np-019
- Outcome: blocked
- KB ref: p-vs-np
- Queue ID: proofq.p-vs-np.019
- Attempt ID: attempt.p-vs-np.024
- Bridge ID: bridge.007
- Source statement: st.thm.karp-many-natural-problems-are-np-complete-karp1
- Target statement: st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo
- Web search used: False
- Entry kind: negative-local-theorem

## Statement

No local gadget theorem realizes the transfer from ordinary NP-complete problems to the MCSP local-reduction setting.

## Summary

The local reduction gadget lemma is blocked: the current artifacts still contain no explicit family of local reductions carrying ordinary NP-complete instances into the MCSP local-reduction regime.

## Informal Proof Or Disproof

# Proof Attempt: attempt.p-vs-np.024

- Queue ID: proofq.p-vs-np.019
- Status: blocked
- Conjecture: Construct and verify an explicit local reduction gadget family witnessing how `NP-complete under polynomial-time many-one reductions` transfers into the MCSP local-reduction regime while preserving `consequence schema NP-complete-classification`.
- Bridge: bridge.007
- Source statement: st.thm.karp-many-natural-problems-are-np-complete-karp1
- Target statement: st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo

## Local Grounding

- Source excerpt: There exist many problems L in combinatorial optimisation/graph theory such that L is NP-complete under polynomial-time many-one reductions.
- Target excerpt: Under"local"polynomial-time reductions (where each output bit is computable with very small time), MCSP is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various reductions would entail unexpected class separations.

## Queue Context

- Candidate object: unspecified reduction gadget family
- Invariant: consequence schema NP-complete-classification
- Route synopsis: Move from `st.thm.karp-many-natural-problems-are-np-complete-karp1` using `NP-complete under polynomial-time many-one reductions` toward `st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo` on problem `MCSP` to obtain `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...`.
- Route lemma under test: Prove that a hardness-magnification witness family turns `NP-complete under polynomial-time many-one reductions` into `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...` while preserving `consequence schema NP-complete-classification`.

## Local InformalMathLib Hits

- No local InformalMathLib hits were found.

## Web Search Gate

Default policy:
- Do not search the web by default. Exhaust the local KB, current artifacts, and local InformalMathLib first.
- Search only if the missing fact is decisive for a proof step, prior-art check, or exact theorem attribution.
- Search when a named theorem, barrier, paper, or threshold fact is not present locally and materially affects the result.
- Do not search for generic background, motivation, or intuitive exposition.
- If web search is used, record the concrete query, the exact source, and what proof step or novelty decision it informed.

## Knowledge Source Invocation Policy

- Stage: 
- Target: 
- Target kind: 

### Source Order


### Consistency Rules


### Escalation Rules


## PDL Program

- Program ID: attempt.p-vs-np.024
- Kind: proof-attempt
- Stage: prove
- Target: Construct and verify an explicit local reduction gadget family witnessing how `NP-complete under polynomial-time many-one reductions` transfers into the MCSP local-reduction regime while preserving `consequence schema NP-complete-classification`.
- Nexus: Move from `st.thm.karp-many-natural-problems-are-np-complete-karp1` using `NP-complete under polynomial-time many-one reductions` toward `st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo` on problem `MCSP` to obtain `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...`.
- Bridge object: unspecified reduction gadget family (family of reductions preserving the route witness structure)
- Positive route: Construct and verify an explicit local reduction gadget family witnessing how `NP-complete under polynomial-time many-one reductions` transfers into the MCSP local-reduction regime while preserving `consequence schema NP-complete-classification`.
- Negative route: The proposed gadget theorem may still hide the core locality requirement instead of proving it.

Anchors:
- source-theorem: st.thm.karp-many-natural-problems-are-np-complete-karp1 | There exist many problems L in combinatorial optimisation/graph theory such that L is NP-complete under polynomial-time many-one reductions.
- target-theorem: st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo | Under"local"polynomial-time reductions (where each output bit is computable with very small time), MCSP is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various reductions would entail unexpected class separations.

Tensions:
- Route lemma under test: Prove that a hardness-magnification witness family turns `NP-complete under polynomial-time many-one reductions` into `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...` while preserving `consequence schema NP-complete-classification`.
- Missing route lemma: Prove that a hardness-magnification witness family turns `NP-complete under polynomial-time many-one reductions` into `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...` while preserving `consequence schema NP-complete-classification`.
- The local reduction gadget lemma is blocked: the current artifacts still contain no explicit family of local reductions carrying ordinary NP-complete instances into the MCSP local-reduction regime.

Proof debt:
- State `Local Reduction Gadget Lemma` on the theorem pair `st.thm.karp-many-natural-problems-are-np-complete-karp1` -> `st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo`.
- Show why the blocked route summary `The reduction-gadget repair for bridge.007 is blocked: it sharpens the transfer mechanism sought, but the current artifacts still contain no explicit family of local reductions carrying ordinary NP-completeness into the MCSP local-reduction regime.` reduces to this lemma rather than to a broader bridge search.
- Either prove the lemma locally or explain why the local artifact stack still cannot realize it.
- The route is blocked by the absence of an explicit local reduction family realizing the transfer.
- No local reduction-gadget family transports ordinary NP-completeness into the MCSP local-reduction setting.
- Prove that a hardness-magnification witness family turns `NP-complete under polynomial-time many-one reductions` into `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...` while preserving `consequence schema NP-complete-classification`.

Decision gates:
- Web search gate: not-needed-local-obstruction -> The missing lemma is already locally identified; browsing is not yet decisive until the framework asks whether such a theorem exists in prior art.
- Negative-route heuristic:  -> Choose whether to continue constructive work, run a parallel negative branch, or switch to impossibility-first.
- Final assessment: blocked -> The local reduction gadget lemma is blocked: the current artifacts still contain no explicit family of local reductions carrying ordinary NP-complete instances into the MCSP local-reduction regime.

Decision: fill this in only if a decisive local gap appears.

## External References To Import Into InformalMathLib

If you use an external theorem, definition, or axiom, record it here in the JSON as an object with:
- `reference_type`: theorem, definition, or axiom
- `title`
- `statement`
- `source_name`
- `source_url`
- `search_query`
- `used_for`
- `notes`

## Informal Proof Or Disproof Attempt

- Theorem statement: Construct and verify an explicit local reduction gadget family witnessing how `NP-complete under polynomial-time many-one reductions` transfers into the MCSP local-reduction regime while preserving `consequence schema NP-complete-classification`.
- Route lemma under test: Prove that a hardness-magnification witness family turns `NP-complete under polynomial-time many-one reductions` into `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...` while preserving `consequence schema NP-complete-classification`.
- Strategy family: repair-lemma

### Informal Tactic Playbook

- No tactic playbook recorded.

### Informal Tactic Trace

- No tactic trace recorded.

### Negative-Route Heuristic

- No negative-route heuristic recorded.

### Contradiction / Impossibility Frame

- No contradiction frame recorded.

Stepwise argument:

- Step 1: The repair lemma narrows the bridge.007 obstruction to an explicit local reduction gadget theorem.
  Justification: This is the natural theorem-sized form of the earlier reduction-gadget failure.
  Depends on: proofq.p-vs-np.012, proofq.p-vs-np.019
- Step 2: No local result exhibits such a reduction family or verifies its locality properties against the target theorem.
  Justification: The source theorem stays in the ordinary many-one regime, while the target theorem is explicitly local-reduction sensitive.
  Depends on: proofq.p-vs-np.019
- Step 3: Therefore the repair lemma is blocked in the current local state.
  Justification: The transfer from ordinary NP-completeness to MCSP local reductions remains unproved.
  Depends on: proofq.p-vs-np.012, proofq.p-vs-np.019

Negative-route analysis:

- Obstruction candidate: The proposed gadget theorem may still hide the core locality requirement instead of proving it.
- Negated claim: 
- Contradiction target: 
- Forbidden outcome: 
- Counterexample or barrier: The artifacts contain no explicit local reduction family whose output bits satisfy the target theorem's locality regime.
- Impossibility claim: 
- Effect on claim: The route remains blocked at the local reduction gadget step.

## Critique Judges

### Statement Grounding Judge

- Is the claim under test stated explicitly and does it match the queue item?
- Are source and target statements grounded in local KB statement ids or InformalMathLib entries?
- Does each proof step say what prior local statement or earlier step it depends on?

Verdict: pass
Notes:
- The repair lemma is explicit and matches the narrowed blocked route.

### Inferential Validity Judge

- Does each step follow informally from its stated dependencies?
- Are quantifiers, regimes, and model shifts preserved rather than silently changed?
- Is the conclusion exactly the claimed result rather than a nearby weaker statement?

Verdict: fail
Blocking issues:
- No local gadget theorem realizes the transfer from ordinary NP-complete problems to the MCSP local-reduction setting.

### Assumption Discipline Judge

- Did the proof introduce any hidden assumptions not already declared?
- Are all uses of prior lemmas, barriers, and transfer claims explicit?
- If an extra assumption is necessary, is the outcome downgraded to a conditional result?

Verdict: pass
Notes:
- The blocked assessment does not presuppose the missing lemma.

### Prior-Art And Novelty Judge

- Can the result already be recovered from local InformalMathLib or KB material?
- If not locally, is a web search required by the search policy before claiming novelty?
- If prior art exists, should the outcome be reclassified as reconstruction or prior_art_found?

Verdict: pass
Notes:
- No local InformalMathLib result discharges this repair lemma.
- Web search was not triggered because the main issue is still local non-realization rather than unresolved attribution.

### Obstruction And Negative-Route Judge

- Does the current argument survive the designated negative route or obstruction check?
- Is there a counterexample, barrier, or failure mode that blocks the route?
- If the route fails, is the negative result itself clearly formulated?

Verdict: fail
Blocking issues:
- The route is blocked by the absence of a verified local reduction gadget family.

### Closure Judge

- Is the final outcome correctly classified as proved, disproved, blocked, deferred, or prior_art_found?
- Does the written proof or disproof support that classification?
- Is the result statement ready to persist into InformalMathLib if the outcome is terminal?

Verdict: pass
Notes:
- Blocked is the correct terminal classification for the current local state.

## Final Assessment

- Outcome: blocked
- Verdict: blocked
- Novelty assessment: The refined diagnosis is that the missing theorem is a locality-preserving reduction construction.
- Confidence: high
- Result statement: No local gadget theorem realizes the transfer from ordinary NP-complete problems to the MCSP local-reduction setting.
- Result summary: The local reduction gadget lemma is blocked: the current artifacts still contain no explicit family of local reductions carrying ordinary NP-complete instances into the MCSP local-reduction regime.

## Major Subresult Assessment

Use this only for terminal `proved` or `disproved` outcomes that might warrant a standalone paper in `artifacts/<kb-ref>/produced_papers`.

Mandatory gates:
- Self-contained statement: False
- Mathematical inspectability: False
- Nontrivial frontier relation: False
- Independent value: False

0-3 axis scores:
- Frontier shift: 1
- Independence: 1
- Transferability: 1
- Barrier clarity: 2
- Proof closure: 0
- Search compression: 2

Threshold rule: all mandatory gates pass, total score >= 11, and at least one of frontier shift / independence / barrier clarity is 3.

- Paper candidate title: 
- Paper candidate summary: 
- Overall judgment: Useful missing-lemma localization, but not paper-worthy.
