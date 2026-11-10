<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Bounded-Depth Extension Tradeoff

- Status: `proved_in_revised_tex`
- TeX corollary: `Bounded-depth extension tradeoff`
- TeX label: `cor:bounded-depth-extension`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Theorem Summary

The revised paper derives a depth/interface tradeoff for bounded-fanin cone-annotated extension proofs.  If every extension definition has fan-in at most \(r\), every final variable has extension depth at most \(h\), and the final contradiction mentions at most \(q\) variables, then every mentioned variable has formula-label cone size at most \(r^h\).  The cone-budget corollary therefore gives
\[
  q r^h \ge 2n^{a-o(1)}
\]
near threshold.

Equivalently, if the final interface has size at most \(L\), then the extension depth must satisfy
\[
  h\ge \log_r(2n^{a-o(1)}/L)
\]
whenever the quotient is larger than \(1\).

## Proof Object

- Proof system scope: bounded-fanin cone-annotated extension resolution.
- Measured object: final-interface variable count times fan-in to the extension depth.
- Normalizer input: cone-budget extension lower bound.
- Consequence: a short final interface requires logarithmic extension depth, unless a final variable has a large declared cone.

## Boundary

This is not an unrestricted lower bound for ER, EF, Frege, IPS, or hidden nonlocal extension systems.  It applies only when fan-in, depth, and dependency cones are part of the auditable proof object.

## Gate Impact

This strengthens `C5` and `C10` by converting cone size into a familiar proof-object parameter: bounded-fanin extension depth.  It preserves `C11` by staying subordinate to the formula-footprint obstruction and its completion-soundness spine.
