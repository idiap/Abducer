---
name: kb-coherence-evaluator
description: Build a typed coherence graph over statements, concepts, and hypotheses, then compute global coherence and local explanatory-power/coherence-delta signals per hypothesis. Use when the user asks for coherentist assessment, global theory consistency checks, explanatory power scoring, or belief-revision guidance over `KB/*.kb.md` and `phyp/*.yaml`.
---


# KB Coherence Evaluator


## Conceptual Role

This skill implements the coherentist layer of the framework by scoring how well candidate hypotheses fit into the global web of claims, supports, tensions, and explanations.

## Framework Contribution

It contributes theory-level selection pressure so the workflow does not optimize only local bridge quality or isolated statement similarity.

## How To Read Outputs

Read its reports as global theory diagnostics: positive scores indicate better mutual fit, while negative deltas indicate tension, weak support, or poor explanatory integration.

## Overview

Construct a typed coherence graph with relation types `supports`, `attacks`, `explains`, `reframes`, and `blocks`. Score global coherence and compute per-hypothesis deltas for belief revision.

Read [references/script-usage.md](references/script-usage.md) for deterministic execution.
Read [references/prompt-template.md](references/prompt-template.md) for narrative interpretation prompts.

## Workflow

1. Parse KB statements and dependency structure.
2. Ingest connector analysis and phyp hypotheses.
3. Build typed nodes and edges across statements, hypotheses, concepts, methods, and barriers.
4. Compute global coherence profile.
5. Compute per-hypothesis:
- `explanatory_power_local`
- `coherence_delta_global`
6. Emit revision guidance for low-coherence hypotheses.

## Output Contract

Produce JSON/Markdown with:

- `typed_coherence_graph`
- `coherence_profile`
- `hypothesis_coherence`
- `belief_revision_recommendations`

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `evaluate_coherence.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
