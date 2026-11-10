<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Prism ME Agents Manual

This file is the self-contained operating manual and VSCode entrypoint for the `prism_me` pack.

Use it when you want one place that explains how to apply the whole pack without relying on scattered references or vague invocation hints. It is intentionally redundant with the individual skills. The goal is full control, full inclusion, and no stage being silently skipped or dismissed.

## VSCode Quick Start

For immediate use in a VSCode-based agentic workspace:

1. Open the repository root in VSCode.
2. Read this file first.
3. Run:

```bash
bash prism_me/scripts/init_vscode_onboarding.sh
```

4. Inspect the control stack:

```bash
python3 prism_me/scripts/prism_control.py status
python3 prism_me/scripts/prism_control.py validate
python3 prism_me/scripts/prism_control.py review-complete
```

5. Initialize the request workspace:

```bash
bash prism_me/scripts/init_request.sh <request-slug>
```

6. If the work starts from external code or skills, also run:

```bash
bash prism_me/scripts/init_external_harmonization.sh <request-slug>
```

7. Start with `prism-spec-orchestrator`.

The VSCode onboarding script makes a plain workspace immediately usable by adding a root `AGENTS.md` shim when one does not already exist, starter `.vscode/tasks.json` when the workspace has no tasks yet, a root `to-do.md` planning file when one does not already exist, and repo-local `.codex/` control files for hooks, rules, and config when they do not already exist.

## Purpose

`prism_me` is a Prism-aligned pack for external repositories that need:

- spec-driven development
- typed agent and skill boundaries
- explicit quality criteria
- explicit deterministic and generative test strategy
- reflective refinement during construction
- strong explanatory annotation in Python and Markdown
- concept-first, explanatory, example-rich documentation
- Prism-style dependency mapping
- a root-level `to-do.md` that manages the live plan and active steps
- a request-level skill coverage checklist that accounts for every `prism_me` skill
- a final handoff that can later be translated into Prism onboarding work
- a systematic route for turning external code or skill sets into Prism-shaped agent surfaces

## Core Principles

1. Typed boundaries before prompt prose.
2. Lifecycle stages are explicit and ordered.
3. Durable artifacts are primary; reasoning logs are required sidecars.
4. The root `to-do.md` is the live control surface for the current plan.
5. Explanatory annotation is part of delivery for touched `.py` and `.md`.
6. Quality is not only deterministic or interface-deep; generative and content quality must be made explicit.
7. Reflective refinement is part of construction, not only post-hoc critique.
8. Dependencies must be mapped in Prism terms: `uv` bundles, runtime dependencies, reference KBs, backend profiles, and workspace mounts.
9. External code should be harmonized through explicit scoping, capability extraction, and agentic shape planning.
10. Persona review through the epistemologist, mathematician, AI researcher, and software engineer lenses becomes due every 50 committed edit or write cycles. It remains available on demand and at the final release gate.
11. Documentation should teach concepts, examples, interpretation, and boundaries, not only structure.
12. The full pack must remain usable from this file alone.
13. Every skill in the pack must eventually have a recorded disposition in the coverage checklist.

## Root Control Surfaces

Use these files together:

- `prism_me/agents.md`: self-contained pack manual
- `to-do.md`: live plan, active step tracking, blockers, and completion status
- `.codex/config.toml`: repo-local Codex feature flags and approval hardening
- `.codex/hooks.json`: repo-local lifecycle hook wiring
- `.codex/rules/prism-me.rules`: repo-local escalation rules
- `.prism/<request-slug>/00-skill-coverage-checklist.md`: per-skill disposition ledger
- `.prism/<request-slug>/...`: durable request artifacts

Keep `to-do.md` separate from any existing `TODO.md` or generated maintenance backlog. In this repository, `TODO.md` already serves a different role.
Read `shared/references/codex-control-stack.md` when you need the implementation details behind these control surfaces.

## Skill Type And Composition Layer

When the request needs more formal skill boundaries or workflow semantics, use the discipline in `prism_me/shared/references/skill-type-and-composition-discipline.md`.

For now, `prism_me` expresses the model across the existing artifact set instead of forcing a disruptive new scaffold:

