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
"""Build qualitative physics relation packets and a mechanistic graph."""

from __future__ import annotations

import argparse
from collections import Counter
from typing import Any

from agentic_common import ROOT, clean_text, load_optional_json, stable_id, utc_now, write_json
from discovery_marathon_common import load_cycles, load_run_state


PACKET_OUT = ROOT / "agentic/reports/qualitative_relation_packets/latest.json"
GRAPH_DIR = ROOT / "agentic/state/qualitative_mechanistic_graphs"
REPORT = ROOT / "agentic/reports/qualitative_mechanistic_graph/latest.md"
GEDANKEN_REPORT = ROOT / "agentic/reports/gedanken_experiments/latest.json"
SYMBOLIC_MATRIX_PROBE = ROOT / "agentic/reports/symbolic_matrix_probe/latest.json"
ANALYTIC_OBLIGATIONS = ROOT / "agentic/reports/analytic_estimate_obligations/latest.json"
FINITE_ALGEBRA_INTERFACES = ROOT / "agentic/reports/finite_algebra_interfaces/latest.json"


def variable(var_id: str, name: str, role: str, qtype: str, dim: str, domain: str, dep: str, control: str, evidence: list[str]) -> dict[str, Any]:
    return {
        "id": var_id,
        "name": name,
        "physical_role": role,
        "quantity_type": qtype,
        "units_or_dimension": dim,
        "domain": domain,
        "independent_or_dependent": dep,
        "control_status": control,
        "source_artifacts": evidence,
    }


def base_variables(evidence: list[str]) -> list[dict[str, Any]]:
    return [
        variable("var.cutoff_a", "lattice spacing / cutoff a", "regulator controlling UV resolution", "scale", "length", "regulated gauge-field construction", "independent", "control knob before continuum limit", evidence),
        variable("var.volume_L", "volume L", "IR box size controlling finite-volume effects", "scale", "length", "regulated gauge-field construction", "independent", "control knob before infinite-volume limit", evidence),
        variable("var.euclidean_time_t", "Euclidean time separation t", "separation used to read spectral decay", "scale", "time/length", "Schwinger function probe", "independent", "observable probe variable", evidence),
        variable("var.correlation_C", "connected correlator C(t)", "gauge-invariant observable correlation", "observable", "observable squared", "Euclidean continuum candidate", "dependent", "measured response", evidence),
        variable("var.spectral_gap_m", "spectral mass scale m", "candidate lower support of Hamiltonian spectrum", "scale", "inverse length", "OS-reconstructed Hilbert space", "dependent", "target witness", evidence),
        variable("var.reflection_gram_N", "reflection Gram matrix N", "finite-family positivity carrier", "matrix", "dimensionless", "OS reflection-positive sector", "dependent", "positivity witness", evidence),
        variable("var.boundary_factor_B", "boundary OPE factor B", "short-distance collar contribution", "matrix", "dimensionless", "collar-collapse probe", "dependent", "mechanism candidate", evidence),
        variable("var.quotient_phase_phi", "quotient holonomy Phi", "phase obstruction in normalized Schur quotient", "phase", "angle", "finite Wilson hairpin probe", "dependent", "falsifier variable", evidence),
    ]


def regime(regime_id: str, name: str, scale: str, limit_order: str, boundary: str, perturbative: str, finite: str, transition: str) -> dict[str, Any]:
    return {
        "id": regime_id,
        "name": name,
        "scale_range": scale,
        "limit_order": limit_order,
        "boundary_conditions": boundary,
        "perturbative_status": perturbative,
        "finite_or_continuum_status": finite,
        "transition_conditions": transition,
    }


def base_regimes() -> list[dict[str, Any]]:
    return [
        regime("reg.fixed_cutoff", "fixed cutoff and finite volume", "a > 0 and L < infinity", "no continuum limit yet", "lattice or regulated boundary", "mixed", "finite regulator", "invalid as final target without transfer"),
        regime("reg.continuum_transfer", "continuum transfer regime", "a -> 0 and L -> infinity with uniform control", "cutoff and volume limits must be certified", "continuum positive-time observables", "nonperturbative", "continuum candidate", "requires tightness, positivity closure, and observable survival"),
        regime("reg.long_time_spectral", "long Euclidean time spectral readout", "t -> infinity", "OS reconstruction before spectral interpretation", "positive-time gauge-invariant observables", "nonperturbative", "continuum Hilbert sector", "requires dense observable sector and positive Hamiltonian"),
        regime("reg.collar_collapse", "reflection-plane collar collapse", "delta -> 0 after finite-family positivity is controlled", "collar limit after fixed-family construction", "Wilson hairpin collars", "boundary-sensitive", "finite-family probe", "phase or determinant obstruction may appear"),
    ]


