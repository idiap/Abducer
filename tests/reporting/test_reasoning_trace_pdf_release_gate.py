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

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_no_argument_pdf_release_gate_validates_all_seven_without_writes() -> None:
    generated = ROOT / "tests/fixtures/reasoning_trace/generated"
    before = {path: (path.stat().st_mtime_ns, path.stat().st_size) for path in generated.iterdir() if path.is_file()}
    result = subprocess.run([sys.executable, str(ROOT / "agentic/scripts/validate_public_reasoning_trace_pdf.py")], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "7 companion set(s)" in result.stdout
    after = {path: (path.stat().st_mtime_ns, path.stat().st_size) for path in generated.iterdir() if path.is_file()}
    assert before == after

