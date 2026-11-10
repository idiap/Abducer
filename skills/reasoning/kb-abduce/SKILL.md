---
name: kb-abduce
description: Generate and rank explanatory hypotheses for observations or target claims that are not fully derivable from the current KB. Use when the user asks for plausible missing premises, best explanations, repair hypotheses, or assumption discovery over `KB/*.kb.md`.
---

# KB Abduce


## Conceptual Role

This skill operationalizes abductive reasoning over a single KB by proposing minimal missing premises that would make a target statement or bridge mathematically viable.

## Framework Contribution

It contributes the hypothesis-generation step that turns structural gaps into explicit, testable assumptions for the next deductive or coherence pass.

## How To Read Outputs

Read its outputs as disciplined missing-premise candidates, not as accepted mathematics; the value lies in exposing what additional structure would have to exist.

## Overview

Propose the smallest plausible hypothesis sets that would explain a target observation or make a desired claim derivable.

Read [references/prompt-template.md](references/prompt-template.md) before generating hypotheses.

## Workflow

1. Define abduction target.
State the observation or claim to explain. When available, use top-ranked targets from `kb-proof-connector`.

2. Compute failure boundary.
Attempt deduction first and list exactly where support is missing.

3. Propose hypothesis sets.
Generate multiple minimal candidate sets (`H1`, `H2`, ...) with explicit semantics in LaTeX. Include connector-suggested cross-statement links as optional hypotheses.

4. Rank hypotheses.
Score by explanatory coverage, structural simplicity, compatibility with existing KB, and novelty risk.

5. Emit falsification tests.
For each hypothesis set, list what evidence would support or refute it.

6. Optional KB update.
If requested, add top hypotheses under `# Derived Statements` as `kind: conjecture`, `status: tentative`.

## Guardrails

- Do not present abduced hypotheses as established facts.
- Prefer fewer assumptions over many weak assumptions.
- Reject hypotheses that contradict `accepted` statements unless contradiction is the explicit goal.

## Output Contract

Return sections in this order:

1. `Target`
2. `Deduction Failure Boundary`
3. `Hypothesis Sets`
4. `Ranking Rationale`
5. `Falsification Tests`
6. `Recommended Next Step`

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
