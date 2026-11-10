# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Causal production tests for literature-conditioned conceptual invention."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

from agentic.discovery.conceptual_ancestry_v3 import (
    build_conceptual_ancestry_literature_projection,
)
from agentic.discovery.contracts import canonical_digest, stable_identifier
from agentic.discovery.literature_conditioned_invention import (
    LiteratureConditionedInventionError,
    build_literature_counterfactual_inputs,
    run_literature_invention_counterfactual_study,
    run_registered_literature_conditioned_invention,
    validate_literature_conditioned_invention_execution,
)
from tests.domains.test_literature_snapshot_capture_bridge import _generic_fixture
from tests.discovery.test_open_world_creativity import _taxonomy


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT
    / "agentic/spec/literature_conditioned_invention_execution_v1.schema.json"
)
PRESENT_USE = "2030-01-02T00:00:00Z"


def _projection(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[dict[str, Any], dict[str, Any]]:
    bundle, snapshot, bridge = _generic_fixture(monkeypatch)
    projection = build_conceptual_ancestry_literature_projection(
        literature_bundle=bundle,
        semantic_snapshot=snapshot,
        literature_snapshot_capture_bridge=bridge,
        present_use_at=PRESENT_USE,
    )
    return projection, bundle


def _run(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    *,
    governed_present_use_at: str = PRESENT_USE,
) -> dict[str, Any]:
    projection, bundle = _projection(monkeypatch)
    return run_registered_literature_conditioned_invention(
        target_id=bundle["target_id"],
        run_id=bundle["run_id"],
        state_version=bundle["state_version"],
        target_pressure=(
            "Explain how finite relational control can change the continuum "
            "obligation without assuming the desired result."
        ),
        root_contradictions=[
            "Finite control and continuum reconstruction pull in different directions.",
            "Representation independence and carrier-specific estimates are both required.",
        ],
        protected_successes=[
            "Retain exact finite-volume positivity and explicit corrections.",
            "Preserve distinct physical carriers under any proposed unification.",
        ],
        literature_projection=projection,
        literature_bundle=bundle,
        governed_present_use_at=governed_present_use_at,
        known_taxonomy=_taxonomy(),
        run_root=tmp_path / "literature-conditioned-invention",
        requested_count=8,
    )


def _reseal(value: dict[str, Any], field: str = "content_digest") -> dict[str, Any]:
    value[field] = canonical_digest(
        {key: item for key, item in value.items() if key != field}
    )
    return value


def _historical_input(current: dict[str, Any]) -> dict[str, Any]:
    historical = copy.deepcopy(current)
    first = historical["causal_inputs"][0]
    first["source_version"] = "historical-v0"
    first["assimilation_delta"] = {
        "event_type": "historical_replay",
        "source_id": first["source_id"],
        "claim_digest": first["claim_digest"],
        "authority": "counterfactual_study_only",
    }
    first.pop("causal_input_digest", None)
    first["causal_input_digest"] = canonical_digest(first)
    historical["input_id"] = stable_identifier(
        "historical-literature-input", current["input_id"]
    )
    historical.pop("content_digest", None)
    return {
        **historical,
        "content_digest": canonical_digest(historical),
    }


def test_schema_is_valid_and_domain_neutral() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    text = (
        SCHEMA_PATH.read_text(encoding="utf-8")
        + (
            ROOT
            / "agentic/discovery/literature_conditioned_invention.py"
        ).read_text(encoding="utf-8")
        + (
            ROOT
            / "agentic/scripts/run_literature_conditioned_invention_worker_v1.py"
        ).read_text(encoding="utf-8")
    )
    assert "yang-mills" not in text.lower()
    assert "mass gap" not in text.lower()


def test_registered_worker_authors_before_family_derivation_and_reopens(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    packet = _run(monkeypatch, tmp_path)
    replay = validate_literature_conditioned_invention_execution(
        packet, known_taxonomy=_taxonomy()
    )
    assert replay == packet
    assert packet["request"]["caller_supplied_inventions"] is False
    assert packet["request"]["caller_supplied_family_labels"] is False
    literature_authority = packet["request"]["literature_authority"]
    assert literature_authority["authority_kind"] == (
        "transitively_reopened_bounded_literature_v1"
    )
    assert literature_authority["governed_present_use_at"] == PRESENT_USE
    assert literature_authority["literature_projection"]["content_digest"] == (
        literature_authority["literature_projection_digest"]
    )
    assert literature_authority["literature_bundle"]["content_digest"] == (
        literature_authority["literature_bundle_digest"]
    )
    assert literature_authority["clock_attestation_authority"] is None
    assert packet["registered_receipt"]["role"] == "high_risk"
    assert packet["registered_receipt"]["operation"] == "high_risk_generation"
    assert packet["registered_receipt"]["outcome_status"] == "accepted"
    assert len(packet["worker_output"]["raw_inventions"]) == 8
    assert packet["worker_output"][
        "identity_erased_conceptual_signature"
    ].startswith("sha256:")
    assessment = packet["task_grounded_family_assessment"]
    assert assessment["semantic_signature_count"] >= 6
    assert assessment["worker_family_labels_consumed"] is False
    assert assessment["status"] == "six_or_more_semantically_distinct_families"
    assert packet[
        "direct_theory_preference_proof_schedule_experiment_effect"
    ] is False
    assert all(value is None for value in packet["authority_nulls"].values())


def test_registered_worker_rejects_literature_after_bounded_deadline(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    with pytest.raises(LiteratureConditionedInventionError) as raised:
        _run(
            monkeypatch,
            tmp_path,
            governed_present_use_at="2040-01-01T00:00:00Z",
        )
    assert raised.value.reason_code == "literature_authority_reopen_failed"


def test_replay_rejects_post_receipt_family_relabelling(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    packet = _run(monkeypatch, tmp_path)
    forged = copy.deepcopy(packet)
    evidence = forged["worker_output"]["family_evidence"][0]
    evidence["intervention_program"]["operation"] = "close_feedback"
    _reseal(evidence, "evidence_digest")
    forged["worker_output"]["semantic_output_signature"] = canonical_digest(
        [
            {
                "intervention_program": row["intervention_program"],
                "prediction": row["prediction"],
                "correction": row["correction"],
                "falsifier": row["falsifier"],
                "physics_return": row["physics_return"],
            }
            for row in sorted(
                forged["worker_output"]["family_evidence"],
                key=lambda item: item["invention_id"],
            )
        ]
    )
    _reseal(forged)
    with pytest.raises(LiteratureConditionedInventionError) as raised:
        validate_literature_conditioned_invention_execution(
            forged, known_taxonomy=_taxonomy()
        )
    assert raised.value.reason_code == "execution_replay_mismatch"


def test_counterfactual_plan_covers_every_required_literature_intervention(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    projection, _bundle = _projection(monkeypatch)
    current = projection["literature_derived_invention_input"]
    worlds = build_literature_counterfactual_inputs(
        current, historical_input=_historical_input(current)
    )
    world_ids = {world["world_id"] for world in worlds}
    assert {
        "current",
        "historical",
        "no_literature",
        "substituted",
        "corrected",
        "superseded",
        "retracted",
    } <= world_ids
    assert len(
        [world for world in worlds if world["world_id"].startswith("removal.")]
    ) == len(current["causal_inputs"])
    by_id = {world["world_id"]: world for world in worlds}
    first = current["causal_inputs"][0]
    corrected = by_id["corrected"]["input"]["causal_inputs"][0]
    assert corrected["claim_digest"] == canonical_digest(
        corrected["exact_claim"]
    )
    assert corrected["semantic_warrant_set_digest"] == canonical_digest(
        corrected["semantic_warrants"]
    )
    assert corrected["assimilation_delta"]["event_type"] == "reframe"
    assert corrected["causal_input_id"] != first["causal_input_id"]
    assert first["causal_input_id"] not in {
        row["causal_input_id"]
        for row in by_id["retracted"]["input"]["causal_inputs"]
    }
    assert first["causal_input_id"] not in {
        row["causal_input_id"]
        for row in by_id["superseded"]["input"]["causal_inputs"]
    }


def test_counterfactual_study_observes_semantic_deltas_or_explicit_nulls(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    packet = _run(monkeypatch, tmp_path / "base")
    request = packet["request"]
    current = request["literature_derived_invention_input"]
    study = run_literature_invention_counterfactual_study(
        base_request=request,
        historical_literature_input=_historical_input(current),
        run_root=tmp_path / "counterfactuals",
        max_workers=4,
    )
    assert study["all_interventions_accounted"] is True
    assert study["comparative_benefit_authorized"] is False
    results = {
        row["world_id"]: row for row in study["world_results"]
    }
    assert results["current"]["observed_effect"] == "reference"
    assert study["semantic_comparison"] == {
        "comparator": "identity_and_provenance_erased_conceptual_projection",
        "request_identity_counts_as_effect": False,
        "receipt_identity_counts_as_effect": False,
        "source_or_claim_digest_counts_as_effect": False,
        "correction_status_alone_counts_as_effect": False,
        "explicit_nulls_permitted": True,
    }
    assert results["no_literature"]["observed_effect"] == "explicit_null"
    for world_id in (
        "historical",
        "substituted",
        "corrected",
        "superseded",
        "retracted",
    ):
        assert results[world_id]["observed_effect"] == "explicit_null"
        assert results[world_id]["comparative_null"]["status"] == (
            "explicit_identity_erased_conceptual_null"
        )
    assert any(
        row["provenance_only_change"]
        for row in study["world_results"]
        if row["world_id"] != "current"
    )
    assert {
        row["identity_erased_conceptual_signature"]
        for row in study["world_results"]
    } == {
        results["current"]["identity_erased_conceptual_signature"]
    }
    assert all(value is None for value in study["authority_nulls"].values())
