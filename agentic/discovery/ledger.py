# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Immutable hash-chained epistemic ledger and deterministic theory reducer.

The ledger is the cumulative memory of discovery: concepts, theory systems,
transformations, literature corrections, branch attempts, evidence, and retired
routes are events rather than mutable prose.  ``EpistemicLedger`` protects append
order and idempotency; ``reduce_events`` derives the complete active constellation
without deleting genealogy, negative knowledge, or failed parallel attempts.
"""

from __future__ import annotations

import copy
import fcntl
import json
import os
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .conceptual_adjudication import validate_sealed_preference_authority
from .contracts import (
    ContractError,
    Namespace,
    canonical_digest,
    canonical_json,
    stable_identifier,
    utc_now,
    validate_instance,
)


GENESIS_HASH = "sha256:" + "0" * 64
REDUCER_VERSION = "1.0.0"

SYNTHESIS_AUTHORITY_NULLS = {
    "proof_authority": None,
    "empirical_authority": None,
    "external_validation_authority": None,
    "source_truth_authority": None,
    "theorem_authority": None,
    "mass_gap_authority": None,
    "physics_result_authority": None,
}
_FORBIDDEN_SYNTHESIS_AUTHORITY_FIELDS = frozenset(
    {
        "preferred_system_id",
        "preference_authority_evidence_id",
        "conceptual_adjudication_evidence_id",
        "conceptual_adjudication_evidence_digest",
        "unification_map",
        "preserved_differences",
    }
)


class LedgerIntegrityError(ContractError):
    """Raised when event order, hashing, identity, or idempotency is dishonest."""


def semantic_event_digest(event: Mapping[str, Any]) -> str:
    """Hash the epistemic meaning of an event, excluding transport metadata."""

    semantic = {
        "event_type": event["event_type"],
        "entity_type": event["entity_type"],
        "entity_id": event["entity_id"],
        "identity": event["identity"],
        "payload": event["payload"],
        "relations": event.get("relations", []),
        "source_receipt_ids": event.get("source_receipt_ids", []),
    }
    return canonical_digest(semantic)


def event_hash(event: Mapping[str, Any]) -> str:
    """Hash the complete ordered event while excluding its self-hash field."""

    return canonical_digest(event, exclude_keys=("event_hash",))


def build_event(
    *,
    sequence: int,
    previous_event_hash: str,
    namespace: Namespace,
    event_type: str,
    entity_type: str,
    entity_id: str,
    payload: Mapping[str, Any],
    actor: str,
    relations: Sequence[Mapping[str, Any]] = (),
    source_receipt_ids: Sequence[str] = (),
    occurred_at: str | None = None,
) -> dict[str, Any]:
    """Build a self-hashed event whose semantic key makes retry idempotent."""

    if sequence < 1:
        raise ContractError("ledger sequence starts at one")
    event: dict[str, Any] = {
        "schema_version": "1.0.0",
        "event_id": stable_identifier(
            "devent", namespace.as_dict(), event_type, entity_type, entity_id, payload
        ),
        "sequence": sequence,
        "previous_event_hash": previous_event_hash,
        "occurred_at": occurred_at or utc_now(),
        "actor": actor,
        "identity": namespace.as_dict(),
        "event_type": event_type,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "payload": dict(payload),
        "relations": [dict(relation) for relation in relations],
        "source_receipt_ids": list(source_receipt_ids),
    }
    event["deduplication_key"] = semantic_event_digest(event)
    event["event_hash"] = event_hash(event)
    validate_instance(event, "discovery_epistemic_event.schema.json")
    return event


def validate_event_chain(
    events: Sequence[Mapping[str, Any]],
    *,
    first_sequence: int = 1,
    previous_hash: str = GENESIS_HASH,
) -> None:
    """Prove sequence, hashes, semantic keys, identity, and state order.

    ``first_sequence`` and ``previous_hash`` permit verification of a suffix
    against a previously reduced state; the defaults retain full-log replay.
    """

    if first_sequence < 1:
        raise LedgerIntegrityError("event sequence starts at one")
    previous = previous_hash
    target_run: tuple[str, str] | None = None
    last_state_version = -1
    seen_ids: set[str] = set()
    seen_semantics: set[str] = set()
    for expected_sequence, event in enumerate(events, first_sequence):
        validate_instance(event, "discovery_epistemic_event.schema.json")
        if event["sequence"] != expected_sequence:
            raise LedgerIntegrityError(
                f"non-contiguous event sequence: expected {expected_sequence}, got {event['sequence']}"
            )
        if event["previous_event_hash"] != previous:
            raise LedgerIntegrityError(f"broken hash predecessor at sequence {expected_sequence}")
        if event["event_hash"] != event_hash(event):
            raise LedgerIntegrityError(f"event hash mismatch at sequence {expected_sequence}")
        if event["deduplication_key"] != semantic_event_digest(event):
            raise LedgerIntegrityError(f"semantic deduplication key mismatch at sequence {expected_sequence}")
        if event["event_id"] in seen_ids or event["deduplication_key"] in seen_semantics:
            raise LedgerIntegrityError(f"duplicate immutable event at sequence {expected_sequence}")
        seen_ids.add(event["event_id"])
        seen_semantics.add(event["deduplication_key"])
        namespace = Namespace.from_mapping(event["identity"])
        identity = (namespace.target_id, namespace.run_id)
        if target_run is None:
            target_run = identity
        elif identity != target_run:
            raise LedgerIntegrityError(f"cross-target/run event at sequence {expected_sequence}")
        if namespace.state_version < last_state_version:
            raise LedgerIntegrityError(f"state version regressed at sequence {expected_sequence}")
        last_state_version = namespace.state_version
        previous = event["event_hash"]


class EpistemicLedger:
    """Append JSONL events under an advisory cross-process lock with fsync."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock_path = path.with_suffix(path.suffix + ".lock")

    def read(self) -> list[dict[str, Any]]:
        """Read and verify the complete immutable chain."""

        if not self.path.exists():
            return []
        events: list[dict[str, Any]] = []
        for number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise LedgerIntegrityError(f"invalid ledger JSON at physical line {number}: {exc}") from exc
            if not isinstance(payload, dict):
                raise LedgerIntegrityError(f"ledger line {number} is not an object")
            events.append(payload)
        validate_event_chain(events)
        return events

    def append_semantic(
        self,
        *,
        namespace: Namespace,
        event_type: str,
        entity_type: str,
        entity_id: str,
        payload: Mapping[str, Any],
        actor: str,
        relations: Sequence[Mapping[str, Any]] = (),
        source_receipt_ids: Sequence[str] = (),
        occurred_at: str | None = None,
    ) -> tuple[dict[str, Any], bool]:
        """Append once, returning the original event on an equivalent retry."""

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+b") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            events = self.read()
            candidate = build_event(
                sequence=len(events) + 1,
                previous_event_hash=events[-1]["event_hash"] if events else GENESIS_HASH,
                namespace=namespace,
                event_type=event_type,
                entity_type=entity_type,
                entity_id=entity_id,
                payload=payload,
                actor=actor,
                relations=relations,
                source_receipt_ids=source_receipt_ids,
                occurred_at=occurred_at,
            )
            for existing in events:
                if existing["deduplication_key"] == candidate["deduplication_key"]:
                    return existing, False
            with self.path.open("ab", buffering=0) as stream:
                stream.write(canonical_json(candidate) + b"\n")
                os.fsync(stream.fileno())
            return candidate, True


