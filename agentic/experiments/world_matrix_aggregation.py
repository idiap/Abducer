# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Order-independent collector for separately produced five-world envelopes."""

from __future__ import annotations

import copy
import threading
from collections.abc import Mapping
from typing import Any

from agentic.discovery.contracts import ContractError

from .world_matrix import (
    CommittedCausalEvidenceResolver,
    WORLD_IDS,
    require_authoritative_experiment_world_matrix_commission,
    validate_experiment_world_observation_envelope,
    validate_five_world_matrix,
)


class ExperimentWorldMatrixAggregator:
    """Accept independently completed worlds in any order, exactly once.

    ``add`` is lock-protected so parallel workers can publish their envelopes
    without sharing mutable observation state.  ``finalize`` is fail-closed
    until all five separately validated worlds are present, then restores the
    canonical order required by the certificate contract.
    """

    def __init__(
        self,
        commission: Mapping[str, Any],
        *,
        evidence_resolver: CommittedCausalEvidenceResolver,
    ) -> None:
        self._evidence_resolver = evidence_resolver
        self._commission = require_authoritative_experiment_world_matrix_commission(
            commission, evidence_resolver=evidence_resolver
        )
        self._by_world: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()

    def add(self, envelope: Mapping[str, Any]) -> dict[str, Any]:
        """Validate and atomically add one actual world producer envelope."""

        validated = validate_experiment_world_observation_envelope(
            self._commission, envelope, evidence_resolver=self._evidence_resolver
        )
        world_id = validated["world_id"]
        with self._lock:
            if world_id in self._by_world:
                raise ContractError(f"duplicate observation envelope for {world_id}")
            self._by_world[world_id] = copy.deepcopy(validated)
        return validated

    def pending_world_ids(self) -> tuple[str, ...]:
        """Return canonical world IDs not yet supplied by parallel workers."""

        with self._lock:
            return tuple(world for world in WORLD_IDS if world not in self._by_world)

    def finalize(self) -> dict[str, Any]:
        """Derive the certificate only after every distinct world is present."""

        with self._lock:
            missing = [world for world in WORLD_IDS if world not in self._by_world]
            if missing:
                raise ContractError(
                    "five-world aggregation is incomplete: " + ", ".join(missing)
                )
            envelopes = [copy.deepcopy(self._by_world[world]) for world in WORLD_IDS]
        return validate_five_world_matrix(
            self._commission, envelopes, evidence_resolver=self._evidence_resolver
        )


__all__ = ["ExperimentWorldMatrixAggregator"]
