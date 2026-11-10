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
def test_isolated_contract_extends_without_changing_existing_registry():
    base=json.loads((ROOT/"agentic/registries/named_workflow_contracts.yaml").read_text())
    isolated=json.loads((ROOT/"agentic/registries/cohere_fast_workflow_contracts.yaml").read_text())["workflow"]
    assert len(base["workflows"]) == 6
    assert isolated["id"] not in {w["id"] for w in base["workflows"]}
    assert isolated["artifact_namespace"].startswith("cohere-fast/")
    assert isolated["domain_binding_required"] and isolated["children"]
def test_children_have_one_parent_and_no_cross_namespace_returns():
    parent=json.loads((ROOT/"agentic/registries/cohere_fast_subworkflows.yaml").read_text())
    assert parent["parent_workflow"] == "cohere_fast"
    assert len({c["id"] for c in parent["subworkflows"]}) == len(parent["subworkflows"])
