---
name: kb-deduce
description: Derive logically implied consequences from statements in a mathematical KB file. Use when the user asks what follows from current definitions/axioms/theorems, requests forward or backward chaining, or wants candidate corollaries with explicit dependency traces in `KB/*.kb.md`.
---


# KB Deduce


## Conceptual Role

This skill operationalizes deductive reasoning over the informal KB by asking what consequences follow once a selected set of premises or hypotheses is provisionally accepted.

## Framework Contribution

It contributes consequence-tracing and pruning: bridges or hypotheses that yield no useful entailment can be deprioritized in later loops.

## How To Read Outputs

Read its outputs as consequence maps and proof-pressure diagnostics that show what the current theory state can already support.

## Overview

Generate conservative deductions from the current KB. Separate strict consequences from speculative ones.

Read [references/prompt-template.md](references/prompt-template.md) before multi-step reasoning.

## Workflow

1. Fix the reasoning scope.
Use a specific target claim for backward chaining or a seed set for forward chaining.

2. Build the rule pool.
Collect usable `accepted` statements first; include `tentative` only if requested.

3. Run constrained chaining.
Emit only results with an explicit dependency path to known statements.

4. Classify output.
- `entailed`: derivable with available premises.
- `conditionally-entailed`: derivable if listed missing premises are added.
- `not-derived`: cannot be proven from current KB.

5. Write back derived results when asked.
Store accepted deductions under `# Derived Statements` with `kind: corollary|observation`.

## Guardrails

- Do not treat analogies as proofs.
- Do not use external math facts unless the user allows imports.
- Keep each derivation path minimal and inspectable.

## Output Contract

Return a table with columns:

`claim | class | depends_on | missing_premises | confidence | proof_sketch`

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Reasoning output must separate conjecture from entailment and never hide missing premises behind fluent explanation.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: statement, hypothesis, consequence, explanation, induction family, deduction chain, or abductive bridge.
- Preserved invariants: definitions, dependencies, entailment direction, support/refutation status, and target relevance.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: claim, mathematical object, inference mode, supporting IDs, preserved/broken invariants, epistemic status, obligations, and next validation. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote on circular support, missing premise, invalid entailment, over-generalized induction, counterexample, or uncited evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
