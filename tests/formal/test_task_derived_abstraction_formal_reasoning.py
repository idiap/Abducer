# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Task-semantic adversaries for the shared finite Category/HoTT engine."""

from __future__ import annotations

import copy

import pytest

from agentic.discovery.contracts import ContractError, canonical_digest, validate_instance
from skills.common.abstraction_formal_reasoning import (
    FormalReasoningError,
    build_category_model_and_witness,
    build_hott_model_and_witness,
    build_negative_witness,
    forge_case_artifact,
    validate_category_model,
    validate_hott_model,
    validate_task_derived_artifact,
)
from skills.common.task_relation_compiler import (
    TaskRelationCompilerError,
    compile_task_relation,
)


PHYSICAL_CARRIER = "gauge-invariant Wilson covariance in the reconstructed OS Hilbert space"
REGIME = "cutoff removal before Osterwalder-Schrader reconstruction"
QUANTIFIERS = [
    "For every declared gauge-invariant observable in the regulated family.",
    "Uniformly over the declared cutoff-removal sequence.",
]
UNTOUCHED_GATES = [
    "same-theory continuum construction",
    "Osterwalder-Schrader reconstruction",
    "uniform positive mass gap",
]


def _case(lens: str, *, physical_carrier: str | None = PHYSICAL_CARRIER) -> dict:
    obligation_id = f"physics.semantic-replay.finite-{lens}-obligation"
    relation = (
        {
            "relation_id": "relation.cutoff-reconstruction-order",
            "relation_kind": "noncommuting_composition",
            "statement": "Cutoff removal and reconstruction are two ordered routes to the target burden.",
            "source_anchor": "regulated Wilson observable",
            "target_anchor": "reflection positivity before spectral transfer",
        }
        if lens == "categorical"
        else {
            "relation_id": "relation.reconstruction-transport-coherence",
            "relation_kind": "equivalence_coherence",
            "statement": "Equivalent regulated presentations induce two predicate transports requiring a higher cell.",
            "source_anchor": "Schwinger functional",
            "target_anchor": "gauge-invariant observable carrier",
        }
    )
    candidate = (
        {
            "decision_id": "decision.compare-reconstruction-orders",
            "decision_kind": "compare_route_order",
            "action": "Compare both reconstruction orders before continuing the physical route.",
            "target_burden_id": obligation_id,
            "trigger_relation_id": relation["relation_id"],
        }
        if lens == "categorical"
        else {
            "decision_id": "decision.require-reconstruction-coherence",
            "decision_kind": "require_coherence",
            "action": "Construct the missing reconstruction transport cell before continuing the physical route.",
            "target_burden_id": obligation_id,
            "trigger_relation_id": relation["relation_id"],
        }
    )
    return {
        "case_id": f"physics.semantic-replay.{lens}",
        "target_id": "physics.semantic-replay",
        "obligation_id": obligation_id,
        "preferred_lens": lens,
        "task_semantics": {
            "pressure": "Relate cutoff removal and spectral reconstruction without commuting them by assertion.",
            "formal_pressure": "Regulator removal and reconstruction form a potentially noncommuting comparison.",
            "protected_invariants": [
                "gauge-invariant observable carrier",
                "reflection positivity before spectral transfer",
                "cutoff-uniform error accounting",
            ],
            "incumbent_primitives": [
                "regulated Wilson observable",
                "Schwinger functional",
                "Osterwalder-Schrader reflection form",
            ],
            "physical_carrier": physical_carrier,
            "regime": REGIME,
            "quantifiers": list(QUANTIFIERS),
            "falsifier": "Exhibit one observable whose two reconstruction paths disagree beyond uniform error.",
            "correction": "Quarantine the route and factor the two reconstruction orders separately.",
            "untouched_physics_gates": list(UNTOUCHED_GATES),
            "task_relations": [relation],
            "incumbent_decision": {
                "decision_id": "decision.continue-direct-reconstruction",
                "decision_kind": "continue_route",
                "action": "Continue the direct reconstruction route under the current burden.",
                "target_burden_id": obligation_id,
            },
            "lens_decisions": {lens: candidate},
        },
    }


def _reseal(artifact: dict) -> dict:
    artifact["artifact_digest"] = canonical_digest(
        {key: value for key, value in artifact.items() if key != "artifact_digest"}
    )
    return artifact


