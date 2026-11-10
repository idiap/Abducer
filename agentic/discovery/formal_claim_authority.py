# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Registered, committed provenance for current formal proof claims.

The proof runtime must never promote an arbitrary caller mapping into a formal
claim.  This module implements the two-stage boundary used instead:

* a registered ``formal-claim-producer`` compiles one typed formalization seed
  from a previously sealed conceptual producer output; and
* only after the producer request, receipt, inputs, registry, and immutable
  output-history bytes are committed can a parent build a formal-claim
  authority for a later proof handoff.

The deterministic compiler intentionally supports a small typed directive.  An
ordinary prose seed produces ``not_ready``.  Extending the supported formal
language requires a versioned producer/validator change; silently inventing a
claim from prose is forbidden.  Neither a ready packet nor its committed
authority establishes truth, checker soundness, theorem status, conceptual
merit, theory preference, or physics value.
"""

from __future__ import annotations

import copy
import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    bytes_digest,
    canonical_digest,
    canonical_json,
    resolve_workspace_path,
    safe_relative_path,
    stable_identifier,
    validate_payload,
)
from agentic.discovery.receipts import (
    ValidatorBinding,
    ValidatorDependencyProfile,
    validate_operator_receipt_identity,
    validate_operator_request_identity,
    verify_current_validator_authority,
)


SPEC_ROOT = Path(__file__).resolve().parents[1] / "spec"
PRODUCER_INPUT_SCHEMA = (
    SPEC_ROOT / "discovery_formal_claim_producer_input_v2.schema.json"
)
PRODUCER_OUTPUT_SCHEMA = (
    SPEC_ROOT / "discovery_formal_claim_producer_output_v2.schema.json"
)
DIRECTIVE_SCHEMA = SPEC_ROOT / "discovery_formal_claim_directive_v2.schema.json"
AUTHORITY_SCHEMA = SPEC_ROOT / "discovery_formal_claim_authority_v2.schema.json"
REGISTRY_PATH = (
    Path(__file__).resolve().parents[1]
    / "registries"
    / "discovery_operator_registry.yaml"
)
PRODUCER_OPERATOR_ID = "formal-claim-producer"
PRODUCER_OPERATOR_VERSION = "2.0.0"
PRODUCER_REGISTRY_ID = "reflective-discovery-operators"
FORMAL_CLAIM_DIRECTIVE_PREFIX = "abducer-formal-claim-v2:"
_SOURCE_OPERATOR_IDS = {"reflective-theory-synthesizer"}
_INPUT_AUTHORITY_NULLS = {
    "claim_truth": False,
    "checker_soundness": False,
    "theorem_status": False,
    "theory_selection": False,
    "same_cycle_theory_mutation": False,
    "independent_semantic_authorship": False,
    "physics_value": False,
}
_AUTHORITY_NULLS = {
    **_INPUT_AUTHORITY_NULLS,
    "proof_success": False,
}

ArtifactLoader = Callable[[str], bytes]


def _self_digest(value: Mapping[str, Any], field: str = "content_digest") -> str:
    return canonical_digest({key: item for key, item in value.items() if key != field})


def _decode_object(data: bytes, label: str) -> dict[str, Any]:
    if type(data) is not bytes:
        raise ContractError(f"{label} must be immutable bytes")
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} is not UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{label} is not a JSON object")
    return value


def _decode_array(data: bytes, label: str) -> list[dict[str, Any]]:
    if type(data) is not bytes:
        raise ContractError(f"{label} must be immutable bytes")
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} is not UTF-8 JSON") from exc
    if not isinstance(value, list) or not all(
        isinstance(row, dict) for row in value
    ):
        raise ContractError(f"{label} is not an array of JSON objects")
    return value


def _workspace_loader(workspace: Path) -> ArtifactLoader:
    root = workspace.resolve()

    def load(relative_path: str) -> bytes:
        path = resolve_workspace_path(root, relative_path, must_exist=True)
        return path.read_bytes()

    return load


def _descriptor_bytes(
    descriptor: Mapping[str, Any],
    *,
    loader: ArtifactLoader,
    expected_namespace: Namespace,
    label: str,
) -> bytes:
    if not isinstance(descriptor, Mapping):
        raise ContractError(f"{label} descriptor must be an object")
    namespace = Namespace.from_mapping(descriptor.get("namespace", {}))
    expected_namespace.assert_matches(namespace, context=label)
    path = safe_relative_path(str(descriptor.get("path", ""))).as_posix()
    data = loader(path)
    if (
        bytes_digest(data) != descriptor.get("sha256")
        or len(data) != descriptor.get("size_bytes")
    ):
        raise ContractError(f"{label} bytes differ from their sealed descriptor")
    return data


def formalization_seed_rows(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Enumerate exact formalization seeds without widening global feedback rows."""

    if not isinstance(packet, Mapping):
        raise ContractError("formalization source packet must be an object")
    rows: list[dict[str, Any]] = []
    packet_id = str(packet.get("packet_id") or "")
    packet_digest = str(packet.get("packet_digest") or "")
    systems = packet.get("conceptual_systems")
    if not packet_id or not packet_digest or not isinstance(systems, list):
        raise ContractError("formalization source packet lacks systems or identity")
    for system in systems:
        if not isinstance(system, Mapping):
            raise ContractError("formalization source system is not an object")
        system_id = str(system.get("system_id") or "")
        seeds = system.get("formalization_seeds")
        if not system_id or not isinstance(seeds, list):
            raise ContractError("formalization source system lacks typed seeds")
        system_digest = canonical_digest(system)
        for index, seed in enumerate(seeds):
            if not isinstance(seed, str) or not seed.strip():
                raise ContractError("formalization seed must be non-empty text")
            row_material = {
                "packet_id": packet_id,
                "packet_digest": packet_digest,
                "system_id": system_id,
                "system_digest": system_digest,
                "formalization_seed_index": index,
                "formalization_seed": seed,
            }
            rows.append(
                {
                    "semantic_kind": "formalization_seed",
                    "semantic_id": stable_identifier(
                        "semantic-formalization-seed-v2",
                        packet_id,
                        system_id,
                        index,
                        seed,
                    ),
                    "row_digest": canonical_digest(row_material),
                    "row": row_material,
                }
            )
    return rows


