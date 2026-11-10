# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Conservative project-local epistemic mapping and extension validation."""

from __future__ import annotations

import hashlib
from typing import Any

from . import __version__
from .jsonio import document_hash
from .model import SCHEMA_VERSION

STANDARD_METHODS = {
    "deductive": "Deductive",
    "abductive": "Abductive",
    "inductive": "Inductive",
    "analogical": "Analogical",
    "contrastive": "Contrastive",
    "model_based": "ModelBased",
    "refutational": "Refutational",
    "evidential": "Evidential",
}

OPERATIONAL_ROLES = {
    "parse",
    "route",
    "format",
    "validate-schema",
    "invoke-tool",
    "invoke-model",
    "deploy",
    "collect",
    "aggregate-structure",
}


def build_reasoning_map(workflow_document: dict[str, Any]) -> dict[str, Any]:
    mappings: list[dict[str, Any]] = []
    for workflow in workflow_document.get("workflows", []):
        for node in workflow.get("nodes", []):
            role = str(node.get("epistemic_role", "")).strip().lower().replace("-", "_")
            node_id = str(node["id"])
            if not role or role.replace("_", "-") in OPERATIONAL_ROLES:
                mapping = {
                    "id": _mapping_id(node_id),
                    "node_id": node_id,
                    "classification": "operational_only",
                    "method": None,
                    "confidence": "unknown" if not role else "explicit",
                    "alternatives": [],
                    "evidence": list(node.get("evidence", [])),
                    "review_status": "extracted" if role else "proposed",
                    "relation": None,
                    "assurance": "ordinary",
                }
            elif role in STANDARD_METHODS:
                mapping = {
                    "id": _mapping_id(node_id),
                    "node_id": node_id,
                    "classification": "standard",
                    "method": STANDARD_METHODS[role],
                    "confidence": "explicit",
                    "alternatives": [],
                    "evidence": list(node.get("evidence", [])),
                    "review_status": "reviewed",
                    "relation": node.get("relation"),
                    "assurance": str(node.get("assurance", "ordinary")),
                }
            else:
                mapping = {
                    "id": _mapping_id(node_id),
                    "node_id": node_id,
                    "classification": "custom_proposal",
                    "method": None,
                    "confidence": "unknown",
                    "alternatives": list(STANDARD_METHODS.values()),
                    "evidence": list(node.get("evidence", [])),
                    "review_status": "proposed",
                    "relation": node.get("relation"),
                    "assurance": "ordinary",
                    "custom": {
                        "operation": role,
                        "inadequacy_analysis": {},
                        "input_type": None,
                        "result_type": None,
                        "materialization": None,
                    },
                }
            mappings.append(mapping)
    document = {
        "artifact": "reasoning-map",
        "schema_version": SCHEMA_VERSION,
        "mappings": sorted(mappings, key=lambda item: item["id"]),
        "tool": {"name": "to-prism", "version": __version__},
        "workflow_hash": document_hash(workflow_document),
    }
    validate_reasoning_map(document)
    return document


def validate_reasoning_map(
    document: dict[str, Any], *, require_approved: bool = False
) -> None:
    seen: set[str] = set()
    for mapping in document.get("mappings", []):
        mapping_id = str(mapping.get("id", ""))
        if not mapping_id or mapping_id in seen:
            raise ValueError(f"duplicate or empty reasoning mapping ID: {mapping_id!r}")
        seen.add(mapping_id)
        classification = mapping.get("classification")
        if (
            classification == "standard"
            and mapping.get("method") not in STANDARD_METHODS.values()
        ):
            raise ValueError(f"{mapping_id} names an unknown standard method")
        if classification == "operational_only" and mapping.get("method") is not None:
            raise ValueError(f"{mapping_id} operational mapping cannot name a method")
        if classification == "custom_proposal":
            custom = mapping.get("custom", {})
            missing = [
                field
                for field in (
                    "operation",
                    "input_type",
                    "result_type",
                    "materialization",
                )
                if not custom.get(field)
            ]
            analysis = custom.get("inadequacy_analysis", {})
            if not isinstance(analysis, dict) or not analysis:
                missing.append("inadequacy_analysis")
            if missing and mapping.get("review_status") in {"reviewed", "approved"}:
                raise ValueError(
                    f"{mapping_id} custom method is incomplete: {sorted(set(missing))}"
                )
            if mapping.get("review_status") == "approved":
                plausible = set(mapping.get("alternatives", []))
                if plausible - set(analysis):
                    raise ValueError(
                        f"{mapping_id} lacks inadequacy analysis for plausible standards"
                    )
        if require_approved and mapping.get("classification") != "operational_only":
            if mapping.get("review_status") != "approved":
                raise ValueError(f"{mapping_id} is not approved for generation")
        _validate_assurance(mapping)


def _validate_assurance(mapping: dict[str, Any]) -> None:
    assurance = mapping.get("assurance", "ordinary")
    allowed = {
        "ordinary",
        "generated",
        "evidence",
        "computed",
        "supported",
        "validated",
        "proof",
        "verified",
    }
    if assurance not in allowed:
        raise ValueError(f"{mapping.get('id')} has unknown assurance {assurance!r}")
    if assurance in {"evidence", "supported", "validated", "proof", "verified"}:
        if not mapping.get("assurance_constructor"):
            raise ValueError(
                f"{mapping.get('id')} strengthens assurance without a checked constructor"
            )


def _mapping_id(node_id: str) -> str:
    return "reasoning_" + hashlib.sha256(node_id.encode("utf-8")).hexdigest()[:24]


__all__ = [
    "OPERATIONAL_ROLES",
    "STANDARD_METHODS",
    "build_reasoning_map",
    "validate_reasoning_map",
]
