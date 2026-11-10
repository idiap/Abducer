# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Dispatch initialization artifacts through the existing operator receipt engine.

Most operators already have registered executable producers and validators. The
source-policy pair has public deterministic producers but no generic registry
entry; these two narrow bindings reopen and validate their complete inputs.
Neither binding grants network, model, canonical-write or scientific authority.
"""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping

from .contracts import (ContractError, Namespace, artifact_descriptor, canonical_digest,
                        load_json, verify_artifact_descriptor)
from .literature_acquisition import validate_source_routing_pre_map_policy, validate_source_routing_realization
from .model_author import write_record
from .receipts import (DiscoveryOperatorDispatcher, OperatorBinding, ReceiptStore,
                       ValidatorBinding, build_operator_request)


CONCEPTUAL_OPERATORS = {
    "high-risk-hypothesis-forger", "parallel-hypothesis-portfolio",
    "reflective-conceptual-discovery", "reflective-theory-synthesizer",
    "blind-conceptual-preference-adjudicator",
}
POLICY_OPERATOR = "source-routing-pre-map-policy-producer"
REALIZATION_OPERATOR = "source-routing-realization-producer"


def _authority_input(request, workspace):
    namespace = Namespace.from_mapping(request["identity"])
    if len(request["input_artifacts"]) != 1:
        raise ContractError("source authority producer requires exactly one complete envelope")
    return load_json(verify_artifact_descriptor(request["input_artifacts"][0], workspace, namespace))


def _replay_authority(request, envelope):
    artifact = envelope["authority_artifact"]
    identity = request["identity"]
    if any(artifact[key] != identity[key] for key in ("target_id", "run_id", "state_version")):
        raise ContractError("source authority artifact crossed its dispatched identity")
    if canonical_digest(artifact) != request["parameters"]["artifact_digest"]:
        raise ContractError("source authority artifact differs from the dispatched commitment")
    arguments = envelope["validation_inputs"]
    if request["operator"]["operator_id"] == POLICY_OPERATOR:
        return validate_source_routing_pre_map_policy(artifact, **arguments)
    if request["operator"]["operator_id"] == REALIZATION_OPERATOR:
        return validate_source_routing_realization(artifact, **arguments)
    raise ContractError("unknown source authority producer")


def source_authority_operator(request: dict, workspace: Path) -> dict:
    """Materialize a source artifact only after full public validator replay."""
    value = _replay_authority(request, _authority_input(request, workspace))
    if len(request["declared_outputs"]) != 1:
        raise ContractError("source authority producer requires exactly one declared output")
    path = workspace / request["declared_outputs"][0]
    path.resolve().relative_to(workspace.resolve())
    write_record(path, value)
    return {"artifacts": [{"path": request["declared_outputs"][0]}],
            "explicit_unknowns": ["Source routing validation establishes local causal identity, not source truth."]}


def source_authority_validator(request: dict, artifacts: list[dict], workspace: Path) -> bool:
    """Independently reopen output and recompute its complete authority boundary."""
    if len(artifacts) != 1:
        raise ContractError("source authority validator requires exactly one output")
    namespace = Namespace.from_mapping(request["identity"])
    output = load_json(verify_artifact_descriptor(artifacts[0], workspace, namespace))
    expected = _replay_authority(request, _authority_input(request, workspace))
    if output != expected:
        raise ContractError("source authority output differs from independent exact replay")
    return True


class BootstrapDispatcher:
    """Keep a complete request/receipt ledger for one target and frozen generation."""

    def __init__(self, *, workspace: Path, root: Path, target_id: str, run_id: str, state_version: int = 0):
        from agentic.scripts.discovery_operator_registry import load_registry
        from agentic.scripts.dispatch_discovery_operators import _bindings
        self.workspace = workspace.resolve()
        self.root = root.resolve()
        self.root.relative_to(self.workspace)
        self.namespace = Namespace(target_id, run_id, "root", state_version)
        self.requests, self.receipts = [], []
        self.projection = None
        self.policy = self.realization = None
        bindings = list(_bindings(load_registry()))
        # The explicit closure covers the source algorithms and all local schema
        # documents they resolve. It is carried into each validator receipt.
        repository = Path(__file__).resolve().parents[2]
        dependencies = tuple("repo://" + path.relative_to(repository).as_posix() for path in sorted([
            * (repository / "agentic/discovery").glob("*.py"),
            * (repository / "agentic/spec").glob("*.schema.json"),
        ]))
        for operator_id in (POLICY_OPERATOR, REALIZATION_OPERATOR):
            bindings.append(OperatorBinding(operator_id, "1.0.0", "literature_assimilation",
                function=source_authority_operator,
                validators=(ValidatorBinding(operator_id + "-validator", "1.0.0",
                    function=source_authority_validator, dependency_paths=dependencies,
                    dependency_policy="explicit_local_semantic_closure"),)))
        self.bindings = {binding.operator_id: binding for binding in bindings}
        self.dispatcher = DiscoveryOperatorDispatcher(bindings, workspace=self.workspace,
            receipt_store=ReceiptStore(self.root / "receipts"))

    def dispatch(self, operator_id: str, kind: str, envelope: Mapping[str, Any], *, parameters=None):
        """Freeze one causal envelope and run both its producer and validators."""
        value, parameters = copy.deepcopy(dict(envelope)), copy.deepcopy(parameters or {})
        if operator_id in CONCEPTUAL_OPERATORS and self.projection is not None:
            value["literature_production_projection"] = copy.deepcopy(self.projection)
            parameters["literature_production_projection_digest"] = self.projection["projection_digest"]
        if operator_id in CONCEPTUAL_OPERATORS and self.realization is not None:
            value["source_routing_pre_map_policy"] = copy.deepcopy(self.policy)
            value["source_routing_realization"] = copy.deepcopy(self.realization)
        number = len(self.requests) + 1
        prefix = self.root.relative_to(self.workspace).as_posix()
        input_name = f"{prefix}/inputs/{number:02d}-{operator_id}.json"
        output_name = f"{prefix}/outputs/{number:02d}-{operator_id}.json"
        write_record(self.workspace / input_name, value)
        request = build_operator_request(operator_id=operator_id,
            operator_version=self.bindings[operator_id].version, kind=kind, namespace=self.namespace,
            invocation_id=f"initialization-{number:02d}-{operator_id}",
            input_artifacts=[artifact_descriptor(self.workspace / input_name, self.workspace, self.namespace)],
            declared_outputs=[output_name], parameters=parameters, required=True)
        write_record(self.root / "requests" / f"{number:02d}.json", request)
        self.requests.append(request)
        receipt = self.dispatcher.dispatch(request)
        self.receipts.append(receipt)
        if receipt["status"] != "succeeded":
            raise ContractError(f"initialization operator {operator_id} failed: {receipt.get('error')}")
        return load_json(self.workspace / output_name), receipt, output_name