def _source_seed(
    producer_input: Mapping[str, Any], *, loader: ArtifactLoader
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    payload = copy.deepcopy(dict(producer_input))
    validate_payload(payload, PRODUCER_INPUT_SCHEMA)
    if payload["authority_nulls"] != _INPUT_AUTHORITY_NULLS:
        raise ContractError("formal-claim producer input authority nulls differ")
    if payload["producer_generation_mode"] != "registered_deterministic_compiler":
        raise ContractError("formal-claim producer generation mode is not registry-derived")
    if payload["source_theory_generation"] != payload["source_prior_state_version"] + 1:
        raise ContractError("formal-claim source generation is not a direct successor")
    if payload["conceptual_system_ids"] != sorted(payload["conceptual_system_ids"]):
        raise ContractError("formal-claim conceptual system IDs are not canonical")
    preferred_ancestry_ids = payload["theory_ancestry"][
        "preferred_system_ids"
    ]
    if (
        len(payload["conceptual_system_ids"]) != 1
        or not set(payload["conceptual_system_ids"]).issubset(
            preferred_ancestry_ids
        )
    ):
        raise ContractError(
            "formal-claim source must name one system inside the preferred theory set"
        )

    source_request = payload["source_producer_request"]
    source_receipt = payload["source_producer_receipt"]
    validate_operator_request_identity(source_request)
    validate_operator_receipt_identity(source_receipt, source_request)
    source_operator_id = str(source_request["operator"]["operator_id"])
    if (
        source_operator_id not in _SOURCE_OPERATOR_IDS
        or source_receipt["status"] != "succeeded"
        or any(
            row.get("status") != "passed"
            for row in source_receipt["validator_receipts"]
        )
    ):
        raise ContractError("formal-claim source is not a successful registered producer")
    source_namespace = Namespace.from_mapping(source_request["identity"])
    if (
        source_namespace.target_id != payload["target_id"]
        or source_namespace.run_id != payload["run_id"]
        or source_namespace.branch_id != "root"
        or source_namespace.state_version != payload["source_prior_state_version"]
    ):
        raise ContractError("formal-claim source request crossed its theory identity")
    for index, descriptor in enumerate(source_request["input_artifacts"]):
        _descriptor_bytes(
            descriptor,
            loader=loader,
            expected_namespace=source_namespace,
            label=f"source producer input {index}",
        )
    history = source_receipt["output_history_artifacts"]
    if len(history) != 1:
        raise ContractError("formal-claim source requires one immutable output history")
    source_output_bytes = _descriptor_bytes(
        history[0],
        loader=loader,
        expected_namespace=source_namespace,
        label="source producer output history",
    )
    source_output = _decode_object(source_output_bytes, "source producer output")
    validate_payload(source_output, "reflective_conceptual_discovery_packet.schema.json")
    if source_output.get("packet_digest") != canonical_digest(
        {
            key: value
            for key, value in source_output.items()
            if key != "packet_digest"
        }
    ):
        raise ContractError("formal-claim source packet digest mismatch")
    if any(
        source_output.get(field) != expected
        for field, expected in (
            ("target_id", payload["target_id"]),
            ("run_id", payload["run_id"]),
            ("branch_id", "root"),
            ("state_version", payload["source_prior_state_version"]),
        )
    ):
        raise ContractError("formal-claim source output crossed its request identity")

    finalized = copy.deepcopy(dict(payload["finalized_reflection"]))
    validate_payload(finalized, "reflective_conceptual_discovery_packet.schema.json")
    if (
        finalized.get("packet_digest") != payload["finalized_reflection_digest"]
        or finalized.get("packet_digest")
        != canonical_digest(
            {
                key: value
                for key, value in finalized.items()
                if key != "packet_digest"
            }
        )
        or any(
            finalized.get(field) != expected
            for field, expected in (
                ("target_id", payload["target_id"]),
                ("run_id", payload["run_id"]),
                ("branch_id", "root"),
                ("state_version", payload["source_prior_state_version"]),
            )
        )
    ):
        raise ContractError("finalized reflection identity or digest differs")
    if (
        finalized.get("conceptual_systems") != source_output.get("conceptual_systems")
        or finalized.get("reflection_rounds") != source_output.get("reflection_rounds")
        or finalized.get("conceptual_genealogy")
        != source_output.get("conceptual_genealogy")
    ):
        raise ContractError(
            "finalized reflection changed registered source systems, rounds, or genealogy"
        )

    conceptual_authority = copy.deepcopy(dict(payload["conceptual_authority"]))
    if payload["conceptual_authority_digest"] != canonical_digest(
        conceptual_authority
    ):
        raise ContractError("formal-claim conceptual authority digest mismatch")
    preferred_ids = conceptual_authority.get("preferred_system_ids")
    synthesis_evidence = conceptual_authority.get("synthesis_evidence")
    parent_evidence = conceptual_authority.get("parent_evidence")
    if (
        conceptual_authority.get("status") not in {"sealed_unique", "sealed_plural"}
        or conceptual_authority.get("preference_authorized") is not True
        or conceptual_authority.get("proof_ready") is not False
        or preferred_ids != preferred_ancestry_ids
        or not set(payload["conceptual_system_ids"]).issubset(preferred_ids)
        or finalized.get("conceptual_adjudication_evidence") != synthesis_evidence
        or not isinstance(parent_evidence, Mapping)
        or not isinstance(synthesis_evidence, Mapping)
        or payload["theory_ancestry"].get("conceptual_authority_digest")
        != payload["conceptual_authority_digest"]
        or payload["theory_ancestry"].get(
            "parent_adjudication_evidence_digest"
        )
        != parent_evidence.get("evidence_digest")
        or payload["theory_ancestry"].get(
            "synthesis_adjudication_evidence_digest"
        )
        != synthesis_evidence.get("evidence_digest")
    ):
        raise ContractError("formal-claim source lacks exact sealed conceptual authority")
    synthesis = finalized.get("provisional_synthesis", {})
    programme = finalized.get("theoretical_programme")
    if (
        not isinstance(programme, Mapping)
        or finalized.get("generation_mode") != "operator_generated"
        or synthesis.get("authority_status")
        not in {"sealed_unique", "sealed_plural"}
        or synthesis.get("investment_authorized") is not True
        or synthesis.get("preferred_system_ids") != preferred_ids
        or programme.get("authority_status") != synthesis.get("authority_status")
        or programme.get("investment_authorized") is not True
        or programme.get("conceptual_system_ids") != preferred_ids
        or programme.get("programme_id") != payload["source_theory_programme_id"]
        or canonical_digest(programme) != payload["source_theory_programme_digest"]
    ):
        raise ContractError("formal-claim source theory programme differs")
    system_ids = sorted(
        str(row.get("system_id"))
        for row in finalized.get("conceptual_systems", [])
        if isinstance(row, Mapping)
    )
    if system_ids != sorted(set(system_ids)) or not set(
        payload["conceptual_system_ids"]
    ).issubset(system_ids):
        raise ContractError("formal-claim source omits a canonical preferred system")
    matching = [
        row
        for row in formalization_seed_rows(finalized)
        if row["semantic_id"] == payload["source_semantic_row_id"]
    ]
    if len(matching) != 1:
        raise ContractError("formal-claim source seed is absent or non-unique")
    seed_row = matching[0]
    if seed_row["row"]["system_id"] not in payload["conceptual_system_ids"]:
        raise ContractError("formal-claim source seed belongs to an unselected system")
    support = finalized.get("support_probe", {})
    if (
        support.get("disposition") not in {"no_probe_needed", "proposed"}
        or support.get("receipt_ids") != []
        or support.get("reflective_assimilation_event_ids") != []
    ):
        raise ContractError(
            "formal-claim source contains same-cycle support-result ancestry"
        )
    literature_basis = finalized.get("literature_basis", {})
    if (
        literature_basis.get("freshness_status") != "current"
        or literature_basis.get("selected_snapshot_id")
        != payload["literature_authority"]["snapshot_id"]
        or literature_basis.get("selected_snapshot_digest")
        != payload["literature_authority"]["snapshot_digest"]
    ):
        raise ContractError("formal-claim source literature differs from the finalized packet")
    return payload, finalized, seed_row


def _formalization_readiness_rejection(
    finalized: Mapping[str, Any], seed_row: Mapping[str, Any]
) -> dict[str, str] | None:
    selected_system = next(
        row
        for row in finalized["conceptual_systems"]
        if row["system_id"] == seed_row["row"]["system_id"]
    )
    gates = finalized.get("stage_gates", {})
    required_gates = (
        "G0_essential_relevance",
        "G0L_literature_rebase",
        "G1_genuine_transformation",
        "G3_unification",
        "G5_reflective_resilience",
        "G6_truth_apt_articulation",
    )
    if selected_system.get("lifecycle_state") not in {
        "formalization_ready",
        "proof_ready",
    } or any(gates.get(name) != "pass" for name in required_gates):
        return {
            "code": "source_not_formalization_ready",
            "detail": (
                "The selected preferred system has not reached the explicit "
                "formalization-ready lifecycle and gate vector."
            ),
        }
    return None


def validate_formal_claim_producer_input(
    producer_input: Mapping[str, Any], *, workspace: Path
) -> dict[str, Any]:
    """Reopen every source descriptor used by one producer input."""

    payload, _source, _row = _source_seed(
        producer_input, loader=_workspace_loader(workspace)
    )
    return payload


def validate_formal_claim_producer_input_with_loader(
    producer_input: Mapping[str, Any], *, loader: ArtifactLoader
) -> dict[str, Any]:
    """Reopen a producer input from an explicit immutable artifact loader."""

    payload, _source, _row = _source_seed(producer_input, loader=loader)
    return payload


def build_formal_claim_producer_input(
    *,
    workspace: Path,
    source_producer_request: Mapping[str, Any],
    source_producer_receipt: Mapping[str, Any],
    finalized_reflection: Mapping[str, Any],
    conceptual_authority: Mapping[str, Any],
    branch_binding: Mapping[str, Any],
    concept_id: str,
    source_semantic_row_id: str,
    literature_authority: Mapping[str, Any],
) -> dict[str, Any]:
    """Derive one producer envelope without accepting a caller claim body.

    The caller selects only a committed branch concept and one existing
    formalization-seed row.  Claim text, adapter, and execution plan are absent
    from this API and can arise only from the registered deterministic compiler.
    The canonical cycle independently re-derives every field before commit.
    """

    finalized = copy.deepcopy(dict(finalized_reflection))
    conceptual = copy.deepcopy(dict(conceptual_authority))
    binding = copy.deepcopy(dict(branch_binding))
    literature = copy.deepcopy(dict(literature_authority))
    validate_payload(
        finalized, "reflective_conceptual_discovery_packet.schema.json"
    )
    if finalized.get("packet_digest") != canonical_digest(
        {
            key: value
            for key, value in finalized.items()
            if key != "packet_digest"
        }
    ):
        raise ContractError("formal-claim input builder received a stale reflection")
    preferred_ids = conceptual.get("preferred_system_ids")
    parent_evidence = conceptual.get("parent_evidence")
    synthesis_evidence = conceptual.get("synthesis_evidence")
    branch_system_ids = binding.get("conceptual_system_ids")
    concept_ids = binding.get("concept_ids")
    if (
        conceptual.get("status") not in {"sealed_unique", "sealed_plural"}
        or conceptual.get("preference_authorized") is not True
        or conceptual.get("proof_ready") is not False
        or not isinstance(preferred_ids, list)
        or not isinstance(parent_evidence, Mapping)
        or not isinstance(synthesis_evidence, Mapping)
        or not isinstance(branch_system_ids, list)
        or not isinstance(concept_ids, list)
        or concept_id not in concept_ids
    ):
        raise ContractError(
            "formal-claim input builder requires one sealed preferred branch concept"
        )
    selected_system_ids = [
        system_id
        for system_id in preferred_ids
        if system_id in branch_system_ids
    ]
    seed_rows = [
        row
        for row in formalization_seed_rows(finalized)
        if row["semantic_id"] == source_semantic_row_id
    ]
    if (
        not selected_system_ids
        or len(seed_rows) != 1
        or seed_rows[0]["row"]["system_id"] not in selected_system_ids
    ):
        raise ContractError(
            "formal-claim input builder seed is not unique inside the preferred branch"
        )
    programme = finalized.get("theoretical_programme")
    if not isinstance(programme, Mapping):
        raise ContractError("formal-claim input builder lacks a theory programme")
    target_id = str(finalized["target_id"])
    run_id = str(finalized["run_id"])
    prior_state_version = int(finalized["state_version"])
    branch_id = str(binding.get("branch_id") or "")
    hypothesis_id = str(binding.get("hypothesis_id") or "")
    source_system_ids = [seed_rows[0]["row"]["system_id"]]
    conjecture_id = stable_identifier(
        "formal-conjecture-v2",
        target_id,
        run_id,
        prior_state_version + 1,
        branch_id,
        hypothesis_id,
        concept_id,
        source_system_ids,
        source_semantic_row_id,
    )
    payload = {
        "schema_version": 2,
        "input_kind": "registered_formal_claim_compilation",
        "target_id": target_id,
        "run_id": run_id,
        "source_prior_state_version": prior_state_version,
        "source_theory_generation": prior_state_version + 1,
        "branch_id": branch_id,
        "hypothesis_id": hypothesis_id,
        "concept_id": concept_id,
        "conceptual_system_ids": source_system_ids,
        "conjecture_id": conjecture_id,
        "source_producer_request": copy.deepcopy(dict(source_producer_request)),
        "source_producer_receipt": copy.deepcopy(dict(source_producer_receipt)),
        "finalized_reflection": finalized,
        "finalized_reflection_digest": finalized["packet_digest"],
        "conceptual_authority": conceptual,
        "conceptual_authority_digest": canonical_digest(conceptual),
        "source_semantic_kind": "formalization_seed",
        "source_semantic_row_id": source_semantic_row_id,
        "source_theory_programme_id": programme["programme_id"],
        "source_theory_programme_digest": canonical_digest(programme),
        "literature_authority": literature,
        "theory_ancestry": {
            "conceptual_authority_digest": canonical_digest(conceptual),
            "parent_adjudication_evidence_digest": parent_evidence[
                "evidence_digest"
            ],
            "synthesis_adjudication_evidence_digest": synthesis_evidence[
                "evidence_digest"
            ],
            "preferred_system_ids": copy.deepcopy(preferred_ids),
        },
        "producer_generation_mode": "registered_deterministic_compiler",
        "no_same_cycle_experiment_ancestry": True,
        "authority_nulls": copy.deepcopy(_INPUT_AUTHORITY_NULLS),
    }
    return validate_formal_claim_producer_input(payload, workspace=workspace)


def _adapter_contract(
    claim: Mapping[str, Any], adapter: str, plan: Mapping[str, Any]
) -> None:
    claim_kind = claim.get("claim_kind")
    plan_kind = plan.get("kind")
    expected = {
        "exact": ({"exact_equality", "exact_integer_predicate"}, "builtin_worker"),
        "finite_model": ({"finite_model"}, "builtin_worker"),
        "lean": ({"lean_proposition"}, "lean"),
        "command": ({"external_checker_claim"}, "external_checker"),
    }
    if adapter not in expected:
        raise ContractError(f"unsupported proof adapter: {adapter!r}")
    claim_kinds, required_plan = expected[adapter]
    if claim_kind not in claim_kinds or plan_kind != required_plan:
        raise ContractError("formal claim, proof adapter, and execution plan disagree")
    if adapter == "lean" and not str(claim.get("proof_term") or "").strip():
        raise ContractError("ready Lean claim requires a non-empty proof term")
    if adapter == "command" and (
        not str(plan.get("checker_identity") or "").strip()
        or not str(plan.get("checker_version") or "").strip()
    ):
        raise ContractError("ready external checker requires registered identity and version")


def _compile_seed(seed: str) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    if not seed.startswith(FORMAL_CLAIM_DIRECTIVE_PREFIX):
        return None, {
            "code": "untyped_formalization_seed",
            "detail": "The selected conceptual seed is prose, not a typed v2 formal-claim directive.",
        }
    encoded = seed.removeprefix(FORMAL_CLAIM_DIRECTIVE_PREFIX).encode("utf-8")
    candidate: dict[str, Any] | None = None
    try:
        candidate = _decode_object(encoded, "formal-claim directive")
        if encoded != canonical_json(candidate):
            raise ContractError("The formal-claim directive is not canonical JSON.")
        validate_payload(candidate, DIRECTIVE_SCHEMA)
        if not isinstance(candidate["formal_claim"], Mapping) or not isinstance(
            candidate["execution_plan"], Mapping
        ):
            raise ContractError("The formal claim and execution plan must be objects.")
        _adapter_contract(
            candidate["formal_claim"],
            candidate["proof_adapter"],
            candidate["execution_plan"],
        )
    except (ContractError, TypeError, AttributeError, ValueError) as exc:
        code = (
            "unsupported_proof_adapter"
            if isinstance(candidate, Mapping)
            and candidate.get("proof_adapter")
            not in {"exact", "finite_model", "lean", "command"}
            else (
                "unsupported_formal_claim_kind"
                if isinstance(candidate, Mapping)
                else "untyped_formalization_seed"
            )
        )
        return None, {"code": code, "detail": str(exc)}
    return candidate, None


def _build_formal_claim_producer_output(
    producer_input: Mapping[str, Any], *, loader: ArtifactLoader
) -> dict[str, Any]:
    payload, finalized, seed_row = _source_seed(producer_input, loader=loader)
    candidate, rejection = _compile_seed(seed_row["row"]["formalization_seed"])
    readiness_rejection = _formalization_readiness_rejection(
        finalized,
        seed_row,
    )
    if readiness_rejection is not None:
        candidate = None
        rejection = readiness_rejection
    ready = candidate is not None
    if payload["literature_authority"]["basis_status"] != "current":
        ready = False
        candidate = None
        rejection = {
            "code": "source_ancestry_mismatch",
            "detail": "A current formal claim cannot be produced from non-current literature.",
        }
    source_request = payload["source_producer_request"]
    source_receipt = payload["source_producer_receipt"]
    source_history = source_receipt["output_history_artifacts"][0]
    source_operator_id = source_request["operator"]["operator_id"]
    core: dict[str, Any] = {
        "schema_version": 2,
        "output_kind": "registered_formal_claim_producer_output",
        "target_id": payload["target_id"],
        "run_id": payload["run_id"],
        "source_prior_state_version": payload["source_prior_state_version"],
        "source_theory_generation": payload["source_theory_generation"],
        "branch_id": payload["branch_id"],
        "hypothesis_id": payload["hypothesis_id"],
        "concept_id": payload["concept_id"],
        "conceptual_system_ids": copy.deepcopy(payload["conceptual_system_ids"]),
        "conjecture_id": payload["conjecture_id"],
        "source_operator_id": source_operator_id,
        "source_operator_request_id": source_request["request_id"],
        "source_operator_receipt_id": source_receipt["receipt_id"],
        "source_operator_receipt_digest": source_receipt["receipt_digest"],
        "source_output_path": source_history["path"],
        "source_output_digest": source_history["sha256"],
        "source_finalized_reflection_id": finalized["packet_id"],
        "source_finalized_reflection_digest": finalized["packet_digest"],
        "source_conceptual_authority_digest": payload[
            "conceptual_authority_digest"
        ],
        "source_semantic_kind": seed_row["semantic_kind"],
        "source_semantic_row_id": seed_row["semantic_id"],
        "source_semantic_row_digest": seed_row["row_digest"],
        "source_theory_programme_id": payload["source_theory_programme_id"],
        "source_theory_programme_digest": payload["source_theory_programme_digest"],
        "literature_authority": copy.deepcopy(payload["literature_authority"]),
        "literature_authority_digest": canonical_digest(payload["literature_authority"]),
        "theory_ancestry": copy.deepcopy(payload["theory_ancestry"]),
        "theory_ancestry_digest": canonical_digest(payload["theory_ancestry"]),
        "producer_generation_mode": payload["producer_generation_mode"],
        "status": "ready" if ready else "not_ready",
        "rejection_reason": None if ready else rejection,
        "display_statement": (
            candidate["display_statement"]
            if ready and candidate is not None
            else seed_row["row"]["formalization_seed"]
        ),
        "formal_claim": copy.deepcopy(candidate["formal_claim"]) if ready else None,
        "formal_claim_digest": (
            canonical_digest(candidate["formal_claim"])
            if ready and candidate is not None
            else None
        ),
        "proof_adapter": str(candidate["proof_adapter"]) if ready else None,
        "execution_plan": copy.deepcopy(candidate["execution_plan"]) if ready else None,
        "execution_plan_digest": (
            canonical_digest(candidate["execution_plan"])
            if ready and candidate is not None
            else None
        ),
        "no_same_cycle_experiment_ancestry": True,
        "authority_nulls": copy.deepcopy(_INPUT_AUTHORITY_NULLS),
    }
    core["output_id"] = stable_identifier(
        "formal-claim-producer-output-v2", canonical_digest(core)
    )
    core["content_digest"] = _self_digest(core)
    validate_formal_claim_producer_output(core)
    return core


def build_formal_claim_producer_output(
    producer_input: Mapping[str, Any], *, workspace: Path
) -> dict[str, Any]:
    """Compile one sealed source seed or return a typed ``not_ready`` packet."""

    return _build_formal_claim_producer_output(
        producer_input,
        loader=_workspace_loader(workspace),
    )


def build_formal_claim_producer_output_with_loader(
    producer_input: Mapping[str, Any], *, loader: ArtifactLoader
) -> dict[str, Any]:
    """Compile from exact caller-supplied immutable bytes, never ambient paths."""

    return _build_formal_claim_producer_output(producer_input, loader=loader)


def validate_formal_claim_producer_output(
    output: Mapping[str, Any]
) -> dict[str, Any]:
    payload = copy.deepcopy(dict(output))
    validate_payload(payload, PRODUCER_OUTPUT_SCHEMA)
    if payload["content_digest"] != _self_digest(payload):
        raise ContractError("formal-claim producer output digest mismatch")
    if payload["source_theory_generation"] != payload["source_prior_state_version"] + 1:
        raise ContractError("formal-claim producer output generation mismatch")
    if payload["conceptual_system_ids"] != sorted(payload["conceptual_system_ids"]):
        raise ContractError("formal-claim producer output systems are not canonical")
    if payload["literature_authority_digest"] != canonical_digest(
        payload["literature_authority"]
    ) or payload["theory_ancestry_digest"] != canonical_digest(
        payload["theory_ancestry"]
    ):
        raise ContractError("formal-claim output ancestry digest mismatch")
    expected_id = stable_identifier(
        "formal-claim-producer-output-v2",
        canonical_digest(
            {
                key: value
                for key, value in payload.items()
                if key not in {"output_id", "content_digest"}
            }
        ),
    )
    if payload["output_id"] != expected_id:
        raise ContractError("formal-claim producer output ID is not content-derived")
    if payload["status"] == "ready":
        if (
            payload["formal_claim_digest"] != canonical_digest(payload["formal_claim"])
            or payload["execution_plan_digest"]
            != canonical_digest(payload["execution_plan"])
        ):
            raise ContractError("ready formal claim or execution-plan digest mismatch")
        _adapter_contract(
            payload["formal_claim"],
            payload["proof_adapter"],
            payload["execution_plan"],
        )
    if payload["authority_nulls"] != _INPUT_AUTHORITY_NULLS:
        raise ContractError("formal-claim output authority nulls differ")
    return payload


def formal_claim_output_semantic_row(
    output: Mapping[str, Any]
) -> dict[str, str]:
    payload = validate_formal_claim_producer_output(output)
    material = {
        "output_id": payload["output_id"],
        "output_digest": payload["content_digest"],
        "status": payload["status"],
        "formal_claim_digest": payload["formal_claim_digest"],
        "source_semantic_row_id": payload["source_semantic_row_id"],
        "source_semantic_row_digest": payload["source_semantic_row_digest"],
    }
    return {
        "semantic_kind": "formal_claim_production",
        "semantic_id": stable_identifier(
            "semantic-formal-claim-production-v2", material
        ),
        "row_digest": canonical_digest(material),
    }


def _registry_operator_row(
    registry: Mapping[str, Any],
    *,
    operator_id: str,
    version: str,
    kind: str,
) -> dict[str, Any]:
    if registry.get("registry_id") != PRODUCER_REGISTRY_ID:
        raise ContractError("formal-claim producer registry ID mismatch")
    rows = [
        row
        for row in registry.get("operators", [])
        if isinstance(row, Mapping) and row.get("operator_id") == operator_id
    ]
    if len(rows) != 1:
        raise ContractError(f"registry row is absent or ambiguous for {operator_id}")
    row = copy.deepcopy(dict(rows[0]))
    if row.get("version") != version or row.get("kind") != kind:
        raise ContractError(f"registry version or kind mismatch for {operator_id}")
    return row


def _committed_registry_binding(registry: Mapping[str, Any]) -> dict[str, Any]:
    return _registry_operator_row(
        registry,
        operator_id=PRODUCER_OPERATOR_ID,
        version=PRODUCER_OPERATOR_VERSION,
        kind="proof",
    )


def _validator_binding(
    row: Mapping[str, Any], *, registry_digest: str
) -> ValidatorBinding:
    command = row.get("command")
    dependencies = row.get("dependency_paths")
    policy = str(row.get("dependency_policy") or "")
    if not isinstance(command, list) or not command or not all(
        isinstance(value, str) and value for value in command
    ):
        raise ContractError("registry validator command is invalid")
    if policy == "derived_repository_closure_v2":
        dependency_paths: tuple[str, ...] = ()
        dependency_profile = ValidatorDependencyProfile.from_mapping(
            row.get("dependency_profile")
        )
        current_registry_digest: str | None = registry_digest
    else:
        if (
            not isinstance(dependencies, list)
            or not dependencies
            or not all(isinstance(value, str) and value for value in dependencies)
        ):
            raise ContractError(
                "registry validator command or dependency closure is invalid"
            )
        dependency_paths = tuple(f"repo://{value}" for value in dependencies)
        dependency_profile = None
        current_registry_digest = None
    return ValidatorBinding(
        validator_id=str(row["validator_id"]),
        version=str(row["version"]),
        command=tuple(command),
        dependency_paths=dependency_paths,
        dependency_policy=policy,
        timeout_seconds=float(row.get("timeout_seconds", 60)),
        dependency_profile=dependency_profile,
        registry_digest=current_registry_digest,
    )


def _verify_receipt_registry_authority(
    receipt: Mapping[str, Any],
    registry: Mapping[str, Any],
    *,
    expected_operator_id: str,
    expected_version: str,
    expected_kind: str,
) -> dict[str, Any]:
    row = _registry_operator_row(
        registry,
        operator_id=expected_operator_id,
        version=expected_version,
        kind=expected_kind,
    )
    if receipt.get("operator") != {
        "operator_id": expected_operator_id,
        "version": expected_version,
        "kind": expected_kind,
    }:
        raise ContractError(f"receipt registry binding differs for {expected_operator_id}")
    validator_rows = row.get("validators")
    if not isinstance(validator_rows, list) or not validator_rows:
        raise ContractError(f"registry lacks validators for {expected_operator_id}")
    registry_digest = canonical_digest(registry)
    expected = {
        str(item["validator_id"]): _validator_binding(
            item, registry_digest=registry_digest
        )
        for item in validator_rows
        if isinstance(item, Mapping)
    }
    actual_rows = receipt.get("validator_receipts")
    if not isinstance(actual_rows, list):
        raise ContractError("operator receipt validator receipts are not an array")
    actual = {
        str(item.get("validator_id")): item
        for item in actual_rows
        if isinstance(item, Mapping)
    }
    if (
        len(expected) != len(validator_rows)
        or len(actual) != len(actual_rows)
        or set(actual) != set(expected)
    ):
        raise ContractError(f"validator set differs from registry for {expected_operator_id}")
    for validator_id, receipt_row in actual.items():
        binding = expected[validator_id]
        if (
            receipt_row.get("validator_version") != binding.version
            or receipt_row.get("status") != "passed"
        ):
            raise ContractError(
                f"validator result differs from registry for {expected_operator_id}/{validator_id}"
            )
        verify_current_validator_authority(
            receipt_row.get("validator_authority", {}),
            binding,
        )
    return row


def _unique_row(
    rows: Any,
    *,
    label: str,
    predicate: Callable[[Mapping[str, Any]], bool],
) -> dict[str, Any]:
    matches = [
        copy.deepcopy(dict(row))
        for row in rows
        if isinstance(row, Mapping) and predicate(row)
    ] if isinstance(rows, list) else []
    if len(matches) != 1:
        raise ContractError(f"{label} has cardinality {len(matches)}, expected one")
    return matches[0]


def _manifest_descriptor(commit: Any, path: str) -> dict[str, Any]:
    matches = [
        copy.deepcopy(dict(row))
        for row in commit.manifest.get("artifacts", [])
        if isinstance(row, Mapping) and row.get("path") == path
    ]
    if len(matches) != 1:
        raise ContractError(f"committed manifest lacks exact artifact {path}")
    return matches[0]


def _expected_literature_authority(cycle: Mapping[str, Any]) -> dict[str, Any]:
    basis = cycle.get("literature_basis", {})
    if (
        basis.get("mode") != "active_current"
        or basis.get("active_investment_allowed") is not True
        or not basis.get("source_routing_pre_map_policy_digest")
        or not basis.get("source_routing_realization_digest")
    ):
        raise ContractError("formal-claim authority requires active-current literature")
    return {
        "authority_kind": "validated_target_scoped_literature_snapshot",
        "snapshot_id": basis["snapshot_id"],
        "snapshot_digest": basis["snapshot_digest"],
        "literature_production_projection_digest": cycle[
            "literature_production_projection_digest"
        ],
        "source_routing_pre_map_policy_digest": basis[
            "source_routing_pre_map_policy_digest"
        ],
        "source_routing_realization_digest": basis[
            "source_routing_realization_digest"
        ],
        "basis_status": "current",
        "consume_before": basis["consume_before"],
        "present_use_evaluated_at": basis["present_use_evaluated_at"],
        "present_use_reason": basis["present_use_reason"],
    }


def _expected_theory_ancestry(cycle: Mapping[str, Any]) -> dict[str, Any]:
    conceptual = cycle.get("conceptual_authority", {})
    parent = conceptual.get("parent_evidence")
    synthesis = conceptual.get("synthesis_evidence")
    if not isinstance(parent, Mapping) or not isinstance(synthesis, Mapping):
        raise ContractError("formal-claim authority lacks committed adjudication evidence")
    return {
        "operator_evidence_digest": cycle["operator_evidence_digest"],
        "conceptual_authority_digest": canonical_digest(conceptual),
        "parent_adjudication_evidence_digest": parent["evidence_digest"],
        "synthesis_adjudication_evidence_digest": synthesis["evidence_digest"],
        "preferred_system_ids": copy.deepcopy(conceptual["preferred_system_ids"]),
    }


def _expected_precommit_theory_ancestry(
    cycle: Mapping[str, Any],
) -> dict[str, Any]:
    """Project only ancestry knowable before the enclosing commit exists."""

    ancestry = _expected_theory_ancestry(cycle)
    ancestry.pop("operator_evidence_digest")
    return ancestry


def _verify_committed_validator_aliases(
    receipt: Mapping[str, Any],
    evidence: Mapping[str, Any],
    *,
    alias_bytes: Mapping[str, bytes],
) -> None:
    expected: dict[tuple[str, int], Mapping[str, Any]] = {}
    for validator in receipt["validator_receipts"]:
        for index, authority_file in enumerate(
            validator["validator_authority"]["files"]
        ):
            expected[(validator["receipt_digest"], index)] = authority_file
    actual: dict[tuple[str, int], Mapping[str, Any]] = {}
    for binding in evidence.get("validator_authority_bindings", []):
        if not isinstance(binding, Mapping) or binding.get("receipt_id") != receipt["receipt_id"]:
            continue
        key = (str(binding["validator_receipt_digest"]), int(binding["file_index"]))
        if key in actual:
            raise ContractError("committed validator authority alias is duplicated")
        actual[key] = binding
    if set(actual) != set(expected):
        raise ContractError("committed validator aliases do not cover the exact receipt authority")
    for key, binding in actual.items():
        authority_file = expected[key]
        path = str(binding["sealed_path"])
        data = alias_bytes[path]
        if (
            binding.get("authority_file") != authority_file
            or binding.get("sealed_sha256") != bytes_digest(data)
            or binding.get("sealed_size_bytes") != len(data)
            or authority_file.get("sha256") != bytes_digest(data)
            or authority_file.get("size_bytes") != len(data)
        ):
            raise ContractError("committed validator authority alias bytes differ")


def _authority_material(
    *,
    commit: Any,
    source_cycle_id: str,
    theory_authorization: Mapping[str, Any],
    registry_path: str,
    registry_bytes: bytes,
    registry: Mapping[str, Any],
    registry_row: Mapping[str, Any],
    evidence_path: str,
    evidence_bytes: bytes,
    evidence: Mapping[str, Any],
    request: Mapping[str, Any],
    receipt: Mapping[str, Any],
    input_path: str,
    input_bytes: bytes,
    producer_input: Mapping[str, Any],
    input_binding: Mapping[str, Any],
    output_path: str,
    output_bytes: bytes,
    output_binding: Mapping[str, Any],
    output: Mapping[str, Any],
    feedback_path: str,
    feedback_bytes: bytes,
    feedback_edge: Mapping[str, Any],
    semantic_projection: Mapping[str, Any],
) -> dict[str, Any]:
    semantic = formal_claim_output_semantic_row(output)
    authority_theory_ancestry = {
        "operator_evidence_digest": evidence["evidence_digest"],
        **copy.deepcopy(output["theory_ancestry"]),
    }
    authority: dict[str, Any] = {
        "schema_version": 2,
        "authority_kind": "committed_registered_formal_claim",
        "producer_registry_id": PRODUCER_REGISTRY_ID,
        "producer_registry_digest": canonical_digest(registry),
        "producer_registry_row_digest": canonical_digest(registry_row),
        "producer_registry_path": registry_path,
        "producer_registry_file_digest": bytes_digest(registry_bytes),
        "producer_operator_id": PRODUCER_OPERATOR_ID,
        "producer_operator_version": PRODUCER_OPERATOR_VERSION,
        "producer_request_id": request["request_id"],
        "producer_request_digest": request["request_digest"],
        "producer_receipt_id": receipt["receipt_id"],
        "producer_receipt_digest": receipt["receipt_digest"],
        "theory_authorization_digest": theory_authorization[
            "authorization_digest"
        ],
        "theory_authorization_basis_digest": theory_authorization[
            "authorization_basis_digest"
        ],
        "literature_authority_basis_digest": theory_authorization[
            "literature_authority_basis_digest"
        ],
        "source_commit_generation": commit.generation,
        "source_commit_id": commit.commit_id,
        "source_manifest_digest": commit.manifest_digest,
        "source_state_file_digest": commit.state_file_digest,
        "source_state_semantic_digest": commit.state_semantic_digest,
        "operator_evidence_path": evidence_path,
        "operator_evidence_file_digest": bytes_digest(evidence_bytes),
        "operator_evidence_digest": evidence["evidence_digest"],
        "producer_request_binding_digest": canonical_digest(request),
        "producer_receipt_binding_digest": canonical_digest(receipt),
        "producer_input_artifacts": copy.deepcopy(request["input_artifacts"]),
        "producer_input_path": input_path,
        "producer_input_file_digest": bytes_digest(input_bytes),
        "producer_input_content_digest": canonical_digest(producer_input),
        "producer_input_binding_digest": canonical_digest(input_binding),
        "output_path": output_path,
        "output_file_digest": bytes_digest(output_bytes),
        "producer_output_id": output["output_id"],
        "producer_output_binding_digest": canonical_digest(output_binding),
        "output_content_digest": output["content_digest"],
        "feedback_edge_path": feedback_path,
        "feedback_edge_file_digest": bytes_digest(feedback_bytes),
        "feedback_edge_id": feedback_edge["feedback_edge_id"],
        "feedback_edge_digest": canonical_digest(feedback_edge),
        "semantic_consumer_event_id": semantic_projection[
            "consumer_event_id"
        ],
        "semantic_consumer_event_hash": semantic_projection[
            "consumer_event_hash"
        ],
        "semantic_row_id": semantic["semantic_id"],
        "semantic_row_digest": semantic["row_digest"],
        "source_cycle_id": source_cycle_id,
        "theory_ancestry": authority_theory_ancestry,
        "theory_ancestry_digest": canonical_digest(authority_theory_ancestry),
        **{
            key: copy.deepcopy(output[key])
            for key in (
                "target_id",
                "run_id",
                "source_prior_state_version",
                "source_theory_generation",
                "branch_id",
                "hypothesis_id",
                "concept_id",
                "conceptual_system_ids",
                "conjecture_id",
                "source_operator_id",
                "source_operator_request_id",
                "source_operator_receipt_id",
                "source_operator_receipt_digest",
                "source_output_path",
                "source_output_digest",
                "source_finalized_reflection_id",
                "source_finalized_reflection_digest",
                "source_conceptual_authority_digest",
                "source_semantic_kind",
                "source_semantic_row_id",
                "source_semantic_row_digest",
                "source_theory_programme_id",
                "source_theory_programme_digest",
                "literature_authority",
                "literature_authority_digest",
                "producer_generation_mode",
                "display_statement",
                "formal_claim",
                "formal_claim_digest",
                "proof_adapter",
                "execution_plan",
                "execution_plan_digest",
                "no_same_cycle_experiment_ancestry",
            )
        },
        "literature_consume_before": output["literature_authority"]["consume_before"],
        "ready_status": output["status"],
        "committed_reopen_required": True,
        "authority_nulls": copy.deepcopy(_AUTHORITY_NULLS),
    }
    authority["authority_id"] = stable_identifier(
        "formal-claim-authority-v2",
        authority["source_commit_id"],
        authority["producer_receipt_id"],
        authority["output_content_digest"],
        authority["semantic_row_digest"],
    )
    authority["content_digest"] = _self_digest(authority)
    return authority


def build_formal_claim_authority_v2(
    theory_authorization: object,
) -> dict[str, Any]:
    """Derive claim provenance from one live current canonical-theory capability."""

    # Imported at the authority-bearing boundary to keep the pure registered
    # producer reusable by the canonical cycle without a cycle <-> gate import
    # loop.  The gate itself imports cycle replay helpers.
    from agentic.discovery.committed_projection import (
        load_committed_cycle_projection_sources,
    )
    from agentic.discovery.theory_gate import validate_authorization_at_use
    from agentic.state.discovery_transaction import DiscoveryTransactionStore

    authorization = validate_authorization_at_use(
        theory_authorization,
        allowed_statuses=("verified_active_current",),
    )
    source_generation = int(authorization["committed_state_version"])
    transaction_head_generation = int(
        authorization["transaction_head_generation"]
    )
    store = DiscoveryTransactionStore(
        Path(str(authorization["transaction_root"])).resolve(),
        target_id=str(authorization["target_id"]),
        run_id=str(authorization["run_id"]),
    )
    sources = load_committed_cycle_projection_sources(store, source_generation)
    cycle = sources.canonical_cycle
    cycle_id = str(cycle["cycle_id"])
    cycle_directory = f"branches/root/cycles/{cycle_id}"
    paths = {
        "registry": f"{cycle_directory}/operator-registry.json",
        "evidence": f"{cycle_directory}/operator-evidence.json",
        "feedback": f"{cycle_directory}/feedback-edges.json",
        "events": f"{cycle_directory}/events.json",
    }
    with store.verified_artifact_context() as context:
        if context.current_generation != transaction_head_generation:
            raise ContractError(
                "formal-claim authority capability is stale relative to the transaction head"
            )
        commit, base = context.read_artifacts(
            source_generation,
            list(paths.values()),
        )
        if (
            context.target_id != authorization["target_id"]
            or context.run_id != authorization["run_id"]
            or commit.commit_id != authorization["commit_id"]
            or commit.manifest_digest != authorization["manifest_digest"]
            or cycle_id != authorization["cycle_id"]
            or cycle.get("prior_state_version") != commit.prior_generation
            or cycle.get("next_state_version") != commit.generation
        ):
            raise ContractError("formal-claim authority crossed its live theory capability")
        evidence = _decode_object(base[paths["evidence"]], "operator evidence")
        if evidence != sources.operator_evidence:
            raise ContractError("formal-claim operator evidence differs from committed projection")
        request = _unique_row(
            evidence.get("operator_requests"),
            label="formal-claim producer request",
            predicate=lambda row: row.get("operator", {}).get("operator_id")
            == PRODUCER_OPERATOR_ID,
        )
        validate_operator_request_identity(request)
        receipt = _unique_row(
            evidence.get("operator_receipts"),
            label="formal-claim producer receipt",
            predicate=lambda row: row.get("operator", {}).get("operator_id")
            == PRODUCER_OPERATOR_ID,
        )
        validate_operator_receipt_identity(receipt, request)
        if len(request["input_artifacts"]) != 1 or len(receipt["output_artifacts"]) != 1:
            raise ContractError("formal-claim producer requires one closed input envelope")
        input_binding = _unique_row(
            evidence.get("input_bindings"),
            label="formal-claim sealed input binding",
            predicate=lambda row: row.get("request_id") == request["request_id"]
            and row.get("input_index") == 0,
        )
        output_binding = _unique_row(
            evidence.get("output_bindings"),
            label="formal-claim sealed output binding",
            predicate=lambda row: row.get("receipt_id") == receipt["receipt_id"]
            and row.get("status") == "succeeded",
        )
        alias_paths = {
            str(input_binding["sealed_path"]),
            str(output_binding["sealed_path"]),
        }
        producer_input_path = str(input_binding["sealed_path"])
        producer_output_path = str(output_binding["sealed_path"])
        _commit, producer_bytes = context.read_artifacts(
            source_generation,
            sorted(alias_paths),
        )
        producer_input = _decode_object(
            producer_bytes[producer_input_path],
            "formal-claim producer input",
        )
        source_request = producer_input.get("source_producer_request", {})
        source_receipt = producer_input.get("source_producer_receipt", {})
        validate_operator_request_identity(source_request)
        validate_operator_receipt_identity(source_receipt, source_request)
        relevant_request_ids = {request["request_id"], source_request["request_id"]}
        relevant_receipt_ids = {receipt["receipt_id"], source_receipt["receipt_id"]}
        relevant_input_bindings = [
            copy.deepcopy(dict(row))
            for row in evidence.get("input_bindings", [])
            if isinstance(row, Mapping) and row.get("request_id") in relevant_request_ids
        ]
        relevant_output_bindings = [
            copy.deepcopy(dict(row))
            for row in evidence.get("output_bindings", [])
            if isinstance(row, Mapping) and row.get("receipt_id") in relevant_receipt_ids
        ]
        relevant_validator_bindings = [
            copy.deepcopy(dict(row))
            for row in evidence.get("validator_authority_bindings", [])
            if isinstance(row, Mapping) and row.get("receipt_id") in relevant_receipt_ids
        ]
        all_alias_paths = sorted(
            {
                str(row["sealed_path"])
                for row in [
                    *relevant_input_bindings,
                    *relevant_output_bindings,
                    *relevant_validator_bindings,
                ]
            }
        )
        _commit, alias_bytes = context.read_artifacts(
            source_generation,
            all_alias_paths,
        )

    registry_bytes = base[paths["registry"]]
    current_registry_bytes = REGISTRY_PATH.read_bytes()
    if registry_bytes != current_registry_bytes:
        raise ContractError("committed formal-claim registry bytes are not current")
    registry = _decode_object(registry_bytes, "formal-claim producer registry")
    registry_row = _verify_receipt_registry_authority(
        receipt,
        registry,
        expected_operator_id=PRODUCER_OPERATOR_ID,
        expected_version=PRODUCER_OPERATOR_VERSION,
        expected_kind="proof",
    )
    _verify_receipt_registry_authority(
        source_receipt,
        registry,
        expected_operator_id="reflective-theory-synthesizer",
        expected_version="1.0.0",
        expected_kind="theory",
    )
    _verify_committed_validator_aliases(
        receipt,
        evidence,
        alias_bytes=alias_bytes,
    )
    _verify_committed_validator_aliases(
        source_receipt,
        evidence,
        alias_bytes=alias_bytes,
    )

    if input_binding.get("original_descriptor") != request["input_artifacts"][0]:
        raise ContractError("formal-claim input alias crossed its request descriptor")
    if (
        output_binding.get("original_descriptor") != receipt["output_artifacts"][0]
        or output_binding.get("history_descriptor")
        != receipt["output_history_artifacts"][0]
    ):
        raise ContractError("formal-claim output alias crossed its receipt descriptor")

    original_aliases: dict[str, bytes] = {}
    for binding in relevant_input_bindings:
        original_aliases[str(binding["original_descriptor"]["path"])] = alias_bytes[
            str(binding["sealed_path"])
        ]
    for binding in relevant_output_bindings:
        data = alias_bytes[str(binding["sealed_path"])]
        original_aliases[str(binding["original_descriptor"]["path"])] = data
        original_aliases[str(binding["history_descriptor"]["path"])] = data

    def committed_loader(relative_path: str) -> bytes:
        canonical = safe_relative_path(relative_path).as_posix()
        if canonical not in original_aliases:
            raise ContractError(
                f"formal-claim committed ancestry omits artifact: {canonical}"
            )
        return original_aliases[canonical]

    output = validate_formal_claim_producer_output(
        _decode_object(alias_bytes[producer_output_path], "formal-claim producer output")
    )
    if receipt["status"] != "succeeded" or request["operator"] != receipt["operator"]:
        raise ContractError("formal-claim producer did not finish through its registered binding")
    namespace = Namespace.from_mapping(request["identity"])
    if (
        namespace.target_id != output["target_id"]
        or namespace.run_id != output["run_id"]
        or namespace.branch_id != output["branch_id"]
        or namespace.state_version != output["source_prior_state_version"]
        or source_generation != output["source_theory_generation"]
        or commit.prior_generation != output["source_prior_state_version"]
        or cycle.get("target_id") != output["target_id"]
        or cycle.get("run_id") != output["run_id"]
    ):
        raise ContractError("committed formal-claim producer crossed theory identity")
    _descriptor_bytes(
        request["input_artifacts"][0],
        loader=committed_loader,
        expected_namespace=namespace,
        label="committed formal-claim producer input",
    )
    expected_output = _build_formal_claim_producer_output(
        producer_input,
        loader=committed_loader,
    )
    if output != expected_output:
        raise ContractError("formal-claim output differs from committed input replay")
    if output["status"] != "ready":
        raise ContractError("a not-ready formalization has no current claim authority")

    if (
        producer_input.get("finalized_reflection") != sources.finalized_reflection
        or producer_input.get("conceptual_authority")
        != cycle.get("conceptual_authority")
        or producer_input.get("literature_authority")
        != _expected_literature_authority(cycle)
        or producer_input.get("theory_ancestry")
        != _expected_precommit_theory_ancestry(cycle)
        or cycle.get("experiment_assimilation", {}).get("present") is not False
        or cycle.get("experiment_reflection_receipt") is not None
        or cycle.get("experiment_world_semantics") is not None
    ):
        raise ContractError("formal-claim input differs from committed cycle ancestry")
    source_receipts = sources.producers_by_role.get("reflective_packets", ())
    if not any(dict(row) == source_receipt for row in source_receipts):
        raise ContractError("formal-claim source receipt is not the committed synthesis producer")
    branch_binding = _unique_row(
        cycle.get("identity_map", {}).get("branch_bindings"),
        label="formal-claim identity-map branch binding",
        predicate=lambda row: row.get("branch_id") == output["branch_id"],
    )
    authorized_system_ids = [
        system_id
        for system_id in cycle["conceptual_authority"]["preferred_system_ids"]
        if system_id in branch_binding["conceptual_system_ids"]
    ]
    expected_conjecture_id = stable_identifier(
        "formal-conjecture-v2",
        output["target_id"],
        output["run_id"],
        output["source_theory_generation"],
        output["branch_id"],
        output["hypothesis_id"],
        output["concept_id"],
        output["conceptual_system_ids"],
        output["source_semantic_row_id"],
    )
    if (
        branch_binding.get("hypothesis_id") != output["hypothesis_id"]
        or output["concept_id"] not in branch_binding.get("concept_ids", [])
        or len(output["conceptual_system_ids"]) != 1
        or not set(output["conceptual_system_ids"]).issubset(
            authorized_system_ids
        )
        or output["conjecture_id"] != expected_conjecture_id
    ):
        raise ContractError("formal-claim identity is not derived from the committed branch map")

    feedback_bytes = base[paths["feedback"]]
    feedback_rows = _decode_array(feedback_bytes, "formal-claim feedback edges")
    feedback_edge = _unique_row(
        feedback_rows,
        label="formal-claim feedback edge",
        predicate=lambda row: row.get("producer_receipt_id") == receipt["receipt_id"]
        and row.get("producer_request_id") == request["request_id"]
        and row.get("producer_operator_id") == PRODUCER_OPERATOR_ID,
    )
    validate_payload(feedback_edge, "discovery_feedback_edge.schema.json")
    semantic = formal_claim_output_semantic_row(output)
    semantic_projection = _unique_row(
        feedback_edge.get("semantic_event_projections"),
        label="formal-claim committed semantic projection",
        predicate=lambda row: row.get("output_path")
        == receipt["output_artifacts"][0]["path"]
        and row.get("semantic_kind") == semantic["semantic_kind"]
        and row.get("semantic_id") == semantic["semantic_id"]
        and row.get("row_digest") == semantic["row_digest"],
    )
    events = _decode_array(base[paths["events"]], "formal-claim committed events")
    semantic_event = _unique_row(
        events,
        label="formal-claim semantic consumer event",
        predicate=lambda row: row.get("event_id")
        == semantic_projection["consumer_event_id"]
        and row.get("event_hash") == semantic_projection["consumer_event_hash"]
        and row.get("payload", {}).get("semantic_projection")
        == {**semantic, "source_output_path": receipt["output_artifacts"][0]["path"]},
    )
    if semantic_event["event_hash"] != feedback_edge["consumer_event_hash"]:
        raise ContractError("formal-claim semantic event differs from feedback edge")

    authority = _authority_material(
        commit=commit,
        source_cycle_id=cycle_id,
        theory_authorization=authorization,
        registry_path=paths["registry"],
        registry_bytes=registry_bytes,
        registry=registry,
        registry_row=registry_row,
        evidence_path=paths["evidence"],
        evidence_bytes=base[paths["evidence"]],
        evidence=evidence,
        request=request,
        receipt=receipt,
        input_path=producer_input_path,
        input_bytes=alias_bytes[producer_input_path],
        producer_input=producer_input,
        input_binding=input_binding,
        output_path=producer_output_path,
        output_bytes=alias_bytes[producer_output_path],
        output_binding=output_binding,
        output=output,
        feedback_path=paths["feedback"],
        feedback_bytes=feedback_bytes,
        feedback_edge=feedback_edge,
        semantic_projection=semantic_projection,
    )
    validate_formal_claim_authority_v2(authority)
    return authority


def validate_formal_claim_authority_v2(
    authority: Mapping[str, Any]
) -> dict[str, Any]:
    payload = copy.deepcopy(dict(authority))
    validate_payload(payload, AUTHORITY_SCHEMA)
    if payload["content_digest"] != _self_digest(payload):
        raise ContractError("formal-claim authority digest mismatch")
    if payload["authority_nulls"] != _AUTHORITY_NULLS:
        raise ContractError("formal-claim authority nulls differ")
    if (
        payload["source_theory_generation"]
        != payload["source_prior_state_version"] + 1
        or payload["source_commit_generation"]
        != payload["source_theory_generation"]
    ):
        raise ContractError("formal-claim authority generation binding mismatch")
    if (
        payload["formal_claim_digest"] != canonical_digest(payload["formal_claim"])
        or payload["execution_plan_digest"]
        != canonical_digest(payload["execution_plan"])
        or payload["literature_authority_digest"]
        != canonical_digest(payload["literature_authority"])
        or payload["theory_ancestry_digest"]
        != canonical_digest(payload["theory_ancestry"])
        or payload["literature_consume_before"]
        != payload["literature_authority"]["consume_before"]
    ):
        raise ContractError("formal-claim authority semantic binding mismatch")
    _adapter_contract(
        payload["formal_claim"], payload["proof_adapter"], payload["execution_plan"]
    )
    expected_id = stable_identifier(
        "formal-claim-authority-v2",
        payload["source_commit_id"],
        payload["producer_receipt_id"],
        payload["output_content_digest"],
        payload["semantic_row_digest"],
    )
    if payload["authority_id"] != expected_id:
        raise ContractError("formal-claim authority ID is not content-derived")
    return payload


def reopen_committed_formal_claim_authority_v2(
    theory_authorization: object,
    authority: Mapping[str, Any],
) -> dict[str, Any]:
    """Rebuild an authority from committed bytes and reject detached mappings."""

    payload = validate_formal_claim_authority_v2(authority)
    rebuilt = build_formal_claim_authority_v2(theory_authorization)
    if rebuilt != payload:
        raise ContractError("formal-claim authority differs from committed reconstruction")
    return rebuilt


__all__ = [
    "AUTHORITY_SCHEMA",
    "FORMAL_CLAIM_DIRECTIVE_PREFIX",
    "PRODUCER_INPUT_SCHEMA",
    "PRODUCER_OPERATOR_ID",
    "PRODUCER_OPERATOR_VERSION",
    "PRODUCER_OUTPUT_SCHEMA",
    "build_formal_claim_authority_v2",
    "build_formal_claim_producer_input",
    "build_formal_claim_producer_output",
    "formal_claim_output_semantic_row",
    "formalization_seed_rows",
    "reopen_committed_formal_claim_authority_v2",
    "validate_formal_claim_authority_v2",
    "validate_formal_claim_producer_input",
    "validate_formal_claim_producer_output",
]
