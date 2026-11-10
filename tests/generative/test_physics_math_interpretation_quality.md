<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generative QA: Physics/Math Interpretation

## Purpose

Use this checklist to review `agentic/reports/physics_math_interpretation/latest.md`
as a substantive Yang-Mills reasoning artifact, not as a keyword or relevance-score
report.

## Required Probes

1. Read the Balaban RG route. It must explain how multiscale effective-action
   control could support a continuum Yang-Mills construction, and it must state
   why fixed-cutoff or finite-volume control is not enough.
2. Read the correlator-decay route. It must explain how reflection positivity,
   transfer matrix construction, OS reconstruction, and Hamiltonian spectral
   gap transfer are related, and it must reject lattice-only decay as sufficient.
3. Check that each route names mathematical objects, a mechanism chain, a
   physical interpretation, false-positive controls, and next lemma questions.
4. Check that the report says what is missing from a proof. It should not imply
   that interpretive coherence proves Yang-Mills existence or the mass gap.
5. Check the cross-route synthesis. It must name the joint problem: continuum
   object, OS reconstruction, nontriviality witness, and positive spectral gap
   must live in the same limiting Yang-Mills theory.

## Rejection Criteria

Reject the report if:

- it just counts route terms or cites a numeric relevance score;
- it uses generic phrases such as "factor the opaque obligation";
- it treats Balaban RG control as automatically proving a mass gap;
- it treats Euclidean correlator decay at fixed lattice spacing as a continuum
  Hamiltonian spectral gap;
- it omits nontriviality, OS/Wightman adequacy, or cutoff-removal pressure;
- it contains no explicit false-positive controls;
- it fails to say that the artifact is not a proof.

## Passing Standard

The report passes when a mathematician or mathematical physicist can identify
the proposed proof mechanism, the exact conceptual bottleneck, the physical
meaning, and the next lemma that would have to be formulated before the route
deserves further proof-queue attention.
