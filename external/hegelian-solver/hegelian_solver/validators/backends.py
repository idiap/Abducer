# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Pluggable validation backend registry.

A `ValidationBackend` is a named handler for one verification method (`proof_plan`, `smt`,
`theorem_prover`, `unit_test`, `simulation`, `benchmark`, `human_review`, ...). None of the
default backends are wired to a real prover/simulator yet — `planned_backend` returns a
`status: "planned"` stub for all of them — but the registry shape is what lets a future
caller register a real SMT or simulation backend under the same name without touching
`validators/core.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


BackendResult = dict[str, Any]
BackendHandler = Callable[[dict[str, Any]], BackendResult]


@dataclass(frozen=True)
class ValidationBackend:
    name: str
    role: str
    handler: BackendHandler

    def run(self, payload: dict[str, Any]) -> BackendResult:
        return self.handler(payload)


def planned_backend(role: str) -> BackendHandler:
    def _handler(payload: dict[str, Any]) -> BackendResult:
        return {
            "status": "planned",
            "role": role,
            "payload_ref": payload.get("id") or payload.get("candidate_id"),
            "notes": [f"{role} backend is registered but not connected"],
        }

    return _handler


class BackendRegistry:
    def __init__(self) -> None:
        self._backends: dict[str, ValidationBackend] = {}

    def register(self, backend: ValidationBackend) -> None:
        self._backends[backend.name] = backend

    def get(self, name: str) -> ValidationBackend:
        return self._backends[name]

    def names(self) -> list[str]:
        return sorted(self._backends)

    def run(self, name: str, payload: dict[str, Any]) -> BackendResult:
        return self.get(name).run(payload)


def default_backend_registry() -> BackendRegistry:
    registry = BackendRegistry()
    for name, role in [
        ("proof_plan", "proof obligation planning"),
        ("smt", "bounded first-order check"),
        ("model_finder", "finite counterexample search"),
        ("theorem_prover", "certified theorem-prover hook"),
        ("unit_test", "runtime unit tests"),
        ("simulation", "physics simulation"),
        ("benchmark", "benchmark evaluation"),
        ("human_review", "human review"),
    ]:
        registry.register(ValidationBackend(name=name, role=role, handler=planned_backend(role)))
    return registry
