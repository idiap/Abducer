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

"""Build an active physics/math interpretation of the Yang-Mills route state.

This report is deliberately not another relevance score. It interprets the
current candidate routes as possible mathematical proof programmes and asks
what each one would have to mean in constructive quantum field theory terms.
"""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, load_json_object, rel, utc_now, write_json


PACKET = ROOT / "agentic/reports/reasoning_monitor/latest.json"
OUT_JSON = ROOT / "agentic/reports/physics_math_interpretation/latest.json"
OUT_MD = ROOT / "agentic/reports/physics_math_interpretation/latest.md"
YANG_MILLS_TARGET = "yang-mills-existence-and-mass-gap-target"


def obligations_for(route: dict[str, Any]) -> list[str]:
    obligations = []
    for row in route.get("obligations", []):
        if isinstance(row, dict) and clean_text(row.get("requirement")):
            obligations.append(clean_text(row["requirement"]))
    return obligations


def route_family(route: dict[str, Any]) -> str:
    return clean_text(route.get("route_blueprint", {}).get("route_family"))


def active_routes(packet: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        route
        for route in packet.get("candidate_routes", [])
        if route.get("route_disposition") == "proof_queue"
    ]


def balaban_interpretation(route: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_thesis": (
            "The route treats Balaban-style renormalisation group control as a possible constructive existence spine: "
            "scale-by-scale effective actions must remain stable while the ultraviolet cutoff is removed, producing a "
            "nontrivial continuum Yang-Mills measure or Schwinger-function family."
        ),
        "mathematical_objects": [
            "regulated lattice or continuum-cutoff Yang-Mills measures for compact simple gauge group G",
            "Balaban effective actions and polymer/small-field estimates across scales",
            "candidate Schwinger functions obtained after cutoff removal",
            "gauge-invariant observables whose correlations can witness nontriviality and a gap",
        ],
        "mechanism_chain": [
            "establish uniform multiscale RG bounds for effective actions",
            "use those bounds to obtain tightness or convergence of regulated measures/Schwinger functions",
            "prove OS positivity and Euclidean invariance survive the limiting procedure",
            "separate the limiting object from a Gaussian or empty theory by an observable witness",
            "derive a cutoff-stable mass-gap witness, such as exponential decay or a Hamiltonian spectral lower bound",
        ],
        "physical_meaning": (
            "If successful, the physics content is not merely ultraviolet regularity; it is confinement-like suppression "
            "of long-range gauge-invariant correlations in a genuine four-dimensional interacting quantum gauge field."
        ),
        "load_bearing_bridge": (
            "The decisive bridge is from RG-controlled cutoff measures to OS-positive continuum Schwinger functions, "
            "and then from those functions to a reconstructed theory with a positive excitation threshold."
        ),
        "conceptual_bottleneck": (
            "Balaban estimates are strong evidence for ultraviolet control, but the Clay problem also requires nontriviality, "
            "OS/Wightman adequacy, and a positive mass gap in the same limiting theory. The route fails if those are proved "
            "in separate regulated worlds."
        ),
        "false_positive_controls": [
            "Do not count finite-volume, fixed-cutoff, or infrared-cutoff control as continuum existence.",
            "Do not count Gaussian/free limiting behavior as Yang-Mills nontriviality.",
            "Do not infer a mass gap from RG stability unless the gap witness survives cutoff removal.",
        ],
        "next_lemma_questions": [
            "Which Balaban effective-action estimates are uniform enough to define a subsequential OS-positive limit?",
            "What gauge-invariant observable rules out collapse to a trivial continuum measure?",
            "Can the same RG bounds provide exponential decay, or is a separate infrared/confinement argument needed?",
        ],
    }


