# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Evidence-backed semantic contracts for generated Prism source."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


class SemanticTypeError(ValueError):
    """A generation plan does not establish specific domain semantics."""


GENERIC_TYPE_NAMES = frozenset(
    {
        "any",
        "context",
        "conversiontask",
        "data",
        "input",
        "item",
        "object",
        "output",
        "payload",
        "record",
        "request",
        "response",
        "result",
        "state",
        "task",
        "text",
        "value",
    }
)

GENERIC_FIELD_NAMES = frozenset(
    {"content", "data", "input", "output", "payload", "result", "text", "value"}
)

SCALAR_TYPES = frozenset(
    {
        "Bool",
        "Bytes",
        "Char",
        "Decimal",
        "Duration",
        "Float",
        "Int",
        "Nat",
        "String",
        "Time",
        "Unit",
    }
)

CONTAINER_TYPES = frozenset({"List", "Map", "Option", "Set", "Tuple"})
IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
TYPE_EXPRESSION = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\[[A-Za-z0-9_, .\[\]]+\])?$")


@dataclass(frozen=True, slots=True)
class SemanticField:
    name: str
    type: str
    description: str


@dataclass(frozen=True, slots=True)
class SemanticVariant:
    name: str
    description: str
    fields: tuple[SemanticField, ...]


@dataclass(frozen=True, slots=True)
class SemanticType:
    name: str
    description: str
    kind: str
    fields: tuple[SemanticField, ...]
    variants: tuple[SemanticVariant, ...]


@dataclass(frozen=True, slots=True)
class SemanticContract:
    types: dict[str, SemanticType]
    mode: str
    workflow_name: str
    workflow_description: str
    input_name: str
    input_type: str
    output_type: str
    output_provenance: str
    fixture: Any
    assurance: str


def validate_semantic_contract(
    model: dict[str, Any], workflow: dict[str, Any], steps: list[dict[str, Any]]
) -> SemanticContract:
    """Require reviewed, nominal, non-placeholder contracts before generation."""
    if (
        model.get("artifact") != "generation-plan"
        or model.get("schema_version") != "1.0"
    ):
        raise SemanticTypeError(
            "generation requires artifact `generation-plan` at schema_version `1.0`"
        )
    types = _type_definitions(model.get("type_definitions"))
    description = _specific_text(workflow.get("description"), "workflow description")
    mode = str(workflow.get("semantic_mode", ""))
    if mode not in {"operational", "epistemic", "mixed"}:
        raise SemanticTypeError(
            "workflow semantic_mode must be operational, epistemic, or mixed"
        )
    input_spec = _object(workflow.get("input"), "workflow input")
    output_spec = _object(workflow.get("output"), "workflow output")
    input_name = _identifier(input_spec.get("name"), "workflow input name")
    input_type = _domain_type_name(input_spec.get("type"), "workflow input type")
    output_type = _domain_type_name(output_spec.get("type"), "workflow output type")
    for label, name in (
        ("workflow input", input_type),
        ("workflow output", output_type),
    ):
        if name not in types:
            raise SemanticTypeError(f"{label} type {name!r} has no type definition")
    output_provenance = str(output_spec.get("provenance", ""))
    if output_provenance not in {"generated", "computed"}:
        raise SemanticTypeError(
            "workflow output provenance must be `generated` or `computed`; "
            "stronger assurance needs an explicit material constructor"
        )
    epistemic = _object(workflow.get("epistemic_contract"), "epistemic_contract")
    for field in ("subject", "question", "output_meaning", "assurance_justification"):
        _specific_text(epistemic.get(field), f"epistemic_contract.{field}")
    observations = epistemic.get("observations")
    if not isinstance(observations, list) or not observations:
        raise SemanticTypeError("epistemic_contract.observations must be non-empty")
    for index, observation in enumerate(observations):
        _specific_text(observation, f"epistemic_contract.observations[{index}]")
    defeaters = epistemic.get("defeaters")
    if not isinstance(defeaters, list):
        raise SemanticTypeError("epistemic_contract.defeaters must be a list")
    _specific_text(
        epistemic.get("defeater_rationale"),
        "epistemic_contract.defeater_rationale",
    )
    if defeaters:
        for index, defeater in enumerate(defeaters):
            _specific_text(defeater, f"epistemic_contract.defeaters[{index}]")
    if epistemic.get("assurance") != "generated":
        raise SemanticTypeError(
            "epistemic_contract.assurance must be `generated` for a model-agent output"
        )
    unresolved = epistemic.get("unresolved")
    if not isinstance(unresolved, list):
        raise SemanticTypeError("epistemic_contract.unresolved must be a list")
    if unresolved:
        raise SemanticTypeError(
            "generation is blocked by unresolved semantic questions: "
            + "; ".join(str(item) for item in unresolved)
        )
    _validate_fixture(input_spec.get("fixture"), types[input_type], types)
    _validate_steps(steps, mode, input_type, output_type, types)
    if steps[-1].get("output_provenance") != output_provenance:
        raise SemanticTypeError(
            "workflow output provenance must match the final step constructor"
        )
    return SemanticContract(
        types=types,
        mode=mode,
        workflow_name=_pascal(str(workflow.get("id", ""))),
        workflow_description=description,
        input_name=input_name,
        input_type=input_type,
        output_type=output_type,
        output_provenance=output_provenance,
        fixture=input_spec.get("fixture"),
        assurance="generated",
    )


