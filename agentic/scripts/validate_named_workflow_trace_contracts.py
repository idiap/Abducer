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
"""Validate named-workflow trace requirements against the execution registry."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXECUTION = ROOT / "agentic/registries/named_workflow_contracts.yaml"
TRACE = ROOT / "agentic/registries/named_workflow_trace_contracts.yaml"


def validate(execution: dict, trace: dict) -> list[str]:
    errors: list[str] = []
    traced = {row.get("id"): row for row in trace.get("workflows", [])}
    for workflow in execution.get("workflows", []):
        workflow_id = workflow["id"]
        contract = traced.get(workflow_id)
        if not contract:
            errors.append(f"missing workflow trace contract: {workflow_id}")
            continue
        if contract.get("version") != workflow.get("version"):
            errors.append(f"version mismatch: {workflow_id}")
        expected_steps = {row["id"]: row for row in workflow.get("steps", [])}
        actual_steps = {row.get("step_id"): row for row in contract.get("steps", [])}
        if set(expected_steps) != set(actual_steps):
            errors.append(f"step coverage mismatch: {workflow_id}")
        for step_id, step in expected_steps.items():
            row = actual_steps.get(step_id, {})
            if row.get("skill") != step.get("skill") or row.get("mode") != step.get("mode"):
                errors.append(f"step projection mismatch: {workflow_id}/{step_id}")
            for field in ("required_fields", "evidence_roles"):
                if not row.get(field):
                    errors.append(f"empty {field}: {workflow_id}/{step_id}")
        actual_profiles = {row.get("id"): row for row in contract.get("profiles", [])}
        for profile in workflow.get("profiles", []):
            profile_id = profile["id"]
            projected = actual_profiles.get(profile_id)
            if not projected:
                errors.append(f"missing profile trace contract: {workflow_id}/{profile_id}")
                continue
            if {x["id"] for x in profile.get("steps", [])} != {x.get("step_id") for x in projected.get("steps", [])}:
                errors.append(f"profile step coverage mismatch: {workflow_id}/{profile_id}")
            if set(profile.get("specialist_skills", [])) != {x.get("skill") for x in projected.get("specialists", [])}:
                errors.append(f"specialist coverage mismatch: {workflow_id}/{profile_id}")
    extras = set(traced) - {row["id"] for row in execution.get("workflows", [])}
    if extras:
        errors.append(f"unknown workflow trace contracts: {sorted(extras)}")
    return errors


def main() -> int:
    execution = json.loads(EXECUTION.read_text(encoding="utf-8"))
    trace = json.loads(TRACE.read_text(encoding="utf-8"))
    errors = validate(execution, trace)
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1
    total_steps = sum(len(row["steps"]) for row in trace["workflows"])
    total_roles = total_steps + sum(len(profile["steps"]) + len(profile["specialists"]) for row in trace["workflows"] for profile in row["profiles"])
    print(f"validated {len(trace['workflows'])} workflows, {total_steps} base steps, {total_roles} total step/profile roles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
