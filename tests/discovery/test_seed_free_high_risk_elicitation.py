# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial controls for proposal-field-free authored-operator elicitation."""

from __future__ import annotations
import copy
import json
import subprocess
import sys
from pathlib import Path
import pytest
from agentic.discovery import hypotheses as hypothesis_runtime
from agentic.discovery.contracts import ContractError, canonical_digest
from agentic.discovery.hypotheses import (
    _callable_digest,
    _deterministic_content_adjudicator,
    _proposal_field_free_authored_operator_proposals,
    build_demo_high_risk_portfolio,
    build_hidden_elicitation_prompt,
    migrate_seed_free_high_risk_elicitation_v1,
    replay_proposal_field_free_high_risk_elicitation,
    run_proposal_field_free_high_risk_elicitation,
    run_seed_free_high_risk_elicitation,
    semantic_hypothesis_signature,
    validate_seed_free_high_risk_elicitation,
)
from agentic.discovery.literature import build_demo_literature_snapshot

ROOT = Path(__file__).resolve().parents[2]


def test_slice_defaults_bind_every_component_and_reject_opaque_or_recursive_values():
    """Literal callback slices have stable identities without a repr fallback."""

    def callback_with(selection):
        def callback(values, selection=selection):
            return values[selection]

        return callback

    baseline = _callable_digest(callback_with(slice(1, 9, 2)))
    assert baseline == _callable_digest(callback_with(slice(1, 9, 2)))
    changed = [slice(2, 9, 2), slice(1, 8, 2), slice(1, 9, 3)]
    assert all(_callable_digest(callback_with(value)) != baseline for value in changed)

    class Opaque:
        def __repr__(self):
            raise AssertionError("opaque values must never be fingerprinted by repr")

    with pytest.raises(ContractError, match="without stable executable serialization"):
        _callable_digest(callback_with(slice(Opaque(), None, None)))
    recursive = []
    selection = slice(recursive, None, None)
    recursive.append(selection)
    with pytest.raises(ContractError, match="recursive executable value"):
        _callable_digest(callback_with(selection))


def _inputs():
    snapshot = build_demo_literature_snapshot(target_id="elicitation-target")
    charter = {
        "target_id": snapshot["target_id"],
        "target_statement": "Explain exact global recurrence without weakening quantifiers.",
        "theory_state_digest": snapshot["theory_state_digest"],
        "root_tensions": [
            "Local witnesses do not explain global recurrence.",
            "Distinct barriers lack a common mechanism.",
        ],
        "target_commitments": ["Preserve exact target identity and quantifier order."],
        "protected_successes": ["Recover the verified boundary regime."],
        "forbidden_target_drift": "No finite-only, average-case, or lexical proxy.",
    }
    prompts = [
        build_hidden_elicitation_prompt(
            prompt_id=f"prompt-{i}",
            target_id=snapshot["target_id"],
            theory_state_digest=snapshot["theory_state_digest"],
            literature_snapshot_digest=snapshot["content_digest"],
            prompt_text=f"Probe conceptual corner {i} without any proposed mechanism or expected answer.",
        )
        for i in range(3)
    ]
    return snapshot, charter, prompts


def _rehash_study(study, *repetition_indices):
    for index in repetition_indices:
        repetition = study["repetitions"][index]
        repetition["content_digest"] = canonical_digest(
            {key: value for key, value in repetition.items() if key != "content_digest"}
        )
    study["content_digest"] = canonical_digest(
        {key: value for key, value in study.items() if key != "content_digest"}
    )


def _legacy_v1_projection(study):
    fields = {
        "schema_version",
        "study_id",
        "target_id",
        "theory_state_digest",
        "literature_snapshot_id",
        "literature_snapshot_digest",
        "generation_mode",
        "generator_authority",
        "adjudicator_authority",
        "authority_separation",
        "protocol",
        "hidden_prompt_seals",
        "repetitions",
        "repeated_diversity",
        "study_status",
        "eligibility",
        "external_human_evidence",
        "claim_boundary",
        "content_digest",
    }
    legacy = {
        key: copy.deepcopy(value) for key, value in study.items() if key in fields
    }
    legacy["schema_version"] = "1.0"
    legacy["generation_mode"] = (
        "seed_free_provider"
        if study["generation_mode"] == "proposal_field_free_provider"
        else "seed_free_deterministic"
    )
    legacy["content_digest"] = canonical_digest(
        {key: value for key, value in legacy.items() if key != "content_digest"}
    )
    return legacy


