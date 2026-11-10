<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Append-Only Self-Auditing RUP-CDCL

- Status: `proved_in_revised_tex`
- TeX label: `cor:append-only-self-auditing-rup-cdcl`
- Role: `proof_system_bridge`
- Criteria served: `C5`, `C8`, `C10`, `C11`

## Claim

A deletion-free self-auditing RUP-CDCL proof format instantiates the
carrier-independent audit upgrade criterion with one fewer annotation layer.
The proof object contains:

1. a checked label decoder from formula-label coordinates to clausal variables;
2. an append-only clause-addition log;
3. checker-visible RUP propagation certificates for the used learned
   consequences;
4. support-local auxiliary witnesses for touched auxiliary clauses.

Because the clause database is monotone, every clause that can participate in a
later propagation is still present in the proof log.  The checker can recover
the touched formula-label support by scanning the append-only database and the
RUP witnesses.  No retained deleted-clause support annotations are needed.

Under the same support-local auxiliary-witness condition as the self-auditing
RUP-CDCL theorem, the generic checker extracts the support set,
support-local CNF, audit witness, and budget from the proof artifact itself.
The support-local normalization transfer applies with linear audit budget,
giving near-threshold proof length \(n^{a-o(1)}\).

## Why This Advances The Gate

The self-auditing RUP-CDCL theorem still required retained support records for
deleted clauses.  This corollary proves a less annotated recognizable subcase:
if the trace is append-only, deletion support is not an extra field.  The live
database itself is the support memory.

This does not close the full top-paper proof-system route, but it moves the
route in the requested direction: from enriched self-audit fields toward an
ordinary proof artifact whose syntax forces part of the support audit.

## Nonclaims

- It is not a lower bound for raw DIMACS.
- It is not a lower bound for deletion-bearing raw RUP/DRUP traces.
- It is not a lower bound for arbitrary CDCL logs.
- It is not a lower bound for provenance-free learned-clause traces.
- It is not a Frege, Extended Frege, IPS, or arbitrary compressed-proof lower
  bound.
- It does not remove the need for a checked label decoder.
- It does not prove an explicit SAT-family/source lower bound.

## Coherence Check

Closest literature object: append-only RUP proof traces and deletion-free
clausal certificate checking.

Before this corollary, the paper had a positive self-auditing RUP-CDCL bridge,
but deletion-bearing traces still had to remember support for deleted clauses.
After this corollary, the deletion-free case is cleaner: monotonicity of the
clause database replaces retained deleted-clause support annotations.

This is C11-admissible as `proof_system_bridge` work.  It strengthens the same
flagship formula-footprint obstruction by making the proof-object audit less
annotated without changing the claim boundary.
