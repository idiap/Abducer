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
"""Validate skill identity and report evidence-bounded integration reachability.

The validator deliberately separates declaration from execution.  A skill in a
workflow with ``conditional`` or ``advisory`` mode is workflow-declared, but it
is runtime-routed only when the operator registry supplies a concrete route.
Execution and downstream effect require progressively stronger evidence.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

from agentic_common import ROOT, load_json_object, rel, write_json


SKILL_REGISTRY = ROOT / "agentic/registries/skill_registry.yaml"
QUALITY_REGISTRY = ROOT / "agentic/registries/skill_quality_registry.yaml"
WORKFLOW_REGISTRY = ROOT / "agentic/registries/workflow_contracts.yaml"
DISPATCH_REGISTRY = ROOT / "agentic/registries/discovery_marathon_skill_dispatch.yaml"
OPERATOR_REGISTRY = ROOT / "agentic/registries/discovery_operator_registry.yaml"
PROJECTIONS = ROOT / "registry/skill_projections/abducer_skill_projections.json"
TASK_ROOT = ROOT / "registry/tasks"
CATALOG = ROOT / "docs/reference/skills.md"
DEFAULT_REPORT = ROOT / "agentic/reports/skill_integration/latest.json"
OPERATOR_RECEIPT_SCHEMA = Path("agentic/spec/discovery_operator_receipt.schema.json")

LEVELS = (
    "catalogued",
    "workflow_declared",
    "runtime_routed",
    "executable",
    "exercised",
    "consumed",
    "feedback_effective",
)
WORKFLOW_MODES = {"required", "conditional", "advisory", "validator_only"}


class IntegrationError(ValueError):
    """Raised when integration declarations disagree."""


def _rows(path: Path, key: str) -> list[dict[str, Any]]:
    value = load_json_object(path).get(key)
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise IntegrationError(f"{rel(path)} needs an object list at {key}")
    return value


def _unique(rows: Iterable[Mapping[str, Any]], field: str, source: Path) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        value = row.get(field)
        if not isinstance(value, str) or not value.strip() or value in result:
            raise IntegrationError(f"{rel(source)} has missing or duplicate {field}: {value!r}")
        result[value] = row
    return result


def _skill_directories(root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for path in sorted((root / "skills").glob("*/*/SKILL.md")):
        name = path.parent.name
        if name in result:
            raise IntegrationError(f"duplicate skill directory name: {name}")
        result[name] = path.parent
    return result


def _catalogued_skill_ids(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(
        re.findall(r"\]\(\.\./\.\./skills/[^/]+/([^/]+)/SKILL\.md\)", text)
    )


def _path_exists_from_command(command: Any, root: Path) -> bool:
    if not isinstance(command, list) or not command or not all(
        isinstance(part, str) and part for part in command
    ):
        return False
    paths = [part for part in command if part.endswith((".py", ".sh"))]
    return bool(paths) and all((root / path).is_file() for path in paths)


def _operator_executable(operator: Mapping[str, Any], root: Path) -> bool:
    """Recognize only a routed adapter with validation and receipt contracts."""

    return bool(
        _path_exists_from_command(operator.get("entrypoint"), root)
        and _path_exists_from_command(operator.get("validator"), root)
        and operator.get("input_contract")
        and isinstance(operator.get("validators"), list)
        and operator["validators"]
        and (root / OPERATOR_RECEIPT_SCHEMA).is_file()
    )


def _load_workflows(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    index = load_json_object(root / rel(WORKFLOW_REGISTRY))
    pointer = index.get("named_workflow_contracts")
    if pointer is None:
        return list(index.get("workflows", [])), index
    if not isinstance(pointer, str) or not (root / pointer).is_file():
        raise IntegrationError("named_workflow_contracts must point to an existing registry")
    payload = load_json_object(root / pointer)
    workflows = payload.get("workflows")
    if not isinstance(workflows, list) or not all(isinstance(row, dict) for row in workflows):
        raise IntegrationError(f"{pointer} needs an object list at workflows")
    return workflows, index


def _workflow_declarations(
    root: Path, known: set[str]
) -> tuple[dict[str, list[dict[str, str]]], set[str]]:
    declarations: dict[str, list[dict[str, str]]] = defaultdict(list)
    workflow_ids: set[str] = set()
    workflows, index = _load_workflows(root)
    for workflow in workflows:
        workflow_id = workflow.get("id")
        if not isinstance(workflow_id, str) or not workflow_id or workflow_id in workflow_ids:
            raise IntegrationError(f"workflow has missing or duplicate id: {workflow_id!r}")
        workflow_ids.add(workflow_id)
        owner = workflow.get("owner_skill")
        if owner not in known:
            raise IntegrationError(f"workflow {workflow_id} has unknown owner skill {owner!r}")
        declarations[owner].append({"surface": "workflow_owner", "id": workflow_id, "mode": "required"})
        steps = workflow.get("steps", [])
        if not isinstance(steps, list):
            raise IntegrationError(f"workflow {workflow_id} steps must be a list")
        for step in steps:
            if not isinstance(step, dict):
                raise IntegrationError(f"workflow {workflow_id} has a malformed step")
            skill = step.get("skill")
            mode = step.get("mode")
            if skill not in known:
                raise IntegrationError(f"workflow {workflow_id} step has unknown skill {skill!r}")
            if mode not in WORKFLOW_MODES:
                raise IntegrationError(f"workflow {workflow_id} step {skill} has invalid mode {mode!r}")
            declarations[skill].append({"surface": "workflow_step", "id": workflow_id, "mode": mode})
        for profile in workflow.get("profiles", []):
            if not isinstance(profile, dict) or not isinstance(profile.get("id"), str):
                raise IntegrationError(f"workflow {workflow_id} has a malformed profile")
            profile_id = f"{workflow_id}:{profile['id']}"
            for step in profile.get("steps", []):
                if not isinstance(step, dict):
                    raise IntegrationError(f"workflow profile {profile_id} has a malformed step")
                skill = step.get("skill")
                mode = step.get("mode")
                if skill not in known or mode not in WORKFLOW_MODES:
                    raise IntegrationError(
                        f"workflow profile {profile_id} has invalid skill/mode {skill!r}/{mode!r}"
                    )
                declarations[skill].append(
                    {"surface": "workflow_profile_step", "id": profile_id, "mode": mode}
                )
            for skill in profile.get("specialist_skills", []):
                if skill not in known:
                    raise IntegrationError(f"workflow profile {profile_id} has unknown specialist {skill!r}")
                declarations[skill].append(
                    {"surface": "workflow_profile_specialist", "id": profile_id, "mode": "conditional"}
                )

    for workflow in index.get("workflows", []):
        if not isinstance(workflow, dict) or not isinstance(workflow.get("id"), str):
            raise IntegrationError("legacy workflow index has a malformed workflow")
        workflow_id = workflow["id"]
        workflow_ids.add(workflow_id)
        owner = workflow.get("owner_skill")
        if owner not in known:
            raise IntegrationError(f"legacy workflow {workflow_id} has unknown owner skill {owner!r}")
        declarations[owner].append(
            {"surface": "legacy_workflow_owner", "id": workflow_id, "mode": "required"}
        )

    task_workflow_ids: set[str] = set()
    for path in sorted((root / rel(TASK_ROOT)).glob("*/task_registry.json")):
        payload = load_json_object(path)
        declared = {
            row.get("name")
            for key in ("reference_skills", "generated_skills")
            for row in payload.get(key, [])
            if isinstance(row, dict)
        }
        unknown_declared = sorted(value for value in declared if value not in known)
        if unknown_declared:
            raise IntegrationError(f"{rel(path)} declares unknown skills: {unknown_declared}")
        references_named_registry = any(
            isinstance(row, dict)
            and row.get("path") == index.get("named_workflow_contracts")
            for key in ("reference_workflows", "generated_workflows")
            for row in payload.get(key, [])
        )
        for workflow in payload.get("visible_workflows", []):
            if not isinstance(workflow, dict) or not isinstance(workflow.get("name"), str):
                raise IntegrationError(f"{rel(path)} has a malformed visible workflow")
            task_workflow_ids.add(workflow["name"])
            if references_named_registry and workflow["name"] not in workflow_ids:
                raise IntegrationError(
                    f"{rel(path)} projects unknown named workflow {workflow['name']!r}"
                )
            for skill in workflow.get("composed_skills", []):
                if skill not in declared or skill not in known:
                    raise IntegrationError(
                        f"{rel(path)} workflow {workflow['name']} uses undeclared/unknown skill {skill!r}"
                    )
                declarations[skill].append(
                    {"surface": "task", "id": workflow["name"], "mode": "advisory"}
                )

    dispatch = load_json_object(root / rel(DISPATCH_REGISTRY))
    dispatch_fields = {
        "required_skills": "required",
        "conditional_skills": "conditional",
        "legacy_advisory_skills": "advisory",
    }
    for phase in dispatch.get("phases", []):
        if not isinstance(phase, dict) or not isinstance(phase.get("phase"), str):
            raise IntegrationError("discovery dispatch has a malformed phase")
        for field, mode in dispatch_fields.items():
            for skill in phase.get(field, []):
                if skill not in known:
                    raise IntegrationError(
                        f"dispatch phase {phase['phase']} references unknown skill {skill!r}"
                    )
                declarations[skill].append(
                    {
                        "surface": "dispatch",
                        "id": "discovery_marathon_loop",
                        "phase": phase["phase"],
                        "mode": mode,
                    }
                )
    return declarations, workflow_ids | task_workflow_ids


def _load_dispositions(
    root: Path, index: Mapping[str, Any], known: set[str]
) -> dict[str, Mapping[str, Any]]:
    pointer = index.get("skill_dispositions")
    if pointer is None:
        return {}
    if not isinstance(pointer, str) or not (root / pointer).is_file():
        raise IntegrationError("skill_dispositions must point to an existing registry")
    payload = load_json_object(root / pointer)
    allowed = set(payload.get("allowed_dispositions", []))
    expected = {"required", "conditional", "advisory", "validator_only", "standalone", "quarantined"}
    if allowed != expected:
        raise IntegrationError(f"{pointer} allowed_dispositions must equal {sorted(expected)}")
    raw_rows = payload.get("skills")
    if raw_rows is not None:
        rows = _unique(raw_rows, "skill", root / pointer)
    else:
        policy = payload.get("resolution_policy")
        if not isinstance(policy, dict):
            raise IntegrationError(f"{pointer} needs skills or resolution_policy")
        named, workflow_index = _load_workflows(root)
        sources: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
        for workflow in named:
            workflow_id = workflow["id"]
            for step in workflow.get("steps", []):
                sources["named_workflow_step"].append(
                    (step["skill"], step["mode"], workflow_id)
                )
            for profile in workflow.get("profiles", []):
                for step in profile.get("steps", []):
                    sources["named_profile_step"].append(
                        (step["skill"], step["mode"], workflow_id)
                    )
                for skill in profile.get("specialist_skills", []):
                    sources["named_profile_specialist"].append(
                        (skill, "conditional", workflow_id)
                    )
        for workflow in workflow_index.get("workflows", []):
            sources["legacy_workflow_owner"].append(
                (workflow["owner_skill"], "required", workflow["id"])
            )
        dispatch = load_json_object(root / rel(DISPATCH_REGISTRY))
        for phase in dispatch.get("phases", []):
            for skill in phase.get("required_skills", []):
                sources["dispatch_required"].append(
                    (skill, "required", "discovery_marathon_loop")
                )
            for skill in phase.get("conditional_skills", []):
                sources["dispatch_conditional"].append(
                    (skill, "conditional", "discovery_marathon_loop")
                )
            for skill in phase.get("legacy_advisory_skills", []):
                sources["dispatch_advisory"].append(
                    (skill, "advisory", "discovery_marathon_loop")
                )
        for task_path in sorted((root / rel(TASK_ROOT)).glob("*/task_registry.json")):
            task = load_json_object(task_path)
            for workflow in task.get("visible_workflows", []):
                workflow_id = workflow.get("workflow_id", workflow.get("name"))
                for skill in workflow.get("composed_skills", []):
                    sources["task_workflow_member"].append(
                        (skill, "advisory", workflow_id)
                    )
        precedence = policy.get("precedence")
        if not isinstance(precedence, list) or not precedence:
            raise IntegrationError(f"{pointer} resolution precedence must be non-empty")
        resolved: dict[str, Mapping[str, Any]] = {}
        for skill in sorted(known):
            chosen: tuple[str, str, str | None] | None = None
            for source in precedence:
                if source == "standalone_default":
                    rule = policy.get(source, {})
                    chosen = (source, rule.get("disposition", "standalone"), None)
                    break
                matches = [row for row in sources.get(source, []) if row[0] == skill]
                if matches:
                    _, mode, workflow_id = matches[0]
                    chosen = (source, mode, workflow_id)
                    break
            if chosen is None:
                raise IntegrationError(f"{pointer} cannot resolve a disposition for {skill}")
            source, disposition, primary = chosen
            rule = policy.get(source, {})
            resolved[skill] = {
                "skill": skill,
                "disposition": disposition,
                "primary_workflow": primary,
                "rationale": rule.get("rationale"),
                "resolution_source": source,
            }
        rows = resolved
    if set(rows) != known:
        raise IntegrationError(
            f"{pointer} skill coverage mismatch: missing={sorted(known - set(rows))}, extra={sorted(set(rows) - known)}"
        )
    for skill, row in rows.items():
        if row.get("disposition") not in allowed:
            raise IntegrationError(f"{pointer} has invalid disposition for {skill}")
        if not isinstance(row.get("rationale"), str) or not row["rationale"].strip():
            raise IntegrationError(f"{pointer} lacks a rationale for {skill}")
        if "executable" in row and not isinstance(row.get("executable"), bool):
            raise IntegrationError(f"{pointer} executable must be boolean for {skill}")
    return rows


def _receipt_levels(root: Path) -> dict[str, Mapping[str, bool]]:
    """Reuse the receipt-backed operator audit; absent evidence remains false."""

    if root.resolve() != ROOT.resolve():
        return {}
    try:
        from run_skill_reachability_audit import build_reachability_report

        report = build_reachability_report(
            receipt_root=root / "agentic/runs/discovery_operator_receipts",
            feedback_path=root / "agentic/state/discovery_feedback_edges.json",
            artifact_root=root,
        )
    except (ImportError, OSError, SystemExit, ValueError):
        return {}
    return {
        row["skill_id"]: row["levels"]
        for row in report.get("skills", [])
        if isinstance(row, dict) and isinstance(row.get("levels"), dict)
    }


def _attained_level(skill: str, flags: Mapping[str, bool]) -> str:
    """Require a monotone evidence ladder and return its highest level."""

    attained = "unreachable"
    for level in LEVELS:
        if flags[level]:
            attained = level
            continue
        later = [candidate for candidate in LEVELS[LEVELS.index(level) + 1 :] if flags[candidate]]
        if later:
            raise IntegrationError(
                f"{skill} reaches {later[0]} without preceding level {level}"
            )
        break
    return attained


def build_report(root: Path = ROOT) -> dict[str, Any]:
    skill_dirs = _skill_directories(root)
    known = set(skill_dirs)
    registry_path = root / rel(SKILL_REGISTRY)
    registry = _unique(_rows(registry_path, "skills"), "name", registry_path)
    projections_path = root / rel(PROJECTIONS)
    projections = _unique(_rows(projections_path, "skills"), "skill_name", projections_path)
    quality_path = root / rel(QUALITY_REGISTRY)
    quality = _unique(_rows(quality_path, "skill_quality"), "name", quality_path)
    catalogued = _catalogued_skill_ids(root / rel(CATALOG))

    for label, values in (
        ("skill registry", set(registry)),
        ("taxonomy projection", set(projections)),
        ("quality registry", set(quality)),
        ("documentation catalog", catalogued),
    ):
        if values != known:
            raise IntegrationError(
                f"{label} coverage mismatch: missing={sorted(known - values)}, extra={sorted(values - known)}"
            )
    for name, row in registry.items():
        expected = skill_dirs[name].relative_to(root).as_posix()
        if row.get("path") != expected or projections[name].get("path") != expected:
            raise IntegrationError(f"registry path mismatch for {name}: expected {expected}")

    declarations, workflow_ids = _workflow_declarations(root, known)
    _, workflow_index = _load_workflows(root)
    dispositions = _load_dispositions(root, workflow_index, known)
    operator_path = root / rel(OPERATOR_REGISTRY)
    operators = _unique(_rows(operator_path, "operators"), "operator_id", operator_path)
    operators_by_skill: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for operator_id, operator in operators.items():
        raw_skill_path = operator.get("skill_path")
        if not isinstance(raw_skill_path, str):
            raise IntegrationError(f"operator {operator_id} lacks skill_path")
        skill = Path(raw_skill_path).parent.name
        expected = f"skills/{Path(raw_skill_path).parent.parent.name}/{skill}/SKILL.md"
        if skill not in known or raw_skill_path != expected:
            raise IntegrationError(
                f"operator {operator_id} has unknown or noncanonical skill path {raw_skill_path!r}"
            )
        operators_by_skill[skill].append(operator)

    receipt_levels = _receipt_levels(root)
    rows: list[dict[str, Any]] = []
    for skill in sorted(known):
        declaration_rows = declarations.get(skill, [])
        skill_operators = operators_by_skill.get(skill, [])
        routed = any(isinstance(operator.get("entrypoint"), list) for operator in skill_operators)
        executable = any(_operator_executable(operator, root) for operator in skill_operators)
        disposition = dispositions.get(skill)
        if disposition:
            declared_disposition = disposition["disposition"]
            primary = disposition.get("primary_workflow")
            if declared_disposition in WORKFLOW_MODES and not declaration_rows:
                raise IntegrationError(f"{skill} is {declared_disposition} but has no workflow declaration")
            if declared_disposition in {"standalone", "quarantined"} and primary is not None:
                raise IntegrationError(f"{skill} disposition {declared_disposition} cannot name primary_workflow")
            if primary is not None and primary not in workflow_ids:
                raise IntegrationError(f"{skill} names unknown primary_workflow {primary!r}")
            if primary is not None:
                primary_rows = [
                    row
                    for row in declaration_rows
                    if row["id"] == primary or row["id"].startswith(f"{primary}:")
                ]
                if not primary_rows:
                    raise IntegrationError(
                        f"{skill} primary_workflow {primary!r} has no matching declaration"
                    )
                if declared_disposition not in {row["mode"] for row in primary_rows}:
                    raise IntegrationError(
                        f"{skill} disposition {declared_disposition!r} disagrees with primary workflow modes"
                    )
            if "executable" in disposition and disposition["executable"] != executable:
                raise IntegrationError(
                    f"{skill} executable disposition is {disposition['executable']} but operator evidence is {executable}"
                )

        evidence_rows = [
            receipt_levels.get(operator["operator_id"], {}) for operator in skill_operators
        ]
        evidence = {
            level: any(bool(row.get(level)) for row in evidence_rows)
            for level in ("exercised", "consumed", "feedback_effective")
        }
        flags = {
            "catalogued": True,
            "workflow_declared": bool(declaration_rows),
            "runtime_routed": routed,
            "executable": executable,
            "exercised": bool(evidence.get("exercised")),
            "consumed": bool(evidence.get("consumed")),
            "feedback_effective": bool(evidence.get("feedback_effective")),
        }
        required_dispatch = any(
            row["surface"] == "dispatch" and row["mode"] == "required"
            for row in declaration_rows
        )
        if required_dispatch and not routed:
            raise IntegrationError(
                f"{skill} is required by runtime dispatch but has no operator route"
            )
        attained = _attained_level(skill, flags)
        rows.append(
            {
                "skill_id": skill,
                "disposition": disposition.get("disposition") if disposition else None,
                "primary_workflow": disposition.get("primary_workflow") if disposition else None,
                "declarations": declaration_rows,
                "attained_level": attained,
                "levels": flags,
            }
        )

    level_counts = {
        level: sum(int(row["levels"][level]) for row in rows)
        for level in LEVELS
    }
    disposition_counts = {
        disposition: sum(int(row["disposition"] == disposition) for row in rows)
        for disposition in sorted({str(row["disposition"]) for row in rows})
    }
    return {
        "schema_version": "1.0.0",
        "evidence_ladder": list(LEVELS),
        "skill_count": len(rows),
        "workflow_id_count": len(workflow_ids),
        "dispositions_complete": len(dispositions) == len(rows),
        "level_counts": level_counts,
        "disposition_counts": disposition_counts,
        "authority_boundary": (
            "Workflow declarations, including advisory and conditional modes, do not establish "
            "runtime routing, execution, consumption, or feedback effect."
        ),
        "skills": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--check-report", type=Path)
    args = parser.parse_args()
    try:
        report = build_report(args.root.resolve())
        if args.check_report:
            existing = load_json_object(args.check_report)
            if existing != report:
                raise IntegrationError(f"integration report is stale: {args.check_report}")
        if args.json_output:
            write_json(args.json_output, report)
    except (IntegrationError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    counts = {
        level: sum(row["levels"][level] for row in report["skills"])
        for level in LEVELS
    }
    print(
        f"validated {report['skill_count']} skills across registries; "
        + ", ".join(f"{level}={counts[level]}" for level in LEVELS)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
