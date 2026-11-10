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
import pytest
from agentic.orchestration.cohere_fast_runner import CohereFastRunner

ACT={"receipt_type":"cohere_fast_activation","workflow_id":"cohere_fast","domain_id":"ym","run_id":"cf-123456789012345678901234","subworkflow_id":None}
def test_runner_writes_receipts_only_in_isolated_root(tmp_path):
    runner=CohereFastRunner(tmp_path)
    def execute(child, packet): return {"state":"accepted","packet":{"previous":child["return_type"]},"artifacts":{f"packets/{child['id']}.json":"{}"}}
    result=runner.run(ACT,{"target":"mass gap"},execute)
    assert result["state"] == "accepted" and len(result["steps"]) == 5
    assert Path(result["run_root"]).is_relative_to(tmp_path)
    assert all((Path(result["run_root"])/"receipts"/f"{r['step_id']}.json").exists() for r in result["steps"])
def test_quarantine_prevents_later_execution(tmp_path):
    seen=[]
    def execute(child, packet):
        seen.append(child["id"]); return {"state":"quarantined" if child["id"]=="derivation-and-proof" else "accepted"}
    result=CohereFastRunner(tmp_path).run(ACT,{},execute)
    assert result["state"] == "quarantined" and seen[-1] == "derivation-and-proof"
def test_artifact_escape_fails_closed(tmp_path):
    with pytest.raises(ValueError): CohereFastRunner(tmp_path).run(ACT,{},lambda c,p:{"state":"accepted","artifacts":{"../../escape":"bad"}})
def test_replay_receipt_identity_is_deterministic(tmp_path):
    run=CohereFastRunner(tmp_path)
    fn=lambda c,p:{"state":"accepted","artifacts":{}}
    a=run.run(ACT,{},fn); b=run.run(ACT,{},fn)
    assert [r["receipt_id"] for r in a["steps"]] == [r["receipt_id"] for r in b["steps"]]
def test_retry_is_bounded_by_child_budget(tmp_path):
    attempts={}
    def execute(child, packet):
        attempts[child["id"]]=attempts.get(child["id"],0)+1
        if child["id"]=="adaptive-frontier" and attempts[child["id"]] < 3: return {"state":"failed"}
        return {"state":"accepted"}
    result=CohereFastRunner(tmp_path).run(ACT,{},execute)
    assert result["state"] == "accepted" and attempts["adaptive-frontier"] == 3
