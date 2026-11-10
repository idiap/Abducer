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
"""Execute exactly one v3 conceptual author operation.

The parent ``ResearchWorkerAdapter`` owns process supervision, resource limits,
environment scrubbing, command authority, and immutable receipts.  This worker
only validates that envelope, holds author processes briefly so the five-way
wave has an observable overlap opportunity, and dispatches the already sealed
postcommit payload.  The blind judge has a different executable and dependency
domain.  This worker never reads a theory store, accepts a route plan, or
dispatches adjudication.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[2]
LOCKED_SITE_PACKAGES = (
    ROOT
    / ".venv"
    / "lib"
    / f"python{sys.version_info.major}.{sys.version_info.minor}"
    / "site-packages"
)
if LOCKED_SITE_PACKAGES.is_dir() and str(LOCKED_SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(LOCKED_SITE_PACKAGES))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.central_conceptual_routes_v3 import (  # noqa: E402
    execute_route_author_payload,
)
from agentic.discovery.contracts import canonical_digest, canonical_json  # noqa: E402


_ROLE_OPERATION = {("formal_lens", "formal_lens")}


def _request() -> dict[str, Any]:
    try:
        raw = json.loads(sys.stdin.buffer.read())
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("central conceptual worker stdin is not one JSON object") from exc
    if not isinstance(raw, dict):
        raise ValueError("central conceptual worker stdin root must be an object")
    expected = {
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
    if set(raw) != expected:
        raise ValueError("central conceptual worker request envelope drift")
    if (
        raw["schema_version"] != 1
        or (raw["role"], raw["operation"]) not in _ROLE_OPERATION
        or not isinstance(raw["invocation_context"], Mapping)
        or not isinstance(raw["payload"], Mapping)
        or raw["payload_digest"] != canonical_digest(raw["payload"])
    ):
        raise ValueError("central conceptual worker request identity or payload digest mismatch")
    context = raw["invocation_context"]
    if (
        not isinstance(context.get("commission_id"), str)
        or not isinstance(context.get("commission_digest"), str)
    ):
        raise ValueError("central conceptual worker lacks a commission identity")
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
        sys.stdout.write("not-a-central-conceptual-response")
        return 0
    if mode == "hang":
        time.sleep(300.0)
        return 0
    if mode is not None:
        raise ValueError("unknown central conceptual worker fault mode")
    return None


def main() -> int:
    request = _request()
    fault_result = _fault(request)
    if fault_result is not None:
        return fault_result
    # The hold has no epistemic meaning.  It only makes process overlap a
    # falsifiable operational condition instead of an unobserved intention.
    time.sleep(0.30)
    output = execute_route_author_payload(request["payload"])
    response = {
        "schema_version": 1,
        "role": request["role"],
        "operation": request["operation"],
        "request_nonce": request["request_nonce"],
        "environment_observation": _environment_observation(),
        "output": output,
    }
    sys.stdout.buffer.write(canonical_json(response))
    sys.stdout.buffer.write(b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
