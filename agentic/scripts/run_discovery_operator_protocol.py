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
"""Execute one central discovery operator through the dispatcher JSON protocol.

The dispatcher supplies a digest-bound request on stdin. This adapter reads the
single immutable input envelope, calls the real domain implementation, writes
exactly one declared JSON output, and returns only protocol JSON on stdout. It
does not evaluate shell text, perform live literature search, or select a theory
from a supporting experiment.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping


CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    Namespace,
    artifact_descriptor,
    canonical_digest,
    canonical_json,
    load_json,
    resolve_workspace_path,
    stable_identifier,
    verify_artifact_descriptor,
)
from agentic.discovery.hypotheses import (  # noqa: E402
    build_hidden_elicitation_prompt,
    forge_high_risk_portfolio,
    replay_proposal_field_free_high_risk_elicitation,
    run_proposal_field_free_high_risk_elicitation,
    validate_proposal_field_free_high_risk_elicitation,
)
from agentic.discovery.literature import (  # noqa: E402
    DEFAULT_LITERATURE_FRESHNESS_SECONDS,
    assimilate_derived_literature,
    assimilate_literature,
    derive_claim_mappings,
    validate_assimilation,
    validate_claim_mapping_derivation,
    validate_snapshot,
    validate_theory_object_catalog,
)
from agentic.discovery.parallel import (  # noqa: E402
    build_parallel_manifest,
    run_parallel_hypothesis_portfolio,
)
from agentic.discovery.conceptual_adjudication import (  # noqa: E402
    build_adjudication_evidence,
    validate_adjudication_evidence,
    validate_sealed_preference_authority,
)
from agentic.discovery.formal_claim_authority import (  # noqa: E402
    build_formal_claim_producer_output,
)
from agentic.discovery.workflow import build_reflective_discovery_packet  # noqa: E402
from agentic.experiments import (  # noqa: E402
    execute_experiment,
    triage_probe,
    validate_commissioned_experiment_spec,
)


REFLECTIVE_OPERATORS = {
    "reflective-conceptual-discovery": "full",
    "reflective-theory-synthesizer": "reflect",
}
SUPPORTED_OPERATORS = {
    *REFLECTIVE_OPERATORS,
    "blind-conceptual-preference-adjudicator",
    "frontier-literature-assimilator",
    "high-risk-hypothesis-forger",
    "parallel-hypothesis-portfolio",
    "dynamic-symbolic-simulation-experimenter",
    "formal-claim-producer",
}

_PROPOSAL_FIELD_FREE_SELECTION_BOUNDARY = (
    "The selected repetition is authorized only for internal conjectural exploration. "
    "It does not establish provider independence, external creativity, novelty, conceptual "
    "depth, truth, a physics result, or physics-investment authority."
)
_DEFAULT_MECHANISM_FREE_PROMPTS = (
    "Interrogate one neglected distinction in the exact target pressure. This instruction "
    "supplies no primitive, relation, mechanism, candidate answer, or evaluation score.",
    "Probe a conceptual corner where the current descriptions may fail to connect. Preserve "
    "the exact target and protected successes; no proposed explanatory structure is supplied.",
    "Ask what the target would force us to understand if familiar decompositions were "
    "temporarily suspended. Do not infer a preferred ontology or expected answer from this prompt.",
)


def _read_request() -> dict[str, Any]:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise ContractError(f"stdin is not a discovery operator request: {exc}") from exc
    if not isinstance(payload, dict):
        raise ContractError("discovery operator request must be an object")
    return payload


def _input_envelope(request: Mapping[str, Any], workspace: Path) -> dict[str, Any]:
    artifacts = request.get("input_artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != 1:
        raise ContractError("central operator protocol requires exactly one input envelope artifact")
    namespace = Namespace.from_mapping(request["identity"])
    path = verify_artifact_descriptor(artifacts[0], workspace, namespace)
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise ContractError("central operator input envelope must be a JSON object")
    return payload


def _output_path(request: Mapping[str, Any], workspace: Path) -> Path:
    outputs = request.get("declared_outputs")
    if not isinstance(outputs, list) or len(outputs) != 1:
        raise ContractError("central operator protocol requires exactly one declared output")
    if outputs[0] == request["input_artifacts"][0]["path"]:
        raise ContractError("operator output may not overwrite its frozen input")
    return resolve_workspace_path(workspace, outputs[0])


def _write_immutable(path: Path, payload: Mapping[str, Any], workspace: Path) -> None:
    encoded = canonical_json(payload) + b"\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == encoded:
            return
        raise ContractError(f"immutable operator output conflict: {path.relative_to(workspace)}")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def _without_digest(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Return a deep copy without the conventional top-level content digest."""

    return {
        key: copy.deepcopy(value)
        for key, value in payload.items()
        if key != "content_digest"
    }


