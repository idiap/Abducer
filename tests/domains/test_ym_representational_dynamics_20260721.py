# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Regression tests for the scoped 2026-07-21 Yang--Mills integration."""

from __future__ import annotations

import copy
import io
import json
import shutil
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

import pytest

from agentic.discovery.contracts import ContractError, Namespace
from agentic.discovery.literature import (
    LANE_TYPES,
    assimilate_derived_literature,
    bind_source_semantic_warrants,
    derive_claim_mappings,
    replay_literature_counterfactuals,
    validate_assimilation as validate_canonical_assimilation,
    validate_claim_mapping_derivation,
    validate_snapshot as validate_canonical_snapshot,
)


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "agentic/scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import integrate_ym_representational_dynamics_20260721 as integration  # noqa: E402
import evaluate_ym_conceptual_quality_20260721 as conceptual_quality  # noqa: E402
import replay_ym_representational_dynamics_20260721 as replay  # noqa: E402
import run_ym_canonical_parent_cycle_20260721 as canonical_runner  # noqa: E402
import validate_ym_canonical_parent_cycle_20260721 as canonical_validation  # noqa: E402


def _current_ym_material_inputs() -> tuple[dict, dict, dict, dict]:
    workspace = integration.REGISTERED_RUNTIME_ROOT / "workspace"
    paths = (
        "artifacts/00-frozen-live-literature-snapshot.json",
        "operator-outputs/01-frontier-literature-assimilator.json",
        "operator-outputs/02-high-risk-hypothesis-forger.json",
        "operator-outputs/03-parallel-hypothesis-portfolio.json",
    )
    return tuple(
        json.loads((workspace / path).read_text(encoding="utf-8")) for path in paths
    )  # type: ignore[return-value]


def _exact_counterexample_receipt() -> dict:
    return {
        "status": "counterexample",
        "epistemic_outcome": "falsifies_claim",
        "certificate": {"left": "1/2", "right": "5/8", "difference": "-1/8"},
        "result": {
            "claim_holds": False,
            "exact_values": {"left": "1/2", "right": "5/8", "difference": "-1/8"},
        },
    }


def _fresh_material_transition() -> tuple[dict, dict, dict]:
    snapshot, assimilation, portfolio, parallel = _current_ym_material_inputs()
    systems, rounds, _ = canonical_runner._ym_conceptual_material(
        snapshot=snapshot,
        assimilation=assimilation,
        portfolio=portfolio,
        parallel=parallel,
    )
    parent_evidence = conceptual_quality.build_evidence(
        systems=systems,
        rounds=rounds[:3],
        snapshot=snapshot,
        proposal_receipt_ids=["opreceipt-regression-parent", "opreceipt-regression-parallel"],
        stage_id="parent",
    )
    synthesis_systems, synthesis_rounds = canonical_runner._assimilate_probe_round(
        systems,
        rounds,
        _exact_counterexample_receipt(),
        selected_system_id=parent_evidence["preferred_system_id"],
    )
    synthesis_evidence = conceptual_quality.build_evidence(
        systems=synthesis_systems,
        rounds=synthesis_rounds,
        snapshot=snapshot,
        proposal_receipt_ids=[
            "opreceipt-regression-parent",
            "opreceipt-regression-parallel",
            "opreceipt-regression-experiment",
        ],
        stage_id="synthesis",
        previous_evidence=parent_evidence,
    )
    parent = {
        "conceptual_systems": systems,
        "reflection_rounds": rounds[:3],
        "independent_evaluation_evidence": [parent_evidence],
    }
    synthesis = {
        "conceptual_systems": synthesis_systems,
        "reflection_rounds": synthesis_rounds,
        "independent_evaluation_evidence": [synthesis_evidence],
    }
    return parent, synthesis, snapshot


def _zip_with_member(name: str, *, symlink: bool = False) -> zipfile.ZipFile:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        info = zipfile.ZipInfo(name)
        if symlink:
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
        archive.writestr(info, b"payload")
    buffer.seek(0)
    return zipfile.ZipFile(buffer)


@pytest.mark.parametrize("name", ["../escape", "/absolute", "folder\\ambiguous"])
def test_safe_archive_member_rejects_filesystem_escape(name: str) -> None:
    with _zip_with_member(name) as archive:
        with pytest.raises(integration.IntegrationError):
            integration.safe_file_members(archive)


def test_safe_archive_member_rejects_symlink() -> None:
    with _zip_with_member("link", symlink=True) as archive:
        with pytest.raises(integration.IntegrationError, match="Symbolic|symbolic"):
            integration.safe_file_members(archive)


def test_active_index_excludes_byproducts_and_quarantines_publication() -> None:
    assert integration.exclusion_reason(PurePosixPath("stage/__pycache__/x.pyc")) == "cache_or_build_directory"
    assert integration.exclusion_reason(PurePosixPath("nested/source.zip")) == "nested_archive"
    publication = PurePosixPath(
        "11_vscode_codex_skill_bundle/.agents/skills/ym-build-latex-paper/SKILL.md"
    )
    active = PurePosixPath(
        "11_vscode_codex_skill_bundle/.agents/skills/ym-prove-conditional-partition-ratio/SKILL.md"
    )
    assert integration.classify_active_path(publication) == "external_only_publication_skill"
    assert integration.classify_active_path(active) == "activated_skill_source"


def test_stage70_qualification_accepts_only_the_declared_noncanonical_hash() -> None:
    flags = {flag: True for flag in json.loads(replay.EXPECTED_QUALIFICATION.read_text())["required_exact_flags"]}
    stored = {"certificates": {"central_four": {**flags, "kkt_witness_sha256": "stored"}}}
    fresh = {"certificates": {"central_four": {**flags, "kkt_witness_sha256": "fresh"}}}
    expected = json.loads(replay.EXPECTED_QUALIFICATION.read_text())
    result = replay.qualification_from_payloads(stored, fresh, expected)
    assert result["accepted"] is True
    fresh["certificates"]["central_four"]["spill_nullity_over_Q"] = 99
    assert replay.qualification_from_payloads(stored, fresh, expected)["accepted"] is False


