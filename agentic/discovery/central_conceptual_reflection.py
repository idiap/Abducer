# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Return central conceptual-route outcomes to one later canonical commit.

The five Category/HoTT/nonformal authorship routes are deliberately unable to
rewrite the theory commit that commissioned them.  This module turns their
authoritatively reopened packet into a typed request.  Its central source commit
and canonical cycle input head are distinct roles at ``N``; only the canonical
compare-and-swap may commit the descendant effect at ``N+1``.
It preserves the full route set, failures, quarantines and local blind result;
it does not turn any of them into a theory selection, proof, experiment, or
claim about conceptual or physical value.

Two validation surfaces are intentionally distinct.  ``decode_*`` proves only
that a retained JSON object is structurally self-consistent.  The authoritative
validator additionally reopens the complete central-route bundle, verifies the
current transaction head or exact active-prefix ancestor, and rejects any
detached or substituted closure.  V2 intake changed paths are computed from
registered producer before/after bytes rather than accepted from callers.
"""

from __future__ import annotations

import copy
import json
import stat
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from agentic.discovery.central_conceptual_routes_v3 import (
    ROUTE_ORDER,
    CentralConceptualRouteError,
    decode_central_conceptual_route_packet,
    reopen_active_prefix_central_conceptual_route_packet,
    reopen_authoritative_central_conceptual_route_packet,
    validate_committed_route_input,
)
from agentic.discovery.receipts import (
    ValidatorBinding,
    validate_operator_receipt_identity,
    validate_operator_request_identity,
    verify_current_validator_authority,
)
from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    safe_relative_path,
    stable_identifier,
    validate_instance,
)
from agentic.discovery.reflection import (
    ReflectionInvariantError,
    validate_packet_invariants,
)
from agentic.state.discovery_transaction import (
    DiscoveryTransactionStore,
    VerifiedCommit,
)


SCHEMA_VERSION = "2.0.0"
SCHEMA_NAME = "central_conceptual_route_reflection_request_v2.schema.json"
INTAKE_SCHEMA_NAME = (
    "central_conceptual_route_reflection_intake_v2.schema.json"
)
OPERATOR_REGISTRY_PATH = (
    Path(__file__).resolve().parents[1]
    / "registries"
    / "discovery_operator_registry.yaml"
)
_CENTRAL_REFLECTION_PRODUCERS = {
    "reflective-conceptual-discovery",
    "reflective-theory-synthesizer",
}
GENERATION_CONTRACT = {
    "central_source_role": "postcommit_central_route_source",
    "cycle_packet_state_role": "canonical_cycle_input_head",
    "descendant_effect_role": "canonical_compare_and_swap_result",
    "same_generation_effect_authorized": False,
    "canonical_compare_and_swap_required": True,
}

CURRENT_THEORY_EFFECT = {
    "theory_mutation_authorized": False,
    "ontology_mutation_authorized": False,
    "preference_replacement_authorized": False,
    "proof_authorized": False,
    "schedule_mutation_authorized": False,
    "experiment_authorized": False,
    "automatic_evidence_relation_authorized": False,
}

AUTHORITY_NULLS = {
    "truth_authority": None,
    "source_truth_authority": None,
    "global_latestness_authority": None,
    "literature_benefit_authority": None,
    "creativity_authority": None,
    "conceptual_merit_authority": None,
    "evaluator_independence": (
        "request_protocol_route_labels_absent_host_isolation_unavailable"
    ),
    "category_hott_advantage_authority": None,
    "physics_value_authority": None,
    "proof_authority": None,
    "theorem_authority": None,
    "experiment_authority": None,
    "generalization_authority": None,
    "publication_authority": None,
}

AUTHORITY_BOUNDARY = (
    "This request preserves one locally executed, authoritatively reopened, "
    "set-valued central-route result solely as material for reflective synthesis "
    "against canonical input head N for an exact N+1 compare-and-swap. It "
    "cannot mutate the commissioning "
    "theory, ontology, conceptual preference, evidence graph, proof state, action "
    "schedule, or experiment programme. Process separation and request-level "
    "route-label absence do not establish evaluator independence, creativity, "
    "conceptual merit, Category/HoTT advantage, truth, theoremhood, continuum "
    "control, physical value, generalization, publication readiness, or any "
    "target-specific scientific result."
)

INTAKE_DIRECT_AUTHORITY = {
    "preference_authorized": False,
    "truth_authorized": False,
    "proof_authorized": False,
    "schedule_authorized": False,
    "experiment_authorized": False,
    "evidence_relation_authorized": False,
}

INTAKE_AUTHORITY_NULLS = {
    "preference_authority": None,
    "truth_authority": None,
    "proof_authority": None,
    "schedule_authority": None,
    "experiment_authority": None,
    "evidence_relation_authority": None,
    "conceptual_merit_authority": None,
    "physics_value_authority": None,
}

INTAKE_AUTHORITY_BOUNDARY = (
    "The central-route selection is proposed against canonical input head N "
    "and can affect theory only if the canonical transaction commits N+1. Each "
    "route is bound to its exact source projection, a registered producer "
    "request and receipt, computed before/after patches, and exact round "
    "outcomes; failed, quarantined, or unavailable routes survive only as "
    "negative knowledge. These process bindings cannot directly authorize "
    "conceptual preference, truth, "
    "proof, scheduling, experiments, evidence relations, conceptual merit, "
    "Category/HoTT advantage, physical value, theoremhood, or a target-specific "
    "scientific result."
)

_MATERIAL_ROUTE_DISPOSITIONS = {
    "incorporated",
    "mutated",
    "synthesized",
    "demoted",
}
_SELECTED_ROUTE_DISPOSITIONS = {
    *_MATERIAL_ROUTE_DISPOSITIONS,
    "unresolved",
    "no_change",
}
_UNRESOLVED_ROUTE_DISPOSITIONS = {
    "unresolved",
    "preserved_unselected_candidate",
}
_NEGATIVE_SOURCE_DISPOSITIONS = {
    "quarantined_preserved_negative_knowledge",
    "unavailable_preserved_negative_knowledge",
    "worker_failure_preserved_negative_knowledge",
}


class CentralConceptualReflectionError(ContractError):
    """Raised when a central-route result cannot enter later reflection."""


def _fail(message: str) -> None:
    raise CentralConceptualReflectionError(
        f"central conceptual reflection request rejected: {message}"
    )


def _portable_commit(commit: VerifiedCommit) -> dict[str, Any]:
    return {
        "generation": commit.generation,
        "prior_generation": commit.prior_generation,
        "commit_id": commit.commit_id,
        "manifest_digest": commit.manifest_digest,
        "state_file_digest": commit.state_file_digest,
        "state_semantic_digest": commit.state_semantic_digest,
    }


def _snapshot_bundle(bundle_root: Path | str, commission_id: str) -> dict[str, Any]:
    """Snapshot every regular bundle file and reject links or unstable reads."""

    root = Path(bundle_root).resolve()
    if not root.is_dir() or root.is_symlink():
        _fail("central-route bundle root is absent, linked, or not a directory")
    paths = sorted(root.rglob("*"), key=lambda row: row.relative_to(root).as_posix())
    files: list[dict[str, Any]] = []
    for path in paths:
        try:
            before = path.lstat()
        except OSError as exc:
            _fail(f"cannot inspect bundle member: {exc}")
        if stat.S_ISDIR(before.st_mode):
            if path.is_symlink():
                _fail("central-route bundle contains a linked directory")
            continue
        if not stat.S_ISREG(before.st_mode) or path.is_symlink():
            _fail("central-route bundle contains a link or special file")
        try:
            data = path.read_bytes()
            after = path.lstat()
        except OSError as exc:
            _fail(f"cannot snapshot bundle member: {exc}")
        if (
            not stat.S_ISREG(after.st_mode)
            or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            or len(data) != before.st_size
        ):
            _fail("central-route bundle member changed during snapshot")
        files.append(
            {
                "relative_path": path.relative_to(root).as_posix(),
                "file_sha256": bytes_digest(data),
                "byte_length": len(data),
            }
        )
    if len({row["relative_path"] for row in files}) != len(files):
        _fail("central-route bundle manifest repeats a relative path")
    required = {
        "commission.json",
        "central-conceptual-route-packet-v3.json",
    }
    if not required.issubset({row["relative_path"] for row in files}):
        _fail("central-route bundle lacks its commission or final packet")
    material = {
        "manifest_kind": "complete_regular_file_closure",
        "commission_id": commission_id,
        "files": files,
        "file_count": len(files),
        "total_byte_length": sum(row["byte_length"] for row in files),
    }
    return {**material, "manifest_digest": canonical_digest(material)}


def _structural_packet(raw: Any) -> dict[str, Any]:
    try:
        packet = decode_central_conceptual_route_packet(raw)
    except (ContractError, CentralConceptualRouteError) as exc:
        _fail(f"source packet detached replay is invalid: {exc}")
    return copy.deepcopy(packet)


def _authoritative_packet(
    raw: Any,
    *,
    bundle_root: Path | str,
    store: DiscoveryTransactionStore,
) -> dict[str, Any]:
    try:
        packet = reopen_authoritative_central_conceptual_route_packet(
            raw, bundle_root=bundle_root, store=store
        )
    except (ContractError, CentralConceptualRouteError) as exc:
        _fail(f"source packet authoritative replay failed: {exc}")
    return copy.deepcopy(packet)


def _active_prefix_packet(
    raw: Any,
    *,
    bundle_root: Path | str,
    store: DiscoveryTransactionStore,
) -> dict[str, Any]:
    """Reopen a completed source packet from a verified active ancestor."""

    try:
        packet = reopen_active_prefix_central_conceptual_route_packet(
            raw, bundle_root=bundle_root, store=store
        )
    except (ContractError, CentralConceptualRouteError) as exc:
        _fail(f"source packet active-prefix replay failed: {exc}")
    return copy.deepcopy(packet)


def _route_projection(packet: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    terminals = {
        str(row["route_id"]): row for row in packet["route_terminals"]
    }
    outputs = {
        str(route_id): output
        for route_id, output in zip(
            ROUTE_ORDER, packet["route_outputs"], strict=True
        )
    }
    bindings = {
        str(row["route_id"]): row
        for row in packet["blind_identity_rebindings"]
    }
    selected_ids = set(packet["selected_route_set"])
    observations: list[dict[str, Any]] = []
    selected: list[dict[str, Any]] = []
    for route_id in ROUTE_ORDER:
        terminal = terminals[route_id]
        output = outputs[route_id]
        binding = bindings.get(route_id)
        is_selected = route_id in selected_ids
        if terminal["terminal_status"] == "failed":
            disposition = "worker_failure_preserved_negative_knowledge"
        elif output is None:
            _fail("nonfailed route lacks its source output")
        elif output["route_status"] == "quarantined":
            disposition = "quarantined_preserved_negative_knowledge"
        elif output["route_status"] == "unavailable":
            disposition = "unavailable_preserved_negative_knowledge"
        elif is_selected:
            disposition = "selected_local_pareto_candidate"
        elif packet["blind_judgment"] is None:
            disposition = "unadjudicated_completed_candidate_preserved"
        else:
            disposition = "not_selected_local_judgment_only"
        handback = output["physics_handback"] if output is not None else None
        candidate_digest = (
            canonical_digest(handback["content_projection"])
            if handback is not None
            and handback["handback_status"] == "admissible_for_blind_comparison"
            else None
        )
        observation = {
            "route_id": route_id,
            "terminal_status": terminal["terminal_status"],
            "terminal_digest": terminal["terminal_digest"],
            "output_status": output["route_status"] if output is not None else None,
            "candidate_content_digest": candidate_digest,
            "handback_digest": (
                handback["handback_digest"] if handback is not None else None
            ),
            "evidence_ledger_digest": (
                binding["evidence_ledger_digest"] if binding is not None else None
            ),
            "selected_for_descendant_reflection": is_selected,
            "preserved_disposition": disposition,
        }
        observations.append(observation)
        if is_selected:
            if binding is None or candidate_digest is None or handback is None:
                _fail("selected route lacks its exact blinded candidate binding")
            selected.append(
                {
                    "route_id": route_id,
                    "candidate_content_digest": candidate_digest,
                    "handback_digest": handback["handback_digest"],
                    "evidence_ledger_digest": binding["evidence_ledger_digest"],
                }
            )
    return observations, selected


def _manifest_replays(raw: Mapping[str, Any]) -> bool:
    manifest = copy.deepcopy(dict(raw))
    files = manifest.get("files")
    if not isinstance(files, list):
        return False
    if (
        manifest.get("file_count") != len(files)
        or manifest.get("total_byte_length")
        != sum(
            row.get("byte_length", -1)
            for row in files
            if isinstance(row, Mapping)
        )
        or len({row.get("relative_path") for row in files if isinstance(row, Mapping)})
        != len(files)
    ):
        return False
    return manifest.get("manifest_digest") == canonical_digest(
        manifest, exclude_keys=("manifest_digest",)
    )


def decode_central_conceptual_reflection_request(raw: Any) -> dict[str, Any]:
    """Decode self-consistent retained bytes without granting live authority."""

    request = copy.deepcopy(dict(raw)) if isinstance(raw, Mapping) else {}
    try:
        validate_instance(request, SCHEMA_NAME)
    except ContractError as exc:
        _fail(f"request schema is invalid: {exc}")
    packet = _structural_packet(request["source_packet"])
    observations, selected = _route_projection(packet)
    source_input = request["source_committed_input"]
    descriptor = packet["committed_input_descriptor"]
    if (
        request["schema_version"] != SCHEMA_VERSION
        or request["artifact_kind"]
        != "central_conceptual_route_reflection_request"
        or request["central_source_commit_generation"]
        != request["cycle_input_head_generation"]
        or request["descendant_effect_commit_generation"]
        != request["cycle_input_head_generation"] + 1
        or request["central_source_verified_commit"] != packet["verified_commit"]
        or request["cycle_input_head_verified_commit"]
        != request["central_source_verified_commit"]
        or request["central_source_commit_generation"]
        != packet["verified_commit"]["generation"]
        or request["cycle_input_head_generation"]
        != request["cycle_input_head_verified_commit"]["generation"]
        or request["generation_contract"] != GENERATION_CONTRACT
        or request["source_packet_digest"] != packet["content_digest"]
        or source_input["path"] != descriptor["path"]
        or source_input["file_sha256"] != descriptor["sha256"]
        or source_input["byte_length"] != descriptor["size_bytes"]
        or request["route_observations"] != observations
        or request["selected_candidate_set"] != selected
        or request["selection_is_set_valued"] is not True
        or request["current_theory_effect"] != CURRENT_THEORY_EFFECT
        or request["authority_nulls"] != AUTHORITY_NULLS
        or request["authority_boundary"] != AUTHORITY_BOUNDARY
        or request["permitted_descendant_effect"]
        != "reflective_synthesis_proposal_at_cycle_input_head_committed_only_by_exact_n_plus_one_cas"
        or request["experiment_role"]
        != "secondary_descendant_falsifier_only_after_reflective_theory_request"
        or not _manifest_replays(request["source_bundle_manifest"])
        or request["source_bundle_manifest"]["commission_id"]
        != packet["commission_id"]
    ):
        _fail("request does not replay its packet, generation, closure, or authority boundary")
    for output in packet["route_outputs"]:
        if output is not None and (
            output["committed_input_sha256"] != source_input["file_sha256"]
            or output["committed_input_byte_length"] != source_input["byte_length"]
            or output["committed_input_content_digest"]
            != source_input["content_digest"]
        ):
            _fail("route output differs from the retained committed input binding")
    expected_id = stable_identifier(
        "central-conceptual-reflection-request-v2",
        request["target_id"],
        request["run_id"],
        request["central_source_verified_commit"],
        request["cycle_input_head_verified_commit"],
        request["descendant_effect_commit_generation"],
        request["source_packet_digest"],
        observations,
        selected,
        request["source_bundle_manifest"]["manifest_digest"],
    )
    if request["request_id"] != expected_id:
        _fail("request identity is not derived from the exact retained content")
    if request["content_digest"] != canonical_digest(
        {
            key: value
            for key, value in request.items()
            if key != "content_digest"
        }
    ):
        _fail("request content digest is invalid")
    return request


def _canonical_payload_bytes(value: Mapping[str, Any]) -> bytes:
    return canonical_json(copy.deepcopy(dict(value))) + b"\n"


def _artifact_binds_bytes(descriptor: Mapping[str, Any], data: bytes) -> bool:
    return (
        descriptor.get("sha256") == bytes_digest(data)
        and descriptor.get("size_bytes") == len(data)
    )


def _registered_producer(request: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    """Reopen the registry and reject merely self-labelled producer requests."""

    try:
        validate_operator_request_identity(request)
        registry_data = OPERATOR_REGISTRY_PATH.read_bytes()
        registry = json.loads(registry_data.decode("utf-8"))
    except (ContractError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail(f"registered producer request cannot be reopened: {exc}")
    operator_id = str(request["operator"]["operator_id"])
    matches = [
        row
        for row in registry.get("operators", [])
        if isinstance(row, Mapping) and row.get("operator_id") == operator_id
    ]
    if len(matches) != 1 or operator_id not in _CENTRAL_REFLECTION_PRODUCERS:
        _fail("central reflection producer is not one exact registered theory operator")
    binding = copy.deepcopy(dict(matches[0]))
    if request["operator"] != {
        "operator_id": operator_id,
        "version": binding.get("version"),
        "kind": binding.get("kind"),
    }:
        _fail("producer request substituted the registered operator version or kind")
    return binding, bytes_digest(registry_data)


def _validate_registered_producer_input(
    *,
    source_request: Mapping[str, Any],
    producer_request: Mapping[str, Any],
    producer_input: Mapping[str, Any],
) -> tuple[dict[str, Any], str]:
    binding, registry_digest = _registered_producer(producer_request)
    input_rows = producer_request["input_artifacts"]
    parameters = producer_request["parameters"]
    source_generation = source_request["cycle_input_head_generation"]
    if (
        producer_request["required"] is not True
        or producer_request["identity"]
        != {
            "target_id": source_request["target_id"],
            "run_id": source_request["run_id"],
            "branch_id": "root",
            "state_version": source_generation,
        }
        or len(input_rows) != 1
        or not _artifact_binds_bytes(
            input_rows[0], _canonical_payload_bytes(producer_input)
        )
        or producer_input.get("central_conceptual_reflection_request")
        != source_request
        or parameters.get("central_conceptual_reflection_request_id")
        != source_request["request_id"]
        or parameters.get("central_conceptual_reflection_request_digest")
        != source_request["content_digest"]
        or parameters.get("central_descendant_effect_commit_generation")
        != source_request["descendant_effect_commit_generation"]
        or not isinstance(
            producer_input.get("central_conceptual_reflection_before"), Mapping
        )
        or not isinstance(
            producer_input.get("central_conceptual_route_directives"), list
        )
    ):
        _fail("registered producer input is detached from the exact source request or input head N")
    return binding, registry_digest


def _claim_material(
    source_request: Mapping[str, Any], producer_request: Mapping[str, Any]
) -> dict[str, Any]:
    material = {
        "target_id": source_request["target_id"],
        "run_id": source_request["run_id"],
        "source_request_id": source_request["request_id"],
        "source_request_digest": source_request["content_digest"],
        "central_source_verified_commit": copy.deepcopy(
            source_request["central_source_verified_commit"]
        ),
        "cycle_input_head_verified_commit": copy.deepcopy(
            source_request["cycle_input_head_verified_commit"]
        ),
        "central_source_commit_generation": source_request[
            "central_source_commit_generation"
        ],
        "cycle_input_head_generation": source_request["cycle_input_head_generation"],
        "descendant_effect_commit_generation": source_request[
            "descendant_effect_commit_generation"
        ],
        "producer_request_id": producer_request["request_id"],
        "producer_request_digest": producer_request["request_digest"],
        "producer_input_digest": producer_request["input_digest"],
        "claim_status": "authoritatively_claimed_at_exact_active_head",
        "descendant_commit_status": "pending_exact_canonical_n_plus_one_commit",
        "canonical_consumption_status": "pending_atomic_canonical_reducer_consumption",
        "portable_only": True,
    }
    material["claim_id"] = stable_identifier(
        "central-reflection-intake-claim-v2",
        source_request["request_id"],
        producer_request["request_id"],
        source_request["cycle_input_head_verified_commit"],
    )
    return material


def _decode_intake_claim(
    raw: Any,
    *,
    source_request: Mapping[str, Any],
    producer_request: Mapping[str, Any],
) -> dict[str, Any]:
    claim = copy.deepcopy(dict(raw)) if isinstance(raw, Mapping) else {}
    expected = _claim_material(source_request, producer_request)
    if (
        {key: value for key, value in claim.items() if key != "claim_digest"}
        != expected
        or claim.get("claim_digest") != canonical_digest(expected)
    ):
        _fail("intake claim does not replay its source head and producer request")
    return claim


def build_central_conceptual_reflection_intake_claim(
    *,
    central_request: Mapping[str, Any],
    store: DiscoveryTransactionStore,
    verified_commit: VerifiedCommit,
    bundle_root: Path | str,
    producer_request: Mapping[str, Any],
    producer_input: Mapping[str, Any],
) -> dict[str, Any]:
    """Claim one registered producer while its exact source remains head N."""

    source_request = validate_authoritative_central_conceptual_reflection_request(
        central_request,
        store=store,
        verified_commit=verified_commit,
        bundle_root=bundle_root,
    )
    _validate_registered_producer_input(
        source_request=source_request,
        producer_request=producer_request,
        producer_input=producer_input,
    )
    material = _claim_material(source_request, producer_request)
    return {**material, "claim_digest": canonical_digest(material)}


def _context_snapshot(
    conceptual_systems: Any, reflection_rounds: Any
) -> dict[str, Any]:
    systems, rounds, _system_ids, _round_ids = _context_rows(
        conceptual_systems, reflection_rounds
    )
    core = {
        "conceptual_systems": systems,
        "reflection_rounds": rounds,
        "conceptual_systems_digest": canonical_digest(systems),
        "reflection_rounds_digest": canonical_digest(rounds),
    }
    return {**core, "snapshot_digest": canonical_digest(core)}


def _pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _value_slot(present: bool, value: Any) -> dict[str, Any]:
    retained = copy.deepcopy(value) if present else None
    return {
        "present": present,
        "value": retained,
        "value_digest": canonical_digest(retained) if present else None,
    }


def _typed_patch(
    *,
    operation: str,
    path: str,
    owner_kind: str,
    owner_id: str,
    before_present: bool,
    before: Any,
    after_present: bool,
    after: Any,
) -> dict[str, Any]:
    core = {
        "operation": operation,
        "path": path,
        "owner_kind": owner_kind,
        "owner_id": owner_id,
        "before": _value_slot(before_present, before),
        "after": _value_slot(after_present, after),
    }
    return {**core, "patch_digest": canonical_digest(core)}


def _diff_value(
    before: Any,
    after: Any,
    *,
    path: str,
    owner_kind: str,
    owner_id: str,
) -> list[dict[str, Any]]:
    if before == after:
        return []
    if isinstance(before, Mapping) and isinstance(after, Mapping):
        patches: list[dict[str, Any]] = []
        for key in sorted(set(before) | set(after)):
            child_path = f"{path}/{_pointer_token(str(key))}"
            if key not in before:
                patches.append(
                    _typed_patch(
                        operation="add", path=child_path,
                        owner_kind=owner_kind, owner_id=owner_id,
                        before_present=False, before=None,
                        after_present=True, after=after[key],
                    )
                )
            elif key not in after:
                patches.append(
                    _typed_patch(
                        operation="remove", path=child_path,
                        owner_kind=owner_kind, owner_id=owner_id,
                        before_present=True, before=before[key],
                        after_present=False, after=None,
                    )
                )
            else:
                patches.extend(
                    _diff_value(
                        before[key], after[key], path=child_path,
                        owner_kind=owner_kind, owner_id=owner_id,
                    )
                )
        return patches
    return [
        _typed_patch(
            operation="replace", path=path,
            owner_kind=owner_kind, owner_id=owner_id,
            before_present=True, before=before,
            after_present=True, after=after,
        )
    ]


def _computed_context_patches(
    before: Mapping[str, Any], after: Mapping[str, Any]
) -> list[dict[str, Any]]:
    patches: list[dict[str, Any]] = []
    for collection, identity, owner_kind in (
        ("conceptual_systems", "system_id", "conceptual_system"),
        ("reflection_rounds", "round_id", "reflection_round"),
    ):
        before_rows = before[collection]
        after_rows = after[collection]
        before_ids = [str(row[identity]) for row in before_rows]
        after_ids = [str(row[identity]) for row in after_rows]
        if before_ids != after_ids:
            _fail(f"registered producer changed ordered {collection} identities; re-identification is forbidden")
        for index, (before_row, after_row) in enumerate(
            zip(before_rows, after_rows, strict=True)
        ):
            patches.extend(
                _diff_value(
                    before_row,
                    after_row,
                    path=f"/{collection}/{index}",
                    owner_kind=owner_kind,
                    owner_id=str(after_row[identity]),
                )
            )
    return sorted(patches, key=lambda row: (row["path"], row["patch_digest"]))


def _producer_binding_and_snapshots(
    *,
    source_request: Mapping[str, Any],
    producer_request: Mapping[str, Any],
    producer_receipt: Mapping[str, Any],
    producer_input: Mapping[str, Any],
    producer_output: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    registry_binding, registry_digest = _validate_registered_producer_input(
        source_request=source_request,
        producer_request=producer_request,
        producer_input=producer_input,
    )
    try:
        validate_operator_receipt_identity(producer_receipt, producer_request)
        validate_instance(
            producer_output, "reflective_conceptual_discovery_packet.schema.json"
        )
        validate_packet_invariants(producer_output)
    except (ContractError, ReflectionInvariantError) as exc:
        _fail(f"registered producer receipt or output is invalid: {exc}")
    expected_validators = registry_binding.get("validators")
    actual_validators = producer_receipt.get("validator_receipts")
    if (
        not isinstance(expected_validators, list)
        or not expected_validators
        or not isinstance(actual_validators, list)
        or [
            (row.get("validator_id"), row.get("validator_version"))
            for row in actual_validators
        ]
        != [
            (row.get("validator_id"), row.get("version"))
            for row in expected_validators
        ]
        or any(row.get("status") != "passed" for row in actual_validators)
    ):
        _fail("producer receipt lacks the registry's exact passing validator vector")
    try:
        for expected, actual in zip(
            expected_validators, actual_validators, strict=True
        ):
            validator_binding = ValidatorBinding(
                validator_id=str(expected["validator_id"]),
                version=str(expected["version"]),
                command=tuple(str(value) for value in expected["command"]),
                dependency_paths=tuple(
                    f"repo://{value}"
                    for value in expected["dependency_paths"]
                ),
                dependency_policy=str(expected["dependency_policy"]),
                timeout_seconds=float(expected["timeout_seconds"]),
            )
            verify_current_validator_authority(
                actual["validator_authority"], validator_binding
            )
    except (ContractError, KeyError, TypeError, ValueError) as exc:
        _fail(f"producer validator authority differs from the current registry: {exc}")
    input_rows = producer_request["input_artifacts"]
    output_rows = producer_receipt["output_artifacts"]
    if (
        producer_receipt["status"] != "succeeded"
        or len(output_rows) != 1
        or not _artifact_binds_bytes(
            output_rows[0], _canonical_payload_bytes(producer_output)
        )
        or producer_output.get("packet_digest")
        != canonical_digest(
            producer_output, exclude_keys=("packet_digest",)
        )
    ):
        _fail("registered producer receipt does not bind one exact successful output packet")
    before_raw = producer_input["central_conceptual_reflection_before"]
    before = _context_snapshot(
        before_raw.get("conceptual_systems"), before_raw.get("reflection_rounds")
    )
    after = _context_snapshot(
        producer_output.get("conceptual_systems"),
        producer_output.get("reflection_rounds"),
    )
    directives = copy.deepcopy(
        producer_input["central_conceptual_route_directives"]
    )
    core = {
        "operator_id": producer_request["operator"]["operator_id"],
        "operator_version": producer_request["operator"]["version"],
        "registry_file_digest": registry_digest,
        "producer_request": copy.deepcopy(dict(producer_request)),
        "producer_receipt": copy.deepcopy(dict(producer_receipt)),
        "producer_input": copy.deepcopy(dict(producer_input)),
        "producer_output": copy.deepcopy(dict(producer_output)),
        "producer_input_digest": canonical_digest(producer_input),
        "producer_output_digest": canonical_digest(producer_output),
        "input_descriptor": copy.deepcopy(input_rows[0]),
        "output_descriptor": copy.deepcopy(output_rows[0]),
        "validator_receipt_digests": [
            str(row["receipt_digest"])
            for row in producer_receipt["validator_receipts"]
        ],
    }
    if registry_binding.get("operator_id") != core["operator_id"]:
        _fail("registered producer binding changed during intake replay")
    binding = {**core, "binding_digest": canonical_digest(core)}
    return binding, before, after, directives


def _source_candidate_projections(
    source_request: Mapping[str, Any],
) -> dict[str, dict[str, Any] | None]:
    return {
        route_id: (
            copy.deepcopy(output["physics_handback"]["content_projection"])
            if output is not None
            else None
        )
        for route_id, output in zip(
            ROUTE_ORDER, source_request["source_packet"]["route_outputs"], strict=True
        )
    }


def _derive_route_accounts(
    *,
    source_request: Mapping[str, Any],
    directives: Any,
    after: Mapping[str, Any],
    patches: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str], list[str], list[str]]:
    if (
        not isinstance(directives, list)
        or len(directives) != len(ROUTE_ORDER)
        or [row.get("route_id") for row in directives] != list(ROUTE_ORDER)
    ):
        _fail("producer route directives must be an ordered five-route bijection")
    expected_fields = {
        "route_id", "descendant_disposition", "referenced_system_ids",
        "referenced_round_ids", "reflection_note",
    }
    if any(not isinstance(row, Mapping) or set(row) != expected_fields for row in directives):
        _fail("producer route directive shape is not exact and cannot contain changed paths")
    observations = {row["route_id"]: row for row in source_request["route_observations"]}
    selected = {row["route_id"]: row for row in source_request["selected_candidate_set"]}
    projections = _source_candidate_projections(source_request)
    system_ids = {str(row["system_id"]) for row in after["conceptual_systems"]}
    rounds_by_id = {str(row["round_id"]): row for row in after["reflection_rounds"]}
    material_owner_routes: dict[str, list[str]] = {}
    for directive in directives:
        route_id = str(directive["route_id"])
        disposition = str(directive["descendant_disposition"])
        refs = [
            *[str(value) for value in directive["referenced_system_ids"]],
            *[str(value) for value in directive["referenced_round_ids"]],
        ]
        if disposition in _MATERIAL_ROUTE_DISPOSITIONS:
            for owner_id in refs:
                material_owner_routes.setdefault(owner_id, []).append(route_id)
    for patch in patches:
        owners = material_owner_routes.get(str(patch["owner_id"]), [])
        if len(owners) != 1:
            _fail("every computed patch must have exactly one material route owner")
    accounts: list[dict[str, Any]] = []
    changed: list[str] = []
    unresolved: list[str] = []
    negative: list[str] = []
    for directive_raw in directives:
        directive = copy.deepcopy(dict(directive_raw))
        route_id = str(directive["route_id"])
        observation = observations[route_id]
        disposition = str(directive["descendant_disposition"])
        system_refs = [str(value) for value in directive["referenced_system_ids"]]
        round_refs = [str(value) for value in directive["referenced_round_ids"]]
        if (
            len(system_refs) != len(set(system_refs))
            or len(round_refs) != len(set(round_refs))
            or any(value not in system_ids for value in system_refs)
            or any(value not in rounds_by_id for value in round_refs)
        ):
            _fail(f"route {route_id} references a missing or duplicated producer output identity")
        is_negative = (
            observation["terminal_status"] == "failed"
            or observation["output_status"] in {"quarantined", "unavailable"}
            or observation["preserved_disposition"] in _NEGATIVE_SOURCE_DISPOSITIONS
        )
        if is_negative:
            if disposition != "preserved_negative_knowledge" or system_refs or round_refs:
                _fail(f"route {route_id} must preserve failure only as negative knowledge")
            negative.append(route_id)
        elif disposition == "preserved_negative_knowledge":
            _fail(f"route {route_id} fabricated negative knowledge")
        elif selected.get(route_id) is not None and (
            disposition not in _SELECTED_ROUTE_DISPOSITIONS
            or not (system_refs or round_refs)
        ):
            _fail(f"selected route {route_id} lacks a linked reflective disposition")
        elif selected.get(route_id) is None and disposition not in {
            *_SELECTED_ROUTE_DISPOSITIONS, "preserved_unselected_candidate"
        }:
            _fail(f"unselected route {route_id} has an invalid disposition")
        route_patches = [
            copy.deepcopy(row)
            for row in patches
            if material_owner_routes.get(str(row["owner_id"])) == [route_id]
        ]
        if disposition in _MATERIAL_ROUTE_DISPOSITIONS and not route_patches:
            _fail(f"material route {route_id} produced no computed content patch")
        if disposition not in _MATERIAL_ROUTE_DISPOSITIONS and route_patches:
            _fail(f"nonmaterial route {route_id} cannot own a computed content patch")
        if disposition in _MATERIAL_ROUTE_DISPOSITIONS:
            changed.append(route_id)
        elif disposition in _UNRESOLVED_ROUTE_DISPOSITIONS:
            unresolved.append(route_id)
        projection = projections[route_id]
        accounts.append(
            {
                "route_id": route_id,
                "source_observation": copy.deepcopy(observation),
                "source_candidate_projection": projection,
                "source_candidate_projection_digest": (
                    canonical_digest(projection) if projection is not None else None
                ),
                "selected_candidate_binding": copy.deepcopy(selected.get(route_id)),
                "causal_directive": directive,
                "computed_patches": route_patches,
                "computed_changed_paths": [row["path"] for row in route_patches],
                "round_outcomes": [
                    {
                        "round_id": round_id,
                        "result": str(rounds_by_id[round_id]["result"]),
                        "round_projection": copy.deepcopy(rounds_by_id[round_id]),
                        "round_projection_digest": canonical_digest(rounds_by_id[round_id]),
                    }
                    for round_id in round_refs
                ],
            }
        )
    return accounts, changed, unresolved, negative


def _decode_json_pointer_token(token: str) -> str:
    """Decode one RFC 6901 token while rejecting malformed escapes."""

    decoded: list[str] = []
    index = 0
    while index < len(token):
        character = token[index]
        if character != "~":
            decoded.append(character)
            index += 1
            continue
        if index + 1 >= len(token) or token[index + 1] not in {"0", "1"}:
            _fail("route account contains a malformed JSON-pointer escape")
        decoded.append("~" if token[index + 1] == "0" else "/")
        index += 2
    return "".join(decoded)


def _context_rows(
    conceptual_systems: Any,
    reflection_rounds: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[str], set[str]]:
    """Freeze the descendant context and prove its local identity closure."""

    if (
        not isinstance(conceptual_systems, list)
        or not conceptual_systems
        or not all(isinstance(row, Mapping) for row in conceptual_systems)
        or not isinstance(reflection_rounds, list)
        or not reflection_rounds
        or not all(isinstance(row, Mapping) for row in reflection_rounds)
    ):
        _fail(
            "central-route intake requires explicit nonempty conceptual systems "
            "and reflection rounds"
        )
    systems = copy.deepcopy(conceptual_systems)
    rounds = copy.deepcopy(reflection_rounds)
    try:
        system_ids = [str(row["system_id"]) for row in systems]
        round_ids = [str(row["round_id"]) for row in rounds]
    except KeyError as exc:
        _fail(f"descendant context lacks a typed identity: {exc}")
    if (
        any(not value for value in system_ids + round_ids)
        or len(set(system_ids)) != len(system_ids)
        or len(set(round_ids)) != len(round_ids)
    ):
        _fail("descendant system and reflection-round identities must be unique")
    system_id_set = set(system_ids)
    for round_row in rounds:
        referenced = round_row.get("system_ids")
        if (
            not isinstance(referenced, list)
            or not referenced
            or any(str(value) not in system_id_set for value in referenced)
        ):
            _fail(
                "reflection round references a missing descendant conceptual system"
            )
    return systems, rounds, system_id_set, set(round_ids)


def _resolve_changed_path(
    pointer: Any,
    *,
    systems: list[dict[str, Any]],
    rounds: list[dict[str, Any]],
) -> tuple[str, str]:
    """Resolve one changed path and return its collection plus owning identity."""

    if not isinstance(pointer, str) or not pointer.startswith("/"):
        _fail("route account changed paths must be JSON pointers")
    tokens = [
        _decode_json_pointer_token(token) for token in pointer[1:].split("/")
    ]
    if len(tokens) < 2 or tokens[0] not in {
        "conceptual_systems",
        "reflection_rounds",
    }:
        _fail(
            "route account changed paths may address only conceptual systems "
            "or reflection rounds"
        )
    raw_index = tokens[1]
    if (
        not raw_index.isdigit()
        or (len(raw_index) > 1 and raw_index.startswith("0"))
    ):
        _fail("route account changed path has a noncanonical array index")
    row_index = int(raw_index)
    rows = systems if tokens[0] == "conceptual_systems" else rounds
    if row_index >= len(rows):
        _fail("route account changed path indexes beyond the descendant context")
    current: Any = rows[row_index]
    for token in tokens[2:]:
        if isinstance(current, Mapping):
            if token not in current:
                _fail("route account changed path does not resolve")
            current = current[token]
        elif isinstance(current, list):
            if (
                not token.isdigit()
                or (len(token) > 1 and token.startswith("0"))
                or int(token) >= len(current)
            ):
                _fail("route account changed path does not resolve")
            current = current[int(token)]
        else:
            _fail("route account changed path descends through a scalar")
    identity_field = (
        "system_id" if tokens[0] == "conceptual_systems" else "round_id"
    )
    return tokens[0], str(rows[row_index][identity_field])


def _analyze_route_accounts(
    *,
    source_request: Mapping[str, Any],
    route_accounts: Any,
    systems: list[dict[str, Any]],
    rounds: list[dict[str, Any]],
    system_ids: set[str],
    round_ids: set[str],
) -> tuple[list[dict[str, Any]], list[str], list[str], list[str]]:
    """Validate exact five-route causality and derive its three status sets."""

    if (
        not isinstance(route_accounts, list)
        or len(route_accounts) != len(ROUTE_ORDER)
        or not all(isinstance(row, Mapping) for row in route_accounts)
    ):
        _fail("route accounts must contain exactly five typed rows")
    accounts = copy.deepcopy(route_accounts)
    required_fields = {
        "route_id",
        "source_observation",
        "selected_candidate_binding",
        "descendant_disposition",
        "referenced_system_ids",
        "referenced_round_ids",
        "changed_paths",
        "reflection_note",
    }
    if any(required_fields - set(row) for row in accounts):
        _fail("route account is missing a required causal field")
    if [str(row["route_id"]) for row in accounts] != list(ROUTE_ORDER):
        _fail("route accounts must be an ordered bijection over ROUTE_ORDER")

    observations = {
        str(row["route_id"]): row
        for row in source_request["route_observations"]
    }
    selected = {
        str(row["route_id"]): row
        for row in source_request["selected_candidate_set"]
    }
    changed: list[str] = []
    unresolved: list[str] = []
    negative: list[str] = []
    for account in accounts:
        route_id = str(account["route_id"])
        observation = observations[route_id]
        selected_binding = selected.get(route_id)
        if account["source_observation"] != observation:
            _fail(f"route {route_id} changed its exact source observation")
        if account["selected_candidate_binding"] != selected_binding:
            _fail(
                f"route {route_id} changed or omitted its selected-candidate binding"
            )
        disposition = str(account["descendant_disposition"])
        is_negative_source = (
            observation["terminal_status"] == "failed"
            or observation["output_status"] in {"quarantined", "unavailable"}
            or observation["preserved_disposition"]
            in _NEGATIVE_SOURCE_DISPOSITIONS
        )
        referenced_system_ids = account["referenced_system_ids"]
        referenced_round_ids = account["referenced_round_ids"]
        changed_paths = account["changed_paths"]
        if (
            not isinstance(referenced_system_ids, list)
            or len(set(referenced_system_ids)) != len(referenced_system_ids)
            or any(str(value) not in system_ids for value in referenced_system_ids)
            or not isinstance(referenced_round_ids, list)
            or len(set(referenced_round_ids)) != len(referenced_round_ids)
            or any(str(value) not in round_ids for value in referenced_round_ids)
            or not isinstance(changed_paths, list)
            or len(set(changed_paths)) != len(changed_paths)
        ):
            _fail(f"route {route_id} has invalid descendant references")
        if is_negative_source:
            if (
                disposition != "preserved_negative_knowledge"
                or referenced_system_ids
                or referenced_round_ids
                or changed_paths
            ):
                _fail(
                    f"route {route_id} failure, quarantine, or unavailability "
                    "must survive only as preserved negative knowledge"
                )
            negative.append(route_id)
            continue
        if disposition == "preserved_negative_knowledge":
            _fail(
                f"route {route_id} cannot fabricate negative knowledge from a "
                "completed candidate"
            )
        if selected_binding is not None:
            if disposition not in _SELECTED_ROUTE_DISPOSITIONS:
                _fail(
                    f"selected route {route_id} lacks an explicit reflective "
                    "disposition"
                )
            if not referenced_system_ids and not referenced_round_ids:
                _fail(
                    f"selected route {route_id} is not linked to a descendant "
                    "system or reflection round"
                )
        elif disposition not in {
            *_SELECTED_ROUTE_DISPOSITIONS,
            "preserved_unselected_candidate",
        }:
            _fail(f"unselected route {route_id} has an invalid disposition")

        if disposition in _MATERIAL_ROUTE_DISPOSITIONS and not changed_paths:
            _fail(f"material route {route_id} lacks an exact changed path")
        if (
            disposition not in _MATERIAL_ROUTE_DISPOSITIONS
            and changed_paths
        ):
            _fail(
                f"nonmaterial route {route_id} cannot claim descendant changed paths"
            )
        for pointer in changed_paths:
            collection, owner_id = _resolve_changed_path(
                pointer, systems=systems, rounds=rounds
            )
            expected_refs = (
                referenced_system_ids
                if collection == "conceptual_systems"
                else referenced_round_ids
            )
            if owner_id not in expected_refs:
                _fail(
                    f"route {route_id} changed path is detached from its "
                    "referenced descendant identity"
                )
        if disposition in _MATERIAL_ROUTE_DISPOSITIONS:
            changed.append(route_id)
        elif disposition in _UNRESOLVED_ROUTE_DISPOSITIONS:
            unresolved.append(route_id)
    return accounts, changed, unresolved, negative


def _computed_patch_set(patches: list[dict[str, Any]]) -> dict[str, Any]:
    core = {
        "patches": copy.deepcopy(patches),
        "changed_paths": [str(row["path"]) for row in patches],
        "patch_count": len(patches),
        "complete_route_cover": True,
    }
    return {**core, "patch_set_digest": canonical_digest(core)}


def _derived_intake_material(
    *,
    source_request: Mapping[str, Any],
    intake_claim: Mapping[str, Any],
    producer_binding: Mapping[str, Any],
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    directives: list[dict[str, Any]],
) -> dict[str, Any]:
    patches = _computed_context_patches(before, after)
    accounts, changed, unresolved, negative = _derive_route_accounts(
        source_request=source_request,
        directives=directives,
        after=after,
        patches=patches,
    )
    patch_set = _computed_patch_set(patches)
    selected_route_ids = [
        str(row["route_id"])
        for row in source_request["selected_candidate_set"]
    ]
    material: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "central_conceptual_route_reflection_intake",
        "target_id": source_request["target_id"],
        "run_id": source_request["run_id"],
        "central_source_commit_generation": source_request[
            "central_source_commit_generation"
        ],
        "cycle_input_head_generation": source_request[
            "cycle_input_head_generation"
        ],
        "descendant_effect_commit_generation": source_request[
            "descendant_effect_commit_generation"
        ],
        "source_request": copy.deepcopy(dict(source_request)),
        "source_request_id": source_request["request_id"],
        "source_request_digest": source_request["content_digest"],
        "intake_claim": copy.deepcopy(dict(intake_claim)),
        "registered_producer_binding": copy.deepcopy(dict(producer_binding)),
        "before_snapshot": copy.deepcopy(dict(before)),
        "after_snapshot": copy.deepcopy(dict(after)),
        "selection_is_set_valued_local_input": True,
        "source_selected_route_ids": selected_route_ids,
        "route_accounts": accounts,
        "computed_patch_set": patch_set,
        "changed_route_ids": changed,
        "unresolved_route_ids": unresolved,
        "negative_knowledge_route_ids": negative,
        "direct_authority": copy.deepcopy(INTAKE_DIRECT_AUTHORITY),
        "authority_nulls": copy.deepcopy(INTAKE_AUTHORITY_NULLS),
        "authority_boundary": INTAKE_AUTHORITY_BOUNDARY,
    }
    material["intake_id"] = stable_identifier(
        "central-conceptual-route-reflection-intake-v2",
        material["target_id"],
        material["run_id"],
        material["central_source_commit_generation"],
        material["cycle_input_head_generation"],
        material["descendant_effect_commit_generation"],
        source_request["request_id"],
        intake_claim["claim_digest"],
        producer_binding["binding_digest"],
        before["snapshot_digest"],
        after["snapshot_digest"],
        canonical_digest(accounts),
        patch_set["patch_set_digest"],
    )
    return material


def decode_central_conceptual_route_reflection_intake(
    raw: Any,
    *,
    conceptual_systems: list[dict[str, Any]],
    reflection_rounds: list[dict[str, Any]],
) -> dict[str, Any]:
    """Replay receipt-derived N-to-N+1 intent against exact output content."""

    intake = copy.deepcopy(dict(raw)) if isinstance(raw, Mapping) else {}
    try:
        validate_instance(intake, INTAKE_SCHEMA_NAME)
        source_request = decode_central_conceptual_reflection_request(
            intake["source_request"]
        )
        binding_raw = intake["registered_producer_binding"]
        binding, before, after, directives = _producer_binding_and_snapshots(
            source_request=source_request,
            producer_request=binding_raw["producer_request"],
            producer_receipt=binding_raw["producer_receipt"],
            producer_input=binding_raw["producer_input"],
            producer_output=binding_raw["producer_output"],
        )
        claim = _decode_intake_claim(
            intake["intake_claim"],
            source_request=source_request,
            producer_request=binding["producer_request"],
        )
    except ContractError as exc:
        _fail(f"descendant intake schema or source closure is invalid: {exc}")
    systems, rounds, _system_ids, _round_ids = _context_rows(
        conceptual_systems, reflection_rounds
    )
    if (
        systems != after["conceptual_systems"]
        or rounds != after["reflection_rounds"]
    ):
        _fail("workflow content differs from the registered producer output bytes")
    expected = _derived_intake_material(
        source_request=source_request,
        intake_claim=claim,
        producer_binding=binding,
        before=before,
        after=after,
        directives=directives,
    )
    if (
        {key: value for key, value in intake.items() if key != "content_digest"}
        != expected
    ):
        _fail(
            "descendant intake does not replay its source roles, claim, exact "
            "registered producer bytes, computed patches, or authority boundary"
        )
    if intake["content_digest"] != canonical_digest(expected):
        _fail("descendant intake content digest is invalid")
    return intake


def build_central_conceptual_route_reflection_intake(
    *,
    central_request: Mapping[str, Any],
    intake_claim: Mapping[str, Any],
    producer_request: Mapping[str, Any],
    producer_receipt: Mapping[str, Any],
    producer_input: Mapping[str, Any],
    producer_output: Mapping[str, Any],
    store: DiscoveryTransactionStore,
    verified_commit: VerifiedCommit,
    bundle_root: Path | str,
    target_id: str,
    run_id: str,
    state_version: int,
    conceptual_systems: list[dict[str, Any]],
    reflection_rounds: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build receipt-derived intent at head N for canonical commit N+1."""

    source_request = validate_authoritative_central_conceptual_reflection_request(
        central_request,
        store=store,
        verified_commit=verified_commit,
        bundle_root=bundle_root,
    )
    binding, before, after, directives = _producer_binding_and_snapshots(
        source_request=source_request,
        producer_request=producer_request,
        producer_receipt=producer_receipt,
        producer_input=producer_input,
        producer_output=producer_output,
    )
    claim = _decode_intake_claim(
        intake_claim,
        source_request=source_request,
        producer_request=binding["producer_request"],
    )
    systems, rounds, _system_ids, _round_ids = _context_rows(
        conceptual_systems, reflection_rounds
    )
    if (
        target_id != source_request["target_id"]
        or run_id != source_request["run_id"]
        or state_version != source_request["cycle_input_head_generation"]
        or source_request["descendant_effect_commit_generation"]
        != state_version + 1
        or systems != after["conceptual_systems"]
        or rounds != after["reflection_rounds"]
    ):
        _fail(
            "workflow namespace and packet state must equal input head N, output "
            "must equal registered producer bytes, and descendant effect must be N+1"
        )
    material = _derived_intake_material(
        source_request=source_request,
        intake_claim=claim,
        producer_binding=binding,
        before=before,
        after=after,
        directives=directives,
    )
    intake = {**material, "content_digest": canonical_digest(material)}
    return decode_central_conceptual_route_reflection_intake(
        intake,
        conceptual_systems=systems,
        reflection_rounds=rounds,
    )


