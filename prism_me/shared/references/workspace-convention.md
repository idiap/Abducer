<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Workspace Convention

The default workspace for one request is `.prism/<request-slug>/`.

At the repository root, keep a live `to-do.md` file for stage and step tracking.

## Required Files

- `01-spec.md`
- `02-agent-contract.yaml`
- `02b-quality-criteria.md`
- `03-repo-map.md`
- `03b-dependency-map.md`
- `04-slice-plan.md`
- `04b-test-strategy.md`
- `05-execution-log.md`
- `05b-refinement-loop.md`
- `05c-test-evidence.md`
- `06-verification.md`
- `07-handoff.md`
- `reasoning-log.md`
- `00-skill-coverage-checklist.md`

## Operating Rules

1. Keep one request per slug.
2. Update existing artifacts instead of rewriting them from scratch unless the framing genuinely changed.
3. Numbered artifacts are the primary surface. `reasoning-log.md` is the sidecar surface.
4. `to-do.md` is the live control surface for the current plan, active slice, blockers, and deferred work.
5. Use repo-relative file paths inside artifacts whenever you cite code, scripts, docs, or tests.
6. Use `03b-dependency-map.md` as the canonical place to map Prism-style dependencies such as bundle ids, runtime dependencies, reference KBs, backend profiles, and workspace mounts.
7. Use `00-skill-coverage-checklist.md` as the canonical place to account for every `prism_me` skill disposition.
8. If the external project already has its own folder conventions, keep a mapping table in the handoff artifact instead of silently changing paths.

## Minimal Stage Order

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

Skipping a stage is allowed only when an existing artifact already satisfies the same contract.
