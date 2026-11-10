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

import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_canonical_entry_point_is_present() -> None:
    assert (PROJECT_ROOT / "main.prism").is_file()


def test_generated_sources_do_not_depend_on_converter() -> None:
    for source in PROJECT_ROOT.rglob("*.prism"):
        text = source.read_text(encoding="utf-8")
        assert "to_prism" not in text
        assert "to-prism" not in text


def test_project_local_prism_checks_and_compiles() -> None:
    launcher = PROJECT_ROOT / "prism"
    assert launcher.is_file()
    environment = {
        "HOME": os.environ.get("HOME", ""),
        "PATH": os.environ.get("PATH", ""),
        "PYTHONNOUSERSITE": "1",
    }
    for command in ("check", "compile"):
        completed = subprocess.run(
            [str(launcher), command, "main.prism"],
            cwd=PROJECT_ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr or completed.stdout
