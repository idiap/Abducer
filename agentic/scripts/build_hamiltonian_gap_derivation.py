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

"""Generate the mathematical derivation behind the Hamiltonian gap route."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, rel, stable_id, utc_now, write_json


PACKET = ROOT / "agentic/reports/reasoning_monitor/latest.json"
OUT_JSON = ROOT / "agentic/reports/hamiltonian_gap_derivation/latest.json"
OUT_MD = ROOT / "agentic/reports/hamiltonian_gap_derivation/latest.md"
YANG_MILLS_TARGET = "yang-mills-existence-and-mass-gap-target"
ROUTE_FAMILY = "Hamiltonian spectral-gap route"


def hamiltonian_routes(packet: dict[str, Any]) -> list[dict[str, Any]]:
    routes = [
        route
        for route in packet.get("candidate_routes", [])
        if route.get("route_blueprint", {}).get("route_family") == ROUTE_FAMILY
    ]
    return sorted(routes, key=lambda route: (route.get("route_disposition") != "revision_loop", route.get("priority", 999)))


def route_obligations(route: dict[str, Any]) -> list[str]:
    return [
        clean_text(row.get("requirement", ""))
        for row in route.get("obligations", [])
        if isinstance(row, dict) and clean_text(row.get("requirement", ""))
    ]


def build_derivation(route: dict[str, Any]) -> dict[str, Any]:
    candidate_id = route["candidate_id"]
    return {
        "derivation_id": stable_id("hamiltonian-gap-derivation", candidate_id),
        "candidate_id": candidate_id,
        "route_family": ROUTE_FAMILY,
        "route_disposition": route.get("route_disposition", ""),
        "creative_operation": route.get("creative_operation", ""),
        "route_text": route.get("proposed_transformation", ""),
        "source_witness": route.get("source_witness", ""),
        "mathematical_subclaim": (
            "Given a reconstructed Wightman/OS Yang-Mills theory with Hilbert space H_YM, vacuum Omega, "
            "strongly continuous time translations U(t), and Hamiltonian H satisfying U(t)=exp(-itH), prove "
            "that there is Delta>0 with spec(H restricted to Omega^perp) subset [Delta,infty)."
        ),
        "symbols": {
            "H_YM": "physical Hilbert space produced by OS/Wightman reconstruction",
            "Omega": "vacuum vector, normalized and invariant under time translations",
            "U(t)": "strongly continuous unitary time-translation group",
            "H": "positive self-adjoint Hamiltonian, the generator of U(t)",
            "P0": "orthogonal projection onto the vacuum sector C Omega",
            "Pperp": "I-P0, the projection onto the vacuum-orthogonal excitation sector",
            "E_H(B)": "spectral projection of H for Borel set B",
            "Delta": "strictly positive spectral-gap constant",
        },
        "assumptions": [
            {
                "id": "A1",
                "name": "OS/Wightman reconstruction",
                "formula": "OS-positive Schwinger data reconstructs (H_YM, Omega, U(t), fields).",
                "source_kb": "st.thm.os-reconstruction",
                "status": "route assumption, not discharged here",
            },
            {
                "id": "A2",
                "name": "Hamiltonian generation",
                "formula": "U(t) is strongly continuous and U(t)=e^{-itH} for a self-adjoint H.",
                "source_kb": "KB/stone-one-parameter-unitary-groups.kb.md::st.app.schrodinger-time-evolution",
                "status": "functional-analytic bridge",
            },
            {
                "id": "A3",
                "name": "Positive energy and vacuum",
                "formula": "H >= 0, H Omega = 0, and P0 projects onto the vacuum sector.",
                "source_kb": "st.def.wightman-qft, st.def.mass-gap",
                "status": "axiomatic target condition",
            },
            {
                "id": "A4",
                "name": "Nontrivial excitation sector",
                "formula": "Pperp H_YM != {0}; gauge-invariant observables create non-vacuum states.",
                "source_kb": "st.prob.yang-mills-existence-mass-gap",
                "status": "essential nontriviality obligation",
            },
            {
                "id": "A5",
                "name": "Spectral lower bound",
                "formula": "there exists Delta>0 such that E_H((0,Delta))Pperp = 0.",
                "source_kb": "st.def.mass-gap-in-hamiltonian-wightman-terms",
                "status": "the hard lemma to prove",
            },
        ],
        "derivation_steps": [
            {
                "step": 1,
                "title": "Construct the Hamiltonian object",
                "derivation": (
                    "From OS/Wightman reconstruction obtain a Hilbert space H_YM, vacuum Omega, and time translations U(t). "
                    "By Stone's theorem, strong continuity of U(t) yields a self-adjoint generator H with U(t)=exp(-itH)."
                ),
                "formula": r"U(t)=e^{-itH},\qquad H=H^*,\qquad H\ge 0.",
                "equation_context": {
                    "definitions": [
                        "H_YM is the Hilbert space reconstructed from OS-positive continuum Schwinger functions.",
                        "U(t) is the strongly continuous unitary group implementing real-time translations on H_YM.",
                        "H is the self-adjoint Stone generator of U(t), with positive energy imposed by the Wightman/OS target axioms.",
                    ],
                    "assumptions_used": ["A1", "A2", "A3"],
                    "valid_when": [
                        "The Schwinger data have already passed to the continuum and satisfy OS positivity strongly enough for reconstruction.",
                        "Time translations are represented by a strongly continuous one-parameter unitary group on the reconstructed Hilbert space.",
                        "The positive-energy axiom is part of the reconstructed Yang-Mills target, not borrowed from a cutoff transfer matrix alone.",
                    ],
                },
                "open_obligation": "Show this H is obtained after continuum/OS reconstruction, not only at fixed lattice cutoff.",
            },
            {
                "step": 2,
                "title": "Separate vacuum and excitations",
                "derivation": (
                    "Normalize the invariant vacuum Omega and set P0=|Omega><Omega|, or the projection onto the full vacuum sector if "
                    "vacuum uniqueness is not yet known. The excitation space is Pperp H_YM=(I-P0)H_YM."
                ),
                "formula": r"P_0=\lvert\Omega\rangle\langle\Omega\rvert,\qquad P_\perp=I-P_0,\qquad H\Omega=0.",
                "equation_context": {
                    "definitions": [
                        "Omega is the normalized invariant vacuum vector in H_YM.",
                        "P0 is the orthogonal projection onto C Omega when the vacuum is unique; otherwise it must be replaced by the projection onto the full zero-energy vacuum sector.",
                        "Pperp is I-P0, the vacuum-orthogonal excitation projection.",
                    ],
                    "assumptions_used": ["A1", "A3", "A4"],
                    "valid_when": [
                        "The vacuum sector has been identified inside the reconstructed continuum theory.",
                        "Either vacuum uniqueness is proved, or the formula is read with P0 as the full vacuum-sector projection.",
                        "H Omega = 0 follows from time-translation invariance of the reconstructed vacuum.",
                    ],
                },
                "open_obligation": "Prove vacuum uniqueness or explicitly work with the whole zero-energy vacuum sector.",
            },
            {
                "step": 3,
                "title": "State the spectral-gap lemma",
                "derivation": (
                    "The Hamiltonian mass-gap claim is the spectral exclusion of low positive energies. In projection form, no "
                    "vacuum-orthogonal state can have spectral support in (0,Delta)."
                ),
                "formula": r"E_H((0,\Delta))P_\perp=0\quad\Longleftrightarrow\quad \operatorname{spec}(H|_{P_\perp\mathcal H_{\mathrm{YM}}})\subset[\Delta,\infty).",
                "equation_context": {
                    "definitions": [
                        "E_H(B) is the spectral projection of the self-adjoint Hamiltonian H for the Borel set B.",
                        "Delta is a fixed positive number, independent of removed cutoffs, proposed as the mass-gap lower bound.",
                        "H restricted to Pperp H_YM means the part of H acting on the invariant vacuum-orthogonal excitation sector.",
                    ],
                    "assumptions_used": ["A2", "A3", "A5"],
                    "valid_when": [
                        "Pperp commutes with H, as it does when P0 projects onto the H-invariant zero-energy vacuum sector.",
                        "The spectral theorem applies to H and the projection statement is made on the reconstructed continuum Hilbert space.",
                        "Delta is strictly positive and the interval (0, Delta) is being excluded only away from the vacuum sector.",
                    ],
                },
                "open_obligation": "Derive this exclusion from constructive/RG/correlator input rather than assuming it.",
            },
            {
                "step": 4,
                "title": "Convert spectral exclusion to an energy inequality",
                "derivation": (
                    "By the spectral theorem, if spectral support on Pperp H_YM lies in [Delta,infty), then every vector psi in the "
                    "quadratic-form domain and orthogonal to the vacuum has energy at least Delta times its norm squared."
                ),
                "formula": r"\psi\perp\Omega \Longrightarrow \langle\psi,H\psi\rangle=\int_{[\Delta,\infty)}\lambda\,d\mu_\psi(\lambda)\ge\Delta\|\psi\|^2.",
                "equation_context": {
                    "definitions": [
                        "psi is a vector in the quadratic-form domain of H and orthogonal to the vacuum sector.",
                        "mu_psi(B)=<psi,E_H(B)psi> is the spectral measure of H associated with psi.",
                        "The integral is the spectral-theorem expression for the Hamiltonian quadratic form on psi.",
                    ],
                    "assumptions_used": ["A2", "A3", "A5"],
                    "valid_when": [
                        "The low-energy spectral exclusion E_H((0, Delta))Pperp=0 has been established.",
                        "psi lies in Pperp H_YM and in the form domain required for <psi,H psi> to be finite.",
                        "The support of mu_psi is contained in [Delta, infinity) after removal of the vacuum component.",
                    ],
                },
                "open_obligation": "Identify a dense class of physical gauge-invariant excitation states to which this estimate applies.",
            },
            {
                "step": 5,
                "title": "Convert the same gap to Euclidean decay",
                "derivation": (
                    "For A with <Omega,A Omega>=0, the Euclidean two-point function has spectral representation. The lower spectral "
                    "support gives exponential decay with rate at least Delta."
                ),
                "formula": r"C_A(t)=\langle A\Omega,e^{-tH}A\Omega\rangle=\int_{[\Delta,\infty)}e^{-t\lambda}\,d\mu_A(\lambda)\le e^{-\Delta t}\|A\Omega\|^2.",
                "equation_context": {
                    "definitions": [
                        "A is a reconstructed gauge-invariant observable, vacuum-subtracted so that <Omega,A Omega>=0.",
                        "C_A(t) is the Euclidean time two-point function produced by OS reconstruction.",
                        "mu_A(B)=<A Omega,E_H(B)A Omega> is the spectral measure of the excitation A Omega.",
                    ],
                    "assumptions_used": ["A1", "A2", "A3", "A5"],
                    "valid_when": [
                        "A Omega belongs to the vacuum-orthogonal sector and to the domain needed for the Euclidean semigroup pairing.",
                        "The OS/Wightman reconstruction identifies Euclidean time translation with the semigroup exp(-tH) for t >= 0.",
                        "The spectral support of A Omega lies in [Delta, infinity), so the exponential bound follows uniformly in t >= 0.",
                    ],
                },
                "open_obligation": "Specify gauge-invariant observables A and show their reconstructed states control the physical spectrum.",
            },
            {
                "step": 6,
                "title": "Use decay-to-gap only with a density hypothesis",
                "derivation": (
                    "Conversely, exponential decay of a sufficiently rich family of vacuum-subtracted observables can imply spectral "
                    "support above Delta only if the created states are dense in the excitation sector."
                ),
                "formula": r"\overline{\{(A-\langle\Omega,A\Omega\rangle)\Omega:A\in\mathcal A_{\mathrm{ginv}}\}}=P_\perp\mathcal H_{\mathrm{YM}}.",
                "equation_context": {
                    "definitions": [
                        "A_ginv is the reconstructed algebra or dense test family of gauge-invariant observables.",
                        "The bar denotes Hilbert-space closure in H_YM.",
                        "(A-<Omega,A Omega>)Omega is the vacuum-subtracted excitation created by A.",
                    ],
                    "assumptions_used": ["A1", "A4"],
                    "valid_when": [
                        "The observable family A_ginv is part of the same reconstructed continuum Yang-Mills theory.",
                        "Gauge-invariant observables are rich enough to generate the physical vacuum-orthogonal excitation sector.",
                        "Null vectors from OS reconstruction have already been quotiented out, so closure is taken in the physical Hilbert space.",
                    ],
                },
                "open_obligation": "Prove the gauge-invariant observable family is spectrally determining after reconstruction.",
            },
            {
                "step": 7,
                "title": "Attach continuum compatibility",
                "derivation": (
                    "For lattice/regulated approximants H_a, a bound inf spec(H_a|Pperp_a)>=Delta_a is useful only if liminf_{a->0}Delta_a>0 "
                    "and the Hilbert spaces, observables, and vacuum sectors converge to the reconstructed continuum theory."
                ),
                "formula": r"\inf\sigma(H_a|_{P_{\perp,a}})\ge\Delta_a,\quad \liminf_{a\to0}\Delta_a\ge\Delta>0.",
                "equation_context": {
                    "definitions": [
                        "a is the ultraviolet cutoff or lattice spacing parameter being removed.",
                        "H_a and Pperp,a are the regulated Hamiltonian and excitation projection before continuum passage.",
                        "Delta_a is the regulated gap lower bound, and Delta is the positive lower bound surviving the limit.",
                    ],
                    "assumptions_used": ["A1", "A4", "A5"],
                    "valid_when": [
                        "The regulated Hilbert spaces, observables, vacuum sectors, and Hamiltonians converge to the same OS-reconstructed continuum object.",
                        "The spectral or Euclidean decay estimate is uniform in the cutoff and does not deteriorate to zero as a -> 0.",
                        "The limiting excitation sector remains nontrivial and interacting, so the bound is not for an empty or Gaussian surrogate.",
                    ],
                },
                "open_obligation": "Prevent the lattice gap from collapsing in the continuum limit.",
            },
        ],
        "candidate_derivation": (
            "If A1-A4 construct the physical continuum theory and A5 is proved, then the target subclaim follows: "
            "Pperp H_YM is the non-vacuum sector and the spectral theorem gives inf spec(H|Pperp H_YM)>=Delta. "
            "Equivalently, H has no spectrum in (0,Delta) away from the vacuum, so the reconstructed Yang-Mills theory has a Hamiltonian mass gap."
        ),
        "what_would_count_as_progress": [
            {
                "claim": "A precise construction of H_YM, Omega, U(t), and H from OS-positive continuum Schwinger functions.",
                "why": (
                    "This is the mathematical bridge from Euclidean functional data to the Hamiltonian problem. Without reconstructed "
                    "objects H_YM, Omega, U(t), and a self-adjoint generator H, the phrase 'spectral gap' is only a desired notation, "
                    "not a claim about the target continuum Yang-Mills theory."
                ),
            },
            {
                "claim": "A proof that gauge-invariant observables create a dense excitation sector.",
                "why": (
                    "A gap detected by a narrow observable family could miss hidden low-energy states. Density is what lets decay "
                    "estimates or spectral bounds for gauge-invariant observables control the whole vacuum-orthogonal physical "
                    "sector P_perp H_YM."
                ),
            },
            {
                "claim": "A cutoff-uniform lower spectral bound or equivalent cutoff-uniform Euclidean decay estimate.",
                "why": (
                    "The Clay target is a continuum problem, so a fixed-regulator lattice gap is not enough: it can collapse when the "
                    "cutoff is removed. Uniformity is the mechanism that transfers a regulated spectral or decay estimate into a "
                    "positive lower bound for the reconstructed continuum Hamiltonian."
                ),
            },
            {
                "claim": "A nontriviality witness showing the excitation sector belongs to an interacting Yang-Mills theory.",
                "why": (
                    "The mass-gap statement must be about the nontrivial interacting gauge theory, not a free, Gaussian, empty, or "
                    "mismatched limit. A nontriviality witness ties the excitation sector carrying the gap to the same continuum "
                    "Yang-Mills object produced by the construction."
                ),
            },
        ],
        "what_does_not_count": [
            "A spectral gap for a fixed lattice spacing without continuum stability.",
            "A heuristic or numerical lower bound not expressed as a spectral theorem statement.",
            "A Hamiltonian defined before OS/Wightman reconstruction of the continuum target.",
            "Decay of observables that do not determine the vacuum-orthogonal spectrum.",
        ],
        "source_obligations": route_obligations(route),
    }


def build_report() -> dict[str, Any]:
    packet = load_json_object(PACKET)
    routes = hamiltonian_routes(packet)
    target_route = next((route for route in routes if route.get("creative_operation") == "theorem_weakening"), routes[0] if routes else None)
    derivations = [build_derivation(target_route)] if target_route else []
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": packet["target"]["target_id"],
        "report_mode": "Hamiltonian spectral-gap mathematical derivation",
        "scope": (
            "This derives the exact spectral subclaim that the Hamiltonian route must prove. It does not prove Yang-Mills; "
            "it exposes the mathematical load-bearing lemmas and the spectral-theorem consequences."
        ),
        "selected_route_count": len(derivations),
        "available_hamiltonian_route_ids": [route["candidate_id"] for route in routes],
        "derivations": derivations,
        "source_artifacts": [
            "agentic/reports/reasoning_monitor/latest.json",
            "KB/yang-mills-existence-and-mass-gap.kb.md",
            "KB/stone-one-parameter-unitary-groups.kb.md",
        ],
    }


def render_derivation(item: dict[str, Any]) -> list[str]:
    lines = [
        f"## Route `{item['candidate_id']}`",
        "",
        f"- Route family: `{item['route_family']}`",
        f"- Disposition: `{item['route_disposition']}`",
        f"- Operation: `{item['creative_operation']}`",
        f"- Route text: {item['route_text']}",
        "",
        "### Mathematical Subclaim",
        "",
        item["mathematical_subclaim"],
        "",
        "### Symbols",
        "",
    ]
    for symbol, meaning in item["symbols"].items():
        lines.append(f"- `${symbol}$: {meaning}")
    lines.extend(["", "### Assumptions", ""])
    for assumption in item["assumptions"]:
        lines.append(f"- `{assumption['id']}` **{assumption['name']}**: {assumption['formula']} ({assumption['status']}; source `{assumption['source_kb']}`)")
    lines.extend(["", "### Derivation", ""])
    for step in item["derivation_steps"]:
        lines.append(f"{step['step']}. **{step['title']}**")
        lines.append("")
        lines.append(step["derivation"])
        lines.append("")
        context = step.get("equation_context", {})
        definitions = context.get("definitions", [])
        assumptions_used = context.get("assumptions_used", [])
        valid_when = context.get("valid_when", [])
        if definitions or assumptions_used or valid_when:
            lines.append("Equation context:")
            lines.append("")
            for definition in definitions:
                lines.append(f"- Definition: {definition}")
            if assumptions_used:
                lines.append(f"- Assumptions used: {', '.join(assumptions_used)}")
            for condition in valid_when:
                lines.append(f"- Valid when: {condition}")
            lines.append("")
        lines.append("```math")
        lines.append(step["formula"])
        lines.append("```")
        lines.append("")
        lines.append(f"Open obligation: {step['open_obligation']}")
        lines.append("")
    lines.extend(["### Candidate Derivation", "", item["candidate_derivation"], ""])
    lines.extend(["### What Would Count As Progress", ""])
    for progress in item["what_would_count_as_progress"]:
        if isinstance(progress, dict):
            lines.append(f"- {progress['claim']}")
            lines.append(f"  Why: {progress['why']}")
        else:
            lines.append(f"- {progress}")
    lines.extend(["", "### What Does Not Count", ""])
    lines.extend(f"- {value}" for value in item["what_does_not_count"])
    lines.append("")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Hamiltonian Spectral-Gap Derivation",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Mode: {report['report_mode']}",
        "",
        report["scope"],
        "",
    ]
    for item in report["derivations"]:
        lines.extend(render_derivation(item))
    return "\n".join(lines)


def main() -> int:
    report = build_report()
    write_json(OUT_JSON, report)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