def _validated_reflective_packet(raw: Any) -> dict[str, Any]:
    packet = copy.deepcopy(dict(raw)) if isinstance(raw, Mapping) else {}
    try:
        validate_instance(
            packet, "reflective_conceptual_discovery_packet.schema.json"
        )
        validate_packet_invariants(packet)
    except (ContractError, ReflectionInvariantError) as exc:
        _fail(f"reflective descendant packet is invalid: {exc}")
    if packet.get("packet_digest") != canonical_digest(
        {
            key: value
            for key, value in packet.items()
            if key != "packet_digest"
        }
    ):
        _fail("reflective descendant packet digest is invalid")
    return packet


def build_central_conceptual_reflection_commit_binding(
    *,
    packet: Mapping[str, Any],
    packet_artifact_path: str,
) -> dict[str, Any]:
    """Build the exact state marker a canonical N+1 commit must consume."""

    if not isinstance(packet_artifact_path, str):
        _fail("descendant packet artifact path must be a canonical relative path")
    try:
        relative_path = safe_relative_path(packet_artifact_path).as_posix()
    except ContractError as exc:
        _fail(f"descendant packet artifact path is unsafe: {exc}")
    if relative_path != packet_artifact_path:
        _fail("descendant packet artifact path is not canonical")
    validated_packet = _validated_reflective_packet(packet)
    intake_raw = validated_packet.get(
        "central_conceptual_route_reflection_intake"
    )
    if not isinstance(intake_raw, Mapping):
        _fail("descendant packet lacks its v2 central reflection intake")
    intake = decode_central_conceptual_route_reflection_intake(
        intake_raw,
        conceptual_systems=validated_packet["conceptual_systems"],
        reflection_rounds=validated_packet["reflection_rounds"],
    )
    if (
        validated_packet["target_id"] != intake["target_id"]
        or validated_packet["run_id"] != intake["run_id"]
        or validated_packet["branch_id"] != "root"
        or validated_packet["state_version"]
        != intake["cycle_input_head_generation"]
        or intake["descendant_effect_commit_generation"]
        != validated_packet["state_version"] + 1
    ):
        _fail("descendant packet namespace or N-to-N+1 role is invalid")
    core = {
        "schema_version": SCHEMA_VERSION,
        "binding_kind": "central_conceptual_reflection_n_plus_one_consumption",
        "target_id": intake["target_id"],
        "run_id": intake["run_id"],
        "central_source_commit_generation": intake[
            "central_source_commit_generation"
        ],
        "cycle_input_head_generation": intake["cycle_input_head_generation"],
        "descendant_effect_commit_generation": intake[
            "descendant_effect_commit_generation"
        ],
        "source_request_id": intake["source_request_id"],
        "source_request_digest": intake["source_request_digest"],
        "intake_claim_id": intake["intake_claim"]["claim_id"],
        "intake_claim_digest": intake["intake_claim"]["claim_digest"],
        "intake_id": intake["intake_id"],
        "intake_digest": intake["content_digest"],
        "packet_id": validated_packet["packet_id"],
        "packet_digest": validated_packet["packet_digest"],
        "packet_artifact_path": relative_path,
        "canonical_consumption_status": (
            "consumed_by_exact_canonical_n_plus_one_state_and_artifact"
        ),
    }
    core["binding_id"] = stable_identifier(
        "central-conceptual-reflection-commit-binding-v2",
        core["target_id"],
        core["run_id"],
        core["descendant_effect_commit_generation"],
        core["intake_claim_digest"],
        core["intake_digest"],
        core["packet_digest"],
        relative_path,
    )
    return {**core, "binding_digest": canonical_digest(core)}