def validate_reasoning_projection(
    raw: Any,
    semantic: SemanticContract,
    steps: list[dict[str, Any]],
) -> None:
    """Validate a reviewed human-scale projection independently of material order."""
    if semantic.mode not in {"mixed", "operational"}:
        raise SemanticTypeError(
            "reasoning_projection is reserved for mixed or operational workflows "
            "whose material steps do not themselves define the reviewed high-level "
            "epistemic topology"
        )
    if not isinstance(raw, dict):
        raise SemanticTypeError("reasoning_projection must be an object")
    if (
        raw.get("input_name") != semantic.input_name
        or raw.get("input_type") != semantic.input_type
    ):
        raise SemanticTypeError(
            "reasoning_projection input must match the reviewed workflow boundary"
        )
    output_type = str(raw.get("output_type", ""))
    if output_type not in semantic.types:
        raise SemanticTypeError(
            f"reasoning_projection output type is undeclared: {output_type}"
        )
    occurrences = raw.get("occurrences")
    topology = raw.get("topology")
    if not isinstance(occurrences, list) or not occurrences:
        raise SemanticTypeError("reasoning_projection requires occurrences")
    if not isinstance(topology, list) or not topology:
        raise SemanticTypeError("reasoning_projection requires topology")

    by_id: dict[str, dict[str, Any]] = {}
    method_contracts: dict[str, tuple[str, str]] = {}
    known_steps = {str(step["id"]) for step in steps}
    covered_epistemic: set[str] = set()
    for occurrence in occurrences:
        if not isinstance(occurrence, dict):
            raise SemanticTypeError(
                "reasoning projection occurrence must be an object"
            )
        occurrence_id = str(occurrence.get("id", ""))
        if not occurrence_id or occurrence_id in by_id:
            raise SemanticTypeError(
                f"duplicate or empty reasoning occurrence ID: {occurrence_id!r}"
            )
        by_id[occurrence_id] = occurrence
        method = str(occurrence.get("method", ""))
        input_type = str(occurrence.get("input_type", ""))
        occurrence_output = str(occurrence.get("output_type", ""))
        if input_type not in semantic.types or occurrence_output not in semantic.types:
            raise SemanticTypeError(
                f"reasoning occurrence {occurrence_id} must use declared nominal types"
            )
        signature = (input_type, occurrence_output)
        if method in method_contracts and method_contracts[method] != signature:
            raise SemanticTypeError(
                f"reasoning method {method} is reused with incompatible contracts"
            )
        method_contracts[method] = signature
        material_steps = occurrence.get("material_steps")
        if not isinstance(material_steps, list) or not material_steps:
            raise SemanticTypeError(
                f"reasoning occurrence {occurrence_id} requires material_steps"
            )
        material_ids = set(map(str, material_steps))
        unknown_steps = sorted(material_ids - known_steps)
        if unknown_steps:
            raise SemanticTypeError(
                f"reasoning occurrence {occurrence_id} maps unknown material steps "
                f"{unknown_steps}"
            )
        covered_epistemic.update(material_ids)

    expected_epistemic = {
        str(step["id"])
        for step in steps
        if step.get("semantic_role") == "epistemic"
    }
    missing_epistemic = sorted(expected_epistemic - covered_epistemic)
    if missing_epistemic:
        raise SemanticTypeError(
            "reasoning_projection leaves epistemic material steps orphaned: "
            f"{missing_epistemic}"
        )

    ordered: list[str] = []
    available: dict[str, str] = {semantic.input_name: semantic.input_type}
    for topology_index, item in enumerate(topology):
        group = item.get("parallel") if isinstance(item, dict) else [item]
        if not isinstance(group, list) or not group:
            raise SemanticTypeError(
                "reasoning topology entries must name occurrences"
            )
        base_available = dict(available)
        produced: dict[str, str] = {}
        for raw_id in group:
            occurrence_id = str(raw_id)
            occurrence = by_id.get(occurrence_id)
            if occurrence is None:
                raise SemanticTypeError(
                    f"reasoning topology names unknown occurrence {occurrence_id}"
                )
            if occurrence_id in ordered:
                raise SemanticTypeError(
                    f"reasoning topology repeats occurrence {occurrence_id}"
                )
            relation = occurrence.get("relation")
            if topology_index == 0 and relation is not None:
                raise SemanticTypeError(
                    f"initial reasoning occurrence {occurrence_id} cannot declare "
                    "a prior-edge relation"
                )
            if topology_index > 0 and not relation:
                raise SemanticTypeError(
                    f"reasoning occurrence {occurrence_id} requires a named relation"
                )
            _validate_projection_arguments(occurrence, semantic, base_available)
            ordered.append(occurrence_id)
            produced[occurrence_id] = str(occurrence["output_type"])
        available.update(produced)

    if set(ordered) != set(by_id):
        raise SemanticTypeError(
            "reasoning topology must include every reviewed occurrence exactly once"
        )
    output_occurrence = str(raw.get("output_occurrence", ""))
    if not isinstance(topology[-1], str) or topology[-1] != output_occurrence:
        raise SemanticTypeError(
            "reasoning_projection output_occurrence must be the final topology occurrence"
        )
    if by_id[output_occurrence]["output_type"] != output_type:
        raise SemanticTypeError(
            "reasoning_projection output type does not match its output occurrence"
        )


