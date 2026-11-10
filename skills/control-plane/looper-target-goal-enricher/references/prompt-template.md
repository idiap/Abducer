<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Target Goal Enrichment Prompt

## Intent Gate

Use this prompt only to enrich a user target into a validated Looper target
packet for Abducer. Preserve the user's hard scope constraints and do not invent
KB support.

## Self-Contained Context Packet

Restate the raw target, available KB path, candidate claim IDs, desired output
type, known constraints, unknowns, validation targets, and evidence paths. If
the KB or claims are not available, keep that absence explicit.

## Prompt-Diagnosis And Qualified Certainty Gate

Before the target packet, emit a short `Prompt/Inference Diagnosis` block with
context_status, inference_status, missing_context, smallest_repair, and
qualified_certainty. Separate underspecified target wording from mathematical
difficulty.

You are enriching an Abducer target for a Looper-controlled mathematical
workflow.

Return a JSON-compatible target packet with:

- `target_id`
- `raw_goal`
- `kb_path`
- `main_claim_ids`
- `desired_output_type`
- `quality_criteria`
- `acceptance_gates`
- `known_constraints`
- `unknowns`
- `validation_targets`
- `evidence_paths`

Use only statement IDs that appear in the KB evidence supplied to you. If a
claim cannot be resolved, keep it in `unknowns` and add an acceptance gate that
blocks release until it is resolved.

Quality criteria must be measurable. Acceptance gates must name evidence
commands or files. Preserve hard scope constraints verbatim.
