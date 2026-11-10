# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Stable typed failures for dynamic experiment runtime v3."""

from __future__ import annotations

from typing import Any, Mapping

from agentic.discovery.contracts import ContractError


class ExperimentRuntimeError(ContractError):
    """Base failure carrying a machine-stable reason code."""

    error_kind = "runtime"

    def __init__(
        self,
        reason_code: str,
        message: str,
        *,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        if not isinstance(reason_code, str) or not reason_code.strip():
            raise ValueError("experiment reason_code must be non-empty")
        self.reason_code = reason_code
        self.details = dict(details or {})
        super().__init__(
            f"experiment_{self.error_kind}[{reason_code}]: {message}"
        )


class ExperimentSpecError(ExperimentRuntimeError):
    """A commissioned v3 specification is absent, unsafe, or inconsistent."""

    error_kind = "spec"


class ExperimentAuthorityError(ExperimentRuntimeError):
    """Observed executable, dependency, or environment authority is stale."""

    error_kind = "authority"


class ExperimentOutputError(ExperimentRuntimeError):
    """An adapter output is outside the closed v3 result union."""

    error_kind = "output"


class ExperimentExecutionError(ExperimentRuntimeError):
    """A commissioned run cannot be executed or persisted safely."""

    error_kind = "execution"


class ExperimentReceiptError(ExperimentRuntimeError):
    """A v3 receipt fails identity, replay, or semantic validation."""

    error_kind = "receipt"


class ExperimentMigrationRequired(ExperimentRuntimeError):
    """Historical v2 bytes were presented where current v3 authority is required."""

    error_kind = "migration"


__all__ = [
    "ExperimentAuthorityError",
    "ExperimentExecutionError",
    "ExperimentMigrationRequired",
    "ExperimentOutputError",
    "ExperimentReceiptError",
    "ExperimentRuntimeError",
    "ExperimentSpecError",
]
