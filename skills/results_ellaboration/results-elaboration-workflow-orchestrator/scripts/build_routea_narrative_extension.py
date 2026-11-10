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
"""Build a narrative-only Route A extension draft by editing open modules only."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "agentic/reports/results_ellaboration/a-finite-schur-feshbach-test-for-reflected-wilson-blocks-an-explicit-four-dimens"
OPENMODULE_RE = re.compile(r"\\begin\{openmodule\}\{([^{}]+)\}(.*?)\\end\{openmodule\}", re.S)


NARRATIVE_MODULES = {
    "G1": r"""
The finite construction uses a source collision, so the geometry of the three primitive hairpins is fixed while the matrix block becomes singular.  A geometric collar version must instead introduce a family of lattice paths
\[
  \gamma_{+,k}(\delta),\qquad
  \gamma_{-,k}(\delta),\qquad
  \gamma_{0,k}(\delta)
\]
on the cutoff lattice \(\Lambda_k\), with lattice spacing \(a_k\), such that the collar width is represented by an integer transverse displacement \(m_k(\delta)\) satisfying \(a_km_k(\delta)\to\delta\).  The base, longitudinal, and temporal scales should be chosen with
\[
  a_kr_k\to R,\qquad a_ks_k\to S,\qquad a_kh_k\to H,
\]
and every edge of every path must remain in the positive-time algebra used by the reflection-positive lattice theory.

The essential geometric condition is not merely that the paths converge as sets.  The reflected Wilson block requires a locked boundary footprint: the portions of the three paths that meet the reflection plane must agree in the sense needed to compare their reflected products, while the transverse collar sign distinguishes the \(+\) and \(-\) channels.  A satisfactory construction would therefore give explicit edge lists, prove
\[
  \rho\gamma_{+,k}(\delta)=\gamma_{-,k}(\delta),
  \qquad
  \rho\gamma_{0,k}(\delta)=\gamma_{0,k}(\delta),
\]
after reflection \(\rho\), and show that the common footprint is independent of the collar sign.  If this cannot be achieved with positive-time support and a stated joint limit \((a_k,\delta)\), the paper should retain the present source-collision result as the finite realization and not describe it as a geometric-collar theorem.
""",
    "G2": r"""
Once a geometric collar is introduced, the reflected Wilson entries will generally carry perimeter, cusp, endpoint, and boundary-overlap factors.  The normalization is legitimate only when these factors are removed inside the same reflected Gram problem.  One-body factors are harmless: if \(N\) is the unnormalized block and \(D_{k,\delta}\) is diagonal, then
\[
  N\succeq0
  \quad\Longleftrightarrow\quad
  D_{k,\delta}ND_{k,\delta}^{*}\succeq0,
\]
and this is realized by rescaling the observables themselves.  The finite source-collision block uses exactly this kind of normalization.

The dangerous case is a pair-dependent factor \(B_{ij}\).  Entrywise division \(N_{ij}/B_{ij}\) is not automatically positivity preserving.  A same-theory collar normalization must therefore prove one of two things: either the factor is actually produced by observable rescaling or block congruence, or the entrywise operation is a Schur product with a positive kernel, equivalently with a separately positive reflected Gram realization.  Without such a positivity certificate, the geometric collar block would no longer be a reflected Gram matrix in the regulated Yang--Mills theory, and any subsequent Schur--Feshbach conclusion would be outside the theory being tested.
""",
    "G3": r"""
The coefficient theorem needed for a geometric collar is the analogue of the exact source expansion, but with the geometric parameter \(\delta\) replacing the artificial source amplitude.  For the normalized geometric block one would need
\[
  q_{k,\delta}
  =
  \one\one^T+\delta H_k+\delta^2K_k+R_{k,\delta},
  \qquad
  \sup_k\frac{\norm{R_{k,\delta}}}{\delta^2}\longrightarrow0
\]
in the declared joint regime.  The matrices \(H_k\) and \(K_k\) must be obtained from the same normalized Wilson block produced by the collar construction and same-theory normalization, not imported from the source-collision model.

