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
"""Closed-envelope subprocess for one open-world maturation branch.

The parent runtime supplies exactly one branch intent/manifest and one theory
proposal.  This process validates their closed identity, returns the proposal
through the registered research-worker envelope, and exposes deliberately
bounded probes used by isolation regressions.  It makes no creativity, truth,
or physics-value claim: semantic authorship remains outside this operational
boundary.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any


_REQUEST_FIELDS = {
    "schema_version",
    "study_id",
    "role",
    "operation",
    "request_nonce",
    "invocation_context",
    "payload",
    "payload_digest",
    "isolation_requirement",
    "fault_mode",
}
_PAYLOAD_FIELDS = {
    "branch_request",
    "matured_response",
    "minimum_residency_seconds",
    "adversarial_probe",
}
_MATURED_FIELDS = {
    "invention_id",
    "branch_id",
    "exploration_role",
    "statement",
    "semantic_core",
    "deep_reflection",
    "risk_reward",
    "physics_handback",
}
_PROBE_FIELDS = {
    "sibling_read_path",
    "sibling_write_path",
    "late_write_path",
    "spawn_late_descendant",
}
_AUTHORITY_BOUNDARY = (
    "caller_supplied_theory_material_validated_in_one_local_branch; no creativity, "
    "truth, physics-value, hidden-input, cognitive-independence, or semantic-"
    "independence authority"
)


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value)).hexdigest()


def _validate_seal(value: Mapping[str, Any], field: str, context: str) -> None:
    if not isinstance(value.get(field), str):
        raise ValueError(f"{context} lacks {field}")
    core = {key: child for key, child in value.items() if key != field}
    if value[field] != _digest(core):
        raise ValueError(f"{context} {field} mismatch")


def _validate_isolation_requirement(raw: Any) -> None:
    required = {
        "schema_version",
        "kernel_isolation_required",
        "minimum_accepted_status",
        "selected_backend",
        "selected_backend_probe_status",
        "content_digest",
    }
    if not isinstance(raw, Mapping) or set(raw) != required:
        raise ValueError("worker isolation requirement must be a closed object")
    kernel_required = raw["kernel_isolation_required"]
    expected_minimum = (
        "kernel_policy_enforced" if kernel_required is True else "strongest_available"
    )
    core = {key: value for key, value in raw.items() if key != "content_digest"}
    if (
        raw["schema_version"] != 1
        or not isinstance(kernel_required, bool)
        or raw["minimum_accepted_status"] != expected_minimum
        or raw["selected_backend"]
        not in {"macos_sandbox_exec", "linux_bubblewrap", "process_group_only"}
        or raw["selected_backend_probe_status"]
        not in {"passed", "unavailable", "failed"}
        or raw["content_digest"] != _digest(core)
    ):
        raise ValueError("worker isolation requirement is invalid")


def _validate_branch_payload(payload: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if set(payload) != _PAYLOAD_FIELDS:
        raise ValueError("open-world maturation payload is not closed")
    branch_request = payload["branch_request"]
    matured = payload["matured_response"]
    if (
        not isinstance(branch_request, Mapping)
        or set(branch_request) != {"intent", "manifest"}
        or not isinstance(branch_request["intent"], Mapping)
        or not isinstance(branch_request["manifest"], Mapping)
    ):
        raise ValueError("branch request must contain one intent and manifest")
    intent = branch_request["intent"]
    manifest = branch_request["manifest"]
    _validate_seal(intent, "intent_digest", "branch intent")
    _validate_seal(manifest, "manifest_digest", "branch manifest")
    if (
        manifest.get("branch_id") != intent.get("branch_id")
        or manifest.get("intent_digest") != intent.get("intent_digest")
    ):
        raise ValueError("branch intent and manifest identities differ")
    if not isinstance(matured, Mapping) or set(matured) != _MATURED_FIELDS:
        raise ValueError("matured response is not the closed response object")
    if (
        matured.get("branch_id") != intent.get("branch_id")
        or matured.get("invention_id") != intent.get("invention_id")
        or matured.get("exploration_role") not in {"candidate", "wildcard"}
    ):
        raise ValueError("matured response belongs to another branch")
    residency = payload["minimum_residency_seconds"]
    if not isinstance(residency, (int, float)) or isinstance(residency, bool):
        raise ValueError("minimum residency must be numeric")
    if not 0.0 <= float(residency) <= 1.0:
        raise ValueError("minimum residency is outside the bounded worker range")
    return dict(branch_request), dict(matured)


def _attempt_probe(raw: Any) -> dict[str, Any]:
    observation: dict[str, Any] = {
        "sibling_read_attempted": False,
        "sibling_read_succeeded": None,
        "sibling_read_error": None,
        "sibling_write_attempted": False,
        "sibling_write_succeeded": None,
        "sibling_write_error": None,
        "late_descendant_spawned": False,
    }
    if raw is None:
        return observation
    if not isinstance(raw, Mapping) or set(raw) != _PROBE_FIELDS:
        raise ValueError("adversarial probe is not a closed object")

    read_path = raw["sibling_read_path"]
    if read_path is not None:
        if not isinstance(read_path, str) or not read_path:
            raise ValueError("sibling read path must be a non-empty string or null")
        observation["sibling_read_attempted"] = True
        try:
            Path(read_path).read_bytes()
        except OSError as exc:
            observation["sibling_read_succeeded"] = False
            observation["sibling_read_error"] = type(exc).__name__
        else:
            observation["sibling_read_succeeded"] = True

    write_path = raw["sibling_write_path"]
    if write_path is not None:
        if not isinstance(write_path, str) or not write_path:
            raise ValueError("sibling write path must be a non-empty string or null")
        observation["sibling_write_attempted"] = True
        try:
            Path(write_path).write_text("open-world-sibling-write", encoding="utf-8")
        except OSError as exc:
            observation["sibling_write_succeeded"] = False
            observation["sibling_write_error"] = type(exc).__name__
        else:
            observation["sibling_write_succeeded"] = True

    late_path = raw["late_write_path"]
    spawn_late = raw["spawn_late_descendant"]
    if not isinstance(spawn_late, bool):
        raise ValueError("spawn_late_descendant must be boolean")
    if spawn_late:
        if not isinstance(late_path, str) or not late_path:
            raise ValueError("late descendant requires one write path")
        code = (
            "import pathlib,time; time.sleep(0.35); "
            f"pathlib.Path({late_path!r}).write_text('late-write', encoding='utf-8')"
        )
        subprocess.Popen(
            [sys.executable, "-I", "-B", "-c", code],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )
        observation["late_descendant_spawned"] = True
    elif late_path is not None:
        raise ValueError("late write path is forbidden without a descendant probe")
    return observation


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, Mapping) or set(request) != _REQUEST_FIELDS:
            raise ValueError("worker request must have the exact closed envelope")
        if (
            request["schema_version"] != 1
            or request["role"] != "high_risk"
            or request["operation"] != "parallel_maturation"
            or not isinstance(request["invocation_context"], Mapping)
            or not isinstance(request["payload"], Mapping)
            or request["payload_digest"] != _digest(request["payload"])
        ):
            raise ValueError("worker request identity or payload digest mismatch")
        _validate_isolation_requirement(request["isolation_requirement"])
        fault_mode = request["fault_mode"]
        if fault_mode not in {None, "exit_nonzero", "invalid_json", "hang"}:
            raise ValueError("unknown fault mode")
        if fault_mode == "exit_nonzero":
            return 17
        if fault_mode == "invalid_json":
            sys.stdout.write("{")
            return 0
        if fault_mode == "hang":
            time.sleep(60.0)

        branch_request, matured = _validate_branch_payload(request["payload"])
        observation = _attempt_probe(request["payload"]["adversarial_probe"])
        time.sleep(float(request["payload"]["minimum_residency_seconds"]))
        output = {
            "output_kind": "parallel_maturation",
            "branch_request_digest": _digest(branch_request),
            "matured_response": matured,
            "matured_response_digest": _digest(matured),
            "access_observation": observation,
            "authority_boundary": _AUTHORITY_BOUNDARY,
        }
        environment = {name: os.environ[name] for name in sorted(os.environ)}
        response = {
            "schema_version": 1,
            "role": "high_risk",
            "operation": "parallel_maturation",
            "request_nonce": str(request["request_nonce"]),
            "environment_observation": {
                "names": sorted(environment),
                "values_digest": _digest(environment),
                "working_directory": str(Path.cwd().resolve()),
            },
            "output": output,
        }
        sys.stdout.buffer.write(_canonical_json(response) + b"\n")
        return 0
    except Exception as exc:
        error = {
            "status": "worker_protocol_error",
            "error_type": type(exc).__name__,
            "message": str(exc),
        }
        sys.stderr.buffer.write(_canonical_json(error) + b"\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
