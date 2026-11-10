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

"""Build Abducer's Hegelian-inspired hypothesis exploration artifacts.

The script is deliberately deterministic. The creative layer is represented as
typed candidate transformations over existing Abducer artifacts; generative
skills may author richer candidates later, but every candidate must fit the same
map, validation, ranking, graph, log, and release contracts.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, kb_ref_from_path, load_json_object, rel, repo_path, stable_id, utc_now, write_json
from abstraction_machinery_selection import POLICY as ABSTRACTION_MACHINERY_POLICY
from abstraction_machinery_selection import machinery_selection_for_candidate, summarize_machinery_portfolio, target_contract_from_ledger
from formal_subgoal_control import POLICY as FORMAL_SUBGOAL_CONTROL_POLICY
from formal_subgoal_control import subgoal_control_for_candidate


GRAPH_STATUSES_FAILURE = {"blocked", "missing-premise", "proof-debt"}
DISCOVERY_KINDS = {"bridge-plan", "conjecture", "connector_bridge", "intervention", "pathway", "proof-sketch"}
GENERATED_HEGELIAN_KINDS = {"conceptual_pressure", "creative_candidate", "validation_obligation"}
DISPOSITIONS = {"proof_queue", "discovery_branch", "revision_loop", "evidence_task", "quarantine", "reject", "stop"}
HARD_GATES = [
    "preservation",
    "target_activation",
    "non_collapse",
    "barrier_compatibility",
    "source_grounding",
    "proof_queue_readiness",
]

TARGET_COMMITMENTS = [
    "main-conjecture",
    "complexity-separation",
    "nonrelativizing-barrier",
    "proof-object-adequacy",
]
YANG_MILLS_COMMITMENT_TERMS = {
    "existence": [
        "constructive",
        "construction",
        "existence",
        "rigorous yang mills",
        "schwinger functions",
        "wightman qft",
    ],
    "nontriviality": [
        "nontrivial",
        "positive mass gap",
        "gauge",
        "yang mills",
        "interacting",
    ],
    "os-wightman-adequacy": [
        "os axioms",
        "osterwalder schrader",
        "wightman",
        "reflection positivity",
        "transfer matrix",
        "schwinger",
    ],
    "continuum-limit": [
        "continuum",
        "lattice continuum",
        "ultraviolet",
        "cutoff",
        "balaban",
        "renormalisation",
        "renormalization",
        "wilson",
    ],
    "positive-mass-gap": [
        "mass gap",
        "spectral gap",
        "hamiltonian",
        "exponential decay",
        "correlator decay",
        "transfer matrix",
        "positive self adjoint",
    ],
}
YANG_MILLS_ROUTE_TERMS = [
    "reflection positivity",
    "transfer matrix",
    "continuum limit",
    "lattice continuum",
    "os reconstruction",
    "wightman",
    "schwinger",
    "mass gap",
    "spectral gap",
    "hamiltonian",
    "exponential decay",
    "correlator decay",
    "balaban",
    "renormalisation",
    "renormalization",
    "infrared cutoff",
    "ultraviolet cutoff",
    "constructive qft",
    "wilson",
]


def normalized_text(*values: Any) -> str:
    raw = " ".join(clean_text(value) for value in values if value is not None)
    return re.sub(r"[^a-z0-9]+", " ", raw.lower()).strip()


def term_hits(text: str, terms: list[str]) -> list[str]:
    padded = f" {text} "
    hits = []
    for term in terms:
        needle = f" {normalized_text(term)} "
        if needle in padded:
            hits.append(term)
    return hits


def yang_mills_profile(*values: Any) -> dict[str, Any]:
    text = normalized_text(*values)
    route_terms = term_hits(text, YANG_MILLS_ROUTE_TERMS)
    commitments = []
    for commitment_id, terms in YANG_MILLS_COMMITMENT_TERMS.items():
        if term_hits(text, terms):
            commitments.append(commitment_id)
    score = min(
        1.0,
        round((len(route_terms) * 0.09) + (len(commitments) * 0.14), 2),
    )
    proof_queue_signature = (
        "positive-mass-gap" in commitments
        and (
            "os-wightman-adequacy" in commitments
            or "continuum-limit" in commitments
            or any(term in route_terms for term in ["balaban", "renormalisation", "renormalization"])
        )
    )
    return {
        "score": score,
        "route_terms": route_terms,
        "commitment_ids": commitments,
        "proof_queue_signature": proof_queue_signature,
    }


def readable_node_id(node_id: str) -> str:
    text = re.sub(r"^(statement|intervention|hypothesis|target|candidate|pressure):", "", node_id)
    text = text.replace("st.thm.", "").replace("st.def.", "").replace("st.rem.", "").replace("st.prob.", "")
    text = re.sub(r"[^A-Za-z0-9]+", " ", text)
    return clean_text(text).strip() or node_id


def yang_mills_route_blueprint(packet: dict[str, Any], operation: str, profile: dict[str, Any]) -> dict[str, Any]:
    terms = set(profile.get("route_terms", []))
    commitments = set(profile.get("commitment_ids", []))
    source = readable_node_id(str(packet.get("source_node_id", "")))
    witness = clean_text(packet.get("witness"))

    if {"balaban", "renormalisation"} & terms or {"balaban", "renormalization"} & terms:
        family = "Balaban RG continuum-control route"
        strategy = (
            "Test the Balaban renormalisation-group mechanism: scale-by-scale control of regulated non-Abelian gauge fields must "
            "survive ultraviolet cutoff removal as a non-Gaussian, OS-positive continuum Yang-Mills object, and that same object "
            "must still supply a gauge-invariant spectral witness for the mass gap."
        )
        gate_requirements = {
            "preservation": "Preserve compact simple gauge-group Yang-Mills structure through the RG block-spin/effective-action construction.",
            "target_activation": "Name the exact Balaban estimates that would produce constructive existence rather than only small-field or cutoff control.",
            "non_collapse": "Show that the limiting measure is interacting and non-Gaussian, not a trivial ultraviolet fixed point.",
            "barrier_compatibility": "Explain how ultraviolet stability plus effective-action convergence addresses the four-dimensional continuum-limit bottleneck.",
            "source_grounding": "Cite the Balaban RG artifact and the KB statements linking RG control to constructive Yang-Mills existence.",
            "proof_queue_readiness": "Split the route into RG stability, cutoff removal, OS positivity, nontriviality, and spectral-gap sublemmas.",
        }
        obligations = [
            "RG stability lemma: formulate the uniform effective-action bounds needed across scales for compact simple gauge group G.",
            "Continuum passage lemma: prove the RG-controlled lattice/regulated measures have a subsequential OS-positive Schwinger-function limit.",
            "Nontriviality lemma: identify a gauge-invariant observable whose limiting correlations do not collapse to a Gaussian/free theory.",
            "Mass-gap witness lemma: extract exponential decay or a Hamiltonian spectral lower bound stable under the continuum limit.",
        ]
        failure_tests = [
            "Demote if the argument only controls a finite-volume or infrared-cutoff theory.",
            "Demote if the RG estimates do not connect to OS/Wightman reconstruction.",
        ]
    elif "correlator decay" in terms or ("transfer matrix" in terms and "mass gap" in terms):
        family = "Euclidean correlator-decay to spectral-gap route"
        strategy = (
            "Test the Euclidean spectral mechanism: gauge-invariant Schwinger-function correlations must decay with cutoff-uniform "
            "rates, reflection positivity must reconstruct the physical Hilbert space, and the corresponding spectral measures "
            "must have support bounded away from zero in the vacuum-orthogonal sector."
        )
        gate_requirements = {
            "preservation": "Preserve the Clay target by keeping OS/Wightman reconstruction, nontriviality, continuum limit, and Delta > 0 explicit.",
            "target_activation": "Specify which Schwinger functions or gauge-invariant local observables witness exponential Euclidean time decay.",
            "non_collapse": "Show the decay statement is not a strong-coupling lattice-only artifact and survives as a nontrivial continuum theory.",
            "barrier_compatibility": "State the cutoff-uniform estimates needed before the transfer-matrix gap can pass to the continuum limit.",
            "source_grounding": "Cite the correlator-decay, reflection-positivity, transfer-matrix, and mass-gap KB evidence.",
            "proof_queue_readiness": "Split the route into reflection positivity, transfer-matrix construction, decay estimate, OS reconstruction, and spectral-gap transfer.",
        }
        obligations = [
            "Reflection-positivity lemma: verify the Euclidean objects used in the route satisfy OS positivity after the limiting procedure.",
            "Transfer-matrix lemma: construct the Hilbert space and positive self-adjoint transfer matrix/Hamiltonian from the OS-positive data.",
            "Decay-to-gap lemma: prove that exponential decay of selected gauge-invariant correlations implies a positive spectral gap above the vacuum.",
            "Uniformity lemma: make the decay constants stable under lattice-spacing and cutoff removal.",
        ]
        failure_tests = [
            "Demote if exponential decay is available only at fixed lattice spacing or strong coupling without continuum transfer.",
            "Demote if the selected observables do not control the physical Hamiltonian spectrum.",
        ]
    elif "reflection positivity" in terms or "os reconstruction" in terms:
        family = "OS reconstruction and reflection-positivity bridge"
        strategy = (
            "Use OS reconstruction as the kinematic bridge: produce reflection-positive Yang-Mills Schwinger functions, reconstruct "
            "Wightman fields and Hamiltonian time evolution, then ask whether a same-theory gauge-invariant spectral witness "
            "excludes arbitrarily light excitations."
        )
        gate_requirements = {
            "preservation": "Keep OS/Wightman adequacy as an explicit construction target rather than a post-hoc interpretation.",
            "target_activation": "Name the Schwinger-function family and reconstruction theorem obligations needed for Yang-Mills on R^4.",
            "non_collapse": "Track nontriviality of the reconstructed field algebra and vacuum sector.",
            "barrier_compatibility": "Show the Schwinger functions arise after the four-dimensional continuum limit, not only from a regulated model.",
            "source_grounding": "Cite OS reconstruction, reflection positivity, and Wightman QFT artifacts from the KB and connection analysis.",
            "proof_queue_readiness": "Split into OS axioms, reconstruction, Hamiltonian spectrum, and mass-gap-witness sublemmas.",
        }
        obligations = [
            "Schwinger-function construction lemma: define the candidate Euclidean n-point functions for Yang-Mills observables.",
            "OS-axiom lemma: prove Euclidean invariance, symmetry, reflection positivity, regularity, and clustering/analyticity as needed.",
            "Reconstruction lemma: recover Wightman fields and a positive-energy Hamiltonian from the OS data.",
            "Gap-attachment lemma: connect the reconstructed Hamiltonian to a positive mass-gap witness.",
        ]
        failure_tests = [
            "Demote if OS positivity is asserted only for a finite lattice theory.",
            "Demote if the mass-gap claim is not attached to the reconstructed Hamiltonian.",
        ]
    elif "wightman" in terms or "constructive qft" in terms:
        family = "Constructive QFT existence route"
        strategy = (
            "Use constructive-QFT methods to build the actual four-dimensional Yang-Mills object: define the Schwinger/Wightman "
            "data, prove that the gauge-invariant vacuum sector is nontrivial, and keep the infrared spectral-gap mechanism "
            "as an additional dynamical burden rather than a consequence of existence alone."
        )
        gate_requirements = {
            "preservation": "Preserve the full Clay target: existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap.",
            "target_activation": "Specify the constructive object being built: measure, Schwinger functions, fields, or Hamiltonian representation.",
            "non_collapse": "Provide a non-Gaussian/non-empty observable witness for the constructed theory.",
            "barrier_compatibility": "Separate low-dimensional or cutoff constructive evidence from the required four-dimensional continuum construction.",
            "source_grounding": "Cite constructive-QFT and Wightman evidence from the KB and source artifacts.",
            "proof_queue_readiness": "Split into construction, axiom verification, nontriviality, continuum, and mass-gap sublemmas.",
        }
        obligations = [
            "Construction lemma: define the nonperturbative Yang-Mills object to be constructed.",
            "Axiom-verification lemma: prove the OS/Wightman properties required by the target.",
            "Nontriviality witness lemma: identify observables or correlations ruling out collapse to a trivial theory.",
            "Mass-gap separation lemma: isolate the spectral gap proof from the existence proof.",
        ]
        failure_tests = [
            "Demote if the route imports low-dimensional constructive QFT without a transfer proof.",
            "Demote if existence is proved without a positive-gap mechanism.",
        ]
    elif "hamiltonian" in terms or "spectral gap" in terms or "mass gap" in terms:
        family = "Hamiltonian spectral-gap route"
        strategy = (
            "Use the Hamiltonian formulation as the endpoint check: after the physical Hilbert space, vacuum, and time-translation "
            "generator are reconstructed from the same continuum Yang-Mills data, prove that vacuum-orthogonal excitations have "
            "energy at least a strictly positive Delta."
        )
        gate_requirements = {
            "preservation": "Preserve the constructed Yang-Mills theory while moving to Hamiltonian spectral language.",
            "target_activation": "Name the Hamiltonian, vacuum sector, and excitation subspace for the reconstructed theory.",
            "non_collapse": "Show the spectral gap belongs to a nontrivial interacting theory.",
            "barrier_compatibility": "Explain how the Hamiltonian is obtained after continuum/OS reconstruction rather than at fixed cutoff.",
            "source_grounding": "Cite the mass-gap and Hamiltonian-Wightman definitions plus any transfer-matrix evidence.",
            "proof_queue_readiness": "Split into Hilbert-space construction, vacuum uniqueness/isolation, excitation spectrum, and positive lower-bound sublemmas.",
        }
        obligations = [
            "Hamiltonian construction lemma: define H as the time-translation generator of the reconstructed theory.",
            "Vacuum isolation lemma: identify the vacuum and prove it is separated from non-vacuum states.",
            "Spectral lower-bound lemma: prove inf spec(H on vacuum-orthogonal sector) >= Delta for some Delta > 0.",
            "Continuum compatibility lemma: show the spectral bound survives the limiting construction.",
        ]
        failure_tests = [
            "Demote if the Hamiltonian exists only for a regulated transfer matrix.",
            "Demote if the gap is numerical/heuristic rather than a rigorous spectral lower bound.",
        ]
    else:
        family = "Yang-Mills target-control route"
        strategy = (
            f"Refine `{source}` into explicit Yang-Mills obligations by naming the construction object, the axiom bridge, "
            "the continuum-limit step, the nontriviality witness, and the positive mass-gap mechanism."
        )
        gate_requirements = {
            gate: f"State the {gate.replace('_', ' ')} obligation using Yang-Mills construction, OS/Wightman adequacy, continuum limit, and Delta > 0."
            for gate in HARD_GATES
        }
        obligations = [
            "Construction-object lemma: name the mathematical Yang-Mills object being built.",
            "Axiom bridge lemma: identify the OS/Wightman condition used by the route.",
            "Continuum-limit lemma: state the cutoff-removal or limiting argument.",
            "Mass-gap lemma: state the rigorous positive-gap witness.",
        ]
        failure_tests = ["Demote if the route cannot name its construction object, continuum step, and mass-gap witness."]

    return {
        "route_family": family,
        "source_label": source,
        "strategy": strategy,
        "gate_requirements": gate_requirements,
        "proof_obligations": obligations,
        "failure_tests": failure_tests,
        "source_witness": witness,
        "commitment_ids": list(commitments),
        "route_terms": list(terms),
        "derivation_artifacts": (
            [
                "agentic/reports/hamiltonian_gap_derivation/latest.html",
                "agentic/reports/hamiltonian_gap_derivation/latest.md",
                "agentic/reports/hamiltonian_gap_derivation/latest.json",
            ]
            if family == "Hamiltonian spectral-gap route"
            else []
        ),
    }


def load_operations() -> list[dict[str, Any]]:
    return load_json_object(ROOT / "agentic/spec/conceptual_creativity_operations.schema.json")["operations"]


def operation_by_id() -> dict[str, dict[str, Any]]:
    return {row["id"]: row for row in load_operations()}


def node_evidence(node: dict[str, Any]) -> list[str]:
    evidence = [str(item) for item in node.get("evidence_paths", []) if str(item).strip()]
    source = clean_text(node.get("source_artifact"))
    if source and source not in evidence:
        evidence.append(source)
    return list(dict.fromkeys(evidence))


def pressure_type_for(node: dict[str, Any]) -> str:
    status = clean_text(node.get("status"))
    kind = clean_text(node.get("kind"))
    if status in {"blocked", "missing-premise"}:
        return "failure"
    if kind in DISCOVERY_KINDS or status in {"bridge-obligation", "route-lemma"}:
        return "discovery_signal"
    if status == "proof-debt":
        return "open_question"
    return "opportunity"


def pressure_severity(node: dict[str, Any], pressure_type: str) -> str:
    if pressure_type == "failure":
        return "high"
    if node.get("kind") in {"proof_obligation", "proof_queue_entry"}:
        return "medium"
    if pressure_type == "discovery_signal":
        return "medium"
    return "low"


def build_pressure_packets(graph: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    packets: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    signals: list[dict[str, Any]] = []
    seen_nodes: set[str] = set()
    frontier_ids = [row.get("id") for row in graph.get("frontier", []) if isinstance(row, dict)]
    selected = []
    by_id = {node["id"]: node for node in graph.get("nodes", []) if isinstance(node, dict) and "id" in node}
    for node_id in frontier_ids:
        node = by_id.get(node_id)
        if node and node.get("kind") not in GENERATED_HEGELIAN_KINDS:
            selected.append(node)
            seen_nodes.add(node_id)
    for node in graph.get("nodes", []):
        if not isinstance(node, dict) or node.get("id") in seen_nodes:
            continue
        if node.get("kind") in GENERATED_HEGELIAN_KINDS:
            continue
        if node.get("kind") in DISCOVERY_KINDS or node.get("status") in GRAPH_STATUSES_FAILURE:
            selected.append(node)
            seen_nodes.add(node["id"])
    for node in selected[:160]:
        ptype = pressure_type_for(node)
        evidence = node_evidence(node)
        pid = stable_id("pressure", graph.get("target_id"), node["id"], ptype)
        label = clean_text(node.get("label")) or node["id"]
        next_action = clean_text(node.get("next_action") or node.get("blocker"))
        hooks = []
        if ptype == "failure":
            hooks = ["negative_route_inversion", "proof_obligation_factorization", "representation_shift"]
        elif node.get("kind") in {"bridge-plan", "connector_bridge", "intervention"}:
            hooks = ["bridge_invention", "analogy_transport", "carrier_introduction"]
        elif node.get("kind") in {"conjecture", "pathway"}:
            hooks = ["abstraction_formation", "regime_restriction", "theorem_weakening"]
        else:
            hooks = ["proof_obligation_factorization", "theorem_weakening", "evidence_task"]
        packet = {
            "pressure_id": pid,
            "pressure_type": ptype,
            "source_node_id": node["id"],
            "source_node_kind": node.get("kind", ""),
            "source_node_status": node.get("status", ""),
            "source_artifacts": evidence,
            "witness": label,
            "severity": pressure_severity(node, ptype),
            "repair_target": next_action or f"Clarify route role for {node['id']}",
            "unknowns": [
                "Which obligations are mathematically dischargeable?",
                "Which source evidence is sufficient for promotion?"
            ],
            "candidate_successor_hooks": hooks,
        }
        packets.append(packet)
        if ptype == "failure":
            failures.append(
                {
                    "certificate_id": stable_id("failure", pid),
                    "pressure_id": pid,
                    "failed_obligation": packet["repair_target"],
                    "witness": packet["witness"],
                    "severity": packet["severity"],
                    "repair_target": packet["repair_target"],
                    "unknowns": packet["unknowns"],
                    "candidate_successor_hooks": packet["candidate_successor_hooks"],
                    "source_artifacts": evidence,
                }
            )
        elif ptype in {"discovery_signal", "opportunity"}:
            signals.append(
                {
                    "signal_id": stable_id("signal", pid),
                    "pressure_id": pid,
                    "pattern_evidence": packet["witness"],
                    "source_artifacts": evidence,
                    "confidence": "medium" if evidence else "low",
                    "disconfirming_observations": [
                        "Semantic proximity may not imply proof transport.",
                        "A repeated route shape may collapse under missing assumptions."
                    ],
                    "candidate_successor_hooks": packet["candidate_successor_hooks"],
                }
            )
    return packets, failures, signals


def choose_operation(packet: dict[str, Any], index: int) -> str:
    if str(packet.get("source_node_id", "")).startswith("target:"):
        return "theorem_weakening"
    profile = yang_mills_profile(packet.get("source_node_id"), packet.get("witness"), packet.get("repair_target"))
    if (
        profile["proof_queue_signature"]
        and packet["pressure_type"] in {"discovery_signal", "open_question", "opportunity"}
        and not str(packet.get("source_node_id", "")).startswith("target:")
    ):
        return "proof_obligation_factorization"
    hooks = [hook for hook in packet.get("candidate_successor_hooks", []) if hook != "evidence_task"]
    if not hooks:
        hooks = ["proof_obligation_factorization"]
    if packet["pressure_type"] == "failure":
        return hooks[index % len(hooks)]
    if packet["source_node_kind"] == "proof_queue_entry":
        return "theorem_weakening"
    return hooks[index % len(hooks)]


def candidate_text(operation: str, packet: dict[str, Any], blueprint: dict[str, Any] | None = None) -> str:
    witness = packet["witness"]
    if blueprint and blueprint.get("route_family"):
        if operation == "proof_obligation_factorization":
            return blueprint["strategy"]
        if operation == "bridge_invention":
            return f"State the {blueprint['route_family']} bridge object for `{packet['source_node_id']}` by naming its Yang-Mills source data, target object, and transfer theorem: {blueprint['strategy']}"
        if operation == "carrier_introduction":
            return f"Name the mathematical carrier for the {blueprint['route_family']} such as a Schwinger family, observable algebra, spectral measure, or reconstructed Hamiltonian: {blueprint['strategy']}"
        if operation == "analogy_transport":
            return f"Use analogy only after identifying the exact Yang-Mills mismatch in dimension, cutoff, gauge group, observable sector, and continuum transfer: {blueprint['strategy']}"
        if operation == "theorem_weakening":
            return f"Use a bounded {blueprint['route_family']} endpoint claim only after stating which reconstructed Yang-Mills objects and observables make it meaningful: {blueprint['strategy']}"
    if operation == "bridge_invention":
        return f"Introduce a mediator that preserves the commitments in `{packet['source_node_id']}` while connecting the blocked route to the target frontier: {witness}"
    if operation == "abstraction_formation":
        return f"Compress the repeated route pressure around `{packet['source_node_id']}` into an abstraction with explicit coverage and excluded cases."
    if operation == "regime_restriction":
        return f"Restrict the active conjecture around `{packet['source_node_id']}` to the smallest regime where the current evidence can be tested."
    if operation == "theorem_weakening":
        return f"Weaken the theorem-shaped obligation at `{packet['source_node_id']}` into a successor claim that preserves target relevance."
    if operation == "theorem_strengthening":
        return f"Strengthen the route at `{packet['source_node_id']}` only where an invariant can survive barrier and source checks."
    if operation == "carrier_introduction":
        return f"Introduce a carrier object for `{packet['source_node_id']}` that can transport structure across proof stages."
    if operation == "negative_route_inversion":
        return f"Turn the failure witness at `{packet['source_node_id']}` into a successor route that explains why the old route failed."
    if operation == "analogy_transport":
        return f"Transport the pattern near `{packet['source_node_id']}` from its source context only after mismatch inventory."
    if operation == "representation_shift":
        return f"Revise the local representation around `{packet['source_node_id']}` so the route can express the missing dependency explicitly."
    return f"Factor the obligation at `{packet['source_node_id']}` into named construction, bridge, evidence, and refutation tasks."


def build_candidates(packets: list[dict[str, Any]], operations: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidates: list[dict[str, Any]] = []
    analyses: list[dict[str, Any]] = []
    failures = [p for p in packets if p["pressure_type"] == "failure"]
    signals = [p for p in packets if p["pressure_type"] == "discovery_signal"]
    open_questions = [p for p in packets if p["pressure_type"] == "open_question"]
    opportunities = [p for p in packets if p["pressure_type"] == "opportunity"]
    candidate_sources = []
    for bucket in (failures[:5], signals[:7], open_questions[:3], opportunities[:3]):
        candidate_sources.extend(bucket)
    if len(candidate_sources) < 12:
        for packet in packets:
            if packet not in candidate_sources:
                candidate_sources.append(packet)
            if len(candidate_sources) >= 16:
                break
    candidate_sources = sorted(
        candidate_sources,
        key=lambda packet: (
            -yang_mills_profile(packet.get("source_node_id"), packet.get("witness"), packet.get("repair_target"))["score"],
            str(packet.get("source_node_id", "")).startswith("target:"),
            packet["pressure_type"] != "discovery_signal",
            packet["pressure_id"],
        ),
    )
    selected_sources = candidate_sources[:16]
    target_sources = [packet for packet in candidate_sources if str(packet.get("source_node_id", "")).startswith("target:")]
    if target_sources and all(not str(packet.get("source_node_id", "")).startswith("target:") for packet in selected_sources):
        selected_sources = selected_sources[:15] + [target_sources[0]]
    for index, packet in enumerate(selected_sources):
        operation = choose_operation(packet, index)
        op = operations[operation]
        candidate_id = stable_id("candidate", packet["pressure_id"], operation)
        validation_pressure = list(op.get("validation_pressure", []))
        profile = yang_mills_profile(packet.get("source_node_id"), packet.get("witness"), packet.get("repair_target"), operation)
        blueprint = (
            yang_mills_route_blueprint(packet, operation, profile)
            if profile.get("route_terms") or profile.get("commitment_ids")
            else {}
        )
        candidate = {
            "candidate_id": candidate_id,
            "source_pressure_ids": [packet["pressure_id"]],
            "creative_operation": operation,
            "creative_operation_label": op["label"],
            "affected_nodes": [packet["source_node_id"]],
            "proposed_transformation": candidate_text(operation, packet, blueprint),
            "source_witness": packet["witness"],
            "source_node_kind": packet.get("source_node_kind", ""),
            "source_node_status": packet.get("source_node_status", ""),
            "domain_specificity": profile,
            "route_blueprint": blueprint,
            "expected_route_value": {
                "target_relevance": "high" if profile["score"] >= 0.55 or packet["severity"] == "high" else "medium",
                "tractability": "medium" if operation in {"theorem_weakening", "proof_obligation_factorization", "regime_restriction"} else "uncertain",
                "novelty": "high" if operation in {"bridge_invention", "carrier_introduction", "representation_shift"} else "medium"
            },
            "disconfirming_observations": [
                "Candidate is demoted if source evidence is removed.",
                "Candidate is quarantined if hard obligations cannot be named."
            ] + list(blueprint.get("failure_tests", [])),
            "validation_requirements": validation_pressure,
            "source_artifacts": packet.get("source_artifacts", []),
            "epistemic_status": "conjectural",
        }
        candidates.append(candidate)
        analyses.append(
            {
                "candidate_id": candidate_id,
                "creative_operation": operation,
                "novelty_role": op["label"],
                "hypothesis_space_delta": {
                    "adds_nodes": [candidate_id],
                    "reframes_pressure": packet["pressure_id"],
                    "changed_possible_routes": ["proof_queue", "discovery_branch", "revision_loop", "quarantine"]
                },
                "controlled_by": ["validation_packet", "candidate_ranking", "looper_dependency_graph"],
                "validation_pressure": validation_pressure,
                "failure_modes": [
                    "Narrative plausibility without artifact grounding.",
                    "Hidden assumption shift.",
                    "Unstated loss of target relevance."
                ],
            }
        )
    return candidates, analyses


def gate_result(candidate: dict[str, Any], gate: str) -> str:
    op = candidate["creative_operation"]
    has_sources = bool(candidate.get("source_artifacts"))
    profile = candidate.get("domain_specificity", {})
    specificity = float(profile.get("score", 0.0))
    commitment_count = len(profile.get("commitment_ids", []))
    generic_target_rewrite = (
        op == "theorem_weakening"
        and any(str(node).startswith("target:") for node in candidate.get("affected_nodes", []))
        and specificity < 0.75
    )
    if gate == "source_grounding":
        return "pass" if has_sources else "fail"
    if gate == "target_activation":
        return "pass" if commitment_count >= 2 and not generic_target_rewrite else "warn"
    if gate == "proof_queue_readiness":
        if op in {"theorem_weakening", "proof_obligation_factorization"} and profile.get("proof_queue_signature") and not generic_target_rewrite:
            return "pass"
        return "warn"
    if gate == "barrier_compatibility":
        if "continuum-limit" in profile.get("commitment_ids", []) or any(term in profile.get("route_terms", []) for term in ["balaban", "renormalisation", "renormalization"]):
            return "pass"
        return "warn" if op in {"theorem_strengthening", "analogy_transport"} else "pass"
    if gate == "non_collapse":
        if "positive-mass-gap" in profile.get("commitment_ids", []) and commitment_count >= 3:
            return "pass"
        return "warn" if op in {"bridge_invention", "analogy_transport", "carrier_introduction"} else "pass"
    if gate == "preservation":
        if commitment_count >= 3:
            return "pass"
        return "warn" if op in {"representation_shift", "negative_route_inversion"} else "pass"
    return "pass"


def route_for(candidate: dict[str, Any], hard_gates: dict[str, str]) -> str:
    if "fail" in hard_gates.values():
        return "quarantine"
    op = candidate["creative_operation"]
    if op == "analogy_transport":
        return "evidence_task"
    if list(hard_gates.values()).count("warn") >= 2:
        return "revision_loop"
    if op in {"theorem_weakening", "proof_obligation_factorization"} and hard_gates["proof_queue_readiness"] == "pass":
        return "proof_queue"
    if op == "theorem_weakening":
        return "revision_loop"
    if op in {"representation_shift", "negative_route_inversion"}:
        return "revision_loop"
    if op in {"bridge_invention", "abstraction_formation", "carrier_introduction", "analogy_transport", "regime_restriction"}:
        return "discovery_branch"
    return "evidence_task"


def gate_requirement_for(candidate: dict[str, Any], gate: str) -> str:
    blueprint = candidate.get("route_blueprint", {})
    gate_requirements = blueprint.get("gate_requirements", {})
    if isinstance(gate_requirements, dict) and clean_text(gate_requirements.get(gate)):
        return clean_text(gate_requirements[gate])
    source = ", ".join(candidate.get("affected_nodes", [])) or candidate["candidate_id"]
    return f"State and discharge the `{gate}` obligation for {candidate['creative_operation']} on {source} before unsafe promotion."


def commitment_ids_for_target(target: dict[str, Any] | None) -> list[str]:
    if not target:
        return TARGET_COMMITMENTS
    kb_ref = kb_ref_from_path(repo_path(str(target["kb_path"]), must_exist=True))
    ledger_path = ROOT / "agentic/state/essential_target_ledgers" / f"{kb_ref}.json"
    if ledger_path.exists():
        ledger = load_json_object(ledger_path)
        commitments = [row.get("id") for row in ledger.get("essential_commitments", []) if isinstance(row, dict)]
        commitments = [str(item) for item in commitments if str(item).strip()]
        if commitments:
            return commitments
    return TARGET_COMMITMENTS


def route_budget_for_target(target: dict[str, Any] | None, disposition: str, default: int) -> int:
    if not target:
        return default
    kb_ref = kb_ref_from_path(repo_path(str(target["kb_path"]), must_exist=True))
    ledger_path = ROOT / "agentic/state/essential_target_ledgers" / f"{kb_ref}.json"
    if ledger_path.exists():
        ledger = load_json_object(ledger_path)
        budgets = ledger.get("route_budgets", {})
        value = budgets.get(disposition)
        if isinstance(value, int) and value > 0:
            return value
    return default


def target_contract_for_target(target: dict[str, Any] | None) -> dict[str, Any]:
    if not target:
        return {}
    kb_ref = kb_ref_from_path(repo_path(str(target["kb_path"]), must_exist=True))
    ledger_path = ROOT / "agentic/state/essential_target_ledgers" / f"{kb_ref}.json"
    if ledger_path.exists():
        return target_contract_from_ledger(load_json_object(ledger_path))
    return {}


def target_relevance_for(candidate: dict[str, Any], disposition: str, hard_gates: dict[str, str], target: dict[str, Any] | None) -> dict[str, Any]:
    expected = candidate.get("expected_route_value", {})
    declared = expected.get("target_relevance", "medium")
    base = {"high": 0.9, "medium": 0.7, "low": 0.45}.get(declared, 0.55)
    profile = candidate.get("domain_specificity", {})
    specificity = float(profile.get("score", 0.0))
    if specificity:
        base = max(base, 0.42 + specificity * 0.55)
    if hard_gates.get("target_activation") != "pass":
        base -= 0.25
    if hard_gates.get("preservation") == "warn":
        base -= 0.1
    if hard_gates.get("source_grounding") == "fail":
        base -= 0.35
    if any(str(node).startswith("target:") for node in candidate.get("affected_nodes", [])) and candidate["creative_operation"] == "theorem_weakening":
        base -= 0.25
    score = max(0.0, min(1.0, round(base, 2)))
    drift_risk = "low"
    if candidate["creative_operation"] in {"analogy_transport", "carrier_introduction", "representation_shift"}:
        drift_risk = "medium"
    if score < 0.6 or disposition == "quarantine":
        drift_risk = "high"
    commitments = commitment_ids_for_target(target)
    profile_commitments = [item for item in profile.get("commitment_ids", []) if item in commitments]
    cited = profile_commitments or (commitments[:2] if len(commitments) >= 2 else commitments)
    if candidate["creative_operation"] in {"negative_route_inversion", "representation_shift", "analogy_transport"}:
        cited.append(commitments[2] if len(commitments) > 2 else cited[-1])
    if disposition == "proof_queue" and commitments:
        cited.append(commitments[-1])
    cited = list(dict.fromkeys(cited))
    routing_decision = disposition
    if score < 0.6 and disposition in {"proof_queue", "discovery_branch"}:
        routing_decision = "watch_archive"
    if drift_risk == "high" and disposition in {"proof_queue", "discovery_branch"}:
        routing_decision = "watch_archive"
    return {
        "target_relevance_score": score,
        "drift_risk": drift_risk,
        "cited_commitment_ids": cited,
        "routing_decision": routing_decision,
        "target_relevance_rationale": (
            "Scores route value by declared target relevance, target activation, preservation, "
            "source grounding, Yang-Mills specificity, and cited essential commitments; high-drift active routes are demoted to watch_archive."
        ),
    }


def build_validation_and_rankings(candidates: list[dict[str, Any]], target: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    packets = []
    rankings = []
    packets_by_candidate: dict[str, dict[str, Any]] = {}
    candidates_by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
    target_contract = target_contract_for_target(target)
    for idx, candidate in enumerate(candidates):
        hard_gates = {gate: gate_result(candidate, gate) for gate in HARD_GATES}
        disposition = route_for(candidate, hard_gates)
        target_commitments = commitment_ids_for_target(target)
        subgoal_control = subgoal_control_for_candidate(
            candidate,
            disposition,
            hard_gates,
            target_commitments=target_commitments,
        )
        candidate["subgoal_control"] = subgoal_control
        machinery_selection = machinery_selection_for_candidate(candidate, target_contract)
        candidate["machinery_selection"] = machinery_selection
        candidate["epistemic_status"] = {
            "proof_queue": "proof-queued",
            "discovery_branch": "discovery-branch",
            "revision_loop": "revision-needed",
            "evidence_task": "evidence-needed",
            "quarantine": "quarantined",
            "reject": "rejected",
            "stop": "stopped",
        }[disposition]
        obligations = [
            {
                "obligation_id": stable_id("obligation", candidate["candidate_id"], gate),
                "gate": gate,
                "status": hard_gates[gate],
                "requirement": gate_requirement_for(candidate, gate)
            }
            for gate in HARD_GATES
        ]
        for index, requirement in enumerate(candidate.get("route_blueprint", {}).get("proof_obligations", []), start=1):
            obligations.append(
                {
                    "obligation_id": stable_id("obligation", candidate["candidate_id"], "route-blueprint", index, requirement),
                    "gate": "route_blueprint",
                    "status": "open",
                    "requirement": requirement,
                }
            )
        packet = {
            "packet_id": stable_id("validation", candidate["candidate_id"]),
            "candidate_id": candidate["candidate_id"],
            "hard_gates": hard_gates,
            "obligations": obligations,
            "gate_summary": {
                "pass": list(hard_gates.values()).count("pass"),
                "warn": list(hard_gates.values()).count("warn"),
                "fail": list(hard_gates.values()).count("fail")
            },
            "route_disposition": disposition,
            "subgoal_control": subgoal_control,
            "machinery_selection": machinery_selection,
        }
        packets.append(packet)
        packets_by_candidate[candidate["candidate_id"]] = packet
        target_relevance = target_relevance_for(candidate, disposition, hard_gates, target)
        specificity = float(candidate.get("domain_specificity", {}).get("score", 0.0))
        score = packet["gate_summary"]["pass"] * 2 - packet["gate_summary"]["warn"] - packet["gate_summary"]["fail"] * 4
        score += int(target_relevance["target_relevance_score"] * 8)
        score += int(specificity * 5)
        if disposition == "proof_queue":
            score += 3
        if disposition == "revision_loop":
            score -= 1
        if disposition == "quarantine":
            score -= 4
        rankings.append(
            {
                "ranking_id": stable_id("ranking", candidate["candidate_id"], disposition),
                "candidate_id": candidate["candidate_id"],
                "route_disposition": disposition,
                "priority": idx + 1,
                "score": score,
                "changed_routing_decision": disposition != "stop",
                **target_relevance,
                "subgoal_control": subgoal_control,
                "machinery_selection": machinery_selection,
                "reasons": [
                    f"Creative operation: {candidate['creative_operation']}",
                    f"Gate summary: {packet['gate_summary']}",
                    f"Disposition selected by hard gates: {disposition}",
                    f"Subgoal control: {subgoal_control['decision']} because {subgoal_control['learning_from_failure']}",
                    f"Machinery selection: {machinery_selection['selected_machinery']} as {machinery_selection['machinery_role']} machinery controlling {machinery_selection['controlled_interface']}",
                    f"Target relevance: {target_relevance['target_relevance_score']} with drift risk {target_relevance['drift_risk']}",
                    f"Yang-Mills specificity terms: {candidate.get('domain_specificity', {}).get('route_terms', [])}",
                    f"Cited commitments: {target_relevance['cited_commitment_ids']}",
                ],
                "validation_packet_id": packet["packet_id"],
            }
        )
    rankings.sort(key=lambda row: (-row["score"], row["priority"], row["candidate_id"]))
    proof_queue_budget = route_budget_for_target(target, "proof_queue", 2)
    active_proof_queue_count = 0
    for row in rankings:
        if row["route_disposition"] != "proof_queue":
            continue
        active_proof_queue_count += 1
        if active_proof_queue_count <= proof_queue_budget:
            row["reasons"].append(f"Within active proof_queue budget {proof_queue_budget}.")
            continue
        packet = packets_by_candidate[row["candidate_id"]]
        candidate = candidates_by_id[row["candidate_id"]]
        row["route_disposition"] = "discovery_branch"
        row["routing_decision"] = "discovery_branch"
        row["subgoal_control"] = subgoal_control_for_candidate(
            candidate,
            "discovery_branch",
            packet["hard_gates"],
            target_commitments=commitment_ids_for_target(target),
        )
        row["score"] -= 4
        row["reasons"].append(
            f"Demoted from proof_queue by long-horizon route budget {proof_queue_budget}; keep as discovery branch until a proof slot opens."
        )
        packet["route_disposition"] = "discovery_branch"
        packet["subgoal_control"] = row["subgoal_control"]
        packet["machinery_selection"] = row["machinery_selection"]
        candidate["subgoal_control"] = row["subgoal_control"]
        candidate["machinery_selection"] = row["machinery_selection"]
        candidate["epistemic_status"] = "discovery-branch"
    rankings.sort(key=lambda row: (-row["score"], row["priority"], row["candidate_id"]))
    for index, row in enumerate(rankings, 1):
        row["priority"] = index
    return packets, rankings


def build_refinement_trace(
    target: dict[str, Any],
    pressures: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    validations: list[dict[str, Any]],
    rankings: list[dict[str, Any]],
) -> dict[str, Any]:
    validation_by_candidate = {row["candidate_id"]: row for row in validations}
    cycles = []
    for ranking in rankings[:10]:
        candidate = next(row for row in candidates if row["candidate_id"] == ranking["candidate_id"])
        pressure_ids = candidate["source_pressure_ids"]
        cycles.append(
            {
                "cycle_id": stable_id("cycle", target["target_id"], ranking["candidate_id"]),
                "input_pressure_ids": pressure_ids,
                "candidate_id": candidate["candidate_id"],
                "validation_packet_id": validation_by_candidate[candidate["candidate_id"]]["packet_id"],
                "route_disposition": ranking["route_disposition"],
                "continue_reason": "; ".join(ranking["reasons"]),
                "stop_condition": "looper_gate_quarantine" if ranking["route_disposition"] == "quarantine" else "",
            }
        )
    return {
        "trace_id": stable_id("trace", target["target_id"], len(pressures), len(candidates)),
        "target_id": target["target_id"],
        "cycles": cycles,
        "stop_conditions": [
            "resolved_by_proof_or_disproof",
            "no_candidates",
            "no_refinement_trigger",
            "plateau",
            "max_cycles",
            "high_reward_extension",
            "looper_gate_quarantine"
        ],
    }


def artifact_summary(map_payload: dict[str, Any]) -> dict[str, Any]:
    dispositions: dict[str, int] = {}
    operations: dict[str, int] = {}
    control_decisions: dict[str, int] = {}
    machinery_roles: dict[str, int] = {}
    for row in map_payload["candidate_rankings"]:
        dispositions[row["route_disposition"]] = dispositions.get(row["route_disposition"], 0) + 1
        decision = row.get("subgoal_control", {}).get("decision", "missing")
        control_decisions[decision] = control_decisions.get(decision, 0) + 1
        role = row.get("machinery_selection", {}).get("machinery_role", "missing")
        machinery_roles[role] = machinery_roles.get(role, 0) + 1
    for row in map_payload["mediation_candidates"]:
        operations[row["creative_operation"]] = operations.get(row["creative_operation"], 0) + 1
    return {
        "pressure_count": len(map_payload["pressure_packets"]),
        "candidate_count": len(map_payload["mediation_candidates"]),
        "validation_count": len(map_payload["validation_packets"]),
        "dispositions": dispositions,
        "creative_operations": operations,
        "subgoal_control_decisions": control_decisions,
        "machinery_roles": machinery_roles,
        "route_changing_candidates": sum(1 for row in map_payload["candidate_rankings"] if row["changed_routing_decision"]),
    }


def add_or_update_node(graph: dict[str, Any], node: dict[str, Any]) -> None:
    for existing in graph["nodes"]:
        if existing["id"] == node["id"]:
            existing.update(node)
            return
    graph["nodes"].append(node)


def add_or_update_edge(graph: dict[str, Any], edge: dict[str, Any]) -> None:
    if edge not in graph["edges"]:
        graph["edges"].append(edge)


def enrich_dependency_graph(graph: dict[str, Any], map_payload: dict[str, Any], artifact_path: str) -> dict[str, Any]:
    candidate_by_id = {row["candidate_id"]: row for row in map_payload["mediation_candidates"]}
    validation_by_candidate = {row["candidate_id"]: row for row in map_payload["validation_packets"]}
    pressure_by_id = {row["pressure_id"]: row for row in map_payload["pressure_packets"]}
    candidate_pressure_ids = {
        pressure_id
        for candidate in map_payload["mediation_candidates"]
        for pressure_id in candidate["source_pressure_ids"]
    }
    visible_pressures = list(map_payload["pressure_packets"][:24])
    for pressure_id in sorted(candidate_pressure_ids):
        pressure = pressure_by_id.get(pressure_id)
        if pressure and pressure not in visible_pressures:
            visible_pressures.append(pressure)
    for pressure in visible_pressures:
        node_id = f"pressure:{pressure['pressure_id']}"
        add_or_update_node(
            graph,
            {
                "id": node_id,
                "kind": "conceptual_pressure",
                "status": "blocked" if pressure["pressure_type"] == "failure" else "proof-debt",
                "label": pressure["witness"],
                "source_artifact": artifact_path,
                "evidence_paths": pressure["source_artifacts"] + [artifact_path],
                "parents": [pressure["source_node_id"]],
                "next_action": "Route this pressure through creative candidate generation and validation gates.",
                "blocker": "",
                "payload": {"pressure_type": pressure["pressure_type"], "severity": pressure["severity"]},
            },
        )
        if pressure["source_node_id"] in {node["id"] for node in graph["nodes"]}:
            add_or_update_edge(graph, {"from": pressure["source_node_id"], "to": node_id, "kind": "raises-conceptual-pressure", "source_artifact": artifact_path})
    for ranking in map_payload["candidate_rankings"][:16]:
        candidate = candidate_by_id[ranking["candidate_id"]]
        validation = validation_by_candidate[candidate["candidate_id"]]
        candidate_node = f"candidate:{candidate['candidate_id']}"
        status = "bridge-obligation" if ranking["route_disposition"] in {"discovery_branch", "proof_queue"} else "blocked"
        add_or_update_node(
            graph,
            {
                "id": candidate_node,
                "kind": "creative_candidate",
                "status": status,
                "label": candidate["proposed_transformation"],
                "source_artifact": artifact_path,
                "evidence_paths": candidate.get("source_artifacts", []) + [artifact_path],
                "parents": [f"pressure:{pid}" for pid in candidate["source_pressure_ids"]],
                "next_action": f"Disposition `{ranking['route_disposition']}` requires validation packet {validation['packet_id']}.",
                "blocker": "" if status != "blocked" else "conceptual-validation-gate",
                "payload": {"creative_operation": candidate["creative_operation"], "ranking_id": ranking["ranking_id"]},
            },
        )
        for pressure_id in candidate["source_pressure_ids"]:
            if pressure_id in pressure_by_id:
                add_or_update_edge(graph, {"from": f"pressure:{pressure_id}", "to": candidate_node, "kind": "motivates-creative-candidate", "source_artifact": artifact_path})
        validation_node = f"validation:{validation['packet_id']}"
        add_or_update_node(
            graph,
            {
                "id": validation_node,
                "kind": "validation_obligation",
                "status": "proof-debt" if validation["route_disposition"] != "quarantine" else "blocked",
                "label": f"Validate {candidate['creative_operation']} candidate via hard gates.",
                "source_artifact": artifact_path,
                "evidence_paths": [artifact_path],
                "parents": [candidate_node],
                "next_action": f"Resolve hard gates before route disposition `{validation['route_disposition']}` is promoted.",
                "blocker": "" if validation["route_disposition"] != "quarantine" else "unmet-hard-gate",
                "payload": validation["gate_summary"],
            },
        )
        add_or_update_edge(graph, {"from": candidate_node, "to": validation_node, "kind": "has-validation-obligation", "source_artifact": artifact_path})
    frontier = [
        {
            "id": node["id"],
            "kind": node["kind"],
            "status": node["status"],
            "next_action": node.get("next_action", ""),
            "blocker": node.get("blocker", ""),
        }
        for node in graph["nodes"]
        if node["status"] not in {"grounded", "accepted-local", "refuted"}
    ]
    frontier.sort(key=lambda row: (row["status"], row["kind"], row["id"]))
    graph["nodes"] = sorted(graph["nodes"], key=lambda row: row["id"])
    graph["edges"] = sorted(graph["edges"], key=lambda row: (row["from"], row["to"], row["kind"]))
    graph["frontier"] = frontier
    graph["summary"] = {"node_count": len(graph["nodes"]), "edge_count": len(graph["edges"]), "frontier_count": len(frontier), "status_counts": {}, "kind_counts": {}}
    for node in graph["nodes"]:
        graph["summary"]["status_counts"][node["status"]] = graph["summary"]["status_counts"].get(node["status"], 0) + 1
        graph["summary"]["kind_counts"][node["kind"]] = graph["summary"]["kind_counts"].get(node["kind"], 0) + 1
    return graph


def render_source_map() -> str:
    return """# Hegelian Source Map For Abducer

