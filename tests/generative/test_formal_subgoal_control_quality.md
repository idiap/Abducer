<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generative Validation: Formal Subgoal Control Quality

This probe validates whether formal subgoal-control decisions are mathematically interpretive rather than boilerplate.

## Quality Criteria

- Target-link specificity: the decision names the target object, not only the route ID.
- Mathematical-object specificity: the blocker mentions objects, premises, regimes, limits, carriers, observables, or theorem conditions.
- Failure-learning quality: the explanation says what the failed attempt taught.
- Decision appropriateness: the chosen action matches the failure structure.
- Universal phrasing: the criteria apply beyond Yang-Mills.

## Probe Cases

1. Informative failed derivation
   - Expected decision: `persist_adapt`.
   - Passing interpretation: the failure exposed a missing bridge lemma or sharper premise.

2. Repeated sterile blocker
   - Expected decision: `backtrack`, `pivot`, `quarantine`, or `stop`.
   - Passing interpretation: persistence is disallowed unless a new premise, object, or bridge is introduced.

3. Analogy-only route
   - Expected decision: `quarantine`.
   - Passing interpretation: analogy can guide evidence search but cannot enter proof authority without transfer certification.

4. Premise-missing formula
   - Expected decision: `backtrack`.
   - Passing interpretation: the formula is moved behind the object, theorem, limit, or representation it assumes.

## Rejection Conditions

- The rationale only says "high value" or "low score".
- The target object is absent.
- The same blocker repeats with `persist_adapt` and no new mathematical learning.
- Evidence-only material is promoted as proof authority.
