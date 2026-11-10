#!/usr/bin/env python3
from __future__ import annotations

from hook_utils import emit, read_payload, trace


CONTROL_TERMS = ("systematically navigate", "fully", "end to end", "recursive", "keep working", "controlled", "goal-oriented")


def main() -> int:
    payload = read_payload()
    prompt = str(payload.get("prompt", "")).lower()
    if any(term in prompt for term in CONTROL_TERMS):
        result = {
            "decision": "warn",
            "reason": "Controlled target-navigation language detected; require target packet and workflow registry evidence.",
            "suggested_skill": "looper-target-goal-enricher",
        }
    else:
        result = {"decision": "accept", "reason": "No control-plane intake trigger detected."}
    trace("user_prompt_submit_intake", payload, result)
    emit(**result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
