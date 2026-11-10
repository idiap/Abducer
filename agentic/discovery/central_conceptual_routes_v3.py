# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Canonical five-route conceptual authorship over one verified theory commit.

This module is the authority-bearing successor to the historical four-route
``central_formal_routes`` prototype.  It deliberately starts from one real
``VerifiedCommit`` and reopens the exact committed conceptual input bytes
before any route is named.  Five matched process workers then receive the same
bytes and equal resource budgets:

* a categorical author;
* a HoTT author;
* a Category-then-HoTT author;
* a HoTT-then-Category author; and
* a capable nonformal author.

The workers author their transformation plans *after* the commit boundary by
enumerating finite witnesses in the committed conceptual core.  Callers cannot
supply plans, route outputs, scores, or winners.  The two sequential routes use
the exact critical-pair algebra in :mod:`formal_concept_sequence_algebra`; they
never merge independent common-ancestor deltas.

All routes return through one carrier-specific physics-handback kernel and are
judged by a separate process from content-only projections under a
precommitted, set-valued Pareto rule.  The capable nonformal route is a genuine
competitor and may win or co-win.  Process separation is operational evidence
only: cognitive/semantic independence, creativity, conceptual merit, truth,
theoremhood, continuum control, physics value, and Yang--Mills authority all
remain unavailable.
"""

from __future__ import annotations

import base64
import copy
import fcntl
import json
import os
import secrets
import tempfile
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_identifier,
    validate_instance,
)
from agentic.discovery.budgets import contained_path
from agentic.discovery.research_worker_isolation import (
    ResearchWorkerAdapter,
    ResearchWorkerIntegrityError,
    receipt_summary,
    validate_research_worker_receipt,
)
from agentic.state.discovery_transaction import (
    DiscoveryTransactionStore,
    VerifiedCommit,
)
from skills.common.abstraction_formal_reasoning import (
    FormalReasoningError,
    forge_case_artifact,
    validate_task_derived_artifact,
)
from skills.common.formal_concept_sequence_algebra import (
    DEFAULT_MAX_ISOMORPHISM_PERMUTATIONS,
    build_conditioned_formal_transformation_sequence,
    compare_conceptual_cores,
    unavailable_core_comparison,
    validate_conditioned_formal_transformation_sequence,
)
from skills.common.formal_concept_transformations import (
    FormalConceptTransformationError,
    construct_categorical_transformation,
    construct_hott_transformation,
    seal_conceptual_core,
    validate_conceptual_core,
    validate_semantic_delta,
)


SCHEMA_VERSION = "3.0.0"
COMMITTED_INPUT_VERSION = "3.0.0"
ROUTE_ORDER = (
    "categorical",
    "hott",
    "category_then_hott",
    "hott_then_category",
    "capable_nonformal",
)
FORMAL_ROUTES = frozenset(ROUTE_ORDER[:-1])
SEQUENTIAL_ROUTES = frozenset(
    {"category_then_hott", "hott_then_category"}
)
ADJUDICATION_CRITERIA = (
    "target_relevance",
    "protected_success_preservation",
    "consequence_specificity",
    "burden_localization",
    "unification_compression",
    "discriminating_falsifier",
    "conceptual_depth",
)
_CANDIDATE_ORDER_POLICY = "canonical_opaque_nonce_order_order_ignored"
_BLIND_NONCE_POLICY = {
    "generation": "system_csprng_256_bit_route_independent",
    "presentation": "lexicographic_opaque_nonce",
    "request_protocol_route_labels_absent": True,
    "parent_process_mapping_retained": True,
    "host_mapping_access_denied": False,
    "bindings_publication_stage": "post_judgment_only",
    "randomness_authorized": False,
    "counterbalancing_authorized": False,
}
_NONTRIVIALITY_CONTRACT = {
    "identity_only_policy": "reject",
    "mere_relabeling_policy": "reject",
    "copied_interface_mediator_policy": "reject",
    "vacuous_equivalence_or_coherence_policy": "reject",
    "protected_observable_conservativity_required": True,
    "carrier_semantics_or_countermodel_required": True,
    "finite_hott_scope_replay_required": True,
    "physically_inert_formal_completion_policy": "quarantine",
    "conditioned_order_comparison_stage": (
        "parent_after_both_independently_conditioned_routes_terminal"
    ),
    "comparative_value_authorized": False,
    "physics_value_authorized": False,
}
_CURRENTNESS_BOUNDARIES = frozenset(
    {
        "commission",
        "after_bundle_lock",
        "before_author_launch",
        "before_judge_launch",
        "before_packet_publication",
        "before_cache_return",
        "authoritative_reopen",
        "authoritative_active_prefix_reopen",
    }
)
REGISTRY_PATH = (
    Path(__file__).resolve().parents[1]
    / "registries"
    / "central_conceptual_route_registry_v3.yaml"
)
ROOT = Path(__file__).resolve().parents[2]

_COMMITTED_INPUT_KEYS = {
    "schema_version",
    "input_id",
    "target_id",
    "run_id",
    "source_cycle_id",
    "conceptual_core",
    "literature_projection",
    "conceptual_ancestry_digest",
    "physics_decision_rule",
    "adjudication_rule",
    "authority_boundary",
    "content_digest",
}
_DECISION_RULE_KEYS = {
    "rule_id",
    "target_id",
    "obligation_id",
    "physical_carrier",
    "regime",
    "quantifiers",
    "protected_successes",
    "incumbent_decision",
    "eligible_decision",
    "explanatory_dependency",
    "changed_burden_template",
    "correction",
    "falsifier",
    "physics_next_action",
    "untouched_physics_gates",
    "carrier_predicate",
    "entailment_table",
    "decision_rule_digest",
}
_DECISION_KEYS = {"decision_id", "action", "target_burden_id"}
_CARRIER_PREDICATE_KEYS = {
    "predicate_id",
    "predicate_kind",
    "before_core_digest",
    "target_burden_id",
    "protected_observable_digests",
    "require_exact_carrier_regime_quantifiers",
    "require_changed_core",
    "require_changed_burden",
    "require_finite_relation_witness",
    "nontriviality_contract",
    "counterexample_policy",
    "predicate_digest",
}
_ENTAILMENT_ROW_KEYS = {
    "outcome",
    "predicate_value",
    "decision_id",
    "action_kind",
    "target_burden_id",
}
_ADJUDICATION_RULE_KEYS = {
    "rule_id",
    "judge_rule",
    "route_labels_visible",
    "formal_vocabulary_bonus",
    "capable_nonformal_eligible",
    "content_digest",
}
_JUDGE_RULE_KEYS = {
    "criteria",
    "evidence_statuses",
    "selection_policy",
    "aggregation_policy",
    "ties_allowed",
    "candidate_order_policy",
    "rule_digest",
}
_LITERATURE_KEYS = {
    "snapshot_id",
    "snapshot_digest",
    "production_projection_digest",
    "consume_before",
    "present_use_evaluated_at",
    "present_use_reason",
}
_INPUT_AUTHORITY = {
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
}
_OUTPUT_AUTHORITY = {
    **_INPUT_AUTHORITY,
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
_DEFAULT_AUTHOR_BUDGET = {
    "budget_id": "central-conceptual-matched-author-budget.v3",
    "wall_time_seconds": 30.0,
    "grace_period_seconds": 0.5,
    "cpu_seconds": 30.0,
    "memory_bytes": 512 * 1024 * 1024,
    "disk_bytes": 64 * 1024 * 1024,
    "network_bytes": 0,
    "token_count": 0,
    "request_count": 0,
    "cost_usd": 0.0,
    "absolute_deadline": None,
}


class CentralConceptualRouteError(ValueError):
    """Fail-closed error for the canonical postcommit route protocol."""


def _fail(message: str) -> None:
    raise CentralConceptualRouteError(message)


def _parse_aware_utc_timestamp(value: Any, label: str) -> datetime:
    """Parse an authority-bearing timestamp without accepting local/naive time."""

    rendered = _text(value, label)
    try:
        instant = datetime.fromisoformat(rendered.replace("Z", "+00:00"))
    except ValueError as exc:
        _fail(f"{label} is not an ISO timestamp: {exc}")
    if instant.tzinfo is None or instant.utcoffset() is None:
        _fail(f"{label} must include an explicit UTC offset")
    return instant.astimezone(timezone.utc)


def _system_utc_now() -> datetime:
    """Read the local host clock; this is not an external trusted-time proof."""

    return datetime.now(timezone.utc)


_TEMPORAL_CAPABILITY_SEAL = object()


class _CentralRouteTemporalCapability:
    """Module-issued, non-injectable access to repeated local-clock checks."""

    __slots__ = ("__seal",)

    def __init__(self, seal: object) -> None:
        if seal is not _TEMPORAL_CAPABILITY_SEAL:
            _fail("central route temporal capability is not module-issued")
        self.__seal = seal

    @classmethod
    def issue(cls) -> "_CentralRouteTemporalCapability":
        return cls(_TEMPORAL_CAPABILITY_SEAL)

    def read(self) -> datetime:
        if self.__seal is not _TEMPORAL_CAPABILITY_SEAL:
            _fail("central route temporal capability seal drift")
        instant = _system_utc_now()
        if (
            not isinstance(instant, datetime)
            or instant.tzinfo is None
            or instant.utcoffset() is None
        ):
            _fail("central route local clock did not return an aware instant")
        return instant.astimezone(timezone.utc)


def _strict(raw: Any, keys: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(raw, Mapping):
        _fail(f"{label} must be a mapping")
    if set(raw) != keys:
        _fail(
            f"{label} keys differ; missing={sorted(keys - set(raw))}, "
            f"extra={sorted(set(raw) - keys)}"
        )
    return raw


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(f"{label} must be nonempty text")
    return " ".join(value.split())


def _identifier(value: Any, label: str) -> str:
    try:
        return validate_identifier(value, label)
    except ContractError as exc:
        _fail(str(exc))
    raise AssertionError("unreachable")


def _digest(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value.startswith("sha256:")
        or len(value) != 71
        or any(character not in "0123456789abcdef" for character in value[7:])
    ):
        _fail(f"{label} must be a canonical sha256 digest")
    return value


def _texts(value: Any, label: str, *, minimum: int = 1) -> list[str]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        _fail(f"{label} must be a sequence")
    rows = [_text(item, label) for item in value]
    if len(rows) < minimum or len(rows) != len(set(rows)):
        _fail(f"{label} is incomplete or duplicated")
    return rows


def _seal(raw: Mapping[str, Any], digest_field: str) -> dict[str, Any]:
    result = copy.deepcopy(dict(raw))
    result.pop(digest_field, None)
    result[digest_field] = canonical_digest(result)
    return result


def _validate_self_digest(
    raw: Mapping[str, Any], digest_field: str, label: str
) -> None:
    claimed = _digest(raw.get(digest_field), f"{label}.{digest_field}")
    expected = canonical_digest(
        {key: value for key, value in raw.items() if key != digest_field}
    )
    if claimed != expected:
        _fail(f"{label} has a stale {digest_field}")


def _validate_decision(raw: Any, label: str) -> dict[str, Any]:
    decision = copy.deepcopy(dict(_strict(raw, _DECISION_KEYS, label)))
    _identifier(decision["decision_id"], f"{label}.decision_id")
    _text(decision["action"], f"{label}.action")
    _identifier(decision["target_burden_id"], f"{label}.target_burden_id")
    return decision


def _canonical_eligible_action(
    rule: Mapping[str, Any], predicate: Mapping[str, Any]
) -> str:
    """Derive the only action a satisfied finite predicate may authorize."""

    return (
        "Inspect the exact witnessed finite carrier delta for predicate "
        f"{predicate['predicate_id']} on {rule['physical_carrier']} against "
        f"every protected observable before escalating burden "
        f"{predicate['target_burden_id']} to theorem or continuum claims."
    )


def validate_physics_decision_rule(raw: Any) -> dict[str, Any]:
    """Validate one carrier-specific rule committed before route authorship."""

    rule = copy.deepcopy(dict(_strict(raw, _DECISION_RULE_KEYS, "physics decision rule")))
    _identifier(rule["rule_id"], "physics decision rule.rule_id")
    _identifier(rule["target_id"], "physics decision rule.target_id")
    _identifier(rule["obligation_id"], "physics decision rule.obligation_id")
    for field in (
        "physical_carrier",
        "regime",
        "explanatory_dependency",
        "changed_burden_template",
        "correction",
        "falsifier",
        "physics_next_action",
    ):
        _text(rule[field], f"physics decision rule.{field}")
    _texts(rule["quantifiers"], "physics decision rule.quantifiers")
    _texts(
        rule["protected_successes"],
        "physics decision rule.protected_successes",
        minimum=2,
    )
    _texts(
        rule["untouched_physics_gates"],
        "physics decision rule.untouched_physics_gates",
    )
    incumbent = _validate_decision(rule["incumbent_decision"], "incumbent decision")
    eligible = _validate_decision(rule["eligible_decision"], "eligible decision")
    if incumbent == eligible or incumbent["target_burden_id"] != eligible["target_burden_id"]:
        _fail("physics decisions must change one action on the same declared burden")
    predicate = copy.deepcopy(
        dict(
            _strict(
                rule["carrier_predicate"],
                _CARRIER_PREDICATE_KEYS,
                "finite carrier predicate",
            )
        )
    )
    _identifier(predicate["predicate_id"], "finite carrier predicate.predicate_id")
    if predicate["predicate_kind"] != (
        "finite_carrier_nontriviality_conservativity_and_obstruction_predicate"
    ):
        _fail("physics decision rule uses an unregistered carrier predicate")
    _digest(
        predicate["before_core_digest"],
        "finite carrier predicate.before_core_digest",
    )
    _identifier(
        predicate["target_burden_id"],
        "finite carrier predicate.target_burden_id",
    )
    protected_digests = predicate["protected_observable_digests"]
    if (
        not isinstance(protected_digests, list)
        or len(protected_digests) < 2
        or protected_digests != sorted(set(protected_digests))
    ):
        _fail("finite carrier predicate must bind two sorted protected observables")
    for digest in protected_digests:
        _digest(digest, "finite carrier predicate.protected_observable_digests")
    for field in (
        "require_exact_carrier_regime_quantifiers",
        "require_changed_core",
        "require_changed_burden",
        "require_finite_relation_witness",
    ):
        if predicate[field] is not True:
            _fail(f"finite carrier predicate weakens {field}")
    if predicate["nontriviality_contract"] != _NONTRIVIALITY_CONTRACT:
        _fail("finite carrier predicate nontriviality contract drift")
    if predicate["counterexample_policy"] != (
        "any_protected_observable_or_member_value_change_fails"
    ):
        _fail("finite carrier predicate counterexample policy drift")
    _validate_self_digest(predicate, "predicate_digest", "finite carrier predicate")
    table = rule["entailment_table"]
    if not isinstance(table, list) or len(table) != 2:
        _fail("physics decision rule requires an exact two-row entailment table")
    table = [
        copy.deepcopy(
            dict(_strict(row, _ENTAILMENT_ROW_KEYS, "physics entailment row"))
        )
        for row in table
    ]
    expected_table = [
        {
            "outcome": "predicate_failed",
            "predicate_value": False,
            "decision_id": incumbent["decision_id"],
            "action_kind": "retain_incumbent",
            "target_burden_id": incumbent["target_burden_id"],
        },
        {
            "outcome": "predicate_satisfied",
            "predicate_value": True,
            "decision_id": eligible["decision_id"],
            "action_kind": "inspect_witnessed_finite_carrier_delta",
            "target_burden_id": eligible["target_burden_id"],
        },
    ]
    if table != expected_table:
        _fail("physics decision entailment table is not the exact two-row function")
    if eligible["action"] != _canonical_eligible_action(rule, predicate):
        _fail("eligible action is not derived from the finite carrier predicate")
    _validate_self_digest(rule, "decision_rule_digest", "physics decision rule")
    return rule


def validate_adjudication_rule(raw: Any) -> dict[str, Any]:
    """Validate the blind, method-neutral selection rule frozen precommit."""

    rule = copy.deepcopy(dict(_strict(raw, _ADJUDICATION_RULE_KEYS, "adjudication rule")))
    _identifier(rule["rule_id"], "adjudication rule.rule_id")
    judge_rule = copy.deepcopy(
        dict(
            _strict(
                rule["judge_rule"], _JUDGE_RULE_KEYS, "adjudication judge rule"
            )
        )
    )
    if tuple(judge_rule["criteria"]) != ADJUDICATION_CRITERIA:
        _fail("adjudication criteria or order differs from the canonical seven criteria")
    if (
        judge_rule["evidence_statuses"] != ["failed", "partial", "satisfied"]
        or judge_rule["selection_policy"] != "set_valued_pareto_nondomination"
        or judge_rule["aggregation_policy"] != "no_scalar_aggregation"
        or judge_rule["ties_allowed"] is not True
        or judge_rule["candidate_order_policy"]
        != _CANDIDATE_ORDER_POLICY
        or rule["route_labels_visible"] is not False
        or rule["formal_vocabulary_bonus"] is not False
        or rule["capable_nonformal_eligible"] is not True
    ):
        _fail("adjudication rule weakens blind equal-opportunity selection")
    _validate_self_digest(judge_rule, "rule_digest", "adjudication judge rule")
    rule["judge_rule"] = judge_rule
    _validate_self_digest(rule, "content_digest", "adjudication rule")
    return rule


def validate_committed_route_input(raw: Any) -> dict[str, Any]:
    """Validate the exact plan-free conceptual input stored in a theory commit."""

    payload = copy.deepcopy(dict(_strict(raw, _COMMITTED_INPUT_KEYS, "committed route input")))
    try:
        validate_instance(payload, "central_conceptual_route_input_v3.schema.json")
    except ContractError as exc:
        _fail(f"committed route input schema failure: {exc}")
    if payload["schema_version"] != COMMITTED_INPUT_VERSION:
        _fail("committed route input version drift")
    for field in ("input_id", "target_id", "run_id", "source_cycle_id"):
        _identifier(payload[field], f"committed route input.{field}")
    core = validate_conceptual_core(payload["conceptual_core"])
    literature = copy.deepcopy(
        dict(_strict(payload["literature_projection"], _LITERATURE_KEYS, "literature projection"))
    )
    for field in ("snapshot_id", "present_use_reason"):
        _text(literature[field], f"literature projection.{field}")
    for field in ("snapshot_digest", "production_projection_digest"):
        _digest(literature[field], f"literature projection.{field}")
    consume_before = _parse_aware_utc_timestamp(
        literature["consume_before"], "literature projection.consume_before"
    )
    evaluated_at = _parse_aware_utc_timestamp(
        literature["present_use_evaluated_at"],
        "literature projection.present_use_evaluated_at",
    )
    if evaluated_at >= consume_before:
        _fail("committed literature was not current at its recorded present use")
    ancestry_digest = _digest(
        payload["conceptual_ancestry_digest"],
        "committed route input.conceptual_ancestry_digest",
    )
    decision_rule = validate_physics_decision_rule(payload["physics_decision_rule"])
    adjudication_rule = validate_adjudication_rule(payload["adjudication_rule"])
    if payload["authority_boundary"] != _INPUT_AUTHORITY:
        _fail("committed route input authority boundary drift")
    if (
        payload["target_id"] != core["target_id"]
        or decision_rule["target_id"] != core["target_id"]
        or decision_rule["obligation_id"] != core["obligation_id"]
        or decision_rule["physical_carrier"] != core["physical_carrier"]
        or decision_rule["regime"] != core["regime"]
        or decision_rule["quantifiers"]
        != [row["statement"] for row in core["quantifiers"]]
    ):
        _fail("physics decision rule is detached from the exact conceptual core")
    predicate = decision_rule["carrier_predicate"]
    protected_digests = sorted(
        canonical_digest(row)
        for row in core["observables"]
        if row["protected"]
    )
    if (
        predicate["before_core_digest"] != core["content_digest"]
        or predicate["target_burden_id"]
        != decision_rule["incumbent_decision"]["target_burden_id"]
        or predicate["protected_observable_digests"] != protected_digests
        or not any(
            row["burden_id"] == predicate["target_burden_id"]
            for row in core["burdens"]
        )
    ):
        _fail("finite carrier predicate is detached from the exact core or burden")
    expected_input_id = stable_identifier(
        "central-conceptual-route-input-v3",
        payload["target_id"],
        payload["run_id"],
        payload["source_cycle_id"],
        core["content_digest"],
        literature,
        ancestry_digest,
        decision_rule["decision_rule_digest"],
        adjudication_rule["content_digest"],
    )
    if payload["input_id"] != expected_input_id:
        _fail("committed route input ID is not derived from its exact plan-free content")
    _validate_self_digest(payload, "content_digest", "committed route input")
    return payload


def build_committed_route_input(
    *,
    target_id: str,
    run_id: str,
    source_cycle_id: str,
    conceptual_core: Mapping[str, Any],
    literature_projection: Mapping[str, Any],
    conceptual_ancestry_digest: str,
    physics_decision_rule: Mapping[str, Any],
    adjudication_rule: Mapping[str, Any],
) -> dict[str, Any]:
    """Build the plan-free artifact that must be committed before five authors run."""

    core = validate_conceptual_core(conceptual_core)
    material = {
        "schema_version": COMMITTED_INPUT_VERSION,
        "target_id": _identifier(target_id, "target_id"),
        "run_id": _identifier(run_id, "run_id"),
        "source_cycle_id": _identifier(source_cycle_id, "source_cycle_id"),
        "conceptual_core": core,
        "literature_projection": copy.deepcopy(dict(literature_projection)),
        "conceptual_ancestry_digest": _digest(
            conceptual_ancestry_digest, "conceptual_ancestry_digest"
        ),
        "physics_decision_rule": validate_physics_decision_rule(physics_decision_rule),
        "adjudication_rule": validate_adjudication_rule(adjudication_rule),
        "authority_boundary": copy.deepcopy(_INPUT_AUTHORITY),
    }
    material["input_id"] = stable_identifier(
        "central-conceptual-route-input-v3",
        material["target_id"],
        material["run_id"],
        material["source_cycle_id"],
        core["content_digest"],
        material["literature_projection"],
        material["conceptual_ancestry_digest"],
        material["physics_decision_rule"]["decision_rule_digest"],
        material["adjudication_rule"]["content_digest"],
    )
    return validate_committed_route_input(_seal(material, "content_digest"))


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _fail(f"central route registry repeats key {key!r}")
        result[key] = value
    return result


def load_central_route_registry(path: Path = REGISTRY_PATH) -> tuple[dict[str, Any], bytes]:
    """Load the exact five-author registry and bind every local dependency byte."""

    if path.is_symlink() or not path.is_file():
        _fail("central route registry must be one regular file")
    data = path.read_bytes()
    try:
        registry = json.loads(data, object_pairs_hook=_object_without_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail(f"central route registry is not JSON-compatible YAML: {exc}")
    if not isinstance(registry, dict) or set(registry) != {
        "schema_version",
        "registry_id",
        "execution_contract",
        "routes",
        "judge",
        "authority_boundary",
    }:
        _fail("central route registry root contract drift")
    if registry["schema_version"] != SCHEMA_VERSION or registry["registry_id"] != (
        "central-formal-conceptual-routes.v3"
    ):
        _fail("central route registry identity drift")
    execution = registry["execution_contract"]
    if execution != {
        "backend": "research_worker_process_wave",
        "max_workers": 5,
        "terminal_barrier_parties": 5,
        "identical_committed_input_bytes": True,
        "equal_resource_budgets": True,
        "process_overlap_required": True,
        "caller_plans_forbidden": True,
        "experiments": "secondary_theory_requested_falsifiers_only",
    }:
        _fail("central route registry execution contract drift")
    rows = registry["routes"]
    if not isinstance(rows, list) or [row.get("route_id") for row in rows] != list(ROUTE_ORDER):
        _fail("central route registry must contain the exact ordered five routes")
    producer_ids: set[str] = set()
    for route_id, row in zip(ROUTE_ORDER, rows, strict=True):
        if not isinstance(row, Mapping) or set(row) != {
            "route_id",
            "producer_id",
            "author_kind",
            "worker_role",
            "worker_operation",
            "dependency_paths",
        }:
            _fail(f"central route registry row drift for {route_id}")
        producer_ids.add(_identifier(row["producer_id"], f"{route_id}.producer_id"))
        if (
            row["route_id"] != route_id
            or row["worker_role"] != "formal_lens"
            or row["worker_operation"] != "formal_lens"
            or row["author_kind"]
            != {
                "categorical": "finite_categorical_concept_author",
                "hott": "finite_hott_concept_author",
                "category_then_hott": "ordered_category_then_hott_author",
                "hott_then_category": "ordered_hott_then_category_author",
                "capable_nonformal": "capable_nonformal_concept_author",
            }[route_id]
        ):
            _fail(f"central route registry author binding drift for {route_id}")
        dependencies = row["dependency_paths"]
        if not isinstance(dependencies, list) or not dependencies or len(dependencies) != len(set(dependencies)):
            _fail(f"central route {route_id} dependency paths are incomplete or duplicated")
        for raw_path in dependencies:
            if not isinstance(raw_path, str) or PurePosixPath(raw_path).is_absolute() or ".." in PurePosixPath(raw_path).parts:
                _fail(f"central route {route_id} dependency path is unsafe")
            dependency = ROOT.joinpath(*PurePosixPath(raw_path).parts)
            if dependency.is_symlink() or not dependency.is_file():
                _fail(f"central route {route_id} dependency is missing: {raw_path}")
    if len(producer_ids) != len(ROUTE_ORDER):
        _fail("central route producer identities are not distinct")
    judge = registry["judge"]
    expected_judge = {
        "judge_id": "blind-content-pareto-judge.v3",
        "study_id": "blind-conceptual-judge-v3",
        "worker_role": "judge",
        "worker_operation": "blind_judgment",
        "worker_script": "agentic/scripts/run_blind_conceptual_judge_v3.py",
        "dependency_paths": [
            "agentic/discovery/blind_conceptual_judge_v3.py",
            "agentic/scripts/run_blind_conceptual_judge_v3.py",
            "agentic/spec/blind_conceptual_judge_input_v3.schema.json",
            "agentic/spec/blind_conceptual_judge_output_v3.schema.json",
        ],
        "information_domain": (
            "opaque_nonces_plus_seven_typed_status_ledgers_only"
        ),
        "selection_policy": "set_valued_pareto_nondomination",
        "route_labels_visible": False,
        "method_bonus": False,
    }
    if judge != expected_judge:
        _fail("central route blind judge binding drift")
    for raw_path in judge["dependency_paths"]:
        if (
            not isinstance(raw_path, str)
            or PurePosixPath(raw_path).is_absolute()
            or ".." in PurePosixPath(raw_path).parts
        ):
            _fail("central route blind judge dependency path is unsafe")
        dependency = ROOT.joinpath(*PurePosixPath(raw_path).parts)
        if dependency.is_symlink() or not dependency.is_file():
            _fail(f"central route blind judge dependency is missing: {raw_path}")
    if registry["authority_boundary"] != _OUTPUT_AUTHORITY:
        _fail("central route registry authority boundary drift")
    binding = copy.deepcopy(registry)
    binding["registry_file_sha256"] = bytes_digest(data)
    binding["registry_byte_length"] = len(data)
    route_descriptors = []
    for raw_path in sorted(
        {
            value
            for row in rows
            for value in row["dependency_paths"]
        }
    ):
        dependency_data = ROOT.joinpath(*PurePosixPath(raw_path).parts).read_bytes()
        route_descriptors.append(
            {
                "path": raw_path,
                "sha256": bytes_digest(dependency_data),
                "byte_length": len(dependency_data),
            }
        )
    judge_descriptors = []
    for raw_path in sorted(judge["dependency_paths"]):
        dependency_data = ROOT.joinpath(*PurePosixPath(raw_path).parts).read_bytes()
        judge_descriptors.append(
            {
                "path": raw_path,
                "sha256": bytes_digest(dependency_data),
                "byte_length": len(dependency_data),
            }
        )
    binding["route_dependency_descriptors"] = route_descriptors
    binding["judge_dependency_descriptors"] = judge_descriptors
    binding["binding_digest"] = canonical_digest(binding)
    return binding, data


def _commit_identity(commit: VerifiedCommit) -> dict[str, Any]:
    return {
        "generation": commit.generation,
        "prior_generation": commit.prior_generation,
        "commit_id": commit.commit_id,
        "manifest_digest": commit.manifest_digest,
        "state_file_digest": commit.state_file_digest,
        "state_semantic_digest": commit.state_semantic_digest,
    }


def _manifest_descriptor(commit: VerifiedCommit, relative_path: str) -> dict[str, Any]:
    matches = [
        copy.deepcopy(dict(row))
        for row in commit.manifest.get("artifacts", [])
        if isinstance(row, Mapping) and row.get("path") == relative_path
    ]
    if len(matches) != 1:
        _fail("verified commit lacks the exact central route input artifact")
    return matches[0]


def commission_from_verified_commit(
    *,
    store: DiscoveryTransactionStore,
    verified_commit: VerifiedCommit,
    committed_input_path: str,
    worker_budget: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Reopen the current commit and capture its exact canonical input bytes once."""

    if type(store) is not DiscoveryTransactionStore or type(verified_commit) is not VerifiedCommit:
        _fail("central conceptual authorship requires a real store and VerifiedCommit")
    try:
        normalized_path = PurePosixPath(committed_input_path)
    except TypeError as exc:
        _fail(f"committed input path is invalid: {exc}")
    if (
        normalized_path.is_absolute()
        or normalized_path.as_posix() != committed_input_path
        or any(part in {"", ".", ".."} for part in normalized_path.parts)
    ):
        _fail("committed input path is not a safe canonical relative path")
    with store.verified_artifact_context() as context:
        if context.current_generation != verified_commit.generation:
            _fail("central route input commit is not the current verified theory head")
        reopened, artifacts = context.read_artifacts(
            verified_commit.generation, [committed_input_path]
        )
    if _commit_identity(reopened) != _commit_identity(verified_commit):
        _fail("supplied VerifiedCommit differs from the store-reopened commit")
    data = artifacts[committed_input_path]
    try:
        raw = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail(f"committed central route input is not UTF-8 JSON: {exc}")
    payload = validate_committed_route_input(raw)
    canonical_bytes = canonical_json(payload) + b"\n"
    if data != canonical_bytes:
        _fail("committed central route input bytes are not the exact canonical packet")
    descriptor = _manifest_descriptor(reopened, committed_input_path)
    if descriptor.get("sha256") != bytes_digest(data) or descriptor.get("size_bytes") != len(data):
        _fail("committed central route input differs from its verified manifest descriptor")
    registry_binding, _ = load_central_route_registry()
    budget = copy.deepcopy(dict(worker_budget or _DEFAULT_AUTHOR_BUDGET))
    commission = {
        "schema_version": SCHEMA_VERSION,
        "commission_id": stable_identifier(
            "central-conceptual-route-commission-v3",
            _commit_identity(reopened),
            descriptor,
            payload["content_digest"],
            registry_binding["binding_digest"],
            budget,
        ),
        "verified_commit": _commit_identity(reopened),
        "committed_input_path": committed_input_path,
        "committed_input_descriptor": descriptor,
        "committed_input_sha256": bytes_digest(data),
        "committed_input_byte_length": len(data),
        "committed_input_base64": base64.b64encode(data).decode("ascii"),
        "committed_input_content_digest": payload["content_digest"],
        "registry_binding": registry_binding,
        "worker_budget": budget,
        "route_fault_modes": {route_id: None for route_id in ROUTE_ORDER},
        "authority_boundary": copy.deepcopy(_OUTPUT_AUTHORITY),
    }
    commission["commission_digest"] = canonical_digest(commission)
    _revalidate_live_commission(
        store=store,
        commission=commission,
        temporal=_CentralRouteTemporalCapability.issue(),
        boundary="commission",
    )
    return commission


