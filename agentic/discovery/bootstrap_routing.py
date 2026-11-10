# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Execute the original two-phase source policy for freshly acquired literature.

The acquisition is reopened first, policy is sealed before mapping, and actual
stage intervals are recorded around each producer invocation. Abstract-only
sources can create questions or explicit no-change records. They cannot become
positive support for a theorem, even if a model finds them persuasive.
"""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Callable, Mapping

from .bootstrap_literature import reopen_acquisition
from .contracts import ContractError, bytes_digest, canonical_digest, stable_identifier, utc_now
from .literature import assimilate_literature, validate_assimilation
from .literature_acquisition import (
    build_source_routing_pre_map_policy, validate_source_routing_pre_map_policy,
    build_source_routing_warrant_validation_packet, validate_source_routing_warrant_validation_packet,
    build_source_routing_realization, validate_source_routing_realization,
    validate_source_routing_consumption, source_routing_realization_requirements,
)
from .model_author import read_record, write_record


BOUNDARY = (
    "Actual bounded HTTP metadata observations, validated local source projections and "
    "internally correlated model relevance assessment only; no provider authentication, "
    "source truth, full-text verification, exhaustive coverage or positive theorem support."
)
ALGORITHMS = (
    ("warrant_validation", "agentic.discovery.literature_acquisition.build_source_routing_warrant_validation_packet"),
    ("claim_mapping", "agentic.discovery.bootstrap_routing.assessment_mappings"),
    ("assimilation", "agentic.discovery.literature.assimilate_literature"),
)


def algorithm_contracts() -> list[dict[str, Any]]:
    """Bind the fixed local routing registry and its current implementation bytes."""
    code_root = Path(__file__).resolve().parent
    dependencies = {name: bytes_digest((code_root / name).read_bytes()) for name in (
        "bootstrap_routing.py", "literature.py", "literature_acquisition.py", "contracts.py")}
    return [{"stage": stage, "component_id": "bootstrap-source-" + stage,
             "algorithm_id": symbol, "config_id": "abstracts-question-only.v1",
             "config_digest": canonical_digest({"registry": ALGORITHMS, "dependencies": dependencies,
                                                "positive_support": False, "mapping_policy": "question_or_no_change"}),
             "authority_class": "local_bootstrap_algorithm_registry"} for stage, symbol in ALGORITHMS]


def assessment_mappings(snapshot: Mapping[str, Any], assessment: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Project assessed abstracts into questions while retaining every noisy hit."""
    values = assessment["value"]["assessments"]
    sources = {row["source_id"]: row for row in snapshot["sources"]}
    if sorted(row["source_id"] for row in values) != sorted(sources):
        raise ContractError("source mapping assessment does not cover the exact acquired set")
    mappings = []
    for row in values:
        source = sources[row["source_id"]]
        if row["claims_verified"] is not False:
            raise ContractError("abstract assessment cannot certify source claims")
        if not any(row["source_excerpt"] in text for text in [source["title"], *source["claims"]]):
            raise ContractError("mapping assessment lacks an exact acquired excerpt")
        event = "new_question" if row["relevance"] in {"direct", "adjacent"} else "justified_no_change"
        theory_ids = [snapshot["target_id"]]
        mappings.append({"mapping_id": stable_identifier("source-theory-map", snapshot["content_digest"],
                source["source_id"], theory_ids, event),
            "source_id": source["source_id"], "theory_object_ids": theory_ids, "object_kinds": ["proof_obligation"],
            "relation": "leaves_open", "exact_claim": row["source_excerpt"],
            "source_limitation": " ".join([*source["limitations"], *row["credibility_concerns"]]),
            "conceptual_change": row["reason"] + " " + " ".join(row["usable_for"]),
            "event_type": event, "coverage_limits": list(snapshot["coverage_limits"]), "confidence": "low"})
    return mappings


