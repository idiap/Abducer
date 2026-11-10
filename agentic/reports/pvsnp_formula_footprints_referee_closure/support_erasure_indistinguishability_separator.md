<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Support-Erasure Indistinguishability Separator

- Status: `proved_in_revised_tex`
- TeX proposition label: `prop:support-erasure-indistinguishability`
- Criteria affected: `C5`, `C8`, `C9`, `C11`
- Result role: `boundary`

## Purpose

This packet strengthens the support-audit necessity separator.  The earlier
separator shows that a short LRAT-style refutation can coexist with a large
minimum sound support audit.  This theorem adds the provenance point: after
erasing variable-role metadata, the same clausal trace can have two semantic
lifts with different formula-label support requirements.

Thus an untyped or provenance-erased LRAT/DRAT trace does not determine the
completion-local support object.  A support audit, typed variable map, or
equivalent provenance certificate is not cosmetic.

## Statement

For every finite set \(T\) and assignment \(\alpha:T\to\{0,1\}\), consider the
clausal skeleton \(C_T\) consisting of:

- unit clauses fixing variables \(P_u\) to \(\alpha(u)\);
- one blocking clause falsified exactly by that joint assignment.

The same linear LRAT-style resolution trace refutes \(C_T\) in two semantic
lifts:

1. **auxiliary lift:** the variables \(P_u\) are auxiliary variables unrelated
   to formula labels; the support-local witness has empty formula-label support;
2. **label lift:** the variables \(P_u\) are formula-label variables \(Y_u\);
   every sound support declaration must contain all of \(T\).

The raw clausal skeleton and LRAT antecedent hints are identical.  The support
difference is entirely in the erased provenance map.

## Proof Skeleton

1. The syntactic refutation is the same in both lifts: resolve the blocking
   clause against the unit clauses.
2. In the auxiliary lift, for every formula labeling, set each auxiliary
   \(P_u\) to \(\alpha(u)\); no formula-label coordinate is needed.
3. In the label lift, omitting \(u\in T\) from the declared support lets a
   completion flip \(Y_u\), falsifying its unit clause.
4. Therefore the same untyped trace supports two incompatible support budgets,
   so trace checking alone cannot certify completion-local support.

## Boundary

This is not a lower bound for every unannotated LRAT/DRAT trace.  It is an
indistinguishability boundary for support extraction from trace syntax alone.
If a proof format includes a trusted variable-role map, clause provenance, or
support-locality checker, then it has added exactly the kind of audit object
required by the support-audited LRAT theorem.

## Gate Impact

This is C11-admitted boundary work.  It strengthens the single
formula-footprint spine by explaining why the proof-system bridge cannot be
obtained from an untyped clausal refutation alone: the missing object is not
more LRAT checking, but semantic support provenance.
