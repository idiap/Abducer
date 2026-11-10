# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Executed matched-budget evaluation for category/HoTT discovery lenses.

The module is a narrow adapter over :mod:`agentic.discovery.parallel`.  It does
not invent a second scheduler or reducer.  Thirty cells (five conditions by six
repetitions) enter the existing isolated-process runtime, one deliberately
fails, and every surviving output is sealed before a condition-blind structural
rubric is applied.  Scores are reproducible diagnostics of obligation-bearing
structure; they are explicitly not truth, novelty, depth, or human-preference
judgments.
"""

from __future__ import annotations

import copy
import datetime as dt
import re
from collections import defaultdict
from typing import Any, Mapping, Sequence

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    validate_instance,
)
from agentic.discovery.hypotheses import validate_high_risk_portfolio
from agentic.discovery.literature import (
    resolve_present_literature_freshness,
    validate_assimilation,
    validate_snapshot,
)
from agentic.discovery.parallel import (
    build_parallel_manifest,
    run_parallel_hypothesis_portfolio,
    validate_parallel_portfolio,
)
from skills.common.abstraction_formal_reasoning import (
    FormalReasoningError,
    callable_digest,
    run_condition_forger,
    validate_condition_forger_result,
)
from skills.common.formal_dependency_authority import (
    FormalDependencyAuthorityError,
    _FormalDependencyRunContext,
    _build_formal_dependency_run_context,
    _validate_formal_dependency_run_context,
)


ARMS = ("categorical", "hott", "combined", "incumbent", "no_abstraction")
SCORE_FIELDS = (
    "burden_closure",
    "obstruction_localization",
    "consequence_yield",
    "unification_without_erasure",
    "correction_specificity",
)
RUBRIC = {
    "burden_closure": ("typed_obligations", "localized"),
    "obstruction_localization": ("witness_checks", "certificate_bound"),
    "consequence_yield": ("consequences", "derived_from_obligation"),
    "unification_without_erasure": ("unification_links", "preserves_difference"),
    "correction_specificity": ("correction_tests", "discriminating"),
}
RUBRIC_DIGEST = canonical_digest(RUBRIC)
MINIMUM_MATCHED_REPETITIONS = 5
PRECOMMITTED_FAILURE_STATUSES = frozenset({"failed", "timeout", "invalid"})
CELL_WALL_SECONDS = 60.0
AUTHORITY_BOUNDARY = (
    "Internal condition-blind protocol calibration of sealed outputs only. "
    "It estimates comparative obligation-bearing utility under this fixture "
    "rubric and does not establish truth, novelty, philosophical depth, a "
    "universal property, a physics theorem, discovery efficacy, or human preference."
)


class AbstractionEvaluationError(ValueError):
    """Raised when execution evidence is incomplete, altered, or self-attested.

    Post-runtime retention failures carry their immutable operational evidence
    on ``failure_evidence`` so a hard calibration stop does not erase which
    siblings completed or why an arm fell below the five-cell floor.
    """

    def __init__(
        self,
        message: str,
        *,
        failure_evidence: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.failure_evidence = (
            None
            if failure_evidence is None
            else copy.deepcopy(dict(failure_evidence))
        )


def _fail(
    message: str,
    *,
    failure_evidence: Mapping[str, Any] | None = None,
) -> None:
    raise AbstractionEvaluationError(message, failure_evidence=failure_evidence)


def _without(payload: Mapping[str, Any], *keys: str) -> dict[str, Any]:
    result = copy.deepcopy(dict(payload))
    for key in keys:
        result.pop(key, None)
    return result


def _mean(values: Sequence[float]) -> float:
    return round(sum(values) / len(values), 6)


def _repeatability(values: Sequence[float]) -> dict[str, Any]:
    """Describe deterministic same-task reruns without population inference.

    These executions reuse sealed tasks and authored deterministic operators.
    They are neither independent draws nor a sample from a task population, so
    a confidence interval would be pseudoreplication.  The diagnostic exposes
    exact run-to-run stability and nothing more.
    """

    if not values:
        _fail("repeatability diagnostic requires at least one execution")
    normalized = [round(float(value), 6) for value in values]
    unique = sorted(set(normalized))
    minimum = min(normalized)
    maximum = max(normalized)
    return {
        "descriptive_mean": _mean(normalized),
        "minimum": minimum,
        "maximum": maximum,
        "range": round(maximum - minimum, 6),
        "unique_values": unique,
        "n_executions": len(normalized),
        "all_replays_identical": len(unique) == 1,
        "unit": "same_sealed_task_execution",
        "iid_assumption": False,
        "population_inference_authorized": False,
        "method": "deterministic-repeatability-diagnostic",
    }


def _paired_calibration(
    score_rows: Mapping[int, Mapping[str, Any]],
    baseline_rows: Mapping[int, Mapping[str, Any]],
) -> dict[str, Any]:
    """Describe only exact repetition pairs, with a typed evidence floor.

    Partial failures may remove different repetitions from an arm and its
    baseline.  Pairing therefore uses the key intersection rather than assuming
    a complete baseline.  Fewer than five pairs remain useful failure evidence,
    but cannot be promoted into a calibrated effect diagnostic.
    """

    matched = sorted(set(score_rows) & set(baseline_rows))
    sufficient = len(matched) >= MINIMUM_MATCHED_REPETITIONS
    diagnostics = None
    if sufficient:
        diagnostics = {
            field: _repeatability(
                [
                    float(score_rows[repetition][field])
                    - float(baseline_rows[repetition][field])
                    for repetition in matched
                ]
            )
            for field in SCORE_FIELDS
        }
    return {
        "status": (
            "sufficient_internal_calibration"
            if sufficient
            else "insufficient_internal_calibration"
        ),
        "minimum_required_matched_repetitions": MINIMUM_MATCHED_REPETITIONS,
        "n_matched_repetitions": len(matched),
        "matched_repetitions": matched,
        "diagnostics": diagnostics,
        "iid_assumption": False,
        "population_inference_authorized": False,
    }


def _node_count(value: Any) -> int:
    if isinstance(value, Mapping):
        return 1 + sum(_node_count(item) for item in value.values())
    if isinstance(value, list):
        return 1 + sum(_node_count(item) for item in value)
    return 1


def _surface_tokens(value: Any) -> int:
    if isinstance(value, Mapping):
        return sum(_surface_tokens(item) for item in value.values())
    if isinstance(value, list):
        return sum(_surface_tokens(item) for item in value)
    if isinstance(value, str):
        return len(re.findall(r"\S+", value))
    return 0


def blinded_structural_projection(sealed_output: Mapping[str, Any]) -> dict[str, Any]:
    """Remove condition identity and prose before deterministic scoring.

    Only typed, boolean-bearing structural records survive.  Arm names,
    mechanism labels, case labels, prose, and keyword frequency cannot affect a
    score.  This is the executable control against keyword-rich decorative
    outputs and equal-length rhetorical padding.
    """

    delta = sealed_output.get("theory_delta", {})
    evidence = delta.get("evaluation_evidence", {}) if isinstance(delta, Mapping) else {}
    if not isinstance(evidence, Mapping):
        evidence = {}
    projection: dict[str, Any] = {}
    for field, (source_field, required_flag) in RUBRIC.items():
        rows = evidence.get(source_field, [])
        projection[field] = [
            {required_flag: bool(row.get(required_flag, False))}
            for row in rows
            if isinstance(row, Mapping)
        ] if isinstance(rows, list) else []
    return projection


def blinded_structural_score(sealed_output: Mapping[str, Any]) -> dict[str, int]:
    """Score a sealed output from the arm-blind structural projection only."""

    projection = blinded_structural_projection(sealed_output)
    score: dict[str, int] = {}
    for field, (_, required_flag) in RUBRIC.items():
        score[field] = min(
            5,
            sum(1 for row in projection[field] if row.get(required_flag) is True),
        )
    return score


def _case_scorecard(execution: Mapping[str, Any], case: Mapping[str, Any]) -> dict[str, Any]:
    """Project one bundled execution back onto one held-out task cluster."""

    case_id = str(case["case_id"])
    artifact_digests = {
        str(row["artifact_digest"])
        for row in execution.get("artifacts", [])
        if isinstance(row, Mapping) and row.get("case_id") == case_id
    }
    evidence = execution.get("evaluation_evidence", {})
    filtered: dict[str, list[dict[str, Any]]] = {}
    for source_field, _ in RUBRIC.values():
        rows = evidence.get(source_field, []) if isinstance(evidence, Mapping) else []
        selected: list[dict[str, Any]] = []
        for row in rows if isinstance(rows, list) else []:
            if not isinstance(row, Mapping):
                continue
            cited = {
                str(value)
                for key, value in row.items()
                if key == "artifact_digest" or key.endswith("_artifact_digest")
            }
            if cited & artifact_digests:
                selected.append(copy.deepcopy(dict(row)))
        filtered[source_field] = selected
    candidate = {"theory_delta": {"evaluation_evidence": filtered}}
    return {
        "case_id": case_id,
        "case_digest": canonical_digest(case),
        "scorecard": blinded_structural_score(candidate),
    }


def _negative_control_outcomes(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Expose rather than merely embed decorative/restatement/sham outcomes."""

    outcomes: list[dict[str, Any]] = []
    for control in execution.get("negative_controls", []):
        scorecard = blinded_structural_score(control["candidate"])
        zero = not any(scorecard.values())
        outcomes.append(
            {
                "control_id": control["control_id"],
                "control_kind": control["control_kind"],
                "candidate_digest": canonical_digest(control["candidate"]),
                "scorecard": scorecard,
                "zero_score_passed": zero,
                "outcome": (
                    "rejected_zero_structural_credit"
                    if zero
                    else "failed_control_received_structural_credit"
                ),
            }
        )
    return outcomes


