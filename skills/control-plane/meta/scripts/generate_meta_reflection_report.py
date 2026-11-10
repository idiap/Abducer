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

"""Generate a perspective-aware meta reflection report from current artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
_MACRO_SCRIPT_DIR = Path(__file__).resolve().parents[3] / "reporting" / "kb-macro-proof-paper-writer" / "scripts"
for _path in (_COMMON_DIR, _MACRO_SCRIPT_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from generate_macro_proof_state_report import compile_pdf
from high_reward_watch import high_reward_watch_paths
from high_reward_watch import load_high_reward_watch
from kb_context import kb_ref_from_artifacts_dir
from reasoning_log import ReasoningLogger


PERSPECTIVES: dict[str, dict[str, str]] = {
    "epistemic": {
        "label": "Epistemic Perspective",
        "focus": "treat the search as a process of learning where the inferential bottleneck really sits",
        "warning": "do not mistake richer organization or higher route articulation for solved mathematics",
    },
    "proof-programme": {
        "label": "Proof-Programme Perspective",
        "focus": "treat the current state as a conditional theorem programme and measure proof debt explicitly",
        "warning": "do not overread a route architecture as closure of the proof itself",
    },
    "barrier-aware": {
        "label": "Barrier-Aware Perspective",
        "focus": "treat the search as a test of where the route may fail, collapse, or reveal a genuine obstruction",
        "warning": "do not treat every failure mode as equally informative; prefer failures that sharpen a real frontier",
    },
    "expert-handoff": {
        "label": "Expert-Handoff Perspective",
        "focus": "treat the artifacts as material for a mathematician deciding what is inspectable, promising, and not yet trustworthy",
        "warning": "do not promote programme-level novelty into theorem-level novelty without terminal evidence",
    },
}

INTERPRETATIONS: dict[str, str] = {
    "balanced": "read the current state conservatively but allow genuine programme-level learning to count as progress",
    "constructive": "foreground what the route has clarified and what positive structure now exists",
    "skeptical": "treat unresolved representation defects, open obligations, and missing evidence as the dominant reading",
}


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _first_nonempty(*values: Any) -> str:
    for value in values:
        text = _clean_text(value)
        if text:
            return text
    return ""


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


def _truncate(value: Any, limit: int = 220) -> str:
    text = _clean_text(value)
    if len(text) <= limit:
        return text
    cut = text[: max(0, limit - 3)].rstrip()
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + "..."


def _latex_escape(value: Any) -> str:
    text = _clean_text(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = text.replace("->", r"$\rightarrow$ ")
    text = text.replace("`", "'")
    return text


def _dedupe_references(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        key = _clean_text(row.get("statement_id")) or f"{_clean_text(row.get('role'))}|{_clean_text(row.get('title'))}"
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def _critic_rows(plausibility: dict[str, Any], *, limit: int = 3) -> list[dict[str, Any]]:
    rows = [row for row in _ensure_list(plausibility.get("critics")) if isinstance(row, dict)]
    rows.sort(key=lambda row: _safe_int(row.get("score"), 99))
    return rows[:limit]


def _route_rows(search_tree: dict[str, Any], *, limit: int = 3) -> list[dict[str, Any]]:
    frontier = _ensure_dict(search_tree.get("frontier"))
    rows = [row for row in _ensure_list(frontier.get("resume")) if isinstance(row, dict)]
    rows.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)
    return rows[:limit]


def _high_reward_summary(high_reward_watch: dict[str, Any]) -> dict[str, Any]:
    """Extract the currently active or most recent high-reward continuation signal."""

    signals = [row for row in _ensure_list(high_reward_watch.get("signals")) if isinstance(row, dict)]
    if not signals:
        return {}
    active = [row for row in signals if _clean_text(row.get("status")).lower() == "active"]
    pending = [row for row in signals if _clean_text(row.get("status")).lower() == "pending"]
    chosen = active[0] if active else (pending[0] if pending else signals[-1])
    return {
        "status": _clean_text(chosen.get("status")),
        "signal_id": _clean_text(chosen.get("signal_id")),
        "title": _clean_text(chosen.get("title")),
        "result_id": _clean_text(chosen.get("result_id")),
        "queue_id": _clean_text(chosen.get("queue_id")),
        "major_subresult_score": _safe_int(chosen.get("major_subresult_score")),
        "recommended_extension_cycles": _safe_int(chosen.get("recommended_extension_cycles")),
        "continuation_rationale": _clean_text(chosen.get("continuation_rationale")),
        "follow_up_prove_queue_ids": [
            _clean_text(value)
            for value in _ensure_list(chosen.get("follow_up_prove_queue_ids"))
            if _clean_text(value)
        ],
        "follow_up_discovery_branch_ids": [
            _clean_text(value)
            for value in _ensure_list(chosen.get("follow_up_discovery_branch_ids"))
            if _clean_text(value)
        ],
    }


def _shift_register(
    *,
    main_conjecture: dict[str, Any],
    leading_route: dict[str, Any],
    proof_summary: dict[str, Any],
    plausibility: dict[str, Any],
) -> list[dict[str, str]]:
    route_target = _clean_text(main_conjecture.get("route_target_claim"))
    core_claim = _clean_text(main_conjecture.get("core_claim"))
    candidate_object = _clean_text(leading_route.get("candidate_object"))
    route_note = _clean_text(leading_route.get("route_consistency_note"))
    pending = _safe_int(_ensure_dict(proof_summary.get("metadata")).get("pending_count"))
    proved = _safe_int(_ensure_dict(proof_summary.get("metadata")).get("proved_count"))
    signals = _ensure_dict(plausibility.get("signals"))
    evidence = _safe_int(signals.get("evidence_count"))

    return [
        {
            "label": "perspective-shift",
            "title": "The main problem is no longer being approached as a direct P versus NP proof.",
            "before": f"The ambient question is the direct conjecture `{core_claim}`.",
            "after": f"The current programme first targets `{route_target}` and only then returns to `{core_claim}` through the grounding implication.",
            "significance": "This is a genuine reframing of the search unit, because it replaces a monolithic open problem with a theorem-pair-specific route target.",
        },
        {
            "label": "sharpening",
            "title": "The bridge has become object-level rather than merely topical.",
            "before": "The hidden transport in the route could be discussed only as a generic bridge or magnification idea.",
            "after": f"The current route is organized around the typed carrier `{candidate_object}` and a named preserved invariant.",
            "significance": "This sharpens the inferential burden from 'find a connection' to 'realize, transport, and cash out a specific bridge object'.",
        },
        {
            "label": "unresolved-defect",
            "title": "Object typing improved, but representation alignment is still unresolved.",
            "before": "The route lacked a concrete carrier.",
            "after": route_note or "Multiple operationalizations remain live without a proved equivalence.",
            "significance": "This is progress in inspectability but not yet in closure; the framework now knows exactly where the representation defect sits.",
        },
        {
            "label": "sharpening",
            "title": "The proof frontier is now theorem-sized and file-backed.",
            "before": "Open work existed only as a diffuse set of bridge or strategy obligations.",
            "after": f"The process now exposes a persistent queue with {pending} pending theorem-shaped proof targets and explicit route lemmas.",
            "significance": "This changes the discovery process from free exploration into an auditable sequence of prove-or-disprove tasks.",
        },
        {
            "label": "persistence",
            "title": "The central hardness still persists as missing proof-carrying evidence.",
            "before": "The original problem was hard because routes spanned incompatible regimes and lacked explicit transfer mechanisms.",
            "after": f"The current state still lacks terminal proof resolution (`proved_count={proved}`) and still shows low external pressure (`evidence_count={evidence}`).",
            "significance": "The process has localized the bottleneck, but it has not yet dissolved it.",
        },
    ]


def build_meta_reflection_report(
    *,
    artifacts_dir: Path,
    perspective: str = "epistemic",
    interpretation: str = "balanced",
) -> dict[str, Any]:
    kb_ref = kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise ValueError("Could not resolve kb_ref from artifacts directory.")

    hardness = _load_json(artifacts_dir / "epistemic-hardness.json")
    macro_state = _load_json(artifacts_dir / "macro-proof-state.json")
    macro_strategy = _load_json(artifacts_dir / "macro-strategy-report.json")
    proof_summary = _load_json(artifacts_dir / "proof-cycle-summary.json")
    plausibility = _load_json(artifacts_dir / "end-to-end-proof-plausibility.json")
    promising = _load_json(artifacts_dir / "promising-directions-report.json")
    search_tree = _load_json(artifacts_dir / "search-space-tree.json")
    high_reward_watch_json, _high_reward_watch_md = high_reward_watch_paths(artifacts_dir)
    high_reward_watch = load_high_reward_watch(high_reward_watch_json, kb_ref=kb_ref)

    perspective_row = PERSPECTIVES.get(perspective, PERSPECTIVES["epistemic"])
    interpretation_note = INTERPRETATIONS.get(interpretation, INTERPRETATIONS["balanced"])

    main_conjecture = _ensure_dict(macro_state.get("main_conjecture"))
    leading_route = _ensure_dict(macro_state.get("leading_route"))
    status_assessment = _ensure_dict(macro_state.get("status_assessment"))
    narrative = _ensure_dict(macro_strategy.get("narrative"))
    proof_meta = _ensure_dict(proof_summary.get("metadata"))
    decision = _ensure_dict(plausibility.get("decision"))
    signals = _ensure_dict(plausibility.get("signals"))

    critic_rows = _critic_rows(plausibility)
    shift_rows = _shift_register(
        main_conjecture=main_conjecture,
        leading_route=leading_route,
        proof_summary=proof_summary,
        plausibility=plausibility,
    )
    frontier_rows = _route_rows(search_tree)
    high_reward = _high_reward_summary(high_reward_watch)

    original_hardness_summary = _first_nonempty(
        hardness.get("epistemic_difficulty_summary"),
        "The original problem is hard because it mixes long-range inferential jumps, sparse explicit dependencies, and barrier-sensitive regime changes.",
    )
    persistent_difficulties = [
        {
            "title": "Representation and transport remain the core unresolved issue.",
            "detail": _first_nonempty(
                leading_route.get("route_consistency_note"),
                "The current route still depends on fixing a single bridge object and proving the transport it is supposed to carry.",
            ),
        },
        {
            "title": "The process is still evidence-thin.",
            "detail": f"Current signals remain weak at the terminal level: evidence_count={_safe_int(signals.get('evidence_count'))}, proved_count={_safe_int(proof_meta.get('proved_count'))}, plausible_solution_detected={bool(decision.get('plausible_solution_detected'))}.",
        },
    ]
    for row in critic_rows:
        persistent_difficulties.append(
            {
                "title": _first_nonempty(row.get("title"), row.get("critic_id")),
                "detail": _first_nonempty(row.get("rationale")),
            }
        )

    intermediate_reading = [
        {
            "title": "The current intermediate results primarily changed route inspectability.",
            "detail": _first_nonempty(
                narrative.get("subresult_value"),
                "The strongest value of the present state is that intermediate claims are now theorem-shaped, inspectable, and attached to explicit bridge objects.",
            ),
        },
        {
            "title": "The leading route is now interpretable as a conditional theorem programme.",
            "detail": _first_nonempty(
                leading_route.get("conditional_proposition"),
                "The route is no longer just a topic connection; it is a conditional theorem package with named obligations and candidate lemmas.",
            ),
        },
    ]
    top_direction = _ensure_dict((_ensure_list(promising.get("most_promising_directions")) or [{}])[0])
    if top_direction:
        intermediate_reading.append(
            {
                "title": "The top direction changed the mathematical narrative even without closing the proof.",
                "detail": _first_nonempty(
                    *(_ensure_list(top_direction.get("novelty_points"))[:2]),
                    "The strongest route now articulates a typed carrier, a preserved invariant, and a route-specific missing lemma.",
                ),
            }
        )
    if high_reward:
        intermediate_reading.append(
            {
                "title": "A high-value intermediate result now justifies bounded continuation explicitly.",
                "detail": _clean_text(
                    f"Signal `{high_reward.get('signal_id')}` is `{high_reward.get('status')}` around "
                    f"`{high_reward.get('title')}` with score {high_reward.get('major_subresult_score', 0)}. "
                    f"It justifies up to {high_reward.get('recommended_extension_cycles', 0)} extra work cycles because "
                    f"it seeded follow-up proof tasks ({len(_ensure_list(high_reward.get('follow_up_prove_queue_ids')))} items) "
                    f"and discovery branches ({len(_ensure_list(high_reward.get('follow_up_discovery_branch_ids')))} items)."
                ),
            }
        )

    current_interpretation = {
        "headline": "The current proof state should be read as a conditional research programme rather than as a near-complete proof.",
        "detail": _first_nonempty(
            narrative.get("bottleneck"),
            status_assessment.get("assessment"),
            "The system has localized the proof debt into a small number of route-specific obligations, but the route remains open.",
        ),
        "not_yet": f"It is not yet a solved proof of `{_clean_text(main_conjecture.get('core_claim'))}` because the leading bridge still lacks discharged source-realization, transport, route, and payoff lemmas.",
    }
    if high_reward:
        current_interpretation["detail"] = _clean_text(
            f"{current_interpretation.get('detail', '')} The process also has an explicit high-reward continuation "
            f"mechanism around `{high_reward.get('title')}`, so extra cycles are being justified by a concrete intermediate result rather than by generic momentum."
        )

    meta_judgment = {
        "headline": "The discovery process has genuinely improved understanding of where the problem is hard, but it has not yet produced evidence that the main conjecture is close to resolution.",
        "detail": "What changed is the granularity of the problem: the search now isolates a sharper target, a typed carrier, a representation defect, and a queue of inspectable obligations. What persists is the absence of terminal proof evidence, adversarial stress, and representation closure.",
        "next_question": "Should the next cycle try to close the leading bridge representation defect, or should it seek a barrier result showing that one operationalization cannot realize the route as currently stated?",
    }
    if perspective == "barrier-aware":
        meta_judgment["headline"] = "The strongest current meta lesson is not successful transport but clarified obstruction pressure."
        meta_judgment["detail"] = "The route now exposes where failure would matter: representation mismatch, transport weakness, and low adversarial evidence are no longer vague difficulties but named defects."
        meta_judgment["next_question"] = "Which negative result would most strongly compress the search space if the current bridge object is impossible or non-payoff-generating?"
    elif perspective == "proof-programme":
        meta_judgment["headline"] = "The current state is a disciplined macro-proof programme with explicit proof debt, not yet a proof."
        meta_judgment["detail"] = "The gain is closure of the programme around a small theorem package. The loss is that none of the terminal obligations has yet been discharged."
        meta_judgment["next_question"] = "Which one theorem, if proved next, would collapse the largest remaining fraction of the route debt?"
    elif perspective == "expert-handoff":
        meta_judgment["headline"] = "The current artifacts are now strong enough for expert inspection, but not strong enough for expert endorsement of a proof claim."
        meta_judgment["detail"] = "A human expert can now inspect a grounded route, candidate carrier, representation defect, and theorem-sized proof frontier. What remains missing is decisive mathematical validation."
        meta_judgment["next_question"] = "Which single route lemma or equivalence question is mature enough to hand to a domain expert as the next audit target?"

    references = _dedupe_references(
        [row for row in _ensure_list(macro_state.get("references")) if isinstance(row, dict)]
        + [row for row in _ensure_list(macro_strategy.get("references")) if isinstance(row, dict)]
    )

    return {
        "metadata": {
            "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "kb_ref": kb_ref,
            "perspective": perspective,
            "perspective_label": perspective_row["label"],
            "interpretation": interpretation,
            "input_artifacts": {
                "epistemic_hardness": bool(hardness),
                "macro_proof_state": bool(macro_state),
                "macro_strategy_report": bool(macro_strategy),
                "proof_cycle_summary": bool(proof_summary),
                "end_to_end_plausibility": bool(plausibility),
                "promising_directions": bool(promising),
                "search_space_tree": bool(search_tree),
                "high_reward_watch": high_reward_watch_json.exists() and bool(_ensure_list(high_reward_watch.get("signals"))),
            },
        },
        "perspective_statement": {
            "label": perspective_row["label"],
            "focus": perspective_row["focus"],
            "warning": perspective_row["warning"],
            "interpretation": interpretation_note,
        },
        "original_hardness": {
            "summary": original_hardness_summary,
            "main_conjecture": _clean_text(main_conjecture.get("core_claim")),
            "route_target": _clean_text(main_conjecture.get("route_target_claim")),
            "hardness_elements": [
                {
                    "title": "Cross-regime proof movement remains difficult.",
                    "detail": "The current route still requires movement from a weak-model lower bound regime to a stronger separation consequence through a bridge object rather than by direct deduction.",
                },
                {
                    "title": "Barrier pressure is now more localized than before.",
                    "detail": _first_nonempty(
                        _ensure_list(persistent_difficulties)[0].get("detail"),
                        "The bridge object and transport law are now explicit sites of failure rather than only generic sources of difficulty.",
                    ),
                },
            ],
        },
        "current_proof_state_interpretation": current_interpretation,
        "shifts_of_understanding": shift_rows,
        "persistent_difficulties": persistent_difficulties,
        "intermediate_result_reading": intermediate_reading,
        "high_reward_continuation": high_reward,
        "frontier_snapshot": [
            {
                "bridge_id": _clean_text(row.get("bridge_id")),
                "policy": _clean_text(row.get("policy")),
                "route_synopsis": _clean_text(row.get("route_synopsis")),
            }
            for row in frontier_rows
        ],
        "meta_judgment": meta_judgment,
        "references": references,
    }


def render_markdown(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    perspective = _ensure_dict(report.get("perspective_statement"))
    original = _ensure_dict(report.get("original_hardness"))
    current = _ensure_dict(report.get("current_proof_state_interpretation"))
    high_reward = _ensure_dict(report.get("high_reward_continuation"))
    meta_judgment = _ensure_dict(report.get("meta_judgment"))

    lines = [
        f"# Meta Reflection Report for {meta.get('kb_ref', '')}",
        "",
        "## Perspective",
        "",
        f"- Perspective: {perspective.get('label', '')}",
        f"- Focus: {perspective.get('focus', '')}",
        f"- Interpretation: {perspective.get('interpretation', '')}",
        f"- Warning: {perspective.get('warning', '')}",
        "",
        "## Original Hardness",
        "",
        original.get("summary", ""),
        "",
    ]
    for row in _ensure_list(original.get("hardness_elements")):
        if not isinstance(row, dict):
            continue
        lines.extend(
            [
                f"### {_clean_text(row.get('title'))}",
                "",
                _clean_text(row.get("detail")),
                "",
            ]
        )
    lines.extend(
        [
            "## Current Proof-State Interpretation",
            "",
            current.get("headline", ""),
            "",
            current.get("detail", ""),
            "",
            f"Not yet: {current.get('not_yet', '')}",
            "",
            "## Shifts Of Understanding",
            "",
        ]
    )
    for row in _ensure_list(report.get("shifts_of_understanding")):
        if not isinstance(row, dict):
            continue
        lines.extend(
            [
                f"### {_clean_text(row.get('title'))}",
                "",
                f"- Class: {_clean_text(row.get('label'))}",
                f"- Before: {_clean_text(row.get('before'))}",
                f"- After: {_clean_text(row.get('after'))}",
                f"- Why it matters: {_clean_text(row.get('significance'))}",
                "",
            ]
        )
    lines.extend(["## Persistent Difficulties", ""])
    for row in _ensure_list(report.get("persistent_difficulties")):
        if not isinstance(row, dict):
            continue
        lines.extend(
            [
                f"### {_clean_text(row.get('title'))}",
                "",
                _clean_text(row.get("detail")),
                "",
            ]
        )
    lines.extend(["## Intermediate-Result Reading", ""])
    for row in _ensure_list(report.get("intermediate_result_reading")):
        if not isinstance(row, dict):
            continue
        lines.extend(
            [
                f"### {_clean_text(row.get('title'))}",
                "",
                _clean_text(row.get("detail")),
                "",
            ]
        )
    lines.extend(["## High-Reward Continuation", ""])
    if not high_reward:
        lines.extend(["No active or pending high-reward continuation signal is recorded.", ""])
    else:
        lines.extend(
            [
                f"- Signal: {high_reward.get('signal_id', '')}",
                f"- Status: {high_reward.get('status', '')}",
                f"- Result: {high_reward.get('title', '')}",
                f"- Score: {high_reward.get('major_subresult_score', 0)}",
                f"- Recommended extension cycles: {high_reward.get('recommended_extension_cycles', 0)}",
                f"- Rationale: {high_reward.get('continuation_rationale', '')}",
                f"- Follow-up proof tasks: {', '.join(_ensure_list(high_reward.get('follow_up_prove_queue_ids')))}",
                f"- Follow-up discovery branches: {', '.join(_ensure_list(high_reward.get('follow_up_discovery_branch_ids')))}",
                "",
            ]
        )
    lines.extend(["## Frontier Snapshot", ""])
    for row in _ensure_list(report.get("frontier_snapshot")):
        if not isinstance(row, dict):
            continue
        lines.extend(
            [
                f"- `{_clean_text(row.get('bridge_id'))}` [{_clean_text(row.get('policy'))}]",
                f"  {_clean_text(row.get('route_synopsis'))}",
            ]
        )
    lines.extend(
        [
            "",
            "## Meta Judgment",
            "",
            meta_judgment.get("headline", ""),
            "",
            meta_judgment.get("detail", ""),
            "",
            f"Next governing question: {meta_judgment.get('next_question', '')}",
            "",
            "## References",
            "",
        ]
    )
    for row in _ensure_list(report.get("references")):
        if not isinstance(row, dict):
            continue
        label = _first_nonempty(row.get("role"), row.get("title"), row.get("statement_id"))
        detail = _first_nonempty(row.get("excerpt"), row.get("detail"))
        statement_id = _clean_text(row.get("statement_id"))
        prefix = f"`{statement_id}` " if statement_id else ""
        lines.append(f"- {prefix}{label}: {_truncate(detail, 260)}")
    return "\n".join(lines).strip() + "\n"


def render_tex(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    perspective = _ensure_dict(report.get("perspective_statement"))
    original = _ensure_dict(report.get("original_hardness"))
    current = _ensure_dict(report.get("current_proof_state_interpretation"))
    high_reward = _ensure_dict(report.get("high_reward_continuation"))
    meta_judgment = _ensure_dict(report.get("meta_judgment"))

    def bullet_items(rows: list[dict[str, Any]], *, field: str = "detail") -> str:
        items: list[str] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            title = _latex_escape(row.get("title"))
            detail = _latex_escape(row.get(field))
            items.append(f"\\item \\textbf{{{title}}} {detail}")
        return "\n".join(items) if items else r"\item No items recorded."

    shift_items: list[str] = []
    for row in _ensure_list(report.get("shifts_of_understanding")):
        if not isinstance(row, dict):
            continue
        shift_items.append(
            "\n".join(
                [
                    f"\\item \\textbf{{{_latex_escape(row.get('title'))}}}",
                    f"\\\\ Class: {_latex_escape(row.get('label'))}",
                    f"\\\\ Before: {_latex_escape(row.get('before'))}",
                    f"\\\\ After: {_latex_escape(row.get('after'))}",
                    f"\\\\ Why it matters: {_latex_escape(row.get('significance'))}",
                ]
            )
        )
    if not shift_items:
        shift_items.append(r"\item No shifts recorded.")

    frontier_items = "\n".join(
        [
            f"\\item \\textbf{{{_latex_escape(row.get('bridge_id'))}}} [{_latex_escape(row.get('policy'))}] {_latex_escape(row.get('route_synopsis'))}"
            for row in _ensure_list(report.get("frontier_snapshot"))
            if isinstance(row, dict)
        ]
    )
    if not frontier_items:
        frontier_items = r"\item No frontier routes recorded."
    reference_items = "\n".join(
        [
            f"\\item \\textbf{{{_latex_escape(_first_nonempty(row.get('role'), row.get('title'), row.get('statement_id'))) }}} {_latex_escape(_truncate(_first_nonempty(row.get('excerpt'), row.get('detail')), 260))}"
            for row in _ensure_list(report.get("references"))
            if isinstance(row, dict)
        ]
    )
    if not reference_items:
        reference_items = r"\item No references recorded."
    high_reward_block = r"No active or pending high-reward continuation signal is recorded."
    if high_reward:
        high_reward_block = "\n".join(
            [
                f"\\textbf{{Signal.}} {_latex_escape(high_reward.get('signal_id'))}",
                "",
                f"\\textbf{{Status.}} {_latex_escape(high_reward.get('status'))}",
                "",
                f"\\textbf{{Result.}} {_latex_escape(high_reward.get('title'))}",
                "",
                f"\\textbf{{Score.}} {_latex_escape(high_reward.get('major_subresult_score'))}",
                "",
                f"\\textbf{{Recommended extension cycles.}} {_latex_escape(high_reward.get('recommended_extension_cycles'))}",
                "",
                f"\\textbf{{Rationale.}} {_latex_escape(high_reward.get('continuation_rationale'))}",
                "",
                f"\\textbf{{Follow-up proof tasks.}} {_latex_escape(', '.join(_ensure_list(high_reward.get('follow_up_prove_queue_ids'))))}",
                "",
                f"\\textbf{{Follow-up discovery branches.}} {_latex_escape(', '.join(_ensure_list(high_reward.get('follow_up_discovery_branch_ids'))))}",
            ]
        )

    return f"""\\documentclass[11pt]{{article}}