def _proposal_field_free_selection(
    study: Mapping[str, Any],
    *,
    hidden_prompts: list[dict[str, Any]],
    counterbalance_seed: str,
    authored_incumbent_comparison_proposals: list[dict[str, Any]] | None,
    study_artifact: Mapping[str, Any],
) -> dict[str, Any]:
    """Materialize the one controls-gated internal-exploration selection.

    The study retains every repetition.  This smaller artifact tells the
    downstream forger exactly which sealed provider output it may consume and
    carries the replay inputs needed to reject a locally rehashed replacement.
    """

    routing = study["exploration_selection"]
    if routing["status"] != "selected_for_internal_exploration":
        raise ContractError(
            "proposal-field-free study controls did not authorize an internal selection"
        )
    selected_index = routing["selected_repetition_index"]
    if not isinstance(selected_index, int):
        raise ContractError("proposal-field-free selection lacks a repetition index")
    selected = next(
        (
            row
            for row in study["repetitions"]
            if row["repetition_index"] == selected_index
        ),
        None,
    )
    if selected is None:
        raise ContractError("proposal-field-free selection names a missing repetition")
    if (
        selected["content_digest"] != routing["selected_repetition_digest"]
        or selected["portfolio"]["content_digest"]
        != routing["selected_portfolio_digest"]
    ):
        raise ContractError("proposal-field-free routing does not bind its selected repetition")
    proposals = selected["provider_output"]["proposals"]
    selection: dict[str, Any] = {
        "schema_version": "3.0",
        "selection_id": (
            "proposal-field-free-selection."
            + canonical_digest(
                [study["study_id"], selected["content_digest"]]
            ).split(":", 1)[1][:24]
        ),
        "study_id": study["study_id"],
        "study_content_digest": study["content_digest"],
        "study_artifact": copy.deepcopy(dict(study_artifact)),
        "study_status": study["study_status"],
        "protocol_controls": {
            "repeated_diversity_status": study["repeated_diversity"]["status"],
            "known_authored_copy_controls_passed": all(
                row["authored_template_copy_control"]["status"] == "passed"
                for row in study["repetitions"]
            ),
            "selection_status": routing["status"],
            "selection_policy_digest": routing["selection_policy_digest"],
        },
        "exploration_selection": copy.deepcopy(routing),
        "selected_repetition_index": selected_index,
        "selected_schedule_slot_id": selected["schedule_slot_id"],
        # Global exact-content identity; unlike semantic_output_id it is not
        # conditioned on the schedule slot in which the deck occurred.
        "selected_semantic_content_id": selected["semantic_content_id"],
        "selected_semantic_output_id": selected["semantic_output_id"],
        # Exact compatibility alias for the former dual-identity selection.
        "selected_semantic_repetition_id": selected["semantic_repetition_id"],
        "selected_evidence_repetition_id": selected["evidence_repetition_id"],
        # Compatibility alias for pre-split selection consumers.
        "selected_repetition_id": selected["repetition_id"],
        "selected_repetition_digest": selected["content_digest"],
        "selected_portfolio_digest": selected["portfolio"]["content_digest"],
        "selected_provider_output_digest": selected["provider_output"][
            "proposal_digest"
        ],
        "selected_raw_response_digest": selected["provider_output"][
            "raw_response_digest"
        ],
        "selected_proposals_digest": canonical_digest(proposals),
        "selected_generation_provenance": copy.deepcopy(
            selected["portfolio"]["generation_provenance"]
        ),
        "eligibility": copy.deepcopy(study["eligibility"]),
        "replay_inputs": {
            "hidden_prompts": copy.deepcopy(hidden_prompts),
            "counterbalance_seed": counterbalance_seed,
            "authored_incumbent_comparison_proposals": copy.deepcopy(
                authored_incumbent_comparison_proposals
            ),
        },
        "authority": "internal_exploration_routing_only",
        "claim_boundary": _PROPOSAL_FIELD_FREE_SELECTION_BOUNDARY,
    }
    selection["content_digest"] = canonical_digest(_without_digest(selection))
    return selection


