<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Contradiction Route Audit Checklist

Use this checklist before a reductio route is treated as proof progress.

## Required Checks

- Exact negation: Does the assumption negate the target rather than strengthen
  or weaken it?
- Same object: Are all objects in the target, negation, carrier, and conflict
  target in the same theory and construction regime?
- Same limit: Are cutoff removal, subsequences, topology, and Hilbert-space
  reconstruction kept fixed or bridged by an explicit lemma?
- Valid carrier: Can the carrier object actually witness the contradiction?
- Accepted conflict target: Is the contradicted claim accepted, imported with
  provenance, validator-backed, or still a proof obligation?
- Excluded cases: Could null sectors, boundary regimes, superselection sectors,
  finite-volume artifacts, or non-dense observable families make the route
  fail?
- Logic boundary: Is the route classical, constructive, or dependent on an
  existence principle?

## Yang-Mills Audit Questions

- If the route assumes no gap, does it produce a vacuum-orthogonal low-energy
  spectral object in the reconstructed H_YM, not only at finite cutoff?
- If the route contradicts Euclidean decay, is the observable family
  spectrally determining in P_perp H_YM?
- If the route uses OS positivity, is positivity preserved in the limiting
  topology and quotient?
- If the route uses nontriviality, is the witness attached to the same
  continuum Schwinger functions as the gap claim?

## Verdict Discipline

Promote only when all hard checks pass. Repair when the idea is promising but
one local obligation is missing. Quarantine when the route is attractive but
the contradiction target or object identity is not yet grounded. Reject when
the contradiction depends on a false or incompatible premise.