def recover_central_conceptual_reflection_intake_claim(
    *,
    central_request: Mapping[str, Any],
    store: DiscoveryTransactionStore,
    verified_commit: VerifiedCommit,
    bundle_root: Path | str,
    producer_request: Mapping[str, Any],
    producer_input: Mapping[str, Any],
) -> dict[str, Any]:
    """Deterministically recover a claim and classify its exact N+1 slot."""

    source_request = validate_active_prefix_central_conceptual_reflection_request(
        central_request,
        store=store,
        verified_commit=verified_commit,
        bundle_root=bundle_root,
    )
    _validate_registered_producer_input(
        source_request=source_request,
        producer_request=producer_request,
        producer_input=producer_input,
    )
    claim_material = _claim_material(source_request, producer_request)
    claim = {
        **claim_material,
        "claim_digest": canonical_digest(claim_material),
    }
    descendant_generation = source_request[
        "descendant_effect_commit_generation"
    ]
    with store.verified_artifact_context() as context:
        current_generation = context.current_generation
        current_commit = context.read_commit(current_generation)
        descendant_commit = (
            context.read_commit(descendant_generation)
            if current_generation >= descendant_generation
            else None
        )
    observed_binding = (
        descendant_commit.state.get("central_conceptual_reflection_consumption")
        if descendant_commit is not None
        else None
    )
    if descendant_commit is None:
        disposition = "pending_exact_n_plus_one_compare_and_swap"
    elif isinstance(observed_binding, Mapping) and (
        observed_binding.get("intake_claim_id") == claim["claim_id"]
        and observed_binding.get("intake_claim_digest")
        == claim["claim_digest"]
        and observed_binding.get("source_request_id")
        == source_request["request_id"]
        and observed_binding.get("source_request_digest")
        == source_request["content_digest"]
    ):
        disposition = "matching_n_plus_one_commit_available_for_exact_replay"
    else:
        disposition = "superseded_by_other_n_plus_one_commit"
    core = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "central_conceptual_reflection_claim_recovery",
        "claim": claim,
        "recovery_disposition": disposition,
        "observed_current_generation": current_generation,
        "observed_current_verified_commit": _portable_commit(current_commit),
        "observed_descendant_verified_commit": (
            _portable_commit(descendant_commit)
            if descendant_commit is not None
            else None
        ),
        "observed_consumption_binding_digest": (
            canonical_digest(observed_binding)
            if isinstance(observed_binding, Mapping)
            else None
        ),
        "authority_nulls": copy.deepcopy(INTAKE_AUTHORITY_NULLS),
    }
    core["recovery_id"] = stable_identifier(
        "central-conceptual-reflection-claim-recovery-v2",
        claim["claim_id"],
        current_generation,
        core["observed_consumption_binding_digest"],
        disposition,
    )
    return {**core, "recovery_digest": canonical_digest(core)}


