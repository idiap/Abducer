# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Focused regressions for the non-mutating default repository gate."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "agentic" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import agentic_check  # noqa: E402


def test_public_reasoning_trace_validator_is_in_default_read_only_gate() -> None:
    script = "agentic/scripts/validate_public_reasoning_trace.py"
    assert script in agentic_check.PIPELINE
    assert script in agentic_check.READ_ONLY_VALIDATORS
    assert script not in agentic_check.REFRESH_ONLY_VALIDATORS


def test_default_gate_reports_exact_refresh_only_omissions(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["agentic_check.py"])
    monkeypatch.setattr(agentic_check, "_run_read_only_gate", lambda scripts: 0)
    assert agentic_check.main() == 0
    output = capsys.readouterr().out
    assert "default read-only" in output
    for script in agentic_check.REFRESH_ONLY_VALIDATORS:
        assert script in output


def test_read_only_gate_checks_post_state_even_when_validator_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    snapshots = iter([{"a": "old"}, {"a": "new"}])
    monkeypatch.setattr(agentic_check, "_repository_snapshot", lambda: next(snapshots))
    monkeypatch.setattr(agentic_check, "_run_scripts", lambda scripts: 7)
    assert agentic_check._run_read_only_gate(("validator.py",)) == 4


def test_repository_snapshot_includes_ignored_evidence_directories_and_symlinks(
    tmp_path: Path,
) -> None:
    evidence = tmp_path / "agentic" / "reports" / "ignored-evidence"
    evidence.mkdir(parents=True)
    (evidence / "receipt.json").write_text("{}", encoding="utf-8")
    (tmp_path / "evidence-link").symlink_to(evidence, target_is_directory=True)
    snapshot = agentic_check._repository_snapshot(tmp_path)
    assert "agentic/reports/ignored-evidence/receipt.json" in snapshot
    assert snapshot["evidence-link"].startswith("symlink:")
