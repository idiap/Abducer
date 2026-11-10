---
name: hegelian-mechanism-counterfactual-critic
description: "Critique crisis-addressing mechanism requirements with counterfactual, adversarial, and abductive tests. Use after a mechanism requirements packet exists and the work needs to identify whether the proposed requirements actually mediate the crisis, where they fail, what observations would disconfirm them, and which alternative mechanisms remain live."
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Mechanism Counterfactual Critic

## Overview

Stress-test mechanism requirements before they become accepted transformations. The critic asks: under what plausible worlds would this mechanism fail, collapse a protected commitment, or only appear to solve the crisis?

The critique should preserve abductive rivalry. A mechanism is stronger when it predicts where it should work, where it should fail, and what observations would favor it over alternative mechanism families.

## Counterfactual Tests

Apply tests such as:

- `remove_requirement`: what breaks if this requirement is absent?
- `invert_incentive`: what happens if actors optimize the mechanism against its purpose?
- `shift_regime`: what happens outside the declared regime?
- `proxy_capture`: what if the mechanism satisfies the proxy but not the target?
- `authority_gap`: who can authorize, audit, or stop the mechanism?
- `evidence_shift`: what if evidence is thinner, noisier, or distribution-shifted?
- `material_bottleneck`: what if infrastructure, labor, money, data, or governance capacity is missing?
- `noncollapse_probe`: does the mechanism preserve both poles or silently choose one?

## Critic Procedure

1. Identify the requirements that claim necessity or joint sufficiency.
2. Remove, invert, or regime-shift each such requirement.
3. Ask whether the crisis returns, moves elsewhere, or collapses into one pole.
4. Compare live rival mechanisms when the evidence underdetermines the proposed one.
5. Convert serious failures into required revisions or stop conditions for the TODO elicitor.

## Output

Return:

```yaml
mechanism_counterfactual_critique:
  requirements_ref: string
  overall_status: plausible | underdetermined | fragile | collapsed | rejected
  counterfactual_tests:
    - id: string
      test_type: remove_requirement | invert_incentive | shift_regime | proxy_capture | authority_gap | evidence_shift | material_bottleneck | noncollapse_probe
      scenario: string
      expected_if_mechanism_valid: string
      failure_signal: string
      affected_requirements: []
      result: pass | fail | unknown | needs_evidence
  hidden_assumptions: []
  collapse_risks: []
  alternative_mechanisms_still_live: []
  required_revisions: []
  evidence_or_experiment_priorities: []
```

## Epistemic Discipline

- A failed counterfactual test does not always reject the mechanism; it may restrict the regime.
- Separate mechanism fragility from crisis impossibility.
- Do not use worst-case speculation as disproof unless the risk is material under the target conditions.
- Preserve disconfirming observations as future graph triggers.
