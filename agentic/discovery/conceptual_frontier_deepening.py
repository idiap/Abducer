# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Compose provider-plural conceptual search into next-cycle theory requests.

This module is deliberately a composition layer, not another discovery
implementation.  It reopens an execution produced by
``aggressive_provider_search``, projects every retained complete conceptual
record into the input contract of ``route_neutral_semantic_evaluation``, and
binds the resulting plural calibration outcome to nonauthoritative future
requests.  Literature reopening, process isolation, family reconstruction,
semantic judging, central formal reasoning, proof, and descendant experiments
remain owned by their existing runtimes.

The central authority invariant is temporal: this packet cannot change the
current theory, proof state, schedule, or experiment state.  Its only mandatory
consumer is a later central reflection.  Optional Category Theory, HoTT,
proof-v3, and N-to-N+8 experiment records are descriptors for future children,
not executions or preferences.
"""

from __future__ import annotations

import copy
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .aggressive_provider_search import (
    validate_aggressive_provider_search_execution,
)
from .contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    validate_identifier,
    validate_payload,
)
from .route_neutral_semantic_evaluation import (
    CONTROL_KINDS,
    run_route_neutral_semantic_evaluation,
    seal_semantic_evidence,
    validate_route_neutral_semantic_evaluation,
)


SCHEMA_VERSION = "1.0.0"
SCHEMA_NAME = "conceptual_frontier_deepening_v1.schema.json"
COMPOSITION_ORDER = (
    "governed_aggressive_provider_search_reopened",
    "all_retained_complete_candidates_projected_route_neutrally",
    "caller_supplied_separately_authored_five_control_set_bound",
    "three_or_more_separately_configured_judges_preregistered",
    "route_neutral_semantic_evaluation_completed",
    "plural_noncompensatory_outcome_preserved",
    "later_reflection_and_optional_future_children_described",
)
CENTRAL_ABSTRACTION_MODES = frozenset({"category_theory", "hott"})
AUTHORITY_NULLS = {
    "canonical_write_authority": None,
    "current_theory_effect_authority": None,
    "conceptual_winner_authority": None,
    "family_label_authority": None,
    "proof_authority": None,
    "experiment_authority": None,
    "scientific_truth_authority": None,
    "semantic_independence_authority": None,
    "category_hott_value_authority": None,
}
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_CALLER_SELECTION_KEYS = frozenset(
    {"winner", "winners", "preferred", "preference", "family_label", "family_labels"}
)


class ConceptualFrontierDeepeningError(ContractError):
    """Stable fail-closed error at the native composition boundary."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"conceptual_frontier_deepening[{reason_code}]: {message}")


def _fail(reason_code: str, message: str) -> None:
    raise ConceptualFrontierDeepeningError(reason_code, message)