\\usepackage[a4paper,margin=1in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}
\\title{{Meta Reflection Report for {_latex_escape(meta.get('kb_ref'))}}}
\\author{{Abducer}}
\\date{{{_latex_escape(meta.get('generated_utc'))}}}
\\begin{{document}}
\\maketitle

\\begin{{abstract}}
This report reflects on the discovery process itself. It asks why the original problem remains hard, how the current bridge and proof programme altered the framing of the problem, and what has genuinely shifted or persisted in understanding under the {_latex_escape(perspective.get('label'))}.
\\end{{abstract}}

\\section{{Perspective}}
\\textbf{{Perspective.}} {_latex_escape(perspective.get('label'))}

\\textbf{{Focus.}} {_latex_escape(perspective.get('focus'))}

\\textbf{{Interpretation.}} {_latex_escape(perspective.get('interpretation'))}

\\textbf{{Warning.}} {_latex_escape(perspective.get('warning'))}

\\section{{Original Hardness}}
{_latex_escape(original.get('summary'))}

\\begin{{itemize}}[leftmargin=1.5em]
{bullet_items([row for row in _ensure_list(original.get("hardness_elements")) if isinstance(row, dict)])}
\\end{{itemize}}

\\section{{Current Proof-State Interpretation}}
\\textbf{{Headline.}} {_latex_escape(current.get('headline'))}

