# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Held-out conceptual-discovery benchmark capture and evaluation.

Two evidence lanes are intentionally disjoint:

* ``synthetic_protocol_fixture`` exercises leakage, time-slice, blinding-shape,
  and scoring code. Synthetic ratings never authorize an efficacy claim.
* ``live_external_hidden_task`` captures actual outputs before truth is loaded,
  runs full baselines and ablations under equal opportunity budgets, and only
  authorizes efficacy after an external verifier authenticates blinded human
  ratings over repeated, domain-disjoint tasks.
"""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import math
import random
import re
import statistics
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from .contracts import validate_payload


RUBRIC_DIMENSIONS = (
    "target_relevance",
    "conceptual_depth",
    "explanatory_understanding",
    "unification_with_preserved_difference",
    "philosophical_clarity",
    "generativity",
    "coherence",
    "honest_truth_boundary",
)
SYNTHETIC_MODE = "synthetic_protocol_fixture"
LIVE_MODE = "live_external_hidden_task"
REQUIRED_LIVE_CONDITIONS = (
    "full_discovery",
    "baseline_conservative",
    "baseline_literature_only",
    "ablation_no_reflection",
    "ablation_no_literature",
    "ablation_no_parallel",
)
MINIMUM_LIVE_REPETITIONS = 5
RUNNER_EXECUTION_KEY = "__abducer_runner_execution__"
VERIFIER_EXECUTION_KEY = "__abducer_verifier_execution__"

HiddenTaskRunner = Callable[[Mapping[str, Any]], Mapping[str, Any]]
HumanEvidenceVerifier = Callable[[bytes, Mapping[str, Any]], Mapping[str, Any]]
HUMAN_TRUST_ANCHOR_SCHEMA = "benchmark_human_evidence_trust_anchor.schema.json"


class BenchmarkIntegrityError(ValueError):
    """Raised when benchmark evidence is malformed, leaked, or overstated."""


def _execution_summary(
    raw: Any,
    *,
    role: str,
    request_digest: str | None = None,
    require_index: bool = False,
    validation_context: Any | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Open wrapper-owned process provenance without granting epistemic authority.

    Capture construction can validate the already-published receipt before the
    role index is finalized.  Evaluation requires the complete transitive chain
    through that immutable index.  The import is intentionally lazy because the
    process adapter reuses this module's role constants.
    """

    if not isinstance(raw, Mapping):
        raise BenchmarkIntegrityError("external process execution summary is malformed")
    from .benchmark_process import validate_external_process_summary

    summary = copy.deepcopy(dict(raw))
    receipt = validate_external_process_summary(
        summary,
        role=role,
        request_digest=request_digest,
        require_index=require_index,
        validation_context=validation_context,
    )
    if summary.get("outcome_status") not in {"accepted", "operational_failure", "protocol_failure"}:
        raise BenchmarkIntegrityError("external process execution outcome is untyped")
    if summary.get("epistemic_effect") != "none_process_execution_has_no_epistemic_authority":
        raise BenchmarkIntegrityError("external process execution overstates epistemic authority")
    return summary, receipt


