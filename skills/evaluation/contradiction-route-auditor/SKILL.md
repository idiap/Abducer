---
name: contradiction-route-auditor
description: Audit proof-by-contradiction routes before they enter proof queue. Use when a reductio branch needs checks for exact negation, same-theory preservation, valid conflict targets, excluded cases, and non-vacuous mathematical content.
---

# Contradiction Route Auditor

## Conceptual Role

This skill is the adversarial gate for reductio routes. It asks whether a
proof-by-contradiction branch really contradicts something accepted in the
same mathematical world, or whether it only sounds decisive because the route
changed objects, strengthened the negation, or imported a conflict target from
outside the active theory.

## When To Use

Use this skill before promoting any contradiction route to proof queue,
including routes produced by `kb-contradiction-strategist`, route packets in
the Yang-Mills long-horizon loop, or human-authored reductio sketches.

Read [references/audit-checklist.md](references/audit-checklist.md) before
returning a verdict.

## Audit Workflow

1. Check exact negation.
   Compare the target claim and the negated assumption for quantifier order,
   object identity, regime, constants, boundary conditions, and scope.

2. Check preserved commitments.
   Verify that the route keeps the same KB assumptions, construction family,
   cutoff/continuum status, observable algebra, Hilbert space, and source
   evidence unless a change is explicitly justified.

3. Check the contradiction carrier.
   Confirm that the selected object can actually carry the contradiction. For
   example, a spectral-gap reductio needs vectors, spectral measures, or dense
   observable-generated states in the reconstructed physical Hilbert space.

4. Check the conflict target.
   Determine whether the contradiction is against an accepted theorem, axiom,
   validator-backed artifact, or only against an aspiration. Missing conflict
   targets become proof obligations, not victories.

5. Check excluded cases.
   Identify boundary regimes, counterexample classes, null sectors, regulator
   artifacts, superselection sectors, non-dense observable families, and
   vacuous cases that could let the negated assumption survive.

6. Emit a verdict.
   Use promote only when the route has a precise negation, same-theory carrier,
   accepted conflict target, and explicit remaining obligations. Otherwise use
   repair, evidence-acquire, revise, quarantine, reject, or watch.

## Guardrails

- Do not approve a contradiction route because it is rhetorically plausible.
- Do not allow a contradiction across different cutoffs, limits, Hilbert
  spaces, observable algebras, gauges, or theories unless the bridge between
  them is itself proved.
- Do not treat a missing conflict target as an accepted theorem.
- Do not ignore cases where the negated assumption is stronger than the actual
  logical negation of the target.
- Do not collapse classical proof by contradiction into constructive witness
  construction; state the logic boundary explicitly when relevant.

## Mathematical Invariants

- Mathematical object: target claim, negated assumption, contradiction
  carrier, conflict target, preserved definitions, excluded cases, and proof
  obligations.
- Preserved invariants: quantifier order, same theory, same construction
  family, same observable algebra, same Hilbert space, same limiting topology,
  support/refutation status, and evidence provenance.
- Broken invariants: target/negation mismatch, unproved limit exchange,
  regulator-to-continuum slippage, hidden strengthening, cross-theory
  contradiction, density gap, and unsupported conflict target.
- Edge case or counterexample class: vacuous negation, null-vector quotient,
  isolated superselection sector, finite-volume artifact, strong-coupling-only
  estimate, and non-generating observable family.

## Epistemic Discipline

- Label each audited route as conjectural, evidence-backed, proof-obligation,
  blocked, refuted, promoted, quarantined, or watch/archive.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths,
  validator output, or explicit unknowns for every substantive finding.
- Separate workflow validity, artifact existence, route plausibility, and
  mathematical proof progress.
- Record disconfirming observations and demotion triggers even when the final
  verdict is repair or promote.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the
answer. Run deterministic validators or repository scripts only when they
directly test artifact freshness, schema validity, route packet presence, or
TODO linkage. After execution, state the mathematical consequence, epistemic
status, unresolved obligations, and next action.

## Output Contract

Return:

- `audited_route`: route ID, target, and source artifact.
- `negation_check`: pass, repair, or fail with exact mismatch if any.
- `same_theory_check`: pass, repair, or fail with preserved and broken
  invariants.
- `carrier_check`: whether the carrier can support the claimed contradiction.
- `conflict_target_check`: accepted, conjectural, missing, incompatible, or
  explicit unknown.
- `excluded_cases`: edge cases, counterexample classes, and boundary regimes.
- `proof_obligations`: obligations required before promotion.
- `disconfirming_observations`: what would demote or reject the route.
- `verdict`: promote, repair, evidence-acquire, revise, quarantine, reject, or
  watch.
- `validation_handoff`: validator, TODO, report, proof obligation, or stop
  condition for the next loop.

## Failure/Demotion

Demote on non-exact negation, hidden premise shift, object mismatch, broken
same-theory invariant, conflict against a merely desired theorem, unhandled
edge case or counterexample class, unsupported density claim, or missing
validation handoff.

## Validation Handoff

When a route passes, hand it to the relevant bridge-lemma packet, proof queue,
or long-horizon report with the remaining proof obligations attached. When it
fails, hand it to `kb-revision-loop`, `counterexample-hunter`,
`premise-completeness-prober`, or a TODO card that names the exact repair.

## Subgoal Control Decision

Audit and return the route's `Subgoal Control Decision`. A contradiction branch may stay active only if failure teaches a precise mathematical hinge such as density, closedness, nontriviality, or uniform decay. If the exact negation, same-theory invariant, carrier, or conflict target fails, return `backtrack`, `pivot`, `quarantine`, or `stop` with the demotion trigger.
