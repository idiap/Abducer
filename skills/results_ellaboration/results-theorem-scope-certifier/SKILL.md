---
name: results-theorem-scope-certifier
description: Certify the exact theorem scope of a paper-facing result candidate before proof, prior-art, or narrative work. Use when a discovery output or draft result may become a publishable subgoal but must first state the covered object, excluded object, hypotheses, non-claims, and promotion boundary.
---

# Results Theorem Scope Certifier

## Conceptual Role

This skill prevents an attractive result candidate from silently expanding into a stronger paper claim. It turns a candidate contribution into a scoped theorem packet with covered cases, excluded cases, hypotheses, proof obligations, and non-claims.

Use it before proof derivation, prior-art comparison, inference-quality review, or manuscript integration.

## Workflow

1. Identify the smallest honest claim.
2. Name the source object, target object, model/regime, and result form: theorem, no-go, finite certificate, obstruction, conditional theorem, or demotion.
3. Split the candidate into:
   - covered domain;
   - explicitly excluded domain;
   - conditional extension domain;
   - non-claim boundary.
4. State hypotheses in checkable form. Each hypothesis must connect to a proof step, disqualifier, or validation handoff.
5. Decide whether the result is ready for proof derivation, needs finite-object formalization, needs prior-art boundary first, or must be demoted.

## Recurring Pattern

For proof-route subgoals, distinguish:

- object-level result: what is actually proved for the named construction or method class;
- route-level implication: what the result says about a broader strategy;
- main-problem implication: what is not proved unless additional target commitments are discharged.

## Output Contract

Return: theorem-scope ID, smallest honest claim, covered domain, excluded domain, conditional extension domain, definitions needed, hypotheses, non-claims, proof obligations, disqualifier checks, downstream skills, and promotion boundary.

## Epistemic Discipline

Assign an epistemic status to the candidate: proved, conditional, scoped no-go, proof obligation, conjectural, blocked, or demoted. Cite evidence through source artifacts, KB IDs, cycle IDs, theorem labels, draft sections, validation reports, or explicit unknowns. The mathematical object and invariant under review must be named before any contribution claim is licensed.

## Guardrails

- Do not let "paper-worthy" mean broad. Prefer a narrow theorem with exact scope.
- Do not cover a stronger proof system, limit regime, model, or target class without an extraction or transfer theorem.
- Do not use vague boundaries such as "under suitable assumptions"; name the assumptions.
- Do not move to manuscript prose before the theorem packet has a proof or explicit proof debt.

## Validation Handoff

Hand off to `results-finite-object-formalizer` when the key object is not defined, to `results-proof-packet-deriver` when the statement is proof-ready, and to `results-prior-art-disqualifier-auditor` before novelty language.

## Failure/Demotion

Demote the candidate when the smallest honest claim is only a restatement of a route, when the covered domain cannot be named, when the excluded domain is doing the real work, or when the source obligation is equivalent to the target theorem.
