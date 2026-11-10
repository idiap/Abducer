# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Conservative nominal contract recovery."""

from __future__ import annotations

import hashlib
import re
from typing import Any

from . import __version__
from .inventory import iter_inventory_items
from .jsonio import document_hash
from .model import SCHEMA_VERSION, require_unique

CONTRACT_KINDS = {
    "skill",
    "hook_group",
    "hook_handler",
    "command",
    "script",
    "tool",
    "agent",
    "subagent",
    "mcp_capability",
    "entry_point",
}


def _contract_id(item_id: str) -> str:
    return "contract_" + hashlib.sha256(item_id.encode("utf-8")).hexdigest()[:24]


def _name(item: dict[str, Any]) -> str:
    candidate = item.get("metadata", {}).get("name") or item["path"].rsplit("/", 1)[-1]
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", str(candidate)).strip("_")
    return normalized or item["id"]


def _port(item: dict[str, Any], direction: str) -> dict[str, Any]:
    metadata = item.get("metadata", {})
    explicit = metadata.get(f"{direction}_type")
    if isinstance(explicit, str) and explicit:
        return {
            "evidence": [{"kind": "declared-metadata", "location": item["path"]}],
            "status": "resolved",
            "type": explicit,
        }
    return {"evidence": [], "status": "unresolved", "type": None}


def build_contracts(inventory: dict[str, Any]) -> dict[str, Any]:
    contracts: list[dict[str, Any]] = []
    for item in iter_inventory_items(inventory):
        if item.get("kind") not in CONTRACT_KINDS:
            continue
        input_port = _port(item, "input")
        output_port = _port(item, "output")
        resolved = (
            input_port["status"] == "resolved" and output_port["status"] == "resolved"
        )
        effects = list(item.get("side_effect_hints", []))
        if item["kind"] in {"command", "script"} and "process" not in effects:
            effects.append("process")
        if item["kind"] == "mcp_capability" and "external-capability" not in effects:
            effects.append("external-capability")
        contracts.append(
            {
                "confidence": "explicit" if resolved else "unknown",
                "effects": sorted(set(effects)),
                "errors": [],
                "evidence": list(item.get("evidence", [])),
                "id": _contract_id(item["id"]),
                "input": input_port,
                "name": _name(item),
                "output": output_port,
                "permissions": sorted(set(item.get("permissions", []))),
                "providers": [item["provider"]],
                "review_status": "extracted" if resolved else "proposed",
                "source_item_id": item["id"],
            }
        )
    contracts.sort(key=lambda contract: (contract["source_item_id"], contract["id"]))
    document = {
        "artifact": "contracts",
        "contracts": contracts,
        "inventory_hash": document_hash(inventory),
        "schema_version": SCHEMA_VERSION,
        "tool": {"name": "to-prism", "version": __version__},
    }
    validate_contracts(document, inventory)
    return document


def validate_contracts(
    contracts_document: dict[str, Any], inventory: dict[str, Any] | None = None
) -> None:
    contracts = contracts_document.get("contracts", [])
    require_unique([contract["id"] for contract in contracts], "contract IDs")
    require_unique(
        [contract["source_item_id"] for contract in contracts], "contract sources"
    )
    if inventory is not None:
        item_ids = {item["id"] for item in iter_inventory_items(inventory)}
        dangling = sorted(
            contract["source_item_id"]
            for contract in contracts
            if contract["source_item_id"] not in item_ids
        )
        if dangling:
            raise ValueError(f"contracts refer to unknown inventory items: {dangling}")
    for contract in contracts:
        for port_name in ("input", "output"):
            port = contract[port_name]
            if port.get("status") == "resolved" and not port.get("type"):
                raise ValueError(
                    f"{contract['id']} has resolved {port_name} without a type"
                )
            if port.get("status") == "unresolved" and port.get("type") is not None:
                raise ValueError(
                    f"{contract['id']} has unresolved {port_name} with a type"
                )
