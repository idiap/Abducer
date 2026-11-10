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


def test_release_gate_is_structurally_valid_and_default_off() -> None:
    result = subprocess.run([sys.executable, "agentic/scripts/validate_cohere_fast_release.py"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((ROOT / "agentic/reports/cohere_fast_release/latest.json").read_text())
    assert report["release_enabled"] is False
    assert report["disposition"] in {"blocked", "ready_but_disabled"}
    assert "source_license" in report["blocked_checks"]
