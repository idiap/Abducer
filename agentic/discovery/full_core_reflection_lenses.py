# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Six independently supervised full-core conceptual reflection lenses.

Each exact lens receives only the same complete candidate core, its lens
identity, and a normalized resource budget in its own
:class:`ResearchWorkerAdapter` process.  The semantic transformation is
authored inside that process rather than supplied by the supervisor.  The
supervisor joins all six attempts before constructing a terminal barrier.
Operational failures remain durable terminal evidence but are never eligible
for conceptual ancestry.

The module also supervises parent-system materializers.  Each such registered
producer consumes one exact matured candidate and the six exact lens outputs,
then emits a typed before/after conceptual delta.  Distinct PIDs and receipts
remain process evidence only; hidden-input, cognitive, semantic, merit, truth,
and physics-value authority remain unavailable.
"""

from __future__ import annotations

import copy
import datetime as dt
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .budgets import ResourceBudget, contained_path
from .contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    validate_identifier,
    validate_payload,
)
from .open_world_creativity import DEEP_REFLECTION_LENSES
from .research_worker_isolation import (
    ResearchWorkerAdapter,
    ResearchWorkerIntegrityError,
    receipt_summary,
    validate_research_worker_receipt,
)


SCHEMA_VERSION = "1.0.0"
SCHEMA_NAME = "full_core_reflection_lens_execution_v1.schema.json"
CANDIDATE_CORE_FIELDS = (
    "statement",
    "semantic_core",
    "risk_reward",
    "physics_handback",
)
AUTHORITY_NULLS = {
    "process_evidence_scope": (
        "six_distinct_supervised_local_process_receipts_only"
    ),
    "hidden_input_independence": "unavailable",
    "cognitive_independence": "unavailable",
    "semantic_independence": "unavailable",
    "conceptual_merit_authority": None,
    "truth_authority": None,
    "physics_value_authority": None,
}
AUTHORITY_BOUNDARY = (
    "This bundle reopens one immutable ResearchWorkerAdapter receipt for each "
    "of six exact conceptual lenses, proves that the complete candidate core "
    "and normalized budget were identical, observes six distinct local PIDs, "
    "and requires one common interval before promotion. It grants local "
    "process and byte-replay evidence only. It grants no hidden-input, "
    "cognitive, semantic, evaluator, creativity, conceptual-merit, truth, "
    "theorem, experiment, or physics-value authority."
)
WORKER_AUTHORITY_BOUNDARY = (
    "one exact common core was transformed by the requested lens inside this "
    "supervised local process; process-local semantic authorship grants no "
    "cognitive independence, semantic independence, conceptual merit, truth, "
    "theorem, experiment, or physics-value authority"
)
MATERIALIZATION_AUTHORITY_BOUNDARY = (
    "one parent conceptual-system byte sequence and typed before/after delta "
    "were authored inside this supervised process from one exact matured "
    "candidate and six exact receipt-bound lens outputs; this grants no "
    "conceptual merit, truth, theorem, experiment, or physics-value authority"
)
LENS_RECIPES = {
    "ontological": ("retype_source", "is ontologically retyped as"),
    "dialectical": ("reverse_relation", "is dialectically opposed by"),
    "genealogical": ("trace_origin", "is contingently inherited through"),
    "modal_explanatory": (
        "counterfactualize_relation",
        "counterfactually conditions rather than necessitates",
    ),
    "unification": (
        "factor_common_structure",
        "is mediated while preserving difference from",
    ),
    "philosophy_of_physics": (
        "identify_physical_carrier",
        "is physically carried through",
    ),
}
REFLECTION_FIELDS = frozenset(
    {
        "named_relation",
        "relation_before",
        "relation_operation",
        "mutation_status",
        "relation_after",
        "exposed_assumption",
        "strongest_opposition",
        "conceptual_mutation",
        "consequence",
        "boundary_or_correction",
        "semantic_core_correction_link",
        "physics_handback_link",
    }
)
MATERIALIZATION_OUTPUT_FIELDS = frozenset(
    {
        "output_kind",
        "candidate_id",
        "matured_candidate_digest",
        "lens_output_set_digest",
        "literature_derived_invention_input_digest",
        "parent_conceptual_system",
        "parent_conceptual_system_digest",
        "conceptual_delta",
        "conceptual_delta_digest",
        "semantic_authorship",
        "authority_boundary",
    }
)


class FullCoreReflectionLensError(ContractError):
    """Carry a stable six-lens supervision or replay rejection code."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"full_core_reflection_lenses[{reason_code}]: {message}")


def _fail(reason_code: str, message: str) -> None:
    raise FullCoreReflectionLensError(reason_code, message)


