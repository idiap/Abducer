---
name: efficient-representation-requirements-elicitor
description: Declaratively elicit the requirements for an efficient mathematical representation of a proof gap. Use when a route needs to state which objects, invariants, operations, equivalence relations, locality/complexity constraints, transfer interfaces, and falsifiers a representation must support before new abstraction design or proof search continues.
---

# Efficient Representation Requirements Elicitor

## Conceptual Role

Turn a vague need for "better concepts" into a declarative requirements packet
for a representation that can carry proof pressure. Efficiency means the
representation compresses the right structure, exposes obligations, and supports
small tests; it does not mean hiding hard assumptions under notation.

## Workflow

1. Restate the target pressure and the specific concept gap.
2. Name the mathematical objects that the representation must encode and the
   objects it must deliberately keep separate.
3. State the primitive operations the proof needs: composition, restriction,
   limit passage, quotienting, interpolation, reduction, conditioning,
   reflection, lifting, comparison, or certificate extraction.
4. State preserved invariants and forbidden collapses.
5. State equivalence or quotient policy: what differences may be identified and
   what must remain visible.
6. State efficiency requirements: compression target, local computability,
   operation cost, sample/finitary probes, proof ergonomics, and interface size.
7. State transfer requirements: source semantics, target semantics, bridge law,
   nontrivial hypotheses, and stress tests.
8. Return acceptance criteria that can route the next cycle to proof search,
   abstraction forging, literature import, or quarantine.

## Guardrails

- Do not equate efficient representation with short notation.
- Do not let a representation merge source and target objects unless the
  equivalence policy proves why that identification is legitimate.
- Do not hide a hard theorem obligation inside a primitive operation,
  quotient, oracle, or transfer interface.
- Do not accept requirements without a falsifier, edge case, or boundary regime.

## Mathematical Invariants

- Mathematical object: the proposed representation and the source/target
  objects it must encode.
- Preserved invariants: definitions, symmetries, positivity, locality,
  complexity class/model commitments, nontriviality, asymptotic regime,
  quantifier order, or spectral/continuum structure, depending on the target.
- Broken invariants: anything the representation compresses away that the proof
  later needs to recover.
- Boundary regime: a small example, edge case, counterexample class, or known
  barrier where the representation should visibly fail rather than silently
  overgeneralize.

## Epistemic Discipline

- Cite evidence from KB IDs, artifacts, reports, branch memory, proof packets,
  formulas, prior-art notes, or explicit unknowns.
- Label each requirement as mandatory, optional, conjectural,
  proof-obligation, blocked, demoted, or rejected.
- Separate representational convenience from theorem relevance.
- Do not accept a representation whose cheapest proof path is to redefine the
  target predicate or merge source and target semantics.

## Output Contract

Return:

- `representation_goal`: what the representation must make possible.
- `target_pressure`: theorem-level pressure and non-claim boundary.
- `objects_to_encode`: source objects, target objects, carriers, observables,
  certificates, examples, and counterexamples.
- `primitive_operations`: operations that must be closed, controlled, or
  explicitly partial.
- `preserved_invariants`: invariants with evidence and status.
- `forbidden_collapses`: circular definitions, hidden quotients, proxy shifts,
  lost regimes, or erased quantifiers.
- `equivalence_policy`: which objects may be identified and which distinctions
  must remain inspectable.
- `efficiency_requirements`: compression, local computability, operation cost,
  interface size, proof ergonomics, and finite/symbolic probe requirements.
- `transfer_interface`: source semantics, target semantics, bridge law,
  nontrivial hypotheses, and stress/failure cases.
- `acceptance_criteria`: conditions for proof search, abstraction refit,
  forge-new, literature import, or quarantine.
- `epistemic_status`, `evidence`, and `validation_handoff`.

## Codex Exec Protocol

When local artifacts exist, read the target profile, active branch packet,
concept-gap diagnosis, abstraction-fit verdict, proof-depth packet, or queue
item before stating requirements. A deterministic run is optional and only
appropriate when a repo script can regenerate those artifacts. If no script is
needed, state that the packet is a generative representation contract and cite
the evidence paths or explicit unknowns.

## Failure/Demotion

Demote packets that are only aspirational, omit invariants, provide no edge
case or counterexample, or fail to separate source and target semantics.
Quarantine representation requirements that make the desired theorem true by
definition rather than by a checkable proof obligation.