def test_literature_hook_is_current_and_fails_closed_for_later_cycle() -> None:
    fixture = json.loads(integration.DEFAULT_LITERATURE.read_text(encoding="utf-8"))
    integration.validate_literature_snapshot(fixture)
    assert fixture["snapshot_kind"] == "provider_backed_web_capture"
    assert fixture["provider_backed"] is True
    assert fixture["live_recency_claim"] is True
    assert fixture["exhaustive_coverage_claim"] is False
    assert fixture["peer_validation_claim"] is False
    source_ids = {row["source_id"] for row in fixture["sources"]}
    assert {
        integration.DIRECT_CHALLENGER_ID,
        *integration.LANE_GENEALOGY_SOURCE_IDS,
    }.issubset(source_ids)
    challenger = next(
        row
        for row in fixture["sources"]
        if row["source_id"] == integration.DIRECT_CHALLENGER_ID
    )
    assert challenger["source_status"] == "unverified_challenger"
    assert challenger["claim_status"] == "unverified_challenger"
    assert len(challenger["claim_audit"]) == 6
    assert all(
        row["verification_status"] == "unverified" and row["required_obligation"]
        for row in challenger["claim_audit"]
    )
    with pytest.raises(integration.IntegrationError, match="cover at least"):
        integration.validate_literature_snapshot(fixture, require_after="2026-07-22")
    withdrawn = next(row for row in fixture["sources"] if row["source_status"] == "withdrawn")
    withdrawn["disposition"] = "included"
    with pytest.raises(integration.IntegrationError, match="withdrawn"):
        integration.validate_literature_snapshot(fixture)


def test_direct_challenger_cannot_be_promoted_by_manual_status_edit() -> None:
    fixture = json.loads(integration.DEFAULT_LITERATURE.read_text(encoding="utf-8"))
    challenger = next(
        row
        for row in fixture["sources"]
        if row["source_id"] == integration.DIRECT_CHALLENGER_ID
    )
    challenger["claim_status"] = "accepted"
    with pytest.raises(integration.IntegrationError, match="unverified challenger"):
        integration.validate_literature_snapshot(fixture)


@pytest.mark.skip(
    reason="User-deferred: historical literature adapter uses an unregistered snapshot validator; "
    "current provenance is missing. See .prism/idiap-software-disclosure/09-publication-migration.md."
)
def test_canonical_literature_adapter_is_valid_and_fail_closed() -> None:
    snapshot = json.loads(
        integration.CANONICAL_LITERATURE_SNAPSHOT.read_text(encoding="utf-8")
    )
    assimilation = json.loads(
        integration.CANONICAL_LITERATURE_ASSIMILATION.read_text(encoding="utf-8")
    )
    validate_canonical_snapshot(snapshot)
    validate_canonical_assimilation(assimilation, snapshot=snapshot)

    assert snapshot["provenance_mode"] == "local_only"
    assert {row["lane_type"] for row in snapshot["lane_receipts"]} == set(
        LANE_TYPES
    )
    assert all(
        row["execution_mode"] == "local_only"
        for row in snapshot["lane_receipts"]
    )
    assert assimilation["hypothesis_rebase_status"] == "provisional_local_only"
    assert assimilation["resolution"]["active_investment_gate"] == "blocked_local_only"

    challenger = next(
        source
        for source in snapshot["sources"]
        if source["source_id"] == integration.DIRECT_CHALLENGER_ID
    )
    assert len(challenger["claims"]) == 7
    mappings = [
        row
        for row in assimilation["theory_mappings"]
        if row["source_id"] == integration.DIRECT_CHALLENGER_ID
    ]
    assert len(mappings) == 6
    assert all(
        row["confidence"] == "low"
        and row["relation"] == "leaves_open"
        and row["event_type"] == "reprioritize"
        for row in mappings
    )

    mutated = json.loads(json.dumps(assimilation))
    mutated["resolution"]["active_investment_gate"] = "pass"
    with pytest.raises(Exception, match="local-only|local_only|digest"):
        validate_canonical_assimilation(mutated, snapshot=snapshot)


