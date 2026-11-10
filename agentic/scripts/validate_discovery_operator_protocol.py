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
"""Independently validate one central operator's exact dispatcher artifacts."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
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
from agentic.discovery.conceptual_adjudication import (  # noqa: E402
    validate_adjudication_evidence,
    validate_sealed_preference_authority,
)
from agentic.discovery.formal_claim_authority import (  # noqa: E402
    build_formal_claim_producer_output,
    validate_formal_claim_producer_input,
    validate_formal_claim_producer_output,
)
from agentic.discovery.hypotheses import forge_high_risk_portfolio, validate_high_risk_portfolio  # noqa: E402
from agentic.discovery.literature import validate_assimilation, validate_snapshot  # noqa: E402
from agentic.discovery.parallel import validate_parallel_portfolio  # noqa: E402
from agentic.discovery.reflection import validate_packet_invariants  # noqa: E402
from agentic.experiments import (  # noqa: E402
    triage_probe,
    validate_commissioned_experiment_spec,
    validate_experiment_receipt,
)
from agentic.scripts.run_discovery_operator_protocol import (  # noqa: E402
    _previous_adjudication_evidence,
    _validated_proposal_field_free_inputs,
)


SUPPORTED_OPERATORS = {
    "reflective-conceptual-discovery",
    "reflective-theory-synthesizer",
    "frontier-literature-assimilator",
    "high-risk-hypothesis-forger",
    "parallel-hypothesis-portfolio",
    "dynamic-symbolic-simulation-experimenter",
    "blind-conceptual-preference-adjudicator",
    "formal-claim-producer",
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


def validate(operator_id: str, request: Mapping[str, Any], envelope: Mapping[str, Any], output: Mapping[str, Any], *, workspace: Path) -> None:
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
        if envelope.get("revise_after_adjudication"):
            from agentic.discovery.reflection import validate_synthesis_revision
            validate_synthesis_revision(envelope)
            if output.get("conceptual_adjudication_evidence") is not None:
                raise ContractError("a revised synthesis cannot retain stale preference authority")
            if output.get("parent_adjudication_evidence") != envelope.get("previous_evidence"):
                raise ContractError("revised synthesis must retain its exact parent critique separately")
            if (output["conceptual_systems"] != envelope["conceptual_systems"]
                    or output["reflection_rounds"] != envelope["reflection_rounds"]):
                raise ContractError("revised synthesis differs from its frozen authored content")
        return
    if operator_id == "formal-claim-producer":
        validate_formal_claim_producer_input(envelope, workspace=workspace)
        validated = validate_formal_claim_producer_output(output)
        identity = request["identity"]
        if (
            validated["target_id"] != identity["target_id"]
            or validated["run_id"] != identity["run_id"]
            or validated["branch_id"] != identity["branch_id"]
            or validated["source_theory_generation"]
            != identity["state_version"] + 1
        ):
            raise ContractError(
                "formal-claim producer output crossed its dispatcher namespace"
            )
        expected = build_formal_claim_producer_output(envelope, workspace=workspace)
        if validated != expected:
            raise ContractError(
                "formal-claim producer output differs from independent exact replay"
            )
        return
    if operator_id == "blind-conceptual-preference-adjudicator":
        systems = envelope.get("systems")
        rounds = envelope.get("reflection_rounds")
        genealogy = envelope.get("frozen_genealogy")
        bindings = envelope.get("candidate_bindings")
        if not all(isinstance(value, list) for value in (systems, rounds, genealogy)):
            raise ContractError("conceptual adjudication validator lacks exact source collections")
        if not isinstance(bindings, Mapping):
            raise ContractError("conceptual adjudication validator lacks private candidate bindings")
        context = {
            "systems": systems,
            "reflection_rounds": rounds,
            "frozen_genealogy": genealogy,
            "candidate_bindings": bindings,
            "theory_state_digest": envelope.get("theory_state_digest"),
            "literature_snapshot_digest": envelope.get("literature_snapshot_digest"),
            "high_risk_portfolio_digest": envelope.get("high_risk_portfolio_digest"),
            "proposer_receipt_ids": envelope.get("proposer_receipt_ids"),
            "previous_evidence": _previous_adjudication_evidence(envelope),
        }
        validate_adjudication_evidence(output, **context)
        validate_sealed_preference_authority(
            output,
            target_id=str(request["identity"]["target_id"]),
            run_id=str(request["identity"]["run_id"]),
            state_version=int(request["identity"]["state_version"]),
            stage_id=str(output["stage_id"]),
            system_ids=[str(row["system_id"]) for row in systems],
            systems=systems,
            reflection_rounds=rounds,
        )
        return
    if operator_id == "frontier-literature-assimilator":
        snapshot = envelope.get("snapshot")
        if not isinstance(snapshot, Mapping):
            raise ContractError("literature validator lacks frozen snapshot")
        validate_snapshot(snapshot)
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
        validate_assimilation(output, snapshot=snapshot)
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
        upstream = _validated_proposal_field_free_inputs(
            request,
            envelope,
            workspace=workspace,
            charter=charter,
            snapshot=snapshot,
        )
        validate_high_risk_portfolio(output)
        if envelope.get("authored_proposals") is not None:
            if upstream is not None:
                raise ContractError("authored proposals cannot claim proposal-field-free study authority")
            parameters = request.get("parameters", {})
            expected = forge_high_risk_portfolio(charter, snapshot,
                proposals=envelope["authored_proposals"], requested_count=int(parameters.get("requested_count", 10)),
                relevance_floor=float(parameters.get("relevance_floor", 0.70)))
            if output != expected:
                raise ContractError("hypothesis output differs from the exact authored-proposal input")
        if upstream is not None and output != envelope.get("selected_portfolio"):
            raise ContractError("hypothesis output differs from recursively sealed selected portfolio")
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
        spec = validate_commissioned_experiment_spec(
            envelope["triage_request"],
            envelope["experiment_request"],
            envelope["experiment_spec"],
        )
        with tempfile.TemporaryDirectory(
            prefix="abducer-independent-experiment-replay-"
        ) as raw:
            validate_experiment_receipt(
                output,
                spec,
                work_directory=Path(raw),
            )
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
        workspace = args.workspace.resolve()
        request, envelope, output = _read_protocol(workspace)
        validate(args.operator_id, request, envelope, output, workspace=workspace)
        return 0
    except (ContractError, KeyError, TypeError, ValueError, OSError) as exc:
        diagnostic = " ".join(str(exc).split())
        if len(diagnostic) > 4096:
            diagnostic = diagnostic[:4080] + "...[truncated]"
        print(f"independent operator validation failed: {diagnostic}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
