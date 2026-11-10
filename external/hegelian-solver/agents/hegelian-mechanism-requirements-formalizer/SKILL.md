---
name: hegelian-mechanism-requirements-formalizer
description: "Turn abductive mechanism hypotheses into formal and material requirements for a crisis-addressing mechanism. Use after mechanism hypotheses have been generated and the desired output is a solver-shaped requirements packet with predicates, mediation maps, capacities, material preconditions, validation obligations, risks, and residual limits."
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Mechanism Requirements Formalizer

## Overview

Convert hypothetical mechanism ideas into requirements precise enough for obligation verification, experiments, design work, or future transformation proposals.

The requirements packet should make a hypothetical mechanism inspectable: what it must define formally, what must exist materially, what evidence would support it, what would count as non-collapse, and where the mechanism's regime ends.

## Requirement Kinds

Use these requirement classes:

- `formal_capacity`: predicate, map, invariant, equivalence, threshold, proof obligation, or objective relation.
- `material_capacity`: actor, workflow, infrastructure, dataset, instrument, market, governance body, or operational capability.
- `interface_capacity`: typed API, authority boundary, measurement bridge, evidence bridge, institutional handoff, or human review surface.
- `epistemic_capacity`: uncertainty quantification, provenance, calibration, auditability, source support, falsification protocol.
- `safety_or_noncollapse_capacity`: prevents the mechanism from satisfying one pole by erasing the other.
- `regime_capacity`: states where the mechanism is valid, invalid, or untested.

## Formal and Material Coupling

For every central requirement, say whether it is:

- `necessary`: the mechanism cannot address the crisis without it.
- `jointly_sufficient`: it helps only as part of a named bundle.
- `exploratory`: plausible but not yet known to be required.
- `regime_specific`: required only under declared material conditions.

Material inference is not secondary. If a requirement depends on labor, data, institutional authority, time scale, budget, physical infrastructure, safety review, or adoption incentives, encode that dependency instead of hiding it in prose.

## Procedure

1. Select the hypothesis or small hypothesis set worth formalizing.
2. Convert each preserved commitment into a requirement.
3. Convert each missing mediator into a formal relation or material process.
4. Add non-collapse requirements: the mechanism must not solve the crisis by suppressing a protected pole.
5. Add feasibility requirements: resources, institutions, data, authority, incentives, and operational time scales.
6. Add validation obligations that can later become `ValidationPacket` items.
7. Add residual limits and open TODOs.

## Output

Return:

```yaml
mechanism_requirements_packet:
  crisis_ref: string
  selected_hypothesis_refs: []
  mechanism_name: string
  mechanism_role: string
  requirements:
    - id: string
      kind: formal_capacity | material_capacity | interface_capacity | epistemic_capacity | safety_or_noncollapse_capacity | regime_capacity
      necessity_status: necessary | jointly_sufficient | exploratory | regime_specific
      statement: string
      formalization: string | null
      material_anchor: string | null
      verifies_commitments: []
      validation_method: proof | simulation | benchmark | audit | field_study | policy_review | experiment | trace_replay | human_review
      evidence_needed: []
      failure_mode_if_missing: string
  mediation_maps:
    - id: string
      source_commitment: string
      target_commitment: string
      map_type: transport | calibration | authorization | accountability | limiting | embedding | refinement | feedback | governance
      statement: string
      required_properties: []
  material_preconditions: []
  implementation_surfaces: []
  validation_obligations: []
  residual_limits: []
  open_todos: []
  assumptions: []
  unknowns: []
```

## Epistemic Discipline

- Requirements must be testable, inspectable, or explicitly marked as open.
- Do not smuggle success into the mechanism name; spell out the capacities.
- Mark which requirements are necessary, which are sufficient only together, and which are exploratory.
- Keep formal mediation and material feasibility in separate fields even when they depend on each other.
