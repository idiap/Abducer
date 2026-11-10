<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Claim Reset Plan

- Status: `implemented`
- Decision: reframe the paper as a conservative certificate-complexity note.

## New Title

Structured Certificate Lower Bounds for Label-Induced Hardness Predicates

## Smallest Honest Abstract Claim

The paper proves inputwise lower bounds for structured certificates of
label-induced circuit-hardness predicates.  The main technical contribution is
a batched static-dictionary upper bound showing that a small two-polarity
formula footprint would yield a small source circuit.  Supporting results give
row-forcing bounds for private occurrence labels and residual-distance bounds
after equality quotienting.

## Nonclaims To State In The Introduction

- The paper does not prove P != NP.
- The paper does not prove SAT outside P/poly.
- The paper does not construct an explicit SAT-labeled carrier with the needed
  unrestricted lower bound.
- The paper does not prove a lower bound for Frege, Extended Frege, IPS, or any
  named standard proof system.
- The paper does not give a bounded-error randomized or interactive certificate
  lower bound.
- The paper does not handle nonlinear SAT semantic constraints such as
  self-reduction inside the quotient theorem.

## Theorem-Status Table

| Claim | Status after reset | Paper placement |
|---|---|---|
| Batched dictionary lemma | `patched_primitive` | Technical lemma before formula theorem |
| Formula-footprint theorem | `main_candidate` | Main theorem |
| Row-forcing theorem | `supporting_structural_lemma` | Supporting theorem |
| Equality quotient theorem | `supporting_structural_lemma` | Supporting theorem |
| SAT parity application | `conditional_calibration` | Application/motivation |
| Proof-system lower bound | `not_claimed` | Open problem only |
| Randomized/interactive extension | `future_work` | Open problem only |
| Explicit hard SAT carrier | `future_work` | Open problem only |

## Intro Surgery

1. Replace completion-barrier language by certificate-complexity language.
2. Move SAT magnification from headline motivation to a calibrated application.
3. Name the formula theorem as the central contribution.
4. Say row forcing and quotient distance are structural tests a proof interface
   must pass, not lower bounds for standard proof systems.
5. Add the literature anchor paragraph before claiming novelty.

## Venue Claim

After the reset, the realistic claim is:

- suitable for arXiv/ECCC as a structural note after the dictionary fix and
  literature update;
- plausible for a workshop;
- not ready for ITCS/CCC/STOC/FOCS-level submission without a randomized
  theorem, named proof-system instantiation, or tight matching-bound theory.
