# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
import importlib.util, json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("cf_intake", ROOT/"hooks/scripts/cohere_fast_intake.py"); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
def test_explicit_domain_and_child_are_deterministic(monkeypatch):
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    a=mod.parse_invocation("cohere-fast ym", target="mass gap")
    b=mod.parse_invocation("cohere-fast ym", target="mass gap")
    assert a == b and a["workflow_id"] == "cohere_fast" and a["domain_id"] == "ym"
    child=mod.parse_invocation("cohere-fast ym independent-audit", target="mass gap")
    assert child["subworkflow_id"] == "independent-audit"
@pytest.mark.parametrize("command", ["cohere-fast", "study YM", "cohere_fast ym", "cohere-fast unknown", "cohere-fast ym nope", "cohere-fast ym independent-audit extra"])
def test_ambiguous_or_implicit_commands_fail(command):
        with pytest.raises(ValueError): mod.parse_invocation(command, target="mass gap")
def test_disabled_domain_fails_closed_without_feature_flag(monkeypatch):
    monkeypatch.delenv("ABDUCER_ENABLE_COHERE_FAST", raising=False)
    with pytest.raises(ValueError): mod.parse_invocation("cohere-fast ym", target="mass gap")
