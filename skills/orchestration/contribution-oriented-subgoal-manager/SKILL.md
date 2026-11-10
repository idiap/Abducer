---
name: contribution-oriented-subgoal-manager
description: Keep a long-horizon Abducer workflow always aiming at at least one independently valuable scientific subgoal. Use when branch scheduling, next-analysis queues, or marathon loops need metrics for contribution potential, conceptual novelty, explanatory power, implication payoff, and certification progress.
---

# Contribution-Oriented Subgoal Manager

## Conceptual Role

Use this skill to make standalone scientific contribution production a standing loop objective. The loop should always know which active subgoal could become a contribution, what type of contribution it is, what would certify it, and which metric is currently blocking it.

This does not mean every cycle must be a paper result. It means every active cycle should either:

- advance a contribution candidate,
- sharpen a contribution disqualifier,
- certify or demote a candidate,
- or explain why no contribution-shaped subgoal is currently reachable.

## Guardrails

- Do not optimize for contribution labels at the expense of target relevance.
- Do not count activity, long runtime, or report generation as contribution progress.
- Do not mark a candidate as certified without evidence and disqualifier checks.
- Do not stop hard but promising branches prematurely; contribution potential can increase after backtracking or falsifier discovery.
- Do not allow infinite branch progression. Every active branch must carry a contribution candidate, a contribution-search move, or an explicit demotion test.
- Do not keep adapting a branch after it has reached the smallest defensible contribution claim; switch to validation, prior-art checking, paper handoff, or archive.

## Good-Enough And Stop Policy

A branch is `publishable_handoff_ready` only when the smallest honest claim is clear, the mathematical object is named, the assumptions and scope are stated, the evidence basis is cited, the prior-art boundary is checked, disqualifiers are resolved or explicitly bounded, the overclaim boundary is explicit, and the paper-note shape can be written without pipeline jargon.

Use three maturity levels:

- `contribution_shaped`: the branch has an externally meaningful object, but validation and novelty gates are not close enough for paper handoff.
- `near_stepping_stone`: one or two bounded prior-art, disqualifier, proof-shape, or validation tasks could make the result paper-note ready.
- `publishable_handoff_ready`: broad exploration should stop for that branch; route budget should move to validation, prior-art, and manuscript packaging.

A branch should `continue` only when the next cycle can plausibly improve at least one monitored dimension: conceptual novelty, explanatory power, implication payoff, validation readiness, target relevance, or disqualifier resolution.

A branch should `adapt` when it remains relevant but the current formulation is too broad, under-typed, or missing a discriminating experiment.

A branch should `backtrack` when the main obstruction is not the idea but a hidden premise, proxy shift, missing source object, missing target object, or invalid transfer.

A branch should `quarantine` when it depends on analogy, a weaker problem, unresolved prior-art risk, or an unverified transfer certificate.

A branch should `stop` when, after at least two explicit adaptation or backtracking attempts, it still cannot name a contribution candidate, a contribution-disqualifying test, or a target-preserving validation handoff.

Never stop solely because proof debt is hard. Stop only when the branch cannot convert hard proof debt into a bounded contribution, falsifier, bridge, probe, or explanatory mechanism.

## Metrics To Monitor

Track:

- `active_candidate_count`: how many contribution-shaped subgoals are alive.
- `contribution_shaped_count`: candidates with an independently meaningful object.
- `near_stepping_stone_count`: candidates close to paper-note readiness after bounded gates.
- `publishable_handoff_count`: candidates that should move out of broad exploration.
- `certification_ready_count`: candidates with enough evidence and bounded missing checks.
- `average_contribution_score`: composite of novelty, explanatory power, implications, validation, and target relevance.
- `average_publishable_subgoal_score`: maturity-weighted score after hard-gate penalties.
- `novelty_pressure`: highest conceptual novelty among active candidates.
- `explanatory_gain`: whether recent cycles clarified a mechanism or failure.
- `implication_payoff`: whether a candidate changes next analyses, route portfolio, or paper argument.
- `validation_gap`: strongest missing evidence, prior-art, or disqualifier check.
- `staleness`: cycles since any candidate improved or was demoted.
- `good_enough_count`: backward-compatible count of publishable handoff candidates.
- `infinite_progression_risk`: branches that keep consuming cycles without improving a contribution metric or resolving a disqualifier.

## Procedure

1. Load current story beats, ranked next analyses, qualitative graph, big-deal archive, and contribution monitor if present.
2. Ensure at least one active next analysis is explicitly tied to a contribution candidate or a contribution-disqualifying test.
3. Route branches so the best candidate receives budget unless target relevance, validation, or drift risk fails.
4. If no candidate exists, force a contribution-search move: bridge lemma search, obstruction search, reusable probe, conceptual reframing, or method paper handoff.
5. If a candidate is `near_stepping_stone`, route the next budget to the missing hard gate, not broad exploration.
6. If a candidate is `publishable_handoff_ready`, stop exploratory cycling on that branch and hand it to validation, prior-art, or paper packaging.
7. Promote, adapt, backtrack, quarantine, or stop contribution candidates using evidence and disqualifiers, not enthusiasm.

## Epistemic Discipline

Use status labels: `active_candidate`, `contribution_search_needed`, `certification_ready`, `near_certification`, `blocked_by_validation`, `blocked_by_prior_art`, `quarantine`, `rejected`, or `certified_contribution`.

Every metric must cite evidence paths, cycle IDs, report fields, validators, or explicit unknowns.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md`. Run `python agentic/scripts/build_scientific_contribution_monitor.py` and inspect the resulting `agentic/reports/scientific_contribution_monitor/latest.json` before changing contribution routing decisions.

## Output Contract

Return:

1. `Contribution Portfolio`: active candidates, contribution types, scores, and statuses.
2. `Loop Objective`: which candidate or contribution-search move should guide the next cycles.
3. `Metrics`: contribution score, novelty, explanatory power, implications, validation gap, and staleness.
4. `Good Enough Boundary`: the smallest contribution claim, handoff threshold, remaining bounded validation, and why further exploration would or would not be waste.
5. `Routing Decision`: continue, adapt, backtrack, pivot, quarantine, stop, handoff, or launch contribution search.
6. `Evidence And Unknowns`: artifacts and explicit unknowns behind every metric.
7. `Validation Handoff`: contribution monitor, queue update, paper handoff, prior-art pass, or TODO.

## Failure/Demotion

Demote a candidate or route when metrics are high only because of generic wording, when no evidence changed, when target relevance is absent, when prior-art risk is unexamined, or when validation gaps remain unbounded.

## Validation Handoff

Run `python agentic/scripts/validate_scientific_contribution_monitor.py` after changing contribution metrics or route priorities.
