---
name: route
description: Compile a fixed `.prism` reasoning program into deterministic bindings from reasoning occurrences to registered skills. Use when a user invokes `route`, requests rigid routing, wants a reproducible skill plan, or needs to validate that a prescribed reasoning sequence has concrete capability coverage without dynamic replanning.
---

# Route

Compile declared `steps` to concrete skills. Treat the `.prism` program as
fixed: do not add, remove, reorder, branch, or reinterpret reasoning
occurrences.

## Procedure

1. Read the selected `.prism` program.
2. Read `agentic/registries/essential_reasoning_types.yaml`,
   `agentic/registries/skill_registry.yaml`, and
   `agentic/registries/reasoning_capability_routes.yaml`.
3. Reject unresolved `_` occurrences, missing mappings, unknown skills, and
   contradictory explicit bindings.
4. Bind each occurrence by explicit `alias=skill` selection or by the named
   rigid profile. Never infer a new step to repair missing coverage.
5. Emit the binding plan before invoking any selected skill.
6. Execute only after the caller accepts the plan or execution was already
   explicitly requested.

Use `scripts/compile_route.py` for deterministic compilation. Read
[references/contract.md](references/contract.md) when changing routing policy
or interpreting a blocked plan.

## Guardrails

- Do not replan. Hand dynamic decisions to `$orch`.
- Do not select a skill absent from the registered reasoning-type mapping.
- Do not treat lexical or profile selection as evidence that a skill's output
  is scientifically correct.
- Preserve input handles, output handles, scope, provenance, taints, claim
  ceilings, and unresolved obligations.
- Preserve the mathematical invariants and relational dependencies declared by
  the program; routing may bind their implementation but cannot rewrite them.
- Do not execute a gap-bearing or blocked plan.

## Epistemic Discipline

Routing has zero claim effect. A successful binding establishes capability
coverage only. Each child output retains its own epistemic status; conditional,
conjectural, not-refuted, blocked, and refuted results cannot be promoted by
route completion. Cite the `.prism` path, registry entries, skill paths, and
explicit unknowns as evidence for every binding decision.

## Output Contract

Return:

- `mode: route`;
- program identity and source digest;
- immutable selection profile;
- one binding per reasoning occurrence with alias, type, skill, mapping kind,
  confidence, inputs, and outputs;
- blockers and unresolved obligations;
- `executable`, which is false whenever any gap or invalid binding remains;
- validation handoff to the capability compiler and relevant skill validator.

## Failure/Demotion

Quarantine the plan when a reasoning type lacks a registered materializer, a
skill is stale or missing, an explicit binding violates its mapping, or a `_`
gap appears. Demotion changes routing readiness only; it does not refute the
scientific goal.

## Codex Exec Protocol

Run deterministically and inspect the emitted artifact:

```bash
python skills/orchestration/route/scripts/compile_route.py \
  agentic/reasoning_flows/abducer_work_loop.prism
```

Record executed commands and artifact inspection. Validate with
`quick_validate.py`, the focused orchestration tests, and
`agentic/scripts/validate_essential_reasoning_types.py`.
