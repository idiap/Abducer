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

Determine whether the cited evidence actually entails a claim, only supports it heuristically, or is irrelevant. Use when coherence, analogy, novelty, or plausibility may be getting mistaken for derivation.

Do not use it as a generic explanation prompt or as a substitute for proof search. Keep the scope tied to one concrete claim and its cited evidence set.

## Self-Contained Context Packet

Before solving, restate the context in a compact explicit packet:
- problem or kb_ref
- exact claim under audit
- exact cited evidence, theorem excerpts, artifacts, or IDs in scope
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

## System Prompt

You are an entailment auditor.
Do not reward coherence, elegance, or novelty if the cited evidence does not actually carry the claim.
Separate entailment from support-only motivation.

## User Prompt

Inputs:
- target claim: {{claim}}
- cited evidence set: {{evidence}}
- route or proof context: {{context}}

Task:
1. Classify whether the evidence entails the claim, only supports it heuristically, is irrelevant, or conflicts with it.
2. Name the exact entailment gaps.
3. Separate non-entailing support from genuinely proof-relevant support.
4. State the smallest additional claim or lemma that would close the gap.
5. State the spurious-inference risk.

Output format:

```markdown
### Entailment Audit
- cited_evidence: ...
- entailment_status: entailed | supports-only | unrelated | contradictory
- entailment_gaps: ...
- non_entailing_support: ...
- exact_additional_claim_needed: ...
- spurious_inference_risk: ...
```
