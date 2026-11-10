# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Human-readable dialectical explanations."""

from __future__ import annotations

from hegelian_solver.schemas import ConceptNode, RankingDecision, TransformationCandidate, ValidationPacket


def explain_transition(
    source: ConceptNode,
    candidate: TransformationCandidate,
    packet: ValidationPacket,
    decision: RankingDecision,
    detailed: bool = False,
) -> str:
    status = "verified Aufhebung" if decision.decision == "accept" else "candidate repair"
    preserved = candidate.preservation_map.get("kind", "preservation map")
    residual = "; ".join(candidate.residual_limits) or "no residual limits declared"
    open_obligations = [
        obligation.kind for obligation in packet.obligations if obligation.status != "passed"
    ]
    base = (
        f"{source.name} develops through {candidate.operator} into "
        f"{candidate.target_concept.get('name')} as a {status}. "
        f"The trigger is treated as a determinate limit because {candidate.resolution_mechanism}. "
        f"Preservation is mediated by {preserved}, while resolution is checked by "
        f"{len(packet.obligations)} obligations. Residual limits: {residual}."
    )
    if detailed:
        base += (
            f" Decision: {decision.decision} with score {decision.score}. "
            f"Open obligations: {', '.join(open_obligations) if open_obligations else 'none'}."
        )
    return base


def explain_run(source: ConceptNode, candidates: list[TransformationCandidate], packets, decisions) -> str:
    packet_by_id = {packet.candidate_id: packet for packet in packets}
    decision_by_id = {decision.candidate_id: decision for decision in decisions}
    accepted = [
        candidate
        for candidate in candidates
        if decision_by_id.get(candidate.id)
        and decision_by_id[candidate.id].decision in {"accept", "accept_as_branch", "provisional"}
    ]
    if not accepted:
        return f"{source.name} produced no accepted successor; inspect rejected candidates and open obligations."
    candidate = accepted[0]
    return explain_transition(
        source,
        candidate,
        packet_by_id[candidate.id],
        decision_by_id[candidate.id],
        detailed=True,
    )
