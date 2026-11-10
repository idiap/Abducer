---
name: hegelian-candidate-ranker
description: Rank Hegelian repair and discovery candidates using transparent multi-objective scores, hard validation gates, Pareto-frontier handling, complexity and loss penalties, and domain-specific ranking features. Use after obligation verification to select, defer, reject, or branch successor concepts.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Candidate Ranker

## Overview

Compare candidates without flattening genuinely different conceptual virtues into a single forced winner. Preserve a Pareto frontier when successors optimize different goals.

## Inputs

- Transformation candidates.
- Validation packets.
- Domain profile.
- Optional user priority weights.

## Hard Gates

Reject or block candidates that fail non-collapse, protected preservation, declared-regime checks, measurement-interface checks for physics, or bounded-risk checks for language-model systems.

Do not let a high novelty score compensate for a hard-gate failure.

## Scoring

For generic and mathematical candidates, score:

`resolution`, `preservation`, `compression`, `universality`, `transfer`, `novel_utility`, `invariance_gain`, minus `complexity`, `loss`, `overfit`, and `proof_burden`.

For physics, score:

`empirical_gain`, `predecessor_recovery`, `symmetry_gain`, `predictive_novelty`, `compression`, `robustness`, minus `ad_hocness`, `unnecessary_ontology`, `regime_confusion`, and `complexity`.

For language-model systems, score:

`failure_resolution`, `capability_preservation`, `source_grounding`, `tool_correctness`, `safety`, `monitorability`, `latency_cost_fit`, `governance`, minus `new_risk`, `workflow_complexity`, and `maintenance_cost`.

## Decision Labels

Use:

- `accept`: all hard gates pass and score is strong.
- `accept_as_branch`: candidate is valid but optimizes a different objective.
- `provisional`: promising but key obligations are partial or unknown.
- `defer`: needs evidence or proof work.
- `reject`: hard gate failed or dominated by better candidates.

## Epistemic Discipline

- Separate formal validity from material adequacy.
- Name evidence, assumptions, uncertainty, residual limits, and possible falsifiers.
- Distinguish verified, provisional, and speculative claims.

## Output

Return a ranked table with scores, gate results, accepted branches, rejected candidates, and the reasoning needed by the graph serializer.
