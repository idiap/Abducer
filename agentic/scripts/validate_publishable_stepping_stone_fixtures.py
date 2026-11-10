#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regression fixtures for publishable stepping-stone promotion logic."""

from __future__ import annotations

from agentic_common import fail
from build_scientific_contribution_monitor import (
    handoff_hard_gates,
    maturity_from_gates,
    publishable_subgoal_score,
    status_from_maturity,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def candidate(
    *,
    contribution_type: str,
    claim: str,
    certification_readiness: int,
    novelty_status: str,
    citation_tasks: list[str],
    disqualifier_verdicts: dict[str, str],
    overclaim: str,
) -> dict:
    return {
        "contribution_type": contribution_type,
        "smallest_honest_claim": claim,
        "scores": {
            "conceptual_novelty": 5,
            "explanatory_power": 5,
            "implications": 5,
            "certification_readiness": certification_readiness,
            "target_relevance": 5,
        },
        "prior_art_boundary": {
            "novelty_status": novelty_status,
            "citation_tasks": citation_tasks,
            "closest_known_results": ["fixture closest result"],
        },
        "disqualifier_tests": [
            {"name": name, "verdict": verdict, "evidence": f"fixture {name}"}
            for name, verdict in disqualifier_verdicts.items()
        ],
        "evidence_basis": ["fixture derivation"],
        "overclaim_boundary": overclaim,
    }


def assert_fixture(label: str, row: dict, expected_maturity: str, expected_status: str) -> None:
    gates = handoff_hard_gates(row)
    maturity = maturity_from_gates(gates)
    status = status_from_maturity(maturity, 100)
    require(maturity == expected_maturity, f"{label}: expected maturity {expected_maturity}, got {maturity}")
    require(status == expected_status, f"{label}: expected status {expected_status}, got {status}")
    exploration_score = 100
    publishable_score = publishable_subgoal_score(row["scores"], gates)
    require(
        publishable_score <= exploration_score,
        f"{label}: publishable score must not exceed exploration score",
    )
    if expected_maturity == "publishable_handoff_ready":
        require(all(gate.get("ready") for gate in gates.values()), f"{label}: publishable fixture must close all gates")
    else:
        require(
            not all(gate.get("ready") for gate in gates.values()),
            f"{label}: non-publishable fixture should leave at least one gate open",
        )


def main() -> int:
    finite_disqualifiers = {
        "already_known": "finite_check_queued",
        "proxy_problem": "pass",
        "target_equivalent_assumption": "pass",
        "evidence_gap": "pass",
        "validation_unbounded": "pass",
        "overclaim_risk": "pass",
        "narrow_bookkeeping": "pass",
    }
    passing_disqualifiers = {key: "pass" for key in finite_disqualifiers}

    assert_fixture(
        "high-scoring prior-art-unknown quantitative obstruction",
        candidate(
            contribution_type="quantitative_transfer_obstruction",
            claim="A bounded transfer obstruction names beta, q, and the collapse threshold.",
            certification_readiness=4,
            novelty_status="finite_check_queued",
            citation_tasks=["compare against hardness magnification and natural proofs"],
            disqualifier_verdicts=finite_disqualifiers,
            overclaim="This result does not prove the main target; it only bounds this transfer route.",
        ),
        "near_stepping_stone",
        "near_certification",
    )

    assert_fixture(
        "proper route-specific no-go handoff",
        candidate(
            contribution_type="route_specific_no_go",
            claim="A route-specific no-go theorem identifies the precise barrier assumptions.",
            certification_readiness=5,
            novelty_status="checked",
            citation_tasks=[],
            disqualifier_verdicts=passing_disqualifiers,
            overclaim="This result does not prove the main target; it rules out only the stated method class.",
        ),
        "publishable_handoff_ready",
        "good_enough_to_handoff",
    )

    assert_fixture(
        "interesting exploration without a named claim",
        candidate(
            contribution_type="contribution_search",
            claim="",
            certification_readiness=3,
            novelty_status="finite_check_queued",
            citation_tasks=["identify adjacent results"],
            disqualifier_verdicts=finite_disqualifiers,
            overclaim="This result does not prove the main target; a claim has not yet been stated.",
        ),
        "contribution_shaped",
        "active_candidate",
    )

    assert_fixture(
        "workflow-only improvement without external scientific object",
        candidate(
            contribution_type="method_or_workflow",
            claim="",
            certification_readiness=5,
            novelty_status="checked",
            citation_tasks=[],
            disqualifier_verdicts=passing_disqualifiers,
            overclaim="This result does not prove the main target; it is only an internal workflow improvement.",
        ),
        "contribution_shaped",
        "active_candidate",
    )

    print("validated publishable stepping-stone regression fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
