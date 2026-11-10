# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Preregister and execute the theory-first discovery comparison study.

The study is deliberately a matched, one-factor-at-a-time design.  One
baseline plus eighteen predeclared perturbations covers the literature,
counterfactual, hypothesis, reflection, evaluator, abstraction, intake, and
descendant-support factors requested by the discovery workflow.  Two replay
replicates and eight protocol stages produce exactly 304 accepted protocol
receipts when the run is complete.  Those receipts are replay evidence, not
304 statistical samples.

Each matched cell executes in the existing bounded, killable process wave.
Workers receive the same frozen resources and task clusters.  They must return
complete opaque candidate content, a set-valued outcome, uncertainty,
agreement, adverse findings, and explicit null findings at every stage.
Operational failure is retained as a terminal receipt and forces the whole
study to a descriptive NULL result.  Publication and every causal, efficacy,
independence, merit, value, truth, and generalization authority remain false.
"""

from __future__ import annotations

import copy
import os
import re
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from .contracts import ContractError, canonical_digest, stable_identifier, validate_identifier
from .parallel import run_bounded_killable_request_wave


SCHEMA_VERSION = "1.0.0"
REPETITIONS = 2
STAGE_IDS = (
    "literature-conditioning",
    "hypothesis-generation",
    "reflective-deepening",
    "formal-abstraction",
    "conceptual-merit-evaluation",
    "theory-intake",
    "descendant-support",
    "outcome-projection",
)
BASELINE_AXES = {
    "literature": "current",
    "counterfactual": "semantic",
    "hypothesis": "aggressive_generative",
    "reflection": "full",
    "evaluator": "semantic",
    "abstraction": "capable_nonformal",
    "intake": "intake",
    "descendant_support": "no_support",
}
FACTOR_VARIATIONS = (
    ("literature", "historical"),
    ("literature", "no_literature"),
    ("counterfactual", "identity_only"),
    ("hypothesis", "fixed_template"),
    ("hypothesis", "conservative_control"),
    ("reflection", "sham"),
    ("reflection", "removal"),
    ("evaluator", "status_only"),
    ("abstraction", "category"),
    ("abstraction", "hott"),
    ("abstraction", "category_then_hott"),
    ("abstraction", "hott_then_category"),
    ("abstraction", "decorative"),
    ("abstraction", "no_abstraction"),
    ("intake", "no_intake"),
    ("descendant_support", "symbolic"),
    ("descendant_support", "simulation"),
    ("descendant_support", "symbolic_and_simulation"),
)
EXPECTED_CONDITION_COUNT = 19
EXPECTED_CELL_COUNT = EXPECTED_CONDITION_COUNT * REPETITIONS
EXPECTED_PROTOCOL_RECEIPT_COUNT = EXPECTED_CELL_COUNT * len(STAGE_IDS)
WORKER_BOUNDARY = (
    "A completed cell proves only bounded process execution and replayable "
    "protocol content. It grants no provider, model, human, cognitive, "
    "semantic, evaluator, merit, truth, or physics authority."
)
AUTHORITY_NULLS = {
    "causal_effect_authority": None,
    "creativity_efficacy_authority": None,
    "literature_benefit_authority": None,
    "conceptual_merit_authority": None,
    "category_hott_value_authority": None,
    "experiment_value_authority": None,
    "provider_independence_authority": None,
    "evaluator_independence_authority": None,
    "external_human_authority": None,
    "population_generalization_authority": None,
    "truth_authority": None,
    "physics_value_authority": None,
}
AUTHORITY_BOUNDARY = (
    "The report is publication-disabled, internally correlated, descriptive "
    "protocol calibration. Sensitivity, invariance, agreement, or repeated "
    "execution does not authorize causal effects, discovery efficacy, "
    "literature benefit, conceptual merit, Category/HoTT value, experiment "
    "value, independence, external-human preference, population "
    "generalization, truth, or physics value."
)
DEFAULT_RESOURCE_PROFILE = {
    "branch_wall_seconds": 5.0,
    "portfolio_wall_seconds": 90.0,
    "max_workers": 8,
    "cpu_seconds": 4,
    "memory_bytes": 536_870_912,
    "max_output_bytes": 1_048_576,
}
_HEX64 = re.compile(r"^sha256:[0-9a-f]{64}$")
_FORBIDDEN_BLIND_KEYS = frozenset(
    {
        "condition_id",
        "changed_axis",
        "changed_level",
        "treatment_axes",
        "route_id",
        "route_label",
        "method_label",
        "formal_status",
        "provider_id",
        "producer_id",
        "winner",
        "score",
    }
)
StudyWorker = Callable[[Mapping[str, Any]], Mapping[str, Any]]


class PreregisteredFactorialStudyError(ContractError):
    """Fail-closed study design, worker-output, or replay error."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"preregistered_factorial_study[{reason_code}]: {message}")


