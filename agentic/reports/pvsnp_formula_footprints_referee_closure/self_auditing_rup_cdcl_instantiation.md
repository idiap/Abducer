<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Self-Auditing RUP-CDCL Instantiation

- Status: `proved_in_revised_tex`
- TeX label: `cor:self-auditing-rup-cdcl`
- Role: `proof_system_bridge`
- Criteria served: `C5`, `C8`, `C10`, `C11`

## Claim

An enriched RUP-CDCL proof format instantiates the carrier-independent audit
upgrade criterion when the proof object itself contains:

1. a checked label decoder from formula-label coordinates to clausal variables;
2. a live-database reconstruction log;
3. checker-visible RUP propagation certificates for every used learned or
   deleted-clause consequence;
4. retained support annotations obtained from the touched clauses and decoded
   label variables.

Under the support-local auxiliary-witness condition, the generic checker
extracts the support set, support-local CNF, audit witness, and budget from the
proof artifact itself.  Therefore the support-local normalization transfer
applies with linear audit budget, giving near-threshold proof length
\(n^{a-o(1)}\).

## Why This Advances The Gate

The previous canonical-namespace RUP-CDCL theorem still used a deterministic
encoding manifest.  This corollary internalizes that information into the proof
syntax.  It is the first positive instantiation of the carrier-independent
audit upgrade criterion in the revised paper.

## Nonclaims

- It is not a lower bound for raw DIMACS.
- It is not a lower bound for raw RUP/DRUP without support parsing.
- It is not a lower bound for arbitrary CDCL logs.
- It is not a Frege, Extended Frege, IPS, or arbitrary compressed-proof lower
  bound.
- It does not prove an explicit SAT-family/source lower bound.

## Coherence Check

Closest literature object: CDCL/RUP/DRUP proof traces and checked clausal proof
certificates.

Before this corollary, the paper had a carrier-independent criterion and a
carrier-specific canonical namespace standardizer.  After this corollary, the
positive route is a self-auditing proof format: the proof object itself carries
the decoder and support audit that raw traces erase.

This is C11-admissible as `proof_system_bridge` work: it strengthens the
flagship formula-footprint obstruction by making the proof-size payoff
intrinsic to a concrete certificate format.
