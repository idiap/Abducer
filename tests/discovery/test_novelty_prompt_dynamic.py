# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for dynamic novelty prompt synthesis.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STRAT_SCRIPTS = ROOT / "skills" / "discovery" / "kb-novel-proof-strategist" / "scripts"
if str(STRAT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(STRAT_SCRIPTS))

from design_strategies import _build_dynamic_novelty_prompt


def test_dynamic_prompt_switches_to_risk_mode_when_coherence_is_low() -> None:
    """
    Concept: Validates that dynamic prompt switches to risk mode when coherence is low.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    strategies = [
        {
            "strategy_id": "strat.001",
            "anchor_statement_id": "st.a",
            "phase": "Meta-Complexity",
            "strategy_score": 0.8,
            "concept_fertility": 0.7,
        }
    ]
    prompt = _build_dynamic_novelty_prompt(
        strategies=strategies,
        coherence_profile={"global_coherence": 0.42, "tension": 0.51},
        coherence_index={"h1": {"coherence_delta_global": -0.2}},
    )
    assert "risk_mode=on" in prompt
    assert "coherence_preservation" in prompt


def test_dynamic_prompt_uses_high_novelty_mode_when_risk_is_low() -> None:
    """
    Concept: Validates that dynamic prompt uses high novelty mode when risk is low.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    strategies = [
        {
            "strategy_id": "strat.001",
            "anchor_statement_id": "st.a",
            "phase": "Meta-Complexity",
            "strategy_score": 0.8,
            "concept_fertility": 0.7,
        }
    ]
    prompt = _build_dynamic_novelty_prompt(
        strategies=strategies,
        coherence_profile={"global_coherence": 0.71, "tension": 0.14},
        coherence_index={"h1": {"coherence_delta_global": 0.12}},
    )
    assert "risk_mode=off" in prompt
    assert "0.38*phase_diversity" in prompt


def test_dynamic_prompt_reports_top_abstraction_conjectures_when_available() -> None:
    """
    Concept: Validates that dynamic prompt reports top abstraction conjectures when available.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    strategies = [
        {
            "strategy_id": "strat.001",
            "anchor_statement_id": "st.a",
            "phase": "Meta-Complexity",
            "strategy_score": 0.8,
            "concept_fertility": 0.7,
        }
    ]
    prompt = _build_dynamic_novelty_prompt(
        strategies=strategies,
        coherence_profile={"global_coherence": 0.71, "tension": 0.14},
        coherence_index={"h1": {"coherence_delta_global": 0.12}},
        top_abstractions=[
            {
                "conjecture_id": "conj.001",
                "abstraction_type": "intermediate-complexity-measure",
                "abstraction_label": "MCSP complexity potential",
                "definitional_profile": {
                    "necessary_attributes": [
                        {"attribute": "preserves `MCSP complexity profile`"},
                    ]
                },
                "counterfactual_probes": [
                    {"intervention": "Remove `preserves `MCSP complexity profile`` from the candidate abstraction."}
                ],
            }
        ],
    )
    assert "top_abstraction_conjectures=conj.001:intermediate-complexity-measure:MCSP complexity potential" in prompt
    assert "top_definitional_requirements=conj.001:preserves `MCSP complexity profile`" in prompt
    assert "top_counterfactual_probes=conj.001:Remove `preserves `MCSP complexity profile`` from the candidate abstraction." in prompt