def relation(rel_id: str, source: str, target: str, kind: str, direction: str, rate: str, monotonicity: str, convergence: str, regimes: list[str], assumptions: list[str], failures: list[str], evidence: list[str], status: str) -> dict[str, Any]:
    return {
        "id": rel_id,
        "source_variable": source,
        "target_variable": target,
        "relation_kind": kind,
        "direction": direction,
        "qualitative_rate": rate,
        "monotonicity": monotonicity,
        "convexity_or_curvature": "not established",
        "convergence_behavior": convergence,
        "valid_regime_ids": regimes,
        "assumptions": assumptions,
        "failure_modes": failures,
        "evidence_paths": evidence,
        "epistemic_status": status,
    }


def cycle_path(cycle: dict[str, Any], run_id: str) -> str:
    return f"agentic/runs/discovery_marathons/{run_id}/cycles/{cycle.get('cycle_id', 'unknown')}.json"


def build_packets(target_id: str, cycles: list[dict[str, Any]], run_id: str) -> list[dict[str, Any]]:
    evidence = [cycle_path(cycle, run_id) for cycle in cycles[-8:]] or ["agentic/reports/discovery_marathon/latest.json"]
    variables = base_variables(evidence)
    regimes = base_regimes()
    recent_cycles = [clean_text(cycle.get("cycle_id")) for cycle in cycles[-8:]]
    relations = [
        relation(
            "rel.cutoff-to-gram-positivity",
            "var.cutoff_a",
            "var.reflection_gram_N",
            "constrains",
            "smaller cutoff should preserve positivity only if the positivity cone is closed",
            "not monotone without uniform topology",
            "conditional",
            "may converge to a positive Gram matrix only in the closed reflected-probe topology",
            ["reg.fixed_cutoff", "reg.continuum_transfer"],
            ["Regulated reflection positivity holds for every fixed cutoff.", "The topology controls finite reflected observable families."],
            ["Reflection positivity leaks under cutoff removal.", "The limiting topology is too weak for positivity closure."],
            evidence,
            "proof_obligation",
        ),
        relation(
            "rel.euclidean-decay-to-gap",
            "var.euclidean_time_t",
            "var.correlation_C",
            "decreases",
            "larger Euclidean time suppresses spectral components above the lower support",
            "exponential when a positive spectral threshold is present",
            "monotone for positive spectral measures after vacuum subtraction",
            "decay rate witnesses spectral support only after OS reconstruction and observable density",
            ["reg.long_time_spectral"],
            ["The correlator has a positive spectral representation.", "The observable belongs to the reconstructed gauge-invariant algebra."],
            ["Decay is only fixed-regulator.", "The observable sector is not dense or misses low-energy states."],
            evidence,
            "conjectural",
        ),
        relation(
            "rel.spectral-gap-controls-correlator",
            "var.spectral_gap_m",
            "var.correlation_C",
            "decreases",
            "larger mass scale gives faster long-time decay",
            "exponential in t with rate bounded by m",
            "locally monotone in the lower spectral threshold",
            "C(t) is bounded by exp(-m t) times the observable norm when the spectral measure avoids (0,m)",
            ["reg.long_time_spectral"],
            ["A positive Hamiltonian and spectral measure are already constructed.", "Vacuum contribution is removed."],
            ["The spectral measure has arbitrarily small non-vacuum support.", "The correlator does not see the full excitation sector."],
            evidence,
            "established",
        ),
        relation(
            "rel-boundary-factor-to-phase",
            "var.boundary_factor_B",
            "var.quotient_phase_phi",
            "enables",
            "boundary OPE factors can introduce phase structure in normalized quotients",
            "finite-family and phase-sensitive",
            "not globally monotone",
            "phase behavior must be computed before Schur quotient positivity can be trusted",
            ["reg.collar_collapse"],
            ["The Wilson hairpin collars share a reflection-plane footprint.", "The normalized quotient is computed within the same finite family."],
            ["A nonzero quotient holonomy makes pairwise positivity insufficient.", "A negative determinant falsifies the proposed positivity bridge."],
            evidence,
            "validated_probe",
        ),
        relation(
            "rel-phase-falsifies-gram-transfer",
            "var.quotient_phase_phi",
            "var.reflection_gram_N",
            "falsifies",
            "nonzero holonomy or negative normalized determinant blocks naive positivity transfer",
            "threshold-like",
            "not monotone",
            "the branch must backtrack or quarantine if the finite-family determinant is negative",
            ["reg.collar_collapse"],
            ["The finite Wilson family is realized in the same reflected observable algebra."],
            ["The phase obstruction is an artifact of a proxy model.", "The determinant test is not realized by Yang-Mills observables."],
            evidence,
            "conjectural",
        ),
    ]
    packet = {
        "packet_id": stable_id("qpr.packet", target_id, recent_cycles),
        "target_id": target_id,
        "created_utc": utc_now(),
        "source_artifacts": evidence,
        "variables": variables,
        "regimes": regimes,
        "relations": relations,
        "falsifiers": [
            "Noncommuting cutoff and volume limits change the qualitative conclusion.",
            "A relation holds only for a proxy observable or fixed regulator.",
            "A finite-family determinant or phase obstruction reverses a proposed positivity transfer.",
        ],
        "concrete_probes": [
            {
                "probe_id": "probe.three-hairpin-schur",
                "description": "Compute a finite Wilson hairpin Schur quotient and determinant to test whether pairwise damping implies finite-family positivity.",
                "transfer_scope": "Calibrates the qualitative phase obstruction; it is not theorem progress without same-theory realization.",
            }
        ],
        "epistemic_status": "conjectural",
        "validation_handoff": "python agentic/scripts/validate_qualitative_relation_packets.py",
    }
    return [packet]