@pytest.mark.expensive
def test_target_claim_mapping_and_all_five_replay_operations_are_derived(
    tmp_path: Path,
) -> None:
    preflight_snapshot, _legacy_assimilation, _legacy_portfolio, _parallel = (
        _current_ym_material_inputs()
    )
    namespace = Namespace(
        integration.TARGET_ID, "ym-generated-routing-test", "root", 0
    )
    counterbalance_seed = "ym-generated-routing-test"
    preflight_workspace = tmp_path / "preflight"
    preflight = canonical_runner.prepare_proposal_field_free_high_risk_envelope(
        charter=canonical_runner._charter(preflight_snapshot),
        literature_snapshot=preflight_snapshot,
        workspace=preflight_workspace,
        namespace=namespace,
        authored_incumbent_comparison_proposals=(
            canonical_runner._authored_domain_template_incumbent_comparison_proposals(
                preflight_snapshot
            )
        ),
        hidden_prompt_texts=canonical_runner.YM_PROPOSAL_FIELD_FREE_PROMPTS,
        repetitions=5,
        requested_count=10,
        counterbalance_seed=counterbalance_seed,
    )
    snapshot = bind_source_semantic_warrants(
        preflight_snapshot,
        canonical_runner._ym_semantic_source_warrants(
            preflight_snapshot,
            generated_portfolio=preflight["selected_portfolio"],
        ),
        authority_id="ym21-generated-candidate-source-claim-audit.v2",
    )
    final_workspace = tmp_path / "final"
    final = canonical_runner.prepare_proposal_field_free_high_risk_envelope(
        charter=canonical_runner._charter(snapshot),
        literature_snapshot=snapshot,
        workspace=final_workspace,
        namespace=namespace,
        authored_incumbent_comparison_proposals=(
            canonical_runner._authored_domain_template_incumbent_comparison_proposals(
                snapshot
            )
        ),
        hidden_prompt_texts=canonical_runner.YM_PROPOSAL_FIELD_FREE_PROMPTS,
        repetitions=5,
        requested_count=10,
        counterbalance_seed=counterbalance_seed,
    )
    generated_binding = canonical_runner._assert_stable_generated_selection(
        preflight,
        final,
        preflight_workspace=preflight_workspace,
        final_workspace=final_workspace,
        expected_namespace=namespace,
    )
    assert generated_binding["schema_version"] == "3.0"
    assert generated_binding["semantic_identity_stable"] is True
    assert generated_binding["global_semantic_content_identity_stable"] is True
    assert generated_binding["evidence_identity_rebound"] is True
    assert (
        generated_binding["preflight_selected_evidence_repetition_id"]
        != generated_binding["final_selected_evidence_repetition_id"]
    )
    assert generated_binding["evidence_only_portfolio_paths"] == list(
        canonical_runner._SNAPSHOT_EVIDENCE_ONLY_PORTFOLIO_PATHS
    )
    assert generated_binding["authoritative_portfolio_projection_digest"] == (
        canonical_runner.canonical_digest(
            generated_binding["authoritative_portfolio_projection"]
        )
    )
    assert generated_binding["candidate_projection"] == generated_binding[
        "authoritative_portfolio_projection"
    ]["hypotheses"]
    assert len(
        {
            row["schedule_slot_id"]
            for row in generated_binding["semantic_repetition_schedule"][
                "repetitions"
            ]
        }
    ) == 5
    assert len(
        {
            row["semantic_content_id"]
            for row in generated_binding["semantic_repetition_schedule"]["repetitions"]
        }
    ) == 5
    assert generated_binding["selected_semantic_content_id"] in {
        row["semantic_content_id"]
        for row in generated_binding["semantic_repetition_schedule"]["repetitions"]
    }
    assert len(
        {
            row["semantic_output_id"]
            for row in generated_binding["semantic_repetition_schedule"]["repetitions"]
        }
    ) == 5
    assert generated_binding["selection_semantic_projection_digest"] == (
        canonical_runner.canonical_digest(
            generated_binding["selection_semantic_projection"]
        )
    )
    assert canonical_runner._legacy_routing_identifiers(generated_binding) == set()
    assert generated_binding["validated_namespace"] == namespace.as_dict()

    for namespace_field, forged_value in (
        ("run_id", "run-forged-self-authorizing"),
        ("branch_id", "branch-forged-self-authorizing"),
        ("state_version", namespace.state_version + 1),
    ):
        forged_workspace = tmp_path / f"forged-namespace-{namespace_field}"
        shutil.copytree(final_workspace, forged_workspace)
        forged_envelope = copy.deepcopy(final)
        forged_namespace_mapping = namespace.as_dict()
        forged_namespace_mapping[namespace_field] = forged_value
        forged_namespace = Namespace.from_mapping(forged_namespace_mapping)

        forged_study_path = forged_workspace / forged_envelope[
            "proposal_field_free_upstream"
        ]["study_artifact"]["path"]
        forged_study_descriptor = canonical_runner.artifact_descriptor(
            forged_study_path,
            forged_workspace,
            forged_namespace,
        )
        forged_envelope["proposal_field_free_upstream"][
            "study_artifact"
        ] = forged_study_descriptor

        forged_selection_path = forged_workspace / forged_envelope[
            "proposal_field_free_upstream"
        ]["selection_artifact"]["path"]
        forged_selection = json.loads(
            forged_selection_path.read_text(encoding="utf-8")
        )
        forged_selection["study_artifact"] = forged_study_descriptor
        forged_selection["content_digest"] = canonical_runner.canonical_digest(
            {
                key: value
                for key, value in forged_selection.items()
                if key != "content_digest"
            }
        )
        forged_selection_path.write_text(
            json.dumps(forged_selection),
            encoding="utf-8",
        )
        forged_envelope["proposal_field_free_upstream"][
            "selection_artifact"
        ] = canonical_runner.artifact_descriptor(
            forged_selection_path,
            forged_workspace,
            forged_namespace,
        )

        with pytest.raises(
            canonical_runner.YMCanonicalCycleError,
            match="namespace mismatch",
        ):
            canonical_runner._assert_stable_generated_selection(
                preflight,
                forged_envelope,
                preflight_workspace=preflight_workspace,
                final_workspace=forged_workspace,
                expected_namespace=namespace,
            )

    splice_workspace = tmp_path / "cross-study-splice"
    splice_envelope = canonical_runner.prepare_proposal_field_free_high_risk_envelope(
        charter=canonical_runner._charter(snapshot),
        literature_snapshot=snapshot,
        workspace=splice_workspace,
        namespace=namespace,
        authored_incumbent_comparison_proposals=(
            canonical_runner._authored_domain_template_incumbent_comparison_proposals(
                snapshot
            )
        ),
        hidden_prompt_texts=canonical_runner.YM_PROPOSAL_FIELD_FREE_PROMPTS,
        repetitions=5,
        requested_count=10,
        counterbalance_seed="ym-cross-study-splice-5",
    )
    final_study = canonical_runner._study_artifact(
        final,
        final_workspace,
        namespace,
    )
    splice_study = canonical_runner._study_artifact(
        splice_envelope,
        splice_workspace,
        namespace,
    )

    def repetition_ids(study: dict, field: str) -> list[str]:
        return [str(row[field]) for row in study["repetitions"]]

    assert repetition_ids(final_study, "semantic_content_id") == repetition_ids(
        splice_study,
        "semantic_content_id",
    )
    for conditioned_identity in (
        "schedule_slot_id",
        "semantic_output_id",
        "evidence_repetition_id",
    ):
        assert repetition_ids(final_study, conditioned_identity) != repetition_ids(
            splice_study,
            conditioned_identity,
        )

    with pytest.raises(
        canonical_runner.YMCanonicalCycleError,
        match="precommitted semantic prompt/repetition schedule changed",
    ):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            splice_envelope,
            preflight_workspace=preflight_workspace,
            final_workspace=splice_workspace,
            expected_namespace=namespace,
        )

    selection_splice_workspace = tmp_path / "selection-only-splice"
    shutil.copytree(final_workspace, selection_splice_workspace)
    selection_splice_envelope = copy.deepcopy(final)
    foreign_selection = canonical_runner._selection_artifact(
        splice_envelope,
        splice_workspace,
        namespace,
    )
    foreign_selection["study_artifact"] = selection_splice_envelope[
        "proposal_field_free_upstream"
    ]["study_artifact"]
    foreign_selection["study_content_digest"] = final_study["content_digest"]
    foreign_selection["content_digest"] = canonical_runner.canonical_digest(
        {
            key: value
            for key, value in foreign_selection.items()
            if key != "content_digest"
        }
    )
    selection_splice_path = selection_splice_workspace / selection_splice_envelope[
        "proposal_field_free_upstream"
    ]["selection_artifact"]["path"]
    selection_splice_path.write_text(
        json.dumps(foreign_selection),
        encoding="utf-8",
    )
    selection_splice_envelope["proposal_field_free_upstream"][
        "selection_artifact"
    ] = canonical_runner.artifact_descriptor(
        selection_splice_path,
        selection_splice_workspace,
        namespace,
    )
    with pytest.raises(
        canonical_runner.YMCanonicalCycleError,
        match=(
            "schedule-slot identity differs|selection-policy semantics changed|"
            "does not bind its semantic/evidence repetition"
        ),
    ):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            selection_splice_envelope,
            preflight_workspace=preflight_workspace,
            final_workspace=selection_splice_workspace,
            expected_namespace=namespace,
        )

    def _rehashed_portfolio_forgery() -> dict:
        forged = copy.deepcopy(final)
        portfolio = forged["selected_portfolio"]
        portfolio["content_digest"] = canonical_runner.canonical_digest(
            {key: value for key, value in portfolio.items() if key != "content_digest"}
        )
        return forged

    semantic_drift = copy.deepcopy(final)
    semantic_drift["selected_portfolio"]["hypotheses"][0]["ontology_delta"][
        "affordance"
    ] += " Rehashed semantic drift."
    semantic_drift = _rehashed_portfolio_forgery() | {
        "selected_portfolio": semantic_drift["selected_portfolio"]
    }
    semantic_drift["selected_portfolio"]["content_digest"] = (
        canonical_runner.canonical_digest(
            {
                key: value
                for key, value in semantic_drift["selected_portfolio"].items()
                if key != "content_digest"
            }
        )
    )
    with pytest.raises(
        canonical_runner.YMCanonicalCycleError,
        match="authoritative generated portfolio changed",
    ):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            semantic_drift,
            preflight_workspace=preflight_workspace,
            final_workspace=final_workspace,
            expected_namespace=namespace,
        )

    genealogy_drift = copy.deepcopy(final)
    genealogy_drift["selected_portfolio"]["hypotheses"][0]["genealogy"].append(
        "rehashed-nonlegacy-genealogy-drift"
    )
    genealogy_drift["selected_portfolio"]["content_digest"] = (
        canonical_runner.canonical_digest(
            {
                key: value
                for key, value in genealogy_drift["selected_portfolio"].items()
                if key != "content_digest"
            }
        )
    )
    with pytest.raises(canonical_runner.YMCanonicalCycleError, match="genealogy changed"):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            genealogy_drift,
            preflight_workspace=preflight_workspace,
            final_workspace=final_workspace,
            expected_namespace=namespace,
        )

    branch_drift = copy.deepcopy(final)
    branch_drift["selected_portfolio"]["parallel_branch_seeds"][0][
        "maturation_question"
    ] += " Rehashed branch drift."
    branch_drift["selected_portfolio"]["content_digest"] = (
        canonical_runner.canonical_digest(
            {
                key: value
                for key, value in branch_drift["selected_portfolio"].items()
                if key != "content_digest"
            }
        )
    )
    with pytest.raises(
        canonical_runner.YMCanonicalCycleError, match="parallel branch seeds changed"
    ):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            branch_drift,
            preflight_workspace=preflight_workspace,
            final_workspace=final_workspace,
            expected_namespace=namespace,
        )

    mapping_drift = copy.deepcopy(final)
    mapping_drift["selected_portfolio"]["hypotheses"][0]["mechanism_key"] += (
        "-rehashed-drift"
    )
    mapping_drift["selected_portfolio"]["content_digest"] = (
        canonical_runner.canonical_digest(
            {
                key: value
                for key, value in mapping_drift["selected_portfolio"].items()
                if key != "content_digest"
            }
        )
    )
    with pytest.raises(
        canonical_runner.YMCanonicalCycleError, match="mapping keys changed"
    ):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            mapping_drift,
            preflight_workspace=preflight_workspace,
            final_workspace=final_workspace,
            expected_namespace=namespace,
        )

    legacy_drift = copy.deepcopy(final)
    legacy_drift["selected_portfolio"]["hypotheses"][0]["genealogy"].append(
        "YM21-R01"
    )
    legacy_drift["selected_portfolio"]["content_digest"] = (
        canonical_runner.canonical_digest(
            {
                key: value
                for key, value in legacy_drift["selected_portfolio"].items()
                if key != "content_digest"
            }
        )
    )
    with pytest.raises(
        canonical_runner.YMCanonicalCycleError, match="legacy YM routing identifiers"
    ):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            legacy_drift,
            preflight_workspace=preflight_workspace,
            final_workspace=final_workspace,
            expected_namespace=namespace,
        )

    collision_workspace = tmp_path / "evidence-collision"
    shutil.copytree(final_workspace, collision_workspace)
    collision_envelope = copy.deepcopy(final)
    study_path = collision_workspace / collision_envelope["proposal_field_free_upstream"][
        "study_artifact"
    ]["path"]
    collision_study = json.loads(study_path.read_text(encoding="utf-8"))
    collision_id = collision_study["repetitions"][0]["evidence_repetition_id"]
    collision_study["repetitions"][1]["evidence_repetition_id"] = collision_id
    collision_study["repetitions"][1]["repetition_id"] = collision_id
    collision_study["repetitions"][1]["content_digest"] = (
        canonical_runner.canonical_digest(
            {
                key: value
                for key, value in collision_study["repetitions"][1].items()
                if key != "content_digest"
            }
        )
    )
    collision_study["content_digest"] = canonical_runner.canonical_digest(
        {
            key: value
            for key, value in collision_study.items()
            if key != "content_digest"
        }
    )
    study_path.write_text(json.dumps(collision_study), encoding="utf-8")
    with pytest.raises(
        canonical_runner.YMCanonicalCycleError,
        match="study artifact descriptor verification failed: artifact digest mismatch",
    ):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            collision_envelope,
            preflight_workspace=preflight_workspace,
            final_workspace=collision_workspace,
            expected_namespace=namespace,
        )

    collision_namespace = Namespace.from_mapping(
        collision_envelope["proposal_field_free_upstream"]["study_artifact"][
            "namespace"
        ]
    )
    rebound_study_descriptor = canonical_runner.artifact_descriptor(
        study_path, collision_workspace, collision_namespace
    )
    collision_envelope["proposal_field_free_upstream"][
        "study_artifact"
    ] = rebound_study_descriptor
    selection_path = collision_workspace / collision_envelope[
        "proposal_field_free_upstream"
    ]["selection_artifact"]["path"]
    collision_selection = json.loads(selection_path.read_text(encoding="utf-8"))
    collision_selection["study_artifact"] = rebound_study_descriptor
    collision_selection["study_content_digest"] = collision_study["content_digest"]
    collision_selection["exploration_selection"] = collision_study[
        "exploration_selection"
    ]
    collision_selection["content_digest"] = canonical_runner.canonical_digest(
        {
            key: value
            for key, value in collision_selection.items()
            if key != "content_digest"
        }
    )
    selection_path.write_text(json.dumps(collision_selection), encoding="utf-8")
    collision_envelope["proposal_field_free_upstream"][
        "selection_artifact"
    ] = canonical_runner.artifact_descriptor(
        selection_path, collision_workspace, collision_namespace
    )
    with pytest.raises(
        canonical_runner.YMCanonicalCycleError,
        match="evidence repetition identities must be unique",
    ):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            collision_envelope,
            preflight_workspace=preflight_workspace,
            final_workspace=collision_workspace,
            expected_namespace=namespace,
        )

    stale_size = copy.deepcopy(final)
    stale_size["proposal_field_free_upstream"]["selection_artifact"][
        "size_bytes"
    ] += 1
    with pytest.raises(
        canonical_runner.YMCanonicalCycleError,
        match="selection artifact descriptor verification failed: artifact size mismatch",
    ):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            stale_size,
            preflight_workspace=preflight_workspace,
            final_workspace=final_workspace,
            expected_namespace=namespace,
        )

    legacy_alias_workspace = tmp_path / "legacy-alias-drift"
    shutil.copytree(final_workspace, legacy_alias_workspace)
    legacy_alias_envelope = copy.deepcopy(final)
    legacy_study_path = legacy_alias_workspace / legacy_alias_envelope[
        "proposal_field_free_upstream"
    ]["study_artifact"]["path"]
    legacy_study = json.loads(legacy_study_path.read_text(encoding="utf-8"))
    legacy_study["repetitions"][0]["repetition_id"] = "elicitation-exact-evidence.forged"
    legacy_study["repetitions"][0]["content_digest"] = canonical_runner.canonical_digest(
        {
            key: value
            for key, value in legacy_study["repetitions"][0].items()
            if key != "content_digest"
        }
    )
    legacy_study["content_digest"] = canonical_runner.canonical_digest(
        {key: value for key, value in legacy_study.items() if key != "content_digest"}
    )
    legacy_study_path.write_text(json.dumps(legacy_study), encoding="utf-8")
    legacy_namespace = Namespace.from_mapping(
        legacy_alias_envelope["proposal_field_free_upstream"]["study_artifact"]["namespace"]
    )
    legacy_study_descriptor = canonical_runner.artifact_descriptor(
        legacy_study_path, legacy_alias_workspace, legacy_namespace
    )
    legacy_alias_envelope["proposal_field_free_upstream"]["study_artifact"] = legacy_study_descriptor
    legacy_selection_path = legacy_alias_workspace / legacy_alias_envelope[
        "proposal_field_free_upstream"
    ]["selection_artifact"]["path"]
    legacy_selection = json.loads(legacy_selection_path.read_text(encoding="utf-8"))
    legacy_selection["study_artifact"] = legacy_study_descriptor
    legacy_selection["study_content_digest"] = legacy_study["content_digest"]
    legacy_selection["content_digest"] = canonical_runner.canonical_digest(
        {key: value for key, value in legacy_selection.items() if key != "content_digest"}
    )
    legacy_selection_path.write_text(json.dumps(legacy_selection), encoding="utf-8")
    legacy_alias_envelope["proposal_field_free_upstream"]["selection_artifact"] = (
        canonical_runner.artifact_descriptor(
            legacy_selection_path, legacy_alias_workspace, legacy_namespace
        )
    )
    with pytest.raises(
        canonical_runner.YMCanonicalCycleError,
        match="repetition_id must exactly alias evidence_repetition_id",
    ):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            legacy_alias_envelope,
            preflight_workspace=preflight_workspace,
            final_workspace=legacy_alias_workspace,
            expected_namespace=namespace,
        )

    schedule_drift_workspace = tmp_path / "schedule-drift"
    schedule_drift = canonical_runner.prepare_proposal_field_free_high_risk_envelope(
        charter=canonical_runner._charter(snapshot),
        literature_snapshot=snapshot,
        workspace=schedule_drift_workspace,
        namespace=namespace,
        authored_incumbent_comparison_proposals=(
            canonical_runner._authored_domain_template_incumbent_comparison_proposals(
                snapshot
            )
        ),
        hidden_prompt_texts=tuple(
            reversed(canonical_runner.YM_PROPOSAL_FIELD_FREE_PROMPTS)
        ),
        repetitions=5,
        requested_count=10,
        counterbalance_seed=counterbalance_seed,
    )
    with pytest.raises(
        canonical_runner.YMCanonicalCycleError,
        match="precommitted semantic prompt/repetition schedule changed",
    ):
        canonical_runner._assert_stable_generated_selection(
            preflight,
            schedule_drift,
            preflight_workspace=preflight_workspace,
            final_workspace=schedule_drift_workspace,
            expected_namespace=namespace,
        )

    runner_source = Path(canonical_runner.__file__).read_text(encoding="utf-8")
    assert "_aligned_final_prompt_texts" not in runner_source
    assert "_prompt_text_schedule" not in runner_source
    assert "itertools.permutations" not in runner_source
    portfolio = final["selected_portfolio"]
    catalog = canonical_runner._ym_theory_catalog(snapshot)
    derivation = derive_claim_mappings(snapshot, theory_catalog=catalog)
    hypotheses = canonical_runner._derived_hypothesis_rebase(derivation)
    assimilation = assimilate_derived_literature(
        snapshot,
        theory_catalog=catalog,
        mapping_derivation=derivation,
        hypotheses=hypotheses,
        candidate_snapshot_ids=[snapshot["snapshot_id"]],
        freshness_evaluated_at=snapshot["search_completed_at"],
    )
    direct_source = next(
        row
        for row in snapshot["sources"]
        if row["source_id"] == integration.DIRECT_CHALLENGER_ID
    )
    direct_mappings = [
        row
        for row in derivation["theory_mappings"]
        if row["source_id"] == integration.DIRECT_CHALLENGER_ID
    ]
    assert len(direct_mappings) == len(
        {" ".join(claim.split()).casefold() for claim in direct_source["claims"]}
    )
    assert len(derivation["mapping_receipts"]) == len(derivation["theory_mappings"])
    assert assimilation["mapping_provenance"]["mode"] == "deterministic_claim_derivation"
    assert assimilation["schema_version"] == "4.0"
    assert derivation["semantic_coverage_audit"]["explicit_warrant_claim_count"] > 0
    assert derivation["semantic_claim_layer"]["epistemic_nulls"] == {
        "source_truth_authorized": False,
        "semantic_entailment_authorized": False,
        "exhaustive_coverage_authorized": False,
        "novelty_authorized": False,
        "external_validation_status": "unavailable",
    }
    generated_ids = {
        row["hypothesis_id"] for row in portfolio["hypotheses"]
    }
    assert set(generated_binding["selected_hypothesis_ids"]) == generated_ids
    assert {
        row["theory_object_id"]
        for row in catalog["theory_objects"]
        if not row["scope_anchor"]
    } == generated_ids
    assert {row["hypothesis_id"] for row in hypotheses} == generated_ids
    assert {
        theory_object_id
        for row in derivation["theory_mappings"]
        for theory_object_id in row["theory_object_ids"]
        if theory_object_id != "YM21-TARGET-SCOPE"
    } == generated_ids
    canonical_runner._assert_generated_live_routing(
        portfolio=portfolio,
        theory_catalog=catalog,
        mapping_derivation=derivation,
        hypothesis_rebase=hypotheses,
        assimilation=assimilation,
    )

    worlds = canonical_runner._literature_counterfactual_worlds(snapshot)
    replay_packet = replay_literature_counterfactuals(
        snapshot,
        theory_catalog=catalog,
        worlds=worlds,
        hypotheses=hypotheses,
        candidate_snapshot_ids=[snapshot["snapshot_id"]],
        freshness_evaluated_at=snapshot["search_completed_at"],
    )
    assert {
        row["transformation"]["operation"]
        for row in replay_packet["world_results"]
    } == {
        "delete_source",
        "no_literature",
        "supersede_source",
        "contradict_source",
        "coverage_only_change",
    }
    assert replay_packet["null_effect_world_ids"] == ["coverage-only-null"]
    assert all(
        row["snapshot"]["provenance_mode"] == "local_only"
        and row["assimilation"]["resolution"]["active_investment_gate"]
        == "blocked_local_only"
        for row in replay_packet["world_results"]
    )
    selected, baseline = canonical_runner._literature_routed_seeds(
        portfolio, assimilation
    )
    trace = canonical_runner._full_literature_counterfactual_replays(
        snapshot=snapshot,
        assimilation=assimilation,
        portfolio=portfolio,
        baseline_trace=baseline,
        theory_catalog=catalog,
        hypotheses=hypotheses,
    )
    trace.pop("content_digest", None)
    trace["generated_candidate_binding"] = generated_binding
    trace["content_digest"] = canonical_runner.canonical_digest(trace)
    canonical_runner._assert_generated_live_routing(
        portfolio=portfolio,
        theory_catalog=catalog,
        mapping_derivation=derivation,
        hypothesis_rebase=hypotheses,
        assimilation=assimilation,
        routing_trace=trace,
    )
    assert canonical_runner._legacy_routing_identifiers(trace) == set()
    assert [row["hypothesis_id"] for row in selected] == trace["selected_hypothesis_ids"]
    null_row = next(
        row for row in trace["full_pipeline_replays"] if row["world_id"] == "coverage-only-null"
    )
    assert null_row["selection_changed"] is False
    assert null_row["programme_changed"] is False
    generic_null = next(
        row
        for row in replay_packet["world_results"]
        if row["world_id"] == "coverage-only-null"
    )
    assert generic_null["effects"]["semantic_coverage_audit_changed"] is True
    assert generic_null["effects"]["semantic_relation_decisions_changed"] is False

    tampered = json.loads(json.dumps(derivation))
    tampered["theory_mappings"][0]["event_type"] = "demote"
    tampered["content_digest"] = canonical_runner.canonical_digest(
        {key: value for key, value in tampered.items() if key != "content_digest"}
    )
    with pytest.raises(ContractError, match="does not replay|digest"):
        validate_claim_mapping_derivation(
            tampered, snapshot=snapshot, theory_catalog=catalog
        )


