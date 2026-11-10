<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Bridge Criteria

## Bridge Score

`bridge_score = 0.45*analysis + 0.25*entrypoint + 0.15*pathway + 0.15*hypothesis`

## Components

- `analysis`: connector candidate score.
- `entrypoint`: strongest endpoint conceptual-entry score.
- `pathway`: strongest endpoint pathway score.
- `hypothesis`: supporting phyp pair priority.

## Tiering

- Tier A: `score >= 0.60`
- Tier B: `0.45 <= score < 0.60`
- Tier C: `< 0.45`
