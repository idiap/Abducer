# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Common I/O contract for granular solver stages.

`run_stage` is the adapter that lets any stage function (deterministic Python or, in
principle, an LLM agent skill) be invoked uniformly: call `handler(payload)`, then normalize
whatever it returns (a Pydantic model, a dict, or a bare value) into a `SkillOutput` with a
consistent `stage`/`artifact_type`/`payload` shape. This is what each granular skill in
`agents/` is documented against, even though the orchestrator currently calls the
Python functions directly rather than through this contract.
"""

from __future__ import annotations

from typing import Any, Callable

from pydantic import BaseModel, Field


class SkillInput(BaseModel):
    stage: str
    payload: dict[str, Any]
    context: dict[str, Any] = Field(default_factory=dict)


class SkillOutput(BaseModel):
    stage: str
    artifact_type: str
    payload: dict[str, Any]
    diagnostics: list[str] = Field(default_factory=list)


def run_stage(stage: str, payload: dict[str, Any], handler: Callable[[dict[str, Any]], Any]) -> SkillOutput:
    result = handler(payload)
    if hasattr(result, "model_dump"):
        result_payload = result.model_dump(mode="json")
        artifact_type = result.__class__.__name__
    elif isinstance(result, dict):
        result_payload = result
        artifact_type = result.get("artifact_type", "dict")
    else:
        result_payload = {"value": result}
        artifact_type = type(result).__name__
    return SkillOutput(stage=stage, artifact_type=artifact_type, payload=result_payload)
