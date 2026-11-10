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
"""Validate evidence-sensitive, target-bound discovery release receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from agentic_common import ROOT, load_json_object


SCHEMA_PATH = ROOT / "agentic/spec/discovery_release_receipt.schema.json"
EXPECTED_DISCOVERY_OPERATORS = {
    "dynamic-symbolic-simulation-experimenter",
    "frontier-literature-assimilator",
    "high-risk-hypothesis-forger",
    "parallel-hypothesis-portfolio",
    "reflective-conceptual-discovery",
    "reflective-theory-synthesizer",
}
REQUIRED_AUTHORITY_EXCLUSIONS = {
    "theorem_or_truth_promotion",
    "literature_novelty_promotion",
    "experiment_theory_selection",
}


class ReleaseValidationError(ValueError):
    """Raised when promotion is unsupported by exact receipt evidence."""


def _canonical_digest(payload: Any) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _schema_validate(payload: dict[str, Any]) -> None:
    try:
        import jsonschema
    except ImportError as exc:  # pragma: no cover - bootstrap diagnostic
        raise ReleaseValidationError("jsonschema is required; run `uv sync --group dev`") from exc
    schema = load_json_object(SCHEMA_PATH)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(validator.iter_errors(payload), key=lambda item: list(item.path))
    if errors:
        raise ReleaseValidationError("; ".join(error.message for error in errors[:8]))


def canonical_theory_evidence_from_reachability(report: dict[str, Any]) -> dict[str, Any]:
    """Project an exact commit-backed reachability report into release evidence."""

    authorization = report.get("canonical_authorization")
    if not isinstance(authorization, dict):
        raise ReleaseValidationError("reachability report has no canonical authorization")
    operator_rows = sorted(
        (row for row in report.get("skills", []) if row.get("operator")),
        key=lambda row: row["skill_id"],
    )
    if (
        report.get("all_operators_feedback_effective") is not True
        or report.get("evidence_errors")
        or {row.get("skill_id") for row in operator_rows} != EXPECTED_DISCOVERY_OPERATORS
        or any(row.get("attained_level") != "feedback_effective" for row in operator_rows)
    ):
        raise ReleaseValidationError("reachability report does not prove all six canonical operators")
    evidence: dict[str, Any] = {
        "status": authorization["status"],
        "authoritative": authorization["authoritative"],
        "target_id": authorization["target_id"],
        "canonical_run_id": authorization["run_id"],
        "cycle_id": authorization["cycle_id"],
        "prior_state_version": authorization["prior_state_version"],
        "committed_state_version": authorization["committed_state_version"],
        "commit_id": authorization["commit_id"],
        "manifest_digest": authorization["manifest_digest"],
        "projection_digest": authorization["projection_digest"],
        "operator_evidence_digest": authorization["operator_evidence_digest"],
        "literature_snapshot_id": authorization["literature_snapshot_id"],
        "literature_snapshot_digest": authorization["literature_snapshot_digest"],
        "operator_count": len(operator_rows),
        "all_operators_feedback_effective": True,
        "operator_bindings": [
            {
                "operator_id": row["skill_id"],
                "receipt_ids": sorted(row["receipt_ids"]),
                "feedback_event_ids": sorted(row["feedback_event_ids"]),
            }
            for row in operator_rows
        ],
        "schedule_id": authorization["schedule_id"],
        "branch_authorizations": [
            {
                "branch_id": branch_id,
                "action_ids": sorted(authorization["action_ids_by_branch"][branch_id]),
                "action_kinds": sorted(authorization["action_kinds_by_branch"][branch_id]),
            }
            for branch_id in sorted(authorization["eligible_branch_ids"])
        ],
        "authorization_semantics": authorization["authorization_semantics"],
    }
    evidence["evidence_digest"] = _canonical_digest(evidence)
    return evidence


def _validate_canonical_theory_evidence(
    payload: dict[str, Any], integrity_errors: list[str], promotion_blockers: list[str]
) -> None:
    """Cross-check embedded canonical authority with the release identity."""

    evidence = payload.get("canonical_theory_evidence")
    if not isinstance(evidence, dict):
        promotion_blockers.append("canonical theory evidence is absent")
        return
    unsigned = dict(evidence)
    claimed_digest = unsigned.pop("evidence_digest", None)
    if claimed_digest != _canonical_digest(unsigned):
        integrity_errors.append("canonical theory evidence digest mismatch")
    if evidence.get("target_id") != payload["target_id"]:
        integrity_errors.append("canonical theory evidence target mismatch")
    if evidence.get("committed_state_version") != payload["state_version"]:
        integrity_errors.append("canonical theory evidence state mismatch")
    if (
        evidence.get("literature_snapshot_id") != payload["literature_snapshot_id"]
        or evidence.get("literature_snapshot_digest")
        != payload["literature_snapshot_digest"]
    ):
        integrity_errors.append("canonical theory evidence literature mismatch")
    bindings = evidence.get("operator_bindings", [])
    operator_ids = {
        row.get("operator_id") for row in bindings if isinstance(row, dict)
    }
    if (
        evidence.get("status") != "verified_active_current"
        or evidence.get("authoritative") is not True
        or evidence.get("all_operators_feedback_effective") is not True
        or evidence.get("operator_count") != 6
        or operator_ids != EXPECTED_DISCOVERY_OPERATORS
    ):
        promotion_blockers.append("canonical six-operator theory evidence is incomplete")


def validate_release_receipt(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate schema, identity, hard gates, validators, and promotion logic."""

    _schema_validate(payload)
    target_id = payload["target_id"]
    run_id = payload["run_id"]
    state_version = payload["state_version"]
    integrity_errors: list[str] = []
    promotion_blockers: list[str] = []
    expected_scope = (
        "target_navigation_continuation"
        if payload["decision"] == "promote"
        else "no_continuation_authorized"
    )
    if payload.get("authorization_scope") != expected_scope:
        integrity_errors.append("release authorization scope contradicts decision")
    if not REQUIRED_AUTHORITY_EXCLUSIONS.issubset(
        set(payload.get("authority_exclusions", []))
    ):
        integrity_errors.append("release omits mandatory authority exclusions")
    _validate_canonical_theory_evidence(payload, integrity_errors, promotion_blockers)
    receipt_ids = {item["receipt_id"] for item in payload["validator_receipts"]}
    for receipt in payload["validator_receipts"]:
        if (receipt["target_id"], receipt["run_id"], receipt["state_version"]) != (target_id, run_id, state_version):
            integrity_errors.append(f"validator {receipt['receipt_id']} identity mismatch")
        if receipt["status"] != "completed" or not receipt.get("valid", False):
            promotion_blockers.append(f"validator {receipt['receipt_id']} is not successful")
    for gate in payload["gate_results"]:
        missing = set(gate["controlling_receipt_ids"]) - receipt_ids
        if missing:
            integrity_errors.append(f"gate {gate['gate_id']} has unknown controlling receipts {sorted(missing)}")
        if gate["required"] and gate["status"] != "pass":
            promotion_blockers.append(f"required gate {gate['gate_id']} is {gate['status']}")
        if gate["status"] == "not_applicable" and not str(gate.get("waiver_reason") or "").strip():
            integrity_errors.append(f"gate {gate['gate_id']} lacks a not-applicable waiver")
    promotable = not integrity_errors and not promotion_blockers
    if payload["decision"] == "promote" and not promotable:
        integrity_errors.extend(promotion_blockers)
        integrity_errors.append("promotion decision contradicts blocking evidence")
    if payload["decision"] != "promote" and promotable:
        # A conservative hold remains allowed when an explicit rationale is given.
        if not payload.get("decision_reasons"):
            integrity_errors.append("non-promotion with all gates passing requires an explicit rationale")
    if payload.get("receipt_digest"):
        unsigned = dict(payload)
        unsigned.pop("receipt_digest", None)
        if payload["receipt_digest"] != _canonical_digest(unsigned):
            integrity_errors.append("release receipt digest mismatch")
    if integrity_errors:
        raise ReleaseValidationError("; ".join(integrity_errors))
    return {
        "valid": True,
        "promotable": promotable,
        "promotion_blockers": promotion_blockers,
        "release_id": payload["release_id"],
    }