@pytest.mark.skip(
    reason="User-deferred: preserved six-operator parent lacks current source-routing and "
    "literature-production evidence. See .prism/idiap-software-disclosure/09-publication-migration.md."
)
def test_registered_six_operator_parent_cycle_is_active_current_and_reachable() -> None:
    summary = canonical_validation.validate(integration.REGISTERED_RUNTIME_ROOT)
    assert summary["status"] == "validated"
    assert summary["operator_receipts"] == 6
    assert summary["feedback_edges"] == 6
    assert summary["committed_state_version"] == 1
    assert summary["literature_mode"] == "active_current"

    binding = json.loads(integration.REGISTERED_RUNTIME_BINDING.read_text(encoding="utf-8"))
    rebase = json.loads(
        (integration.NORMALIZED_ROOT / "literature_rebase.json").read_text(encoding="utf-8")
    )
    registry = json.loads(integration.YM_REGISTRY.read_text(encoding="utf-8"))
    assert binding["status"] == "active_current"
    assert binding["snapshot"]["provenance_mode"] == "live"
    assert binding["snapshot"]["lane_count"] == 6
    assert binding["operator_receipts"]["count"] == 6
    assert rebase["active_canonical_literature_status"] == "active_current"
    assert rebase["registered_runtime_upgrade"] == binding
    assert registry["canonical_literature_interop"]["registered_runtime_upgrade"] == binding
    # The older projection remains honestly local; it is no longer confused
    # with the active registered runtime.
    assert registry["canonical_literature_interop"]["snapshot"]["provenance_mode"] == "local_only"
    assert registry["pre_cycle_hook"]["last_completed_runtime_status"] == "active_current"


