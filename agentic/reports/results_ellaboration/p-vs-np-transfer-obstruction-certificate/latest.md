<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# P vs NP Result Refinement Packet

- Status: `pvsnp_result_refinement_ready`
- Target: `p-vs-np-target`
- Paper project: `p-vs-np-transfer-obstruction-certificate`
- Epistemic status: `paper_scaffold_ready_for_theorem_consolidation`

## Smallest Honest Claim

For a named P vs NP bridge route whose source carrier H_N is upper-bounded from SAT circuits by SIZE(H_N) <= N^{q+beta c+o(1)}, a barely-superlinear lower bound SIZE(H_N)>N^a rules out only target exponents c satisfying a>q+beta c. Therefore beta>0 gives a bounded-window obstruction, not an NP not subset P/poly result.

## Current Consolidation Target

- Object: `TransparentRowSupport_N`
- Status: `consolidation_target`
- Claim: The recent FormulaEval selector cases should be collapsed into one abstraction: a FormulaEval mechanism is target-preserving exactly when the selected row support is proof-visible, advice-free, influence-closed, enumerable or explicitly scan-charged, and row-expanded inside the same Gamma ledger.

### Theorem Pair

- Positive theorem: If a Psys_sym FormulaEval mechanism satisfies TransparentRowSupport_N with discovery charge U_N, row-support size T_N, and FormulaEval expansion charge X_N, then the existing bEF parser extends to Gamma_trans(pi)=Gamma_bEF(pi)+U_N+X_N. If N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)}, the alleged LB_N(1+epsilon) certificate is falsified in the same nonuniform SIZE model.
- Countermodel theorem: If a FormulaEval mechanism lacks visible row support, selector extensionality, influence closure, or a charged semantic-realizer, then a private-row or unread-enable-bit construction gives two proof surfaces with the same parsed transcript but different FormulaEval dependence or carrier parity. Occurrence completion is therefore invalid.

### Stop Rule

Do not add more selector classes unless they either instantiate TransparentRowSupport_N as a nontrivial example needed by the paper or disprove one of its definition fields. The next cycle must draft/prove the generic theorem pair.

## Readiness

- Decision: `paper_scaffold_ready_for_theorem_consolidation`
- Permitted claim: A scoped parser/falsifier obstruction note: transparent FormulaEval row support has an exact Gamma charge, while hidden semantic FormulaEval support is blocked by a private-row countermodel.

## Missing Blockers

- unify the selector zoo under one TransparentRowSupport_N definition rather than accumulating more cases
- write the positive theorem and private-row countermodel theorem as the main paper pair
- complete nearest-work comparison before strong novelty language
- prove or demote RealSATInfluenceRealizer_N as an explicit open problem rather than leaving it as semantic fog

## Next Paper Actions

- Promote TransparentRowSupport_N from cycle evidence into a formal definition.
- Write the Gamma extension theorem and private-row countermodel theorem as the main result pair.
- Move selector cases into examples, not new main claims.
- Add a prior-art paragraph around hardness magnification, MCSP/MKtP, natural proofs, relativization, and algebrization.
- Close with RealSATInfluenceRealizer_N and AC0 output-sensitive enumeration as exact open problems.