def _default_receipts() -> list[Path]:
    return sorted((ROOT / "agentic/reports/releases/targets").glob("*/runs/*/release.json"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", action="append", default=[], help="Release receipt JSON; may be repeated.")
    parser.add_argument("--canonical-cycle", type=Path)
    parser.add_argument("--canonical-state-root", type=Path)
    parser.add_argument("--canonical-receipt-root", type=Path)
    parser.add_argument("--canonical-workspace", type=Path)
    args = parser.parse_args()
    canonical_paths = (
        args.canonical_cycle,
        args.canonical_state_root,
        args.canonical_receipt_root,
        args.canonical_workspace,
    )
    if any(canonical_paths) and not all(canonical_paths):
        print("ERROR: all four canonical evidence paths must be supplied together", file=sys.stderr)
        return 2
    paths = [ROOT / raw for raw in args.receipt] if args.receipt else _default_receipts()
    if not paths:
        # No release is not promotion.  Contract availability is a valid neutral state.
        sample_evidence = {
            "status": "verified_active_current", "authoritative": True,
            "target_id": "contract",
            "canonical_run_id": "canonical-contract", "cycle_id": "cycle.contract",
            "prior_state_version": 0, "committed_state_version": 1,
            "commit_id": "commit.contract", "manifest_digest": "sha256:" + "0" * 64,
            "projection_digest": "sha256:" + "1" * 64,
            "operator_evidence_digest": "sha256:" + "2" * 64,
            "literature_snapshot_id": "contract", "literature_snapshot_digest": "sha256:" + "0" * 64,
            "operator_count": 6, "all_operators_feedback_effective": True,
            "operator_bindings": [
                {"operator_id": operator_id, "receipt_ids": [f"receipt.{index}"], "feedback_event_ids": [f"event.{index}"]}
                for index, operator_id in enumerate(sorted(EXPECTED_DISCOVERY_OPERATORS), 1)
            ],
            "schedule_id": "schedule.contract",
            "branch_authorizations": [{
                "branch_id": "branch.contract",
                "action_ids": ["action.contract"],
                "action_kinds": ["reflect"],
            }],
            "authorization_semantics": "exact canonical schedule binding",
        }
        sample_evidence["evidence_digest"] = _canonical_digest(sample_evidence)
        sample = {
            "schema_version": "1.0.0", "release_id": "contract-self-check", "target_id": "contract",
            "run_id": "contract", "state_version": 1, "literature_snapshot_id": "contract",
            "literature_snapshot_digest": "sha256:" + "0" * 64, "assimilation_receipt_id": "contract",
            "created_utc": "2026-07-21T00:00:00Z", "gate_results": [{"gate_id": "shape", "required": True, "status": "pass", "controlling_receipt_ids": ["validator.contract"]}],
            "validator_receipts": [{"receipt_id": "validator.contract", "target_id": "contract", "run_id": "contract", "state_version": 1, "status": "completed", "valid": True, "completed_utc": "2026-07-21T00:00:00Z", "output_digest": "sha256:" + "0" * 64}],
            "trace_digest": "sha256:" + "0" * 64, "canonical_theory_evidence": sample_evidence,
            "authorization_scope": "target_navigation_continuation",
            "authority_exclusions": sorted(REQUIRED_AUTHORITY_EXCLUSIONS),
            "decision": "promote"
        }
        sample["receipt_digest"] = _canonical_digest(sample)
        _schema_validate(sample)
        print("validated release receipt contract; no authoritative release receipt is present, so nothing was promoted")
        return 0
    seen: set[tuple[str, str]] = set()
    try:
        for path in paths:
            payload = load_json_object(path)
            identity = (payload.get("target_id", ""), payload.get("run_id", ""))
            if identity in seen:
                raise ReleaseValidationError(f"duplicate target/run release identity: {identity}")
            seen.add(identity)
            validate_release_receipt(payload)
            if all(canonical_paths):
                # Recompute the embedded authority from exact immutable inputs;
                # an internally self-consistent release field is not enough.
                from run_skill_reachability_audit import build_reachability_report

                embedded = payload.get("canonical_theory_evidence") or {}
                report = build_reachability_report(
                    receipt_root=args.canonical_receipt_root,
                    artifact_root=args.canonical_workspace,
                    canonical_cycle_path=args.canonical_cycle,
                    canonical_state_root=args.canonical_state_root,
                    target_id=payload["target_id"],
                    run_id=embedded.get("canonical_run_id"),
                )
                expected = canonical_theory_evidence_from_reachability(report)
                if payload.get("canonical_theory_evidence") != expected:
                    raise ReleaseValidationError(
                        "release canonical theory evidence differs from exact current files"
                    )
    except (OSError, ReleaseValidationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"validated {len(paths)} target-bound discovery release receipt(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
