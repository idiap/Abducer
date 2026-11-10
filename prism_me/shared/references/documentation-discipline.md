<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Documentation Discipline

Use this guide when a request creates, revises, or depends on documentation.

The goal is not to produce thin structural notes or directory tours. The goal is to build documentation that helps a new agent or engineer understand:

- the core concept
- the purpose of the capability
- the mental model behind the workflow
- how to interpret outputs
- what concrete examples look like
- what decisions, risks, and boundaries matter

## What Good Documentation Should Feel Like

Good documentation should be:

- concept-driven
- explanatory
- example-rich
- concrete
- operationally useful
- readable as onboarding material

It should not be limited to:

- file structure listings
- connection diagrams without explanation
- abstract bullet piles
- references to components without telling the reader why they matter

## Preferred Documentation Shape

When writing substantial documentation, prefer this general flow:

1. Purpose
   Explain what the document is for and why it exists.

2. Core concept
   Explain the underlying idea or mental model in plain language.

3. Where it fits
   Explain how the documented thing sits in the larger workflow or architecture.

4. Concrete examples
   Show one or more realistic examples, not only abstract placeholders.

5. Operational guidance
   Explain how to use, extend, test, or troubleshoot the thing in practice.

6. Boundaries and risks
   Explain failure modes, constraints, and what should not be assumed.

## Example Expectations

Examples should be:

- plausible
- close to real usage
- short enough to scan
- rich enough to teach something

Prefer:

- before and after examples
- good versus weak examples
- typical flows
- edge-case examples when they clarify the concept

## Documentation Questions To Answer

Most substantive docs should answer many of these:

1. What concept is this document trying to teach?
2. Why does this capability, workflow, or artifact exist?
3. What should the reader understand before acting on it?
4. What does a concrete good example look like?
5. How should the reader interpret the outputs or next steps?
6. What are the important limits, edge cases, or failure modes?

## For Markdown Specifically

When editing `.md` files:

- open with purpose, not just headings
- add section introductions where the purpose might be unclear
- include at least one concrete example when the document explains a workflow, skill, or artifact
- explain outputs, not only steps
- make the document usable without requiring chat history

## Workflow Impact

- `prism-repo-cartographer` should identify weak documentation surfaces and missing examples.
- `prism-slice-planner` should allocate explicit documentation work when understanding is thin.
- `prism-implementation-driver` should improve documentation when the feature, workflow, or artifact changed materially.
- `prism-spec-verification-critic` should check that documentation became more explanatory, example-rich, and concrete.
- `prism-integration-handoff` should record documentation updates and remaining documentation debt.