def initial_state(target_id: str, run_id: str) -> dict[str, Any]:
    """Create the complete empty state shape consumed by the reducer."""

    return {
        "schema_version": "1.0.0",
        "reducer_version": REDUCER_VERSION,
        "target_id": target_id,
        "run_id": run_id,
        "generation": 0,
        "event_count": 0,
        "last_event_hash": GENESIS_HASH,
        "conceptual_systems": {},
        "concepts": {},
        "hypotheses": {},
        "evidence": {},
        "literature_snapshots": {},
        "branch_attempts": {},
        "branches": {},
        "transformations": {},
        "syntheses": {},
        "understanding_deltas": {},
        "relations": {},
        "retired_routes": {},
        "active_theory_constellation": [],
        "current_literature_snapshot_id": None,
        "stale_branches": [],
        "rebase_history": [],
        "deduplication_keys": [],
    }


def _append_unique(values: list[Any], item: Any) -> None:
    """Append a structured value only if canonical meaning is not present."""

    digest = canonical_digest(item)
    if all(canonical_digest(existing) != digest for existing in values):
        values.append(copy.deepcopy(item))


def _record_revision(
    table: dict[str, Any], entity_id: str, record: Mapping[str, Any], event: Mapping[str, Any]
) -> dict[str, Any]:
    """Update an entity while preserving every event-addressable revision."""

    existing = table.get(entity_id, {"entity_id": entity_id, "revisions": []})
    revisions = existing.setdefault("revisions", [])
    revision = {
        "event_id": event["event_id"],
        "event_hash": event["event_hash"],
        "record": copy.deepcopy(dict(record)),
    }
    _append_unique(revisions, revision)
    existing.update(copy.deepcopy(dict(record)))
    existing["entity_id"] = entity_id
    existing["last_event_id"] = event["event_id"]
    table[entity_id] = existing
    return existing