def _canonical_bytes(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _content_digest(payload: Mapping[str, Any]) -> str:
    return _digest_bytes(
        _canonical_bytes({key: value for key, value in payload.items() if key != "content_digest"})
    )


def build_human_evidence_trust_anchor(
    *,
    trust_anchor_id: str,
    authority_id: str,
    benchmark_id: str,
    verifier_command_authority_digest: str,
) -> dict[str, Any]:
    """Build a caller-policy anchor, never an out-of-band external trust root."""

    anchor: dict[str, Any] = {
        "schema_version": 1,
        "trust_anchor_id": trust_anchor_id,
        "authority_id": authority_id,
        "benchmark_id": benchmark_id,
        "verifier_command_authority_digest": verifier_command_authority_digest,
        "trust_boundary": "caller_configured_external_authority_not_evidence_supplied",
        "policy_scope": "caller_policy_eligibility_only",
        "out_of_band_signature_status": "unavailable_no_independent_trust_store",
        "external_authority_eligible": False,
    }
    anchor["content_digest"] = _content_digest(anchor)
    validate_payload(anchor, HUMAN_TRUST_ANCHOR_SCHEMA)
    return anchor


def _validate_human_evidence_trust_anchor(
    raw: Mapping[str, Any], *, benchmark_id: str
) -> dict[str, Any]:
    anchor = copy.deepcopy(dict(raw))
    validate_payload(anchor, HUMAN_TRUST_ANCHOR_SCHEMA)
    if anchor["content_digest"] != _content_digest(anchor):
        raise BenchmarkIntegrityError("human evidence trust anchor digest mismatch")
    if anchor["benchmark_id"] != benchmark_id:
        raise BenchmarkIntegrityError("human evidence trust anchor targets another benchmark")
    return anchor


def _capture_manifest_digest(payload: Mapping[str, Any]) -> str:
    """Bind preregistered generation inputs while allowing post-capture ratings."""

    return _digest_bytes(
        _canonical_bytes(
            {
                key: value
                for key, value in payload.items()
                if key not in {"human_evidence"}
            }
        )
    )


def _load_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BenchmarkIntegrityError(f"cannot read benchmark JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise BenchmarkIntegrityError(f"benchmark JSON must be an object: {path}")
    return payload


def _resolve(root: Path, raw: str, *, must_exist: bool = True) -> Path:
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        raise BenchmarkIntegrityError(f"unsafe benchmark path: {raw}")
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise BenchmarkIntegrityError(f"benchmark path escapes fixture root: {raw}") from exc
    if must_exist and not resolved.is_file():
        raise BenchmarkIntegrityError(f"missing benchmark artifact: {raw}")
    return resolved


def _normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _normalize_latex(value: str) -> str:
    return re.sub(r"[\s{}$\\]+", "", value.lower())


def scan_leakage(text: str, ground_truth: Mapping[str, Any]) -> set[str]:
    """Detect label, LaTeX, dependency, and artifact-presence leakage."""

    channels: set[str] = set()
    normalized = _normalize_text(text)
    latex = _normalize_latex(text)
    labels = [*ground_truth.get("labels", []), *ground_truth.get("aliases", [])]
    if any(
        _normalize_text(str(label))
        and _normalize_text(str(label)) in normalized
        for label in labels
    ):
        channels.add("label")
    if any(
        _normalize_latex(str(expression))
        and _normalize_latex(str(expression)) in latex
        for expression in ground_truth.get("latex_signatures", [])
    ):
        channels.add("latex")
    for edge in ground_truth.get("dependency_edges", []):
        if isinstance(edge, list) and len(edge) == 2:
            left, right = (_normalize_text(str(item)) for item in edge)
            if left and right and left in normalized and right in normalized:
                channels.add("dependency")
    if any(
        str(marker).lower() in text.lower()
        for marker in ground_truth.get("forbidden_artifact_markers", [])
    ):
        channels.add("artifact_presence")
    return channels


def inter_rater_agreement(packet: Mapping[str, Any]) -> float:
    """Return normalized pairwise agreement for a two-condition rubric fixture."""

    ratings = packet.get("ratings", [])
    if not isinstance(ratings, list) or len(ratings) < 2:
        raise BenchmarkIntegrityError("rubric packet requires at least two raters")
    comparisons = 0
    distance = 0.0
    for index, left in enumerate(ratings):
        for right in ratings[index + 1 :]:
            for condition in packet.get("conditions", []):
                left_scores = left.get("scores", {}).get(condition, {})
                right_scores = right.get("scores", {}).get(condition, {})
                for dimension in RUBRIC_DIMENSIONS:
                    a = left_scores.get(dimension)
                    b = right_scores.get(dimension)
                    if (
                        not isinstance(a, int)
                        or not isinstance(b, int)
                        or not (1 <= a <= 5 and 1 <= b <= 5)
                    ):
                        raise BenchmarkIntegrityError(
                            f"invalid rubric score for {condition}/{dimension}"
                        )
                    comparisons += 1
                    distance += abs(a - b) / 4.0
    return round(1.0 - distance / comparisons, 6) if comparisons else 0.0


def _validate_synthetic_rubric(packet: Mapping[str, Any]) -> float:
    if packet.get("condition_labels_hidden") is not True or not packet.get("randomization_seed"):
        raise BenchmarkIntegrityError("synthetic rubric comparison must model blinding")
    if set(packet.get("conditions", [])) != {"A", "B"}:
        raise BenchmarkIntegrityError("synthetic rubric must expose anonymous A/B conditions")
    if not packet.get("adjudication"):
        raise BenchmarkIntegrityError("synthetic rubric requires an adjudication policy")
    agreement = inter_rater_agreement(packet)
    if agreement < float(packet.get("minimum_agreement", 0.70)):
        raise BenchmarkIntegrityError(
            f"synthetic rubric agreement below fixture threshold: {agreement}"
        )
    return agreement


def _validate_time_slice(packet: Mapping[str, Any]) -> None:
    time_slice = packet.get("time_slice", {})
    try:
        cutoff = dt.date.fromisoformat(str(time_slice.get("cutoff")))
        for source in time_slice.get("pre_cutoff_sources", []):
            if dt.date.fromisoformat(source["publication_date"]) > cutoff:
                raise BenchmarkIntegrityError("future source leaked into pre-cutoff context")
        later_sources = time_slice.get("withheld_later_sources", [])
        if not later_sources or any(
            dt.date.fromisoformat(source["publication_date"]) <= cutoff
            for source in later_sources
        ):
            raise BenchmarkIntegrityError("time-sliced case needs genuinely later sources")
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, BenchmarkIntegrityError):
            raise
        raise BenchmarkIntegrityError(f"invalid time-slice metadata: {exc}") from exc
    rebase = packet.get("candidate_output", {}).get("later_snapshot_rebase", {})
    if not rebase.get("source_ids") or rebase.get("action") not in {
        "absorb", "reframe", "merge", "split", "retire", "new_question"
    }:
        raise BenchmarkIntegrityError("candidate did not causally assimilate later snapshot")


def _validate_portfolios(packet: Mapping[str, Any]) -> dict[str, float]:
    aggressive = packet.get("aggressive_portfolio", {})
    conservative = packet.get("conservative_baseline", {})
    if aggressive.get("resource_budget") != conservative.get("resource_budget"):
        raise BenchmarkIntegrityError("aggressive and conservative portfolios need matched budgets")
    items = aggressive.get("hypotheses", [])
    corners = {
        item.get("corner_family") for item in items if item.get("target_relevance") is True
    }
    if len(corners) < 6:
        raise BenchmarkIntegrityError("aggressive portfolio lacks six relevant corners")
    for item in items:
        required = (
            item.get("mechanism"),
            item.get("value_if_right"),
            item.get("learning_if_wrong"),
            item.get("correction_condition"),
        )
        if item.get("selected") and (
            item.get("target_relevance") is not True or not all(required)
        ):
            raise BenchmarkIntegrityError("low plausibility or shock alone counted as creativity")
    conservative_mechanisms = {
        item.get("mechanism") for item in conservative.get("hypotheses", [])
    }
    return {
        "aggressive_corner_diversity": min(1.0, len(corners) / 8.0),
        "conservative_mechanism_diversity": min(
            1.0, len(conservative_mechanisms) / 8.0
        ),
    }


def _validate_common_manifest(manifest: Mapping[str, Any]) -> tuple[list[Mapping[str, Any]], list[str]]:
    authorship = manifest.get("ground_truth_authorship", {})
    if (
        authorship.get("independent_of_system") is not True
        or not authorship.get("author_id")
        or authorship.get("author_id") == "abducer-runtime"
    ):
        raise BenchmarkIntegrityError("ground truth lacks independent provenance")
    tuning = manifest.get("configuration_provenance", {})
    if (
        set(tuning.get("selected_from_splits", [])) - {"train", "development"}
        or tuning.get("frozen_scores_observed") is not False
    ):
        raise BenchmarkIntegrityError("configuration selection observed frozen evidence")
    cases = manifest.get("cases", manifest.get("tasks", []))
    if not isinstance(cases, list) or not cases:
        raise BenchmarkIntegrityError("benchmark manifest has no cases/tasks")
    minimum_domains = int(manifest.get("minimum_domains", 3))
    domains = [str(case.get("domain") or "") for case in cases]
    if (
        len(cases) < minimum_domains
        or any(not domain for domain in domains)
        or len(set(domains)) != len(domains)
    ):
        raise BenchmarkIntegrityError("cases must cover disjoint domain-level splits")
    return cases, domains


def _score_synthetic_case(
    case_id: str,
    working_text: str,
    truth: Mapping[str, Any],
    packet: Mapping[str, Any],
) -> dict[str, Any]:
    if scan_leakage(working_text, truth):
        raise BenchmarkIntegrityError(f"{case_id}: frozen truth leaks into working KB")
    output = packet.get("candidate_output", {})
    generation_inputs = json.dumps(output.get("generation_inputs", []), sort_keys=True).lower()
    forbidden = [
        *truth.get("labels", []),
        *truth.get("aliases", []),
        *truth.get("forbidden_artifact_markers", []),
    ]
    if any(str(item).lower() in generation_inputs for item in forbidden):
        raise BenchmarkIntegrityError(f"{case_id}: generation inputs expose frozen truth")
    if output.get("output_closed_before_truth_load") is not True:
        raise BenchmarkIntegrityError(f"{case_id}: output did not close before truth load")
    expected = truth.get("expected", {})
    transformations = set(output.get("conceptual_transformation_ids", []))
    expected_transforms = set(expected.get("conceptual_transformation_ids", []))
    conceptual = len(transformations & expected_transforms) / max(1, len(expected_transforms))
    understanding = 1.0 if (
        output.get("understanding_delta", {}).get("before")
        != output.get("understanding_delta", {}).get("after")
        and output.get("understanding_delta", {}).get("new_distinctions")
    ) else 0.0
    _validate_time_slice(packet)
    portfolio = _validate_portfolios(packet)
    synthetic_agreement = _validate_synthetic_rubric(packet.get("expert_packet", {}))
    return {
        "case_id": case_id,
        "domain": packet["domain"],
        "protocol_valid": True,
        "synthetic_protocol_metrics": {
            "route_reconstruction": round(float(output.get("route_reconstruction", 0.0)), 6),
            "conceptual_transformation": round(conceptual, 6),
            "understanding_shape": round(understanding, 6),
            "synthetic_rubric_agreement": synthetic_agreement,
            **portfolio,
        },
        "human_rating_status": "not_human_synthetic_fixture",
        "efficacy_authorized": False,
    }


def _evaluate_synthetic_manifest(path: Path, manifest: Mapping[str, Any]) -> dict[str, Any]:
    if manifest.get("schema_version") != "1.0.0" or manifest.get("split") != "frozen":
        raise BenchmarkIntegrityError("synthetic manifest must be version 1.0.0/frozen")
    cases, domains = _validate_common_manifest(manifest)
    root = path.parent
    rows: list[dict[str, Any]] = []
    for case in cases:
        working = _resolve(root, case["working_kb"])
        truth_path = _resolve(root, case["ground_truth"])
        packet_path = _resolve(root, case["case_packet"])
        if truth_path in {working, packet_path}:
            raise BenchmarkIntegrityError("truth must be external to working/candidate packets")
        truth = _load_object(truth_path)
        packet = _load_object(packet_path)
        if packet.get("domain") != case.get("domain") or packet.get("case_id") != case.get("case_id"):
            raise BenchmarkIntegrityError("synthetic case identity mismatch")
        rows.append(
            _score_synthetic_case(
                case["case_id"], working.read_text(encoding="utf-8"), truth, packet
            )
        )
    return {
        "benchmark_id": manifest["benchmark_id"],
        "benchmark_mode": SYNTHETIC_MODE,
        "split": "frozen",
        "case_count": len(rows),
        "domain_count": len(set(domains)),
        "protocol_valid": all(row["protocol_valid"] for row in rows),
        "synthetic_fixture_passed": all(row["protocol_valid"] for row in rows),
        "efficacy_authorized": False,
        "replicated": False,
        "cases": rows,
        "evidence_boundary": (
            "Synthetic packets and synthetic rubric values validate protocol mechanics only. "
            "They are never human ratings and cannot support conceptual-discovery efficacy."
        ),
    }


def _validate_budget(budget: Mapping[str, Any]) -> dict[str, float | int]:
    required = {"tokens", "wall_seconds", "cost_units"}
    if not required.issubset(budget):
        raise BenchmarkIntegrityError("live benchmark budget lacks tokens/wall/cost")
    normalized: dict[str, float | int] = {
        "tokens": int(budget["tokens"]),
        "wall_seconds": float(budget["wall_seconds"]),
        "cost_units": float(budget["cost_units"]),
    }
    if any(float(value) <= 0 for value in normalized.values()):
        raise BenchmarkIntegrityError("live benchmark budgets must be positive")
    return normalized


def _validate_live_manifest(manifest: Mapping[str, Any]) -> tuple[list[Mapping[str, Any]], list[str], tuple[str, ...], int, dict[str, float | int]]:
    if manifest.get("schema_version") != "2.0.0" or manifest.get("split") != "external_hidden":
        raise BenchmarkIntegrityError("live manifest must be version 2.0.0/external_hidden")
    tasks, domains = _validate_common_manifest(manifest)
    conditions = tuple(str(item) for item in manifest.get("conditions", []))
    if set(conditions) != set(REQUIRED_LIVE_CONDITIONS) or len(conditions) != len(set(conditions)):
        raise BenchmarkIntegrityError(
            "live benchmark requires full, conservative/literature baselines, and all ablations"
        )
    repetitions = int(manifest.get("repetitions", 0))
    if repetitions < MINIMUM_LIVE_REPETITIONS:
        raise BenchmarkIntegrityError(
            f"live benchmark requires at least {MINIMUM_LIVE_REPETITIONS} repetitions"
        )
    preregistration = manifest.get("preregistration", {})
    if (
        preregistration.get("registered_before_capture") is not True
        or not preregistration.get("protocol_id")
        or not preregistration.get("analysis_plan_digest")
    ):
        raise BenchmarkIntegrityError("live benchmark lacks preregistration provenance")
    return tasks, domains, conditions, repetitions, _validate_budget(manifest.get("resource_budget", {}))


def capture_live_hidden_task_outputs(
    manifest_path: Path,
    runner: HiddenTaskRunner,
    *,
    output_path: Path | None = None,
) -> dict[str, Any]:
    """Run the condition×task×repetition matrix without loading ground truth.

    The runner receives only parsed task bytes, condition/ablation identity, and
    the preregistered opportunity budget. Ground-truth paths are never included
    in the runner request or capture packet.
    """

    manifest_path = Path(manifest_path).resolve()
    manifest = _load_object(manifest_path)
    if manifest.get("benchmark_mode") != LIVE_MODE:
        raise BenchmarkIntegrityError("output capture is only available for live manifests")
    tasks, _domains, conditions, repetitions, budget = _validate_live_manifest(manifest)
    root = manifest_path.parent
    configured_output = _resolve(
        root, str(manifest.get("output_capture") or ""), must_exist=False
    )
    destination = Path(output_path).resolve() if output_path is not None else configured_output
    if destination != configured_output:
        raise BenchmarkIntegrityError("capture output must match the preregistered manifest path")

    task_payloads: dict[str, tuple[bytes, Any, str]] = {}
    for task in tasks:
        case_id = str(task.get("case_id") or "")
        task_path = _resolve(root, str(task.get("task_packet") or ""))
        raw = task_path.read_bytes()
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise BenchmarkIntegrityError(f"hidden task {case_id} is not JSON: {exc}") from exc
        task_payloads[case_id] = (raw, parsed, str(task["task_packet"]))

    schedule = [
        (str(task["case_id"]), str(task["domain"]), repetition, condition)
        for task in tasks
        for repetition in range(1, repetitions + 1)
        for condition in conditions
    ]
    randomization_seed = str(manifest.get("condition_randomization_seed") or "")
    if not randomization_seed:
        raise BenchmarkIntegrityError("live capture requires a frozen randomization seed")
    random.Random(f"{manifest['benchmark_id']}:{randomization_seed}").shuffle(schedule)

    outputs: list[dict[str, Any]] = []
    for order, (case_id, domain, repetition, condition) in enumerate(schedule, start=1):
        task_raw, task_payload, task_ref = task_payloads[case_id]
        request = {
            "benchmark_id": manifest["benchmark_id"],
            "case_id": case_id,
            "domain": domain,
            "condition": condition,
            "repetition": repetition,
            "task_packet": copy.deepcopy(task_payload),
            "task_packet_digest": _digest_bytes(task_raw),
            "resource_budget": copy.deepcopy(budget),
            "forbidden_generation_input_classes": [
                "withheld evaluator evidence",
                "withheld labels",
                "other condition outputs",
                "human ratings",
            ],
        }
        raw_result = runner(copy.deepcopy(request))
        if not isinstance(raw_result, Mapping):
            raise BenchmarkIntegrityError("hidden-task runner returned a non-object")
        raw_result = copy.deepcopy(dict(raw_result))
        execution_raw = raw_result.pop(RUNNER_EXECUTION_KEY, None)
        execution = None
        if execution_raw is not None:
            execution, _receipt = _execution_summary(
                execution_raw,
                role="benchmark_runner",
                request_digest=_digest_bytes(_canonical_bytes(request) + b"\n"),
            )
            if execution["outcome_status"] != "accepted":
                raise BenchmarkIntegrityError("failed external process cannot supply a candidate")
        candidate = raw_result.get("candidate_output")
        if candidate in (None, "", [], {}):
            raise BenchmarkIntegrityError("hidden-task runner returned an empty output")
        usage = raw_result.get("resource_usage", {})
        if not isinstance(usage, Mapping):
            raise BenchmarkIntegrityError("hidden-task resource usage must be an object")
        normalized_usage = {
            "tokens": int(usage.get("tokens", 0)),
            "wall_seconds": float(usage.get("wall_seconds", 0.0)),
            "cost_units": float(usage.get("cost_units", 0.0)),
        }
        if any(normalized_usage[key] < 0 or normalized_usage[key] > float(budget[key]) for key in budget):
            raise BenchmarkIntegrityError("hidden-task runner exceeded its matched budget")
        generation_refs = list(raw_result.get("generation_input_refs", [task_ref]))
        if generation_refs != [task_ref]:
            raise BenchmarkIntegrityError("live output used inputs beyond its hidden task packet")
        candidate_bytes = _canonical_bytes({"candidate_output": candidate})
        output_row = {
                "output_id": _digest_bytes(
                    _canonical_bytes(
                        {
                            "benchmark_id": manifest["benchmark_id"],
                            "case_id": case_id,
                            "condition": condition,
                            "repetition": repetition,
                            "candidate_digest": _digest_bytes(candidate_bytes),
                        }
                    )
                ),
                "execution_order": order,
                "case_id": case_id,
                "domain": domain,
                "condition": condition,
                "repetition": repetition,
                "task_packet_ref": task_ref,
                "task_packet_digest": _digest_bytes(task_raw),
                "allocated_budget": copy.deepcopy(budget),
                "resource_usage": normalized_usage,
                "generation_input_refs": generation_refs,
                "candidate_output": copy.deepcopy(candidate),
                "candidate_output_digest": _digest_bytes(candidate_bytes),
                "output_closed_before_truth_load": True,
            }
        output_row["execution_mode"] = (
            "governed_external_process" if execution is not None else "in_process_runner"
        )
        if execution is not None:
            output_row["external_process_execution"] = execution
            output_row["isolation_status"] = execution["isolation_status"]
            output_row["external_efficacy_eligible"] = execution[
                "external_efficacy_eligible"
            ]
        else:
            output_row["isolation_status"] = "in_process_unattested"
            output_row["external_efficacy_eligible"] = False
        outputs.append(output_row)
    capture: dict[str, Any] = {
        "schema_version": "1.0.0",
        "capture_id": _digest_bytes(
            _canonical_bytes(
                {
                    "benchmark_id": manifest["benchmark_id"],
                    "manifest_digest": _capture_manifest_digest(manifest),
                    "schedule": schedule,
                }
            )
        ),
        "benchmark_id": manifest["benchmark_id"],
        "manifest_digest": _capture_manifest_digest(manifest),
        "benchmark_mode": LIVE_MODE,
        "condition_order_randomized": True,
        "truth_loaded_during_capture": False,
        "capture_closed": True,
        "conditions": list(conditions),
        "repetitions": repetitions,
        "resource_budget_per_output": copy.deepcopy(budget),
        "execution_authority_boundary": (
            "A transitive receipt/index chain authenticates local process execution only. "
            "The current adapter has no deny-by-construction host isolation, so neither "
            "governed local nor in-process rows establish hiddenness or external efficacy."
        ),
        "outputs": outputs,
    }
    capture["content_digest"] = _content_digest(capture)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(_canonical_bytes(capture) + b"\n")
    return capture


def _load_descriptor_bytes(root: Path, descriptor: Mapping[str, Any]) -> bytes:
    artifact_ref = str(descriptor.get("artifact_ref") or "")
    path = _resolve(root, artifact_ref)
    raw = path.read_bytes()
    expected_digest = str(descriptor.get("sha256") or "")
    expected_length = descriptor.get("byte_length")
    if (
        descriptor.get("media_type") != "application/json"
        or not re.fullmatch(r"sha256:[a-f0-9]{64}", expected_digest)
        or isinstance(expected_length, bool)
        or not isinstance(expected_length, int)
        or expected_length <= 0
    ):
        raise BenchmarkIntegrityError("external evidence descriptor is incomplete")
    if _digest_bytes(raw) != expected_digest or len(raw) != expected_length:
        raise BenchmarkIntegrityError("external evidence bytes differ from descriptor")
    return raw


def _validate_capture(
    root: Path,
    manifest: Mapping[str, Any],
    tasks: Sequence[Mapping[str, Any]],
    conditions: Sequence[str],
    repetitions: int,
    budget: Mapping[str, float | int],
    validation_context: Any | None = None,
) -> tuple[dict[str, Any], dict[str, Mapping[str, Any]]]:
    capture_path = _resolve(root, str(manifest.get("output_capture") or ""))
    capture = _load_object(capture_path)
    if (
        capture.get("benchmark_id") != manifest.get("benchmark_id")
        or capture.get("manifest_digest") != _capture_manifest_digest(manifest)
        or capture.get("benchmark_mode") != LIVE_MODE
        or capture.get("truth_loaded_during_capture") is not False
        or capture.get("capture_closed") is not True
        or capture.get("condition_order_randomized") is not True
        or capture.get("content_digest") != _content_digest(capture)
    ):
        raise BenchmarkIntegrityError("live capture identity/closure digest is invalid")
    outputs = capture.get("outputs", [])
    expected_keys = {
        (str(task["case_id"]), condition, repetition)
        for task in tasks
        for condition in conditions
        for repetition in range(1, repetitions + 1)
    }
    actual_keys = {
        (str(row.get("case_id")), str(row.get("condition")), int(row.get("repetition", 0)))
        for row in outputs
        if isinstance(row, Mapping)
    }
    if actual_keys != expected_keys or len(outputs) != len(expected_keys):
        raise BenchmarkIntegrityError("live capture lacks the exact condition/repetition matrix")
    by_id: dict[str, Mapping[str, Any]] = {}
    tasks_by_id = {str(item["case_id"]): item for item in tasks}
    for row in outputs:
        output_id = str(row.get("output_id") or "")
        if not output_id or output_id in by_id:
            raise BenchmarkIntegrityError("live capture output IDs must be unique")
        task = tasks_by_id[str(row["case_id"])]
        task_path = _resolve(root, str(task["task_packet"]))
        task_raw = task_path.read_bytes()
        if (
            row.get("task_packet_ref") != task["task_packet"]
            or row.get("task_packet_digest") != _digest_bytes(task_raw)
            or row.get("generation_input_refs") != [task["task_packet"]]
            or row.get("allocated_budget") != budget
            or row.get("output_closed_before_truth_load") is not True
        ):
            raise BenchmarkIntegrityError("live output is not bound to its exact hidden input/budget")
        usage = row.get("resource_usage", {})
        if any(
            float(usage.get(key, -1)) < 0
            or float(usage.get(key, -1)) > float(budget[key])
            for key in budget
        ):
            raise BenchmarkIntegrityError("live output exceeded its opportunity budget")
        expected_candidate_digest = _digest_bytes(
            _canonical_bytes({"candidate_output": row.get("candidate_output")})
        )
        if row.get("candidate_output_digest") != expected_candidate_digest:
            raise BenchmarkIntegrityError("captured candidate output digest mismatch")
        execution_mode = row.get("execution_mode")
        execution_raw = row.get("external_process_execution")
        if execution_mode == "in_process_runner":
            if execution_raw is not None:
                raise BenchmarkIntegrityError("in-process capture row claims external execution")
            if (
                row.get("isolation_status") != "in_process_unattested"
                or row.get("external_efficacy_eligible") is not False
            ):
                raise BenchmarkIntegrityError("in-process isolation boundary is misstated")
        elif execution_mode == "governed_external_process":
            try:
                task_payload = json.loads(task_raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise BenchmarkIntegrityError(f"hidden task bytes changed shape: {exc}") from exc
            request = {
                "benchmark_id": manifest["benchmark_id"],
                "case_id": str(row["case_id"]),
                "domain": str(row["domain"]),
                "condition": str(row["condition"]),
                "repetition": int(row["repetition"]),
                "task_packet": task_payload,
                "task_packet_digest": _digest_bytes(task_raw),
                "resource_budget": copy.deepcopy(budget),
                "forbidden_generation_input_classes": [
                    "withheld evaluator evidence",
                    "withheld labels",
                    "other condition outputs",
                    "human ratings",
                ],
            }
            _summary, receipt = _execution_summary(
                execution_raw,
                role="benchmark_runner",
                request_digest=_digest_bytes(_canonical_bytes(request) + b"\n"),
                require_index=True,
                validation_context=validation_context,
            )
            if (
                _summary.get("isolation_status") != "unisolated_protocol_only"
                or _summary.get("external_efficacy_eligible") is not False
                or row.get("isolation_status") != _summary["isolation_status"]
                or row.get("external_efficacy_eligible") is not False
            ):
                raise BenchmarkIntegrityError(
                    "local governed runner overstates deny-by-construction isolation"
                )
            response = receipt.get("response_payload")
            if not isinstance(response, Mapping) or set(response) != {
                "candidate_output", "resource_usage", "generation_input_refs"
            }:
                raise BenchmarkIntegrityError("governed runner response projection is not exact")
            response_usage = response["resource_usage"]
            if not isinstance(response_usage, Mapping):
                raise BenchmarkIntegrityError("governed runner response usage is malformed")
            normalized_response_usage = {
                "tokens": int(response_usage.get("tokens", 0)),
                "wall_seconds": float(response_usage.get("wall_seconds", 0.0)),
                "cost_units": float(response_usage.get("cost_units", 0.0)),
            }
            if (
                response["candidate_output"] != row.get("candidate_output")
                or normalized_response_usage != row.get("resource_usage")
                or response["generation_input_refs"] != row.get("generation_input_refs")
            ):
                raise BenchmarkIntegrityError("capture row differs from its governed response receipt")
        else:
            raise BenchmarkIntegrityError("live output execution mode is missing or unknown")
        by_id[output_id] = row
    return capture, by_id


def _automatic_live_metrics(
    root: Path,
    tasks: Sequence[Mapping[str, Any]],
    outputs: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    task_metrics: dict[str, dict[str, list[float]]] = {}
    for task in tasks:
        case_id = str(task["case_id"])
        task_raw = _resolve(root, str(task["task_packet"])).read_text(encoding="utf-8")
        truth = _load_object(_resolve(root, str(task["ground_truth"])))
        if scan_leakage(task_raw, truth):
            raise BenchmarkIntegrityError(f"{case_id}: truth leaked into hidden task packet")
        expected = set(truth.get("expected", {}).get("conceptual_transformation_ids", []))
        task_metrics[case_id] = {}
        for row in outputs.values():
            if row["case_id"] != case_id:
                continue
            candidate = row.get("candidate_output", {})
            transforms = set(
                candidate.get("conceptual_transformation_ids", [])
                if isinstance(candidate, Mapping)
                else []
            )
            score = len(expected & transforms) / max(1, len(expected))
            task_metrics[case_id].setdefault(str(row["condition"]), []).append(score)
    return {
        case_id: {
            condition: round(statistics.fmean(values), 6)
            for condition, values in sorted(by_condition.items())
        }
        for case_id, by_condition in sorted(task_metrics.items())
    }


def _score_vector(scores: Mapping[str, Any]) -> float:
    values: list[float] = []
    for dimension in RUBRIC_DIMENSIONS:
        value = scores.get(dimension)
        if not isinstance(value, int) or not 1 <= value <= 5:
            raise BenchmarkIntegrityError(f"invalid authenticated human score: {dimension}")
        values.append(value / 5.0)
    return statistics.fmean(values)


def _validate_authenticated_ratings(
    packet: Mapping[str, Any],
    capture: Mapping[str, Any],
    outputs: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, float], float]:
    if (
        packet.get("schema_version") != "1.0.0"
        or packet.get("benchmark_id") != capture.get("benchmark_id")
        or packet.get("capture_digest") != capture.get("content_digest")
        or packet.get("condition_labels_hidden") is not True
        or not packet.get("adjudication_policy")
    ):
        raise BenchmarkIntegrityError("authenticated human packet identity/blinding is invalid")
    minimum_raters = int(packet.get("minimum_raters_per_output", 2))
    if minimum_raters < 2:
        raise BenchmarkIntegrityError("human evidence needs at least two raters per output")
    disclosures = {
        str(item.get("rater_id")): item for item in packet.get("rater_disclosures", [])
    }
    if not disclosures or any(
        item.get("independent_of_system") is not True
        or item.get("conflict_disclosed") is not True
        for item in disclosures.values()
    ):
        raise BenchmarkIntegrityError("human raters lack independence/conflict disclosures")
    by_output: dict[str, list[tuple[str, float]]] = {output_id: [] for output_id in outputs}
    seen: set[tuple[str, str]] = set()
    for rating in packet.get("ratings", []):
        output_id = str(rating.get("output_id") or "")
        rater_id = str(rating.get("rater_id") or "")
        if output_id not in outputs or rater_id not in disclosures:
            raise BenchmarkIntegrityError("human rating names unknown output/rater")
        key = (output_id, rater_id)
        if key in seen:
            raise BenchmarkIntegrityError("duplicate human rating for output/rater")
        seen.add(key)
        by_output[output_id].append((rater_id, _score_vector(rating.get("scores", {}))))
    if any(len({rater for rater, _ in rows}) < minimum_raters for rows in by_output.values()):
        raise BenchmarkIntegrityError("not every live output has independent replicated ratings")

    output_means = {
        output_id: statistics.fmean(value for _rater, value in rows)
        for output_id, rows in by_output.items()
    }
    pair_agreements: list[float] = []
    for rows in by_output.values():
        for index, (_left_id, left) in enumerate(rows):
            for _right_id, right in rows[index + 1 :]:
                pair_agreements.append(1.0 - abs(left - right))
    agreement = statistics.fmean(pair_agreements) if pair_agreements else 0.0
    minimum_agreement = float(packet.get("minimum_agreement", 0.70))
    if agreement < minimum_agreement:
        raise BenchmarkIntegrityError(
            f"authenticated human agreement below threshold: {agreement:.6f}"
        )
    return output_means, round(agreement, 6)


def _paired_effect(differences: Sequence[float], full: Sequence[float], control: Sequence[float]) -> dict[str, Any]:
    if len(differences) < MINIMUM_LIVE_REPETITIONS:
        raise BenchmarkIntegrityError("effect estimate lacks repeated paired observations")
    mean_difference = statistics.fmean(differences)
    sample_sd = statistics.stdev(differences) if len(differences) > 1 else 0.0
    standard_error = sample_sd / math.sqrt(len(differences))
    pooled_values = [*full, *control]
    pooled_sd = statistics.stdev(pooled_values) if len(pooled_values) > 1 else 0.0
    standardized_effect = mean_difference / pooled_sd if pooled_sd > 0 else None
    return {
        "n_pairs": len(differences),
        "full_mean": round(statistics.fmean(full), 6),
        "control_mean": round(statistics.fmean(control), 6),
        "mean_difference": round(mean_difference, 6),
        "sample_sd_difference": round(sample_sd, 6),
        "standard_error": round(standard_error, 6),
        "confidence_interval_95": [
            round(mean_difference - 1.96 * standard_error, 6),
            round(mean_difference + 1.96 * standard_error, 6),
        ],
        "standardized_effect_size": (
            None if standardized_effect is None else round(standardized_effect, 6)
        ),
        "positive_pair_fraction": round(
            sum(value > 0 for value in differences) / len(differences), 6
        ),
        "degenerate_variance": pooled_sd == 0,
    }


def _effect_estimates(
    outputs: Mapping[str, Mapping[str, Any]], output_means: Mapping[str, float]
) -> dict[str, dict[str, Any]]:
    by_key = {
        (str(row["case_id"]), int(row["repetition"]), str(row["condition"])): output_means[output_id]
        for output_id, row in outputs.items()
    }
    estimates: dict[str, dict[str, Any]] = {}
    units = sorted({(case_id, repetition) for case_id, repetition, _condition in by_key})
    for comparator in REQUIRED_LIVE_CONDITIONS:
        if comparator == "full_discovery":
            continue
        full = [by_key[(case_id, repetition, "full_discovery")] for case_id, repetition in units]
        control = [by_key[(case_id, repetition, comparator)] for case_id, repetition in units]
        estimates[comparator] = _paired_effect(
            [left - right for left, right in zip(full, control)], full, control
        )
    return estimates


def _positive_effect_gate_status(
    estimates: Mapping[str, Mapping[str, Any]], minimum_effect: float
) -> str:
    """Classify the primary matched baseline without granting claim authority."""

    primary = estimates.get("baseline_conservative")
    if not isinstance(primary, Mapping) or int(primary.get("n_pairs", 0)) < MINIMUM_LIVE_REPETITIONS:
        return "underpowered"
    if (
        primary.get("confidence_interval_95", [0.0])[0] > 0
        and primary.get("standardized_effect_size") is not None
        and float(primary["standardized_effect_size"]) >= minimum_effect
        and primary.get("degenerate_variance") is False
    ):
        return "positive_caller_policy_only"
    return "null_or_negative"


def _replication_gate_status(
    estimates: Mapping[str, Mapping[str, Any]], minimum_effect: float
) -> str:
    """Classify all preregistered comparisons separately from authentication."""

    if not estimates or any(
        int(estimate.get("n_pairs", 0)) < MINIMUM_LIVE_REPETITIONS
        for estimate in estimates.values()
    ):
        return "underpowered"
    if all(
        estimate.get("confidence_interval_95", [0.0])[0] > 0
        and estimate.get("standardized_effect_size") is not None
        and float(estimate["standardized_effect_size"]) >= minimum_effect
        and estimate.get("degenerate_variance") is False
        for estimate in estimates.values()
    ):
        return "passed_caller_policy_only"
    return "not_replicated"


def _evaluate_live_manifest_with_context(
    path: Path,
    manifest: Mapping[str, Any],
    human_evidence_verifier: HumanEvidenceVerifier | None,
    human_evidence_trust_anchor: Mapping[str, Any] | None,
    validation_context: Any,
) -> dict[str, Any]:
    tasks, domains, conditions, repetitions, budget = _validate_live_manifest(manifest)
    root = path.parent
    capture, outputs = _validate_capture(
        root,
        manifest,
        tasks,
        conditions,
        repetitions,
        budget,
        validation_context=validation_context,
    )
    automatic = _automatic_live_metrics(root, tasks, outputs)
    base_report: dict[str, Any] = {
        "benchmark_id": manifest["benchmark_id"],
        "benchmark_mode": LIVE_MODE,
        "split": "external_hidden",
        "case_count": len(tasks),
        "domain_count": len(set(domains)),
        "condition_count": len(conditions),
        "repetitions": repetitions,
        "output_count": len(outputs),
        "capture_digest": capture["content_digest"],
        "matched_opportunity_budget": budget,
        "capture_execution_modes": sorted(
            {str(row.get("execution_mode")) for row in outputs.values()}
        ),
        "governed_process_capture": bool(outputs)
        and all(
            row.get("execution_mode") == "governed_external_process"
            for row in outputs.values()
        ),
        "externally_governed_capture": False,
        "capture_isolation_status": (
            "local_subprocess_protocol_only"
            if outputs
            and all(
                row.get("execution_mode") == "governed_external_process"
                and row.get("isolation_status") == "unisolated_protocol_only"
                for row in outputs.values()
            )
            else "in_process_or_mixed_unattested"
        ),
        "protocol_valid": True,
        "automatic_heldout_diagnostics": automatic,
        "effect_estimates": {},
        "human_evidence": {"status": "absent"},
        "authentication_verified": False,
        "caller_policy_eligible": False,
        "external_authority_eligible": False,
        "positive_efficacy_gate_status": "not_evaluated",
        "replication_gate_status": "not_evaluated",
        "efficacy_authorized": False,
        "replicated": False,
        "evidence_boundary": (
            "Automatic diagnostics and local process authentication are secondary. "
            "External efficacy additionally requires deny-by-construction task isolation "
            "and an out-of-band signed authority; both are unavailable locally."
        ),
    }
    descriptor = manifest.get("human_evidence")
    if not isinstance(descriptor, Mapping):
        return base_report
    if human_evidence_verifier is None:
        base_report["human_evidence"] = {
            "status": "verifier_absent",
            "artifact_ref": descriptor.get("artifact_ref"),
        }
        return base_report
    if human_evidence_trust_anchor is None:
        base_report["human_evidence"] = {
            "status": "trust_anchor_absent",
            "artifact_ref": descriptor.get("artifact_ref"),
        }
        return base_report
    anchor = _validate_human_evidence_trust_anchor(
        human_evidence_trust_anchor, benchmark_id=str(manifest["benchmark_id"])
    )

    raw = _load_descriptor_bytes(root, descriptor)
    verification = human_evidence_verifier(raw, copy.deepcopy(dict(descriptor)))
    if not isinstance(verification, Mapping):
        base_report["human_evidence"] = {"status": "authentication_rejected"}
        return base_report
    verification = copy.deepcopy(dict(verification))
    execution_raw = verification.pop(VERIFIER_EXECUTION_KEY, None)
    if execution_raw is None:
        base_report["human_evidence"] = {
            "status": "verifier_execution_unavailable",
            "trust_anchor_id": anchor["trust_anchor_id"],
        }
        return base_report
    execution, receipt = _execution_summary(
        execution_raw,
        role="human_evidence_verifier",
        require_index=True,
        validation_context=validation_context,
    )
    if execution["outcome_status"] != "accepted":
        base_report["human_evidence"] = {"status": "verifier_operational_failure", "execution": execution, "epistemic_effect": "none_operational_outcome_only"}
        base_report["operationally_complete"] = False
        return base_report
    try:
        verifier_request_digest = _digest_bytes(
            _canonical_bytes(
                {
                    "descriptor": copy.deepcopy(dict(descriptor)),
                    "artifact_utf8": raw.decode("utf-8", errors="strict"),
                }
            )
            + b"\n"
        )
    except UnicodeDecodeError as exc:
        raise BenchmarkIntegrityError(
            "accepted human verifier execution used non-UTF-8 evidence"
        ) from exc
    if execution["request_digest"] != verifier_request_digest:
        raise BenchmarkIntegrityError("human verifier receipt targets another request")
    governed_response = receipt.get("response_payload")
    if not isinstance(governed_response, Mapping) or verification != governed_response:
        raise BenchmarkIntegrityError(
            "human verifier callback differs from its governed response receipt"
        )
    if (
        anchor["verifier_command_authority_digest"]
        != execution["command_authority_digest"]
        or anchor["authority_id"] != descriptor.get("authority_id")
    ):
        base_report["human_evidence"] = {
            "status": "trust_anchor_mismatch",
            "execution": execution,
            "trust_anchor_id": anchor["trust_anchor_id"],
        }
        return base_report
    if not all(
        verification.get(key) is True
        for key in (
            "authenticated",
            "blinding_verified",
            "independent_raters_verified",
            "ratings_immutable",
        )
    ):
        base_report["human_evidence"] = {"status": "authentication_rejected"}
        base_report["human_evidence"]["execution"] = execution
        return base_report
    if (
        verification.get("artifact_sha256") != _digest_bytes(raw)
        or verification.get("authority_id") != anchor["authority_id"]
        or not anchor["authority_id"]
    ):
        base_report["human_evidence"] = {"status": "authentication_identity_mismatch"}
        return base_report
    try:
        ratings = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BenchmarkIntegrityError(f"authenticated rating artifact is invalid JSON: {exc}") from exc
    if not isinstance(ratings, dict):
        raise BenchmarkIntegrityError("authenticated rating artifact must be an object")
    output_means, agreement = _validate_authenticated_ratings(ratings, capture, outputs)
    estimates = _effect_estimates(outputs, output_means)
    minimum_effect = float(manifest.get("minimum_standardized_effect", 0.30))
    positive_status = _positive_effect_gate_status(estimates, minimum_effect)
    replication_status = _replication_gate_status(estimates, minimum_effect)
    base_report.update(
        {
            "effect_estimates": estimates,
            "human_evidence": {
                "status": "authenticated_protocol_only",
                "authority_id": descriptor["authority_id"],
                "trust_anchor_id": anchor["trust_anchor_id"],
                "trust_anchor_digest": anchor["content_digest"],
                "artifact_sha256": _digest_bytes(raw),
                "inter_rater_agreement": agreement,
                "minimum_standardized_effect": minimum_effect,
                "execution": execution,
                "authority_boundary": (
                    "The governed verifier authenticates bytes under caller policy. "
                    "Its local subprocess and caller-minted anchor are not an external trust root."
                ),
            },
            "authentication_verified": True,
            "caller_policy_eligible": True,
            "external_authority_eligible": False,
            "positive_efficacy_gate_status": positive_status,
            "replication_gate_status": replication_status,
            "efficacy_authorized": False,
            "replicated": False,
        }
    )
    return base_report


def _evaluate_live_manifest(
    path: Path,
    manifest: Mapping[str, Any],
    human_evidence_verifier: HumanEvidenceVerifier | None,
    human_evidence_trust_anchor: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Evaluate once and close every cached authority with a final drift sweep."""

    from .benchmark_process import ExternalProcessValidationContext

    validation_context = ExternalProcessValidationContext()
    try:
        return _evaluate_live_manifest_with_context(
            path,
            manifest,
            human_evidence_verifier,
            human_evidence_trust_anchor,
            validation_context,
        )
    finally:
        validation_context.assert_unchanged()


def evaluate_benchmark_manifest(
    path: Path,
    *,
    human_evidence_verifier: HumanEvidenceVerifier | None = None,
    human_evidence_trust_anchor: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate a synthetic protocol fixture or a live external benchmark."""

    path = Path(path).resolve()
    manifest = _load_object(path)
    mode = manifest.get("benchmark_mode")
    if mode == SYNTHETIC_MODE:
        if human_evidence_verifier is not None or human_evidence_trust_anchor is not None:
            raise BenchmarkIntegrityError("synthetic fixtures cannot accept human authority")
        return _evaluate_synthetic_manifest(path, manifest)
    if mode == LIVE_MODE:
        return _evaluate_live_manifest(
            path,
            manifest,
            human_evidence_verifier,
            human_evidence_trust_anchor,
        )
    raise BenchmarkIntegrityError(
        "benchmark_mode must explicitly distinguish synthetic fixtures from live evidence"
    )


__all__ = [
    "BenchmarkIntegrityError",
    "HumanEvidenceVerifier",
    "LIVE_MODE",
    "MINIMUM_LIVE_REPETITIONS",
    "REQUIRED_LIVE_CONDITIONS",
    "RUBRIC_DIMENSIONS",
    "RUNNER_EXECUTION_KEY",
    "SYNTHETIC_MODE",
    "VERIFIER_EXECUTION_KEY",
    "build_human_evidence_trust_anchor",
    "capture_live_hidden_task_outputs",
    "evaluate_benchmark_manifest",
    "inter_rater_agreement",
    "scan_leakage",
]
