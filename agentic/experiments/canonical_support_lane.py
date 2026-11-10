# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Parallel production and serial commitment for theory-subordinate support.

The canonical theory cycle commits generation ``N`` before this module may run.
One anchor then commits at ``N+1``; five independently produced world
observations are accepted only in the fixed :data:`WORLD_IDS` order at
``N+2`` through ``N+6``; and one aggregation commits at ``N+7``.  Producer
execution is a real concurrent wave, while persistence is deliberately serial.

The API is restartable.  An exact anchor retry is idempotent, an interrupted
prefix is replayed before missing worlds are produced, and an already committed
observation is never replaced by a newly returned value.  The returned support
reference contains only portable commit references and the certificate's typed
next-cycle reflection request.  It cannot mutate theory, select a branch,
authorize proof, or establish physical-target support.
"""

from __future__ import annotations

import copy
from concurrent.futures import (
    Future,
    ThreadPoolExecutor,
    TimeoutError as FuturesTimeoutError,
    as_completed,
)
from dataclasses import dataclass
from threading import Barrier
from typing import Any, Callable, Mapping, Sequence

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    validate_identifier,
    validate_payload,
)
from agentic.state.discovery_transaction import DiscoveryTransactionStore

from .world_matrix import (
    WORLD_IDS,
    CommittedCausalEvidencePaths,
)
from .world_matrix_commits import (
    VerifiedWorldMatrixAggregationCommit,
    VerifiedWorldMatrixAnchorCommit,
    VerifiedWorldMatrixObservationCommit,
    build_world_matrix_aggregation_input_manifest,
    commit_canonical_world_matrix_aggregation,
    commit_canonical_world_matrix_anchor,
    commit_canonical_world_matrix_observation,
    derive_canonical_world_matrix_certificate,
    replay_canonical_world_matrix_commit_chain,
    require_active_canonical_world_matrix_commit_chain,
)


_LOCAL_PRODUCER_AUTHORITY = (
    "local_transcript_only_not_external_or_independent_authority"
)
_SUPPORT_BOUNDARY = (
    "secondary support over immutable theory N; only the typed aggregation "
    "request for next-cycle reflection may leave this lane"
)
_SUPPORT_SCHEMA = "canonical_support_lane.schema.json"


class SupportLaneProductionError(ContractError):
    """One or more parallel producers failed before their serial commit."""

    def __init__(self, failures: Mapping[str, Exception]) -> None:
        self.failures = dict(failures)
        summary = ", ".join(
            f"{world_id}:{type(error).__name__}"
            for world_id, error in sorted(self.failures.items())
        )
        super().__init__(f"parallel support production failed: {summary}")


class SupportLaneProductionTimeout(SupportLaneProductionError):
    """The producer wave exceeded its deadline before every world terminated."""

    def __init__(self, timed_out_world_ids: Sequence[str]) -> None:
        self.timed_out_world_ids = tuple(timed_out_world_ids)
        super().__init__(
            {
                world_id: TimeoutError("world producer exceeded the wave deadline")
                for world_id in self.timed_out_world_ids
            }
        )


@dataclass(frozen=True, slots=True)
class WorldObservationProduction:
    """One producer's exact observation output and local evidence paths."""

    world_id: str
    observation_envelope: Mapping[str, Any]
    evidence_records: tuple[CommittedCausalEvidencePaths, ...]
    production_receipt: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class AggregationProduction:
    """The aggregation producer binding and its local evidence paths."""

    aggregation_producer_binding: Mapping[str, Any]
    evidence_records: tuple[CommittedCausalEvidencePaths, ...]
    production_receipt: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class CanonicalSupportLaneResult:
    """Verified N+1..N+7 commits plus a compact theory-subordinate receipt."""

    anchor: VerifiedWorldMatrixAnchorCommit
    observations: tuple[VerifiedWorldMatrixObservationCommit, ...]
    aggregation: VerifiedWorldMatrixAggregationCommit
    parallel_production_receipt: Mapping[str, Any]
    support_reference: Mapping[str, Any]


WorldProducer = Callable[[Mapping[str, Any]], WorldObservationProduction]
AggregationProducer = Callable[[Mapping[str, Any]], AggregationProduction]
Failpoint = str | Callable[[str], None] | None


def _self_digest(value: Mapping[str, Any], field: str) -> str:
    return canonical_digest(
        {key: item for key, item in value.items() if key != field}
    )