def _fail(reason_code: str, message: str) -> None:
    raise PreregisteredFactorialStudyError(reason_code, message)


def _exact(value: Mapping[str, Any], fields: set[str], label: str) -> None:
    if not isinstance(value, Mapping) or set(value) != fields:
        _fail("contract_shape_invalid", f"{label} has an open or incomplete shape")


def _text(value: Any, label: str) -> str:
    result = " ".join(str(value or "").split())
    if not result:
        _fail("contract_value_invalid", f"{label} must be nonempty")
    return result


def _text_list(
    value: Any,
    label: str,
    *,
    minimum: int = 1,
    unique: bool = True,
) -> list[str]:
    if (
        not isinstance(value, Sequence)
        or isinstance(value, (str, bytes, bytearray))
        or len(value) < minimum
    ):
        _fail("contract_value_invalid", f"{label} must contain at least {minimum} rows")
    rows = [_text(item, label) for item in value]
    if unique and len(rows) != len(set(rows)):
        _fail("contract_value_invalid", f"{label} rows must be unique")
    return rows


def _sealed(core: Mapping[str, Any], digest_field: str = "content_digest") -> dict[str, Any]:
    result = copy.deepcopy(dict(core))
    result[digest_field] = canonical_digest(result)
    return result


def _verify_seal(value: Mapping[str, Any], digest_field: str, label: str) -> None:
    expected = canonical_digest(
        {key: child for key, child in value.items() if key != digest_field}
    )
    if value.get(digest_field) != expected:
        _fail("digest_mismatch", f"{label} digest changed")


def _resource_profile(value: Mapping[str, Any] | None) -> dict[str, Any]:
    profile = copy.deepcopy(dict(value or DEFAULT_RESOURCE_PROFILE))
    _exact(
        profile,
        {
            "branch_wall_seconds",
            "portfolio_wall_seconds",
            "max_workers",
            "cpu_seconds",
            "memory_bytes",
            "max_output_bytes",
        },
        "resource profile",
    )
    for field in ("max_workers", "cpu_seconds", "memory_bytes", "max_output_bytes"):
        item = profile[field]
        if isinstance(item, bool) or not isinstance(item, int) or item < 1:
            _fail("resource_profile_invalid", f"{field} must be a positive integer")
    for field in ("branch_wall_seconds", "portfolio_wall_seconds"):
        item = profile[field]
        if isinstance(item, bool) or not isinstance(item, (int, float)) or item <= 0:
            _fail("resource_profile_invalid", f"{field} must be positive")
    if float(profile["branch_wall_seconds"]) > float(
        profile["portfolio_wall_seconds"]
    ):
        _fail(
            "resource_profile_invalid",
            "branch deadline cannot exceed portfolio deadline",
        )
    if float(profile["portfolio_wall_seconds"]) > 3600:
        _fail("resource_profile_invalid", "portfolio deadline exceeds one hour")
    return profile


def _condition_rows() -> list[dict[str, Any]]:
    raw: list[tuple[str, str, dict[str, str]]] = [
        ("baseline", "baseline", copy.deepcopy(BASELINE_AXES))
    ]
    for axis, level in FACTOR_VARIATIONS:
        axes = copy.deepcopy(BASELINE_AXES)
        axes[axis] = level
        raw.append((axis, level, axes))
    rows: list[dict[str, Any]] = []
    for axis, level, axes in raw:
        core = {
            "condition_id": stable_identifier(
                "factorial-condition", axis, level
            ),
            "changed_axis": axis,
            "changed_level": level,
            "treatment_axes": axes,
        }
        rows.append(_sealed(core, "condition_digest"))
    if len(rows) != EXPECTED_CONDITION_COUNT:
        _fail("internal_design_invalid", "the preregistered condition count drifted")
    return rows