def _seal(core: Mapping[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(dict(core))
    return {**row, "content_digest": canonical_digest(row)}


def _verify_seal(value: Mapping[str, Any], label: str) -> None:
    expected = canonical_digest(
        {key: child for key, child in value.items() if key != "content_digest"}
    )
    if value.get("content_digest") != expected:
        _fail("digest_mismatch", f"{label} content digest does not replay")


def _reject_caller_selection(value: Any, *, path: str = "$") -> None:
    """Keep caller-authored labels and winners outside the composition input."""

    if isinstance(value, Mapping):
        for raw_key, child in value.items():
            key = str(raw_key).strip().lower()
            if key in _CALLER_SELECTION_KEYS:
                _fail(
                    "caller_authored_selection_forbidden",
                    f"caller input contains {key} at {path}",
                )
            _reject_caller_selection(child, path=f"{path}.{raw_key}")
    elif isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        for index, child in enumerate(value):
            _reject_caller_selection(child, path=f"{path}[{index}]")


def _route_neutral_content(matured_output: Mapping[str, Any]) -> dict[str, Any]:
    """Return the complete conceptual record without process identities.

    Aggressive search already establishes which fields constitute complete
    conceptual content.  Two conceptual classification keys contain the word
    ``status``; they are losslessly renamed so the route-neutral evaluator does
    not confuse semantic state with workflow status.  No value is removed.
    """

    matured = matured_output["matured_invention"]
    complete = {
        "statement": copy.deepcopy(matured["statement"]),
        "semantic_core": copy.deepcopy(matured["semantic_core"]),
        "deep_reflection": copy.deepcopy(matured["deep_reflection"]),
        "risk_reward": copy.deepcopy(matured["risk_reward"]),
        "physics_handback": copy.deepcopy(matured["physics_handback"]),
        "typed_family_evidence": copy.deepcopy(
            matured_output["typed_family_evidence"]
        ),
    }

    def neutralize(value: Any) -> Any:
        if isinstance(value, Mapping):
            result: dict[str, Any] = {}
            for raw_key, child in value.items():
                key = str(raw_key)
                neutral_key = (
                    "conceptual_classification"
                    if key == "status"
                    else "conceptual_mutation_classification"
                    if key == "mutation_status"
                    else key
                )
                if neutral_key in result:
                    _fail(
                        "route_neutral_projection_collision",
                        f"conceptual key {neutral_key} is ambiguous",
                    )
                result[neutral_key] = neutralize(child)
            return result
        if isinstance(value, Sequence) and not isinstance(
            value, (str, bytes, bytearray)
        ):
            return [neutralize(child) for child in value]
        return copy.deepcopy(value)

    return neutralize(complete)


def _judge_pointers(
    judge_configurations: Sequence[Mapping[str, Any]],
) -> list[str]:
    """Extract evidence pointers; the evaluator owns full config validation."""

    pointers: set[str] = set()
    try:
        for configuration in judge_configurations:
            for rule in configuration["dimension_rules"].values():
                pointers.update(str(pointer) for pointer in rule["pointers"])
    except (AttributeError, KeyError, TypeError) as exc:
        raise ConceptualFrontierDeepeningError(
            "judge_configuration_unreadable",
            "judge configurations do not expose dimension-rule pointers",
        ) from exc
    if not pointers:
        _fail("judge_configuration_unreadable", "judge pointers are empty")
    return sorted(pointers)


def _candidate_projection(
    search: Mapping[str, Any],
    judge_configurations: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Project every retained alias exactly once without redoing family logic."""

    retained = list(search["retention"]["retained_candidate_aliases"])
    binding_by_alias = {
        row["candidate_alias"]: row
        for row in search["family_private_binding"]["bindings"]
    }
    output_by_invention = {
        row["matured_invention"]["invention_id"]: row
        for row in search["matured_outputs"]
    }
    if len(binding_by_alias) != len(search["family_private_binding"]["bindings"]):
        _fail("retained_branch_binding_invalid", "candidate aliases are not unique")
    if len(output_by_invention) != len(search["matured_outputs"]):
        _fail("retained_branch_binding_invalid", "matured inventions are not unique")

    pointers = _judge_pointers(judge_configurations)
    candidates: list[dict[str, Any]] = []
    source_bindings: list[dict[str, Any]] = []
    for alias in sorted(retained):
        binding = binding_by_alias.get(alias)
        if binding is None:
            _fail(
                "retained_branch_missing",
                f"retained candidate {alias} has no private source binding",
            )
        matured_output = output_by_invention.get(binding["invention_id"])
        if (
            matured_output is None
            or matured_output["matured_invention"]["branch_id"]
            != binding["branch_id"]
        ):
            _fail(
                "retained_branch_missing",
                f"retained candidate {alias} lacks its complete matured branch",
            )
        content = _route_neutral_content(matured_output)
        source_digests = {
            pointer: canonical_digest(
                {
                    "aggressive_search_execution_digest": search["content_digest"],
                    "candidate_alias": alias,
                    "source_complete_content_digest": binding[
                        "complete_content_digest"
                    ],
                    "content_pointer": pointer,
                }
            )
            for pointer in pointers
        }
        try:
            evidence = seal_semantic_evidence(
                content,
                evidence_id=stable_identifier(
                    "frontier-semantic-evidence",
                    alias,
                    search["content_digest"],
                ),
                pointer_source_digests=source_digests,
            )
        except Exception as exc:
            raise ConceptualFrontierDeepeningError(
                "candidate_evidence_projection_failed",
                f"retained candidate {alias} cannot satisfy judge evidence pointers",
            ) from exc
        candidates.append(
            {
                "candidate_id": alias,
                "content": content,
                "sealed_evidence": evidence,
            }
        )
        source_bindings.append(
            _seal(
                {
                    "candidate_id": alias,
                    "source_invention_id": binding["invention_id"],
                    "source_branch_id": binding["branch_id"],
                    "source_complete_content_digest": binding[
                        "complete_content_digest"
                    ],
                    "route_neutral_content_digest": canonical_digest(content),
                    "evidence_digest": evidence["evidence_digest"],
                }
            )
        )
    if [row["candidate_id"] for row in candidates] != sorted(retained):
        _fail(
            "retained_branch_missing",
            "route-neutral projection is not a bijection over retained branches",
        )
    receipt = _seal(
        {
            "policy": "all_retained_complete_content_lossless_route_neutral_projection_v1",
            "retained_candidate_aliases": sorted(retained),
            "converted_candidate_ids": [
                row["candidate_id"] for row in candidates
            ],
            "all_retained_branches_converted": True,
            "typed_family_evidence_preserved": True,
            "caller_authored_winners": False,
            "caller_authored_family_labels": False,
            "route_or_status_metadata_in_content": False,
        }
    )
    return candidates, source_bindings, receipt


def build_route_neutral_frontier_candidates(
    *,
    aggressive_search_execution: Mapping[str, Any],
    known_taxonomy: Mapping[str, Any],
    judge_configurations: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Expose the deterministic projection so callers can author controls.

    In particular, a caller can construct the required copied-status control
    from an exact candidate row before invoking the semantic panel.  The main
    runtime recomputes this projection and never trusts a caller-supplied copy.
    """

    try:
        search = validate_aggressive_provider_search_execution(
            aggressive_search_execution,
            known_taxonomy=known_taxonomy,
        )
    except Exception as exc:
        raise ConceptualFrontierDeepeningError(
            "aggressive_search_invalid",
            "governed aggressive provider search did not reopen",
        ) from exc
    candidates, _bindings, _receipt = _candidate_projection(
        search, judge_configurations
    )
    return candidates


def _validate_control_authorship(
    *,
    controls: Sequence[Mapping[str, Any]],
    control_set_authorship: Mapping[str, Any],
    search: Mapping[str, Any],
    judge_configurations: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    expected_fields = {
        "authorship_id",
        "author_id",
        "author_configuration_digest",
        "authored_before_semantic_evaluation",
        "composition_runtime_authored_controls",
    }
    if set(control_set_authorship) != expected_fields:
        _fail(
            "control_authorship_invalid",
            "control-set authorship descriptor has an open or incomplete shape",
        )
    validate_identifier(
        str(control_set_authorship["authorship_id"]), "authorship_id"
    )
    author_id = str(control_set_authorship["author_id"])
    validate_identifier(author_id, "control author_id")
    if not _DIGEST.fullmatch(
        str(control_set_authorship["author_configuration_digest"])
    ):
        _fail(
            "control_authorship_invalid",
            "control author configuration digest is invalid",
        )
    if (
        control_set_authorship["authored_before_semantic_evaluation"] is not True
        or control_set_authorship["composition_runtime_authored_controls"] is not False
    ):
        _fail(
            "control_authorship_invalid",
            "controls must be caller supplied before evaluation",
        )
    if len(controls) != len(CONTROL_KINDS):
        _fail("control_set_incomplete", "the exact five-control set is required")
    try:
        control_ids = [str(row["control_id"]) for row in controls]
        control_kinds = [str(row["control_kind"]) for row in controls]
    except (KeyError, TypeError) as exc:
        raise ConceptualFrontierDeepeningError(
            "control_set_incomplete", "control rows lack identities or kinds"
        ) from exc
    if (
        len(set(control_ids)) != len(control_ids)
        or sorted(control_kinds) != sorted(CONTROL_KINDS)
    ):
        _fail(
            "control_set_incomplete",
            "one sham, decorative, irrelevant, capable-rival, and copied-status control is required",
        )
    provider_markers = {
        str(value)
        for slot in search["request"]["slot_schedule"]
        for value in slot["provider_authority"].values()
        if value is not None
    }
    judge_ids = {
        str(configuration.get("config_id", ""))
        for configuration in judge_configurations
    }
    if author_id in provider_markers or author_id in judge_ids:
        _fail(
            "control_authorship_not_separate",
            "control author overlaps a candidate provider or judge configuration",
        )
    control_set_digest = canonical_digest(
        sorted((copy.deepcopy(dict(row)) for row in controls), key=lambda row: row["control_id"])
    )
    return _seal(
        {
            **copy.deepcopy(dict(control_set_authorship)),
            "control_set_digest": control_set_digest,
            "control_ids": sorted(control_ids),
            "control_kinds": sorted(control_kinds),
            "separate_from_candidate_provider_and_judge_identities": True,
            "independence_authority": None,
        }
    )


def _semantic_input_bindings(
    candidates: Sequence[Mapping[str, Any]],
    controls: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for raw in candidates:
        rows.append(
            {
                "source_id": raw["candidate_id"],
                "source_kind": "candidate",
                "control_kind": None,
                "copied_candidate_id": None,
                "content_digest": canonical_digest(raw["content"]),
                "evidence_digest": raw["sealed_evidence"]["evidence_digest"],
            }
        )
    for raw in controls:
        rows.append(
            {
                "source_id": raw["control_id"],
                "source_kind": "control",
                "control_kind": raw["control_kind"],
                "copied_candidate_id": raw["copied_candidate_id"],
                "content_digest": canonical_digest(raw["content"]),
                "evidence_digest": raw["sealed_evidence"]["evidence_digest"],
            }
        )
    return sorted(rows, key=lambda row: row["source_id"])


def _future_requests(
    *,
    causal_binding: Mapping[str, Any],
    plural_candidate_ids: Sequence[str],
    central_abstraction_modes: Sequence[str],
    request_proof_v3: bool,
    request_descendant_experiment: bool,
) -> dict[str, Any]:
    modes = sorted(set(central_abstraction_modes))
    if len(modes) != len(central_abstraction_modes) or (
        set(modes) - CENTRAL_ABSTRACTION_MODES
    ):
        _fail(
            "central_abstraction_mode_invalid",
            "central abstraction modes must be unique Category Theory and/or HoTT",
        )
    source_state = causal_binding["source_state_version"]
    next_state = source_state + 1
    candidates = sorted(plural_candidate_ids)
    later_reflection = _seal(
        {
            "request_kind": "later_central_reflection_request_descriptor",
            "source_state_version": source_state,
            "earliest_effect_state_version": next_state,
            "candidate_ids": candidates,
            "source_causal_binding_digest": causal_binding["content_digest"],
            "plural_set_must_remain_visible": True,
            "nonauthoritative_future_request": True,
            "direct_current_effect": False,
        }
    )
    central = [
        _seal(
            {
                "request_kind": "central_formal_route_future_request_descriptor",
                "formal_language": mode,
                "source_state_version": source_state,
                "earliest_consumer_state_version": next_state,
                "candidate_ids": candidates,
                "source_causal_binding_digest": causal_binding["content_digest"],
                "physics_return_required": True,
                "formal_vocabulary_preference_bonus": False,
                "nonauthoritative_future_request": True,
                "direct_current_effect": False,
            }
        )
        for mode in modes
    ]
    proof = (
        [
            _seal(
                {
                    "request_kind": "proof_v3_future_child_request_descriptor",
                    "canonical_route": "proof_v3",
                    "source_state_version": source_state,
                    "eligible_only_after_reflection_state_version": next_state,
                    "candidate_ids": candidates,
                    "source_causal_binding_digest": causal_binding[
                        "content_digest"
                    ],
                    "nonauthoritative_future_request": True,
                    "direct_current_effect": False,
                }
            )
        ]
        if request_proof_v3
        else []
    )
    descendants = (
        [
            _seal(
                {
                    "request_kind": "descendant_experiment_n_to_n_plus_8_future_child_request_descriptor",
                    "canonical_route": "world_v3_descendant_n_to_n_plus_8",
                    "source_state_version": source_state,
                    "future_parent_theory_generation": next_state,
                    "required_terminal_reflection_generation": next_state + 8,
                    "candidate_ids": candidates,
                    "source_causal_binding_digest": causal_binding[
                        "content_digest"
                    ],
                    "launch_only_after_future_theory_commit": True,
                    "nonauthoritative_future_request": True,
                    "direct_current_effect": False,
                }
            )
        ]
        if request_descendant_experiment
        else []
    )
    return _seal(
        {
            "request_options": {
                "central_abstraction_modes": modes,
                "proof_v3_requested": request_proof_v3,
                "descendant_experiment_requested": request_descendant_experiment,
            },
            "later_reflection_request": later_reflection,
            "central_abstraction_requests": central,
            "proof_v3_requests": proof,
            "descendant_experiment_requests": descendants,
        }
    )


def run_conceptual_frontier_deepening(
    *,
    aggressive_search_execution: Mapping[str, Any],
    known_taxonomy: Mapping[str, Any],
    controls: Sequence[Mapping[str, Any]],
    control_set_authorship: Mapping[str, Any],
    judge_configurations: Sequence[Mapping[str, Any]],
    semantic_run_root: Path | str,
    counterbalance_entropy: str,
    central_abstraction_modes: Sequence[str] = (),
    request_proof_v3: bool = False,
    request_descendant_experiment: bool = False,
    caller_authored_winners: Sequence[str] | None = None,
    caller_authored_family_labels: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Run the native composition without granting a same-cycle effect.

    The aggressive search execution is an immutable upstream result.  Callers
    needing to author a copied-status control should first use
    :func:`build_route_neutral_frontier_candidates`; this function recomputes
    that projection and rejects any missing retained branch.
    """

    if caller_authored_winners:
        _fail(
            "caller_authored_selection_forbidden",
            "the caller cannot provide winners",
        )
    if caller_authored_family_labels:
        _fail(
            "caller_authored_selection_forbidden",
            "the caller cannot provide family labels",
        )
    _reject_caller_selection(controls, path="$.controls")
    _reject_caller_selection(
        control_set_authorship, path="$.control_set_authorship"
    )
    _reject_caller_selection(
        judge_configurations, path="$.judge_configurations"
    )
    try:
        search = validate_aggressive_provider_search_execution(
            aggressive_search_execution,
            known_taxonomy=known_taxonomy,
        )
    except Exception as exc:
        raise ConceptualFrontierDeepeningError(
            "aggressive_search_invalid",
            "governed aggressive provider search did not reopen",
        ) from exc

    configurations = sorted(
        (copy.deepcopy(dict(row)) for row in judge_configurations),
        key=lambda row: str(row.get("config_id", "")),
    )
    candidates, candidate_source_bindings, conversion_receipt = (
        _candidate_projection(search, configurations)
    )
    control_rows = sorted(
        (copy.deepcopy(dict(row)) for row in controls),
        key=lambda row: str(row.get("control_id", "")),
    )
    authorship = _validate_control_authorship(
        controls=control_rows,
        control_set_authorship=control_set_authorship,
        search=search,
        judge_configurations=configurations,
    )
    semantic_inputs = _seal(
        {
            "candidate_rows": candidates,
            "candidate_source_bindings": candidate_source_bindings,
            "control_rows": control_rows,
            "control_set_authorship": authorship,
            "judge_configurations": configurations,
            "judge_configuration_digests": [
                canonical_digest(configuration)
                for configuration in configurations
            ],
            "conversion_receipt": conversion_receipt,
        }
    )
    evaluation = run_route_neutral_semantic_evaluation(
        study_id=stable_identifier(
            "conceptual-frontier-semantic-study",
            search["request"]["namespace"],
            semantic_inputs["content_digest"],
        ),
        run_root=semantic_run_root,
        candidates=candidates,
        controls=control_rows,
        judge_configurations=configurations,
        counterbalance_entropy=counterbalance_entropy,
    )
    if evaluation["evaluation_status"] == "NULL":
        failure_reason = evaluation["failure"]["reason_code"]
        reason = (
            "route_leakage"
            if failure_reason in {"route_label_leak", "source_identity_leak"}
            else "semantic_evaluator_null"
        )
        _fail(reason, f"route-neutral evaluator returned NULL: {failure_reason}")
    preference = evaluation["preference"]
    if (
        preference["status"] != "plural"
        or len(preference["candidate_ids"]) < 2
    ):
        _fail(
            "plural_outcome_required",
            "semantic evaluation did not preserve at least two candidates",
        )
    candidate_ids = {row["candidate_id"] for row in candidates}
    if not set(preference["candidate_ids"]).issubset(candidate_ids):
        _fail(
            "semantic_preference_unbound",
            "semantic outcome names a non-frontier candidate",
        )
    plural_outcome = _seal(
        {
            "status": "plural_internal_calibration_only",
            "candidate_ids": sorted(preference["candidate_ids"]),
            "basis": preference["basis"],
            "semantic_evaluation_digest": evaluation["content_digest"],
            "winner_authority": None,
            "family_label_authority": None,
        }
    )
    request = search["request"]
    literature = request["literature_authority"]
    causal_binding = _seal(
        {
            "namespace": copy.deepcopy(request["namespace"]),
            "source_state_version": request["namespace"]["state_version"],
            "aggressive_search_request_digest": search["request_digest"],
            "aggressive_search_execution_digest": search["content_digest"],
            "aggressive_search_causal_order_digest": canonical_digest(
                search["causal_order"]
            ),
            "literature_authority_digest": literature["content_digest"],
            "literature_bundle_digest": literature["literature_bundle_digest"],
            "literature_projection_digest": literature[
                "literature_projection_digest"
            ],
            "literature_input_digest": literature["literature_input_digest"],
            "governed_present_use_at": literature["governed_present_use_at"],
            "semantic_inputs_digest": semantic_inputs["content_digest"],
            "semantic_evaluation_digest": evaluation["content_digest"],
            "plural_outcome_digest": plural_outcome["content_digest"],
            "composition_order": list(COMPOSITION_ORDER),
        }
    )
    future_requests = _future_requests(
        causal_binding=causal_binding,
        plural_candidate_ids=plural_outcome["candidate_ids"],
        central_abstraction_modes=central_abstraction_modes,
        request_proof_v3=request_proof_v3,
        request_descendant_experiment=request_descendant_experiment,
    )
    source_state = causal_binding["source_state_version"]
    effect_policy = {
        "same_cycle_theory_effect": False,
        "same_cycle_proof_effect": False,
        "same_cycle_experiment_effect": False,
        "same_cycle_schedule_effect": False,
        "canonical_write_effect": False,
        "later_reflection_earliest_effect_state_version": source_state + 1,
        "proof_and_experiment_children_authoritative_now": False,
    }
    core = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "conceptual_frontier_deepening",
        "composition_id": stable_identifier(
            "conceptual-frontier-deepening",
            causal_binding["content_digest"],
            future_requests["content_digest"],
        ),
        "aggressive_search_execution": search,
        "aggressive_search_execution_digest": search["content_digest"],
        "semantic_inputs": semantic_inputs,
        "semantic_evaluation": evaluation,
        "plural_outcome": plural_outcome,
        "causal_order_currentness_binding": causal_binding,
        "future_requests": future_requests,
        "effect_policy": effect_policy,
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
    }
    packet = _seal(core)
    validate_conceptual_frontier_deepening(
        packet,
        known_taxonomy=known_taxonomy,
    )
    return packet


def validate_conceptual_frontier_deepening(
    packet: Mapping[str, Any],
    *,
    known_taxonomy: Mapping[str, Any],
    reopen_semantic_receipts: bool = True,
) -> dict[str, Any]:
    """Replay every composition binding while delegating domain logic."""

    value = copy.deepcopy(dict(packet))
    try:
        validate_payload(value, SCHEMA_NAME)
    except ContractError as exc:
        raise ConceptualFrontierDeepeningError(
            "schema_invalid", "composition packet violates its exact schema"
        ) from exc
    _verify_seal(value, "conceptual frontier composition")
    if value["authority_nulls"] != AUTHORITY_NULLS:
        _fail("authority_overclaim", "mandatory authority nulls changed")
    try:
        search = validate_aggressive_provider_search_execution(
            value["aggressive_search_execution"],
            known_taxonomy=known_taxonomy,
        )
    except Exception as exc:
        raise ConceptualFrontierDeepeningError(
            "aggressive_search_invalid",
            "embedded aggressive search no longer reopens",
        ) from exc
    if value["aggressive_search_execution_digest"] != search["content_digest"]:
        _fail("causal_binding_mismatch", "aggressive execution digest changed")

    semantic_inputs = value["semantic_inputs"]
    configurations = semantic_inputs["judge_configurations"]
    expected_candidates, expected_sources, expected_receipt = (
        _candidate_projection(search, configurations)
    )
    if (
        semantic_inputs["candidate_rows"] != expected_candidates
        or semantic_inputs["candidate_source_bindings"] != expected_sources
        or semantic_inputs["conversion_receipt"] != expected_receipt
    ):
        _fail(
            "retained_candidate_conversion_mismatch",
            "retained complete branches are missing or their projection changed",
        )
    expected_authorship = _validate_control_authorship(
        controls=semantic_inputs["control_rows"],
        control_set_authorship={
            key: semantic_inputs["control_set_authorship"][key]
            for key in (
                "authorship_id",
                "author_id",
                "author_configuration_digest",
                "authored_before_semantic_evaluation",
                "composition_runtime_authored_controls",
            )
        },
        search=search,
        judge_configurations=configurations,
    )
    if semantic_inputs["control_set_authorship"] != expected_authorship:
        _fail("control_authorship_invalid", "control-set authorship changed")
    if semantic_inputs["judge_configuration_digests"] != [
        canonical_digest(configuration) for configuration in configurations
    ]:
        _fail("judge_configuration_binding_mismatch", "judge configs changed")
    expected_inputs = _seal(
        {
            key: copy.deepcopy(semantic_inputs[key])
            for key in (
                "candidate_rows",
                "candidate_source_bindings",
                "control_rows",
                "control_set_authorship",
                "judge_configurations",
                "judge_configuration_digests",
                "conversion_receipt",
            )
        }
    )
    if semantic_inputs != expected_inputs:
        _fail("semantic_input_binding_mismatch", "semantic input seal changed")

    evaluation = value["semantic_evaluation"]
    try:
        validate_route_neutral_semantic_evaluation(
            evaluation,
            reopen_receipts=reopen_semantic_receipts,
        )
    except Exception as exc:
        raise ConceptualFrontierDeepeningError(
            "semantic_evaluation_invalid",
            "embedded route-neutral evaluation no longer reopens",
        ) from exc
    if evaluation["evaluation_status"] == "NULL":
        _fail(
            "semantic_evaluator_null",
            "NULL semantic evaluation cannot become a preference",
        )
    expected_source_bindings = _semantic_input_bindings(
        semantic_inputs["candidate_rows"],
        semantic_inputs["control_rows"],
    )
    if (
        evaluation["input_commitment"]["source_bindings"]
        != expected_source_bindings
        or evaluation["input_commitment"]["judge_config_bindings"]
        != [
            {
                "config_id": configuration["config_id"],
                "config_digest": canonical_digest(configuration),
                "perspective_digest": canonical_digest(
                    configuration["perspective"]
                ),
            }
            for configuration in configurations
        ]
    ):
        _fail(
            "semantic_input_binding_mismatch",
            "semantic evaluator inputs differ from composition inputs",
        )
    preference = evaluation["preference"]
    if (
        preference["status"] != "plural"
        or len(preference["candidate_ids"]) < 2
    ):
        _fail("plural_outcome_required", "semantic outcome is not plural")
    candidate_ids = {
        row["candidate_id"] for row in semantic_inputs["candidate_rows"]
    }
    if not set(preference["candidate_ids"]).issubset(candidate_ids):
        _fail("semantic_preference_unbound", "plural outcome crossed candidates")
    expected_plural = _seal(
        {
            "status": "plural_internal_calibration_only",
            "candidate_ids": sorted(preference["candidate_ids"]),
            "basis": preference["basis"],
            "semantic_evaluation_digest": evaluation["content_digest"],
            "winner_authority": None,
            "family_label_authority": None,
        }
    )
    if value["plural_outcome"] != expected_plural:
        _fail("plural_outcome_binding_mismatch", "plural outcome changed")

    request = search["request"]
    literature = request["literature_authority"]
    expected_causal = _seal(
        {
            "namespace": copy.deepcopy(request["namespace"]),
            "source_state_version": request["namespace"]["state_version"],
            "aggressive_search_request_digest": search["request_digest"],
            "aggressive_search_execution_digest": search["content_digest"],
            "aggressive_search_causal_order_digest": canonical_digest(
                search["causal_order"]
            ),
            "literature_authority_digest": literature["content_digest"],
            "literature_bundle_digest": literature["literature_bundle_digest"],
            "literature_projection_digest": literature[
                "literature_projection_digest"
            ],
            "literature_input_digest": literature["literature_input_digest"],
            "governed_present_use_at": literature["governed_present_use_at"],
            "semantic_inputs_digest": semantic_inputs["content_digest"],
            "semantic_evaluation_digest": evaluation["content_digest"],
            "plural_outcome_digest": expected_plural["content_digest"],
            "composition_order": list(COMPOSITION_ORDER),
        }
    )
    if value["causal_order_currentness_binding"] != expected_causal:
        _fail(
            "causal_binding_mismatch",
            "literature, order, currentness, or semantic causality changed",
        )
    options = value["future_requests"]["request_options"]
    expected_future = _future_requests(
        causal_binding=expected_causal,
        plural_candidate_ids=expected_plural["candidate_ids"],
        central_abstraction_modes=options["central_abstraction_modes"],
        request_proof_v3=options["proof_v3_requested"],
        request_descendant_experiment=options[
            "descendant_experiment_requested"
        ],
    )
    if value["future_requests"] != expected_future:
        _fail("future_request_binding_mismatch", "future descriptors changed")
    source_state = request["namespace"]["state_version"]
    expected_effects = {
        "same_cycle_theory_effect": False,
        "same_cycle_proof_effect": False,
        "same_cycle_experiment_effect": False,
        "same_cycle_schedule_effect": False,
        "canonical_write_effect": False,
        "later_reflection_earliest_effect_state_version": source_state + 1,
        "proof_and_experiment_children_authoritative_now": False,
    }
    if value["effect_policy"] != expected_effects:
        _fail(
            "same_cycle_effect_forbidden",
            "theory, proof, experiment, schedule, or write effect became current",
        )
    expected_id = stable_identifier(
        "conceptual-frontier-deepening",
        expected_causal["content_digest"],
        expected_future["content_digest"],
    )
    if value["composition_id"] != expected_id:
        _fail("composition_identity_mismatch", "composition identity changed")
    return value


__all__ = [
    "AUTHORITY_NULLS",
    "COMPOSITION_ORDER",
    "ConceptualFrontierDeepeningError",
    "build_route_neutral_frontier_candidates",
    "run_conceptual_frontier_deepening",
    "validate_conceptual_frontier_deepening",
]