{_latex_escape(current.get('detail'))}

\\textbf{{Not yet.}} {_latex_escape(current.get('not_yet'))}

\\section{{Shifts Of Understanding}}
\\begin{{itemize}}[leftmargin=1.5em]
{chr(10).join(shift_items)}
\\end{{itemize}}

\\section{{Persistent Difficulties}}
\\begin{{itemize}}[leftmargin=1.5em]
{bullet_items([row for row in _ensure_list(report.get("persistent_difficulties")) if isinstance(row, dict)])}
\\end{{itemize}}

\\section{{Intermediate-Result Reading}}
\\begin{{itemize}}[leftmargin=1.5em]
{bullet_items([row for row in _ensure_list(report.get("intermediate_result_reading")) if isinstance(row, dict)])}
\\end{{itemize}}

\\section{{High-Reward Continuation}}
{high_reward_block}

\\section{{Frontier Snapshot}}
\\begin{{itemize}}[leftmargin=1.5em]
{frontier_items}
\\end{{itemize}}

\\section{{Meta Judgment}}
\\textbf{{Headline.}} {_latex_escape(meta_judgment.get('headline'))}

{_latex_escape(meta_judgment.get('detail'))}

\\textbf{{Next governing question.}} {_latex_escape(meta_judgment.get('next_question'))}