def _validate_projection_arguments(
    occurrence: dict[str, Any],
    semantic: SemanticContract,
    available: dict[str, str],
) -> None:
    occurrence_id = str(occurrence["id"])
    arguments = occurrence.get("arguments")
    if not isinstance(arguments, list) or not arguments:
        raise SemanticTypeError(
            f"reasoning occurrence {occurrence_id} requires arguments"
        )
    sources: list[tuple[str | None, str, str]] = []
    for argument in arguments:
        if not isinstance(argument, dict):
            raise SemanticTypeError(
                f"reasoning occurrence {occurrence_id} argument must be an object"
            )
        source = str(argument.get("source", ""))
        if source not in available:
            raise SemanticTypeError(
                f"reasoning occurrence {occurrence_id} uses unavailable source {source}"
            )
        field = argument.get("field")
        sources.append(
            (str(field) if field is not None else None, source, available[source])
        )
    input_type = str(occurrence["input_type"])
    if len(sources) == 1 and sources[0][0] is None:
        if sources[0][2] != input_type:
            raise SemanticTypeError(
                f"reasoning occurrence {occurrence_id} expects {input_type}, "
                f"but source {sources[0][1]} produces {sources[0][2]}"
            )
        return
    if any(field is None for field, _, _ in sources):
        raise SemanticTypeError(
            f"reasoning occurrence {occurrence_id} record arguments must all name fields"
        )
    definition = semantic.types[input_type]
    if definition.kind != "record":
        raise SemanticTypeError(
            f"reasoning occurrence {occurrence_id} joins inputs through non-record "
            f"{input_type}"
        )
    expected = {field.name: field.type for field in definition.fields}
    supplied = {str(field): source_type for field, _, source_type in sources}
    if supplied != expected:
        raise SemanticTypeError(
            f"reasoning occurrence {occurrence_id} must bind exactly {expected}, "
            f"got {supplied}"
        )


def render_types(types: dict[str, SemanticType]) -> str:
    lines: list[str] = []
    for definition in types.values():
        lines.append(f"# {definition.description}")
        lines.append(f"type {definition.name}:")
        if definition.kind == "record":
            for field in definition.fields:
                lines.append(f"    # {field.description}")
                lines.append(f"    {field.name}: {field.type}")
        else:
            for variant in definition.variants:
                if variant.fields:
                    parameters = ", ".join(
                        f"{field.name}: {field.type}" for field in variant.fields
                    )
                    lines.append(f"    | {variant.name}({parameters})")
                else:
                    lines.append(f"    | {variant.name}")
        lines.append("")
    return "\n".join(lines)


