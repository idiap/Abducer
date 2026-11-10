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
"""Validate one executable discovery cycle as an integrated causal system.

Individual schema validators answer whether one artifact is internally valid.
This release-oriented validator answers the stronger question required by the
discovery TODOs: did all six registered operators execute on one frozen
target/run/state lineage, did their exact output bytes causally enter one
immutable canonical commit, and did theory remain the controller of optional
proof and experiment support?

The command is intentionally path-explicit.  It never discovers a mutable
``latest`` result and never substitutes a demo packet for acceptance evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "agentic/scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "agentic/scripts"))

from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    canonical_digest,
    load_json,
    resolve_workspace_path,
    validate_instance,
    validate_payload,
)
from agentic.discovery.evaluation import validate_evaluation_receipt  # noqa: E402
from agentic.discovery.hypotheses import validate_high_risk_portfolio  # noqa: E402
from agentic.discovery.literature import validate_assimilation, validate_snapshot  # noqa: E402
from agentic.discovery.parallel import validate_parallel_portfolio  # noqa: E402
from agentic.discovery.receipts import ensure_evaluation_ready  # noqa: E402
from agentic.discovery.reflection import validate_packet_invariants  # noqa: E402
from agentic.discovery.theory_gate import verify_canonical_theory_cycle  # noqa: E402
from agentic.experiments import (  # noqa: E402
    receipt_staleness,
    validate_experiment_receipt,
)
from discovery_operator_registry import REGISTRY_PATH, load_registry  # noqa: E402
from dispatch_discovery_operators import _bindings as registry_bindings  # noqa: E402
from run_skill_reachability_audit import build_reachability_report  # noqa: E402


EXPECTED_OPERATORS = {
    "dynamic-symbolic-simulation-experimenter",
    "frontier-literature-assimilator",
    "high-risk-hypothesis-forger",
    "parallel-hypothesis-portfolio",
    "reflective-conceptual-discovery",
    "reflective-theory-synthesizer",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(f"canonical discovery acceptance failed: {message}")


def _object(path: Path, label: str) -> dict[str, Any]:
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise ContractError(f"{label} must be a JSON object: {path}")
    return payload


def _role_paths(request: Mapping[str, Any], workspace: Path, role: str) -> list[Path]:
    roles = request.get("artifact_roles", {})
    _require(isinstance(roles, Mapping), "cycle request has no artifact role map")
    raw = roles.get(role)
    values = raw if isinstance(raw, list) else [raw]
    _require(values and all(isinstance(value, str) for value in values), f"missing role {role}")
    return [resolve_workspace_path(workspace, value, must_exist=True) for value in values]


def _validate_reflective_packet(packet: dict[str, Any]) -> None:
    validate_payload(packet, "reflective_conceptual_discovery_packet.schema.json")
    claimed = packet["packet_digest"]
    _require(
        claimed == canonical_digest(packet, exclude_keys=("packet_digest",)),
        "reflective packet digest mismatch",
    )
    validate_packet_invariants(packet)


def validate_canonical_acceptance(
    *,
    cycle_path: Path,
    cycle_request_path: Path,
    state_root: Path,
    workspace: Path,
    receipt_root: Path,
    target_id: str,
    run_id: str,
    registry_path: Path = REGISTRY_PATH,
    authority_repository_root: Path = ROOT,
) -> dict[str, Any]:
    """Validate exact artifacts and return a compact evidence summary.

    A six-route production cycle is additionally resolved through the current
    registry so every declared local validator dependency is re-hashed. Local
    control fixtures with different operator sets retain generic commit replay
    and fail later at their intended acceptance boundary.
    """

    cycle_path = cycle_path.resolve()
    cycle_request_path = cycle_request_path.resolve()
    state_root = state_root.resolve()
    workspace = workspace.resolve()
    receipt_root = receipt_root.resolve()
    cycle = _object(cycle_path, "canonical cycle projection")
    request = _object(cycle_request_path, "canonical cycle request")

    operator_requests = request.get("operator_requests")
    operator_receipts = request.get("operator_receipts")
    _require(isinstance(operator_requests, list), "cycle request lacks operator_requests")
    _require(isinstance(operator_receipts, list), "cycle request lacks operator_receipts")
    ensure_evaluation_ready(operator_requests, operator_receipts, workspace=workspace)

    request_operator_ids = {
        str(item.get("operator", {}).get("operator_id"))
        for item in operator_requests
        if isinstance(item, Mapping)
    }
    approved_bindings = None
    if request_operator_ids == EXPECTED_OPERATORS:
        approved_bindings = {
            binding.operator_id: binding
            for binding in registry_bindings(load_registry(registry_path))
        }
        _require(
            set(approved_bindings) == EXPECTED_OPERATORS,
            "current operator registry does not define the exact six acceptance routes",
        )

    authorization = verify_canonical_theory_cycle(
        cycle_path,
        target_id=target_id,
        run_id=run_id,
        state_root=state_root,
        # Stable acceptance fixtures prove immutable historical semantics.
        # Live consumers retain the gate's default wall-clock freshness check.
        require_current=False,
        approved_operator_bindings=approved_bindings,
        authority_repository_root=authority_repository_root,
    )
    reachability = build_reachability_report(
        receipt_root=receipt_root,
        artifact_root=workspace,
        canonical_cycle_path=cycle_path,
        canonical_state_root=state_root,
        target_id=target_id,
        run_id=run_id,
    )
    _require(
        reachability["all_operators_feedback_effective"] is True,
        f"six-operator feedback chain is incomplete: {reachability['evidence_errors']}",
    )
    operator_ids = {
        edge["producer_operator_id"] for edge in cycle.get("feedback_edges", [])
    }
    _require(operator_ids == EXPECTED_OPERATORS, "canonical feedback does not cover exactly six operators")

    snapshot = _object(_role_paths(request, workspace, "literature_snapshot")[0], "literature snapshot")
    validate_snapshot(snapshot)
    _require(
        snapshot["content_digest"] == cycle["literature_basis"]["snapshot_digest"],
        "cycle is not bound to the exact validated literature snapshot",
    )
    _require(
        snapshot.get("provenance_mode") == "live"
        and all(
            lane.get("execution_mode") == "live" and lane.get("status") == "completed"
            for lane in snapshot.get("lane_receipts", [])
        )
        and cycle["literature_basis"].get("active_investment_allowed") is True,
        "acceptance exercise must use provider-backed active-current literature",
    )

    assimilation = _object(
        _role_paths(request, workspace, "literature_assimilation")[0],
        "literature assimilation",
    )
    validate_assimilation(assimilation, snapshot=snapshot)
    _require(assimilation.get("theory_mappings"), "literature produced no causal theory mappings")

    high_risk = _object(
        _role_paths(request, workspace, "high_risk_portfolio")[0],
        "high-risk portfolio",
    )
    validate_high_risk_portfolio(high_risk)
    _require(
        high_risk.get("literature_snapshot_digest") == snapshot["content_digest"],
        "high-risk portfolio was not rebased on the frozen current snapshot",
    )

    parallel = _object(
        _role_paths(request, workspace, "parallel_portfolio")[0],
        "parallel portfolio",
    )
    validate_parallel_portfolio(parallel)
    _require(cycle["parallel_outcome"]["canonical_cas_commits"] == 1, "parallel merge is not one CAS commit")
    _require(cycle["parallel_outcome"]["retained_dissent_ids"], "parallel merge erased dissent")
    _require(
        cycle["parallel_outcome"]["failed_or_invalid_attempt_ids"],
        "acceptance exercise did not prove partial-failure preservation",
    )

    reflective_packets = [
        _object(path, "reflective packet")
        for path in _role_paths(request, workspace, "reflective_packets")
    ]
    _require(len(reflective_packets) == 2, "parent reflection and distinct synthesis are both required")
    for packet in reflective_packets:
        _validate_reflective_packet(packet)
    _require(
        canonical_digest(reflective_packets[0]) != canonical_digest(reflective_packets[1]),
        "theory synthesis did not materially change the reflective packet",
    )

    experiment = _object(
        _role_paths(request, workspace, "experiment_receipt")[0],
        "experiment receipt",
    )
    spec_matches = sorted(workspace.rglob(f"experiments/{experiment['experiment_id']}/spec.json"))
    _require(len(spec_matches) == 1, "exact frozen experiment specification is missing or ambiguous")
    experiment_spec = _object(spec_matches[0], "experiment specification")
    immutable_receipt = _object(spec_matches[0].parent / "receipt.json", "immutable experiment receipt")
    _require(
        canonical_digest(experiment) == canonical_digest(immutable_receipt),
        "operator experiment output differs from the immutable runtime receipt",
    )
    validate_experiment_receipt(
        immutable_receipt,
        experiment_spec,
        work_directory=spec_matches[0].parent,
    )
    _require(
        receipt_staleness(immutable_receipt, experiment_spec)["stale"] is False,
        "experiment receipt is stale",
    )
    assimilation_result = cycle["experiment_assimilation"]
    _require(assimilation_result.get("present") is True, "six-route exercise omitted experiment support")
    _require(
        assimilation_result.get("theory_selected") is False
        and assimilation_result.get("proof_authorized") is False,
        "support experiment assumed theory-selection or proof authority",
    )
    _require(
        all(action.get("kind") != "probe" for action in cycle["schedule"]["actions"]),
        "an assimilated experiment incorrectly scheduled a repeated probe",
    )

    evaluations = cycle.get("evaluation_receipts", [])
    _require(isinstance(evaluations, list) and evaluations, "independent evaluation receipts are absent")
    for evaluation in evaluations:
        validate_evaluation_receipt(evaluation)
        _require(
            evaluation["evaluator_identity"] != evaluation["proposer_identity"],
            "proposal and evaluation identities are not independent",
        )
        _require(
            evaluation.get("promotion_decision") == "not_requested",
            "conceptual evaluation was mistaken for established-claim promotion",
        )

    conceptual_authority = cycle.get("conceptual_authority", {})
    if "local_structural_fallback" in conceptual_authority.get("generation_modes", []):
        _require(
            conceptual_authority.get("fallback_disposition") == "maturation_only"
            and conceptual_authority.get("internal_correlated_rubric_pass") is False
            and conceptual_authority.get("external_depth_validation_status") == "unavailable"
            and conceptual_authority.get("external_understanding_validation_status") == "unavailable"
            and conceptual_authority.get("proof_ready") is False
            and cycle.get("proof_handoff") is None,
            "structural fallback was promoted into depth, understanding, or proof authority",
        )
        _require(
            all(
                evaluation.get("creative_worth_decision") in {
                    "incubate", "revise", "demote", "duplicate"
                }
                for evaluation in evaluations
            ),
            "fallback acceptance contradicts the independently evaluated incubation disposition",
        )

    if cycle.get("proof_handoff") is not None:
        validate_instance(cycle["proof_handoff"], "discovery_proof_handoff.schema.json")
        proof = cycle["proof_handoff"]
        _require(
            proof["branch_id"] in authorization["eligible_branch_ids"],
            "proof handoff is outside the canonical theory schedule",
        )
        _require(
            proof["obligation_id"] in cycle["identity_map"]["proof_obligation_ids"],
            "proof handoff obligation is outside the canonical identity map",
        )

    return {
        "schema_version": "1.0.0",
        "status": "passed",
        "target_id": target_id,
        "run_id": run_id,
        "cycle_id": cycle["cycle_id"],
        "commit_id": authorization["commit_id"],
        "manifest_digest": authorization["manifest_digest"],
        "operator_count": len(operator_ids),
        "all_operators_feedback_effective": True,
        "literature_mode": cycle["literature_basis"]["mode"],
        "literature_mapping_count": len(assimilation["theory_mappings"]),
        "high_risk_candidate_count": len(high_risk["hypotheses"]),
        "valid_parallel_branch_count": len(cycle["parallel_outcome"]["valid_branch_ids"]),
        "retained_dissent_count": len(cycle["parallel_outcome"]["retained_dissent_ids"]),
        "experiment_subordinate": True,
        "proof_handoff_count": 1 if cycle.get("proof_handoff") is not None else 0,
        "authority_boundary": cycle["authority_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycle", required=True, type=Path)
    parser.add_argument("--cycle-request", required=True, type=Path)
    parser.add_argument("--state-root", required=True, type=Path)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--receipt-root", required=True, type=Path)
    parser.add_argument("--target-id", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    try:
        result = validate_canonical_acceptance(
            cycle_path=args.cycle,
            cycle_request_path=args.cycle_request,
            state_root=args.state_root,
            workspace=args.workspace,
            receipt_root=args.receipt_root,
            target_id=args.target_id,
            run_id=args.run_id,
        )
    except (ContractError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
