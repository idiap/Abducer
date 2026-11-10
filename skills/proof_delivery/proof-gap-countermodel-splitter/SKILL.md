---
name: proof-gap-countermodel-splitter
description: Split blocked proof gaps into repair lemmas, countermodels, no-go theorems, or quarantine decisions. Use when a proof-delivery run cannot complete a lemma and needs to decide whether to adapt the statement, prove a smaller lemma, construct a counterexample, convert the branch into an impossibility theorem, or stop.
---

# Proof Gap Countermodel Splitter

## Role

Use this skill when a proof attempt blocks. Its job is to avoid infinite proof-churning by deciding what the block means.

## Mathematical Invariants

Keep the blocked mathematical object fixed while splitting the gap: exact lemma statement, premises, desired conclusion, dependency location, model, quantifiers, and parameters. A repair is valid only if it states which invariant changes and why the new statement still serves the theorem; otherwise the branch must become a counterexample, no-go candidate, or quarantine decision.

Countermodel search is not optional. Test edge cases, toy models, degeneracies, proxy/oracle variants, model-switch cases, and adversarial parameter regimes before classifying the gap as merely missing technique.

## Epistemic Discipline

Assign an epistemic status to the gap: `repairable`, `blocked`, `likely_false`, `countermodel_found`, `needs_prior_art`, `no_go_candidate`, or `quarantine`. Cite evidence source artifacts, KB IDs, proof packets, validator outputs, or explicit unknowns for the classification.

The validation handoff must name the next proof action and the disconfirmation criterion. If no bounded repair, countermodel, no-go theorem, or quarantine test can be stated, demote the branch instead of allowing another vague cycle.

## Workflow

1. **Name the blocked lemma.** State the exact premise, desired conclusion, and where it is used.
2. **Classify the gap.** Choose: missing definition, missing estimate, missing transfer, wrong quantifier, model mismatch, advice/proxy leakage, known barrier, or likely false statement.
3. **Search for countermodels.** Construct the smallest edge case, toy model, oracle/proxy model, degeneracy, finite example, or adversarial parameter regime that would falsify the lemma.
4. **Try one repair.** If repair is plausible, weaken assumptions or conclusion exactly once and state the new lemma.
5. **Choose route disposition.** Use `repair_lemma`, `countermodel`, `no_go_theorem`, `prior_art_needed`, `quarantine`, or `return_to_discovery`.

## Output Contract

Return:

1. `Blocked Lemma`
2. `Gap Type`
3. `Countermodel Search`
4. `Repair Candidate`
5. `No-Go Candidate`
6. `Disposition`
7. `Next Proof Action`

## Failure/Demotion

Demote if the split leaves the branch in "needs more thinking" without a concrete lemma, countermodel, no-go statement, or quarantine criterion.
