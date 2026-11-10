---
name: looper-target-goal-enricher
description: Enrich a raw mathematical target into a validated Abducer target packet with output type, quality criteria, acceptance gates, constraints, unknowns, validation targets, and evidence paths. Use before controlled target-navigation or recursive dependency closure.
---

# Looper Target Goal Enricher

## Conceptual Role

This skill is the generative intake layer for Abducer's Looper control plane.
It converts a raw mathematical ambition into a target packet that can be
validated, recursively expanded, and governed.

## Inputs

- Raw target or user request.
- Candidate KB path in `KB/*.kb.md`.
- Relevant existing artifacts under `artifacts/<kb-ref>/` and `phyp/`.
- Target packet schema at `agentic/spec/target_packet_schema.json`.

## Procedure

1. Identify the concrete mathematical target and distinguish it from broad
   background ambition.
2. Resolve the target to one or more KB statement IDs when possible.
3. Infer the output type: proof route, proof sketch, refutation, dependency map,
   expert handoff, research-program update, or controlled iteration.
4. Select quality criteria that are task-specific and measurable.
5. Create acceptance gates that can block release.
6. Preserve hard constraints exactly, including source policy, local-only gates,
   and no-hidden-hook requirements.
7. State unknowns as decision-relevant gaps rather than generic questions.
8. Emit a target packet conforming to `agentic/spec/target_packet_schema.json`.

## Required Output

- A target packet under `agentic/examples/targets/` or
  `agentic/state/current_target.json`.
- A refined goal statement.
- Acceptance gates with required evidence.
- Validation targets that name concrete artifacts.

## Boundaries

- Do not treat a problem title as a target.
- Do not invent KB statement IDs.
- Do not relax user constraints while rewriting the goal.
- Do not use hidden chain-of-thought; provide auditable rationale summaries and
  packet fields only.

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
