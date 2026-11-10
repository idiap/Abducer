---
name: kb-end-to-end-proof-critic
description: Assess whether the current artifact chain supports a plausible end-to-end proof of the main conjecture. Use when the user asks if the current route is close to a real solution, what still blocks end-to-end plausibility, or whether the system should stop because a plausible solution has been found.
---

# KB End-To-End Proof Critic

## Conceptual Role

This skill is the stop-rule and plausibility layer for the whole proof programme.
It does not ask whether a route is interesting.
It asks whether the current artifact chain is strong enough to count as a plausible end-to-end proof candidate.

## When To Use It

Use it when the current artifact set already contains:

1. `macro-proof-state.json`
2. `macro-strategy-report.json`
3. `proof-cycle-summary.json`
4. `InformalMathLib/<kb-ref>/index.json`
5. terminal proof attempts, if any

Use it when the user asks:

1. whether the main problem may already have a plausible solution;
2. what still blocks end-to-end proof plausibility;
3. whether the work loop should stop or continue.

## Workflow

1. Read the macro-proof and macro-strategy artifacts.
2. Read the proof-cycle summary, InformalMathLib, and terminal proof attempts.
3. Apply the critic panel from [references/critic-panel.md](references/critic-panel.md).
4. Evaluate the mandatory stop gates:
   grounded main conjecture,
   at least one terminal proved attempt,
   no open or partial completion items,
   no failed terminal critique judges.
5. Emit a plausibility report and stop decision.

Read [references/critic-panel.md](references/critic-panel.md) for the critic set and stop rule.
Read [references/prompt-template.md](references/prompt-template.md) for the inspection prompt shape.

## Guardrails

- Do not confuse a strong route programme with a plausible solved proof.
- Do not ignore open completion items just because one intermediate result is strong.
- Treat failed critique judges as blocking defects for end-to-end plausibility.
- Require explicit grounding from the route target back to the main conjecture.

## Deterministic Path

Use `scripts/generate_end_to_end_plausibility_report.py`.

Example:

```text
python skills/evaluation/kb-end-to-end-proof-critic/scripts/generate_end_to_end_plausibility_report.py --artifacts-dir artifacts/p-vs-np
```

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `generate_end_to_end_plausibility_report.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
