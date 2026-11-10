# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Theory-requested experiment triage, immutable execution, and validation."""

from __future__ import annotations

import copy
import datetime as dt
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Mapping

from agentic.discovery.budgets import (
    ResourceGovernor,
    complete_governed_process_environment,
    contained_path,
    minimal_replacement_environment,
    validate_job_id,
    validate_v2_process_event,
)
from agentic.discovery.contracts import (
    ContractError,
    SchemaValidationError,
    canonical_digest,
    stable_identifier,
    utc_now,
    validate_payload,
)

from .adapters import AdapterSpecError, execute_adapter, exact_adapter, finite_model_adapter
from .authority import (
    build_experiment_authority,
    build_experiment_dependency_authority,
    validate_experiment_authority,
)
from .errors import (
    ExperimentAuthorityError,
    ExperimentExecutionError,
    ExperimentMigrationRequired,
    ExperimentOutputError,
    ExperimentReceiptError,
    ExperimentRuntimeError,
    ExperimentSpecError,
)


SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "spec"
TRIAGE_SCHEMA = SCHEMA_ROOT / "dynamic_probe_triage.schema.json"
LEGACY_V2_SPEC_SCHEMA = SCHEMA_ROOT / "dynamic_experiment_spec_v2.schema.json"
LEGACY_V2_RECEIPT_SCHEMA = SCHEMA_ROOT / "dynamic_experiment_receipt_v2.schema.json"
SPEC_SCHEMA = SCHEMA_ROOT / "dynamic_experiment_spec_v3.schema.json"
RECEIPT_SCHEMA = SCHEMA_ROOT / "dynamic_experiment_receipt_v3.schema.json"
ADAPTER_VERSION = "dynamic-experiment-adapters/1.1.0"
RUNTIME_CONTRACT_VERSION = "dynamic-experiment-runtime/3.1.0"
MIGRATION_CONTRACT_VERSION = "dynamic-experiment-v2-migration/1.0.0"
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_CLAIM_KINDS = {"theory_premise", "model_consequence", "calibration", "boundary_condition"}
_TARGET_RELATIONS = {
    "exact_target_consequence",
    "necessary_not_sufficient",
    "toy_or_proxy",
    "calibration_only",
}
_OPERATIONAL_FAILURE_STATUSES = {
    "capability_unavailable",
    "deadline_exhausted",
    "resource_exhausted",
    "solver_failure",
    "invalid_spec",
    "operational_failure",
}
VALIDATOR_ID = "dynamic-experiment-independent-validator"
VALIDATOR_VERSION = "3.1.0"
EXPERIMENT_RECEIPT_SCHEMA_INVALID = "experiment_receipt_schema_invalid"
EXPERIMENT_OUTPUT_CONTRACT_INVALID = "experiment_output_contract_invalid"
RESOURCE_AUTHORITY_BOUNDARY = (
    "validated_current_v2_local_process_protocol_and_recorded_aggregate_"
    "telemetry_with_no_epistemic_scientific_truth_experiment_value_or_"
    "physics_authority"
)
LEGACY_V2_RESOURCE_AUTHORITY_BOUNDARY = (
    "recorded_local_operational_telemetry_not_independently_replayed_"
    "and_not_epistemic_or_external_measurement_authority"
)
_RECEIPT_SEMANTIC_FIELDS = (
    "spec_id", "execution_id", "experiment_id", "branch_id", "target_id",
    "run_id", "state_version",
    "theory_programme_id", "source_theory_programme_digest",
    "source_reflection_packet_digest", "conceptual_system_ids",
    "theoretical_question_id", "adapter", "status", "epistemic_outcome",
    "result_variant", "spec_digest", "authority_digest", "code_digest",
    "environment_digest", "result", "certificate",
    "uncertainty_analysis", "completeness", "validator", "output_digest",
    "transfer_boundary", "theory_effect_contract_digest", "theory_effect",
    "reflective_assimilation", "failure", "resource_authority_boundary",
    "resource_provenance_digest",
)
_V3_SPEC_FIELDS = frozenset(
    {
        "schema_version", "contract_version", "spec_id", "execution_id",
        "precommitted_receipt_id", "experiment_id", "branch_id", "target_id",
        "run_id", "state_version", "theory_programme_id",
        "source_theory_programme_digest", "source_reflection_packet_digest",
        "conceptual_system_ids", "theoretical_question_id",
        "tested_theory_claim", "probe_role", "expected_conceptual_change",
        "triage_digest", "adapter", "model", "preregistration", "controls",
        "seed_policy", "resource_budget", "transfer_boundary",
        "theory_effect_contract", "code_version", "execution_authority",
        "authority_digest", "code_digest", "observed_environment",
        "environment_digest", "created_at", "spec_digest",
    }
)
_V3_RECEIPT_FIELDS = frozenset(
    {
        "schema_version", "contract_version", "receipt_id",
        "receipt_content_digest", "spec_id", "execution_id", "experiment_id",
        "branch_id", "target_id", "run_id", "state_version",
        "theory_programme_id", "source_theory_programme_digest",
        "source_reflection_packet_digest", "conceptual_system_ids",
        "theoretical_question_id", "adapter", "status", "epistemic_outcome",
        "result_variant", "spec_digest", "authority_digest", "code_digest",
        "environment_digest", "started_at", "completed_at", "resource_usage",
        "resource_authority_boundary", "resource_provenance_digest", "result",
        "certificate", "uncertainty_analysis", "completeness", "validator",
        "output_digest", "transfer_boundary", "theory_effect_contract_digest",
        "theory_effect", "reflective_assimilation", "failure",
    }
)
_LEGACY_SPEC_FIELDS = frozenset(
    {
        "experiment_id", "branch_id", "target_id", "run_id", "state_version",
        "theory_programme_id", "source_theory_programme_digest",
        "source_reflection_packet_digest", "conceptual_system_ids",
        "theoretical_question_id", "tested_theory_claim", "probe_role",
        "expected_conceptual_change", "triage_digest", "adapter", "model",
        "preregistration", "controls", "seed_policy", "resource_budget",
        "transfer_boundary", "theory_effect_contract", "code_version",
        "spec_digest", "created_at",
    }
)
_LEGACY_RECEIPT_FIELDS = frozenset(
    {
        "receipt_id", "receipt_content_digest", "experiment_id", "branch_id",
        "target_id", "run_id", "state_version", "theory_programme_id",
        "source_theory_programme_digest", "source_reflection_packet_digest",
        "conceptual_system_ids", "theoretical_question_id", "adapter", "status",
        "epistemic_outcome", "spec_digest", "code_digest", "environment_digest",
        "started_at", "completed_at", "resource_usage",
        "resource_authority_boundary", "resource_provenance_digest", "result",
        "certificate", "uncertainty_analysis", "completeness", "validator",
        "output_digest", "transfer_boundary", "theory_effect_contract_digest",
        "theory_effect", "reflective_assimilation", "failure",
    }
)
_OUTPUT_VARIANTS = frozenset(
    {
        "exact_rational_support", "exact_rational_counterexample",
        "exact_integer_support", "exact_integer_counterexample",
        "sympy_support", "sympy_counterexample", "finite_model_support",
        "finite_model_counterexample", "finite_model_inconclusive",
        "numeric_deterministic_support", "numeric_deterministic_counterexample",
        "sweep_deterministic_support", "sweep_deterministic_counterexample",
        "numeric_stochastic_support", "numeric_stochastic_counterexample",
        "sweep_stochastic_support", "sweep_stochastic_counterexample",
        "lean_support", "hybrid_support", "hybrid_counterexample",
        "operational_capability_unavailable", "operational_deadline_exhausted",
        "operational_resource_exhausted", "operational_solver_failure",
        "operational_invalid_spec", "operational_failure",
    }
)
_MEASUREMENT_DIMENSIONS = frozenset(
    {
        "wall_time_seconds", "cpu_seconds", "peak_memory_bytes", "disk_bytes",
        "network_bytes", "token_count", "request_count", "cost_usd",
    }
)
_OPERATIONAL_TELEMETRY_SENTINEL = {
    "kind": "locally_measured_operational_telemetry_elided_for_replay"
}
def _top_level_digest(
    value: Mapping[str, Any], *excluded_root_fields: str
) -> str:
    """Hash exact nested content while excluding only named root properties."""

    material = copy.deepcopy(dict(value))
    for field in excluded_root_fields:
        material.pop(field, None)
    return canonical_digest(material)


def _schema_version(value: Mapping[str, Any], *, artifact: str) -> int:
    version = value.get("schema_version")
    if version == 2:
        raise ExperimentMigrationRequired(
            "historical_v2_reexecution_required",
            f"historical v2 {artifact} is non-authoritative until explicit v3 reexecution",
        )
    if version != 3:
        raise ExperimentSpecError(
            "unsupported_schema_version",
            f"{artifact} schema_version must be current v3 or historical v2",
        )
    return 3


def _spec_precommit_core(spec: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in spec.items()
        if key
        not in {
            "spec_id",
            "execution_id",
            "precommitted_receipt_id",
            "spec_digest",
        }
    }


def _legacy_v2_spec_projection(spec: Mapping[str, Any]) -> dict[str, Any]:
    projection = {
        key: copy.deepcopy(spec[key])
        for key in _LEGACY_SPEC_FIELDS
        if key in spec
    }
    projection.update(
        {
            "schema_version": 2,
            "environment": copy.deepcopy(spec.get("observed_environment")),
        }
    )
    projection["spec_digest"] = canonical_digest(
        projection, exclude_keys=("spec_digest", "created_at")
    )
    return projection


