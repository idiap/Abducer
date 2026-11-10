<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Prompt Template


## Intent Gate

Use this prompt only when the task matches this skill contract:

Run the prove cycle over the persistent proof queue: consume one queued claim, attempt an informal proof or disproof, apply systematic critique judges, use web search only under a parsimonious gate, and persist terminal positive or negative results into a problem-scoped InformalMathLib plus a summary report.

Do not use it as a generic brainstorming prompt or as a substitute for an adjacent skill. Keep the scope tied to the specific claim, route, artifact set, or decision named in the input packet.

## Self-Contained Context Packet

Before solving, restate the context in a compact explicit packet:
- problem or kb_ref
- exact claim, route, object, or artifact under inspection
- exact input artifacts, IDs, excerpts, or paths in scope
- exact decision to make or artifact to produce
- constraints, evidence policy, and output format

If any required item is missing, say so explicitly and do not invent hidden context, broaden the task silently, or rely on repository background that is not named in the packet.

## Prompt-Diagnosis And Qualified Certainty Gate

When the task involves substantive inference rather than pure extraction, formatting, or rendering, run a short self-critical pre-pass:
- classify `context_status`: `well-posed` | `partially-ill-posed` | `ill-posed`
- classify `inference_status`: `determined` | `underdetermined` | `difficult-but-well-posed`
- list the exact blocking context or prompt defects if the packet is not well behaved
- state the smallest repair that would make the task self-contained
- estimate `certainty_now` and `certainty_if_well_posed` using only `very-low` | `low` | `medium` | `high`

Do not confuse malformed context with hard mathematics. If the packet is ill-posed, make that diagnosis explicit and keep any mathematical conclusion provisional.

If the task produces a report, table, narrative assessment, or recommendation, prepend a short `Prompt/Inference Diagnosis` block before the main result with:
- `context_status`
- `inference_status`
- `blocking_defects`
- `minimal_repair`
- `certainty_now`
- `certainty_if_well_posed`

If `context_status` is `well-posed` and the inference is routine, keep this block concise. If the packet is ill-posed or the inference is underdetermined, do not hide this diagnosis inside later prose.

Use the shared epistemic shape from [docs/research-methods/epistemic-prompt-framework.md](../../../../docs/research-methods/epistemic-prompt-framework.md).

Objective: consume one queued proof target, attempt an informal proof or disproof, run systematic critique, and finalize the result honestly.

Required workflow:

1. Start from the queue dossier
- queue id
- claim text
- source/target statement ids
- candidate object
- invariant
- mathematical_layers packet
- any upstream `lean_symbolic_search` diagnostics or symbolic theorem-candidate provenance
- local InformalMathLib hits

2. Local-first grounding
- what local KB statements matter
- what local InformalMathLib results matter
- how the prose claim, LaTeX theorem, and Lean-style scaffold align
- whether any Lean/Lake bounded-search output sharpens the obligation list or only suggests a theorem shape
- whether the local material already resolves the task
- recorded local-search failures before any browsing

Interpretation rule:
- `mathematical_layers` and `lean_symbolic_search` are typed scaffolds and obligation hints, not proof objects;
- `build_ok = false` is a tooling/context defect unless a theorem-shaped impossibility result is explicitly present;
- a symbolic candidate theorem can motivate a route lemma, but it does not discharge that lemma.

3. Local counterexample and barrier search
- nearest local counterexample pattern
- barrier analogs in the KB or InformalMathLib
- model mismatch probe
- whether the claim survives the local adversarial pass

4. Web-search gate
- is web search triggered under policy
- why or why not
- what exact local search failed first
- if yes, record exact queries and sources
- record what exact statement changed because of the search
- if an external theorem, definition, or axiom is used, record it under `external_references` so it enters InformalMathLib

5. Informal proof or disproof attempt
- theorem/result statement under test
- assumptions
- explicit negative-route heuristic:
  decision = constructive-first / parallel / negative-first,
  epistemic principle,
  triggers,
  anti-triggers,
  why contradiction/impossibility is or is not justified now
- tactic-guided proof control using an informal tactic trace
- normalize goal, introduce assumptions, reduce to route lemma, extract subgoals, construct witness, activate target theorem, transport invariant, negate goal, obstruction probe, derive contradiction, prove impossibility claim, closure check as applicable
- ordered proof steps
- step granularity sufficient for expert inspection
- dependencies for each step
- explicit contradiction/impossibility frame:
  negated claim,
  contradiction target,
  forbidden outcome,
  theorem-shaped impossibility claim if the route fails
- negative route or obstruction analysis

6. Critique judges
- statement grounding
- tactic goal-control
- inferential validity
- assumption discipline
- citation fidelity
- proof granularity
- tactic trace discipline
- tactic subgoal exposure
- prior-art and novelty
- local counterexample search
- obstruction and negative route
- contradiction and impossibility discipline
- closure

7. Final classification
- proved
- disproved
- prior_art_found
- blocked
- deferred

8. Persistable result
- final result statement
- concise summary
- whether it belongs in InformalMathLib now

9. Major-subresult assessment
- mandatory gates: self-contained statement, inspectability, frontier relation, independent value
- 0-3 scores for frontier shift, independence, transferability, barrier clarity, proof closure, search compression
- paper candidate title and summary if the result is strong enough to stand alone
- if all gates pass, total score >= 11, and at least one of frontier shift / independence / barrier clarity is 3, mark it as paper-worthy