def node_from_variable(var: dict[str, Any]) -> dict[str, Any]:
    kind = "observable" if var["quantity_type"] == "observable" else "scale" if var["quantity_type"] == "scale" else "variable"
    return {
        "id": var["id"],
        "label": var["name"],
        "node_type": kind,
        "description": f"{var['physical_role']} ({var['control_status']})",
        "epistemic_status": "conjectural" if var["independent_or_dependent"] != "independent" else "established",
        "evidence_paths": var["source_artifacts"],
    }


def node_from_regime(reg: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": reg["id"],
        "label": reg["name"],
        "node_type": "regime",
        "description": f"{reg['scale_range']}; transition: {reg['transition_conditions']}",
        "epistemic_status": "established",
        "evidence_paths": ["agentic/spec/qualitative_physics_relation_packet.schema.json"],
    }


def edge_from_relation(rel: dict[str, Any], packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": rel["id"],
        "source": rel["source_variable"],
        "target": rel["target_variable"],
        "edge_type": rel["relation_kind"],
        "direction": rel["direction"],
        "sign": "negative" if rel["relation_kind"] == "decreases" else "positive" if rel["relation_kind"] == "increases" else "conditional",
        "strength": "conditional",
        "linearity": rel["qualitative_rate"],
        "qualitative_behavior": (
            f"{rel['direction']}. Rate/regime character: {rel['qualitative_rate']}. "
            f"Convergence behavior: {rel['convergence_behavior']}"
        ),
        "validity_regime": rel["valid_regime_ids"],
        "assumptions": rel["assumptions"],
        "failure_modes": rel["failure_modes"],
        "evidence_paths": rel["evidence_paths"],
        "epistemic_status": rel["epistemic_status"],
        "originating_cycle_ids": [path.rsplit("/", 1)[-1].replace(".json", "") for path in rel["evidence_paths"] if "cycle-" in path] or [packet["packet_id"]],
    }