def _study_id_basis(
    *,
    task_cluster_ids: Sequence[str],
    entropy_digest: str,
    resource_profile: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "task_cluster_ids": list(task_cluster_ids),
        "entropy_digest": entropy_digest,
        "resource_profile": copy.deepcopy(dict(resource_profile)),
        "repetitions": REPETITIONS,
        "stage_ids": list(STAGE_IDS),
        "conditions": _condition_rows(),
    }


def _allocation_rows(
    *,
    study_id: str,
    entropy_digest: str,
    conditions: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    first = sorted(
        (copy.deepcopy(dict(row)) for row in conditions),
        key=lambda row: canonical_digest(
            {
                "entropy_digest": entropy_digest,
                "condition_digest": row["condition_digest"],
            }
        ),
    )
    orders = (first, list(reversed(first)))
    rows: list[dict[str, Any]] = []
    ordinal = 0
    for repetition, order in enumerate(orders, start=1):
        for within_repetition, condition in enumerate(order):
            rows.append(
                {
                    "ordinal": ordinal,
                    "within_repetition": within_repetition,
                    "repetition": repetition,
                    "condition_id": condition["condition_id"],
                    "branch_id": stable_identifier(
                        "factorial-cell",
                        study_id,
                        condition["condition_id"],
                        repetition,
                    ),
                }
            )
            ordinal += 1
    return rows


def build_preregistered_factorial_design(
    *,
    task_cluster_ids: Sequence[str],
    entropy_commitment: str,
    resource_profile: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Freeze the exact 19-condition, two-replicate comparison design."""

    clusters = _text_list(
        task_cluster_ids,
        "task cluster identifiers",
        minimum=2,
    )
    for cluster_id in clusters:
        validate_identifier(cluster_id, "task cluster identifier")
    entropy_digest = canonical_digest(
        {"entropy_commitment": _text(entropy_commitment, "entropy commitment")}
    )
    profile = _resource_profile(resource_profile)
    basis = _study_id_basis(
        task_cluster_ids=clusters,
        entropy_digest=entropy_digest,
        resource_profile=profile,
    )
    study_id = stable_identifier("preregistered-factorial-study", canonical_digest(basis))
    conditions = basis["conditions"]
    core = {
        **basis,
        "study_id": study_id,
        "allocations": _allocation_rows(
            study_id=study_id,
            entropy_digest=entropy_digest,
            conditions=conditions,
        ),
        "expected_condition_count": EXPECTED_CONDITION_COUNT,
        "expected_cell_count": EXPECTED_CELL_COUNT,
        "expected_protocol_receipt_count": EXPECTED_PROTOCOL_RECEIPT_COUNT,
        "protocol_receipts_are_samples": False,
        "publication_enabled": False,
        "effect_inference_authorized": False,
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    return validate_preregistered_factorial_design(_sealed(core))


def validate_preregistered_factorial_design(
    design: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay the exact factor levels, allocation, resources, and nulls."""

    _exact(
        design,
        {
            "schema_version",
            "study_id",
            "task_cluster_ids",
            "entropy_digest",
            "resource_profile",
            "repetitions",
            "stage_ids",
            "conditions",
            "allocations",
            "expected_condition_count",
            "expected_cell_count",
            "expected_protocol_receipt_count",
            "protocol_receipts_are_samples",
            "publication_enabled",
            "effect_inference_authorized",
            "authority_nulls",
            "authority_boundary",
            "content_digest",
        },
        "factorial design",
    )
    _verify_seal(design, "content_digest", "factorial design")
    if design["schema_version"] != SCHEMA_VERSION:
        _fail("schema_version_invalid", "factorial design version is unsupported")
    clusters = _text_list(
        design["task_cluster_ids"], "task cluster identifiers", minimum=2
    )
    for cluster_id in clusters:
        validate_identifier(cluster_id, "task cluster identifier")
    if not _HEX64.fullmatch(str(design["entropy_digest"])):
        _fail("entropy_invalid", "entropy digest is not canonical SHA-256")
    profile = _resource_profile(design["resource_profile"])
    if design["repetitions"] != REPETITIONS or design["stage_ids"] != list(STAGE_IDS):
        _fail("protocol_grid_invalid", "repetition or stage grid changed")
    expected_conditions = _condition_rows()
    if design["conditions"] != expected_conditions:
        _fail("factor_grid_invalid", "the 19 preregistered conditions changed")
    basis = _study_id_basis(
        task_cluster_ids=clusters,
        entropy_digest=str(design["entropy_digest"]),
        resource_profile=profile,
    )
    expected_study_id = stable_identifier(
        "preregistered-factorial-study", canonical_digest(basis)
    )
    if design["study_id"] != expected_study_id:
        _fail("study_identity_invalid", "study identity is not content-derived")
    expected_allocations = _allocation_rows(
        study_id=expected_study_id,
        entropy_digest=str(design["entropy_digest"]),
        conditions=expected_conditions,
    )
    if design["allocations"] != expected_allocations:
        _fail(
            "allocation_invalid",
            "allocation is not the deterministic counterbalanced schedule",
        )
    if (
        design["expected_condition_count"] != EXPECTED_CONDITION_COUNT
        or design["expected_cell_count"] != EXPECTED_CELL_COUNT
        or design["expected_protocol_receipt_count"]
        != EXPECTED_PROTOCOL_RECEIPT_COUNT
    ):
        _fail("protocol_grid_invalid", "declared protocol cardinalities changed")
    if (
        design["protocol_receipts_are_samples"] is not False
        or design["publication_enabled"] is not False
        or design["effect_inference_authorized"] is not False
        or design["authority_nulls"] != AUTHORITY_NULLS
        or design["authority_boundary"] != AUTHORITY_BOUNDARY
    ):
        _fail("authority_escalation", "factorial design invented authority")
    return copy.deepcopy(dict(design))


def _requests(design: Mapping[str, Any]) -> list[dict[str, Any]]:
    condition_by_id = {
        row["condition_id"]: row for row in design["conditions"]
    }
    requests: list[dict[str, Any]] = []
    for allocation in design["allocations"]:
        core = {
            "branch_id": allocation["branch_id"],
            "study_id": design["study_id"],
            "cell_id": allocation["branch_id"],
            "condition": copy.deepcopy(
                condition_by_id[allocation["condition_id"]]
            ),
            "repetition": allocation["repetition"],
            "task_cluster_ids": copy.deepcopy(design["task_cluster_ids"]),
            "stage_ids": list(STAGE_IDS),
            "resource_profile": copy.deepcopy(design["resource_profile"]),
            "budget": {
                "wall_seconds": float(
                    design["resource_profile"]["branch_wall_seconds"]
                )
            },
            "worker_contract": WORKER_BOUNDARY,
        }
        requests.append({**core, "request_digest": canonical_digest(core)})
    return requests


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, Mapping):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(child))
    elif isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        for child in value:
            keys.update(_walk_keys(child))
    return keys


