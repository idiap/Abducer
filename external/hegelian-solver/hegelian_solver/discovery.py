# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Discovery signal mining.

Where `failures.py` reacts to negative evidence (something the concept got wrong),
`mine_discovery_signals` reacts to positive structural pressure that isn't itself a
failure: enough examples to suggest a shared interface, invariants/representation maps
suggesting an invariant pattern, physics symmetries, or LM tool/trace usage. Each detected
`DiscoverySignal` already names its `candidate_move` (the operator in
`operators/library.py` it should trigger) and a placeholder `score` dict matching the
domain's ranking features, mirroring how `FailureCertificate.repair_target` works for
failures. Like failures, signals feed `operators.propose_candidates` as triggers.
"""

from __future__ import annotations

from hegelian_solver.ids import stable_id
from hegelian_solver.schemas import ConceptNode, DiscoverySignal


def mine_discovery_signals(concept: ConceptNode) -> list[DiscoverySignal]:
    signals: list[DiscoverySignal] = []

    if len(concept.examples) >= 2:
        label = "SharedInterface"
        payload = {
            "label": label,
            "evidence": concept.examples,
            "latent_structure": {
                "examples": len(concept.examples),
                "interface": concept.interface,
                "axioms": concept.axioms_or_constraints,
            },
            "candidate_move": "AbstractInterface",
            "candidate_concept": f"Abstract{concept.name}",
            "expected_obligations": ["coverage", "transfer", "non_vacuity", "novelty"],
            "score": {
                "coverage": min(1.0, len(concept.examples) / 4),
                "compression": 0.7,
                "transfer": 0.7,
                "predictive_power": 0.4,
                "canonicality": 0.5,
                "complexity_penalty": 0.2,
                "overfit_penalty": 0.2,
            },
        }
        payload["id"] = stable_id("signal", payload)
        signals.append(DiscoverySignal.model_validate(payload))

    if concept.invariants or concept.representation_maps:
        label = "InvariantPattern"
        payload = {
            "label": label,
            "evidence": concept.invariants + concept.representation_maps,
            "latent_structure": {
                "invariants": concept.invariants,
                "representation_maps": concept.representation_maps,
            },
            "candidate_move": "Invariantize",
            "candidate_concept": f"Invariant{concept.name}",
            "expected_obligations": ["well_defined_equivalence", "protected_distinctions"],
            "score": {
                "coverage": 0.6,
                "compression": 0.6,
                "transfer": 0.5,
                "predictive_power": 0.4,
                "canonicality": 0.7,
                "complexity_penalty": 0.2,
                "overfit_penalty": 0.1,
            },
        }
        payload["id"] = stable_id("signal", payload)
        signals.append(DiscoverySignal.model_validate(payload))

    if concept.domain == "physical_concept":
        symmetries = getattr(concept, "symmetries", {})
        if symmetries:
            payload = {
                "label": "SymmetryPattern",
                "evidence": [symmetries],
                "latent_structure": {"symmetries": symmetries},
                "candidate_move": "InvariantizeKinematics",
                "candidate_concept": f"SymmetryAware{concept.name}",
                "expected_obligations": ["covariance", "limiting_case_recovery"],
                "score": {
                    "coverage": 0.6,
                    "compression": 0.5,
                    "transfer": 0.6,
                    "predictive_power": 0.5,
                    "canonicality": 0.6,
                    "complexity_penalty": 0.2,
                    "overfit_penalty": 0.1,
                },
            }
            payload["id"] = stable_id("signal", payload)
            signals.append(DiscoverySignal.model_validate(payload))

    if concept.domain == "language_model_concept":
        tools = getattr(concept, "tools", [])
        traces = getattr(concept, "traces", [])
        if tools or traces:
            payload = {
                "label": "ToolAPIExtension" if tools else "ExternalEvidencePressure",
                "evidence": tools or traces,
                "latent_structure": {"tools": tools, "traces": traces},
                "candidate_move": "Toolify" if tools else "Retrieve",
                "candidate_concept": f"Grounded{concept.name}",
                "expected_obligations": ["tool_schema_validity", "source_support", "risk_bound"],
                "score": {
                    "coverage": 0.5,
                    "compression": 0.5,
                    "transfer": 0.6,
                    "predictive_power": 0.6,
                    "canonicality": 0.5,
                    "complexity_penalty": 0.3,
                    "overfit_penalty": 0.2,
                },
            }
            payload["id"] = stable_id("signal", payload)
            signals.append(DiscoverySignal.model_validate(payload))

    return signals