def render_fixture(
    value: Any, type_name: str, definitions: dict[str, SemanticType], indent: int = 0
) -> str:
    definition = definitions[type_name]
    if definition.kind != "record" or not isinstance(value, dict):
        raise SemanticTypeError(f"fixture type {type_name} must be a record")
    prefix = " " * indent
    child = " " * (indent + 4)
    lines = [f"{type_name}("]
    for field in definition.fields:
        rendered = _render_value(value[field.name], field.type, definitions, indent + 4)
        lines.append(f"{child}{field.name} = {rendered},")
    lines.append(f"{prefix})")
    return "\n".join(lines)


def _type_definitions(raw: Any) -> dict[str, SemanticType]:
    if not isinstance(raw, list) or not raw:
        raise SemanticTypeError(
            "generation requires non-empty type_definitions; generic text envelopes are forbidden"
        )
    definitions: dict[str, SemanticType] = {}
    for index, item in enumerate(raw):
        specification = _object(item, f"type_definitions[{index}]")
        name = _domain_type_name(
            specification.get("name"), f"type_definitions[{index}].name"
        )
        if name in definitions:
            raise SemanticTypeError(f"duplicate type definition {name}")
        description = _specific_text(
            specification.get("description"), f"type {name} description"
        )
        kind = str(specification.get("kind", ""))
        if kind not in {"record", "variant"}:
            raise SemanticTypeError(f"type {name} kind must be record or variant")
        fields = _fields(specification.get("fields", []), f"type {name}")
        variants: tuple[SemanticVariant, ...] = ()
        if kind == "record":
            if not fields:
                raise SemanticTypeError(f"record type {name} must have fields")
            if len(fields) == 1 and fields[0].name.lower() in GENERIC_FIELD_NAMES:
                raise SemanticTypeError(
                    f"record type {name} is an uninformative one-field text/data envelope"
                )
        else:
            if fields:
                raise SemanticTypeError(
                    f"variant type {name} cannot declare record fields"
                )
            raw_variants = specification.get("variants")
            if not isinstance(raw_variants, list) or not raw_variants:
                raise SemanticTypeError(f"variant type {name} must have variants")
            parsed: list[SemanticVariant] = []
            for variant_index, raw_variant in enumerate(raw_variants):
                variant = _object(raw_variant, f"type {name} variant {variant_index}")
                variant_name = _domain_type_name(
                    variant.get("name"), f"type {name} variant {variant_index} name"
                )
                parsed.append(
                    SemanticVariant(
                        variant_name,
                        _specific_text(
                            variant.get("description"),
                            f"variant {variant_name} description",
                        ),
                        _fields(variant.get("fields", []), f"variant {variant_name}"),
                    )
                )
            variants = tuple(parsed)
        definitions[name] = SemanticType(name, description, kind, fields, variants)
    known = set(definitions) | set(SCALAR_TYPES) | set(CONTAINER_TYPES)
    for definition in definitions.values():
        for field in (
            *definition.fields,
            *(f for v in definition.variants for f in v.fields),
        ):
            if "Any" in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", field.type):
                raise SemanticTypeError(
                    f"{definition.name}.{field.name} cannot use Any"
                )
            unknown = sorted(
                set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", field.type)) - known
            )
            if unknown:
                raise SemanticTypeError(
                    f"{definition.name}.{field.name} refers to unknown types {unknown}"
                )
    return definitions


def _fields(raw: Any, owner: str) -> tuple[SemanticField, ...]:
    if not isinstance(raw, list):
        raise SemanticTypeError(f"{owner} fields must be a list")
    fields: list[SemanticField] = []
    seen: set[str] = set()
    for index, raw_field in enumerate(raw):
        field = _object(raw_field, f"{owner} field {index}")
        name = _identifier(field.get("name"), f"{owner} field {index} name")
        if name in seen:
            raise SemanticTypeError(f"{owner} has duplicate field {name}")
        seen.add(name)
        type_expression = str(field.get("type", ""))
        if TYPE_EXPRESSION.fullmatch(type_expression) is None:
            raise SemanticTypeError(
                f"{owner}.{name} has invalid type {type_expression!r}"
            )
        fields.append(
            SemanticField(
                name,
                type_expression,
                _specific_text(field.get("description"), f"{owner}.{name} description"),
            )
        )
    return tuple(fields)


