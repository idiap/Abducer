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
"""Execute one closed-kernel formal route inside an isolated worker process.

The parent research-worker adapter owns process supervision, budgets, command
authority, environment scrubbing, and immutable receipts.  This script has one
small responsibility: validate the adapter envelope, pause briefly so the four
independently spawned processes overlap as a real wave, and invoke the shared
central formal-route implementation.  It contains no Category/HoTT logic of its
own.

Fault modes are deliberately handled here so tests exercise the same process
boundary as production: a nonzero exit, malformed response, or nonterminating
worker must become a terminal operational receipt without erasing siblings.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[2]
# ResearchWorkerAdapter resolves the virtual-environment interpreter symlink to
# its base executable before applying ``-I``.  Re-add only this repository's
# lock-backed site-packages directory so the shared validators (notably
# jsonschema) remain importable without inheriting user or environment paths.
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

from agentic.discovery.central_formal_routes import (  # noqa: E402
    execute_central_formal_route_payload,
)
from agentic.discovery.contracts import canonical_digest, canonical_json  # noqa: E402


def _request() -> dict[str, Any]:
    try:
        raw = json.loads(sys.stdin.buffer.read())
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("central formal worker stdin is not one JSON object") from exc
    if not isinstance(raw, dict):
        raise ValueError("central formal worker stdin root must be an object")
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
        raise ValueError("central formal worker request envelope drift")
    if (
        raw["schema_version"] != 1
        or raw["role"] != "formal_lens"
        or raw["operation"] != "formal_lens"
        or not isinstance(raw["payload"], Mapping)
        or raw["payload_digest"] != canonical_digest(raw["payload"])
    ):
        raise ValueError("central formal worker request identity or payload digest mismatch")
    return raw


def _environment_observation() -> dict[str, Any]:
    bindings = dict(sorted(os.environ.items()))
    return {
        "names": sorted(bindings),
        "values_digest": canonical_digest(bindings),
        "working_directory": str(Path.cwd().resolve()),
    }


def main() -> int:
    request = _request()
    fault_mode = request["fault_mode"]
    if fault_mode == "exit_nonzero":
        return 19
    if fault_mode == "invalid_json":
        sys.stdout.write("not-a-central-formal-response")
        return 0
    if fault_mode == "hang":
        time.sleep(300.0)
        return 0
    if fault_mode is not None:
        raise ValueError("unknown central formal worker fault mode")

    payload = request["payload"]
    hold = payload["orchestration_request"]["composition_policy"][
        "process_overlap_hold_seconds"
    ]
    if isinstance(hold, bool) or not isinstance(hold, (int, float)) or not 0.0 <= hold <= 1.0:
        raise ValueError("process overlap hold must be a bounded number")
    time.sleep(float(hold))
    output = execute_central_formal_route_payload(payload)
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