def correlator_gap_interpretation(route: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_thesis": (
            "The route interprets Euclidean exponential decay of gauge-invariant correlators as a spectral gap programme: "
            "reflection positivity should turn Euclidean time decay into a transfer-matrix or Hamiltonian lower bound after "
            "OS reconstruction."
        ),
        "mathematical_objects": [
            "reflection-positive Schwinger functions for gauge-invariant Yang-Mills observables",
            "transfer matrix or reconstructed Hamiltonian generated by Euclidean time translations",
            "vacuum sector and vacuum-orthogonal excitation subspace",
            "cutoff-uniform exponential decay constants for selected correlation functions",
        ],
        "mechanism_chain": [
            "identify Schwinger functions or local gauge-invariant observables carrying the decay claim",
            "prove reflection positivity and construct the transfer matrix/Hilbert space",
            "establish exponential Euclidean time decay with constants independent of lattice spacing and cutoffs",
            "pass through OS reconstruction to Wightman fields and a positive-energy Hamiltonian",
            "show the decay lower-bounds the first non-vacuum excitation and therefore proves a spectral gap Delta > 0",
        ],
        "physical_meaning": (
            "The physics content is a rigorous version of massive behavior: gauge-invariant excitations cannot approach "
            "the vacuum with arbitrarily small energy, so long-distance correlations decay exponentially."
        ),
        "load_bearing_bridge": (
            "The decisive bridge is decay-to-spectrum transfer: exponential Euclidean correlator decay must become a "
            "positive Hamiltonian gap in the reconstructed continuum theory, not merely in a lattice approximation."
        ),
        "conceptual_bottleneck": (
            "Strong-coupling lattice decay is not enough. The hard step is uniformity through the continuum limit while "
            "preserving reflection positivity, nontriviality, and control over the physical observable sector."
        ),
        "false_positive_controls": [
            "Reject decay estimates whose constants vanish as the cutoff is removed.",
            "Reject transfer-matrix gaps that live only in a regulated lattice Hilbert space.",
            "Reject observables that do not constrain the physical Hamiltonian spectrum after OS reconstruction.",
        ],
        "next_lemma_questions": [
            "Which gauge-invariant Schwinger functions are sufficient to detect the vacuum-orthogonal spectral threshold?",
            "Can reflection positivity be preserved for the exact limiting objects used in the decay argument?",
            "What uniform decay estimate survives the lattice-continuum passage without becoming vacuous?",
        ],
    }


def os_interpretation(route: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_thesis": (
            "The route treats OS reconstruction as the axiomatic spine: construct Euclidean Yang-Mills data first, then "
            "recover Wightman fields, Hamiltonian dynamics, and only then attach a mass-gap witness."
        ),
        "mathematical_objects": [
            "Euclidean Schwinger functions",
            "OS reflection operation and positivity form",
            "reconstructed Hilbert space, vacuum, fields, and Hamiltonian",
            "gap witness in the reconstructed spectrum",
        ],
        "mechanism_chain": [
            "construct the Schwinger-function family",
            "verify OS positivity and regularity properties",
            "apply reconstruction to obtain Wightman QFT data",
            "identify the Hamiltonian and vacuum sector",
            "prove or import a positive mass-gap witness for that Hamiltonian",
        ],
        "physical_meaning": (
            "The physics content is the transition from Euclidean functional integrals to a real-time quantum field theory "
            "with positive energy and physically meaningful excitations."
        ),
        "load_bearing_bridge": "The decisive bridge is OS reconstruction from Euclidean gauge-field data to Wightman/Hamiltonian data.",
        "conceptual_bottleneck": (
            "OS adequacy alone gives a theory, not the mass gap. The route only becomes Clay-relevant when reconstruction "
            "and the spectral gap are attached to the same nontrivial continuum object."
        ),
        "false_positive_controls": [
            "Do not treat formal Euclidean path integrals as constructed Schwinger functions.",
            "Do not infer a Hamiltonian gap from OS reconstruction alone.",
            "Do not ignore gauge-invariant observables and nontriviality of the vacuum sector.",
        ],
        "next_lemma_questions": [
            "Which Schwinger functions are actually constructed and with what regularity?",
            "Where does reflection positivity enter the limiting argument?",
            "What independent input supplies the positive spectral gap after reconstruction?",
        ],
    }


def constructive_interpretation(route: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_thesis": (
            "The route interprets constructive QFT evidence as an existence programme for Yang-Mills: define the nonperturbative "
            "object, verify axioms, prove nontriviality, and keep the mass-gap argument as a distinct burden."
        ),
        "mathematical_objects": [
            "constructive measure or Schwinger-function family",
            "OS/Wightman axiom verification targets",
            "non-Gaussian observable or correlation witness",
            "spectral-gap mechanism attached to the constructed theory",
        ],
        "mechanism_chain": [
            "define the object to be constructed",
            "prove it has the required Euclidean or Wightman properties",
            "show it is nontrivial and four-dimensional",
            "connect it to gauge-invariant physical observables",
            "supply a separate argument for Delta > 0",
        ],
        "physical_meaning": (
            "The physics content is existence of a genuine quantum Yang-Mills field theory, not perturbation theory or an "
            "effective model, with massive physical excitations."
        ),
        "load_bearing_bridge": "The decisive bridge is from construction to axiomatic adequacy plus nontrivial spectral content.",
        "conceptual_bottleneck": "Constructive existence without a gap is too weak; a gap argument without the constructed theory is ungrounded.",
        "false_positive_controls": [
            "Reject lower-dimensional constructive analogies without transfer.",
            "Reject existence statements that omit nontriviality.",
            "Reject mass-gap claims that are not attached to the constructed object.",
        ],
        "next_lemma_questions": [
            "What exactly is the constructed Yang-Mills object?",
            "Which axiom verification remains open?",
            "What observable witnesses both nontriviality and the spectral gap?",
        ],
    }


