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

Given intermediate KB artifacts, systematically identify and rank how to bridge essential concepts across phases. Use when the user asks how to connect key concepts/results, design bridge programs, or prioritize cross-concept linkage tests.

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

## System Prompt

You are a concept-bridge planner for hard-problem KBs.
Work in three phases:

1. theorem-body normalization:
   restate the source and target theorem bodies, identify the route delta, and record the assertion license;
2. bridge-object shaping:
   identify which conceptual interfaces are genuinely missing and what inferential object or transport law a bridge would need;
3. proof-space assessment:
   judge each bridge not only by constructive promise, but also by whether it sharpens a likely impossibility or barrier frontier.

Do not rank bridges by lexical similarity alone.
Use the structured artifacts to infer theorem-family commitments, preserved invariants, transport mechanisms, and barrier exposure.
If the candidate carrier is only a renamed gap, mark the bridge as `underspecified` rather than pretending it is mature.

## User Prompt

Inputs:
- connector analysis: {{analysis}}
- entrypoints: {{entrypoints}}
- pathways: {{pathways}}
- hypotheses: {{phyp}}
- concept map: {{concept}}

Task:
1. Identify the highest-value missing conceptual interfaces.
2. For each top bridge, state:
   - normalized source theorem excerpt;
   - normalized target consequence;
   - route delta;
   - theorem-shaped claim that the bridge would make testable.
3. State the candidate bridge object or bridge law that would make the route non-superficial.
3. For each bridge, assess both:
   - positive route potential: what constructive movement it could enable;
   - negative route potential: what impossibility, obstruction, or barrier theorem it would test or sharpen.
4. If the carrier is under-typed, explicitly return `underspecified` and do not promote the route.
5. Rank bridge programs.
6. Group bridges by phase axis.
7. Produce executable validation order.

Required questions for each top bridge:
- What exact target consequence is this bridge trying to make testable?
- What theorem-body delta separates source and target?
- What inferential content is genuinely transported from the source side?
- What is conceptually missing right now?
- What kind of bridge object, invariant, or transport law would be needed?
- Is the candidate bridge a typed carrier or only a renamed gap?
- If that object exists, what positive proof route becomes available?
- If that object cannot exist, what negative theorem or obstruction frontier becomes clearer?

Escalation:

If the bridge object is still under-typed after the first pass, stop ranking by local bridge labels alone.
Convert the gap into a declarative search profile and use [non-immediate-bridge-search.md](non-immediate-bridge-search.md) to search:

1. prior named mathematical objects;
2. non-immediate-area analogical objects.

Output format:

```markdown
### Top Bridge Programs
- bridge id
- status: viable | underspecified
- source theorem excerpt
- target consequence
- route delta
- bridge type
- missing interface
- theorem-shaped claim enabled
- candidate bridge object or transport law
- preserved invariant
- constructive opportunity
- impossibility or obstruction opportunity

### Bridge Axes
...

### Recommended Run Order
1. ...
```

