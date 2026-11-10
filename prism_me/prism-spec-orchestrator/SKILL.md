---
name: prism-spec-orchestrator
description: Coordinate Prism-style spec-driven agentic development in an external repository. Use when a request should move through spec intake, external harmonization when needed, typed contract authoring, repo mapping, dependency mapping, slice planning, execution, verification, and a final Prism-ready handoff under `.prism/<request-slug>/`.
---

# Prism Spec Orchestrator

Use this as the entrypoint skill for the `prism_me` pack.

Read these first:

- [../agents.md](../agents.md)
- [../shared/references/prism-alignment.md](../shared/references/prism-alignment.md)
- [../shared/references/persona-review-discipline.md](../shared/references/persona-review-discipline.md)
- [../shared/references/annotation-discipline.md](../shared/references/annotation-discipline.md)
- [../shared/references/dependency-discipline.md](../shared/references/dependency-discipline.md)
- [../shared/references/documentation-discipline.md](../shared/references/documentation-discipline.md)
- [../shared/references/external-harmonization.md](../shared/references/external-harmonization.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/references/testing-discipline.md](../shared/references/testing-discipline.md)
- [../shared/references/todo-discipline.md](../shared/references/todo-discipline.md)
- [../shared/references/workspace-convention.md](../shared/references/workspace-convention.md)
- [../shared/references/release-gates.md](../shared/references/release-gates.md)
- [../skill-pack.yaml](../skill-pack.yaml)

If the request workspace does not exist yet, create it with:

```bash
bash prism_me/scripts/init_request.sh <request-slug>
```

## Routing Order

Route to the earliest missing or stale artifact:

1. `01-spec.md` -> `prism-spec-intake`
2. external-source requests: `02c-external-surface.md` -> `prism-external-reference-scoper`
3. external-source requests: `02d-external-capabilities.md` -> `prism-external-capability-extractor`
4. external-source requests: `02e-agentic-shape.md` -> `prism-agentic-shape-forger`
5. `02-agent-contract.yaml` -> `prism-agent-contract-author`
6. `02b-quality-criteria.md` -> `prism-quality-criteria-elicitor`
7. `03-repo-map.md` -> `prism-repo-cartographer`
8. `03b-dependency-map.md` -> `prism-dependency-cartographer`
9. `04-slice-plan.md` -> `prism-slice-planner`
10. `04b-test-strategy.md` -> `prism-test-strategy-architect`
11. `05-execution-log.md` -> `prism-implementation-driver`
12. `05b-refinement-loop.md` -> `prism-reflective-refinement-loop`
13. `05c-test-evidence.md` -> `prism-generative-validation-runner`
14. review-due state or `05d-persona-review.md` refresh -> `prism-persona-review-orchestrator`
15. `06-verification.md` -> `prism-spec-verification-critic`
16. `07-handoff.md` -> `prism-integration-handoff`

Update `reasoning-log.md` after every stage.

## Workflow

1. Resolve the request slug and workspace path.
2. Check whether earlier artifacts became stale after later discovery.
3. Sync `to-do.md` with the active request, current stage, next skill, and blockers.
4. Sync `.prism/<request-slug>/00-skill-coverage-checklist.md` alongside `to-do.md` so every `prism_me` skill has a disposition.
5. Route only to the minimum next skill needed to restore a valid stage order.
6. Enforce the gate for the current stage before advancing.
7. Prefer small, auditable progress over broad, multi-stage improvisation.
8. Stop and surface blockers if a required upstream artifact is missing or contradicted.
9. If the work touches `.py` or `.md`, ensure annotation work is planned, executed, and verified as part of the stage flow.
10. When building skills or agents, ensure quality criteria are defined early and reflective refinement loops run before final verification.
11. When the source starts outside Prism, route through scoping, capability extraction, and agentic-shape delivery before deeper contract or bundle decisions.
12. Ensure dependency mapping becomes explicit before planning and execution: bundles, runtimes, KBs, backends, mounts, and source paths.
13. Ensure testing becomes explicit as a stage: deterministic matrix, generative matrix, executed evidence, and failure-to-regression conversion.
14. Ensure documentation work is explicit whenever the capability, workflow, or outputs need concept-first explanation and examples.
15. When the control stack reports a due persona review after 50 committed edit or write cycles, route through `prism-persona-review-orchestrator` before more implementation drift accumulates. The lane remains available on demand and is retained at the final release gate.

## Guardrails

- Do not treat polished prose as a substitute for typed contracts.
- Do not skip straight to implementation unless earlier artifacts already satisfy the same contract.
- If the spec changes materially, mark downstream artifacts stale and revisit them.
- If the dependency picture changes materially, mark the slice plan, test strategy, verification, and handoff artifacts stale and revisit them.
- Keep provenance explicit when a stage depends on external scripts, services, or preserved runtimes.
- Keep `to-do.md` aligned with the numbered artifacts so the live plan stays trustworthy.
- Keep the skill coverage checklist aligned with `to-do.md` so every pack skill has an explicit disposition.
- Keep the persona-review control fields in `to-do.md` aligned with the real edit-cycle state and review status.
- Treat `reasoning-log.md` as required sidecar output, never as the primary artifact.
- Treat explanatory annotation as part of the deliverable for touched Python and Markdown files.
- Treat `agents.md` as a required, self-contained control surface for applying the pack end to end.
- Do not let a skill remain unaccounted for in `.prism/<request-slug>/00-skill-coverage-checklist.md`.

## Output Contract

Return a short orchestration status that names:

- current stage
- artifact touched or required next
- coverage disposition status
- gate status
- blocker, if any
- next skill to invoke
