# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial tests for the portable literature-production input boundary."""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    canonical_json,
    stable_identifier,
)
from agentic.discovery.literature_production_commitment import (
    LiteratureProductionCommitmentError,
    build_portable_literature_production_input_receipt,
    reopen_portable_literature_production_input,
    validate_portable_literature_production_input_receipt,
)
from agentic.evals.ym_representational_dynamics_20260721.literature_production_chain import (
    build_publication_disabled_literature_production_chain,
)


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "agentic" / "scripts" / "run_literature_production_commitment.py"
STARTED_AT = "2026-07-22T12:39:01Z"
MANIFEST_PATH = "committed/literature-production/manifest.json"


@pytest.fixture(scope="module")
def manifest() -> dict[str, Any]:
    return build_publication_disabled_literature_production_chain(
        execution_started_at=STARTED_AT
    )


def _write_manifest(
    root: Path,
    value: dict[str, Any],
    relative_path: str = MANIFEST_PATH,
) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json(value) + b"\n")
    return path


def _receipt(root: Path, value: dict[str, Any]) -> dict[str, Any]:
    _write_manifest(root, value)
    return build_portable_literature_production_input_receipt(
        root,
        MANIFEST_PATH,
    )


def _reseal_receipt(value: dict[str, Any]) -> None:
    descriptor = value["descriptor"]
    descriptor["descriptor_digest"] = canonical_digest(
        {
            key: child
            for key, child in descriptor.items()
            if key != "descriptor_digest"
        }
    )
    projection = value["consumer_projection"]
    projection["projection_digest"] = canonical_digest(
        {
            key: child
            for key, child in projection.items()
            if key != "projection_digest"
        }
    )
    value["receipt_id"] = stable_identifier(
        "literature-input-receipt",
        descriptor["descriptor_digest"],
        projection["projection_digest"],
    )
    value["receipt_digest"] = canonical_digest(
        {key: child for key, child in value.items() if key != "receipt_digest"}
    )


def test_typed_adjudication_systems_are_stage_internal_not_upstream_authority(
    manifest: dict[str, Any],
) -> None:
    stages = {row["stage_id"]: row for row in manifest["stages"]}
    forbidden = {
        "typed_parent_systems",
        "typed_synthesis_systems",
        "typed_conceptual_systems",
    }
    for stage in manifest["stages"]:
        roles = {row["role"] for row in stage["request"]["input_bindings"]}
        assert roles.isdisjoint(forbidden)
        if stage["stage_id"] not in {
            "parent_conceptual_adjudication",
            "synthesis_conceptual_adjudication",
        }:
            assert stage["derived_intermediates"] == []

    expected_sources = {
        "parent_conceptual_adjudication": "parent_reflection",
        "synthesis_conceptual_adjudication": "theory_only_synthesis",
    }
    for stage_id, source_role in expected_sources.items():
        [derived] = stages[stage_id]["derived_intermediates"]
        assert derived["role"] == "typed_conceptual_systems"
        assert derived["derivation_kind"] == (
            "stage_internal_deterministic_projection"
        )
        assert derived["derived_from_input_roles"] == [source_role]
        assert derived["row_count"] == 6
        assert derived["authority_class"] == (
            "derived_non_authoritative_intermediate"
        )


def test_receipt_reopens_exact_bytes_and_preserves_every_authority_limit(
    tmp_path: Path,
    manifest: dict[str, Any],
) -> None:
    receipt = _receipt(tmp_path, manifest)
    assert validate_portable_literature_production_input_receipt(
        tmp_path, receipt
    ) == receipt
    projection = reopen_portable_literature_production_input(tmp_path, receipt)
    assert projection == receipt["consumer_projection"]
    assert receipt["descriptor"]["path"] == MANIFEST_PATH
    assert receipt["descriptor"]["semantic_digest"] == canonical_digest(manifest)
    assert str(tmp_path.resolve()) not in json.dumps(receipt, sort_keys=True)

    validation_scope = receipt["validation_scope"]
    assert validation_scope["exact_manifest_bytes_reopened"] is True
    assert validation_scope["manifest_internal_causal_invariants_validated"] is True
    assert validation_scope["source_bundle_reexecution_performed"] is False
    assert validation_scope["code_dependency_reexecution_performed"] is False
    assert validation_scope["runtime_root_persisted"] is False

    provenance = projection["theory_generation_provenance"]
    assert provenance["proposal_field_free"] is False
    assert provenance["high_risk"]["mode"] == (
        "operator_instantiated_from_authored_proposals"
    )
    assert provenance["high_risk"]["proposal_request_digest"] is None
    assert provenance["high_risk"]["generator_policy_digest"] is None
    assert provenance["high_risk"]["scoring_policy_digest"] is None
    assert provenance["parent_reflection_generation_mode"] == (
        "local_structural_fallback"
    )
    assert provenance["theory_only_synthesis_generation_mode"] == (
        "operator_generated"
    )

    materiality = projection["synthesis_materiality"]
    assert materiality["material"] is False
    assert materiality["new_reflection_rounds"] == 0
    assert materiality["improved_dimensions"] == []
    assert materiality["semantic_patch_content_changed"] is False
    assert materiality["semantic_patch_change_count"] == 0

    for authority_field in (
        "parent_adjudication_authority",
        "synthesis_adjudication_authority",
    ):
        authority = projection[authority_field]
        assert authority["panel_evidence_class"] == (
            "correlated_internal_critique"
        )
        assert authority["plural_independent_perspectives"] is False
        assert authority["external_human_evidence_available"] is False
        assert authority["external_human_evidence_status"] == "unavailable"
        assert authority["external_generalization_authorized"] is False

    boundaries = copy.deepcopy(projection["claim_boundaries"])
    assert boundaries.pop("bounded_local_production_causality") is True
    assert boundaries.pop(
        "internal_correlated_conceptual_adjudication_executed"
    ) is True
    assert boundaries.pop("internal_deep_lens_adjudication_executed") is True
    assert set(boundaries.values()) == {False}
    assert projection["publication_enabled"] is False
    assert projection["world_commissioning_authorized"] is False


