# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""End-to-end tests for the receipt-backed canonical discovery parent cycle.

The main fixture is intentionally causal rather than a bag of independently
valid JSON examples.  Six dispatcher operators execute in one frozen
target/run/state lineage: live literature assimilation -> high-risk generation
-> parallel maturation -> reflective parent -> theory-commissioned exact support
-> distinct reflective synthesis.  The cycle then proves that every output was
consumed by a semantic ledger event in one atomic CAS commit.
"""

from __future__ import annotations

import copy
import datetime as dt
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

from agentic.discovery import cycle as cycle_runtime
from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    artifact_descriptor,
    bytes_digest,
    canonical_digest,
    canonical_json,
    load_json,
    validate_payload,
)
from agentic.discovery.conceptual_adjudication import (
    DIMENSIONS,
    build_adjudication_source_bindings,
    build_blind_packet,
    build_judge_report,
    validate_adjudication_evidence,
)
from agentic.discovery.cycle import (
    EXPERIMENT_WORLD_MATRIX_SCOPE,
    build_canonical_world_authority_projection,
    derive_conceptual_authority,
    finalize_post_adjudication_reflection,
    replay_canonical_world_authority_projection,
    run_canonical_discovery_cycle,
    validate_five_experiment_world_semantics,
)
from agentic.discovery.evaluation import CONCEPTUAL_GATE_IDS, evaluate_discovery_delta
from agentic.discovery.formal_claim_authority import (
    FORMAL_CLAIM_DIRECTIVE_PREFIX,
    build_formal_claim_producer_input,
    formalization_seed_rows,
)
from agentic.discovery.hypotheses import forge_high_risk_portfolio, validate_high_risk_portfolio
from agentic.discovery.ledger import initial_state
from agentic.discovery.literature import (
    LANE_TYPES,
    assimilate_literature,
    build_demo_literature_snapshot,
    run_frontier_literature_cycle,
    resolve_present_literature_freshness,
    validate_assimilation,
    validate_snapshot,
)
from agentic.discovery.literature_acquisition import (
    build_source_routing_pre_map_policy,
    build_source_routing_realization,
    derive_source_routing_semantic_warrants,
    source_routing_realization_requirements,
)
from agentic.discovery.literature_production_commitment import (
    build_portable_literature_production_input_bundle,
)
from agentic.discovery.parallel import (
    build_parallel_manifest,
    run_parallel_hypothesis_portfolio,
    validate_parallel_portfolio,
)
from agentic.discovery.receipts import (
    DiscoveryOperatorDispatcher,
    OperatorBinding,
    ReceiptStore,
    ValidatorBinding,
    build_operator_request,
)
from agentic.discovery.reflection import validate_packet_invariants
from agentic.discovery.workflow import build_reflective_discovery_packet
from agentic.experiments import (
    ExperimentReceiptError,
    triage_probe,
    validate_commissioned_experiment_spec,
    validate_experiment_receipt,
    validate_experiment_reflection_receipt,
)
# Legacy fixture artifacts are history inputs, never the production API route.
from agentic.experiments.runtime import compile_experiment_spec, execute_experiment
from agentic.experiments.world_matrix import (
    AUTHORITY_COMPONENT_ORDER,
    build_experiment_authority_projection,
)
from agentic.scripts.discovery_operator_registry import load_registry
from agentic.scripts.dispatch_discovery_operators import _bindings as registry_bindings
from agentic.scripts.run_discovery_operator_protocol import (
    _conceptual_adjudication,
    _reflective,
)
from agentic.evals.ym_representational_dynamics_20260721.literature_production_chain import (
    build_publication_disabled_literature_production_chain,
)
from agentic.state.discovery_transaction import DiscoveryTransactionStore
from tests.discovery.test_discovery_independent_evaluation import rich_candidate


CANONICAL_OPERATOR_IDS = {
    "reflective-conceptual-discovery",
    "reflective-theory-synthesizer",
    "frontier-literature-assimilator",
    "high-risk-hypothesis-forger",
    "parallel-hypothesis-portfolio",
    "dynamic-symbolic-simulation-experimenter",
    "blind-conceptual-preference-adjudicator",
}

_CACHED_LITERATURE_PRODUCTION_INPUT_BUNDLE: dict[str, Any] | None = None
_LITERATURE_PRODUCTION_MANIFEST_PATH = (
    "committed/literature-production/manifest.json"
)
EXACT_FORMAL_DIRECTIVE = {
    "display_statement": "1/3 + 1/6 = 1/2",
    "formal_claim": {
        "claim_kind": "exact_equality",
        "operation": "equality",
        "left": "1/3 + 1/6",
        "right": "1/2",
    },
    "proof_adapter": "exact",
    "execution_plan": {"kind": "builtin_worker"},
}
EXACT_FORMAL_SEED = (
    FORMAL_CLAIM_DIRECTIVE_PREFIX
    + canonical_json(EXACT_FORMAL_DIRECTIVE).decode("utf-8")
)


def _portable_literature_production_input(
    workspace: Path,
) -> tuple[dict[str, Any], str]:
    """Materialize one reusable exact production bundle for canonical tests."""

    global _CACHED_LITERATURE_PRODUCTION_INPUT_BUNDLE
    if _CACHED_LITERATURE_PRODUCTION_INPUT_BUNDLE is None:
        manifest = build_publication_disabled_literature_production_chain(
            execution_started_at="2026-07-22T12:39:01Z"
        )
        manifest_path = workspace / _LITERATURE_PRODUCTION_MANIFEST_PATH
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_bytes(canonical_json(manifest) + b"\n")
        _CACHED_LITERATURE_PRODUCTION_INPUT_BUNDLE = (
            build_portable_literature_production_input_bundle(
                workspace,
                _LITERATURE_PRODUCTION_MANIFEST_PATH,
            )
        )
    bundle = copy.deepcopy(_CACHED_LITERATURE_PRODUCTION_INPUT_BUNDLE)
    bundle_path = "external-search/literature-production-input-bundle.json"
    _write_json(workspace, bundle_path, bundle)
    return bundle, bundle_path


def _typed_unification(system: Mapping[str, Any]) -> dict[str, Any]:
    """Upgrade one proposal to the typed explanatory graph used by adjudication."""

    row = copy.deepcopy(dict(system))
    before_graph = {
        "nodes": [
            {
                "node_id": "local-construction-pressure",
                "node_kind": "source_case",
                "label": "Local construction pressure in the exact target regime",
                "content_paths": ["/target_pressures_addressed/0"],
            },
            {
                "node_id": "global-interpretation-pressure",
                "node_kind": "source_case",
                "label": "Global interpretation pressure in the exact target regime",
                "content_paths": ["/mechanism_or_principle"],
            },
        ],
        "edges": [],
    }
    mediator = {
        "node_id": "regime-indexed-mediator",
        "node_kind": "mediator",
        "label": "Regime indexed mediator preserving distinct physical burdens",
        "content_paths": ["/mechanism_or_principle"],
    }
    edges = [
        {
            "edge_id": "construction-to-mediator",
            "source_node_id": "local-construction-pressure",
            "relation_kind": "mediates",
            "target_node_id": "regime-indexed-mediator",
            "statement": "The local construction burden enters through an independently correctable mediation relation.",
            "warrant_paths": ["/mechanism_or_principle"],
        },
        {
            "edge_id": "interpretation-to-mediator",
            "source_node_id": "global-interpretation-pressure",
            "relation_kind": "constrains",
            "target_node_id": "regime-indexed-mediator",
            "statement": "The global interpretation burden constrains the mediator without becoming identical to construction.",
            "warrant_paths": ["/mechanism_or_principle"],
        },
    ]
    after_graph = {"nodes": [*before_graph["nodes"], mediator], "edges": edges}
    row["unification_claims"] = {
        "unification_kind": "regime_indexed_mediation",
        "source_case_ids": [
            "local-construction-pressure",
            "global-interpretation-pressure",
        ],
        "mediator": {
            "statement": "A regime indexed mediator relates local construction and global interpretation while preserving their non substitutable physical burdens.",
            "primitive_refs": ["regime indexed explanatory mediator primitive"],
            "relation_refs": ["non erasing mediation between distinct target burdens"],
            "node_ids": ["regime-indexed-mediator"],
        },
        "mappings": [
            {
                "mapping_id": "local-construction-map",
                "source_case_id": "local-construction-pressure",
                "target_node_id": "regime-indexed-mediator",
                "map_kind": "mediation",
                "bridge_statement": "Local construction maps to the mediator only through the proposal's explicit target relevant mechanism.",
                "warrant_paths": ["/mechanism_or_principle"],
            },
            {
                "mapping_id": "global-interpretation-map",
                "source_case_id": "global-interpretation-pressure",
                "target_node_id": "regime-indexed-mediator",
                "map_kind": "interpretation",
                "bridge_statement": "Global interpretation maps to the mediator through a separately correctable explanatory constraint.",
                "warrant_paths": ["/mechanism_or_principle"],
            },
        ],
        "preserved_differences": [
            {
                "difference_id": "construction-remains-distinct",
                "source_case_ids": ["local-construction-pressure"],
                "statement": "Constructing the local carrier remains distinct from interpreting its global physical significance.",
                "preservation_witness_paths": ["/identities_and_differences/0"],
                "witness_node_ids": [
                    "local-construction-pressure",
                    "regime-indexed-mediator",
                ],
                "witness_edge_ids": ["construction-to-mediator"],
            },
            {
                "difference_id": "interpretation-remains-distinct",
                "source_case_ids": ["global-interpretation-pressure"],
                "statement": "Interpreting the global regime remains distinct from constructing the local carrier that enters it.",
                "preservation_witness_paths": ["/identities_and_differences/0"],
                "witness_node_ids": [
                    "global-interpretation-pressure",
                    "regime-indexed-mediator",
                ],
                "witness_edge_ids": ["interpretation-to-mediator"],
            },
        ],
        "explanatory_graph_transition": {
            "before_graph": before_graph,
            "after_graph": after_graph,
            "before_graph_digest": canonical_digest(before_graph),
            "after_graph_digest": canonical_digest(after_graph),
            "added_nodes": [mediator],
            "added_edges": edges,
            "new_explanatory_dependencies": [
                "Local construction now precedes global interpretation through an independently correctable regime indexed mediator."
            ],
        },
        "scope_conditions": [
            "The mediation applies only in the exact target regime represented by the frozen discovery charter."
        ],
        "transfer_obligations": [
            "Show that both source burdens retain their declared meaning under the proposed mediation map."
        ],
        "erasure_risks": [
            "An untyped common principle would erase the physical distinction between construction and interpretation."
        ],
        "failure_conditions": [
            "Demote the proposal if either source burden disappears from the explanatory graph transition."
        ],
    }
    return row


def _conceptual_judgment(
    candidate: Mapping[str, Any],
    packet: Mapping[str, Any],
    lens_family: str,
) -> Mapping[str, Any]:
    """Return content-warranted judgments with one blind, non-ID quality signal."""

    content = candidate["content"]
    strong = content.get("relation") == "synthesis"
    lens_language = {
        "ontological": {
            "question": "Which primitive commitments make the regime indexed mediator physically real rather than merely notational?",
            "tension": "The ontology must relate local construction and global interpretation without declaring their burdens identical.",
            "assumption": "The inherited ontology assumes that a shared vocabulary already supplies a shared explanatory carrier.",
            "analysis": "The ontological test asks whether the mediator adds a separately correctable primitive commitment to the target theory.",
            "handback": "Which target invariant distinguishes an ontologically real mediator from a convenient change of presentation?",
        },
        "dialectical": {
            "question": "Which opposition between construction and interpretation is genuinely mediated instead of hidden by synthesis?",
            "tension": "Construction demands a carrier while interpretation demands global coherence, and neither demand entails the other.",
            "assumption": "The inherited dialectic assumes disagreement vanishes when both sides receive one abstract description.",
            "analysis": "The dialectical test requires the candidate to preserve opposition and expose independently failing correction conditions.",
            "handback": "Which countermodel separates genuine mediation from a verbal compromise between incompatible physical burdens?",
        },
        "explanatory": {
            "question": "Which directional dependency makes the mediator increase understanding rather than add another descriptive layer?",
            "tension": "The explanation must compress recurrent failures while retaining their causal order and distinct failure modes.",
            "assumption": "The inherited explanation treats co occurrence of successful routes as evidence of one common mechanism.",
            "analysis": "The explanatory test asks whether removing the mediator changes a target question and its dependency structure.",
            "handback": "Which removal test shows that the new explanatory dependency materially changes the physics research programme?",
        },
    }[lens_family]
    paths = {
        "essential_relevance": "/target_pressures_addressed",
        "explanatory_mediation": "/mechanism_or_principle",
        "conceptual_depth": "/primitives",
        "unification_power": "/unification_claims/source_case_ids",
        "preserved_difference": "/unification_claims/preserved_differences",
        "generativity": "/formalization_seeds",
        "reflective_resilience": "/correction_conditions",
        "truth_aptness": "/residual_contradictions",
    }
    dimensions: dict[str, Any] = {}
    for dimension in DIMENSIONS:
        path = paths[dimension]
        value: Any = content
        for token in path.lstrip("/").split("/"):
            value = value[token]
        dimensions[dimension] = {
            "rating": "strong" if strong else "weak",
            "warrants": [
                {
                    "path": path,
                    "value_digest": canonical_digest(value),
                    "explanation": "The cited candidate bytes expose whether the proposal mediates the target pressures while preserving their correction conditions.",
                }
            ],
            "strongest_objection": "The proposed mediator may remain a relabelling unless removing it destroys a target relevant explanatory dependency.",
            "correction_test": "Remove the mediator and demote the proposal unless the exact physical research question loses explanatory structure.",
        }
    lens_warrants = []
    for path in (
        "/mechanism_or_principle",
        "/unification_claims/mediator/statement",
    ):
        value = content
        for token in path.lstrip("/").split("/"):
            value = value[token]
        lens_warrants.append(
            {
                "path": path,
                "value_digest": canonical_digest(value),
                "explanation": "This exact content identifies the mediator and its non substitutable explanatory role in the target physics.",
            }
        )
    return {
        "dimensions": dimensions,
        "deep_lens_analysis": {
            "lens_family": lens_family,
            "focal_question": lens_language["question"],
            "content_warrants": lens_warrants,
            "root_aporia_or_tension": lens_language["tension"],
            "inherited_assumption_exposed": lens_language["assumption"],
            "candidate_specific_analysis": lens_language["analysis"],
            "conceptual_consequence": {
                "kind": "tension_registered" if lens_family == "dialectical" else "relation_revised",
                "changed_paths": ["/mechanism_or_principle"],
                "statement": "Retain the mediation only while its target relevant dependency and preserved differences remain explicit.",
            },
            "physics_value_handback": {
                "target_pressure_paths": ["/target_pressures_addressed/0"],
                "changed_theory_question": lens_language["handback"],
                "relevance_limit": "This judgment redirects theoretical work but establishes no theorem, empirical law, or physical equivalence.",
            },
            "strongest_objection": "The mediation could still be decorative unless an independent countermodel removes its claimed dependency.",
            "correction_test": "Construct the removal countermodel and demote the proposal if the target question remains unchanged.",
        },
    }


def _ontological_judge(candidate: Mapping[str, Any], packet: Mapping[str, Any]) -> Mapping[str, Any]:
    return _conceptual_judgment(candidate, packet, "ontological")


def _dialectical_judge(candidate: Mapping[str, Any], packet: Mapping[str, Any]) -> Mapping[str, Any]:
    return _conceptual_judgment(candidate, packet, "dialectical")


def _explanatory_judge(candidate: Mapping[str, Any], packet: Mapping[str, Any]) -> Mapping[str, Any]:
    return _conceptual_judgment(candidate, packet, "explanatory")


def _write_json(workspace: Path, relative: str, payload: dict[str, Any]) -> Path:
    """Write deterministic fixture bytes inside the dispatcher trust boundary."""

    path = workspace / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    return path


def _live_providers(target_id: str, *, variant: str = "primary") -> dict[str, Any]:
    """Return six actually invoked fixture-provider search adapters."""

    providers: dict[str, Any] = {}
    for index, lane_type in enumerate(LANE_TYPES):

        def provider(request: dict[str, Any], *, index: int = index, lane_type: str = lane_type) -> dict[str, Any]:
            return {
                "provider": f"fixture-live-provider-{lane_type}",
                "index": f"fixture-live-index-{lane_type}",
                "execution_mode": "live",
                "status": "completed",
                "coverage_cutoff": "2026-07-21T23:59:59Z",
                "sources": [
                    {
                        "work_identity": f"{target_id}-work-{variant}-{lane_type}-{index}",
                        "title": f"Target-scoped {variant} result for {lane_type}",
                        "authors": [f"Fixture Author {index}"],
                        "publication_date": str(2020 + index),
                        "source_version": "v1",
                        "source_type": "primary",
                        "url": f"https://example.test/{target_id}/{variant}/{lane_type}",
                        "correction_status": "none_known",
                        "decision_relevant": True,
                        "claims": [f"Claim-level result {index} for {target_id}."],
                        "limitations": [f"Result {index} is limited to its declared fixture regime."],
                    }
                ],
            }

        providers[lane_type] = provider
    return providers


def _search_request(target_id: str, theory_digest: str) -> dict[str, Any]:
    return {
        "target_id": target_id,
        "claim_scope": "conceptual mechanisms and barriers",
        "theory_state_digest": theory_digest,
        "coverage_cutoff": "2026-07-21T23:59:59Z",
        "coverage_limits": ["Only the six named fixture-provider indexes were queried."],
        "search_lanes": [
            {
                "lane_type": lane_type,
                "queries": [f"{target_id} exact {lane_type.replace('_', ' ')}"],
                "inclusion_policy": "Include target-scoped primary results.",
                "exclusion_policy": "Exclude target mismatch and duplicate versions.",
            }
            for lane_type in LANE_TYPES
        ],
    }


def _mappings(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    """Causally map every decision-relevant source into a theory action."""

    return [
        {
            "source_id": source["source_id"],
            "theory_object_ids": [f"concept-source-{index}"],
            "object_kinds": ["concept", "schedule"],
            "relation": "reframes" if index == 0 else "leaves_open",
            "exact_claim": source["claims"][0],
            "source_limitation": source["limitations"][0],
            "conceptual_change": f"Reframe explanatory carrier {index} around the exact source limitation.",
            "event_type": "reframe" if index == 0 else "justified_no_change",
            "coverage_limits": list(snapshot["coverage_limits"]),
            "confidence": "high" if index == 0 else "medium",
        }
        for index, source in enumerate(snapshot["sources"])
    ]


def _charter(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "target_id": snapshot["target_id"],
        "target_statement": "Explain the target without replacing its exact quantifiers or regime.",
        "theory_state_digest": snapshot["theory_state_digest"],
        "root_tensions": [
            "Local witness structure does not explain global behavior.",
            "Recurring barriers lack one mechanism.",
        ],
        "target_commitments": ["Preserve exact quantifiers, regime, and nontrivial target identity."],
        "protected_successes": ["Recover the incumbent construction in its verified boundary regime."],
        "forbidden_target_drift": "No average-case, finite-only, or lexical proxy.",
    }


def _budget() -> dict[str, Any]:
    return {
        "budget_id": "canonical-cycle-budget",
        "wall_time_seconds": 5.0,
        "grace_period_seconds": 0.1,
        "cpu_seconds": 2.0,
        "memory_bytes": 256 * 1024 * 1024,
        "disk_bytes": 16 * 1024 * 1024,
        "network_bytes": 0,
        "token_count": 0,
        "request_count": 0,
        "cost_usd": 0.0,
    }


class CanonicalExercise:
    """Build one receipt-backed operator lineage over real core packet builders."""

    def __init__(
        self,
        tmp_path: Path,
        *,
        live: bool = True,
        experiment: bool = False,
        experiment_scenario: str | None = None,
        registry_routes: bool = False,
        bound_conceptual_evidence: bool = False,
        adjudication_outcome: str = "unique",
        commission_support: bool = False,
        literature_snapshot: dict[str, Any] | None = None,
        formal_seed_mode: str = "absent",
    ) -> None:
        self.workspace = tmp_path / "workspace"
        self.workspace.mkdir()
        self.state_root = tmp_path / "canonical-state"
        (
            self.literature_production_input_bundle,
            literature_production_input_path,
        ) = _portable_literature_production_input(self.workspace)
        self.target_id = self.literature_production_input_bundle["target_id"]
        self.run_id = "run-canonical-cycle"
        self.state_version = 0
        self.namespace = Namespace(self.target_id, self.run_id, "root", self.state_version)
        self.prior_state = initial_state(self.target_id, self.run_id)
        self.theory_digest = canonical_digest(self.prior_state)
        self.live = live
        self.experiment_scenario = experiment_scenario or (
            "misleading_toy_positive" if experiment else "none"
        )
        if self.experiment_scenario not in {
            "none",
            "neutral_inconclusive",
            "misleading_toy_positive",
            "registered_premise_falsifier",
            "operational_failure",
        }:
            raise ValueError(f"unknown experiment scenario: {self.experiment_scenario}")
        self.with_experiment = self.experiment_scenario != "none"
        self.registry_routes = registry_routes
        self.bound_conceptual_evidence = bound_conceptual_evidence
        if adjudication_outcome not in {"unique", "plural", "revise_all"}:
            raise ValueError(
                f"unknown adjudication outcome: {adjudication_outcome}"
            )
        self.adjudication_outcome = adjudication_outcome
        self.commission_support = commission_support
        if formal_seed_mode not in {
            "absent",
            "ready_exact",
            "untyped_ready",
            "typed_not_mature",
        }:
            raise ValueError(f"unknown formal seed mode: {formal_seed_mode}")
        if formal_seed_mode != "absent" and (
            not live or self.with_experiment or not registry_routes
        ):
            raise ValueError(
                "formal producer fixtures require live no-experiment registry routes"
            )
        self.formal_seed_mode = formal_seed_mode
        self._provided_literature_snapshot = copy.deepcopy(literature_snapshot)
        self.requests: list[dict[str, Any]] = []
        self.receipts: list[dict[str, Any]] = []
        self.roles: dict[str, Any] = {
            "literature_production_input_bundle": literature_production_input_path
        }
        self._counter = 0
        if registry_routes and not live:
            raise ValueError("registry routes reject local-only parallel investment by design")
        fixture_bindings = self._make_bindings()
        self._bindings = (
            [
                *registry_bindings(load_registry()),
                *[
                    binding
                    for binding in fixture_bindings
                    if binding.operator_id
                    in {
                        "source-routing-pre-map-policy-producer",
                        "source-routing-realization-producer",
                    }
                ],
            ]
            if registry_routes
            else fixture_bindings
        )
        self.dispatcher = DiscoveryOperatorDispatcher(
            self._bindings,
            workspace=self.workspace,
            receipt_store=ReceiptStore(self.workspace / "operator-receipts"),
        )
        self._build()

    def _bound_preference_evidence(
        self,
        *,
        stage: str,
        proposal_receipt: dict[str, Any],
        preferred_system_id: str,
    ) -> dict[str, Any]:
        """Build a genuine independently evaluated receipt for authority tests."""

        candidate = rich_candidate()
        candidate.update(
            {
                "target_id": self.target_id,
                "proposal_receipt_ids": [proposal_receipt["receipt_id"]],
                "proposal_invocation_id": proposal_receipt["invocation_id"],
                "proposer_identity": proposal_receipt["operator"]["operator_id"],
                "conceptual_system_id": preferred_system_id,
                "literature_snapshot": {
                    "snapshot_id": self.snapshot["snapshot_id"],
                    "target_id": self.target_id,
                    "status": "validated_current",
                    "content_digest": self.snapshot["content_digest"],
                },
                "source_relation_assessments": [
                    {
                        "source_id": self.snapshot["sources"][0]["source_id"],
                        "relation": "sharpens",
                        "reason": "The bound panel candidate explicitly consumes the frozen target literature.",
                    }
                ],
            }
        )
        receipt = evaluate_discovery_delta(
            candidate,
            evaluator_identity=f"bound-conceptual-panel.{stage}",
            evaluator_invocation_id=f"bound-conceptual-panel-{stage}",
            evaluator_version="structural-evaluator/1.0.0",
            genealogy=[],
        )
        assert receipt["creative_worth_decision"] == "prefer"
        return {
            "evaluation_role": "conceptual_gate",
            "preferred_system_id": preferred_system_id,
            "evaluation_receipt": receipt,
            "gate_findings": {
                gate_id: {
                    "status": "pass",
                    "basis": "Bound independent panel adjudication over the declared conceptual candidate.",
                }
                for gate_id in CONCEPTUAL_GATE_IDS
            },
            "stage_comparison": {
                "applicability": "applicable",
                "material": True,
                "reason": "The adjudicated synthesis changes typed mechanism and explanatory dependencies.",
            },
            "content_adjudication": {
                "authority": {
                    "panel_evidence_class": "correlated_internal_critique",
                }
            },
        }

    def _make_bindings(self) -> list[OperatorBinding]:
        kinds = {
            "source-routing-pre-map-policy-producer": "literature_assimilation",
            "source-routing-realization-producer": "literature_assimilation",
            "frontier-literature-assimilator": "literature_assimilation",
            "high-risk-hypothesis-forger": "hypothesis",
            "parallel-hypothesis-portfolio": "hypothesis",
            "reflective-conceptual-discovery": "theory",
            "reflective-theory-synthesizer": "theory",
            "dynamic-symbolic-simulation-experimenter": "support_probe",
            "local-reflective-incubator": "theory",
            "local-reflective-synthesizer": "theory",
            "blind-conceptual-preference-adjudicator": "evaluation",
        }
        return [
            OperatorBinding(
                operator_id=operator_id,
                version=(
                    "2.0.0"
                    if operator_id == "blind-conceptual-preference-adjudicator"
                    else "1.0.0"
                ),
                kind=kind,
                function=self._execute_operator,
                validators=(
                    ValidatorBinding(
                        validator_id=f"validator-{operator_id}",
                        version="1.0.0",
                        function=self._validate_operator,
                    ),
                ),
            )
            for operator_id, kind in kinds.items()
        ]

    def _envelope(self, request: dict[str, Any]) -> dict[str, Any]:
        return load_json(self.workspace / request["input_artifacts"][0]["path"])

    def _output(self, request: dict[str, Any], payload: dict[str, Any]) -> str:
        relative = request["declared_outputs"][0]
        _write_json(self.workspace, relative, payload)
        return relative

    def _execute_operator(self, request: dict[str, Any], workspace: Path) -> dict[str, Any]:
        operator_id = request["operator"]["operator_id"]
        envelope = self._envelope(request)
        if operator_id == "frontier-literature-assimilator":
            output = assimilate_literature(
                envelope["snapshot"],
                theory_state_digest=envelope["snapshot"]["theory_state_digest"],
                theory_mappings=envelope["theory_mappings"],
            )
        elif operator_id in {
            "source-routing-pre-map-policy-producer",
            "source-routing-realization-producer",
        }:
            output = copy.deepcopy(envelope["authority_artifact"])
        elif operator_id == "high-risk-hypothesis-forger":
            output = forge_high_risk_portfolio(
                envelope["charter"],
                envelope["literature_snapshot"],
                requested_count=10,
            )
        elif operator_id == "parallel-hypothesis-portfolio":
            portfolio = envelope["high_risk_portfolio"]
            manifest = build_parallel_manifest(
                portfolio,
                base_theory_state_version=self.state_version,
                branch_seeds=portfolio["parallel_branch_seeds"][:4],
                resource_budget={
                    "wall_seconds": 10,
                    "max_workers": 4,
                    "cost_units": 12,
                    "storage_bytes": 100_000,
                    "matched_budget_baseline_corner_coverage": 1,
                },
            )
            failed = set(envelope.get("failure_branch_ids", []))
            dissent = set(envelope.get("dissent_branch_ids", []))

            def worker(branch_request: dict[str, Any]) -> dict[str, Any]:
                if branch_request["branch_id"] in failed:
                    raise RuntimeError("deliberate branch-local operational failure")
                return {
                    "theory_delta": {
                        "delta_class": "conceptual_deepening",
                        "mechanism_key": f"matured-{branch_request['mechanism_key']}",
                        "changed_question": f"What invariant makes {branch_request['branch_id']} explain the shared obstruction?",
                    },
                    "claims": [
                        {
                            "proposition": "The branch-specific carrier changes the explanatory dependency.",
                            "stance": "oppose" if branch_request["branch_id"] in dissent else "support",
                        }
                    ],
                    "genealogy": [branch_request["hypothesis_id"]],
                    "conceptual_learning": True,
                    "is_dissent": branch_request["branch_id"] in dissent,
                }

            output = run_parallel_hypothesis_portfolio(manifest, worker)
        elif operator_id in {
            "reflective-conceptual-discovery",
            "reflective-theory-synthesizer",
        }:
            output, _unknowns = _reflective(operator_id, request, envelope)
        elif operator_id in {
            "local-reflective-incubator",
            "local-reflective-synthesizer",
        }:
            output = build_reflective_discovery_packet(envelope)
        elif operator_id == "dynamic-symbolic-simulation-experimenter":
            spec = validate_commissioned_experiment_spec(
                envelope["triage_request"],
                envelope["experiment_request"],
                envelope["experiment_spec"],
            )
            output = execute_experiment(spec, workspace / "experiment-runtime")
        elif operator_id == "blind-conceptual-preference-adjudicator":
            output, _unknowns = _conceptual_adjudication(request, envelope)
        else:  # pragma: no cover - binding table is closed.
            raise AssertionError(operator_id)
        relative = self._output(request, output)
        return {"artifacts": [{"path": relative}], "explicit_unknowns": []}

    def _validate_operator(
        self,
        request: dict[str, Any],
        artifacts: list[dict[str, Any]],
        workspace: Path,
    ) -> bool:
        operator_id = request["operator"]["operator_id"]
        output = load_json(workspace / artifacts[0]["path"])
        envelope = self._envelope(request)
        if operator_id == "frontier-literature-assimilator":
            validate_assimilation(output, snapshot=envelope["snapshot"])
        elif operator_id == "source-routing-pre-map-policy-producer":
            validate_payload(output, "source_routing_pre_map_policy.schema.json")
            assert output == envelope["authority_artifact"]
        elif operator_id == "source-routing-realization-producer":
            validate_payload(output, "source_routing_realization.schema.json")
            assert output == envelope["authority_artifact"]
        elif operator_id == "high-risk-hypothesis-forger":
            validate_high_risk_portfolio(output)
        elif operator_id == "parallel-hypothesis-portfolio":
            validate_parallel_portfolio(output)
        elif "reflective" in operator_id:
            validate_payload(output, "reflective_conceptual_discovery_packet.schema.json")
            validate_packet_invariants(output)
        elif operator_id == "dynamic-symbolic-simulation-experimenter":
            spec = validate_commissioned_experiment_spec(
                envelope["triage_request"],
                envelope["experiment_request"],
                envelope["experiment_spec"],
            )
            validate_experiment_receipt(output, spec, work_directory=workspace)
        elif operator_id == "blind-conceptual-preference-adjudicator":
            validate_adjudication_evidence(
                output,
                systems=envelope["systems"],
                reflection_rounds=envelope["reflection_rounds"],
                frozen_genealogy=envelope["frozen_genealogy"],
                candidate_bindings=envelope["candidate_bindings"],
                theory_state_digest=envelope["theory_state_digest"],
                literature_snapshot_digest=envelope["literature_snapshot_digest"],
                high_risk_portfolio_digest=envelope["high_risk_portfolio_digest"],
                proposer_receipt_ids=envelope["proposer_receipt_ids"],
                previous_evidence=envelope.get("previous_evidence"),
            )
        return True

    def dispatch(
        self,
        operator_id: str,
        kind: str,
        envelope: dict[str, Any],
        *,
        branch_id: str = "root",
        parameters: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any], str]:
        envelope = copy.deepcopy(envelope)
        request_parameters = copy.deepcopy(parameters or {})
        if operator_id in {
            "high-risk-hypothesis-forger",
            "parallel-hypothesis-portfolio",
            "reflective-conceptual-discovery",
            "reflective-theory-synthesizer",
            "local-reflective-incubator",
            "local-reflective-synthesizer",
            "blind-conceptual-preference-adjudicator",
        }:
            literature_projection = self.literature_production_input_bundle[
                "semantic_consumer_projection"
            ]
            envelope["literature_production_projection"] = copy.deepcopy(
                literature_projection
            )
            request_parameters[
                "literature_production_projection_digest"
            ] = literature_projection["projection_digest"]
        if hasattr(self, "source_routing_realization") and operator_id in {
            "high-risk-hypothesis-forger",
            "parallel-hypothesis-portfolio",
            "reflective-conceptual-discovery",
            "reflective-theory-synthesizer",
            "dynamic-symbolic-simulation-experimenter",
            "blind-conceptual-preference-adjudicator",
        }:
            envelope["source_routing_pre_map_policy"] = copy.deepcopy(
                self.source_routing_pre_map_policy
            )
            envelope["source_routing_realization"] = copy.deepcopy(
                self.source_routing_realization
            )
        self._counter += 1
        namespace = Namespace(self.target_id, self.run_id, branch_id, self.state_version)
        input_relative = f"operator-inputs/{self._counter:02d}-{operator_id}.json"
        output_relative = f"operator-outputs/{self._counter:02d}-{operator_id}.json"
        input_path = _write_json(self.workspace, input_relative, envelope)
        operator_version = next(
            (binding.version for binding in self._bindings
             if binding.operator_id == operator_id),
            None,
        )
        if operator_version is None:
            raise ContractError(
                "fixture cannot execute a retired or unregistered production "
                f"operator: {operator_id}"
            )
        request = build_operator_request(
            operator_id=operator_id,
            operator_version=operator_version,
            kind=kind,
            namespace=namespace,
            invocation_id=f"invocation-{self._counter:02d}-{operator_id}",
            input_artifacts=[artifact_descriptor(input_path, self.workspace, namespace)],
            declared_outputs=[output_relative],
            parameters=request_parameters,
            required=True,
        )
        receipt = self.dispatcher.dispatch(request)
        assert receipt["status"] == "succeeded", receipt.get("error")
        self.requests.append(request)
        self.receipts.append(receipt)
        return load_json(self.workspace / output_relative), receipt, output_relative

    def _reflection_request(
        self,
        portfolio: dict[str, Any],
        parallel: dict[str, Any],
        snapshot: dict[str, Any],
        assimilation_path: str,
    ) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "run_id": self.run_id,
            "branch_id": "root",
            "state_version": self.state_version,
            "prior_conceptual_state_ref": "state:0",
            "discovery_charter": {
                "essential_question": "What structure explains the shared obstruction without weakening the target?",
                "desired_understanding": "Explain recurrent route failures while preserving their real differences.",
                "bottleneck_diagnosis": "conceptual",
                "bottleneck_evidence": "Several mature routes fail at the same unrepresented interface.",
                "target_commitments": ["preserve the exact target", "preserve quantifier order"],
                "relevance_horizon": "A successful concept would reorganize multiple essential routes.",
                "incumbent_framework": "object-first local decomposition",
                "conceptual_opacity": "The shared obstruction appears only as unrelated local failures.",
                "non_claim_boundary": "No theorem, empirical law, or novelty is established by reflection.",
            },
            "conceptual_genealogy": {
                "inherited_concepts": ["local route", "witness", "barrier"],
                "historical_or_logical_formation": ["Local decomposition made route-specific failure primary."],
                "protected_successes": ["known special cases", "target quantifier order"],
                "rejected_or_retired_ancestors": ["one-size-fits-all bridge"],
                "hidden_assumptions": ["local objects are fundamental explanatory units"],
            },
            "literature_basis": {
                "selected_snapshot_id": snapshot["snapshot_id"],
                "snapshot_target_id": self.target_id,
                "selected_snapshot_digest": snapshot["content_digest"],
                "search_completed_utc": snapshot["search_completed_at"],
                # The local test intentionally demonstrates that the parent
                # cycle trusts search receipts over this upstream label.
                "freshness_status": "current",
                "search_receipt_ids": [row["lane_id"] for row in snapshot["lane_receipts"]],
                "assimilation_packet_ref": assimilation_path,
                "source_to_theory_delta_summary": ["Claim-level mappings reframed the explanatory carrier."],
                "literature_generated_questions": ["Can the carrier be represented without target drift?"],
                "coverage_limitations": list(snapshot["coverage_limits"]),
                "superseded_snapshot_ids": [],
            },
            "root_tensions": [
                {
                    "tension_id": "tension-shared-obstruction",
                    "opposed_commitments": ["route-local explanation", "shared recurrence"],
                    "strongest_form_of_each_side": ["Routes use distinct formal objects.", "The failure relation recurs."],
                    "minimal_incompatibility_or_missing_mediation": "No carrier relates route objects without identifying them.",
                    "regime": "all active routes",
                    "why_root_level": "The missing relation blocks explanation before local proof work.",
                }
            ],
            "high_risk_portfolio": portfolio,
            "parallel_portfolio": parallel,
            "operator_receipt_ids": [row["receipt_id"] for row in self.receipts],
            "explicit_unknowns": ["Whether the proposed mediation has a nontrivial formal model."],
        }

    def _adjudication_envelope(
        self,
        *,
        packet: Mapping[str, Any],
        proposal_receipt: Mapping[str, Any],
        stage_id: str,
        previous_evidence: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Freeze one complete blind-panel input around exact proposal bytes."""

        systems = copy.deepcopy(packet["conceptual_systems"])
        rounds = copy.deepcopy(packet["reflection_rounds"])
        genealogy: list[dict[str, Any]] = []
        proposer_receipt_ids = [str(proposal_receipt["receipt_id"])]
        source_bindings = build_adjudication_source_bindings(
            run_id=self.run_id,
            state_version=self.state_version,
            theory_state_digest=self.theory_digest,
            literature_snapshot_digest=self.snapshot["content_digest"],
            high_risk_portfolio_digest=self.portfolio["content_digest"],
            systems=systems,
            reflection_rounds=rounds,
            frozen_genealogy=genealogy,
            proposer_receipt_ids=proposer_receipt_ids,
        )
        blind_packet, candidate_bindings = build_blind_packet(
            target_id=self.target_id,
            stage_id=stage_id,
            target_charter={
                "root_tensions": [
                    str(row["minimal_incompatibility_or_missing_mediation"])
                    for row in packet["root_tensions"]
                ],
                "target_statement": packet["discovery_charter"][
                    "essential_question"
                ],
                "protected_successes": packet["discovery_charter"][
                    "target_commitments"
                ],
                "non_claims": [
                    packet["discovery_charter"]["non_claim_boundary"]
                ],
            },
            systems=systems,
            reflection_rounds=rounds,
            proposer_identity=str(proposal_receipt["operator"]["operator_id"]),
            source_bindings=source_bindings,
            counterbalance_seed=f"canonical-{stage_id}-seed",
        )
        created_at = str(proposal_receipt["completed_at"])

        def configured_judge(
            base_judge: Any,
        ) -> Any:
            if self.adjudication_outcome == "unique":
                return base_judge

            def judge(
                candidate: Mapping[str, Any],
                judge_packet: Mapping[str, Any],
            ) -> Mapping[str, Any]:
                judgment = copy.deepcopy(base_judge(candidate, judge_packet))
                rating = (
                    "strong"
                    if self.adjudication_outcome == "plural"
                    else "weak"
                )
                for dimension in judgment["dimensions"].values():
                    dimension["rating"] = rating
                return judgment

            return judge

        reports = [
            build_judge_report(
                blind_packet,
                adjudicator_id=f"canonical-{stage_id}-{lens}-judge",
                perspective=lens,
                lens_family=lens,
                version="1.0.0",
                judge=configured_judge(judge),
                created_at=created_at,
            )
            for lens, judge in (
                ("ontological", _ontological_judge),
                ("dialectical", _dialectical_judge),
                ("explanatory", _explanatory_judge),
            )
        ]
        return {
            "blind_packet": blind_packet,
            "judge_reports": reports,
            "systems": systems,
            "reflection_rounds": rounds,
            "frozen_genealogy": genealogy,
            "candidate_bindings": candidate_bindings,
            "theory_state_digest": self.theory_digest,
            "literature_snapshot_digest": self.snapshot["content_digest"],
            "high_risk_portfolio_digest": self.portfolio["content_digest"],
            "proposer_receipt_ids": proposer_receipt_ids,
            "previous_evidence": copy.deepcopy(previous_evidence),
            "previous_evidence_digest": (
                previous_evidence["evidence_digest"]
                if previous_evidence is not None
                else None
            ),
            "created_at": created_at,
        }

    def _build(self) -> None:
        if self._provided_literature_snapshot is not None:
            self.snapshot = copy.deepcopy(self._provided_literature_snapshot)
        elif self.live:
            self.snapshot = run_frontier_literature_cycle(
                _search_request(self.target_id, self.theory_digest),
                providers=_live_providers(self.target_id),
            )
        else:
            self.snapshot = build_demo_literature_snapshot(
                target_id=self.target_id, theory_state_digest=self.theory_digest
            )
        validate_snapshot(self.snapshot)
        snapshot_path = "external-search/frozen-snapshot.json"
        _write_json(self.workspace, snapshot_path, self.snapshot)
        self.roles["literature_snapshot"] = snapshot_path

        assimilation_envelope = {
            "snapshot": self.snapshot,
            "theory_mappings": _mappings(self.snapshot),
        }
        if self.live:
            source_ids = sorted(row["source_id"] for row in self.snapshot["sources"])
            self.source_routing_authority = {
                "capture_content_digest": canonical_digest(
                    {
                        "target_id": self.target_id,
                        "snapshot_id": self.snapshot["snapshot_id"],
                        "lane_receipts": self.snapshot["lane_receipts"],
                    }
                ),
                "acquisition_content_digest": self.snapshot["content_digest"],
                "tool_response_content_digests": sorted(
                    row["content_digest"] for row in self.snapshot["lane_receipts"]
                ),
                "version_graph_content_digests": [],
                "source_ids": source_ids,
                "source_routing_eligibility": {
                    source_id: "unverified_audit_only" for source_id in source_ids
                },
                "authority_boundary": (
                    "fixture provider observations and exact snapshot validators; "
                    "no provider authentication, source truth, novelty, or exhaustiveness"
                ),
            }
            self.acquisition_receipt = {
                "receipt_id": "receipt-validated-live-acquisition",
                "status": "succeeded",
                "identity": {
                    "target_id": self.target_id,
                    "run_id": self.run_id,
                    "state_version": self.state_version,
                },
                "completed_at": self.snapshot["search_completed_at"],
            }
            self.source_routing_algorithm_contracts = [
                {
                    "stage": stage,
                    "component_id": f"source-routing-{stage}.v1",
                    "algorithm_id": f"bounded-{stage}-algorithm.v1",
                    "config_id": f"source-routing-{stage}-config.v1",
                    "config_digest": canonical_digest(
                        {"stage": stage, "policy": "canonical-fixture-exact-v1"}
                    ),
                    "authority_class": "approved_internal_algorithm_registry",
                }
                for stage in ("warrant_validation", "claim_mapping", "assimilation")
            ]
            self.source_routing_pre_map_policy = build_source_routing_pre_map_policy(
                authority=self.source_routing_authority,
                snapshot=self.snapshot,
                target_id=self.target_id,
                run_id=self.run_id,
                state_version=self.state_version,
                acquisition_producer_receipt=self.acquisition_receipt,
                algorithm_contracts=self.source_routing_algorithm_contracts,
            )
            (
                self.source_routing_pre_map_policy,
                self.source_routing_pre_map_policy_receipt,
                policy_path,
            ) = self.dispatch(
                "source-routing-pre-map-policy-producer",
                "literature_assimilation",
                {
                    "authority_artifact": self.source_routing_pre_map_policy,
                },
                parameters={
                    "producer_role": "source_routing_pre_map_policy",
                    "artifact_id": self.source_routing_pre_map_policy[
                        "policy_id"
                    ],
                    "artifact_digest": canonical_digest(
                        self.source_routing_pre_map_policy
                    ),
                },
            )
            self.roles["source_routing_pre_map_policy"] = policy_path
            assimilation_envelope["source_routing_pre_map_policy"] = copy.deepcopy(
                self.source_routing_pre_map_policy
            )

        self.assimilation, self.assimilation_receipt, assimilation_path = self.dispatch(
            "frontier-literature-assimilator",
            "literature_assimilation",
            assimilation_envelope,
        )
        self.roles["literature_assimilation"] = assimilation_path
        if self.live:
            warrants = derive_source_routing_semantic_warrants(self.snapshot)
            requirements = source_routing_realization_requirements(
                policy=self.source_routing_pre_map_policy,
                snapshot=self.snapshot,
                validated_warrants=warrants,
                claim_mappings=self.assimilation["theory_mappings"],
                assimilation=self.assimilation,
            )
            stage_receipts = [
                {
                    "receipt_id": (
                        self.assimilation_receipt["receipt_id"]
                        if row["stage"] == "assimilation"
                        else f"receipt-source-routing-{row['stage']}"
                    ),
                    "stage": row["stage"],
                    "status": "succeeded",
                    "identity": {
                        "target_id": self.target_id,
                        "run_id": self.run_id,
                        "state_version": self.state_version,
                    },
                    "pre_map_policy_id": self.source_routing_pre_map_policy[
                        "policy_id"
                    ],
                    "pre_map_policy_digest": self.source_routing_pre_map_policy[
                        "policy_digest"
                    ],
                    "algorithm_contract_digest": row[
                        "algorithm_contract_digest"
                    ],
                    "started_at": self.assimilation_receipt["completed_at"],
                    "completed_at": self.assimilation_receipt["completed_at"],
                    "input_digest": row["input_digest"],
                    "output_digest": row["output_digest"],
                }
                for row in requirements
            ]
            self.source_routing_realization = build_source_routing_realization(
                policy=self.source_routing_pre_map_policy,
                authority=self.source_routing_authority,
                snapshot=self.snapshot,
                acquisition_producer_receipt=self.acquisition_receipt,
                algorithm_contracts=self.source_routing_algorithm_contracts,
                validated_warrants=warrants,
                claim_mappings=self.assimilation["theory_mappings"],
                assimilation=self.assimilation,
                stage_receipts=stage_receipts,
            )
            (
                self.source_routing_realization,
                self.source_routing_realization_receipt,
                realization_path,
            ) = self.dispatch(
                "source-routing-realization-producer",
                "literature_assimilation",
                {
                    "authority_artifact": self.source_routing_realization,
                },
                parameters={
                    "producer_role": "source_routing_realization",
                    "artifact_id": self.source_routing_realization[
                        "realization_id"
                    ],
                    "artifact_digest": canonical_digest(
                        self.source_routing_realization
                    ),
                },
            )
            self.roles["source_routing_realization"] = realization_path
        self.portfolio, self.portfolio_receipt, portfolio_path = self.dispatch(
            "high-risk-hypothesis-forger",
            "hypothesis",
            {
                "charter": _charter(self.snapshot),
                "literature_snapshot": self.snapshot,
                "assimilation_packet": self.assimilation,
            },
        )
        self.roles["high_risk_portfolio"] = portfolio_path
        seed_ids = [row["branch_id"] for row in self.portfolio["parallel_branch_seeds"][:4]]
        self.parallel, self.parallel_receipt, parallel_path = self.dispatch(
            "parallel-hypothesis-portfolio",
            "hypothesis",
            {
                "high_risk_portfolio": self.portfolio,
                "branch_seeds": self.portfolio["parallel_branch_seeds"][:4],
                "failure_branch_ids": [seed_ids[0]],
                "dissent_branch_ids": [seed_ids[-1]],
                "resource_budget": {
                    "wall_seconds": 10,
                    "max_workers": 4,
                    "cost_units": 12,
                    "storage_bytes": 100_000,
                    "matched_budget_baseline_corner_coverage": 1,
                },
            },
        )
        self.roles["parallel_portfolio"] = parallel_path

        reflection_portfolio = self.portfolio
        parent_operator = "reflective-conceptual-discovery"
        synthesis_operator = "reflective-theory-synthesizer"
        if not self.live:
            # The standalone reflective builder intentionally blocks local-only
            # active investment.  Build its structural-incubation projection
            # without laundering provisional rebase receipts into completion;
            # the canonical cycle will impose the stronger local restrictions.
            reflection_portfolio = copy.deepcopy(self.portfolio)
            for hypothesis in reflection_portfolio["hypotheses"]:
                hypothesis.pop("literature_rebase_receipt", None)
                hypothesis["concept_lifecycle_state"] = "incubating"
            parent_operator = "local-reflective-incubator"
            synthesis_operator = "local-reflective-synthesizer"
        reflection_request = self._reflection_request(
            reflection_portfolio, self.parallel, self.snapshot, assimilation_path
        )
        preview = build_reflective_discovery_packet(reflection_request)
        if self.live:
            reflection_request.update(
                {
                    "generation_mode": "operator_generated",
                    "conceptual_systems": [
                        _typed_unification(row)
                        for row in preview["conceptual_systems"]
                    ],
                    "reflection_rounds": preview["reflection_rounds"],
                }
            )
            for system in reflection_request["conceptual_systems"]:
                if self.formal_seed_mode == "ready_exact":
                    system["lifecycle_state"] = "formalization_ready"
                    system["formalization_seeds"] = [EXACT_FORMAL_SEED]
                elif self.formal_seed_mode == "untyped_ready":
                    system["lifecycle_state"] = "formalization_ready"
                    system["formalization_seeds"] = [
                        "Define an exact carrier, but this remains prose."
                    ]
                elif self.formal_seed_mode == "typed_not_mature":
                    system["formalization_seeds"] = [EXACT_FORMAL_SEED]
        self.parent_packet, self.parent_receipt, parent_path = self.dispatch(
            parent_operator, "theory", reflection_request
        )
        self.parent_adjudication_evidence = None
        if self.live:
            parent_adjudication_envelope = self._adjudication_envelope(
                packet=self.parent_packet,
                proposal_receipt=self.parent_receipt,
                stage_id="parent-conceptual-adjudication",
            )
            (
                self.parent_adjudication_evidence,
                self.parent_adjudication_receipt,
                parent_adjudication_path,
            ) = self.dispatch(
                "blind-conceptual-preference-adjudicator",
                "evaluation",
                parent_adjudication_envelope,
            )
            self.roles["parent_conceptual_adjudication"] = (
                parent_adjudication_path
            )

        parent_preference = (
            self.parent_adjudication_evidence["preference_set"]
            if self.parent_adjudication_evidence is not None
            else None
        )
        preferred_ids = (
            list(parent_preference["preferred_system_ids"])
            if parent_preference is not None
            else []
        )
        preferred_id = preferred_ids[0] if len(preferred_ids) == 1 else None
        programme_id = self.parent_packet["theoretical_programme"]["programme_id"]

        experiment_path = None
        if self.with_experiment:
            parent_programme_digest = canonical_digest(
                self.parent_packet["theoretical_programme"]
            )
            branch_id = self.parallel["branch_results"][0]["branch_id"]
            adapter = "exact"
            probe_role = "discriminator"
            model = {
                "operation": "equality",
                "left": "1/3 + 1/6",
                "right": "1/2",
            }
            resource_budget = _budget()
            theory_effect_contract = None
            registered_claim_kind = "model_consequence"
            registered_target_relation = "toy_or_proxy"
            if self.experiment_scenario == "neutral_inconclusive":
                adapter = "finite_model"
                model = {
                    "variables": {"x": [0, 1, 2, 3]},
                    "predicate": "x >= 0",
                    "quantifier": "forall",
                    "max_states": 2,
                }
            elif self.experiment_scenario == "registered_premise_falsifier":
                probe_role = "falsifier"
                model = {"operation": "equality", "left": "1", "right": "2"}
                registered_claim_kind = "theory_premise"
                registered_target_relation = "necessary_not_sufficient"
                theory_effect_contract = {
                    "tested_claim_id": "question-exact-carrier",
                    "tested_claim_kind": "theory_premise",
                    "target_relation": "necessary_not_sufficient",
                    "if_supported": "record_scoped_consistency_only",
                    "if_falsified": "request_registered_premise_revision",
                    "theory_identity_locked": True,
                    "automatic_theory_selection": False,
                    "automatic_proof": False,
                }
            elif self.experiment_scenario == "operational_failure":
                model = {"operation": "unsupported_operation"}
            registered_claim = {
                "claim_id": "question-exact-carrier",
                "claim_kind": registered_claim_kind,
                "target_relation": registered_target_relation,
                "statement": "Does the declared exact carrier identity hold?",
                "theory_programme_id": programme_id,
                "conceptual_system_ids": [preferred_id],
                "source_theory_programme_digest": parent_programme_digest,
                "source_reflection_packet_digest": self.parent_packet["packet_digest"],
            }
            registered_claim["claim_digest"] = canonical_digest(registered_claim)
            experiment_envelope = {
                "triage_request": {
                    "target_id": self.target_id,
                    "theory_programme_id": programme_id,
                    "source_theory_programme_digest": parent_programme_digest,
                    "source_reflection_packet_digest": self.parent_packet["packet_digest"],
                    "conceptual_system_ids": [preferred_id],
                    "registered_theory_claims": [registered_claim],
                    "theoretical_question_id": "question-exact-carrier",
                    "question": "Does the declared exact carrier identity hold?",
                    "programme_maturity": "mature",
                    "probe_role": probe_role,
                    "decision_effect": {
                        "if_supported": "retain the carrier premise",
                        "if_not_supported": "revise the carrier premise",
                    },
                    "expected_conceptual_change": "Decide whether the carrier remains primitive or must be retyped.",
                    "theory_generated_justification": "Reflection isolated this equality as the remaining discriminator.",
                    "candidate_methods": [adapter],
                    "state_version": self.state_version,
                },
                "experiment_request": {
                    "run_id": self.run_id,
                    "branch_id": branch_id,
                    "adapter": adapter,
                    "model": model,
                    "preregistration": {
                        "hypothesis": "the declared exact carrier equality holds",
                        "decision_rule": {"comparator": "==", "threshold": 1},
                        "stopping_rule": "stop after the declared exact evaluation",
                        "analysis_plan": "evaluate the frozen rational expression",
                        "registered_at": "2026-07-21T10:00:00Z",
                    },
                    "controls": [
                        {
                            "control_id": "control-rational-domain",
                            "variable": "arithmetic_domain",
                            "value": "rational",
                            "role": "held_fixed",
                        }
                    ],
                    "seed_policy": {"stochastic": False, "policy": "not_applicable"},
                    "resource_budget": resource_budget,
                    "transfer_boundary": "The certificate applies only to the declared equality and is not an unbounded theorem.",
                },
            }
            if theory_effect_contract is not None:
                experiment_envelope["experiment_request"][
                    "theory_effect_contract"
                ] = theory_effect_contract
            triage = triage_probe(experiment_envelope["triage_request"])
            assert triage["decision"] == "commission"
            self.experiment_spec = compile_experiment_spec(
                triage, experiment_envelope["experiment_request"]
            )
            experiment_envelope["experiment_spec"] = copy.deepcopy(
                self.experiment_spec
            )
            experiment_spec_path = "experiment-specs/commissioned-experiment.json"
            _write_json(
                self.workspace,
                experiment_spec_path,
                self.experiment_spec,
            )
            self.roles["experiment_spec"] = experiment_spec_path
            self.experiment_receipt, _, experiment_path = self.dispatch(
                "dynamic-symbolic-simulation-experimenter",
                "support_probe",
                experiment_envelope,
                branch_id=branch_id,
                parameters={"theory_commissioned": True},
            )
            self.roles["experiment_receipt"] = experiment_path

        synthesis_envelope = {
            **reflection_request,
            "prior_reflective_packet": self.parent_packet,
            "parallel_portfolio": self.parallel,
            "previous_evidence": copy.deepcopy(
                self.parent_adjudication_evidence
            ),
            "request_theory_support_probe": self.commission_support,
        }
        if self.with_experiment:
            synthesis_envelope["experiment_result"] = self.experiment_receipt
        self.synthesis_packet, self.synthesis_receipt, synthesis_path = self.dispatch(
            synthesis_operator, "theory", synthesis_envelope
        )
        self.roles["reflective_packets"] = [parent_path, synthesis_path]
        self.synthesis_adjudication_evidence = None
        if self.live:
            synthesis_adjudication_envelope = self._adjudication_envelope(
                packet=self.synthesis_packet,
                proposal_receipt=self.synthesis_receipt,
                stage_id="synthesis-conceptual-adjudication",
                previous_evidence=self.parent_adjudication_evidence,
            )
            (
                self.synthesis_adjudication_evidence,
                self.synthesis_adjudication_receipt,
                synthesis_adjudication_path,
            ) = self.dispatch(
                "blind-conceptual-preference-adjudicator",
                "evaluation",
                synthesis_adjudication_envelope,
            )
            self.roles["synthesis_conceptual_adjudication"] = (
                synthesis_adjudication_path
            )

    def cycle_kwargs(self) -> dict[str, Any]:
        return {
            "workspace": self.workspace,
            "state_root": self.state_root,
            "target_id": self.target_id,
            "run_id": self.run_id,
            "state_version": self.state_version,
            "operator_requests": self.requests,
            "operator_receipts": self.receipts,
            "artifact_roles": self.roles,
            "evaluator_identity": "independent-canonical-evaluator",
            "idempotency_key": "canonical-cycle-exercise",
            # The present-use clock is an explicit part of the canonical
            # request identity.  Replays inject the same instant rather than
            # silently renewing literature freshness from wall-clock time.
            "present_use_at": self.assimilation["resolution"]["evaluated_at"],
        }


