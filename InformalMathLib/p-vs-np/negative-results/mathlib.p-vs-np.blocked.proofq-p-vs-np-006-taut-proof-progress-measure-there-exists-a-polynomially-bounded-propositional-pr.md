<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# TAUT proof progress measure: There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP

- Result ID: mathlib.p-vs-np.blocked.proofq-p-vs-np-006
- Outcome: blocked
- KB ref: p-vs-np
- Queue ID: proofq.p-vs-np.006
- Attempt ID: attempt.p-vs-np.011
- Bridge ID: bridge.003
- Source statement: st.def.cook-reckhow-propositional-proof-system
- Target statement: st.thm.cook-reckhow-proof-systems-and-cookreckhow1979
- Web search used: False
- Entry kind: negative-local-theorem

## Statement

Blocked result: the current `bridge.003` dossier does not prove the Cook-Reckhow characterization theorem through `TAUT proof progress measure`, because no local theorem connects the proposed monotone proof measure to polynomially bounded proof systems or to either direction of the equivalence with `NP = coNP`.

## Summary

The attempt isolates a characterization obstruction: the source statement is only definitional, while the target theorem is a biconditional class-collapse statement, and the proposed carrier does not bridge that gap locally.

## Informal Proof Or Disproof

# Proof Attempt: attempt.p-vs-np.011

- Queue ID: proofq.p-vs-np.006
- Status: blocked
- Conjecture: There exists an admissible TAUT proof progress measure, realized as a monotone potential function over proofs or certificates, such that whenever A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is... holds for TAUT in Cook-Reckhow-proof-system, the object organizes the source-side mathematical content while preserving the invariant TAUT complexity profile in Cook-Reckhow-proof-system and yields There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP.
- Bridge: bridge.003
- Source statement: st.def.cook-reckhow-propositional-proof-system
- Target statement: st.thm.cook-reckhow-proof-systems-and-cookreckhow1979

## Local Grounding

- Source excerpt: A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is the set of propositional tautologies. A string pi is an f -proof of formula varphi if f(pi)=varphi.
- Target excerpt: There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP.

## Queue Context

- Candidate object: TAUT proof progress measure
- Invariant: TAUT complexity profile in Cook-Reckhow-proof-system
- Route synopsis: Move from `st.def.cook-reckhow-propositional-proof-system` on problem `TAUT` in model `Cook-Reckhow-proof-system` using `A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is...` toward `st.thm.cook-reckhow-proof-systems-and-cookreckhow1979` in model `Cook-Reckhow-proof-system` to obtain `There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP`.
- Route lemma under test: Prove that a proof certificate family or monotone proof measure turns `A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is...` into `There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP` while preserving `TAUT complexity profile in Cook-Reckhow-proof-system`.

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

- Program ID: attempt.p-vs-np.011
- Kind: proof-attempt
- Stage: prove
- Target: There exists an admissible TAUT proof progress measure, realized as a monotone potential function over proofs or certificates, such that whenever A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is... holds for TAUT in Cook-Reckhow-proof-system, the object organizes the source-side mathematical content while preserving the invariant TAUT complexity profile in Cook-Reckhow-proof-system and yields There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP.
- Nexus: Move from `st.def.cook-reckhow-propositional-proof-system` on problem `TAUT` in model `Cook-Reckhow-proof-system` using `A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is...` toward `st.thm.cook-reckhow-proof-systems-and-cookreckhow1979` in model `Cook-Reckhow-proof-system` to obtain `There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP`.
- Bridge object: TAUT proof progress measure (monotone potential function over proofs or certificates)
- Positive route: There exists an admissible TAUT proof progress measure, realized as a monotone potential function over proofs or certificates, such that whenever A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is... holds for TAUT in Cook-Reckhow-proof-system, the object organizes the source-side mathematical content while preserving the invariant TAUT complexity profile in Cook-Reckhow-proof-system and yields There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP.
- Negative route: Allow `TAUT proof progress measure` to record only generic proof-system structure while leaving boundedness and the `NP = coNP` equivalence implicit.

Anchors:
- source-theorem: st.def.cook-reckhow-propositional-proof-system | A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is the set of propositional tautologies. A string pi is an f -proof of formula varphi if f(pi)=varphi.
- target-theorem: st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP.