@pytest.mark.skip(
    reason="User-deferred: historical reflection lacks current internal-correlated and external "
    "validation evidence. See .prism/idiap-software-disclosure/09-publication-migration.md."
)
def test_registered_reflection_is_spectral_descent_with_internal_correlated_G2_G4_evidence() -> None:
    runtime = integration.REGISTERED_RUNTIME_ROOT
    result = json.loads((runtime / "canonical_cycle_result.json").read_text(encoding="utf-8"))
    acceptance = json.loads((runtime / "acceptance_report.json").read_text(encoding="utf-8"))
    roles = json.loads((runtime / "artifact_roles.json").read_text(encoding="utf-8"))
    packets = [
        json.loads((runtime / "workspace" / path).read_text(encoding="utf-8"))
        for path in roles["reflective_packets"]
    ]
    assert [len(packet["reflection_rounds"]) for packet in packets] == [3, 4]
    assert all(packet["generation_mode"] == "operator_generated" for packet in packets)
    assert all(
        packet["stage_gates"]["G2_philosophical_depth"] == "pass"
        and packet["stage_gates"]["G4_understanding_gain"] == "pass"
        and packet["independent_evaluation_evidence"]
        for packet in packets
    )
    selected_id = packets[-1]["independent_evaluation_evidence"][0][
        "preferred_system_id"
    ]
    preferred = next(
        row
        for row in packets[-1]["conceptual_systems"]
        if row["system_id"] == selected_id
    )
    assert canonical_validation.REQUIRED_PRIMITIVES <= set(preferred["primitives"])
    assert canonical_validation.REQUIRED_RELATIONS <= set(
        preferred["relations_operations_and_dynamics"]
    )
    assert {
        item.split(":", 1)[0] for item in preferred["formalization_seeds"]
    } == conceptual_quality.REQUIRED_FORMALIZATION_IDS
    authority = result["conceptual_authority"]
    assert authority["internal_correlated_rubric_pass"] is True
    assert authority["panel_evidence_class"] == "correlated_internal_critique"
    assert authority["external_depth_validation_status"] == "unavailable"
    assert authority["external_understanding_validation_status"] == "unavailable"
    assert authority["internal_evaluation_decisions"] == ["prefer"]
    assert authority["proof_ready"] is False
    assert acceptance["checks"]["G2_G4_pass_from_bound_internal_correlated_evidence"]
    assert acceptance["checks"]["synthesizer_materially_extends_reflection"]