def _profile(arm: str, preferred_lens: str) -> dict[str, int]:
    """Generate precommitted calibration structure, never evidence of lens value."""

    if arm == "combined":
        return {field: 5 for field in SCORE_FIELDS}
    if arm == preferred_lens:
        return {
            "burden_closure": 4,
            "obstruction_localization": 5,
            "consequence_yield": 4,
            "unification_without_erasure": 4,
            "correction_specificity": 4,
        }
    if arm in {"categorical", "hott"}:
        return {
            "burden_closure": 2,
            "obstruction_localization": 2,
            "consequence_yield": 2,
            "unification_without_erasure": 2,
            "correction_specificity": 2,
        }
    if arm == "incumbent":
        return {
            "burden_closure": 2,
            "obstruction_localization": 2,
            "consequence_yield": 1,
            "unification_without_erasure": 2,
            "correction_specificity": 2,
        }
    return {
        "burden_closure": 1,
        "obstruction_localization": 1,
        "consequence_yield": 1,
        "unification_without_erasure": 1,
        "correction_specificity": 1,
    }


def _rows(prefix: str, count: int, flag: str, **extra: Any) -> list[dict[str, Any]]:
    return [
        {"evidence_id": f"{prefix}.{index + 1}", flag: True, **extra}
        for index in range(count)
    ]


class _AbstractionCellWorker:
    """Picklable process worker carrying only the frozen cell plan."""

    def __init__(
        self,
        cells: Mapping[str, Mapping[str, Any]],
        fail_branch_ids: Sequence[str],
        dependency_context: _FormalDependencyRunContext,
    ):
        self.cells = copy.deepcopy(dict(cells))
        self.fail_branch_ids = frozenset(str(value) for value in fail_branch_ids)
        self.dependency_context = copy.deepcopy(dependency_context)

    def __call__(self, request: Mapping[str, Any]) -> dict[str, Any]:
        branch_id = str(request["branch_id"])
        if branch_id in self.fail_branch_ids:
            raise RuntimeError("precommitted partial-failure injection")
        cell = self.cells[branch_id]
        arm = str(cell["arm"])
        cases = [dict(case) for case in cell["cases"]]
        execution = run_condition_forger(
            arm,
            cases,
            _dependency_context=self.dependency_context,
        )
        evidence = copy.deepcopy(execution["evaluation_evidence"])
        # Every arm receives the same surface token budget.  This text is kept
        # out of the blinded projection and therefore cannot buy a score.
        surface_form = " ".join(f"surface-token-{index:02d}" for index in range(48))
        supports = arm in {"categorical", "hott", "combined"}
        return {
            "theory_delta": {
                "delta_class": "matched_abstraction_condition",
                "mechanism_key": f"executed-{request['mechanism_key']}",
                "forger_execution": execution,
                "changed_question": (
                    "Across the same sealed held-out suite, which executable formal "
                    "obligations change without weakening any target quantifier?"
                ),
                "new_explanatory_dependencies": [
                    {
                        "source": case["pressure_id"],
                        "relation": "is_tested_by",
                        "target": case["obligation_id"],
                    }
                    for case in cases
                ],
                "new_distinctions": [
                    {
                        "name": f"representation-versus-target-{case['case_id']}",
                        "left": "representation-level transformation",
                        "right": "unchanged target conclusion",
                        "preservation_condition": case["preservation_condition"],
                    }
                    for case in cases
                ],
                "transformations": [
                    {
                        "input": case["pressure_id"],
                        "operator": f"registered-{arm}-condition",
                        "output": case["obligation_id"],
                    }
                    for case in cases
                ],
                "falsifiers": [case["falsifier"] for case in cases],
                "evaluation_evidence": evidence,
                "surface_form": surface_form,
            },
            "claims": [
                {
                    "proposition": "A structural abstraction materially improves the frozen target route.",
                    "stance": "support" if supports else "oppose",
                }
            ],
            "genealogy": [request["hypothesis_id"]],
            "conceptual_learning": supports,
            "is_dissent": not supports,
            "resource_usage": {"cost_units": 0.25, "storage_bytes": 1024},
        }


def _validate_cases(cases: Sequence[Mapping[str, Any]], target_id: str) -> list[dict[str, Any]]:
    required = {
        "case_id", "target_id", "preferred_lens", "target_statement", "pressure_id",
        "pressure_statement", "obligation_id", "obligation_statement",
        "preservation_condition", "falsifier",
    }
    normalized = [copy.deepcopy(dict(item)) for item in cases]
    if len(normalized) < 2:
        _fail("evaluation requires at least two case-specific held-outs")
    ids: list[str] = []
    lenses: set[str] = set()
    for case in normalized:
        missing = required - case.keys()
        if missing:
            _fail(f"case is missing fields: {sorted(missing)}")
        if case["target_id"] != target_id:
            _fail("held-out case target differs from the evaluated target")
        if case["preferred_lens"] not in {"categorical", "hott"}:
            _fail("each held-out case must select categorical or hott")
        ids.append(str(case["case_id"]))
        lenses.add(str(case["preferred_lens"]))
        for field in required - {"preferred_lens"}:
            if len(str(case[field]).strip()) < 4:
                _fail(f"case {case['case_id']} has decorative {field}")
    if len(ids) != len(set(ids)):
        _fail("held-out case IDs must be unique")
    if lenses != {"categorical", "hott"}:
        _fail("held-out set must exercise both categorical and HoTT selectivity")
    return normalized


