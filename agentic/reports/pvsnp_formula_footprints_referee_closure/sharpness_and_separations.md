<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Sharpness And Separations

- Status: `implemented`
- Decision: the current draft does not yet prove a full matching-bound theory. The artifact supplies simple separations and records the required demotions.

## What Can Be Shown Now

### Separation S1: Formula labels can be cheaper than occurrence labels

Use parity with \(M_n\) odd and let every row contain \(M_n\) copies of the same
generated key \(u_x\), with \(x\mapsto u_x\) injective.

- In the formula-label model, the row output is the single shared label
  \(\lambda(u_x)\).  The footprint counts one generated formula per forced row.
- In the occurrence-label model, the \(M_n\) row positions are independent.  To
  force a parity row, all \(M_n\) positions must be queried.

Thus the occurrence forcing cost has an \(M_n\) factor that the formula model
does not have on the same row shape.  This is a genuine model separation, even
though the hard source function is still supplied by counting rather than an
explicit SAT carrier.

### Separation S2: Equality quotient can collapse occurrence hardness

Use parity with two identical occurrences per row and quotient them by equality.
Before quotienting, the private occurrence model can realize arbitrary row
parities.  After quotienting, each row contains the same quotient label twice,
so the row parity contribution is zero.  The quotient carrier is constant, and
the hardness predicate is empty above constant circuit size.

This shows why equality-aware quotienting is not cosmetic: sound equality links
can destroy private-occurrence hardness.

### Coincidence S3: Full-rank one-label quotient coincides with the formula model

If each row has one quotient class and the incidence map is the identity on
source rows, the formula, occurrence, and quotient source images all realize the
same truth tables up to the chosen labeling model.  The quotient theorem then
reduces to ordinary sparse-row patching.

## What Is Not Yet Proved

The draft still does not prove a general matching upper bound of the form
\[
  C_1(\mathsf{Hard}^{\mathrm{form}}) =
  \widetilde{\Theta}(s)
\]
or
\[
  C_1(\mathsf{Hard}^{\mathrm{occ}}) =
  \Theta(Ms/n)
\]
for a natural explicit family.  The lower bounds remain necessary conditions
unless a family is supplied whose hard labelings have matching small
certificates.

## Demotion Rule

- Formula-footprint theorem: remains the main candidate because the batched
  lookup improvement is quantitative and not just sparse patching.
- Row-forcing theorem: demote to a supporting aggregator lemma until matching
  examples or proof-system extraction are added.
- Quotient-distance theorem: demote to an equality-aware sparse-patching lemma
  until rank/nonvacuity and separation examples are integrated.
- SAT section: keep as conditional calibration.

## Paper Patch

Use `sharpness_and_separations.tex` as a compact section or appendix paragraph
after the theorem statements or before related work.
