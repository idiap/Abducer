# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regression tests for proposal-field-free high-risk operator orchestration.

The tests exercise the causal boundary that ordinary portfolio-shape tests do
not see: a study must run and replay before dispatch, its immutable selection
must pass protocol controls, and the operator may consume only that selected
provider output.  Target-authored candidates remain a blinded baseline.
"""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    artifact_descriptor,
    canonical_digest,
    canonical_json,
    load_json,
)
from agentic.discovery.hypotheses import build_demo_high_risk_portfolio
from agentic.discovery.literature import build_demo_literature_snapshot
from agentic.discovery.receipts import build_operator_request
from agentic.scripts.run_discovery_operator_protocol import (
    _high_risk,
    prepare_proposal_field_free_high_risk_envelope,
)


ROOT = Path(__file__).resolve().parents[2]


def _inputs() -> tuple[dict, dict, list[dict]]:
    snapshot = build_demo_literature_snapshot(target_id="upstream-high-risk-target")
    charter = {
        "target_id": snapshot["target_id"],
        "target_statement": "Explain exact global recurrence without weakening its quantifiers.",
        "theory_state_digest": snapshot["theory_state_digest"],
        "root_tensions": [
            "Local witnesses do not explain global recurrence.",
            "Distinct barriers lack a common explanatory relation.",
        ],
        "target_commitments": ["Preserve the exact target and quantifier order."],
        "protected_successes": ["Recover the verified boundary regime."],
        "forbidden_target_drift": "No finite-only, average-case, or lexical proxy.",
    }
    baseline = copy.deepcopy(build_demo_high_risk_portfolio(snapshot)["hypotheses"])
    return snapshot, charter, baseline


def _request(namespace: Namespace) -> dict:
    return {
        "identity": namespace.as_dict(),
        "parameters": {"requested_count": 10, "relevance_floor": 0.70},
    }


def test_upstream_study_and_selection_are_immutable_exact_and_baseline_only(
    tmp_path: Path,
) -> None:
    snapshot, charter, baseline = _inputs()
    namespace = Namespace(snapshot["target_id"], "run-upstream", "root", 0)
    envelope = prepare_proposal_field_free_high_risk_envelope(
        charter=charter,
        literature_snapshot=snapshot,
        workspace=tmp_path,
        namespace=namespace,
        authored_incumbent_comparison_proposals=baseline,
        repetitions=5,
        requested_count=10,
        counterbalance_seed="focused-upstream-test",
    )

    assert "proposals" not in envelope
    bindings = envelope["proposal_field_free_upstream"]
    study = load_json(tmp_path / bindings["study_artifact"]["path"])
    selection = load_json(tmp_path / bindings["selection_artifact"]["path"])
    assert len(study["repetitions"]) == 5
    assert study["generation_mode"] == "proposal_field_free_authored_operator"
    assert study["equal_count_authored_incumbent_comparison"]["source_proposals_digest"] == (
        canonical_digest(baseline)
    )
    assert study["equal_count_authored_incumbent_comparison"][
        "generation_opportunity_matched"
    ] is False
    assert selection["protocol_controls"] == {
        "repeated_diversity_status": "passed",
        "known_authored_copy_controls_passed": True,
        "selection_status": "selected_for_internal_exploration",
        "selection_policy_digest": study["exploration_selection"][
            "selection_policy_digest"
        ],
    }
    selected = study["repetitions"][selection["selected_repetition_index"]]
    assert study["schema_version"] == "3.0"
    assert selection["schema_version"] == "3.0"
    assert selection["selected_schedule_slot_id"] == selected["schedule_slot_id"]
    assert selection["selected_semantic_content_id"] == selected["semantic_content_id"]
    assert study["exploration_selection"]["selected_semantic_content_id"] == selected[
        "semantic_content_id"
    ]
    assert selection["selected_semantic_output_id"] == selected["semantic_output_id"]
    assert selection["selected_semantic_repetition_id"] == selected["semantic_output_id"]
    assert selection["selected_repetition_id"] == selected["evidence_repetition_id"]
    assert selection["exploration_selection"] == study["exploration_selection"]
    assert envelope["selected_proposals"] == selected["provider_output"]["proposals"]
    assert envelope["generation_provenance"] == selected["portfolio"][
        "generation_provenance"
    ]

    portfolio, unknowns = _high_risk(
        _request(namespace), envelope, tmp_path
    )
    assert portfolio == selected["portfolio"]
    assert portfolio["generation_provenance"]["mode"] == (
        "proposal_field_free_authored_operator"
    )
    assert any("does not establish provider independence" in row for row in unknowns)


def test_upstream_rejects_tampered_selection_or_selected_provenance(
    tmp_path: Path,
) -> None:
    snapshot, charter, baseline = _inputs()
    namespace = Namespace(snapshot["target_id"], "run-tamper", "root", 0)
    envelope = prepare_proposal_field_free_high_risk_envelope(
        charter=charter,
        literature_snapshot=snapshot,
        workspace=tmp_path,
        namespace=namespace,
        authored_incumbent_comparison_proposals=baseline,
    )

    forged = copy.deepcopy(envelope)
    forged["generation_provenance"]["generator_authority_id"] = "forged-authority"
    with pytest.raises(ContractError, match="generation provenance differs"):
        _high_risk(_request(namespace), forged, tmp_path)

    selection_path = tmp_path / envelope["proposal_field_free_upstream"][
        "selection_artifact"
    ]["path"]
    original_selection = load_json(selection_path)
    forged_selection = copy.deepcopy(original_selection)
    forged_selection["selected_semantic_content_id"] = (
        "elicitation-semantic-content.forged"
    )
    forged_selection["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in forged_selection.items()
            if key != "content_digest"
        }
    )
    selection_path.write_bytes(canonical_json(forged_selection) + b"\n")
    forged_envelope = copy.deepcopy(envelope)
    forged_envelope["proposal_field_free_upstream"]["selection_artifact"] = (
        artifact_descriptor(selection_path, tmp_path, namespace)
    )
    with pytest.raises(ContractError, match="selection differs from the replayed study"):
        _high_risk(_request(namespace), forged_envelope, tmp_path)

    selection_path.write_bytes(canonical_json(original_selection) + b"\n")
    selection_path.write_bytes(selection_path.read_bytes() + b" ")
    with pytest.raises(ContractError, match="artifact digest mismatch"):
        _high_risk(_request(namespace), envelope, tmp_path)


def test_less_than_five_repetitions_and_direct_proposal_fields_fail_closed(
    tmp_path: Path,
) -> None:
    snapshot, charter, baseline = _inputs()
    namespace = Namespace(snapshot["target_id"], "run-floor", "root", 0)
    with pytest.raises(ContractError, match="at least five repetitions"):
        prepare_proposal_field_free_high_risk_envelope(
            charter=charter,
            literature_snapshot=snapshot,
            workspace=tmp_path,
            namespace=namespace,
            authored_incumbent_comparison_proposals=baseline,
            repetitions=4,
        )

    with pytest.raises(ContractError, match="direct proposal fields are not accepted"):
        _high_risk(
            _request(namespace),
            {
                "charter": charter,
                "literature_snapshot": snapshot,
                "proposals": baseline,
            },
            tmp_path,
        )


def test_operator_and_independent_validator_replay_upstream_across_processes(
    tmp_path: Path,
) -> None:
    snapshot, charter, incumbent = _inputs()
    namespace = Namespace(snapshot["target_id"], "run-cross-process", "root", 0)
    envelope = prepare_proposal_field_free_high_risk_envelope(
        charter=charter,
        literature_snapshot=snapshot,
        workspace=tmp_path,
        namespace=namespace,
        authored_incumbent_comparison_proposals=incumbent,
        counterbalance_seed="cross-process-upstream-test",
    )
    envelope_path = tmp_path / "inputs" / "high-risk-envelope.json"
    envelope_path.parent.mkdir(parents=True, exist_ok=True)
    envelope_path.write_bytes(canonical_json(envelope) + b"\n")
    output_relative = "outputs/high-risk-portfolio.json"
    request = build_operator_request(
        operator_id="high-risk-hypothesis-forger",
        operator_version="1.0.0",
        kind="hypothesis",
        namespace=namespace,
        invocation_id="cross-process-high-risk",
        input_artifacts=[artifact_descriptor(envelope_path, tmp_path, namespace)],
        declared_outputs=[output_relative],
        parameters={"requested_count": 10, "relevance_floor": 0.70},
        required=True,
        requested_at="2026-07-22T00:00:00Z",
    )
    operator = subprocess.run(
        [
            sys.executable,
            str(ROOT / "agentic/scripts/run_discovery_operator_protocol.py"),
            "--operator-id",
            "high-risk-hypothesis-forger",
            "--workspace",
            str(tmp_path),
        ],
        cwd=ROOT,
        input=canonical_json(request),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert operator.returncode == 0, operator.stderr.decode()
    output_path = tmp_path / output_relative
    assert load_json(output_path) == envelope["selected_portfolio"]

    validation_protocol = {
        "request": request,
        "artifacts": [artifact_descriptor(output_path, tmp_path, namespace)],
    }
    validator = subprocess.run(
        [
            sys.executable,
            str(ROOT / "agentic/scripts/validate_discovery_operator_protocol.py"),
            "--operator-id",
            "high-risk-hypothesis-forger",
            "--workspace",
            str(tmp_path),
        ],
        cwd=ROOT,
        input=canonical_json(validation_protocol),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert validator.returncode == 0, validator.stderr.decode()


def test_ym_runner_routes_authored_domain_deck_only_to_incumbent_comparison() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "agentic/scripts/run_ym_canonical_parent_cycle_20260721.py"
    ).read_text(encoding="utf-8")
    assert "def _authored_domain_template_incumbent_comparison_proposals(" in source
    assert "authored_incumbent_comparison_proposals=(" in source
    assert "_authored_domain_template_incumbent_comparison_proposals(snapshot)" in source
    assert '"proposals": _proposals(snapshot)' not in source