def _candidate_parts(
    candidate: Mapping[str, Any],
) -> tuple[str, dict[str, Any]]:
    if not isinstance(candidate, Mapping):
        _fail("candidate_invalid", "candidate must be an object")
    candidate_id = str(candidate.get("invention_id", ""))
    try:
        validate_identifier(candidate_id, "candidate_id")
    except ContractError as exc:
        raise FullCoreReflectionLensError(
            "candidate_invalid", "candidate invention_id is invalid"
        ) from exc
    missing = [field for field in CANDIDATE_CORE_FIELDS if field not in candidate]
    if missing:
        _fail(
            "candidate_core_incomplete",
            "candidate lacks complete core fields: " + ",".join(missing),
        )
    core = {
        field: copy.deepcopy(candidate[field])
        for field in CANDIDATE_CORE_FIELDS
    }
    if not isinstance(core["statement"], str) or not core["statement"].strip():
        _fail("candidate_core_invalid", "candidate statement is empty")
    if any(not isinstance(core[field], Mapping) for field in CANDIDATE_CORE_FIELDS[1:]):
        _fail("candidate_core_invalid", "candidate structured core fields must be objects")
    semantic_core = core["semantic_core"]
    relations = semantic_core.get("relations")
    if not isinstance(relations, list) or not relations:
        _fail("candidate_core_invalid", "semantic core requires typed relations")
    if not all(
        isinstance(row, Mapping)
        and set(row) == {"source", "polarity", "target"}
        and all(isinstance(row[key], str) and row[key].strip() for key in row)
        for row in relations
    ):
        _fail("candidate_core_invalid", "semantic relations are not closed")
    if not all(
        isinstance(semantic_core.get(field), str)
        and semantic_core[field].strip()
        for field in ("correction_condition", "falsifier")
    ):
        _fail("candidate_core_invalid", "semantic correction/falsifier is absent")
    return candidate_id, core


def _normalized_budget(raw: Mapping[str, Any] | None) -> dict[str, Any]:
    candidate = (
        ResearchWorkerAdapter.default_budget()
        if raw is None
        else copy.deepcopy(dict(raw))
    )
    try:
        return asdict(ResourceBudget.from_mapping(candidate))
    except (TypeError, ValueError) as exc:
        raise FullCoreReflectionLensError(
            "matched_budget_invalid", "lens budget is not a valid resource budget"
        ) from exc