def prepare_proposal_field_free_high_risk_envelope(
    *,
    charter: Mapping[str, Any],
    literature_snapshot: Mapping[str, Any],
    workspace: Path,
    namespace: Namespace,
    assimilation_packet: Mapping[str, Any] | None = None,
    authored_incumbent_comparison_proposals: list[Mapping[str, Any]] | None = None,
    hidden_prompt_texts: tuple[str, ...] = _DEFAULT_MECHANISM_FREE_PROMPTS,
    repetitions: int = 5,
    requested_count: int = 10,
    counterbalance_seed: str = "proposal-field-free-upstream-v1",
) -> dict[str, Any]:
    """Create immutable proposal-field-free study inputs for one operator call.

    Generation and blind scoring run before the high-risk operator request is
    built.  The target-authored deck is supplied only to the equal-budget
    baseline condition.  The returned envelope contains the exact selected
    provider proposals, their provenance, and namespace-bound descriptors for
    both immutable artifacts, so the dispatcher request digest seals the whole
    causal path.
    """

    if repetitions < 5:
        raise ContractError("upstream high-risk orchestration requires at least five repetitions")
    incumbent = (
        None
        if authored_incumbent_comparison_proposals is None
        else [copy.deepcopy(dict(row)) for row in authored_incumbent_comparison_proposals]
    )
    prompts = [
        build_hidden_elicitation_prompt(
            prompt_id=f"mechanism-free-{index}",
            target_id=str(charter["target_id"]),
            theory_state_digest=str(charter["theory_state_digest"]),
            literature_snapshot_digest=str(literature_snapshot["content_digest"]),
            prompt_text=text,
        )
        for index, text in enumerate(hidden_prompt_texts)
    ]
    study = run_proposal_field_free_high_risk_elicitation(
        charter,
        literature_snapshot,
        hidden_prompts=prompts,
        repetitions=repetitions,
        requested_count=requested_count,
        counterbalance_seed=counterbalance_seed,
        authored_incumbent_comparison_proposals=incumbent,
    )
    validate_proposal_field_free_high_risk_elicitation(
        study,
        charter=charter,
        literature_snapshot=literature_snapshot,
        hidden_prompts=prompts,
        counterbalance_seed=counterbalance_seed,
        authored_incumbent_comparison_proposals=incumbent,
    )
    replay = replay_proposal_field_free_high_risk_elicitation(
        study,
        charter,
        literature_snapshot,
        hidden_prompts=prompts,
        counterbalance_seed=counterbalance_seed,
        authored_incumbent_comparison_proposals=incumbent,
    )
    if not replay["same_seed_exact_replay"]:
        raise ContractError("proposal-field-free study did not replay exactly")
    artifact_root = (
        workspace
        / "operator-studies"
        / f"{study['study_id']}.{study['content_digest'].split(':', 1)[1][:16]}"
    )
    study_path = artifact_root / "study.json"
    selection_path = artifact_root / "selection.json"
    _write_immutable(study_path, study, workspace)
    study_binding = artifact_descriptor(study_path, workspace, namespace)
    selection = _proposal_field_free_selection(
        study,
        hidden_prompts=prompts,
        counterbalance_seed=counterbalance_seed,
        authored_incumbent_comparison_proposals=incumbent,
        study_artifact=study_binding,
    )
    _write_immutable(selection_path, selection, workspace)
    selected = study["repetitions"][selection["selected_repetition_index"]]
    envelope: dict[str, Any] = {
        "charter": copy.deepcopy(dict(charter)),
        "literature_snapshot": copy.deepcopy(dict(literature_snapshot)),
        "selected_proposals": copy.deepcopy(
            selected["provider_output"]["proposals"]
        ),
        "generation_provenance": copy.deepcopy(
            selected["portfolio"]["generation_provenance"]
        ),
        "selected_portfolio": copy.deepcopy(selected["portfolio"]),
        "proposal_field_free_upstream": {
            "study_artifact": study_binding,
            "selection_artifact": artifact_descriptor(
                selection_path, workspace, namespace
            ),
        },
    }
    if assimilation_packet is not None:
        envelope["assimilation_packet"] = copy.deepcopy(dict(assimilation_packet))
    return envelope


