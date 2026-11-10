# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Evidence-sensitive release and executable registry regression tests."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from discovery_operator_registry import load_registry  # noqa: E402
from dispatch_discovery_operators import _bindings  # noqa: E402
from validate_target_navigation_release import ReleaseValidationError, validate_release_receipt  # noqa: E402
from run_target_navigation import build_release_receipt, new_run_id  # noqa: E402


def digest(label: str) -> str:
    return "sha256:" + hashlib.sha256(label.encode()).hexdigest()


def canonical_digest(payload: dict) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def canonical_evidence() -> dict:
    operators = [
        "dynamic-symbolic-simulation-experimenter",
        "frontier-literature-assimilator",
        "high-risk-hypothesis-forger",
        "parallel-hypothesis-portfolio",
        "reflective-conceptual-discovery",
        "reflective-theory-synthesizer",
    ]
    evidence = {
        "status": "verified_active_current",
        "authoritative": True,
        "target_id": "target-a",
        "canonical_run_id": "canonical-run-a",
        "cycle_id": "cycle-a",
        "prior_state_version": 2,
        "committed_state_version": 3,
        "commit_id": "commit-a",
        "manifest_digest": digest("manifest"),
        "projection_digest": digest("projection"),
        "operator_evidence_digest": digest("operator-evidence"),
        "literature_snapshot_id": "literature.target-a.3",
        "literature_snapshot_digest": digest("literature"),
        "operator_count": 6,
        "all_operators_feedback_effective": True,
        "operator_bindings": [
            {
                "operator_id": operator,
                "receipt_ids": [f"receipt-{index}"],
                "feedback_event_ids": [f"event-{index}"],
            }
            for index, operator in enumerate(operators, 1)
        ],
        "schedule_id": "schedule-a",
        "branch_authorizations": [{
            "branch_id": "branch-a",
            "action_ids": ["action-a"],
            "action_kinds": ["reflect"],
        }],
        "authorization_semantics": "exact canonical schedule binding",
    }
    evidence["evidence_digest"] = canonical_digest(evidence)
    return evidence


def sign(payload: dict) -> dict:
    payload.pop("receipt_digest", None)
    payload["receipt_digest"] = canonical_digest(payload)
    return payload


def valid_release() -> dict:
    return sign({
        "schema_version": "1.0.0",
        "release_id": "release.valid.001",
        "target_id": "target-a",
        "run_id": "run-a",
        "state_version": 3,
        "literature_snapshot_id": "literature.target-a.3",
        "literature_snapshot_digest": digest("literature"),
        "assimilation_receipt_id": "assimilation.target-a.3",
        "created_utc": "2026-07-21T12:00:00Z",
        "gate_results": [{"gate_id": "G0", "required": True, "status": "pass", "controlling_receipt_ids": ["validator.g0"]}],
        "validator_receipts": [{"receipt_id": "validator.g0", "target_id": "target-a", "run_id": "run-a", "state_version": 3, "status": "completed", "valid": True, "completed_utc": "2026-07-21T11:59:00Z", "output_digest": digest("validator")}],
        "trace_digest": digest("trace"),
        "canonical_theory_evidence": canonical_evidence(),
        "authorization_scope": "target_navigation_continuation",
        "authority_exclusions": [
            "experiment_theory_selection",
            "literature_novelty_promotion",
            "theorem_or_truth_promotion",
        ],
        "decision": "promote",
        "decision_reasons": ["All required gates and exact identities passed."]
    })


def test_release_is_signed_and_navigation_only() -> None:
    payload = valid_release()
    assert validate_release_receipt(payload)["promotable"] is True

    unsigned = valid_release()
    unsigned.pop("receipt_digest")
    with pytest.raises(ReleaseValidationError, match="receipt_digest"):
        validate_release_receipt(unsigned)

    wrong_scope = valid_release()
    wrong_scope["authorization_scope"] = "no_continuation_authorized"
    sign(wrong_scope)
    with pytest.raises(ReleaseValidationError, match="target_navigation_continuation"):
        validate_release_receipt(wrong_scope)

    missing_exclusion = valid_release()
    missing_exclusion["authority_exclusions"].pop()
    sign(missing_exclusion)
    with pytest.raises(ReleaseValidationError, match="too short"):
        validate_release_receipt(missing_exclusion)


def test_promotion_requires_exact_canonical_theory_evidence() -> None:
    payload = valid_release()
    payload.pop("canonical_theory_evidence")
    sign(payload)
    with pytest.raises(ReleaseValidationError, match="canonical_theory_evidence"):
        validate_release_receipt(payload)


def test_canonical_evidence_digest_and_state_are_binding() -> None:
    payload = valid_release()
    payload["canonical_theory_evidence"]["commit_id"] = "commit-tampered"
    sign(payload)
    with pytest.raises(ReleaseValidationError, match="evidence digest"):
        validate_release_receipt(payload)

    payload = valid_release()
    payload["canonical_theory_evidence"]["committed_state_version"] = 4
    payload["canonical_theory_evidence"]["evidence_digest"] = canonical_digest(
        {
            key: value
            for key, value in payload["canonical_theory_evidence"].items()
            if key != "evidence_digest"
        }
    )
    sign(payload)
    with pytest.raises(ReleaseValidationError, match="state mismatch"):
        validate_release_receipt(payload)