def _normalized_literature_input(
    raw: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Return one sealed causal input, retaining an explicit standalone null."""

    if raw is None:
        core = {
            "schema_version": "1.0.0",
            "artifact_kind": "literature_derived_invention_input",
            "input_id": "literature-derived-invention-input.unavailable",
            "target_id": "standalone-full-core-reflection",
            "raw_capture_sha256": canonical_digest(
                "unavailable_raw_capture"
            ),
            "semantic_bridge_id": "literature-bridge.unavailable",
            "semantic_bridge_digest": canonical_digest(
                "unavailable_semantic_bridge"
            ),
            "semantic_snapshot_id": "literature-snapshot.unavailable",
            "semantic_snapshot_digest": canonical_digest(
                "unavailable_semantic_snapshot"
            ),
            "causal_inputs": [
                {
                    "causal_input_id": "literature-causal-input.unavailable",
                    "assimilation_delta": {
                        "event_type": "justified_no_change",
                    },
                }
            ],
            "corrected_or_superseded_source_ids": [],
            "retracted_source_ids": [],
            "coverage_limits": [
                "No semantic literature input was supplied to this standalone execution."
            ],
            "authority_nulls": {
                "source_truth_authority": None,
                "semantic_entailment_authority": None,
                "global_latestness_authority": None,
                "exhaustiveness_authority": None,
                "literature_benefit_authority": None,
                "creativity_authority": None,
            },
        }
        return {**core, "content_digest": canonical_digest(core)}
    value = copy.deepcopy(dict(raw))
    if (
        value.get("artifact_kind") != "literature_derived_invention_input"
        or value.get("content_digest")
        != canonical_digest(
            {key: item for key, item in value.items() if key != "content_digest"}
        )
        or not isinstance(value.get("causal_inputs"), list)
        or not value["causal_inputs"]
    ):
        _fail(
            "literature_invention_input_invalid",
            "lens input must be one exact sealed semantic causal projection",
        )
    return value


def _receipt_path(receipt: Mapping[str, Any]) -> Path:
    try:
        run_directory = Path(str(receipt["workspace"]["run_directory"]))
        return contained_path(
            run_directory, *Path(str(receipt["receipt_ref"])).parts
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise FullCoreReflectionLensError(
            "receipt_path_invalid", "research-worker receipt path is invalid"
        ) from exc


def _parse_time(value: Any, field: str) -> dt.datetime | None:
    if value is None:
        return None
    if not isinstance(value, str):
        _fail("terminal_interval_invalid", f"{field} must be a timestamp or null")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise FullCoreReflectionLensError(
            "terminal_interval_invalid", f"{field} is invalid"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _fail("terminal_interval_invalid", f"{field} must carry a timezone")
    return parsed.astimezone(dt.UTC)


def _physics_link(candidate_core: Mapping[str, Any]) -> str:
    handback = candidate_core["physics_handback"]
    for field in (
        "correction_or_falsifier",
        "proposed_next_decision",
        "decision_rationale",
        "physical_carrier",
        "regime_and_quantifiers",
    ):
        value = handback.get(field)
        if isinstance(value, str) and value.strip():
            return value
    _fail("candidate_core_invalid", "physics handback lacks a link target")


def _derived_reflection(
    candidate_core: Mapping[str, Any], lens_id: str
) -> dict[str, Any]:
    """Independently reconstruct the deterministic process-authored lens."""

    semantic_core = candidate_core["semantic_core"]
    relation_index = DEEP_REFLECTION_LENSES.index(lens_id) % len(
        semantic_core["relations"]
    )
    before = copy.deepcopy(dict(semantic_core["relations"][relation_index]))
    operation, polarity = LENS_RECIPES[lens_id]
    if lens_id == "dialectical":
        after = {
            "source": before["target"],
            "polarity": polarity,
            "target": before["source"],
        }
    elif lens_id == "genealogical":
        after = {
            "source": f"historical conditions of {before['source']}",
            "polarity": polarity,
            "target": before["target"],
        }
    elif lens_id == "unification":
        after = {
            "source": f"shared structure across {before['source']}",
            "polarity": polarity,
            "target": before["target"],
        }
    elif lens_id == "philosophy_of_physics":
        after = {
            "source": before["source"],
            "polarity": polarity,
            "target": (
                f"{before['target']} on {_physics_link(candidate_core)}"
            ),
        }
    else:
        after = {
            "source": (
                f"ontologically retyped {before['source']}"
                if lens_id == "ontological"
                else before["source"]
            ),
            "polarity": polarity,
            "target": before["target"],
        }
    named = (
        f"{before['source']} --{before['polarity']}--> {before['target']}"
    )
    correction = str(semantic_core["correction_condition"])
    return {
        "named_relation": named,
        "relation_before": before,
        "relation_operation": operation,
        "mutation_status": "changed",
        "relation_after": after,
        "exposed_assumption": (
            f"The {lens_id} producer exposes the assumption that {named} "
            "must retain its inherited explanatory type."
        ),
        "strongest_opposition": (
            f"The strongest opposition is that the {lens_id} transformation "
            "may relocate vocabulary without changing a target burden."
        ),
        "conceptual_mutation": (
            f"The {lens_id} operation replaces the inherited relation with "
            f"{after['source']} --{after['polarity']}--> {after['target']}."
        ),
        "consequence": (
            f"The {lens_id} transformation requires the next theory action "
            "to test the changed relation rather than the supplied wording."
        ),
        "boundary_or_correction": correction,
        "semantic_core_correction_link": correction,
        "physics_handback_link": _physics_link(candidate_core),
    }


def _expected_output(
    *,
    candidate_id: str,
    candidate_core: Mapping[str, Any],
    lens_id: str,
    literature_input: Mapping[str, Any],
) -> dict[str, Any]:
    reflection = _derived_reflection(candidate_core, lens_id)
    relation_after = reflection["relation_after"]
    causal_rows = literature_input["causal_inputs"]
    selected_input = causal_rows[
        DEEP_REFLECTION_LENSES.index(lens_id) % len(causal_rows)
    ]
    return {
        "output_kind": "reflection",
        "candidate_id": candidate_id,
        "lens_id": lens_id,
        "candidate_core_digest": canonical_digest(candidate_core),
        "literature_derived_invention_input_digest": literature_input[
            "content_digest"
        ],
        "literature_causal_input_id": selected_input["causal_input_id"],
        "literature_assimilation_delta": copy.deepcopy(
            selected_input["assimilation_delta"]
        ),
        "reflection": copy.deepcopy(dict(reflection)),
        "reflection_digest": canonical_digest(reflection),
        "operation_witness": {
            "lens_operation": reflection["relation_operation"],
            "named_relation": reflection["named_relation"],
            "relation_before_digest": canonical_digest(
                reflection["relation_before"]
            ),
            "relation_after_digest": (
                canonical_digest(relation_after)
                if relation_after is not None
                else None
            ),
            "mutation_status": reflection["mutation_status"],
            "complete_core_fields_replayed": sorted(CANDIDATE_CORE_FIELDS),
        },
        "semantic_authorship": {
            "status": "authored_inside_supervised_process",
            "upstream_reflection_supplied": False,
            "input_scope": (
                "exact_common_core_plus_lens_identity_plus_semantic_literature_input"
            ),
            "producer_algorithm": (
                "closed_lens_specific_relation_transformation_v1"
            ),
        },
        "authority_boundary": WORKER_AUTHORITY_BOUNDARY,
    }


def _execution_record(
    *,
    receipt: Mapping[str, Any],
    candidate_id: str,
    candidate_core: Mapping[str, Any],
    matched_budget: Mapping[str, Any],
    literature_input: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        path = _receipt_path(receipt)
        registered = validate_research_worker_receipt(
            receipt,
            receipt_path=path,
            require_live_authority=receipt.get("outcome_status") == "accepted",
        )
        summary = receipt_summary(registered, receipt_path=path)
    except (OSError, ResearchWorkerIntegrityError) as exc:
        raise FullCoreReflectionLensError(
            "receipt_replay_failed", "registered lens receipt failed exact replay"
        ) from exc
    request = registered["request_payload"]
    payload = request["payload"]
    context = request["invocation_context"]
    lens_id = str(payload.get("lens_id", ""))
    if lens_id not in DEEP_REFLECTION_LENSES:
        _fail("lens_bijection_invalid", "receipt names an unknown lens")
    expected_core_digest = canonical_digest(candidate_core)
    expected_budget_digest = canonical_digest(matched_budget)
    expected_literature_digest = literature_input["content_digest"]
    expected_payload = {
        "candidate_id": candidate_id,
        "candidate_core": copy.deepcopy(dict(candidate_core)),
        "candidate_core_digest": expected_core_digest,
        "lens_id": lens_id,
        "matched_budget_digest": expected_budget_digest,
        "literature_derived_invention_input": copy.deepcopy(
            dict(literature_input)
        ),
        "literature_derived_invention_input_digest": (
            expected_literature_digest
        ),
        "minimum_residency_seconds": payload.get(
            "minimum_residency_seconds"
        ),
    }
    expected_context = {
        "candidate_id": candidate_id,
        "candidate_core_digest": expected_core_digest,
        "lens_id": lens_id,
        "matched_budget_digest": expected_budget_digest,
        "literature_derived_invention_input_digest": (
            expected_literature_digest
        ),
    }
    if (
        registered["role"] != "candidate"
        or registered["operation"] != "reflection"
        or payload != expected_payload
        or context != expected_context
        or registered["resource_receipt"]["budget"] != dict(matched_budget)
        or registered["budget_digest"] != expected_budget_digest
    ):
        _fail(
            "receipt_request_binding_mismatch",
            f"{lens_id} receipt changed its complete core, lens, context, or budget",
        )
    if registered["outcome_status"] == "accepted":
        output = registered["response_payload"]["output"]
        if output != _expected_output(
            candidate_id=candidate_id,
            candidate_core=candidate_core,
            lens_id=lens_id,
            literature_input=literature_input,
        ):
            _fail(
                "lens_output_binding_mismatch",
                f"{lens_id} output does not replay its exact full-core operation",
            )
    record_core = {
        "lens_id": lens_id,
        "candidate_core_digest": expected_core_digest,
        "produced_reflection": copy.deepcopy(
            registered["response_payload"]["output"]["reflection"]
        )
        if registered["outcome_status"] == "accepted"
        else None,
        "produced_reflection_digest": (
            registered["response_payload"]["output"]["reflection_digest"]
            if registered["outcome_status"] == "accepted"
            else None
        ),
        "semantic_output_digest": (
            canonical_digest(registered["response_payload"]["output"])
            if registered["outcome_status"] == "accepted"
            else None
        ),
        "matched_budget_digest": expected_budget_digest,
        "literature_derived_invention_input_digest": (
            expected_literature_digest
        ),
        "registered_receipt": copy.deepcopy(registered),
        "receipt_file_sha256": summary["receipt_file_sha256"],
        "receipt_byte_length": summary["receipt_byte_length"],
    }
    return {
        **record_core,
        "execution_record_digest": canonical_digest(record_core),
    }


def _barrier(
    *,
    candidate_core_digest: str,
    matched_budget_digest: str,
    literature_derived_invention_input_digest: str,
    executions: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    members: list[dict[str, Any]] = []
    intervals: list[tuple[dt.datetime, int]] = []
    starts: list[dt.datetime] = []
    completions: list[dt.datetime] = []
    for record in executions:
        receipt = record["registered_receipt"]
        event = receipt["process_event"]
        if event.get("event") != "process_terminal":
            _fail("barrier_nonterminal", "a lens receipt is not terminal")
        started = _parse_time(event.get("started_at"), "process_started_at")
        completed = _parse_time(event.get("completed_at"), "process_completed_at")
        if (started is None) != (completed is None):
            _fail("terminal_interval_invalid", "lens interval is only partially recorded")
        if started is not None and completed is not None:
            if completed < started:
                _fail("terminal_interval_invalid", "lens process completed before it started")
            starts.append(started)
            completions.append(completed)
            intervals.extend(((started, 1), (completed, -1)))
        members.append(
            {
                "lens_id": record["lens_id"],
                "receipt_id": receipt["receipt_id"],
                "receipt_digest": receipt["content_digest"],
                "receipt_file_sha256": record["receipt_file_sha256"],
                "request_sha256": receipt["request_sha256"],
                "response_sha256": receipt["response_sha256"],
                "outcome_status": receipt["outcome_status"],
                "pid": event.get("pid"),
                "process_started_at": event.get("started_at"),
                "process_completed_at": event.get("completed_at"),
            }
        )
    active = 0
    peak = 0
    for _instant, delta in sorted(intervals, key=lambda item: (item[0], item[1])):
        active += delta
        peak = max(peak, active)
    all_overlap = (
        len(starts) == len(DEEP_REFLECTION_LENSES)
        and max(starts) < min(completions)
    )
    receipt_ids = {member["receipt_id"] for member in members}
    process_ids = {
        member["pid"] for member in members if isinstance(member["pid"], int)
    }
    accepted = sum(
        member["outcome_status"] == "accepted" for member in members
    )
    exact_bijection = (
        len(members) == len(DEEP_REFLECTION_LENSES)
        and [member["lens_id"] for member in members]
        == list(DEEP_REFLECTION_LENSES)
        and len(receipt_ids) == len(DEEP_REFLECTION_LENSES)
    )
    promotion_eligible = bool(
        exact_bijection
        and accepted == len(DEEP_REFLECTION_LENSES)
        and len(process_ids) == len(DEEP_REFLECTION_LENSES)
        and peak == len(DEEP_REFLECTION_LENSES)
        and all_overlap
    )
    core = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "full_core_reflection_lens_terminal_barrier",
        "barrier_id": stable_identifier(
            "full-core-reflection-lens-barrier",
            candidate_core_digest,
            matched_budget_digest,
            literature_derived_invention_input_digest,
            members,
        ),
        "status": "all_scheduled_lenses_terminal",
        "candidate_core_digest": candidate_core_digest,
        "matched_budget_digest": matched_budget_digest,
        "literature_derived_invention_input_digest": (
            literature_derived_invention_input_digest
        ),
        "scheduled_lens_count": len(DEEP_REFLECTION_LENSES),
        "terminal_lens_count": len(members),
        "accepted_lens_count": accepted,
        "distinct_receipt_count": len(receipt_ids),
        "distinct_process_count": len(process_ids),
        "observed_peak_parallelism": peak,
        "all_six_intervals_overlap": all_overlap,
        "exact_lens_receipt_bijection": exact_bijection,
        "promotion_eligible": promotion_eligible,
        "terminal_members": members,
    }
    return {**core, "barrier_digest": canonical_digest(core)}


def build_full_core_reflection_lens_execution_bundle(
    candidate: Mapping[str, Any],
    *,
    registered_receipts: Sequence[Mapping[str, Any]],
    matched_budget: Mapping[str, Any] | None = None,
    literature_derived_invention_input: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Bind exactly six immutable receipts and close one all-terminal barrier."""

    candidate_id, candidate_core = _candidate_parts(candidate)
    budget = _normalized_budget(matched_budget)
    literature_input = _normalized_literature_input(
        literature_derived_invention_input
    )
    receipts = [copy.deepcopy(dict(row)) for row in registered_receipts]
    if len(receipts) != len(DEEP_REFLECTION_LENSES):
        _fail(
            "missing_lens_receipt",
            "the terminal barrier requires exactly six registered receipts",
        )
    executions = [
        _execution_record(
            receipt=receipt,
            candidate_id=candidate_id,
            candidate_core=candidate_core,
            matched_budget=budget,
            literature_input=literature_input,
        )
        for receipt in receipts
    ]
    by_lens: dict[str, dict[str, Any]] = {}
    for execution in executions:
        lens_id = execution["lens_id"]
        if lens_id in by_lens:
            _fail(
                "duplicate_lens_receipt",
                f"multiple receipts claim the {lens_id} lens",
            )
        by_lens[lens_id] = execution
    if set(by_lens) != set(DEEP_REFLECTION_LENSES):
        _fail(
            "missing_lens_receipt",
            "receipt set is not an exact bijection over the six lenses",
        )
    ordered = [by_lens[lens_id] for lens_id in DEEP_REFLECTION_LENSES]
    core_digest = canonical_digest(candidate_core)
    budget_digest = canonical_digest(budget)
    barrier = _barrier(
        candidate_core_digest=core_digest,
        matched_budget_digest=budget_digest,
        literature_derived_invention_input_digest=literature_input[
            "content_digest"
        ],
        executions=ordered,
    )
    core = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "full_core_reflection_lens_execution_bundle",
        "execution_bundle_id": stable_identifier(
            "full-core-reflection-lens-execution",
            candidate_id,
            core_digest,
            literature_input["content_digest"],
            [row["execution_record_digest"] for row in ordered],
        ),
        "candidate_id": candidate_id,
        "candidate_core": candidate_core,
        "candidate_core_digest": core_digest,
        "literature_derived_invention_input": literature_input,
        "literature_derived_invention_input_digest": literature_input[
            "content_digest"
        ],
        "lens_order": list(DEEP_REFLECTION_LENSES),
        "matched_budget": budget,
        "matched_budget_digest": budget_digest,
        "status": (
            "all_terminal_promotion_eligible"
            if barrier["promotion_eligible"]
            else "all_terminal_not_promotion_eligible"
        ),
        "lens_executions": ordered,
        "all_terminal_barrier": barrier,
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    bundle = {**core, "content_digest": canonical_digest(core)}
    validate_payload(bundle, SCHEMA_NAME)
    return bundle


def validate_full_core_reflection_lens_execution_bundle(
    bundle: Mapping[str, Any],
    *,
    candidate: Mapping[str, Any] | None = None,
    require_promotion_eligible: bool = False,
) -> dict[str, Any]:
    """Reopen all six receipts and reconstruct the exact terminal barrier."""

    value = copy.deepcopy(dict(bundle))
    validate_payload(value, SCHEMA_NAME)
    if value["content_digest"] != canonical_digest(
        {key: item for key, item in value.items() if key != "content_digest"}
    ):
        _fail("bundle_digest_mismatch", "lens execution bundle digest changed")
    if candidate is None:
        candidate_value = {
            "invention_id": value["candidate_id"],
            **copy.deepcopy(value["candidate_core"]),
        }
    else:
        candidate_value = copy.deepcopy(dict(candidate))
    expected = build_full_core_reflection_lens_execution_bundle(
        candidate_value,
        registered_receipts=[
            row["registered_receipt"] for row in value["lens_executions"]
        ],
        matched_budget=value["matched_budget"],
        literature_derived_invention_input=value[
            "literature_derived_invention_input"
        ],
    )
    if value != expected:
        _fail(
            "bundle_replay_mismatch",
            "lens/core/receipt/budget/barrier binding does not replay",
        )
    if require_promotion_eligible and not value["all_terminal_barrier"][
        "promotion_eligible"
    ]:
        _fail(
            "lens_process_barrier_ineligible",
            "ancestry requires six accepted distinct overlapping lens processes",
        )
    return copy.deepcopy(value)


def run_full_core_reflection_lenses(
    candidate: Mapping[str, Any],
    *,
    run_root: Path | str,
    matched_budget: Mapping[str, Any] | None = None,
    literature_derived_invention_input: Mapping[str, Any] | None = None,
    require_kernel_isolation: bool = False,
    max_workers: int = 6,
    minimum_residency_seconds: float = 0.35,
    fault_plan: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Execute all six lens processes, join them, and return terminal evidence."""

    candidate_id, candidate_core = _candidate_parts(candidate)
    if (
        not isinstance(max_workers, int)
        or isinstance(max_workers, bool)
        or not 1 <= max_workers <= len(DEEP_REFLECTION_LENSES)
    ):
        _fail("worker_count_invalid", "max_workers must be between one and six")
    if (
        not isinstance(minimum_residency_seconds, (int, float))
        or isinstance(minimum_residency_seconds, bool)
        or not 0.02 <= float(minimum_residency_seconds) <= 1.0
    ):
        _fail(
            "residency_invalid",
            "minimum_residency_seconds must remain in [0.02, 1.0]",
        )
    faults = dict(fault_plan or {})
    if set(faults) - set(DEEP_REFLECTION_LENSES) or any(
        mode not in {"exit_nonzero", "invalid_json", "hang"}
        for mode in faults.values()
    ):
        _fail("fault_plan_invalid", "fault plan names an unknown lens or mode")
    budget = _normalized_budget(matched_budget)
    literature_input = _normalized_literature_input(
        literature_derived_invention_input
    )
    core_digest = canonical_digest(candidate_core)
    budget_digest = canonical_digest(budget)
    study_id = stable_identifier(
        "full-core-reflection-lens-study",
        candidate_id,
        core_digest,
        literature_input["content_digest"],
        budget,
        require_kernel_isolation,
    )
    worker_script = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "run_full_core_reflection_lens_worker.py"
    )
    adapter = ResearchWorkerAdapter(
        study_id=study_id,
        run_root=run_root,
        worker_script=worker_script,
        approved_dependency_paths=(
            Path(__file__).resolve(),
            Path(__file__).resolve().parents[1] / "spec" / SCHEMA_NAME,
        ),
        require_kernel_isolation=require_kernel_isolation,
    )

    def invoke(lens_id: str) -> dict[str, Any]:
        return adapter.invoke(
            role="candidate",
            operation="reflection",
            invocation_context={
                "candidate_id": candidate_id,
                "candidate_core_digest": core_digest,
                "lens_id": lens_id,
                "matched_budget_digest": budget_digest,
                "literature_derived_invention_input_digest": (
                    literature_input["content_digest"]
                ),
            },
            payload={
                "candidate_id": candidate_id,
                "candidate_core": copy.deepcopy(candidate_core),
                "candidate_core_digest": core_digest,
                "lens_id": lens_id,
                "matched_budget_digest": budget_digest,
                "literature_derived_invention_input": copy.deepcopy(
                    literature_input
                ),
                "literature_derived_invention_input_digest": (
                    literature_input["content_digest"]
                ),
                "minimum_residency_seconds": float(
                    minimum_residency_seconds
                ),
            },
            budget=budget,
            fault_mode=faults.get(lens_id),
        )

    receipts_by_lens: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(invoke, lens_id): lens_id
            for lens_id in DEEP_REFLECTION_LENSES
        }
        for future in as_completed(futures):
            lens_id = futures[future]
            receipts_by_lens[lens_id] = future.result()
    return build_full_core_reflection_lens_execution_bundle(
        candidate,
        registered_receipts=[
            receipts_by_lens[lens_id] for lens_id in DEEP_REFLECTION_LENSES
        ],
        matched_budget=budget,
        literature_derived_invention_input=literature_input,
    )


def _materialization_lens_outputs(
    candidate: Mapping[str, Any],
    bundle: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Return the exact six process-authored outputs and receipt bindings."""

    validated = validate_full_core_reflection_lens_execution_bundle(
        bundle, candidate=candidate, require_promotion_eligible=True
    )
    outputs: list[dict[str, Any]] = []
    for execution in validated["lens_executions"]:
        receipt = execution["registered_receipt"]
        output = receipt["response_payload"]["output"]
        outputs.append(
            {
                "lens_id": execution["lens_id"],
                "candidate_core_digest": execution["candidate_core_digest"],
                "literature_derived_invention_input_digest": execution[
                    "literature_derived_invention_input_digest"
                ],
                "reflection": copy.deepcopy(output["reflection"]),
                "reflection_digest": output["reflection_digest"],
                "execution_record_digest": execution[
                    "execution_record_digest"
                ],
                "receipt_id": receipt["receipt_id"],
                "receipt_digest": receipt["content_digest"],
                "response_sha256": receipt["response_sha256"],
            }
        )
    return outputs


def _validate_materialization_output(
    output: Mapping[str, Any],
    *,
    candidate: Mapping[str, Any],
    lens_outputs: Sequence[Mapping[str, Any]],
    literature_input: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay typed before/after and exact producer-input digest bindings."""

    value = copy.deepcopy(dict(output))
    if set(value) != MATERIALIZATION_OUTPUT_FIELDS:
        _fail(
            "materialization_output_invalid",
            "parent materialization output is not the closed typed record",
        )
    candidate_id, _core = _candidate_parts(candidate)
    candidate_value = copy.deepcopy(dict(candidate))
    candidate_digest = canonical_digest(candidate_value)
    outputs = [copy.deepcopy(dict(row)) for row in lens_outputs]
    output_set_digest = canonical_digest(outputs)
    system = value["parent_conceptual_system"]
    delta = value["conceptual_delta"]
    if (
        value["output_kind"] != "candidate_generation"
        or value["candidate_id"] != candidate_id
        or value["matured_candidate_digest"] != candidate_digest
        or value["lens_output_set_digest"] != output_set_digest
        or value["literature_derived_invention_input_digest"]
        != literature_input["content_digest"]
        or not isinstance(system, Mapping)
        or value["parent_conceptual_system_digest"]
        != canonical_digest(system)
        or not isinstance(delta, Mapping)
        or value["conceptual_delta_digest"] != canonical_digest(delta)
        or value["authority_boundary"]
        != MATERIALIZATION_AUTHORITY_BOUNDARY
        or value["semantic_authorship"]
        != {
            "status": "authored_inside_registered_supervised_process",
            "input_scope": (
                "exact_matured_candidate_plus_six_lens_outputs_plus_semantic_literature_input"
            ),
            "producer_algorithm": "closed_parent_system_materialization_v1",
        }
    ):
        _fail(
            "materialization_output_binding_mismatch",
            "parent output changed its exact candidate, lenses, or authorship",
        )
    if (
        delta.get("delta_kind")
        != (
            "matured_candidate_plus_six_lens_outputs_to_parent_conceptual_system"
        )
        or delta.get("source_candidate_id") != candidate_id
        or delta.get("source_candidate_digest") != candidate_digest
        or delta.get("lens_output_set_digest") != output_set_digest
        or delta.get("literature_derived_invention_input_digest")
        != literature_input["content_digest"]
        or delta.get("before")
        != {
            "artifact_kind": "matured_candidate",
            "content": candidate_value,
            "content_digest": candidate_digest,
        }
        or delta.get("after")
        != {
            "artifact_kind": "parent_conceptual_system",
            "content": dict(system),
            "content_digest": canonical_digest(system),
        }
        or delta.get("changed_paths")
        != [
            f"/lens_outputs/{index}/reflection/relation_after"
            for index in range(len(DEEP_REFLECTION_LENSES))
        ]
        or delta.get("preserved_source_paths")
        != [
            "/statement",
            "/semantic_core/protected_differences",
            "/semantic_core/correction_condition",
            "/physics_handback",
        ]
    ):
        _fail(
            "materialization_delta_invalid",
            "typed parent before/after delta does not replay",
        )
    return value


def validate_parent_system_materialization_receipt(
    receipt: Mapping[str, Any],
    *,
    candidate: Mapping[str, Any],
    lens_execution_bundle: Mapping[str, Any],
) -> dict[str, Any]:
    """Reopen one registered producer receipt and its exact conceptual delta."""

    candidate_id, _core = _candidate_parts(candidate)
    lens_outputs = _materialization_lens_outputs(
        candidate, lens_execution_bundle
    )
    literature_input = _normalized_literature_input(
        lens_execution_bundle["literature_derived_invention_input"]
    )
    try:
        path = _receipt_path(receipt)
        registered = validate_research_worker_receipt(
            receipt, receipt_path=path, require_live_authority=True
        )
        summary = receipt_summary(registered, receipt_path=path)
    except (OSError, ResearchWorkerIntegrityError) as exc:
        raise FullCoreReflectionLensError(
            "materialization_receipt_replay_failed",
            "registered parent producer receipt failed exact replay",
        ) from exc
    if (
        registered["outcome_status"] != "accepted"
        or not isinstance(registered["response_payload"], Mapping)
    ):
        _fail(
            "materialization_producer_failed",
            "registered parent producer did not return an accepted response",
        )
    budget = registered["resource_receipt"]["budget"]
    budget_digest = canonical_digest(budget)
    candidate_value = copy.deepcopy(dict(candidate))
    candidate_digest = canonical_digest(candidate_value)
    output_set_digest = canonical_digest(lens_outputs)
    payload = registered["request_payload"]["payload"]
    expected_payload = {
        "matured_candidate": candidate_value,
        "matured_candidate_digest": candidate_digest,
        "lens_outputs": lens_outputs,
        "lens_output_set_digest": output_set_digest,
        "literature_derived_invention_input": literature_input,
        "literature_derived_invention_input_digest": literature_input[
            "content_digest"
        ],
        "matched_budget_digest": budget_digest,
        "minimum_residency_seconds": payload.get(
            "minimum_residency_seconds"
        ),
    }
    expected_context = {
        "candidate_id": candidate_id,
        "matured_candidate_digest": candidate_digest,
        "lens_output_set_digest": output_set_digest,
        "literature_derived_invention_input_digest": literature_input[
            "content_digest"
        ],
        "matched_budget_digest": budget_digest,
    }
    if (
        registered["role"] != "candidate"
        or registered["operation"] != "candidate_generation"
        or payload != expected_payload
        or registered["request_payload"]["invocation_context"]
        != expected_context
        or registered["budget_digest"] != budget_digest
    ):
        _fail(
            "materialization_receipt_binding_mismatch",
            "parent producer receipt changed candidate, lenses, context, or budget",
        )
    output = _validate_materialization_output(
        registered["response_payload"]["output"],
        candidate=candidate_value,
        lens_outputs=lens_outputs,
        literature_input=literature_input,
    )
    record_core = {
        "candidate_id": candidate_id,
        "matured_candidate_digest": candidate_digest,
        "lens_output_set_digest": output_set_digest,
        "literature_derived_invention_input_digest": literature_input[
            "content_digest"
        ],
        "parent_conceptual_system": copy.deepcopy(
            output["parent_conceptual_system"]
        ),
        "parent_conceptual_system_digest": output[
            "parent_conceptual_system_digest"
        ],
        "conceptual_delta": copy.deepcopy(output["conceptual_delta"]),
        "conceptual_delta_digest": output["conceptual_delta_digest"],
        "registered_receipt": copy.deepcopy(registered),
        "receipt_file_sha256": summary["receipt_file_sha256"],
        "receipt_byte_length": summary["receipt_byte_length"],
    }
    return {
        **record_core,
        "materialization_record_digest": canonical_digest(record_core),
    }


def run_registered_parent_system_materializations(
    candidates: Sequence[Mapping[str, Any]],
    *,
    lens_execution_bundles: Sequence[Mapping[str, Any]],
    run_root: Path | str,
    matched_budget: Mapping[str, Any] | None = None,
    require_kernel_isolation: bool = False,
    minimum_residency_seconds: float = 0.05,
) -> list[dict[str, Any]]:
    """Author one receipt-backed parent system per exact matured candidate."""

    candidate_rows = [copy.deepcopy(dict(row)) for row in candidates]
    candidate_map = {
        _candidate_parts(row)[0]: row for row in candidate_rows
    }
    if len(candidate_map) != len(candidate_rows) or not candidate_rows:
        _fail(
            "materialization_candidate_bijection_invalid",
            "materialization candidates are empty or repeat identities",
        )
    bundle_map = {
        str(row.get("candidate_id", "")): copy.deepcopy(dict(row))
        for row in lens_execution_bundles
    }
    if set(bundle_map) != set(candidate_map):
        _fail(
            "materialization_lens_bijection_invalid",
            "each candidate requires one exact six-lens execution bundle",
        )
    if (
        not isinstance(minimum_residency_seconds, (int, float))
        or isinstance(minimum_residency_seconds, bool)
        or not 0.0 <= float(minimum_residency_seconds) <= 1.0
    ):
        _fail(
            "residency_invalid",
            "materialization residency must remain in [0, 1]",
        )
    budget = _normalized_budget(matched_budget)
    budget_digest = canonical_digest(budget)
    lens_outputs = {
        candidate_id: _materialization_lens_outputs(
            candidate_map[candidate_id], bundle_map[candidate_id]
        )
        for candidate_id in sorted(candidate_map)
    }
    literature_inputs = {
        candidate_id: _normalized_literature_input(
            bundle_map[candidate_id][
                "literature_derived_invention_input"
            ]
        )
        for candidate_id in sorted(candidate_map)
    }
    study_id = stable_identifier(
        "parent-system-materialization-study",
        {
            candidate_id: {
                "candidate_digest": canonical_digest(
                    candidate_map[candidate_id]
                ),
                "lens_output_set_digest": canonical_digest(
                    lens_outputs[candidate_id]
                ),
                "literature_derived_invention_input_digest": literature_inputs[
                    candidate_id
                ]["content_digest"],
            }
            for candidate_id in sorted(candidate_map)
        },
        budget,
        require_kernel_isolation,
    )
    worker_script = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "run_full_core_reflection_lens_worker.py"
    )
    adapter = ResearchWorkerAdapter(
        study_id=study_id,
        run_root=run_root,
        worker_script=worker_script,
        approved_dependency_paths=(
            Path(__file__).resolve(),
            Path(__file__).resolve().parents[1] / "spec" / SCHEMA_NAME,
        ),
        require_kernel_isolation=require_kernel_isolation,
    )

    def invoke(candidate_id: str) -> dict[str, Any]:
        candidate = candidate_map[candidate_id]
        outputs = lens_outputs[candidate_id]
        candidate_digest = canonical_digest(candidate)
        output_set_digest = canonical_digest(outputs)
        literature_input = literature_inputs[candidate_id]
        return adapter.invoke(
            role="candidate",
            operation="candidate_generation",
            invocation_context={
                "candidate_id": candidate_id,
                "matured_candidate_digest": candidate_digest,
                "lens_output_set_digest": output_set_digest,
                "literature_derived_invention_input_digest": literature_input[
                    "content_digest"
                ],
                "matched_budget_digest": budget_digest,
            },
            payload={
                "matured_candidate": copy.deepcopy(candidate),
                "matured_candidate_digest": candidate_digest,
                "lens_outputs": copy.deepcopy(outputs),
                "lens_output_set_digest": output_set_digest,
                "literature_derived_invention_input": literature_input,
                "literature_derived_invention_input_digest": literature_input[
                    "content_digest"
                ],
                "matched_budget_digest": budget_digest,
                "minimum_residency_seconds": float(
                    minimum_residency_seconds
                ),
            },
            budget=budget,
        )

    receipts: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=len(candidate_map)) as pool:
        futures = {
            pool.submit(invoke, candidate_id): candidate_id
            for candidate_id in sorted(candidate_map)
        }
        for future in as_completed(futures):
            receipts[futures[future]] = future.result()
    return [receipts[candidate_id] for candidate_id in sorted(receipts)]


__all__ = [
    "AUTHORITY_NULLS",
    "CANDIDATE_CORE_FIELDS",
    "FullCoreReflectionLensError",
    "SCHEMA_NAME",
    "SCHEMA_VERSION",
    "build_full_core_reflection_lens_execution_bundle",
    "run_registered_parent_system_materializations",
    "run_full_core_reflection_lenses",
    "validate_full_core_reflection_lens_execution_bundle",
    "validate_parent_system_materialization_receipt",
]
