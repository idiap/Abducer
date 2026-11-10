# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Governed symbolic and simulation producers for descendant experiment worlds.

This module fills the executable layer between a theory-authored discriminating
question and the existing world-v3 storage chronology.  It deliberately does
not commit a theory, choose a preferred programme, authorize proof, or construct
the N+1..N+8 content graph.  Its narrower contract is:

* freeze one typed question, its dimensional/domain assumptions, and two exact
  worker specifications before launch;
* execute symbolic transition checking and a bounded recurrence simulation in
  separate ResourceGovernor-v2 process groups;
* retain bounded, self-digested terminal receipts even when one worker fails;
* reduce successful semantic outputs in a fixed order independent of process
  completion order; and
* return only immutable negative knowledge and a candidate request for the
  later N+8 reflective consumer.

The production facade and replay validator are intentionally different entry
points.  :func:`run_descendant_support_process_wave` is the only function here
that launches workers.  :func:`validate_descendant_support_process_execution`
recomputes semantics from already captured bytes and never starts a process.
The caller must still translate a validated result into role-correct
``GraphStageProduct`` objects and pass those through the canonical world-v3
facade.  This separation prevents a process receipt from acquiring storage or
same-cycle scientific authority merely because it is operationally complete.
"""

from __future__ import annotations

import copy
import json
import os
import re
import sys
from collections.abc import Mapping, Sequence
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


# ``python -I`` removes the repository and its locked environment from the
# import path.  The worker restores only these two explicit locations before
# importing shared contracts; no ambient PYTHONPATH is inherited.
_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
_LOCKED_SITE_PACKAGES = (
    _REPOSITORY_ROOT
    / ".venv"
    / "lib"
    / f"python{sys.version_info.major}.{sys.version_info.minor}"
    / "site-packages"
)
if _LOCKED_SITE_PACKAGES.is_dir() and str(_LOCKED_SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(_LOCKED_SITE_PACKAGES))
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from agentic.discovery.budgets import (  # noqa: E402
    ResourceBudget,
    ResourceGovernor,
    minimal_replacement_environment,
)
from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_identifier,
)


CONTRACT_VERSION = "descendant-support-process/1.0.0"
WORKER_RESPONSE_VERSION = "descendant-support-worker-response/1.0.0"
WORKER_IDS = ("symbolic_transition_trace", "bounded_simulation")
MAX_WORKER_INPUT_BYTES = 128 * 1024
MAX_WORKER_OUTPUT_BYTES = 128 * 1024
MAX_WORKER_STDERR_BYTES = 16 * 1024
MAX_SYMBOLIC_TRANSITIONS = 64
MAX_SIMULATION_TRAJECTORIES = 16
MAX_SIMULATION_STEPS = 64

_DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}")
_NUMBER_RE = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*|\\.[0-9]+)?")
_AUTHORITY_NULLS = {
    "current_theory_mutation_authorized": False,
    "theory_selection_authorized": False,
    "preference_effect_authorized": False,
    "proof_authorized": False,
    "schedule_mutation_authorized": False,
    "physics_authority": False,
    "truth_authority": False,
    "experiment_value_authority": False,
    "hard_host_isolation_authority": False,
    "worker_cognitive_independence_authority": False,
    "worker_semantic_independence_authority": False,
}
_REDUCTION_POLICY = {
    "policy_id": "symbolic-precedence-then-bounded-simulation-v1",
    "misleading_positive_rule": (
        "simulation scoped support plus symbolic premise falsification is "
        "retained as a rejected misleading positive"
    ),
    "falsifier_rule": (
        "a scoped falsifier requests later reflection only after the complete "
        "descendant chronology"
    ),
    "inconclusive_rule": (
        "partial coverage, mixed trajectories, or domain escape cannot support "
        "or falsify the registered premise"
    ),
}


class DescendantProcessContractError(ContractError):
    """Reject malformed, tampered, or authority-inflated descendant evidence."""


@dataclass(frozen=True, slots=True)
class DescendantSupportProcessExecution:
    """Frozen canonical bytes for one completed or no-probe process wave."""

    request_digest: str
    packet_digest: str
    _canonical_packet: bytes

    def as_dict(self) -> dict[str, Any]:
        """Return a detached JSON projection; mutation cannot alter this receipt."""

        value = json.loads(self._canonical_packet)
        if not isinstance(value, dict):
            raise DescendantProcessContractError(
                "frozen descendant execution is not one JSON object"
            )
        return value


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise DescendantProcessContractError(f"{label} must be an object")
    return copy.deepcopy(dict(value))


def _exact_keys(
    value: Mapping[str, Any], required: set[str], label: str
) -> dict[str, Any]:
    record = _mapping(value, label)
    if set(record) != required:
        missing = sorted(required - set(record))
        extra = sorted(set(record) - required)
        raise DescendantProcessContractError(
            f"{label} shape drifted; missing={missing}, extra={extra}"
        )
    return record


def _digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or _DIGEST_RE.fullmatch(value) is None:
        raise DescendantProcessContractError(f"{label} must be one sha256 digest")
    return value


def _bounded_text(value: Any, label: str, *, maximum: int = 4096) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise DescendantProcessContractError(
            f"{label} must be non-empty and at most {maximum} characters"
        )
    return value


def _fraction(value: Any, label: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise DescendantProcessContractError(
            f"{label} must be an integer or exact decimal/rational string"
        )
    token = str(value)
    if len(token) > 96 or _NUMBER_RE.fullmatch(token) is None:
        raise DescendantProcessContractError(f"{label} is not a bounded exact number")
    try:
        return Fraction(token)
    except (ValueError, ZeroDivisionError) as exc:
        raise DescendantProcessContractError(f"{label} is not a finite rational") from exc


def _fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def _validate_domain(
    raw: Mapping[str, Any],
    *,
    quantity: str | None = None,
    unit: str | None = None,
) -> dict[str, Any]:
    domain = _exact_keys(
        raw,
        {"quantity", "unit", "minimum", "maximum"},
        "domain assumption",
    )
    domain["quantity"] = _bounded_text(
        domain["quantity"], "domain quantity", maximum=128
    )
    domain["unit"] = _bounded_text(domain["unit"], "domain unit", maximum=128)
    if quantity is not None and domain["quantity"] != quantity:
        raise DescendantProcessContractError("domain quantity differs from worker state")
    if unit is not None and domain["unit"] != unit:
        raise DescendantProcessContractError("domain unit differs from worker state")
    minimum = _fraction(domain["minimum"], "domain minimum")
    maximum = _fraction(domain["maximum"], "domain maximum")
    if minimum > maximum:
        raise DescendantProcessContractError("domain minimum exceeds its maximum")
    domain["minimum"] = _fraction_text(minimum)
    domain["maximum"] = _fraction_text(maximum)
    return domain


def _inside(value: Fraction, domain: Mapping[str, Any]) -> bool:
    return (
        _fraction(domain["minimum"], "domain minimum")
        <= value
        <= _fraction(domain["maximum"], "domain maximum")
    )


def _validate_authorship(
    raw: Mapping[str, Any], *, theory_generation: int
) -> dict[str, Any]:
    authorship = _exact_keys(
        raw,
        {
            "producer_role",
            "source_theory_generation",
            "source_theory_programme_digest",
            "source_reflection_digest",
            "author_receipt_digest",
            "authored_before_worker_launch",
        },
        "question authorship",
    )
    if (
        authorship["producer_role"] != "committed_theory_reflection"
        or authorship["source_theory_generation"] != theory_generation
        or authorship["authored_before_worker_launch"] is not True
    ):
        raise DescendantProcessContractError(
            "discriminating question lacks prelaunch committed-theory authorship"
        )
    for field in (
        "source_theory_programme_digest",
        "source_reflection_digest",
        "author_receipt_digest",
    ):
        authorship[field] = _digest(authorship[field], f"authorship {field}")
    return authorship


def _validate_question(
    raw: Mapping[str, Any], *, theory_generation: int
) -> dict[str, Any]:
    question = _exact_keys(
        raw,
        {
            "question_id",
            "statement",
            "tested_premise_id",
            "tested_premise_digest",
            "support_interpretation",
            "falsifier_interpretation",
            "domain_assumptions",
            "discriminating_rule",
            "authorship",
        },
        "discriminating question",
    )
    validate_identifier(str(question["question_id"]), "question_id")
    validate_identifier(str(question["tested_premise_id"]), "tested_premise_id")
    question["statement"] = _bounded_text(
        question["statement"], "question statement"
    )
    question["support_interpretation"] = _bounded_text(
        question["support_interpretation"], "support interpretation"
    )
    question["falsifier_interpretation"] = _bounded_text(
        question["falsifier_interpretation"], "falsifier interpretation"
    )
    question["tested_premise_digest"] = _digest(
        question["tested_premise_digest"], "tested premise digest"
    )
    if question["discriminating_rule"] != _REDUCTION_POLICY:
        raise DescendantProcessContractError(
            "question discriminating rule differs from deterministic reduction"
        )
    domains = question["domain_assumptions"]
    if (
        not isinstance(domains, list)
        or len(domains) != 1
        or not isinstance(domains[0], Mapping)
    ):
        raise DescendantProcessContractError(
            "question requires exactly one explicit state domain"
        )
    question["domain_assumptions"] = [_validate_domain(domains[0])]
    question["authorship"] = _validate_authorship(
        question["authorship"], theory_generation=theory_generation
    )
    return question


def _validate_symbolic_spec(raw: Mapping[str, Any]) -> dict[str, Any]:
    spec = _exact_keys(
        raw,
        {
            "worker_kind",
            "state_quantity",
            "state_unit",
            "initial_value",
            "domain",
            "coverage",
            "transitions",
        },
        "symbolic transition specification",
    )
    if spec["worker_kind"] != "symbolic_transition_trace":
        raise DescendantProcessContractError("symbolic worker kind is invalid")
    quantity = _bounded_text(
        spec["state_quantity"], "symbolic state quantity", maximum=128
    )
    unit = _bounded_text(spec["state_unit"], "symbolic state unit", maximum=128)
    spec["state_quantity"] = quantity
    spec["state_unit"] = unit
    spec["domain"] = _validate_domain(
        spec["domain"], quantity=quantity, unit=unit
    )
    initial = _fraction(spec["initial_value"], "symbolic initial value")
    if not _inside(initial, spec["domain"]):
        raise DescendantProcessContractError(
            "symbolic initial value lies outside its declared domain"
        )
    spec["initial_value"] = _fraction_text(initial)
    if spec["coverage"] not in {"complete", "bounded_partial"}:
        raise DescendantProcessContractError("symbolic coverage is invalid")
    transitions = spec["transitions"]
    if (
        not isinstance(transitions, list)
        or not transitions
        or len(transitions) > MAX_SYMBOLIC_TRANSITIONS
    ):
        raise DescendantProcessContractError(
            "symbolic transitions must be a non-empty bounded list"
        )
    normalized: list[dict[str, Any]] = []
    expected_input = initial
    seen: set[str] = set()
    for index, raw_transition in enumerate(transitions):
        transition = _exact_keys(
            raw_transition,
            {"step_id", "input", "multiplier", "offset", "claimed_output"},
            f"symbolic transition {index}",
        )
        validate_identifier(str(transition["step_id"]), "symbolic step_id")
        if transition["step_id"] in seen:
            raise DescendantProcessContractError("symbolic step IDs repeat")
        seen.add(str(transition["step_id"]))
        input_value = _fraction(transition["input"], "symbolic transition input")
        if input_value != expected_input:
            raise DescendantProcessContractError(
                "symbolic transition inputs do not form one frozen trace"
            )
        multiplier = _fraction(
            transition["multiplier"], "symbolic transition multiplier"
        )
        offset = _fraction(transition["offset"], "symbolic transition offset")
        claimed = _fraction(
            transition["claimed_output"], "symbolic claimed output"
        )
        normalized.append(
            {
                "step_id": str(transition["step_id"]),
                "input": _fraction_text(input_value),
                "multiplier": _fraction_text(multiplier),
                "offset": _fraction_text(offset),
                "claimed_output": _fraction_text(claimed),
            }
        )
        expected_input = claimed
    spec["transitions"] = normalized
    return spec


def _validate_simulation_spec(raw: Mapping[str, Any]) -> dict[str, Any]:
    spec = _exact_keys(
        raw,
        {
            "worker_kind",
            "state_quantity",
            "state_unit",
            "step_unit",
            "domain",
            "initial_values",
            "recurrence",
            "steps",
            "acceptance",
            "sample_policy",
            "seed_policy",
        },
        "bounded simulation specification",
    )
    if spec["worker_kind"] != "bounded_simulation":
        raise DescendantProcessContractError("simulation worker kind is invalid")
    quantity = _bounded_text(
        spec["state_quantity"], "simulation state quantity", maximum=128
    )
    unit = _bounded_text(spec["state_unit"], "simulation state unit", maximum=128)
    spec["state_quantity"] = quantity
    spec["state_unit"] = unit
    spec["step_unit"] = _bounded_text(
        spec["step_unit"], "simulation step unit", maximum=128
    )
    spec["domain"] = _validate_domain(
        spec["domain"], quantity=quantity, unit=unit
    )
    values = spec["initial_values"]
    if (
        not isinstance(values, list)
        or not values
        or len(values) > MAX_SIMULATION_TRAJECTORIES
    ):
        raise DescendantProcessContractError(
            "simulation initial values must be a non-empty bounded ensemble"
        )
    normalized_values: list[str] = []
    for index, value in enumerate(values):
        parsed = _fraction(value, f"simulation initial value {index}")
        if not _inside(parsed, spec["domain"]):
            raise DescendantProcessContractError(
                "simulation initial value lies outside its declared domain"
            )
        normalized_values.append(_fraction_text(parsed))
    spec["initial_values"] = normalized_values
    recurrence = _exact_keys(
        spec["recurrence"],
        {"multiplier", "offset"},
        "simulation recurrence",
    )
    spec["recurrence"] = {
        "multiplier": _fraction_text(
            _fraction(recurrence["multiplier"], "simulation multiplier")
        ),
        "offset": _fraction_text(
            _fraction(recurrence["offset"], "simulation offset")
        ),
    }
    if (
        isinstance(spec["steps"], bool)
        or not isinstance(spec["steps"], int)
        or not 1 <= spec["steps"] <= MAX_SIMULATION_STEPS
    ):
        raise DescendantProcessContractError("simulation step count is out of bounds")
    acceptance = _exact_keys(
        spec["acceptance"],
        {"comparator", "threshold"},
        "simulation acceptance rule",
    )
    if acceptance["comparator"] not in {"<", "<=", "==", ">=", ">"}:
        raise DescendantProcessContractError("simulation comparator is invalid")
    spec["acceptance"] = {
        "comparator": acceptance["comparator"],
        "threshold": _fraction_text(
            _fraction(acceptance["threshold"], "simulation threshold")
        ),
    }
    if spec["sample_policy"] != "deterministic_declared_initial_ensemble":
        raise DescendantProcessContractError("simulation sample policy is invalid")
    if spec["seed_policy"] != {"stochastic": False, "seed": None}:
        raise DescendantProcessContractError(
            "bounded recurrence simulation must be deterministically seeded"
        )
    return spec


def _normalize_budget(raw: Mapping[str, Any], worker_id: str) -> dict[str, Any]:
    budget = ResourceBudget.from_mapping(raw)
    normalized = asdict(budget)
    if normalized["budget_id"] != f"descendant-{worker_id}":
        raise DescendantProcessContractError(
            f"{worker_id} budget has the wrong immutable budget ID"
        )
    if (
        normalized["network_bytes"] != 0
        or normalized["token_count"] != 0
        or normalized["request_count"] != 0
        or normalized["cost_usd"] != 0.0
    ):
        raise DescendantProcessContractError(
            "local descendant workers require zero remote-resource allowances"
        )
    return normalized


def build_theory_authored_descendant_experiment_request(
    *,
    target_id: str,
    run_id: str,
    branch_id: str,
    theory_generation: int,
    question_id: str,
    question_statement: str,
    tested_premise_id: str,
    tested_premise_digest: str,
    support_interpretation: str,
    falsifier_interpretation: str,
    domain_assumption: Mapping[str, Any],
    source_theory_programme_digest: str,
    source_reflection_digest: str,
    author_receipt_digest: str,
    route_decision: str,
    symbolic_spec: Mapping[str, Any] | None = None,
    simulation_spec: Mapping[str, Any] | None = None,
    resource_budgets: Mapping[str, Mapping[str, Any]] | None = None,
    stdout_limits: Mapping[str, int] | None = None,
) -> dict[str, Any]:
    """Freeze one question and its exact process inputs before any worker launch."""

    validate_identifier(target_id, "target_id")
    validate_identifier(run_id, "run_id")
    validate_identifier(branch_id, "branch_id")
    if (
        isinstance(theory_generation, bool)
        or not isinstance(theory_generation, int)
        or theory_generation < 0
    ):
        raise DescendantProcessContractError(
            "theory_generation must be a non-negative integer"
        )
    if route_decision not in {"commission", "no_probe"}:
        raise DescendantProcessContractError("route decision must commission or no_probe")
    question = {
        "question_id": question_id,
        "statement": question_statement,
        "tested_premise_id": tested_premise_id,
        "tested_premise_digest": tested_premise_digest,
        "support_interpretation": support_interpretation,
        "falsifier_interpretation": falsifier_interpretation,
        "domain_assumptions": [copy.deepcopy(dict(domain_assumption))],
        "discriminating_rule": copy.deepcopy(_REDUCTION_POLICY),
        "authorship": {
            "producer_role": "committed_theory_reflection",
            "source_theory_generation": theory_generation,
            "source_theory_programme_digest": source_theory_programme_digest,
            "source_reflection_digest": source_reflection_digest,
            "author_receipt_digest": author_receipt_digest,
            "authored_before_worker_launch": True,
        },
    }
    normalized_question = _validate_question(
        question, theory_generation=theory_generation
    )
    if route_decision == "no_probe":
        if any(
            value is not None
            for value in (symbolic_spec, simulation_spec, resource_budgets, stdout_limits)
        ):
            raise DescendantProcessContractError(
                "no_probe cannot carry executable worker inputs"
            )
        worker_specs: dict[str, Any] = {}
        budgets: dict[str, Any] = {}
        limits: dict[str, int] = {}
    else:
        if symbolic_spec is None or simulation_spec is None or resource_budgets is None:
            raise DescendantProcessContractError(
                "commission requires symbolic, simulation, and resource inputs"
            )
        if set(resource_budgets) != set(WORKER_IDS):
            raise DescendantProcessContractError(
                "commission requires one independent budget per worker"
            )
        worker_specs = {
            "symbolic_transition_trace": _validate_symbolic_spec(symbolic_spec),
            "bounded_simulation": _validate_simulation_spec(simulation_spec),
        }
        question_domain = normalized_question["domain_assumptions"][0]
        for worker_id in WORKER_IDS:
            if worker_specs[worker_id]["domain"] != question_domain:
                raise DescendantProcessContractError(
                    f"{worker_id} domain differs from the theory-authored question"
                )
        budgets = {
            worker_id: _normalize_budget(resource_budgets[worker_id], worker_id)
            for worker_id in WORKER_IDS
        }
        raw_limits = (
            {worker_id: MAX_WORKER_OUTPUT_BYTES for worker_id in WORKER_IDS}
            if stdout_limits is None
            else dict(stdout_limits)
        )
        if set(raw_limits) != set(WORKER_IDS):
            raise DescendantProcessContractError(
                "commission requires one stdout ceiling per worker"
            )
        limits = {}
        for worker_id, value in raw_limits.items():
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or not 64 <= value <= MAX_WORKER_OUTPUT_BYTES
            ):
                raise DescendantProcessContractError(
                    f"{worker_id} stdout ceiling is out of bounds"
                )
            limits[worker_id] = value
    request: dict[str, Any] = {
        "schema_version": 1,
        "contract_version": CONTRACT_VERSION,
        "message_kind": "theory_authored_descendant_experiment_request",
        "target_id": target_id,
        "run_id": run_id,
        "branch_id": branch_id,
        "theory_generation": theory_generation,
        "route_decision": route_decision,
        "question": normalized_question,
        "worker_specs": worker_specs,
        "resource_budgets": budgets,
        "execution_policy": {
            "worker_order": list(WORKER_IDS),
            "process_boundary": "resource_governor_v2_isolated_process_group",
            "replacement_environment_required": True,
            "stdin_limit_bytes": MAX_WORKER_INPUT_BYTES,
            "stdout_limit_bytes": limits,
            "stderr_limit_bytes": MAX_WORKER_STDERR_BYTES,
            "max_symbolic_transitions": MAX_SYMBOLIC_TRANSITIONS,
            "max_simulation_trajectories": MAX_SIMULATION_TRAJECTORIES,
            "max_simulation_steps": MAX_SIMULATION_STEPS,
            "late_write_policy": "reject_worker_directory_change_or_live_descendant",
            "reduction_order": list(WORKER_IDS),
        },
        "required_descendant_chronology": {
            "theory_generation_offset": 0,
            "support_anchor_offset": 1,
            "world_offsets": [2, 3, 4, 5, 6],
            "aggregation_offset": 7,
            "later_reflection_offset": 8,
        },
        "authority_nulls": copy.deepcopy(_AUTHORITY_NULLS),
    }
    request["request_id"] = stable_identifier(
        "descendant-process-request",
        target_id,
        run_id,
        branch_id,
        theory_generation,
        question_id,
        canonical_digest(worker_specs),
    )
    request["content_digest"] = canonical_digest(request)
    return validate_theory_authored_descendant_experiment_request(request)


def validate_theory_authored_descendant_experiment_request(
    raw: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay the complete prelaunch request contract without executing it."""

    request = _exact_keys(
        raw,
        {
            "schema_version",
            "contract_version",
            "message_kind",
            "target_id",
            "run_id",
            "branch_id",
            "theory_generation",
            "route_decision",
            "question",
            "worker_specs",
            "resource_budgets",
            "execution_policy",
            "required_descendant_chronology",
            "authority_nulls",
            "request_id",
            "content_digest",
        },
        "descendant process request",
    )
    for field in ("target_id", "run_id", "branch_id", "request_id"):
        validate_identifier(str(request[field]), field)
    theory_generation = request["theory_generation"]
    if (
        request["schema_version"] != 1
        or request["contract_version"] != CONTRACT_VERSION
        or request["message_kind"]
        != "theory_authored_descendant_experiment_request"
        or isinstance(theory_generation, bool)
        or not isinstance(theory_generation, int)
        or theory_generation < 0
        or request["route_decision"] not in {"commission", "no_probe"}
        or request["authority_nulls"] != _AUTHORITY_NULLS
        or request["required_descendant_chronology"]
        != {
            "theory_generation_offset": 0,
            "support_anchor_offset": 1,
            "world_offsets": [2, 3, 4, 5, 6],
            "aggregation_offset": 7,
            "later_reflection_offset": 8,
        }
        or request["content_digest"]
        != canonical_digest(
            {
                key: value
                for key, value in request.items()
                if key != "content_digest"
            }
        )
    ):
        raise DescendantProcessContractError(
            "descendant request constants, chronology, authority, or digest drifted"
        )
    request["question"] = _validate_question(
        request["question"], theory_generation=theory_generation
    )
    policy = _mapping(request["execution_policy"], "execution policy")
    expected_static_policy = {
        "worker_order": list(WORKER_IDS),
        "process_boundary": "resource_governor_v2_isolated_process_group",
        "replacement_environment_required": True,
        "stdin_limit_bytes": MAX_WORKER_INPUT_BYTES,
        "stderr_limit_bytes": MAX_WORKER_STDERR_BYTES,
        "max_symbolic_transitions": MAX_SYMBOLIC_TRANSITIONS,
        "max_simulation_trajectories": MAX_SIMULATION_TRAJECTORIES,
        "max_simulation_steps": MAX_SIMULATION_STEPS,
        "late_write_policy": "reject_worker_directory_change_or_live_descendant",
        "reduction_order": list(WORKER_IDS),
    }
    limits = policy.pop("stdout_limit_bytes", None)
    if policy != expected_static_policy:
        raise DescendantProcessContractError("descendant execution policy drifted")
    if request["route_decision"] == "no_probe":
        if request["worker_specs"] != {} or request["resource_budgets"] != {} or limits != {}:
            raise DescendantProcessContractError(
                "no_probe request carries executable state"
            )
    else:
        if (
            not isinstance(request["worker_specs"], Mapping)
            or set(request["worker_specs"]) != set(WORKER_IDS)
            or not isinstance(request["resource_budgets"], Mapping)
            or set(request["resource_budgets"]) != set(WORKER_IDS)
            or not isinstance(limits, Mapping)
            or set(limits) != set(WORKER_IDS)
        ):
            raise DescendantProcessContractError(
                "commission worker, budget, or output cardinality drifted"
            )
        request["worker_specs"] = {
            "symbolic_transition_trace": _validate_symbolic_spec(
                request["worker_specs"]["symbolic_transition_trace"]
            ),
            "bounded_simulation": _validate_simulation_spec(
                request["worker_specs"]["bounded_simulation"]
            ),
        }
        question_domain = request["question"]["domain_assumptions"][0]
        if any(
            request["worker_specs"][worker_id]["domain"] != question_domain
            for worker_id in WORKER_IDS
        ):
            raise DescendantProcessContractError(
                "worker domains differ from the discriminating question"
            )
        request["resource_budgets"] = {
            worker_id: _normalize_budget(
                request["resource_budgets"][worker_id], worker_id
            )
            for worker_id in WORKER_IDS
        }
        for worker_id, value in limits.items():
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or not 64 <= value <= MAX_WORKER_OUTPUT_BYTES
            ):
                raise DescendantProcessContractError(
                    f"{worker_id} stdout ceiling is out of bounds"
                )
    return request


