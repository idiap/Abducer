---
name: evidence-acquisition-planner
description: For each unresolved hypothesis, proof obligation, contradiction route, or theoretical bridge, propose the cheapest decisive local, prior-art, empirical, lattice, numerical, or web-backed evidence test. Use when a theoretical step requires closely related empirical evidence without letting empirical support replace proof.
---

# Evidence Acquisition Planner

## Role

This skill turns unresolved conjectures and theoretical proof obligations into
concrete evidence plans. It can request empirical, numerical, simulation,
lattice, phenomenological, or experimental evidence when such evidence is
closely related to a proof step. Its core job is to keep that evidence useful
without confusing it with a theorem.

## When To Use

Use it when:

1. hypotheses remain open after evaluation;
2. the next step is unclear;
3. web search may be needed but only under a parsimonious gate;
4. a theoretical step asks whether nearby empirical or numerical evidence
   supports, refutes, calibrates, or prioritizes an assumption.

Read [references/prompt-template.md](references/prompt-template.md).
Read [references/empirical-evidence-gating.md](references/empirical-evidence-gating.md)
when the request involves lattice, simulation, numerical, phenomenological,
or experimental evidence.

## Evidence Modes

- `source_import`: find exact theorem, definition, prior-art statement, or
  source quotation needed for a proof obligation.
- `empirical_probe`: find nearby empirical, numerical, lattice, simulation, or
  phenomenological evidence that bears on a theoretical assumption.
- `negative_evidence`: look for failed simulations, counter-observations,
  no-go evidence, or known numerical instability.
- `transfer_gap`: state what theorem would be needed before empirical evidence
  could count toward a proof route.

## Empirical Evidence Gate

Use empirical evidence only when it is attached to a specific theoretical
obligation. The evidence request must name:

- the theory step it supports or challenges;
- the empirical observable or numerical quantity;
- the proximity class: same theory/regime, regulated approximation, analogy,
  toy model, or unrelated;
- what would count as support, refutation, calibration, or prioritization;
- the exact proof boundary that prevents empirical evidence from being treated
  as theorem evidence.

For Yang-Mills, acceptable empirical-nearby evidence can include lattice
glueball spectra, Wilson-loop area-law/string-tension measurements,
finite-size scaling, continuum-extrapolated Monte Carlo estimates,
Euclidean correlator decay, topological susceptibility, and checks of
reflection-positive lattice actions. These are route-guiding evidence, not
Clay-target proof, unless a same-theory transfer theorem is supplied.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Ingestion does not validate truth; it only preserves inspectable source structure for later reasoning.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: source statement, theorem body, symbol, definition, citation, normalized KB card, and dependency edge.
- Preserved invariants: source text provenance, symbol identity, statement dependency, confidence status, and explicit missing fields.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: evidence request ID, linked theoretical obligation, evidence mode,
empirical observable or source statement, proximity class, search plan,
acceptable sources, support/refutation criteria, transfer gap, proof boundary,
source IDs, explicit unknowns, artifact paths, validation result, and next
repair. Include executed commands and produced artifacts when a deterministic
run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote malformed, uncited, ambiguous, stale, non-proximate, or lossy intake to
repair/evidence task instead of using it as reasoning evidence. Quarantine any
empirical evidence that is fixed-cutoff, finite-volume, non-gauge-invariant,
or analogy-only when the theoretical obligation requires continuum Yang-Mills.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
