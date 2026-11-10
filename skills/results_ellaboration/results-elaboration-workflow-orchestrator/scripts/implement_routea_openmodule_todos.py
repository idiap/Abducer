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
"""Implement Route A open-module TODOs as manuscript-integrated module packets."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "agentic/reports/results_ellaboration/a-finite-schur-feshbach-test-for-reflected-wilson-blocks-an-explicit-four-dimens"


MODULE_PACKETS: dict[str, dict[str, Any]] = {
    "G1": {
        "status": "implemented_as_geometric_construction_packet",
        "title": "geometric family",
        "claim": "This module is not yet a theorem. It is implemented as a precise construction target for a cutoff-indexed geometric collar.",
        "target": r"construct paths \(\gamma_{+,k}(\delta),\gamma_{-,k}(\delta),\gamma_{0,k}(\delta)\) with locked reflected boundary footprint",
        "calculations": [
            r"Choose integers \(r_k,s_k,h_k,m_k(\delta)\) with \(a_kr_k\to R\), \(a_ks_k\to S\), \(a_kh_k\to H\), and \(a_km_k(\delta)\to\delta\).",
            r"Write each path as an ordered edge list using \(A_k\), \(B_k=A_k+r_ke_1\), transverse offsets \(\pm m_k(\delta)e_2\), and the temporal offset \(h_ke_0\).",
            r"Check every edge has time coordinate \(\ge1\), or move the base time from \(1\) to \(1+h_k\) and record the shift.",
            r"Compute the common reflected boundary footprint and prove it is independent of the collar sign \(\pm\delta\).",
            r"Prove \(\rho\gamma_{+,k}(\delta)=\gamma_{-,k}(\delta)\) and \(\rho\gamma_{0,k}(\delta)=\gamma_{0,k}(\delta)\).",
        ],
        "promotion": "Promote G1 only when the edge-list construction satisfies positive-time support, footprint locking, reflection pairing, and the stated joint scaling.",
        "demotion": "Keep G1 open if the collar collapse changes the footprint, exits the positive algebra, or depends on an unstated order of limits.",
    },
    "G2": {
        "status": "implemented_as_normalization_certificate_packet",
        "title": "renormalized same-theory normalization",
        "claim": "This module is implemented as a normalization audit and theorem target, not as a completed renormalization proof.",
        "target": r"prove that all renormalized geometric-collar normalizations are same-theory positive operations",
        "calculations": [
            r"List every normalization factor for \(N_{k,\delta}\): perimeter, cusp, boundary, endpoint, and overlap factors.",
            r"Classify each factor as one-body \(a_i\overline a_j\), block congruence, pair-dependent \(B_{ij}\), or positive-kernel candidate.",
            r"For one-body factors define \(D_{k,\delta}\) and verify \(q_{k,\delta}=D_{k,\delta}N_{k,\delta}D_{k,\delta}^*\).",
            r"For pair-dependent factors test whether \(B^{-1}\) is positive definite or can be represented as a Schur product with a positive kernel.",
            r"Record any factor that fails these tests as a demotion blocker for the geometric-collar application.",
        ],
        "promotion": "Promote G2 only when every removed factor is realized by congruence, direct normalized observables, or a proved positive-kernel factorization.",
        "demotion": "Demote the geometric route if it needs pair-dependent entrywise division without a positivity certificate.",
    },
    "G3": {
        "status": "implemented_as_geometric_coefficient_packet",
        "title": "geometric coefficient extraction",
        "claim": "This module is implemented as the exact coefficient-extraction workload for the geometric collar; no geometric H,K theorem is claimed yet.",
        "target": r"derive \(q_{k,\delta}=\one\one^T+\delta H_k+\delta^2K_k+R_{k,\delta}\) from the geometric collar",
        "calculations": [
            r"Express every entry of the normalized geometric block \(q_{k,\delta}(i,j)\) as a same-theory Wilson expectation.",
            r"Choose whether to expand entries directly or expand \(\log q_{k,\delta}(i,j)\), then state the conversion to \(H_k,K_k\).",
            r"Compute first variations in \(\delta\) and isolate additive one-body terms killed by \(P\).",
            r"Compute second variations and separate genuine \(K_k\) terms from Schur correction terms.",
            r"Prove \(\sup_k\|R_{k,\delta}\|/\delta^2\to0\) in the declared \(a_k,\delta\) regime.",
        ],
        "promotion": r"Promote G3 only when \(H_k,K_k\) and the operator-norm remainder are derived from the same normalized geometric block.",
        "demotion": r"Do not promote the source-amplitude \(H,K\) calculation as a geometric-collar coefficient theorem.",
    },
    "G4": {
        "status": "implemented_as_non_degeneracy_program",
        "title": "uniform nondegeneracy",
        "claim": "This module is implemented as a lower-bound programme for the reduced margins, not as a proved continuum lower bound.",
        "target": r"prove or certify lower bounds for the renormalized analogues of \(\sigma_k\) and \(\tau_k\)",
        "calculations": [
            r"Define the renormalized \(\sigma_k(\delta)\) and \(\tau_k(\delta)\) after G2 normalization.",
            r"Separate positivity from strict positivity: reflection positivity gives \(\ge0\), not a lower bound.",
            r"Identify whether lower bounds come from symmetry, transfer-matrix estimates, character expansion, or certified finite computation.",
            r"Propagate certified intervals into \(2\sigma_k\) and \(2\tau_k/3\).",
            r"State the limiting margin condition needed before revising the abstract toward geometric-collar success.",
        ],
        "promotion": "Promote G4 only when lower bounds survive the chosen cutoff trajectory.",
        "demotion": r"Keep strict-margin claims finite if \(\sigma_k\) or \(\tau_k\) may vanish as \(k\to\infty\).",
    },
    "E1": {
        "status": "implemented_as_endpoint_derivation_packet",
        "title": "endpoint regulator derivation",
        "claim": "This module is implemented as a same-regulator endpoint derivation target, not as an endpoint theorem.",
        "target": r"derive the endpoint estimator and color/incidence factors from the SU(2) heat-kernel regulator",
        "calculations": [
            r"Define endpoint boxes from the G1 geometric paths, including which plaquettes and links belong to each box.",
            r"Define source variables and singlet projections in the fundamental \(SU(2)\) representation.",
            r"Derive \(C_{\mathrm{col}}\) from the heat-kernel group integral with stated trace normalization.",
            r"Derive the incidence weights in \(2\widehat\kappa^{12}_{4,v}-4\widehat\kappa^{13}_{4,v}-4\widehat\kappa^{23}_{4,v}\) from path geometry, not by assumption.",
            r"Check diagonal terms vanish only under the unit-diagonal normalization condition.",
        ],
        "promotion": "Promote E1 only when the estimator is derived from the same geometric Wilson family and regulator.",
        "demotion": "Do not infer endpoint signs from an incidence ansatz not tied to the regulated path integral.",
    },
    "E2": {
        "status": "implemented_as_two_sided_error_packet",
        "title": "cumulant and tail bounds",
        "claim": "This module is implemented as the two-sided error architecture needed for endpoint certificates.",
        "target": r"prove \(|R_{\mathrm{end}}-\widehat R_{\mathrm{end}}|\le\Delta_{\mathrm{end}}\)",
        "calculations": [
            r"State the compact source domain for every endpoint logarithm \(\ell_v(s)=\log Z_v(s)\).",
            r"Prove or bound \(\sup|\ell_v^{(6)}(s)|\) to justify the five-point fourth-derivative stencil.",
            r"Bound endpoint, corner, inter-box, and tail terms on both sides.",
            r"Propagate the two-sided error into \(M_G+\widehat R_{\mathrm{end}}\pm\Delta_{\mathrm{end}}\).",
            r"Classify the result as positive certificate, negative certificate, or inconclusive; never use a one-sided lower bound as a negative certificate.",
        ],
        "promotion": "Promote E2 only with a same-regulator two-sided error bound.",
        "demotion": r"A one-sided lower bound can certify positivity when \(M_G-U>0\), but cannot certify an obstruction.",
    },
    "M1": {
        "status": "implemented_as_continuum_reconstruction_handoff",
        "title": "continuum reconstruction",
        "claim": "This module is implemented as a reconstruction handoff checklist; it remains open.",
        "target": r"construct continuum Schwinger functions satisfying the full OS axioms on a separating Wilson algebra",
        "calculations": [
            r"List the OS axioms still missing: Euclidean invariance, symmetry, regularity, clustering/nontriviality as applicable, and reflection positivity for a separating algebra.",
            r"Specify the topology for \(a_k\to0\), \(L_ka_k,T_ka_k\to\infty\).",
            r"State tightness or compactness estimates needed for Wilson-loop distributions.",
            r"Identify how finite geometric-collar blocks embed into the continuum observable algebra.",
            r"Name which result would produce the reconstructed Hilbert space and Hamiltonian.",
        ],
        "promotion": "Promote M1 only with an actual continuum construction or a theorem importing one in the same theory.",
        "demotion": "Finite reflection positivity must remain a necessary finite condition, not OS reconstruction.",
    },
    "M2": {
        "status": "implemented_as_spectral_gap_handoff",
        "title": "gap estimate",
        "claim": "This module is implemented as a spectral-gap handoff checklist; it remains open.",
        "target": r"derive a same-theory estimate implying no Hamiltonian spectrum in \((0,\Delta)\)",
        "calculations": [
            r"Define the reconstructed Hamiltonian \(H_{\mathrm{YM}}\), vacuum \(\Omega\), and excitation sector.",
            r"State the Euclidean decay, transfer-matrix, or correlation estimate sufficient for a spectral gap.",
            r"Check that the estimate is in the same continuum theory produced by M1.",
            r"Audit every step for circular use of exponential decay, clustering, or mass gap.",
            r"State what observable sector witnesses the first non-vacuum excitation.",
        ],
        "promotion": "Promote M2 only after M1 and a non-circular same-theory spectral estimate.",
        "demotion": "No finite-block or endpoint result may be described as a mass-gap proof.",
    },
}


INSERTION_PREAMBLE = r"""
The following open modules have now been refined into implementation packets.  Each packet separates the calculation to be performed, deterministic checks, promotion criteria, and demotion criteria.  This is a manuscript integration of the expansion pipeline: it makes the next mathematical work explicit while preserving the claim boundary of the finite Route A result.
"""


def expanded_module(module_id: str, original_title: str) -> str:
    packet = MODULE_PACKETS[module_id]
    lines = [
        rf"\begin{{openmodule}}{{{original_title}}}",
        packet["claim"],
        "",
        r"\emph{Target.} " + packet["target"] + ".",
        "",
        r"\emph{Needed calculations.}",
        r"\begin{enumerate}[label=(\alph*)]",
    ]
    for item in packet["calculations"]:
        lines.append(rf"  \item {item}")
    lines += [
        r"\end{enumerate}",
        "",
        r"\emph{Promotion criterion.} " + packet["promotion"],
        "",
        r"\emph{Demotion boundary.} " + packet["demotion"],
        r"\end{openmodule}",
    ]
    return "\n".join(lines)


def integrate_modules(text: str) -> str:
    intro = "The remaining steps are stated here in a form that can be filled without changing the finite result.\n"
    if INSERTION_PREAMBLE.strip() not in text:
        text = text.replace(intro, intro + "\n" + INSERTION_PREAMBLE.strip() + "\n")

    def repl(match: re.Match[str]) -> str:
        title = match.group(1)
        module_id = title.split(":", 1)[0].strip()
        if module_id not in MODULE_PACKETS:
            return match.group(0)
        return expanded_module(module_id, title)

    return re.sub(r"\\begin\{openmodule\}\{([^{}]+)\}.*?\\end\{openmodule\}", repl, text, flags=re.S)


def assert_no_tex_control_corruption(text: str) -> None:
    """Reject generated TeX containing non-newline/tab control characters or tabbed macros."""
    controls = [
        (idx, ord(ch))
        for idx, ch in enumerate(text)
        if ord(ch) < 32 and ch not in "\n\r\t"
    ]
    if controls:
        sample = ", ".join(f"{idx}:{code}" for idx, code in controls[:8])
        raise ValueError(f"generated TeX contains forbidden control characters: {sample}")

    suspicious_tabs = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if "\t" in line and ("au_" in line or "o\\infty" in line or "sigma" in line):
            suspicious_tabs.append(lineno)
    if suspicious_tabs:
        raise ValueError(
            "generated TeX contains tab-corrupted math macros near lines "
            + ", ".join(map(str, suspicious_tabs[:8]))
        )


def implementation_status() -> dict[str, Any]:
    items = [
        {
            "todo_id": "todo-001",
            "status": "completed",
            "artifact": "routea_three_hairpin_certificate.json",
            "claim_boundary": "finite source-collision algebra only",
        },
        {
            "todo_id": "todo-002",
            "status": "completed",
            "artifact": "compiled integrated manuscript and label/reference audit",
            "claim_boundary": "manuscript integrity only",
        },
    ]
    for offset, module_id in enumerate(["G1", "G2", "G3", "G4", "E1", "E2", "M1", "M2"], start=3):
        packet = MODULE_PACKETS[module_id]
        items.append(
            {
                "todo_id": f"todo-{offset:03d}",
                "module_id": module_id,
                "status": packet["status"],
                "artifact": f"expanded open module packet for {module_id}",
                "claim_boundary": packet["claim"],
                "promotion": packet["promotion"],
                "demotion": packet["demotion"],
            }
        )
    return {
        "schema": "abducer.results_elaboration.routea_openmodule_implementation.v1",
        "items": items,
    }


def render_status_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Route A Open-Module TODO Implementation Status",
        "",
        "The deterministic TODOs are completed as executable certificates and manuscript audits.  The mathematical open modules are implemented as paper-integrated proof/calculation packets with promotion and demotion boundaries; they are not falsely promoted to theorems.",
        "",
    ]
    for item in payload["items"]:
        lines += [
            f"## {item['todo_id']}",
            "",
            f"- Status: `{item['status']}`",
            f"- Artifact: {item['artifact']}",
            f"- Claim boundary: {item['claim_boundary']}",
        ]
        if "module_id" in item:
            lines += [
                f"- Module: `{item['module_id']}`",
                f"- Promotion: {item['promotion']}",
                f"- Demotion: {item['demotion']}",
            ]
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    args = parser.parse_args()
    draft = args.draft.expanduser().resolve()
    text = draft.read_text(encoding="utf-8")
    expanded = integrate_modules(text)
    assert_no_tex_control_corruption(expanded)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = OUT_DIR / "finite_wilson_os_routeA_SU2_all_todos_integrated.tex"
    status_json_path = OUT_DIR / "routea_openmodule_todo_implementation_status.json"
    status_md_path = OUT_DIR / "routea_openmodule_todo_implementation_status.md"
    tex_path.write_text(expanded, encoding="utf-8")
    status = implementation_status()
    status_json_path.write_text(json.dumps(status, indent=2), encoding="utf-8")
    status_md_path.write_text(render_status_markdown(status), encoding="utf-8")
    print(f"Wrote {tex_path}")
    print(f"Wrote {status_json_path}")
    print(f"Wrote {status_md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