def test_receipt_is_deterministic_for_one_exact_snapshot(
    tmp_path: Path,
    manifest: dict[str, Any],
) -> None:
    first = _receipt(tmp_path, manifest)
    second = build_portable_literature_production_input_receipt(
        tmp_path,
        MANIFEST_PATH,
    )
    assert second == first


def test_noncanonical_manifest_serialization_is_rejected(
    tmp_path: Path,
    manifest: dict[str, Any],
) -> None:
    path = tmp_path / MANIFEST_PATH
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(LiteratureProductionCommitmentError) as exc_info:
        build_portable_literature_production_input_receipt(
            tmp_path,
            MANIFEST_PATH,
        )
    assert exc_info.value.reason_code == "manifest_bytes_not_canonical"


def test_exact_manifest_byte_substitution_is_rejected(
    tmp_path: Path,
    manifest: dict[str, Any],
) -> None:
    receipt = _receipt(tmp_path, manifest)
    substituted = build_publication_disabled_literature_production_chain(
        execution_started_at="2026-07-22T12:39:02Z"
    )
    _write_manifest(tmp_path, substituted)
    with pytest.raises(LiteratureProductionCommitmentError) as exc_info:
        reopen_portable_literature_production_input(tmp_path, receipt)
    assert exc_info.value.reason_code in {
        "manifest_bytes_size_mismatch",
        "manifest_bytes_digest_mismatch",
    }


def test_rehashed_derived_intermediate_substitution_is_rejected(
    tmp_path: Path,
    manifest: dict[str, Any],
) -> None:
    tampered = copy.deepcopy(manifest)
    parent_stage = next(
        row
        for row in tampered["stages"]
        if row["stage_id"] == "parent_conceptual_adjudication"
    )
    parent_stage["derived_intermediates"][0]["content_digest"] = (
        "sha256:" + "0" * 64
    )
    tampered["manifest_digest"] = canonical_digest(
        {
            key: child
            for key, child in tampered.items()
            if key != "manifest_digest"
        }
    )
    _write_manifest(tmp_path, tampered)
    with pytest.raises(LiteratureProductionCommitmentError) as exc_info:
        build_portable_literature_production_input_receipt(
            tmp_path,
            MANIFEST_PATH,
        )
    assert exc_info.value.reason_code == "derived_intermediate_evidence_mismatch"


def test_fully_rehashed_descriptor_projection_substitution_is_rejected(
    tmp_path: Path,
    manifest: dict[str, Any],
) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first = _receipt(first_root, manifest)
    substituted = build_publication_disabled_literature_production_chain(
        execution_started_at="2026-07-22T12:39:02Z"
    )
    second = _receipt(second_root, substituted)

    forged = copy.deepcopy(first)
    forged["descriptor"] = copy.deepcopy(second["descriptor"])
    _reseal_receipt(forged)
    with pytest.raises(LiteratureProductionCommitmentError) as exc_info:
        reopen_portable_literature_production_input(second_root, forged)
    assert exc_info.value.reason_code == "receipt_projection_identity_mismatch"


def test_receipt_reopens_after_whole_root_relocation_and_source_deletion(
    tmp_path: Path,
    manifest: dict[str, Any],
) -> None:
    original = tmp_path / "original"
    receipt = _receipt(original, manifest)
    expected = reopen_portable_literature_production_input(original, receipt)
    relocated = tmp_path / "relocated"
    shutil.copytree(original, relocated)
    shutil.rmtree(original)
    assert not original.exists()
    assert reopen_portable_literature_production_input(relocated, receipt) == expected


def test_cli_builds_then_reopens_in_fresh_process_after_relocation(
    tmp_path: Path,
    manifest: dict[str, Any],
) -> None:
    original = tmp_path / "process-original"
    _write_manifest(original, manifest)
    receipt_path = original / "receipts" / "literature-input.json"
    receipt_path.parent.mkdir(parents=True)
    built = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "build",
            "--root",
            str(original),
            "--manifest-path",
            MANIFEST_PATH,
            "--output",
            str(receipt_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert built.returncode == 0, built.stderr
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    relocated = tmp_path / "process-relocated"
    shutil.copytree(original, relocated)
    shutil.rmtree(original)
    relocated_receipt = relocated / "receipts" / "literature-input.json"
    projection_path = relocated / "receipts" / "consumer-projection.json"
    reopened = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "reopen",
            "--root",
            str(relocated),
            "--receipt",
            str(relocated_receipt),
            "--output",
            str(projection_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert reopened.returncode == 0, reopened.stderr
    assert json.loads(projection_path.read_text(encoding="utf-8")) == receipt[
        "consumer_projection"
    ]

    overwrite = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "reopen",
            "--root",
            str(relocated),
            "--receipt",
            str(relocated_receipt),
            "--output",
            str(projection_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert overwrite.returncode == 1
    assert "File exists" in overwrite.stderr


def test_receipt_schema_rejects_untyped_extension(
    tmp_path: Path,
    manifest: dict[str, Any],
) -> None:
    receipt = _receipt(tmp_path, manifest)
    receipt["world_commission_token"] = "forged"
    with pytest.raises(ContractError):
        validate_portable_literature_production_input_receipt(tmp_path, receipt)