def _worker_envelope(
    request: Mapping[str, Any], worker_id: str
) -> dict[str, Any]:
    envelope: dict[str, Any] = {
        "schema_version": 1,
        "contract_version": CONTRACT_VERSION,
        "message_kind": "descendant_support_worker_request",
        "worker_id": worker_id,
        "request_id": request["request_id"],
        "request_digest": request["content_digest"],
        "question": copy.deepcopy(request["question"]),
        "worker_spec": copy.deepcopy(request["worker_specs"][worker_id]),
        "authority_nulls": copy.deepcopy(_AUTHORITY_NULLS),
    }
    envelope["content_digest"] = canonical_digest(envelope)
    return envelope


def _validate_worker_envelope(raw: Mapping[str, Any], worker_id: str) -> dict[str, Any]:
    envelope = _exact_keys(
        raw,
        {
            "schema_version",
            "contract_version",
            "message_kind",
            "worker_id",
            "request_id",
            "request_digest",
            "question",
            "worker_spec",
            "authority_nulls",
            "content_digest",
        },
        "descendant worker envelope",
    )
    if (
        envelope["schema_version"] != 1
        or envelope["contract_version"] != CONTRACT_VERSION
        or envelope["message_kind"] != "descendant_support_worker_request"
        or envelope["worker_id"] != worker_id
        or envelope["authority_nulls"] != _AUTHORITY_NULLS
        or envelope["content_digest"]
        != canonical_digest(
            {
                key: value
                for key, value in envelope.items()
                if key != "content_digest"
            }
        )
    ):
        raise DescendantProcessContractError(
            "descendant worker envelope identity or digest drifted"
        )
    validate_identifier(str(envelope["request_id"]), "request_id")
    _digest(envelope["request_digest"], "worker request digest")
    authorship = _mapping(envelope["question"], "worker question").get(
        "authorship", {}
    )
    theory_generation = authorship.get("source_theory_generation")
    if not isinstance(theory_generation, int):
        raise DescendantProcessContractError(
            "worker question lacks source theory generation"
        )
    envelope["question"] = _validate_question(
        envelope["question"], theory_generation=theory_generation
    )
    envelope["worker_spec"] = (
        _validate_symbolic_spec(envelope["worker_spec"])
        if worker_id == "symbolic_transition_trace"
        else _validate_simulation_spec(envelope["worker_spec"])
    )
    if envelope["worker_spec"]["domain"] != envelope["question"]["domain_assumptions"][0]:
        raise DescendantProcessContractError(
            "worker envelope changed the theory-authored domain"
        )
    return envelope