def _decode_committed_input(commission: Mapping[str, Any]) -> dict[str, Any]:
    try:
        data = base64.b64decode(
            commission["committed_input_base64"], validate=True
        )
    except (KeyError, TypeError, ValueError) as exc:
        _fail(f"commission does not carry exact committed input bytes: {exc}")
    if (
        bytes_digest(data) != commission.get("committed_input_sha256")
        or len(data) != commission.get("committed_input_byte_length")
    ):
        _fail("commission committed input bytes differ from their descriptor")
    try:
        raw = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail(f"commission committed input is invalid: {exc}")
    payload = validate_committed_route_input(raw)
    if (
        data != canonical_json(payload) + b"\n"
        or payload["content_digest"] != commission.get("committed_input_content_digest")
    ):
        _fail("commission input is not the exact canonical committed packet")
    return payload


def _revalidate_live_commission(
    *,
    store: DiscoveryTransactionStore,
    commission: Mapping[str, Any],
    temporal: _CentralRouteTemporalCapability,
    boundary: str,
    require_current_head: bool = True,
) -> dict[str, Any]:
    """Reopen input/dependencies and enforce head or active-prefix authority.

    Authorship and first publication require the commissioning generation to
    remain the current head.  A later canonical consumer instead needs the
    exact source commit to remain in the verified active prefix after its
    descendant was committed.  The latter is a lineage check, not permission
    to author new route output from a stale source.
    """

    if (
        type(store) is not DiscoveryTransactionStore
        or type(temporal) is not _CentralRouteTemporalCapability
        or boundary not in _CURRENTNESS_BOUNDARIES
    ):
        _fail("central route currentness recheck lacks governed authority")
    committed = _decode_committed_input(commission)
    if (
        committed["target_id"] != store.target_id
        or committed["run_id"] != store.run_id
    ):
        _fail(f"{boundary}: committed input belongs to a different target/run")
    try:
        generation = commission["verified_commit"]["generation"]
        relative_path = commission["committed_input_path"]
    except (KeyError, TypeError) as exc:
        _fail(f"{boundary}: commission currentness identity is incomplete: {exc}")
    with store.verified_artifact_context() as context:
        if require_current_head and context.current_generation != generation:
            _fail(f"{boundary}: verified theory head advanced after commission")
        if not require_current_head and context.current_generation < generation:
            _fail(f"{boundary}: source generation is not in the verified active prefix")
        reopened, artifacts = context.read_artifacts(generation, [relative_path])
    data = artifacts[relative_path]
    descriptor = _manifest_descriptor(reopened, relative_path)
    if (
        _commit_identity(reopened) != commission.get("verified_commit")
        or descriptor != commission.get("committed_input_descriptor")
        or bytes_digest(data) != commission.get("committed_input_sha256")
        or len(data) != commission.get("committed_input_byte_length")
    ):
        _fail(f"{boundary}: authoritative committed input was substituted")
    try:
        embedded = base64.b64decode(
            commission["committed_input_base64"], validate=True
        )
    except (KeyError, TypeError, ValueError) as exc:
        _fail(f"{boundary}: commission input bytes cannot be reopened: {exc}")
    if data != embedded:
        _fail(f"{boundary}: committed bytes differ from the immutable theory bundle")
    registry_binding, _ = load_central_route_registry()
    if registry_binding != commission.get("registry_binding"):
        _fail(f"{boundary}: route or judge dependency binding changed")
    literature = committed["literature_projection"]
    evaluated_at = _parse_aware_utc_timestamp(
        literature["present_use_evaluated_at"],
        "literature projection.present_use_evaluated_at",
    )
    consume_before = _parse_aware_utc_timestamp(
        literature["consume_before"], "literature projection.consume_before"
    )
    now = temporal.read()
    if now < evaluated_at:
        _fail(f"{boundary}: local clock precedes the recorded literature evaluation")
    if now >= consume_before:
        _fail(f"{boundary}: committed literature consume-before deadline expired")
    return committed


def _relation_action(relation: Mapping[str, Any]) -> dict[str, str]:
    return {
        str(row["source_member_id"]): str(row["target_member_id"])
        for row in relation["action"]
    }


def _compose_relations(
    first: Mapping[str, Any], second: Mapping[str, Any]
) -> tuple[tuple[str, str], ...] | None:
    if first["target_primitive_id"] != second["source_primitive_id"]:
        return None
    left = _relation_action(first)
    right = _relation_action(second)
    if any(value not in right for value in left.values()):
        return None
    return tuple(sorted((source, right[middle]) for source, middle in left.items()))


def _path_composite(
    core: Mapping[str, Any], relation_ids: Sequence[str]
) -> tuple[str, str, dict[str, str]] | None:
    relations = {
        row["relation_id"]: row for row in core["relations"]
    }
    if len(relation_ids) < 1 or any(item not in relations for item in relation_ids):
        return None
    selected = [relations[item] for item in relation_ids]
    action = _relation_action(selected[0])
    for index, relation in enumerate(selected[1:], start=1):
        next_action = _relation_action(relation)
        if (
            selected[index - 1]["target_primitive_id"]
            != relation["source_primitive_id"]
            or any(value not in next_action for value in action.values())
        ):
            return None
        action = {
            source: next_action[middle] for source, middle in action.items()
        }
    return (
        selected[0]["source_primitive_id"],
        selected[-1]["target_primitive_id"],
        action,
    )


def _leg_action(
    raw: Any,
    *,
    source_members: Sequence[str],
    target_members: Sequence[str],
) -> dict[str, str] | None:
    """Decode one proposed finite leg without weakening the shared constructor.

    The relation-specific kernel remains the construction authority.  This
    local decoder exists only so route planning and later nontriviality replay
    can independently reconstruct the exact pointwise scope before invoking
    that kernel.
    """

    if not isinstance(raw, Mapping) or set(raw) != {
        "relation_id",
        "statement",
        "action",
    }:
        return None
    action_rows = raw.get("action")
    if not isinstance(action_rows, list) or len(action_rows) != len(
        source_members
    ):
        return None
    result: dict[str, str] = {}
    for expected_source, row in zip(
        source_members, action_rows, strict=True
    ):
        if (
            not isinstance(row, Mapping)
            or set(row) != {"source_member_id", "target_member_id"}
            or row.get("source_member_id") != expected_source
            or row.get("target_member_id") not in target_members
            or expected_source in result
        ):
            return None
        result[expected_source] = str(row["target_member_id"])
    return result


def _transport_values(
    values: Mapping[str, Any],
    action: Mapping[str, str],
    target_members: Sequence[str],
) -> dict[str, Any] | None:
    """Transport one finite observable when every target fiber is coherent."""

    if set(values) != set(action):
        return None
    fibers: dict[str, list[str]] = {
        target_member: [] for target_member in target_members
    }
    for source_member, target_member in action.items():
        if target_member not in fibers:
            return None
        fibers[target_member].append(source_member)
    transported: dict[str, Any] = {}
    for target_member in target_members:
        sources = fibers[target_member]
        if not sources:
            return None
        distinct = {
            canonical_json(values[source_member])
            for source_member in sources
        }
        if len(distinct) != 1:
            return None
        transported[target_member] = values[sources[0]]
    return transported


def _protected_transport_chain(
    core: Mapping[str, Any],
    *,
    source_primitive_id: str,
    steps: Sequence[
        tuple[str, str, Mapping[str, str], Sequence[str]]
    ],
    require_registered_target: bool,
) -> list[dict[str, Any]] | None:
    """Replay protected observables through a finite chain of total maps."""

    source_observables = sorted(
        (
            row
            for row in core["observables"]
            if row["protected"]
            and row["carrier_primitive_id"] == source_primitive_id
        ),
        key=lambda row: row["observable_id"],
    )
    if not source_observables or not steps:
        return None
    final_target_id = steps[-1][1]
    registered_targets = sorted(
        (
            row
            for row in core["observables"]
            if row["protected"]
            and row["carrier_primitive_id"] == final_target_id
        ),
        key=lambda row: row["observable_id"],
    )
    rows: list[dict[str, Any]] = []
    for observable in source_observables:
        current_values = {
            row["member_id"]: row["value"]
            for row in observable["evaluations"]
        }
        step_rows: list[dict[str, Any]] = []
        current_primitive_id = source_primitive_id
        for relation_id, target_id, action, target_members in steps:
            transported = _transport_values(
                current_values, action, target_members
            )
            if transported is None:
                return None
            step_rows.append(
                {
                    "relation_id": relation_id,
                    "source_primitive_id": current_primitive_id,
                    "target_primitive_id": target_id,
                    "transported_values_digest": canonical_digest(
                        [
                            {
                                "member_id": member_id,
                                "value": transported[member_id],
                            }
                            for member_id in target_members
                        ]
                    ),
                }
            )
            current_values = transported
            current_primitive_id = target_id
        matching_targets = [
            row["observable_id"]
            for row in registered_targets
            if {
                item["member_id"]: item["value"]
                for item in row["evaluations"]
            }
            == current_values
        ]
        if require_registered_target and not matching_targets:
            return None
        rows.append(
            {
                "source_observable_id": observable["observable_id"],
                "target_observable_ids": matching_targets,
                "steps": step_rows,
                "pointwise_values_preserved": True,
            }
        )
    return rows


def _graph_mediator_witness(
    core: Mapping[str, Any], direct: Mapping[str, Any]
) -> dict[str, Any]:
    """Construct the finite graph factorization of one declared map."""

    primitives = {
        row["primitive_id"]: row for row in core["primitives"]
    }
    source = primitives[direct["source_primitive_id"]]
    action = _relation_action(direct)
    mediator_id = stable_identifier(
        "central-graph-mediator-v3",
        core["target_id"],
        direct["relation_id"],
        direct["action"],
    )
    mediator_members = [
        stable_identifier(
            "central-graph-mediator-member-v3",
            mediator_id,
            source_member,
            action[source_member],
        )
        for source_member in source["member_ids"]
    ]
    return {
        "witness_kind": "mediator_factorization",
        "direct_relation_id": direct["relation_id"],
        "mediator": {
            "primitive_id": mediator_id,
            "statement": (
                "Finite graph carrier whose members retain each declared "
                f"{direct['relation_id']} source-target pair."
            ),
            "member_ids": mediator_members,
        },
        "first_leg": {
            "relation_id": stable_identifier(
                "central-graph-first-leg-v3", mediator_id
            ),
            "statement": (
                "Embed each source member into its explicit graph pair."
            ),
            "action": [
                {
                    "source_member_id": source_member,
                    "target_member_id": mediator_member,
                }
                for source_member, mediator_member in zip(
                    source["member_ids"], mediator_members, strict=True
                )
            ],
        },
        "second_leg": {
            "relation_id": stable_identifier(
                "central-graph-second-leg-v3", mediator_id
            ),
            "statement": (
                "Project each graph pair to its declared target member."
            ),
            "action": [
                {
                    "source_member_id": mediator_member,
                    "target_member_id": action[source_member],
                }
                for source_member, mediator_member in zip(
                    source["member_ids"], mediator_members, strict=True
                )
            ],
        },
    }


def _mediator_scope(
    core: Mapping[str, Any], witness: Mapping[str, Any]
) -> dict[str, Any] | None:
    """Reconstruct a positive, non-copying finite mediator factorization."""

    relations = {
        row["relation_id"]: row for row in core["relations"]
    }
    primitives = {
        row["primitive_id"]: row for row in core["primitives"]
    }
    direct = relations.get(witness.get("direct_relation_id"))
    mediator = witness.get("mediator")
    if (
        direct is None
        or not isinstance(mediator, Mapping)
        or set(mediator) != {"primitive_id", "statement", "member_ids"}
        or direct["source_primitive_id"] == direct["target_primitive_id"]
    ):
        return None
    source = primitives[direct["source_primitive_id"]]
    target = primitives[direct["target_primitive_id"]]
    mediator_id = mediator.get("primitive_id")
    mediator_members = mediator.get("member_ids")
    occupied_members = {
        member_id
        for primitive in core["primitives"]
        for member_id in primitive["member_ids"]
    }
    if (
        not isinstance(mediator_id, str)
        or mediator_id in primitives
        or mediator_id
        in {source["primitive_id"], target["primitive_id"]}
        or not isinstance(mediator_members, list)
        or len(mediator_members) != len(source["member_ids"])
        or len(set(mediator_members)) != len(mediator_members)
        or bool(set(mediator_members) & occupied_members)
        or mediator.get("statement")
        in {source["statement"], target["statement"]}
    ):
        return None
    first = _leg_action(
        witness.get("first_leg"),
        source_members=source["member_ids"],
        target_members=mediator_members,
    )
    second = _leg_action(
        witness.get("second_leg"),
        source_members=mediator_members,
        target_members=target["member_ids"],
    )
    if first is None or second is None:
        return None
    direct_action = _relation_action(direct)
    composite = {
        source_member: second[first[source_member]]
        for source_member in source["member_ids"]
    }
    if composite != direct_action:
        return None
    transport_rows = _protected_transport_chain(
        core,
        source_primitive_id=source["primitive_id"],
        steps=[
            (
                str(witness["first_leg"]["relation_id"]),
                str(mediator_id),
                first,
                mediator_members,
            ),
            (
                str(witness["second_leg"]["relation_id"]),
                target["primitive_id"],
                second,
                target["member_ids"],
            ),
        ],
        require_registered_target=True,
    )
    if not transport_rows:
        return None
    return {
        "scope_kind": "finite_graph_mediator_factorization",
        "direct_relation_id": direct["relation_id"],
        "source_carrier_binding": {
            "primitive_id": source["primitive_id"],
            "primitive_digest": canonical_digest(source),
        },
        "mediator_carrier_binding": {
            "primitive_id": mediator_id,
            "primitive_digest": canonical_digest(mediator),
        },
        "target_carrier_binding": {
            "primitive_id": target["primitive_id"],
            "primitive_digest": canonical_digest(target),
        },
        "first_leg_relation_id": witness["first_leg"]["relation_id"],
        "second_leg_relation_id": witness["second_leg"]["relation_id"],
        "pointwise_factorization_rows": [
            {
                "source_member_id": source_member,
                "mediator_member_id": first[source_member],
                "factored_target_member_id": composite[source_member],
                "direct_target_member_id": direct_action[source_member],
            }
            for source_member in source["member_ids"]
        ],
        "protected_transport_rows": transport_rows,
        "mediator_distinct_from_endpoints": True,
        "mediator_members_disjoint_from_registered_carriers": True,
        "copied_interface_authorized": False,
        "existence_scope": "one_exact_declared_finite_graph_factorization",
        "uniqueness_scope": "not_claimed",
        "universal_property_authorized": False,
        "continuum_scope_authorized": False,
    }


def _functorial_witness(
    core: Mapping[str, Any], source_relation: Mapping[str, Any]
) -> dict[str, Any]:
    """Build a finite representation-change square from one declared map."""

    primitives = {
        row["primitive_id"]: row for row in core["primitives"]
    }
    source = primitives[source_relation["source_primitive_id"]]
    target = primitives[source_relation["target_primitive_id"]]
    transfer_id = stable_identifier(
        "central-functorial-transfer-v3",
        core["target_id"],
        source_relation["relation_id"],
        source_relation["action"],
    )
    transferred_source_id = stable_identifier(
        "central-transferred-source-v3", transfer_id
    )
    transferred_target_id = stable_identifier(
        "central-transferred-target-v3", transfer_id
    )
    transferred_source_members = [
        stable_identifier(
            "central-transferred-source-member-v3",
            transfer_id,
            member_id,
        )
        for member_id in source["member_ids"]
    ]
    transferred_target_members = [
        stable_identifier(
            "central-transferred-target-member-v3",
            transfer_id,
            member_id,
        )
        for member_id in target["member_ids"]
    ]
    source_component = dict(
        zip(source["member_ids"], transferred_source_members, strict=True)
    )
    target_component = dict(
        zip(target["member_ids"], transferred_target_members, strict=True)
    )
    source_action = _relation_action(source_relation)
    return {
        "witness_kind": "functorial_transfer",
        "source_relation_id": source_relation["relation_id"],
        "transferred_source": {
            "primitive_id": transferred_source_id,
            "statement": (
                f"Transferred source representation for {source_relation['relation_id']}."
            ),
            "member_ids": transferred_source_members,
        },
        "transferred_target": {
            "primitive_id": transferred_target_id,
            "statement": (
                f"Transferred target representation for {source_relation['relation_id']}."
            ),
            "member_ids": transferred_target_members,
        },
        "source_component": {
            "relation_id": stable_identifier(
                "central-functor-source-component-v3", transfer_id
            ),
            "statement": "Map the source carrier into its transferred representation.",
            "action": [
                {
                    "source_member_id": member_id,
                    "target_member_id": source_component[member_id],
                }
                for member_id in source["member_ids"]
            ],
        },
        "target_component": {
            "relation_id": stable_identifier(
                "central-functor-target-component-v3", transfer_id
            ),
            "statement": "Map the target carrier into its transferred representation.",
            "action": [
                {
                    "source_member_id": member_id,
                    "target_member_id": target_component[member_id],
                }
                for member_id in target["member_ids"]
            ],
        },
        "transferred_relation": {
            "relation_id": stable_identifier(
                "central-transferred-relation-v3", transfer_id
            ),
            "statement": "Transport the declared map across both representation components.",
            "action": [
                {
                    "source_member_id": source_component[source_member],
                    "target_member_id": target_component[
                        source_action[source_member]
                    ],
                }
                for source_member in source["member_ids"]
            ],
        },
    }


