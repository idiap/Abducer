<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# MCSP obstruction family: major consequences such as NP not in P/poly

- Result ID: mathlib.p-vs-np.blocked.proofq-p-vs-np-009
- Outcome: blocked
- KB ref: p-vs-np
- Queue ID: proofq.p-vs-np.009
- Attempt ID: attempt.p-vs-np.014
- Bridge ID: bridge.001
- Source statement: st.def.hardness-magnification-phenomenon-programme-leve
- Target statement: st.thm.oliveira-pich-santhanam-magnification-near-state
- Web search used: False
- Entry kind: negative-local-theorem

## Statement

No explicit MCSP obstruction family is locally realized for the leading hardness-magnification route.

## Summary

The second-order repair conjecture is blocked: it clarifies the kind of hard family the route would need, but the current artifacts still provide only a typed role-description and no concrete forcing object.

## Informal Proof Or Disproof

# Proof Attempt: attempt.p-vs-np.014

- Queue ID: proofq.p-vs-np.009
- Status: blocked
- Conjecture: An adequate `canonical-obstruction-family` bridge concept for `bridge.001` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `nonuniform-circuit-exponential-lower-bound`, preserves `MCSP complexity profile in nonuniform-circuits`, and is strong enough to force `NP-not-in-P/poly`.
- Bridge: bridge.001
- Source statement: st.def.hardness-magnification-phenomenon-programme-leve
- Target statement: st.thm.oliveira-pich-santhanam-magnification-near-state

## Local Grounding

- Source excerpt: A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.
- Target excerpt: In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for suitable promise gaps and input length N=2^n ) imply major consequences such as NP not in P/poly.

## Queue Context

- Candidate object: MCSP obstruction family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route synopsis: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.oliveira-pich-santhanam-magnification-near-state` in model `nonuniform-circuits` to obtain `major consequences such as NP not in P/poly`.
- Route lemma under test: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.

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

- Program ID: attempt.p-vs-np.014
- Kind: proof-attempt
- Stage: prove
- Target: An adequate `canonical-obstruction-family` bridge concept for `bridge.001` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `nonuniform-circuit-exponential-lower-bound`, preserves `MCSP complexity profile in nonuniform-circuits`, and is strong enough to force `NP-not-in-P/poly`.
- Nexus: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.oliveira-pich-santhanam-magnification-near-state` in model `nonuniform-circuits` to obtain `major consequences such as NP not in P/poly`.
- Bridge object: MCSP obstruction family (family of hard instances or obstructions forcing the target payoff)
- Positive route: An adequate `canonical-obstruction-family` bridge concept for `bridge.001` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `nonuniform-circuit-exponential-lower-bound`, preserves `MCSP complexity profile in nonuniform-circuits`, and is strong enough to force `NP-not-in-P/poly`.
- Negative route: The proposed obstruction family may only restate the desired payoff as a typed role-description.

Anchors:
- source-theorem: st.def.hardness-magnification-phenomenon-programme-leve | A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.
- target-theorem: st.thm.oliveira-pich-santhanam-magnification-near-state | In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for suitable promise gaps and input length N=2^n ) imply major consequences such as NP not in P/poly.

Tensions:
- Route lemma under test: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.
- Missing route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.
- The second-order repair conjecture is blocked: it clarifies the kind of hard family the route would need, but the current artifacts still provide only a typed role-description and no concrete forcing object.