def test_support_only_synthesizer_delta_is_rejected() -> None:
    parent, synthesis, _ = _fresh_material_transition()
    canonical_validation.validate_material_reflective_transition(parent, synthesis)
    support_only = json.loads(json.dumps(synthesis))
    support_only["reflection_rounds"] = json.loads(
        json.dumps(parent["reflection_rounds"])
    )
    support_only["conceptual_systems"] = json.loads(
        json.dumps(parent["conceptual_systems"])
    )
    with pytest.raises(
        canonical_validation.CanonicalValidationError,
        match="differs from its bound conceptual evidence|semantic maturation",
    ):
        canonical_validation.validate_material_reflective_transition(
            parent, support_only
        )


def test_exact_but_semantically_irrelevant_probe_patch_is_rejected() -> None:
    parent, synthesis, snapshot = _fresh_material_transition()
    sham_systems = json.loads(json.dumps(synthesis["conceptual_systems"]))
    sham_rounds = json.loads(json.dumps(synthesis["reflection_rounds"]))
    selected_id = parent["independent_evaluation_evidence"][0]["preferred_system_id"]
    selected = next(row for row in sham_systems if row["system_id"] == selected_id)
    selected["formalization_seeds"][4] = (
        "YM21-F05: Add a syntactically detailed but target-irrelevant bookkeeping convention with no path-comparison content."
    )
    selected["formalization_seeds"][6] = (
        "YM21-F07: Add another equally long bookkeeping convention whose terminology does not answer the probe."
    )
    selected["correction_conditions"][3] = (
        "YM21-C04: Revise the typography if the decorative convention becomes inconvenient."
    )
    sham_objection = (
        "The notation could be aesthetically uneven even though this objection says nothing about regulator-path composition."
    )
    sham_correction = (
        "Rewrite the notation until the presentation is visually uniform, without testing any common-endpoint transport claim."
    )
    sham_rounds[-1]["strongest_objections"][-1] = sham_objection
    sham_rounds[-1]["correction_tests"] = [sham_correction]
    sham_rounds[-1]["semantic_patch_links"] = [
        {
            "candidate_ref": selected_id,
            "objection": sham_objection,
            "correction_test": sham_correction,
            "changed_paths": ["/correction_conditions", "/formalization_seeds"],
        }
    ]
    sham_evidence = conceptual_quality.build_evidence(
        systems=sham_systems,
        rounds=sham_rounds,
        snapshot=snapshot,
        proposal_receipt_ids=[
            "opreceipt-regression-parent",
            "opreceipt-regression-parallel",
            "opreceipt-regression-experiment",
        ],
        stage_id="synthesis",
        previous_evidence=parent["independent_evaluation_evidence"][0],
    )
    sham_packet = {
        "conceptual_systems": sham_systems,
        "reflection_rounds": sham_rounds,
        "independent_evaluation_evidence": [sham_evidence],
    }
    assert sham_evidence["stage_comparison"]["material"] is True
    with pytest.raises(
        canonical_validation.CanonicalValidationError,
        match="target-relevant semantic carriers",
    ):
        canonical_validation.validate_material_reflective_transition(
            parent, sham_packet
        )