def build_local_production_receipt(
    *,
    producer_id: str,
    invocation_id: str,
    request_digest: str,
    output: Mapping[str, Any],
) -> dict[str, Any]:
    """Build a replayable local receipt without claiming independent authority."""

    validate_identifier(producer_id, "producer_id")
    validate_identifier(invocation_id, "invocation_id")
    receipt: dict[str, Any] = {
        "schema_version": "1.0.0",
        "receipt_kind": "canonical_support_local_production",
        "producer_id": producer_id,
        "invocation_id": invocation_id,
        "request_digest": request_digest,
        "output_digest": canonical_digest(output),
        "status": "succeeded",
        "producer_authority": _LOCAL_PRODUCER_AUTHORITY,
        "external_independence_authority": None,
    }
    receipt["receipt_id"] = stable_identifier(
        "support-production-receipt", producer_id, invocation_id, request_digest
    )
    receipt["receipt_digest"] = canonical_digest(receipt)
    validate_payload(receipt, _SUPPORT_SCHEMA)
    return receipt


def _validate_production_receipt(
    receipt: Mapping[str, Any],
    *,
    request_digest: str,
    output: Mapping[str, Any],
) -> dict[str, Any]:
    record = copy.deepcopy(dict(receipt))
    required = {
        "schema_version",
        "receipt_kind",
        "producer_id",
        "invocation_id",
        "request_digest",
        "output_digest",
        "status",
        "producer_authority",
        "external_independence_authority",
        "receipt_id",
        "receipt_digest",
    }
    if set(record) != required:
        raise ContractError("support production receipt has an open or incomplete shape")
    validate_identifier(str(record["producer_id"]), "producer_id")
    validate_identifier(str(record["invocation_id"]), "invocation_id")
    if (
        record["schema_version"] != "1.0.0"
        or record["receipt_kind"] != "canonical_support_local_production"
        or record["request_digest"] != request_digest
        or record["output_digest"] != canonical_digest(output)
        or record["status"] != "succeeded"
        or record["producer_authority"] != _LOCAL_PRODUCER_AUTHORITY
        or record["external_independence_authority"] is not None
        or record["receipt_id"]
        != stable_identifier(
            "support-production-receipt",
            record["producer_id"],
            record["invocation_id"],
            request_digest,
        )
        or record["receipt_digest"] != _self_digest(record, "receipt_digest")
    ):
        raise ContractError("support production receipt identity or digest drifted")
    validate_payload(record, _SUPPORT_SCHEMA)
    return record


