# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Production and adversarial tests for the sealed YM literature-to-theory chain."""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.contracts import ContractError, canonical_digest, canonical_json
from agentic.evals.ym_representational_dynamics_20260721.literature_production_chain import (
    ACQUISITION_NAME,
    CAPTURE_NAME,
    DEFAULT_AUTHORITY_ROOT,
    ORDERED_STAGE_IDS,
    LiteratureProductionChainError,
    build_publication_disabled_literature_production_chain,
    validate_literature_production_chain_manifest,
)


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "agentic" / "scripts" / "run_ym_literature_production_chain_20260722.py"
RESPONSE_DIRECTORY = "frontier_search_live_capture_20260722_tool_responses"
STARTED_AT = "2026-07-22T12:39:01Z"


@pytest.fixture(scope="module")
def manifest() -> dict[str, Any]:
    return build_publication_disabled_literature_production_chain(
        execution_started_at=STARTED_AT
    )


def _stages(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["stage_id"]: row for row in manifest["stages"]}


def _seal_top(payload: dict[str, Any], field: str = "content_digest") -> None:
    payload[field] = canonical_digest(
        {key: value for key, value in payload.items() if key != field}
    )


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_bytes(canonical_json(payload) + b"\n")


def _copy_authority(tmp_path: Path) -> Path:
    destination = tmp_path / "sealed-authority"
    destination.mkdir()
    shutil.copy2(DEFAULT_AUTHORITY_ROOT / CAPTURE_NAME, destination / CAPTURE_NAME)
    shutil.copy2(
        DEFAULT_AUTHORITY_ROOT / ACQUISITION_NAME,
        destination / ACQUISITION_NAME,
    )
    shutil.copytree(
        DEFAULT_AUTHORITY_ROOT / RESPONSE_DIRECTORY,
        destination / RESPONSE_DIRECTORY,
    )
    return destination


def _reseal_manifest(manifest: dict[str, Any]) -> None:
    order_material = [
        {
            "stage_index": row["stage_index"],
            "stage_id": row["stage_id"],
            "request_id": row["request"]["request_id"],
            "receipt_id": row["receipt"]["receipt_id"],
            "status": row["status"],
            "output_digest": row["output"]["content_digest"],
        }
        for row in manifest["stages"]
    ]
    manifest["chain_order_digest"] = canonical_digest(order_material)
    manifest["manifest_digest"] = canonical_digest(
        {key: value for key, value in manifest.items() if key != "manifest_digest"}
    )


def test_complete_chain_executes_available_stages_and_preserves_nulls(
    manifest: dict[str, Any],
) -> None:
    stages = _stages(manifest)
    assert manifest["ordered_stage_ids"] == list(ORDERED_STAGE_IDS)
    assert [row["stage_index"] for row in manifest["stages"]] == list(range(11))
    assert len(manifest["source_bundle"]["artifacts"]) == 8
    assert {row["status"] for row in manifest["stages"]} == {"succeeded"}

    mapping = stages["claim_mapping"]["output"]["payload"]["mapping_derivation"]
    assert len(mapping["theory_mappings"]) == 22
    assert {row["semantic_relation"] for row in mapping["theory_mappings"]} == {
        "unresolved"
    }
    assimilation = stages["assimilation"]["output"]["payload"]
    assert assimilation["resolution"]["freshness_status"] == "current"
    assert stages["source_routing_realization"]["status"] == "succeeded"

    portfolio = stages["high_risk_input"]["output"]["payload"]
    assert portfolio["generation_provenance"]["mode"] == (
        "operator_instantiated_from_authored_proposals"
    )
    assert portfolio["generation_provenance"]["proposal_request_digest"] is None
    assert "authored_fallback_not_proposal_field_free" in stages["high_risk_input"][
        "receipt"
    ]["reason_codes"]
    assert stages["parent_reflection"]["output"]["payload"]["generation_mode"] == (
        "local_structural_fallback"
    )
    assert stages["theory_only_synthesis"]["output"]["payload"][
        "generation_mode"
    ] == "operator_generated"

    parent_evidence = stages["parent_conceptual_adjudication"]["output"]["payload"]
    synthesis_evidence = stages["synthesis_conceptual_adjudication"]["output"][
        "payload"
    ]
    assert stages["parent_conceptual_adjudication"]["status"] == "succeeded"
    assert stages["synthesis_conceptual_adjudication"]["status"] == "succeeded"
    for stage_id in (
        "parent_conceptual_adjudication",
        "synthesis_conceptual_adjudication",
    ):
        evidence = stages[stage_id]["output"]["payload"]
        authority = evidence["content_adjudication"]["authority"]
        assert evidence["blind_packet"]["blinding_audit"]["status"] == "passed"
        assert len(evidence["judge_reports"]) == 3
        assert {
            row["adjudicator"]["lens_family"] for row in evidence["judge_reports"]
        } == {"ontological", "dialectical", "explanatory"}
        assert all(
            row["adjudicator"]["independence_claim"] == "correlated_internal"
            for row in evidence["judge_reports"]
        )
        assert len(evidence["typed_unification_closure"]["assessments"]) == 6
        assert all(
            row["graph_closed"] is True
            for row in evidence["typed_unification_closure"]["assessments"]
        )
        assert authority["plural_independent_perspectives"] is False
        assert authority["panel_evidence_class"] == "correlated_internal_critique"
        assert authority["external_human_evidence_available"] is False
        assert authority["external_human_evidence_status"] == "unavailable"
        assert authority["external_generalization_authorized"] is False

    assert stages["theory_only_synthesis"]["output"]["payload"][
        "conceptual_adjudication_evidence"
    ] == parent_evidence
    assert synthesis_evidence["input_binding"]["previous_evidence_digest"] == (
        parent_evidence["evidence_digest"]
    )
    assert synthesis_evidence["content_adjudication"]["stage_comparison"][
        "material"
    ] is False

    assert manifest["publication_enabled"] is False
    assert manifest["world_commissioning_authorized"] is False
    assert manifest["chain_status"] == "completed_before_world_commissioning"
    boundaries = copy.deepcopy(manifest["claim_boundaries"])
    assert boundaries.pop("bounded_local_production_causality") is True
    assert boundaries.pop("internal_correlated_conceptual_adjudication_executed") is True
    assert boundaries.pop("internal_deep_lens_adjudication_executed") is True
    assert set(boundaries.values()) == {False}


