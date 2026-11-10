<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reasoning trace compatibility boundary

The workflow-neutral reasoning trace is an additive, opt-in reporting path. It does not replace the established process graph, reasoning dynamics, conceptual dynamics, or the specialized Yang–Mills reasoning monitor.

## Stable surfaces

The existing reports retain their current generators, output locations, embedded packet formats, controls, first view, domain terminology, and command-line behavior. Their semantic contract is frozen in `tests/fixtures/reasoning_trace/main_workflow_baseline/compatibility_contract.json`. The compatibility test checks the expert-visible controls and information surfaces rather than comparing timestamp-sensitive HTML byte for byte.

The generic trace may read legacy artifacts through a conservative adapter. It must not write back to those artifacts or infer scientific claims from filenames, receipts, green control decisions, or presentation labels. Missing public rationale is represented as `trace_incomplete`.

## Version boundary

- Legacy reports remain the default for the main discovery workflow.
- Generic trace generation is explicit and writes only to the public-reasoning report area.
- Existing report schemas are supported projections, not the semantic schema for named workflows.
- A digest receipt establishes artifact identity and integrity; it does not establish entailment, correctness, novelty, or proof acceptance.
- Promotion of the generic renderer requires the compatibility suite, semantic trace validation, offline HTML checks, and expert review to pass.

This boundary lets named workflows gain richer inference visibility without destabilizing a report that is already useful to its main-workflow audience.