def _legacy_v2_receipt_projection(
    receipt: Mapping[str, Any], legacy_spec: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    projection = {
        key: copy.deepcopy(receipt[key])
        for key in _LEGACY_RECEIPT_FIELDS
        if key in receipt
    }
    projection["schema_version"] = 2
    if isinstance(projection.get("validator"), Mapping):
        projection["validator"] = dict(projection["validator"])
        projection["validator"]["version"] = "2.0.0"
    if legacy_spec is not None:
        projection["spec_digest"] = legacy_spec["spec_digest"]
    resource_usage = projection.get("resource_usage")
    if isinstance(resource_usage, Mapping):
        projected_usage = copy.deepcopy(dict(resource_usage))
        if projected_usage.get("events"):
            raise ExperimentMigrationRequired(
                "historical_v2_projection_unavailable_for_process_receipt",
                "current v2-supervised process evidence cannot be downgraded into the "
                "historical flat dynamic-experiment process shape",
            )
        measurement = projected_usage.get("resource_measurement")
        if isinstance(measurement, Mapping):
            disk = measurement.get("disk_bytes")
            projected_usage["resource_measurement"] = {
                "wall_time_seconds": {"status": "measured", "enforced": True},
                "cpu_seconds": {"status": "measured", "enforced": True},
                "peak_memory_bytes": {"status": "measured", "enforced": True},
                "disk_bytes": {
                    key: copy.deepcopy(disk[key])
                    for key in (
                        "status",
                        "enforced",
                        "accounting_root",
                        "sample_interval_seconds",
                        "limitation",
                    )
                    if isinstance(disk, Mapping) and key in disk
                },
                **{
                    dimension: copy.deepcopy(measurement[dimension])
                    for dimension in (
                        "network_bytes",
                        "token_count",
                        "request_count",
                        "cost_usd",
                    )
                },
            }
        projection["resource_usage"] = projected_usage
    projection["resource_authority_boundary"] = LEGACY_V2_RESOURCE_AUTHORITY_BOUNDARY
    projection["output_digest"] = experiment_output_digest(projection)
    projection["validator"]["checked_digest"] = projection["output_digest"]
    projection["resource_provenance_digest"] = _resource_provenance_digest(
        projection
    )
    projection["receipt_content_digest"] = _legacy_v2_receipt_semantic_digest(
        projection
    )
    projection["receipt_id"] = stable_identifier(
        "experiment-receipt-v2",
        projection["experiment_id"],
        projection["spec_digest"],
        projection["receipt_content_digest"],
    )
    return projection


def _normalize_theory_claim_registry(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Validate exact claim records bound to the sealed theory/reflection bytes."""

    raw_claims = source.get("registered_theory_claims", [])
    if not isinstance(raw_claims, list):
        raise ContractError("registered_theory_claims must be an array")
    normalized: list[dict[str, Any]] = []
    for raw in raw_claims:
        if not isinstance(raw, Mapping):
            raise ContractError("registered theory claims must be objects")
        core = {
            "claim_id": str(raw.get("claim_id") or "").strip(),
            "claim_kind": str(raw.get("claim_kind") or "").strip(),
            "target_relation": str(raw.get("target_relation") or "").strip(),
            "statement": str(raw.get("statement") or "").strip(),
            "theory_programme_id": str(raw.get("theory_programme_id") or "").strip(),
            "conceptual_system_ids": sorted(
                {str(value).strip() for value in raw.get("conceptual_system_ids", []) if str(value).strip()}
            ),
            "source_theory_programme_digest": str(
                raw.get("source_theory_programme_digest") or ""
            ),
            "source_reflection_packet_digest": str(
                raw.get("source_reflection_packet_digest") or ""
            ),
        }
        if (
            not core["claim_id"]
            or core["claim_kind"] not in _CLAIM_KINDS
            or core["target_relation"] not in _TARGET_RELATIONS
            or not core["statement"]
            or not core["theory_programme_id"]
            or not core["conceptual_system_ids"]
            or _DIGEST.fullmatch(core["source_theory_programme_digest"]) is None
            or _DIGEST.fullmatch(core["source_reflection_packet_digest"]) is None
        ):
            raise ContractError("registered theory claim is incomplete or invalid")
        expected_digest = canonical_digest(core)
        if raw.get("claim_digest") != expected_digest:
            raise ContractError("registered theory claim digest mismatch")
        normalized.append({**core, "claim_digest": expected_digest})
    claim_ids = [row["claim_id"] for row in normalized]
    if len(claim_ids) != len(set(claim_ids)):
        raise ContractError("registered theory claim IDs must be unique")
    return sorted(normalized, key=lambda row: row["claim_id"])


def _receipt_semantic_digest(receipt: Mapping[str, Any]) -> str:
    """Bind every receipt byte except the root self-digest property itself."""

    return _top_level_digest(receipt, "receipt_content_digest")


def _legacy_v2_receipt_semantic_digest(receipt: Mapping[str, Any]) -> str:
    """Reproduce the frozen v2 semantic projection without granting authority."""

    return canonical_digest(
        {
            field: copy.deepcopy(receipt[field])
            for field in _RECEIPT_SEMANTIC_FIELDS
            if field in receipt
        }
    )


def _experiment_output_projection(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Return every authority-bearing result semantic checked by the validator."""

    return {
        field: {"present": field in receipt, "value": receipt.get(field)}
        for field in (
            "status",
            "epistemic_outcome",
            "result_variant",
            "result",
            "certificate",
            "uncertainty_analysis",
            "completeness",
            "failure",
            "theory_effect",
            "reflective_assimilation",
        )
    }


def experiment_output_digest(receipt: Mapping[str, Any]) -> str:
    """Digest the complete experiment output semantics, including failures."""

    return canonical_digest(_experiment_output_projection(receipt))


def _resource_provenance_digest(receipt: Mapping[str, Any]) -> str:
    """Bind recorded local telemetry without treating it as epistemic evidence."""

    return canonical_digest(
        {
            "started_at": receipt.get("started_at"),
            "completed_at": receipt.get("completed_at"),
            "resource_usage": receipt.get("resource_usage"),
            "authority_boundary": receipt.get("resource_authority_boundary"),
        }
    )


def _typed_operational_failure(output: Mapping[str, Any]) -> dict[str, str] | None:
    """Derive the exact typed non-epistemic failure carried by an outcome."""

    status = str(output.get("status") or "")
    if status not in _OPERATIONAL_FAILURE_STATUSES:
        return None
    result = output.get("result") if isinstance(output.get("result"), Mapping) else {}
    stages = result.get("stages") if isinstance(result.get("stages"), list) else []
    terminal = stages[-1] if stages and isinstance(stages[-1], Mapping) else None
    if terminal is not None and terminal.get("status") == status:
        nested = _typed_operational_failure(terminal)
        message = nested["message"] if nested is not None else status
    elif isinstance(result.get("error"), str) and result["error"].strip():
        message = result["error"].strip()
    elif status == "capability_unavailable":
        message = f"required capability unavailable: {result.get('capability', 'unspecified')}"
    elif status in {"deadline_exhausted", "resource_exhausted"}:
        dimension = result.get("dimension") or result.get("budget_status") or "bounded_execution"
        message = f"{status}: {dimension} did not complete within its declared limit"
    else:
        process = result.get("process") if isinstance(result.get("process"), Mapping) else {}
        message = (
            f"{status}: process_status={process.get('status', 'unspecified')} "
            f"returncode={process.get('returncode', 'unspecified')}"
        )
    return {"kind": status, "message": message, "epistemic_effect": "none"}


def _normalized_lean_process(process: Mapping[str, Any]) -> dict[str, Any]:
    """Quotient a separately validated process event for semantic replay."""

    if not isinstance(process, Mapping):
        raise ContractError("Lean process telemetry is not an object")
    return copy.deepcopy(_OPERATIONAL_TELEMETRY_SENTINEL)


def _normalized_operational_output(
    output: Mapping[str, Any], spec: Mapping[str, Any]
) -> dict[str, Any]:
    """Normalize the closed output union using trusted adapter/path rules."""

    fields = (
        "status",
        "epistemic_outcome",
        "result",
        "certificate",
        "uncertainty_analysis",
        "completeness",
        "failure",
    )
    normalized = {
        field: copy.deepcopy(output[field])
        for field in fields
        if field in output
    }
    adapter = str(spec.get("adapter") or "")
    status = str(output.get("status") or "")
    result = normalized.get("result")

    budget_keys = {"budget_status", "dimension", "used", "limit"}
    if (
        status in {"deadline_exhausted", "resource_exhausted"}
        and isinstance(result, Mapping)
        and set(result) == budget_keys
    ):
        normalized_result = copy.deepcopy(dict(result))
        normalized_result["used"] = copy.deepcopy(_OPERATIONAL_TELEMETRY_SENTINEL)
        normalized["result"] = normalized_result

    if adapter == "lean" and isinstance(result, Mapping):
        process = result.get("process")
        if isinstance(process, Mapping):
            normalized_result = copy.deepcopy(dict(result))
            normalized_result["process"] = _normalized_lean_process(process)
            normalized["result"] = normalized_result

    if adapter == "hybrid" and isinstance(result, Mapping):
        stages = result.get("stages")
        planned = spec.get("model", {}).get("stages", [])
        if isinstance(stages, list) and isinstance(planned, list):
            normalized_result = copy.deepcopy(dict(result))
            normalized_stages: list[Any] = []
            for index, stage_output in enumerate(stages):
                if not isinstance(stage_output, Mapping) or index >= len(planned):
                    normalized_stages.append(copy.deepcopy(stage_output))
                    continue
                child_spec = dict(spec)
                child_spec.update(planned[index])
                normalized_stages.append(
                    _normalized_operational_output(stage_output, child_spec)
                )
            normalized_result["stages"] = normalized_stages
            normalized["result"] = normalized_result
    return normalized


def _operational_replay_projection(
    output: Mapping[str, Any], spec: Mapping[str, Any]
) -> dict[str, Any]:
    """Project exact semantics modulo a small enumerated telemetry quotient.

    Field names and object shapes never grant telemetry status.  Scientific
    values named ``used``, ``dimension``, ``limit``, ``pid``, or ``digest``
    therefore remain authoritative unless they occupy a registered path in the
    already schema-closed adapter/status variant.
    """

    normalized = _normalized_operational_output(output, spec)
    return {
        field: {
            "present": field in output,
            "value": normalized.get(field),
        }
        for field in (
            "status",
            "epistemic_outcome",
            "result",
            "certificate",
            "uncertainty_analysis",
            "completeness",
            "failure",
        )
    }


def _closed_mapping(
    value: Any, expected_keys: set[str] | frozenset[str], label: str
) -> Mapping[str, Any]:
    """Require an exact registered object shape, including property absence."""

    if not isinstance(value, Mapping) or set(value) != set(expected_keys):
        actual = sorted(value) if isinstance(value, Mapping) else type(value).__name__
        raise ContractError(
            f"{label} is not schema-closed: expected {sorted(expected_keys)!r}, got {actual!r}"
        )
    return value


def _validate_measurement_boundaries(value: Any, label: str) -> None:
    measurement = _closed_mapping(
        value,
        _MEASUREMENT_DIMENSIONS | {"measurement_schema_version"},
        label,
    )
    if measurement["measurement_schema_version"] != 2:
        raise ContractError(f"{label} is not current measurement schema v2")


def _validate_process_event(value: Any, label: str, *, accepted: bool) -> None:
    if not isinstance(value, Mapping):
        raise ContractError(f"{label} is not an object")
    try:
        validate_v2_process_event(value, accepted=accepted)
    except ValueError as exc:
        raise ContractError(f"{label} is not a valid v2 process event: {exc}") from exc


def _spec_contains_lean(spec: Mapping[str, Any]) -> bool:
    """Return whether the closed adapter plan can launch a Lean process."""

    if spec.get("adapter") == "lean":
        return True
    if spec.get("adapter") != "hybrid":
        return False
    model = spec.get("model")
    stages = model.get("stages") if isinstance(model, Mapping) else None
    return isinstance(stages, list) and any(
        isinstance(stage, Mapping) and stage.get("adapter") == "lean"
        for stage in stages
    )


def _planned_process_bindings(
    spec: Mapping[str, Any],
    output: Mapping[str, Any],
    work_directory: Path | None,
) -> list[tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any], Path]]:
    """Bind ordered nested process events to their plan, output, and workspace."""

    bindings: list[
        tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any], Path]
    ] = []

    def add_lean_binding(
        stage_spec: Mapping[str, Any],
        stage_output: Mapping[str, Any],
        stage_directory: Path | None,
        *,
        label: str,
    ) -> None:
        result = stage_output.get("result")
        if not isinstance(result, Mapping) or result.get("available") is not True:
            return
        event = result.get("process")
        if not isinstance(event, Mapping):
            raise ContractError(f"{label} omits its governed process event")
        if stage_directory is None:
            raise ContractError(
                "process-bearing experiment validation requires its immutable work directory"
            )
        bindings.append((event, stage_output, stage_spec, stage_directory))

    adapter = str(spec.get("adapter") or "")
    if adapter == "lean":
        add_lean_binding(spec, output, work_directory, label="Lean adapter output")
        return bindings
    if adapter != "hybrid":
        return bindings
    model = spec.get("model")
    planned = model.get("stages") if isinstance(model, Mapping) else None
    result = output.get("result")
    executed = result.get("stages") if isinstance(result, Mapping) else None
    if not isinstance(planned, list) or not isinstance(executed, list):
        raise ContractError("hybrid process binding lacks its planned or executed stages")
    if len(executed) > len(planned):
        raise ContractError("hybrid output executed more stages than were planned")
    for index, stage_output in enumerate(executed):
        stage_plan = planned[index]
        if not isinstance(stage_plan, Mapping) or not isinstance(stage_output, Mapping):
            raise ContractError(f"hybrid stage {index} is not an object")
        if stage_plan.get("adapter") != "lean":
            continue
        child_spec = dict(spec)
        child_spec.update(stage_plan)
        stage_directory = (
            contained_path(work_directory, f"stage-{index:02d}")
            if work_directory is not None
            else None
        )
        add_lean_binding(
            child_spec,
            stage_output,
            stage_directory,
            label=f"hybrid Lean stage {index}",
        )
    return bindings


