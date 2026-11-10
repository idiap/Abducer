"""Synthetic Codex hook used only as inventory fixture data."""

import json
import sys

payload = json.load(sys.stdin)
if payload.get("tool_name") == "apply_patch":
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "fixture is read-only",
                }
            }
        )
    )
