"""Plan-bound conformance checks for generated Prism layer boundaries."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


def canonical_sha256(value: Any) -> str:
    """Return a stable digest for a reviewed JSON-compatible artifact."""
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def validate_generated_layers(project_root: Path, model: dict[str, Any]) -> list[str]:
    """Check that generated source respects the reviewed semantic layers."""
    root = project_root.resolve()
    workflows = model.get("workflows")
    if not isinstance(workflows, list) or len(workflows) != 1:
        return ["layer conformance requires exactly one reviewed workflow"]
    workflow = workflows[0]
    if not isinstance(workflow, dict):
        return ["reviewed workflow must be an object"]
    steps = workflow.get("steps")
    if not isinstance(steps, list) or not steps:
        return ["reviewed workflow must contain typed steps"]

    workflow_name = _pascal(str(workflow.get("id", "")))
    mode = str(workflow.get("semantic_mode", ""))
    epistemic = [step for step in steps if step.get("semantic_role") == "epistemic"]
    operational = [step for step in steps if step.get("semantic_role") == "operational"]
    reasoning_path = root / "reasoning.prism"
    materialization_path = root / "materialization.prism"
    main_path = root / "main.prism"
    issues: list[str] = []

    if operational and epistemic and mode != "mixed":
        issues.append("mixed operational/epistemic steps require semantic_mode mixed")
    if not epistemic and mode != "operational":
        issues.append("a workflow without epistemic steps must be operational")
    if not operational and mode == "mixed":
        issues.append("semantic_mode mixed requires at least one operational step")

    if not epistemic:
        if reasoning_path.exists():
            issues.append("operational workflow must not contain reasoning.prism")
    elif not reasoning_path.is_file():
        issues.append("workflow with epistemic occurrences requires reasoning.prism")
    else:
        reasoning = reasoning_path.read_text(encoding="utf-8")
        for step in epistemic:
            method = str(step.get("reasoning_type", ""))
            if not method or not re.search(rf"^type\s+{re.escape(method)}\b", reasoning, re.MULTILINE):
                issues.append(f"reasoning.prism omits epistemic operation {method or step.get('id')}")
            relation = step.get("relation_type")
            if relation and not re.search(rf"^relation\s+{re.escape(str(relation))}\b", reasoning, re.MULTILINE):
                issues.append(f"reasoning.prism omits declared relation {relation}")
        if mode == "mixed":
            if re.search(r"^reasoning\s+", reasoning, re.MULTILINE):
                issues.append("mixed reasoning.prism must not own the material workflow sequence")
            if "Computed[" in reasoning:
                issues.append("mixed reasoning.prism must not contain Computed material operations")
        elif mode == "epistemic":
            if not re.search(rf"^reasoning\s+{re.escape(workflow_name)}\b", reasoning, re.MULTILINE):
                issues.append("epistemic reasoning.prism omits the reviewed reasoning workflow")
            for step in steps[1:]:
                relation = step.get("relation_type")
                if relation and f"] by {relation}" not in reasoning:
                    issues.append(f"reasoning workflow does not license {step.get('id')} by {relation}")

    if not materialization_path.is_file():
        issues.append("generated project omits materialization.prism")
    else:
        materialization = materialization_path.read_text(encoding="utf-8")
        if mode in {"mixed", "operational"}:
            if not re.search(rf"^workflow\s+{re.escape(workflow_name)}\b", materialization, re.MULTILINE):
                issues.append("materialization.prism must own the mixed/operational workflow")
        elif f"converted_workflow = {workflow_name}(" not in materialization:
            issues.append("materialization.prism omits the epistemic workflow bindings")
        for step in operational:
            if step.get("material_kind") == "computed":
                marker = f"def {step.get('id')}_compute("
                if marker not in materialization:
                    issues.append(f"materialization.prism omits computed adapter binding {step.get('id')}")
        for step in epistemic:
            marker = f"agent {step.get('id')}_agent("
            if marker not in materialization:
                issues.append(f"materialization.prism omits epistemic agent binding {step.get('id')}")

    if not main_path.is_file():
        issues.append("generated project omits main.prism")
    return issues


def validate_generation_provenance(project_root: Path, model: dict[str, Any]) -> list[str]:
    """Bind the package-generated claim to the exact plan and Prism sources."""
    root = project_root.resolve()
    record_path = root / "conversion" / "generation.json"
    if not record_path.is_file():
        return ["generated project omits conversion/generation.json"]
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ["conversion/generation.json is not valid JSON"]
    issues: list[str] = []
    if record.get("generator") != "to_prism":
        issues.append("generation record does not identify the to_prism generator")
    expected_plan = "sha256:" + canonical_sha256(model)
    if record.get("generation_plan_sha256") != expected_plan:
        issues.append("generation-plan digest does not match conversion-model.json")
    hashes = record.get("source_hashes")
    if not isinstance(hashes, dict) or not hashes:
        issues.append("generation record omits generated Prism source hashes")
    else:
        for relative, expected in hashes.items():
            path = root / str(relative)
            if not path.is_file():
                issues.append(f"generated source is missing: {relative}")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                issues.append(f"generated source hash differs: {relative}")
    return issues


def _pascal(value: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in re.split(r"[-_]", value) if part)


__all__ = [
    "canonical_sha256",
    "validate_generated_layers",
    "validate_generation_provenance",
]
