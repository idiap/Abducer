<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Scoring

## Entrypoint Score

For statement `s`:

`entry_score(s) = 0.45*intervention + 0.30*hypothesis_pressure + 0.15*bridge_incidence + 0.10*phase_weight`

## Components

- `intervention`: from connector `top_interventions` score.
- `hypothesis_pressure`: normalized priority pressure from `phyp` where statement appears as target/support.
- `bridge_incidence`: normalized cumulative score of connection candidates touching statement.
- `phase_weight`: prior weight from concept-evolution phase.

## Usage

Use top 3-5 entry points as immediate abductive targets.
Use concept tracks to diversify proof exploration across paradigms.
