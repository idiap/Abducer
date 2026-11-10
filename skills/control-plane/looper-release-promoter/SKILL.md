---
name: looper-release-promoter
description: Interpret compliance, drift, dependency, workflow, hook, and validation evidence to promote, quarantine, roll back, or escalate a controlled Abducer iteration. Use at the end of target-navigation and Looper-controlled work-loop slices.
---

# Looper Release Promoter

## Conceptual Role

This skill is the generative release interpretation layer. Deterministic reports
count evidence; this skill decides what the evidence means for promotion,
quarantine, rollback, or escalation.

## Inputs

- Dependency closure report.
- Compliance report.
- Drift report.
- Frame adequacy report.
- Workflow and hook validation results.
- Promotion gate policy.

## Procedure

1. Identify the controlled iteration and target.
2. Summarize what changed and which workflow executed.
3. Check whether all blocking gates have evidence.
4. Separate passing evidence from fragile, missing, waived, or drift-risk
   evidence.
5. Recommend promote, quarantine, rollback, or escalate.
6. State rollback path and open blockers.

## Required Output

- `agentic/reports/releases/ITER-*.md`
- Release decision with evidence.
- Rollback path.
- Open blocker list.

## Boundaries

- Do not promote if critical target dependencies are unknown without TODOs or
  waivers.
- Do not hide blockers inside prose.
- Do not treat validation success as mathematical proof.

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

## Subgoal Control Decision

Release promotion must cite the active `Subgoal Control Decision` summary. Promote only when active proof/discovery routes have compatible decisions and no stale repeated blockers. Quarantine, roll back, or escalate if a route persists without target-object link, learning from failure, or backtrack/pivot/quarantine/stop triggers.

## Best Machinery Assessment

Release promotion must cite the active machinery portfolio and unresolved abstraction-chain gaps. Promote only when active proof routes carry a `Best Machinery Assessment` with `machinery_role`, `controlled_interface`, `why_best_available`, `premature_use_warning`, `required_bridge_obligation`, `invalid_use_modes`, and `validation_handoff`. Block promotion if method choice is missing, solves a proxy problem, or uses endpoint/witness machinery before the required construction and transfer objects exist.
