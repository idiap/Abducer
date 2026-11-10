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

"""Generate an expert-facing macro-strategy report for the current proof plan."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import kb_ref_from_artifacts_dir
from proof_queue import load_proof_queue
from reasoning_log import ReasoningLogger

from generate_macro_proof_state_report import build_report as build_macro_proof_state
from generate_macro_proof_state_report import compile_pdf


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


def _reference_row(*, statement_id: Any, title: Any, role: str, detail: Any) -> dict[str, str]:
    return {
        "statement_id": _clean_text(statement_id),
        "title": _clean_text(title),
        "role": _clean_text(role),
        "detail": _clean_text(detail),
    }


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


def _load_or_build_macro_state(*, kb_path: Path, artifacts_dir: Path) -> dict[str, Any]:
    json_path = artifacts_dir / "macro-proof-state.json"
    if json_path.exists():
        return _load_json(json_path)
    return build_macro_proof_state(kb_path=kb_path, artifacts_dir=artifacts_dir)


def _leading_sketches(proof_sketches: dict[str, Any], bridge_id: str) -> list[dict[str, Any]]:
    rows = [
        row
        for row in _ensure_list(proof_sketches.get("proof_sketches"))
        if isinstance(row, dict) and _clean_text(row.get("bridge_id")) == bridge_id
    ]
    rows.sort(key=lambda row: _safe_float(row.get("sketch_score")), reverse=True)
    return rows


def _find_obligation(sketch: dict[str, Any], *kinds: str) -> str:
    wanted = {kind.strip().lower() for kind in kinds if kind.strip()}
    for row in _ensure_list(sketch.get("proof_obligations")):
        if not isinstance(row, dict):
            continue
        kind = _clean_text(row.get("kind")).lower()
        if kind in wanted:
            return _first_nonempty(row.get("requirement"), row.get("claim_template"))
    return ""


def _find_obligation_by_text(sketch: dict[str, Any], needle: str) -> str:
    needle_s = needle.lower()
    for row in _ensure_list(sketch.get("proof_obligations")):
        if not isinstance(row, dict):
            continue
        requirement = _first_nonempty(row.get("requirement"), row.get("claim_template"))
        if needle_s in requirement.lower():
            return requirement
    return ""


def build_strategy_report(*, kb_path: Path, artifacts_dir: Path) -> dict[str, Any]:
    kb_ref = kb_ref_from_artifacts_dir(artifacts_dir)
    macro_state = _load_or_build_macro_state(kb_path=kb_path, artifacts_dir=artifacts_dir)
    proof_sketches = _load_json(artifacts_dir / "proof-sketches.json")
    proof_queue = load_proof_queue(artifacts_dir / "proof-queue.json", kb_ref=kb_ref)

    main = _ensure_dict(macro_state.get("main_conjecture"))
    leading = _ensure_dict(macro_state.get("leading_route"))
    supporting = [row for row in _ensure_list(macro_state.get("supporting_routes")) if isinstance(row, dict)]
    status = _ensure_dict(macro_state.get("status_assessment"))
    bridge_id = _clean_text(leading.get("bridge_id"))
    sketches = _leading_sketches(proof_sketches, bridge_id)
    primary_sketch = _ensure_dict(sketches[0] if sketches else {})

    operationalizations = []
    seen_objects: set[str] = set()
    for sketch in sketches:
        obj = _first_nonempty(sketch.get("conjectured_object"), sketch.get("title"))
        seen_objects.add(obj)
        operationalizations.append(
            {
                "sketch_id": _clean_text(sketch.get("sketch_id")),
                "score": _safe_float(sketch.get("sketch_score")),
                "object": obj,
                "carrier_kind": _clean_text(sketch.get("carrier_kind")),
                "family": _clean_text(sketch.get("proof_strategy_family")),
                "route_lemma": _first_nonempty(
                    _ensure_dict(sketch.get("statement_delta")).get("missing_witness_or_transport"),
                    leading.get("missing_route_lemma"),
                ),
            }
        )

    established = [
        {
            "title": "Final grounding to the main conjecture is already available.",
            "detail": f"The KB already supplies the implication `{main.get('route_target_claim', '')}` => `{main.get('core_claim', '')}` via `{main.get('grounding_statement_id', '')}`.",
        },
        {
            "title": "The proof target has been reduced to a sharper nonuniform statement.",
            "detail": f"The current macro-plan is to prove `{main.get('route_target_claim', '')}` and then conclude `{main.get('core_claim', '')}`.",
        },
        {
            "title": "A leading theorem pair and invariant have already been isolated.",
            "detail": f"The leading route is `{bridge_id}` with invariant `{leading.get('invariant', '')}` and target consequence `{leading.get('target_claim_focus', '')}`.",
        },
    ]
    if operationalizations:
        established.append(
            {
                "title": "At least one typed bridge operationalization exists.",
                "detail": f"The leading bridge currently has {len(operationalizations)} operationalization(s): {', '.join(item['object'] for item in operationalizations)}.",
            }
        )

    missing_for_completion: list[dict[str, str]] = []
    if len(seen_objects) > 1:
        missing_for_completion.append(
            {
                "kind": "representation-alignment",
                "title": "Choose or prove equivalence between the live bridge operationalizations.",
                "why": "The leading bridge currently has more than one concrete realization. A complete proof needs either one fixed carrier or a theorem proving that the two carriers are interchangeable for the route.",
                "completion_condition": f"Show that `{operationalizations[0]['object']}` and `{operationalizations[1]['object']}` are equivalent for the route, or commit to one and restate all downstream lemmas in that representation.",
            }
        )

    source_realization = _first_nonempty(
        _find_obligation(primary_sketch, "antecedent-realization"),
        _find_obligation_by_text(primary_sketch, "source-to-object"),
        _first_nonempty(*_ensure_list(leading.get("proof_obligations"))),
    )
    transport = _first_nonempty(
        _find_obligation(primary_sketch, "invariant-preservation", "transport-claim"),
        _find_obligation_by_text(primary_sketch, "transport claim"),
    )
    route_lemma = _first_nonempty(
        _find_obligation(primary_sketch, "operationalizability"),
        leading.get("missing_route_lemma"),
    )
    payoff = _first_nonempty(
        _find_obligation(primary_sketch, "consequence-forcing", "payoff-claim"),
        _find_obligation_by_text(primary_sketch, "payoff claim"),
    )
    threshold_control = _find_obligation_by_text(primary_sketch, "threshold control")

    core_missing_rows = [
        ("source-realization", "Realize the source-side lower-bound content inside the chosen bridge object.", source_realization),
        ("invariant-transport", "Prove that the bridge object preserves the named invariant along the route.", transport),
        ("route-lemma", "Discharge the route-specific magnification lemma.", route_lemma),
        ("payoff", "Convert the realized bridge object into the target nonuniform consequence.", payoff),
    ]
    for kind, title, detail in core_missing_rows:
        if detail:
            missing_for_completion.append(
                {
                    "kind": kind,
                    "title": title,
                    "why": "Without this statement, the current proof plan remains conditional rather than complete.",
                    "completion_condition": detail,
                }
            )
    if threshold_control:
        missing_for_completion.append(
            {
                "kind": "threshold-control",
                "title": "Make the threshold regime mathematically explicit.",
                "why": "The surrogate operationalization still needs theorem-level control of the threshold at which mild lower bounds magnify into the target payoff.",
                "completion_condition": threshold_control,
            }
        )

    epistemic_gaps = [
        {
            "title": "No adversarial evidence has yet been accumulated.",
            "detail": f"The current run still records `evidence_count = {_safe_int(status.get('evidence_count'))}`, so the route is structurally articulated but not externally stress-tested.",
        },
        {
            "title": "No proof item in the queue is resolved yet.",
            "detail": f"The current proof queue has `{_safe_int(_ensure_dict(proof_queue.get('metadata')).get('pending_count'))}` pending items and no completed proof attempts.",
        },
    ]

    completion_checklist = [
        {
            "status": "established",
            "title": "Reduction from `NP not in P/poly` to `P != NP`.",
            "detail": main.get("grounding_implication", ""),
        },
        {
            "status": "partial",
            "title": "Leading bridge object fixed and operationalized.",
            "detail": "A typed object exists, but the route still has multiple operationalizations." if len(seen_objects) > 1 else "A typed object exists for the leading route.",
        },
        {
            "status": "open",
            "title": "Source-to-object realization theorem.",
            "detail": source_realization,
        },
        {
            "status": "open",
            "title": "Invariant-preservation transport theorem.",
            "detail": transport,
        },
        {
            "status": "open",
            "title": "Route-specific magnification lemma.",
            "detail": route_lemma,
        },
        {
            "status": "open",
            "title": "Payoff theorem yielding the nonuniform separation target.",
            "detail": payoff,
        },
    ]
    if threshold_control:
        completion_checklist.append(
            {
                "status": "open",
                "title": "Threshold-control theorem for the surrogate operationalization.",
                "detail": threshold_control,
            }
        )

    fallback_routes = []
    for row in supporting[:2]:
        fallback_routes.append(
            {
                "bridge_id": _clean_text(row.get("bridge_id")),
                "route_synopsis": _clean_text(row.get("route_synopsis")),
                "why_it_matters": _clean_text(row.get("missing_route_lemma")),
            }
        )

    queue_frontier = [
        {
            "queue_id": _clean_text(row.get("queue_id")),
            "title": _clean_text(row.get("title")),
            "priority": _safe_float(row.get("priority")),
        }
        for row in _ensure_list(proof_queue.get("entries"))[:3]
        if isinstance(row, dict)
    ]

    narrative = {
        "abstract": (
            "This report should be read as a strategic mathematical note rather than as a project-management checklist. "
            "Its purpose is to explain why the current route does not yet close the main conjecture, what theorem package is still missing, and which nearby routes remain mathematically meaningful."
        ),
        "bottleneck": (
            "The decisive bottleneck is the leading magnification bridge. "
            "The final reduction from the nonuniform target to the main conjecture is already available, so the strategic question is whether the bridge object can be fixed and the source-realization, transport, route, and payoff lemmas can be discharged."
        ),
        "subresult_value": (
            "Several missing items would already count as mathematically meaningful subresults even if the main conjecture remained open, especially a clean source-to-object realization theorem, a transport theorem for the invariant, or a barrier result ruling out one of the operationalizations."
        ),
    }

    references = _dedupe_references(
        [
            _reference_row(
                statement_id=main.get("grounding_statement_id"),
                title=main.get("grounding_statement_title"),
                role="Grounding implication",
                detail=main.get("grounding_implication"),
            ),
            _reference_row(
                statement_id=leading.get("source_statement_id"),
                title="Leading-route source statement",
                role="Leading-route source",
                detail=leading.get("source_excerpt"),
            ),
            _reference_row(
                statement_id=leading.get("target_statement_id"),
                title="Leading-route target statement",
                role="Leading-route target",
                detail=leading.get("target_excerpt"),
            ),
        ]
        + [
            _reference_row(
                statement_id=row.get("target_statement_id"),
                title=row.get("bridge_id"),
                role="Fallback-route target",
                detail=row.get("route_synopsis"),
            )
            for row in supporting[:2]
        ]
    )

    return {
        "metadata": {
            "kb_ref": kb_ref,
            "bridge_id": bridge_id,
        },
        "narrative": narrative,
        "summary_answer": {
            "headline": "The proof is not blocked at the final reduction to P versus NP; it is blocked at the leading magnification bridge.",
            "detail": "To complete the proof on the current macro-strategy, one must fix a single bridge operationalization and then prove the source-realization, invariant-transport, route, and payoff lemmas that yield `NP not in P/poly`. Once that theorem is in hand, the final implication to `P != NP` is already available in the KB.",
        },
        "main_conjecture": main,
        "leading_route": leading,
        "operationalizations": operationalizations,
        "established_components": established,
        "missing_for_completion": missing_for_completion,
        "completion_checklist": completion_checklist,
        "epistemic_gaps": epistemic_gaps,
        "fallback_routes": fallback_routes,
        "queue_frontier": queue_frontier,
        "references": references,
    }


def render_markdown(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    narrative = _ensure_dict(report.get("narrative"))
    main = _ensure_dict(report.get("main_conjecture"))
    leading = _ensure_dict(report.get("leading_route"))
    answer = _ensure_dict(report.get("summary_answer"))
    operationalizations = [row for row in _ensure_list(report.get("operationalizations")) if isinstance(row, dict)]
    established = [row for row in _ensure_list(report.get("established_components")) if isinstance(row, dict)]
    missing = [row for row in _ensure_list(report.get("missing_for_completion")) if isinstance(row, dict)]
    checklist = [row for row in _ensure_list(report.get("completion_checklist")) if isinstance(row, dict)]
    epistemic = [row for row in _ensure_list(report.get("epistemic_gaps")) if isinstance(row, dict)]
    fallback = [row for row in _ensure_list(report.get("fallback_routes")) if isinstance(row, dict)]
    frontier = [row for row in _ensure_list(report.get("queue_frontier")) if isinstance(row, dict)]
    references = [row for row in _ensure_list(report.get("references")) if isinstance(row, dict)]

    lines = [
        f"# Macro-Strategy Report for {meta.get('kb_ref', '')}",
        "",
        "## Abstract",
        "",
        narrative.get("abstract", ""),
        "",
        "## Executive Answer",
        "",
        answer.get("headline", ""),
        answer.get("detail", ""),
        "",
        "## Strategic Bottleneck",
        "",
        narrative.get("bottleneck", ""),
        "",
        "## Current Reduction",
        "",
        f"- Main conjecture: `{main.get('core_claim', '')}`",
        f"- Stronger route target: `{main.get('route_target_claim', '')}`",
        f"- Grounding implication already available: {main.get('grounding_implication', '')}",
        f"- Leading bridge: `{meta.get('bridge_id', '')}`",
        f"- Leading route synopsis: {leading.get('route_synopsis', '')}",
        "",
        "## What Is Already Established",
        "",
    ]
    for row in established:
        lines.extend([f"- {row.get('title', '')}", f"  {row.get('detail', '')}"])

    lines.extend(["", "## Leading Operationalizations", ""])
    for row in operationalizations:
        lines.extend(
            [
                f"### {row.get('sketch_id', 'sketch')}",
                "",
                f"- Object: {row.get('object', '')}",
                f"- Score: {row.get('score', 0.0):.3f}",
                f"- Carrier kind: {row.get('carrier_kind', '')}",
                f"- Family: {row.get('family', '')}",
                f"- Route lemma under this operationalization: {row.get('route_lemma', '')}",
                "",
            ]
        )

    lines.extend(["## What Is Missing For Completion", ""])
    for row in missing:
        lines.extend(
            [
                f"### {row.get('title', '')}",
                "",
                f"- Why it is missing: {row.get('why', '')}",
                f"- What completion requires: {row.get('completion_condition', '')}",
                "",
            ]
        )

    lines.extend(["## Completion Checklist", ""])
    for row in checklist:
        lines.extend(
            [
                f"- [{row.get('status', '').upper()}] {row.get('title', '')}",
                f"  {row.get('detail', '')}",
            ]
        )

    lines.extend(["", "## Epistemic Gaps", ""])
    for row in epistemic:
        lines.extend([f"- {row.get('title', '')}", f"  {row.get('detail', '')}"])

    lines.extend(["", "## Subresult Perspective", ""])
    lines.extend([narrative.get("subresult_value", ""), ""])

    lines.extend(["", "## Fallback Routes", ""])
    for row in fallback:
        lines.extend(
            [
                f"- `{row.get('bridge_id', '')}`: {row.get('route_synopsis', '')}",
                f"  Missing route lemma: {row.get('why_it_matters', '')}",
            ]
        )

    lines.extend(["", "## Proof Frontier", ""])
    for row in frontier:
        lines.extend([f"- `{row.get('queue_id', '')}` ({row.get('priority', 0.0):.3f}): {row.get('title', '')}"])

    lines.extend(["", "## Relevant References", ""])
    for row in references:
        lines.extend(
            [
                f"- [{row.get('role', 'Reference')}] `{row.get('statement_id', '')}` {row.get('title', '')}".rstrip(),
                f"  {row.get('detail', '')}",
            ]
        )
    if not references:
        lines.extend(["- No references recorded.", ""])

    return "\n".join(lines).rstrip() + "\n"


def render_tex(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    narrative = _ensure_dict(report.get("narrative"))
    main = _ensure_dict(report.get("main_conjecture"))
    leading = _ensure_dict(report.get("leading_route"))
    answer = _ensure_dict(report.get("summary_answer"))
    operationalizations = [row for row in _ensure_list(report.get("operationalizations")) if isinstance(row, dict)]
    established = [row for row in _ensure_list(report.get("established_components")) if isinstance(row, dict)]
    missing = [row for row in _ensure_list(report.get("missing_for_completion")) if isinstance(row, dict)]
    checklist = [row for row in _ensure_list(report.get("completion_checklist")) if isinstance(row, dict)]
    epistemic = [row for row in _ensure_list(report.get("epistemic_gaps")) if isinstance(row, dict)]
    fallback = [row for row in _ensure_list(report.get("fallback_routes")) if isinstance(row, dict)]
    frontier = [row for row in _ensure_list(report.get("queue_frontier")) if isinstance(row, dict)]
    references = [row for row in _ensure_list(report.get("references")) if isinstance(row, dict)]

    def _render_itemize(rows: list[str]) -> str:
        items = [rf"\item {_latex_escape(row)}" for row in rows if _clean_text(row)]
        if not items:
            return "No entries recorded."
        return "\n".join([r"\begin{itemize}[leftmargin=*,itemsep=0.2em]", *items, r"\end{itemize}"])

    operationalizations_block = "\n".join(
        [
            "\n".join(
                [
                    rf"\subsection*{{{_latex_escape(row.get('sketch_id'))}}}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    rf"\item Object: {_latex_escape(row.get('object'))}",
                    rf"\item Score: {_safe_float(row.get('score')):.3f}",
                    rf"\item Carrier kind: {_latex_escape(row.get('carrier_kind'))}",
                    rf"\item Family: {_latex_escape(row.get('family'))}",
                    rf"\item Route lemma under this operationalization: {_latex_escape(row.get('route_lemma'))}",
                    r"\end{itemize}",
                ]
            )
            for row in operationalizations
        ]
    ) or "No operationalizations recorded."

    missing_block = "\n".join(
        [
            "\n".join(
                [
                    rf"\subsection*{{{_latex_escape(row.get('title'))}}}",
                    rf"\textbf{{Why it is missing.}} {_latex_escape(row.get('why'))}",
                    "",
                    rf"\textbf{{What completion requires.}} {_latex_escape(row.get('completion_condition'))}",
                ]
            )
            for row in missing
        ]
    ) or "No missing items recorded."

    references_block = _render_itemize(
        [
            f"[{_clean_text(row.get('role'))}] {_clean_text(row.get('statement_id'))}: {_clean_text(row.get('title'))}. {_clean_text(row.get('detail'))}"
            for row in references
        ]
    )

    report_date = "March 17, 2026"
    return rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}

\title{{Macro-Strategy Report for {_latex_escape(meta.get('kb_ref'))}}}
\author{{Abducer Macro-Proof Paper Writer}}
\date{{{report_date}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
{_latex_escape(narrative.get('abstract'))}
\end{{abstract}}

\section{{Executive Answer}}
{_latex_escape(answer.get('headline'))} {_latex_escape(answer.get('detail'))}

\section{{Strategic Bottleneck}}
{_latex_escape(narrative.get('bottleneck'))}

\section{{Current Reduction}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
\item Main conjecture: {_latex_escape(main.get('core_claim'))}
\item Stronger route target: {_latex_escape(main.get('route_target_claim'))}
\item Grounding implication: {_latex_escape(main.get('grounding_implication'))}
\item Leading bridge: \texttt{{{_latex_escape(meta.get('bridge_id'))}}}
\item Leading route synopsis: {_latex_escape(leading.get('route_synopsis'))}
\end{{itemize}}

\section{{What Is Already Established}}
{_render_itemize([_first_nonempty(row.get('title'), '') + " " + _first_nonempty(row.get('detail'), '') for row in established])}

\section{{Leading Operationalizations}}
{operationalizations_block}

\section{{What Is Missing For Completion}}
{missing_block}

\section{{Completion Checklist}}
{_render_itemize([f"[{_clean_text(row.get('status')).upper()}] {_clean_text(row.get('title'))}: {_clean_text(row.get('detail'))}" for row in checklist])}

\section{{Epistemic Gaps}}
{_render_itemize([_first_nonempty(row.get('title'), '') + " " + _first_nonempty(row.get('detail'), '') for row in epistemic])}

\section{{Subresult Perspective}}
{_latex_escape(narrative.get('subresult_value'))}

\section{{Fallback Routes}}
{_render_itemize([f"{_clean_text(row.get('bridge_id'))}: {_clean_text(row.get('route_synopsis'))} Missing route lemma: {_clean_text(row.get('why_it_matters'))}" for row in fallback])}

\section{{Proof Frontier}}
{_render_itemize([f"{_clean_text(row.get('queue_id'))} ({_safe_float(row.get('priority')):.3f}): {_clean_text(row.get('title'))}" for row in frontier])}

\section{{Relevant References}}
{references_block}

\end{{document}}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kb", required=True, help="Path to the KB markdown file.")
    parser.add_argument("--artifacts-dir", required=True, help="Artifacts directory for the target problem.")
    parser.add_argument("--no-pdf", action="store_true", help="Skip LaTeX compilation.")
    parser.add_argument("--preferred-engine", default="auto", help="LaTeX engine preference.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[4]
    kb_path = Path(args.kb).resolve()
    artifacts_dir = Path(args.artifacts_dir).resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    logger = ReasoningLogger("kb-macro-strategy-report", repo_root=repo_root)

    logger.step(
        "Loaded macro-strategy inputs.",
        details=f"KB: {kb_path}\nArtifacts: {artifacts_dir}",
        surface_kind="evidence_loading",
        surface_focus="macro-strategy",
    )
    report = build_strategy_report(kb_path=kb_path, artifacts_dir=artifacts_dir)
    logger.step(
        "Built macro-strategy report payload.",
        details=(
            f"Leading bridge: {_ensure_dict(report.get('metadata')).get('bridge_id', '')}\n"
            f"Missing items: {len(_ensure_list(report.get('missing_for_completion')))}"
        ),
        surface_kind="artifact_synthesis",
        surface_focus="proof completion gaps",
    )

    json_path = artifacts_dir / "macro-strategy-report.json"
    md_path = artifacts_dir / "macro-strategy-report.md"
    tex_path = artifacts_dir / "macro-strategy-report.tex"
    pdf_path = artifacts_dir / "macro-strategy-report.pdf"

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    tex_path.write_text(render_tex(report), encoding="utf-8")
    logger.add_output("macro-strategy-report.json", json_path)
    logger.add_output("macro-strategy-report.md", md_path)
    logger.add_output("macro-strategy-report.tex", tex_path)

    if not args.no_pdf:
        compile_pdf(tex_path, pdf_path, preferred_engine=args.preferred_engine)
        logger.add_output("macro-strategy-report.pdf", pdf_path)

    logger.finalize(
        "completed",
        summary=(
            f"Generated macro-strategy report for {_ensure_dict(report.get('metadata')).get('kb_ref', '')} "
            f"with leading bridge {_ensure_dict(report.get('metadata')).get('bridge_id', '')}."
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
