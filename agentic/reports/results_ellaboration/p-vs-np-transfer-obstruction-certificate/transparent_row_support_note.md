<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Transparent Row Support for FormulaEval: A Parser/Falsifier Boundary

- Status: `transparent_row_support_note_ready`
- Epistemic status: `paper_scaffold_not_main_theorem`
- Source packet: `agentic/reports/results_ellaboration/p-vs-np-transfer-obstruction-certificate/latest.json`

## Abstract Claim

This note consolidates the recent P vs NP discovery cycles into a scoped theorem pair. Transparent FormulaEval row support extends the Gamma parser ledger and yields an upper-bound falsifier; hidden semantic support is blocked by a private-row or unread-enable-bit countermodel.

## Non-Claims

- This does not prove P != NP.
- This does not prove SAT outside P/poly.
- This is a proof-system transfer obstruction and parser/falsifier boundary.

## Definition: TransparentRowSupport_N

- **influence_closure**: every row whose SAT value can change a FormulaEval line is included in the charged support
- **no_hidden_advice**: row support cannot be supplied by nonuniform tables, semantic oracles, or private enable bits unless charged
- **row_enumeration_or_scan_charge**: either RowSetEnumerator_N outputs selected rows with certified cost U_N or the parser pays the full scan charge F_FE N^{1+q+o(1)}
- **row_expansion_charge**: each distinct selected row contributes the complete occurrence/SAT expansion term, typically N times the row count or T_N M_N in projected formulations
- **same_theory_parser**: all support, selector, extension, and SAT occurrence conventions are read by the same proof verifier and circuit model
- **visible_selector_code**: the proof displays the row predicate, extension rule, or enumerator certificate used to select rows

## Theorem A: Transparent Support Gives A Gamma Falsifier

If a Psys_sym FormulaEval mechanism satisfies TransparentRowSupport_N with discovery charge U_N, row-support size T_N, and FormulaEval expansion charge X_N, then the existing bEF parser extends to Gamma_trans(pi)=Gamma_bEF(pi)+U_N+X_N. If N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)}, the alleged LB_N(1+epsilon) certificate is falsified in the same nonuniform SIZE model.

### Proof Spine

- Parse all bEF, SATeq, bounded-SR_h, and extension dependencies into Gamma_bEF.
- Use visible selector or enumerator fields to compute the complete FormulaEval row support or pay full scan.
- Apply influence closure so every SAT row that can alter a FormulaEval line enters the charged support.
- Expand each charged row into the same occurrence/SAT representation used by the carrier H_N^SAT.
- Compose the public generator, parsed transcript, and residual patches into a nonuniform circuit for H_N^SAT.
- Contradict LB_N(1+epsilon) exactly when the total size is subthreshold.

## Theorem B: Hidden Support Gives A Private-Row Countermodel

If a FormulaEval mechanism lacks visible row support, selector extensionality, influence closure, or a charged semantic-realizer, then a private-row or unread-enable-bit construction gives two proof surfaces with the same parsed transcript but different FormulaEval dependence or carrier parity. Occurrence completion is therefore invalid.

### Countermodel Spine

- Choose a row r* not present in the parsed support Q_pi.
- Let a hidden enable bit or semantic selector decide whether r* participates in FormulaEval.
- Keep all displayed proof bits and charged occurrence neighborhoods fixed.
- Flip the uncharged SAT/FormulaEval value at r*.
- The parser outputs the same transcript while the selected support or H_N^SAT parity changes.

## Examples Subsumed

- interval-union FormulaEval
- proof-visible selector scan
- ROBDD selector
- guarded deterministic decomposable NNF selector
- projected guarded-dDNNF with witness or projected-enumerator charge

## Open Problems

- RealSATInfluenceRealizer_N: force semantic FormulaEval influence into visible charged support.
- AC0PrefixNonemptiness_N or an equivalent output-sensitive enumeration theorem for AC0 selectors.
- Prior-art comparison against hardness magnification, MCSP/MKtP, natural proofs, relativization, and algebrization.

## Stop Rule

Do not add more selector classes unless they either instantiate TransparentRowSupport_N as a nontrivial example needed by the paper or disprove one of its definition fields. The next cycle must draft/prove the generic theorem pair.

## Next Paper Action

Write the TransparentRowSupport_N theorem/countermodel pair as the paper core before running more exploratory cycles.