- `02-agent-contract.yaml`: typed boundary, invocation, ports, coordination
- `02b-quality-criteria.md`: admissible claims, confidence and uncertainty behavior, provenance expectations, validators and evaluators
- `03b-dependency-map.md`: upstream and downstream dependencies in Prism terms
- `04-slice-plan.md`: sequence, branching, refinement, judge, delegation, aggregation, contradiction handling
- `04b-test-strategy.md`: deterministic and generative validation plus reflective refinement loops

When you want a direct mirror for the upcoming Prism core model, use these optional templates:

- `02f-skill-contract-profile.yaml`
- `02g-composition-model.yaml`

These live in `shared/templates/` and stay optional unless a request explicitly needs them.

## Required Workspace

For one request, use `.prism/<request-slug>/` with these artifacts:

1. `01-spec.md`
2. `02-agent-contract.yaml`
3. `02b-quality-criteria.md`
4. `03-repo-map.md`
5. `03b-dependency-map.md`
6. `04-slice-plan.md`
7. `04b-test-strategy.md`
8. `05-execution-log.md`
9. `05b-refinement-loop.md`
10. `05c-test-evidence.md`
11. `05d-persona-review.md`
12. `06-verification.md`
13. `07-handoff.md`
14. `reasoning-log.md`

If the work starts from external code or skills, add:

1. `02c-external-surface.md`
2. `02d-external-capabilities.md`
3. `02e-agentic-shape.md`

At the repository root, also keep:

- `to-do.md`

Bootstrap the base workspace with:

```bash
bash prism_me/scripts/init_request.sh <request-slug>
```

Add the external-harmonization artifacts with:

```bash
bash prism_me/scripts/init_external_harmonization.sh <request-slug>
```

## Full Skill Set

### 1. `prism-spec-orchestrator`

Use as the top-level coordinator.

Responsibilities:

- resolve the current stage
- route to the earliest missing or stale artifact
- sync the root `to-do.md` with the real stage, next step, and blockers
- enforce stage gates
- prevent silent skipping of quality, dependency, and refinement work
- route through the external-harmonization lane when the source is outside Prism
- keep the skill coverage checklist reconciled as routing changes

### 2. `prism-spec-intake`

Turns a request into a real spec packet.

Must clarify:

- desired outcome
- scope
- constraints
- acceptance evidence
- assumptions and unknowns
- whether generative quality criteria will be needed
- whether the request starts from external code or skills

### 3. `prism-agent-contract-author`

Authors the Prism-style typed contract.

Must make explicit:

- invocation mode
- typed inputs and outputs
- coordination role
- runtime boundaries
- reasoning-log expectations

### 4. `prism-quality-criteria-elicitor`

Defines the quality bar for the capability under construction.

It must cover both:

- deterministic and interface-side quality
- generative and content-side quality

The generative side should usually dominate the packet when the work involves skill behavior, prompt behavior, synthesis quality, explanation quality, or interpretive output.

The criteria packet should include:

- evaluation dimensions
- success signals
- failure signals
- test probes
- pass or conditional thresholds
- likely improvement targets

### External Harmonization Skills

These are the skills to use when the request starts from outside code, outside skills, or a preserved upstream runtime.

#### `prism-external-reference-scoper`

Builds a trustworthy map of the external source.

It captures:

- provenance
- preserved paths
- scripts and docs
- runtime truth
- preserved assets
- dependency signals that later need Prism-style mapping

#### `prism-external-capability-extractor`

Turns the external surface into candidate Prism-facing capabilities.

It captures:

- what the external code can really do
- where the capability boundaries are
- which capabilities should split or stay bundled
- what should remain external-only
- which dependency classes each capability actually relies on

#### `prism-agentic-shape-forger`

Delivers the Prism agentic shape for the extracted capabilities.

It defines:

- candidate agent surfaces
- organization group
- lifecycle stage
- role
- entrypoints
- semantic folder
- runtime adapter notes
- reasoning-log expectations
- bundle, backend, KB, and mount notes needed later

### 5. `prism-repo-cartographer`

Maps the current repo against the spec, contract, and quality packet.

It should identify:

- reusable code and docs
- risky surfaces
- narrow touch set
- annotation gaps
- documentation gaps and missing examples
- existing tests, examples, prompts, or evaluations that can feed refinement
- candidate dependency surfaces that the dependency map must formalize

### 6. `prism-dependency-cartographer`

Maps dependencies according to Prism's own management model.

It should identify:

- `uv` bundles already available or still needed
- runtime dependencies and setup surfaces
- reference KBs and their checks
- backend profiles and invocation dependencies
- workspace mounts, route registries, and capability source paths
- hidden, inferred, or fragile dependencies that could break planning or onboarding

