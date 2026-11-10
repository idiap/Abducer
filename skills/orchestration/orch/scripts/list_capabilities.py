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
"""Project one epistemic reasoning type onto its registered materializers."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TYPE_REGISTRY = ROOT / "agentic/registries/essential_reasoning_types.yaml"
SKILL_REGISTRY = ROOT / "agentic/registries/skill_registry.yaml"
PROJECTIONS = ROOT / "registry/skill_projections/abducer_skill_projections.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def source_receipt(role: str, path: Path) -> dict[str, str]:
    return {
        "role": role,
        "path": str(path.relative_to(ROOT)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reasoning_type")
    parser.add_argument(
        "--domain",
        help="Optionally retain skills projected into this problem-domain taxonomy ID.",
    )
    args = parser.parse_args()

    type_payload = load(TYPE_REGISTRY)
    valid_types = {row["id"] for row in type_payload["reasoning_types"]}
    if args.reasoning_type not in valid_types:
        raise SystemExit(f"unknown reasoning type: {args.reasoning_type}")

    skills = {row["name"]: row for row in load(SKILL_REGISTRY)["skills"]}
    projections = {
        row["skill_name"]: row for row in load(PROJECTIONS)["skills"]
    }
    candidates = []
    for mapping in type_payload["skill_mappings"]:
        assigned = {mapping["primary_type"], *mapping.get("secondary_types", [])}
        if args.reasoning_type not in assigned:
            continue
        skill_name = mapping["skill"]
        skill = skills.get(skill_name)
        projection = projections.get(skill_name)
        if skill is None or projection is None:
            continue
        domains = projection.get("problem_domain_types", [])
        if args.domain and args.domain not in domains:
            continue
        candidates.append(
            {
                "skill": skill_name,
                "path": skill["path"],
                "mapping_kind": (
                    "primary"
                    if mapping["primary_type"] == args.reasoning_type
                    else "secondary"
                ),
                "mapping_confidence": mapping["confidence"],
                "epistemic_role": mapping["epistemic_role"],
                "workflow_role": projection["workflow_role"],
                "problem_domain_types": domains,
                "description": skill["description"],
            }
        )

    rank = {"primary": 0, "secondary": 1}
    confidence = {"high": 0, "medium": 1, "low": 2}
    candidates.sort(
        key=lambda row: (
            rank[row["mapping_kind"]],
            confidence[row["mapping_confidence"]],
            row["skill"],
        )
    )
    result = {
        "schema_version": "1.0.0",
        "mode": "orch_capability_query",
        "reasoning_type": args.reasoning_type,
        "domain_filter": args.domain,
        "registry_sources": [
            source_receipt("reasoning_types", TYPE_REGISTRY),
            source_receipt("skills", SKILL_REGISTRY),
            source_receipt("skill_projections", PROJECTIONS),
        ],
        "candidates": candidates,
        "blocked": not candidates,
        "selection_rule": "epistemic type first; contract and domain fit second; route validation before execution",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if candidates else 2


if __name__ == "__main__":
    raise SystemExit(main())