def _validate_parallel_production_receipt(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    record = copy.deepcopy(dict(receipt))
    validate_payload(record, _SUPPORT_SCHEMA)
    submitted = list(record["submitted_world_ids"])
    completion = list(record["completion_order"])
    receipt_digests = list(record["production_receipt_digests"])
    if (
        not set(submitted).issubset(set(WORLD_IDS))
        or set(completion) != set(submitted)
        or len(completion) != len(submitted)
        or len(receipt_digests) != len(submitted)
        or len(set(receipt_digests)) != len(receipt_digests)
        or record["max_workers"] != len(submitted)
        or record["parallel_receipt_digest"]
        != _self_digest(record, "parallel_receipt_digest")
    ):
        raise ContractError("parallel production receipt identity or cardinality drifted")
    return record


def _world_production_request(
    *,
    world_id: str,
    world_request: Mapping[str, Any],
    anchor_reference: Mapping[str, Any],
) -> dict[str, Any]:
    request: dict[str, Any] = {
        "schema_version": "1.0.0",
        "request_kind": "produce_one_theory_subordinate_world_observation",
        "world_id": world_id,
        "world_request": copy.deepcopy(dict(world_request)),
        "anchor_reference": copy.deepcopy(dict(anchor_reference)),
        "theory_mutation_authorized": False,
        "canonical_commit_order": list(WORLD_IDS),
    }
    request["request_digest"] = canonical_digest(request)
    return request


def _aggregation_production_request(
    *,
    aggregation_input_manifest: Mapping[str, Any],
    certificate: Mapping[str, Any],
) -> dict[str, Any]:
    request: dict[str, Any] = {
        "schema_version": "1.0.0",
        "request_kind": "produce_theory_subordinate_world_aggregation",
        "aggregation_input_manifest": copy.deepcopy(
            dict(aggregation_input_manifest)
        ),
        "certificate": copy.deepcopy(dict(certificate)),
        "theory_mutation_authorized": False,
        "only_permitted_downstream_effect": "pending_next_cycle_reflection_only",
    }
    request["request_digest"] = canonical_digest(request)
    return request


def _produce_parallel_wave(
    *,
    missing_world_ids: Sequence[str],
    world_requests: Mapping[str, Mapping[str, Any]],
    anchor_reference: Mapping[str, Any],
    world_producers: Mapping[str, WorldProducer],
    max_workers: int,
    wave_timeout_seconds: float,
) -> tuple[dict[str, WorldObservationProduction], dict[str, Any]]:
    if (
        isinstance(wave_timeout_seconds, bool)
        or not isinstance(wave_timeout_seconds, (int, float))
        or wave_timeout_seconds <= 0
    ):
        raise ContractError("parallel support wave timeout must be positive")
    if not missing_world_ids:
        receipt: dict[str, Any] = {
            "schema_version": "1.0.0",
            "execution_mode": "parallel_production_serial_commit",
            "submitted_world_ids": [],
            "completion_order": [],
            "canonical_commit_order": list(WORLD_IDS),
            "max_workers": 0,
            "wave_timeout_seconds": float(wave_timeout_seconds),
            "production_receipt_digests": [],
            "producer_failures": [],
            "authority_boundary": _SUPPORT_BOUNDARY,
        }
        receipt["parallel_receipt_digest"] = canonical_digest(receipt)
        return {}, _validate_parallel_production_receipt(receipt)
    if (
        isinstance(max_workers, bool)
        or not isinstance(max_workers, int)
        or max_workers < len(missing_world_ids)
        or max_workers > len(WORLD_IDS)
    ):
        raise ContractError(
            "parallel support requires one available worker for every missing world"
        )
    barrier = Barrier(len(missing_world_ids))
    requests = {
        world_id: _world_production_request(
            world_id=world_id,
            world_request=world_requests[world_id],
            anchor_reference=anchor_reference,
        )
        for world_id in missing_world_ids
    }

    def invoke(world_id: str) -> WorldObservationProduction:
        barrier.wait()
        return world_producers[world_id](copy.deepcopy(requests[world_id]))

    results: dict[str, WorldObservationProduction] = {}
    failures: dict[str, Exception] = {}
    completion_order: list[str] = []
    pool = ThreadPoolExecutor(
        max_workers=len(missing_world_ids),
        thread_name_prefix="canonical-support-world",
    )
    futures: dict[Future[WorldObservationProduction], str]
    try:
        futures = {
            pool.submit(invoke, world_id): world_id
            for world_id in missing_world_ids
        }
        try:
            completed = as_completed(
                futures,
                timeout=float(wave_timeout_seconds),
            )
            for future in completed:
                world_id = futures[future]
                completion_order.append(world_id)
                try:
                    production = future.result()
                except Exception as exc:  # retain every ordinary producer failure
                    failures[world_id] = exc
                    continue
                if not isinstance(production, WorldObservationProduction):
                    failures[world_id] = ContractError(
                        "world producer returned an untyped output"
                    )
                    continue
                results[world_id] = production
        except FuturesTimeoutError:
            timed_out = [
                world_id
                for future, world_id in futures.items()
                if not future.done()
            ]
            for future in futures:
                future.cancel()
            raise SupportLaneProductionTimeout(timed_out)
    finally:
        # Running callbacks cannot be killed safely in a thread.  They receive
        # no commit capability, so any late return is diagnostic-only and can
        # never enter the serial canonical commit loop below.
        pool.shutdown(wait=False, cancel_futures=True)
    if failures:
        raise SupportLaneProductionError(failures)

    receipt_digests: list[str] = []
    for world_id in missing_world_ids:
        production = results[world_id]
        request = requests[world_id]
        if production.world_id != world_id:
            raise ContractError("parallel producer returned another world's identity")
        validated_receipt = _validate_production_receipt(
            production.production_receipt,
            request_digest=request["request_digest"],
            output=production.observation_envelope,
        )
        receipt_digests.append(validated_receipt["receipt_digest"])
    parallel_receipt: dict[str, Any] = {
        "schema_version": "1.0.0",
        "execution_mode": "parallel_production_serial_commit",
        "submitted_world_ids": list(missing_world_ids),
        "completion_order": completion_order,
        "canonical_commit_order": list(WORLD_IDS),
        "max_workers": len(missing_world_ids),
        "wave_timeout_seconds": float(wave_timeout_seconds),
        "production_receipt_digests": receipt_digests,
        "producer_failures": [],
        "authority_boundary": _SUPPORT_BOUNDARY,
    }
    parallel_receipt["parallel_receipt_digest"] = canonical_digest(
        parallel_receipt
    )
    return results, _validate_parallel_production_receipt(parallel_receipt)


def _failpoint(
    failpoints: Mapping[str, Failpoint] | None, key: str
) -> Failpoint:
    return None if failpoints is None else failpoints.get(key)


def run_canonical_theory_support_lane(
    *,
    store: DiscoveryTransactionStore,
    theory_generation: int,
    cycle_id: str,
    commission: Mapping[str, Any],
    commission_producer_binding: Mapping[str, Any],
    world_requests: Mapping[str, Mapping[str, Any]],
    world_request_producer_bindings: Mapping[str, Mapping[str, Any]],
    anchor_evidence_records: Sequence[CommittedCausalEvidencePaths],
    world_producers: Mapping[str, WorldProducer],
    aggregation_producer: AggregationProducer,
    max_workers: int = 5,
    wave_timeout_seconds: float = 120.0,
    failpoints: Mapping[str, Failpoint] | None = None,
) -> CanonicalSupportLaneResult:
    """Run or resume the sole canonical N+1..N+7 support transaction."""

    # Imported here because committed_projection itself imports the experiment
    # world contract.  Keeping this edge lazy preserves package-level imports
    # while leaving the runtime dependency exact and unavoidable.
    from agentic.discovery.committed_projection import (
        derive_committed_cycle_world_authority_projection,
    )

    validate_identifier(cycle_id, "cycle_id")
    if set(world_requests) != set(WORLD_IDS):
        raise ContractError("support lane requires exactly five pre-anchor requests")
    if set(world_request_producer_bindings) != set(WORLD_IDS):
        raise ContractError(
            "support lane requires exactly five pre-anchor request producers"
        )
    if set(world_producers) != set(WORLD_IDS):
        raise ContractError("support lane requires exactly five world producers")
    derived_projection = derive_committed_cycle_world_authority_projection(
        store, theory_generation
    )
    if commission.get("authority_projection") != derived_projection:
        raise ContractError(
            "support commission is not derived from the exact committed theory generation"
        )
    anchor = commit_canonical_world_matrix_anchor(
        store=store,
        expected_generation=theory_generation,
        cycle_id=cycle_id,
        authority_projection=derived_projection,
        commission=commission,
        commission_producer_binding=commission_producer_binding,
        world_requests=world_requests,
        world_request_producer_bindings=world_request_producer_bindings,
        evidence_records=anchor_evidence_records,
        failpoint=_failpoint(failpoints, "anchor"),
    )
    prefix = replay_canonical_world_matrix_commit_chain(
        store=store,
        anchor_reference=anchor.commit_reference,
    )
    if prefix["aggregation_transition"] is not None:
        active = require_active_canonical_world_matrix_commit_chain(
            store=store,
            anchor_reference=anchor.commit_reference,
        )
        empty_parallel = _produce_parallel_wave(
            missing_world_ids=(),
            world_requests=world_requests,
            anchor_reference=anchor.commit_reference,
            world_producers=world_producers,
            max_workers=max_workers,
            wave_timeout_seconds=wave_timeout_seconds,
        )[1]
        support = _support_reference(active)
        return CanonicalSupportLaneResult(
            anchor=anchor,
            observations=tuple(),
            aggregation=VerifiedWorldMatrixAggregationCommit(
                active["aggregation_transition"],
                active["aggregation_reference"],
                active["verified_commits"][-1],
            ),
            parallel_production_receipt=empty_parallel,
            support_reference=support,
        )

    existing_count = len(prefix["observation_transitions"])
    missing_world_ids = WORLD_IDS[existing_count:]
    produced, parallel_receipt = _produce_parallel_wave(
        missing_world_ids=missing_world_ids,
        world_requests=world_requests,
        anchor_reference=anchor.commit_reference,
        world_producers=world_producers,
        max_workers=max_workers,
        wave_timeout_seconds=wave_timeout_seconds,
    )
    committed_observations: list[VerifiedWorldMatrixObservationCommit] = []
    for world_id in missing_world_ids:
        production = produced[world_id]
        committed_observations.append(
            commit_canonical_world_matrix_observation(
                store=store,
                anchor_reference=anchor.commit_reference,
                expected_generation=store.current_generation(),
                observation_envelope=production.observation_envelope,
                evidence_records=production.evidence_records,
                failpoint=_failpoint(failpoints, world_id),
            )
        )

    ready = replay_canonical_world_matrix_commit_chain(
        store=store,
        anchor_reference=anchor.commit_reference,
    )
    if len(ready["observation_references"]) != len(WORLD_IDS):
        raise ContractError("support lane did not commit exactly five observations")
    aggregation_input = build_world_matrix_aggregation_input_manifest(
        anchor_reference=ready["anchor_reference"],
        observation_references=ready["observation_references"],
        commission_id=ready["anchor_transition"]["commission_id"],
        commission_digest=ready["anchor_transition"]["commission_digest"],
    )
    certificate = derive_canonical_world_matrix_certificate(
        store=store,
        anchor_reference=anchor.commit_reference,
    )
    aggregation_request = _aggregation_production_request(
        aggregation_input_manifest=aggregation_input,
        certificate=certificate,
    )
    aggregation_output = aggregation_producer(copy.deepcopy(aggregation_request))
    if not isinstance(aggregation_output, AggregationProduction):
        raise ContractError("aggregation producer returned an untyped output")
    _validate_production_receipt(
        aggregation_output.production_receipt,
        request_digest=aggregation_request["request_digest"],
        output=aggregation_output.aggregation_producer_binding,
    )
    aggregation = commit_canonical_world_matrix_aggregation(
        store=store,
        anchor_reference=anchor.commit_reference,
        expected_generation=store.current_generation(),
        aggregation_producer_binding=(
            aggregation_output.aggregation_producer_binding
        ),
        evidence_records=aggregation_output.evidence_records,
        failpoint=_failpoint(failpoints, "aggregation"),
    )
    active = require_active_canonical_world_matrix_commit_chain(
        store=store,
        anchor_reference=anchor.commit_reference,
    )
    return CanonicalSupportLaneResult(
        anchor=anchor,
        observations=tuple(committed_observations),
        aggregation=aggregation,
        parallel_production_receipt=parallel_receipt,
        support_reference=_support_reference(active),
    )


def _support_reference(replay: Mapping[str, Any]) -> dict[str, Any]:
    """Build one retry-stable reference from the committed full-wave history."""

    certificate = replay["certificate"]
    production_manifest: dict[str, Any] = {
        "schema_version": "1.0.0",
        "manifest_kind": "canonical_support_committed_full_wave",
        "canonical_commit_order": list(WORLD_IDS),
        "anchor_reference": copy.deepcopy(replay["anchor_reference"]),
        "observation_references": copy.deepcopy(
            replay["observation_references"]
        ),
        "aggregation_reference": copy.deepcopy(
            replay["aggregation_reference"]
        ),
        "certificate_id": certificate["certificate_id"],
        "certificate_digest": certificate["certificate_digest"],
    }
    production_manifest["production_manifest_digest"] = canonical_digest(
        production_manifest
    )
    reference: dict[str, Any] = {
        "schema_version": "1.0.0",
        "reference_kind": "canonical_theory_subordinate_support",
        "programme_id": replay["programme_id"],
        "target_id": replay["anchor_transition"]["target_id"],
        "run_id": replay["anchor_transition"]["run_id"],
        "theory_generation": replay["anchor_transition"]["prior_generation"],
        "anchor_reference": copy.deepcopy(replay["anchor_reference"]),
        "observation_references": copy.deepcopy(
            replay["observation_references"]
        ),
        "aggregation_reference": copy.deepcopy(
            replay["aggregation_reference"]
        ),
        "certificate_id": certificate["certificate_id"],
        "certificate_digest": certificate["certificate_digest"],
        "pending_next_cycle_reflection": copy.deepcopy(
            certificate["pending_review"]
        ),
        "derived_denials": copy.deepcopy(certificate["derived_denials"]),
        "production_manifest": production_manifest,
        "production_manifest_digest": production_manifest[
            "production_manifest_digest"
        ],
        "theory_mutation_authorized": False,
        "theory_selection_authorized": False,
        "proof_authorized": False,
        "physical_target_support_authorized": False,
        "authority_boundary": _SUPPORT_BOUNDARY,
    }
    reference["support_reference_digest"] = canonical_digest(reference)
    validate_payload(reference, _SUPPORT_SCHEMA)
    if reference["support_reference_digest"] != _self_digest(
        reference, "support_reference_digest"
    ):
        raise ContractError("canonical support reference digest drifted")
    return reference


__all__ = [
    "AggregationProduction",
    "CanonicalSupportLaneResult",
    "SupportLaneProductionError",
    "SupportLaneProductionTimeout",
    "WorldObservationProduction",
    "build_local_production_receipt",
    "run_canonical_theory_support_lane",
]
