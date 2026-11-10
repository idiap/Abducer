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

"""Generate a LaTeX/PDF report for the current proof queue state."""

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

from kb_context import kb_ref_from_artifacts_dir
from proof_queue import load_proof_queue
from proof_queue import proof_queue_paths
from reasoning_log import ReasoningLogger


def _ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def _truncate(value: Any, limit: int = 220) -> str:
    text = _clean_text(value)
    if len(text) <= limit:
        return text
    cut = text[: max(0, limit - 3)].rstrip()
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + "..."


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


def build_report(*, queue: dict[str, Any], kb_ref: str) -> dict[str, Any]:
    metadata = _ensure_dict(queue.get("metadata"))
    entries = [row for row in _ensure_list(queue.get("entries")) if isinstance(row, dict)]
    by_status: dict[str, list[dict[str, Any]]] = {}
    for row in entries:
        status = _clean_text(row.get("status")) or "pending"
        by_status.setdefault(status, []).append(row)
    for rows in by_status.values():
        rows.sort(key=lambda item: _safe_float(item.get("priority")), reverse=True)
    return {
        "metadata": {
            "kb_ref": kb_ref,
            "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
            "queue_updated_utc": metadata.get("updated_utc", ""),
            "queue_version": metadata.get("queue_version", ""),
            "pending_count": metadata.get("pending_count", len(by_status.get("pending", []))),
            "in_progress_count": metadata.get("in_progress_count", len(by_status.get("in_progress", []))),
            "completed_count": metadata.get("completed_count", sum(len(rows) for status, rows in by_status.items() if status not in {"pending", "in_progress"})),
            "entry_count": len(entries),
        },
        "entries": entries,
        "by_status": by_status,
    }


