<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Frame Adequacy Report

This report asks whether the current vocabulary can state, diagnose, and evaluate the target dependencies.

## Role Coverage

- `conceptual_pressure`: 22
- `creative_candidate`: 16
- `definition`: 7
- `intervention`: 20
- `intervention-focus`: 1
- `problem`: 1
- `remark`: 1
- `target`: 1
- `theorem`: 12
- `validation_obligation`: 16

## Adequacy Signals

- Proxy-eval risk nodes: 20
- Proof-debt or route-lemma nodes: 39
- Blocked nodes: 3

## Decision

warn: the frame is adequate for control-plane navigation, but mathematical proof debt remains explicit.
