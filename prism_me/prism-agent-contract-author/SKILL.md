---
name: prism-agent-contract-author
description: Author a Prism-style agent contract for an external capability. Use when a feature, workflow, or external runtime needs explicit planner metadata, typed inputs and outputs, coordination role, reasoning-log requirements, provenance, and runtime-boundary notes before implementation or onboarding.
---

# Prism Agent Contract Author

This skill turns a capability into a Prism-ready contract artifact.

Read:

- [../agents.md](../agents.md)
- [../shared/references/dependency-discipline.md](../shared/references/dependency-discipline.md)
- [../shared/references/external-harmonization.md](../shared/references/external-harmonization.md)
- [../shared/references/prism-alignment.md](../shared/references/prism-alignment.md)
- [../shared/references/release-gates.md](../shared/references/release-gates.md)
- [../shared/references/generative-quality-criteria.md](../shared/references/generative-quality-criteria.md)
- [../shared/templates/02-agent-contract.yaml](../shared/templates/02-agent-contract.yaml)
- [../shared/templates/02f-skill-contract-profile.yaml](../shared/templates/02f-skill-contract-profile.yaml)
- [../shared/templates/reasoning-log.md](../shared/templates/reasoning-log.md)
- `.prism/<request-slug>/01-spec.md`

## Workflow

1. Name the capability boundary and its lifecycle role.
2. Fill in `metadata` so provenance and semantic placement stay explicit.
3. Define planner cues: invocation condition, use cases, exclusions, role, priority, companions.
4. Define `runtime_adapter` only as far as the real runtime boundary is known.
5. Define typed `inputs` and `outputs`; make one durable primary output explicit.
6. Add the required `reasoning_log` sidecar contract.
7. Decide whether the request needs the optional skill contract profile; if yes, write or update `.prism/<request-slug>/02f-skill-contract-profile.yaml` using the current Prism core field names, and if no, record the explicit not-applicable reason in `.prism/<request-slug>/reasoning-log.md`.
8. Record allowed upstream and downstream agent kinds in `coordination`.
9. Keep dependency-bearing runtime truth visible in the contract where it belongs, especially workspace mounts, execution entrypoints, and source paths.
10. Leave full bundle, KB, backend, and dependency-edge mapping to `.prism/<request-slug>/03b-dependency-map.md` rather than overloading the contract.
11. Make space for later quality criteria and reflective refinement surfaces if the capability has meaningful generative behavior.
12. If the request started from external code, align the contract with `.prism/<request-slug>/02e-agentic-shape.md` instead of inventing a disconnected boundary.
13. Write or update `.prism/<request-slug>/02-agent-contract.yaml`.
14. Append a matching entry to `.prism/<request-slug>/reasoning-log.md`.

## Guardrails

- Typed ports come before prompt wording.
- Do not hide runtime dependencies in a prose note when they belong in `runtime_adapter`.
- Do not hide workspace mounts, route registries, or capability source paths when the capability depends on them.
- Do not flatten preserved external runtimes into fake native abstractions.
- If the request warrants `02f-skill-contract-profile.yaml`, use the current core field names directly: `input_evidence_types`, `output_contract`, `preconditions`, `assumptions`, `claim_policy`, `confidence_policy`, `provenance_policy`, `validators`, `evaluators`, `upstream_dependencies`, and `downstream_dependencies`.
- Every contract must state how reasoning logs are produced and where they live.

## Output Contract

Produce one YAML artifact with:

- metadata and provenance
- planner metadata
- runtime adapter notes
- typed invocation, input, output, coordination, and reasoning-log sections