def test_failed_or_unknown_required_gate_blocks_promotion() -> None:
    for status in ("fail", "unknown"):
        payload = valid_release()
        payload["gate_results"][0]["status"] = status
        sign(payload)
        with pytest.raises(ReleaseValidationError, match="required gate"):
            validate_release_receipt(payload)


def test_failed_or_unknown_required_gate_is_valid_as_a_non_promoting_hold() -> None:
    for status in ("fail", "unknown"):
        payload = valid_release()
        payload["gate_results"][0]["status"] = status
        payload["decision"] = "hold"
        payload["authorization_scope"] = "no_continuation_authorized"
        payload["decision_reasons"] = ["Required evidence is not yet positive."]
        sign(payload)
        result = validate_release_receipt(payload)
        assert result["valid"] is True
        assert result["promotable"] is False
        assert result["promotion_blockers"] == [f"required gate G0 is {status}"]


def test_unsuccessful_validator_is_a_blocker_not_a_malformed_hold() -> None:
    payload = valid_release()
    payload["validator_receipts"][0]["status"] = "failed"
    payload["validator_receipts"][0]["valid"] = False
    payload["decision"] = "quarantine"
    payload["authorization_scope"] = "no_continuation_authorized"
    payload["decision_reasons"] = ["Independent validation failed."]
    sign(payload)
    result = validate_release_receipt(payload)
    assert result["promotable"] is False
    assert "validator validator.g0 is not successful" in result["promotion_blockers"]


def test_wrong_target_run_or_state_receipt_is_rejected() -> None:
    for field, value in (("target_id", "wrong"), ("run_id", "wrong"), ("state_version", 99)):
        payload = valid_release()
        payload["validator_receipts"][0][field] = value
        sign(payload)
        with pytest.raises(ReleaseValidationError, match="identity mismatch"):
            validate_release_receipt(payload)


def test_not_applicable_gate_requires_reasoned_waiver() -> None:
    payload = valid_release()
    payload["gate_results"].append({"gate_id": "optional", "required": False, "status": "not_applicable", "controlling_receipt_ids": []})
    sign(payload)
    with pytest.raises(ReleaseValidationError, match="waiver"):
        validate_release_receipt(payload)


def test_registry_keeps_current_theory_roles_and_history_only_experiments() -> None:
    registry = load_registry()
    operators = {row["operator_id"]: row for row in registry["operators"]}
    assert set(operators) == {
        "reflective-conceptual-discovery", "reflective-theory-synthesizer",
        "formal-claim-producer", "blind-conceptual-preference-adjudicator",
        "frontier-literature-assimilator", "high-risk-hypothesis-forger",
        "parallel-hypothesis-portfolio", "canonical-causal-artifact-producer",
        "dynamic-symbolic-simulation-experimenter",
    }
    bindings = _bindings(registry)
    assert {binding.operator_id for binding in bindings} == {
        key for key, row in operators.items() if row.get("production_status") != "history_only"
    }
    assert all(binding.version == operators[binding.operator_id]["version"] for binding in bindings)
    assert all(binding.command and binding.validators for binding in bindings)
    assert all(binding.validators[0].command for binding in bindings)
    assert all(row["entrypoint"] and row["validator"] for row in registry["operators"])
    assert registry["parent_operator"] == "reflective-conceptual-discovery"
    literature = next(item for item in registry["operators"] if item["operator_id"] == "frontier-literature-assimilator")
    assert literature["kind"] == "literature_assimilation"
    assert "search" not in literature["command"]
    experiment = next(item for item in registry["operators"] if item["operator_id"] == "dynamic-symbolic-simulation-experimenter")
    assert experiment["conditional"] is True
    for operator_id in ("canonical-causal-artifact-producer", "dynamic-symbolic-simulation-experimenter"):
        assert operators[operator_id]["production_status"] == "history_only"
        assert operators[operator_id]["canonical_reachability"] is False
    assert experiment["kind"] == "support_probe"
    assert experiment["required_consumers"] == ["reflective-conceptual-discovery"]
    assert registry["authority_policy"]["worker_shared_state_writes"] is False


def test_navigation_run_ids_are_unique_and_never_latest() -> None:
    first = new_run_id(entropy="a" * 12)
    second = new_run_id(entropy="b" * 12)
    assert first != second
    assert "latest" not in first and "current" not in first


def test_missing_literature_produces_valid_hold_not_promotion(tmp_path: Path) -> None:
    trace = tmp_path / "run.jsonl"
    trace.write_text('{"event":"started"}\n', encoding="utf-8")
    run_id = "navigation-test-run"
    validators = [{
        "receipt_id": f"validator.target-packet.{run_id}",
        "target_id": "target-a", "run_id": run_id, "state_version": 0,
        "status": "completed", "valid": True,
        "completed_utc": "2026-07-21T12:00:00Z", "output_digest": digest("ok"),
    }, {
        "receipt_id": f"validator.target-literature.{run_id}",
        "target_id": "target-a", "run_id": run_id, "state_version": 0,
        "status": "completed", "valid": False,
        "completed_utc": "2026-07-21T12:00:00Z", "output_digest": digest("missing"),
    }]
    receipt = build_release_receipt(
        target_id="target-a", run_id=run_id, state_version=0,
        validator_receipts=validators, trace_path=trace, literature_binding=None,
    )
    assert receipt["decision"] == "hold"
    assert validate_release_receipt(receipt)["promotable"] is False
    assert receipt["literature_snapshot_id"] == "missing-target-scoped-literature"
