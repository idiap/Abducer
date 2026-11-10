<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Release Promotion Prompt

## Intent Gate

Use this prompt only to decide whether a bounded Looper-controlled Abducer
iteration is promotable as control-plane evidence. Do not treat release
promotion as mathematical proof of the target.

## Self-Contained Context Packet

List the iteration ID, target packet, dependency graph/frontier, workflow
manifest, hook results, compliance report, drift report, frame-adequacy report,
and validation evidence supplied to you. Mark absent inputs as unknown.

## Prompt-Diagnosis And Qualified Certainty Gate

Before the release decision, emit a short `Prompt/Inference Diagnosis` block
with context_status, inference_status, missing_context, smallest_repair, and
qualified_certainty. Distinguish missing evidence from genuine release blockers.

Given a controlled Abducer iteration, review:

- target packet;
- dependency graph and frontier;
- workflow registry;
- hook contract results;
- compliance report;
- drift report;
- frame adequacy report;
- validation command evidence.

Return a release report with:

- iteration ID;
- target ID;
- workflow executed;
- evidence table;
- blocking gate status;
- drift and frame-adequacy assessment;
- rollback path;
- open blockers;
- decision: promote, quarantine, rollback, or escalate.

Validation success is not mathematical proof. Promotion means the control-plane
slice is internally coherent and evidence-complete.
