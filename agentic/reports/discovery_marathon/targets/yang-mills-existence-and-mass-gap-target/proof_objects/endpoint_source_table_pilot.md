<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# YM Endpoint Source Table Pilot

Status: `needs_external_math`
Another endpoint marathon allowed: `False`

The repository contains the endpoint gate narrative and required fields, but not the concrete regulated source-equivalence enumeration or outward-rounded log Z evaluator needed to instantiate one positive-D row.

## Sample Slots

- Slot 1 `log Z_{a,c}(-3h)`: `externally-required` because regulated source evaluator or analytic interval proof
- Slot 2 `log Z_{a,c}(-2h)`: `externally-required` because regulated source evaluator or analytic interval proof
- Slot 3 `log Z_{a,c}(-1h)`: `externally-required` because regulated source evaluator or analytic interval proof
- Slot 4 `log Z_{a,c}(0h)`: `externally-required` because regulated source evaluator or analytic interval proof
- Slot 5 `log Z_{a,c}(1h)`: `externally-required` because regulated source evaluator or analytic interval proof
- Slot 6 `log Z_{a,c}(2h)`: `externally-required` because regulated source evaluator or analytic interval proof
- Slot 7 `log Z_{a,c}(3h)`: `externally-required` because regulated source evaluator or analytic interval proof

Kappa certification need: outward-rounded seven-point stencil or root-quartic cap with M8 validity bound

T_tail certification need: cutoff-uniform bound for the endpoint source family in the fixed heat-kernel geometry

Decision rule: promote if I_- >= 0; finite_falsifier if I_+ < 0; quarantine if 0 lies in the interval or T_tail is missing
