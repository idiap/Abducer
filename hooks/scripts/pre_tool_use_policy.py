#!/usr/bin/env python3
from __future__ import annotations

from hook_utils import DESTRUCTIVE_COMMAND_MARKERS, emit, has_evidence_marker, protected_path, read_payload, trace


def main() -> int:
    payload = read_payload()
    command = str(payload.get("command", ""))
    path = str(payload.get("path", ""))
    if any(marker in command for marker in DESTRUCTIVE_COMMAND_MARKERS):
        result = {"decision": "block", "reason": "Destructive command requires explicit user request and release evidence."}
    elif path and protected_path(path) and not has_evidence_marker(payload):
        result = {"decision": "warn", "reason": "Protected control-plane path change should cite TODO or decision evidence."}
    else:
        result = {"decision": "accept", "reason": "No deterministic pre-tool policy violation detected."}
    trace("pre_tool_use_policy", payload, result)
    emit(**result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
