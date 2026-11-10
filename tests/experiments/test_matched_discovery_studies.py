# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Acceptance tests for publication-disabled matched discovery studies.

The suite performs one real 19-cell execution with two recoverable faults and
then resumes the same content-derived study.  That single execution history is
used to test the complete grid, failed-stage blinding, sibling preservation,
immutable receipt reuse, matched-complete derivation, report reopening, and
adversarial swaps.  The assertions intentionally preserve the runtime's
epistemic boundary: a green report is internally correlated descriptive
calibration, never evidence of creative, conceptual, or physical advantage.
"""

from __future__ import annotations

import copy
import json
import threading
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping
from unittest import mock

import pytest

from agentic.discovery.contracts import canonical_digest, file_digest, stable_identifier
from agentic.discovery import matched_studies as matched_runtime
from agentic.discovery.matched_studies import (
    ARMS,
    LITERATURE_WORLD_IDS,
    STRATEGY_IDS,
    STAGE_SCHEDULE,
    MatchedStudyIntegrityError,
    build_matched_study_plan,
    load_matched_discovery_study_report,
    load_matched_study_fixture,
    run_matched_discovery_study,
    scientific_cell_projection,
    study_fault_key,
    validate_matched_discovery_study,
    write_matched_discovery_study_report,
)
from agentic.discovery import research_worker_isolation
from agentic.scripts import run_matched_discovery_study as study_cli
from agentic.scripts import run_matched_discovery_worker as study_worker
from skills.common.abstraction_formal_reasoning import (
    FormalReasoningError,
    validate_category_model,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "tests"
    / "fixtures"
    / "matched_discovery_studies"
    / "independent_task_clusters.json"
)
STAGE_TO_ROLE_OPERATION = {
    stage_id: (role, operation) for stage_id, role, operation in STAGE_SCHEDULE
}
# A real 19-cell, eight-stage subprocess study and its recovery are integration
# work, not a two-minute unit fixture. Individual worker budgets remain sealed.
pytestmark = [pytest.mark.expensive, pytest.mark.timeout(600)]
LITERATURE_FAMILY = "synthetic_literature_descriptor_calibration"
STRATEGY_FAMILY = "synthetic_strategy_descriptor_calibration"
FORMAL_FAMILY = "formal_lens_structural_calibration"


def _rehash(report: Mapping[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(dict(report))
    mutated["content_digest"] = canonical_digest(
        {key: value for key, value in mutated.items() if key != "content_digest"}
    )
    return mutated


def _cell(
    report: Mapping[str, Any], *, family_id: str, condition_id: str
) -> dict[str, Any]:
    matches = [
        cell
        for family in report["families"]
        if family["family_id"] == family_id
        for cell in family["cells"]
        if cell["condition_id"] == condition_id and cell["repetition"] == 1
    ]
    assert len(matches) == 1
    return matches[0]


def _receipt_summary(cell: Mapping[str, Any], stage_id: str) -> dict[str, Any]:
    role, operation = STAGE_TO_ROLE_OPERATION[stage_id]
    matches = [
        row
        for row in cell["receipts"]
        if row["role"] == role and row["operation"] == operation
    ]
    # candidate/high-risk maturation share an operation, so role disambiguates
    # the two parallel branches.
    assert len(matches) == 1
    return matches[0]


def _receipt(
    report: Mapping[str, Any], cell: Mapping[str, Any], stage_id: str
) -> dict[str, Any]:
    summary = _receipt_summary(cell, stage_id)
    return json.loads(
        (Path(report["run_directory"]) / summary["receipt_ref"]).read_text(
            encoding="utf-8"
        )
    )


def _direct_blind_packet(
    fixture: Mapping[str, Any],
    catalog: Mapping[tuple[str, str], Mapping[str, Any]],
    *,
    arm: str,
    strategy_index: int = 0,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Build one task-local packet without executing a subprocess receipt."""

    task = fixture["tasks"][0]
    strategy = fixture["strategies"][strategy_index]
    world = fixture["literature_worlds"][0]
    # Formal-family candidate framing is intentionally frozen at incumbent;
    # only the later formalization changes between these direct probes.
    candidates = study_worker._candidate_generation(
        {
            "tasks": [task],
            "arm": "incumbent",
            "strategy": strategy,
            "literature_world": world,
        }
    )["records"]
    high_risk = study_worker._high_risk_generation(
        {
            "tasks": [task],
            "candidates": candidates,
            "strategy": strategy,
            "corner_descriptors": matched_runtime._corner_descriptor_catalog(),
        }
    )["records"]
    candidate_maturation = study_worker._parallel_maturation(
        {"branch_kind": "candidate", "proposals": candidates}
    )["records"]
    high_risk_maturation = study_worker._parallel_maturation(
        {"branch_kind": "high_risk", "proposals": high_risk}
    )["records"]
    selected_lenses = (
        ("categorical", "hott")
        if arm == "combined"
        else (arm,)
        if arm in {"categorical", "hott"}
        else ()
    )
    artifacts = [
        copy.deepcopy(catalog[(task["task_id"], lens)])
        for lens in selected_lenses
    ]
    formal = study_worker._formal_lens(
        {"tasks": [task], "lens": arm, "typed_artifacts": artifacts}
    )["records"][0]
    reflection = study_worker._reflection(
        {
            "candidate_maturation": candidate_maturation,
            "high_risk_maturation": high_risk_maturation,
            "formal_rows": [formal],
            "route_status": world["route_status"],
        }
    )["records"][0]
    packet = {
        "opaque_candidate_id": "opaque.direct-candidate",
        "task_token": "task.direct-token",
        "task_rubric": {
            "pressure": task["pressure"],
            "protected_invariants": list(task["protected_invariants"]),
            "incumbent_primitives": list(task["incumbent_primitives"]),
            "physical_carrier": task["physical_carrier"],
            "formal_pressure": task["formal_pressure"],
            "falsifier": task["falsifier"],
        },
        "reflection": {
            "rounds": copy.deepcopy(reflection["rounds"]),
            "synthesis": reflection["synthesis"],
            "unification_edges": copy.deepcopy(reflection["unification_edges"]),
            "correction_conditions": copy.deepcopy(
                reflection["correction_conditions"]
            ),
            "convergence_status": reflection["convergence_status"],
            "conceptual_content": copy.deepcopy(reflection["conceptual_content"]),
        },
        "formal": {
            "content_projection": copy.deepcopy(formal["content_projection"])
        },
    }
    return packet, formal, reflection