def test_repeated_study_is_proposal_field_free_blind_diverse_and_human_null():
    snapshot, charter, prompts = _inputs()
    study = run_proposal_field_free_high_risk_elicitation(
        charter,
        snapshot,
        hidden_prompts=prompts,
        repetitions=5,
        counterbalance_seed="stable-seed",
    )
    assert study["generation_mode"] == "proposal_field_free_authored_operator"
    assert study["protocol"]["proposal_field_status"] == "absent"
    assert study["protocol"]["authored_operator_atlas_digest"].startswith("sha256:")
    assert study["protocol"]["generator_policy_digest"].startswith("sha256:")
    assert study["protocol"]["scoring_policy_digest"].startswith("sha256:")
    incumbent = study["equal_count_authored_incumbent_comparison"]
    assert incumbent["condition"] == "equal_count_authored_incumbent_deck"
    assert incumbent["proposal_count"] == 10
    assert incumbent["generation_opportunity_matched"] is False
    assert incumbent["literature_exposure_matched"] is False
    assert (
        study["descriptive_condition_comparison"]["advantage_inference_authorized"]
        is False
    )
    assert study["descriptive_condition_comparison"]["iid_assumption"] is False
    assert (
        study["exploration_selection"]["status"] == "selected_for_internal_exploration"
    )
    assert study["exploration_selection"]["truth_authorized"] is False
    assert len(study["repetitions"]) == 5
    assert study["repeated_diversity"]["status"] == "passed"
    assert study["external_human_evidence"]["status"] == "unavailable"
    assert study["eligibility"] == {
        "internal_exploration": "eligible_internal_only",
        "internal_refinement": "eligible_internal_only",
        "theorem_investment": "requires_distinct_formal_evidence",
        "physics_investment": "requires_distinct_domain_evidence",
        "efficacy_claim": "not_authorized",
        "authority_basis": "internal_protocol_controls_only",
    }
    assert all(
        row["authored_template_copy_control"]["status"] == "passed"
        for row in study["repetitions"]
    )
    assert all(
        set(rating["scores"])
        == {
            "essential_relevance",
            "conceptual_depth",
            "unification",
            "corner_diversity",
            "correction_specificity",
        }
        for row in study["repetitions"]
        for rating in row["blind_adjudication"]["ratings"]
    )
    assert all(
        row["portfolio"]["generation_provenance"]["mode"]
        == "proposal_field_free_authored_operator"
        for row in study["repetitions"]
    )
    assert all(
        row["portfolio"]["generation_provenance"]["authored_operator_atlas_digest"]
        == study["protocol"]["authored_operator_atlas_digest"]
        for row in study["repetitions"]
    )


