# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Focused identity tests for the canonical theory-support lane."""

from __future__ import annotations

import copy

from agentic.discovery.contracts import canonical_digest
from agentic.experiments.canonical_support_lane import _support_reference
from agentic.experiments.world_matrix import WORLD_IDS


def _reference(kind: str, generation: int) -> dict:
    return {
        "reference_kind": kind,
        "generation": generation,
        "manifest_digest": "sha256:" + f"{generation:064x}",
    }


def _completed_replay() -> dict:
    anchor = _reference("world_matrix_anchor_commit", 12)
    observations = [
        _reference(f"world_observation_{world_id}", 13 + index)
        for index, world_id in enumerate(WORLD_IDS)
    ]
    aggregation = _reference("world_matrix_aggregation_commit", 18)
    return {
        "programme_id": "programme-retry-stability",
        "anchor_transition": {
            "target_id": "support-target",
            "run_id": "support-run",
            "prior_generation": 11,
        },
        "anchor_reference": anchor,
        "observation_references": observations,
        "aggregation_reference": aggregation,
        "certificate": {
            "certificate_id": "support-certificate",
            "certificate_digest": "sha256:" + "a" * 64,
            "pending_review": {
                "requested": True,
                "effect": "next_cycle_reflection_only",
            },
            "derived_denials": {
                "theory_mutation_authorized": False,
                "theory_selection_authorized": False,
            },
        },
    }


def test_support_reference_binds_complete_committed_wave_not_completion_order() -> None:
    replay = _completed_replay()
    first = _support_reference(copy.deepcopy(replay))
    replay["diagnostic_parallel_completion_order"] = list(reversed(WORLD_IDS))
    second = _support_reference(copy.deepcopy(replay))

    assert second == first
    manifest = first["production_manifest"]
    assert manifest["canonical_commit_order"] == list(WORLD_IDS)
    assert manifest["anchor_reference"] == replay["anchor_reference"]
    assert manifest["observation_references"] == replay["observation_references"]
    assert manifest["aggregation_reference"] == replay["aggregation_reference"]
    assert manifest["production_manifest_digest"] == canonical_digest(
        {
            key: value
            for key, value in manifest.items()
            if key != "production_manifest_digest"
        }
    )
    assert first["production_manifest_digest"] == manifest[
        "production_manifest_digest"
    ]
    assert first["support_reference_digest"] == canonical_digest(
        {
            key: value
            for key, value in first.items()
            if key != "support_reference_digest"
        }
    )


def test_support_reference_changes_when_any_committed_world_reference_changes() -> None:
    baseline = _support_reference(_completed_replay())
    changed = _completed_replay()
    changed["observation_references"][2] = _reference(
        "world_observation_replacement", 15
    )

    replacement = _support_reference(changed)
    assert replacement["production_manifest_digest"] != baseline[
        "production_manifest_digest"
    ]
    assert replacement["support_reference_digest"] != baseline[
        "support_reference_digest"
    ]
