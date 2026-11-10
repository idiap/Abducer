<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Prefix-Typed RUP Support-Witness Necessity

Status: `proved_in_revised_tex`

TeX label: `prop:prefix-typed-rup-support-witness-necessity`

Role: `boundary`

This packet records the boundary theorem added after the prefix-typed
append-only RUP-CDCL corollary.  The positive corollary removes the
proof-internal label decoder when formula-label variables are public syntax.
This proposition shows that the remaining support-local auxiliary witness is
not removable by public typing and append-only RUP checking alone.

## Theorem Summary

Measured object: typed append-only RUP-CDCL trace without support-local
auxiliary witnesses.

Conclusion: public formula-label typing and append-only RUP checking do not
certify completion-local auxiliary support without an additional support-local
witness or an equivalent proof-system invariant.

Proof-system status:
`boundary_for_prefix_typed_append_only_RUP_CDCL_support_locality_not_free`.

## Boundary Mechanism

- scan the public formula-label namespace in the append-only log and RUP
  certificates;
- fix the scanned support set \(W\);
- use a same-skeleton auxiliary lift whose displayed clausal replay is
  unchanged but whose semantic soundness depends on a hidden label
  \(h\notin W\);
- choose two completions agreeing on \(W\) and differing at \(h\);
- observe that the trace, public scan, and RUP certificates are identical while
  auxiliary support-locality differs.

## Nonclaims

This proposition does not refute the prefix-typed append-only RUP-CDCL lower
bound, which assumes support-local auxiliary witnesses.  It does not rule out a
proof system whose ordinary rules intrinsically enforce auxiliary
support-locality.  It does not handle deletion-bearing or untyped RUP/DRUP
traces, arbitrary CDCL, Frege, Extended Frege, IPS, arbitrary compressed proofs,
or an explicit SAT-family/source lower bound.

## Coherence

Closest literature object: typed append-only clausal traces with public
variable roles and checker-visible RUP certificates.

Before: after public label typing, the remaining support-local witness
obligation could look like removable bookkeeping.

After: the witness is a real semantic invariant unless an intrinsic
proof-system rule supplies the same completion-locality fact.

C11 role: `boundary`.

Why not fragmented: it sharpens the exact blocker left by the strongest current
RUP-CDCL bridge and prevents the next loop from chasing a false “syntax alone”
route.
