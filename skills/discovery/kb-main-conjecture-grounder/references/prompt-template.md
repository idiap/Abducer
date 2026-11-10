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

Ground current KB artifacts in the central theorem or conjecture under study and explain, in mathematical narrative form, how the active routes bear on that conjecture. Use when the user asks how the current bridges, proof sketches, or queue relate to the main conjecture itself, for example how a route in the P vs NP workspace bears on the claim P != NP.

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

Objective: explain how the current artifacts bear on the main conjecture itself.

Evidence-class contract:

- Tag each paragraph implicitly as one of:
  grounded local theorem,
  conditional route claim,
  conjectural bridge-object proposal,
  research recommendation.
- The narrative must make these classes legible to an expert reader.

Required structure:

1. Name the conjecture explicitly.
2. Cite the local KB statements that define the ambient classes and the relevant implication target.
3. State the strongest current conditional route in theorem-pair form.
4. Explain why that route is relevant to the conjecture.
5. Separate:
   what is grounded,
   what is conditional,
   what remains open.
6. End with the current proof frontier: route lemma, carrier, invariant, and next proof tasks.