def _build_cells(
    target_id: str,
    cases: Sequence[Mapping[str, Any]],
    repetitions: int,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    seeds: list[dict[str, Any]] = []
    cells: dict[str, dict[str, Any]] = {}
    corner = {
        "categorical": "missing_mediator",
        "hott": "duality_completion",
        "combined": "unification_conjecture",
        "incumbent": "conservative_control",
        "no_abstraction": "negative_theory",
    }
    case_suite_digest = canonical_digest(list(cases))
    case_suite_id = stable_identifier(
        "abstraction-case-suite", target_id, case_suite_digest
    )
    for arm in ARMS:
        for repetition in range(1, repetitions + 1):
            branch_id = stable_identifier(
                "abstraction-cell", target_id, arm, repetition, case_suite_id
            )
            hypothesis_id = stable_identifier(
                "abstraction-hypothesis", target_id, arm, repetition, case_suite_id
            )
            seed = {
                "branch_id": branch_id,
                "hypothesis_id": hypothesis_id,
                "corner_family": corner[arm],
                "mechanism_key": f"{arm}-condition-r{repetition}",
                "unique_primitives": [
                    f"condition_{arm}", f"repetition_{repetition}", case_suite_id
                ],
                "maturation_question": (
                    f"For sealed suite {case_suite_id}, can condition {arm} localize "
                    "an executable obligation without changing any target?"
                ),
                "genealogy": [hypothesis_id],
                "is_wildcard": arm == "combined",
                "allowed_skills": {
                    "categorical": ["categorical-concept-forger"],
                    "hott": ["hott-equivalence-coherence-forger"],
                    "combined": ["categorical-concept-forger", "hott-equivalence-coherence-forger"],
                    "incumbent": ["reflective-theory-synthesizer"],
                    "no_abstraction": ["reflective-conceptual-discovery"],
                }[arm],
                "budget": {
                    "wall_seconds": CELL_WALL_SECONDS,
                    "cost_units": 1.0,
                    "storage_bytes": 20_000,
                },
                "expected_theory_delta": "One sealed target-preserving obligation and correction structure.",
            }
            seeds.append(seed)
            cells[branch_id] = {
                "arm": arm,
                "repetition": repetition,
                "case_suite_id": case_suite_id,
                "cases": copy.deepcopy(list(cases)),
            }
    return seeds, cells


def _cell_binding(
    *,
    arm: str,
    repetition: int,
    case_suite_id: str,
    branch_id: str,
    request: Mapping[str, Any],
) -> dict[str, Any]:
    core = {
        "arm": arm,
        "repetition": repetition,
        "case_suite_id": case_suite_id,
        "branch_id": branch_id,
        "request_digest": canonical_digest(request),
        "seed_digest": request["seed_digest"],
        "input_digest": request["input_digest"],
    }
    return {**core, "cell_binding_digest": canonical_digest(core)}


def _operational_attempt_projection(
    *,
    arm: str,
    repetition: int,
    case_suite_id: str,
    branch_id: str,
    request: Mapping[str, Any],
    receipt: Mapping[str, Any],
    result: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Project one runtime receipt without discarding its failure diagnosis."""

    binding = _cell_binding(
        arm=arm,
        repetition=repetition,
        case_suite_id=case_suite_id,
        branch_id=branch_id,
        request=request,
    )
    return {
        "arm": arm,
        "repetition": repetition,
        "case_suite_id": case_suite_id,
        "branch_id": branch_id,
        "request_digest": binding["request_digest"],
        "seed_digest": binding["seed_digest"],
        "cell_binding_digest": binding["cell_binding_digest"],
        "status": receipt["status"],
        "input_digest": receipt["input_digest"],
        "sealed_output_digest": None if result is None else result["output_digest"],
        "branch_receipt_digest": canonical_digest(receipt),
        "opportunity_budget": copy.deepcopy(dict(request["budget"])),
        "validator_receipt_ids": list(receipt["validator_receipt_ids"]),
        "is_dissent": bool(result and result["is_dissent"]),
        "failure_class": receipt["failure_class"],
        "failure_detail": receipt["failure_detail"],
    }


def _overhead(sealed_output: Mapping[str, Any], receipt: Mapping[str, Any]) -> dict[str, Any]:
    usage = receipt["resource_usage"]
    return {
        "wall_seconds": round(float(usage["wall_seconds"]), 6),
        "cost_units": round(float(usage["cost_units"]), 6),
        "storage_bytes": int(usage["storage_bytes"]),
        "semantic_nodes": _node_count(sealed_output),
        "surface_tokens": _surface_tokens(sealed_output),
    }


def _build_task_clusters(
    outputs: Sequence[Mapping[str, Any]],
    cases: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Use held-out cases—not deterministic reruns—as reporting clusters."""

    by_arm_repetition = {
        (str(row["arm"]), int(row["repetition"])): row for row in outputs
    }
    clusters: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        arm_results: list[dict[str, Any]] = []
        for arm in ARMS:
            rows = sorted(
                (row for row in outputs if row["arm"] == arm),
                key=lambda row: int(row["repetition"]),
            )
            score_rows = {
                int(row["repetition"]): next(
                    item for item in row["case_scorecards"] if item["case_id"] == case_id
                )["scorecard"]
                for row in rows
            }
            if not score_rows:
                _fail(
                    f"arm {arm} retained no execution for held-out case {case_id}; "
                    "a zero-retention arm is an execution failure, not a calibration"
                )
            baseline_scores = {
                repetition: next(
                    item
                    for item in by_arm_repetition[("no_abstraction", repetition)]["case_scorecards"]
                    if item["case_id"] == case_id
                )["scorecard"]
                for repetition in score_rows
                if ("no_abstraction", repetition) in by_arm_repetition
            }
            arm_results.append(
                {
                    "arm": arm,
                    "n_completed": len(rows),
                    "retention_status": (
                        "sufficient_retained_repetitions"
                        if len(rows) >= MINIMUM_MATCHED_REPETITIONS
                        else "insufficient_retained_repetitions"
                    ),
                    "score_repeatability": {
                        field: _repeatability([score_rows[rep][field] for rep in sorted(score_rows)])
                        for field in SCORE_FIELDS
                    },
                    "paired_differences_vs_no_abstraction": _paired_calibration(
                        score_rows, baseline_scores
                    ),
                }
            )
        clusters.append(
            {
                "case_id": case_id,
                "case_digest": canonical_digest(case),
                "preferred_lens": case["preferred_lens"],
                "arm_results": arm_results,
            }
        )
    return {
        "unit_of_analysis": "sealed_held_out_case",
        "within_task_repetition_role": "deterministic_repeatability_check_only",
        "iid_assumption": False,
        "population_inference_authorized": False,
        "task_count": len(clusters),
        "clusters": clusters,
    }


def _summarize_negative_controls(outputs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    expected = ("decorative", "restatement", "sham")
    summaries: list[dict[str, Any]] = []
    for kind in expected:
        rows = [
            item
            for output in outputs
            for item in output["negative_control_outcomes"]
            if item["control_kind"] == kind
        ]
        all_zero = bool(rows) and all(item["zero_score_passed"] for item in rows)
        summaries.append(
            {
                "control_kind": kind,
                "control_ids": sorted({str(item["control_id"]) for item in rows}),
                "n_executions": len(rows),
                "all_zero": all_zero,
                "outcome": (
                    "rejected_zero_structural_credit"
                    if all_zero
                    else "failed_control_received_structural_credit"
                ),
            }
        )
    return summaries


def _build_aggregates(
    outputs: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    repetitions: int,
    task_clusters: Mapping[str, Any],
    cases: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_arm: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for output in outputs:
        by_arm[str(output["arm"])].append(output)
    attempt_by_arm: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for attempt in attempts:
        attempt_by_arm[str(attempt["arm"])].append(attempt)
    suite_ids = {str(row["case_suite_id"]) for row in outputs}
    if len(suite_ids) != 1:
        _fail("aggregate outputs must share one exact held-out case suite")
    baseline = {
        int(row["repetition"]): row["scorecard"]
        for row in by_arm["no_abstraction"]
    }
    aggregates: list[dict[str, Any]] = []
    for arm in ARMS:
        rows = sorted(by_arm[arm], key=lambda item: int(item["repetition"]))
        if not rows:
            _fail(
                f"arm {arm} retained no completed execution; the report cannot "
                "fabricate descriptive summaries for an empty arm"
            )
        means = {
            field: _mean([float(row["scorecard"][field]) for row in rows])
            for field in SCORE_FIELDS
        }
        score_repeatability = {
            field: _repeatability([float(row["scorecard"][field]) for row in rows])
            for field in SCORE_FIELDS
        }
        paired = _paired_calibration(
            {int(row["repetition"]): row["scorecard"] for row in rows},
            baseline,
        )
        mean_overhead = {
            field: _mean([float(row["overhead"][field]) for row in rows])
            for field in ("wall_seconds", "cost_units", "storage_bytes", "semantic_nodes", "surface_tokens")
        }
        eligible_case_ids = [
            str(case["case_id"])
            for case in cases
            if arm == "combined"
            or (arm in {"categorical", "hott"} and case["preferred_lens"] == arm)
        ]
        cluster_rows = {
            str(cluster["case_id"]): next(
                item for item in cluster["arm_results"] if item["arm"] == arm
            )
            for cluster in task_clusters["clusters"]
        }
        positive_dimensions = [
            field
            for field in SCORE_FIELDS
            if eligible_case_ids
            and all(
                cluster_rows[case_id]["paired_differences_vs_no_abstraction"]["status"]
                == "sufficient_internal_calibration"
                and cluster_rows[case_id]["paired_differences_vs_no_abstraction"]
                ["diagnostics"][field]["minimum"] > 0
                for case_id in eligible_case_ids
            )
        ]
        aggregates.append(
            {
                "arm": arm,
                "n_scheduled": repetitions,
                "n_completed": len(rows),
                "n_failed": sum(item["status"] != "completed" for item in attempt_by_arm[arm]),
                "retention_status": (
                    "sufficient_retained_repetitions"
                    if len(rows) >= MINIMUM_MATCHED_REPETITIONS
                    else "insufficient_retained_repetitions"
                ),
                "descriptive_mean_scorecard": means,
                "score_repeatability": score_repeatability,
                "mean_overhead": mean_overhead,
                "paired_differences_vs_no_abstraction": paired,
                "task_cluster_summary": {
                    "eligible_case_ids": eligible_case_ids,
                    "task_cluster_count": len(eligible_case_ids),
                    "dimensions_positive_on_all_eligible_cases": positive_dimensions,
                },
                "internal_refinement_eligible": (
                    arm in {"categorical", "hott", "combined"}
                    and paired["status"] == "sufficient_internal_calibration"
                    and len(positive_dimensions) >= 2
                ),
            }
        )
    return aggregates


def _calibration_summary(aggregates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Type full-factorial sufficiency without promoting descriptive arm means."""

    paired_counts = {
        str(row["arm"]): int(
            row["paired_differences_vs_no_abstraction"]["n_matched_repetitions"]
        )
        for row in aggregates
    }
    insufficient = sorted(
        arm
        for arm, count in paired_counts.items()
        if count < MINIMUM_MATCHED_REPETITIONS
    )
    return {
        "calibration_status": (
            "sufficient_internal_calibration"
            if not insufficient
            else "insufficient_internal_calibration"
        ),
        "minimum_matched_repetitions_per_arm": min(paired_counts.values()),
        "insufficient_calibration_arms": insufficient,
    }


def _validate_basis(
    literature_snapshot: Mapping[str, Any],
    assimilation_packet: Mapping[str, Any],
    source_portfolio: Mapping[str, Any],
    *,
    require_present: bool = False,
    present_use_at: dt.datetime | None = None,
) -> None:
    try:
        validate_snapshot(literature_snapshot)
        validate_assimilation(assimilation_packet, snapshot=literature_snapshot)
        validate_high_risk_portfolio(source_portfolio, literature_snapshot=literature_snapshot)
    except ContractError as exc:
        _fail(str(exc))
    if literature_snapshot["provenance_mode"] != "live":
        _fail("active abstraction evaluation requires a receipt-backed live snapshot")
    freshness = (
        resolve_present_literature_freshness(
            assimilation_packet, now=present_use_at
        )
        if require_present
        else assimilation_packet["resolution"]
    )
    if freshness["freshness_status"] != "current":
        _fail("abstraction evaluation requires current literature assimilation")
    if freshness["active_investment_gate"] != "pass":
        _fail("literature assimilation blocks active investment")
    if assimilation_packet["hypothesis_rebase_status"] != "current":
        _fail("hypotheses have not been rebased to the current literature snapshot")


def _evaluation_common_input_digest(
    *,
    target_id: str,
    literature_snapshot_digest: str,
    assimilation_digest: str,
    source_portfolio_digest: str,
    cases: Sequence[Mapping[str, Any]],
    repetitions: int,
    failure_schedule: Sequence[Mapping[str, Any]],
    dependency_authority_digest: str,
) -> str:
    """Derive the one common identity used by success and hard-failure paths."""

    return canonical_digest(
        {
            "target_id": target_id,
            "literature_snapshot_digest": literature_snapshot_digest,
            "assimilation_digest": assimilation_digest,
            "source_portfolio_digest": source_portfolio_digest,
            "cases": list(cases),
            "arms": ARMS,
            "repetitions": repetitions,
            "precommitted_failure_cells": list(failure_schedule),
            "rubric_digest": RUBRIC_DIGEST,
            "dependency_authority_digest": dependency_authority_digest,
        }
    )


def validate_abstraction_evaluation_failure_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay a hard-floor failure from its full basis, runtime, and receipts."""

    packet = copy.deepcopy(dict(evidence))
    try:
        validate_instance(packet, "abstraction_evaluation_failure.schema.json")
    except ContractError as exc:
        _fail(str(exc))
    if packet["content_digest"] != canonical_digest(_without(packet, "content_digest")):
        _fail("abstraction failure evidence content digest mismatch")
    try:
        dependency_context = _validate_formal_dependency_run_context(
            packet["dependency_authority"]
        )
        validate_parallel_portfolio(packet["runtime_portfolio"])
    except (FormalDependencyAuthorityError, ContractError) as exc:
        _fail(str(exc))
    dependency_authority = dependency_context.snapshot()
    runtime = packet["runtime_portfolio"]
    if packet["dependency_authority_digest"] != dependency_authority["content_digest"]:
        _fail("abstraction failure changed its dependency authority digest")
    if packet["runtime_portfolio_digest"] != runtime["content_digest"]:
        _fail("abstraction failure changed its runtime portfolio digest")
    if packet["rubric_digest"] != RUBRIC_DIGEST:
        _fail("abstraction failure rubric digest differs from the live sealed rubric")
    snapshot = packet["literature_snapshot"]
    assimilation = packet["assimilation_packet"]
    portfolio = packet["source_portfolio"]
    _validate_basis(snapshot, assimilation, portfolio)
    if (
        packet["literature_snapshot_digest"] != snapshot["content_digest"]
        or packet["assimilation_digest"] != assimilation["content_digest"]
        or packet["source_portfolio_digest"] != portfolio["content_digest"]
    ):
        _fail("abstraction failure basis digest mismatch")
    target_id = str(packet["target_id"])
    if target_id != snapshot["target_id"] or target_id != runtime["target_id"]:
        _fail("abstraction failure target differs across its sealed basis")
    cases = _validate_cases(packet["held_out_cases"], target_id)
    if packet["held_out_case_suite_digest"] != canonical_digest(cases):
        _fail("abstraction failure held-out suite digest mismatch")
    repetitions = int(packet["repetitions_scheduled_per_arm"])
    expected_seeds, expected_cells = _build_cells(target_id, cases, repetitions)
    suite_ids = {str(row["case_suite_id"]) for row in expected_cells.values()}
    if suite_ids != {packet["case_suite_id"]} or tuple(packet["factorial_arms"]) != ARMS:
        _fail("abstraction failure changed its exact factorial or case suite")
    schedule = list(packet["precommitted_failures"])
    if len({(row["arm"], row["repetition"]) for row in schedule}) != len(schedule):
        _fail("abstraction failure schedule contains duplicate cells")
    for row in schedule:
        cell = expected_cells.get(str(row["branch_id"]))
        if cell is None or (row["arm"], int(row["repetition"])) != (
            cell["arm"],
            cell["repetition"],
        ):
            _fail("abstraction failure schedule is not bound to an exact cell")
    expected_common_input = _evaluation_common_input_digest(
        target_id=target_id,
        literature_snapshot_digest=snapshot["content_digest"],
        assimilation_digest=assimilation["content_digest"],
        source_portfolio_digest=portfolio["content_digest"],
        cases=cases,
        repetitions=repetitions,
        failure_schedule=schedule,
        dependency_authority_digest=dependency_authority["content_digest"],
    )
    if packet["common_input_digest"] != expected_common_input:
        _fail("abstraction failure common input digest mismatch")
    expected_manifest = build_parallel_manifest(
        portfolio,
        base_theory_state_version=0,
        branch_seeds=expected_seeds,
        resource_budget=runtime["resource_budget"],
    )
    if runtime["branch_requests"] != expected_manifest["branch_requests"]:
        _fail("abstraction failure runtime requests differ from the sealed factorial")
    runtime_receipts = {row["branch_id"]: row for row in runtime["attempt_receipts"]}
    runtime_results = {row["branch_id"]: row for row in runtime["branch_results"]}
    runtime_requests = {row["branch_id"]: row for row in runtime["branch_requests"]}
    scheduled_failure_ids = {str(row["branch_id"]) for row in schedule}
    if any(
        runtime_receipts[branch_id]["status"] not in PRECOMMITTED_FAILURE_STATUSES
        for branch_id in scheduled_failure_ids
    ):
        _fail("a precommitted abstraction failure has a completed or disallowed runtime status")
    expected_attempts: list[dict[str, Any]] = []
    for arm in ARMS:
        for repetition in range(1, repetitions + 1):
            branch_id = next(
                branch_id
                for branch_id, cell in expected_cells.items()
                if cell["arm"] == arm and cell["repetition"] == repetition
            )
            expected_attempts.append(
                _operational_attempt_projection(
                    arm=arm,
                    repetition=repetition,
                    case_suite_id=packet["case_suite_id"],
                    branch_id=branch_id,
                    request=runtime_requests[branch_id],
                    receipt=runtime_receipts[branch_id],
                    result=runtime_results.get(branch_id),
                )
            )
    if packet["attempt_receipts"] != expected_attempts:
        _fail("abstraction failure attempts are not exact runtime projections")
    completed = [row for row in expected_attempts if row["status"] == "completed"]
    failed = [row for row in expected_attempts if row["status"] != "completed"]
    actual_failure_ids = {str(row["branch_id"]) for row in failed}
    if packet["unexpected_failure_branch_ids"] != sorted(
        actual_failure_ids - scheduled_failure_ids
    ):
        _fail("abstraction failure unexpected-branch ledger is not an exact projection")
    if any(row["failure_class"] is not None or row["failure_detail"] is not None for row in completed):
        _fail("completed abstraction siblings cannot carry failure diagnostics")
    if any(
        not isinstance(row["failure_class"], str)
        or not row["failure_class"].strip()
        or not isinstance(row["failure_detail"], str)
        or not row["failure_detail"].strip()
        for row in failed
    ):
        _fail("failed abstraction attempts must preserve failure class and detail")
    completed_by_arm = {
        arm: sum(row["arm"] == arm for row in completed) for arm in ARMS
    }
    under_retained = {
        arm: count
        for arm, count in completed_by_arm.items()
        if count < MINIMUM_MATCHED_REPETITIONS
    }
    if not under_retained:
        _fail("hard-floor failure evidence has no under-retained arm")
    if (
        packet["completed_by_arm"] != completed_by_arm
        or packet["under_retained_arms"] != under_retained
        or packet["failed_attempts"] != failed
        or packet["completed_sibling_branch_ids"]
        != sorted(row["branch_id"] for row in completed)
    ):
        _fail("abstraction failure sibling or failure ledger mismatch")
    expected_failure_id = stable_identifier(
        "abstraction-evaluation-failure",
        expected_common_input,
        runtime["content_digest"],
    )
    if packet["failure_id"] != expected_failure_id:
        _fail("abstraction failure identity mismatch")
    return {
        "status": "valid_hard_floor_failure",
        "failure_id": expected_failure_id,
        "completed_sibling_count": len(completed),
        "failed_attempt_count": len(failed),
        "under_retained_arms": under_retained,
    }


def run_abstraction_parallel_evaluation(
    *,
    literature_snapshot: Mapping[str, Any],
    assimilation_packet: Mapping[str, Any],
    source_portfolio: Mapping[str, Any],
    cases: Sequence[Mapping[str, Any]],
    repetitions: int = 6,
    max_workers: int = 5,
    now: dt.datetime | None = None,
    precommitted_failure_cells: Sequence[tuple[str, int]] | None = None,
) -> dict[str, Any]:
    """Execute five conditions and retain typed evidence after partial failure.

    The optional failure schedule is a deterministic test/control surface.  It
    is sealed into the common input identity before execution.  At least one
    execution per arm must survive so raw operational diagnostics are honest.
    After fan-in, fewer than five completed executions in any arm is a hard
    calibration failure with a separate digest-bound failure-evidence payload;
    no underpowered comparison report is emitted.
    """

    if repetitions < 6:
        _fail("schedule at least six repetitions so one failure leaves five retained")
    if max_workers < 2:
        _fail("parallel evaluation requires at least two isolated workers")
    snapshot = copy.deepcopy(dict(literature_snapshot))
    assimilation = copy.deepcopy(dict(assimilation_packet))
    portfolio = copy.deepcopy(dict(source_portfolio))
    _validate_basis(
        snapshot,
        assimilation,
        portfolio,
        require_present=True,
        present_use_at=now,
    )
    target_id = str(portfolio["target_id"])
    normalized_cases = _validate_cases(cases, target_id)
    # Freeze the complete byte/import/schema closure once before fan-out.  Every
    # worker and nested witness binds this exact record; the second full check
    # after fan-in detects dependency drift without rescanning in every cell.
    dependency_context = _build_formal_dependency_run_context()
    dependency_authority = dependency_context.snapshot()
    seeds, cells = _build_cells(target_id, normalized_cases, repetitions)
    requested_failures = list(
        precommitted_failure_cells
        if precommitted_failure_cells is not None
        else [("categorical", repetitions)]
    )
    normalized_failures = sorted(
        {(str(arm), int(repetition)) for arm, repetition in requested_failures}
    )
    if not normalized_failures:
        _fail("at least one precommitted failure is required by this calibration")
    if any(
        arm not in ARMS or repetition < 1 or repetition > repetitions
        for arm, repetition in normalized_failures
    ):
        _fail("precommitted failure cells must name an exact scheduled arm/repetition")
    retained_after_schedule = {
        arm: repetitions - sum(cell_arm == arm for cell_arm, _ in normalized_failures)
        for arm in ARMS
    }
    if any(count < 1 for count in retained_after_schedule.values()):
        _fail("a precommitted failure schedule must retain at least one execution per arm")
    failure_schedule = [
        {
            "arm": arm,
            "repetition": repetition,
            "branch_id": next(
                branch_id
                for branch_id, cell in cells.items()
                if cell["arm"] == arm and cell["repetition"] == repetition
            ),
        }
        for arm, repetition in normalized_failures
    ]
    failure_ids = {row["branch_id"] for row in failure_schedule}
    common_input_digest = _evaluation_common_input_digest(
        target_id=target_id,
        literature_snapshot_digest=snapshot["content_digest"],
        assimilation_digest=assimilation["content_digest"],
        source_portfolio_digest=portfolio["content_digest"],
        cases=normalized_cases,
        repetitions=repetitions,
        failure_schedule=failure_schedule,
        dependency_authority_digest=dependency_authority["content_digest"],
    )
    portfolio_wall_seconds = (
        ((len(seeds) + max_workers - 1) // max_workers) * CELL_WALL_SECONDS
        + CELL_WALL_SECONDS
    )
    manifest = build_parallel_manifest(
        portfolio,
        base_theory_state_version=0,
        branch_seeds=seeds,
        resource_budget={
            "wall_seconds": portfolio_wall_seconds,
            "max_workers": max_workers,
            "cost_units": float(len(seeds)),
            "storage_bytes": len(seeds) * 20_000,
        },
    )
    runtime = run_parallel_hypothesis_portfolio(
        manifest,
        _AbstractionCellWorker(
            cells,
            sorted(failure_ids),
            dependency_context,
        ),
    )
    validate_parallel_portfolio(runtime)
    try:
        dependency_context = _validate_formal_dependency_run_context(
            dependency_authority
        )
        dependency_authority = dependency_context.snapshot()
    except FormalDependencyAuthorityError as exc:
        _fail(f"formal dependency authority drifted during factorial execution: {exc}")

    runtime_receipts = {row["branch_id"]: row for row in runtime["attempt_receipts"]}
    runtime_results = {row["branch_id"]: row for row in runtime["branch_results"]}
    attempts: list[dict[str, Any]] = []
    operational_attempts: list[dict[str, Any]] = []
    outputs: list[dict[str, Any]] = []
    common_budget: dict[str, Any] | None = None
    for arm in ARMS:
        for repetition in range(1, repetitions + 1):
            branch_id = next(
                key for key, cell in cells.items()
                if cell["arm"] == arm and cell["repetition"] == repetition
            )
            cell = cells[branch_id]
            receipt = runtime_receipts[branch_id]
            request = next(row for row in runtime["branch_requests"] if row["branch_id"] == branch_id)
            budget = copy.deepcopy(dict(request["budget"]))
            if common_budget is None:
                common_budget = {**budget, "max_workers": max_workers}
            result = runtime_results.get(branch_id)
            binding = _cell_binding(
                arm=arm,
                repetition=repetition,
                case_suite_id=cell["case_suite_id"],
                branch_id=branch_id,
                request=request,
            )
            operational_attempt = _operational_attempt_projection(
                arm=arm,
                repetition=repetition,
                case_suite_id=cell["case_suite_id"],
                branch_id=branch_id,
                request=request,
                receipt=receipt,
                result=result,
            )
            operational_attempts.append(operational_attempt)
            attempts.append(_without(operational_attempt, "failure_class", "failure_detail"))
            if result is None:
                continue
            sealed = _without(result, "output_digest")
            alias = stable_identifier("blind-output", result["output_digest"])
            projection = blinded_structural_projection(sealed)
            execution = sealed["theory_delta"]["forger_execution"]
            outputs.append(
                {
                    "arm": arm,
                    "repetition": repetition,
                    "case_suite_id": cell["case_suite_id"],
                    "branch_id": branch_id,
                    "cell_binding_digest": binding["cell_binding_digest"],
                    "blind_alias": alias,
                    "sealed_output": sealed,
                    "sealed_output_digest": result["output_digest"],
                    "blinded_projection_digest": canonical_digest(projection),
                    "scorecard": blinded_structural_score(sealed),
                    "case_scorecards": [
                        _case_scorecard(execution, case) for case in normalized_cases
                    ],
                    "negative_control_outcomes": _negative_control_outcomes(execution),
                    "overhead": _overhead(sealed, receipt),
                    "is_dissent": bool(result["is_dissent"]),
                }
            )
    assert common_budget is not None
    completed_by_arm = {
        arm: sum(row["arm"] == arm for row in outputs)
        for arm in ARMS
    }
    under_retained = {
        arm: count
        for arm, count in completed_by_arm.items()
        if count < MINIMUM_MATCHED_REPETITIONS
    }
    if under_retained:
        failed_attempts = [
            copy.deepcopy(row)
            for row in operational_attempts
            if row["status"] != "completed"
        ]
        failure_evidence = {
            "schema_version": "1.0.0",
            "failure_id": stable_identifier(
                "abstraction-evaluation-failure",
                common_input_digest,
                runtime["content_digest"],
            ),
            "status": "insufficient_retained_executions",
            "target_id": target_id,
            "factorial_arms": list(ARMS),
            "repetitions_scheduled_per_arm": repetitions,
            "minimum_required_per_arm": MINIMUM_MATCHED_REPETITIONS,
            "case_suite_id": next(iter({cell["case_suite_id"] for cell in cells.values()})),
            "held_out_cases": normalized_cases,
            "held_out_case_suite_digest": canonical_digest(normalized_cases),
            "literature_snapshot": snapshot,
            "literature_snapshot_digest": snapshot["content_digest"],
            "assimilation_packet": assimilation,
            "assimilation_digest": assimilation["content_digest"],
            "source_portfolio": portfolio,
            "source_portfolio_digest": portfolio["content_digest"],
            "precommitted_failures": failure_schedule,
            "common_input_digest": common_input_digest,
            "rubric_digest": RUBRIC_DIGEST,
            "dependency_authority": dependency_authority,
            "runtime_portfolio": runtime,
            "attempt_receipts": operational_attempts,
            "completed_sibling_branch_ids": sorted(
                row["branch_id"]
                for row in operational_attempts
                if row["status"] == "completed"
            ),
            "unexpected_failure_branch_ids": sorted(
                row["branch_id"]
                for row in operational_attempts
                if row["status"] != "completed" and row["branch_id"] not in failure_ids
            ),
            "completed_by_arm": completed_by_arm,
            "under_retained_arms": under_retained,
            "failed_attempts": failed_attempts,
            "runtime_portfolio_digest": runtime["content_digest"],
            "dependency_authority_digest": dependency_authority["content_digest"],
        }
        failure_evidence["content_digest"] = canonical_digest(failure_evidence)
        validate_abstraction_evaluation_failure_evidence(failure_evidence)
        _fail(
            "parallel evaluation retained fewer than five completed executions "
            f"for arm(s): {under_retained}",
            failure_evidence=failure_evidence,
        )
    blind_order = sorted(
        outputs,
        key=lambda row: canonical_digest([common_input_digest, row["blind_alias"]]),
    )
    evaluator_core = {
        "evaluator_id": "abstraction-structural-evaluator",
        "evaluator_version": "1.0.0",
        "evaluator_executable_digest": callable_digest(blinded_structural_score),
        "dependency_authority_digest": dependency_authority["content_digest"],
        "rubric_digest": RUBRIC_DIGEST,
        "blind": True,
        "authority_class": "internal_protocol_calibration",
        "conceptual_value_authorized": False,
        "physics_value_authorized": False,
        "counterbalanced_seed_digest": canonical_digest([common_input_digest, "counterbalanced-v1"]),
        "sealed_output_set_digest": canonical_digest(
            [row["sealed_output_digest"] for row in blind_order]
        ),
        "blinded_input_set_digest": canonical_digest(
            [[row["blind_alias"], row["blinded_projection_digest"]] for row in blind_order]
        ),
        "score_set_digest": canonical_digest(
            [[row["blind_alias"], row["scorecard"]] for row in blind_order]
        ),
        "receipt_id": stable_identifier(
            "abstraction-evaluator-receipt",
            common_input_digest,
            RUBRIC_DIGEST,
            callable_digest(blinded_structural_score),
            dependency_authority["content_digest"],
        ),
        "external_human": {
            "status": "unavailable",
            "reason": "No authenticated external-human evaluation was supplied for this run.",
            "fabricated": False,
            "receipt_id": None,
        },
    }
    evaluator_core["receipt_digest"] = canonical_digest(evaluator_core)
    task_clusters = _build_task_clusters(outputs, normalized_cases)
    negative_control_outcomes = _summarize_negative_controls(outputs)
    aggregates = _build_aggregates(
        outputs, attempts, repetitions, task_clusters, normalized_cases
    )
    calibration = _calibration_summary(aggregates)
    retained = sorted(row["branch_id"] for row in outputs)
    failed_branch_ids = sorted(
        row["branch_id"] for row in attempts if row["status"] != "completed"
    )
    runtime_dissent = runtime["merge_proposal"]["retained_dissent_ids"]
    case_suite_id = next(iter({cell["case_suite_id"] for cell in cells.values()}))
    full_factorial_refinement_eligible = (
        calibration["calibration_status"] == "sufficient_internal_calibration"
        and all(
            row["internal_refinement_eligible"]
            for row in aggregates
            if row["arm"] in {"categorical", "hott", "combined"}
        )
    )
    report: dict[str, Any] = {
        "schema_version": "4.0.0",
        "evaluation_id": stable_identifier(
            "abstraction-evaluation", target_id, common_input_digest, runtime["content_digest"]
        ),
        "target_id": target_id,
        "literature_snapshot_id": snapshot["snapshot_id"],
        "literature_snapshot_digest": snapshot["content_digest"],
        "assimilation_packet_id": assimilation["packet_id"],
        "assimilation_digest": assimilation["content_digest"],
        "factorial_arms": list(ARMS),
        "repetitions_scheduled_per_arm": repetitions,
        "minimum_retained_repetitions_per_arm": min(
            row["n_completed"] for row in aggregates
        ),
        "minimum_matched_repetitions_per_arm": calibration[
            "minimum_matched_repetitions_per_arm"
        ],
        "calibration_status": calibration["calibration_status"],
        "common_input_digest": common_input_digest,
        "common_budget": common_budget,
        "matched_budget": True,
        "case_suite_id": case_suite_id,
        "held_out_cases": normalized_cases,
        "held_out_case_suite_digest": canonical_digest(normalized_cases),
        "dependency_authority": dependency_authority,
        "skill_bindings": [
            {"skill_id": "categorical-concept-forger", "contract_schema": "agentic/spec/abstraction_forge_packet.schema.json", "registry_status": "promoted", "dependency_authority_digest": dependency_authority["content_digest"]},
            {"skill_id": "hott-equivalence-coherence-forger", "contract_schema": "agentic/spec/abstraction_forge_packet.schema.json", "registry_status": "promoted", "dependency_authority_digest": dependency_authority["content_digest"]},
            {"skill_id": "ym-categorical-hott-physics-bridge", "contract_schema": "agentic/spec/ym_categorical_hott_bridge.schema.json", "registry_status": "promoted", "dependency_authority_digest": dependency_authority["content_digest"]},
        ],
        "literature_snapshot": snapshot,
        "assimilation_packet": assimilation,
        "source_portfolio": portfolio,
        "source_portfolio_digest": portfolio["content_digest"],
        "runtime_portfolio": runtime,
        "runtime_portfolio_digest": runtime["content_digest"],
        "attempt_receipts": attempts,
        "condition_outputs": outputs,
        "evaluator_evidence": evaluator_core,
        "task_clustered_reporting": task_clusters,
        "negative_control_outcomes": negative_control_outcomes,
        "aggregates": aggregates,
        "partial_failure": {
            "precommitted_failures": [
                {**row, "status": runtime_receipts[row["branch_id"]]["status"]}
                for row in failure_schedule
            ],
            "unexpected_failure_branch_ids": sorted(
                set(failed_branch_ids) - failure_ids
            ),
            "retained_completed_branch_ids": retained,
            "minimum_completed_per_arm": min(row["n_completed"] for row in aggregates),
            "insufficient_calibration_arms": calibration[
                "insufficient_calibration_arms"
            ],
            "siblings_preserved": True,
        },
        "dissent": {
            "retained_dissent_branch_ids": list(runtime_dissent),
            "contradiction_edges": copy.deepcopy(runtime["merge_proposal"]["contradiction_edges"]),
            "flattened": False,
        },
        "decision_authority": {
            "status": "internal_calibration_refinement_only",
            "calibration_status": calibration["calibration_status"],
            "full_factorial_refinement_eligible": full_factorial_refinement_eligible,
            "investment_authorized": False,
            "conceptual_value_authorized": False,
            "physics_value_authorized": False,
            "reason": (
                "Worker profiles precommit the structural cardinalities later counted by the "
                "internal evaluator; task-clustered repeatability may guide refinement, but "
                "cannot establish conceptual or physical value or authorize investment."
            ),
        },
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    report["content_digest"] = canonical_digest(_without(report, "content_digest"))
    validate_abstraction_parallel_evaluation(report)
    return report


def validate_abstraction_parallel_evaluation(report: Mapping[str, Any]) -> dict[str, Any]:
    """Transitively recompute execution, cell, seal, evaluator, and effect evidence."""

    packet = copy.deepcopy(dict(report))
    try:
        validate_instance(packet, "abstraction_parallel_evaluation.schema.json")
    except ContractError as exc:
        _fail(str(exc))
    if packet["content_digest"] != canonical_digest(_without(packet, "content_digest")):
        _fail("parallel evaluation content digest mismatch")
    try:
        dependency_context = _validate_formal_dependency_run_context(
            packet["dependency_authority"]
        )
        dependency_authority = dependency_context.snapshot()
    except FormalDependencyAuthorityError as exc:
        _fail(str(exc))
    expected_bindings = [
        {"skill_id": "categorical-concept-forger", "contract_schema": "agentic/spec/abstraction_forge_packet.schema.json", "registry_status": "promoted", "dependency_authority_digest": dependency_authority["content_digest"]},
        {"skill_id": "hott-equivalence-coherence-forger", "contract_schema": "agentic/spec/abstraction_forge_packet.schema.json", "registry_status": "promoted", "dependency_authority_digest": dependency_authority["content_digest"]},
        {"skill_id": "ym-categorical-hott-physics-bridge", "contract_schema": "agentic/spec/ym_categorical_hott_bridge.schema.json", "registry_status": "promoted", "dependency_authority_digest": dependency_authority["content_digest"]},
    ]
    if packet["skill_bindings"] != expected_bindings:
        _fail("skill bindings are not exact semantic-ID projections of the formal contracts")
    _validate_basis(
        packet["literature_snapshot"],
        packet["assimilation_packet"],
        packet["source_portfolio"],
    )
    if packet["source_portfolio_digest"] != packet["source_portfolio"]["content_digest"]:
        _fail("source portfolio digest binding mismatch")
    runtime = packet["runtime_portfolio"]
    try:
        validate_parallel_portfolio(runtime)
    except ContractError as exc:
        _fail(str(exc))
    if packet["runtime_portfolio_digest"] != runtime["content_digest"]:
        _fail("runtime portfolio digest binding mismatch")
    if packet["target_id"] != runtime["target_id"] or packet["target_id"] != packet["literature_snapshot"]["target_id"]:
        _fail("evaluation target differs across frozen artifacts")
    if packet["literature_snapshot_digest"] != runtime["literature_snapshot_digest"]:
        _fail("runtime did not use the report's exact literature snapshot")
    if packet["assimilation_digest"] != packet["assimilation_packet"]["content_digest"]:
        _fail("assimilation digest binding mismatch")
    if tuple(packet["factorial_arms"]) != ARMS:
        _fail("factorial arms must be the exact precommitted five-arm order")
    repetitions = int(packet["repetitions_scheduled_per_arm"])
    cases = _validate_cases(packet["held_out_cases"], packet["target_id"])
    if packet["held_out_case_suite_digest"] != canonical_digest(cases):
        _fail("held-out case suite digest mismatch")
    expected_seeds, expected_cell_map = _build_cells(
        packet["target_id"], cases, repetitions
    )
    expected_suite_ids = {
        str(cell["case_suite_id"]) for cell in expected_cell_map.values()
    }
    if len(expected_suite_ids) != 1 or packet["case_suite_id"] not in expected_suite_ids:
        _fail("case_suite_id is not the exact identity of the held-out task suite")
    expected_manifest = build_parallel_manifest(
        packet["source_portfolio"],
        base_theory_state_version=0,
        branch_seeds=expected_seeds,
        resource_budget=runtime["resource_budget"],
    )
    if runtime["branch_requests"] != expected_manifest["branch_requests"]:
        _fail("runtime branch requests are not the exact sealed cell seeds")
    expected_common_input = _evaluation_common_input_digest(
        target_id=packet["target_id"],
        literature_snapshot_digest=packet["literature_snapshot"]["content_digest"],
        assimilation_digest=packet["assimilation_packet"]["content_digest"],
        source_portfolio_digest=packet["source_portfolio"]["content_digest"],
        cases=cases,
        repetitions=repetitions,
        failure_schedule=[
            {
                "arm": row["arm"],
                "repetition": row["repetition"],
                "branch_id": row["branch_id"],
            }
            for row in packet["partial_failure"]["precommitted_failures"]
        ],
        dependency_authority_digest=dependency_authority["content_digest"],
    )
    if packet["common_input_digest"] != expected_common_input:
        _fail("common evaluation input digest was not recomputed from sealed cases")
    if packet["evaluation_id"] != stable_identifier(
        "abstraction-evaluation",
        packet["target_id"],
        expected_common_input,
        runtime["content_digest"],
    ):
        _fail("evaluation identity differs from its runtime and common input")
    expected_cells = {(arm, repetition) for arm in ARMS for repetition in range(1, repetitions + 1)}
    attempts = list(packet["attempt_receipts"])
    actual_cells = {(row["arm"], int(row["repetition"])) for row in attempts}
    if actual_cells != expected_cells or len(attempts) != len(expected_cells):
        _fail("attempt receipts do not form one exact arm-by-repetition factorial")
    if len({row["branch_id"] for row in attempts}) != len(attempts):
        _fail("factorial attempt branch IDs are not unique")
    runtime_receipts = {row["branch_id"]: row for row in runtime["attempt_receipts"]}
    runtime_results = {row["branch_id"]: row for row in runtime["branch_results"]}
    runtime_requests = {row["branch_id"]: row for row in runtime["branch_requests"]}
    budgets = []
    for row in attempts:
        branch_id = row["branch_id"]
        if branch_id not in runtime_receipts or branch_id not in runtime_requests:
            _fail("evaluation receipt cites a branch outside the runtime portfolio")
        receipt = runtime_receipts[branch_id]
        request = runtime_requests[branch_id]
        cell = expected_cell_map.get(branch_id)
        if cell is None:
            _fail("attempt branch is outside the precommitted cell map")
        binding = _cell_binding(
            arm=cell["arm"],
            repetition=cell["repetition"],
            case_suite_id=cell["case_suite_id"],
            branch_id=branch_id,
            request=request,
        )
        for field in (
            "arm",
            "repetition",
            "case_suite_id",
            "request_digest",
            "seed_digest",
            "cell_binding_digest",
        ):
            if row[field] != binding[field]:
                _fail(f"attempt {field} is not bound to its request and seed")
        if row["status"] != receipt["status"] or row["input_digest"] != receipt["input_digest"]:
            _fail("attempt summary differs from its runtime receipt")
        if row["branch_receipt_digest"] != canonical_digest(receipt):
            _fail("attempt receipt digest mismatch")
        if row["validator_receipt_ids"] != receipt["validator_receipt_ids"]:
            _fail("attempt validator receipts differ from the runtime receipt")
        if row["opportunity_budget"] != request["budget"]:
            _fail("attempt opportunity budget differs from the executed request")
        budgets.append(canonical_digest(row["opportunity_budget"]))
        result = runtime_results.get(branch_id)
        expected_output = None if result is None else result["output_digest"]
        if row["sealed_output_digest"] != expected_output:
            _fail("attempt output seal differs from the runtime result")
    if len(set(budgets)) != 1 or packet["matched_budget"] is not True:
        _fail("all factorial cells must receive exactly equal opportunity budgets")
    common = {**attempts[0]["opportunity_budget"], "max_workers": runtime["resource_budget"]["max_workers"]}
    if packet["common_budget"] != common:
        _fail("common budget summary does not match executed requests")

    outputs = list(packet["condition_outputs"])
    completed_ids = {row["branch_id"] for row in attempts if row["status"] == "completed"}
    if {row["branch_id"] for row in outputs} != completed_ids or len(outputs) != len(completed_ids):
        _fail("condition outputs must represent every and only completed branch once")
    for row in outputs:
        branch_id = row["branch_id"]
        runtime_result = runtime_results[branch_id]
        attempt = next(item for item in attempts if item["branch_id"] == branch_id)
        for field in ("arm", "repetition", "case_suite_id", "cell_binding_digest"):
            if row[field] != attempt[field]:
                _fail(f"condition output {field} differs from its attempt")
        sealed = row["sealed_output"]
        if sealed != _without(runtime_result, "output_digest"):
            _fail("sealed output content differs from the executed branch result")
        if row["sealed_output_digest"] != canonical_digest(sealed):
            _fail("sealed output digest mismatch")
        projection = blinded_structural_projection(sealed)
        if row["blinded_projection_digest"] != canonical_digest(projection):
            _fail("blinded evaluator projection digest mismatch")
        if row["scorecard"] != blinded_structural_score(sealed):
            _fail("scorecard was not derived from the blinded structural projection")
        try:
            replay = validate_condition_forger_result(
                sealed["theory_delta"]["forger_execution"],
                row["arm"],
                cases,
                _dependency_context=dependency_context,
            )
        except (KeyError, FormalReasoningError) as exc:
            _fail(f"registered condition forger replay failed: {exc}")
        if sealed["theory_delta"]["evaluation_evidence"] != replay["evaluation_evidence"]:
            _fail("condition score evidence was not derived from the forger replay")
        expected_case_scores = [_case_scorecard(replay, case) for case in cases]
        if row["case_scorecards"] != expected_case_scores:
            _fail("case scorecards were not projected from exact held-out tasks")
        expected_controls = _negative_control_outcomes(replay)
        if row["negative_control_outcomes"] != expected_controls:
            _fail("negative-control outcomes were not replayed exactly")
        if any(not item["zero_score_passed"] for item in expected_controls):
            _fail("decorative, restatement, or sham control earned credit")
        if row["blind_alias"] != stable_identifier(
            "blind-output", row["sealed_output_digest"]
        ):
            _fail("blind alias is not derived from the sealed output")
        receipt = runtime_receipts[branch_id]
        if row["overhead"] != _overhead(sealed, receipt):
            _fail("abstraction overhead summary differs from executed evidence")
        if row["is_dissent"] != bool(runtime_result["is_dissent"]):
            _fail("dissent label differs from the runtime result")
    blind_order = sorted(
        outputs,
        key=lambda row: canonical_digest([packet["common_input_digest"], row["blind_alias"]]),
    )
    evaluator = packet["evaluator_evidence"]
    evaluator_core = _without(evaluator, "receipt_digest")
    if evaluator["receipt_digest"] != canonical_digest(evaluator_core):
        _fail("evaluator receipt digest mismatch")
    expected_eval = {
        "sealed_output_set_digest": canonical_digest([row["sealed_output_digest"] for row in blind_order]),
        "blinded_input_set_digest": canonical_digest([[row["blind_alias"], row["blinded_projection_digest"]] for row in blind_order]),
        "score_set_digest": canonical_digest([[row["blind_alias"], row["scorecard"]] for row in blind_order]),
    }
    for field, expected in expected_eval.items():
        if evaluator[field] != expected:
            _fail(f"evaluator {field} mismatch")
    if evaluator["rubric_digest"] != RUBRIC_DIGEST or evaluator["blind"] is not True:
        _fail("evaluator rubric or blinding authority differs from the executable contract")
    expected_executable = callable_digest(blinded_structural_score)
    if evaluator["evaluator_executable_digest"] != expected_executable:
        _fail("evaluator executable digest differs from the live scorer")
    if evaluator["dependency_authority_digest"] != dependency_authority["content_digest"]:
        _fail("evaluator receipt changes its bounded transitive dependency authority")
    if evaluator["counterbalanced_seed_digest"] != canonical_digest(
        [expected_common_input, "counterbalanced-v1"]
    ):
        _fail("evaluator counterbalancing seed is not common-input bound")
    if evaluator["receipt_id"] != stable_identifier(
        "abstraction-evaluator-receipt",
        expected_common_input,
        RUBRIC_DIGEST,
        expected_executable,
        dependency_authority["content_digest"],
    ):
        _fail("evaluator receipt identity is not executable/input bound")
    if (
        evaluator["authority_class"] != "internal_protocol_calibration"
        or evaluator["conceptual_value_authorized"] is not False
        or evaluator["physics_value_authorized"] is not False
    ):
        _fail("internal calibration cannot acquire conceptual or physics-value authority")
    if evaluator["external_human"] != {
        "status": "unavailable",
        "reason": "No authenticated external-human evaluation was supplied for this run.",
        "fabricated": False,
        "receipt_id": None,
    }:
        _fail("external-human evidence must remain the exact typed unavailable value")
    expected_task_clusters = _build_task_clusters(outputs, cases)
    if packet["task_clustered_reporting"] != expected_task_clusters:
        _fail("task-clustered held-out reporting was not exactly recomputed")
    if (
        expected_task_clusters["iid_assumption"] is not False
        or expected_task_clusters["population_inference_authorized"] is not False
    ):
        _fail("deterministic reruns cannot acquire IID or population authority")
    expected_controls = _summarize_negative_controls(outputs)
    if packet["negative_control_outcomes"] != expected_controls:
        _fail("report-level negative-control outcomes differ from sealed executions")
    if {row["control_kind"] for row in expected_controls} != {"decorative", "restatement", "sham"}:
        _fail("all three abstraction negative-control families are mandatory")
    if any(not row["all_zero"] for row in expected_controls):
        _fail("a negative-control family received structural credit")
    expected_aggregates = _build_aggregates(
        outputs, attempts, repetitions, expected_task_clusters, cases
    )
    if packet["aggregates"] != expected_aggregates:
        _fail("aggregate repeatability, task clusters, failures, or refinement gate were not recomputed")
    if packet["minimum_retained_repetitions_per_arm"] != min(row["n_completed"] for row in expected_aggregates):
        _fail("minimum retained repetition summary mismatch")
    calibration = _calibration_summary(expected_aggregates)
    if packet["minimum_matched_repetitions_per_arm"] != calibration["minimum_matched_repetitions_per_arm"]:
        _fail("minimum exact matched-repetition summary mismatch")
    if packet["calibration_status"] != calibration["calibration_status"]:
        _fail("full-factorial calibration status was not derived from exact pairs")
    partial = packet["partial_failure"]
    precommitted = partial["precommitted_failures"]
    if len({(row["arm"], row["repetition"]) for row in precommitted}) != len(precommitted):
        _fail("precommitted failure cells are not unique")
    for row in precommitted:
        cell = expected_cell_map.get(row["branch_id"])
        if cell is None or (row["arm"], row["repetition"]) != (
            cell["arm"], cell["repetition"]
        ):
            _fail("precommitted failure does not identify an exact scheduled cell")
        if runtime_receipts.get(row["branch_id"], {}).get("status") != row["status"]:
            _fail("precommitted failure status differs from its runtime receipt")
        if row["status"] not in {"failed", "timeout", "invalid"}:
            _fail("precommitted failure receipt is not a real failed execution")
    actual_failed = {
        row["branch_id"] for row in attempts if row["status"] != "completed"
    }
    declared_failed = {row["branch_id"] for row in precommitted}
    if partial["unexpected_failure_branch_ids"] != sorted(actual_failed - declared_failed):
        _fail("unexpected failure branch IDs are not an exact runtime projection")
    if partial["retained_completed_branch_ids"] != sorted(completed_ids):
        _fail("partial-failure ledger did not preserve every completed sibling")
    if partial["minimum_completed_per_arm"] != min(
        row["n_completed"] for row in expected_aggregates
    ):
        _fail("partial-failure retained-count summary mismatch")
    if partial["insufficient_calibration_arms"] != calibration["insufficient_calibration_arms"]:
        _fail("partial-failure insufficiency was not derived from exact matched pairs")
    if packet["dissent"]["retained_dissent_branch_ids"] != runtime["merge_proposal"]["retained_dissent_ids"]:
        _fail("dissent IDs differ from the conflict-preserving runtime merge")
    if packet["dissent"]["contradiction_edges"] != runtime["merge_proposal"]["contradiction_edges"]:
        _fail("contradiction edges differ from the runtime merge")
    expected_authority = {
        "status": "internal_calibration_refinement_only",
        "calibration_status": calibration["calibration_status"],
        "full_factorial_refinement_eligible": (
            calibration["calibration_status"] == "sufficient_internal_calibration"
            and all(
                row["internal_refinement_eligible"]
                for row in expected_aggregates
                if row["arm"] in {"categorical", "hott", "combined"}
            )
        ),
        "investment_authorized": False,
        "conceptual_value_authorized": False,
        "physics_value_authorized": False,
        "reason": (
            "Worker profiles precommit the structural cardinalities later counted by the "
            "internal evaluator; task-clustered repeatability may guide refinement, but "
            "cannot establish conceptual or physical value or authorize investment."
        ),
    }
    if packet["decision_authority"] != expected_authority:
        _fail("decision authority must remain internal calibration/refinement only")
    if packet["authority_boundary"] != AUTHORITY_BOUNDARY:
        _fail("evaluation authority boundary was altered")
    return {
        "status": "valid",
        "evaluation_id": packet["evaluation_id"],
        "case_suite_id": packet["case_suite_id"],
        "completed_outputs": len(outputs),
        "minimum_retained_repetitions_per_arm": packet["minimum_retained_repetitions_per_arm"],
        "minimum_matched_repetitions_per_arm": packet["minimum_matched_repetitions_per_arm"],
        "calibration_status": packet["calibration_status"],
        "insufficient_calibration_arms": partial["insufficient_calibration_arms"],
        "dissent_count": len(packet["dissent"]["retained_dissent_branch_ids"]),
        "external_human_status": "unavailable",
        "investment_authorized": False,
    }


__all__ = [
    "ARMS",
    "AbstractionEvaluationError",
    "blinded_structural_projection",
    "blinded_structural_score",
    "run_abstraction_parallel_evaluation",
    "validate_abstraction_evaluation_failure_evidence",
    "validate_abstraction_parallel_evaluation",
]
