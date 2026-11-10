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
"""Load and render the executable reflective-discovery operator registry.

The registry is deliberately JSON-compatible YAML.  It is the only source used
to derive operator route documentation, so a prose route cannot silently drift
from its executable command, schemas, validator, consumer, or authority edge.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
from typing import Any

try:  # Package import in tests and ``python -m`` execution.
    from agentic.scripts.agentic_common import ROOT, load_json_object
except ImportError:  # Direct script execution keeps its directory on sys.path.
    from agentic_common import ROOT, load_json_object


REGISTRY_PATH = ROOT / "agentic/registries/discovery_operator_registry.yaml"
ROUTES_DOC_PATH = ROOT / "docs/research-methods/discovery-operator-routes.md"
_ALLOWED_KINDS = {
    "theory",
    "literature_search",
    "literature_assimilation",
    "hypothesis",
    "proof",
    "support_probe",
    "reducer",
    "evaluation",
}
_SHELL_PROGRAMS = {"bash", "cmd", "fish", "powershell", "pwsh", "sh", "zsh"}
_EXPERIMENT_OPERATOR_ID = "dynamic-symbolic-simulation-experimenter"
_FORMAL_CLAIM_OPERATOR_ID = "formal-claim-producer"
_CAUSAL_ARTIFACT_OPERATOR_ID = "canonical-causal-artifact-producer"
_CENTRAL_CONCEPTUAL_ROUTE_ID = "central-formal-conceptual-routes-v3"
_CENTRAL_CONCEPTUAL_ROUTE_ORDER = [
    "categorical",
    "hott",
    "category_then_hott",
    "hott_then_category",
    "capable_nonformal",
]
_CENTRAL_CONCEPTUAL_ROUTE_AUTHORITY = {
    "theory_first": True,
    "experiments_secondary_theory_requested_falsifiers_only": True,
    "caller_authored_route_plans_authorized": False,
    "same_cycle_experiment_authority": False,
    "truth_authorized": False,
    "conceptual_merit_authorized": False,
    "physics_value_authorized": False,
    "theorem_authorized": False,
    "continuum_authorized": False,
    "yang_mills_authorized": False,
    "real_verified_commit_required": True,
    "five_postcommit_process_authors_required": True,
    "content_only_set_valued_adjudication": True,
    "hidden_input_independence_authorized": False,
    "cognitive_independence_authorized": False,
    "semantic_independence_authorized": False,
    "creativity_authorized": False,
    "relevance_authorized": False,
    "conceptual_depth_authorized": False,
    "philosophical_understanding_authorized": False,
    "unification_power_authorized": False,
    "formal_advantage_authorized": False,
}
_CAUSAL_ARTIFACT_INPUT_CONTRACT = {
    "artifact_count": 0,
    "media_type": "application/json",
    "required_fields": [],
    "required_parameters": [
        "causal_stage_id",
        "producer_role",
        "artifact_id",
        "artifact_digest",
        "artifact_value",
        "evidence_authority_id",
        "authority_boundary",
    ],
}
_EXPERIMENT_RECEIPT_SCHEMA = "agentic/spec/dynamic_experiment_receipt_v3.schema.json"
_EXPERIMENT_REFLECTION_SCHEMA = (
    "agentic/spec/dynamic_experiment_reflection_receipt_v1.schema.json"
)
_POST_SYNTHESIS_INPUTS = [
    {"input_id": "experiment_spec", "source": "artifact_role", "role": "experiment_spec", "role_index": 0, "operator_id": None, "cardinality": "exactly_one", "schema": "agentic/spec/dynamic_experiment_spec_v3.schema.json"},
    {"input_id": "experiment_receipt", "source": "artifact_role", "role": "experiment_receipt", "role_index": 0, "operator_id": _EXPERIMENT_OPERATOR_ID, "cardinality": "exactly_one", "schema": _EXPERIMENT_RECEIPT_SCHEMA},
    {"input_id": "source_reflection_packet", "source": "artifact_role", "role": "reflective_packets", "role_index": 0, "operator_id": "reflective-conceptual-discovery", "cardinality": "exactly_one", "schema": "agentic/spec/reflective_conceptual_discovery_packet.schema.json"},
    {"input_id": "result_reflection_packet", "source": "artifact_role", "role": "reflective_packets", "role_index": 1, "operator_id": "reflective-theory-synthesizer", "cardinality": "exactly_one", "schema": "agentic/spec/reflective_conceptual_discovery_packet.schema.json"},
    {"input_id": "synthesis_operator_receipt", "source": "successful_operator_receipt", "role": None, "role_index": None, "operator_id": "reflective-theory-synthesizer", "cardinality": "exactly_one", "schema": "agentic/spec/discovery_operator_receipt.schema.json"},
]
_POST_SYNTHESIS_DERIVATION_CONTRACT = {
    "experiment_receipt_validated_against_exact_spec": True,
    "result_packet_consumes_experiment_receipt": True,
    "synthesis_receipt_must_succeed": True,
    "source_and_result_packet_digests_bound": True,
    "advertised_as_operator_output": False,
}
_NON_AUTHORITATIVE_REFLECTION_BOUNDARY = {
    "theory_identity_changed": False,
    "ontology_mutation_authorized": False,
    "theory_selected": False,
    "proof_authorized": False,
    "automatic_evidence_relation_authorized": False,
    "schedule_mutation_authorized": False,
}
_FORMAL_CLAIM_DEPENDENCY_PROFILE = {
    "scope": "formal_claim_producer_validator_repository_closure",
    "entry_python_paths": {
        "agentic/scripts/run_discovery_operator_protocol.py": [
            "formal_claim_producer"
        ],
        "agentic/scripts/validate_discovery_operator_protocol.py": [
            "independent_validator"
        ],
        "agentic/scripts/dispatch_discovery_operators.py": [
            "dispatcher_authority"
        ],
        "agentic/scripts/discovery_operator_registry.py": ["registry_authority"],
    },
    "semantic_paths": {
        "agentic/spec/discovery_formal_claim_schedule_binding_v1.schema.json": [
            "schedule_binding_contract"
        ],
        "agentic/registries/discovery_operator_registry.yaml": [
            "operator_registry_semantic_root"
        ],
        "skills/reasoning/formal-claim-producer/SKILL.md": [
            "formal_claim_skill_semantic_root"
        ],
    },
    "authority_boundary": (
        "Exact captured repository-local producer, independent-validator, dispatcher, "
        "registry, skill, schema, recursive import/package-initializer/$ref, and "
        "runtime-pin identity only; no truth, proof, theorem, semantic-independence, "
        "theory-selection, or physics authority."
    ),
    "runtime_distributions": {
        "jsonschema": "jsonschema",
        "referencing": "referencing",
    },
    "registry_path": "agentic/registries/discovery_operator_registry.yaml",
}
_POST_SYNTHESIS_REQUIRED_DEPENDENCIES = {
    "agentic/discovery/contracts.py",
    "agentic/discovery/dependency_authority.py",
    "agentic/experiments/authority.py",
    "agentic/experiments/errors.py",
    "agentic/experiments/reflection.py",
    "agentic/experiments/runtime.py",
    "agentic/spec/discovery_operator_receipt.schema.json",
    "agentic/spec/dynamic_experiment_receipt.schema.json",
    "agentic/spec/dynamic_experiment_receipt_v2.schema.json",
    _EXPERIMENT_RECEIPT_SCHEMA,
    _EXPERIMENT_REFLECTION_SCHEMA,
    "agentic/spec/dynamic_experiment_spec.schema.json",
    "agentic/spec/dynamic_experiment_spec_v2.schema.json",
    "agentic/spec/dynamic_experiment_spec_v3.schema.json",
    "agentic/spec/dynamic_experiment_v3_common.schema.json",
    "agentic/spec/reflective_conceptual_discovery_packet.schema.json",
}


def canonical_digest(payload: Any) -> str:
    """Return a typed SHA-256 digest over canonical JSON."""

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _validate_argv(value: Any, *, context: str) -> list[str]:
    """Require an explicit argv vector and reject shell-evaluation routes."""

    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{context} must be a non-empty argv array")
    program = os.path.basename(value[0]).lower()
    if program in _SHELL_PROGRAMS or "-c" in value[1:]:
        raise ValueError(f"{context} may not route through shell evaluation")
    return value


def _validate_dependency_paths(value: Any, *, context: str) -> list[str]:
    """Require an exact, existing repository-relative semantic closure."""

    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ValueError(f"{context} must be a non-empty repository-relative path array")
    if len(value) != len(set(value)):
        raise ValueError(f"{context} contains duplicate paths")
    normalized: list[str] = []
    for raw in value:
        path = PurePosixPath(raw)
        if path.is_absolute() or ".." in path.parts or "." in path.parts or "\\" in raw:
            raise ValueError(f"{context} contains an unsafe path: {raw!r}")
        candidate = ROOT.joinpath(*path.parts)
        if not candidate.is_file():
            raise ValueError(f"{context} dependency does not exist: {raw}")
        normalized.append(path.as_posix())
    return normalized


def _validate_post_synthesis_artifacts(
    registry: dict[str, Any], operators: list[dict[str, Any]]
) -> None:
    """Enforce reflection as a cycle-derived artifact, never an operator output.

    Reflection exists only after an exact experiment spec/receipt pair has been
    consumed by a successful synthesis.  Encoding that relation separately
    prevents the experiment command from advertising bytes it cannot produce.
    """

    records = registry.get("post_synthesis_artifacts")
    if not isinstance(records, list) or len(records) != 1:
        raise ValueError("registry requires exactly one post-synthesis artifact contract")
    record = records[0]
    if not isinstance(record, dict):
        raise ValueError("post-synthesis artifact contract must be an object")
    required_header = {
        "artifact_id": "dynamic-experiment-post-result-reflection",
        "schema_version": "1.0.0",
        "producer": "canonical-discovery-cycle",
        "derivation_stage": "post_synthesis_after_experiment_result_consumption",
        "conditional": True,
        "schema": _EXPERIMENT_REFLECTION_SCHEMA,
        "builder_symbol": "agentic.experiments.reflection:build_experiment_reflection_receipt",
        "validator_symbol": "agentic.experiments.reflection:validate_experiment_reflection_receipt",
        "dependency_policy": "explicit_local_semantic_closure",
    }
    if any(record.get(key) != value for key, value in required_header.items()):
        raise ValueError("post-synthesis reflection header or implementation binding drift")
    if record.get("required_inputs") != _POST_SYNTHESIS_INPUTS:
        raise ValueError("post-synthesis reflection must bind its exact five causal inputs")
    if record.get("derivation_contract") != _POST_SYNTHESIS_DERIVATION_CONTRACT:
        raise ValueError("post-synthesis reflection derivation contract drift")
    if record.get("authority_boundary") != _NON_AUTHORITATIVE_REFLECTION_BOUNDARY:
        raise ValueError("post-synthesis reflection acquired forbidden theory authority")
    dependencies = set(
        _validate_dependency_paths(
            record.get("dependency_paths"),
            context="post-synthesis reflection dependency_paths",
        )
    )
    missing = sorted(_POST_SYNTHESIS_REQUIRED_DEPENDENCIES - dependencies)
    if missing:
        raise ValueError(
            "post-synthesis reflection semantic closure is incomplete: "
            + ", ".join(missing)
        )
    experiment = next(
        (row for row in operators if row.get("operator_id") == _EXPERIMENT_OPERATOR_ID),
        None,
    )
    if experiment is None or experiment.get("output_schemas") != [
        _EXPERIMENT_RECEIPT_SCHEMA
    ]:
        raise ValueError("dynamic experiment must advertise exactly its v3 receipt output")
    if any(
        _EXPERIMENT_REFLECTION_SCHEMA in row.get("output_schemas", [])
        for row in operators
    ):
        raise ValueError(
            "cycle-derived post-synthesis reflection may not be advertised as an operator output"
        )


def _validate_literature_conditioned_invention_route(
    registry: dict[str, Any],
) -> None:
    """Bind literature use to causal invention and counterfactual reopening."""

    expected = {
        "route_id": "literature-conditioned-invention-v1",
        "route_version": "1.0.0",
        "skill_path": (
            "skills/reasoning/literature-conditioned-invention-forger/SKILL.md"
        ),
        "production_caller": (
            "agentic.discovery:run_registered_literature_conditioned_invention"
        ),
        "authoritative_reopener": (
            "agentic.discovery:validate_literature_conditioned_invention_execution"
        ),
        "supervised_worker": (
            "agentic.scripts.run_literature_conditioned_invention_worker_v1"
        ),
        "execution_schema": (
            "agentic/spec/literature_conditioned_invention_execution_v1.schema.json"
        ),
        "request_before_output_required": True,
        "exact_semantic_claim_warrant_correction_input_required": True,
        "caller_supplied_inventions_allowed": False,
        "caller_supplied_family_labels_allowed": False,
        "minimum_task_grounded_family_count": 6,
        "counterfactual_interventions": [
            "current",
            "historical",
            "no_literature",
            "removal_each",
            "substitution",
            "correction",
            "supersession",
            "retraction",
        ],
        "request_or_invention_identity_counts_as_semantic_delta": False,
        "direct_theory_preference_proof_schedule_experiment_effect": False,
        "source_truth_authority": False,
        "creativity_authority": False,
        "literature_benefit_authority": False,
        "physics_value_authority": False,
        "truth_authority": False,
    }
    if registry.get("canonical_literature_conditioned_invention_route") != expected:
        raise ValueError(
            "canonical literature-conditioned invention route or authority nulls drifted"
        )


def _validate_canonical_proof_route(registry: dict[str, Any]) -> None:
    """Bind production proof reachability to the in-process v3 facade only."""

    expected = {
        "route_id": "canonical-proof-v3",
        "route_version": "3.0.0",
        "production_caller": (
            "agentic.discovery.proof_v3_facade:"
            "run_committed_proof_action_v3"
        ),
        "reconciliation_caller": (
            "agentic.discovery.proof_v3_facade:"
            "reconcile_committed_proof_action_v3"
        ),
        "executor_facade": (
            "agentic.discovery.proof_v3_facade:execute_proof_v3"
        ),
        "worker_module": "agentic.scripts.run_discovery_proof_worker_v3",
        "live_prelaunch_capability_required": True,
        "serializable_cli_available": False,
        "caller_selected_command_allowed": False,
        "caller_selected_attempt_allowed": False,
        "result_intake_terminal_statuses": [
            "proof_result_intake_consumed",
            "proof_result_intake_superseded",
        ],
        "legacy_launch_routes": [
            {
                "route": "agentic.discovery.proof:run_proof_continuation",
                "production_status": "history_only",
                "launch_enabled": False,
            },
            {
                "route": "agentic.scripts.run_discovery_proof_worker",
                "production_status": "history_only",
                "launch_enabled": False,
            },
            {
                "route": "agentic.scripts.run_proof_continuation",
                "production_status": "history_only",
                "launch_enabled": False,
            },
        ],
        "same_cycle_theory_mutation_authorized": False,
        "proof_truth_authority": False,
        "checker_soundness_authority": False,
        "physics_authority": False,
    }
    if registry.get("canonical_proof_route") != expected:
        raise ValueError(
            "canonical proof route or history-only launch bindings drifted"
        )


def _validate_central_conceptual_route(
    registry: dict[str, Any], operators: list[dict[str, Any]]
) -> None:
    """Bind the five-route process wave to its sole typed production facade."""

    expected = {
        "route_id": _CENTRAL_CONCEPTUAL_ROUTE_ID,
        "route_version": "3.0.0",
        "production_status": "active_typed_python_api",
        "invocation_mode": (
            "typed_python_facade_with_live_store_verified_commit_and_process_wave"
        ),
        "generic_dispatch_enabled": False,
        "operator_registry_member": False,
        "python_api": "agentic.discovery:run_central_conceptual_routes",
        "route_registry": (
            "agentic/registries/central_conceptual_route_registry_v3.yaml"
        ),
        "route_registry_loader": (
            "agentic.discovery.central_conceptual_routes_v3:"
            "load_central_route_registry"
        ),
        "structural_packet_validator": (
            "agentic.discovery:decode_central_conceptual_route_packet"
        ),
        "active_current_validator": (
            "agentic.discovery:"
            "reopen_authoritative_central_conceptual_route_packet"
        ),
        "input_schema": (
            "agentic/spec/central_conceptual_route_input_v3.schema.json"
        ),
        "packet_schema": (
            "agentic/spec/central_conceptual_route_packet_v3.schema.json"
        ),
        "matched_route_order": _CENTRAL_CONCEPTUAL_ROUTE_ORDER,
        "matched_process_author_count": 5,
        "process_overlap_required": True,
        "blind_content_set_valued_judge_required": True,
        "live_store_required": True,
        "verified_commit_required": True,
        "caller_authored_route_plans_allowed": False,
        "serializable_cli_available": False,
        "result_effect": (
            "eligible_input_to_central_reflection_n_to_n_plus_1_intake_only"
        ),
        "central_reflection_intake": {
            "source_generation_role": "canonical_input_head_n",
            "descendant_effect_generation_offset": 1,
            "canonical_compare_and_swap_required": True,
            "same_generation_effect_authorized": False,
        },
        "direct_state_write_authorized": False,
        "same_generation_theory_mutation_authorized": False,
        "authority_boundary": _CENTRAL_CONCEPTUAL_ROUTE_AUTHORITY,
    }
    if registry.get("canonical_central_conceptual_route") != expected:
        raise ValueError(
            "canonical central conceptual typed facade or authority boundary drifted"
        )
    route_registry = load_json_object(ROOT / expected["route_registry"])
    if (
        route_registry.get("schema_version") != "3.0.0"
        or route_registry.get("registry_id")
        != "central-formal-conceptual-routes.v3"
        or [
            row.get("route_id")
            for row in route_registry.get("routes", [])
            if isinstance(row, dict)
        ]
        != _CENTRAL_CONCEPTUAL_ROUTE_ORDER
        or route_registry.get("execution_contract")
        != {
            "backend": "research_worker_process_wave",
            "max_workers": 5,
            "terminal_barrier_parties": 5,
            "identical_committed_input_bytes": True,
            "equal_resource_budgets": True,
            "process_overlap_required": True,
            "caller_plans_forbidden": True,
            "experiments": "secondary_theory_requested_falsifiers_only",
        }
        or route_registry.get("authority_boundary")
        != _CENTRAL_CONCEPTUAL_ROUTE_AUTHORITY
    ):
        raise ValueError(
            "canonical central conceptual facade detached from its exact route registry"
        )
    if _CENTRAL_CONCEPTUAL_ROUTE_ID in {
        row["operator_id"] for row in operators
    }:
        raise ValueError(
            "typed canonical central conceptual facade must not be a generic "
            "dispatcher operator"
        )


def _validate_descendant_experiment_cutover(
    registry: dict[str, Any], operators: list[dict[str, Any]]
) -> None:
    """Make N+8 the sole executable experiment route in the registry."""

    route = registry.get("canonical_descendant_experiment_route")
    expected_offsets = list(range(9))
    if (
        not isinstance(route, dict)
        or route.get("route_id") != "canonical-descendant-experiment-v3"
        or route.get("route_version") != "3.0.0"
        or route.get("production_status") != "active_typed_python_api"
        or route.get("invocation_mode")
        != "typed_python_facade_with_parallel_callbacks"
        or route.get("generic_dispatch_enabled") is not False
        or route.get("operator_registry_member") is not False
        or route.get("python_api")
        != "agentic.experiments:run_canonical_descendant_experiment_v3"
        or route.get("active_current_validator")
        != "agentic.experiments:validate_world_v3_descendant_closure"
        or route.get("replay_validator_module")
        != "agentic.scripts.validate_world_v3_descendant_chain"
        or route.get("replay_command")
        != [
            "python",
            "-m",
            "agentic.scripts.validate_world_v3_descendant_chain",
            "--workspace",
            ".",
        ]
        or route.get("replay_is_producer") is not False
        or [row.get("generation_offset") for row in route.get("chronology", [])]
        != expected_offsets
        or any(row.get("cardinality") != 1 for row in route.get("chronology", []))
        or route.get("parallel_world_production") is not True
        or route.get("serial_commit_order") is not True
        or route.get("requires_exact_active_current_head") is not True
        or route.get("result_effect")
        != "later_theory_cycle_reflection_input_only"
        or any(
            route.get(field) is not False
            for field in (
                "current_cycle_theory_mutation_authorized",
                "automatic_theory_selection_authorized",
                "proof_authorized",
                "physics_authority",
            )
        )
    ):
        raise ValueError("canonical descendant experiment chronology drifted")
    policy = registry.get("authority_policy", {})
    if (
        policy.get("same_generation_experiment_authority") is not False
        or policy.get("canonical_experiment_completion_generation_offset") != 8
    ):
        raise ValueError("registry restored same-generation experiment authority")

    by_id = {row["operator_id"]: row for row in operators}
    if "canonical-descendant-experiment-v3" in by_id:
        raise ValueError(
            "typed canonical descendant facade must not be a generic dispatcher operator"
        )
    for operator_id in (
        "canonical-causal-artifact-producer",
        "dynamic-symbolic-simulation-experimenter",
    ):
        historical = by_id.get(operator_id)
        if (
            historical is None
            or historical.get("production_status") != "history_only"
            or historical.get("dispatch_enabled") is not False
            or historical.get("canonical_reachability") is not False
        ):
            raise ValueError(f"historical experiment route was re-enabled: {operator_id}")
    artifact = registry["post_synthesis_artifacts"][0]
    if (
        artifact.get("production_status") != "history_only"
        or artifact.get("dispatch_enabled") is not False
        or artifact.get("canonical_reachability") is not False
        or artifact.get("superseded_by")
        != "canonical-descendant-experiment-v3:N+8"
    ):
        raise ValueError("same-generation post-synthesis reflection was re-enabled")


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    """Load and validate the registry consumed directly by the dispatcher."""

    registry = load_json_object(path)
    operators = registry.get("operators")
    if not isinstance(operators, list) or not operators:
        raise ValueError("operator registry must contain a non-empty operators array")
    ids = [item.get("operator_id") for item in operators if isinstance(item, dict)]
    if len(ids) != len(operators) or len(set(ids)) != len(ids):
        raise ValueError("operator registry contains missing or duplicate operator IDs")
    for row in operators:
        if not isinstance(row.get("version"), str) or not row["version"]:
            raise ValueError(f"operator {row.get('operator_id')} requires an exact version")
        if row.get("kind") not in _ALLOWED_KINDS:
            raise ValueError(f"operator {row.get('operator_id')} has unsupported kind {row.get('kind')!r}")
        contract = row.get("input_contract")
        if row.get("operator_id") == _CAUSAL_ARTIFACT_OPERATOR_ID:
            if contract != _CAUSAL_ARTIFACT_INPUT_CONTRACT:
                raise ValueError(
                    "canonical causal artifact producer requires its exact "
                    "zero-ambient-input parameter contract"
                )
        elif (
            not isinstance(contract, dict)
            or contract.get("artifact_count") != 1
            or contract.get("media_type") != "application/json"
            or not isinstance(contract.get("required_fields"), list)
            or not contract["required_fields"]
        ):
            raise ValueError(f"operator {row['operator_id']} requires an exact one-artifact JSON input contract")
        _validate_argv(row.get("command"), context=f"operator {row['operator_id']} command")
        validators = row.get("validators")
        if not isinstance(validators, list) or not validators:
            raise ValueError(f"operator {row['operator_id']} requires independent validators")
        validator_ids: list[str] = []
        for validator in validators:
            if not isinstance(validator, dict):
                raise ValueError(f"operator {row['operator_id']} validator must be an object")
            validator_ids.append(str(validator.get("validator_id") or ""))
            if not validator_ids[-1] or not isinstance(validator.get("version"), str):
                raise ValueError(f"operator {row['operator_id']} validator requires ID and version")
            _validate_argv(
                validator.get("command"),
                context=f"operator {row['operator_id']} validator {validator_ids[-1]}",
            )
            if row["operator_id"] == _FORMAL_CLAIM_OPERATOR_ID:
                if (
                    validator.get("dependency_policy")
                    != "derived_repository_closure_v2"
                    or validator.get("dependency_profile")
                    != _FORMAL_CLAIM_DEPENDENCY_PROFILE
                    or "dependency_paths" in validator
                ):
                    raise ValueError(
                        "formal-claim producer validator derived dependency profile drift"
                    )
                profile_paths = [
                    *_FORMAL_CLAIM_DEPENDENCY_PROFILE["entry_python_paths"],
                    *_FORMAL_CLAIM_DEPENDENCY_PROFILE["semantic_paths"],
                ]
                _validate_dependency_paths(
                    profile_paths,
                    context="formal-claim producer dependency roots",
                )
            else:
                if (
                    validator.get("dependency_policy")
                    != "explicit_local_semantic_closure"
                ):
                    raise ValueError(
                        f"operator {row['operator_id']} validator {validator_ids[-1]} "
                        "must declare explicit_local_semantic_closure"
                    )
                _validate_dependency_paths(
                    validator.get("dependency_paths"),
                    context=(
                        f"operator {row['operator_id']} validator "
                        f"{validator_ids[-1]} dependency_paths"
                    ),
                )
        if len(validator_ids) != len(set(validator_ids)):
            raise ValueError(f"operator {row['operator_id']} has duplicate validator IDs")
    _validate_post_synthesis_artifacts(registry, operators)
    _validate_literature_conditioned_invention_route(registry)
    _validate_canonical_proof_route(registry)
    _validate_central_conceptual_route(registry, operators)
    _validate_descendant_experiment_cutover(registry, operators)
    return registry


def _routes_license_preamble() -> str:
    """Keep existing SPDX comments when regenerating the owned document body."""
    if not ROUTES_DOC_PATH.exists():
        return ""
    text = ROUTES_DOC_PATH.read_text(encoding="utf-8")
    offset = 0
    while text[offset:].lstrip().startswith("<!--"):
        start = offset + len(text[offset:]) - len(text[offset:].lstrip())
        end = text.find("-->", start)
        if end < 0:
            raise ValueError("unterminated route-document comment")
        if "SPDX-" not in text[start:end]:
            break
        offset = end + 3
        while offset < len(text) and text[offset].isspace():
            offset += 1
    return text[:offset]


def render_routes(registry: dict[str, Any]) -> str:
    """Render the registry body deterministically, retaining license metadata.

    Licensing comments belong to the file rather than the registry projection.
    Preserving that prefix keeps both generation and exact-body validation
    compatible with contributor-aware disclosure headers.
    """

    digest = canonical_digest(registry)
    lines = [
        "# Reflective Discovery Operator Routes",
        "",
        "This file is generated from `agentic/registries/discovery_operator_registry.yaml`.",
        "It documents execution and authority boundaries; registry presence alone is not an execution receipt.",
        "Every command below is an argv vector executed without a shell. Each successful route also requires a separate validator subprocess and a digest-valid receipt.",
        "",
        f"- Registry digest: `{digest}`",
        f"- Parent operator: `{registry['parent_operator']}`",
        "- Canonical state writer: `discovery-epistemic-reducer`",
        "- Experiments: conditional, theory-requested support only",
        "",
    ]
    central_route = registry["canonical_central_conceptual_route"]
    lines.extend(
        [
            "## Canonical central conceptual route producer",
            "",
            f"- Route/version: `{central_route['route_id']}` / `{central_route['route_version']}`",
            f"- Production API: `{central_route['python_api']}`",
            f"- Invocation: `{central_route['invocation_mode']}`",
            "- Generic dispatcher: `disabled`",
            f"- Exact route registry: `{central_route['route_registry']}`",
            f"- Matched route order: `{json.dumps(central_route['matched_route_order'], ensure_ascii=False)}`",
            f"- Structural packet validator: `{central_route['structural_packet_validator']}`",
            f"- Active-current validator: `{central_route['active_current_validator']}`",
            "- Serializable production CLI: `no`",
            "- Execution: five equal-budget process authors with required overlap, a terminal barrier, and one content-only set-valued blind judge.",
            "- Reflection effect: eligible input only for the exact canonical head `N` to compare-and-swap descendant `N+1` intake; no same-generation theory mutation or direct state write.",
            "- Authority: no truth, conceptual-merit, creativity, relevance, depth, philosophical-understanding, unification, formal-advantage, theorem, continuum, Yang–Mills, or physics-value authority.",
            "",
        ]
    )
    descendant_route = registry["canonical_descendant_experiment_route"]
    lines.extend(
        [
            "## Canonical descendant experiment producer",
            "",
            f"- Route/version: `{descendant_route['route_id']}` / `{descendant_route['route_version']}`",
            f"- Production API: `{descendant_route['python_api']}`",
            f"- Invocation: `{descendant_route['invocation_mode']}`",
            "- Generic dispatcher: `disabled`",
            f"- Read-only replay command: `{json.dumps(descendant_route['replay_command'], ensure_ascii=False)}`",
            "- Replay command produces canonical state: `no`",
            "- Chronology: committed theory `N`; anchor `N+1`; five parallel-produced, serially committed worlds `N+2..N+6`; aggregation `N+7`; immutable later-cycle reflection input `N+8`.",
            "- Authority: later-cycle reflection input only; no current-theory mutation, automatic selection, proof, or physics authority.",
            "",
        ]
    )
    for operator in registry["operators"]:
        parent = operator["parent_operator"] or "root"
        command = json.dumps(operator["command"], ensure_ascii=False)
        contract = operator["input_contract"]
        artifact_count = contract["artifact_count"]
        required_fields = ", ".join(
            f"`{item}`" for item in contract["required_fields"]
        )
        required_parameters = ", ".join(
            f"`{item}`" for item in contract.get("required_parameters", [])
        )
        if artifact_count == 0:
            input_envelope = (
                "no input artifacts; request parameters: "
                + (required_parameters or "none")
            )
        else:
            noun = "artifact" if artifact_count == 1 else "artifacts"
            input_envelope = (
                f"exactly {artifact_count} digest-bound "
                f"`{contract['media_type']}` {noun}; required fields: "
                f"{required_fields or 'none'}"
            )
        validator_descriptions: list[str] = []
        for item in operator["validators"]:
            if item["dependency_policy"] == "derived_repository_closure_v2":
                profile = item["dependency_profile"]
                dependency_summary = (
                    f"{len(profile['entry_python_paths'])} Python roots + "
                    f"{len(profile['semantic_paths'])} semantic roots; recursive closure"
                )
            else:
                dependency_summary = (
                    f"{len(item['dependency_paths'])} local semantic dependencies"
                )
            validator_descriptions.append(
                f"{item['validator_id']}@{item['version']} "
                f"{json.dumps(item['command'], ensure_ascii=False)} "
                f"[{item['dependency_policy']}; {dependency_summary}]"
            )
        validators = "; ".join(validator_descriptions)
        lines.extend(
            [
                f"## {operator['operator_id']}",
                "",
                f"- Role: `{operator['role']}`",
                f"- Version/kind: `{operator['version']}` / `{operator['kind']}`",
                f"- Parent: `{parent}`",
                f"- Conditional: `{'yes' if operator['conditional'] else 'no'}`",
                f"- Dispatch enabled: `{'yes' if operator.get('dispatch_enabled', True) else 'no'}`",
                f"- Production status: `{operator.get('production_status', 'active')}`",
                f"- Skill: `{operator['skill_path']}`",
                f"- Command argv: `{command}`",
                f"- Independent validators: `{validators}`",
                f"- Input envelope: {input_envelope}",
                f"- Domain payload schemas: {', '.join(f'`{item}`' for item in operator['input_schemas']) or 'none'}",
                f"- Output schemas: {', '.join(f'`{item}`' for item in operator['output_schemas']) or 'none'}",
                f"- Required consumers: {', '.join(f'`{item}`' for item in operator['required_consumers'])}",
                f"- Allowed state effects: {', '.join(f'`{item}`' for item in operator['allowed_state_effects'])}",
                f"- Feedback effect: {operator['feedback_effect']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Post-synthesis derived artifacts",
            "",
            "These artifacts are not independently dispatched operators. They are derived by the canonical cycle only after their exact causal inputs have been verified.",
            "",
        ]
    )
    for artifact in registry["post_synthesis_artifacts"]:
        input_summary = ", ".join(
            f"{item['input_id']} ({item['source']}:{item['role'] or item['operator_id']}[{item['role_index']}])"
            for item in artifact["required_inputs"]
        )
        lines.extend(
            [
                f"### {artifact['artifact_id']}",
                "",
                f"- Producer/stage: `{artifact['producer']}` / `{artifact['derivation_stage']}`",
                f"- Schema: `{artifact['schema']}`",
                f"- Exact causal inputs: {input_summary}",
                "- Interpretation: records the executed post-result reflection decision; it cannot mutate theory, ontology, selection, proof, evidence relations, or schedule directly.",
                "",
            ]
        )
    lines.extend(
        [
            "## Provenance and commissioning boundaries",
            "",
            "- `frontier-literature-assimilator` never performs or fabricates a remote search. It consumes an already frozen, schema-valid snapshot from the explicit provider boundary: receipt-backed `live` provenance can authorize a bounded current rebase, while inline/static inputs remain `local_only` and block active investment and novelty claims.",
            "- `central-formal-conceptual-routes-v3` is reachable only through its typed live-store/verified-commit facade. Its exact five-route registry, structural decoder, and active-current reopener are validator surfaces, not a serializable producer CLI or a generic dispatcher binding.",
            "- `canonical-descendant-experiment-v3` is invoked only through its typed Python facade. Its locator-based command is a read-only active-current replay validator and is never a producer or generic dispatcher binding.",
            "- `dynamic-symbolic-simulation-experimenter` is a history-only reader. New experiment production must use the typed canonical descendant facade.",
            "- `dynamic-experiment-post-result-reflection` is history-only; the canonical descendant route commits the immutable later-cycle reflection input at `N+8`.",
            "- A route is exercised only when the command ran, every declared output was hashed, the independent validator passed the exact hashes, and the resulting receipt validates against `discovery_operator_receipt.schema.json`.",
            "",
            "## Reusable batch execution",
            "",
            "Use `python -m agentic.scripts.dispatch_discovery_operators --requests <requests.json> --registry <registry.json> --workspace <workspace> --receipts <receipt-root> --manifest <workspace-relative-manifest.json>` to execute caller-prepared digest-bound requests.",
            "The optional manifest records exact receipts and candidate consumers, but fixes `feedback_committed` and every candidate `consumed`/`state_edge_committed` field to `false`. Only the canonical cycle/reducer may later attest those edges.",
            "",
        ]
    )
    return _routes_license_preamble() + "\n".join(lines).rstrip() + "\n"