def _validate_complete_content(
    value: Mapping[str, Any],
    *,
    blind: bool,
) -> dict[str, Any]:
    _exact(value, {"candidate_contents", "content_digest"}, "complete content")
    rows = value["candidate_contents"]
    if not isinstance(rows, list) or not rows:
        _fail(
            "worker_output_invalid",
            "complete content must contain at least one full candidate",
        )
    opaque_ids: list[str] = []
    for row in rows:
        _exact(
            row,
            {"opaque_candidate_id", "content", "sealed_evidence"},
            "complete candidate",
        )
        opaque_id = _text(row["opaque_candidate_id"], "opaque candidate id")
        validate_identifier(opaque_id, "opaque candidate id")
        opaque_ids.append(opaque_id)
        content = row["content"]
        _exact(
            content,
            {
                "conceptual_core",
                "mechanism",
                "protected_successes",
                "falsifier",
                "correction",
                "physics_return",
            },
            "candidate conceptual content",
        )
        for field in (
            "conceptual_core",
            "mechanism",
            "falsifier",
            "correction",
            "physics_return",
        ):
            _text(content[field], f"candidate {field}")
        _text_list(
            content["protected_successes"],
            "candidate protected successes",
            minimum=1,
        )
        evidence = row["sealed_evidence"]
        if not isinstance(evidence, list) or not evidence:
            _fail("worker_output_invalid", "candidate evidence must be nonempty")
        for item in evidence:
            _exact(item, {"pointer", "digest"}, "sealed candidate evidence")
            if not _text(item["pointer"], "evidence pointer").startswith("/"):
                _fail(
                    "worker_output_invalid",
                    "candidate evidence pointer must be absolute JSON Pointer",
                )
            if not _HEX64.fullmatch(str(item["digest"])):
                _fail("worker_output_invalid", "candidate evidence digest is invalid")
    if len(opaque_ids) != len(set(opaque_ids)):
        _fail("worker_output_invalid", "opaque candidate ids must be unique")
    expected = canonical_digest(rows)
    if value["content_digest"] != expected:
        _fail("digest_mismatch", "complete candidate content digest changed")
    if blind and _walk_keys(value).intersection(_FORBIDDEN_BLIND_KEYS):
        _fail(
            "blind_projection_leak",
            "conceptual evaluator content leaked route, status, score, or winner fields",
        )
    return copy.deepcopy(dict(value))