The practical calculation should separate three effects.  First, additive one-body variations are killed by the projection \(P\) onto \(\one^\perp\), so they do not determine the reduced first-order form.  Second, genuine pairwise second variations enter \(PK_kP\).  Third, the rank-one direction contributes the Schur--Feshbach correction
\[
  n^{-1}PH_k ee^*H_kP,
\]
which must be subtracted before reading the null-channel second-order margin.  The finite calculation in this paper shows why that subtraction matters: without it the second null-channel value contains a spurious \(\sigma^2\) contribution.  The geometric collar calculation would be stronger only if it derives the corresponding \(H_k,K_k\) and remainder bound from actual Wilson geometry.
""",
    "G4": r"""
Reflection positivity gives nonnegativity of reflected norms, but the finite Schur--Feshbach gate requires strict reduced margins.  In the source-collision block these margins are \(2\sigma\) and \(2\tau/3\).  In a collar family they become cutoff-dependent quantities, say \(\sigma_k\) and \(\tau_k\), after the renormalizations of G2 and the coefficient extraction of G3.  The required statement is a lower-bound result along the chosen cutoff trajectory, for example
\[
  \inf_{k\ge k_0}\sigma_k>0,
  \qquad
  \inf_{k\ge k_0}\tau_k>0,
\]
or a weaker but still nonvanishing bound sufficient for the scale at which the collar test is applied.

This is a genuinely mathematical input, not a consequence of bounded Wilson loops.  Boundedness supplies upper bounds and compactness of finite-dimensional blocks; it does not prevent the reduced norms from collapsing in the continuum limit.  Possible routes include a character-expansion estimate, a transfer-matrix lower bound, a symmetry argument excluding the vanishing channel, or a certified finite computation tied to a controlled cutoff regime.  If the available evidence gives only \(\sigma_k,\tau_k\ge0\), the strict-margin claim must remain finite-cutoff and conditional.
""",
    "E1": r"""
The endpoint estimator must be derived from the same \(SU(2)\) heat-kernel regulator and from the actual geometric paths of G1.  The first step is to define endpoint boxes around the places where the reflected collars meet the common boundary footprint, then introduce local source variables and singlet projections for the fundamental representation.  The color factor \(C_{\mathrm{col}}\) and the incidence weights must come from this local group integral and the path ordering of the Wilson loops.

For a normalized \(3\times3\) block with zero diagonal coefficient \(R\), the null-channel identity is
\[
  z^TRz=2R_{12}-4R_{13}-4R_{23},
  \qquad z=(1,1,-2)^T.
\]
Thus an endpoint calculation may have the schematic form
\[
  \widehat R_{\mathrm{end}}
  =
  C_{\mathrm{col}}\sum_v
  \left(
  2\widehat\kappa^{12}_{4,v}
  -4\widehat\kappa^{13}_{4,v}
  -4\widehat\kappa^{23}_{4,v}
  \right)
  +\widehat E_{\mathrm{tail}},
\]
but this formula is meaningful only after the endpoint boxes, cumulants, color normalization, and tail region have been derived from the regulated Wilson family.  Otherwise the incidence expression is only a mnemonic for the null-channel algebra, not a result about the lattice gauge theory.
""",
    "E2": r"""
The endpoint correction can be used in the Schur--Feshbach margin only with a two-sided error estimate.  The target estimate is
\[
  |R_{\mathrm{end}}-\widehat R_{\mathrm{end}}|
  \le \Delta_{\mathrm{end}},
\]
where \(R_{\mathrm{end}}\) is the exact endpoint contribution in the same regulator.  This requires bounds on the connected fourth source derivatives, the discretization error in the finite-difference estimator, and all omitted endpoint, corner, inter-box, and tail terms.

The five-point formula in Appendix \ref{app:five-point} gives a deterministic fourth-derivative certificate once a uniform sixth-derivative bound is known.  The missing analytic work is therefore to prove such a bound on the relevant source domain and to propagate it through the endpoint decomposition.  With a two-sided estimate, the inequalities
\[
  M_G+\widehat R_{\mathrm{end}}-\Delta_{\mathrm{end}}>0
  \quad\text{or}\quad
  M_G+\widehat R_{\mathrm{end}}+\Delta_{\mathrm{end}}<0
\]
certify, respectively, persistence or failure of the corrected finite margin.  A one-sided lower bound can certify positivity when \(M_G-U>0\), but it cannot certify a negative obstruction.
""",
    "M1": r"""
Finite reflection positivity is only one component of the Osterwalder--Schrader reconstruction problem.  A continuum reconstruction step would have to construct Schwinger functions on a separating Wilson algebra and verify the full set of hypotheses needed to obtain a Hilbert space, a vacuum vector, and Euclidean time translations.  Besides reflection positivity, this includes the relevant Euclidean covariance, regularity, symmetry, tightness or compactness of the continuum limit, and nontriviality of the resulting theory.