\\section{{References}}
\\begin{{itemize}}[leftmargin=1.5em]
{reference_items}
\\end{{itemize}}

\\end{{document}}
"""


def write_report(
    report: dict[str, Any],
    *,
    output_json: Path,
    output_md: Path,
    output_tex: Path,
    output_pdf: Path,
) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")
    output_tex.write_text(render_tex(report), encoding="utf-8")
    compile_pdf(output_tex, output_pdf)


def main() -> int:
    logger = ReasoningLogger("meta")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    ap.add_argument("--perspective", default="epistemic", choices=sorted(PERSPECTIVES), help="Meta perspective.")
    ap.add_argument("--interpretation", default="balanced", choices=sorted(INTERPRETATIONS), help="Interpretive stance.")
    ap.add_argument("--output-json", default="", help="Optional output JSON path.")
    ap.add_argument("--output-md", default="", help="Optional output Markdown path.")
    ap.add_argument("--output-tex", default="", help="Optional output TeX path.")
    ap.add_argument("--output-pdf", default="", help="Optional output PDF path.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()

    kb_ref = kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("[ERROR] Could not resolve kb_ref for meta reflection.")

    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "meta-reflection-report.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "meta-reflection-report.md"
    output_tex = Path(args.output_tex) if args.output_tex else artifacts_dir / "meta-reflection-report.tex"
    output_pdf = Path(args.output_pdf) if args.output_pdf else artifacts_dir / "meta-reflection-report.pdf"
    for name, path in {
        "json": output_json,
        "md": output_md,
        "tex": output_tex,
        "pdf": output_pdf,
    }.items():
        if not path.is_absolute():
            resolved = (repo_root / path).resolve()
            if name == "json":
                output_json = resolved
            elif name == "md":
                output_md = resolved
            elif name == "tex":
                output_tex = resolved
            else:
                output_pdf = resolved

    report = build_meta_reflection_report(
        artifacts_dir=artifacts_dir,
        perspective=args.perspective,
        interpretation=args.interpretation,
    )
    write_report(
        report,
        output_json=output_json,
        output_md=output_md,
        output_tex=output_tex,
        output_pdf=output_pdf,
    )

    judgment = _ensure_dict(report.get("meta_judgment"))
    logger.step(
        "Generated meta reflection report",
        "\n".join(
            [
                f"kb_ref={kb_ref}",
                f"perspective={args.perspective}",
                f"interpretation={args.interpretation}",
                f"headline={_clean_text(judgment.get('headline'))}",
            ]
        ),
        surface_focus="meta-reflection",
        surface_stage="meta",
        surface_metrics={
            "shift_count": len(_ensure_list(report.get("shifts_of_understanding"))),
            "persistent_difficulty_count": len(_ensure_list(report.get("persistent_difficulties"))),
            "frontier_route_count": len(_ensure_list(report.get("frontier_snapshot"))),
        },
        surface_taxonomy={"reasoning_types": ["meta-analysis", "reflective-interpretation"]},
    )
    logger.add_output("meta_reflection_json", output_json)
    logger.add_output("meta_reflection_md", output_md)
    logger.add_output("meta_reflection_tex", output_tex)
    logger.add_output("meta_reflection_pdf", output_pdf)
    log_path = logger.finalize(
        "success",
        summary=f"Generated meta reflection report for `{kb_ref}` under perspective `{args.perspective}`.",
    )
    print(f"[OK] Wrote meta reflection JSON: {output_json}")
    print(f"[OK] Wrote meta reflection Markdown: {output_md}")
    print(f"[OK] Wrote meta reflection TeX: {output_tex}")
    print(f"[OK] Wrote meta reflection PDF: {output_pdf}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
