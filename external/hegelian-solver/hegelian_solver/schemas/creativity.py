# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Pydantic models for conceptual creativity analysis.

A `ConceptualCreativityAnalysis` explains *why* a transformation candidate counts as a
creative move rather than a merely corrective one: what latent tension it reframes, what
new constructive resource it introduces, what it preserves, what it makes newly possible
(its generative payoff), and what it risks. Every field is meant to be grounded in the
candidate's own trace artifacts (its trigger, preservation map, expected obligations,
residual limits) rather than asserted free-form — see `hegelian_solver.creativity` for the
deterministic builder and `agents/hegelian-conceptual-creativity-reasoner` for the agent-facing
version of the same discipline.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from hegelian_solver.schemas.models import StrictModel

ConceptualOperationKind = Literal[
    "closure_completion",
    "abstraction_interface_discovery",
    "invariance_reparameterization",
    "quotienting_redundancy_removal",
    "localization_regime_restriction",
    "externalization_or_tooling",
    "bridge_mediation",
    "latent_carrier_introduction",
    "governance_safety_scaffold",
]


class SourcePressure(StrictModel):
    """The determinate negation or discovery pressure that the creative move responds to."""

    kind: Literal["failure", "discovery_signal"]
    id: str
    label: str
    statement: str


class ConceptualCreativityAnalysis(StrictModel):
    id: str
    candidate_id: str
    operator: str
    operation: ConceptualOperationKind
    repair_vs_affordance: Literal["repair", "affordance_creation", "mixed"]
    source_pressure: SourcePressure
    latent_tension: str
    creative_reframing: str
    new_constructive_resource: str
    new_affordance: list[str] = Field(default_factory=list)
    preservation_under_transformation: list[str] = Field(default_factory=list)
    generative_payoff: list[str] = Field(default_factory=list)
    creative_risks: list[str] = Field(default_factory=list)
    why_creative_not_corrective: str
    downstream_concept_seeds: list[str] = Field(default_factory=list)
    residual_todos: list[str] = Field(default_factory=list)


def all_creativity_schema_models() -> list[type[StrictModel]]:
    return [SourcePressure, ConceptualCreativityAnalysis]
