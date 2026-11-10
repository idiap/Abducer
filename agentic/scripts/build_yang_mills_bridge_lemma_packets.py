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

"""Build explicit bridge-lemma packets for the next Yang-Mills long-horizon step."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, load_json_object, rel, stable_id, utc_now, write_json


LONG_HORIZON = ROOT / "agentic/reports/long_horizon/latest.json"
MONITOR = ROOT / "agentic/reports/reasoning_monitor/latest.json"
OUT_JSON = ROOT / "agentic/reports/yang_mills_bridge_lemma_packets/latest.json"
OUT_MD = ROOT / "agentic/reports/yang_mills_bridge_lemma_packets/latest.md"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"


def route_by_family(packet: dict[str, Any], family: str) -> dict[str, Any]:
    for route in packet.get("candidate_routes", []):
        if route.get("route_blueprint", {}).get("route_family") == family:
            return route
    return {}


def build_packets() -> dict[str, Any]:
    long_horizon = load_json_object(LONG_HORIZON)
    monitor = load_json_object(MONITOR)
    balaban = route_by_family(monitor, "Balaban RG continuum-control route")
    decay = route_by_family(monitor, "Euclidean correlator-decay to spectral-gap route")
    packets = [
        {
            "packet_id": stable_id("ym-bridge-lemma", "rg-to-os-continuum-passage"),
            "title": "RG-to-OS Continuum Passage Bridge Lemma",
            "source_route_id": balaban.get("candidate_id", ""),
            "route_family": "Balaban RG continuum-control route",
            "recursive_role": "turn construction pressure into a same-theory continuum object",
            "lemma_statement": (
                "For compact simple gauge group G on four-dimensional Euclidean space, suppose a directed family of regulated "
                "Yang-Mills measures or Schwinger distributions has Balaban-style multiscale effective-action bounds strong enough "
                "to give tightness/convergence on gauge-invariant observables, and suppose reflection positivity, Euclidean "
                "covariance, gauge invariance, and a non-Gaussian observable witness are preserved uniformly through cutoff removal. "
                "Then a subsequential continuum family of gauge-invariant Schwinger functions S_n exists, is OS-positive, is nontrivial, "
                "and reconstructs a candidate physical Hilbert space H_YM with vacuum Omega and time-translation semigroup."
            ),
            "source_objects": [
                "regulated Yang-Mills measures dmu_{a,L} or Schwinger distributions S_n^{a,L}",
                "Balaban effective actions and polymer/small-field estimates across scales",
                "compact simple gauge group G and gauge-invariant observable algebra A_ginv^{a,L}",
            ],
            "target_objects": [
                "continuum gauge-invariant Schwinger functions S_n on R^4",
                "OS-positive reconstruction data for H_YM, Omega, and Euclidean time semigroup",
                "nontrivial observable witness in the same limiting Yang-Mills object",
            ],
            "definitions": [
                "Cutoff removal means a -> 0 and L -> infinity along a directed regulated family.",
                "OS positivity is reflection positivity for the limiting Schwinger functions after quotienting null vectors.",
                "Same-theory invariant means construction, reconstruction, nontriviality, and gap witnesses refer to the same limiting object S_n.",
            ],
            "assumptions": [
                "Uniform multiscale bounds imply tightness or distributional precompactness for gauge-invariant Schwinger functions.",
                "Reflection positivity and Euclidean covariance are stable under the limiting topology used.",
                "There exists a gauge-invariant observable O whose connected limiting cumulant does not vanish in the Gaussian/free pattern.",
            ],
            "equations": [
                {
                    "label": "continuum passage",
                    "display": "S_n^{a,L} -> S_n as a -> 0 and L -> infinity",
                    "latex": r"S_n^{a,L}\Longrightarrow S_n\quad(a\to0,\ L\to\infty)",
                    "valid_when": "The regulated Schwinger functions are uniformly controlled in a topology where OS positivity and Euclidean covariance are closed conditions.",
                },
                {
                    "label": "OS positivity preservation",
                    "display": "sum_i,j c_i conjugate(c_j) S(f_i^theta, f_j) >= 0",
                    "latex": r"\sum_{i,j}\overline{c_i}c_j\,S(\Theta f_i,f_j)\ge 0",
                    "valid_when": "Each regulated object is reflection-positive and the test functions/observable algebra survive the limiting quotient.",
                },
                {
                    "label": "nontriviality witness",
                    "display": "<O_1 ... O_k>_c != 0 in the continuum limit",
                    "latex": r"\langle O_1\cdots O_k\rangle_c\ne0",
                    "valid_when": "The observable O_i are gauge-invariant and belong to the same limiting algebra used for reconstruction.",
                },
            ],
            "proof_obligations": [
                "Name the exact Balaban estimates that yield precompactness rather than only local small-field control.",
                "Prove the limiting topology preserves OS positivity for the gauge-invariant observable sector.",
                "Attach one non-Gaussian gauge-invariant observable witness to rule out triviality.",
                "Record the reconstructed H_YM, Omega, and semigroup as outputs of S_n, not as independent postulates.",
            ],
            "failure_tests": [
                "Reject if the limit exists only at finite volume or fixed ultraviolet cutoff.",
                "Reject if OS positivity is asserted for the regulator but not proved closed in the limiting topology.",
                "Reject if the nontriviality witness comes from a different approximation scheme than S_n.",
            ],
            "contradiction_branches": [
                {
                    "branch_id": stable_id("ym-reductio", "os-positivity-failure"),
                    "strategy": "OS-positivity-failure reductio",
                    "exact_negation": (
                        "There exists a finite reflected test-observable family f_i and coefficients c_i such that the "
                        "continuum reflection form sum_i,j conjugate(c_i)c_j S(Theta f_i,f_j) is strictly negative."
                    ),
                    "contradiction_carrier": "a negative reflection-positivity quadratic form in the limiting gauge-invariant Schwinger functions",
                    "preserved_commitments": [
                        "The regulated approximants are reflection-positive in the same gauge-invariant observable sector.",
                        "The limiting topology is strong enough for the reflection form to be a closed nonnegative cone.",
                        "The limiting Schwinger functions are the same objects used for reconstruction and later gap analysis.",
                    ],
                    "derived_consequence": (
                        "If the negative continuum form exists while all approximating reflection forms are nonnegative and the cone is closed, "
                        "the limit would both belong and not belong to the OS-positive cone."
                    ),
                    "conflict_target": "closedness of reflection positivity under the selected cutoff-removal topology",
                    "proof_obligations": [
                        "Specify the topology on gauge-invariant Schwinger distributions.",
                        "Prove reflection positivity is closed in that topology for the chosen observable algebra.",
                        "Show the negative test family survives the OS null-vector quotient.",
                    ],
                    "failure_modes": [
                        "The limiting topology is too weak to preserve the reflection form.",
                        "The test-observable family changes across the cutoff sequence.",
                        "Gauge fixing or quotienting changes the observable sector.",
                    ],
                    "audit_skill": "contradiction-route-auditor",
                    "learning_if_failed": "Failure would show that the continuum route needs a sharper topology or a different construction of the OS-positive sector before spectral reasoning can be trusted.",
                },
                {
                    "branch_id": stable_id("ym-reductio", "triviality-collapse"),
                    "strategy": "Triviality-collapse reductio",
                    "exact_negation": (
                        "Every continuum subsequential limit of the regulated gauge-invariant Yang-Mills observables is Gaussian/free or "
                        "has vanishing connected cumulants for the nontriviality witness family."
                    ),
                    "contradiction_carrier": "a connected gauge-invariant cumulant or Wilson-loop observable in the same limiting Schwinger family",
                    "preserved_commitments": [
                        "The nontriviality witness is measured in the same limiting Schwinger functions S_n.",
                        "Connected cumulants are defined after the same cutoff-removal process as OS reconstruction.",
                        "Gauge invariance and Euclidean covariance remain active commitments.",
                    ],
                    "derived_consequence": (
                        "The assumed trivial collapse forces the selected connected cumulant to vanish, while the same-theory witness requires "
                        "a nonzero interacting cumulant in that limit."
                    ),
                    "conflict_target": "same-theory non-Gaussian or nonzero connected-cumulant witness",
                    "proof_obligations": [
                        "Select the witness observable family and its normalization.",
                        "Prove the witness belongs to the same continuum object as the OS reconstruction.",
                        "Show the witness distinguishes interacting Yang-Mills from a Gaussian/free limit.",
                    ],
                    "failure_modes": [
                        "The witness comes from a different approximation scheme.",
                        "The cumulant normalization vanishes or diverges in the limit.",
                        "The branch proves only non-Gaussianity at finite cutoff.",
                    ],
                    "audit_skill": "contradiction-route-auditor",
                    "learning_if_failed": "Failure would demote the route to a nontriviality-evidence task rather than allowing the gap analysis to proceed on an empty continuum theory.",
                },
            ],
            "conditional_skill_triggers": [
                {"skill": "prior-art-importer", "trigger": "Exact Balaban theorem statements must be imported or normalized before promotion."},
                {"skill": "review-reasoner-fields-medalist", "trigger": "Stress-test whether the proposed limiting topology is mathematically plausible."},
                {"skill": "kb-contradiction-strategist", "trigger": "Use when OS positivity or nontriviality is better explored through the negated continuum-construction assumption."},
                {"skill": "contradiction-route-auditor", "trigger": "Audit reductio branches before they are allowed to justify proof-queue promotion."},
                {"skill": "expert-handoff", "trigger": "Package the bridge once it has theorem names, assumptions, and one observable witness."},
            ],
            "next_recursive_subgoals": [
                "Search the KB/prior-art cache for the strongest Balaban precompactness or convergence statement.",
                "Choose the limiting topology and state the closure lemma for reflection positivity.",
                "Select a candidate gauge-invariant nontriviality observable.",
            ],
            "promotion_condition": "Promote only when the lemma names the regulated objects, limiting topology, OS-positivity preservation theorem, and nontriviality witness.",
            "same_theory_invariant": "The same Schwinger functions S_n are the sole object from which nontriviality, reconstruction, and any later mass-gap witness must be read.",
        },
        {
            "packet_id": stable_id("ym-bridge-lemma", "decay-to-hamiltonian-gap"),
            "title": "Cutoff-Uniform Decay-to-Hamiltonian-Gap Bridge Lemma",
            "source_route_id": decay.get("candidate_id", ""),
            "route_family": "Euclidean correlator-decay to spectral-gap route",
            "recursive_role": "turn a Euclidean decay witness into a Hamiltonian spectral exclusion",
            "lemma_statement": (
                "Suppose the same OS-positive continuum Yang-Mills Schwinger functions S_n reconstruct H_YM, Omega, H and a gauge-invariant "
                "observable algebra A_ginv. If a spectrally determining vacuum-subtracted family A in A_ginv has connected Euclidean "
                "time correlations bounded by C_A exp(-m t) with m >= m0 > 0 uniformly through cutoff removal, then the reconstructed "
                "Hamiltonian has no vacuum-orthogonal spectrum in (0,m0), hence Spec(H restricted to P_perp H_YM) subset [m0,infinity)."
            ),
            "source_objects": [
                "OS-positive continuum Yang-Mills Schwinger functions S_n from the RG-to-OS bridge",
                "gauge-invariant observable algebra A_ginv and vacuum-subtracted vectors (A-<A>)Omega",
                "cutoff-uniform Euclidean decay estimates for connected two-point functions",
            ],
            "target_objects": [
                "spectral measure mu_A for A Omega under H",
                "dense vacuum-orthogonal sector P_perp H_YM",
                "Hamiltonian spectral exclusion E_H((0,m0))P_perp = 0",
            ],
            "definitions": [
                "Spectrally determining means the closure of vacuum-subtracted gauge-invariant observable vectors is P_perp H_YM.",
                "Cutoff-uniform means the decay rate has a positive lower bound before taking the continuum limit.",
                "P_perp is the projection away from the reconstructed vacuum sector, not a regulator-level excitation space.",
            ],
            "assumptions": [
                "OS reconstruction identifies Euclidean time translation with exp(-tH) on H_YM.",
                "The observable family is dense in the physical vacuum-orthogonal sector after quotienting OS null vectors.",
                "The connected correlation decay rate m satisfies liminf m_{a,L} >= m0 > 0.",
            ],
            "equations": [
                {
                    "label": "spectral representation",
                    "display": "C_A(t) = integral exp(-t lambda) d mu_A(lambda)",
                    "latex": r"C_A(t)=\int_0^\infty e^{-t\lambda}\,d\mu_A(\lambda)",
                    "valid_when": "A Omega is a reconstructed vacuum-orthogonal vector and Euclidean time is represented by exp(-tH).",
                },
                {
                    "label": "uniform decay",
                    "display": "|C_A^{a,L}(t)| <= C_A exp(-m_{a,L} t), liminf m_{a,L} >= m0 > 0",
                    "latex": r"|C_A^{a,L}(t)|\le C_Ae^{-m_{a,L}t},\qquad \liminf_{a\to0,L\to\infty}m_{a,L}\ge m_0>0",
                    "valid_when": "The constants are controlled uniformly for the same observable family that survives reconstruction.",
                },
                {
                    "label": "Hamiltonian gap conclusion",
                    "display": "E_H((0,m0)) P_perp = 0",
                    "latex": r"E_H((0,m_0))P_\perp=0",
                    "valid_when": "The observable family is spectrally determining, so decay support restrictions extend from A Omega vectors to P_perp H_YM.",
                },
            ],
            "proof_obligations": [
                "Specify the gauge-invariant observable family and prove its density in P_perp H_YM.",
                "Prove decay constants stay bounded below through cutoff removal.",
                "Show the spectral measure support implication is valid for the reconstructed continuum Hamiltonian.",
                "Check the nontriviality witness is compatible with the same observable algebra.",
            ],
            "failure_tests": [
                "Reject if the decay is only a strong-coupling or finite-lattice estimate.",
                "Reject if observables do not determine all physical non-vacuum excitations.",
                "Reject if the continuum construction and spectral estimate refer to different limiting objects.",
            ],
            "contradiction_branches": [
                {
                    "branch_id": stable_id("ym-reductio", "no-hamiltonian-gap"),
                    "strategy": "No-gap spectral reductio",
                    "exact_negation": (
                        "For every epsilon > 0 there exists psi_epsilon in P_perp H_YM with ||psi_epsilon|| = 1 and "
                        "<psi_epsilon,H psi_epsilon> < epsilon; equivalently the vacuum-orthogonal spectral support of H meets "
                        "(0,epsilon) for arbitrarily small epsilon."
                    ),
                    "contradiction_carrier": "low-energy vacuum-orthogonal spectral measures or observable-generated approximants in the reconstructed H_YM",
                    "preserved_commitments": [
                        "H, Omega, and P_perp are reconstructed from the same OS-positive continuum Schwinger functions.",
                        "Gauge-invariant vacuum-subtracted observables are dense in P_perp H_YM.",
                        "The Euclidean connected two-point decay bound holds uniformly with rate bounded below by m0 > 0.",
                    ],
                    "derived_consequence": (
                        "The no-gap assumption puts spectral mass arbitrarily close to zero, while a spectrally determining observable family "
                        "with cutoff-uniform e^{-m0 t} decay forces its spectral measures to have no support in (0,m0)."
                    ),
                    "conflict_target": "spectral support exclusion E_H((0,m0))P_perp = 0 obtained from OS reconstruction, density, and uniform Euclidean decay",
                    "proof_obligations": [
                        "Prove the gauge-invariant observable family is dense in the physical vacuum-orthogonal sector.",
                        "Show the low-energy vectors can be approximated by vacuum-subtracted observable vectors.",
                        "Prove the Laplace-transform spectral support lemma for the reconstructed Hamiltonian.",
                        "Transport the cutoff-uniform decay estimate to the continuum without changing the object.",
                    ],
                    "failure_modes": [
                        "The no-gap vectors live outside the observable-generated sector.",
                        "The decay estimate is finite-cutoff, strong-coupling, or not uniform in the continuum limit.",
                        "The route silently changes from the reconstructed H_YM to a different Hamiltonian or subsequence.",
                    ],
                    "audit_skill": "contradiction-route-auditor",
                    "learning_if_failed": "Failure would identify whether the next pivot should attack observable density, uniform decay, or same-theory reconstruction rather than continuing a generic mass-gap slogan.",
                },
            ],
            "conditional_skill_triggers": [
                {"skill": "evidence-acquisition-planner", "trigger": "Locate precise correlator-decay, reflection-positivity, and transfer-matrix evidence."},
                {"skill": "review-reasoner-epistemologist", "trigger": "Audit whether decay evidence is being over-transported across cutoff removal."},
                {"skill": "kb-contradiction-strategist", "trigger": "Use when the no-gap negation can expose low-energy spectral mass obligations."},
                {"skill": "contradiction-route-auditor", "trigger": "Audit the exact no-gap negation, carrier, density obligation, and same-theory invariant."},
                {"skill": "kb-macro-proof-paper-writer", "trigger": "Summarize the bridge only after its assumptions and failure tests are explicit."},
            ],
            "next_recursive_subgoals": [
                "Formalize the density condition for gauge-invariant observables.",
                "Write the spectral-support lemma from exponential decay using the reconstructed Hamiltonian.",
                "Connect m0 to the Delta used by the Hamiltonian derivation report.",
            ],
            "promotion_condition": "Promote only when the decay estimate is cutoff-uniform and the observable family is spectrally determining in the reconstructed continuum theory.",
            "same_theory_invariant": "The decay estimates, spectral measure, observable density claim, and Hamiltonian H must all be attached to the same reconstructed Yang-Mills S_n.",
        },
    ]
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "quality_gate": "pass",
        "source_artifacts": [
            rel(LONG_HORIZON),
            rel(MONITOR),
            "agentic/reports/physics_math_interpretation/latest.md",
            "agentic/reports/hamiltonian_gap_derivation/latest.md",
        ],
        "long_horizon_status": long_horizon.get("quality_gate", ""),
        "skill_coherence_status": long_horizon.get("skill_ecosystem_coherence", {}).get("status", ""),
        "packets": packets,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Yang-Mills Bridge-Lemma Packets",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Quality gate: `{report['quality_gate']}`",
        f"- Long-horizon status: `{report['long_horizon_status']}`",
        f"- Skill coherence status: `{report['skill_coherence_status']}`",
        "",
    ]
    for packet in report["packets"]:
        lines.extend(
            [
                f"## {packet['title']}",
                "",
                f"- Packet: `{packet['packet_id']}`",
                f"- Source route: `{packet['source_route_id']}`",
                f"- Route family: `{packet['route_family']}`",
                f"- Recursive role: {packet['recursive_role']}",
                "",
                "### Lemma Statement",
                "",
                packet["lemma_statement"],
                "",
                "### Objects",
                "",
                "**Source objects**",
            ]
        )
        lines.extend(f"- {item}" for item in packet["source_objects"])
        lines.extend(["", "**Target objects**"])
        lines.extend(f"- {item}" for item in packet["target_objects"])
        lines.extend(["", "### Definitions And Assumptions", ""])
        lines.extend(f"- Definition: {item}" for item in packet["definitions"])
        lines.extend(f"- Assumption: {item}" for item in packet["assumptions"])
        lines.extend(["", "### Equations", ""])
        for equation in packet["equations"]:
            lines.append(f"- {equation['label']}: `{equation['display']}`")
            lines.append(f"  - TeX: `{equation['latex']}`")
            lines.append(f"  - Valid when: {equation['valid_when']}")
        lines.extend(["", "### Proof Obligations", ""])
        lines.extend(f"- {item}" for item in packet["proof_obligations"])
        lines.extend(["", "### Failure Tests", ""])
        lines.extend(f"- {item}" for item in packet["failure_tests"])
        if packet.get("contradiction_branches"):
            lines.extend(["", "### Proof By Contradiction Branches", ""])
            for branch in packet["contradiction_branches"]:
                lines.extend(
                    [
                        f"#### {branch['strategy']}",
                        "",
                        f"- Branch: `{branch['branch_id']}`",
                        f"- Exact negation: {branch['exact_negation']}",
                        f"- Contradiction carrier: {branch['contradiction_carrier']}",
                        f"- Derived consequence: {branch['derived_consequence']}",
                        f"- Conflict target: {branch['conflict_target']}",
                        f"- Audit skill: `{branch['audit_skill']}`",
                        f"- Learning if failed: {branch['learning_if_failed']}",
                        "",
                        "**Preserved commitments**",
                    ]
                )
                lines.extend(f"- {item}" for item in branch["preserved_commitments"])
                lines.extend(["", "**Proof obligations**"])
                lines.extend(f"- {item}" for item in branch["proof_obligations"])
                lines.extend(["", "**Failure modes**"])
                lines.extend(f"- {item}" for item in branch["failure_modes"])
        lines.extend(["", "### Conditional Skill Triggers", ""])
        for trigger in packet["conditional_skill_triggers"]:
            lines.append(f"- `{trigger['skill']}`: {trigger['trigger']}")
        lines.extend(["", "### Next Recursive Subgoals", ""])
        lines.extend(f"- {item}" for item in packet["next_recursive_subgoals"])
        lines.extend(["", f"Promotion condition: {packet['promotion_condition']}"])
        lines.extend(["", f"Same-theory invariant: {packet['same_theory_invariant']}", ""])
    return "\n".join(lines)


def main() -> int:
    report = build_packets()
    write_json(OUT_JSON, report)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
