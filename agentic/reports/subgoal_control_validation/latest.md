<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Formal Subgoal Control Generative Validation

Status: `validation-probe-defined`

The validation probes distinguish hard-but-live proof debt from low-information repetition. A passing control decision must name the target object, preserve commitments, explain what failure taught, and choose an action consistent with the failure structure.

## Probe Expectations

- Informative failed derivation: `persist_adapt`.
- Repeated sterile blocker: `backtrack`, `pivot`, `quarantine`, or `stop`.
- Analogy-only route: `quarantine`.
- Premise-missing formula: `backtrack`.

## Repair Rule

Reject generic control prose. Require target object, blocker, learning from failure, next action, and backtrack, pivot, quarantine, and stop triggers.
