<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# P vs NP Inference Quality Reviewer Generative Probes

Use these probes when forward-testing `pvsnp-inference-quality-controller` and the consistency reviewers.

## Fixed Exponent Inflation

Prompt: A branch proves that SAT lacks `SIZE(n^3)` circuits on infinitely many lengths and claims this is enough for `NP not subset P/poly`.

Expected behavior: the reviewer must identify fixed-exponent-only evidence, infinitely-often length regime, and invalid promotion to all-polynomial nonuniform separation. The next obligation is a quantifier repair lemma.

## Natural Property Overreach

Prompt: A branch says natural proofs blocks a proposed combinatorial lower-bound property, but it has not checked largeness, constructivity, or usefulness.

Expected behavior: the reviewer must reject the generic barrier label, request the three natural-proofs conditions, and preserve possible non-large or nonconstructive escape conditions.

## MCSP Row Advice Leak

Prompt: A branch extracts a hard MCSP row using a nonuniform selector and claims an advice-free NP lower bound.

Expected behavior: the reviewer must identify advice leakage, separate row hardness from language hardness, and request a uniform row-selection certificate before promotion.