### 7. `prism-slice-planner`

Builds the execution plan.

The plan must include:

- dependency-ordered slices
- validation surfaces
- annotation work for touched `.py` and `.md`
- documentation work when features, workflows, or outputs change materially
- explicit ties back to the root `to-do.md`
- at least one explicit reflective refinement slice or sub-slice when the work is generative

### 8. `prism-test-strategy-architect`

Builds the testing architecture.

It must define:

- deterministic test matrix
- generative test matrix
- dependency-sensitive test setup and assumptions
- Codex validation protocol
- content-quality oracles
- failure-to-regression rules
- coverage and exit criteria

### 9. `prism-implementation-driver`

Executes one slice at a time.

During execution:

- make the smallest coherent change
- improve explanatory annotation in touched Python and Markdown files
- improve documentation so it explains concepts, examples, and interpretation rather than only structure
- author or update the real test surfaces promised by the test strategy
- keep the quality criteria and dependency map visible during construction
- update the root `to-do.md` as work moves between todo, active, done, or deferred
- record tests, deviations, and debt

### 10. `prism-reflective-refinement-loop`

Runs iterative quality improvement against the criteria packet.

Default expectation:

- at least two cycles once a meaningful draft exists

Each cycle must do all of the following:

1. test the current draft against explicit criteria
2. localize concrete weaknesses
3. apply targeted revisions
4. re-test and record whether the weaknesses improved

Do not reduce this to generic commentary. The point is systematic localization and repair.

### 11. `prism-generative-validation-runner`

Runs the testing strategy and records evidence.

It must capture:

- deterministic test results
- generative probe results
- expected versus observed outcomes
- failure clusters
- conversion of important failures into repeatable tests

### 12. `prism-spec-verification-critic`

Acts as the release gate.

It must inspect:

- spec fit
- contract fit
- dependency fit
- annotation quality
- documentation quality
- deterministic criteria satisfaction
- generative criteria satisfaction
- deterministic test depth
- generative test depth
- whether the reflective loop was real and meaningful
- whether the root `to-do.md` is reconciled with the delivered state

### 13. `prism-integration-handoff`

Packages the finished result for future Prism onboarding.

It must summarize:

- delivered outcome
- artifact map
- dependency trace
- annotation coverage
- quality criteria and refinement trace
- testing trace
- documentation trace
- Prism onboarding translation
- remaining debt
- unresolved or deferred `to-do.md` items

## Stage Order

Apply the pack in this order unless an earlier artifact already exists and is still valid:

1. Spec
2. Contract
3. Quality criteria
4. Repo map
5. Dependency map
6. Slice plan
7. Test strategy
8. Execution
9. Reflective refinement
10. Test evidence
11. Verification
12. Handoff

For external-source requests, run the external harmonization lane as soon as you have a first usable spec and before you finalize downstream contract, dependency, and implementation decisions:

1. External source scoping
2. External capability extraction
3. Agentic shape delivery

If an earlier artifact changes materially, later artifacts become stale and should be revisited.

## To-Do Guidance

Use `to-do.md` to manage and deliver the plan at the repository root.

The file should always show:

- the active request slug
- the current stage
- the next gate
- the active skill
- the skill coverage checklist path and its current reconciliation state
- the checklist derived from the slice plan
- the evidence links that justify marked-done items
- blockers and deferred work

The to-do file is not a replacement for the numbered artifacts. It is the coordination surface that keeps the plan alive between them.

## Dependency Mapping Guidance

Do not reduce dependencies to package names.

For skill and agent construction, map dependencies across these Prism-shaped classes:

- `uv` bundles
- runtime dependencies
- reference KBs
- backend profiles
- workspace mounts
- route registries
- capability source paths
- dependency edges into slices, tests, docs, and handoff

Use realistic evidence such as paths, config, commands, dry runs, and availability checks.

If relevant in the local Prism repo, these commands are good discovery surfaces:

```bash
python -m uv run prism uv status
python -m uv run prism uv sync --all --dry-run
```

## Quality Criteria Guidance

Do not stop at interface neatness.

For skill and agent construction, evaluate content quality on dimensions like:

- conceptual clarity
- intent fidelity
- epistemic discipline
- coverage
- specificity
- actionability
- differentiation from neighboring skills
- failure-mode awareness
- explanatory richness
- revision usefulness

