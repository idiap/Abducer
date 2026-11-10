# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Verify a canonical theory cycle before a compatibility runtime invests.

The canonical discovery cycle and older workflow runners intentionally keep
separate transaction stores and state schemas.  This module is the narrow seam
between them: it verifies a result projection against the immutable canonical
commit, checks that current literature actually permits investment, and derives
the exact branch IDs authorized by both the canonical identity map and its
theory-first schedule.  Consumers receive an authorization record, never a
writer or an inferred operator receipt.

The verifier is reusable by the legacy marathon, the outer work-cycle runner,
and future compatibility adapters.  A projection is not trusted because it is
well shaped; every decision-bearing field is compared with bytes inside the
verified compare-and-swap commit.
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import tempfile
from collections.abc import Iterator, Mapping, Sequence
from pathlib import Path
from typing import Any

from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    file_digest,
    load_json,
    safe_relative_path,
    stable_identifier,
    validate_instance,
)
from agentic.discovery.committed_projection import (
    load_committed_cycle_literature_input,
)
from agentic.discovery.ledger import initial_state, reduce_from_state, validate_event_chain
from agentic.discovery.hypotheses import validate_high_risk_portfolio
from agentic.discovery.formal_claim_authority import (
    build_formal_claim_producer_output_with_loader,
    validate_formal_claim_producer_input_with_loader,
    validate_formal_claim_producer_output,
)
from agentic.discovery.literature import (
    resolve_present_literature_freshness,
    validate_assimilation,
    validate_snapshot,
)
from agentic.discovery.parallel import validate_parallel_portfolio
from agentic.discovery.reflection import validate_packet_invariants
from agentic.discovery.literature_production_commitment import (
    validate_portable_literature_production_input_bundle,
)
from agentic.discovery.receipts import (
    OperatorBinding,
    semantic_output_rows,
    validate_operator_receipt_identity,
    validate_operator_request_identity,
    validator_dependency_policy_is_supported,
    verify_current_validator_authority,
)
from agentic.discovery.cycle import (
    _canonical_semantic_output_rows,
    _validate_stage_causality,
    derive_conceptual_authority,
    validate_source_authority_pair_execution,
)
from agentic.discovery.scheduler import reserve_actions_transaction
from agentic.experiments import (
    experiment_output_digest,
    validate_experiment_receipt,
    validate_experiment_spec,
)
from agentic.experiments.world_matrix import WORLD_IDS
from agentic.experiments.world_matrix_commits import (
    replay_canonical_world_matrix_commit_chain,
    require_active_canonical_world_matrix_commit_chain,
)
from agentic.state.discovery_transaction import DiscoveryTransactionStore


_AGENTIC_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANONICAL_THEORY_STATE_ROOT = (
    _AGENTIC_ROOT / "state/canonical_discovery_transactions"
)
_FORBIDDEN_COMPATIBILITY_ROOTS = {
    (_AGENTIC_ROOT / "state/discovery_transactions").resolve(),
}

# These are the feedback-effective theory operators that must precede any
# legacy branch investment.  The experiment operator is deliberately absent:
# it is optional support commissioned by theory, never a prerequisite for it.
REQUIRED_THEORY_OPERATOR_IDS = frozenset(
    {
        "source-routing-pre-map-policy-producer",
        "source-routing-realization-producer",
        "frontier-literature-assimilator",
        "high-risk-hypothesis-forger",
        "parallel-hypothesis-portfolio",
        "reflective-conceptual-discovery",
        "reflective-theory-synthesizer",
        "blind-conceptual-preference-adjudicator",
    }
)

# A legacy branch may run only when the canonical scheduler requests a positive
# theory action. Control gates carry no branch investment, while incubation or
# retirement explicitly withhold it. ``prove`` is visible only for consumers
# that also require the exact typed proof handoff; ``probe`` is excluded because
# support experiments have their own theory-subordinate execution lane.
AUTHORIZED_BRANCH_ACTION_KINDS = frozenset(
    {
        "reflect",
        "reframe",
        "differentiate",
        "parallel_mature",
        "cross_pollinate",
        "synthesize",
        "formalize",
        "derive",
        "compare",
        "read",
        "prove",
    }
)
KNOWN_FEEDBACK_OPERATOR_IDS = frozenset(
    {
        *REQUIRED_THEORY_OPERATOR_IDS,
        "dynamic-symbolic-simulation-experimenter",
        "formal-claim-producer",
        "local-reflective-incubator",
        "local-reflective-synthesizer",
    }
)
LOCAL_REQUIRED_THEORY_OPERATOR_IDS = frozenset(
    {
        "frontier-literature-assimilator",
        "high-risk-hypothesis-forger",
        "parallel-hypothesis-portfolio",
        "local-reflective-incubator",
        "local-reflective-synthesizer",
    }
)
_INVESTMENT_BLOCKING_RESTRICTIONS = frozenset(
    {"no_active_investment", "literature_blind"}
)
_MUTABLE_PROJECTION_NAMES = frozenset(
    {"latest", "latest.json", "current", "current.json"}
)
_OPERATOR_ROLES = {
    "source-routing-pre-map-policy-producer": frozenset(
        {"source_routing_pre_map_policy"}
    ),
    "source-routing-realization-producer": frozenset(
        {"source_routing_realization"}
    ),
    "frontier-literature-assimilator": frozenset({"literature_assimilation"}),
    "high-risk-hypothesis-forger": frozenset({"high_risk_portfolio"}),
    "parallel-hypothesis-portfolio": frozenset({"parallel_portfolio"}),
    "reflective-conceptual-discovery": frozenset({"reflective_packets"}),
    "reflective-theory-synthesizer": frozenset({"reflective_packets"}),
    "blind-conceptual-preference-adjudicator": frozenset(
        {
            "parent_conceptual_adjudication",
            "synthesis_conceptual_adjudication",
        }
    ),
    "dynamic-symbolic-simulation-experimenter": frozenset({"experiment_receipt"}),
    "formal-claim-producer": frozenset({"formal_claim_output"}),
    "local-reflective-incubator": frozenset({"reflective_packets"}),
    "local-reflective-synthesizer": frozenset({"reflective_packets"}),
}

SYSTEM_UTC_CLOCK_AUTHORITY_ID = "abducer-system-utc-clock.v1"
PROOF_RECOVERY_UTC_CLOCK_AUTHORITY_ID = (
    "abducer-proof-executor-recovery-utc-clock.v1"
)
_AUTHORIZATION_FACTORY_SEAL = object()
_TEMPORAL_FACTORY_SEAL = object()


class _GovernedLocalTemporalCapability:
    """Closed-registry access to the host wall clock, with an honest boundary.

    This is a governed *local-process* capability: callers cannot provide an
    instant or callback, and every read is bound to the same observed source
    manifest.  It is deliberately not described as authenticated time because
    neither the host clock nor the checkout is externally attested.
    """

    __slots__ = ("_authority_manifest_bytes", "_factory_seal")

    def __init__(self, authority_id: str, *, _factory_seal: object | None = None) -> None:
        if _factory_seal is not _TEMPORAL_FACTORY_SEAL:
            raise TypeError("local temporal capability is issued only by canonical theory replay")
        manifest = _governed_clock_authority(authority_id)
        object.__setattr__(
            self,
            "_authority_manifest_bytes",
            json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8"),
        )
        object.__setattr__(self, "_factory_seal", _factory_seal)

    def __setattr__(self, _name: str, _value: object) -> None:
        raise TypeError("local temporal capability is immutable")

    def manifest(self) -> dict[str, Any]:
        return json.loads(self._authority_manifest_bytes)

    def read(self) -> tuple[dt.datetime, dict[str, Any]]:
        manifest = self.manifest()
        _require(
            manifest == _governed_clock_authority(str(manifest["authority_id"])),
            "local temporal capability implementation changed after issuance",
        )
        instant = _system_utc_now()
        _require(isinstance(instant, dt.datetime), "governed local clock did not return a date-time")
        _require(
            instant.tzinfo is not None,
            "governed local clock returned a timezone-naive date-time",
        )
        return instant.astimezone(dt.timezone.utc), manifest


class VerifiedTheoryAuthorization(Mapping[str, Any]):
    """Immutable in-process capability issued after exact canonical replay.

    Authority is stored as immutable JSON bytes and exposed only through
    defensive copies.  Durable JSON is obtained explicitly with
    :func:`authorization_projection`; it is evidence about a capability, not a
    capability that can later be mutated into broader permission.
    """

    __slots__ = (
        "_authorization_factory_seal",
        "_payload_bytes",
        "_payload_bytes_digest",
        "_present_investment_verified",
        "_temporal_capability",
    )

    def __init__(
        self,
        payload: Mapping[str, Any],
        _factory_seal: object | None = None,
        present_investment_verified: bool = True,
        temporal_capability: _GovernedLocalTemporalCapability | None = None,
    ) -> None:
        if _factory_seal is not _AUTHORIZATION_FACTORY_SEAL:
            raise TypeError(
                "VerifiedTheoryAuthorization is issued only by canonical theory replay"
            )
        normalized = copy.deepcopy(dict(payload))
        encoded = json.dumps(
            normalized,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        object.__setattr__(self, "_authorization_factory_seal", _factory_seal)
        object.__setattr__(self, "_payload_bytes", encoded)
        object.__setattr__(self, "_payload_bytes_digest", bytes_digest(encoded))
        object.__setattr__(self, "_present_investment_verified", present_investment_verified)
        object.__setattr__(self, "_temporal_capability", temporal_capability)

    def __setattr__(self, _name: str, _value: object) -> None:
        raise TypeError("verified theory authorization is immutable")

    def __setitem__(self, _key: str, _value: object) -> None:
        raise TypeError("verified theory authorization is immutable")

    def _snapshot(self) -> dict[str, Any]:
        return json.loads(self._payload_bytes)

    def __getitem__(self, key: str) -> Any:
        return self._snapshot()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._snapshot())

    def __len__(self) -> int:
        return len(self._snapshot())

    def to_projection(self) -> dict[str, Any]:
        """Return a detached JSON-ready evidence projection."""

        return self._snapshot()


def _issue_verified_authorization(
    payload: Mapping[str, Any],
    *,
    present_investment_verified: bool,
    temporal_capability: _GovernedLocalTemporalCapability | None = None,
) -> VerifiedTheoryAuthorization:
    """Issue the opaque marker through the sole module-private factory."""

    return VerifiedTheoryAuthorization(
        copy.deepcopy(dict(payload)),
        _factory_seal=_AUTHORIZATION_FACTORY_SEAL,
        present_investment_verified=present_investment_verified,
        temporal_capability=temporal_capability,
    )


def _validate_authorization_projection(payload: Mapping[str, Any]) -> None:
    """Recompute every authority-bearing digest present in an issued projection."""

    if "authorization_digest" in payload:
        _require(
            payload.get("authorization_digest")
            == canonical_digest(payload, exclude_keys=("authorization_digest",)),
            "authorization projection digest is invalid",
        )
    basis = payload.get("authorization_basis")
    if isinstance(basis, Mapping):
        _require(
            payload.get("authorization_basis_digest") == canonical_digest(basis),
            "immutable authorization basis digest is invalid",
        )
    literature_basis = payload.get("literature_authority_basis")
    if isinstance(literature_basis, Mapping):
        _require(
            payload.get("literature_authority_basis_digest")
            == canonical_digest(literature_basis),
            "immutable literature authority basis digest is invalid",
        )
    support_evidence = payload.get("theory_subordinate_support_evidence")
    if isinstance(support_evidence, Mapping):
        _require(
            support_evidence.get("support_evidence_digest")
            == canonical_digest(
                support_evidence,
                exclude_keys=("support_evidence_digest",),
            )
            and payload.get("theory_subordinate_support_evidence_digest")
            == support_evidence.get("support_evidence_digest"),
            "theory-subordinate support evidence digest is invalid",
        )
        denials = support_evidence.get("derived_denials")
        _require(
            isinstance(denials, Mapping)
            and all(value is False for value in denials.values()),
            "support evidence cannot carry theory, proof, or physics authority",
        )
    decision = payload.get("present_investment_decision")
    if isinstance(decision, Mapping):
        _require(
            payload.get("present_investment_decision_digest") == canonical_digest(decision),
            "present-investment decision digest is invalid",
        )
        _require(
            decision.get("authorization_basis_digest")
            == payload.get("authorization_basis_digest")
            and decision.get("literature_authority_basis_digest")
            == payload.get("literature_authority_basis_digest"),
            "present-investment decision crossed its immutable basis",
        )
        clock = decision.get("clock_authority")
        _require(isinstance(clock, Mapping), "present-investment decision lacks clock authority")
        _require(
            decision.get("clock_authority_digest") == clock.get("authority_digest")
            and clock.get("authority_digest")
            == canonical_digest(clock, exclude_keys=("authority_digest",)),
            "present-investment clock authority digest is invalid",
        )
    schedule = payload.get("schedule")
    if isinstance(schedule, Mapping):
        if payload.get("status") == "actions_reserved":
            _require(
                schedule.get("consumed_schedule_digest")
                == canonical_digest(
                    schedule,
                    exclude_keys=("consumed_schedule_digest", "created_at"),
                ),
                "reserved consumed-schedule digest is invalid",
            )
        else:
            _require(
                schedule.get("schedule_digest")
                == canonical_digest(
                    schedule,
                    exclude_keys=("schedule_digest", "created_at", "consumption_log"),
                ),
                "authorization schedule digest is invalid",
            )
    eligibility = {
        "eligible_branch_ids": payload.get("eligible_branch_ids"),
        "action_ids_by_branch": payload.get("action_ids_by_branch"),
        "action_kinds_by_branch": payload.get("action_kinds_by_branch"),
        "investment_authorized": payload.get("investment_authorized"),
        "authorization_semantics": payload.get("authorization_semantics"),
    }
    if all(value is not None for value in eligibility.values()) and isinstance(basis, Mapping):
        _require(
            basis.get("schedule_eligibility_derivation_digest")
            == canonical_digest(eligibility),
            "authorization eligibility differs from the immutable schedule derivation",
        )
    reservation = payload.get("reservation")
    if isinstance(reservation, Mapping):
        _require(
            reservation.get("reservation_digest")
            == canonical_digest(reservation, exclude_keys=("reservation_digest",)),
            "action reservation digest is invalid",
        )
        reservation_basis = payload.get("reservation_authorization_basis")
        _require(
            isinstance(reservation_basis, Mapping)
            and payload.get("reservation_authorization_basis_digest")
            == canonical_digest(reservation_basis)
            and reservation_basis.get("source_authorization_basis_digest")
            == payload.get("authorization_basis_digest")
            and reservation_basis.get("reservation_digest")
            == reservation.get("reservation_digest"),
            "reservation authority crossed its immutable theory basis",
        )
        temporal_evaluation = payload.get("reservation_temporal_evaluation")
        _require(
            isinstance(temporal_evaluation, Mapping)
            and payload.get("reservation_temporal_evaluation_digest")
            == canonical_digest(temporal_evaluation)
            and temporal_evaluation == reservation.get("temporal_evaluation"),
            "reservation temporal evidence is missing or changed",
        )


def authorization_projection(value: VerifiedTheoryAuthorization) -> dict[str, Any]:
    """Return a validated, detached serializable projection of a capability."""

    _require(isinstance(value, VerifiedTheoryAuthorization), "authorization projection requires a runtime capability")
    _require(
        value._authorization_factory_seal is _AUTHORIZATION_FACTORY_SEAL
        and bytes_digest(value._payload_bytes) == value._payload_bytes_digest,
        "runtime authorization capability seal is invalid",
    )
    payload = value.to_projection()
    _validate_authorization_projection(payload)
    return payload


def authorization_is_runtime_verified(value: object) -> bool:
    """Return whether ``value`` carries present-investment verifier authority."""

    if not isinstance(value, VerifiedTheoryAuthorization):
        return False
    try:
        authorization_projection(value)
    except (ContractError, TypeError, ValueError):
        return False
    return value._present_investment_verified