def hamiltonian_interpretation(route: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_thesis": (
            "The route converts the problem into Hamiltonian spectral language: after constructing the physical Hilbert space "
            "and vacuum, prove the first vacuum-orthogonal excitation has energy at least Delta > 0."
        ),
        "mathematical_objects": [
            "physical Hilbert space",
            "vacuum vector and vacuum-orthogonal sector",
            "positive self-adjoint Hamiltonian",
            "spectral lower bound Delta",
        ],
        "mechanism_chain": [
            "construct the Hilbert space from OS/Wightman data or a transfer matrix",
            "identify the time-translation generator",
            "isolate the vacuum sector",
            "control the excitation spectrum",
            "prove a positive lower bound stable under the continuum limit",
        ],
        "physical_meaning": "The physics content is a rigorous mass threshold for all non-vacuum physical excitations.",
        "load_bearing_bridge": "The decisive bridge is from constructed continuum dynamics to a spectral lower bound.",
        "conceptual_bottleneck": "A regulated Hamiltonian gap does not solve the problem unless it survives reconstruction and cutoff removal.",
        "false_positive_controls": [
            "Reject numerical or heuristic gaps.",
            "Reject gaps for cutoff Hamiltonians without continuum stability.",
            "Reject a spectral claim before the physical Hilbert space is constructed.",
        ],
        "next_lemma_questions": [
            "How is the Hamiltonian obtained from the constructed Yang-Mills theory?",
            "What controls the vacuum-orthogonal spectral infimum?",
            "Which limit preserves the lower bound Delta?",
        ],
    }


def target_control_interpretation(route: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_thesis": (
            "The route is a target-control branch: it keeps compact simple gauge group structure visible while checking whether "
            "a proposed mediator actually contributes to construction, axioms, continuum passage, nontriviality, or mass gap."
        ),
        "mathematical_objects": [
            "compact simple gauge group G",
            "connections or gauge fields valued in the Lie algebra of G",
            "gauge-invariant observables",
            "target obligations for existence, OS/Wightman adequacy, continuum limit, nontriviality, and gap",
        ],
        "mechanism_chain": [
            "preserve the correct gauge group and gauge-invariant observable language",
            "identify which Clay obligation the mediator could support",
            "reject purely definitional bridges that do not advance construction or spectral control",
            "attach the mediator to a concrete route family before promotion",
        ],
        "physical_meaning": "The physics content is structural discipline: the search must remain about non-Abelian Yang-Mills theory.",
        "load_bearing_bridge": "The decisive bridge is from gauge-group structure to a substantive construction or spectral obligation.",
        "conceptual_bottleneck": "Correct definitions are necessary but not progress unless they constrain a proof mechanism.",
        "false_positive_controls": [
            "Reject definitional restatements as proof progress.",
            "Reject bridges that do not mention a constructed object or physical observable.",
            "Reject gauge-language routes that never face continuum or spectral obligations.",
        ],
        "next_lemma_questions": [
            "Which later route uses the compact simple gauge group assumption essentially?",
            "Does the bridge affect OS positivity, nontriviality, or the spectral gap?",
            "What construction object would make the definition operational?",
        ],
    }


INTERPRETERS = [
    ("Balaban RG continuum-control route", balaban_interpretation),
    ("Euclidean correlator-decay to spectral-gap route", correlator_gap_interpretation),
    ("OS reconstruction and reflection-positivity bridge", os_interpretation),
    ("Constructive QFT existence route", constructive_interpretation),
    ("Hamiltonian spectral-gap route", hamiltonian_interpretation),
    ("Yang-Mills target-control route", target_control_interpretation),
]


