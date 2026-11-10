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

Profile the conceptual breakthrough or abstraction required by the current blocked frontier. Use when the question is no longer which theorem is missing, but what kind of conceptual move discovery must make next.

Do not use it as a generic brainstorming prompt, a theorem prover, or a substitute for queue admission. Keep the scope tied to the blocked frontier, the obstruction classes, the branch families, and the exact discovery-routing decision named in the packet.

## Self-Contained Context Packet

Before solving, restate the context in a compact explicit packet:
- problem or kb_ref
- exact blocked frontier, bridge layer, or obstruction family under inspection
- exact queue items, theorem pairs, excerpts, or artifacts in scope
- exact routing decision, branch dossier, or report to produce
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

## Parallel Mathematical Packet

If a branch family, minimal theorem shape, or routed discovery layer is theorem-sized, emit a native `mathematical_layers` packet instead of leaving it as prose-only strategy text.

Required layers:
- `informal`
- `latex`
- `lean_style`

Required fields:
- `quantifier_signature`
- `object_signature`
- `symbol_ledger`
- `latex.theorem_statement`
- `lean_style.scaffold`

The Lean-style scaffold is a notation-first type-theory representation and should be marked non-executable unless the packet is genuinely formalized.

## Lean/Lake Search Reading

When branch artifacts include `lean_symbolic_search`, use it to classify what kind of breakthrough is still missing.

Read explicitly:
- `build_ok`
- `routes[*].readiness.mode`
- `routes[*].readiness.blockers`
- `routes[*].search_shapes`
- `routes[*].candidate_count`

Interpret them as follows:
- `llm-first` means the branch is still under-typed and the next breakthrough is representational or packet-level;
- `hybrid-llm-plus-symbolic` means the branch needs both typing repairs and bounded theorem-shape search;
- `symbolic-search-ready` means the route is typed enough that discovery should ask which finite bridge family matters most.

Shape patterns are conceptual evidence:
- repeated `transport` pressure suggests regime-transfer work;
- repeated `equivalence` pressure suggests operationalization alignment or coherence work;
- repeated `factorization` pressure suggests diagrammatic or intermediate-object work;
- repeated `obstruction` pressure suggests negative-route discovery is first-class.

Do not treat `build_ok = false` or the absence of symbolic candidates as a mathematical barrier by itself.

## Required Structure

1. Obstruction-family diagnosis
- obstruction class
- why the frontier is blocked here
- decisive next observation

2. Discovery routing decision
- branch family
- required move
- minimal theorem shape
- major-subresult type
- anti-patterns

3. Native mathematical packet for theorem-sized branches
- quantifier signature
- symbol ledger
- LaTeX theorem statement
- Lean-style scaffold
- one-sentence gloss linking notation to the route

4. Symbolic-search reading
- readiness mode
- dominant search shapes
- whether the bottleneck is typing, abstraction, transfer, factorization, or obstruction
- whether the symbolic layer changes branch ranking

5. Search policy
- local-first or external-framework search
- stopping criteria
- what would count as superficial progress
