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

Given connector, pathway, bridge-plan, hardness, and phyp artifacts, investigate concept gaps and conjecture which mathematical abstraction or object types could close them. Use when the user asks for conjecture mode, concept-gap analysis, bridge-filling abstractions, missing intermediate mathematical objects, or a systematic search for abstractions that would make a proof bridge testable.

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

Objective: diagnose concept gaps between current bridge endpoints and conjecture the mathematical abstraction types that would make those bridges testable.

This prompt must separate two movements:

1. bridge-object shaping:
   articulate what kind of missing object, invariant, certificate, witness, representation, or transport law would close the gap;
2. proof-space assessment:
   assess both the constructive route enabled by that object and the negative or impossibility-style route that would show the object cannot exist or cannot pay off under the current commitments.

Required structure:

1. Gap diagnosis
- bridge id
- source statement id
- target statement id
- normalized source theorem excerpt
- normalized target consequence
- route delta
- dominant gap axes
- why the current invariant, transport rule, or theorem-family interface is insufficient

2. Abstraction conjecture
- status: viable | underspecified
- abstraction type
- candidate mathematical object
- theorem-shaped claim enabled by the object
- inferential role
- expected preserved invariant
- barrier relation
- positive route enabled if the object exists
- negative route or impossibility pressure if it does not

3. Definitional reasoning
- necessary attributes
- sufficient attribute sets
- why lexical or topical overlap is not sufficient
- what makes the object theorem-family specific rather than generic
- if the object is only a renamed gap, return `underspecified`

4. Counterfactual reasoning
- if a necessary attribute is removed, what fails
- if a sufficient attribute set is realized, what becomes testable
- what counterfactual would support a constructive route
- what counterfactual would support an impossibility or obstruction diagnosis
- which counterfactual best discriminates a genuine bridge concept from a superficial analogy

5. Validation and assessment
- what theorem-family obligation the abstraction would create
- what impossibility theorem, obstruction, or barrier family it would probe
- how it could fail
- whether failure would still have epistemic value
- what artifact should be updated if retained
