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

"""Shared context-vs-inference diagnosis utilities for persisted artifacts."""

from __future__ import annotations

from collections import Counter
from typing import Any


CONTEXT_STATUSES = ("well-posed", "partially-ill-posed", "ill-posed")
INFERENCE_STATUSES = ("determined", "underdetermined", "difficult-but-well-posed")
CERTAINTY_LEVELS = ("very-low", "low", "medium", "high")
_CORE_WARNING_SNIPPETS = (
    "`source_excerpt`",
    "`target_excerpt`",
    "`missing_route_lemma`",
    "`route_synopsis`",
    "`proof_strategy_family`",
    "proof obligations or candidate lemmas",
    "source theorem is missing",
    "target theorem is missing",
)
_TERMINAL_OUTCOMES = {"proved", "disproved", "blocked", "prior_art_found"}


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _append_unique(rows: list[str], text: str) -> None:
    cleaned = _clean_text(text)
    if cleaned and cleaned not in rows:
        rows.append(cleaned)


def _is_core_warning(text: str) -> bool:
    lowered = _clean_text(text).lower()
    return any(snippet.lower() in lowered for snippet in _CORE_WARNING_SNIPPETS)


def _certainty_from_confidence(value: Any) -> str:
    lowered = _clean_text(value).lower()
    if lowered in CERTAINTY_LEVELS:
        return lowered
    if lowered in {"guarded-medium", "moderate"}:
        return "medium"
    if lowered in {"guarded-low", "tentative"}:
        return "low"
    return "medium"


def _minimal_repair_from_issues(issues: list[str], *, inference_status: str) -> str:
    for issue in issues:
        lowered = _clean_text(issue).lower()
        if "truncation markers" in lowered:
            return "Replace truncated theorem or route text with the full local statement."
        if "schema placeholders" in lowered:
            return "Replace schema placeholders with exact theorem names, regimes, and claim bodies."
        if "`candidate_object`" in lowered and ("generic" in lowered or "underspecified" in lowered):
            return "Give the bridge object a concrete local name and state its defining property."
        if "source theorem is missing" in lowered or "`source_excerpt` is empty" in lowered:
            return "Attach a local source theorem excerpt or a stable source statement identifier."
        if "target theorem is missing" in lowered or "`target_excerpt` is empty" in lowered:
            return "Attach a local target theorem excerpt or a stable target statement identifier."
        if "`missing_route_lemma` is empty" in lowered:
            return "Name the next missing route lemma explicitly."
        if "`route_synopsis` is empty" in lowered:
            return "Add one explicit route synopsis describing the bridge move."
        if "`proof_strategy_family` is empty" in lowered:
            return "Specify the intended proof strategy family before asking for the inference."
        if "proof obligations or candidate lemmas" in lowered:
            return "List at least one proof obligation or candidate lemma so the next step is explicit."
        if "pending critique judge" in lowered:
            return "Complete the critique judge verdicts before treating the route verdict as settled."
        if "result statement" in lowered or "result summary" in lowered:
            return "State the terminal result and its summary explicitly inside the attempt dossier."
    if inference_status == "determined":
        return "No packet repair is needed; the current state is explicit enough for audit."
    return "No packet repair is needed; the remaining uncertainty is mathematical rather than prompt-shaped."


