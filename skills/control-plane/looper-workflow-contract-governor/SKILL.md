---
name: looper-workflow-contract-governor
description: Govern visible Abducer workflows by checking composed skills, deterministic hooks, required artifacts, validators, gate decisions, and handoffs. Use when target-navigation or work-loop routes must be controlled by explicit workflow contracts.
---

# Looper Workflow Contract Governor

## Conceptual Role

This skill keeps workflows as the visible unit. It interprets whether a run is
properly composed from skills, hooks, artifacts, validators, and gate decisions.

## Inputs

- Task workflow manifests under `registry/tasks/*/task_registry.json`.
- Workflow contracts under `agentic/registries/workflow_contracts.yaml`.
- Gate policy under `agentic/registries/gate_policy.yaml`.
- Hook registry under `hooks/hooks.json`.
- Runtime skill application logs.

## Procedure

1. Read the active task manifest from its `visible_workflows` section first.
2. Verify that every named skill, hook, workflow reference, artifact, and
   validator is declared.
3. Interpret gate decisions using the shared gate policy.
4. Identify lifecycle gaps, invalid waivers, orphan skills, and stale handoffs.
5. Recommend whether the workflow may continue, must warn, must block, or must
   quarantine.

## Required Output

- Workflow governance finding with gate decision.
- Explicit missing artifacts or invalid composition edges.
- Suggested repair TODOs when the workflow cannot continue.

## Boundaries

- Do not promote a workflow because individual skills look plausible.
- Do not allow hidden hooks to substitute for workflow contracts.
- Do not accept waivers without evidence and review scope.

## Prompt Contract

Use `references/prompt-template.md`.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Workflow validity is not theorem validity; never promote a mathematical claim merely because a hook, report, or release gate passed.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: target packet, dependency graph node, workflow contract, hook decision, gate packet, and release artifact.
- Preserved invariants: target identity, declared dependencies, gate semantics, artifact provenance, and unresolved proof debt.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: decision, cited evidence paths or explicit unknowns, unresolved mathematical debt, rollback/quarantine condition, and next validator. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote or quarantine on uncited artifacts, missing target packet IDs, hidden hooks, stale gates, unsupported proof claims, or drift from essential target commitments.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
