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

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "hooks/scripts"))
from cohere_fast_intake import parse_invocation


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def test_existing_named_registry_is_not_a_cohere_fast_mutation_surface() -> None:
    registry = json.loads((ROOT / "agentic/registries/named_workflow_contracts.yaml").read_text())
    assert len(registry["workflows"]) == 6
    assert all(row["id"] != "cohere_fast" for row in registry["workflows"])
    isolated = json.loads((ROOT / "agentic/registries/cohere_fast_workflow_contracts.yaml").read_text())
    assert isolated["workflow"]["id"] == "cohere_fast"


def test_generic_domain_text_does_not_parse_as_activation() -> None:
    for text in ("work on Yang-Mills", "ym", "cohere-fast", "please cohere the ym proof"):
        try:
            parse_invocation(text, target="yang-mills")
        except ValueError:
            pass
        else:
            raise AssertionError(f"implicit activation accepted: {text}")


def test_existing_workflow_validators_still_pass() -> None:
    before = sha("agentic/registries/named_workflow_contracts.yaml")
    commands = [
        [sys.executable, "agentic/scripts/validate_workflow_contracts.py"],
        [sys.executable, "agentic/scripts/validate_named_workflow_trace_contracts.py"],
        [sys.executable, "agentic/scripts/run_hook_contract_tests.py"],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
    assert sha("agentic/registries/named_workflow_contracts.yaml") == before
