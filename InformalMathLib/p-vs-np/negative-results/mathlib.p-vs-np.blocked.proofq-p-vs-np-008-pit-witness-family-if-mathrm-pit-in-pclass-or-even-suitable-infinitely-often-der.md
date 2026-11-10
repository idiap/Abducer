<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# PIT witness family: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...

- Result ID: mathlib.p-vs-np.blocked.proofq-p-vs-np-008
- Outcome: blocked
- KB ref: p-vs-np
- Queue ID: proofq.p-vs-np.008
- Attempt ID: attempt.p-vs-np.013
- Bridge ID: bridge.013
- Source statement: st.def.hitting-set-for-pit-black-box
- Target statement: st.thm.kabanets-impagliazzo-pit-derandomisation-implies
- Web search used: False
- Entry kind: negative-local-theorem

## Statement

Blocked result: the current `bridge.013` dossier does not prove a route from the black-box hitting-set definition to the Kabanets-Impagliazzo derandomization theorem, because no local theorem upgrades the semantic hitting-set notion into the algorithmic PIT premise needed for the target lower-bound consequence.

## Summary

The attempt isolates a definition-to-derandomization obstruction: the source is only a black-box hitting-set definition, while the target theorem assumes a much stronger PIT-derandomization condition, and the current bridge never supplies that upgrade.

## Informal Proof Or Disproof

# Proof Attempt: attempt.p-vs-np.013

- Queue ID: proofq.p-vs-np.008
- Status: blocked
- Conjecture: There exists an admissible PIT witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by... holds for PIT in black-box-PIT, the object organizes the source-side mathematical content while preserving the invariant PIT semantic object across the transfer black-box-PIT -> arithmetic-circuits and yields If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard... for PIT in arithmetic-circuits.
- Bridge: bridge.013
- Source statement: st.def.hitting-set-for-pit-black-box
- Target statement: st.thm.kabanets-impagliazzo-pit-derandomisation-implies

## Local Grounding

- Source excerpt: A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by some circuit in mathcal C , there exists mathbf a in H with p(mathbf a )neq 0.
- Target excerpt: If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.

## Queue Context

- Candidate object: PIT witness family
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

