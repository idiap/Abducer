"""Small dependency-free schema checks used at all public boundaries."""

from __future__ import annotations

from typing import Any, Mapping

from .models import ResultStatus


class SchemaError(ValueError):
    pass


def validate_skill_result(value: Mapping[str, Any]) -> None:
    required = {"status", "artifacts", "claims", "uncertainties", "next", "provenance"}
    missing = required - value.keys()
    if missing:
        raise SchemaError(f"SkillResult missing fields: {sorted(missing)}")
    if value["status"] not in {item.value for item in ResultStatus}:
        raise SchemaError(f"invalid SkillResult status: {value['status']}")
    for key in ("artifacts", "claims", "uncertainties", "next"):
        if not isinstance(value[key], list):
            raise SchemaError(f"{key} must be a list")
    if not isinstance(value["provenance"], Mapping):
        raise SchemaError("provenance must be an object")


def validate_payload(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise SchemaError("skill input must be a JSON object")
    return dict(value)
