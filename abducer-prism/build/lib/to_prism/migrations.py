"""Explicit, fail-closed migrations for persisted conversion documents."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .schemas import require_valid

CURRENT_SCHEMA_VERSION = "1.0"
MIGRATABLE_ARTIFACTS = frozenset(
    {
        "baseline",
        "contracts",
        "decisions",
        "inventory",
        "reasoning-map",
        "report",
        "to-prism-lock",
        "workflow",
    }
)


def migrate_document(document: dict[str, Any]) -> dict[str, Any]:
    """Migrate a known legacy document or reject an unknown future contract.

    Version ``0.9`` was the pre-release form of the 1.0 shape; its only wire
    difference was the version marker. No heuristic field repair is attempted.
    """
    artifact = document.get("artifact")
    if artifact not in MIGRATABLE_ARTIFACTS:
        raise ValueError(f"unsupported migration artifact: {artifact!r}")
    version = document.get("schema_version")
    if version == CURRENT_SCHEMA_VERSION:
        result = deepcopy(document)
    elif version == "0.9":
        result = deepcopy(document)
        result["schema_version"] = CURRENT_SCHEMA_VERSION
    else:
        raise ValueError(f"no migration from {artifact} schema version {version!r}")
    require_valid(result, str(artifact))
    return result


__all__ = ["CURRENT_SCHEMA_VERSION", "MIGRATABLE_ARTIFACTS", "migrate_document"]
