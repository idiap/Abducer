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

"""Build empirical-evidence requests from active Yang-Mills bridge obligations."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, load_json_object, rel, stable_id, utc_now, write_json


BRIDGE = ROOT / "agentic/reports/yang_mills_bridge_lemma_packets/latest.json"
OUT_JSON = ROOT / "agentic/reports/empirical_evidence_requests/latest.json"
OUT_MD = ROOT / "agentic/reports/empirical_evidence_requests/latest.md"
TARGET_ID = "yang-mills-existence-and-mass-gap-target"


def request(**kwargs: Any) -> dict[str, Any]:
    return kwargs


def build_requests() -> dict[str, Any]:
    bridge = load_json_object(BRIDGE)
    packets = {packet["route_family"]: packet for packet in bridge.get("packets", []) if isinstance(packet, dict)}
    rg_packet = packets.get("Balaban RG continuum-control route", {})
    decay_packet = packets.get("Euclidean correlator-decay to spectral-gap route", {})
    requests = [
        request(
            request_id=stable_id("empirical-evidence", "wilson-loop-string-tension-nontriviality"),
            linked_packet_id=rg_packet.get("packet_id", ""),
            linked_theoretical_step="Attach one non-Gaussian gauge-invariant observable witness to rule out triviality.",
            evidence_mode="empirical_probe",
            empirical_question=(
                "Do lattice Yang-Mills simulations or continuum-extrapolated analyses show gauge-invariant Wilson-loop "
                "area-law behavior, string tension, or connected cumulants that can guide a same-theory nontriviality witness?"
            ),
            observable_or_quantity="Wilson-loop area law, string tension, or connected gauge-invariant cumulants",
            proximity_class="continuum-extrapolated-regulated-evidence",
            search_plan=[
                "Search for lattice Yang-Mills Wilson-loop/string-tension studies with continuum extrapolation or controlled scaling.",
                "Extract which gauge group, dimension, action, observable normalization, and cutoff/volume controls are used.",
                "Record whether the observable could become a same-theory nontriviality witness after OS/continuum reconstruction.",
            ],
            acceptable_sources=[
                "peer-reviewed lattice gauge theory papers",
                "review articles summarizing Wilson-loop area law or string tension evidence",
                "public numerical datasets or reproducible lattice simulation reports",
            ],
            support_criteria=[
                "Evidence concerns four-dimensional compact simple gauge Yang-Mills or a clearly marked regulated approximation.",
                "The observable is gauge invariant and connected to a continuum-extrapolated scale.",
                "The result suggests a nonzero interacting gauge-invariant witness rather than a Gaussian/free collapse.",
            ],
            refutation_criteria=[
                "Evidence is only fixed cutoff, finite volume, or non-gauge-invariant.",
                "The measured signal disappears under continuum extrapolation.",
                "The source concerns a different theory without an explicit transfer argument.",
            ],
            transfer_gap=(
                "A theorem must still show that the selected observable belongs to the same limiting Schwinger family "
                "used for OS reconstruction and that its connected cumulant survives cutoff removal."
            ),
            proof_boundary="Proof boundary: Wilson-loop or string-tension evidence can select and prioritize a nontriviality witness, but it is not proof of continuum nontriviality.",
            integration_action="If supportive, add a nontriviality-witness evidence task and keep it behind the RG-to-OS same-theory gate.",
            demotion_triggers=[
                "quarantine if evidence is analogy-only",
                "demote if no continuum or scaling control is reported",
                "demote if the observable cannot be tied to gauge-invariant Schwinger functions",
            ],
            skill_triggers=["evidence-acquisition-planner", "prior-art-importer", "review-reasoner-epistemologist"],
        ),
        request(
            request_id=stable_id("empirical-evidence", "glueball-correlator-decay-gap-scale"),
            linked_packet_id=decay_packet.get("packet_id", ""),
            linked_theoretical_step="Prove decay constants stay bounded below through cutoff removal.",
            evidence_mode="empirical_probe",
            empirical_question=(
                "Do lattice glueball correlator or mass-spectrum studies provide continuum-extrapolated evidence for "
                "positive gauge-invariant mass scales compatible with Euclidean correlator decay?"
            ),
            observable_or_quantity="Gauge-invariant glueball correlator decay, mass ratios, and spectral scale estimates",
            proximity_class="continuum-extrapolated-regulated-evidence",
            search_plan=[
                "Search for glueball spectrum and Euclidean correlator decay studies in four-dimensional pure Yang-Mills lattice gauge theory.",
                "Extract continuum extrapolation, finite-size scaling, gauge group, observable family, and mass-scale uncertainty.",
                "Record whether the evidence supports a candidate observable family for the decay-to-gap bridge.",
            ],
            acceptable_sources=[
                "lattice glueball spectrum papers",
                "continuum-extrapolated Monte Carlo studies",
                "reviews of pure Yang-Mills mass gap and glueball masses",
            ],
            support_criteria=[
                "The study estimates a positive mass scale from gauge-invariant correlators.",
                "The source reports continuum extrapolation or scaling checks.",
                "The observable family is close to the one needed for OS spectral reconstruction.",
            ],
            refutation_criteria=[
                "Mass estimates vanish or become unstable under continuum extrapolation.",
                "The observable is gauge-fixed or not gauge invariant without a transfer argument.",
                "Only strong-coupling or fixed-lattice-spacing evidence is available.",
            ],
            transfer_gap=(
                "A proof must still turn the regulated correlator evidence into a cutoff-uniform bound for the same "
                "continuum Schwinger functions and show the observable family is spectrally determining in P_perp H_YM."
            ),
            proof_boundary="Proof boundary: positive lattice glueball masses guide the decay route, but they are not proof of E_H((0,m0))P_perp=0.",
            integration_action="If supportive, prioritize the cutoff-uniform decay and observable-density proof obligations.",
            demotion_triggers=[
                "quarantine if evidence has no continuum extrapolation",
                "demote if the observable sector is not gauge invariant",
                "pivot if all close evidence suggests nonuniform decay constants",
            ],
            skill_triggers=["evidence-acquisition-planner", "prior-art-importer", "contradiction-route-auditor"],
        ),
        request(
            request_id=stable_id("empirical-evidence", "reflection-positive-lattice-actions-transfer"),
            linked_packet_id=rg_packet.get("packet_id", ""),
            linked_theoretical_step="Prove the limiting topology preserves OS positivity for the gauge-invariant observable sector.",
            evidence_mode="source_import",
            empirical_question=(
                "Which reflection-positive lattice gauge actions, transfer-matrix constructions, or numerical practice constraints "
                "are close enough to inform the OS-positivity preservation obligation?"
            ),
            observable_or_quantity="Reflection-positive lattice action, transfer matrix, and Schwinger-function positivity tests",
            proximity_class="regulated-approximation",
            search_plan=[
                "Search for reflection positivity and transfer-matrix results for lattice gauge theories.",
                "Separate rigorous source theorems from empirical/numerical practice.",
                "Extract conditions on action, gauge group, observable algebra, and limiting topology.",
            ],
            acceptable_sources=[
                "mathematical physics papers on lattice reflection positivity",
                "transfer-matrix construction references",
                "lattice gauge theory reviews with explicit reflection-positivity conditions",
            ],
            support_criteria=[
                "The source states reflection positivity for gauge-invariant lattice observables.",
                "The construction is compatible with compact simple gauge groups.",
                "The result identifies what topology or algebra is needed for a limiting OS argument.",
            ],
            refutation_criteria=[
                "The action used by the target route is not reflection positive.",
                "The transfer matrix applies only after gauge fixing that changes observables.",
                "No limiting closedness result can be stated.",
            ],
            transfer_gap="A closure theorem is still needed before regulated reflection positivity implies OS positivity of the continuum Schwinger functions.",
            proof_boundary="Proof boundary: reflection-positive lattice practice can supply source conditions, but the continuum OS theorem remains a mathematical proof obligation.",
            integration_action="If supportive, import theorem statements and sharpen the OS-positivity-failure reductio conflict target.",
            demotion_triggers=[
                "demote if no topology for closedness can be named",
                "quarantine if the transfer matrix belongs to a different observable algebra",
                "repair if the evidence only concerns scalar models",
            ],
            skill_triggers=["evidence-acquisition-planner", "prior-art-importer", "contradiction-route-auditor"],
        ),
        request(
            request_id=stable_id("empirical-evidence", "negative-evidence-uniform-decay"),
            linked_packet_id=decay_packet.get("packet_id", ""),
            linked_theoretical_step="Transport the cutoff-uniform decay estimate to the continuum without changing the object.",
            evidence_mode="negative_evidence",
            empirical_question=(
                "Are there lattice, numerical, or prior-art warnings that apparent mass scales or correlator decay constants "
                "degenerate under continuum extrapolation, finite-size scaling, or observable-sector changes?"
            ),
            observable_or_quantity="Cutoff dependence of correlator decay rates and finite-size scaling of mass estimates",
            proximity_class="continuum-extrapolated-regulated-evidence",
            search_plan=[
                "Search specifically for failures, systematic uncertainties, and continuum-extrapolation caveats in mass-gap-related lattice studies.",
                "Record whether finite-size effects, topology freezing, gauge fixing, or scale setting could invalidate a naive decay-to-gap inference.",
                "Use findings as demotion tests for the no-gap spectral reductio and decay-to-gap bridge.",
            ],
            acceptable_sources=[
                "lattice systematic-error studies",
                "reviews of glueball mass extrapolation limitations",
                "method papers discussing finite-size, continuum, or scale-setting artifacts",
            ],
            support_criteria=[
                "Evidence identifies concrete conditions required to keep decay constants stable.",
                "Known failure modes can be translated into proof obligations or demotion triggers.",
                "The evidence refines the search without replacing the theorem.",
            ],
            refutation_criteria=[
                "The evidence shows all close decay estimates are fixed-cutoff artifacts.",
                "Continuum extrapolation destroys the positive lower bound.",
                "Observable-sector changes make the spectral interpretation invalid.",
            ],
            transfer_gap="Even negative empirical evidence must be translated into mathematical boundary regimes before it can refute a proof route.",
            proof_boundary="Proof boundary: numerical instability can demote or reprioritize a route; it is not proof against the mathematical target by itself.",
            integration_action="If negative evidence is strong, pivot toward construction/nontriviality or revise the observable family.",
            demotion_triggers=[
                "pivot if decay constants systematically vanish under cutoff removal",
                "quarantine if the observable family is not spectrally determining",
                "backtrack if the evidence shows finite-volume contamination",
            ],
            skill_triggers=["evidence-acquisition-planner", "counterexample-hunter", "review-reasoner-epistemologist"],
        ),
    ]
    return {
        "version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "source_artifact": rel(BRIDGE),
        "quality_gate": "pass",
        "requests": requests,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Empirical Evidence Requests",
        "",
        f"- Target: `{report['target_id']}`",
        f"- Source: `{report['source_artifact']}`",
        f"- Requests: {len(report['requests'])}",
        "",
    ]
    for item in report["requests"]:
        lines.extend(
            [
                f"## {item['request_id']}",
                "",
                f"- Mode: `{item['evidence_mode']}`",
                f"- Proximity: `{item['proximity_class']}`",
                f"- Linked step: {item['linked_theoretical_step']}",
                f"- Observable or quantity: {item['observable_or_quantity']}",
                "",
                "### Empirical Question",
                "",
                item["empirical_question"],
                "",
                "### Search Plan",
            ]
        )
        lines.extend(f"- {row}" for row in item["search_plan"])
        lines.extend(["", "### Support Criteria"])
        lines.extend(f"- {row}" for row in item["support_criteria"])
        lines.extend(["", "### Refutation Criteria"])
        lines.extend(f"- {row}" for row in item["refutation_criteria"])
        lines.extend(["", f"Transfer gap: {item['transfer_gap']}"])
        lines.extend(["", f"Proof boundary: {item['proof_boundary']}"])
        lines.extend(["", f"Integration action: {item['integration_action']}", ""])
    return "\n".join(lines)


def main() -> int:
    report = build_requests()
    write_json(OUT_JSON, report)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