def _execute_symbolic(spec: Mapping[str, Any]) -> dict[str, Any]:
    trace: list[dict[str, Any]] = []
    mismatches: list[str] = []
    domain_violations: list[str] = []
    for transition in spec["transitions"]:
        input_value = _fraction(transition["input"], "symbolic input")
        actual = (
            _fraction(transition["multiplier"], "symbolic multiplier") * input_value
            + _fraction(transition["offset"], "symbolic offset")
        )
        claimed = _fraction(transition["claimed_output"], "symbolic claimed output")
        equation_holds = actual == claimed
        domain_holds = _inside(input_value, spec["domain"]) and _inside(
            actual, spec["domain"]
        )
        if not equation_holds:
            mismatches.append(str(transition["step_id"]))
        if not domain_holds:
            domain_violations.append(str(transition["step_id"]))
        trace.append(
            {
                "step_id": transition["step_id"],
                "equation": (
                    f"{transition['multiplier']}*{transition['input']}"
                    f"+{transition['offset']}={_fraction_text(actual)}"
                ),
                "claimed_output": transition["claimed_output"],
                "actual_output": _fraction_text(actual),
                "equation_holds": equation_holds,
                "domain_holds": domain_holds,
                "unit": spec["state_unit"],
            }
        )
    if mismatches:
        outcome = "premise_falsifier"
    elif domain_violations or spec["coverage"] == "bounded_partial":
        outcome = "inconclusive"
    else:
        outcome = "scoped_support"
    result: dict[str, Any] = {
        "worker_kind": "symbolic_transition_trace",
        "epistemic_outcome": outcome,
        "trace": trace,
        "mismatching_step_ids": mismatches,
        "domain_violation_step_ids": domain_violations,
        "coverage": spec["coverage"],
        "domain": copy.deepcopy(spec["domain"]),
        "scope_boundary": (
            "exact rational transition replay in the declared finite trace only"
        ),
    }
    result["result_digest"] = canonical_digest(result)
    return result


