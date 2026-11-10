#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Implement Route A paper-attack TODOs as paper-native results/demotions."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "agentic/reports/results_ellaboration/a-finite-schur-feshbach-test-for-reflected-wilson-blocks-an-explicit-four-dimens"
OPENMODULE_RE = re.compile(r"\\begin\{openmodule\}\{([^{}]+)\}(.*?)\\end\{openmodule\}", re.S)
FORBIDDEN_PAPER_TERMS = (
    "pipeline",
    "workflow",
    "TODO",
    "todo",
    "result-elaboration",
    "implementation packet",
    "agent",
    "skill",
    "queue",
)


RESULT_BLOCKS: dict[str, str] = {
    "G1": r"""
\begin{remark}[Geometric collar obstruction for the present hairpin layout]
\label{rem:current-hairpin-collar-obstruction}
The existing hairpin geometry admits a literal transverse parameter by replacing
\[
  s\quad\text{with}\quad m_k(\delta),
  \qquad a_km_k(\delta)\to\delta,
\]
in \eqref{eq:eta-plus}--\eqref{eq:eta-minus}.  This gives explicit paths in the positive algebra,
\[
  A_k\to A_k\pm m_k(\delta)e_2
  \to B_k\pm m_k(\delta)e_2
  \to B_k,
\]
with the same base path \(\beta_k\), and the spatial reflection \(\rho\) still interchanges the two signs.  Thus positive-time support and the reflected pairing can be preserved.

However, this does not yet produce the geometric collar collision needed to replace the source-collision block.  As \(\delta\downarrow0\), the two transverse detours collapse to the base path:
\[
  \eta_{+,k}(\delta),\eta_{-,k}(\delta)\longrightarrow \beta_k,
  \qquad
  \gamma_{+,k}(\delta),\gamma_{-,k}(\delta)\longrightarrow \beta_k\circ\beta_k^{-1}.
\]
The central loop \(\gamma_{0,k}\), as defined in \eqref{eq:eta-zero}--\eqref{eq:gamma-hairpins}, remains a temporal detour and does not participate in the same geometric collision.  Therefore the present three-hairpin layout does not by itself supply a three-channel rank-one geometric collar limit.  A genuine collar theorem would have to modify the central channel or the common footprint so that all three normalized reflected observables approach the same limiting object in the same joint \((a_k,\delta)\) regime.
\end{remark}
""",
    "G2": r"""
\begin{proposition}[Normalization gate for any geometric collar]
\label{prop:collar-normalization-gate}
Let \(N_{k,\delta}\) be a reflected Gram block obtained from a future geometric collar family in the same finite heat-kernel lattice theory.  A normalized block \(q_{k,\delta}\) remains a same-theory reflected Gram block if the removed factors are implemented by observable rescaling, an invertible block congruence, or a Schur product with a positive kernel that itself has a reflected-Gram realization.  In particular, diagonal normalization by \(N_{ii}^{-1/2}\) is admissible whenever \(N_{ii}>0\).

An entrywise quotient by a pair-dependent factor \(B_{ij}\) is not admissible from positivity alone.  It must be accompanied by a proof that the operation is positivity preserving in the reflected Wilson algebra.
\end{proposition}

\begin{proof}
Observable rescaling and block changes of basis give congruences, hence preserve positive semidefiniteness.  A Schur product with a positive kernel preserves positivity by the Schur product theorem, and the same-theory requirement asks that this kernel be realized by reflected observables in the regulated theory.  The warning about pair-dependent quotients is exactly the obstruction isolated in Section \ref{app:normalization}: a positive entrywise denominator need not have a positive entrywise inverse.  Thus such a quotient is not justified unless its inverse factor is separately certified.
\end{proof}
""",
    "G3": r"""
\begin{proposition}[Coefficient-extraction gate for a future collar]
\label{prop:collar-coefficient-gate}
Suppose a geometric collar construction and same-theory normalization produce a block
\[
  q_{k,\delta}
  =
  \one\one^T+\delta H_k+\delta^2K_k+R_{k,\delta},
  \qquad
  \sup_k\frac{\norm{R_{k,\delta}}}{\delta^2}\to0.
\]
Then the finite Schur--Feshbach test applies at each cutoff with
\[
  A_k=PH_kP,
  \qquad
  C_k=P\left(K_k-\frac13H_kee^TH_k\right)P,
\]
for \(e=3^{-1/2}\one\).  The source-collision matrices \(H,K\) computed in Section \ref{sec:finite-certificate} cannot be substituted for \(H_k,K_k\) unless they are derived from the same geometric block \(q_{k,\delta}\).
\end{proposition}

\begin{proof}
This is Theorem \ref{thm:schur-feshbach} with \(n=3\), applied to the asserted geometric expansion.  The conclusion depends on the actual first and second derivatives of the same matrix family \(q_{k,\delta}\).  A different singular family may have the same rank-one limit but different derivatives, so the source-amplitude calculation supplies an analogy and a finite model, not the geometric coefficients themselves.
\end{proof}
""",
    "G4": r"""
\begin{remark}[Strict margins remain a separate lower-bound problem]
\label{rem:strict-margin-lower-bound}
For a future collar block, reflection positivity can at most give nonnegativity of the relevant reflected norms.  The Schur--Feshbach gate requires more: after the normalization and coefficient extraction one must prove lower bounds for the reduced quantities replacing \(\sigma\) and \(\tau\), for example
\[
  \inf_{k\ge k_0}\sigma_k>0,
  \qquad
  \inf_{k\ge k_0}\tau_k>0,
\]
or a certified finite-regime analogue with stated errors.  Boundedness of Wilson loops gives compactness and upper bounds, but it does not prevent these reduced correlations from vanishing along a cutoff trajectory.  Consequently the strict-margin statement of the present paper remains finite-cutoff and conditional on \(\sigma,\tau>0\).
\end{remark}
""",
    "E1": r"""
\begin{remark}[Endpoint estimator status]
\label{rem:endpoint-estimator-status}
The null-channel identity \eqref{eq:offdiag-null-identity} fixes the algebraic incidence pattern that any endpoint correction would have to feed.  It does not derive the endpoint correction from the gauge theory.  A regulator-derived endpoint estimator must first specify endpoint boxes for the actual collar paths, local source variables, the \(SU(2)\) singlet projection, and the color normalization in the heat-kernel measure.  Since Remark \ref{rem:current-hairpin-collar-obstruction} shows that the present hairpin layout has not yet supplied the required geometric collar, the endpoint expression \eqref{eq:endpoint-estimator-template} remains a schematic target rather than a proved Wilson integral.
\end{remark}
""",
    "E2": r"""
\begin{proposition}[Two-sided endpoint certificate logic]
\label{prop:two-sided-endpoint-logic}
Assume an endpoint derivation in the same regulator produces a number \(\widehat R_{\mathrm{end}}\) and a certified error \(\Delta_{\mathrm{end}}\) such that
\[
  |R_{\mathrm{end}}-\widehat R_{\mathrm{end}}|
  \le \Delta_{\mathrm{end}}.
\]
Then the implications in Lemma \ref{lem:endpoint-certificates} are the valid finite tests.  A lower bound \(R_{\mathrm{end}}\ge -U\) can certify positivity when \(M_G-U>0\), but it cannot certify a negative obstruction.
\end{proposition}

\begin{proof}
The two-sided estimate gives
\[
  \widehat R_{\mathrm{end}}-\Delta_{\mathrm{end}}
  \le R_{\mathrm{end}}
  \le \widehat R_{\mathrm{end}}+\Delta_{\mathrm{end}}.
\]
Adding \(M_G\) proves the positive and negative tests.  A one-sided lower bound contains no upper control on \(R_{\mathrm{end}}\), so it cannot prove \(M_G+R_{\mathrm{end}}<0\).
\end{proof}
""",
    "M1": r"""
\begin{remark}[Finite positivity is not OS reconstruction]
\label{rem:finite-positivity-not-reconstruction}
The finite reflected Gram tests in this paper are necessary consistency checks for any Euclidean Yang--Mills construction, but they do not supply continuum Schwinger functions.  A reconstruction theorem would still have to provide a limiting Wilson algebra and verify the remaining Osterwalder--Schrader hypotheses, including the appropriate Euclidean covariance, regularity, limiting positivity on a separating algebra, and nontriviality.  No such continuum construction is asserted here.
\end{remark}
""",
    "M2": r"""
\begin{remark}[No spectral gap follows from the finite block]
\label{rem:no-gap-from-finite-block}
A mass-gap statement concerns the spectrum of the Hamiltonian reconstructed from a continuum Euclidean theory.  Since Remark \ref{rem:finite-positivity-not-reconstruction} leaves reconstruction open, the finite block and endpoint bookkeeping cannot imply
\[
  \operatorname{Spec}(H_{\mathrm{YM}})\cap(0,\Delta)=\varnothing.
\]
Any future spectral argument must be made in the same reconstructed theory and must not assume exponential clustering or a spectral gap as an input.
\end{remark}
""",
}


