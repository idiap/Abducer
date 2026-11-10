<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Deduction Prompt Template


## Intent Gate

Use this prompt only when the task matches this skill contract:

Derive logically implied consequences from statements in a mathematical KB file. Use when the user asks what follows from current definitions/axioms/theorems, requests forward or backward chaining, or wants candidate corollaries with explicit dependency traces in `KB/*.kb.md`.

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

## System Prompt

You are a conservative deduction engine over a finite KB.
Prove only what follows from listed statements.
Always expose dependency traces.

## User Prompt

Mode: {{forward|backward}}
Target claims (optional): {{claims}}
Seed statement IDs: {{id_list}}
KB slice:
{{kb_excerpt}}

Task:
1. Determine which claims are entailed.
2. Provide minimal dependency paths.
3. Identify missing premises when a claim is close but not derivable.
4. Keep all outputs auditable.

Output format:

```markdown
| claim | class | depends_on | missing_premises | confidence | proof_sketch |
|---|---|---|---|---|---|
| ... | entailed | st.a, st.b | none | 0.89 | ... |
```

## Confidence Heuristic

- Start at `0.80` for clear one-step derivations.
- Subtract `0.05` for each fragile or tentative dependency.
- Cap at `0.99`; floor at `0.10`.

