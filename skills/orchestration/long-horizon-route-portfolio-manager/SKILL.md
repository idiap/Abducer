---
name: long-horizon-route-portfolio-manager
description: Manage Abducer long-horizon hypothesis exploration as a target-relevance portfolio. Use when a route set, discovery loop, or candidate ranking must preserve essential target commitments, avoid low-value drift, budget active branches, and decide whether hypotheses enter proof queue, discovery branch, revision loop, watch/archive, quarantine, or rejection.
---

# Long-Horizon Route Portfolio Manager

## Conceptual Role

Use this skill to keep creative exploration tied to the target spine. Treat generated hypotheses as disposable portfolio items, but treat essential target commitments as non-disposable constraints that must be cited before a branch receives active attention.

## Inputs

- Essential target ledgers under `agentic/state/essential_target_ledgers/*.json`.
- Candidate rankings from `artifacts/hegelian/candidate_rankings.json` or `artifacts/hegelian/hypothesis_exploration_map.json`.
- Target packets, KB files, dependency graphs, and validation packets.
- Current route budgets, active branch count, and unresolved proof obligations.

## Procedure

1. Resolve the active target ledger and list its essential commitments.
2. For each candidate, name the mathematical object, route family, cited commitments, target-relevance score, drift risk, and active budget consumed.
3. Promote only candidates whose cited commitments cover the route's required target commitments and whose drift risk is not high.
4. Send low-relevance but valid ideas to `watch_archive`; send high-drift or uncited ideas to `quarantine` or `reject`.
5. Preserve conceptual creativity by keeping speculative branches visible, but prevent them from consuming proof-queue budget until they produce commitment-specific evidence.

## Guardrails

- Do not confuse novelty with value; a candidate that changes many concepts can still be low-value for the target.
- Do not let a branch enter `proof_queue` or `discovery_branch` without cited commitment IDs and inspected evidence paths.
- Do not collapse target commitments into a weaker problem unless the ledger explicitly marks that weakening as accepted.
- Do not treat workflow validity, generated prose, or artifact presence as theorem progress.

## Mathematical Invariants

- Preserve the target's essential commitments across route transformations.
- Track the mathematical object under transformation: theorem statement, bridge object, carrier, invariant, counterexample class, or proof obligation.
- Separate preserved invariants, broken invariants, accepted weakenings, and forbidden drift patterns.
- Test at least one edge case or boundary regime when a route changes representation or imports an analogy.

## Epistemic Discipline

- Label every route as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Cite KB IDs, dependency node IDs, validation packets, artifact paths, or explicit unknowns for every substantive promotion claim.
- Record disconfirming observations and demotion triggers before extending a branch budget.
- Keep uncertainty visible in reports so a fluent low-value route is not laundered into active proof progress.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md`.

- Run `python agentic/scripts/validate_target_relevance.py` when a ledger, candidate ranking, or route budget changes.
- Inspect `agentic/state/essential_target_ledgers/*.json`, `artifacts/hegelian/candidate_rankings.json`, and `artifacts/hegelian/hypothesis_exploration_map.json` after execution.
- Interpret the deterministic result generatively: state which commitments were preserved, which route families are over-budget, which branches drifted, and which obligations remain.

## Output Contract

Return:

1. `Target Spine`: commitment IDs, source evidence, and forbidden drift patterns.
2. `Portfolio Table`: candidate ID, route family, target-relevance score, drift risk, cited commitments, and routing decision.
3. `Promotion Decisions`: proof queue, discovery branch, revision loop, evidence task, watch/archive, quarantine, reject, or stop.
4. `Preserved Invariants`: commitments and mathematical objects that survived the route transformation.
5. `Broken/Unknown Invariants`: missing commitments, edge cases, counterexamples, or unvalidated representation shifts.
6. `Unresolved Obligations`: proof, source, validation, or target-relevance work needed before more budget is allocated.

## Failure/Demotion

Demote a route when it has no cited commitment IDs, target-relevance score below the active threshold, high drift risk with active routing, uncited source evidence, broken invariants, or a forbidden weakening. Falsify a portfolio decision if a later validator shows the branch no longer preserves an essential commitment.

## Validation Handoff

After making or changing a portfolio decision, run the target relevance validator and hand off unresolved failures as TODOs or validation packets rather than leaving them as narrative caveats.

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

For each active branch, state a `Subgoal Control Decision`: `persist_adapt`, `backtrack`, `pivot`, `quarantine`, or `stop`. Persistence is allowed only when the branch remains target-linked and the last failure teaches a sharper premise, object, regime, or bridge. Repeated identical blockers without new mathematical learning must force backtrack, pivot, quarantine, or stop.

## Best Machinery Assessment

For each active branch, aggregate its `Best Machinery Assessment`: `machinery_role`, `controlled_interface`, `why_best_available`, `premature_use_warning`, `required_bridge_obligation`, `invalid_use_modes`, and `validation_handoff`. Interpret the portfolio by role balance, not method count. Construction without transfer, witness without construction, and validation language without source objects should trigger restrategy, backtrack, pivot, or quarantine.
