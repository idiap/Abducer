---
name: kb-induce
description: Generalize successful bridge, strategy, lemma, or proof-sketch patterns into reusable theorem schemas. Use when the user asks to abstract a proof route, infer a reusable bridge template, or consolidate repeated strategy-level structures over `KB/*.kb.md`.
---


# KB Induce


## Conceptual Role

This skill performs scoped induction over existing bridge, strategy, and proof artifacts to recover reusable higher-level patterns.

## Framework Contribution

It contributes late-stage abstraction by generalizing already-isolated proof motifs rather than mining the raw KB for loose similarities.

## How To Read Outputs

Read its outputs as family-level generalizations or strategy schemas, not as first-line discovery mechanisms.

## Overview

Identify recurring structures in already-stabilized bridge, strategy, or proof-sketch artifacts and convert them into explicit candidate generalizations.

Read [references/prompt-template.md](references/prompt-template.md) before creating induced conjectures.

This is not a first-line discovery mode over raw KB content. In this framework, `kb-induce` is an optional late-stage synthesis tool used after `conjecture`, `strategies`, or `proof-sketch`, once there is enough structured evidence to generalize safely.

## Workflow

1. Select induction corpus.
Choose a coherent family of related bridge objects, strategies, proof sketches, or theorem-family statements.

2. Extract structural features.
Track quantifier shape, algebraic/topological conditions, and conclusion forms.

3. Cluster patterns.
Group statements by shared antecedent or conclusion templates.

4. Propose generalizations.
Emit candidate schemas in LaTeX with domain constraints, theorem-family scope, and explicit failure regime.

5. Stress test each conjecture.
List known supporting examples, possible counterexample classes, and required validation tasks.

6. Optional KB update.
Store surviving candidates as `kind: conjecture`, `status: tentative`, with links to supporting statement IDs.

## Guardrails

- Do not use induction as a primary source of bridge discovery over sparse raw KB content.
- Do not overgeneralize across incompatible domains or proof regimes.
- Keep induced claims weaker when evidence is sparse.
- Mark data-poor conjectures with lower confidence.

## Output Contract

Return sections:

1. `Pattern Clusters`
2. `Candidate Generalizations`
3. `Support and Counterexample Risk`
4. `Validation Plan`

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
