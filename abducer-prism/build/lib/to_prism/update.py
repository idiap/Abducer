"""Semantic inventory diffing and generated-file update boundaries."""

from __future__ import annotations

from typing import Any

from .jsonio import document_hash
from .lock import verify_generated_ownership


def semantic_inventory_diff(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    old_items = {item["id"]: item for item in old.get("items", [])}
    new_items = {item["id"]: item for item in new.get("items", [])}
    added = sorted(new_items.keys() - old_items.keys())
    removed = sorted(old_items.keys() - new_items.keys())
    affected: set[str] = set(added) | set(removed)
    for item_id in added:
        affected.update(
            item["id"] for item in new_items[item_id].get("semantic_elements", [])
        )
    for item_id in removed:
        affected.update(
            item["id"] for item in old_items[item_id].get("semantic_elements", [])
        )
    changed: list[dict[str, Any]] = []
    for item_id in sorted(old_items.keys() & new_items.keys()):
        before, after = old_items[item_id], new_items[item_id]
        if before == after:
            continue
        fields = sorted(
            key
            for key in before.keys() | after.keys()
            if before.get(key) != after.get(key)
        )
        changed.append({"fields": fields, "id": item_id})
        affected.add(item_id)
        affected.update(
            item["id"]
            for item in (
                old_items[item_id].get("semantic_elements", [])
                + new_items[item_id].get("semantic_elements", [])
            )
        )
    return {
        "added": added,
        "affected_dependencies": sorted(affected),
        "changed": changed,
        "new_inventory_hash": document_hash(new),
        "old_inventory_hash": document_hash(old),
        "removed": removed,
    }


def changed_dependencies(diff: dict[str, Any]) -> set[str]:
    direct = {
        *diff.get("added", []),
        *diff.get("removed", []),
        *(item["id"] for item in diff.get("changed", [])),
    }
    return direct | set(diff.get("affected_dependencies", []))


def detect_update_conflicts(
    output_root: Any, lock_document: dict[str, Any]
) -> list[dict[str, str]]:
    """Detect divergence before regeneration; user edits are never overwritten."""

    return verify_generated_ownership(output_root, lock_document)