def _validate_synthesis_authority(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> dict[str, Any]:
    """Recompute the authority of one synthesis event from its complete inputs."""

    payload = event["payload"]
    forbidden = sorted(_FORBIDDEN_SYNTHESIS_AUTHORITY_FIELDS.intersection(payload))
    if forbidden:
        raise LedgerIntegrityError(
            "synthesis payload rejects singular or ID-only conceptual authority fields: "
            f"{forbidden}"
        )
    if payload.get("authority_nulls") != SYNTHESIS_AUTHORITY_NULLS:
        raise LedgerIntegrityError(
            "synthesis payload must preserve every proof, empirical, external, source, "
            "theorem, mass-gap, and physics-result authority as an explicit null"
        )
    systems_raw = payload.get("conceptual_systems")
    rounds_raw = payload.get("reflection_rounds")
    if not isinstance(systems_raw, list) or not all(
        isinstance(row, Mapping) for row in systems_raw
    ):
        raise LedgerIntegrityError("synthesis payload lacks exact ordered conceptual_systems")
    if not isinstance(rounds_raw, list) or not all(
        isinstance(row, Mapping) for row in rounds_raw
    ):
        raise LedgerIntegrityError("synthesis payload lacks exact ordered reflection_rounds")
    systems = [copy.deepcopy(dict(row)) for row in systems_raw]
    rounds = [copy.deepcopy(dict(row)) for row in rounds_raw]
    system_ids = [str(row.get("system_id", "")) for row in systems]
    if not system_ids or any(not system_id for system_id in system_ids):
        raise LedgerIntegrityError("every synthesis candidate requires a system_id")
    if len(system_ids) != len(set(system_ids)):
        raise LedgerIntegrityError("synthesis candidate system IDs must be unique")
    systems_by_id = dict(zip(system_ids, systems, strict=True))

    # The event-carried frozen candidates must agree with the latest conceptual
    # content already established by immutable entity events. Reducer metadata may
    # add fields, but it cannot replace any sealed candidate field.
    for system_id, frozen in systems_by_id.items():
        current = state["conceptual_systems"].get(system_id)
        if not isinstance(current, Mapping):
            raise LedgerIntegrityError(
                f"synthesis candidate {system_id} has no prior conceptual-system event"
            )
        if any(current.get(key) != value for key, value in frozen.items()):
            raise LedgerIntegrityError(
                f"synthesis candidate {system_id} differs from the current ledger content"
            )

    component_ids = [str(value) for value in payload.get("component_system_ids", [])]
    preferred_ids = [str(value) for value in payload.get("preferred_system_ids", [])]
    diagnostic_ids = [
        str(value) for value in payload.get("diagnostic_synthesis_system_ids", [])
    ]
    for field_name, values in (
        ("component_system_ids", component_ids),
        ("preferred_system_ids", preferred_ids),
        ("diagnostic_synthesis_system_ids", diagnostic_ids),
    ):
        if len(values) != len(set(values)):
            raise LedgerIntegrityError(f"{field_name} must be set-valued")
        if not set(values).issubset(systems_by_id):
            raise LedgerIntegrityError(f"{field_name} escapes the exact candidate set")
    if set(preferred_ids).intersection(diagnostic_ids):
        raise LedgerIntegrityError("preferred and diagnostic synthesis sets must be disjoint")

    evidence = payload.get("conceptual_adjudication_evidence")
    if evidence is None:
        if preferred_ids or payload.get("preference_authorized") is not False:
            raise LedgerIntegrityError(
                "a null conceptual adjudication authorizes no preferred systems"
            )
        if not diagnostic_ids:
            raise LedgerIntegrityError(
                "an unadjudicated synthesis must name at least one diagnostic system"
            )
        status = "absent_diagnostic_only"
        preference_set = None
    elif isinstance(evidence, Mapping):
        try:
            preference_set = validate_sealed_preference_authority(
                evidence,
                target_id=str(event["identity"]["target_id"]),
                run_id=str(event["identity"]["run_id"]),
                state_version=int(event["identity"]["state_version"]),
                system_ids=system_ids,
                systems=systems,
                reflection_rounds=rounds,
            )
        except ContractError as exc:
            raise LedgerIntegrityError(str(exc)) from exc
        expected_preferred = list(preference_set["preferred_system_ids"])
        if preferred_ids != expected_preferred:
            raise LedgerIntegrityError(
                "synthesis preferred_system_ids differ from the recomputed sealed set"
            )
        decision = preference_set["decision"]
        if decision == "revise_all":
            expected_diagnostics = list(preference_set["nondominated_system_ids"])
            if not expected_diagnostics:
                expected_diagnostics = list(system_ids)
            if (
                payload.get("preference_authorized") is not False
                or diagnostic_ids != expected_diagnostics
            ):
                raise LedgerIntegrityError(
                    "revise_all is diagnostic-only and requires the complete nondominated diagnostic set"
                )
            status = "sealed_revise_all_diagnostic_only"
        else:
            if payload.get("preference_authorized") is not True or diagnostic_ids:
                raise LedgerIntegrityError(
                    "a non-empty sealed preference requires preference_authorized=true "
                    "and an empty diagnostic set"
                )
            status = (
                "sealed_unique"
                if decision == "prefer_unique"
                else "sealed_plural"
            )
    else:
        raise LedgerIntegrityError(
            "conceptual_adjudication_evidence must be a complete object or null"
        )

    authority_ids = [*preferred_ids, *diagnostic_ids]
    unification_rows = payload.get("unification_maps")
    if not isinstance(unification_rows, list) or not all(
        isinstance(row, Mapping) for row in unification_rows
    ):
        raise LedgerIntegrityError(
            "synthesis requires one closed unification row per authority system"
        )
    unification_system_ids = [str(row.get("system_id", "")) for row in unification_rows]
    if unification_system_ids != authority_ids or len(unification_system_ids) != len(
        set(unification_system_ids)
    ):
        raise LedgerIntegrityError(
            "synthesis unification rows must be an ordered bijection over every preferred or diagnostic system"
        )
    for row in unification_rows:
        system_id = str(row["system_id"])
        expected_claim = systems_by_id[system_id].get("unification_claims")
        if row.get("unification_map") != expected_claim:
            raise LedgerIntegrityError(
                f"synthesis unification map for {system_id} differs from its exact system claim"
            )
        assert isinstance(expected_claim, Mapping)
        expected_differences = expected_claim.get(
            "preserved_differences", expected_claim.get("differences_preserved", [])
        )
        if row.get("preserved_differences") != expected_differences:
            raise LedgerIntegrityError(
                f"synthesis preserved differences for {system_id} differ from its exact system claim"
            )

    return {
        "status": status,
        "preference_set": copy.deepcopy(preference_set),
        "evidence_id": evidence.get("evidence_id") if isinstance(evidence, Mapping) else None,
        "evidence_digest": evidence.get("evidence_digest") if isinstance(evidence, Mapping) else None,
        "preferred_system_ids": preferred_ids,
        "diagnostic_synthesis_system_ids": diagnostic_ids,
        "unification_maps": copy.deepcopy(unification_rows),
        "authority_nulls": copy.deepcopy(SYNTHESIS_AUTHORITY_NULLS),
    }


def _reduce_one(state: dict[str, Any], event: Mapping[str, Any]) -> None:
    """Apply one validated event without collapsing theoretical interpretation."""

    event_type, entity_id = event["event_type"], event["entity_id"]
    payload = event["payload"]
    entity_type = event["entity_type"]

    if event_type == "entity_upsert":
        table_name = {
            "conceptual_system": "conceptual_systems",
            "concept": "concepts",
            "hypothesis": "hypotheses",
            "branch": "branches",
        }.get(entity_type)
        if table_name is None:
            raise LedgerIntegrityError(f"unsupported entity_upsert type: {entity_type}")
        _record_revision(state[table_name], entity_id, payload["record"], event)

    elif event_type in {"perspective_shift", "ontology_revision", "conceptual_transformation"}:
        affected = payload["affected_system_ids"]
        transformation = {
            **copy.deepcopy(dict(payload)),
            "transformation_id": entity_id,
            "event_id": event["event_id"],
        }
        state["transformations"][entity_id] = transformation
        for system_id in affected:
            system = state["conceptual_systems"].setdefault(
                system_id,
                {"entity_id": system_id, "status": "active", "genealogy": [], "revisions": []},
            )
            genealogy = system.setdefault("genealogy", [])
            _append_unique(
                genealogy,
                {
                    "transformation_id": entity_id,
                    "event_id": event["event_id"],
                    "kind": payload["transformation_kind"],
                    "parent_revision_id": payload.get("parent_revision_ids", {}).get(system_id),
                    "preserved_differences": payload.get("preserved_differences", []),
                },
            )
            system["current_revision_id"] = payload["result_revision_ids"][system_id]
            system["last_event_id"] = event["event_id"]

    elif event_type == "synthesis_recorded":
        authority = _validate_synthesis_authority(state, event)
        state["syntheses"][entity_id] = {
            **copy.deepcopy(dict(payload)),
            "event_id": event["event_id"],
            "conceptual_preference_authority": authority,
        }
        for system_id in authority["preferred_system_ids"]:
            system = state["conceptual_systems"][system_id]
            _append_unique(
                system.setdefault("preference_synthesis_memberships", []), entity_id
            )
            _append_unique(
                system.setdefault("conceptual_preference_evidence_ids", []),
                authority["evidence_id"],
            )
        for system_id in authority["diagnostic_synthesis_system_ids"]:
            system = state["conceptual_systems"][system_id]
            _append_unique(
                system.setdefault("diagnostic_synthesis_memberships", []), entity_id
            )

    elif event_type == "understanding_delta_recorded":
        state["understanding_deltas"][entity_id] = {
            **copy.deepcopy(dict(payload)),
            "event_id": event["event_id"],
        }

    elif event_type == "evidence_recorded":
        evidence = {**copy.deepcopy(dict(payload)), "event_id": event["event_id"]}
        state["evidence"][entity_id] = evidence
        for hypothesis_id in payload["hypothesis_ids"]:
            hypothesis = state["hypotheses"].setdefault(
                hypothesis_id,
                {
                    "entity_id": hypothesis_id,
                    "status": "proposed",
                    "evidence_edges": [],
                    "interpretations": [],
                    "revisions": [],
                },
            )
            edge = {
                "evidence_id": entity_id,
                "relation": payload["relation"],
                "claim_id": payload["claim_id"],
                "event_id": event["event_id"],
                "decisive": payload.get("decisive", False),
            }
            _append_unique(hypothesis.setdefault("evidence_edges", []), edge)
            if "theoretical_interpretation" in payload:
                _append_unique(
                    hypothesis.setdefault("interpretations", []), payload["theoretical_interpretation"]
                )
            if payload.get("decisive") and payload["relation"] == "contradicts":
                hypothesis["status"] = "refuted"
                hypothesis["retired_by_evidence_id"] = entity_id

    elif event_type == "literature_snapshot_recorded":
        snapshot = {**copy.deepcopy(dict(payload)), "event_id": event["event_id"]}
        state["literature_snapshots"][entity_id] = snapshot
        current_id = state["current_literature_snapshot_id"]
        current = state["literature_snapshots"].get(current_id) if current_id else None
        if current is None or (payload["completed_at"], entity_id) > (
            current["completed_at"],
            current_id,
        ):
            state["current_literature_snapshot_id"] = entity_id
            stale = set(state["stale_branches"])
            stale.update(payload.get("affected_branch_ids", []))
            rebases_by_branch = {item["branch_id"]: item for item in payload.get("branch_rebases", [])}
            for branch_id in payload.get("survivor_branch_ids", []):
                rebase = rebases_by_branch.get(branch_id)
                if rebase is None:
                    raise LedgerIntegrityError(f"surviving branch {branch_id} lacks explicit rebase")
                branch = state["branches"].setdefault(
                    branch_id,
                    {
                        "entity_id": branch_id,
                        "status": "active",
                        "intuition_genealogy": [],
                        "revisions": [],
                    },
                )
                # Rebase adds interpretation; it never rewrites pre-search intuition.
                _append_unique(branch.setdefault("literature_rebases", []), rebase)
                branch["literature_snapshot_id"] = entity_id
                stale.discard(branch_id)
                _append_unique(
                    state["rebase_history"],
                    {"snapshot_id": entity_id, "branch_id": branch_id, "rebase": rebase},
                )
            state["stale_branches"] = sorted(stale)

    elif event_type == "branch_attempt_recorded":
        attempt = {**copy.deepcopy(dict(payload)), "event_id": event["event_id"]}
        state["branch_attempts"][entity_id] = attempt
        branch_id = payload["branch_id"]
        branch = state["branches"].setdefault(
            branch_id,
            {"entity_id": branch_id, "status": "active", "intuition_genealogy": [], "revisions": []},
        )
        _append_unique(branch.setdefault("attempt_ids", []), entity_id)
        for parent in payload.get("parent_branch_ids", []):
            _append_unique(branch.setdefault("ancestry", []), parent)
        for conflict in payload.get("conflicts", []):
            _append_unique(branch.setdefault("conflicts", []), conflict)
        if payload["outcome"] in {"failed", "timed_out"}:
            _append_unique(branch.setdefault("operational_failures", []), entity_id)
        elif payload["outcome"] == "validated":
            _append_unique(branch.setdefault("validated_attempts", []), entity_id)

    elif event_type == "route_retired":
        state["retired_routes"][entity_id] = {
            **copy.deepcopy(dict(payload)),
            "event_id": event["event_id"],
        }
        if entity_id in state["branches"]:
            state["branches"][entity_id]["status"] = "retired"

    elif event_type == "relation_recorded":
        for relation in event["relations"]:
            state["relations"][relation["relation_id"]] = {
                **copy.deepcopy(dict(relation)),
                "event_id": event["event_id"],
            }

    elif event_type in {"prediction_recorded", "proof_obligation_recorded", "reflection_recorded"}:
        # Less common typed records remain queryable without inventing policy.
        collection = state.setdefault(event_type.removesuffix("_recorded") + "s", {})
        collection[entity_id] = {**copy.deepcopy(dict(payload)), "event_id": event["event_id"]}
    else:
        raise LedgerIntegrityError(f"unsupported event type: {event_type}")

    for relation in event.get("relations", []):
        state["relations"][relation["relation_id"]] = {
            **copy.deepcopy(dict(relation)),
            "event_id": event["event_id"],
        }


def reduce_events(events: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Reconstruct the full theory constellation deterministically from events."""

    validate_event_chain(events)
    if not events:
        raise LedgerIntegrityError("target and run are unknowable for an empty event sequence")
    first_namespace = Namespace.from_mapping(events[0]["identity"])
    state = initial_state(first_namespace.target_id, first_namespace.run_id)
    for event in events:
        if event["deduplication_key"] in state["deduplication_keys"]:
            continue
        _reduce_one(state, event)
        state["deduplication_keys"].append(event["deduplication_key"])
        state["event_count"] += 1
        state["last_event_hash"] = event["event_hash"]
        state["generation"] = max(state["generation"], event["identity"]["state_version"] + 1)
    state["active_theory_constellation"] = sorted(
        system_id
        for system_id, system in state["conceptual_systems"].items()
        if system.get("status", "active") != "retired"
    )
    validate_instance(state, "discovery_epistemic_state.schema.json")
    return state


def reduce_from_state(
    prior_state: Mapping[str, Any], events: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Apply a contiguous event suffix to an already reduced canonical state.

    A transaction persists reduced state plus an immutable event artifact. Later
    cycles can therefore advance from that verified state without resolving a
    mutable ``latest`` log. The suffix must extend the exact sequence/hash
    boundary and remain bound to the frozen prior generation.
    """

    state = copy.deepcopy(dict(prior_state))
    validate_instance(state, "discovery_epistemic_state.schema.json")
    if not events:
        raise LedgerIntegrityError("a canonical state transition requires at least one event")
    namespace = Namespace.from_mapping(events[0]["identity"])
    if (state["target_id"], state["run_id"]) != (
        namespace.target_id,
        namespace.run_id,
    ):
        raise LedgerIntegrityError("event suffix target/run does not match prior state")
    expected_sequence = int(state["event_count"]) + 1
    if events[0]["sequence"] != expected_sequence:
        raise LedgerIntegrityError(
            f"event suffix starts at sequence {events[0]['sequence']}, expected {expected_sequence}"
        )
    if events[0]["previous_event_hash"] != state["last_event_hash"]:
        raise LedgerIntegrityError("event suffix does not extend the prior event hash")
    validate_event_chain(
        events,
        first_sequence=expected_sequence,
        previous_hash=state["last_event_hash"],
    )
    expected_version = int(state["generation"])
    for event in events:
        event_namespace = Namespace.from_mapping(event["identity"])
        if (
            event_namespace.target_id != state["target_id"]
            or event_namespace.run_id != state["run_id"]
            or event_namespace.state_version != expected_version
        ):
            raise LedgerIntegrityError(
                "event suffix is not bound to the frozen prior state generation"
            )
        if event["deduplication_key"] not in state["deduplication_keys"]:
            _reduce_one(state, event)
            state["deduplication_keys"].append(event["deduplication_key"])
        state["event_count"] += 1
        state["last_event_hash"] = event["event_hash"]
    state["generation"] = expected_version + 1
    state["active_theory_constellation"] = sorted(
        system_id
        for system_id, system in state["conceptual_systems"].items()
        if system.get("status", "active") != "retired"
    )
    validate_instance(state, "discovery_epistemic_state.schema.json")
    return state


def replay_fixture(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Replay a versioned fixture and optionally verify its expected digest."""

    events = payload.get("events")
    if events is None and isinstance(payload.get("semantic_events"), list):
        events = []
        for index, item in enumerate(payload["semantic_events"], 1):
            if not isinstance(item, Mapping):
                raise ContractError("semantic fixture events must be objects")
            events.append(
                build_event(
                    sequence=index,
                    previous_event_hash=events[-1]["event_hash"] if events else GENESIS_HASH,
                    namespace=Namespace.from_mapping(item["identity"]),
                    event_type=item["event_type"],
                    entity_type=item["entity_type"],
                    entity_id=item["entity_id"],
                    payload=item["payload"],
                    actor=item.get("actor", "fixture"),
                    relations=item.get("relations", []),
                    source_receipt_ids=item.get("source_receipt_ids", []),
                    occurred_at=item.get("occurred_at", f"2026-07-21T00:00:{index:02d}Z"),
                )
            )
    if not isinstance(events, list):
        raise ContractError("replay fixture requires events or semantic_events")
    state = reduce_events(events)
    expected = payload.get("expected_state_digest")
    if expected is not None and canonical_digest(state) != expected:
        raise LedgerIntegrityError(
            f"replayed state digest differs: expected {expected}, got {canonical_digest(state)}"
        )
    return state
