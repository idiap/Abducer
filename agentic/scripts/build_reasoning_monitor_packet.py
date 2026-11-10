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

"""Build the self-contained data packet for the reasoning monitor HTML."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, kb_ref_from_path, load_json_object, load_optional_json, rel, repo_path, utc_now, write_json
from abstraction_machinery_selection import POLICY as ABSTRACTION_MACHINERY_POLICY
from abstraction_machinery_selection import summarize_machinery_portfolio
from formal_subgoal_control import POLICY as FORMAL_SUBGOAL_CONTROL_POLICY
from formal_subgoal_control import summary_from_controls


OUT = ROOT / "agentic/reports/reasoning_monitor/latest.json"


def file_card(path: str, role: str) -> dict[str, Any]:
    target = ROOT / path
    return {"path": path, "role": role, "exists": target.exists()}


def node_by_id(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["id"]: row for row in graph.get("nodes", []) if isinstance(row, dict)}


def build_frontier(graph: dict[str, Any], limit: int = 80) -> dict[str, Any]:
    nodes = node_by_id(graph)
    rows = []
    for item in graph.get("frontier", [])[:limit]:
        node = nodes.get(item["id"], {})
        rows.append(
            {
                "node_id": item["id"],
                "kind": item.get("kind", node.get("kind", "")),
                "status": item.get("status", node.get("status", "")),
                "label": clean_text(node.get("label") or item.get("next_action") or item.get("blocker") or item["id"])[:420],
                "next_action": clean_text(item.get("next_action") or node.get("next_action") or item.get("blocker") or node.get("blocker")),
                "evidence_paths": node.get("evidence_paths", []),
                "parents": node.get("parents", []),
            }
        )
    return {
        "total": graph["summary"]["frontier_count"],
        "node_count": graph["summary"]["node_count"],
        "edge_count": graph["summary"]["edge_count"],
        "status_counts": graph["summary"].get("status_counts", {}),
        "kind_counts": graph["summary"].get("kind_counts", {}),
        "items": rows,
    }


def build_candidate_routes(hypothesis: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = {row["candidate_id"]: row for row in hypothesis.get("mediation_candidates", []) if isinstance(row, dict)}
    validations = {row["candidate_id"]: row for row in hypothesis.get("validation_packets", []) if isinstance(row, dict)}
    routes = []
    for ranking in hypothesis.get("candidate_rankings", []):
        if not isinstance(ranking, dict):
            continue
        candidate = candidates.get(ranking["candidate_id"], {})
        validation = validations.get(ranking["candidate_id"], {})
        routes.append(
            {
                "candidate_id": ranking["candidate_id"],
                "priority": ranking.get("priority"),
                "route_disposition": ranking.get("route_disposition"),
                "routing_decision": ranking.get("routing_decision"),
                "target_relevance_score": ranking.get("target_relevance_score"),
                "drift_risk": ranking.get("drift_risk"),
                "cited_commitment_ids": ranking.get("cited_commitment_ids", []),
                "creative_operation": candidate.get("creative_operation", ""),
                "creative_operation_label": candidate.get("creative_operation_label", ""),
                "proposed_transformation": clean_text(candidate.get("proposed_transformation"))[:700],
                "source_witness": clean_text(candidate.get("source_witness"))[:700],
                "domain_specificity": candidate.get("domain_specificity", {}),
                "route_blueprint": candidate.get("route_blueprint", {}),
                "subgoal_control": ranking.get("subgoal_control") or candidate.get("subgoal_control") or validation.get("subgoal_control", {}),
                "machinery_selection": ranking.get("machinery_selection") or candidate.get("machinery_selection") or validation.get("machinery_selection", {}),
                "expected_route_value": candidate.get("expected_route_value", {}),
                "disconfirming_observations": candidate.get("disconfirming_observations", []),
                "source_artifacts": candidate.get("source_artifacts", []),
                "validation_packet_id": ranking.get("validation_packet_id"),
                "gate_summary": validation.get("gate_summary", {}),
                "hard_gates": validation.get("hard_gates", {}),
                "obligations": validation.get("obligations", []),
                "reasons": ranking.get("reasons", []),
                "epistemic_status": candidate.get("epistemic_status", "conjectural"),
            }
        )
    return routes


def collect_proof_obligations(
    routes: list[dict[str, Any]],
    frontier: dict[str, Any],
    contradiction_routes: list[dict[str, Any]] | None = None,
    empirical_requests: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    obligations = []
    for route in routes:
        for obligation in route.get("obligations", []):
            if not isinstance(obligation, dict):
                continue
            obligations.append(
                {
                    "source": "candidate_validation",
                    "candidate_id": route["candidate_id"],
                    "gate": obligation.get("gate"),
                    "status": obligation.get("status"),
                    "requirement": obligation.get("requirement"),
                }
            )
    for item in frontier["items"]:
        if item["status"] in {"proof-debt", "bridge-obligation", "tentative-local"}:
            obligations.append(
                {
                    "source": "dependency_frontier",
                    "candidate_id": "",
                    "gate": item["kind"],
                    "status": item["status"],
                    "requirement": item["next_action"] or item["label"],
                }
            )
    for route in contradiction_routes or []:
        for obligation in route.get("proof_obligations", []):
            obligations.append(
                {
                    "source": "contradiction_route",
                    "candidate_id": route.get("branch_id", ""),
                    "gate": route.get("strategy", ""),
                    "status": route.get("computed_verdict", "proof-obligation"),
                    "requirement": obligation,
                }
            )
    for item in empirical_requests or []:
        obligations.append(
            {
                "source": "empirical_evidence_request",
                "candidate_id": item.get("request_id", ""),
                "gate": item.get("evidence_mode", ""),
                "status": "evidence-task",
                "requirement": f"{item.get('empirical_question', '')} Proof boundary: {item.get('proof_boundary', '')}",
            }
        )
    return {
        "total": len(obligations),
        "items": obligations[:160],
    }


def build_contradiction_routes(bridge: dict[str, Any], validation: dict[str, Any]) -> list[dict[str, Any]]:
    verdicts = {
        row.get("route_id"): row
        for row in validation.get("routes", [])
        if isinstance(row, dict) and row.get("source") == "yang_mills_bridge_packet"
    }
    rows = []
    for packet in bridge.get("packets", []) if isinstance(bridge.get("packets"), list) else []:
        if not isinstance(packet, dict):
            continue
        for branch in packet.get("contradiction_branches", []):
            if not isinstance(branch, dict):
                continue
            verdict = verdicts.get(branch.get("branch_id"), {})
            rows.append(
                {
                    "branch_id": branch.get("branch_id", ""),
                    "source_packet_id": packet.get("packet_id", ""),
                    "source_packet_title": packet.get("title", ""),
                    "route_family": packet.get("route_family", ""),
                    "strategy": branch.get("strategy", ""),
                    "exact_negation": branch.get("exact_negation", ""),
                    "contradiction_carrier": branch.get("contradiction_carrier", ""),
                    "preserved_commitments": branch.get("preserved_commitments", []),
                    "derived_consequence": branch.get("derived_consequence", ""),
                    "conflict_target": branch.get("conflict_target", ""),
                    "proof_obligations": branch.get("proof_obligations", []),
                    "failure_modes": branch.get("failure_modes", []),
                    "audit_skill": branch.get("audit_skill", ""),
                    "learning_if_failed": branch.get("learning_if_failed", ""),
                    "computed_verdict": verdict.get("computed_verdict", "unvalidated"),
                    "mathematical_learning": verdict.get("mathematical_learning", ""),
                    "finding_count": verdict.get("finding_count", 0),
                    "same_theory_invariant": packet.get("same_theory_invariant", ""),
                    "equation_checkpoints": contradiction_equations(branch),
                }
            )
    return rows


def contradiction_equations(branch: dict[str, Any]) -> list[dict[str, str]]:
    strategy = clean_text(branch.get("strategy")).lower()
    if "no-gap" in strategy:
        return [
            {
                "label": "No-gap negation",
                "display": "for all epsilon > 0, exists psi_epsilon in P_perp H_YM with ||psi_epsilon||=1 and <psi_epsilon,H psi_epsilon> < epsilon",
                "valid_when": "H_YM, Omega, H, and P_perp are reconstructed from the same OS-positive continuum Schwinger functions.",
            },
            {
                "label": "Contradiction target",
                "display": "E_H((0,m0)) P_perp = 0",
                "valid_when": "Gauge-invariant observables are spectrally determining and Euclidean decay is cutoff-uniform with m >= m0 > 0.",
            },
        ]
    if "positivity" in strategy:
        return [
            {
                "label": "Negated OS positivity",
                "display": "sum_i,j conjugate(c_i)c_j S(Theta f_i,f_j) < 0",
                "valid_when": "The test-observable family belongs to the limiting gauge-invariant algebra and survives the OS null quotient.",
            },
            {
                "label": "Closed positive cone target",
                "display": "S_n^{a,L} reflection-positive and S_n^{a,L} => S_n imply S_n reflection-positive",
                "valid_when": "The cutoff-removal topology makes reflection positivity a closed condition.",
            },
        ]
    return [
        {
            "label": "Triviality-collapse negation",
            "display": "<O_1 ... O_k>_c = 0 for every candidate nontriviality witness family",
            "valid_when": "The O_i are gauge-invariant observables in the same continuum Schwinger family used for reconstruction.",
        },
        {
            "label": "Nontriviality conflict target",
            "display": "<O_1 ... O_k>_c != 0 in the continuum limit",
            "valid_when": "A same-theory non-Gaussian witness has been proved for the limiting Yang-Mills object.",
        },
    ]


def target_spine(target: dict[str, Any], ledger: dict[str, Any]) -> dict[str, Any]:
    commitments = ledger.get("essential_commitments", [])
    return {
        "commitments": commitments,
        "commitment_ids": [row["id"] for row in commitments if isinstance(row, dict) and row.get("id")],
        "accepted_weakenings": ledger.get("accepted_weakenings", []),
        "forbidden_drift_patterns": ledger.get("forbidden_drift_patterns", []),
        "active_route_families": ledger.get("active_route_families", []),
        "route_budgets": ledger.get("route_budgets", {}),
        "target_object_contract": ledger.get("target_object_contract", {}),
        "main_claim_ids": target.get("main_claim_ids", []),
    }


def machinery_monitor_section(routes: list[dict[str, Any]], abstraction_chain: dict[str, Any]) -> dict[str, Any]:
    selections = [
        route.get("machinery_selection", {})
        for route in routes
        if isinstance(route.get("machinery_selection"), dict) and route.get("machinery_selection")
    ]
    return {
        "title": "Machinery Selection",
        "purpose": (
            "Explain why each mathematical abstraction is being used now: which proof role it plays, which interface it controls, "
            "what invalid uses are blocked, and how the abstraction chain moves from target object to final claim."
        ),
        "policy": ABSTRACTION_MACHINERY_POLICY,
        "summary": summarize_machinery_portfolio(selections),
        "items": selections,
        "abstraction_chain": abstraction_chain,
        "universal_role_read": [
            "Construction is valuable when the target object is not yet built.",
            "Representation is valuable when the object exists but cannot yet be reasoned over.",
            "Invariant preservation is valuable when transformations risk changing the problem.",
            "Transfer is valuable when meaning must cross a regime, limit, or formalism.",
            "Witness machinery is valuable when the final claim needs a detectable certificate.",
            "Obstruction machinery is valuable when a route fails and the failure can teach the next bridge.",
            "Validation machinery is valuable when local success might solve a proxy instead of the target.",
        ],
    }


def evidence_ledger(paths: list[dict[str, str]], routes: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, Any]:
    cards = {row["path"]: file_card(row["path"], row["role"]) for row in paths}
    for route in routes:
        for path in route.get("source_artifacts", []):
            if isinstance(path, str) and path.strip():
                cards.setdefault(path, file_card(path, "candidate source"))
    for event in events:
        for path in event.get("evidence_paths", []):
            if isinstance(path, str) and path.strip() and path != "explicit-unknown":
                cards.setdefault(path, file_card(path, "reasoning event evidence"))
    rows = sorted(cards.values(), key=lambda row: (not row["exists"], row["path"]))
    return {
        "total": len(rows),
        "missing": [row for row in rows if not row["exists"]],
        "items": rows,
    }


def interpretative_strategy_story(routes: list[dict[str, Any]], contradiction_routes: list[dict[str, Any]]) -> dict[str, Any]:
    by_family: dict[str, list[dict[str, Any]]] = {}
    for route in routes:
        family = route.get("route_blueprint", {}).get("route_family", "")
        if family:
            by_family.setdefault(family, []).append(route)
    hamiltonian = by_family.get("Hamiltonian spectral-gap route", [])
    correlator = by_family.get("Euclidean correlator-decay to spectral-gap route", [])
    balaban = by_family.get("Balaban RG continuum-control route", [])
    os_routes = by_family.get("OS reconstruction and reflection-positivity bridge", [])
    h_route = next((route for route in hamiltonian if route.get("creative_operation") == "theorem_weakening"), hamiltonian[0] if hamiltonian else {})
    c_route = correlator[0] if correlator else {}
    b_route = balaban[0] if balaban else {}
    os_route = os_routes[0] if os_routes else {}
    contradiction_names = [route.get("strategy", "") for route in contradiction_routes]
    return {
        "title": "Physics Strategy Story",
        "mode": "generative interpretative strategy, not route-index prose",
        "physics_explanation_contract": [
            "Name the dynamical object: four-dimensional compact simple Yang-Mills gauge-field configurations, their gauge-invariant observable algebra, and the vacuum sector being constructed.",
            "Explain the scale story: which ultraviolet cutoff, infrared volume, and coarse-graining or continuum-limit passage is being controlled.",
            "Name the observables that carry physical information, such as Wilson loops, local curvature composites, or gauge-invariant Schwinger functions, rather than generic proof nodes.",
            "Separate kinematics from dynamics: OS positivity and reconstruction build the Hilbert-space language, while decay, clustering, and nontriviality must express the dynamics of the gauge theory.",
            "Connect Euclidean data to spectral meaning through the spectral measure of time correlations and say what support away from zero would physically exclude.",
            "State same-theory transfer: the continuum object, reconstructed Hamiltonian, observable algebra, nontriviality witness, and gap witness must be outputs of one limiting theory.",
            "Describe failure physically: cutoff leakage, finite-volume artifacts, Gaussian collapse, loss of reflection positivity, or an observable family too small to see the excitation spectrum.",
            "Turn each strategic move into a mechanism-bearing lemma with assumptions, equations, observables, limit regime, and a disqualifying counter-scenario.",
        ],
        "current_thesis": (
            "The physical story is about whether fluctuating non-Abelian gauge fields can be controlled across scales so that "
            "the continuum limit still contains an interacting gauge-invariant vacuum sector, and whether the Euclidean time "
            "correlations of that same sector have spectral support bounded away from zero. Balaban-style RG is the ultraviolet "
            "and continuum-construction spine; OS/reflection positivity is the passage from Euclidean Schwinger data to a "
            "Hilbert-space energy operator; correlator decay is the infrared spectral witness. The Hamiltonian gap statement "
            "is therefore the endpoint of this chain, not an object that may be postulated independently."
        ),
        "story_beats": [
            {
                "phase": "first_attempt_hamiltonian_subclaim",
                "headline": "First we tried to express the goal as a bounded Hamiltonian spectral-gap subclaim.",
                "tried": (
                    h_route.get("proposed_transformation")
                    or "Construct the physical Hilbert space, identify the vacuum, and prove a strictly positive lower bound on first non-vacuum excitation."
                ),
                "physics_story": (
                    "This is the clean energy-spectrum formulation of the Clay target. Once Euclidean Yang-Mills has produced "
                    "OS-positive Schwinger functions, reconstruction should give the physical Hilbert space of gauge-invariant "
                    "states, the vacuum vector, time translations, and a positive Hamiltonian. A mass gap means that after removing "
                    "the vacuum line there are no arbitrarily soft physical excitations: the first glueball-like gauge-invariant "
                    "energy lies at least Delta above the vacuum."
                ),
                "equations": [
                    {
                        "label": "Hamiltonian endpoint",
                        "latex": r"\mathcal H_{\mathrm{YM}},\ \Omega,\ H\ge 0,\ P_\perp=1-|\Omega\rangle\langle\Omega|",
                        "display": "H_YM, Omega, H >= 0, P_perp = 1 - |Omega><Omega|",
                    },
                    {
                        "label": "Mass-gap form",
                        "latex": r"\operatorname{Spec}(H|_{P_\perp\mathcal H_{\mathrm{YM}}})\subseteq[\Delta,\infty),\quad \Delta>0",
                        "display": "Spec(H restricted to P_perp H_YM) subset [Delta, infinity), Delta > 0",
                    },
                    {
                        "label": "Equivalent spectral projection exclusion",
                        "latex": r"E_H((0,\Delta))P_\perp=0",
                        "display": "E_H((0, Delta)) P_perp = 0",
                    },
                ],
                "why_it_did_not_pay_off": [
                    "This did not pay off as a proof route because it described the endpoint more than the construction mechanism.",
                    "X: the Hamiltonian formulation presupposes the reconstructed continuum Hilbert space rather than constructing it.",
                    "Y: the key inequality E_H((0,Delta)) P_perp = 0 is the hard mass-gap lemma itself, so naming it does not discharge it.",
                    "Z: a fixed-lattice transfer-matrix gap may disappear as the cutoff is removed, and gauge-invariant observables may fail to determine the full excitation spectrum.",
                ],
                "what_we_learned": [
                    "We learned that Hamiltonian language is indispensable as an endpoint test but weak as a discovery engine unless the reconstruction inputs are already available.",
                    "A claimed gap must always be asked backwards: where did H_YM, Omega, H, P_perp, and the observable algebra come from?",
                    "This converted the analysis from naming a desired spectral inequality into tracking the Euclidean construction and reconstruction prerequisites that make the inequality meaningful.",
                ],
                "decision": "Keep this as the mathematical endpoint and derivation checkpoint, but do not promote it as the primary proof route.",
                "moved_to": "Euclidean correlator decay plus OS/transfer machinery, because it offers a possible witness for the Hamiltonian spectral lower bound.",
                "supporting_artifacts": h_route.get("route_blueprint", {}).get("derivation_artifacts", []),
            },
            {
                "phase": "second_attempt_correlator_decay",
                "headline": "Then we moved to Euclidean correlator decay as a spectral-gap witness.",
                "tried": c_route.get(
                    "proposed_transformation",
                    "Prove exponential decay for gauge-invariant Euclidean two-point functions and transfer it through OS reconstruction to a Hamiltonian spectral gap.",
                ),
                "physics_story": (
                    "This is the Euclidean physics face of a gap. If a gauge-invariant observable O creates physical excitations "
                    "from the vacuum, its connected Euclidean time correlation is a Laplace transform of the Hamiltonian spectral "
                    "measure seen by O. Exponential decay with a cutoff-independent rate says that this spectral measure has no "
                    "weight near zero. The route is physically meaningful only if the observables survive the continuum limit and "
                    "are rich enough to see the vacuum-orthogonal excitation sector."
                ),
                "equations": [
                    {
                        "label": "Euclidean decay witness",
                        "latex": r"|\langle O(t)O(0)\rangle-\langle O\rangle^2|\le C_O e^{-m t}",
                        "display": "|<O(t)O(0)> - <O>^2| <= C_O exp(-m t)",
                    },
                    {
                        "label": "Spectral representation pressure",
                        "latex": r"\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)",
                        "display": "<O(t)O(0)>_c = integral_0^infinity exp(-t lambda) d mu_O(lambda)",
                    },
                    {
                        "label": "Gap inference target",
                        "latex": r"\operatorname{supp}(\mu_O)\subseteq[m,\infty)\ \text{for a spectrally determining family }O",
                        "display": "supp(mu_O) subset [m, infinity) for a spectrally determining family O",
                    },
                ],
                "what_paid_off": [
                    "It connects directly to the Hamiltonian endpoint through spectral representation.",
                    "It exposes concrete observables and decay constants rather than only an abstract spectral claim.",
                    "It tells the monitor what a mass-gap witness would look like in Euclidean data.",
                ],
                "why_it_did_not_pay_off": [
                    "It did not pay off as a standalone proof route because Euclidean decay can be true in a regulated or strong-coupling regime without proving a continuum Yang-Mills mass gap.",
                    "It left two hidden assumptions exposed: the decay constants must not vanish under cutoff removal, and the observable family must determine the whole physical excitation spectrum.",
                    "It also did not by itself supply nontriviality; an exponentially decaying sector is not enough if the limiting theory is Gaussian, empty, or not the constructed Yang-Mills object.",
                ],
                "what_we_learned": [
                    "Correlator decay is valuable only when it is a same-theory spectral witness: the observables, OS reconstruction, and Hamiltonian must all come from the same limiting Schwinger functions.",
                    "The right mathematical object to demand next is not just a decay estimate, but a cutoff-uniform decay-to-spectrum lemma with an observable-density hypothesis.",
                    "This taught the loop to treat strong-coupling lattice decay as evidence-task material until it carries a continuum-transfer certificate.",
                ],
                "remaining_blockers": [
                    "The decay constants must be uniform through cutoff removal.",
                    "The selected gauge-invariant observables must be dense or spectrally determining in the vacuum-orthogonal sector.",
                    "The reconstructed theory must remain nontrivial and interacting.",
                ],
                "decision": "Keep this route in the active proof queue, but require uniformity and spectral-determining observables before treating it as progress.",
                "moved_to": "Balaban/RG continuum control, because correlator decay is not enough unless it survives into the same continuum object.",
                "route_id": c_route.get("candidate_id", ""),
            },
            {
                "phase": "third_attempt_balaban_rg",
                "headline": "In parallel we moved to Balaban RG as the continuum-construction spine.",
                "tried": b_route.get(
                    "proposed_transformation",
                    "Use Balaban-style renormalisation control to construct the four-dimensional continuum Yang-Mills object and preserve nontriviality.",
                ),
                "physics_story": (
                    "This is the scale-dynamics side. Starting with regulated gauge fields, the RG analysis must show that integrating "
                    "out short-distance modes does not lose control of the non-Abelian interaction, does not break the gauge-invariant "
                    "observable algebra, and has a continuum limit as the lattice spacing goes to zero and the volume goes to infinity. "
                    "For the Clay problem, ultraviolet stability is not yet the explanation of the gap; it is the condition under which "
                    "there is a nontrivial continuum vacuum whose correlations could carry a gap."
                ),
                "equations": [
                    {
                        "label": "Cutoff-removal spine",
                        "latex": r"S_{a,L}(A)\xrightarrow[a\to 0,\ L\to\infty]{} S_{\mathrm{YM}}^{\mathrm{cont}}",
                        "display": "S_{a,L}(A) -> S_YM^cont as a -> 0 and L -> infinity",
                    },
                    {
                        "label": "Uniform control demand",
                        "latex": r"\sup_k \|R_k\|_{\mathcal B_k}<\infty\quad\text{with nontrivial interacting remainder}",
                        "display": "sup_k ||R_k||_{B_k} < infinity with nontrivial interacting remainder",
                    },
                    {
                        "label": "OS-positive limit target",
                        "latex": r"S_n^{(a,L)}\Rightarrow S_n,\quad S_n\ \text{satisfies reflection positivity}",
                        "display": "S_n^{(a,L)} => S_n, with S_n satisfying reflection positivity",
                    },
                ],
                "what_paid_off": [
                    "It addresses the four-dimensional continuum-limit bottleneck directly.",
                    "It gives a place to ask for nontriviality witnesses in the limiting Yang-Mills object.",
                    "It can potentially feed the correlator-decay route with cutoff-stable estimates.",
                ],
                "why_it_did_not_pay_off": [
                    "It did not pay off as a mass-gap route by itself because ultraviolet/RG stability is not the same thing as an infrared spectral threshold.",
                    "It still leaves the OS/Wightman bridge open: a controlled effective action sequence must produce Schwinger functions with the axioms needed for reconstruction.",
                    "It can falsely look like progress if the loop celebrates multiscale control while never extracting a gauge-invariant decay or spectral witness.",
                ],
                "what_we_learned": [
                    "Balaban-style control should be used as the construction spine, not as a substitute for the mass-gap mechanism.",
                    "The decisive test is whether RG-controlled cutoff objects produce OS-positive continuum Schwinger functions and a non-Gaussian same-theory witness.",
                    "This shifted the loop toward an RG-to-OS bridge lemma instead of adding more renormalisation vocabulary.",
                ],
                "remaining_blockers": [
                    "RG stability alone is not a mass gap.",
                    "The limiting object must satisfy OS/Wightman adequacy.",
                    "A mass-gap witness must be extracted in the same limiting theory rather than imported from a regulated model.",
                ],
                "decision": "Keep this route in the active proof queue as the construction spine.",
                "moved_to": "Fuse RG continuum control with correlator-decay/spectral transfer rather than treating them as separate successes.",
                "route_id": b_route.get("candidate_id", ""),
            },
            {
                "phase": "current_recursive_strategy",
                "headline": "Now the recursive strategy is to fuse construction and spectral transfer.",
                "tried": os_route.get("proposed_transformation", "Use OS reconstruction as the bridge between Euclidean construction and Hamiltonian spectral claims."),
                "physics_story": (
                    "The bridge has to say how a continuum gauge theory constructed by scale control becomes a spectral statement. "
                    "The same limiting Schwinger functions must satisfy reflection positivity, define the gauge-invariant observable "
                    "algebra, retain a non-Gaussian connected sector, and have Euclidean time correlations whose spectral measures "
                    "avoid a neighborhood of zero. Only then can the reconstructed Hamiltonian inherit a positive lower threshold."
                ),
                "equations": [
                    {
                        "label": "Bridge lemma skeleton",
                        "latex": r"\mathrm{RG\ control}+\mathrm{OS\ positivity}+\mathrm{uniform\ clustering}\Rightarrow \Delta_{\mathrm{YM}}>0",
                        "display": "RG control + OS positivity + uniform clustering => Delta_YM > 0",
                    },
                    {
                        "label": "Same-theory constraint",
                        "latex": r"(S_n,\mathcal H_{\mathrm{YM}},H,\Omega)\ \text{must be reconstructed from the same limiting theory}",
                        "display": "(S_n, H_YM, H, Omega) must be reconstructed from the same limiting theory",
                    },
                ],
                "why_this_is_the_next_goal": [
                    "It keeps the continuum object, OS reconstruction, nontriviality witness, and Hamiltonian gap in the same theory.",
                    "It prevents drift into pure Hamiltonian notation without construction.",
                    "It prevents drift into lattice-only decay without continuum spectral meaning.",
                ],
                "what_we_learned": [
                    "The analysis should now advance by testing typed bridge lemmas, not by accumulating more route families.",
                    "A strategy only counts as learning if it changes the mathematical dependency order: Hamiltonian claims move behind reconstruction gates, decay claims move behind uniformity/density gates, and RG claims move behind OS/nontriviality gates.",
                    "The next useful artifact is therefore a bridge-lemma packet with definitions, assumptions, equations, failure tests, and conditional skill triggers.",
                ],
                "next_recursive_questions": [
                    "Which exact Schwinger functions or Wilson-loop/local-curvature observables are candidates for decay estimates?",
                    "Can Balaban-style bounds imply any uniform clustering or decay input, or is a separate infrared argument required?",
                    "What density theorem for gauge-invariant observables would make decay-to-gap transfer legitimate?",
                ],
                "decision": "The next iteration should produce explicit bridge-lemma packets, not another broad slogan.",
                "moved_to": "OS-positive continuum Schwinger functions plus gauge-invariant spectral-determining observables.",
            },
            {
                "phase": "proof_by_contradiction_branching",
                "headline": "We then added reductio branches to test whether the negated worlds create real mathematical pressure.",
                "tried": (
                    "Assume the structured negations that matter for Yang-Mills: OS positivity fails, the continuum limit collapses "
                    "to triviality, or the reconstructed Hamiltonian has no positive gap."
                ),
                "physics_story": (
                    "A reductio is physically useful only when the negated world leaves a detectable trace. If there is no gap, "
                    "there should be a sequence of vacuum-orthogonal gauge-invariant states with energies tending to zero, or "
                    "equivalently spectral weight accumulating at the origin for some determining observable family. If OS positivity "
                    "fails, the Euclidean theory cannot reconstruct a positive-norm quantum Hilbert space. If the continuum limit is "
                    "trivial, connected gauge-invariant cumulants collapse. These are physical failure modes, not just logical negations."
                ),
                "equations": [
                    {
                        "label": "No-gap negated world",
                        "latex": r"\forall\varepsilon>0\ \exists\psi_\varepsilon\in P_\perp\mathcal H_{\mathrm{YM}},\ \|\psi_\varepsilon\|=1,\ \langle\psi_\varepsilon,H\psi_\varepsilon\rangle<\varepsilon",
                        "display": "for all epsilon > 0, exists psi_epsilon in P_perp H_YM with ||psi_epsilon||=1 and <psi_epsilon,H psi_epsilon> < epsilon",
                        "valid_when": "H_YM, Omega, H, and P_perp are reconstructed from the same OS-positive continuum Schwinger functions.",
                    },
                    {
                        "label": "OS-failure negated world",
                        "latex": r"\sum_{i,j}\overline c_i c_j S(\Theta f_i,f_j)<0",
                        "display": "sum_i,j conjugate(c_i)c_j S(Theta f_i,f_j) < 0",
                        "valid_when": "The f_i are reflected gauge-invariant test observables in the limiting Schwinger-function algebra.",
                    },
                    {
                        "label": "Triviality-collapse negated world",
                        "latex": r"\langle O_1\cdots O_k\rangle_c=0\quad\text{for the witness family}",
                        "display": "<O_1 ... O_k>_c = 0 for the witness family",
                        "valid_when": "The O_i are gauge-invariant observables in the same continuum object used for reconstruction and gap analysis.",
                    },
                ],
                "what_paid_off": [
                    "The reductio branches expose carrier objects instead of slogans: spectral mass, reflection forms, and connected cumulants.",
                    "They make backtracking precise: if the conflict cannot be made same-theory, the route is quarantined rather than celebrated.",
                    "They turn failure into learning by naming whether density, closedness, nontriviality, or cutoff-uniformity is the missing hinge.",
                ],
                "why_it_did_not_pay_off": [
                    "No contradiction branch currently proves Yang-Mills; each branch is only promotable as a proof obligation.",
                    "The no-gap reductio still depends on observable density and cutoff-uniform decay.",
                    "The OS and triviality reductios still depend on closedness of reflection positivity and a same-theory nontriviality witness.",
                ],
                "what_we_learned": [
                    "The loop learned to use contradiction as a disciplined pressure test rather than an excuse to skip construction.",
                    "A branch succeeds only if the contradiction target is accepted or validator-backed in the same theory.",
                    "A failed branch is still valuable when it tells us whether to pivot toward density, closedness, nontriviality, or uniform-decay evidence.",
                ],
                "remaining_blockers": [
                    "Audit exact negation and same-theory preservation before proof-queue promotion.",
                    "Attach every contradiction branch to a certification artifact and demotion trigger.",
                    "Keep all reductio carriers inside the reconstructed continuum Yang-Mills object.",
                ],
                "decision": "Keep all three reductio branches active as proof-obligation pressure tests, not as proof results.",
                "moved_to": "Contradiction-route auditing plus bridge-lemma validation.",
                "active_branches": contradiction_names,
            },
        ],
        "anti_drift_rules": [
            "Do not count Hamiltonian notation as progress unless the Hilbert space comes from the reconstructed continuum Yang-Mills theory.",
            "Do not count Euclidean decay as progress unless constants survive cutoff removal.",
            "Do not count RG ultraviolet control as progress toward the gap unless it connects to OS-positive Schwinger functions and a mass-gap witness.",
            "Do not split construction, nontriviality, and spectral gap across different regulated theories.",
            "Do not count a reductio branch as progress unless its exact negation, carrier, and conflict target preserve the same Yang-Mills object.",
        ],
    }


def success_milestones(routes: list[dict[str, Any]]) -> dict[str, Any]:
    route_families = {route.get("route_blueprint", {}).get("route_family", "") for route in routes}

    def status_for(*families: str) -> str:
        if any(family in route_families for family in families):
            return "route_in_play_not_achieved"
        return "not_started"

    return {
        "title": "Success Milestones",
        "purpose": (
            "Signpost the big-deal mathematical achievements that would change the status of the Yang-Mills run. "
            "A milestone is not proof completion; it becomes a potential breakthrough only when it is potentially achieved "
            "by attached certification evidence and its disqualifiers have been actively checked. Each card names a success signal, "
            "certification evidence, disqualifier tests, and a next action."
        ),
        "promotion_policy": [
            "Do not mark achieved from notation, route ranking, or successful report generation.",
            "Mark potential_breakthrough_signal only when the certification evidence is attached to the same continuum Yang-Mills object.",
            "Demote immediately if the result lives only at fixed cutoff, in finite volume, or in a theory that is not the reconstructed target theory.",
        ],
        "items": [
            {
                "milestone_id": "ym-ms-01-continuum-construction",
                "label": "Continuum Yang-Mills object constructed",
                "current_status": status_for("Balaban RG continuum-control route"),
                "why_big_deal": "This would attack the existence half of the Clay target rather than only optimizing a regulated lattice model.",
                "potentially_achieved_when": "A Balaban/RG-controlled cutoff sequence is shown to have a continuum limit with OS-positive Schwinger functions for compact simple gauge group Yang-Mills on R^4.",
                "success_signal": "Cutoff-removal theorem with a named limiting object S_n and preserved gauge-invariant observables.",
                "certification_evidence": [
                    "Uniform multiscale/RG bounds across the cutoff-removal sequence.",
                    "Tightness or convergence argument for the regulated measures or Schwinger functions.",
                    "Reflection positivity survives the limiting procedure.",
                ],
                "disqualifiers": [
                    "Only finite-volume or fixed-lattice-spacing control is available.",
                    "The limit is not shown to be a quantum Yang-Mills object on R^4.",
                    "Gauge-group structure is lost or replaced by a scalar/free surrogate.",
                ],
                "next_action": "Formulate the exact continuum-passage lemma connecting Balaban-style estimates to OS-positive limiting Schwinger functions.",
                "linked_commitments": ["existence", "continuum-limit", "os-wightman-adequacy"],
                "equations": [
                    {
                        "label": "Continuum limit witness",
                        "display": "S_n^{(a,L)} => S_n on R^4 as a -> 0 and L -> infinity",
                    }
                ],
            },
            {
                "milestone_id": "ym-ms-02-os-reconstruction",
                "label": "OS reconstruction yields the physical Hilbert space",
                "current_status": status_for("OS reconstruction and reflection-positivity bridge", "Euclidean correlator-decay to spectral-gap route"),
                "why_big_deal": "This would turn Euclidean data into the Hamiltonian arena where a mass gap has a precise spectral meaning.",
                "potentially_achieved_when": "The limiting Schwinger functions satisfy the OS axioms strongly enough to reconstruct H_YM, Omega, and H from the same continuum theory.",
                "success_signal": "A reconstruction packet names the Hilbert space, vacuum, Hamiltonian/semigroup, observable domain, and positivity argument.",
                "certification_evidence": [
                    "Reflection positivity for the limiting Schwinger functions.",
                    "Euclidean covariance, symmetry, regularity, and clustering assumptions required by the reconstruction theorem.",
                    "Explicit identification of gauge-invariant observable classes carried into the Hilbert space.",
                ],
                "disqualifiers": [
                    "The Hilbert space is postulated rather than reconstructed.",
                    "The reconstruction applies to a different regulated theory.",
                    "The observable class is too small to speak about the physical excitation spectrum.",
                ],
                "next_action": "Write the OS reconstruction obligation as a bridge lemma with inputs, theorem used, and output objects H_YM, Omega, H.",
                "linked_commitments": ["existence", "os-wightman-adequacy"],
                "equations": [
                    {
                        "label": "Reconstruction output",
                        "display": "OS(S_n) => (H_YM, Omega, H, gauge-invariant observable algebra)",
                    }
                ],
            },
            {
                "milestone_id": "ym-ms-03-nontriviality-witness",
                "label": "Nontrivial interacting continuum theory witnessed",
                "current_status": status_for("Balaban RG continuum-control route"),
                "why_big_deal": "This would prevent an apparent construction from collapsing into a Gaussian, empty, or purely classical limit.",
                "potentially_achieved_when": "A gauge-invariant observable has limiting correlations or cumulants incompatible with the free/Gaussian theory.",
                "success_signal": "A nonzero connected correlation, Wilson-loop area/perimeter behavior, or higher cumulant survives cutoff removal.",
                "certification_evidence": [
                    "Observable is defined in the same limiting continuum object.",
                    "Connected or higher-order correlation does not vanish in the limit.",
                    "The witness distinguishes the result from a free Gaussian fixed point.",
                ],
                "disqualifiers": [
                    "The witness is only heuristic or simulation-level evidence.",
                    "The observable is not gauge invariant.",
                    "The nontriviality claim comes from a different approximation scheme than the constructed limit.",
                ],
                "next_action": "Select one candidate gauge-invariant observable family and state the exact non-Gaussianity/nontriviality lemma it would need to satisfy.",
                "linked_commitments": ["nontriviality", "continuum-limit"],
                "equations": [
                    {
                        "label": "Connected witness",
                        "display": "<O_1 O_2>_c != 0 in the continuum limit",
                    }
                ],
            },
            {
                "milestone_id": "ym-ms-04-uniform-correlator-decay",
                "label": "Cutoff-uniform Euclidean mass-gap witness obtained",
                "current_status": status_for("Euclidean correlator-decay to spectral-gap route"),
                "why_big_deal": "This would provide the first concrete spectral-gap witness rather than only a desired Hamiltonian inequality.",
                "potentially_achieved_when": "Gauge-invariant Euclidean correlations decay exponentially with constants stable under continuum-limit passage.",
                "success_signal": "A family of observables O has |<O(t)O(0)>_c| <= C_O exp(-m t) with m > 0 independent of the removed cutoff.",
                "certification_evidence": [
                    "The decay estimate is proved before and after taking the continuum limit.",
                    "The mass parameter m has a positive lower bound independent of cutoff scale.",
                    "The observable family is tied to the reconstructed physical Hilbert space.",
                ],
                "disqualifiers": [
                    "Decay is available only at strong coupling or fixed lattice spacing.",
                    "Constants degenerate to zero under cutoff removal.",
                    "The observable family is not spectrally determining.",
                ],
                "next_action": "Turn the correlator route into a decay-to-gap lemma with explicit uniform constants and observable-density assumptions.",
                "linked_commitments": ["positive-mass-gap", "continuum-limit", "os-wightman-adequacy"],
                "equations": [
                    {
                        "label": "Uniform decay",
                        "display": "|<O(t)O(0)>_c| <= C_O exp(-m t), m >= m_0 > 0 uniformly in cutoff",
                    }
                ],
            },
            {
                "milestone_id": "ym-ms-05-hamiltonian-gap",
                "label": "Positive Hamiltonian spectral gap proved",
                "current_status": status_for("Hamiltonian spectral-gap route", "Euclidean correlator-decay to spectral-gap route"),
                "why_big_deal": "This is the mass-gap half of the Clay target in the reconstructed physical Hilbert space.",
                "potentially_achieved_when": "The reconstructed Hamiltonian has no non-vacuum spectrum in (0, Delta) for some Delta > 0.",
                "success_signal": "A theorem proves Spec(H restricted to P_perp H_YM) subset [Delta, infinity) for the same continuum theory.",
                "certification_evidence": [
                    "H, Omega, and P_perp come from OS/Wightman reconstruction of the constructed Yang-Mills theory.",
                    "A decay-to-gap or direct spectral argument excludes all non-vacuum states below Delta.",
                    "Gauge-invariant observables determine the relevant excitation sector.",
                ],
                "disqualifiers": [
                    "The gap is only a finite-lattice transfer-matrix gap.",
                    "The spectral statement is asserted before Hilbert-space reconstruction.",
                    "The proof omits vacuum uniqueness or the projection onto non-vacuum excitations.",
                ],
                "next_action": "Use the Hamiltonian derivation as a checkpoint: list every premise needed before E_H((0, Delta)) P_perp = 0 can be claimed.",
                "linked_commitments": ["positive-mass-gap", "existence", "nontriviality"],
                "equations": [
                    {
                        "label": "Hamiltonian gap",
                        "display": "Spec(H restricted to P_perp H_YM) subset [Delta, infinity), Delta > 0",
                    }
                ],
            },
            {
                "milestone_id": "ym-ms-06-integrated-clay-target",
                "label": "Same-theory Clay target integration achieved",
                "current_status": "not_achieved",
                "why_big_deal": "This is the point where local successes stop being isolated and become a candidate solution architecture for the full problem.",
                "potentially_achieved_when": "Existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap are proved for one and the same Yang-Mills theory.",
                "success_signal": "A single dependency-closed proof packet connects all five essential commitments with no theory-switching or cutoff leakage.",
                "certification_evidence": [
                    "All upstream milestones cite the same limiting object and observable algebra.",
                    "No open proof obligation blocks a required Clay commitment.",
                    "Failure tests for cutoff leakage, triviality, and insufficient reconstruction all pass.",
                ],
                "disqualifiers": [
                    "Construction, nontriviality, and gap are proved in different theories.",
                    "Any essential target commitment is weakened without an accepted weakening rule.",
                    "The proof depends on an unvalidated heuristic or numerical premise.",
                ],
                "next_action": "Keep this as the top-level success gate and only promote lower milestones when they preserve all essential commitments.",
                "linked_commitments": ["existence", "nontriviality", "os-wightman-adequacy", "continuum-limit", "positive-mass-gap"],
                "equations": [
                    {
                        "label": "Integrated target",
                        "display": "existence + nontriviality + OS/Wightman + continuum limit + Delta_YM > 0 in one theory",
                    }
                ],
            },
        ],
    }


def strategic_reorientation_control(routes: list[dict[str, Any]], frontier: dict[str, Any]) -> dict[str, Any]:
    proof_routes = [route for route in routes if route.get("route_disposition") == "proof_queue"]
    discovery_routes = [route for route in routes if route.get("route_disposition") == "discovery_branch"]
    blocked_frontier = [
        item
        for item in frontier.get("items", [])
        if item.get("status") in {"blocked", "proof-debt", "bridge-obligation", "tentative-local"}
    ]

    def route_assessment(route: dict[str, Any]) -> dict[str, Any]:
        family = route.get("route_blueprint", {}).get("route_family", "")
        commitments = route.get("cited_commitment_ids", [])
        control = route.get("subgoal_control", {})
        if "Balaban" in family:
            return {
                "candidate_id": route["candidate_id"],
                "route_family": family,
                "recommended_move": "restrategize",
                "subgoal_control": control,
                "formal_control_decision": control.get("decision", "missing"),
                "obstruction_type": "construction-to-reconstruction bridge missing",
                "current_read": (
                    "This route is still high-value because it attacks continuum construction, but it must stop behaving as if "
                    "ultraviolet control automatically implies OS-positive continuum Schwinger functions or a mass gap."
                ),
                "backtrack_trigger": "Backtrack if the next step only controls finite volume, small fields, or cutoff-dependent measures.",
                "pivot_trigger": "Pivot away from this as proof-queue lead if no theorem-shaped RG-to-OS bridge can be stated after the bridge pass.",
                "next_probe": "Name the exact regulated input objects, limiting Schwinger-function output, and reflection-positivity preservation theorem.",
                "protected_commitments": commitments,
            }
        if "correlator" in family.lower():
            return {
                "candidate_id": route["candidate_id"],
                "route_family": family,
                "recommended_move": "restrategize-with-pivot-test",
                "subgoal_control": control,
                "formal_control_decision": control.get("decision", "missing"),
                "obstruction_type": "spectral witness lacks cutoff-uniform transfer",
                "current_read": (
                    "This route is valuable because it sees the mass gap through Euclidean decay, but it is dangerous if decay "
                    "constants or observable-density assumptions disappear in the continuum limit."
                ),
                "backtrack_trigger": "Backtrack if the observable family is not gauge invariant, not spectrally determining, or not reconstructed into H_YM.",
                "pivot_trigger": "Pivot toward construction/nontriviality if every plausible decay estimate loses its positive lower bound under cutoff removal.",
                "next_probe": "Formulate the decay-to-gap lemma with OS positivity, spectral measure support, observable density, and cutoff-uniform constants.",
                "protected_commitments": commitments,
            }
        return {
            "candidate_id": route["candidate_id"],
            "route_family": family or "unclassified route family",
            "recommended_move": "quarantine-until-classified",
            "subgoal_control": control,
            "formal_control_decision": control.get("decision", "missing"),
            "obstruction_type": "route family not mapped to a Yang-Mills reorientation pattern",
            "current_read": "The route cannot guide the proof queue until its construction object, spectral target, and target commitments are typed.",
            "backtrack_trigger": "Backtrack if it relies on an unconstructed object or unaccepted weakening.",
            "pivot_trigger": "Pivot if another route preserves more essential commitments with fewer hidden assumptions.",
            "next_probe": "Classify the route against construction, reconstruction, nontriviality, decay, and spectral-transfer obligations.",
            "protected_commitments": commitments,
        }

    return {
        "title": "Reorientation Control",
        "purpose": (
            "Give the long-horizon loop a reflective mechanism for restrategize, backtrack, and pivot decisions in physics terms. "
            "The aim is not to move because the search feels stuck; it is to diagnose whether the obstruction concerns construction "
            "of the continuum gauge-field measure, reconstruction of the quantum Hilbert space, nontriviality of the vacuum sector, "
            "or the infrared spectral support of gauge-invariant excitations. Current Diagnosis states the physical obstruction; "
            "Current Recommendation states the licensed move; Bounded Reflection prevents endless meta-looping; Route-Level diagnosis "
            "binds every control decision to a concrete route; each mode names a Forbidden Shortcut that would create false progress."
        ),
        "current_diagnosis": (
            "Physically, the active routes are not competing stories about different problems. They are two incomplete views of "
            "one Yang-Mills mechanism. The Balaban/RG route asks whether the non-Abelian gauge-field ensemble can be controlled "
            "from the ultraviolet cutoff to a non-Gaussian continuum vacuum with reflection-positive Schwinger functions. The "
            "correlator route asks whether gauge-invariant observables in that same vacuum have Euclidean time spectral measures "
            "whose support stays away from zero, which would exclude arbitrarily light physical excitations after reconstruction. "
            "Neither view is disposable: RG without an infrared spectral witness constructs no gap, while decay without continuum "
            "object identity and observable density may only describe a regulated or too-small sector. The correct next motion is "
            "a bridge-focused restrategy that proves or falsifies same-theory transfer across cutoff removal, OS reconstruction, "
            "nontriviality, and spectral support."
        ),
        "current_recommendation": {
            "decision": "restrategize_without_wholesale_pivot",
            "rationale": (
                "Do not pivot away from the current routes merely because the mathematical obstruction is hard. The live physical question is "
                "whether scale-controlled gauge-field construction can feed a Euclidean spectral measure argument in the same "
                "continuum theory. The honest move is to type that bridge: source objects, observable algebra, limiting regime, "
                "spectral measure, and disqualifying failure modes."
            ),
            "backtrack_guard": "Backtrack whenever an energy-spectrum, lattice, or decay claim uses a Hilbert space, vacuum, observable family, or decay constant before showing how it survives OS-positive continuum reconstruction.",
            "pivot_guard": "Pivot only after the relevant physical obstruction has repeated under certification: no continuum object, no reflection positivity, no nontrivial connected sector, no observable density, or no cutoff-uniform spectral lower bound.",
            "quarantine_guard": "Strong-coupling lattice decay, lower-dimensional analogies, and numerical glueball evidence remain evidence tasks until they state the transfer certificate connecting them to the same continuum Yang-Mills object.",
            "formal_subgoal_guard": "Persist with a formula subgoal only while it remains target-linked and each failed attempt teaches a sharper premise, object, regime, or bridge; otherwise backtrack, pivot, quarantine, or stop.",
        },
        "bounded_reflection_contract": {
            "max_reflection_passes_before_action": 2,
            "required_output_per_pass": [
                "one typed bridge lemma or a named reason it cannot be stated",
                "one backtrack/pivot/quarantine decision tied to a concrete route or explicit no-change rationale",
                "one validation artifact that can be inspected by the long-horizon probe",
                "one formal subgoal-control decision for every active proof or discovery route",
            ],
            "stop_reflecting_when": [
                "the next action is only a paraphrase of the previous action",
                "no route-level obstruction type changes after two passes",
                "the loop cannot name a same-theory object connecting construction, reconstruction, and spectral claims",
                "a subgoal records repeated blockers without new mathematical learning",
            ],
            "resume_search_when": "A route-level next_probe has been converted into a concrete lemma packet, evidence task, or demotion decision.",
        },
        "control_policy": [
            "Restrategize when a route remains target-relevant but the current formulation hides the real missing lemma.",
            "Backtrack when a step achieved apparent progress by importing an object from the wrong theory, cutoff, volume, or reconstruction stage.",
            "Pivot when a route repeatedly fails its own certification tests while another route preserves more essential commitments with fewer hidden assumptions.",
            "Quarantine when a route is interesting but cannot yet preserve existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap in one theory.",
            "Deepen rather than pivot when the obstruction is a missing bridge lemma whose source and target objects are already correctly identified.",
        ],
        "reorientation_modes": [
            {
                "mode": "restrategize",
                "deep_meaning": "Change the decomposition of the problem while preserving the same high-value route family.",
                "yang_mills_use": "Turn broad RG or correlator slogans into bridge lemmas with named source objects, target objects, and transfer theorem.",
                "trigger": "A route has high target relevance but its obligations repeat at the same abstraction level.",
                "allowed_action": "Refactor the route into construction, reconstruction, nontriviality, decay, and spectral-transfer packets.",
                "forbidden_shortcut": "Renaming the same obligation with more mathematical nouns.",
            },
            {
                "mode": "backtrack",
                "deep_meaning": "Undo a locally attractive step because it changed the theory, weakened the target, or used an object before it was constructed.",
                "yang_mills_use": "Return from Hamiltonian notation to OS reconstruction if H_YM, Omega, H, or P_perp were merely assumed.",
                "trigger": "A proof step depends on fixed-lattice gaps, finite-volume estimates, postulated Hilbert spaces, or non-gauge-invariant witnesses.",
                "allowed_action": "Move the step back behind the relevant construction or reconstruction milestone and restate it as a premise obligation.",
                "forbidden_shortcut": "Treating a regulated or heuristic result as if it already lived in the continuum Yang-Mills theory.",
            },
            {
                "mode": "pivot",
                "deep_meaning": "Change route family because the present family is structurally unable to certify the target commitments.",
                "yang_mills_use": "Shift priority from a standalone Hamiltonian route to RG plus OS/correlator transfer, or from correlator decay to construction if uniformity collapses.",
                "trigger": "The same disqualifier fires after refinement: cutoff constants vanish, observables fail to determine the spectrum, or nontriviality cannot be witnessed.",
                "allowed_action": "Promote a discovery branch that covers the failed commitment and demote the blocked proof route to watch/archive or evidence-task status.",
                "forbidden_shortcut": "Pivoting because another route is easier while silently dropping an essential Clay commitment.",
            },
            {
                "mode": "quarantine",
                "deep_meaning": "Keep a seductive idea visible without allowing it to steer the proof queue.",
                "yang_mills_use": "Hold lattice strong-coupling decay, analogies, or lower-dimensional mechanisms as evidence tasks until a transfer theorem is named.",
                "trigger": "A candidate is conceptually illuminating but fails same-theory, continuum, or OS/Wightman gates.",
                "allowed_action": "Attach disconfirming observations and require a transfer certificate before re-entry.",
                "forbidden_shortcut": "Letting a vivid analogy count as progress on the main route.",
            },
        ],
        "decision_points": [
            {
                "checkpoint": "RG construction route",
                "if_progress": "Uniform multiscale control begins to name a continuum limiting object and OS-positive Schwinger functions.",
                "if_stalls": "Restrategize into a continuum-passage bridge lemma rather than adding more RG terminology.",
                "backtrack_if": "The route only controls a small-field, finite-volume, or cutoff-dependent object.",
                "pivot_if": "No path from RG estimates to OS-positive continuum Schwinger functions can be stated after the next bridge-lemma pass.",
                "next_experiment": "Ask for the exact theorem shape: assumptions on regulated measures, output Schwinger functions, and preservation of reflection positivity.",
            },
            {
                "checkpoint": "Correlator-decay route",
                "if_progress": "A gauge-invariant observable family has exponential decay with cutoff-stable constants.",
                "if_stalls": "Backtrack to observable choice and spectral-density assumptions before trying another decay estimate.",
                "backtrack_if": "The decay estimate is fixed-lattice, strong-coupling-only, or disconnected from the reconstructed Hilbert space.",
                "pivot_if": "Uniform constants provably degenerate under cutoff removal.",
                "next_experiment": "State a decay-to-gap lemma with hypotheses on OS positivity, spectral representation, and observable density.",
            },
            {
                "checkpoint": "Hamiltonian spectral route",
                "if_progress": "H_YM, Omega, H, and P_perp are outputs of reconstruction, not assumptions.",
                "if_stalls": "Treat the Hamiltonian statement as an endpoint checklist and backtrack to OS reconstruction.",
                "backtrack_if": "The route asks to prove E_H((0, Delta))P_perp=0 before constructing H.",
                "pivot_if": "The route cannot identify any Euclidean or constructive source for the spectral lower bound.",
                "next_experiment": "Map each Hamiltonian premise to the exact Euclidean construction or spectral-transfer obligation that would supply it.",
            },
            {
                "checkpoint": "Same-theory integration",
                "if_progress": "Construction, nontriviality, OS reconstruction, and mass-gap witness all cite the same limiting object.",
                "if_stalls": "Restrategize around object identity: name the limiting theory and require every lemma to type-check against it.",
                "backtrack_if": "A local success belongs to a different regulated theory or weakens compact simple gauge-group Yang-Mills.",
                "pivot_if": "The active route family can only prove a nearby theorem after accepted weakenings are exhausted.",
                "next_experiment": "Build a same-theory dependency table with rows for object, observable algebra, reconstruction output, and gap witness.",
            },
        ],
        "route_assessments": [route_assessment(route) for route in proof_routes],
        "pivot_watchlist": [
            {
                "candidate_id": route["candidate_id"],
                "route_family": route.get("route_blueprint", {}).get("route_family", ""),
                "why_not_proof_queue_now": "Held outside proof queue by budget or because it duplicates a proof-queue family; promote only if it covers a failed commitment better.",
                "promotion_condition": "A proof-queue route fires its pivot trigger, and this branch preserves the missing essential commitment with clearer certification evidence.",
            }
            for route in discovery_routes[:4]
        ],
        "active_reorientation_queue": [
            {
                "action_id": "reorient-01-bridge-rg-to-os",
                "mode": "restrategize",
                "priority": "high",
                "action": "Formulate the bridge lemma from Balaban-style RG control to OS-positive continuum Schwinger functions.",
                "why_now": "It is the shared missing hinge between construction and spectral-gap routes.",
                "success_condition": "The lemma names assumptions, output objects, failure tests, and the same-theory invariant.",
            },
            {
                "action_id": "reorient-02-backtrack-hamiltonian-premises",
                "mode": "backtrack",
                "priority": "high",
                "action": "Move every Hamiltonian spectral claim behind explicit OS reconstruction premises.",
                "why_now": "The Hamiltonian route is a useful endpoint but becomes misleading if H_YM is assumed.",
                "success_condition": "Every occurrence of H, Omega, and P_perp has a reconstruction source or is marked as an open premise.",
            },
            {
                "action_id": "reorient-03-pivot-test-correlator-uniformity",
                "mode": "pivot-test",
                "priority": "medium",
                "action": "Probe whether correlator decay can be made cutoff-uniform; if not, pivot priority toward construction/nontriviality.",
                "why_now": "A nonuniform decay estimate would be a beautiful dead end for the Clay target.",
                "success_condition": "The loop records whether constants remain bounded below through cutoff removal.",
            },
            {
                "action_id": "reorient-04-quarantine-analogies",
                "mode": "quarantine",
                "priority": "medium",
                "action": "Keep lattice-only, strong-coupling, or lower-dimensional analogies out of the proof queue unless they carry transfer certificates.",
                "why_now": "These ideas are valuable for intuition but dangerous for target drift.",
                "success_condition": "Every analogy is stored as an evidence task with explicit transfer obligations.",
            },
        ],
        "loop_metrics": {
            "active_proof_routes": len(proof_routes),
            "discovery_routes": len(discovery_routes),
            "blocked_or_bridge_frontier": len(blocked_frontier),
        },
        "formal_subgoal_control_summary": summary_from_controls(
            [route.get("subgoal_control", {}) for route in routes if isinstance(route.get("subgoal_control"), dict)]
        ),
    }


def visual_tokens() -> dict[str, Any]:
    return {
        "lanes": {
            "target": {"label": "Target Spine", "color": "#f2c94c"},
            "dependency": {"label": "Dependency Frontier", "color": "#4cc9f0"},
            "conceptual": {"label": "Conceptual Pressure", "color": "#d65db1"},
            "candidate": {"label": "Candidate Routes", "color": "#64d68a"},
            "validation": {"label": "Validation Gates", "color": "#7aa2ff"},
            "milestone": {"label": "Success Milestones", "color": "#2fd6b5"},
            "drift": {"label": "Drift Guard", "color": "#ffb454"},
            "reflection": {"label": "Reflection", "color": "#c7a6ff"}
        },
        "statuses": {
            "evidence-backed": {"label": "Evidence backed", "color": "#64d68a"},
            "proof-obligation": {"label": "Proof obligation", "color": "#f2c94c"},
            "conjectural": {"label": "Conjectural", "color": "#7aa2ff"},
            "blocked": {"label": "Blocked", "color": "#ff6678"},
            "watch/archive": {"label": "Watch/archive", "color": "#9ea7b3"}
        },
        "salience": {
            "critical": "#ff6678",
            "high": "#f2c94c",
            "medium": "#4cc9f0",
            "low": "#9ea7b3"
        }
    }


def build_packet() -> dict[str, Any]:
    target = load_json_object(ROOT / "agentic/state/current_target.json")
    kb_ref = kb_ref_from_path(repo_path(target["kb_path"], must_exist=True))
    graph_path = f"agentic/state/dependency_graphs/{kb_ref}.json"
    graph = load_json_object(ROOT / graph_path)
    reasoning = load_json_object(ROOT / "agentic/reports/reasoning_progress/latest.json")
    hypothesis = load_json_object(ROOT / "artifacts/hegelian/hypothesis_exploration_map.json")
    stale = load_json_object(ROOT / "agentic/reports/stale_workflows/latest.json")
    skill_depth = load_optional_json(ROOT / "agentic/reports/skill_depth/latest.json")
    bridge_packets = load_optional_json(ROOT / "agentic/reports/yang_mills_bridge_lemma_packets/latest.json")
    contradiction_validation = load_optional_json(ROOT / "agentic/reports/proof_by_contradiction_validation/latest.json")
    empirical_evidence = load_optional_json(ROOT / "agentic/reports/empirical_evidence_requests/latest.json")
    abstraction_chain = load_optional_json(ROOT / "agentic/reports/abstraction_chains/latest.json")
    discovery_stretch = load_optional_json(ROOT / "agentic/reports/discovery_stretch/latest.json")
    discovery_marathon = load_optional_json(ROOT / "agentic/reports/discovery_marathon/latest.json")
    qualitative_graph_path = ROOT / "agentic/state/qualitative_mechanistic_graphs" / f"{target['target_id']}.json"
    qualitative_graph = load_optional_json(qualitative_graph_path)
    ledger_path = ROOT / "agentic/state/essential_target_ledgers" / f"{kb_ref}.json"
    ledger = load_json_object(ledger_path) if ledger_path.exists() else {}
    frontier = build_frontier(graph)
    routes = build_candidate_routes(hypothesis)
    contradiction_routes = build_contradiction_routes(bridge_packets, contradiction_validation)
    empirical_requests = empirical_evidence.get("requests", []) if isinstance(empirical_evidence.get("requests"), list) else []
    events = reasoning.get("events", [])
    source_artifacts = [
        {"path": "agentic/state/current_target.json", "role": "active target"},
        {"path": graph_path, "role": "active dependency graph"},
        {"path": f"agentic/reports/dependency_closure/{kb_ref}.md", "role": "dependency closure report"},
        {"path": "artifacts/hegelian/hypothesis_exploration_map.json", "role": "hypothesis exploration map"},
        {"path": "artifacts/hegelian/candidate_rankings.json", "role": "candidate rankings"},
        {"path": "artifacts/hegelian/validation_packets.json", "role": "validation packets"},
        {"path": "agentic/reports/reasoning_progress/latest.json", "role": "reasoning progress events"},
        {"path": "agentic/reports/stale_workflows/latest.json", "role": "stale workflow preflight"},
        {"path": f"agentic/state/essential_target_ledgers/{kb_ref}.json", "role": "essential target ledger"},
        {"path": "agentic/reports/skill_depth/latest.json", "role": "skill-depth audit"},
        {"path": "agentic/reports/yang_mills_bridge_lemma_packets/latest.json", "role": "Yang-Mills bridge and contradiction branches"},
        {"path": "agentic/reports/proof_by_contradiction_validation/latest.json", "role": "proof-by-contradiction route validation"},
        {"path": "agentic/reports/empirical_evidence_requests/latest.json", "role": "closely related empirical evidence requests"},
        {"path": "agentic/reports/abstraction_chains/latest.json", "role": "abstraction-chain machinery planning"},
        {"path": "artifacts/hegelian/machinery_selection_packets.json", "role": "machinery-selection packets"},
        {"path": "agentic/reports/discovery_stretch/latest.json", "role": "large-stretch discovery exploration"},
        {"path": "agentic/reports/discovery_marathon/latest.json", "role": "long-horizon discovery marathon"},
        {"path": "agentic/registries/discovery_marathon_skill_dispatch.yaml", "role": "marathon skill-dispatch matrix"},
        {"path": f"agentic/state/qualitative_mechanistic_graphs/{target['target_id']}.json", "role": "qualitative mechanistic graph"},
        {"path": "agentic/reports/qualitative_relation_packets/latest.json", "role": "qualitative relation packets"},
    ]
    packet = {
        "version": 1,
        "generated_utc": utc_now(),
        "target": {
            "target_id": target["target_id"],
            "raw_goal": target["raw_goal"],
            "kb_path": target["kb_path"],
            "main_claim_ids": target.get("main_claim_ids", []),
            "desired_output_type": target.get("desired_output_type", ""),
            "quality_criteria": target.get("quality_criteria", []),
            "known_constraints": target.get("known_constraints", []),
            "unknowns": target.get("unknowns", []),
        },
        "target_spine": target_spine(target, ledger),
        "reasoning_events": {
            "event_count": reasoning.get("event_count", len(events)),
            "events": events,
        },
        "frontier": frontier,
        "conceptual_pressure": {
            "summary": hypothesis.get("summary", {}),
            "pressure_packets": hypothesis.get("pressure_packets", [])[:80],
            "creative_operations": hypothesis.get("summary", {}).get("creative_operations", {}),
        },
        "interpretative_strategy_story": interpretative_strategy_story(routes, contradiction_routes),
        "success_milestones": success_milestones(routes),
        "machinery_selection": machinery_monitor_section(routes, abstraction_chain),
        "formal_subgoal_control_policy": FORMAL_SUBGOAL_CONTROL_POLICY,
        "reorientation_control": strategic_reorientation_control(routes, frontier),
        "contradiction_routes": {
            "title": "Proof-by-contradiction branches",
            "purpose": "Track reductio routes as controlled mathematical pressure tests with exact negation, same-theory carriers, conflict targets, obligations, and audit verdicts.",
            "total": len(contradiction_routes),
            "validation_summary": contradiction_validation.get("summary", {}),
            "generative_review": contradiction_validation.get("generative_review", {}),
            "items": contradiction_routes,
        },
        "empirical_evidence_requests": {
            "title": "Closely Related Empirical Evidence Requests",
            "purpose": (
                "Expose when a theoretical proof step needs nearby empirical, lattice, numerical, or simulation evidence. "
                "Each request states a transfer gap and proof boundary. These requests can guide route priority, identify witnesses, "
                "refine assumptions, or trigger demotion, but they do not replace proof obligations."
            ),
            "total": len(empirical_requests),
            "source_artifact": "agentic/reports/empirical_evidence_requests/latest.json",
            "items": empirical_requests,
        },
        "discovery_stretch": {
            "title": "Large-Stretch Discovery Exploration",
            "purpose": (
                "Track a larger batch of mathematically typed discovery programs. Each program names a controlled interface, "
                "equations with validity conditions, falsifiers, next experiments, promotion signals, and pivot signals."
            ),
            "quality_gate": discovery_stretch.get("quality_gate", ""),
            "stretch_thesis": discovery_stretch.get("stretch_thesis", ""),
            "role_counts": discovery_stretch.get("role_counts", {}),
            "programs": discovery_stretch.get("programs", []),
            "next_run_queue": discovery_stretch.get("next_run_queue", []),
            "source_artifact": "agentic/reports/discovery_stretch/latest.json",
        },
        "discovery_marathon": {
            "title": "Discovery Marathon",
            "purpose": (
                "Track the long-horizon recursive run as durable branch memory, cycle learning, skill-dispatch traces, "
                "deep reviews, and controlled promotion decisions. This is the operational layer that lets discovery run "
                "for hours while preserving the target spine and avoiding low-value drift. The What Actually Changed section "
                "separates mathematical learning from workflow bookkeeping."
            ),
            "run_id": discovery_marathon.get("run_id", ""),
            "target_id": discovery_marathon.get("target_id", ""),
            "status": discovery_marathon.get("status", "no_active_run"),
            "cycle_count": discovery_marathon.get("cycle_count", 0),
            "research_cycle_count": discovery_marathon.get("research_cycle_count", 0),
            "synthetic_cycle_count": discovery_marathon.get("synthetic_cycle_count", 0),
            "wall_clock_budget_minutes": discovery_marathon.get("wall_clock_budget_minutes", 0),
            "cycle_minutes": discovery_marathon.get("cycle_minutes", 0),
            "branch_summaries": discovery_marathon.get("branch_summaries", []),
            "cycle_summaries": discovery_marathon.get("cycle_summaries", []),
            "deep_reviews": discovery_marathon.get("deep_reviews", []),
            "what_actually_changed": discovery_marathon.get("what_actually_changed", []),
            "next_queue": discovery_marathon.get("next_queue", []),
            "breakthrough_status": discovery_marathon.get("breakthrough_status", "no_breakthrough_claimed"),
            "source_artifact": "agentic/reports/discovery_marathon/latest.json",
        },
        "qualitative_mechanistic_graph": {
            "title": "Qualitative Mechanistic Graph",
            "purpose": (
                "Accumulate qualitative physics understanding as typed variables, regimes, mechanisms, constraints, and relation edges. "
                "This graph records how quantities are believed to influence one another, under which regimes, with which assumptions, "
                "and with which epistemic status."
            ),
            "source_artifact": f"agentic/state/qualitative_mechanistic_graphs/{target['target_id']}.json",
            "summary": qualitative_graph.get("summary", {}),
            "nodes": qualitative_graph.get("nodes", []),
            "edges": qualitative_graph.get("edges", []),
            "updates": qualitative_graph.get("updates", []),
            "validation_handoff": qualitative_graph.get("validation_handoff", "python agentic/scripts/validate_qualitative_mechanistic_graph.py"),
        },
        "candidate_routes": routes,
        "proof_obligations": collect_proof_obligations(routes, frontier, contradiction_routes, empirical_requests),
        "evidence_ledger": evidence_ledger(source_artifacts, routes, events),
        "stale_workflow": {
            "active_target_id": stale.get("active_target_id"),
            "critical_findings": stale.get("critical_findings"),
            "historical_artifact_count": stale.get("historical_artifact_count"),
            "active_checks": stale.get("active_checks", []),
            "findings": stale.get("findings", []),
        },
        "skill_depth": {
            "summary": skill_depth.get("summary", {}),
            "report": "agentic/reports/skill_depth/latest.md",
        },
        "visual_tokens": visual_tokens(),
        "source_artifacts": [file_card(row["path"], row["role"]) for row in source_artifacts],
        "validation": {
            "active_target_match": target["target_id"] == graph.get("target_id") == hypothesis.get("target_id") == reasoning.get("target_id"),
            "missing_evidence_count": 0,
            "historical_artifacts_are_non_active": stale.get("critical_findings") == 0,
        },
    }
    packet["validation"]["missing_evidence_count"] = len(packet["evidence_ledger"]["missing"])
    return packet


def main() -> int:
    packet = build_packet()
    write_json(OUT, packet)
    print(f"Wrote {rel(OUT)} for {packet['target']['target_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
