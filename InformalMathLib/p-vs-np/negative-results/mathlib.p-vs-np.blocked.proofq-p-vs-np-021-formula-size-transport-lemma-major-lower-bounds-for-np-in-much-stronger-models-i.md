<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Formula-Size Transport Lemma: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...

- Result ID: mathlib.p-vs-np.blocked.proofq-p-vs-np-021
- Outcome: blocked
- KB ref: p-vs-np
- Queue ID: proofq.p-vs-np.021
- Attempt ID: attempt.p-vs-np.026
- Bridge ID: bridge.010
- Source statement: st.thm.oliveira-pich-santhanam-magnification-near-state
- Target statement: st.thm.oliveira-santhanam-hardness-magnification-for-na
- Web search used: False
- Entry kind: negative-local-theorem

## Statement

No local formula-size transport theorem carries the near-threshold bridge.010 route into the target regime.

## Summary

The formula-size transport lemma for bridge.010 is blocked: even with the stronger near-threshold source theorem, the current artifacts still do not realize the cross-model move into formula-size.

## Informal Proof Or Disproof

# Proof Attempt: attempt.p-vs-np.026

- Queue ID: proofq.p-vs-np.021
- Status: blocked
- Conjecture: Prove a theorem transporting `MCSP obstruction family` from the nonuniform-circuits regime into the formula-size regime while preserving `MCSP complexity profile in nonuniform-circuits` strongly enough to lift `In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for...` into `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Bridge: bridge.010
- Source statement: st.thm.oliveira-pich-santhanam-magnification-near-state
- Target statement: st.thm.oliveira-santhanam-hardness-magnification-for-na

## Local Grounding

- Source excerpt: In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for suitable promise gaps and input length N=2^n ) imply major consequences such as NP not in P/poly.
- Target excerpt: There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).

## Queue Context

- Candidate object: MCSP obstruction family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route synopsis: Move from `st.thm.oliveira-pich-santhanam-magnification-near-state` on problem `MCSP` in model `nonuniform-circuits` using `In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for...` toward `st.thm.oliveira-santhanam-hardness-magnification-for-na` in model `formula-size` to obtain `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Route lemma under test: Prove that a MCSP witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.

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

- Program ID: attempt.p-vs-np.026
- Kind: proof-attempt
- Stage: prove
- Target: Prove a theorem transporting `MCSP obstruction family` from the nonuniform-circuits regime into the formula-size regime while preserving `MCSP complexity profile in nonuniform-circuits` strongly enough to lift `In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for...` into `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Nexus: Move from `st.thm.oliveira-pich-santhanam-magnification-near-state` on problem `MCSP` in model `nonuniform-circuits` using `In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for...` toward `st.thm.oliveira-santhanam-hardness-magnification-for-na` in model `formula-size` to obtain `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Bridge object: MCSP obstruction family (family of hard instances or obstructions forcing the target payoff)
- Positive route: Prove a theorem transporting `MCSP obstruction family` from the nonuniform-circuits regime into the formula-size regime while preserving `MCSP complexity profile in nonuniform-circuits` strongly enough to lift `In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for...` into `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Negative route: The transport lemma may only exploit the stronger source theorem rhetorically without proving the actual model shift.

Anchors:
- source-theorem: st.thm.oliveira-pich-santhanam-magnification-near-state | In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for suitable promise gaps and input length N=2^n ) imply major consequences such as NP not in P/poly.
- target-theorem: st.thm.oliveira-santhanam-hardness-magnification-for-na | There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).

Tensions:
- Route lemma under test: Prove that a MCSP witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Missing route lemma: Prove that a MCSP witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- The formula-size transport lemma for bridge.010 is blocked: even with the stronger near-threshold source theorem, the current artifacts still do not realize the cross-model move into formula-size.

Proof debt:
- State `Formula-Size Transport Lemma` on the theorem pair `st.thm.oliveira-pich-santhanam-magnification-near-state` -> `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
- Show why the blocked route summary `The bridge.010 obstruction-family repair is blocked: even starting from the stronger near-threshold MCSP theorem, the current artifacts still lack both a realized hard family and the nonuniform-circuits to formula-size transport theorem.` reduces to this lemma rather than to a broader bridge search.
- Either prove the lemma locally or explain why the local artifact stack still cannot realize it.
- The current route is blocked by a missing cross-model transport theorem, not just by the lack of a named carrier.
- No local MCSP obstruction-family theorem carries the near-threshold magnification route into the formula-size regime.
- Prove that a MCSP witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.

Decision gates:
- Web search gate: not-needed-local-obstruction -> The missing lemma is already locally identified; browsing is not yet decisive until the framework asks whether such a theorem exists in prior art.
- Negative-route heuristic:  -> Choose whether to continue constructive work, run a parallel negative branch, or switch to impossibility-first.
- Final assessment: blocked -> The formula-size transport lemma for bridge.010 is blocked: even with the stronger near-threshold source theorem, the current artifacts still do not realize the cross-model move into formula-size.

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

- Theorem statement: Prove a theorem transporting `MCSP obstruction family` from the nonuniform-circuits regime into the formula-size regime while preserving `MCSP complexity profile in nonuniform-circuits` strongly enough to lift `In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for...` into `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Route lemma under test: Prove that a MCSP witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
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

- Step 1: The repair lemma isolates the bridge.010 obstruction as a formula-size transport theorem starting from the stronger near-threshold source theorem.
  Justification: This is the theorem-sized form of the bridge.010 blocked result.
  Depends on: proofq.p-vs-np.013, proofq.p-vs-np.021
- Step 2: No local result shows that the stronger source theorem removes the model-shift defect or supplies the target transport theorem.
  Justification: The same nonuniform-circuits to formula-size shift remains unresolved.
  Depends on: proofq.p-vs-np.021
- Step 3: Therefore the repair lemma is blocked in the current local state.
  Justification: The stronger source theorem does not itself prove the cross-model transport lemma.
  Depends on: proofq.p-vs-np.013, proofq.p-vs-np.021

Negative-route analysis:

- Obstruction candidate: The transport lemma may only exploit the stronger source theorem rhetorically without proving the actual model shift.
- Negated claim: 
- Contradiction target: 
- Forbidden outcome: 
- Counterexample or barrier: No local theorem carries the near-threshold MCSP content into the formula-size target class.
- Impossibility claim: 
- Effect on claim: The route remains blocked at the same transport defect in a sharper source regime.

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
- No local formula-size transport theorem carries the near-threshold bridge.010 route into the target regime.

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
- The route is blocked by the same missing formula-size transport theorem, now in near-threshold form.

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
- Novelty assessment: The sharpened diagnosis is that even the better source theorem does not eliminate the formula-size transport obligation.
- Confidence: high
- Result statement: No local formula-size transport theorem carries the near-threshold bridge.010 route into the target regime.
- Result summary: The formula-size transport lemma for bridge.010 is blocked: even with the stronger near-threshold source theorem, the current artifacts still do not realize the cross-model move into formula-size.

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