Tensions:
- Route lemma under test: Prove that a proof certificate family or monotone proof measure turns `A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is...` into `There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP` while preserving `TAUT complexity profile in Cook-Reckhow-proof-system`.
- Missing route lemma: Prove that a proof certificate family or monotone proof measure turns `A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is...` into `There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP` while preserving `TAUT complexity profile in Cook-Reckhow-proof-system`.
- The attempt isolates a characterization obstruction: the source statement is only definitional, while the target theorem is a biconditional class-collapse statement, and the proposed carrier does not bridge that gap locally.

Proof debt:
- Prove that a proof certificate family or monotone proof measure turns `A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is...` into `There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP` while preserving `TAUT complexity profile in Cook-Reckhow-proof-system`.

Decision gates:
- Web search gate: not-evaluated -> Default stance: do not browse until a decisive local gap or prior-art uncertainty is identified.
- Negative-route heuristic:  -> Choose whether to continue constructive work, run a parallel negative branch, or switch to impossibility-first.
- Final assessment: blocked -> The attempt isolates a characterization obstruction: the source statement is only definitional, while the target theorem is a biconditional class-collapse statement, and the proposed carrier does not bridge that gap locally.

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

- Theorem statement: There exists an admissible TAUT proof progress measure, realized as a monotone potential function over proofs or certificates, such that whenever A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is... holds for TAUT in Cook-Reckhow-proof-system, the object organizes the source-side mathematical content while preserving the invariant TAUT complexity profile in Cook-Reckhow-proof-system and yields There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP.
- Route lemma under test: Prove that a proof certificate family or monotone proof measure turns `A (Cook--Reckhow) propositional proof system is a polynomial-time computable surjection f:bits^*twoheadrightarrow TAUT, where TAUT is...` into `There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP` while preserving `TAUT complexity profile in Cook-Reckhow-proof-system`.
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

- Step 1: The source statement is only the definition of a Cook-Reckhow proof system, so it introduces proof objects but does not yet assert boundedness, simulation, or any complexity-class collapse.
  Justification: The source excerpt says that a proof system is a polynomial-time computable surjection onto TAUT. That is much weaker than the target biconditional characterization involving polynomial bounds and `NP = coNP`.
  Depends on: st.def.cook-reckhow-propositional-proof-system, bridge.003
- Step 2: The target theorem is stronger in two directions at once: it asserts an iff characterization and contains a complexity-class equality, neither of which is present in the source regime.
  Justification: To reach the target, the route would need at least a theorem connecting the existence of polynomially bounded proofs to `NP = coNP`, and another theorem explaining the converse direction. The current dossier does not decompose or prove either direction.
  Depends on: st.thm.cook-reckhow-proof-systems-and-cookreckhow1979, bridge.003
- Step 3: The candidate carrier `TAUT proof progress measure` is not locally grounded in any theorem showing that a monotone proof measure yields polynomially bounded proofs or a class-collapse argument.
  Justification: The bridge object is an added explanatory proposal, not a theorem from the local KB. No local source-to-object or payoff lemma turns this monotone potential into the target characterization theorem.
  Depends on: bridge-plan:bridge.003, expert-hypothesis-paper:bridge.003
- Step 4: Because the route never proves either direction of the biconditional, it cannot derive the target theorem even as an informal bridge explanation.
  Justification: The current route preserves only a generic TAUT complexity profile. It does not show how bounded proof size arises, nor how the existence of such a system forces `NP = coNP`.
  Depends on: st.def.cook-reckhow-propositional-proof-system, st.thm.cook-reckhow-proof-systems-and-cookreckhow1979, bridge.003
- Step 5: The correct verdict is `blocked`: the route is too weak to justify the Cook-Reckhow characterization theorem through the proposed carrier.
  Justification: A positive result would need explicit lemmas for the bounded-proof direction and the class-collapse direction, or a theorem connecting the proof-progress measure to both. Neither appears in the local artifacts.
  Depends on: bridge.003, st.thm.cook-reckhow-proof-systems-and-cookreckhow1979

Negative-route analysis:

