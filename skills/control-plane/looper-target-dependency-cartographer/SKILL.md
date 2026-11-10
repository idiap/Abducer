---
name: looper-target-dependency-cartographer
description: Recursively cartograph all proof, premise, route, bridge, queue, InformalMathLib, and evidence dependencies for a validated Abducer target packet. Use when a target must become goal-oriented and dependency-controlled.
---

# Looper Target Dependency Cartographer

## Conceptual Role

This skill is the generative interpretation layer over the deterministic
dependency graph. It decides which open dependency nodes matter, how they should
be grouped into proof work, and where Abducer should continue, revise, or stop.

## Inputs

- A validated target packet.
- `KB/<kb-ref>.kb.md`.
- Existing Abducer artifacts under `artifacts/<kb-ref>/`.
- `phyp/<kb-ref>.proof-hypotheses.yaml`.
- Dependency graph schema and generated graph.

## Procedure

1. Read the target packet and its acceptance gates.
2. Inspect the generated dependency graph, not just the raw artifact list.
3. Classify unresolved nodes by mathematical role: missing premise, bridge
   object, route lemma, proof debt, external prior-art need, stale route, or
   blocker.
4. Identify the next frontier that best serves the target rather than merely the
   highest local score.
5. Recommend the next Abducer workflow route and the skill sequence required.
6. Produce a dependency-closure report and frontier update.

## Required Output

- `agentic/state/dependency_graphs/<target>.json`
- `agentic/state/dependency_frontier.json`
- `agentic/reports/dependency_closure/<target>.md`
- Next-action recommendations linked to node IDs.

## Boundaries

- Do not collapse similarity links into proof dependencies.
- Do not mark a dependency closed because it is mentioned in an artifact.
- Do not continue recursion without cycle detection.
- Do not hide blockers; unresolved dependencies require a next action or TODO.

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