- Program ID: attempt.p-vs-np.013
- Kind: proof-attempt
- Stage: prove
- Target: There exists an admissible PIT witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by... holds for PIT in black-box-PIT, the object organizes the source-side mathematical content while preserving the invariant PIT semantic object across the transfer black-box-PIT -> arithmetic-circuits and yields If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard... for PIT in arithmetic-circuits.
- Nexus: Move from `st.def.hitting-set-for-pit-black-box` on problem `PIT` in model `black-box-PIT` using `A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by...` toward `st.thm.kabanets-impagliazzo-pit-derandomisation-implies` in model `arithmetic-circuits` to obtain `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Bridge object: PIT witness family (family of instances equipped with a monotone witness measure)
- Positive route: There exists an admissible PIT witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by... holds for PIT in black-box-PIT, the object organizes the source-side mathematical content while preserving the invariant PIT semantic object across the transfer black-box-PIT -> arithmetic-circuits and yields If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard... for PIT in arithmetic-circuits.
- Negative route: Allow the route to preserve only the semantic black-box hitting-set notion while leaving the algorithmic PIT-derandomization premise implicit.

Anchors:
- source-theorem: st.def.hitting-set-for-pit-black-box | A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by some circuit in mathcal C , there exists mathbf a in H with p(mathbf a )neq 0.
- target-theorem: st.thm.kabanets-impagliazzo-pit-derandomisation-implies | If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard variants), then at least one of the following holds: NEXP not in P/poly quad or quad Permanent does not have polynomial-size arithmetic circuits.

Tensions:
- Route lemma under test: Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Missing route lemma: Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- The attempt isolates a definition-to-derandomization obstruction: the source is only a black-box hitting-set definition, while the target theorem assumes a much stronger PIT-derandomization condition, and the current bridge never supplies that upgrade.

Proof debt:
- Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.

Decision gates:
- Web search gate: not-evaluated -> Default stance: do not browse until a decisive local gap or prior-art uncertainty is identified.
- Negative-route heuristic:  -> Choose whether to continue constructive work, run a parallel negative branch, or switch to impossibility-first.
- Final assessment: blocked -> The attempt isolates a definition-to-derandomization obstruction: the source is only a black-box hitting-set definition, while the target theorem assumes a much stronger PIT-derandomization condition, and the current bridge never supplies that upgrade.

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

- Theorem statement: There exists an admissible PIT witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A set Hsubseteq mathbb F ^n is a hitting set for a class mathcal C of n -variate circuits if for every nonzero polynomial p computed by... holds for PIT in black-box-PIT, the object organizes the source-side mathematical content while preserving the invariant PIT semantic object across the transfer black-box-PIT -> arithmetic-circuits and yields If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard... for PIT in arithmetic-circuits.
- Route lemma under test: Prove that a hitting-set or pseudorandom-generator family preserves `PIT semantic object` while transporting the route from the black-box-PIT regime to the arithmetic-circuits regime strongly enough to derive `If mathrm PIT in Pclass (or even suitable infinitely-often derandomisations in nondeterministic subexponential time, in standard...`.
- Strategy family: 

### Informal Tactic Playbook

- No tactic playbook recorded.

### Informal Tactic Trace

- No tactic trace recorded.

### Negative-Route Heuristic

- No negative-route heuristic recorded.

### Contradiction / Impossibility Frame

- No contradiction frame recorded.

Stepwise argument:

- Step 1: The source statement is only the definition of a hitting set for black-box PIT; it does not assert that such hitting sets are computable efficiently, uniform, or strong enough to derandomize PIT.
  Justification: The source excerpt defines what a hitting set is for a circuit class. It does not yet provide a polynomial-time PIT algorithm or any complexity-theoretic consequence.
  Depends on: st.def.hitting-set-for-pit-black-box, bridge.013
- Step 2: The target theorem is an implication from a much stronger algorithmic premise, namely a PIT derandomization hypothesis, to major lower-bound consequences such as `NEXP not in P/poly` or arithmetic lower bounds for Permanent.
  Justification: The target excerpt is not a restatement of the hitting-set definition. It requires an algorithmic PIT assumption and then derives hardness consequences in stronger models.
  Depends on: st.thm.kabanets-impagliazzo-pit-derandomisation-implies, bridge.013
- Step 3: The proposed `PIT witness family` never becomes a theorem supplying that algorithmic premise: no local carrier theorem turns the existence or definition of a black-box hitting set into PIT in P or an equivalent derandomization claim.
  Justification: The route keeps the carrier and transport abstract. No local source-to-object or payoff lemma upgrades from the semantic notion of a hitting set to the algorithmic derandomization premise named in the target theorem.
  Depends on: bridge-plan:bridge.013, search-space-tree
- Step 4: Because the route never proves the derandomization premise, it cannot reach the target lower-bound disjunction.
  Justification: The Kabanets-Impagliazzo theorem is conditional on PIT derandomization. Without a theorem producing that condition from the black-box hitting-set definition, the target consequence is not locally justified.
  Depends on: st.def.hitting-set-for-pit-black-box, st.thm.kabanets-impagliazzo-pit-derandomisation-implies, bridge.013
- Step 5: The correct verdict is `blocked`: the route fails at the definition-to-derandomization step because it never upgrades the black-box hitting-set notion into the algorithmic PIT premise required by the target theorem.
  Justification: A positive result would require an explicit theorem converting the semantic hitting-set object into an efficient PIT procedure or an equivalent pseudorandom-generator/derandomization statement. No such theorem is present locally.
  Depends on: bridge.013, st.def.hitting-set-for-pit-black-box, st.thm.kabanets-impagliazzo-pit-derandomisation-implies

Negative-route analysis:

- Obstruction candidate: Allow the route to preserve only the semantic black-box hitting-set notion while leaving the algorithmic PIT-derandomization premise implicit.
- Negated claim: 
- Contradiction target: 
- Forbidden outcome: 
- Counterexample or barrier: The local barrier is a definition-to-derandomization gap: a hitting set can exist as a semantic object without yielding a polynomial-time PIT algorithm. The carrier can therefore preserve PIT-flavored structure while never entering the stronger algorithmic regime demanded by the target theorem.
- Impossibility claim: 
- Effect on claim: The route is blocked. Progress would require an explicit theorem converting the hitting-set notion into an efficient PIT procedure or a precise derandomization surrogate strong enough for the Kabanets-Impagliazzo consequence.

## Critique Judges

### Statement Grounding Judge

- Is the claim under test stated explicitly and does it match the queue item?
- Are source and target statements grounded in local KB statement ids or InformalMathLib entries?
- Does each proof step say what prior local statement or earlier step it depends on?

Verdict: pass
Notes:
- The queue conjecture, source definition, and Kabanets-Impagliazzo target theorem are explicitly grounded in local KB ids.
- The blocked diagnosis points to the missing upgrade from semantic hitting set to algorithmic PIT premise.

### Inferential Validity Judge

- Does each step follow informally from its stated dependencies?
- Are quantifiers, regimes, and model shifts preserved rather than silently changed?
- Is the conclusion exactly the claimed result rather than a nearby weaker statement?

Verdict: fail
Notes:
- The recorded argument supports a blocked verdict, not a proof verdict.
- The failure occurs before any algorithmic PIT derandomization statement is established.
Blocking issues:
- No local step derives PIT in P or an equivalent derandomization claim from the hitting-set definition.
- No local step derives the target lower-bound disjunction from the current carrier.

### Assumption Discipline Judge

- Did the proof introduce any hidden assumptions not already declared?
- Are all uses of prior lemmas, barriers, and transfer claims explicit?
- If an extra assumption is necessary, is the outcome downgraded to a conditional result?

Verdict: pass
Notes:
- The blocked verdict does not assume that a semantic hitting set already yields an efficient PIT algorithm.
- The missing derandomization upgrade is made explicit rather than hidden.

### Prior-Art And Novelty Judge

- Can the result already be recovered from local InformalMathLib or KB material?
- If not locally, is a web search required by the search policy before claiming novelty?
- If prior art exists, should the outcome be reclassified as reconstruction or prior_art_found?

Verdict: pass
Notes:
- No theorem-level novelty is being claimed; this is a route-level obstruction diagnosis.
- Web search is not triggered because the source/target logical gap is already clear from the local KB statements.

### Obstruction And Negative-Route Judge

- Does the current argument survive the designated negative route or obstruction check?
- Is there a counterexample, barrier, or failure mode that blocks the route?
- If the route fails, is the negative result itself clearly formulated?

Verdict: fail
Notes:
- The negative route succeeds because semantic PIT objects are weaker than the algorithmic derandomization premise of the target theorem.
- The carrier remains descriptive and never becomes theorem-forcing.
Blocking issues:
- The route does not produce an efficient PIT algorithm or equivalent derandomization statement.
- The carrier remains `PIT witness family` rather than a proved pseudorandom-generator or algorithmic hitting-set construction.

### Closure Judge

- Is the final outcome correctly classified as proved, disproved, blocked, deferred, or prior_art_found?
- Does the written proof or disproof support that classification?
- Is the result statement ready to persist into InformalMathLib if the outcome is terminal?

Verdict: pass
Notes:
- Given the failed inferential and obstruction checks, `blocked` is the correct terminal classification.
- The restart condition is explicit: add a theorem converting the semantic hitting-set notion into the target algorithmic premise.

## Final Assessment

- Outcome: blocked
- Verdict: blocked
- Novelty assessment: No theorem-level novelty is claimed. The value of this attempt is the sharper localization of the definition-to-derandomization gap.
- Confidence: high
- Result statement: Blocked result: the current `bridge.013` dossier does not prove a route from the black-box hitting-set definition to the Kabanets-Impagliazzo derandomization theorem, because no local theorem upgrades the semantic hitting-set notion into the algorithmic PIT premise needed for the target lower-bound consequence.
- Result summary: The attempt isolates a definition-to-derandomization obstruction: the source is only a black-box hitting-set definition, while the target theorem assumes a much stronger PIT-derandomization condition, and the current bridge never supplies that upgrade.

## Major Subresult Assessment

Use this only for terminal `proved` or `disproved` outcomes that might warrant a standalone paper in `artifacts/<kb-ref>/produced_papers`.

Mandatory gates:
- Self-contained statement: False
- Mathematical inspectability: True
- Nontrivial frontier relation: True
- Independent value: False

0-3 axis scores:
- Frontier shift: 1
- Independence: 0
- Transferability: 1
- Barrier clarity: 2
- Proof closure: 0
- Search compression: 2

Threshold rule: all mandatory gates pass, total score >= 11, and at least one of frontier shift / independence / barrier clarity is 3.

- Paper candidate title: 
- Paper candidate summary: 
- Overall judgment: Useful definition-to-derandomization obstruction diagnosis, but not yet a theorem-level subresult.
