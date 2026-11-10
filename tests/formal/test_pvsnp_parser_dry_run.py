# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""
Regression tests for report parsing without unintended KB mutation.

Concept: Captures the intended behavior of one part of the KB reasoning framework under deterministic test conditions.
Contribution: Keeps future refactors aligned with the framework's conceptual and inferential contracts.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_pvsnp_parser_dry_run_does_not_mutate_kb(tmp_path: Path) -> None:
    """
    Concept: Validates that pvsnp parser dry run does not mutate kb.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    input_report = tmp_path / "mini-report.tex"
    input_report.write_text(
        "\n".join(
            [
                r"\section{Mini}",
                r"\begin{definition}[Toy Definition]",
                r"A toy definition body.",
                r"\end{definition}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    kb_path = tmp_path / "mini.kb.md"
    kb_path.write_text(
        "\n".join(
            [
                "---",
                "kb_id: mini",
                "title: Mini",
                "domain: mathematics",
                "subdomain: test",
                "---",
                "",
                "# Source Index",
                "",
                "| source_id | type | citation | locator | reliability | notes |",
                "|---|---|---|---|---|---|",
                "| src.001 | file | baseline | full document | high | baseline |",
                "",
                "# Canonical Statements",
                "",
                "# Derived Statements",
                "",
                "# Change Log",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    before = kb_path.read_text(encoding="utf-8")

    output_statements = tmp_path / "parsed.json"
    script = ROOT / "skills" / "ingest" / "pvsnp-kb-parser" / "scripts" / "parse_report.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--input",
            str(input_report),
            "--output-statements",
            str(output_statements),
            "--kb",
            str(kb_path),
            "--source-id",
            "src.999",
            "--citation",
            "fake-citation",
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + "\n" + result.stdout

    after = kb_path.read_text(encoding="utf-8")
    assert before == after