def interpret_route(route: dict[str, Any]) -> dict[str, Any]:
    family = route_family(route)
    for expected, builder in INTERPRETERS:
        if family == expected:
            content = builder(route)
            break
    else:
        content = target_control_interpretation(route)
    obligations = obligations_for(route)
    content.update(
        {
            "candidate_id": route["candidate_id"],
            "route_family": family or "unclassified",
            "creative_operation": route.get("creative_operation", ""),
            "route_disposition": route.get("route_disposition", ""),
            "source_witness": clean_text(route.get("source_witness", "")),
            "interpreted_obligations": obligations[:8],
            "content_verdict": "substantive route, not proof",
            "why_not_a_proof": (
                "This interpretation identifies a mathematically meaningful proof programme, but none of the listed "
                "load-bearing lemmas has been discharged inside the artifact."
            ),
        }
    )
    return content


def build_report() -> dict[str, Any]:
    packet = load_json_object(PACKET)
    routes = active_routes(packet)
    interpretations = [interpret_route(route) for route in routes]
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": packet["target"]["target_id"],
        "interpretation_mode": "active physics/math route interpretation",
        "not_a_score_policy": (
            "The report passes only if it articulates route-specific mechanisms, mathematical objects, physical meaning, "
            "failure controls, and next lemma questions. Numeric relevance scores are intentionally not used."
        ),
        "scope_boundary": (
            "This is an interpretive audit of the current Yang-Mills mechanism search. It does not claim a proof of Yang-Mills existence "
            "or the mass gap."
        ),
        "active_route_count": len(routes),
        "interpretations": interpretations,
        "cross_route_synthesis": {
            "constructive_spine": (
                "The Balaban RG route supplies the strongest continuum-construction pressure, while the correlator-decay route "
                "supplies the clearest spectral-gap transfer pressure."
            ),
            "missing_joint_step": (
                "The central missing joint step is to make the continuum object, OS reconstruction, nontriviality witness, "
                "and positive spectral gap live in the same limiting Yang-Mills theory."
            ),
            "next_mathematical_physics_focus": [
                "Treat Balaban/RG control as progress only when it outputs OS-positive continuum Schwinger functions for gauge-invariant observables.",
                "Treat correlator decay as progress only when the decay rate is cutoff-uniform and its spectral measure belongs to a determining observable family.",
                "State the bridge lemma that could let RG-controlled construction feed the Euclidean spectral-measure argument in one limiting Yang-Mills theory.",
            ],
        },
        "source_artifacts": [
            "agentic/reports/reasoning_monitor/latest.json",
            "agentic/reports/long_horizon/latest.json",
            "agentic/reports/hamiltonian_gap_derivation/latest.md",
            "KB/yang-mills-existence-and-mass-gap.kb.md",
        ],
    }


def render_interpretation(item: dict[str, Any]) -> list[str]:
    lines = [
        f"### {item['candidate_id']}",
        "",
        f"- Route family: `{item['route_family']}`",
        f"- Verdict: {item['content_verdict']}",
        f"- Thesis: {item['route_thesis']}",
        f"- Physical meaning: {item['physical_meaning']}",
        f"- Load-bearing bridge: {item['load_bearing_bridge']}",
        f"- Conceptual bottleneck: {item['conceptual_bottleneck']}",
        "",
        "Mathematical objects:",
    ]
    lines.extend(f"- {value}" for value in item["mathematical_objects"])
    lines.append("")
    lines.append("Mechanism chain:")
    lines.extend(f"{index}. {value}" for index, value in enumerate(item["mechanism_chain"], start=1))
    lines.append("")
    lines.append("False-positive controls:")
    lines.extend(f"- {value}" for value in item["false_positive_controls"])
    lines.append("")
    lines.append("Next lemma questions:")
    lines.extend(f"- {value}" for value in item["next_lemma_questions"])
    lines.append("")
    lines.append("Why this is not a proof:")
    lines.append("")
    lines.append(item["why_not_a_proof"])
    lines.append("")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Physics/Math Interpretation Audit",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Mode: {report['interpretation_mode']}",
        f"- Active routes interpreted: {report['active_route_count']}",
        "",
        "## Policy",
        "",
        report["not_a_score_policy"],
        "",
        report["scope_boundary"],
        "",
        "## Active Route Interpretations",
        "",
    ]
    for item in report["interpretations"]:
        lines.extend(render_interpretation(item))
    synthesis = report["cross_route_synthesis"]
    lines.extend(
        [
            "## Cross-Route Synthesis",
            "",
            f"- Constructive spine: {synthesis['constructive_spine']}",
            f"- Missing joint step: {synthesis['missing_joint_step']}",
            "",
            "Next mathematical-physics focus:",
        ]
    )
    lines.extend(f"- {value}" for value in synthesis["next_mathematical_physics_focus"])
    lines.append("")
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