def _validate_steps(
    steps: list[dict[str, Any]],
    mode: str,
    workflow_input: str,
    workflow_output: str,
    definitions: dict[str, SemanticType],
) -> None:
    prior = workflow_input
    for index, step in enumerate(steps):
        label = f"step {step['id']}"
        _specific_text(step.get("description"), f"{label} description")
        input_type = _domain_type_name(step.get("input_type"), f"{label} input_type")
        output_type = _domain_type_name(step.get("output_type"), f"{label} output_type")
        if input_type not in definitions or output_type not in definitions:
            raise SemanticTypeError(f"{label} types must name declared domain types")
        if input_type != prior:
            raise SemanticTypeError(
                f"{label} expects {input_type}, but its predecessor produces {prior}"
            )
        role = str(step.get("semantic_role", ""))
        if role not in {"operational", "epistemic"}:
            raise SemanticTypeError(
                f"{label} semantic_role must be operational or epistemic"
            )
        if mode == "operational" and role != "operational":
            raise SemanticTypeError(f"operational workflow contains epistemic {label}")
        if mode == "epistemic" and role != "epistemic":
            raise SemanticTypeError(
                "v1 epistemic generation requires each rendered occurrence to be epistemic; "
                f"keep operational {label} in materialization"
            )
        if role == "epistemic":
            _specific_text(
                step.get("granularity_rationale"),
                f"{label} granularity_rationale",
            )
            reasoning_type = _domain_type_name(
                step.get("reasoning_type"), f"{label} reasoning_type"
            )
            if reasoning_type in definitions:
                raise SemanticTypeError(
                    f"{label} reasoning_type must name an operation, not domain type {reasoning_type}"
                )
            _specific_text(
                step.get("reasoning_rationale"), f"{label} reasoning_rationale"
            )
        elif step.get("reasoning_type") is not None:
            raise SemanticTypeError(f"operational {label} cannot name a reasoning_type")
        if role == "operational" and step.get("relation_type") is not None:
            raise SemanticTypeError(
                f"operational {label} cannot name a reasoning relation"
            )
        skills = step.get("skills")
        if not isinstance(skills, list) or not skills:
            raise SemanticTypeError(
                f"{label} must be materialized by one or more reviewed skills"
            )
        paths: set[str] = set()
        for skill_index, skill in enumerate(skills):
            specification = _object(skill, f"{label} skill {skill_index}")
            path = str(specification.get("path", "")).strip()
            if not path:
                raise SemanticTypeError(f"{label} skill {skill_index} needs a path")
            if path in paths:
                raise SemanticTypeError(f"{label} repeats skill path {path}")
            paths.add(path)
            _specific_text(
                specification.get("role"), f"{label} skill {skill_index} role"
            )
            _specific_text(
                specification.get("contribution"),
                f"{label} skill {skill_index} contribution",
            )
        material_kind = str(step.get("material_kind", "agent"))
        if material_kind not in {"agent", "computed"}:
            raise SemanticTypeError(f"{label} material_kind must be agent or computed")
        effects = step.get("effects")
        if material_kind == "agent":
            if step.get("output_provenance") != "generated":
                raise SemanticTypeError(
                    f"agent {label} output_provenance must be generated"
                )
            if step.get("failure_type") != "ModelFailure":
                raise SemanticTypeError(f"agent {label} failure_type must be ModelFailure")
            if not isinstance(effects, list) or set(effects) != {
                "AI.Generate",
                "Context.Disclose",
            }:
                raise SemanticTypeError(
                    f"agent {label} must explicitly declare AI.Generate and Context.Disclose"
                )
        else:
            if role != "operational":
                raise SemanticTypeError(f"computed {label} must be operational")
            if step.get("output_provenance") != "computed":
                raise SemanticTypeError(
                    f"computed {label} output_provenance must be computed"
                )
            if step.get("failure_type") != "PythonError":
                raise SemanticTypeError(f"computed {label} failure_type must be PythonError")
            if effects != ["Python.Call"]:
                raise SemanticTypeError(
                    f"computed {label} must explicitly declare only Python.Call"
                )
            operation = str(step.get("adapter_operation", ""))
            if re.fullmatch(r"[a-z][a-z0-9_.-]*", operation) is None:
                raise SemanticTypeError(
                    f"computed {label} requires a reviewed adapter_operation"
                )
            procedure = str(step.get("procedure", ""))
            if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{2,}", procedure) is None:
                raise SemanticTypeError(
                    f"computed {label} requires a named deterministic procedure"
                )
        step["input_type"] = input_type
        step["output_type"] = output_type
        step["semantic_role"] = role
        step["material_kind"] = material_kind
        prior = output_type
    if prior != workflow_output:
        raise SemanticTypeError(
            f"workflow output is {workflow_output}, but final step produces {prior}"
        )
    final_provenance = str(steps[-1].get("output_provenance", ""))
    # The workflow-level wrapper must reflect the last explicit constructor.
    # This is checked here because the chain validator owns step ordering.
    if final_provenance not in {"generated", "computed"}:
        raise SemanticTypeError("final step has invalid output provenance")


