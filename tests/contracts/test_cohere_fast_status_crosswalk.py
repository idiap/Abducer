# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_status_crosswalk_is_conservative_and_negative_states_are_sticky():
    data = yaml.safe_load((ROOT / "agentic/registries/cohere_fast_status_crosswalk.yaml").read_text())
    assert data["unsupported"] == "reject"
    assert data["mappings"]["validated"]["epistemic"] == "candidate"
    for state in ("falsified", "retracted", "superseded"):
        assert data["mappings"][state]["sticky_negative"] is True
    assert any("never implies proof" in rule for rule in data["rules"])
