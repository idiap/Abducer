<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Pathway Scoring

## Score

`pathway_score = 0.50*entry_score + 0.30*avg_hypothesis_priority + 0.20*avg_link_score`

## Interpretation

- High score: run first in abductive loop.
- Medium score: run if top pathways stall.
- Low score: park for later exploration.

## Execution Principle

Each pathway must include:

1. Abductive step on anchor statement.
2. Deductive test with top tentative links.
3. Retention rule based on consequence gain.
