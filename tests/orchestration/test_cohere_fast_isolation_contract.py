# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def load(path): return json.loads((ROOT/path).read_text())
def test_isolation_contract_is_explicit_and_abducer_native():
    c=load("agentic/spec/cohere_fast_isolation_contract.yaml")
    assert c["workflow_id"] == "cohere_fast" and c["activation"] == "explicit_only"
    assert c["canonical_state_authority"] == "abducer"
    assert "tdr" in c["forbidden_control_planes"]
    assert c["run_root_template"].startswith("artifacts/cohere-fast/")
def test_existing_registry_does_not_default_route_cohere_fast():
    named=load("agentic/registries/named_workflow_contracts.yaml")
    assert all(w["id"] != "cohere_fast" for w in named["workflows"])