## Disposition

The Hegelian Solver snapshot remains source evidence. Abducer adopts selected control concepts as native hypothesis-space artifacts and rejects a second runtime, copied agent tree, or proof-bypassing acceptance labels.

## Adopted Concepts

| Source idea | Abducer adaptation | Evidence |
| --- | --- | --- |
| Concept/crisis packet | `conceptual_pressure_packet` tied to dependency graph nodes | `external/hegelian-solver/refs`, `agentic/spec/conceptual_pressure_packet.schema.json` |
| Failure certificate | `abducer_failure_certificate` for blocked proof, bridge, source, or premise obligations | `agentic/spec/abducer_failure_certificate.schema.json` |
| Discovery signal | Positive structural pressure from repeated route shapes or bridge opportunity | `agentic/spec/abducer_discovery_signal.schema.json` |
| Mediation candidate | Creative route transformation over Abducer artifacts | `agentic/spec/abducer_mediation_candidate.schema.json` |
| Validation packet | Hard proof/source/non-collapse gates | `agentic/spec/abducer_validation_packet.schema.json` |
| Bounded reflection | `conceptual_refinement_trace` consumed by `work` and Looper gates | `artifacts/hegelian/conceptual_refinement_trace.json` |

## Rejected Material

- Standalone Hegelian CLI as Abducer entrypoint.
- Parallel `agents/` tree copied into `skills/`.
- Generic accept labels treated as proof.
- Creative terminology that cannot produce obligations, graph edges, or route dispositions.
"""


def render_operations_doc(operations: list[dict[str, Any]]) -> str:
    lines = [
        "# Conceptual Creativity Operations",
        "",
        "Abducer treats conceptual creativity as a typed transformation over the hypothesis exploration map. A move is creative only when it changes route options and creates validation obligations.",
        "",
        "| Operation | Produces | Validation pressure |",
        "| --- | --- | --- |",
    ]
    for row in operations:
        lines.append(f"| `{row['id']}` | {', '.join(row['produces'])} | {', '.join(row['validation_pressure'])} |")
    lines.extend(
        [
            "",
            "## Validation Rule",
            "",
            "No creative operation can promote itself. It must pass through a validation packet, candidate ranking, Looper graph edge, and release evidence. Missing source grounding or unnamed hard obligations force quarantine or rejection.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_release_report(map_payload: dict[str, Any]) -> str:
    summary = map_payload["summary"]
    return f"""# Hegelian Conceptual Refinement Release Report