def build_graph(target_id: str, packets: list[dict[str, Any]]) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: dict[str, dict[str, Any]] = {}
    updates = []
    for packet in packets:
        for var in packet["variables"]:
            nodes[var["id"]] = node_from_variable(var)
        for reg in packet["regimes"]:
            nodes[reg["id"]] = node_from_regime(reg)
        for rel in packet["relations"]:
            edge = edge_from_relation(rel, packet)
            edges[edge["id"]] = edge
            updates.append(
                {
                    "id": stable_id("qpr.update", edge["id"], packet["packet_id"]),
                    "action": "add_edge" if edge["epistemic_status"] in {"conjectural", "established", "validated_probe"} else "challenge_edge",
                    "edge_id": edge["id"],
                    "packet_id": packet["packet_id"],
                    "created_utc": packet["created_utc"],
                }
            )
    gedanken_report = load_optional_json(GEDANKEN_REPORT)
    gedanken_packets = [row for row in gedanken_report.get("packets", []) if isinstance(row, dict)]
    for packet in gedanken_packets:
        packet_id = clean_text(packet.get("packet_id"))
        transfer = packet.get("transfer_scope", {}) if isinstance(packet.get("transfer_scope"), dict) else {}
        update_action = clean_text(packet.get("graph_update_action")) or "none"
        if update_action in {"none", "quarantine"}:
            continue
        for graph_update in packet.get("proposed_graph_updates", []):
            if not isinstance(graph_update, dict):
                continue
            edge_id = clean_text(graph_update.get("edge_id"))
            if not edge_id or edge_id not in edges:
                continue
            edge = edges[edge_id]
            edge.setdefault("gedanken_packet_ids", [])
            if packet_id and packet_id not in edge["gedanken_packet_ids"]:
                edge["gedanken_packet_ids"].append(packet_id)
            edge.setdefault("gedanken_transfer_scopes", [])
            edge["gedanken_transfer_scopes"].append(
                {
                    "packet_id": packet_id,
                    "transfer_verdict": transfer.get("transfer_verdict", "unknown"),
                    "transfers": transfer.get("transfers", ""),
                    "does_not_transfer": transfer.get("does_not_transfer", ""),
                    "transfer_certificate_needed": transfer.get("transfer_certificate_needed", ""),
                }
            )
            edge["evidence_paths"] = sorted(set(edge.get("evidence_paths", []) + packet.get("source_artifacts", [])))
            edge["failure_modes"] = sorted(set(edge.get("failure_modes", []) + packet.get("failure_modes", [])[:2]))
            updates.append(
                {
                    "id": stable_id("qpr.gedanken.update", edge_id, packet_id),
                    "action": update_action,
                    "edge_id": edge_id,
                    "packet_id": packet_id,
                    "epistemic_status": "conceptual_probe",
                    "transfer_verdict": transfer.get("transfer_verdict", "unknown"),
                    "created_utc": packet.get("created_utc", utc_now()),
                }
            )
    symbolic = load_optional_json(SYMBOLIC_MATRIX_PROBE)
    obligations = load_optional_json(ANALYTIC_OBLIGATIONS)
    finite_interfaces = load_optional_json(FINITE_ALGEBRA_INTERFACES)
    if symbolic:
        symbolic_path = "agentic/reports/symbolic_matrix_probe/latest.json"
        nodes.setdefault(
            "var.finite_quotient_matrix_Q",
            {
                "id": "var.finite_quotient_matrix_Q",
                "label": "finite normalized quotient matrix Q",
                "node_type": "symbolic_carrier",
                "description": "PMP symbolic formula carrier for determinant, principal minors, and quotient holonomy.",
                "epistemic_status": "symbolic_formula",
                "evidence_paths": [symbolic_path],
            },
        )
        edges["rel-symbolic-quotient-determinant"] = {
            "id": "rel-symbolic-quotient-determinant",
            "source": "var.quotient_phase_phi",
            "target": "var.finite_quotient_matrix_Q",
            "edge_type": "constrains",
            "direction": "The quotient holonomy Phi enters det(Q) through cos(Phi), so phase control can decide finite-family positivity.",
            "sign": "conditional",
            "strength": "exact finite algebra",
            "linearity": "trigonometric in Phi and multilinear in rho12 rho23 rho13",
            "qualitative_behavior": "Symbolic_formula: det(Q)=1-rho12^2-rho23^2-rho13^2+2 rho12 rho23 rho13 cos(Phi). This controls a finite matrix interface, not Yang-Mills proof status.",
            "validity_regime": ["reg.collar_collapse"],
            "assumptions": symbolic.get("probe_decision", {}).get("carrier", {}).get("validity_conditions", []),
            "failure_modes": [item.get("condition", "") for item in symbolic.get("falsifier_templates", [])],
            "evidence_paths": [symbolic_path],
            "epistemic_status": "symbolic_formula",
            "originating_cycle_ids": symbolic.get("source_cycle_ids", []),
        }
        updates.append(
            {
                "id": stable_id("qpr.pmp.symbolic", symbolic.get("generated_utc", "")),
                "action": "add_symbolic_formula_edge",
                "edge_id": "rel-symbolic-quotient-determinant",
                "packet_id": "pmp.symbolic_matrix_probe",
                "epistemic_status": "symbolic_formula",
                "created_utc": symbolic.get("generated_utc", utc_now()),
            }
        )
    if obligations:
        obligation_path = "agentic/reports/analytic_estimate_obligations/latest.json"
        nodes.setdefault(
            "var.analytic_estimate_obligations",
            {
                "id": "var.analytic_estimate_obligations",
                "label": "PMP analytic estimate obligations",
                "node_type": "obligation_set",
                "description": "Formula-derived Yang-Mills analytic obligations: boundary OPE, contacts, quotient phase, modulus positivity, and same-theory realization.",
                "epistemic_status": "analytic_obligation",
                "evidence_paths": [obligation_path],
            },
        )
        edges["rel-symbolic-formula-to-analytic-obligations"] = {
            "id": "rel-symbolic-formula-to-analytic-obligations",
            "source": "var.finite_quotient_matrix_Q",
            "target": "var.analytic_estimate_obligations",
            "edge_type": "induces",
            "direction": "Exact finite algebra induces proof-relevant analytic estimates before any bounded numeric search is allowed.",
            "sign": "conditional",
            "strength": "workflow-control",
            "linearity": "not numeric",
            "qualitative_behavior": "Analytic_obligation: the determinant and holonomy formulas become boundary OPE, additive contact, quotient phase, modulus PSD, and same-theory realization targets.",
            "validity_regime": ["reg.continuum_transfer", "reg.collar_collapse"],
            "assumptions": ["Finite symbolic identities are valid.", "Proof status remains blocked until same-theory analytic transfer is certified."],
            "failure_modes": [item.get("what_would_falsify_it", "") for item in obligations.get("obligations", [])[:4]],
            "evidence_paths": [obligation_path],
            "epistemic_status": "analytic_obligation",
            "originating_cycle_ids": obligations.get("source_cycle_ids", []),
        }
        updates.append(
            {
                "id": stable_id("qpr.pmp.obligation", obligations.get("generated_utc", "")),
                "action": "add_analytic_obligation_edge",
                "edge_id": "rel-symbolic-formula-to-analytic-obligations",
                "packet_id": "pmp.analytic_estimate_obligations",
                "epistemic_status": "analytic_obligation",
                "created_utc": obligations.get("generated_utc", utc_now()),
            }
        )
    packets_finite = finite_interfaces.get("packets", []) if isinstance(finite_interfaces.get("packets"), list) else []
    if packets_finite:
        packet = packets_finite[0]
        finite_path = "agentic/reports/finite_algebra_interfaces/latest.json"
        nodes.setdefault(
            "var.equational_interface_packet",
            {
                "id": "var.equational_interface_packet",
                "label": "ESR finite algebra interface packet",
                "node_type": "symbolic_carrier",
                "description": "Non-Lean equational interface containing exact identities, side conditions, falsifier shapes, and analytic obligations.",
                "epistemic_status": "equational_interface",
                "evidence_paths": [finite_path],
            },
        )
        nodes.setdefault(
            "var.side_condition_ledger",
            {
                "id": "var.side_condition_ledger",
                "label": "finite algebra side-condition ledger",
                "node_type": "side_condition_ledger",
                "description": "Hermitian, normalized, nonzero quotient, phase convention, and finite-family assumptions required before formulas are valid.",
                "epistemic_status": "side_condition_ledger",
                "evidence_paths": [finite_path],
            },
        )
        edges["rel-equational-interface-to-side-conditions"] = {
            "id": "rel-equational-interface-to-side-conditions",
            "source": "var.equational_interface_packet",
            "target": "var.side_condition_ledger",
            "edge_type": "constrains",
            "direction": "Every exact identity is valid only under the side-condition ledger; failing a side condition backtracks the branch before analytic promotion.",
            "sign": "conditional",
            "strength": "deterministic validation",
            "linearity": "not numeric",
            "qualitative_behavior": "Side_condition_ledger: Hermitian normalization, nonzero quotient entries, phase convention, and finite-family scope decide whether the determinant and holonomy formulas apply.",
            "validity_regime": ["reg.collar_collapse", "reg.continuum_transfer"],
            "assumptions": [item.get("condition", "") for item in packet.get("side_conditions", [])],
            "failure_modes": [item.get("failure_effect", "") for item in packet.get("side_conditions", [])],
            "evidence_paths": [finite_path],
            "epistemic_status": "side_condition_ledger",
            "originating_cycle_ids": packet.get("source_cycle_ids", []),
        }
        edges["rel-finite-interface-falsifier-shapes"] = {
            "id": "rel-finite-interface-falsifier-shapes",
            "source": "var.equational_interface_packet",
            "target": "var.reflection_gram_N",
            "edge_type": "falsifies",
            "direction": "Formula-derived falsifier shapes can demote pairwise-positivity, phase-removal, or modulus-only transfer branches.",
            "sign": "negative",
            "strength": "formula-derived branch control",
            "linearity": "determinant and holonomy conditions",
            "qualitative_behavior": "Falsifier_shape: negative determinant with pairwise minors passing, nonzero cycle holonomy, negative modulus quotient minor, or nonzero additive contact prevents naive positivity transfer.",
            "validity_regime": ["reg.collar_collapse"],
            "assumptions": ["finite interface packet validates", "falsifier preserves the same carrier side conditions except for the changed condition"],
            "failure_modes": [item.get("disconfirming_observation", "") for item in packet.get("falsifier_templates", [])],
            "evidence_paths": [finite_path],
            "epistemic_status": "falsifier_shape",
            "originating_cycle_ids": packet.get("source_cycle_ids", []),
        }
        updates.extend(
            [
                {
                    "id": stable_id("qpr.esr.interface", packet.get("packet_id", "")),
                    "action": "add_equational_interface_node",
                    "edge_id": "rel-equational-interface-to-side-conditions",
                    "packet_id": packet.get("packet_id", "esr.interface"),
                    "epistemic_status": "equational_interface",
                    "created_utc": finite_interfaces.get("generated_utc", utc_now()),
                },
                {
                    "id": stable_id("qpr.esr.falsifier", packet.get("packet_id", "")),
                    "action": "add_falsifier_shape_edge",
                    "edge_id": "rel-finite-interface-falsifier-shapes",
                    "packet_id": packet.get("packet_id", "esr.interface"),
                    "epistemic_status": "falsifier_shape",
                    "created_utc": finite_interfaces.get("generated_utc", utc_now()),
                },
            ]
        )
    status_counts = Counter(edge["epistemic_status"] for edge in edges.values())
    graph = {
        "version": 1,
        "target_id": target_id,
        "generated_utc": utc_now(),
        "source_artifacts": [path for packet in packets for path in packet["source_artifacts"]],
        "source_cycle_ids": sorted(
            {
                path.rsplit("/", 1)[-1].replace(".json", "")
                for packet in packets
                for path in packet["source_artifacts"]
                if "cycle-" in path
            }
        ),
        "nodes": sorted(nodes.values(), key=lambda row: row["id"]),
        "edges": sorted(edges.values(), key=lambda row: row["id"]),
        "updates": updates,
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "relation_packet_count": len(packets),
            "status_counts": dict(status_counts),
            "relation_kinds": dict(Counter(edge["edge_type"] for edge in edges.values())),
            "gedanken_link_count": sum(len(edge.get("gedanken_packet_ids", [])) for edge in edges.values()),
        },
        "validation_handoff": "python agentic/scripts/validate_qualitative_mechanistic_graph.py",
    }
    return graph


