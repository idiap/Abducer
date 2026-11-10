# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from validate_public_reasoning_trace_pdf import EXPECTED_STEMS, companion_paths, extract_pdf_text


def test_all_reports_have_pages_metadata_selectable_text_and_textual_graphs() -> None:
    for stem in sorted(EXPECTED_STEMS):
        paths = companion_paths(stem)
        info = subprocess.run(["pdfinfo", str(paths["pdf"])], capture_output=True, text=True, check=True).stdout
        assert "Title:           Public Reasoning Trace" in info
        assert "Pages:" in info
        text = extract_pdf_text(paths["pdf"])
        packet = json.loads(paths["packet"].read_text(encoding="utf-8"))
        assert "Contents" in text
        assert "Expert reading contract" in text
        assert "Causal and workflow graph ledger" in text
        assert "Chronological precedence does" in text
        assert packet["identity"]["workflow_id"] in text


def test_accessibility_claim_is_honest_not_pdf_ua() -> None:
    coverage_doc = (ROOT / "docs/reference/reasoning-trace-pdf-accessibility.md").read_text(encoding="utf-8")
    assert "do not establish PDF/UA conformance" in coverage_doc
    assert "not run" in coverage_doc
