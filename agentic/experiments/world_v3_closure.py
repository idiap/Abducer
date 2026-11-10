# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Contextual replay for thin world-v3 support and descendant closures.

The v3 schemas and :mod:`agentic.experiments.world_object_roles` deliberately
prove only local object shape and payload-derived storage edges.  A valid
request, result, or envelope can still be spliced into the wrong target, run,
world, or generation unless the whole closed diagram is replayed together.
This module supplies that missing contextual layer.

``validate_world_v3_closure`` validates only the N+7 support prefix.  Canonical
active-current completion requires :func:`validate_world_v3_descendant_closure`,
which adds a sole immutable N+8 return and rejects the old endpoint as final
authority.  Both validators accept store-resolved, path-free content objects
plus their exact committed generations.  It reconstructs the frozen theory
base, the anchor, five sequential storage commits, and the aggregation root;
then it replays every portable materializer binding as byte provenance.  The
result establishes a bounded local causal diagram only.  It does not establish
that an experiment is scientifically sound, that a source is true, that a
result changes the current theory, or that any physics claim is warranted.
"""

from __future__ import annotations

import copy
import json
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from agentic.discovery.contracts import ContractError, canonical_json
from agentic.experiments.causal_materializer_content_graph_v3 import (
    validate_portable_causal_materialization_closure_v3,
)
from agentic.experiments.world_object_graph import (
    ResolvedContentObject,
    build_content_object_ref,
)
from agentic.experiments.world_object_roles import (
    derive_content_object_edges,
    validate_payload_derived_edges,
    validate_role_bound_object,
)


WORLD_ORDER = (
    "no_probe",
    "neutral_inconclusive",
    "misleading_toy_positive",
    "registered_premise_falsifier",
    "operational_failure",
)
PROJECTION_COMPONENT_ORDER = (
    "committed_ancestor",
    "theory_programme",
    "reflection_packet",
    "conceptual_systems",
    "genealogy",
    "source_authority",
    "registered_claim",
    "generator_authority",
    "adjudication_authority",
    "schedule",
)
THEORY_COMPONENT_KINDS = frozenset(PROJECTION_COMPONENT_ORDER) - {
    "committed_ancestor",
    "source_authority",
}

_DOMAIN_COUNTS = {
    "world_theory_carrier_v3": 9,
    "world_precommit_ancestor_carrier_v3": 1,
    "world_plan_v3": 5,
    "world_no_probe_decision_v3": 1,
    "world_execution_result_v3": 4,
    "world_next_cycle_reflection_v3": 4,
    "world_projection_component_v3": 10,
    "world_projection_index_v3": 1,
    "world_matrix_commission_v3": 1,
    "world_request_v3": 5,
    "world_observation_v3": 5,
    "world_observation_envelope_v3": 5,
    "world_matrix_certificate_v3": 1,
    "world_matrix_anchor_root_v3": 1,
    "world_matrix_aggregation_root_v3": 1,
}


def _decode_ref(data: bytes, label: str) -> dict[str, Any]:
    """Return one defensive canonical mapping stored inside a verified result."""

    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} is not canonical JSON") from exc
    if not isinstance(value, dict) or canonical_json(value) != data:
        raise ContractError(f"{label} is not one canonical JSON object")
    return value


@dataclass(frozen=True, slots=True)
class VerifiedWorldV3Closure:
    """Defensive summary of a replayed N-1 through N+7 world closure.

    The summary intentionally exposes references and ordering, not hydrated
    scientific values.  Consumers that need domain meaning must reopen the
    exact objects again and apply their own registered semantic validators.
    """

    target_id: str
    run_id: str
    theory_generation: int
    prior_state_version: int
    consumed_object_ids: tuple[str, ...]
    materializer_binding_ids: tuple[str, ...]
    world_ids: tuple[str, ...]
    world_generations: tuple[int, ...]
    result_effect: str
    _anchor_ref_data: bytes
    _envelope_ref_data: tuple[bytes, ...]
    _aggregation_ref_data: bytes

    @property
    def anchor_root_ref(self) -> dict[str, Any]:
        """Return a defensive copy of the exact N+1 anchor ref."""

        return _decode_ref(self._anchor_ref_data, "verified world-v3 anchor ref")

    @property
    def observation_envelope_refs(self) -> tuple[dict[str, Any], ...]:
        """Return defensive copies of the five N+2 through N+6 refs."""

        return tuple(
            _decode_ref(data, "verified world-v3 envelope ref")
            for data in self._envelope_ref_data
        )

    @property
    def aggregation_root_ref(self) -> dict[str, Any]:
        """Return a defensive copy of the exact N+7 aggregation ref."""

        return _decode_ref(
            self._aggregation_ref_data,
            "verified world-v3 aggregation ref",
        )


@dataclass(frozen=True, slots=True)
class VerifiedWorldV3DescendantClosure:
    """A complete active chronology ending in the immutable N+8 return."""

    support_prefix: VerifiedWorldV3Closure
    reflection_generation: int
    result_effect: str
    current_cycle_theory_mutation_authorized: bool
    automatic_theory_selection_authorized: bool
    proof_authorized: bool
    physics_authority: bool
    _reflection_ref_data: bytes

    @property
    def reflection_root_ref(self) -> dict[str, Any]:
        """Return a defensive copy of the exact N+8 root reference."""

        return _decode_ref(
            self._reflection_ref_data,
            "verified world-v3 descendant reflection ref",
        )


def _copy_ref(raw: Mapping[str, Any], label: str) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise ContractError(f"{label} must be a content-object ref")
    return copy.deepcopy(dict(raw))


def validate_world_v3_closure(
    objects: Sequence[ResolvedContentObject],
    aggregation_root_ref: Mapping[str, Any],
    *,
    theory_generation: int,
    committed_generations: Mapping[str, int],
) -> VerifiedWorldV3Closure:
    """Replay the exact N-1 through N+7 support prefix, not canonical finality.

    ``objects`` must be the already resolved exact content-object closure.
    ``committed_generations`` is the commit-membership projection supplied by
    the transaction layer and must account for every object exactly once.  A
    future canonical caller should derive that projection from store-minted
    commit contexts; this validator never treats a free generation number as
    transaction authority by itself.

    Five experiment worlds share the frozen N/N+1 inputs and may be produced in
    parallel.  Their N+2..N+6 predecessor links express storage order only:
    semantic result flow between sibling worlds is rejected by the generation
    and exact-parent checks.  Results can affect only a later reflection.
    """

    if isinstance(objects, (str, bytes)) or not isinstance(objects, Sequence):
        raise ContractError("world-v3 closure must be a sequence")
    if type(theory_generation) is not int or theory_generation < 1:
        raise ContractError("world-v3 theory generation must be a positive integer")
    if not isinstance(committed_generations, Mapping):
        raise ContractError("world-v3 committed generations must be a mapping")

    by_id: dict[str, ResolvedContentObject] = {}
    by_kind: dict[str, list[ResolvedContentObject]] = defaultdict(list)
    role_objects: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for resolved in objects:
        if type(resolved) is not ResolvedContentObject:
            raise ContractError("world-v3 closure requires exact resolved objects")
        if type(resolved.data) is not bytes:
            raise ContractError("world-v3 resolved object bytes are not immutable bytes")
        value = copy.deepcopy(dict(resolved.value))
        if canonical_json(value) != resolved.data:
            raise ContractError(
                "world-v3 resolved bytes differ from their canonical decoded value"
            )
        ref = _copy_ref(resolved.ref, "world-v3 resolved ref")
        expected_ref = build_content_object_ref(
            object_kind=str(ref.get("object_kind", "")),
            data=resolved.data,
            semantic_value=value,
        )
        if ref != expected_ref:
            raise ContractError("world-v3 resolved object identity does not replay")
        value = validate_role_bound_object(ref, value)
        object_id = str(ref["object_id"])
        if object_id in by_id:
            raise ContractError("world-v3 closure repeats a content object")
        defensive = ResolvedContentObject(
            ref=ref,
            value=value,
            data=bytes(resolved.data),
        )
        by_id[object_id] = defensive
        by_kind[str(ref["object_kind"])].append(defensive)
        role_objects.append((ref, value))

    if not by_id:
        raise ContractError("world-v3 closure is empty")
    if set(committed_generations) != set(by_id):
        raise ContractError(
            "world-v3 generation membership differs from the exact object closure"
        )
    generations: dict[str, int] = {}
    for object_id, raw_generation in committed_generations.items():
        if type(raw_generation) is not int:
            raise ContractError("world-v3 object generation must be an integer")
        if not theory_generation - 1 <= raw_generation <= theory_generation + 7:
            raise ContractError("world-v3 object generation lies outside N-1 through N+7")
        generations[str(object_id)] = raw_generation

    edges: list[dict[str, str]] = []
    for ref, value in role_objects:
        edges.extend(derive_content_object_edges(object_ref=ref, payload=value))
    validate_payload_derived_edges(objects=role_objects, declared_edges=edges)

    root_ref = _copy_ref(aggregation_root_ref, "world-v3 aggregation-root ref")
    if root_ref.get("object_kind") != "world_matrix_aggregation_root_v3":
        raise ContractError("world-v3 closure root is not an aggregation root")
    try:
        root_resolved = by_id[str(root_ref["object_id"])]
    except KeyError as exc:
        raise ContractError("world-v3 closure lacks its aggregation root") from exc
    if dict(root_resolved.ref) != root_ref:
        raise ContractError("world-v3 aggregation root differs from its exact ref")

    dependencies: dict[str, list[str]] = defaultdict(list)
    dependents: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        source = edge["source_object_id"]
        target = edge["target_object_id"]
        dependencies[target].append(source)
        dependents[source].append(target)
        if generations[source] > generations[target]:
            raise ContractError(
                "world-v3 dependency points backward from a future generation"
            )

    # Reachability is part of contextual closure, not merely graph shape.  It
    # rejects both missing prerequisites and smuggled sixth-world/sidecar
    # objects that are valid in isolation but do not support this exact root.
    reachable: set[str] = set()
    active: set[str] = set()

    def visit(object_id: str) -> None:
        if object_id in active:
            raise ContractError("world-v3 payload-derived dependency graph is cyclic")
        if object_id in reachable:
            return
        active.add(object_id)
        for prerequisite in dependencies.get(object_id, []):
            visit(prerequisite)
        active.remove(object_id)
        reachable.add(object_id)

    visit(str(root_ref["object_id"]))
    if reachable != set(by_id):
        raise ContractError(
            "world-v3 root does not reach the exact supplied object closure"
        )

    for object_kind, expected_count in _DOMAIN_COUNTS.items():
        if len(by_kind.get(object_kind, [])) != expected_count:
            raise ContractError(
                f"world-v3 closure requires exactly {expected_count} {object_kind} object(s)"
            )

    def only(object_kind: str) -> ResolvedContentObject:
        return by_kind[object_kind][0]

    def resolve(
        raw_ref: Mapping[str, Any],
        expected_kind: str,
        label: str,
    ) -> ResolvedContentObject:
        ref = _copy_ref(raw_ref, label)
        if ref.get("object_kind") != expected_kind:
            raise ContractError(f"{label} names the wrong object kind")
        try:
            resolved = by_id[str(ref["object_id"])]
        except KeyError as exc:
            raise ContractError(f"{label} lacks an exact resolved object") from exc
        if dict(resolved.ref) != ref:
            raise ContractError(f"{label} differs from its exact resolved ref")
        return resolved

    aggregation = copy.deepcopy(dict(root_resolved.value))
    anchor_resolved = resolve(
        aggregation["anchor_root_ref"],
        "world_matrix_anchor_root_v3",
        "aggregation anchor",
    )
    anchor = copy.deepcopy(dict(anchor_resolved.value))
    certificate_resolved = resolve(
        aggregation["certificate_ref"],
        "world_matrix_certificate_v3",
        "aggregation certificate",
    )
    certificate = copy.deepcopy(dict(certificate_resolved.value))
    projection_resolved = resolve(
        anchor["projection_index_ref"],
        "world_projection_index_v3",
        "anchor projection",
    )
    projection = copy.deepcopy(dict(projection_resolved.value))
    commission_resolved = resolve(
        anchor["commission_ref"],
        "world_matrix_commission_v3",
        "anchor commission",
    )
    commission = copy.deepcopy(dict(commission_resolved.value))

    target_id = str(anchor["target_id"])
    run_id = str(anchor["run_id"])
    prior_state_version = theory_generation - 1
    for label, value in (
        ("projection", projection),
        ("commission", commission),
        ("anchor", anchor),
        ("aggregation", aggregation),
    ):
        if value.get("target_id") != target_id or value.get("run_id") != run_id:
            raise ContractError(f"world-v3 {label} crosses target or run identity")
    for label, value in (
        ("projection", projection),
        ("commission", commission),
        ("anchor", anchor),
    ):
        if value["prior_state_version"] != prior_state_version:
            raise ContractError(
                f"world-v3 {label} does not bind the exact N-1 state"
            )
    if any(
        value["world_order"] != list(WORLD_ORDER)
        for value in (commission, anchor, certificate, aggregation)
    ):
        raise ContractError("world-v3 world order differs across closure roots")

    component_by_kind: dict[str, ResolvedContentObject] = {}
    component_payloads: dict[str, ResolvedContentObject] = {}
    seen_component_refs: set[str] = set()
    seen_payload_refs: set[str] = set()
    for expected_kind, entry in zip(
        PROJECTION_COMPONENT_ORDER,
        projection["components"],
        strict=True,
    ):
        if entry["component_kind"] != expected_kind:
            raise ContractError("world-v3 projection component vector is relabelled")
        component_resolved = resolve(
            entry["object_ref"],
            "world_projection_component_v3",
            f"projection component {expected_kind}",
        )
        component = copy.deepcopy(dict(component_resolved.value))
        if component["component_kind"] != expected_kind:
            raise ContractError("world-v3 projection component payload is relabelled")
        component_id = str(component_resolved.ref["object_id"])
        if component_id in seen_component_refs:
            raise ContractError("world-v3 projection reuses a component object")
        seen_component_refs.add(component_id)
        payload_ref = component["component_payload_ref"]
        payload_resolved = resolve(
            payload_ref,
            str(payload_ref["object_kind"]),
            f"projection payload {expected_kind}",
        )
        payload_id = str(payload_resolved.ref["object_id"])
        if payload_id in seen_payload_refs:
            raise ContractError("world-v3 projection reuses a semantic carrier")
        seen_payload_refs.add(payload_id)
        component_by_kind[expected_kind] = component_resolved
        component_payloads[expected_kind] = payload_resolved

    ancestor = copy.deepcopy(
        dict(component_payloads["committed_ancestor"].value)
    )
    if (
        ancestor["target_id"] != target_id
        or ancestor["run_id"] != run_id
        or ancestor["precommit_state_version"] != prior_state_version
    ):
        raise ContractError("world-v3 committed ancestor crosses N-1 identity")
    if (
        generations[str(ancestor["precommit_state_ref"]["object_id"])]
        != theory_generation - 1
        or generations[str(ancestor["precommit_receipt_ref"]["object_id"])]
        != theory_generation - 1
    ):
        raise ContractError("world-v3 committed ancestor evidence is not from N-1")

    literature_resolved = component_payloads["source_authority"]
    if dict(anchor["literature_input_ref"]) != dict(literature_resolved.ref):
        raise ContractError("world-v3 anchor literature differs from its projection")
    if generations[str(literature_resolved.ref["object_id"])] != theory_generation:
        raise ContractError("world-v3 literature authority is not a theory-N input")

    theory_carriers: dict[str, ResolvedContentObject] = {}
    for component_kind in THEORY_COMPONENT_KINDS:
        carrier_resolved = component_payloads[component_kind]
        carrier = copy.deepcopy(dict(carrier_resolved.value))
        if carrier["carrier_kind"] != component_kind:
            raise ContractError("world-v3 projection launders a theory carrier")
        theory_carriers[component_kind] = carrier_resolved

    registered_claim_resolved = resolve(
        commission["registered_claim_ref"],
        "world_theory_carrier_v3",
        "commission registered claim",
    )
    if dict(registered_claim_resolved.ref) != dict(
        theory_carriers["registered_claim"].ref
    ):
        raise ContractError("world-v3 commission claim differs from its projection")
    spec_family_resolved = resolve(
        commission["spec_family_ref"],
        "world_theory_carrier_v3",
        "commission specification family",
    )
    if spec_family_resolved.value["carrier_kind"] != "experiment_spec_family":
        raise ContractError("world-v3 commission specification carrier is invalid")
    if str(spec_family_resolved.ref["object_id"]) in seen_payload_refs:
        raise ContractError("world-v3 specification carrier aliases a projection carrier")

    all_carriers = [*theory_carriers.values(), spec_family_resolved]
    carrier_source_ids: set[str] = set()
    for carrier_resolved in all_carriers:
        carrier = copy.deepcopy(dict(carrier_resolved.value))
        source_id = str(carrier["source_ref"]["object_id"])
        if source_id in carrier_source_ids:
            raise ContractError("world-v3 theory carriers reuse a semantic source")
        carrier_source_ids.add(source_id)
        if (
            generations[source_id] != theory_generation
            or generations[str(carrier["source_receipt_ref"]["object_id"])]
            != theory_generation
        ):
            raise ContractError("world-v3 theory carrier is not derived from theory N")

    anchor_generation = theory_generation + 1
    anchor_kinds = {
        "world_theory_carrier_v3",
        "world_precommit_ancestor_carrier_v3",
        "world_projection_component_v3",
        "world_projection_index_v3",
        "world_matrix_commission_v3",
        "world_plan_v3",
        "world_request_v3",
        "world_matrix_anchor_root_v3",
    }
    for object_kind in anchor_kinds:
        for resolved in by_kind[object_kind]:
            if generations[str(resolved.ref["object_id"])] != anchor_generation:
                raise ContractError(
                    f"world-v3 {object_kind} is not committed at anchor N+1"
                )

    requests: list[ResolvedContentObject] = []
    plans: list[ResolvedContentObject] = []
    request_bindings: list[dict[str, Any]] = []
    for ordinal, (world_id, request_entry, binding_entry) in enumerate(
        zip(
            WORLD_ORDER,
            anchor["world_requests"],
            anchor["world_request_materializer_bindings"],
            strict=True,
        )
    ):
        if (
            request_entry["world_id"] != world_id
            or binding_entry["world_id"] != world_id
        ):
            raise ContractError("world-v3 anchor request vector is relabelled")
        request_resolved = resolve(
            request_entry["object_ref"],
            "world_request_v3",
            f"anchor request {world_id}",
        )
        request = copy.deepcopy(dict(request_resolved.value))
        plan_resolved = resolve(
            request["world_plan_ref"],
            "world_plan_v3",
            f"world plan {world_id}",
        )
        plan = copy.deepcopy(dict(plan_resolved.value))
        disposition = "not_executed" if ordinal == 0 else "executed"
        if (
            request["world_id"] != world_id
            or request["world_ordinal"] != ordinal
            or request["execution_disposition"] != disposition
            or request["commission_ref"] != dict(commission_resolved.ref)
            or plan["world_id"] != world_id
            or plan["world_ordinal"] != ordinal
            or plan["execution_disposition"] != disposition
            or plan["commission_ref"] != dict(commission_resolved.ref)
        ):
            raise ContractError("world-v3 request and plan identities do not commute")
        requests.append(request_resolved)
        plans.append(plan_resolved)
        request_bindings.append(copy.deepcopy(dict(binding_entry["object_ref"])))
    if len({str(row.ref["object_id"]) for row in plans}) != len(WORLD_ORDER):
        raise ContractError("world-v3 plans are not five distinct objects")

    materializer_cache: dict[str, tuple[int, bytes]] = {}
    materializer_ids: list[str] = []

    def verify_materialization(
        binding_ref: Mapping[str, Any],
        expected: ResolvedContentObject,
        *,
        owner_generation: int,
        label: str,
    ) -> None:
        ref = _copy_ref(binding_ref, f"{label} materializer binding")
        binding_resolved = resolve(
            ref,
            "causal_materializer_binding_header_v3",
            f"{label} materializer binding",
        )
        binding_id = str(binding_resolved.ref["object_id"])
        if generations[binding_id] != owner_generation:
            raise ContractError(f"{label} materializer binding is in the wrong generation")
        cached = materializer_cache.get(binding_id)
        if cached is not None:
            if cached != (owner_generation, expected.data):
                raise ContractError(
                    f"{label} reuses a materializer binding for different bytes"
                )
            return
        verified = validate_portable_causal_materialization_closure_v3(
            tuple(by_id.values()),
            ref,
        )
        artifact_resolved = resolve(
            verified.artifact_ref,
            "causal_materializer_artifact_evidence_v3",
            f"{label} materializer artifact",
        )
        if (
            artifact_resolved.data != expected.data
            or artifact_resolved.value != expected.value
        ):
            raise ContractError(
                f"{label} materializer artifact differs from the exact domain bytes"
            )
        if generations[str(artifact_resolved.ref["object_id"])] > owner_generation:
            raise ContractError(f"{label} materializer consumes a future artifact")
        for object_id in verified.consumed_object_ids:
            if object_id not in by_id or generations[object_id] > owner_generation:
                raise ContractError(f"{label} materializer consumes future/absent evidence")
        materializer_cache[binding_id] = (owner_generation, bytes(expected.data))
        materializer_ids.append(binding_id)

    verify_materialization(
        commission["adjudication_materializer_binding_ref"],
        resolve(
            theory_carriers["adjudication_authority"].value["source_ref"],
            "producer_artifact_evidence",
            "adjudication source",
        ),
        owner_generation=anchor_generation,
        label="adjudication authority",
    )
    verify_materialization(
        commission["schedule_materializer_binding_ref"],
        resolve(
            theory_carriers["schedule"].value["source_ref"],
            "producer_artifact_evidence",
            "schedule source",
        ),
        owner_generation=anchor_generation,
        label="schedule authority",
    )
    verify_materialization(
        anchor["commission_materializer_binding_ref"],
        commission_resolved,
        owner_generation=anchor_generation,
        label="commission",
    )
    for world_id, request_resolved, binding_ref in zip(
        WORLD_ORDER,
        requests,
        request_bindings,
        strict=True,
    ):
        verify_materialization(
            binding_ref,
            request_resolved,
            owner_generation=anchor_generation,
            label=f"{world_id} request",
        )

    envelope_entries = aggregation["observation_envelopes"]
    certificate_entries = certificate["observation_envelopes"]
    if envelope_entries != certificate_entries:
        raise ContractError(
            "world-v3 certificate and aggregation envelope vectors differ"
        )
    if certificate["commission_ref"] != dict(commission_resolved.ref):
        raise ContractError("world-v3 certificate crosses commission identity")

    envelopes: list[ResolvedContentObject] = []
    observations: list[ResolvedContentObject] = []
    result_ids: set[str] = set()
    reflection_ids: set[str] = set()
    prior_parent_ref = dict(anchor_resolved.ref)
    no_probe_seen = False
    for ordinal, (world_id, entry) in enumerate(
        zip(WORLD_ORDER, envelope_entries, strict=True)
    ):
        if entry["world_id"] != world_id:
            raise ContractError("world-v3 envelope vector is relabelled")
        world_generation = theory_generation + 2 + ordinal
        envelope_resolved = resolve(
            entry["object_ref"],
            "world_observation_envelope_v3",
            f"world envelope {world_id}",
        )
        envelope = copy.deepcopy(dict(envelope_resolved.value))
        observation_resolved = resolve(
            envelope["observation_ref"],
            "world_observation_v3",
            f"world observation {world_id}",
        )
        observation = copy.deepcopy(dict(observation_resolved.value))
        request_resolved = requests[ordinal]
        request = copy.deepcopy(dict(request_resolved.value))
        if (
            envelope["world_id"] != world_id
            or envelope["world_ordinal"] != ordinal
            or envelope["commission_ref"] != dict(commission_resolved.ref)
            or envelope["parent_root_ref"] != prior_parent_ref
            or observation["world_id"] != world_id
            or observation["world_ordinal"] != ordinal
            or observation["commission_ref"] != dict(commission_resolved.ref)
            or observation["request_ref"] != dict(request_resolved.ref)
        ):
            raise ContractError("world-v3 envelope/observation causality is spliced")
        if (
            generations[str(envelope_resolved.ref["object_id"])] != world_generation
            or generations[str(observation_resolved.ref["object_id"])]
            != world_generation
        ):
            raise ContractError("world-v3 world payload is in the wrong generation")
        if generations[str(prior_parent_ref["object_id"])] != world_generation - 1:
            raise ContractError(
                "world-v3 envelope parent is not the immediate storage predecessor"
            )
        verify_materialization(
            envelope["observation_materializer_binding_ref"],
            observation_resolved,
            owner_generation=world_generation,
            label=f"{world_id} observation",
        )

        if ordinal == 0:
            no_probe = resolve(
                observation["no_probe_decision_ref"],
                "world_no_probe_decision_v3",
                "no-probe decision",
            )
            decision = copy.deepcopy(dict(no_probe.value))
            if (
                request["execution_disposition"] != "not_executed"
                or observation["observation_kind"] != "no_probe_decision"
                or decision["request_ref"] != dict(request_resolved.ref)
                or decision["world_id"] != world_id
                or decision["world_ordinal"] != ordinal
                or generations[str(no_probe.ref["object_id"])] != world_generation
            ):
                raise ContractError("world-v3 no-probe branch implies execution")
            no_probe_seen = True
        else:
            if (
                observation["observation_kind"]
                != "executed_result_with_reflection"
                or request["execution_disposition"] != "executed"
                or observation["request_materializer_binding_ref"]
                != request_bindings[ordinal]
            ):
                raise ContractError("world-v3 executed request binding is inconsistent")
            result_resolved = resolve(
                observation["result_ref"],
                "world_execution_result_v3",
                f"{world_id} result",
            )
            reflection_resolved = resolve(
                observation["reflection_ref"],
                "world_next_cycle_reflection_v3",
                f"{world_id} reflection",
            )
            result = copy.deepcopy(dict(result_resolved.value))
            reflection = copy.deepcopy(dict(reflection_resolved.value))
            if (
                result["world_id"] != world_id
                or result["world_ordinal"] != ordinal
                or result["request_ref"] != dict(request_resolved.ref)
                or result["result_effect"] != "next_cycle_reflection_only"
                or reflection["world_id"] != world_id
                or reflection["world_ordinal"] != ordinal
                or reflection["result_ref"] != dict(result_resolved.ref)
                or reflection["current_cycle_theory_mutation_authorized"] is not False
            ):
                raise ContractError("world-v3 result/reflection causality is spliced")
            for child in (result_resolved, reflection_resolved):
                child_id = str(child.ref["object_id"])
                if generations[child_id] != world_generation:
                    raise ContractError(
                        "world-v3 result/reflection is in the wrong generation"
                    )
            result_id = str(result_resolved.ref["object_id"])
            reflection_id = str(reflection_resolved.ref["object_id"])
            if result_id in result_ids or reflection_id in reflection_ids:
                raise ContractError("world-v3 reuses a result or reflection")
            result_ids.add(result_id)
            reflection_ids.add(reflection_id)
            verify_materialization(
                observation["result_materializer_binding_ref"],
                result_resolved,
                owner_generation=world_generation,
                label=f"{world_id} result",
            )
            verify_materialization(
                observation["reflection_materializer_binding_ref"],
                reflection_resolved,
                owner_generation=world_generation,
                label=f"{world_id} reflection",
            )
        envelopes.append(envelope_resolved)
        observations.append(observation_resolved)
        prior_parent_ref = dict(envelope_resolved.ref)

    if not no_probe_seen or len(result_ids) != 4 or len(reflection_ids) != 4:
        raise ContractError("world-v3 closure lacks its closed no-probe/executed sum")
    if len({str(row.ref["object_id"]) for row in envelopes}) != 5:
        raise ContractError("world-v3 closure does not contain five distinct worlds")

    aggregation_generation = theory_generation + 7
    if (
        generations[str(certificate_resolved.ref["object_id"])]
        != aggregation_generation
        or generations[str(root_resolved.ref["object_id"])]
        != aggregation_generation
    ):
        raise ContractError("world-v3 certificate/aggregation is not committed at N+7")
    verify_materialization(
        aggregation["certificate_materializer_binding_ref"],
        certificate_resolved,
        owner_generation=aggregation_generation,
        label="world certificate",
    )

    # Results and reflections may feed their same-world wrapper and later
    # aggregation path only.  The global monotonicity check above already
    # rejects any edge into N/N+1; this role check prevents an unrelated
    # same-generation object from laundering result authority.
    allowed_result_dependents = {
        "world_execution_result_v3": {
            "world_next_cycle_reflection_v3",
            "world_observation_v3",
        },
        "world_next_cycle_reflection_v3": {"world_observation_v3"},
    }
    for object_kind, allowed_kinds in allowed_result_dependents.items():
        for resolved in by_kind[object_kind]:
            for dependent_id in dependents.get(str(resolved.ref["object_id"]), []):
                dependent_kind = str(by_id[dependent_id].ref["object_kind"])
                if dependent_kind not in allowed_kinds:
                    raise ContractError(
                        "world-v3 result authority escapes forward-only reflection"
                    )

    return VerifiedWorldV3Closure(
        target_id=target_id,
        run_id=run_id,
        theory_generation=theory_generation,
        prior_state_version=prior_state_version,
        consumed_object_ids=tuple(sorted(by_id)),
        materializer_binding_ids=tuple(materializer_ids),
        world_ids=WORLD_ORDER,
        world_generations=tuple(
            theory_generation + 2 + ordinal for ordinal in range(len(WORLD_ORDER))
        ),
        result_effect="next_cycle_reflection_only",
        _anchor_ref_data=canonical_json(dict(anchor_resolved.ref)),
        _envelope_ref_data=tuple(
            canonical_json(dict(row.ref)) for row in envelopes
        ),
        _aggregation_ref_data=canonical_json(dict(root_resolved.ref)),
    )


def validate_world_v3_descendant_closure(
    objects: Sequence[ResolvedContentObject],
    reflection_root_ref: Mapping[str, Any],
    *,
    theory_generation: int,
    committed_generations: Mapping[str, int],
) -> VerifiedWorldV3DescendantClosure:
    """Replay the sole canonical N..N+8 descendant experiment chronology.

    The N+8 object is an immutable input for a later theory cycle.  It cannot
    mutate the theory committed at N, select a theory, authorize proof, or
    establish physics.  A bare N+7 aggregation remains a valid historical
    support prefix but is deliberately insufficient for this boundary.
    """

    if isinstance(objects, (str, bytes)) or not isinstance(objects, Sequence):
        raise ContractError("world-v3 descendant closure must be a sequence")
    if not isinstance(committed_generations, Mapping):
        raise ContractError("world-v3 descendant generations must be a mapping")
    root_ref = _copy_ref(
        reflection_root_ref,
        "world-v3 descendant reflection-root ref",
    )
    if root_ref.get("object_kind") != "world_matrix_descendant_reflection_root_v3":
        raise ContractError(
            "world-v3 canonical completion requires the N+8 reflection root"
        )
    reflections = [
        row
        for row in objects
        if type(row) is ResolvedContentObject
        and row.ref.get("object_kind")
        == "world_matrix_descendant_reflection_root_v3"
    ]
    if len(reflections) != 1:
        raise ContractError(
            "world-v3 descendant closure requires one exact reflection root"
        )
    reflection_resolved = reflections[0]
    if dict(reflection_resolved.ref) != root_ref:
        raise ContractError(
            "world-v3 descendant reflection differs from the supplied exact ref"
        )
    reflection = validate_role_bound_object(
        reflection_resolved.ref,
        reflection_resolved.value,
    )
    reflection_id = str(reflection_resolved.ref["object_id"])
    if set(committed_generations) != {
        str(row.ref["object_id"]) for row in objects
    }:
        raise ContractError(
            "world-v3 descendant generation membership differs from its closure"
        )
    if committed_generations.get(reflection_id) != theory_generation + 8:
        raise ContractError(
            "world-v3 descendant reflection is not committed at exact N+8"
        )
    other_n8 = [
        object_id
        for object_id, generation in committed_generations.items()
        if generation == theory_generation + 8 and object_id != reflection_id
    ]
    if other_n8:
        raise ContractError(
            "world-v3 N+8 commit contains authority beyond the immutable reflection"
        )

    support_objects = tuple(row for row in objects if row is not reflection_resolved)
    support_generations = {
        object_id: generation
        for object_id, generation in committed_generations.items()
        if object_id != reflection_id
    }
    support = validate_world_v3_closure(
        support_objects,
        reflection["aggregation_root_ref"],
        theory_generation=theory_generation,
        committed_generations=support_generations,
    )
    if (
        reflection["target_id"] != support.target_id
        or reflection["run_id"] != support.run_id
        or reflection["aggregation_root_ref"] != support.aggregation_root_ref
        or reflection["reflection_disposition"]
        != "immutable_input_for_later_theory_reflection"
        or reflection["result_effect"]
        != "later_theory_cycle_reflection_input_only"
        or reflection["current_cycle_theory_mutation_authorized"] is not False
        or reflection["automatic_theory_selection_authorized"] is not False
        or reflection["proof_authorized"] is not False
        or reflection["physics_authority"] is not False
    ):
        raise ContractError(
            "world-v3 descendant reflection crosses its exact support boundary"
        )
    return VerifiedWorldV3DescendantClosure(
        support_prefix=support,
        reflection_generation=theory_generation + 8,
        result_effect="later_theory_cycle_reflection_input_only",
        current_cycle_theory_mutation_authorized=False,
        automatic_theory_selection_authorized=False,
        proof_authorized=False,
        physics_authority=False,
        _reflection_ref_data=canonical_json(dict(reflection_resolved.ref)),
    )


__all__ = [
    "PROJECTION_COMPONENT_ORDER",
    "THEORY_COMPONENT_KINDS",
    "VerifiedWorldV3Closure",
    "VerifiedWorldV3DescendantClosure",
    "WORLD_ORDER",
    "validate_world_v3_closure",
    "validate_world_v3_descendant_closure",
]
