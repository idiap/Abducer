---
name: completed-subgoal-enablement-auditor
description: Audit whether a completed, achieved, handoff-ready, or claimed subgoal genuinely enables progress on the larger Abducer target problem. Use when a result atlas entry, proof object, marathon cycle window, paper section, or queue item is being interpreted as a completed subgoal for P vs NP, Yang-Mills, or another target and the workflow must decide whether it is a necessary gate, reusable bridge, local-only result, side contribution, or overclaimed proxy.
---

# Completed Subgoal Enablement Auditor

## Role

Use this skill to decide whether a completed subgoal is actually enabling for the bigger problem. The point is not to praise completion. The point is to identify the exact target gate that is now open, still closed, or shown to be impossible.

An enabling subgoal must change the proof architecture, route portfolio, validation burden, or paper handoff for the target. A result can be valuable and still not be enabling.

## Evidence To Load

Prefer current repo artifacts over memory or prose:

- `agentic/reports/result_subgoal_atlas/latest.json`
- `agentic/state/subgoals/<target-id>.json`
- `agentic/reports/discovery_marathon/latest.json`
- `agentic/reports/timeline_paper/latest.json`
- proof-delivery queues such as `agentic/reports/pvsnp_proof_delivery_queue/latest.json`
- the source cycle, proof packet, report section, or manuscript fragment being audited

If artifacts disagree, preserve the disagreement as an audit finding instead of smoothing it away.

## Enablement Classes

Classify the completed subgoal as exactly one primary class:

- `target_gate_opened`: a named necessary gate for the bigger problem is now discharged or narrowed to a smaller finite obligation.
- `bridge_enabled`: a source object, target object, and transfer/reconstruction map are now explicit enough for the next proof step.
- `route_decision_enabled`: the result decides whether to continue, backtrack, quarantine, or pivot a route family.
- `paper_handoff_enabled`: the result is not the main theorem but is mature enough to support a scoped paper section or note.
- `validation_enabled`: the result creates a concrete validator, falsifier, countermodel, or proof-quality gate.
- `local_value_only`: the subgoal is completed but does not currently unlock a larger target step.
- `proxy_or_overclaim`: the subgoal is being treated as enabling without a valid source-to-target handoff.

Use secondary tags only after choosing the primary class.

## Audit Procedure

1. State the completed subgoal in its smallest honest form.
2. Identify the larger target commitment it is supposed to enable.
3. Name the precondition that existed before completion.
4. Name the postcondition that is now true.
5. Check whether the postcondition is actually used by a next theorem, transfer, falsifier, validation gate, route decision, or paper handoff.
6. Separate direct enablement from indirect value:
   - direct: without this subgoal, a named next proof step could not proceed;
   - indirect: it improves understanding or packaging but does not discharge a gate;
   - negative: it rules out a route or exposes a countermodel;
   - none: it is complete but not target-enabling.
7. State remaining blockers that prevent the completed subgoal from enabling the bigger problem.
8. Decide whether the next workflow action is `use`, `package`, `validate`, `extend`, `backtrack`, `quarantine`, or `stop`.

## Mathematical Invariants

Preserve the mathematical object under audit:

- target identity;
- source object and target object;
- transfer, reduction, reconstruction, or validation map;
- quantifier regime and model assumptions;
- non-claim boundary;
- evidence path and cycle/proof-object ids;
- status distinction between achieved, handoff-ready, partially achieved, open, blocked, falsified, and quarantined.

Never mark a subgoal enabling merely because it is complete, elegant, difficult, or reportable.

Treat edge case, counterexample, boundary regime, and failure regime evidence as decisive. A completed subgoal that fails on the first boundary regime may still be useful, but it should not be labeled target-enabling.

## P Vs NP Checklist

For P vs NP, ask:

- Does the completed subgoal name the source carrier or proof system?
- Does it name the target class, SAT/NP-complete target, circuit model, and length map?
- Does it preserve all-exponent or nonuniform quantifiers without advice leakage?
- Does it establish a transfer inequality, bounded-window obstruction, searchable-certificate gate, countermodel, or barrier-specific no-go?
- Does it avoid implying `P != NP`, `SAT notin P/poly`, or arbitrary lower bounds unless those are actually proved?
- Does the result enable the proof-delivery queue, proof-object frontier, or paper module to shrink?

## Yang-Mills Checklist

For Yang-Mills, ask:

- Does the completed subgoal act inside the same theory or only on a finite/proxy object?
- Does it name the Wilson observable family, OS/reflection positivity object, continuum/reconstruction handoff, or spectral-gap obligation?
- Does it discharge a finite positivity obstruction, same-theory transfer, uniform remainder, OPE coefficient, or nontriviality witness gate?
- Does it avoid implying existence or mass gap from a fixed-cutoff or analogy-only result?

## Output Contract

Return:

1. `Completed Subgoal`: id, smallest honest claim, achievement status, evidence paths.
2. `Bigger Problem Link`: target commitment, source object, target object, and transfer or validation map.
3. `Before/After Gate`: precondition before completion and postcondition after completion.
4. `Enablement Class`: one primary class plus optional secondary tags.
5. `Enablement Mechanism`: exactly how the completed subgoal changes the next proof, validation, route, or paper step.
6. `Residual Blockers`: what remains open before the larger target advances.
7. `Overclaim Boundary`: what the completed subgoal does not prove.
8. `Next Action`: use, package, validate, extend, backtrack, quarantine, or stop.
9. `Atlas Update`: suggested `achievement_status`, enablement note, open obligations, promotion criteria, and demotion criteria.
10. `Validation Handoff`: validator, proof queue item, timeline section, paper section, or TODO that should carry the next step.

## Epistemic Discipline

Use epistemic status labels: `enabled`, `partially_enabled`, `route_deciding`, `paper_handoff_ready`, `local_value_only`, `blocked`, `quarantined`, or `proxy_or_overclaim`.

Every enablement claim must cite evidence: artifact paths, KB IDs, cycle IDs, proof-object IDs, source artifacts, validators, or explicit unknowns. Keep achievement status separate from enablement status; a completed local result can still fail to enable the larger target.

## Failure/Demotion

Demote to `local_value_only` or `proxy_or_overclaim` when the audit cannot name a target commitment, source object, target object, transfer map, postcondition, evidence path, or next consuming proof step.

Do not demote solely because the subgoal is intermediate. Intermediate work is enabling when it opens a necessary gate.