## Target

- Target ID: `{map_payload['target_id']}`
- KB: `{map_payload['kb_path']}`
- Scope: hypothesis-space control and validation, not proof of the mathematical target.

## Workflow Evidence

- Hypothesis exploration map: `artifacts/hegelian/hypothesis_exploration_map.json`
- Failure/signal cartography: `artifacts/hegelian/failure_signal_cartography.json`
- Mediation candidates: `artifacts/hegelian/mediation_candidates.json`
- Validation packets: `artifacts/hegelian/validation_packets.json`
- Candidate rankings: `artifacts/hegelian/candidate_rankings.json`
- Machinery-selection packets: `artifacts/hegelian/machinery_selection_packets.json`
- Refinement trace: `artifacts/hegelian/conceptual_refinement_trace.json`

## Route-Changing Evidence

- Pressure packets: {summary['pressure_count']}
- Creative candidates: {summary['candidate_count']}
- Validation packets: {summary['validation_count']}
- Route-changing candidates: {summary['route_changing_candidates']}
- Dispositions: `{summary['dispositions']}`
- Machinery roles: `{summary.get('machinery_roles', {})}`

## Hard Gate Policy

Candidates with failed source grounding are quarantined. Candidates without proof-queue readiness remain discovery branches, revision items, or evidence tasks.
Candidates also need target-object-linked machinery selection: a proof role, controlled interface, invalid-use modes, bridge obligation, and validation handoff.

