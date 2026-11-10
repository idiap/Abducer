<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Formal Subgoal Control Policy

This policy controls formula-like subgoals across Abducer targets. It is intentionally universal: the active target ledger supplies the domain commitments, while the workflow supplies the decision discipline.

## Decisions

- `persist_adapt`: continue only when the subgoal remains attached to the target object and the last failed attempt produced new mathematical information.
- `backtrack`: move the claim behind the premise, object, theorem, limit, or representation it currently assumes.
- `pivot`: change route family after repeated certified failure with no new target-relevant learning.
- `quarantine`: preserve an interesting route as evidence, analogy, or transfer-risk material without proof authority.
- `stop`: remove the subgoal from active loop budget when it has no target-object link or no informative learning path.

## Required Interpretation

Every controlled subgoal must state:

- the target object it is about;
- the essential commitments it preserves;
- the current blocker;
- what the last failure taught;
- the next action;
- what would force backtracking, pivoting, quarantine, or stop.

## Workflow Role

The policy is enforced at candidate generation, route ranking, reasoning-event logging, monitor-packet construction, long-horizon probing, HTML rendering, gate policy, and release promotion. It prevents a formula from persisting merely because it sounds important.

## Validation Boundary

Deterministic validators can require fields, compatibility, and repeated-blocker action. Generative validation still has to judge whether the explanation is mathematically meaningful and target-aware.