Proof debt:
- Source-to-object claim: build `MCSP obstruction family` from the source theorem content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` available in st.def.hardness-magnification-phenomenon-programme-leve (problems MCSP; models nonuniform-circuits; claims A barely-nontrivial lower bound for an explicit problem Q in a weak model, MCSP nonuniform circuits lower bound).
- Transport claim: prove that `MCSP obstruction family` preserves `MCSP complexity profile in nonuniform-circuits` across the route nonuniform-circuits.
- Payoff claim: show that `MCSP obstruction family` upgrades major separation consequence and thereby upgrade `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` in st.thm.oliveira-pich-santhanam-magnification-near-state (problems MCSP; models nonuniform-circuits; claims major consequences such as NP not in P/poly, MCSP nonuniform circuits lower bound).
- Specify the mathematical carrier and admissibility conditions of `MCSP obstruction family` as a family of hard instances or obstructions forcing the target payoff.
- Locate where `MCSP complexity profile in nonuniform-circuits` lives and how it is measured inside the conjectured object while crossing nonuniform-circuits.
- State the first theorem-family lemma that turns `MCSP obstruction family` from `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly`.
- Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.

Decision gates:
- Web search gate: not-needed-local-obstruction -> The blocking issue is already local and structural: the conjecture does not identify a concrete hard-instance family or forcing lemma, so browsing is not yet decisive.
- Negative-route heuristic:  -> Choose whether to continue constructive work, run a parallel negative branch, or switch to impossibility-first.
- Final assessment: blocked -> The second-order repair conjecture is blocked: it clarifies the kind of hard family the route would need, but the current artifacts still provide only a typed role-description and no concrete forcing object.

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

- Theorem statement: An adequate `canonical-obstruction-family` bridge concept for `bridge.001` is a `family of hard instances or obstructions forcing the target payoff` named `MCSP obstruction family` that absorbs `nonuniform-circuit-exponential-lower-bound`, preserves `MCSP complexity profile in nonuniform-circuits`, and is strong enough to force `NP-not-in-P/poly`.
- Route lemma under test: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.
- Strategy family: canonical-obstruction-family

### Informal Tactic Playbook

- No tactic playbook recorded.

### Informal Tactic Trace

- No tactic trace recorded.

### Negative-Route Heuristic

- No negative-route heuristic recorded.

### Contradiction / Impossibility Frame

- No contradiction frame recorded.

Stepwise argument:

- Step 1: The repair conjecture sharpens the blocked route into a typed carrier requirement, but it does not itself construct an explicit MCSP obstruction family.
  Justification: The theorem statement and proof obligations specify what the carrier must do, but they remain definitional and conditional rather than realized by a local theorem.
  Depends on: proofq.p-vs-np.009, st.def.hardness-magnification-phenomenon-programme-leve, st.thm.oliveira-pich-santhanam-magnification-near-state
- Step 2: No local result currently builds a hard-instance family that absorbs the source-side lower-bound content and forces NP not in P/poly.
  Justification: The local InformalMathLib is empty on this route, the queue item still lists source-to-object construction as an open obligation, and the missing route lemma is unchanged from the blocked first-layer route.
  Depends on: proofq.p-vs-np.001, proofq.p-vs-np.009
- Step 3: Therefore the obstruction-family reformulation is a useful sharpening of the missing object, but the conjecture is blocked as a proof target in the current local state.
  Justification: Without a realized carrier, the transport and payoff obligations remain conditional, and the negative route reduces the conjecture to topical overlap dressed as a stronger object.
  Depends on: proofq.p-vs-np.009

Negative-route analysis:

- Obstruction candidate: The proposed obstruction family may only restate the desired payoff as a typed role-description.
- Negated claim: 
- Contradiction target: 
- Forbidden outcome: 
- Counterexample or barrier: The current artifacts specify admissibility clauses for such a family, but they do not exhibit a single concrete hard-instance family or obstruction theorem that realizes those clauses on the source-target theorem pair.
- Impossibility claim: 
- Effect on claim: The route remains blocked: the stronger carrier language sharpens the missing bridge, but it does not close the proof obligation.

## Critique Judges

### Statement Grounding Judge

- Is the claim under test stated explicitly and does it match the queue item?
- Are source and target statements grounded in local KB statement ids or InformalMathLib entries?
- Does each proof step say what prior local statement or earlier step it depends on?

Verdict: pass
Notes:
- The conjecture is explicit, theorem-pair grounded, and tied to the blocked bridge.001 route.

### Inferential Validity Judge

- Does each step follow informally from its stated dependencies?
- Are quantifiers, regimes, and model shifts preserved rather than silently changed?
- Is the conclusion exactly the claimed result rather than a nearby weaker statement?

Verdict: fail
Blocking issues:
- No local theorem realizes the claimed obstruction family.
- The route lemma remains identical to the blocked first-layer magnification obligation.

### Assumption Discipline Judge

- Did the proof introduce any hidden assumptions not already declared?
- Are all uses of prior lemmas, barriers, and transfer claims explicit?
- If an extra assumption is necessary, is the outcome downgraded to a conditional result?

Verdict: pass
Notes:
- The blocked assessment does not assume the carrier exists; it treats existence as the unresolved issue.

### Prior-Art And Novelty Judge

- Can the result already be recovered from local InformalMathLib or KB material?
- If not locally, is a web search required by the search policy before claiming novelty?
- If prior art exists, should the outcome be reclassified as reconstruction or prior_art_found?

Verdict: pass
Notes:
- No local InformalMathLib result duplicates this exact obstruction-family formulation.
- Web search was not triggered because the failure is already a local realization defect, not a missing attribution question.

### Obstruction And Negative-Route Judge

- Does the current argument survive the designated negative route or obstruction check?
- Is there a counterexample, barrier, or failure mode that blocks the route?
- If the route fails, is the negative result itself clearly formulated?

Verdict: fail
Blocking issues:
- The conjecture survives only as a role-description; it fails the negative-route check against mere topical overlap.

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
- Novelty assessment: The value here is not a new theorem but a sharper obstruction: the route needs a concrete hard-instance family, not another renamed witness carrier.
- Confidence: high
- Result statement: No explicit MCSP obstruction family is locally realized for the leading hardness-magnification route.
- Result summary: The second-order repair conjecture is blocked: it clarifies the kind of hard family the route would need, but the current artifacts still provide only a typed role-description and no concrete forcing object.

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
- Overall judgment: Useful obstruction sharpening for the leading route, but not paper-worthy without a realized hard family.