def _validate_fixture(
    value: Any, definition: SemanticType, definitions: dict[str, SemanticType]
) -> None:
    if definition.kind != "record" or not isinstance(value, dict):
        raise SemanticTypeError("workflow fixture must be an object for a record input")
    expected = {field.name for field in definition.fields}
    actual = set(value)
    if actual != expected:
        raise SemanticTypeError(
            f"fixture for {definition.name} must have exactly {sorted(expected)}, got {sorted(actual)}"
        )
    for field in definition.fields:
        _render_value(value[field.name], field.type, definitions, 0)


def _render_value(
    value: Any, type_expression: str, definitions: dict[str, SemanticType], indent: int
) -> str:
    if type_expression == "String":
        if not isinstance(value, str):
            raise SemanticTypeError("fixture String field requires a string")
        return json.dumps(value, ensure_ascii=False)
    if type_expression == "Bool":
        if not isinstance(value, bool):
            raise SemanticTypeError("fixture Bool field requires a boolean")
        return "True" if value else "False"
    if type_expression in {"Int", "Nat"}:
        if not isinstance(value, int) or isinstance(value, bool):
            raise SemanticTypeError(
                f"fixture {type_expression} field requires an integer"
            )
        if type_expression == "Nat" and value < 0:
            raise SemanticTypeError("fixture Nat field cannot be negative")
        return str(value)
    if type_expression in {"Float", "Decimal"}:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise SemanticTypeError(
                f"fixture {type_expression} field requires a number"
            )
        return str(float(value))
    list_match = re.fullmatch(r"List\[(.+)\]", type_expression)
    if list_match:
        if not isinstance(value, list):
            raise SemanticTypeError("fixture List field requires an array")
        return (
            "["
            + ", ".join(
                _render_value(item, list_match.group(1), definitions, indent)
                for item in value
            )
            + "]"
        )
    if type_expression in definitions:
        return render_fixture(value, type_expression, definitions, indent)
    raise SemanticTypeError(
        f"fixture rendering does not support {type_expression}; provide a supported nominal/scalar/list shape"
    )


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SemanticTypeError(f"{label} must be an object")
    return value


def _identifier(value: Any, label: str) -> str:
    text = str(value or "")
    if IDENTIFIER.fullmatch(text) is None:
        raise SemanticTypeError(f"{label} must be an identifier")
    return text


def _domain_type_name(value: Any, label: str) -> str:
    name = _identifier(value, label)
    if name.lower() in GENERIC_TYPE_NAMES:
        raise SemanticTypeError(f"{label} {name!r} is generic and forbidden")
    return name


def _specific_text(value: Any, label: str) -> str:
    text = str(value or "").strip()
    if len(text) < 20:
        raise SemanticTypeError(
            f"{label} must state at least 20 characters of domain meaning"
        )
    return text


def _pascal(value: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", value)
    result = "".join(word[:1].upper() + word[1:] for word in words)
    if not result or result.lower() in GENERIC_TYPE_NAMES:
        raise SemanticTypeError("workflow id must yield a specific nominal name")
    return result


__all__ = [
    "GENERIC_TYPE_NAMES",
    "SemanticContract",
    "SemanticType",
    "SemanticTypeError",
    "render_fixture",
    "render_types",
    "validate_reasoning_projection",
    "validate_semantic_contract",
]