def _validated_runtime_authorization(
    value: Mapping[str, Any], *, require_fresh: bool
) -> tuple[dict[str, Any], dt.datetime | None, dict[str, Any] | None]:
    """Validate the immutable capability and, at use, reread its local clock."""

    _require(
        isinstance(value, VerifiedTheoryAuthorization)
        and authorization_is_runtime_verified(value),
        "operation requires a live runtime-verified authorization capability",
    )
    payload = authorization_projection(value)
    if not require_fresh:
        return payload, None, None
    temporal = value._temporal_capability
    _require(
        isinstance(temporal, _GovernedLocalTemporalCapability)
        and temporal._factory_seal is _TEMPORAL_FACTORY_SEAL,
        "runtime authorization lacks its governed local temporal capability",
    )
    evaluated_at, manifest = temporal.read()
    decision = payload.get("present_investment_decision")
    _require(isinstance(decision, Mapping), "runtime authorization lacks a present decision")
    _require(
        manifest == decision.get("clock_authority"),
        "runtime temporal capability differs from the present decision",
    )
    consume_before = _timestamp(decision.get("consume_before"), "authorization consume-before")
    commit_at = _timestamp(decision.get("recorded_commit_created_at"), "recorded commit time")
    _require(commit_at <= evaluated_at, "governed local clock precedes the recorded commit")
    _require(
        evaluated_at <= consume_before,
        "governed local authorization passed its consume-before boundary",
    )
    return payload, evaluated_at, manifest


def validate_authorization_at_use_with_temporal_evidence(
    value: Mapping[str, Any],
    *,
    allowed_statuses: Sequence[str] = ("verified_active_current", "actions_reserved"),
) -> tuple[dict[str, Any], dt.datetime, dict[str, Any], str]:
    """Revalidate one capability and expose its exact use-time clock evidence.

    This is intentionally a local process-time capability, not an external or
    authenticated time oracle.  Consumers use it to prevent an issued or
    reserved capability from being replayed after its declared investment
    window.  The returned instant is the actual governed clock read used by the
    validation; the detached manifest and its digest let a durable downstream
    record preserve that point-in-time observation without claiming cross-store
    atomicity or externally authenticated time.
    """

    statuses = tuple(str(status) for status in allowed_statuses)
    _require(bool(statuses), "authorization use-time status set is empty")
    payload, evaluated_at, manifest = _validated_runtime_authorization(
        value, require_fresh=True
    )
    _require(
        payload.get("status") in statuses,
        "runtime authorization has the wrong status at capability use",
    )
    _require(
        isinstance(evaluated_at, dt.datetime)
        and evaluated_at.tzinfo is not None
        and evaluated_at.utcoffset() == dt.timedelta(0),
        "governed local clock did not return an aware UTC instant",
    )
    _require(
        isinstance(manifest, Mapping),
        "runtime authorization lacks governed clock evidence",
    )
    clock_authority = copy.deepcopy(dict(manifest))
    clock_authority_digest = clock_authority.get("authority_digest")
    _require(
        isinstance(clock_authority_digest, str)
        and clock_authority_digest
        == canonical_digest(
            clock_authority,
            exclude_keys=("authority_digest",),
        ),
        "governed local clock authority digest is invalid",
    )
    return (
        payload,
        evaluated_at.astimezone(dt.timezone.utc),
        clock_authority,
        clock_authority_digest,
    )


def validate_authorization_at_use(
    value: Mapping[str, Any],
    *,
    allowed_statuses: Sequence[str] = ("verified_active_current", "actions_reserved"),
) -> dict[str, Any]:
    """Preserve the projection-only use-time validation API."""

    payload, _, _, _ = validate_authorization_at_use_with_temporal_evidence(
        value,
        allowed_statuses=allowed_statuses,
    )
    return payload


def _role_specific_consumer(operator_id: str, event: Mapping[str, Any]) -> bool:
    """Recognize the closed semantic event class owned by each operator."""

    event_type = event.get("event_type")
    entity_type = event.get("entity_type")
    kind = event.get("payload", {}).get("kind")
    if operator_id == "source-routing-pre-map-policy-producer":
        return event_type == "reflection_recorded" and kind == (
            "source_routing_pre_map_policy"
        )
    if operator_id == "source-routing-realization-producer":
        return event_type == "reflection_recorded" and kind == (
            "source_routing_realization"
        )
    if operator_id == "frontier-literature-assimilator":
        return event_type == "literature_snapshot_recorded" and entity_type == "literature_snapshot"
    if operator_id == "high-risk-hypothesis-forger":
        return event_type == "entity_upsert" and entity_type == "hypothesis"
    if operator_id == "parallel-hypothesis-portfolio":
        return event_type == "branch_attempt_recorded" and entity_type == "branch_attempt"
    if operator_id in {
        "reflective-conceptual-discovery",
        "local-reflective-incubator",
    }:
        mutation = event.get("payload", {}).get("mutation_or_synthesis", {})
        payload = event.get("payload", {})
        return (
            event_type == "reflection_recorded"
            and entity_type == "reflection"
            and ((payload.get("result") in {"mutated", "synthesized", "demoted"}
                  and bool(mutation.get("changed_primitives_relations_or_explanation")))
                 or (payload.get("result") == "no_change"
                     and bool(str(payload.get("no_change_reason") or "").strip())
                     and not mutation.get("changed_primitives_relations_or_explanation")))
        )
    if operator_id in {
        "reflective-theory-synthesizer",
        "local-reflective-synthesizer",
    }:
        return event_type == "synthesis_recorded" and entity_type == "synthesis"
    if operator_id == "blind-conceptual-preference-adjudicator":
        return event_type == "reflection_recorded" and kind == "conceptual_adjudication_evidence"
    if operator_id == "dynamic-symbolic-simulation-experimenter":
        return event_type == "reflection_recorded" and kind == "post_result_reflective_assimilation"
    if operator_id == "formal-claim-producer":
        return event_type == "reflection_recorded" and kind == "formal_claim_production"
    return False


def _require(condition: bool, message: str) -> None:
    """Raise a contract error with a theory-gate-specific explanation."""

    if not condition:
        raise ContractError(f"canonical theory gate rejected projection: {message}")


def _timestamp(value: Any, label: str) -> dt.datetime:
    """Parse one timezone-aware canonical deadline."""

    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ContractError(f"canonical theory gate rejected projection: {label} is not ISO date-time") from exc
    _require(parsed.tzinfo is not None, f"{label} is not timezone-aware")
    return parsed.astimezone(dt.timezone.utc)


def _load_object(path: Path, label: str) -> dict[str, Any]:
    """Load one exact JSON object from the canonical commit."""

    payload = load_json(path)
    if not isinstance(payload, dict):
        raise ContractError(f"canonical theory gate {label} is not a JSON object: {path}")
    return payload


def _resolve_commit(
    store: DiscoveryTransactionStore,
    *,
    generation: int,
    commit_id: str,
) -> tuple[Path, dict[str, Any]]:
    """Locate the one manifest matching an already verified store generation."""

    matches: list[tuple[Path, dict[str, Any]]] = []
    for candidate in store.commits_dir.iterdir():
        if not candidate.is_dir():
            continue
        manifest_path = candidate / "manifest.json"
        if not manifest_path.is_file():
            continue
        manifest = _load_object(manifest_path, "manifest")
        if manifest.get("generation") == generation and manifest.get("commit_id") == commit_id:
            matches.append((candidate, manifest))
    _require(len(matches) == 1, "the exact commit ID/generation is missing or ambiguous")
    return matches[0]


def _assert_projection_paths(
    projection: Mapping[str, Any],
    *,
    projection_path: Path,
    state_root: Path,
    commit_path: Path,
    manifest_path: Path,
) -> None:
    """Check absolute or projection-relative self-location fields exactly."""

    expected = {
        "transaction_root": state_root,
        "commit_path": commit_path,
        "manifest_path": manifest_path,
    }
    for field, expected_path in expected.items():
        declared = projection.get(field)
        if declared is None:
            continue
        declared_path = Path(str(declared))
        if not declared_path.is_absolute():
            declared_path = safe_relative_path(
                str(declared), projection_path.parent, forbid_latest=False
            )
        _require(
            declared_path.resolve() == expected_path.resolve(),
            f"{field} does not name the verified canonical transaction location",
        )


