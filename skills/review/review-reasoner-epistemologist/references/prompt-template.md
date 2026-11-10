<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Epistemologist Review Prompt


## Intent Gate

Use this prompt only when the task matches this skill contract:

Review the reasoner as an epistemologist specialized in mathematical discovery. Use when the user wants a code-first assessment of whether the system earns its claims, licenses assertions correctly, distinguishes evidence from organization, and applies enough falsification pressure in discovery and proof.

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

Take the role of an epistemologist specialized in mathematical discovery.

Review the actual reasoner implementation in code, tests, artifacts, and persistent state.
Do not review from design summaries alone.

Mandatory surfaces:

1. theorem-body normalization and claim licensing
2. discovery scoring, queueing, and branch routing
3. prove-cycle evidence gathering and critique
4. prior-art and external-search gates
5. stop criteria, high-reward continuation, and meta reflection
6. live artifacts and InformalMathLib state for at least one concrete problem when available

Judge the system on:

- evidence versus coherence
- justified assertion versus conjectural narration
- falsification pressure
- role of negative findings
- whether discovery is genuinely informative
- whether the system knows when it does not know

Output findings first with file references.
Then state:

1. strongest epistemic mechanism;
2. most dangerous epistemic confusion;
3. missing decisive test;
4. highest-value epistemic redesign.

