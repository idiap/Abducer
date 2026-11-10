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

"""Shared end-to-end proof plausibility assessment utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from inference_diagnosis import refresh_attempt_inference_diagnosis
from inference_diagnosis import summarize_inference_diagnoses
from kb_context import kb_ref_from_artifacts_dir
from problem_mathlib import load_mathlib_index
from problem_mathlib import mathlib_paths


CRITIC_ORDER = (
    "main-claim-closure",
    "dependency-closure",
    "assumption-discipline",
    "bridge-realism",
    "adversarial-pressure",
    "proof-granularity",
    "end-to-end-consistency",
    "novelty-discipline",
)


def _load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk, defaulting to an empty mapping on failure."""
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _ensure_dict(value: Any) -> dict[str, Any]:
    """Normalize an arbitrary value into a dictionary-shaped object."""
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    """Normalize an arbitrary value into a list-shaped object."""
    return value if isinstance(value, list) else []


def _clean_text(value: Any) -> str:
    """Collapse text-like values into a single normalized line for scoring logic."""
    return " ".join(str(value or "").strip().split())


def _safe_int(value: Any, default: int = 0) -> int:
    """Parse an integer-like value while preserving a safe fallback."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _boolish_pass(value: Any) -> bool:
    """Interpret stored judge verdict tokens as a passing audit outcome."""
    return _clean_text(value).lower() in {"pass", "passed", "ok", "approved", "true", "yes"}


def _count_status(rows: list[dict[str, Any]], *wanted: str) -> int:
    """Count how many records carry one of the requested normalized statuses."""
    wanted_s = {item.strip().lower() for item in wanted if item.strip()}
    return sum(1 for row in rows if _clean_text(row.get("status")).lower() in wanted_s)


def load_attempts(attempt_dir: Path) -> list[dict[str, Any]]:
    """Load and sort persisted proof attempts from newest to oldest."""
    attempts: list[dict[str, Any]] = []
    if not attempt_dir.exists():
        return attempts
    for path in sorted(attempt_dir.glob("*.json")):
        payload = _load_json(path)
        if not payload:
            continue
        refresh_attempt_inference_diagnosis(payload)
        payload["_artifact_path"] = str(path)
        attempts.append(payload)
    attempts.sort(
        key=lambda row: (
            _clean_text(_ensure_dict(row.get("metadata")).get("updated_utc"))
            or _clean_text(_ensure_dict(row.get("metadata")).get("started_utc")),
            _clean_text(_ensure_dict(row.get("metadata")).get("attempt_id")),
        ),
        reverse=True,
    )
    return attempts


def load_plausibility_inputs(repo_root: Path, artifacts_dir: Path) -> dict[str, Any]:
    """Collect the artifact set required for end-to-end plausibility scoring."""
    kb_ref = kb_ref_from_artifacts_dir(artifacts_dir)
    mathlib_json, _ = mathlib_paths(repo_root, kb_ref)
    return {
        "kb_ref": kb_ref,
        "macro_state": _load_json(artifacts_dir / "macro-proof-state.json"),
        "macro_strategy": _load_json(artifacts_dir / "macro-strategy-report.json"),
        "proof_summary": _load_json(artifacts_dir / "proof-cycle-summary.json"),
        "mathlib": load_mathlib_index(mathlib_json, kb_ref=kb_ref),
        "attempts": load_attempts(artifacts_dir / "proof-attempts"),
    }


def _judge_records(attempt: dict[str, Any], token: str) -> list[dict[str, Any]]:
    """Return critique-judge records whose title or id matches the requested token."""
    out: list[dict[str, Any]] = []
    token_s = token.lower()
    for row in _ensure_list(attempt.get("critique_judges")):
        if not isinstance(row, dict):
            continue
        title = _clean_text(row.get("title")).lower()
        judge_id = _clean_text(row.get("judge_id")).lower()
        if token_s in title or token_s in judge_id:
            out.append(row)
    return out


def _latest_terminal_attempts(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Filter proof attempts down to terminal outcomes relevant to plausibility."""
    out = []
    for attempt in attempts:
        outcome = _clean_text(_ensure_dict(attempt.get("final_assessment")).get("outcome")).lower()
        if outcome in {"proved", "disproved", "prior_art_found", "blocked"}:
            out.append(attempt)
    return out