def render_tex(report: dict[str, Any]) -> str:
    metadata = _ensure_dict(report.get("metadata"))
    by_status = _ensure_dict(report.get("by_status"))
    summary_rows = []
    for status in ("pending", "in_progress", "proved", "disproved", "blocked", "deferred", "prior_art_found"):
        rows = [row for row in _ensure_list(by_status.get(status)) if isinstance(row, dict)]
        if rows:
            summary_rows.append(
                rf"{_latex_escape(status.replace('_', ' ').title())} & {len(rows)} \\"
            )
    if not summary_rows:
        summary_rows.append(r"None & 0 \\")

    def render_entry(row: dict[str, Any]) -> str:
        proof_obligations = [
            rf"\item {_latex_escape(item)}"
            for item in _ensure_list(row.get("proof_obligations"))[:4]
            if _clean_text(item)
        ]
        candidate_lemmas = [
            rf"\item {_latex_escape(item)}"
            for item in _ensure_list(row.get("candidate_lemmas"))[:4]
            if _clean_text(item)
        ]
        resolution = _clean_text(row.get("resolution_summary"))
        resolution_block = ""
        if resolution:
            resolution_block = "\n".join(
                [
                    r"\paragraph{Resolution}",
                    _latex_escape(resolution),
                ]
            )
        attempt_block = ""
        attempts = [item for item in _ensure_list(row.get("attempt_ids")) if _clean_text(item)]
        if attempts:
            attempt_block = "\n".join(
                [
                    r"\paragraph{Attempts}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.15em]",
                    *[rf"\item \texttt{{{_latex_escape(item)}}}" for item in attempts],
                    r"\end{itemize}",
                ]
            )
        obligations_block = ""
        if proof_obligations:
            obligations_block = "\n".join(
                [
                    r"\paragraph{Proof Obligations}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *proof_obligations,
                    r"\end{itemize}",
                ]
            )
        lemmas_block = ""
        if candidate_lemmas:
            lemmas_block = "\n".join(
                [
                    r"\paragraph{Candidate Lemmas}",
                    r"\begin{itemize}[leftmargin=*,itemsep=0.2em]",
                    *candidate_lemmas,
                    r"\end{itemize}",
                ]
            )
        return "\n".join(
            [
                rf"\subsection*{{{_latex_escape(row.get('queue_id') or 'Queue Entry')}}}",
                r"\begin{itemize}[leftmargin=*,itemsep=0.25em]",
                rf"\item Status: {_latex_escape(row.get('status'))}",
                rf"\item Priority: {_safe_float(row.get('priority')):.3f}",
                rf"\item Bridge: \texttt{{{_latex_escape(row.get('bridge_id'))}}}",
                rf"\item Route: \texttt{{{_latex_escape(row.get('source_statement_id'))}}} $\rightarrow$ \texttt{{{_latex_escape(row.get('target_statement_id'))}}}",
                rf"\item Candidate object: {_latex_escape(row.get('candidate_object'))}",
                rf"\item Carrier kind: {_latex_escape(row.get('carrier_kind'))}",
                rf"\item Invariant: {_latex_escape(row.get('preserved_invariant'))}",
                rf"\item Conjecture: {_latex_escape(row.get('conjecture_statement') or row.get('claim_text'))}",
                rf"\item Route lemma under test: {_latex_escape(row.get('missing_route_lemma'))}",
                rf"\item Route synopsis: {_latex_escape(row.get('route_synopsis'))}",
                r"\end{itemize}",
                r"\paragraph{Theorem Pair}",
                rf"\textbf{{Source.}} {_latex_escape(_truncate(row.get('source_excerpt'), 420))}",
                "",
                rf"\textbf{{Target.}} {_latex_escape(_truncate(row.get('target_excerpt'), 420))}",
                "",
                obligations_block,
                lemmas_block,
                resolution_block,
                attempt_block,
            ]
        ).strip()

    sections = []
    for status in ("in_progress", "pending", "proved", "disproved", "blocked", "deferred", "prior_art_found"):
        rows = [row for row in _ensure_list(by_status.get(status)) if isinstance(row, dict)]
        if not rows:
            continue
        sections.append(rf"\section{{{_latex_escape(status.replace('_', ' ').title())}}}")
        for row in rows:
            sections.append(render_entry(row))

    if not sections:
        sections.append(r"\section{Queue Entries}")
        sections.append("No queue entries are currently recorded.")

    report_date = dt.datetime.now().strftime("%B %d, %Y")
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
\usepackage{{longtable}}
\usepackage{{xcolor}}

\hypersetup{{
  colorlinks=true,
  linkcolor=blue!50!black,
  urlcolor=blue!50!black,
  citecolor=blue!50!black,
  pdftitle={{Proof Queue Report for {_latex_escape(metadata.get('kb_ref'))}}}
}}

