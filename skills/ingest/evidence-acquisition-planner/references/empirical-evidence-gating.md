<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Empirical Evidence Gating

Use this reference when a theoretical route asks for empirical, lattice,
simulation, numerical, phenomenological, or experimental evidence.

## Required Fields

- `linked_theoretical_step`: the proof obligation or route branch that needs
  evidence.
- `empirical_question`: the concrete question evidence should answer.
- `observable_or_quantity`: the measured or simulated object.
- `proximity_class`: same-theory, regulated-approximation, analogy, toy-model,
  or unrelated.
- `support_criteria`: what would increase confidence or priority.
- `refutation_criteria`: what would demote, pivot, or quarantine the route.
- `transfer_gap`: what theorem is still needed before the evidence bears on
  proof.
- `proof_boundary`: why this evidence is not itself proof.

## Yang-Mills Examples

- Correlator decay route: search for lattice glueball correlator decay,
  continuum-extrapolated mass estimates, and finite-size scaling. This supports
  the plausibility of a positive spectral scale but does not prove a Clay mass
  gap without OS reconstruction, observable density, and cutoff-uniform transfer.
- Nontriviality route: search for Wilson-loop area law, string tension, or
  nonzero connected gauge-invariant cumulants. This guides the choice of a
  nontriviality witness but does not prove continuum nontriviality unless the
  witness is shown to survive cutoff removal in the same limiting object.
- OS/transfer route: search for reflection positivity and transfer-matrix
  results for lattice gauge actions. This can identify source theorems, but it
  remains a prior-art or transfer-gap task until the limiting topology is known.

## Demotion Rules

Quarantine the evidence request when:

- the evidence is only fixed cutoff or finite volume and no continuum
  extrapolation is requested;
- the observable is not gauge invariant;
- the evidence concerns a different theory or dimension;
- the request would let numerical agreement replace a missing theorem;
- the route cannot state what result would change after the evidence is found.