def execute_source_routing(*, acquisition_root: Path, acquisition_digest: str,
                           target_id: str, run_id: str, theory_state_digest: str,
                           assessment: Mapping[str, Any], root: Path,
                           state_version: int = 0,
                           publish_policy: Callable | None = None,
                           assimilation_operator: Callable | None = None,
                           production_ledger=None) -> dict[str, Any]:
    """Perform and seal source routing, optionally through canonical dispatch hooks."""
    identity = {"target_id": target_id, "run_id": run_id, "state_version": state_version}
    root.mkdir(parents=True, exist_ok=False)
    started = utc_now()
    acquisition = read_record(acquisition_root / "acquisition.json")
    def reopen():
        return reopen_acquisition(acquisition_root, expected_digest=acquisition_digest,
            target_id=target_id, run_id=run_id, theory_state_digest=theory_state_digest)
    snapshot = (production_ledger.run("acquisition_reopen", {
        "exact_source_bundle": production_ledger.source_bundle, "acquisition": acquisition}, reopen)
        if production_ledger else reopen())
    completed = utc_now()
    acquisition_receipt = {"receipt_id": stable_identifier("acquisition-reopen", acquisition_digest, identity, started),
        "status": "succeeded", "identity": identity, "started_at": started, "completed_at": completed,
        "input_digest": acquisition_digest, "output_digest": snapshot["content_digest"]}
    write_record(root / "acquisition-reopen.json", acquisition_receipt)
    authority = {"capture_content_digest": acquisition_digest,
        "acquisition_content_digest": snapshot["content_digest"],
        "tool_response_content_digests": sorted({"sha256:" + row["response"]["sha256"] for row in acquisition["captures"]}),
        "version_graph_content_digests": [], "source_ids": sorted(row["source_id"] for row in snapshot["sources"]),
        "source_routing_eligibility": {row["source_id"]: "unverified_audit_only" for row in snapshot["sources"]},
        "authority_boundary": BOUNDARY}
    algorithms = algorithm_contracts()
    policy_args = {"authority": authority, "snapshot": snapshot, **identity,
                   "acquisition_producer_receipt": acquisition_receipt, "algorithm_contracts": algorithms}
    def make_policy():
        value = build_source_routing_pre_map_policy(**policy_args, sealed_at=utc_now())
        return validate_source_routing_pre_map_policy(value,
            **{key: value for key, value in policy_args.items() if key not in identity})
    policy = (production_ledger.run("source_pre_map_policy", policy_args, make_policy)
              if production_ledger else make_policy())
    write_record(root / "pre-map-policy.json", policy)
    if publish_policy:
        publish_policy(policy)
    contracts = {row["stage"]: row for row in policy["algorithm_contracts"]}
    intervals = {}
    # Freeze the inputs of each operation before execution, including the
    # externally authored assessment as data for the fixed question-only map.
    def stage(name, inputs, producer, validator):
        request = {"stage": name, "identity": identity, "pre_map_policy_digest": policy["policy_digest"],
                   "algorithm_contract_digest": contracts[name]["contract_digest"],
                   "started_at": utc_now(), "inputs": inputs}
        write_record(root / (name + "-request.json"), request)
        def execute():
            output = producer()
            validator(output)
            return {"theory_mappings": output} if name == "claim_mapping" else output
        output = (production_ledger.run(name, {"source_pre_map_policy": policy, **inputs}, execute)
                  if production_ledger else execute())
        if name == "claim_mapping":
            output = output["theory_mappings"]
        intervals[name] = (request["started_at"], utc_now())
        write_record(root / (name + "-output.json"), {"value": output})
        return output
    warrants = stage("warrant_validation", {"snapshot_digest": snapshot["content_digest"]},
        lambda: build_source_routing_warrant_validation_packet(policy=policy, snapshot=snapshot),
        lambda output: validate_source_routing_warrant_validation_packet(output, policy=policy, snapshot=snapshot))
    mappings = stage("claim_mapping", {"assessment": assessment, "warrant_digest": warrants["packet_digest"]},
        lambda: assessment_mappings(snapshot, assessment),
        lambda output: validate_source_routing_consumption(authority=authority, sources=snapshot["sources"],
            stage="claim_mapping", theory_mappings=output, semantic_warrants=warrants["validated_warrants"], require_complete_mapping=True))
    assimilation = stage("assimilation", {"mappings": mappings, "warrant_digest": warrants["packet_digest"]},
        lambda: assimilation_operator(snapshot, mappings, policy) if assimilation_operator else assimilate_literature(
            snapshot, theory_state_digest=theory_state_digest, theory_mappings=mappings),
        lambda output: validate_assimilation(output, snapshot=snapshot))
    if assimilation["theory_mappings"] != mappings:
        raise ContractError("assimilation changed the question-only source map")
    requirements = source_routing_realization_requirements(policy=policy, snapshot=snapshot,
        validated_warrants=warrants["validated_warrants"], claim_mappings=mappings, assimilation=assimilation)
    receipts = []
    for row in requirements:
        stage_id = row["stage"]
        first, last = intervals[stage_id]
        receipt = {**row, "receipt_id": stable_identifier("source-stage", identity, row, first, last),
                   "status": "succeeded", "identity": identity,
                   "pre_map_policy_id": policy["policy_id"], "pre_map_policy_digest": policy["policy_digest"],
                   "started_at": first, "completed_at": last}
        write_record(root / (stage_id + "-receipt.json"), receipt)
        receipts.append(receipt)
    realization_args = {"policy": policy, "authority": authority, "snapshot": snapshot,
        "acquisition_producer_receipt": acquisition_receipt, "algorithm_contracts": algorithms,
        "validated_warrants": warrants["validated_warrants"], "claim_mappings": mappings,
        "assimilation": assimilation, "stage_receipts": receipts}
    def make_realization():
        value = build_source_routing_realization(**realization_args, completed_at=utc_now())
        return validate_source_routing_realization(value, **realization_args)
    realization = (production_ledger.run("source_routing_realization", realization_args, make_realization)
                   if production_ledger else make_realization())
    write_record(root / "realization.json", realization)
    return {"snapshot": snapshot, "authority": authority, "acquisition_receipt": acquisition_receipt,
            "policy": policy, "warrants": warrants, "mappings": mappings, "assimilation": assimilation,
            "realization": realization, "stage_receipts": receipts}