def build_queue_inference_diagnosis(
    entry: dict[str, Any],
    *,
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    contract_dict = _ensure_dict(contract)
    blockers = [_clean_text(row) for row in _ensure_list(contract_dict.get("blockers")) if _clean_text(row)]
    warnings = [_clean_text(row) for row in _ensure_list(contract_dict.get("warnings")) if _clean_text(row)]
    strengths = [_clean_text(row) for row in _ensure_list(contract_dict.get("strengths")) if _clean_text(row)]
    if blockers:
        context_status = "ill-posed"
    elif any(_is_core_warning(row) for row in warnings):
        context_status = "partially-ill-posed"
    else:
        context_status = "well-posed"
    inference_status = "underdetermined" if context_status != "well-posed" else "difficult-but-well-posed"
    if context_status == "ill-posed":
        certainty_now = "very-low"
        certainty_if_well_posed = "medium" if len(strengths) >= 2 else "low"
        rationale = (
            "Current uncertainty is dominated by packet defects, so the route should be repaired before treating it as a mathematical proof target."
        )
    elif context_status == "partially-ill-posed":
        certainty_now = "low"
        certainty_if_well_posed = "medium"
        rationale = (
            "The route is partially grounded, but missing local restatements or next-step structure still make the inference underdetermined."
        )
    else:
        certainty_now = "medium" if len(strengths) >= 3 else "low"
        certainty_if_well_posed = certainty_now
        rationale = "The packet is explicit enough for proof work; the remaining uncertainty is the mathematical difficulty of the route itself."
    return {
        "context_status": context_status,
        "inference_status": inference_status,
        "blocking_defects": blockers[:4],
        "minimal_repair": _minimal_repair_from_issues(blockers or warnings, inference_status=inference_status),
        "certainty_now": certainty_now,
        "certainty_if_well_posed": certainty_if_well_posed,
        "rationale": rationale,
    }


def refresh_attempt_inference_diagnosis(attempt: dict[str, Any]) -> dict[str, Any]:
    target = _ensure_dict(attempt.get("target"))
    contract = _ensure_dict(target.get("interpretability_contract"))
    if not contract:
        from queue_entry_interpretability import assess_queue_entry_interpretability

        contract = assess_queue_entry_interpretability(target)
        if contract:
            target["interpretability_contract"] = contract
    if "inference_diagnosis" not in target and contract:
        target["inference_diagnosis"] = build_queue_inference_diagnosis(target, contract=contract)
    metadata = _ensure_dict(attempt.get("metadata"))
    local_context = _ensure_dict(attempt.get("local_context"))
    proof_attempt = _ensure_dict(attempt.get("proof_attempt"))
    final_assessment = _ensure_dict(attempt.get("final_assessment"))
    blockers = list(_ensure_list(_ensure_dict(contract).get("blockers")))
    warnings: list[str] = []

    has_stepwise_argument = any(
        isinstance(row, dict) and (_clean_text(row.get("claim")) or _clean_text(row.get("justification")))
        for row in _ensure_list(proof_attempt.get("stepwise_argument"))
    )
    if not _clean_text(proof_attempt.get("theorem_statement")) and not _clean_text(proof_attempt.get("result_statement")):
        if has_stepwise_argument:
            _append_unique(warnings, "The attempt dossier is missing an explicit theorem header, even though a stepwise argument is present.")
        else:
            _append_unique(blockers, "The attempt dossier is missing both a theorem statement and a terminal result statement.")
    if not _clean_text(local_context.get("source_excerpt")):
        _append_unique(warnings, "`local_context.source_excerpt` is empty, so the source premise is not restated inside the attempt.")
    if not _clean_text(local_context.get("target_excerpt")):
        _append_unique(warnings, "`local_context.target_excerpt` is empty, so the target theorem body is not restated inside the attempt.")

    outcome = (
        _clean_text(final_assessment.get("outcome")).lower()
        or _clean_text(metadata.get("status")).lower()
    )
    judges = [row for row in _ensure_list(attempt.get("critique_judges")) if isinstance(row, dict)]
    pending_judges = [
        _clean_text(row.get("judge_id")) or _clean_text(row.get("title"))
        for row in judges
        if _clean_text(row.get("verdict")).lower() in {"", "pending"}
    ]
    if outcome in _TERMINAL_OUTCOMES and pending_judges:
        _append_unique(
            warnings,
            f"Terminal outcome still has pending critique judge verdicts: {', '.join(pending_judges[:3])}.",
        )
    if outcome in _TERMINAL_OUTCOMES and not (
        _clean_text(proof_attempt.get("result_summary")) or _clean_text(final_assessment.get("summary"))
    ):
        _append_unique(warnings, "Terminal attempt is missing `proof_attempt.result_summary`.")

    if blockers:
        context_status = "ill-posed"
    elif any(_is_core_warning(row) for row in warnings):
        context_status = "partially-ill-posed"
    else:
        context_status = "well-posed"

    step_count = sum(
        1
        for row in _ensure_list(proof_attempt.get("stepwise_argument"))
        if isinstance(row, dict) and (_clean_text(row.get("claim")) or _clean_text(row.get("justification")))
    )
    terminal_determined = (
        outcome in _TERMINAL_OUTCOMES
        and bool(
            _clean_text(proof_attempt.get("result_statement"))
            or _clean_text(final_assessment.get("summary"))
            or step_count > 0
        )
    )

    if blockers:
        inference_status = "underdetermined"
    elif terminal_determined:
        inference_status = "determined"
    elif context_status != "well-posed":
        inference_status = "underdetermined"
    else:
        inference_status = "difficult-but-well-posed"

    if context_status == "ill-posed":
        certainty_now = "very-low"
        certainty_if_well_posed = "medium" if terminal_determined or step_count >= 2 else "low"
        rationale = (
            "The dossier still has context defects, so any route verdict should be treated mainly as packet diagnosis rather than stable mathematical evidence."
        )
    elif context_status == "partially-ill-posed":
        certainty_now = "low"
        certainty_if_well_posed = _certainty_from_confidence(final_assessment.get("confidence")) if terminal_determined else "medium"
        rationale = (
            "The route is materially specified, but missing local restatements or audit fields still weaken the current verdict."
        )
    elif inference_status == "determined":
        certainty_now = _certainty_from_confidence(final_assessment.get("confidence"))
        certainty_if_well_posed = certainty_now
        rationale = "The current dossier is explicit enough and already records a route verdict that can be audited locally."
    else:
        certainty_now = "medium" if step_count >= 2 else "low"
        certainty_if_well_posed = "medium"
        rationale = "The packet is explicit enough for proof work, but the remaining uncertainty is mathematical rather than prompt-shaped."

    diagnosis = {
        "context_status": context_status,
        "inference_status": inference_status,
        "blocking_defects": [_clean_text(row) for row in blockers[:4] if _clean_text(row)],
        "minimal_repair": _minimal_repair_from_issues(blockers or warnings, inference_status=inference_status),
        "certainty_now": certainty_now,
        "certainty_if_well_posed": certainty_if_well_posed,
        "rationale": rationale,
    }
    attempt["target"] = target
    attempt["inference_diagnosis"] = diagnosis
    return diagnosis


def summarize_inference_diagnoses(rows: list[dict[str, Any]]) -> dict[str, Any]:
    context_counts = {key: 0 for key in CONTEXT_STATUSES}
    inference_counts = {key: 0 for key in INFERENCE_STATUSES}
    defect_counter: Counter[str] = Counter()
    samples = {
        "ill_posed": [],
        "underdetermined": [],
        "difficult_but_well_posed": [],
        "determined": [],
    }
    count = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        diagnosis = _ensure_dict(row.get("inference_diagnosis"))
        if not diagnosis:
            diagnosis = _ensure_dict(_ensure_dict(row.get("interpretability_contract")).get("inference_diagnosis"))
        if not diagnosis:
            continue
        count += 1
        context_status = _clean_text(diagnosis.get("context_status"))
        inference_status = _clean_text(diagnosis.get("inference_status"))
        if context_status in context_counts:
            context_counts[context_status] += 1
        if inference_status in inference_counts:
            inference_counts[inference_status] += 1
        for defect in _ensure_list(diagnosis.get("blocking_defects")):
            cleaned = _clean_text(defect)
            if cleaned:
                defect_counter[cleaned] += 1
        subject_id = (
            _clean_text(row.get("queue_id"))
            or _clean_text(_ensure_dict(row.get("metadata")).get("attempt_id"))
            or _clean_text(row.get("result_id"))
            or _clean_text(row.get("title"))
        )
        if context_status == "ill-posed" and subject_id and len(samples["ill_posed"]) < 5:
            samples["ill_posed"].append(subject_id)
        if inference_status == "underdetermined" and subject_id and len(samples["underdetermined"]) < 5:
            samples["underdetermined"].append(subject_id)
        if inference_status == "difficult-but-well-posed" and subject_id and len(samples["difficult_but_well_posed"]) < 5:
            samples["difficult_but_well_posed"].append(subject_id)
        if inference_status == "determined" and subject_id and len(samples["determined"]) < 5:
            samples["determined"].append(subject_id)
    return {
        "count": count,
        "context_counts": context_counts,
        "inference_counts": inference_counts,
        "common_blocking_defects": [
            {"text": text, "count": count_value}
            for text, count_value in defect_counter.most_common(5)
        ],
        "sample_subjects": samples,
    }
