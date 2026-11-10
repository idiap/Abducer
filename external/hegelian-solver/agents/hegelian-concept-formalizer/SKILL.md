---
name: hegelian-concept-formalizer
description: Normalize a seed concept, theory, model, or system into a solver-ready Hegelian concept node with typed structure, tasks, interface, preservation constraints, examples, invariants, history, and allowed operators. Use when raw prose, examples, specs, or legacy data must become a structured concept representation before evaluation.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Concept Formalizer

## Overview

Turn informal concept material into a concept node that downstream failure, discovery, transformation, and graph skills can consume.

## Inputs

- A `domain_profile` from `hegelian-domain-adapter`.
- Raw concept prose, existing schema, examples, tasks, known failures, or intended use.
- Optional `retrospective_evolution_packet` stages from `hegelian-retrospective-evolution-formalizer`.
- Optional predecessor concepts and protected meanings.

## Procedure

1. Name the concept with a stable `id`, a human `name`, and a short `role`.
2. Separate internal structure from external demands:
   - structure: signature, axioms, state space, architecture, dynamics, tools, policies;
   - demands: tasks, explanation targets, evaluation criteria, intended uses.
3. Record admissible models or interpretations; use explicit nulls when unavailable.
4. Record examples, counterexamples, traces, known successes, known failures, and analogies.
5. Declare invariants, equivalence notions, normal forms, representation maps, regimes, or provenance rules.
6. Declare preservation constraints: facts, distinctions, behaviors, predictions, or interfaces that successors must keep.
7. Declare allowed meta-operators from the domain profile.
8. For retrospective stages, preserve `time_span`, source evidence, material context, and anachronism risks in `history`, `source_refs`, `material_analysis`, and `epistemic_profile`.
9. Record assumptions and unresolved fields instead of silently inventing them.

## Generic Concept Node

Use this base shape unless the domain adapter supplies a stricter schema:

```yaml
concept_node:
  id: string
  name: string
  domain: string
  role: string
  signature: {}
  axioms_or_constraints: []
  admissible_models: []
  tasks: []
  interface: []
  preservation: []
  examples: []
  counterexamples: []
  invariants: []
  equivalences: []
  representation_maps: []
  history: []
  allowed_operators: []
  source_refs: []
  formal_analysis: {}
  material_analysis: {}
  epistemic_profile: {}
  status: draft | active | provisional | validated | rejected
  assumptions: []
  unknowns: []
```

## Domain Extensions

- For mathematical concepts, keep the solver tuple fields visible: typed signature, axioms, models, tasks, interface, preservation constraints, examples, invariants, history, and operators.
- For physical concepts, add state space, observables, dynamics, symmetries, parameters with units, measurement model, regime, evidence, anomalies, limiting cases, and effective/provisional status.
- For language-model concepts, add representation, architecture, data, objective, interaction, tools, evaluation, safety, governance, trace types, and deployment context.

## Epistemic Discipline

- Separate formal validity from material adequacy.
- Name evidence, assumptions, uncertainty, residual limits, and possible falsifiers.
- Distinguish verified, provisional, and speculative claims.

## Quality Bar

- Do not mix evidence into axioms.
- Do not mix intended tasks into proven properties.
- Do not erase partial operations; mark their domain or totalization demand.
- Preserve ambiguity as `unknowns` when the source does not determine a field.
- Make every preservation constraint testable by a later obligation.