def test_conceptual_coherence_below_half_fails_without_erasing_dissent() -> None:
    snapshot, assimilation, portfolio, parallel = _current_ym_material_inputs()
    systems, rounds, _ = canonical_runner._ym_conceptual_material(
        snapshot=snapshot,
        assimilation=assimilation,
        portfolio=portfolio,
        parallel=parallel,
    )
    weakened = json.loads(json.dumps(systems))
    baseline = conceptual_quality.build_evidence(
        systems=systems,
        rounds=rounds[:3],
        snapshot=snapshot,
        proposal_receipt_ids=["opreceipt-regression-baseline"],
        stage_id="parent",
    )
    preferred = next(
        row
        for row in weakened
        if row["system_id"] == baseline["preferred_system_id"]
    )
    preferred["residual_contradictions"].append(
        "A second unresolved contradiction lowers independently measured coherence below the release floor."
    )
    with pytest.raises(
        ContractError,
        match="structural screen failed|threshold failed: coherence",
    ):
        conceptual_quality.build_evidence(
            systems=weakened,
            rounds=rounds,
            snapshot=snapshot,
            proposal_receipt_ids=["opreceipt-regression-parent"],
            stage_id="parent",
        )


def test_rival_intuitions_are_only_pre_targeted_repair_and_causally_rebased() -> None:
    portfolio = json.loads(
        (integration.NORMALIZED_ROOT / "aggressive_rival_portfolio.json").read_text(
            encoding="utf-8"
        )
    )
    literature = json.loads(integration.DEFAULT_LITERATURE.read_text(encoding="utf-8"))
    sources = {row["source_id"]: row for row in literature["sources"]}
    hypotheses = {row["hypothesis_id"]: row for row in portfolio["hypotheses"]}
    for seed in integration.RIVAL_SEEDS:
        row = hypotheses[seed["id"]]
        intuition = row["pre_targeted_repair_intuition"]
        rebase = row["literature_rebase"]
        expected_sources = [item[0] for item in seed["sources"]]
        assert intuition["text"] == seed["intuition"]
        assert intuition["captured_at"] == integration.PRE_TARGETED_REPAIR_INTUITION_CAPTURED_AT
        assert intuition["full_frontier_search_precedence"] == "unknown"
        assert "not a pre-search claim" in intuition["temporal_boundary"]
        assert rebase["mapping_phase"] == "targeted_repair_after_bounded_search"
        assert rebase["mapped_at"] == literature["retrieved_at"]
        assert rebase["source_ids"] == expected_sources
        assert rebase["priority_effect"]["changed_by_source_ids"] == expected_sources
        assert len(rebase["required_revisions"]) >= 2
        effects = {item["source_id"]: item for item in rebase["causal_effects"]}
        assert set(effects) == set(expected_sources)
        for source_id, effect in effects.items():
            assert effect["source_domain"] == sources[source_id]["domain"]
            assert effect["transfer_boundary"] == sources[source_id]["transfer_boundary"]
            assert effect["claim_status"] == sources[source_id]["claim_status"]
    for hypothesis_id in ("YM21-R02", "YM21-R08", "YM21-R10"):
        assert integration.DIRECT_CHALLENGER_ID in hypotheses[hypothesis_id][
            "literature_rebase"
        ]["source_ids"]


def test_broad_frontier_capture_has_six_non_id_seeded_lanes_and_raw_dispositions() -> None:
    capture = json.loads(integration.BROAD_FRONTIER_CAPTURE.read_text(encoding="utf-8"))
    integration.validate_frontier_search_capture(capture)
    assert {row["lane_type"] for row in capture["lanes"]} == set(LANE_TYPES)
    assert capture["provider"]["receipt_status"] == "externally_executed_then_frozen"
    assert capture["provider"]["executable_replay_status"] == "frozen_response_adapter_only"
    by_source = {row["source_id"]: row for row in capture["raw_results"]}
    for source_id in (
        integration.DIRECT_CHALLENGER_ID,
        "zenodo-19614728",
        "preprints-202604.0332-v1",
        "ssrn-4819820",
    ):
        assert by_source[source_id]["claim_status"] == "unverified_challenger"
    for source_id in ("ssrn-6141826", "ssrn-6614481", "zenodo-21068209"):
        assert by_source[source_id]["disposition"].startswith("excluded_inaccessible")


