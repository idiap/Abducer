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
    DESTRUCTIVE_COMMAND_MARKERS,
    emit,
    has_evidence_marker,
    protected_path,
    read_payload,
    safe_repo_artifact,
    trace,
    validate_activation_receipt,
    workflow_context,
)


def main() -> int:
    payload = read_payload()
    command = str(payload.get("command", ""))
    path = str(payload.get("target_path", payload.get("path", "")))
    if any(marker in command for marker in DESTRUCTIVE_COMMAND_MARKERS):
        result = {"decision": "block", "reason": "Destructive command requires explicit user request and release evidence."}
    elif payload.get("workflow_id") or payload.get("controlled") is True:
        workflow, _step, error = workflow_context(payload)
        if error:
            result = {"decision": "block", "reason": error}
        elif activation_error := validate_activation_receipt(payload, workflow):
            result = {"decision": "block", "reason": activation_error}
        else:
            tool = str(payload.get("tool", "")).strip()
            mutation_class = str(payload.get("mutation_class", "")).strip()
            budget = payload.get("budget")
            if not tool or not path or mutation_class not in {"read_only", "create", "modify", "delete"}:
                result = {
                    "decision": "block",
                    "reason": "Workflow-local tool use requires tool, target_path, and a registered mutation_class.",
                }
            elif not isinstance(budget, dict) or budget.get("approved") is not True:
                result = {"decision": "block", "reason": "Workflow-local tool use requires an approved structured budget."}
            elif safe_repo_artifact(path) is None:
                result = {"decision": "block", "reason": "Workflow-local target_path must be repository-relative."}
            elif mutation_class == "delete":
                result = {"decision": "block", "reason": "Named-workflow tool policy does not authorize deletion."}
            elif protected_path(path) and not has_evidence_marker(payload):
                result = {"decision": "warn", "reason": "Protected control-plane path change should cite TODO or decision evidence."}
            else:
                result = {
                    "decision": "accept",
                    "reason": "Workflow-local tool identity, path, mutation class, and budget are authorized.",
                    "workflow_id": workflow.get("id"),
                    "step_id": payload.get("step_id", payload.get("step")),
                }
    elif path and protected_path(path) and not has_evidence_marker(payload):
        result = {"decision": "warn", "reason": "Protected control-plane path change should cite TODO or decision evidence."}
    else:
        result = {"decision": "accept", "reason": "No deterministic pre-tool policy violation detected."}
    trace("pre_tool_use_policy", payload, result)
    emit(**result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
