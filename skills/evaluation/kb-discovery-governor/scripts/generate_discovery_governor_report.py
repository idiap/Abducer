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

"""Deterministically govern discovery depth and promotion value from local artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from discovery_branch_queue import discovery_branch_paths
from discovery_branch_queue import load_discovery_branch_state
from discovery_branch_queue import save_discovery_branch_state
from kb_context import kb_ref_from_artifacts_dir
from proof_queue import load_proof_queue


REPORT_VERSION = 1
BRANCH_DECISION_ORDER = {
    "major_subresult_candidate": 0,
    "deepen": 1,
    "lateralize": 2,
    "freeze": 3,
}
PROMOTION_DECISION_ORDER = {
    "major_subresult_candidate": 0,
    "queue_for_proof": 1,
    "lateralize": 2,
    "freeze": 3,
}
PROMOTION_ALLOWED_DECISIONS = {"major_subresult_candidate", "queue_for_proof"}
MAJOR_SUBRESULT_SCORE_THRESHOLD = 11


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def discovery_governor_paths(artifacts_dir: Path) -> tuple[Path, Path]:
    return artifacts_dir / "discovery-governor-report.json", artifacts_dir / "discovery-governor-report.md"


def default_discovery_governor_report(*, kb_ref: str) -> dict[str, Any]:
    now = _utc_now()
    return {
        "metadata": {
            "kb_ref": _clean_text(kb_ref),
            "report_version": REPORT_VERSION,
            "generated_utc": now,
            "updated_utc": now,
            "branch_count": 0,
            "branch_freeze_count": 0,
            "branch_active_recommendation_count": 0,
            "branch_major_candidate_count": 0,
            "expert_package_count": 0,
            "promotion_ready_count": 0,
            "promotion_major_candidate_count": 0,
        },
        "branch_decisions": [],
        "expert_package_decisions": [],
        "summary": [],
    }


def load_discovery_governor_report(path: Path, *, kb_ref: str) -> dict[str, Any]:
    payload = _load_json(path)
    if not payload:
        return default_discovery_governor_report(kb_ref=kb_ref)
    payload.setdefault("metadata", {})
    payload.setdefault("branch_decisions", [])
    payload.setdefault("expert_package_decisions", [])
    payload.setdefault("summary", [])
    if not isinstance(payload["metadata"], dict):
        payload["metadata"] = {}
    if not isinstance(payload["branch_decisions"], list):
        payload["branch_decisions"] = []
    if not isinstance(payload["expert_package_decisions"], list):
        payload["expert_package_decisions"] = []
    if not isinstance(payload["summary"], list):
        payload["summary"] = []
    payload["metadata"]["kb_ref"] = _clean_text(payload["metadata"].get("kb_ref") or kb_ref)
    payload["metadata"]["report_version"] = REPORT_VERSION
    return payload


def _is_schematic(text: Any) -> bool:
    normalized = _clean_text(text).lower()
    if not normalized:
        return True
    bad_tokens = {
        "source theorem s",
        "target theorem t",
        "regime r",
        "carrier c",
        "invariant i",
        "object d",
        "unspecified",
    }
    return any(token in normalized for token in bad_tokens)


def _contains_truncation(text: Any) -> bool:
    normalized = _clean_text(text).lower()
    return "..." in normalized or "truncated" in normalized


def _theorem_shaped(text: Any) -> bool:
    normalized = _clean_text(text).lower()
    if not normalized or _is_schematic(normalized) or _contains_truncation(normalized):
        return False
    return any(marker in normalized for marker in ("for every", "there exists", "if ", "whenever", "no ", "every "))


def _score_band(value_score: float) -> str:
    if value_score >= 0.80:
        return "high-value"
    if value_score >= 0.65:
        return "valuable"
    if value_score >= 0.45:
        return "exploratory"
    return "low-value"


def _major_score_to_axis(score_0_to_4: int) -> int:
    if score_0_to_4 >= 4:
        return 3
    if score_0_to_4 >= 3:
        return 2
    if score_0_to_4 >= 2:
        return 1
    return 0


def _render_major_candidate_rationale(assessment: dict[str, Any]) -> str:
    if assessment.get("qualifies"):
        return _clean_text(
            f"Clears the major-subresult gate with score {assessment.get('score_total', 0)} and strong "
            f"{assessment.get('dominant_axis', 'frontier')} leverage."
        )
    failed = [
        label
        for label, passes in _ensure_dict(assessment.get("mandatory_gates")).items()
        if not bool(passes)
    ]
    if failed:
        return _clean_text(f"Fails mandatory gates: {', '.join(failed)}.")
    return _clean_text(
        f"Major-subresult score {assessment.get('score_total', 0)} remains below the threshold "
        f"{assessment.get('score_threshold', MAJOR_SUBRESULT_SCORE_THRESHOLD)}."
    )


def _major_subresult_assessment(
    *,
    self_contained_statement: bool,
    mathematical_inspectability: bool,
    nontrivial_frontier_relation: bool,
    independent_value: bool,
    frontier_shift: int,
    independence: int,
    transferability: int,
    barrier_clarity: int,
    proof_closure: int,
    search_compression: int,
) -> dict[str, Any]:
    gates = {
        "self_contained_statement": bool(self_contained_statement),
        "mathematical_inspectability": bool(mathematical_inspectability),
        "nontrivial_frontier_relation": bool(nontrivial_frontier_relation),
        "independent_value": bool(independent_value),
    }
    axes = {
        "frontier_shift": max(0, min(3, _safe_int(frontier_shift))),
        "independence": max(0, min(3, _safe_int(independence))),
        "transferability": max(0, min(3, _safe_int(transferability))),
        "barrier_clarity": max(0, min(3, _safe_int(barrier_clarity))),
        "proof_closure": max(0, min(3, _safe_int(proof_closure))),
        "search_compression": max(0, min(3, _safe_int(search_compression))),
    }
    score_total = sum(axes.values())
    gate_pass = all(gates.values())
    dominant_axis, dominant_axis_score = max(axes.items(), key=lambda item: (item[1], item[0]))
    key_axis_max = max(axes["frontier_shift"], axes["independence"], axes["barrier_clarity"])
    qualifies = gate_pass and score_total >= MAJOR_SUBRESULT_SCORE_THRESHOLD and key_axis_max >= 3
    assessment = {
        "mandatory_gates": gates,
        "axes": axes,
        "score_total": score_total,
        "score_threshold": MAJOR_SUBRESULT_SCORE_THRESHOLD,
        "gate_pass": gate_pass,
        "key_axis_max": key_axis_max,
        "qualifies": qualifies,
        "dominant_axis": dominant_axis if dominant_axis_score else "",
    }
    assessment["rationale"] = _render_major_candidate_rationale(assessment)
    return assessment


def _weighted_value_score(axes: dict[str, int]) -> float:
    normalized = {key: max(0.0, min(1.0, _safe_int(value) / 4.0)) for key, value in axes.items()}
    return round(
        0.16 * normalized.get("specificity", 0.0)
        + 0.18 * normalized.get("consequence_leverage", 0.0)
        + 0.16 * normalized.get("independent_subresult_potential", 0.0)
        + 0.12 * normalized.get("cross_route_leverage", 0.0)
        + 0.12 * normalized.get("falsifiability", 0.0)
        + 0.10 * normalized.get("barrier_exposure", 0.0)
        + 0.10 * normalized.get("search_space_compression", 0.0)
        + 0.06 * normalized.get("tractability", 0.0),
        3,
    )


def _major_type_index(breakthrough_profile: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for row in _ensure_list(breakthrough_profile.get("profiles")):
        if not isinstance(row, dict):
            continue
        obstruction = _clean_text(row.get("obstruction_class"))
        major_type = _clean_text(row.get("major_subresult_type"))
        if obstruction and major_type:
            mapping[obstruction] = major_type
    return mapping


def _package_index(expert_report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    agenda = _ensure_dict(expert_report.get("agenda"))
    for bucket in ("ready_for_prove", "ready_for_discovery"):
        for row in _ensure_list(agenda.get(bucket)):
            if not isinstance(row, dict):
                continue
            package_id = _clean_text(row.get("package_id"))
            if package_id:
                index[package_id] = row
    return index


def branch_decision_index(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        _clean_text(row.get("branch_id")): row
        for row in _ensure_list(report.get("branch_decisions"))
        if isinstance(row, dict) and _clean_text(row.get("branch_id"))
    }


def expert_package_decision_index(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        _clean_text(row.get("package_id")): row
        for row in _ensure_list(report.get("expert_package_decisions"))
        if isinstance(row, dict) and _clean_text(row.get("package_id"))
    }


def _revisit_penalty(attempt_count: int, summary: str) -> float:
    penalty = 0.0
    normalized = summary.lower()
    if attempt_count >= 2:
        penalty += 0.05
    if attempt_count >= 3:
        penalty += 0.03
    if attempt_count and normalized and not any(token in normalized for token in ("theorem", "promotable", "state delta", "concrete")):
        penalty += 0.04
    return round(min(0.20, penalty), 3)


def _branch_major_type(branch: dict[str, Any], major_type_by_obstruction: dict[str, str]) -> str:
    for obstruction in _ensure_list(branch.get("linked_obstruction_classes")):
        major_type = major_type_by_obstruction.get(_clean_text(obstruction))
        if major_type:
            return major_type
    return "exploratory-conjecture"


def _score_branch(branch: dict[str, Any], *, major_type_by_obstruction: dict[str, str]) -> dict[str, Any]:
    branch_id = _clean_text(branch.get("branch_id"))
    theorem_shape = _clean_text(branch.get("minimal_theorem_shape"))
    abstraction_required = _clean_text(branch.get("abstraction_required"))
    required_move = _clean_text(branch.get("required_move"))
    linked_queue_ids = [_clean_text(value) for value in _ensure_list(branch.get("linked_queue_ids")) if _clean_text(value)]
    linked_breakthrough_families = [_clean_text(value) for value in _ensure_list(branch.get("linked_breakthrough_families")) if _clean_text(value)]
    linked_obstruction_classes = [_clean_text(value) for value in _ensure_list(branch.get("linked_obstruction_classes")) if _clean_text(value)]
    required_questions = [_clean_text(value) for value in _ensure_list(branch.get("required_questions")) if _clean_text(value)]
    expected_deliverables = [_clean_text(value) for value in _ensure_list(branch.get("expected_deliverables")) if _clean_text(value)]
    anti_patterns = [_clean_text(value) for value in _ensure_list(branch.get("anti_patterns")) if _clean_text(value)]
    negative_outputs = [_clean_text(value) for value in _ensure_list(branch.get("negative_outputs")) if _clean_text(value)]
    sample_targets = [_clean_text(value) for value in _ensure_list(branch.get("sample_theorem_targets")) if _clean_text(value)]
    routing_priority = _safe_float(branch.get("routing_priority"))
    attempt_count = _safe_int(branch.get("attempt_count"))
    last_outcome_summary = _clean_text(branch.get("last_outcome_summary"))
    major_type = _branch_major_type(branch, major_type_by_obstruction)

    self_contained_statement = bool(theorem_shape) and not _is_schematic(theorem_shape) and not _contains_truncation(theorem_shape)
    typed_mechanism = bool(abstraction_required) and not _is_schematic(abstraction_required)
    frontier_context = bool(linked_queue_ids) or bool(_clean_text(branch.get("target_label")))
    positive_negative_tests = bool(required_questions) and bool(anti_patterns or negative_outputs)
    mathematical_inspectability = self_contained_statement and bool(required_questions or sample_targets)
    independent_value = major_type in {"standalone theorem", "barrier result", "transfer principle", "bridge object/tool"} and self_contained_statement

    specificity = 4 if self_contained_statement and typed_mechanism and frontier_context and expected_deliverables else 3 if self_contained_statement and typed_mechanism and frontier_context else 2 if self_contained_statement and frontier_context else 1 if theorem_shape or required_move else 0
    consequence_leverage = min(
        4,
        (1 if frontier_context else 0)
        + (1 if len(linked_queue_ids) >= 1 else 0)
        + (1 if len(linked_queue_ids) >= 3 or routing_priority >= 1.0 else 0)
        + (1 if major_type in {"standalone theorem", "barrier result", "transfer principle"} else 0),
    )
    independent_subresult_potential = {
        "research recommendation": 0,
        "exploratory-conjecture": 1,
        "bridge object/tool": 2,
        "transfer principle": 3,
        "standalone theorem": 4,
        "barrier result": 4,
    }.get(major_type, 1)
    if independent_value and independent_subresult_potential < 3:
        independent_subresult_potential = 3
    cross_route_surface = len(set(linked_queue_ids + linked_breakthrough_families + linked_obstruction_classes))
    cross_route_leverage = 4 if cross_route_surface >= 6 else 3 if cross_route_surface >= 4 else 2 if cross_route_surface >= 2 else 1 if cross_route_surface >= 1 else 0
    falsifiability = 4 if positive_negative_tests and negative_outputs else 3 if positive_negative_tests else 2 if anti_patterns or negative_outputs else 1 if required_questions else 0
    barrier_exposure = 4 if major_type == "barrier result" else 3 if any("barrier" in value.lower() or "pit" in value.lower() for value in linked_obstruction_classes + negative_outputs) else 2 if linked_obstruction_classes else 1 if anti_patterns else 0
    search_space_compression = 4 if len(linked_queue_ids) >= 6 or cross_route_surface >= 6 else 3 if len(linked_queue_ids) >= 3 or cross_route_surface >= 4 else 2 if len(linked_queue_ids) >= 2 else 1 if len(linked_queue_ids) == 1 else 0
    tractability = 4 if self_contained_statement and required_questions and expected_deliverables and sample_targets else 3 if self_contained_statement and required_questions and sample_targets else 2 if self_contained_statement and required_questions else 1 if theorem_shape or required_move else 0
    revisit_penalty = _revisit_penalty(attempt_count, last_outcome_summary)

    axes = {
        "specificity": specificity,
        "consequence_leverage": consequence_leverage,
        "independent_subresult_potential": independent_subresult_potential,
        "cross_route_leverage": cross_route_leverage,
        "falsifiability": falsifiability,
        "barrier_exposure": barrier_exposure,
        "search_space_compression": search_space_compression,
        "tractability": tractability,
    }
    raw_value_score = _weighted_value_score(axes)
    value_score = round(max(0.0, raw_value_score - revisit_penalty), 3)
    major_assessment = _major_subresult_assessment(
        self_contained_statement=self_contained_statement,
        mathematical_inspectability=mathematical_inspectability,
        nontrivial_frontier_relation=frontier_context and consequence_leverage >= 2,
        independent_value=independent_subresult_potential >= 3,
        frontier_shift=_major_score_to_axis(consequence_leverage),
        independence=_major_score_to_axis(independent_subresult_potential),
        transferability=_major_score_to_axis(cross_route_leverage),
        barrier_clarity=_major_score_to_axis(max(barrier_exposure, falsifiability)),
        proof_closure=_major_score_to_axis(tractability),
        search_compression=_major_score_to_axis(search_space_compression),
    )

    if not (self_contained_statement and typed_mechanism and frontier_context):
        decision = "freeze"
        rationale = "Freeze until the branch names a self-contained theorem packet, typed mechanism, and explicit frontier context."
    elif major_assessment.get("qualifies"):
        decision = "major_subresult_candidate"
        rationale = _clean_text(
            f"The branch already targets broader mathematics of type `{major_type}` and {major_assessment['rationale'].lower()}"
        )
    elif value_score >= 0.65:
        if cross_route_leverage >= 3 and tractability <= 2:
            decision = "lateralize"
            rationale = "Keep the branch live, but lateralize it until the theorem packet becomes more inspection-ready."
        else:
            decision = "deepen"
            rationale = "The branch is specific, consequential, and tractable enough to justify more local search depth."
    elif value_score >= 0.45 and (search_space_compression >= 3 or barrier_exposure >= 3):
        decision = "lateralize"
        rationale = "Retain the branch for breadth or barrier value, but do not let it dominate the active frontier."
    else:
        decision = "freeze"
        rationale = "Demote the branch because it is currently too low-value or too diffuse to justify active depth."

    return {
        "branch_id": branch_id,
        "target_label": _clean_text(branch.get("target_label")),
        "status_before_governor": _clean_text(branch.get("status")),
        "major_subresult_type": major_type,
        "linked_queue_count": len(linked_queue_ids),
        "attempt_count": attempt_count,
        "revisit_penalty": revisit_penalty,
        "mandatory_preconditions": {
            "self_contained_statement": self_contained_statement,
            "typed_mechanism": typed_mechanism,
            "frontier_context": frontier_context,
            "positive_negative_test_path": positive_negative_tests,
        },
        "value_axes": axes,
        "value_score": value_score,
        "value_band": _score_band(value_score),
        "major_subresult_assessment": major_assessment,
        "decision": decision,
        "rationale": _clean_text(rationale),
    }


def _score_package(
    package: dict[str, Any],
    *,
    branch_decisions: dict[str, dict[str, Any]],
    major_type_by_obstruction: dict[str, str],
) -> dict[str, Any]:
    package_id = _clean_text(package.get("package_id"))
    branch_id = _clean_text(package.get("branch_id"))
    exact_statement = _clean_text(package.get("exact_statement"))
    target_excerpt = _clean_text(package.get("target_excerpt"))
    bridge_object = _ensure_dict(package.get("bridge_object"))
    lemma = _ensure_dict(package.get("first_nontrivial_lemma"))
    linked_queue_ids = [_clean_text(value) for value in _ensure_list(package.get("linked_queue_ids")) if _clean_text(value)]
    linked_bridge_ids = [_clean_text(value) for value in _ensure_list(package.get("linked_bridge_ids")) if _clean_text(value)]
    admissibility_conditions = [_clean_text(value) for value in _ensure_list(package.get("admissibility_conditions")) if _clean_text(value)]
    negative_barrier_version = _clean_text(package.get("negative_barrier_version"))
    independent_value_claim = _clean_text(package.get("independent_value_claim"))
    regime = _ensure_dict(package.get("regime_and_quantifiers"))
    expert_gate = _ensure_dict(package.get("expert_gate"))

    branch_major_type = _clean_text(_ensure_dict(branch_decisions.get(branch_id)).get("major_subresult_type"))
    if not branch_major_type:
        branch_major_type = _branch_major_type({"linked_obstruction_classes": []}, major_type_by_obstruction)
    self_contained_statement = bool(exact_statement) and not _is_schematic(exact_statement) and not _contains_truncation(exact_statement)
    typed_mechanism = bool(_clean_text(bridge_object.get("name"))) and (
        bool(_clean_text(bridge_object.get("definition"))) or bool(_clean_text(bridge_object.get("invariant")))
    )
    frontier_context = bool(target_excerpt) and bool(_clean_text(package.get("target_statement_id")))
    positive_negative_tests = _theorem_shaped(lemma.get("statement")) and bool(negative_barrier_version)
    mathematical_inspectability = self_contained_statement and _theorem_shaped(lemma.get("statement"))

    specificity = 4 if self_contained_statement and typed_mechanism and admissibility_conditions and regime else 3 if self_contained_statement and typed_mechanism and frontier_context else 2 if self_contained_statement and frontier_context else 1 if exact_statement else 0
    consequence_leverage = min(
        4,
        (1 if frontier_context else 0)
        + (1 if len(linked_queue_ids) >= 1 else 0)
        + (1 if len(linked_queue_ids) >= 2 or len(linked_bridge_ids) >= 2 else 0)
        + (1 if branch_major_type in {"standalone theorem", "barrier result", "transfer principle"} else 0),
    )
    independent_subresult_potential = 4 if independent_value_claim and branch_major_type in {"standalone theorem", "barrier result", "transfer principle"} else 3 if independent_value_claim else 1
    cross_route_surface = len(set(linked_queue_ids + linked_bridge_ids))
    cross_route_leverage = 4 if cross_route_surface >= 5 else 3 if cross_route_surface >= 3 else 2 if cross_route_surface >= 2 else 1 if cross_route_surface == 1 else 0
    falsifiability = 4 if positive_negative_tests else 3 if negative_barrier_version else 1 if _theorem_shaped(lemma.get("statement")) else 0
    barrier_exposure = 4 if branch_major_type == "barrier result" and negative_barrier_version else 3 if negative_barrier_version else 1 if branch_major_type == "transfer principle" else 0
    search_space_compression = 4 if len(linked_queue_ids) >= 4 or len(linked_bridge_ids) >= 4 else 3 if len(linked_queue_ids) >= 2 or len(linked_bridge_ids) >= 3 else 2 if len(linked_queue_ids) >= 1 else 0
    tractability = 4 if mathematical_inspectability and admissibility_conditions and bool(expert_gate.get("passes")) else 3 if mathematical_inspectability and bool(expert_gate.get("passes")) else 2 if mathematical_inspectability else 1 if exact_statement else 0
    axes = {
        "specificity": specificity,
        "consequence_leverage": consequence_leverage,
        "independent_subresult_potential": independent_subresult_potential,
        "cross_route_leverage": cross_route_leverage,
        "falsifiability": falsifiability,
        "barrier_exposure": barrier_exposure,
        "search_space_compression": search_space_compression,
        "tractability": tractability,
    }
    value_score = _weighted_value_score(axes)
    major_assessment = _major_subresult_assessment(
        self_contained_statement=self_contained_statement,
        mathematical_inspectability=mathematical_inspectability,
        nontrivial_frontier_relation=frontier_context and consequence_leverage >= 2,
        independent_value=bool(independent_value_claim),
        frontier_shift=_major_score_to_axis(consequence_leverage),
        independence=_major_score_to_axis(independent_subresult_potential),
        transferability=_major_score_to_axis(cross_route_leverage),
        barrier_clarity=_major_score_to_axis(max(falsifiability, barrier_exposure)),
        proof_closure=_major_score_to_axis(tractability),
        search_compression=_major_score_to_axis(search_space_compression),
    )

    if not bool(expert_gate.get("passes")) or not (self_contained_statement and typed_mechanism and frontier_context and positive_negative_tests):
        decision = "freeze"
        rationale = "Do not promote the package yet; it is still too weak or incomplete as a broader mathematical target."
    elif major_assessment.get("qualifies"):
        decision = "major_subresult_candidate"
        rationale = _clean_text(
            f"The package is strong enough to count as a major intermediate result and {major_assessment['rationale'].lower()}"
        )
    elif value_score >= 0.65:
        decision = "queue_for_proof"
        rationale = "Promote this package to prove; it is concrete, consequential, and inspectable enough to justify theorem-level proof work."
    elif value_score >= 0.45 and (cross_route_leverage >= 3 or barrier_exposure >= 3):
        decision = "lateralize"
        rationale = "Keep the package visible for broader relevance, but do not spend a proof slot on it yet."
    else:
        decision = "freeze"
        rationale = "Do not promote the package; it is currently elegant but inert relative to the active programme."

    return {
        "package_id": package_id,
        "branch_id": branch_id,
        "title": _clean_text(package.get("title")),
        "major_subresult_type": branch_major_type,
        "linked_queue_count": len(linked_queue_ids),
        "linked_bridge_count": len(linked_bridge_ids),
        "mandatory_preconditions": {
            "self_contained_statement": self_contained_statement,
            "typed_mechanism": typed_mechanism,
            "frontier_context": frontier_context,
            "positive_negative_test_path": positive_negative_tests,
        },
        "value_axes": axes,
        "value_score": value_score,
        "value_band": _score_band(value_score),
        "major_subresult_assessment": major_assessment,
        "decision": decision,
        "rationale": _clean_text(rationale),
    }


def build_report(*, artifacts_dir: Path, kb_ref: str, activate_top_k: int = 4) -> dict[str, Any]:
    branch_json, _ = discovery_branch_paths(artifacts_dir)
    branch_state = load_discovery_branch_state(branch_json, kb_ref=kb_ref)
    proof_queue = load_proof_queue(artifacts_dir / "proof-queue.json", kb_ref=kb_ref)
    breakthrough_profile = _load_json(artifacts_dir / "discovery-breakthrough-profile.json")
    expert_report = _load_json(artifacts_dir / "expert-conjectures.json")
    major_type_by_obstruction = _major_type_index(breakthrough_profile)

    branch_rows = [row for row in _ensure_list(branch_state.get("branches")) if isinstance(row, dict)]
    branch_decisions = [_score_branch(row, major_type_by_obstruction=major_type_by_obstruction) for row in branch_rows]
    branch_decisions.sort(
        key=lambda row: (
            BRANCH_DECISION_ORDER.get(_clean_text(row.get("decision")), 99),
            -_safe_float(row.get("value_score")),
            -_safe_float(_ensure_dict(row.get("major_subresult_assessment")).get("score_total")),
            _clean_text(row.get("branch_id")),
        )
    )
    for rank, row in enumerate(branch_decisions, start=1):
        row["governor_rank"] = rank
        row["recommended_status"] = "deprioritized" if row["decision"] == "freeze" else ("active" if rank <= max(1, activate_top_k) else "pending")

    branch_index = {row["branch_id"]: row for row in branch_decisions if _clean_text(row.get("branch_id"))}
    package_rows = [row for row in _package_index(expert_report).values() if isinstance(row, dict)]
    package_decisions = [
        _score_package(row, branch_decisions=branch_index, major_type_by_obstruction=major_type_by_obstruction)
        for row in package_rows
    ]
    package_decisions.sort(
        key=lambda row: (
            PROMOTION_DECISION_ORDER.get(_clean_text(row.get("decision")), 99),
            -_safe_float(row.get("value_score")),
            -_safe_float(_ensure_dict(row.get("major_subresult_assessment")).get("score_total")),
            _clean_text(row.get("package_id")),
        )
    )

    report = default_discovery_governor_report(kb_ref=kb_ref)
    meta = report["metadata"]
    meta["generated_utc"] = _utc_now()
    meta["updated_utc"] = meta["generated_utc"]
    meta["branch_count"] = len(branch_decisions)
    meta["branch_freeze_count"] = sum(1 for row in branch_decisions if row.get("decision") == "freeze")
    meta["branch_active_recommendation_count"] = sum(1 for row in branch_decisions if row.get("recommended_status") == "active")
    meta["branch_major_candidate_count"] = sum(1 for row in branch_decisions if _ensure_dict(row.get("major_subresult_assessment")).get("qualifies"))
    meta["expert_package_count"] = len(package_decisions)
    meta["promotion_ready_count"] = sum(1 for row in package_decisions if row.get("decision") in PROMOTION_ALLOWED_DECISIONS)
    meta["promotion_major_candidate_count"] = sum(1 for row in package_decisions if row.get("decision") == "major_subresult_candidate")
    meta["proof_queue_pending_count"] = int(_ensure_dict(proof_queue.get("metadata")).get("pending_count", 0) or 0)
    report["branch_decisions"] = branch_decisions
    report["expert_package_decisions"] = package_decisions
    report["summary"] = [
        _clean_text(
            f"The governor reviewed {meta['branch_count']} discovery branches and recommends {meta['branch_active_recommendation_count']} active branches,"
            f" freezing {meta['branch_freeze_count']} low-value or under-specified routes."
        ),
        _clean_text(
            f"{meta['branch_major_candidate_count']} branch-level routes and {meta['promotion_major_candidate_count']} expert packages currently qualify"
            " as major-subresult candidates under the deterministic gate."
        ),
        _clean_text(
            f"{meta['promotion_ready_count']} expert packages are worth proof-queue promotion under the current broader-relevance policy."
        ),
    ]
    return report


def apply_governor_to_branch_state(
    state: dict[str, Any],
    *,
    report: dict[str, Any],
    activate_top_k: int,
) -> dict[str, Any]:
    branch_by_id = branch_decision_index(report)
    candidates: list[dict[str, Any]] = []
    for row in _ensure_list(state.get("branches")):
        if not isinstance(row, dict):
            continue
        branch_id = _clean_text(row.get("branch_id"))
        decision = _ensure_dict(branch_by_id.get(branch_id))
        if not decision:
            continue
        row["governor_decision"] = _clean_text(decision.get("decision"))
        row["governor_rationale"] = _clean_text(decision.get("rationale"))
        row["governor_value_score"] = _safe_float(decision.get("value_score"))
        row["governor_value_band"] = _clean_text(decision.get("value_band"))
        row["governor_rank"] = _safe_int(decision.get("governor_rank"))
        row["governor_major_candidate"] = bool(_ensure_dict(decision.get("major_subresult_assessment")).get("qualifies"))
        row["governor_major_score"] = _safe_int(_ensure_dict(decision.get("major_subresult_assessment")).get("score_total"))
        row["governor_major_type"] = _clean_text(decision.get("major_subresult_type"))
        row["governor_revisit_penalty"] = _safe_float(decision.get("revisit_penalty"))
        status = _clean_text(row.get("status")).lower()
        if status == "blocked":
            continue
        if row["governor_decision"] == "freeze":
            row["status"] = "deprioritized"
            row["activation_reason"] = _clean_text(
                f"Discovery governor froze this branch: {row['governor_rationale']}"
            )
            row["updated_utc"] = _utc_now()
            continue
        candidates.append(row)

    candidates.sort(
        key=lambda row: (
            BRANCH_DECISION_ORDER.get(_clean_text(row.get("governor_decision")), 99),
            -_safe_float(row.get("governor_value_score")),
            -_safe_float(row.get("governor_major_score")),
            -_safe_float(row.get("routing_priority")),
            _clean_text(row.get("branch_id")),
        )
    )
    for index, row in enumerate(candidates, start=1):
        row["status"] = "active" if index <= max(1, activate_top_k) else "pending"
        if row["status"] == "active":
            row["activation_reason"] = _clean_text(
                f"Selected by discovery governor as an active {row.get('governor_decision', 'discovery')} branch."
            )
        else:
            row["activation_reason"] = _clean_text(
                "Kept pending by discovery governor while higher-value branches stay active."
            )
        row["updated_utc"] = _utc_now()
    return state


def render_markdown(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    branch_rows = [row for row in _ensure_list(report.get("branch_decisions")) if isinstance(row, dict)]
    package_rows = [row for row in _ensure_list(report.get("expert_package_decisions")) if isinstance(row, dict)]
    lines = [
        "# Discovery Governor Report",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Updated (UTC): {meta.get('updated_utc', '')}",
        f"- Branches reviewed: {meta.get('branch_count', 0)}",
        f"- Active recommendations: {meta.get('branch_active_recommendation_count', 0)}",
        f"- Frozen branches: {meta.get('branch_freeze_count', 0)}",
        f"- Branch major-subresult candidates: {meta.get('branch_major_candidate_count', 0)}",
        f"- Expert packages reviewed: {meta.get('expert_package_count', 0)}",
        f"- Promotion-ready packages: {meta.get('promotion_ready_count', 0)}",
        f"- Promotion major-subresult candidates: {meta.get('promotion_major_candidate_count', 0)}",
        "",
        "## Summary",
        "",
    ]
    if _ensure_list(report.get("summary")):
        for row in _ensure_list(report.get("summary")):
            lines.append(f"- {_clean_text(row)}")
    else:
        lines.append("- No discovery-governor summary is available.")
    lines.extend(["", "## Branch Decisions", ""])
    if not branch_rows:
        lines.append("- No discovery branches were available.")
    for row in branch_rows:
        major = _ensure_dict(row.get("major_subresult_assessment"))
        lines.extend(
            [
                f"### {row.get('branch_id', '')}",
                "",
                f"- Decision: {row.get('decision', '')}",
                f"- Recommended status: {row.get('recommended_status', '')}",
                f"- Value score: {row.get('value_score', 0):.3f} ({row.get('value_band', '')})",
                f"- Major-subresult type: {row.get('major_subresult_type', '')}",
                f"- Major score: {major.get('score_total', 0)}",
                f"- Major candidate: {bool(major.get('qualifies'))}",
                f"- Rationale: {row.get('rationale', '')}",
                "",
            ]
        )
    lines.extend(["## Expert Package Decisions", ""])
    if not package_rows:
        lines.append("- No expert packages were available.")
    for row in package_rows:
        major = _ensure_dict(row.get("major_subresult_assessment"))
        lines.extend(
            [
                f"### {row.get('package_id', '')}",
                "",
                f"- Title: {row.get('title', '')}",
                f"- Decision: {row.get('decision', '')}",
                f"- Value score: {row.get('value_score', 0):.3f} ({row.get('value_band', '')})",
                f"- Major-subresult type: {row.get('major_subresult_type', '')}",
                f"- Major score: {major.get('score_total', 0)}",
                f"- Major candidate: {bool(major.get('qualifies'))}",
                f"- Rationale: {row.get('rationale', '')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def write_report(report: dict[str, Any], *, output_json: Path, output_md: Path) -> None:
    meta = _ensure_dict(report.get("metadata"))
    meta["report_version"] = REPORT_VERSION
    meta["updated_utc"] = _utc_now()
    report["metadata"] = meta
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic discovery-governor report.")
    parser.add_argument("--artifacts-dir", required=True, help="Problem artifact directory.")
    parser.add_argument("--kb-ref", default="", help="Problem reference. Defaults from artifacts dir.")
    parser.add_argument("--top-k", type=int, default=4, help="Number of discovery branches to recommend as active.")
    parser.add_argument(
        "--apply-to-branch-queue",
        action="store_true",
        help="Also rewrite discovery-branch-queue.* with the governor decision applied.",
    )
    args = parser.parse_args()

    artifacts_dir = Path(args.artifacts_dir).resolve()
    kb_ref = _clean_text(args.kb_ref) or kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("Could not infer kb_ref from artifacts dir; pass --kb-ref explicitly.")

    report = build_report(artifacts_dir=artifacts_dir, kb_ref=kb_ref, activate_top_k=max(1, args.top_k))
    output_json, output_md = discovery_governor_paths(artifacts_dir)
    write_report(report, output_json=output_json, output_md=output_md)
    if args.apply_to_branch_queue:
        branch_json, branch_md = discovery_branch_paths(artifacts_dir)
        branch_state = load_discovery_branch_state(branch_json, kb_ref=kb_ref)
        apply_governor_to_branch_state(branch_state, report=report, activate_top_k=max(1, args.top_k))
        save_discovery_branch_state(branch_state, json_path=branch_json, md_path=branch_md)
    print(f"[OK] Wrote discovery governor report: {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