def _commission_only_projection_inputs(
    exercise: CanonicalExercise,
) -> dict[str, Any]:
    """Finalize a post-adjudication theory anchor without executing a world."""

    authority = derive_conceptual_authority(
        target_id=exercise.target_id,
        run_id=exercise.run_id,
        state_version=exercise.state_version,
        literature_mode="active_current",
        parent_packet=exercise.parent_packet,
        synthesis_packet=exercise.synthesis_packet,
        parent_evidence=exercise.parent_adjudication_evidence,
        synthesis_evidence=exercise.synthesis_adjudication_evidence,
    )
    packet = finalize_post_adjudication_reflection(
        synthesis_packet=exercise.synthesis_packet,
        conceptual_authority=authority,
    )

    hypotheses = {
        row["hypothesis_id"]: row for row in exercise.portfolio["hypotheses"]
    }
    concept_ids_by_hypothesis = {
        hypothesis_id: cycle_runtime._hypothesis_concept_ids(hypothesis)
        for hypothesis_id, hypothesis in hypotheses.items()
    }
    all_systems = {
        row["system_id"]: row
        for source_packet in (exercise.parent_packet, packet)
        for row in source_packet["conceptual_systems"]
    }
    system_ids_by_hypothesis = {
        hypothesis_id: sorted(
            system_id
            for system_id in all_systems
            if hypothesis_id
            in cycle_runtime._system_hypotheses(
                system_id, all_systems, set(hypotheses)
            )
        )
        for hypothesis_id in hypotheses
    }
    source_pair = {
        "pre_map_policy": exercise.source_routing_pre_map_policy,
        "realization": exercise.source_routing_realization,
    }
    schedule = cycle_runtime._scheduler_projection(
        target_id=exercise.target_id,
        run_id=exercise.run_id,
        state_version=exercise.state_version,
        literature_mode="active_current",
        snapshot_id=exercise.snapshot["snapshot_id"],
        portfolio=exercise.portfolio,
        parallel=exercise.parallel,
        final_reflection=packet,
        concept_ids_by_hypothesis=concept_ids_by_hypothesis,
        system_ids_by_hypothesis=system_ids_by_hypothesis,
        proof_handoff=None,
        experiment_receipt=None,
        source_routing_precommit=source_pair,
        conceptual_authority=authority,
    )
    schedule["created_at"] = max(
        receipt["completed_at"] for receipt in exercise.receipts
    )
    producers_by_role = {
        "source_routing_pre_map_policy": [
            exercise.source_routing_pre_map_policy_receipt
        ],
        "source_routing_realization": [
            exercise.source_routing_realization_receipt
        ],
        "high_risk_portfolio": [exercise.portfolio_receipt],
        "parallel_portfolio": [exercise.parallel_receipt],
        "reflective_packets": [
            exercise.parent_receipt,
            exercise.synthesis_receipt,
        ],
        "parent_conceptual_adjudication": [
            exercise.parent_adjudication_receipt
        ],
        "synthesis_conceptual_adjudication": [
            exercise.synthesis_adjudication_receipt
        ],
    }
    return {
        "target_id": exercise.target_id,
        "run_id": exercise.run_id,
        "state_version": exercise.state_version,
        "prior_state": exercise.prior_state,
        "final_reflection": packet,
        "conceptual_authority": authority,
        "source_authority_pair": source_pair,
        "literature_production_input_bundle": copy.deepcopy(
            exercise.literature_production_input_bundle
        ),
        "producers_by_role": producers_by_role,
        "schedule": schedule,
    }


