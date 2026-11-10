# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Replayable semantic decision records."""

from __future__ import annotations

import hashlib
from typing import Any

from . import __version__
from .inventory import iter_inventory_items
from .model import SCHEMA_VERSION, require_unique

VALID_STATUSES = {"extracted", "proposed", "reviewed", "approved", "invalidated"}


def decision_id(kind: str, dependencies: list[str]) -> str:
    identity = f"{kind}\0" + "\0".join(sorted(dependencies))
    return "decision_" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]


def make_decision(
    *,
    kind: str,
    choice: Any,
    depends_on: list[str],
    rationale: str,
    status: str = "proposed",
    evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid decision status: {status}")
    dependencies = sorted(set(depends_on))
    return {
        "choice": choice,
        "depends_on": dependencies,
        "evidence": evidence or [],
        "id": decision_id(kind, dependencies),
        "kind": kind,
        "rationale": rationale,
        "status": status,
    }


def build_decisions(inventory: dict[str, Any]) -> dict[str, Any]:
    decisions = []
    for item in iter_inventory_items(inventory):
        if item.get("disposition") == "unresolved":
            decisions.append(
                make_decision(
                    kind="mapping-disposition",
                    choice="unresolved",
                    depends_on=[item["id"]],
                    rationale="A reviewer must choose convert, wrap, copy, exclude, or unsupported.",
                    evidence=item.get("evidence", []),
                )
            )
    decisions.sort(key=lambda decision: decision["id"])
    document = {
        "artifact": "decisions",
        "decisions": decisions,
        "schema_version": SCHEMA_VERSION,
        "tool": {"name": "to-prism", "version": __version__},
    }
    validate_decisions(document)
    return document


def validate_decisions(document: dict[str, Any]) -> None:
    decisions = document.get("decisions", [])
    require_unique([decision["id"] for decision in decisions], "decision IDs")
    for decision in decisions:
        if decision.get("status") not in VALID_STATUSES:
            raise ValueError(f"invalid decision status in {decision.get('id')}")


def invalidate_changed_decisions(
    document: dict[str, Any], changed_dependencies: set[str]
) -> dict[str, Any]:
    result = {**document, "decisions": []}
    for decision in document.get("decisions", []):
        copied = dict(decision)
        if changed_dependencies.intersection(decision.get("depends_on", [])):
            copied["status"] = "invalidated"
        result["decisions"].append(copied)
    validate_decisions(result)
    return result
