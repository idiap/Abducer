---
name: kb-explain
description: Explain mathematical statements from a KB file in layered natural language while staying grounded in statement IDs and dependencies. Use when the user asks for intuition, restatement, concept linking, or stepwise explanation of definitions, axioms, theorems, or proof sketches stored in `KB/*.kb.md`.
---


# KB Explain


## Conceptual Role

This skill translates structured KB artifacts into human-readable mathematical explanations for users inspecting concepts, dependencies, and proof attempts.

## Framework Contribution

It contributes interpretability by turning internal graph and hypothesis structures into explicit mathematical narratives.

## How To Read Outputs

Read its outputs as explanatory reconstructions of the current state of reasoning rather than as new inferential steps.

## Overview

Generate audience-aware explanations from KB statements without adding unsupported claims.

Read [references/prompt-template.md](references/prompt-template.md) before composing long explanations.

## Workflow

1. Select the target statement IDs.
Use explicit IDs from user input, otherwise infer from nearest title or symbol match.

2. Build a dependency slice.
Collect `depends_on` ancestors until the explanation is coherent.

3. Produce three layers.
- Plain-language intuition.
- Semi-formal reasoning chain.
- LaTeX-level restatement tied to IDs.

4. Cite every nontrivial claim.
Attach statement IDs inline for traceability.

5. Declare uncertainty.
If the KB lacks a needed premise, stop and list the exact missing IDs under `Missing Support`.

## Guardrails

- Do not introduce new theorems as facts.
- Treat `status: tentative` statements as provisional.
- Keep symbol meaning consistent with the KB glossary.
- Distinguish explanation from proof completion.

## Output Contract

Use this section order:

1. `Summary`
2. `Dependency Path`
3. `Detailed Explanation`
4. `Missing Support`
5. `Referenced IDs`

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
