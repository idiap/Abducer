<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Loop Policy

## Objective

After `phyp` generation, iterate through unresolved hypotheses and converge toward a stable support/refute partition.

## Round Mechanics

1. Select unresolved hypotheses (`status` not in `supported|refuted`).
2. Score each hypothesis for support and refutation.
3. Apply verdict transition:
   - `supported` -> `status: supported`
   - `refuted` -> `status: refuted`
   - `provisionally-supported` -> `status: provisionally-supported`
   - `provisionally-refuted` -> `status: provisionally-refuted`
   - `inconclusive` -> `status: needs-testing`
4. Append round evaluation entry into `evaluation_history`.

## Threshold Schedule

- Start with strict thresholds for early rounds.
- Decrease thresholds each round by a fixed step to reduce stagnation.
- Optional final-round forcing emits provisional outcomes by score dominance.
- By default, rounds after the first require new round evidence files.

## Stopping Rules

Stop when one condition is met:

- No unresolved hypotheses remain.
- Maximum rounds reached.
- No new evidence and annealing without evidence is disabled.

## Outputs

- Round-level JSON/Markdown report
- Reviewed hypothesis YAML with updated statuses and evaluation history
- Ranked promotion/refutation candidate lists
