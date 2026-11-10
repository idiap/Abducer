---
name: kb-revision-loop
description: Generate ontology and representation revision actions from loop/coherence/hardness artifacts. Use when unresolved hypotheses remain after iterative testing and the workflow should trigger concept splitting, definition repair, regime switching, or KB re-encoding.
---


# KB Revision Loop


## Conceptual Role

This skill proposes executable revisions to the KB or hypothesis set when the current ontology or concept structure blocks progress.

## Framework Contribution

It contributes closed-loop repair by making failure trigger ontology changes rather than mere reranking of existing paths.

## How To Read Outputs

Read its outputs as repair programs for the knowledge representation, including patched artifacts that can seed the next run.

## Overview

Convert stagnation signals into explicit revision actions over concepts, definitions, and proof regimes.

Read [references/script-usage.md](references/script-usage.md) for deterministic execution.
Read [references/prompt-template.md](references/prompt-template.md) for narrative interpretation prompts.

## Output Contract

Emit JSON/Markdown with:

- `revision_actions`
- `priority_program`
- `revision_summary`

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `revise_ontology.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.

## Subgoal Control Decision

When revising a route or hypothesis, emit a `Subgoal Control Decision` that explains whether the revision should persist by adaptation, backtrack to a missing premise, pivot to another route family, quarantine as evidence-only material, or stop. Include target-object link, preserved commitments, blocker, learning from failure, next action, and demotion triggers.