def _core_validate(lens: str, model: dict, witness: dict, obligation_id: str) -> dict:
    validator = validate_category_model if lens == "categorical" else validate_hott_model
    return validator(model, witness, {obligation_id})


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_default_regime_alias_needs_no_relation_endpoint_resolution(lens: str) -> None:
    case = _case(lens)
    case["task_semantics"].pop("regime")
    case["task_semantics"].pop("task_relations")
    case["task_semantics"].pop("lens_decisions")
    compiled = compile_task_relation(case, lens)
    assert compiled["task_contract"]["regime"] == case["task_semantics"]["pressure"]
    assert compiled["task_relations"] == []
    aliases = [node for node in compiled["semantic_nodes"] if node["node_kind"] in {"pressure", "regime"}]
    assert len({node["node_id"] for node in aliases}) == 2


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_declared_relations_still_reject_ambiguous_textual_anchors(lens: str) -> None:
    case = _case(lens)
    case["task_semantics"]["regime"] = case["task_semantics"]["pressure"]
    with pytest.raises(TaskRelationCompilerError, match="textually distinct"):
        compile_task_relation(case, lens)


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_task_translation_binds_every_anchor_and_returns_exact_handback(lens: str) -> None:
    case = _case(lens)
    artifact = forge_case_artifact(case, lens)

    result = validate_task_derived_artifact(case, artifact)
    translation = artifact["semantic_translation"]
    semantics = case["task_semantics"]
    assert result["status"] == "valid"
    assert artifact["formalization_scope"] == "task_derived_finite_semantic_translation"
    assert [row["statement"] for row in translation["primitive_bindings"]] == semantics["incumbent_primitives"]
    assert [row["statement"] for row in translation["invariant_bindings"]] == semantics["protected_invariants"]
    assert all(row["formal_member_id"] for row in translation["primitive_bindings"] + translation["invariant_bindings"])
    assert artifact["semantic_translation_receipt"]["status"] == "passed"
    assert artifact["task_derived_formal_delta"]["countermodel_result"] == (
        "noncommuting" if lens == "categorical" else "noncoherent"
    )
    handback = artifact["physics_handback"]
    assert handback["physical_carrier"] == PHYSICAL_CARRIER
    assert handback["regime"] == {"statement": REGIME, "origin": "declared"}
    assert [row["statement"] for row in handback["quantifiers"]] == QUANTIFIERS
    assert handback["falsifier"] == semantics["falsifier"]
    assert handback["correction"] == semantics["correction"]
    assert handback["untouched_physics_gates"] == UNTOUCHED_GATES
    assert handback["changed_next_physics_decision"]
    assert handback["handback_status"] == "decision_changed"
    assert handback["decision_comparison"]["substantive_change"] is True
    assert handback["incumbent_decision"] != handback["proposed_next_decision"]
    assert handback["investment_disposition"] == "non_investment_formal_evidence_only"
    assert not any(
        handback[field]
        for field in (
            "formal_elegance_authorized",
            "theorem_authorized",
            "yang_mills_authorized",
            "physics_value_authorized",
            "investment_authorized",
        )
    )
    assert {"continuum", "theorem", "mass_gap", "physics_value"}.issubset(handback["authority_nulls"])


