---
name: hegelian-use-case-motivation-writer
description: Generate a grounded motivation for a Hegelian solver use case from its role, intended use, examples, material stakes, failure pressure, discovery signals, and epistemic limits. Use when a report should explain why a scenario matters before presenting formal notation, concept evolution, validation, or ranking.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Use Case Motivation Writer

## Purpose

Write the motivation that answers: why is this use case worth running through the solver at all?

The motivation should make the reader understand the concrete work the concept is supposed to do before the report introduces failures, successors, validation packets, or formal notation.

## Required Inputs

- Use case `name` and `role`.
- Declared `tasks`, especially task goals and expected use.
- `examples`, `counterexamples`, `reported_failures`, or anomalies.
- `material_analysis`, especially practice, stakes, evidence, phenomena, or residual limits.
- `formal_analysis`, especially the trigger and target operator.
- `epistemic_profile`, especially assumptions, knowns, uncertainty, and falsifiers.
- Optional discovery signals and selected candidate successor.

## Procedure

1. Name the use case and its concrete conceptual role.
2. State the intended use in task language, not only in domain labels.
3. Ground the use case in examples or practice so it does not sound abstract by default.
4. State why the current concept comes under pressure: failure, anomaly, missing operation, missing invariance, missing evidence, or discovery signal.
5. State the stakes: what breaks, becomes misleading, or remains unusable if the pressure is ignored.
6. State why the solver is an appropriate instrument for this case: it can test preservation, candidate repair, obligations, ranking, and residual limits.
7. Name epistemic limits and assumptions briefly so motivation does not overclaim.

## Style

- Write 3-5 short paragraphs.
- Start with concrete use, not abstract dialectical vocabulary.
- Prefer "This use case is motivated by..." only once.
- Use exact artifact terms when they are available, such as failure labels, task names, and operators.
- Keep motivation separate from the final explanation: motivation explains why the case matters; explanation says what the solver did.

## Output Shape

Return:

```yaml
motivation:
  paragraphs:
    - string
motivation_terms:
  use_case: string
  intended_use: string
  examples_or_practice:
    - string
  pressure: string
  stakes: string
  why_solver: string
  epistemic_limits:
    - string
```

## Guardrails

- Do not invent historical facts or empirical evidence not present in the artifacts.
- Do not treat the proposed successor as already validated.
- Do not collapse motivation into a generic sales pitch.
- Do not hide uncertainty, residual limits, or missing evidence.
- Do not quote raw JSON; use the artifact content in prose.