def _latest_proved_attempts(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Filter proof attempts down to those that currently claim a proved result."""
    out = []
    for attempt in attempts:
        outcome = _clean_text(_ensure_dict(attempt.get("final_assessment")).get("outcome")).lower()
        if outcome == "proved":
            out.append(attempt)
    return out


def _terminal_judge_failure_count(attempts: list[dict[str, Any]]) -> int:
    """Count non-passing critique verdicts across terminal proof attempts."""
    count = 0
    for attempt in attempts:
        for judge in _ensure_list(attempt.get("critique_judges")):
            if not isinstance(judge, dict):
                continue
            verdict = _clean_text(judge.get("verdict")).lower()
            if verdict and verdict not in {"pass", "passed", "ok", "approved"}:
                count += 1
    return count


def _all_target_judges_pass(attempts: list[dict[str, Any]], token: str) -> bool:
    """Check whether every matching judge across terminal attempts reports a pass."""
    hits = 0
    for attempt in attempts:
        records = _judge_records(attempt, token)
        if not records:
            continue
        hits += len(records)
        if not all(_boolish_pass(row.get("verdict")) for row in records):
            return False
    return hits > 0


def _step_count(attempt: dict[str, Any]) -> int:
    """Count nonempty proof steps in one attempt's stepwise informal argument."""
    proof_attempt = _ensure_dict(attempt.get("proof_attempt"))
    count = 0
    for row in _ensure_list(proof_attempt.get("stepwise_argument")):
        if not isinstance(row, dict):
            continue
        if _clean_text(row.get("claim")) or _clean_text(row.get("justification")):
            count += 1
    return count


def build_plausibility_report(
    *,
    kb_ref: str,
    macro_state: dict[str, Any],
    macro_strategy: dict[str, Any],
    proof_summary: dict[str, Any],
    mathlib: dict[str, Any],
    attempts: list[dict[str, Any]],
) -> dict[str, Any]:
    """Score whether the current artifact chain plausibly closes the main proof route."""
    normalized_attempts: list[dict[str, Any]] = []
    for row in attempts:
        if not isinstance(row, dict):
            continue
        refresh_attempt_inference_diagnosis(row)
        normalized_attempts.append(row)
    attempts = normalized_attempts
    macro_main = _ensure_dict(macro_state.get("main_conjecture"))
    macro_leading = _ensure_dict(macro_state.get("leading_route"))
    macro_status = _ensure_dict(macro_state.get("status_assessment"))
    strategy_missing = [row for row in _ensure_list(macro_strategy.get("missing_for_completion")) if isinstance(row, dict)]
    strategy_checklist = [row for row in _ensure_list(macro_strategy.get("completion_checklist")) if isinstance(row, dict)]
    operationalizations = [row for row in _ensure_list(macro_strategy.get("operationalizations")) if isinstance(row, dict)]
    summary_meta = _ensure_dict(proof_summary.get("metadata"))
    mathlib_results = [row for row in _ensure_list(mathlib.get("results")) if isinstance(row, dict)]
    terminal_attempts = _latest_terminal_attempts(attempts)
    proved_attempts = _latest_proved_attempts(attempts)
    latest_proved = proved_attempts[0] if proved_attempts else {}
    summary_diagnosis = _ensure_dict(proof_summary.get("diagnosis_overview"))
    diagnosis_overview = {
        "queue_active": _ensure_dict(summary_diagnosis.get("queue_active")),
        "queue": _ensure_dict(summary_diagnosis.get("queue")),
        "queue_historical": _ensure_dict(summary_diagnosis.get("queue_historical")),
        "attempts_active": _ensure_dict(summary_diagnosis.get("attempts_active")) or summarize_inference_diagnoses(
            [
                row
                for row in attempts
                if _clean_text(_ensure_dict(row.get("metadata")).get("status")).lower() == "in_progress"
                or _clean_text(_ensure_dict(row.get("final_assessment")).get("outcome")).lower() == "in_progress"
            ]
        ),
        "attempts": _ensure_dict(summary_diagnosis.get("attempts")) or summarize_inference_diagnoses(attempts),
        "attempts_historical": _ensure_dict(summary_diagnosis.get("attempts_historical")),
    }

    open_count = _count_status(strategy_checklist, "open")
    partial_count = _count_status(strategy_checklist, "partial")
    established_count = _count_status(strategy_checklist, "established")
    evidence_count = _safe_int(macro_status.get("evidence_count"))
    proved_count = _safe_int(summary_meta.get("proved_count"))
    disproved_count = _safe_int(summary_meta.get("disproved_count"))
    blocked_count = _safe_int(summary_meta.get("blocked_count"))
    produced_paper_count = _safe_int(summary_meta.get("produced_paper_count"))
    external_reference_count = _safe_int(summary_meta.get("external_reference_count"))
    prior_art_count = sum(1 for row in mathlib_results if _clean_text(row.get("outcome")).lower() == "prior_art_found")
    route_consistency_note = _clean_text(macro_leading.get("route_consistency_note"))
    negative_route = _clean_text(macro_leading.get("negative_route"))
    failure_diagnosis = _clean_text(macro_leading.get("failure_diagnosis"))
    mathematical_assumptions = [
        _clean_text(item)
        for item in _ensure_list(macro_leading.get("mathematical_assumptions"))
        if _clean_text(item)
    ]
    obligations = [_clean_text(item) for item in _ensure_list(macro_leading.get("proof_obligations")) if _clean_text(item)]
    lemmas = [_clean_text(item) for item in _ensure_list(macro_leading.get("candidate_lemmas")) if _clean_text(item)]
    proof_outline = [_clean_text(item) for item in _ensure_list(macro_leading.get("proof_outline")) if _clean_text(item)]
    main_grounded = bool(_clean_text(macro_main.get("core_claim")) and _clean_text(macro_main.get("grounding_implication")))
    completion_clear = open_count == 0 and partial_count == 0
    no_failed_judges = _terminal_judge_failure_count(terminal_attempts) == 0 and len(terminal_attempts) > 0

    critics: list[dict[str, Any]] = []

    def add_critic(critic_id: str, title: str, score: int, rationale: str) -> None:
        """Append one bounded critic verdict to the report under construction."""
        critics.append(
            {
                "critic_id": critic_id,
                "title": title,
                "score": max(0, min(4, int(score))),
                "rationale": _clean_text(rationale),
            }
        )

    if main_grounded and completion_clear and proved_count > 0:
        add_critic(
            "main-claim-closure",
            "Main-Claim Closure Critic",
            4,
            "The main conjecture is grounded by a final implication and the completion checklist no longer reports open or partial steps.",
        )
    elif main_grounded and proved_count > 0 and open_count <= 1:
        add_critic(
            "main-claim-closure",
            "Main-Claim Closure Critic",
            3,
            "A terminal proved result exists and the route is close to closure, but at least one checklist item still remains open or partial.",
        )
    elif main_grounded and _clean_text(macro_main.get("route_target_claim")):
        add_critic(
            "main-claim-closure",
            "Main-Claim Closure Critic",
            2,
            "The route target and final grounding implication are explicit, but no terminal route result yet closes the main problem.",
        )
    elif _clean_text(macro_main.get("core_claim")):
        add_critic(
            "main-claim-closure",
            "Main-Claim Closure Critic",
            1,
            "The main claim is named, but the route is not yet grounded by a completed proof chain.",
        )
    else:
        add_critic("main-claim-closure", "Main-Claim Closure Critic", 0, "No grounded route to the main claim is currently visible.")

    if completion_clear and proved_count > 0 and no_failed_judges:
        add_critic(
            "dependency-closure",
            "Dependency-Closure Critic",
            4,
            "Critical dependencies are closed: the checklist is clear, a terminal proved result exists, and no critique judge failures remain.",
        )
    elif proved_count > 0 and open_count <= 2:
        add_critic(
            "dependency-closure",
            "Dependency-Closure Critic",
            3,
            "A proved route result exists and only a small residual dependency set remains.",
        )
    elif obligations and lemmas:
        add_critic(
            "dependency-closure",
            "Dependency-Closure Critic",
            2,
            "The route has explicit obligations and candidate lemmas, but they are not yet discharged.",
        )
    elif obligations or strategy_missing:
        add_critic(
            "dependency-closure",
            "Dependency-Closure Critic",
            1,
            "The missing dependencies are listed, but the route is still materially open.",
        )
    else:
        add_critic("dependency-closure", "Dependency-Closure Critic", 0, "The dependency structure is too incomplete to support closure judgments.")

    if mathematical_assumptions and not route_consistency_note and _all_target_judges_pass(terminal_attempts, "assumption"):
        add_critic(
            "assumption-discipline",
            "Assumption-Discipline Critic",
            4,
            "Assumptions are explicit, the route has no active representation inconsistency, and terminal attempts passed the assumption-discipline judge.",
        )
    elif mathematical_assumptions and _all_target_judges_pass(terminal_attempts, "assumption"):
        add_critic(
            "assumption-discipline",
            "Assumption-Discipline Critic",
            3,
            "Assumptions are explicit and critique passed, but a representation shift still weakens full assumption discipline.",
        )
    elif mathematical_assumptions:
        add_critic(
            "assumption-discipline",
            "Assumption-Discipline Critic",
            2,
            "The route declares mathematical assumptions, but no terminal proof audit has yet stabilized them.",
        )
    elif _clean_text(macro_leading.get("candidate_object")):
        add_critic(
            "assumption-discipline",
            "Assumption-Discipline Critic",
            1,
            "A route exists, but assumptions are not yet disciplined enough for end-to-end plausibility.",
        )
    else:
        add_critic("assumption-discipline", "Assumption-Discipline Critic", 0, "Assumptions are not yet explicit enough to audit the route.")

    carrier_kind = _clean_text(macro_leading.get("carrier_kind"))
    candidate_object = _clean_text(macro_leading.get("candidate_object"))
    if candidate_object and carrier_kind and len(operationalizations) <= 1 and not route_consistency_note:
        add_critic(
            "bridge-realism",
            "Bridge-Realism Critic",
            4,
            "A single typed bridge object currently carries the route without unresolved representation ambiguity.",
        )
    elif candidate_object and carrier_kind and len(operationalizations) <= 2:
        add_critic(
            "bridge-realism",
            "Bridge-Realism Critic",
            3,
            "The bridge object is typed, but multiple operationalizations remain live.",
        )
    elif candidate_object and carrier_kind:
        add_critic(
            "bridge-realism",
            "Bridge-Realism Critic",
            2,
            "The bridge object is typed, but realism is weakened by unresolved multiplicity or insufficient route consolidation.",
        )
    elif candidate_object:
        add_critic(
            "bridge-realism",
            "Bridge-Realism Critic",
            1,
            "A named bridge object exists, but it is not yet mathematically typed enough to support a plausible end-to-end proof.",
        )
    else:
        add_critic("bridge-realism", "Bridge-Realism Critic", 0, "No credible bridge object is currently carrying the route.")

    if evidence_count >= 2 and (blocked_count + disproved_count) >= 1:
        add_critic(
            "adversarial-pressure",
            "Adversarial-Pressure Critic",
            4,
            "The route has absorbed real adversarial pressure, including explicit negative evidence and barrier-sensitive evaluation.",
        )
    elif evidence_count >= 1 and (blocked_count + disproved_count) >= 1:
        add_critic(
            "adversarial-pressure",
            "Adversarial-Pressure Critic",
            3,
            "The route has some external or negative pressure, though the adversarial record is still modest.",
        )
    elif (blocked_count + disproved_count) >= 1:
        add_critic(
            "adversarial-pressure",
            "Adversarial-Pressure Critic",
            2,
            "At least one negative or blocking result exists, so the route has seen nontrivial stress.",
        )
    elif negative_route or failure_diagnosis:
        add_critic(
            "adversarial-pressure",
            "Adversarial-Pressure Critic",
            1,
            "A negative route is stated, but it has not yet been tested by actual adversarial results.",
        )
    else:
        add_critic("adversarial-pressure", "Adversarial-Pressure Critic", 0, "The route has not yet faced a meaningful adversarial probe.")

    if latest_proved and _step_count(latest_proved) >= 3 and no_failed_judges:
        add_critic(
            "proof-granularity",
            "Proof-Granularity Critic",
            4,
            "A terminal proved attempt contains a multi-step inspectable argument and no critique failures.",
        )
    elif latest_proved and _step_count(latest_proved) >= 2:
        add_critic(
            "proof-granularity",
            "Proof-Granularity Critic",
            3,
            "A terminal proved attempt has a substantive stepwise argument, though full audit closure is not yet ideal.",
        )
    elif obligations and lemmas and proof_outline:
        add_critic(
            "proof-granularity",
            "Proof-Granularity Critic",
            2,
            "The proof architecture is inspectable through obligations, lemmas, and outline, but it is not yet a proved argument.",
        )
    elif obligations or lemmas:
        add_critic(
            "proof-granularity",
            "Proof-Granularity Critic",
            1,
            "The route has some proof structure, but not enough granularity to assess a plausible complete proof.",
        )
    else:
        add_critic("proof-granularity", "Proof-Granularity Critic", 0, "The proof remains too schematic to judge plausibility.")

    if main_grounded and completion_clear and not route_consistency_note:
        add_critic(
            "end-to-end-consistency",
            "End-to-End Consistency Critic",
            4,
            "The macro route, bridge object, and final implication align without active completion or representation defects.",
        )
    elif main_grounded and not route_consistency_note:
        add_critic(
            "end-to-end-consistency",
            "End-to-End Consistency Critic",
            3,
            "The global proof architecture is coherent, though completion defects still remain.",
        )
    elif main_grounded:
        add_critic(
            "end-to-end-consistency",
            "End-to-End Consistency Critic",
            2,
            "The final implication chain is known, but the route still has an internal consistency defect.",
        )
    elif _clean_text(macro_main.get("core_claim")):
        add_critic(
            "end-to-end-consistency",
            "End-to-End Consistency Critic",
            1,
            "The main claim is identified, but the end-to-end route remains insufficiently coherent.",
        )
    else:
        add_critic("end-to-end-consistency", "End-to-End Consistency Critic", 0, "No stable end-to-end proof architecture is in view.")

    traced_external_usage = 0
    for attempt in terminal_attempts:
        web_sources = _ensure_list(_ensure_dict(attempt.get("web_search_gate")).get("sources"))
        external_refs = _ensure_list(attempt.get("external_references"))
        if web_sources and external_refs:
            traced_external_usage += 1
    if proved_count > 0 and prior_art_count == 0 and traced_external_usage == len([a for a in terminal_attempts if _ensure_list(_ensure_dict(a.get("web_search_gate")).get("sources"))]):
        add_critic(
            "novelty-discipline",
            "Novelty-Discipline Critic",
            4,
            "The current terminal results are not marked as prior art and any external search usage is traceably imported into InformalMathLib.",
        )
    elif terminal_attempts and prior_art_count == 0:
        add_critic(
            "novelty-discipline",
            "Novelty-Discipline Critic",
            3,
            "Terminal attempts exist and none are currently downgraded to prior art, though search trace discipline is not yet maximal.",
        )
    elif terminal_attempts or external_reference_count > 0 or produced_paper_count > 0:
        add_critic(
            "novelty-discipline",
            "Novelty-Discipline Critic",
            2,
            "The system is at least tracking prior art and external references as first-class proof metadata.",
        )
    elif _clean_text(macro_status.get("novelty_argument")):
        add_critic(
            "novelty-discipline",
            "Novelty-Discipline Critic",
            1,
            "Novelty is only argued at the program level; no terminal proof result has yet been audited against prior art.",
        )
    else:
        add_critic("novelty-discipline", "Novelty-Discipline Critic", 0, "Novelty discipline is not yet strong enough to trust a proof claim.")

    critics.sort(key=lambda row: CRITIC_ORDER.index(row["critic_id"]) if row["critic_id"] in CRITIC_ORDER else 999)
    total_score = sum(_safe_int(row.get("score")) for row in critics)
    normalized_score = round(total_score / (4.0 * max(1, len(critics))), 3)
    min_critic_score = min((_safe_int(row.get("score"), 0) for row in critics), default=0)
    score_caps: list[dict[str, Any]] = []

    def apply_cap(*, cap: float, reason: str) -> None:
        """Apply an epistemic cap so programme maturity cannot masquerade as proof evidence."""

        nonlocal normalized_score
        bounded_cap = max(0.0, min(1.0, float(cap)))
        pre_cap = normalized_score
        normalized_score = round(min(normalized_score, bounded_cap), 3)
        if normalized_score < pre_cap:
            score_caps.append(
                {
                    "cap": bounded_cap,
                    "reason": _clean_text(reason),
                }
            )

    if evidence_count == 0 and proved_count == 0:
        apply_cap(
            cap=0.35,
            reason="No external evidence and no proved local result exist, so the score must remain in low-plausibility territory regardless of programme structure.",
        )
    elif proved_count == 0:
        apply_cap(
            cap=0.45,
            reason="Without any proved local result, the score cannot rise into near-solution territory.",
        )
    elif evidence_count == 0:
        apply_cap(
            cap=0.60,
            reason="A proved local route without supporting evidence still receives a moderate cap until external or adversarial evidence accumulates.",
        )

    mandatory_gates = {
        "grounded_main_conjecture": main_grounded,
        "terminal_proved_attempt": len(proved_attempts) > 0,
        "completion_checklist_clear": completion_clear,
        "no_failed_terminal_judges": no_failed_judges,
    }
    plausible_solution_detected = all(mandatory_gates.values()) and normalized_score >= 0.80 and min_critic_score >= 2

    if plausible_solution_detected:
        decision = "stop-plausible-solution"
        decision_detail = "The current artifact chain clears all plausibility gates for an end-to-end proof claim."
    elif not main_grounded:
        decision = "continue-missing-grounding"
        decision_detail = "The main conjecture is not yet grounded by a stable final implication chain."
    elif len(proved_attempts) == 0:
        decision = "continue-no-terminal-proof"
        decision_detail = "No terminal proved attempt yet carries the leading route to a candidate full solution."
    elif not completion_clear:
        decision = "continue-open-completion-items"
        decision_detail = "The macro-strategy checklist still has open or partial completion items."
    elif not no_failed_judges:
        decision = "continue-critique-failures"
        decision_detail = "At least one terminal proof attempt still carries critique failures."
    else:
        decision = "continue-low-plausibility"
        decision_detail = "The critic panel remains below the threshold for a plausible end-to-end proof."

    return {
        "metadata": {
            "kb_ref": kb_ref,
            "critic_count": len(critics),
            "terminal_attempt_count": len(terminal_attempts),
            "proved_attempt_count": len(proved_attempts),
            "open_completion_count": open_count,
            "partial_completion_count": partial_count,
            "established_completion_count": established_count,
        },
        "signals": {
            "main_grounded": main_grounded,
            "evidence_count": evidence_count,
            "proved_count": proved_count,
            "disproved_count": disproved_count,
            "blocked_count": blocked_count,
            "produced_paper_count": produced_paper_count,
            "external_reference_count": external_reference_count,
            "prior_art_count": prior_art_count,
            "route_consistency_note": route_consistency_note,
            "candidate_object": candidate_object,
            "carrier_kind": carrier_kind,
            "score_caps": score_caps,
        },
        "diagnosis_overview": diagnosis_overview,
        "mandatory_gates": mandatory_gates,
        "critics": critics,
        "plausibility_score": normalized_score,
        "decision": {
            "plausible_solution_detected": plausible_solution_detected,
            "decision": decision,
            "detail": decision_detail,
        },
    }


def build_plausibility_report_from_artifacts(repo_root: Path, artifacts_dir: Path) -> dict[str, Any]:
    """Load the current artifacts from disk and build a plausibility report from them."""
    inputs = load_plausibility_inputs(repo_root, artifacts_dir)
    return build_plausibility_report(
        kb_ref=inputs["kb_ref"],
        macro_state=inputs["macro_state"],
        macro_strategy=inputs["macro_strategy"],
        proof_summary=inputs["proof_summary"],
        mathlib=inputs["mathlib"],
        attempts=inputs["attempts"],
    )


def render_plausibility_markdown(report: dict[str, Any]) -> str:
    """Render the plausibility report as a compact expert-readable Markdown summary."""
    meta = _ensure_dict(report.get("metadata"))
    signals = _ensure_dict(report.get("signals"))
    diagnosis_overview = _ensure_dict(report.get("diagnosis_overview"))
    gates = _ensure_dict(report.get("mandatory_gates"))
    decision = _ensure_dict(report.get("decision"))
    critics = [row for row in _ensure_list(report.get("critics")) if isinstance(row, dict)]
    lines = [
        "# End-to-End Proof Plausibility Report",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Plausibility score: {report.get('plausibility_score', 0.0):.3f}",
        f"- Decision: {decision.get('decision', '')}",
        f"- Plausible solution detected: {decision.get('plausible_solution_detected', False)}",
        f"- Detail: {decision.get('detail', '')}",
        "",
        "## Context Vs Inference Diagnosis",
        "",
    ]
    for label, scope_note, row in (
        ("Queue Active", "Active queue rows only.", _ensure_dict(diagnosis_overview.get("queue_active"))),
        ("Queue", "Current non-archival queue rows.", _ensure_dict(diagnosis_overview.get("queue"))),
        (
            "Queue Historical Archive",
            "Retired or legacy ill-posed terminal queue rows.",
            _ensure_dict(diagnosis_overview.get("queue_historical")),
        ),
        ("Attempts Active", "Active attempt dossiers only.", _ensure_dict(diagnosis_overview.get("attempts_active"))),
        ("Attempts", "Latest current attempt dossiers after collapsing superseded retries.", _ensure_dict(diagnosis_overview.get("attempts"))),
        (
            "Attempts Historical Archive",
            "Superseded retries or attempts inherited from archived queue rows.",
            _ensure_dict(diagnosis_overview.get("attempts_historical")),
        ),
    ):
        if not row:
            continue
        context_counts = _ensure_dict(row.get("context_counts"))
        inference_counts = _ensure_dict(row.get("inference_counts"))
        lines.extend(
            [
                f"### {label}",
                "",
                f"- Scope: {scope_note}",
                f"- Count: {row.get('count', 0)}",
                (
                    f"- Context counts: well-posed={context_counts.get('well-posed', 0)}, "
                    f"partially-ill-posed={context_counts.get('partially-ill-posed', 0)}, "
                    f"ill-posed={context_counts.get('ill-posed', 0)}"
                ),
                (
                    f"- Inference counts: determined={inference_counts.get('determined', 0)}, "
                    f"underdetermined={inference_counts.get('underdetermined', 0)}, "
                    f"difficult-but-well-posed={inference_counts.get('difficult-but-well-posed', 0)}"
                ),
            ]
        )
        defects = [item for item in _ensure_list(row.get("common_blocking_defects")) if isinstance(item, dict)]
        if defects:
            lines.append(
                "- Common blocking defects: "
                + " | ".join(f"{item.get('text', '')} ({int(item.get('count', 0) or 0)})" for item in defects)
            )
        lines.append("")
    lines.extend(
        [
            "## Mandatory Gates",
            "",
        ]
    )
    for key, value in gates.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Signals",
            "",
            f"- Main grounded: {signals.get('main_grounded', False)}",
            f"- Evidence count: {signals.get('evidence_count', 0)}",
            f"- Proved results: {signals.get('proved_count', 0)}",
            f"- Disproved results: {signals.get('disproved_count', 0)}",
            f"- Blocked results: {signals.get('blocked_count', 0)}",
            f"- Produced papers: {signals.get('produced_paper_count', 0)}",
            f"- External references: {signals.get('external_reference_count', 0)}",
            f"- Prior-art findings: {signals.get('prior_art_count', 0)}",
            f"- Candidate object: {signals.get('candidate_object', '')}",
            f"- Carrier kind: {signals.get('carrier_kind', '')}",
            f"- Route consistency note: {signals.get('route_consistency_note', '')}",
            "",
        ]
    )
    caps = [row for row in _ensure_list(signals.get("score_caps")) if isinstance(row, dict)]
    if caps:
        lines.extend(["## Score Caps", ""])
        for row in caps:
            lines.append(f"- Cap: {float(row.get('cap', 0.0) or 0.0):.3f} | Reason: {row.get('reason', '')}")
        lines.append("")
    lines.extend(
        [
            "## Critic Panel",
            "",
            "| Critic | Score | Rationale |",
            "|---|---:|---|",
        ]
    )
    for row in critics:
        lines.append(f"| {row.get('title', '')} | {row.get('score', 0)} | {row.get('rationale', '')} |")
    if not critics:
        lines.append("| - | 0 | No critic data available. |")
    lines.append("")
    return "\n".join(lines)