def test_default_callable_authorities_are_cross_process_stable() -> None:
    local = {
        "generator": _callable_digest(_proposal_field_free_authored_operator_proposals),
        "adjudicator": _callable_digest(_deterministic_content_adjudicator),
    }
    code = (
        "import json; "
        "from agentic.discovery.hypotheses import "
        "_callable_digest, _deterministic_content_adjudicator, "
        "_proposal_field_free_authored_operator_proposals; "
        "print(json.dumps({'generator': _callable_digest("
        "_proposal_field_free_authored_operator_proposals), "
        "'adjudicator': _callable_digest(_deterministic_content_adjudicator)}, "
        "sort_keys=True))"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(completed.stdout) == local


def test_same_seed_replays_exactly_while_repetitions_remain_distinct():
    snapshot, charter, prompts = _inputs()
    study = run_seed_free_high_risk_elicitation(
        charter,
        snapshot,
        hidden_prompts=prompts,
        repetitions=5,
        counterbalance_seed="replay-seed",
    )
    replay = replay_proposal_field_free_high_risk_elicitation(
        study,
        charter,
        snapshot,
        hidden_prompts=prompts,
        counterbalance_seed="replay-seed",
    )
    assert replay["same_seed_exact_replay"]
    assert study["repeated_diversity"]["unique_deck_count"] == 5
    schedule_ids = [row["schedule_slot_id"] for row in study["repetitions"]]
    content_ids = [row["semantic_content_id"] for row in study["repetitions"]]
    semantic_ids = [row["semantic_output_id"] for row in study["repetitions"]]
    evidence_ids = [row["evidence_repetition_id"] for row in study["repetitions"]]
    assert len(set(schedule_ids)) == len(schedule_ids)
    assert len(set(content_ids)) == len(content_ids)
    assert len(set(semantic_ids)) == len(semantic_ids)
    assert len(set(evidence_ids)) == len(evidence_ids)
    assert [
        row["semantic_repetition_id"] for row in study["repetitions"]
    ] == semantic_ids
    assert [row["repetition_id"] for row in study["repetitions"]] == evidence_ids


def test_identical_prompt_and_provider_output_cannot_collide_across_schedule_slots():
    snapshot, charter, prompts = _inputs()
    copied = copy.deepcopy(build_demo_high_risk_portfolio(snapshot)["hypotheses"])

    def constant_provider(_request):
        return {"proposals": copy.deepcopy(copied)}

    authority = {
        "authority_id": "fixture.constant-output-provider",
        "authority_class": "test_provider",
    }
    study = run_proposal_field_free_high_risk_elicitation(
        charter,
        snapshot,
        hidden_prompts=prompts[:1],
        repetitions=7,
        counterbalance_seed="collision-control",
        provider=constant_provider,
        provider_authority=authority,
    )
    repetitions = study["repetitions"]
    assert len({row["provider_output"]["proposal_digest"] for row in repetitions}) == 1
    assert len({row["semantic_content_id"] for row in repetitions}) == 1
    assert len({row["prompt_seal"]["semantic_prompt_id"] for row in repetitions}) == 1
    assert len({row["schedule_slot_id"] for row in repetitions}) == 7
    assert len({row["semantic_output_id"] for row in repetitions}) == 7
    assert len({row["evidence_repetition_id"] for row in repetitions}) == 7
    assert replay_proposal_field_free_high_risk_elicitation(
        study,
        charter,
        snapshot,
        hidden_prompts=prompts[:1],
        counterbalance_seed="collision-control",
        provider=constant_provider,
        provider_authority=authority,
    )["same_seed_exact_replay"]


def test_rehashed_repetition_identity_collisions_and_forgery_fail_closed():
    snapshot, charter, prompts = _inputs()
    study = run_proposal_field_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts
    )

    schedule_collision = copy.deepcopy(study)
    schedule_collision["repetitions"][1]["schedule_slot_id"] = schedule_collision[
        "repetitions"
    ][0]["schedule_slot_id"]
    _rehash_study(schedule_collision, 1)
    with pytest.raises(ContractError, match="schedule-slot identities must be unique"):
        validate_seed_free_high_risk_elicitation(
            schedule_collision,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )

    content_collision = copy.deepcopy(study)
    content_collision["repetitions"][1]["semantic_content_id"] = content_collision[
        "repetitions"
    ][0]["semantic_content_id"]
    _rehash_study(content_collision, 1)
    with pytest.raises(
        ContractError,
        match="semantic-content identity differs from canonical proposal content",
    ):
        validate_seed_free_high_risk_elicitation(
            content_collision,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )

    semantic_collision = copy.deepcopy(study)
    collided_semantic = semantic_collision["repetitions"][0]["semantic_output_id"]
    semantic_collision["repetitions"][1]["semantic_output_id"] = collided_semantic
    semantic_collision["repetitions"][1]["semantic_repetition_id"] = collided_semantic
    _rehash_study(semantic_collision, 1)
    with pytest.raises(
        ContractError, match="semantic-output identities must be unique"
    ):
        validate_seed_free_high_risk_elicitation(
            semantic_collision,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )

    evidence_collision = copy.deepcopy(study)
    collided_id = evidence_collision["repetitions"][0]["evidence_repetition_id"]
    evidence_collision["repetitions"][1]["evidence_repetition_id"] = collided_id
    evidence_collision["repetitions"][1]["repetition_id"] = collided_id
    _rehash_study(evidence_collision, 1)
    with pytest.raises(
        ContractError, match="evidence repetition identities must be unique"
    ):
        validate_seed_free_high_risk_elicitation(
            evidence_collision,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )

    evidence_forgery = copy.deepcopy(study)
    forged_id = "elicitation-evidence-repetition.forged"
    evidence_forgery["repetitions"][0]["evidence_repetition_id"] = forged_id
    evidence_forgery["repetitions"][0]["repetition_id"] = forged_id
    _rehash_study(evidence_forgery, 0)
    with pytest.raises(ContractError, match="evidence repetition identity differs"):
        validate_seed_free_high_risk_elicitation(
            evidence_forgery,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )

    semantic_alias = copy.deepcopy(study)
    semantic_alias["repetitions"][0][
        "semantic_repetition_id"
    ] = "elicitation-semantic-output.forged"
    _rehash_study(semantic_alias, 0)
    with pytest.raises(ContractError, match="must exactly alias semantic_output_id"):
        validate_seed_free_high_risk_elicitation(
            semantic_alias,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )

    legacy_alias = copy.deepcopy(study)
    legacy_alias["repetitions"][0][
        "repetition_id"
    ] = "elicitation-exact-evidence.forged"
    _rehash_study(legacy_alias, 0)
    with pytest.raises(
        ContractError, match="must exactly alias evidence_repetition_id"
    ):
        validate_seed_free_high_risk_elicitation(
            legacy_alias,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )


