#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Lightweight artifact contract validation for KB skill interoperability."""

from __future__ import annotations

from typing import Any


def _require_object(payload: Any, name: str) -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if not isinstance(payload, dict):
        raise ValueError(f"{name} must be a JSON/YAML object.")
    return payload


def _require_list_field(payload: dict[str, Any], name: str, field: str) -> list[Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    value = payload.get(field)
    if not isinstance(value, list):
        raise ValueError(f"{name}.{field} must be a list.")
    return value


def validate_phyp(payload: Any, name: str = "phyp") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    p = _require_object(payload, name)
    _require_list_field(p, name, "hypotheses")
    return p


def validate_connection_analysis(payload: Any, name: str = "analysis") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    p = _require_object(payload, name)
    _require_list_field(p, name, "top_interventions")
    _require_list_field(p, name, "connection_candidates")
    return p


def validate_entrypoints(payload: Any, name: str = "entrypoints") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    p = _require_object(payload, name)
    _require_list_field(p, name, "ranked_entrypoints")
    return p


def validate_pathways(payload: Any, name: str = "pathways") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    p = _require_object(payload, name)
    _require_list_field(p, name, "pathways")
    return p


def validate_bridges(payload: Any, name: str = "bridges") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    p = _require_object(payload, name)
    _require_list_field(p, name, "bridge_programs")
    return p


def validate_coherence_report(payload: Any, name: str = "coherence") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    p = _require_object(payload, name)
    _require_object(p.get("coherence_profile"), name + ".coherence_profile")
    _require_list_field(p, name, "hypothesis_coherence")
    return p


def validate_conjecture_report(payload: Any, name: str = "conjectures") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Enforces the schema for conjecture-mode outputs so downstream stages can safely consume gap and abstraction artifacts.
    """

    p = _require_object(payload, name)
    _require_list_field(p, name, "gap_clusters")
    _require_list_field(p, name, "abstraction_conjectures")
    return p


def validate_strategy_report(payload: Any, name: str = "strategies") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Enforces the schema for proof-strategy outputs so downstream stages can safely consume strategy portfolios.
    """

    p = _require_object(payload, name)
    _require_list_field(p, name, "strategies")
    return p


def validate_proof_sketch_report(payload: Any, name: str = "proof_sketches") -> dict[str, Any]:
    """
    Relevance: Operates within the shared utilities layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Enforces the schema for proof-sketch outputs so interpretation, orchestration, and later reasoning stages can consume structured proof outlines.
    """

    p = _require_object(payload, name)
    _require_object(p.get("metadata"), name + ".metadata")
    _require_list_field(p, name, "proof_sketches")
    _require_list_field(p, name, "recommended_execution_order")
    return p