def _validate_process_bindings(
    spec: Mapping[str, Any],
    receipt: Mapping[str, Any],
    resource_usage: Mapping[str, Any],
    work_directory: Path | None,
) -> None:
    """Replay every current v2 process authority and its exact nested binding."""

    root = work_directory.resolve(strict=True) if work_directory is not None else None
    bindings = _planned_process_bindings(spec, receipt, root)
    expected_events = [event for event, _output, _plan, _path in bindings]
    if resource_usage["events"] != expected_events:
        raise ContractError(
            "experiment resource events differ in identity, order, or cardinality "
            "from the executed adapter stages"
        )
    aggregate_measurement = resource_usage["resource_measurement"]
    if bindings and root is not None:
        disk = aggregate_measurement.get("disk_bytes")
        if not isinstance(disk, Mapping) or disk.get("accounting_root") != str(root):
            raise ContractError("experiment aggregate accounting root differs from its workspace")
    for index, (event, stage_output, stage_spec, stage_directory) in enumerate(bindings):
        if event.get("role") != "solver":
            raise ContractError(f"experiment process event {index} has a non-solver role")
        event_status = event.get("status")
        expected_stage_status = (
            "succeeded"
            if event_status == "succeeded"
            else "deadline_exhausted"
            if event_status == "deadline_exhausted"
            else "solver_failure"
        )
        if stage_output.get("status") != expected_stage_status:
            raise ContractError(
                f"experiment process event {index} status differs from its Lean stage"
            )
        command = event.get("command")
        model = stage_spec.get("model")
        requested_executable = (
            str(model.get("executable", "lean")) if isinstance(model, Mapping) else "lean"
        )
        observed_executable = shutil.which(requested_executable)
        expected_executable = (
            str(Path(observed_executable).resolve(strict=True))
            if observed_executable is not None
            else None
        )
        if (
            not isinstance(command, list)
            or len(command) != 2
            or command[0] != expected_executable
            or command[1] != "Probe.lean"
        ):
            raise ContractError(
                f"experiment process event {index} command differs from the current Lean plan"
            )
        if event.get("resource_measurement") != aggregate_measurement:
            raise ContractError(
                f"experiment process event {index} measurement boundary differs from its receipt"
            )
        expected_environment = None
        if event.get("supervision_attempt") is not None:
            base_environment = minimal_replacement_environment(
                stage_directory,
                create_temporary=False,
            )
            expected_environment = complete_governed_process_environment(
                base_environment,
                deadline=resource_usage["deadline"],
                budget=resource_usage["budget"],
            )
        try:
            validate_v2_process_event(
                event,
                accepted=stage_output.get("status") == "succeeded",
                expected_workspace=stage_directory,
                expected_replacement_environment=expected_environment,
                require_live_execution_authority=True,
            )
        except ValueError as exc:
            raise ContractError(
                f"experiment process event {index} fails current v2 replay: {exc}"
            ) from exc


def _independent_adapter_replay(
    spec: Mapping[str, Any], work_directory: Path | None
) -> dict[str, Any]:
    """Replay process adapters in scratch space, never in receipt evidence space."""

    if _spec_contains_lean(spec):
        with tempfile.TemporaryDirectory(prefix="abducer-experiment-replay-") as raw:
            replay_root = Path(raw).resolve(strict=True)
            governor = ResourceGovernor.from_mapping(
                spec["resource_budget"], run_directory=replay_root
            )
            output = execute_adapter(spec, governor, replay_root)
            output["failure"] = _typed_operational_failure(output)
            _validate_adapter_output_contract(output, spec)
            return output
    governor = ResourceGovernor.from_mapping(spec["resource_budget"])
    output = execute_adapter(spec, governor, Path.cwd())
    output["failure"] = _typed_operational_failure(output)
    _validate_adapter_output_contract(output, spec)
    return output


