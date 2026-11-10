# Proof Attempt: attempt.p-vs-np.009

- Queue ID: proofq.p-vs-np.004
- Status: blocked
- Conjecture: There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever NP-complete under polynomial-time many-one reductions holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification from the source regime to MCSP and yields is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various... for MCSP.
- Bridge: bridge.007
- Source statement: st.thm.karp-many-natural-problems-are-np-complete-karp1
- Target statement: st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo

## Prompt / Inference Diagnosis

- Context status: ill-posed
- Inference status: underdetermined
- Blocking defects: `claim_text` contains truncation markers, so the theorem state is not self-contained. | `conjecture_statement` contains truncation markers, so the theorem state is not self-contained. | `route_synopsis` contains truncation markers, so the theorem state is not self-contained.
- Minimal repair: Replace truncated theorem or route text with the full local statement.
- Certainty now: very-low
- Certainty if well posed: medium
- Rationale: The dossier still has context defects, so any route verdict should be treated mainly as packet diagnosis rather than stable mathematical evidence.

## Local Grounding

- Source excerpt: There exist many problems L in combinatorial optimisation/graph theory such that L is NP-complete under polynomial-time many-one reductions.
- Target excerpt: Under"local"polynomial-time reductions (where each output bit is computable with very small time), MCSP is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various reductions would entail unexpected class separations.

## Queue Context

- Candidate object: unspecified witness family
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

- Program ID: attempt.p-vs-np.009
- Kind: proof-attempt
- Stage: prove
- Target: There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever NP-complete under polynomial-time many-one reductions holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification from the source regime to MCSP and yields is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various... for MCSP.
- Nexus: Move from `st.thm.karp-many-natural-problems-are-np-complete-karp1` using `NP-complete under polynomial-time many-one reductions` toward `st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo` on problem `MCSP` to obtain `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...`.
- Bridge object: unspecified witness family (family of instances equipped with a monotone witness measure)
- Positive route: There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever NP-complete under polynomial-time many-one reductions holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification from the source regime to MCSP and yields is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various... for MCSP.
- Negative route: Allow the route to preserve only the generic fact that many problems are NP-complete, while leaving the local-reduction structure to MCSP implicit.

Anchors:
- source-theorem: st.thm.karp-many-natural-problems-are-np-complete-karp1 | There exist many problems L in combinatorial optimisation/graph theory such that L is NP-complete under polynomial-time many-one reductions.
- target-theorem: st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo | Under"local"polynomial-time reductions (where each output bit is computable with very small time), MCSP is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various reductions would entail unexpected class separations.

Tensions:
- Route lemma under test: Prove that a hardness-magnification witness family turns `NP-complete under polynomial-time many-one reductions` into `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...` while preserving `consequence schema NP-complete-classification`.
- Missing route lemma: Prove that a hardness-magnification witness family turns `NP-complete under polynomial-time many-one reductions` into `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...` while preserving `consequence schema NP-complete-classification`.
- The attempt isolates a reduction-regime obstruction: the source theorem is about ordinary NP-completeness, while the target theorem is about MCSP under local reductions, and the route never constructs the local transfer law needed to connect them.

Proof debt:
- Prove the source-to-object claim: the source-side content `NP-complete under polynomial-time many-one reductions` available at `st.thm.karp-many-natural-problems-are-np-complete-karp1` can be organized into `unspecified witness family` as a family of instances equipped with a monotone witness measure.
- Prove the payoff claim: once `unspecified witness family` carries the route data from `NP-complete under polynomial-time many-one reductions` toward `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...`, it forces `MCSP-hardness-transfer` at `st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo`.
- Prove the transport claim: every admissible realization of `unspecified witness family` preserves `consequence schema NP-complete-classification` while crossing the route model shift not yet typed.
- Construct the transfer-law claim: an explicit reduction or transport map sends `NP-complete under polynomial-time many-one reductions` into `unspecified witness family` without losing the route to `MCSP-hardness-transfer`.
- Show that every admissible realization of `unspecified witness family` preserves `consequence schema NP-complete-classification` across model shift not yet typed.
- Source-to-object lemma: the source-side content `NP-complete under polynomial-time many-one reductions` at `st.thm.karp-many-natural-problems-are-np-complete-karp1` yields a realization of `unspecified witness family` as a family of instances equipped with a monotone witness measure, satisfying admits source-side witness data for `NP-complete under polynomial-time many-one reductions`; preserves the route invariant `consequence schema NP-complete-classification`; provides an explicit transfer law or reduction mechanism on the route.
- Transport lemma: every admissible realization of `unspecified witness family` preserves `consequence schema NP-complete-classification` while crossing model shift not yet typed.
- Payoff lemma: if `unspecified witness family` is realized, carries `consequence schema NP-complete-classification`, and discharges the route-specific step from `NP-complete under polynomial-time many-one reductions` to `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...`, then `MCSP-hardness-transfer` holds at `st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo`.
- Reduction lemma: the source-side content `NP-complete under polynomial-time many-one reductions` reduces to the surrogate object encoded by `unspecified witness family` without weakening the path to `MCSP-hardness-transfer`.
- Prove that a hardness-magnification witness family turns `NP-complete under polynomial-time many-one reductions` into `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...` while preserving `consequence schema NP-complete-classification`.

