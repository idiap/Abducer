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

"""Build stepwise abstraction-chain packets for target-led machinery choice."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, kb_ref_from_path, load_json_object, rel, repo_path, stable_id, utc_now, write_json


OUT_JSON = ROOT / "agentic/reports/abstraction_chains/latest.json"
OUT_MD = ROOT / "agentic/reports/abstraction_chains/latest.md"


def load_target_contract(target: dict[str, Any]) -> dict[str, Any]:
    kb_ref = kb_ref_from_path(repo_path(str(target["kb_path"]), must_exist=True))
    ledger_path = ROOT / "agentic/state/essential_target_ledgers" / f"{kb_ref}.json"
    if not ledger_path.exists():
        return {}
    return load_json_object(ledger_path).get("target_object_contract", {})


def yang_mills_chain(target: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    nodes = [
        {
            "node_id": "raw_target",
            "role": "target",
            "object": contract.get("exact_target_object", target.get("raw_goal", "")),
            "why_needed": "The machinery must preserve the exact problem rather than solve a nearby regulated, lower-dimensional, or heuristic proxy.",
        },
        {
            "node_id": "regulated_gauge_fields",
            "role": "constructed_object",
            "object": "Regulated compact-simple Yang-Mills gauge-field ensemble with ultraviolet cutoff and infrared volume control.",
            "why_needed": "Construction machinery needs a source object whose limits can be analyzed without losing gauge structure.",
        },
        {
            "node_id": "continuum_schwinger_functions",
            "role": "representation",
            "object": "Continuum gauge-invariant Schwinger functions S_n for observables such as Wilson-loop or local curvature-composite families.",
            "why_needed": "Schwinger data are the Euclidean representation on which OS reconstruction and correlator decay can act.",
        },
        {
            "node_id": "invariant_layer",
            "role": "invariant_preservation",
            "object": "Gauge invariance, OS positivity, Euclidean covariance, nontrivial connected sector, and same-theory identity.",
            "why_needed": "These invariants prevent the chain from changing the theory while passing through limits and reconstructions.",
        },
        {
            "node_id": "os_reconstruction",
            "role": "transfer",
            "object": "Reconstructed physical Hilbert space H_YM, vacuum Omega, Hamiltonian H, and gauge-invariant observable algebra.",
            "why_needed": "Hamiltonian spectral claims are meaningful only after Euclidean data transfer into a positive-energy quantum theory.",
        },
        {
            "node_id": "spectral_witness",
            "role": "witness",
            "object": "Cutoff-uniform Euclidean decay or spectral-measure support away from zero for a spectrally determining observable family.",
            "why_needed": "The mass gap needs a witness that excludes arbitrarily soft non-vacuum excitations in the reconstructed theory.",
        },
        {
            "node_id": "hamiltonian_mass_gap",
            "role": "final_claim",
            "object": "Spec(H on P_perp H_YM) subset [Delta, infinity) for some Delta > 0 in the same nontrivial theory.",
            "why_needed": "This is the final Clay mass-gap commitment after construction, reconstruction, nontriviality, and witness transfer are certified.",
        },
    ]
    edges = [
        {
            "from": "raw_target",
            "to": "regulated_gauge_fields",
            "bridge_obligation": "Choose a regulator without weakening compact simple gauge Yang-Mills on R^4.",
            "assumptions": ["target_object_contract", "accepted regulator family"],
            "output": "regulated source objects for construction machinery",
            "failure_mode": "The route begins by solving a different model.",
            "validator_handoff": "agentic/scripts/validate_target_relevance.py",
        },
        {
            "from": "regulated_gauge_fields",
            "to": "continuum_schwinger_functions",
            "bridge_obligation": "RG-to-Schwinger continuum-passage lemma with topology, tightness/convergence, and gauge-invariant observable survival.",
            "assumptions": ["uniform multiscale estimates", "cutoff-removal regime", "observable definitions"],
            "output": "candidate continuum Schwinger functions",
            "failure_mode": "Only finite-volume, fixed-cutoff, or small-field control is obtained.",
            "validator_handoff": "agentic/scripts/validate_hypothesis_exploration.py",
        },
        {
            "from": "continuum_schwinger_functions",
            "to": "invariant_layer",
            "bridge_obligation": "Closedness and preservation lemma for reflection positivity, covariance, gauge invariance, and nontrivial connected correlations.",
            "assumptions": ["limit topology where positivity is closed", "same observable algebra", "non-Gaussian witness candidate"],
            "output": "OS-positive nontrivial same-theory Schwinger data",
            "failure_mode": "The continuum limit exists but is trivial, non-positive, or no longer gauge-invariant.",
            "validator_handoff": "agentic/scripts/validate_yang_mills_bridge_lemma_packets.py",
        },
        {
            "from": "invariant_layer",
            "to": "os_reconstruction",
            "bridge_obligation": "OS reconstruction packet naming H_YM, Omega, H, null quotient, domains, and gauge-invariant observables.",
            "assumptions": ["OS axioms", "nontriviality after null quotient", "observable algebra"],
            "output": "physical Hilbert-space and Hamiltonian objects",
            "failure_mode": "Hamiltonian notation is postulated rather than reconstructed.",
            "validator_handoff": "agentic/scripts/validate_reasoning_monitor.py",
        },
        {
            "from": "os_reconstruction",
            "to": "spectral_witness",
            "bridge_obligation": "Observable-density and decay-to-spectrum lemma connecting Euclidean correlations to spectral support of H.",
            "assumptions": ["spectrally determining observable family", "cutoff-uniform constants", "same reconstructed Hamiltonian"],
            "output": "spectral measures with support bounded away from zero",
            "failure_mode": "Decay is true only in a regulated sector or for observables too small to determine excitations.",
            "validator_handoff": "agentic/scripts/validate_long_horizon_probe.py",
        },
        {
            "from": "spectral_witness",
            "to": "hamiltonian_mass_gap",
            "bridge_obligation": "Spectrum-to-gap endpoint lemma proving E_H((0, Delta)) P_perp = 0 for one Delta > 0.",
            "assumptions": ["vacuum projection", "positive self-adjoint H", "same-theory spectral witness"],
            "output": "positive Hamiltonian mass gap",
            "failure_mode": "The witness does not cover the full vacuum-orthogonal sector.",
            "validator_handoff": "agentic/scripts/validate_big_deal_goal_archive.py",
        },
    ]
    return {
        "chain_id": stable_id("abstraction-chain", target["target_id"], "yang-mills"),
        "target_id": target["target_id"],
        "status": "open_obligation_chain",
        "interpretation": "The best machinery is not a single method; it is the ordered chain that lets construction, representation, invariants, transfer, witness, and validation act on one target object.",
        "nodes": nodes,
        "bridge_obligations": edges,
        "role_alignment": {
            "construction": "RG and multiscale control act from regulated gauge fields to continuum Schwinger data.",
            "representation": "Schwinger functions represent the Euclidean theory in a form that reconstruction and decay estimates can inspect.",
            "invariant_preservation": "Gauge invariance, reflection positivity, nontriviality, and same-theory identity must survive every arrow.",
            "transfer": "OS reconstruction transfers Euclidean data to Hilbert-space spectral semantics.",
            "witness": "Euclidean decay and spectral measures witness the absence of low-energy non-vacuum excitations.",
            "validation": "Same-theory and cutoff-uniform checks certify that the final gap belongs to the Clay target.",
        },
    }


def render_markdown(packet: dict[str, Any]) -> str:
    lines = [
        "# Abstraction Chain Packet",
        "",
        f"- Target: `{packet['target_id']}`",
        f"- Status: `{packet['status']}`",
        "",
        packet["interpretation"],
        "",
        "## Nodes",
        "",
    ]
    for node in packet["nodes"]:
        lines.append(f"- `{node['node_id']}` `{node['role']}`: {node['object']}")
        lines.append(f"  - Why needed: {node['why_needed']}")
    lines.extend(["", "## Bridge Obligations", ""])
    for edge in packet["bridge_obligations"]:
        lines.append(f"- `{edge['from']}` -> `{edge['to']}`: {edge['bridge_obligation']}")
        lines.append(f"  - Assumptions: `{', '.join(edge['assumptions'])}`")
        lines.append(f"  - Output: {edge['output']}")
        lines.append(f"  - Failure mode: {edge['failure_mode']}")
        lines.append(f"  - Validator handoff: `{edge['validator_handoff']}`")
    lines.extend(["", "## Role Alignment", ""])
    for role, description in packet["role_alignment"].items():
        lines.append(f"- `{role}`: {description}")
    return "\n".join(lines) + "\n"


def main() -> int:
    target = load_json_object(ROOT / "agentic/state/current_target.json")
    contract = load_target_contract(target)
    packet = yang_mills_chain(target, contract)
    write_json(OUT_JSON, packet)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_markdown(packet), encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
