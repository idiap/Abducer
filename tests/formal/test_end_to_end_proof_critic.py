# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for the end-to-end proof critic."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMON_DIR = ROOT / "skills" / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from end_to_end_plausibility import build_plausibility_report
from end_to_end_plausibility import render_plausibility_markdown


def _base_macro_state() -> dict:
    return {
        "main_conjecture": {
            "core_claim": "P != NP",
            "route_target_claim": "NP not in P/poly",
            "grounding_implication": "If NP not in P/poly, then P != NP.",
        },
        "leading_route": {
            "candidate_object": "MCSP witness family",
            "carrier_kind": "family of instances equipped with a monotone witness measure",
            "negative_route": "The witness family could fail to encode the source hardness.",
            "failure_diagnosis": "The route collapses if the bridge object is only topical overlap.",
            "mathematical_assumptions": ["Assume an admissible witness family exists."],
            "proof_obligations": ["Realize the source theorem inside the witness family."],
            "candidate_lemmas": ["The witness family preserves the invariant."],
            "proof_outline": ["Build the witness family.", "Transport the invariant.", "Force the payoff."],
        },
        "status_assessment": {
            "evidence_count": 0,
            "novelty_argument": "This is currently a theorem-pair-specific research programme.",
        },
    }


def _base_macro_strategy() -> dict:
    return {
        "operationalizations": [
            {
                "object": "MCSP witness family",
                "carrier_kind": "family of instances equipped with a monotone witness measure",
            }
        ],
        "missing_for_completion": [
            {"kind": "route-lemma", "title": "Discharge the route lemma."}
        ],
        "completion_checklist": [
            {"status": "established", "title": "Grounding implication"},
            {"status": "open", "title": "Route lemma"},
        ],
    }


def test_plausibility_report_stays_false_while_completion_items_are_open() -> None:
    report = build_plausibility_report(
        kb_ref="demo",
        macro_state=_base_macro_state(),
        macro_strategy=_base_macro_strategy(),
        proof_summary={
            "metadata": {
                "proved_count": 0,
                "disproved_count": 0,
                "blocked_count": 0,
                "produced_paper_count": 0,
                "external_reference_count": 0,
            },
            "diagnosis_overview": {
                "queue": {
                    "count": 1,
                    "context_counts": {"well-posed": 0, "partially-ill-posed": 0, "ill-posed": 1},
                    "inference_counts": {"determined": 0, "underdetermined": 1, "difficult-but-well-posed": 0},
                    "common_blocking_defects": [{"text": "Queue entry is truncated.", "count": 1}],
                },
                "queue_historical": {
                    "count": 2,
                    "context_counts": {"well-posed": 0, "partially-ill-posed": 0, "ill-posed": 2},
                    "inference_counts": {"determined": 0, "underdetermined": 2, "difficult-but-well-posed": 0},
                    "common_blocking_defects": [{"text": "Historical queue entry is truncated.", "count": 2}],
                },
            },
        },
        mathlib={"results": []},
        attempts=[],
    )

    assert report["decision"]["plausible_solution_detected"] is False
    assert report["decision"]["decision"] in {"continue-no-terminal-proof", "continue-open-completion-items"}
    assert report["mandatory_gates"]["grounded_main_conjecture"] is True
    assert report["mandatory_gates"]["terminal_proved_attempt"] is False
    assert report["plausibility_score"] <= 0.35
    assert report["signals"]["score_caps"][0]["cap"] == 0.35
    assert report["diagnosis_overview"]["queue"]["context_counts"]["ill-posed"] == 1
    assert report["diagnosis_overview"]["queue_historical"]["count"] == 2


def test_plausibility_report_detects_plausible_solution_when_all_gates_clear() -> None:
    macro_state = _base_macro_state()
    macro_state["status_assessment"]["evidence_count"] = 2
    macro_strategy = {
        "operationalizations": [
            {
                "object": "MCSP witness family",
                "carrier_kind": "family of instances equipped with a monotone witness measure",
            }
        ],
        "missing_for_completion": [],
        "completion_checklist": [
            {"status": "established", "title": "Grounding implication"},
            {"status": "established", "title": "Route lemma"},
            {"status": "established", "title": "Payoff theorem"},
        ],
    }
    proof_summary = {
        "metadata": {
            "proved_count": 1,
            "disproved_count": 0,
            "blocked_count": 1,
            "produced_paper_count": 1,
            "external_reference_count": 1,
        }
    }
    attempts = [
        {
            "metadata": {"attempt_id": "attempt.demo.001"},
            "proof_attempt": {
                "stepwise_argument": [
                    {"claim": "Step 1", "justification": "Because source theorem.", "depends_on": ["st.src"]},
                    {"claim": "Step 2", "justification": "Because transport lemma.", "depends_on": ["lemma.transport"]},
                    {"claim": "Step 3", "justification": "Because payoff theorem.", "depends_on": ["lemma.payoff"]},
                ]
            },
            "final_assessment": {"outcome": "proved"},
            "critique_judges": [
                {"judge_id": "assumption-discipline", "title": "Assumption Discipline Judge", "verdict": "pass"},
                {"judge_id": "statement-grounding", "title": "Statement Grounding Judge", "verdict": "pass"},
                {"judge_id": "inferential-validity", "title": "Inferential Validity Judge", "verdict": "pass"},
                {"judge_id": "obstruction-and-negative-route", "title": "Obstruction And Negative-Route Judge", "verdict": "pass"},
                {"judge_id": "closure", "title": "Closure Judge", "verdict": "pass"},
            ],
            "web_search_gate": {"sources": [{"title": "Example source"}]},
            "external_references": [{"title": "Imported theorem"}],
        }
    ]
    mathlib = {
        "results": [
            {"result_id": "mathlib.demo.001", "outcome": "proved"},
            {"result_id": "mathlib.demo.002", "outcome": "blocked"},
            {"result_id": "mathlibref.demo.001", "outcome": "external_reference", "entry_kind": "external-reference"},
        ]
    }

    report = build_plausibility_report(
        kb_ref="demo",
        macro_state=macro_state,
        macro_strategy=macro_strategy,
        proof_summary=proof_summary,
        mathlib=mathlib,
        attempts=attempts,
    )

    assert report["decision"]["plausible_solution_detected"] is True
    assert report["decision"]["decision"] == "stop-plausible-solution"
    assert report["mandatory_gates"]["completion_checklist_clear"] is True
    assert report["mandatory_gates"]["terminal_proved_attempt"] is True
    assert report["plausibility_score"] >= 0.80
    assert report["diagnosis_overview"]["attempts"]["context_counts"]["ill-posed"] == 1
    assert report["diagnosis_overview"]["attempts"]["inference_counts"]["underdetermined"] == 1
    markdown = render_plausibility_markdown(report)
    assert "## Context Vs Inference Diagnosis" in markdown
    assert "### Attempts" in markdown
