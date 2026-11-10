# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Lifecycle hooks for the orchestrator's reflective refinement loop.

Every iteration of propose -> validate -> rank fires named hooks before the orchestrator
decides whether to stop or refine further. Hooks let external code (CLI flags, tests,
telemetry, future agent skills) observe or react to a run without editing the orchestrator
itself. All hooks default to no-ops, so passing no `SolverHooks` changes nothing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

HookFn = Callable[..., None]


def _noop(*_args: Any, **_kwargs: Any) -> None:
    return None


@dataclass
class SolverHooks:
    on_iteration_start: HookFn = _noop
    on_candidates_generated: HookFn = _noop
    on_validated: HookFn = _noop
    on_ranked: HookFn = _noop
    on_iteration_end: HookFn = _noop
    on_stop: HookFn = _noop

    def fire(self, name: str, **kwargs: Any) -> None:
        getattr(self, name)(**kwargs)
