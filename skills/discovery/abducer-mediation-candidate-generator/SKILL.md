---
name: abducer-mediation-candidate-generator
description: Generate grounded Abducer mediation candidates and creative hypothesis transformations from pressure packets. Use when the workflow needs bridge invention, abstraction formation, regime restriction, theorem weakening or strengthening, carrier introduction, negative-route inversion, analogy transport, proof-obligation factorization, or representation shift candidates.
---

# Abducer Mediation Candidate Generator

## Role

Generate creative but controlled transformations over the hypothesis exploration
space. A candidate is useful only when it changes route options and creates
validation obligations.

## Creative Operations

- `bridge_invention`: introduce a mediator, relation, map, or invariant.
- `abstraction_formation`: compress repeated proof or route shapes.
- `regime_restriction`: narrow assumptions, classes, encodings, or parameters.
- `theorem_weakening`: relax an overstrong target into a testable successor.
- `theorem_strengthening`: add a sharper invariant when evidence supports it.
- `carrier_introduction`: introduce an object that transports structure.
- `negative_route_inversion`: turn failure evidence into a successor route.
- `analogy_transport`: move a pattern from a source theorem family with mismatch inventory.
- `proof_obligation_factorization`: split an opaque blocker into lemmas or evidence tasks.
- `representation_shift`: revise local ontology or proof vocabulary.

## Workflow

1. Read pressure packets and classification artifacts.
2. Generate multiple candidate classes when the pressure supports them.
3. Cite source pressure IDs, affected dependency nodes, KB IDs, and artifact paths.
4. State the proposed transformation, expected route value, and disconfirming observations.
5. List validation requirements before recommending a disposition.

## Guardrails

- Withhold candidates when pressure lacks grounding.
- Do not optimize for novelty over proof/source/non-collapse discipline.
- Do not treat a candidate as proof; send it to obligation gating.

## Output Contract

Emit `abducer_mediation_candidate` and `conceptual_creativity_analysis` objects. Run `agentic/scripts/build_hypothesis_exploration_map.py` for deterministic seeds and `agentic/scripts/validate_hypothesis_exploration.py` before promotion.

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
