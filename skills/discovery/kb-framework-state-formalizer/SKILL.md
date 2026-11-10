---
name: kb-framework-state-formalizer
description: Formalize the current state of the Abducer reasoning framework as a concise LaTeX system description with typed state, inference operators, orchestration composition, scoring semantics, and logging contracts. Use when the user asks to formalize the framework itself, summarize the architecture mathematically, or generate a succinct `.tex` document describing the current reasoning pipeline.
---

# KB Framework State Formalizer

## Conceptual Role

This skill turns the current framework implementation into a concise formal system description.

## Framework Contribution

It makes the framework itself inspectable as a typed reasoning architecture rather than only as a collection of scripts.

## Overview

Run this skill when the target is the framework, not a specific KB.

It reads the current repository documentation and emits a short LaTeX formalization of:

1. the typed KB and artifact state,
2. the current inference-mode sets,
3. the deterministic stage operators,
4. the orchestration composition,
5. the scoring and logging semantics.

Read [references/script-usage.md](references/script-usage.md) for deterministic execution.
Read [references/prompt-template.md](references/prompt-template.md) for prompt-mode rendering constraints.

## Workflow

1. Read the current framework sources: `README.md`, `docs/architecture/architecture.md`, `docs/architecture/orchestration.md`, and `docs/reference/skills.md`.
2. Recover current primary inference modes, orchestrator intents, and skill inventory.
3. Map the implemented stages into a concise typed operator algebra.
4. Render a short LaTeX document that states the framework signature, stage composition, and observability contract.
5. Write a machine-readable manifest and the `.tex` file, and log the generation step.

## Guardrails

- Formalize the implemented framework state, not an aspirational future version.
- Keep the output succinct: prefer definitions, equations, and short operator descriptions over narrative exposition.
- Use repository docs and already-processed metadata as sources of truth.
- Preserve traceability by listing the source documents and generated outputs in the reasoning log.

## Output Contract

Return:

1. `metadata`
2. `framework_signature`
3. `inference_modes`
4. `operators`
5. `latex_path`
6. `latex_source`

Use `scripts/generate_framework_state_formalization.py` for deterministic outputs.

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `generate_framework_state_formalization.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
