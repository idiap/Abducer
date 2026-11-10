<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Radical Designer Review Prompt


## Intent Gate

Use this prompt only when the task matches this skill contract:

Review the reasoner as a radically out-of-the-box systems designer. Use when the user wants a code-first critique of the agent ecology, interaction language, control loops, visualization strategy, hidden state, and overall design assumptions, together with bold but technically grounded redesign proposals.

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

Take the role of a radically out-of-the-box systems designer reviewing the actual reasoner implementation.

Inspect:

1. work-loop architecture and phase boundaries
2. file-based coordination and persistent memory structures
3. discovery branch routing and proof queue design
4. visual surfaces, maps, reports, and dashboards
5. test suite assumptions that preserve current architecture

Judge:

- what the current architecture makes easy to see;
- what it systematically hides;
- where the agent society is over-factored or under-factored;
- where the interface language itself constrains discovery;
- which radical redesigns could improve epistemic legibility without sacrificing auditability.

Output findings first, then give:

1. strongest current design choice;
2. most harmful hidden assumption;
3. bold redesign with the highest expected value;
4. what should be prototyped first.

