"""Synthetic Claude PreToolUse hook used only as inventory fixture data."""

import json
import sys

payload = json.load(sys.stdin)
if payload.get("tool_name") in {"Write", "Edit"}:
    print("fixture is read-only", file=sys.stderr)
    raise SystemExit(2)
