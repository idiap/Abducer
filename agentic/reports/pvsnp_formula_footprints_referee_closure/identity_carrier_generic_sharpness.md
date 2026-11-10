<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Identity-Carrier Generic Sharpness

- Status: `proved_in_revised_tex`
- Integrated theorem: `Generic sharpness in the identity carrier`
- TeX target: `structured_certificate_lower_bounds_revision.tex`
- Criteria affected: `C2`, `C4`, `C10`, `C11`

## Statement

In the identity formula-label carrier, set \(M_n=1\), \(G_{n,1}(x)=x\), \(A_1(z)=z\), and \(U_n=\{0,1\}^n\).  A formula labeling is then an ordinary truth table \(f:\{0,1\}^n\to\{0,1\}\), and the hardness predicate is \(\Ckt(f)>s\).

For a uniformly random \(f\), and for
\[
  m \ge C s\log(s+n)+r,
\]
with high probability there is a completion-sound certificate \(f|_T\) of size \(m\) for \(\Ckt(f)>s\).  The certificate can be chosen with both output values represented and neither polarity exceeding \(2m/3\).

## Proof Idea

There are at most \(2^{O(s\log(s+n))}\) size-\(s\) truth tables.  A random \(m\)-point test set \(T\) eliminates each fixed size-\(s\) truth table with probability \(1-2^{-m}\).  A union bound shows that, for \(m=O(s\log(s+n))\), no size-\(s\) circuit agrees with \(f\) on all of \(T\).  Then every completion of \(f|_T\) has complexity greater than \(s\), so \(f|_T\) is a \(1\)-certificate.  A Chernoff bound gives the two-polarity balance.

## Publication-Level Role

This theorem turns the formula-footprint lower bound into a near-sharp statement in the standard identity truth-table carrier.  It does not construct an explicit SAT-labeled carrier and does not yield a standard proof-system lower bound.  Its role is to show that the flagship formula-footprint scale is not an artifact of the proof: in the baseline model, generic hard functions have certificates matching the lower bound up to polylogarithmic factors.