def _validate_adapter_output_contract(
    output: Mapping[str, Any], spec: Mapping[str, Any]
) -> None:
    """Bind each closed public output union to its commissioned adapter/status."""

    required = {
        "status", "epistemic_outcome", "result", "certificate",
        "uncertainty_analysis", "completeness",
    }
    if not required.issubset(output):
        raise ContractError(
            f"adapter output is missing fields {sorted(required - set(output))!r}"
        )
    if "schema_version" not in output and set(output) not in {
        frozenset(required),
        frozenset(required | {"failure"}),
    }:
        raise ContractError(
            f"adapter output has unregistered fields {sorted(set(output) - required - {'failure'})!r}"
        )
    status = str(output["status"])
    outcome = str(output["epistemic_outcome"])
    adapter = str(spec.get("adapter") or "")
    result = output["result"]
    certificate = output["certificate"]
    uncertainty = output["uncertainty_analysis"]
    completeness = output["completeness"]

    if status == "invalid_spec":
        invalid = _closed_mapping(result, {"error"}, "invalid-spec result")
        if (
            not isinstance(invalid["error"], str)
            or not invalid["error"].strip()
            or outcome != "not_evaluated"
            or certificate is not None
            or uncertainty is not None
            or completeness is not None
        ):
            raise ContractError("invalid-spec output carries impossible evidence fields")
        return

    if adapter == "hybrid":
        hybrid = _closed_mapping(
            result, {"stages", "all_stages_completed"}, "hybrid result"
        )
        stages = hybrid["stages"]
        planned = spec.get("model", {}).get("stages", [])
        if (
            not isinstance(stages, list)
            or not stages
            or not isinstance(planned, list)
            or len(stages) > len(planned)
        ):
            raise ContractError("hybrid stage cardinality differs from its sealed model")
        for index, stage_output in enumerate(stages):
            _closed_mapping(
                stage_output,
                {
                    "status", "epistemic_outcome", "result", "certificate",
                    "uncertainty_analysis", "completeness",
                },
                f"hybrid stage {index}",
            )
            child_spec = dict(spec)
            child_spec.update(planned[index])
            _validate_adapter_output_contract(stage_output, child_spec)
        hybrid_completeness = _closed_mapping(
            completeness,
            {"complete", "completed_stages", "planned_stages"},
            "hybrid completeness",
        )
        complete = hybrid["all_stages_completed"] is True
        if (
            hybrid_completeness["complete"] is not complete
            or hybrid_completeness["completed_stages"] != len(stages)
            or hybrid_completeness["planned_stages"] != len(planned)
        ):
            raise ContractError("hybrid result/completeness mismatch")
        hybrid_uncertainty = _closed_mapping(
            uncertainty, {"stage_uncertainties"}, "hybrid uncertainty"
        )
        if hybrid_uncertainty["stage_uncertainties"] != [
            stage["uncertainty_analysis"] for stage in stages
        ]:
            raise ContractError("hybrid uncertainty differs from its ordered stages")
        if complete:
            hybrid_certificate = _closed_mapping(
                certificate, {"kind", "stage_certificates"}, "hybrid certificate"
            )
            if (
                hybrid_certificate["kind"] != "hybrid_stage_chain"
                or hybrid_certificate["stage_certificates"]
                != [stage["certificate"] for stage in stages]
            ):
                raise ContractError("hybrid certificate differs from its ordered stages")
        elif certificate is not None:
            raise ContractError("incomplete hybrid output cannot carry a certificate")
        expected_status = (
            "counterexample"
            if complete and any(stage["status"] == "counterexample" for stage in stages)
            else "succeeded"
            if complete
            else stages[-1]["status"]
        )
        expected_outcome = (
            "falsifies_claim" if expected_status == "counterexample"
            else "supports_within_scope" if expected_status == "succeeded"
            else "not_evaluated"
        )
        if status != expected_status or outcome != expected_outcome:
            raise ContractError("hybrid root status is not derived from its stage chain")
        return

    result_keys = frozenset(result) if isinstance(result, Mapping) else frozenset()
    budget_keys = frozenset({"budget_status", "dimension", "used", "limit"})
    if status in {"deadline_exhausted", "resource_exhausted"} and result_keys == budget_keys:
        budget_result = _closed_mapping(result, budget_keys, "budget-exhaustion result")
        if budget_result["budget_status"] not in {
            "deadline_exhausted", "cpu_exhausted", "out_of_memory",
            "disk_exhausted", "network_exhausted", "token_exhausted",
            "request_exhausted", "spend_exhausted", "input_exhausted",
            "output_exhausted",
        }:
            raise ContractError("budget-exhaustion status is unregistered")
        expected_status = (
            "deadline_exhausted"
            if budget_result["budget_status"] == "deadline_exhausted"
            else "resource_exhausted"
        )
        closed_completeness = _closed_mapping(
            completeness, {"complete"}, "budget-exhaustion completeness"
        )
        if (
            status != expected_status
            or outcome != "not_evaluated"
            or certificate is not None
            or uncertainty is not None
            or closed_completeness["complete"] is not False
        ):
            raise ContractError("budget-exhaustion output/status mismatch")
        return

    if status == "capability_unavailable":
        capability = _closed_mapping(
            result, {"available", "capability"}, "capability result"
        )
        if (
            adapter not in {"sympy", "lean"}
            or capability["available"] is not False
            or capability["capability"] != adapter
            or outcome != "not_evaluated"
            or certificate is not None
            or uncertainty is not None
            or completeness is not None
        ):
            raise ContractError("capability-unavailable output/adapter mismatch")
        return

    if adapter == "finite_model" and status == "resource_exhausted":
        finite = _closed_mapping(
            result, {"claim_holds", "explored", "state_count"},
            "incomplete finite-model result",
        )
        finite_completeness = _closed_mapping(
            completeness, {"complete", "explored", "state_count", "max_states"},
            "incomplete finite-model completeness",
        )
        finite_uncertainty = _closed_mapping(
            uncertainty, {"kind"}, "incomplete finite-model uncertainty"
        )
        if (
            finite_uncertainty["kind"] != "none_deterministic_but_incomplete"
            or finite["claim_holds"] is not None
            or outcome != "inconclusive"
            or certificate is not None
            or finite_completeness["complete"] is not False
            or finite["explored"] != finite_completeness["explored"]
            or finite["state_count"] != finite_completeness["state_count"]
        ):
            raise ContractError("incomplete finite-model output is internally inconsistent")
        return

    if adapter == "sympy" and status == "solver_failure":
        failed = _closed_mapping(result, {"available", "error"}, "SymPy failure")
        if (
            failed["available"] is not True
            or outcome != "not_evaluated"
            or certificate is not None
            or uncertainty is not None
            or completeness is not None
        ):
            raise ContractError("SymPy failure output is internally inconsistent")
        return

    if adapter == "lean" and status in {"deadline_exhausted", "solver_failure"}:
        lean = _closed_mapping(
            result, {"available", "proposition", "process"}, "Lean process result"
        )
        _validate_process_event(
            lean["process"], "Lean process result.process", accepted=False
        )
        lean_completeness = _closed_mapping(
            completeness, {"complete", "scope"}, "Lean completeness"
        )
        if (
            lean["available"] is not True
            or outcome != "not_evaluated"
            or certificate is not None
            or uncertainty is not None
            or lean_completeness["complete"] is not False
        ):
            raise ContractError("Lean operational output is internally inconsistent")
        return

    if status not in {"succeeded", "counterexample"}:
        raise ContractError(f"adapter {adapter!r} cannot emit status {status!r}")
    expected_outcome = "supports_within_scope" if status == "succeeded" else "falsifies_claim"
    if outcome != expected_outcome:
        raise ContractError("decisive adapter status/outcome mismatch")

    model = spec.get("model", {})
    if adapter == "exact" and model.get("operation", "equality") == "equality":
        exact = _closed_mapping(result, {"claim_holds", "exact_values"}, "exact result")
        _closed_mapping(exact["exact_values"], {"left", "right", "difference"}, "exact values")
        exact_certificate = _closed_mapping(
            certificate,
            {"kind", "expression", "left", "right", "difference", "verification"},
            "exact certificate",
        )
        if exact_certificate["kind"] != "normalized_rational_equality":
            raise ContractError("exact certificate kind is unregistered")
        exact_uncertainty = _closed_mapping(
            uncertainty, {"kind", "roundoff"}, "exact uncertainty"
        )
        exact_completeness = _closed_mapping(
            completeness, {"complete", "scope"}, "exact completeness"
        )
        if (
            exact_uncertainty != {"kind": "none_exact_arithmetic", "roundoff": 0}
            or exact_completeness
            != {"complete": True, "scope": "declared rational expression"}
        ):
            raise ContractError("exact output discriminants are invalid")
    elif adapter == "exact" and model.get("operation") == "integer_predicate":
        _closed_mapping(result, {"claim_holds", "assignment"}, "integer result")
        integer_certificate = _closed_mapping(
            certificate, {"kind", "predicate", "assignment", "value"},
            "integer certificate",
        )
        if integer_certificate["kind"] != "exact_integer_predicate":
            raise ContractError("integer certificate kind is unregistered")
        integer_uncertainty = _closed_mapping(
            uncertainty, {"kind", "roundoff"}, "integer uncertainty"
        )
        integer_completeness = _closed_mapping(
            completeness, {"complete", "scope"}, "integer completeness"
        )
        if (
            integer_uncertainty != {"kind": "none_exact_arithmetic", "roundoff": 0}
            or integer_completeness
            != {"complete": True, "scope": "declared assignment"}
        ):
            raise ContractError("integer output discriminants are invalid")
    elif adapter == "sympy":
        _closed_mapping(result, {"claim_holds", "normal_form", "sympy_version"}, "SymPy result")
        sympy_certificate = _closed_mapping(
            certificate, {"kind", "left", "right", "normal_form", "sympy_version"},
            "SymPy certificate",
        )
        if sympy_certificate["kind"] != "sympy_exact_normal_form":
            raise ContractError("SymPy certificate kind is unregistered")
        sympy_uncertainty = _closed_mapping(uncertainty, {"kind"}, "SymPy uncertainty")
        sympy_completeness = _closed_mapping(
            completeness, {"complete", "scope"}, "SymPy completeness"
        )
        if (
            sympy_uncertainty["kind"] != "symbolic_exact_no_numeric_roundoff"
            or sympy_completeness["complete"] is not True
        ):
            raise ContractError("SymPy output discriminants are invalid")
    elif adapter == "finite_model":
        _closed_mapping(result, {"claim_holds", "witness", "counterexample"}, "finite-model result")
        finite_certificate = _closed_mapping(
            certificate,
            {
                "kind", "quantifier", "predicate", "domains", "witness",
                "counterexample", "explored", "state_count", "decisive_early_witness",
            },
            "finite-model certificate",
        )
        if finite_certificate["kind"] != "finite_model_exhaustion":
            raise ContractError("finite-model certificate kind is unregistered")
        finite_uncertainty = _closed_mapping(
            uncertainty, {"kind"}, "finite-model uncertainty"
        )
        _closed_mapping(
            completeness, {"complete", "explored", "state_count", "scope"},
            "finite-model completeness",
        )
        if finite_uncertainty["kind"] != "none_finite_deterministic":
            raise ContractError("finite-model uncertainty kind is unregistered")
    elif adapter in {"numeric", "sweep"} and spec.get("seed_policy", {}).get("stochastic"):
        _closed_mapping(
            result, {"claim_holds", "estimate", "sample_count", "sample_digest_material"},
            "stochastic result",
        )
        stochastic_certificate = _closed_mapping(
            certificate, {"kind", "seed_policy", "sample_count", "decision_rule"},
            "stochastic certificate",
        )
        if stochastic_certificate["kind"] != "seeded_stochastic_replay":
            raise ContractError("stochastic certificate kind is unregistered")
        if not isinstance(uncertainty, Mapping) or frozenset(uncertainty) not in {
            frozenset({"method", "estimate", "standard_error", "lower", "upper"}),
            frozenset({"method", "estimate", "lower", "upper"}),
        }:
            raise ContractError("stochastic uncertainty is not schema-closed")
        stochastic_completeness = _closed_mapping(
            completeness, {"complete", "scope", "stopping_rule"},
            "stochastic completeness",
        )
        if (
            uncertainty["method"] != spec["preregistration"].get("uncertainty_method")
            or stochastic_certificate["seed_policy"] != spec["seed_policy"]
            or stochastic_certificate["sample_count"]
            != spec["preregistration"].get("sample_size")
            or stochastic_completeness["stopping_rule"]
            != spec["preregistration"].get("stopping_rule")
        ):
            raise ContractError("stochastic output discriminants differ from preregistration")
    elif adapter in {"numeric", "sweep"}:
        numeric = _closed_mapping(
            result, {"claim_holds", "samples", "minimum", "maximum"}, "numeric result"
        )
        if not isinstance(numeric["samples"], list):
            raise ContractError("numeric samples must be an array")
        for index, sample in enumerate(numeric["samples"]):
            _closed_mapping(sample, {"parameters", "value"}, f"numeric sample {index}")
        numeric_certificate = _closed_mapping(
            certificate, {"kind", "expression", "decision_rule", "points"},
            "numeric certificate",
        )
        if numeric_certificate["kind"] != "deterministic_numeric_replay":
            raise ContractError("numeric certificate kind is unregistered")
        numeric_uncertainty = _closed_mapping(
            uncertainty,
            {
                "kind", "absolute_tolerance", "relative_tolerance",
                "does_not_establish_exact_equality",
            },
            "numeric uncertainty",
        )
        numeric_completeness = _closed_mapping(
            completeness, {"complete", "scope", "points"}, "numeric completeness"
        )
        if (
            numeric_uncertainty["kind"] != "floating_point"
            or numeric_uncertainty["does_not_establish_exact_equality"] is not True
            or numeric_certificate["expression"] != model.get("expression")
            or numeric_certificate["points"] != len(numeric["samples"])
            or numeric_completeness["points"] != len(numeric["samples"])
        ):
            raise ContractError("numeric output discriminants are invalid")
    elif adapter == "lean":
        lean = _closed_mapping(result, {"available", "proposition", "process"}, "Lean result")
        _validate_process_event(lean["process"], "Lean result.process", accepted=True)
        lean_certificate = _closed_mapping(
            certificate, {"kind", "source", "proposition", "executable"},
            "Lean certificate",
        )
        if lean_certificate["kind"] != "lean_kernel_checked":
            raise ContractError("Lean certificate kind is unregistered")
        lean_uncertainty = _closed_mapping(uncertainty, {"kind"}, "Lean uncertainty")
        lean_completeness = _closed_mapping(
            completeness, {"complete", "scope"}, "Lean completeness"
        )
        if (
            lean_uncertainty["kind"] != "none_kernel_check"
            or lean_completeness["complete"] is not True
            or lean_certificate["proposition"] != model.get("proposition")
        ):
            raise ContractError("Lean output discriminants are invalid")
    else:
        raise ContractError(f"unregistered adapter output contract: {adapter!r}")

    if (
        isinstance(result, Mapping)
        and "claim_holds" in result
        and result["claim_holds"] is not (status == "succeeded")
    ):
        raise ContractError("claim_holds differs from decisive status")
    if not isinstance(completeness, Mapping) or completeness.get("complete") is not True:
        raise ContractError("decisive adapter output must be complete")


def _result_variant(output: Mapping[str, Any], spec: Mapping[str, Any]) -> str:
    """Discriminate the closed adapter/status/result union with one stable tag."""

    status = str(output.get("status") or "")
    adapter = str(spec.get("adapter") or "")
    outcome = str(output.get("epistemic_outcome") or "")
    operational = {
        "capability_unavailable": "operational_capability_unavailable",
        "deadline_exhausted": "operational_deadline_exhausted",
        "resource_exhausted": "operational_resource_exhausted",
        "solver_failure": "operational_solver_failure",
        "invalid_spec": "operational_invalid_spec",
        "operational_failure": "operational_failure",
    }
    if adapter == "finite_model" and status == "resource_exhausted" and outcome == "inconclusive":
        variant = "finite_model_inconclusive"
    elif status in operational:
        variant = operational[status]
    else:
        suffix = "support" if status == "succeeded" else "counterexample"
        if adapter == "exact":
            operation = spec.get("model", {}).get("operation", "equality")
            prefix = "exact_integer" if operation == "integer_predicate" else "exact_rational"
        elif adapter in {"numeric", "sweep"}:
            mode = "stochastic" if spec.get("seed_policy", {}).get("stochastic") else "deterministic"
            prefix = f"{adapter}_{mode}"
        else:
            prefix = adapter
        variant = f"{prefix}_{suffix}"
    if variant not in _OUTPUT_VARIANTS:
        raise ExperimentOutputError(
            "unregistered_output_variant",
            f"adapter/status pair {adapter!r}/{status!r} has no closed v3 output variant",
        )
    return variant


def _theory_effect_contract(
    triage: Mapping[str, Any], request: Mapping[str, Any]
) -> dict[str, Any]:
    """Freeze what a probe may change before execution.

    Missing caller detail defaults to the weakest toy/proxy interpretation; a
    free-text transfer boundary can never promote a result into theory support.
    """

    supplied = request.get("theory_effect_contract")
    if supplied is None:
        return {
            "tested_claim_id": str(triage["theoretical_question_id"]),
            "tested_claim_kind": "model_consequence",
            "target_relation": "toy_or_proxy",
            "if_supported": "record_scoped_consistency_only",
            "if_falsified": "record_scoped_counterexample_only",
            "theory_identity_locked": True,
            "automatic_theory_selection": False,
            "automatic_proof": False,
        }
    if not isinstance(supplied, Mapping):
        raise ContractError("theory effect contract must be an object")
    return dict(supplied)