def _compare(left: Fraction, comparator: str, right: Fraction) -> bool:
    return {
        "<": left < right,
        "<=": left <= right,
        "==": left == right,
        ">=": left >= right,
        ">": left > right,
    }[comparator]


def _execute_simulation(spec: Mapping[str, Any]) -> dict[str, Any]:
    multiplier = _fraction(spec["recurrence"]["multiplier"], "simulation multiplier")
    offset = _fraction(spec["recurrence"]["offset"], "simulation offset")
    threshold = _fraction(spec["acceptance"]["threshold"], "simulation threshold")
    comparator = str(spec["acceptance"]["comparator"])
    trajectories: list[dict[str, Any]] = []
    accepted = 0
    escaped = 0
    for ordinal, initial_token in enumerate(spec["initial_values"]):
        value = _fraction(initial_token, "simulation initial value")
        trace = [_fraction_text(value)]
        first_escape: int | None = None
        for step in range(1, int(spec["steps"]) + 1):
            value = multiplier * value + offset
            trace.append(_fraction_text(value))
            if first_escape is None and not _inside(value, spec["domain"]):
                first_escape = step
        accepted_here = first_escape is None and _compare(
            value, comparator, threshold
        )
        accepted += int(accepted_here)
        escaped += int(first_escape is not None)
        trajectories.append(
            {
                "trajectory_ordinal": ordinal,
                "initial_value": initial_token,
                "state_trace": trace,
                "terminal_value": _fraction_text(value),
                "first_domain_escape_step": first_escape,
                "acceptance_holds": accepted_here,
                "state_unit": spec["state_unit"],
                "step_unit": spec["step_unit"],
            }
        )
    total = len(trajectories)
    if escaped:
        outcome = "inconclusive"
    elif accepted == total:
        outcome = "scoped_support"
    elif accepted == 0:
        outcome = "premise_falsifier"
    else:
        outcome = "inconclusive"
    result: dict[str, Any] = {
        "worker_kind": "bounded_simulation",
        "epistemic_outcome": outcome,
        "trajectories": trajectories,
        "accepted_trajectory_count": accepted,
        "domain_escape_count": escaped,
        "trajectory_count": total,
        "steps": spec["steps"],
        "acceptance": copy.deepcopy(spec["acceptance"]),
        "domain": copy.deepcopy(spec["domain"]),
        "scope_boundary": (
            "deterministic finite recurrence over the declared initial ensemble only"
        ),
    }
    result["result_digest"] = canonical_digest(result)
    return result