@pytest.mark.parametrize("lens", ["categorical", "hott"])
@pytest.mark.parametrize("attack", ["carrier", "quantifier", "falsifier"])
def test_rehashing_cannot_repair_semantic_contract_swaps(lens: str, attack: str) -> None:
    case = _case(lens)
    artifact = forge_case_artifact(case, lens)
    contract = artifact["semantic_translation"]["task_contract"]
    if attack == "carrier":
        contract["physical_carrier"] = "foreign carrier"
    elif attack == "quantifier":
        contract["quantifier_bindings"][0]["statement"] = "There exists one convenient observable."
    else:
        contract["falsifier"] = "A decorative non-test."

    with pytest.raises(FormalReasoningError) as caught:
        validate_task_derived_artifact(case, _reseal(artifact))
    assert caught.value.reason_code == "task_semantic_translation_invalid"


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_mechanically_valid_parallel_route_swap_fails_semantic_replay(lens: str) -> None:
    case = _case(lens)
    artifact = forge_case_artifact(case, lens)
    old = artifact["negative_witness"]
    swapped = build_negative_witness(
        model=artifact["model"],
        validator_id=(
            "finite-category-countermodel.v1" if lens == "categorical"
            else "finite-hott-countermodel.v1"
        ),
        witness_kind=old["witness_kind"], step_namespace=old["step_namespace"],
        prefix=old["diagram_id"].removesuffix(".diagram"),
        source_id=old["source_id"], target_id=old["target_id"],
        left_path_ids=old["right_path_ids"], right_path_ids=old["left_path_ids"],
        left_composite_id=old["right_composite_id"],
        right_composite_id=old["left_composite_id"],
    )
    replay = _core_validate(lens, artifact["model"], swapped, case["obligation_id"])
    assert replay["result"] in {"noncommuting", "noncoherent"}
    artifact["negative_witness"] = swapped
    artifact["countermodel_output_digest"] = canonical_digest(replay)

    with pytest.raises(FormalReasoningError) as caught:
        validate_task_derived_artifact(case, _reseal(artifact))
    assert caught.value.reason_code == "task_semantic_translation_invalid"


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_valid_but_semantically_unbound_isomorphic_fixture_fails(lens: str) -> None:
    case = _case(lens)
    artifact = forge_case_artifact(case, lens)
    build = build_category_model_and_witness if lens == "categorical" else build_hott_model_and_witness
    model, witness = build(f"irrelevant-isomorph.{lens}", case["obligation_id"])
    replay = _core_validate(lens, model, witness, case["obligation_id"])
    assert replay["result"] in {"noncommuting", "noncoherent"}
    artifact["model"], artifact["negative_witness"] = model, witness
    artifact["countermodel_output_digest"] = canonical_digest(replay)

    with pytest.raises(FormalReasoningError, match="task relation binding") as caught:
        validate_task_derived_artifact(case, _reseal(artifact))
    assert caught.value.reason_code == "task_semantic_translation_invalid"


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_carrier_change_derives_a_new_model_and_witness_identity(lens: str) -> None:
    first = forge_case_artifact(_case(lens), lens)
    second_case = _case(lens, physical_carrier="sector-resolved gauge-invariant observable algebra")
    second = forge_case_artifact(second_case, lens)

    assert first["semantic_translation"]["formal_projection"]["semantic_prefix"] != second["semantic_translation"]["formal_projection"]["semantic_prefix"]
    assert first["task_derived_model_identity"] != second["task_derived_model_identity"]
    assert validate_task_derived_artifact(second_case, second)["status"] == "valid"


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_nonphysics_control_retains_theory_delta_without_physics_decision(lens: str) -> None:
    case = _case(lens, physical_carrier=None)
    artifact = forge_case_artifact(case, lens)
    assert validate_task_derived_artifact(case, artifact)["status"] == "valid"
    assert artifact["physics_handback"]["physical_carrier"] is None
    assert artifact["physics_handback"]["changed_next_physics_decision"] is None
    assert artifact["physics_handback"]["changed_next_theory_decision"]
    assert artifact["physics_handback"]["handback_status"] == "quarantined_non_physics"
    assert artifact["physics_handback"]["route_control_disposition"] == "quarantine_non_investment"
    assert artifact["task_derived_formal_delta"]["formal_carrier"] == case["task_semantics"]["pressure"]


@pytest.mark.parametrize("field", ["incumbent_primitives", "protected_invariants"])
def test_incomplete_or_duplicate_task_semantics_fail_typed(field: str) -> None:
    case = _case("categorical")
    case["task_semantics"][field] = ["duplicate", "duplicate"]
    with pytest.raises(FormalReasoningError) as caught:
        forge_case_artifact(case, "categorical")
    assert caught.value.reason_code == "task_semantic_translation_invalid"


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_generic_builders_and_artifacts_remain_explicitly_internal(lens: str) -> None:
    build = build_category_model_and_witness if lens == "categorical" else build_hott_model_and_witness
    model, witness = build(f"generic-compat.{lens}", "obligation.generic")
    assert _core_validate(lens, model, witness, "obligation.generic")["result"] in {"noncommuting", "noncoherent"}
    assert not {"semantic_translation", "task_derived_formal_delta", "physics_handback"}.intersection(model)

    case = {
        "case_id": f"generic-compat.{lens}", "target_id": "generic-compat",
        "obligation_id": "obligation.generic", "preferred_lens": lens,
    }
    artifact = forge_case_artifact(case, lens)
    assert artifact["skill_version"] == "3.0.0-generic-internal"
    assert "Generic internal finite-structure plumbing" in artifact["authority_boundary"]
    assert "semantic_translation" not in artifact


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_isomorphic_presentations_share_one_canonical_replay_identity(lens: str) -> None:
    case = _case(lens)
    canonical = forge_case_artifact(case, lens)
    relabelled = forge_case_artifact(case, lens, presentation_id="independent-display-names")

    assert validate_task_derived_artifact(case, canonical)["status"] == "valid"
    assert validate_task_derived_artifact(case, relabelled)["status"] == "valid"
    assert canonical["task_derived_model_identity"]["model_digest"] != relabelled[
        "task_derived_model_identity"
    ]["model_digest"]
    assert canonical["task_derived_model_identity"]["canonical_isomorphism_digest"] == relabelled[
        "task_derived_model_identity"
    ]["canonical_isomorphism_digest"]
    assert canonical["semantic_translation"]["compilation_digest"] == relabelled[
        "semantic_translation"
    ]["compilation_digest"]