def _validate_stage_record(
    value: Mapping[str, Any],
    *,
    expected_stage_id: str,
) -> dict[str, Any]:
    _exact(
        value,
        {
            "stage_id",
            "status",
            "complete_content",
            "set_valued_outcome",
            "uncertainty",
            "agreement",
            "adverse_findings",
            "null_findings",
            "record_digest",
        },
        "stage record",
    )
    _verify_seal(value, "record_digest", "stage record")
    if value["stage_id"] != expected_stage_id:
        _fail("stage_order_invalid", "worker stage order or identity changed")
    if value["status"] not in {"completed", "typed_null"}:
        _fail("worker_output_invalid", "stage status is unsupported")
    complete = _validate_complete_content(
        value["complete_content"],
        blind=expected_stage_id == "conceptual-merit-evaluation",
    )
    candidate_ids = {
        row["opaque_candidate_id"] for row in complete["candidate_contents"]
    }
    outcome = _text_list(
        value["set_valued_outcome"],
        "set-valued outcome",
        minimum=0 if value["status"] == "typed_null" else 1,
    )
    if outcome != sorted(outcome) or not set(outcome).issubset(candidate_ids):
        _fail(
            "worker_output_invalid",
            "set-valued outcome is not a sorted candidate subset",
        )
    for field in ("uncertainty", "agreement"):
        child = value[field]
        _exact(child, {"status", "summary"}, field)
        if child["status"] not in {"reported", "unavailable"}:
            _fail("worker_output_invalid", f"{field} status is unsupported")
        _text(child["summary"], f"{field} summary")
    _text_list(
        value["adverse_findings"],
        "adverse findings",
        minimum=0,
        unique=False,
    )
    _text_list(value["null_findings"], "null findings", minimum=1)
    return copy.deepcopy(dict(value))