def derive_theory_effect(
    spec: Mapping[str, Any], *, status: str, epistemic_outcome: str
) -> dict[str, Any]:
    """Map a scoped result to a non-promotional theory effect."""

    contract = spec["theory_effect_contract"]
    operational = status not in {"succeeded", "counterexample"}
    premise_revision = "not_authorized"
    if epistemic_outcome == "inconclusive":
        kind = "no_theory_effect_inconclusive"
    elif operational or epistemic_outcome == "not_evaluated":
        kind = "no_theory_effect_operational"
    elif epistemic_outcome == "maps_boundary":
        kind = "scoped_boundary_map_only"
    elif epistemic_outcome == "supports_within_scope":
        kind = (
            "no_theory_effect_preregistered"
            if contract["if_supported"] == "no_change"
            else "bounded_consistency_signal_only"
        )
    elif (
        epistemic_outcome == "falsifies_claim"
        and contract["if_falsified"] == "no_change"
    ):
        kind = "no_theory_effect_preregistered"
    elif (
        epistemic_outcome == "falsifies_claim"
        and contract["tested_claim_kind"] == "theory_premise"
        and contract["if_falsified"] == "request_registered_premise_revision"
    ):
        kind = "registered_premise_revision_requested"
        premise_revision = "requires_reflective_review"
    elif epistemic_outcome == "falsifies_claim":
        kind = "scoped_counterexample_only"
    else:  # pragma: no cover - receipt schema closes the outcome enum.
        raise ContractError("unsupported experiment epistemic outcome")
    return {
        "effect_kind": kind,
        "tested_claim_id": contract["tested_claim_id"],
        "tested_claim_kind": contract["tested_claim_kind"],
        "target_relation": contract["target_relation"],
        "contract_digest": canonical_digest(contract),
        "automatic_hypothesis_relation": "none",
        "premise_revision_status": premise_revision,
        "theory_identity_changed": False,
        "theory_selected": False,
        "proof_authorized": False,
        "physical_target_support_authorized": False,
        "experiment_subordinate_to_theory": True,
    }


def _recommendation_for_outcome(epistemic_outcome: str) -> str:
    """Return the one closed reflective recommendation for an outcome."""

    try:
        return {
            "supports_within_scope": "Reflect on whether the bounded support sharpens the named mechanism without treating it as theorem proof.",
            "falsifies_claim": "Revisit the originating premise and conceptual mechanism using the verified scoped counterexample.",
            "maps_boundary": "Assimilate the mapped validity boundary and revise the theory's domain claims.",
            "inconclusive": "Preserve the theory and record the operational or finite-scope limit; do not infer falsification.",
            "not_evaluated": "Record the operational outcome only; the theory remains epistemically unchanged.",
        }[epistemic_outcome]
    except KeyError as exc:  # pragma: no cover - schemas close the public enum.
        raise ContractError("unsupported experiment epistemic outcome") from exc


def _reflective_assimilation(
    conceptual_system_ids: list[str], epistemic_outcome: str
) -> list[dict[str, str]]:
    """Build exactly one non-promotional recommendation per conceptual system."""

    recommendation = _recommendation_for_outcome(epistemic_outcome)
    return [
        {
            "conceptual_system_id": conceptual_id,
            "recommendation": recommendation,
            "authority_boundary": "reflective_assimilation_required_runtime_does_not_select_theory_or_prove_theorem",
        }
        for conceptual_id in conceptual_system_ids
    ]


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def triage_probe(request: Mapping[str, Any]) -> dict[str, Any]:
    """Decide whether a mature theory question warrants a support probe."""

    source = dict(request)
    input_digest = canonical_digest(source, exclude_keys=("input_digest", "triage_id", "created_at"))
    target_id = str(source.get("target_id", ""))
    theory_id = source.get("theory_programme_id")
    programme_digest = source.get("source_theory_programme_digest")
    reflection_digest = source.get("source_reflection_packet_digest")
    question_id = source.get("theoretical_question_id")
    conceptual_ids = sorted(set(str(value) for value in source.get("conceptual_system_ids", []) if _nonempty(value)))
    registered_claims = _normalize_theory_claim_registry(source)
    maturity = source.get("programme_maturity", "unformed")
    question = str(source.get("question", ""))
    expected_change = str(source.get("expected_conceptual_change", ""))
    justification = str(source.get("theory_generated_justification", ""))
    decision_effect = source.get("decision_effect", {})
    methods = sorted(set(source.get("candidate_methods", [])))
    reasons: list[str] = []

    if source.get("probe_needed") is False:
        decision = "no_probe_needed"
        reasons.append("the theory programme explicitly has no decision that requires computational support")
    else:
        mature = maturity in {"mature", "formalization_ready"}
        exact_question = _nonempty(question) and _nonempty(question_id)
        effectful = (
            isinstance(decision_effect, Mapping)
            and _nonempty(decision_effect.get("if_supported"))
            and _nonempty(decision_effect.get("if_not_supported"))
            and decision_effect.get("if_supported") != decision_effect.get("if_not_supported")
            and _nonempty(expected_change)
        )
        theory_bound = (
            _nonempty(theory_id)
            and bool(conceptual_ids)
            and _nonempty(justification)
            and isinstance(programme_digest, str)
            and _DIGEST.fullmatch(programme_digest) is not None
            and isinstance(reflection_digest, str)
            and _DIGEST.fullmatch(reflection_digest) is not None
        )
        matching_claims = [
            row
            for row in registered_claims
            if row["claim_id"] == question_id
            and row["statement"] == question.strip()
            and row["theory_programme_id"] == theory_id
            and row["conceptual_system_ids"] == conceptual_ids
            and row["source_theory_programme_digest"] == programme_digest
            and row["source_reflection_packet_digest"] == reflection_digest
        ]
        theory_bound = theory_bound and len(matching_claims) == 1
        if mature and exact_question and effectful and theory_bound and methods:
            decision = "commission"
            reasons.append("a mature theory generated a discriminating support question with two consequential outcomes")
        elif not mature or not exact_question or not theory_bound:
            decision = "immature_question"
            reasons.append("the theory programme, conceptual binding, or exact support question is not mature")
        else:
            decision = "no_probe_needed"
            reasons.append("the proposed computation has no preregistered conceptual decision consequence")

    triage = {
        "schema_version": 1,
        "triage_id": stable_identifier("triage", target_id, theory_id, question_id, input_digest),
        "target_id": target_id,
        "theory_programme_id": theory_id if _nonempty(theory_id) else None,
        "source_theory_programme_digest": (
            programme_digest
            if isinstance(programme_digest, str) and _DIGEST.fullmatch(programme_digest)
            else None
        ),
        "source_reflection_packet_digest": (
            reflection_digest
            if isinstance(reflection_digest, str) and _DIGEST.fullmatch(reflection_digest)
            else None
        ),
        "conceptual_system_ids": conceptual_ids,
        "registered_theory_claims": registered_claims,
        "theoretical_question_id": question_id if _nonempty(question_id) else None,
        "question": question,
        "programme_maturity": maturity,
        "probe_role": source.get("probe_role", "none"),
        "decision": decision,
        "decision_effect": {
            "if_supported": str(decision_effect.get("if_supported", "")),
            "if_not_supported": str(decision_effect.get("if_not_supported", "")),
        },
        "expected_conceptual_change": expected_change,
        "theory_generated_justification": justification,
        "candidate_methods": methods,
        "state_version": int(source.get("state_version", 0)),
        "input_digest": input_digest,
        "reasons": reasons,
        "created_at": utc_now(),
    }
    validate_payload(triage, TRIAGE_SCHEMA)
    return triage


def current_code_digest() -> str:
    """Return the transitive repository/runtime dependency authority digest."""

    return build_experiment_dependency_authority()["content_digest"]


def _validate_v3_spec_shape(
    spec: Mapping[str, Any], *, validate_current_authority: bool = True
) -> dict[str, Any]:
    """Validate the closed v3 spec, precommit DAG, and observed authority."""

    supplied = dict(spec)
    _schema_version(supplied, artifact="experiment specification")
    if set(supplied) != set(_V3_SPEC_FIELDS):
        raise ExperimentSpecError(
            "spec_not_schema_closed",
            f"v3 spec fields differ: expected {sorted(_V3_SPEC_FIELDS)!r}, got {sorted(supplied)!r}",
        )
    if supplied.get("contract_version") != RUNTIME_CONTRACT_VERSION:
        if supplied.get("contract_version") == "dynamic-experiment-runtime/3.0.0":
            raise ExperimentMigrationRequired(
                "historical_v3_0_reexecution_required",
                "dynamic experiment v3.0 lacks current governed-process authority; "
                "recompile and reexecute under v3.1",
            )
        raise ExperimentSpecError(
            "spec_contract_version_mismatch", "v3 runtime contract version is invalid"
        )
    try:
        validate_payload(supplied, SPEC_SCHEMA)
    except ContractError as exc:
        raise ExperimentSpecError(
            "spec_common_contract_invalid", str(exc)
        ) from exc
    if supplied.get("spec_digest") != _top_level_digest(supplied, "spec_digest"):
        raise ExperimentSpecError(
            "spec_self_digest_mismatch",
            "spec_digest must bind every nested value and omit only the root spec_digest",
        )
    authority = supplied.get("execution_authority")
    if not isinstance(authority, Mapping):
        raise ExperimentSpecError(
            "execution_authority_missing", "v3 spec lacks execution authority"
        )
    if supplied.get("authority_digest") != authority.get("content_digest"):
        raise ExperimentSpecError(
            "authority_digest_mismatch", "spec authority digest differs from its record"
        )
    dependency = authority.get("dependency_authority")
    environment = authority.get("observed_environment")
    if not isinstance(dependency, Mapping) or not isinstance(environment, Mapping):
        raise ExperimentSpecError(
            "authority_components_missing",
            "execution authority lacks dependency or observed-environment authority",
        )
    if supplied.get("code_digest") != dependency.get("content_digest"):
        raise ExperimentSpecError(
            "dependency_digest_mismatch", "spec code digest is not the transitive closure digest"
        )
    if supplied.get("observed_environment") != environment:
        raise ExperimentSpecError(
            "observed_environment_mismatch",
            "spec environment is not the one inside execution authority",
        )
    if supplied.get("environment_digest") != environment.get("content_digest"):
        raise ExperimentSpecError(
            "environment_digest_mismatch",
            "spec environment digest differs from observed environment",
        )
    expected_spec_id = stable_identifier(
        "experiment-spec-v3", canonical_digest(_spec_precommit_core(supplied))
    )
    if supplied.get("spec_id") != expected_spec_id:
        raise ExperimentSpecError(
            "spec_id_mismatch", "precommitted spec identity is invalid"
        )
    expected_execution_id = stable_identifier(
        "experiment-execution-v3",
        expected_spec_id,
        supplied["authority_digest"],
        supplied["branch_id"],
        supplied["run_id"],
    )
    if supplied.get("execution_id") != expected_execution_id:
        raise ExperimentSpecError(
            "execution_id_mismatch", "precommitted execution identity is invalid"
        )
    expected_receipt_id = stable_identifier(
        "experiment-receipt-v3",
        expected_spec_id,
        expected_execution_id,
        supplied["experiment_id"],
    )
    if supplied.get("precommitted_receipt_id") != expected_receipt_id:
        raise ExperimentSpecError(
            "receipt_id_precommit_mismatch",
            "precommitted receipt identity is invalid",
        )
    if validate_current_authority:
        validate_experiment_authority(
            authority,
            adapter=str(supplied["adapter"]),
            model=supplied["model"],
        )
    return supplied


