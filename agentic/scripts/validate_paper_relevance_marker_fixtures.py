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
"""Regression fixtures for good-enough paper relevance markers."""

from __future__ import annotations

from agentic_common import fail
from build_scientific_contribution_monitor import good_enough_paper_relevance, paper_relevance_markers


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def gates(*, ready: bool) -> dict:
    return {
        key: {"ready": ready, "finite_task": True, "evidence": f"fixture {key}"}
        for key in [
            "claim_statement_ready",
            "evidence_ready",
            "novelty_boundary_ready",
            "validation_ready",
            "overclaim_boundary_ready",
        ]
    }


def marker_packet(text: str, *, novelty_status: str = "finite_check_queued", all_gates_ready: bool = False) -> tuple[list[dict], dict]:
    gate_packet = gates(ready=all_gates_ready)
    markers = paper_relevance_markers(
        target_id="p-vs-np-target",
        text=text,
        scores={
            "conceptual_novelty": 5,
            "explanatory_power": 5,
            "implications": 5,
            "certification_readiness": 5,
            "target_relevance": 5,
        },
        gates=gate_packet,
        prior={"novelty_status": novelty_status},
        disqualifiers=[
            {"name": "already_known", "verdict": "pass", "evidence": "fixture"},
            {"name": "advice_leakage", "verdict": "pass", "evidence": "fixture"},
        ],
        form={
            "form": "quantitative_transfer_obstruction",
            "audience": "complexity theorists",
            "novelty_axis": "exact beta and q threshold collapse",
            "decisive_validation": "derive the transfer inequality",
        },
    )
    return markers, good_enough_paper_relevance(markers, gate_packet)


def main() -> int:
    rich_text = (
        "The source carrier is an MCSP-style language and the target class is SAT against nonuniform circuit lower bounds. "
        "The exact transfer inequality exposes beta, q, and threshold collapse; because advice leakage and natural/algebrization "
        "barriers bind the route, the falsifier decides whether to pivot, backtrack, quarantine, or continue with a subpolynomial "
        "certificate bridge family under explicit assumptions."
    )
    markers, relevance = marker_packet(rich_text)
    by_dimension = {marker["dimension"]: marker for marker in markers}
    require(set(by_dimension) == {"conceptual_depth", "conceptual_novelty", "unblocking_power", "applicability", "understanding_gain"}, "missing marker dimensions")
    require(relevance["status"] == "strong_relevance_certification_pending", f"unexpected rich relevance status {relevance['status']}")
    require(by_dimension["conceptual_depth"]["score"] >= 4, "rich fixture should have conceptual depth")
    require(by_dimension["unblocking_power"]["score"] >= 4, "rich fixture should have unblocking power")
    require(by_dimension["understanding_gain"]["score"] >= 4, "rich fixture should have understanding gain")

    ready_markers, ready_relevance = marker_packet(rich_text, novelty_status="checked", all_gates_ready=True)
    require(ready_relevance["status"] == "paper_relevance_ready", f"ready fixture got {ready_relevance['status']}")
    require(all(marker["status"] in {"strong", "paper_ready"} for marker in ready_markers), "ready fixture should not have weak markers")

    vague_text = "This is promising progress toward P vs NP and should be explored more."
    vague_markers, vague_relevance = marker_packet(vague_text)
    require(vague_relevance["status"] in {"weak_relevance", "moderate_relevance_needs_sharpening"}, "vague fixture overpromoted")
    require(any(marker["status"] in {"weak", "adequate"} for marker in vague_markers), "vague fixture needs at least one non-strong marker")

    print("validated paper relevance marker fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
