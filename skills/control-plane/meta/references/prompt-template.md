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

Reflect on the nature of the current mathematical discovery process from a chosen perspective, explain why the original problem remains hard, interpret the present proof state and intermediate results, and identify what has genuinely shifted or persisted in understanding. Use when the user asks for meta-analysis, reflective interpretation of the discovery process, or how the current search changed the problem framing.

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

Objective: reflect on the current mathematical discovery process itself from a chosen perspective.

Required inputs:

- perspective
- interpretation stance
- epistemic-hardness artifact
- macro-proof state
- macro-strategy report
- proof-cycle summary
- end-to-end plausibility report
- optional promising-directions and search-space-tree artifacts

Required structure:

1. Perspective statement
- chosen perspective
- what that perspective attends to
- what it refuses to overinterpret

2. Original hardness
- why the original problem is hard
- which hardness elements remain central
- which of those elements were made more explicit by the current process

3. Current proof-state interpretation
- what the present macro-proof should be read as
- what it is not yet
- how intermediate results bear on that interpretation

4. Shifts of understanding
- at least three shifts or sharpenings
- at least two persistent difficulties
- explicit shift taxonomy labels

5. Intermediate-result reading
- which current subresults or partial structures already changed expert understanding
- whether they changed problem framing, proof strategy, barrier awareness, or route inspectability

6. Meta-judgment
- what the process has genuinely learned
- what remains epistemically thin
- which next question should govern the next cycle

Guardrails:

- distinguish organization from mathematical discovery;
- distinguish theorem-level progress from programme-level progress;
- treat persistent hardness as informative;
- do not claim understanding shifted if only labels changed.