def consume_committed_central_conceptual_route_reflection_intake(
    *,
    store: DiscoveryTransactionStore,
    descendant_verified_commit: VerifiedCommit,
    packet_artifact_path: str,
    bundle_root: Path | str,
) -> dict[str, Any]:
    """Replay the immutable N+1 state and packet into one consumption receipt."""

    if (
        type(store) is not DiscoveryTransactionStore
        or type(descendant_verified_commit) is not VerifiedCommit
    ):
        _fail("committed intake consumption requires real store capabilities")
    if not isinstance(packet_artifact_path, str):
        _fail("committed intake artifact path must be a string")
    try:
        with store.verified_artifact_context() as context:
            if context.current_generation < descendant_verified_commit.generation:
                _fail("descendant commit is absent from the verified active prefix")
            reopened, artifacts = context.read_artifacts(
                descendant_verified_commit.generation, [packet_artifact_path]
            )
            if _portable_commit(reopened) != _portable_commit(
                descendant_verified_commit
            ):
                _fail("supplied descendant capability differs from the store commit")
            packet_bytes = artifacts[packet_artifact_path]
            source_commit = context.read_commit(reopened.prior_generation)
    except ContractError as exc:
        _fail(f"committed descendant packet cannot be reopened: {exc}")
    try:
        packet_raw = json.loads(packet_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail(f"committed descendant packet is unreadable: {exc}")
    packet = _validated_reflective_packet(packet_raw)
    if packet_bytes != canonical_json(packet) + b"\n":
        _fail("committed descendant packet bytes are not canonical")
    binding = build_central_conceptual_reflection_commit_binding(
        packet=packet,
        packet_artifact_path=packet_artifact_path,
    )
    intake = packet["central_conceptual_route_reflection_intake"]
    if (
        reopened.generation != intake["descendant_effect_commit_generation"]
        or reopened.prior_generation != intake["cycle_input_head_generation"]
        or reopened.state.get("generation") != reopened.generation
        or reopened.state.get("central_conceptual_reflection_consumption")
        != binding
        or _portable_commit(source_commit)
        != intake["source_request"]["cycle_input_head_verified_commit"]
    ):
        _fail("N+1 commit state does not atomically consume the exact source intake")
    validate_active_prefix_central_conceptual_reflection_request(
        intake["source_request"],
        store=store,
        verified_commit=source_commit,
        bundle_root=bundle_root,
    )
    descriptors = [
        copy.deepcopy(dict(row))
        for row in reopened.manifest.get("artifacts", [])
        if row.get("path") == packet_artifact_path
    ]
    if len(descriptors) != 1:
        _fail("descendant packet lacks one exact manifest descriptor")
    core = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "central_conceptual_reflection_consumption_receipt",
        "target_id": intake["target_id"],
        "run_id": intake["run_id"],
        "source_request_id": intake["source_request_id"],
        "source_request_digest": intake["source_request_digest"],
        "intake_claim_id": intake["intake_claim"]["claim_id"],
        "intake_claim_digest": intake["intake_claim"]["claim_digest"],
        "intake_id": intake["intake_id"],
        "intake_digest": intake["content_digest"],
        "packet_id": packet["packet_id"],
        "packet_digest": packet["packet_digest"],
        "packet_artifact_descriptor": descriptors[0],
        "consumption_binding": binding,
        "descendant_verified_commit": _portable_commit(reopened),
        "consumption_status": "consumed_and_recovered_from_immutable_n_plus_one",
        "idempotent_replay": True,
        "authority_nulls": copy.deepcopy(INTAKE_AUTHORITY_NULLS),
    }
    core["consumption_id"] = stable_identifier(
        "central-conceptual-reflection-consumption-v2",
        core["intake_claim_digest"],
        core["intake_digest"],
        core["packet_digest"],
        core["descendant_verified_commit"],
    )
    return {**core, "receipt_digest": canonical_digest(core)}


