"""Synthetic successful Codex Stop hook fixture."""

import json
import sys

json.load(sys.stdin)
print(json.dumps({"continue": True}))
