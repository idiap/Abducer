<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Prism ME Skill Coverage Checklist

- Request Slug: `<request-slug>`
- Status: `draft`
- Last Updated: ``

## Purpose

Use this checklist to account for every skill in the `prism_me` pack.

Every skill must end up with one clear disposition. Do not leave a row blank at handoff.

## Disposition Rules

- `used`: the skill was invoked directly or its responsibility is embodied in delivered artifacts.
- `not-applicable`: the skill was inspected and intentionally not needed for this request.
- `deferred`: the skill matters, but the work is intentionally postponed.
- `blocked`: the skill is required, but a dependency prevents use right now.
- `stale`: intermediate state only; do not leave a row in this state at handoff.

## Coverage Matrix

| Skill | Disposition | Evidence / Artifact | Notes |
| --- | --- | --- | --- |
| `prism-spec-orchestrator` |  |  |  |
| `prism-spec-intake` |  |  |  |
| `prism-agent-contract-author` |  |  |  |
| `prism-quality-criteria-elicitor` |  |  |  |
| `prism-external-reference-scoper` |  |  |  |
| `prism-external-capability-extractor` |  |  |  |
| `prism-agentic-shape-forger` |  |  |  |
| `prism-repo-cartographer` |  |  |  |
| `prism-dependency-cartographer` |  |  |  |
| `prism-slice-planner` |  |  |  |
| `prism-test-strategy-architect` |  |  |  |
| `prism-implementation-driver` |  |  |  |
| `prism-reflective-refinement-loop` |  |  |  |
| `prism-generative-validation-runner` |  |  |  |
| `prism-persona-review-orchestrator` |  |  |  |
| `prism-epistemologist-review` |  |  |  |
| `prism-mathematician-review` |  |  |  |
| `prism-ai-researcher-review` |  |  |  |
| `prism-software-engineer-review` |  |  |  |
| `prism-spec-verification-critic` |  |  |  |
| `prism-integration-handoff` |  |  |  |

## Reconciliation Rules

- Keep this checklist and the root `to-do.md` in sync.
- Record skipped, deferred, or blocked skills in `reasoning-log.md` when their disposition changes.
- Do not mark the request ready for handoff while any skill row is blank or ambiguous.
