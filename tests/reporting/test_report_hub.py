# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Regression tests for the unified report hub generator."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills" / "control-plane" / "meta" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from archive_legacy_reports import archive_legacy_reports
from generate_report_hub import build_hub_manifest
from generate_report_hub import discover_report_groups
from generate_report_hub import latex_to_html
from generate_report_hub import render_report_hub_html
from generate_report_hub import write_report_hub


def test_latex_to_html_preserves_structure_and_math() -> None:
    tex = r"""
\documentclass{article}
\title{Demo Report}
\begin{document}
\maketitle
\section{Overview}
Inline math $A \rightarrow B$.

\begin{itemize}
\item First point
\item Second point with \textbf{emphasis}
\end{itemize}

\begin{longtable}{ll}
\toprule
Signal & Score \\
\midrule
\endhead
bridge & 0.9 \\
\bottomrule
\end{longtable}
\end{document}
"""
    html = latex_to_html(tex, source_name="demo-report.tex")
    assert "<h1>Demo Report</h1>" in html
    assert "<h2>Overview</h2>" in html
    assert "<ul>" in html
    assert "<strong>emphasis</strong>" in html
    assert "<table>" in html
    assert "$A \\rightarrow B$" in html
    assert "<th>Signal</th>" in html
    assert "built-in best-effort converter" in html


def test_report_hub_manifest_groups_formats_under_one_report(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True)
    (artifacts_dir / "proof-cycle-summary.md").write_text("# Summary\n\nHello.", encoding="utf-8")
    (artifacts_dir / "proof-cycle-summary.tex").write_text(
        "\\documentclass{article}\\begin{document}\\section{Summary}Hello.\\end{document}",
        encoding="utf-8",
    )
    (artifacts_dir / "process-graph.html").write_text("<!doctype html><title>Graph</title>", encoding="utf-8")

    manifest = build_hub_manifest(artifacts_dir, output_html=artifacts_dir / "report-hub.html")
    reports = {row["key"]: row for row in manifest["reports"]}

    assert "proof-cycle-summary" in reports
    assert reports["proof-cycle-summary"]["available_formats"] == ["md", "tex"]
    assert reports["process-graph"]["available_formats"] == ["html"]
    assert manifest["metadata"]["report_count"] == 2


def test_write_report_hub_emits_tabbed_html_interface(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True)
    (artifacts_dir / "work-state.md").write_text("# Work State\n\nCurrent state.", encoding="utf-8")
    (artifacts_dir / "process-graph.html").write_text("<!doctype html><title>Graph</title>", encoding="utf-8")

    manifest = write_report_hub(artifacts_dir=artifacts_dir, output_html=artifacts_dir / "report-hub.html")
    html = (artifacts_dir / "report-hub.html").read_text(encoding="utf-8")

    assert manifest["metadata"]["report_count"] == 2
    assert "Unified Report Interface" in html
    assert "MathJax" in html
    assert "report-tab" in html
    assert "format-pill" in html
    assert "work-state" in html
    assert "process-graph.html" in html
    assert "Markdown is pre-rendered into HTML." in html


def test_report_hub_ignores_non_report_and_legacy_top_level_files(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True)
    (artifacts_dir / "work-state.md").write_text("# Work State\n", encoding="utf-8")
    (artifacts_dir / "prior-art-pass-input.json").write_text("{}", encoding="utf-8")
    (artifacts_dir / "process-graph-evolution.json").write_text("{}", encoding="utf-8")
    (artifacts_dir / "review-reasoner-report.md").write_text("# Legacy Review\n", encoding="utf-8")
    (artifacts_dir / "proof-queue-report.tex").write_text("\\documentclass{article}", encoding="utf-8")
    (artifacts_dir / "report-hub.html").write_text("<!doctype html>", encoding="utf-8")

    reports = discover_report_groups(artifacts_dir, output_html=artifacts_dir / "report-hub.html")

    assert [row["key"] for row in reports] == ["work-state"]


def test_archive_legacy_reports_moves_orphan_legacy_exports(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True)
    (artifacts_dir / "review-reasoner-report.md").write_text("# Legacy Review\n", encoding="utf-8")
    (artifacts_dir / "proof-queue-report.tex").write_text("\\documentclass{article}", encoding="utf-8")
    (artifacts_dir / "work-state.md").write_text("# Work State\n", encoding="utf-8")

    inventory = archive_legacy_reports(artifacts_dir)

    assert inventory["metadata"]["archived_count"] == 2
    assert not (artifacts_dir / "review-reasoner-report.md").exists()
    assert not (artifacts_dir / "proof-queue-report.tex").exists()
    assert (artifacts_dir / "legacy-reports" / "review-reasoner-report.md").exists()
    assert (artifacts_dir / "legacy-reports" / "proof-queue-report.tex").exists()
    assert (artifacts_dir / "legacy-report-inventory.json").exists()
    assert (artifacts_dir / "legacy-report-inventory.md").exists()
    assert (artifacts_dir / "work-state.md").exists()


def test_render_report_hub_html_includes_manifest_payload() -> None:
    manifest = {
        "metadata": {"title": "Demo Hub", "report_count": 1, "format_counts": {"md": 1}},
        "reports": [
            {
                "key": "demo-report",
                "label": "Demo Report",
                "category": "Core",
                "default_format": "md",
                "available_formats": ["md"],
                "formats": {"md": {"kind": "inline", "rendered_html": "<article>demo</article>"}},
            }
        ],
    }
    html = render_report_hub_html(manifest)
    assert "<title>Demo Hub</title>" in html
    assert "demo-report" in html
    assert "Demo Report" in html
    assert "report-manifest" in html
