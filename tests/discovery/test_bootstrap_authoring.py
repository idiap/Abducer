# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Exercise the authored-proposal path against the original independent validator."""
import copy

import pytest

from agentic.discovery.bootstrap_authoring import compile_proposals, proposal_schema, produce_portfolio
from agentic.discovery.bootstrap_reflection import system_schema
from agentic.discovery.contracts import ContractError, canonical_digest
from agentic.discovery.model_author import validate_value
from agentic.scripts.run_discovery_operator_protocol import _high_risk
from agentic.scripts.validate_discovery_operator_protocol import validate
from tests.discovery.test_proposal_field_free_operator_upstream import _inputs


def inputs():
    snapshot, charter, candidates = _inputs()
    fields = set(proposal_schema()["properties"])
    proposals = [{key: copy.deepcopy(row[key]) for key in fields} for row in candidates]
    proposals[0]["mechanism"] = "A newly authored mechanism retained exactly through the source producer."
    blind = {"value": {"proposals": proposals}, "content_digest": canonical_digest(proposals)}
    rebases = [{"mechanism_key": row["mechanism_key"], "literature_relation": "coverage_unknown",
                "source_ids": [], "rationale": "The bounded sources do not resolve this conjecture.",
                "remaining_checks": ["Check a complete argument in primary sources."]} for row in proposals]
    rebase = {"value": {"rebases": rebases}}
    return snapshot, charter, blind, rebase


def test_all_ideas_are_authored_and_original_operator_consumes_them(tmp_path):
    snapshot, charter, blind, rebase = inputs()
    for row in blind["value"]["proposals"]:
        validate_value(row, proposal_schema(), None)
    proposals = compile_proposals(charter=charter, blind=blind, rebase=rebase)
    request = {"identity": {"target_id": snapshot["target_id"]}, "parameters": {},
               "operator": {"operator_id": "high-risk-hypothesis-forger"}}
    envelope = {"charter": charter, "literature_snapshot": snapshot, "authored_proposals": proposals}
    output, _ = _high_risk(request, envelope, tmp_path)
    assert output == produce_portfolio(charter=charter, snapshot=snapshot, blind=blind, rebase=rebase)
    by_key = {row["mechanism_key"]: row for row in output["hypotheses"]}
    for proposal in proposals:
        for field in proposal_schema()["properties"]:
            assert by_key[proposal["mechanism_key"]][field] == proposal[field]
    assert output["generation_provenance"]["generator_authority_id"] == "operator.supplied-proposals"
    assert all(row["literature_relation"] == "coverage_unknown" for row in output["hypotheses"])
    validate("high-risk-hypothesis-forger", request, envelope, output, workspace=tmp_path)
    # A separately valid template portfolio cannot substitute for the authored input.
    other, _ = _high_risk(request, {key: value for key, value in envelope.items() if key != "authored_proposals"}, tmp_path)
    with pytest.raises(ContractError, match="exact authored-proposal"):
        validate("high-risk-hypothesis-forger", request, envelope, other, workspace=tmp_path)


def test_authoring_schema_requires_full_content_and_excludes_ledger_authority():
    schema = proposal_schema()
    assert set(schema["required"]) == set(schema["properties"])
    assert not {"selection_status", "literature_rebase_receipt", "blind_articulation_digest"} & set(schema["properties"])
    with pytest.raises(ContractError, match="required property"):
        validate_value({"mechanism": "An underspecified idea"}, schema, None)
    reflection = system_schema()
    assert "structural_identity" not in reflection["properties"]
    assert "lifecycle_state" not in reflection["properties"]