def _validated_proposal_field_free_inputs(
    request: Mapping[str, Any],
    envelope: Mapping[str, Any],
    *,
    workspace: Path,
    charter: Mapping[str, Any],
    snapshot: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]] | None:
    """Replay the upstream study and return only its controls-selected deck."""

    bundle = envelope.get("proposal_field_free_upstream")
    present = {
        "bundle": bundle is not None,
        "selected_proposals": "selected_proposals" in envelope,
        "generation_provenance": "generation_provenance" in envelope,
        "selected_portfolio": "selected_portfolio" in envelope,
    }
    if not any(present.values()):
        if "proposals" in envelope:
            raise ContractError(
                "direct proposal fields are not accepted; supply a proposal-field-free upstream bundle"
            )
        return None
    if not all(present.values()) or not isinstance(bundle, Mapping):
        raise ContractError("proposal-field-free upstream inputs must be supplied as one complete bundle")
    if set(bundle) != {"study_artifact", "selection_artifact"}:
        raise ContractError("proposal-field-free upstream binding has an invalid strict shape")
    namespace = Namespace.from_mapping(request["identity"])
    study_path = verify_artifact_descriptor(
        bundle["study_artifact"], workspace, namespace
    )
    selection_path = verify_artifact_descriptor(
        bundle["selection_artifact"], workspace, namespace
    )
    study = load_json(study_path)
    selection = load_json(selection_path)
    if not isinstance(study, Mapping) or not isinstance(selection, Mapping):
        raise ContractError("proposal-field-free study and selection must be JSON objects")
    if selection.get("study_artifact") != bundle["study_artifact"]:
        raise ContractError("proposal-field-free selection does not bind the exact study artifact")
    if selection.get("content_digest") != canonical_digest(
        _without_digest(selection)
    ):
        raise ContractError("proposal-field-free selection content digest mismatch")
    replay_inputs = selection.get("replay_inputs")
    if not isinstance(replay_inputs, Mapping) or set(replay_inputs) != {
        "hidden_prompts",
        "counterbalance_seed",
        "authored_incumbent_comparison_proposals",
    }:
        raise ContractError("proposal-field-free selection replay inputs have an invalid strict shape")
    prompts = replay_inputs["hidden_prompts"]
    incumbent = replay_inputs["authored_incumbent_comparison_proposals"]
    if not isinstance(prompts, list) or (
        incumbent is not None and not isinstance(incumbent, list)
    ):
        raise ContractError("proposal-field-free replay inputs have invalid collection types")
    validate_proposal_field_free_high_risk_elicitation(
        study,
        charter=charter,
        literature_snapshot=snapshot,
        hidden_prompts=prompts,
        counterbalance_seed=str(replay_inputs["counterbalance_seed"]),
        authored_incumbent_comparison_proposals=incumbent,
    )
    replay = replay_proposal_field_free_high_risk_elicitation(
        study,
        charter,
        snapshot,
        hidden_prompts=prompts,
        counterbalance_seed=str(replay_inputs["counterbalance_seed"]),
        authored_incumbent_comparison_proposals=incumbent,
    )
    if not replay["same_seed_exact_replay"]:
        raise ContractError("proposal-field-free upstream study failed exact callback replay")
    expected_selection = _proposal_field_free_selection(
        study,
        hidden_prompts=[copy.deepcopy(dict(row)) for row in prompts],
        counterbalance_seed=str(replay_inputs["counterbalance_seed"]),
        authored_incumbent_comparison_proposals=(
            None
            if incumbent is None
            else [copy.deepcopy(dict(row)) for row in incumbent]
        ),
        study_artifact=bundle["study_artifact"],
    )
    if dict(selection) != expected_selection:
        raise ContractError("proposal-field-free selection differs from the replayed study controls")
    selected = study["repetitions"][selection["selected_repetition_index"]]
    proposals = envelope["selected_proposals"]
    provenance = envelope["generation_provenance"]
    if not isinstance(proposals, list) or not isinstance(provenance, Mapping):
        raise ContractError("selected proposals and generation provenance have invalid types")
    if proposals != selected["provider_output"]["proposals"]:
        raise ContractError("operator proposals differ from the controls-selected provider output")
    if dict(provenance) != selected["portfolio"]["generation_provenance"]:
        raise ContractError("operator generation provenance differs from the selected repetition")
    if envelope["selected_portfolio"] != selected["portfolio"]:
        raise ContractError("operator selected portfolio differs from the recursively sealed selection")
    return [copy.deepcopy(dict(row)) for row in proposals], copy.deepcopy(
        dict(provenance)
    )