def _attach_formal_claim(exercise: CanonicalExercise) -> dict[str, Any]:
    """Dispatch one exact formal producer from sealed post-adjudication context."""

    context = _commission_only_projection_inputs(exercise)
    packet = context["final_reflection"]
    authority = context["conceptual_authority"]
    hypotheses = {
        row["hypothesis_id"]: row for row in exercise.portfolio["hypotheses"]
    }
    concept_ids_by_hypothesis = {
        hypothesis_id: cycle_runtime._hypothesis_concept_ids(hypothesis)
        for hypothesis_id, hypothesis in hypotheses.items()
    }
    all_systems = {
        row["system_id"]: row
        for source_packet in (exercise.parent_packet, packet)
        for row in source_packet["conceptual_systems"]
    }
    system_ids_by_hypothesis = {
        hypothesis_id: sorted(
            system_id
            for system_id in all_systems
            if hypothesis_id
            in cycle_runtime._system_hypotheses(
                system_id, all_systems, set(hypotheses)
            )
        )
        for hypothesis_id in hypotheses
    }
    valid_branch_ids = {
        row["branch_id"] for row in exercise.parallel["branch_results"]
    }
    branch_by_hypothesis = {
        row["hypothesis_id"]: row["branch_id"]
        for row in exercise.parallel["branch_requests"]
        if row["branch_id"] in valid_branch_ids
    }
    candidates: list[tuple[int, str, str, dict[str, Any], dict[str, Any]]] = []
    preferred_ids = set(authority["preferred_system_ids"])
    for source_row in formalization_seed_rows(packet):
        source_system_id = source_row["row"]["system_id"]
        if source_system_id not in preferred_ids:
            continue
        for hypothesis_id in cycle_runtime._system_hypotheses(
            source_system_id, all_systems, set(hypotheses)
        ):
            branch_id = branch_by_hypothesis.get(hypothesis_id)
            if branch_id is None:
                continue
            branch_binding = {
                "branch_id": branch_id,
                "hypothesis_id": hypothesis_id,
                "concept_ids": concept_ids_by_hypothesis[hypothesis_id],
                "conceptual_system_ids": system_ids_by_hypothesis[hypothesis_id],
            }
            branch_preferred_count = len(
                preferred_ids.intersection(branch_binding["conceptual_system_ids"])
            )
            candidates.append(
                (
                    -branch_preferred_count,
                    branch_id,
                    source_system_id,
                    source_row,
                    branch_binding,
                )
            )
    if not candidates:
        raise AssertionError("fixture has no preferred seed on a validated branch")
    _, _, source_system_id, source_row, branch_binding = sorted(
        candidates,
        key=lambda row: (row[0], row[1], row[2], row[3]["semantic_id"]),
    )[0]
    synthesis_request = next(
        row
        for row in exercise.requests
        if row["request_id"] == exercise.synthesis_receipt["request_id"]
    )
    evaluated_at = dt.datetime.fromisoformat(
        exercise.assimilation["resolution"]["evaluated_at"].replace(
            "Z", "+00:00"
        )
    )
    present_freshness = resolve_present_literature_freshness(
        exercise.assimilation,
        now=evaluated_at,
    )
    freshness = cycle_runtime._freshness_policy(
        exercise.snapshot,
        exercise.assimilation,
        present_freshness,
    )
    literature_authority = {
        "authority_kind": "validated_target_scoped_literature_snapshot",
        "snapshot_id": exercise.snapshot["snapshot_id"],
        "snapshot_digest": exercise.snapshot["content_digest"],
        "literature_production_projection_digest": exercise.literature_production_input_bundle[
            "semantic_consumer_projection"
        ]["projection_digest"],
        "source_routing_pre_map_policy_digest": exercise.source_routing_pre_map_policy[
            "policy_digest"
        ],
        "source_routing_realization_digest": exercise.source_routing_realization[
            "realization_digest"
        ],
        "basis_status": "current",
        "consume_before": freshness["consume_before"],
        "present_use_evaluated_at": freshness["present_use_evaluated_at"],
        "present_use_reason": freshness["present_use_reason"],
    }
    producer_input = build_formal_claim_producer_input(
        workspace=exercise.workspace,
        source_producer_request=synthesis_request,
        source_producer_receipt=exercise.synthesis_receipt,
        finalized_reflection=packet,
        conceptual_authority=authority,
        branch_binding=branch_binding,
        concept_id=branch_binding["concept_ids"][0],
        source_semantic_row_id=source_row["semantic_id"],
        literature_authority=literature_authority,
    )
    output, receipt, output_path = exercise.dispatch(
        "formal-claim-producer",
        "proof",
        producer_input,
        branch_id=branch_binding["branch_id"],
    )
    exercise.roles["formal_claim_output"] = output_path
    return {
        "producer_input": producer_input,
        "output": output,
        "request": exercise.requests[-1],
        "receipt": receipt,
        "branch_binding": branch_binding,
        "source_row": source_row,
        "source_system_id": source_system_id,
        "finalized_reflection": packet,
        "conceptual_authority": authority,
    }


