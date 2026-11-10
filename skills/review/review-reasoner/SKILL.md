---
name: review-reasoner
description: "Run a multi-perspective, code-first review of the reasoner under five critical lenses: an epistemologist of mathematical discovery, a Fields Medalist mathematician, a DeepMind-style mathematical discovery scientist, a concept-discovery logician, and a radically out-of-the-box systems designer. Use when the user wants a deep review of how the reasoner actually works, where it fails, how the epistemic process is encoded in code, or how the architecture should change."
---

# Review Reasoner

## Conceptual Role

This is the macro review skill for the reasoner as an implemented system.
It is not a document reviewer.
It is a code-and-state reviewer.

Use it to inspect how the platform actually performs theorem grounding, discovery, proof search, critique, persistence, reflection, and control-loop governance.

## Required Review Surface

Review the full local environment rather than a high-level description.

At minimum inspect:

1. `skills/common`
2. active stage scripts under `skills/*/scripts`
3. prompt stack under `skills/*/SKILL.md`, `skills/*/references`, and `skills/*/agents/openai.yaml`
4. `tests`
5. live state in `artifacts/<kb-ref>` when relevant
6. persistent theorem memory in `InformalMathLib/<kb-ref>`
7. supporting docs only as secondary evidence

Treat docs as claims about the system.
Treat code, tests, and persisted state as the primary evidence.

## Workflow

1. Inspect the actual control path:
   theorem-body normalization,
   discovery,
   prove,
   work,
   meta,
   prior-art import,
   persistence.
2. Review the reasoner through all five lenses listed in [references/reviewer-stack.md](references/reviewer-stack.md).
3. For each lens:
   identify concrete implementation strengths,
   concrete defects,
   missing mechanisms,
   and likely failure modes.
4. Compare the lenses:
   where they converge,
   where they disagree,
   and which disagreements are structurally important.
5. End with a prioritized redesign agenda:
   what to fix now,
   what to instrument next,
   what should be reconsidered architecturally.

Read [references/prompt-template.md](references/prompt-template.md) for the full macro review prompt.
Read [references/reviewer-stack.md](references/reviewer-stack.md) for the five reviewer lenses and how to combine them.

## Output Contract

The review should:

1. present findings first, ordered by severity;
2. cite actual files, modules, tests, and artifacts;
3. separate epistemic defects from mathematical defects from systems defects;
4. distinguish implemented capability from aspirational documentation;
5. end with convergence, disagreement, and recommended next interventions.

## Guardrails

- Do not review from summaries alone.
- Do not treat prompt documents as evidence that the mechanism really exists.
- Do not confuse rich artifacts with valid discovery.
- Do not collapse all criticism into generic architecture comments; tie every major claim to code paths and state transitions.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Review should create actionable obligations, not aesthetic commentary or generic caution.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: reviewed claim, definition, invariant, route, evidence packet, and falsifier.
- Preserved invariants: object identity, assumptions, preserved/broken invariants, evidence status, and review scope.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: severity-ranked findings, mathematical objects, epistemic statuses, evidence paths, falsification tests, demotion reasons, and concrete TODOs. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote claims on unsupported evidence, broken invariants, hidden assumptions, counterexamples, or scope overreach.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