def test_schedule_and_semantic_output_ignore_authority_while_exact_evidence_binds_it():
    snapshot, charter, prompts = _inputs()
    baseline = run_proposal_field_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts
    )

    def alternate_generator(request):
        return hypothesis_runtime._proposal_field_free_authored_operator_proposals(
            request
        )

    def alternate_adjudicator(request):
        response = hypothesis_runtime._deterministic_content_adjudicator(request)
        # Preserve validity while ensuring the exact adjudicator response differs.
        response["ratings"][0]["scores"]["conceptual_depth"] = round(
            response["ratings"][0]["scores"]["conceptual_depth"] - 0.01, 6
        )
        return response

    alternate = run_proposal_field_free_high_risk_elicitation(
        charter,
        snapshot,
        hidden_prompts=prompts,
        provider=alternate_generator,
        provider_authority={
            "authority_id": "fixture.alternate-generator",
            "authority_class": "test",
        },
        adjudicator=alternate_adjudicator,
        adjudicator_authority={
            "authority_id": "fixture.alternate-adjudicator",
            "authority_class": "test",
        },
    )
    assert [row["schedule_slot_id"] for row in baseline["repetitions"]] == [
        row["schedule_slot_id"] for row in alternate["repetitions"]
    ]
    assert [row["semantic_content_id"] for row in baseline["repetitions"]] == [
        row["semantic_content_id"] for row in alternate["repetitions"]
    ]
    assert [row["semantic_output_id"] for row in baseline["repetitions"]] == [
        row["semantic_output_id"] for row in alternate["repetitions"]
    ]
    assert [row["evidence_repetition_id"] for row in baseline["repetitions"]] != [
        row["evidence_repetition_id"] for row in alternate["repetitions"]
    ]


def test_authored_template_copy_is_detected_and_mode_is_honest():
    snapshot, charter, prompts = _inputs()
    authored = copy.deepcopy(build_demo_high_risk_portfolio(snapshot)["hypotheses"])

    def copied_provider(_request):
        return {"proposals": copy.deepcopy(authored)}

    study = run_seed_free_high_risk_elicitation(
        charter,
        snapshot,
        hidden_prompts=prompts,
        repetitions=5,
        provider=copied_provider,
        provider_authority={
            "authority_id": "fixture.copied-provider",
            "authority_class": "test_provider",
        },
    )
    assert study["generation_mode"] == "proposal_field_free_provider"
    assert study["protocol"]["authored_operator_atlas_digest"] is None
    assert study["study_status"] == "protocol_completed_with_failed_controls"
    assert all(
        row["authored_template_copy_control"]["status"] == "failed"
        for row in study["repetitions"]
    )
    assert (
        study["exploration_selection"]["status"] == "withheld_failed_protocol_controls"
    )
    assert study["exploration_selection"]["selected_repetition_index"] is None
    authored_portfolio = build_demo_high_risk_portfolio(snapshot)
    assert (
        authored_portfolio["generation_provenance"]["mode"]
        == "operator_instantiated_from_authored_proposals"
    )


