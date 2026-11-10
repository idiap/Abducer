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

Transform final KB reasoning artifacts into a bridge-first expert report that explains the main conceptual bridges, their proof sketches, and the supporting high-potential hypotheses using transparent generative justification. Use when the user asks for a final scientific report, an expert-facing explanation of the leading bridge programs, or a rigorous explanation of why specific bridges/hypotheses deserve expert attention.

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

Objective: produce a final expert-facing report from end-stage KB artifacts that explains the main conceptual bridges, the proof sketches behind them, and why those bridges are currently the right objects of attention.

This prompt must be bridge-first rather than hypothesis-only.

Evidence-class contract:

- Every paragraph must read primarily as one of:
  grounded local theorem,
  conditional route claim,
  conjectural bridge-object proposal,
  research recommendation.
- Keep these classes legible in the prose.

Required structure:

1. Scientific framing
- target theorem family or problem regime
- inferential objective
- artifact provenance
- why a bridge-first reading is appropriate
- evidence class for each paragraph: grounded local theorem | conditional route claim | conjectural bridge-object proposal | research recommendation

2. Main conceptual bridge portfolio
- bridge id
- source and target regimes
- missing conceptual interface
- conjectured bridge object or transport law
- preserved invariant
- why the bridge is theorem-family specific rather than topical

3. Proof sketch interpretation for each main bridge
- selected proof-strategy family
- why that proof family fits this bridge
- positive route: what constructive program becomes plausible if the bridge object exists
- key proof obligations, candidate lemmas, and outline steps
- negative route: counterfactual, impossibility pressure, or abort condition that would disqualify the bridge

4. Expert justification
- why this bridge outranks nearby alternatives
- what existing evidence supports it
- what would count as genuine progress
- what would count as falsification or non-payoff

5. Supporting hypothesis portfolio
- linked hypothesis ids
- how they support or weaken the bridge
- where hypothesis evidence is strong, provisional, or still open

6. Expert action plan
- immediate mathematical checks
- barrier probes
- revision triggers
- when to continue, sharpen, split, or abandon the bridge

7. Limitations and confidence
- known blind spots
- artifact sparsity warnings
- which conclusions are strongly grounded vs still conjectural

