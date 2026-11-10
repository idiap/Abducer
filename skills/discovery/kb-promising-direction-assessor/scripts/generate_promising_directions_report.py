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

"""Generate a promising-directions assessment report from final KB artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _clean_text(value: Any) -> str:
    text = str(value or "").strip()
    return " ".join(text.split())


def _first_nonempty(*values: Any) -> str:
    for value in values:
        cleaned = _clean_text(value)
        if cleaned:
            return cleaned
    return ""


def _truncate(text: Any, limit: int = 180) -> str:
    cleaned = _clean_text(text)
    if len(cleaned) <= limit:
        return cleaned
    cut = cleaned[: max(0, limit - 3)].rstrip()
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


def _kb_ref_from_artifacts_dir(artifacts_dir: Path, expert: dict[str, Any]) -> str:
    metadata = _ensure_dict(expert.get("metadata"))
    return _first_nonempty(metadata.get("kb_ref"), artifacts_dir.name)


def _normalize_bridges(expert: dict[str, Any]) -> list[dict[str, Any]]:
    portfolio = [row for row in _ensure_list(expert.get("bridge_portfolio")) if isinstance(row, dict)]
    by_id = {_clean_text(row.get("bridge_id")): row for row in portfolio if _clean_text(row.get("bridge_id"))}
    recommended: list[dict[str, Any]] = []
    for item in _ensure_list(expert.get("recommended_bridges")):
        if isinstance(item, dict):
            bridge_id = _clean_text(item.get("bridge_id"))
            if bridge_id and bridge_id in by_id:
                merged = dict(by_id[bridge_id])
                merged.update(item)
                recommended.append(merged)
            else:
                recommended.append(item)
        else:
            bridge_id = _clean_text(item)
            if bridge_id and bridge_id in by_id:
                recommended.append(by_id[bridge_id])
    bridges = recommended or portfolio
    bridges = [row for row in bridges if isinstance(row, dict)]
    bridges.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)
    return bridges


def _hypothesis_index(hypothesis_eval: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        _clean_text(row.get("hypothesis_id")): row
        for row in _ensure_list(hypothesis_eval.get("results"))
        if isinstance(row, dict) and _clean_text(row.get("hypothesis_id"))
    }


def _direction_title(bridge: dict[str, Any]) -> str:
    delta = _ensure_dict(bridge.get("statement_delta"))
    abstraction = _first_nonempty(bridge.get("abstraction_label"), bridge.get("conjectured_object"), bridge.get("bridge_id"))
    target_focus = _first_nonempty(delta.get("target_claim_focus"), bridge.get("target_consequence_schema"), bridge.get("target_statement_id"))
    return _clean_text(f"{abstraction}: {target_focus}")


def _linked_hypothesis_summary(bridge: dict[str, Any], hypothesis_rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    linked_ids = [_clean_text(value) for value in _ensure_list(bridge.get("linked_hypothesis_ids")) if _clean_text(value)]
    linked_rows = [hypothesis_rows[hyp_id] for hyp_id in linked_ids if hyp_id in hypothesis_rows]
    verdicts: dict[str, int] = {}
    best_confidence = 0.0
    best_action = ""
    for row in linked_rows:
        verdict = _clean_text(row.get("verdict")) or "unknown"
        verdicts[verdict] = verdicts.get(verdict, 0) + 1
        best_confidence = max(best_confidence, _safe_float(row.get("confidence")))
        if not best_action:
            best_action = _clean_text(row.get("recommended_action"))
    return {
        "count": len(linked_rows),
        "verdict_counts": verdicts,
        "best_confidence": best_confidence,
        "best_action": best_action,
    }


def _build_novelty_points(bridge: dict[str, Any]) -> list[str]:
    delta = _ensure_dict(bridge.get("statement_delta"))
    abstraction = _first_nonempty(bridge.get("abstraction_label"), bridge.get("conjectured_object"))
    carrier_kind = _clean_text(bridge.get("carrier_kind"))
    invariant = _clean_text(bridge.get("preserved_invariant"))
    missing_lemma = _first_nonempty(bridge.get("missing_route_lemma"), delta.get("missing_witness_or_transport"))
    negative_route = _clean_text(bridge.get("negative_route"))
    points = [
        _clean_text(
            f"The route is theorem-pair specific: it tries to move from `{delta.get('source_claim_focus')}` to "
            f"`{delta.get('target_claim_focus')}` rather than proposing a generic topic-level bridge."
        ),
        _clean_text(
            f"The candidate novelty is the object `{abstraction}`, typed as `{carrier_kind}`, which is meant to make "
            f"the hidden transport mechanism mathematically explicit."
        ),
        _clean_text(
            f"The route is constrained by the preserved invariant `{invariant}`, so the proposal is not only "
            f"to reach the target consequence but to preserve a specific mathematical profile while doing so."
        ),
        _clean_text(
            f"The novelty remains programmatic rather than theorem-level because the decisive missing lemma is still: "
            f"{missing_lemma}"
        ),
    ]
    if negative_route:
        points.append(
            _clean_text(
                f"The route includes an explicit falsification probe: {negative_route}"
            )
        )
    return [point for point in points if point]


def _build_promising_points(bridge: dict[str, Any], linked: dict[str, Any]) -> list[str]:
    signals = _ensure_dict(bridge.get("signals"))
    sketch_operationalization = _safe_float(
        signals.get("sketch_operationalization", signals.get("proof_readiness"))
    )
    points = [
        _clean_text(
            f"Bridge priority {_safe_float(bridge.get('priority')):.3f} with sketch score "
            f"{_safe_float(signals.get('sketch_score')):.3f}, mathematical specificity "
            f"{_safe_float(signals.get('mathematical_specificity')):.3f}, evidence signal "
            f"{_safe_float(signals.get('evidence_signal')):.3f}, and sketch operationalization "
            f"{sketch_operationalization:.3f}."
        ),
        _clean_text(
            f"The route synopsis is: {bridge.get('route_synopsis')}"
        ),
        _clean_text(
            f"The proof family `{bridge.get('proof_strategy_family')}` is used because "
            f"{bridge.get('family_rationale')}"
        ),
    ]
    if linked.get("count"):
        points.append(
            _clean_text(
                f"Linked hypotheses: {linked.get('count')} with verdict profile {linked.get('verdict_counts')} "
                f"and best confidence {linked.get('best_confidence'):.3f}."
            )
        )
    return [point for point in points if point]


def _build_risk_points(bridge: dict[str, Any], evidence_count: int, unresolved_count: int) -> list[str]:
    points = [
        _clean_text(bridge.get("failure_diagnosis")),
        _clean_text(
            f"Abort logic: {_first_nonempty(*_ensure_list(bridge.get('abort_conditions'))[:2])}"
        ),
        _clean_text(
            f"Global limitation: evidence_count={evidence_count} and unresolved hypotheses={unresolved_count}, "
            f"so the route is still under mathematical pressure."
        ),
    ]
    return [point for point in points if point]


def _build_direction(bridge: dict[str, Any], hypothesis_rows: dict[str, dict[str, Any]], evidence_count: int, unresolved_count: int) -> dict[str, Any]:
    delta = _ensure_dict(bridge.get("statement_delta"))
    linked = _linked_hypothesis_summary(bridge, hypothesis_rows)
    return {
        "bridge_id": _clean_text(bridge.get("bridge_id")),
        "title": _direction_title(bridge),
        "priority": _safe_float(bridge.get("priority")),
        "bridge_type": _clean_text(bridge.get("bridge_type")),
        "source_statement_id": _clean_text(bridge.get("source_statement_id")),
        "target_statement_id": _clean_text(bridge.get("target_statement_id")),
        "source_excerpt": _first_nonempty(bridge.get("source_excerpt"), delta.get("source_theorem_excerpt")),
        "target_excerpt": _first_nonempty(bridge.get("target_excerpt"), delta.get("target_theorem_excerpt")),
        "route_synopsis": _clean_text(bridge.get("route_synopsis")),
        "abstraction_label": _first_nonempty(bridge.get("abstraction_label"), bridge.get("conjectured_object")),
        "carrier_kind": _clean_text(bridge.get("carrier_kind")),
        "preserved_invariant": _clean_text(bridge.get("preserved_invariant")),
        "statement_delta": delta,
        "missing_route_lemma": _first_nonempty(bridge.get("missing_route_lemma"), delta.get("missing_witness_or_transport")),
        "novelty_points": _build_novelty_points(bridge),
        "promising_points": _build_promising_points(bridge, linked),
        "risk_points": _build_risk_points(bridge, evidence_count, unresolved_count),
        "proof_obligations": [_clean_text(value) for value in _ensure_list(bridge.get("proof_obligations"))[:4] if _clean_text(value)],
        "candidate_lemmas": [_clean_text(value) for value in _ensure_list(bridge.get("candidate_lemmas"))[:4] if _clean_text(value)],
        "expert_actions": [_clean_text(value) for value in _ensure_list(bridge.get("expert_actions"))[:3] if _clean_text(value)],
        "negative_route": _clean_text(bridge.get("negative_route")),
        "linked_hypotheses": linked,
    }


def _select_next_best_direction(directions: list[dict[str, Any]], all_bridges: list[dict[str, Any]], hypothesis_rows: dict[str, dict[str, Any]], evidence_count: int, unresolved_count: int) -> dict[str, Any]:
    if not directions:
        return {}
    top = directions[0]
    top_bridge_id = _clean_text(top.get("bridge_id"))
    top_abstraction = _clean_text(top.get("abstraction_label"))
    top_source = _clean_text(top.get("source_statement_id"))
    top_target = _clean_text(top.get("target_statement_id"))
    for bridge in all_bridges:
        bridge_id = _clean_text(bridge.get("bridge_id"))
        if not bridge_id or bridge_id == top_bridge_id:
            continue
        if (
            _clean_text(bridge.get("abstraction_label")) == top_abstraction
            and _clean_text(bridge.get("source_statement_id")) == top_source
            and _clean_text(bridge.get("target_statement_id")) != top_target
        ):
            direction = _build_direction(bridge, hypothesis_rows, evidence_count, unresolved_count)
            direction["assessment"] = _clean_text(
                "This is the next best direction because it keeps the leading bridge object fixed while forcing it "
                "through a harder transport regime. If the same witness family survives this adjacent target, that is "
                "evidence that the carrier is mathematically real rather than tuned only to one theorem statement."
            )
            return direction
    fallback = next((bridge for bridge in all_bridges if _clean_text(bridge.get("bridge_id")) != top_bridge_id), {})
    if not fallback:
        return {}
    direction = _build_direction(fallback, hypothesis_rows, evidence_count, unresolved_count)
    direction["assessment"] = _clean_text(
        "This is the next best direction because it is the highest-priority surviving route outside the top bridge."
    )
    return direction


def _select_probe(hypothesis_eval: dict[str, Any], preferred_target: str = "") -> dict[str, Any]:
    rows = [row for row in _ensure_list(hypothesis_eval.get("results")) if isinstance(row, dict)]
    rows = [row for row in rows if _clean_text(row.get("verdict")) == "inconclusive"]
    rows.sort(key=lambda row: _safe_float(row.get("priority")), reverse=True)
    for row in rows:
        if preferred_target and _clean_text(row.get("target_statement_id")) == preferred_target:
            return row
    return rows[0] if rows else {}


def build_report(expert: dict[str, Any], hypothesis_eval: dict[str, Any], *, artifacts_dir: Path, top_k: int = 3) -> dict[str, Any]:
    bridges = _normalize_bridges(expert)
    hypothesis_rows = _hypothesis_index(hypothesis_eval)
    evidence_count = _safe_int(_ensure_dict(hypothesis_eval.get("metadata")).get("evidence_count"))
    unresolved_count = _safe_int(_ensure_dict(_ensure_dict(hypothesis_eval.get("summary")).get("verdict_counts")).get("inconclusive"))
    directions = [
        _build_direction(bridge, hypothesis_rows, evidence_count, unresolved_count)
        for bridge in bridges[: max(1, top_k)]
    ]
    next_best = _select_next_best_direction(directions, bridges, hypothesis_rows, evidence_count, unresolved_count)
    probe = _select_probe(hypothesis_eval, preferred_target=_clean_text(next_best.get("target_statement_id")))

    positive_evidence = [
        _clean_text(
            f"The leading route is theorem-grounded at the level of source and target excerpts, not only labels: "
            f"{directions[0].get('source_statement_id')} -> {directions[0].get('target_statement_id')}."
        ) if directions else "",
        _clean_text(
            f"The bridge objects are typed carriers such as `{directions[0].get('abstraction_label')}` with carrier "
            f"`{directions[0].get('carrier_kind')}`, rather than generic placeholders."
        ) if directions else "",
        _clean_text(
            "The routes expose explicit missing lemmas and negative routes, so novelty is attached to a falsifiable "
            "mathematical program rather than to generic thematic similarity."
        ),
    ]
    limitations = [
        _clean_text(
            f"The current run still has evidence_count={evidence_count}, so support is structural and explanatory, not evidential."
        ),
        _clean_text(
            f"There remain {unresolved_count} inconclusive hypotheses, so the frontier is not yet mathematically settled."
        ),
        _clean_text(
            "The novelty is therefore programmatic: new route decompositions, typed carriers, and missing lemmas, not validated new theorems."
        ),
    ]

    kb_ref = _kb_ref_from_artifacts_dir(artifacts_dir, expert)
    run_id = _first_nonempty(
        _ensure_dict(expert.get("metadata")).get("selected_run_id"),
        _ensure_dict(expert.get("metadata")).get("generated_utc"),
    )
    return {
        "metadata": {
            "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "kb_ref": kb_ref,
            "artifacts_dir": str(artifacts_dir),
            "source_run_id": run_id,
            "top_k": max(1, top_k),
            "evidence_count": evidence_count,
            "unresolved_hypothesis_count": unresolved_count,
        },
        "summary": {
            "top_direction_id": _clean_text(directions[0].get("bridge_id")) if directions else "",
            "next_best_direction_id": _clean_text(next_best.get("bridge_id")),
            "direction_count": len(directions),
        },
        "most_promising_directions": directions,
        "novelty_assessment": {
            "positive_evidence": [value for value in positive_evidence if value],
            "limitations": [value for value in limitations if value],
            "verdict": _clean_text(
                "There is real programmatic novelty in the sense of a new content-level bridge program: the framework "
                "isolates specific theorem-pair deltas, proposes typed intermediate carriers, and exposes missing route "
                "lemmas. There is not yet evidence of theorem-level novelty, because the decisive lemmas remain open and "
                "the run has not accumulated external or adversarial evidence."
            ),
        },
        "next_best_direction": next_best,
        "recommended_probe": {
            "hypothesis_id": _clean_text(probe.get("hypothesis_id")),
            "target_statement_id": _clean_text(probe.get("target_statement_id")),
            "priority": _safe_float(probe.get("priority")),
            "recommended_action": _clean_text(probe.get("recommended_action")),
            "reason": _first_nonempty(*_ensure_list(probe.get("reasons"))[:2]),
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    metadata = _ensure_dict(report.get("metadata"))
    novelty = _ensure_dict(report.get("novelty_assessment"))
    next_best = _ensure_dict(report.get("next_best_direction"))
    probe = _ensure_dict(report.get("recommended_probe"))

    lines = [
        "# Promising Directions Assessment",
        "",
        f"- Generated (UTC): {_clean_text(metadata.get('generated_utc'))}",
        f"- KB ref: {_clean_text(metadata.get('kb_ref'))}",
        f"- Source run: {_clean_text(metadata.get('source_run_id'))}",
        f"- Evidence count: {_safe_int(metadata.get('evidence_count'))}",
        f"- Unresolved hypotheses: {_safe_int(metadata.get('unresolved_hypothesis_count'))}",
        "",
        "## Executive Summary",
        "",
        _clean_text(novelty.get("verdict")),
        "",
        "## Most Promising Directions",
        "",
    ]

    for idx, direction in enumerate(_ensure_list(report.get("most_promising_directions")), start=1):
        direction = _ensure_dict(direction)
        lines.extend(
            [
                f"### {idx}. {_clean_text(direction.get('title'))}",
                "",
                f"- Bridge ID: {_clean_text(direction.get('bridge_id'))}",
                f"- Type: {_clean_text(direction.get('bridge_type'))}",
                f"- Priority: {_safe_float(direction.get('priority')):.3f}",
                f"- Route: {_clean_text(direction.get('source_statement_id'))} -> {_clean_text(direction.get('target_statement_id'))}",
                f"- Abstraction: {_clean_text(direction.get('abstraction_label'))}",
                f"- Carrier: {_clean_text(direction.get('carrier_kind'))}",
                f"- Invariant: {_clean_text(direction.get('preserved_invariant'))}",
                f"- Route synopsis: {_clean_text(direction.get('route_synopsis'))}",
                "",
                "#### Why It Is Promising",
                "",
            ]
        )
        lines.extend(f"- {point}" for point in _ensure_list(direction.get("promising_points")))
        lines.extend(
            [
                "",
                "#### Content-wise Novelty Argument",
                "",
            ]
        )
        lines.extend(f"- {point}" for point in _ensure_list(direction.get("novelty_points")))
        lines.extend(
            [
                "",
                "#### Key Obligations",
                "",
            ]
        )
        lines.extend(f"- {point}" for point in _ensure_list(direction.get("proof_obligations"))[:4])
        lines.extend(
            [
                "",
                "#### Main Risks",
                "",
            ]
        )
        lines.extend(f"- {point}" for point in _ensure_list(direction.get("risk_points")))
        lines.extend(
            [
                "",
                "#### Expert Actions",
                "",
            ]
        )
        lines.extend(f"- {point}" for point in _ensure_list(direction.get("expert_actions")))
        lines.append("")

    lines.extend(
        [
            "## Novelty Assessment",
            "",
            "### Positive Evidence",
            "",
        ]
    )
    lines.extend(f"- {point}" for point in _ensure_list(novelty.get("positive_evidence")))
    lines.extend(
        [
            "",
            "### Limits",
            "",
        ]
    )
    lines.extend(f"- {point}" for point in _ensure_list(novelty.get("limitations")))
    lines.extend(
        [
            "",
            "### Verdict",
            "",
            _clean_text(novelty.get("verdict")),
            "",
            "## Next Best Direction To Explore",
            "",
        ]
    )
    if next_best:
        lines.extend(
            [
                f"- Bridge ID: {_clean_text(next_best.get('bridge_id'))}",
                f"- Title: {_clean_text(next_best.get('title'))}",
                f"- Route: {_clean_text(next_best.get('source_statement_id'))} -> {_clean_text(next_best.get('target_statement_id'))}",
                f"- Assessment: {_clean_text(next_best.get('assessment'))}",
                f"- Missing route lemma: {_clean_text(next_best.get('missing_route_lemma'))}",
                "",
            ]
        )
    if probe:
        lines.extend(
            [
                "## Recommended Probe",
                "",
                f"- Hypothesis: {_clean_text(probe.get('hypothesis_id'))}",
                f"- Target statement: {_clean_text(probe.get('target_statement_id'))}",
                f"- Priority: {_safe_float(probe.get('priority')):.3f}",
                f"- Recommended action: {_clean_text(probe.get('recommended_action'))}",
                f"- Reason: {_clean_text(probe.get('reason'))}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_tex(report: dict[str, Any]) -> str:
    metadata = _ensure_dict(report.get("metadata"))
    novelty = _ensure_dict(report.get("novelty_assessment"))
    directions = [_ensure_dict(value) for value in _ensure_list(report.get("most_promising_directions"))]
    next_best = _ensure_dict(report.get("next_best_direction"))
    probe = _ensure_dict(report.get("recommended_probe"))

    direction_blocks: list[str] = []
    for idx, direction in enumerate(directions, start=1):
        section = [
            rf"\subsection{{{idx}. {_latex_escape(direction.get('title'))}}}",
            r"\begin{itemize}[leftmargin=*,itemsep=0.25em]",
            rf"\item Bridge ID: \texttt{{{_latex_escape(direction.get('bridge_id'))}}}",
            rf"\item Type: {_latex_escape(direction.get('bridge_type'))}",
            rf"\item Priority: {_safe_float(direction.get('priority')):.3f}",
            rf"\item Route: \texttt{{{_latex_escape(direction.get('source_statement_id'))}}} $\rightarrow$ \texttt{{{_latex_escape(direction.get('target_statement_id'))}}}",
            rf"\item Abstraction: {_latex_escape(direction.get('abstraction_label'))}",
            rf"\item Carrier: {_latex_escape(direction.get('carrier_kind'))}",
            rf"\item Invariant: {_latex_escape(direction.get('preserved_invariant'))}",
            rf"\item Route synopsis: {_latex_escape(direction.get('route_synopsis'))}",
            r"\end{itemize}",
            r"\paragraph{Why It Is Promising}",
            r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
        ]
        section.extend(rf"\item {_latex_escape(point)}" for point in _ensure_list(direction.get("promising_points")))
        section.extend(
            [
                r"\end{itemize}",
                r"\paragraph{Content-wise Novelty Argument}",
                r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
            ]
        )
        section.extend(rf"\item {_latex_escape(point)}" for point in _ensure_list(direction.get("novelty_points")))
        section.extend(
            [
                r"\end{itemize}",
                r"\paragraph{Key Obligations}",
                r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
            ]
        )
        section.extend(rf"\item {_latex_escape(point)}" for point in _ensure_list(direction.get("proof_obligations"))[:4])
        section.extend(
            [
                r"\end{itemize}",
                r"\paragraph{Main Risks}",
                r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
            ]
        )
        section.extend(rf"\item {_latex_escape(point)}" for point in _ensure_list(direction.get("risk_points")))
        section.extend(
            [
                r"\end{itemize}",
                r"\paragraph{Expert Actions}",
                r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
            ]
        )
        section.extend(rf"\item {_latex_escape(point)}" for point in _ensure_list(direction.get("expert_actions")))
        section.append(r"\end{itemize}")
        direction_blocks.append("\n".join(section))

    positive_evidence = "\n".join(
        rf"\item {_latex_escape(point)}" for point in _ensure_list(novelty.get("positive_evidence"))
    )
    limitations = "\n".join(
        rf"\item {_latex_escape(point)}" for point in _ensure_list(novelty.get("limitations"))
    )
    next_best_block = ""
    if next_best:
        next_best_block = "\n".join(
            [
                r"\section{Next Best Direction To Explore}",
                r"\begin{itemize}[leftmargin=*,itemsep=0.25em]",
                rf"\item Bridge ID: \texttt{{{_latex_escape(next_best.get('bridge_id'))}}}",
                rf"\item Title: {_latex_escape(next_best.get('title'))}",
                rf"\item Route: \texttt{{{_latex_escape(next_best.get('source_statement_id'))}}} $\rightarrow$ \texttt{{{_latex_escape(next_best.get('target_statement_id'))}}}",
                rf"\item Assessment: {_latex_escape(next_best.get('assessment'))}",
                rf"\item Missing route lemma: {_latex_escape(next_best.get('missing_route_lemma'))}",
                r"\end{itemize}",
            ]
        )
    probe_block = ""
    if probe:
        probe_block = "\n".join(
            [
                r"\section{Recommended Probe}",
                r"\begin{itemize}[leftmargin=*,itemsep=0.25em]",
                rf"\item Hypothesis: \texttt{{{_latex_escape(probe.get('hypothesis_id'))}}}",
                rf"\item Target statement: \texttt{{{_latex_escape(probe.get('target_statement_id'))}}}",
                rf"\item Priority: {_safe_float(probe.get('priority')):.3f}",
                rf"\item Recommended action: {_latex_escape(probe.get('recommended_action'))}",
                rf"\item Reason: {_latex_escape(probe.get('reason'))}",
                r"\end{itemize}",
            ]
        )

    return rf"""\documentclass[11pt]{{article}}