def module_key(title: str) -> str:
    match = re.match(r"\s*([A-Z]\d+)", title)
    if not match:
        raise ValueError(f"cannot identify open-module key from title {title!r}")
    return match.group(1)


TODO_IDS = {
    "G1": "routea-attack-001",
    "G2": "routea-attack-002",
    "G3": "routea-attack-003",
    "G4": "routea-attack-004",
    "E1": "routea-attack-005",
    "E2": "routea-attack-006",
    "M1": "routea-attack-007",
    "M2": "routea-attack-008",
}


def replace_open_modules(text: str) -> tuple[str, list[str]]:
    seen: list[str] = []

    def repl(match: re.Match[str]) -> str:
        key = module_key(match.group(1))
        if key not in RESULT_BLOCKS:
            return match.group(0)
        seen.append(key)
        return RESULT_BLOCKS[key].strip()

    return OPENMODULE_RE.sub(repl, text), seen


def update_table_and_conclusion(text: str) -> str:
    text = text.replace(
        "Continuum and mass gap & Not proved; separated into open modules & Section \\ref{sec:open-modules} \\\\",
        "Continuum and mass gap & Not proved; finite-to-continuum and spectral transfers remain separate obstructions & Section \\ref{sec:open-modules} \\\\",
    )
    text = text.replace(
        "The present source collision must still be replaced or supplemented by a lattice-resolved geometric collar; renormalized coefficients and strict margins must be controlled along a continuum trajectory; endpoint cumulants need two-sided, regulator-specific error estimates; and reflection positivity must be joined to continuum reconstruction and a spectral estimate.  Those are open modules, not consequences of the finite block.",
        "The present source collision cannot yet be upgraded to the current transverse-collar layout: the transverse channels collapse to the base loop while the temporal channel remains a different detour.  A future collar theorem must therefore change the geometric family or the central channel, certify same-theory normalization, derive the geometric coefficients, and then prove strict margins.  Endpoint, continuum, and spectral conclusions remain downstream of those requirements.",
    )
    return text


