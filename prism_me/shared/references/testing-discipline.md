<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Testing Discipline

Use this guide when a request needs systematic testing in a Codex-style agentic environment.

The aim is not only to add a few deterministic checks. The aim is to generate a strong testing surface that combines:

- deterministic tests
- property and invariant checks
- regression tests
- generative validation
- content-quality probes
- failure-driven test expansion

## Core Principle

Testing should be broad enough to verify both:

1. interface and deterministic behavior
2. content, interpretation, and expected outcomes

If the capability generates prose, plans, explanations, classifications, summaries, prompts, or agent instructions, then deterministic tests alone are not enough.

## Deterministic Testing

Always look for opportunities to add:

- unit tests
- integration tests
- regression tests
- schema or contract tests
- invariant checks
- file-layout or artifact-shape checks

These should anchor the stable parts of behavior.

## Generative Testing

In a Codex-style environment, generative testing means using the agent to systematically create and run probes against the intended behavior.

Good generative testing includes:

- prompt or input variation
- adversarial or ambiguous probes
- edge-case synthesis
- content-quality evaluation against explicit criteria
- expected-outcome verification against the spec and quality packet
- consistency checks across paraphrases, perturbations, and near-neighbor cases

## Oracles

Generative testing still needs an oracle.

Anchor the oracle in:

- the spec packet
- the quality-criteria packet
- explicit expected outcomes
- known invariants
- concrete failure patterns

Do not use pure vibes as the judge.

## Codex Validation Workflow

1. Define the target behavior and the expected outcome.
2. Generate deterministic tests for stable behavior.
3. Generate probe families for generative behavior.
4. Run the probes and record outcomes.
5. Localize failure patterns.
6. Convert important failures into new regression tests, deterministic checks, or repeatable generative probes.
7. Re-run after fixes.

## Good Generative Probe Families

- paraphrase families
- hostile or adversarial inputs
- boundary-condition inputs
- incomplete-information prompts
- misleading-context prompts
- variation in tone, verbosity, or framing
- counterexample-seeking probes
- rubric-based content audits

## Required Evidence

A good testing packet should record:

- what was tested
- how it was tested
- what the expected outcome was
- what actually happened
- which failures became new tests
- what still remains weak

## Workflow Impact

- `prism-repo-cartographer` should identify existing test harnesses and testing gaps.
- `prism-test-strategy-architect` should define the deterministic and generative test matrix.
- `prism-implementation-driver` should generate or update actual tests and test harnesses, not just talk about them.
- `prism-generative-validation-runner` should run Codex-style validation and record evidence.
- `prism-reflective-refinement-loop` should use test evidence to localize and repair weaknesses.
- `prism-spec-verification-critic` should audit testing depth, not only feature completion.