\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern}}
\usepackage{{amsmath,amssymb}}
\usepackage{{booktabs}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{tabularx}}
\usepackage{{xcolor}}

\hypersetup{{
  colorlinks=true,
  linkcolor=blue!50!black,
  urlcolor=blue!50!black,
  citecolor=blue!50!black,
  pdftitle={{Promising Directions Assessment for {_latex_escape(metadata.get('kb_ref'))}}}
}}

\title{{Promising Directions Assessment for \texttt{{{_latex_escape(metadata.get('kb_ref'))}}}}}
\author{{Neuro-symbolic AI Group\\Idiap Research Institute}}
\date{{March 16, 2026}}

\begin{{document}}
\maketitle

\begin{{abstract}}
This report identifies the most promising mathematical directions currently surfaced by the framework for
\texttt{{{_latex_escape(metadata.get('kb_ref'))}}}. The assessment is content-first: each route is described by
its theorem pair, typed bridge object, preserved invariant, missing route lemma, and failure logic. The novelty claim
is assessed at the level of mathematical program rather than theorem announcement. The conclusion is that the current
run contains real route-level novelty and a plausible discovery direction, but not a validated theorem-level discovery.
\end{{abstract}}

\section{{Run Context}}
\begin{{itemize}}[leftmargin=*,itemsep=0.25em]
\item Generated (UTC): {_latex_escape(metadata.get('generated_utc'))}
\item Source run: {_latex_escape(metadata.get('source_run_id'))}
\item Evidence count: {_safe_int(metadata.get('evidence_count'))}
\item Unresolved hypotheses: {_safe_int(metadata.get('unresolved_hypothesis_count'))}
\end{{itemize}}

