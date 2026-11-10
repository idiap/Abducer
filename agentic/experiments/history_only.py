# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Fail-closed compatibility names for superseded experiment producers.

Historical validators and migration tools may import their implementation
modules directly.  Canonical callers must use the descendant content-graph
facade; the package-level names below deliberately cannot produce new state.
"""

from __future__ import annotations

from typing import NoReturn

from .errors import ExperimentMigrationRequired


CANONICAL_DESCENDANT_API = (
    "agentic.experiments:run_canonical_descendant_experiment_v3"
)


def reject_history_only_execution(symbol: str) -> NoReturn:
    """Reject a package-level attempt to execute a superseded producer."""

    raise ExperimentMigrationRequired(
        "history_only_execution_route",
        (
            f"{symbol} is retained only as an import-compatible history reader; "
            f"new production must use {CANONICAL_DESCENDANT_API}"
        ),
        details={
            "symbol": symbol,
            "production_status": "history_only",
            "canonical_reachability": False,
            "superseded_by": CANONICAL_DESCENDANT_API,
        },
    )


def compile_experiment_spec(*_args: object, **_kwargs: object) -> NoReturn:
    return reject_history_only_execution("compile_experiment_spec")


def execute_experiment(*_args: object, **_kwargs: object) -> NoReturn:
    return reject_history_only_execution("execute_experiment")


def reexecute_v2_experiment(*_args: object, **_kwargs: object) -> NoReturn:
    return reject_history_only_execution("reexecute_v2_experiment")


def run_canonical_theory_support_lane(
    *_args: object, **_kwargs: object
) -> NoReturn:
    return reject_history_only_execution("run_canonical_theory_support_lane")


def run_canonical_world_support_production(
    *_args: object, **_kwargs: object
) -> NoReturn:
    return reject_history_only_execution("run_canonical_world_support_production")


def production_causal_operator_binding(
    *_args: object, **_kwargs: object
) -> NoReturn:
    return reject_history_only_execution("production_causal_operator_binding")


class CausalArtifactProducerRuntime:
    """Import-compatible constructor that cannot restore the legacy producer."""

    def __new__(cls, *_args: object, **_kwargs: object) -> NoReturn:
        return reject_history_only_execution("CausalArtifactProducerRuntime")


__all__ = [
    "CANONICAL_DESCENDANT_API",
    "CausalArtifactProducerRuntime",
    "compile_experiment_spec",
    "execute_experiment",
    "production_causal_operator_binding",
    "reexecute_v2_experiment",
    "reject_history_only_execution",
    "run_canonical_theory_support_lane",
    "run_canonical_world_support_production",
]
