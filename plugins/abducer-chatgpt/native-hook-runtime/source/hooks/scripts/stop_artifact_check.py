#!/usr/bin/env python3
from __future__ import annotations

from hook_utils import ROOT, emit, read_payload, trace


REQUIRED = (
    "agentic/state/current_target.json",
    "agentic/state/dependency_frontier.json",
    "agentic/reports/compliance/latest.md",
    "agentic/reports/drift/latest.md",
    "agentic/todos/looper_integration_todos.yaml",
)


def main() -> int:
    payload = read_payload()
    if not payload.get("controlled", True):
        result = {"decision": "accept", "reason": "Uncontrolled stop does not require Looper artifacts."}
    else:
        missing = [path for path in REQUIRED if not (ROOT / path).exists()]
        if missing:
            result = {"decision": "block", "reason": "Missing controlled-iteration stop artifacts.", "missing": missing}
        else:
            result = {"decision": "accept", "reason": "Required stop-time artifacts are present."}
    trace("stop_artifact_check", payload, result)
    emit(**result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
