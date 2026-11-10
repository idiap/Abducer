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
"""History-only decoder and hard rejection for proof-worker-v1.

Historical request bytes remain inspectable data, never process-launch
authority. The sole current worker is run_discovery_proof_worker_v3.py and
is reachable only through the live in-process proof-v3 facade.
"""

from __future__ import annotations

import copy
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.discovery.contracts import (  # noqa: E402
    canonical_digest,
    validate_payload,
)


_HISTORY_ONLY_MESSAGE = (
    "proof worker v1 is history-only and cannot execute; "
    "proof-v3 is the sole live worker"
)


def decode_historical_proof_worker_request_v1(
    request: Mapping[str, Any],
    *,
    expected_artifact_digest: str,
) -> dict[str, Any]:
    """Validate and return inert historical request bytes."""

    payload = copy.deepcopy(dict(request))
    validate_payload(payload, "discovery_proof_worker_protocol.schema.json")
    if canonical_digest(payload) != expected_artifact_digest:
        raise ValueError("historical proof-worker request artifact digest mismatch")
    return {
        "status": "historical_decode_only",
        "authoritative_for_execution_or_theory": False,
        "artifact_digest": expected_artifact_digest,
        "payload": payload,
    }


def execute(request: Mapping[str, Any]) -> dict[str, Any]:
    """Reject before adapter, resource, filesystem, or subprocess activity."""

    del request
    raise RuntimeError(_HISTORY_ONLY_MESSAGE)


def main() -> int:
    try:
        request = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        if not isinstance(request, Mapping):
            raise ValueError("proof worker request must be a JSON object")
        execute(request)
    except Exception as exc:
        sys.stderr.write(f"{type(exc).__name__}: {exc}\n")
        return 2
    raise AssertionError("retired proof worker unexpectedly returned")


if __name__ == "__main__":
    raise SystemExit(main())
