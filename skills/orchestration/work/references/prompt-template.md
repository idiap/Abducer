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

Run the persistent outer work loop that alternates discovery and prove cycles, refreshes end-to-end proof plausibility after each step, and stops either when a maximum cycle budget is reached or when the current artifacts support a plausible solution to the main problem.

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

Objective: run one outer-loop `work` step and decide whether to continue or stop.

Required workflow:

1. load the persistent work state
2. refresh the end-to-end plausibility report
3. if the stop rule already fires, stop and explain why
4. otherwise run exactly one phase:
   - discovery: refresh the proof queue from the current frontier
   - prove: consume the next queue item and open the next proof dossier
5. refresh the plausibility report again
6. if discovery ran, summarize the `lean_symbolic_search` diagnostics separately from mathematical blockers
7. account for proof debt and revisit penalties
8. if the loop continues, explain why another cycle is justified
9. persist the next phase and stop status

Required output:

1. current phase executed
2. updated cycle count
3. next phase
4. stop status
5. proof debt summary
6. symbolic-search summary when discovery executed
7. revisit penalty summary
8. most important blocking defects if the loop continues

Interpretation rule:
- separate Lean/Lake tool failures, packet-typing failures, and genuine mathematical blockers;
- do not report a generated Lean module or symbolic theorem candidate as proof progress unless a theorem was actually discharged.

Do not run an unbounded autonomous search.
One invocation of `work` performs one outer-loop step.
