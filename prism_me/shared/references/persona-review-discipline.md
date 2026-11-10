<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Persona Review Discipline

Use the persona-review lane to force deliberate perspective changes during Prism execution work.

## Trigger

The Prism control stack counts edit and write code-generation cycles.

When the active request accumulates 50 new edit or write cycles since the last completed persona review, the control stack marks persona review due. This sparse automatic cadence is a drift checkpoint, not a ban on earlier review: the lane remains available on demand and is still required at the final release gate.

At that point:

1. Route to `prism-persona-review-orchestrator`.
2. Update `.prism/<request-slug>/05d-persona-review.md`.
3. Sync the persona-review control fields in `to-do.md`.
4. Treat the generated TODOs as first-class plan inputs.
5. Mark the review complete with `python3 prism_me/scripts/prism_control.py review-complete`.

## Personas

### Epistemologist

Focus on:

- claim-to-evidence fit
- hidden assumptions
- overconfident inference
- weak falsification posture
- missing boundary conditions

### Mathematician

Focus on:

- internal consistency
- precise definitions
- unstated invariants
- edge cases
- quantitative, complexity, or convergence claims

### AI Researcher

Focus on:

- benchmark and baseline discipline
- experimental validity
- ablation quality
- generalization claims
- literature positioning

### Software Engineer

Focus on:

- architecture and dependency integrity
- test depth and regression protection
- maintainability and readability
- operational safety
- developer workflow and documentation quality

## Output Discipline

The persona-review lane must produce:

- explicit findings for each persona
- explicit nulls when a persona has no material concern
- a consolidated TODO queue
- a short gate decision on whether implementation can proceed

Do not let persona review collapse into vague praise, generic "looks good" language, or a single blended paragraph.
