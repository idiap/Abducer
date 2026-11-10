<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Carrier-Independent Audit Upgrade Criterion

- Status: `proved_in_revised_tex`
- TeX label: `cor:carrier-independent-audit-upgrade`
- Criteria affected: `C5`, `C8`, `C10`, `C11`
- Result role: `proof_system_bridge`

## Statement

If a recognizable proof or certificate system has a polynomial-time,
proof-system-intrinsic audit extractor

\[
  \mathsf{Aud}_{\mathcal P}(\pi,n)=(S_\pi,\Gamma_\pi,\mathcal W_\pi)
\]

that computes formula-label support, a support-local CNF, and support-locality
evidence from the proof artifact itself, without a carrier-specific namespace
manifest, hidden role advice, or semantic oracle, then the support-local
normalization transfer theorem applies.

In the near-threshold regime, any budget \(B(|\pi|)\) controlling the extracted
support and audit data satisfies

\[
  B(|\pi|)\ge 2n^{a-o(1)}.
\]

If \(B(L)=O(L^k)\), then every accepted proof has length
\[
  |\pi|\ge n^{a/k-o(1)}.
\]

## Proof Object

The proof is a direct packaging of `thm:support-local-normalization-transfer`.
The audit extractor supplies the four required objects:

- support set \(S_\pi\);
- support-local CNF \(\Gamma_\pi(Y,W)\);
- sound refutation of \(\Phi_{n,s,A}\wedge\Gamma_\pi(Y,W)\);
- budget \(B(|\pi|)\) controlling support plus audit data.

The new contribution is not a stronger lower bound by itself.  It converts the
remaining publication-level proof-system blocker into a checkable theorem
target: the audit must be intrinsic to the proof system rather than imported
from a carrier-specific manifest.

## C11 Admission

This is admitted as proof-system bridge work, not as an independent side result.
It strengthens the same formula-footprint spine by making the before/after
understanding shift explicit:

- before: the remaining proof-system blocker was a broad request for a stronger
  recognizable invariant;
- after: the blocker is an exact extractor obligation with support-locality,
  soundness, and budget fields.

## Nonclaims

- no lower bound for Frege, Extended Frege, IPS, or arbitrary compressed proofs;
- no support extraction from raw RUP/DRUP/LRAT/DRAT/CDCL syntax;
- no replacement for an explicit SAT-family or source lower-bound theorem;
- no top-paper completion unless a concrete system instantiates the extractor.
