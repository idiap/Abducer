---
name: workflow-contract-extractor
description: Extract structured workflow-stack contracts from repository coordination docs. Use when Codex needs to read AGENTS.md or a similar project contract and recover stack names, modes, triggers, artifact entrypoints, handoffs, guardrails, and ordered skill hooks before graphing or auditing workflow interactions.
---

# Workflow Contract Extractor

Use this as the first hook in the workflow graph reporting stack.

## Inputs

- onboarding pointer [AGENTS.md](../../AGENTS.md), authoritative [Prism agent contract](../../prism_me/agents.md), and active `.prism/<request>/` artifacts
- optional project-support index, usually [proj_skills/INDEX.md](../INDEX.md)
- optional main skill index, usually [docs/reference/skills.md](../../docs/reference/skills.md)

## Procedure

1. Follow `AGENTS.md` pointers. Extract Prism stage order and skill responsibilities from `prism_me/agents.md`, active request state from `to-do.md` and `.prism/<request>/`, and the four project-support stacks from `proj_skills/INDEX.md`.
2. Extract:
   - stack title
   - mode
   - trigger
   - artifact entrypoints
   - handoff
   - ordered `$skill-name` hooks
   - local guardrails when present
3. Preserve stack order from the source document.
4. Do not infer missing hooks from prose unless a `$skill-name` token is explicit.
5. Keep the extracted packet neutral; graph interpretation belongs to `$workflow-graph-modeler`.

## Handoff

Leave a structured workflow packet suitable for deterministic graph construction:

- `stacks`
- `skills`
- `stack_skill_edges`
- `source_document`
- `extraction_warnings`
