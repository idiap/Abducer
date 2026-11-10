# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Load the dedicated constructive Category/HoTT producer registry.

The central formal-lens route is deliberately separate from the general
discovery-operator registry.  Its four producers have one narrow job: consume
the same frozen task-semantic ancestor and return finite, internal protocol
evidence.  This loader makes that composition executable rather than leaving
route names in prose.  It rejects duplicate JSON keys, unsafe dependency
paths, missing local closure files, callable drift, or any attempt to relabel
thread concurrency as process, kernel, filesystem, network, hidden-input, or
cognitive isolation.

The resulting binding hashes live repository bytes.  That is useful local
replay authority, but it is not a signer, independent model, external judge,
or physics authority; every public record says so explicitly.
"""

from __future__ import annotations

import importlib
import inspect
import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping

from .contracts import ROOT, canonical_digest, file_digest


REGISTRY_PATH = ROOT / "agentic/registries/formal_lens_producer_registry.yaml"
REGISTRY_RELATIVE_PATH = "agentic/registries/formal_lens_producer_registry.yaml"
ROUTE_ORDER = ("categorical", "hott", "combined", "capable_nonformal")

_EXPECTED_CALLABLES = {
    "categorical": ("category_theory", "constructive-category-route.v1", "produce_categorical_route", ("categorical",)),
    "hott": ("homotopy_type_theory", "constructive-hott-route.v1", "produce_hott_route", ("hott",)),
    "combined": ("combined_formal", "constructive-category-hott-combined-route.v1", "produce_combined_route", ("categorical", "hott")),
    "capable_nonformal": ("capable_nonformal_control", "capable-nonformal-reasoning-control.v1", "produce_capable_nonformal_route", ()),
}
_EXPECTED_EXECUTION_CONTRACT = {
    "scheduler": "ThreadPoolExecutor",
    "max_workers": 4,
    "start_barrier_parties": 4,
    "execution_backend": "shared_process_thread_pool",
    "process_isolation": False,
    "kernel_isolation": False,
    "filesystem_isolation": False,
    "network_isolation": False,
    "hidden_input_independence_authorized": False,
    "cognitive_independence_authorized": False,
    "semantic_independence_authorized": False,
    "claim_scope": "concurrent_local_protocol_routes_only",
}
_EXPECTED_AUTHORITY_BOUNDARY = {
    "registry_authority": "repository_local_registered_execution_not_external_authority",
    "formal_outputs": "finite_internal_constructive_protocol_only",
    "experiments": "secondary_theory_requested_falsifier_only",
    "truth_authorized": False,
    "conceptual_value_authorized": False,
    "physics_value_authorized": False,
    "theorem_authorized": False,
    "continuum_authorized": False,
    "yang_mills_authorized": False,
}
_REQUIRED_DEPENDENCIES = {
    "agentic/discovery/contracts.py",
    "agentic/discovery/formal_lens_production.py",
    "agentic/discovery/formal_lens_registry.py",
    "agentic/spec/formal_lens_production_packet.schema.json",
    "agentic/spec/formal_lens_production_request.schema.json",
    "agentic/spec/task_relation_compilation.schema.json",
    "skills/common/abstraction_formal_reasoning.py",
    "skills/common/task_relation_compiler.py",
}


class FormalLensRegistryError(ValueError):
    """Raised when a route or its local executable authority drifts."""


@dataclass(frozen=True, slots=True)
class FormalLensProducerBinding:
    """One validated route and the exact callable used by the thread wave."""

    route_id: str
    route_kind: str
    producer_id: str
    module: str
    callable_name: str
    required_lenses: tuple[str, ...]
    function: Callable[[Mapping[str, Any], Any], dict[str, Any]]
    implementation_sha256: str
    dependency_descriptors: tuple[dict[str, Any], ...]

    def public_record(self) -> dict[str, Any]:
        """Return only the sealed, schema-shaped local binding evidence."""

        return {
            "route_id": self.route_id,
            "producer_id": self.producer_id,
            "module": self.module,
            "callable": self.callable_name,
            "implementation_sha256": self.implementation_sha256,
            "dependency_descriptors": [dict(row) for row in self.dependency_descriptors],
        }


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise FormalLensRegistryError(f"formal-lens registry repeats key {key!r}")
        result[key] = value
    return result


def _load_registry_bytes(path: Path) -> tuple[dict[str, Any], bytes]:
    if path.is_symlink() or not path.is_file():
        raise FormalLensRegistryError("formal-lens registry must be one regular file")
    data = path.read_bytes()
    try:
        raw = json.loads(data, object_pairs_hook=_object_without_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FormalLensRegistryError(f"formal-lens registry is not JSON-compatible YAML: {exc}") from exc
    if not isinstance(raw, dict):
        raise FormalLensRegistryError("formal-lens registry root must be an object")
    return raw, data


def _dependency_descriptor(raw: str) -> dict[str, Any]:
    if not isinstance(raw, str) or not raw:
        raise FormalLensRegistryError("formal-lens dependency path must be nonempty text")
    relative = PurePosixPath(raw)
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts) or "\\" in raw:
        raise FormalLensRegistryError(f"unsafe formal-lens dependency path: {raw!r}")
    path = ROOT.joinpath(*relative.parts)
    if path.is_symlink() or not path.is_file():
        raise FormalLensRegistryError(f"formal-lens dependency is not a regular file: {raw}")
    return {
        "relative_path": relative.as_posix(),
        "sha256": file_digest(path),
        "byte_length": path.stat().st_size,
    }


def _validate_route(row: Any, expected_route_id: str) -> FormalLensProducerBinding:
    if not isinstance(row, dict) or set(row) != {
        "route_id",
        "route_kind",
        "producer_id",
        "module",
        "callable",
        "required_lenses",
        "dependency_paths",
    }:
        raise FormalLensRegistryError(f"route {expected_route_id} does not have the exact registry contract")
    if row["route_id"] != expected_route_id:
        raise FormalLensRegistryError("formal-lens route order or identity drift")
    route_kind, producer_id, callable_name, required_lenses = _EXPECTED_CALLABLES[expected_route_id]
    if (
        row["route_kind"] != route_kind
        or row["producer_id"] != producer_id
        or row["module"] != "agentic.discovery.formal_lens_production"
        or row["callable"] != callable_name
        or tuple(row["required_lenses"]) != required_lenses
    ):
        raise FormalLensRegistryError(f"route {expected_route_id} implementation binding drift")
    paths = row["dependency_paths"]
    if not isinstance(paths, list) or len(paths) != len(set(paths)) or set(paths) != _REQUIRED_DEPENDENCIES:
        raise FormalLensRegistryError(f"route {expected_route_id} dependency closure drift")
    descriptors = tuple(_dependency_descriptor(path) for path in paths)
    module = importlib.import_module(row["module"])
    function = getattr(module, callable_name, None)
    if not callable(function) or function.__module__ != row["module"]:
        raise FormalLensRegistryError(f"route {expected_route_id} callable is unavailable or foreign")
    parameters = tuple(inspect.signature(function).parameters)
    if parameters != ("request", "execution_context"):
        raise FormalLensRegistryError(
            f"route {expected_route_id} callable must accept exactly request and execution_context"
        )
    implementation = next(
        descriptor
        for descriptor in descriptors
        if descriptor["relative_path"] == "agentic/discovery/formal_lens_production.py"
    )
    return FormalLensProducerBinding(
        route_id=expected_route_id,
        route_kind=route_kind,
        producer_id=producer_id,
        module=row["module"],
        callable_name=callable_name,
        required_lenses=required_lenses,
        function=function,
        implementation_sha256=str(implementation["sha256"]),
        dependency_descriptors=descriptors,
    )


def load_formal_lens_producer_registry(
    path: Path = REGISTRY_PATH,
) -> tuple[tuple[FormalLensProducerBinding, ...], dict[str, Any]]:
    """Load four exact producers and return their local byte-bound record."""

    raw, _ = _load_registry_bytes(path)
    if set(raw) != {
        "schema_version",
        "registry_id",
        "execution_contract",
        "routes",
        "authority_boundary",
    }:
        raise FormalLensRegistryError("formal-lens registry root contract drift")
    if raw["schema_version"] != "1.0.0" or raw["registry_id"] != "formal-lens-producer-registry.v1":
        raise FormalLensRegistryError("formal-lens registry identity drift")
    if raw["execution_contract"] != _EXPECTED_EXECUTION_CONTRACT:
        raise FormalLensRegistryError("formal-lens execution/isolation contract drift")
    if raw["authority_boundary"] != _EXPECTED_AUTHORITY_BOUNDARY:
        raise FormalLensRegistryError("formal-lens authority boundary drift")
    rows = raw["routes"]
    if not isinstance(rows, list) or len(rows) != len(ROUTE_ORDER):
        raise FormalLensRegistryError("formal-lens registry requires exactly four routes")
    bindings = tuple(_validate_route(row, route_id) for row, route_id in zip(rows, ROUTE_ORDER, strict=True))
    record: dict[str, Any] = {
        "registry_version": "1.0.0",
        "registry_path": REGISTRY_RELATIVE_PATH,
        "registry_file_sha256": file_digest(path),
        "route_bindings": [binding.public_record() for binding in bindings],
        "authority_boundary": "repository_local_registered_execution_not_external_authority",
    }
    record["binding_digest"] = canonical_digest(record)
    return bindings, record


__all__ = [
    "FormalLensProducerBinding",
    "FormalLensRegistryError",
    "REGISTRY_PATH",
    "ROUTE_ORDER",
    "load_formal_lens_producer_registry",
]