def validate_central_conceptual_reflection_consumption_receipt(
    raw: Any,
    *,
    store: DiscoveryTransactionStore,
    descendant_verified_commit: VerifiedCommit,
    packet_artifact_path: str,
    bundle_root: Path | str,
) -> dict[str, Any]:
    """Require a retained receipt to equal a fresh immutable replay exactly."""

    receipt = copy.deepcopy(dict(raw)) if isinstance(raw, Mapping) else {}
    expected = consume_committed_central_conceptual_route_reflection_intake(
        store=store,
        descendant_verified_commit=descendant_verified_commit,
        packet_artifact_path=packet_artifact_path,
        bundle_root=bundle_root,
    )
    if receipt != expected:
        _fail("consumption receipt differs from exact N+1 recovery replay")
    return receipt


def _reopen_committed_input(
    *,
    store: DiscoveryTransactionStore,
    verified_commit: VerifiedCommit,
    packet: Mapping[str, Any],
    require_current_head: bool = True,
) -> dict[str, Any]:
    if type(store) is not DiscoveryTransactionStore or type(verified_commit) is not VerifiedCommit:
        _fail("authoritative validation requires a real store and VerifiedCommit")
    descriptor = packet["committed_input_descriptor"]
    path = str(descriptor["path"])
    with store.verified_artifact_context() as context:
        if require_current_head and context.current_generation != verified_commit.generation:
            _fail("central-route source commit is no longer the current theory head")
        if not require_current_head and context.current_generation < verified_commit.generation:
            _fail("central-route source commit is absent from the verified active prefix")
        reopened, artifacts = context.read_artifacts(
            verified_commit.generation, [path]
        )
    portable = _portable_commit(reopened)
    if (
        portable != _portable_commit(verified_commit)
        or portable != packet["verified_commit"]
    ):
        _fail("packet, supplied capability, and store commit identities differ")
    data = artifacts[path]
    if (
        bytes_digest(data) != descriptor["sha256"]
        or len(data) != descriptor["size_bytes"]
    ):
        _fail("committed central-route input differs from its manifest descriptor")
    try:
        raw = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail(f"committed central-route input is unreadable: {exc}")
    committed_input = validate_committed_route_input(raw)
    if data != canonical_json(committed_input) + b"\n":
        _fail("committed central-route input bytes are not canonical")
    if (
        committed_input["target_id"] != store.target_id
        or committed_input["run_id"] != store.run_id
    ):
        _fail("committed central-route input crossed the transaction namespace")
    return committed_input


