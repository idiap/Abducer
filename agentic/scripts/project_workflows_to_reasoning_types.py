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
"""Project authoritative skill-occurrence graphs into reasoning-type graphs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
ONTOLOGY = ROOT / "agentic/registries/essential_reasoning_types.yaml"
RELATIONS = ROOT / "agentic/registries/epistemic_relations.yaml"
NAMED = ROOT / "agentic/registries/named_workflow_contracts.yaml"
COHERE = ROOT / "agentic/registries/cohere_fast_ym_workflow.yaml"
OUTPUT = ROOT / "agentic/state/reasoning_type_workflow_projections.json"


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def mapping_index() -> tuple[dict[str, dict], set[str], dict[str, dict]]:
    payload = json.loads(ONTOLOGY.read_text(encoding="utf-8"))
    mappings = {row["skill"]: row for row in payload["skill_mappings"]}
    non_epistemic = {row["skill"] for row in payload.get("non_epistemic_materializers", [])}
    types = {row["id"]: row for row in payload["reasoning_types"]}
    return mappings, non_epistemic, types


def occurrence(node_id: str, skill: str, mappings: dict[str, dict], non_epistemic: set[str], types: dict[str, dict], **metadata: object) -> dict:
    if skill in mappings:
        row = mappings[skill]
        secondary = row.get("secondary_types", [])
        expression = {
            "kind": "atomic" if not secondary else "coinstantiated_unordered",
            "primary": row["primary_type"],
            "secondary": secondary,
            "input_state": types[row["primary_type"]]["input_state"],
            "output_state": types[row["primary_type"]]["output_state"],
            "claim_ceiling": types[row["primary_type"]]["claim_ceiling"],
        }
        classification = "epistemic"
    elif skill in non_epistemic:
        expression = {"kind": "epsilon_operational"}
        classification = "operational"
    else:
        expression = {"kind": "opaque_unmapped"}
        classification = "gap"
    return {
        "id": node_id,
        "classification": classification,
        "type_expression": expression,
        "provenance": {"skill": skill, **metadata},
    }


def named_projection(workflow: dict, mappings: dict[str, dict], non_epistemic: set[str], types: dict[str, dict]) -> dict:
    nodes: list[dict] = []
    steps = list(workflow["steps"])
    for profile in workflow.get("profiles", []):
        steps.extend(
            {**step, "id": f"{profile['id']}:{step['id']}", "profile": profile["id"]}
            for step in profile.get("steps", [])
        )
        steps.extend(
            {
                "id": f"{profile['id']}:specialist:{index}",
                "skill": skill,
                "mode": "profile_specialist",
                "when": "profile specialist ordering and join are unspecified",
                "consumes": [],
                "produces": [profile.get("specialist_output", "OpaqueProfileOutput")],
                "profile": profile["id"],
            }
            for index, skill in enumerate(profile.get("specialist_skills", []), 1)
        )
    for step in steps:
        nodes.append(
            occurrence(
                step["id"], step["skill"], mappings, non_epistemic, types,
                workflow_step=step["id"], mode=step.get("mode"),
                guard=step.get("when"), profile=step.get("profile"),
            )
        )
    producers: dict[str, list[str]] = {}
    by_id = {step["id"]: step for step in steps}
    for step in steps:
        for artifact in step.get("produces", []):
            producers.setdefault(artifact, []).append(step["id"])
    edges: list[dict] = []
    ambiguous_joins: list[dict] = []
    for step in steps:
        sources: list[str] = []
        for artifact in step.get("consumes", []):
            sources.extend(producers.get(artifact, []))
        sources = sorted(set(sources))
        if sources:
            edges.append({
                "sources": sources, "target": step["id"], "relation": "artifact_dependency",
                "epistemic_relation": "requires",
                "relational_coherence": "unknown_without_state_binding",
                "join": "single" if len(sources) == 1 else "unspecified",
                "guard": step.get("when"),
            })
        if len(sources) > 1 and any(by_id[source].get("mode") == "conditional" for source in sources):
            ambiguous_joins.append({
                "target": step["id"], "sources": sources,
                "reason": "conditional producers feed a multi-input step without all/any/fallback semantics",
            })
    mapped = sum(node["classification"] == "epistemic" for node in nodes)
    operational = sum(node["classification"] == "operational" for node in nodes)
    return {
        "workflow_id": workflow["id"],
        "projection_status": "complete" if mapped + operational == len(nodes) and not ambiguous_joins else "degraded",
        "occurrences": nodes,
        "relations": edges,
        "controls": {
            "iterations": [],
            "switches": [
                {"to": row["workflow"], "when": row["when"], "artifact_type": row["artifact_type"]}
                for row in workflow.get("handoffs", [])
            ],
        },
        "gaps": {
            "unmapped_occurrences": [node["id"] for node in nodes if node["classification"] == "gap"],
            "ambiguous_joins": ambiguous_joins,
        },
        "coverage": {
            "total": len(nodes), "mapped": mapped, "operational": operational,
            "unmapped": len(nodes) - mapped - operational,
            "mapped_fraction": round(mapped / len(nodes), 4) if nodes else 0,
        },
        "relational_coherence": {
            "status": "unknown",
            "resolved_edges": 0,
            "unknown_edges": len(edges),
            "reason": "Source artifacts do not yet bind claim identity, epistemic ports, or join modality.",
        },
    }


def cohere_projection(mappings: dict[str, dict], non_epistemic: set[str], types: dict[str, dict]) -> dict:
    workflow = yaml.safe_load(COHERE.read_text(encoding="utf-8"))
    nodes = [
        occurrence(
            row["id"], row["skill"], mappings, non_epistemic, types,
            subworkflow=row["subworkflow"], disposition=row["disposition"],
        )
        for row in workflow["nodes"]
    ]
    mapped = sum(node["classification"] == "epistemic" for node in nodes)
    return {
        "workflow_id": "cohere_fast",
        "projection_status": "complete" if mapped == len(nodes) else "degraded",
        "occurrences": nodes,
        "relations": [
            {"sources": list(row.get("depends_on", [])), "target": row["id"], "relation": "declared_dependency", "epistemic_relation": "requires", "relational_coherence": "unknown_without_state_binding", "join": "all" if len(row.get("depends_on", [])) > 1 else "single"}
            for row in workflow["nodes"] if row.get("depends_on")
        ],
        "controls": {"iterations": [], "switches": []},
        "gaps": {
            "unmapped_occurrences": [node["id"] for node in nodes if node["classification"] == "gap"],
            "ambiguous_joins": [],
            "identifier_alias_required": "subworkflow underscores in domain DAG versus hyphens in parent contract",
        },
        "coverage": {
            "total": len(nodes), "mapped": mapped, "operational": 0,
            "unmapped": len(nodes) - mapped,
            "mapped_fraction": round(mapped / len(nodes), 4),
        },
        "relational_coherence": {
            "status": "unknown",
            "resolved_edges": 0,
            "unknown_edges": sum(bool(row.get("depends_on")) for row in workflow["nodes"]),
            "reason": "Only one domain occurrence is curated and dependency edges carry no claim-state bindings.",
        },
    }


def build() -> dict:
    mappings, non_epistemic, types = mapping_index()
    named = json.loads(NAMED.read_text(encoding="utf-8"))
    projections = [named_projection(row, mappings, non_epistemic, types) for row in named["workflows"]]
    projections.append(cohere_projection(mappings, non_epistemic, types))
    return {
        "schema_version": "1.0.0",
        "view": "reasoning_type_occurrence_graph",
        "executable": False,
        "ontology": {"path": ONTOLOGY.relative_to(ROOT).as_posix(), "digest": digest(ONTOLOGY)},
        "relation_ontology": {"path": RELATIONS.relative_to(ROOT).as_posix(), "digest": digest(RELATIONS)},
        "sources": [
            {"path": NAMED.relative_to(ROOT).as_posix(), "digest": digest(NAMED)},
            {"path": COHERE.relative_to(ROOT).as_posix(), "digest": digest(COHERE)},
        ],
        "projection_rules": {
            "unmapped": "retain_as_opaque_gap",
            "multi_type": "single_coinstantiated_occurrence_without_invented_order",
            "operational": "epsilon_only_when_explicitly_declared",
            "joins": "preserve_or_mark_unspecified",
            "workflow_switches": "preserve_guard_and_target",
            "relational_coherence": "unknown_until_claim_identity_state_ports_and_join_semantics_are_bound",
        },
        "workflows": projections,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(build(), indent=2, sort_keys=True) + "\n"
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit("stale reasoning-type workflow projection")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(rendered, encoding="utf-8")
    payload = json.loads(rendered)
    mapped = sum(row["coverage"]["mapped"] for row in payload["workflows"])
    total = sum(row["coverage"]["total"] for row in payload["workflows"])
    print(f"reasoning-type projection current: mapped {mapped}/{total} occurrences")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
