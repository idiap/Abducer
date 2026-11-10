<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Cone-Budget Extension Lower Bound

- Status: `proved_in_revised_tex`
- TeX corollary: `Cone-budget extension lower bound`
- TeX label: `cor:cone-budget-extension`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Theorem Summary

The revised paper derives a quantitative proof-object lower bound from the dependency-cone normalizer.  In a cone-annotated extension refutation, if the final contradiction mentions at most \(q\) variables and every mentioned label or extension variable has declared cone size at most \(d\), then \(qd\) must cover the final formula-label support.

In the near-threshold regime, the final cone budget must satisfy
\[
  qd \ge 2n^{a-o(1)}.
\]
Equivalently, a proof whose final interface has size \(L\) and whose cones are bounded by \(D(L)\) must satisfy \(L D(L)\ge 2n^{a-o(1)}\).

## Proof Object

- Proof system scope: cone-annotated extension resolution.
- Measured object: product of final-interface variable count and maximum declared dependency-cone size.
- Normalizer input: dependency-cone extension normalizer.
- Consequence: a short final interface is possible only if at least one declared cone is large.

## Boundary

This is not an unrestricted lower bound for Extended Frege, Frege, IPS, or hidden nonlocal extension systems.  It applies only when the proof object supplies dependency cones that can be audited and counted.

## Gate Impact

This strengthens `C5` and `C10` by turning the cone normalizer into an explicit size tradeoff.  It preserves `C11` because it sharpens the same formula-footprint obstruction: proof artifacts must pay either in final-interface size or dependency-cone size.
