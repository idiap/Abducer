---
name: kb-contradiction-strategist
description: Build disciplined proof-by-contradiction routes for KB targets. Use when direct construction stalls, when a negated target may expose a spectral, compactness, density, positivity, nontriviality, or same-theory conflict, or when the discovery loop needs a reductio branch with explicit mathematical obligations.
---

# KB Contradiction Strategist

## Conceptual Role

This skill turns proof by contradiction from a vague tactic into a controlled
discovery route. It assumes the exact negation of a target, preserves the
ambient mathematical commitments, and searches for a contradiction that is
visible as a theorem-shaped conflict rather than a narrative discomfort.

## When To Use

Use this skill when:

1. a direct construction route has stalled but the negation of the target has
   mathematical structure;
2. a target can be re-expressed as excluding an obstruction, spectrum, null
   sector, degeneracy, collapse, or boundary regime;
3. a Yang-Mills route needs to test "no mass gap", "no OS-positive limit",
   "trivial continuum limit", or "non-dense observable sector" as structured
   assumptions;
4. the long-horizon loop needs a branch that can backtrack if the negated
   assumption survives.

Read [references/contradiction-route-template.md](references/contradiction-route-template.md)
before emitting a route packet.

## Workflow

1. State the target and exact negation.
   The negation must match the target's quantifiers, object, regime, and
   theory. If the negation is unclear, stop and emit a formalization TODO.

2. Preserve the commitments.
   List the KB statements, definitions, construction regime, cutoff/continuum
   status, observable algebra, Hilbert space, and invariants that remain valid
   under the temporary negated assumption.

3. Choose a contradiction carrier.
   Select the mathematical object that will carry the contradiction, such as a
   low-energy vector sequence, a spectral measure, a limiting Schwinger
   function, a compactness witness, a reflection-positivity quadratic form, a
   connected cumulant, or a gauge-invariant observable family.

4. Generate the impossible consequence.
   Derive a consequence of the negated assumption and preserved commitments.
   The consequence must conflict with an explicit theorem, axiom, accepted KB
   statement, validator-backed artifact, or named proof obligation.

5. Expose the proof obligations.
   Record every lemma needed to make the contradiction genuine, including
   density, closure, same-theory, uniformity, regularity, and limiting
   arguments.

6. Route the branch.
   Send theorem-shaped obligations to proof queue, missing source claims to
   evidence acquisition, object mismatch to revision, and weak or non-exact
   negations to quarantine.

## Contradiction Route Families

- Spectral-collapse reductio: assume no positive gap, construct normalized
  vacuum-orthogonal vectors psi_n with <psi_n,H psi_n> -> 0, and test conflict
  with cutoff-uniform Euclidean decay or spectral support exclusion.
- Positivity-failure reductio: assume the continuum object fails OS positivity
  and test whether reflection-positive approximants plus closedness of the
  limiting topology rule this out.
- Triviality-collapse reductio: assume all connected gauge-invariant cumulants
  collapse to the free/Gaussian pattern and test conflict with a same-theory
  nontriviality witness.
- Density-failure reductio: assume gauge-invariant observables do not generate
  the physical vacuum-orthogonal sector and identify the missing sector or
  superselection obstruction that must be explained.
- Compactness-obstruction reductio: assume no continuum subsequential limit and
  test conflict with tightness or precompactness estimates at the same
  regulator and observable level.
- Same-theory reductio: assume a route's witnesses belong to incompatible
  limiting objects and use this to demote the route rather than fake progress.

## Guardrails

- Do not write "assume not P" unless P has been formalized with the correct
  quantifiers and mathematical object.
- Do not derive contradiction by switching theories, cutoffs, Hilbert spaces,
  observable algebras, gauges, or limiting subsequences without naming that
  switch as a broken invariant.
- Do not treat a contradiction route as a proof; it is conjectural until every
  derivation step and conflict target is discharged.
- Do not use reductio to hide missing construction. If the contradiction
  requires an unproved existence theorem, emit that theorem as an obligation.
- Do not confuse contradiction with counterexample search: counterexamples
  attack the target, while reductio temporarily assumes the target's negation
  and searches for an impossible consequence.

## Mathematical Invariants

- Mathematical object: target statement, exact negation, preserved KB
  commitments, contradiction carrier, derived consequence, conflict target,
  proof obligations, and route disposition.
- Preserved invariants: theory identity, cutoff/continuum regime, observable
  algebra, Hilbert space reconstruction, quantifier order, assumptions,
  boundary conditions, and support/refutation status.
- Broken invariants: any object mismatch, quantifier strengthening, hidden
  compactness premise, unsupported density claim, unlicensed limit exchange,
  or conflict target imported from another theory.
- Edge case or counterexample class: vacuous contradiction, too-strong
  negation, regulator-only contradiction, free-theory collapse, superselection
  sector leakage, and non-dense observable families.

## Epistemic Discipline

- Label each route as conjectural, proof-obligation, evidence-backed, blocked,
  refuted, promoted, quarantined, or watch/archive.
- Record evidence paths using KB IDs, dependency node IDs, target packet IDs,
  artifact paths, validator output, or explicit unknowns for every substantive
  claim.
- Mark the contradiction target as accepted, conjectural, imported,
  validator-backed, or missing; a contradiction against a missing target is not
  progress until that target is established.
- Record disconfirming observations and demotion triggers before recommending
  proof queue promotion.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the
answer. Run deterministic validators or repository scripts only when they
directly ground route validity, artifact freshness, or TODO closure. After
execution, state the mathematical consequence, epistemic status, unresolved
obligations, and next action.

## Output Contract

Return:

- `target_claim`: the target statement and source evidence.
- `exact_negation`: the formal negated assumption, including quantifiers.
- `preserved_commitments`: definitions, KB IDs, artifacts, and invariants that
  remain in force.
- `contradiction_carrier`: the object expected to carry the contradiction.
- `derived_consequence`: the consequence generated from the negated assumption.
- `conflict_target`: the theorem, axiom, KB claim, validator-backed artifact,
  or explicit unknown it conflicts with.
- `proof_obligations`: lemmas needed to make the contradiction valid.
- `failure_modes`: ways the route could fail or be demoted.
- `disposition`: promote, repair, evidence-acquire, revise, quarantine, reject,
  or watch.
- `validation_handoff`: the validator, TODO, proof obligation, report, or stop
  condition that controls the next loop.

## Failure/Demotion

Demote on non-exact negation, object mismatch, hidden premise shift, broken
same-theory invariant, conflict against an unaccepted target, unsupported
limit exchange, vacuous contradiction, or absence of a falsifiable next
obligation.

## Validation Handoff

Hand off each route to `contradiction-route-auditor` before proof-queue
promotion. If the route is Yang-Mills-specific, also attach it to the active
bridge-lemma packet or long-horizon target report so the next recursive loop
can decide whether to pursue, repair, pivot, or backtrack.

## Subgoal Control Decision

Every reductio branch must include a `Subgoal Control Decision`. Use `persist_adapt` only when the exact negation, contradiction carrier, and conflict target remain same-theory and the failed attempt identifies a sharper density, closedness, nontriviality, or uniformity obligation. Use `backtrack`, `pivot`, `quarantine`, or `stop` when the branch assumes an unbuilt object, repeats without learning, relies on transfer-risk evidence, or loses target identity.
