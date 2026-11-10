<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Randomized Accepting-Union Theorem

- Status: `proved_in_revised_tex`
- Paper location: `structured_certificate_lower_bounds_revision.tex`
- Criteria affected: C6 randomized/interactive robustness.

## Theorem

Let \(P:\{0,1\}^V\to\{0,1\}\) be a Boolean property and let \(V_R\) be a randomized adaptive oracle verifier.  Fix \(y\) with \(P(y)=1\).  Let \(A_y\) be the set of random strings on which the verifier accepts \(y\), and let \(U_y\) be the union of all variables queried during those accepting executions.

If every \(y'\) with \(P(y')=0\) is accepted with probability at most \(\beta\), while \(y\) is accepted with probability greater than \(\beta\), then \(y|_{U_y}\) is a deterministic \(1\)-certificate for \(P\).

## Consequence For Formula Footprints

For a bounded-error formula-label verifier for \(\HardF_{n,s,A}\), the union of formula labels queried on accepting executions satisfies the same two-sided footprint lower bound as deterministic certificates:

\[
  g_n+c\Lookup(M_n,|U_{\lambda,b}|,\ell_n)+cM_n>s
  \qquad b\in\{0,1\}.
\]

In the near-threshold regime, both accepting-union polarity classes have size \(n^{a-o(1)}\).

## Proof Spine

1. Suppose a non-hard completion \(y'\) agrees with \(y\) on the accepting-query union.
2. For every random string that accepts on \(y\), the adaptive execution under \(y'\) follows the same path and receives the same answers.
3. Therefore \(y'\) is accepted on at least the accepting probability of \(y\), contradicting the soundness gap.
4. The accepting union is a deterministic certificate, so the deterministic footprint theorem applies.

## Boundary

This is a union-footprint theorem.  It does not lower-bound the expected number of queries in one randomized run.  A verifier might query few labels per seed while spreading its accepting paths over a large union.  Expected-footprint, transcript-support, communication-query, and information-revealed lower bounds remain open.