The finite Route A block is useful because any proposed continuum theory must be compatible with such finite reflected Gram tests.  It is not itself a continuum construction.  A successful M1 result would specify the topology in which
\[
  a_k\to0,\qquad L_ka_k\to\infty,\qquad T_ka_k\to\infty
\]
and show how the regulated Wilson observables used here embed into the limiting observable algebra.  Without that construction, the paper should speak only about finite-cutoff reflected Wilson blocks and necessary finite conditions.
""",
    "M2": r"""
After OS reconstruction, a mass-gap claim is a statement about the spectrum of the Hamiltonian \(H_{\mathrm{YM}}\) in the reconstructed physical Hilbert space.  The required estimate has the form
\[
  \operatorname{Spec}(H_{\mathrm{YM}})\cap(0,\Delta)=\varnothing
\]
for some \(\Delta>0\), with the vacuum sector separated from the first non-vacuum excitation created by gauge-invariant observables.  Such a statement must be proved in the same continuum theory supplied by M1.

The finite Schur--Feshbach block does not by itself give this spectral estimate.  Its role is more local: it supplies a controlled reflected-Gram obstruction or certificate that any proposed Euclidean construction must respect.  A later gap argument would need a same-theory Euclidean decay estimate, transfer-matrix bound, or Hamiltonian lower bound that does not assume exponential clustering or spectral isolation at the outset.  Any argument that uses the mass gap to justify the endpoint or collar estimates would be circular and should remain outside the claim boundary of this paper.
""",
}

FORBIDDEN_MANUSCRIPT_TERMS = (
    "pipeline",
    "workflow",
    "TODO",
    "todo",
    "result-elaboration",
    "implementation packet",
)


def module_key(title: str) -> str:
    match = re.match(r"\s*([A-Z]\d+)", title)
    if not match:
        raise ValueError(f"cannot identify open-module key from title {title!r}")
    return match.group(1)


def strip_openmodule_bodies(text: str) -> str:
    return OPENMODULE_RE.sub(lambda m: rf"\begin{{openmodule}}{{{m.group(1)}}}__OPENMODULE_BODY__\end{{openmodule}}", text)


def assert_only_openmodules_changed(source: str, generated: str) -> None:
    if strip_openmodule_bodies(source) != strip_openmodule_bodies(generated):
        raise ValueError("narrative extension changed text outside openmodule environments")


def assert_no_pipeline_discourse(text: str) -> None:
    lowered = text.lower()
    for term in FORBIDDEN_MANUSCRIPT_TERMS:
        if term.lower() in lowered:
            raise ValueError(f"forbidden manuscript discourse term found: {term}")


def assert_no_tex_control_corruption(text: str) -> None:
    controls = [
        (idx, ord(ch))
        for idx, ch in enumerate(text)
        if ord(ch) < 32 and ch not in "\n\r\t"
    ]
    if controls:
        sample = ", ".join(f"{idx}:{code}" for idx, code in controls[:8])
        raise ValueError(f"generated TeX contains forbidden control characters: {sample}")


def enrich(source: str) -> str:
    seen: set[str] = set()

    def repl(match: re.Match[str]) -> str:
        title = match.group(1)
        key = module_key(title)
        if key not in NARRATIVE_MODULES:
            raise ValueError(f"missing narrative module for {key}")
        seen.add(key)
        body = NARRATIVE_MODULES[key].strip()
        return f"\\begin{{openmodule}}{{{title}}}\n{body}\n\\end{{openmodule}}"

    generated = OPENMODULE_RE.sub(repl, source)
    missing = sorted(set(NARRATIVE_MODULES) - seen)
    if missing:
        raise ValueError(f"source did not contain open modules: {', '.join(missing)}")
    assert_only_openmodules_changed(source, generated)
    assert_no_pipeline_discourse(generated)
    assert_no_tex_control_corruption(generated)
    return generated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    parser.add_argument("--output", type=Path, default=OUT_DIR / "finite_wilson_os_routeA_SU2_narrative_enriched.tex")
    args = parser.parse_args()

    source_path = args.draft.expanduser().resolve()
    output_path = args.output.expanduser().resolve()
    source = source_path.read_text(encoding="utf-8")
    generated = enrich(source)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generated, encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
