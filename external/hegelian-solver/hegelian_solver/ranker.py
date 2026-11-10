# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Candidate scoring and branching decisions.

Implements Phase 9 of the solver: hard gates first, then a transparent weighted score, then
one of five decisions (`accept`, `accept_as_branch`, `provisional`, `defer`, `reject`) that
lets multiple valid candidates branch the concept graph instead of forcing a single winner.

`score_candidate` blends two signals into one number in [0, 1]: `feature_score` (the mean
of the candidate's own `ranking_features`, domain-specific weights set in
`operators/library.py`) and `validation_score` (how many of its obligations passed/are
partial/failed, from `validators/core.py`). `rank_candidate` then applies
`packet.hard_gate_failures` as an absolute veto before the score is even consulted — a
candidate cannot buy its way past a failed hard gate with a high feature score.
"""

from __future__ import annotations

from hegelian_solver.schemas import RankingDecision, TransformationCandidate, ValidationPacket


POSITIVE_FEATURES = {
    "resolution",
    "preservation",
    "compression",
    "universality",
    "transfer",
    "invariance_gain",
    "novel_utility",
    "empirical_gain",
    "predecessor_recovery",
    "symmetry_gain",
    "predictive_novelty",
    "robustness",
    "failure_resolution",
    "capability_preservation",
    "source_grounding",
    "tool_correctness",
    "safety",
    "monitorability",
    "latency_cost_fit",
}

NEGATIVE_FEATURES = {
    "complexity",
    "loss",
    "overfit",
    "proof_burden",
    "ad_hocness",
    "unnecessary_ontology",
    "regime_confusion",
    "new_risk",
    "workflow_complexity",
    "maintenance_cost",
}


def score_candidate(candidate: TransformationCandidate, packet: ValidationPacket) -> tuple[float, dict[str, float]]:
    """Blend ranking features and obligation status into one score in [0, 1].

    `0.55` is a deliberate positive baseline (a candidate with neutral features and no
    failed obligations should land in `provisional`, not `reject`); the two signals are
    then weighted 0.35/0.45 so validation status matters slightly more than declared
    features. See `rank_candidate` for how the score maps to a decision.
    """

    features = candidate.ranking_features
    feature_score = 0.0
    for key, value in features.items():
        if key in NEGATIVE_FEATURES:
            feature_score -= value
        else:
            feature_score += value

    if features:
        feature_score = feature_score / max(len(features), 1)

    passed = sum(1 for obligation in packet.obligations if obligation.status == "passed")
    partial = sum(1 for obligation in packet.obligations if obligation.status == "partial")
    failed = sum(1 for obligation in packet.obligations if obligation.status == "failed")
    validation_score = (passed + 0.35 * partial - failed) / max(len(packet.obligations), 1)
    score = max(0.0, min(1.0, 0.55 + feature_score * 0.35 + validation_score * 0.45))
    return score, {"feature_score": feature_score, "validation_score": validation_score}


def rank_candidate(candidate: TransformationCandidate, packet: ValidationPacket) -> RankingDecision:
    """Decide one candidate's fate: hard gate failures always `reject`; otherwise the score
    plus whether any obligation is still `unknown`/`planned`/`partial` ("unknownish")
    decides between `accept` (score >= 0.7, nothing unknownish), `accept_as_branch`
    (score >= 0.6, nothing unknownish — a valid alternative, not necessarily the winner),
    `provisional` (score >= 0.55), or `defer`."""

    score, scores = score_candidate(candidate, packet)
    if packet.hard_gate_failures:
        decision = "reject"
        reasons = list(packet.hard_gate_failures)
    else:
        unknownish = [
            obligation
            for obligation in packet.obligations
            if obligation.status in {"unknown", "planned", "partial"}
        ]
        if not unknownish and score >= 0.7:
            decision = "accept"
            reasons = ["all obligations passed"]
        elif not unknownish and score >= 0.6:
            decision = "accept_as_branch"
            reasons = ["valid branch optimizing a distinct objective"]
        elif score >= 0.55:
            decision = "provisional"
            reasons = ["candidate has open obligations"]
        else:
            decision = "defer"
            reasons = ["needs stronger evidence or lower complexity"]

    gate_results = {
        obligation.kind: obligation.status for obligation in packet.obligations
    }
    return RankingDecision(
        candidate_id=candidate.id,
        decision=decision,
        score=round(score, 4),
        scores={key: round(value, 4) for key, value in scores.items()},
        gate_results=gate_results,
        reasons=reasons,
    )


def rank_candidates(
    candidates: list[TransformationCandidate], packets: list[ValidationPacket]
) -> list[RankingDecision]:
    """Rank every candidate that has a matching validation packet, best first
    (non-rejected before rejected, then by descending score).

    NOTE: a candidate with no matching packet is silently dropped rather than flagged — see
    TODO.md Phase 19.
    """

    packet_by_id = {packet.candidate_id: packet for packet in packets}
    decisions = [
        rank_candidate(candidate, packet_by_id[candidate.id])
        for candidate in candidates
        if candidate.id in packet_by_id
    ]
    return sorted(decisions, key=lambda item: (item.decision == "reject", -item.score, item.candidate_id))
