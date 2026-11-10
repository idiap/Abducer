---
name: orch
description: Dynamically select, sequence, and reassess registered reasoning capabilities against a structured goal, current epistemic state, critic criteria, budgets, and observed outputs. Use when a user invokes `orch`, requests adaptive orchestration, or needs an orchestration agent to choose the next reasoning type and concrete skill rather than follow a fixed route.
---

# Orch

Orchestrate at the reasoning-type level, then use `$route` to bind each chosen
occurrence to a concrete skill. Reassess after every material output.

## Procedure

1. Freeze the structured goal, critic criteria, evidence obligations,
   constraints, KB references, budgets, and stop conditions.
2. Load the reasoning namespace from
   `agentic/registries/essential_reasoning_types.yaml` and the live skill
   namespace from `agentic/registries/skill_registry.yaml`.
3. Describe the current epistemic deficit without naming a preferred skill.
4. Select the next reasoning type using
   [references/selection-policy.md](references/selection-policy.md).
5. Query compatible materializers with `scripts/list_capabilities.py`. Select
   among that filtered set using prerequisites, domain fit, input/output
   compatibility, and child-contract authority; availability alone is not a
   reason to invoke a skill.
6. Materialize the decision as a minimal `.prism` occurrence or bounded
   subprogram, including an explicit binding when the default route is not the
   best compatible materializer.
7. Delegate rigid binding to `$route`; never bypass its mapping checks.
8. Invoke the bound skill, ingest its typed output, update goal-criterion
   dispositions and open obligations, then decide whether to continue,
   branch, switch, calibrate, or stop.
9. Require evidential status calibration before acceptance or workflow switch.

## Guardrails

- Do not orchestrate directly over skill names before selecting a reasoning
  type; capability availability must not determine epistemic need.
- Do not repeat an unchanged reasoning move without a new input, state delta,
  or explicit recovery hypothesis.
- Keep iteration bounded and expose budget consumption.
- Do not silently discard alternatives, defeaters, failed attempts, or critic
  criteria.
- Do not let orchestration success increase claim authority.
- Use `$route` when the sequence is already fixed.
- Preserve the orchestration invariants: type-before-skill selection, no
  execution without a valid route receipt, bounded iteration, and calibration
  before acceptance or workflow switching.

## Epistemic Discipline

An orchestration choice is a Plan or Decision, not object-level Evidence.
Record why the selected reasoning type addresses the current deficit, which
source artifacts or KB IDs support that diagnosis, and which explicit unknowns
remain. Preserve each child result's epistemic status and force demotion when
critic findings or failed criteria warrant it.

## Output Contract

Return:

- `mode: orch`;
- structured goal and current criterion dispositions;
- current epistemic-state summary;
- chosen reasoning type and justification;
- `$route` binding receipt for the concrete skill;
- bounded budget and iteration counters;
- observed output, state delta, and preserved open obligations;
- next action: continue, branch, switch, calibrate, accept, quarantine, or stop;
- validation handoff and unresolved obligations.

## Failure/Demotion

Quarantine or stop on capability gaps, repeated no-delta cycles, exhausted
budgets, contradictory criteria, missing evidence, or route-binding failure.
Demote any recommendation whose justification relies on skill availability
rather than the goal's epistemic deficit.

## Codex Exec Protocol

Use deterministic commands only for namespace inspection and `$route`
compilation. Keep reasoning-type selection generative and reviewable. Record
executed commands, inspected artifacts, selected registry rows, and the route
receipt. Validate the two skills together with the focused orchestration tests.

```bash
python skills/orchestration/orch/scripts/list_capabilities.py \
  abductive_hypothesis_formation
```
