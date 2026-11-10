# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial, oracle-anchored probes for high-risk conceptual generation."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from agentic.discovery.contracts import ContractError, canonical_digest
from agentic.discovery.hypotheses import (
    blind_articulation_digest,
    build_demo_high_risk_portfolio,
    structural_signature,
    validate_high_risk_portfolio,
)


CASES = Path(__file__).with_name("high_risk_hypothesis_cases.jsonl")


def _rehash(portfolio: dict) -> None:
    """Recompute the envelope digest after a deliberate adversarial mutation."""

    portfolio["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in portfolio.items()
            if key != "content_digest"
        }
    )


def _rebind_articulation(candidate: dict) -> None:
    """Keep inner provenance valid so each probe reaches its semantic oracle."""

    digest = blind_articulation_digest(candidate)
    candidate["blind_articulation_digest"] = digest
    candidate["literature_rebase_receipt"][
        "blind_articulation_digest"
    ] = digest


@pytest.mark.generative
@pytest.mark.parametrize(
    "case",
    [
        json.loads(line)
        for line in CASES.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ],
    ids=lambda case: case["case_id"],
)
def test_high_risk_quality_cases(case: dict) -> None:
    """Apply a metamorphic mutation and judge it with the stated fixed oracle."""

    portfolio = build_demo_high_risk_portfolio()
    mutation = case["mutation"]
    if mutation == "mystical_mechanism":
        portfolio["hypotheses"][0][
            "mechanism"
        ] = "Cosmic mystical vibration guarantees the answer."
    elif mutation == "remove_target_pressure":
        portfolio["hypotheses"][0]["target_pressures_addressed"] = []
    elif mutation == "claim_novelty":
        portfolio["hypotheses"][0]["novelty_claim"] = True
    elif mutation == "pending_rebase":
        portfolio["hypotheses"][0]["literature_relation"] = "pending_rebase"
    elif mutation == "active_structural_duplicate":
        left = portfolio["hypotheses"][0]
        right = portfolio["hypotheses"][1]
        right["ontology_delta"] = copy.deepcopy(left["ontology_delta"])
        right["mechanism_key"] = left["mechanism_key"]
        right["maturation_question"] = left["maturation_question"]
        right["genealogy"] = copy.deepcopy(left["genealogy"])
        right["structural_signature"] = structural_signature(right)
        right["selection_status"] = "selected_pareto"
    elif mutation != "none":
        raise AssertionError(f"unknown generative mutation: {mutation}")
    if mutation in {
        "mystical_mechanism",
        "remove_target_pressure",
        "active_structural_duplicate",
    }:
        _rebind_articulation(portfolio["hypotheses"][0])
        if mutation == "active_structural_duplicate":
            _rebind_articulation(portfolio["hypotheses"][1])
    _rehash(portfolio)

    if case["expected_valid"]:
        validate_high_risk_portfolio(portfolio)
    else:
        with pytest.raises(ContractError):
            validate_high_risk_portfolio(portfolio)
