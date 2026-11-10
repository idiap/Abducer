---
name: looper-hook-policy-maintainer
description: Maintain transparent deterministic hook policy for Abducer's Looper control plane. Use when UserPromptSubmit, PreSkillUse, PostSkillUse, PreToolUse, or Stop hooks need review, repair, or extension.
---

# Looper Hook Policy Maintainer

## Conceptual Role

This skill keeps hooks small, deterministic, and visible. Hooks may log, warn,
or block. They must not hide target navigation or proof-search reasoning.

## Inputs

- `hooks/hooks.json`.
- Hook scripts under `hooks/scripts/`.
- Hook fixtures under `agentic/evals/hook_contract/`.
- Hook traces under `agentic/traces/hook_runs/`.

## Procedure

1. Check that each hook has a deterministic event, script, and test fixture.
2. Reject hook behavior that performs hidden orchestration, generative
   diagnosis, or proof-search continuation.
3. Ensure warning and blocking decisions cite concrete policy reasons.
4. Require Stop hooks to protect current target, dependency frontier,
   compliance, drift, and next TODO evidence.
5. Produce repair instructions and fixtures when a hook changes.

## Required Output

- Hook policy finding.
- Updated hook fixture expectations when behavior changes.
- TODOs for unsafe or missing hook coverage.

## Boundaries

- Do not add generative reasoning inside hooks.
- Do not let hooks mutate proof artifacts.
- Do not block normal read-only inspection without a concrete policy reason.

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
