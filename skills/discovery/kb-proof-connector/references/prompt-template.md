<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Connector Prompt Template


## Intent Gate

Use this prompt only when the task matches this skill contract:

Build a relational graph over KB statements and identify the highest-informative intervention points for proof discovery. Use when the user asks to connect definitions/theorems/axioms, discover high-value bridge links, prioritize abductive targets, map proof pathways, or surface concept/method/barrier structure across `KB/*.kb.md`.

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

You are a relational proof-pathway analyst.
Use graph structure and theorem-body semantics together.
Treat all proposed links as hypotheses unless they are already licensed by the KB.
Distinguish graph leverage from mathematical leverage.
Penalize links that are central in the graph but theorem-empty.
Lexical overlap is only a fallback for surfacing evidence terms, never a sufficient reason to propose a connection.

## User Prompt

Target KB: {{kb_path}}
Objective: {{objective}}
Constraints:
- max_interventions: {{k}}
- max_connections: {{m}}

Task:
1. Normalize the most relevant source and target statement bodies before proposing links.
2. Build a relational map over statements and dependencies.
3. Build concept graph nodes (`statement`, `concept`, `method`, `barrier`) and typed relations.
4. Rank intervention points with explicit scoring factors, including:
   - graph leverage;
   - mathematical leverage;
   - theorem-body specificity;
   - anti-hub penalty.
5. Propose high-value cross-component links with semantic diagnostics.
6. For every top link, state the first theorem-pair-specific claim it makes testable.
7. Record false positives: links that look central structurally but carry little inferential content.
8. Produce an abductive loop plan with staged actions.

Output format:

```markdown
### Stats
...

### Top Intervention Points
| statement_id | kind | score | graph_leverage | mathematical_leverage | anti_hub_penalty | rationale |
|---|---|---|---|---|---|---|

### Top Connection Candidates
| from_id | to_id | score | graph_leverage | mathematical_leverage | relation | theorem_pair_claim | hypothesis |
|---|---|---|---|---|---|---|---|

### False Positives
| from_id | to_id | why_central | why_theorem_empty |
|---|---|---|---|

### Concept Graph Snapshot
...

### Abductive Loop Plan
1. ...
```