def test_wrong_prompt_target_digest_and_provider_authority_fail_closed():
    snapshot, charter, prompts = _inputs()
    wrong = copy.deepcopy(prompts)
    wrong[0]["target_id"] = "wrong-target"
    wrong[0]["content_digest"] = canonical_digest(
        {key: value for key, value in wrong[0].items() if key != "content_digest"}
    )
    with pytest.raises(ContractError, match="prompt target mismatch"):
        run_seed_free_high_risk_elicitation(charter, snapshot, hidden_prompts=wrong)

    def provider(_request):
        return []

    with pytest.raises(ContractError, match="authority digest mismatch"):
        run_seed_free_high_risk_elicitation(
            charter,
            snapshot,
            hidden_prompts=prompts,
            provider=provider,
            provider_authority={
                "authority_id": "fixture.provider",
                "authority_class": "test",
                "expected_callable_digest": canonical_digest("wrong"),
            },
        )


def test_output_seal_tampering_is_rejected():
    snapshot, charter, prompts = _inputs()
    study = run_seed_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts
    )
    tampered = copy.deepcopy(study)
    tampered["repetitions"][0]["provider_output_seal"]["proposal_digest"] = (
        canonical_digest("tampered")
    )
    tampered["repetitions"][0]["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in tampered["repetitions"][0].items()
            if key != "content_digest"
        }
    )
    tampered["content_digest"] = canonical_digest(
        {key: value for key, value in tampered.items() if key != "content_digest"}
    )
    with pytest.raises(ContractError, match="output seal"):
        validate_seed_free_high_risk_elicitation(
            tampered,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )


def test_rehashed_forged_rating_and_warrant_are_rejected_by_callback_replay():
    snapshot, charter, prompts = _inputs()
    study = run_seed_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts
    )
    forged = copy.deepcopy(study)
    adjudication = forged["repetitions"][0]["blind_adjudication"]
    adjudication["ratings"][0]["scores"]["conceptual_depth"] = 0.0
    adjudication["ratings"][0]["warrants"]["conceptual_depth"] = [
        "attacker-authored",
        canonical_digest("attacker"),
    ]
    adjudication["response_digest"] = canonical_digest(
        {"ratings": adjudication["ratings"]}
    )
    adjudication["dimension_means"]["conceptual_depth"] = 0.0
    _rehash_study(forged, 0)
    with pytest.raises(
        ContractError, match="blind adjudication differs from exact callback replay"
    ):
        validate_seed_free_high_risk_elicitation(
            forged,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )


def test_rehashed_forged_provider_proposal_is_rejected_by_exact_content_identity():
    snapshot, charter, prompts = _inputs()
    study = run_seed_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts
    )
    forged = copy.deepcopy(study)
    repetition = forged["repetitions"][0]
    output = repetition["provider_output"]
    output["proposals"][0]["genealogy"] = ["attacker-authored-lineage"]
    output["proposal_digest"] = canonical_digest(output["proposals"])
    raw = (
        output["proposals"]
        if output["response_shape"] == "proposal_sequence"
        else {"proposals": output["proposals"]}
    )
    output["raw_response_digest"] = canonical_digest(raw)
    repetition["provider_receipt"]["output_digest"] = output["proposal_digest"]
    repetition["provider_receipt"]["raw_response_digest"] = output[
        "raw_response_digest"
    ]
    repetition["provider_output_seal"].update(
        {
            "proposal_digest": output["proposal_digest"],
            "raw_response_digest": output["raw_response_digest"],
        }
    )
    _rehash_study(forged, 0)
    with pytest.raises(
        ContractError,
        match="semantic-content identity differs from canonical proposal content",
    ):
        validate_seed_free_high_risk_elicitation(
            forged,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )


def test_rehashed_authority_relabel_is_rejected():
    snapshot, charter, prompts = _inputs()
    study = run_seed_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts
    )
    forged = copy.deepcopy(study)
    forged["generator_authority"]["authority_id"] = "attacker.generator"
    forged["generator_authority"]["authority_class"] = "claimed_external_authority"
    _rehash_study(forged)
    with pytest.raises(ContractError, match="generator authority metadata mismatch"):
        validate_seed_free_high_risk_elicitation(
            forged,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )


