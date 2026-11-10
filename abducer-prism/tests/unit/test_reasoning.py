# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import pytest
from to_prism.reasoning import build_reasoning_map, validate_reasoning_map


def test_explicit_reasoning_role_maps_without_name_heuristics() -> None:
    workflow = {
        "workflows": [
            {
                "nodes": [
                    {"id": "deduce", "epistemic_role": "deductive", "evidence": []},
                    {"id": "format", "epistemic_role": "format", "evidence": []},
                    {
                        "id": "novel",
                        "epistemic_role": "causal-synthesis",
                        "evidence": [],
                    },
                ]
            }
        ]
    }
    result = build_reasoning_map(workflow)
    mappings = {item["node_id"]: item for item in result["mappings"]}
    assert mappings["deduce"]["method"] == "Deductive"
    assert mappings["format"]["classification"] == "operational_only"
    assert mappings["novel"]["classification"] == "custom_proposal"


def test_assurance_strengthening_requires_constructor() -> None:
    document = {
        "mappings": [
            {
                "id": "m",
                "classification": "standard",
                "method": "Evidential",
                "assurance": "evidence",
                "review_status": "approved",
            }
        ]
    }
    with pytest.raises(ValueError, match="without a checked constructor"):
        validate_reasoning_map(document)
