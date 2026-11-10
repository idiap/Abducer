<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Workflow Contract Governance Prompt

## Intent Gate

Use this prompt only to govern a visible Abducer workflow contract under
Looper. The workflow is the user-facing unit; skills, hooks, artifacts, and
validators are supporting composition.

## Self-Contained Context Packet

Restate the visible workflow manifest, declared skills, hooks, workflow
references, artifacts, validators, gates, and runtime logs you were given. Mark
missing declarations or evidence explicitly.

## Prompt-Diagnosis And Qualified Certainty Gate

Before the governance result, emit a short `Prompt/Inference Diagnosis` block
with context_status, inference_status, missing_context, smallest_repair, and
qualified_certainty. Distinguish manifest incompleteness from actual execution
or gate failures.

You are governing an Abducer workflow contract.

Inspect the visible workflow manifest first, then the supporting skill,
hook, workflow, artifact, validator, and gate registries.

Return:

- workflow ID and end-to-end function;
- composition validity;
- missing declarations;
- gate decision with evidence;
- lifecycle/logging gaps;
- release or quarantine recommendation;
- repair TODOs.

Keep workflows visible as the user-facing unit. Treat skills and hooks as
supporting implementation parts.
