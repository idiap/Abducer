---
name: abducer-refinement-route-ranker
description: Rank validated Abducer creative candidates into proof queue, discovery branch, revision loop, evidence task, quarantine, rejection, or stop dispositions. Use when hypothesis-space exploration must become work-loop actions and Looper-visible route decisions.
---

# Abducer Refinement Route Ranker

## Role

Choose continuation routes from validation evidence. Ranking is a control-plane
decision over the hypothesis exploration space, not a proof of the candidate.

## Workflow

1. Read candidates, validation packets, epistemic statuses, and source pressure.
2. Score expected target contribution, validation strength, risk, and tractability.
3. Select one disposition: `proof_queue`, `discovery_branch`, `revision_loop`, `evidence_task`, `quarantine`, `reject`, or `stop`.
4. Record whether the candidate changed routing behavior.
5. Emit work-loop and Looper graph evidence.

## Guardrails

- Rank validated route value over elegance.
- Quarantine failed hard gates.
- Keep exploratory candidates out of proof queue until proof-form obligations are explicit.
- Record residual risks and rejected alternatives.

## Output Contract

Emit `abducer_candidate_ranking` objects and update `conceptual_refinement_trace` through `agentic/scripts/build_hypothesis_exploration_map.py`.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Do not let a fluent or busy workflow consume horizon budget without target relevance, evidence, and validation handoff.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: workflow route, active target ledger, skill sequence, route budget, state artifact, and candidate disposition.
- Preserved invariants: target commitments, route order, budget boundaries, evidence handoffs, and stop/quarantine conditions.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: selected route, target-relevance and drift-risk evidence, skill sequence, executed commands if any, produced artifacts, unresolved obligations, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote routes that exceed budget, omit commitment citations, skip validators, or drift into low-value hypotheses.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.

## Subgoal Control Decision

Whenever a candidate, formula, route subclaim, or proof obligation is ranked, emit a `Subgoal Control Decision` with: `decision` (`persist_adapt`, `backtrack`, `pivot`, `quarantine`, or `stop`), `target_object_link`, preserved commitments, current blocker, learning from failure, next action, backtrack trigger, pivot trigger, quarantine trigger, stop condition, and validation handoff. Route disposition must be compatible with this decision: proof queue and discovery branch require `persist_adapt`; quarantine requires `quarantine`; rejection or terminal stop requires `stop` or `quarantine`.

## Best Machinery Assessment

When ranking a route, preserve or emit a `Best Machinery Assessment` with `machinery_role`, `controlled_interface`, `why_best_available`, `premature_use_warning`, `required_bridge_obligation`, `invalid_use_modes`, and `validation_handoff`. A route is rankable only when the selected machinery controls the current bottleneck against the active target-object contract. Method prestige, historical relevance, or fluent abstraction language is not enough without a proof role and interface.