@pytest.fixture(scope="module")
def formal_probe_evidence() -> dict[str, Any]:
    fixture = load_matched_study_fixture(FIXTURE)
    catalog = matched_runtime._build_typed_formal_catalog(fixture)
    return {
        "fixture": fixture,
        "catalog": catalog,
        "packets": {
            arm: _direct_blind_packet(fixture, catalog, arm=arm)
            for arm in ARMS
        },
    }


@pytest.fixture(scope="module")
def study_evidence(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    """Execute a partial study and an exact same-study repair once per module."""

    root = tmp_path_factory.mktemp("matched-discovery-study")
    fixture_path = root / "independent_task_clusters.json"
    fixture_bytes = FIXTURE.read_bytes()
    fixture_path.write_bytes(fixture_bytes)
    fixture = load_matched_study_fixture(fixture_path)
    plan = build_matched_study_plan(fixture, repetitions=1)
    literature_family = plan[0]
    blind_condition = literature_family["conditions"][0]
    maturation_condition = literature_family["conditions"][1]

    blind_fault = study_fault_key(
        {
            "family_id": literature_family["family_id"],
            "condition_id": blind_condition["condition_id"],
            "repetition": 1,
        },
        "blind_judgment",
    )
    maturation_fault = study_fault_key(
        {
            "family_id": literature_family["family_id"],
            "condition_id": maturation_condition["condition_id"],
            "repetition": 1,
        },
        "high_risk_maturation",
    )
    run_root = root / "runs"
    barriers: dict[str, threading.Barrier] = {}
    barrier_hits: defaultdict[str, int] = defaultdict(int)
    barrier_lock = threading.Lock()
    original_invoke = research_worker_isolation.ResearchWorkerAdapter.invoke

    def synchronized_invoke(
        adapter: research_worker_isolation.ResearchWorkerAdapter,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if kwargs.get("operation") == "parallel_maturation":
            context = kwargs["invocation_context"]
            cell_key = str(context["cell_key"])
            with barrier_lock:
                barrier = barriers.setdefault(cell_key, threading.Barrier(2))
                barrier_hits[cell_key] += 1
            # This barrier makes the acceptance test fail if the two maturation
            # invocations cease to be independently scheduled.  It does not
            # alter request bytes or scientific worker outputs.
            barrier.wait(timeout=10.0)
        return original_invoke(adapter, *args, **kwargs)

    with mock.patch.object(
        research_worker_isolation.ResearchWorkerAdapter,
        "invoke",
        new=synchronized_invoke,
    ):
        partial = run_matched_discovery_study(
            fixture_path=fixture_path,
            run_root=run_root,
            run_id="matched-runtime-regression-01",
            repetitions=1,
            max_workers=6,
            fault_plan={blind_fault: "exit_nonzero", maturation_fault: "exit_nonzero"},
        )
    partial_path = write_matched_discovery_study_report(partial)

    maturation_partial = _cell(
        partial,
        family_id=literature_family["family_id"],
        condition_id=maturation_condition["condition_id"],
    )
    sibling_summary = copy.deepcopy(
        _receipt_summary(maturation_partial, "candidate_maturation")
    )
    sibling_path = Path(partial["run_directory"]) / sibling_summary["receipt_ref"]
    sibling_bytes = sibling_path.read_bytes()
    partial_receipt_bytes = {
        row["receipt_ref"]: (Path(partial["run_directory"]) / row["receipt_ref"]).read_bytes()
        for family in partial["families"]
        for cell in family["cells"]
        for row in cell["receipts"]
    }

    # Removing the deterministic faults changes only those invocation requests.
    # Every already-successful request reopens its exact immutable receipt.
    with mock.patch.object(
        research_worker_isolation.ResearchWorkerAdapter,
        "invoke",
        new=synchronized_invoke,
    ):
        repaired = run_matched_discovery_study(
            fixture_path=fixture_path,
            run_root=run_root,
            run_id="matched-runtime-regression-01",
            repetitions=1,
            max_workers=6,
        )
    repaired_path = write_matched_discovery_study_report(repaired)
    return {
        "fixture": fixture,
        "fixture_path": fixture_path,
        "fixture_bytes": fixture_bytes,
        "plan": plan,
        "blind_condition_id": blind_condition["condition_id"],
        "maturation_condition_id": maturation_condition["condition_id"],
        "partial": partial,
        "partial_path": partial_path,
        "partial_receipt_bytes": partial_receipt_bytes,
        "repaired": repaired,
        "repaired_path": repaired_path,
        "sibling_summary": sibling_summary,
        "sibling_path": sibling_path,
        "sibling_bytes": sibling_bytes,
        "barrier_hits": dict(barrier_hits),
    }


def test_plan_has_exact_families_conditions_tasks_and_repetitions(tmp_path: Path) -> None:
    fixture = load_matched_study_fixture(FIXTURE)
    plan = build_matched_study_plan(fixture, repetitions=2)

    assert [family["family_id"] for family in plan] == [
        LITERATURE_FAMILY,
        STRATEGY_FAMILY,
        FORMAL_FAMILY,
    ]
    assert [len(family["conditions"]) for family in plan] == [8, 4, 7]
    assert sum(len(family["conditions"]) for family in plan) == 19
    assert [family["repetitions"] for family in plan] == [2, 2, 2]
    assert [row["literature_world_id"] for row in plan[0]["conditions"]] == list(
        LITERATURE_WORLD_IDS
    )
    assert [row["strategy_id"] for row in plan[1]["conditions"]] == list(
        STRATEGY_IDS
    )
    assert [row["arm"] for row in plan[2]["conditions"]] == list(ARMS)
    assert len({row["condition_id"] for family in plan for row in family["conditions"]}) == 19
    assert len(fixture["tasks"]) == len({row["cluster_id"] for row in fixture["tasks"]}) == 6

    run_root = tmp_path / "invalid-fault-run"
    with pytest.raises(MatchedStudyIntegrityError, match="unscheduled cell or stage"):
        run_matched_discovery_study(
            fixture_path=FIXTURE,
            run_root=run_root,
            run_id="matched-invalid-fault-plan",
            repetitions=1,
            fault_plan={"not/a/scheduled/fault": "exit_nonzero"},
        )
    assert not run_root.exists()


def test_v2_fixture_binds_exact_descriptor_bytes_without_production_authority() -> None:
    fixture = load_matched_study_fixture(FIXTURE)
    artifact = fixture["descriptor_artifacts"][0]
    artifact_path = ROOT / artifact["repository_path"]

    assert fixture["schema_version"] == 2
    assert fixture["study_authority"] == {
        "mode": "synthetic_structural_descriptor_calibration",
        "production_source_authority_executed": False,
        "production_discovery_operators_executed": False,
        "external_provider_plurality_status": "unavailable",
        "causal_effect_authorized": False,
    }
    assert file_digest(artifact_path) == artifact["file_sha256"]
    assert artifact_path.stat().st_size == artifact["byte_length"]
    assert json.loads(artifact_path.read_text(encoding="utf-8"))["content_digest"] == (
        artifact["declared_content_digest"]
    )
    assert artifact["use"] == "immutable_descriptor_context_only_not_executed"
    assert artifact["production_chain_executed"] is False


def test_worker_rejects_resealed_artifact_with_stale_delta_self_digest(
    formal_probe_evidence: Mapping[str, Any],
) -> None:
    task = formal_probe_evidence["fixture"]["tasks"][0]
    artifact = copy.deepcopy(formal_probe_evidence["catalog"][(task["task_id"], "categorical")])
    assert study_worker._typed_artifact_summary(task, "categorical", artifact)
    artifact["task_derived_formal_delta"]["changed_theoretical_burden"] += " Tampered."
    artifact["artifact_digest"] = canonical_digest({key: value for key, value in artifact.items() if key != "artifact_digest"})
    with pytest.raises(ValueError, match="task-semantic handback"):
        study_worker._typed_artifact_summary(task, "categorical", artifact)


def test_shared_typed_category_witness_replays_and_rejects_semantic_corruption(
    formal_probe_evidence: Mapping[str, Any],
) -> None:
    fixture = formal_probe_evidence["fixture"]
    task = fixture["tasks"][0]
    artifact = formal_probe_evidence["catalog"][(task["task_id"], "categorical")]
    result = validate_category_model(
        artifact["model"],
        artifact["negative_witness"],
        {artifact["obligation_id"]},
    )
    assert result["result"] == "noncommuting"
    assert result["counterexamples"]

    corrupted = copy.deepcopy(artifact["model"])
    corrupted["objects"][0]["element_ids"].append("foreign-unmapped-element")
    with pytest.raises(FormalReasoningError, match="total single-valued map"):
        validate_category_model(
            corrupted,
            artifact["negative_witness"],
            {artifact["obligation_id"]},
        )


def test_formal_and_control_arms_are_count_matched_without_invocation_bonus(
    formal_probe_evidence: Mapping[str, Any],
) -> None:
    signatures = {}
    scores = {}
    for arm, (packet, formal, _reflection) in formal_probe_evidence["packets"].items():
        projection = formal["content_projection"]
        signatures[arm] = (
            len(projection["object_role_slots"]),
            len(projection["law_slots"]),
            len(projection["witness_slots"]),
            len(projection["correction_obligations"]),
        )
        scores[arm] = study_worker._blind_judgment(
            {"blinded_packets": [packet]}
        )["records"][0]["dimension_scores"]

    assert set(signatures.values()) == {(3, 6, 2, 2)}
    assert scores["categorical"] == scores["hott"] == scores["combined"]
    assert scores["categorical"] == scores["incumbent"] == scores["no_abstraction"]
    assert scores["decorative"]["burden_localization"] < scores["incumbent"][
        "burden_localization"
    ]


def test_blind_judge_is_label_status_and_paraphrase_invariant_but_semantic_sensitive(
    formal_probe_evidence: Mapping[str, Any],
) -> None:
    packet, formal, reflection = copy.deepcopy(
        formal_probe_evidence["packets"]["categorical"]
    )
    baseline = study_worker._blind_judgment({"blinded_packets": [packet]})[
        "records"
    ][0]["dimension_scores"]
    assert set(packet["formal"]) == {"content_projection"}
    assert all(key not in packet for key in ("condition_id", "strategy_id", "arm", "lens"))

    fixture = formal_probe_evidence["fixture"]
    source_packets = matched_runtime._sanitized_blind_packets(
        fixture=fixture,
        cell={"cell_key": "direct-status-invariance-cell"},
        reflections=[reflection],
        formal_rows=[formal],
    )[0]
    relabelled_formal = copy.deepcopy(formal)
    relabelled_formal["lens"] = "forbidden-mutated-lens"
    relabelled_formal["status"] = "forbidden-mutated-status"
    relabelled_packets = matched_runtime._sanitized_blind_packets(
        fixture=fixture,
        cell={"cell_key": "direct-status-invariance-cell"},
        reflections=[reflection],
        formal_rows=[relabelled_formal],
    )[0]
    assert relabelled_packets == source_packets

    paraphrased = copy.deepcopy(packet)
    paraphrased["reflection"]["rounds"][0]["tension"] = (
        "Equivalent prose: retain the same structured mechanism and anchors."
    )
    paraphrased["reflection"]["conceptual_content"]["candidate"]["statement"] = (
        "A surface paraphrase of the candidate statement."
    )
    paraphrased["reflection"]["conceptual_content"]["high_risk_portfolio"][0]["statement"] = (
        "A surface paraphrase of the aggressive statement."
    )
    assert study_worker._blind_judgment({"blinded_packets": [paraphrased]})[
        "records"
    ][0]["dimension_scores"] == baseline

    corrupted = copy.deepcopy(packet)
    corrupted["reflection"]["conceptual_content"]["semantic_anchors"] = []
    corrupted_portfolio = corrupted["reflection"]["conceptual_content"][
        "high_risk_portfolio"
    ]
    corrupted_portfolio[0]["falsifier"] = "foreign falsifier"
    corrupted_portfolio[0]["risk_axes"] = []
    for row in corrupted_portfolio[:4]:
        row["mechanism"] = "same-label semantic collapse"
        row["ontology_delta"]["new_primitive"] = "same-collapsed-primitive"
    corrupted["formal"]["content_projection"]["semantic_anchor"] = "foreign anchor"
    corrupted["formal"]["content_projection"]["correction_obligations"] = [
        "foreign correction one",
        "foreign correction two",
    ]
    corrupted_scores = study_worker._blind_judgment(
        {"blinded_packets": [corrupted]}
    )["records"][0]["dimension_scores"]
    assert sum(corrupted_scores.values()) < sum(baseline.values())
    assert corrupted_scores["risk_reward"] < baseline["risk_reward"]

    labelled = copy.deepcopy(packet)
    labelled["strategy_id"] = "forbidden-direct-label"
    with pytest.raises(ValueError, match="leaks an intervention label"):
        study_worker._blind_judgment({"blinded_packets": [labelled]})


def test_strategy_content_survives_maturation_reflection_and_blind_projection(
    study_evidence: Mapping[str, Any],
) -> None:
    report = study_evidence["repaired"]
    family = next(
        row for row in report["families"] if row["family_id"] == STRATEGY_FAMILY
    )
    first_task_candidate_statements = set()
    first_task_candidate_mechanisms = set()
    first_task_portfolio_signatures = set()
    blind_packet_digests = set()

    for cell in family["cells"]:
        candidate_records = _receipt(report, cell, "candidate_generation")[
            "response_payload"
        ]["output"]["records"]
        high_risk_records = _receipt(report, cell, "high_risk_generation")[
            "response_payload"
        ]["output"]["records"]
        candidate_maturation = _receipt(report, cell, "candidate_maturation")[
            "response_payload"
        ]["output"]["records"]
        high_risk_maturation = _receipt(report, cell, "high_risk_maturation")[
            "response_payload"
        ]["output"]["records"]
        reflection_records = _receipt(report, cell, "reflection")["response_payload"][
            "output"
        ]["records"]
        blind_packets = _receipt(report, cell, "blind_judgment")["request_payload"][
            "payload"
        ]["blinded_packets"]

        task_count = len(study_evidence["fixture"]["tasks"])
        assert len(candidate_records) == len(candidate_maturation) == task_count
        assert len(high_risk_records) == len(high_risk_maturation) == task_count * 10
        assert len(reflection_records) == len(blind_packets) == task_count
        high_output = _receipt(report, cell, "high_risk_generation")["response_payload"][
            "output"
        ]
        assert high_output["portfolio_execution"]["variants_per_task"] == 10
        maturation_output = _receipt(report, cell, "high_risk_maturation")[
            "response_payload"
        ]["output"]
        assert maturation_output["branch_execution"] == {
            "mode": "parallel_isolated_portfolio_branches",
            "max_workers": 10,
            "scheduled_branch_count": task_count * 10,
            "completed_branch_count": task_count * 10,
            "barrier_status": "complete",
            "shared_mutable_state": False,
        }
        for candidate, matured_candidate, reflection, packet in zip(
            candidate_records,
            candidate_maturation,
            reflection_records,
            blind_packets,
            strict=True,
        ):
            task_high = [
                row for row in high_risk_records if row["task_id"] == candidate["task_id"]
            ]
            task_matured = [
                row for row in high_risk_maturation if row["task_id"] == candidate["task_id"]
            ]
            assert len(task_high) == len(task_matured) == 10
            assert len({row["corner_family"] for row in task_high}) == 10
            assert len({row["mechanism"] for row in task_high}) >= 8
            assert sum(row["is_wildcard"] for row in task_high) >= 2
            assert sum(row["is_control"] for row in task_high) == 1
            assert matured_candidate["proposal_content"]["statement"] == candidate[
                "statement"
            ]
            assert matured_candidate["proposal_content"]["mechanism"] == candidate[
                "mechanism"
            ]
            matured_by_parent = {row["parent_id"]: row for row in task_matured}
            for high_risk in task_high:
                preserved = matured_by_parent[high_risk["variant_id"]]["proposal_content"]
                for field in (
                    "statement",
                    "mechanism",
                    "risk_axes",
                    "reward_axes",
                    "premortem",
                    "falsifier",
                    "ontology_delta",
                    "decisive_question",
                ):
                    assert preserved[field] == high_risk[field]
            assert reflection["conceptual_content"]["candidate"] == matured_candidate[
                "proposal_content"
            ]
            assert reflection["conceptual_content"]["high_risk_portfolio"] == sorted(
                [row["proposal_content"] for row in task_matured],
                key=lambda row: row["corner_family"],
            )
            assert packet["reflection"]["conceptual_content"] == reflection[
                "conceptual_content"
            ]
            packet_json = json.dumps(packet, sort_keys=True)
            for preserved_value in (
                candidate["statement"],
                candidate["mechanism"],
                task_high[0]["statement"],
                task_high[0]["premortem"],
                task_high[0]["falsifier"],
            ):
                assert preserved_value in packet_json

        condition = next(
            row
            for row in family["conditions"]
            if row["condition_id"] == cell["condition_id"]
        )
        assert condition["strategy_id"] not in json.dumps(blind_packets, sort_keys=True)
        first_task_candidate_statements.add(candidate_records[0]["statement"])
        first_task_candidate_mechanisms.add(candidate_records[0]["mechanism"])
        first_task_portfolio_signatures.add(
            study_worker._blind_judgment({"blinded_packets": [blind_packets[0]]})[
                "records"
            ][0]["semantic_diagnostics"]["portfolio_signature"]
        )
        blind_packet_digests.add(canonical_digest(blind_packets))

    assert len(first_task_candidate_statements) == len(family["cells"]) == 4
    assert len(first_task_candidate_mechanisms) == len(family["cells"]) == 4
    assert len(first_task_portfolio_signatures) == len(family["cells"]) == 4
    assert len(blind_packet_digests) == len(family["cells"]) == 4


def test_formal_family_freezes_generation_and_consumes_exact_typed_artifacts(
    study_evidence: Mapping[str, Any],
    formal_probe_evidence: Mapping[str, Any],
) -> None:
    report = study_evidence["repaired"]
    family = next(
        row for row in report["families"] if row["family_id"] == FORMAL_FAMILY
    )
    expected_artifact_counts = {
        "categorical": 6,
        "hott": 6,
        "combined": 12,
        "incumbent": 0,
        "no_abstraction": 0,
        "decorative": 0,
        "restatement": 0,
    }
    candidate_outputs = []

    for cell in family["cells"]:
        candidate_receipt = _receipt(report, cell, "candidate_generation")
        assert candidate_receipt["request_payload"]["payload"]["arm"] == "incumbent"
        candidate_outputs.append(candidate_receipt["response_payload"]["output"])

        formal_receipt = _receipt(report, cell, "formal_lens")
        request_payload = formal_receipt["request_payload"]["payload"]
        arm = request_payload["lens"]
        expected_artifacts = matched_runtime._formal_artifacts_for_arm(
            study_evidence["fixture"],
            arm,
            formal_probe_evidence["catalog"],
        )
        assert request_payload["typed_artifacts"] == expected_artifacts
        assert len(request_payload["typed_artifacts"]) == expected_artifact_counts[arm]

        output = formal_receipt["response_payload"]["output"]
        assert output["formal_execution"]["scope"] == (
            "shared_typed_finite_engine_parent_replay_plus_isolated_projection"
        )
        assert output["formal_execution"]["theorem_authorized"] is False
        assert output["formal_execution"]["continuum_authorized"] is False
        assert output["formal_execution"]["physics_value_authorized"] is False
        for row in output["records"]:
            expected_summaries = 2 if arm == "combined" else 1
            assert len(row["typed_artifact_summaries"]) == expected_summaries
            assert row["content_projection"]["physics_handback"] == row[
                "physics_handback"
            ]
            handback = row["physics_handback"]
            if handback is not None:
                assert handback["physics_value_evidence_status"] == "unavailable"
                assert handback["continuum_authority_status"] == "unavailable"

    assert all(output == candidate_outputs[0] for output in candidate_outputs[1:])


def test_reopen_rejects_live_typed_formal_catalog_drift(
    study_evidence: Mapping[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    original_builder = matched_runtime._build_typed_formal_catalog

    def drifted_catalog(
        fixture: Mapping[str, Any],
    ) -> dict[tuple[str, str], dict[str, Any]]:
        catalog = copy.deepcopy(original_builder(fixture))
        key = next(key for key in sorted(catalog) if key[1] == "categorical")
        catalog[key]["artifact_digest"] = "0" * 64
        return catalog

    monkeypatch.setattr(
        matched_runtime,
        "_build_typed_formal_catalog",
        drifted_catalog,
    )
    with pytest.raises(
        MatchedStudyIntegrityError,
        match="formal_lens did not consume exact prior outputs",
    ):
        load_matched_discovery_study_report(study_evidence["repaired_path"])


def test_failed_blind_stage_keeps_exact_blinding_without_invented_scores(
    study_evidence: Mapping[str, Any],
) -> None:
    partial = study_evidence["partial"]
    blind_cell = _cell(
        partial,
        family_id=LITERATURE_FAMILY,
        condition_id=study_evidence["blind_condition_id"],
    )

    assert blind_cell["attempted_stage_count"] == 7
    assert blind_cell["failure_stages"] == ["blind_judgment"]
    assert blind_cell["blinding"]["status"] == "internal_process_blind_only"
    assert blind_cell["blinding"]["condition_labels_withheld"] is True
    assert blind_cell["blinding"]["cognitive_independence_authorized"] is False
    assert blind_cell["internal_judge_scores"] == []
    assert validate_matched_discovery_study(partial) == partial


def test_parallel_failure_preserves_the_successful_sibling_and_barrier_state(
    study_evidence: Mapping[str, Any],
) -> None:
    partial_cell = _cell(
        study_evidence["partial"],
        family_id=LITERATURE_FAMILY,
        condition_id=study_evidence["maturation_condition_id"],
    )

    assert partial_cell["attempted_stage_count"] == 4
    assert partial_cell["failure_stages"] == ["high_risk_maturation"]
    assert partial_cell["parallel_maturation"] == {
        "scheduled_branch_count": 2,
        "completed_branch_count": 1,
        "barrier_status": "partial",
    }
    assert _receipt_summary(partial_cell, "candidate_maturation")["outcome_status"] == "accepted"
    assert _receipt_summary(partial_cell, "high_risk_maturation")["outcome_status"] != "accepted"


def test_every_cell_schedules_both_maturation_branches_concurrently(
    study_evidence: Mapping[str, Any],
) -> None:
    # Nineteen cell identities each crossed the two-party barrier once in the
    # partial attempt and once in the repaired attempt.
    assert len(study_evidence["barrier_hits"]) == 19
    assert set(study_evidence["barrier_hits"].values()) == {4}


def test_same_study_retry_reuses_successes_retains_failures_and_repairs_only_gaps(
    study_evidence: Mapping[str, Any],
) -> None:
    repaired_cell = _cell(
        study_evidence["repaired"],
        family_id=LITERATURE_FAMILY,
        condition_id=study_evidence["maturation_condition_id"],
    )
    repaired_sibling = _receipt_summary(repaired_cell, "candidate_maturation")

    assert repaired_sibling == study_evidence["sibling_summary"]
    assert study_evidence["sibling_path"].read_bytes() == study_evidence["sibling_bytes"]
    for receipt_ref, original_bytes in study_evidence["partial_receipt_bytes"].items():
        receipt_path = Path(study_evidence["partial"]["run_directory"]) / receipt_ref
        assert receipt_path.read_bytes() == original_bytes
    receipt_files = list(
        (Path(study_evidence["repaired"]["run_directory"]) / "receipts").rglob("*.json")
    )
    assert len(receipt_files) == 154  # 152 repaired-chain receipts + two retained failures
    assert load_matched_discovery_study_report(study_evidence["partial_path"]) == study_evidence[
        "partial"
    ]


def test_repaired_one_repetition_run_has_19_cells_and_152_receipts(
    study_evidence: Mapping[str, Any],
) -> None:
    report = study_evidence["repaired"]
    cells = [cell for family in report["families"] for cell in family["cells"]]

    assert report["schema_version"] == 3
    assert report["isolation_requirement"] == matched_runtime._study_isolation_requirement(
        False
    )
    assert report["status"] == "protocol_complete_internal_calibration_only"
    assert len(cells) == 19
    assert all(cell["complete"] and cell["attempted_stage_count"] == 8 for cell in cells)
    assert sum(len(cell["receipts"]) for cell in cells) == 152
    assert {
        family["family_id"]: family["matched_complete_repetitions"]
        for family in report["families"]
    } == {
        LITERATURE_FAMILY: [1],
        STRATEGY_FAMILY: [1],
        FORMAL_FAMILY: [1],
    }
    assert all(value is False for key, value in report["authority_outcomes"].items() if key.endswith("_authorized"))
    assert report["authority_outcomes"]["authority_distinct_evaluation_status"] == "unavailable"
    assert report["authority_outcomes"]["external_provider_status"] == "unavailable"
    assert report["authority_outcomes"]["provider_plurality_authorized"] is False
    assert report["authority_outcomes"]["production_chain_executed"] is False


def test_study_isolation_floor_changes_identity_and_rejects_nonrequired_receipts(
    study_evidence: Mapping[str, Any],
) -> None:
    report = study_evidence["repaired"]
    fixture = study_evidence["fixture"]
    nonrequired = matched_runtime._study_isolation_requirement(False)
    kernel_required = matched_runtime._study_isolation_requirement(True)
    repetitions = report["families"][0]["repetitions"]
    expected_nonrequired_id = stable_identifier(
        "matched-study",
        report["run_id"],
        canonical_digest(fixture),
        repetitions,
        nonrequired,
    )
    expected_kernel_id = stable_identifier(
        "matched-study",
        report["run_id"],
        canonical_digest(fixture),
        repetitions,
        kernel_required,
    )

    assert report["study_id"] == expected_nonrequired_id
    assert expected_kernel_id != expected_nonrequired_id
    forged = copy.deepcopy(report)
    forged["isolation_requirement"] = kernel_required
    with pytest.raises(MatchedStudyIntegrityError, match="identity is not content-derived"):
        validate_matched_discovery_study(_rehash(forged))

    planned_family = study_evidence["plan"][0]
    planned_condition = planned_family["conditions"][0]
    cell = report["families"][0]["cells"][0]
    with pytest.raises(
        research_worker_isolation.ResearchWorkerIntegrityError,
        match="required isolation identity",
    ):
        matched_runtime._validate_cell_chain(
            fixture=fixture,
            family=planned_family,
            condition=planned_condition,
            cell=cell,
            run_directory=Path(report["run_directory"]),
            study_id=report["study_id"],
            required_kernel_isolation=True,
            formal_catalog=matched_runtime._build_typed_formal_catalog(fixture),
        )


def test_one_failed_cell_excludes_only_its_family_repetition(
    study_evidence: Mapping[str, Any],
) -> None:
    partial = study_evidence["partial"]
    families = {family["family_id"]: family for family in partial["families"]}

    assert partial["status"] == "partial_failure_internal_calibration_only"
    assert families[LITERATURE_FAMILY]["matched_complete_repetitions"] == []
    assert families[STRATEGY_FAMILY]["matched_complete_repetitions"] == [1]
    assert families[FORMAL_FAMILY]["matched_complete_repetitions"] == [1]
    assert all(
        result["score_observations"] == 0
        and all(value is None for value in result["mean_scores"].values())
        for result in families[LITERATURE_FAMILY]["descriptive_results"]
    )


def test_report_reopen_is_exact_and_checks_live_command_authority(
    study_evidence: Mapping[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    assert load_matched_discovery_study_report(study_evidence["repaired_path"]) == study_evidence[
        "repaired"
    ]

    def reject_live_authority(_authority: Mapping[str, Any]) -> None:
        raise research_worker_isolation.ResearchWorkerIntegrityError(
            "simulated current-checkout dependency drift"
        )

    monkeypatch.setattr(
        research_worker_isolation, "_require_live_command_authority", reject_live_authority
    )
    with pytest.raises(
        research_worker_isolation.ResearchWorkerIntegrityError,
        match="current-checkout dependency drift",
    ):
        load_matched_discovery_study_report(study_evidence["repaired_path"])


def test_reopen_rejects_fixture_byte_drift_even_when_json_semantics_are_unchanged(
    study_evidence: Mapping[str, Any],
) -> None:
    fixture_path = study_evidence["fixture_path"]
    original = study_evidence["fixture_bytes"]
    try:
        fixture_path.write_bytes(original + b"\n")
        with pytest.raises(MatchedStudyIntegrityError, match="fixture bytes or semantics changed"):
            load_matched_discovery_study_report(study_evidence["repaired_path"])
    finally:
        fixture_path.write_bytes(original)
    assert load_matched_discovery_study_report(study_evidence["repaired_path"])[
        "content_digest"
    ] == study_evidence["repaired"]["content_digest"]


def test_reopen_rejects_noncanonical_report_bytes_and_recovers_after_restore(
    study_evidence: Mapping[str, Any],
) -> None:
    report_path = study_evidence["repaired_path"]
    original = report_path.read_bytes()
    try:
        report_path.write_bytes(original + b" ")
        with pytest.raises(MatchedStudyIntegrityError, match="report file bytes changed"):
            load_matched_discovery_study_report(report_path)
    finally:
        report_path.write_bytes(original)
    assert load_matched_discovery_study_report(report_path) == study_evidence["repaired"]


def test_reopen_rejects_receipt_byte_tamper_and_recovers_after_restore(
    study_evidence: Mapping[str, Any],
) -> None:
    first = study_evidence["repaired"]["families"][0]["cells"][0]["receipts"][0]
    receipt_path = Path(study_evidence["repaired"]["run_directory"]) / first["receipt_ref"]
    original = receipt_path.read_bytes()
    try:
        receipt_path.write_bytes(original + b" ")
        with pytest.raises(MatchedStudyIntegrityError, match="receipt summary file bytes changed"):
            load_matched_discovery_study_report(study_evidence["repaired_path"])
    finally:
        receipt_path.write_bytes(original)
    assert load_matched_discovery_study_report(study_evidence["repaired_path"])[
        "study_id"
    ] == study_evidence["repaired"]["study_id"]


def test_rehashed_cross_cell_receipt_swap_is_rejected(
    study_evidence: Mapping[str, Any],
) -> None:
    tampered = copy.deepcopy(study_evidence["repaired"])
    cells = tampered["families"][0]["cells"]
    cells[0]["receipts"][0] = copy.deepcopy(cells[1]["receipts"][0])
    with pytest.raises(MatchedStudyIntegrityError, match="invocation context differs from its stage"):
        validate_matched_discovery_study(_rehash(tampered))


def test_rehashed_condition_and_projection_swaps_are_rejected(
    study_evidence: Mapping[str, Any],
) -> None:
    condition_swap = copy.deepcopy(study_evidence["repaired"])
    condition_swap["families"][0]["conditions"][0:2] = reversed(
        condition_swap["families"][0]["conditions"][0:2]
    )
    with pytest.raises(MatchedStudyIntegrityError, match="family plan changed"):
        validate_matched_discovery_study(_rehash(condition_swap))

    projection_swap = copy.deepcopy(study_evidence["repaired"])
    rows = projection_swap["deterministic_projection"]["cell_projection_digests"]
    rows[0], rows[1] = rows[1], rows[0]
    projection_swap["deterministic_projection"]["projection_digest"] = canonical_digest(rows)
    with pytest.raises(MatchedStudyIntegrityError, match="scientific projection mismatch"):
        validate_matched_discovery_study(_rehash(projection_swap))


def test_scientific_projection_excludes_operational_metadata_but_not_outputs(
    study_evidence: Mapping[str, Any],
) -> None:
    cell = study_evidence["repaired"]["families"][0]["cells"][0]
    run_directory = Path(study_evidence["repaired"]["run_directory"])
    receipts = [
        json.loads((run_directory / row["receipt_ref"]).read_text(encoding="utf-8"))
        for row in cell["receipts"]
    ]
    baseline = scientific_cell_projection(cell, receipts)
    operationally_changed = copy.deepcopy(receipts)
    for receipt in operationally_changed:
        receipt["command_authority"] = {"changed": True}
        receipt["environment_authority"] = {"changed": True}
        receipt["workspace"] = {"changed": True}
        receipt["resource_receipt"] = {"changed": True}
        receipt["process_event"]["started_at"] = "2099-01-01T00:00:00+00:00"
        if receipt["response_payload"] is not None:
            receipt["response_payload"]["environment_observation"] = {"changed": True}
    assert scientific_cell_projection(cell, operationally_changed) == baseline

    scientifically_changed = copy.deepcopy(receipts)
    scientifically_changed[0]["response_payload"]["output"]["records"][0][
        "statement"
    ] += " Altered scientific content."
    assert scientific_cell_projection(cell, scientifically_changed) != baseline


def test_rehashed_blinding_swap_is_rejected(
    study_evidence: Mapping[str, Any],
) -> None:
    tampered = copy.deepcopy(study_evidence["repaired"])
    cells = tampered["families"][0]["cells"]
    assert cells[0]["blinding"] != cells[1]["blinding"]
    cells[0]["blinding"], cells[1]["blinding"] = cells[1]["blinding"], cells[0]["blinding"]
    with pytest.raises(MatchedStudyIntegrityError, match="blind mapping or scores are not exact"):
        validate_matched_discovery_study(_rehash(tampered))


def test_judge_invocation_withholds_direct_condition_strategy_and_arm_labels(
    study_evidence: Mapping[str, Any],
) -> None:
    cell = study_evidence["repaired"]["families"][0]["cells"][0]
    summary = _receipt_summary(cell, "blind_judgment")
    receipt_path = Path(study_evidence["repaired"]["run_directory"]) / summary[
        "receipt_ref"
    ]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    assert set(receipt["request_payload"]["invocation_context"]) == {
        "stage_id",
        "repetition",
        "fixture_semantic_digest",
        "stage_schedule_digest",
        "opaque_cell_token",
    }
    assert set(receipt["request_payload"]["payload"]) == {"blinded_packets"}
    assert cell["condition_id"] not in json.dumps(receipt["request_payload"], sort_keys=True)


def test_cli_reopen_exit_codes_distinguish_valid_partial_and_invalid(
    study_evidence: Mapping[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert study_cli.main(["--validate-existing", str(study_evidence["repaired_path"])]) == 0
    full_summary = json.loads(capsys.readouterr().out)
    assert full_summary["status"] == "protocol_complete_internal_calibration_only"
    assert full_summary["attempted_stage_receipt_count"] == 152
    assert full_summary["publication_authorized"] is False
    assert full_summary["advantage_inference_authorized"] is False

    assert study_cli.main(["--validate-existing", str(study_evidence["partial_path"])]) == 0
    partial_summary = json.loads(capsys.readouterr().out)
    assert partial_summary["status"] == "partial_failure_internal_calibration_only"

    assert (
        study_cli.main(
            [
                "--validate-existing",
                str(study_evidence["partial_path"]),
                "--require-complete",
            ]
        )
        == 3
    )
    required = json.loads(capsys.readouterr().out)
    assert required["status"] == "partial_failure_internal_calibration_only"

    malformed = tmp_path / "malformed.json"
    malformed.write_text("{not-json", encoding="utf-8")
    assert study_cli.main(["--validate-existing", str(malformed)]) == 2
    invalid = json.loads(capsys.readouterr().err)
    assert invalid["status"] == "matched_study_failed"

    assert study_cli.main([]) == 2
    missing = json.loads(capsys.readouterr().err)
    assert missing["status"] == "matched_study_failed"
    assert "--run-root and --run-id" in missing["message"]

    assert (
        study_cli.main(
            [
                "--run-root",
                str(tmp_path / "malformed-fault-run"),
                "--run-id",
                "malformed-fault-run",
                "--fault",
                "missing-separator",
            ]
        )
        == 2
    )
    malformed_fault = json.loads(capsys.readouterr().err)
    assert malformed_fault["error_type"] == "ArgumentTypeError"