\section{{Executive Summary}}
{_latex_escape(novelty.get('verdict'))}

\section{{Most Promising Directions}}
{chr(10).join(direction_blocks)}

\section{{Novelty Assessment}}
\subsection{{Positive Evidence}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
{positive_evidence}
\end{{itemize}}

\subsection{{Limits}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
{limitations}
\end{{itemize}}

\subsection{{Verdict}}
{_latex_escape(novelty.get('verdict'))}

{next_best_block}

{probe_block}

\end{{document}}
"""


def _candidate_engine_paths() -> list[Path]:
    roots = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64",
        Path(os.environ.get("PROGRAMFILES", "")) / "MiKTeX" / "miktex" / "bin" / "x64",
        Path.home() / "AppData" / "Local" / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64",
    ]
    return [path for path in roots if str(path)]


def _find_latex_engine(preferred: str = "auto") -> list[str]:
    candidates = ["xelatex", "pdflatex", "lualatex"] if preferred == "auto" else [preferred, "pdflatex", "xelatex", "lualatex"]
    seen: set[str] = set()
    ordered = [name for name in candidates if not (name in seen or seen.add(name))]
    for name in ordered:
        found = shutil.which(name)
        if found:
            return [found]
        for root in _candidate_engine_paths():
            path = root / f"{name}.exe"
            if path.exists():
                return [str(path)]
    raise FileNotFoundError("No LaTeX engine found. Checked xelatex/pdflatex/lualatex and common MiKTeX locations.")


def compile_pdf(tex_path: Path, pdf_path: Path, preferred_engine: str = "auto") -> Path:
    engine = _find_latex_engine(preferred_engine)
    workdir = tex_path.parent
    cmd = engine + ["-interaction=nonstopmode", "-halt-on-error", tex_path.name]
    for _ in range(2):
        result = subprocess.run(
            cmd,
            cwd=workdir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"LaTeX compilation failed with engine {engine[0]}:\n{result.stdout}\n{result.stderr}"
            )
    built_pdf = workdir / tex_path.with_suffix(".pdf").name
    if built_pdf != pdf_path:
        pdf_path.write_bytes(built_pdf.read_bytes())
    for suffix in (".aux", ".log", ".out", ".toc"):
        candidate = workdir / tex_path.with_suffix(suffix).name
        if candidate.exists():
            candidate.unlink()
    return pdf_path


def main() -> int:
    logger = ReasoningLogger("kb-promising-direction-assessor")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref> directory.")
    ap.add_argument("--expert-paper", default="", help="Optional expert-hypothesis-paper JSON path.")
    ap.add_argument("--hypothesis-eval", default="", help="Optional hypothesis-evaluation JSON path.")
    ap.add_argument("--output-json", default="", help="Output path for promising-directions-report JSON.")
    ap.add_argument("--output-md", default="", help="Output path for promising-directions-report Markdown.")
    ap.add_argument("--output-tex", default="", help="Output path for promising-directions-report TeX.")
    ap.add_argument("--output-pdf", default="", help="Output path for promising-directions-report PDF.")
    ap.add_argument("--top-k", type=int, default=3, help="Number of leading directions to include.")
    ap.add_argument("--latex-engine", default="auto", help="LaTeX engine preference: auto, xelatex, pdflatex, lualatex.")
    ap.add_argument(
        "--compile-pdf",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Compile the generated TeX to PDF.",
    )
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()

    expert_path = Path(args.expert_paper) if args.expert_paper else artifacts_dir / "expert-hypothesis-paper.json"
    if not expert_path.is_absolute():
        expert_path = (repo_root / expert_path).resolve()
    hypothesis_eval_path = Path(args.hypothesis_eval) if args.hypothesis_eval else artifacts_dir / "hypothesis-evaluation.json"
    if not hypothesis_eval_path.is_absolute():
        hypothesis_eval_path = (repo_root / hypothesis_eval_path).resolve()

    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "promising-directions-report.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "promising-directions-report.md"
    output_tex = Path(args.output_tex) if args.output_tex else artifacts_dir / "promising-directions-report.tex"
    output_pdf = Path(args.output_pdf) if args.output_pdf else artifacts_dir / "promising-directions-report.pdf"

    logger.step(
        "Parsed promising-directions-assessor arguments",
        "\n".join(
            [
                f"artifacts_dir={artifacts_dir}",
                f"expert_paper={expert_path}",
                f"hypothesis_eval={hypothesis_eval_path}",
                f"output_json={output_json}",
                f"output_md={output_md}",
                f"output_tex={output_tex}",
                f"output_pdf={output_pdf}",
                f"top_k={max(1, args.top_k)}",
                f"compile_pdf={args.compile_pdf}",
                f"latex_engine={args.latex_engine}",
            ]
        ),
        surface_focus="promising-directions-assessment",
        surface_stage="promising-directions-assessment",
    )

    if not expert_path.exists():
        raise FileNotFoundError(f"Expert paper JSON not found: {expert_path}")
    if not hypothesis_eval_path.exists():
        raise FileNotFoundError(f"Hypothesis evaluation JSON not found: {hypothesis_eval_path}")

    expert = _load_json(expert_path)
    hypothesis_eval = _load_json(hypothesis_eval_path)
    report = build_report(expert, hypothesis_eval, artifacts_dir=artifacts_dir, top_k=max(1, args.top_k))

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_tex.parent.mkdir(parents=True, exist_ok=True)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")
    output_tex.write_text(render_tex(report), encoding="utf-8")

    if args.compile_pdf:
        compile_pdf(output_tex, output_pdf, preferred_engine=args.latex_engine)

    logger.step(
        "Built promising-directions assessment",
        "\n".join(
            [
                f"direction_count={_safe_int(_ensure_dict(report.get('summary')).get('direction_count'))}",
                f"top_direction_id={_ensure_dict(report.get('summary')).get('top_direction_id', '')}",
                f"next_best_direction_id={_ensure_dict(report.get('summary')).get('next_best_direction_id', '')}",
            ]
        ),
        surface_focus="promising-directions-assessment",
        surface_stage="promising-directions-assessment",
        surface_metrics={
            "direction_count": _safe_int(_ensure_dict(report.get("summary")).get("direction_count")),
            "evidence_count": _safe_int(_ensure_dict(report.get("metadata")).get("evidence_count")),
            "unresolved_hypothesis_count": _safe_int(_ensure_dict(report.get("metadata")).get("unresolved_hypothesis_count")),
        },
        surface_taxonomy={"reasoning_types": ["promising-directions-assessment"]},
    )

    logger.add_output("promising_directions_report_json", output_json)
    logger.add_output("promising_directions_report_md", output_md)
    logger.add_output("promising_directions_report_tex", output_tex)
    if args.compile_pdf:
        logger.add_output("promising_directions_report_pdf", output_pdf)

    log_path = logger.finalize(
        "success",
        summary=(
            f"Generated promising-directions assessment with "
            f"{_safe_int(_ensure_dict(report.get('summary')).get('direction_count'))} leading directions."
        ),
    )
    print(f"[OK] Wrote promising directions JSON: {output_json}")
    print(f"[OK] Wrote promising directions Markdown: {output_md}")
    print(f"[OK] Wrote promising directions TeX: {output_tex}")
    if args.compile_pdf:
        print(f"[OK] Wrote promising directions PDF: {output_pdf}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