def _validate_live_central_conceptual_reflection_request(
    raw: Any,
    *,
    store: DiscoveryTransactionStore,
    verified_commit: VerifiedCommit,
    bundle_root: Path | str,
    require_current_head: bool,
) -> dict[str, Any]:
    """Reopen the complete source closure at its head or active ancestor."""

    request = decode_central_conceptual_reflection_request(raw)
    before = _snapshot_bundle(
        bundle_root, request["source_packet"]["commission_id"]
    )
    if before != request["source_bundle_manifest"]:
        _fail("retained bundle manifest differs from current immutable files")
    packet = (
        _authoritative_packet(
            request["source_packet"], bundle_root=bundle_root, store=store
        )
        if require_current_head
        else _active_prefix_packet(
            request["source_packet"], bundle_root=bundle_root, store=store
        )
    )
    after = _snapshot_bundle(bundle_root, packet["commission_id"])
    if after != before:
        _fail("central-route bundle changed during authoritative replay")
    committed_input = _reopen_committed_input(
        store=store,
        verified_commit=verified_commit,
        packet=packet,
        require_current_head=require_current_head,
    )
    expected_input = {
        "path": packet["committed_input_descriptor"]["path"],
        "file_sha256": packet["committed_input_descriptor"]["sha256"],
        "byte_length": packet["committed_input_descriptor"]["size_bytes"],
        "input_id": committed_input["input_id"],
        "content_digest": committed_input["content_digest"],
    }
    if (
        request["source_committed_input"] != expected_input
        or request["target_id"] != committed_input["target_id"]
        or request["run_id"] != committed_input["run_id"]
        or request["conceptual_ancestry_digest"]
        != committed_input["conceptual_ancestry_digest"]
        or request["literature_projection_digest"]
        != canonical_digest(committed_input["literature_projection"])
    ):
        _fail("request is detached from its exact committed conceptual input")
    return request


