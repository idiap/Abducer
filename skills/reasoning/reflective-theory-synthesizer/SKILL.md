---
name: reflective-theory-synthesizer
description: Reconstruct, philosophically reflect on, transform, and synthesize rival conceptual systems into deeper theory candidates with explicit ontology, explanatory ideals, preserved tensions, unification, and new implications. Use when concepts or theories need ontological, dialectical, epistemological, explanatory, modal, representational, genealogical, or unificatory reflection before formalization, proof, or experiment, especially when current language is shallow, fragmented, or unable to express the root problem.
---

# Reflective Theory Synthesizer

## Role

Turn deep philosophical reflection into concrete theoretical change. Reconstruct
what a conceptual system says exists, how its objects relate, what counts as an
explanation, what it makes visible, and where it fails; then produce revised or
synthesized systems rather than free-floating commentary.

Read [references/reflection-lenses.md](references/reflection-lenses.md) and
select only the lenses that can change the live conceptual problem.

## Required Inputs

Require a discovery charter, root tension, incumbent conceptual system, at
least one rival or opposed commitment, protected successes, and the desired
understanding gain. If a rival is missing, construct the strongest immanent
opposition rather than a weak strawman.

For an abstract but usable prompt, infer a provisional charter and protected
successes, label the reconstruction `underdetermined`, and list the concrete
domain inputs that would revise it. If missing context prevents preservation of
target identity or the strongest form of the opposition, stop with a minimal
repair request rather than manufacturing a field-specific synthesis.

## Mathematical Invariants

- Mathematical object: the target phenomenon or theorem pressure, conceptual
  primitives, carrier objects, relations, operations, mechanisms, invariants,
  regimes, representations, and explanatory obligations.
- Preserved invariants: target identity, strongest version of each opposed
  commitment, incumbent successes, nontrivial cases, quantifier and regime
  structure, and distinctions required for the target.
- Broken invariants: any identity, equivalence, primitive, level distinction, or
  explanatory assumption deliberately changed by the synthesis.
- Boundary case: include a case where the synthesis fragments, becomes vacuous,
  erases a difference, or reverts to one of its predecessors.

## Workflow

### 1. Reconstruct each conceptual system

State its primitives, ontology, identities and differences, relations,
operations, dynamics, explanatory ideal, protected successes, absences, and
correction conditions. Reconstruct the strongest version before criticizing it.

### 2. Locate the constitutive tension

Distinguish formal contradiction, practical trade-off, regime mismatch,
underdetermination, absent mediator, abstraction failure, and competing
explanatory ideals. Name why the tension is productive: what new concept would
have to become possible for both protected commitments to be rethought.

### 3. Reflect through multiple lenses

Use at least three applicable lenses from the reference, including an
ontological and a dialectical lens for major synthesis tasks. For each lens,
return:

- what assumption or absence it exposes;
- what it preserves;
- what conceptual mutation it recommends;
- what new risk or blindness the mutation creates.

Do not count a lens as used if it only restates the candidate.

### 4. Generate structural mutations

Apply one or more concrete operations:

- split an overloaded concept or introduce a missing distinction;
- mediate opposed systems with a new relation, process, interface, or carrier;
- reconstruct objects as relations, processes, constraints, or levels;
- change an equivalence policy, invariant, scale, or regime organization;
- complete, adjoin, abstract, quotient, invert, stratify, or dualize structure;
- transform a failure into a negative organizing principle;
- synthesize systems while preserving their non-reducible differences.

Reuse `abducer-mediation-candidate-generator`, `proof-bridge-object-forger`,
`proof-creative-variant-prober`, `kb-gap-abstraction-conjecturer`, and
`efficient-representation-requirements-elicitor` for their specialist parts.
Invoke a specialist's full workflow only when its artifact and validator
prerequisites are available; otherwise apply the named conceptual operation
directly and record the unavailable prerequisite.
Use the external Hegelian source skills only as conceptual source material, not
as a second runtime.

### 5. Build rival syntheses

Construct at least one conservative synthesis and one more transformative
synthesis when the tension supports both. For each, state the new conceptual
resource, resolution mechanism, unification gain, lost structure, residual
contradiction, and generative consequences.

A synthesis may preserve the opposition as a regime, level, duality, or
productive tension rather than dissolving it. Do not force reconciliation when
the difference is constitutive.

### 6. Produce an understanding delta

Explain precisely:

- what the predecessor could not express or explain;
- what the synthesis now makes intelligible;
- which cases or routes are unified and which differences remain;
- which questions, formal objects, or proof obligations now become visible;
- what could still cause the synthesis to be revised or abandoned.

Experiments are not required. End with a support question only if the theory has
matured enough to request one.

## Guardrails

- Do not use philosophical vocabulary as a substitute for mathematical or
  scientific content.
- Do not caricature the antithesis to make synthesis easy.
- Do not call terminological substitution a conceptual transformation.
- Do not call erasure, averaging, or vague generality unification.
- Do not assume every contradiction should be eliminated; distinguish
  productive, regime-indexed, and genuinely inconsistent tensions.
- Do not make the desired conclusion true by changing definitions silently.

## Output Contract

Return:

1. `Conceptual Systems`: reconstructed incumbent and rivals.
2. `Constitutive Tension`: strongest opposed commitments and exact pressure.
3. `Reflection Matrix`: lens, exposed assumption, preservation, mutation, and
   new risk.
4. `Transformation Genealogy`: operations, ancestors, preserved and lost
   structure.
5. `Rival Syntheses`: conservative and transformative candidates when viable.
6. `Unification Map`: unified cases, common principle, preserved differences,
   and erasure risks.
7. `Understanding Delta`: before, after, perspective shift, remaining opacity.
8. `Generative Consequences`: new questions, definitions, mechanisms,
   derivations, and proof obligations.
9. `Correction Conditions`: objections, boundary cases, and revision triggers.
10. `Handoff`: preferred synthesis recommendation, retained opposition, and next
    reflection, formalization, reading, proof, or optional support question.

## Epistemic Discipline

Assign epistemic status separately to reconstruction, interpretation,
conceptual mutation, synthesis, formal consequence, and established claim. Use
`interpretive`, `conjectural`, `reflectively_supported`, `conceptually_preferred`,
`formalization_needed`, `proof_obligation`, `validated`, `refuted`, or
`explicit_unknown`. Cite source artifacts, conceptual ancestors, exact tensions,
and preserved successes. Deep understanding is a reasoned theoretical judgment,
not proof authority.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when repository artifacts ground the
systems under reflection. Read the actual target, theory, pressure, failure,
coherence, or prior-art artifacts before synthesizing. Deterministic execution
is optional: reflection is generative work, and a command should not be run only
to make it appear empirical.

## Failure/Demotion

Demote philosophical vapour, weak opposition, novelty theatre, hidden target
change, unification by erasure, synthesis without a mechanism, reflection that
causes no conceptual mutation, and theories whose fertility is protected from
all eventual correction. Preserve an honest `no_synthesis` result when the
opposition should remain plural.

## Validation Handoff

Return to `reflective-conceptual-discovery` with the synthesis candidates,
understanding delta, unresolved dissent, and the next theory-level question.
