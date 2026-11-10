# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""
Regression tests for artifact contract validation across the KB reasoning framework.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
COMMON = ROOT / "skills" / "common"
if str(COMMON) not in sys.path:
    sys.path.insert(0, str(COMMON))

from contracts import validate_coherence_report
from contracts import validate_conjecture_report
from contracts import validate_proof_sketch_report
from contracts import validate_strategy_report


def test_validate_coherence_report_accepts_expected_shape() -> None:
    """
    Concept: Validates that validate coherence report accepts expected shape.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    payload = {
        "coherence_profile": {"global_coherence": 0.5},
        "hypothesis_coherence": [{"hypothesis_id": "h1", "coherence_delta_global": 0.1}],
    }
    validated = validate_coherence_report(payload)
    assert validated["coherence_profile"]["global_coherence"] == 0.5
    assert validated["hypothesis_coherence"][0]["hypothesis_id"] == "h1"


def test_validate_coherence_report_requires_fields() -> None:
    """
    Concept: Validates that validate coherence report requires fields.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    with pytest.raises(ValueError):
        validate_coherence_report({"hypothesis_coherence": []})
    with pytest.raises(ValueError):
        validate_coherence_report({"coherence_profile": {}})


def test_validate_conjecture_report_accepts_expected_shape() -> None:
    """
    Concept: Validates that validate conjecture report accepts expected shape.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    payload = {
        "gap_clusters": [{"bridge_id": "bridge.001"}],
        "abstraction_conjectures": [{"conjecture_id": "conj.001"}],
    }
    validated = validate_conjecture_report(payload)
    assert validated["gap_clusters"][0]["bridge_id"] == "bridge.001"
    assert validated["abstraction_conjectures"][0]["conjecture_id"] == "conj.001"


def test_validate_strategy_report_accepts_expected_shape() -> None:
    """
    Concept: Validates that validate strategy report accepts expected shape.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    payload = {
        "strategies": [{"strategy_id": "strat.001"}],
    }
    validated = validate_strategy_report(payload)
    assert validated["strategies"][0]["strategy_id"] == "strat.001"


def test_validate_proof_sketch_report_accepts_expected_shape() -> None:
    """
    Concept: Validates that validate proof sketch report accepts expected shape.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    payload = {
        "metadata": {"sketch_count": 1},
        "proof_sketches": [{"sketch_id": "psk.001"}],
        "recommended_execution_order": ["psk.001"],
    }
    validated = validate_proof_sketch_report(payload)
    assert validated["proof_sketches"][0]["sketch_id"] == "psk.001"