def validate_authoritative_central_conceptual_reflection_request(
    raw: Any,
    *,
    store: DiscoveryTransactionStore,
    verified_commit: VerifiedCommit,
    bundle_root: Path | str,
) -> dict[str, Any]:
    """Require the central source commit to be the exact current input head."""

    return _validate_live_central_conceptual_reflection_request(
        raw,
        store=store,
        verified_commit=verified_commit,
        bundle_root=bundle_root,
        require_current_head=True,
    )


def validate_active_prefix_central_conceptual_reflection_request(
    raw: Any,
    *,
    store: DiscoveryTransactionStore,
    verified_commit: VerifiedCommit,
    bundle_root: Path | str,
) -> dict[str, Any]:
    """Reopen the exact source after a canonical descendant was committed."""

    return _validate_live_central_conceptual_reflection_request(
        raw,
        store=store,
        verified_commit=verified_commit,
        bundle_root=bundle_root,
        require_current_head=False,
    )


def build_central_conceptual_reflection_request(
    *,
    store: DiscoveryTransactionStore,
    verified_commit: VerifiedCommit,
    packet: Mapping[str, Any],
    bundle_root: Path | str,
) -> dict[str, Any]:
    """Build one no-current-effect request at input head N for commit N+1."""

    authoritative_packet = _authoritative_packet(
        packet, bundle_root=bundle_root, store=store
    )
    bundle_manifest = _snapshot_bundle(
        bundle_root, authoritative_packet["commission_id"]
    )
    committed_input = _reopen_committed_input(
        store=store,
        verified_commit=verified_commit,
        packet=authoritative_packet,
    )
    observations, selected = _route_projection(authoritative_packet)
    source_commit = _portable_commit(verified_commit)
    input_binding = {
        "path": authoritative_packet["committed_input_descriptor"]["path"],
        "file_sha256": authoritative_packet["committed_input_descriptor"]["sha256"],
        "byte_length": authoritative_packet["committed_input_descriptor"]["size_bytes"],
        "input_id": committed_input["input_id"],
        "content_digest": committed_input["content_digest"],
    }
    material = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "central_conceptual_route_reflection_request",
        "target_id": committed_input["target_id"],
        "run_id": committed_input["run_id"],
        "central_source_commit_generation": verified_commit.generation,
        "cycle_input_head_generation": verified_commit.generation,
        "descendant_effect_commit_generation": verified_commit.generation + 1,
        "central_source_verified_commit": source_commit,
        "cycle_input_head_verified_commit": copy.deepcopy(source_commit),
        "generation_contract": copy.deepcopy(GENERATION_CONTRACT),
        "source_committed_input": input_binding,
        "conceptual_ancestry_digest": committed_input[
            "conceptual_ancestry_digest"
        ],
        "literature_projection_digest": canonical_digest(
            committed_input["literature_projection"]
        ),
        "source_packet": copy.deepcopy(authoritative_packet),
        "source_packet_digest": authoritative_packet["content_digest"],
        "source_bundle_manifest": bundle_manifest,
        "route_observations": observations,
        "selected_candidate_set": selected,
        "selection_is_set_valued": True,
        "current_theory_effect": copy.deepcopy(CURRENT_THEORY_EFFECT),
        "permitted_descendant_effect": (
            "reflective_synthesis_proposal_at_cycle_input_head_committed_only_by_exact_n_plus_one_cas"
        ),
        "experiment_role": (
            "secondary_descendant_falsifier_only_after_reflective_theory_request"
        ),
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    material["request_id"] = stable_identifier(
        "central-conceptual-reflection-request-v2",
        material["target_id"],
        material["run_id"],
        source_commit,
        source_commit,
        verified_commit.generation + 1,
        material["source_packet_digest"],
        observations,
        selected,
        bundle_manifest["manifest_digest"],
    )
    request = {**material, "content_digest": canonical_digest(material)}
    return validate_authoritative_central_conceptual_reflection_request(
        request,
        store=store,
        verified_commit=verified_commit,
        bundle_root=bundle_root,
    )


__all__ = [
    "AUTHORITY_BOUNDARY",
    "AUTHORITY_NULLS",
    "CURRENT_THEORY_EFFECT",
    "GENERATION_CONTRACT",
    "INTAKE_AUTHORITY_BOUNDARY",
    "INTAKE_AUTHORITY_NULLS",
    "INTAKE_DIRECT_AUTHORITY",
    "CentralConceptualReflectionError",
    "build_central_conceptual_reflection_commit_binding",
    "build_central_conceptual_reflection_request",
    "build_central_conceptual_reflection_intake_claim",
    "build_central_conceptual_route_reflection_intake",
    "consume_committed_central_conceptual_route_reflection_intake",
    "decode_central_conceptual_reflection_request",
    "decode_central_conceptual_route_reflection_intake",
    "recover_central_conceptual_reflection_intake_claim",
    "validate_active_prefix_central_conceptual_reflection_request",
    "validate_authoritative_central_conceptual_reflection_request",
    "validate_central_conceptual_reflection_consumption_receipt",
]
