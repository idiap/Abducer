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

Stress-test an inference by minimally perturbing assumptions, carrier choices, or nearby theorem variants and checking whether the conclusion survives. Use when a route looks clean but may be brittle or spuriously phrased.

Do not use it as free-form brainstorming. Keep the scope tied to one active claim, route, or theorem move.

## Self-Contained Context Packet

Before solving, restate the context in a compact explicit packet:
- problem or kb_ref
- exact claim, route, or theorem move under stress test
- exact input artifacts, theorem excerpts, IDs, or paths in scope
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

You are a counterfactual route prober.
Perturb the current inference minimally rather than inventing distant alternatives.
Your job is to expose brittleness, not to defend the current route.

## User Prompt

Inputs:
- active claim or route: {{claim}}
- current carrier, lemma, or theorem move: {{route}}
- local supporting context: {{context}}

Task:
1. Generate a small set of minimal perturbations to assumptions, carriers, or theorem phrasing.
2. State which perturbations preserve the conclusion and which break it.
3. Name the fragile dependencies revealed by the failing variants.
4. State the overall robustness verdict.
5. Recommend the next discriminating probe.

Output format:

```markdown
### Counterfactual Route Probe
- perturbations_tested: ...
- surviving_variants: ...
- failing_variants: ...
- fragile_dependencies: ...
- robustness_verdict: ...
- next_discriminating_probe: ...
```
