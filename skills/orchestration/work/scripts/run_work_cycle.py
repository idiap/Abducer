#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Alternate discovery and prove cycles under a persistent stop-aware work loop."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import re
import sys
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_SKILLS_ROOT = Path(__file__).resolve().parents[3]
_REPO_ROOT = Path(__file__).resolve().parents[4]
_COMMON_DIR = _SKILLS_ROOT / "common"
_DISCOVERY_SCRIPT_DIR = _SKILLS_ROOT / "discovery" / "kb-discovery-cycle" / "scripts"
_BREAKTHROUGH_SCRIPT_DIR = _SKILLS_ROOT / "evaluation" / "kb-discovery-breakthrough-profiler" / "scripts"
_GOVERNOR_SCRIPT_DIR = _SKILLS_ROOT / "evaluation" / "kb-discovery-governor" / "scripts"
_META_SCRIPT_DIR = _SKILLS_ROOT / "control-plane" / "meta" / "scripts"
_PROVE_SCRIPT_DIR = _SKILLS_ROOT / "discovery" / "kb-prove-cycle" / "scripts"
for _path in (_REPO_ROOT, _COMMON_DIR, _DISCOVERY_SCRIPT_DIR, _BREAKTHROUGH_SCRIPT_DIR, _GOVERNOR_SCRIPT_DIR, _META_SCRIPT_DIR, _PROVE_SCRIPT_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from end_to_end_plausibility import build_plausibility_report_from_artifacts
from end_to_end_plausibility import render_plausibility_markdown
from agentic.discovery.contracts import ContractError
from agentic.discovery.contracts import bytes_digest
from agentic.discovery.contracts import canonical_digest
from agentic.discovery.contracts import stable_identifier
from agentic.discovery.contracts import validate_digest
from agentic.discovery.contracts import validate_identifier
from agentic.discovery.theory_gate import AUTHORIZED_BRANCH_ACTION_KINDS
from agentic.discovery.theory_gate import VerifiedTheoryAuthorization
from agentic.discovery.theory_gate import authorization_is_runtime_verified
from agentic.discovery.theory_gate import authorization_projection
from agentic.discovery.theory_gate import filter_authorized_branches
from agentic.discovery.theory_gate import reserve_canonical_theory_actions
from agentic.discovery.theory_gate import validate_authorization_at_use
from agentic.discovery.theory_gate import verify_canonical_theory_cycle
from discovery_branch_queue import load_discovery_branch_state
from enqueue_proof_candidates import build_queue_entries
from enqueue_proof_candidates import build_repair_lemma_entries
from enqueue_proof_candidates import build_repair_queue_entries
from enqueue_discovery_programmes import apply_promotions as apply_discovery_programme_promotions
from enqueue_discovery_programmes import build_promotions as build_discovery_programme_promotions
from execute_discovery_branches import execute_active_discovery_branches
from generate_discovery_branch_synthesis import build_report as build_discovery_branch_synthesis_report
from generate_discovery_branch_synthesis import render_markdown as render_discovery_branch_synthesis_markdown
from generate_discovery_branch_synthesis import render_tex as render_discovery_branch_synthesis_tex
from generate_discovery_branch_synthesis import compile_pdf as compile_discovery_branch_synthesis_pdf
from generate_meta_reflection_report import build_meta_reflection_report
from generate_meta_reflection_report import write_report as write_meta_report
from generate_discovery_breakthrough_profile import build_report as build_breakthrough_report
from generate_discovery_breakthrough_profile import build_discovery_pattern_routing
from generate_discovery_breakthrough_profile import build_expanded_prompt_pack as build_breakthrough_prompt_pack
from generate_discovery_breakthrough_profile import compile_pdf as compile_breakthrough_pdf
from generate_discovery_breakthrough_profile import render_markdown as render_breakthrough_markdown
from generate_discovery_breakthrough_profile import render_discovery_pattern_routing_markdown
from generate_discovery_breakthrough_profile import render_discovery_pattern_routing_tex
from generate_discovery_breakthrough_profile import render_prompt_pack_markdown
from generate_discovery_breakthrough_profile import render_prompt_pack_tex
from generate_discovery_breakthrough_profile import render_tex as render_breakthrough_tex


_WORK_AUTHORIZATION_FACTORY_SEAL = object()
_WORK_CAPABILITY_BINDING_FIELDS = (
    "target_id",
    "run_id",
    "cycle_id",
    "commit_id",
    "committed_state_version",
    "authorization_digest",
    "authorization_basis_digest",
    "present_investment_decision_digest",
)


@dataclass(frozen=True)
class _ValidatedWorkCycleCapture:
    """One coherent use-time capture of every authority-bearing wrapper slot."""

    projection: dict[str, Any]
    source_capability: VerifiedTheoryAuthorization
    source_projection: Mapping[str, Any]
    reserved_capability: VerifiedTheoryAuthorization | None
    reserved_projection: Mapping[str, Any] | None


class WorkCycleAuthorization(Mapping[str, Any]):
    """Freeze legacy work metadata around one exact theory capability.

    The canonical capability and detached projection are separately immutable.
    Every read rechecks their target, run, lineage, basis, and present-decision
    identities, so a stale wrapper cannot be rebound to another live capability.
    """

    __slots__ = (
        "_runtime_capability",
        "_reserved_runtime_capability",
        "_projection_bytes",
        "_projection_bytes_digest",
        "_capability_binding_digest",
        "_factory_seal",
    )

    def __init__(
        self,
        runtime_capability: VerifiedTheoryAuthorization,
        projection: Mapping[str, Any],
        *,
        _reserved_runtime_capability: VerifiedTheoryAuthorization | None = None,
        _factory_seal: object | None = None,
    ) -> None:
        if _factory_seal is not _WORK_AUTHORIZATION_FACTORY_SEAL:
            raise TypeError("work-cycle authorization is issued only after canonical verification")
        detached = json.loads(json.dumps(dict(projection)))
        encoded = json.dumps(
            detached,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        object.__setattr__(self, "_runtime_capability", runtime_capability)
        object.__setattr__(
            self,
            "_reserved_runtime_capability",
            _reserved_runtime_capability,
        )
        object.__setattr__(self, "_projection_bytes", encoded)
        object.__setattr__(self, "_projection_bytes_digest", bytes_digest(encoded))
        object.__setattr__(
            self,
            "_capability_binding_digest",
            canonical_digest(
                {field: detached.get(field) for field in _WORK_CAPABILITY_BINDING_FIELDS}
            ),
        )
        object.__setattr__(self, "_factory_seal", _factory_seal)
        self._validated_snapshot()

    def __setattr__(self, _name: str, _value: object) -> None:
        """Reject capability and projection replacement after verification."""

        raise TypeError("work-cycle authorization is immutable")

    def _capture_validated_authority(self) -> _ValidatedWorkCycleCapture:
        """Validate captured locals once so later mutation cannot redirect a side effect."""

        factory_seal = self._factory_seal
        projection_bytes = self._projection_bytes
        projection_bytes_digest = self._projection_bytes_digest
        capability_binding_digest = self._capability_binding_digest
        source_capability = self._runtime_capability
        reserved_capability = self._reserved_runtime_capability
        _require_work_contract(
            factory_seal is _WORK_AUTHORIZATION_FACTORY_SEAL
            and bytes_digest(projection_bytes) == projection_bytes_digest,
            "work-cycle authorization seal or immutable projection bytes are invalid",
        )
        source_projection = validate_authorization_at_use(
            source_capability,
            allowed_statuses=("verified_active_current",),
        )
        projection = json.loads(projection_bytes)
        binding_values = {
            field: projection.get(field) for field in _WORK_CAPABILITY_BINDING_FIELDS
        }
        _require_work_contract(
            capability_binding_digest == canonical_digest(binding_values),
            "work-cycle capability binding digest changed",
        )
        for field, projected in binding_values.items():
            _require_work_contract(
                projected is not None and projected == source_projection.get(field),
                f"work-cycle projection {field} differs from its runtime capability",
            )
        binding = projection.get("work_binding")
        _require_work_contract(
            isinstance(binding, Mapping),
            "work-cycle projection lacks its exact work binding",
        )
        for field in (
            "target_id", "run_id", "cycle_id", "commit_id",
            "committed_state_version",
        ):
            _require_work_contract(
                binding.get(field) == source_projection.get(field),
                f"work binding {field} differs from its runtime capability",
            )
        _require_work_contract(
            projection.get("work_binding_digest") == binding.get("binding_digest")
            and binding.get("binding_digest")
            == canonical_digest(binding, exclude_keys=("binding_digest",)),
            "work binding digest is invalid at capability use",
        )
        reservation = projection.get("action_reservation")
        reserved_projection: Mapping[str, Any] | None = None
        if reserved_capability is None:
            _require_work_contract(
                reservation is None,
                "work-cycle projection fabricates a reservation capability",
            )
        else:
            reserved_projection = validate_authorization_at_use(
                reserved_capability,
                allowed_statuses=("actions_reserved",),
            )
            expected_reservation = _validated_reserved_work_record(
                projection,
                reserved_projection,
            )
            _require_work_contract(
                isinstance(reservation, Mapping)
                and dict(reservation) == expected_reservation,
                "work-cycle reservation projection differs from its reserved capability",
            )
        return _ValidatedWorkCycleCapture(
            projection=projection,
            source_capability=source_capability,
            source_projection=source_projection,
            reserved_capability=reserved_capability,
            reserved_projection=reserved_projection,
        )

    def _validated_snapshot(self) -> dict[str, Any]:
        """Return detached work metadata from one coherent authority capture."""

        return self._capture_validated_authority().projection

    @property
    def runtime_capability(self) -> VerifiedTheoryAuthorization:
        """Return the active source or reserved capability after full replay."""

        capture = self._capture_validated_authority()
        return capture.reserved_capability or capture.source_capability

    @property
    def source_runtime_capability(self) -> VerifiedTheoryAuthorization:
        """Return the pre-reservation capability after full wrapper replay."""

        return self._capture_validated_authority().source_capability

    @property
    def reservation_verified(self) -> bool:
        """Return whether this wrapper carries a validated CAS reservation."""

        return self._capture_validated_authority().reserved_capability is not None

    def __getitem__(self, key: str) -> Any:
        return self._validated_snapshot()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._validated_snapshot())

    def __len__(self) -> int:
        return len(self._validated_snapshot())

    def with_reservation(
        self,
        reserved_capability: VerifiedTheoryAuthorization,
    ) -> "WorkCycleAuthorization":
        """Bind the genuine reserved capability; caller-authored maps are invalid."""

        capture = self._capture_validated_authority()
        projection = capture.projection
        _require_work_contract(
            capture.reserved_capability is None
            and "action_reservation" not in projection,
            "work-cycle authorization is already reserved",
        )
        _require_work_contract(
            isinstance(reserved_capability, VerifiedTheoryAuthorization),
            "work-cycle reservation requires the live reserved capability",
        )
        reserved = validate_authorization_at_use(
            reserved_capability,
            allowed_statuses=("actions_reserved",),
        )
        projection["action_reservation"] = _validated_reserved_work_record(
            projection,
            reserved,
        )
        return WorkCycleAuthorization(
            capture.source_capability,
            projection,
            _reserved_runtime_capability=reserved_capability,
            _factory_seal=_WORK_AUTHORIZATION_FACTORY_SEAL,
        )


def _issue_work_cycle_authorization(
    runtime_capability: VerifiedTheoryAuthorization,
    projection: Mapping[str, Any],
) -> WorkCycleAuthorization:
    """Keep construction behind the canonical work-verification boundary."""

    return WorkCycleAuthorization(
        runtime_capability,
        projection,
        _factory_seal=_WORK_AUTHORIZATION_FACTORY_SEAL,
    )


def _validated_reserved_work_record(
    source: Mapping[str, Any],
    reserved: Mapping[str, Any],
) -> dict[str, Any]:
    """Reconstruct the only reservation record a work wrapper may retain."""

    phase = _clean_text(source.get("phase")).lower()
    _require_work_contract(phase in {"discovery", "prove"}, "reservation phase is invalid")
    action_ids = source.get("phase_action_ids", [])
    _require_work_contract(
        isinstance(action_ids, list)
        and bool(action_ids)
        and len(action_ids) == len(set(action_ids)),
        "reservation requires a non-empty unique phase action set",
    )
    action_ids = sorted(str(action_id) for action_id in action_ids)
    binding = source.get("work_binding")
    _require_work_contract(
        isinstance(binding, Mapping),
        "verified authorization has no work binding",
    )
    branch_id = _clean_text(binding.get("canonical_branch_id"))
    consumer_scope = "outer_prove" if phase == "prove" else "outer_discovery"
    proof_obligation_id = (
        _clean_text(binding.get("canonical_proof_obligation_id"))
        if phase == "prove"
        else None
    )
    _require_work_contract(
        reserved.get("status") == "actions_reserved"
        and reserved.get("target_id") == source.get("target_id")
        and reserved.get("run_id") == source.get("run_id")
        and reserved.get("reserved_branch_ids") == [branch_id]
        and reserved.get("reserved_action_ids") == action_ids
        and reserved.get("reservation_consumer_scope") == consumer_scope
        and reserved.get("source_commit_id") == source.get("commit_id")
        and reserved.get("source_committed_state_version")
        == source.get("committed_state_version")
        and reserved.get("authorization_basis_digest")
        == source.get("authorization_basis_digest")
        and reserved.get("present_investment_decision_digest")
        == source.get("present_investment_decision_digest"),
        "canonical reservation crossed target, run, branch, action, source lineage, or temporal basis",
    )
    if phase == "prove":
        _require_work_contract(
            reserved.get("proof_obligation_id") == proof_obligation_id,
            "canonical prove reservation changed the proof obligation",
        )
    reservation = reserved.get("reservation")
    _require_work_contract(
        isinstance(reservation, Mapping)
        and reservation.get("action_ids") == action_ids
        and reservation.get("source_cycle_id") == source.get("cycle_id")
        and reservation.get("source_commit_id") == source.get("commit_id")
        and reservation.get("reserved_state_generation")
        == reserved.get("committed_state_version")
        and reservation.get("reservation_digest")
        == canonical_digest(reservation, exclude_keys=("reservation_digest",)),
        "canonical reservation does not bind the exact action set and lineage",
    )
    reservation_basis = reserved.get("reservation_authorization_basis")
    _require_work_contract(
        isinstance(reservation_basis, Mapping)
        and reserved.get("reservation_authorization_basis_digest")
        == canonical_digest(reservation_basis)
        and reservation_basis.get("source_authorization_basis_digest")
        == source.get("authorization_basis_digest")
        and reservation_basis.get("reservation_digest")
        == reservation.get("reservation_digest"),
        "canonical reservation authority crossed the source theory basis",
    )
    updated_schedule = reserved.get("schedule")
    _require_work_contract(
        isinstance(updated_schedule, Mapping),
        "reserved authorization has no updated schedule",
    )
    consumed = {
        str(row.get("action_id"))
        for row in updated_schedule.get("actions", [])
        if isinstance(row, Mapping) and row.get("status") == "consumed"
    }
    _require_work_contract(
        set(action_ids).issubset(consumed),
        "reserved actions are not consumed in the updated schedule",
    )
    record = {
        **dict(reservation),
        "reserved_commit_id": reserved["commit_id"],
        "reserved_manifest_digest": reserved["manifest_digest"],
        "reserved_commit_path": reserved["commit_path"],
        "updated_schedule_digest": updated_schedule.get(
            "consumed_schedule_digest",
            updated_schedule.get("schedule_digest", ""),
        ),
        "reserved_authorization_digest": reserved["authorization_digest"],
        "reservation_authorization_basis_digest": reserved[
            "reservation_authorization_basis_digest"
        ],
        "reservation_temporal_evaluation_digest": reserved[
            "reservation_temporal_evaluation_digest"
        ],
    }
    record["work_reservation_binding_digest"] = canonical_digest(record)
    return record
from generate_discovery_breakthrough_profile import spawn_discovery_branches
from discovery_branch_queue import save_discovery_branch_state
from generate_discovery_governor_report import apply_governor_to_branch_state
from generate_discovery_governor_report import build_report as build_discovery_governor_report
from generate_discovery_governor_report import discovery_governor_paths
from generate_discovery_governor_report import write_report as write_discovery_governor_report
from generate_expert_conjectures import build_report as build_expert_conjecture_report
from generate_expert_conjectures import expert_conjecture_paths
from generate_expert_conjectures import write_report as write_expert_conjecture_report
from high_reward_watch import high_reward_watch_paths
from high_reward_watch import load_high_reward_watch
from high_reward_watch import save_high_reward_watch
from high_reward_watch import select_high_reward_signal_for_continuation
from high_reward_watch import signal_live_followups
from high_reward_watch import update_signal_status
from inference_diagnosis import refresh_attempt_inference_diagnosis
from kb_context import canonical_artifacts_dir
from kb_context import kb_ref_from_artifacts_dir
from kb_context import resolve_kb_reference
from problem_mathlib import append_mathlib_result
from problem_mathlib import load_mathlib_index
from problem_mathlib import mathlib_paths
from problem_mathlib import save_mathlib_index
from problem_mathlib import search_mathlib
from problem_mathlib import write_mathlib_result_file
from generate_proof_cycle_summary import refresh_summary_from_sources
from proof_queue import consume_next_entry
from proof_queue import finalize_queue_entry
from proof_queue import enqueue_entries
from proof_queue import load_proof_queue
from proof_queue import proof_queue_paths
from proof_queue import queue_entry_selection_sort_key
from proof_queue import save_proof_queue
from proof_discovery_language import serialize_proof_attempt_as_pdl
from proof_discovery_language import serialize_queue_entry_as_pdl
from reasoning_log import ReasoningLogger
from start_proof_cycle import build_attempt_record
from start_proof_cycle import render_attempt_markdown
from statement_text import load_statement_index


WORK_STATE_VERSION = 3
WORK_BINDING_SCHEMA_VERSION = "1.0.0"
CANONICAL_AUTHORITY_MODE = "canonical-theory-gate"
LEGACY_COMPATIBILITY_MODE = "non-authoritative-legacy-compatibility"
DISCOVERY_ACTION_KINDS = frozenset(AUTHORIZED_BRANCH_ACTION_KINDS) - {"prove"}
_PHASE_BLOCKING_RESTRICTIONS = frozenset(
    {"no_active_investment", "literature_blind", "no_promotion", "no_proof"}
)
_MUTABLE_BINDING_PATH_NAMES = frozenset({"latest", "latest.json", "current", "current.json"})
_WORK_BINDING_FIELDS = frozenset(
    {
        "schema_version",
        "binding_id",
        "phase",
        "target_id",
        "run_id",
        "cycle_id",
        "commit_id",
        "committed_state_version",
        "canonical_branch_id",
        "canonical_hypothesis_id",
        "canonical_proof_obligation_id",
        "local_work_item_kind",
        "local_work_item_id",
        "local_work_item_digest",
        "binding_digest",
    }
)
DEFAULT_META_INTERVAL = 6
DEFAULT_META_PERSPECTIVE = "epistemic"
DEFAULT_META_INTERPRETATION = "balanced"


def _utc_now() -> str:
    """Return the current UTC time in ISO 8601 form for persisted metadata."""
    return dt.datetime.now(dt.UTC).isoformat()


def _load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk, defaulting to an empty mapping on failure."""
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _require_work_contract(condition: bool, message: str) -> None:
    """Fail closed at the canonical-to-legacy work boundary."""

    if not condition:
        raise ContractError(f"work-cycle canonical gate rejected execution: {message}")


def _load_json_object_strict(
    path: Path,
    *,
    label: str,
    expected_file_digest: str = "",
) -> WorkCycleAuthorization:
    """Load one required JSON object without legacy empty-object fallback."""

    _require_work_contract(path.is_file(), f"{label} does not exist: {path}")
    try:
        payload_bytes = path.read_bytes()
        payload = json.loads(payload_bytes)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"work-cycle canonical gate could not read {label}: {path}: {exc}") from exc
    if expected_file_digest:
        validate_digest(expected_file_digest)
        _require_work_contract(
            bytes_digest(payload_bytes) == expected_file_digest,
            f"{label} bytes changed after canonical verification",
        )
    _require_work_contract(isinstance(payload, dict), f"{label} must be a JSON object: {path}")
    return payload


def _validate_work_binding(binding: Mapping[str, Any], *, phase: str) -> dict[str, Any]:
    """Validate the exact, self-digested bridge from canonical IDs to one local row."""

    materialized = dict(binding)
    actual_fields = set(materialized)
    _require_work_contract(
        actual_fields == _WORK_BINDING_FIELDS,
        "canonical work binding fields differ from the exact v1 contract "
        f"(missing={sorted(_WORK_BINDING_FIELDS - actual_fields)}, unknown={sorted(actual_fields - _WORK_BINDING_FIELDS)})",
    )
    _require_work_contract(
        materialized.get("schema_version") == WORK_BINDING_SCHEMA_VERSION,
        f"canonical work binding schema_version must be {WORK_BINDING_SCHEMA_VERSION}",
    )
    for field in (
        "binding_id",
        "target_id",
        "run_id",
        "cycle_id",
        "commit_id",
        "canonical_branch_id",
        "canonical_hypothesis_id",
        "local_work_item_id",
    ):
        value = materialized.get(field)
        _require_work_contract(isinstance(value, str), f"{field} must be a string identifier")
        validate_identifier(value, field)
    _require_work_contract(materialized.get("phase") == phase, "canonical work binding phase does not match dispatched phase")
    generation = materialized.get("committed_state_version")
    _require_work_contract(
        isinstance(generation, int) and not isinstance(generation, bool) and generation > 0,
        "committed_state_version must be a positive integer",
    )
    expected_kind = "discovery_branch" if phase == "discovery" else "proof_queue_entry"
    _require_work_contract(
        materialized.get("local_work_item_kind") == expected_kind,
        f"local_work_item_kind must be `{expected_kind}` for phase `{phase}`",
    )
    proof_obligation = materialized.get("canonical_proof_obligation_id")
    if phase == "prove":
        validate_identifier(str(proof_obligation or ""), "canonical_proof_obligation_id")
    else:
        _require_work_contract(
            proof_obligation is None,
            "discovery binding must use null canonical_proof_obligation_id",
        )
    validate_digest(str(materialized.get("local_work_item_digest", "")))
    validate_digest(str(materialized.get("binding_digest", "")))
    _require_work_contract(
        materialized["binding_digest"]
        == canonical_digest(materialized, exclude_keys=("binding_digest",)),
        "canonical work binding digest is invalid",
    )
    return materialized


def verify_work_cycle_theory_authorization(
    *,
    projection_path: Path,
    state_root: Path,
    target_id: str,
    run_id: str,
    work_binding: Mapping[str, Any],
    phase: str,
    previous_lineage: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Verify one canonical cycle and its exact phase-specific work binding.

    The canonical verifier proves active-current literature, immutable commit
    lineage, operator feedback, and schedule eligibility.  This adapter adds
    the narrower obligation required by the legacy work loop: the same branch
    must have a phase-appropriate action and exactly one canonical
    branch/hypothesis (and, for prove, proof-obligation) identity.  It never
    maps from a title, statement, or lexical similarity.
    """

    normalized_phase = _clean_text(phase).lower()
    _require_work_contract(normalized_phase in {"discovery", "prove"}, "phase must be discovery or prove")
    validate_identifier(target_id, "target_id")
    validate_identifier(run_id, "run_id")
    binding = _validate_work_binding(work_binding, phase=normalized_phase)
    _require_work_contract(binding["target_id"] == target_id, "work binding target differs from requested canonical target")
    _require_work_contract(binding["run_id"] == run_id, "work binding run differs from requested canonical run")

    authorization = verify_canonical_theory_cycle(
        projection_path,
        target_id=target_id,
        run_id=run_id,
        state_root=state_root,
        previous_lineage=previous_lineage,
    )
    _require_work_contract(
        authorization_is_runtime_verified(authorization),
        "canonical authorization was not produced by the live runtime verifier",
    )
    _require_work_contract(
        authorization.get("status") == "verified_active_current" and authorization.get("authoritative") is True,
        "canonical verifier did not return active-current authority",
    )
    _require_work_contract(
        Path(str(authorization.get("projection_path", ""))).resolve() == projection_path.resolve(),
        "canonical verifier replayed a different projection path",
    )
    _require_work_contract(
        Path(str(authorization.get("transaction_root", ""))).resolve() == state_root.resolve(),
        "canonical verifier replayed a different transaction root",
    )
    for field in ("target_id", "run_id", "cycle_id", "commit_id", "committed_state_version"):
        _require_work_contract(
            binding[field] == authorization.get(field),
            f"work binding {field} differs from verified canonical authorization",
        )

    projection = _load_json_object_strict(
        projection_path,
        label="canonical cycle projection",
        expected_file_digest=_clean_text(authorization.get("projection_digest")),
    )
    for field in ("target_id", "run_id", "cycle_id", "commit_id", "committed_state_version"):
        _require_work_contract(
            projection.get(field) == binding[field],
            f"committed projection {field} differs from the exact work binding",
        )
    branch_id = binding["canonical_branch_id"]
    hypothesis_id = binding["canonical_hypothesis_id"]
    identity_map = projection.get("identity_map")
    _require_work_contract(isinstance(identity_map, Mapping), "canonical projection identity_map is absent")
    branch_bindings = identity_map.get("branch_bindings", [])
    _require_work_contract(isinstance(branch_bindings, list), "canonical branch_bindings must be a list")
    exact_branch_bindings = [
        row
        for row in branch_bindings
        if isinstance(row, Mapping)
        and row.get("branch_id") == branch_id
        and row.get("hypothesis_id") == hypothesis_id
    ]
    _require_work_contract(
        len(exact_branch_bindings) == 1,
        "canonical branch/hypothesis intersection is missing or ambiguous",
    )
    valid_parallel_branch_ids = projection.get("parallel_outcome", {}).get("valid_branch_ids", [])
    _require_work_contract(
        isinstance(valid_parallel_branch_ids, list)
        and valid_parallel_branch_ids.count(branch_id) == 1,
        "canonical branch is absent or duplicated in the validated parallel outcome",
    )
    hypothesis_ids = identity_map.get("hypothesis_ids", [])
    _require_work_contract(
        isinstance(hypothesis_ids, list) and hypothesis_ids.count(hypothesis_id) == 1,
        "canonical hypothesis is absent or duplicated in the identity map",
    )
    required_action_kinds = {"prove"} if normalized_phase == "prove" else DISCOVERY_ACTION_KINDS
    schedule = projection.get("schedule")
    _require_work_contract(isinstance(schedule, Mapping), "canonical projection schedule is absent")
    schedule_actions = schedule.get("actions", [])
    _require_work_contract(isinstance(schedule_actions, list), "canonical schedule actions must be a list")
    action_kinds_by_branch = authorization.get("action_kinds_by_branch", {})
    _require_work_contract(
        isinstance(action_kinds_by_branch, Mapping),
        "canonical action-kind authorization is malformed",
    )
    raw_action_kinds = action_kinds_by_branch.get(branch_id, [])
    _require_work_contract(isinstance(raw_action_kinds, list), "canonical branch action kinds must be a list")
    _require_work_contract(
        bool(set(raw_action_kinds) & required_action_kinds),
        f"canonical branch has no phase-appropriate `{normalized_phase}` action",
    )
    action_ids_by_branch = authorization.get("action_ids_by_branch", {})
    _require_work_contract(
        isinstance(action_ids_by_branch, Mapping),
        "canonical action-ID authorization is malformed",
    )
    raw_authorized_action_ids = action_ids_by_branch.get(branch_id, [])
    _require_work_contract(isinstance(raw_authorized_action_ids, list), "canonical branch action IDs must be a list")
    phase_kinds_by_id = {
        str(row.get("action_id")): row.get("kind")
        for row in schedule_actions
        if isinstance(row, Mapping) and row.get("action_id")
    }
    authorized_action_ids = {
        str(action_id)
        for action_id in raw_authorized_action_ids
        if phase_kinds_by_id.get(str(action_id)) in required_action_kinds
    }
    phase_actions: list[Mapping[str, Any]] = []
    for row in schedule_actions:
        if not isinstance(row, Mapping):
            continue
        branch_ids = row.get("branch_ids", [])
        restrictions = row.get("restrictions", [])
        _require_work_contract(isinstance(branch_ids, list), "canonical schedule action branch_ids must be a list")
        _require_work_contract(isinstance(restrictions, list), "canonical schedule action restrictions must be a list")
        if (
            row.get("action_id") in authorized_action_ids
            and row.get("kind") in required_action_kinds
            and row.get("status") == "pending"
            and branch_ids == [branch_id]
            and not (set(restrictions) & _PHASE_BLOCKING_RESTRICTIONS)
        ):
            phase_actions.append(row)
    _require_work_contract(
        bool(phase_actions)
        and {str(row["action_id"]) for row in phase_actions} == authorized_action_ids,
        f"every consumer-scoped `{normalized_phase}` action must be pending, unblocked, and bound solely to the exact branch",
    )

    if normalized_phase == "prove":
        obligation_id = binding["canonical_proof_obligation_id"]
        proof_handoff = projection.get("proof_handoff")
        _require_work_contract(isinstance(proof_handoff, Mapping), "prove binding requires one committed proof handoff")
        _require_work_contract(
            proof_handoff.get("branch_id") == branch_id
            and proof_handoff.get("hypothesis_id") == hypothesis_id
            and proof_handoff.get("obligation_id") == obligation_id,
            "proof handoff does not exactly match canonical branch, hypothesis, and obligation",
        )
        concept_id = proof_handoff.get("concept_id")
        branch_concept_ids = exact_branch_bindings[0].get("concept_ids", [])
        identity_concept_ids = identity_map.get("concept_ids", [])
        _require_work_contract(
            isinstance(concept_id, str)
            and isinstance(branch_concept_ids, list)
            and branch_concept_ids.count(concept_id) == 1
            and isinstance(identity_concept_ids, list)
            and identity_concept_ids.count(concept_id) == 1,
            "proof handoff concept does not exactly belong to the bound branch and canonical identity map",
        )
        obligation_ids = identity_map.get("proof_obligation_ids", [])
        _require_work_contract(
            isinstance(obligation_ids, list)
            and obligation_ids.count(obligation_id) == 1,
            "canonical proof obligation is missing or duplicated in the identity map",
        )
    work_projection = authorization_projection(authorization)
    work_projection.update(
        {
            "authority_mode": CANONICAL_AUTHORITY_MODE,
            "phase": normalized_phase,
            "phase_action_ids": sorted({str(row["action_id"]) for row in phase_actions}),
            "promotion_allowed": True,
            "work_binding": binding,
            "work_binding_digest": binding["binding_digest"],
        }
    )
    return _issue_work_cycle_authorization(authorization, work_projection)


def reserve_work_cycle_actions(
    authorization: WorkCycleAuthorization,
) -> WorkCycleAuthorization:
    """Atomically consume the exact phase actions before local investment.

    Verification alone is a time-of-check decision.  This compare-and-swap
    reservation advances the canonical store first, so two work runners cannot
    both act on the same pending schedule action.  The returned record binds
    the reservation artifact and its immutable commit for work-state history.
    """

    _require_work_contract(
        isinstance(authorization, WorkCycleAuthorization),
        "action reservation requires a sealed work-cycle authorization",
    )
    capture = authorization._capture_validated_authority()
    source = capture.projection
    _require_work_contract(
        capture.reserved_capability is None,
        "action reservation cannot replay an already reserved work capability",
    )
    runtime_capability = capture.source_capability
    phase = _clean_text(source.get("phase")).lower()
    _require_work_contract(phase in {"discovery", "prove"}, "reservation phase is invalid")
    action_ids = source.get("phase_action_ids", [])
    _require_work_contract(
        isinstance(action_ids, list)
        and bool(action_ids)
        and len(action_ids) == len(set(action_ids)),
        "reservation requires a non-empty unique phase action set",
    )
    work_binding = source.get("work_binding")
    _require_work_contract(isinstance(work_binding, Mapping), "verified authorization has no work binding")
    branch_id = _clean_text(work_binding.get("canonical_branch_id"))
    _require_work_contract(bool(branch_id), "verified work binding has no canonical branch")
    consumer_receipt_id = stable_identifier(
        "work-consumer",
        source["target_id"],
        source["run_id"],
        work_binding["binding_digest"],
    )
    consumer_scope = "outer_prove" if phase == "prove" else "outer_discovery"
    proof_obligation_id = (
        _clean_text(work_binding.get("canonical_proof_obligation_id")) if phase == "prove" else None
    )
    reserved_authorization = reserve_canonical_theory_actions(
        runtime_capability,
        branch_ids=[branch_id],
        consumer_receipt_id=consumer_receipt_id,
        consumer_scope=consumer_scope,
        proof_obligation_id=proof_obligation_id,
    )
    reserved = validate_authorization_at_use(
        reserved_authorization,
        allowed_statuses=("actions_reserved",),
    )
    reserved_projection = copy.deepcopy(source)
    reserved_projection["action_reservation"] = _validated_reserved_work_record(
        source,
        reserved,
    )
    return WorkCycleAuthorization(
        capture.source_capability,
        reserved_projection,
        _reserved_runtime_capability=reserved_authorization,
        _factory_seal=_WORK_AUTHORIZATION_FACTORY_SEAL,
    )


def _local_work_item_path(*, phase: str, repo_root: Path, artifacts_dir: Path, kb_ref: str) -> Path:
    """Resolve the one legacy state artifact that contains a bound work row."""

    if phase == "discovery":
        return discovery_branch_queue_paths(artifacts_dir)[0]
    return proof_queue_paths(repo_root, kb_ref)[0]


def verify_exact_local_work_item(
    *,
    phase: str,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    authorization: WorkCycleAuthorization,
) -> dict[str, Any]:
    """Re-read and bind one exact executable legacy row to canonical identities."""

    _require_work_contract(
        isinstance(authorization, WorkCycleAuthorization),
        "local work verification requires a sealed work-cycle authorization",
    )
    source = authorization._validated_snapshot()
    normalized_phase = _clean_text(phase).lower()
    _require_work_contract(
        normalized_phase in {"discovery", "prove"}
        and source.get("phase") == normalized_phase,
        "local work phase differs from its sealed work-cycle authorization",
    )
    binding = source.get("work_binding")
    _require_work_contract(isinstance(binding, Mapping), "verified authorization has no work binding")
    path = _local_work_item_path(
        phase=normalized_phase,
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
    )
    payload = _load_json_object_strict(path, label=f"{normalized_phase} local work state")
    collection_name = "branches" if normalized_phase == "discovery" else "entries"
    id_field = "branch_id" if normalized_phase == "discovery" else "queue_id"
    rows = payload.get(collection_name)
    _require_work_contract(isinstance(rows, list), f"local {collection_name} must be a list")
    local_id = binding["local_work_item_id"]
    matches = [
        row
        for row in rows
        if isinstance(row, dict) and row.get(id_field) == local_id
    ]
    _require_work_contract(
        len(matches) == 1,
        f"exact local {normalized_phase} work item `{local_id}` is missing or duplicated",
    )
    row = matches[0]
    status = _clean_text(row.get("status")).lower()
    allowed_statuses = {"active", "pending"} if normalized_phase == "discovery" else {"pending"}
    _require_work_contract(
        status in allowed_statuses,
        f"exact local {normalized_phase} work item `{local_id}` is not executable from status `{status}`",
    )
    _require_work_contract(
        canonical_digest(row) == binding["local_work_item_digest"],
        f"exact local {normalized_phase} work item `{local_id}` changed after its binding was created",
    )
    expected_annotations = {
        "canonical_target_id": binding["target_id"],
        "canonical_run_id": binding["run_id"],
        "canonical_cycle_id": binding["cycle_id"],
        "canonical_commit_id": binding["commit_id"],
        "canonical_state_version": binding["committed_state_version"],
        "canonical_branch_id": binding["canonical_branch_id"],
        "canonical_hypothesis_id": binding["canonical_hypothesis_id"],
        "canonical_proof_obligation_id": binding["canonical_proof_obligation_id"],
    }
    for field, expected in expected_annotations.items():
        _require_work_contract(
            field in row and row.get(field) == expected,
            f"local work item annotation `{field}` does not exactly match the canonical binding",
        )
    return {
        "path": str(path.resolve()),
        "id": local_id,
        "kind": binding["local_work_item_kind"],
        "digest": binding["local_work_item_digest"],
        "row": dict(row),
    }


def _compatibility_authorization(*, phase: str) -> dict[str, Any]:
    """Return the explicit non-authority contract for opt-in legacy execution."""

    return {
        "schema_version": WORK_BINDING_SCHEMA_VERSION,
        "status": "non_authoritative_legacy_compatibility",
        "authority_mode": LEGACY_COMPATIBILITY_MODE,
        "authoritative": False,
        "canonical_theory_verified": False,
        "phase": phase,
        "promotion_allowed": False,
        "research_promotion_allowed": False,
        "proof_promotion_allowed": False,
        "warning": (
            "Legacy compatibility executed without canonical active-current theory authority; "
            "its outputs cannot authorize research or proof promotion."
        ),
    }


def _authority_record(authorization: Mapping[str, Any]) -> dict[str, Any]:
    """Project authorization into a compact, stable work-state record."""

    if isinstance(authorization, WorkCycleAuthorization):
        payload = authorization._validated_snapshot()
        reserved = authorization._reserved_runtime_capability is not None
    else:
        payload = dict(authorization)
        reserved = False
    binding = payload.get("work_binding") if isinstance(payload.get("work_binding"), Mapping) else {}
    reservation = (
        payload.get("action_reservation")
        if isinstance(payload.get("action_reservation"), Mapping)
        else {}
    )
    canonical_verified = payload.get("status") == "verified_active_current"
    # Verification identifies a potentially valid action; reservation is what
    # makes one runner its exclusive consumer.  Never expose pre-reservation
    # early returns (for example a mutable plausibility stop or max-cycle stop)
    # as authoritative or promotion-capable.
    authoritative = canonical_verified and reserved and bool(reservation)
    promotion_allowed = payload.get("promotion_allowed") is True and authoritative
    return {
        "schema_version": WORK_BINDING_SCHEMA_VERSION,
        "mode": payload.get("authority_mode", ""),
        "status": payload.get("status", ""),
        "authoritative": authoritative,
        "canonical_theory_verified": canonical_verified,
        "promotion_allowed": promotion_allowed,
        "research_promotion_allowed": promotion_allowed,
        "proof_promotion_allowed": promotion_allowed,
        "target_id": payload.get("target_id", ""),
        "run_id": payload.get("run_id", ""),
        "cycle_id": payload.get("cycle_id", ""),
        "commit_id": payload.get("commit_id", ""),
        "committed_state_version": payload.get("committed_state_version", 0),
        "binding_id": binding.get("binding_id", ""),
        "binding_digest": payload.get("work_binding_digest", ""),
        "canonical_branch_id": binding.get("canonical_branch_id", ""),
        "canonical_hypothesis_id": binding.get("canonical_hypothesis_id", ""),
        "canonical_proof_obligation_id": binding.get("canonical_proof_obligation_id"),
        "local_work_item_kind": binding.get("local_work_item_kind", ""),
        "local_work_item_id": binding.get("local_work_item_id", ""),
        "local_work_item_digest": binding.get("local_work_item_digest", ""),
        "phase_action_ids": list(payload.get("phase_action_ids", [])),
        "authorization_digest": payload.get("authorization_digest", ""),
        "action_reserved": authoritative,
        "reservation_id": reservation.get("reservation_id", ""),
        "reservation_digest": reservation.get("reservation_digest", ""),
        "reservation_consumer_receipt_id": reservation.get("consumer_receipt_id", ""),
        "reservation_source_state_generation": reservation.get("source_state_generation", 0),
        "reservation_state_generation": reservation.get("reserved_state_generation", 0),
        "reservation_commit_id": reservation.get("reserved_commit_id", ""),
        "reservation_manifest_digest": reservation.get("reserved_manifest_digest", ""),
        "reservation_commit_path": reservation.get("reserved_commit_path", ""),
        "warning": payload.get("warning", ""),
    }


def _decorate_authority(
    state: dict[str, Any],
    latest: Mapping[str, Any],
    authorization: Mapping[str, Any],
) -> dict[str, Any]:
    """Attach an unmistakable authority record to all work-cycle return paths."""

    record = _authority_record(authorization)
    decorated = dict(latest)
    decorated["authority"] = record
    decorated["authoritative"] = record["authoritative"]
    decorated["promotion_allowed"] = record["promotion_allowed"]
    meta = _ensure_dict(state.get("metadata"))
    meta["authority_mode"] = record["mode"]
    meta["authoritative"] = record["authoritative"]
    meta["promotion_allowed"] = record["promotion_allowed"]
    meta["last_authority"] = record
    state["metadata"] = meta
    return decorated


def _load_looper_frontier(repo_root: Path, kb_ref: str) -> dict[str, Any]:
    """Load optional Looper target/dependency frontier context for governed runs."""

    frontier_path = repo_root / "agentic" / "state" / "dependency_frontier.json"
    target_path = repo_root / "agentic" / "state" / "current_target.json"
    frontier = _load_json(frontier_path)
    target = _load_json(target_path)
    if not frontier or not target:
        return {}
    kb_path = _clean_text(target.get("kb_path"))
    if kb_ref and kb_path and not kb_path.endswith(f"{kb_ref}.kb.md"):
        return {}
    rows = [row for row in _ensure_list(frontier.get("frontier")) if isinstance(row, dict)]
    status_counts: dict[str, int] = {}
    for row in rows:
        status = _clean_text(row.get("status")) or "unknown"
        status_counts[status] = status_counts.get(status, 0) + 1
    return {
        "target_id": _clean_text(target.get("target_id")),
        "frontier_count": len(rows),
        "status_counts": status_counts,
        "recommended_next": _clean_text(frontier.get("next_workflow_recommendation")),
        "frontier_path": str(frontier_path),
        "target_path": str(target_path),
    }


def _ensure_dict(value: Any) -> dict[str, Any]:
    """Normalize an arbitrary value into a dictionary-shaped object."""
    return value if isinstance(value, dict) else {}


def _ensure_list(value: Any) -> list[Any]:
    """Normalize an arbitrary value into a list-shaped object."""
    return value if isinstance(value, list) else []


def _clean_text(value: Any) -> str:
    """Collapse free-form text-like values into a single normalized line."""
    return " ".join(str(value or "").strip().split())


def _safe_int(value: Any, default: int = 0) -> int:
    """Parse an integer-like value while preserving a safe fallback."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _queue_has_active_entries(queue: dict[str, Any]) -> bool:
    """Return whether the persistent queue still has work that discovery should not supersede."""
    for row in _ensure_list(queue.get("entries")):
        if not isinstance(row, dict):
            continue
        status = _clean_text(row.get("status")).lower()
        if status == "pending":
            return True
    return False


def _top_open_queue_entry(queue: dict[str, Any]) -> dict[str, Any]:
    """Return the strongest currently open queue entry for surfaced reasoning summaries."""

    statuses = {"pending": 0, "in_progress": 1, "deferred": 2}
    rows = [
        row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict)
        and _clean_text(row.get("status")).lower() in statuses
        and _clean_text(row.get("deferred_by")) != "inactive-discovery-frontier"
    ]
    rows.sort(
        key=lambda row: (
            statuses.get(_clean_text(row.get("status")).lower(), 99),
            *queue_entry_selection_sort_key(row),
        )
    )
    return rows[0] if rows else {}


def _interpretability_deferred_entries(queue: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in _ensure_list(queue.get("entries")):
        if not isinstance(row, dict):
            continue
        if _clean_text(row.get("status")).lower() != "deferred":
            continue
        if _clean_text(row.get("deferred_by")) != "llm-interpretability-gate":
            continue
        rows.append(row)
    rows.sort(key=lambda item: float(item.get("priority", 0.0) or 0.0), reverse=True)
    return rows


def work_state_paths(artifacts_dir: Path) -> tuple[Path, Path]:
    """Return the canonical JSON and Markdown locations for the work-state artifact."""
    return artifacts_dir / "work-state.json", artifacts_dir / "work-state.md"


def plausibility_report_paths(artifacts_dir: Path) -> tuple[Path, Path]:
    """Return the canonical JSON and Markdown locations for the plausibility report."""
    return artifacts_dir / "end-to-end-proof-plausibility.json", artifacts_dir / "end-to-end-proof-plausibility.md"


def meta_report_paths(artifacts_dir: Path) -> tuple[Path, Path, Path, Path]:
    """Return the canonical artifact paths for the auto-generated meta reflection report."""

    return (
        artifacts_dir / "meta-reflection-report.json",
        artifacts_dir / "meta-reflection-report.md",
        artifacts_dir / "meta-reflection-report.tex",
        artifacts_dir / "meta-reflection-report.pdf",
    )


def breakthrough_profile_paths(artifacts_dir: Path) -> tuple[Path, Path, Path, Path]:
    """Return the canonical artifact paths for the discovery breakthrough profile."""
    return (
        artifacts_dir / "discovery-breakthrough-profile.json",
        artifacts_dir / "discovery-breakthrough-profile.md",
        artifacts_dir / "discovery-breakthrough-profile.tex",
        artifacts_dir / "discovery-breakthrough-profile.pdf",
    )


def breakthrough_prompt_paths(artifacts_dir: Path) -> tuple[Path, Path, Path, Path]:
    """Return the canonical artifact paths for the family-specific discovery prompt pack."""
    return (
        artifacts_dir / "discovery-family-prompts.json",
        artifacts_dir / "discovery-family-prompts.md",
        artifacts_dir / "discovery-family-prompts.tex",
        artifacts_dir / "discovery-family-prompts.pdf",
    )


def discovery_pattern_routing_paths(artifacts_dir: Path) -> tuple[Path, Path, Path, Path]:
    """Return the canonical artifact paths for the spawned discovery-layer routing plan."""
    return (
        artifacts_dir / "discovery-pattern-routing.json",
        artifacts_dir / "discovery-pattern-routing.md",
        artifacts_dir / "discovery-pattern-routing.tex",
        artifacts_dir / "discovery-pattern-routing.pdf",
    )


def discovery_branch_queue_paths(artifacts_dir: Path) -> tuple[Path, Path]:
    """Return the canonical artifact paths for the persistent discovery-branch queue."""

    return artifacts_dir / "discovery-branch-queue.json", artifacts_dir / "discovery-branch-queue.md"


def discovery_branch_synthesis_paths(artifacts_dir: Path) -> tuple[Path, Path, Path, Path]:
    """Return the canonical artifact paths for the discovery-branch synthesis report."""

    return (
        artifacts_dir / "discovery-branch-synthesis.json",
        artifacts_dir / "discovery-branch-synthesis.md",
        artifacts_dir / "discovery-branch-synthesis.tex",
        artifacts_dir / "discovery-branch-synthesis.pdf",
    )


def _refresh_discovery_governor(
    *,
    artifacts_dir: Path,
    kb_ref: str,
    top_k: int,
    apply_to_branch_queue: bool,
) -> tuple[dict[str, Any], tuple[Path, Path]]:
    """Regenerate the deterministic discovery-governor report and optionally apply it to branch state."""

    report = build_discovery_governor_report(
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        activate_top_k=max(1, top_k),
    )
    governor_json, governor_md = discovery_governor_paths(artifacts_dir)
    write_discovery_governor_report(report, output_json=governor_json, output_md=governor_md)
    if apply_to_branch_queue:
        branch_json, branch_md = discovery_branch_queue_paths(artifacts_dir)
        branch_state = load_discovery_branch_state(branch_json, kb_ref=kb_ref)
        apply_governor_to_branch_state(branch_state, report=report, activate_top_k=max(1, top_k))
        save_discovery_branch_state(branch_state, json_path=branch_json, md_path=branch_md)
    return report, (governor_json, governor_md)


def default_work_state(*, kb_ref: str, max_cycles: int) -> dict[str, Any]:
    """Build a fresh persistent work-state payload before any outer-loop steps run."""
    now = _utc_now()
    return {
        "metadata": {
            "kb_ref": kb_ref,
            "work_state_version": WORK_STATE_VERSION,
            "generated_utc": now,
            "updated_utc": now,
            "cycle_count": 0,
            "max_cycles": max(1, max_cycles),
            "next_phase": "discovery",
            "stop_status": "running",
            "stop_reason": "",
            "plausible_solution_detected": False,
            "meta_interval": DEFAULT_META_INTERVAL,
            "meta_perspective": DEFAULT_META_PERSPECTIVE,
            "meta_interpretation": DEFAULT_META_INTERPRETATION,
            "last_meta_cycle": 0,
            "last_meta_reason": "",
            "last_meta_queue_signature": "",
            "high_reward_active": False,
            "high_reward_signal_id": "",
            "high_reward_result_id": "",
            "high_reward_started_cycle": 0,
            "high_reward_extension_cycles": 0,
            "high_reward_reason": "",
            "authority_mode": "unverified",
            "authoritative": False,
            "promotion_allowed": False,
            "last_authority": {},
            "canonical_theory_lineage": {},
        },
        "latest": {},
        "plausibility": {},
        "history": [],
    }


def load_work_state(path: Path, *, kb_ref: str, max_cycles: int) -> dict[str, Any]:
    """Load a saved work state and repair required metadata fields if needed."""
    if not path.exists():
        return default_work_state(kb_ref=kb_ref, max_cycles=max_cycles)
    payload = _load_json(path)
    if not payload:
        return default_work_state(kb_ref=kb_ref, max_cycles=max_cycles)
    payload.setdefault("metadata", {})
    payload.setdefault("latest", {})
    payload.setdefault("plausibility", {})
    payload.setdefault("history", [])
    meta = _ensure_dict(payload.get("metadata"))
    meta["kb_ref"] = kb_ref
    meta["work_state_version"] = WORK_STATE_VERSION
    meta["max_cycles"] = max(1, max_cycles)
    meta.setdefault("meta_interval", DEFAULT_META_INTERVAL)
    meta.setdefault("meta_perspective", DEFAULT_META_PERSPECTIVE)
    meta.setdefault("meta_interpretation", DEFAULT_META_INTERPRETATION)
    meta.setdefault("last_meta_cycle", 0)
    meta.setdefault("last_meta_reason", "")
    meta.setdefault("last_meta_queue_signature", "")
    meta.setdefault("high_reward_active", False)
    meta.setdefault("high_reward_signal_id", "")
    meta.setdefault("high_reward_result_id", "")
    meta.setdefault("high_reward_started_cycle", 0)
    meta.setdefault("high_reward_extension_cycles", 0)
    meta.setdefault("high_reward_reason", "")
    meta.setdefault("authority_mode", "unverified")
    meta.setdefault("authoritative", False)
    meta.setdefault("promotion_allowed", False)
    meta.setdefault("last_authority", {})
    meta.setdefault("canonical_theory_lineage", {})
    payload["metadata"] = meta
    return payload


def render_work_state_markdown(state: dict[str, Any]) -> str:
    """Render a human-readable summary of the current outer-loop state."""
    meta = _ensure_dict(state.get("metadata"))
    latest = _ensure_dict(state.get("latest"))
    plausibility = _ensure_dict(state.get("plausibility"))
    decision = _ensure_dict(plausibility.get("decision"))
    history = [row for row in _ensure_list(state.get("history")) if isinstance(row, dict)]
    lines = [
        "# Work State",
        "",
        f"- KB ref: {meta.get('kb_ref', '')}",
        f"- Cycle count: {meta.get('cycle_count', 0)} / {meta.get('max_cycles', 0)}",
        f"- Next phase: {meta.get('next_phase', '')}",
        f"- Stop status: {meta.get('stop_status', '')}",
        f"- Stop reason: {meta.get('stop_reason', '')}",
        f"- Plausible solution detected: {meta.get('plausible_solution_detected', False)}",
        f"- Meta interval: {meta.get('meta_interval', DEFAULT_META_INTERVAL)}",
        f"- Last meta cycle: {meta.get('last_meta_cycle', 0)}",
        f"- Last meta reason: {meta.get('last_meta_reason', '')}",
        f"- High-reward active: {meta.get('high_reward_active', False)}",
        f"- High-reward signal: {meta.get('high_reward_signal_id', '')}",
        f"- High-reward extension cycles: {meta.get('high_reward_extension_cycles', 0)}",
        f"- High-reward rationale: {meta.get('high_reward_reason', '')}",
        f"- Looper target: {meta.get('looper_target_id', '')}",
        f"- Looper frontier count: {meta.get('looper_frontier_count', 0)}",
        f"- Looper frontier recommendation: {meta.get('looper_frontier_recommendation', '')}",
        f"- Authority mode: {meta.get('authority_mode', 'unverified')}",
        f"- Authoritative: {meta.get('authoritative', False)}",
        f"- Promotion allowed: {meta.get('promotion_allowed', False)}",
        "",
        "## Latest Step",
        "",
        f"- Phase: {latest.get('phase', '')}",
        f"- Status: {latest.get('status', '')}",
        f"- Detail: {latest.get('detail', '')}",
        f"- Meta trigger: {latest.get('meta_trigger_reason', '')}",
        f"- Authoritative: {latest.get('authoritative', False)}",
        f"- Promotion allowed: {latest.get('promotion_allowed', False)}",
        f"- Canonical binding: {_ensure_dict(latest.get('authority')).get('binding_id', '')}",
        f"- Canonical action reserved: {_ensure_dict(latest.get('authority')).get('action_reserved', False)}",
        f"- Canonical reservation: {_ensure_dict(latest.get('authority')).get('reservation_id', '')}",
        "",
        "## Plausibility",
        "",
        f"- Score: {plausibility.get('plausibility_score', 0.0):.3f}" if plausibility else "- Score: 0.000",
        f"- Decision: {decision.get('decision', '')}",
        f"- Detail: {decision.get('detail', '')}",
        "",
        "## History",
        "",
    ]
    if not history:
        lines.append("- No work cycles recorded yet.")
        lines.append("")
    else:
        for row in history[-8:]:
            lines.append(
                f"- Cycle {row.get('cycle_number', 0)} | {row.get('phase', '')} | {row.get('status', '')} | "
                f"authoritative={row.get('authoritative', False)} | promotion_allowed={row.get('promotion_allowed', False)} | "
                f"{row.get('detail', '')}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def save_work_state(state: dict[str, Any], *, json_path: Path, md_path: Path) -> None:
    """Persist the current work state in both machine-readable and narrative form."""
    meta = _ensure_dict(state.get("metadata"))
    meta["updated_utc"] = _utc_now()
    state["metadata"] = meta
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_work_state_markdown(state), encoding="utf-8")


def _write_plausibility_report(artifacts_dir: Path, report: dict[str, Any]) -> tuple[Path, Path]:
    """Write the latest end-to-end plausibility report next to the current artifacts."""
    output_json, output_md = plausibility_report_paths(artifacts_dir)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_plausibility_markdown(report), encoding="utf-8")
    return output_json, output_md


def _queue_meta_signature(repo_root: Path, kb_ref: str) -> str:
    """Summarize the current proof-queue state for de-duplicating queue-exhaustion meta triggers."""

    queue_json, _ = proof_queue_paths(repo_root, kb_ref)
    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    queue_meta = _ensure_dict(queue.get("metadata"))
    return "|".join(
        [
            str(int(queue_meta.get("pending_count", 0) or 0)),
            str(int(queue_meta.get("in_progress_count", 0) or 0)),
            str(int(queue_meta.get("completed_count", 0) or 0)),
        ]
    )


def _load_high_reward_context(
    *,
    artifacts_dir: Path,
    kb_ref: str,
    repo_root: Path,
) -> tuple[dict[str, Any], tuple[Path, Path], dict[str, Any], dict[str, Any]]:
    """Load the watch, proof queue, and discovery-branch state needed for budget deferral."""

    watch_json, watch_md = high_reward_watch_paths(artifacts_dir)
    watch = load_high_reward_watch(watch_json, kb_ref=kb_ref)
    queue_json, _queue_md = proof_queue_paths(repo_root, kb_ref)
    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    branch_json, _branch_md = discovery_branch_queue_paths(artifacts_dir)
    branch_state = load_discovery_branch_state(branch_json, kb_ref=kb_ref)
    return watch, (watch_json, watch_md), queue, branch_state


def _clear_high_reward_state(meta: dict[str, Any]) -> None:
    """Reset the in-memory high-reward continuation fields on the work metadata."""

    meta["high_reward_active"] = False
    meta["high_reward_signal_id"] = ""
    meta["high_reward_result_id"] = ""
    meta["high_reward_started_cycle"] = 0
    meta["high_reward_extension_cycles"] = 0
    meta["high_reward_reason"] = ""


def _high_reward_extension_allows_continue(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    meta: dict[str, Any],
) -> tuple[bool, str, dict[str, Any]]:
    """Decide whether a high-reward result should defer the nominal cycle budget stop."""

    watch, watch_paths, queue, branch_state = _load_high_reward_context(
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        repo_root=repo_root,
    )
    for row in _ensure_list(watch.get("signals")):
        if not isinstance(row, dict):
            continue
        status = _clean_text(row.get("status")).lower()
        if status not in {"pending", "active"}:
            continue
        followup_status = signal_live_followups(row, queue=queue, branch_state=branch_state)
        if not followup_status["has_live_followups"]:
            update_signal_status(
                watch,
                signal_id=_clean_text(row.get("signal_id")),
                status="expired",
                note="No live dependent follow-up tasks remain for this high-reward result.",
            )
    signal, followup_status = select_high_reward_signal_for_continuation(
        watch,
        queue=queue,
        branch_state=branch_state,
    )
    if signal is None:
        if _clean_text(meta.get("high_reward_signal_id")):
            _clear_high_reward_state(meta)
        save_high_reward_watch(watch, json_path=watch_paths[0], md_path=watch_paths[1])
        return False, "", {}

    signal_id = _clean_text(signal.get("signal_id"))
    recommended_extension = max(1, _safe_int(signal.get("recommended_extension_cycles"), 4))
    if not bool(meta.get("high_reward_active")) or _clean_text(meta.get("high_reward_signal_id")) != signal_id:
        signal = update_signal_status(
            watch,
            signal_id=signal_id,
            status="active",
            note="Activated by the work loop at the nominal cycle budget because live dependent follow-ups remain.",
            activated_at_cycle=_safe_int(meta.get("cycle_count")),
        )
        meta["high_reward_active"] = True
        meta["high_reward_signal_id"] = signal_id
        meta["high_reward_result_id"] = _clean_text(signal.get("result_id"))
        meta["high_reward_started_cycle"] = _safe_int(meta.get("cycle_count"))
        meta["high_reward_extension_cycles"] = recommended_extension
        meta["high_reward_reason"] = _clean_text(signal.get("continuation_rationale"))
        save_high_reward_watch(watch, json_path=watch_paths[0], md_path=watch_paths[1])
        return True, "activated-high-reward-extension", signal

    extension_used = max(0, _safe_int(meta.get("cycle_count")) - _safe_int(meta.get("max_cycles")))
    if extension_used < max(1, _safe_int(meta.get("high_reward_extension_cycles"), recommended_extension)):
        save_high_reward_watch(watch, json_path=watch_paths[0], md_path=watch_paths[1])
        return True, "continuing-high-reward-extension", signal

    update_signal_status(
        watch,
        signal_id=signal_id,
        status="expired",
        note="The bounded high-reward continuation window was consumed without terminal closure.",
    )
    save_high_reward_watch(watch, json_path=watch_paths[0], md_path=watch_paths[1])
    _clear_high_reward_state(meta)
    return False, "", {}


def _should_run_meta(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    meta: dict[str, Any],
    latest: dict[str, Any],
) -> tuple[bool, str, str]:
    """Determine whether the work loop should auto-run the meta reflection layer now."""

    cycle_count = _safe_int(meta.get("cycle_count"))
    interval = max(1, _safe_int(meta.get("meta_interval"), DEFAULT_META_INTERVAL))
    last_meta_cycle = _safe_int(meta.get("last_meta_cycle"))
    stop_status = _clean_text(meta.get("stop_status")).lower()
    queue_signature = _queue_meta_signature(repo_root, kb_ref)
    pending_count, in_progress_count, _completed_count = [
        _safe_int(value) for value in (queue_signature.split("|") + ["0", "0", "0"])[:3]
    ]

    if stop_status in {"stop-plausible-solution", "stop-max-cycles"} and cycle_count > last_meta_cycle:
        return True, stop_status, queue_signature
    if pending_count == 0 and in_progress_count == 0:
        if _clean_text(meta.get("last_meta_reason")) != "queue-exhausted" or _clean_text(meta.get("last_meta_queue_signature")) != queue_signature:
            return True, "queue-exhausted", queue_signature
    if cycle_count > 0 and cycle_count % interval == 0 and cycle_count != last_meta_cycle:
        return True, f"cycle-interval-{interval}", queue_signature
    if _clean_text(latest.get("status")).lower() == "idle" and _clean_text(latest.get("phase")).lower() == "prove":
        if _clean_text(meta.get("last_meta_reason")) != "prove-idle" or _clean_text(meta.get("last_meta_queue_signature")) != queue_signature:
            return True, "prove-idle", queue_signature
    return False, "", queue_signature


def _run_meta_checkpoint(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    perspective: str,
    interpretation: str,
) -> tuple[dict[str, Any], tuple[Path, Path, Path, Path], dict[str, str]]:
    """Generate and persist the current meta reflection artifacts for the work loop."""

    logger = ReasoningLogger("meta", repo_root=repo_root)
    logger.add_kv("artifacts_dir", str(artifacts_dir))
    logger.add_kv("perspective", perspective)
    logger.add_kv("interpretation", interpretation)
    report = build_meta_reflection_report(
        artifacts_dir=artifacts_dir,
        perspective=perspective,
        interpretation=interpretation,
    )
    output_json, output_md, output_tex, output_pdf = meta_report_paths(artifacts_dir)
    write_meta_report(
        report,
        output_json=output_json,
        output_md=output_md,
        output_tex=output_tex,
        output_pdf=output_pdf,
    )
    logger.step(
        "Automatic meta checkpoint",
        "\n".join(
            [
                f"perspective={perspective}",
                f"interpretation={interpretation}",
                f"headline={_clean_text(_ensure_dict(report.get('meta_judgment')).get('headline'))}",
            ]
        ),
    )
    logger.add_output("meta_reflection_json", output_json)
    logger.add_output("meta_reflection_md", output_md)
    logger.add_output("meta_reflection_tex", output_tex)
    logger.add_output("meta_reflection_pdf", output_pdf)
    logger.finalize(
        "success",
        summary=(
            _clean_text(_ensure_dict(report.get("meta_judgment")).get("headline"))
            or "Generated automatic meta reflection checkpoint."
        ),
    )
    return report, (output_json, output_md, output_tex, output_pdf), {
        "meta_reasoning_log_md": str(logger.log_path),
        "meta_reasoning_surface_md": str(logger.surface_path),
        "meta_reasoning_surface_json": str(logger.surface_json_path),
    }


def _write_breakthrough_profile(
    artifacts_dir: Path,
    *,
    kb_ref: str,
    prior_art: dict[str, Any],
    queue: dict[str, Any],
) -> tuple[
    dict[str, Any],
    tuple[Path, Path, Path, Path],
    tuple[Path, Path, Path, Path],
    tuple[Path, Path, Path, Path],
    tuple[Path, Path],
    list[dict[str, str]],
]:
    """Persist a breakthrough-profile report when discovery has exhausted the local queue."""
    report = build_breakthrough_report(prior_art=prior_art, queue=queue, kb_ref=kb_ref)
    output_json, output_md, output_tex, output_pdf = breakthrough_profile_paths(artifacts_dir)
    prompt_pack = build_breakthrough_prompt_pack(report)
    routing = build_discovery_pattern_routing(report, prompt_pack)
    prompt_json, prompt_md, prompt_tex, prompt_pdf = breakthrough_prompt_paths(artifacts_dir)
    routing_json, routing_md, routing_tex, routing_pdf = discovery_pattern_routing_paths(artifacts_dir)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_breakthrough_markdown(report), encoding="utf-8")
    output_tex.write_text(render_breakthrough_tex(report), encoding="utf-8")
    prompt_json.write_text(json.dumps(prompt_pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prompt_md.write_text(render_prompt_pack_markdown(prompt_pack), encoding="utf-8")
    prompt_tex.write_text(render_prompt_pack_tex(prompt_pack), encoding="utf-8")
    routing_json.write_text(json.dumps(routing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    routing_md.write_text(render_discovery_pattern_routing_markdown(routing), encoding="utf-8")
    routing_tex.write_text(render_discovery_pattern_routing_tex(routing), encoding="utf-8")
    _branch_state, branch_paths, branch_dossiers = spawn_discovery_branches(
        routing,
        artifacts_dir=artifacts_dir,
        activate_top_k=4,
    )
    compile_breakthrough_pdf(output_tex, output_pdf, preferred_engine="auto")
    compile_breakthrough_pdf(prompt_tex, prompt_pdf, preferred_engine="auto")
    compile_breakthrough_pdf(routing_tex, routing_pdf, preferred_engine="auto")
    return (
        report,
        (output_json, output_md, output_tex, output_pdf),
        (prompt_json, prompt_md, prompt_tex, prompt_pdf),
        (routing_json, routing_md, routing_tex, routing_pdf),
        branch_paths,
        branch_dossiers,
    )


def _run_branch_to_theorem_pipeline(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    branch_outputs: tuple[Path, Path],
    top_k: int,
    exact_branch_id: str = "",
    expected_branch_digest: str = "",
    canonical_branch_id: str = "",
    canonical_hypothesis_id: str = "",
    promotion_allowed: bool = True,
) -> dict[str, Any]:
    """Execute branches and promote only work permitted by the caller's authority."""

    execution_state, execution_index, execution_paths, execution_outputs = execute_active_discovery_branches(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        limit=1 if _clean_text(exact_branch_id) else max(1, top_k),
        exact_branch_id=_clean_text(exact_branch_id),
        expected_branch_digest=_clean_text(expected_branch_digest),
    )
    if _clean_text(exact_branch_id):
        _require_work_contract(
            len(execution_outputs) == 1
            and _clean_text(execution_outputs[0].get("branch_id")) == _clean_text(exact_branch_id),
            "authoritative discovery executor did not return exactly the bound branch",
        )
    execution_meta = _ensure_dict(execution_index.get("metadata"))
    executed_current_round = int(execution_meta.get("last_run_execution_count", len(execution_outputs)) or 0) > 0
    if not executed_current_round:
        return {
            "executed_current_round": False,
            "execution_paths": execution_paths,
            "execution_outputs": execution_outputs,
            "branch_state": execution_state,
            "execution_index": execution_index,
            "synthesis_report": {},
            "synthesis_paths": discovery_branch_synthesis_paths(artifacts_dir),
            "expert_report": {},
            "expert_paths": expert_conjecture_paths(artifacts_dir),
            "governor_report": {},
            "governor_paths": discovery_governor_paths(artifacts_dir),
            "promotion_report": {
                "metadata": {
                    "kb_ref": kb_ref,
                    "programme_count": 0,
                    "promotion_allowed": bool(promotion_allowed),
                },
                "entries": [],
            },
            "promotion_paths": (
                artifacts_dir / "discovery-programme-promotions.json",
                artifacts_dir / "discovery-programme-promotions.md",
            ),
            "promotion_counts": {
                "added": 0,
                "updated": 0,
                "deferred": 0,
            },
            "queue_paths": proof_queue_paths(repo_root, kb_ref),
            "branch_outputs": branch_outputs,
        }
    synthesis_report = build_discovery_branch_synthesis_report(
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        repo_root=repo_root,
    )
    synthesis_json, synthesis_md, synthesis_tex, synthesis_pdf = discovery_branch_synthesis_paths(artifacts_dir)
    synthesis_json.write_text(json.dumps(synthesis_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    synthesis_md.write_text(render_discovery_branch_synthesis_markdown(synthesis_report), encoding="utf-8")
    synthesis_tex.write_text(render_discovery_branch_synthesis_tex(synthesis_report), encoding="utf-8")
    compile_discovery_branch_synthesis_pdf(synthesis_tex, synthesis_pdf, preferred_engine="auto")

    expert_report = build_expert_conjecture_report(
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        repo_root=repo_root,
    )
    expert_json, expert_md, expert_tex, expert_pdf = expert_conjecture_paths(artifacts_dir)
    write_expert_conjecture_report(
        expert_report,
        output_json=expert_json,
        output_md=expert_md,
        output_tex=expert_tex,
        output_pdf=expert_pdf,
        latex_engine="auto",
    )
    governor_report, governor_paths = _refresh_discovery_governor(
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        top_k=1 if _clean_text(exact_branch_id) else top_k,
        apply_to_branch_queue=not bool(_clean_text(exact_branch_id)),
    )

    promotion_candidates = build_discovery_programme_promotions(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
    )
    candidate_entries = [
        dict(row)
        for row in _ensure_list(promotion_candidates.get("entries"))
        if isinstance(row, dict)
    ]
    if _clean_text(exact_branch_id):
        candidate_entries = [
            row
            for row in candidate_entries
            if _clean_text(row.get("discovery_branch_id")) == _clean_text(exact_branch_id)
        ]
        for row in candidate_entries:
            row["canonical_branch_id"] = _clean_text(canonical_branch_id)
            row["canonical_hypothesis_id"] = _clean_text(canonical_hypothesis_id)
            row["canonical_proof_obligation_id"] = None
            row["canonical_promotion_authority"] = CANONICAL_AUTHORITY_MODE
    promotion_meta = dict(_ensure_dict(promotion_candidates.get("metadata")))
    promotion_meta["programme_count"] = len(candidate_entries) if promotion_allowed else 0
    promotion_meta["promotion_allowed"] = bool(promotion_allowed)
    promotion_meta["exact_branch_id"] = _clean_text(exact_branch_id)
    promotion_report = {
        "metadata": promotion_meta,
        "entries": candidate_entries if promotion_allowed else [],
    }
    if not promotion_allowed:
        promotion_report["withheld_entries"] = candidate_entries
        promotion_report["metadata"]["withheld_count"] = len(candidate_entries)
        promotion_report["metadata"]["withheld_reason"] = (
            "Non-authoritative legacy compatibility cannot promote discovery outputs."
        )
    promotion_json = artifacts_dir / "discovery-programme-promotions.json"
    promotion_md = artifacts_dir / "discovery-programme-promotions.md"
    promotion_json.write_text(json.dumps(promotion_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    promotion_md.write_text(
        "\n".join(
            [
                "# Discovery Programme Promotions",
                "",
                f"- KB ref: {kb_ref}",
                f"- Source: {_clean_text(_ensure_dict(promotion_report.get('metadata')).get('source'))}",
                f"- Programmes considered: {int(_ensure_dict(promotion_report.get('metadata')).get('programme_count', 0) or 0)}",
                f"- Promotion allowed: {bool(_ensure_dict(promotion_report.get('metadata')).get('promotion_allowed'))}",
                f"- Withheld: {int(_ensure_dict(promotion_report.get('metadata')).get('withheld_count', 0) or 0)}",
                f"- Withheld reason: {_clean_text(_ensure_dict(promotion_report.get('metadata')).get('withheld_reason'))}",
                "",
            ]
            + [
                f"- {_clean_text(row.get('title'))}: {_clean_text(row.get('conjecture_statement'))}"
                for row in _ensure_list(promotion_report.get("entries"))
                if isinstance(row, dict)
            ]
        ).rstrip()
        + "\n",
        encoding="utf-8",
    )
    if not promotion_allowed or not candidate_entries:
        added = updated = deferred = 0
        queue_paths = proof_queue_paths(repo_root, kb_ref)
    elif _clean_text(exact_branch_id):
        queue_json, queue_md = proof_queue_paths(repo_root, kb_ref)
        queue = load_proof_queue(queue_json, kb_ref=kb_ref)
        added, updated = enqueue_entries(queue, candidate_entries)
        deferred = 0
        save_proof_queue(queue, json_path=queue_json, md_path=queue_md)
        refresh_summary_from_sources(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            queue=queue,
        )
        queue_paths = (queue_json, queue_md)
    else:
        _queue, added, updated, deferred, queue_paths = apply_discovery_programme_promotions(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            report=promotion_report,
        )
    synthesis_report = build_discovery_branch_synthesis_report(
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        repo_root=repo_root,
    )
    synthesis_json.write_text(json.dumps(synthesis_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    synthesis_md.write_text(render_discovery_branch_synthesis_markdown(synthesis_report), encoding="utf-8")
    synthesis_tex.write_text(render_discovery_branch_synthesis_tex(synthesis_report), encoding="utf-8")
    compile_discovery_branch_synthesis_pdf(synthesis_tex, synthesis_pdf, preferred_engine="auto")

    return {
        "executed_current_round": True,
        "execution_paths": execution_paths,
        "execution_outputs": execution_outputs,
        "branch_state": execution_state,
        "execution_index": execution_index,
        "synthesis_report": synthesis_report,
        "synthesis_paths": (synthesis_json, synthesis_md, synthesis_tex, synthesis_pdf),
        "expert_report": expert_report,
        "expert_paths": (expert_json, expert_md, expert_tex, expert_pdf),
        "governor_report": governor_report,
        "governor_paths": governor_paths,
        "promotion_report": promotion_report,
        "promotion_paths": (promotion_json, promotion_md),
        "promotion_counts": {
            "added": added,
            "updated": updated,
            "deferred": deferred,
        },
        "queue_paths": queue_paths,
        "branch_outputs": branch_outputs,
    }


def _next_attempt_id(attempt_dir: Path, *, kb_ref: str) -> str:
    """Allocate the next monotonic proof-attempt identifier for this problem."""
    prefix = f"attempt.{kb_ref}."
    current = 0
    if attempt_dir.exists():
        for path in attempt_dir.glob("*.json"):
            name = path.stem
            if not name.startswith(prefix):
                continue
            suffix = name[len(prefix) :]
            if suffix.isdigit():
                current = max(current, int(suffix))
    return f"{prefix}{current + 1:03d}"


def _attempt_paths(artifacts_dir: Path, attempt_id: str) -> tuple[Path, Path]:
    """Return the JSON and Markdown paths for one proof-attempt dossier."""
    attempt_dir = artifacts_dir / "proof-attempts"
    return attempt_dir / f"{attempt_id}.json", attempt_dir / f"{attempt_id}.md"


def _load_attempt_rows(artifacts_dir: Path) -> list[dict[str, Any]]:
    """Load persisted proof-attempt dossiers for local prove-loop diagnostics."""
    attempt_dir = artifacts_dir / "proof-attempts"
    if not attempt_dir.exists():
        return []
    rows: list[dict[str, Any]] = []
    for path in sorted(attempt_dir.glob("*.json")):
        payload = _load_json(path)
        if payload:
            rows.append(payload)
    return rows


def _blocked_result_id(kb_ref: str, *, queue_id: str, attempt_id: str) -> str:
    token = re.sub(r"[^a-z0-9]+", "-", _clean_text(queue_id or attempt_id).lower()).strip("-") or "blocked-result"
    return f"mathlib.{kb_ref}.blocked.{token}"


def _auto_blockable_attempt_rows(queue: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("status")).lower() == "in_progress"
    ]
    rows.sort(
        key=lambda row: (
            -float(row.get("priority", 0.0) or 0.0),
            _clean_text(row.get("queue_id")),
        )
    )
    return rows


def _blocked_mathlib_hits(attempt: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        row
        for row in _ensure_list(_ensure_dict(attempt.get("local_context")).get("mathlib_hits"))
        if isinstance(row, dict) and _clean_text(row.get("outcome")).lower() == "blocked"
    ]


def _attempt_continuation_stage(attempt: dict[str, Any]) -> int:
    metadata = _ensure_dict(attempt.get("metadata"))
    return max(0, _safe_int(metadata.get("continuation_stage")))


def _attempt_ready_for_auto_block(attempt: dict[str, Any]) -> bool:
    metadata = _ensure_dict(attempt.get("metadata"))
    final_assessment = _ensure_dict(attempt.get("final_assessment"))
    proof_attempt = _ensure_dict(attempt.get("proof_attempt"))
    outcome = _clean_text(final_assessment.get("outcome")) or _clean_text(metadata.get("status"))
    if outcome.lower() not in {"", "in_progress"}:
        return False
    if _attempt_continuation_stage(attempt) < 3:
        return False
    if _clean_text(proof_attempt.get("result_statement")) or _clean_text(proof_attempt.get("result_summary")):
        return False
    stepwise_argument = [
        row
        for row in _ensure_list(proof_attempt.get("stepwise_argument"))
        if isinstance(row, dict) and (_clean_text(row.get("claim")) or _clean_text(row.get("justification")))
    ]
    return bool(stepwise_argument)


def _auto_block_summary(attempt: dict[str, Any]) -> tuple[str, str]:
    target = _ensure_dict(attempt.get("target"))
    candidate_object = _clean_text(target.get("candidate_object")) or "current bridge object"
    route_lemma = _clean_text(target.get("missing_route_lemma")) or "the current route lemma"
    blocked_titles = [
        _clean_text(row.get("title")) or _clean_text(row.get("result_id"))
        for row in _blocked_mathlib_hits(attempt)[:3]
        if _clean_text(row.get("title")) or _clean_text(row.get("result_id"))
    ]
    related_blockers = (
        f" Related local blockers: {', '.join(blocked_titles)}."
        if blocked_titles
        else ""
    )
    result_statement = _clean_text(
        f"No local proof currently discharges `{route_lemma}` for `{candidate_object}` from the present artifact state."
    )
    result_summary = _clean_text(
        f"The scaffolded attempt did not discharge `{route_lemma}` for `{candidate_object}` and remains blocked by already-recorded local obstructions.{related_blockers}"
    )
    return result_statement, result_summary


def _append_stepwise_progress(
    proof_attempt: dict[str, Any],
    *,
    claim: str,
    justification: str,
    depends_on: list[str] | None = None,
    status: str = "",
) -> bool:
    claim = _clean_text(claim)
    justification = _clean_text(justification)
    dependencies = [_clean_text(value) for value in (depends_on or []) if _clean_text(value)]
    if not claim and not justification:
        return False
    steps = [dict(row) for row in _ensure_list(proof_attempt.get("stepwise_argument")) if isinstance(row, dict)]
    for row in steps:
        if _clean_text(row.get("claim")) == claim and _clean_text(row.get("justification")) == justification:
            existing = [_clean_text(value) for value in _ensure_list(row.get("depends_on")) if _clean_text(value)]
            for dep in dependencies:
                if dep not in existing:
                    existing.append(dep)
            row["depends_on"] = existing
            if status:
                row["status"] = status
            proof_attempt["stepwise_argument"] = steps
            return False
    step = {
        "step": len(steps) + 1,
        "claim": claim,
        "justification": justification,
        "depends_on": dependencies,
    }
    if status:
        step["status"] = status
    steps.append(step)
    proof_attempt["stepwise_argument"] = steps
    return True


def _update_judge_record(
    attempt: dict[str, Any],
    *,
    judge_id: str,
    verdict: str,
    note: str = "",
    blocker: str = "",
) -> None:
    judges = [row for row in _ensure_list(attempt.get("critique_judges")) if isinstance(row, dict)]
    matched = False
    for row in judges:
        if _clean_text(row.get("judge_id")) != judge_id:
            continue
        matched = True
        row["verdict"] = verdict
        notes = [_clean_text(value) for value in _ensure_list(row.get("notes")) if _clean_text(value)]
        blockers = [_clean_text(value) for value in _ensure_list(row.get("blocking_issues")) if _clean_text(value)]
        if note and note not in notes:
            notes.append(note)
        if blocker and blocker not in blockers:
            blockers.append(blocker)
        row["notes"] = notes
        row["blocking_issues"] = blockers
        break
    if not matched:
        judges.append(
            {
                "judge_id": judge_id,
                "title": judge_id.replace("-", " ").title(),
                "questions": [],
                "verdict": verdict,
                "blocking_issues": [blocker] if blocker else [],
                "notes": [note] if note else [],
            }
        )
    attempt["critique_judges"] = judges


def _record_local_results_used(
    proof_attempt: dict[str, Any],
    *,
    blocked_hits: list[dict[str, Any]],
    route_lemma: str,
) -> int:
    existing = [dict(row) for row in _ensure_list(proof_attempt.get("local_results_used")) if isinstance(row, dict)]
    existing_ids = {_clean_text(row.get("result_id")) for row in existing if _clean_text(row.get("result_id"))}
    added = 0
    for row in blocked_hits[:3]:
        result_id = _clean_text(row.get("result_id"))
        if not result_id or result_id in existing_ids:
            continue
        existing.append(
            {
                "result_id": result_id,
                "title": _clean_text(row.get("title")) or result_id,
                "outcome": _clean_text(row.get("outcome")) or "blocked",
                "role": _clean_text(
                    f"Local blocker relevant to the current route lemma `{route_lemma or 'current route lemma'}`."
                ),
            }
        )
        existing_ids.add(result_id)
        added += 1
    proof_attempt["local_results_used"] = existing
    return added


def _append_continuation_log(
    proof_attempt: dict[str, Any],
    *,
    stage: int,
    headline: str,
    details: list[str],
) -> None:
    log = [dict(row) for row in _ensure_list(proof_attempt.get("continuation_log")) if isinstance(row, dict)]
    log.append(
        {
            "stage": stage,
            "timestamp_utc": _utc_now(),
            "headline": _clean_text(headline),
            "details": [_clean_text(value) for value in details if _clean_text(value)],
        }
    )
    proof_attempt["continuation_log"] = log


def _unique_texts(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        text = _clean_text(value)
        if not text or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return ordered


def _select_constructive_text(
    values: list[Any],
    *,
    keywords: tuple[str, ...],
    preferred_prefixes: tuple[str, ...] = (),
) -> str:
    rows = [_clean_text(value) for value in values if _clean_text(value)]
    ranked: list[tuple[int, int, str]] = []
    if preferred_prefixes:
        for idx, row in enumerate(rows):
            lowered = row.lower()
            if not any(keyword in lowered for keyword in keywords):
                continue
            for prefix_idx, prefix in enumerate(preferred_prefixes):
                if lowered.startswith(prefix):
                    ranked.append((prefix_idx, idx, row))
                    break
        if ranked:
            ranked.sort()
            return ranked[0][2]
    for row in rows:
        lowered = row.lower()
        if all(keyword in lowered for keyword in keywords):
            return row
    for row in rows:
        lowered = row.lower()
        if any(keyword in lowered for keyword in keywords):
            return row
    return rows[0] if rows else ""


def _latest_branch_execution_report(artifacts_dir: Path, *, branch_id: str) -> dict[str, Any]:
    branch_id = _clean_text(branch_id)
    if not branch_id:
        return {}
    execution_dir = artifacts_dir / "discovery-branch-executions"
    index = _load_json(execution_dir / "index.json")
    executions = [
        row
        for row in _ensure_list(_ensure_dict(index).get("executions"))
        if isinstance(row, dict) and _clean_text(row.get("branch_id")) == branch_id
    ]
    for row in executions:
        artifact_json = _clean_text(row.get("artifact_json"))
        if not artifact_json:
            continue
        payload = _load_json(Path(artifact_json))
        if payload:
            return payload
    for path in sorted(execution_dir.glob("*.json"), reverse=True):
        if path.name == "index.json":
            continue
        payload = _load_json(path)
        if _clean_text(_ensure_dict(_ensure_dict(payload).get("metadata")).get("branch_id")) == branch_id:
            return payload
    return {}


def _branch_candidate_title(row: dict[str, Any]) -> str:
    candidate = _ensure_dict(row.get("candidate"))
    return _clean_text(candidate.get("title")) or _clean_text(row.get("title"))


def _branch_candidate_statement(row: dict[str, Any]) -> str:
    candidate = _ensure_dict(row.get("candidate"))
    return _clean_text(candidate.get("theorem_statement")) or _clean_text(row.get("statement"))


def _branch_candidate_shape(row: dict[str, Any]) -> str:
    candidate = _ensure_dict(row.get("candidate"))
    return _clean_text(candidate.get("shape")) or _clean_text(row.get("search_shape"))


def _branch_candidate_object(row: dict[str, Any]) -> str:
    candidate = _ensure_dict(row.get("candidate"))
    candidate_layers = _ensure_dict(candidate.get("mathematical_layers"))
    object_signature = _ensure_dict(candidate_layers.get("object_signature"))
    return (
        _clean_text(row.get("candidate_object"))
        or _clean_text(candidate.get("candidate_object"))
        or _clean_text(object_signature.get("bridge_object"))
    )


def _branch_candidate_obligations(row: dict[str, Any]) -> list[str]:
    candidate = _ensure_dict(row.get("candidate"))
    return _unique_texts(
        [_clean_text(value) for value in _ensure_list(candidate.get("obligations"))]
        + [_clean_text(value) for value in _ensure_list(row.get("obligations"))]
    )


def _branch_candidate_queue_ids(row: dict[str, Any]) -> list[str]:
    candidate = _ensure_dict(row.get("candidate"))
    return _unique_texts(
        [_clean_text(row.get("queue_id"))]
        + [_clean_text(value) for value in _ensure_list(row.get("linked_queue_ids"))]
        + [_clean_text(value) for value in _ensure_list(candidate.get("linked_queue_ids"))]
    )


def _matches_current_route(
    row: dict[str, Any],
    *,
    queue_id: str,
    target_title: str,
    route_lemma: str,
    theorem_statement: str,
    candidate_object: str,
) -> bool:
    linked_queue_ids = _branch_candidate_queue_ids(row)
    if queue_id and queue_id in linked_queue_ids:
        return True
    title = _branch_candidate_title(row)
    statement = _branch_candidate_statement(row)
    branch_object = _branch_candidate_object(row)
    named_targets = {value for value in [target_title, route_lemma] if value}
    if title and title in named_targets:
        return True
    if statement and theorem_statement and statement == theorem_statement:
        return True
    if branch_object and candidate_object and branch_object == candidate_object:
        if title and named_targets and title in named_targets:
            return True
        if statement and theorem_statement and theorem_statement in statement:
            return True
    return False


def _build_positive_subgoal_package(
    *,
    artifacts_dir: Path,
    attempt: dict[str, Any],
) -> dict[str, Any]:
    target = _ensure_dict(attempt.get("target"))
    proof_attempt = _ensure_dict(attempt.get("proof_attempt"))
    expert_context = _ensure_dict(proof_attempt.get("expert_conjecture_context"))
    math_layers = _ensure_dict(target.get("mathematical_layers")) or _ensure_dict(expert_context.get("mathematical_layers"))
    if not math_layers:
        return {}
    object_signature = _ensure_dict(math_layers.get("object_signature"))
    latex = _ensure_dict(math_layers.get("latex"))
    lean_style = _ensure_dict(math_layers.get("lean_style"))
    queue_id = _clean_text(_ensure_dict(attempt.get("metadata")).get("queue_id"))
    target_title = _clean_text(target.get("title"))
    route_lemma = _clean_text(proof_attempt.get("route_lemma_under_test")) or _clean_text(target.get("missing_route_lemma"))
    theorem_statement = _clean_text(proof_attempt.get("theorem_statement")) or _clean_text(target.get("conjecture_statement"))
    candidate_object = _clean_text(object_signature.get("bridge_object")) or _clean_text(target.get("candidate_object"))
    branch_id = _clean_text(target.get("discovery_branch_id"))
    execution_report = _latest_branch_execution_report(artifacts_dir, branch_id=branch_id)
    execution = _ensure_dict(execution_report.get("execution"))
    lean_search = _ensure_dict(execution.get("lean_symbolic_search"))
    theorem_candidates = [
        row
        for row in _ensure_list(execution.get("theorem_candidates"))
        if isinstance(row, dict)
        and _matches_current_route(
            row,
            queue_id=queue_id,
            target_title=target_title,
            route_lemma=route_lemma,
            theorem_statement=theorem_statement,
            candidate_object=candidate_object,
        )
    ]
    lean_candidates = [
        row
        for row in _ensure_list(lean_search.get("candidates"))
        if isinstance(row, dict)
        and _matches_current_route(
            row,
            queue_id=queue_id,
            target_title=target_title,
            route_lemma=route_lemma,
            theorem_statement=theorem_statement,
            candidate_object=candidate_object,
        )
        and _branch_candidate_shape(row) != "obstruction"
    ]
    matched_queue_ids = _unique_texts(
        [queue_id]
        + [value for row in theorem_candidates for value in _branch_candidate_queue_ids(row)]
        + [value for row in lean_candidates for value in _branch_candidate_queue_ids(row)]
    )
    lean_routes = [
        row
        for row in _ensure_list(lean_search.get("routes"))
        if isinstance(row, dict) and _clean_text(row.get("queue_id")) in matched_queue_ids
    ]
    lean_routes.sort(
        key=lambda row: (
            0 if _clean_text(row.get("queue_id")) == queue_id else 1,
            -_safe_int(row.get("lean_readiness_score")),
            -len([value for value in _ensure_list(row.get("search_shapes")) if _clean_text(value) and _clean_text(value) != "obstruction"]),
            _clean_text(row.get("queue_id")),
        )
    )
    lean_route = lean_routes[0] if lean_routes else {}
    candidate_titles = _unique_texts(
        [_branch_candidate_title(row) for row in lean_candidates]
        + [_branch_candidate_title(row) for row in theorem_candidates]
    )
    candidate_obligations = _unique_texts(
        [_clean_text(value) for value in _ensure_list(target.get("proof_obligations"))]
        + [_clean_text(value) for value in _ensure_list(target.get("candidate_lemmas"))]
        + [value for row in theorem_candidates for value in _branch_candidate_obligations(row)]
        + [value for row in lean_candidates for value in _branch_candidate_obligations(row)]
    )
    all_shapes = _unique_texts(
        [_clean_text(value) for row in lean_routes for value in _ensure_list(row.get("search_shapes"))]
        + [_branch_candidate_shape(row) for row in theorem_candidates]
        + [_branch_candidate_shape(row) for row in lean_candidates]
    )
    positive_shapes = [value for value in all_shapes if value != "obstruction"]
    bridge_object = candidate_object
    bridge_witness = _clean_text(object_signature.get("bridge_witness")) or "BW(W)"
    route_object = _clean_text(object_signature.get("route_object")) or "R(W)"
    target_object = _clean_text(object_signature.get("target_object")) or "T(W)"
    invariant = _clean_text(object_signature.get("invariant")) or _clean_text(target.get("preserved_invariant"))
    quantifier_signature = _clean_text(math_layers.get("quantifier_signature"))
    readiness = _ensure_dict(lean_route.get("readiness"))
    next_constructive_steps = _unique_texts(
        [
            _clean_text(
                f"Construct a concrete witness `{bridge_witness}` for `{bridge_object}` under `{quantifier_signature or 'the local admissibility assumptions'}`."
            ),
            _clean_text(
                f"Prove that `{bridge_witness}` preserves `{invariant}` while mediating from `{route_object}` to `{target_object}`."
            ),
            _clean_text(
                f"Expose the exact target-activation clause proving `{bridge_witness}` is strong enough to realize `{_clean_text(target.get('target_statement_id')) or 'the queued target theorem'}`."
            ),
        ]
        + (
            [_clean_text(f"Realize the positive bridge shape `{positive_shapes[0]}` before revisiting any obstruction conclusion.")]
            if positive_shapes
            else []
        )
        + candidate_obligations[:2]
    )
    return {
        "status": "generated",
        "source": "mathematical_layers+branch_execution" if execution_report else "mathematical_layers-only",
        "supporting_branch_execution_id": _clean_text(_ensure_dict(execution_report.get("metadata")).get("execution_id")),
        "route_lemma": route_lemma,
        "constructive_goal": theorem_statement,
        "quantifier_signature": quantifier_signature,
        "latex_theorem": _clean_text(latex.get("theorem_statement")),
        "lean_theorem_name": _clean_text(lean_style.get("theorem_name")),
        "bridge_object": bridge_object,
        "bridge_witness_symbol": bridge_witness,
        "route_object": route_object,
        "target_object": target_object,
        "preserved_invariant": invariant,
        "admissibility_conditions": _unique_texts(_ensure_list(target.get("admissibility_conditions"))),
        "readiness_mode": _clean_text(readiness.get("mode")),
        "readiness_score": _safe_int(lean_route.get("lean_readiness_score") or readiness.get("score")),
        "readiness_reasons": _unique_texts(_ensure_list(readiness.get("reasons"))),
        "search_shapes": all_shapes,
        "positive_shapes": positive_shapes,
        "candidate_titles": candidate_titles,
        "candidate_obligations": candidate_obligations,
        "next_constructive_steps": next_constructive_steps,
    }


def _active_attempt_records(
    *,
    artifacts_dir: Path,
    queue: dict[str, Any],
) -> list[dict[str, Any]]:
    queue_by_id = {
        _clean_text(row.get("queue_id")): row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("queue_id"))
    }
    rows: list[dict[str, Any]] = []
    for attempt in _load_attempt_rows(artifacts_dir):
        metadata = _ensure_dict(attempt.get("metadata"))
        final_assessment = _ensure_dict(attempt.get("final_assessment"))
        status = _clean_text(metadata.get("status")).lower()
        outcome = _clean_text(final_assessment.get("outcome")).lower()
        if status != "in_progress" and outcome != "in_progress":
            continue
        attempt_id = _clean_text(metadata.get("attempt_id"))
        queue_id = _clean_text(metadata.get("queue_id"))
        rows.append(
            {
                "attempt_id": attempt_id,
                "queue_id": queue_id,
                "attempt": attempt,
                "attempt_json": _attempt_paths(artifacts_dir, attempt_id)[0],
                "attempt_md": _attempt_paths(artifacts_dir, attempt_id)[1],
                "queue_row": _ensure_dict(queue_by_id.get(queue_id)),
            }
        )
    rows.sort(
        key=lambda row: (
            _clean_text(_ensure_dict(_ensure_dict(row.get("attempt")).get("metadata")).get("started_utc")),
            _clean_text(row.get("attempt_id")),
        )
    )
    return rows


def _resume_attempt_record(
    *,
    artifacts_dir: Path,
    kb_ref: str,
    attempt_record: dict[str, Any],
) -> dict[str, Any]:
    attempt = _ensure_dict(attempt_record.get("attempt"))
    attempt_json = Path(attempt_record["attempt_json"])
    attempt_md = Path(attempt_record["attempt_md"])
    metadata = _ensure_dict(attempt.get("metadata"))
    target = _ensure_dict(attempt.get("target"))
    local_context = _ensure_dict(attempt.get("local_context"))
    proof_attempt = _ensure_dict(attempt.get("proof_attempt"))
    final_assessment = _ensure_dict(attempt.get("final_assessment"))
    blocked_hits = _blocked_mathlib_hits(attempt)
    blocked_titles = [
        _clean_text(row.get("title")) or _clean_text(row.get("result_id"))
        for row in blocked_hits[:3]
        if _clean_text(row.get("title")) or _clean_text(row.get("result_id"))
    ]
    blocked_result_ids = [_clean_text(row.get("result_id")) for row in blocked_hits[:3] if _clean_text(row.get("result_id"))]
    theorem_statement = _clean_text(proof_attempt.get("theorem_statement"))
    route_lemma = _clean_text(proof_attempt.get("route_lemma_under_test")) or _clean_text(target.get("missing_route_lemma"))
    assumptions = [_clean_text(row) for row in _ensure_list(proof_attempt.get("assumptions")) if _clean_text(row)]
    failure_diagnosis = _clean_text(target.get("failure_diagnosis"))
    negative_route = _clean_text(target.get("negative_route"))
    candidate_object = _clean_text(target.get("candidate_object")) or "the candidate bridge object"
    invariant = _clean_text(target.get("preserved_invariant")) or "the current route invariant"
    target_statement_id = _clean_text(target.get("target_statement_id"))
    target_excerpt = _clean_text(local_context.get("target_excerpt")) or _clean_text(target.get("target_excerpt"))
    strategy = _clean_text(proof_attempt.get("strategy")) or _clean_text(target.get("proof_strategy_family"))
    continuation_stage = _attempt_continuation_stage(attempt)
    positive_subgoal_package = _build_positive_subgoal_package(artifacts_dir=artifacts_dir, attempt=attempt)
    positive_shapes = _ensure_list(positive_subgoal_package.get("positive_shapes"))
    candidate_obligations = _ensure_list(positive_subgoal_package.get("candidate_obligations"))
    constructive_steps = _ensure_list(positive_subgoal_package.get("next_constructive_steps"))
    readiness_mode = _clean_text(positive_subgoal_package.get("readiness_mode"))
    readiness_score = _safe_int(positive_subgoal_package.get("readiness_score"))
    supporting_execution_id = _clean_text(positive_subgoal_package.get("supporting_branch_execution_id"))
    lean_theorem_name = _clean_text(positive_subgoal_package.get("lean_theorem_name"))
    bridge_witness_symbol = _clean_text(positive_subgoal_package.get("bridge_witness_symbol"))
    route_object = _clean_text(positive_subgoal_package.get("route_object")) or "R(W)"
    target_object = _clean_text(positive_subgoal_package.get("target_object")) or "T(W)"
    contradiction_frame = _ensure_dict(proof_attempt.get("contradiction_frame"))
    negative_argument = _ensure_dict(proof_attempt.get("negative_argument"))

    if not _clean_text(negative_argument.get("obstruction_candidate")) and negative_route:
        negative_argument["obstruction_candidate"] = negative_route
    if not _clean_text(negative_argument.get("negated_claim")) and negative_route:
        negative_argument["negated_claim"] = negative_route
    if not _clean_text(negative_argument.get("contradiction_target")):
        negative_argument["contradiction_target"] = _clean_text(target.get("target_statement_id")) or route_lemma
    if not _clean_text(negative_argument.get("forbidden_outcome")) and failure_diagnosis:
        negative_argument["forbidden_outcome"] = failure_diagnosis
    if not _clean_text(negative_argument.get("effect_on_claim")) and failure_diagnosis:
        negative_argument["effect_on_claim"] = failure_diagnosis
    if not _clean_text(negative_argument.get("impossibility_claim")) and theorem_statement.lower().startswith(("no ", "there is no", "there exists no")):
        negative_argument["impossibility_claim"] = theorem_statement

    if not _clean_text(contradiction_frame.get("negated_claim")) and _clean_text(negative_argument.get("negated_claim")):
        contradiction_frame["negated_claim"] = negative_argument.get("negated_claim")
    if not _clean_text(contradiction_frame.get("contradiction_target")) and _clean_text(negative_argument.get("contradiction_target")):
        contradiction_frame["contradiction_target"] = negative_argument.get("contradiction_target")
    if not _clean_text(contradiction_frame.get("forbidden_outcome")) and _clean_text(negative_argument.get("forbidden_outcome")):
        contradiction_frame["forbidden_outcome"] = negative_argument.get("forbidden_outcome")
    if not _clean_text(contradiction_frame.get("impossibility_claim_template")) and _clean_text(negative_argument.get("impossibility_claim")):
        contradiction_frame["impossibility_claim_template"] = negative_argument.get("impossibility_claim")

    tactic_trace = [row for row in _ensure_list(proof_attempt.get("informal_tactic_trace")) if isinstance(row, dict)]
    completed = 0
    in_progress = 0
    for row in tactic_trace:
        tactic_id = _clean_text(row.get("tactic_id"))
        notes = [str(note) for note in _ensure_list(row.get("notes"))]
        if tactic_id == "normalize-goal" and theorem_statement:
            row["status"] = "completed"
            note = "The theorem statement is already normalized as the local claim under test."
        elif tactic_id == "introduce-assumptions" and assumptions:
            row["status"] = "completed"
            note = "The dossier already exposes the local assumptions and admissibility clauses."
        elif tactic_id == "reduce-to-route-lemma" and route_lemma:
            row["status"] = "completed"
            note = f"The route lemma `{route_lemma}` is already the explicit prove-time subgoal."
        elif tactic_id == "extract-subgoal" and route_lemma:
            row["status"] = "completed"
            note = f"The subgoal `{route_lemma}` is already named in the current dossier."
        elif tactic_id == "construct-witness" and candidate_object:
            row["status"] = "in_progress"
            note = _clean_text(
                (constructive_steps or [f"The live burden is to realize `{candidate_object}` concretely rather than keep it as a role-description."])[0]
            )
        elif tactic_id == "transport-invariant" and invariant:
            row["status"] = "in_progress"
            note = _clean_text(
                (constructive_steps + [f"The next local burden is to preserve `{invariant}` across the route-specific realization step."])[1]
            )
        elif tactic_id == "activate-target-theorem" and target_statement_id:
            row["status"] = "completed"
            note = f"Target activation is reduced to discharging `{route_lemma or target_statement_id}` against `{target_statement_id}`."
        elif tactic_id == "negate-goal" and _clean_text(negative_argument.get("negated_claim")):
            row["status"] = "completed"
            note = "The negated branch has been made explicit from the queue packet."
        elif tactic_id == "obstruction-probe" and blocked_titles:
            row["status"] = "completed"
            note = f"Local obstruction analogues already exist in InformalMathLib: {', '.join(blocked_titles)}."
        elif tactic_id == "obstruction-probe" and (_clean_text(negative_argument.get("forbidden_outcome")) or failure_diagnosis):
            row["status"] = "in_progress"
            note = _clean_text(negative_argument.get("forbidden_outcome")) or failure_diagnosis
        elif tactic_id == "derive-contradiction" and blocked_titles:
            row["status"] = "in_progress"
            note = f"Any contradiction route must separate the current packet from nearby blockers: {', '.join(blocked_titles)}."
        elif tactic_id == "prove-impossibility-claim" and _clean_text(negative_argument.get("impossibility_claim")):
            row["status"] = "in_progress"
            note = "The current theorem statement is already shaped like a negative local claim."
        else:
            continue
        if note and note not in notes:
            notes.append(note)
        row["notes"] = notes
        status = _clean_text(row.get("status")).lower()
        if status == "completed":
            completed += 1
        elif status == "in_progress":
            in_progress += 1

    added_steps = 0
    added_results = _record_local_results_used(
        proof_attempt,
        blocked_hits=blocked_hits,
        route_lemma=route_lemma,
    )
    if positive_subgoal_package:
        proof_attempt["positive_subgoal_package"] = positive_subgoal_package
    if continuation_stage < 1:
        activation_step = _clean_text(
            f"Reduce target activation to the explicit route lemma `{route_lemma or target_statement_id or 'current route lemma'}` for `{candidate_object}`."
        )
        activation_justification = _clean_text(
            f"Under strategy `{strategy or 'current proof strategy'}`, the target theorem `{target_statement_id or target_excerpt or 'the queued target'}` activates only after the route-local realization burden is discharged."
        )
        if _append_stepwise_progress(
            proof_attempt,
            claim=activation_step,
            justification=activation_justification,
            depends_on=[route_lemma, target_statement_id],
            status="in_progress",
        ):
            added_steps += 1
        positive_step = _clean_text(
            (constructive_steps or [f"Construct a concrete witness for `{candidate_object}`."])[0]
        )
        positive_justification = _clean_text(
            f"The constructive packet exposes `{bridge_witness_symbol or 'the bridge witness'}` "
            f"with shapes {', '.join(positive_shapes[:3]) or 'not-yet-typed'} "
            f"and route lemma `{route_lemma or 'current route lemma'}`."
        )
        if _append_stepwise_progress(
            proof_attempt,
            claim=positive_step,
            justification=positive_justification,
            depends_on=[route_lemma] + [lean_theorem_name],
            status="in_progress",
        ):
            added_steps += 1
        if candidate_obligations:
            obligation_step = _clean_text(
                candidate_obligations[0]
            )
            obligation_justification = _clean_text(
                f"Lean/math packet evidence now isolates this as an explicit constructive obligation for `{candidate_object}`."
            )
            if _append_stepwise_progress(
                proof_attempt,
                claim=obligation_step,
                justification=obligation_justification,
                depends_on=[route_lemma],
                status="in_progress",
            ):
                added_steps += 1
        if blocked_titles:
            blocker_step = _clean_text(
                f"Record the nearest local blockers for `{route_lemma or 'the current route lemma'}` instead of restarting the same realization pattern."
            )
            blocker_justification = _clean_text(
                f"InformalMathLib already records nearby blocked routes: {', '.join(blocked_titles)}."
            )
            if _append_stepwise_progress(
                proof_attempt,
                claim=blocker_step,
                justification=blocker_justification,
                depends_on=blocked_result_ids,
                status="completed",
            ):
                added_steps += 1
            negative_argument["counterexample_or_barrier"] = _clean_text(
                negative_argument.get("counterexample_or_barrier")
            ) or blocker_justification
            negative_argument["effect_on_claim"] = _clean_text(negative_argument.get("effect_on_claim")) or _clean_text(
                f"The constructive route remains open only if `{candidate_object}` avoids the obstruction pattern already seen in {', '.join(blocked_titles)}."
            )
        _append_continuation_log(
            proof_attempt,
            stage=1,
            headline="Grounded the active proof state against local blockers, target activation, and a constructive subgoal packet.",
            details=[
                activation_step,
                activation_justification,
                _clean_text(
                    f"Constructive packet shapes: {', '.join(positive_shapes[:3])}."
                    if positive_shapes
                    else "Constructive packet is currently sourced from mathematical layers without additional Lean shape evidence."
                ),
                _clean_text(
                    f"Primary constructive witness symbol: `{bridge_witness_symbol}`."
                    if bridge_witness_symbol
                    else ""
                ),
                _clean_text(
                    f"Imported {added_results} local InformalMathLib blockers into the dossier."
                    if added_results
                    else "No new local InformalMathLib blocker had to be imported."
                ),
            ],
        )
        _update_judge_record(
            attempt,
            judge_id="statement-grounding",
            verdict="passes",
            note="The resumed attempt now grounds the live goal against the named route lemma and target theorem.",
        )
        _update_judge_record(
            attempt,
            judge_id="tactic-goal-control",
            verdict="passes",
            note=f"The prove loop keeps the focus on `{route_lemma or target_statement_id or 'the queued target'}`.",
        )
        _update_judge_record(
            attempt,
            judge_id="tactic-subgoal-exposure",
            verdict="passes",
            note=(
                f"The constructive packet now exposes `{bridge_witness_symbol or 'the bridge witness'}` "
                f"and {len(candidate_obligations)} explicit constructive obligation(s)."
            ),
        )
        _update_judge_record(
            attempt,
            judge_id="tactic-trace-discipline",
            verdict="passes",
            note="The tactic trace was updated from template state into explicit completed and in-progress checkpoints.",
        )
        _update_judge_record(
            attempt,
            judge_id="local-counterexample-search",
            verdict="in_progress",
            note=(
                f"Nearby blocked local results were imported: {', '.join(blocked_titles)}."
                if blocked_titles
                else "No local blocker is known yet; the obstruction search remains open."
            ),
        )
        _update_judge_record(
            attempt,
            judge_id="obstruction-and-negative-route",
            verdict="in_progress",
            note=_clean_text(negative_argument.get("effect_on_claim")) or failure_diagnosis,
        )
        continuation_stage = 1
    elif continuation_stage < 2:
        realization_claim = ""
        if "realization" in positive_shapes:
            realization_claim = _select_constructive_text(
                constructive_steps + candidate_obligations,
                keywords=("realiz", "construct", "build"),
                preferred_prefixes=("construct", "realize", "build"),
            ) or _clean_text(
                f"Realize `{candidate_object}` as an admissible carrier witnessed by `{bridge_witness_symbol or 'the bridge witness'}`."
            )
            realization_justification = _clean_text(
                f"Branch execution `{supporting_execution_id or 'the current discovery branch'}` keeps `realization` live for `{candidate_object}` rather than collapsing immediately into the obstruction route."
            )
            if _append_stepwise_progress(
                proof_attempt,
                claim=realization_claim,
                justification=realization_justification,
                depends_on=[route_lemma, lean_theorem_name] + blocked_result_ids,
                status="in_progress",
            ):
                added_steps += 1
        else:
            realization_justification = ""

        transport_claim = ""
        if "transport" in positive_shapes:
            transport_claim = _select_constructive_text(
                candidate_obligations + constructive_steps,
                keywords=("transport",),
                preferred_prefixes=("define", "transport", "prove"),
            ) or _clean_text(
                f"Define the transport from `{route_object}` to `{target_object}` and prove that it preserves `{invariant}`."
            )
            transport_justification = _clean_text(
                f"Lean/branch evidence isolates `transport` as a live positive shape for `{candidate_object}`, so the next local burden is to make the map from `{route_object}` to `{target_object}` explicit."
            )
            if _append_stepwise_progress(
                proof_attempt,
                claim=transport_claim,
                justification=transport_justification,
                depends_on=[route_lemma, lean_theorem_name],
                status="in_progress",
            ):
                added_steps += 1
        else:
            transport_justification = ""

        factorization_claim = ""
        if "factorization" in positive_shapes:
            factorization_claim = _select_constructive_text(
                candidate_obligations + constructive_steps,
                keywords=("factor", "mediate", "intermediate"),
                preferred_prefixes=("exhibit", "factor", "build", "introduce"),
            ) or _clean_text(
                f"Exhibit an intermediate typed object factoring the route from `{route_object}` to `{target_object}` through `{candidate_object}`."
            )
            factorization_justification = _clean_text(
                f"Lean/branch evidence keeps `factorization` live for `{candidate_object}`, so the next local burden is to make the mediating object and factorization law explicit."
            )
            if _append_stepwise_progress(
                proof_attempt,
                claim=factorization_claim,
                justification=factorization_justification,
                depends_on=[route_lemma, lean_theorem_name],
                status="in_progress",
            ):
                added_steps += 1
        else:
            factorization_justification = ""

        equivalence_claim = ""
        if "equivalence" in positive_shapes:
            equivalence_claim = _select_constructive_text(
                candidate_obligations + constructive_steps,
                keywords=("equivalence", "equivalent", "coherence", "naturality"),
                preferred_prefixes=("construct", "prove", "determine", "exhibit"),
            ) or _clean_text(
                f"Construct an explicit equivalence witness between `{route_object}` and `{target_object}` for `{candidate_object}`."
            )
            equivalence_justification = _clean_text(
                f"Lean/branch evidence keeps `equivalence` live for `{candidate_object}`, so the next local burden is to make the witness and its coherence or naturality law explicit."
            )
            if _append_stepwise_progress(
                proof_attempt,
                claim=equivalence_claim,
                justification=equivalence_justification,
                depends_on=[route_lemma, lean_theorem_name],
                status="in_progress",
            ):
                added_steps += 1
        else:
            equivalence_justification = ""

        shape_focus_claim = _clean_text(
            f"Keep the constructive branch on shapes `{', '.join(positive_shapes[:3])}` before promoting the impossibility route."
            if positive_shapes
            else f"Keep the constructive branch on the explicit route lemma `{route_lemma or 'current route lemma'}` before promoting the impossibility route."
        )
        shape_focus_justification = _clean_text(
            f"Readiness mode `{readiness_mode or 'unclassified'}` with score `{readiness_score}` still supports bounded constructive pressure on `{candidate_object}`."
        )
        if _append_stepwise_progress(
            proof_attempt,
            claim=shape_focus_claim,
            justification=shape_focus_justification,
            depends_on=[route_lemma] + ([supporting_execution_id] if supporting_execution_id else []),
            status="in_progress",
        ):
            added_steps += 1

        _append_continuation_log(
            proof_attempt,
            stage=2,
            headline="Pressed the constructive branch through shape-specific obligations before escalating to obstruction.",
            details=[
                _clean_text(
                    f"Positive shapes kept live: {', '.join(positive_shapes[:3])}."
                    if positive_shapes
                    else "No positive shape is yet typed tightly enough to outrank the negative branch."
                ),
                _clean_text(
                    f"Readiness mode `{readiness_mode}` with score `{readiness_score}` comes from branch execution `{supporting_execution_id}`."
                    if readiness_mode or supporting_execution_id
                    else ""
                ),
                realization_claim,
                realization_justification,
                transport_claim,
                transport_justification,
                factorization_claim,
                factorization_justification,
                equivalence_claim,
                equivalence_justification,
                shape_focus_claim,
            ],
        )
        _update_judge_record(
            attempt,
            judge_id="tactic-subgoal-exposure",
            verdict="passes",
            note=(
                f"Shape-specific constructive obligations are now explicit: {', '.join(positive_shapes[:3]) or 'route-local constructive pressure only'}."
            ),
        )
        _update_judge_record(
            attempt,
            judge_id="inferential-validity",
            verdict="in_progress",
            note=(
                f"The constructive continuation now separates {', '.join(positive_shapes[:3]) or 'constructive'} obligations for `{candidate_object}` instead of collapsing them into a single obstruction summary."
            ),
        )
        _update_judge_record(
            attempt,
            judge_id="obstruction-and-negative-route",
            verdict="in_progress",
            note=_clean_text(
                f"Constructive shapes remain live on `{candidate_object}`: {', '.join(positive_shapes[:3])}."
                if positive_shapes
                else f"The constructive route remains primary on `{route_lemma or candidate_object}`."
            ),
        )
        _update_judge_record(
            attempt,
            judge_id="contradiction-and-impossibility-discipline",
            verdict="pending",
            note="The impossibility branch is intentionally deferred until the shape-specific constructive obligations have been pressed further.",
        )
        continuation_stage = 2
    else:
        impossibility_claim = _clean_text(negative_argument.get("impossibility_claim")) or _clean_text(
            f"No admissible `{candidate_object}` currently discharges `{route_lemma or 'the current route lemma'}` while preserving `{invariant}` from the present artifact state."
        )
        negative_argument["impossibility_claim"] = impossibility_claim
        if not _clean_text(negative_argument.get("effect_on_claim")):
            negative_argument["effect_on_claim"] = _clean_text(
                f"Without a witness escaping the current obstruction pattern, `{route_lemma or 'the current route lemma'}` remains unjustified."
            )
        contradiction_frame["impossibility_claim_template"] = _clean_text(
            contradiction_frame.get("impossibility_claim_template")
        ) or impossibility_claim
        contradiction_frame["contradiction_target"] = _clean_text(contradiction_frame.get("contradiction_target")) or (
            _clean_text(negative_argument.get("contradiction_target")) or route_lemma or target_statement_id
        )
        barrier_step = _clean_text(
            f"Formulate the route-local impossibility candidate `{impossibility_claim}`."
        )
        barrier_justification = _clean_text(
            f"The negative route `{negative_route or 'current obstruction route'}` is now sharpened against local blockers and the missing route lemma `{route_lemma or 'current route lemma'}`."
        )
        if _append_stepwise_progress(
            proof_attempt,
            claim=barrier_step,
            justification=barrier_justification,
            depends_on=blocked_result_ids + [route_lemma],
            status="in_progress",
        ):
            added_steps += 1
        if blocked_titles:
            separation_step = _clean_text(
                f"Any future constructive continuation must separate `{candidate_object}` from the obstruction pattern already recorded locally."
            )
            separation_justification = _clean_text(
                f"Without a witness escaping {', '.join(blocked_titles)}, target activation remains unjustified."
            )
            if _append_stepwise_progress(
                proof_attempt,
                claim=separation_step,
                justification=separation_justification,
                depends_on=blocked_result_ids,
                status="in_progress",
            ):
                added_steps += 1
            negative_argument["counterexample_or_barrier"] = _clean_text(
                negative_argument.get("counterexample_or_barrier")
            ) or separation_justification
        for row in tactic_trace:
            tactic_id = _clean_text(row.get("tactic_id"))
            notes = [str(note) for note in _ensure_list(row.get("notes"))]
            if tactic_id == "negate-goal":
                row["status"] = "completed"
                note = "The route-local impossibility candidate now exposes the explicit negated branch."
            elif tactic_id == "prove-impossibility-claim":
                row["status"] = "in_progress"
                note = impossibility_claim
            elif tactic_id == "derive-contradiction" and blocked_titles:
                row["status"] = "in_progress"
                note = f"The contradiction route remains tied to local blockers: {', '.join(blocked_titles)}."
            else:
                continue
            if note and note not in notes:
                notes.append(note)
            row["notes"] = notes
        _append_continuation_log(
            proof_attempt,
            stage=3,
            headline="Synthesized the negative branch into a theorem-shaped impossibility candidate.",
            details=[
                barrier_step,
                _clean_text(
                    f"Constructive packet remained open on shapes {', '.join(positive_shapes[:3])}."
                    if positive_shapes
                    else "No additional constructive shape escaped the obstruction packet."
                ),
                _clean_text(
                    negative_argument.get("effect_on_claim")
                    or f"The live constructive burden is to escape the current obstruction pattern for `{candidate_object}`."
                ),
            ],
        )
        _update_judge_record(
            attempt,
            judge_id="local-counterexample-search",
            verdict="passes",
            note=(
                f"The resumed dossier now ties the route to concrete local blockers: {', '.join(blocked_titles)}."
                if blocked_titles
                else "The local counterexample search stayed negative, so the route remains open but unsupported."
            ),
        )
        _update_judge_record(
            attempt,
            judge_id="obstruction-and-negative-route",
            verdict="blocking" if blocked_titles else "in_progress",
            note=_clean_text(negative_argument.get("effect_on_claim")),
            blocker=_clean_text(negative_argument.get("counterexample_or_barrier")),
        )
        _update_judge_record(
            attempt,
            judge_id="contradiction-and-impossibility-discipline",
            verdict="in_progress",
            note=impossibility_claim,
        )
        continuation_stage = 3

    metadata["updated_utc"] = _utc_now()
    metadata["resume_count"] = _safe_int(metadata.get("resume_count")) + 1
    metadata["continuation_stage"] = continuation_stage
    proof_attempt["informal_tactic_trace"] = tactic_trace
    proof_attempt["negative_argument"] = negative_argument
    proof_attempt["contradiction_frame"] = contradiction_frame
    attempt["metadata"] = metadata
    attempt["proof_attempt"] = proof_attempt
    attempt["final_assessment"] = final_assessment
    refresh_attempt_inference_diagnosis(attempt)
    attempt["pdl_program"] = serialize_proof_attempt_as_pdl(attempt)
    attempt_json.write_text(json.dumps(attempt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    attempt_md.write_text(render_attempt_markdown(attempt), encoding="utf-8")
    refresh_summary_from_sources(repo_root=Path(__file__).resolve().parents[4], artifacts_dir=artifacts_dir, kb_ref=kb_ref)
    return {
        "attempt_id": _clean_text(metadata.get("attempt_id")),
        "queue_id": _clean_text(metadata.get("queue_id")),
        "proof_attempt_json": str(attempt_json),
        "proof_attempt_md": str(attempt_md),
        "continuation_stage": continuation_stage,
        "blocked_hit_count": len(blocked_hits),
        "added_local_results": added_results,
        "added_step_count": added_steps,
        "completed_tactic_count": completed,
        "active_tactic_count": in_progress,
        "forbidden_outcome": _clean_text(negative_argument.get("forbidden_outcome")),
    }


def _auto_finalize_scaffold_attempt(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    queue: dict[str, Any],
    mathlib: dict[str, Any],
) -> dict[str, Any]:
    queue_json, queue_md = proof_queue_paths(repo_root, kb_ref)
    for row in _auto_blockable_attempt_rows(queue):
        attempt_ids = [value for value in _ensure_list(row.get("attempt_ids")) if _clean_text(value)]
        if not attempt_ids:
            continue
        attempt_id = _clean_text(attempt_ids[-1])
        attempt_json, attempt_md = _attempt_paths(artifacts_dir, attempt_id)
        attempt = _load_json(attempt_json)
        if not attempt or not _attempt_ready_for_auto_block(attempt):
            continue
        blocked_hits = _blocked_mathlib_hits(attempt)
        if not blocked_hits:
            continue

        proof_attempt = _ensure_dict(attempt.get("proof_attempt"))
        final_assessment = _ensure_dict(attempt.get("final_assessment"))
        target = _ensure_dict(attempt.get("target"))
        result_statement, result_summary = _auto_block_summary(attempt)
        proof_attempt["result_statement"] = _clean_text(proof_attempt.get("result_statement")) or result_statement
        proof_attempt["result_summary"] = _clean_text(proof_attempt.get("result_summary")) or result_summary
        negative_argument = _ensure_dict(proof_attempt.get("negative_argument"))
        negative_argument["effect_on_claim"] = _clean_text(negative_argument.get("effect_on_claim")) or result_summary
        proof_attempt["negative_argument"] = negative_argument
        final_assessment["outcome"] = "blocked"
        final_assessment["verdict"] = "blocked"
        final_assessment["confidence"] = _clean_text(final_assessment.get("confidence")) or "low"
        final_assessment["summary"] = _clean_text(final_assessment.get("summary")) or result_summary
        metadata = _ensure_dict(attempt.get("metadata"))
        metadata["status"] = "blocked"
        attempt["metadata"] = metadata
        attempt["proof_attempt"] = proof_attempt
        attempt["final_assessment"] = final_assessment
        refresh_attempt_inference_diagnosis(attempt)
        attempt_json.write_text(json.dumps(attempt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        attempt_md.write_text(render_attempt_markdown(attempt), encoding="utf-8")

        queue_id = _clean_text(metadata.get("queue_id")) or _clean_text(row.get("queue_id"))
        result_id = _blocked_result_id(kb_ref, queue_id=queue_id, attempt_id=attempt_id)
        result = {
            "result_id": result_id,
            "queue_id": queue_id,
            "attempt_id": attempt_id,
            "bridge_id": _clean_text(target.get("bridge_id")) or _clean_text(row.get("bridge_id")),
            "source_statement_id": _clean_text(target.get("source_statement_id")) or _clean_text(row.get("source_statement_id")),
            "target_statement_id": _clean_text(target.get("target_statement_id")) or _clean_text(row.get("target_statement_id")),
            "outcome": "blocked",
            "title": _clean_text(target.get("title")) or _clean_text(row.get("title")) or "Blocked route",
            "entry_kind": "negative-local-theorem",
            "statement": proof_attempt["result_statement"],
            "summary": final_assessment["summary"],
            "tags": [
                _clean_text(target.get("candidate_object")) or _clean_text(row.get("candidate_object")),
                _clean_text(target.get("preserved_invariant")) or _clean_text(row.get("preserved_invariant")),
                _clean_text(target.get("proof_strategy_family")) or _clean_text(row.get("proof_strategy_family")),
            ],
            "web_search_used": bool(_ensure_list(_ensure_dict(attempt.get("web_search_gate")).get("sources"))),
            "major_subresult_score": 0,
            "major_subresult_candidate": False,
        }
        artifact_path = write_mathlib_result_file(
            repo_root,
            kb_ref=kb_ref,
            result=result,
            proof_markdown=attempt_md.read_text(encoding="utf-8"),
        )
        result["artifact_path"] = str(artifact_path)
        append_mathlib_result(mathlib, result)
        mathlib_json, mathlib_md = mathlib_paths(repo_root, kb_ref)
        save_mathlib_index(mathlib, json_path=mathlib_json, md_path=mathlib_md)
        finalize_queue_entry(
            queue,
            queue_id=queue_id,
            outcome="blocked",
            result_id=result_id,
            attempt_id=attempt_id,
            summary=final_assessment["summary"],
        )
        save_proof_queue(queue, json_path=queue_json, md_path=queue_md)
        refresh_summary_from_sources(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            queue=queue,
            mathlib=mathlib,
        )
        return {
            "attempt_id": attempt_id,
            "queue_id": queue_id,
            "result_id": result_id,
            "summary": final_assessment["summary"],
            "proof_attempt_json": str(attempt_json),
            "proof_attempt_md": str(attempt_md),
            "proof_queue_json": str(queue_json),
            "mathlib_json": str(mathlib_json),
        }
    return {}


def _run_exact_discovery_phase(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    exact_branch_id: str,
    expected_branch_digest: str,
    canonical_branch_id: str,
    canonical_hypothesis_id: str,
) -> dict[str, Any]:
    """Execute and promote only one preflight-bound canonical discovery branch."""

    validate_identifier(exact_branch_id, "local discovery branch ID")
    validate_digest(expected_branch_digest)
    validate_identifier(canonical_branch_id, "canonical branch ID")
    validate_identifier(canonical_hypothesis_id, "canonical hypothesis ID")
    branch_outputs = discovery_branch_queue_paths(artifacts_dir)
    result = _run_branch_to_theorem_pipeline(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        branch_outputs=branch_outputs,
        top_k=1,
        exact_branch_id=exact_branch_id,
        expected_branch_digest=expected_branch_digest,
        canonical_branch_id=canonical_branch_id,
        canonical_hypothesis_id=canonical_hypothesis_id,
        promotion_allowed=True,
    )
    promotion_counts = _ensure_dict(result.get("promotion_counts"))
    outputs: dict[str, str] = {
        "discovery_branch_queue_json": str(branch_outputs[0]),
        "discovery_branch_queue_md": str(branch_outputs[1]),
        "discovery_branch_execution_index_json": str(result["execution_paths"][0]),
        "discovery_branch_execution_index_md": str(result["execution_paths"][1]),
    }
    if result.get("executed_current_round"):
        for key, paths in (
            ("discovery_branch_synthesis", result["synthesis_paths"]),
            ("expert_conjectures", result["expert_paths"]),
        ):
            outputs[f"{key}_json"] = str(paths[0])
            outputs[f"{key}_md"] = str(paths[1])
            outputs[f"{key}_tex"] = str(paths[2])
            outputs[f"{key}_pdf"] = str(paths[3])
        outputs["discovery_governor_report_json"] = str(result["governor_paths"][0])
        outputs["discovery_governor_report_md"] = str(result["governor_paths"][1])
        outputs["discovery_programme_promotions_json"] = str(result["promotion_paths"][0])
        outputs["discovery_programme_promotions_md"] = str(result["promotion_paths"][1])
        for row in result.get("execution_outputs", []):
            if isinstance(row, dict) and _clean_text(row.get("md")):
                outputs["discovery_branch_execution_md"] = _clean_text(row.get("md"))
    return {
        "phase": "discovery",
        "status": "completed",
        "detail": _clean_text(
            f"Executed exactly bound local discovery branch `{exact_branch_id}` for canonical branch "
            f"`{canonical_branch_id}` under hypothesis `{canonical_hypothesis_id}`; promoted "
            f"{int(promotion_counts.get('added', 0) or 0)} new and "
            f"{int(promotion_counts.get('updated', 0) or 0)} refreshed branch-bound theorem packages."
        ),
        "local_branch_id": exact_branch_id,
        "canonical_branch_id": canonical_branch_id,
        "canonical_hypothesis_id": canonical_hypothesis_id,
        "promotion_counts": promotion_counts,
        "outputs": outputs,
        "pdl_payload": {
            "operations": [
                {
                    "id": "select-exact",
                    "detail": "Executed one exact branch ID and row digest authorized by the canonical theory schedule.",
                },
                {
                    "id": "promote-exact",
                    "detail": "Filtered theorem promotion to packages carrying that same exact discovery branch ID.",
                },
            ],
            "judgments": [
                {
                    "form": "C ; B ; H |- execute(B)",
                    "detail": "Canonical cycle, branch, and hypothesis identities intersect before local investment.",
                }
            ],
            "control_objects": ["canonical_theory_cycle", "discovery_branch_queue", "proof_queue"],
            "epistemic_state": {
                "exact_branch_count": 1,
                "promoted_count": int(promotion_counts.get("added", 0) or 0)
                + int(promotion_counts.get("updated", 0) or 0),
            },
        },
    }


def run_discovery_phase(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    top_k: int,
    exact_branch_id: str = "",
    expected_branch_digest: str = "",
    canonical_branch_id: str = "",
    canonical_hypothesis_id: str = "",
    promotion_allowed: bool = True,
) -> dict[str, Any]:
    """Materialize legacy discovery, or execute one authoritative bound branch."""

    if _clean_text(exact_branch_id):
        _require_work_contract(promotion_allowed, "authoritative exact discovery cannot run with promotion disabled")
        return _run_exact_discovery_phase(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            exact_branch_id=_clean_text(exact_branch_id),
            expected_branch_digest=_clean_text(expected_branch_digest),
            canonical_branch_id=_clean_text(canonical_branch_id),
            canonical_hypothesis_id=_clean_text(canonical_hypothesis_id),
        )

    queue_json, queue_md = proof_queue_paths(repo_root, kb_ref)
    expert = _load_json(artifacts_dir / "expert-hypothesis-paper.json")
    search_space = _load_json(artifacts_dir / "search-space-tree.json")
    gap_abstractions = _load_json(artifacts_dir / "concept-gap-abstractions.json")
    if not expert or not search_space:
        return {
            "phase": "discovery",
            "status": "blocked",
            "detail": "Discovery inputs are incomplete: need expert-hypothesis-paper.json and search-space-tree.json.",
        }
    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    entries = build_queue_entries(expert=expert, search_space=search_space, kb_ref=kb_ref, top_k=top_k)
    breakthrough_report: dict[str, Any] | None = None
    breakthrough_paths: tuple[Path, Path, Path, Path] | None = None
    breakthrough_prompt_outputs: tuple[Path, Path, Path, Path] | None = None
    breakthrough_routing_outputs: tuple[Path, Path, Path, Path] | None = None
    breakthrough_branch_outputs: tuple[Path, Path] | None = None
    breakthrough_branch_dossiers: list[dict[str, str]] = []
    if not _queue_has_active_entries(queue):
        prior_art = _load_json(artifacts_dir / "prior-art-pass-report.json")
        if prior_art:
            (
                breakthrough_report,
                breakthrough_paths,
                breakthrough_prompt_outputs,
                breakthrough_routing_outputs,
                breakthrough_branch_outputs,
                breakthrough_branch_dossiers,
            ) = _write_breakthrough_profile(artifacts_dir, kb_ref=kb_ref, prior_art=prior_art, queue=queue)
        entries.extend(
            build_repair_queue_entries(
                gap_abstractions=gap_abstractions,
                queue=queue,
                kb_ref=kb_ref,
                breakthrough_profile=breakthrough_report,
                top_k=max(1, top_k),
            )
        )
        entries.extend(
            build_repair_lemma_entries(
                artifacts_dir=artifacts_dir,
                queue=queue,
                kb_ref=kb_ref,
                breakthrough_profile=breakthrough_report,
                top_k=max(1, top_k),
            )
        )
    added, updated = enqueue_entries(queue, entries)
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)
    refresh_summary_from_sources(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        queue=queue,
    )
    outputs: dict[str, str] = {
        "proof_queue_json": str(queue_json),
        "proof_queue_md": str(queue_md),
    }
    detail = f"Queued or refreshed {len(entries)} proof targets (added={added}, updated={updated})."
    theorem_compiler_result: dict[str, Any] | None = None
    governor_report: dict[str, Any] | None = None
    governor_paths: tuple[Path, Path] | None = None
    if breakthrough_paths is not None:
        top_profile = _ensure_dict((_ensure_list(_ensure_dict(breakthrough_report).get("profiles")) or [{}])[0])
        outputs.update(
            {
                "discovery_breakthrough_profile_json": str(breakthrough_paths[0]),
                "discovery_breakthrough_profile_md": str(breakthrough_paths[1]),
                "discovery_breakthrough_profile_tex": str(breakthrough_paths[2]),
                "discovery_breakthrough_profile_pdf": str(breakthrough_paths[3]),
            }
        )
        if breakthrough_prompt_outputs is not None:
            outputs.update(
                {
                    "discovery_family_prompts_json": str(breakthrough_prompt_outputs[0]),
                    "discovery_family_prompts_md": str(breakthrough_prompt_outputs[1]),
                    "discovery_family_prompts_tex": str(breakthrough_prompt_outputs[2]),
                    "discovery_family_prompts_pdf": str(breakthrough_prompt_outputs[3]),
                }
            )
        if breakthrough_routing_outputs is not None:
            outputs.update(
                {
                    "discovery_pattern_routing_json": str(breakthrough_routing_outputs[0]),
                    "discovery_pattern_routing_md": str(breakthrough_routing_outputs[1]),
                    "discovery_pattern_routing_tex": str(breakthrough_routing_outputs[2]),
                    "discovery_pattern_routing_pdf": str(breakthrough_routing_outputs[3]),
                }
            )
        if breakthrough_branch_outputs is not None:
            outputs.update(
                {
                    "discovery_branch_queue_json": str(breakthrough_branch_outputs[0]),
                    "discovery_branch_queue_md": str(breakthrough_branch_outputs[1]),
                }
            )
            for row in breakthrough_branch_dossiers[:4]:
                branch_key = _clean_text(row.get("branch_id")).replace("-", "_").replace(".", "_")
                outputs[f"discovery_branch_{branch_key}_md"] = row["md"]
            governor_report, governor_paths = _refresh_discovery_governor(
                artifacts_dir=artifacts_dir,
                kb_ref=kb_ref,
                top_k=top_k,
                apply_to_branch_queue=True,
            )
            outputs.update(
                {
                    "discovery_governor_report_json": str(governor_paths[0]),
                    "discovery_governor_report_md": str(governor_paths[1]),
                }
            )
        top_family = _clean_text(top_profile.get("breakthrough_family"))
        top_obstruction = _clean_text(top_profile.get("obstruction_class"))
        detail = _clean_text(
            f"{detail} Discovery is now guided by a breakthrough profile centered on"
            f" `{top_family or 'abstraction-search'}` via `{top_obstruction or 'blocked frontier'}`."
        )
        if breakthrough_routing_outputs is not None:
            routing_payload = _load_json(breakthrough_routing_outputs[0])
            layer_count = int(_ensure_dict(routing_payload.get("metadata")).get("layer_count", 0) or 0)
            detail = _clean_text(f"{detail} Spawned {layer_count} routed discovery layers across families and patterns.")
        if breakthrough_branch_outputs is not None:
            branch_payload = _load_json(discovery_branch_queue_paths(artifacts_dir)[0])
            branch_count = int(_ensure_dict(branch_payload.get("metadata")).get("branch_count", 0) or 0)
            active_count = int(_ensure_dict(branch_payload.get("metadata")).get("active_count", 0) or 0)
            detail = _clean_text(f"{detail} Materialized {branch_count} persistent discovery branches with {active_count} active.")
            if governor_report is not None:
                governor_meta = _ensure_dict(governor_report.get("metadata"))
                detail = _clean_text(
                    f"{detail} The discovery governor recommends {int(governor_meta.get('branch_active_recommendation_count', 0) or 0)} active branches"
                    f" and freezes {int(governor_meta.get('branch_freeze_count', 0) or 0)} low-value routes."
                )
            refreshed_queue = load_proof_queue(queue_json, kb_ref=kb_ref)
            if not _queue_has_active_entries(refreshed_queue):
                theorem_compiler_result = _run_branch_to_theorem_pipeline(
                    repo_root=repo_root,
                    artifacts_dir=artifacts_dir,
                    kb_ref=kb_ref,
                    branch_outputs=breakthrough_branch_outputs,
                    top_k=top_k,
                    promotion_allowed=promotion_allowed,
                )
                synthesis_paths = theorem_compiler_result["synthesis_paths"]
                expert_paths = theorem_compiler_result["expert_paths"]
                governor_paths = theorem_compiler_result["governor_paths"]
                execution_paths = theorem_compiler_result["execution_paths"]
                promotion_paths = theorem_compiler_result["promotion_paths"]
                promotion_counts = _ensure_dict(theorem_compiler_result.get("promotion_counts"))
                expert_meta = _ensure_dict(_ensure_dict(theorem_compiler_result.get("expert_report")).get("metadata"))
                execution_meta = _ensure_dict(_ensure_dict(theorem_compiler_result.get("execution_index")).get("metadata"))
                outputs.update(
                    {
                        "discovery_branch_execution_index_json": str(execution_paths[0]),
                        "discovery_branch_execution_index_md": str(execution_paths[1]),
                    }
                )
                if theorem_compiler_result.get("executed_current_round"):
                    outputs.update(
                        {
                            "discovery_branch_synthesis_json": str(synthesis_paths[0]),
                            "discovery_branch_synthesis_md": str(synthesis_paths[1]),
                            "discovery_branch_synthesis_tex": str(synthesis_paths[2]),
                            "discovery_branch_synthesis_pdf": str(synthesis_paths[3]),
                            "expert_conjectures_json": str(expert_paths[0]),
                            "expert_conjectures_md": str(expert_paths[1]),
                            "expert_conjectures_tex": str(expert_paths[2]),
                            "expert_conjectures_pdf": str(expert_paths[3]),
                            "discovery_governor_report_json": str(governor_paths[0]),
                            "discovery_governor_report_md": str(governor_paths[1]),
                            "discovery_programme_promotions_json": str(promotion_paths[0]),
                            "discovery_programme_promotions_md": str(promotion_paths[1]),
                        }
                    )
                    for row in theorem_compiler_result.get("execution_outputs", [])[:4]:
                        if not isinstance(row, dict):
                            continue
                        branch_key = _clean_text(row.get("branch_id")).replace("-", "_").replace(".", "_")
                        outputs[f"discovery_branch_execution_{branch_key}_md"] = row["md"]
                    detail = _clean_text(
                        f"{detail} Executed the active discovery branches, compiled {int(expert_meta.get('expert_conjecture_count', 0) or 0)} theorem packages,"
                        f" and promoted {int(promotion_counts.get('added', 0) or 0)} new plus {int(promotion_counts.get('updated', 0) or 0)} refreshed expert-grade conjectures back into prove."
                    )
                    detail = _clean_text(
                        f"{detail} Lean/Lake search evaluated {int(execution_meta.get('last_run_lean_route_count', 0) or 0)} typed routes"
                        f" and emitted {int(execution_meta.get('last_run_lean_candidate_count', 0) or 0)} bounded theorem candidates."
                    )
                    governor_meta = _ensure_dict(_ensure_dict(theorem_compiler_result.get("governor_report")).get("metadata"))
                    detail = _clean_text(
                        f"{detail} The governor judged {int(governor_meta.get('promotion_ready_count', 0) or 0)} packages proof-worthy"
                        f" and {int(governor_meta.get('promotion_major_candidate_count', 0) or 0)} as major intermediate results."
                    )
                else:
                    detail = _clean_text(
                        f"{detail} No discovery branches were executed in this round, so theorem compilation and proof promotion were skipped."
                    )
    elif not _queue_has_active_entries(queue):
        detail = _clean_text(
            f"{detail} The queue is locally exhausted, but no prior-art-pass-report.json is available"
            " to classify the required breakthrough family."
        )
    top_open_entry = _top_open_queue_entry(queue)
    pdl_payload: dict[str, Any] = {
        "program": serialize_queue_entry_as_pdl(top_open_entry) if top_open_entry else {},
        "operations": [
            {
                "id": "aggregate",
                "detail": f"Aggregated {len(entries)} discovery frontier entries into the current proof queue view.",
            },
            {
                "id": "route",
                "detail": "Routed the current frontier into queue refresh, branch spawning, and optional theorem compilation.",
            },
        ],
        "judgments": [
            {
                "form": "A ; T |-m X",
                "detail": "Discovery isolates the active tension between current theorem bodies and the next target claim.",
            },
            {
                "form": "N ; B |- P",
                "detail": "The routed frontier induces a discovery programme or queue entry only after a bridge-shaped nexus is available.",
            },
        ],
        "control_objects": ["kb", "proof_queue", "discovery_branch_queue"],
        "epistemic_state": {
            "queue_added": added,
            "queue_updated": updated,
            "top_k": top_k,
            "has_breakthrough_profile": 1 if breakthrough_paths is not None else 0,
        },
    }
    if governor_report is not None:
        pdl_payload["operations"].append(
            {
                "id": "govern",
                "detail": "Applied the deterministic discovery governor to separate major or decisive routes from low-value discovery drift.",
            }
        )
        pdl_payload["control_objects"].append("discovery_governor")
        governor_meta = _ensure_dict(governor_report.get("metadata"))
        pdl_payload["epistemic_state"]["governor_active_recommendations"] = int(
            governor_meta.get("branch_active_recommendation_count", 0) or 0
        )
        pdl_payload["epistemic_state"]["governor_frozen_branches"] = int(
            governor_meta.get("branch_freeze_count", 0) or 0
        )
    if theorem_compiler_result is not None:
        pdl_payload["operations"].append(
            {
                "id": "concretize",
                "detail": "Compiled branch-level discoveries into expert-grade theorem packages before prove promotion.",
            }
        )
        pdl_payload["control_objects"].append("mathlib")
    return {
        "phase": "discovery",
        "status": "completed",
        "detail": detail,
        "queue_entry_count": len(entries),
        "queue_added": added,
        "queue_updated": updated,
        "outputs": outputs,
        "pdl_payload": pdl_payload,
    }


def run_prove_phase(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    kb_path: Path | None,
    exact_queue_id: str = "",
    expected_queue_digest: str = "",
) -> dict[str, Any]:
    """Consume a pending item, with exact selection for canonical callers."""

    queue_json, queue_md = proof_queue_paths(repo_root, kb_ref)
    normalized_exact_queue_id = _clean_text(exact_queue_id)
    if normalized_exact_queue_id:
        raw_queue = _load_json_object_strict(queue_json, label="authoritative proof queue")
        exact_rows = [
            row
            for row in _ensure_list(raw_queue.get("entries"))
            if isinstance(row, dict) and _clean_text(row.get("queue_id")) == normalized_exact_queue_id
        ]
        _require_work_contract(
            len(exact_rows) == 1,
            f"authoritative prove selector requires exactly one queue row `{normalized_exact_queue_id}`",
        )
        _require_work_contract(
            _clean_text(exact_rows[0].get("status")).lower() == "pending",
            f"authoritative prove queue row `{normalized_exact_queue_id}` is not pending",
        )
        _require_work_contract(
            bool(_clean_text(expected_queue_digest))
            and canonical_digest(exact_rows[0]) == _clean_text(expected_queue_digest),
            f"authoritative prove queue row `{normalized_exact_queue_id}` changed after binding preflight",
        )
    mathlib_json, mathlib_md = mathlib_paths(repo_root, kb_ref)
    queue = load_proof_queue(queue_json, kb_ref=kb_ref)
    if normalized_exact_queue_id:
        normalized_matches = [
            row
            for row in _ensure_list(queue.get("entries"))
            if isinstance(row, dict) and _clean_text(row.get("queue_id")) == normalized_exact_queue_id
        ]
        _require_work_contract(
            len(normalized_matches) == 1
            and _clean_text(normalized_matches[0].get("status")).lower() == "pending",
            f"authoritative prove queue row `{normalized_exact_queue_id}` did not remain consumable after normalization",
        )
    mathlib = load_mathlib_index(mathlib_json, kb_ref=kb_ref)
    if not mathlib_json.exists():
        save_mathlib_index(mathlib, json_path=mathlib_json, md_path=mathlib_md)
    auto_blocked = (
        {}
        if normalized_exact_queue_id
        else _auto_finalize_scaffold_attempt(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            queue=queue,
            mathlib=mathlib,
        )
    )
    if auto_blocked:
        return {
            "phase": "prove",
            "status": "completed",
            "detail": (
                f"Auto-finalized scaffold-only proof attempt `{auto_blocked['attempt_id']}` from "
                f"`{auto_blocked['queue_id']}` as `blocked` because the route remained unresolved and local InformalMathLib already contained related blockers."
            ),
            "attempt_id": auto_blocked["attempt_id"],
            "queue_id": auto_blocked["queue_id"],
            "result_id": auto_blocked["result_id"],
            "outputs": {
                "proof_attempt_json": auto_blocked["proof_attempt_json"],
                "proof_attempt_md": auto_blocked["proof_attempt_md"],
                "proof_queue_json": auto_blocked["proof_queue_json"],
                "mathlib_json": auto_blocked["mathlib_json"],
            },
            "pdl_payload": {
                "operations": [
                    {
                        "id": "obstruct",
                        "detail": "The prove loop resumed the oldest scaffold-only attempt and finalized it as a blocked local theorem before opening any new queue item.",
                    },
                    {
                        "id": "persist",
                        "detail": "The blocked outcome was persisted into InformalMathLib, the proof queue, and the proof-cycle summary.",
                    },
                ],
                "judgments": [
                    {
                        "form": "P ; O |- impossibility(T)",
                        "detail": "The oldest open route remained scaffold-only and inherited already-recorded local blockers, so the loop closed it before consuming another conjecture.",
                    }
                ],
                "control_objects": ["proof_queue", "mathlib", "proof_attempts"],
                "epistemic_state": {"auto_blocked_attempt": 1},
            },
        }
    active_attempts = [] if normalized_exact_queue_id else _active_attempt_records(artifacts_dir=artifacts_dir, queue=queue)
    if active_attempts:
        resumed = _resume_attempt_record(
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            attempt_record=active_attempts[0],
        )
        return {
            "phase": "prove",
            "status": "completed",
            "detail": (
                f"Resumed proof attempt `{resumed['attempt_id']}` from queue item `{resumed['queue_id']}`; "
                f"normalized {resumed['completed_tactic_count']} tactic checkpoints and left "
                f"{resumed['active_tactic_count']} obstruction-style step(s) active. "
                f"Continuation stage {resumed['continuation_stage']} added {resumed['added_step_count']} stepwise proof updates "
                f"and imported {resumed['added_local_results']} local blocker reference(s)."
            ),
            "attempt_id": resumed["attempt_id"],
            "queue_id": resumed["queue_id"],
            "outputs": {
                "proof_attempt_json": resumed["proof_attempt_json"],
                "proof_attempt_md": resumed["proof_attempt_md"],
                "proof_queue_json": str(queue_json),
            },
            "pdl_payload": {
                "operations": [
                    {
                        "id": "resume",
                        "detail": "The prove loop resumed an already-open proof dossier instead of opening a new queue item.",
                    },
                    {
                        "id": "expose",
                        "detail": "The continuation step grounded the local route against InformalMathLib blockers and sharpened the obstruction branch inside the attempt dossier.",
                    },
                ],
                "judgments": [
                    {
                        "form": "P ; A |- continue(A)",
                        "detail": "An open proof attempt still deserves local pressure, so the loop extends it before consuming a fresh pending theorem.",
                    }
                ],
                "control_objects": ["proof_attempts", "proof_queue"],
                "epistemic_state": {
                    "active_attempt_count": len(active_attempts),
                    "continuation_stage": resumed["continuation_stage"],
                    "blocked_hit_count": resumed["blocked_hit_count"],
                    "completed_tactic_count": resumed["completed_tactic_count"],
                    "active_tactic_count": resumed["active_tactic_count"],
                },
            },
        }
    pending = [
        row
        for row in _ensure_list(queue.get("entries"))
        if isinstance(row, dict) and _clean_text(row.get("status")).lower() == "pending"
    ]
    if not pending:
        interpretability_deferred = _interpretability_deferred_entries(queue)
        if interpretability_deferred:
            save_proof_queue(queue, json_path=queue_json, md_path=queue_md)
            top_row = interpretability_deferred[0]
            top_reason = _clean_text(top_row.get("deferred_reason")) or "Re-encode the route as a self-contained theorem state."
            return {
                "phase": "prove",
                "status": "idle",
                "detail": (
                    "No pending proof-queue item passes the LLM interpretability gate; "
                    f"{len(interpretability_deferred)} entries are deferred for re-encoding. "
                    f"Top blocker on `{_clean_text(top_row.get('queue_id'))}`: {top_reason}"
                ),
                "pdl_payload": {
                    "operations": [
                        {
                            "id": "route",
                            "detail": "The prove gate deferred the current frontier because the queued theorem states are not self-contained enough for direct LLM proof work.",
                        }
                    ],
                    "judgments": [
                        {
                            "form": "K ; Q |- defer(reencode)",
                            "detail": "Pending proof work exists, but the strongest queue items still require re-encoding before they become theorem-level proof targets.",
                        }
                    ],
                    "control_objects": ["proof_queue"],
                    "epistemic_state": {
                        "pending_count": 0,
                        "interpretability_deferred_count": len(interpretability_deferred),
                        "top_deferred_queue_id": _clean_text(top_row.get("queue_id")),
                    },
                },
            }
        active_attempt_rows = _load_attempt_rows(artifacts_dir)
        active_attempt_ids = [
            _clean_text(_ensure_dict(row.get("metadata")).get("attempt_id"))
            for row in active_attempt_rows
            if (
                _clean_text(_ensure_dict(row.get("metadata")).get("status")).lower() == "in_progress"
                or _clean_text(_ensure_dict(row.get("final_assessment")).get("outcome")).lower() == "in_progress"
            )
        ]
        if active_attempt_ids:
            return {
                "phase": "prove",
                "status": "idle",
                "detail": (
                    "No pending proof-queue item is available. "
                    f"{len(active_attempt_ids)} proof attempt(s) remain in progress "
                    f"({', '.join(active_attempt_ids[:3])}), but the current work loop only resumes them indirectly "
                    "through terminalization or auto-blocking rather than a dedicated continuation executor."
                ),
                "pdl_payload": {
                    "operations": [
                        {
                            "id": "inspect",
                            "detail": "The prove loop found live attempt dossiers but has no direct resume step for extending them.",
                        }
                    ],
                    "judgments": [
                        {
                            "form": "P ; A |- gap(resume-executor)",
                            "detail": "The frontier is not empty, but the work loop lacks a dedicated continuation transition for already-open proof attempts.",
                        }
                    ],
                    "control_objects": ["proof_queue", "proof_attempts"],
                    "epistemic_state": {
                        "pending_count": 0,
                        "active_attempt_count": len(active_attempt_ids),
                    },
                },
            }
        return {
            "phase": "prove",
            "status": "idle",
            "detail": "No pending proof-queue item is available, so the loop returns to discovery.",
            "pdl_payload": {
                "operations": [
                    {
                        "id": "route",
                        "detail": "The work loop found no pending theorem-shaped item to consume, so control returns to discovery.",
                    }
                ],
                "judgments": [
                    {
                        "form": "P ; G @ next",
                        "detail": "The prove gate is idle because the pending frontier is empty.",
                    }
                ],
                "control_objects": ["proof_queue"],
                "epistemic_state": {"pending_count": 0},
            },
        }

    attempt_dir = artifacts_dir / "proof-attempts"
    attempt_dir.mkdir(parents=True, exist_ok=True)
    attempt_id = _next_attempt_id(attempt_dir, kb_ref=kb_ref)
    queue_entry = consume_next_entry(
        queue,
        attempt_id=attempt_id,
        queue_id=normalized_exact_queue_id,
    )
    save_proof_queue(queue, json_path=queue_json, md_path=queue_md)
    refresh_summary_from_sources(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        queue=queue,
        mathlib=mathlib,
    )

    query_terms = [
        _clean_text(queue_entry.get("candidate_object")),
        _clean_text(queue_entry.get("preserved_invariant")),
        _clean_text(queue_entry.get("target_statement_id")),
        _clean_text(queue_entry.get("bridge_id")),
    ]
    mathlib_hits = search_mathlib(mathlib, query_terms, limit=5)
    statement_index = load_statement_index(kb_path) if kb_path else {}
    attempt = build_attempt_record(
        attempt_id=attempt_id,
        kb_ref=kb_ref,
        queue_entry=queue_entry,
        mathlib_hits=mathlib_hits,
        statement_index=statement_index,
    )
    attempt_json, attempt_md = _attempt_paths(artifacts_dir, attempt_id)
    attempt_json.write_text(json.dumps(attempt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    attempt_md.write_text(render_attempt_markdown(attempt), encoding="utf-8")
    refresh_summary_from_sources(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        queue=queue,
        mathlib=mathlib,
    )
    pdl_payload = {
        "program": _ensure_dict(attempt.get("pdl_program")),
        "operations": [
            {
                "id": "extract",
                "detail": "Loaded the current theorem body, queue context, and local InformalMathLib hints into one proof dossier.",
            },
            {
                "id": "focus",
                "detail": "Focused the proof on the missing route lemma and the explicit local theorem under test.",
            },
            {
                "id": "route",
                "detail": "Routed the next live conjecture into a prove attempt scaffold with tactic and critique structure.",
            },
        ],
        "judgments": [
            {
                "form": "K ; M |- A : grounded",
                "detail": "Local KB and InformalMathLib excerpts are now the anchor set for the attempt.",
            },
            {
                "form": "N ; B |- P",
                "detail": "The selected queue item has been re-expressed as a proof-discovery programme.",
            },
        ],
        "control_objects": ["kb", "mathlib", "proof_queue"],
        "epistemic_state": {"mathlib_hits": len(mathlib_hits)},
    }
    return {
        "phase": "prove",
        "status": "completed",
        "detail": f"Started proof attempt `{attempt_id}` from queue item `{queue_entry.get('queue_id', '')}`.",
        "attempt_id": attempt_id,
        "queue_id": _clean_text(queue_entry.get("queue_id")),
        "mathlib_hit_count": len(mathlib_hits),
        "outputs": {
            "proof_attempt_json": str(attempt_json),
            "proof_attempt_md": str(attempt_md),
            "proof_queue_json": str(queue_json),
        },
        "pdl_payload": pdl_payload,
    }


def execute_work_cycle(
    *,
    repo_root: Path,
    artifacts_dir: Path,
    kb_ref: str,
    kb_path: Path | None,
    state: dict[str, Any],
    phase_override: str,
    top_k: int,
    logger: ReasoningLogger | None = None,
    canonical_cycle_path: Path | None = None,
    canonical_state_root: Path | None = None,
    canonical_target_id: str = "",
    canonical_run_id: str = "",
    canonical_work_binding: Mapping[str, Any] | None = None,
    non_authoritative_legacy_compatibility: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Run one outer-loop step behind a fail-closed canonical theory boundary."""

    meta = _ensure_dict(state.get("metadata"))
    latest: dict[str, Any] = {}
    requested_phase = _clean_text(phase_override).lower() or "auto"
    _require_work_contract(
        requested_phase in {"auto", "discovery", "prove"},
        "phase_override must be auto, discovery, or prove",
    )
    phase = (
        requested_phase
        if requested_phase in {"discovery", "prove"}
        else _clean_text(meta.get("next_phase")).lower() or "discovery"
    )
    _require_work_contract(phase in {"discovery", "prove"}, "persisted next_phase must be discovery or prove")
    supplied_canonical_inputs = any(
        (
            canonical_cycle_path is not None,
            canonical_state_root is not None,
            bool(_clean_text(canonical_target_id)),
            bool(_clean_text(canonical_run_id)),
            canonical_work_binding is not None,
        )
    )
    if non_authoritative_legacy_compatibility:
        _require_work_contract(
            not supplied_canonical_inputs,
            "canonical inputs cannot be mixed with non-authoritative legacy compatibility",
        )
        authorization = _compatibility_authorization(phase=phase)
        local_work_item: dict[str, Any] = {}
    else:
        _require_work_contract(
            canonical_cycle_path is not None
            and canonical_state_root is not None
            and bool(_clean_text(canonical_target_id))
            and bool(_clean_text(canonical_run_id))
            and isinstance(canonical_work_binding, Mapping),
            "authoritative execution requires canonical cycle, state root, target, run, and exact work binding",
        )
        prior_lineage = meta.get("canonical_theory_lineage")
        authorization = verify_work_cycle_theory_authorization(
            projection_path=Path(canonical_cycle_path),
            state_root=Path(canonical_state_root),
            target_id=_clean_text(canonical_target_id),
            run_id=_clean_text(canonical_run_id),
            work_binding=canonical_work_binding,
            phase=phase,
            previous_lineage=prior_lineage if isinstance(prior_lineage, Mapping) and prior_lineage else None,
        )
        local_work_item = verify_exact_local_work_item(
            phase=phase,
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            authorization=authorization,
        )
    authority_record = _authority_record(authorization)
    meta["authority_mode"] = authority_record["mode"]
    meta["authoritative"] = authority_record["authoritative"]
    meta["promotion_allowed"] = authority_record["promotion_allowed"]
    meta["last_authority"] = authority_record
    state["metadata"] = meta
    looper_frontier = _load_looper_frontier(repo_root, kb_ref)
    if looper_frontier:
        meta["looper_target_id"] = looper_frontier.get("target_id", "")
        meta["looper_frontier_count"] = looper_frontier.get("frontier_count", 0)
        meta["looper_frontier_recommendation"] = looper_frontier.get("recommended_next", "")
        meta["looper_frontier_status_counts"] = looper_frontier.get("status_counts", {})
    plausibility = build_plausibility_report_from_artifacts(repo_root, artifacts_dir)
    state["plausibility"] = plausibility
    decision = _ensure_dict(plausibility.get("decision"))
    if decision.get("plausible_solution_detected"):
        meta["stop_status"] = "stop-plausible-solution"
        meta["stop_reason"] = _clean_text(decision.get("detail"))
        meta["plausible_solution_detected"] = True
        state["metadata"] = meta
        latest = _decorate_authority(state, {
            "phase": "none",
            "status": "stopped",
            "detail": _clean_text(decision.get("detail")),
        }, authorization)
        state["latest"] = latest
        return state, latest

    if _safe_int(meta.get("cycle_count")) >= _safe_int(meta.get("max_cycles")):
        allow_continue, continuation_reason, signal = _high_reward_extension_allows_continue(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            meta=meta,
        )
        if not allow_continue:
            meta["stop_status"] = "stop-max-cycles"
            meta["stop_reason"] = f"Reached max_cycles={meta.get('max_cycles', 0)}."
            state["metadata"] = meta
            latest = _decorate_authority(state, {
                "phase": "none",
                "status": "stopped",
                "detail": _clean_text(meta.get("stop_reason")),
            }, authorization)
            state["latest"] = latest
            return state, latest
        meta["stop_status"] = "running"
        meta["stop_reason"] = _clean_text(
            f"Continuing beyond max_cycles under `{_clean_text(signal.get('signal_id'))}` via `{continuation_reason}`."
        )

    if authority_record["canonical_theory_verified"]:
        authorization = reserve_work_cycle_actions(authorization)
        # The reservation closes the canonical action race.  Re-read the
        # independently mutable compatibility row afterwards so a concurrent
        # local edit cannot slip between binding verification and dispatch.
        local_work_item = verify_exact_local_work_item(
            phase=phase,
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            authorization=authorization,
        )
        authority_record = _authority_record(authorization)
        meta["last_authority"] = authority_record
        state["metadata"] = meta

    if logger is not None:
        logger.surface(
            "Dispatching work phase",
            details="\n".join(
                [
                    f"phase={phase}",
                    f"cycle_count={_safe_int(meta.get('cycle_count'))}",
                    f"max_cycles={_safe_int(meta.get('max_cycles'))}",
                    f"next_phase_before_dispatch={_clean_text(meta.get('next_phase'))}",
                    f"authority_mode={authority_record['mode']}",
                    f"authoritative={authority_record['authoritative']}",
                    f"promotion_allowed={authority_record['promotion_allowed']}",
                    f"action_reserved={authority_record['action_reserved']}",
                    f"reservation_id={authority_record['reservation_id']}",
                    f"looper_target={_clean_text(looper_frontier.get('target_id')) if looper_frontier else 'none'}",
                    f"looper_frontier_count={looper_frontier.get('frontier_count', 0) if looper_frontier else 0}",
                ]
            ),
            focus=f"work::{phase}",
            significance="The outer loop chooses whether the next epistemic move is discovery or prove.",
            kind="conceptual_move",
            tags=["work-loop", phase],
            stage="work",
            pdl={
                "operations": [
                    {
                        "id": "route",
                        "detail": f"The work loop dispatches the next phase as `{phase}` under the current stop and plausibility state.",
                    }
                ],
                "judgments": [
                    {
                        "form": "P ; G @ next",
                        "detail": f"Governance routes the current programme into `{phase}`.",
                    }
                ],
                "control_objects": ["proof_queue", "discovery_branch_queue", "mathlib", "meta"],
                "epistemic_state": {
                    "cycle_count": _safe_int(meta.get("cycle_count")),
                    "plausibility_score": float(_ensure_dict(state.get("plausibility")).get("plausibility_score", 0.0) or 0.0),
                    "looper_frontier": looper_frontier,
                },
            },
        )
    if phase == "prove":
        latest = run_prove_phase(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            kb_path=kb_path,
            exact_queue_id=(local_work_item.get("id", "") if authority_record["authoritative"] else ""),
            expected_queue_digest=(local_work_item.get("digest", "") if authority_record["authoritative"] else ""),
        )
        next_phase = "discovery"
    else:
        binding = _ensure_dict(authorization.get("work_binding"))
        latest = run_discovery_phase(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            top_k=top_k,
            exact_branch_id=(local_work_item.get("id", "") if authority_record["authoritative"] else ""),
            expected_branch_digest=(local_work_item.get("digest", "") if authority_record["authoritative"] else ""),
            canonical_branch_id=(
                _clean_text(binding.get("canonical_branch_id")) if authority_record["authoritative"] else ""
            ),
            canonical_hypothesis_id=(
                _clean_text(binding.get("canonical_hypothesis_id")) if authority_record["authoritative"] else ""
            ),
            promotion_allowed=authority_record["promotion_allowed"],
        )
        next_phase = "prove"
    latest = _decorate_authority(state, latest, authorization)
    if authority_record["authoritative"]:
        reservation = _ensure_dict(authorization.get("action_reservation"))
        meta["canonical_theory_lineage"] = {
            "target_id": authorization["target_id"],
            "run_id": authorization["run_id"],
            "transaction_root": authorization["transaction_root"],
            "cycle_id": authorization["cycle_id"],
            "source_commit_id": authorization["commit_id"],
            "commit_id": reservation["reserved_commit_id"],
            "committed_state_version": reservation["reserved_state_generation"],
            "work_binding_digest": authorization["work_binding_digest"],
            "reservation_id": reservation["reservation_id"],
            "reservation_digest": reservation["reservation_digest"],
        }
    if logger is not None:
        logger.surface(
            f"Completed work {latest.get('phase', phase)} phase",
            details="\n".join(
                [
                    f"status={_clean_text(latest.get('status'))}",
                    f"detail={_clean_text(latest.get('detail'))}",
                    f"authoritative={latest.get('authoritative', False)}",
                    f"promotion_allowed={latest.get('promotion_allowed', False)}",
                ]
            ),
            focus=f"work::{latest.get('phase', phase)}",
            significance="Records the epistemic result of the selected work phase and the state it exposed to the outer loop.",
            kind="result_synthesis",
            tags=["work-loop", _clean_text(latest.get("phase", phase)), _clean_text(latest.get("status"))],
            stage="work",
            pdl=_ensure_dict(latest.get("pdl_payload")),
        )

    meta["cycle_count"] = _safe_int(meta.get("cycle_count")) + 1
    meta["next_phase"] = next_phase
    meta["stop_status"] = "running"
    meta["stop_reason"] = ""
    meta["plausible_solution_detected"] = False
    state["metadata"] = meta
    state["latest"] = latest
    state.setdefault("history", [])
    if not isinstance(state["history"], list):
        state["history"] = []
    state["history"].append(
        {
            "cycle_number": meta["cycle_count"],
            "phase": latest.get("phase", phase),
            "status": latest.get("status", ""),
            "detail": latest.get("detail", ""),
            "authority_mode": authority_record["mode"],
            "authoritative": authority_record["authoritative"],
            "promotion_allowed": authority_record["promotion_allowed"],
            "canonical_binding_id": authority_record["binding_id"],
            "canonical_reservation_id": authority_record["reservation_id"],
            "canonical_reservation_digest": authority_record["reservation_digest"],
            "canonical_reservation_commit_id": authority_record["reservation_commit_id"],
            "timestamp_utc": _utc_now(),
        }
    )

    plausibility = build_plausibility_report_from_artifacts(repo_root, artifacts_dir)
    state["plausibility"] = plausibility
    decision = _ensure_dict(plausibility.get("decision"))
    if decision.get("plausible_solution_detected"):
        meta["stop_status"] = "stop-plausible-solution"
        meta["stop_reason"] = _clean_text(decision.get("detail"))
        meta["plausible_solution_detected"] = True
    elif _safe_int(meta.get("cycle_count")) >= _safe_int(meta.get("max_cycles")):
        allow_continue, continuation_reason, signal = _high_reward_extension_allows_continue(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            meta=meta,
        )
        if allow_continue:
            meta["stop_status"] = "running"
            meta["stop_reason"] = _clean_text(
                f"Continuing beyond max_cycles under `{_clean_text(signal.get('signal_id'))}` via `{continuation_reason}`."
            )
            latest["detail"] = _clean_text(f"{latest.get('detail', '')} High-reward continuation remains active.")
            latest["high_reward_trigger_reason"] = continuation_reason
            latest["high_reward_signal_id"] = _clean_text(signal.get("signal_id"))
        else:
            meta["stop_status"] = "stop-max-cycles"
            meta["stop_reason"] = f"Reached max_cycles={meta.get('max_cycles', 0)}."

    run_meta, meta_reason, queue_signature = _should_run_meta(
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        meta=meta,
        latest=latest,
    )
    if run_meta:
        meta_report, meta_outputs, meta_log_outputs = _run_meta_checkpoint(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            perspective=_clean_text(meta.get("meta_perspective")) or DEFAULT_META_PERSPECTIVE,
            interpretation=_clean_text(meta.get("meta_interpretation")) or DEFAULT_META_INTERPRETATION,
        )
        latest["detail"] = _clean_text(
            f"{latest.get('detail', '')} Meta invoked automatically under trigger `{meta_reason}`."
        )
        latest.setdefault("outputs", {})
        if isinstance(latest["outputs"], dict):
            latest["outputs"].update(
                {
                    "meta_reflection_json": str(meta_outputs[0]),
                    "meta_reflection_md": str(meta_outputs[1]),
                    "meta_reflection_tex": str(meta_outputs[2]),
                    "meta_reflection_pdf": str(meta_outputs[3]),
                }
            )
            latest["outputs"].update(meta_log_outputs)
        latest["meta_trigger_reason"] = meta_reason
        latest["meta_headline"] = _clean_text(_ensure_dict(meta_report.get("meta_judgment")).get("headline"))
        meta["last_meta_cycle"] = _safe_int(meta.get("cycle_count"))
        meta["last_meta_reason"] = meta_reason
        meta["last_meta_queue_signature"] = queue_signature
        if logger is not None:
            logger.surface(
                "Automatic meta checkpoint",
                details="\n".join(
                    [
                        f"reason={meta_reason}",
                        f"headline={_clean_text(_ensure_dict(meta_report.get('meta_judgment')).get('headline'))}",
                    ]
                ),
                focus="meta-checkpoint",
                significance="The loop reflects on the current discovery/proof state because a governance trigger fired.",
                kind="conceptual_move",
                tags=["work-loop", "meta", meta_reason],
                stage="meta",
                pdl={
                    "operations": [
                        {
                            "id": "aggregate",
                            "detail": "Meta aggregates the current proof, discovery, and queue state into a reflective interpretation.",
                        },
                        {
                            "id": "route",
                            "detail": "The work loop routes control through the reflective layer before continuing.",
                        },
                    ],
                    "judgments": [
                        {
                            "form": "P ; G @ next",
                            "detail": f"Meta was invoked under trigger `{meta_reason}`.",
                        }
                    ],
                    "control_objects": ["meta", "proof_queue", "mathlib"],
                },
            )
    state["metadata"] = meta
    return state, latest


def main() -> int:
    """Run the work-loop CLI: resolve inputs, execute one cycle, persist, and log."""
    logger = ReasoningLogger("work")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", default="", help="Optional KB markdown path.")
    ap.add_argument("--kb-ref", default="", help="Optional KB reference override.")
    ap.add_argument("--artifacts-dir", default="", help="Optional artifacts/<kb-ref> path.")
    ap.add_argument("--max-cycles", type=int, default=6, help="Maximum number of work cycles before stopping.")
    ap.add_argument("--meta-interval", type=int, default=DEFAULT_META_INTERVAL, help="Run meta automatically every N completed work cycles.")
    ap.add_argument("--meta-perspective", default=DEFAULT_META_PERSPECTIVE, help="Perspective used for auto-invoked meta reflection.")
    ap.add_argument("--meta-interpretation", default=DEFAULT_META_INTERPRETATION, help="Interpretation used for auto-invoked meta reflection.")
    ap.add_argument("--top-k", type=int, default=8, help="Maximum queue entries to materialize during discovery.")
    ap.add_argument("--phase", default="auto", help="One of auto, discovery, prove.")
    ap.add_argument("--canonical-cycle", default="", help="Immutable canonical discovery-cycle projection JSON.")
    ap.add_argument("--canonical-state-root", default="", help="Exact canonical transaction-state root.")
    ap.add_argument("--canonical-target-id", default="", help="Exact canonical discovery target ID.")
    ap.add_argument("--canonical-run-id", default="", help="Exact canonical discovery run ID.")
    ap.add_argument(
        "--canonical-work-binding",
        default="",
        help="Immutable JSON binding from canonical branch/hypothesis/obligation IDs to one digest-bound local row.",
    )
    ap.add_argument(
        "--non-authoritative-legacy-compatibility",
        action="store_true",
        help="Opt into legacy execution with authoritative=false and all promotion authority disabled.",
    )
    ap.add_argument("--output-json", default="", help="Optional work-state JSON path.")
    ap.add_argument("--output-md", default="", help="Optional work-state Markdown path.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    kb_path: Path | None = None
    kb_ref = _clean_text(args.kb_ref)
    if args.kb:
        kb_path = Path(args.kb)
        if not kb_path.is_absolute():
            kb_path = (repo_root / kb_path).resolve()
        kb_ctx = resolve_kb_reference(kb_path, explicit_kb_ref=kb_ref)
        kb_ref = kb_ctx["kb_ref"]

    artifacts_dir = Path(args.artifacts_dir) if args.artifacts_dir else (canonical_artifacts_dir(repo_root, kb_ref) if kb_ref else None)
    if artifacts_dir is None:
        raise SystemExit("[ERROR] Provide either --kb or both --kb-ref and --artifacts-dir.")
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    if not kb_ref:
        kb_ref = kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("[ERROR] Could not resolve kb_ref for work loop.")

    def resolve_cli_path(value: str) -> Path | None:
        if not _clean_text(value):
            return None
        path = Path(value)
        return path.resolve() if path.is_absolute() else (repo_root / path).resolve()

    canonical_cycle_path = resolve_cli_path(args.canonical_cycle)
    canonical_state_root = resolve_cli_path(args.canonical_state_root)
    canonical_binding_path = resolve_cli_path(args.canonical_work_binding)
    canonical_work_binding: dict[str, Any] | None = None
    try:
        if canonical_binding_path is not None:
            _require_work_contract(
                not any(part.lower() in _MUTABLE_BINDING_PATH_NAMES for part in canonical_binding_path.parts),
                "mutable latest/current canonical work-binding aliases are forbidden",
            )
            canonical_work_binding = _load_json_object_strict(
                canonical_binding_path,
                label="canonical work binding",
            )
    except ContractError as exc:
        raise SystemExit(f"[ERROR] {exc}") from exc

    output_json, output_md = work_state_paths(artifacts_dir)
    if args.output_json:
        output_json = Path(args.output_json)
        if not output_json.is_absolute():
            output_json = (repo_root / output_json).resolve()
    if args.output_md:
        output_md = Path(args.output_md)
        if not output_md.is_absolute():
            output_md = (repo_root / output_md).resolve()

    state = load_work_state(output_json, kb_ref=kb_ref, max_cycles=max(1, args.max_cycles))
    state.setdefault("metadata", {})
    if isinstance(state["metadata"], dict):
        state["metadata"]["meta_interval"] = max(1, _safe_int(args.meta_interval, DEFAULT_META_INTERVAL))
        state["metadata"]["meta_perspective"] = _clean_text(args.meta_perspective) or DEFAULT_META_PERSPECTIVE
        state["metadata"]["meta_interpretation"] = _clean_text(args.meta_interpretation) or DEFAULT_META_INTERPRETATION
    logger.add_kv("kb_ref", kb_ref)
    logger.add_kv("artifacts_dir", str(artifacts_dir))
    try:
        state, latest = execute_work_cycle(
            repo_root=repo_root,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            kb_path=kb_path,
            state=state,
            phase_override=_clean_text(args.phase).lower(),
            top_k=max(1, args.top_k),
            logger=logger,
            canonical_cycle_path=canonical_cycle_path,
            canonical_state_root=canonical_state_root,
            canonical_target_id=_clean_text(args.canonical_target_id),
            canonical_run_id=_clean_text(args.canonical_run_id),
            canonical_work_binding=canonical_work_binding,
            non_authoritative_legacy_compatibility=bool(args.non_authoritative_legacy_compatibility),
        )
    except ContractError as exc:
        raise SystemExit(f"[ERROR] {exc}") from exc
    save_work_state(state, json_path=output_json, md_path=output_md)
    plausibility_json, plausibility_md = _write_plausibility_report(artifacts_dir, _ensure_dict(state.get("plausibility")))

    meta = _ensure_dict(state.get("metadata"))
    decision = _ensure_dict(_ensure_dict(state.get("plausibility")).get("decision"))
    logger.step(
        "Ran work cycle",
        "\n".join(
            [
                f"kb_ref={kb_ref}",
                f"cycle_count={meta.get('cycle_count', 0)}",
                f"phase={latest.get('phase', '')}",
                f"status={latest.get('status', '')}",
                f"detail={_clean_text(latest.get('detail'))}",
                f"next_phase={meta.get('next_phase', '')}",
                f"stop_status={meta.get('stop_status', '')}",
                f"high_reward_signal_id={meta.get('high_reward_signal_id', '')}",
                f"plausibility_score={_ensure_dict(state.get('plausibility')).get('plausibility_score', 0.0)}",
                f"plausible_solution_detected={decision.get('plausible_solution_detected', False)}",
                f"authority_mode={meta.get('authority_mode', '')}",
                f"authoritative={meta.get('authoritative', False)}",
                f"promotion_allowed={meta.get('promotion_allowed', False)}",
            ]
        ),
        surface_focus="work-loop",
        surface_stage="work",
        surface_metrics={
            "cycle_count": int(meta.get("cycle_count", 0) or 0),
            "plausibility_score": float(_ensure_dict(state.get("plausibility")).get("plausibility_score", 0.0) or 0.0),
            "plausible_solution_detected": 1 if decision.get("plausible_solution_detected") else 0,
            "high_reward_active": 1 if meta.get("high_reward_active") else 0,
        },
        surface_taxonomy={"reasoning_types": ["work-loop", "discovery", "prove", "proof-critic"]},
        surface_pdl=_ensure_dict(latest.get("pdl_payload")),
    )
    logger.add_output("work_state_json", output_json)
    logger.add_output("work_state_md", output_md)
    logger.add_output("end_to_end_plausibility_json", plausibility_json)
    logger.add_output("end_to_end_plausibility_md", plausibility_md)
    if _clean_text(meta.get("high_reward_signal_id")):
        watch_json, watch_md = high_reward_watch_paths(artifacts_dir)
        logger.add_output("high_reward_watch_json", watch_json)
        logger.add_output("high_reward_watch_md", watch_md)
    outputs = _ensure_dict(latest.get("outputs"))
    for key, value in outputs.items():
        if _clean_text(value):
            logger.add_output(key, Path(_clean_text(value)))
    log_path = logger.finalize(
        "success",
        summary=f"Ran work cycle for `{kb_ref}`; phase `{latest.get('phase', '')}` ended with status `{latest.get('status', '')}`.",
    )
    print(f"[OK] Wrote work-state JSON: {output_json}")
    print(f"[OK] Wrote work-state Markdown: {output_md}")
    print(f"[OK] Wrote plausibility JSON: {plausibility_json}")
    print(f"[OK] Wrote plausibility Markdown: {plausibility_md}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