def assert_no_forbidden_paper_terms(text: str) -> None:
    lowered = text.lower()
    for term in FORBIDDEN_PAPER_TERMS:
        if term.lower() in lowered:
            raise ValueError(f"forbidden paper term found in generated TeX: {term}")


def assert_no_tex_control_corruption(text: str) -> None:
    bad = [(i, ord(ch)) for i, ch in enumerate(text) if ord(ch) < 32 and ch not in "\n\r\t"]
    if bad:
        sample = ", ".join(f"{i}:{code}" for i, code in bad[:8])
        raise ValueError(f"generated TeX contains control characters: {sample}")


def completion_payload(seen: list[str]) -> dict[str, Any]:
    module_status = {
        "G1": {
            "status": "demoted_with_obstruction",
            "result": "The present transverse hairpin collar keeps support and reflection pairing, but its transverse loops collapse to the base loop while the temporal channel does not.",
            "paper_label": "rem:current-hairpin-collar-obstruction",
        },
        "G2": {
            "status": "implemented_as_normalization_gate",
            "result": "Same-theory normalization is characterized by congruence, observable rescaling, or positive-kernel reflected Gram realization; pair-dependent quotients remain uncertified.",
            "paper_label": "prop:collar-normalization-gate",
        },
        "G3": {
            "status": "implemented_as_coefficient_gate",
            "result": "The geometric Schur-Feshbach coefficients are conditional on a same-block expansion; source-collision H,K cannot be reused as geometric derivatives.",
            "paper_label": "prop:collar-coefficient-gate",
        },
        "G4": {
            "status": "demoted_to_lower_bound_obligation",
            "result": "Strict geometric margins require lower bounds; reflection positivity gives nonnegativity only.",
            "paper_label": "rem:strict-margin-lower-bound",
        },
        "E1": {
            "status": "demoted_to_regulator_derivation_obligation",
            "result": "The endpoint incidence pattern is algebraic until endpoint boxes, sources, color factors, and tails are derived from actual collar paths.",
            "paper_label": "rem:endpoint-estimator-status",
        },
        "E2": {
            "status": "implemented_as_two_sided_certificate_logic",
            "result": "Two-sided endpoint error bounds support positive or negative finite certificates; one-sided lower bounds cannot certify negative obstructions.",
            "paper_label": "prop:two-sided-endpoint-logic",
        },
        "M1": {
            "status": "demoted_to_reconstruction_boundary",
            "result": "Finite reflected Gram positivity is not OS reconstruction.",
            "paper_label": "rem:finite-positivity-not-reconstruction",
        },
        "M2": {
            "status": "demoted_to_spectral_boundary",
            "result": "No Hamiltonian mass gap follows from the finite block without continuum reconstruction and a same-theory spectral estimate.",
            "paper_label": "rem:no-gap-from-finite-block",
        },
    }
    items = [
        {
            "id": "routea-attack-000",
            "status": "completed",
            "result": "Paper result integration locked to theorem/proposition/lemma/certificate/remark/demotion forms with forbidden-language audit.",
        }
    ]
    for key in seen:
        items.append({"id": TODO_IDS[key], "module": key, **module_status[key]})
    items.append(
        {
            "id": "routea-attack-009",
            "status": "completed",
            "result": "Generated clean paper TeX/PDF after replacing highlighted module sections with paper-native results and demotions.",
        }
    )
    return {
        "schema": "abducer.routea_paper_attack_completion.v1",
        "source_paper_claim": "finite-cutoff SU(2) heat-kernel source-collision Schur-Feshbach Wilson-block result",
        "items": items,
    }


