<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Schema-To-Examples Construction Lemma: NP-complete under polynomial-time many-one reductions

- Result ID: mathlib.p-vs-np.blocked.proofq-p-vs-np-022
- Outcome: blocked
- KB ref: p-vs-np
- Queue ID: proofq.p-vs-np.022
- Attempt ID: attempt.p-vs-np.027
- Bridge ID: bridge.012
- Source statement: st.def.np-completeness
- Target statement: st.thm.karp-many-natural-problems-are-np-complete-karp1
- Web search used: False
- Entry kind: negative-local-theorem

## Statement

No local construction theorem derives natural NP-complete examples from the abstract NP-completeness schema.

## Summary

The schema-to-examples construction lemma is blocked: the current artifacts still do not construct concrete natural NP-complete examples from the abstract NP-completeness definition.

## Informal Proof Or Disproof

# Proof Attempt: attempt.p-vs-np.027

- Queue ID: proofq.p-vs-np.022
- Status: blocked
- Conjecture: Construct a reduction family that turns the abstract schema `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` into concrete natural examples realizing `NP-complete under polynomial-time many-one reductions`.
- Bridge: bridge.012
- Source statement: st.def.np-completeness
- Target statement: st.thm.karp-many-natural-problems-are-np-complete-karp1

## Local Grounding

- Source excerpt: A language L is emph NP-complete (under le_m^p ) iff (i) LinNP and (ii) for every AinNP , Ale_m^p L.
- Target excerpt: There exist many problems L in combinatorial optimisation/graph theory such that L is NP-complete under polynomial-time many-one reductions.

## Queue Context

- Candidate object: unspecified reduction gadget family
- Invariant: consequence schema NP-complete-classification
- Route synopsis: Move from `st.def.np-completeness` using `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` toward `st.thm.karp-many-natural-problems-are-np-complete-karp1` to obtain `NP-complete under polynomial-time many-one reductions`.
- Route lemma under test: Prove that a witness-preserving transport map turns `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` into `NP-complete under polynomial-time many-one reductions` while preserving `consequence schema NP-complete-classification`.

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

- Program ID: attempt.p-vs-np.027
- Kind: proof-attempt
- Stage: prove
- Target: Construct a reduction family that turns the abstract schema `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` into concrete natural examples realizing `NP-complete under polynomial-time many-one reductions`.
- Nexus: Move from `st.def.np-completeness` using `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` toward `st.thm.karp-many-natural-problems-are-np-complete-karp1` to obtain `NP-complete under polynomial-time many-one reductions`.
- Bridge object: unspecified reduction gadget family (family of reductions preserving the route witness structure)
- Positive route: Construct a reduction family that turns the abstract schema `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` into concrete natural examples realizing `NP-complete under polynomial-time many-one reductions`.
- Negative route: The construction lemma may simply restate the definition and target theorem without building any examples.

Anchors:
- source-theorem: st.def.np-completeness | A language L is emph NP-complete (under le_m^p ) iff (i) LinNP and (ii) for every AinNP , Ale_m^p L.
- target-theorem: st.thm.karp-many-natural-problems-are-np-complete-karp1 | There exist many problems L in combinatorial optimisation/graph theory such that L is NP-complete under polynomial-time many-one reductions.

Tensions:
- Route lemma under test: Prove that a witness-preserving transport map turns `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` into `NP-complete under polynomial-time many-one reductions` while preserving `consequence schema NP-complete-classification`.
- Missing route lemma: Prove that a witness-preserving transport map turns `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` into `NP-complete under polynomial-time many-one reductions` while preserving `consequence schema NP-complete-classification`.
- The schema-to-examples construction lemma is blocked: the current artifacts still do not construct concrete natural NP-complete examples from the abstract NP-completeness definition.

Proof debt:
- State `Schema-To-Examples Construction Lemma` on the theorem pair `st.def.np-completeness` -> `st.thm.karp-many-natural-problems-are-np-complete-karp1`.
- Show why the blocked route summary `The reduction-gadget repair for bridge.012 is blocked: the stronger carrier identifies the kind of construction needed, but the current artifacts still do not turn the abstract NP-completeness definition into concrete natural NP-complete examples.` reduces to this lemma rather than to a broader bridge search.
- Either prove the lemma locally or explain why the local artifact stack still cannot realize it.
- The route is blocked by a constructive gap from abstract schema to explicit natural examples.
- No local reduction-gadget family derives natural NP-complete examples from the abstract NP-completeness schema.
- Prove that a witness-preserving transport map turns `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` into `NP-complete under polynomial-time many-one reductions` while preserving `consequence schema NP-complete-classification`.

Decision gates:
- Web search gate: not-needed-local-obstruction -> The missing lemma is already locally identified; browsing is not yet decisive until the framework asks whether such a theorem exists in prior art.
- Negative-route heuristic:  -> Choose whether to continue constructive work, run a parallel negative branch, or switch to impossibility-first.
- Final assessment: blocked -> The schema-to-examples construction lemma is blocked: the current artifacts still do not construct concrete natural NP-complete examples from the abstract NP-completeness definition.

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

- Theorem statement: Construct a reduction family that turns the abstract schema `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` into concrete natural examples realizing `NP-complete under polynomial-time many-one reductions`.
- Route lemma under test: Prove that a witness-preserving transport map turns `A language L is emph NP-complete (under le_m^p ) iff (i) LinNP` into `NP-complete under polynomial-time many-one reductions` while preserving `consequence schema NP-complete-classification`.
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

- Step 1: The repair lemma narrows bridge.012 to the missing construction from abstract completeness schema to concrete natural examples.
  Justification: This is the theorem-sized version of the earlier definition-to-existence obstruction.
  Depends on: proofq.p-vs-np.015, proofq.p-vs-np.022
- Step 2: No local result performs that construction or identifies the concrete natural problem families witnessing the target theorem.
  Justification: The source remains schematic while the target is existential and example-based.
  Depends on: proofq.p-vs-np.022
- Step 3: Therefore the construction lemma is blocked in the current local state.
  Justification: The route still lacks the concrete theorem producing natural NP-complete instances.
  Depends on: proofq.p-vs-np.015, proofq.p-vs-np.022

Negative-route analysis:

- Obstruction candidate: The construction lemma may simply restate the definition and target theorem without building any examples.
- Negated claim: 
- Contradiction target: 
- Forbidden outcome: 
- Counterexample or barrier: The local artifacts contain no explicit example-producing reduction family.
- Impossibility claim: 
- Effect on claim: The route remains blocked at schema-to-examples construction.

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
- No local construction theorem derives natural NP-complete examples from the abstract NP-completeness schema.

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
- The route is blocked by the absence of an explicit construction of natural NP-complete examples.

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
- Novelty assessment: The route is now localized to one constructive theorem rather than a generic completeness gap.
- Confidence: high
- Result statement: No local construction theorem derives natural NP-complete examples from the abstract NP-completeness schema.
- Result summary: The schema-to-examples construction lemma is blocked: the current artifacts still do not construct concrete natural NP-complete examples from the abstract NP-completeness definition.

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
