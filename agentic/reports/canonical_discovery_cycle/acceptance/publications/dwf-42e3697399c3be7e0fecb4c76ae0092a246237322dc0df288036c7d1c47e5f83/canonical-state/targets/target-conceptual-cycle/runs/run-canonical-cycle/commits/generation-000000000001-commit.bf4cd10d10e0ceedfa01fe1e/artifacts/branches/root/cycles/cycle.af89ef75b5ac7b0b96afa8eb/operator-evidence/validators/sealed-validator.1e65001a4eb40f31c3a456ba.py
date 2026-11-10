#!/usr/bin/env python3
"""Independently validate one central operator's exact dispatcher artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping


CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    Namespace,
    canonical_digest,
    load_json,
    validate_payload,
    verify_artifact_descriptor,
)
from agentic.discovery.hypotheses import validate_high_risk_portfolio  # noqa: E402
from agentic.discovery.literature import validate_assimilation, validate_snapshot  # noqa: E402
from agentic.discovery.parallel import validate_parallel_portfolio  # noqa: E402
from agentic.discovery.reflection import validate_packet_invariants  # noqa: E402
from agentic.experiments import (  # noqa: E402
    compile_experiment_spec,
    triage_probe,
    validate_experiment_receipt,
)


SUPPORTED_OPERATORS = {
    "reflective-conceptual-discovery",
    "reflective-theory-synthesizer",
    "frontier-literature-assimilator",
    "high-risk-hypothesis-forger",
    "parallel-hypothesis-portfolio",
    "dynamic-symbolic-simulation-experimenter",
}


def _read_protocol(workspace: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise ContractError(f"validator stdin is not protocol JSON: {exc}") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("request"), dict):
        raise ContractError("validator protocol requires a request object")
    request = payload["request"]
    namespace = Namespace.from_mapping(request["identity"])
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != 1:
        raise ContractError("validator requires exactly one output artifact")
    output_path = verify_artifact_descriptor(artifacts[0], workspace, namespace)
    if artifacts[0]["path"] not in request["declared_outputs"]:
        raise ContractError("validator output is not declared by the request")
    inputs = request.get("input_artifacts")
    if not isinstance(inputs, list) or len(inputs) != 1:
        raise ContractError("validator requires exactly one input envelope")
    input_path = verify_artifact_descriptor(inputs[0], workspace, namespace)
    output = load_json(output_path)
    envelope = load_json(input_path)
    if not isinstance(output, dict) or not isinstance(envelope, dict):
        raise ContractError("operator input and output must both be JSON objects")
    return request, envelope, output


def _identity(output: Mapping[str, Any], request: Mapping[str, Any]) -> None:
    identity = request["identity"]
    for field in ("target_id", "run_id", "branch_id", "state_version"):
        if field in output and output[field] != identity[field]:
            raise ContractError(f"operator output/request identity mismatch for {field}")


def validate(operator_id: str, request: Mapping[str, Any], envelope: Mapping[str, Any], output: Mapping[str, Any]) -> None:
    if request.get("operator", {}).get("operator_id") != operator_id:
        raise ContractError("validator argv operator differs from request")
    _identity(output, request)
    if operator_id in {"reflective-conceptual-discovery", "reflective-theory-synthesizer"}:
        validate_payload(dict(output), "reflective_conceptual_discovery_packet.schema.json")
        unsigned = dict(output)
        claimed = unsigned.pop("packet_digest")
        if claimed != canonical_digest(unsigned):
            raise ContractError("reflective packet digest mismatch")
        validate_packet_invariants(output)
        return
    if operator_id == "frontier-literature-assimilator":
        snapshot = envelope.get("snapshot")
        if not isinstance(snapshot, Mapping):
            raise ContractError("literature validator lacks frozen snapshot")
        validate_snapshot(snapshot)
        validate_assimilation(output, snapshot=snapshot)
        expected = (
            ("local_only", "blocked_local_only", "provisional_local_only")
            if snapshot["provenance_mode"] == "local_only"
            else ("live", "pass", "current")
        )
        actual = (
            output["selected_snapshot"]["provenance_mode"],
            output["resolution"]["active_investment_gate"],
            output["hypothesis_rebase_status"],
        )
        if actual != expected:
            raise ContractError(
                "literature assimilation changed the frozen snapshot's provenance authority: "
                f"expected {expected}, got {actual}"
            )
        return
    if operator_id == "high-risk-hypothesis-forger":
        snapshot = envelope.get("literature_snapshot")
        charter = envelope.get("charter")
        if not isinstance(snapshot, Mapping) or not isinstance(charter, Mapping):
            raise ContractError("hypothesis validator lacks charter or frozen snapshot")
        validate_snapshot(snapshot)
        if (
            charter.get("target_id") != request["identity"]["target_id"]
            or snapshot.get("target_id") != request["identity"]["target_id"]
            or charter.get("theory_state_digest") != snapshot.get("theory_state_digest")
        ):
            raise ContractError("hypothesis input identity or theory digest mismatch")
        assimilation = envelope.get("assimilation_packet")
        if assimilation is not None:
            if not isinstance(assimilation, Mapping):
                raise ContractError("assimilation_packet must be an object")
            validate_assimilation(assimilation, snapshot=snapshot)
        validate_high_risk_portfolio(output)
        return
    if operator_id == "parallel-hypothesis-portfolio":
        validate_parallel_portfolio(output)
        source = envelope.get("high_risk_portfolio", {})
        if not isinstance(source, Mapping):
            raise ContractError("parallel validator lacks high_risk_portfolio")
        validate_high_risk_portfolio(source)
        if output.get("base_theory_state_version") != request["identity"]["state_version"]:
            raise ContractError("parallel output is bound to the wrong theory state version")
        hypotheses = {
            str(item.get("hypothesis_id")): item
            for item in source.get("hypotheses", [])
            if isinstance(item, Mapping)
        }
        selected_seeds = envelope.get("branch_seeds") or source.get(
            "parallel_branch_seeds", []
        )
        for seed in selected_seeds:
            candidate = hypotheses.get(str(seed.get("hypothesis_id")))
            rebase = candidate.get("literature_rebase_receipt", {}) if candidate else {}
            if (
                not candidate
                or candidate.get("concept_lifecycle_state") != "literature_rebased"
                or rebase.get("status") != "completed"
            ):
                raise ContractError(
                    "parallel output was produced without a completed non-local literature rebase"
                )
        return
    if operator_id == "dynamic-symbolic-simulation-experimenter":
        triage = triage_probe(envelope["triage_request"])
        if triage["decision"] != "commission":
            raise ContractError("experiment output lacks a valid theory commission")
        spec = compile_experiment_spec(triage, envelope["experiment_request"])
        validate_experiment_receipt(output, spec)
        if request.get("parameters", {}).get("theory_commissioned") is not True:
            raise ContractError("experiment request lacks theory commission binding")
        return
    raise ContractError(f"unsupported central discovery operator: {operator_id}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operator-id", choices=sorted(SUPPORTED_OPERATORS), required=True)
    parser.add_argument("--workspace", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    try:
        request, envelope, output = _read_protocol(args.workspace.resolve())
        validate(args.operator_id, request, envelope, output)
        return 0
    except (ContractError, KeyError, TypeError, ValueError, OSError) as exc:
        print(f"independent operator validation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
