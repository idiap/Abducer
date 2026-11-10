---
name: hegelian-abductive-mechanism-hypothesizer
description: "Generate hypothetical and abductive mechanism hypotheses from a formalized conceptual crisis. Use after a `tension_formalization_packet` exists and the next task is to infer what kind of mediating mechanism, relation, interface, institution, model, protocol, experiment, or control loop would have to exist to address the crisis while preserving its opposed commitments."
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Abductive Mechanism Hypothesizer

## Overview

Move from exact crisis to plausible mechanism families. The question is: if the crisis were addressable, what mechanism would explain how both protected commitments could be jointly satisfied under the material conditions?

The output is not a solution proposal. It is a disciplined hypothesis space over missing mediators: relations, capacities, interfaces, institutions, experiments, controls, or proof obligations that would make the crisis intelligible as addressable.

## Hypothetical and Abductive Logic

Use these inference roles:

- `necessary_mediator`: without this relation, process, or capacity, the protected commitments cannot both be preserved.
- `enabling_condition`: the mechanism might work only if this material or epistemic condition is present.
- `jointly_sufficient_set`: no single requirement suffices, but a named bundle would explain how the crisis is mediated.
- `diagnostic_observation`: if observed, this would make the mechanism more plausible than its rivals.
- `defeater`: if observed, this would show the mechanism only renamed or displaced the crisis.
- `impossibility_boundary`: a condition under which the crisis should be scoped as unaddressable by this mechanism family.

Follow the solver's formal shape: preserve both poles where possible, mediate the exact incompatibility, prevent collapse into one pole, and expose residual limits.

## Abductive Procedure

1. Read the `tension_formalization_packet`.
2. Restate the minimal incompatible commitments as obligations the mechanism must jointly mediate.
3. Infer missing mediators:
   - relation: transport, calibration, authorization, equivalence, limiting map, accountability map;
   - process: feedback loop, measurement update, governance workflow, learning protocol, proof obligation, market design;
   - entity: latent carrier, interface layer, boundary object, role, institution, instrument, data asset;
   - constraint: regime declaration, authority type, uncertainty threshold, rollback boundary, non-displacement guarantee.
4. Generate multiple mechanism hypotheses:
   - conservative mechanism: least structural change;
   - expressive mechanism: new concept or interface;
   - institutional/material mechanism: workflow, governance, infrastructure, or incentive change;
   - hybrid mechanism when formal and material changes are inseparable.
5. For each hypothesis, label the inference role of each claimed requirement: necessary, enabling, jointly sufficient, diagnostic, defeater, or boundary.
6. For each hypothesis, name what would make it explanatory rather than decorative.
7. Do not claim the mechanism works. State what it would have to do and what evidence would make it plausible.

## Output

Return:

```yaml
mechanism_abduction_packet:
  crisis_ref: string
  crisis_restated: string
  required_mediation_shape:
    commitments_to_preserve: []
    incompatibility_to_mediate: string
    missing_relation_or_process: []
    inference_commitments: []
  mechanism_hypotheses:
    - id: string
      label: string
      hypothesis_type: conservative | expressive | institutional | hybrid | experimental
      abductive_claim: string
      if_this_existed_then: string
      formal_mediation:
        new_predicates: []
        new_maps: []
        constraints: []
        preserved_obligations: []
      material_mediation:
        actors: []
        practices_or_infrastructure: []
        resources_needed: []
        incentive_or_governance_changes: []
      explanatory_gain: []
      new_risks: []
      disconfirming_observations: []
      evidence_needed: []
  rejected_hypotheses: []
  assumptions: []
  unknowns: []
```

## Epistemic Discipline

- Prefer mechanisms that explain the incompatibility, not mechanisms that merely rename it.
- Separate necessary mechanism requirements from convenient implementation details.
- State the strongest reason each hypothesis might fail.
- Treat material feasibility as part of abduction when institutions, tools, or infrastructure are required.
- Keep multiple live hypotheses when the evidence underdetermines the mechanism.
