---
name: proof-obligation-formalizer
description: Formalize theorem-shaped proof obligations before proof attempts. Use when a queue item, paper subgoal, no-go route, transfer lemma, or mathematical claim needs precise definitions, assumptions, quantifiers, model conventions, validity conditions, non-claims, and proof obligations before derivation can begin.
---

# Proof Obligation Formalizer

## Role

Turn an informal theorem-shaped task into a proof-ready obligation. This skill is the antidote to vague proof work: no derivation starts until the objects, quantifiers, and model are typed.

## Mathematical Invariants

Define the mathematical objects before inference begins: source object, target object, definitions, maps, parameters, proof system or analytic setting, validity regime, and non-claims. The invariant is statement fidelity: every extracted lemma must preserve the theorem's intended target relation without smuggling in a stronger conclusion, weaker premise, model switch, or target-equivalent assumption.

Each proof obligation must include edge cases and counterexample shapes that would falsify it. Undefined objects, unstable quantifiers, or ambiguous carriers block proof delivery until they are resolved or explicitly scoped away.

## Epistemic Discipline

Every obligation receives an epistemic status: `ready_for_lemma_chain`, `conditional`, `blocked_by_definition`, `blocked_by_quantifier`, `requires_prior_art`, or `quarantine`. Cite evidence source artifacts, KB IDs, literature-gap warrants, reports, or explicit unknowns supporting the formalization.

The validation handoff is to `lemma-chain-proof-builder` only when definitions, assumptions, non-claims, falsifiers, and model boundaries are explicit. Demote obligations that rely on disconfirmed assumptions, unstated prior art novelty, or hidden target-equivalent premises.

## Workflow

1. **State the theorem candidate.** Write the strongest honest conclusion and the weakest assumptions that might imply it.
2. **Define objects.** Define every source object, target object, relation, map, parameter, proof system, algebraic structure, topology, or model used in the statement.
3. **Set quantifiers.** Record all/existential order, fixed versus arbitrary parameters, finite versus asymptotic regimes, eventually versus infinitely often, uniform versus nonuniform, and advice/oracle status where relevant.
4. **List assumptions and non-claims.** Separate hypotheses used by the proof from background motivation. State what the theorem does not prove.
5. **Extract proof obligations.** Produce named lemmas with inputs, outputs, dependencies, and validation conditions.
6. **Emit falsifiers.** Name the smallest counterexample shape or edge regime that would invalidate the obligation.

## Output Contract

Return:

1. `Formal Statement`
2. `Definition Ledger`
3. `Quantifier And Model Ledger`
4. `Assumptions`
5. `Non-Claims`
6. `Named Proof Obligations`
7. `Falsifiers`
8. `Ready For Lemma Chain`: yes/no with blocker.

## Failure/Demotion

Demote if a theorem depends on undefined objects, changes model mid-proof, has stronger conclusion quantifiers than premise quantifiers, or treats a target-equivalent assumption as a genuine intermediate result.