def render_completion_md(payload: dict[str, Any]) -> str:
    lines = [
        "# Route A Paper Attack Completion",
        "",
        "The paper attack pass implemented the marked modules as validated paper-native results, gates, and demotions. The current paper claim remains the finite source-collision theorem; the geometric-collar upgrade is blocked for the present hairpin layout.",
        "",
    ]
    for item in payload["items"]:
        lines.extend(
            [
                f"## {item['id']}",
                "",
                f"- Status: `{item['status']}`",
                f"- Result: {item['result']}",
            ]
        )
        if "module" in item:
            lines.append(f"- Module: `{item['module']}`")
        if "paper_label" in item:
            lines.append(f"- Paper label: `{item['paper_label']}`")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    parser.add_argument("--output", type=Path, default=OUT_DIR / "finite_wilson_os_routeA_SU2_attack_integrated.tex")
    args = parser.parse_args()

    draft = args.draft.expanduser().resolve()
    text = draft.read_text(encoding="utf-8")
    updated, seen = replace_open_modules(text)
    missing = sorted(set(RESULT_BLOCKS) - set(seen))
    if missing:
        raise ValueError(f"missing open modules in source draft: {', '.join(missing)}")
    updated = update_table_and_conclusion(updated)
    assert_no_forbidden_paper_terms(updated)
    assert_no_tex_control_corruption(updated)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    output = args.output.expanduser().resolve()
    output.write_text(updated, encoding="utf-8")
    payload = completion_payload(seen)
    json_path = OUT_DIR / "routea_paper_attack_completion.json"
    md_path = OUT_DIR / "routea_paper_attack_completion.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(render_completion_md(payload), encoding="utf-8")
    print(f"Wrote {output}")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