def test_lenses_compile_distinct_relation_native_consequences() -> None:
    category = forge_case_artifact(_case("categorical"), "categorical")
    hott = forge_case_artifact(_case("hott"), "hott")

    category_consequence = category["task_derived_formal_delta"]["lens_consequences"][0]
    hott_consequence = hott["task_derived_formal_delta"]["lens_consequences"][0]
    assert category_consequence["consequence_kind"] == "ordered_composite_comparison"
    assert category_consequence["decision_dimension"] == "route_order"
    assert hott_consequence["consequence_kind"] == "equivalence_coherence_cell"
    assert hott_consequence["decision_dimension"] == "coherence_obligation"
    assert category_consequence["statement"] != hott_consequence["statement"]


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_wrong_lens_relation_quarantines_instead_of_manufacturing_relevance(lens: str) -> None:
    case = _case(lens)
    relation = case["task_semantics"]["task_relations"][0]
    relation["relation_kind"] = (
        "equivalence_coherence" if lens == "categorical" else "noncommuting_composition"
    )
    artifact = forge_case_artifact(case, lens)

    assert validate_task_derived_artifact(case, artifact)["status"] == "valid"
    assert artifact["semantic_translation"]["lens_selection"]["status"] == "inapplicable"
    assert artifact["task_derived_formal_delta"]["lens_consequences"] == []
    assert artifact["physics_handback"]["handback_status"] == "quarantined_lens_inapplicable"
    assert artifact["physics_handback"]["proposed_next_decision"] is None
    assert artifact["physics_handback"]["investment_authorized"] is False


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_unchanged_incumbent_decision_is_typed_noninvestment_quarantine(lens: str) -> None:
    case = _case(lens)
    incumbent = case["task_semantics"]["incumbent_decision"]
    candidate = case["task_semantics"]["lens_decisions"][lens]
    candidate.update(
        {
            "decision_kind": incumbent["decision_kind"],
            "action": incumbent["action"],
            "target_burden_id": incumbent["target_burden_id"],
        }
    )
    artifact = forge_case_artifact(case, lens)
    handback = artifact["physics_handback"]

    assert handback["handback_status"] == "quarantined_no_decision_change"
    assert handback["decision_comparison"]["substantive_change"] is False
    assert handback["changed_next_physics_decision"] is None
    assert handback["route_control_disposition"] == "quarantine_non_investment"
    assert handback["investment_authorized"] is False


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_missing_incumbent_decision_is_typed_noninvestment_quarantine(lens: str) -> None:
    case = _case(lens)
    del case["task_semantics"]["incumbent_decision"]
    artifact = forge_case_artifact(case, lens)

    assert artifact["physics_handback"]["handback_status"] == "quarantined_missing_decision_declaration"
    assert artifact["physics_handback"]["incumbent_decision"] is None
    assert artifact["physics_handback"]["proposed_next_decision"] is None


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_normalized_cross_task_model_swap_rejects_foreign_meaning_binding(lens: str) -> None:
    first_case = _case(lens)
    second_case = _case(lens, physical_carrier="sector-resolved observable carrier")
    first = forge_case_artifact(first_case, lens)
    second = forge_case_artifact(second_case, lens)
    assert first["task_derived_model_identity"]["canonical_isomorphism_digest"] == second[
        "task_derived_model_identity"
    ]["canonical_isomorphism_digest"]

    first["model"] = copy.deepcopy(second["model"])
    first["negative_witness"] = copy.deepcopy(second["negative_witness"])
    with pytest.raises(FormalReasoningError, match="task relation binding") as caught:
        validate_task_derived_artifact(first_case, _reseal(first))
    assert caught.value.reason_code == "task_semantic_translation_invalid"


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_compilation_schema_is_closed_against_rehashed_extra_authority(lens: str) -> None:
    compilation = compile_task_relation(_case(lens), lens)
    compilation["formal_elegance_proves_physics"] = True
    compilation["compilation_digest"] = canonical_digest(
        {key: value for key, value in compilation.items() if key != "compilation_digest"}
    )
    with pytest.raises(ContractError):
        validate_instance(compilation, "task_relation_compilation.schema.json")


@pytest.mark.parametrize("lens", ["categorical", "hott"])
def test_relation_endpoint_must_name_declared_task_meaning(lens: str) -> None:
    case = _case(lens)
    case["task_semantics"]["task_relations"][0]["target_anchor"] = "foreign elegant abstraction"
    with pytest.raises(FormalReasoningError, match="declared semantic anchors") as caught:
        forge_case_artifact(case, lens)
    assert caught.value.reason_code == "task_semantic_translation_invalid"
