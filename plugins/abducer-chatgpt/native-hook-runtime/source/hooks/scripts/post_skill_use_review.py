#!/usr/bin/env python3
from __future__ import annotations

from hook_utils import ROOT, emit, read_payload, trace


def main() -> int:
    payload = read_payload()
    missing = [path for path in payload.get("expected_artifacts", []) if not (ROOT / str(path)).exists()]
    if missing:
        result = {"decision": "warn", "reason": "Skill completed without expected artifacts.", "missing": missing}
    else:
        result = {"decision": "accept", "reason": "Expected post-skill artifacts are present."}
    trace("post_skill_use_review", payload, result)
    emit(**result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