def _functorial_scope(
    core: Mapping[str, Any], witness: Mapping[str, Any]
) -> dict[str, Any] | None:
    """Replay one finite naturality square and its protected predicates."""

    relations = {
        row["relation_id"]: row for row in core["relations"]
    }
    primitives = {
        row["primitive_id"]: row for row in core["primitives"]
    }
    source_relation = relations.get(witness.get("source_relation_id"))
    transferred_source = witness.get("transferred_source")
    transferred_target = witness.get("transferred_target")
    if (
        source_relation is None
        or source_relation["source_primitive_id"]
        == source_relation["target_primitive_id"]
        or not isinstance(transferred_source, Mapping)
        or not isinstance(transferred_target, Mapping)
    ):
        return None
    source = primitives[source_relation["source_primitive_id"]]
    target = primitives[source_relation["target_primitive_id"]]
    new_ids = {
        transferred_source.get("primitive_id"),
        transferred_target.get("primitive_id"),
    }
    new_member_sets = [
        transferred_source.get("member_ids"),
        transferred_target.get("member_ids"),
    ]
    occupied_members = {
        member_id
        for primitive in core["primitives"]
        for member_id in primitive["member_ids"]
    }
    if (
        len(new_ids) != 2
        or None in new_ids
        or bool(new_ids & set(primitives))
        or any(not isinstance(rows, list) or not rows for rows in new_member_sets)
        or any(
            len(set(rows)) != len(rows)
            or bool(set(rows) & occupied_members)
            for rows in new_member_sets
        )
        or bool(set(new_member_sets[0]) & set(new_member_sets[1]))
    ):
        return None
    source_component = _leg_action(
        witness.get("source_component"),
        source_members=source["member_ids"],
        target_members=new_member_sets[0],
    )
    target_component = _leg_action(
        witness.get("target_component"),
        source_members=target["member_ids"],
        target_members=new_member_sets[1],
    )
    transferred_relation = _leg_action(
        witness.get("transferred_relation"),
        source_members=new_member_sets[0],
        target_members=new_member_sets[1],
    )
    if any(
        action is None
        for action in (
            source_component,
            target_component,
            transferred_relation,
        )
    ):
        return None
    source_action = _relation_action(source_relation)
    left = {
        member_id: target_component[source_action[member_id]]
        for member_id in source["member_ids"]
    }
    right = {
        member_id: transferred_relation[source_component[member_id]]
        for member_id in source["member_ids"]
    }
    if left != right:
        return None
    registered_relation_transport = _protected_transport_chain(
        core,
        source_primitive_id=source["primitive_id"],
        steps=[
            (
                source_relation["relation_id"],
                target["primitive_id"],
                source_action,
                target["member_ids"],
            )
        ],
        require_registered_target=True,
    )
    left_transport = _protected_transport_chain(
        core,
        source_primitive_id=source["primitive_id"],
        steps=[
            (
                source_relation["relation_id"],
                target["primitive_id"],
                source_action,
                target["member_ids"],
            ),
            (
                str(witness["target_component"]["relation_id"]),
                str(transferred_target["primitive_id"]),
                target_component,
                new_member_sets[1],
            ),
        ],
        require_registered_target=False,
    )
    right_transport = _protected_transport_chain(
        core,
        source_primitive_id=source["primitive_id"],
        steps=[
            (
                str(witness["source_component"]["relation_id"]),
                str(transferred_source["primitive_id"]),
                source_component,
                new_member_sets[0],
            ),
            (
                str(witness["transferred_relation"]["relation_id"]),
                str(transferred_target["primitive_id"]),
                transferred_relation,
                new_member_sets[1],
            ),
        ],
        require_registered_target=False,
    )
    if (
        not registered_relation_transport
        or not left_transport
        or not right_transport
        or [
            row["steps"][-1]["transported_values_digest"]
            for row in left_transport
        ]
        != [
            row["steps"][-1]["transported_values_digest"]
            for row in right_transport
        ]
    ):
        return None
    return {
        "scope_kind": "finite_protected_observable_functorial_transfer",
        "source_relation_id": source_relation["relation_id"],
        "source_carrier_binding": {
            "primitive_id": source["primitive_id"],
            "primitive_digest": canonical_digest(source),
        },
        "target_carrier_binding": {
            "primitive_id": target["primitive_id"],
            "primitive_digest": canonical_digest(target),
        },
        "transferred_source_binding": {
            "primitive_id": transferred_source["primitive_id"],
            "primitive_digest": canonical_digest(transferred_source),
        },
        "transferred_target_binding": {
            "primitive_id": transferred_target["primitive_id"],
            "primitive_digest": canonical_digest(transferred_target),
        },
        "source_component_relation_id": witness["source_component"][
            "relation_id"
        ],
        "target_component_relation_id": witness["target_component"][
            "relation_id"
        ],
        "transferred_relation_id": witness["transferred_relation"][
            "relation_id"
        ],
        "naturality_rows": [
            {
                "source_member_id": member_id,
                "left_target_member_id": left[member_id],
                "right_target_member_id": right[member_id],
                "pointwise_equal": True,
            }
            for member_id in source["member_ids"]
        ],
        "registered_source_relation_transport_rows": (
            registered_relation_transport
        ),
        "left_protected_transport_rows": left_transport,
        "right_protected_transport_rows": right_transport,
        "transferred_carriers_distinct_and_disjoint": True,
        "naturality_scope": "one_declared_finite_map_and_two_explicit_components",
        "functor_scope": "finite_total_functions_only",
        "universal_functor_authorized": False,
        "continuum_scope_authorized": False,
    }


def _noncommutation_scope(
    core: Mapping[str, Any],
    left_ids: Sequence[str],
    right_ids: Sequence[str],
) -> dict[str, Any] | None:
    left = _path_composite(core, left_ids)
    right = _path_composite(core, right_ids)
    if (
        left is None
        or right is None
        or left[:2] != right[:2]
        or set(left[2]) != set(right[2])
    ):
        return None
    mismatch = sorted(
        member for member in left[2] if left[2][member] != right[2][member]
    )
    if not mismatch:
        return None
    source_id, target_id = left[:2]
    source_observables = sorted(
        (
            row
            for row in core["observables"]
            if row["protected"] and row["carrier_primitive_id"] == source_id
        ),
        key=lambda row: row["observable_id"],
    )
    target_observables = sorted(
        (
            row
            for row in core["observables"]
            if row["protected"] and row["carrier_primitive_id"] == target_id
        ),
        key=lambda row: row["observable_id"],
    )
    distinguishing_rows: list[dict[str, Any]] = []
    preserving_sides: set[str] = set()
    for source_observable in source_observables:
        source_values = {
            row["member_id"]: row["value"]
            for row in source_observable["evaluations"]
        }
        for target_observable in target_observables:
            target_values = {
                row["member_id"]: row["value"]
                for row in target_observable["evaluations"]
            }
            for side, action in (("left", left[2]), ("right", right[2])):
                if all(
                    source_values.get(member) == target_values.get(action[member])
                    for member in action
                ):
                    preserving_sides.add(side)
            for member in mismatch:
                if (
                    left[2][member] in target_values
                    and right[2][member] in target_values
                    and target_values[left[2][member]]
                    != target_values[right[2][member]]
                ):
                    distinguishing_rows.append(
                        {
                            "source_member_id": member,
                            "left_target_member_id": left[2][member],
                            "right_target_member_id": right[2][member],
                            "target_observable_id": target_observable[
                                "observable_id"
                            ],
                            "left_value": target_values[left[2][member]],
                            "right_value": target_values[right[2][member]],
                        }
                    )
    if not distinguishing_rows or not preserving_sides:
        return None
    return {
        "scope_kind": "finite_protected_observable_noncommutation_countermodel",
        "source_primitive_id": source_id,
        "target_primitive_id": target_id,
        "left_path_relation_ids": list(left_ids),
        "right_path_relation_ids": list(right_ids),
        "finite_member_ids": sorted(left[2]),
        "mismatch_member_ids": mismatch,
        "protected_distinguishing_rows": distinguishing_rows,
        "protected_observable_preserving_sides": sorted(preserving_sides),
        "comparison_scope": "pointwise_declared_finite_carrier_only",
        "isomorphism_scope": "not_evaluated_or_claimed",
        "continuum_scope_authorized": False,
    }


def _hott_transport_scope(
    core: Mapping[str, Any],
    forward: Mapping[str, Any],
    inverse: Mapping[str, Any],
    path_ids: Sequence[str],
) -> dict[str, Any] | None:
    if (
        forward["relation_id"] == inverse["relation_id"]
        or forward["source_primitive_id"] != forward["target_primitive_id"]
        or inverse["source_primitive_id"] != forward["target_primitive_id"]
        or inverse["target_primitive_id"] != forward["source_primitive_id"]
    ):
        return None
    primitive_id = forward["source_primitive_id"]
    primitives = {
        row["primitive_id"]: row for row in core["primitives"]
    }
    primitive = primitives.get(primitive_id)
    if primitive is None:
        return None
    forward_action = _relation_action(forward)
    inverse_action = _relation_action(inverse)
    members = list(primitive["member_ids"])
    if (
        set(forward_action) != set(members)
        or set(inverse_action) != set(members)
        or all(forward_action[member] == member for member in members)
        or any(
            inverse_action.get(forward_action[member]) != member
            or forward_action.get(inverse_action[member]) != member
            for member in members
        )
    ):
        return None
    inhabitants = {
        row["inhabitant_id"]: row for row in core["inhabitants"]
    }
    selected_paths = [inhabitants.get(item) for item in path_ids]
    if any(row is None or row["level"] != 1 for row in selected_paths):
        return None
    required_boundaries = {
        (member, forward_action[member]) for member in members
    } | {
        (member, inverse_action[member]) for member in members
    }
    observed_boundaries = {
        (row["source_boundary_id"], row["target_boundary_id"])
        for row in selected_paths
        if row is not None
        and row["ambient_primitive_id"] == primitive_id
        and row["derivation_rule"] != "reflexivity"
        and row["evidence_refs"]
    }
    if required_boundaries != observed_boundaries:
        return None
    transport_rows: list[dict[str, Any]] = []
    protected = sorted(
        (
            row
            for row in core["observables"]
            if row["protected"]
            and row["carrier_primitive_id"] == primitive_id
        ),
        key=lambda row: row["observable_id"],
    )
    for observable in protected:
        values = {
            row["member_id"]: row["value"]
            for row in observable["evaluations"]
        }
        for member in members:
            transport_rows.append(
                {
                    "observable_id": observable["observable_id"],
                    "member_id": member,
                    "forward_member_id": forward_action[member],
                    "inverse_member_id": inverse_action[member],
                    "forward_preserved": values[member]
                    == values[forward_action[member]],
                    "inverse_preserved": values[member]
                    == values[inverse_action[member]],
                }
            )
    if not transport_rows or not all(
        row["forward_preserved"] and row["inverse_preserved"]
        for row in transport_rows
    ):
        return None
    return {
        "scope_kind": "finite_identity_path_transport_with_declared_inverse",
        "ambient_primitive_id": primitive_id,
        "forward_relation_id": forward["relation_id"],
        "inverse_relation_id": inverse["relation_id"],
        "finite_member_ids": members,
        "path_inhabitant_ids": list(path_ids),
        "round_trip_rows": [
            {
                "member_id": member,
                "forward_then_inverse_member_id": inverse_action[
                    forward_action[member]
                ],
                "inverse_then_forward_member_id": forward_action[
                    inverse_action[member]
                ],
            }
            for member in members
        ],
        "transport_rows": transport_rows,
        "judgmental_equality_authorized": False,
        "identity_path_scope": "declared_evidence_bearing_level_one_paths_only",
        "equivalence_scope": "finite_bijection_with_distinct_declared_inverse_only",
        "inverse_scope": "pointwise_declared_finite_members_only",
        "composite_scope": "both_map_composites_replayed_pointwise",
        "round_trip_scope": "both_composites_equal_finite_identity_actions",
        "transport_scope": "listed_protected_observable_evaluations_only",
        "naturality_scope": "not_claimed_without_a_declared_map_family",
        "coherence_scope": "no_level_two_coherence_claim",
        "univalence_authorized": False,
        "higher_inductive_authorized": False,
        "continuum_scope_authorized": False,
    }


def _hott_equivalence_scope(
    core: Mapping[str, Any],
    forward: Mapping[str, Any],
    inverse: Mapping[str, Any],
    left_path_ids: Sequence[str],
    right_path_ids: Sequence[str],
    coherence_cell_ids: Sequence[str],
) -> dict[str, Any] | None:
    """Replay a distinct-carrier finite equivalence and explicit coherence."""

    primitives = {
        row["primitive_id"]: row for row in core["primitives"]
    }
    source = primitives.get(forward["source_primitive_id"])
    target = primitives.get(forward["target_primitive_id"])
    if (
        source is None
        or target is None
        or source["primitive_id"] == target["primitive_id"]
        or inverse["source_primitive_id"] != target["primitive_id"]
        or inverse["target_primitive_id"] != source["primitive_id"]
        or forward["relation_id"] == inverse["relation_id"]
    ):
        return None
    forward_action = _relation_action(forward)
    inverse_action = _relation_action(inverse)
    source_members = list(source["member_ids"])
    target_members = list(target["member_ids"])
    if (
        set(forward_action) != set(source_members)
        or set(inverse_action) != set(target_members)
        or set(forward_action.values()) != set(target_members)
        or set(inverse_action.values()) != set(source_members)
    ):
        return None
    source_roundtrips = {
        member: inverse_action.get(forward_action[member])
        for member in source_members
    }
    target_roundtrips = {
        member: forward_action.get(inverse_action[member])
        for member in target_members
    }
    if source_roundtrips != {member: member for member in source_members} or (
        target_roundtrips != {member: member for member in target_members}
    ):
        return None

    inhabitants = {
        row["inhabitant_id"]: row for row in core["inhabitants"]
    }
    if (
        not left_path_ids
        or not right_path_ids
        or len(set(left_path_ids)) != len(left_path_ids)
        or len(set(right_path_ids)) != len(right_path_ids)
        or set(left_path_ids) & set(right_path_ids)
    ):
        return None
    try:
        left_paths = [inhabitants[item] for item in left_path_ids]
        right_paths = [inhabitants[item] for item in right_path_ids]
        cells = [inhabitants[item] for item in coherence_cell_ids]
    except KeyError:
        return None
    expected_left = {
        (source["primitive_id"], member, member)
        for member in source_members
    }
    expected_right = {
        (target["primitive_id"], member, member)
        for member in target_members
    }
    observed_left = {
        (
            row["ambient_primitive_id"],
            row["source_boundary_id"],
            row["target_boundary_id"],
        )
        for row in left_paths
        if row["level"] == 1
        and row["derivation_rule"] != "free_adjoinment"
    }
    observed_right = {
        (
            row["ambient_primitive_id"],
            row["source_boundary_id"],
            row["target_boundary_id"],
        )
        for row in right_paths
        if row["level"] == 1
        and row["derivation_rule"] != "free_adjoinment"
    }
    if observed_left != expected_left or observed_right != expected_right:
        return None
    selected_paths = set(left_path_ids) | set(right_path_ids)
    if (
        not cells
        or len(set(coherence_cell_ids)) != len(coherence_cell_ids)
        or any(
            row["level"] != 2
            or row["derivation_rule"] != "declared_coherence_constructor"
            or not row["evidence_refs"]
            or row["source_boundary_id"] == row["target_boundary_id"]
            or row["source_boundary_id"] not in selected_paths
            or row["target_boundary_id"] not in selected_paths
            for row in cells
        )
    ):
        return None

    source_observables = sorted(
        (
            row
            for row in core["observables"]
            if row["protected"]
            and row["carrier_primitive_id"] == source["primitive_id"]
        ),
        key=lambda row: row["observable_id"],
    )
    target_observables = sorted(
        (
            row
            for row in core["observables"]
            if row["protected"]
            and row["carrier_primitive_id"] == target["primitive_id"]
        ),
        key=lambda row: row["observable_id"],
    )
    transport_rows: list[dict[str, Any]] = []
    for source_observable in source_observables:
        source_values = {
            row["member_id"]: row["value"]
            for row in source_observable["evaluations"]
        }
        matches: list[Mapping[str, Any]] = []
        for target_observable in target_observables:
            target_values = {
                row["member_id"]: row["value"]
                for row in target_observable["evaluations"]
            }
            if all(
                source_values[source_member]
                == target_values[forward_action[source_member]]
                for source_member in source_members
            ) and all(
                target_values[target_member]
                == source_values[inverse_action[target_member]]
                for target_member in target_members
            ):
                matches.append(target_observable)
        if not matches:
            return None
        selected = matches[0]
        target_values = {
            row["member_id"]: row["value"]
            for row in selected["evaluations"]
        }
        transport_rows.extend(
            {
                "source_observable_id": source_observable["observable_id"],
                "target_observable_id": selected["observable_id"],
                "source_member_id": source_member,
                "forward_member_id": forward_action[source_member],
                "forward_value_preserved": (
                    source_values[source_member]
                    == target_values[forward_action[source_member]]
                ),
                "inverse_value_preserved": (
                    target_values[forward_action[source_member]]
                    == source_values[
                        inverse_action[forward_action[source_member]]
                    ]
                ),
            }
            for source_member in source_members
        )
    if not transport_rows or not all(
        row["forward_value_preserved"] and row["inverse_value_preserved"]
        for row in transport_rows
    ):
        return None
    return {
        "scope_kind": "finite_distinct_carrier_equivalence_with_coherence",
        "source_carrier_binding": {
            "primitive_id": source["primitive_id"],
            "primitive_digest": canonical_digest(source),
        },
        "target_carrier_binding": {
            "primitive_id": target["primitive_id"],
            "primitive_digest": canonical_digest(target),
        },
        "forward_relation_id": forward["relation_id"],
        "inverse_relation_id": inverse["relation_id"],
        "source_identity_path_inhabitant_ids": list(left_path_ids),
        "target_identity_path_inhabitant_ids": list(right_path_ids),
        "coherence_cell_ids": list(coherence_cell_ids),
        "source_round_trip_rows": [
            {
                "member_id": member,
                "forward_then_inverse_member_id": source_roundtrips[member],
                "identity_replayed": source_roundtrips[member] == member,
            }
            for member in source_members
        ],
        "target_round_trip_rows": [
            {
                "member_id": member,
                "inverse_then_forward_member_id": target_roundtrips[member],
                "identity_replayed": target_roundtrips[member] == member,
            }
            for member in target_members
        ],
        "transport_rows": transport_rows,
        "equivalence_scope": (
            "finite_bijection_between_distinct_registered_carriers_only"
        ),
        "identity_scope": (
            "both_composites_pointwise_equal_declared_finite_identity_maps"
        ),
        "inverse_scope": "one_explicit_forward_and_inverse_relation_pair",
        "round_trip_scope": "both_registered_carriers_replayed_pointwise",
        "transport_scope": (
            "paired_protected_observable_evaluations_on_both_carriers_only"
        ),
        "naturality_scope": (
            "forward_inverse_protected_predicate_squares_pointwise_only"
        ),
        "coherence_scope": (
            "listed_declared_level_two_cells_between_selected_parallel_"
            "roundtrip_paths_only"
        ),
        "judgmental_equality_authorized": False,
        "univalence_authorized": False,
        "higher_inductive_authorized": False,
        "general_hott_semantics_authorized": False,
        "physical_equivalence_authorized": False,
        "continuum_scope_authorized": False,
    }


def _candidate_consequence(
    core: Mapping[str, Any],
    rule: Mapping[str, Any],
    relation: Mapping[str, Any],
    finite_scope: Mapping[str, Any],
) -> dict[str, str]:
    """Derive a physics return from this candidate rather than shared prose."""

    kind = str(relation["relation_kind"])
    scope_kind = str(finite_scope["scope_kind"])
    scope_tag = canonical_digest(finite_scope).split(":", 1)[1][:16]
    source = str(relation["source_primitive_id"])
    target = str(relation["target_primitive_id"])
    interpretation = (
        f"Within {core['physical_carrier']} in {core['regime']}, candidate "
        f"{relation['relation_id']} interprets the finite {kind} witness "
        f"from {source} to {target} as {scope_kind} ({scope_tag}); this is a "
        "carrier-level interpretation, not a physical-equivalence claim."
    )
    return {
        "explanatory_gain": interpretation,
        "new_question": (
            f"Which carrier construction realizes scope {scope_tag} for "
            f"{relation['relation_id']} while retaining every committed "
            "quantifier and protected observable?"
        ),
        "changed_burden": (
            f"Candidate {relation['relation_id']} must realize {scope_kind} "
            f"for burden {rule['incumbent_decision']['target_burden_id']} "
            f"on {source}->{target} with exact scope digest {scope_tag}."
        ),
        "correction": (
            f"Withdraw candidate {relation['relation_id']} if replay of "
            f"{scope_kind} ({scope_tag}) changes an endpoint, inverse, path, "
            "coherence cell, or protected observable evaluation."
        ),
        "falsifier": (
            f"Produce one member or protected-observable row in scope "
            f"{scope_tag} for which the asserted {kind} factorization, "
            "round trip, transport, naturality, or coherence equation fails."
        ),
        "physics_next_action": (
            f"Reconstruct candidate {relation['relation_id']} and scope "
            f"{scope_tag} in the declared physical carrier, then derive the "
            "corresponding carrier-level counterexample before any theorem "
            "or continuum escalation."
        ),
    }


def _consequence(
    core: Mapping[str, Any],
    rule: Mapping[str, Any],
    relation: Mapping[str, Any],
    finite_scope: Mapping[str, Any],
) -> dict[str, str]:
    return {
        **_candidate_consequence(
            core, rule, relation, finite_scope
        )
    }


def _plan(
    *,
    core: Mapping[str, Any],
    rule: Mapping[str, Any],
    relation_kind: str,
    relation_hypothesis: Mapping[str, Any],
    witness: Mapping[str, Any],
    finite_scope: Mapping[str, Any],
) -> dict[str, Any]:
    material = {
        "relation_hypothesis": copy.deepcopy(dict(relation_hypothesis)),
        "witness": copy.deepcopy(dict(witness)),
        "finite_scope": copy.deepcopy(dict(finite_scope)),
        "consequence_contract": _consequence(
            core,
            rule,
            relation_hypothesis,
            finite_scope,
        ),
    }
    return {
        "transformation_id": stable_identifier(
            "postcommit-conceptual-transformation-v3",
            core["content_digest"],
            relation_kind,
            material,
        ),
        **material,
    }


