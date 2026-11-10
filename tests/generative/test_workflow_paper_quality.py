# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Semantic guardrails for generated framework-paper bundles."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def test_consistency_adjudicator_rejects_unlicensed_strong_language(tmp_path: Path) -> None:
    sections = tmp_path / "sections"
    sections.mkdir()
    (sections / "method.tex").write_text("\\section{Method} We demonstrate effectiveness.\n")
    (sections / "method.section.json").write_text(json.dumps({
        "section_id": "method", "consumed_claim_ids": [], "tex_fragment": "method.tex"
    }))
    ledger = tmp_path / "claims.json"
    ledger.write_text(json.dumps({"claims": []}))
    blueprint = tmp_path / "blueprint.json"
    blueprint.write_text(json.dumps({"sections": [{
        "section_id": "method", "required": True, "allowed_claim_ids": []
    }]}))
    output = tmp_path / "review.json"
    result = subprocess.run([
        sys.executable,
        str(REPO / "proj_skills/framework-paper-consistency-adjudicator/scripts/adjudicate_paper.py"),
        "--claim-ledger", str(ledger), "--blueprint", str(blueprint),
        "--sections-dir", str(sections), "--output", str(output),
    ], cwd=REPO, text=True, capture_output=True, check=False)
    assert result.returncode != 0
    report = json.loads(output.read_text())
    assert any(item["code"] == "unlicensed_strong_language" for item in report["findings"])


def test_validator_rejects_missing_epistemic_sections(tmp_path: Path) -> None:
    (tmp_path / "main.tex").write_text("\\begin{document}Text\\end{document}\n")
    (tmp_path / "build-manifest.json").write_text("{}\n")
    result = subprocess.run([
        sys.executable, str(REPO / "proj_skills/framework-paper-validator/scripts/validate_paper.py"),
        "--bundle", str(tmp_path),
    ], cwd=REPO, text=True, capture_output=True, check=False)
    assert result.returncode != 0
    report = json.loads((tmp_path / "validation.json").read_text())
    assert "missing limitations section" in report["errors"]
    assert "missing evaluation/evidence-status section" in report["errors"]


def test_validator_rejects_tampered_manifest_digest(tmp_path: Path) -> None:
    tex = "\\begin{document}\\section{Current Evidence Status}Unknown.\\section{Limitations}Scoped.\\end{document}\n"
    (tmp_path / "main.tex").write_text(tex)
    (tmp_path / "build-manifest.json").write_text(json.dumps({"main_tex_sha256": "0" * 64}))
    result = subprocess.run([
        sys.executable, str(REPO / "proj_skills/framework-paper-validator/scripts/validate_paper.py"),
        "--bundle", str(tmp_path),
    ], cwd=REPO, text=True, capture_output=True, check=False)
    assert result.returncode != 0
    assert "digest does not match" in (tmp_path / "validation.json").read_text()
