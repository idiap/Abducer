---
name: hegelian-conceptual-crisis-formalizer
description: "Formalize an elicited field tension into an exact conceptual crisis packet with incompatible commitments, failed obligations, regime boundaries, evidence states, preservation requirements, and possible transformations. Use after field tension elicitation and evidence cartography when the desired output is a precise formalization of the tension rather than a general explanation or debate summary."
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Conceptual Crisis Formalizer

## Overview

Produce the formalization of a field tension. The output should locate the smallest load-bearing incompatibility that makes the field unable to satisfy its own commitments under the declared material conditions.

## Crisis Types

Classify the crisis as one or more of:

- `measurement_crisis`: the metric or proxy no longer tracks the target concept.
- `regime_crisis`: a concept valid in one regime is overextended into another.
- `ontology_crisis`: the field lacks the entities or relations needed to explain its own cases.
- `interface_crisis`: two systems or practices require incompatible interfaces.
- `objective_crisis`: optimization target and intended role diverge.
- `agency_crisis`: tool, actor, institution, or model status is ambiguous and changes obligations.
- `evidence_crisis`: admissible evidence standards cannot decide the central claim.
- `governance_crisis`: capability, accountability, and control are misaligned.
- `abstraction_crisis`: existing categories are too coarse, too rigid, or collapse decisive distinctions.
- `translation_crisis`: formal success does not transport materially across contexts.

## Procedure

1. Read `field_tension_elicitation_packet` and `tension_evidence_map`.
2. Identify the minimal inconsistent commitment set:
   - commitments A and B;
   - shared assumptions needed for the conflict;
   - material condition under which they cannot both hold;
   - evidence state for each premise.
3. Formalize the tension in two layers:
   - formal layer: symbols, predicates, constraints, obligations, maps, or failure certificates;
   - material layer: field practices, actors, instruments, institutions, data, costs, risks, and consequences.
4. State why simple resolutions fail:
   - semantic clarification only;
   - better measurement only;
   - narrower regime only;
   - adding governance only;
   - declaring one pole irrelevant.
5. Name exact crisis:
   - one sentence;
   - no buzzwords;
   - includes incompatible commitments, scope, and what must be preserved.
6. Emit transformation pressure without prematurely choosing the repair.

## Output

Return:

```yaml
tension_formalization_packet:
  id: string
  field: string
  tension_name: string
  exact_crisis_statement: string
  crisis_types: []
  minimal_incompatible_commitments:
    - id: string
      commitment: string
      pole: string
      formalization: string
      material_anchor: string
      evidence_state: string
      source_refs: []
  shared_assumptions_required_for_crisis: []
  material_conditions:
    scope: string
    regimes: []
    actors_or_systems: []
    stakes: []
  formal_core:
    predicates: []
    constraints: []
    failed_obligations: []
    incompatibility_schema: string
  failed_mediations: []
  preservation_requirements: []
  candidate_transformation_pressures:
    - operator_family: string
      target_concept_hint: string
      what_it_must_preserve: []
      new_risks: []
  evidence_map_ref: string | null
  epistemic_status:
    confidence: low | medium | high
    live_uncertainties: []
    possible_falsifiers: []
    web_expansion_needed: required | recommended | not_needed | forbidden_by_user
  downstream_solver_hooks:
    failure_certificates: []
    discovery_signals: []
    validation_obligations: []
```

## Quality Bar

- The crisis statement must be sharper than the field-level controversy.
- At least two commitments must be steelmanned and preserved unless explicitly rejected.
- The formal core must name the incompatibility, not only the topics involved.
- The material conditions must say when the crisis appears; avoid timeless overclaiming.
- Candidate transformation pressure must remain provisional until obligation verification.
- Hand off to `hegelian-abductive-mechanism-hypothesizer` when the next task is to infer what kind of mechanism could mediate the crisis.

## Epistemic Discipline

- Distinguish contradiction, tradeoff, underdetermination, and missing mediation.
- Treat uncertainty as part of the formalization when it changes what can be concluded.
- Do not collapse material harms into formal inconsistency or formal elegance into adequacy.
- Name the strongest non-crisis interpretation and why it does or does not suffice.
