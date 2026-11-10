---
name: proof-strategy-lockin-orchestrator
description: Freeze and run bounded proof-strategy cycles for a publication-worthy subgoal, then release the workflow back to conceptual exploration. Use after critical mass is reached.
---

# Proof Strategy Lock-In Orchestrator

Convert exploratory critical mass into a bounded completion cycle.

## Critical Conceptual Depth

Lock-in is justified only when the subgoal carries a sharp conceptual claim:
it proves a meaningful object exists, certifies transfer, explains an
obstruction, unifies a family, or draws a boundary that changes the route's
understanding. The orchestration should protect that core claim from
fragmenting into unrelated tasks.

## Value Signal

State the publication value before the cycle begins and re-evaluate it at the
end. The final state must say how the subgoal changes understanding, why it is
novel enough at its scope, and whether the completed result is coherent rather
than a bundle of disconnected artifacts.

## Guardrails

- Do not lock in without a frozen subgoal, non-claims, hard gates, cycle
  budget, stop conditions, and return-to-exploration trigger.
- Do not allow broad branch hopping while lock-in is active.
- Do not allow nested publication-consolidation. The default limit is four
  completion cycles with recursion depth one; side lemmas that do not fit the
  budget become blocked handoffs or return to exploration.
- Keep the local subgoal and the larger target problem visible in every
  consolidation cycle. For Yang-Mills, distinguish finite Route A results from
  the full OS/Wightman continuum construction and mass-gap obligation.
- If the subgoal is a transfer theorem, freeze anti-definitionality tests,
  required failure cases, consequence delta, and prior-art delta.

## Epistemic Discipline

- Cite evidence paths, learning-ledger events, KB ids, validators, and explicit
  unknowns.
- Label final state as publication_ready_subgoal, precise_demotion,
  blocked_named_lemma, no_publication_result, released_to_exploration, or
  quarantined.
- Preserve main-problem non-claims even when a subgoal is publication-ready.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when running validators, report
builders, manuscript integration, or deterministic artifact checks. Inspect
the produced artifacts and include executed commands in the validation
handoff.

## Output Contract

Return:

- `subgoal_statement`
- `non_claims`
- `locked_hard_gates`
- `allowed_cycle_types`
- `cycle_budget`
- `publication_consolidation_control`
- `main_problem_balance`
- `recursion_guard`
- `stop_conditions`
- `publication_target`
- `anti_definitionality_tests`
- `return_to_exploration_trigger`
- `final_state`
- `learning_events_to_write`
- `evidence`
- `validation_handoff`

## Failure/Demotion

Demote lock-in that completes a technically correct but conceptually inert
subgoal, especially a definition-built transfer theorem. Quarantine lock-in
plans that suppress needed conceptual exploration or blur the main-problem
boundary.
