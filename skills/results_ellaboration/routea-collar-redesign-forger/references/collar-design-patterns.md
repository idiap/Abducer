<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Collar Design Patterns

## Pattern A: Symmetric Transverse Triplet

All three channels use transverse offsets that vanish with \(\delta\). The central channel has zero signed offset but must still carry a nontrivial observable difference before the limit, for example by a second transverse lobe or a small plaquette collar. Reject the pattern if the central observable is exactly the base loop for all \(\delta\).

## Pattern B: Temporal-Transverse Hybrid

The central channel may remain temporal only if its temporal height also scales with \(\delta\), so it collapses to the same limiting loop as the transverse channels. Reject the pattern if \(a_k h_k\to H>0\) while transverse offsets vanish.

## Pattern C: Common-Base Plaquette Collar

Attach small plaquette loops to a shared base path. The signs are reflected by \(\rho\), and the central channel uses a symmetric plaquette pair. This pattern is promising when the Wilson-loop response is localized near a common footprint.

## Pattern D: Paired Lollipop Collar

Use a shared stem and small lobes that shrink to the same stem. This can preserve a common limiting support while still producing channel-dependent second variations. Reject it if the lobes require links outside \(t\ge1\).

## Pattern E: Quotient-Observable Collar

The path geometry may be fixed while observables are normalized or quotiented to create a collision. This is allowed only when every quotient has a same-theory positivity-preserving realization. Send such factors to `routea-same-theory-factorization-hunter`.

## Ranking Heuristic

Prefer candidates that:

1. have explicit edge lists at every cutoff;
2. have a common limiting loop before normalization;
3. keep \(\rho\)-pairing local and transparent;
4. minimize pair-dependent quotients;
5. expose first and second geometric variations calculably.