\title{{Proof Queue Report for \texttt{{{_latex_escape(metadata.get('kb_ref'))}}}}}
\author{{Neuro-symbolic AI Group\\Idiap Research Institute}}
\date{{{_latex_escape(report_date)}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
This report captures the current state of the persistent proof queue for \texttt{{{_latex_escape(metadata.get('kb_ref'))}}}.
It records the active conjectures, their theorem pairs, bridge objects, invariants, route lemmas, and the main obligations
currently assigned to each route. The report is intended as an inspectable snapshot of the prove frontier.
\end{{abstract}}

\section{{Queue Snapshot}}
\begin{{itemize}}[leftmargin=*,itemsep=0.25em]
\item Queue version: {_latex_escape(metadata.get('queue_version'))}
\item Queue updated (UTC): {_latex_escape(metadata.get('queue_updated_utc'))}
\item Report generated (UTC): {_latex_escape(metadata.get('generated_utc'))}
\item Total entries: {_latex_escape(metadata.get('entry_count'))}
\item Pending: {_latex_escape(metadata.get('pending_count'))}
\item In progress: {_latex_escape(metadata.get('in_progress_count'))}
\item Completed: {_latex_escape(metadata.get('completed_count'))}
\end{{itemize}}

\section{{Status Summary}}
\begin{{center}}
\begin{{tabular}}{{lr}}
\toprule
Status & Count \\
\midrule
{chr(10).join(summary_rows)}
\bottomrule
\end{{tabular}}
\end{{center}}

{chr(10).join(sections)}

\end{{document}}
"""


def main() -> int:
    logger = ReasoningLogger("kb-proof-queue-report")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    ap.add_argument("--kb-ref", default="", help="Optional KB reference override.")
    ap.add_argument("--queue-json", default="", help="Optional proof-queue JSON path.")
    ap.add_argument("--output-tex", default="", help="Optional proof-queue-report TeX path.")
    ap.add_argument("--output-pdf", default="", help="Optional proof-queue-report PDF path.")
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
    kb_ref = _clean_text(args.kb_ref) or kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("[ERROR] Could not resolve kb_ref for proof queue report.")

    queue_json, _ = proof_queue_paths(repo_root, kb_ref)
    if args.queue_json:
        queue_json = Path(args.queue_json)
        if not queue_json.is_absolute():
            queue_json = (repo_root / queue_json).resolve()
    output_tex = Path(args.output_tex) if args.output_tex else artifacts_dir / "proof-queue-report.tex"
    output_pdf = Path(args.output_pdf) if args.output_pdf else artifacts_dir / "proof-queue-report.pdf"
    if not output_tex.is_absolute():
        output_tex = (repo_root / output_tex).resolve()
    if not output_pdf.is_absolute():
        output_pdf = (repo_root / output_pdf).resolve()

    logger.step(
        "Parsed proof-queue-report arguments",
        "\n".join(
            [
                f"artifacts_dir={artifacts_dir}",
                f"kb_ref={kb_ref}",
                f"queue_json={queue_json}",
                f"output_tex={output_tex}",
                f"output_pdf={output_pdf}",
                f"compile_pdf={args.compile_pdf}",
                f"latex_engine={args.latex_engine}",
            ]
        ),
        surface_focus="proof-queue-report",
        surface_stage="prove-cycle",
    )

    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    report = build_report(queue=queue, kb_ref=kb_ref)
    tex_source = render_tex(report)

    output_tex.parent.mkdir(parents=True, exist_ok=True)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    output_tex.write_text(tex_source, encoding="utf-8")
    if args.compile_pdf:
        compile_pdf(output_tex, output_pdf, preferred_engine=args.latex_engine)

    logger.step(
        "Generated proof queue report",
        "\n".join(
            [
                f"entry_count={_clean_text(report['metadata'].get('entry_count'))}",
                f"pending_count={_clean_text(report['metadata'].get('pending_count'))}",
                f"in_progress_count={_clean_text(report['metadata'].get('in_progress_count'))}",
                f"completed_count={_clean_text(report['metadata'].get('completed_count'))}",
            ]
        ),
        surface_focus="proof-queue-report",
        surface_stage="prove-cycle",
        surface_metrics={
            "entry_count": int(report["metadata"].get("entry_count", 0) or 0),
            "pending_count": int(report["metadata"].get("pending_count", 0) or 0),
            "in_progress_count": int(report["metadata"].get("in_progress_count", 0) or 0),
            "completed_count": int(report["metadata"].get("completed_count", 0) or 0),
        },
        surface_taxonomy={"reasoning_types": ["prove-cycle", "queue-report"]},
    )
    logger.add_output("proof_queue_report_tex", output_tex)
    if args.compile_pdf:
        logger.add_output("proof_queue_report_pdf", output_pdf)
    log_path = logger.finalize(
        "success",
        summary=f"Generated proof queue report for `{kb_ref}` with {report['metadata'].get('entry_count', 0)} entries.",
    )
    print(f"[OK] Wrote proof queue report TeX: {output_tex}")
    if args.compile_pdf:
        print(f"[OK] Wrote proof queue report PDF: {output_pdf}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
