<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Macro-Compressed ER Reuse Tradeoff

- Status: `proved_in_revised_tex`
- TeX corollary label: `cor:macro-compressed-er`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Result

The revised paper proves a concrete macro-library version of the compressed ER transfer.

For a macro-compressed acyclic extension refutation with displayed skeleton length \(S\), macro-library literal length \(D\), and \(r\) macro invocations, if the expansion is a displayed acyclic ER refutation satisfying the displayed ER hypotheses, then near threshold:
\[
  S+rD\ge 2n^{a-o(1)}.
\]

If the encoded length \(L\) controls all three parameters \(S,D,r\le L\), then:
\[
  L^2+L\ge 2n^{a-o(1)},
  \qquad
  L\ge n^{a/2-o(1)}.
\]

## Proof Skeleton

1. Each macro invocation expands to a displayed body from a library of total length \(D\).
2. The full displayed expansion has length at most \(S+rD\).
3. The displayed acyclic ER length lower bound gives expansion length at least \(2n^{a-o(1)}\).
4. Therefore \(S+rD\ge 2n^{a-o(1)}\).
5. If \(S,D,r\le L\), then \(S+rD\le L+L^2\), giving the square-root lower bound.

## Nonclaim Boundary

This does not lower-bound arbitrary compressed proof systems, Frege, Extended Frege, IPS, or implicit proofs.  It applies only to macro systems whose macro bodies have displayed acyclic ER expansions with visible invocation accounting.

## Gate Impact

This makes the compressed-proof route more concrete: ordinary macro sharing is not a free escape.  A macro-compressed proof must pay either a large skeleton, large macro library, or many invocations.  The next support-budget bridge is the support-declared macro ER normalizer; the remaining top-paper blocker is to instantiate such declarations, or controlled expansion, for a stronger proof system.