def test_every_stage_binds_request_receipt_output_code_and_dependencies(
    manifest: dict[str, Any],
) -> None:
    for stage in manifest["stages"]:
        request = stage["request"]
        receipt = stage["receipt"]
        implementation = stage["implementation"]
        output = stage["output"]
        assert request["stage_id"] == stage["stage_id"]
        assert request["input_bindings"]
        assert receipt["request_id"] == request["request_id"]
        assert receipt["request_digest"] == request["request_digest"]
        assert receipt["input_digest"] == request["input_digest"]
        assert receipt["output_digest"] == output["content_digest"]
        assert request["implementation_digest"] == implementation[
            "implementation_digest"
        ]
        assert receipt["implementation_digest"] == implementation[
            "implementation_digest"
        ]
        assert request["dependency_set_digest"] == implementation[
            "dependency_set_digest"
        ]
        assert receipt["dependency_set_digest"] == implementation[
            "dependency_set_digest"
        ]
        assert implementation["code_artifact"]["sha256"].startswith("sha256:")
        assert implementation["dependencies"]
        assert output["content_digest"] == canonical_digest(output["payload"])


def test_exact_manifest_replays_against_source_code_and_dependency_bytes(
    manifest: dict[str, Any],
) -> None:
    assert validate_literature_production_chain_manifest(manifest) == manifest


def test_stage_omission_is_rejected(manifest: dict[str, Any]) -> None:
    tampered = copy.deepcopy(manifest)
    del tampered["stages"][2]
    _reseal_manifest(tampered)
    with pytest.raises(ContractError):
        validate_literature_production_chain_manifest(tampered)


def test_stage_reordering_is_rejected(manifest: dict[str, Any]) -> None:
    tampered = copy.deepcopy(manifest)
    tampered["stages"][2], tampered["stages"][3] = (
        tampered["stages"][3],
        tampered["stages"][2],
    )
    _reseal_manifest(tampered)
    with pytest.raises(LiteratureProductionChainError) as exc_info:
        validate_literature_production_chain_manifest(tampered)
    assert exc_info.value.reason_code == "stage_order_invalid"


def test_stage_output_substitution_is_rejected_by_exact_replay(
    manifest: dict[str, Any],
) -> None:
    tampered = copy.deepcopy(manifest)
    mapping_output = copy.deepcopy(tampered["stages"][3]["output"]["payload"])
    assimilation_stage = tampered["stages"][4]
    assimilation_stage["output"]["payload"] = mapping_output
    assimilation_stage["output"]["content_digest"] = canonical_digest(mapping_output)
    assimilation_stage["receipt"]["output_digest"] = assimilation_stage["output"][
        "content_digest"
    ]
    _reseal_manifest(tampered)
    with pytest.raises(LiteratureProductionChainError) as exc_info:
        validate_literature_production_chain_manifest(tampered)
    assert exc_info.value.reason_code == "manifest_replay_mismatch"


