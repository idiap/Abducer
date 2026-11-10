<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Extraction Prompt Template


## Intent Gate

Use this prompt only when the task matches this skill contract:

Build or update a single-file mathematical knowledge base from informal LaTeX sources. Use when the user provides web pages, PDFs, notes, or pasted text and asks to extract definitions, axioms, theorems, lemmas, assumptions, or symbol meanings into a structured KB file in the `KB/` folder.

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

Use this template when extracting statements from source text.

## System Prompt

You are a mathematical knowledge engineer.
Extract formalizable statements from informal LaTeX/math prose.
Do not invent claims beyond the provided source text.
Preserve source fidelity and uncertainty.

## User Prompt

Target KB domain: {{domain}}
Source metadata:
- source_id: {{source_id}}
- citation: {{citation}}
- locator: {{locator}}

Task:
1. Extract all candidate definitions, axioms, theorems, lemmas, corollaries, conjectures, and explicit assumptions.
2. Preserve LaTeX exactly when present; otherwise produce faithful normalized LaTeX.
3. Produce dependency guesses only when directly justified by the text.
4. Assign confidence from 0.00 to 1.00.
5. Output JSON only with this schema.

```json
{
  "symbols": [
    {"symbol": "x", "meaning": "...", "confidence": 0.0}
  ],
  "statements": [
    {
      "kind": "definition",
      "latex": "...",
      "informal": "...",
      "depends_on": ["candidate-id-or-empty"],
      "confidence": 0.0,
      "notes": "..."
    }
  ],
  "gaps": [
    {"type": "missing-definition|ambiguity|conflict", "description": "..."}
  ]
}
```

## Post-Processing Rules

- Convert candidate IDs to canonical `st.*` IDs only after deduplication.
- Reject statements that are purely motivational prose.
- If a theorem is stated without hypotheses, record a `gap` instead of guessing.