def _generic_projection_with_component_extension(
    projection: Mapping[str, Any], component_kind: str
) -> dict[str, Any]:
    values = {
        row["component_kind"]: copy.deepcopy(row["value"])
        for row in projection["components"]
    }
    values[component_kind]["adversarial_extension"] = {
        "attempt": "fully_rehashed_component_substitution"
    }
    if component_kind == "registered_claim":
        values[component_kind]["claim_digest"] = canonical_digest(
            values[component_kind], exclude_keys=("claim_digest",)
        )
    return _rehash_projection_with_values(projection, values)


def _rehash_projection_with_values(
    projection: Mapping[str, Any], values: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    """Build a generically valid projection after a semantic substitution."""

    return build_experiment_authority_projection(
        target_id=projection["target_id"],
        run_id=projection["run_id"],
        prior_state_version=projection["prior_state_version"],
        committed_ancestor=values["committed_ancestor"],
        theory_programme=values["theory_programme"],
        reflection_packet=values["reflection_packet"],
        conceptual_systems=values["conceptual_systems"],
        genealogy=values["genealogy"],
        source_authority=values["source_authority"],
        registered_claim=values["registered_claim"],
        generator_authority=values["generator_authority"],
        adjudication_authority=values["adjudication_authority"],
        schedule=values["schedule"],
    )


def test_cycle_derives_and_replays_the_exact_world_authority_projection(
    tmp_path: Path,
) -> None:
    exercise = CanonicalExercise(
        tmp_path, live=True, experiment=False, commission_support=True
    )
    inputs = _commission_only_projection_inputs(exercise)

    projection = build_canonical_world_authority_projection(**inputs)

    assert [
        row["component_kind"] for row in projection["components"]
    ] == list(AUTHORITY_COMPONENT_ORDER)
    assert replay_canonical_world_authority_projection(
        projection, **inputs
    ) == projection
    values = {
        row["component_kind"]: row["value"] for row in projection["components"]
    }
    assert values["registered_claim"]["source_reflection_packet_digest"] == inputs[
        "final_reflection"
    ]["packet_digest"]
    assert values["conceptual_systems"]["ordered_system_ids"] == inputs[
        "conceptual_authority"
    ]["preferred_system_ids"]
    programme_probes = [
        action
        for action in values["schedule"]["actions"]
        if action["kind"] == "probe"
        and action["priority_class"] == "theory_subordinate_support"
    ]
    assert len(programme_probes) == 1
    assert programme_probes[0]["payload"]["permitted_direct_effect"] == "none"
    assert {
        "no_automatic_theory_selection",
        "no_direct_proof_authority",
        "no_direct_physics_result_authority",
        "requires_post_result_reflection",
    }.issubset(programme_probes[0]["restrictions"])


@pytest.mark.parametrize("component_kind", AUTHORITY_COMPONENT_ORDER)
def test_cycle_replay_rejects_every_fully_rehashed_component_substitution(
    tmp_path: Path,
    component_kind: str,
) -> None:
    exercise = CanonicalExercise(
        tmp_path, live=True, experiment=False, commission_support=True
    )
    inputs = _commission_only_projection_inputs(exercise)
    projection = build_canonical_world_authority_projection(**inputs)
    substituted = _generic_projection_with_component_extension(
        projection, component_kind
    )

    with pytest.raises(
        ContractError,
        match=(
            "caller-supplied world authority projection differs from "
            "cycle-derived state"
        ),
    ):
        replay_canonical_world_authority_projection(substituted, **inputs)


def test_cycle_projection_rejects_unsealed_packet_null_inflation_and_receipt_reorder(
    tmp_path: Path,
) -> None:
    exercise = CanonicalExercise(
        tmp_path, live=True, experiment=False, commission_support=True
    )
    inputs = _commission_only_projection_inputs(exercise)

    unsealed_packet = copy.deepcopy(inputs)
    unsealed_packet["final_reflection"]["support_probe"][
        "theoretical_question"
    ] = "A caller-replaced question."
    with pytest.raises(ContractError, match="self-digest is invalid"):
        build_canonical_world_authority_projection(**unsealed_packet)

    inflated = copy.deepcopy(inputs)
    inflated["conceptual_authority"]["creativity_authority"] = {
        "invented": True
    }
    with pytest.raises(ContractError, match="conceptual-merit authority"):
        build_canonical_world_authority_projection(**inflated)

    reordered = copy.deepcopy(inputs)
    reordered["producers_by_role"]["reflective_packets"].reverse()
    with pytest.raises(ContractError, match="wrong ordered producers"):
        build_canonical_world_authority_projection(**reordered)


def test_cycle_projection_preserves_plural_authority_and_rejects_index_zero_collapse(
    tmp_path: Path,
) -> None:
    exercise = CanonicalExercise(
        tmp_path,
        live=True,
        experiment=False,
        adjudication_outcome="plural",
        commission_support=True,
    )
    inputs = _commission_only_projection_inputs(exercise)
    projection = build_canonical_world_authority_projection(**inputs)
    preferred_ids = inputs["conceptual_authority"]["preferred_system_ids"]
    assert len(preferred_ids) > 1
    values = {
        row["component_kind"]: copy.deepcopy(row["value"])
        for row in projection["components"]
    }
    assert values["conceptual_systems"]["ordered_system_ids"] == preferred_ids
    assert values["theory_programme"]["conceptual_system_ids"] == preferred_ids
    assert values["registered_claim"]["conceptual_system_ids"] == preferred_ids

    values["conceptual_systems"]["ordered_system_ids"] = [preferred_ids[0]]
    values["conceptual_systems"]["systems"] = [
        values["conceptual_systems"]["systems"][0]
    ]
    values["theory_programme"]["conceptual_system_ids"] = [preferred_ids[0]]
    values["registered_claim"]["conceptual_system_ids"] = [preferred_ids[0]]
    values["registered_claim"]["claim_digest"] = canonical_digest(
        values["registered_claim"], exclude_keys=("claim_digest",)
    )
    collapsed = _rehash_projection_with_values(projection, values)
    with pytest.raises(ContractError, match="cycle-derived state"):
        replay_canonical_world_authority_projection(collapsed, **inputs)


def _proof_request(exercise: CanonicalExercise) -> dict[str, Any]:
    branch = exercise.parallel["branch_results"][0]["branch_id"]
    request = next(row for row in exercise.parallel["branch_requests"] if row["branch_id"] == branch)
    return {
        "formalization_ready": True,
        "branch_id": branch,
        "hypothesis_id": request["hypothesis_id"],
        "conjecture_id": "conjecture-exact-carrier",
        "statement": "1/3 + 1/6 = 1/2",
        "proof_adapter": "exact",
        "proof_payload": {"operation": "equality", "left": "1/3 + 1/6", "right": "1/2"},
        "resource_budget": _budget(),
    }


@pytest.mark.parametrize(
    (
        "live",
        "adjudication_outcome",
        "expected_status",
        "expected_decision",
        "expected_preferred_count",
    ),
    [
        (True, "unique", "sealed_unique", "prefer_unique", 1),
        (True, "plural", "sealed_plural", "retain_plural_nondominated", 6),
        (
            True,
            "revise_all",
            "sealed_revise_all_diagnostic_only",
            "revise_all",
            0,
        ),
        (
            False,
            "unique",
            "absent_diagnostic_only",
            "absent_local",
            0,
        ),
    ],
)
def test_total_set_valued_authority_matrix(
    tmp_path: Path,
    live: bool,
    adjudication_outcome: str,
    expected_status: str,
    expected_decision: str,
    expected_preferred_count: int,
) -> None:
    exercise = CanonicalExercise(
        tmp_path,
        live=live,
        experiment=False,
        adjudication_outcome=adjudication_outcome,
    )
    result = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    authority = result["conceptual_authority"]
    assert authority["status"] == expected_status
    assert authority["decision"] == expected_decision
    assert len(authority["preferred_system_ids"]) == expected_preferred_count
    authority_ids = [
        *authority["preferred_system_ids"],
        *authority["diagnostic_synthesis_system_ids"],
    ]
    assert [row["system_id"] for row in authority["system_outcomes"]] == authority_ids
    assert all(
        row["component_programme"]["conceptual_system_id"] == row["system_id"]
        and row["understanding_delta"]["conceptual_system_id"]
        == row["system_id"]
        for row in authority["system_outcomes"]
    )
    for field in (
        "philosophical_depth_authority",
        "understanding_gain_authority",
        "unification_power_authority",
        "creativity_authority",
        "relevance_authority",
    ):
        assert authority[field] is None
    for field in (
        "external_depth_validation_status",
        "external_understanding_validation_status",
        "external_unification_validation_status",
        "external_creativity_validation_status",
        "external_relevance_validation_status",
    ):
        assert authority[field] == "unavailable"
    if live:
        assert result["source_routing_pre_map_policy"] == (
            exercise.source_routing_pre_map_policy
        )
        assert result["source_routing_realization"] == (
            exercise.source_routing_realization
        )
        assert sum(
            edge["producer_operator_id"]
            == "blind-conceptual-preference-adjudicator"
            for edge in result["feedback_edges"]
        ) == 2
    else:
        assert result["source_routing_pre_map_policy"] is None
        assert result["source_routing_realization"] is None
        assert authority["diagnostic_synthesis_system_ids"] == (
            exercise.synthesis_packet["provisional_synthesis"][
                "diagnostic_synthesis_system_ids"
            ]
        )
        assert all(
            edge["producer_operator_id"]
            != "blind-conceptual-preference-adjudicator"
            for edge in result["feedback_edges"]
        )
    if authority["preference_authorized"] is False:
        if live:
            assert all(
                "no_active_investment" in action["restrictions"]
                for action in result["schedule"]["actions"]
                if action["branch_ids"]
            )
        else:
            assert result["schedule"]["literature_investment_blocked"] is True


def test_canonical_path_quarantines_singular_and_v1_helpers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import agentic.discovery.cycle as cycle_module

    assert not hasattr(
        cycle_module, "_validate_source_routing_precommit_execution"
    )

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("quarantined legacy helper became reachable")

    for symbol in (
        "_integrate_parallel_theory",
        "_evaluation_candidate",
        "_build_experiment_world_semantics",
    ):
        monkeypatch.setattr(cycle_module, symbol, forbidden)
    for name, live in (("active", True), ("local", False)):
        root = tmp_path / name
        root.mkdir()
        exercise = CanonicalExercise(root, live=live, experiment=False)
        result = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
        assert result["experiment_world_semantics"] is None

    root = tmp_path / "legacy-source"
    root.mkdir()
    exercise = CanonicalExercise(root, live=True, experiment=False)
    roles = copy.deepcopy(exercise.roles)
    roles["source_routing_precommit"] = roles.pop(
        "source_routing_pre_map_policy"
    )
    roles.pop("source_routing_realization")
    kwargs = exercise.cycle_kwargs()
    kwargs["artifact_roles"] = roles
    with pytest.raises(
        ContractError,
        match="legacy post-assimilation source-routing precommit|policy-realization",
    ):
        run_canonical_discovery_cycle(**kwargs)


@pytest.mark.skip(
    reason="historical post-execution experiment-v1 integration is quarantined; v2 commission tests own this surface"
)
def test_active_six_operator_cycle_commits_semantic_feedback_and_branch_integrated_theory(
    tmp_path: Path,
) -> None:
    exercise = CanonicalExercise(
        tmp_path,
        live=True,
        experiment=True,
        registry_routes=True,
    )
    assert {row["operator"]["operator_id"] for row in exercise.receipts} == SIX_OPERATORS
    result = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    assert result["committed_state_version"] == 1
    assert result["literature_basis"]["mode"] == "active_current"
    assert result["parallel_outcome"]["canonical_cas_commits"] == 1
    assert len(result["parallel_outcome"]["valid_branch_ids"]) == 3
    assert result["parallel_outcome"]["failed_or_invalid_attempt_ids"]
    assert result["parallel_outcome"]["retained_dissent_ids"]

    feedback_by_operator = {row["producer_operator_id"]: row for row in result["feedback_edges"]}
    assert set(feedback_by_operator) == SIX_OPERATORS
    events = {row["event_id"]: row for row in result["events"]}
    for edge in result["feedback_edges"]:
        validate_payload(edge, "discovery_feedback_edge.schema.json")
        event = events[edge["consumer_event_id"]]
        assert edge["consumer_event_hash"] == event["event_hash"]
        assert edge["producer_receipt_id"] in event["source_receipt_ids"]
        assert edge["committed_state_generation"] == 1
        assert edge["producer_output_artifacts"]
        assert event["payload"].get("kind") != "operator_output_consumed"
        assert edge["semantic_event_projections"]
        for projection in edge["semantic_event_projections"]:
            projected_event = events[projection["consumer_event_id"]]
            assert projection["consumer_event_hash"] == projected_event["event_hash"]
            assert projected_event["payload"]["semantic_projection"] == {
                "semantic_kind": projection["semantic_kind"],
                "semantic_id": projection["semantic_id"],
                "row_digest": projection["row_digest"],
                "source_output_path": projection["output_path"],
            }
    evidence = result["operator_evidence"]
    assert len(evidence["input_bindings"]) == len(exercise.requests)
    assert evidence["validator_authority_bindings"]
    assert len({row["sealed_path"] for row in evidence["input_bindings"]}) == len(
        evidence["input_bindings"]
    )

    state = DiscoveryTransactionStore(
        exercise.state_root, target_id=exercise.target_id, run_id=exercise.run_id
    ).read_state()
    assert state is not None
    snapshot_record = state["literature_snapshots"][exercise.snapshot["snapshot_id"]]
    assert len(snapshot_record["search_lane_receipt_ids"]) >= 6
    assert snapshot_record["snapshot_validator_receipt_ids"]
    integrated_id = result["parallel_outcome"]["branch_integrated_preferred_system_id"]
    integrated = state["conceptual_systems"][integrated_id]
    assert "Validated branch mechanisms" in integrated["mechanism_or_principle"]
    assert any("Retained dissenting branch" in row for row in integrated["residual_contradictions"])
    assert all(row["promotion_decision"] == "not_requested" for row in result["evaluation_receipts"])
    assert result["experiment_assimilation"]["theory_selected"] is False
    assert result["experiment_assimilation"]["proof_authorized"] is False
    reflection_receipt = result["experiment_reflection_receipt"]
    assert reflection_receipt is not None
    assert result["experiment_assimilation"]["post_result_reflection_receipt_ids"] == [
        reflection_receipt["reflection_receipt_id"]
    ]
    assert reflection_receipt["experiment_binding"]["receipt_id"] == (
        exercise.experiment_receipt["receipt_id"]
    )
    assert reflection_receipt["synthesis_binding"]["operator_receipt_id"] == (
        exercise.synthesis_receipt["receipt_id"]
    )
    assert reflection_receipt["synthesis_binding"]["experiment_result_consumed"] is True
    assert reflection_receipt["authority_boundary"] == {
        "experiment_subordinate_to_theory": True,
        "theory_identity_changed": False,
        "ontology_mutation_authorized": False,
        "theory_selected": False,
        "proof_authorized": False,
        "physical_target_support_authorized": False,
        "automatic_evidence_relation_authorized": False,
        "schedule_mutation_authorized": False,
    }
    validate_experiment_reflection_receipt(
        reflection_receipt,
        exercise.experiment_spec,
        exercise.experiment_receipt,
        exercise.parent_packet,
        exercise.synthesis_packet,
        exercise.synthesis_receipt,
        work_directory=exercise.workspace,
    )
    assert result["proof_handoff"] is None
    assert result["conceptual_authority"]["fallback_disposition"] == "maturation_only"
    assert result["conceptual_authority"]["internal_correlated_rubric_pass"] is False
    assert result["conceptual_authority"]["external_depth_validation_status"] == "unavailable"
    assert result["conceptual_authority"]["external_understanding_validation_status"] == "unavailable"
    assert "depth_claim_authorized" not in result["conceptual_authority"]
    assert "understanding_claim_authorized" not in result["conceptual_authority"]
    assert all(action["kind"] != "probe" for action in result["schedule"]["actions"])
    assert all(action["kind"] != "prove" for action in result["schedule"]["actions"])

    commit = next((exercise.state_root / "targets" / exercise.target_id / "runs" / exercise.run_id / "commits").iterdir())
    manifest = load_json(commit / "manifest.json")
    manifest_digests = {Path(row["path"]).name: row["sha256"] for row in manifest["artifacts"]}
    assert result["artifact_digests"]["feedback_edges"] == manifest_digests["feedback-edges.json"]
    committed_reflection_path = next(
        commit.rglob("experiment-reflection-receipt.json")
    )
    assert load_json(committed_reflection_path) == reflection_receipt
    assert result["manifest_digest"].startswith("sha256:")
    assert Path(result["transaction_root"]) == exercise.state_root.resolve()
    assert Path(result["commit_path"]) == commit.resolve()
    assert Path(result["manifest_path"]) == (commit / "manifest.json").resolve()

    forged_reflection = copy.deepcopy(reflection_receipt)
    forged_reflection["typed_delta"]["review_reason"] = "forged_post_result_judgment"
    forged_reflection["typed_delta"]["delta_digest"] = canonical_digest(
        forged_reflection["typed_delta"], exclude_keys=("delta_digest",)
    )
    forged_reflection["reflection_digest"] = canonical_digest(
        forged_reflection, exclude_keys=("reflection_digest",)
    )
    with pytest.raises(ExperimentReceiptError) as reflection_error:
        validate_experiment_reflection_receipt(
            forged_reflection,
            exercise.experiment_spec,
            exercise.experiment_receipt,
            exercise.parent_packet,
            exercise.synthesis_packet,
            exercise.synthesis_receipt,
            work_directory=exercise.workspace,
        )
    assert reflection_error.value.reason_code == "experiment_reflection_receipt_invalid"


def test_live_status_booleans_cannot_replace_digest_bound_lane_validator_evidence(
    tmp_path: Path,
) -> None:
    exercise = CanonicalExercise(tmp_path, live=True, experiment=False)
    tampered = copy.deepcopy(exercise.snapshot)
    # Snapshot-validator IDs are outside the snapshot content digest by design. The parent
    # therefore has to prove the derived content-to-validator relationship in
    # addition to accepting the lane's live/completed status booleans.
    tampered["validator_receipts"][0]["receipt_id"] = "validator.hand-authored-live-claim"
    _write_json(exercise.workspace, exercise.roles["literature_snapshot"], tampered)
    with pytest.raises(ContractError, match="snapshot validator receipt identity mismatch"):
        run_canonical_discovery_cycle(**exercise.cycle_kwargs())


def test_cycle_needs_no_experiment_and_no_probe_needed_continues_reflection(tmp_path: Path) -> None:
    exercise = CanonicalExercise(tmp_path, live=True, experiment=False)
    result = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    assert result["experiment_assimilation"]["present"] is False
    assert result["proof_handoff"] is None
    assert all(action["kind"] != "probe" for action in result["schedule"]["actions"])
    assert any(action["kind"] == "reflect" for action in result["schedule"]["actions"])
    assert result["schedule"]["literature_investment_blocked"] is False


def test_ready_registered_formal_claim_binds_one_actual_producer_action(
    tmp_path: Path,
) -> None:
    exercise = CanonicalExercise(
        tmp_path,
        live=True,
        experiment=False,
        registry_routes=True,
        formal_seed_mode="ready_exact",
    )
    formal = _attach_formal_claim(exercise)
    output = formal["output"]
    result = run_canonical_discovery_cycle(**exercise.cycle_kwargs())

    assert output["status"] == "ready"
    assert output["formal_claim"] == EXACT_FORMAL_DIRECTIVE["formal_claim"]
    assert output["formal_claim_digest"] == canonical_digest(
        EXACT_FORMAL_DIRECTIVE["formal_claim"]
    )
    assert output["proof_adapter"] == "exact"
    assert output["execution_plan"] == {"kind": "builtin_worker"}
    prove = [
        action for action in result["schedule"]["actions"]
        if action["kind"] == "prove"
    ]
    assert len(prove) == 1
    assert prove[0]["branch_ids"] == [output["branch_id"]]
    binding = prove[0]["payload"]["formal_claim_binding"]
    assert binding["producer_receipt_id"] == formal["receipt"]["receipt_id"]
    assert binding["producer_receipt_id"] != output["source_operator_receipt_id"]
    assert output["source_operator_receipt_id"] == exercise.synthesis_receipt[
        "receipt_id"
    ]
    assert binding["producer_request_id"] == formal["request"]["request_id"]
    assert binding["output_id"] == output["output_id"]
    assert binding["output_digest"] == output["content_digest"]
    assert binding["formal_claim_digest"] == output["formal_claim_digest"]
    assert binding["execution_plan_digest"] == output["execution_plan_digest"]
    edge = next(
        row for row in result["feedback_edges"]
        if row["producer_operator_id"] == "formal-claim-producer"
    )
    assert edge["producer_receipt_id"] == formal["receipt"]["receipt_id"]
    role_binding = next(
        row for row in result["operator_evidence"]["role_bindings"]
        if row["role"] == "formal_claim_output"
    )
    assert role_binding["producer_receipt_id"] == formal["receipt"]["receipt_id"]
    assert result["proof_handoff"] is None
    assert result["conceptual_authority"]["proof_ready"] is False


@pytest.mark.parametrize(
    ("formal_seed_mode", "reason_code"),
    [
        ("untyped_ready", "untyped_formalization_seed"),
        ("typed_not_mature", "source_not_formalization_ready"),
    ],
)
def test_not_ready_registered_formal_claim_is_total_and_schedules_no_prove(
    tmp_path: Path,
    formal_seed_mode: str,
    reason_code: str,
) -> None:
    exercise = CanonicalExercise(
        tmp_path,
        live=True,
        experiment=False,
        registry_routes=True,
        formal_seed_mode=formal_seed_mode,
    )
    formal = _attach_formal_claim(exercise)
    output = formal["output"]
    result = run_canonical_discovery_cycle(**exercise.cycle_kwargs())

    assert output["status"] == "not_ready"
    assert output["rejection_reason"]["code"] == reason_code
    assert output["formal_claim"] is None
    assert output["formal_claim_digest"] is None
    assert output["proof_adapter"] is None
    assert output["execution_plan"] is None
    assert output["execution_plan_digest"] is None
    assert all(
        action["kind"] != "prove" for action in result["schedule"]["actions"]
    )
    assert all(
        "formal_claim_binding" not in action.get("payload", {})
        for action in result["schedule"]["actions"]
    )
    assert sum(
        edge["producer_operator_id"] == "formal-claim-producer"
        for edge in result["feedback_edges"]
    ) == 1
    assert result["proof_handoff"] is None
    assert result["conceptual_authority"]["proof_ready"] is False


def test_plural_preference_separates_global_ancestry_from_one_source_system(
    tmp_path: Path,
) -> None:
    exercise = CanonicalExercise(
        tmp_path,
        live=True,
        experiment=False,
        registry_routes=True,
        adjudication_outcome="plural",
        formal_seed_mode="ready_exact",
    )
    formal = _attach_formal_claim(exercise)
    producer_input = formal["producer_input"]
    output = formal["output"]
    authority = formal["conceptual_authority"]
    branch_preferred = set(authority["preferred_system_ids"]).intersection(
        formal["branch_binding"]["conceptual_system_ids"]
    )
    assert len(branch_preferred) >= 2
    assert producer_input["conceptual_system_ids"] == [
        formal["source_system_id"]
    ]
    assert output["conceptual_system_ids"] == [formal["source_system_id"]]
    assert producer_input["theory_ancestry"]["preferred_system_ids"] == authority[
        "preferred_system_ids"
    ]
    assert len(authority["preferred_system_ids"]) > 1
    result = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    assert sum(
        action["kind"] == "prove" for action in result["schedule"]["actions"]
    ) == 1


@pytest.mark.parametrize("corruption", ["omit", "duplicate", "substitute_receipt"])
def test_ready_formal_schedule_corruption_fails_before_commit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    corruption: str,
) -> None:
    exercise = CanonicalExercise(
        tmp_path,
        live=True,
        experiment=False,
        registry_routes=True,
        formal_seed_mode="ready_exact",
    )
    formal = _attach_formal_claim(exercise)
    original = cycle_runtime.schedule_discovery_actions

    def corrupt(state: Mapping[str, Any]) -> dict[str, Any]:
        schedule = original(state)
        prove = [
            action for action in schedule["actions"]
            if action["kind"] == "prove"
        ]
        assert len(prove) == 1
        if corruption == "omit":
            schedule["actions"].remove(prove[0])
        elif corruption == "duplicate":
            schedule["actions"].append(copy.deepcopy(prove[0]))
        else:
            prove[0]["payload"]["formal_claim_binding"][
                "producer_receipt_id"
            ] = formal["output"]["source_operator_receipt_id"]
        return schedule

    monkeypatch.setattr(cycle_runtime, "schedule_discovery_actions", corrupt)
    with pytest.raises(
        ContractError,
        match="ready formal-claim output does not schedule exactly one bound prove action",
    ):
        run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    store = DiscoveryTransactionStore(
        exercise.state_root,
        target_id=exercise.target_id,
        run_id=exercise.run_id,
    )
    assert store.current_generation() == 0


