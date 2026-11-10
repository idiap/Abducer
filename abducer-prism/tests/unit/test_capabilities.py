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

from pathlib import Path

from to_prism.capabilities import probe_prism

KIT_ROOT = Path(__file__).resolve().parents[2]


def test_public_prism_capability_probe() -> None:
    result = probe_prism(str(KIT_ROOT / ".venv/bin/prism"))
    assert set(result["commands"]) == {
        "parse",
        "check",
        "compile",
        "run",
        "verify-run",
        "build",
    }
    assert result["matrix"]["typed-domain-input"]["cli"] == "fixture-harness-only"
