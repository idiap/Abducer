---
name: kb-epistemic-hardness
description: Explain epistemologically why a hard problem is difficult using the current KB and intermediate artifacts. Use when the user asks why a problem (e.g., P vs NP) is hard, what the essential epistemic bottlenecks are, or which structural constraints block straightforward proof progress.
---


# KB Epistemic Hardness


## Conceptual Role

This skill articulates why a target problem is hard in epistemic and conceptual terms, not just by restating that it is open or technically difficult.

## Framework Contribution

It contributes barrier analysis, asymmetry diagnosis, and research-program pressure points that explain which kinds of conceptual innovation are actually needed.

## How To Read Outputs

Read its outputs as a diagnosis of where current mathematical knowledge fails to close the problem and which barrier families dominate the search space.

## Overview

Articulate why a target problem is hard by combining KB structure, concept evolution, entry points, pathways, connector links, and hypothesis pressure.

Read [references/essential-elements.md](references/essential-elements.md) for element taxonomy.
Read [references/script-usage.md](references/script-usage.md) for deterministic generation.
Read [references/prompt-template.md](references/prompt-template.md) for narrative rendering.

## Workflow

1. Load target KB and intermediate artifacts.
2. Quantify structural signals (dependency sparsity, barrier pressure, bridge dependence, phase dispersion).
3. Synthesize essential epistemic elements with explicit evidence IDs.
4. Produce concise actionable focus recommendations.

## Guardrails

- Ground every claim in KB/artifact evidence.
- Distinguish established constraints from conjectural bridge pressure.
- Keep outputs problem-specific, not generic complexity-theory prose.

## Output Contract

Return:

1. `Summary`
2. `KB Stats`
3. `Essential Elements`
4. `Recommended Focus`

Use `scripts/articulate_hardness.py` for reproducible outputs.

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `articulate_hardness.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
