<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Critique Judges

Every terminal proof-cycle outcome must fill in all judge verdicts.

## 1. Statement Grounding Judge

Check:

1. The claim under test matches the queued claim.
2. Source and target statements are grounded in local statement ids or InformalMathLib entries.
3. Every proof step names its dependencies.

## 2. Tactic Goal-Control Judge

Check:

1. `normalize-goal` rewrites the task into the exact theorem or route-local statement under test.
2. `reduce-to-route-lemma` preserves sufficiency rather than weakening the queued claim.
3. `closure-check` returns to the original queued claim and rules out goal drift.

## 3. Inferential Validity Judge

Check:

1. Each step follows informally from what it cites.
2. Quantifiers and model assumptions are preserved.
3. The conclusion matches the exact target claim.

## 4. Assumption Discipline Judge

Check:

1. No hidden assumptions were introduced.
2. Any extra assumption is stated explicitly.
3. Conditional outcomes are labeled as conditional rather than unconditional proofs.

## 5. Citation Fidelity Judge

Check:

1. Every cited theorem, definition, or axiom matches the statement actually used.
2. Web-sourced references are recorded with exact source and role.
3. No step relies on a paraphrase that changes the mathematical content.

## 6. Proof Granularity Judge

Check:

1. Each proof step is small enough for expert inspection.
2. Jumps over route lemmas, reductions, or quantifier changes are explicitly marked as unresolved.
3. The argument does not hide the main burden inside vague phrases such as "it follows" or "one can show."

## 7. Tactic Trace-Discipline Judge

Check:

1. The informal tactic trace is updated from template state into a real trace with statuses and notes.
2. Each recommended tactic is either executed, explicitly skipped with a reason, or marked as blocked/deferred.
3. Tactic statuses agree with the written stepwise argument and final verdict.

## 8. Tactic Subgoal-Exposure Judge

Check:

1. `extract-subgoal` and `activate-target-theorem` expose exact intermediate claims and missing hypotheses.
2. `construct-witness` and `transport-invariant` state the witness, carrier, transport law, or obstruction explicitly.
3. A failed tactic becomes a named blocker or negative result rather than disappearing from the dossier.

## 9. Prior-Art And Novelty Judge

Check:

1. Whether the result is already present in local InformalMathLib or KB.
2. Whether web search is required under policy.
3. Whether the outcome should be downgraded to `prior_art_found`.

## 10. Local Counterexample-Search Judge

Check:

1. A local search for counterexamples, model mismatches, or barrier analogs was actually attempted.
2. The search names what was checked and what failed to falsify the claim.
3. If a nearby failure pattern exists, the argument explains why it does not apply.

## 11. Obstruction And Negative-Route Judge

Check:

1. Whether the proof survives the designated negative route.
2. Whether a counterexample, obstruction, or barrier defeats the claim.
3. Whether failure itself yields a usable negative result.

## 12. Contradiction And Impossibility Discipline Judge

Check:

1. A contradiction or impossibility route is used only when the negative-route heuristic justifies it as `parallel` or `negative-first`.
2. The decision is tied to a structural obstruction, barrier, transport failure, or non-realization claim rather than mere lack of progress.
3. If negation is used, the exact negated claim is stated explicitly.
4. If contradiction is used, the forbidden collapse, barrier, or inconsistency is named precisely.
5. If the constructive route fails, the dossier formulates a theorem-shaped impossibility or non-realization claim rather than only reporting `blocked`.

## 13. Closure Judge

Check:

1. Whether the outcome label is correct.
2. Whether the result statement is ready for persistence.
3. Whether the final summary is honest about the proof status.
