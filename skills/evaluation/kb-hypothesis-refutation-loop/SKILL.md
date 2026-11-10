---
name: kb-hypothesis-refutation-loop
description: Run iterative hypothesis-validation rounds after `phyp` generation to drive hypotheses toward supported/refuted outcomes. Use when the user asks for multi-round testing, convergence over hypotheses, pruning low-yield hypotheses, or systematic refutation loops over `phyp/*.proof-hypotheses.yaml`.
---


# KB Hypothesis Refutation Loop


## Conceptual Role

This skill iterates over current proof hypotheses to support, weaken, refine, or refute them across multiple rounds.

## Framework Contribution

It contributes persistence and theory revision pressure by preventing the system from leaving generated hypotheses unevaluated after a single pass.

## How To Read Outputs

Read its outputs as the evolving status history of the current hypothesis set and as a signal of where the framework is still underdetermined.

## Overview

Run a round-based post-`phyp` loop that repeatedly evaluates unresolved hypotheses until convergence or round budget exhaustion.

Read [references/loop-policy.md](references/loop-policy.md) for loop semantics.
Read [references/script-usage.md](references/script-usage.md) for execution.
Read [references/prompt-template.md](references/prompt-template.md) for orchestration prompts.

## Workflow

1. Initialize loop state.
Load KB statements, hypothesis payload, and optional connector analysis scores.

2. Evaluate unresolved hypotheses per round.
Run support/refutation scoring only on unresolved items.

3. Update statuses.
Write status transitions to hypothesis records with per-round evaluation history.

4. Tighten or relax decision policy.
Adjust thresholds by round; optionally emit provisional final-round outcomes.
By default, rounds after the first require new evidence files.

5. Emit loop artifacts.
Persist JSON + Markdown round reports and reviewed hypothesis YAML.

## Guardrails

- Keep each verdict auditable with explicit scores and reasons.
- Never drop hypotheses silently; unresolved hypotheses remain visible.
- Preserve hypothesis IDs and provenance.
- Treat supported outcomes as loop-level evidence, not formal theorem proofs.

## Output Contract

Return:

1. `Round Summaries`
2. `Final Status Counts`
3. `Promotion Candidates`
4. `Refutation Candidates`
5. `Updated Hypothesis File`

Use `scripts/iterate_hypotheses.py` for deterministic outputs.

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `iterate_hypotheses.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.

## Subgoal Control Decision

For each unresolved or refuted hypothesis, emit a `Subgoal Control Decision`. Use `persist_adapt` when a failed check sharpens a premise, object, or bridge; `backtrack` when the hypothesis assumed an unbuilt premise; `pivot` when repeated failures stop teaching the target; `quarantine` when evidence or analogy is not proof-authorized; and `stop` when the hypothesis no longer has a target-object link.
