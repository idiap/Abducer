# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Record a live literature-to-theory chain before canonical consumption.

Every stage freezes its exact inputs and implementation before invoking its
producer. The completed manifest is a portable record of that execution. It is
not a claim that model-generated proposals or internally correlated judgments
are scientifically true. Historical replay manifests retain their own format.
"""
from __future__ import annotations

import copy
import inspect
from pathlib import Path
from typing import Any, Callable, Mapping

from .contracts import ContractError, bytes_digest, canonical_digest, stable_identifier, utc_now
from .literature_production_commitment import (
    LIVE_CHAIN_KIND, MANIFEST_SCHEMA_NAME, ORDERED_STAGE_IDS,
    _validate_manifest_internal, build_portable_literature_production_input_bundle,
)
from .model_author import read_record, write_record


BOUNDARY = (
    "Actual local production from bounded public acquisition and internally correlated model authorship. "
    "No source truth, external or independent preference, scientific improvement, theorem, experiment, "
    "publication or world authority is established by this execution record."
)


def file_identity(root: Path, path: Path, role: str) -> dict[str, Any]:
    """Bind exact regular bytes; acquisition files need not themselves be JSON."""
    path.relative_to(root)
    if any(item.is_symlink() for item in (path, *path.parents)) or not path.is_file():
        raise ContractError("production input is not a regular confined file")
    data = path.read_bytes()
    return {"role": role, "relative_path": path.relative_to(root).as_posix(),
            "sha256": bytes_digest(data), "size_bytes": len(data), "content_digest": None}


def acquisition_bundle(root: Path) -> dict[str, Any]:
    """Describe the exact six captures, acquisition journal and frozen snapshot."""
    acquisition, snapshot = read_record(root / "acquisition.json"), read_record(root / "snapshot.json")
    paths = [root / row["response"]["path"] for row in acquisition["captures"]]
    paths += [root / "acquisition.json", root / "snapshot.json"]
    if len(paths) != 8 or len(set(paths)) != 8:
        raise ContractError("live source bundle requires six distinct raw lane captures")
    value = {"authority_root_kind": "caller_supplied_immutable_bundle_root",
             "capture_id": acquisition["content_digest"], "snapshot_id": snapshot["snapshot_id"],
             "artifacts": [file_identity(root, path, path.stem) for path in paths],
             "embedded_version_graphs": [],
             "source_ids": sorted(row["source_id"] for row in snapshot["sources"]),
             "authority_boundary": BOUNDARY}
    value["bundle_digest"] = canonical_digest(value)
    return value


class ProductionLedger:
    """Execute eleven ordered stages with durable request-before-output records."""

    def __init__(self, *, workspace: Path, root: Path, target_id: str, run_id: str,
                 source_bundle: Mapping[str, Any], state_version: int = 0):
        self.workspace, self.root = workspace.resolve(), root.resolve()
        self.root.relative_to(self.workspace)
        self.root.mkdir(parents=True, exist_ok=False)
        self.identity = {"target_id": target_id, "run_id": run_id, "state_version": state_version}
        self.source_bundle = copy.deepcopy(dict(source_bundle))
        self.started = utc_now()
        self.stages: list[dict[str, Any]] = []
        repository = Path(__file__).resolve().parents[2]
        files = sorted([*(repository / "agentic/discovery").glob("*.py"),
                        *(repository / "agentic/spec").glob("*.schema.json"),
                        repository / "agentic/scripts/run_discovery_operator_protocol.py",
                        repository / "agentic/scripts/validate_discovery_operator_protocol.py"])
        self.dependencies = [file_identity(repository, path, "local_semantic_dependency") for path in files]
        self.code = file_identity(repository, Path(__file__).resolve(), "live_production_recorder")
        self.schema = file_identity(repository, repository / "agentic/spec" / MANIFEST_SCHEMA_NAME, "manifest_schema")

    def run(self, stage_id: str, inputs: Mapping[str, Any], producer: Callable,
            *, schema: str | None = None, reason_codes=()) -> dict[str, Any]:
        """Invoke a producer returning a payload, optionally with its native receipt."""
        index = len(self.stages)
        if index >= len(ORDERED_STAGE_IDS) or ORDERED_STAGE_IDS[index] != stage_id:
            raise ContractError("live production stages must execute in their exact causal order")
        folder = self.root / f"{index:02d}-{stage_id}"
        bindings = []
        for role, value in inputs.items():
            # Lists and scalars are wrapped only in the saved file. Their input
            # digest still names the exact value consumed by the producer.
            path = folder / "inputs" / (role + ".json")
            write_record(path, {"value": value})
            digest = canonical_digest(value)
            source = next((row["stage_id"] for row in reversed(self.stages)
                           if row["output"]["content_digest"] == digest), None)
            bindings.append({"role": role, "digest": digest, "source_stage_id": source,
                             "source_artifact_path": path.relative_to(self.workspace).as_posix()})
        repository = Path(__file__).resolve().parents[2]
        producer_file = inspect.getsourcefile(producer)
        if not producer_file:
            raise ContractError("production stage requires an inspectable local producer")
        implementation = {"symbol": producer.__module__ + "." + producer.__qualname__,
            "implementation_version": "1.0.0", "code_artifact": file_identity(repository, Path(producer_file).resolve(), "stage_producer"),
            "dependencies": self.dependencies, "dependency_set_digest": canonical_digest(self.dependencies)}
        implementation["implementation_digest"] = canonical_digest(implementation)
        started = utc_now()
        request = {"request_id": stable_identifier("production-request", stage_id, self.identity,
                       canonical_digest(bindings), implementation["implementation_digest"], started),
            "stage_id": stage_id, **self.identity, "created_at": started,
            "publication_enabled": False, "world_commissioning_requested": False,
            "input_bindings": bindings, "input_digest": canonical_digest(bindings),
            "implementation_digest": implementation["implementation_digest"],
            "dependency_set_digest": implementation["dependency_set_digest"]}
        request["request_digest"] = canonical_digest(request)
        write_record(folder / "request.json", request)
        result = producer()
        payload, native = (result[0], result[1]) if isinstance(result, tuple) else (result, None)
        if not isinstance(payload, Mapping):
            raise ContractError("production stage output must be an object")
        payload = copy.deepcopy(dict(payload))
        completed = utc_now()
        output_digest = canonical_digest(payload)
        receipt = {"receipt_id": stable_identifier("production-receipt", request["request_digest"],
                       "succeeded", output_digest, completed), "status": "succeeded",
            "started_at": started, "completed_at": completed, "request_id": request["request_id"],
            "request_digest": request["request_digest"], "input_digest": request["input_digest"],
            "output_digest": output_digest, "implementation_digest": implementation["implementation_digest"],
            "dependency_set_digest": implementation["dependency_set_digest"],
            "producer_authority": "local_registered_operator_execution" if native else "local_unregistered_execution",
            "reason_codes": sorted(set(reason_codes)), "authority_boundary": BOUNDARY, "native_receipt": native}
        derived = []
        if stage_id in {"parent_conceptual_adjudication", "synthesis_conceptual_adjudication"}:
            role = "parent_reflection" if stage_id.startswith("parent") else "theory_only_synthesis"
            derived = [{"role": "typed_conceptual_systems",
                "derivation_kind": "stage_internal_deterministic_projection",
                "derived_from_input_roles": [role],
                "content_digest": payload["input_binding"]["conceptual_systems_digest"],
                "row_count": len(payload["blind_packet"]["candidates"]),
                "authority_class": "derived_non_authoritative_intermediate",
                "authority_boundary": "These rows project exact parent content for adjudication; they are not independently acquired evidence."}]
        stage = {"stage_index": index, "stage_id": stage_id, "status": "succeeded", "request": request,
            "receipt": receipt, "implementation": implementation, "derived_intermediates": derived,
            "output": {"artifact_role": stage_id, "schema_path": "agentic/spec/" + schema if schema else None,
                       "content_digest": output_digest, "payload": payload}}
        write_record(folder / "stage.json", stage)
        self.stages.append(stage)
        return payload

    def finish(self) -> tuple[dict[str, Any], str]:
        """Seal the complete chain and reopen its exact bytes as canonical input."""
        order = [{"stage_index": row["stage_index"], "stage_id": row["stage_id"],
                  "request_id": row["request"]["request_id"], "receipt_id": row["receipt"]["receipt_id"],
                  "status": row["status"], "output_digest": row["output"]["content_digest"]} for row in self.stages]
        manifest = {"schema_version": "1.0.0", "manifest_id": stable_identifier("literature-production-chain",
                        self.source_bundle["bundle_digest"], self.started, order),
            "chain_kind": LIVE_CHAIN_KIND, **self.identity, "execution_started_at": self.started,
            "publication_enabled": False, "world_commissioning_authorized": False,
            "chain_status": "completed_before_world_commissioning", "source_bundle": self.source_bundle,
            "schema_identity": self.schema, "ordered_stage_ids": list(ORDERED_STAGE_IDS), "stages": self.stages,
            "chain_order_digest": canonical_digest(order), "claim_boundaries": {
                "bounded_local_production_causality": True, "source_truth_authorized": False,
                "global_latestness_authorized": False, "exhaustive_coverage_authorized": False,
                "literature_benefit_authorized": False, "internal_correlated_conceptual_adjudication_executed": True,
                "external_or_independent_conceptual_preference_authorized": False,
                "internal_deep_lens_adjudication_executed": True, "creativity_or_depth_authorized": False,
                "physics_value_authorized": False, "theorem_or_yang_mills_result_authorized": False,
                "independent_producer_or_evaluator_authorized": False, "experiments_executed": False}}
        manifest["manifest_digest"] = canonical_digest(manifest)
        _validate_manifest_internal(manifest)
        path = self.root / "manifest.json"
        write_record(path, manifest)
        relative = path.relative_to(self.workspace).as_posix()
        bundle = build_portable_literature_production_input_bundle(self.workspace, relative)
        write_record(self.root / "input-bundle.json", bundle)
        return bundle, (self.root / "input-bundle.json").relative_to(self.workspace).as_posix()
