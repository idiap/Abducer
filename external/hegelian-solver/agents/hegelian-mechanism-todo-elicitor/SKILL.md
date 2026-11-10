---
name: hegelian-mechanism-todo-elicitor
description: "Elicit concrete TODOs from abductive mechanism requirements and counterfactual critiques. Use when a crisis-addressing mechanism remains hypothetical and the next step is to produce an ordered backlog of proof work, evidence gathering, experiments, simulations, governance design, implementation tasks, and validation obligations."
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Mechanism TODO Elicitor

## Overview

Turn hypothetical mechanism reasoning into an action backlog. The output should make clear what must be proven, measured, built, governed, or rejected before the mechanism can be treated as a candidate solution.

TODOs are part of the epistemic object. They should expose the remaining distance between a plausible abductive explanation and a validated mechanism: proof distance, evidence distance, material implementation distance, governance distance, and decision distance.

## TODO Classes

Use:

- `formal_work`: definitions, proofs, consistency checks, invariants, mediation maps.
- `evidence_work`: source search, datasets, measurements, audits, field studies, expert review.
- `simulation_or_benchmark`: simulation, replay, benchmark, stress test, red-team test.
- `material_design`: workflow, institution, infrastructure, incentive, governance, staffing.
- `implementation`: prototype, schema, API, policy engine, monitor, report, data pipeline.
- `validation`: acceptance criteria, hard gates, non-collapse tests, residual limit checks.
- `decision`: branch, defer, reject, scope restriction, or escalation.

## TODO Elicitation Rules

- Every high-priority TODO must point to a requirement, hidden assumption, counterfactual failure, or possible falsifier.
- Include at least one stop condition for each mechanism family so failed validation can terminate the branch.
- Separate tasks that discover whether the mechanism is plausible from tasks that implement it.
- When formal and material work are coupled, create paired TODOs rather than one vague omnibus task.

## Output

Return:

```yaml
mechanism_todo_packet:
  requirements_ref: string
  critique_ref: string | null
  todo_groups:
    - group_id: string
      purpose: string
      todos:
        - id: string
          class: formal_work | evidence_work | simulation_or_benchmark | material_design | implementation | validation | decision
          task: string
          why_needed: string
          depends_on: []
          artifact_expected: string
          acceptance_criterion: string
          priority: low | medium | high | critical
          blocks_candidate_acceptance: true | false
  immediate_next_actions: []
  deferred_questions: []
  stop_conditions: []
```

## Epistemic Discipline

- TODOs must be tied to a requirement, uncertainty, or failed counterfactual test.
- Mark blockers that prevent calling the mechanism a candidate repair.
- Include stop conditions so sunk-cost momentum does not masquerade as validation.
- Preserve open disagreement as a decision TODO when evidence cannot settle it yet.
