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
"""Generate or check a deterministic release receipt for one canonical cycle.

The receipt promotes only target-navigation continuation.  It embeds the exact
commit-backed six-operator evidence and explicitly denies theorem/truth
promotion.  Generation is deterministic from immutable inputs; ``--check`` is
the read-only CI mode and fails on any drift.
"""

from __future__ import annotations

import argparse
import json
import sys
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
    file_digest,
    load_json,
    stable_identifier,
)
from agentic_common import write_json  # noqa: E402
from run_skill_reachability_audit import build_reachability_report  # noqa: E402
from validate_canonical_discovery_acceptance import (  # noqa: E402
    validate_canonical_acceptance,
)
from validate_target_navigation_release import (  # noqa: E402
    canonical_theory_evidence_from_reachability,
    validate_release_receipt,
)


def build_release(
    *,
    cycle_path: Path,
    cycle_request_path: Path,
    state_root: Path,
    workspace: Path,
    receipt_root: Path,
    target_id: str,
    run_id: str,
) -> dict[str, Any]:
    """Build a deterministic navigation-release receipt from exact evidence."""

    acceptance = validate_canonical_acceptance(
        cycle_path=cycle_path,
        cycle_request_path=cycle_request_path,
        state_root=state_root,
        workspace=workspace,
        receipt_root=receipt_root,
        target_id=target_id,
        run_id=run_id,
    )
    reachability = build_reachability_report(
        receipt_root=receipt_root,
        artifact_root=workspace,
        canonical_cycle_path=cycle_path,
        canonical_state_root=state_root,
        target_id=target_id,
        run_id=run_id,
    )
    evidence = canonical_theory_evidence_from_reachability(reachability)
    cycle = load_json(cycle_path)
    if not isinstance(cycle, dict):
        raise ContractError("canonical cycle projection must be an object")
    literature_edges = [
        edge
        for edge in cycle.get("feedback_edges", [])
        if edge.get("producer_operator_id") == "frontier-literature-assimilator"
    ]
    if len(literature_edges) != 1:
        raise ContractError("canonical release requires one exact literature feedback edge")
    completed = max(event["occurred_at"] for event in cycle["events"])
    validator_specs = [
        ("canonical-acceptance", canonical_digest(acceptance)),
        ("operator-feedback", canonical_digest(reachability)),
        (
            "target-literature",
            canonical_digest(
                {
                    "snapshot_id": evidence["literature_snapshot_id"],
                    "snapshot_digest": evidence["literature_snapshot_digest"],
                    "assimilation_receipt_id": literature_edges[0]["producer_receipt_id"],
                }
            ),
        ),
    ]
    validators = [
        {
            "receipt_id": f"validator.{name}.{cycle['cycle_id']}",
            "target_id": target_id,
            "run_id": run_id,
            "state_version": cycle["committed_state_version"],
            "status": "completed",
            "valid": True,
            "completed_utc": completed,
            "output_digest": output_digest,
        }
        for name, output_digest in validator_specs
    ]
    gates = [
        {
            "gate_id": name,
            "required": True,
            "status": "pass",
            "controlling_receipt_ids": [validator["receipt_id"]],
        }
        for (name, _), validator in zip(validator_specs, validators, strict=True)
    ]
    release: dict[str, Any] = {
        "schema_version": "1.0.0",
        "release_id": stable_identifier(
            "release", target_id, run_id, cycle["commit_id"], "navigation-continuation"
        ),
        "target_id": target_id,
        "run_id": run_id,
        "state_version": cycle["committed_state_version"],
        "literature_snapshot_id": evidence["literature_snapshot_id"],
        "literature_snapshot_digest": evidence["literature_snapshot_digest"],
        "assimilation_receipt_id": literature_edges[0]["producer_receipt_id"],
        "created_utc": completed,
        "gate_results": gates,
        "validator_receipts": validators,
        "trace_digest": file_digest(cycle_path),
        "operator_trace_path": (
            cycle_path.resolve().relative_to(ROOT.resolve()).as_posix()
            if cycle_path.resolve().is_relative_to(ROOT.resolve())
            else str(cycle_path.resolve())
        ),
        "canonical_theory_evidence": evidence,
        "authorization_scope": "target_navigation_continuation",
        "authority_exclusions": [
            "experiment_theory_selection",
            "literature_novelty_promotion",
            "theorem_or_truth_promotion",
        ],
        "decision": "promote",
        "decision_reasons": [
            "Exact current canonical theory, literature, and six feedback-effective operator gates passed.",
            "Promotion authorizes target-navigation continuation only; it does not promote a theorem, truth claim, novelty claim, or experiment result.",
        ],
    }
    release["receipt_digest"] = canonical_digest(release)
    validate_release_receipt(release)
    return release


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycle", required=True, type=Path)
    parser.add_argument("--cycle-request", required=True, type=Path)
    parser.add_argument("--state-root", required=True, type=Path)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--receipt-root", required=True, type=Path)
    parser.add_argument("--target-id", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        release = build_release(
            cycle_path=args.cycle,
            cycle_request_path=args.cycle_request,
            state_root=args.state_root,
            workspace=args.workspace,
            receipt_root=args.receipt_root,
            target_id=args.target_id,
            run_id=args.run_id,
        )
        if args.check:
            existing = load_json(args.output)
            if existing != release:
                raise ContractError("canonical release artifact differs from exact current evidence")
        else:
            write_json(args.output, release)
    except (ContractError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "status": "passed",
                "mode": "checked" if args.check else "generated",
                "release_id": release["release_id"],
                "decision": release["decision"],
                "output": str(args.output),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
