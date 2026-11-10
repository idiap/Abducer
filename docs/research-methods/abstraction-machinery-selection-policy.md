<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Abstraction And Machinery Selection Policy

Abducer chooses mathematical and conceptual machinery by proof role, not by prestige.

## Universal Roles

- `construction`: builds the target object or a regulated approximation that can be transferred to it.
- `representation`: gives the object a tractable mathematical form.
- `invariant_preservation`: keeps essential commitments unchanged across transformations.
- `transfer`: moves information between regimes, formalisms, limits, or reconstructed objects.
- `witness`: produces a detectable property that would certify the target claim.
- `obstruction`: explains why a naive route fails and what must be repaired.
- `validation`: checks that the route proves the intended target rather than a nearby proxy.

## Required Questions

Every machinery-selection packet must answer:

- What is the active target object?
- What bottleneck is being addressed?
- Which interface does this machinery control?
- What assumptions are required before the machinery applies?
- What obligation does it produce?
- How could this machinery be used prematurely or incorrectly?
- Which validator, artifact, or skill must inspect the handoff?

## Yang-Mills Alignment

For Yang-Mills, RG/multiscale control is construction machinery; Schwinger functions are representation machinery; gauge invariance and same-theory identity are invariant machinery; OS reconstruction is transfer machinery; Euclidean correlator decay and spectral measures are witness machinery; cutoff leakage and Gaussian collapse are obstruction machinery; cutoff-uniformity, observable-density, and same-theory checks are validation machinery.

This alignment is illustrative. Other targets must supply their own target-object contract and example alignment through the active ledger.
