---
name: expert-handoff
description: Turn a route, proof attempt, or bridge program into a compact expert-facing inspection dossier. Use when a human mathematician needs to inspect the precise live claims and burdens.
---

# Expert Handoff

## Role

This skill compresses the current state into claims a human expert can actually inspect.

## When To Use

Use it when:

1. one route should be reviewed by a mathematician;
2. a proof attempt needs external expert attention;
3. the system must explain exactly what remains open.

Read [references/prompt-template.md](references/prompt-template.md).

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Reporting must not launder conjectural, blocked, or low-relevance routes into conclusions.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: report section, handoff claim, expert summary, proof narrative, table, and cited artifact.
- Preserved invariants: claim-to-evidence mapping, status labels, target commitments, source limits, and unresolved obligations.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: claims with evidence paths or unknowns, epistemic status, target relevance, unresolved debt, demotion triggers, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote or annotate claims when evidence is missing, status is conjectural, disconfirmation is unresolved, or report prose overstates proof progress.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
