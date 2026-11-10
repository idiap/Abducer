<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Controller-Complete Adaptive Audit Normalizer

- Status: `proved_in_revised_tex`
- TeX label: `prop:controller-complete-adaptive-audit-normalizer`
- Criteria affected: `C5`, `C8`, `C9`, `C10`, `C11`
- Result role: proof-system bridge.

## Claim

A hidden adaptive transcript becomes a sound support normalizer only when it is
accompanied by a controller-complete audit.  The audit must expose a finite
acyclic controller, certify that the hidden controller agrees with the exposed
controller on the completion cylinder being claimed, and list the queried
frontier coordinates on the replayed path.

Under those hypotheses, root plus the audited path coordinates is
support-local.  If the audit certifies the whole controller globally, then the
minimum support is exactly root plus the ordinary pointwise certificate
complexity of the exposed controller.

## C11 Admission Card

- Role: `proof_system_bridge`
- Flagship obstruction strengthened: proof-object support budget for the
  formula-footprint barrier.
- Before/after shift: before, hidden adaptive summaries were only separated as
  unsound transcript-only evidence; after, the paper states the precise positive
  audit object that turns such a summary into checker-visible support.
- Boundary clarified: a transcript is not enough; controller completeness and
  local equivalence to an exposed acyclic controller are the measured objects.
- Remaining nonclaim: arbitrary hidden SAT self-reduction semantics, learned
  clauses, cyclic controllers, and raw proof-system traces are not shown to
  supply such an audit.
- Narrative indivisibility: separated from the formula-footprint spine, the
  theorem is just a bookkeeping lemma; inside the paper it identifies exactly
  what a proof artifact must expose to pay for hidden adaptive support.

## Proof Skeleton

1. Let the audit expose an acyclic branching program \(B\), a replay path
   \(\pi\), and a support \(S\) containing the root and every frontier query on
   \(\pi\).
2. For any completion preserving \(S\), the same queried values force the same
   path \(\pi\) through \(B\).
3. The terminal value on \(\pi\) is the hard root value.
4. Controller completeness certifies that the hidden controller agrees with
   \(B\) on every completion preserving \(S\).
5. Therefore every preserving completion satisfies the residual relation, so
   \(S\) is support-local.
6. If the audit is global, the visible branching-program theorem gives the
   exact minimum support \(1+C_b(F_B,a|_Q)\).

## Nonclaims

- no arbitrary hidden adaptive SAT self-reduction invariant;
- no learned-clause semantic influence theorem;
- no cyclic semantic dependency theorem;
- no support extraction from transcript summaries without controller audit;
- no explicit SAT-carrier lower bound.
