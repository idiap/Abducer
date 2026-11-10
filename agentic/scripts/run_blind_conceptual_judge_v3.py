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
"""Run only the separated v3 blind judge in a sealed research-worker envelope.

The parent ``ResearchWorkerAdapter`` owns isolation, resource supervision,
environment replacement, executable sealing, and receipt publication.  This
entrypoint accepts exactly the judge role and blind-judgment operation.  It has
no author operation and forwards only the closed adjudication payload to the
separated judge module.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[2]
JUDGE_MODULE_PATH = ROOT / "agentic/discovery/blind_conceptual_judge_v3.py"
JUDGE_MODULE_SPEC = importlib.util.spec_from_file_location(
    "_sealed_blind_conceptual_judge_v3", JUDGE_MODULE_PATH
)
if JUDGE_MODULE_SPEC is None or JUDGE_MODULE_SPEC.loader is None:
    raise RuntimeError("sealed blind judge module cannot be loaded")
JUDGE_MODULE = importlib.util.module_from_spec(JUDGE_MODULE_SPEC)
JUDGE_MODULE_SPEC.loader.exec_module(JUDGE_MODULE)
canonical_digest = JUDGE_MODULE.canonical_digest
execute_blind_conceptual_judgment = (
    JUDGE_MODULE.execute_blind_conceptual_judgment
)


STUDY_ID = "blind-conceptual-judge-v3"
ROLE = "judge"
OPERATION = "blind_judgment"
_ENVELOPE_KEYS = {
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
_CONTEXT_KEYS = {"commission_digest"}
_MAX_STDIN_BYTES = 4 * 1024 * 1024


def _canonical_json(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("worker envelope is not canonical-JSON encodable") from exc


def _stable_identifier(prefix: str, *parts: Any) -> str:
    suffix = hashlib.sha256(_canonical_json(list(parts))).hexdigest()[:24]
    return f"{prefix}.{suffix}"


def _request() -> dict[str, Any]:
    raw_bytes = sys.stdin.buffer.read(_MAX_STDIN_BYTES + 1)
    if len(raw_bytes) > _MAX_STDIN_BYTES:
        raise ValueError("blind judge worker stdin exceeds its fixed envelope limit")
    try:
        raw = json.loads(raw_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("blind judge worker stdin is not one JSON object") from exc
    if not isinstance(raw, dict) or set(raw) != _ENVELOPE_KEYS:
        raise ValueError("blind judge research-worker envelope drift")
    if (
        raw["schema_version"] != 1
        or raw["study_id"] != STUDY_ID
        or raw["role"] != ROLE
        or raw["operation"] != OPERATION
    ):
        raise ValueError("blind judge worker rejects non-judge and author operations")
    context = raw["invocation_context"]
    payload = raw["payload"]
    if (
        not isinstance(context, Mapping)
        or set(context) != _CONTEXT_KEYS
        or not isinstance(payload, Mapping)
        or not isinstance(raw["isolation_requirement"], Mapping)
    ):
        raise ValueError("blind judge worker information domain is not closed")
    if (
        context["commission_digest"] != payload.get("commission_digest")
        or raw["payload_digest"] != canonical_digest(payload)
    ):
        raise ValueError("blind judge worker commission or payload digest mismatch")
    expected_nonce = _stable_identifier(
        "research-worker-request",
        raw["study_id"],
        raw["role"],
        raw["operation"],
        dict(context),
        dict(payload),
        dict(raw["isolation_requirement"]),
        raw["fault_mode"],
    )
    if raw["request_nonce"] != expected_nonce:
        raise ValueError("blind judge worker request nonce mismatch")
    if raw["fault_mode"] not in {None, "exit_nonzero", "invalid_json", "hang"}:
        raise ValueError("blind judge worker fault mode is unknown")
    return raw


def _environment_observation() -> dict[str, Any]:
    bindings = dict(sorted(os.environ.items()))
    return {
        "names": sorted(bindings),
        "values_digest": canonical_digest(bindings),
        "working_directory": str(Path.cwd().resolve()),
    }


def _fault(request: Mapping[str, Any]) -> int | None:
    mode = request["fault_mode"]
    if mode == "exit_nonzero":
        return 23
    if mode == "invalid_json":
        sys.stdout.write("not-a-blind-judge-response")
        return 0
    if mode == "hang":
        time.sleep(300.0)
        return 0
    return None


def main() -> int:
    request = _request()
    fault_result = _fault(request)
    if fault_result is not None:
        return fault_result
    output = execute_blind_conceptual_judgment(request["payload"])
    response = {
        "schema_version": 1,
        "role": ROLE,
        "operation": OPERATION,
        "request_nonce": request["request_nonce"],
        "environment_observation": _environment_observation(),
        "output": output,
    }
    sys.stdout.buffer.write(_canonical_json(response))
    sys.stdout.buffer.write(b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
