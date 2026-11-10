<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Novelty Policy

## Candidate Strength

`base_strength = 0.65*pathway_score + 0.35*support_score`

Where:

`support_score = 0.60*avg_hypothesis_priority + 0.40*max(avg_link_score, avg_bridge_score)`

## Diversity-Aware Selection

Use greedy selection with:

`selection_score = 0.70*base_strength + 0.30*novelty`

Novelty combines:

- phase novelty (new phase preferred)
- low anchor overlap with already selected strategies

## Objective

Maximize expected progress while maintaining conceptual diversity and non-redundancy.
