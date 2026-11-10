<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Canonical-Namespace RUP-CDCL Standardizer

- Status: `proved_in_revised_tex`
- TeX statement: `structured_certificate_lower_bounds_revision.tex`
- TeX label: `cor:canonical-namespace-rup-cdcl`
- Criteria affected: `C5`, `C8`, `C9`, `C11`
- Result role: `proof_system_bridge`

## Statement

The RUP-complete CDCL bridge does not need a trusted external role map when the
trace is paired with a deterministic encoding manifest that the checker can
verify.

The manifest supplies:

- a reserved formula-label variable interval;
- an injective map from that interval to frontier coordinates;
- a disjoint auxiliary-variable region;
- a deterministic rule that the support of a touched clause is the label
  interval variables appearing in it, mapped to frontier coordinates;
- a live-database log reconstructing original clauses, accepted learned clauses,
  and deletions at each RUP check;
- a retention rule that keeps charged support for deleted-clause consequences.

Under these conditions the manifest is an equivalent local-support parser, so
the RUP-complete CDCL support normalizer applies.

## Before/After Shift

Before this corollary, the RUP-complete theorem still allowed the support parser
to be stated as a trusted namespace, trusted role map, or equivalent parser.

After this corollary, one parser is fully checkable: a canonical label-variable
interval plus live-database manifest lets the checker compute support directly
from touched clauses.  The remaining gap is no longer namespace parsing for
this carrier; it is whether a stronger proof system naturally emits such an
audited object, or whether an explicit SAT-family/source lower bound can replace
the proof-system payoff.

## Nonclaims

- no support extraction from unmanifested DIMACS syntax;
- no support extraction from raw RUP or DRUP without a label interval and live
  database log;
- no arbitrary CDCL lower bound;
- no hidden role inference from variable names alone;
- no deleted-clause support erasure;
- no Frege, Extended Frege, IPS, or arbitrary compressed-proof lower bound;
- no explicit SAT-carrier lower bound.

## C11 Admission

This is admitted as a proof-system bridge.  It serves the same result spine by
turning the RUP-complete CDCL support audit into a checkable encoding condition,
rather than adding an unrelated proof-system claim.