- Obstruction candidate: Allow `TAUT proof progress measure` to record only generic proof-system structure while leaving boundedness and the `NP = coNP` equivalence implicit.
- Negated claim: 
- Contradiction target: 
- Forbidden outcome: 
- Counterexample or barrier: The local barrier is a characterization gap: a monotone proof measure may describe proof progress without yielding a polynomial bound or a complexity-class equality. The route can therefore preserve TAUT proof-system structure while failing to establish either direction of the Cook-Reckhow iff theorem.
- Impossibility claim: 
- Effect on claim: The route is blocked. Progress would require explicit lemmas deriving polynomial boundedness and the `NP = coNP` characterization from the chosen carrier, or a different route decomposition that treats the two theorem directions separately.

## Critique Judges

### Statement Grounding Judge

- Is the claim under test stated explicitly and does it match the queue item?
- Are source and target statements grounded in local KB statement ids or InformalMathLib entries?
- Does each proof step say what prior local statement or earlier step it depends on?

Verdict: pass
Notes:
- The queue conjecture, source definition, and target characterization theorem are explicitly grounded in local KB ids.
- The blocked diagnosis identifies the missing biconditional structure rather than a generic lack of detail.

### Inferential Validity Judge

- Does each step follow informally from its stated dependencies?
- Are quantifiers, regimes, and model shifts preserved rather than silently changed?
- Is the conclusion exactly the claimed result rather than a nearby weaker statement?

Verdict: fail
Notes:
- The recorded argument supports a blocked verdict, not a proof verdict.
- The failure occurs before either direction of the biconditional target theorem is established.
Blocking issues:
- No local step derives polynomial boundedness from the proposed proof-progress carrier.
- No local step derives or explains the `NP = coNP` direction of the characterization theorem.

### Assumption Discipline Judge

- Did the proof introduce any hidden assumptions not already declared?
- Are all uses of prior lemmas, barriers, and transfer claims explicit?
- If an extra assumption is necessary, is the outcome downgraded to a conditional result?

Verdict: pass
Notes:
- The blocked verdict does not assume that a generic Cook-Reckhow proof system is already polynomially bounded.
- The missing boundedness and class-collapse lemmas are made explicit instead of being hidden.

### Prior-Art And Novelty Judge

- Can the result already be recovered from local InformalMathLib or KB material?
- If not locally, is a web search required by the search policy before claiming novelty?
- If prior art exists, should the outcome be reclassified as reconstruction or prior_art_found?

Verdict: pass
Notes:
- The target theorem is already present in the local KB, but the current route-specific bridge explanation is not recovered from the local carrier.
- No web search is triggered because the relevant theorem and definitional gap are already local.

### Obstruction And Negative-Route Judge

- Does the current argument survive the designated negative route or obstruction check?
- Is there a counterexample, barrier, or failure mode that blocks the route?
- If the route fails, is the negative result itself clearly formulated?

Verdict: fail
Notes:
- The negative route succeeds because proof-progress structure is weaker than the polynomial boundedness and class-collapse content of the target theorem.
- The current carrier can remain descriptive without becoming theorem-forcing.
Blocking issues:
- No local theorem connects `TAUT proof progress measure` to a polynomially bounded proof system.
- No local theorem decomposes or proves the two directions of `There exists a polynomially bounded propositional proof system for TAUT if and only if NP=coNP`.

### Closure Judge

- Is the final outcome correctly classified as proved, disproved, blocked, deferred, or prior_art_found?
- Does the written proof or disproof support that classification?
- Is the result statement ready to persist into InformalMathLib if the outcome is terminal?

Verdict: pass
Notes:
- Given the failed inferential and obstruction checks, `blocked` is the correct terminal classification.
- The restart condition is explicit: either decompose the theorem into its two directions or supply a carrier that actually implies both.

## Final Assessment

- Outcome: blocked
- Verdict: blocked
- Novelty assessment: No theorem-level novelty is claimed. The value of this attempt is the clearer diagnosis that the current bridge object does not explain the Cook-Reckhow characterization theorem.
- Confidence: high
- Result statement: Blocked result: the current `bridge.003` dossier does not prove the Cook-Reckhow characterization theorem through `TAUT proof progress measure`, because no local theorem connects the proposed monotone proof measure to polynomially bounded proof systems or to either direction of the equivalence with `NP = coNP`.
- Result summary: The attempt isolates a characterization obstruction: the source statement is only definitional, while the target theorem is a biconditional class-collapse statement, and the proposed carrier does not bridge that gap locally.

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
- Overall judgment: Useful characterization-gap diagnosis, but not yet a theorem-level subresult.