def _derive_category_plan(
    core: Mapping[str, Any], rule: Mapping[str, Any]
) -> dict[str, Any] | None:
    # Prefer a positive graph mediator.  Unlike an interface copy, the graph
    # members bind source-target pairs, are disjoint from both endpoints, and
    # replay protected observables through both legs.
    declared = sorted(
        (
            row
            for row in core["relations"]
            if row["relation_type"] == "declared_finite_map"
            and row["source_primitive_id"] != row["target_primitive_id"]
        ),
        key=lambda row: row["relation_id"],
    )
    for direct in declared:
        witness = _graph_mediator_witness(core, direct)
        finite_scope = _mediator_scope(core, witness)
        if finite_scope is None:
            continue
        hypothesis = {
            "relation_id": stable_identifier(
                "postcommit-relation-hypothesis-v3",
                "mediating_factorization",
                direct["relation_id"],
                finite_scope,
            ),
            "relation_kind": "mediating_factorization",
            "statement": (
                f"Factor declared map {direct['relation_id']} through its "
                "distinct finite graph carrier while preserving protected "
                "observable values pointwise."
            ),
            "source_primitive_id": direct["source_primitive_id"],
            "target_primitive_id": direct["target_primitive_id"],
            "premise_ids": [
                f"committed-core:{core['content_digest']}",
                f"decision-rule:{rule['decision_rule_digest']}",
                f"declared-map:{direct['relation_id']}",
            ],
        }
        return _plan(
            core=core,
            rule=rule,
            relation_kind="mediating_factorization",
            relation_hypothesis=hypothesis,
            witness=witness,
            finite_scope=finite_scope,
        )

    # If an exact graph mediator is already materialized, retain a second
    # positive route: an explicit representation-transfer square whose two
    # paths agree pointwise on each protected finite observable.
    for source_relation in declared:
        witness = _functorial_witness(core, source_relation)
        finite_scope = _functorial_scope(core, witness)
        if finite_scope is None:
            continue
        hypothesis = {
            "relation_id": stable_identifier(
                "postcommit-relation-hypothesis-v3",
                "functorial_transfer",
                source_relation["relation_id"],
                finite_scope,
            ),
            "relation_kind": "functorial_transfer",
            "statement": (
                f"Transfer declared map {source_relation['relation_id']} "
                "through two distinct finite representations and replay its "
                "protected-observable naturality square pointwise."
            ),
            "source_primitive_id": source_relation["source_primitive_id"],
            "target_primitive_id": source_relation["target_primitive_id"],
            "premise_ids": [
                f"committed-core:{core['content_digest']}",
                f"decision-rule:{rule['decision_rule_digest']}",
                f"declared-map:{source_relation['relation_id']}",
            ],
        }
        return _plan(
            core=core,
            rule=rule,
            relation_kind="functorial_transfer",
            relation_hypothesis=hypothesis,
            witness=witness,
            finite_scope=finite_scope,
        )

    # Preserve the negative countermodel as a final categorical fallback.
    relations = sorted(core["relations"], key=lambda row: row["relation_id"])
    paths: list[tuple[Mapping[str, Any], Mapping[str, Any], tuple[tuple[str, str], ...]]] = []
    for first in relations:
        for second in relations:
            composed = _compose_relations(first, second)
            if composed is not None:
                paths.append((first, second, composed))
    for index, left in enumerate(paths):
        for right in paths[index + 1 :]:
            if (
                left[0]["source_primitive_id"] == right[0]["source_primitive_id"]
                and left[1]["target_primitive_id"] == right[1]["target_primitive_id"]
                and left[2] != right[2]
            ):
                hypothesis = {
                    "relation_id": stable_identifier(
                        "postcommit-relation-hypothesis-v3",
                        "noncommuting_composition",
                        left[0]["relation_id"],
                        left[1]["relation_id"],
                        right[0]["relation_id"],
                        right[1]["relation_id"],
                    ),
                    "relation_kind": "noncommuting_composition",
                    "statement": (
                        "Two declared composites with the same endpoints disagree on "
                        "at least one finite carrier member."
                    ),
                    "source_primitive_id": left[0]["source_primitive_id"],
                    "target_primitive_id": left[1]["target_primitive_id"],
                    "premise_ids": [
                        f"committed-core:{core['content_digest']}",
                        f"decision-rule:{rule['decision_rule_digest']}",
                    ],
                }
                witness = {
                    "witness_kind": "noncommutativity_localization",
                    "left_path_relation_ids": [
                        left[0]["relation_id"],
                        left[1]["relation_id"],
                    ],
                    "right_path_relation_ids": [
                        right[0]["relation_id"],
                        right[1]["relation_id"],
                    ],
                }
                finite_scope = _noncommutation_scope(
                    core,
                    witness["left_path_relation_ids"],
                    witness["right_path_relation_ids"],
                )
                if finite_scope is None:
                    continue
                return _plan(
                    core=core,
                    rule=rule,
                    relation_kind="noncommuting_composition",
                    relation_hypothesis=hypothesis,
                    witness=witness,
                    finite_scope=finite_scope,
                )
    return None


def _derive_hott_plan(
    core: Mapping[str, Any], rule: Mapping[str, Any]
) -> dict[str, Any] | None:
    primitives = {row["primitive_id"]: row for row in core["primitives"]}
    inhabitants = sorted(core["inhabitants"], key=lambda row: row["inhabitant_id"])
    relations = sorted(core["relations"], key=lambda row: row["relation_id"])
    inhabitant_by_id = {
        row["inhabitant_id"]: row for row in inhabitants
    }

    # A genuine distinct-carrier finite equivalence is the primary HoTT
    # opportunity.  Both inverse composites, protected predicate transport,
    # and a non-vacuous listed level-two coherence cell must already be
    # present in the committed core; no free completion is admitted.
    for forward in relations:
        if forward["source_primitive_id"] == forward["target_primitive_id"]:
            continue
        source = primitives[forward["source_primitive_id"]]
        target = primitives[forward["target_primitive_id"]]
        forward_action = _relation_action(forward)
        inverse = next(
            (
                candidate
                for candidate in relations
                if candidate["relation_id"] != forward["relation_id"]
                and candidate["source_primitive_id"]
                == target["primitive_id"]
                and candidate["target_primitive_id"]
                == source["primitive_id"]
                and set(_relation_action(candidate))
                == set(target["member_ids"])
                and all(
                    _relation_action(candidate).get(
                        forward_action[source_member]
                    )
                    == source_member
                    for source_member in source["member_ids"]
                )
                and all(
                    forward_action.get(
                        _relation_action(candidate)[target_member]
                    )
                    == target_member
                    for target_member in target["member_ids"]
                )
            ),
            None,
        )
        if inverse is None:
            continue
        left_boundaries = {
            (source["primitive_id"], member, member)
            for member in source["member_ids"]
        }
        right_boundaries = {
            (target["primitive_id"], member, member)
            for member in target["member_ids"]
        }
        left_paths = [
            row["inhabitant_id"]
            for row in inhabitants
            if row["level"] == 1
            and row["derivation_rule"] != "free_adjoinment"
            and (
                row["ambient_primitive_id"],
                row["source_boundary_id"],
                row["target_boundary_id"],
            )
            in left_boundaries
        ]
        right_paths = [
            row["inhabitant_id"]
            for row in inhabitants
            if row["level"] == 1
            and row["derivation_rule"] != "free_adjoinment"
            and (
                row["ambient_primitive_id"],
                row["source_boundary_id"],
                row["target_boundary_id"],
            )
            in right_boundaries
        ]
        selected_paths = set(left_paths) | set(right_paths)
        cells = [
            row["inhabitant_id"]
            for row in inhabitants
            if row["level"] == 2
            and row["derivation_rule"] == "declared_coherence_constructor"
            and row["evidence_refs"]
            and row["source_boundary_id"] != row["target_boundary_id"]
            and row["source_boundary_id"] in selected_paths
            and row["target_boundary_id"] in selected_paths
            and inhabitant_by_id[row["source_boundary_id"]][
                "ambient_primitive_id"
            ]
            == row["ambient_primitive_id"]
            == inhabitant_by_id[row["target_boundary_id"]][
                "ambient_primitive_id"
            ]
        ]
        finite_scope = _hott_equivalence_scope(
            core,
            forward,
            inverse,
            left_paths,
            right_paths,
            cells,
        )
        if finite_scope is None:
            continue
        hypothesis = {
            "relation_id": stable_identifier(
                "postcommit-relation-hypothesis-v3",
                "equivalence_coherence",
                forward["relation_id"],
                inverse["relation_id"],
                finite_scope,
            ),
            "relation_kind": "equivalence_coherence",
            "statement": (
                f"Relate distinct registered carriers {source['primitive_id']} "
                f"and {target['primitive_id']} by explicit inverse maps, "
                "pointwise protected-predicate transport, both round trips, "
                "and listed level-two coherence only."
            ),
            "source_primitive_id": source["primitive_id"],
            "target_primitive_id": target["primitive_id"],
            "premise_ids": [
                f"committed-core:{core['content_digest']}",
                f"decision-rule:{rule['decision_rule_digest']}",
                f"forward-map:{forward['relation_id']}",
                f"inverse-map:{inverse['relation_id']}",
            ],
        }
        witness = {
            "witness_kind": "equivalence_coherence",
            "construction_origin": "derived_inhabitant",
            "forward_relation_id": forward["relation_id"],
            "inverse_relation_id": inverse["relation_id"],
            "left_path_inhabitant_ids": left_paths,
            "right_path_inhabitant_ids": right_paths,
            "coherence_cell_ids": cells,
            "adjoined_paths": [],
            "adjoined_cells": [],
        }
        return _plan(
            core=core,
            rule=rule,
            relation_kind="equivalence_coherence",
            relation_hypothesis=hypothesis,
            witness=witness,
            finite_scope=finite_scope,
        )

    # Retain the previous nonidentity same-carrier transport as a bounded
    # fallback when no committed distinct-carrier equivalence exists.
    for relation in relations:
        if relation["source_primitive_id"] != relation["target_primitive_id"]:
            continue
        primitive = primitives[relation["source_primitive_id"]]
        action = _relation_action(relation)
        if all(action[member] == member for member in primitive["member_ids"]):
            continue
        inverse = next(
            (
                candidate
                for candidate in relations
                if candidate["relation_id"] != relation["relation_id"]
                and candidate["source_primitive_id"]
                == relation["target_primitive_id"]
                and candidate["target_primitive_id"]
                == relation["source_primitive_id"]
                and all(
                    _relation_action(candidate).get(action[member]) == member
                    and action.get(_relation_action(candidate)[member]) == member
                    for member in primitive["member_ids"]
                )
            ),
            None,
        )
        if inverse is None:
            continue
        required = {
            (member, action[member]) for member in primitive["member_ids"]
        } | {
            (member, _relation_action(inverse)[member])
            for member in primitive["member_ids"]
        }
        path_by_boundary = {
            (row["source_boundary_id"], row["target_boundary_id"]): row
            for row in inhabitants
            if row["level"] == 1
            and row["ambient_primitive_id"] == primitive["primitive_id"]
            and row["derivation_rule"] != "reflexivity"
            and row["evidence_refs"]
        }
        if not required.issubset(path_by_boundary):
            continue
        path_ids = sorted(
            {path_by_boundary[boundary]["inhabitant_id"] for boundary in required}
        )
        finite_scope = _hott_transport_scope(
            core, relation, inverse, path_ids
        )
        if finite_scope is None:
            continue
        hypothesis = {
            "relation_id": stable_identifier(
                "postcommit-relation-hypothesis-v3",
                "identity_transport",
                relation["relation_id"],
                path_ids,
            ),
            "relation_kind": "identity_transport",
            "statement": (
                "Transport the committed protected predicates along declared "
                "level-one inhabitants without adding paths."
            ),
            "source_primitive_id": primitive["primitive_id"],
            "target_primitive_id": primitive["primitive_id"],
            "premise_ids": [
                f"committed-core:{core['content_digest']}",
                f"decision-rule:{rule['decision_rule_digest']}",
            ],
        }
        witness = {
            "witness_kind": "identity_transport",
            "construction_origin": "derived_inhabitant",
            "transport_relation_id": relation["relation_id"],
            "path_inhabitant_ids": path_ids,
            "adjoined_paths": [],
        }
        witness["path_inhabitant_ids"] = path_ids
        return _plan(
            core=core,
            rule=rule,
            relation_kind="identity_transport",
            relation_hypothesis=hypothesis,
            witness=witness,
            finite_scope=finite_scope,
        )
    return None