## Decision

Decision: promote

Rationale: the integration produces Abducer-native hypothesis-space artifacts, Looper-visible graph nodes, hard validation obligations, route dispositions, tests, and review evidence while preserving mathematical proof debt.
"""


def render_coherence_review(map_payload: dict[str, Any]) -> str:
    return f"""# Hegelian Abducer Coherence Review

## Finding

The integration is Abducer-native: the Hegelian source snapshot informs contracts, but routing flows through the hypothesis exploration map, validation packets, candidate rankings, `work`, and Looper graph evidence.

## Conceptual Creativity

The map records creative operations as route-changing transformations. Current operations observed: `{map_payload['summary']['creative_operations']}`.

## Validation Depth

Validation covers deterministic schemas, replay stability, hard gates, generative quality probes, metamorphic evidence removal, ablation of the creativity layer, and proof-queue safety.

## Residual Risk

The current generated candidates are deterministic seeds. Richer mathematical candidates should be authored by the repo-local generative skills, then rechecked by the same validator before promotion.
"""


def write_jsonl_log(path: Path, map_payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    events = [
        ("skill_application_start", "abducer-conceptual-pressure-formalizer", "Started hypothesis-space refinement from dependency graph."),
        ("skill_application_action_taken", "abducer-failure-signal-cartographer", f"Classified {len(map_payload['pressure_packets'])} pressure packets."),
        ("skill_application_action_taken", "abducer-mediation-candidate-generator", f"Generated {len(map_payload['mediation_candidates'])} creative candidates."),
        ("skill_application_gate_evaluated", "abducer-obligation-gatekeeper", f"Built {len(map_payload['validation_packets'])} validation packets."),
        ("skill_application_evidence_recorded", "abducer-refinement-route-ranker", f"Ranked {len(map_payload['candidate_rankings'])} route dispositions."),
        ("skill_application_complete", "looper-workflow-contract-governor", "Recorded Looper-visible conceptual refinement evidence."),
    ]
    with path.open("w", encoding="utf-8") as handle:
        for event, skill, summary in events:
            handle.write(
                json.dumps(
                    {
                        "run_id": "HEGELIAN-ITER-0001",
                        "target_id": map_payload["target_id"],
                        "workflow_id": "conceptual_hypothesis_exploration_loop",
                        "event": event,
                        "skill_id": skill,
                        "summary": summary,
                        "evidence": ["artifacts/hegelian/hypothesis_exploration_map.json"],
                        "created_utc": map_payload["generated_utc"],
                    },
                    sort_keys=True,
                )
                + "\n"
            )


def build_map(target_path: Path, graph_path: Path, *, enrich_graph: bool = True, write_artifacts: bool = True) -> dict[str, Any]:
    target = load_json_object(target_path)
    graph = load_json_object(graph_path)
    operations = operation_by_id()
    pressures, failures, signals = build_pressure_packets(graph)
    candidates, creativity = build_candidates(pressures, operations)
    validations, rankings = build_validation_and_rankings(candidates, target)
    trace = build_refinement_trace(target, pressures, candidates, validations, rankings)
    map_payload = {
        "map_id": stable_id("hypothesis-map", target["target_id"], graph["graph_id"]),
        "target_id": target["target_id"],
        "kb_path": target["kb_path"],
        "source_graph": rel(graph_path),
        "generated_utc": utc_now(),
        "creative_operations": load_operations(),
        "pressure_packets": pressures,
        "failure_certificates": failures,
        "discovery_signals": signals,
        "mediation_candidates": candidates,
        "conceptual_creativity_analysis": creativity,
        "validation_packets": validations,
        "candidate_rankings": rankings,
        "abstraction_machinery_policy": ABSTRACTION_MACHINERY_POLICY,
        "formal_subgoal_control_policy": FORMAL_SUBGOAL_CONTROL_POLICY,
        "refinement_trace": trace,
        "summary": {},
    }
    map_payload["summary"] = artifact_summary(map_payload)
    if not write_artifacts:
        return map_payload
    out_dir = ROOT / "artifacts/hegelian"
    write_json(out_dir / "hypothesis_exploration_map.json", map_payload)
    write_json(out_dir / "failure_signal_cartography.json", {"failure_certificates": failures, "discovery_signals": signals, "pressure_packets": pressures})
    write_json(out_dir / "mediation_candidates.json", {"candidates": candidates, "conceptual_creativity_analysis": creativity})
    write_json(out_dir / "validation_packets.json", {"validation_packets": validations})
    write_json(out_dir / "candidate_rankings.json", {"candidate_rankings": rankings})
    machinery_selections = [row["machinery_selection"] for row in rankings]
    write_json(
        out_dir / "machinery_selection_packets.json",
        {
            "policy": ABSTRACTION_MACHINERY_POLICY,
            "summary": summarize_machinery_portfolio(machinery_selections),
            "selections": machinery_selections,
            "candidate_ids": [row["candidate_id"] for row in rankings],
        },
    )
    write_json(
        out_dir / "formal_subgoal_controls.json",
        {
            "policy": FORMAL_SUBGOAL_CONTROL_POLICY,
            "controls": [row["subgoal_control"] for row in rankings],
            "candidate_ids": [row["candidate_id"] for row in rankings],
        },
    )
    write_json(out_dir / "conceptual_refinement_trace.json", trace)
    write_json(ROOT / "agentic/fixtures/hegelian/hypothesis_exploration_map.example.json", map_payload)
    write_json(ROOT / "agentic/fixtures/hegelian/conceptual_pressure_packet.example.json", pressures[:4])
    mixed_pressures = [row for row in pressures if row["pressure_type"] == "failure"][:4]
    mixed_pressures.extend([row for row in pressures if row["pressure_type"] == "discovery_signal"][:4])
    if len(mixed_pressures) < 8:
        mixed_pressures.extend([row for row in pressures if row not in mixed_pressures][: 8 - len(mixed_pressures)])
    # Runtime output must never rewrite checked-in regression inputs, including
    # the P-vs-NP fixture when this builder is running a different target.
    write_json(out_dir / "pressure_case.json", {"target": target, "pressures": mixed_pressures, "candidates": candidates[:4]})
    write_json(out_dir / "hegelian_pressure_cases.json", {"cases": pressures[:6]})
    (ROOT / "docs/integrations/hegelian-source-map.md").write_text(render_source_map(), encoding="utf-8")
    (ROOT / "docs/research-methods/conceptual-creativity-operations.md").write_text(render_operations_doc(load_operations()), encoding="utf-8")
    (ROOT / "agentic/reports/hegelian_conceptual_refinement_release_report.md").parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "agentic/reports/hegelian_conceptual_refinement_release_report.md").write_text(render_release_report(map_payload), encoding="utf-8")
    (ROOT / "agentic/reports/hegelian_abducer_coherence_review.md").write_text(render_coherence_review(map_payload), encoding="utf-8")
    write_jsonl_log(ROOT / "agentic/logs/hegelian-conceptual-refinement.jsonl", map_payload)
    if enrich_graph:
        enriched = enrich_dependency_graph(graph, map_payload, "artifacts/hegelian/hypothesis_exploration_map.json")
        write_json(graph_path, enriched)
    return map_payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="agentic/examples/targets/p-vs-np-target.json")
    parser.add_argument("--graph", default="agentic/state/dependency_graphs/p-vs-np.json")
    parser.add_argument("--no-enrich-graph", action="store_true")
    args = parser.parse_args()
    payload = build_map(ROOT / args.target, ROOT / args.graph, enrich_graph=not args.no_enrich_graph)
    print(
        "Wrote artifacts/hegelian/hypothesis_exploration_map.json "
        f"with {payload['summary']['candidate_count']} candidates"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
