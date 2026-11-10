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

"""Import decisive prior-art references into InformalMathLib and report their effect on the current proof state."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

_SKILLS_ROOT = Path(__file__).resolve().parents[3]
_COMMON_DIR = _SKILLS_ROOT / "common"
_PROVE_SCRIPT_DIR = _SKILLS_ROOT / "discovery" / "kb-prove-cycle" / "scripts"
for _path in (_COMMON_DIR, _PROVE_SCRIPT_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from end_to_end_plausibility import build_plausibility_report_from_artifacts
from end_to_end_plausibility import render_plausibility_markdown
from generate_proof_cycle_summary import build_summary
from generate_proof_cycle_summary import write_summary
from generate_proof_queue_report import compile_pdf
from kb_context import kb_ref_from_artifacts_dir
from problem_mathlib import append_mathlib_result
from problem_mathlib import load_mathlib_index
from problem_mathlib import mathlib_paths
from problem_mathlib import render_mathlib_catalog
from problem_mathlib import write_mathlib_entry_file
from proof_queue import load_proof_queue
from proof_queue import proof_queue_paths
from reasoning_log import ReasoningLogger


EXTERNAL_REFERENCE_TYPES = {"theorem", "definition", "axiom"}


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


def _slugify(text: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "-", _clean_text(text).lower()).strip("-")


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


def _reference_key(reference: dict[str, Any]) -> str:
    return "|".join(
        [
            _clean_text(reference.get("reference_type")).lower(),
            _clean_text(reference.get("title")).lower(),
            _clean_text(reference.get("source_url")).lower(),
            _clean_text(reference.get("statement")).lower(),
        ]
    )


def _next_external_reference_id(index: dict[str, Any], *, kb_ref: str) -> str:
    prefix = f"mathlibref.{kb_ref}."
    current = 0
    for row in _ensure_list(index.get("results")):
        if not isinstance(row, dict):
            continue
        result_id = _clean_text(row.get("result_id"))
        if not result_id.startswith(prefix):
            continue
        suffix = result_id[len(prefix) :]
        if suffix.isdigit():
            current = max(current, int(suffix))
    return f"{prefix}{current + 1:03d}"


def _queue_index(queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        _clean_text(row.get("queue_id")): row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("queue_id"))
    }


def _normalize_reference(row: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(row, dict):
        return {}
    reference_type = _clean_text(row.get("reference_type")).lower()
    title = _clean_text(row.get("title"))
    statement = _clean_text(row.get("statement"))
    if reference_type not in EXTERNAL_REFERENCE_TYPES or not title or not statement:
        return {}
    return {
        "reference_type": reference_type,
        "title": title,
        "statement": statement,
        "source_name": _clean_text(row.get("source_name")),
        "source_url": _clean_text(row.get("source_url")),
        "search_query": _clean_text(row.get("search_query")),
        "used_for": _clean_text(row.get("used_for")),
        "notes": _clean_text(row.get("notes")),
        "canonical_citation": _clean_text(row.get("canonical_citation")),
        "what_changed": _clean_text(row.get("what_changed")),
        "local_search_failure": _clean_text(row.get("local_search_failure")),
        "linked_queue_ids": [
            _clean_text(value)
            for value in _ensure_list(row.get("linked_queue_ids"))
            if _clean_text(value)
        ],
        "linked_obstruction_classes": [
            _clean_text(value)
            for value in _ensure_list(row.get("linked_obstruction_classes"))
            if _clean_text(value)
        ],
    }


def _import_references(
    *,
    repo_root: Path,
    kb_ref: str,
    mathlib: dict[str, Any],
    references: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    existing_by_key = {
        _clean_text(row.get("external_reference_key")): row
        for row in _ensure_list(mathlib.get("results"))
        if isinstance(row, dict) and _clean_text(row.get("external_reference_key"))
    }
    imported: list[dict[str, Any]] = []
    for reference in references:
        key = _reference_key(reference)
        existing = existing_by_key.get(key)
        result_id = _clean_text(_ensure_dict(existing).get("result_id")) or _next_external_reference_id(mathlib, kb_ref=kb_ref)
        result = {
            "result_id": result_id,
            "entry_kind": "external-reference",
            "outcome": "external_reference",
            "queue_id": ",".join(reference["linked_queue_ids"]),
            "attempt_id": "",
            "bridge_id": "",
            "source_statement_id": "",
            "target_statement_id": "",
            "reference_type": reference["reference_type"],
            "title": reference["title"],
            "statement": reference["statement"],
            "summary": reference["what_changed"] or reference["used_for"],
            "source_name": reference["source_name"] or reference["canonical_citation"],
            "source_url": reference["source_url"],
            "search_query": reference["search_query"],
            "used_for": reference["used_for"],
            "external_reference_key": key,
            "tags": [
                reference["reference_type"],
                *reference["linked_obstruction_classes"],
                *reference["linked_queue_ids"],
            ],
            "web_search_used": bool(reference["source_url"]),
        }
        notes_lines = [
            f"Canonical citation: {reference['canonical_citation']}" if reference["canonical_citation"] else "",
            f"Local search failure: {reference['local_search_failure']}" if reference["local_search_failure"] else "",
            f"What changed: {reference['what_changed']}" if reference["what_changed"] else "",
            f"Linked queue ids: {', '.join(reference['linked_queue_ids'])}" if reference["linked_queue_ids"] else "",
            f"Obstruction classes: {', '.join(reference['linked_obstruction_classes'])}" if reference["linked_obstruction_classes"] else "",
            f"Notes: {reference['notes']}" if reference["notes"] else "",
        ]
        artifact_path = write_mathlib_entry_file(
            repo_root,
            kb_ref=kb_ref,
            result=result,
            proof_markdown="\n".join(line for line in notes_lines if line).strip(),
        )
        result["artifact_path"] = str(artifact_path)
        append_mathlib_result(mathlib, result)
        existing_by_key[key] = result
        imported.append({**reference, **result})
    return imported


def build_report(
    *,
    kb_ref: str,
    input_payload: dict[str, Any],
    imported: list[dict[str, Any]],
    queue: dict[str, Any],
) -> dict[str, Any]:
    queue_rows = _queue_index(queue)
    blocked_rows = [
        row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("status")).lower() == "blocked"
    ]
    obstruction_map: dict[str, dict[str, Any]] = {}
    for reference in imported:
        for name in reference.get("linked_obstruction_classes", []):
            row = obstruction_map.setdefault(
                name,
                {
                    "name": name,
                    "reference_ids": [],
                    "titles": [],
                    "queue_ids": [],
                    "what_changed": [],
                },
            )
            row["reference_ids"].append(reference["result_id"])
            row["titles"].append(reference["title"])
            row["queue_ids"].extend(reference.get("linked_queue_ids", []))
            if reference.get("what_changed"):
                row["what_changed"].append(reference["what_changed"])
    for row in obstruction_map.values():
        row["reference_ids"] = sorted(set(_clean_text(value) for value in row["reference_ids"] if _clean_text(value)))
        row["titles"] = sorted(set(_clean_text(value) for value in row["titles"] if _clean_text(value)))
        row["queue_ids"] = sorted(set(_clean_text(value) for value in row["queue_ids"] if _clean_text(value)))
        row["linked_queue_titles"] = [
            _clean_text(_ensure_dict(queue_rows.get(queue_id)).get("title")) or queue_id
            for queue_id in row["queue_ids"]
        ]

    covered_queue_ids = {
        queue_id
        for reference in imported
        for queue_id in reference.get("linked_queue_ids", [])
        if queue_id
    }
    uncovered_blocked = [
        {
            "queue_id": _clean_text(row.get("queue_id")),
            "title": _clean_text(row.get("title")),
            "summary": _clean_text(row.get("resolution_summary")),
        }
        for row in blocked_rows
        if _clean_text(row.get("queue_id")) not in covered_queue_ids
    ]
    key_findings = [
        _clean_text(item)
        for item in _ensure_list(input_payload.get("key_findings"))
        if _clean_text(item)
    ]
    if not key_findings:
        key_findings = [
            "The imported references mostly ground targets and barriers rather than closing the missing lemmas themselves.",
            "The proof state changes by sharpening which steps are truly novel versus already established in the literature.",
        ]
    return {
        "metadata": {
            "kb_ref": kb_ref,
            "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "imported_reference_count": len(imported),
            "blocked_queue_count": len(blocked_rows),
            "covered_blocked_queue_count": len(covered_queue_ids),
            "uncovered_blocked_queue_count": len(uncovered_blocked),
        },
        "search_justification": _clean_text(_ensure_dict(input_payload.get("metadata")).get("search_justification")),
        "key_findings": key_findings,
        "imported_references": imported,
        "obstruction_map": sorted(obstruction_map.values(), key=lambda row: row["name"]),
        "uncovered_blocked_routes": uncovered_blocked,
    }


def render_markdown(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    imported = [row for row in _ensure_list(report.get("imported_references")) if isinstance(row, dict)]
    obstruction_map = [row for row in _ensure_list(report.get("obstruction_map")) if isinstance(row, dict)]
    uncovered = [row for row in _ensure_list(report.get("uncovered_blocked_routes")) if isinstance(row, dict)]
    lines = [
        "# Prior-Art Pass Report",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Generated (UTC): {meta.get('generated_utc', '')}",
        f"- Imported references: {meta.get('imported_reference_count', 0)}",
        f"- Blocked queue items: {meta.get('blocked_queue_count', 0)}",
        f"- Covered blocked queue items: {meta.get('covered_blocked_queue_count', 0)}",
        f"- Uncovered blocked queue items: {meta.get('uncovered_blocked_queue_count', 0)}",
        "",
        "## Search Justification",
        "",
        f"{report.get('search_justification', '') or 'No explicit search-justification note was recorded.'}",
        "",
        "## Key Findings",
        "",
    ]
    findings = [item for item in _ensure_list(report.get("key_findings")) if _clean_text(item)]
    if not findings:
        lines.append("- No key findings recorded.")
        lines.append("")
    else:
        for item in findings:
            lines.append(f"- {item}")
        lines.append("")

    lines.extend(["## Imported References", ""])
    if not imported:
        lines.append("- No decisive external references were imported.")
        lines.append("")
    for row in imported:
        lines.extend(
            [
                f"### {row.get('title', row.get('result_id', 'Reference'))}",
                "",
                f"- Result ID: {row.get('result_id', '')}",
                f"- Type: {row.get('reference_type', '')}",
                f"- Statement: {row.get('statement', '')}",
                f"- Canonical citation: {row.get('canonical_citation', '')}",
                f"- Source: {row.get('source_name', '')}",
                f"- URL: {row.get('source_url', '')}",
                f"- Search query: {row.get('search_query', '')}",
                f"- Used for: {row.get('used_for', '')}",
                f"- What changed: {row.get('what_changed', '')}",
                f"- Linked queue ids: {', '.join(row.get('linked_queue_ids', []))}",
                f"- Obstruction classes: {', '.join(row.get('linked_obstruction_classes', []))}",
                f"- InformalMathLib file: {row.get('artifact_path', '')}",
                "",
            ]
        )

    lines.extend(["## Obstruction Map", ""])
    if not obstruction_map:
        lines.append("- No obstruction-class map recorded.")
        lines.append("")
    for row in obstruction_map:
        lines.extend(
            [
                f"### {row.get('name', 'Obstruction Class')}",
                "",
                f"- Reference IDs: {', '.join(row.get('reference_ids', []))}",
                f"- Reference titles: {', '.join(row.get('titles', []))}",
                f"- Queue IDs: {', '.join(row.get('queue_ids', []))}",
                f"- Queue titles: {', '.join(row.get('linked_queue_titles', []))}",
                "",
            ]
        )
        for item in row.get("what_changed", []):
            lines.append(f"- Change: {item}")
        lines.append("")

    lines.extend(["## Still Uncovered", ""])
    if not uncovered:
        lines.append("- All currently blocked queue items are linked to at least one imported prior-art reference.")
        lines.append("")
    else:
        for row in uncovered:
            lines.append(f"- `{row.get('queue_id', '')}` | {row.get('title', '')} | {row.get('summary', '')}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_tex(report: dict[str, Any]) -> str:
    meta = _ensure_dict(report.get("metadata"))
    imported = [row for row in _ensure_list(report.get("imported_references")) if isinstance(row, dict)]
    obstruction_map = [row for row in _ensure_list(report.get("obstruction_map")) if isinstance(row, dict)]
    uncovered = [row for row in _ensure_list(report.get("uncovered_blocked_routes")) if isinstance(row, dict)]
    imported_rows = [
        rf"{_latex_escape(row.get('result_id'))} & {_latex_escape(row.get('reference_type'))} & {_latex_escape(row.get('title'))} & {_latex_escape(', '.join(row.get('linked_obstruction_classes', [])))} \\"
        for row in imported
    ] or [r"None & - & - & - \\"]
    obstruction_sections: list[str] = []
    for row in obstruction_map:
        changes = [
            rf"\item {_latex_escape(item)}"
            for item in row.get("what_changed", [])
            if _clean_text(item)
        ] or [r"\item No effect note recorded."]
        obstruction_sections.append(
            "\n".join(
                [
                    rf"\subsection*{{{_latex_escape(row.get('name'))}}}",
                    rf"\textbf{{References.}} {_latex_escape(', '.join(row.get('reference_ids', [])))}",
                    "",
                    rf"\textbf{{Queue ids.}} {_latex_escape(', '.join(row.get('queue_ids', [])))}",
                    "",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *changes,
                    r"\end{itemize}",
                ]
            )
        )
    if not obstruction_sections:
        obstruction_sections.append("No obstruction-class coverage was recorded.")
    uncovered_items = [
        rf"\item \texttt{{{_latex_escape(row.get('queue_id'))}}}: {_latex_escape(row.get('title'))} -- {_latex_escape(row.get('summary'))}"
        for row in uncovered
    ] or [r"\item All blocked queue items have at least one linked imported reference."]

    report_date = dt.datetime.now().strftime("%B %d, %Y")
    return rf"""\documentclass[11pt]{{article}}