def _verify_committed_artifacts(
    projection: Mapping[str, Any],
    *,
    commit_path: Path,
    manifest: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind every projected cycle field to the exact committed artifact bytes."""

    descriptor_rows = manifest.get("artifacts", [])
    _require(isinstance(descriptor_rows, list), "manifest artifacts must be a list")
    descriptors = {
        str(row.get("path")): row
        for row in descriptor_rows
        if isinstance(row, Mapping) and row.get("path")
    }
    _require(len(descriptors) == len(descriptor_rows), "manifest artifact paths are malformed or duplicated")
    artifact_paths = projection.get("artifact_paths", {})
    artifact_digests = projection.get("artifact_digests", {})
    _require(isinstance(artifact_paths, Mapping), "artifact_paths must be an object")
    _require(isinstance(artifact_digests, Mapping), "artifact_digests must be an object")
    _require(set(artifact_paths) == set(artifact_digests), "artifact path/digest roles differ")
    _require(len(set(artifact_paths.values())) == len(artifact_paths), "artifact roles are not a path bijection")
    _require(
        set(str(value) for value in artifact_paths.values()) == set(descriptors),
        "projection roles do not exactly cover the commit manifest",
    )
    required_roles = {
        "cycle",
        "events",
        "evaluations",
        "schedule",
        "feedback_edges",
        "operator_evidence",
    }
    _require(required_roles.issubset(artifact_paths), "required committed cycle artifacts are absent")
    _require(required_roles.issubset(artifact_digests), "required committed artifact digests are absent")

    committed: dict[str, Any] = {}
    json_roles = {
        *required_roles,
        "proof_handoff",
        "experiment_reflection_receipt",
    }
    for role, raw_relative in artifact_paths.items():
        relative = safe_relative_path(str(raw_relative))
        relative_text = relative.as_posix()
        descriptor = descriptors.get(relative_text)
        _require(descriptor is not None, f"artifact role {role!r} is absent from the commit manifest")
        artifact = commit_path / "artifacts" / relative
        _require(artifact.is_file(), f"artifact role {role!r} is missing from the commit")
        actual_digest = file_digest(artifact)
        _require(actual_digest == descriptor.get("sha256"), f"manifest digest mismatch for artifact role {role!r}")
        _require(artifact.stat().st_size == descriptor.get("size_bytes"), f"manifest size mismatch for artifact role {role!r}")
        _require(actual_digest == artifact_digests.get(role), f"projection digest mismatch for artifact role {role!r}")
        if role in json_roles:
            committed[str(role)] = load_json(artifact)

    core = committed["cycle"]
    _require(isinstance(core, Mapping), "committed cycle artifact is not an object")
    for field, value in core.items():
        _require(projection.get(field) == value, f"projection field {field!r} differs from committed cycle bytes")
    _require(projection.get("events") == committed["events"], "events differ from committed bytes")

    evaluations = committed["evaluations"]
    _require(isinstance(evaluations, Mapping), "committed evaluations artifact is not an object")
    _require(
        projection.get("evaluation_receipts") == evaluations.get("receipts"),
        "evaluation receipts differ from committed bytes",
    )
    _require(
        projection.get("evaluation_identity_bindings")
        == evaluations.get("candidate_identity_bindings"),
        "evaluation identity bindings differ from committed bytes",
    )
    _require(projection.get("schedule") == committed["schedule"], "schedule differs from committed bytes")
    _require(
        projection.get("feedback_edges") == committed["feedback_edges"],
        "feedback edges differ from committed bytes",
    )
    _require(
        projection.get("operator_evidence") == committed["operator_evidence"],
        "operator evidence differs from committed bytes",
    )
    evidence = committed["operator_evidence"]
    _require(isinstance(evidence, Mapping), "committed operator evidence is not an object")
    validate_instance(evidence, "canonical_operator_evidence.schema.json")
    _require(
        evidence.get("evidence_digest")
        == canonical_digest(evidence, exclude_keys=("evidence_digest",)),
        "operator evidence self-digest is invalid",
    )
    _require(
        evidence.get("evidence_digest") == projection.get("operator_evidence_digest"),
        "cycle does not bind the sealed operator evidence digest",
    )
    committed_proof = committed.get("proof_handoff")
    _require(projection.get("proof_handoff") == committed_proof, "proof handoff differs from committed bytes")
    if projection.get("proof_handoff_id") is not None:
        _require("proof_handoff" in artifact_paths and committed_proof is not None, "proof handoff artifact is absent")
        _require(
            committed_proof.get("handoff_id") == projection.get("proof_handoff_id"),
            "proof handoff ID differs from committed bytes",
        )
    else:
        _require("proof_handoff" not in artifact_paths and committed_proof is None, "unexpected proof handoff artifact")
    committed_reflection = committed.get("experiment_reflection_receipt")
    projected_reflection = projection.get("experiment_reflection_receipt")
    _require(
        committed_reflection == projected_reflection,
        "experiment reflection receipt differs from committed bytes",
    )
    _require(
        projected_reflection is None
        and committed_reflection is None
        and "experiment_reflection_receipt" not in artifact_paths,
        "same-generation experiment reflection is forbidden; terminal support "
        "observations may request only a distinct descendant theory reflection",
    )
    return committed


def _request_input_digest(request: Mapping[str, Any]) -> str:
    """Recompute the dispatcher request digest from every declared input."""

    return canonical_digest(
        {
            "identity": request["identity"],
            "operator": request["operator"],
            "parameters": request.get("parameters", {}),
            "input_artifacts": request.get("input_artifacts", []),
            "declared_outputs": request.get("declared_outputs", []),
        }
    )


def _validate_role_payloads(role_payloads: Mapping[str, list[dict[str, Any]]]) -> None:
    """Independently validate every semantic output reconstructed from sealed bytes."""

    snapshots = role_payloads.get("literature_snapshot", [])
    literature_bundles = role_payloads.get(
        "literature_production_input_bundle", []
    )
    assimilations = role_payloads.get("literature_assimilation", [])
    portfolios = role_payloads.get("high_risk_portfolio", [])
    parallels = role_payloads.get("parallel_portfolio", [])
    reflections = role_payloads.get("reflective_packets", [])
    experiment_specs = role_payloads.get("experiment_spec", [])
    experiment_receipts = role_payloads.get("experiment_receipt", [])
    routing_policies = role_payloads.get("source_routing_pre_map_policy", [])
    routing_realizations = role_payloads.get("source_routing_realization", [])
    legacy_routing_precommits = role_payloads.get("source_routing_precommit", [])
    parent_adjudications = role_payloads.get(
        "parent_conceptual_adjudication", []
    )
    synthesis_adjudications = role_payloads.get(
        "synthesis_conceptual_adjudication", []
    )
    formal_claim_outputs = role_payloads.get("formal_claim_output", [])
    _require(len(snapshots) == len(assimilations) == len(portfolios) == len(parallels) == 1,
             "sealed core semantic roles do not have exact cardinality one")
    _require(
        len(literature_bundles) == 1,
        "sealed literature-production input role must have exact cardinality one",
    )
    _require(
        len(reflections) == 2,
        "sealed reflective packet role must contain exact parent and synthesis proposals",
    )
    _require(
        len(formal_claim_outputs) <= 1,
        "sealed formal-claim role has cardinality greater than one",
    )
    _require(
        not legacy_routing_precommits,
        "legacy source-routing precommit is compatibility-only and cannot enter active authority",
    )
    _require(
        not experiment_specs and not experiment_receipts,
        "same-generation experiment roles are forbidden at the theory gate; "
        "replay descendant support through its registered commit chain",
    )
    snapshot = snapshots[0]
    validate_snapshot(snapshot)
    literature_bundle = validate_portable_literature_production_input_bundle(
        literature_bundles[0]
    )
    assimilation = assimilations[0]
    validate_assimilation(assimilation, snapshot=snapshot)
    if snapshot.get("provenance_mode") == "live":
        _require(
            len(routing_policies) == len(routing_realizations) == 1,
            "sealed active literature lacks exactly one source-routing policy-realization pair",
        )
        _require(
            len(parent_adjudications) == len(synthesis_adjudications) == 1,
            "sealed active conceptual authority lacks exact parent and synthesis adjudications",
        )
    else:
        _require(
            not routing_policies
            and not routing_realizations
            and not parent_adjudications
            and not synthesis_adjudications
            and not formal_claim_outputs,
            "non-active literature carries fabricated source or conceptual preference authority",
        )
    validate_high_risk_portfolio(portfolios[0], literature_snapshot=snapshot)
    validate_parallel_portfolio(parallels[0])
    _require(
        literature_bundle.get("target_id") == snapshot.get("target_id")
        and literature_bundle.get("state_version")
        == parallels[0].get("base_theory_state_version"),
        "sealed literature-production input crossed target or theory generation",
    )
    for packet in reflections:
        validate_instance(packet, "reflective_conceptual_discovery_packet.schema.json")
        _require(
            packet.get("packet_digest")
            == canonical_digest(packet, exclude_keys=("packet_digest",)),
            "sealed reflective packet self-digest is invalid",
        )
        validate_packet_invariants(packet)
    for evidence in [*parent_adjudications, *synthesis_adjudications]:
        validate_instance(
            evidence, "conceptual_adjudication_evidence.schema.json"
        )
        _require(
            evidence.get("evidence_digest")
            == canonical_digest(
                evidence, exclude_keys=("evidence_digest", "created_at")
            ),
            "sealed conceptual adjudication self-digest is invalid",
        )
    for formal_claim_output in formal_claim_outputs:
        validate_formal_claim_producer_output(formal_claim_output)
    for spec, receipt in zip(experiment_specs, experiment_receipts, strict=True):
        validate_instance(spec, "dynamic_experiment_spec_v3.schema.json")
        validate_experiment_spec(spec)
        validate_instance(receipt, "dynamic_experiment_receipt_v3.schema.json")
        for field in (
            "experiment_id",
            "branch_id",
            "target_id",
            "run_id",
            "state_version",
            "theory_programme_id",
            "source_theory_programme_digest",
            "source_reflection_packet_digest",
            "conceptual_system_ids",
            "theoretical_question_id",
            "adapter",
            "spec_digest",
        ):
            _require(
                receipt.get(field) == spec.get(field),
                f"sealed experiment receipt differs from its specification field {field}",
            )
        expected = experiment_output_digest(receipt)
        _require(receipt.get("output_digest") == expected, "sealed experiment output digest is invalid")
        _require(
            receipt.get("validator", {}).get("status") == "valid"
            and receipt.get("validator", {}).get("checked_digest") == expected,
            "sealed experiment validator did not bind the exact result",
        )

        # Receipt fields and self-digests are necessary but not sufficient. Run
        # the adapter validator again in an isolated scratch directory so the
        # gate independently reproduces decisive and operational outcomes from
        # the exact sealed specification rather than trusting producer labels.
        with tempfile.TemporaryDirectory(prefix="abducer-theory-gate-experiment-") as raw:
            try:
                validate_experiment_receipt(
                    receipt,
                    spec,
                    work_directory=Path(raw),
                )
            except ContractError as exc:
                raise ContractError(
                    "canonical theory gate rejected projection: independent sealed "
                    f"experiment replay failed: {exc}"
                ) from exc


def _system_utc_now() -> dt.datetime:
    """Read the process system clock at microsecond resolution in UTC."""

    return dt.datetime.now(dt.timezone.utc)


def _governed_clock_authority(authority_id: str) -> dict[str, Any]:
    """Describe the sole governed local clock without claiming authentication."""

    _require(
        authority_id == SYSTEM_UTC_CLOCK_AUTHORITY_ID,
        f"unregistered present clock authority {authority_id!r}",
    )
    manifest = {
        "schema_version": "1.0.0",
        "authority_id": SYSTEM_UTC_CLOCK_AUTHORITY_ID,
        "authority_kind": "closed_registry_local_process_wall_clock",
        "implementation_module": __name__,
        "implementation_symbol": "_system_utc_now",
        "implementation_digest": file_digest(Path(__file__).resolve()),
        "time_scale": "UTC",
        "resolution": "microsecond",
        "authority_scope": "ephemeral_present_investment_decision_only",
        "caller_supplied_instants_allowed": False,
        "authentication_status": "not_externally_authenticated",
        "trust_boundary": "current_process_host_clock_and_checkout",
    }
    manifest["authority_digest"] = canonical_digest(manifest)
    return manifest


def read_proof_recovery_clock_evidence() -> tuple[str, dict[str, Any], str]:
    """Read one governed instant for proof-lease recovery and nothing else.

    Unlike the investment capability, this clock remains readable after a
    literature consume-before deadline.  Its manifest explicitly withholds
    investment, launch, respawn, theory-selection, and proof authority.  The
    caller supplies neither an instant nor a callback.
    """

    manifest: dict[str, Any] = {
        "schema_version": "1.0.0",
        "authority_id": PROOF_RECOVERY_UTC_CLOCK_AUTHORITY_ID,
        "authority_kind": (
            "closed_registry_local_process_wall_clock_recovery_only"
        ),
        "implementation_module": __name__,
        "implementation_symbol": "_system_utc_now",
        "implementation_digest": file_digest(Path(__file__).resolve()),
        "time_scale": "UTC",
        "resolution": "microsecond",
        "authority_scope": (
            "proof_executor_lease_checkpoint_and_expiry_recovery_only"
        ),
        "caller_supplied_instants_allowed": False,
        "readable_after_investment_expiry": True,
        "may_validate_present_investment": False,
        "may_authorize_launch": False,
        "may_authorize_respawn": False,
        "may_mutate_theory": False,
        "authentication_status": "not_externally_authenticated",
        "trust_boundary": "current_process_host_clock_and_checkout",
    }
    manifest["authority_digest"] = canonical_digest(manifest)
    instant = _system_utc_now()
    _require(
        isinstance(instant, dt.datetime)
        and instant.tzinfo is not None,
        "proof recovery clock returned no aware date-time",
    )
    observed = instant.astimezone(dt.timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )
    return observed, manifest, str(manifest["authority_digest"])


def _read_governed_present_instant(
    authority_id: str,
) -> tuple[dt.datetime, dict[str, Any], _GovernedLocalTemporalCapability]:
    """Read one governed instant; callers select an authority ID, never a time."""

    capability = _GovernedLocalTemporalCapability(
        authority_id,
        _factory_seal=_TEMPORAL_FACTORY_SEAL,
    )
    instant, authority = capability.read()
    return instant, authority, capability


def _verify_assimilated_literature_authority(
    literature: Mapping[str, Any],
    *,
    evidence_index: Mapping[str, Any],
    manifest: Mapping[str, Any],
    require_current: bool,
    clock_authority_id: str,
) -> dict[str, Any]:
    """Derive freshness only from sealed snapshot/assimilation authority.

    The cycle's recorded use-time proves historical causality.  It never acts
    as the verifier's present clock.  Conversely, frozen-response provenance
    remains tied to the original acquisition even when a trusted current-time
    evaluation still falls inside that acquisition's bounded window.
    """

    role_payloads = evidence_index["role_payloads"]
    snapshots = role_payloads.get("literature_snapshot", [])
    assimilations = role_payloads.get("literature_assimilation", [])
    routing_policies = role_payloads.get("source_routing_pre_map_policy", [])
    routing_realizations = role_payloads.get("source_routing_realization", [])
    active = literature.get("mode") == "active_current"
    _require(
        len(snapshots) == len(assimilations) == 1,
        "sealed literature snapshot/assimilation roles lack exact cardinality one",
    )
    _require(
        (len(routing_policies), len(routing_realizations))
        == ((1, 1) if active else (0, 0)),
        "sealed source-routing authority cardinality differs from literature mode",
    )
    snapshot = snapshots[0]
    assimilation = assimilations[0]
    routing_policy = routing_policies[0] if active else None
    routing_realization = routing_realizations[0] if active else None
    validate_snapshot(snapshot)
    validate_assimilation(assimilation, snapshot=snapshot)

    selected = assimilation.get("selected_snapshot", {})
    expected_selected = {
        "snapshot_id": snapshot["snapshot_id"],
        "content_digest": snapshot["content_digest"],
        "search_completed_at": snapshot["search_completed_at"],
        "coverage_cutoff": snapshot["coverage_cutoff"],
        "provenance_mode": snapshot["provenance_mode"],
        "coverage_limits": list(snapshot["coverage_limits"]),
        "validator_receipt_ids": [
            row["receipt_id"]
            for row in snapshot["validator_receipts"]
            if row["status"] == "passed"
        ],
    }
    _require(
        selected == expected_selected,
        "sealed assimilation selected-snapshot projection differs from the sealed snapshot",
    )
    resolution = assimilation.get("resolution", {})
    required_resolution = {
        "freshness_policy",
        "evaluated_at",
        "max_age_seconds",
        "consume_before",
        "authority_scope",
    }
    _require(
        required_resolution.issubset(resolution),
        "sealed assimilation lacks bounded temporal authority",
    )
    if active:
        _require(
            literature.get("active_investment_allowed") is True
            and literature.get("restrictions") == [],
            "active-current literature basis is not investable",
        )
    else:
        _require(
            literature.get("mode") == "local_only_incubation"
            and literature.get("active_investment_allowed") is False
            and "no_active_investment"
            in set(literature.get("restrictions", [])),
            "local literature basis does not preserve its non-investment boundary",
        )
    try:
        _timestamp(selected["coverage_cutoff"], "sealed coverage cutoff")
        projected_coverage_cutoff = selected["coverage_cutoff"]
    except ContractError:
        projected_coverage_cutoff = selected["search_completed_at"]
    exact_basis = {
        "snapshot_id": selected["snapshot_id"],
        "snapshot_digest": selected["content_digest"],
        "source_routing_pre_map_policy_id": (
            routing_policy["policy_id"] if routing_policy is not None else None
        ),
        "source_routing_pre_map_policy_digest": (
            routing_policy["policy_digest"]
            if routing_policy is not None
            else None
        ),
        "source_routing_realization_id": (
            routing_realization["realization_id"]
            if routing_realization is not None
            else None
        ),
        "source_routing_realization_digest": (
            routing_realization["realization_digest"]
            if routing_realization is not None
            else None
        ),
        "policy": resolution["freshness_policy"],
        "search_completed_at": selected["search_completed_at"],
        "coverage_cutoff": projected_coverage_cutoff,
        "max_age_seconds": resolution["max_age_seconds"],
        "consume_before": resolution["consume_before"],
        "authority_scope": resolution["authority_scope"],
    }
    for field, expected in exact_basis.items():
        _require(
            literature.get(field) == expected,
            f"literature basis field {field} differs from sealed assimilation authority",
        )
    completed_at = _timestamp(
        selected["search_completed_at"], "sealed literature search completion"
    )
    resolution_at = _timestamp(
        resolution["evaluated_at"], "sealed assimilation evaluation"
    )
    recorded_use_at = _timestamp(
        literature.get("present_use_evaluated_at"),
        "recorded canonical literature use",
    )
    commit_at = _timestamp(manifest.get("created_at"), "canonical commit clock")
    _require(
        completed_at <= resolution_at <= recorded_use_at <= commit_at,
        "literature clocks do not satisfy search <= assimilation <= recorded use <= trusted commit",
    )
    expected_freshness = "current" if active else "local_only"
    expected_gate = "pass" if active else "blocked_local_only"
    _require(
        resolution.get("freshness_status") == expected_freshness
        and resolution.get("active_investment_gate") == expected_gate,
        "sealed assimilation status differs from its literature mode",
    )

    recorded = resolve_present_literature_freshness(
        assimilation, now=recorded_use_at
    )
    _require(
        recorded["freshness_status"] == expected_freshness
        and recorded["active_investment_gate"] == expected_gate,
        f"recorded canonical literature use is invalid: {recorded['reason']}",
    )
    _require(
        literature.get("present_use_reason") == recorded["reason"],
        "recorded canonical literature reason differs from sealed freshness replay",
    )

    present_evaluation: dict[str, Any] | None = None
    temporal_capability: _GovernedLocalTemporalCapability | None = None
    if require_current and active:
        present_at, clock_authority, temporal_capability = _read_governed_present_instant(
            clock_authority_id
        )
        _require(
            commit_at <= present_at,
            "governed present clock precedes the immutable canonical commit",
        )
        present = resolve_present_literature_freshness(
            assimilation, now=present_at
        )
        _require(
            present["freshness_status"] == "current"
            and present["active_investment_gate"] == "pass",
            f"governed present-use literature evaluation denied investment: {present['reason']}",
        )
        present_evaluation = {
            "status": "authorized_current",
            "authoritative": True,
            "clock_authority": clock_authority,
            "clock_authority_digest": clock_authority["authority_digest"],
            "evaluated_at": present["evaluated_at"],
            "freshness_status": present["freshness_status"],
            "active_investment_gate": present["active_investment_gate"],
            "reason": present["reason"],
            "recorded_commit_created_at": manifest["created_at"],
            "recorded_commit_time_authority": "unattested_transaction_manifest_local_time",
            "consume_before": resolution["consume_before"],
        }

    provenance_mode = str(snapshot["provenance_mode"])
    acquisition = (
        snapshot["original_acquisition_snapshot"]
        if provenance_mode == "frozen_response_replay"
        else snapshot
    )
    immutable_basis = {
        "literature_snapshot_id": snapshot["snapshot_id"],
        "literature_snapshot_digest": snapshot["content_digest"],
        "literature_assimilation_packet_id": assimilation["packet_id"],
        "literature_assimilation_digest": assimilation["content_digest"],
        "source_routing_pre_map_policy_id": (
            routing_policy["policy_id"] if routing_policy is not None else None
        ),
        "source_routing_pre_map_policy_digest": (
            routing_policy["policy_digest"]
            if routing_policy is not None
            else None
        ),
        "source_routing_realization_id": (
            routing_realization["realization_id"]
            if routing_realization is not None
            else None
        ),
        "source_routing_realization_digest": (
            routing_realization["realization_digest"]
            if routing_realization is not None
            else None
        ),
        "source_routing_acquisition_authority_digest": (
            routing_policy["acquisition_authority_digest"]
            if routing_policy is not None
            else None
        ),
        "source_routing_stage_receipt_ids": (
            {
                row["stage"]: row["receipt_id"]
                for row in routing_realization["stage_receipts"]
            }
            if routing_realization is not None
            else {}
        ),
        "literature_freshness_policy": resolution["freshness_policy"],
        "literature_consume_before": resolution["consume_before"],
        "literature_authority_scope": resolution["authority_scope"],
        "literature_provenance_mode": provenance_mode,
        "literature_acquisition_snapshot_id": acquisition["snapshot_id"],
        "literature_acquisition_snapshot_digest": acquisition["content_digest"],
        "literature_resolution_evaluated_at": resolution["evaluated_at"],
        "literature_recorded_use_evaluated_at": recorded["evaluated_at"],
        "literature_recorded_use_reason": recorded["reason"],
    }
    return {
        "immutable_basis": immutable_basis,
        "immutable_basis_digest": canonical_digest(immutable_basis),
        "present_evaluation": present_evaluation,
        "temporal_capability": temporal_capability,
        "source_authority_pair": (
            {
                "pre_map_policy": routing_policy,
                "realization": routing_realization,
            }
            if active
            else None
        ),
    }


def _verify_operator_evidence(
    projection: Mapping[str, Any],
    *,
    committed: Mapping[str, Any],
    commit_path: Path,
) -> dict[str, Any]:
    """Replay complete requests, attempts, validators, sealed bytes, and role bijection."""

    evidence = committed["operator_evidence"]
    _require(
        evidence.get("cycle_id") == projection.get("cycle_id")
        and evidence.get("target_id") == projection.get("target_id")
        and evidence.get("run_id") == projection.get("run_id")
        and evidence.get("prior_state_version") == projection.get("prior_state_version"),
        "sealed operator evidence crossed the canonical cycle identity",
    )
    requests: dict[str, dict[str, Any]] = {}
    for raw in evidence.get("operator_requests", []):
        validate_operator_request_identity(raw)
        request = dict(raw)
        request_id = str(request["request_id"])
        _require(request_id not in requests, f"duplicate sealed operator request {request_id}")
        identity = request["identity"]
        _require(
            (identity["target_id"], identity["run_id"], identity["state_version"])
            == (projection["target_id"], projection["run_id"], projection["prior_state_version"]),
            f"sealed request {request_id} crossed target/run/state",
        )
        _require(request["input_digest"] == _request_input_digest(request),
                 f"sealed request {request_id} has an invalid input digest")
        _require(len(request["declared_outputs"]) == len(set(request["declared_outputs"])),
                 f"sealed request {request_id} repeats a declared output")
        requests[request_id] = request

    receipts: dict[str, dict[str, Any]] = {}
    attempts: dict[str, set[int]] = {}
    successes_by_request: dict[str, list[dict[str, Any]]] = {}
    for raw in evidence.get("operator_receipts", []):
        validate_operator_receipt_identity(raw)
        receipt = dict(raw)
        receipt_id = str(receipt["receipt_id"])
        request_id = str(receipt["request_id"])
        _require(receipt_id not in receipts, f"duplicate sealed operator receipt {receipt_id}")
        request = requests.get(request_id)
        _require(request is not None, f"sealed receipt {receipt_id} has no sealed request")
        validate_operator_receipt_identity(receipt, request)
        attempt = int(receipt["attempt"])
        prior_attempts = attempts.setdefault(request_id, set())
        _require(attempt not in prior_attempts, f"request {request_id} repeats attempt {attempt}")
        prior_attempts.add(attempt)
        for field in ("invocation_id", "operator", "identity", "required", "input_digest"):
            _require(receipt[field] == request[field],
                     f"sealed receipt {receipt_id} does not exactly bind request field {field}")
        output_digests = [row["sha256"] for row in receipt["output_history_artifacts"]]
        for validator in receipt["validator_receipts"]:
            _require(validator["artifact_digests"] == output_digests,
                     f"validator for {receipt_id} does not bind the exact ordered output set")
        if receipt["status"] == "succeeded":
            _require(set(row["path"] for row in receipt["output_artifacts"])
                     == set(request["declared_outputs"]),
                     f"successful receipt {receipt_id} does not cover every declared output")
            successes_by_request.setdefault(request_id, []).append(receipt)
        receipts[receipt_id] = receipt
    _require(set(attempts) == set(requests), "one or more sealed requests lack a terminal attempt receipt")
    for request_id, numbers in attempts.items():
        _require(numbers == set(range(1, max(numbers) + 1)),
                 f"sealed attempts for {request_id} are not contiguous from one")
        success = successes_by_request.get(request_id, [])
        _require(len(success) <= 1, f"request {request_id} has multiple successful attempts")
        if success:
            _require(success[0]["attempt"] == max(numbers),
                     f"request {request_id} has attempts after success")
    expected_success_ids = sorted(
        receipt_id for receipt_id, receipt in receipts.items() if receipt["status"] == "succeeded"
    )
    _require(evidence.get("successful_receipt_ids") == expected_success_ids,
             "sealed successful receipt index is incomplete or forged")
    _require(projection.get("input_receipt_ids") == expected_success_ids,
             "cycle input receipt index differs from sealed successful attempts")

    input_bindings = evidence.get("input_bindings", [])
    input_keys: set[tuple[str, int]] = set()
    input_paths: set[str] = set()
    input_payloads: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    artifact_bytes_by_original_path: dict[str, bytes] = {}
    for binding in input_bindings:
        request_id = str(binding["request_id"])
        request = requests.get(request_id)
        _require(request is not None, f"sealed input names unknown request {request_id}")
        index = int(binding["input_index"])
        key = (request_id, index)
        _require(key not in input_keys, f"duplicate sealed input binding {key}")
        input_keys.add(key)
        _require(index < len(request["input_artifacts"]), f"sealed input index is out of range: {key}")
        descriptor = binding["original_descriptor"]
        _require(descriptor == request["input_artifacts"][index],
                 f"sealed input {key} differs from its exact request descriptor")
        _require(binding["operator_id"] == request["operator"]["operator_id"],
                 f"sealed input {key} crossed operator identity")
        sealed_path = str(binding["sealed_path"])
        _require(sealed_path not in input_paths,
                 f"multiple request descriptors alias committed input {sealed_path}")
        input_paths.add(sealed_path)
        role = str(binding["commit_artifact_role"])
        _require(projection["artifact_paths"].get(role) == sealed_path,
                 f"sealed input {key} is absent from its commit role")
        data = (commit_path / "artifacts" / safe_relative_path(sealed_path)).read_bytes()
        _require(
            bytes_digest(data) == descriptor["sha256"] == binding["sealed_sha256"]
            and len(data) == descriptor["size_bytes"] == binding["sealed_size_bytes"],
            f"sealed input bytes differ from exact request descriptor {key}",
        )
        original_path = str(descriptor["path"])
        prior_bytes = artifact_bytes_by_original_path.get(original_path)
        _require(
            prior_bytes is None or prior_bytes == data,
            f"committed artifact path has conflicting immutable bytes: {original_path}",
        )
        artifact_bytes_by_original_path[original_path] = data
        try:
            payload = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ContractError(f"sealed request input {key} is not JSON: {exc}") from exc
        _require(isinstance(payload, dict), f"sealed request input {key} is not an object")
        input_payloads.setdefault(request_id, []).append((index, payload))
    expected_input_keys = {
        (request_id, index)
        for request_id, request in requests.items()
        for index, _ in enumerate(request["input_artifacts"])
    }
    _require(input_keys == expected_input_keys,
             "request descriptors and committed input bindings are not an exact bijection")
    ordered_input_payloads = {
        request_id: [payload for _, payload in sorted(rows)]
        for request_id, rows in input_payloads.items()
    }

    artifact_paths = projection["artifact_paths"]
    output_bindings = evidence.get("output_bindings", [])
    binding_keys: set[tuple[str, str]] = set()
    output_by_receipt: dict[str, list[dict[str, Any]]] = {}
    for binding in output_bindings:
        receipt_id = str(binding["receipt_id"])
        receipt = receipts.get(receipt_id)
        _require(receipt is not None, f"sealed output binding names unknown receipt {receipt_id}")
        _require(
            binding["request_id"] == receipt["request_id"]
            and binding["operator_id"] == receipt["operator"]["operator_id"]
            and binding["attempt"] == receipt["attempt"]
            and binding["status"] == receipt["status"],
            f"sealed output binding for {receipt_id} crossed its receipt",
        )
        descriptor = binding["original_descriptor"]
        history_descriptor = binding["history_descriptor"]
        key = (receipt_id, str(descriptor.get("path", "")))
        _require(key not in binding_keys, f"duplicate sealed output binding {key}")
        binding_keys.add(key)
        _require(descriptor in receipt["output_artifacts"],
                 f"sealed output binding for {receipt_id} is not an exact receipt descriptor")
        descriptor_index = receipt["output_artifacts"].index(descriptor)
        _require(history_descriptor == receipt["output_history_artifacts"][descriptor_index],
                 f"sealed output binding for {receipt_id} lacks exact attempt history")
        role = str(binding["commit_artifact_role"])
        _require(artifact_paths.get(role) == binding["sealed_path"],
                 f"sealed output {key} is not bound to its commit artifact role")
        sealed = commit_path / "artifacts" / safe_relative_path(str(binding["sealed_path"]))
        data = sealed.read_bytes()
        _require(
            bytes_digest(data) == descriptor["sha256"] == binding["sealed_sha256"]
            and len(data) == descriptor["size_bytes"] == binding["sealed_size_bytes"],
            f"sealed output bytes differ from receipt {receipt_id}",
        )
        for original_path in (
            str(descriptor["path"]),
            str(history_descriptor["path"]),
        ):
            prior_bytes = artifact_bytes_by_original_path.get(original_path)
            _require(
                prior_bytes is None or prior_bytes == data,
                f"committed artifact path has conflicting immutable bytes: {original_path}",
            )
            artifact_bytes_by_original_path[original_path] = data
        output_by_receipt.setdefault(receipt_id, []).append(dict(binding))
    expected_output_keys = {
        (receipt_id, str(descriptor["path"]))
        for receipt_id, receipt in receipts.items()
        for descriptor in receipt["output_artifacts"]
    }
    _require(binding_keys == expected_output_keys,
             "sealed output bindings do not exactly cover every attempt output")

    expected_validator_keys: set[tuple[str, str, int]] = set()
    validators_by_digest: dict[tuple[str, str], Mapping[str, Any]] = {}
    for receipt_id, receipt in receipts.items():
        for validator in receipt["validator_receipts"]:
            authority = validator["validator_authority"]
            _require(
                authority["authority_digest"]
                == canonical_digest(authority, exclude_keys=("authority_digest",))
                == validator["validator_code_digest"],
                f"validator authority digest is invalid for {receipt_id}",
            )
            _require(
                validator_dependency_policy_is_supported(authority),
                f"validator authority for {receipt_id} overclaims imports",
            )
            validators_by_digest[(receipt_id, validator["receipt_digest"])] = validator
            expected_validator_keys.update(
                (receipt_id, validator["receipt_digest"], index)
                for index, _ in enumerate(authority["files"])
            )
    validator_keys: set[tuple[str, str, int]] = set()
    validator_paths: set[str] = set()
    for binding in evidence.get("validator_authority_bindings", []):
        key = (
            str(binding["receipt_id"]),
            str(binding["validator_receipt_digest"]),
            int(binding["file_index"]),
        )
        _require(key not in validator_keys, f"duplicate validator authority binding {key}")
        validator_keys.add(key)
        validator = validators_by_digest.get((key[0], key[1]))
        _require(validator is not None, f"validator authority binding has no approved receipt {key}")
        authority = validator["validator_authority"]
        _require(
            binding["validator_id"] == validator["validator_id"]
            and binding["authority_digest"] == authority["authority_digest"]
            and binding["authority_file"] == authority["files"][key[2]],
            f"validator authority binding crossed approved runtime identity {key}",
        )
        sealed_path = str(binding["sealed_path"])
        _require(sealed_path not in validator_paths,
                 f"validator authority files alias committed path {sealed_path}")
        validator_paths.add(sealed_path)
        _require(projection["artifact_paths"].get(binding["commit_artifact_role"]) == sealed_path,
                 f"validator authority binding is absent from its commit role {key}")
        data = (commit_path / "artifacts" / safe_relative_path(sealed_path)).read_bytes()
        authority_file = binding["authority_file"]
        _require(
            bytes_digest(data) == authority_file["sha256"] == binding["sealed_sha256"]
            and len(data) == authority_file["size_bytes"] == binding["sealed_size_bytes"],
            f"validator executable/dependency bytes differ for {key}",
        )
    _require(validator_keys == expected_validator_keys,
             "validator authority bindings do not exactly cover approved runtime files")

    role_payload_rows: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    role_payload_by_path: dict[str, dict[str, Any]] = {}
    role_bindings: dict[tuple[str, int], dict[str, Any]] = {}
    producer_role_by_output: dict[tuple[str, str], str] = {}
    for raw in evidence.get("role_bindings", []):
        binding = dict(raw)
        role_name, role_index = str(binding["role"]), int(binding["role_index"])
        role_key = (role_name, role_index)
        _require(role_key not in role_bindings, f"duplicate sealed semantic role {role_key}")
        role_bindings[role_key] = binding
        commit_role = str(binding["commit_artifact_role"])
        _require(artifact_paths.get(commit_role) == binding["sealed_path"],
                 f"semantic role {role_key} is not bound to the named commit artifact")
        sealed = commit_path / "artifacts" / safe_relative_path(str(binding["sealed_path"]))
        data = sealed.read_bytes()
        _require(bytes_digest(data) == binding["sha256"] and len(data) == binding["size_bytes"],
                 f"semantic role {role_key} does not match its sealed bytes")
        if binding["source_kind"] == "operator_output":
            receipt_id = str(binding["producer_receipt_id"])
            request_id = str(binding["producer_request_id"])
            operator_id = str(binding["producer_operator_id"])
            receipt = receipts.get(receipt_id)
            _require(receipt is not None and receipt["status"] == "succeeded",
                     f"semantic role {role_key} is not produced by a successful receipt")
            _require(receipt["request_id"] == request_id and receipt["operator"]["operator_id"] == operator_id,
                     f"semantic role {role_key} crossed producer identity")
            output_key = (receipt_id, str(binding["original_path"]))
            matching = [row for row in output_by_receipt.get(receipt_id, [])
                        if row["original_descriptor"]["path"] == binding["original_path"]]
            _require(len(matching) == 1 and matching[0]["semantic_role"] == role_name
                     and matching[0]["sealed_path"] == binding["sealed_path"],
                     f"semantic role {role_key} is not bijective with its output binding")
            _require(output_key not in producer_role_by_output,
                     f"one successful output impersonates multiple roles: {output_key}")
            producer_role_by_output[output_key] = role_name
            _require(role_name in _OPERATOR_ROLES.get(operator_id, frozenset()),
                     f"operator {operator_id} is sealed under the wrong semantic role {role_name}")
        else:
            _require(role_name in {
                "literature_snapshot",
                "literature_production_input_bundle",
            },
                     f"untrusted external artifact was admitted as decision role {role_name}")
            _require(all(binding[field] is None for field in (
                "producer_receipt_id", "producer_request_id", "producer_operator_id"
            )), f"external semantic role {role_key} fabricates a producer")
        try:
            payload = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ContractError(f"sealed semantic role {role_key} is not JSON: {exc}") from exc
        _require(isinstance(payload, dict), f"sealed semantic role {role_key} is not an object")
        role_payload_rows.setdefault(role_name, []).append((role_index, payload))
        role_payload_by_path[str(binding["original_path"])] = payload
    for role, rows in role_payload_rows.items():
        expected_indices = list(range(len(rows)))
        actual_indices = sorted(index for name, index in role_bindings if name == role)
        _require(actual_indices == expected_indices, f"semantic role {role} indices are not contiguous")
    # Manifest list order is not semantic authority.  Reconstruct every role in
    # its explicit role-index order before selecting a final reflection.
    role_payloads = {
        role: [payload for _, payload in sorted(rows, key=lambda item: item[0])]
        for role, rows in role_payload_rows.items()
    }
    successful_output_keys = {
        key for key in expected_output_keys if receipts[key[0]]["status"] == "succeeded"
    }
    _require(set(producer_role_by_output) == successful_output_keys,
             "successful output and semantic-role assignment are not an exact bijection")
    _validate_role_payloads(role_payloads)
    role_paths: dict[str, list[str]] = {}
    producers_by_role: dict[str, list[dict[str, Any]]] = {}
    for (role_name, role_index), binding in sorted(
        role_bindings.items(), key=lambda item: (item[0][0], item[0][1])
    ):
        paths = role_paths.setdefault(role_name, [])
        _require(
            role_index == len(paths),
            f"semantic role {role_name} path order is not contiguous",
        )
        paths.append(str(binding["original_path"]))
        receipt_id = binding.get("producer_receipt_id")
        if receipt_id is not None:
            producers_by_role.setdefault(role_name, []).append(
                receipts[str(receipt_id)]
            )
    _validate_stage_causality(
        operator_requests=list(requests.values()),
        input_payloads=ordered_input_payloads,
        payloads=role_payloads,
        producers_by_role=producers_by_role,
        role_paths=role_paths,
    )
    validate_source_authority_pair_execution(
        active_required=role_payloads["literature_snapshot"][0].get(
            "provenance_mode"
        )
        == "live",
        payloads=role_payloads,
        producers_by_role=producers_by_role,
        operator_requests=list(requests.values()),
        operator_receipts=list(receipts.values()),
        input_payloads=ordered_input_payloads,
        require_artifact_producers=True,
    )
    return {
        "requests": requests,
        "receipts": receipts,
        "outputs_by_receipt": output_by_receipt,
        "role_payloads": role_payloads,
        "role_payload_by_path": role_payload_by_path,
        "input_payloads": ordered_input_payloads,
        "artifact_bytes_by_original_path": artifact_bytes_by_original_path,
        "role_bindings": role_bindings,
        "role_paths": role_paths,
        "producers_by_role": producers_by_role,
        "evidence_digest": evidence["evidence_digest"],
    }


def _verify_feedback_lineage(
    projection: Mapping[str, Any], evidence_index: Mapping[str, Any]
) -> dict[str, dict[str, Any]]:
    """Prove that each successful operator changed its exact role-specific event."""

    events = {
        str(row.get("event_id")): row
        for row in projection.get("events", [])
        if isinstance(row, Mapping) and row.get("event_id")
    }
    bindings: dict[str, dict[str, Any]] = {}
    input_receipts = set(projection.get("input_receipt_ids", []))
    edge_receipts: set[str] = set()
    receipts = evidence_index["receipts"]
    role_payloads = evidence_index["role_payloads"]
    role_payload_by_path = evidence_index["role_payload_by_path"]
    for edge in projection.get("feedback_edges", []):
        validate_instance(edge, "discovery_feedback_edge.schema.json")
        operator_id = str(edge["producer_operator_id"])
        receipt = receipts.get(str(edge["producer_receipt_id"]))
        _require(receipt is not None and receipt["status"] == "succeeded",
                 f"feedback edge for {operator_id} has no successful sealed receipt")
        _require(edge["producer_receipt_id"] not in edge_receipts,
                 f"successful receipt {edge['producer_receipt_id']} has ambiguous feedback edges")
        edge_receipts.add(edge["producer_receipt_id"])
        _require(
            edge["producer_request_id"] == receipt["request_id"]
            and operator_id == receipt["operator"]["operator_id"],
            f"feedback edge for {operator_id} crossed sealed request/receipt identity",
        )
        expected_outputs = [
            {key: descriptor[key] for key in ("path", "sha256", "size_bytes")}
            for descriptor in receipt["output_artifacts"]
        ]
        _require(edge["producer_output_artifacts"] == expected_outputs,
                 f"feedback edge for {operator_id} does not bind the exact output descriptors")
        event = events.get(str(edge["consumer_event_id"]))
        _require(event is not None, f"feedback edge for {operator_id} names no committed event")
        _require(
            event.get("event_hash") == edge["consumer_event_hash"],
            f"feedback edge for {operator_id} has a stale event hash",
        )
        _require(
            edge["producer_receipt_id"] in event.get("source_receipt_ids", []),
            f"feedback edge for {operator_id} is not a source of its semantic event",
        )
        _require(
            event.get("payload", {}).get("kind") != "operator_output_consumed",
            f"feedback edge for {operator_id} points only to bookkeeping",
        )
        _require(
            _role_specific_consumer(operator_id, event),
            f"feedback edge for {operator_id} does not point to its role-specific semantic event",
        )
        _require(
            edge["producer_receipt_id"] in input_receipts,
            f"feedback edge for {operator_id} is absent from cycle input receipts",
        )
        _require(
            edge["target_id"] == projection["target_id"]
            and edge["run_id"] == projection["run_id"]
            and edge["prior_state_version"] == projection["prior_state_version"]
            and edge["committed_state_generation"] == projection["committed_state_version"],
            f"feedback edge for {operator_id} crossed the cycle lineage",
        )
        receipt_roles = {
            str(binding["role"])
            for binding in evidence_index["role_bindings"].values()
            if binding.get("producer_receipt_id") == edge["producer_receipt_id"]
        }
        _require(
            len(receipt_roles) == 1,
            f"successful operator {operator_id} lacks one exact semantic role",
        )
        expected_role = next(iter(receipt_roles))
        _require(
            expected_role in _OPERATOR_ROLES.get(operator_id, frozenset()),
            f"successful operator has no closed feedback role: {operator_id}",
        )
        operator_payloads = role_payloads.get(expected_role, [])
        expected_projections: list[dict[str, Any]] = []
        for descriptor in receipt["output_artifacts"]:
            output_path = str(descriptor["path"])
            output_payload = role_payload_by_path.get(output_path)
            _require(output_payload is not None,
                     f"feedback output {output_path} has no sealed semantic payload")
            for row in _canonical_semantic_output_rows(operator_id, output_payload):
                marker = {**row, "source_output_path": output_path}
                matches = [
                    candidate
                    for candidate in events.values()
                    if candidate.get("payload", {}).get("semantic_projection") == marker
                    and edge["producer_receipt_id"] in candidate.get("source_receipt_ids", [])
                ]
                _require(len(matches) == 1,
                         f"semantic row {marker} does not project to exactly one committed event")
                semantic_event = matches[0]
                expected_projections.append(
                    {
                        "output_path": output_path,
                        **row,
                        "consumer_event_id": semantic_event["event_id"],
                        "consumer_event_hash": semantic_event["event_hash"],
                    }
                )
        expected_projections.sort(
            key=lambda row: (row["output_path"], row["semantic_kind"], row["semantic_id"])
        )
        _require(edge["semantic_event_projections"] == expected_projections,
                 f"feedback edge for {operator_id} is not an exhaustive semantic-row projection")
        payload = event.get("payload", {})
        if operator_id == "source-routing-pre-map-policy-producer":
            policy = operator_payloads[0]
            _require(
                payload.get("kind") == "source_routing_pre_map_policy"
                and payload.get("source_authority_artifact_id")
                == policy["policy_id"]
                and payload.get("source_authority_artifact_digest")
                == policy["policy_digest"]
                and payload.get("source_authority_artifact") == policy,
                "source policy feedback does not equal its sealed producer artifact",
            )
        elif operator_id == "source-routing-realization-producer":
            realization = operator_payloads[0]
            _require(
                payload.get("kind") == "source_routing_realization"
                and payload.get("source_authority_artifact_id")
                == realization["realization_id"]
                and payload.get("source_authority_artifact_digest")
                == realization["realization_digest"]
                and payload.get("source_authority_artifact") == realization,
                "source realization feedback does not equal its sealed producer artifact",
            )
        elif operator_id == "frontier-literature-assimilator":
            assimilation = operator_payloads[0]
            snapshot = role_payloads["literature_snapshot"][0]
            _require(
                event["entity_id"] == assimilation["selected_snapshot"]["snapshot_id"]
                and payload.get("assimilation_packet_id") == assimilation["packet_id"]
                and payload.get("assimilation_content_digest") == assimilation["content_digest"]
                and payload.get("content_digest") == snapshot["content_digest"]
                and payload.get("source_claim_mappings") == assimilation["theory_mappings"]
                and payload.get("source_theory_deltas") == assimilation["ledger_events"],
                "literature feedback event does not equal the sealed assimilation/snapshot content",
            )
        elif operator_id == "high-risk-hypothesis-forger":
            portfolio = operator_payloads[0]
            hypothesis = next(
                (row for row in portfolio["hypotheses"] if row["hypothesis_id"] == event["entity_id"]),
                None,
            )
            record = payload.get("record", {})
            _require(
                hypothesis is not None
                and record.get("source_portfolio_id") == portfolio["portfolio_id"]
                and record.get("source_portfolio_digest") == portfolio["content_digest"]
                and all(record.get(key) == value for key, value in hypothesis.items()),
                "hypothesis feedback event does not preserve the sealed portfolio candidate",
            )
        elif operator_id == "parallel-hypothesis-portfolio":
            parallel = operator_payloads[0]
            attempt = next(
                (row for row in parallel["attempt_receipts"] if row["receipt_id"] == event["entity_id"]),
                None,
            )
            expected_outcome = (
                "validated" if attempt and attempt["status"] in {"completed", "reused"}
                else "timed_out" if attempt and attempt["status"] == "timeout" else "failed"
            )
            _require(
                attempt is not None
                and payload.get("branch_id") == attempt["branch_id"]
                and payload.get("operational_status") == attempt["status"]
                and payload.get("outcome") == expected_outcome
                and payload.get("parallel_portfolio_id") == parallel["portfolio_id"]
                and payload.get("parallel_portfolio_digest") == parallel["content_digest"],
                "parallel feedback event does not equal a sealed attempt",
            )
        elif operator_id in {"reflective-conceptual-discovery", "local-reflective-incubator"}:
            packet = next((row for row in operator_payloads if row["packet_id"] == payload.get("packet_id")), None)
            round_row = next(
                (
                    row
                    for row in packet.get("reflection_rounds", [])
                    if row["round_id"] == payload.get("round_id")
                ),
                None,
            ) if packet else None
            _require(
                packet is not None and round_row is not None
                and payload.get("packet_digest") == packet["packet_digest"]
                and all(payload.get(key) == value for key, value in round_row.items())
                and ((round_row["result"] in {"mutated", "synthesized", "demoted"}
                      and bool(round_row["mutation_or_synthesis"]["changed_primitives_relations_or_explanation"]))
                     or (round_row["result"] == "no_change"
                         and bool(str(round_row.get("no_change_reason") or "").strip())
                         and not round_row["mutation_or_synthesis"]["changed_primitives_relations_or_explanation"])),
                "reflective-parent feedback does not equal a sealed material or explicit no-change reflection round",
            )
        elif operator_id in {"reflective-theory-synthesizer", "local-reflective-synthesizer"}:
            packet = next(
                (
                    row
                    for row in operator_payloads
                    if row.get("conceptual_systems")
                    == payload.get("conceptual_systems")
                    and row.get("reflection_rounds")
                    == payload.get("reflection_rounds")
                ),
                None,
            )
            _require(
                packet is not None
                and payload.get("component_system_ids")
                == [
                    system["system_id"]
                    for system in packet["conceptual_systems"]
                ]
                and payload.get("conceptual_systems")
                == packet["conceptual_systems"]
                and payload.get("reflection_rounds")
                == packet["reflection_rounds"],
                "reflective-synthesizer feedback does not bind the complete sealed candidate set",
            )
        elif operator_id == "blind-conceptual-preference-adjudicator":
            evidence = operator_payloads[0]
            _require(
                payload.get("stage_id") == evidence["stage_id"]
                and payload.get("evidence_id") == evidence["evidence_id"]
                and payload.get("evidence_digest") == evidence["evidence_digest"]
                and payload.get("preference_set") == evidence["preference_set"]
                and payload.get("conceptual_adjudication_evidence") == evidence,
                "conceptual-adjudication feedback does not equal the complete sealed evidence",
            )
        elif operator_id == "dynamic-symbolic-simulation-experimenter":
            experiment = operator_payloads[0]
            reflection = projection.get("experiment_reflection_receipt")
            _require(
                isinstance(reflection, Mapping)
                and payload.get("experiment_receipt_id") == experiment["receipt_id"]
                and payload.get("recommendations") == experiment["reflective_assimilation"]
                and payload.get("post_result_reflection_receipt_ids")
                == [reflection["reflection_receipt_id"]]
                and payload.get("post_result_reflection_digest")
                == reflection["reflection_digest"]
                and payload.get("typed_delta") == reflection["typed_delta"]
                and event.get("identity", {}).get("branch_id") == experiment["branch_id"],
                "experiment feedback does not exactly bind reflective assimilation",
            )
        elif operator_id == "formal-claim-producer":
            formal_claim_output = operator_payloads[0]
            _require(
                payload.get("kind") == "formal_claim_production"
                and payload.get("output_id")
                == formal_claim_output["output_id"]
                and payload.get("output_digest")
                == formal_claim_output["content_digest"]
                and payload.get("status") == formal_claim_output["status"]
                and payload.get("formal_claim_output") == formal_claim_output,
                "formal-claim feedback does not equal the sealed producer output",
            )
        if operator_id in KNOWN_FEEDBACK_OPERATOR_IDS:
            binding = bindings.setdefault(
                operator_id,
                {
                    "receipt_ids": [],
                    "request_ids": [],
                    "feedback_edge_ids": [],
                    "consumer_event_ids": [],
                    "producer_output_artifacts": [],
                    "semantic_roles": [],
                    "operator_evidence_digest": evidence_index["evidence_digest"],
                },
            )
            binding["receipt_ids"].append(edge["producer_receipt_id"])
            binding["request_ids"].append(edge["producer_request_id"])
            binding["feedback_edge_ids"].append(edge["feedback_edge_id"])
            binding["consumer_event_ids"].append(edge["consumer_event_id"])
            binding["producer_output_artifacts"].extend(
                edge["producer_output_artifacts"]
            )
            binding["semantic_roles"].append(expected_role)
    _require(edge_receipts == input_receipts,
             "every successful sealed receipt must have exactly one feedback-effective edge")
    required_operator_ids = (
        REQUIRED_THEORY_OPERATOR_IDS
        if projection.get("literature_basis", {}).get("mode")
        == "active_current"
        else LOCAL_REQUIRED_THEORY_OPERATOR_IDS
    )
    missing = required_operator_ids - bindings.keys()
    _require(not missing, f"required feedback-effective operators are missing: {sorted(missing)}")
    expected_cardinalities = {
        operator_id: (
            2
            if operator_id == "blind-conceptual-preference-adjudicator"
            else 1
        )
        for operator_id in required_operator_ids
    }
    _require(
        all(
            len(bindings[operator_id]["receipt_ids"]) == count
            for operator_id, count in expected_cardinalities.items()
        ),
        "required feedback-effective operator cardinalities are not exact",
    )
    for binding in bindings.values():
        for key in (
            "receipt_ids",
            "request_ids",
            "feedback_edge_ids",
            "consumer_event_ids",
            "semantic_roles",
        ):
            binding[key] = sorted(binding[key])
    return bindings


def _verify_formal_claim_schedule_join(
    projection: Mapping[str, Any],
    evidence_index: Mapping[str, Any],
    operator_bindings: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Independently reconstruct the producer-to-prove join from committed bytes."""

    outputs = evidence_index["role_payloads"].get("formal_claim_output", [])
    actions = [
        dict(action)
        for action in projection.get("schedule", {}).get("actions", [])
        if isinstance(action, Mapping)
    ]
    prove_actions = [action for action in actions if action.get("kind") == "prove"]
    bound_actions = [
        action
        for action in actions
        if isinstance(action.get("payload", {}).get("formal_claim_binding"), Mapping)
    ]
    if not outputs:
        _require(
            not prove_actions
            and not bound_actions
            and "formal-claim-producer" not in operator_bindings,
            "absent formal-claim output leaked a prove action or producer binding",
        )
        join = {
            "schema_version": 1,
            "join_kind": "gate_replayed_formal_claim_schedule",
            "status": "absent_no_prove",
            "output_id": None,
            "producer_receipt_id": None,
            "action_id": None,
            "binding_digest": None,
            "authority_nulls": {
                "claim_truth": False,
                "checker_soundness": False,
                "theorem_status": False,
                "physics_value": False,
            },
        }
        join["join_digest"] = canonical_digest(join)
        return join

    _require(len(outputs) == 1, "formal-claim role cardinality is not zero or one")
    output = validate_formal_claim_producer_output(outputs[0])
    producers = evidence_index["producers_by_role"].get(
        "formal_claim_output", []
    )
    _require(
        len(producers) == 1,
        "formal-claim output lacks one exact committed producer receipt",
    )
    receipt = producers[0]
    request = evidence_index["requests"].get(receipt["request_id"])
    inputs = evidence_index["input_payloads"].get(receipt["request_id"], [])
    _require(
        isinstance(request, Mapping)
        and len(inputs) == 1
        and receipt.get("operator", {}).get("operator_id")
        == "formal-claim-producer"
        and receipt.get("status") == "succeeded",
        "formal-claim producer request, receipt, or input is not exact",
    )
    artifact_bytes = evidence_index["artifact_bytes_by_original_path"]

    def load_committed_artifact(relative_path: str) -> bytes:
        data = artifact_bytes.get(relative_path)
        if type(data) is not bytes:
            raise ContractError(
                "formal-claim gate replay requested an uncommitted artifact path"
            )
        return data

    producer_input = validate_formal_claim_producer_input_with_loader(
        inputs[0], loader=load_committed_artifact
    )
    _require(
        build_formal_claim_producer_output_with_loader(
            producer_input, loader=load_committed_artifact
        )
        == output,
        "formal-claim gate replay differs from the sealed producer output",
    )
    semantic_rows = semantic_output_rows("formal-claim-producer", output)
    _require(
        len(semantic_rows) == 1,
        "formal-claim output lacks one semantic producer row",
    )
    semantic_row = semantic_rows[0]
    event_candidates = [
        event
        for event in projection.get("events", [])
        if isinstance(event, Mapping)
        and event.get("event_type") == "reflection_recorded"
        and event.get("entity_id") == semantic_row["semantic_id"]
        and event.get("source_receipt_ids") == [receipt["receipt_id"]]
        and event.get("payload", {}).get("kind")
        == "formal_claim_production"
    ]
    _require(
        len(event_candidates) == 1,
        "formal-claim producer does not bind one exact semantic event",
    )
    event = event_candidates[0]
    event_payload = event["payload"]
    semantic_projection = event_payload.get("semantic_projection", {})
    feedback_binding = operator_bindings.get("formal-claim-producer")
    _require(
        isinstance(feedback_binding, Mapping)
        and feedback_binding.get("receipt_ids") == [receipt["receipt_id"]]
        and feedback_binding.get("request_ids") == [request["request_id"]]
        and feedback_binding.get("consumer_event_ids") == [event["event_id"]]
        and feedback_binding.get("semantic_roles") == ["formal_claim_output"]
        and event_payload.get("output_id") == output["output_id"]
        and event_payload.get("output_digest") == output["content_digest"]
        and event_payload.get("status") == output["status"]
        and event_payload.get("formal_claim_output") == output
        and semantic_projection.get("semantic_kind")
        == semantic_row["semantic_kind"]
        and semantic_projection.get("semantic_id") == semantic_row["semantic_id"]
        and semantic_projection.get("row_digest") == semantic_row["row_digest"],
        "formal-claim feedback lineage differs from its exact committed producer join",
    )

    if output["status"] == "not_ready":
        _require(
            not prove_actions and not bound_actions,
            "not-ready formal-claim output leaked a prove action",
        )
        join = {
            "schema_version": 1,
            "join_kind": "gate_replayed_formal_claim_schedule",
            "status": "not_ready_no_prove",
            "output_id": output["output_id"],
            "producer_receipt_id": receipt["receipt_id"],
            "action_id": None,
            "binding_digest": None,
            "authority_nulls": {
                "claim_truth": False,
                "checker_soundness": False,
                "theorem_status": False,
                "physics_value": False,
            },
        }
        join["join_digest"] = canonical_digest(join)
        return join

    expected_binding = {
        "schema_version": 1,
        "binding_kind": "registered_formal_claim_prove_action",
        "producer_operator_id": "formal-claim-producer",
        "producer_request_id": request["request_id"],
        "producer_request_digest": request["request_digest"],
        "producer_receipt_id": receipt["receipt_id"],
        "producer_receipt_digest": receipt["receipt_digest"],
        "producer_input_digest": canonical_digest(producer_input),
        "consumer_event_id": event["event_id"],
        "consumer_event_hash": event["event_hash"],
        "semantic_row_id": semantic_row["semantic_id"],
        "semantic_row_digest": semantic_row["row_digest"],
        "output_id": output["output_id"],
        "output_digest": output["content_digest"],
        "source_theory_generation": output["source_theory_generation"],
        "conjecture_id": output["conjecture_id"],
        "formal_claim_digest": output["formal_claim_digest"],
        "execution_plan_digest": output["execution_plan_digest"],
    }
    validate_instance(
        expected_binding,
        "discovery_formal_claim_schedule_binding_v1.schema.json",
    )
    _require(
        len(prove_actions) == len(bound_actions) == 1
        and prove_actions[0] == bound_actions[0],
        "ready formal-claim output does not have exactly one bound prove action",
    )
    action = prove_actions[0]
    schedule_binding = action["payload"]["formal_claim_binding"]
    schedule_identity = next(
        (
            binding
            for binding in projection.get("schedule", {}).get(
                "identity_bindings", []
            )
            if binding.get("branch_id") == output["branch_id"]
        ),
        None,
    )
    _require(
        schedule_binding == expected_binding
        and action.get("status") == "pending"
        and not set(action.get("restrictions", [])).intersection(
            _INVESTMENT_BLOCKING_RESTRICTIONS
        )
        and action.get("branch_ids") == [output["branch_id"]]
        and output["source_theory_generation"]
        == projection["committed_state_version"]
        and output["branch_id"]
        in projection.get("parallel_outcome", {}).get("valid_branch_ids", [])
        and isinstance(schedule_identity, Mapping)
        and schedule_identity.get("hypothesis_id") == output["hypothesis_id"]
        and output["concept_id"] in schedule_identity.get("concept_ids", [])
        and set(output["conceptual_system_ids"]).issubset(
            schedule_identity.get("conceptual_system_ids", [])
        ),
        "ready formal-claim action differs from the independently replayed committed join",
    )
    join = {
        "schema_version": 1,
        "join_kind": "gate_replayed_formal_claim_schedule",
        "status": "ready_prove_pending",
        "output_id": output["output_id"],
        "producer_receipt_id": receipt["receipt_id"],
        "action_id": action["action_id"],
        "binding_digest": canonical_digest(expected_binding),
        "authority_nulls": {
            "claim_truth": False,
            "checker_soundness": False,
            "theorem_status": False,
            "physics_value": False,
        },
    }
    join["join_digest"] = canonical_digest(join)
    return join


def _verify_current_validator_bindings(
    evidence_index: Mapping[str, Any],
    approved_bindings: Mapping[str, OperatorBinding],
    *,
    repository_root: Path,
) -> None:
    """Resolve every sealed validator back to the current approved registry.

    Commit replay proves what bytes validated the historical attempt. This
    second check proves that those local semantic bytes still equal the modules
    and schemas approved by the current production registry. It is deliberately
    opt-in for generic fixture cycles and mandatory for release acceptance.
    """

    for receipt in evidence_index["receipts"].values():
        operator_id = str(receipt["operator"]["operator_id"])
        operator = approved_bindings.get(operator_id)
        _require(operator is not None, f"validator authority has no approved operator {operator_id}")
        _require(
            receipt["operator"].get("version") == operator.version
            and receipt["operator"].get("kind") == operator.kind,
            f"sealed operator binding differs from current registry for {operator_id}",
        )
        expected = {validator.validator_id: validator for validator in operator.validators}
        actual = {
            str(validator["validator_id"]): validator
            for validator in receipt["validator_receipts"]
        }
        _require(
            len(actual) == len(receipt["validator_receipts"]) and set(actual) == set(expected),
            f"sealed validator set differs from current registry for {operator_id}",
        )
        for validator_id, validator_receipt in actual.items():
            try:
                verify_current_validator_authority(
                    validator_receipt["validator_authority"],
                    expected[validator_id],
                    repository_root=repository_root,
                )
            except ContractError as exc:
                raise ContractError(
                    "canonical theory gate rejected projection: "
                    f"current validator authority failed for {operator_id}/{validator_id}: {exc}"
                ) from exc


def _derive_schedule_authorization(
    projection: Mapping[str, Any], committed_state: Mapping[str, Any]
) -> dict[str, Any]:
    """Intersect committed state genealogy, scheduler identity, and positive actions."""

    identity_map = projection.get("identity_map", {})
    schedule = projection.get("schedule", {})
    _require(isinstance(identity_map, Mapping), "identity_map must be an object")
    _require(isinstance(schedule, Mapping), "schedule must be an object")
    _require(schedule.get("schedule_id") == projection.get("schedule_id"), "schedule ID mismatch")
    _require(schedule.get("target_id") == projection.get("target_id"), "schedule target mismatch")
    _require(
        schedule.get("state_version") == projection.get("prior_state_version"),
        "schedule is not bound to the cycle's frozen prior state",
    )
    active_literature = (
        projection.get("literature_basis", {}).get("mode") == "active_current"
    )
    _require(
        schedule.get("literature_investment_blocked")
        is (not active_literature),
        "schedule literature-investment boundary differs from literature mode",
    )
    claimed_schedule_digest = schedule.get("schedule_digest")
    _require(
        claimed_schedule_digest
        == canonical_digest(
            schedule,
            exclude_keys=("schedule_digest", "created_at", "consumption_log"),
        ),
        "schedule digest is invalid",
    )
    _require(not schedule.get("consumption_log"), "source theory schedule was already consumed")
    _require(
        committed_state.get("current_literature_snapshot_id")
        == projection.get("literature_basis", {}).get("snapshot_id"),
        "schedule literature ID is not the current reduced-state snapshot",
    )
    state_snapshot = committed_state.get("literature_snapshots", {}).get(
        projection.get("literature_basis", {}).get("snapshot_id")
    )
    _require(
        isinstance(state_snapshot, Mapping)
        and state_snapshot.get("content_digest")
        == projection.get("literature_basis", {}).get("snapshot_digest")
        and state_snapshot.get("investment_gate")
        == (
            "active_current"
            if active_literature
            else "local_only_incubation"
        ),
        "schedule literature authority is not grounded in committed state",
    )

    branch_bindings = identity_map.get("branch_bindings", [])
    schedule_bindings = schedule.get("identity_bindings", [])
    _require(isinstance(branch_bindings, list) and branch_bindings, "canonical branch bindings are absent")
    _require(isinstance(schedule_bindings, list) and schedule_bindings, "schedule identity bindings are absent")
    by_branch: dict[str, Mapping[str, Any]] = {}
    for binding in branch_bindings:
        _require(isinstance(binding, Mapping), "canonical branch binding is malformed")
        branch_id = str(binding.get("branch_id", ""))
        _require(branch_id and branch_id not in by_branch, "canonical branch IDs are empty or duplicated")
        by_branch[branch_id] = binding
    scheduled_bindings: dict[str, Mapping[str, Any]] = {}
    for binding in schedule_bindings:
        _require(isinstance(binding, Mapping), "schedule identity binding is malformed")
        branch_id = str(binding.get("branch_id", ""))
        _require(branch_id and branch_id not in scheduled_bindings, "schedule branch IDs are empty or duplicated")
        scheduled_bindings[branch_id] = binding
    _require(set(by_branch) == set(scheduled_bindings), "schedule and canonical branch identities differ")
    for branch_id, binding in by_branch.items():
        _require(
            canonical_digest(binding) == canonical_digest(scheduled_bindings[branch_id]),
            f"schedule remapped canonical branch {branch_id}",
        )
        state_branch = committed_state.get("branches", {}).get(branch_id)
        hypothesis_id = str(binding.get("hypothesis_id", ""))
        concept_ids = list(binding.get("concept_ids", []))
        system_ids = list(binding.get("conceptual_system_ids", []))
        state_hypothesis = committed_state.get("hypotheses", {}).get(hypothesis_id)
        _require(
            isinstance(state_branch, Mapping)
            and state_branch.get("hypothesis_id") == hypothesis_id
            and state_branch.get("concept_ids") == concept_ids,
            f"canonical branch binding {branch_id} is absent or remapped in reduced state",
        )
        _require(
            isinstance(state_hypothesis, Mapping)
            and state_hypothesis.get("concept_ids") == concept_ids,
            f"canonical hypothesis binding {hypothesis_id} is absent or remapped in reduced state",
        )
        for concept_id in concept_ids:
            concept = committed_state.get("concepts", {}).get(concept_id)
            _require(
                isinstance(concept, Mapping)
                and hypothesis_id in concept.get("hypothesis_ids", []),
                f"concept {concept_id} does not ground hypothesis {hypothesis_id}",
            )
        for system_id in system_ids:
            system = committed_state.get("conceptual_systems", {}).get(system_id)
            _require(
                isinstance(system, Mapping)
                and hypothesis_id in system.get("hypothesis_ids", [])
                and set(concept_ids).issubset(system.get("concept_ids", [])),
                f"conceptual system {system_id} does not ground branch {branch_id}",
            )

    identity_sets = {
        "concept_ids": "concepts",
        "hypothesis_ids": "hypotheses",
        "branch_ids": "branches",
        "conceptual_system_ids": "conceptual_systems",
        "proof_obligation_ids": "proof_obligations",
    }
    for identity_field, state_table in identity_sets.items():
        values = list(identity_map.get(identity_field, []))
        _require(len(values) == len(set(values)), f"identity map duplicates {identity_field}")
        table = committed_state.get(state_table, {})
        _require(set(values).issubset(table), f"identity map {identity_field} is not grounded in reduced state")

    valid_parallel = set(projection.get("parallel_outcome", {}).get("valid_branch_ids", []))
    action_ids_by_branch: dict[str, list[str]] = {}
    action_kinds_by_branch: dict[str, list[str]] = {}
    actions = schedule.get("actions", [])
    _require(isinstance(actions, list), "schedule actions must be a list")
    action_ids: set[str] = set()
    for action in actions:
        _require(isinstance(action, Mapping), "schedule action is malformed")
        action_id = str(action.get("action_id", ""))
        _require(action_id and action_id not in action_ids, "schedule action IDs are empty or duplicated")
        action_ids.add(action_id)
        _require(
            action.get("target_id") == projection.get("target_id")
            and action.get("state_version") == projection.get("prior_state_version"),
            f"schedule action {action_id} crossed target/state identity",
        )
        expected_action_id = stable_identifier(
            "action",
            {
                "kind": action.get("kind"),
                "target_id": action.get("target_id"),
                "state_version": action.get("state_version"),
                "branch_ids": sorted(set(action.get("branch_ids", []))),
                "depends_on": sorted(set(action.get("depends_on", []))),
                "payload": action.get("payload", {}),
            },
        )
        _require(action_id == expected_action_id, f"schedule action ID is not content-derived: {action_id}")
        _require(set(action.get("branch_ids", [])).issubset(by_branch),
                 f"schedule action {action_id} names an unbound branch")
        if action.get("kind") not in AUTHORIZED_BRANCH_ACTION_KINDS:
            continue
        if not active_literature:
            continue
        if action.get("status") != "pending":
            continue
        restrictions = set(action.get("restrictions", []))
        if restrictions & _INVESTMENT_BLOCKING_RESTRICTIONS:
            continue
        for branch_id in action.get("branch_ids", []):
            branch_id = str(branch_id)
            if branch_id not in by_branch or branch_id not in valid_parallel:
                continue
            action_ids_by_branch.setdefault(branch_id, []).append(str(action["action_id"]))
            action_kinds_by_branch.setdefault(branch_id, []).append(str(action["kind"]))
    eligible = sorted(action_ids_by_branch)
    preference_authorized = (
        projection.get("conceptual_authority", {}).get(
            "preference_authorized"
        )
        is True
    )
    if preference_authorized:
        _require(
            eligible,
            "no branch survives canonical binding and schedule authorization",
        )
    else:
        _require(
            not eligible,
            "a diagnostic-only conceptual outcome leaked branch investment authority",
        )
    for branch_id in eligible:
        _require(
            branch_id in valid_parallel
            and bool(by_branch[branch_id].get("conceptual_system_ids"))
            and committed_state["branches"][branch_id].get("status") == "validated"
            and bool(committed_state["branches"][branch_id].get("validated_attempts")),
            f"eligible branch {branch_id} lacks a validated state/attempt/system grounding",
        )
    return {
        "eligible_branch_ids": eligible,
        "action_ids_by_branch": {
            branch_id: sorted(set(action_ids_by_branch[branch_id])) for branch_id in eligible
        },
        "action_kinds_by_branch": {
            branch_id: sorted(set(action_kinds_by_branch[branch_id])) for branch_id in eligible
        },
        "investment_authorized": preference_authorized and bool(eligible),
        "authorization_semantics": (
            "branch_id must occur in identical canonical/schedule identity bindings, in a validated "
            "parallel result, and in at least one pending positive theory action without an "
            "investment-blocking restriction"
        ),
    }


def _theory_subordinate_support_projection(
    replay: Mapping[str, Any],
    *,
    committed_generation: int,
    committed_state: Mapping[str, Any],
) -> dict[str, Any]:
    """Compress an exact N+1..N+7 replay without importing experiment authority.

    The full commission, requests, observations, producer evidence, and
    certificate remain in their immutable commits.  A theory authorization
    carries only portable commit references, the one next-cycle reflection
    request, and the certificate's explicit denials.  None of these fields can
    alter the theory commit, schedule, ontology, branch eligibility, or proof
    status established at generation ``N``.
    """

    anchor = replay.get("anchor_transition")
    anchor_reference = replay.get("anchor_reference")
    observations = replay.get("observation_references")
    aggregation_reference = replay.get("aggregation_reference")
    certificate = replay.get("certificate")
    _require(
        isinstance(anchor, Mapping)
        and isinstance(anchor_reference, Mapping)
        and isinstance(observations, list)
        and len(observations) == len(WORLD_IDS)
        and isinstance(aggregation_reference, Mapping)
        and isinstance(certificate, Mapping),
        "support replay is not one complete anchor/five-world/aggregation chain",
    )
    expected_generations = list(
        range(committed_generation + 2, committed_generation + 2 + len(WORLD_IDS))
    )
    theory_projection = copy.deepcopy(dict(committed_state))
    theory_projection.pop("generation", None)
    frozen_theory_digest = canonical_digest(theory_projection)
    _require(
        anchor.get("prior_generation") == committed_generation
        and anchor_reference.get("generation") == committed_generation + 1
        and [row.get("generation") for row in observations]
        == expected_generations
        and aggregation_reference.get("generation") == committed_generation + 7
        and anchor.get("frozen_theory_state_projection_digest")
        == frozen_theory_digest
        and aggregation_reference.get("frozen_theory_state_projection_digest")
        == frozen_theory_digest,
        "support chain is not the exact generation-only N+1 through N+7 suffix of the theory commit",
    )
    denials = copy.deepcopy(dict(certificate.get("derived_denials", {})))
    _require(
        denials
        and all(value is False for value in denials.values()),
        "support certificate lacks complete negative theory/proof/physics authority",
    )
    support: dict[str, Any] = {
        "schema_version": "1.0.0",
        "evidence_kind": "canonical_five_world_theory_subordinate_support",
        "authority_status": replay.get("authority_status"),
        "theory_commit_generation": committed_generation,
        "support_head_generation": aggregation_reference["generation"],
        "anchor_reference": copy.deepcopy(dict(anchor_reference)),
        "observation_references": copy.deepcopy(observations),
        "aggregation_reference": copy.deepcopy(dict(aggregation_reference)),
        "certificate_id": certificate["certificate_id"],
        "certificate_digest": certificate["certificate_digest"],
        "pending_next_cycle_reflection": copy.deepcopy(
            certificate["pending_review"]
        ),
        "derived_denials": denials,
        "theory_state_projection_digest": frozen_theory_digest,
        "theory_selected": False,
        "current_cycle_theory_mutation_authorized": False,
        "schedule_mutation_authorized": False,
        "proof_authorized": False,
        "physical_target_support_authorized": False,
        "authority_boundary": (
            "secondary support over immutable theory N; only the typed N+7 "
            "pending-next-cycle reflection request may be consumed"
        ),
    }
    support["support_evidence_digest"] = canonical_digest(support)
    return support


def verify_canonical_theory_cycle(
    projection_path: Path | str,
    *,
    target_id: str,
    run_id: str,
    state_root: Path | str = DEFAULT_CANONICAL_THEORY_STATE_ROOT,
    previous_lineage: Mapping[str, Any] | None = None,
    require_current: bool = True,
    clock_authority_id: str = SYSTEM_UTC_CLOCK_AUTHORITY_ID,
    approved_operator_bindings: Mapping[str, OperatorBinding] | None = None,
    authority_repository_root: Path | str | None = None,
    support_anchor_reference: Mapping[str, Any] | None = None,
) -> VerifiedTheoryAuthorization:
    """Return a JSON-ready branch authorization for one exact current commit.

    ``previous_lineage`` is optional for first adoption.  Once a compatibility
    runtime records a canonical generation, the next projection must start from
    exactly that generation and use the same transaction root.  This prevents a
    legacy runner from reusing or silently switching theory histories.
    ``support_anchor_reference`` optionally names the sole canonical
    generation-only support suffix: anchor N+1, five ordered observations
    N+2..N+6, and aggregation N+7.  The suffix may expose only a later
    reflection request; it never contributes to branch eligibility or the
    theory state. ``require_current=False`` returns a typed historical-replay record that
    cannot authorize investment.  Live callers may select only a registered
    clock authority; they cannot inject an instant or callback, and projection
    timestamps never substitute for the governed clock.  Release callers pass
    ``approved_operator_bindings`` so validator modules and schemas are re-hashed
    against the current checkout, not merely replayed from snapshots.
    """

    path = Path(projection_path).resolve()
    _require(path.is_file(), "canonical cycle projection path does not exist")
    _require(
        not any(part.lower() in _MUTABLE_PROJECTION_NAMES for part in path.parts),
        "mutable latest/current projection aliases are forbidden",
    )
    try:
        projection_bytes = path.read_bytes()
        projection = json.loads(projection_bytes)
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(
            f"canonical theory gate result projection is unreadable: {path}: {exc}"
        ) from exc
    _require(isinstance(projection, dict), "result projection is not a JSON object")
    projection_digest = bytes_digest(projection_bytes)
    validate_instance(projection, "canonical_discovery_cycle.schema.json")
    _require(projection.get("target_id") == target_id, "target identity mismatch")
    _require(projection.get("run_id") == run_id, "run identity mismatch")
    prior_generation = projection.get("prior_state_version")
    committed_generation = projection.get("committed_state_version")
    _require(
        projection.get("next_state_version") == committed_generation
        and committed_generation == prior_generation + 1,
        "state generations are not one contiguous canonical transition",
    )

    resolved_state_root = Path(state_root).resolve()
    _require(
        resolved_state_root not in _FORBIDDEN_COMPATIBILITY_ROOTS,
        "canonical theory verification cannot use a legacy compatibility transaction root",
    )
    store = DiscoveryTransactionStore(resolved_state_root, target_id=target_id, run_id=run_id)
    current_generation = store.current_generation()
    support_replay: dict[str, Any] | None = None
    transaction_head_generation = committed_generation
    if support_anchor_reference is not None:
        _require(
            isinstance(support_anchor_reference, Mapping),
            "support anchor reference must be one typed portable mapping",
        )
        support_replay = (
            require_active_canonical_world_matrix_commit_chain(
                store=store,
                anchor_reference=support_anchor_reference,
            )
            if require_current
            else replay_canonical_world_matrix_commit_chain(
                store=store,
                anchor_reference=support_anchor_reference,
            )
        )
        aggregation_reference = support_replay.get("aggregation_reference")
        _require(
            support_replay.get("status") == "complete"
            and isinstance(aggregation_reference, Mapping),
            "support anchor does not resolve to a complete seven-transition chain",
        )
        transaction_head_generation = aggregation_reference.get("generation")
    if require_current:
        _require(
            current_generation == transaction_head_generation,
            "theory projection is stale unless the current head is either its "
            "own commit or its exact generation-only N+7 support aggregation",
        )
    committed_state = store.read_state(committed_generation)
    _require(committed_state is not None, "committed canonical state is unreadable")
    _require(canonical_digest(committed_state) == projection.get("state_digest"), "state digest mismatch")
    support_evidence = (
        _theory_subordinate_support_projection(
            support_replay,
            committed_generation=committed_generation,
            committed_state=committed_state,
        )
        if support_replay is not None
        else None
    )
    prior_state = (
        store.read_state(prior_generation)
        if prior_generation
        else initial_state(target_id, run_id)
    )
    _require(prior_state is not None, "prior canonical state is unreadable")
    commit_path, manifest = _resolve_commit(
        store,
        generation=committed_generation,
        commit_id=str(projection.get("commit_id")),
    )
    manifest_path = commit_path / "manifest.json"
    _require(file_digest(manifest_path) == projection.get("manifest_digest"), "manifest digest mismatch")
    _require(
        manifest.get("target_id") == target_id
        and manifest.get("run_id") == run_id
        and manifest.get("prior_generation") == prior_generation
        and manifest.get("generation") == committed_generation,
        "manifest target/run/state lineage mismatch",
    )
    _require(
        manifest.get("state_semantic_digest") == projection.get("state_digest"),
        "manifest and projection state digests differ",
    )
    _assert_projection_paths(
        projection,
        projection_path=path,
        state_root=resolved_state_root,
        commit_path=commit_path,
        manifest_path=manifest_path,
    )
    committed = _verify_committed_artifacts(
        projection, commit_path=commit_path, manifest=manifest
    )
    events = projection.get("events", [])
    validate_event_chain(
        events,
        first_sequence=int(prior_state.get("event_count", 0)) + 1,
        previous_hash=str(prior_state.get("last_event_hash")),
    )
    _require(
        committed_state.get("event_count")
        == int(prior_state.get("event_count", 0)) + len(events),
        "committed event count does not extend the prior ledger by this suffix",
    )
    _require(
        committed_state.get("last_event_hash")
        == (events[-1]["event_hash"] if events else prior_state.get("last_event_hash")),
        "committed state does not terminate at the projected event suffix",
    )
    replayed_state = reduce_from_state(prior_state, events)
    _require(
        canonical_digest(replayed_state) == canonical_digest(committed_state)
        and replayed_state == committed_state,
        "committed canonical state is not the exact deterministic reducer replay",
    )

    evidence_index = _verify_operator_evidence(
        projection, committed=committed, commit_path=commit_path
    )
    committed_literature = load_committed_cycle_literature_input(
        store,
        committed_generation,
    )
    verified_literature_commit = committed_literature.verified_commit
    sealed_literature_bundle = evidence_index["role_payloads"][
        "literature_production_input_bundle"
    ][0]
    literature_bundle = committed_literature.bundle
    literature_input_projection = literature_bundle[
        "semantic_consumer_projection"
    ]
    literature_input_summary = projection.get("literature_production_input", {})
    _require(
        verified_literature_commit.commit_id == projection.get("commit_id")
        and verified_literature_commit.generation == committed_generation
        and verified_literature_commit.prior_generation == prior_generation
        and verified_literature_commit.manifest_digest
        == projection.get("manifest_digest")
        and verified_literature_commit.state_semantic_digest
        == projection.get("state_digest"),
        "literature-production input was not reopened from the projected VerifiedCommit",
    )
    _require(
        sealed_literature_bundle == literature_bundle,
        "operator evidence literature bundle differs from its committed projection copy",
    )
    _require(
        literature_input_summary.get("bundle_id")
        == literature_bundle.get("bundle_id")
        and literature_input_summary.get("bundle_digest")
        == literature_bundle.get("bundle_digest")
        and literature_input_summary.get("production_manifest_descriptor")
        == literature_bundle.get("production_manifest_descriptor")
        and literature_input_summary.get("commitment_receipt_id")
        == literature_bundle.get("commitment_receipt", {}).get("receipt_id")
        and literature_input_summary.get("commitment_receipt_digest")
        == literature_bundle.get("commitment_receipt", {}).get("receipt_digest")
        and literature_input_summary.get("semantic_projection_digest")
        == literature_input_projection.get("projection_digest")
        and literature_input_summary.get("authority_nulls")
        == literature_input_projection.get("authority_nulls")
        and projection.get("literature_production_projection_digest")
        == literature_input_projection.get("projection_digest"),
        "cycle literature-production summary differs from exact committed bundle bytes",
    )
    literature_verification = _verify_assimilated_literature_authority(
        projection.get("literature_basis", {}),
        evidence_index=evidence_index,
        manifest=manifest,
        require_current=require_current,
        clock_authority_id=clock_authority_id,
    )
    if approved_operator_bindings is not None:
        _verify_current_validator_bindings(
            evidence_index,
            approved_operator_bindings,
            repository_root=(
                Path(authority_repository_root).resolve()
                if authority_repository_root is not None
                else Path(__file__).resolve().parents[2]
            ),
        )
    reflective_packets = evidence_index["role_payloads"]["reflective_packets"]
    evaluations = committed["evaluations"].get("receipts", [])
    evaluation_bindings = committed["evaluations"].get(
        "candidate_identity_bindings", []
    )
    _require(
        evaluations == [] and evaluation_bindings == [],
        "legacy singular conceptual evaluations cannot coexist with sealed set-valued authority",
    )
    role_payloads = evidence_index["role_payloads"]
    parent_evidence = role_payloads.get("parent_conceptual_adjudication", [None])[0]
    synthesis_evidence = role_payloads.get(
        "synthesis_conceptual_adjudication", [None]
    )[0]
    expected_conceptual_authority = derive_conceptual_authority(
        target_id=target_id,
        run_id=run_id,
        state_version=prior_generation,
        literature_mode=str(projection["literature_basis"]["mode"]),
        parent_packet=reflective_packets[0],
        synthesis_packet=reflective_packets[1],
        parent_evidence=parent_evidence,
        synthesis_evidence=synthesis_evidence,
        proof_ready=projection.get("proof_handoff") is not None,
    )
    _require(
        projection.get("conceptual_authority") == expected_conceptual_authority,
        "conceptual authority does not equal the complete sealed set-valued evidence replay",
    )
    operator_bindings = _verify_feedback_lineage(projection, evidence_index)
    formal_claim_schedule_join = _verify_formal_claim_schedule_join(
        projection,
        evidence_index,
        operator_bindings,
    )
    schedule_authorization = _derive_schedule_authorization(projection, committed_state)
    source_authority_pair = literature_verification["source_authority_pair"]
    active_literature = projection["literature_basis"]["mode"] == "active_current"
    if active_literature:
        _require(
            isinstance(source_authority_pair, Mapping),
            "active literature lacks its sealed source authority pair",
        )
        routing_policy = source_authority_pair["pre_map_policy"]
        routing_realization = source_authority_pair["realization"]
        _require(
            projection.get("source_routing_pre_map_policy") == routing_policy
            and projection.get("source_routing_pre_map_policy_digest")
            == routing_policy["policy_digest"]
            and projection.get("source_routing_realization") == routing_realization
            and projection.get("source_routing_realization_digest")
            == routing_realization["realization_digest"],
            "cycle projection does not equal the sealed source-routing authority pair",
        )
        _require(
            projection["schedule"].get("source_routing_pre_map_policy_id")
            == routing_policy["policy_id"]
            and projection["schedule"].get("source_routing_pre_map_policy_digest")
            == routing_policy["policy_digest"]
            and projection["schedule"].get("source_routing_realization_id")
            == routing_realization["realization_id"]
            and projection["schedule"].get("source_routing_realization_digest")
            == routing_realization["realization_digest"],
            "canonical schedule does not consume the exact source-routing authority pair",
        )
    else:
        routing_policy = None
        routing_realization = None
        _require(
            source_authority_pair is None
            and projection.get("source_routing_pre_map_policy") is None
            and projection.get("source_routing_pre_map_policy_digest") is None
            and projection.get("source_routing_realization") is None
            and projection.get("source_routing_realization_digest") is None
            and all(
                projection["schedule"].get(field) is None
                for field in (
                    "source_routing_pre_map_policy_id",
                    "source_routing_pre_map_policy_digest",
                    "source_routing_realization_id",
                    "source_routing_realization_digest",
                )
            ),
            "local incubation fabricated source-routing authority",
        )

    prior = dict(previous_lineage or {})
    if prior:
        _require(prior.get("target_id") == target_id, "previous lineage target mismatch")
        _require(prior.get("run_id") == run_id, "previous lineage run mismatch")
        _require(
            Path(str(prior.get("transaction_root", ""))).resolve() == resolved_state_root,
            "canonical transaction root changed across compatibility cycles",
        )
        _require(
            prior.get(
                "transaction_head_generation",
                prior.get("committed_state_version"),
            )
            == prior_generation,
            "projection does not continue the previously consumed canonical generation",
        )
        _require(
            prior.get("commit_id") != projection.get("commit_id"),
            "canonical cycle projection was already consumed",
        )

    literature_authority = literature_verification["immutable_basis"]
    literature_authority_basis_digest = literature_verification[
        "immutable_basis_digest"
    ]
    authorization_basis = {
        "schema_version": "1.0.0",
        "basis_kind": "immutable_canonical_theory_commit",
        "target_id": target_id,
        "run_id": run_id,
        "cycle_id": projection["cycle_id"],
        "prior_state_version": prior_generation,
        "committed_state_version": committed_generation,
        "transaction_head_generation": transaction_head_generation,
        "commit_id": projection["commit_id"],
        "manifest_digest": projection["manifest_digest"],
        "projection_digest": projection_digest,
        "literature_authority_basis_digest": literature_authority_basis_digest,
        "literature_production_projection_digest": projection[
            "literature_production_projection_digest"
        ],
        "source_routing_pre_map_policy_digest": (
            routing_policy["policy_digest"]
            if routing_policy is not None
            else None
        ),
        "source_routing_realization_digest": (
            routing_realization["realization_digest"]
            if routing_realization is not None
            else None
        ),
        "schedule_id": projection["schedule_id"],
        "schedule_digest": projection["schedule"]["schedule_digest"],
        "schedule_eligibility_derivation_digest": canonical_digest(
            schedule_authorization
        ),
        "proof_handoff_digest": (
            canonical_digest(projection["proof_handoff"])
            if projection.get("proof_handoff") is not None
            else None
        ),
        "operator_evidence_digest": projection["operator_evidence_digest"],
        "conceptual_authority_digest": canonical_digest(
            projection["conceptual_authority"]
        ),
        "operator_bindings_digest": canonical_digest(operator_bindings),
        "formal_claim_schedule_join_digest": formal_claim_schedule_join[
            "join_digest"
        ],
        "theory_subordinate_support_evidence_digest": (
            support_evidence["support_evidence_digest"]
            if support_evidence is not None
            else None
        ),
    }
    authorization_basis_digest = canonical_digest(authorization_basis)
    investment_authorized = (
        require_current
        and schedule_authorization["investment_authorized"] is True
    )
    present_evaluation = literature_verification["present_evaluation"]
    present_decision = None
    present_decision_digest = None
    if present_evaluation is not None:
        present_decision = {
            "schema_version": "1.0.0",
            "decision_kind": (
                "ephemeral_present_investment"
                if investment_authorized
                else "ephemeral_present_noninvestment"
            ),
            "authorization_basis_digest": authorization_basis_digest,
            "literature_authority_basis_digest": literature_authority_basis_digest,
            **present_evaluation,
            "status": (
                "authorized_current"
                if investment_authorized
                else "withheld_no_conceptual_preference"
            ),
            "authoritative": investment_authorized,
        }
        present_decision_digest = canonical_digest(present_decision)

    if require_current:
        eligibility_projection = schedule_authorization
    else:
        eligibility_projection = {
            "historical_investment_eligibility": "not_authorized",
            "counterfactual_eligible_branch_ids": schedule_authorization[
                "eligible_branch_ids"
            ],
            "counterfactual_action_ids_by_branch": schedule_authorization[
                "action_ids_by_branch"
            ],
            "counterfactual_action_kinds_by_branch": schedule_authorization[
                "action_kinds_by_branch"
            ],
            "counterfactual_investment_authorized": schedule_authorization[
                "investment_authorized"
            ],
            "counterfactual_authorization_semantics": schedule_authorization[
                "authorization_semantics"
            ],
        }

    authorization_payload = {
        "schema_version": "1.0.0",
        "status": (
            "verified_active_current"
            if investment_authorized
            else "verified_active_current_no_investment"
            if require_current and active_literature
            else "verified_local_incubation"
            if require_current
            else "verified_historical_replay"
        ),
        "authoritative": investment_authorized,
        "verification_scope": (
            "present_investment"
            if investment_authorized
            else "present_theory_replay_no_investment"
            if require_current and active_literature
            else "local_incubation_replay_no_investment"
            if require_current
            else "historical_replay_only"
        ),
        "target_id": target_id,
        "run_id": run_id,
        "cycle_id": projection["cycle_id"],
        "prior_state_version": prior_generation,
        "committed_state_version": committed_generation,
        "transaction_head_generation": transaction_head_generation,
        "commit_id": projection["commit_id"],
        "manifest_digest": projection["manifest_digest"],
        "transaction_root": str(resolved_state_root),
        "commit_path": str(commit_path.resolve()),
        "manifest_path": str(manifest_path.resolve()),
        "projection_path": str(path),
        "projection_digest": projection_digest,
        **literature_authority,
        "literature_authority_basis": literature_authority,
        "literature_authority_basis_digest": literature_authority_basis_digest,
        "literature_production_input": copy.deepcopy(
            projection["literature_production_input"]
        ),
        "literature_production_projection_digest": projection[
            "literature_production_projection_digest"
        ],
        "authorization_basis": authorization_basis,
        "authorization_basis_digest": authorization_basis_digest,
        "present_investment_decision": present_decision,
        "present_investment_decision_digest": present_decision_digest,
        "literature_present_use_evaluated_at": (
            present_decision["evaluated_at"] if present_decision else None
        ),
        "literature_present_use_reason": (
            present_decision["reason"]
            if present_decision
            else projection["literature_basis"]["present_use_reason"]
            if not active_literature
            else "not_evaluated_historical_replay"
        ),
        "schedule_id": projection["schedule_id"],
        "schedule_digest": projection["schedule"]["schedule_digest"],
        "schedule": projection["schedule"],
        "proof_handoff": projection.get("proof_handoff"),
        "operator_evidence_digest": projection["operator_evidence_digest"],
        "conceptual_authority": projection["conceptual_authority"],
        "theory_subordinate_support_evidence": support_evidence,
        "theory_subordinate_support_evidence_digest": (
            support_evidence["support_evidence_digest"]
            if support_evidence is not None
            else None
        ),
        "operator_bindings": operator_bindings,
        "formal_claim_schedule_join": formal_claim_schedule_join,
        **eligibility_projection,
    }
    authorization_payload["authorization_digest"] = canonical_digest(
        authorization_payload
    )
    return _issue_verified_authorization(
        authorization_payload,
        present_investment_verified=investment_authorized,
        temporal_capability=literature_verification["temporal_capability"],
    )


def reserve_canonical_theory_actions(
    authorization: Mapping[str, Any],
    *,
    branch_ids: Sequence[str],
    consumer_receipt_id: str,
    consumer_scope: str = "legacy_marathon",
    proof_obligation_id: str | None = None,
) -> VerifiedTheoryAuthorization:
    """CAS-reserve the exact verified action set before compatibility investment."""

    authorization_payload, reservation_at, clock_authority = _validated_runtime_authorization(
        authorization,
        require_fresh=True,
    )
    _require(
        authorization_payload.get("status") == "verified_active_current"
        and authorization_payload.get("authoritative") is True,
        "action reservation requires active-current authority",
    )
    normalized_branches = sorted(set(str(branch_id) for branch_id in branch_ids))
    _require(normalized_branches and len(normalized_branches) == len(branch_ids),
             "action reservation requires non-empty unique branch IDs")
    eligible = set(
        authorization_payload.get("reserved_branch_ids", [])
        if authorization_payload.get("status") == "actions_reserved"
        else authorization_payload.get("eligible_branch_ids", [])
    )
    _require(set(normalized_branches).issubset(eligible),
             "action reservation names a branch outside canonical authority")
    conceptual_kinds = set(AUTHORIZED_BRANCH_ACTION_KINDS) - {"prove"}
    if consumer_scope in {"legacy_marathon", "outer_discovery"}:
        permitted = conceptual_kinds
        _require(proof_obligation_id is None,
                 "conceptual compatibility reservation cannot claim a proof obligation")
    elif consumer_scope == "outer_prove":
        permitted = {"prove"}
        handoff = authorization_payload.get("proof_handoff")
        _require(
            isinstance(handoff, Mapping)
            and len(normalized_branches) == 1
            and handoff.get("branch_id") == normalized_branches[0]
            and proof_obligation_id is not None
            and handoff.get("obligation_id") == proof_obligation_id,
            "outer prove reservation requires the exact committed branch/obligation handoff",
        )
    else:
        raise ContractError(
            f"canonical theory gate rejected projection: unknown reservation consumer scope {consumer_scope!r}"
        )
    action_ids: list[str] = []
    for branch_id in normalized_branches:
        kinds = set(authorization_payload.get("action_kinds_by_branch", {}).get(branch_id, []))
        ids = authorization_payload.get("action_ids_by_branch", {}).get(branch_id, [])
        selected_ids = [
            action_id
            for action_id in ids
            if next(
                (
                    action.get("kind")
                    for action in authorization_payload["schedule"]["actions"]
                    if action.get("action_id") == action_id
                ),
                None,
            ) in permitted
        ]
        _require(kinds.intersection(permitted) and selected_ids,
                 f"branch {branch_id} has no action of the permitted compatibility kind")
        action_ids.extend(selected_ids)
    action_ids = sorted(set(action_ids))
    state_root = Path(str(authorization_payload["transaction_root"])).resolve()
    _require(state_root not in _FORBIDDEN_COMPATIBILITY_ROOTS,
             "canonical action reservation cannot use a legacy transaction root")
    store = DiscoveryTransactionStore(
        state_root,
        target_id=str(authorization_payload["target_id"]),
        run_id=str(authorization_payload["run_id"]),
    )
    updated_schedule, result, reservation = reserve_actions_transaction(
        store,
        authorization_payload["schedule"],
        action_ids,
        expected_generation=int(
            authorization_payload.get(
                "transaction_head_generation",
                authorization_payload["committed_state_version"],
            )
        ),
        consumer_receipt_id=consumer_receipt_id,
        source_cycle_id=str(authorization_payload["cycle_id"]),
        source_commit_id=str(authorization_payload["commit_id"]),
        consume_before=str(authorization_payload["literature_consume_before"]),
        allowed_action_kinds=sorted(permitted),
        temporal_evaluation={
            "evaluated_at": reservation_at.isoformat().replace("+00:00", "Z"),
            "clock_authority": clock_authority,
            "clock_authority_digest": clock_authority["authority_digest"],
            "authentication_status": "governed_local_process_time_not_externally_authenticated",
        },
    )
    reserved_payload = copy.deepcopy(authorization_payload)
    reserved_payload.update(
        {
            "status": "actions_reserved",
            "source_commit_id": authorization_payload["commit_id"],
            "source_committed_state_version": authorization_payload["committed_state_version"],
            "source_transaction_head_generation": authorization_payload.get(
                "transaction_head_generation",
                authorization_payload["committed_state_version"],
            ),
            "committed_state_version": result.generation,
            "transaction_head_generation": result.generation,
            "commit_id": result.commit_id,
            "manifest_digest": result.manifest_digest,
            "commit_path": str(result.commit_path.resolve()),
            "manifest_path": str((result.commit_path / "manifest.json").resolve()),
            "reserved_branch_ids": normalized_branches,
            "reserved_action_ids": action_ids,
            "reservation_consumer_scope": consumer_scope,
            "proof_obligation_id": proof_obligation_id,
            "reservation": reservation,
            "reservation_digest": reservation["reservation_digest"],
            "schedule": updated_schedule,
        }
    )
    reservation_basis = {
        "schema_version": "1.0.0",
        "basis_kind": "immutable_canonical_action_reservation",
        "source_authorization_basis_digest": authorization_payload[
            "authorization_basis_digest"
        ],
        "reservation_digest": reservation["reservation_digest"],
        "reserved_commit_id": result.commit_id,
        "reserved_manifest_digest": result.manifest_digest,
        "reserved_state_generation": result.generation,
        "consumed_schedule_digest": updated_schedule["consumed_schedule_digest"],
        "reserved_branch_ids": normalized_branches,
        "reserved_action_ids": action_ids,
    }
    reservation_basis_digest = canonical_digest(reservation_basis)
    reserved_payload["reservation_authorization_basis"] = reservation_basis
    reserved_payload["reservation_authorization_basis_digest"] = reservation_basis_digest
    temporal_evaluation = reservation["temporal_evaluation"]
    reserved_payload["reservation_temporal_evaluation"] = temporal_evaluation
    reserved_payload["reservation_temporal_evaluation_digest"] = canonical_digest(
        temporal_evaluation
    )
    reserved_payload.pop("authorization_digest", None)
    reserved_payload["authorization_digest"] = canonical_digest(reserved_payload)
    return _issue_verified_authorization(
        reserved_payload,
        present_investment_verified=True,
        temporal_capability=authorization._temporal_capability,
    )


def filter_authorized_branches(
    branches: Sequence[Mapping[str, Any]], authorization: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """Return only legacy branches explicitly authorized by the theory schedule.

    The function fails closed when no exact branch ID intersects.  It never
    guesses from titles, prose hypotheses, lexical similarity, or target-wide
    membership because those would silently dissolve the canonical genealogy.
    """

    authorization_payload, _, _ = _validated_runtime_authorization(
        authorization,
        require_fresh=True,
    )
    _require(
        authorization_payload.get("status") in {"verified_active_current", "actions_reserved"}
        and authorization_payload.get("authoritative") is True,
        "branch filtering requires a verified active-current authorization",
    )
    _require(
        authorization_payload.get("target_id")
        and authorization_payload.get("run_id"),
        "branch filtering requires target/run-bound authority",
    )
    eligible = set(
        authorization_payload.get("reserved_branch_ids", [])
        if authorization_payload.get("status") == "actions_reserved"
        else authorization_payload.get("eligible_branch_ids", [])
    )
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for branch in branches:
        branch_id = str(branch.get("branch_id", ""))
        if branch_id not in eligible:
            continue
        if branch.get("target_id") is not None:
            _require(branch.get("target_id") == authorization_payload["target_id"],
                     f"legacy branch {branch_id!r} crossed target identity")
        if branch.get("run_id") is not None:
            _require(branch.get("run_id") == authorization_payload["run_id"],
                     f"legacy branch {branch_id!r} crossed run identity")
        _require(branch_id not in seen, f"legacy branch ID {branch_id!r} is duplicated")
        seen.add(branch_id)
        selected.append(dict(branch))
    _require(
        selected,
        "no legacy branch has an exact ID authorized by the canonical schedule; an explicit binding is required",
    )
    return selected


__all__ = [
    "AUTHORIZED_BRANCH_ACTION_KINDS",
    "DEFAULT_CANONICAL_THEORY_STATE_ROOT",
    "PROOF_RECOVERY_UTC_CLOCK_AUTHORITY_ID",
    "REQUIRED_THEORY_OPERATOR_IDS",
    "VerifiedTheoryAuthorization",
    "authorization_projection",
    "authorization_is_runtime_verified",
    "validate_authorization_at_use",
    "validate_authorization_at_use_with_temporal_evidence",
    "filter_authorized_branches",
    "read_proof_recovery_clock_evidence",
    "reserve_canonical_theory_actions",
    "verify_canonical_theory_cycle",
]