def _formal_execution(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    model_projection = [
        {
            "task_id": row.get("task_id"),
            "category": row.get("category_check"),
            "hott": row.get("hott_check"),
        }
        for row in records
    ]
    witness_projection = [
        {
            "task_id": row.get("task_id"),
            "category_mismatches": (
                row["category_check"].get("mismatch_elements", [])
                if isinstance(row.get("category_check"), Mapping)
                else []
            ),
            "hott_round_trip": (
                row["hott_check"].get("round_trip_holds")
                if isinstance(row.get("hott_check"), Mapping)
                else None
            ),
        }
        for row in records
    ]
    return {
        "model_digest": canonical_digest(model_projection),
        "witness_digest": canonical_digest(witness_projection),
        "theorem_authorized": False,
        "continuum_authorized": False,
        "physics_value_authorized": False,
        "conceptual_advantage_authorized": False,
    }


def _lens_for_plan(plan: Mapping[str, Any]) -> str:
    kind = plan["relation_hypothesis"]["relation_kind"]
    if kind in {
        "noncommuting_composition",
        "mediating_factorization",
        "functorial_transfer",
    }:
        return "categorical"
    if kind in {
        "identity_transport",
        "equivalence_coherence",
        "path_independence",
        "descent_coherence",
    }:
        return "hott"
    _fail("postcommit plan has no registered Category/HoTT task relation")
    raise AssertionError("unreachable")


def _task_relation_endpoint_anchors(
    core: Mapping[str, Any], relation: Mapping[str, Any]
) -> tuple[str, str, list[str]]:
    """Return role-typed anchors bound to the exact endpoint primitives.

    The shared task-relation compiler correctly rejects a graph edge whose two
    semantic-node strings are identical.  A HoTT endorelation still has two
    boundary *roles* over one primitive, so it receives two canonical role
    copies of the same exact primitive statement.  Their primitive IDs and
    digests remain explicitly bound by ``_forge_artifact_binding``.
    """

    primitives = {row["primitive_id"]: row for row in core["primitives"]}
    source = primitives.get(relation["source_primitive_id"])
    target = primitives.get(relation["target_primitive_id"])
    if source is None or target is None:
        _fail("task relation endpoints are outside the exact authored core")
    if source["primitive_id"] == target["primitive_id"]:
        source_anchor = (
            f"{source['primitive_id']} source-boundary role: {source['statement']}"
        )
        target_anchor = (
            f"{target['primitive_id']} target-boundary role: {target['statement']}"
        )
        return source_anchor, target_anchor, [source_anchor, target_anchor]
    source_anchor = f"{source['primitive_id']}: {source['statement']}"
    target_anchor = f"{target['primitive_id']}: {target['statement']}"
    return source_anchor, target_anchor, []


def _meaning_case(
    *,
    core: Mapping[str, Any],
    rule: Mapping[str, Any],
    plan: Mapping[str, Any],
    route_id: str,
    stage: str,
) -> dict[str, Any]:
    """Compile an exact transformed-core boundary through the shared relation API."""

    lens = _lens_for_plan(plan)
    primitive_anchors = {
        row["primitive_id"]: f"{row['primitive_id']}: {row['statement']}"
        for row in core["primitives"]
    }
    primitives = list(primitive_anchors.values())
    invariants = [
        f"{row['observable_id']}: {row['statement']}"
        for row in core["observables"]
        if row["protected"]
    ]
    if len(primitives) < 2 or len(invariants) < 2:
        _fail("task-relation forgers require two primitives and two protected invariants")
    relation = plan["relation_hypothesis"]
    source_anchor, target_anchor, role_anchors = _task_relation_endpoint_anchors(
        core, relation
    )
    primitives.extend(role_anchors)
    relation_id = stable_identifier(
        "central-task-relation-v3",
        route_id,
        stage,
        core["content_digest"],
        plan["transformation_id"],
    )
    candidate_kind = (
        "compare_route_order" if lens == "categorical" else "require_coherence"
    )
    return {
        "case_id": stable_identifier(
            "central-task-relation-case-v3",
            route_id,
            stage,
            core["content_digest"],
            plan["transformation_id"],
        ),
        "target_id": core["target_id"],
        "obligation_id": core["obligation_id"],
        "task_semantics": {
            "pressure": relation["statement"],
            "formal_pressure": (
                "Replay the exact finite relation witness and expose a changed "
                "carrier-level burden without weakening the committed target."
            ),
            "incumbent_primitives": primitives,
            "protected_invariants": invariants,
            "physical_carrier": core["physical_carrier"],
            "regime": core["regime"],
            "quantifiers": [row["statement"] for row in core["quantifiers"]],
            "falsifier": rule["falsifier"],
            "correction": rule["correction"],
            "untouched_physics_gates": copy.deepcopy(
                rule["untouched_physics_gates"]
            ),
            "task_relations": [
                {
                    "relation_id": relation_id,
                    "relation_kind": relation["relation_kind"],
                    "statement": relation["statement"],
                    "source_anchor": source_anchor,
                    "target_anchor": target_anchor,
                }
            ],
            "incumbent_decision": {
                **copy.deepcopy(rule["incumbent_decision"]),
                "decision_kind": "continue_route",
            },
            "lens_decisions": {
                lens: {
                    **copy.deepcopy(rule["eligible_decision"]),
                    "decision_kind": candidate_kind,
                    "trigger_relation_id": relation_id,
                }
            },
        },
    }


def _forge_skill_evidence(
    *,
    core: Mapping[str, Any],
    rule: Mapping[str, Any],
    plan: Mapping[str, Any],
    route_id: str,
    stage: str,
) -> dict[str, Any]:
    """Invoke and independently replay the existing Category/HoTT forger kernel."""

    case = _meaning_case(
        core=core,
        rule=rule,
        plan=plan,
        route_id=route_id,
        stage=stage,
    )
    lens = _lens_for_plan(plan)
    artifact = forge_case_artifact(
        case,
        lens,
        presentation_id=stable_identifier(
            "central-postcommit-presentation-v3",
            route_id,
            stage,
            core["content_digest"],
        ),
    )
    replay = validate_task_derived_artifact(case, artifact)
    binding = _forge_artifact_binding(
        core=core,
        plan=plan,
        route_id=route_id,
        stage=stage,
        case=case,
        artifact=artifact,
    )
    return {
        "skill_id": artifact["skill_id"],
        "lens": lens,
        "stage": stage,
        "authored_from_core_digest": core["content_digest"],
        "plan": copy.deepcopy(dict(plan)),
        "case": case,
        "artifact": artifact,
        "artifact_replay": replay,
        "artifact_digest": artifact["artifact_digest"],
        "binding": binding,
        "binding_digest": binding["binding_digest"],
    }


def _forge_artifact_binding(
    *,
    core: Mapping[str, Any],
    plan: Mapping[str, Any],
    route_id: str,
    stage: str,
    case: Mapping[str, Any],
    artifact: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind a reused forger result to one exact transformation premise."""

    task_relations = case.get("task_semantics", {}).get("task_relations", [])
    if not isinstance(task_relations, list) or len(task_relations) != 1:
        _fail("reused forger case does not expose one exact task relation")
    relation = plan["relation_hypothesis"]
    task_relation = task_relations[0]
    primitives = {row["primitive_id"]: row for row in core["primitives"]}
    source = primitives.get(relation["source_primitive_id"])
    target = primitives.get(relation["target_primitive_id"])
    if source is None or target is None:
        _fail("reused forger binding names an absent primitive endpoint")
    expected_source, expected_target, _role_anchors = (
        _task_relation_endpoint_anchors(core, relation)
    )
    if (
        task_relation.get("relation_kind") != relation["relation_kind"]
        or task_relation.get("statement") != relation["statement"]
        or task_relation.get("source_anchor") != expected_source
        or task_relation.get("target_anchor") != expected_target
        or artifact.get("case_id") != case.get("case_id")
        or artifact.get("target_id") != core["target_id"]
        or artifact.get("obligation_id") != core["obligation_id"]
    ):
        _fail("reused forger artifact is detached from its exact task relation")
    return _seal(
        {
            "route_id": route_id,
            "stage": stage,
            "core_digest": core["content_digest"],
            "plan_digest": canonical_digest(plan),
            "relation_hypothesis_digest": canonical_digest(relation),
            "witness_digest": canonical_digest(plan["witness"]),
            "consequence_contract_digest": canonical_digest(
                plan["consequence_contract"]
            ),
            "source_primitive_id": source["primitive_id"],
            "source_primitive_digest": canonical_digest(source),
            "target_primitive_id": target["primitive_id"],
            "target_primitive_digest": canonical_digest(target),
            "case_digest": canonical_digest(case),
            "artifact_digest": artifact["artifact_digest"],
        },
        "binding_digest",
    )


def _apply_postcommit_plan(
    core: Mapping[str, Any], plan: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    constructor = (
        construct_categorical_transformation
        if _lens_for_plan(plan) == "categorical"
        else construct_hott_transformation
    )
    delta = constructor(
        core,
        plan["relation_hypothesis"],
        plan["witness"],
        plan["consequence_contract"],
    )
    replay = validate_semantic_delta(delta)
    if canonical_json(delta["before_core"]) != canonical_json(core):
        _fail("postcommit plan did not start from its exact authored core")
    validate_conceptual_core(delta["after_core"], allow_free=True)
    return delta, replay


def _build_conditioned_sequence_delta(
    *,
    base_core: Mapping[str, Any],
    route_id: str,
    first_plan: Mapping[str, Any],
    first_delta: Mapping[str, Any],
    second_plan: Mapping[str, Any],
    second_delta: Mapping[str, Any],
    sequence: Mapping[str, Any],
    conditioned_path: Mapping[str, Any],
) -> dict[str, Any]:
    material = {
        "schema_version": "1.0.0",
        "delta_kind": "intermediate_conditioned_category_hott_sequence",
        "route_id": route_id,
        "before_core": copy.deepcopy(dict(base_core)),
        "after_core": copy.deepcopy(dict(second_delta["after_core"])),
        "first_plan": copy.deepcopy(dict(first_plan)),
        "first_plan_authored_from_core_digest": base_core["content_digest"],
        "first_delta": copy.deepcopy(dict(first_delta)),
        "intermediate_core_digest": first_delta["after_core"]["content_digest"],
        "second_plan": copy.deepcopy(dict(second_plan)),
        "second_plan_authored_from_core_digest": first_delta["after_core"][
            "content_digest"
        ],
        "second_delta": copy.deepcopy(dict(second_delta)),
        "selected_conditioned_path_id": conditioned_path[
            "conditioned_path_id"
        ],
        "sequence_digest": sequence["content_digest"],
        "exact_intermediate_boundary": canonical_json(second_delta["before_core"])
        == canonical_json(first_delta["after_core"]),
        "protected_distinctions_preserved": conditioned_path[
            "protected_distinctions_preserved"
        ],
        "free_completion_detected": conditioned_path[
            "free_completion_detected"
        ],
        "authority_boundary": copy.deepcopy(_OUTPUT_AUTHORITY),
    }
    material["content_digest"] = canonical_digest(material)
    return material


def _build_nonformal_delta(
    core_raw: Mapping[str, Any], rule: Mapping[str, Any]
) -> dict[str, Any]:
    before = validate_conceptual_core(core_raw)
    candidate_id = stable_identifier(
        "nonformal-contrastive-candidate-v3",
        before["content_digest"],
        rule["decision_rule_digest"],
    )
    physical_interpretation = (
        f"Within {before['physical_carrier']} in {before['regime']}, "
        f"candidate {candidate_id} reverses the explanatory dependence of "
        f"burden {rule['incumbent_decision']['target_burden_id']} and asks "
        "which minimal counter-assumption preserves the registered observables."
    )
    burden_statement = (
        f"Candidate {candidate_id} must identify a minimal counter-assumption "
        f"to burden {rule['incumbent_decision']['target_burden_id']} while "
        "preserving every exact protected observable evaluation."
    )
    correction = (
        f"Withdraw candidate {candidate_id} if its counter-assumption changes "
        "a protected observable, target, regime, or committed quantifier."
    )
    falsifier = (
        f"Exhibit one protected member evaluation for candidate {candidate_id} "
        "that cannot survive the reversed explanatory dependency."
    )
    physics_next_action = (
        f"Construct the minimal carrier-level countermodel for candidate "
        f"{candidate_id} before requesting any symbolic, simulation, theorem, "
        "or continuum support."
    )
    new_burden = {
        "burden_id": stable_identifier(
            "nonformal-contrastive-burden-v3",
            before["content_digest"],
            rule["decision_rule_digest"],
        ),
        "statement": burden_statement,
        "status": "open",
    }
    after_raw = {
        key: copy.deepcopy(value)
        for key, value in before.items()
        if key != "content_digest"
    }
    after_raw["burdens"] = [*after_raw["burdens"], new_burden]
    after = seal_conceptual_core(after_raw)
    original_burden = next(
        row
        for row in before["burdens"]
        if row["burden_id"]
        == rule["incumbent_decision"]["target_burden_id"]
    )
    relation_evidence = _seal(
        {
            "relation_kind": "contrastive_dependency_reversal",
            "source_burden_id": original_burden["burden_id"],
            "source_burden_digest": canonical_digest(original_burden),
            "target_burden_id": new_burden["burden_id"],
            "target_burden_digest": canonical_digest(new_burden),
            "protected_observable_digests": sorted(
                canonical_digest(row)
                for row in before["observables"]
                if row["protected"]
            ),
            "counter_assumption": new_burden["statement"],
        },
        "witness_digest",
    )
    material = {
        "schema_version": "1.0.0",
        "delta_kind": "typed_nonformal_contrastive_dependency_reversal",
        "before_core": before,
        "after_core": after,
        "changed_conceptual_resource": new_burden["statement"],
        "changed_burdens": [new_burden["statement"]],
        "relation_evidence": relation_evidence,
        "witness": {
            "decision_rule_digest": rule["decision_rule_digest"],
            "protected_observable_digests": [
                canonical_digest(row)
                for row in before["observables"]
                if row["protected"]
            ],
            "original_burden_id": rule["incumbent_decision"][
                "target_burden_id"
            ],
            "new_burden_id": new_burden["burden_id"],
            "correction": correction,
            "falsifier": falsifier,
        },
        "candidate_physics_return": {
            "physical_interpretation": physical_interpretation,
            "burden_delta": [burden_statement],
            "correction": correction,
            "falsifier": falsifier,
            "physics_next_action": physics_next_action,
        },
        "authority_boundary": copy.deepcopy(_OUTPUT_AUTHORITY),
    }
    material["content_digest"] = canonical_digest(material)
    return material


def _validate_nonformal_delta(
    core: Mapping[str, Any], rule: Mapping[str, Any], raw: Mapping[str, Any]
) -> dict[str, Any]:
    expected = _build_nonformal_delta(core, rule)
    if canonical_json(raw) != canonical_json(expected):
        _fail("capable nonformal conceptual delta does not independently replay")
    return copy.deepcopy(expected)


def _stage_nontriviality_certificate(
    core: Mapping[str, Any],
    plan: Mapping[str, Any],
    delta: Mapping[str, Any],
    *,
    stage: str,
) -> dict[str, Any]:
    """Replay one finite scope and distinguish structure from formal decoration."""

    kind = plan.get("relation_hypothesis", {}).get("relation_kind")
    lens = _lens_for_plan(plan)
    expected_scope: dict[str, Any] | None = None
    identity_only = False
    mere_relabeling = True
    trivial_mediator = kind == "mediating_factorization"
    vacuous = True
    carrier_effect = False
    if kind == "mediating_factorization":
        expected_scope = _mediator_scope(core, plan["witness"])
        identity_only = expected_scope is None
        mere_relabeling = expected_scope is None
        trivial_mediator = (
            expected_scope is None
            or not expected_scope["mediator_distinct_from_endpoints"]
            or not expected_scope[
                "mediator_members_disjoint_from_registered_carriers"
            ]
        )
        vacuous = expected_scope is None
        carrier_effect = expected_scope is not None
    elif kind == "functorial_transfer":
        expected_scope = _functorial_scope(core, plan["witness"])
        identity_only = expected_scope is None
        mere_relabeling = expected_scope is None
        trivial_mediator = False
        vacuous = expected_scope is None
        carrier_effect = expected_scope is not None
    elif kind == "noncommuting_composition":
        witness = plan["witness"]
        expected_scope = _noncommutation_scope(
            core,
            witness["left_path_relation_ids"],
            witness["right_path_relation_ids"],
        )
        identity_only = False
        mere_relabeling = expected_scope is None
        trivial_mediator = False
        vacuous = expected_scope is None
        carrier_effect = expected_scope is not None
    elif kind == "equivalence_coherence":
        relations = {
            row["relation_id"]: row for row in core["relations"]
        }
        witness = plan["witness"]
        forward = relations.get(witness["forward_relation_id"])
        inverse = relations.get(witness["inverse_relation_id"])
        if forward is not None and inverse is not None:
            expected_scope = _hott_equivalence_scope(
                core,
                forward,
                inverse,
                witness["left_path_inhabitant_ids"],
                witness["right_path_inhabitant_ids"],
                witness["coherence_cell_ids"],
            )
        identity_only = (
            expected_scope is None
            or forward is None
            or forward["source_primitive_id"]
            == forward["target_primitive_id"]
        )
        mere_relabeling = expected_scope is None
        trivial_mediator = False
        vacuous = expected_scope is None
        carrier_effect = expected_scope is not None and not identity_only
    elif kind == "identity_transport":
        relations = {
            row["relation_id"]: row for row in core["relations"]
        }
        witness = plan["witness"]
        forward = relations.get(witness["transport_relation_id"])
        scope = plan.get("finite_scope", {})
        inverse = relations.get(scope.get("inverse_relation_id"))
        if forward is not None and inverse is not None:
            expected_scope = _hott_transport_scope(
                core,
                forward,
                inverse,
                witness["path_inhabitant_ids"],
            )
        action = _relation_action(forward) if forward is not None else {}
        identity_only = bool(action) and all(
            source == target for source, target in action.items()
        )
        mere_relabeling = expected_scope is None
        trivial_mediator = False
        vacuous = expected_scope is None or identity_only
        carrier_effect = expected_scope is not None and not identity_only
    exact_scope = (
        expected_scope is not None
        and canonical_json(plan.get("finite_scope"))
        == canonical_json(expected_scope)
    )
    before_projection = {
        key: core[key]
        for key in ("primitives", "relations", "observables", "inhabitants")
    }
    after = delta.get("after_core", {})
    after_projection = {
        key: after.get(key)
        for key in ("primitives", "relations", "observables", "inhabitants")
    }
    structural_change = canonical_json(before_projection) != canonical_json(
        after_projection
    )
    protected_before = {
        row["observable_id"]: row
        for row in core["observables"]
        if row["protected"]
    }
    protected_after = {
        row["observable_id"]: row
        for row in after.get("observables", [])
        if row.get("protected")
    }
    material = {
        "stage": stage,
        "lens": lens,
        "relation_kind": kind,
        "finite_scope_digest": (
            canonical_digest(expected_scope)
            if expected_scope is not None
            else None
        ),
        "exact_scope_replayed": exact_scope,
        "identity_only": identity_only,
        "mere_relabeling": mere_relabeling,
        "trivial_copied_mediator": trivial_mediator,
        "vacuous_equivalence_or_coherence": vacuous,
        "protected_observable_conservativity": (
            bool(protected_before)
            and all(
                protected_after.get(observable_id) == observable
                for observable_id, observable in protected_before.items()
            )
        ),
        "structural_change_beyond_burden_text": structural_change,
        "carrier_semantics_or_countermodel": carrier_effect
        and structural_change,
        "physically_inert_completion": not (
            carrier_effect and structural_change
        ),
    }
    return {**material, "certificate_digest": canonical_digest(material)}


def _nonformal_nontriviality_certificate(
    core: Mapping[str, Any],
    rule: Mapping[str, Any],
    delta: Mapping[str, Any],
) -> dict[str, Any]:
    valid = False
    try:
        expected = _validate_nonformal_delta(core, rule, delta)
        relation = expected["relation_evidence"]
        original = next(
            row
            for row in core["burdens"]
            if row["burden_id"]
            == rule["incumbent_decision"]["target_burden_id"]
        )
        valid = (
            relation["source_burden_id"] != relation["target_burden_id"]
            and relation["counter_assumption"] != original["statement"]
            and relation["protected_observable_digests"]
            == sorted(
                canonical_digest(row)
                for row in core["observables"]
                if row["protected"]
            )
        )
    except (CentralConceptualRouteError, KeyError, StopIteration):
        valid = False
    material = {
        "stage": "single",
        "lens": "capable_nonformal",
        "relation_kind": "contrastive_dependency_reversal",
        "finite_scope_digest": canonical_digest(
            {"exact_contrastive_delta": delta.get("content_digest")}
        ),
        "exact_scope_replayed": valid,
        "identity_only": not valid,
        "mere_relabeling": not valid,
        "trivial_copied_mediator": False,
        "vacuous_equivalence_or_coherence": False,
        "protected_observable_conservativity": valid,
        "structural_change_beyond_burden_text": False,
        "carrier_semantics_or_countermodel": valid,
        "physically_inert_completion": not valid,
    }
    return {**material, "certificate_digest": canonical_digest(material)}


def _route_nontriviality_evaluation(
    *,
    core: Mapping[str, Any],
    rule: Mapping[str, Any],
    route_id: str,
    candidate_delta: Mapping[str, Any] | None,
    skill_evidence: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    certificates: list[dict[str, Any]] = []
    if candidate_delta is not None and route_id == "capable_nonformal":
        certificates = [
            _nonformal_nontriviality_certificate(core, rule, candidate_delta)
        ]
    elif candidate_delta is not None:
        if candidate_delta.get("delta_kind") == (
            "intermediate_conditioned_category_hott_sequence"
        ):
            stages = [
                (
                    "first",
                    core,
                    candidate_delta.get("first_plan"),
                    candidate_delta.get("first_delta"),
                ),
                (
                    "second",
                    candidate_delta.get("first_delta", {}).get("after_core"),
                    candidate_delta.get("second_plan"),
                    candidate_delta.get("second_delta"),
                ),
            ]
        else:
            stages = [
                (
                    "single",
                    core,
                    skill_evidence[0].get("plan") if skill_evidence else None,
                    candidate_delta,
                )
            ]
        for stage, stage_core, plan, delta in stages:
            try:
                if not all(
                    isinstance(item, Mapping)
                    for item in (stage_core, plan, delta)
                ):
                    _fail("nontriviality stage is incomplete")
                certificates.append(
                    _stage_nontriviality_certificate(
                        stage_core, plan, delta, stage=stage
                    )
                )
            except (
                CentralConceptualRouteError,
                FormalConceptTransformationError,
                KeyError,
                TypeError,
                ValueError,
            ):
                break
    contract_bound = (
        rule["carrier_predicate"].get("nontriviality_contract")
        == _NONTRIVIALITY_CONTRACT
    )
    material = {
        "contract_digest": canonical_digest(_NONTRIVIALITY_CONTRACT),
        "contract_bound": contract_bound,
        "stage_certificates": certificates,
        "nonidentity_or_contrastive_effect": bool(certificates)
        and all(not row["identity_only"] for row in certificates),
        "mere_relabeling_rejected": bool(certificates)
        and all(not row["mere_relabeling"] for row in certificates),
        "trivial_mediator_rejected": bool(certificates)
        and all(not row["trivial_copied_mediator"] for row in certificates),
        "vacuous_equivalence_or_coherence_rejected": bool(certificates)
        and all(
            not row["vacuous_equivalence_or_coherence"]
            for row in certificates
        ),
        "protected_observable_conservativity_replayed": bool(certificates)
        and all(
            row["protected_observable_conservativity"]
            for row in certificates
        ),
        "carrier_semantics_or_countermodel_replayed": bool(certificates)
        and all(
            row["carrier_semantics_or_countermodel"]
            for row in certificates
        ),
        "physically_inert_completion_rejected": bool(certificates)
        and all(not row["physically_inert_completion"] for row in certificates),
        "exact_finite_scope_replayed": bool(certificates)
        and all(row["exact_scope_replayed"] for row in certificates),
        "comparative_value_authorized": False,
        "physics_value_authorized": False,
    }
    return {**material, "nontriviality_digest": canonical_digest(material)}


def _decision_rule_evidence(
    *,
    core: Mapping[str, Any],
    rule: Mapping[str, Any],
    route_id: str,
    status: str,
    candidate_delta: Mapping[str, Any] | None,
    skill_evidence: Sequence[Mapping[str, Any]],
    quarantine_reasons: Sequence[str],
) -> dict[str, Any]:
    """Evaluate the frozen rule against exact before/after witness bytes."""

    before = candidate_delta.get("before_core") if candidate_delta else None
    after = candidate_delta.get("after_core") if candidate_delta else None
    protected_before = {
        row["observable_id"]: row
        for row in core["observables"]
        if row["protected"]
    }
    protected_after = (
        {
            row["observable_id"]: row
            for row in after.get("observables", [])
            if row.get("protected")
        }
        if isinstance(after, Mapping)
        else {}
    )
    skill_replays: list[dict[str, Any]] = []
    relation_witnesses: list[dict[str, Any]] = []
    producer_replay_valid = False
    if route_id == "capable_nonformal" and candidate_delta is not None:
        try:
            expected_nonformal = _validate_nonformal_delta(
                core, rule, candidate_delta
            )
            relation_evidence = expected_nonformal["relation_evidence"]
            relation_witnesses = [
                {
                    "stage": "single",
                    "relation_kind": relation_evidence["relation_kind"],
                    "source_anchor_id": relation_evidence["source_burden_id"],
                    "target_anchor_id": relation_evidence["target_burden_id"],
                    "stage_core_digest": core["content_digest"],
                    "plan_digest": None,
                    "relation_digest": relation_evidence["witness_digest"],
                    "witness_digest": relation_evidence["witness_digest"],
                    "consequence_digest": canonical_digest(
                        expected_nonformal["changed_burdens"]
                    ),
                    "delta_digest": expected_nonformal["content_digest"],
                    "producer_binding_digest": relation_evidence[
                        "witness_digest"
                    ],
                    "finite_witness_valid": True,
                }
            ]
            producer_replay_valid = True
        except (CentralConceptualRouteError, KeyError, StopIteration):
            producer_replay_valid = False
    elif candidate_delta is not None:
        if candidate_delta.get("delta_kind") == (
            "intermediate_conditioned_category_hott_sequence"
        ):
            stages = [
                (
                    "first",
                    core,
                    candidate_delta.get("first_plan"),
                    candidate_delta.get("first_delta"),
                ),
                (
                    "second",
                    candidate_delta.get("first_delta", {}).get("after_core"),
                    candidate_delta.get("second_plan"),
                    candidate_delta.get("second_delta"),
                ),
            ]
        else:
            stages = [
                (
                    "single",
                    core,
                    skill_evidence[0].get("plan") if skill_evidence else None,
                    candidate_delta,
                )
            ]
        producer_replay_valid = len(stages) == len(skill_evidence)
        for index, (stage, stage_core, plan, actual_delta) in enumerate(stages):
            row = skill_evidence[index] if index < len(skill_evidence) else {}
            replay: dict[str, Any]
            case_binding_valid = False
            delta_binding_valid = False
            expected_binding: dict[str, Any] | None = None
            try:
                if (
                    not isinstance(stage_core, Mapping)
                    or not isinstance(plan, Mapping)
                    or not isinstance(actual_delta, Mapping)
                    or row.get("stage") != stage
                    or canonical_json(row.get("plan")) != canonical_json(plan)
                ):
                    _fail("formal skill stage is detached from the candidate delta")
                expected_case = _meaning_case(
                    core=stage_core,
                    rule=rule,
                    plan=plan,
                    route_id=route_id,
                    stage=stage,
                )
                if canonical_json(row.get("case")) != canonical_json(expected_case):
                    _fail("formal skill case is detached from the exact stage core")
                artifact = row["artifact"]
                replay = validate_task_derived_artifact(expected_case, artifact)
                expected_binding = _forge_artifact_binding(
                    core=stage_core,
                    plan=plan,
                    route_id=route_id,
                    stage=stage,
                    case=expected_case,
                    artifact=artifact,
                )
                case_binding_valid = canonical_json(row.get("binding")) == canonical_json(
                    expected_binding
                )
                replayed_delta, _ = _apply_postcommit_plan(stage_core, plan)
                delta_binding_valid = canonical_json(replayed_delta) == canonical_json(
                    actual_delta
                )
            except (
                CentralConceptualRouteError,
                FormalConceptTransformationError,
                FormalReasoningError,
                KeyError,
                StopIteration,
                TypeError,
                ValueError,
            ) as exc:
                replay = {"status": "invalid", "reason": type(exc).__name__}
            artifact = row.get("artifact", {})
            handback = (
                artifact.get("physics_handback", {})
                if isinstance(artifact, Mapping)
                else {}
            )
            proposed = handback.get("proposed_next_decision")
            skill_replays.append(
                {
                    "artifact_digest": (
                        artifact.get("artifact_digest")
                        if isinstance(artifact, Mapping)
                        and isinstance(artifact.get("artifact_digest"), str)
                        else canonical_digest({"invalid_artifact_stage": stage})
                    ),
                    "stage": stage,
                    "stage_core_digest": (
                        stage_core.get("content_digest")
                        if isinstance(stage_core, Mapping)
                        else canonical_digest({"invalid_stage_core": stage})
                    ),
                    "plan_digest": (
                        canonical_digest(plan)
                        if isinstance(plan, Mapping)
                        else canonical_digest({"invalid_plan": stage})
                    ),
                    "binding_digest": (
                        expected_binding["binding_digest"]
                        if expected_binding is not None
                        else canonical_digest({"invalid_binding": stage})
                    ),
                    "replay": replay,
                    "case_binding_valid": case_binding_valid,
                    "delta_binding_valid": delta_binding_valid,
                    "decision_changed": handback.get("handback_status")
                    == "decision_changed",
                    "candidate_action_matches": bool(
                        isinstance(proposed, Mapping)
                        and proposed.get("decision_id")
                        == rule["eligible_decision"]["decision_id"]
                        and proposed.get("action")
                        == rule["eligible_decision"]["action"]
                        and proposed.get("target_burden_id")
                        == rule["eligible_decision"]["target_burden_id"]
                    ),
                }
            )
            relation = plan.get("relation_hypothesis", {}) if isinstance(plan, Mapping) else {}
            relation_witnesses.append(
                {
                    "stage": stage,
                    "relation_kind": relation.get("relation_kind", "invalid"),
                    "source_anchor_id": relation.get(
                        "source_primitive_id", "invalid"
                    ),
                    "target_anchor_id": relation.get(
                        "target_primitive_id", "invalid"
                    ),
                    "stage_core_digest": skill_replays[-1]["stage_core_digest"],
                    "plan_digest": skill_replays[-1]["plan_digest"],
                    "relation_digest": canonical_digest(relation),
                    "witness_digest": canonical_digest(
                        plan.get("witness", {}) if isinstance(plan, Mapping) else {}
                    ),
                    "consequence_digest": canonical_digest(
                        plan.get("consequence_contract", {})
                        if isinstance(plan, Mapping)
                        else {}
                    ),
                    "delta_digest": (
                        actual_delta.get("content_digest")
                        if isinstance(actual_delta, Mapping)
                        else canonical_digest({"invalid_delta": stage})
                    ),
                    "producer_binding_digest": skill_replays[-1][
                        "binding_digest"
                    ],
                    "finite_witness_valid": case_binding_valid
                    and delta_binding_valid,
                }
            )
            producer_replay_valid = (
                producer_replay_valid
                and case_binding_valid
                and delta_binding_valid
            )

    before_burdens = (
        {row["burden_id"]: row for row in before.get("burdens", [])}
        if isinstance(before, Mapping)
        else {}
    )
    after_burdens = (
        {row["burden_id"]: row for row in after.get("burdens", [])}
        if isinstance(after, Mapping)
        else {}
    )
    changed_burden_rows = [
        {
            "burden_id": burden_id,
            "before_digest": (
                canonical_digest(before_burdens[burden_id])
                if burden_id in before_burdens
                else None
            ),
            "after_digest": canonical_digest(after_burden),
            "after_statement": after_burden["statement"],
        }
        for burden_id, after_burden in sorted(after_burdens.items())
        if before_burdens.get(burden_id) != after_burden
    ]
    protected_checks: list[dict[str, Any]] = []
    for observable_id, observable in sorted(protected_before.items()):
        observed_after = protected_after.get(observable_id)
        before_values = {
            row["member_id"]: row["value"] for row in observable["evaluations"]
        }
        after_values = (
            {
                row["member_id"]: row["value"]
                for row in observed_after.get("evaluations", [])
            }
            if isinstance(observed_after, Mapping)
            else {}
        )
        counterexample_members = sorted(
            member_id
            for member_id in set(before_values) | set(after_values)
            if before_values.get(member_id) != after_values.get(member_id)
        )
        metadata_preserved = observed_after == observable
        protected_checks.append(
            {
                "observable_id": observable_id,
                "before_digest": canonical_digest(observable),
                "after_digest": (
                    canonical_digest(observed_after)
                    if isinstance(observed_after, Mapping)
                    else None
                ),
                "counterexample_member_ids": counterexample_members,
                "metadata_preserved": metadata_preserved,
                "preserved": metadata_preserved and not counterexample_members,
            }
        )
    predicate = rule["carrier_predicate"]
    exact_before = isinstance(before, Mapping) and canonical_json(before) == canonical_json(core)
    target_preserved = (
        isinstance(after, Mapping)
        and after.get("target_id") == core["target_id"] == rule["target_id"]
        and after.get("obligation_id")
        == core["obligation_id"]
        == rule["obligation_id"]
        and after.get("physical_carrier")
        == core["physical_carrier"]
        == rule["physical_carrier"]
        and after.get("regime") == core["regime"] == rule["regime"]
        and [row["statement"] for row in after.get("quantifiers", [])]
        == rule["quantifiers"]
    )
    protected_preserved = bool(protected_checks) and all(
        row["preserved"] for row in protected_checks
    )
    core_changed = isinstance(after, Mapping) and after.get("content_digest") != core[
        "content_digest"
    ]
    burden_changed = bool(changed_burden_rows)
    finite_relation_witness_bound = bool(relation_witnesses) and all(
        row["finite_witness_valid"] for row in relation_witnesses
    )
    executable_predicate_bound = (
        predicate["before_core_digest"] == core["content_digest"]
        and predicate["target_burden_id"]
        == rule["incumbent_decision"]["target_burden_id"]
        and predicate["protected_observable_digests"]
        == sorted(row["before_digest"] for row in protected_checks)
        and predicate["nontriviality_contract"] == _NONTRIVIALITY_CONTRACT
    )
    nontriviality = _route_nontriviality_evaluation(
        core=core,
        rule=rule,
        route_id=route_id,
        candidate_delta=candidate_delta,
        skill_evidence=skill_evidence,
    )
    evaluation_value = all(
        (
            exact_before,
            target_preserved,
            protected_preserved,
            core_changed,
            burden_changed,
            finite_relation_witness_bound,
            producer_replay_valid,
            executable_predicate_bound,
            nontriviality["contract_bound"],
            nontriviality["nonidentity_or_contrastive_effect"],
            nontriviality["mere_relabeling_rejected"],
            nontriviality["trivial_mediator_rejected"],
            nontriviality["vacuous_equivalence_or_coherence_rejected"],
            nontriviality[
                "protected_observable_conservativity_replayed"
            ],
            nontriviality["carrier_semantics_or_countermodel_replayed"],
            nontriviality["physically_inert_completion_rejected"],
            nontriviality["exact_finite_scope_replayed"],
        )
    )
    route_eligible = status == "completed" and not quarantine_reasons
    entailed_value = evaluation_value and route_eligible
    entailment_row = copy.deepcopy(rule["entailment_table"][1 if entailed_value else 0])
    canonical_action_entailment = (
        entailment_row["decision_id"]
        == (
            rule["eligible_decision"]["decision_id"]
            if entailed_value
            else rule["incumbent_decision"]["decision_id"]
        )
        and rule["eligible_decision"]["action"]
        == _canonical_eligible_action(rule, predicate)
    )
    checks = {
        "route_completed_without_quarantine": route_eligible,
        "exact_before_core": exact_before,
        "target_carrier_regime_quantifiers_preserved": target_preserved,
        "protected_observables_preserved_exactly": protected_preserved,
        "conceptual_core_changed": core_changed,
        "declared_burden_retained": isinstance(after, Mapping)
        and any(
            row["burden_id"]
            == rule["incumbent_decision"]["target_burden_id"]
            for row in after.get("burdens", [])
        ),
        "changed_burden_witnessed": burden_changed,
        "finite_relation_witness_bound": finite_relation_witness_bound,
        "carrier_counterexample_absent": protected_preserved,
        "precommitted_executable_predicate_bound": executable_predicate_bound,
        "registered_semantic_producer_replayed": producer_replay_valid,
        "precommitted_nontriviality_contract_bound": nontriviality[
            "contract_bound"
        ],
        "nonidentity_or_contrastive_effect_replayed": nontriviality[
            "nonidentity_or_contrastive_effect"
        ],
        "mere_relabeling_rejected": nontriviality[
            "mere_relabeling_rejected"
        ],
        "trivial_mediator_rejected": nontriviality[
            "trivial_mediator_rejected"
        ],
        "vacuous_equivalence_or_coherence_rejected": nontriviality[
            "vacuous_equivalence_or_coherence_rejected"
        ],
        "protected_observable_conservativity_replayed": nontriviality[
            "protected_observable_conservativity_replayed"
        ],
        "carrier_semantics_or_countermodel_replayed": nontriviality[
            "carrier_semantics_or_countermodel_replayed"
        ],
        "physically_inert_completion_rejected": nontriviality[
            "physically_inert_completion_rejected"
        ],
        "exact_finite_scope_replayed": nontriviality[
            "exact_finite_scope_replayed"
        ],
        "canonical_action_entailment": canonical_action_entailment,
    }
    predicate_evaluation = {
        "before_core_digest": (
            before.get("content_digest") if isinstance(before, Mapping) else None
        ),
        "after_core_digest": (
            after.get("content_digest") if isinstance(after, Mapping) else None
        ),
        "relation_witnesses": relation_witnesses,
        "changed_burden_rows": changed_burden_rows,
        "protected_observable_checks": protected_checks,
        "exact_carrier_regime_quantifiers": target_preserved,
        "core_changed": core_changed,
        "burden_changed": burden_changed,
        "finite_relation_witness_bound": finite_relation_witness_bound,
        "producer_replay_valid": producer_replay_valid,
        "nontriviality_evaluation": nontriviality,
        "counterexample_absent": protected_preserved,
        "predicate_value_before_route_status": evaluation_value,
    }
    predicate_evaluation["evaluation_digest"] = canonical_digest(
        predicate_evaluation
    )
    predicate_satisfied = all(checks.values())
    return {
        "rule_id": rule["rule_id"],
        "rule_digest": rule["decision_rule_digest"],
        "predicate_id": predicate["predicate_id"],
        "predicate_digest": predicate["predicate_digest"],
        "route_id": route_id,
        "checks": checks,
        "predicate_evaluation": predicate_evaluation,
        "entailment_row": entailment_row,
        "entailed_decision": copy.deepcopy(
            rule["eligible_decision"]
            if predicate_satisfied
            else rule["incumbent_decision"]
        ),
        "skill_replays": skill_replays,
        "candidate_delta_digest": (
            candidate_delta.get("content_digest") if candidate_delta else None
        ),
        "predicate_satisfied": predicate_satisfied,
        "authority": (
            "Exact finite rule replay may change one theory-research action; "
            "it grants no truth, theorem, physics-value, or investment authority."
        ),
    }


def _criterion_evidence(
    *,
    rule_evidence: Mapping[str, Any],
    changed_burdens: Sequence[str],
    unification_links: Sequence[str],
) -> list[dict[str, Any]]:
    checks = rule_evidence["checks"]
    statuses = {
        "target_relevance": (
            "satisfied"
            if checks["target_carrier_regime_quantifiers_preserved"]
            else "failed"
        ),
        "protected_success_preservation": (
            "satisfied"
            if checks["protected_observables_preserved_exactly"]
            else "failed"
        ),
        "consequence_specificity": (
            "satisfied"
            if checks["finite_relation_witness_bound"]
            and checks["canonical_action_entailment"]
            else "failed"
        ),
        "burden_localization": (
            "satisfied"
            if checks["declared_burden_retained"]
            and checks["changed_burden_witnessed"]
            and bool(changed_burdens)
            else "failed"
        ),
        "unification_compression": (
            "partial" if unification_links else "failed"
        ),
        "discriminating_falsifier": (
            "satisfied"
            if checks["carrier_counterexample_absent"]
            and checks["precommitted_executable_predicate_bound"]
            else "failed"
        ),
        # A changed finite core earns inspection, never conceptual-depth
        # authority.  Hence this criterion cannot exceed partial internally.
        "conceptual_depth": (
            "partial" if checks["conceptual_core_changed"] else "failed"
        ),
    }
    evaluation = rule_evidence["predicate_evaluation"]
    basis = {
        "target_relevance": {
            "check": checks["target_carrier_regime_quantifiers_preserved"],
            "exact_carrier_regime_quantifiers": evaluation[
                "exact_carrier_regime_quantifiers"
            ],
        },
        "protected_success_preservation": {
            "check": checks["protected_observables_preserved_exactly"],
            "protected_observable_checks": evaluation[
                "protected_observable_checks"
            ],
        },
        "consequence_specificity": {
            "finite_relation_witness_bound": checks[
                "finite_relation_witness_bound"
            ],
            "canonical_action_entailment": checks["canonical_action_entailment"],
            "relation_witnesses": evaluation["relation_witnesses"],
        },
        "burden_localization": {
            "declared_burden_retained": checks["declared_burden_retained"],
            "changed_burden_witnessed": checks["changed_burden_witnessed"],
            "changed_burdens": list(changed_burdens),
            "changed_burden_rows": evaluation["changed_burden_rows"],
        },
        "unification_compression": {
            "unification_links": list(unification_links),
            "links_present": bool(unification_links),
        },
        "discriminating_falsifier": {
            "carrier_counterexample_absent": checks[
                "carrier_counterexample_absent"
            ],
            "precommitted_executable_predicate_bound": checks[
                "precommitted_executable_predicate_bound"
            ],
            "predicate_digest": rule_evidence["predicate_digest"],
        },
        "conceptual_depth": {
            "conceptual_core_changed": checks["conceptual_core_changed"],
            "before_core_digest": evaluation["before_core_digest"],
            "after_core_digest": evaluation["after_core_digest"],
        },
    }
    limitations = {
        "unification_compression": (
            "links_do_not_establish_internal_unification_authority"
        ),
        "conceptual_depth": (
            "finite_change_does_not_establish_internal_conceptual_depth"
        ),
    }
    result: list[dict[str, Any]] = []
    for criterion in ADJUDICATION_CRITERIA:
        status = statuses[criterion]
        support_refs = (
            [canonical_digest({"criterion": criterion, "basis": basis[criterion]})]
            if status in {"partial", "satisfied"}
            else []
        )
        counter_refs = (
            [
                canonical_digest(
                    {
                        "criterion": criterion,
                        "basis": basis[criterion],
                        "limitation": limitations.get(
                            criterion, "declared_criterion_checks_not_satisfied"
                        ),
                    }
                )
            ]
            if status in {"failed", "partial"}
            else []
        )
        result.append(
            {
                "criterion": criterion,
                "status": status,
                "evidence_refs": support_refs,
                "counterevidence_refs": counter_refs,
                "method_or_vocabulary_bonus": False,
                "conceptual_merit_authorized": False,
            }
        )
    return result


def _candidate_physics_return(
    *,
    core: Mapping[str, Any],
    route_id: str,
    candidate_delta: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Reconstruct the physical handback from the exact candidate delta.

    The committed decision rule still decides whether a research action may
    change, but it no longer supplies route-invariant prose.  Interpretation,
    burden, correction, falsifier, and next action are projected from the
    actual formal plans (or the typed nonformal delta) and bound by one digest.
    """

    if candidate_delta is None:
        material = {
            "route_id": route_id,
            "candidate_delta_digest": None,
            "physical_interpretation": (
                f"Route {route_id} produced no replayable carrier candidate "
                f"for {core['physical_carrier']} in {core['regime']}."
            ),
            "burden_delta": [],
            "correction": (
                f"Keep route {route_id} unavailable until an exact candidate "
                "delta and finite witness can be replayed."
            ),
            "falsifier": (
                f"No route-{route_id} falsifier is admissible without a "
                "candidate-bound finite scope."
            ),
            "physics_next_action": (
                f"Do not commission support work for route {route_id}; first "
                "construct a replayable theory-side candidate."
            ),
            "candidate_relation_digests": [],
            "candidate_consequence_digests": [],
        }
        return {**material, "basis_digest": canonical_digest(material)}

    if candidate_delta.get("delta_kind") == (
        "typed_nonformal_contrastive_dependency_reversal"
    ):
        projected = candidate_delta.get("candidate_physics_return")
        if not isinstance(projected, Mapping) or set(projected) != {
            "physical_interpretation",
            "burden_delta",
            "correction",
            "falsifier",
            "physics_next_action",
        }:
            projected = {
                "physical_interpretation": (
                    f"Route {route_id} supplied a malformed nonformal physics "
                    "return and therefore has no usable interpretation."
                ),
                "burden_delta": [],
                "correction": (
                    f"Quarantine route {route_id} until its typed nonformal "
                    "physics return replays."
                ),
                "falsifier": (
                    f"Malformed route-{route_id} return is itself a protocol "
                    "counterexample, not a physical falsifier."
                ),
                "physics_next_action": (
                    f"Repair route {route_id} before commissioning any support."
                ),
            }
        material = {
            "route_id": route_id,
            "candidate_delta_digest": candidate_delta.get("content_digest"),
            **copy.deepcopy(dict(projected)),
            "candidate_relation_digests": [
                canonical_digest(
                    candidate_delta.get("relation_evidence", {})
                )
            ],
            "candidate_consequence_digests": [
                canonical_digest(projected)
            ],
        }
        return {**material, "basis_digest": canonical_digest(material)}

    plans: list[Mapping[str, Any]]
    if candidate_delta.get("delta_kind") == (
        "intermediate_conditioned_category_hott_sequence"
    ):
        plans = [
            plan
            for plan in (
                candidate_delta.get("first_plan"),
                candidate_delta.get("second_plan"),
            )
            if isinstance(plan, Mapping)
        ]
    else:
        relation = candidate_delta.get("relation_hypothesis")
        consequence = candidate_delta.get("consequence_contract")
        plans = (
            [
                {
                    "relation_hypothesis": relation,
                    "consequence_contract": consequence,
                }
            ]
            if isinstance(relation, Mapping)
            and isinstance(consequence, Mapping)
            else []
        )

    def unique_text(field: str) -> list[str]:
        values: list[str] = []
        for plan in plans:
            consequence = plan.get("consequence_contract", {})
            value = (
                consequence.get(field)
                if isinstance(consequence, Mapping)
                else None
            )
            if isinstance(value, str) and value and value not in values:
                values.append(value)
        return values

    interpretations = unique_text("explanatory_gain")
    burdens = unique_text("changed_burden")
    corrections = unique_text("correction")
    falsifiers = unique_text("falsifier")
    actions = unique_text("physics_next_action")
    relation_digests = [
        canonical_digest(plan.get("relation_hypothesis", {}))
        for plan in plans
    ]
    consequence_digests = [
        canonical_digest(plan.get("consequence_contract", {}))
        for plan in plans
    ]
    valid = bool(
        plans
        and interpretations
        and burdens
        and corrections
        and falsifiers
        and actions
    )
    material = {
        "route_id": route_id,
        "candidate_delta_digest": candidate_delta.get("content_digest"),
        "physical_interpretation": (
            " Then ".join(interpretations)
            if valid
            else (
                f"Route {route_id} has no complete candidate-derived physical "
                "interpretation."
            )
        ),
        "burden_delta": burdens if valid else [],
        "correction": (
            " Then ".join(corrections)
            if valid
            else f"Quarantine incomplete route {route_id}."
        ),
        "falsifier": (
            " Then ".join(falsifiers)
            if valid
            else f"No route-{route_id} physical falsifier is authorized."
        ),
        "physics_next_action": (
            " Then ".join(actions)
            if valid
            else f"Do not commission support work for route {route_id}."
        ),
        "candidate_relation_digests": relation_digests,
        "candidate_consequence_digests": consequence_digests,
    }
    return {**material, "basis_digest": canonical_digest(material)}


def _shared_handback(
    *,
    route_id: str,
    payload: Mapping[str, Any],
    status: str,
    evidence: Mapping[str, Any] | None,
    changed_burdens: Sequence[str],
    changed_resource: str,
    unification_links: Sequence[str],
    quarantine_reasons: Sequence[str],
    candidate_delta: Mapping[str, Any] | None,
    skill_evidence: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    core = payload["conceptual_core"]
    rule = payload["physics_decision_rule"]
    candidate_physics = _candidate_physics_return(
        core=core,
        route_id=route_id,
        candidate_delta=candidate_delta,
    )
    effective_burdens = (
        candidate_physics["burden_delta"]
        if candidate_delta is not None
        else list(changed_burdens)
    )
    rule_evidence = _decision_rule_evidence(
        core=core,
        rule=rule,
        route_id=route_id,
        status=status,
        candidate_delta=candidate_delta,
        skill_evidence=skill_evidence,
        quarantine_reasons=quarantine_reasons,
    )
    admissible = rule_evidence["predicate_satisfied"]
    decision_replay = {
        "rule_id": rule["rule_id"],
        "rule_digest": rule["decision_rule_digest"],
        "baseline": copy.deepcopy(rule["incumbent_decision"]),
        "candidate": copy.deepcopy(rule_evidence["entailed_decision"]),
        "research_action_changed": bool(admissible),
        "change_scope": "carrier_specific_theory_research_action_only",
        "physics_truth_authorized": False,
    }
    content_projection = {
        "target_id": core["target_id"],
        "obligation_id": core["obligation_id"],
        "physical_carrier": core["physical_carrier"],
        "regime": core["regime"],
        "quantifiers": [row["statement"] for row in core["quantifiers"]],
        "protected_successes": copy.deepcopy(rule["protected_successes"]),
        "physical_interpretation": candidate_physics[
            "physical_interpretation"
        ],
        "candidate_physics_basis_digest": candidate_physics[
            "basis_digest"
        ],
        "explanatory_dependency": candidate_physics[
            "physical_interpretation"
        ],
        "changed_conceptual_resource": changed_resource,
        "changed_burdens": list(effective_burdens),
        "correction": candidate_physics["correction"],
        "falsifier": candidate_physics["falsifier"],
        "physics_next_action": candidate_physics["physics_next_action"],
        "untouched_physics_gates": copy.deepcopy(rule["untouched_physics_gates"]),
        "unification_links": list(unification_links),
        "evidence_chain_digest": canonical_digest(evidence) if evidence is not None else None,
        "conceptual_delta_digest": rule_evidence["candidate_delta_digest"],
        "decision_rule_evidence": rule_evidence,
        "criterion_evidence": _criterion_evidence(
            rule_evidence=rule_evidence,
            changed_burdens=effective_burdens,
            unification_links=unification_links,
        ),
        "decision_replay": decision_replay,
    }
    return _seal(
        {
            "handback_id": stable_identifier(
                "central-conceptual-physics-handback-v3",
                payload["content_digest"],
                route_id,
                status,
                content_projection,
                list(quarantine_reasons),
            ),
            "route_id": route_id,
            "handback_status": (
                "admissible_for_blind_comparison" if admissible else "quarantined_or_unavailable"
            ),
            "content_projection": content_projection,
            "quarantine_reasons": list(quarantine_reasons),
            "experiment_role": "secondary_theory_requested_falsifier_only",
            "authority_boundary": copy.deepcopy(_OUTPUT_AUTHORITY),
        },
        "handback_digest",
    )


def execute_route_author_payload(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Derive and execute one route plan inside its postcommit process."""

    payload = copy.deepcopy(dict(raw))
    _strict(payload, {"schema_version", "route_id", "commission", "payload_digest"}, "route author payload")
    _validate_self_digest(payload, "payload_digest", "route author payload")
    if payload["schema_version"] != SCHEMA_VERSION or payload["route_id"] not in ROUTE_ORDER:
        _fail("route author payload version or route identity drift")
    commission = payload["commission"]
    if not isinstance(commission, Mapping):
        _fail("route author commission is absent")
    _validate_self_digest(commission, "commission_digest", "route commission")
    committed = _decode_committed_input(commission)
    core = committed["conceptual_core"]
    rule = committed["physics_decision_rule"]
    route_id = payload["route_id"]
    producer_rows = [
        row
        for row in commission.get("registry_binding", {}).get("routes", [])
        if row.get("route_id") == route_id
    ]
    producer_binding = (
        copy.deepcopy(producer_rows[0]) if len(producer_rows) == 1 else None
    )
    evidence: dict[str, Any] | None = None
    candidate_delta: dict[str, Any] | None = None
    skill_evidence: list[dict[str, Any]] = []
    status = "unavailable"
    reasons: list[str] = []
    changed_burdens: list[str] = []
    changed_resource = "No route-specific conceptual resource was available."
    unification_links: list[str] = []
    records: list[dict[str, Any]] = []

    try:
        if route_id == "capable_nonformal":
            candidate_delta = _validate_nonformal_delta(
                core, rule, _build_nonformal_delta(core, rule)
            )
            status = "completed"
            nontriviality_certificate = _nonformal_nontriviality_certificate(
                core, rule, candidate_delta
            )
            if nontriviality_certificate["physically_inert_completion"]:
                reasons.append("nontriviality_predicate_failed")
                status = "quarantined"
            changed_resource = (
                "Reverse the incumbent explanatory dependency and demand the minimal "
                "counter-assumption that preserves every protected success."
            )
            changed_burdens = list(candidate_delta["changed_burdens"])
            unification_links = [
                f"protected-observable:{canonical_digest(row)}"
                for row in core["observables"]
                if row["protected"]
            ]
            evidence = {
                "method": "capable_nonformal_contrastive_reversal",
                "source_core_digest": core["content_digest"],
                "typed_conceptual_delta": candidate_delta,
                "caller_plan_used": False,
                "nontriviality_certificate": nontriviality_certificate,
            }
            records = [
                {
                    "task_id": stable_identifier(
                        "nonformal-postcommit-author-v3", core["content_digest"], rule["rule_id"]
                    ),
                    "category_check": None,
                    "hott_check": None,
                    "semantic_delta": candidate_delta,
                }
            ]
        elif route_id in {"categorical", "hott"}:
            plan = (
                _derive_category_plan(core, rule)
                if route_id == "categorical"
                else _derive_hott_plan(core, rule)
            )
            if plan is None:
                reasons.append(f"{route_id}_finite_witness_unavailable")
            else:
                skill_evidence = [
                    _forge_skill_evidence(
                        core=core,
                        rule=rule,
                        plan=plan,
                        route_id=route_id,
                        stage="single",
                    )
                ]
                delta, replay = _apply_postcommit_plan(core, plan)
                nontriviality_certificate = _stage_nontriviality_certificate(
                    core, plan, delta, stage="single"
                )
                candidate_delta = delta
                evidence = {
                    "plan": plan,
                    "skill_reuse": skill_evidence,
                    "delta": delta,
                    "replay": replay,
                    "nontriviality_certificate": nontriviality_certificate,
                }
                if replay["protected_erasure_detected"]:
                    reasons.append("protected_observable_erasure")
                if replay["after_status"] == "counterfactual_only":
                    reasons.append("free_completion_counterfactual")
                if nontriviality_certificate[
                    "physically_inert_completion"
                ]:
                    reasons.append("nontriviality_predicate_failed")
                status = "completed" if not reasons else "quarantined"
                changed_burdens = [delta["semantic_delta"]["changed_burden"]]
                changed_resource = delta["relation_hypothesis"]["statement"]
                unification_links = [
                    f"premise:{premise}"
                    for premise in delta["relation_hypothesis"]["premise_ids"]
                ]
                summary = {
                    "relation_kind": replay["relation_kind"],
                    "constructor_id": replay["constructor_id"],
                    "after_status": replay["after_status"],
                    "witness_digest": delta["construction"]["witness_digest"],
                }
                records = [
                    {
                        "task_id": plan["transformation_id"],
                        "category_check": (
                            {
                                **summary,
                                "mismatch_elements": (
                                    ["protected_observable_erasure"]
                                    if replay["protected_erasure_detected"]
                                    else []
                                ),
                            }
                            if route_id == "categorical"
                            else None
                        ),
                        "hott_check": (
                            {
                                **summary,
                                "boundary_materialization_status": (
                                    "replayed_finite_level_one_boundaries"
                                ),
                                "round_trip_holds": True,
                                "finite_scope": copy.deepcopy(
                                    plan["finite_scope"]
                                ),
                            }
                            if route_id == "hott"
                            else None
                        ),
                        "semantic_delta": delta,
                    }
                ]
        else:
            first_lens, second_lens = (
                ("categorical", "hott")
                if route_id == "category_then_hott"
                else ("hott", "categorical")
            )
            first_plan = (
                _derive_category_plan(core, rule)
                if first_lens == "categorical"
                else _derive_hott_plan(core, rule)
            )
            if first_plan is None:
                reasons.append(f"{first_lens}_first_stage_witness_unavailable")
            else:
                first_skill = _forge_skill_evidence(
                    core=core,
                    rule=rule,
                    plan=first_plan,
                    route_id=route_id,
                    stage="first",
                )
                first_delta, first_replay = _apply_postcommit_plan(
                    core, first_plan
                )
                candidate_delta = first_delta
                if first_replay["protected_erasure_detected"]:
                    reasons.append("protected_observable_erasure")
                if first_replay["after_status"] == "counterfactual_only":
                    reasons.append("free_completion_counterfactual")
                if reasons:
                    status = "quarantined"
                intermediate = first_delta["after_core"]
                second_plan = (
                    _derive_category_plan(intermediate, rule)
                    if second_lens == "categorical"
                    else _derive_hott_plan(intermediate, rule)
                )
                if second_plan is None:
                    reasons.append(
                        f"{second_lens}_intermediate_stage_witness_unavailable"
                    )
                elif not reasons:
                    second_skill = _forge_skill_evidence(
                        core=intermediate,
                        rule=rule,
                        plan=second_plan,
                        route_id=route_id,
                        stage="second",
                    )
                    second_delta, second_replay = _apply_postcommit_plan(
                        intermediate, second_plan
                    )
                    first_nontriviality = _stage_nontriviality_certificate(
                        core, first_plan, first_delta, stage="first"
                    )
                    second_nontriviality = _stage_nontriviality_certificate(
                        intermediate,
                        second_plan,
                        second_delta,
                        stage="second",
                    )
                    # The shared sequence algebra validates its historical
                    # five-field plan shape.  Central finite-scope certificates
                    # remain separately bound in the exact full plans below.
                    sequence_first_plan = {
                        key: copy.deepcopy(value)
                        for key, value in first_plan.items()
                        if key != "finite_scope"
                    }
                    sequence_second_plan = {
                        key: copy.deepcopy(value)
                        for key, value in second_plan.items()
                        if key != "finite_scope"
                    }
                    sequence = build_conditioned_formal_transformation_sequence(
                        core,
                        sequence_first_plan,
                        first_delta,
                        sequence_second_plan,
                        second_delta,
                    )
                    validate_conditioned_formal_transformation_sequence(
                        sequence
                    )
                    conditioned_path = sequence["conditioned_path"]
                    candidate_delta = _build_conditioned_sequence_delta(
                        base_core=core,
                        route_id=route_id,
                        first_plan=first_plan,
                        first_delta=first_delta,
                        second_plan=second_plan,
                        second_delta=second_delta,
                        sequence=sequence,
                        conditioned_path=conditioned_path,
                    )
                    skill_evidence = [first_skill, second_skill]
                    evidence = {
                        "selected_order": copy.deepcopy(
                            conditioned_path["order"]
                        ),
                        "selected_conditioned_path_id": conditioned_path[
                            "conditioned_path_id"
                        ],
                        "first_plan_authored_from_core_digest": core[
                            "content_digest"
                        ],
                        "second_plan_authored_from_core_digest": intermediate[
                            "content_digest"
                        ],
                        "skill_reuse": skill_evidence,
                        "first_replay": first_replay,
                        "second_replay": second_replay,
                        "conditioned_delta": candidate_delta,
                        "sequence": sequence,
                        "nontriviality_certificates": [
                            first_nontriviality,
                            second_nontriviality,
                        ],
                    }
                    if conditioned_path["status"] != "completed":
                        reasons.extend(conditioned_path["quarantine_reasons"])
                    if not candidate_delta["exact_intermediate_boundary"]:
                        reasons.append("second_stage_not_conditioned_on_intermediate")
                    if not sequence["finite_handback"][
                        "eligible_for_precommitted_rule_replay"
                    ]:
                        reasons.append(
                            "sequence_not_eligible_for_precommitted_rule_replay"
                        )
                    if any(
                        row["physically_inert_completion"]
                        for row in (first_nontriviality, second_nontriviality)
                    ):
                        reasons.append("nontriviality_predicate_failed")
                    status = "completed" if not reasons else "quarantined"
                    witness = conditioned_path["witness_differences"]
                    changed_burdens = list(witness["burden_statements"])
                    changed_resource = (
                        "The second conceptual transformation was authored only "
                        "after exact validation of the first transformed core."
                    )
                    unification_links = [
                        (
                            "conditioned-path:"
                            f"{conditioned_path['conditioned_path_id']}"
                        ),
                        f"intermediate-core:{intermediate['content_digest']}",
                    ]
                    records = []
                    for plan, delta in (
                        (first_plan, first_delta),
                        (second_plan, second_delta),
                    ):
                        kind = plan["relation_hypothesis"]["relation_kind"]
                        records.append(
                            {
                                "task_id": plan["transformation_id"],
                                "category_check": (
                                    {
                                        "relation_kind": kind,
                                        "mismatch_elements": [],
                                    }
                                    if _lens_for_plan(plan) == "categorical"
                                    else None
                                ),
                                "hott_check": (
                                    {
                                        "relation_kind": kind,
                                        "boundary_materialization_status": (
                                            "replayed_finite_level_one_boundaries"
                                        ),
                                        "round_trip_holds": True,
                                        "finite_scope": copy.deepcopy(
                                            plan["finite_scope"]
                                        ),
                                    }
                                    if _lens_for_plan(plan) == "hott"
                                    else None
                                ),
                                "semantic_delta": delta,
                            }
                        )
    except (FormalConceptTransformationError, FormalReasoningError) as exc:
        status = "quarantined"
        reasons.append(getattr(exc, "reason_code", type(exc).__name__))

    if not records:
        records = [
            {
                "task_id": stable_identifier(
                    "unavailable-postcommit-author-v3", route_id, core["content_digest"]
                ),
                "category_check": None,
                "hott_check": None,
                "semantic_delta": None,
            }
        ]
    handback = _shared_handback(
        route_id=route_id,
        payload=committed,
        status=status,
        evidence=evidence,
        changed_burdens=changed_burdens,
        changed_resource=changed_resource,
        unification_links=unification_links,
        quarantine_reasons=reasons,
        candidate_delta=candidate_delta,
        skill_evidence=skill_evidence,
    )
    return {
        "output_kind": "formal_lens",
        "schema_version": SCHEMA_VERSION,
        "route_id": route_id,
        "producer_binding": producer_binding,
        "producer_authorship_stage": "post_verified_commit",
        "caller_plan_used": False,
        "committed_input_sha256": commission["committed_input_sha256"],
        "committed_input_byte_length": commission["committed_input_byte_length"],
        "committed_input_content_digest": committed["content_digest"],
        "route_status": status,
        "evidence": evidence,
        "physics_handback": handback,
        "records": records,
        "formal_execution": _formal_execution(records),
        "authority_boundary": copy.deepcopy(_OUTPUT_AUTHORITY),
    }


def _blind_adjudication_rule(
    committed_rule: Mapping[str, Any],
) -> dict[str, Any]:
    """Return the exact judge rule frozen inside the committed comparison rule."""

    validated = validate_adjudication_rule(committed_rule)
    return copy.deepcopy(validated["judge_rule"])


def _blind_criterion_ledger(content: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Project exact typed statuses to digest-only judge evidence rows."""

    rows = content.get("criterion_evidence")
    if not isinstance(rows, list) or [row.get("criterion") for row in rows] != list(
        ADJUDICATION_CRITERIA
    ):
        _fail("blind candidate lacks the exact ordered criterion-evidence ledger")
    ledger: list[dict[str, Any]] = []
    for row in rows:
        if (
            set(row)
            != {
                "criterion",
                "status",
                "evidence_refs",
                "counterevidence_refs",
                "method_or_vocabulary_bonus",
                "conceptual_merit_authorized",
            }
            or row["status"] not in {"failed", "partial", "satisfied"}
            or row["method_or_vocabulary_bonus"] is not False
            or row["conceptual_merit_authorized"] is not False
            or not isinstance(row["evidence_refs"], list)
            or not isinstance(row["counterevidence_refs"], list)
        ):
            _fail("blind criterion evidence is incomplete or method-biased")
        status = row["status"]
        if (
            status == "satisfied"
            and (not row["evidence_refs"] or row["counterevidence_refs"])
        ) or (
            status == "failed"
            and (row["evidence_refs"] or not row["counterevidence_refs"])
        ) or (
            status == "partial"
            and (not row["evidence_refs"] or not row["counterevidence_refs"])
        ):
            _fail("blind criterion evidence polarity does not match its status")
        support_digest = (
            canonical_digest(
                {
                    "criterion": row["criterion"],
                    "polarity": "support",
                    "refs": row["evidence_refs"],
                }
            )
            if status in {"partial", "satisfied"}
            else None
        )
        counterevidence_digest = (
            canonical_digest(
                {
                    "criterion": row["criterion"],
                    "polarity": "counterevidence",
                    "refs": row["counterevidence_refs"],
                }
            )
            if status in {"failed", "partial"}
            else None
        )
        criterion_row = {
            "criterion": row["criterion"],
            "status": status,
            "support_digest": support_digest,
            "counterevidence_digest": counterevidence_digest,
        }
        ledger.append(
            {**criterion_row, "criterion_digest": canonical_digest(criterion_row)}
        )
    return ledger


def _blind_candidate(
    opaque_candidate_nonce: str, content: Mapping[str, Any]
) -> dict[str, Any]:
    ledger = _blind_criterion_ledger(content)
    return {
        "opaque_candidate_nonce": opaque_candidate_nonce,
        "criterion_evidence_ledger": ledger,
        "evidence_ledger_digest": canonical_digest(ledger),
    }


def _new_opaque_nonces(count: int) -> list[str]:
    """Generate unique system-random nonces independent of candidate material."""

    nonces: list[str] = []
    seen: set[str] = set()
    while len(nonces) < count:
        nonce = secrets.token_hex(32)
        if nonce not in seen:
            seen.add(nonce)
            nonces.append(nonce)
    return nonces


def _validate_and_execute_blind_request(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Replay through the separated implementation without importing it in authors."""

    from agentic.discovery.blind_conceptual_judge_v3 import (
        execute_blind_conceptual_judgment,
        validate_judgment_request,
    )

    request = validate_judgment_request(raw)
    return execute_blind_conceptual_judgment(request)


def _route_payload(commission: Mapping[str, Any], route_id: str) -> dict[str, Any]:
    return _seal(
        {
            "schema_version": SCHEMA_VERSION,
            "route_id": route_id,
            "commission": copy.deepcopy(dict(commission)),
        },
        "payload_digest",
    )


def _write_immutable_json(path: Path, payload: Mapping[str, Any]) -> None:
    data = canonical_json(payload) + b"\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.is_symlink() or not path.is_file() or path.read_bytes() != data:
            _fail(f"immutable central route artifact collision at {path}")
        return
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.stage-"
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary_path, path)
        except FileExistsError:
            if path.is_symlink() or not path.is_file() or path.read_bytes() != data:
                _fail(f"immutable central route artifact collision at {path}")
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


@contextmanager
def _exclusive_bundle_lock(bundle: Path):
    """Serialize one commission bundle while final files remain immutable."""

    lock_path = contained_path(bundle, ".central-conceptual-route.lock")
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(lock_path, flags, 0o600)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _json_artifact_reference(
    *, bundle: Path, path: Path, payload: Mapping[str, Any]
) -> dict[str, Any]:
    data = canonical_json(payload) + b"\n"
    try:
        relative_path = path.resolve().relative_to(bundle.resolve()).as_posix()
    except ValueError as exc:
        _fail(f"central route JSON artifact escapes its bundle: {exc}")
    if path.is_symlink() or not path.is_file() or path.read_bytes() != data:
        _fail("central route JSON artifact is absent or not exact canonical bytes")
    return {
        "relative_path": relative_path,
        "file_sha256": bytes_digest(data),
        "byte_length": len(data),
        "payload_digest": canonical_digest(payload),
    }


def _load_json_artifact(
    bundle: Path, reference: Mapping[str, Any], *, label: str
) -> dict[str, Any]:
    path = contained_path(bundle, *PurePosixPath(reference["relative_path"]).parts)
    if path.is_symlink() or not path.is_file():
        _fail(f"{label} immutable reference is unavailable")
    data = path.read_bytes()
    if (
        bytes_digest(data) != reference["file_sha256"]
        or len(data) != reference["byte_length"]
    ):
        _fail(f"{label} immutable file bytes differ from their reference")
    try:
        raw = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail(f"{label} immutable file is not JSON: {exc}")
    if (
        not isinstance(raw, dict)
        or data != canonical_json(raw) + b"\n"
        or canonical_digest(raw) != reference["payload_digest"]
    ):
        _fail(f"{label} immutable payload is noncanonical or substituted")
    return raw


def _validate_blind_freeze(
    raw: Mapping[str, Any],
    *,
    commission_digest: str,
    barrier_digest: str,
    committed_rule: Mapping[str, Any],
    admissible_outputs: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    freeze = copy.deepcopy(
        dict(
            _strict(
                raw,
                {
                    "schema_version",
                    "freeze_id",
                    "commission_digest",
                    "barrier_digest",
                    "judge_rule_digest",
                    "nonce_policy",
                    "request",
                    "bindings",
                    "content_digest",
                },
                "blind binding/request freeze",
            )
        )
    )
    _validate_self_digest(freeze, "content_digest", "blind binding/request freeze")
    judge_rule = _blind_adjudication_rule(committed_rule)
    expected_routes = [
        route_id for route_id in ROUTE_ORDER if route_id in admissible_outputs
    ]
    if (
        freeze["schema_version"] != SCHEMA_VERSION
        or freeze["commission_digest"] != commission_digest
        or freeze["barrier_digest"] != barrier_digest
        or freeze["judge_rule_digest"] != judge_rule["rule_digest"]
        or freeze["nonce_policy"] != _BLIND_NONCE_POLICY
    ):
        _fail("blind binding/request freeze identity or nonce policy drift")
    bindings = freeze["bindings"]
    if (
        not isinstance(bindings, list)
        or [row.get("route_id") for row in bindings] != expected_routes
        or len({row.get("opaque_candidate_nonce") for row in bindings})
        != len(bindings)
    ):
        _fail("blind binding/request freeze route or nonce set drift")
    expected_candidates: list[dict[str, Any]] = []
    for binding in bindings:
        if not isinstance(binding, Mapping) or set(binding) != {
            "opaque_candidate_nonce",
            "route_id",
            "content_digest",
            "handback_digest",
            "evidence_ledger_digest",
        }:
            _fail("blind binding/request freeze binding shape drift")
        output = admissible_outputs[binding["route_id"]]
        handback = output["physics_handback"]
        content = handback["content_projection"]
        candidate = _blind_candidate(binding["opaque_candidate_nonce"], content)
        if (
            binding["content_digest"] != canonical_digest(content)
            or binding["handback_digest"] != handback["handback_digest"]
            or binding["evidence_ledger_digest"]
            != candidate["evidence_ledger_digest"]
        ):
            _fail("blind binding/request freeze is detached from an exact handback")
        expected_candidates.append(candidate)
    expected_candidates.sort(key=lambda row: row["opaque_candidate_nonce"])
    request = freeze["request"]
    expected_request = {
        "schema_version": SCHEMA_VERSION,
        "commission_digest": commission_digest,
        "adjudication_rule": judge_rule,
        "opaque_candidates": expected_candidates,
    }
    expected_request["request_digest"] = canonical_digest(expected_request)
    if request != expected_request:
        _fail("blind binding/request freeze does not contain the exact rebuilt request")
    _validate_and_execute_blind_request(request)
    expected_freeze_id = stable_identifier(
        "central-conceptual-blind-freeze-v3",
        commission_digest,
        barrier_digest,
        request["request_digest"],
        bindings,
    )
    if freeze["freeze_id"] != expected_freeze_id:
        _fail("blind binding/request freeze ID is not content-derived")
    return freeze


def _freeze_or_reopen_blind_request(
    *,
    bundle: Path,
    commission_digest: str,
    barrier_digest: str,
    committed_rule: Mapping[str, Any],
    admissible_outputs: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    path = contained_path(bundle, "blind-binding-request-freeze-v3.json")
    if path.exists():
        provisional = {
            "relative_path": "blind-binding-request-freeze-v3.json",
            "file_sha256": bytes_digest(path.read_bytes()),
            "byte_length": len(path.read_bytes()),
            "payload_digest": canonical_digest(json.loads(path.read_bytes())),
        }
        freeze = _load_json_artifact(bundle, provisional, label="blind freeze")
        validated = _validate_blind_freeze(
            freeze,
            commission_digest=commission_digest,
            barrier_digest=barrier_digest,
            committed_rule=committed_rule,
            admissible_outputs=admissible_outputs,
        )
        return validated, _json_artifact_reference(
            bundle=bundle, path=path, payload=validated
        )
    route_ids = [
        route_id for route_id in ROUTE_ORDER if route_id in admissible_outputs
    ]
    nonces = _new_opaque_nonces(len(route_ids))
    bindings: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    for route_id, nonce in zip(route_ids, nonces, strict=True):
        handback = admissible_outputs[route_id]["physics_handback"]
        content = handback["content_projection"]
        candidate = _blind_candidate(nonce, content)
        candidates.append(candidate)
        bindings.append(
            {
                "opaque_candidate_nonce": nonce,
                "route_id": route_id,
                "content_digest": canonical_digest(content),
                "handback_digest": handback["handback_digest"],
                "evidence_ledger_digest": candidate["evidence_ledger_digest"],
            }
        )
    candidates.sort(key=lambda row: row["opaque_candidate_nonce"])
    judge_rule = _blind_adjudication_rule(committed_rule)
    request = {
        "schema_version": SCHEMA_VERSION,
        "commission_digest": commission_digest,
        "adjudication_rule": judge_rule,
        "opaque_candidates": candidates,
    }
    request["request_digest"] = canonical_digest(request)
    material = {
        "schema_version": SCHEMA_VERSION,
        "freeze_id": stable_identifier(
            "central-conceptual-blind-freeze-v3",
            commission_digest,
            barrier_digest,
            request["request_digest"],
            bindings,
        ),
        "commission_digest": commission_digest,
        "barrier_digest": barrier_digest,
        "judge_rule_digest": judge_rule["rule_digest"],
        "nonce_policy": copy.deepcopy(_BLIND_NONCE_POLICY),
        "request": request,
        "bindings": bindings,
    }
    freeze = {**material, "content_digest": canonical_digest(material)}
    validated = _validate_blind_freeze(
        freeze,
        commission_digest=commission_digest,
        barrier_digest=barrier_digest,
        committed_rule=committed_rule,
        admissible_outputs=admissible_outputs,
    )
    _write_immutable_json(path, validated)
    reopened = _load_json_artifact(
        bundle,
        _json_artifact_reference(bundle=bundle, path=path, payload=validated),
        label="blind freeze",
    )
    return _validate_blind_freeze(
        reopened,
        commission_digest=commission_digest,
        barrier_digest=barrier_digest,
        committed_rule=committed_rule,
        admissible_outputs=admissible_outputs,
    ), _json_artifact_reference(bundle=bundle, path=path, payload=reopened)


def _parse_time(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        _fail(f"worker event timestamp is invalid: {exc}")
    raise AssertionError("unreachable")


def _terminal(route_id: str, receipt: Mapping[str, Any]) -> dict[str, Any]:
    event = receipt["process_event"]
    accepted = receipt["outcome_status"] == "accepted"
    output = (
        receipt["response_payload"]["output"]
        if accepted and isinstance(receipt.get("response_payload"), Mapping)
        else None
    )
    return _seal(
        {
            "terminal_id": stable_identifier(
                "central-conceptual-route-terminal-v3",
                route_id,
                receipt["content_digest"],
            ),
            "route_id": route_id,
            "terminal_status": (
                "failed"
                if not accepted
                else "completed"
                if output["route_status"] == "completed"
                else "quarantined_or_unavailable"
            ),
            "worker_receipt_id": receipt["receipt_id"],
            "worker_receipt_digest": receipt["content_digest"],
            "process_id": event["pid"],
            "process_started_at": event["started_at"],
            "process_completed_at": event["completed_at"],
            "process_status": receipt["process_status"],
            "descendant_leak_detected": event["descendant_leak_detected"],
            "stdout_drain_incomplete": event["stdout_drain_incomplete"],
            "stderr_drain_incomplete": event["stderr_drain_incomplete"],
            "failure": copy.deepcopy(receipt["failure"]),
        },
        "terminal_digest",
    )


def _terminal_barrier(
    commission: Mapping[str, Any], terminals: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    pids = [row["process_id"] for row in terminals]
    distinct = len(terminals) == 5 and all(
        isinstance(pid, int) and pid > 0 for pid in pids
    ) and len(set(pids)) == 5
    overlap = False
    if distinct:
        overlap = max(_parse_time(row["process_started_at"]) for row in terminals) < min(
            _parse_time(row["process_completed_at"]) for row in terminals
        )
    all_terminal = len(terminals) == 5 and all(
        row["terminal_status"] in {"completed", "quarantined_or_unavailable", "failed"}
        and not row["descendant_leak_detected"]
        and not row["stdout_drain_incomplete"]
        and not row["stderr_drain_incomplete"]
        for row in terminals
    )
    return _seal(
        {
            "barrier_id": stable_identifier(
                "central-conceptual-terminal-barrier-v3",
                commission["commission_digest"],
                [row["terminal_digest"] for row in terminals],
            ),
            "expected_routes": list(ROUTE_ORDER),
            "all_routes_terminal": all_terminal,
            "all_routes_started_as_distinct_processes": distinct,
            "parallel_process_overlap_observed": overlap,
            "identical_committed_input_bytes": True,
            "equal_resource_budgets": True,
            "collected_after_all_process_futures_terminal": True,
            "late_outputs_admissible": False,
            "terminal_digests": [row["terminal_digest"] for row in terminals],
        },
        "barrier_digest",
    )


def _approved_dependencies(
    registry: Mapping[str, Any], descriptor_field: str
) -> list[Path]:
    # ResearchWorkerAdapter adds these five paths itself.  Passing any of them
    # again would create a duplicate approved descriptor and make the command
    # authority ambiguous (`approved` versus `argv+approved`).  They remain in
    # the registry binding and command authority; this filter removes only the
    # duplicate adapter argument.
    adapter_owned = {
        "agentic/discovery/research_worker_isolation.py",
        "agentic/discovery/budgets.py",
        "agentic/discovery/contracts.py",
        "agentic/discovery/benchmark_process.py",
        "agentic/spec/research_worker_execution_receipt.schema.json",
    }
    return [
        ROOT.joinpath(*PurePosixPath(row["path"]).parts)
        for row in registry[descriptor_field]
        if row["path"] not in adapter_owned
    ]


def _reopen_receipt_summary(
    *, bundle: Path, study_id: str, summary: Mapping[str, Any]
) -> dict[str, Any]:
    path = contained_path(
        bundle,
        "processes",
        study_id,
        *PurePosixPath(summary["receipt_ref"]).parts,
    )
    try:
        if path.is_symlink() or not path.is_file():
            _fail("immutable research-worker receipt reference is unavailable")
        receipt = validate_research_worker_receipt(
            json.loads(path.read_bytes()), receipt_path=path
        )
        if receipt_summary(receipt, receipt_path=path) != summary:
            _fail("research-worker receipt summary does not replay exactly")
    except (OSError, json.JSONDecodeError, ResearchWorkerIntegrityError) as exc:
        _fail(f"research-worker receipt replay failed: {exc}")
    return receipt


def _conditioned_order_comparison(
    outputs: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Compare two independently conditioned orders without ranking either."""

    forward = outputs.get("category_then_hott")
    reverse = outputs.get("hott_then_category")
    forward_delta = (
        forward.get("evidence", {}).get("conditioned_delta")
        if isinstance(forward, Mapping)
        and isinstance(forward.get("evidence"), Mapping)
        else None
    )
    reverse_delta = (
        reverse.get("evidence", {}).get("conditioned_delta")
        if isinstance(reverse, Mapping)
        and isinstance(reverse.get("evidence"), Mapping)
        else None
    )
    available = all(
        isinstance(item, Mapping)
        for item in (forward, reverse, forward_delta, reverse_delta)
    )
    independent = bool(
        available
        and forward_delta.get("route_id") == "category_then_hott"
        and reverse_delta.get("route_id") == "hott_then_category"
        and forward_delta.get("first_plan_authored_from_core_digest")
        == forward_delta.get("before_core", {}).get("content_digest")
        and reverse_delta.get("first_plan_authored_from_core_digest")
        == reverse_delta.get("before_core", {}).get("content_digest")
        and forward_delta.get("second_plan_authored_from_core_digest")
        == forward_delta.get("first_delta", {})
        .get("after_core", {})
        .get("content_digest")
        and reverse_delta.get("second_plan_authored_from_core_digest")
        == reverse_delta.get("first_delta", {})
        .get("after_core", {})
        .get("content_digest")
        and forward_delta.get("exact_intermediate_boundary") is True
        and reverse_delta.get("exact_intermediate_boundary") is True
    )
    forward_order = (
        [
            _lens_for_plan(forward_delta["first_plan"]),
            _lens_for_plan(forward_delta["second_plan"]),
        ]
        if available
        else []
    )
    reverse_order = (
        [
            _lens_for_plan(reverse_delta["first_plan"]),
            _lens_for_plan(reverse_delta["second_plan"]),
        ]
        if available
        else []
    )
    asymmetric = (
        forward_order == ["categorical", "hott"]
        and reverse_order == ["hott", "categorical"]
    )
    forward_after = (
        forward_delta.get("after_core", {}).get("content_digest")
        if available
        else None
    )
    reverse_after = (
        reverse_delta.get("after_core", {}).get("content_digest")
        if available
        else None
    )
    strictly_distinct = bool(
        forward_after and reverse_after and forward_after != reverse_after
    )
    if available:
        try:
            isomorphism_comparison = compare_conceptual_cores(
                forward_delta["after_core"],
                reverse_delta["after_core"],
                max_permutations=DEFAULT_MAX_ISOMORPHISM_PERMUTATIONS,
            )
        except (
            FormalConceptTransformationError,
            KeyError,
            TypeError,
            ValueError,
        ):
            isomorphism_comparison = unavailable_core_comparison(
                max_permutations=DEFAULT_MAX_ISOMORPHISM_PERMUTATIONS,
                reason_code="conditioned_final_core_replay_failed",
            )
    else:
        isomorphism_comparison = unavailable_core_comparison(
            max_permutations=DEFAULT_MAX_ISOMORPHISM_PERMUTATIONS,
            reason_code="conditioned_order_outputs_unavailable",
        )
    isomorphism_status = isomorphism_comparison["comparison_status"]
    comparison_kind = {
        "strictly_equal": "strictly_equal",
        "isomorphic": "isomorphic_commuting",
        "not_isomorphic": "productive_noncommutation",
        "ceiling_unavailable": "ceiling_unavailable",
        "not_available": "unavailable",
    }[isomorphism_status]
    both_admissible = bool(
        available
        and forward["physics_handback"]["handback_status"]
        == "admissible_for_blind_comparison"
        and reverse["physics_handback"]["handback_status"]
        == "admissible_for_blind_comparison"
    )
    material = {
        "comparison_status": "compared" if available else "unavailable",
        "forward_route_id": (
            "category_then_hott" if available else None
        ),
        "reverse_route_id": "hott_then_category" if available else None,
        "forward_delta_digest": (
            forward_delta.get("content_digest") if available else None
        ),
        "reverse_delta_digest": (
            reverse_delta.get("content_digest") if available else None
        ),
        "forward_order": forward_order,
        "reverse_order": reverse_order,
        "independently_conditioned": independent,
        "asymmetric_order_replayed": asymmetric,
        "strict_after_core_difference": strictly_distinct,
        "isomorphism_aware": True,
        "isomorphism_comparison": isomorphism_comparison,
        "comparison_kind": comparison_kind,
        "productive_noncommutation_retained": (
            independent
            and asymmetric
            and isomorphism_status == "not_isomorphic"
            and both_admissible
        ),
        "isomorphism_scope": (
            "bounded_exact_internal_relabelling_via_formal_concept_sequence_algebra"
        ),
        "comparative_value_authorized": False,
        "physics_gain_authorized": False,
        "category_hott_advantage_authorized": False,
    }
    return {**material, "comparison_digest": canonical_digest(material)}


def decode_central_conceptual_route_packet(raw: Any) -> dict[str, Any]:
    """Decode self-contained structure only; this grants no bundle authority."""

    packet = copy.deepcopy(dict(raw)) if isinstance(raw, Mapping) else {}
    try:
        validate_instance(packet, "central_conceptual_route_packet_v3.schema.json")
    except ContractError as exc:
        _fail(f"central conceptual route packet schema failure: {exc}")
    _validate_self_digest(packet, "content_digest", "central conceptual route packet")
    terminals = packet["route_terminals"]
    if [row["route_id"] for row in terminals] != list(ROUTE_ORDER):
        _fail("central conceptual route terminals are not in exact route order")
    for row in terminals:
        _validate_self_digest(row, "terminal_digest", "central route terminal")
    barrier = packet["terminal_barrier"]
    _validate_self_digest(barrier, "barrier_digest", "central route terminal barrier")
    if barrier["terminal_digests"] != [row["terminal_digest"] for row in terminals]:
        _fail("terminal barrier does not bind the exact ordered terminals")
    outputs = packet["route_outputs"]
    route_summaries = packet["route_receipt_summaries"]
    if [row["route_id"] for row in route_summaries] != list(ROUTE_ORDER):
        _fail("central route receipt summaries are not in exact route order")
    for route_id, output in zip(ROUTE_ORDER, outputs, strict=True):
        terminal = terminals[ROUTE_ORDER.index(route_id)]
        summary = route_summaries[ROUTE_ORDER.index(route_id)]["summary"]
        if (
            summary["receipt_id"] != terminal["worker_receipt_id"]
            or summary["receipt_digest"] != terminal["worker_receipt_digest"]
            or summary["receipt_digest"]
            != packet["route_receipt_digests"][ROUTE_ORDER.index(route_id)]
        ):
            _fail("route receipt summary is detached from its terminal")
        if output is None:
            if terminal["terminal_status"] != "failed":
                _fail("a nonfailed route is missing its output")
            continue
        if output["route_id"] != route_id:
            _fail("central route output order or identity drift")
        handback = output["physics_handback"]
        if handback["route_id"] != route_id:
            _fail("physics handback is detached from its route output")
        _validate_self_digest(handback, "handback_digest", "central route physics handback")
        if terminal["terminal_status"] == "failed":
            _fail("a failed route cannot carry an accepted output")
    admissible_outputs = {
        output["route_id"]: output
        for output in outputs
        if output is not None
        and output["physics_handback"]["handback_status"]
        == "admissible_for_blind_comparison"
    }
    expected_order_comparison = _conditioned_order_comparison(
        {
            output["route_id"]: output
            for output in outputs
            if output is not None
        }
    )
    if packet["conditioned_order_comparison"] != expected_order_comparison:
        _fail("conditioned Category/HoTT order comparison does not replay")
    if packet["blind_candidate_count"] != len(admissible_outputs):
        _fail("blind candidate count differs from exact admissible handbacks")
    bindings = packet["blind_identity_rebindings"]
    if len({row["opaque_candidate_nonce"] for row in bindings}) != len(bindings):
        _fail("blind identity rebindings repeat an opaque candidate")
    request = packet["blind_judge_request"]
    for binding in bindings:
        route_id = binding["route_id"]
        output = admissible_outputs.get(route_id)
        handback = output["physics_handback"] if output is not None else None
        candidate = (
            _blind_candidate(
                binding["opaque_candidate_nonce"], handback["content_projection"]
            )
            if handback is not None
            else None
        )
        if handback is None or (
            binding["handback_digest"] != handback["handback_digest"]
            or binding["content_digest"]
            != canonical_digest(handback["content_projection"])
            or binding["evidence_ledger_digest"]
            != candidate["evidence_ledger_digest"]
        ):
            _fail("blind identity rebinds a missing or substituted handback")
    judgment = packet["blind_judgment"]
    selected_routes = packet["selected_route_set"]
    if judgment is None:
        if (
            request is not None
            or bindings
            or selected_routes
            or packet["blind_binding_record_reference"] is not None
            or packet["blind_binding_record_digest"] is not None
            or packet["blind_judge_receipt_digest"] is not None
            or packet["blind_judge_receipt_summary"] is not None
        ):
            _fail("route selection exists without a blind judge receipt")
    else:
        if (
            request is None
            or packet["blind_binding_record_reference"] is None
            or packet["blind_binding_record_digest"] is None
            or packet["blind_judge_receipt_digest"] is None
            or packet["blind_judge_receipt_summary"] is None
            or [row["route_id"] for row in bindings]
            != [route_id for route_id in ROUTE_ORDER if route_id in admissible_outputs]
        ):
            _fail("adjudicated packet lacks its complete post-judge binding evidence")
        expected_candidates = sorted(
            [
                _blind_candidate(
                    row["opaque_candidate_nonce"],
                    admissible_outputs[row["route_id"]]["physics_handback"][
                        "content_projection"
                    ],
                )
                for row in bindings
            ],
            key=lambda row: row["opaque_candidate_nonce"],
        )
        if request["opaque_candidates"] != expected_candidates:
            _fail("blind judge request is not the exact reconstructed evidence ledger")
        expected_judgment = _validate_and_execute_blind_request(request)
        if judgment != expected_judgment:
            _fail("blind judgment differs from exact local deterministic replay")
        by_opaque = {
            row["opaque_candidate_nonce"]: row["route_id"] for row in bindings
        }
        try:
            selected = {by_opaque[value] for value in judgment["preference_set"]}
        except KeyError as exc:
            _fail(f"blind judge selected an unbound opaque candidate: {exc}")
        expected_routes = [route_id for route_id in ROUTE_ORDER if route_id in selected]
        if expected_routes != selected_routes:
            _fail("selected route set differs from post-judge opaque rebindings")
        if (
            packet["blind_judge_receipt_summary"]["receipt_digest"]
            != packet["blind_judge_receipt_digest"]
        ):
            _fail("blind judge receipt digest and summary differ")
    expected_packet_id = stable_identifier(
        "central-conceptual-route-packet-v3",
        packet["commission_digest"],
        barrier["barrier_digest"],
        packet["conditioned_order_comparison"]["comparison_digest"],
        request["request_digest"] if request is not None else None,
        packet["blind_binding_record_digest"],
        packet["blind_judge_receipt_summary"],
        judgment,
    )
    if packet["packet_id"] != expected_packet_id:
        _fail("central conceptual route packet ID is not content-derived")
    return packet


def _reopen_authoritative_central_conceptual_route_packet(
    raw: Any,
    *,
    bundle_root: Path | str,
    store: DiscoveryTransactionStore,
    temporal: _CentralRouteTemporalCapability,
    boundary: str,
    require_current_head: bool = True,
) -> dict[str, Any]:
    """Reopen every immutable artifact plus the still-current theory authority."""

    packet = decode_central_conceptual_route_packet(raw)
    bundle = Path(bundle_root).resolve()
    commission = _load_json_artifact(
        bundle, packet["commission_artifact_reference"], label="commission"
    )
    if (
        commission["commission_id"] != packet["commission_id"]
        or commission["commission_digest"] != packet["commission_digest"]
        or commission["verified_commit"] != packet["verified_commit"]
        or commission["committed_input_descriptor"]
        != packet["committed_input_descriptor"]
        or commission["registry_binding"]["binding_digest"]
        != packet["registry_binding_digest"]
    ):
        _fail("persisted commission differs from the packet commission")
    outputs = packet["route_outputs"]
    for route_id, summary_row, output in zip(
        ROUTE_ORDER, packet["route_receipt_summaries"], outputs, strict=True
    ):
        receipt = _reopen_receipt_summary(
            bundle=bundle,
            study_id="central-formal-conceptual-routes-v3",
            summary=summary_row["summary"],
        )
        if (
            receipt["request_payload"]["invocation_context"]
            != {
                "commission_id": commission["commission_id"],
                "commission_digest": commission["commission_digest"],
                "route_id": route_id,
            }
            or receipt["request_payload"]["payload"]
            != _route_payload(commission, route_id)
            or receipt["request_payload"]["fault_mode"]
            != commission["route_fault_modes"][route_id]
            or (
                receipt["response_payload"]["output"]
                if receipt["outcome_status"] == "accepted"
                else None
            )
            != output
        ):
            _fail("persisted route receipt request/output does not replay")
    judgment = packet["blind_judgment"]
    if judgment is not None:
        admissible_outputs = {
            output["route_id"]: output
            for output in outputs
            if output is not None
            and output["physics_handback"]["handback_status"]
            == "admissible_for_blind_comparison"
        }
        freeze = _load_json_artifact(
            bundle,
            packet["blind_binding_record_reference"],
            label="blind binding/request freeze",
        )
        committed = _decode_committed_input(commission)
        freeze = _validate_blind_freeze(
            freeze,
            commission_digest=commission["commission_digest"],
            barrier_digest=packet["terminal_barrier"]["barrier_digest"],
            committed_rule=committed["adjudication_rule"],
            admissible_outputs=admissible_outputs,
        )
        if (
            freeze["content_digest"] != packet["blind_binding_record_digest"]
            or freeze["request"] != packet["blind_judge_request"]
            or freeze["bindings"] != packet["blind_identity_rebindings"]
        ):
            _fail("persisted blind freeze differs from post-judge packet bindings")
        judge_receipt = _reopen_receipt_summary(
            bundle=bundle,
            study_id="blind-conceptual-judge-v3",
            summary=packet["blind_judge_receipt_summary"],
        )
        if (
            judge_receipt["study_id"] != "blind-conceptual-judge-v3"
            or judge_receipt["request_payload"]["invocation_context"]
            != {"commission_digest": commission["commission_digest"]}
            or judge_receipt["request_payload"]["payload"]
            != packet["blind_judge_request"]
            or judge_receipt["response_payload"]["output"] != judgment
        ):
            _fail("persisted blind judge receipt request/output does not replay")
    _revalidate_live_commission(
        store=store,
        commission=commission,
        temporal=temporal,
        boundary=boundary,
        require_current_head=require_current_head,
    )
    return packet


def reopen_authoritative_central_conceptual_route_packet(
    raw: Any,
    *,
    bundle_root: Path | str,
    store: DiscoveryTransactionStore,
) -> dict[str, Any]:
    """Return authority only after bundle, receipts, head, and lease reopening."""

    return _reopen_authoritative_central_conceptual_route_packet(
        raw,
        bundle_root=bundle_root,
        store=store,
        temporal=_CentralRouteTemporalCapability.issue(),
        boundary="authoritative_reopen",
    )


def reopen_active_prefix_central_conceptual_route_packet(
    raw: Any,
    *,
    bundle_root: Path | str,
    store: DiscoveryTransactionStore,
) -> dict[str, Any]:
    """Reopen a completed route bundle from an exact verified ancestor.

    This consumer-only surface differs from the current-head authoring surface:
    it permits later committed descendants while still reopening every route
    and judge receipt, the exact source commit, registry dependencies, and the
    unexpired literature lease.  It never licenses another authoring wave.
    """

    return _reopen_authoritative_central_conceptual_route_packet(
        raw,
        bundle_root=bundle_root,
        store=store,
        temporal=_CentralRouteTemporalCapability.issue(),
        boundary="authoritative_active_prefix_reopen",
        require_current_head=False,
    )


def run_central_conceptual_routes(
    *,
    store: DiscoveryTransactionStore,
    verified_commit: VerifiedCommit,
    committed_input_path: str,
    output_root: Path | str,
    worker_budget: Mapping[str, Any] | None = None,
    route_fault_modes: Mapping[str, str | None] | None = None,
    persistence_failpoint: str | None = None,
) -> dict[str, Any]:
    """Run five matched authors in parallel, then one content-only blind judge."""

    temporal = _CentralRouteTemporalCapability.issue()
    commission = commission_from_verified_commit(
        store=store,
        verified_commit=verified_commit,
        committed_input_path=committed_input_path,
        worker_budget=worker_budget,
    )
    faults = (
        {route_id: None for route_id in ROUTE_ORDER}
        if route_fault_modes is None
        else dict(route_fault_modes)
    )
    if set(faults) != set(ROUTE_ORDER) or any(
        value not in {None, "exit_nonzero", "invalid_json", "hang"}
        for value in faults.values()
    ):
        _fail("route fault modes must cover the exact five routes")
    if persistence_failpoint not in {
        None,
        "after_commission_before_authors",
        "after_blind_freeze_before_judge",
        "after_judge_receipt_before_packet",
        "after_packet_validation_before_publish",
    }:
        _fail("unknown central conceptual route persistence failpoint")
    commission = copy.deepcopy(commission)
    base_commission_id = commission["commission_id"]
    commission.pop("commission_digest")
    commission["commission_id"] = stable_identifier(
        "central-conceptual-route-commission-v3",
        base_commission_id,
        faults,
    )
    commission["route_fault_modes"] = faults
    commission["commission_digest"] = canonical_digest(commission)
    root = Path(output_root).resolve()
    bundle = contained_path(root, commission["commission_id"])
    bundle.mkdir(parents=True, exist_ok=True)
    with _exclusive_bundle_lock(bundle):
        _revalidate_live_commission(
            store=store,
            commission=commission,
            temporal=temporal,
            boundary="after_bundle_lock",
        )
        packet_path = contained_path(bundle, "central-conceptual-route-packet-v3.json")
        commission_path = contained_path(bundle, "commission.json")
        _write_immutable_json(commission_path, commission)
        commission_reference = _json_artifact_reference(
            bundle=bundle, path=commission_path, payload=commission
        )
        if packet_path.exists():
            try:
                data = packet_path.read_bytes()
                existing = json.loads(data)
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                _fail(f"existing central route packet is invalid: {exc}")
            if (
                not isinstance(existing, dict)
                or data != canonical_json(existing) + b"\n"
                or existing.get("commission_digest") != commission["commission_digest"]
                or existing.get("commission_artifact_reference")
                != commission_reference
            ):
                _fail("existing central route packet belongs to a different commission")
            return _reopen_authoritative_central_conceptual_route_packet(
                existing,
                bundle_root=bundle,
                store=store,
                temporal=temporal,
                boundary="before_cache_return",
            )
        if persistence_failpoint == "after_commission_before_authors":
            _fail("injected persistence fault after commission before authors")
        registry = commission["registry_binding"]
        adapter = ResearchWorkerAdapter(
            study_id="central-formal-conceptual-routes-v3",
            run_root=contained_path(bundle, "processes"),
            worker_script=ROOT / "agentic/scripts/run_central_conceptual_route_worker_v3.py",
            approved_dependency_paths=_approved_dependencies(
                registry, "route_dependency_descriptors"
            ),
            input_limit_bytes=16 * 1024 * 1024,
            stdout_limit_bytes=32 * 1024 * 1024,
            stderr_limit_bytes=512 * 1024,
        )
        route_payloads = {
            route_id: _route_payload(commission, route_id) for route_id in ROUTE_ORDER
        }

        def invoke(route_id: str) -> dict[str, Any]:
            return adapter.invoke(
                role="formal_lens",
                operation="formal_lens",
                invocation_context={
                    "commission_id": commission["commission_id"],
                    "commission_digest": commission["commission_digest"],
                    "route_id": route_id,
                },
                payload=route_payloads[route_id],
                budget=commission["worker_budget"],
                fault_mode=faults[route_id],
            )

        _revalidate_live_commission(
            store=store,
            commission=commission,
            temporal=temporal,
            boundary="before_author_launch",
        )
        with ThreadPoolExecutor(max_workers=5) as pool:
            future_by_route = {
                route_id: pool.submit(invoke, route_id) for route_id in ROUTE_ORDER
            }
            receipts = {
                route_id: future_by_route[route_id].result()
                for route_id in ROUTE_ORDER
            }
        terminals = [_terminal(route_id, receipts[route_id]) for route_id in ROUTE_ORDER]
        barrier = _terminal_barrier(commission, terminals)
        if not barrier["all_routes_terminal"]:
            _fail("five-route terminal barrier did not observe every terminal")
        outputs = {
            route_id: receipts[route_id]["response_payload"]["output"]
            for route_id in ROUTE_ORDER
            if receipts[route_id]["outcome_status"] == "accepted"
        }
        if any(
            output["committed_input_sha256"] != commission["committed_input_sha256"]
            or output["committed_input_byte_length"]
            != commission["committed_input_byte_length"]
            or output["committed_input_content_digest"]
            != commission["committed_input_content_digest"]
            or output["caller_plan_used"] is not False
            or output["producer_authorship_stage"] != "post_verified_commit"
            for output in outputs.values()
        ):
            _fail("one route did not consume the identical plan-free committed bytes")
        route_summaries = [
            {
                "route_id": route_id,
                "summary": receipt_summary(receipts[route_id]),
            }
            for route_id in ROUTE_ORDER
        ]
        admissible_outputs = {
            route_id: output
            for route_id, output in outputs.items()
            if output["physics_handback"]["handback_status"]
            == "admissible_for_blind_comparison"
        }
        matched_comparison_eligible = bool(
            barrier["all_routes_terminal"]
            and barrier["all_routes_started_as_distinct_processes"]
            and barrier["parallel_process_overlap_observed"]
            and not any(row["terminal_status"] == "failed" for row in terminals)
        )
        conditioned_order_comparison = _conditioned_order_comparison(outputs)
        judgment: dict[str, Any] | None = None
        judge_request: dict[str, Any] | None = None
        judge_receipt: dict[str, Any] | None = None
        judge_summary: dict[str, Any] | None = None
        blind_bindings: list[dict[str, Any]] = []
        freeze_reference: dict[str, Any] | None = None
        freeze_digest: str | None = None
        selected_routes: list[str] = []
        if admissible_outputs and matched_comparison_eligible:
            committed = _decode_committed_input(commission)
            freeze, freeze_reference = _freeze_or_reopen_blind_request(
                bundle=bundle,
                commission_digest=commission["commission_digest"],
                barrier_digest=barrier["barrier_digest"],
                committed_rule=committed["adjudication_rule"],
                admissible_outputs=admissible_outputs,
            )
            judge_request = copy.deepcopy(freeze["request"])
            freeze_digest = freeze["content_digest"]
            if persistence_failpoint == "after_blind_freeze_before_judge":
                _fail("injected persistence fault after blind freeze before judge")
            judge_adapter = ResearchWorkerAdapter(
                study_id=registry["judge"]["study_id"],
                run_root=contained_path(bundle, "processes"),
                worker_script=ROOT / registry["judge"]["worker_script"],
                approved_dependency_paths=_approved_dependencies(
                    registry, "judge_dependency_descriptors"
                ),
                input_limit_bytes=4 * 1024 * 1024,
                stdout_limit_bytes=4 * 1024 * 1024,
                stderr_limit_bytes=256 * 1024,
            )
            _revalidate_live_commission(
                store=store,
                commission=commission,
                temporal=temporal,
                boundary="before_judge_launch",
            )
            judge_receipt = judge_adapter.invoke(
                role="judge",
                operation="blind_judgment",
                invocation_context={
                    "commission_digest": commission["commission_digest"]
                },
                payload=judge_request,
                budget=commission["worker_budget"],
            )
            if judge_receipt["outcome_status"] != "accepted":
                _fail("blind content judge did not return an accepted terminal receipt")
            judgment = copy.deepcopy(judge_receipt["response_payload"]["output"])
            if judgment != _validate_and_execute_blind_request(judge_request):
                _fail("separated blind judge output differs from exact parent replay")
            judge_summary = receipt_summary(judge_receipt)
            if persistence_failpoint == "after_judge_receipt_before_packet":
                _fail("injected persistence fault after judge receipt before packet")
            # The durable private mapping exists before launch for crash-safe retry;
            # it becomes a public packet rebinding only after validated judgment.
            blind_bindings = copy.deepcopy(freeze["bindings"])
            route_by_nonce = {
                row["opaque_candidate_nonce"]: row["route_id"]
                for row in blind_bindings
            }
            selected = {
                route_by_nonce[nonce] for nonce in judgment["preference_set"]
            }
            selected_routes = [
                route_id for route_id in ROUTE_ORDER if route_id in selected
            ]
        packet_core = {
            "schema_version": SCHEMA_VERSION,
            "commission_id": commission["commission_id"],
            "commission_digest": commission["commission_digest"],
            "commission_artifact_reference": commission_reference,
            "verified_commit": copy.deepcopy(commission["verified_commit"]),
            "committed_input_descriptor": copy.deepcopy(
                commission["committed_input_descriptor"]
            ),
            "registry_binding_digest": registry["binding_digest"],
            "route_terminals": terminals,
            "terminal_barrier": barrier,
            "route_outputs": [
                copy.deepcopy(outputs.get(route_id)) for route_id in ROUTE_ORDER
            ],
            "route_receipt_digests": [
                receipts[route_id]["content_digest"] for route_id in ROUTE_ORDER
            ],
            "route_receipt_summaries": route_summaries,
            "conditioned_order_comparison": conditioned_order_comparison,
            "blind_candidate_count": len(admissible_outputs),
            "blind_nonce_policy": copy.deepcopy(_BLIND_NONCE_POLICY),
            "blind_judge_request": judge_request,
            "blind_binding_record_reference": freeze_reference,
            "blind_binding_record_digest": freeze_digest,
            "blind_identity_rebindings": blind_bindings,
            "blind_judgment": judgment,
            "blind_judge_receipt_digest": (
                judge_receipt["content_digest"] if judge_receipt is not None else None
            ),
            "blind_judge_receipt_summary": judge_summary,
            "selected_route_set": selected_routes,
            "selection_is_set_valued": True,
            "matched_comparison_eligible": matched_comparison_eligible,
            "capable_nonformal_structurally_eligible": True,
            "experiments": "secondary_theory_requested_falsifiers_only",
            "authority_boundary": copy.deepcopy(_OUTPUT_AUTHORITY),
        }
        packet = {
            **packet_core,
            "packet_id": stable_identifier(
                "central-conceptual-route-packet-v3",
                commission["commission_digest"],
                barrier["barrier_digest"],
                conditioned_order_comparison["comparison_digest"],
                judge_request["request_digest"] if judge_request is not None else None,
                freeze_digest,
                judge_summary,
                judgment,
            ),
        }
        packet["content_digest"] = canonical_digest(packet)
        _reopen_authoritative_central_conceptual_route_packet(
            packet,
            bundle_root=bundle,
            store=store,
            temporal=temporal,
            boundary="before_packet_publication",
        )
        if persistence_failpoint == "after_packet_validation_before_publish":
            _fail("injected persistence fault after packet validation before publish")
        _write_immutable_json(packet_path, packet)
        try:
            reopened_packet = json.loads(packet_path.read_bytes())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            _fail(f"persisted central route packet cannot be reopened: {exc}")
        return _reopen_authoritative_central_conceptual_route_packet(
            reopened_packet,
            bundle_root=bundle,
            store=store,
            temporal=temporal,
            boundary="before_cache_return",
        )


__all__ = [
    "ADJUDICATION_CRITERIA",
    "CentralConceptualRouteError",
    "ROUTE_ORDER",
    "build_committed_route_input",
    "commission_from_verified_commit",
    "decode_central_conceptual_route_packet",
    "execute_route_author_payload",
    "load_central_route_registry",
    "reopen_active_prefix_central_conceptual_route_packet",
    "reopen_authoritative_central_conceptual_route_packet",
    "run_central_conceptual_routes",
    "validate_adjudication_rule",
    "validate_committed_route_input",
    "validate_physics_decision_rule",
]
