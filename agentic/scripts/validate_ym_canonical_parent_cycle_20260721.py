#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Validate YM21 semantics only after exact canonical-commit replay.

The generic theory gate is the authority boundary.  This target validator then
loads every decision-bearing role and operator input from that verified commit;
mutable workspace files and report copies are never semantic inputs.  The
remaining checks are deliberately domain-specific and retain the no-proof,
no-source-validation, no-external-efficacy boundary.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SCRIPT_ROOT = ROOT / "agentic/scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    canonical_digest,
    canonical_json,
    file_digest,
    load_json,
    safe_relative_path,
    stable_identifier,
    validate_payload,
)
from agentic.discovery.conceptual_adjudication import (  # noqa: E402
    validate_material_system_transition,
)
from agentic.discovery.evaluation import (  # noqa: E402
    CONCEPTUAL_GATE_IDS,
    validate_evaluation_receipt,
)
from agentic.discovery.hypotheses import validate_high_risk_portfolio  # noqa: E402
from agentic.discovery.literature import (  # noqa: E402
    assimilate_derived_literature,
    derive_claim_mappings,
    validate_assimilation,
    validate_claim_mapping_derivation,
    validate_literature_counterfactual_replay,
    validate_snapshot,
    validate_theory_object_catalog,
)
from agentic.discovery.parallel import validate_parallel_portfolio  # noqa: E402
from agentic.discovery.reflection import validate_packet_invariants  # noqa: E402
from agentic.discovery.theory_gate import verify_canonical_theory_cycle  # noqa: E402
from agentic.experiments import (  # noqa: E402
    validate_experiment_receipt,
    validate_experiment_reflection_receipt,
)
from evaluate_ym_conceptual_quality_20260721 import (  # noqa: E402
    REQUIRED_CORRECTION_IDS,
    REQUIRED_FORMALIZATION_IDS,
    conceptual_structure_projection,
    validate_evidence as validate_conceptual_quality_evidence,
)
from integrate_ym_representational_dynamics_20260721 import (  # noqa: E402
    REGISTERED_RUNTIME_BINDING,
    REGISTERED_RUNTIME_ROOT,
    TARGET_ID,
    registered_runtime_binding_if_present,
)
from run_ym_canonical_parent_cycle_20260721 import (  # noqa: E402
    CONCEPTUAL_QUALITY_REFINEMENT_HISTORY_NAME,
    DIRECT_CHALLENGER_ID,
    PARENT_CONCEPTUAL_QUALITY_EVIDENCE_NAME,
    PUBLICATION_FAILURE_DIR,
    PUBLICATION_FILE_ROLES,
    PUBLICATION_STATUS_NAME,
    RUN_ID,
    SIX_OPERATORS,
    SYNTHESIS_CONCEPTUAL_QUALITY_EVIDENCE_NAME,
    _acceptance_markdown,
    _derived_hypothesis_rebase,
    _literature_counterfactual_worlds,
    _refinement_history_from_committed_material,
    _ym_theory_catalog,
    build_acceptance_report,
    expected_current_frontier_provenance,
)


REQUIRED_PRIMITIVES = {
    "regulated Yang-Mills presentation",
    "spectral-scale production witness",
    "observable-completeness witness",
    "descent-stability witness",
    "spectral-descent transport groupoid",
    "transport holonomy defect",
}
REQUIRED_RELATIONS = {
    "produces_scale_on",
    "detects_nonvacuum_sector",
    "transports_observable_semantics",
    "satisfies_descent_cocycle",
    "measures_holonomy_defect",
}


class CanonicalValidationError(RuntimeError):
    """Raised on one broken committed target invariant."""