def _execute_worker(envelope: Mapping[str, Any], worker_id: str) -> dict[str, Any]:
    request = _validate_worker_envelope(envelope, worker_id)
    output = (
        _execute_symbolic(request["worker_spec"])
        if worker_id == "symbolic_transition_trace"
        else _execute_simulation(request["worker_spec"])
    )
    response: dict[str, Any] = {
        "schema_version": 1,
        "contract_version": WORKER_RESPONSE_VERSION,
        "message_kind": "descendant_support_worker_response",
        "worker_id": worker_id,
        "request_id": request["request_id"],
        "request_digest": request["request_digest"],
        "worker_request_digest": request["content_digest"],
        "output": output,
        "output_digest": canonical_digest(output),
        "authority_nulls": copy.deepcopy(_AUTHORITY_NULLS),
    }
    response["content_digest"] = canonical_digest(response)
    return response


def _validate_worker_response(
    raw: Mapping[str, Any],
    *,
    envelope: Mapping[str, Any],
    worker_id: str,
) -> dict[str, Any]:
    response = _exact_keys(
        raw,
        {
            "schema_version",
            "contract_version",
            "message_kind",
            "worker_id",
            "request_id",
            "request_digest",
            "worker_request_digest",
            "output",
            "output_digest",
            "authority_nulls",
            "content_digest",
        },
        "descendant worker response",
    )
    expected_output = _execute_worker(envelope, worker_id)["output"]
    if (
        response["schema_version"] != 1
        or response["contract_version"] != WORKER_RESPONSE_VERSION
        or response["message_kind"] != "descendant_support_worker_response"
        or response["worker_id"] != worker_id
        or response["request_id"] != envelope["request_id"]
        or response["request_digest"] != envelope["request_digest"]
        or response["worker_request_digest"] != envelope["content_digest"]
        or response["output"] != expected_output
        or response["output_digest"] != canonical_digest(expected_output)
        or response["authority_nulls"] != _AUTHORITY_NULLS
        or response["content_digest"]
        != canonical_digest(
            {
                key: value
                for key, value in response.items()
                if key != "content_digest"
            }
        )
    ):
        raise DescendantProcessContractError(
            "descendant worker response failed semantic replay"
        )
    return response


