<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Public reasoning trace contract

Version 2 records expert-inspectable, artifact-grounded summaries of inferences across workflows. It is an additive interface: existing process-graph, reasoning-surface, and specialized monitor outputs remain valid.

The trace is deliberately **not** a chain-of-thought record. Producers must state bounded public premises, an operator, an inspectable warrant, a conclusion, alternatives, falsifiers, uncertainty, and scope. If these are unavailable, they must emit `trace_incomplete`; they must not reconstruct or guess private deliberation.

Each event is run-scoped, monotonically sequenced, causally linked, and uses repository-relative artifact references. External evidence must be marked external. The three status axes are independent:

- `artifact_validation_status` concerns presence and byte integrity only.
- `claim_epistemic_status` concerns the public claim and its evidence.
- `workflow_disposition` concerns routing and execution control.

Consequently, an integrity-valid receipt may coexist with a conjectural or refuted claim. Authorization, successful execution, and HTML presentation never promote a scientific claim. Scope widening or epistemic promotion requires an explicit public warrant, evidence, and relevant authority.

Control events use `claim_epistemic_status: not_applicable` and contain no invented scientific rationale. Public-inference events may cite control events as causal parents, but chronology alone is not an inference.

The canonical schemas are `agentic/spec/public_reasoning_event.schema.json` and `agentic/spec/public_reasoning_trace.schema.json`. The status vocabulary and legacy projection are normative companion files. Presentation hints are advisory and have no semantic authority.
