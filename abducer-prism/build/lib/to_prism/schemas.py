"""Small dependency-free validator for the kit's versioned JSON contracts."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .paths import PathSafetyError, normalize_relative_path

SCHEMA_FILES = {
    "baseline": "baseline.schema.json",
    "inventory": "inventory.schema.json",
    "contracts": "contracts.schema.json",
    "workflow": "workflow.schema.json",
    "reasoning-map": "reasoning-map.schema.json",
    "decisions": "decisions.schema.json",
    "to-prism-lock": "lock.schema.json",
    "report": "report.schema.json",
    "provider-profile": "provider-profile.schema.json",
    "generation-plan": "generation-plan.schema.json",
    "project-semantic-taxonomy": "project-semantic-taxonomy.schema.json",
}

_GENERIC_SKILL_WORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "arbitrary",
        "content",
        "convert",
        "converts",
        "data",
        "do",
        "does",
        "generic",
        "handle",
        "handler",
        "input",
        "into",
        "of",
        "output",
        "perform",
        "performs",
        "process",
        "processes",
        "produce",
        "produces",
        "result",
        "return",
        "returns",
        "skill",
        "task",
        "text",
        "the",
        "this",
        "to",
        "transform",
        "transformation",
        "transforms",
        "value",
        "workflow",
        "worker",
    }
)


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


class SchemaValidationError(ValueError):
    def __init__(self, issues: list[ValidationIssue]):
        self.issues = tuple(issues)
        super().__init__("; ".join(map(str, issues)))


def schema_directory() -> Path:
    development = Path(__file__).resolve().parents[2] / "schemas"
    if development.is_dir():
        return development
    installed = Path(sys.prefix) / "share" / "to-prism" / "schemas"
    if installed.is_dir():
        return installed
    raise FileNotFoundError("to-prism JSON schemas are not installed")


def load_schema(name: str) -> dict[str, Any]:
    filename = SCHEMA_FILES.get(name, name if name.endswith(".schema.json") else "")
    if not filename:
        raise KeyError(f"unknown schema: {name}")
    with (schema_directory() / filename).open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"schema {filename} is not an object")
    return value


def _matches_type(value: Any, expected: str) -> bool:
    return {
        "array": isinstance(value, list),
        "boolean": isinstance(value, bool),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "null": value is None,
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "object": isinstance(value, dict),
        "string": isinstance(value, str),
    }.get(expected, True)


def _validate(value: Any, schema: dict[str, Any], path: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if "const" in schema and value != schema["const"]:
        issues.append(ValidationIssue(path, f"must equal {schema['const']!r}"))
        return issues
    if "enum" in schema and value not in schema["enum"]:
        issues.append(ValidationIssue(path, f"must be one of {schema['enum']!r}"))
        return issues
    expected = schema.get("type")
    if expected:
        allowed = [expected] if isinstance(expected, str) else expected
        if not any(_matches_type(value, item) for item in allowed):
            issues.append(ValidationIssue(path, f"must have type {allowed!r}"))
            return issues
    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                issues.append(
                    ValidationIssue(path, f"missing required property {key!r}")
                )
        properties = schema.get("properties", {})
        for key, item in value.items():
            child_path = f"{path}.{key}"
            if key in properties:
                issues.extend(_validate(item, properties[key], child_path))
            elif schema.get("additionalProperties") is False:
                issues.append(ValidationIssue(child_path, "unknown property"))
    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for index, item in enumerate(value):
            issues.extend(_validate(item, schema["items"], f"{path}[{index}]"))
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            issues.append(ValidationIssue(path, "string is too short"))
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            issues.append(
                ValidationIssue(path, "string does not match required pattern")
            )
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            issues.append(ValidationIssue(path, f"must be >= {schema['minimum']}"))
    return issues


def validate_document(
    document: Any, schema_name: str | None = None
) -> list[ValidationIssue]:
    if schema_name is None:
        if not isinstance(document, dict) or not isinstance(
            document.get("artifact"), str
        ):
            return [ValidationIssue("$", "artifact discriminator is required")]
        schema_name = document["artifact"]
    issues = _validate(document, load_schema(schema_name), "$")
    if not issues and isinstance(document, dict):
        issues.extend(_artifact_invariants(document, schema_name))
    return issues


def _duplicates(values: list[str]) -> list[str]:
    return sorted({value for value in values if values.count(value) > 1})


def _artifact_invariants(
    document: dict[str, Any], schema_name: str
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if schema_name == "inventory":
        items = document["items"]
        for duplicate in _duplicates([item["id"] for item in items]):
            issues.append(ValidationIssue("$.items", f"duplicate item ID {duplicate}"))
        for index, item in enumerate(items):
            try:
                normalize_relative_path(item["path"])
            except PathSafetyError:
                issues.append(
                    ValidationIssue(
                        f"$.items[{index}].path",
                        "must be canonical and source-relative",
                    )
                )
        coverage = document["coverage"]
        if coverage["total"] != len(items):
            issues.append(
                ValidationIssue("$.coverage.total", "does not match item count")
            )
        if coverage["classified"] + coverage["unresolved"] != coverage["total"]:
            issues.append(
                ValidationIssue(
                    "$.coverage", "classified + unresolved must equal total"
                )
            )
        semantic = [
            element for item in items for element in item.get("semantic_elements", [])
        ]
        semantic_coverage = document["semantic_coverage"]
        if semantic_coverage["total"] != len(semantic):
            issues.append(
                ValidationIssue(
                    "$.semantic_coverage.total", "does not match semantic element count"
                )
            )
        if (
            semantic_coverage["classified"] + semantic_coverage["unresolved"]
            != semantic_coverage["total"]
        ):
            issues.append(
                ValidationIssue(
                    "$.semantic_coverage",
                    "classified + unresolved must equal total",
                )
            )
    elif schema_name == "contracts":
        contracts = document["contracts"]
        for duplicate in _duplicates([item["id"] for item in contracts]):
            issues.append(
                ValidationIssue("$.contracts", f"duplicate contract ID {duplicate}")
            )
    elif schema_name == "workflow":
        workflows = document["workflows"]
        for duplicate in _duplicates([item["id"] for item in workflows]):
            issues.append(
                ValidationIssue("$.workflows", f"duplicate workflow ID {duplicate}")
            )
        from .graph import validate_workflow_graph

        issues.extend(
            ValidationIssue("$.workflows", diagnostic.message)
            for diagnostic in validate_workflow_graph(document)
        )
    elif schema_name == "reasoning-map":
        for duplicate in _duplicates(
            [item["id"] for item in document.get("mappings", [])]
        ):
            issues.append(
                ValidationIssue(
                    "$.mappings", f"duplicate reasoning mapping ID {duplicate}"
                )
            )
    elif schema_name == "decisions":
        for duplicate in _duplicates(
            [item["id"] for item in document.get("decisions", [])]
        ):
            issues.append(
                ValidationIssue("$.decisions", f"duplicate decision ID {duplicate}")
            )
    elif schema_name == "to-prism-lock":
        records = document["generated_files"]
        for duplicate in _duplicates([item.get("path", "") for item in records]):
            issues.append(
                ValidationIssue(
                    "$.generated_files", f"duplicate generated path {duplicate}"
                )
            )
        for index, item in enumerate(records):
            try:
                normalize_relative_path(item.get("path", ""))
            except PathSafetyError:
                issues.append(
                    ValidationIssue(
                        f"$.generated_files[{index}].path",
                        "must be canonical and output-relative",
                    )
                )
    elif schema_name == "generation-plan":
        workflows = document["workflows"]
        for duplicate in _duplicates([item["id"] for item in workflows]):
            issues.append(
                ValidationIssue("$.workflows", f"duplicate workflow ID {duplicate}")
            )
        from .semantic_types import SemanticTypeError, validate_semantic_contract

        for index, workflow in enumerate(workflows):
            steps = workflow["steps"]
            for duplicate in _duplicates([step["id"] for step in steps]):
                issues.append(
                    ValidationIssue(
                        f"$.workflows[{index}].steps",
                        f"duplicate step ID {duplicate}",
                    )
                )
            for step_index, step in enumerate(steps):
                effects = step["effects"]
                material_kind = step.get("material_kind", "agent")
                expected_effects = (
                    {"Python.Call"}
                    if material_kind == "computed"
                    else {"AI.Generate", "Context.Disclose"}
                )
                if len(effects) != len(expected_effects) or set(effects) != expected_effects:
                    message = (
                        "must contain only Python.Call exactly once"
                        if material_kind == "computed"
                        else "must contain AI.Generate and Context.Disclose exactly once"
                    )
                    issues.append(
                        ValidationIssue(
                            f"$.workflows[{index}].steps[{step_index}].effects",
                            message,
                        )
                    )
                skills = step["skills"]
                if not skills:
                    issues.append(
                        ValidationIssue(
                            f"$.workflows[{index}].steps[{step_index}].skills",
                            "must compose one or more explicitly attributed skills",
                        )
                    )
                for skill_index, skill in enumerate(skills):
                    for field in ("role", "contribution"):
                        words = set(re.findall(r"[a-z]+", skill[field].lower()))
                        if words and words <= _GENERIC_SKILL_WORDS:
                            issues.append(
                                ValidationIssue(
                                    f"$.workflows[{index}].steps[{step_index}].skills[{skill_index}].{field}",
                                    f"must identify a domain-specific skill {field}",
                                )
                            )
            try:
                validate_semantic_contract(
                    document,
                    workflow,
                    [dict(step) for step in steps],
                )
            except SemanticTypeError as error:
                issues.append(ValidationIssue(f"$.workflows[{index}]", str(error)))
    elif schema_name == "project-semantic-taxonomy":
        from .semantic_types import GENERIC_TYPE_NAMES

        objects = document["objects"]
        operations = document["operations"]
        for duplicate in _duplicates([item["id"] for item in objects]):
            issues.append(
                ValidationIssue("$.objects", f"duplicate object ID {duplicate}")
            )
        for duplicate in _duplicates([item["nominal_type"] for item in objects]):
            issues.append(
                ValidationIssue("$.objects", f"duplicate nominal type {duplicate}")
            )
        for index, item in enumerate(objects):
            if item["nominal_type"].lower() in GENERIC_TYPE_NAMES:
                issues.append(
                    ValidationIssue(
                        f"$.objects[{index}].nominal_type",
                        "must name a project-specific semantic object",
                    )
                )
            if not item["source_anchors"]:
                issues.append(
                    ValidationIssue(
                        f"$.objects[{index}].source_anchors",
                        "must contain project-source evidence",
                    )
                )
        for duplicate in _duplicates([item["id"] for item in operations]):
            issues.append(
                ValidationIssue("$.operations", f"duplicate operation ID {duplicate}")
            )
        nominal_types = {item["nominal_type"] for item in objects}
        for index, item in enumerate(operations):
            if (
                item["semantic_role"] == "epistemic"
                and item["result_provenance"] != "generated"
            ):
                issues.append(
                    ValidationIssue(
                        f"$.operations[{index}].result_provenance",
                        "epistemic occurrences in the to_prism conversion profile must be generated",
                    )
                )
            for field, message in (
                ("input_types", "must name one or more nominal input types"),
                ("skill_composition", "must attribute one or more source skills"),
                ("source_anchors", "must contain project-source evidence"),
            ):
                if not item[field]:
                    issues.append(
                        ValidationIssue(f"$.operations[{index}].{field}", message)
                    )
            for input_index, type_name in enumerate(item["input_types"]):
                if type_name not in nominal_types:
                    issues.append(
                        ValidationIssue(
                            f"$.operations[{index}].input_types[{input_index}]",
                            f"undeclared nominal type {type_name}",
                        )
                    )
            if item["output_type"] not in nominal_types:
                issues.append(
                    ValidationIssue(
                        f"$.operations[{index}].output_type",
                        f"undeclared nominal type {item['output_type']}",
                    )
                )
            for duplicate in _duplicates(
                [skill["path"] for skill in item["skill_composition"]]
            ):
                issues.append(
                    ValidationIssue(
                        f"$.operations[{index}].skill_composition",
                        f"duplicate skill path {duplicate}",
                    )
                )
    return issues


def require_valid(document: Any, schema_name: str | None = None) -> Any:
    issues = validate_document(document, schema_name)
    if issues:
        raise SchemaValidationError(issues)
    return document


validate_artifact = require_valid
