<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Provenance-Typed LRAT Support Audit

- Status: `proved_in_revised_tex`
- TeX corollary label: `cor:provenance-typed-lrat`
- Criteria affected: `C5`, `C8`, `C10`, `C11`
- Result role: `proof_system_bridge`

## Purpose

The support-audited LRAT theorem assumes a support audit as a verified invariant.
The support-erasure separator explains why this audit cannot be recovered from
untyped clausal syntax alone.  This corollary closes the trusted-provenance
branch: a typed variable-role map plus block-local clause provenance is enough
to produce the required support audit.

## Statement

Let an LRAT-style checked trace, or a DRAT trace accompanied by an LRAT
certificate, refute
\[
  \Phi_{n,s,A}(Y,Z)\wedge \bigwedge_{j\in J}\Gamma_j(Y,W_j).
\]
Assume the trace carries a trusted provenance package:

1. a variable-role map identifying formula-label variables \(Y_u\) and
   auxiliary blocks \(W_j\);
2. disjoint auxiliary blocks \(W_j\);
3. a declared formula-label support \(P_j\subseteq U_n\) for each block;
4. a checked local witness invariant: every labeling agreeing with the hard
   labeling on \(P_j\) has some witness assignment satisfying
   \(\Gamma_j\);
5. derived-clause provenance is the union of antecedent provenance, while the
   final support budget is \(S_\tau=\bigcup_j P_j\).

Then \(S_\tau\) is a sound support audit.  Hence the formula-footprint lower
bound applies to the provenance-typed trace:
\[
  |S_{\tau,0}|, |S_{\tau,1}| \ge n^{a-o(1)}
\]
near threshold, and any checker-visible support budget \(B(|\tau|)\) satisfies
\[
  B(|\tau|)\ge 2n^{a-o(1)}.
\]

## Proof Skeleton

1. A completion agreeing with the hard labeling on \(S_\tau\) agrees on every
   block support \(P_j\).
2. The local witness invariant supplies a satisfying witness for each block.
3. Disjoint auxiliary blocks let the witnesses be combined into one global
   auxiliary assignment satisfying the whole \(\Gamma_\tau\).
4. Therefore the provenance package verifies the support-audit invariant
   required by the support-audited LRAT theorem.
5. LRAT soundness and the formula-footprint theorem give the polarity and
   budget lower bounds.

## Nonclaim Boundary

This does not prove a lower bound for raw unaudited LRAT/DRAT, for untyped
traces with erased variable roles, for provenance packages whose auxiliary
blocks share variables without a separate compatibility proof, or for stronger
systems such as Frege, Extended Frege, IPS, or arbitrary compressed proofs.

## Gate Impact

This is C11-admitted proof-system bridge work.  It upgrades the previous
support-audit assumption into an explicit checker-facing provenance discipline:
trusted typed provenance is now a proved route to the Formula Footprints
support-budget lower bound, while plain unaudited LRAT/DRAT remains outside the
claim.
