---
name: project-readme-concept-builder
description: Build or refresh the evidence-grounded conceptual center of a repository README. Use when the public project promise, differentiator, audience, architecture summary, trust boundary, or explanation of what the system actually does has changed or become obscured by implementation detail.
---

# Project README Concept Builder

Build the front-door explanation of a project from repository evidence. Own the README's conceptual center; do not turn it into an internal architecture inventory.

## Read First

1. Read the [root project overview](../../README.md) and the [documentation index](../../docs/README.md).
2. Read the repository coordination contract and package metadata.
3. Read the smallest concept document that explains the current system.
4. Inspect the executable entrypoint and one representative emitted result.
5. Read [concept evidence questions](references/concept-evidence-questions.md) when the project identity or claim boundary is unclear.

## Build The Concept

1. State the project in one sentence: user, input, transformation, and useful outcome.
2. Name the central problem it solves without comparing feature counts.
3. Explain the system with three to five reasoning moves that a reader can retain.
4. State the trust boundary beside the promise. Separate generated output, validation evidence, and signoff evidence.
5. Select only the capabilities needed to support the concept. Delegate exhaustive detail to linked guides and references.
6. Check every public claim against code, configuration, a test, or an emitted artifact.

## Handoff

Leave a compact concept packet for `$project-readme-orchestrator` containing:

- one-sentence promise
- primary users and jobs
- conceptual reasoning sequence
- differentiator
- trust and evidence boundary
- source anchors for each material claim
- details that should move one click deeper

The packet may be a short working note or a structured object. Do not create a permanent artifact unless the repository workflow requires one.

## Quality Bar

- Lead with what the project enables, not its directory structure.
- Prefer concrete verification language over agent-framework vocabulary.
- Make the conceptual model intelligible before installation.
- Keep the opening useful to both a verification engineer and a researcher.
- Do not imply formal closure, simulator fidelity, or production readiness without matching evidence.
