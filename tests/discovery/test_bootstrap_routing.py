# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Verify source-policy ordering and the absence of positive source authority."""
import copy
import os
from pathlib import Path
import sys

import pytest

from agentic.discovery.bootstrap_routing import execute_source_routing, assessment_mappings
from agentic.discovery.bootstrap_dispatch import BootstrapDispatcher, POLICY_OPERATOR, REALIZATION_OPERATOR
from agentic.discovery.contracts import ContractError, canonical_digest
from test_bootstrap_literature import acquire


def assessment_for(snapshot):
    return {"value": {"assessments": [{
        "source_id": row["source_id"], "source_excerpt": row["claims"][0],
        "relevance": "direct", "reason": "The bounded construction leaves the global obligation unresolved.",
        "credibility_concerns": ["The full proof has not been inspected."],
        "usable_for": ["Ask which finite estimate survives the limit."], "claims_verified": False,
    } for row in snapshot["sources"]]}}


def test_routing_executes_ordered_stages_from_exact_acquisition(tmp_path):
    capture, acquired, _ = acquire(tmp_path)
    snapshot = acquired["snapshot"]
    published = []
    result = execute_source_routing(acquisition_root=capture,
        acquisition_digest=acquired["manifest"]["content_digest"], target_id="target-example", run_id="run-example",
        theory_state_digest=canonical_digest({"state": 0}), assessment=assessment_for(snapshot), root=tmp_path / "routing",
        publish_policy=lambda policy: published.append(policy["policy_digest"]))
    assert published == [result["policy"]["policy_digest"]]
    assert result["assimilation"]["selected_snapshot"]["content_digest"] == snapshot["content_digest"]
    assert len(result["mappings"]) == len(snapshot["sources"])
    assert {row["relation"] for row in result["mappings"]} == {"leaves_open"}
    assert result["warrants"]["validated_warrants"] == []
    previous = result["policy"]["sealed_at"]
    for stage in result["stage_receipts"]:
        assert previous <= stage["started_at"] <= stage["completed_at"]
        previous = stage["completed_at"]
    assert previous <= result["realization"]["completed_at"]
    assert result["realization"]["stage_receipts"] == result["stage_receipts"]


def test_noise_is_retained_and_claim_fabrication_is_rejected(tmp_path):
    _, acquired, _ = acquire(tmp_path)
    snapshot = acquired["snapshot"]
    assessment = assessment_for(snapshot)
    assessment["value"]["assessments"][0]["relevance"] = "irrelevant"
    mappings = assessment_mappings(snapshot, assessment)
    assert mappings[0]["event_type"] == "justified_no_change"
    corrupt = copy.deepcopy(assessment)
    corrupt["value"]["assessments"][0]["claims_verified"] = True
    with pytest.raises(ContractError, match="cannot certify"):
        assessment_mappings(snapshot, corrupt)
    corrupt = copy.deepcopy(assessment)
    corrupt["value"]["assessments"][0]["source_excerpt"] = "This theorem proves the global target."
    with pytest.raises(ContractError, match="exact acquired excerpt"):
        assessment_mappings(snapshot, corrupt)


def test_source_pair_and_assimilation_produce_real_dispatcher_receipts(tmp_path, monkeypatch):
    monkeypatch.setenv("PATH", str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"])
    monkeypatch.setenv("PYTHONPATH", str(Path(__file__).resolve().parents[2]))
    capture, acquired, _ = acquire(tmp_path)
    snapshot = acquired["snapshot"]
    dispatcher = BootstrapDispatcher(workspace=tmp_path, root=tmp_path / "operators",
                                     target_id="target-example", run_id="run-example")
    def publish_policy(policy):
        dispatcher.dispatch(POLICY_OPERATOR, "literature_assimilation", {
            "authority_artifact": policy, "validation_inputs": {
                "authority": policy["acquisition_authority"], "snapshot": snapshot,
                "acquisition_producer_receipt": policy["acquisition_completion"],
                "algorithm_contracts": policy["algorithm_contracts"]}},
            parameters={"producer_role": "source_routing_pre_map_policy", "artifact_id": policy["policy_id"],
                        "artifact_digest": canonical_digest(policy)})
    def assimilate(snapshot, mappings, policy):
        output, _, _ = dispatcher.dispatch("frontier-literature-assimilator", "literature_assimilation", {
            "snapshot": snapshot, "theory_mappings": mappings, "source_routing_pre_map_policy": policy})
        return output
    result = execute_source_routing(acquisition_root=capture,
        acquisition_digest=acquired["manifest"]["content_digest"], target_id="target-example", run_id="run-example",
        theory_state_digest=canonical_digest({"state": 0}), assessment=assessment_for(snapshot), root=tmp_path / "routing",
        publish_policy=publish_policy, assimilation_operator=assimilate)
    realization = result["realization"]
    dispatcher.dispatch(REALIZATION_OPERATOR, "literature_assimilation", {
        "authority_artifact": realization, "validation_inputs": {
            "policy": result["policy"], "authority": result["authority"], "snapshot": snapshot,
            "acquisition_producer_receipt": result["acquisition_receipt"],
            "algorithm_contracts": result["policy"]["algorithm_contracts"],
            "validated_warrants": result["warrants"]["validated_warrants"],
            "claim_mappings": result["mappings"], "assimilation": result["assimilation"],
            "stage_receipts": result["stage_receipts"]}},
        parameters={"producer_role": "source_routing_realization", "artifact_id": realization["realization_id"],
                    "artifact_digest": canonical_digest(realization)})
    assert len(dispatcher.receipts) == 3
    assert all(row["status"] == "succeeded" and row["validator_receipts"] for row in dispatcher.receipts)
