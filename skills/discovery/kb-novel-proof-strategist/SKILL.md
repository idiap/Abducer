---
name: kb-novel-proof-strategist
description: Build a diversified proof-strategy portfolio from intermediate results and generate a systematic prompt that maximizes novelty under rigor constraints. Use when the user asks for distinct proof strategies, strategy portfolios, or novelty-maximizing planning prompts.
---


# KB Novel Proof Strategist


## Conceptual Role

This skill designs proof strategies that combine current bridges, conjectured abstractions, and coherence diagnostics into distinct research programs.

## Framework Contribution

It contributes strategic diversification and novelty pressure so the framework explores more than one local connector route.

## How To Read Outputs

Read its outputs as higher-level proof programs whose quality depends on concept fertility, bridge fit, and barrier-awareness.

## Overview

Transform entrypoints, pathways, bridge programs, and hypotheses into ranked proof strategies with a novelty-maximizing prompt.

Read [references/novelty-policy.md](references/novelty-policy.md) for selection logic.
Read [references/script-usage.md](references/script-usage.md) for execution.
Read [references/prompt-template.md](references/prompt-template.md) for orchestration prompts.

## Workflow

1. Load intermediate artifacts.
2. Build strategy candidates from pathways and support context.
3. Select a diverse strategy set (phase diversity + low overlap).
4. Generate novelty-maximizing systematic prompt.

## Guardrails

- Every strategy must be anchored by statement IDs.
- Keep assumptions minimal and testable.
- Enforce diversity across conceptual phases.

## Output Contract

Return:

1. `Stats`
2. `Strategies`
3. `Novelty-Maximizing Prompt`

Use `scripts/design_strategies.py` for deterministic output.
Use `scripts/run_integrated_pvsnp.py` for integrated test execution.

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `design_strategies.py, run_integrated_pvsnp.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
