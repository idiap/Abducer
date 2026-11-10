<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Review Reasoner Prompt Template


## Intent Gate

Use this prompt only when the task matches this skill contract:

Run a multi-perspective, code-first review of the reasoner under five critical lenses: an epistemologist of mathematical discovery, a Fields Medalist mathematician, a DeepMind-style mathematical discovery scientist, a concept-discovery logician, and a radically out-of-the-box systems designer. Use when the user wants a deep review of how the reasoner actually works, where it fails, how the epistemic process is encoded in code, or how the architecture should change.

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

Review the actual repository implementation of the reasoner.
Do not review a high-level description.

Inspect the code and state directly:

1. `skills/common`
2. `skills/*/scripts` for discovery, prove, prior-art, work, and meta control
3. `skills/*/SKILL.md`, `skills/*/references`, and `skills/*/agents/openai.yaml`
4. `tests`
5. `artifacts/<kb-ref>` and `InformalMathLib/<kb-ref>` when a concrete problem state exists
6. supporting docs only as secondary evidence

Run a five-lens critical review:

1. epistemologist specialized in mathematical discovery
2. Fields Medalist mathematician
3. DeepMind-style scientist of mathematical discovery systems
4. epistemology/logician expert in concept discovery
5. radically out-of-the-box systems designer

For each lens:

- identify what the reasoner is actually doing in code;
- state what epistemic function it successfully realizes;
- identify where the implementation overclaims, under-instruments, or confuses structure with evidence;
- identify the most serious missing mechanism;
- recommend changes at the level of code, control flow, prompts, persistence, or evaluation.

Output format:

1. findings first, ordered by severity;
2. one section per reviewer lens;
3. a convergence matrix:
   shared concerns,
   lens-specific concerns,
   disagreements;
4. a prioritized redesign agenda.

