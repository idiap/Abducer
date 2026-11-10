---
name: next-experiment-queue-ranker
description: Rank Abducer next-experiment queues by target payoff, discriminating power, execution readiness, and anti-drift controls. Use when a discovery marathon, long-horizon loop, report tab, or branch scheduler needs to decide which queued experiment should run next and what concrete payoff criteria would justify promotion, adaptation, backtracking, quarantine, or stop.
---

# Next-Experiment Queue Ranker

## Conceptual Role

Use this skill to turn an accumulated queue of possible next experiments into an ordered control surface. The queue is not a todo list in chronological order; it is a portfolio of possible interventions on the current proof or discovery state.

Rank an experiment highly only when it can force a meaningful mathematical or conceptual decision. Prefer experiments that can decide a branch, expose a counterexample, certify a bridge condition, sharpen a source/target object, or produce a transferable calculation.

Use the same evaluation point to decide whether a branch should continue, adapt, backtrack, pivot, enter watch/archive, become a quarantine candidate, or become a stop candidate. Stop is a staged conclusion, not a default penalty for difficulty.

## Inputs

- Current next-experiment queue from `agentic/reports/discovery_marathon/latest.json`, `agentic/reports/discovery_marathon/latest.html`, or the embedded `marathon-data` payload.
- Cycle packets under `agentic/runs/discovery_marathons/*/cycles/*.json`.
- Active target ledger, dependency graph, branch memory, falsifiers, validation handoffs, and current report state.
- Queue item context: originating cycle, branch title, mathematical learning, blocking gap, falsifiers, equations, and selected skills.

## Ranking Procedure

1. Read the queue item together with its originating cycle, not as a standalone sentence.
2. Identify the mathematical object under pressure: bridge lemma, construction, observable, spectral witness, counterexample class, estimate, transfer certificate, or validation artifact.
3. Score target payoff by asking whether success would change the route state: promote, persist/adapt, backtrack, pivot, quarantine, or stop.
4. Score discriminating power by asking whether failure teaches something precise rather than merely saying the problem remains hard.
5. Score execution readiness by asking whether the experiment names an operation that can be run or derived: compute, construct, extract, bound, test, compare, certify, or falsify.
6. Score target integration by checking cited commitments, source object, target object, same-theory transfer, and validation handoff.
7. Penalize broad certification requests, generic literature searches, analogies without transfer certificates, repeated blockers, and experiments that do not name a decision criterion.
8. Emit payoff criteria before recommending a run. A ranked item without payoff criteria is not ready for long-horizon budget.
9. Emit a branch-continuation decision: `continue_run_next`, `adapt_then_run`, `backtrack_to_sharpen`, `watch_archive_until_sharpened`, `quarantine_candidate`, or `stop_candidate_after_repeat_low_payoff`.
10. Before any stop candidate is accepted, state what would rescue the branch from stopping.

## Payoff Criteria

For each ranked queue item, state at least two payoff criteria:

- `Decision payoff`: what result would promote, persist/adapt, backtrack, pivot, quarantine, or stop the branch.
- `Mathematical payoff`: what object, formula, estimate, counterexample, or proof obligation becomes sharper.
- `Evidence payoff`: what artifact, source, computation, or validator would support or disconfirm the claim.
- `Anti-drift payoff`: what target commitment or same-theory condition prevents the experiment from becoming a low-value side quest.

When possible, phrase payoff criteria as falsifiable tests: "If determinant \(D<0\), quarantine the positivity route"; "If the same-theory transfer certificate cannot name the target observable algebra, backtrack"; "If the estimate is only fixed-cutoff, keep the result as evidence rather than proof progress."

## Continuation And Stop Control

Use ranking as a branch-control decision point, but avoid premature stopping.

Prefer `continue_run_next` when an experiment has a concrete decision test and high target payoff. Prefer `adapt_then_run` when the branch remains target-linked but the experiment is too broad. Prefer `backtrack_to_sharpen` when the branch touches an important object but needs a smaller premise, estimate, or falsifier. Prefer `watch_archive_until_sharpened` when the idea is plausible but not ready for active budget.

Use `stop_candidate_after_repeat_low_payoff` only when all of the following hold:

- Repeated evaluations keep the branch low-payoff after at least one adaptation or sharpening attempt.
- The branch cannot name a target-preserving source object, target object, validation handoff, or decision criterion.
- Recent failures no longer sharpen definitions, assumptions, regimes, estimates, falsifiers, or bridge obligations.
- Stopping the branch would not abandon the only active route to an essential target commitment.

Do not stop a branch merely because it is hard, slow, mathematically ambitious, or currently blocked. A hard blocker that teaches the correct missing premise is a reason to adapt or backtrack, not to stop.

## Guardrails

- Do not rank by recency, fluency, branch popularity, or ease alone.
- Do not treat a queue item as high value unless it names a target-relevant mathematical object and a decision it can force.
- Do not let a broad "certify the weakest condition" item outrank a concrete finite calculation unless it has been rewritten into a named premise test.
- Do not treat empirical, analogical, or numerical evidence as proof progress without a transfer certificate.
- Do not hide low-payoff items; keep them visible as watch/archive or sharpening tasks.
- Do not stop a branch without repeat evidence, a failed sharpening attempt, and a stated rescue condition.

## Mathematical Invariants

- Mathematical object: the queued experiment plus its source branch, source object, target object, formulas, falsifiers, and validation handoff.
- Preserved invariants: target commitments, same-theory transfer, typed source/target objects, explicit decision criteria, and falsifiable payoff criteria.
- Broken invariants: missing observable algebra, hidden proxy shift, fixed-regulator result presented as continuum progress, analogy without transfer, or a calculation that cannot affect a branch decision.
- Edge case: a low-scoring queue item may still be urgent if it blocks every high-scoring route; label it `infrastructure_blocker` rather than pretending it has mathematical payoff.
- Edge case: a branch may deserve continuation even after repeated failures when each failure localizes a new invariant, boundary regime, counterexample class, or proof obligation.

## Epistemic Discipline

Label every queue item with an epistemic status: `ready_to_run`, `needs_sharpening`, `evidence_task`, `proof_obligation`, `blocked`, `watch_archive`, `quarantine`, or `rejected`.

Cite evidence paths, KB IDs, cycle IDs, branch IDs, equations, validators, or explicit unknowns for every ranking decision. Preserve disconfirming observations and demotion triggers in the output. If the ranking depends on an assumption, state the assumption and the validator or artifact that could falsify it.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the ranking.

- Run `python agentic/scripts/generate_discovery_marathon_html.py` after queue-ranking report changes.
- Run `python agentic/scripts/validate_discovery_marathon_report.py` to verify ranked queue shape, payoff criteria, and renderability.
- Run `python agentic/scripts/validate_discovery_marathon_skill_dispatch.py` when dispatch requirements change.
- Inspect the produced HTML or embedded payload before interpreting the deterministic run.

## Output Contract

Return:

1. `Ranked Queue`: rank, cycle ID, branch, priority score or band, and epistemic status.
2. `Why This Target`: the target-relevance and decision-value reason for each high-ranked item.
3. `Payoff Criteria`: concrete success, failure, and anti-drift criteria.
4. `Required Skills`: skills to invoke before or during the experiment.
5. `Branch Continuation Decision`: continue, adapt, backtrack, pivot, watch/archive, quarantine candidate, or stop candidate.
6. `Premature-Stop Guard`: explicit conditions under which the branch must not be stopped yet.
7. `Stop Criteria`: repeat-evidence conditions required before stopping is licensed.
8. `Demotion/Backtrack Triggers`: what would lower the item, quarantine it, or force a pivot.
9. `Validation Handoff`: report, validator, artifact, or cycle packet that must record the decision.

## Failure/Demotion

Demote a queue item when it lacks a target object, has no falsifiable payoff criterion, repeats a previous blocker without new mathematical learning, requires unbounded exploration, shifts to another theory, or only promises generic literature/background value. Quarantine an item when its success would solve a different problem than the active target. Mark an item as a stop candidate only after repeat low-payoff evidence and a failed sharpening attempt. Falsify the ranking if a later validator shows missing payoff criteria, missing required skills, missing premature-stop guards, or sorted priority disagreement in the report payload.

## Validation Handoff

End by naming the next validator or artifact that controls the queue. For marathon reports, the handoff is `agentic/scripts/validate_discovery_marathon_report.py` plus the ranked queue embedded in `agentic/reports/discovery_marathon/full_timeline.html`. For future cycles, the handoff is the `branch_selection` dispatch phase and the next persisted cycle packet.