def validate_factorial_cell_result(
    result: Mapping[str, Any],
    request: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one worker result against its exact precommitted cell."""

    _exact(
        result,
        {
            "request_digest",
            "cell_id",
            "repetition",
            "worker_pid",
            "stage_records",
            "worker_boundary",
            "result_digest",
        },
        "factorial cell result",
    )
    _verify_seal(result, "result_digest", "factorial cell result")
    if (
        result["request_digest"] != request["request_digest"]
        or result["cell_id"] != request["cell_id"]
        or result["repetition"] != request["repetition"]
    ):
        _fail("worker_binding_invalid", "worker result changed its cell binding")
    if (
        isinstance(result["worker_pid"], bool)
        or not isinstance(result["worker_pid"], int)
        or result["worker_pid"] < 1
    ):
        _fail("worker_output_invalid", "worker pid is invalid")
    if result["worker_boundary"] != WORKER_BOUNDARY:
        _fail("authority_escalation", "worker boundary changed")
    records = result["stage_records"]
    if not isinstance(records, list) or len(records) != len(STAGE_IDS):
        _fail("protocol_receipt_count_invalid", "cell must return exactly eight stages")
    for record, stage_id in zip(records, STAGE_IDS, strict=True):
        _validate_stage_record(record, expected_stage_id=stage_id)
    return copy.deepcopy(dict(result))


def _terminal(
    *,
    request: Mapping[str, Any],
    outcome: Mapping[str, Any],
) -> dict[str, Any]:
    message = outcome.get("message")
    process = {
        "started_at": _text(outcome.get("started_at"), "worker start time"),
        "elapsed_seconds": max(0.0, float(outcome.get("elapsed", 0.0))),
        "message_kind": str(message.get("kind", "invalid"))
        if isinstance(message, Mapping)
        else "invalid",
    }
    result: dict[str, Any] | None = None
    failure: dict[str, str] | None = None
    status = "failed"
    if isinstance(message, Mapping) and message.get("kind") == "ok":
        try:
            payload = message.get("payload")
            if not isinstance(payload, Mapping):
                _fail("worker_output_invalid", "worker payload is not an object")
            result = validate_factorial_cell_result(payload, request)
            status = "completed"
        except (ContractError, ValueError, TypeError) as exc:
            failure = {
                "error_class": type(exc).__name__,
                "detail": _text(exc, "worker validation failure"),
            }
            status = "invalid"
    else:
        failure = {
            "error_class": _text(
                message.get("error_class", "WorkerFailure")
                if isinstance(message, Mapping)
                else "InvalidWorkerMessage",
                "worker failure class",
            ),
            "detail": _text(
                message.get("detail", "worker returned no valid terminal message")
                if isinstance(message, Mapping)
                else "worker returned no valid terminal message",
                "worker failure detail",
            ),
        }
    core = {
        "terminal_status": status,
        "request": copy.deepcopy(dict(request)),
        "process": process,
        "result": result,
        "failure": failure,
    }
    return _sealed(core, "terminal_digest")


def _scientific_projection(
    terminals: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    accepted = 0
    for terminal in terminals:
        request = terminal["request"]
        result = terminal["result"]
        if terminal["terminal_status"] == "completed":
            records = result["stage_records"]
            accepted += len(records)
            final = records[-1]
            row = {
                "condition_id": request["condition"]["condition_id"],
                "repetition": request["repetition"],
                "terminal_status": "completed",
                "set_valued_outcome": copy.deepcopy(final["set_valued_outcome"]),
                "uncertainty": copy.deepcopy(final["uncertainty"]),
                "agreement": copy.deepcopy(final["agreement"]),
                "adverse_findings": copy.deepcopy(final["adverse_findings"]),
                "null_findings": copy.deepcopy(final["null_findings"]),
            }
        else:
            row = {
                "condition_id": request["condition"]["condition_id"],
                "repetition": request["repetition"],
                "terminal_status": terminal["terminal_status"],
                "set_valued_outcome": [],
                "uncertainty": {
                    "status": "unavailable",
                    "summary": "Cell failure prevents uncertainty interpretation.",
                },
                "agreement": {
                    "status": "unavailable",
                    "summary": "Cell failure prevents agreement interpretation.",
                },
                "adverse_findings": [
                    f"{terminal['failure']['error_class']}: "
                    f"{terminal['failure']['detail']}"
                ],
                "null_findings": [
                    "The failed cell contributes no causal, efficacy, merit, or value evidence."
                ],
            }
        rows.append(row)
    rows.sort(key=lambda row: (row["condition_id"], row["repetition"]))
    completed = sum(row["terminal_status"] == "completed" for row in rows)
    status = (
        "completed_descriptive_only"
        if completed == EXPECTED_CELL_COUNT
        and accepted == EXPECTED_PROTOCOL_RECEIPT_COUNT
        else "partial_failure_null"
    )
    return {
        "status": status,
        "condition_outcomes": rows,
        "completed_cell_count": completed,
        "failed_cell_count": EXPECTED_CELL_COUNT - completed,
        "accepted_protocol_receipt_count": accepted,
        "expected_protocol_receipt_count": EXPECTED_PROTOCOL_RECEIPT_COUNT,
        "protocol_receipts_are_samples": False,
        "descriptive_only": True,
        "causal_effect": None,
        "comparative_advantage": None,
        "population_generalization": None,
    }


def _process_observation(
    terminals: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    pids = sorted(
        {
            terminal["result"]["worker_pid"]
            for terminal in terminals
            if terminal["terminal_status"] == "completed"
        }
    )
    return {
        "distinct_worker_pid_count": len(pids),
        "all_completed_workers_outside_parent": bool(pids)
        and all(pid != os.getpid() for pid in pids),
        "process_plurality_observed": len(pids) >= 2,
        "independence_authorized": False,
    }


def run_preregistered_factorial_study(
    design: Mapping[str, Any],
    worker: StudyWorker,
) -> dict[str, Any]:
    """Execute all 38 matched cells in bounded killable worker processes."""

    checked = validate_preregistered_factorial_design(design)
    requests = _requests(checked)
    outcomes = run_bounded_killable_request_wave(
        requests,
        worker,
        max_workers=int(checked["resource_profile"]["max_workers"]),
        portfolio_wall_seconds=float(
            checked["resource_profile"]["portfolio_wall_seconds"]
        ),
    )
    if len(outcomes) != EXPECTED_CELL_COUNT:
        _fail("terminal_barrier_invalid", "process wave lost a terminal cell")
    terminals = [
        _terminal(request=request, outcome=outcome)
        for request, outcome in zip(requests, outcomes, strict=True)
    ]
    projection = _scientific_projection(terminals)
    core = {
        "schema_version": SCHEMA_VERSION,
        "study_id": checked["study_id"],
        "design": checked,
        "status": projection["status"],
        "terminals": terminals,
        "scientific_projection": projection,
        "process_boundary_observation": _process_observation(terminals),
        "expected_protocol_receipt_count": EXPECTED_PROTOCOL_RECEIPT_COUNT,
        "accepted_protocol_receipt_count": projection[
            "accepted_protocol_receipt_count"
        ],
        "protocol_receipts_are_samples": False,
        "publication_enabled": False,
        "effect_inference_authorized": False,
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    return validate_preregistered_factorial_study(_sealed(core))


def validate_preregistered_factorial_study(
    report: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay a complete or partial study without granting outcome authority."""

    _exact(
        report,
        {
            "schema_version",
            "study_id",
            "design",
            "status",
            "terminals",
            "scientific_projection",
            "process_boundary_observation",
            "expected_protocol_receipt_count",
            "accepted_protocol_receipt_count",
            "protocol_receipts_are_samples",
            "publication_enabled",
            "effect_inference_authorized",
            "authority_nulls",
            "authority_boundary",
            "content_digest",
        },
        "factorial study report",
    )
    _verify_seal(report, "content_digest", "factorial study report")
    design = validate_preregistered_factorial_design(report["design"])
    if report["schema_version"] != SCHEMA_VERSION or report["study_id"] != design["study_id"]:
        _fail("study_identity_invalid", "report identity changed")
    requests = _requests(design)
    terminals = report["terminals"]
    if not isinstance(terminals, list) or len(terminals) != EXPECTED_CELL_COUNT:
        _fail("terminal_barrier_invalid", "report lacks exactly 38 terminals")
    for terminal, request in zip(terminals, requests, strict=True):
        _exact(
            terminal,
            {
                "terminal_status",
                "request",
                "process",
                "result",
                "failure",
                "terminal_digest",
            },
            "terminal receipt",
        )
        _verify_seal(terminal, "terminal_digest", "terminal receipt")
        if terminal["request"] != request:
            _fail("worker_binding_invalid", "terminal request changed")
        _exact(
            terminal["process"],
            {"started_at", "elapsed_seconds", "message_kind"},
            "terminal process observation",
        )
        _text(terminal["process"]["started_at"], "worker start time")
        elapsed = terminal["process"]["elapsed_seconds"]
        if isinstance(elapsed, bool) or not isinstance(elapsed, (int, float)) or elapsed < 0:
            _fail("worker_output_invalid", "terminal elapsed time is invalid")
        _text(terminal["process"]["message_kind"], "worker message kind")
        if terminal["terminal_status"] == "completed":
            if terminal["failure"] is not None or not isinstance(
                terminal["result"], Mapping
            ):
                _fail("terminal_state_invalid", "completed terminal is inconsistent")
            validate_factorial_cell_result(terminal["result"], request)
        elif terminal["terminal_status"] in {"failed", "invalid"}:
            if terminal["result"] is not None or not isinstance(
                terminal["failure"], Mapping
            ):
                _fail("terminal_state_invalid", "failed terminal is inconsistent")
            _exact(
                terminal["failure"],
                {"error_class", "detail"},
                "terminal failure",
            )
            _text(terminal["failure"]["error_class"], "terminal failure class")
            _text(terminal["failure"]["detail"], "terminal failure detail")
        else:
            _fail("terminal_state_invalid", "terminal status is unsupported")
    projection = _scientific_projection(terminals)
    if report["scientific_projection"] != projection or report["status"] != projection["status"]:
        _fail("scientific_projection_invalid", "scientific projection is not replay-derived")
    observation = _process_observation(terminals)
    if report["process_boundary_observation"] != observation:
        _fail("process_observation_invalid", "process observation changed")
    if projection["status"] == "completed_descriptive_only" and (
        observation["process_plurality_observed"] is not True
        or observation["all_completed_workers_outside_parent"] is not True
    ):
        _fail("process_observation_invalid", "complete study lacks real process plurality")
    if (
        report["expected_protocol_receipt_count"]
        != EXPECTED_PROTOCOL_RECEIPT_COUNT
        or report["accepted_protocol_receipt_count"]
        != projection["accepted_protocol_receipt_count"]
        or report["protocol_receipts_are_samples"] is not False
        or report["publication_enabled"] is not False
        or report["effect_inference_authorized"] is not False
        or report["authority_nulls"] != AUTHORITY_NULLS
        or report["authority_boundary"] != AUTHORITY_BOUNDARY
    ):
        _fail("authority_escalation", "factorial report invented authority")
    return copy.deepcopy(dict(report))


def seal_factorial_stage_record(
    *,
    stage_id: str,
    status: str,
    candidate_contents: Sequence[Mapping[str, Any]],
    set_valued_outcome: Sequence[str],
    uncertainty: Mapping[str, Any],
    agreement: Mapping[str, Any],
    adverse_findings: Sequence[str],
    null_findings: Sequence[str],
) -> dict[str, Any]:
    """Provider helper for building one exact, digest-bound stage record."""

    rows = [copy.deepcopy(dict(row)) for row in candidate_contents]
    complete = {
        "candidate_contents": rows,
        "content_digest": canonical_digest(rows),
    }
    core = {
        "stage_id": stage_id,
        "status": status,
        "complete_content": complete,
        "set_valued_outcome": sorted(str(item) for item in set_valued_outcome),
        "uncertainty": copy.deepcopy(dict(uncertainty)),
        "agreement": copy.deepcopy(dict(agreement)),
        "adverse_findings": [str(item) for item in adverse_findings],
        "null_findings": [str(item) for item in null_findings],
    }
    return _sealed(core, "record_digest")


def seal_factorial_cell_result(
    request: Mapping[str, Any],
    *,
    worker_pid: int,
    stage_records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Provider helper for binding eight stage records to one exact request."""

    core = {
        "request_digest": request["request_digest"],
        "cell_id": request["cell_id"],
        "repetition": request["repetition"],
        "worker_pid": worker_pid,
        "stage_records": [copy.deepcopy(dict(row)) for row in stage_records],
        "worker_boundary": WORKER_BOUNDARY,
    }
    return _sealed(core, "result_digest")


__all__ = [
    "AUTHORITY_BOUNDARY",
    "AUTHORITY_NULLS",
    "BASELINE_AXES",
    "EXPECTED_CELL_COUNT",
    "EXPECTED_CONDITION_COUNT",
    "EXPECTED_PROTOCOL_RECEIPT_COUNT",
    "FACTOR_VARIATIONS",
    "PreregisteredFactorialStudyError",
    "REPETITIONS",
    "STAGE_IDS",
    "build_preregistered_factorial_design",
    "run_preregistered_factorial_study",
    "seal_factorial_cell_result",
    "seal_factorial_stage_record",
    "validate_factorial_cell_result",
    "validate_preregistered_factorial_design",
    "validate_preregistered_factorial_study",
]
