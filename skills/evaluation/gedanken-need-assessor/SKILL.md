---
name: gedanken-need-assessor
description: "Decide when Abducer should run a Gedanken experiment: an imagined but concrete situation that can expose a hidden assumption, variable dependence, regime shift, counterfactual contrast, or transfer boundary. Use before spending discovery budget on a thought experiment or when a branch is conceptually underdetermined."
---

# Gedanken Need Assessor

## Conceptual Role

Use this skill to decide whether a branch needs a Gedanken experiment. A Gedanken experiment is warranted when ordinary deduction, qualitative graph reasoning, or direct concrete probes have not yet made the decisive mechanism visible, but an imagined controlled situation could isolate the missing variable, contrast, or failure mode.

Do not use it as decoration. The result must be a budget decision: `design_now`, `defer_until_variable_typed`, `defer_until_regime_typed`, `run_concrete_probe_first`, `quarantine_as_analogy`, or `not_needed`.

## Functional Generation Requirements

Base the decision on live branch context whenever available: current blocker, target obligation, qualitative graph edge, recent falsifiers, next-experiment queue, and originating cycle or branch IDs. If those are absent, state that the assessment is a seed assessment and list what live context is missing. Do not reuse a seed packet without adapting its variables, contrast, and transfer boundary to the active branch.

## Need Criteria

Use `design_now` when at least two are true:

- The branch has typed variables or can type them locally, but the decisive mechanism remains conceptually opaque.
- A controlled contrast can separate two explanations, such as pairwise versus finite-family positivity.
- The situation can produce an expected observation that would change a next-cycle action.
- The insight can be transferred only with an explicit certificate, so overclaim risk can be controlled.

Use `defer_until_variable_typed` or `defer_until_regime_typed` when the imagined situation would merely hide missing definitions. Use `run_concrete_probe_first` when a small computation is already available and more informative. Use `quarantine_as_analogy` when no same-target transfer path can be stated.

## Mathematical Invariants

- Mathematical object: active branch, source object, target object, variables, regimes, relation edges, and proof obligations.
- Preserved invariants: target relevance, controlled contrast, held-fixed assumptions, validity regime, and explicit transfer scope.
- Broken invariants: analogy without transfer, untyped variables, missing observation, no follow-up decision, or proof claims from an imagined situation.
- Edge case or counterexample: a beautiful imagined situation is rejected if it cannot name what would disconfirm it.

## Epistemic Discipline

Assign epistemic status: `design_now`, `defer`, `concrete_probe_first`, `quarantine`, or `not_needed`. Cite evidence paths, KB IDs, cycle IDs, qualitative graph edges, validators, or explicit unknowns. A Gedanken experiment may justify a follow-up cycle; it does not prove the target.

## Output Contract

Return:

1. `Need Decision`: one of `design_now`, `run_concrete_probe_first`, `defer_until_variable_typed`, `defer_until_regime_typed`, `quarantine_as_analogy`, or `not_needed`.
2. `Need Assessment`: a schema-ready object with `decision`, `criteria_met`, `criteria_missing`, `rejected_alternatives`, and `why_not_direct_derivation_or_probe`.
3. `Candidate Contrast`: the variables or mechanisms the situation should separate.
4. `Required Preconditions`: variables, regimes, or transfer certificate needed before design.
5. `Expected Follow-Up Value`: what later cycle could do with the insight.
6. `Packet Provenance`: originating cycle IDs, branch IDs, affected node or edge IDs if already known.
7. `Validation Handoff`: `agentic/spec/gedanken_experiment_packet.schema.json` and `python agentic/scripts/validate_gedanken_experiment_packets.py`.

## Failure/Demotion

Demote when the proposed situation is generic inspiration, lacks a target object, cannot identify held-fixed variables, has no disconfirming observation, or would be a proxy problem. Quarantine if it is analogy-only. Reject any output that says the thought experiment proves the theorem.

## Validation Handoff

When design is licensed, hand off to `gedanken-situation-designer`. When the packet is produced, run `python agentic/scripts/validate_gedanken_experiment_packets.py` and feed the follow-up task to `gedanken-followup-planner` or the ranked queue.
