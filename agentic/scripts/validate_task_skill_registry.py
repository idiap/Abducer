#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Validate workflow-visible task registries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel, repo_path


TASKS = ROOT / "registry" / "tasks"
TAXONOMY = ROOT / "registry" / "taxonomy" / "workflow_taxonomy.json"


def taxonomy_ids() -> dict[str, set[str]]:
    taxonomy = load_json_object(TAXONOMY)
    return {
        "reasoning_types": {row["id"] for row in taxonomy["reasoning_types"]},
        "problem_domain_types": {row["id"] for row in taxonomy["problem_domain_types"]},
        "task_context_types": {row["id"] for row in taxonomy["task_context_types"]},
    }


def entry_names(manifest: dict[str, Any], key: str) -> set[str]:
    value = manifest.get(key, [])
    if not isinstance(value, list):
        return set()
    return {str(row.get("name")) for row in value if isinstance(row, dict) and row.get("name")}


def validate_manifest(path: Path, ids: dict[str, set[str]]) -> None:
    manifest = load_json_object(path)
    for field in ["task_id", "title", "status", "visible_workflows"]:
        if field not in manifest:
            fail(f"{rel(path)} missing {field}")
    workflows = manifest["visible_workflows"]
    if not isinstance(workflows, list) or not workflows:
        fail(f"{rel(path)} needs non-empty visible_workflows")
    declared_skills = entry_names(manifest, "reference_skills") | entry_names(manifest, "generated_skills")
    declared_hooks = entry_names(manifest, "reference_hooks") | entry_names(manifest, "generated_hooks")
    declared_workflows = entry_names(manifest, "reference_workflows") | entry_names(manifest, "generated_workflows")
    for section, entries in [
        ("reference_skills", manifest.get("reference_skills", [])),
        ("reference_hooks", manifest.get("reference_hooks", [])),
        ("reference_workflows", manifest.get("reference_workflows", [])),
        ("generated_skills", manifest.get("generated_skills", [])),
        ("generated_hooks", manifest.get("generated_hooks", [])),
        ("generated_workflows", manifest.get("generated_workflows", [])),
    ]:
        if not isinstance(entries, list):
            fail(f"{rel(path)} {section} must be a list")
        for entry in entries:
            if not isinstance(entry, dict):
                fail(f"{rel(path)} {section} entries must be objects")
            if not clean_text(entry.get("name")) or not clean_text(entry.get("why")):
                fail(f"{rel(path)} {section} entry missing name or why")
            raw_path = entry.get("path")
            if raw_path:
                repo_path(str(raw_path), must_exist=True)
    for workflow in workflows:
        if not isinstance(workflow, dict):
            fail(f"{rel(path)} visible_workflows entries must be objects")
        name = clean_text(workflow.get("name"))
        if not name:
            fail(f"{rel(path)} visible workflow missing name")
        for field in ["end_to_end_function", "key_function"]:
            if not clean_text(workflow.get(field)):
                fail(f"{rel(path)} visible workflow {name} missing {field}")
        if workflow["key_function"] not in ids["task_context_types"]:
            fail(f"{rel(path)} visible workflow {name} key_function must be a task_context_type")
        for field, allowed in ids.items():
            values = workflow.get(field)
            if not isinstance(values, list) or not values:
                fail(f"{rel(path)} visible workflow {name} needs non-empty {field}")
            unknown = [value for value in values if value not in allowed]
            if unknown:
                fail(f"{rel(path)} visible workflow {name} unknown {field}: {unknown}")
        for skill in workflow.get("composed_skills", []):
            if skill not in declared_skills:
                fail(f"{rel(path)} visible workflow {name} uses undeclared skill: {skill}")
        for hook in workflow.get("deterministic_hooks", []):
            if hook not in declared_hooks:
                fail(f"{rel(path)} visible workflow {name} uses undeclared hook: {hook}")
        for ref_name in workflow.get("workflow_references", []):
            if ref_name not in declared_workflows:
                fail(f"{rel(path)} visible workflow {name} uses undeclared workflow: {ref_name}")
        for field in ["artifacts", "validators"]:
            values = workflow.get(field)
            if not isinstance(values, list) or not values:
                fail(f"{rel(path)} visible workflow {name} needs non-empty {field}")
            for raw in values:
                repo_path(str(raw), must_exist=True)


def main() -> int:
    ids = taxonomy_ids()
    manifests = sorted(TASKS.glob("*/task_registry.json"))
    if not manifests:
        fail("no task registries found")
    for manifest in manifests:
        validate_manifest(manifest, ids)
    print(f"validated {len(manifests)} task workflow registries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