def _timestamp(value: Any, label: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise CanonicalValidationError(f"{label} is not an ISO date-time") from exc
    if parsed.tzinfo is None:
        raise CanonicalValidationError(f"{label} must be timezone-aware")
    return parsed.astimezone(dt.timezone.utc)


def _validate_freshness_at_execution(
    projection: Mapping[str, Any], manifest: Mapping[str, Any]
) -> dict[str, str]:
    """Prove historical consumption was live without using today's clock."""

    literature = projection.get("literature_basis", {})
    if (
        literature.get("mode") != "active_current"
        or literature.get("active_investment_allowed") is not True
        or literature.get("policy") != "search_completion_bounded_consumption_v1"
    ):
        raise CanonicalValidationError(
            "historical replay lacks an active-current execution basis"
        )
    completed = _timestamp(
        literature.get("search_completed_at"), "literature search completion"
    )
    consume_before = _timestamp(
        literature.get("consume_before"), "literature consume-before deadline"
    )
    committed = _timestamp(manifest.get("created_at"), "canonical commit time")
    event_times = [
        _timestamp(row.get("occurred_at"), "canonical event time")
        for row in projection.get("events", [])
        if isinstance(row, Mapping)
    ]
    if not event_times:
        raise CanonicalValidationError("historical replay has no timed canonical events")
    if not (
        completed <= min(event_times)
        and max(event_times) <= committed
        and committed <= consume_before
    ):
        raise CanonicalValidationError(
            "canonical theory consumption did not occur inside the sealed literature window"
        )
    return {
        "freshness_at_execution": "active_current",
        "search_completed_at": literature["search_completed_at"],
        "consume_before": literature["consume_before"],
        "committed_at": str(manifest["created_at"]),
    }


def present_investment_freshness(
    consume_before: str,
    *,
    search_completed_at: str | None = None,
    now: dt.datetime | None = None,
) -> str:
    """Return a live investment status without changing historical evidence."""

    instant = now or dt.datetime.now(dt.timezone.utc)
    if instant.tzinfo is None:
        raise CanonicalValidationError("investment freshness clock must be timezone-aware")
    normalized = instant.astimezone(dt.timezone.utc)
    if search_completed_at is not None and normalized < _timestamp(
        search_completed_at, "literature search completion"
    ):
        return "clock_precedes_search_completion"
    return (
        "fresh_for_new_investment"
        if normalized <= _timestamp(consume_before, "literature consume-before deadline")
        else "refresh_required_before_new_investment"
    )


def _expected_frozen_provenance() -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        return expected_current_frontier_provenance()
    except Exception as exc:
        raise CanonicalValidationError(
            f"current acquisition provenance is unavailable or invalid: {exc}"
        ) from exc


def _validated_frozen_provenance(output_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    expected_catalog, expected_binding = _expected_frozen_provenance()
    source_catalog = _object(output_root / "frozen_provider_source_catalog.json")
    if source_catalog != expected_catalog:
        raise CanonicalValidationError("frozen provider source catalog drift")
    capture_binding = _object(output_root / "frozen_live_capture_binding.json")
    if capture_binding != expected_binding:
        raise CanonicalValidationError("captured external search provenance drift")
    return source_catalog, capture_binding


def _artifact_roles_from_commit(operator_evidence: Mapping[str, Any]) -> dict[str, Any]:
    grouped: dict[str, list[tuple[int, str]]] = {}
    for binding in operator_evidence.get("role_bindings", []):
        grouped.setdefault(str(binding["role"]), []).append(
            (int(binding["role_index"]), str(binding["original_path"]))
        )
    roles: dict[str, Any] = {}
    for role, indexed_paths in grouped.items():
        indexed_paths.sort()
        if [index for index, _ in indexed_paths] != list(range(len(indexed_paths))):
            raise CanonicalValidationError(f"role publication indices drift: {role}")
        paths = [path for _, path in indexed_paths]
        roles[role] = paths[0] if len(paths) == 1 else paths
    return roles


def _validate_publication_status(
    output_root: Path,
    projection: Mapping[str, Any],
    authorization: Mapping[str, Any],
) -> dict[str, Any]:
    status_path = output_root / PUBLICATION_STATUS_NAME
    if not os.path.lexists(status_path) or status_path.is_symlink() or not status_path.is_file():
        raise CanonicalValidationError("publication status is absent or unsafe")
    status = _object(status_path)
    validate_payload(status, "ym_canonical_publication_status.schema.json")
    if status_path.read_bytes() != canonical_json(status) + b"\n":
        raise CanonicalValidationError("publication status bytes are not canonical")
    if (
        status.get("target_id") != TARGET_ID
        or status.get("run_id") != RUN_ID
        or status.get("cycle_id") != projection["cycle_id"]
        or status.get("commit_id") != projection["commit_id"]
        or status.get("manifest_digest") != projection["manifest_digest"]
        or status.get("state_digest") != projection["state_digest"]
        or status.get("core_validation_authorization_basis_digest")
        != authorization["authorization_basis_digest"]
        or status.get("core_validation_present_decision_digest")
        != authorization["present_investment_decision_digest"]
        or status.get("content_digest")
        != canonical_digest(status, exclude_keys=("content_digest",))
    ):
        raise CanonicalValidationError("publication status crossed its committed core")
    expected_files: list[dict[str, Any]] = []
    for relative in sorted(PUBLICATION_FILE_ROLES):
        path = safe_relative_path(relative, output_root)
        if path.is_symlink() or not path.is_file():
            raise CanonicalValidationError(f"publication file is absent or unsafe: {relative}")
        expected_files.append(
            {
                "path": relative,
                "sha256": file_digest(path),
                "size_bytes": path.stat().st_size,
                "role": PUBLICATION_FILE_ROLES[relative],
            }
        )
    if status.get("files") != expected_files:
        raise CanonicalValidationError("publication file descriptor set drift")
    expected_publication_id = stable_identifier(
        "ympub",
        TARGET_ID,
        RUN_ID,
        projection["cycle_id"],
        projection["commit_id"],
        projection["manifest_digest"],
        projection["state_digest"],
        authorization["authorization_basis_digest"],
        canonical_digest(expected_files),
    )
    if status.get("publication_id") != expected_publication_id:
        raise CanonicalValidationError("publication identifier did not bind its file descriptor set")
    return status


def _validate_publication_failures(
    output_root: Path, projection: Mapping[str, Any]
) -> list[str]:
    directory = output_root / PUBLICATION_FAILURE_DIR
    if not os.path.lexists(directory):
        return []
    if directory.is_symlink() or not directory.is_dir():
        raise CanonicalValidationError("publication failure directory is unsafe")
    result_digest = file_digest(output_root / "canonical_cycle_result.json")
    failure_ids: list[str] = []
    for path in sorted(directory.iterdir(), key=lambda item: item.name):
        if path.is_symlink() or not path.is_file() or path.suffix != ".json":
            raise CanonicalValidationError("publication failure directory contains an unsafe entry")
        payload = _object(path)
        validate_payload(payload, "ym_canonical_publication_failure.schema.json")
        if path.read_bytes() != canonical_json(payload) + b"\n":
            raise CanonicalValidationError("publication failure receipt bytes are not canonical")
        expected_id = stable_identifier(
            "ympubfail",
            projection["cycle_id"],
            projection["commit_id"],
            payload["failed_stage"],
            payload["error_class"],
            payload["error_message"],
            result_digest,
        )
        if (
            path.name != f"{expected_id}.json"
            or payload.get("failure_id") != expected_id
            or payload.get("target_id") != TARGET_ID
            or payload.get("run_id") != RUN_ID
            or payload.get("cycle_id") != projection["cycle_id"]
            or payload.get("commit_id") != projection["commit_id"]
            or payload.get("canonical_result_digest") != result_digest
            or payload.get("content_digest")
            != canonical_digest(payload, exclude_keys=("content_digest",))
        ):
            raise CanonicalValidationError("publication failure receipt crossed its committed core")
        failure_ids.append(expected_id)
    return failure_ids


def _object(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise CanonicalValidationError(f"expected JSON object: {path}")
    return payload


def _committed_object(
    commit_path: Path, projection: Mapping[str, Any], artifact_role: str
) -> dict[str, Any]:
    relative = projection.get("artifact_paths", {}).get(artifact_role)
    if not isinstance(relative, str):
        raise CanonicalValidationError(f"verified projection omits committed role {artifact_role}")
    return _object(commit_path / "artifacts" / safe_relative_path(relative))


def _role_payloads(
    commit_path: Path,
    projection: Mapping[str, Any],
    operator_evidence: Mapping[str, Any],
    role: str,
) -> list[dict[str, Any]]:
    rows = sorted(
        (
            dict(binding)
            for binding in operator_evidence.get("role_bindings", [])
            if binding.get("role") == role
        ),
        key=lambda row: int(row["role_index"]),
    )
    if [int(row["role_index"]) for row in rows] != list(range(len(rows))):
        raise CanonicalValidationError(f"committed role indices are not contiguous: {role}")
    payloads = []
    for row in rows:
        artifact_role = str(row["commit_artifact_role"])
        if projection.get("artifact_paths", {}).get(artifact_role) != row.get("sealed_path"):
            raise CanonicalValidationError(f"committed role binding crossed projection: {role}")
        payloads.append(_committed_object(commit_path, projection, artifact_role))
    return payloads


def _operator_input(
    commit_path: Path,
    projection: Mapping[str, Any],
    operator_evidence: Mapping[str, Any],
    operator_id: str,
) -> dict[str, Any]:
    requests = [
        row
        for row in operator_evidence.get("operator_requests", [])
        if row.get("operator", {}).get("operator_id") == operator_id
    ]
    if len(requests) != 1:
        raise CanonicalValidationError(f"expected one committed request for {operator_id}")
    request_id = requests[0]["request_id"]
    bindings = sorted(
        (
            row
            for row in operator_evidence.get("input_bindings", [])
            if row.get("request_id") == request_id
        ),
        key=lambda row: int(row["input_index"]),
    )
    if len(bindings) != 1 or int(bindings[0]["input_index"]) != 0:
        raise CanonicalValidationError(f"expected one sealed input for {operator_id}")
    return _committed_object(
        commit_path, projection, str(bindings[0]["commit_artifact_role"])
    )


def _assert_material_transition(
    parent: Mapping[str, Any], synthesis: Mapping[str, Any], evidence: Mapping[str, Any]
) -> None:
    parent_structure = conceptual_structure_projection(
        parent["conceptual_systems"], parent["reflection_rounds"]
    )
    synthesis_structure = conceptual_structure_projection(
        synthesis["conceptual_systems"], synthesis["reflection_rounds"]
    )
    if canonical_digest(parent_structure) == canonical_digest(synthesis_structure):
        raise CanonicalValidationError("synthesis has no decision-bearing conceptual change")
    if (
        len(parent["reflection_rounds"]) != 3
        or len(synthesis["reflection_rounds"]) != 4
        or synthesis["reflection_rounds"][:3] != parent["reflection_rounds"]
        or evidence.get("stage_comparison", {}).get("material") is not True
        or evidence.get("stage_comparison", {}).get("new_reflection_rounds") != 1
    ):
        raise CanonicalValidationError("synthesis is not an exact one-round material extension")


def _require_phrases(value: str, phrases: Sequence[str], *, carrier: str) -> None:
    lowered = value.lower()
    missing = [phrase for phrase in phrases if phrase.lower() not in lowered]
    if missing:
        raise CanonicalValidationError(
            f"probe-driven {carrier} lacks target-relevant semantic carriers: {missing}"
        )


def _validate_probe_semantic_patch(
    synthesis: Mapping[str, Any], evidence: Mapping[str, Any]
) -> None:
    """Reject exact-but-irrelevant links in the target's probe maturation.

    The generic adjudicator proves referential integrity.  This target-specific
    check adds the narrower Yang--Mills meaning test: the objection must concern
    unequal path products, the correction must demand independent common-
    endpoint comparison, and the changed F05/F07/C04 obligations must retain
    local composition and holonomy as separate burdens.
    """

    selected_id = str(evidence.get("preferred_system_id", ""))
    selected = next(
        (
            row
            for row in synthesis.get("conceptual_systems", [])
            if row.get("system_id") == selected_id
        ),
        None,
    )
    if selected is None:
        raise CanonicalValidationError("probe semantic patch cannot resolve the selected system")
    comparison = evidence.get("stage_comparison", {})
    semantic_patch = comparison.get("semantic_patch", {})
    links = semantic_patch.get("objection_links", [])
    final_round = synthesis.get("reflection_rounds", [])[-1]
    raw_links = final_round.get("semantic_patch_links", [])
    if (
        len(links) != 1
        or len(raw_links) != 1
        or set(raw_links[0].get("changed_paths", []))
        != {"/formalization_seeds", "/correction_conditions"}
    ):
        raise CanonicalValidationError("probe mutation lacks one exact two-path semantic link")
    _require_phrases(
        str(raw_links[0].get("objection", "")),
        ("unequal path factors", "multiplicative composition", "path-independent descent"),
        carrier="objection",
    )
    _require_phrases(
        str(raw_links[0].get("correction_test", "")),
        ("independently admissible paths", "common endpoints", "holonomy defect", "separate obligation"),
        carrier="correction test",
    )
    formalization = {
        str(item).split(":", 1)[0]: str(item)
        for item in selected.get("formalization_seeds", [])
    }
    corrections = {
        str(item).split(":", 1)[0]: str(item)
        for item in selected.get("correction_conditions", [])
    }
    _require_phrases(
        formalization.get("YM21-F05", ""),
        ("typed local inequality", "no composite law", "separate comparison theorem"),
        carrier="F05 obligation",
    )
    _require_phrases(
        formalization.get("YM21-F07", ""),
        ("independently admissible", "common-endpoint", "holonomy defect", "cutoff-uniform"),
        carrier="F07 obligation",
    )
    _require_phrases(
        corrections.get("YM21-C04", ""),
        ("independently admissible", "common-endpoint", "nonzero", "local composition laws alone"),
        carrier="C04 correction",
    )


def validate_material_reflective_transition(
    parent: Mapping[str, Any], synthesis: Mapping[str, Any]
) -> None:
    """Publicly validate the exact parent-to-synthesis target transition."""

    parent_evidence_rows = parent.get("independent_evaluation_evidence", [])
    synthesis_evidence_rows = synthesis.get("independent_evaluation_evidence", [])
    if len(parent_evidence_rows) != 1 or len(synthesis_evidence_rows) != 1:
        raise CanonicalValidationError("material transition requires one evidence packet per stage")
    parent_evidence = parent_evidence_rows[0]
    synthesis_evidence = synthesis_evidence_rows[0]
    for packet, evidence in (
        (parent, parent_evidence),
        (synthesis, synthesis_evidence),
    ):
        projection = conceptual_structure_projection(
            packet.get("conceptual_systems", []), packet.get("reflection_rounds", [])
        )
        if canonical_digest(projection) != evidence.get("input_binding", {}).get(
            "conceptual_structure_digest"
        ):
            raise CanonicalValidationError(
                "reflective packet differs from its bound conceptual evidence"
            )
    selected_id = str(synthesis_evidence.get("preferred_system_id", ""))
    before = next(
        (
            row
            for row in parent.get("conceptual_systems", [])
            if row.get("system_id") == selected_id
        ),
        None,
    )
    after = next(
        (
            row
            for row in synthesis.get("conceptual_systems", [])
            if row.get("system_id") == selected_id
        ),
        None,
    )
    if before is None or after is None:
        raise CanonicalValidationError("material transition does not preserve the selected system")
    try:
        validate_material_system_transition(
            previous_evidence=parent_evidence,
            current_evidence=synthesis_evidence,
            before_system=before,
            after_system=after,
        )
    except ContractError as exc:
        raise CanonicalValidationError(f"invalid semantic maturation: {exc}") from exc
    _assert_material_transition(parent, synthesis, synthesis_evidence)
    _validate_probe_semantic_patch(synthesis, synthesis_evidence)


def _validate_conceptual_evidence(
    *,
    inputs: Sequence[Mapping[str, Any]],
    packets: Sequence[Mapping[str, Any]],
    snapshot: Mapping[str, Any],
) -> list[dict[str, Any]]:
    evidence_rows: list[dict[str, Any]] = []
    previous: Mapping[str, Any] | None = None
    for index, (envelope, packet) in enumerate(zip(inputs, packets, strict=True)):
        bound = envelope.get("independent_evaluation_evidence")
        if not isinstance(bound, list) or len(bound) != 1 or not isinstance(bound[0], Mapping):
            raise CanonicalValidationError("reflective input lacks one exact conceptual evidence packet")
        evidence = dict(bound[0])
        systems = envelope.get("conceptual_systems")
        rounds = envelope.get("reflection_rounds")
        if not isinstance(systems, list) or not isinstance(rounds, list):
            raise CanonicalValidationError("reflective input lacks systems or rounds")
        validate_conceptual_quality_evidence(
            evidence,
            systems=systems,
            rounds=rounds,
            snapshot=snapshot,
            previous_evidence=previous,
        )
        receipt = evidence["evaluation_receipt"]
        validate_evaluation_receipt(receipt)
        if packet.get("independent_evaluation_evidence") != [evidence]:
            raise CanonicalValidationError("reflective output changed its exact conceptual evidence")
        if packet.get("evaluation_receipt_ids") != [receipt["evaluation_id"]]:
            raise CanonicalValidationError("reflective output changed the evaluation identity")
        if packet.get("generation_mode") != "operator_generated":
            raise CanonicalValidationError("YM reflective packet used an unapproved generation mode")
        expected_role = "diagnostic" if index == 0 else "conceptual_gate"
        if evidence.get("evaluation_role") != expected_role:
            raise CanonicalValidationError("conceptual evidence role/order mismatch")
        if set(evidence.get("gate_findings", {})) != set(CONCEPTUAL_GATE_IDS):
            raise CanonicalValidationError("conceptual evidence omits a G0--G6 gate")
        if index == 1 and any(
            evidence["gate_findings"][gate_id].get("status") != "pass"
            for gate_id in CONCEPTUAL_GATE_IDS
        ):
            raise CanonicalValidationError("synthesis conceptual gate vector does not fully pass")
        if canonical_digest(
            conceptual_structure_projection(packet["conceptual_systems"], packet["reflection_rounds"])
        ) != evidence["input_binding"]["conceptual_structure_digest"]:
            raise CanonicalValidationError("operator output changed the adjudicated conceptual structure")
        evidence_rows.append(evidence)
        previous = evidence
    return evidence_rows


def _validate_selected_system(
    packets: Sequence[Mapping[str, Any]], evidence_rows: Sequence[Mapping[str, Any]]
) -> str:
    selected_ids = {str(row["preferred_system_id"]) for row in evidence_rows}
    if len(selected_ids) != 1:
        raise CanonicalValidationError("blind parent/synthesis adjudications selected different systems")
    selected_id = next(iter(selected_ids))
    for packet in packets:
        selected = next(
            (row for row in packet["conceptual_systems"] if row["system_id"] == selected_id),
            None,
        )
        if selected is None:
            raise CanonicalValidationError("blind selected system is absent from a reflective packet")
        if not REQUIRED_PRIMITIVES.issubset(set(selected["primitives"])):
            raise CanonicalValidationError("selected mediator lacks a YM scale/detection/descent primitive")
        if not REQUIRED_RELATIONS.issubset(set(selected["relations_operations_and_dynamics"])):
            raise CanonicalValidationError("selected mediator lacks a YM scale/detection/descent relation")
        formal_ids = {
            str(item).split(":", 1)[0] for item in selected["formalization_seeds"]
        }
        correction_ids = {
            str(item).split(":", 1)[0] for item in selected["correction_conditions"]
        }
        if formal_ids != REQUIRED_FORMALIZATION_IDS or correction_ids != REQUIRED_CORRECTION_IDS:
            raise CanonicalValidationError("selected mediator lacks the exact F01--F09/C01--C06 programme")
        if len(selected["unification_claims"]["differences_preserved"]) < 5:
            raise CanonicalValidationError("selected mediator erases a non-substitutable proof burden")
    return selected_id


def _validate_experiment(
    spec: Mapping[str, Any],
    experiment: Mapping[str, Any],
    reflection: Mapping[str, Any],
    parent: Mapping[str, Any],
    synthesis: Mapping[str, Any],
    synthesis_operator_receipt: Mapping[str, Any],
) -> None:
    """Replay the exact current experiment and its executed reflective return."""

    validate_experiment_receipt(experiment, spec)
    validate_experiment_reflection_receipt(
        reflection,
        spec,
        experiment,
        parent,
        synthesis,
        synthesis_operator_receipt,
    )
    if (
        experiment.get("source_reflection_packet_digest") != parent.get("packet_digest")
        or experiment.get("source_theory_programme_digest")
        != canonical_digest(parent["theoretical_programme"])
    ):
        raise CanonicalValidationError("experiment is not commissioned by the exact parent theory bytes")
    result = experiment.get("result", {})
    exact = result.get("exact_values", {}) if isinstance(result, Mapping) else {}
    certificate = experiment.get("certificate", {})
    if (
        experiment.get("status") != "counterexample"
        or experiment.get("epistemic_outcome") != "falsifies_claim"
        or result.get("claim_holds") is not False
        or exact != {"left": "1/2", "right": "5/8", "difference": "-1/8"}
        or certificate.get("left") != "1/2"
        or certificate.get("right") != "5/8"
        or certificate.get("difference") != "-1/8"
    ):
        raise CanonicalValidationError("experiment lacks the exact preregistered path counterexample")
    if not experiment.get("transfer_boundary", "").startswith(
        "The certificate concerns one rational toy"
    ):
        raise CanonicalValidationError("experiment escaped its finite non-YM transfer boundary")
    final_round = synthesis["reflection_rounds"][-1]
    if (
        experiment.get("receipt_id") not in synthesis["support_probe"]["receipt_ids"]
        or "1/2" not in " ".join(final_round["strongest_objections"])
        or "5/8" not in " ".join(final_round["strongest_objections"])
    ):
        raise CanonicalValidationError("synthesis did not assimilate the exact counterexample")


def _expected_ranked_impacts(
    portfolio: Mapping[str, Any], assimilation: Mapping[str, Any]
) -> list[dict[str, Any]]:
    event_weight = {
        "demote": 9,
        "split": 8,
        "new_question": 7,
        "reframe": 6,
        "reprioritize": 5,
    }
    confidence_weight = {"high": 3, "medium": 2, "low": 1, "unknown": 0}
    mappings = list(assimilation.get("theory_mappings", []))
    rows = []
    for seed in portfolio["parallel_branch_seeds"]:
        hypothesis_id = str(seed["hypothesis_id"])
        impacts = [
            row for row in mappings if hypothesis_id in row.get("theory_object_ids", [])
        ]
        source_ids = sorted({str(row["source_id"]) for row in impacts})
        rows.append(
            {
                "hypothesis_id": hypothesis_id,
                "branch_id": seed["branch_id"],
                "corner_family": seed["corner_family"],
                "is_wildcard": bool(seed.get("is_wildcard")),
                "impact_score": sum(
                    event_weight.get(str(row.get("event_type")), 1)
                    + confidence_weight.get(str(row.get("confidence")), 0)
                    for row in impacts
                )
                + 2 * len(source_ids)
                + len({str(row.get("event_type")) for row in impacts}),
                "source_ids": source_ids,
                "mapping_ids": sorted(str(row["mapping_id"]) for row in impacts),
            }
        )
    return sorted(rows, key=lambda row: (-row["impact_score"], row["hypothesis_id"]))


def _expected_selection(ranked: Sequence[Mapping[str, Any]], *, count: int = 4) -> list[str]:
    chosen = [dict(row) for row in ranked if not row["is_wildcard"]][: count - 1]
    used = {str(row["hypothesis_id"]) for row in chosen}
    wildcard = next(
        (
            dict(row)
            for row in ranked
            if row["is_wildcard"] and str(row["hypothesis_id"]) not in used
        ),
        None,
    )
    if wildcard is not None:
        chosen.append(wildcard)
    for row in ranked:
        if len(chosen) >= count:
            break
        if str(row["hypothesis_id"]) not in {
            str(item["hypothesis_id"]) for item in chosen
        }:
            chosen.append(dict(row))
    return [str(row["hypothesis_id"]) for row in chosen]


def _expected_branch_projection(
    selected_ids: Sequence[str],
    portfolio: Mapping[str, Any],
    assimilation: Mapping[str, Any],
) -> dict[str, Any]:
    by_id = {
        str(row["hypothesis_id"]): row for row in portfolio["parallel_branch_seeds"]
    }
    mappings = list(assimilation.get("theory_mappings", []))
    rows = []
    for hypothesis_id in selected_ids:
        seed = by_id[hypothesis_id]
        impacts = [
            row for row in mappings if hypothesis_id in row.get("theory_object_ids", [])
        ]
        source_ids = sorted({str(row["source_id"]) for row in impacts})
        limitations = sorted({str(row["source_limitation"]) for row in impacts})
        changed_question = (
            "Which explicit mediator and correction condition would make this branch answer: "
            + str(seed["maturation_question"])
            + (
                " under the exact source limitations " + " | ".join(limitations)
                if limitations
                else " when no literature-derived constraint is available"
            )
        )
        rows.append(
            {
                "hypothesis_id": hypothesis_id,
                "branch_id": seed["branch_id"],
                "mechanism_key": f"matured-{seed['mechanism_key']}",
                "source_ids": source_ids,
                "changed_question": changed_question,
                "new_explanatory_dependency": {
                    "source": seed["mechanism_key"],
                    "relation": "must_be_mediated_by",
                    "target": seed["unique_primitives"][0],
                },
                "correction_condition": (
                    "The carrier must remain testable without assuming the Yang--Mills target conclusion."
                ),
            }
        )
    programme = {
        "selected_hypothesis_ids": [row["hypothesis_id"] for row in rows],
        "changed_questions": [row["changed_question"] for row in rows],
        "dependencies": [row["new_explanatory_dependency"] for row in rows],
        "correction_conditions": [row["correction_condition"] for row in rows],
    }
    return {
        "branch_results": rows,
        "branch_results_digest": canonical_digest(rows),
        "programme_projection": programme,
        "programme_digest": canonical_digest(programme),
    }


def _validate_route_packet(
    route: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    portfolio: Mapping[str, Any],
    *,
    require_source_removals: bool,
) -> list[str]:
    if route.get("content_digest") != canonical_digest(
        {key: value for key, value in route.items() if key != "content_digest"}
    ):
        raise CanonicalValidationError("literature routing trace digest mismatch")
    if route.get("assimilation_digest") != canonical_digest(assimilation):
        raise CanonicalValidationError("literature routing trace crossed assimilation bytes")
    if route.get("portfolio_digest") != canonical_digest(portfolio):
        raise CanonicalValidationError("literature routing trace crossed portfolio bytes")
    ranked = _expected_ranked_impacts(portfolio, assimilation)
    selected = _expected_selection(ranked)
    if route.get("ranked_impacts") != ranked or route.get("selected_hypothesis_ids") != selected:
        raise CanonicalValidationError("literature routing is not the registered content-derived ranking")
    counterfactuals = route.get("source_removal_counterfactuals", [])
    if require_source_removals:
        mapping_sources = sorted(
            {str(row["source_id"]) for row in assimilation.get("theory_mappings", [])}
        )
        if [row.get("removed_source_id") for row in counterfactuals] != mapping_sources:
            raise CanonicalValidationError("mapping-removal counterfactual coverage drift")
        by_source = {source: [] for source in mapping_sources}
        for source in mapping_sources:
            reduced = {
                **assimilation,
                "theory_mappings": [
                    row
                    for row in assimilation.get("theory_mappings", [])
                    if row["source_id"] != source
                ],
            }
            by_source[source] = _expected_ranked_impacts(portfolio, reduced)
        for row in counterfactuals:
            reranked = by_source[str(row["removed_source_id"])]
            counterfactual_ids = _expected_selection(reranked)
            if (
                row.get("selected_hypothesis_ids") != counterfactual_ids
                or row.get("route_changed") is not (counterfactual_ids != selected)
                or row.get("baseline_rank") != [item["hypothesis_id"] for item in ranked]
                or row.get("counterfactual_rank")
                != [item["hypothesis_id"] for item in reranked]
            ):
                raise CanonicalValidationError("mapping-removal routing replay drift")
    elif counterfactuals or route.get("source_removal_changes_route") is not False:
        raise CanonicalValidationError("nested full replay contains undeclared routing sub-replays")
    if route.get("source_removal_changes_route") is not any(
        row.get("route_changed") is True for row in counterfactuals
    ):
        raise CanonicalValidationError("mapping-removal routing sensitivity summary drift")
    return selected


def _validate_routing(
    trace: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    portfolio: Mapping[str, Any],
    parallel: Mapping[str, Any],
    theory_catalog: Mapping[str, Any],
    hypotheses: Sequence[Mapping[str, Any]],
) -> None:
    selected_ids = _validate_route_packet(
        trace, assimilation, portfolio, require_source_removals=True
    )
    selected = {str(row["hypothesis_id"]) for row in parallel["branch_requests"]}
    if selected != set(selected_ids):
        raise CanonicalValidationError("parallel wave differs from mapping-derived routing")
    worlds = _literature_counterfactual_worlds(snapshot)
    generic_replay = trace.get("literature_counterfactual_replay")
    if not isinstance(generic_replay, Mapping):
        raise CanonicalValidationError("routing trace lacks generic derivational replay")
    declared_worlds = {str(row["world_id"]): dict(row) for row in worlds}
    replayed_worlds = {
        str(row["world_id"]): {
            "world_id": row["world_id"],
            **row["transformation"],
            "expected_effect": row["evaluation"]["expected_effect"],
        }
        for row in generic_replay.get("world_results", [])
    }
    if replayed_worlds != declared_worlds:
        raise CanonicalValidationError("target literature replay world schedule drift")
    validate_literature_counterfactual_replay(
        generic_replay,
        snapshot=snapshot,
        theory_catalog=theory_catalog,
        hypotheses=hypotheses,
    )
    if generic_replay["baseline"]["assimilation"] != assimilation:
        raise CanonicalValidationError("committed assimilation crossed replay baseline")
    generic_by_id = {
        str(row["world_id"]): row for row in generic_replay["world_results"]
    }
    rows = trace.get("full_pipeline_replays", [])
    if (
        trace.get("counterfactual_replay_mode")
        != "derived_claim_mapping_full_pipeline_local_only"
        or trace.get("required_replay_operations")
        != [
            "delete_source",
            "no_literature",
            "supersede_source",
            "contradict_source",
            "coverage_only_change",
        ]
        or trace.get("all_scenarios_reexecuted") is not True
        or len(rows) != len(worlds)
        or {str(row.get("world_id")) for row in rows} != set(generic_by_id)
        or trace.get("null_effect_world_ids")
        != generic_replay.get("null_effect_world_ids")
    ):
        raise CanonicalValidationError("full literature counterfactual coverage drift")
    baseline_projection = _expected_branch_projection(selected_ids, portfolio, assimilation)
    if trace.get("baseline_branch_projection") != baseline_projection:
        raise CanonicalValidationError("baseline branch maturation projection drift")
    selection_changes: list[str] = []
    programme_changes: list[str] = []
    for row in rows:
        world_id = str(row["world_id"])
        generic_world = generic_by_id[world_id]
        counterfactual_snapshot = generic_world["snapshot"]
        counterfactual_assimilation = generic_world["assimilation"]
        route = row.get("route")
        if not isinstance(route, Mapping):
            raise CanonicalValidationError("full literature replay lacks typed stage artifacts")
        validate_snapshot(counterfactual_snapshot)
        validate_assimilation(counterfactual_assimilation, snapshot=counterfactual_snapshot)
        if (
            row.get("operation") != generic_world["transformation"]["operation"]
            or row.get("generic_world_digest") != generic_world["content_digest"]
            or counterfactual_snapshot.get("provenance_mode") != "local_only"
            or any(
                item.get("execution_mode") != "local_only"
                or item.get("status") != "completed"
                for item in counterfactual_snapshot["lane_receipts"]
            )
        ):
            raise CanonicalValidationError(f"counterfactual snapshot semantics drift: {world_id}")
        replay_selected = _validate_route_packet(
            route, counterfactual_assimilation, portfolio, require_source_removals=False
        )
        projection = _expected_branch_projection(
            replay_selected, portfolio, counterfactual_assimilation
        )
        selection_changed = replay_selected != selected_ids
        questions_changed = (
            projection["branch_results_digest"]
            != baseline_projection["branch_results_digest"]
        )
        programme_changed = (
            projection["programme_digest"] != baseline_projection["programme_digest"]
        )
        if (
            row.get("selected_hypothesis_ids") != replay_selected
            or row.get("branch_projection") != projection
            or row.get("selection_changed") is not selection_changed
            or row.get("questions_changed") is not questions_changed
            or row.get("programme_changed") is not programme_changed
        ):
            raise CanonicalValidationError(f"counterfactual branch replay drift: {world_id}")
        if selection_changed:
            selection_changes.append(world_id)
        if programme_changed:
            programme_changes.append(world_id)
    if (
        trace.get("selection_change_scenarios") != sorted(selection_changes)
        or trace.get("programme_change_scenarios") != sorted(programme_changes)
        or not programme_changes
    ):
        raise CanonicalValidationError("full literature causal-sensitivity summary drift")


def validate(
    output_root: Path = REGISTERED_RUNTIME_ROOT,
    *,
    require_publication: bool = True,
    historical_replay: bool = False,
    cycle_path: Path | None = None,
    state_root: Path | None = None,
) -> dict[str, Any]:
    output_root = output_root.resolve()
    projection_path = (
        cycle_path.resolve()
        if cycle_path is not None
        else output_root / "canonical_cycle_result.json"
    )
    resolved_state_root = (
        state_root.resolve() if state_root is not None else output_root / "state"
    )
    projection = _object(projection_path)

    # This must happen before any target semantics are read.  It verifies the
    # exact projection, manifest, CAS state, event replay, all sealed inputs and
    # outputs, validator authority bytes, role bijections, and feedback lineage.
    authorization = verify_canonical_theory_cycle(
        projection_path,
        target_id=TARGET_ID,
        run_id=RUN_ID,
        state_root=resolved_state_root,
        require_current=not historical_replay,
    )
    commit_path = Path(authorization["commit_path"])
    commit_manifest = _object(Path(authorization["manifest_path"]))
    execution_freshness = _validate_freshness_at_execution(
        projection, commit_manifest
    )
    operator_evidence = _committed_object(
        commit_path, projection, "operator_evidence"
    )

    requests = operator_evidence["operator_requests"]
    receipts = operator_evidence["operator_receipts"]
    operator_ids = {
        row["operator"]["operator_id"]
        for row in receipts
        if row.get("status") == "succeeded"
    }
    if len(requests) != 6 or len(receipts) != 6 or operator_ids != SIX_OPERATORS:
        raise CanonicalValidationError("canonical YM wave is not the exact six-operator wave")

    snapshot_rows = _role_payloads(commit_path, projection, operator_evidence, "literature_snapshot")
    assimilation_rows = _role_payloads(commit_path, projection, operator_evidence, "literature_assimilation")
    portfolio_rows = _role_payloads(commit_path, projection, operator_evidence, "high_risk_portfolio")
    parallel_rows = _role_payloads(commit_path, projection, operator_evidence, "parallel_portfolio")
    packets = _role_payloads(commit_path, projection, operator_evidence, "reflective_packets")
    experiment_spec_rows = _role_payloads(
        commit_path, projection, operator_evidence, "experiment_spec"
    )
    experiment_rows = _role_payloads(
        commit_path, projection, operator_evidence, "experiment_receipt"
    )
    if not all(
        len(rows) == 1
        for rows in (
            snapshot_rows,
            assimilation_rows,
            portfolio_rows,
            parallel_rows,
            experiment_spec_rows,
            experiment_rows,
        )
    ) or len(packets) != 2:
        raise CanonicalValidationError("committed YM semantic-role cardinality drift")
    snapshot, assimilation, portfolio, parallel, experiment_spec, experiment = (
        snapshot_rows[0],
        assimilation_rows[0],
        portfolio_rows[0],
        parallel_rows[0],
        experiment_spec_rows[0],
        experiment_rows[0],
    )
    experiment_reflection = projection.get("experiment_reflection_receipt")
    if not isinstance(experiment_reflection, Mapping):
        raise CanonicalValidationError(
            "canonical YM cycle lacks its executed experiment reflection receipt"
        )
    synthesis_receipts = [
        row
        for row in receipts
        if row.get("operator", {}).get("operator_id")
        == "reflective-theory-synthesizer"
        and row.get("status") == "succeeded"
    ]
    if len(synthesis_receipts) != 1:
        raise CanonicalValidationError(
            "canonical YM cycle lacks one successful synthesis operator receipt"
        )
    parent_input = _operator_input(
        commit_path, projection, operator_evidence, "reflective-conceptual-discovery"
    )
    synthesis_input = _operator_input(
        commit_path, projection, operator_evidence, "reflective-theory-synthesizer"
    )
    literature_input = _operator_input(
        commit_path, projection, operator_evidence, "frontier-literature-assimilator"
    )
    expected_source_catalog, expected_capture_binding = _expected_frozen_provenance()
    if (
        literature_input.get("frozen_provider_source_catalog")
        != expected_source_catalog
        or literature_input.get("frozen_live_capture_binding")
        != expected_capture_binding
    ):
        raise CanonicalValidationError(
            "sealed literature input lacks exact frozen provider provenance"
        )

    validate_snapshot(snapshot)
    validate_assimilation(assimilation, snapshot=snapshot)
    theory_catalog = literature_input.get("theory_catalog")
    mapping_derivation = literature_input.get("mapping_derivation")
    hypotheses = literature_input.get("hypotheses")
    if not all(
        isinstance(item, (Mapping, list))
        for item in (theory_catalog, mapping_derivation, hypotheses)
    ):
        raise CanonicalValidationError(
            "literature operator input lacks catalog, derivation, or hypothesis rebase"
        )
    expected_catalog = _ym_theory_catalog(snapshot)
    if theory_catalog != expected_catalog:
        raise CanonicalValidationError("YM theory catalog did not derive from the target vocabulary")
    validate_theory_object_catalog(theory_catalog)
    validate_claim_mapping_derivation(
        mapping_derivation,
        snapshot=snapshot,
        theory_catalog=theory_catalog,
    )
    if mapping_derivation != derive_claim_mappings(
        snapshot, theory_catalog=theory_catalog
    ):
        raise CanonicalValidationError("literature mapping derivation replay drift")
    if hypotheses != _derived_hypothesis_rebase(mapping_derivation):
        raise CanonicalValidationError("hypothesis rebase was not derived from claim receipts")
    expected_assimilation = assimilate_derived_literature(
        snapshot,
        theory_catalog=theory_catalog,
        mapping_derivation=mapping_derivation,
        hypotheses=hypotheses,
        candidate_snapshot_ids=[snapshot["snapshot_id"]],
    )
    if assimilation != expected_assimilation:
        raise CanonicalValidationError("committed assimilation does not replay from derived claims")
    validate_high_risk_portfolio(portfolio, literature_snapshot=snapshot)
    validate_parallel_portfolio(parallel)
    for packet in packets:
        validate_payload(packet, "reflective_conceptual_discovery_packet.schema.json")
        validate_packet_invariants(packet)
    evidence_rows = _validate_conceptual_evidence(
        inputs=[parent_input, synthesis_input], packets=packets, snapshot=snapshot
    )
    selected_id = _validate_selected_system(packets, evidence_rows)
    validate_material_reflective_transition(packets[0], packets[1])
    _validate_experiment(
        experiment_spec,
        experiment,
        experiment_reflection,
        packets[0],
        packets[1],
        synthesis_receipts[0],
    )

    routing_trace = parent_input.get("literature_routing_trace")
    generation_trace = parent_input.get("conceptual_generation_trace")
    if not isinstance(routing_trace, Mapping) or not isinstance(generation_trace, Mapping):
        raise CanonicalValidationError("sealed reflection input lacks causal routing/generation traces")
    _validate_routing(
        routing_trace,
        snapshot,
        assimilation,
        portfolio,
        parallel,
        theory_catalog,
        hypotheses,
    )
    if (
        generation_trace.get("snapshot_digest") != snapshot["content_digest"]
        or generation_trace.get("assimilation_digest") != canonical_digest(assimilation)
        or generation_trace.get("portfolio_digest") != canonical_digest(portfolio)
        or generation_trace.get("parallel_digest") != canonical_digest(parallel)
        or generation_trace.get("generated_systems_digest")
        != canonical_digest(parent_input["conceptual_systems"])
        or generation_trace.get("parent_rounds_digest")
        != canonical_digest(parent_input["reflection_rounds"])
    ):
        raise CanonicalValidationError("conceptual generation trace crossed its exact causal inputs")

    if (
        projection.get("committed_state_version") != 1
        or projection.get("parallel_outcome", {}).get("canonical_cas_commits") != 1
        or projection.get("literature_basis", {}).get("mode") != "active_current"
        or projection.get("experiment_assimilation", {}).get("theory_selected") is not False
        or projection.get("experiment_assimilation", {}).get("proof_authorized") is not False
        or any(row.get("promotion_decision") != "not_requested" for row in projection["evaluation_receipts"])
    ):
        raise CanonicalValidationError("canonical result escaped one-commit/current-literature/no-promotion policy")

    core_summary = {
        "status": "validated_core" if not require_publication else "validated",
        "target_id": TARGET_ID,
        "run_id": RUN_ID,
        "cycle_id": projection["cycle_id"],
        "commit_id": projection["commit_id"],
        "committed_state_version": projection["committed_state_version"],
        "operator_receipts": len(receipts),
        "feedback_edges": len(projection["feedback_edges"]),
        "selected_system_id": selected_id,
        "literature_mode": projection["literature_basis"]["mode"],
        **execution_freshness,
        "experiment_outcome": experiment["epistemic_outcome"],
        "authorization_basis_digest": authorization["authorization_basis_digest"],
        "present_investment_decision_digest": authorization[
            "present_investment_decision_digest"
        ],
        "authority_boundary": (
            "Validation establishes exact committed protocol and target-specific conceptual consistency only; "
            "it does not validate source claims, autonomous discovery efficacy, a continuum construction, or a Yang--Mills mass gap."
        ),
    }
    if not require_publication:
        return core_summary

    # Report copies are non-authoritative, but if published they must equal the
    # exact evidence embedded in sealed operator inputs.
    for name, evidence in zip(
        (PARENT_CONCEPTUAL_QUALITY_EVIDENCE_NAME, SYNTHESIS_CONCEPTUAL_QUALITY_EVIDENCE_NAME),
        evidence_rows,
        strict=True,
    ):
        if _object(output_root / name) != evidence:
            raise CanonicalValidationError(f"published conceptual evidence copy drift: {name}")
    refinement = _object(output_root / CONCEPTUAL_QUALITY_REFINEMENT_HISTORY_NAME)
    if (
        refinement.get("parent_evidence_id") != evidence_rows[0]["evidence_id"]
        or refinement.get("synthesis_evidence_id") != evidence_rows[1]["evidence_id"]
        or refinement.get("probe_receipt_id") != experiment["receipt_id"]
        or refinement.get("stage_comparison") != evidence_rows[1]["stage_comparison"]
        or refinement.get("retained_dissent") is not True
    ):
        raise CanonicalValidationError("published refinement history crossed committed evidence")
    acceptance = _object(output_root / "acceptance_report.json")
    if acceptance.get("status") != "passed" or not all(acceptance.get("checks", {}).values()):
        raise CanonicalValidationError("acceptance report contains a failed check")
    required_checks = {
        "blind_plural_content_adjudication_and_full_synthesis_gates",
        "G2_G4_pass_from_bound_internal_correlated_evidence",
        "latest_literature_changed_parallel_priorities",
        "latest_literature_full_pipeline_counterfactual_replays",
        "experiment_remains_theory_subordinate",
        "six_feedback_edges_reachable",
        "operator_evidence_sealed",
    }
    if not required_checks.issubset(acceptance.get("checks", {})):
        raise CanonicalValidationError("acceptance report omits a target release check")

    source_catalog, capture_binding = _validated_frozen_provenance(output_root)
    expected_roles = _artifact_roles_from_commit(operator_evidence)
    if _object(output_root / "operator_requests.json") != {"requests": requests}:
        raise CanonicalValidationError("published operator request index drift")
    if _object(output_root / "operator_receipts.json") != {"receipts": receipts}:
        raise CanonicalValidationError("published operator receipt index drift")
    if _object(output_root / "artifact_roles.json") != expected_roles:
        raise CanonicalValidationError("published artifact role index drift")
    if (
        _object(output_root / "conceptual_generation_trace.json")
        != generation_trace
        or _object(output_root / "literature_routing_counterfactuals.json")
        != routing_trace
    ):
        raise CanonicalValidationError("published causal trace drift")
    expected_refinement = _refinement_history_from_committed_material(
        evidence_rows, experiment
    )
    if refinement != expected_refinement:
        raise CanonicalValidationError("published refinement history is not exact")
    expected_acceptance = build_acceptance_report(
        result=projection,
        requests=list(requests),
        receipts=list(receipts),
        snapshot=snapshot,
        assimilation=assimilation,
        portfolio=portfolio,
        parallel=parallel,
        experiment_receipt=experiment,
        capture_binding=capture_binding,
        literature_routing_trace=routing_trace,
        reflective_packets=packets,
        conceptual_quality_evidence=evidence_rows,
    )
    if acceptance != expected_acceptance:
        raise CanonicalValidationError("acceptance report did not replay from committed material")
    if (output_root / "acceptance_report.md").read_bytes() != _acceptance_markdown(
        expected_acceptance, projection
    ):
        raise CanonicalValidationError("acceptance Markdown did not replay byte-for-byte")
    if source_catalog != expected_source_catalog:
        raise CanonicalValidationError("published provider source catalog crossed sealed input")
    publication_status = _validate_publication_status(
        output_root, projection, authorization
    )
    publication_failure_ids = _validate_publication_failures(output_root, projection)

    if output_root == REGISTERED_RUNTIME_ROOT.resolve():
        runtime_binding = registered_runtime_binding_if_present()
        if runtime_binding is not None and _object(REGISTERED_RUNTIME_BINDING) != runtime_binding:
            raise CanonicalValidationError("registered canonical runtime binding is stale")

    return {
        **core_summary,
        "publication_id": publication_status["publication_id"],
        "publication_files": len(publication_status["files"]),
        "publication_failure_receipts": len(publication_failure_ids),
    }


def load_committed_publication_material(
    output_root: Path,
    *,
    historical_replay: bool = False,
    cycle_path: Path | None = None,
    state_root: Path | None = None,
) -> dict[str, Any]:
    """Return report inputs only after exact committed-core target replay."""

    output_root = output_root.resolve()
    projection_path = (
        cycle_path.resolve()
        if cycle_path is not None
        else output_root / "canonical_cycle_result.json"
    )
    resolved_state_root = (
        state_root.resolve() if state_root is not None else output_root / "state"
    )
    core_validation = validate(
        output_root,
        require_publication=False,
        historical_replay=historical_replay,
        cycle_path=projection_path,
        state_root=resolved_state_root,
    )
    projection = _object(projection_path)
    authorization = verify_canonical_theory_cycle(
        projection_path,
        target_id=TARGET_ID,
        run_id=RUN_ID,
        state_root=resolved_state_root,
        require_current=not historical_replay,
    )
    if (
        authorization["authorization_basis_digest"]
        != core_validation["authorization_basis_digest"]
    ):
        raise CanonicalValidationError(
            "publication replay immutable authorization basis changed between passes"
        )
    commit_path = Path(authorization["commit_path"])
    operator_evidence = _committed_object(
        commit_path, projection, "operator_evidence"
    )
    snapshot = _role_payloads(
        commit_path, projection, operator_evidence, "literature_snapshot"
    )[0]
    assimilation = _role_payloads(
        commit_path, projection, operator_evidence, "literature_assimilation"
    )[0]
    portfolio = _role_payloads(
        commit_path, projection, operator_evidence, "high_risk_portfolio"
    )[0]
    parallel = _role_payloads(
        commit_path, projection, operator_evidence, "parallel_portfolio"
    )[0]
    experiment = _role_payloads(
        commit_path, projection, operator_evidence, "experiment_receipt"
    )[0]
    experiment_spec = _role_payloads(
        commit_path, projection, operator_evidence, "experiment_spec"
    )[0]
    experiment_reflection = projection.get("experiment_reflection_receipt")
    if not isinstance(experiment_reflection, Mapping):
        raise CanonicalValidationError(
            "committed publication material lacks experiment reflection"
        )
    packets = _role_payloads(
        commit_path, projection, operator_evidence, "reflective_packets"
    )
    parent_input = _operator_input(
        commit_path, projection, operator_evidence, "reflective-conceptual-discovery"
    )
    synthesis_input = _operator_input(
        commit_path, projection, operator_evidence, "reflective-theory-synthesizer"
    )
    literature_input = _operator_input(
        commit_path, projection, operator_evidence, "frontier-literature-assimilator"
    )
    parent_evidence = list(parent_input.get("independent_evaluation_evidence", []))
    synthesis_evidence = list(
        synthesis_input.get("independent_evaluation_evidence", [])
    )
    if len(parent_evidence) != 1 or len(synthesis_evidence) != 1:
        raise CanonicalValidationError("committed publication evidence cardinality drift")
    source_catalog = literature_input.get("frozen_provider_source_catalog")
    capture_binding = literature_input.get("frozen_live_capture_binding")
    expected_catalog, expected_binding = _expected_frozen_provenance()
    if source_catalog != expected_catalog or capture_binding != expected_binding:
        raise CanonicalValidationError("committed frozen provenance drift")
    return {
        "core_validation": core_validation,
        "result": projection,
        "requests": list(operator_evidence["operator_requests"]),
        "receipts": list(operator_evidence["operator_receipts"]),
        "artifact_roles": _artifact_roles_from_commit(operator_evidence),
        "snapshot": snapshot,
        "assimilation": assimilation,
        "portfolio": portfolio,
        "parallel": parallel,
        "experiment_spec": experiment_spec,
        "experiment_receipt": experiment,
        "experiment_reflection_receipt": dict(experiment_reflection),
        "reflective_packets": packets,
        "conceptual_quality_evidence": [parent_evidence[0], synthesis_evidence[0]],
        "conceptual_generation_trace": parent_input["conceptual_generation_trace"],
        "literature_routing_trace": parent_input["literature_routing_trace"],
        "source_catalog": source_catalog,
        "capture_binding": capture_binding,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=REGISTERED_RUNTIME_ROOT)
    parser.add_argument(
        "--historical-replay",
        action="store_true",
        help="replay immutable evidence and prove freshness at execution without authorizing new investment",
    )
    args = parser.parse_args()
    try:
        summary = validate(
            args.output_root, historical_replay=args.historical_replay
        )
    except (CanonicalValidationError, ContractError, OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
