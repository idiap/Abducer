<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Support-Declared Macro ER Normalizer

- Status: `proved_in_revised_tex`
- TeX corollary label: `cor:support-declared-macro-er`
- Criteria affected: `C5`, `C8`, `C10`, `C11`

## Result

The revised paper now proves the support-budget analogue of the macro-compressed ER tradeoff.

For a macro-compressed extension refutation, suppose the compressed object supplies a declared formula-label support \(S_\rho\) and a sound support invariant: every completion of labels agreeing with the hard labeling on \(S_\rho\) has some macro/extension witness satisfying the compressed macro constraints and final clauses.  If the easy-completion CNF plus those constraints has a resolution refutation, then \(S_\rho\) is a completion-sound formula-label certificate.

Therefore, for each polarity \(b\),
\[
  g_n+c\mathrm{Lookup}(M_n,|S_{\rho,b}|,\ell_n)+cM_n>s.
\]

Near threshold,
\[
  |S_{\rho,0}|,|S_{\rho,1}|\ge n^{a-o(1)}.
\]

If the support declaration has budget \(|S_\rho|\le B(|\rho|)\), then
\[
  B(|\rho|)\ge 2n^{a-o(1)}.
\]

## Proof Skeleton

1. Treat the macro-compressed proof object as a compressed support-local auxiliary package \(\Gamma_\rho(Y,W)\).
2. The declared support invariant says \(\Gamma_\rho\) remains satisfiable under every completion preserving \(S_\rho\).
3. A refutation of \(\Phi_{n,s,A}\wedge\Gamma_\rho\) then makes every such completion hard.
4. Hence \(\lambda|_{S_\rho}\) is a formula-label \(1\)-certificate.
5. Apply the formula-footprint theorem and the near-threshold corollary.

## Nonclaim Boundary

This is not a lower bound for arbitrary compressed proofs, Frege, Extended Frege, IPS, implicit proofs, or macros with unsound or hidden nonlocal support.  It applies only when the proof object supplies a sound declared formula-label support or when a separate normalizer proves such a support declaration.

## Gate Impact

This is a C11-admitted proof-system bridge.  It does not add a fragmented side result: it directly answers the next-loop support-budget question by saying that compressed macro syntax can avoid displayed expansion only if it exposes a large sound support declaration, or else leaves the present local-completion framework.