def test_prompt_schedule_alias_status_and_claim_mutations_fail_closed():
    snapshot, charter, prompts = _inputs()
    study = run_seed_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts
    )
    prompt_forgery = copy.deepcopy(study)
    prompt_forgery["repetitions"][0]["prompt_seal"] = copy.deepcopy(
        prompt_forgery["repetitions"][1]["prompt_seal"]
    )
    _rehash_study(prompt_forgery, 0)
    with pytest.raises(ContractError, match="prompt seal or schedule"):
        validate_seed_free_high_risk_elicitation(
            prompt_forgery,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )
    alias_forgery = copy.deepcopy(study)
    alias_forgery["repetitions"][0]["blind_adjudication"]["alias_resolution"][0][
        "hypothesis_id"
    ] = "hypothesis.forged"
    _rehash_study(alias_forgery, 0)
    with pytest.raises(ContractError, match="blind adjudication"):
        validate_seed_free_high_risk_elicitation(
            alias_forgery,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )
    for field, value, match in [
        ("study_status", "protocol_completed_with_failed_controls", "study status"),
        ("claim_boundary", "This packet proves conceptual depth.", "claim boundary"),
    ]:
        forged = copy.deepcopy(study)
        forged[field] = value
        _rehash_study(forged)
        with pytest.raises(ContractError, match=match):
            validate_seed_free_high_risk_elicitation(
                forged,
                charter=charter,
                literature_snapshot=snapshot,
                hidden_prompts=prompts,
            )


def test_same_callable_cannot_be_relabelled_as_two_authorities():
    snapshot, charter, prompts = _inputs()

    class DualAuthority:
        def __call__(self, request):
            if "hidden_prompt_text" in request:
                return hypothesis_runtime._seed_free_protocol_proposals(request)
            return hypothesis_runtime._deterministic_content_adjudicator(request)

    dual = DualAuthority()
    with pytest.raises(ContractError, match="executable authorities must be distinct"):
        run_seed_free_high_risk_elicitation(
            charter,
            snapshot,
            hidden_prompts=prompts,
            provider=dual,
            provider_authority={
                "authority_id": "fixture.generator",
                "authority_class": "test",
            },
            adjudicator=dual,
            adjudicator_authority={
                "authority_id": "fixture.adjudicator",
                "authority_class": "test",
            },
        )


def test_non_replayable_provider_is_typed_unverifiable_and_rejected():
    snapshot, charter, prompts = _inputs()

    def provider(_request):
        return []

    with pytest.raises(ContractError, match="unsupported and unverifiable"):
        run_seed_free_high_risk_elicitation(
            charter,
            snapshot,
            hidden_prompts=prompts,
            provider=provider,
            provider_authority={
                "authority_id": "fixture.provider",
                "authority_class": "test",
                "replayability": "unverifiable",
            },
        )


def test_semantic_diversity_signature_ignores_repetition_suffix_and_genealogy():
    candidate = build_demo_high_risk_portfolio()["hypotheses"][0]
    left, right = copy.deepcopy(candidate), copy.deepcopy(candidate)
    for row, suffix in ((left, "_r1"), (right, "_r9")):
        row["ontology_delta"]["new_primitives"] = [
            item + suffix for item in row["ontology_delta"]["new_primitives"]
        ]
        row["ontology_delta"]["new_relations"] = [
            item + suffix for item in row["ontology_delta"]["new_relations"]
        ]
        row["mechanism"] += " marker" + suffix
        row["maturation_question"] += " marker" + suffix
        row["genealogy"] = ["run-specific" + suffix]
    assert semantic_hypothesis_signature(left) == semantic_hypothesis_signature(right)


def test_strict_nested_schema_rejects_unknown_fields():
    snapshot, charter, prompts = _inputs()
    study = run_seed_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts
    )
    forged = copy.deepcopy(study)
    forged["repetitions"][0]["provider_output_seal"]["unknown"] = True
    _rehash_study(forged, 0)
    with pytest.raises(ContractError, match="Additional properties"):
        validate_seed_free_high_risk_elicitation(
            forged,
            charter=charter,
            literature_snapshot=snapshot,
            hidden_prompts=prompts,
        )


