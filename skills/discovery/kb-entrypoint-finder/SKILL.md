---
name: kb-entrypoint-finder
description: Identify and rank the best conceptual entry points for proof progress by combining KB structure, concept-evolution phases, connector analysis, and proof hypotheses. Use when the user asks where to start, highest-impact intervention points, or best conceptual on-ramps for a specific KB.
---


# KB Entrypoint Finder


## Conceptual Role

This skill identifies the most informative conceptual entry points into a hard mathematical problem by combining graph position, concept evolution, and coherence signals.

## Framework Contribution

It contributes prioritization so later stages start from statements with the highest expected proof payoff rather than arbitrary canonical definitions or theorems.

## How To Read Outputs

Read ranked entry points as candidate starting positions for deeper proof work; the score explains why one concept is a better intervention target than another.

## Overview

Compute reproducible rankings of conceptual entry points by integrating relational graph signals with concept-evolution structure.

Read [references/scoring.md](references/scoring.md) for score composition.
Read [references/script-usage.md](references/script-usage.md) for execution commands.
Read [references/prompt-template.md](references/prompt-template.md) for narrative outputs.

## Workflow

1. Load context artifacts.
Use `KB/*.kb.md`, `artifacts/*/concept-evolution.md`, `artifacts/*/connection-analysis.json`, and `phyp/*.proof-hypotheses.yaml`.

2. Compute entry-point score.
Combine intervention, hypothesis pressure, bridge incidence, and concept-phase weight.

3. Rank and cluster.
Produce top entry points globally and grouped by conceptual phase.

4. Recommend first actions.
For top entries, suggest immediate `kb-abduce` and `kb-deduce` tests.

## Guardrails

- Use statement IDs as the anchor unit.
- Keep scoring transparent and auditable.
- Prefer high-leverage points over broad low-signal coverage.

## Output Contract

Return:

1. `Stats`
2. `Top Entry Points`
3. `Concept Tracks`
4. `Tactical Next Step`

Use `scripts/recommend_entrypoints.py` for deterministic output.

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `recommend_entrypoints.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
