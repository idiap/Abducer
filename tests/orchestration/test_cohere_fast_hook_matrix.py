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
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("cf_policy",ROOT/"hooks/scripts/cohere_fast_policy.py"); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
def base():
    activation={"receipt_type":"cohere_fast_activation","workflow_id":"cohere_fast","domain_id":"ym","run_id":"cf-run"}
    return {**activation,"activation_receipt":activation,"skill":"cohere-fast-orchestrator","artifact_prefix":"cohere-fast/ym/cf-run/","subworkflow_id":None,"parent_run_id":None,"parent_event_id":None}
def test_bound_parent_request_is_accepted(monkeypatch):
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    assert mod.authorize(base())["decision"] == "accept"
def test_cross_run_domain_workflow_and_namespace_are_blocked(monkeypatch):
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    cases=[]
    for key,value in [("run_id","other"),("domain_id","other"),("workflow_id","proof_consolidation"),("artifact_prefix","cohere-fast/ym/other/")]:
        p=base(); p[key]=value; cases.append(p)
    assert all(mod.authorize(p)["decision"] == "block" for p in cases)
def test_child_requires_valid_lineage(monkeypatch):
    monkeypatch.setenv("ABDUCER_ENABLE_COHERE_FAST", "true")
    p=base(); p["subworkflow_id"]="independent-audit"
    assert mod.authorize(p)["decision"] == "block"
    p["parent_run_id"]="cf-parent"; p["parent_event_id"]="forged"
    assert mod.authorize(p)["decision"] == "block"
    p["parent_event_id"]="evt-parent"
    assert mod.authorize(p)["decision"] == "accept"
