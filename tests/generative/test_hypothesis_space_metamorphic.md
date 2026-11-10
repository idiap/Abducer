<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Hypothesis-Space Metamorphic Validation

## Evidence Removal

When source artifacts are removed from candidates, `source_grounding` must fail
and route disposition must become `quarantine` or `reject`.

## Gate Perturbation

When `proof_queue_readiness` changes from pass to warn, theorem-shaped promotion
must fall back to discovery branch, revision loop, or evidence task.

## Route Causality

The hypothesis exploration map must record `changed_routing_decision: true` for
candidates that alter continuation behavior.
