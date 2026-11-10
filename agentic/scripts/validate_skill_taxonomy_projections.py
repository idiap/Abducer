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

"""Validate skill taxonomy projections."""

from __future__ import annotations

from agentic_common import ROOT, fail, iter_skill_dirs, load_json_object, rel, skill_name_from_dir


PROJECTIONS = ROOT / "registry" / "skill_projections" / "abducer_skill_projections.json"
TAXONOMY = ROOT / "registry" / "taxonomy" / "workflow_taxonomy.json"


def main() -> int:
    taxonomy = load_json_object(TAXONOMY)
    allowed = {
        "reasoning_types": {row["id"] for row in taxonomy["reasoning_types"]},
        "problem_domain_types": {row["id"] for row in taxonomy["problem_domain_types"]},
        "task_context_types": {row["id"] for row in taxonomy["task_context_types"]},
    }
    payload = load_json_object(PROJECTIONS)
    rows = payload.get("skills")
    if not isinstance(rows, list) or not rows:
        fail(f"{rel(PROJECTIONS)} needs non-empty skills list")
    seen: set[str] = set()
    projected = set()
    for row in rows:
        if not isinstance(row, dict):
            fail(f"{rel(PROJECTIONS)} skills entries must be objects")
        name = row.get("skill_name")
        if not isinstance(name, str) or not name:
            fail(f"{rel(PROJECTIONS)} has projection without skill_name")
        if name in seen:
            fail(f"{rel(PROJECTIONS)} duplicate projection for {name}")
        seen.add(name)
        path = ROOT / str(row.get("path", ""))
        if not (path / "SKILL.md").exists():
            fail(f"{rel(PROJECTIONS)} projection path missing SKILL.md for {name}: {row.get('path')}")
        projected.add(name)
        for field, ids in allowed.items():
            values = row.get(field)
            if not isinstance(values, list) or not values:
                fail(f"{rel(PROJECTIONS)} projection {name} missing {field}")
            unknown = [value for value in values if value not in ids]
            if unknown:
                fail(f"{rel(PROJECTIONS)} projection {name} has unknown {field}: {unknown}")
        for field in ["workflow_role", "inputs", "outputs", "deterministic_boundaries", "generative_boundaries", "validators", "failure_modes"]:
            value = row.get(field)
            if not value:
                fail(f"{rel(PROJECTIONS)} projection {name} missing {field}")
    missing = {skill_name_from_dir(path) for path in iter_skill_dirs()} - projected
    if missing:
        fail(f"{rel(PROJECTIONS)} missing projections for skills: {', '.join(sorted(missing))}")
    print(f"validated {len(rows)} skill taxonomy projections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
