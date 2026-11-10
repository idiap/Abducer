---
name: proof-delivery-workflow-orchestrator
description: Orchestrate proof-delivery subworkflows for theorem-shaped queue items. Use when a discovery, result-elaboration, P vs NP, Yang-Mills, or general mathematical queue item is no longer asking for exploration but for a delivered proof packet, including theorem statement, definitions, lemma chain, proof attempt, inference-quality review, proof gap localization, and paper/report handoff.
---

# Proof Delivery Workflow Orchestrator

## Role

Use this skill after a queue item has become theorem-shaped. The goal is not to produce more strategy prose. The goal is to force a bounded proof outcome: proved theorem, conditional theorem, blocked named lemma, countermodel/no-go, or quarantine.

## Mathematical Invariants

Bind the proof-delivery mathematical object before routing: theorem candidate, source object, target object, definitions, carrier/model, quantifier order, validity regime, and paper/report insertion target. The orchestrator must preserve these invariants across subskills; any change in model, theorem strength, hypothesis set, or target relation creates a new proof obligation rather than a silent rewrite.

Edge cases and counterexample obligations must travel with the queue item. A proof-delivery run is not complete until the selected subworkflow has either checked them, converted them into named blocked lemmas, or produced a countermodel/no-go disposition.

## Epistemic Discipline

Treat proof delivery as an epistemic gate, not a productivity label. Every routed artifact must state its epistemic status, evidence citation, source artifacts, explicit unknowns, and validation handoff before it can be promoted.

If the literature gap, physical/conceptual payoff, prior-art boundary, or proof-quality gate fails, demote to repair, `needs_prior_art`, `return_to_discovery`, or `quarantine`. Do not let a proof-delivery run hide disconfirmation inside strategy language or continue recursively without a bounded proof outcome.

## Workflow

1. **Bind the queue item.** Record queue ID, target, source artifact, theorem-shaped claim, intended paper/report section, and why this item outranks broader exploration.
2. **Select proof subworkflow.** Route to:
   - `proof-obligation-formalizer` for definitions, assumptions, quantifiers, and non-claims;
   - `lemma-chain-proof-builder` for derivation;
   - `proof-gap-countermodel-splitter` when a lemma stalls;
   - `proof-quality-gatekeeper` before promotion;
   - domain-specific proof workflow such as `pvsnp-forcedrows-proof-workflow` when present.
3. **Separate proof from discovery.** Permit new conceptual moves only when they discharge a named proof gap. Do not let a proof-delivery run become a new marathon branch.
4. **Demand proof artifacts.** Require a structured proof packet with statement, definitions, assumptions, lemmas, proof steps, blocked obligations, countermodels, reviewer findings, and paper insertion target.
5. **Close with disposition.** Choose one: `proof_delivered`, `conditional_theorem_ready`, `blocked_at_named_lemma`, `countermodel_found`, `no_go_ready`, `needs_prior_art`, or `quarantine`.

## Queue Admission Criteria

Promote a queue item into proof delivery only if it has:

- a named source object and target object;
- a formal conclusion or no-go conclusion;
- a model/validity regime;
- at least one concrete lemma or calculation to attempt;
- a success criterion and a demotion criterion;
- a validation handoff.

Reject or return to discovery if the item only says to explore, compare, brainstorm, deepen, or look for promising routes.

## Output Contract

Return:

1. `Proof Delivery Target`: queue ID, theorem title, source object, target object, and target problem relation.
2. `Subworkflow Plan`: ordered skills and why each is needed.
3. `Proof Artifact Requirements`: exact fields the proof packet must contain.
4. `Stop Conditions`: what counts as proof, conditional proof, blocked lemma, countermodel, or quarantine.
5. `Paper/Report Handoff`: section, theorem label, appendix, or result packet to update.

## Failure/Demotion

Demote if the run repeats strategy language, lacks definitions, hides proof debt inside an assumption, skips inference review, or cannot state what would count as a delivered proof.