Decision gates:
- Web search gate: not-evaluated -> Default stance: do not browse until a decisive local gap or prior-art uncertainty is identified.
- Negative-route heuristic:  -> Choose whether to continue constructive work, run a parallel negative branch, or switch to impossibility-first.
- Final assessment: blocked -> The attempt isolates a reduction-regime obstruction: the source theorem is about ordinary NP-completeness, while the target theorem is about MCSP under local reductions, and the route never constructs the local transfer law needed to connect them.

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

- Theorem statement: There exists an admissible unspecified witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever NP-complete under polynomial-time many-one reductions holds for the source regime, the object organizes the source-side mathematical content while preserving the invariant consequence schema NP-complete-classification from the source regime to MCSP and yields is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various... for MCSP.
- Route lemma under test: Prove that a hardness-magnification witness family turns `NP-complete under polynomial-time many-one reductions` into `is not NP-complete. More broadly, the paper develops evidence and conditional consequences suggesting NP-hardness of MCSP under various...` while preserving `consequence schema NP-complete-classification`.
- Strategy family: surrogate-reduction-transfer

### Informal Tactic Playbook

- No tactic playbook recorded.

### Informal Tactic Trace

- No tactic trace recorded.

### Negative-Route Heuristic

- No negative-route heuristic recorded.

### Contradiction / Impossibility Frame

- No contradiction frame recorded.

Stepwise argument:

- Step 1: The source theorem only says that many natural problems are NP-complete under ordinary polynomial-time many-one reductions; it does not isolate MCSP, local reductions, or any route-specific transfer into MCSP.
  Justification: The source statement is a broad classification theorem about many NP-complete problems. The target theorem, by contrast, is specifically about MCSP and a restricted reduction notion.
  Depends on: st.thm.karp-many-natural-problems-are-np-complete-karp1, bridge.007
- Step 2: The target route is under-typed exactly where the theorem becomes delicate: the route state leaves the model shift unspecified even though the target theorem is about local reductions to MCSP.
  Justification: Both the queue dossier and the search-space state record `model shift not yet typed`, while the target excerpt explicitly hinges on a local-reduction restriction. Without typing that shift, the route does not preserve the decisive mathematical condition.
  Depends on: bridge.007, search-space-tree, st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo
- Step 3: No local route fixes a coherent carrier or transfer law: the artifacts alternate between `unspecified witness family` and `unspecified reduction gadget family`, but neither is realized as a family of local reductions into MCSP.
  Justification: The proof sketches give two live operationalizations for the same route, both still unspecified at the mathematical level. Neither produces a theorem that translates generic NP-complete classification into the local-reduction regime of the target theorem.
  Depends on: psk.004, psk.006, expert-hypothesis-paper:bridge.007
- Step 4: Because the route never constructs or analyzes the required local reduction family, it cannot derive the target negative result that MCSP is not NP-complete under local reductions.
  Justification: The target theorem is not a generic hardness-transfer payoff. It is a restriction theorem about a specific reduction class. The current dossier has no local theorem showing that the source NP-complete classification enters that restricted regime.
  Depends on: st.thm.karp-many-natural-problems-are-np-complete-karp1, st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo, bridge.007
- Step 5: The correct verdict is `blocked`: the route fails before any MCSP-specific local-reduction argument is built, so the proposed bridge remains only topical rather than mathematical.
  Justification: A positive result would require an explicit local reduction family or an explicit barrier theorem showing why such reductions fail. Neither ingredient is present in the local artifacts.
  Depends on: psk.004, psk.006, bridge.007

Negative-route analysis:

- Obstruction candidate: Allow the route to preserve only the generic fact that many problems are NP-complete, while leaving the local-reduction structure to MCSP implicit.
- Negated claim: 
- Contradiction target: 
- Forbidden outcome: 
- Counterexample or barrier: The local barrier is a reduction-regime mismatch: ordinary polynomial-time many-one reductions do not automatically yield the local reductions analyzed in the Murray-Williams theorem. The carrier can therefore preserve generic NP-complete flavor while never entering the target theorem?s restricted reduction regime.
- Impossibility claim: 
- Effect on claim: The route is blocked. Progress would require a concrete local reduction family into MCSP or a theorem translating ordinary NP-complete classification into the target local-reduction setting.

## Critique Judges

### Statement Grounding Judge

- Is the claim under test stated explicitly and does it match the queue item?
- Are source and target statements grounded in local KB statement ids or InformalMathLib entries?
- Does each proof step say what prior local statement or earlier step it depends on?

Verdict: pass
Notes:
- The queue conjecture, source theorem, and target theorem are explicitly grounded in local artifact ids.
- The blocked diagnosis points to the typed gap at the reduction regime rather than to generic lack of detail.

### Inferential Validity Judge

- Does each step follow informally from its stated dependencies?
- Are quantifiers, regimes, and model shifts preserved rather than silently changed?
- Is the conclusion exactly the claimed result rather than a nearby weaker statement?

Verdict: fail
Notes:
- The recorded argument supports a blocked verdict, not a proof verdict.
- The failure occurs before any local-reduction route into MCSP is established.
Blocking issues:
- No local step derives the local-reduction restriction from the broad NP-complete source theorem.
- No local step proves that either live carrier produces the target MCSP theorem.

### Assumption Discipline Judge

- Did the proof introduce any hidden assumptions not already declared?
- Are all uses of prior lemmas, barriers, and transfer claims explicit?
- If an extra assumption is necessary, is the outcome downgraded to a conditional result?

Verdict: pass
Notes:
- The blocked verdict does not smuggle in a hidden identification between ordinary many-one reductions and local reductions.
- The missing transfer law is made explicit instead of being assumed.

### Prior-Art And Novelty Judge

- Can the result already be recovered from local InformalMathLib or KB material?
- If not locally, is a web search required by the search policy before claiming novelty?
- If prior art exists, should the outcome be reclassified as reconstruction or prior_art_found?

Verdict: pass
Notes:
- No theorem-level novelty is being claimed; this is a route-level obstruction diagnosis.
- Web search is not triggered because the local source and target theorems already suffice to identify the regime mismatch.

### Obstruction And Negative-Route Judge

- Does the current argument survive the designated negative route or obstruction check?
- Is there a counterexample, barrier, or failure mode that blocks the route?
- If the route fails, is the negative result itself clearly formulated?

Verdict: fail
Notes:
- The negative route succeeds because topical NP-complete structure is weaker than the local-reduction structure required by the target theorem.
- The route remains blocked until the reduction regime is typed and realized.
Blocking issues:
- The model shift is still recorded as `model shift not yet typed`.
- Neither `unspecified witness family` nor `unspecified reduction gadget family` is realized as a local reduction family into MCSP.

### Closure Judge

- Is the final outcome correctly classified as proved, disproved, blocked, deferred, or prior_art_found?
- Does the written proof or disproof support that classification?
- Is the result statement ready to persist into InformalMathLib if the outcome is terminal?

Verdict: pass
Notes:
- Given the failed inferential and obstruction checks, `blocked` is the correct terminal classification.
- The restart condition is explicit: build a typed local reduction mechanism or prove an explicit barrier theorem for that regime.

## Final Assessment

- Outcome: blocked
- Verdict: blocked
- Novelty assessment: No theorem-level novelty is claimed. The value of this attempt is the sharper localization of the reduction-regime mismatch for the MCSP non-NP-completeness route.
- Confidence: high
- Result statement: Blocked result: the current `bridge.007` dossier does not prove the route from generic NP-complete classification to the Murray-Williams local-reduction theorem for MCSP, because no local theorem types the reduction regime and no local carrier realizes an explicit family of local reductions or an equivalent barrier argument.
- Result summary: The attempt isolates a reduction-regime obstruction: the source theorem is about ordinary NP-completeness, while the target theorem is about MCSP under local reductions, and the route never constructs the local transfer law needed to connect them.

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
- Overall judgment: Useful reduction-regime obstruction diagnosis, but not yet a theorem-level subresult.
