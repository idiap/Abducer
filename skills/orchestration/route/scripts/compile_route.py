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
"""Compile fixed PRISM reasoning steps to registered skill bindings."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.orchestration.reasoning_flow_language import (  # noqa: E402
    TYPE_CODES,
    occurrences,
    parse_file,
)

TYPE_REGISTRY = ROOT / "agentic/registries/essential_reasoning_types.yaml"
SKILL_REGISTRY = ROOT / "agentic/registries/skill_registry.yaml"
ROUTE_REGISTRY = ROOT / "agentic/registries/reasoning_capability_routes.yaml"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def source_receipt(role: str, path: Path) -> dict[str, str]:
    return {
        "role": role,
        "path": str(path.relative_to(ROOT)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def parse_bindings(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"invalid --bind {value!r}; expected alias=skill")
        alias, skill = value.split("=", 1)
        if not alias or not skill or alias in result:
            raise SystemExit(f"invalid or duplicate --bind alias: {alias!r}")
        result[alias] = skill
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("program", type=Path)
    parser.add_argument("--profile", default="default")
    parser.add_argument("--bind", action="append", default=[], metavar="ALIAS=SKILL")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    program = args.program.resolve()
    if not program.is_file() or program.suffix != ".prism":
        raise SystemExit("program must be an existing .prism file")

    type_payload = load(TYPE_REGISTRY)
    skill_payload = load(SKILL_REGISTRY)
    route_payload = load(ROUTE_REGISTRY)
    profiles = {row["id"]: row for row in route_payload["profiles"]}
    if args.profile not in profiles:
        raise SystemExit(f"unknown route profile: {args.profile}")
    profile = profiles[args.profile]
    explicit = parse_bindings(args.bind)

    known_skills = {row["name"]: row for row in skill_payload["skills"]}
    mappings = {row["skill"]: row for row in type_payload["skill_mappings"]}
    program_text = program.read_text(encoding="utf-8")
    reasoning = parse_file(program)

    nodes: list[tuple[str, dict]] = [("steps", row) for row in occurrences(reasoning["steps"])]
    for index, repeat in enumerate(reasoning["repeats"]):
        nodes.extend((f"repeat[{index}]", row) for row in occurrences(repeat["body"]))

    bindings = []
    blockers = []
    seen_aliases = {row.get("alias") for _, row in nodes if row.get("alias")}
    unknown_explicit = sorted(set(explicit) - seen_aliases)
    if unknown_explicit:
        blockers.append({"kind": "unknown_explicit_alias", "aliases": unknown_explicit})

    for location, node in nodes:
        alias = node.get("alias")
        if node["op"] == "gap":
            blockers.append({"kind": "unresolved_reasoning_gap", "location": location, "alias": alias})
            continue
        reasoning_type = TYPE_CODES[node["code"]]
        skill = explicit.get(alias) or profile["bindings"].get(reasoning_type)
        if not skill:
            blockers.append({"kind": "unbound_reasoning_type", "alias": alias, "reasoning_type": reasoning_type})
            continue
        mapping = mappings.get(skill)
        supported = mapping and reasoning_type in {
            mapping["primary_type"], *mapping.get("secondary_types", []),
        }
        if skill not in known_skills:
            blockers.append({"kind": "unknown_skill", "alias": alias, "skill": skill})
            continue
        if not supported:
            blockers.append({
                "kind": "mapping_mismatch", "alias": alias,
                "reasoning_type": reasoning_type, "skill": skill,
            })
            continue
        bindings.append({
            "location": location,
            "alias": alias,
            "code": node["code"],
            "reasoning_type": reasoning_type,
            "skill": skill,
            "skill_path": known_skills[skill]["path"],
            "mapping_kind": "primary" if mapping["primary_type"] == reasoning_type else "secondary",
            "confidence": mapping["confidence"],
            "inputs": node.get("inputs", []),
            "outputs": node.get("outputs", []),
        })

    result = {
        "schema_version": "1.0.0",
        "mode": "route",
        "program_id": reasoning["id"],
        "program_path": str(program.relative_to(ROOT)),
        "program_sha256": hashlib.sha256(program_text.encode("utf-8")).hexdigest(),
        "profile": args.profile,
        "registry_sources": [
            source_receipt("reasoning_types", TYPE_REGISTRY),
            source_receipt("skills", SKILL_REGISTRY),
            source_receipt("route_profiles", ROUTE_REGISTRY),
        ],
        "bindings": bindings,
        "blockers": blockers,
        "unresolved_obligations": ["validate every child output under its own skill contract"],
        "executable": not blockers,
        "validation_handoff": [
            "agentic/scripts/validate_essential_reasoning_types.py",
            "agentic/scripts/validate_skill_registry.py",
        ],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["executable"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