def test_seed_free_elicitation_cli_passes():
    completed = subprocess.run(
        [sys.executable, "agentic/scripts/validate_seed_free_high_risk_elicitation.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "proposal-field-free high-risk elicitation: pass" in completed.stdout


def test_legacy_api_names_are_exact_compatibility_aliases():
    snapshot, charter, prompts = _inputs()
    canonical = run_proposal_field_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts
    )
    legacy = run_seed_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts
    )
    assert legacy == canonical
    assert legacy["schema_version"] == "3.0"
    assert "seed_free" not in legacy["generation_mode"]


def test_authored_incumbent_comparison_and_selection_tampering_fail_exact_replay():
    snapshot, charter, prompts = _inputs()
    study = run_proposal_field_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts
    )
    forged_comparison = copy.deepcopy(
        study["equal_count_authored_incumbent_comparison"]
    )
    forged_comparison["generation_opportunity_matched"] = True
    for field, value, match in [
        (
            "equal_count_authored_incumbent_comparison",
            forged_comparison,
            "False|exact replayable",
        ),
        (
            "exploration_selection",
            {**study["exploration_selection"], "truth_authorized": True},
            "Additional properties|False|exact replayable",
        ),
    ]:
        forged = copy.deepcopy(study)
        forged[field] = value
        forged["content_digest"] = canonical_digest(
            {key: item for key, item in forged.items() if key != "content_digest"}
        )
        with pytest.raises(ContractError, match=match):
            validate_seed_free_high_risk_elicitation(
                forged,
                charter=charter,
                literature_snapshot=snapshot,
                hidden_prompts=prompts,
            )


def test_v1_migration_replays_exact_content_and_revokes_seed_freedom_claim():
    snapshot, charter, prompts = _inputs()
    seed = "legacy-migration-seed"
    current = run_proposal_field_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts, counterbalance_seed=seed
    )
    result = migrate_seed_free_high_risk_elicitation_v1(
        _legacy_v1_projection(current),
        charter,
        snapshot,
        hidden_prompts=prompts,
        counterbalance_seed=seed,
    )
    receipt = result["migration_receipt"]
    assert result["migrated_study"] == current
    assert receipt["source_schema_version"] == "1.0"
    assert receipt["destination_schema_version"] == "3.0"
    assert receipt["legacy_claim_status"] == "overstated_seed_freedom_revoked"
    assert receipt["content_digest"] == canonical_digest(
        {key: value for key, value in receipt.items() if key != "content_digest"}
    )


def test_v1_migration_rejects_rehashed_provider_forgery_and_shape_extension():
    snapshot, charter, prompts = _inputs()
    seed = "legacy-adversarial-seed"
    current = run_proposal_field_free_high_risk_elicitation(
        charter, snapshot, hidden_prompts=prompts, counterbalance_seed=seed
    )
    forged = _legacy_v1_projection(current)
    repetition = forged["repetitions"][0]
    output = repetition["provider_output"]
    output["proposals"][0]["genealogy"] = ["rehashed-attacker-lineage"]
    output["proposal_digest"] = canonical_digest(output["proposals"])
    raw = (
        {"proposals": output["proposals"]}
        if output["response_shape"] == "proposals_object"
        else output["proposals"]
    )
    output["raw_response_digest"] = canonical_digest(raw)
    repetition["provider_receipt"]["output_digest"] = output["proposal_digest"]
    repetition["provider_receipt"]["raw_response_digest"] = output[
        "raw_response_digest"
    ]
    repetition["provider_output_seal"].update(
        proposal_digest=output["proposal_digest"],
        raw_response_digest=output["raw_response_digest"],
    )
    _rehash_study(forged, 0)
    with pytest.raises(
        ContractError, match="provider output differs from current exact replay"
    ):
        migrate_seed_free_high_risk_elicitation_v1(
            forged, charter, snapshot, hidden_prompts=prompts, counterbalance_seed=seed
        )

    extended = _legacy_v1_projection(current)
    extended["unrecognized_authority_claim"] = True
    extended["content_digest"] = canonical_digest(
        {key: value for key, value in extended.items() if key != "content_digest"}
    )
    with pytest.raises(ContractError, match="strict v1 packet shape"):
        migrate_seed_free_high_risk_elicitation_v1(
            extended,
            charter,
            snapshot,
            hidden_prompts=prompts,
            counterbalance_seed=seed,
        )
