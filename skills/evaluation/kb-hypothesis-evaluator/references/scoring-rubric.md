<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Scoring Rubric

## Bridge-Link Hypotheses

Support score blends:

- Direct dependency signal (`target.depends_on` already includes support)
- Connector analysis score (`connection_candidates[from->to]`)
- Lexical overlap between support/target statements
- Evidence-term coverage
- Kind compatibility (`definition->theorem`, `theorem->corollary`, etc.)

Refutation score blends:

- Self-loop relation (`support_statement_id == target_statement_id`)
- Missing statement IDs in KB
- Direction conflict (`support.depends_on` includes target)
- Contradiction/negation signal
- Weak-signal penalty

## Intervention-Focus Hypotheses

Support score blends:

- Hypothesis priority
- Cross-component potential
- Relative downstream impact
- Relative unresolved dependency pressure

Refutation score increases with:

- Missing target statement
- Low priority
- Low-yield signal (weak downstream + weak cross-component signal)

## Conceptual-Discovery Hypotheses

Applies to:

- `definition-introduction`
- `representation-shift`
- `intermediate-invariant`
- `barrier-escape-principle`
- `analogy-transfer`
- `normal-form-reduction`

Support score blends:

- Priority
- Connector/analysis pair score
- Lexical/symbolic overlap
- Direct dependency compatibility
- Kind-specific novelty bonus

Refutation score increases with:

- Missing support/target statement IDs
- Contradiction/negation signal
- Negative evidence adjustments

## Coherence and Explanatory Adjustments

When `--coherence-report` is provided:

- `explanatory_power_local` and positive `coherence_delta_global` increase support score.
- Negative `coherence_delta_global` increases refute score.
- Coherence reasons are appended to hypothesis rationale for auditability.

## Verdict Policy

- `supported`: support score exceeds threshold and beats refute score by margin.
- `refuted`: refute score exceeds threshold and beats support score by margin.
- `inconclusive`: neither side dominates.
- Optional forced policy: final tie-break by higher score -> provisional support/refutation.