def test_code_dependency_identity_substitution_is_rejected_by_exact_replay(
    manifest: dict[str, Any],
) -> None:
    tampered = copy.deepcopy(manifest)
    tampered["stages"][6]["implementation"]["dependencies"][0]["sha256"] = (
        "sha256:" + "0" * 64
    )
    _reseal_manifest(tampered)
    with pytest.raises(LiteratureProductionChainError) as exc_info:
        validate_literature_production_chain_manifest(tampered)
    assert exc_info.value.reason_code == "manifest_replay_mismatch"


def test_stale_execution_time_cannot_renew_checked_in_literature() -> None:
    with pytest.raises(LiteratureProductionChainError) as exc_info:
        build_publication_disabled_literature_production_chain(
            execution_started_at="2026-08-22T12:39:00Z"
        )
    assert exc_info.value.reason_code == "stale_literature"


def test_rehashed_target_change_is_rejected(tmp_path: Path) -> None:
    authority = _copy_authority(tmp_path)
    capture_path = authority / CAPTURE_NAME
    capture = json.loads(capture_path.read_text(encoding="utf-8"))
    capture["target_id"] = "substituted-yang-mills-target"
    _seal_top(capture)
    _write_json(capture_path, capture)
    with pytest.raises(ContractError):
        build_publication_disabled_literature_production_chain(
            authority_root=authority,
            execution_started_at=STARTED_AT,
        )


def test_rehashed_source_version_change_is_rejected(tmp_path: Path) -> None:
    authority = _copy_authority(tmp_path)
    acquisition_path = authority / ACQUISITION_NAME
    acquisition = json.loads(acquisition_path.read_text(encoding="utf-8"))
    source = next(
        row for row in acquisition["sources"] if row["source_id"] == "zenodo-21479499"
    )
    source["source_version"] = "3.0-substituted"
    _seal_top(source)
    _seal_top(acquisition)
    _write_json(acquisition_path, acquisition)
    with pytest.raises(ContractError):
        build_publication_disabled_literature_production_chain(
            authority_root=authority,
            execution_started_at=STARTED_AT,
        )


def test_rehashed_correction_status_change_is_rejected(tmp_path: Path) -> None:
    authority = _copy_authority(tmp_path)
    acquisition_path = authority / ACQUISITION_NAME
    acquisition = json.loads(acquisition_path.read_text(encoding="utf-8"))
    source = next(
        row for row in acquisition["sources"] if row["source_id"] == "arxiv-2606.19362-v1"
    )
    source["correction_status"] = "corrected"
    _seal_top(source)
    _seal_top(acquisition)
    _write_json(acquisition_path, acquisition)
    with pytest.raises(ContractError):
        build_publication_disabled_literature_production_chain(
            authority_root=authority,
            execution_started_at=STARTED_AT,
        )


def test_semantically_inert_raw_response_byte_change_is_rejected(tmp_path: Path) -> None:
    authority = _copy_authority(tmp_path)
    response_path = authority / RESPONSE_DIRECTORY / (
        "ym22-current-closest-known-work.json"
    )
    response_path.write_bytes(response_path.read_bytes() + b" ")
    with pytest.raises(ContractError):
        build_publication_disabled_literature_production_chain(
            authority_root=authority,
            execution_started_at=STARTED_AT,
        )


def test_cli_builds_validates_and_refuses_to_overwrite(tmp_path: Path) -> None:
    built_path = tmp_path / "chain.json"
    replay_path = tmp_path / "replayed-chain.json"
    build_command = [
        sys.executable,
        str(CLI),
        "--execution-started-at",
        STARTED_AT,
        "--output",
        str(built_path),
    ]
    built = subprocess.run(build_command, cwd=ROOT, text=True, capture_output=True)
    assert built.returncode == 0, built.stderr
    manifest = json.loads(built_path.read_text(encoding="utf-8"))
    assert manifest["publication_enabled"] is False

    overwrite = subprocess.run(build_command, cwd=ROOT, text=True, capture_output=True)
    assert overwrite.returncode == 1
    assert "File exists" in overwrite.stderr

    validated = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--validate-manifest",
            str(built_path),
            "--output",
            str(replay_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert validated.returncode == 0, validated.stderr
    assert replay_path.read_bytes() == built_path.read_bytes()