def render_markdown(graph: dict[str, Any]) -> str:
    lines = [
        "# Qualitative Mechanistic Graph",
        "",
        f"- Target: `{graph['target_id']}`",
        f"- Nodes: `{graph['summary']['node_count']}`",
        f"- Edges: `{graph['summary']['edge_count']}`",
        f"- Status counts: `{graph['summary']['status_counts']}`",
        "",
        "## Relation Edges",
        "",
    ]
    for edge in graph["edges"]:
        lines.append(f"### {edge['id']}")
        lines.append(f"- `{edge['source']}` --{edge['edge_type']}--> `{edge['target']}`")
        lines.append(f"- Direction: {edge['direction']}")
        lines.append(f"- Regime: `{', '.join(edge['validity_regime'])}`")
        lines.append(f"- Epistemic status: `{edge['epistemic_status']}`")
        lines.append(f"- Failure modes: {'; '.join(edge['failure_modes'])}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="yang-mills-existence-and-mass-gap-target")
    args = parser.parse_args()
    _, run_state = load_run_state()
    cycles = [cycle for cycle in load_cycles(run_state) if cycle.get("valid_as_research_cycle")] if run_state else []
    run_id = run_state.get("run_id", "unknown-run") if run_state else "unknown-run"
    packets = build_packets(args.target, cycles, run_id)
    graph = build_graph(args.target, packets)
    write_json(PACKET_OUT, {"version": 1, "packets": packets})
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    graph_path = GRAPH_DIR / f"{args.target}.json"
    write_json(graph_path, graph)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render_markdown(graph), encoding="utf-8")
    print(f"Wrote {PACKET_OUT.relative_to(ROOT)}")
    print(f"Wrote {graph_path.relative_to(ROOT)}")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
