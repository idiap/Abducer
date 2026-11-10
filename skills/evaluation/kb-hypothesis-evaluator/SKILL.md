---
name: kb-hypothesis-evaluator
description: Evaluate proof hypotheses generated in `phyp/*.proof-hypotheses.yaml` and classify each as supported, refuted, or inconclusive using KB structure, connector evidence, and optional coherence/explanatory signals. Use when the user asks to test hypotheses, validate bridge links, decide which hypotheses to promote, or produce hypothesis-level outcome reports after proof-hypothesis generation.
---


# KB Hypothesis Evaluator


## Conceptual Role

This skill evaluates generated proof hypotheses against connector, coherence, and KB evidence to classify them as supported, refuted, or inconclusive.

## Framework Contribution

It contributes disciplined triage so the workflow can retain only hypotheses that improve the inferential state of the theory.

## How To Read Outputs

Read its outputs as evidence-based hypothesis diagnostics; an inconclusive result means the hypothesis remains an open research obligation rather than a valid bridge.

## Overview

Run deterministic per-hypothesis evaluation over bridge, intervention, and conceptual-discovery hypotheses.

Read [references/scoring-rubric.md](references/scoring-rubric.md) for scoring logic.
Read [references/script-usage.md](references/script-usage.md) for execution.
Read [references/prompt-template.md](references/prompt-template.md) for narrative interpretation prompts.

## Workflow

1. Load KB + phyp payload.
Parse statement YAML blocks from `KB/*.kb.md` and all hypotheses from `phyp/*.proof-hypotheses.yaml`.

2. Compute support/refutation signals.
For bridge-link hypotheses, score dependency alignment, lexical overlap, evidence-term coverage, and connector score.
For intervention-focus hypotheses, score priority + cross-component leverage + downstream impact.
For conceptual kinds (`definition-introduction`, `representation-shift`, `intermediate-invariant`, `barrier-escape-principle`, `analogy-transfer`, `normal-form-reduction`), score novelty-aware support/refutation with contradiction and dependency checks.
If a coherence report is provided, apply explanatory/coherence adjustments before verdict classification.
Optionally ingest per-hypothesis round evidence from deduction/abduction results.

3. Classify outcomes.
Assign `supported`, `refuted`, or `inconclusive` (or provisional outcomes if force-resolution is enabled).

4. Emit actionable outputs.
Produce JSON + Markdown report and optionally updated hypothesis YAML with status transitions.

## Guardrails

- Keep every verdict tied to statement IDs and scored signals.
- Do not treat `supported` as formal proof; it is an evaluation result for loop routing.
- Keep refutation reasons explicit (missing IDs, direction conflict, contradiction signal).
- Preserve original hypothesis IDs and metadata.

## Output Contract

Return:

1. `Stats`
2. `Verdict Counts`
3. `Per-Hypothesis Results`
4. `Recommended Actions`

Use `scripts/evaluate_hypotheses.py` for deterministic outputs.

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `evaluate_hypotheses.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