def _regular_file_snapshot(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        metadata = path.lstat()
        if path.is_symlink():
            raise DescendantProcessContractError(
                "worker directory contains a symbolic link"
            )
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            snapshot[relative] = bytes_digest(path.read_bytes())
        elif not path.is_dir():
            raise DescendantProcessContractError(
                "worker directory contains a non-regular filesystem entry"
            )
    return snapshot


def _bounded_reason(value: str) -> str:
    return " ".join(value.replace("\x00", " ").split())[:512]


def _terminal_receipt(
    *,
    request: Mapping[str, Any],
    worker_id: str,
    workspace: Path,
) -> dict[str, Any]:
    worker_root = (workspace / "workers" / worker_id).resolve()
    try:
        worker_root.relative_to(workspace)
    except ValueError as exc:
        raise DescendantProcessContractError(
            "worker directory escaped the execution workspace"
        ) from exc
    worker_root.mkdir(parents=True, exist_ok=True)
    replacement_environment = minimal_replacement_environment(worker_root)
    envelope = _worker_envelope(request, worker_id)
    input_bytes = canonical_json(envelope)
    before = _regular_file_snapshot(worker_root)
    governor = ResourceGovernor.from_mapping(
        request["resource_budgets"][worker_id],
        run_directory=worker_root,
    )
    process_event: Mapping[str, Any] | None = None
    operational_reason: str | None = None
    response: dict[str, Any] | None = None
    try:
        process_event = governor.run_process(
            [
                str(Path(sys.executable).resolve(strict=True)),
                "-I",
                "-B",
                str(Path(__file__).resolve(strict=True)),
                "--worker",
                worker_id,
            ],
            cwd=worker_root,
            replacement_environment=replacement_environment,
            role="worker",
            input_bytes=input_bytes,
            input_limit_bytes=MAX_WORKER_INPUT_BYTES,
            stdout_limit_bytes=request["execution_policy"]["stdout_limit_bytes"][
                worker_id
            ],
            stderr_limit_bytes=MAX_WORKER_STDERR_BYTES,
        )
        after = _regular_file_snapshot(worker_root)
        clean_filesystem = before == after
        process_ok = (
            process_event.get("event_schema_version") == 2
            and process_event.get("status") == "succeeded"
            and process_event.get("returncode") == 0
            and process_event.get("descendant_leak_detected") is False
            and process_event.get("stdout_utf8_valid") is True
            and process_event.get("stdout_drain_incomplete") is False
            and process_event.get("stderr_drain_incomplete") is False
            and process_event.get("post_supervision_acceptance", {}).get("status")
            == "accepted"
            and process_event.get("resource_limit_execution", {}).get(
                "replacement_environment_used"
            )
            is True
            and process_event.get("resource_limit_execution", {}).get(
                "observation_status"
            )
            == "exact_match"
            and clean_filesystem
        )
        if process_ok:
            try:
                decoded = json.loads(str(process_event["stdout"]))
                response = _validate_worker_response(
                    decoded,
                    envelope=envelope,
                    worker_id=worker_id,
                )
            except (
                DescendantProcessContractError,
                json.JSONDecodeError,
                KeyError,
                TypeError,
                ValueError,
            ) as exc:
                operational_reason = _bounded_reason(
                    f"worker_output_validation_failed:{type(exc).__name__}:{exc}"
                )
        else:
            operational_reason = _bounded_reason(
                "process_terminal_rejected:"
                f"{process_event.get('status')}:{process_event.get('termination')}:"
                f"filesystem_unchanged={clean_filesystem}"
            )
    except (OSError, RuntimeError, ValueError) as exc:
        operational_reason = _bounded_reason(
            f"process_supervision_failed:{type(exc).__name__}:{exc}"
        )
    terminal_status = "succeeded" if response is not None else "operational_failure"
    event_digest = (
        canonical_digest(process_event) if process_event is not None else None
    )
    receipt: dict[str, Any] = {
        "schema_version": 1,
        "contract_version": CONTRACT_VERSION,
        "receipt_kind": "descendant_support_process_terminal",
        "worker_id": worker_id,
        "request_id": request["request_id"],
        "request_digest": request["content_digest"],
        "worker_request_digest": envelope["content_digest"],
        "worker_module_digest": bytes_digest(Path(__file__).read_bytes()),
        "resource_budget_digest": canonical_digest(
            request["resource_budgets"][worker_id]
        ),
        "terminal_status": terminal_status,
        "operational_reason": operational_reason,
        "process_event": copy.deepcopy(process_event),
        "process_event_digest": event_digest,
        "worker_response": response,
        "worker_response_digest": (
            response["content_digest"] if response is not None else None
        ),
        "late_write_contained": (
            bool(
                process_event is not None
                and process_event.get("descendant_leak_detected") is False
                and before == _regular_file_snapshot(worker_root)
            )
        ),
        "authority_nulls": copy.deepcopy(_AUTHORITY_NULLS),
    }
    receipt["receipt_id"] = stable_identifier(
        "descendant-terminal",
        request["request_id"],
        worker_id,
        event_digest,
        receipt["worker_response_digest"],
    )
    receipt["receipt_digest"] = canonical_digest(receipt)
    return receipt


def _validate_terminal_receipt(
    raw: Mapping[str, Any],
    *,
    request: Mapping[str, Any],
    worker_id: str,
) -> dict[str, Any]:
    receipt = _exact_keys(
        raw,
        {
            "schema_version",
            "contract_version",
            "receipt_kind",
            "worker_id",
            "request_id",
            "request_digest",
            "worker_request_digest",
            "worker_module_digest",
            "resource_budget_digest",
            "terminal_status",
            "operational_reason",
            "process_event",
            "process_event_digest",
            "worker_response",
            "worker_response_digest",
            "late_write_contained",
            "authority_nulls",
            "receipt_id",
            "receipt_digest",
        },
        "descendant terminal receipt",
    )
    envelope = _worker_envelope(request, worker_id)
    event = receipt["process_event"]
    event_digest = canonical_digest(event) if event is not None else None
    if (
        receipt["schema_version"] != 1
        or receipt["contract_version"] != CONTRACT_VERSION
        or receipt["receipt_kind"] != "descendant_support_process_terminal"
        or receipt["worker_id"] != worker_id
        or receipt["request_id"] != request["request_id"]
        or receipt["request_digest"] != request["content_digest"]
        or receipt["worker_request_digest"] != envelope["content_digest"]
        or receipt["worker_module_digest"]
        != bytes_digest(Path(__file__).read_bytes())
        or receipt["resource_budget_digest"]
        != canonical_digest(request["resource_budgets"][worker_id])
        or receipt["process_event_digest"] != event_digest
        or receipt["authority_nulls"] != _AUTHORITY_NULLS
        or receipt["receipt_id"]
        != stable_identifier(
            "descendant-terminal",
            request["request_id"],
            worker_id,
            event_digest,
            receipt["worker_response_digest"],
        )
        or receipt["receipt_digest"]
        != canonical_digest(
            {
                key: value
                for key, value in receipt.items()
                if key != "receipt_digest"
            }
        )
    ):
        raise DescendantProcessContractError(
            "descendant terminal receipt identity or digest drifted"
        )
    if receipt["terminal_status"] == "succeeded":
        if (
            receipt["operational_reason"] is not None
            or event is None
            or event.get("event_schema_version") != 2
            or event.get("status") != "succeeded"
            or event.get("returncode") != 0
            or event.get("descendant_leak_detected") is not False
            or event.get("resource_limit_execution", {}).get(
                "replacement_environment_used"
            )
            is not True
            or event.get("post_supervision_acceptance", {}).get("status")
            != "accepted"
            or receipt["late_write_contained"] is not True
            or not isinstance(receipt["worker_response"], Mapping)
        ):
            raise DescendantProcessContractError(
                "successful terminal receipt lacks accepted process evidence"
            )
        response = _validate_worker_response(
            receipt["worker_response"],
            envelope=envelope,
            worker_id=worker_id,
        )
        if receipt["worker_response_digest"] != response["content_digest"]:
            raise DescendantProcessContractError(
                "terminal receipt changed the worker response digest"
            )
    elif receipt["terminal_status"] == "operational_failure":
        if (
            not isinstance(receipt["operational_reason"], str)
            or not receipt["operational_reason"]
            or receipt["worker_response"] is not None
            or receipt["worker_response_digest"] is not None
        ):
            raise DescendantProcessContractError(
                "operational terminal receipt has an impossible output state"
            )
    else:
        raise DescendantProcessContractError("terminal receipt status is invalid")
    return receipt


def _negative_knowledge(
    *,
    request: Mapping[str, Any],
    worker_id: str,
    output: Mapping[str, Any],
) -> dict[str, Any]:
    knowledge: dict[str, Any] = {
        "knowledge_kind": "immutable_scoped_negative_observation",
        "source_worker_id": worker_id,
        "tested_premise_id": request["question"]["tested_premise_id"],
        "tested_premise_digest": request["question"]["tested_premise_digest"],
        "worker_output_digest": output["result_digest"],
        "scope": output["scope_boundary"],
        "requires_later_reflection": True,
        "direct_theory_effect_authorized": False,
    }
    knowledge["knowledge_id"] = stable_identifier(
        "descendant-negative-knowledge",
        request["request_id"],
        worker_id,
        output["result_digest"],
    )
    knowledge["knowledge_digest"] = canonical_digest(knowledge)
    return knowledge


def _reduce(
    *,
    request: Mapping[str, Any],
    receipts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    successful: dict[str, Mapping[str, Any]] = {}
    failures: list[str] = []
    for receipt in receipts:
        worker_id = str(receipt["worker_id"])
        if receipt["terminal_status"] == "succeeded":
            successful[worker_id] = receipt["worker_response"]["output"]
        else:
            failures.append(worker_id)
    outcomes = {
        worker_id: (
            successful[worker_id]["epistemic_outcome"]
            if worker_id in successful
            else "operational_failure"
        )
        for worker_id in WORKER_IDS
        if worker_id in successful or worker_id in failures
    }
    negatives = [
        _negative_knowledge(
            request=request,
            worker_id=worker_id,
            output=successful[worker_id],
        )
        for worker_id in WORKER_IDS
        if worker_id in successful
        and successful[worker_id]["epistemic_outcome"] == "premise_falsifier"
    ]
    if request["route_decision"] == "no_probe":
        classification = "no_probe"
    elif failures:
        classification = "operational_failure"
    elif (
        outcomes["symbolic_transition_trace"] == "premise_falsifier"
        and outcomes["bounded_simulation"] == "scoped_support"
    ):
        classification = "misleading_toy_positive"
    elif "premise_falsifier" in outcomes.values():
        classification = "registered_premise_falsifier"
    else:
        # Scoped finite support is intentionally reduced to inconclusive at the
        # theory boundary; only a later reflection may interpret it.
        classification = "neutral_inconclusive"
    complete = request["route_decision"] == "no_probe" or not failures
    later_reflection: dict[str, Any] | None = None
    if complete and negatives:
        later_reflection = {
            "request_kind": "candidate_later_descendant_reflection",
            "source_request_id": request["request_id"],
            "source_request_digest": request["content_digest"],
            "tested_premise_id": request["question"]["tested_premise_id"],
            "negative_knowledge_digests": [
                row["knowledge_digest"] for row in negatives
            ],
            "not_before_generation": request["theory_generation"] + 8,
            "requires_committed_aggregation_at_offset": 7,
            "current_cycle_effect_authorized": False,
        }
        later_reflection["request_id"] = stable_identifier(
            "later-descendant-reflection",
            request["request_id"],
            [row["knowledge_digest"] for row in negatives],
        )
        later_reflection["request_digest"] = canonical_digest(later_reflection)
    reduction: dict[str, Any] = {
        "reduction_policy": copy.deepcopy(_REDUCTION_POLICY),
        "worker_order": list(WORKER_IDS),
        "worker_outcomes": outcomes,
        "failed_worker_ids": [
            worker_id for worker_id in WORKER_IDS if worker_id in failures
        ],
        "world_classification": classification,
        "complete_process_wave": complete,
        "negative_knowledge": negatives,
        "later_reflection_request": later_reflection,
        "same_cycle_effects": {
            "theory": False,
            "preference": False,
            "proof": False,
            "schedule": False,
        },
    }
    reduction["reduction_digest"] = canonical_digest(reduction)
    return reduction


def _packet(
    request: Mapping[str, Any],
    receipts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    reduction = _reduce(request=request, receipts=receipts)
    packet: dict[str, Any] = {
        "schema_version": 1,
        "contract_version": CONTRACT_VERSION,
        "packet_kind": "descendant_support_process_execution",
        "request_id": request["request_id"],
        "request_digest": request["content_digest"],
        "target_id": request["target_id"],
        "run_id": request["run_id"],
        "branch_id": request["branch_id"],
        "theory_generation": request["theory_generation"],
        "route_decision": request["route_decision"],
        "production_invocation_mode": (
            "typed_python_facade_with_process_contained_symbolic_simulation_workers"
        ),
        "replay_invocation_mode": (
            "read_only_semantic_replay_validator_never_produces"
        ),
        "worker_order": list(WORKER_IDS),
        "terminal_receipts": [copy.deepcopy(dict(row)) for row in receipts],
        "terminal_barrier_complete": (
            request["route_decision"] == "no_probe"
            or len(receipts) == len(WORKER_IDS)
        ),
        "semantic_reduction": reduction,
        "descendant_world_product_eligible": (
            reduction["complete_process_wave"]
        ),
        "canonical_n_plus_8_closure_authorized": False,
        "composition_requirement": (
            "translate into role-validated GraphStageProduct values and use the "
            "canonical world-v3 facade; this packet cannot commit"
        ),
        "authority_nulls": copy.deepcopy(_AUTHORITY_NULLS),
    }
    packet["packet_digest"] = canonical_digest(packet)
    return packet


def run_descendant_support_process_wave(
    request: Mapping[str, Any],
    *,
    workspace: Path | str,
) -> DescendantSupportProcessExecution:
    """Launch the two governed producers, or return the exact no-probe packet."""

    validated = validate_theory_authored_descendant_experiment_request(request)
    root = Path(workspace).resolve()
    root.mkdir(parents=True, exist_ok=True)
    if root.is_symlink() or not root.is_dir():
        raise DescendantProcessContractError(
            "descendant process workspace must be a canonical directory"
        )
    if validated["route_decision"] == "no_probe":
        receipts: list[dict[str, Any]] = []
    else:
        receipts_by_worker: dict[str, dict[str, Any]] = {}
        futures: dict[Future[dict[str, Any]], str] = {}
        with ThreadPoolExecutor(
            max_workers=len(WORKER_IDS),
            thread_name_prefix="descendant-process-supervisor",
        ) as executor:
            for worker_id in WORKER_IDS:
                futures[
                    executor.submit(
                        _terminal_receipt,
                        request=validated,
                        worker_id=worker_id,
                        workspace=root,
                    )
                ] = worker_id
            for future in as_completed(futures):
                worker_id = futures[future]
                try:
                    receipts_by_worker[worker_id] = future.result()
                except Exception as exc:  # preserve an immutable operational terminal
                    receipt: dict[str, Any] = {
                        "schema_version": 1,
                        "contract_version": CONTRACT_VERSION,
                        "receipt_kind": "descendant_support_process_terminal",
                        "worker_id": worker_id,
                        "request_id": validated["request_id"],
                        "request_digest": validated["content_digest"],
                        "worker_request_digest": _worker_envelope(
                            validated, worker_id
                        )["content_digest"],
                        "worker_module_digest": bytes_digest(
                            Path(__file__).read_bytes()
                        ),
                        "resource_budget_digest": canonical_digest(
                            validated["resource_budgets"][worker_id]
                        ),
                        "terminal_status": "operational_failure",
                        "operational_reason": _bounded_reason(
                            f"supervisor_exception:{type(exc).__name__}:{exc}"
                        ),
                        "process_event": None,
                        "process_event_digest": None,
                        "worker_response": None,
                        "worker_response_digest": None,
                        "late_write_contained": False,
                        "authority_nulls": copy.deepcopy(_AUTHORITY_NULLS),
                    }
                    receipt["receipt_id"] = stable_identifier(
                        "descendant-terminal",
                        validated["request_id"],
                        worker_id,
                        None,
                        None,
                    )
                    receipt["receipt_digest"] = canonical_digest(receipt)
                    receipts_by_worker[worker_id] = receipt
        receipts = [receipts_by_worker[worker_id] for worker_id in WORKER_IDS]
    packet = _packet(validated, receipts)
    validate_descendant_support_process_execution(packet, validated)
    encoded = canonical_json(packet)
    return DescendantSupportProcessExecution(
        request_digest=validated["content_digest"],
        packet_digest=packet["packet_digest"],
        _canonical_packet=encoded,
    )


def validate_descendant_support_process_execution(
    raw: Mapping[str, Any] | DescendantSupportProcessExecution,
    request: Mapping[str, Any],
) -> dict[str, Any]:
    """Reopen terminal bytes and semantic reduction without launching workers."""

    validated_request = validate_theory_authored_descendant_experiment_request(
        request
    )
    source = raw.as_dict() if isinstance(raw, DescendantSupportProcessExecution) else raw
    packet = _exact_keys(
        source,
        {
            "schema_version",
            "contract_version",
            "packet_kind",
            "request_id",
            "request_digest",
            "target_id",
            "run_id",
            "branch_id",
            "theory_generation",
            "route_decision",
            "production_invocation_mode",
            "replay_invocation_mode",
            "worker_order",
            "terminal_receipts",
            "terminal_barrier_complete",
            "semantic_reduction",
            "descendant_world_product_eligible",
            "canonical_n_plus_8_closure_authorized",
            "composition_requirement",
            "authority_nulls",
            "packet_digest",
        },
        "descendant process execution packet",
    )
    if (
        packet["schema_version"] != 1
        or packet["contract_version"] != CONTRACT_VERSION
        or packet["packet_kind"] != "descendant_support_process_execution"
        or packet["request_id"] != validated_request["request_id"]
        or packet["request_digest"] != validated_request["content_digest"]
        or packet["target_id"] != validated_request["target_id"]
        or packet["run_id"] != validated_request["run_id"]
        or packet["branch_id"] != validated_request["branch_id"]
        or packet["theory_generation"] != validated_request["theory_generation"]
        or packet["route_decision"] != validated_request["route_decision"]
        or packet["production_invocation_mode"]
        != "typed_python_facade_with_process_contained_symbolic_simulation_workers"
        or packet["replay_invocation_mode"]
        != "read_only_semantic_replay_validator_never_produces"
        or packet["worker_order"] != list(WORKER_IDS)
        or packet["authority_nulls"] != _AUTHORITY_NULLS
        or packet["canonical_n_plus_8_closure_authorized"] is not False
        or packet["packet_digest"]
        != canonical_digest(
            {
                key: value
                for key, value in packet.items()
                if key != "packet_digest"
            }
        )
    ):
        raise DescendantProcessContractError(
            "descendant process packet identity, authority, or digest drifted"
        )
    raw_receipts = packet["terminal_receipts"]
    if not isinstance(raw_receipts, list):
        raise DescendantProcessContractError("terminal receipts must be a list")
    if validated_request["route_decision"] == "no_probe":
        if raw_receipts or packet["terminal_barrier_complete"] is not True:
            raise DescendantProcessContractError(
                "no_probe packet contains a process receipt"
            )
        receipts: list[dict[str, Any]] = []
    else:
        if (
            len(raw_receipts) != len(WORKER_IDS)
            or [row.get("worker_id") for row in raw_receipts] != list(WORKER_IDS)
            or packet["terminal_barrier_complete"] is not True
        ):
            raise DescendantProcessContractError(
                "process packet lacks the fixed complete terminal barrier"
            )
        receipts = [
            _validate_terminal_receipt(
                raw_receipts[index],
                request=validated_request,
                worker_id=worker_id,
            )
            for index, worker_id in enumerate(WORKER_IDS)
        ]
    expected_reduction = _reduce(
        request=validated_request,
        receipts=receipts,
    )
    if (
        packet["semantic_reduction"] != expected_reduction
        or packet["descendant_world_product_eligible"]
        is not expected_reduction["complete_process_wave"]
    ):
        raise DescendantProcessContractError(
            "descendant semantic reduction is not deterministic"
        )
    return packet


def _worker_main(worker_id: str) -> int:
    if worker_id not in WORKER_IDS:
        return 64
    try:
        raw = json.loads(sys.stdin.buffer.read())
        if not isinstance(raw, dict):
            raise DescendantProcessContractError(
                "worker stdin root must be one JSON object"
            )
        response = _execute_worker(raw, worker_id)
        encoded = canonical_json(response)
        if len(encoded) > MAX_WORKER_OUTPUT_BYTES:
            raise DescendantProcessContractError(
                "worker response exceeds the hard protocol ceiling"
            )
        sys.stdout.buffer.write(encoded)
        sys.stdout.buffer.write(b"\n")
        return 0
    except (
        DescendantProcessContractError,
        json.JSONDecodeError,
        OSError,
        TypeError,
        ValueError,
    ) as exc:
        sys.stderr.write(
            _bounded_reason(f"{type(exc).__name__}:{exc}") + "\n"
        )
        return 65


__all__ = [
    "CONTRACT_VERSION",
    "DescendantProcessContractError",
    "DescendantSupportProcessExecution",
    "MAX_SIMULATION_STEPS",
    "MAX_SIMULATION_TRAJECTORIES",
    "MAX_SYMBOLIC_TRANSITIONS",
    "WORKER_IDS",
    "build_theory_authored_descendant_experiment_request",
    "run_descendant_support_process_wave",
    "validate_descendant_support_process_execution",
    "validate_theory_authored_descendant_experiment_request",
]


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--worker":
        raise SystemExit(64)
    raise SystemExit(_worker_main(sys.argv[2]))
