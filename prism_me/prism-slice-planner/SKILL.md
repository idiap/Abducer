---
name: prism-slice-planner
description: Turn a Prism-style spec, contract, and repo map into an ordered execution plan. Use when work must be decomposed into implementation slices with dependencies, file touch expectations, validation steps, exit criteria, and rejected alternatives instead of a flat checklist.
---

# Prism Slice Planner

This skill converts the request into an execution graph.

Read:

- [../agents.md](../agents.md)
- [../shared/references/annotation-discipline.md](../shared/references/annotation-discipline.md)
- [../shared/references/dependency-discipline.md](../shared/references/dependency-discipline.md)
- [../shared/references/documentation-discipline.md](../shared/references/documentation-discipline.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/references/testing-discipline.md](../shared/references/testing-discipline.md)
- [../shared/references/todo-discipline.md](../shared/references/todo-discipline.md)
- [../shared/references/release-gates.md](../shared/references/release-gates.md)
- [../shared/templates/04-slice-plan.md](../shared/templates/04-slice-plan.md)
- [../shared/templates/02g-composition-model.yaml](../shared/templates/02g-composition-model.yaml)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)
- `.prism/<request-slug>/01-spec.md`
- `.prism/<request-slug>/02-agent-contract.yaml`
- `.prism/<request-slug>/02b-quality-criteria.md`
- `.prism/<request-slug>/03-repo-map.md`
- `.prism/<request-slug>/03b-dependency-map.md`

## Workflow

1. Read the spec, contract, quality criteria, repo map, and dependency map together.
2. Identify the shortest path to the acceptance evidence.
3. Decompose the work into ordered slices with real dependencies, including dependency provisioning or verification steps when the work relies on bundles, KBs, backends, or workspace shape.
4. Include at least one slice or sub-slice for applying the quality criteria and running reflective refinement.
5. For each slice, state intent, dependencies consumed or changed, files touched, annotation work for touched `.py` and `.md` files, tests or checks, exit criteria, and follow-up debt.
6. Decide whether the request needs an explicit composition policy; if yes, write or update `.prism/<request-slug>/02g-composition-model.yaml` using the current `WorkflowCompositionPolicySpec` field names, and if no, record the explicit not-applicable reason in `.prism/<request-slug>/reasoning-log.md`.
7. Update `to-do.md` so the active plan mirrors the slice graph in a compact, execution-friendly checklist.
8. Make sure the plan leaves room for deterministic test generation, generative validation, and dependency-sensitive checks rather than treating them as last-minute checks.
9. Make sure the plan leaves room for documentation work when the change introduces or materially alters concepts, workflows, outputs, or user understanding.
10. Record rejected alternatives so later reviewers can see why the route was chosen.
11. Define the release gate for entering execution.
12. Write or update `.prism/<request-slug>/04-slice-plan.md`.
13. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Do not emit a flat checklist that hides dependency order.
- Do not let a slice rely on hidden dependency setup.
- Do not let `to-do.md` drift away from the approved slice plan.
- If the request warrants `02g-composition-model.yaml`, keep the policy object aligned to the current rover schema directly: `kind`, `condition`, `branch_targets`, `max_iterations`, `exit_when`, `iteration_input`, `delegate_to`, `aggregation_sources`, `aggregation_mode`, `contradiction_resolution`, `judge_role`, and `notes`.
- Every slice needs a validation surface.
- Separate current-scope work from deferred debt.
- If a slice cannot be explained in terms of existing artifacts, the earlier stages are not ready.
- If the slice touches Python or Markdown, include explicit annotation work unless the file is already clearly explanatory.
- If the work is generative or content-heavy, the plan should allocate time for at least two reflective refinement cycles.
- If the work is generative or content-heavy, the plan should also allocate time for explicit generative validation and follow-on regression creation.
- If the work changes behavior that humans or downstream agents need to understand, allocate documentation work explicitly instead of hoping the structure speaks for itself.

## Output Contract

Produce a slice plan with:

- planning summary
- dependency-ordered slice graph
- dependency-sensitive setup notes
- root to-do alignment
- per-slice detail
- rejected alternatives
- execution entry gate
