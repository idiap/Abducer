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
from __future__ import annotations

from .hook_utils import (
    emit,
    read_payload,
    safe_repo_artifact,
    trace,
    valid_skill_receipt,
    validate_activation_receipt,
    workflow_context,
)


def main() -> int:
    payload = read_payload()
    if not payload.get("controlled", True):
        result = {"decision": "accept", "reason": "Explicitly uncontrolled stop has no workflow exit claim."}
    else:
        workflow, _step, error = workflow_context(payload, require_step=False)
        if error:
            result = {"decision": "block", "reason": error}
        elif activation_error := validate_activation_receipt(payload, workflow):
            result = {"decision": "block", "reason": activation_error}
        else:
            gate = workflow.get("exit_gate", {})
            required = (
                gate.get("required_artifacts", workflow.get("required_artifacts", []))
                if isinstance(gate, dict)
                else []
            )
            # Legacy contracts list concrete repository paths.  Versioned named
            # contracts list artifact type IDs, proven by workflow receipts.
            legacy_paths = [item for item in required if "/" in str(item)]
            required_types = {str(item) for item in required if "/" not in str(item)}
            completed = payload.get("completed_artifacts", payload.get("artifact_receipts", []))
            if isinstance(completed, (str, dict)):
                completed = [completed]
            target = str(payload.get("target", payload.get("target_id", ""))).strip()
            named_contract = bool(workflow.get("input_artifact"))
            invalid_receipts = []
            completed_types: set[str] = set()
            for item in completed:
                if named_contract:
                    if not valid_skill_receipt(item, workflow=workflow, target=target):
                        invalid_receipts.append(item)
                        continue
                    completed_types.add(str(item.get("artifact_type", "")))
                elif isinstance(item, dict):
                    if item.get("status") in {"accepted", "validated"}:
                        completed_types.add(str(item.get("type", item.get("artifact_type", ""))))
                else:
                    completed_types.add(str(item))
            invalid = [str(path) for path in legacy_paths if safe_repo_artifact(path) is None]
            missing = [
                str(path)
                for path in legacy_paths
                if safe_repo_artifact(path) is not None and not safe_repo_artifact(path).exists()
            ]
            missing_types = sorted(required_types - completed_types)
            obligations = payload.get("open_obligations", [])
            gate_status = str(payload.get("gate_status", "")).strip()
            allowed = {str(item) for item in gate.get("allowed", [])} if isinstance(gate, dict) else set()
            obligation_policy = str(gate.get("open_obligations_policy", "forbid")) if isinstance(gate, dict) else "forbid"
            if invalid_receipts:
                result = {
                    "decision": "block",
                    "reason": "Named-workflow exit requires digest-bound receipts for this workflow version and target.",
                }
            elif invalid:
                result = {"decision": "block", "reason": "Workflow exit artifacts must be repository-relative.", "invalid": invalid}
            elif missing:
                result = {"decision": "block", "reason": "Active workflow exit artifacts are missing.", "missing": missing}
            elif missing_types:
                result = {
                    "decision": "block",
                    "reason": "Active workflow receipt types are missing.",
                    "missing_artifact_types": missing_types,
                }
            elif obligations and obligation_policy == "forbid":
                result = {
                    "decision": "block",
                    "reason": "Active workflow has open obligations.",
                    "open_obligations": obligations,
                }
            elif obligations and obligation_policy == "archive_only" and any(
                not isinstance(item, dict) or item.get("status") != "archived" for item in obligations
            ):
                result = {"decision": "block", "reason": "Open obligations must be archived before this workflow may stop."}
            elif obligations and obligation_policy == "allow_declared" and any(
                not isinstance(item, dict) or not item.get("declared") for item in obligations
            ):
                result = {"decision": "block", "reason": "Every open obligation must be explicitly declared."}
            elif allowed and gate_status not in allowed:
                result = {
                    "decision": "block",
                    "reason": f"Gate status `{gate_status}` is not an allowed workflow exit status.",
                }
            else:
                result = {
                    "decision": "accept",
                    "reason": "Active workflow exit requirements are satisfied.",
                    "workflow_id": workflow.get("id"),
                }
    trace("stop_artifact_check", payload, result)
    emit(**result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
