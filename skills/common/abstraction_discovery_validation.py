# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Referential contracts for category/HoTT forges and the Yang--Mills bridge.

Schema validation establishes shape.  This module establishes cross-reference
and evidence integrity: arrows and transports really compose, parallel paths
share endpoints, witness certificates bind executable evidence, current
literature receipts bind the pressure that selected the lens, auditor outputs
are exact rather than named handoffs, and any refinement signal is derived from
an executed five-arm evaluation.  Successful category/HoTT validation returns a
closed formal-lens execution receipt so downstream bridges can replay exact code,
literature, model, witness, evaluation, and handback identities.  That finite
internal receipt never grants theorem, continuum, investment, conceptual-value,
physics-value, production-evidence, or cognitive-independence authority.
"""

from __future__ import annotations

import copy
from typing import Any, Mapping, Sequence

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    validate_instance,
)
from skills.common.abstraction_parallel_evaluation import (
    SCORE_FIELDS,
    validate_abstraction_parallel_evaluation,
)
from skills.common.discovery_lens_heuristic import (
    build_categorical_pathway_heuristic,
    build_hott_pathway_heuristic,
)
from skills.common.abstraction_formal_reasoning import (
    FormalReasoningError,
    validate_category_model as validate_executable_category_model,
    validate_hott_model as validate_executable_hott_model,
    validate_physical_diagram as validate_executable_physical_diagram,
)
from skills.common.ym_abstraction_calibrations import (
    YMCalibrationError,
    validate_ym_calibration,
)
from skills.common.formal_dependency_authority import (
    FormalDependencyAuthorityError,
    _validate_formal_dependency_run_context,
)
from skills.common.theory_atlas_defect_compiler import (
    TheoryAtlasDefectError,
    validate_theory_atlas_defect_packet,
)


PLACEHOLDERS = {"unknown", "n/a", "na", "none", "todo", "tbd", "placeholder"}
PHYSICS_CARRIER_TERMS = {
    "gauge", "observable", "schwinger", "wilson", "hilbert", "hamiltonian",
    "lattice", "continuum", "correlation", "field", "renormalization", "measure", "algebra",
}
YM_CALIBRATION_CASE_IDS = (
    "finite_transfer_matrix",
    "finite_volume_gap_collapse",
    "hidden_gapless_direct_sum",
    "massive_gaussian",
    "massless_gaussian",
    "noncommuting_limit_order",
    "regulated_4d_lattice",
    "spatial_only_decay",
    "topological_theory",
)
YM_CALIBRATION_CASES = frozenset(YM_CALIBRATION_CASE_IDS)
YM_HANDOFFS = {
    "ym-freeze-clay-target", "ym-build-representation-calculus", "ym-build-observable-core",
    "ym-calibrate-restricted-models", "ym-define-relational-rigidity",
    "ym-prove-continuum-coherence", "ym-reconstruct-os-gap", "ym-audit-frontier",
    "physical-relevance-impact-auditor", "proof-same-domain-transfer-certifier",
}
YM_TARGET_CONTRACT = {
    "spacetime_dimension": 4,
    "pure_gauge": True,
    "gauge_group_scope": "every declared compact simple gauge group",
    "continuum_required": True,
    "mass_gap_required": True,
}
YM_TARGET_CONTRACT_REFS = frozenset(YM_TARGET_CONTRACT)
YM_QUANTIFIER_CONTRACT = {
    "coupling": {
        "value_domain": "renormalized coupling trajectories fixed by physical normalization",
        "statement": "Along every declared renormalized coupling trajectory with physical normalization held fixed.",
    },
    "cutoff": {
        "value_domain": "strictly positive ultraviolet regulators directed toward zero",
        "statement": "For every sufficiently small positive ultraviolet cutoff in the declared directed removal net.",
    },
    "distance": {
        "value_domain": "strictly positive physical Euclidean temporal separations",
        "statement": "For every declared strictly positive physical Euclidean temporal separation.",
    },
    "observable_class": {
        "value_domain": "the declared state-separating gauge-invariant observable core",
        "statement": "For every observable in the declared state-separating gauge-invariant core.",
    },
    "volume": {
        "value_domain": "finite regulated volumes directed toward the infinite-volume limit",
        "statement": "Uniformly over the declared finite regulated volumes before the infinite-volume limit.",
    },
}
YM_QUANTIFIER_KEYS = tuple(YM_QUANTIFIER_CONTRACT)
YM_STRUCTURE_CONTRACTS = {
    "four_dimensional_pure_yang_mills": {
        "kind": "fixed_target_commitment", "target_contract_refs": ("pure_gauge", "spacetime_dimension"),
        "quantifier_refs": ("coupling", "cutoff", "distance", "observable_class", "volume"), "claim_level": "C0", "obligation_kind": "theorem",
    },
    "compact_simple_gauge_group_scope": {
        "kind": "fixed_target_commitment", "target_contract_refs": ("gauge_group_scope",),
        "quantifier_refs": ("coupling", "observable_class"), "claim_level": "C0", "obligation_kind": "theorem",
    },
    "gauge_invariance": {
        "kind": "transport_invariant", "target_contract_refs": ("gauge_group_scope", "pure_gauge"),
        "quantifier_refs": ("coupling", "cutoff", "observable_class", "volume"), "claim_level": "C2", "obligation_kind": "both",
    },
    "observable_algebra": {
        "kind": "transport_invariant", "target_contract_refs": ("continuum_required",),
        "quantifier_refs": ("coupling", "cutoff", "distance", "observable_class", "volume"), "claim_level": "C2", "obligation_kind": "both",
    },
    "regulator_ledger": {
        "kind": "transport_invariant", "target_contract_refs": ("continuum_required",),
        "quantifier_refs": ("cutoff",), "claim_level": "C1", "obligation_kind": "theorem",
    },
    "volume_ledger": {
        "kind": "transport_invariant", "target_contract_refs": ("continuum_required",),
        "quantifier_refs": ("volume",), "claim_level": "C1", "obligation_kind": "theorem",
    },
    "coupling_trajectory": {
        "kind": "transport_invariant", "target_contract_refs": ("continuum_required",),
        "quantifier_refs": ("coupling",), "claim_level": "C1", "obligation_kind": "theorem",
    },
    "physical_normalization": {
        "kind": "transport_invariant", "target_contract_refs": ("mass_gap_required",),
        "quantifier_refs": ("coupling", "distance"), "claim_level": "C2", "obligation_kind": "both",
    },
    "locality": {
        "kind": "transport_invariant", "target_contract_refs": ("continuum_required",),
        "quantifier_refs": ("cutoff", "distance", "observable_class"), "claim_level": "C2", "obligation_kind": "both",
    },
    "reflection_positivity": {
        "kind": "transport_invariant", "target_contract_refs": ("continuum_required",),
        "quantifier_refs": ("coupling", "cutoff", "distance", "observable_class", "volume"), "claim_level": "C3", "obligation_kind": "both",
    },
    "theory_identity": {
        "kind": "transport_invariant", "target_contract_refs": ("continuum_required", "gauge_group_scope", "mass_gap_required", "pure_gauge", "spacetime_dimension"),
        "quantifier_refs": ("coupling", "cutoff", "distance", "observable_class", "volume"), "claim_level": "C3", "obligation_kind": "theorem",
    },
    "continuum_limit_order": {
        "kind": "transport_invariant", "target_contract_refs": ("continuum_required",),
        "quantifier_refs": ("coupling", "cutoff", "volume"), "claim_level": "C3", "obligation_kind": "theorem",
    },
    "os_reconstruction_burden": {
        "kind": "open_reconstruction_burden", "target_contract_refs": ("continuum_required", "mass_gap_required"),
        "quantifier_refs": ("coupling", "cutoff", "distance", "observable_class", "volume"), "claim_level": "C3", "obligation_kind": "both",
    },
    "positive_hamiltonian_gap_target": {
        "kind": "desired_consequence", "target_contract_refs": ("mass_gap_required",),
        "quantifier_refs": ("coupling", "distance", "observable_class", "volume"), "claim_level": "C3", "obligation_kind": "theorem",
    },
}
YM_STRUCTURE_IDS = tuple(YM_STRUCTURE_CONTRACTS)
YM_STRUCTURES = frozenset(YM_STRUCTURE_IDS)
YM_STRUCTURE_STATEMENTS = {
    "four_dimensional_pure_yang_mills": "Keep the bridge inside four-dimensional pure Yang--Mills without changing the target theory.",
    "compact_simple_gauge_group_scope": "Retain the declared quantification over every compact simple gauge group.",
    "gauge_invariance": "Transfer the declared gauge invariance through the finite representation bridge.",
    "observable_algebra": "Transfer the state-separating gauge-invariant observable algebra without quotienting physical distinctions.",
    "regulator_ledger": "Track every regulator and cutoff-removal comparison used by the bridge.",
    "volume_ledger": "Track finite-volume dependence before any infinite-volume conclusion is attempted.",
    "coupling_trajectory": "Keep the renormalized coupling trajectory explicit through every representation change.",
    "physical_normalization": "Preserve the declared physical normalization instead of defining the desired gap into the units.",
    "locality": "Return locality preservation as an explicit theorem burden at every representation step.",
    "reflection_positivity": "Return reflection-positivity preservation as a separate continuum-facing theorem burden.",
    "theory_identity": "Prove that source and target presentations denote the same target theory rather than analogous models.",
    "continuum_limit_order": "Record and justify the order of cutoff, volume, and coupling limits without silent interchange.",
    "os_reconstruction_burden": "Leave Osterwalder--Schrader reconstruction open until its hypotheses are proved on the continuum carrier.",
    "positive_hamiltonian_gap_target": "Keep a positive Hamiltonian spectral gap as the desired consequence, never as a preserved premise.",
}
YM_CHANGE_PREFIXES = ("representation.", "proof_obligation.")
YM_CHANGED_STRUCTURES = (
    "proof_obligation.continuum_preservation",
    "representation.regulator_comparison_topology",
)
YM_CHANGED_STRUCTURES_INVALID = "ym_changed_structures_invalid"
YM_CONTINUUM_AUTHORITY_REQUIRED = "ym_continuum_authority_required"
YM_EVIDENCE_INFERENCE_INVALID = "ym_evidence_inference_invalid"
YM_EVIDENCE_STATUS_MATRIX_INVALID = "ym_evidence_status_matrix_invalid"
YM_CARRIER_STATUS_DERIVATION_INVALID = "ym_carrier_status_derivation_invalid"
YM_CORRECTION_COVERAGE_INVALID = "ym_correction_coverage_invalid"
YM_EVIDENCE_MATRIX_VERSION = "1.0.0"
YM_AUTHORITY_SCOPE = "sealed_bridge_representation_only"
YM_LENS_STRUCTURE_MAP = {
    "categorical": (
        "gauge_invariance",
        "locality",
        "observable_algebra",
        "regulator_ledger",
        "theory_identity",
        "volume_ledger",
    ),
    "hott": (
        "continuum_limit_order",
        "coupling_trajectory",
        "physical_normalization",
        "reflection_positivity",
        "theory_identity",
    ),
}
YM_CALIBRATION_STRUCTURE_MAP = {
    "finite_transfer_matrix": (
        "gauge_invariance",
        "observable_algebra",
        "theory_identity",
    ),
    "finite_volume_gap_collapse": (
        "positive_hamiltonian_gap_target",
        "volume_ledger",
    ),
    "hidden_gapless_direct_sum": (
        "observable_algebra",
        "os_reconstruction_burden",
        "positive_hamiltonian_gap_target",
    ),
    "massive_gaussian": ("physical_normalization",),
    "massless_gaussian": ("positive_hamiltonian_gap_target",),
    "noncommuting_limit_order": (
        "continuum_limit_order",
        "coupling_trajectory",
        "os_reconstruction_burden",
        "volume_ledger",
    ),
    "regulated_4d_lattice": (
        "continuum_limit_order",
        "coupling_trajectory",
        "locality",
        "reflection_positivity",
        "regulator_ledger",
    ),
    "spatial_only_decay": (
        "locality",
        "os_reconstruction_burden",
        "reflection_positivity",
    ),
    "topological_theory": (
        "positive_hamiltonian_gap_target",
        "theory_identity",
    ),
}
YM_CORRECTION_STRUCTURE_MAP = {
    # Each correction challenges every obligation. This prevents a globally
    # complete test union from concealing a locally uncorrectable structure by
    # partitioning the tests across otherwise unrelated ledger rows.
    "ym.test.hidden-sector": YM_STRUCTURE_IDS,
    "ym.test.uniform-density": YM_STRUCTURE_IDS,
}
YM_TRANSFER_AUTHORITY_BOUNDARY = (
    "The certificate orders only this sealed finite bridge representation; categorical or HoTT "
    "equivalence is not physical equivalence and proves no continuum construction or mass gap."
)
YM_CERTIFICATE_AUDIT_STATUS = {
    "proved": "passed",
    "conditional": "conditional",
    "open": "open",
    "failed": "failed",
}


class AbstractionValidationError(ValueError):
    """Raised when an abstraction is shaped but not referentially operational."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "abstraction_validation_invalid",
    ) -> None:
        super().__init__(message)
        self.reason_code = reason_code


