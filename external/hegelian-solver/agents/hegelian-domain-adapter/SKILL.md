---
name: hegelian-domain-adapter
description: Select and instantiate the correct Hegelian solver schema family for mathematical concepts, physical theories, language-model systems, or generic concept evolution. Use before formalization when the active domain determines concept fields, failure labels, validation obligations, evidence types, and candidate ranking gates.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Domain Adapter

## Overview

Decide which domain profile governs a solver run and declare the extra fields and validation checks that downstream skills must preserve.

## Reference Routing

- Math: `../../refs/hegelian_concept_solver_spec.md`, `../../refs/hegelian_logic_mathematical_concepts.tex`, and discovery details from `../../refs/dialectical_concept_solver_refined_with_discovery.md`.
- Physics: `../../refs/dialectical_concept_solver_physics_examples.md`.
- Language-model systems: `../../refs/dialectical_concept_solver_language_model_evolution.md`.
- `../../refs/dialectical_concept_solver_physics_examples (1).md` is a duplicate of the canonical physics file; use only for provenance checks.

## Domain Profiles

Choose `mathematical_concept` when the concept is a typed theory, algebraic structure, function notion, equivalence notion, geometry, topology, foundation, or proof-oriented abstraction.

Required checks:
- typed signature, axioms, models, tasks, interface, preservation constraints;
- examples/counterexamples and invariants when discovery is requested;
- proof obligations for preservation, resolution, non-collapse, conservativity, universality, transfer, adequacy, and residual limits.

Choose `physical_concept` when the object is a physical model, theory, phenomenon, instrument-facing observable, scale transition, anomaly, or effective theory.

Required checks:
- state space, observables, dynamics, symmetries, parameters, measurement model, regime, evidence, and limiting cases;
- formal, empirical, explanatory, preservation, anti-overfit, measurement, and regime obligations;
- explicit status such as `validated`, `effective`, `provisional`, or `rejected`.

Choose `language_model_concept` when the object is a model, assistant, RAG system, tool-using system, agent, multimodal model, reasoning-time system, or governed deployment.

Required checks:
- model/system layers: representation, architecture, data, objective, interaction, tools, evaluation, safety, governance, history;
- trace evidence separated by type: generation, retrieval, tool result, benchmark score, human preference, formal verification, policy decision, deployment incident;
- safety, reliability, provenance, latency/cost, governance, and regression obligations.

Choose `generic_concept` only when no domain is known. Start with the refined concept tuple and mark domain-specific obligations as `unknown`.

## Epistemic Discipline

- Separate formal validity from material adequacy.
- Name evidence, assumptions, uncertainty, residual limits, and possible falsifiers.
- Distinguish verified, provisional, and speculative claims.

## Output

Emit:

```yaml
domain_profile:
  domain: mathematical_concept | physical_concept | language_model_concept | generic_concept
  schema_kind: string
  required_fields: []
  failure_taxonomy: []
  discovery_taxonomy: []
  validation_gates: []
  ranking_features: []
  refs_used: []
  assumptions: []
  unknowns: []
```
