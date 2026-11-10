---
name: abducer-conceptual-pressure-formalizer
description: Formalize Abducer dependency frontier nodes, blocked proof results, bridge gaps, and repeated route pressure into conceptual pressure packets. Use when hypothesis-space exploration needs typed failure, opportunity, open-question, or discovery-signal inputs before creative candidate generation.
---

# Abducer Conceptual Pressure Formalizer

## Role

Convert Abducer artifacts into typed conceptual pressure packets. Treat pressure
as a control signal over the hypothesis exploration space, not as an explanation
after the route has already been chosen.

## Inputs

- Target packet.
- Dependency graph frontier.
- KB statement IDs.
- Bridge, abstraction, proof queue, pathway, and blocked-result artifacts.
- Existing `artifacts/hegelian/hypothesis_exploration_map.json` when refining.

## Workflow

1. Identify the exact source node or artifact that creates pressure.
2. Classify the pressure as `failure`, `discovery_signal`, `opportunity`, or `open_question`.
3. Preserve the witness text and source artifact paths.
4. State the repair target and unknowns.
5. Name successor hooks such as bridge invention, obligation factorization, theorem weakening, or representation shift.

## Guardrails

- Do not invent pressure without a source node, artifact path, or KB ID.
- Do not collapse positive discovery signals into failures.
- Do not treat a pressure packet as proof progress.
- If source evidence is absent, mark the pressure as low-confidence and route it to evidence acquisition or quarantine.

## Output Contract

Emit objects conforming to `agentic/spec/conceptual_pressure_packet.schema.json`.
Use `agentic/scripts/build_hypothesis_exploration_map.py` for deterministic seeded packets and `agentic/scripts/validate_hypothesis_exploration.py` before promotion.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- A score or label is never enough; evaluation must expose what would falsify, demote, or repair the route.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: definitions, bridge objects, candidate hypotheses, entailment gaps, premises, regimes, counterexamples, and proof obligations.
- Preserved invariants: objects compared, assumptions used, preserved invariants, broken invariants, boundary regimes, and witness evidence.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
