<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Formula-Size Transport Lemma: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...

- Result ID: mathlib.p-vs-np.blocked.proofq-p-vs-np-020
- Outcome: blocked
- KB ref: p-vs-np
- Queue ID: proofq.p-vs-np.020
- Attempt ID: attempt.p-vs-np.025
- Bridge ID: bridge.002
- Source statement: st.def.hardness-magnification-phenomenon-programme-leve
- Target statement: st.thm.oliveira-santhanam-hardness-magnification-for-na
- Web search used: False
- Entry kind: negative-local-theorem

## Statement

No local formula-size transport theorem carries the bridge.002 MCSP obstruction-family route into the target regime.

## Summary

The formula-size transport lemma for bridge.002 is blocked: the current artifacts still do not prove how the MCSP obstruction-family data crosses from nonuniform circuits into the formula-size regime.

## Informal Proof Or Disproof

# Proof Attempt: attempt.p-vs-np.025

- Queue ID: proofq.p-vs-np.020
- Status: blocked
- Conjecture: Prove a theorem transporting `MCSP obstruction family` from the nonuniform-circuits regime into the formula-size regime while preserving `MCSP complexity profile in nonuniform-circuits` strongly enough to lift `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Bridge: bridge.002
- Source statement: st.def.hardness-magnification-phenomenon-programme-leve
- Target statement: st.thm.oliveira-santhanam-hardness-magnification-for-na

## Local Grounding

- Source excerpt: A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.
- Target excerpt: There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).

## Queue Context

- Candidate object: MCSP obstruction family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route synopsis: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.oliveira-santhanam-hardness-magnification-for-na` in model `formula-size` to obtain `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Route lemma under test: Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.

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

- Program ID: attempt.p-vs-np.025
- Kind: proof-attempt
- Stage: prove
- Target: Prove a theorem transporting `MCSP obstruction family` from the nonuniform-circuits regime into the formula-size regime while preserving `MCSP complexity profile in nonuniform-circuits` strongly enough to lift `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Nexus: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.oliveira-santhanam-hardness-magnification-for-na` in model `formula-size` to obtain `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Bridge object: MCSP obstruction family (family of hard instances or obstructions forcing the target payoff)
- Positive route: Prove a theorem transporting `MCSP obstruction family` from the nonuniform-circuits regime into the formula-size regime while preserving `MCSP complexity profile in nonuniform-circuits` strongly enough to lift `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Negative route: The transport lemma may only restate the source and target regimes without proving preservation across them.

Anchors:
- source-theorem: st.def.hardness-magnification-phenomenon-programme-leve | A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.
- target-theorem: st.thm.oliveira-santhanam-hardness-magnification-for-na | There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).

Tensions:
- Route lemma under test: Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Missing route lemma: Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- The formula-size transport lemma for bridge.002 is blocked: the current artifacts still do not prove how the MCSP obstruction-family data crosses from nonuniform circuits into the formula-size regime.

Proof debt:
- State `Formula-Size Transport Lemma` on the theorem pair `st.def.hardness-magnification-phenomenon-programme-leve` -> `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
- Show why the blocked route summary `The second-order bridge.002 repair is blocked: the stronger carrier requirement clarifies the object sought, but the current artifacts still lack both a realized hard family and the nonuniform-circuits -> formula-size transport theorem.` reduces to this lemma rather than to a broader bridge search.
- Either prove the lemma locally or explain why the local artifact stack still cannot realize it.
- The current route is blocked by a missing cross-model transport theorem, not just by the lack of a named carrier.
- No local MCSP obstruction-family theorem transports the leading magnification route into the formula-size regime.
- Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.

Decision gates:
- Web search gate: not-needed-local-obstruction -> The missing lemma is already locally identified; browsing is not yet decisive until the framework asks whether such a theorem exists in prior art.
- Negative-route heuristic:  -> Choose whether to continue constructive work, run a parallel negative branch, or switch to impossibility-first.
- Final assessment: blocked -> The formula-size transport lemma for bridge.002 is blocked: the current artifacts still do not prove how the MCSP obstruction-family data crosses from nonuniform circuits into the formula-size regime.

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

- Theorem statement: Prove a theorem transporting `MCSP obstruction family` from the nonuniform-circuits regime into the formula-size regime while preserving `MCSP complexity profile in nonuniform-circuits` strongly enough to lift `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Route lemma under test: Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
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

- Step 1: The repair lemma correctly names the missing theorem as a cross-model transport result into formula-size.
  Justification: This is the theorem-sized version of the bridge.002 transport defect.
  Depends on: proofq.p-vs-np.010, proofq.p-vs-np.020
- Step 2: No local result establishes that the invariant survives the nonuniform-circuits to formula-size shift in the way the target theorem requires.
  Justification: The model shift remains explicit in the route synopsis and unresolved in the blocked abstraction attempt.
  Depends on: proofq.p-vs-np.020
- Step 3: Therefore the formula-size transport lemma is blocked in the current local state.
  Justification: The route still needs a concrete cross-model theorem, not just a stronger obstruction-family carrier.
  Depends on: proofq.p-vs-np.010, proofq.p-vs-np.020

Negative-route analysis:

- Obstruction candidate: The transport lemma may only restate the source and target regimes without proving preservation across them.
- Negated claim: 
- Contradiction target: 
- Forbidden outcome: 
- Counterexample or barrier: No local theorem identifies the invariant-preserving map into the formula-size target setting.
- Impossibility claim: 
- Effect on claim: The route remains blocked at the cross-model transport step.

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
- No local formula-size transport theorem carries the bridge.002 MCSP obstruction-family route into the target regime.

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
- The route is blocked by the lack of an invariant-preserving nonuniform-circuits -> formula-size transport theorem.

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
- Novelty assessment: The route is now localized to one transport theorem rather than a vague formula-size gap.
- Confidence: high
- Result statement: No local formula-size transport theorem carries the bridge.002 MCSP obstruction-family route into the target regime.
- Result summary: The formula-size transport lemma for bridge.002 is blocked: the current artifacts still do not prove how the MCSP obstruction-family data crosses from nonuniform circuits into the formula-size regime.

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
