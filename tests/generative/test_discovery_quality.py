# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Executable adversarial/generative fixtures for discovery-quality evaluation."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tests.discovery.test_discovery_independent_evaluation import evaluate, rich_candidate


CASES = [json.loads(line) for line in (Path(__file__).with_name("discovery_quality_cases.jsonl")).read_text(encoding="utf-8").splitlines() if line.strip()]


@pytest.mark.parametrize("case", CASES, ids=[row["case_id"] for row in CASES])
def test_adversarial_discovery_quality_case(case: dict) -> None:
    candidate = rich_candidate()
    genealogy: list[dict] = []
    mutation = case["mutation"]
    if mutation == "strip_typed_structure":
        for field in ("concepts", "ontology", "mechanism", "unification_map", "obligations", "predictions"):
            candidate.pop(field, None)
        candidate["self_assessment"] = "radical deep unified synthesis explanatory ontology"
    elif mutation == "paraphrase_existing":
        genealogy = [copy.deepcopy(candidate)]
        candidate["understanding_delta"]["before"] = "an algorithmic absence"
        candidate["understanding_delta"]["after"] = "a boundary obstruction under combination"
    elif mutation == "remove_mechanism_path":
        candidate["risk_reward"]["mechanism_path"] = ""
        candidate["risk_reward"]["truth_confidence"] = 0.05
    elif mutation == "assert_breakthrough_without_authority":
        candidate.update(promotion_requested=True, proof_status="open", evidence_status="open")
        candidate["self_assessment"] = "breakthrough proved"
    elif mutation == "remove_essential_relevance":
        candidate["relevance"] = {"essential": False, "target_dependencies": [], "root_tensions": []}
    elif mutation == "citation_absence_only":
        candidate["literature_snapshot"] = {"target_id": candidate["target_id"], "status": "missing", "citation_count": 0}
        candidate["source_relation_assessments"] = []
    elif mutation == "supersede_snapshot":
        candidate["literature_snapshot"]["status"] = "superseded"
    elif mutation == "validated_established_claim":
        candidate.update(
            promotion_requested=True,
            proof_status="proved",
            evidence_status="open",
            established_claim_gates=[{"gate_id": "proof-check", "applicability": "applicable", "status": "passed", "reason": "an independent checker validated the exact certificate"}],
        )
    else:  # pragma: no cover - keeps additions explicit.
        raise AssertionError(f"unknown fixture mutation: {mutation}")
    receipt = evaluate(candidate, genealogy)
    assert receipt["creative_worth_decision"] == case["expected_creative"]
    assert receipt["promotion_decision"] == case["expected_promotion"]
    assert receipt["literature_novelty"]["claim_allowed"] is case["expected_novelty"]

