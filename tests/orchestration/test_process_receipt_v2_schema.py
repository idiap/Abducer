# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Recursive schema and version-union tests for governed process receipts."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

import pytest

from agentic import process_supervision
from agentic.discovery import benchmark_process
from agentic.discovery.benchmark import BenchmarkIntegrityError
from agentic.discovery.benchmark_process import (
    ExternalBenchmarkProcessAdapter,
    decode_historical_external_process_receipt,
)
from agentic.discovery.contracts import (
    SchemaValidationError,
    canonical_digest,
    validate_payload,
)


SCHEMA = "benchmark_external_process_receipt.schema.json"


def _request() -> dict[str, Any]:
    return {
        "benchmark_id": "schema-benchmark",
        "case_id": "case",
        "domain": "physics",
        "condition": "full_discovery",
        "repetition": 1,
        "task_packet": {"question": "q"},
        "task_packet_digest": "sha256:" + "a" * 64,
        "resource_budget": {
            "tokens": 10,
            # These cases test receipt schemas, not subsecond process timing.
            "wall_seconds": 5.0,
            "cost_units": 1.0,
        },
        "forbidden_generation_input_classes": [],
    }


@pytest.fixture(scope="module")
def v2_receipt_template(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    """Capture real process evidence once for the independent schema attacks."""
    tmp_path = tmp_path_factory.mktemp("process-receipt-schema")
    code = (
        "import json; json.load(__import__('sys').stdin); "
        "print(json.dumps({'candidate_output':{'ok':True},"
        "'resource_usage':{'tokens':2,'wall_seconds':.01,'cost_units':.1},"
        "'generation_input_refs':['tasks/case.json']}))"
    )
    adapter = ExternalBenchmarkProcessAdapter(
        command=[sys.executable, "-c", code],
        role="benchmark_runner",
        benchmark_id="schema-benchmark",
        benchmark_run_id="schema-run",
        run_root=tmp_path,
    )
    adapter.hidden_runner(_request())
    path = next((adapter.run_directory / "receipts" / "benchmark_runner").glob("*.json"))
    receipt = json.loads(path.read_text(encoding="utf-8"))
    validate_payload(receipt, SCHEMA)
    return receipt


@pytest.fixture
def v2_receipt(v2_receipt_template: dict[str, Any]) -> dict[str, Any]:
    """Keep mutations isolated without retesting process timing for every key."""
    return copy.deepcopy(v2_receipt_template)


def _v1_measurement(accounting_root: str) -> dict[str, Any]:
    measured = {"status": "measured", "enforced": True}
    unavailable = {
        "status": "unavailable",
        "enforced": False,
        "reason": "legacy compatibility observation",
    }
    return {
        "wall_time_seconds": dict(measured),
        "cpu_seconds": dict(measured),
        "peak_memory_bytes": dict(measured),
        "disk_bytes": {
            "status": "sampled_high_water",
            "enforced": True,
            "accounting_root": accounting_root,
            "sample_interval_seconds": 0.01,
            "limitation": "legacy sampled observation",
        },
        "network_bytes": dict(unavailable),
        "token_count": dict(unavailable),
        "request_count": dict(unavailable),
        "cost_usd": dict(unavailable),
    }


def _as_v1(receipt: dict[str, Any]) -> dict[str, Any]:
    legacy = copy.deepcopy(receipt)
    legacy["schema_version"] = 1
    event = legacy["process_event"]
    for key in (
        "event_schema_version",
        "supervision_attempt",
        "resource_limit_execution",
        "post_supervision_acceptance",
    ):
        event.pop(key)
    accounting_root = event["resource_measurement"]["disk_bytes"]["accounting_root"]
    event["resource_measurement"] = _v1_measurement(accounting_root)
    legacy["resource_receipt"]["events"] = [copy.deepcopy(event)]
    legacy["resource_receipt"]["resource_measurement"] = _v1_measurement(
        accounting_root
    )
    return legacy


def _at(root: dict[str, Any], path: str) -> dict[str, Any]:
    value: Any = root
    for part in path.split("."):
        value = value[part]
    assert isinstance(value, dict)
    return value


def test_outer_event_receipt_version_union_is_exclusive(
    v2_receipt: dict[str, Any],
) -> None:
    v1_receipt = _as_v1(v2_receipt)
    validate_payload(v1_receipt, SCHEMA)
    validate_payload(v2_receipt, SCHEMA)

    outer_v1_nested_v2 = copy.deepcopy(v2_receipt)
    outer_v1_nested_v2["schema_version"] = 1
    with pytest.raises(SchemaValidationError):
        validate_payload(outer_v1_nested_v2, SCHEMA)

    outer_v2_nested_v1 = copy.deepcopy(v1_receipt)
    outer_v2_nested_v1["schema_version"] = 2
    with pytest.raises(SchemaValidationError):
        validate_payload(outer_v2_nested_v1, SCHEMA)


def test_fully_rehashed_v1_is_decode_only_not_current_authority(
    v2_receipt: dict[str, Any],
) -> None:
    legacy = _as_v1(v2_receipt)
    legacy["resource_receipt_digest"] = canonical_digest(
        legacy["resource_receipt"]
    )
    legacy["content_digest"] = canonical_digest(
        {key: value for key, value in legacy.items() if key != "content_digest"}
    )
    receipt_path = (
        Path(legacy["workspace"]["run_directory"]) / legacy["receipt_ref"]
    )
    validate_payload(legacy, SCHEMA)
    with pytest.raises(BenchmarkIntegrityError, match="decode-only"):
        benchmark_process._validate_receipt(legacy, receipt_path)
    assert decode_historical_external_process_receipt(
        legacy,
        receipt_path=receipt_path,
    ) == legacy


def test_v1_nullable_stdin_limit_is_legacy_only(v2_receipt: dict[str, Any]) -> None:
    legacy = _as_v1(v2_receipt)
    legacy["process_event"]["stdin_limit_bytes"] = None
    legacy["resource_receipt"]["events"][0]["stdin_limit_bytes"] = None
    validate_payload(legacy, SCHEMA)

    current = copy.deepcopy(v2_receipt)
    current["process_event"]["stdin_limit_bytes"] = None
    current["resource_receipt"]["events"][0]["stdin_limit_bytes"] = None
    with pytest.raises(SchemaValidationError):
        validate_payload(current, SCHEMA)


def test_process_and_later_aggregate_measurements_may_differ(
    v2_receipt: dict[str, Any],
) -> None:
    process_measurement = v2_receipt["process_event"]["resource_measurement"]
    aggregate_measurement = v2_receipt["resource_receipt"]["resource_measurement"]
    assert process_measurement != aggregate_measurement
    assert process_measurement["request_count"]["status"] == "unavailable"
    assert aggregate_measurement["request_count"]["status"] == "externally_reported"
    validate_payload(v2_receipt, SCHEMA)


NESTED_REQUIRED_KEYS = (
    ("process_event.supervision_attempt.request", "argv"),
    ("process_event.supervision_attempt.request.environment_bindings.0", "name"),
    ("process_event.supervision_attempt.streams", "stdout"),
    ("process_event.supervision_attempt.streams.stdout", "captured_bytes"),
    ("process_event.supervision_attempt.process", "process_started"),
    ("process_event.supervision_attempt.timing", "clock"),
    ("process_event.supervision_attempt.resource_observation", "wait4_accounting_scope"),
    ("process_event.supervision_attempt.sampling", "policy"),
    ("process_event.supervision_attempt.sampling.policy", "mode"),
    ("process_event.supervision_attempt.limits", "total_deadline_ns"),
    ("process_event.supervision_attempt.containment", "mode"),
    ("process_event.supervision_attempt.authority_boundaries", "semantic_authority"),
    ("process_event.supervision_attempt.invariant_projection", "outcome"),
    ("process_event.supervision_attempt.invariant_projection.outcome", "status"),
    ("process_event.resource_limit_execution", "capture_limit_bytes"),
    ("process_event.resource_limit_execution.resource_exec_plan", "plan_kind"),
    ("process_event.resource_limit_execution.resource_exec_plan.declared_limits", "remaining_cpu_ns"),
    ("process_event.resource_limit_execution.resource_exec_plan.kernel_limits", "rlimit_cpu_soft_seconds"),
    ("process_event.resource_limit_execution.resource_exec_plan.scope", "cpu"),
    ("process_event.resource_limit_execution.pre_execution_observation", "python_executable"),
    ("process_event.resource_limit_execution.pre_execution_observation.python_executable", "sha256"),
    ("process_event.post_supervision_acceptance", "status"),
)


@pytest.mark.parametrize("path,required_key", NESTED_REQUIRED_KEYS)
@pytest.mark.parametrize("mutation", ("extra", "missing"))
def test_every_v2_nested_contract_is_recursively_closed(
    v2_receipt: dict[str, Any],
    path: str,
    required_key: str,
    mutation: str,
) -> None:
    forged = copy.deepcopy(v2_receipt)
    target: Any = forged
    for part in path.split("."):
        target = target[int(part)] if part.isdigit() else target[part]
    assert isinstance(target, dict)
    if mutation == "extra":
        target["unexpected_contract_field"] = True
    else:
        target.pop(required_key)
    with pytest.raises(SchemaValidationError):
        validate_payload(forged, SCHEMA)


def test_failure_variant_schema_exactly_matches_runtime_closed_union() -> None:
    schema_path = (
        Path(__file__).resolve().parents[2]
        / "agentic"
        / "spec"
        / "process_supervision_attempt.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    variants: set[tuple[str, str, str]] = set()
    for branch in schema["$defs"]["failureVariantV2"]["oneOf"]:
        properties = branch["properties"]
        category = properties["category"]["const"]
        stage = properties["stage"]["const"]
        reason_schema = properties["reason_code"]
        reasons = reason_schema.get("enum", [reason_schema.get("const")])
        variants.update((category, stage, reason) for reason in reasons)
    assert variants == process_supervision._FAILURE_VARIANTS


def test_invalid_failure_triple_and_mixed_execution_sums_fail_closed(
    v2_receipt: dict[str, Any],
) -> None:
    invalid_failure = copy.deepcopy(v2_receipt)
    diagnostic = {
        "ordinal": 0,
        "category": "diagnostic",
        "stage": "process_exit",
        "reason_code": "worker_exit_nonzero",
        "message": "invalid triple",
        "message_sha256": "sha256:" + "0" * 64,
        "message_truncated": True,
    }
    invalid_failure["process_event"]["supervision_attempt"][
        "nonfatal_diagnostics"
    ] = [diagnostic]
    invalid_failure["resource_receipt"]["events"][0] = copy.deepcopy(
        invalid_failure["process_event"]
    )
    with pytest.raises(SchemaValidationError):
        validate_payload(invalid_failure, SCHEMA)

    mixed = copy.deepcopy(v2_receipt)
    mixed["process_event"]["supervision_attempt"] = None
    mixed["resource_receipt"]["events"][0] = copy.deepcopy(mixed["process_event"])
    with pytest.raises(SchemaValidationError):
        validate_payload(mixed, SCHEMA)

    not_run = copy.deepcopy(v2_receipt)
    not_run["process_event"]["post_supervision_acceptance"]["status"] = "not_run"
    not_run["resource_receipt"]["events"][0] = copy.deepcopy(
        not_run["process_event"]
    )
    with pytest.raises(SchemaValidationError):
        validate_payload(not_run, SCHEMA)


def test_observation_and_top_outcome_discriminants_fail_closed(
    v2_receipt: dict[str, Any],
) -> None:
    missing_post_observation = copy.deepcopy(v2_receipt)
    execution = missing_post_observation["process_event"][
        "resource_limit_execution"
    ]
    execution["post_execution_observation"] = None
    execution["observation_error"] = None
    missing_post_observation["resource_receipt"]["events"][0] = copy.deepcopy(
        missing_post_observation["process_event"]
    )
    with pytest.raises(SchemaValidationError):
        validate_payload(missing_post_observation, SCHEMA)

    accepted_without_response = copy.deepcopy(v2_receipt)
    accepted_without_response["response_payload"] = None
    accepted_without_response["response_digest"] = None
    with pytest.raises(SchemaValidationError):
        validate_payload(accepted_without_response, SCHEMA)
