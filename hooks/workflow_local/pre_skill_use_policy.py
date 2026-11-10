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

from .hook_utils import emit, read_payload, trace, validate_activation_receipt, workflow_context


def main() -> int:
    payload = read_payload()
    skill = str(payload.get("skill", "")).strip()
    controlled = bool(payload.get("controlled", True))
    if not controlled:
        result = {"decision": "accept", "reason": "Invocation is explicitly uncontrolled; workflow authorization was not claimed."}
    elif not skill:
        result = {"decision": "block", "reason": "Controlled invocation requires `skill`."}
    else:
        workflow, step, error = workflow_context(payload)
        if error:
            result = {"decision": "block", "reason": error}
        elif activation_error := validate_activation_receipt(payload, workflow):
            result = {"decision": "block", "reason": activation_error}
        elif str(step.get("skill", "")) != skill:
            result = {
                "decision": "block",
                "reason": f"Skill `{skill}` is not the declared member of step `{step.get('id', step.get('order'))}`.",
            }
        elif str(step.get("mode", "required")) == "conditional" and (
            not isinstance(payload.get("conditional_evidence"), dict)
            or not payload["conditional_evidence"]
            or payload["conditional_evidence"].get("activated") is False
        ):
            result = {
                "decision": "block",
                "reason": "Conditional skill requires activated, structured `conditional_evidence`.",
            }
        else:
            prerequisites = {str(item) for item in step.get("prerequisites", [])}
            completed = {str(item) for item in payload.get("completed_steps", [])}
            skipped_rows = payload.get("skipped_steps", [])
            if not isinstance(skipped_rows, list):
                skipped_rows = []
            skipped = {
                str(item.get("step_id"))
                for item in skipped_rows
                if isinstance(item, dict) and item.get("step_id") and item.get("reason")
            }
            order = step.get("order")
            if isinstance(order, int):
                for prior in workflow.get("steps", []):
                    if not isinstance(prior, dict) or not isinstance(prior.get("order"), int):
                        continue
                    if prior["order"] >= order:
                        continue
                    prior_id = str(prior.get("id", prior["order"]))
                    prior_mode = str(prior.get("mode", "required"))
                    if prior_mode in {"required", "validator_only"}:
                        prerequisites.add(prior_id)
                    elif prior_mode in {"conditional", "advisory"} and prior_id not in skipped:
                        prerequisites.add(prior_id)
            missing = sorted(prerequisites - completed)
            if missing:
                result = {
                    "decision": "block",
                    "reason": "Earlier required workflow steps are incomplete; conditional steps require completion or a reasoned skip.",
                    "missing": missing,
                }
            else:
                result = {
                    "decision": "accept",
                    "reason": "Skill is authorized for the active workflow, target, and step.",
                    "workflow_id": workflow.get("id"),
                    "step_id": step.get("id", step.get("order")),
                }
    trace("pre_skill_use_policy", payload, result)
    emit(**result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