def _fail(
    message: str,
    *,
    reason_code: str = "abstraction_validation_invalid",
) -> None:
    raise AbstractionValidationError(message, reason_code=reason_code)


def _schema(payload: Mapping[str, Any], schema: str) -> None:
    try:
        validate_instance(dict(payload), schema)
    except ContractError as exc:
        _fail(str(exc))


def _substantive(value: Any, field: str, minimum: int = 12) -> str:
    text = " ".join(str(value or "").split())
    if len(text) < minimum or text.lower() in PLACEHOLDERS:
        _fail(f"{field} is missing or decorative")
    return text


def _normalized(value: str) -> str:
    return " ".join(value.lower().split())


def forge_subject_digest(payload: Mapping[str, Any]) -> str:
    """Digest the exact forge candidate consumed by all three auditors."""

    required_atlas_fields = (
        "theory_atlas_packet",
        "theory_atlas_validation_receipt",
        "theory_atlas_crosswalk",
    )
    missing_atlas_fields = [
        field for field in required_atlas_fields if field not in payload
    ]
    if missing_atlas_fields:
        _fail(
            "forge subject digest is missing required theory-atlas authority fields: "
            + ", ".join(missing_atlas_fields),
            reason_code="theory_atlas_binding_missing",
        )

    return canonical_digest(
        {
            key: copy.deepcopy(payload[key])
            for key in (
                "target_id", "domain_kind", "lens", "literature_basis", "source_pressure",
                "theory_atlas_packet", "theory_atlas_validation_receipt",
                "theory_atlas_crosswalk",
                "target_contract", "categorical_model", "hott_model", "failure_witness", "translation",
                "physics_handback", "dependency_authority",
            )
        }
    )


def ym_bridge_subject_digest(payload: Mapping[str, Any]) -> str:
    """Digest the exact physical bridge candidate consumed by its auditors."""

    return canonical_digest(
        {
            key: copy.deepcopy(payload[key])
            for key in (
                "target_id", "literature_basis", "upstream_packet_bindings", "lens", "target_contract",
                "continuum_authority",
                "representation_package", "physical_diagram", "carrier_translations",
                "same_domain_transfer", "failure_witness", "theorem_obligations",
                "correction_tests", "calibration_matrix",
                "physics_handback", "dependency_authority",
            )
        }
    )


