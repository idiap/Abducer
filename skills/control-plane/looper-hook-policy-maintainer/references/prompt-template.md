<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Hook Policy Prompt

## Intent Gate

Use this prompt only to review Looper hook policy for an Abducer workflow. The
goal is to keep hooks deterministic, visible, and bounded while routing
generative judgment through explicit skills.

## Self-Contained Context Packet

State the hook registry, hook scripts, fixtures, traces, protected paths, and
workflow manifest you were given. If any are missing, mark them as unknown
instead of inferring their contents.

## Prompt-Diagnosis And Qualified Certainty Gate

Before the main result, emit a short `Prompt/Inference Diagnosis` block with
context_status, inference_status, missing_context, smallest_repair, and
qualified_certainty. Separate prompt/context defects from real hook-governance
risks.

Review the Abducer hook registry, scripts, fixtures, and traces.

Return:

- hook coverage summary;
- hidden-orchestration risks;
- accept/warn/block fixture adequacy;
- protected-path policy issues;
- Stop artifact coverage;
- precise hook or fixture repairs.

Hooks must stay deterministic. Put generative judgment in explicit skills, not
in hook scripts.