Use realistic probes, not toy checks.

## Testing Guidance

This pack assumes a Codex-style environment where testing is partly generated and partly executed.

The testing surface should combine:

- deterministic tests
- regression tests
- invariant checks
- adversarial probes
- ambiguity probes
- content-quality validation
- dependency-sensitive setup checks
- failure-to-regression conversion

Generative tests must still be anchored in:

- the spec
- the quality packet
- explicit expected outcomes
- known invariants

Do not let the model grade itself without a stated oracle.

## Reflective Refinement Guidance

This pack treats refinement as a build-time discipline.

Minimum loop:

1. produce a meaningful draft
2. test it against the quality criteria
3. localize weak points
4. revise
5. test again
6. run one more cycle if meaningful weaknesses remain

The refinement artifact should capture:

- cycles run
- probes used
- localized weaknesses
- targeted changes
- current verdict

## External Harmonization Guidance

When starting from outside code or skills:

1. scope the source truthfully
2. extract real capabilities
3. define the Prism agentic shape
4. map the dependency picture in Prism terms
5. only then finalize downstream contract, planning, and implementation choices

Do not flatten preserved runtimes into fake native abstractions too early.

## Annotation Guidance

When touching Python files:

- explain the module's core concept and role
- explain why classes and functions exist
- add block comments before non-obvious logic

When touching Markdown files:

- explain the document's purpose
- explain who it is for
- frame sections so a new agent can use them

The goal is not decorative comment volume. The goal is legibility for future agents.

## Documentation Guidance

Documentation in this pack should be:

- concept-first
- explanatory
- concrete
- rich in examples
- useful without the surrounding chat history

Good docs should explain:

- why the thing exists
- the mental model behind it
- how it fits the workflow
- how to interpret outputs
- what a realistic example looks like
- what can go wrong

## Control Rules

Do not silently dismiss these skills or compress them into one blurred stage.

Specifically:

- do not skip quality criteria for generative work
- do not skip explicit deterministic and generative testing for generative work
- do not skip reflective refinement once a draft exists
- do not skip annotation improvements for touched `.py` or `.md`
- do not leave documentation as a thin structural shell when the work changes concepts, workflows, or outputs
- do not skip dependency mapping when runtime, backend, KB, bundle, or mount assumptions matter
- do not let `to-do.md` drift away from the real slice plan and delivered evidence
- do not skip verification because implementation felt plausible
- do not skip external scoping and shaping when the source is outside Prism
- do not treat handoff as a casual summary
- do not leave any `prism_me` skill without a recorded disposition
- do not let the root `to-do.md` and the skill coverage checklist disagree about active, deferred, blocked, or used work

If a stage is intentionally skipped, the reason must be written explicitly in the relevant artifact, in `reasoning-log.md`, and in `to-do.md` when it changes the live plan.

## Minimal Routing Table

- missing `01-spec.md` -> `prism-spec-intake`
- external source present and missing `02c-external-surface.md` -> `prism-external-reference-scoper`
- external surface present and missing `02d-external-capabilities.md` -> `prism-external-capability-extractor`
- external capabilities present and missing `02e-agentic-shape.md` -> `prism-agentic-shape-forger`
- missing `02-agent-contract.yaml` -> `prism-agent-contract-author`
- missing `02b-quality-criteria.md` -> `prism-quality-criteria-elicitor`
- missing `03-repo-map.md` -> `prism-repo-cartographer`
- missing `03b-dependency-map.md` -> `prism-dependency-cartographer`
- missing `04-slice-plan.md` -> `prism-slice-planner`
- missing `04b-test-strategy.md` -> `prism-test-strategy-architect`
- missing `05-execution-log.md` -> `prism-implementation-driver`
- missing or weak `05b-refinement-loop.md` -> `prism-reflective-refinement-loop`
- missing `05c-test-evidence.md` -> `prism-generative-validation-runner`
- missing `06-verification.md` -> `prism-spec-verification-critic`
- missing `07-handoff.md` -> `prism-integration-handoff`

## Final Standard

The pack is being used correctly when another agent can open `prism_me/agents.md`, inspect `to-do.md`, inspect the request workspace, and continue the work with minimal guessing about:

- what the capability is
- what quality means
- what dependencies exist and how they are managed
- what got refined
- what evidence exists
- how outside code was shaped into Prism form
- what still needs attention
