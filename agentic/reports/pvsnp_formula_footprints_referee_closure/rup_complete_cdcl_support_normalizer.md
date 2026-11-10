<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# RUP-Complete CDCL Support Normalizer

- Status: `proved_in_revised_tex`
- TeX statement: `structured_certificate_lower_bounds_revision.tex`
- TeX label: `cor:rup-complete-cdcl`
- Criteria affected: `C5`, `C8`, `C9`, `C11`
- Result role: `proof_system_bridge`

## Statement

A CDCL/DRUP-style learned-clause log supplies the controller-complete adaptive
audit when every used learned clause, propagation, pruning step, and
deletion-dependent use carries a checker-visible RUP propagation certificate
over the known live clause database.

The proof object must also expose a trusted formula-label namespace, a trusted
variable-role map, or an equivalent local-support parser.  Deleted clauses do
not erase support: if a later consequence uses a retained learned clause, the
retained RUP certificate and its parsed formula-label support remain charged.

## Support Budget

Let `W_Pi` be the union of formula-label frontier coordinates appearing in:

- replayed RUP unit-propagation traces;
- clauses touched by those traces;
- local-support parser output for used clauses;
- retained certificates for deleted clauses whose consequences are still used.

Then

`S_Pi = {root} union replay_path_queries union W_Pi`

is support-local for the residual relation at the hard tuple.  Any checker
budget upper-bounding the replay path and parsed RUP-trace support inherits the
same near-threshold formula-footprint lower bound.

## Before/After Shift

Before this corollary, the paper had an antecedent-complete CDCL theorem and a
matching erasure trichotomy: CDCL support was sound if learned clauses exposed
antecedent DAGs, and unsound if all provenance and roles were erased.

After this corollary, the positive bridge no longer requires an explicit
learned-clause antecedent DAG.  Checker-visible RUP propagation traces over a
known live clause database can supply the audit, provided the trace support is
parsed into formula-label coordinates and retained across deletions.

## Nonclaims

- no arbitrary CDCL lower bound;
- no support extraction from raw RUP or DRUP syntax without namespace, role map,
  or local-support parser;
- no hidden clause-minimization normalizer;
- no deleted-clause support erasure;
- no cyclic restart or search-graph normalizer;
- no Frege, Extended Frege, IPS, or arbitrary compressed-proof lower bound;
- no explicit SAT-carrier lower bound.

## C11 Admission

This is admitted as a proof-system bridge.  It serves the same cohered spine:
completion-sound proof evidence must expose or charge the formula-label support
on which it depends.  The corollary answers the CDCL erasure boundary by showing
exactly what non-plain RUP information is sufficient, rather than adding a
separate theorem arc.
