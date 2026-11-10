---
name: abstraction-fit-gap-auditor
description: Compare current, available, and possible new abstractions against a major conceptual proof gap. Use when a proof route may be using the wrong carrier, quotient, invariant, interface, model, or bridge object and needs a critical fit verdict before promotion, lock-in, or another discovery cycle.
---

# Abstraction Fit Gap Auditor

## Conceptual Role

Audit whether an abstraction actually fits the mathematical pressure it is
asked to carry. The skill is adversarial: it checks whether a candidate
representation preserves the target-relevant structure, exposes the hard
tension, and creates nontrivial proof obligations rather than defining success
into existence.

## Workflow

1. Start from a declared gap or concept-gap packet.
2. List candidate abstractions in three groups: current abstraction, available
   local/literature abstractions, and genuinely new abstraction candidates.
3. For each candidate, state what structure it preserves, what it hides, what
   operations it makes cheap, and what proof obligations it creates.
4. Test the candidate against the major conceptual tension, not only against
   local convenience.
5. Score fit by explanatory power, unification power, boundary sharpness,
   target preservation, proof obligation visibility, and efficiency.
6. Return a verdict: keep, refit, compose, forge-new, quarantine, or reject.
7. Hand viable candidates to `proof-bridge-object-forger`,
   `kb-gap-abstraction-conjecturer`, or
   `efficient-representation-requirements-elicitor`.

## Guardrails

- Do not compare abstractions only by name, familiarity, or elegance.
- Do not treat local convenience as target fit unless target-relevant
  invariants and failure regimes remain visible.
- Do not promote an abstraction whose cheapest proof path erases the target
  pressure, merges source and target semantics, or hides proof debt in a
  quotient.
- Do not skip available local or literature abstractions before recommending a
  new object.

## Mathematical Invariants

- Mathematical object: each abstraction candidate and the target object it must
  preserve.
- Preserved invariants: definitions, equivalence relations, symmetries,
  positivity, locality, uniformity, nontriviality, asymptotic regimes, transfer
  laws, or proof-system semantics required by the target.
- Broken invariants: any structure lost when passing through the abstraction,
  especially hidden quotienting, proxy substitution, regime drift, or
  definition-built target predicates.
- Edge case or counterexample: for every promoted or refit candidate, give a
  boundary regime or concrete failure case where fit would break.

## Efficient Fit Heuristics

An efficient representation is not merely shorter notation. It should compress
proof-relevant structure while keeping obligations visible.

- Object economy: few primitives, but not by hiding target assumptions.
- Operation closure: the operations needed by the proof stay inside the
  represented class or have explicit escape certificates.
- Invariant visibility: the main invariant can be inspected, transported, and
  falsified.
- Local computability: small examples, finite tests, or symbolic probes expose
  failure modes.
- Transfer sufficiency: source and target semantics remain independently
  meaningful.
- Literature fit: the abstraction explains how it differs from, refines, or is
  blocked by known approaches.

## Epistemic Discipline

- Cite evidence paths, KB IDs, target packets, branch IDs, proof-depth packets,
  prior-art notes, or explicit unknowns for each abstraction compared.
- Label each verdict as evidence-backed, conjectural, proof-obligation,
  blocked, demoted, quarantined, or rejected.
- Do not reward an abstraction for making the proof easy by erasing the problem.
- Require a disconfirming observation before any abstraction receives a promote,
  refit, or compose verdict.

## Output Contract

Return:

- `gap_statement`: the conceptual gap and the tension it must resolve.
- `objects_compared`: abstraction candidates and their source/target objects.
- `fit_matrix`: for each candidate, include preserved structure, lost
  structure, expressive gain, explanatory gain, unification gain, operation
  cost, proof obligations, edge case or counterexample, and evidence.
- `fit_verdict`: keep, refit, compose, forge-new, quarantine, or reject.
- `best_next_abstraction`: the candidate or new object family that should drive
  the next proof cycle.
- `requirements_missing`: what the best candidate still cannot represent.
- `disconfirming_tests`: what would falsify or demote the fit verdict.
- `epistemic_status` and `validation_handoff`.

## Codex Exec Protocol

When possible, inspect the local KB, bridge plans, proof-depth packets, target
profile, prior-art notes, and queue item before issuing the fit verdict. Use
deterministic scripts only when they already generate one of those artifacts;
otherwise perform a generative audit and make the evidence paths or explicit
unknowns part of the output.

## Failure/Demotion

Demote abstraction comparisons that only rank labels, ignore broken invariants,
omit edge cases, or skip available local/literature candidates. Quarantine any
candidate whose definition already includes the desired theorem-level
conclusion.
