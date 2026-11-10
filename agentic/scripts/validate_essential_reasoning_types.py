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
"""Validate the initial many-to-many skill/epistemic-reasoning map."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "agentic/registries/essential_reasoning_types.yaml"
SKILLS = ROOT / "registry/skill_projections/abducer_skill_projections.json"
DOMAIN_BUNDLES = ROOT / "agentic/registries/domain_skill_bundles.yaml"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> int:
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    projected = {row["skill_name"] for row in json.loads(SKILLS.read_text(encoding="utf-8"))["skills"]}
    domain = yaml.safe_load(DOMAIN_BUNDLES.read_text(encoding="utf-8"))
    private = {skill for bundle in domain.get("bundles", []) for skill in bundle.get("allowed_skills", [])}
    known = projected | private
    types = payload.get("reasoning_types", [])
    type_ids = [row.get("id") for row in types]
    if len(types) != 8 or len(set(type_ids)) != len(type_ids):
        fail("initial registry must contain eight unique reasoning types")
    if {row.get("family") for row in types} != {"core_inference", "epistemic_control"}:
        fail("reasoning families must separate core inference and epistemic control")
    required_fields = {"definition", "input_state", "output_state", "warrant", "claim_ceiling", "failure_modes", "exemplar_skills"}
    for row in types:
        missing = sorted(field for field in required_fields if not row.get(field))
        if missing:
            fail(f"{row['id']} lacks fields: {missing}")
        unknown = sorted(set(row["exemplar_skills"]) - known)
        if unknown:
            fail(f"{row['id']} references unknown skills: {unknown}")
    mappings = payload.get("skill_mappings", [])
    mapped_names = [row.get("skill") for row in mappings]
    if len(set(mapped_names)) != len(mapped_names):
        fail("skill_mappings contains duplicate skills")
    for row in mappings:
        if row.get("skill") not in known:
            fail(f"mapping references unknown skill: {row.get('skill')}")
        assigned = {row.get("primary_type"), *row.get("secondary_types", [])}
        if not assigned <= set(type_ids):
            fail(f"{row['skill']} references unknown reasoning type")
        if row.get("epistemic_role") not in {"generator", "transformer", "validator", "adjudicator"}:
            fail(f"{row['skill']} has invalid epistemic_role")
        if row.get("confidence") not in {"high", "medium", "low"}:
            fail(f"{row['skill']} has invalid confidence")
    for row in payload.get("non_epistemic_materializers", []):
        if row.get("skill") not in known:
            fail(f"non-epistemic mapping references unknown skill: {row.get('skill')}")
        if row["skill"] in mapped_names:
            fail(f"{row['skill']} cannot be both epistemic and non-epistemic")
    for style in payload.get("reasoning_styles", []):
        composition = style.get("composition", [])
        if not composition or not set(composition) <= set(type_ids):
            fail(f"{style.get('id')} has invalid composition")
        if len(composition) != len(set(composition)):
            fail(f"{style.get('id')} repeats a reasoning type")
        if not style.get("required_guards"):
            fail(f"{style.get('id')} needs required guards")
    print(f"validated {len(type_ids)} essential reasoning types, {len(mappings)} curated skill mappings, {len(payload.get('reasoning_styles', []))} compositions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
