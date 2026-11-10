#!/usr/bin/env python3
from __future__ import annotations

import json

from hook_utils import ROOT, emit, read_payload, trace


def _declared_skills() -> set[str]:
    skills = set()
    for path in (ROOT / "registry" / "tasks").glob("*/task_registry.json"):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        for workflow in manifest.get("visible_workflows", []):
            for skill in workflow.get("composed_skills", []):
                skills.add(str(skill))
    return skills


def main() -> int:
    payload = read_payload()
    skill = str(payload.get("skill", ""))
    controlled = bool(payload.get("controlled", True))
    declared = _declared_skills()
    if controlled and skill and skill not in declared:
        result = {"decision": "block", "reason": f"Skill `{skill}` is not declared in any visible workflow."}
    else:
        result = {"decision": "accept", "reason": "Skill is declared or invocation is explicitly uncontrolled."}
    trace("pre_skill_use_policy", payload, result)
    emit(**result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
