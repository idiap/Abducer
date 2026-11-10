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
import stat
import subprocess
import sys
from pathlib import Path

import pytest

from agentic.testing.generate_cohere_fast_scenarios import validate

ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "agentic/testing/generate_cohere_fast_scenarios.py"
FIXTURE = ROOT / "tests/fixtures/cohere_fast/ym/codex_exec_scenarios.json"


def test_checked_in_codex_exec_corpus_is_semantically_valid() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    validate(payload)
    assert payload["generator"] == "codex-exec"


def test_generator_invokes_codex_exec_with_schema_and_read_only_sandbox(tmp_path: Path) -> None:
    recorded = tmp_path / "argv.json"
    fake = tmp_path / "codex"
    fixture = FIXTURE.read_text(encoding="utf-8")
    fake.write_text(
        "#!/usr/bin/env python3\n"
        "import json, pathlib, sys\n"
        f"pathlib.Path({str(recorded)!r}).write_text(json.dumps(sys.argv[1:]))\n"
        "out = pathlib.Path(sys.argv[sys.argv.index('--output-last-message') + 1])\n"
        f"out.write_text({fixture!r})\n",
        encoding="utf-8",
    )
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    output = tmp_path / "scenarios.json"
    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--codex", str(fake), "--output", str(output)],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    argv = json.loads(recorded.read_text(encoding="utf-8"))
    assert argv[0] == "exec"
    assert "--ephemeral" in argv
    assert argv[argv.index("--sandbox") + 1] == "read-only"
    assert Path(argv[argv.index("--output-schema") + 1]) == ROOT / "agentic/spec/cohere_fast_generative_scenarios.schema.json"
    assert json.loads(output.read_text(encoding="utf-8"))["scenarios"]


def test_generator_rejects_incomplete_scenario_coverage() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["scenarios"] = payload["scenarios"][:1]
    with pytest.raises(Exception):
        validate(payload)
