<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Expansion-Bounded Compressed ER Transfer

- Status: `proved_in_revised_tex`
- TeX corollary label: `cor:compressed-er-expansion`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Result

The revised paper proves the compressed-proof transfer that follows from the displayed acyclic ER length lower bound.

If a compressed acyclic extension refutation \(\rho\) expands by a sound decompression map \(\operatorname{Exp}\) to a displayed acyclic extension refutation satisfying the displayed ER hypotheses, and if the displayed expansion length is bounded by a monotone budget \(B(|\rho|)\), then near threshold:
\[
  B(|\rho|)\ge 2n^{a-o(1)}.
\]

In particular, if \(B(L)\le C L^k\), then
\[
  |\rho|\ge C^{-1/k}2^{1/k}n^{a/k-o(1)}.
\]

## Proof Skeleton

1. Expand the compressed proof to a displayed acyclic ER object.
2. Apply the displayed acyclic ER length lower bound to the expansion.
3. Compare the resulting displayed length lower bound with the assumed expansion budget \(B(|\rho|)\).
4. For polynomial expansion, rearrange \(C|\rho|^k\ge 2n^{a-o(1)}\).

## Nonclaim Boundary

This is not a lower bound for arbitrary compressed proof systems, Frege, Extended Frege, IPS, or implicit proofs.  It applies only when the compressed object has a sound displayed acyclic ER expansion with a controlled expansion budget.  If the proof system hides dependency support without such an expansion, or leaves the displayed acyclic ER model, this transfer does not apply.

## Gate Impact

This is the next C11-aligned proof-system bridge after displayed acyclic ER.  It turns the remaining compressed-system obstacle into a concrete budget theorem: prove controlled expansion/support for the compressed proof format, or explain why the format is genuinely nonlocal.
