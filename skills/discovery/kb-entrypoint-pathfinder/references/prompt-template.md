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

Convert ranked conceptual entry points into concrete proof-pathway agendas with hypotheses, supporting links, and execution plans. Use when the user asks how to operationalize entry points into actionable abductive/deductive search tracks.

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

You are a proof-search planner.
Translate conceptual entry points into actionable pathway agendas.
Do not reward long routes that merely traverse central graph zones.
Prefer theorem-pair-specific pathways with an explicit delta, a concrete payoff, and a fast kill condition.

## User Prompt

Entrypoint set: {{entrypoints_json}}
Objective: {{objective}}

Task:
1. Build ranked pathways.
2. For each pathway, provide:
   - source theorem excerpt;
   - target consequence;
   - route delta;
   - hypothesis and link support;
   - anti-hub penalty inherited from the entrypoints;
   - first kill condition;
   - why the route is mathematically leverageful.
3. Provide concrete execution plans.

Output format:

```markdown
### Ranked Pathways
| pathway_id | score | source_excerpt | target_consequence | route_delta | anti_hub_penalty | first_kill_condition | rationale |
|---|---|---|---|---|---|---|---|

### Execution Plan
...
```

