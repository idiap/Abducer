<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Parsimonious Probe Quality Checks

Use these checks when reviewing PMP outputs generatively:

- The workflow chooses exact symbolic derivation before numerical search when
  the carrier is a finite matrix, determinant, minor, quotient, phase, or
  rephasing equation.
- Analytic obligations name the mathematical object, validity regime,
  certification condition, falsifier condition, and same-theory transfer
  boundary.
- Bounded numerical probes state a bounded domain, stopping condition,
  qualitative decision value, deterministic reproducibility, and non-proof
  boundary.
- Full simulation requests are rejected from proof promotion or marked
  `external_evidence_only`.
- The output explains what was learned in mathematical language, not as a
  generic score.
