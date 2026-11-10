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
"""Validate the essential epistemic-output algebra and example mappings."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "agentic/registries/epistemic_output_types.yaml"
NAMED = ROOT / "agentic/registries/named_workflow_contracts.yaml"
COHERE_SUBWORKFLOWS = ROOT / "agentic/registries/cohere_fast_subworkflows.yaml"
COHERE_ARTIFACTS = ROOT / "agentic/spec/cohere_fast_artifacts.schema.json"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def split_member(value: str) -> tuple[str, str]:
    if value.count(":") != 1:
        fail(f"output member must be Kind:subtype: {value!r}")
    return tuple(value.split(":", 1))  # type: ignore[return-value]


def known_artifacts() -> set[str]:
    named = json.loads(NAMED.read_text(encoding="utf-8"))
    result: set[str] = set()
    for workflow in named["workflows"]:
        result.add(workflow["input_artifact"]["type"])
        for step in workflow["steps"]:
            result.update(step.get("consumes", []))
            result.update(step.get("produces", []))
        for handoff in workflow.get("handoffs", []):
            result.add(handoff["artifact_type"])
        for profile in workflow.get("profiles", []):
            result.add(profile.get("specialist_output", ""))
            for step in profile.get("steps", []):
                result.update(step.get("consumes", []))
                result.update(step.get("produces", []))
    children = json.loads(COHERE_SUBWORKFLOWS.read_text(encoding="utf-8"))
    for row in children["subworkflows"]:
        result.add(row["input_type"])
        result.add(row["return_type"])
    cohere = json.loads(COHERE_ARTIFACTS.read_text(encoding="utf-8"))
    result.update(cohere.get("$defs", {}))
    return {value for value in result if value}


def main() -> int:
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    kinds = {row["id"]: row for row in payload["output_kinds"]}
    expected = {"KnowledgeBase", "Claim", "Evidence", "Decision", "Model", "Relation", "Obligation", "Plan", "Presentation", "Bundle"}
    if set(kinds) != expected:
        fail(f"output kinds mismatch: {sorted(set(kinds) ^ expected)}")
    common = set(payload["common_properties"])
    required_common = {"output_id", "kind", "reasoning_occurrence_id", "scope", "provenance", "taints", "open_obligations", "mutability", "terminality", "admissible_consumers"}
    if common != required_common:
        fail("common output envelope properties are incomplete")
    for kind, row in kinds.items():
        for field in ("meaning", "claim_effects", "default_mutability", "composition", "admissible_consumers", "subtypes"):
            if not row.get(field):
                fail(f"{kind} lacks {field}")
    for zero_kind in ("Evidence", "Model", "Plan", "Presentation"):
        if kinds[zero_kind]["claim_effects"] != ["none"]:
            fail(f"{zero_kind} must have zero direct claim effect")
    if kinds["Presentation"]["native_modality_required"]:
        fail("Presentation must not acquire epistemic modality")
    ports = payload["semantic_port_types"]
    port_ids = [row["id"] for row in ports]
    if len(port_ids) != len(set(port_ids)):
        fail("duplicate semantic port type")
    if any(row["output_kind"] not in kinds for row in ports):
        fail("semantic port references unknown output kind")
    codomains = {row["reasoning_type"]: row for row in payload["reasoning_codomains"]}
    if set(codomains) != set("DAITCMRE"):
        fail("every essential reasoning type needs exactly one codomain declaration")
    for code, row in codomains.items():
        for variant in row["variants"]:
            for member in variant["members"]:
                kind, subtype = split_member(member)
                if kind not in kinds or subtype not in kinds[kind]["subtypes"]:
                    fail(f"{code}/{variant['id']} references unknown output member {member}")
    for code in "DAITCM":
        members = {split_member(value)[0] for variant in codomains[code]["variants"] for value in variant["members"]}
        if not {"Claim", "Relation"} <= members:
            fail(f"{code} must emit both a Claim and its warrant Relation")
    r_variants = {row["id"]: row for row in codomains["R"]["variants"]}
    if any(split_member(value)[0] == "Claim" for value in r_variants["not_refuted"]["members"]):
        fail("R.not_refuted must not emit a positive Claim")
    e_members = {split_member(value)[0] for value in codomains["E"]["variants"][0]["members"]}
    if "Claim" in e_members or not {"Decision", "Relation"} <= e_members:
        fail("E must emit calibration Decision/Relation and no substantive Claim")
    known = known_artifacts()
    for row in payload["artifact_examples"]:
        if row["artifact_type"] not in known:
            fail(f"example references unknown artifact type: {row['artifact_type']}")
        for member in row["contains"]:
            kind, subtype = split_member(member)
            if kind not in kinds or subtype not in kinds[kind]["subtypes"]:
                fail(f"{row['artifact_type']} references unknown member {member}")
    print(
        f"validated {len(kinds)} output kinds, {len(ports)} semantic port types, "
        f"{len(codomains)} reasoning codomains, {len(payload['artifact_examples'])} artifact examples"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
