# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Deterministic machine and human conversion reports."""

from __future__ import annotations

from typing import Any

from . import __version__
from .inventory import iter_inventory_items
from .model import PRESERVATION_LEVELS, SCHEMA_VERSION


def build_report(
    inventory: dict[str, Any],
    contracts: dict[str, Any] | None = None,
    workflow: dict[str, Any] | None = None,
    *,
    conversion_class: str = "linked",
) -> dict[str, Any]:
    if conversion_class not in {"linked", "portable"}:
        raise ValueError("conversion class must be linked or portable")
    source_items = inventory.get("items", [])
    items = list(iter_inventory_items(inventory))
    unresolved = [item for item in items if item.get("disposition") == "unresolved"]
    unsupported = [item for item in items if item.get("disposition") == "unsupported"]
    contracts_list = contracts.get("contracts", []) if contracts else []
    unresolved_contracts = [
        contract
        for contract in contracts_list
        if contract.get("input", {}).get("status") == "unresolved"
        or contract.get("output", {}).get("status") == "unresolved"
    ]
    debts = [
        {
            "id": f"debt:{item['id']}",
            "kind": "unsupported-source-item",
            "source_item_id": item["id"],
            "status": "open",
        }
        for item in unsupported
    ]
    debts.extend(
        {
            "id": f"debt:{contract['id']}",
            "kind": "unresolved-contract",
            "contract_id": contract["id"],
            "status": "open",
        }
        for contract in unresolved_contracts
    )
    workflows = workflow.get("workflows", []) if workflow else []
    preservation = []
    for item in workflows:
        for level in PRESERVATION_LEVELS:
            preservation.append(
                {
                    "evidence": [],
                    "level": level,
                    "status": "not_tested",
                    "workflow_id": item["id"],
                }
            )
    publication = "blocked" if unresolved or unsupported else "review_required"
    return {
        "artifact": "report",
        "conversion_class": conversion_class,
        "debts": sorted(debts, key=lambda debt: debt["id"]),
        "preservation": preservation,
        "publication": publication,
        "schema_version": SCHEMA_VERSION,
        "summary": {
            "contracts": len(contracts_list),
            "semantic_elements": len(items) - len(source_items),
            "source_items": len(source_items),
            "unsupported_items": len(unsupported),
            "unresolved_items": len(unresolved),
            "workflows": len(workflows),
        },
        "tool": {"name": "to-prism", "version": __version__},
    }


def render_report_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Prism conversion report",
        "",
        f"Publication status: **{report['publication']}**",
        f"Conversion class: **{report['conversion_class']}**",
        "",
        "## Summary",
        "",
        f"- Source items: {summary['source_items']}",
        f"- Semantic elements: {summary.get('semantic_elements', 0)}",
        f"- Contracts: {summary['contracts']}",
        f"- Workflows: {summary['workflows']}",
        f"- Unresolved items: {summary['unresolved_items']}",
        f"- Unsupported items: {summary['unsupported_items']}",
        "",
        "## Preservation",
        "",
    ]
    if report["preservation"]:
        for result in report["preservation"]:
            lines.append(
                f"- `{result['workflow_id']}` / {result['level']}: {result['status']}"
            )
    else:
        lines.append("No workflow preservation claim has been established.")
    lines.extend(["", "## Conversion debt", ""])
    if report["debts"]:
        for debt in report["debts"]:
            subject = debt.get("source_item_id") or debt.get("contract_id")
            lines.append(f"- `{debt['kind']}` for `{subject}` ({debt['status']})")
    else:
        lines.append("No open conversion debt was recorded.")
    lines.extend(
        [
            "",
            "This report records evidence status; typed execution alone does not establish behavioral equivalence.",
            "",
        ]
    )
    return "\n".join(lines)


render_markdown = render_report_markdown
