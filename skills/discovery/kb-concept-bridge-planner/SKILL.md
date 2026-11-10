---
name: kb-concept-bridge-planner
description: Given intermediate KB artifacts, systematically identify and rank how to bridge essential concepts across phases. Use when the user asks how to connect key concepts/results, design bridge programs, or prioritize cross-concept linkage tests.
---


# KB Concept Bridge Planner


## Conceptual Role

This skill turns ranked statements and connector evidence into explicit bridge programs that specify where a proof route should try to pass through the KB.

## Framework Contribution

It contributes a bridge-level research agenda by converting abstract connectivity into typed bridge families, commitments, and intervention sequences.

## How To Read Outputs

Read its outputs as proposed proof routes with typed inferential commitments, not as proofs; the bridge type, invariant, and barrier scope explain why each route matters.

## Overview

Construct bridge programs that connect essential concepts using connector links, entrypoint signals, pathway signals, and hypothesis support.

Read [references/bridge-criteria.md](references/bridge-criteria.md) for scoring logic.
Read [references/script-usage.md](references/script-usage.md) for reproducible runs.
Read [references/prompt-template.md](references/prompt-template.md) for narrative output.
Read [references/non-immediate-bridge-search.md](references/non-immediate-bridge-search.md) when the local bridge object is still under-typed and the search needs prior objects or analogical candidates from non-immediate areas.

## Workflow

1. Ingest intermediate results (`analysis`, `entrypoints`, `pathways`, `phyp`, `concept`).
2. Score bridge candidates and classify bridge types.
3. For the top bridges, state both the missing bridge object/transport law and the main positive vs negative proof-space opportunities.
4. If the bridge object is still schematic, convert the gap into a declarative search profile and search for bridge objects beyond the immediate area.
5. Group bridges by conceptual axes (phase -> phase).
6. Emit prioritized run order with validation protocol.

## Guardrails

- Keep bridge proposals tentative until deductive validation.
- Prefer high-score bridges that touch essential entry points.
- Track bridge axes explicitly to avoid phase-local loops.
- Do not treat negative or impossibility-style routes as fallback only; they are part of the epistemic value of a bridge program.
- When searching non-immediate areas, distinguish named-object precedent, structural analogy, and mere topical resemblance.

## Output Contract

Return:

1. `Stats`
2. `Top Bridge Programs`
3. `Bridge Axes`
4. `Recommended Run Order`

Use `scripts/plan_bridges.py` for deterministic outputs.

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `plan_bridges.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
