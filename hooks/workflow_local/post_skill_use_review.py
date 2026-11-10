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

import json

from .hook_utils import (
    declared_types,
    emit,
    file_digest,
    make_skill_receipt,
    read_payload,
    safe_repo_artifact,
    trace,
    validate_activation_receipt,
    validate_artifact_envelope,
    workflow_context,
)


def main() -> int:
    payload = read_payload()
    if not payload.get("controlled", True):
        decision = "accept"
        result = {"decision": decision, "reason": "Explicitly uncontrolled completion; no workflow receipt is claimed."}
    else:
        output_type = ""
        epistemic_status = ""
        workflow, step, error = workflow_context(payload)
        skill = str(payload.get("skill", "")).strip()
        if error:
            decision = "block"
            result = {"decision": decision, "reason": error}
        elif activation_error := validate_activation_receipt(payload, workflow):
            decision = "block"
            result = {"decision": decision, "reason": activation_error}
        elif skill != str(step.get("skill", "")):
            decision = "block"
            result = {"decision": decision, "reason": "Post-skill receipt does not match the declared workflow step skill."}
        else:
            declared = declared_types(step, "produces")
            output_type = str(payload.get("output_type", payload.get("artifact_type", ""))).strip()
            expected = payload.get("expected_artifacts", [])
            if isinstance(expected, str):
                expected = [expected]
            invalid = [str(path) for path in expected if safe_repo_artifact(path) is None]
            missing = [
                str(path)
                for path in expected
                if safe_repo_artifact(path) is not None and not safe_repo_artifact(path).exists()
            ]
            epistemic_status = str(payload.get("epistemic_status", "")).strip()
            allowed_statuses = {"candidate", "validated", "quarantined", "rejected", "archived"}
            if not output_type:
                decision = "block"
                result = {"decision": decision, "reason": "Controlled completion requires `output_type`."}
            elif declared and output_type not in declared:
                decision = "block"
                result = {"decision": decision, "reason": f"Output type `{output_type}` is not declared by the workflow step."}
            elif epistemic_status not in allowed_statuses:
                decision = "block"
                result = {
                    "decision": decision,
                    "reason": "Controlled completion requires a registered `epistemic_status`.",
                    "allowed": sorted(allowed_statuses),
                }
            elif not expected:
                decision = "block"
                result = {
                    "decision": decision,
                    "reason": "Controlled completion requires at least one expected artifact reference.",
                }
            elif invalid:
                decision = "block"
                result = {"decision": decision, "reason": "Expected artifact paths must be repository-relative.", "invalid": invalid}
            elif missing:
                decision = "block"
                result = {"decision": decision, "reason": "Declared expected artifacts are missing.", "missing": missing}
            else:
                envelope_error = None
                if workflow.get("input_artifact"):
                    for raw in expected:
                        path = safe_repo_artifact(raw)
                        try:
                            envelope = json.loads(path.read_text(encoding="utf-8")) if path else None
                        except (OSError, json.JSONDecodeError):
                            envelope = None
                        envelope_error = validate_artifact_envelope(
                            envelope,
                            workflow=workflow,
                            target=str(payload.get("target", payload.get("target_id", ""))).strip(),
                            output_type=output_type,
                            epistemic_status=epistemic_status,
                        )
                        if envelope_error:
                            break
                if envelope_error:
                    decision = "block"
                    result = {"decision": decision, "reason": envelope_error}
                else:
                    decision = "accept"
                    result = {
                        "decision": decision,
                        "reason": "Declared output contract is satisfied; workflow receipt emitted.",
                        "workflow_id": workflow.get("id"),
                        "step_id": step.get("id", step.get("order")),
                        "output_type": output_type,
                        "epistemic_status": epistemic_status,
                    }
        raw_artifacts = payload.get("expected_artifacts", [])
        if isinstance(raw_artifacts, str):
            raw_artifacts = [raw_artifacts]
        if not isinstance(raw_artifacts, list):
            raw_artifacts = []
        artifact_paths = [str(path) for path in raw_artifacts]
        artifact_digests = {
            raw: file_digest(path)
            for raw in artifact_paths
            if (path := safe_repo_artifact(raw)) is not None and path.exists()
        }
        result["receipt"] = make_skill_receipt({
            "status": "accepted" if decision == "accept" else "rejected",
            "controlled": True,
            "workflow_id": workflow.get("id") if workflow else None,
            "workflow_version": workflow.get("version") if workflow else None,
            "target": str(payload.get("target", payload.get("target_id", ""))).strip(),
            "step_id": step.get("id", step.get("order")) if step else None,
            "skill": skill,
            "artifact_type": output_type or None,
            "epistemic_status": epistemic_status or None,
            "artifact_paths": artifact_paths,
            "artifact_digests": artifact_digests,
        })
    trace("post_skill_use_review", payload, result)
    emit(**result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