\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern}}
\usepackage{{booktabs}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{longtable}}

\hypersetup{{
  colorlinks=true,
  linkcolor=blue!50!black,
  urlcolor=blue!50!black,
  citecolor=blue!50!black,
  pdftitle={{Prior-Art Pass Report for {_latex_escape(meta.get('kb_ref'))}}}
}}

\title{{Prior-Art Pass Report for \texttt{{{_latex_escape(meta.get('kb_ref'))}}}}}
\author{{Neuro-symbolic AI Group\\Idiap Research Institute}}
\date{{{_latex_escape(report_date)}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
This report records a targeted prior-art pass over the current blocked proof frontier. It imports decisive external theorem-level references into the problem-scoped InformalMathLib and explains what those references change about the current proof state.
\end{{abstract}}

\section{{Snapshot}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
\item Imported references: {_latex_escape(meta.get('imported_reference_count'))}
\item Blocked queue items: {_latex_escape(meta.get('blocked_queue_count'))}
\item Covered blocked queue items: {_latex_escape(meta.get('covered_blocked_queue_count'))}
\item Uncovered blocked queue items: {_latex_escape(meta.get('uncovered_blocked_queue_count'))}
\end{{itemize}}

\section{{Search Justification}}
{_latex_escape(report.get('search_justification') or 'No explicit search-justification note was recorded.')}

\section{{Key Findings}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
{chr(10).join(rf"\item {_latex_escape(item)}" for item in _ensure_list(report.get('key_findings')) if _clean_text(item)) or r"\item No key findings recorded."}
\end{{itemize}}

\section{{Imported References}}
\begin{{longtable}}{{p{{0.13\linewidth}}p{{0.1\linewidth}}p{{0.42\linewidth}}p{{0.25\linewidth}}}}
\toprule
ID & Type & Title & Obstruction classes \\
\midrule
{chr(10).join(imported_rows)}
\bottomrule
\end{{longtable}}

\section{{Obstruction Map}}
{chr(10).join(obstruction_sections)}

\section{{Still Uncovered}}
\begin{{itemize}}[leftmargin=*,itemsep=0.2em]
{chr(10).join(uncovered_items)}
\end{{itemize}}

\end{{document}}
"""


def main() -> int:
    logger = ReasoningLogger("kb-prior-art-pass")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    ap.add_argument("--kb-ref", default="", help="Optional KB reference override.")
    ap.add_argument("--input-json", required=True, help="Curated prior-art input JSON.")
    ap.add_argument("--mathlib-json", default="", help="Optional InformalMathLib index JSON path.")
    ap.add_argument("--queue-json", default="", help="Optional proof-queue JSON path.")
    ap.add_argument("--output-json", default="", help="Optional prior-art report JSON path.")
    ap.add_argument("--output-md", default="", help="Optional prior-art report Markdown path.")
    ap.add_argument("--output-tex", default="", help="Optional prior-art report TeX path.")
    ap.add_argument("--output-pdf", default="", help="Optional prior-art report PDF path.")
    ap.add_argument("--latex-engine", default="auto", help="LaTeX engine preference.")
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
    kb_ref = _clean_text(args.kb_ref) or kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("[ERROR] Could not resolve kb_ref for prior-art pass.")

    input_json = Path(args.input_json)
    if not input_json.is_absolute():
        input_json = (repo_root / input_json).resolve()
    input_payload = _load_json(input_json)
    references = [
        normalized
        for normalized in (_normalize_reference(row) for row in _ensure_list(input_payload.get("references")))
        if normalized
    ]
    if not references:
        raise SystemExit(f"[ERROR] No valid references found in {input_json}")

    mathlib_json, mathlib_md = mathlib_paths(repo_root, kb_ref)
    queue_json, _ = proof_queue_paths(repo_root, kb_ref)
    if args.mathlib_json:
        mathlib_json = Path(args.mathlib_json)
        if not mathlib_json.is_absolute():
            mathlib_json = (repo_root / mathlib_json).resolve()
    if args.queue_json:
        queue_json = Path(args.queue_json)
        if not queue_json.is_absolute():
            queue_json = (repo_root / queue_json).resolve()

    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "prior-art-pass-report.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "prior-art-pass-report.md"
    output_tex = Path(args.output_tex) if args.output_tex else artifacts_dir / "prior-art-pass-report.tex"
    output_pdf = Path(args.output_pdf) if args.output_pdf else artifacts_dir / "prior-art-pass-report.pdf"
    if not output_json.is_absolute():
        output_json = (repo_root / output_json).resolve()
    if not output_md.is_absolute():
        output_md = (repo_root / output_md).resolve()
    if not output_tex.is_absolute():
        output_tex = (repo_root / output_tex).resolve()
    if not output_pdf.is_absolute():
        output_pdf = (repo_root / output_pdf).resolve()

    logger.step(
        "Parsed prior-art-pass arguments",
        "\n".join(
            [
                f"artifacts_dir={artifacts_dir}",
                f"kb_ref={kb_ref}",
                f"input_json={input_json}",
                f"reference_count={len(references)}",
            ]
        ),
        surface_focus="prior-art-pass",
        surface_stage="prior-art",
    )

    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    mathlib = load_mathlib_index(mathlib_json, kb_ref=kb_ref)
    imported = _import_references(repo_root=repo_root, kb_ref=kb_ref, mathlib=mathlib, references=references)
    mathlib_json.parent.mkdir(parents=True, exist_ok=True)
    mathlib_json.write_text(json.dumps(mathlib, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    mathlib_md.write_text(render_mathlib_catalog(mathlib), encoding="utf-8")

    report = build_report(kb_ref=kb_ref, input_payload=input_payload, imported=imported, queue=queue)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_tex.parent.mkdir(parents=True, exist_ok=True)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")
    output_tex.write_text(render_tex(report), encoding="utf-8")
    if args.compile_pdf:
        compile_pdf(output_tex, output_pdf, preferred_engine=args.latex_engine)

    proof_summary = build_summary(kb_ref=kb_ref, queue=queue, mathlib=mathlib)
    write_summary(
        proof_summary,
        output_json=artifacts_dir / "proof-cycle-summary.json",
        output_md=artifacts_dir / "proof-cycle-summary.md",
    )

    plausibility = build_plausibility_report_from_artifacts(repo_root, artifacts_dir)
    (artifacts_dir / "end-to-end-proof-plausibility.json").write_text(
        json.dumps(plausibility, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (artifacts_dir / "end-to-end-proof-plausibility.md").write_text(
        render_plausibility_markdown(plausibility),
        encoding="utf-8",
    )

    logger.step(
        "Imported prior-art references",
        "\n".join(
            [
                f"imported_reference_count={len(imported)}",
                f"mathlib_external_reference_count={mathlib.get('metadata', {}).get('external_reference_count', 0)}",
                f"plausibility_score={plausibility.get('plausibility_score', 0.0)}",
            ]
        ),
        surface_focus="prior-art-pass",
        surface_stage="prior-art",
        surface_metrics={
            "imported_reference_count": len(imported),
            "external_reference_count": int(mathlib.get("metadata", {}).get("external_reference_count", 0) or 0),
            "plausibility_score": float(plausibility.get("plausibility_score", 0.0) or 0.0),
        },
        surface_taxonomy={"reasoning_types": ["prior-art", "mathlib-update", "proof-state-refresh"]},
    )
    logger.add_output("mathlib_json", mathlib_json)
    logger.add_output("mathlib_md", mathlib_md)
    logger.add_output("prior_art_pass_json", output_json)
    logger.add_output("prior_art_pass_md", output_md)
    logger.add_output("prior_art_pass_tex", output_tex)
    if args.compile_pdf:
        logger.add_output("prior_art_pass_pdf", output_pdf)
    logger.add_output("proof_cycle_summary_md", artifacts_dir / "proof-cycle-summary.md")
    logger.add_output("end_to_end_plausibility_md", artifacts_dir / "end-to-end-proof-plausibility.md")
    log_path = logger.finalize(
        "success",
        summary=f"Imported {len(imported)} prior-art references for `{kb_ref}` and refreshed proof-state reports.",
    )
    print(f"[OK] Updated InformalMathLib JSON: {mathlib_json}")
    print(f"[OK] Wrote prior-art report JSON: {output_json}")
    print(f"[OK] Wrote prior-art report Markdown: {output_md}")
    print(f"[OK] Wrote prior-art report TeX: {output_tex}")
    if args.compile_pdf:
        print(f"[OK] Wrote prior-art report PDF: {output_pdf}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
