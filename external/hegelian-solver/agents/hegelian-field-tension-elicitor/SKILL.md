---
name: hegelian-field-tension-elicitor
description: "Elicit and sharpen an implicit or underspecified tension in a field before formal solver work. Use when the user names a field, controversy, research program, practice, technology, policy area, or scientific domain and wants the opposed commitments, stakes, evidence standards, actors, regimes, and latent conceptual pressure made explicit rather than starting from a ready-made failure certificate."
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Field Tension Elicitor

## Overview

Turn a vague field-level discomfort into an explicit tension surface. This skill prepares the material that the crisis formalizer will turn into an exact conceptual crisis.

## Procedure

1. Identify the field and scope: discipline, subfield, practice, time horizon, deployment setting, and affected actors.
2. Name the apparent poles without caricature. Each pole must have a rational commitment, not merely an opinion.
3. Extract the concepts doing load-bearing work: model, object, metric, mechanism, agency, safety, evidence, validity, explanation, autonomy, fairness, scale, or governance.
4. Ask what each pole is trying to preserve:
   - formal commitments: definitions, invariants, constraints, proofs, objective functions, standards;
   - material commitments: instruments, institutions, labor, infrastructure, patient or user outcomes, costs, risks;
   - epistemic commitments: what counts as evidence, whose testimony counts, how uncertainty is managed.
5. Identify pressure points:
   - empirical anomaly, operational breakdown, benchmark saturation, interpretability gap, institutional mismatch, safety incident, measurement proxy failure, regime overextension, or value conflict.
6. Separate genuine tension from noise:
   - disagreement over facts;
   - disagreement over values;
   - ambiguity in terms;
   - scale or regime mismatch;
   - incompatible obligations under shared goals.
7. Produce an elicitation packet with enough structure for evidence cartography and crisis formalization.

## Output

Return:

```yaml
field_tension_elicitation_packet:
  field: string
  scope:
    domain: string
    subfield: string | null
    temporal_scope: string | null
    material_setting: string | null
  tension_name: string
  initial_question: string
  poles:
    - id: string
      label: string
      strongest_version: string
      formal_commitments: []
      material_commitments: []
      epistemic_commitments: []
      protected_successes: []
      unacceptable_losses: []
  shared_background:
    assumptions: []
    shared_goals: []
    shared_terms_with_possible_ambiguity: []
  pressure_points:
    - id: string
      kind: empirical | formal | operational | institutional | ethical | explanatory | governance
      description: string
      affected_commitments: []
      evidence_needed: []
  candidate_crisis_hypotheses: []
  web_expansion:
    decision: required | recommended | not_needed | forbidden_by_user
    reasons: []
  assumptions: []
  unknowns: []
```

## Epistemic Discipline

- Steelman each pole before naming a contradiction.
- Avoid reducing field tensions to binary preference conflict when a regime distinction may dissolve them.
- Distinguish lexical ambiguity from real conceptual incompatibility.
- Preserve actor-level stakes without making them decide formal validity.
- Mark what evidence would weaken or overturn the proposed tension.
