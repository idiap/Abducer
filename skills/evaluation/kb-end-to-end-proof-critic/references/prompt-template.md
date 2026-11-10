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

Assess whether the current artifact chain supports a plausible end-to-end proof of the main conjecture. Use when the user asks if the current route is close to a real solution, what still blocks end-to-end plausibility, or whether the system should stop because a plausible solution has been found.

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

Objective: determine whether the current artifact chain supports a plausible end-to-end proof of the main conjecture.

Required inputs:

- macro-proof state
- macro-strategy report
- proof-cycle summary
- InformalMathLib index
- terminal proof attempts

Required output:

1. mandatory gates
2. critic-by-critic score and rationale
3. normalized plausibility score
4. proof-debt accounting
5. revisit-penalty assessment
6. stop/continue decision
7. if the answer is continue, explain why another cycle is still justified
8. explicit blocking defects if the answer is continue

Do not reward elegance or route coherence alone.
Require actual closure of the macro-strategy checklist and honest terminal proof critique.

