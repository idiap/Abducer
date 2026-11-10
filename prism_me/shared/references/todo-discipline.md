<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# To-Do Discipline

Use the root `to-do.md` file as the live planning and delivery control surface for Prism ME work in a repository.

This file is intentionally different from any existing `TODO.md`, backlog export, or maintenance queue. In this repository, `TODO.md` already serves a separate maintenance purpose. Keep `to-do.md` focused on the current Prism ME delivery plan.

## Goal

Make the active plan visible at the repository root so another agent can understand:

- what request is active
- what stage it is in
- what the next concrete steps are
- what evidence already exists
- what is blocked, deferred, or still unfinished

## What Belongs In `to-do.md`

Keep the file short, current, and execution-facing.

Record:

- the active request slug
- the goal in one or two concrete sentences
- the current stage
- the next gate
- the active coordinating skill
- the skill coverage checklist path and its current reconciliation state
- the ordered checklist derived from the slice plan
- evidence links back to `.prism/<request-slug>/` artifacts
- blockers, deferred work, and follow-ups

## Relationship To Other Artifacts

Use the files this way:

- `to-do.md`: root control surface for plan and status
- `04-slice-plan.md`: durable planning artifact with dependency-ordered slices
- `05-execution-log.md`: evidence of work actually performed
- `00-skill-coverage-checklist.md`: per-skill disposition ledger
- `06-verification.md`: release-gate critique
- `07-handoff.md`: final delivery and adoption summary

The root to-do is the steering wheel. The numbered artifacts are the durable evidence surfaces.

## Operating Rules

1. Keep one clearly marked block per active request slug.
2. Update `to-do.md` when the plan changes, when the active slice changes, and when work moves to done, blocked, or deferred.
3. Make checklist items concrete enough that another agent can continue the work without guessing.
4. Link items to artifacts, files, or evidence whenever possible.
5. Do not mark an item done until there is evidence in code, docs, tests, or artifacts.
6. Before handoff, reconcile every unchecked item: finish it, defer it explicitly, or explain why it is out of scope.
7. Before handoff, reconcile every skill row in the coverage checklist: mark it used, not-applicable, deferred, or blocked, with evidence or rationale.

## Recommended Shape

Use these sections:

- `Current Request`
- `Plan`
- `Evidence Links`
- `Blockers And Deferred Work`
- `Completed Notes`

## Guardrails

- Do not turn `to-do.md` into a second full specification.
- Do not let the checklist drift away from the slice plan.
- Do not hide blockers in chat only; record them in the file.
- Do not mix repo-maintenance backlog items into this file unless they are part of the current Prism ME delivery.