def _reflective(
    operator_id: str, request: Mapping[str, Any], envelope: Mapping[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    expected_stage = REFLECTIVE_OPERATORS[operator_id]
    stage = str(request.get("parameters", {}).get("stage", expected_stage))
    if stage != expected_stage:
        raise ContractError(f"{operator_id} requires stage={expected_stage!r}")
    working = copy.deepcopy(dict(envelope))
    if operator_id == "reflective-theory-synthesizer":
        previous = working.get("previous_evidence")
        revised = working.pop("revise_after_adjudication", False)
        if not isinstance(revised, bool):
            raise ContractError("revise_after_adjudication must be an explicit boolean")
        if revised:
            from agentic.discovery.reflection import validate_synthesis_revision
            validate_synthesis_revision(working)
            # A parent's sealed assessment is a reason to revise, not current
            # authority over changed systems. A new panel must assess the result.
            working.pop("conceptual_adjudication_evidence", None)
        if previous is not None:
            if not isinstance(previous, Mapping):
                raise ContractError(
                    "reflective synthesis previous_evidence must be a complete object"
                )
            if not revised:
                working["conceptual_adjudication_evidence"] = copy.deepcopy(dict(previous))
        probe_flag = working.pop("request_theory_support_probe", False)
        if not isinstance(probe_flag, bool):
            raise ContractError(
                "request_theory_support_probe must be an explicit boolean"
            )
        if probe_flag:
            if revised:
                raise ContractError("revised synthesis needs fresh adjudication before commissioning support")
            if previous is None:
                raise ContractError(
                    "a theory support proposal requires sealed parent adjudication"
                )
            preview = build_reflective_discovery_packet(working)
            preferred_ids = list(
                preview["provisional_synthesis"]["preferred_system_ids"]
            )
            if not preferred_ids:
                raise ContractError(
                    "a theory support proposal requires a nonempty sealed preference set"
                )
            systems_by_id = {
                str(row["system_id"]): row
                for row in preview["conceptual_systems"]
            }
            correction_conditions = [
                str(condition)
                for system_id in preferred_ids
                for condition in systems_by_id[system_id].get(
                    "correction_conditions", []
                )
                if str(condition).strip()
            ]
            if not correction_conditions:
                raise ContractError(
                    "a theory support proposal requires an explicit correction condition"
                )
            question = (
                "Does the preferred programme survive its declared correction "
                f"condition: {correction_conditions[0]}"
            )
            question_id = stable_identifier(
                "theory-support-question",
                preview["theoretical_programme"]["programme_id"],
                preferred_ids,
                correction_conditions[0],
            )
            working["support_probe"] = {
                "disposition": "proposed",
                "theory_programme_id": preview["theoretical_programme"][
                    "programme_id"
                ],
                "theoretical_question_id": question_id,
                "conceptual_system_ids": preferred_ids,
                "theoretical_question": question,
                "role": "symbolic_derivation",
                "why_theory_alone_is_currently_insufficient": (
                    "The preferred programme declares a finite correction condition "
                    "whose failure can localize a premise without selecting a theory."
                ),
                "possible_theory_updates": [
                    "If the registered condition fails, request reflective revision "
                    "of that premise only."
                ],
                "receipt_ids": [],
                "reflective_assimilation_event_ids": [],
            }
            working["next_reflective_action"] = {
                "kind": "probe",
                "question": question,
                "expected_conceptual_change": (
                    "Localize whether the declared correction condition requires "
                    "a later reflective premise revision."
                ),
            }
    packet = build_reflective_discovery_packet(working)
    if operator_id == "reflective-theory-synthesizer" and revised:
        packet["parent_adjudication_evidence"] = copy.deepcopy(dict(previous))
        packet["packet_digest"] = canonical_digest({key: value for key, value in packet.items() if key != "packet_digest"})
    return packet, list(packet.get("explicit_unknowns", []))


def _previous_adjudication_evidence(
    envelope: Mapping[str, Any],
) -> Mapping[str, Any] | None:
    """Resolve prior authority from its complete sealed object, never an ID alone.

    A synthesis-stage adjudication must replay the earlier panel and blind packet,
    so a caller-provided digest cannot stand in for the prior bytes.  The optional
    descriptor digest is only a consistency check over the embedded evidence;
    the adjudication builder performs the full recursive validation.
    """

    previous = envelope.get("previous_evidence")
    declared_digest = envelope.get("previous_evidence_digest")
    if previous is None:
        if declared_digest is not None:
            raise ContractError(
                "conceptual adjudicator cannot consume a previous-evidence digest without the full sealed evidence"
            )
        return None
    if not isinstance(previous, Mapping):
        raise ContractError("previous conceptual adjudication evidence must be an object")
    embedded_digest = previous.get("evidence_digest")
    if not isinstance(embedded_digest, str) or not embedded_digest:
        raise ContractError("previous conceptual adjudication evidence lacks its evidence digest")
    if declared_digest is not None and declared_digest != embedded_digest:
        raise ContractError(
            "previous conceptual adjudication descriptor digest differs from the embedded sealed evidence"
        )
    return previous


def _conceptual_adjudication(
    request: Mapping[str, Any], envelope: Mapping[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    """Build the sole sealed, set-valued conceptual preference authority."""

    identity = request["identity"]
    packet = envelope.get("blind_packet")
    reports = envelope.get("judge_reports")
    systems = envelope.get("systems")
    rounds = envelope.get("reflection_rounds")
    genealogy = envelope.get("frozen_genealogy")
    if not isinstance(packet, Mapping) or not isinstance(reports, list):
        raise ContractError("conceptual adjudicator requires a blind packet and judge reports")
    if not isinstance(systems, list) or not isinstance(rounds, list) or not isinstance(genealogy, list):
        raise ContractError(
            "conceptual adjudicator requires exact systems, reflection rounds, and frozen genealogy"
        )
    context = {
        "systems": systems,
        "reflection_rounds": rounds,
        "frozen_genealogy": genealogy,
        "candidate_bindings": envelope.get("candidate_bindings"),
        "theory_state_digest": envelope.get("theory_state_digest"),
        "literature_snapshot_digest": envelope.get("literature_snapshot_digest"),
        "high_risk_portfolio_digest": envelope.get("high_risk_portfolio_digest"),
        "proposer_receipt_ids": envelope.get("proposer_receipt_ids"),
        "previous_evidence": _previous_adjudication_evidence(envelope),
    }
    if not isinstance(context["candidate_bindings"], Mapping):
        raise ContractError("conceptual adjudicator requires the private alias-to-system binding")
    evidence = build_adjudication_evidence(
        packet=packet,
        reports=reports,
        run_id=str(identity["run_id"]),
        state_version=int(identity["state_version"]),
        created_at=str(envelope["created_at"]),
        **context,
    )
    validate_adjudication_evidence(evidence, **context)
    validate_sealed_preference_authority(
        evidence,
        target_id=str(identity["target_id"]),
        run_id=str(identity["run_id"]),
        state_version=int(identity["state_version"]),
        stage_id=str(packet["stage_id"]),
        system_ids=[str(row["system_id"]) for row in systems],
        systems=systems,
        reflection_rounds=rounds,
    )
    return evidence, [
        "The sealed preference is internal conceptual adjudication, not proof, external validation, or an established physics result."
    ]


def _literature(
    request: Mapping[str, Any], envelope: Mapping[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    snapshot = envelope.get("snapshot")
    if not isinstance(snapshot, Mapping):
        raise ContractError("literature assimilation envelope requires a frozen snapshot")
    validate_snapshot(snapshot)
    if snapshot["target_id"] != request["identity"]["target_id"]:
        raise ContractError("literature snapshot target differs from request target")
    theory_catalog = envelope.get("theory_catalog")
    bound_derivation = envelope.get("mapping_derivation")
    if theory_catalog is not None:
        if not isinstance(theory_catalog, Mapping):
            raise ContractError("theory_catalog must be an object")
        if "theory_mappings" in envelope:
            raise ContractError("derived literature mode cannot also supply manual theory_mappings")
        validate_theory_object_catalog(theory_catalog)
        if bound_derivation is None:
            bound_derivation = derive_claim_mappings(
                snapshot, theory_catalog=theory_catalog
            )
        elif not isinstance(bound_derivation, Mapping):
            raise ContractError("mapping_derivation must be an object")
        else:
            validate_claim_mapping_derivation(
                bound_derivation,
                snapshot=snapshot,
                theory_catalog=theory_catalog,
            )
        packet = assimilate_derived_literature(
            snapshot,
            theory_catalog=theory_catalog,
            mapping_derivation=bound_derivation,
            hypotheses=envelope.get("hypotheses", []),
            prior_snapshot=envelope.get("prior_snapshot"),
            candidate_snapshot_ids=envelope.get("candidate_snapshot_ids", []),
            freshness_max_age_seconds=envelope.get(
                "freshness_max_age_seconds",
                DEFAULT_LITERATURE_FRESHNESS_SECONDS,
            ),
            freshness_evaluated_at=envelope.get("freshness_evaluated_at"),
        )
    else:
        if bound_derivation is not None:
            raise ContractError("mapping_derivation requires its exact theory_catalog")
        if "theory_mappings" not in envelope:
            raise ContractError(
                "literature envelope requires legacy theory_mappings or a theory_catalog"
            )
        packet = assimilate_literature(
            snapshot,
            theory_state_digest=snapshot["theory_state_digest"],
            theory_mappings=envelope["theory_mappings"],
            hypotheses=envelope.get("hypotheses", []),
            prior_snapshot=envelope.get("prior_snapshot"),
            candidate_snapshot_ids=envelope.get("candidate_snapshot_ids", []),
            freshness_max_age_seconds=envelope.get(
                "freshness_max_age_seconds",
                DEFAULT_LITERATURE_FRESHNESS_SECONDS,
            ),
            freshness_evaluated_at=envelope.get("freshness_evaluated_at"),
        )
    validate_assimilation(packet, snapshot=snapshot)
    unknowns = list(packet["explicit_unknowns"])
    if snapshot["provenance_mode"] == "local_only":
        unknowns.append(
            "Static literature input was not a live search and cannot establish recency or novelty."
        )
    else:
        unknowns.append(
            "The frozen live-search receipts establish bounded search recency, not exhaustive coverage, source correctness, or novelty."
        )
    return packet, sorted(set(unknowns))


def _high_risk(
    request: Mapping[str, Any], envelope: Mapping[str, Any], workspace: Path
) -> tuple[dict[str, Any], list[str]]:
    charter = envelope.get("charter")
    snapshot = envelope.get("literature_snapshot")
    if not isinstance(charter, Mapping) or not isinstance(snapshot, Mapping):
        raise ContractError("hypothesis envelope requires charter and literature_snapshot objects")
    if charter.get("target_id") != request["identity"]["target_id"]:
        raise ContractError("hypothesis charter target differs from request target")
    assimilation = envelope.get("assimilation_packet")
    if assimilation is not None:
        if not isinstance(assimilation, Mapping):
            raise ContractError("assimilation_packet must be an object")
        validate_assimilation(assimilation, snapshot=snapshot)
    parameters = request.get("parameters", {})
    upstream = _validated_proposal_field_free_inputs(
        request,
        envelope,
        workspace=workspace,
        charter=charter,
        snapshot=snapshot,
    )
    proposals, generation_provenance = upstream or (None, None)
    authored = envelope.get("authored_proposals")
    if authored is not None:
        if upstream is not None:
            raise ContractError("authored proposals cannot also claim proposal-field-free study authority")
        if not isinstance(authored, list) or not all(isinstance(row, Mapping) for row in authored):
            raise ContractError("authored_proposals must be a list of conjecture objects")
        # The immutable input envelope binds actual authored content. Provenance
        # remains the source forger's supplied-proposal mode; a model call does
        # not establish proposal-field-free creativity or independent merit.
        proposals = authored
    requested_count = int(parameters.get("requested_count", 10))
    relevance_floor = float(parameters.get("relevance_floor", 0.70))
    if upstream is not None and relevance_floor != 0.70:
        raise ContractError(
            "proposal-field-free study portfolios require the sealed relevance floor 0.70"
        )
    packet = forge_high_risk_portfolio(
        charter,
        snapshot,
        proposals=proposals,
        requested_count=requested_count,
        relevance_floor=relevance_floor,
        generation_provenance=generation_provenance,
    )
    if upstream is not None:
        selection = load_json(
            verify_artifact_descriptor(
                envelope["proposal_field_free_upstream"]["selection_artifact"],
                workspace,
                Namespace.from_mapping(request["identity"]),
            )
        )
        study = load_json(
            verify_artifact_descriptor(
                envelope["proposal_field_free_upstream"]["study_artifact"],
                workspace,
                Namespace.from_mapping(request["identity"]),
            )
        )
        selected = study["repetitions"][selection["selected_repetition_index"]]
        if packet != selected["portfolio"]:
            raise ContractError(
                "operator portfolio differs from the exact controls-selected study portfolio"
            )
        return packet, [
            "Every hypothesis remains conjectural; structural risk and value are not evidence of truth.",
            _PROPOSAL_FIELD_FREE_SELECTION_BOUNDARY,
        ]
    return packet, [
        "Every hypothesis remains conjectural; structural risk and value are not evidence of truth.",
        "No proposal-field-free upstream study was supplied; authored proposals or fallback templates cannot support a proposal-field-free generation claim.",
    ]


def _parallel_worker(
    envelope: Mapping[str, Any], branch_id: str, request: Mapping[str, Any]
) -> dict[str, Any]:
    failures = {str(item) for item in envelope.get("failure_branch_ids", [])}
    if branch_id in failures:
        raise RuntimeError("fixture-configured branch-local failure")
    configured = envelope.get("worker_outputs", {}).get(branch_id)
    if isinstance(configured, Mapping):
        return dict(configured)
    dissent = branch_id in {str(item) for item in envelope.get("dissent_branch_ids", [])}
    return {
        "theory_delta": {
            "delta_class": "conceptual_deepening",
            "mechanism_key": f"matured-{request['mechanism_key']}",
            "changed_question": (
                "Which explicit mediator and correction condition would make "
                f"this branch answer: {request['maturation_question']}"
            ),
            "new_explanatory_dependencies": [
                {
                    "source": request["mechanism_key"],
                    "relation": "must_be_mediated_by",
                    "target": request["unique_primitives"][0],
                }
            ],
            "new_distinctions": [
                {
                    "name": f"{request['mechanism_key']}-carrier-vs-target",
                    "left": "branch-specific explanatory carrier",
                    "right": "the target conclusion it is intended to explain",
                    "preservation_condition": "the carrier must be testable without assuming the target",
                }
            ],
        },
        "claims": [
            {
                "proposition": "The target may require the branch-specific explanatory carrier.",
                "stance": "oppose" if dissent else "support",
            }
        ],
        "genealogy": [request["hypothesis_id"]],
        "conceptual_learning": True,
        "is_dissent": dissent,
    }


def _parallel(
    request: Mapping[str, Any], envelope: Mapping[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    portfolio = envelope.get("high_risk_portfolio")
    if not isinstance(portfolio, Mapping):
        raise ContractError("parallel envelope requires high_risk_portfolio")
    if portfolio.get("target_id") != request["identity"]["target_id"]:
        raise ContractError("parallel portfolio target differs from request target")
    hypotheses = {
        str(item.get("hypothesis_id")): item
        for item in portfolio.get("hypotheses", [])
        if isinstance(item, Mapping)
    }
    selected_seeds = envelope.get("branch_seeds") or portfolio.get(
        "parallel_branch_seeds", []
    )
    for seed in selected_seeds:
        candidate = hypotheses.get(str(seed.get("hypothesis_id")))
        rebase = candidate.get("literature_rebase_receipt", {}) if candidate else {}
        if (
            not candidate
            or candidate.get("concept_lifecycle_state") != "literature_rebased"
            or rebase.get("status") != "completed"
        ):
            raise ContractError(
                "parallel maturation requires a completed, non-local literature rebase for every seed"
            )
    manifest = build_parallel_manifest(
        portfolio,
        base_theory_state_version=request["identity"]["state_version"],
        branch_seeds=envelope.get("branch_seeds"),
        dependencies=envelope.get("dependencies"),
        resource_budget=envelope.get("resource_budget"),
    )

    def worker(branch_request: Mapping[str, Any]) -> dict[str, Any]:
        return _parallel_worker(envelope, str(branch_request["branch_id"]), branch_request)

    def conservative_control(branch_request: Mapping[str, Any]) -> dict[str, Any]:
        """Spend the same opportunity budget on a non-inventive local continuation."""

        return {
            "theory_delta": {
                "delta_class": "conservative_local_continuation",
                "changed_question": (
                    "Which existing local estimate can be tightened without introducing "
                    f"a new primitive for {branch_request['mechanism_key']}?"
                ),
            },
            "claims": [],
            "genealogy": [branch_request["hypothesis_id"]],
            "conceptual_learning": False,
        }

    packet = run_parallel_hypothesis_portfolio(
        manifest,
        worker,
        matched_budget_control_worker=conservative_control,
    )
    unknowns = [
        "Parallel structural candidates do not establish conceptual learning, any branch claim, or a shared-state write.",
        "The executed conservative control supports only a matched-opportunity scheduler comparison, not discovery efficacy."
    ]
    if packet["partial_failure_ledger"]["retry_branch_ids"]:
        unknowns.append("One or more branch-local attempts remain retryable.")
    return packet, unknowns


def _experiment(
    request: Mapping[str, Any], envelope: Mapping[str, Any], output: Path
) -> tuple[dict[str, Any], list[str]]:
    if request.get("parameters", {}).get("theory_commissioned") is not True:
        raise ContractError("support experiment requires an explicit theory_commissioned parameter")
    triage_request = envelope.get("triage_request")
    experiment_request = envelope.get("experiment_request")
    commissioned_spec = envelope.get("experiment_spec")
    if (
        not isinstance(triage_request, Mapping)
        or not isinstance(experiment_request, Mapping)
        or not isinstance(commissioned_spec, Mapping)
    ):
        raise ContractError(
            "experiment envelope requires triage_request, experiment_request, and experiment_spec"
        )
    identity = request["identity"]
    if (
        triage_request.get("target_id") != identity["target_id"]
        or int(triage_request.get("state_version", -1)) != identity["state_version"]
        or experiment_request.get("run_id") != identity["run_id"]
        or experiment_request.get("branch_id") != identity["branch_id"]
    ):
        raise ContractError("experiment commission identity differs from dispatcher namespace")
    triage = triage_probe(triage_request)
    if triage["decision"] != "commission":
        raise ContractError(
            "uncommissioned or immature probes must be represented as a justified dispatcher skip"
        )
    spec = validate_commissioned_experiment_spec(
        triage_request,
        experiment_request,
        commissioned_spec,
    )
    runtime_root = output.parent / "operator-runtime" / request["request_id"]
    receipt = execute_experiment(spec, runtime_root)
    return receipt, [
        "The result is model-scoped support only and must return to reflective theory assessment."
    ]


def execute(
    operator_id: str,
    request: Mapping[str, Any],
    envelope: Mapping[str, Any],
    output: Path,
    workspace: Path,
) -> tuple[dict[str, Any], list[str]]:
    if operator_id in REFLECTIVE_OPERATORS:
        return _reflective(operator_id, request, envelope)
    if operator_id == "blind-conceptual-preference-adjudicator":
        return _conceptual_adjudication(request, envelope)
    if operator_id == "frontier-literature-assimilator":
        return _literature(request, envelope)
    if operator_id == "high-risk-hypothesis-forger":
        return _high_risk(request, envelope, workspace)
    if operator_id == "parallel-hypothesis-portfolio":
        return _parallel(request, envelope)
    if operator_id == "dynamic-symbolic-simulation-experimenter":
        return _experiment(request, envelope, output)
    if operator_id == "formal-claim-producer":
        identity = request["identity"]
        if (
            envelope.get("target_id") != identity["target_id"]
            or envelope.get("run_id") != identity["run_id"]
            or envelope.get("branch_id") != identity["branch_id"]
            or envelope.get("source_theory_generation")
            != identity["state_version"] + 1
        ):
            raise ContractError(
                "formal-claim producer input crossed its dispatcher namespace"
            )
        return build_formal_claim_producer_output(
            envelope,
            workspace=workspace,
        ), [
            "Formal-claim production establishes only registered provenance for a typed claim-and-plan packet; it does not establish truth, proof success, theorem status, theory preference, or physics value."
        ]
    raise ContractError(f"unsupported central discovery operator: {operator_id}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operator-id", choices=sorted(SUPPORTED_OPERATORS), required=True)
    parser.add_argument("--workspace", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    try:
        workspace = args.workspace.resolve()
        request = _read_request()
        if request.get("operator", {}).get("operator_id") != args.operator_id:
            raise ContractError("argv operator ID differs from the digest-bound request")
        envelope = _input_envelope(request, workspace)
        output = _output_path(request, workspace)
        packet, unknowns = execute(
            args.operator_id, request, envelope, output, workspace
        )
        _write_immutable(output, packet, workspace)
        print(
            json.dumps(
                {
                    "artifacts": [{"path": output.relative_to(workspace).as_posix()}],
                    "explicit_unknowns": unknowns,
                },
                sort_keys=True,
            )
        )
        return 0
    except (ContractError, KeyError, TypeError, ValueError, OSError) as exc:
        diagnostic = " ".join(str(exc).split())
        if len(diagnostic) > 4096:
            diagnostic = diagnostic[:4080] + "...[truncated]"
        print(f"operator protocol rejected: {diagnostic}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
