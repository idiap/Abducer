---
name: mathematical-concept-gap-revisitor
description: Critically revisit deep mathematical concepts, conceptual tensions, and major gaps in a proof route. Use when a theorem-shaped cycle, marathon branch, KB bridge, or report feels shallow, definitional, fragmented, stuck in local lemmas, or representation-limited and must diagnose whether the current concepts are the right ones before more proof search.
---

# Mathematical Concept Gap Revisitor

## Conceptual Role

Re-open the conceptual substrate of a route before another proof cycle. The
skill asks what mathematical object, invariant, or representation is failing to
carry the target pressure, and whether the current route is exploring a real
tension or only decorating a local lemma.

## Workflow

1. Name the target theorem pressure in its strongest honest form.
2. State the concept under review and the mathematical role it is supposed to
   play: carrier, invariant, obstruction, bridge, quotient, limit object,
   certificate, energy functional, observable, proof system, or semantic model.
3. Elicit the declarative tension: list the commitments that must jointly hold
   but do not yet fit in the current route.
4. Diagnose the failure mode: triviality, definitional collapse, missing
   invariant, wrong object, wrong equivalence relation, limit-order trap,
   transfer gap, literature mismatch, or insufficient explanatory compression.
5. Ask whether available abstractions already fit better. Check local KBs,
   bridge plans, pressure packets, proof-depth packets, prior-art notes, and
   repo-local skills before inventing a new abstraction.
6. If no available abstraction fits, state the new abstraction type needed and
   the proof obligations it would introduce.
7. Hand off the representation problem to
   `efficient-representation-requirements-elicitor` and candidate comparisons
   to `abstraction-fit-gap-auditor`.

## Guardrails

- Do not proceed if the route cannot name a target pressure, mathematical
  object, and invariant under stress.
- Do not describe the need for conceptual depth without producing a declarative
  tension.
- Do not invent new abstractions while ignoring available local abstractions,
  KB artifacts, proof packets, or literature anchors.
- Do not promote a diagnosis that makes the desired conclusion true by
  definition.

## Mathematical Invariants

- Mathematical object: the concept or abstraction being asked to carry proof
  pressure.
- Preserved invariants: target commitments, source definitions, equivalence
  relations, positivity/monotonicity/symmetry/complexity constraints, and limit
  or transfer interfaces relevant to the route.
- Broken invariants: any structure that becomes invisible, vacuous, circular,
  non-composable, non-uniform, non-local, or disconnected from the target after
  the current representation is used.
- Edge case or counterexample: name one regime, example, barrier, or boundary
  case where the current concept would fail or become merely definitional.

## Epistemic Discipline

- Cite KB IDs, artifact paths, branch IDs, proof packets, report sections,
  prior-art anchors, or explicit unknowns for every diagnosis.
- Label each claim as evidence-backed, conjectural, proof-obligation, blocked,
  demoted, quarantined, or rejected.
- Do not treat fluency, technical density, or a renamed definition as conceptual
  progress.
- Do not invent a new abstraction until at least one available abstraction has
  been tested against the declared tension.

## Output Contract

Return:

- `target_pressure`: theorem-level pressure that the route must respect.
- `concept_under_review`: object, definition, invariant, or abstraction family.
- `declarative_tension`: commitments that must jointly hold, with the exact
  incompatibility or missing mediator.
- `current_abstraction_failure`: why the present representation is shallow,
  circular, underpowered, or misfit.
- `major_gap_hypotheses`: object gap, invariant gap, representation gap,
  transfer gap, efficiency gap, literature gap, or proof-obligation gap.
- `available_abstractions_to_revisit`: existing concepts, skills, KB artifacts,
  and literature anchors worth testing first.
- `new_abstraction_trigger`: what would justify forging a new object rather
  than repairing the current one.
- `efficient_representation_handoff`: declarative requirements to pass to
  `efficient-representation-requirements-elicitor`.
- `falsifiers`: edge cases, counterexamples, or review objections that would
  demote the diagnosis.
- `epistemic_status`, `evidence`, and `validation_handoff`.

## Codex Exec Protocol

When local artifacts are available, inspect the relevant KB, latest marathon
cycle, proof-depth packet, lock-in report, queue item, or report section before
diagnosing the gap. A deterministic run is optional and only appropriate when a
repo script already materializes the cited artifact. If no execution is useful,
state that the diagnosis is generative and cite the source artifacts or explicit
unknowns that bound it.

## Failure/Demotion

Demote the diagnosis if it only says "needs deeper concepts" without naming the
tension, mathematical object, invariant, available alternatives, and falsifier.
Quarantine any diagnosis that changes the target problem, assumes the desired
conclusion, or treats a definitional transfer theorem as substantive progress.
