<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# PIT Upgrade Lemma: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...

- Result ID: mathlib.p-vs-np.blocked.proofq-p-vs-np-017
- Outcome: blocked
- KB ref: p-vs-np
- Queue ID: proofq.p-vs-np.017
- Attempt ID: attempt.p-vs-np.022
- Bridge ID: bridge.013
- Source statement: st.def.hitting-set-for-pit-black-box
- Target statement: st.thm.kabanets-impagliazzo-pit-derandomisation-implies
- Web search used: False
- Entry kind: negative-local-theorem

## Statement

No local upgrade theorem turns the PIT certificate-family object into the PIT-derandomization premise used by the Kabanets-Impagliazzo route.

## Summary

The PIT upgrade lemma is blocked: the current artifacts still provide only semantic black-box PIT objects, not a local theorem converting them into the algorithmic derandomization premise required by the target theorem.

## Informal Proof Or Disproof

# Proof Attempt: attempt.p-vs-np.022

- Queue ID: proofq.p-vs-np.017
- Status: blocked
- Conjecture: Prove an upgrade theorem turning the semantic black-box PIT object behind `PIT certificate family` into an algorithmic PIT-derandomization premise strong enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Bridge: bridge.013
- Source statement: st.def.hitting-set-for-pit-black-box
- Target statement: st.thm.kabanets-impagliazzo-pit-derandomisation-implies

## Local Grounding

- Source excerpt: A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by some circuit in mathcal C , there exists mathbf a in H with p(mathbf a )neq 0.
- Target excerpt: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.

## Queue Context

- Candidate object: PIT certificate family
- Invariant: PIT semantic object
- Route synopsis: Move from `st.def.hitting-set-for-pit-black-box` on problem `PIT` in model `black-box-PIT` using `A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by...` toward `st.thm.kabanets-impagliazzo-pit-derandomisation-implies` in model `arithmetic-circuits` to obtain `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Route lemma under test: Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.

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

- Program ID: attempt.p-vs-np.022
- Kind: proof-attempt
- Stage: prove
- Target: Prove an upgrade theorem turning the semantic black-box PIT object behind `PIT certificate family` into an algorithmic PIT-derandomization premise strong enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Nexus: Move from `st.def.hitting-set-for-pit-black-box` on problem `PIT` in model `black-box-PIT` using `A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by...` toward `st.thm.kabanets-impagliazzo-pit-derandomisation-implies` in model `arithmetic-circuits` to obtain `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Bridge object: PIT certificate family (checkable certificate map or algebraic witness relation)
- Positive route: Prove an upgrade theorem turning the semantic black-box PIT object behind `PIT certificate family` into an algorithmic PIT-derandomization premise strong enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Negative route: The alleged upgrade theorem may merely restate the semantic certificate object without producing a derandomization algorithm.

Anchors:
- source-theorem: st.def.hitting-set-for-pit-black-box | A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by some circuit in mathcal C , there exists mathbf a in H with p(mathbf a )neq 0.
- target-theorem: st.thm.kabanets-impagliazzo-pit-derandomisation-implies | If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.

Tensions:
- Route lemma under test: Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Missing route lemma: Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- The PIT upgrade lemma is blocked: the current artifacts still provide only semantic black-box PIT objects, not a local theorem converting them into the algorithmic derandomization premise required by the target theorem.

Proof debt:
- State `PIT Upgrade Lemma` on the theorem pair `st.def.hitting-set-for-pit-black-box` -> `st.thm.kabanets-impagliazzo-pit-derandomisation-implies`.
- Show why the blocked route summary `The PIT certificate-family repair is blocked: the stronger carrier clarifies the desired algebraic witness, but the current artifacts still do not upgrade a semantic black-box hitting-set object into the algorithmic PIT-derandomization premise used by the target theorem.` reduces to this lemma rather than to a broader bridge search.
- Either prove the lemma locally or explain why the local artifact stack still cannot realize it.
- The route is blocked at the semantic-to-algorithmic upgrade from hitting sets or certificates to derandomization.
- No local PIT certificate-family theorem upgrades black-box hitting sets into the PIT-derandomization premise of the Kabanets-Impagliazzo route.
- Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.

Decision gates:
- Web search gate: not-needed-local-obstruction -> The missing lemma is already locally identified; browsing is not yet decisive until the framework asks whether such a theorem exists in prior art.
- Negative-route heuristic:  -> Choose whether to continue constructive work, run a parallel negative branch, or switch to impossibility-first.
- Final assessment: blocked -> The PIT upgrade lemma is blocked: the current artifacts still provide only semantic black-box PIT objects, not a local theorem converting them into the algorithmic derandomization premise required by the target theorem.

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

- Theorem statement: Prove an upgrade theorem turning the semantic black-box PIT object behind `PIT certificate family` into an algorithmic PIT-derandomization premise strong enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Route lemma under test: Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
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

- Step 1: The repair lemma correctly isolates the missing theorem as an upgrade from a semantic black-box PIT object to an algorithmic derandomization premise.
  Justification: This is exactly the gap left after the certificate-family route was blocked.
  Depends on: proofq.p-vs-np.016, proofq.p-vs-np.017
- Step 2: No local result proves that the certificate-family object yields a deterministic PIT algorithm or an equivalent premise of the target theorem.
  Justification: The local artifact stack still stops at semantic witness structure rather than algorithmic derandomization.
  Depends on: proofq.p-vs-np.017
- Step 3: Therefore the repair lemma itself is blocked in the current local state.
  Justification: The route still needs a semantic-to-algorithmic upgrade theorem that is not yet present.
  Depends on: proofq.p-vs-np.016, proofq.p-vs-np.017

Negative-route analysis:

- Obstruction candidate: The alleged upgrade theorem may merely restate the semantic certificate object without producing a derandomization algorithm.
- Negated claim: 
- Contradiction target: 
- Forbidden outcome: 
- Counterexample or barrier: No local theorem turns the black-box certificate structure into the target algorithmic premise.
- Impossibility claim: 
- Effect on claim: The route remains blocked at the PIT upgrade step.

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
- No local upgrade theorem turns the PIT certificate-family object into the PIT-derandomization premise used by the Kabanets-Impagliazzo route.

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
- The route is blocked by the absence of a semantic-to-algorithmic PIT upgrade theorem.

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
- Novelty assessment: This pass confirms that the missing object is not another PIT carrier but the upgrade theorem itself.
- Confidence: high
- Result statement: No local upgrade theorem turns the PIT certificate-family object into the PIT-derandomization premise used by the Kabanets-Impagliazzo route.
- Result summary: The PIT upgrade lemma is blocked: the current artifacts still provide only semantic black-box PIT objects, not a local theorem converting them into the algorithmic derandomization premise required by the target theorem.

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
