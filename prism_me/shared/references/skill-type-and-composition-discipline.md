<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Skill Type And Composition Discipline

This reference explains how to express Prism-style skill typing and composition today in `prism_me`, and how that maps to the planned Prism-core evolution.

Use it when a request needs more explicit skill contracts, richer composition rules, or a clearer path from external capabilities into Prism-shaped agent surfaces.

## Why This Discipline Exists

`prism_me` already has strong stage discipline, but some of the most important semantics still need to be distributed across the existing artifact set.

This note keeps the model systematic without forcing a disruptive artifact migration before Prism core lands a first-class skill contract profile and composition schema.

## The Contract Shape To Elicit

For each significant skill or capability, make the following explicit:

- input evidence types
- output schema
- preconditions
- assumptions
- admissible claim types
- confidence and uncertainty behavior
- provenance emitted
- validators and evaluators
- upstream and downstream dependencies

## Where To Record Each Concern Today

`prism_me` can now keep this information in the existing stage artifacts, and it can also emit aligned optional serializations in `02f` and `02g` when a request needs them.

### `02-agent-contract.yaml`

Record:

- invocation mode
- entrypoints
- typed inputs and outputs
- coordination role
- reasoning-log expectations

This is the closest existing artifact to the Prism-native typed boundary contract.

If `02f-skill-contract-profile.yaml` exists, keep it aligned with this file and treat it as the richer normalized serialization for skill typing. Use the current core field names directly: `input_evidence_types`, `output_contract`, `preconditions`, `assumptions`, `claim_policy`, `confidence_policy`, `provenance_policy`, `validators`, `evaluators`, `upstream_dependencies`, and `downstream_dependencies`.

### `02b-quality-criteria.md`

Record:

- admissible claims
- non-admissible claims
- confidence expectations
- uncertainty disclosure rules
- provenance expectations for answers, evidence, and synthesis
- validator dimensions
- evaluator dimensions
- generative quality criteria

This file is where the epistemic and content-quality bar should be made precise.

### `03b-dependency-map.md`

Record:

- upstream dependencies
- downstream dependencies
- runtime dependencies
- `uv` bundles
- backend profiles
- reference KBs
- workspace mounts
- fragile hidden dependencies

Use Prism dependency terms rather than generic package lists.

### `04-slice-plan.md`

Record:

- execution sequence
- branch points
- refinement loops
- critic or judge checkpoints
- evidence aggregation moments
- contradiction localization and resolution steps
- delegation boundaries

This file is the current best place to spell out composition behavior.

If `02g-composition-model.yaml` exists, keep it aligned with this file and treat it as the richer normalized serialization for composition semantics. Use the current workflow policy field names directly: `kind`, `condition`, `branch_targets`, `max_iterations`, `exit_when`, `iteration_input`, `delegate_to`, `aggregation_sources`, `aggregation_mode`, `contradiction_resolution`, `judge_role`, and `notes`.

### `04b-test-strategy.md`

Record:

- deterministic validators
- schema checks
- evaluator plans
- generative tests
- reflective refinement loops
- failure localization expectations
- regression protection after refinement

This is where the contract becomes executable quality control.

## Composition Vocabulary To Use

Use these names consistently in the artifacts above:

- `sequence`
- `branch`
- `loop`
- `refinement`
- `arbitration`
- `judge`
- `delegation`
- `aggregation`
- `contradiction-resolution`

When using one of these patterns, also record the operating rule:

- branch guard
- loop exit condition
- max iteration count
- winner or tie-break rule
- evidence merge rule
- contradiction resolution policy

## Recommended Authoring Order

1. Define the typed boundary in `02-agent-contract.yaml`.
2. Define epistemic and generative quality criteria in `02b-quality-criteria.md`.
3. Map dependency edges in `03b-dependency-map.md`.
4. Describe composition behavior in `04-slice-plan.md`.
5. Turn the contract into validators and evaluators in `04b-test-strategy.md`.

## Guidance On DSPy

For `prism_me`, treat DSPy as optional support infrastructure rather than the canonical contract layer.

Good uses:

- evaluator programs for generative quality
- optimization loops for prompt programs
- experimental refinement harnesses

Avoid making DSPy the required surface for:

- core skill contracts
- dependency mapping
- provenance policy
- runtime boundary definition
- Prism workflow composition

Those should stay in Prism-native terms so the external pack can later import cleanly into Prism.

## Optional Aligned Artifacts

`prism_me` now ships these optional aligned artifacts:

- `02f-skill-contract-profile.yaml`
- `02g-composition-model.yaml`

They remain optional so the default external-project workflow stays lightweight, but when they are used they should stay aligned with the current Prism core schema names rather than inventing a parallel dialect.
