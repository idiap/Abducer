<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Stop Criteria

The outer `work` loop stops when either condition holds:

## 1. Cycle Budget Exhausted

Stop when:

- `cycle_count >= max_cycles`

This is a hard budget stop.

## 2. Plausible Solution Detected

Stop when the end-to-end proof critic reports `plausible_solution_detected = true`.

That requires:

1. the main conjecture is grounded by a final implication chain;
2. at least one terminal proved attempt exists;
3. the macro-strategy completion checklist is clear of open and partial items;
4. no terminal critique judge failures remain;
5. the normalized critic score is at least `0.80`;
6. no critic scores below `2`.

## Continue Conditions

Continue if:

- there is no plausible solution yet; and
- the cycle budget is not exhausted.

In that case the loop alternates the next phase:

- `discovery -> prove`
- `prove -> discovery`