def test_direct_challenger_mappings_are_claim_specific_and_counterfactual_checked() -> None:
    literature = json.loads(integration.DEFAULT_LITERATURE.read_text(encoding="utf-8"))
    assimilation = json.loads(
        integration.CANONICAL_LITERATURE_ASSIMILATION.read_text(encoding="utf-8")
    )
    mappings = assimilation["theory_mappings"]
    integration.validate_direct_claim_theory_mappings(mappings, literature)
    direct = [row for row in mappings if row["source_id"] == integration.DIRECT_CHALLENGER_ID]
    target_sets = {
        tuple(sorted(value for value in row["theory_object_ids"] if value.startswith("YM21-R")))
        for row in direct
    }
    assert len(target_sets) == 6

    broadcast = json.loads(json.dumps(mappings))
    first = next(row for row in broadcast if row["source_id"] == integration.DIRECT_CHALLENGER_ID)
    first["theory_object_ids"] = sorted({*first["theory_object_ids"], "YM21-R07"})
    with pytest.raises(integration.IntegrationError, match="claim-specific rival mapping drift"):
        integration.validate_direct_claim_theory_mappings(broadcast, literature)

    rationale_swap = json.loads(json.dumps(mappings))
    direct_rows = [row for row in rationale_swap if row["source_id"] == integration.DIRECT_CHALLENGER_ID]
    direct_rows[0]["conceptual_change"] = direct_rows[1]["conceptual_change"]
    with pytest.raises(integration.IntegrationError, match="rationale/counterfactual"):
        integration.validate_direct_claim_theory_mappings(rationale_swap, literature)


def test_incumbent_overlap_is_typed_digest_bound_and_independently_evaluated() -> None:
    portfolio = json.loads(
        (integration.NORMALIZED_ROOT / "aggressive_rival_portfolio.json").read_text(encoding="utf-8")
    )
    evaluation = json.loads(integration.INCUMBENT_OVERLAP_EVALUATION.read_text(encoding="utf-8"))
    integration.validate_incumbent_overlap_evaluation(evaluation, portfolio)
    assert evaluation["evaluator_identity"] != evaluation["generator_identity"]
    assert evaluation["independence"]["generator_externality_flags_treated_as_untrusted_inputs"] is True
    by_id = {row["candidate_id"]: row for row in evaluation["evaluations"]}
    assert by_id["YM21-R10"]["verdict"] == "incumbent_control_identity"
    for candidate_id in ("YM21-R01", "YM21-R02", "YM21-R08", "YM21-R09"):
        assert "endpoint_overlap" in by_id[candidate_id]["overlap_types"]

    self_attested = json.loads(json.dumps(evaluation))
    self_attested["evaluator_identity"] = self_attested["generator_identity"]
    self_attested.pop("content_digest")
    self_attested["content_digest"] = integration.sha256_bytes(
        integration.canonical_bytes(self_attested)
    )
    with pytest.raises(integration.IntegrationError, match="not independent"):
        integration.validate_incumbent_overlap_evaluation(self_attested, portfolio)


def test_integrated_registry_activates_exactly_three_and_reuses_existing_skills() -> None:
    registry = json.loads(integration.YM_REGISTRY.read_text(encoding="utf-8"))
    assert {row["skill"] for row in registry["active_imported_skills"]} == set(integration.ACTIVE_NEW_SKILLS)
    assert len(registry["active_imported_skills"]) == 3
    assert set(registry["reused_existing_skills"]) == set(integration.REUSED_SKILLS)
    assert set(registry["external_only_publication_skills"]) == set(integration.PUBLICATION_SKILLS)
    assert registry["controller"] == "reflective-conceptual-discovery"
    assert registry["replay"]["role"] == "secondary_support"
    snapshot = json.loads(
        integration.CANONICAL_LITERATURE_SNAPSHOT.read_text(encoding="utf-8")
    )
    assimilation = json.loads(
        integration.CANONICAL_LITERATURE_ASSIMILATION.read_text(encoding="utf-8")
    )
    interop = registry["canonical_literature_interop"]
    assert interop["snapshot"]["snapshot_id"] == snapshot["snapshot_id"]
    assert interop["snapshot"]["content_digest"] == snapshot["content_digest"]
    assert interop["snapshot"]["provenance_mode"] == "local_only"
    assert interop["assimilation"]["packet_id"] == assimilation["packet_id"]
    assert interop["assimilation"]["content_digest"] == assimilation["content_digest"]
    assert interop["assimilation"]["active_investment_gate"] == "blocked_local_only"
    assert "--theory-state-digest <canonical-state-digest>" in registry[
        "pre_cycle_hook"
    ]["command"]


def test_publication_skills_are_preserved_externally_but_not_activated() -> None:
    mapping = json.loads(
        (integration.NORMALIZED_ROOT / "publication_capability_map.json").read_text(encoding="utf-8")
    )
    assert len(mapping["skills"]) == 10
    assert all(row["local_activation"] is False for row in mapping["skills"])
    for name in integration.PUBLICATION_SKILLS:
        assert not (ROOT / "skills/yang_mills" / name / "SKILL.md").exists()


def test_todo_deck_is_acceptance_ready_without_premature_resolution() -> None:
    deck_path = ROOT / "agentic/todos/ym_representational_dynamics_20260721_todos.yaml"
    deck = json.loads(deck_path.read_text(encoding="utf-8"))
    assert [row["id"] for row in deck] == [f"YM21-{index:03d}" for index in range(1, 11)]
    assert all(row["status"] in {"open", "resolved"} and row["evidence"] for row in deck)
    assert all(row.get("validation_commands") for row in deck)
    for row in deck:
        if row["status"] == "resolved":
            assert any(str(item).startswith("receipt:") for item in row["evidence"])


def test_raw_replay_preserves_stage70_failure_without_skip_or_xfail() -> None:
    report = json.loads((integration.REPORT_ROOT / "replay_report.json").read_text(encoding="utf-8"))
    assert report["status"] == "passed_with_qualified_stage70_drift"
    assert report["no_observed_skip_or_xfail"] is True
    assert report["suppression_policy"] == {
        "failures_suppressed": False,
        "skip_injected": False,
        "xfail_used": False,
    }
    stage70 = next(row for row in report["stages"] if row["stage"] == "70_h3_exact_multistar")
    assert stage70["raw_status"] == "failed"
    assert stage70["counts"]["passed"] == 13
    assert stage70["counts"]["failed"] == 1
    assert stage70["effective_status"] == "qualified_noncanonical_witness_drift"
