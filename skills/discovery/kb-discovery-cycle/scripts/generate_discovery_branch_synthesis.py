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

"""Synthesize completed discovery-branch executions into a consolidated frontier report."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
_PROVE_SCRIPT_DIR = Path(__file__).resolve().parents[3] / "discovery" / "kb-prove-cycle" / "scripts"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))
if str(_PROVE_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_PROVE_SCRIPT_DIR))

from execute_discovery_branches import discovery_execution_paths
from generate_proof_queue_report import compile_pdf
from kb_context import canonical_artifacts_dir
from kb_context import kb_ref_from_artifacts_dir
from proof_queue import load_proof_queue
from proof_queue import proof_queue_paths
from reasoning_log import ReasoningLogger


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _normalize_target_id(value: Any) -> str:
    return _clean_text(value).lower().replace("_", "-").replace(" ", "-")


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
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


def _branch_queue_paths(artifacts_dir: Path) -> tuple[Path, Path]:
    return artifacts_dir / "discovery-branch-queue.json", artifacts_dir / "discovery-branch-queue.md"


def _synthesis_paths(artifacts_dir: Path) -> tuple[Path, Path, Path, Path]:
    return (
        artifacts_dir / "discovery-branch-synthesis.json",
        artifacts_dir / "discovery-branch-synthesis.md",
        artifacts_dir / "discovery-branch-synthesis.tex",
        artifacts_dir / "discovery-branch-synthesis.pdf",
    )


def _execution_reports(index: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [row for row in _ensure_list(index.get("executions")) if isinstance(row, dict)]
    reports: list[dict[str, Any]] = []
    for row in rows:
        report = _load_json(Path(str(row.get("artifact_json", "")).strip()))
        if report:
            reports.append(report)
    return reports


def _promotion_mode(target_id: str, *, report: dict[str, Any]) -> str:
    state_delta = _ensure_dict(_ensure_dict(report.get("execution")).get("state_delta"))
    if int(state_delta.get("promotable_theorem_count", 0) or 0) <= 0:
        return "discovery-candidate"
    if _normalize_target_id(target_id) in {
        "realization",
        "transport",
        "alignment",
        "explicitness",
        "semantic-bridge",
        "constructive-instantiation",
        "barrier-aware-transfer",
    }:
        return "prove-candidate"
    return "discovery-candidate"


def _agenda_bucket(mode: str) -> str:
    return "ready_for_prove" if _clean_text(mode) == "prove-candidate" else "ready_for_discovery"


def _headline_for_report(report: dict[str, Any]) -> str:
    branch = _ensure_dict(report.get("branch"))
    execution = _ensure_dict(report.get("execution"))
    theorem_candidates = [row for row in _ensure_list(execution.get("theorem_candidates")) if isinstance(row, dict)]
    concrete = [
        row
        for row in theorem_candidates
        if _clean_text(row.get("concretization_status")) == "concrete"
    ]
    if concrete:
        return _clean_text(concrete[0].get("statement")) or _clean_text(concrete[0].get("title"))
    target_id = _normalize_target_id(branch.get("target_id"))
    claims = [_clean_text(row) for row in _ensure_list(execution.get("candidate_claims")) if _clean_text(row)]
    if target_id == "transport":
        return claims[0] if claims else "Prove the formula-size transport theorem preserving the MCSP route invariant."
    if target_id == "alignment":
        return claims[0] if claims else "Prove the alignment theorem from the MCSP carrier to the general magnification object class."
    if target_id == "explicitness":
        return claims[0] if claims else "Upgrade the PIT semantic object into an explicit generator or certificate family."
    if target_id == "semantic-bridge":
        return claims[0] if claims else "Bridge the Cook-Reckhow definitional object to the NP = coNP characterization."
    if target_id == "constructive-instantiation":
        return claims[0] if claims else "Construct explicit natural instances from the abstract NP-complete schema."
    if target_id == "barrier-aware-transfer":
        return claims[0] if claims else "Either construct a locality-preserving gadget family or prove an impossibility theorem."
    if claims:
        return claims[0]
    return _clean_text(branch.get("minimal_theorem_shape")) or _clean_text(branch.get("required_move"))


def build_report(*, artifacts_dir: Path, kb_ref: str, repo_root: Path | None = None) -> dict[str, Any]:
    repo_root = (repo_root or Path(__file__).resolve().parents[4]).resolve()
    branch_json, _ = _branch_queue_paths(artifacts_dir)
    execution_json, _ = discovery_execution_paths(artifacts_dir)
    branch_state = _load_json(branch_json)
    execution_index = _load_json(execution_json)
    queue_json, _ = proof_queue_paths(repo_root, kb_ref)
    proof_queue = load_proof_queue(queue_json, kb_ref=kb_ref)

    branches = [row for row in _ensure_list(branch_state.get("branches")) if isinstance(row, dict)]
    reports = _execution_reports(execution_index)

    branch_by_id = {_clean_text(row.get("branch_id")): row for row in branches}
    family_counter: Counter[str] = Counter()
    obstruction_counter: Counter[str] = Counter()
    mathlib_counter: Counter[str] = Counter()

    for row in branches:
        if _clean_text(row.get("status")).lower() != "completed":
            continue
        for family in _ensure_list(row.get("linked_breakthrough_families")):
            text = _clean_text(family)
            if text:
                family_counter[text] += 1
        for obstruction in _ensure_list(row.get("linked_obstruction_classes")):
            text = _clean_text(obstruction)
            if text:
                obstruction_counter[text] += 1
    for report in reports:
        frontier = _ensure_dict(report.get("local_frontier"))
        for hit in _ensure_list(frontier.get("mathlib_hits")):
            title = _clean_text(_ensure_dict(hit).get("title"))
            if title:
                mathlib_counter[title] += 1

    programmes: list[dict[str, Any]] = []
    for report in reports:
        branch = _ensure_dict(report.get("branch"))
        execution = _ensure_dict(report.get("execution"))
        branch_id = _clean_text(_ensure_dict(report.get("metadata")).get("branch_id"))
        target_id = _clean_text(branch.get("target_id"))
        state_delta = _ensure_dict(execution.get("state_delta"))
        theorem_candidates = [row for row in _ensure_list(execution.get("theorem_candidates")) if isinstance(row, dict)]
        concrete_theorem_candidates = [
            row for row in theorem_candidates if _clean_text(row.get("concretization_status")) == "concrete"
        ]
        mode = _promotion_mode(target_id, report=report)
        programmes.append(
            {
                "branch_id": branch_id,
                "target_id": target_id,
                "target_label": _clean_text(branch.get("target_label")),
                "mode": mode,
                "agenda_bucket": _agenda_bucket(mode),
                "routing_priority": _safe_float(branch.get("routing_priority")),
                "headline": _headline_for_report(report),
                "rationale": _clean_text(branch.get("required_move")) or _clean_text(execution.get("summary")),
                "linked_queue_count": int(_ensure_dict(report.get("local_frontier")).get("linked_queue_count", 0) or 0),
                "execution_status": _clean_text(_ensure_dict(report.get("metadata")).get("status")),
                "state_delta_kind": _clean_text(state_delta.get("delta_kind")),
                "promotable_theorem_count": int(state_delta.get("promotable_theorem_count", 0) or 0),
                "max_concretization_score": int(state_delta.get("max_concretization_score", 0) or 0),
                "concrete_theorem_candidates": concrete_theorem_candidates,
                "artifact_json": _clean_text(
                    next(
                        (
                            row.get("artifact_json")
                            for row in _ensure_list(execution_index.get("executions"))
                            if isinstance(row, dict) and _clean_text(row.get("branch_id")) == branch_id
                        ),
                        "",
                    )
                ),
                "artifact_md": _clean_text(
                    next(
                        (
                            row.get("artifact_md")
                            for row in _ensure_list(execution_index.get("executions"))
                            if isinstance(row, dict) and _clean_text(row.get("branch_id")) == branch_id
                        ),
                        "",
                    )
                ),
            }
        )
    programmes.sort(key=lambda row: (_safe_float(row.get("routing_priority")), row.get("branch_id", "")), reverse=True)
    ready_for_prove = [row for row in programmes if _clean_text(row.get("agenda_bucket")) == "ready_for_prove"]
    ready_for_discovery = [row for row in programmes if _clean_text(row.get("agenda_bucket")) == "ready_for_discovery"]

    return {
        "metadata": {
            "kb_ref": kb_ref,
            "completed_branch_count": sum(1 for row in branches if _clean_text(row.get("status")).lower() == "completed"),
            "execution_count": len(reports),
            "proof_queue_pending": int(_ensure_dict(proof_queue.get("metadata")).get("pending_count", 0) or 0),
            "proof_queue_completed": int(_ensure_dict(proof_queue.get("metadata")).get("completed_count", 0) or 0),
            "ready_for_prove_count": len(ready_for_prove),
            "ready_for_discovery_count": len(ready_for_discovery),
        },
        "top_breakthrough_families": [
            {"family": family, "count": count}
            for family, count in family_counter.most_common(8)
        ],
        "top_obstruction_classes": [
            {"obstruction_class": obstruction, "count": count}
            for obstruction, count in obstruction_counter.most_common(8)
        ],
        "top_mathlib_references": [
            {"title": title, "count": count}
            for title, count in mathlib_counter.most_common(8)
        ],
        "next_programmes": programmes,
        "agenda": {
            "ready_for_prove": ready_for_prove,
            "ready_for_discovery": ready_for_discovery,
        },
        "judgment": {
            "summary": (
                "All routed discovery branches were executed once. The frontier is now better characterized than expanded: "
                "the dominant pressure remains on MCSP carrier realization, formula-size transport, and theorem-activation alignment."
            ),
            "next_move": (
                "Promote only the theorem-shaped branch families into the next prove-or-disprove agenda, and keep the pattern-level branches "
                "as discovery guidance rather than treating them as solved proof tasks."
            ),
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    lines = [
        "# Discovery Branch Synthesis",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Completed branches: {meta.get('completed_branch_count', 0)}",
        f"- Executed branch passes: {meta.get('execution_count', 0)}",
        f"- Proof queue pending: {meta.get('proof_queue_pending', 0)}",
        f"- Proof queue completed: {meta.get('proof_queue_completed', 0)}",
        f"- Ready for prove: {meta.get('ready_for_prove_count', 0)}",
        f"- Ready for discovery: {meta.get('ready_for_discovery_count', 0)}",
        "",
        "## Judgment",
        "",
        f"- {_ensure_dict(report.get('judgment')).get('summary', '')}",
        f"- Next move: {_ensure_dict(report.get('judgment')).get('next_move', '')}",
        "",
        "## Top Breakthrough Families",
        "",
    ]
    for row in _ensure_list(report.get("top_breakthrough_families")):
        lines.append(f"- {row.get('family', '')}: {row.get('count', 0)}")
    lines.extend(["", "## Top Obstruction Classes", ""])
    for row in _ensure_list(report.get("top_obstruction_classes")):
        lines.append(f"- {row.get('obstruction_class', '')}: {row.get('count', 0)}")
    lines.extend(["", "## Most Reused InformalMathLib References", ""])
    refs = [row for row in _ensure_list(report.get("top_mathlib_references")) if isinstance(row, dict)]
    if not refs:
        lines.append("- No InformalMathLib references were reused across branch executions.")
    else:
        for row in refs:
            lines.append(f"- {row.get('title', '')}: {row.get('count', 0)}")
    lines.extend(["", "## Ready For Prove", ""])
    ready_for_prove = [row for row in _ensure_list(_ensure_dict(report.get("agenda")).get("ready_for_prove")) if isinstance(row, dict)]
    if not ready_for_prove:
        lines.append("- No theorem-shaped programmes are currently ready to re-enter prove.")
    else:
        for row in ready_for_prove:
            lines.append(
                f"- {row.get('branch_id', '')}: {row.get('headline', '')} "
                f"(priority {_safe_float(row.get('routing_priority')):.3f}; linked queue {int(row.get('linked_queue_count', 0) or 0)})"
            )
    lines.extend(["", "## Ready For Discovery", ""])
    ready_for_discovery = [row for row in _ensure_list(_ensure_dict(report.get("agenda")).get("ready_for_discovery")) if isinstance(row, dict)]
    if not ready_for_discovery:
        lines.append("- No discovery-guidance programmes remain.")
    else:
        for row in ready_for_discovery:
            lines.append(
                f"- {row.get('branch_id', '')}: {row.get('headline', '')} "
                f"(priority {_safe_float(row.get('routing_priority')):.3f}; linked queue {int(row.get('linked_queue_count', 0) or 0)})"
            )
    lines.extend(["", "## Next Programmes", ""])
    for row in _ensure_list(report.get("next_programmes")):
        if not isinstance(row, dict):
            continue
        lines.extend(
            [
                f"### {row.get('branch_id', '')}",
                "",
                f"- Mode: {row.get('mode', '')}",
                f"- Execution status: {row.get('execution_status', '')}",
                f"- State delta: {row.get('state_delta_kind', '')}",
                f"- Target: {row.get('target_label', '')}",
                f"- Routing priority: {_safe_float(row.get('routing_priority')):.3f}",
                f"- Linked queue items: {int(row.get('linked_queue_count', 0) or 0)}",
                f"- Promotable theorem candidates: {int(row.get('promotable_theorem_count', 0) or 0)}",
                f"- Max concretization score: {int(row.get('max_concretization_score', 0) or 0)}",
                f"- Headline claim: {row.get('headline', '')}",
                f"- Rationale: {row.get('rationale', '')}",
                f"- Report: {row.get('artifact_md', '')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_tex(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    family_rows = "\n".join(
        f"\\item {_latex_escape(row.get('family', ''))}: {int(row.get('count', 0) or 0)}"
        for row in _ensure_list(report.get("top_breakthrough_families"))
        if isinstance(row, dict)
    ) or "\\item No repeated breakthrough families recorded."
    obstruction_rows = "\n".join(
        f"\\item {_latex_escape(row.get('obstruction_class', ''))}: {int(row.get('count', 0) or 0)}"
        for row in _ensure_list(report.get("top_obstruction_classes"))
        if isinstance(row, dict)
    ) or "\\item No repeated obstruction classes recorded."
    ref_rows = "\n".join(
        f"\\item {_latex_escape(row.get('title', ''))}: {int(row.get('count', 0) or 0)}"
        for row in _ensure_list(report.get("top_mathlib_references"))
        if isinstance(row, dict)
    ) or "\\item No reused InformalMathLib references recorded."
    prove_rows = "\n".join(
        f"\\item {_latex_escape(row.get('branch_id', ''))}: {_latex_escape(row.get('headline', ''))} "
        f"(priority {_safe_float(row.get('routing_priority')):.3f}; linked queue {int(row.get('linked_queue_count', 0) or 0)})"
        for row in _ensure_list(_ensure_dict(report.get("agenda")).get("ready_for_prove"))
        if isinstance(row, dict)
    ) or "\\item No theorem-shaped programmes are currently ready to re-enter prove."
    discovery_rows = "\n".join(
        f"\\item {_latex_escape(row.get('branch_id', ''))}: {_latex_escape(row.get('headline', ''))} "
        f"(priority {_safe_float(row.get('routing_priority')):.3f}; linked queue {int(row.get('linked_queue_count', 0) or 0)})"
        for row in _ensure_list(_ensure_dict(report.get("agenda")).get("ready_for_discovery"))
        if isinstance(row, dict)
    ) or "\\item No discovery-guidance programmes remain."
    programme_sections = []
    for row in _ensure_list(report.get("next_programmes")):
        if not isinstance(row, dict):
            continue
        programme_sections.append(
            "\n".join(
                [
                    f"\\subsection*{{{_latex_escape(row.get('branch_id', ''))}}}",
                    "\\begin{itemize}",
                    f"\\item Mode: {_latex_escape(row.get('mode', ''))}",
                    f"\\item Target: {_latex_escape(row.get('target_label', ''))}",
                    f"\\item Routing priority: {_safe_float(row.get('routing_priority')):.3f}",
                    f"\\item Linked queue items: {int(row.get('linked_queue_count', 0) or 0)}",
                    f"\\item Headline claim: {_latex_escape(row.get('headline', ''))}",
                    f"\\item Rationale: {_latex_escape(row.get('rationale', ''))}",
                    f"\\item Report: \\texttt{{{_latex_escape(row.get('artifact_md', ''))}}}",
                    "\\end{itemize}",
                ]
            )
        )
    programme_blob = "\n\n".join(programme_sections) or "\\subsection*{No programmes}\\noindent No next programmes recorded."
    judgment = _ensure_dict(report.get("judgment"))
    return rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{hyperref}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\title{{Discovery Branch Synthesis}}
\author{{Abducer}}
\date{{}}
\begin{{document}}
\maketitle

\noindent
\textbf{{KB ref:}} {_latex_escape(meta.get('kb_ref', ''))}\\
\textbf{{Completed branches:}} {int(meta.get('completed_branch_count', 0) or 0)}\\
\textbf{{Executed branch passes:}} {int(meta.get('execution_count', 0) or 0)}\\
\textbf{{Proof queue pending:}} {int(meta.get('proof_queue_pending', 0) or 0)}\\
\textbf{{Proof queue completed:}} {int(meta.get('proof_queue_completed', 0) or 0)}\\
\textbf{{Ready for prove:}} {int(meta.get('ready_for_prove_count', 0) or 0)}\\
\textbf{{Ready for discovery:}} {int(meta.get('ready_for_discovery_count', 0) or 0)}

\section*{{Judgment}}
\begin{{itemize}}
\item {_latex_escape(judgment.get('summary', ''))}
\item Next move: {_latex_escape(judgment.get('next_move', ''))}
\end{{itemize}}

\section*{{Top Breakthrough Families}}
\begin{{itemize}}
{family_rows}
\end{{itemize}}

\section*{{Top Obstruction Classes}}
\begin{{itemize}}
{obstruction_rows}
\end{{itemize}}

\section*{{Most Reused InformalMathLib References}}
\begin{{itemize}}
{ref_rows}
\end{{itemize}}

\section*{{Ready For Prove}}
\begin{{itemize}}
{prove_rows}
\end{{itemize}}

\section*{{Ready For Discovery}}
\begin{{itemize}}
{discovery_rows}
\end{{itemize}}

\section*{{Next Programmes}}
{programme_blob}

\end{{document}}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthesize completed discovery-branch executions.")
    parser.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    parser.add_argument("--kb-ref", default="", help="Optional KB reference override.")
    parser.add_argument("--latex-engine", default="auto", help="Preferred LaTeX engine for PDF generation.")
    args = parser.parse_args()

    artifacts_dir = Path(args.artifacts_dir).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[4]
    kb_ref = _clean_text(args.kb_ref) or kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("Unable to determine kb_ref from artifacts directory; pass --kb-ref.")
    artifacts_dir = canonical_artifacts_dir(repo_root, kb_ref) if not artifacts_dir.exists() else artifacts_dir

    logger = ReasoningLogger("kb-discovery-branch-synthesis", repo_root=repo_root)
    report = build_report(artifacts_dir=artifacts_dir, kb_ref=kb_ref, repo_root=repo_root)
    output_json, output_md, output_tex, output_pdf = _synthesis_paths(artifacts_dir)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")
    output_tex.write_text(render_tex(report), encoding="utf-8")
    compile_pdf(output_tex, output_pdf, preferred_engine=args.latex_engine)

    logger.step(
        "Synthesized discovery-branch executions",
        details="\n".join(
            [
                f"kb_ref={kb_ref}",
                f"completed_branches={int(_ensure_dict(report.get('metadata')).get('completed_branch_count', 0) or 0)}",
                f"execution_count={int(_ensure_dict(report.get('metadata')).get('execution_count', 0) or 0)}",
            ]
        ),
    )
    logger.add_output("discovery_branch_synthesis_json", output_json)
    logger.add_output("discovery_branch_synthesis_md", output_md)
    logger.add_output("discovery_branch_synthesis_tex", output_tex)
    logger.add_output("discovery_branch_synthesis_pdf", output_pdf)
    logger.finalize(
        status="success",
        summary=f"Synthesized {int(_ensure_dict(report.get('metadata')).get('execution_count', 0) or 0)} discovery-branch executions for `{kb_ref}`.",
    )

    print(f"[OK] Wrote discovery branch synthesis JSON: {output_json}")
    print(f"[OK] Wrote discovery branch synthesis Markdown: {output_md}")
    print(f"[OK] Wrote discovery branch synthesis TeX: {output_tex}")
    print(f"[OK] Wrote discovery branch synthesis PDF: {output_pdf}")
    print(f"[LOG] {logger.log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