def validate_experiment_spec(spec: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one current v3 spec against live transitive authority."""

    return _validate_v3_spec_shape(spec)


def _typed_spec_operation(function):
    def wrapped(*args: Any, **kwargs: Any) -> dict[str, Any]:
        try:
            return function(*args, **kwargs)
        except ExperimentRuntimeError:
            raise
        except (ContractError, KeyError, TypeError, ValueError) as exc:
            raise ExperimentSpecError(
                "spec_compilation_failed", str(exc)
            ) from exc

    return wrapped


@_typed_spec_operation
def compile_experiment_spec(triage: Mapping[str, Any], request: Mapping[str, Any]) -> dict[str, Any]:
    """Compile a commission into a v3 spec with all outer IDs precommitted."""

    validate_payload(dict(triage), TRIAGE_SCHEMA)
    if triage.get("decision") != "commission":
        raise ExperimentSpecError(
            "triage_not_commissioned",
            "only a commissioned triage decision can compile an experiment",
        )
    forbidden = {
        "environment", "observed_environment", "execution_authority",
        "authority_digest", "code_digest", "code_version", "certificate",
        "spec_id", "execution_id", "receipt_id", "precommitted_receipt_id",
    }
    supplied_forbidden = sorted(forbidden.intersection(request))
    if supplied_forbidden:
        reason = (
            "caller_environment_forbidden"
            if "environment" in supplied_forbidden or "observed_environment" in supplied_forbidden
            else "caller_authority_material_forbidden"
        )
        raise ExperimentSpecError(
            reason,
            f"runtime-observed/precommitted fields cannot be caller supplied: {supplied_forbidden!r}",
        )
    adapter = request.get("adapter")
    if adapter not in triage.get("candidate_methods", []):
        raise ExperimentSpecError(
            "adapter_not_admitted", "selected adapter was not admitted by triage"
        )
    stochastic = bool(request.get("seed_policy", {}).get("stochastic"))
    preregistration = request.get("preregistration", {})
    if stochastic:
        missing = [name for name in ("estimand", "sample_size", "stopping_rule", "uncertainty_method") if not preregistration.get(name)]
        if missing:
            raise ExperimentSpecError(
                "stochastic_preregistration_incomplete",
                f"stochastic preregistration missing: {', '.join(missing)}",
            )
    model = dict(request.get("model", {}))
    authority = build_experiment_authority(adapter=str(adapter), model=model)
    environment = authority["observed_environment"]
    theory_effect_contract = _theory_effect_contract(triage, request)
    matching_claims = [
        row
        for row in triage["registered_theory_claims"]
        if row["claim_id"] == theory_effect_contract.get("tested_claim_id")
        and row["claim_kind"] == theory_effect_contract.get("tested_claim_kind")
        and row["target_relation"] == theory_effect_contract.get("target_relation")
    ]
    if len(matching_claims) != 1:
        raise ExperimentSpecError(
            "tested_claim_not_registered",
            "theory effect contract does not name one sealed registered theory claim",
        )
    if (
        theory_effect_contract.get("if_falsified") == "request_registered_premise_revision"
        and theory_effect_contract.get("tested_claim_kind") != "theory_premise"
    ):
        raise ExperimentSpecError(
            "premise_revision_scope_invalid",
            "premise revision may be requested only for a registered theory premise",
        )
    spec = {
        "schema_version": 3,
        "contract_version": RUNTIME_CONTRACT_VERSION,
        "experiment_id": str(request.get("experiment_id") or stable_identifier("experiment", triage["triage_id"], adapter, request.get("model"))),
        "branch_id": validate_job_id(str(request.get("branch_id"))),
        "target_id": triage["target_id"],
        "run_id": validate_job_id(str(request.get("run_id"))),
        "state_version": triage["state_version"],
        "theory_programme_id": triage["theory_programme_id"],
        "source_theory_programme_digest": triage[
            "source_theory_programme_digest"
        ],
        "source_reflection_packet_digest": triage[
            "source_reflection_packet_digest"
        ],
        "conceptual_system_ids": list(triage["conceptual_system_ids"]),
        "theoretical_question_id": triage["theoretical_question_id"],
        "tested_theory_claim": dict(matching_claims[0]),
        "probe_role": triage["probe_role"],
        "expected_conceptual_change": triage["expected_conceptual_change"],
        "triage_digest": _top_level_digest(triage, "created_at"),
        "adapter": adapter,
        "model": model,
        "preregistration": dict(preregistration),
        "controls": list(request.get("controls", [])),
        "seed_policy": dict(request.get("seed_policy", {"stochastic": False, "policy": "not_applicable"})),
        "resource_budget": dict(request.get("resource_budget", {})),
        "transfer_boundary": str(request.get("transfer_boundary", "")),
        "theory_effect_contract": theory_effect_contract,
        "code_version": ADAPTER_VERSION,
        "execution_authority": authority,
        "authority_digest": authority["content_digest"],
        "code_digest": authority["dependency_authority"]["content_digest"],
        "observed_environment": environment,
        "environment_digest": environment["content_digest"],
        "created_at": str(request.get("created_at") or utc_now()),
    }
    spec["spec_id"] = stable_identifier(
        "experiment-spec-v3", canonical_digest(_spec_precommit_core(spec))
    )
    spec["execution_id"] = stable_identifier(
        "experiment-execution-v3",
        spec["spec_id"],
        spec["authority_digest"],
        spec["branch_id"],
        spec["run_id"],
    )
    spec["precommitted_receipt_id"] = stable_identifier(
        "experiment-receipt-v3",
        spec["spec_id"],
        spec["execution_id"],
        spec["experiment_id"],
    )
    spec["spec_digest"] = _top_level_digest(spec, "spec_digest")
    _validate_v3_spec_shape(spec, validate_current_authority=False)
    return spec


@_typed_spec_operation
def validate_commissioned_experiment_spec(
    triage_request: Mapping[str, Any],
    experiment_request: Mapping[str, Any],
    spec: Mapping[str, Any],
) -> dict[str, Any]:
    """Rederive a v3 preseal from exact commission and observed authority."""

    triage = triage_probe(triage_request)
    if triage["decision"] != "commission":
        raise ExperimentSpecError(
            "commission_replay_rejected",
            "presealed experiment spec lacks a valid theory commission",
        )
    supplied = _validate_v3_spec_shape(spec)
    replay_request = dict(experiment_request)
    replay_request["created_at"] = supplied["created_at"]
    expected = compile_experiment_spec(triage, replay_request)
    if supplied != expected:
        raise ExperimentSpecError(
            "commission_envelope_mismatch",
            "presealed experiment spec differs from its sealed commission envelope"
        )
    return supplied


def experiment_directory(run_directory: Path | str, spec: Mapping[str, Any]) -> Path:
    root = Path(run_directory).resolve()
    branch = validate_job_id(str(spec["branch_id"]))
    experiment = validate_job_id(str(spec["experiment_id"]))
    return contained_path(root, "branches", branch, "experiments", experiment)


def _write_immutable_json(path: Path, payload: Mapping[str, Any]) -> None:
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        existing = json.loads(path.read_text(encoding="utf-8"))
        if canonical_digest(existing) != canonical_digest(payload):
            raise ContractError(f"immutable experiment artifact conflict: {path}")


def _validate_v3_receipt_shape(receipt: Mapping[str, Any]) -> dict[str, Any]:
    supplied = dict(receipt)
    version = supplied.get("schema_version")
    if version == 2:
        raise ExperimentMigrationRequired(
            "historical_v2_reexecution_required",
            "historical v2 receipt is non-authoritative until explicit v3 reexecution",
        )
    if version != 3:
        raise ExperimentReceiptError(
            "unsupported_schema_version", "receipt schema_version is not v3"
        )
    if set(supplied) != set(_V3_RECEIPT_FIELDS):
        raise ExperimentReceiptError(
            "receipt_not_schema_closed",
            f"v3 receipt fields differ: expected {sorted(_V3_RECEIPT_FIELDS)!r}, got {sorted(supplied)!r}",
        )
    if supplied.get("contract_version") != RUNTIME_CONTRACT_VERSION:
        if supplied.get("contract_version") == "dynamic-experiment-runtime/3.0.0":
            raise ExperimentMigrationRequired(
                "historical_v3_0_reexecution_required",
                "dynamic experiment v3.0 receipt is historical and must be reexecuted "
                "under the current v3.1 contract",
            )
        raise ExperimentReceiptError(
            "receipt_contract_version_mismatch",
            "v3 receipt runtime contract version is invalid",
        )
    if supplied.get("result_variant") not in _OUTPUT_VARIANTS:
        raise ExperimentReceiptError(
            "unregistered_output_variant", "receipt result_variant is not registered"
        )
    if _DIGEST.fullmatch(str(supplied.get("authority_digest") or "")) is None:
        raise ExperimentReceiptError(
            "authority_digest_invalid", "receipt authority digest is invalid"
        )
    try:
        validate_payload(supplied, RECEIPT_SCHEMA)
    except SchemaValidationError as exc:
        # Preserve the public distinction between a malformed receipt envelope
        # and a malformed adapter output.  The closed v3 schema is deliberately
        # the first check, but certificate/result union failures still belong
        # to the adapter-output contract and must retain that typed error.
        if exc.locations == ("$.certificate",):
            raise ExperimentOutputError(
                EXPERIMENT_OUTPUT_CONTRACT_INVALID, str(exc)
            ) from exc
        raise ExperimentReceiptError(
            EXPERIMENT_RECEIPT_SCHEMA_INVALID, str(exc)
        ) from exc
    except ContractError as exc:
        raise ExperimentReceiptError(
            EXPERIMENT_RECEIPT_SCHEMA_INVALID, str(exc)
        ) from exc
    return supplied


def _typed_receipt_validator(function):
    def wrapped(*args: Any, **kwargs: Any) -> None:
        try:
            function(*args, **kwargs)
        except ExperimentRuntimeError:
            raise
        except (ContractError, KeyError, TypeError, ValueError) as exc:
            raise ExperimentReceiptError(
                "receipt_semantic_validation_failed", str(exc)
            ) from exc

    return wrapped


@_typed_receipt_validator
def validate_experiment_receipt(
    receipt: Mapping[str, Any],
    spec: Mapping[str, Any],
    *,
    work_directory: Path | None = None,
) -> None:
    """Independently validate receipt identity and adapter certificate semantics."""

    spec = _validate_v3_spec_shape(spec)
    receipt = _validate_v3_receipt_shape(receipt)
    try:
        _validate_adapter_output_contract(receipt, spec)
    except ContractError as exc:
        raise ExperimentOutputError(
            EXPERIMENT_OUTPUT_CONTRACT_INVALID, str(exc)
        ) from exc
    if receipt["spec_digest"] != spec["spec_digest"]:
        raise ContractError("experiment receipt is stale for this specification")
    for field in (
        "spec_id",
        "execution_id",
        "experiment_id",
        "branch_id",
        "target_id",
        "run_id",
        "state_version",
        "theory_programme_id",
        "source_theory_programme_digest",
        "source_reflection_packet_digest",
        "theoretical_question_id",
        "adapter",
    ):
        if receipt[field] != spec[field]:
            raise ContractError(f"receipt/spec mismatch for {field}")
    if receipt["conceptual_system_ids"] != spec["conceptual_system_ids"]:
        raise ContractError("receipt/spec conceptual system mismatch")
    expected_claim_digest = canonical_digest(
        spec["tested_theory_claim"], exclude_keys=("claim_digest",)
    )
    if spec["tested_theory_claim"]["claim_digest"] != expected_claim_digest:
        raise ContractError("experiment tested theory claim digest mismatch")
    if receipt["authority_digest"] != spec["authority_digest"]:
        raise ContractError("experiment receipt execution authority digest mismatch")
    if receipt["code_digest"] != spec["code_digest"]:
        raise ContractError("experiment receipt transitive code digest mismatch")
    if receipt["environment_digest"] != spec["environment_digest"]:
        raise ContractError("experiment receipt environment digest mismatch")
    expected_variant = _result_variant(receipt, spec)
    if receipt["result_variant"] != expected_variant:
        raise ContractError("experiment receipt output variant mismatch")
    if receipt["transfer_boundary"] != spec["transfer_boundary"]:
        raise ContractError("experiment receipt transfer boundary mismatch")
    validator = receipt["validator"]
    if (
        validator["validator_id"] != VALIDATOR_ID
        or validator["version"] != VALIDATOR_VERSION
        or validator["status"] != "valid"
    ):
        raise ContractError("experiment receipt validator authority mismatch")
    try:
        started_at = dt.datetime.fromisoformat(
            str(receipt["started_at"]).replace("Z", "+00:00")
        )
        completed_at = dt.datetime.fromisoformat(
            str(receipt["completed_at"]).replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ContractError("experiment receipt timestamps are invalid") from exc
    if (
        started_at.tzinfo is None
        or completed_at.tzinfo is None
        or completed_at < started_at
    ):
        raise ContractError("experiment receipt completion precedes its start")
    expected_resource_digest = _resource_provenance_digest(receipt)
    if receipt["resource_authority_boundary"] != RESOURCE_AUTHORITY_BOUNDARY:
        raise ContractError("experiment resource authority boundary mismatch")
    if receipt["resource_provenance_digest"] != expected_resource_digest:
        raise ContractError("experiment resource provenance digest mismatch")
    resource_usage = _closed_mapping(
        receipt["resource_usage"],
        {"budget", "usage", "status", "events", "deadline", "resource_measurement"},
        "experiment resource usage",
    )
    expected_budget = ResourceGovernor.from_mapping(spec["resource_budget"]).receipt(
        "succeeded"
    )["budget"]
    if resource_usage.get("budget") != expected_budget:
        raise ContractError("experiment resource usage differs from its declared budget")
    usage = _closed_mapping(
        resource_usage["usage"], _MEASUREMENT_DIMENSIONS, "experiment resource usage.usage"
    )
    if any(
        isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0
        for value in usage.values()
    ):
        raise ContractError("experiment resource usage contains an invalid measurement")
    if not isinstance(resource_usage["events"], list):
        raise ContractError("experiment resource events must be an array")
    _validate_measurement_boundaries(
        resource_usage["resource_measurement"],
        "experiment resource usage.resource_measurement",
    )
    _validate_process_bindings(spec, receipt, resource_usage, work_directory)
    expected_resource_status = (
        "succeeded"
        if receipt["status"] in {"succeeded", "counterexample"}
        else "worker_failed"
    )
    if resource_usage.get("status") != expected_resource_status:
        raise ContractError("experiment resource status differs from its outcome")
    contract = spec["theory_effect_contract"]
    claim = spec["tested_theory_claim"]
    if (
        claim["claim_id"] != contract["tested_claim_id"]
        or claim["claim_kind"] != contract["tested_claim_kind"]
        or claim["target_relation"] != contract["target_relation"]
    ):
        raise ContractError("experiment specification crossed its sealed tested theory claim")
    expected_theory_effect = derive_theory_effect(
        spec,
        status=receipt["status"],
        epistemic_outcome=receipt["epistemic_outcome"],
    )
    if receipt["theory_effect_contract_digest"] != canonical_digest(
        spec["theory_effect_contract"]
    ):
        raise ContractError("receipt theory-effect contract digest mismatch")
    if receipt["theory_effect"] != expected_theory_effect:
        raise ContractError("receipt theory effect exceeds the preregistered scope")
    expected_failure = _typed_operational_failure(receipt)
    if "failure" not in receipt or receipt["failure"] != expected_failure:
        raise ContractError("experiment receipt failure semantics mismatch")
    if receipt["status"] == "counterexample" and receipt["certificate"] is None:
        raise ContractError("counterexample outcome requires a replayable certificate")
    if spec["adapter"] == "finite_model" and receipt["status"] in {"succeeded", "counterexample"}:
        completeness = receipt.get("completeness") or {}
        if completeness.get("complete") is not True:
            raise ContractError("decisive finite result lacks completeness or a decisive verified witness")
    if spec["seed_policy"].get("stochastic"):
        if not receipt.get("uncertainty_analysis") or not receipt.get("certificate", {}).get("seed_policy"):
            raise ContractError("stochastic result lacks uncertainty analysis or seed replay certificate")
    # Replay decisive, hybrid, and operational outcomes alike.  An invalid
    # specification is replayed as the same typed AdapterSpecError; every other
    # status must reproduce the complete epistemic output tuple.  Thus an
    # operational label cannot be substituted for a decisive result (or vice
    # versa) merely by rehashing the receipt.
    try:
        replayed = _independent_adapter_replay(spec, work_directory)
    except AdapterSpecError as exc:
        replayed = {
            "status": "invalid_spec",
            "epistemic_outcome": "not_evaluated",
            "result": {"error": str(exc)},
            "certificate": None,
            "uncertainty_analysis": None,
            "completeness": None,
        }
        replayed["failure"] = _typed_operational_failure(replayed)
        _validate_adapter_output_contract(replayed, spec)
    if _operational_replay_projection(replayed, spec) != _operational_replay_projection(
        receipt, spec
    ):
        qualifier = (
            "operational "
            if receipt["status"] not in {"succeeded", "counterexample"}
            else ""
        )
        raise ContractError(f"independent adapter {qualifier}replay mismatch")
    expected_assimilation = _reflective_assimilation(
        list(spec["conceptual_system_ids"]), receipt["epistemic_outcome"]
    )
    if receipt["reflective_assimilation"] != expected_assimilation:
        raise ContractError(
            "experiment receipt reflective recommendations differ from runtime policy"
        )
    expected_output = experiment_output_digest(receipt)
    if receipt["output_digest"] != expected_output:
        raise ContractError("experiment output digest mismatch")
    if receipt["validator"]["checked_digest"] != expected_output:
        raise ContractError("experiment validator did not validate the exact output")
    expected_receipt_content = _receipt_semantic_digest(receipt)
    if receipt["receipt_content_digest"] != expected_receipt_content:
        raise ContractError("experiment receipt semantic content digest mismatch")
    expected_receipt_id = spec["precommitted_receipt_id"]
    if receipt["receipt_id"] != expected_receipt_id:
        raise ContractError("experiment receipt differs from its precommitted identity")
    linked = [row["conceptual_system_id"] for row in receipt["reflective_assimilation"]]
    if linked != list(spec["conceptual_system_ids"]) or len(linked) != len(set(linked)):
        raise ContractError(
            "every linked conceptual system must receive exactly one ordered recommendation"
        )


def receipt_staleness(receipt: Mapping[str, Any], current_spec: Mapping[str, Any]) -> dict[str, Any]:
    """Explain whether model, decision rule, code, or environment invalidates a receipt."""

    if receipt.get("schema_version") == 2 or current_spec.get("schema_version") == 2:
        return {
            "stale": True,
            "reasons": ["historical_v2_reexecution_required"],
        }
    reasons: list[str] = []
    expected_spec = _top_level_digest(current_spec, "spec_digest")
    if (
        current_spec.get("spec_digest") != expected_spec
        or receipt.get("spec_digest") != expected_spec
    ):
        reasons.append("spec_or_preregistration_changed")
    try:
        current_authority = build_experiment_authority(
            adapter=str(current_spec.get("adapter") or ""),
            model=current_spec.get("model", {}),
        )
    except ExperimentAuthorityError:
        current_authority = None
    if (
        current_authority is None
        or current_spec.get("execution_authority") != current_authority
        or receipt.get("authority_digest") != current_spec.get("authority_digest")
        or receipt.get("code_digest")
        != (
            current_authority["dependency_authority"]["content_digest"]
            if current_authority is not None
            else None
        )
    ):
        reasons.append("adapter_code_changed")
    expected_environment = (
        current_authority["observed_environment"]["content_digest"]
        if current_authority is not None
        else None
    )
    if (
        current_spec.get("environment_digest") != expected_environment
        or receipt.get("environment_digest") != expected_environment
    ):
        reasons.append("environment_changed")
    return {"stale": bool(reasons), "reasons": reasons}


def _typed_execution(function):
    def wrapped(*args: Any, **kwargs: Any) -> dict[str, Any]:
        try:
            return function(*args, **kwargs)
        except ExperimentRuntimeError:
            raise
        except (ContractError, KeyError, OSError, TypeError, ValueError) as exc:
            raise ExperimentExecutionError(
                "experiment_execution_failed", str(exc)
            ) from exc

    return wrapped


@_typed_execution
def execute_experiment(spec: Mapping[str, Any], run_directory: Path | str) -> dict[str, Any]:
    """Execute once in a branch-scoped immutable directory and return a receipt."""

    spec = _validate_v3_spec_shape(spec)
    workdir = experiment_directory(run_directory, spec)
    workdir.mkdir(parents=True, exist_ok=True)
    preregistration_path = workdir / "preregistration.json"
    spec_path = workdir / "spec.json"
    receipt_path = workdir / "receipt.json"
    code_manifest_path = workdir / "code-manifest.json"
    code_digest = spec["code_digest"]
    environment_digest = spec["environment_digest"]
    _write_immutable_json(preregistration_path, dict(spec["preregistration"]))
    _write_immutable_json(spec_path, dict(spec))
    code_manifest = {
        "manifest_version": "dynamic-experiment-code-manifest/3.1.0",
        "adapter_version": spec["code_version"],
        "spec_id": spec["spec_id"],
        "execution_id": spec["execution_id"],
        "authority_digest": spec["authority_digest"],
        "code_digest": code_digest,
        "observed_environment": spec["observed_environment"],
        "environment_digest": environment_digest,
        "execution_authority": spec["execution_authority"],
    }
    code_manifest["content_digest"] = _top_level_digest(
        code_manifest, "content_digest"
    )
    _write_immutable_json(code_manifest_path, code_manifest)
    if receipt_path.exists():
        existing = json.loads(receipt_path.read_text(encoding="utf-8"))
        validate_experiment_receipt(existing, spec, work_directory=workdir)
        if receipt_staleness(existing, spec)["stale"]:
            raise ExperimentReceiptError(
                "existing_receipt_stale", "existing experiment receipt is stale"
            )
        return existing

    governor = ResourceGovernor.from_mapping(spec["resource_budget"], run_directory=workdir)
    started_at = utc_now()
    try:
        output = execute_adapter(spec, governor, workdir)
    except AdapterSpecError as exc:
        output = {
            "status": "invalid_spec",
            "epistemic_outcome": "not_evaluated",
            "result": {"error": str(exc)},
            "certificate": None,
            "uncertainty_analysis": None,
            "completeness": None,
        }
    failure = _typed_operational_failure(output)
    theory_effect = derive_theory_effect(
        spec, status=output["status"], epistemic_outcome=output["epistemic_outcome"]
    )
    reflective_assimilation = _reflective_assimilation(
        list(spec["conceptual_system_ids"]), output["epistemic_outcome"]
    )
    try:
        _validate_adapter_output_contract(output, spec)
    except ContractError as exc:
        raise ExperimentOutputError(
            EXPERIMENT_OUTPUT_CONTRACT_INVALID, str(exc)
        ) from exc
    result_variant = _result_variant(output, spec)
    receipt = {
        "schema_version": 3,
        "contract_version": RUNTIME_CONTRACT_VERSION,
        "receipt_id": spec["precommitted_receipt_id"],
        "receipt_content_digest": "",
        "spec_id": spec["spec_id"],
        "execution_id": spec["execution_id"],
        "experiment_id": spec["experiment_id"],
        "branch_id": spec["branch_id"],
        "target_id": spec["target_id"],
        "run_id": spec["run_id"],
        "state_version": spec["state_version"],
        "theory_programme_id": spec["theory_programme_id"],
        "source_theory_programme_digest": spec[
            "source_theory_programme_digest"
        ],
        "source_reflection_packet_digest": spec[
            "source_reflection_packet_digest"
        ],
        "conceptual_system_ids": list(spec["conceptual_system_ids"]),
        "theoretical_question_id": spec["theoretical_question_id"],
        "adapter": spec["adapter"],
        "status": output["status"],
        "epistemic_outcome": output["epistemic_outcome"],
        "result_variant": result_variant,
        "spec_digest": spec["spec_digest"],
        "authority_digest": spec["authority_digest"],
        "code_digest": code_digest,
        "environment_digest": environment_digest,
        "started_at": started_at,
        "completed_at": utc_now(),
        "resource_usage": governor.receipt("succeeded" if output["status"] in {"succeeded", "counterexample"} else "worker_failed"),
        "resource_authority_boundary": RESOURCE_AUTHORITY_BOUNDARY,
        "resource_provenance_digest": "",
        "result": output["result"],
        "certificate": output["certificate"],
        "uncertainty_analysis": output["uncertainty_analysis"],
        "completeness": output["completeness"],
        "validator": {
            "validator_id": VALIDATOR_ID,
            "version": VALIDATOR_VERSION,
            "status": "valid",
            "checked_digest": "",
        },
        "output_digest": "",
        "transfer_boundary": spec["transfer_boundary"],
        "theory_effect_contract_digest": canonical_digest(
            spec["theory_effect_contract"]
        ),
        "theory_effect": theory_effect,
        "reflective_assimilation": reflective_assimilation,
        "failure": failure,
    }
    receipt["resource_provenance_digest"] = _resource_provenance_digest(receipt)
    receipt["output_digest"] = experiment_output_digest(receipt)
    receipt["validator"]["checked_digest"] = receipt["output_digest"]
    receipt["receipt_content_digest"] = _receipt_semantic_digest(receipt)
    validate_experiment_receipt(receipt, spec, work_directory=workdir)
    _write_immutable_json(receipt_path, receipt)
    return receipt


def plan_v2_experiment_reexecution(
    legacy_spec: Mapping[str, Any],
    legacy_receipt: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a non-authoritative plan; never translate v2 evidence into v3."""

    validation = validate_v2_experiment_artifacts(legacy_spec, legacy_receipt)
    historical_spec_digest = canonical_digest(dict(legacy_spec))
    historical_receipt_digest = (
        canonical_digest(dict(legacy_receipt))
        if legacy_receipt is not None
        else None
    )
    request_fields = (
        "run_id", "branch_id", "adapter", "model", "preregistration",
        "controls", "seed_policy", "resource_budget", "transfer_boundary",
        "theory_effect_contract",
    )
    request_template = {
        field: copy.deepcopy(legacy_spec[field])
        for field in request_fields
        if field in legacy_spec
    }
    plan: dict[str, Any] = {
        "schema_version": 3,
        "migration_contract_version": MIGRATION_CONTRACT_VERSION,
        "migration_id": stable_identifier(
            "experiment-v2-reexecution",
            historical_spec_digest,
            historical_receipt_digest,
        ),
        "status": "reexecution_required",
        "reason_code": "historical_v2_reexecution_required",
        "authoritative_for_current_evidence": False,
        "historical_artifacts": {
            "spec_schema_version": 2,
            "spec_artifact_digest": historical_spec_digest,
            "declared_spec_digest": legacy_spec.get("spec_digest"),
            "receipt_schema_version": (
                2 if legacy_receipt is not None else None
            ),
            "receipt_artifact_digest": historical_receipt_digest,
            "declared_receipt_id": (
                legacy_receipt.get("receipt_id")
                if legacy_receipt is not None
                else None
            ),
            "validation_digest": validation["validation_digest"],
            "validation_status": "valid_historical_non_authoritative",
        },
        "excluded_legacy_authority": [
            "caller_declared_environment",
            "non_transitive_code_digest",
            "result_derived_receipt_identity",
            "legacy_certificate_as_current_authority",
        ],
        "v3_request_template": request_template,
        "required_action": (
            "obtain a current commissioned triage, compile under observed v3 "
            "authority, and independently reexecute every adapter stage"
        ),
    }
    plan["migration_digest"] = _top_level_digest(plan, "migration_digest")
    return plan


def validate_v2_experiment_artifacts(
    legacy_spec: Mapping[str, Any],
    legacy_receipt: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Fully validate frozen v2 bytes before planning a non-authoritative rerun.

    This validates historical internal consistency only. It deliberately does
    not replay against current code, accept caller-declared environment as
    current authority, or promote the historical result into present evidence.
    """

    try:
        if not isinstance(legacy_spec, Mapping) or legacy_spec.get("schema_version") != 2:
            raise ContractError("legacy specification is not schema version 2")
        spec = copy.deepcopy(dict(legacy_spec))
        validate_payload(spec, LEGACY_V2_SPEC_SCHEMA)
        if spec["spec_digest"] != canonical_digest(
            spec, exclude_keys=("spec_digest", "created_at")
        ):
            raise ContractError("historical v2 specification digest mismatch")
        claim = spec["tested_theory_claim"]
        if claim["claim_digest"] != canonical_digest(
            claim, exclude_keys=("claim_digest",)
        ):
            raise ContractError("historical v2 tested claim digest mismatch")
        contract = spec["theory_effect_contract"]
        if (
            claim["claim_id"] != contract["tested_claim_id"]
            or claim["claim_kind"] != contract["tested_claim_kind"]
            or claim["target_relation"] != contract["target_relation"]
        ):
            raise ContractError("historical v2 tested claim crossed its effect contract")

        receipt_digest: str | None = None
        if legacy_receipt is not None:
            if not isinstance(legacy_receipt, Mapping) or legacy_receipt.get("schema_version") != 2:
                raise ContractError("legacy receipt is not schema version 2")
            receipt = copy.deepcopy(dict(legacy_receipt))
            validate_payload(receipt, LEGACY_V2_RECEIPT_SCHEMA)
            for field in (
                "experiment_id", "branch_id", "target_id", "run_id",
                "state_version", "theory_programme_id",
                "source_theory_programme_digest",
                "source_reflection_packet_digest", "conceptual_system_ids",
                "theoretical_question_id", "adapter", "spec_digest",
                "transfer_boundary",
            ):
                expected = spec["spec_digest"] if field == "spec_digest" else spec[field]
                if receipt[field] != expected:
                    raise ContractError(f"historical v2 receipt/spec mismatch for {field}")
            # Frozen v2 schemas allowed open certificate/result objects.  Close
            # that historical gap before even issuing a non-authoritative
            # migration plan: status, outcome, adapter result, certificate,
            # uncertainty, completeness, and preregistration discriminants
            # must form one registered internal output variant.
            _validate_adapter_output_contract(receipt, spec)
            if receipt["failure"] != _typed_operational_failure(receipt):
                raise ContractError("historical v2 failure semantics mismatch")
            if receipt["reflective_assimilation"] != _reflective_assimilation(
                list(spec["conceptual_system_ids"]), receipt["epistemic_outcome"]
            ):
                raise ContractError(
                    "historical v2 reflective assimilation differs from runtime policy"
                )
            try:
                started_at = dt.datetime.fromisoformat(
                    str(receipt["started_at"]).replace("Z", "+00:00")
                )
                completed_at = dt.datetime.fromisoformat(
                    str(receipt["completed_at"]).replace("Z", "+00:00")
                )
            except ValueError as exc:
                raise ContractError("historical v2 receipt timestamps are invalid") from exc
            if (
                started_at.tzinfo is None
                or completed_at.tzinfo is None
                or completed_at < started_at
            ):
                raise ContractError(
                    "historical v2 receipt completion precedes its start"
                )
            if receipt["theory_effect_contract_digest"] != canonical_digest(contract):
                raise ContractError("historical v2 effect-contract digest mismatch")
            if receipt["theory_effect"] != derive_theory_effect(
                spec,
                status=receipt["status"],
                epistemic_outcome=receipt["epistemic_outcome"],
            ):
                raise ContractError("historical v2 theory effect exceeds its contract")
            if receipt["output_digest"] != experiment_output_digest(receipt):
                raise ContractError("historical v2 output digest mismatch")
            if receipt["validator"] != {
                "validator_id": VALIDATOR_ID,
                "version": "2.0.0",
                "status": "valid",
                "checked_digest": receipt["output_digest"],
            }:
                raise ContractError("historical v2 validator record mismatch")
            if (
                receipt["resource_authority_boundary"]
                != LEGACY_V2_RESOURCE_AUTHORITY_BOUNDARY
            ):
                raise ContractError("historical v2 resource authority boundary mismatch")
            if receipt["resource_provenance_digest"] != _resource_provenance_digest(receipt):
                raise ContractError("historical v2 resource provenance digest mismatch")
            if receipt["receipt_content_digest"] != _legacy_v2_receipt_semantic_digest(receipt):
                raise ContractError("historical v2 receipt content digest mismatch")
            expected_receipt_id = stable_identifier(
                "experiment-receipt-v2",
                receipt["experiment_id"],
                receipt["spec_digest"],
                receipt["receipt_content_digest"],
            )
            if receipt["receipt_id"] != expected_receipt_id:
                raise ContractError("historical v2 receipt identity mismatch")
            receipt_digest = canonical_digest(receipt)
        record = {
            "validation_contract": MIGRATION_CONTRACT_VERSION,
            "status": "valid_historical_non_authoritative",
            "authoritative_for_current_evidence": False,
            "spec_artifact_digest": canonical_digest(spec),
            "receipt_artifact_digest": receipt_digest,
        }
        record["validation_digest"] = _top_level_digest(
            record, "validation_digest"
        )
        return record
    except ExperimentMigrationRequired:
        raise
    except (ContractError, KeyError, TypeError, ValueError) as exc:
        raise ExperimentMigrationRequired(
            "legacy_v2_validation_failed", str(exc)
        ) from exc


def reexecute_v2_experiment(
    legacy_spec: Mapping[str, Any],
    legacy_receipt: Mapping[str, Any] | None,
    commissioned_triage: Mapping[str, Any],
    run_directory: Path | str,
    *,
    request_overrides: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Recommission and rerun v2 material; only the new v3 receipt is usable."""

    migration = plan_v2_experiment_reexecution(legacy_spec, legacy_receipt)
    request = copy.deepcopy(migration["v3_request_template"])
    request.update(copy.deepcopy(dict(request_overrides or {})))
    request.pop("experiment_id", None)
    request.pop("created_at", None)
    spec = compile_experiment_spec(commissioned_triage, request)
    receipt = execute_experiment(spec, run_directory)
    return {
        "migration_plan": migration,
        "v3_spec": spec,
        "v3_receipt": receipt,
        "legacy_authoritative": False,
        "v3_receipt_authoritative_after_validation": True,
    }