@pytest.mark.skip(
    reason="historical five-world v1 reconstruction is non-authoritative and unreachable from the canonical cycle"
)
def test_five_experiment_ablations_preserve_theory_identity_and_only_request_typed_review(
    tmp_path: Path,
) -> None:
    expected_effects = {
        "none": None,
        "neutral_inconclusive": "no_theory_effect_inconclusive",
        "misleading_toy_positive": "bounded_consistency_signal_only",
        "registered_premise_falsifier": "registered_premise_revision_requested",
        "operational_failure": "no_theory_effect_operational",
    }
    worlds: list[dict[str, Any]] = []
    shared_literature_snapshot: dict[str, Any] | None = None
    for scenario, expected_effect in expected_effects.items():
        case_root = tmp_path / scenario
        case_root.mkdir()
        exercise = CanonicalExercise(
            case_root,
            live=True,
            experiment_scenario=scenario,
            literature_snapshot=shared_literature_snapshot,
        )
        if shared_literature_snapshot is None:
            shared_literature_snapshot = copy.deepcopy(exercise.snapshot)
        result = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
        assimilation = result["experiment_assimilation"]
        actual_effect = (
            assimilation["theory_effect"]["effect_kind"]
            if assimilation["theory_effect"] is not None
            else None
        )
        assert actual_effect == expected_effect
        assert assimilation["theory_identity_changed"] is False
        assert assimilation["theory_selected"] is False
        assert assimilation["proof_authorized"] is False
        assert assimilation["automatic_evidence_relation_recorded"] is False
        assert assimilation["premise_revision_requested"] is (
            scenario == "registered_premise_falsifier"
        )
        assert result["proof_handoff"] is None
        assert all(
            receipt["promotion_decision"] == "not_requested"
            for receipt in result["evaluation_receipts"]
        )
        receipt_id = assimilation["receipt_id"]
        if receipt_id is not None:
            assert not any(
                event["event_type"] == "evidence_recorded"
                and receipt_id in event.get("source_receipt_ids", [])
                for event in result["events"]
            )
        worlds.append(result)

    certificate = validate_five_experiment_world_semantics(worlds)
    assert certificate["matrix_scope"] == EXPERIMENT_WORLD_MATRIX_SCOPE
    assert certificate["world_ids"] == [
        "no_probe",
        "neutral_inconclusive",
        "misleading_toy_positive",
        "registered_premise_falsifier",
        "operational_failure",
    ]
    assert certificate["theory_identity_changed"] is False
    assert certificate["theory_selected"] is False
    assert certificate["proof_authorized"] is False
    assert certificate["automatic_evidence_relation_recorded"] is False
    assert certificate["only_permitted_delta"] == "registered_premise_review_pending"

    semantics = [row["experiment_world_semantics"] for row in worlds]
    assert len({row["theory_state_projection_digest"] for row in semantics}) == 1
    assert len({row["schedule_projection_digest"] for row in semantics}) == 1
    assert len({row["committed_ancestor"]["byte_digest"] for row in semantics}) == 1
    assert len(
        {row["matrix_precommitment"]["precommitment_digest"] for row in semantics}
    ) == 1
    by_world = {row["world_id"]: row for row in semantics}
    assert by_world["no_probe"]["executed_spec_binding"] is None
    assert by_world["no_probe"]["post_result_reflection_binding"] is None
    assert all(
        row["post_result_reflection_binding"]["typed_delta"]
        == row["permitted_pending_review_delta"]
        for world_id, row in by_world.items()
        if world_id != "no_probe"
    )
    assert by_world["registered_premise_falsifier"][
        "permitted_pending_review_delta"
    ]["status"] == "pending"
    assert all(
        row["permitted_pending_review_delta"]["status"] == "none"
        for world_id, row in by_world.items()
        if world_id != "registered_premise_falsifier"
    )

    def rehash(row: dict[str, Any]) -> None:
        ancestor = row["committed_ancestor"]
        ancestor_bytes = (
            json.dumps(
                ancestor["projection"],
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
            + "\n"
        ).encode("utf-8")
        ancestor["byte_size"] = len(ancestor_bytes)
        ancestor["byte_digest"] = bytes_digest(ancestor_bytes)
        precommitment = row["matrix_precommitment"]
        precommitment["precommitment_digest"] = canonical_digest(
            precommitment, exclude_keys=("precommitment_digest",)
        )
        delta = row["permitted_pending_review_delta"]
        delta["delta_digest"] = canonical_digest(
            delta,
            exclude_keys=("delta_digest",),
        )
        reflection = row.get("post_result_reflection_binding")
        if reflection is not None:
            reflection_delta = reflection["typed_delta"]
            reflection_delta["delta_digest"] = canonical_digest(
                reflection_delta, exclude_keys=("delta_digest",)
            )
        row["theory_state_projection_digest"] = canonical_digest(
            row["theory_state_projection"]
        )
        row["schedule_projection_digest"] = canonical_digest(
            row["schedule_projection"]
        )
        row["semantics_digest"] = canonical_digest(
            row,
            exclude_keys=("semantics_digest",),
        )

    def rejected(mutator: Any) -> None:
        attack = copy.deepcopy(semantics)
        mutator(attack)
        for row in attack:
            rehash(row)
        with pytest.raises(ContractError):
            validate_five_experiment_world_semantics(attack)

    # Every attack is rehashed after mutation.  These are semantic comparisons,
    # not integrity-only checks, and collectively cover the complete theory and
    # schedule projection families plus the one permitted review delta.
    rejected(
        lambda rows: rows[1]["committed_ancestor"]["projection"][
            "parent_reflective_theory"
        ]["explicit_unknowns"].append("forged committed ancestor")
    )
    rejected(
        lambda rows: rows[1]["matrix_precommitment"].__setitem__(
            "premise_statement", "forged post-experiment premise"
        )
    )
    rejected(
        lambda rows: rows[1]["theory_state_projection"][
            "integrated_reflective_theory"
        ]["theoretical_programme"]["proof_or_model_obligations"].append(
            "Mutated programme obligation"
        )
    )
    rejected(
        lambda rows: rows[1]["theory_state_projection"][
            "integrated_reflective_theory"
        ]["conceptual_systems"][0]["primitives"].append("mutated primitive")
    )
    rejected(
        lambda rows: rows[1]["theory_state_projection"][
            "integrated_reflective_theory"
        ]["conceptual_genealogy"]["historical_or_logical_formation"].append(
            "Mutated genealogy edge"
        )
    )
    rejected(
        lambda rows: rows[1]["theory_state_projection"]["literature_snapshot"][
            "sources"
        ][0]["claims"].append("Mutated literature claim")
    )
    rejected(
        lambda rows: rows[1]["theory_state_projection"][
            "integrated_reflective_theory"
        ]["provisional_synthesis"].__setitem__(
            "preferred_system_id",
            rows[1]["theory_state_projection"]["integrated_reflective_theory"][
                "conceptual_systems"
            ][0]["system_id"],
        )
    )
    rejected(
        lambda rows: rows[1]["schedule_projection"]["actions"][0].__setitem__(
            "kind", "prove"
        )
    )
    rejected(
        lambda rows: rows[1]["schedule_projection"]["actions"][1][
            "depends_on"
        ].append("action.synthetic-dependency")
    )
    rejected(
        lambda rows: rows[1]["schedule_projection"]["actions"][1]["payload"][
            "priority_vector"
        ].__setitem__("programme_impact", 0.0)
    )
    rejected(
        lambda rows: rows[1]["schedule_projection"]["actions"][1][
            "branch_ids"
        ].append("theory-branch.synthetic")
    )
    rejected(
        lambda rows: rows[3]["permitted_pending_review_delta"].__setitem__(
            "tested_claim_id", "claim.wrong"
        )
    )
    rejected(
        lambda rows: rows[1].__setitem__(
            "permitted_pending_review_delta",
            copy.deepcopy(rows[3]["permitted_pending_review_delta"]),
        )
    )
    rejected(
        lambda rows: (
            rows[1].__setitem__(
                "permitted_pending_review_delta",
                copy.deepcopy(rows[3]["permitted_pending_review_delta"]),
            ),
            rows[1]["post_result_reflection_binding"].__setitem__(
                "typed_delta",
                copy.deepcopy(rows[3]["permitted_pending_review_delta"]),
            ),
        )
    )
    rejected(
        lambda rows: rows[3]["permitted_pending_review_delta"].__setitem__(
            "status", "accepted"
        )
    )
    rejected(
        lambda rows: (
            rows[1]["direct_mutation_audit"]["theory_mutation_event_ids"].append(
                "devent.synthetic-mutation"
            ),
            rows[1]["direct_mutation_audit"].__setitem__(
                "theory_identity_changed", True
            ),
        )
    )
    rejected(lambda rows: rows[1].__setitem__("run_id", "run.crossed"))
    rejected(
        lambda rows: rows[1].__setitem__(
            "world_id", "outside_declared_five_world_matrix"
        )
    )
    rejected(
        lambda rows: rows.__setitem__(4, copy.deepcopy(rows[0]))
    )
    rejected(
        lambda rows: rows[1]["theory_state_projection"][
            "integrated_reflective_theory"
        ].pop("explicit_unknowns")
    )

    missing_world = copy.deepcopy(semantics[:-1])
    with pytest.raises(ContractError, match="exactly five"):
        validate_five_experiment_world_semantics(missing_world)


def test_local_only_cycle_is_explicitly_incubating_and_blocks_investment(tmp_path: Path) -> None:
    exercise = CanonicalExercise(tmp_path, live=False, experiment=False)
    result = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    assert result["literature_basis"]["mode"] == "local_only_incubation"
    assert result["literature_basis"]["active_investment_allowed"] is False
    assert {"no_novelty_claim", "no_active_investment", "no_experiment", "no_proof"}.issubset(
        result["literature_basis"]["restrictions"]
    )
    assert result["schedule"]["literature_investment_blocked"] is True
    assert all(row["literature_novelty"]["claim_allowed"] is False for row in result["evaluation_receipts"])
    assert all(row["promotion_decision"] == "not_requested" for row in result["evaluation_receipts"])


def test_caller_authored_proof_handoff_is_rejected_for_local_cycle(tmp_path: Path) -> None:
    exercise = CanonicalExercise(tmp_path, live=False, experiment=False)
    # The registered producer/post-commit route now owns proof authorization.
    # A caller-authored request is rejected before literature-specific checks.
    with pytest.raises(ContractError, match="caller-authored proof_request is disabled"):
        run_canonical_discovery_cycle(
            **exercise.cycle_kwargs(), proof_request=_proof_request(exercise)
        )


def test_caller_authored_proof_handoff_is_rejected_for_active_cycle(
    tmp_path: Path,
) -> None:
    exercise = CanonicalExercise(tmp_path, live=True, experiment=False)
    with pytest.raises(
        ContractError,
        match="caller-authored proof_request is disabled",
    ):
        run_canonical_discovery_cycle(
            **exercise.cycle_kwargs(), proof_request=_proof_request(exercise)
        )


def test_stale_cross_artifact_literature_and_cross_target_are_rejected(tmp_path: Path) -> None:
    exercise = CanonicalExercise(tmp_path, live=True, experiment=False)
    newer = run_frontier_literature_cycle(
        _search_request(exercise.target_id, exercise.theory_digest),
        providers=_live_providers(exercise.target_id, variant="newer"),
    )
    stale_portfolio, stale_receipt, stale_path = exercise.dispatch(
        "high-risk-hypothesis-forger",
        "hypothesis",
        {
            "charter": _charter(newer),
            "literature_snapshot": newer,
            "assimilation_packet": assimilate_literature(
                newer,
                theory_state_digest=newer["theory_state_digest"],
                theory_mappings=_mappings(newer),
            ),
        },
    )
    assert stale_portfolio["literature_snapshot_digest"] != exercise.snapshot["content_digest"]
    kwargs = exercise.cycle_kwargs()
    kwargs["operator_requests"] = [
        row for row in kwargs["operator_requests"] if row["request_id"] != exercise.portfolio_receipt["request_id"]
    ]
    kwargs["operator_receipts"] = [
        row for row in kwargs["operator_receipts"] if row["receipt_id"] != exercise.portfolio_receipt["receipt_id"]
    ]
    kwargs["artifact_roles"] = {**exercise.roles, "high_risk_portfolio": stale_path}
    with pytest.raises(ContractError, match="stale or different literature"):
        run_canonical_discovery_cycle(**kwargs)
    with pytest.raises(ContractError, match="crossed target/run/state"):
        run_canonical_discovery_cycle(**{**exercise.cycle_kwargs(), "target_id": "another-target"})


def test_one_cas_commit_is_idempotent_for_exact_same_operator_lineage(tmp_path: Path) -> None:
    exercise = CanonicalExercise(tmp_path, live=True, experiment=False)
    first = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    second = run_canonical_discovery_cycle(**exercise.cycle_kwargs())
    assert first["commit_id"] == second["commit_id"]
    assert first["committed_state_version"] == second["committed_state_version"] == 1
    assert first["events"] == second["events"]
    assert second["idempotent"] is True
    commits = list(
        (
            exercise.state_root
            / "targets"
            / exercise.target_id
            / "runs"
            / exercise.run_id
            / "commits"
        ).iterdir()
    )
    assert len(commits) == 1
