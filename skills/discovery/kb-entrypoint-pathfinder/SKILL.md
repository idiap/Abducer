---
name: kb-entrypoint-pathfinder
description: Convert ranked conceptual entry points into concrete proof-pathway agendas with hypotheses, supporting links, and execution plans. Use when the user asks how to operationalize entry points into actionable abductive/deductive search tracks.
---


# KB Entrypoint Pathfinder


## Conceptual Role

This skill synthesizes short proof-oriented pathways from the ranked entry points into surrounding bridge and hypothesis structure.

## Framework Contribution

It contributes local route planning by showing how an entry point can be expanded into a usable sequence of nearby inferential moves.

## How To Read Outputs

Read pathways as compact route sketches: they are valuable when they reveal how an entry concept can be operationalized into a bridge program or proof sketch.

## Overview

Turn top conceptual entry points into executable pathway bundles for iterative proof search.

Read [references/pathway-scoring.md](references/pathway-scoring.md) for ranking policy.
Read [references/script-usage.md](references/script-usage.md) for command usage.
Read [references/prompt-template.md](references/prompt-template.md) for narrative rendering.

## Workflow

1. Load ranked entry points.
Consume `entrypoints.json` from `kb-entrypoint-finder`.

2. Attach hypothesis and link context.
Join relevant `phyp` hypotheses and connector links per entry statement.

3. Build pathway agendas.
Produce per-path goal, support set, and loop execution checklist.

4. Rank pathways.
Score each pathway by entry strength and support quality.

## Guardrails

- Keep each pathway centered on one anchor statement.
- Keep hypotheses tentative until validated.
- Include explicit stop/prune conditions.

## Output Contract

Return:

1. `Stats`
2. `Ranked Pathways`
3. `Execution Plan` (per pathway)

Use `scripts/synthesize_pathways.py` for deterministic outputs.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Novelty is not value; generated hypotheses must carry status labels and disconfirming observations before receiving active attention.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: candidate bridge, conjecture, entrypoint, proof sketch, route family, or conceptual transformation.
- Preserved invariants: target commitments, source-grounded definitions, bridge compatibility, and explicit proof obligations.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `synthesize_pathways.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
