<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Prefix-Typed Append-Only RUP-CDCL

Status: `proved_in_revised_tex`

TeX label: `cor:prefix-typed-append-only-rup-cdcl`

Role: `proof_system_bridge`

This packet records the less-annotated RUP-CDCL bridge added after the
append-only self-auditing corollary.  It removes the proof-internal label
decoder, but only under a typed proof-system convention: formula-label variables
must be a public syntactic class, so the checker can recover the corresponding
coordinate from the variable name itself.

## Theorem Summary

Measured object: typed append-only RUP-CDCL proof object with public
formula-label namespace, append-only clause log, RUP witnesses, and
support-local auxiliary witnesses.

Conclusion: the carrier-independent audit upgrade criterion applies with linear
audit budget without a proof-internal label decoder and without retained
deleted-clause support records.

Proof-system status:
`positive_for_prefix_typed_append_only_RUP_CDCL_not_untyped_raw_RUP_DRUP_or_arbitrary_CDCL`.

## Audit Requirements

- `public_formula_label_variable_namespace`
- `append_only_clause_addition_log`
- `checker_visible_RUP_propagation_certificates`
- `support_local_auxiliary_witnesses`
- `no_proof_internal_label_decoder_needed`
- `no_deleted_clause_support_annotations_needed`
- `no_external_carrier_specific_manifest`
- `no_hidden_role_advice`
- `no_semantic_oracle`

## Proof Skeleton

- scan the append-only clause database and RUP witnesses;
- parse formula-label support using the public syntactic namespace;
- form the support-local CNF from monotone replay clauses;
- verify support-local auxiliary witnesses for touched auxiliary clauses;
- apply the carrier-independent audit upgrade criterion;
- use the linear audit budget to derive the \(n^{a-o(1)}\) proof-length lower
  bound.

## Nonclaims

This theorem does not prove lower bounds for raw DIMACS, untyped raw RUP/DRUP,
deletion-bearing RUP/DRUP without retained support, arbitrary CDCL,
provenance-free learned clauses, Frege, Extended Frege, IPS, arbitrary
compressed proofs, systems without support-locality witnesses, or an explicit
SAT-family/source lower bound.

## Coherence

Closest literature object: typed or sorted proof traces with public variable
roles, append-only RUP traces, and deletion-free clausal certificate checking.

Before: append-only self-auditing RUP-CDCL still required a proof-internal label
decoder.

After: a public formula-label namespace replaces that decoder in the deletion-free
case.

C11 role: `proof_system_bridge`.

Why not fragmented: this removes exactly one more annotation layer from the same
RUP-CDCL bridge and keeps the remaining blocker visible: remove support-local
witness assumptions, handle deletion-bearing or untyped traces, or switch to an
explicit SAT-family route.