def build_physics_handback(
    *,
    target_id: str,
    domain_kind: str,
    physical_carrier: str,
    burdens: Sequence[Mapping[str, Any]],
    correction_tests: Sequence[Mapping[str, Any]],
    failure_witness: Mapping[str, Any],
    target_contract: Mapping[str, Any] | None = None,
    preservation_transfer: Mapping[str, Any] | None = None,
    quantifier_contract: Mapping[str, Any] | None = None,
    evidence_registry: Sequence[Mapping[str, Any]] | None = None,
    carrier_translations: Sequence[Mapping[str, Any]] | None = None,
    continuum_authority: Mapping[str, Any] | None = None,
    theory_atlas_binding: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Bind abstraction language back to burdens, corrections, and failure.

    The handback is mandatory even when the domain is non-physics: in that
    case it records why no physical carrier applies.  It is deliberately an
    internal reflective-theory return and can never mint physics-value or
    investment authority.
    """

    burden_rows = [copy.deepcopy(dict(row)) for row in burdens]
    correction_rows = [copy.deepcopy(dict(row)) for row in correction_tests]
    core = {
        "handback_status": "returned_to_reflective_theory",
        "authority_class": "internal_finite_local_refinement_only",
        "target_id": target_id,
        "domain_kind": domain_kind,
        "physical_carrier": physical_carrier,
        "target_burden_ids": [str(row["obligation_id"]) for row in burden_rows],
        "target_burdens_digest": canonical_digest(burden_rows),
        "correction_test_ids": [str(row["test_id"]) for row in correction_rows],
        "correction_tests_digest": canonical_digest(correction_rows),
        "failure_witness_digest": canonical_digest(failure_witness),
        "failure_conditions": [
            str(failure_witness["exact_obstruction"]),
            *[str(item) for item in failure_witness["boundary_conditions"]],
        ],
        "physics_value_language_status": "internal_hypothesis_only_after_handback",
        "continuum_authority": None,
        "authority_distinct_physics_value_evidence_status": "unavailable",
        "authority_distinct_physics_value_evidence_ids": [],
        "physics_value_authorized": False,
        "investment_authorized": False,
        "next_route": "reflective-theory-synthesizer",
    }
    if theory_atlas_binding is not None:
        core["theory_atlas_binding"] = copy.deepcopy(dict(theory_atlas_binding))
    optional_ym_parts = (
        target_contract,
        preservation_transfer,
        quantifier_contract,
        evidence_registry,
        carrier_translations,
        continuum_authority,
    )
    if any(value is None for value in optional_ym_parts) and any(
        value is not None for value in optional_ym_parts
    ):
        _fail("YM physics handback contract, transfer, quantifiers, and evidence must be supplied together")
    if target_contract is not None and preservation_transfer is not None:
        contract = copy.deepcopy(dict(target_contract))
        transfer = copy.deepcopy(dict(preservation_transfer))
        quantifiers = copy.deepcopy(dict(quantifier_contract or {}))
        evidence = [copy.deepcopy(dict(row)) for row in evidence_registry or []]
        carriers = [
            copy.deepcopy(dict(row)) for row in carrier_translations or []
        ]
        continuum = copy.deepcopy(dict(continuum_authority or {}))
        if transfer["continuum_authority_digest"] != continuum.get(
            "content_digest"
        ):
            _fail(
                "YM physics handback continuum authority differs from its transfer binding"
            )
        carriers_by_structure: dict[str, list[str]] = {
            structure_id: [] for structure_id in YM_STRUCTURE_IDS
        }
        for carrier in carriers:
            for structure_id in carrier["preservation_structure_ids"]:
                carriers_by_structure[str(structure_id)].append(
                    str(carrier["abstract_entity_id"])
                )
        burden_by_structure = {
            str(row["preservation_structure_ids"][0]): row
            for row in burden_rows
        }
        burden_matrix = []
        for structure_row in transfer["structure_ledger"]:
            structure_id = str(structure_row["structure_id"])
            burden = burden_by_structure[structure_id]
            matrix_core = {
                "structure_id": structure_id,
                "obligation_id": str(burden["obligation_id"]),
                "status": str(structure_row["status"]),
                "carrier_translation_ids": sorted(
                    carriers_by_structure[structure_id]
                ),
                "target_contract_refs": copy.deepcopy(
                    structure_row["target_contract_refs"]
                ),
                "quantifier_refs": copy.deepcopy(
                    structure_row["quantifier_refs"]
                ),
                "evidence_refs": copy.deepcopy(structure_row["evidence_refs"]),
                "correction_test_ids": copy.deepcopy(
                    structure_row["correction_test_ids"]
                ),
                "continuum_authority_digest": transfer[
                    "continuum_authority_digest"
                ],
            }
            burden_matrix.append(
                {**matrix_core, "content_digest": canonical_digest(matrix_core)}
            )
        core.update(
            {
                "target_contract": contract,
                "target_contract_digest": canonical_digest(contract),
                "quantifier_contract": quantifiers,
                "quantifier_contract_digest": canonical_digest(quantifiers),
                "preservation_evidence_registry": evidence,
                "preservation_evidence_registry_digest": canonical_digest(evidence),
                "carrier_translations": carriers,
                "carrier_translation_digest": canonical_digest(carriers),
                "physics_burden_matrix": burden_matrix,
                "physics_burden_matrix_digest": canonical_digest(burden_matrix),
                "preservation_structure_ledger": copy.deepcopy(transfer["structure_ledger"]),
                "preservation_structure_ledger_digest": transfer["structure_ledger_digest"],
                "changed_structures": copy.deepcopy(transfer["changed_structures"]),
                "transfer_certificate_status": transfer["certificate_status"],
                "transfer_certificate_status_basis": copy.deepcopy(transfer["certificate_status_basis"]),
                "continuum_authority": continuum,
                "continuum_authority_digest": transfer["continuum_authority_digest"],
                "evidence_matrix_version": transfer["evidence_matrix_version"],
                "preservation_transfer_digest": canonical_digest(transfer),
            }
        )
        core["preservation_binding_digest"] = canonical_digest(
            {
                "target_contract_digest": core["target_contract_digest"],
                "quantifier_contract_digest": core["quantifier_contract_digest"],
                "preservation_evidence_registry_digest": core[
                    "preservation_evidence_registry_digest"
                ],
                "preservation_structure_ledger_digest": core["preservation_structure_ledger_digest"],
                "target_burdens_digest": core["target_burdens_digest"],
                "correction_tests_digest": core["correction_tests_digest"],
                "carrier_translation_digest": core["carrier_translation_digest"],
                "physics_burden_matrix_digest": core[
                    "physics_burden_matrix_digest"
                ],
                "continuum_authority_digest": core["continuum_authority_digest"],
                "preservation_transfer_digest": core["preservation_transfer_digest"],
            }
        )
    return {**core, "content_digest": canonical_digest(core)}


def _validate_physics_handback(
    payload: Mapping[str, Any],
    *,
    physical_carrier: str,
    burdens: Sequence[Mapping[str, Any]],
    correction_tests: Sequence[Mapping[str, Any]],
    target_contract: Mapping[str, Any] | None = None,
    preservation_transfer: Mapping[str, Any] | None = None,
    quantifier_contract: Mapping[str, Any] | None = None,
    evidence_registry: Sequence[Mapping[str, Any]] | None = None,
    carrier_translations: Sequence[Mapping[str, Any]] | None = None,
    continuum_authority: Mapping[str, Any] | None = None,
    theory_atlas_binding: Mapping[str, Any] | None = None,
) -> None:
    expected = build_physics_handback(
        target_id=str(payload["target_id"]),
        domain_kind=str(payload.get("domain_kind", "physics")),
        physical_carrier=physical_carrier,
        burdens=burdens,
        correction_tests=correction_tests,
        failure_witness=payload["failure_witness"],
        target_contract=target_contract,
        preservation_transfer=preservation_transfer,
        quantifier_contract=quantifier_contract,
        evidence_registry=evidence_registry,
        carrier_translations=carrier_translations,
        continuum_authority=continuum_authority,
        theory_atlas_binding=theory_atlas_binding,
    )
    if payload["physics_handback"] != expected:
        _fail("physics burden/correction/failure handback is not exact")


def literature_pressure_digest(
    *, source_mapping_ids: Sequence[str], pressure_payload: Any
) -> str:
    """Bind source-to-theory mappings to the exact pressure used downstream."""

    return canonical_digest(
        {"source_mapping_ids": sorted(source_mapping_ids), "pressure_payload": pressure_payload}
    )


def _theory_atlas_binding(
    atlas_packet: Mapping[str, Any],
    validation_receipt: Mapping[str, Any],
    crosswalk: Mapping[str, Any],
) -> dict[str, Any]:
    """Project the exact finite pre-forge authority into every physics handback."""

    return {
        "packet_id": str(atlas_packet["packet_id"]),
        "packet_digest": str(atlas_packet["content_digest"]),
        "validation_receipt_id": str(validation_receipt["validation_receipt_id"]),
        "validation_receipt_digest": str(validation_receipt["content_digest"]),
        "crosswalk_digest": str(crosswalk["content_digest"]),
        "authority_class": "finite_pre_forge_structural_pressure_only",
        "automatic_promotion_authorized": False,
    }


def _forge_model_identifier_set(packet: Mapping[str, Any]) -> set[str]:
    """Return the complete declared finite model namespace for crosswalk closure."""

    if packet["lens"] == "categorical":
        model = packet["categorical_model"]
        identifiers = {
            *(str(row["object_id"]) for row in model["objects"]),
            *(str(row["morphism_id"]) for row in model["morphisms"]),
            *(str(row["composition_id"]) for row in model["compositions"]),
            str(model["universal_property"]["construction_id"]),
            str(model["new_consequence"]["consequence_id"]),
        }
    else:
        model = packet["hott_model"]
        identifiers = {
            *(str(row["type_id"]) for row in model["types"]),
            *(str(row["map_id"]) for row in model["maps"]),
            *(str(row["path_id"]) for row in model["paths"]),
            *(str(row["fiber_id"]) for row in model["path_fibers"]),
            *(str(row["predicate_id"]) for row in model["transported_predicates"]),
            *(str(row["equivalence_id"]) for row in model["equivalences"]),
            *(str(row["transport_id"]) for row in model["transports"]),
            *(str(row["composition_id"]) for row in model["transport_compositions"]),
            *(str(row["cell_id"]) for row in model["coherence_cells"]),
            str(model["new_consequence"]["consequence_id"]),
        }
    return identifiers


def _failure_witness_identifier_set(witness: Mapping[str, Any]) -> set[str]:
    """Return every named component of the independently replayed failure witness."""

    return {
        str(witness["diagram_id"]),
        str(witness["source_id"]),
        str(witness["target_id"]),
        str(witness["left_composite_id"]),
        str(witness["right_composite_id"]),
        str(witness["certificate"]["certificate_id"]),
        *(str(value) for value in witness["left_path_ids"]),
        *(str(value) for value in witness["right_path_ids"]),
        *(str(row["evidence_id"]) for row in witness["evidence"]),
    }


def _validate_theory_atlas_source(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Replay the preserved atlas and its exact bridge into this finite forge.

    The crosswalk is deliberately surjective onto every declared namespace:
    each atlas defect/candidate/return square and each forge pressure, model,
    witness, and translation identifier must occur.  This turns the atlas into
    inspectable structural pressure without allowing it to validate the forge.
    """

    atlas = packet["theory_atlas_packet"]
    supplied_receipt = packet["theory_atlas_validation_receipt"]
    try:
        derived_receipt = validate_theory_atlas_defect_packet(atlas)
    except TheoryAtlasDefectError as exc:
        _fail(f"theory atlas source is invalid: {exc}", reason_code=exc.reason_code)
    if supplied_receipt != derived_receipt:
        _fail("theory atlas validation receipt is not replay-derived")
    if atlas["target_id"] != packet["target_id"]:
        _fail("theory atlas target differs from the forge target")

    crosswalk = packet["theory_atlas_crosswalk"]
    if crosswalk["content_digest"] != canonical_digest(
        crosswalk, exclude_keys=("content_digest",)
    ):
        _fail("theory atlas crosswalk has a stale digest")
    expected_header = {
        "atlas_packet_id": atlas["packet_id"],
        "atlas_packet_digest": atlas["content_digest"],
        "atlas_validation_receipt_id": derived_receipt["validation_receipt_id"],
        "atlas_validation_receipt_digest": derived_receipt["content_digest"],
        "target_id": packet["target_id"],
        "lens": packet["lens"],
        "source_pressure_digest": canonical_digest(packet["source_pressure"]),
        "authority_class": "finite_pre_forge_structural_pressure_only",
        "automatic_promotion_authorized": False,
    }
    if any(crosswalk[field] != value for field, value in expected_header.items()):
        _fail("theory atlas crosswalk header does not bind the exact forge")

    defects = {str(row["defect_id"]): row for row in atlas["defects"]}
    candidates = {
        str(row["candidate_id"]): row for row in atlas["completion_candidates"]
    }
    return_squares = {
        str(row["square_id"]): row for row in atlas["return_squares"]
    }
    rows = crosswalk["rows"]
    row_defects = [str(row["defect_id"]) for row in rows]
    row_candidates = [str(row["completion_candidate_id"]) for row in rows]
    if len(row_defects) != len(set(row_defects)) or set(row_defects) != set(defects):
        _fail("theory atlas crosswalk does not cover every defect exactly once")
    if len(row_candidates) != len(set(row_candidates)) or set(row_candidates) != set(candidates):
        _fail("theory atlas crosswalk does not cover every completion candidate exactly once")

    pressure_ids = {
        str(queue_id)
        for frontier in packet["source_pressure"]["frontier_rows"]
        for queue_id in frontier["queue_ids"]
    }
    model_ids = _forge_model_identifier_set(packet)
    witness_ids = _failure_witness_identifier_set(packet["failure_witness"])
    obligation_ids = {
        str(row["obligation_id"])
        for row in packet["translation"]["observable_or_theorem_obligations"]
    }
    observed = {
        "return_square_ids": set(),
        "source_pressure_queue_ids": set(),
        "forge_model_refs": set(),
        "failure_witness_refs": set(),
        "translation_obligation_ids": set(),
    }
    allowed = {
        "return_square_ids": set(return_squares),
        "source_pressure_queue_ids": pressure_ids,
        "forge_model_refs": model_ids,
        "failure_witness_refs": witness_ids,
        "translation_obligation_ids": obligation_ids,
    }
    for row in rows:
        defect_id = str(row["defect_id"])
        candidate_id = str(row["completion_candidate_id"])
        candidate = candidates[candidate_id]
        if candidate["defect_id"] != defect_id:
            _fail("theory atlas crosswalk splices a completion across defects")
        square_refs = {str(value) for value in row["return_square_ids"]}
        if any(return_squares[value]["completion_candidate_id"] != candidate_id for value in square_refs):
            _fail("theory atlas crosswalk splices a return square across completions")
        for field in observed:
            values = {str(value) for value in row[field]}
            if not values or not values <= allowed[field]:
                _fail(f"theory atlas crosswalk has unknown or empty {field}")
            if field == "return_square_ids" and observed[field] & values:
                _fail("theory atlas return square is assigned more than once")
            observed[field].update(values)
    for field, expected in allowed.items():
        if observed[field] != expected:
            _fail(f"theory atlas crosswalk is not exactly closed over {field}")
    return _theory_atlas_binding(atlas, derived_receipt, crosswalk)


def _validate_literature_basis(
    basis: Mapping[str, Any], *, target_id: str, pressure_payload: Any
) -> None:
    if basis["target_id"] != target_id:
        _fail("literature basis target differs from the active target")
    snapshot_receipt = basis["snapshot_validator_receipt"]
    if (
        snapshot_receipt["target_id"] != target_id
        or snapshot_receipt["validated_digest"] != basis["snapshot_digest"]
        or snapshot_receipt["status"] != "passed"
    ):
        _fail("literature snapshot validator receipt is not target/digest bound")
    assimilation_receipt = basis["assimilation_validator_receipt"]
    if (
        assimilation_receipt["target_id"] != target_id
        or assimilation_receipt["validated_assimilation_digest"] != basis["assimilation_digest"]
        or assimilation_receipt["validated_snapshot_digest"] != basis["snapshot_digest"]
        or basis["assimilation_input_snapshot_digest"] != basis["snapshot_digest"]
    ):
        _fail("literature assimilation receipt is not bound to the selected snapshot")
    expected_pressure = literature_pressure_digest(
        source_mapping_ids=basis["source_mapping_ids"], pressure_payload=pressure_payload
    )
    if basis["pressure_mapping_digest"] != expected_pressure:
        _fail("literature source mappings do not bind the exact abstraction pressure")


def _validate_literature_evaluation_binding(
    basis: Mapping[str, Any], report: Mapping[str, Any]
) -> None:
    """Bind the compact forge projection to the report's validated artifacts.

    ``literature_basis`` deliberately avoids copying a potentially large
    snapshot and assimilation packet into every forge.  A digest projection is
    safe only if its metadata, validator receipt, and *complete ordered mapping
    identity* are replayed against the full artifacts already carried by the
    five-arm evaluation.  Otherwise a caller could relabel the latest search or
    replace its mapping set, recompute the local pressure digest, and retain a
    superficially valid current-literature claim.
    """

    snapshot = report["literature_snapshot"]
    assimilation = report["assimilation_packet"]
    resolution = assimilation["resolution"]
    expected_projection = {
        "target_id": snapshot["target_id"],
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_digest": snapshot["content_digest"],
        "search_completed_at": snapshot["search_completed_at"],
        "coverage_cutoff": snapshot["coverage_cutoff"],
        "freshness_status": resolution["freshness_status"],
        "target_match": resolution["target_match"],
        "active_investment_gate": resolution["active_investment_gate"],
        "assimilation_packet_id": assimilation["packet_id"],
        "assimilation_digest": assimilation["content_digest"],
        "assimilation_input_snapshot_digest": assimilation["selected_snapshot"][
            "content_digest"
        ],
        "hypothesis_rebase_status": assimilation["hypothesis_rebase_status"],
        "source_mapping_ids": [
            row["mapping_id"] for row in assimilation["theory_mappings"]
        ],
    }
    for field, expected in expected_projection.items():
        if basis[field] != expected:
            _fail(
                f"literature basis {field} is not the exact executed evaluation projection"
            )

    projected_snapshot_receipt = basis["snapshot_validator_receipt"]
    matching_receipts = [
        row
        for row in snapshot["validator_receipts"]
        if row["receipt_id"] == projected_snapshot_receipt["receipt_id"]
    ]
    if len(matching_receipts) != 1:
        _fail("literature basis cites no unique executed snapshot validator receipt")
    executed_snapshot_receipt = matching_receipts[0]
    expected_snapshot_receipt = {
        "validator_id": executed_snapshot_receipt["validator_id"],
        "receipt_id": executed_snapshot_receipt["receipt_id"],
        "target_id": snapshot["target_id"],
        "validated_digest": executed_snapshot_receipt["validated_digest"],
        "status": executed_snapshot_receipt["status"],
    }
    if projected_snapshot_receipt != expected_snapshot_receipt:
        _fail("literature basis snapshot receipt differs from the executed receipt")

    expected_assimilation_receipt = {
        "validator_id": "literature-assimilation-validator.v1",
        "receipt_id": stable_identifier(
            "assimilation-validator", assimilation["content_digest"]
        ),
        "target_id": assimilation["target_id"],
        "validated_assimilation_digest": assimilation["content_digest"],
        "validated_snapshot_digest": snapshot["content_digest"],
        "status": "passed",
    }
    if basis["assimilation_validator_receipt"] != expected_assimilation_receipt:
        _fail("literature basis assimilation receipt is not replay-derived")


def _authority_entry_digest(authority: Mapping[str, Any], path: str) -> str:
    """Return one exact executable digest from the validated dependency closure."""

    matches = [
        row["content_digest"]
        for row in authority["entries"]
        if row["path"] == path
    ]
    if len(matches) != 1:
        _fail(f"formal dependency authority lacks one exact entry for {path}")
    return str(matches[0])


def _build_formal_lens_execution_receipt(
    *,
    packet: Mapping[str, Any],
    packet_digest: str,
    dependency_authority: Mapping[str, Any],
    parallel_evaluation: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind one successful finite lens replay without expanding its authority.

    The receipt is intentionally emitted only after the forge model, full
    evaluation artifact, and complete current-literature projection have all
    crossed their validators.  It records that exact finite execution, but its
    explicit nulls prevent a downstream consumer from reading local replay as
    production evidence, cognitive independence, a theorem, or physics value.
    """

    evaluation_authority = parallel_evaluation["dependency_authority"]
    if (
        evaluation_authority["authority_version"]
        != dependency_authority["authority_version"]
        or evaluation_authority["content_digest"]
        != dependency_authority["content_digest"]
    ):
        _fail("forge and evaluation dependency authorities differ")
    lens = str(packet["lens"])
    model = (
        packet["categorical_model"]
        if lens == "categorical"
        else packet["hott_model"]
    )
    literature = packet["literature_basis"]
    atlas_binding = _theory_atlas_binding(
        packet["theory_atlas_packet"],
        packet["theory_atlas_validation_receipt"],
        packet["theory_atlas_crosswalk"],
    )
    receipt_id = stable_identifier(
        "formal-lens-execution",
        packet["packet_id"],
        packet_digest,
        parallel_evaluation["content_digest"],
        dependency_authority["content_digest"],
    )
    core = {
        "authority_version": "2.0.0",
        "receipt_id": receipt_id,
        "validator_id": (
            "finite-categorical-forge-validator.v5"
            if lens == "categorical"
            else "finite-hott-forge-validator.v5"
        ),
        "execution_mode": "in_process_deterministic_validation",
        "status": "passed",
        "authority_scope": "sealed_finite_formal_lens_execution_only",
        "target_id": packet["target_id"],
        "packet_id": packet["packet_id"],
        "packet_schema_version": packet["schema_version"],
        "packet_digest": packet_digest,
        "lens": lens,
        "model_digest": canonical_digest(model),
        "witness_certificate_digest": canonical_digest(
            packet["failure_witness"]["certificate"]
        ),
        "physics_handback_digest": packet["physics_handback"]["content_digest"],
        "theory_atlas_packet_id": atlas_binding["packet_id"],
        "theory_atlas_packet_digest": atlas_binding["packet_digest"],
        "theory_atlas_validation_receipt_id": atlas_binding[
            "validation_receipt_id"
        ],
        "theory_atlas_validation_receipt_digest": atlas_binding[
            "validation_receipt_digest"
        ],
        "theory_atlas_crosswalk_digest": atlas_binding["crosswalk_digest"],
        "theory_atlas_authority_class": atlas_binding["authority_class"],
        "theory_atlas_automatic_promotion_authorized": False,
        "dependency_authority_version": dependency_authority[
            "authority_version"
        ],
        "dependency_authority_digest": dependency_authority["content_digest"],
        "validator_module_digest": _authority_entry_digest(
            dependency_authority,
            "skills/common/abstraction_discovery_validation.py",
        ),
        "formal_reasoning_module_digest": _authority_entry_digest(
            dependency_authority,
            "skills/common/abstraction_formal_reasoning.py",
        ),
        "evaluation_runtime_module_digest": _authority_entry_digest(
            dependency_authority,
            "skills/common/abstraction_parallel_evaluation.py",
        ),
        "evaluation_schema_version": parallel_evaluation["schema_version"],
        "evaluation_id": parallel_evaluation["evaluation_id"],
        "evaluation_digest": parallel_evaluation["content_digest"],
        "literature_snapshot_id": literature["snapshot_id"],
        "literature_snapshot_digest": literature["snapshot_digest"],
        "assimilation_packet_id": literature["assimilation_packet_id"],
        "assimilation_digest": literature["assimilation_digest"],
        "literature_projection_digest": canonical_digest(literature),
        "production_evidence_status": "not_attested",
        "authority_distinct_evaluation_status": "unavailable",
        "theorem_authorized": False,
        "continuum_authorized": False,
        "physics_value_authorized": False,
        "investment_authorized": False,
        "cognitive_independence_authorized": False,
    }
    receipt = {**core, "content_digest": canonical_digest(core)}
    _schema(receipt, "formal_lens_execution_receipt.schema.json")
    return receipt


def _validate_audit_envelope(
    receipt: Mapping[str, Any], *, expected_skill: str, target_id: str, subject_digest: str
) -> Mapping[str, Any]:
    if receipt["skill_id"] != expected_skill:
        _fail(f"expected {expected_skill} receipt")
    if receipt["target_id"] != target_id or receipt["subject_digest"] != subject_digest:
        _fail(f"{expected_skill} receipt target or subject digest mismatch")
    output_digest = canonical_digest(receipt["output"])
    if receipt["output_digest"] != output_digest:
        _fail(f"{expected_skill} output digest mismatch")
    validator = receipt["validator_receipt"]
    if validator["validated_output_digest"] != output_digest or validator["status"] != "passed":
        _fail(f"{expected_skill} validator did not bind the exact output")
    return receipt["output"]


def _validate_auditors(
    payload: Mapping[str, Any], *, subject_digest: str, physics: bool,
    ym_bridge: bool = False,
) -> None:
    audits = payload["audit_receipts"]
    if audits["subject_digest"] != subject_digest:
        _fail("auditor subject digest differs from the candidate")
    target_id = payload["target_id"]
    fit = _validate_audit_envelope(
        audits["fit_gap"], expected_skill="abstraction-fit-gap-auditor",
        target_id=target_id, subject_digest=subject_digest,
    )
    required_fit = {"verdict", "incumbent_gap", "candidate_gain", "remaining_gap", "failure_case"}
    if set(fit) != required_fit:
        _fail("fit-gap output is not the exact typed auditor result")
    same = _validate_audit_envelope(
        audits["same_domain"], expected_skill="proof-same-domain-transfer-certifier",
        target_id=target_id, subject_digest=subject_digest,
    )
    required_same = (
        {
            "source_domain", "target_domain", "structure_ledger_digest",
            "changed_structures", "certificate_status", "certificate_status_basis",
            "quantifier_contract_digest", "evidence_registry_digest",
            "carrier_translation_digest", "continuum_authority_digest",
            "evidence_matrix_version", "preservation_transfer_digest", "failure_case",
        }
        if ym_bridge
        else {"source_domain", "target_domain", "preserved_structures", "changed_structures", "certificate_status", "failure_case"}
    )
    if set(same) != required_same:
        _fail("same-domain output is not the exact typed certifier result")
    if _normalized(same["source_domain"]) != _normalized(same["target_domain"]):
        _fail("same-domain certifier output changes the target domain")
    physical = audits["physical_relevance"]
    if physics:
        if physical is None:
            _fail("physics packet lacks a physical-relevance auditor receipt")
        output = _validate_audit_envelope(
            physical, expected_skill="physical-relevance-impact-auditor",
            target_id=target_id, subject_digest=subject_digest,
        )
        required = {
            "physical_carrier", "target_gate", "obligation_ids",
            "essential_relevance", "physical_reward", "investment_decision", "failure_case",
        }
        required.add("correction_test_ids" if ym_bridge else "correction_test_id")
        if set(output) != required:
            _fail("physical-relevance output is not the exact typed auditor result")
    elif physical is not None:
        _fail("nonphysics packet cannot invent a physical-relevance receipt")


def _repeatability_projection(diagnostics: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    return {
        field: copy.deepcopy(dict(diagnostics[field]))
        for field in SCORE_FIELDS
    }


def _validate_ablation(
    ablation: Mapping[str, Any], decision: str, condition_arm: str,
    report: Mapping[str, Any], *, target_id: str, snapshot_digest: str, assimilation_digest: str,
) -> dict[str, Any]:
    try:
        validate_abstraction_parallel_evaluation(report)
    except Exception as exc:
        _fail(f"parallel evaluation is invalid: {exc}")
    summary = ablation["evaluation_report"]
    aggregates = {row["arm"]: row for row in report["aggregates"]}
    condition = aggregates[condition_arm]
    baseline = aggregates["no_abstraction"]
    paired = condition["paired_differences_vs_no_abstraction"]
    expected_summary = {
        "schema_version": report["schema_version"], "evaluation_id": report["evaluation_id"],
        "content_digest": report["content_digest"], "target_id": report["target_id"],
        "case_suite_id": report["case_suite_id"],
        "literature_snapshot_digest": report["literature_snapshot_digest"],
        "assimilation_digest": report["assimilation_digest"], "condition_arm": condition_arm,
        "baseline_arm": "no_abstraction",
        "repetitions_completed": paired["n_matched_repetitions"],
        "minimum_required_matched_repetitions": paired[
            "minimum_required_matched_repetitions"
        ],
        "calibration_status": paired["status"],
        "runtime_portfolio_digest": report["runtime_portfolio_digest"],
        "evaluator_receipt_id": report["evaluator_evidence"]["receipt_id"],
        "partial_failure_status": "siblings_preserved",
        "task_cluster_count": report["task_clustered_reporting"]["task_count"],
        "population_inference_authorized": False,
        "external_human_status": report["evaluator_evidence"]["external_human"]["status"],
    }
    if summary != expected_summary:
        _fail("value ablation summary is not bound to the exact executed report")
    if target_id != report["target_id"] or snapshot_digest != report["literature_snapshot_digest"] or assimilation_digest != report["assimilation_digest"]:
        _fail("value ablation report uses a different target or literature basis")
    if ablation["with_abstraction"] != condition["descriptive_mean_scorecard"] or ablation["without_abstraction"] != baseline["descriptive_mean_scorecard"]:
        _fail("value ablation scorecards differ from executed aggregate means")
    diagnostics = paired["diagnostics"]
    repeatability = (
        None if diagnostics is None else _repeatability_projection(diagnostics)
    )
    if ablation["paired_repeatability_diagnostics"] != repeatability:
        _fail("value ablation repeatability diagnostics differ from executed paired differences")
    net = (
        None
        if diagnostics is None
        else round(
            sum(float(diagnostics[field]["descriptive_mean"]) for field in SCORE_FIELDS),
            6,
        )
    )
    if ablation["net_new_value"] != net:
        _fail("net_new_value differs from the exact matched-pair diagnostic")
    signal = (
        paired["status"] == "sufficient_internal_calibration"
        and condition["internal_refinement_eligible"] is True
    )
    if ablation["frozen_suite_refinement_signal"] is not signal:
        _fail("frozen-suite refinement signal differs from task-clustered diagnostics")
    invest_decisions = {"invest", "invest_high_physics_reward", "invest_restricted_model_only"}
    if decision in invest_decisions:
        _fail("finite local abstraction evaluation never authorizes investment")
    if (
        decision in {"refine", "refine_bridge"}
        and paired["status"] != "sufficient_internal_calibration"
    ):
        _fail("refinement requires at least five exact matched repetitions")
    if decision in {"refine", "refine_bridge"} and (net is None or net <= 0):
        _fail("refinement requires positive executed abstraction value")
    if decision in {"refine", "refine_bridge"} and condition["internal_refinement_eligible"] is not True:
        _fail("internal calibration does not support refinement for this condition")
    return {
        "net_new_value": net,
        "condition_arm": condition_arm,
        "repetitions": paired["n_matched_repetitions"],
        "calibration_status": paired["status"],
    }


def validate_forge_packet(
    payload: Mapping[str, Any], *, expected_lens: str | None = None,
    parallel_evaluation: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate one generic categorical or HoTT forge packet transitively."""

    packet = copy.deepcopy(dict(payload))
    _schema(packet, "abstraction_forge_packet.schema.json")
    try:
        dependency_context = _validate_formal_dependency_run_context(
            packet["dependency_authority"]
        )
        dependency_authority = dependency_context.snapshot()
    except FormalDependencyAuthorityError as exc:
        _fail(str(exc))
    lens = packet["lens"]
    if expected_lens and lens != expected_lens:
        _fail(f"expected {expected_lens} lens, got {lens}")
    rows = packet["source_pressure"]["frontier_rows"]
    computed = build_categorical_pathway_heuristic(rows) if lens == "categorical" else build_hott_pathway_heuristic(rows)
    projection_fields = ("lens_id", "recommended", "score", "threshold", "active_criteria", "active_anti_triggers")
    expected_projection = {field: computed[field] for field in projection_fields}
    if packet["source_pressure"]["heuristic"] != expected_projection or computed["recommended"] is not True:
        _fail("stored shared-lens heuristic is stale or does not recommend this route")
    _validate_literature_basis(
        packet["literature_basis"], target_id=packet["target_id"], pressure_payload=rows
    )
    atlas_binding = _validate_theory_atlas_source(packet)
    translation = packet["translation"]
    obligation_ids = {
        row["obligation_id"]
        for row in translation["observable_or_theorem_obligations"]
    }
    try:
        if lens == "categorical":
            validate_executable_category_model(
                packet["categorical_model"],
                packet["failure_witness"],
                obligation_ids,
                _dependency_context=dependency_context,
            )
        else:
            validate_executable_hott_model(
                packet["hott_model"],
                packet["failure_witness"],
                obligation_ids,
                _dependency_context=dependency_context,
            )
    except FormalReasoningError as exc:
        _fail(str(exc), reason_code=exc.reason_code)
    carrier = translation["physical_carrier"].lower()
    physics = packet["domain_kind"] == "physics"
    if physics:
        if carrier.startswith("not_applicable_non_physics:") or not any(term in carrier for term in PHYSICS_CARRIER_TERMS):
            _fail("physics packet lacks a concrete physical carrier")
    elif not carrier.startswith("not_applicable_non_physics:"):
        _fail("nonphysics packet must state why no physical carrier applies")
    obligations = translation["observable_or_theorem_obligations"]
    _validate_physics_handback(
        packet,
        physical_carrier=translation["physical_carrier"],
        burdens=obligations,
        correction_tests=[translation["correction_test"]],
        theory_atlas_binding=atlas_binding,
    )
    if not any(row["control_status"] == "not_reached_without_abstraction" for row in obligations):
        _fail("no obligation is shown to be unreachable without the abstraction")
    subject = forge_subject_digest(packet)
    _validate_auditors(packet, subject_digest=subject, physics=physics)
    fit = packet["audit_receipts"]["fit_gap"]["output"]
    same = packet["audit_receipts"]["same_domain"]["output"]
    if translation["decision"] == "invest" and (
        fit["verdict"] != "candidate_advantage" or same["certificate_status"] != "passed"
    ):
        _fail("forge investment requires positive fit-gap and passed same-domain outputs")
    if physics:
        physical = packet["audit_receipts"]["physical_relevance"]["output"]
        obligation_ids = [row["obligation_id"] for row in obligations]
        if physical["physical_carrier"] != translation["physical_carrier"] or set(physical["obligation_ids"]) != set(obligation_ids):
            _fail("physical auditor output does not bind the packet carrier and obligations")
        if physical["correction_test_id"] != translation["correction_test"]["test_id"]:
            _fail("physical auditor output does not bind the correction test")
        if physical["investment_decision"] != translation["decision"]:
            _fail("physical auditor decision differs from the forge decision")
    if parallel_evaluation is None:
        _fail("forge validation requires the full executed parallel evaluation artifact")
    ablation = _validate_ablation(
        packet["value_ablation"], translation["decision"], lens, parallel_evaluation,
        target_id=packet["target_id"], snapshot_digest=packet["literature_basis"]["snapshot_digest"],
        assimilation_digest=packet["literature_basis"]["assimilation_digest"],
    )
    _validate_literature_evaluation_binding(
        packet["literature_basis"], parallel_evaluation
    )
    packet_digest = canonical_digest(packet)
    formal_receipt = _build_formal_lens_execution_receipt(
        packet=packet,
        packet_digest=packet_digest,
        dependency_authority=dependency_authority,
        parallel_evaluation=parallel_evaluation,
    )
    return {
        "status": "valid", "packet_id": packet["packet_id"], "packet_digest": packet_digest,
        "validation_receipt_id": formal_receipt["receipt_id"],
        "formal_lens_execution_receipt": formal_receipt,
        "theory_atlas_validation_receipt_id": atlas_binding[
            "validation_receipt_id"
        ],
        "theory_atlas_crosswalk_digest": atlas_binding["crosswalk_digest"],
        "lens": lens, "heuristic_score": computed["score"], "witness_kind": packet["failure_witness"]["witness_kind"],
        **ablation,
    }


def _ym_exact_sorted_refs(row: Mapping[str, Any], field: str, label: str) -> list[str]:
    values = [str(value) for value in row[field]]
    if not values or values != sorted(set(values)):
        _fail(f"{label} {field} must be a nonempty canonical unique list")
    return values


def _ym_evidence_entry(
    evidence_ref: str,
    evidence_kind: str,
    source: Mapping[str, Any],
    *,
    source_ref: str,
    subject_structure_id: str,
    claim_id: str,
    inference_type: str,
    exact_claim: str,
    polarity: str,
    conclusion: str,
    quantified_domain_coverage: Sequence[str] = (),
) -> dict[str, Any]:
    """Seal one derived bridge-evidence locator to its exact source bytes."""

    if subject_structure_id not in YM_STRUCTURES:
        _fail(
            "Yang--Mills evidence must name canonical structures",
            reason_code=YM_EVIDENCE_INFERENCE_INVALID,
        )
    quantifier_coverage = sorted(set(quantified_domain_coverage))
    if not set(quantifier_coverage).issubset(
        YM_STRUCTURE_CONTRACTS[subject_structure_id]["quantifier_refs"]
    ):
        _fail(
            "Yang--Mills evidence claims quantifier coverage outside its subject",
            reason_code=YM_EVIDENCE_INFERENCE_INVALID,
        )
    core = {
        "evidence_ref": evidence_ref,
        "evidence_kind": evidence_kind,
        "source_ref": source_ref,
        "source_digest": canonical_digest(source),
        "subject_structure_id": subject_structure_id,
        "claim_id": claim_id,
        "inference_type": inference_type,
        "exact_claim": exact_claim,
        "polarity": polarity,
        "conclusion": conclusion,
        "quantified_domain_coverage": quantifier_coverage,
        "authority_scope": YM_AUTHORITY_SCOPE,
    }
    return {**core, "content_digest": canonical_digest(core)}


def _ym_derived_evidence_registry(
    *,
    target_contract: Mapping[str, Any],
    upstream_packet_bindings: Sequence[Mapping[str, Any]],
    failure_witness: Mapping[str, Any],
    calibration_matrix: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Derive the complete evidence registry instead of trusting caller labels."""

    rows = []
    for field in sorted(YM_TARGET_CONTRACT_REFS):
        structure_ids = sorted(
            structure_id
            for structure_id, contract in YM_STRUCTURE_CONTRACTS.items()
            if field in contract["target_contract_refs"]
        )
        for structure_id in structure_ids:
            rows.append(
                _ym_evidence_entry(
                    f"target_contract.{field}.{structure_id}",
                    "target_declaration",
                    {"field": field, "value": target_contract[field]},
                    source_ref=f"target_contract.{field}",
                    subject_structure_id=structure_id,
                    claim_id=f"ym.claim.target.{field}.{structure_id}",
                    inference_type="scope_declaration",
                    exact_claim=(
                        f"Target field {field} is fixed to {target_contract[field]!r} "
                        f"for {structure_id}; this declares scope and proves no construction."
                    ),
                    polarity="declares",
                    conclusion="target_declaration_only",
                )
            )
    for row in sorted(upstream_packet_bindings, key=lambda item: str(item["packet_id"])):
        for structure_id in YM_LENS_STRUCTURE_MAP[str(row["lens"])]:
            rows.append(
                _ym_evidence_entry(
                    f"upstream_packet.{row['packet_id']}.{structure_id}",
                    "validated_finite_forge",
                    row,
                    source_ref=str(row["packet_id"]),
                    subject_structure_id=structure_id,
                    claim_id=f"ym.claim.finite.{row['packet_id']}.{structure_id}",
                    inference_type="finite_transport_support",
                    exact_claim=(
                        f"Validated finite {row['lens']} forge {row['packet_id']} "
                        f"supports only the sealed bridge facet of {structure_id}."
                    ),
                    polarity="supports",
                    conclusion="finite_bridge_support_only",
                )
            )
    continuum_structures = (
        "os_reconstruction_burden",
        "positive_hamiltonian_gap_target",
    )
    for row in sorted(failure_witness["evidence"], key=lambda item: str(item["evidence_id"])):
        for structure_id in continuum_structures:
            rows.append(
                _ym_evidence_entry(
                    f"failure_witness.evidence.{row['evidence_id']}.{structure_id}",
                    "finite_negative_witness",
                    row,
                    source_ref=str(row["evidence_id"]),
                    subject_structure_id=structure_id,
                    claim_id=f"ym.claim.obstruction.{row['evidence_id']}.{structure_id}",
                    inference_type="finite_obstruction",
                    exact_claim=(
                        f"Finite witness {row['evidence_id']} localizes a bridge "
                        f"obstruction for {structure_id} without deciding the continuum target."
                    ),
                    polarity="challenges",
                    conclusion="finite_bridge_obstruction_only",
                )
            )
    calibration_kinds = {
        "symbolic": (
            "calibration_symbolic_replay",
            "restricted_symbolic_calibration",
            "calibrates",
            "restricted_symbolic_boundary_only",
        ),
        "countermodel": (
            "calibration_countermodel_replay",
            "restricted_countermodel",
            "challenges",
            "restricted_countermodel_only",
        ),
        "boundary_fixture": (
            "calibration_boundary_fixture",
            "boundary_calibration",
            "bounds",
            "declared_boundary_fixture_only",
        ),
    }
    for row in sorted(calibration_matrix, key=lambda item: str(item["case_id"])):
        evidence = row.get("evidence")
        if isinstance(evidence, Mapping):
            evidence_kind, inference_type, polarity, conclusion = calibration_kinds[
                str(row["runner_kind"])
            ]
            for structure_id in YM_CALIBRATION_STRUCTURE_MAP[str(row["case_id"])]:
                rows.append(
                    _ym_evidence_entry(
                        f"calibration.{row['case_id']}.{evidence['evidence_id']}.{structure_id}",
                        evidence_kind,
                        {
                            "evidence": evidence,
                            "validator_receipt": row["validator_receipt"],
                            "result_status": row["result_status"],
                        },
                        source_ref=str(row["case_id"]),
                        subject_structure_id=structure_id,
                        claim_id=f"ym.claim.calibration.{row['case_id']}.{structure_id}",
                        inference_type=inference_type,
                        exact_claim=(
                            f"Calibration {row['case_id']} bears only on the sealed "
                            f"finite or declared boundary of {structure_id}."
                        ),
                        polarity=polarity,
                        conclusion=conclusion,
                    )
                )
    return sorted(rows, key=lambda row: row["evidence_ref"])


def _ym_quantifier_binding_digest(refs: Sequence[str]) -> str:
    return canonical_digest(
        [
            {"quantifier_id": ref, **copy.deepcopy(YM_QUANTIFIER_CONTRACT[ref])}
            for ref in refs
        ]
    )


def _ym_evidence_binding_digest(
    refs: Sequence[str], registry_by_ref: Mapping[str, Mapping[str, Any]]
) -> str:
    return canonical_digest([registry_by_ref[ref] for ref in refs])


def _ym_unavailable_continuum_authority() -> dict[str, Any]:
    """Emit a typed absence; self-hashed JSON can never mint continuum authority."""

    core = {
        "authority_version": "1.0.0",
        "status": "unavailable",
        "reason_code": "no_approved_continuum_checker_registered",
        "target_id": "yang-mills-existence-and-mass-gap-target",
        "claim_ids": [],
        "authority_scope": "no_continuum_claim_authority",
    }
    return {**core, "content_digest": canonical_digest(core)}


def _ym_derived_carrier_translations(
    translations: Sequence[Mapping[str, Any]],
    *,
    ledger: Sequence[Mapping[str, Any]],
    registry: Sequence[Mapping[str, Any]],
    correction_ids_by_structure: Mapping[str, Sequence[str]],
) -> list[dict[str, Any]]:
    """Derive carrier status and evidence from exact structure-ledger rows."""

    ledger_by_id = {str(row["structure_id"]): row for row in ledger}
    registry_by_ref = {str(row["evidence_ref"]): row for row in registry}
    ledger_digest = canonical_digest(ledger)
    registry_digest = canonical_digest(registry)
    raw_fields = (
        "abstract_entity_id",
        "abstract_entity",
        "entity_kind",
        "physical_carrier_id",
        "physical_carrier",
        "preservation_structure_ids",
        "preserved_invariants",
        "broken_or_open_invariants",
        "target_burden",
    )
    order = {"failed": 0, "open": 1, "conditional": 2, "proved": 3}
    output: list[dict[str, Any]] = []
    for authored in sorted(
        translations,
        key=lambda row: str(row["abstract_entity_id"]),
    ):
        try:
            row = {field: copy.deepcopy(authored[field]) for field in raw_fields}
        except KeyError as exc:
            _fail(
                f"carrier translation lacks derived-basis input {exc.args[0]}",
                reason_code=YM_CARRIER_STATUS_DERIVATION_INVALID,
            )
        structure_ids = [str(value) for value in row["preservation_structure_ids"]]
        if (
            not structure_ids
            or structure_ids != sorted(set(structure_ids))
            or not set(structure_ids).issubset(ledger_by_id)
            or any(ledger_by_id[value]["status"] == "required" for value in structure_ids)
        ):
            _fail(
                "carrier translations require canonical non-declaration structure bindings",
                reason_code=YM_CARRIER_STATUS_DERIVATION_INVALID,
            )
        structure_statuses = [
            {
                "structure_id": structure_id,
                "status": str(ledger_by_id[structure_id]["status"]),
            }
            for structure_id in structure_ids
        ]
        statuses = [value["status"] for value in structure_statuses]
        if any(status not in order for status in statuses):
            _fail(
                "carrier status basis includes a non-evidential target declaration",
                reason_code=YM_CARRIER_STATUS_DERIVATION_INVALID,
            )
        derived_status = min(statuses, key=order.__getitem__)
        if derived_status == "proved":
            derived_status = "conditional"
        evidence_refs = sorted(
            {
                str(reference)
                for structure_id in structure_ids
                for reference in ledger_by_id[structure_id]["evidence_refs"]
            }
        )
        basis = {
            "evidence_matrix_version": YM_EVIDENCE_MATRIX_VERSION,
            "lattice_order": ["failed", "open", "conditional", "proved"],
            "structure_statuses": structure_statuses,
            "finite_authority_cap": "conditional",
            "derivation_rule": "minimum_structure_status_then_cap_finite_authority_at_conditional",
        }
        output.append(
            {
                **row,
                "preservation_status": derived_status,
                "preservation_status_basis": basis,
                "preservation_status_basis_digest": canonical_digest(basis),
                "evidence_refs": evidence_refs,
                "evidence_binding_digest": _ym_evidence_binding_digest(
                    evidence_refs,
                    registry_by_ref,
                ),
                "structure_ledger_digest": ledger_digest,
                "evidence_registry_digest": registry_digest,
                "correction_test_ids": sorted(
                    {
                        correction_id
                        for structure_id in structure_ids
                        for correction_id in correction_ids_by_structure[
                            structure_id
                        ]
                    }
                ),
            }
        )
    return output


def _ym_status_rationale(kind: str, status: str) -> str:
    rationales = {
        "required": "This row freezes a target commitment; it does not assert that the target theory has been constructed.",
        "conditional": "Only sealed finite bridge and calibration evidence is available; continuum physical preservation remains unproved.",
        "open": "The burden or consequence remains open and cannot be promoted by categorical or HoTT form alone.",
        "proved": "Proof is limited to the sealed finite bridge representation and grants no continuum physical theorem.",
        "failed": "A sealed negative witness defeats this bridge-level preservation claim without deciding the full target theory.",
    }
    if kind == "fixed_target_commitment" and status != "required":
        _fail("fixed Yang--Mills target commitments must have required status")
    return rationales[status]


def build_ym_preservation_contract(
    *,
    upstream_packet_bindings: Sequence[Mapping[str, Any]],
    failure_witness: Mapping[str, Any],
    calibration_matrix: Sequence[Mapping[str, Any]],
    correction_tests: Sequence[Mapping[str, Any]],
    carrier_translations: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build the canonical current 14-row YM bridge ledger and handback inputs.

    The current fixture deliberately marks transport evidence conditional and
    reconstruction/consequence rows open.  Later packets may strengthen or
    fail rows only when the validator finds evidence appropriate to that status.
    """

    corrections = sorted(
        [copy.deepcopy(dict(row)) for row in correction_tests],
        key=lambda row: str(row["test_id"]),
    )
    correction_ids = [str(row["test_id"]) for row in corrections]
    if correction_ids != sorted(YM_CORRECTION_STRUCTURE_MAP):
        _fail("YM preservation builder requires unique correction tests")
    correction_ids_by_structure = {
        structure_id: [
            correction_id
            for correction_id in correction_ids
            if structure_id in YM_CORRECTION_STRUCTURE_MAP[correction_id]
        ]
        for structure_id in YM_STRUCTURE_IDS
    }
    for row in corrections:
        correction_id = str(row["test_id"])
        if list(row.get("preservation_structure_ids", ())) != list(
            YM_CORRECTION_STRUCTURE_MAP[correction_id]
        ):
            _fail(
                "YM correction scope is not the canonical structure-specific matrix",
                reason_code=YM_CORRECTION_COVERAGE_INVALID,
            )
    if any(not value for value in correction_ids_by_structure.values()):
        _fail(
            "YM correction matrix leaves a structure without a falsifier",
            reason_code=YM_CORRECTION_COVERAGE_INVALID,
        )
    carriers = sorted(
        [copy.deepcopy(dict(row)) for row in carrier_translations],
        key=lambda row: str(row["abstract_entity_id"]),
    )
    evidence_registry = _ym_derived_evidence_registry(
        target_contract=YM_TARGET_CONTRACT,
        upstream_packet_bindings=upstream_packet_bindings,
        failure_witness=failure_witness,
        calibration_matrix=calibration_matrix,
    )
    registry_by_ref = {row["evidence_ref"]: row for row in evidence_registry}
    ledger: list[dict[str, Any]] = []
    obligations: list[dict[str, Any]] = []
    for structure_id in YM_STRUCTURE_IDS:
        contract = YM_STRUCTURE_CONTRACTS[structure_id]
        kind = str(contract["kind"])
        if kind == "fixed_target_commitment":
            status = "required"
            evidence_refs = sorted(
                ref
                for ref, evidence in registry_by_ref.items()
                if evidence["subject_structure_id"] == structure_id
                and evidence["evidence_kind"] == "target_declaration"
            )
        elif kind == "transport_invariant":
            status = "conditional"
            evidence_refs = sorted(
                ref
                for ref, evidence in registry_by_ref.items()
                if evidence["subject_structure_id"] == structure_id
            )
        else:
            status = "open"
            evidence_refs = sorted(
                ref
                for ref, evidence in registry_by_ref.items()
                if evidence["subject_structure_id"] == structure_id
            )
        target_refs = list(contract["target_contract_refs"])
        quantifier_refs = list(contract["quantifier_refs"])
        obligation_id = f"ym.obligation.{structure_id}"
        common = {
            "target_contract_refs": target_refs,
            "quantifier_refs": quantifier_refs,
            "quantifier_binding_digest": _ym_quantifier_binding_digest(quantifier_refs),
            "evidence_refs": evidence_refs,
            "evidence_binding_digest": _ym_evidence_binding_digest(
                evidence_refs, registry_by_ref
            ),
            "correction_test_ids": correction_ids_by_structure[structure_id],
            "status": status,
            "authority_scope": YM_AUTHORITY_SCOPE,
        }
        ledger.append(
            {
                "structure_id": structure_id,
                "structure_kind": kind,
                "obligation_ids": [obligation_id],
                "status_rationale": _ym_status_rationale(kind, status),
                # These are separately committed artifacts.  Keep their
                # nested rows independent so mutating one cannot rewrite its
                # cross-checking peer before the validator sees the attack.
                **copy.deepcopy(common),
            }
        )
        obligations.append(
            {
                "obligation_id": obligation_id,
                "preservation_structure_ids": [structure_id],
                "claim_level": contract["claim_level"],
                "observable_or_theorem": contract["obligation_kind"],
                "statement": YM_STRUCTURE_STATEMENTS[structure_id],
                "quantifiers": copy.deepcopy(YM_QUANTIFIER_CONTRACT),
                **copy.deepcopy(common),
            }
        )
    carriers = _ym_derived_carrier_translations(
        carriers,
        ledger=ledger,
        registry=evidence_registry,
        correction_ids_by_structure=correction_ids_by_structure,
    )
    continuum_authority = _ym_unavailable_continuum_authority()
    certificate_status, certificate_status_basis = _ym_certificate_status_basis(
        ledger, carriers
    )
    quantifier_digest = canonical_digest(YM_QUANTIFIER_CONTRACT)
    evidence_digest = canonical_digest(evidence_registry)
    transfer = {
        "source_domain": "four-dimensional pure Yang-Mills",
        "target_domain": "four-dimensional pure Yang-Mills",
        "structure_ledger": ledger,
        "structure_ledger_digest": canonical_digest(ledger),
        "changed_structures": list(YM_CHANGED_STRUCTURES),
        "certificate_status": certificate_status,
        "certificate_status_basis": certificate_status_basis,
        "quantifier_contract_digest": quantifier_digest,
        "evidence_registry_digest": evidence_digest,
        "carrier_translation_digest": canonical_digest(carriers),
        "continuum_authority_digest": continuum_authority["content_digest"],
        "evidence_matrix_version": YM_EVIDENCE_MATRIX_VERSION,
        "consequence_delta": "The finite bridge returns typed preservation, reconstruction, and spectral burdens without promoting them to physical equivalence.",
        "authority_boundary": YM_TRANSFER_AUTHORITY_BOUNDARY,
    }
    return {
        "quantifier_contract": copy.deepcopy(YM_QUANTIFIER_CONTRACT),
        "quantifier_contract_digest": quantifier_digest,
        "evidence_registry": evidence_registry,
        "evidence_registry_digest": evidence_digest,
        "continuum_authority": continuum_authority,
        "carrier_translations": carriers,
        "theorem_obligations": obligations,
        "same_domain_transfer": transfer,
    }


def _ym_certificate_status_basis(
    ledger: Sequence[Mapping[str, Any]], translations: Sequence[Mapping[str, Any]],
) -> tuple[str, dict[str, Any]]:
    """Compute the transfer certificate from every structure and carrier status."""

    basis: dict[str, Any] = {
        "lattice_order": ["failed", "open", "conditional", "proved"],
        "required_structure_ids": sorted(str(row["structure_id"]) for row in ledger if row["status"] == "required"),
        "proved_structure_ids": sorted(str(row["structure_id"]) for row in ledger if row["status"] == "proved"),
        "conditional_structure_ids": sorted(str(row["structure_id"]) for row in ledger if row["status"] == "conditional"),
        "open_structure_ids": sorted(str(row["structure_id"]) for row in ledger if row["status"] == "open"),
        "failed_structure_ids": sorted(str(row["structure_id"]) for row in ledger if row["status"] == "failed"),
        "proved_carrier_translation_ids": sorted(str(row["abstract_entity_id"]) for row in translations if row["preservation_status"] == "proved"),
        "conditional_carrier_translation_ids": sorted(str(row["abstract_entity_id"]) for row in translations if row["preservation_status"] == "conditional"),
        "open_carrier_translation_ids": sorted(str(row["abstract_entity_id"]) for row in translations if row["preservation_status"] == "open"),
        "failed_carrier_translation_ids": sorted(str(row["abstract_entity_id"]) for row in translations if row["preservation_status"] == "failed"),
    }
    if basis["failed_structure_ids"] or basis["failed_carrier_translation_ids"]:
        return "failed", basis
    if basis["open_structure_ids"] or basis["open_carrier_translation_ids"]:
        return "open", basis
    if basis["conditional_structure_ids"] or basis["conditional_carrier_translation_ids"]:
        return "conditional", basis
    return "proved", basis


def _validate_ym_preservation_contract(bridge: Mapping[str, Any]) -> None:
    """Replay the typed YM structure ledger and every cross-artifact binding."""

    if dict(bridge["target_contract"]) != YM_TARGET_CONTRACT:
        _fail("Yang--Mills target contract differs from the exact frozen target")
    if (
        dict(bridge["quantifier_contract"]) != YM_QUANTIFIER_CONTRACT
        or bridge["quantifier_contract_digest"]
        != canonical_digest(YM_QUANTIFIER_CONTRACT)
    ):
        _fail("Yang--Mills quantifier contract is not the canonical text/value ledger")
    expected_registry = _ym_derived_evidence_registry(
        target_contract=bridge["target_contract"],
        upstream_packet_bindings=bridge["upstream_packet_bindings"],
        failure_witness=bridge["failure_witness"],
        calibration_matrix=bridge["calibration_matrix"],
    )
    if (
        bridge["evidence_registry"] != expected_registry
        or bridge["evidence_registry_digest"] != canonical_digest(expected_registry)
    ):
        _fail(
            "Yang--Mills evidence registry is not the exact derived source ledger",
            reason_code=YM_EVIDENCE_INFERENCE_INVALID,
        )
    expected_continuum_authority = _ym_unavailable_continuum_authority()
    if bridge["continuum_authority"] != expected_continuum_authority:
        _fail(
            "serialized continuum authority is unavailable unless an approved opaque verifier is added",
            reason_code=YM_CONTINUUM_AUTHORITY_REQUIRED,
        )
    registry_by_ref = {row["evidence_ref"]: row for row in expected_registry}
    transfer = bridge["same_domain_transfer"]
    ledger = list(transfer["structure_ledger"])
    structure_ids = [str(row["structure_id"]) for row in ledger]
    if structure_ids != list(YM_STRUCTURE_IDS):
        _fail("same-domain transfer must use the canonical ordered 14-row Yang--Mills ledger")
    if transfer["structure_ledger_digest"] != canonical_digest(ledger):
        _fail("same-domain structure ledger digest mismatch")
    changed = [str(value) for value in transfer["changed_structures"]]
    if changed != sorted(set(changed)) or tuple(changed) != YM_CHANGED_STRUCTURES or any(
        not any(value.startswith(prefix) and len(value) > len(prefix) for prefix in YM_CHANGE_PREFIXES)
        for value in changed
    ):
        _fail(
            f"{YM_CHANGED_STRUCTURES_INVALID}: same-domain changes must be typed as "
            "representation or proof-obligation changes"
        )
    if set(changed).intersection(YM_STRUCTURES):
        _fail("same-domain changes cannot alter a preserved Yang--Mills structure")

    obligations = list(bridge["theorem_obligations"])
    obligation_ids = [str(row["obligation_id"]) for row in obligations]
    expected_obligation_ids = [f"ym.obligation.{structure_id}" for structure_id in YM_STRUCTURE_IDS]
    if obligation_ids != expected_obligation_ids:
        _fail("Yang--Mills theorem obligations must cover every structure exactly once")
    obligation_by_id = {str(row["obligation_id"]): row for row in obligations}
    correction_id_list = [str(row["test_id"]) for row in bridge["correction_tests"]]
    if correction_id_list != sorted(YM_CORRECTION_STRUCTURE_MAP):
        _fail("Yang--Mills correction tests must use canonical unique ID order")
    correction_ids_by_structure = {
        structure_id: [
            correction_id
            for correction_id in correction_id_list
            if structure_id in YM_CORRECTION_STRUCTURE_MAP[correction_id]
        ]
        for structure_id in YM_STRUCTURE_IDS
    }
    for correction in bridge["correction_tests"]:
        correction_id = str(correction["test_id"])
        if correction["preservation_structure_ids"] != list(
            YM_CORRECTION_STRUCTURE_MAP[correction_id]
        ):
            _fail(
                "Yang--Mills correction scope is not exact or is misrouted",
                reason_code=YM_CORRECTION_COVERAGE_INVALID,
            )
    correction_ids = set(correction_id_list)
    used_evidence_refs: set[str] = set()
    for row in ledger:
        structure_id = str(row["structure_id"])
        contract = YM_STRUCTURE_CONTRACTS[structure_id]
        if row["structure_kind"] != contract["kind"] or row["authority_scope"] != YM_AUTHORITY_SCOPE:
            _fail(f"Yang--Mills structure {structure_id} has the wrong kind or authority scope")
        allowed_statuses = {
            "fixed_target_commitment": {"required"},
            "transport_invariant": {"proved", "conditional", "open", "failed"},
            "open_reconstruction_burden": {"open", "proved", "failed"},
            "desired_consequence": {"open", "proved", "failed"},
        }[str(row["structure_kind"])]
        if row["status"] not in allowed_statuses:
            _fail(f"Yang--Mills structure {structure_id} has an impossible status for its kind")
        if row["status"] == "proved" and row["structure_kind"] != "fixed_target_commitment":
            _fail(
                "The finite bridge cannot prove any physical transport, reconstruction, "
                "or spectral claim; a separately verified continuum authority is required",
                reason_code=YM_CONTINUUM_AUTHORITY_REQUIRED,
            )
        target_refs = _ym_exact_sorted_refs(row, "target_contract_refs", structure_id)
        quantifier_refs = _ym_exact_sorted_refs(row, "quantifier_refs", structure_id)
        evidence_refs = _ym_exact_sorted_refs(row, "evidence_refs", structure_id)
        bound_obligation_ids = _ym_exact_sorted_refs(row, "obligation_ids", structure_id)
        bound_correction_ids = _ym_exact_sorted_refs(row, "correction_test_ids", structure_id)
        if target_refs != list(contract["target_contract_refs"]):
            _fail(f"Yang--Mills structure {structure_id} changes its exact target-field binding")
        if quantifier_refs != list(contract["quantifier_refs"]):
            _fail(f"Yang--Mills structure {structure_id} changes its exact quantifier binding")
        if not set(evidence_refs).issubset(registry_by_ref):
            _fail(f"Yang--Mills structure {structure_id} cites unavailable evidence")
        used_evidence_refs.update(evidence_refs)
        evidence_kinds = {registry_by_ref[ref]["evidence_kind"] for ref in evidence_refs}
        if any(
            structure_id != registry_by_ref[ref]["subject_structure_id"]
            for ref in evidence_refs
        ):
            _fail(
                f"Yang--Mills structure {structure_id} cites evidence for another inference",
                reason_code=YM_EVIDENCE_INFERENCE_INVALID,
            )
        conclusions = {registry_by_ref[ref]["conclusion"] for ref in evidence_refs}
        if any(
            not set(registry_by_ref[ref]["quantified_domain_coverage"]).issubset(
                quantifier_refs
            )
            for ref in evidence_refs
        ):
            _fail(
                f"Yang--Mills structure {structure_id} cites foreign quantifier coverage",
                reason_code=YM_EVIDENCE_INFERENCE_INVALID,
            )
        if row["status"] == "required" and evidence_kinds != {"target_declaration"}:
            _fail(f"Yang--Mills target commitment {structure_id} must cite declarations only")
        if row["status"] in {"conditional", "proved"} and evidence_kinds == {"target_declaration"}:
            _fail(f"Yang--Mills structure {structure_id} cannot derive {row['status']} from declarations alone")
        if row["status"] == "proved" and not evidence_kinds.intersection(
            {"validated_finite_forge", "calibration_symbolic_replay", "calibration_countermodel_replay"}
        ):
            _fail(f"Yang--Mills proved structure {structure_id} lacks replayable bridge evidence")
        if row["status"] == "failed" and not evidence_kinds.intersection(
            {"finite_negative_witness", "calibration_countermodel_replay"}
        ):
            _fail(f"Yang--Mills failed structure {structure_id} lacks negative evidence")
        if row["status"] == "failed" and not conclusions.intersection(
            {"finite_bridge_obstruction_only", "restricted_countermodel_only"}
        ):
            _fail(
                f"Yang--Mills failed structure {structure_id} lacks a challenging conclusion",
                reason_code=YM_EVIDENCE_STATUS_MATRIX_INVALID,
            )
        if row["quantifier_binding_digest"] != _ym_quantifier_binding_digest(quantifier_refs):
            _fail(f"Yang--Mills structure {structure_id} quantifier digest mismatch")
        if row["evidence_binding_digest"] != _ym_evidence_binding_digest(
            evidence_refs, registry_by_ref
        ):
            _fail(f"Yang--Mills structure {structure_id} evidence digest mismatch")
        if row["status_rationale"] != _ym_status_rationale(
            str(row["structure_kind"]), str(row["status"])
        ):
            _fail(f"Yang--Mills structure {structure_id} changes its status semantics")
        expected_obligation_id = f"ym.obligation.{structure_id}"
        if (
            bound_obligation_ids != [expected_obligation_id]
            or bound_correction_ids != correction_ids_by_structure[structure_id]
        ):
            _fail(
                f"Yang--Mills structure {structure_id} has an inexact obligation or correction binding",
                reason_code=YM_CORRECTION_COVERAGE_INVALID,
            )
        obligation = obligation_by_id[expected_obligation_id]
        if (
            obligation["preservation_structure_ids"] != [structure_id]
            or obligation["target_contract_refs"] != target_refs
            or obligation["quantifier_refs"] != quantifier_refs
            or obligation["evidence_refs"] != evidence_refs
            or obligation["quantifier_binding_digest"] != row["quantifier_binding_digest"]
            or obligation["evidence_binding_digest"] != row["evidence_binding_digest"]
            or obligation["correction_test_ids"] != bound_correction_ids
            or obligation["claim_level"] != contract["claim_level"]
            or obligation["observable_or_theorem"] != contract["obligation_kind"]
            or obligation["status"] != row["status"]
            or obligation["statement"] != YM_STRUCTURE_STATEMENTS[structure_id]
            or obligation["quantifiers"] != YM_QUANTIFIER_CONTRACT
            or obligation["authority_scope"] != YM_AUTHORITY_SCOPE
        ):
            _fail(f"Yang--Mills obligation {expected_obligation_id} is not the exact structure handback")
    contract_refs = {
        str(reference)
        for row in obligations
        for reference in row["target_contract_refs"]
    }
    structure_refs = {
        str(reference)
        for row in obligations
        for reference in row["preservation_structure_ids"]
    }
    if contract_refs != YM_TARGET_CONTRACT_REFS:
        _fail("theorem obligations do not cover every frozen Yang--Mills target field")
    if structure_refs != YM_STRUCTURES:
        _fail("theorem obligations do not cover every preserved Yang--Mills structure")
    quantifier_refs = {str(reference) for row in obligations for reference in row["quantifier_refs"]}
    if quantifier_refs != set(YM_QUANTIFIER_KEYS):
        _fail("theorem obligations do not cover every Yang--Mills quantifier")
    if {str(reference) for row in obligations for reference in row["correction_test_ids"]} != correction_ids:
        _fail("theorem obligations do not cover every correction test")
    for correction_id, expected_structures in YM_CORRECTION_STRUCTURE_MAP.items():
        actual_structures = tuple(
            row["structure_id"]
            for row in ledger
            if correction_id in row["correction_test_ids"]
        )
        if actual_structures != tuple(
            structure_id
            for structure_id in YM_STRUCTURE_IDS
            if structure_id in expected_structures
        ):
            _fail(
                "Yang--Mills correction-to-structure coverage is not bidirectional",
                reason_code=YM_CORRECTION_COVERAGE_INVALID,
            )
    if used_evidence_refs != set(registry_by_ref):
        _fail("the typed structure ledger does not account for every derived evidence row")
    if not any(
        row["claim_level"] == "C3"
        and row["observable_or_theorem"] in {"theorem", "both"}
        for row in obligations
    ):
        _fail("Yang--Mills handback requires an explicit C3 theorem obligation")
    expected_status, expected_basis = _ym_certificate_status_basis(
        ledger, bridge["carrier_translations"]
    )
    expected_carriers = _ym_derived_carrier_translations(
        bridge["carrier_translations"],
        ledger=ledger,
        registry=expected_registry,
        correction_ids_by_structure=correction_ids_by_structure,
    )
    if bridge["carrier_translations"] != expected_carriers:
        _fail(
            "carrier preservation status or basis is not derived from the exact ledger",
            reason_code=YM_CARRIER_STATUS_DERIVATION_INVALID,
        )
    if transfer["certificate_status"] != expected_status or transfer["certificate_status_basis"] != expected_basis:
        _fail("same-domain certificate status does not equal the fail-closed structure/carrier lattice")
    if transfer["carrier_translation_digest"] != canonical_digest(bridge["carrier_translations"]):
        _fail("same-domain transfer does not bind the exact carrier translations")
    if (
        transfer["quantifier_contract_digest"] != bridge["quantifier_contract_digest"]
        or transfer["evidence_registry_digest"] != bridge["evidence_registry_digest"]
        or transfer["continuum_authority_digest"]
        != expected_continuum_authority["content_digest"]
        or transfer["evidence_matrix_version"] != YM_EVIDENCE_MATRIX_VERSION
        or transfer["authority_boundary"] != YM_TRANSFER_AUTHORITY_BOUNDARY
    ):
        _fail("same-domain transfer does not bind quantifier/evidence authority and its finite boundary")


def validate_ym_bridge(
    payload: Mapping[str, Any], *, upstream_packets: Sequence[Mapping[str, Any]] | None = None,
    parallel_evaluation: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate the Yang--Mills bridge, including upstream forges and calibrations."""

    bridge = copy.deepcopy(dict(payload))
    _schema(bridge, "ym_categorical_hott_bridge.schema.json")
    try:
        dependency_context = _validate_formal_dependency_run_context(
            bridge["dependency_authority"]
        )
        dependency_authority = dependency_context.snapshot()
    except FormalDependencyAuthorityError as exc:
        _fail(str(exc))
    _validate_literature_basis(
        bridge["literature_basis"], target_id=bridge["target_id"],
        pressure_payload={
            "carrier_translations": bridge["carrier_translations"],
            "theorem_obligations": bridge["theorem_obligations"],
        },
    )
    if upstream_packets is None or parallel_evaluation is None:
        _fail("YM bridge validation requires upstream forge packets and the executed evaluation")
    bindings = {row["packet_id"]: row for row in bridge["upstream_packet_bindings"]}
    if len(bindings) != len(bridge["upstream_packet_bindings"]):
        _fail("upstream packet bindings duplicate a packet ID")
    if list(bindings) != sorted(bindings):
        _fail("upstream packet bindings must use canonical packet-ID order")
    validated_lenses: set[str] = set()
    for upstream in upstream_packets:
        packet = upstream.get("packet") if isinstance(upstream, Mapping) else None
        evaluation = upstream.get("parallel_evaluation", parallel_evaluation) if isinstance(upstream, Mapping) else None
        if not isinstance(packet, Mapping) or not isinstance(evaluation, Mapping):
            _fail("each upstream binding needs a packet and parallel evaluation")
        result = validate_forge_packet(packet, parallel_evaluation=evaluation)
        binding = bindings.get(packet["packet_id"])
        if binding is None:
            _fail("validated upstream forge lacks a bridge binding")
        model = packet["categorical_model"] if packet["lens"] == "categorical" else packet["hott_model"]
        expected = {
            "packet_id": packet["packet_id"], "packet_digest": result["packet_digest"],
            "lens": packet["lens"], "model_digest": canonical_digest(model),
            "witness_certificate_digest": canonical_digest(packet["failure_witness"]["certificate"]),
            "validation_receipt_id": result["validation_receipt_id"],
            "formal_lens_execution_receipt": result[
                "formal_lens_execution_receipt"
            ],
        }
        if binding != expected:
            _fail("YM upstream binding differs from the transitively validated forge")
        validated_lenses.add(packet["lens"])
    if set(bindings) != {upstream["packet"]["packet_id"] for upstream in upstream_packets}:
        _fail("YM bridge contains an unvalidated upstream packet binding")
    required_lenses = {"categorical", "hott"} if bridge["lens"] == "categorical_hott" else {bridge["lens"]}
    if not required_lenses.issubset(validated_lenses):
        _fail("YM bridge lacks the upstream forge lens required by its declaration")
    try:
        validate_executable_physical_diagram(
            bridge["physical_diagram"], bridge["failure_witness"]
        )
    except FormalReasoningError as exc:
        _fail(str(exc), reason_code=exc.reason_code)
    for field, value in bridge["representation_package"].items():
        _substantive(value, f"representation_package.{field}")
    physical_objects = {row["object_id"] for row in bridge["physical_diagram"]["objects"]}
    carrier_ids = [str(row["abstract_entity_id"]) for row in bridge["carrier_translations"]]
    if carrier_ids != sorted(set(carrier_ids)):
        _fail("carrier translations must use canonical unique abstract-entity order")
    for index, row in enumerate(bridge["carrier_translations"]):
        carrier = _substantive(row["physical_carrier"], f"carrier_translations[{index}].physical_carrier").lower()
        if row["physical_carrier_id"] not in physical_objects or not any(term in carrier for term in PHYSICS_CARRIER_TERMS):
            _fail(f"carrier translation {index} lacks a declared concrete physical carrier")
    transfer = bridge["same_domain_transfer"]
    if _normalized(transfer["source_domain"]) != _normalized(transfer["target_domain"]) or "four-dimensional pure yang-mills" not in _normalized(transfer["source_domain"]):
        _fail("same-domain transfer must preserve four-dimensional pure Yang--Mills")
    _validate_ym_preservation_contract(bridge)
    _validate_physics_handback(
        bridge,
        physical_carrier=bridge["carrier_translations"][0]["physical_carrier"],
        burdens=bridge["theorem_obligations"],
        correction_tests=bridge["correction_tests"],
        target_contract=bridge["target_contract"],
        preservation_transfer=transfer,
        quantifier_contract=bridge["quantifier_contract"],
        evidence_registry=bridge["evidence_registry"],
        carrier_translations=bridge["carrier_translations"],
        continuum_authority=bridge["continuum_authority"],
    )
    subject = ym_bridge_subject_digest(bridge)
    _validate_auditors(bridge, subject_digest=subject, physics=True, ym_bridge=True)
    same = bridge["audit_receipts"]["same_domain"]["output"]
    if (
        _normalized(same["source_domain"]) != _normalized(transfer["source_domain"])
        or _normalized(same["target_domain"]) != _normalized(transfer["target_domain"])
        or same["structure_ledger_digest"] != transfer["structure_ledger_digest"]
        or same["changed_structures"] != transfer["changed_structures"]
        or same["certificate_status"]
        != YM_CERTIFICATE_AUDIT_STATUS[transfer["certificate_status"]]
        or same["certificate_status_basis"] != transfer["certificate_status_basis"]
        or same["quantifier_contract_digest"] != transfer["quantifier_contract_digest"]
        or same["evidence_registry_digest"] != transfer["evidence_registry_digest"]
        or same["carrier_translation_digest"] != transfer["carrier_translation_digest"]
        or same["continuum_authority_digest"]
        != transfer["continuum_authority_digest"]
        or same["evidence_matrix_version"] != transfer["evidence_matrix_version"]
        or same["preservation_transfer_digest"] != canonical_digest(transfer)
    ):
        _fail("same-domain auditor output differs from the physical transfer ledger")
    case_ids = [row["case_id"] for row in bridge["calibration_matrix"]]
    if case_ids != list(YM_CALIBRATION_CASE_IDS):
        _fail("calibration matrix must use the canonical order of all nine registered cases")
    calibration_statuses: list[str] = []
    for row in bridge["calibration_matrix"]:
        status = row["result_status"]
        calibration_statuses.append(status)
        try:
            validate_ym_calibration(row)
        except YMCalibrationError as exc:
            _fail(f"calibration {row['case_id']} is not an executable replay: {exc}")
        if row["dependency_authority"]["content_digest"] != dependency_authority["content_digest"]:
            _fail("calibration dependency authority differs from the bridge closure")
    if not any(row["kind"] in {"theorem", "countermodel", "literature"} for row in bridge["correction_tests"]):
        _fail("YM correction tests need a theory-facing test, not simulation alone")
    decision = bridge["physics_evaluation"]["decision"]
    if decision in {"invest_high_physics_reward", "invest_restricted_model_only"}:
        _fail("finite local bridge evidence never authorizes physics investment")
    ablation = _validate_ablation(
        bridge["value_ablation"], decision, "combined", parallel_evaluation,
        target_id=bridge["target_id"], snapshot_digest=bridge["literature_basis"]["snapshot_digest"],
        assimilation_digest=bridge["literature_basis"]["assimilation_digest"],
    )
    _validate_literature_evaluation_binding(
        bridge["literature_basis"], parallel_evaluation
    )
    physical_output = bridge["audit_receipts"]["physical_relevance"]["output"]
    obligations = [row["obligation_id"] for row in bridge["theorem_obligations"]]
    correction_ids = [row["test_id"] for row in bridge["correction_tests"]]
    if physical_output["obligation_ids"] != obligations or physical_output["correction_test_ids"] != correction_ids:
        _fail("physical auditor output does not bind exact theorem obligations and correction test")
    if physical_output["investment_decision"] != decision:
        _fail("physical auditor decision differs from the bridge decision")
    evaluation = bridge["physics_evaluation"]
    if (
        evaluation["assessment_status"] != "post_handback_internal_hypothesis"
        or evaluation["physics_value_authorized"] is not False
        or evaluation["investment_authorized"] is not False
    ):
        _fail("physics-value language must remain a post-handback internal hypothesis")
    if not YM_HANDOFFS <= set(bridge["downstream_handoffs"]):
        _fail("YM bridge omits a mandatory downstream proof, relevance, or frontier handoff")
    bridge_digest = canonical_digest(bridge)
    return {
        "status": "valid", "bridge_id": bridge["bridge_id"], "bridge_digest": bridge_digest,
        "validation_receipt_id": stable_identifier("ym-bridge-validation", bridge["bridge_id"], bridge_digest),
        "upstream_formal_lens_execution_receipt_ids": [
            row["formal_lens_execution_receipt"]["receipt_id"]
            for row in bridge["upstream_packet_bindings"]
        ],
        "claim_level": bridge["claim_level"], "decision": decision,
        "calibration_cases": len(case_ids), "completed_calibrations": calibration_statuses.count("passed"),
        **ablation,
    }


__all__ = [
    "AbstractionValidationError", "YM_CARRIER_STATUS_DERIVATION_INVALID", "YM_CONTINUUM_AUTHORITY_REQUIRED", "YM_CORRECTION_COVERAGE_INVALID", "YM_EVIDENCE_INFERENCE_INVALID", "YM_EVIDENCE_MATRIX_VERSION", "YM_EVIDENCE_STATUS_MATRIX_INVALID", "YM_QUANTIFIER_CONTRACT", "YM_STRUCTURE_CONTRACTS", "YM_STRUCTURE_IDS", "build_physics_handback", "build_ym_preservation_contract", "forge_subject_digest", "literature_pressure_digest",
    "validate_forge_packet", "validate_ym_bridge", "ym_bridge_subject_digest",
]
