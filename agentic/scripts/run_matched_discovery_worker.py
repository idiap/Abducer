#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Execute one declared, deterministic matched-study worker operation.

This entrypoint is intentionally self-contained and standard-library only.  The
parent isolation adapter can therefore grant the child read access to this one
script and the Python runtime without granting read access to the repository or
to sibling study workspaces.  It performs bounded structural operations for the
candidate, high-risk, finite formal-lens, reflection, and blind-judge roles.

The outputs are *internal calibration material*.  They contain executable
finite Category/HoTT checks and structured conceptual transformations, but they
never assert truth, theorem status, continuum control, cognitive independence,
creative advantage, or physics value.
"""

from __future__ import annotations

import hashlib
import json
import os
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Mapping, Sequence


ROLES = {"candidate", "high_risk", "formal_lens", "judge"}
OPERATIONS = {
    "candidate_generation",
    "high_risk_generation",
    "parallel_maturation",
    "formal_lens",
    "reflection",
    "blind_judgment",
    "convergence",
    "isolation_probe",
}
ARMS = {
    "incumbent",
    "categorical",
    "hott",
    "combined",
    "no_abstraction",
    "decorative",
    "restatement",
}


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value)).hexdigest()


def _identifier(prefix: str, *parts: Any) -> str:
    suffix = hashlib.sha256(_canonical_json(list(parts))).hexdigest()[:24]
    return f"{prefix}.{suffix}"


def _text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _string_list(value: Any, *, field: str, minimum: int = 1) -> list[str]:
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f"{field} must be a non-empty string list")
    result = [_text(item) for item in value]
    if any(not item for item in result) or len(set(result)) != len(result):
        raise ValueError(f"{field} must contain unique substantive strings")
    return result


def _tasks(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("tasks")
    if not isinstance(raw, list) or not raw:
        raise ValueError("payload.tasks must be a non-empty list")
    tasks: list[dict[str, Any]] = []
    seen: set[str] = set()
    required = {
        "task_id",
        "cluster_id",
        "domain",
        "pressure",
        "protected_invariants",
        "incumbent_primitives",
        "physical_carrier",
        "formal_pressure",
        "falsifier",
    }
    for row in raw:
        if not isinstance(row, Mapping) or set(row) != required:
            raise ValueError("each task must have the exact declared task fields")
        task = dict(row)
        task_id = _text(task["task_id"])
        if not task_id or task_id in seen:
            raise ValueError("task identifiers must be unique and non-empty")
        seen.add(task_id)
        task["task_id"] = task_id
        task["cluster_id"] = _text(task["cluster_id"])
        task["domain"] = _text(task["domain"])
        task["pressure"] = _text(task["pressure"])
        task["protected_invariants"] = _string_list(
            task["protected_invariants"], field="protected_invariants"
        )
        task["incumbent_primitives"] = _string_list(
            task["incumbent_primitives"], field="incumbent_primitives"
        )
        task["physical_carrier"] = (
            None if task["physical_carrier"] is None else _text(task["physical_carrier"])
        )
        task["formal_pressure"] = _text(task["formal_pressure"])
        task["falsifier"] = _text(task["falsifier"])
        if not all(
            task[key]
            for key in ("cluster_id", "domain", "pressure", "formal_pressure", "falsifier")
        ):
            raise ValueError("task text fields must be substantive")
        tasks.append(task)
    return tasks


def _literature_effect(world: Mapping[str, Any]) -> tuple[str, str]:
    world_id = _text(world.get("world_id"))
    admitted = int(world.get("admitted_source_count", 0))
    route = _text(world.get("route_status"))
    effects = {
        "current_v3": (
            "current_routed",
            f"Use {admitted} admitted current records and preserve correction lineage.",
        ),
        "historical_v2": (
            "historical_only",
            "Treat the historical source set as a prior programme state, not current authority.",
        ),
        "no_literature": (
            "explicit_null",
            "Retain the pre-search intuition and mark every scheduled literature lane null.",
        ),
        "version_naive": (
            "quarantined",
            "Correction and withdrawal lineage was intentionally removed; investment is held.",
        ),
        "surveillance_only": (
            "observed_not_routed",
            "Observed records remain surveillance context and do not authorize theory routing.",
        ),
        "lane_drop": (
            "incomplete_lanes",
            "One scheduled lane is explicit null; missing coverage remains a named limitation.",
        ),
        "ambiguous_lineage": (
            "quarantined",
            "Version lineage is ambiguous, so source-conditioned convergence is prohibited.",
        ),
        "target_mismatch": (
            "rejected_target_mismatch",
            "All returned records fail the target join and cannot influence the programme.",
        ),
    }
    if world_id not in effects or not route:
        raise ValueError("unknown or malformed literature world")
    return effects[world_id]


def _arm_structure(task: Mapping[str, Any], arm: str) -> tuple[list[str], list[str], str]:
    incumbent = list(task["incumbent_primitives"])
    carrier = task["physical_carrier"] or "declared nonphysics semantic carrier"
    if arm == "categorical":
        return (
            incumbent + ["typed interface objects", "composable morphisms"],
            ["functorial transport", "commuting comparison square"],
            f"Localize the pressure as failure of a comparison square over {carrier}.",
        )
    if arm == "hott":
        return (
            incumbent + ["identity types", "path-indexed fibers"],
            ["transport along equivalence", "higher coherence"],
            f"Localize the pressure as representative dependence of transport over {carrier}.",
        )
    if arm == "combined":
        return (
            incumbent
            + ["typed interface objects", "composable morphisms", "identity types", "path-indexed fibers"],
            ["functorial transport", "commuting comparison square", "path coherence"],
            f"Compare diagram commutativity with path coherence before returning to {carrier}.",
        )
    if arm == "no_abstraction":
        return (
            incumbent,
            ["direct local implication"],
            "Work directly in the task vocabulary without introducing a higher-level language.",
        )
    if arm == "decorative":
        return (
            incumbent,
            ["unchanged incumbent relation"],
            "Add categorical and homotopical words only as a declared rhetorical overlay.",
        )
    if arm == "restatement":
        return (
            incumbent,
            ["restated incumbent relation"],
            "Restate the pressure while preserving every incumbent primitive and dependency.",
        )
    return (
        incumbent + ["explicit regime ledger"],
        ["incumbent mechanism under boundary audit"],
        f"Strengthen the incumbent route while keeping the carrier {carrier} explicit.",
    )


def _strategy_move(strategy: Mapping[str, Any], task: Mapping[str, Any]) -> str:
    strategy_id = _text(strategy.get("strategy_id"))
    moves = {
        "incumbent_systematic": (
            "Make every incumbent dependency explicit and search only for its weakest missing lemma."
        ),
        "mechanism_inversion": (
            "Invert the explanatory direction and ask whether the alleged consequence is the constraint that generates the mechanism."
        ),
        "boundary_object_transfer": (
            "Introduce a boundary object that carries exactly the invariants shared by otherwise incompatible regimes."
        ),
        "failure_first_counterfactual": (
            "Treat the sharpest falsifier as primary and derive the smallest ontology in which that failure becomes structurally impossible."
        ),
    }
    if strategy_id not in moves:
        raise ValueError("unknown synthetic generation strategy")
    return f"{moves[strategy_id]} Target pressure: {task['pressure']}"


def _strategy_transformation(
    strategy: Mapping[str, Any], task: Mapping[str, Any], base_mechanism: str
) -> dict[str, Any]:
    """Turn a strategy descriptor into a task-specific mechanistic delta.

    The operation name is semantic content, not the fixture's direct strategy
    label.  A blind judge may inspect the proposed transformation while still
    being unable to recover condition identity from a privileged field.
    """

    strategy_id = _text(strategy.get("strategy_id"))
    invariant = task["protected_invariants"][0]
    primitive = task["incumbent_primitives"][0]
    carrier = task["physical_carrier"] or "declared nonphysics semantic carrier"
    specifications = {
        "incumbent_systematic": {
            "operator": "dependency_localization",
            "new_primitive": "explicit_dependency_ledger",
            "new_relation": "localizes_weakest_target_dependency",
            "mechanism_delta": (
                f"Factor {base_mechanism} into an explicit dependency ledger; "
                f"the weakest unresolved dependency must preserve {invariant}."
            ),
            "decisive_question": (
                f"Which dependency of {primitive} first fails while the carrier {carrier} remains fixed?"
            ),
        },
        "mechanism_inversion": {
            "operator": "causal_direction_inversion",
            "new_primitive": "consequence_constraint_generator",
            "new_relation": "consequence_generates_admissible_mechanism",
            "mechanism_delta": (
                f"Treat the observable consequence encoded by {task['falsifier']} as a constraint "
                f"that generates admissible realizations of {primitive}, then recover {base_mechanism}."
            ),
            "decisive_question": (
                f"Does consequence-first reconstruction preserve {invariant} without assuming {primitive}?"
            ),
        },
        "boundary_object_transfer": {
            "operator": "invariant_boundary_interposition",
            "new_primitive": "task_invariant_boundary_carrier",
            "new_relation": "mediates_regimes_without_identifying_them",
            "mechanism_delta": (
                f"Interpose a boundary carrier containing exactly {invariant}; transport between "
                f"the incumbent regimes only through maps that return to {carrier}."
            ),
            "decisive_question": (
                f"Can the boundary carrier reconstruct {primitive} on both sides without erasing a regime difference?"
            ),
        },
        "failure_first_counterfactual": {
            "operator": "failure_excluding_reconstruction",
            "new_primitive": "minimal_failure_excluding_ontology",
            "new_relation": "forbids_declared_counterexample_before_reconstruction",
            "mechanism_delta": (
                f"Make the counterexample class in {task['falsifier']} primitive, exclude it by a minimal "
                f"structural axiom, and reconstruct {base_mechanism} only afterward."
            ),
            "decisive_question": (
                f"What weakest axiom excludes the declared failure while retaining {invariant} and {carrier}?"
            ),
        },
    }
    if strategy_id not in specifications:
        raise ValueError("unknown synthetic generation strategy")
    specification = specifications[strategy_id]
    return {
        **specification,
        "preserved_invariant": invariant,
        "task_carrier": carrier,
        "mechanism_chain": [
            f"Apply {specification['operator']} to {primitive}.",
            specification["mechanism_delta"],
            f"Reject the transformation if {task['falsifier']}",
        ],
    }


def _candidate_generation(payload: Mapping[str, Any]) -> dict[str, Any]:
    tasks = _tasks(payload)
    arm = _text(payload.get("arm"))
    strategy = payload.get("strategy")
    world = payload.get("literature_world")
    if arm not in ARMS or not isinstance(strategy, Mapping) or not isinstance(world, Mapping):
        raise ValueError(
            "candidate generation requires a known arm plus synthetic strategy and literature descriptors"
        )
    route_status, literature_effect = _literature_effect(world)
    records = []
    for task in tasks:
        primitives, relations, base_mechanism = _arm_structure(task, arm)
        transformation = _strategy_transformation(strategy, task, base_mechanism)
        primitives = list(dict.fromkeys([*primitives, transformation["new_primitive"]]))
        relations = list(dict.fromkeys([*relations, transformation["new_relation"]]))
        mechanism = transformation["mechanism_delta"]
        statement = _strategy_move(strategy, task)
        candidate_id = _identifier(
            "matched-candidate",
            task["task_id"],
            arm,
            strategy["strategy_id"],
            world["world_id"],
            statement,
        )
        records.append(
            {
                "candidate_id": candidate_id,
                "task_id": task["task_id"],
                "statement": statement,
                "primitives": primitives,
                "relations": relations,
                "mechanism": mechanism,
                "strategy_transformation": transformation,
                "protected_invariants": list(task["protected_invariants"]),
                "literature_effect": literature_effect,
                "route_status": route_status,
                "treatment_authority": "synthetic_structural_descriptor_calibration_only",
                "correction_conditions": [
                    task["falsifier"],
                    "Withdraw the move if it changes the declared physical or semantic carrier.",
                ],
                "falsifier": task["falsifier"],
                "physical_value_link": (
                    f"The only physics-facing value carrier is {task['physical_carrier']}."
                    if task["physical_carrier"]
                    else "This transfer control has no physics-value authority."
                ),
                "opportunity_count": 1,
            }
        )
    return {"output_kind": "candidate_generation", "records": records}


def _corner_descriptors(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("corner_descriptors")
    required = {
        "corner_family",
        "mechanism_key",
        "primitive",
        "relation",
        "intuitive_leap",
        "mechanism",
        "affordance",
        "risk",
        "maturation_question",
        "is_wildcard",
        "is_control",
        "descriptor_digest",
    }
    if not isinstance(raw, list) or len(raw) != 10:
        raise ValueError("high-risk generation requires the exact ten-corner catalog")
    rows: list[dict[str, Any]] = []
    families: set[str] = set()
    controls = 0
    wildcards = 0
    for item in raw:
        if not isinstance(item, Mapping) or set(item) != required:
            raise ValueError("high-risk corner descriptor has open or missing fields")
        row = dict(item)
        core = {key: row[key] for key in row if key != "descriptor_digest"}
        if row["descriptor_digest"] != _digest(core):
            raise ValueError("high-risk corner descriptor digest changed")
        for field in (
            "corner_family",
            "mechanism_key",
            "primitive",
            "relation",
            "intuitive_leap",
            "mechanism",
            "affordance",
            "risk",
            "maturation_question",
        ):
            row[field] = _text(row[field])
            if not row[field]:
                raise ValueError("high-risk corner descriptor text is empty")
        if not isinstance(row["is_wildcard"], bool) or not isinstance(row["is_control"], bool):
            raise ValueError("high-risk corner flags must be Boolean")
        families.add(row["corner_family"])
        controls += int(row["is_control"])
        wildcards += int(row["is_wildcard"])
        rows.append(row)
    if len(families) < 6 or controls != 1 or wildcards < 2:
        raise ValueError("high-risk corner catalog lost diversity, control, or wildcards")
    return rows


def _high_risk_generation(payload: Mapping[str, Any]) -> dict[str, Any]:
    tasks = {row["task_id"]: row for row in _tasks(payload)}
    candidates = payload.get("candidates")
    strategy = payload.get("strategy")
    if not isinstance(candidates, list) or not isinstance(strategy, Mapping):
        raise ValueError("high-risk generation requires candidates and one synthetic strategy")
    descriptors = _corner_descriptors(payload)
    catalog_digest = _digest(descriptors)
    records = []
    for candidate in candidates:
        if not isinstance(candidate, Mapping) or candidate.get("task_id") not in tasks:
            raise ValueError("high-risk candidate does not map to a declared task")
        task = tasks[str(candidate["task_id"])]
        portfolio_id = _identifier(
            "matched-high-risk-portfolio", candidate["candidate_id"], catalog_digest
        )
        for descriptor in descriptors:
            corner_family = descriptor["corner_family"]
            mechanism = (
                f"{descriptor['mechanism']} Task instantiation: compose this corner with "
                f"{candidate['mechanism']} while preserving {task['protected_invariants']}."
            )
            variant_id = _identifier(
                "matched-high-risk",
                portfolio_id,
                corner_family,
                descriptor["mechanism_key"],
                mechanism,
            )
            ontology_delta = {
                "new_primitive": f"{descriptor['primitive']}::{task['task_id']}",
                "new_relation": descriptor["relation"],
                "retyped_incumbent": candidate["primitives"][0],
                "affordance": descriptor["affordance"],
            }
            risk_axes = [
                {
                    "axis_id": "ontology_risk",
                    "rationale": (
                        f"{descriptor['risk']} The proposed primitive {ontology_delta['new_primitive']} "
                        f"must not presuppose {task['falsifier']}."
                    ),
                },
                {
                    "axis_id": "carrier_translation_risk",
                    "rationale": (
                        f"The relation {descriptor['relation']} may fail to return to "
                        f"{task['physical_carrier'] or 'the declared semantic carrier'} while preserving "
                        f"{task['protected_invariants'][0]}."
                    ),
                },
            ]
            reward_axes = [
                {
                    "axis_id": "unification_upside",
                    "rationale": (
                        f"{descriptor['affordance']} It must retain the distinction among "
                        f"{task['protected_invariants']}."
                    ),
                },
                {
                    "axis_id": "question_generation_upside",
                    "rationale": descriptor["maturation_question"],
                },
            ]
            correction_conditions = [
                *candidate["correction_conditions"],
                (
                    f"Retire the {corner_family} branch if {ontology_delta['new_primitive']} is "
                    "definitionally equivalent to the desired conclusion."
                ),
            ]
            premortem = (
                f"{corner_family} premortem: {descriptor['risk']} The strategy transformation "
                f"{candidate['strategy_transformation']['operator']} may merely rename the incumbent "
                f"mechanism; the earliest decisive question is {descriptor['maturation_question']}"
            )
            records.append(
                {
                    "variant_id": variant_id,
                    "branch_id": _identifier("matched-corner-branch", variant_id),
                    "portfolio_id": portfolio_id,
                    "task_id": task["task_id"],
                    "parent_candidate_id": str(candidate["candidate_id"]),
                    "corner_family": corner_family,
                    "mechanism_key": descriptor["mechanism_key"],
                    "statement": (
                        f"Aggressive {corner_family} corner for {task['pressure']}: "
                        f"{descriptor['intuitive_leap']}"
                    ),
                    "mechanism": mechanism,
                    "mechanism_chain": [
                        descriptor["intuitive_leap"],
                        mechanism,
                        descriptor["maturation_question"],
                    ],
                    "ontology_delta": ontology_delta,
                    "decisive_question": descriptor["maturation_question"],
                    "parent_statement": str(candidate["statement"]),
                    "parent_mechanism": str(candidate["mechanism"]),
                    "parent_primitives": list(candidate["primitives"]),
                    "parent_relations": list(candidate["relations"]),
                    "strategy_transformation": dict(candidate["strategy_transformation"]),
                    "target_pressure": task["pressure"],
                    "protected_invariants": list(candidate["protected_invariants"]),
                    "risk_axes": risk_axes,
                    "reward_axes": reward_axes,
                    "premortem": premortem,
                    "falsifier": task["falsifier"],
                    "correction_conditions": correction_conditions,
                    "physical_value_link": str(candidate["physical_value_link"]),
                    "conceptual_distance": (
                        "protected_low_confidence_high_upside_wildcard"
                        if descriptor["is_wildcard"]
                        else (
                            "capable_incumbent_control"
                            if descriptor["is_control"]
                            else "noncontrol_structural_corner"
                        )
                    ),
                    "is_wildcard": descriptor["is_wildcard"],
                    "is_control": descriptor["is_control"],
                    "incubation_status": "protected_high_risk_incubation",
                    "literature_effect": str(candidate["literature_effect"]),
                    "treatment_authority": "synthetic_internal_structural_portfolio_only",
                    "parallel_contract": {
                        "frozen_parent_candidate_id": candidate["candidate_id"],
                        "forbidden_sibling_context_before_barrier": True,
                        "shared_mutable_state": False,
                        "join_after_all_terminal": True,
                    },
                    "opportunity_count": 1,
                }
            )
    return {
        "output_kind": "high_risk_generation",
        "records": records,
        "portfolio_execution": {
            "task_count": len(tasks),
            "variants_per_task": len(descriptors),
            "corner_catalog_digest": catalog_digest,
            "scheduled_branch_count": len(records),
            "corner_families": sorted(row["corner_family"] for row in descriptors),
            "protected_wildcard_count_per_task": sum(
                int(row["is_wildcard"]) for row in descriptors
            ),
            "capable_control_count_per_task": sum(
                int(row["is_control"]) for row in descriptors
            ),
            "authority_boundary": "internal_structural_portfolio_execution_no_merit_or_value_authority",
        },
    }


def _parallel_maturation(payload: Mapping[str, Any]) -> dict[str, Any]:
    branch_kind = _text(payload.get("branch_kind"))
    proposals = payload.get("proposals")
    if branch_kind not in {"candidate", "high_risk"} or not isinstance(proposals, list):
        raise ValueError("parallel maturation requires one declared proposal branch")
    def mature(proposal: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(proposal, Mapping):
            raise ValueError("maturation proposal must be an object")
        parent_id = str(proposal.get("candidate_id") or proposal.get("variant_id") or "")
        task_id = _text(proposal.get("task_id"))
        if not parent_id or not task_id:
            raise ValueError("maturation proposal lacks identity")
        if branch_kind == "candidate":
            preserved_content = {
                "statement": str(proposal["statement"]),
                "mechanism": str(proposal["mechanism"]),
                "primitives": list(proposal["primitives"]),
                "relations": list(proposal["relations"]),
                "strategy_transformation": dict(proposal["strategy_transformation"]),
                "protected_invariants": list(proposal["protected_invariants"]),
                "literature_effect": str(proposal["literature_effect"]),
                "falsifier": str(proposal["falsifier"]),
                "correction_conditions": list(proposal["correction_conditions"]),
                "physical_value_link": str(proposal["physical_value_link"]),
            }
            mechanism_steps = [
                f"Instantiate the proposed mechanism: {proposal['mechanism']}",
                "Propagate the declared protected invariants without changing their carrier.",
                f"Attempt the declared falsifier: {proposal['falsifier']}",
            ]
            semantic_anchors = [
                *proposal["protected_invariants"],
                *proposal["primitives"],
                proposal["falsifier"],
            ]
        else:
            preserved_content = {
                "statement": str(proposal["statement"]),
                "branch_id": str(proposal["branch_id"]),
                "portfolio_id": str(proposal["portfolio_id"]),
                "corner_family": str(proposal["corner_family"]),
                "mechanism_key": str(proposal["mechanism_key"]),
                "mechanism": str(proposal["mechanism"]),
                "mechanism_chain": list(proposal["mechanism_chain"]),
                "ontology_delta": dict(proposal["ontology_delta"]),
                "decisive_question": str(proposal["decisive_question"]),
                "parent_statement": str(proposal["parent_statement"]),
                "parent_mechanism": str(proposal["parent_mechanism"]),
                "parent_primitives": list(proposal["parent_primitives"]),
                "parent_relations": list(proposal["parent_relations"]),
                "strategy_transformation": dict(proposal["strategy_transformation"]),
                "target_pressure": str(proposal["target_pressure"]),
                "protected_invariants": list(proposal["protected_invariants"]),
                "risk_axes": list(proposal["risk_axes"]),
                "reward_axes": list(proposal["reward_axes"]),
                "premortem": str(proposal["premortem"]),
                "literature_effect": str(proposal["literature_effect"]),
                "falsifier": str(proposal["falsifier"]),
                "correction_conditions": list(proposal["correction_conditions"]),
                "physical_value_link": str(proposal["physical_value_link"]),
                "conceptual_distance": str(proposal["conceptual_distance"]),
                "is_wildcard": bool(proposal["is_wildcard"]),
                "is_control": bool(proposal["is_control"]),
                "parallel_contract": dict(proposal["parallel_contract"]),
            }
            mechanism_steps = [
                *proposal["mechanism_chain"],
                f"Run the premortem before convergence: {proposal['premortem']}",
                f"Attempt the declared falsifier: {proposal['falsifier']}",
            ]
            semantic_anchors = [
                *proposal["protected_invariants"],
                *proposal["parent_primitives"],
                proposal["ontology_delta"]["new_primitive"],
                proposal["ontology_delta"]["new_relation"],
                proposal["falsifier"],
            ]
        return {
            "maturation_id": _identifier(
                "matched-maturation",
                parent_id,
                branch_kind,
                proposal.get("branch_id"),
            ),
            "task_id": task_id,
            "parent_id": parent_id,
            "branch_kind": branch_kind,
            "proposal_content": preserved_content,
            "explicit_mechanism_steps": mechanism_steps,
            "boundary_conditions": [
                "No finite witness is promoted to an unbounded statement.",
                "No formal equivalence is promoted to physical equivalence.",
            ],
            "correction_paths": list(proposal["correction_conditions"]),
            "protected_differences": [
                "finite versus continuum authority",
                "formal representation versus physical carrier",
            ],
            "unresolved_objections": [
                "Independent authority has not judged relevance, depth, or physics value.",
                "Population generalization and cognitive independence remain unavailable.",
            ],
            "semantic_anchors": semantic_anchors,
            "opportunity_count": 1,
        }

    if branch_kind == "high_risk":
        max_workers = min(10, len(proposals))
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            records = list(pool.map(mature, proposals))
        branch_execution = {
            "mode": "parallel_isolated_portfolio_branches",
            "max_workers": max_workers,
            "scheduled_branch_count": len(proposals),
            "completed_branch_count": len(records),
            "barrier_status": "complete",
            "shared_mutable_state": False,
        }
    else:
        records = [mature(proposal) for proposal in proposals]
        branch_execution = {
            "mode": "single_candidate_branch_per_task",
            "max_workers": 1,
            "scheduled_branch_count": len(proposals),
            "completed_branch_count": len(records),
            "barrier_status": "complete",
            "shared_mutable_state": False,
        }
    return {
        "output_kind": "parallel_maturation",
        "branch_kind": branch_kind,
        "records": records,
        "branch_execution": branch_execution,
    }


def _formal_case(task: Mapping[str, Any], lens: str) -> dict[str, Any]:
    """Reconstruct the task-bound case identity used by the shared formal engine."""

    return {
        "case_id": f"{task['task_id']}.{lens}",
        "target_id": task["task_id"],
        "obligation_id": f"{task['task_id']}.finite-{lens}-obligation",
        "preferred_lens": lens,
        "task_semantics": {
            "pressure": task["pressure"],
            "formal_pressure": task["formal_pressure"],
            "protected_invariants": list(task["protected_invariants"]),
            "incumbent_primitives": list(task["incumbent_primitives"]),
            "physical_carrier": task["physical_carrier"],
            "falsifier": task["falsifier"],
        },
    }


def _typed_artifact_summary(
    task: Mapping[str, Any], lens: str, artifact: Mapping[str, Any]
) -> dict[str, Any]:
    """Fail closed on the sealed shared-engine envelope and expose fixed slots.

    The parent runtime replays the full registered validator.  This isolated,
    standard-library worker checks the exact case and artifact digests and then
    projects a count-matched summary.  It never implements a second category or
    HoTT semantics.
    """

    case = _formal_case(task, lens)
    expected_keys = {
        "skill_id", "skill_version", "lens", "case_id", "target_id",
        "case_digest", "obligation_id", "model", "negative_witness",
        "countermodel_output_digest", "target_preserved", "derived_consequence",
        "correction_test_precommitted", "authority_boundary",
        "dependency_authority_digest", "formalization_scope",
        "semantic_translation", "task_derived_model_identity",
        "semantic_translation_receipt", "task_derived_formal_delta",
        "physics_handback", "artifact_digest",
    }
    if not isinstance(artifact, Mapping) or set(artifact) != expected_keys:
        raise ValueError("typed formal artifact lacks the exact shared-engine envelope")
    core = {key: value for key, value in artifact.items() if key != "artifact_digest"}
    if (
        artifact["artifact_digest"] != _digest(core)
        or artifact["case_digest"] != _digest(case)
        or artifact["case_id"] != case["case_id"]
        or artifact["target_id"] != task["task_id"]
        or artifact["obligation_id"] != case["obligation_id"]
        or artifact["lens"] != lens
        or artifact["skill_version"] != "4.0.0-task-derived"
        or artifact["formalization_scope"]
        != "task_derived_finite_semantic_translation"
        or artifact["target_preserved"] is not True
        or artifact["derived_consequence"] is not True
        or artifact["correction_test_precommitted"] is not True
    ):
        raise ValueError("typed formal artifact changed its task or validator binding")
    translation = artifact["semantic_translation"]
    semantic_receipt = artifact["semantic_translation_receipt"]
    task_delta = artifact["task_derived_formal_delta"]
    physics_handback = artifact["physics_handback"]
    task_semantics = case["task_semantics"]
    # The producer seals the delta's content, excluding its self-digest. Hashing
    # the already sealed object rejects every genuine handback. Recompute the
    # same core and verify both the self-seal and the handback reference.
    delta_digest = (
        _digest({key: value for key, value in task_delta.items() if key != "content_digest"})
        if isinstance(task_delta, Mapping)
        else None
    )
    if (
        not all(
            isinstance(row, Mapping)
            for row in (
                translation,
                semantic_receipt,
                task_delta,
                physics_handback,
                artifact["task_derived_model_identity"],
            )
        )
        or translation.get("mode") != "task_derived_finite_semantic_translation"
        or translation.get("lens") != lens
        or translation.get("case_digest") != _digest(case)
        or translation.get("task_semantics_digest") != _digest(task_semantics)
        or translation.get("task_contract", {}).get("physical_carrier")
        != task["physical_carrier"]
        or translation.get("task_contract", {}).get("formal_pressure")
        != task["formal_pressure"]
        or len(translation.get("primitive_bindings", []))
        != len(task["incumbent_primitives"])
        or len(translation.get("invariant_bindings", []))
        != len(task["protected_invariants"])
        or semantic_receipt.get("status") != "passed"
        or semantic_receipt.get("case_digest") != _digest(case)
        or semantic_receipt.get("model_identity")
        != artifact["task_derived_model_identity"]
        or task_delta.get("model_identity")
        != artifact["task_derived_model_identity"]
        or task_delta.get("physical_carrier") != task["physical_carrier"]
        or task_delta.get("falsifier") != task["falsifier"]
        or physics_handback.get("task_derived_formal_delta_digest")
        != delta_digest
        or task_delta.get("content_digest") != delta_digest
        or physics_handback.get("physical_carrier") != task["physical_carrier"]
        or physics_handback.get("falsifier") != task["falsifier"]
    ):
        raise ValueError("typed formal artifact lacks its exact task-semantic handback")
    witness = artifact["negative_witness"]
    certificate = witness.get("certificate") if isinstance(witness, Mapping) else None
    receipt = certificate.get("validator_receipt") if isinstance(certificate, Mapping) else None
    if (
        not isinstance(receipt, Mapping)
        or receipt.get("status") != "passed"
        or receipt.get("dependency_authority_digest")
        != artifact["dependency_authority_digest"]
    ):
        raise ValueError("typed formal artifact lacks a passed dependency-bound witness")
    model = artifact["model"]
    if lens == "categorical":
        law_names = ["typing", "identities", "composition", "associativity", "universality", "naturality_burden"]
        witness_kind = "finite_noncommuting_parallel_composites"
        formal_kind = "typed_finite_category_shared_engine"
    else:
        law_names = ["typing", "map_totality", "inverse_homotopies", "transport", "path_fibers", "two_cell_coherence"]
        witness_kind = "finite_noncoherent_transport_composites"
        formal_kind = "typed_finite_discrete_hott_shared_engine"
    return {
        "formal_kind": formal_kind,
        "artifact_digest": artifact["artifact_digest"],
        "model_digest": _digest(model),
        "witness_digest": _digest(witness),
        "validator_receipt_id": receipt["receipt_id"],
        "dependency_authority_digest": artifact["dependency_authority_digest"],
        "formalization_scope": artifact["formalization_scope"],
        "semantic_translation_digest": _digest(translation),
        "semantic_translation_receipt_id": semantic_receipt["receipt_id"],
        "task_derived_model_identity": dict(artifact["task_derived_model_identity"]),
        "task_derived_formal_delta": dict(task_delta),
        "physics_handback": dict(physics_handback),
        "law_slots": [
            {"slot_id": f"law-{index + 1}", "law": name, "result": "shared_engine_replayed"}
            for index, name in enumerate(law_names)
        ],
        "witness_slot": {
            "kind": witness_kind,
            "exact_obstruction": str(witness["exact_obstruction"]),
            "certificate_id": certificate["certificate_id"],
        },
    }


def _control_artifact_summary(task: Mapping[str, Any], lens: str) -> dict[str, Any]:
    """Return a slot-matched control without pretending that a validator ran."""

    control_kind = {
        "incumbent": "capable_incumbent_control",
        "no_abstraction": "capable_direct_reasoning_control",
        "decorative": "count_matched_semantically_corrupt_sham",
        "restatement": "count_matched_restatement_control",
    }[lens]
    law_names = ["typing", "identity", "composition", "transport", "coherence", "target_handback"]
    return {
        "formal_kind": control_kind,
        "artifact_digest": _digest({"task": task["task_id"], "control": lens}),
        "model_digest": _digest({"control": lens, "slots": law_names}),
        "witness_digest": _digest({"falsifier": task["falsifier"], "control": lens}),
        "validator_receipt_id": None,
        "dependency_authority_digest": None,
        "formalization_scope": "count_matched_control_without_task_derived_translation",
        "semantic_translation_digest": None,
        "semantic_translation_receipt_id": None,
        "task_derived_model_identity": None,
        "task_derived_formal_delta": None,
        "physics_handback": None,
        "law_slots": [
            {"slot_id": f"law-{index + 1}", "law": name, "result": "control_not_formally_replayed"}
            for index, name in enumerate(law_names)
        ],
        "witness_slot": {
            "kind": "declared_control_burden",
            "exact_obstruction": task["formal_pressure"],
            "certificate_id": None,
        },
    }


def _formal_lens(payload: Mapping[str, Any]) -> dict[str, Any]:
    tasks = _tasks(payload)
    lens = _text(payload.get("lens"))
    if lens not in ARMS:
        raise ValueError("formal lens operation requires a declared study arm")
    raw_artifacts = payload.get("typed_artifacts", [])
    if not isinstance(raw_artifacts, list):
        raise ValueError("formal lens typed_artifacts must be a list")
    artifact_index = {
        (str(row.get("target_id")), str(row.get("lens"))): row
        for row in raw_artifacts
        if isinstance(row, Mapping)
    }
    invoked_lenses = (
        ["categorical", "hott"] if lens == "combined"
        else [lens] if lens in {"categorical", "hott"}
        else []
    )
    expected_pairs = {(task["task_id"], selected) for task in tasks for selected in invoked_lenses}
    if set(artifact_index) != expected_pairs:
        raise ValueError("formal lens artifacts are not task-total for the invoked lenses")
    records = []
    execution_rows = []
    model_rows = []
    witness_rows = []
    for task in tasks:
        summaries = [
            _typed_artifact_summary(task, selected, artifact_index[(task["task_id"], selected)])
            for selected in invoked_lenses
        ] or [_control_artifact_summary(task, lens)]
        invoked = bool(invoked_lenses)
        category_check = next(
            (
                {**summary, "mismatch_elements": [summary["witness_slot"]["certificate_id"]]}
                for summary in summaries
                if summary["formal_kind"] == "typed_finite_category_shared_engine"
            ),
            None,
        )
        hott_check = next(
            (
                {**summary, "round_trip_holds": False}
                for summary in summaries
                if summary["formal_kind"] == "typed_finite_discrete_hott_shared_engine"
            ),
            None,
        )
        localized_invariant = task["protected_invariants"][0]
        task_deltas = [
            summary["task_derived_formal_delta"] for summary in summaries
            if summary["task_derived_formal_delta"] is not None
        ]
        task_handbacks = [
            summary["physics_handback"] for summary in summaries
            if summary["physics_handback"] is not None
        ]
        burden = (
            " | ".join(
                str(delta["changed_theoretical_burden"]) for delta in task_deltas
            )
            if invoked
            else (
                f"Directly audit {task['formal_pressure']} against {localized_invariant} and "
                f"the declared falsifier {task['falsifier']}"
                if lens in {"incumbent", "no_abstraction"}
                else (
                    "Formal vocabulary is present, but its slots are deliberately detached from the task anchors."
                    if lens == "decorative"
                    else f"Restate the open burden {task['formal_pressure']} without claiming a new decision."
                )
            )
        )
        changed_next_decision = (
            " | ".join(
                str(
                    handback.get("changed_next_physics_decision")
                    or handback["changed_next_theory_decision"]
                )
                for handback in task_handbacks
            )
            if invoked
            else (
                f"Before using the declared carrier, run the correction test: {task['falsifier']}"
                if lens in {"incumbent", "no_abstraction"}
                else (
                    "No target-changing decision follows from the decorative sham."
                    if lens == "decorative"
                    else "No target-changing decision follows from a restatement alone."
                )
            )
        )
        formal_id = _identifier("matched-formal", task["task_id"], lens, summaries, burden)
        physics_handback = None
        if task["physical_carrier"] is not None:
            physics_handback = {
                "physical_carrier": task["physical_carrier"],
                "finite_consequence": (
                    f"The finite check localizes {task['formal_pressure']} on the named carrier."
                    if invoked
                    else f"The control returns the declared burden {task['formal_pressure']} without formal promotion."
                ),
                "changed_next_decision": changed_next_decision,
                "correction_test": task["falsifier"],
                "touched_gate": "finite representation and burden localization only",
                "untouched_gates": [
                    "same-theory continuum construction",
                    "Osterwalder-Schrader reconstruction",
                    "uniform positive mass gap",
                ],
                "physics_value_evidence_status": "unavailable",
                "continuum_authority_status": "unavailable",
                "task_derived_handbacks": task_handbacks,
            }
        semantic_anchor = (
            localized_invariant
            if lens != "decorative"
            else "foreign decorative anchor with no task identity"
        )
        # Every arm exposes exactly three role slots, six law slots per summary,
        # two correction slots, and one handback slot.  The judge assesses task
        # alignment, never the number or presence of formal artifacts.
        content_projection = {
            "task_semantics_digest": _digest(_formal_case(task, "categorical")["task_semantics"]),
            "semantic_anchor": semantic_anchor,
            "object_role_slots": [
                {"slot_id": "source", "task_anchor": task["incumbent_primitives"][0]},
                {"slot_id": "mediator", "task_anchor": semantic_anchor},
                {"slot_id": "target", "task_anchor": task["physical_carrier"] or task["pressure"]},
            ],
            "law_slots": summaries[0]["law_slots"],
            "witness_slots": [
                summaries[0]["witness_slot"],
                {
                    "kind": "task_falsifier",
                    "exact_obstruction": task["falsifier"] if lens != "decorative" else "unbound decorative obstruction",
                    "certificate_id": None,
                },
            ],
            "localized_burden": burden,
            "changed_next_decision": changed_next_decision,
            "correction_obligations": [
                task["falsifier"] if lens != "decorative" else "unbound decorative correction",
                f"Preserve {localized_invariant}" if lens != "decorative" else "preserve an unbound decorative token",
            ],
            "physics_handback": physics_handback,
            "task_derived_formal_delta": task_deltas if invoked else None,
            "semantic_translation_receipt_ids": (
                [summary["semantic_translation_receipt_id"] for summary in summaries]
                if invoked else []
            ),
        }
        row = {
            "formal_id": formal_id,
            "task_id": task["task_id"],
            "lens": lens,
            "status": (
                "finite_task_derived_semantic_check_executed"
                if invoked
                else (
                    "sham_formalism_control"
                    if lens == "decorative"
                    else "nonformal_control_arm"
                )
            ),
            "typed_artifact_summaries": summaries,
            # These two fields preserve the existing isolation-adapter
            # response contract.  They are typed shared-engine summaries, not
            # the removed lexical descriptor implementation.
            "category_check": category_check,
            "hott_check": hott_check,
            "burden_localization": burden,
            "falsifier": task["falsifier"],
            "overhead_units": 2 if lens == "combined" else (1 if invoked else 0),
            "physics_handback": physics_handback,
            "content_projection": content_projection,
        }
        records.append(row)
        execution_rows.append({"task_id": task["task_id"], "summaries": summaries})
        model_rows.append(
            {"task_id": task["task_id"], "category": category_check, "hott": hott_check}
        )
        witness_rows.append(
            {
                "task_id": task["task_id"],
                "category_mismatches": (
                    category_check["mismatch_elements"] if category_check else []
                ),
                "hott_round_trip": (
                    hott_check["round_trip_holds"] if hott_check else None
                ),
            }
        )
    return {
        "output_kind": "formal_lens",
        "lens": lens,
        "records": records,
        "formal_execution": {
            "scope": "shared_typed_finite_engine_parent_replay_plus_isolated_projection",
            "status": (
                "finite_task_specific_checks_executed"
                if lens in {"categorical", "hott", "combined"}
                else "control_without_checked_formal_relations"
            ),
            "artifact_summary_digest": _digest(execution_rows),
            "model_digest": _digest(model_rows),
            "witness_digest": _digest(witness_rows),
            "formal_semantics": (
                "task_derived_typed_finite_category_and_or_discrete_hott_shared_engine"
                if invoked
                else "count_matched_control_without_formal_replay"
            ),
            "theorem_authorized": False,
            "continuum_authorized": False,
            "physics_value_authorized": False,
            "conceptual_advantage_authorized": False,
        },
    }


def _reflection(payload: Mapping[str, Any]) -> dict[str, Any]:
    candidate_rows = payload.get("candidate_maturation")
    high_risk_rows = payload.get("high_risk_maturation")
    formal_rows = payload.get("formal_rows")
    if not all(isinstance(rows, list) for rows in (candidate_rows, high_risk_rows, formal_rows)):
        raise ValueError("reflection requires both matured branches and the formal handback")
    by_task = {
        str(row["task_id"]): row for row in formal_rows if isinstance(row, Mapping)
    }
    high_by_task: dict[str, list[Mapping[str, Any]]] = {}
    for row in high_risk_rows:
        if not isinstance(row, Mapping):
            raise ValueError("high-risk maturation row must be an object")
        high_by_task.setdefault(str(row["task_id"]), []).append(row)
    records = []
    for candidate in candidate_rows:
        if not isinstance(candidate, Mapping):
            raise ValueError("candidate maturation row must be an object")
        task_id = str(candidate["task_id"])
        high = high_by_task.get(task_id)
        formal = by_task.get(task_id)
        if high is None or formal is None:
            raise ValueError("reflection inputs are not task-total")
        high = sorted(high, key=lambda row: str(row["proposal_content"]["corner_family"]))
        portfolio = [dict(row["proposal_content"]) for row in high]
        families = [str(row["corner_family"]) for row in portfolio]
        mechanisms = [str(row["mechanism"]) for row in portfolio]
        if (
            len(portfolio) != 10
            or len(set(families)) < 6
            or len(set(mechanisms)) < 8
            or sum(int(row["is_control"] is True) for row in portfolio) != 1
            or sum(int(row["is_wildcard"] is True) for row in portfolio) < 2
        ):
            raise ValueError("reflection requires one diverse ten-corner portfolio per task")
        radical = next(row for row in portfolio if not row["is_control"])
        control = next(row for row in portfolio if row["is_control"])
        wildcard = next(row for row in portfolio if row["is_wildcard"])
        route_status = _text(payload.get("route_status"))
        convergence_status = (
            "quarantined_source_authority"
            if route_status in {"quarantined", "rejected_target_mismatch"}
            else "plural_incubation"
        )
        records.append(
            {
                "reflection_id": _identifier(
                    "matched-reflection",
                    candidate["maturation_id"],
                    [row["maturation_id"] for row in high],
                    formal["formal_id"],
                ),
                "task_id": task_id,
                "rounds": [
                    {
                        "round_id": "round-1-tension",
                        "tension": (
                            f"Candidate mechanism: {candidate['proposal_content']['mechanism']} "
                            f"Ten noncollapsed corners: {families}"
                        ),
                        "mutation": (
                            f"Preserve the candidate anchors {candidate['semantic_anchors']} while testing "
                            f"the radical mechanism {radical['mechanism']} against the capable control "
                            f"{control['mechanism']}."
                        ),
                        "preserved_differences": list(candidate["protected_differences"]),
                        "question": radical["decisive_question"],
                    },
                    {
                        "round_id": "round-2-wildcard-premortem",
                        "tension": f"Protected wildcard: {wildcard['statement']}",
                        "mutation": (
                            f"Run its premortem {wildcard['premortem']} without allowing sibling "
                            "conclusions to erase the branch-specific failure."
                        ),
                        "preserved_differences": list(high[0]["protected_differences"]),
                        "question": wildcard["decisive_question"],
                    },
                    {
                        "round_id": "round-3-formal-handback",
                        "tension": f"Localized formal burden: {formal['burden_localization']}",
                        "mutation": (
                            f"Return every surviving corner to the task correction condition "
                            f"{formal['falsifier']} before convergence."
                        ),
                        "preserved_differences": list(high[0]["protected_differences"]),
                        "question": formal["falsifier"],
                    },
                ],
                "synthesis": (
                    f"Incubate the candidate alongside ten structurally distinct corners; retain "
                    f"the capable control and protected wildcards around {formal['burden_localization']}."
                ),
                "unification_edges": [
                    {
                        "source_anchor": candidate["proposal_content"]["mechanism"],
                        "target_anchor": formal["content_projection"]["semantic_anchor"],
                        "preserved_difference": candidate["protected_differences"][0],
                    },
                    {
                        "source_anchor": radical["mechanism"],
                        "target_anchor": formal["falsifier"],
                        "preserved_difference": high[0]["protected_differences"][1],
                    },
                    {
                        "source_anchor": wildcard["ontology_delta"]["new_primitive"],
                        "target_anchor": control["ontology_delta"]["new_primitive"],
                        "preserved_difference": "wildcard restructuring versus capable incumbent deepening",
                    },
                ],
                "correction_conditions": list(
                    dict.fromkeys(
                        [
                            *candidate["correction_paths"],
                            *[
                                correction
                                for row in high
                                for correction in row["correction_paths"]
                            ],
                        ]
                    )
                ),
                "conceptual_content": {
                    "candidate": candidate["proposal_content"],
                    "high_risk_portfolio": portfolio,
                    "portfolio_structure": {
                        "portfolio_id": portfolio[0]["portfolio_id"],
                        "corner_families": families,
                        "mechanism_signatures": [_digest(value) for value in mechanisms],
                        "structural_branch_count": len(portfolio),
                        "protected_wildcard_count": sum(
                            int(row["is_wildcard"] is True) for row in portfolio
                        ),
                        "capable_control_count": sum(
                            int(row["is_control"] is True) for row in portfolio
                        ),
                        "all_branch_barriers_complete": all(
                            row["parallel_contract"]["join_after_all_terminal"] is True
                            and row["parallel_contract"]["shared_mutable_state"] is False
                            for row in portfolio
                        ),
                    },
                    "candidate_mechanism_steps": list(candidate["explicit_mechanism_steps"]),
                    "high_risk_mechanism_steps": [
                        list(row["explicit_mechanism_steps"]) for row in high
                    ],
                    "semantic_anchors": list(candidate["semantic_anchors"]),
                },
                "convergence_status": convergence_status,
                "opportunity_count": 1,
            }
        )
    return {"output_kind": "reflection", "records": records}


def _blind_judgment(payload: Mapping[str, Any]) -> dict[str, Any]:
    packets = payload.get("blinded_packets")
    if not isinstance(packets, list) or not packets:
        raise ValueError("blind judgment requires blinded packets")
    forbidden = {
        "condition_id",
        "provider_id",
        "strategy_id",
        "arm",
        "lens",
        "formal_status",
        "literature_world_id",
        "original_candidate_id",
    }
    records = []
    for packet in packets:
        if not isinstance(packet, Mapping) or forbidden.intersection(packet):
            raise ValueError("judge packet leaks an intervention label")
        required = {"opaque_candidate_id", "task_token", "task_rubric", "reflection", "formal"}
        if set(packet) != required:
            raise ValueError("judge packet must contain only the blinded evidence projection")
        reflection = packet["reflection"]
        formal = packet["formal"]
        task = packet["task_rubric"]
        if not all(isinstance(row, Mapping) for row in (reflection, formal, task)):
            raise ValueError("judge evidence is malformed")
        rounds = reflection.get("rounds", [])
        edges = reflection.get("unification_edges", [])
        corrections = reflection.get("correction_conditions", [])
        conceptual = reflection.get("conceptual_content")
        projection = formal.get("content_projection")
        if not isinstance(conceptual, Mapping) or not isinstance(projection, Mapping):
            raise ValueError("judge evidence lacks a content projection")
        complete_rounds = sum(
            isinstance(row, Mapping)
            and all(_text(row.get(key)) for key in ("tension", "mutation", "question"))
            and bool(row.get("preserved_differences"))
            for row in rounds
        )
        task_invariants = set(task.get("protected_invariants", []))
        semantic_anchors = set(conceptual.get("semantic_anchors", []))
        candidate = conceptual.get("candidate", {})
        portfolio = conceptual.get("high_risk_portfolio", [])
        portfolio_structure = conceptual.get("portfolio_structure", {})
        handback = projection.get("physics_handback")
        correction_obligations = projection.get("correction_obligations", [])
        if (
            not isinstance(candidate, Mapping)
            or not isinstance(portfolio, list)
            or not all(isinstance(row, Mapping) for row in portfolio)
            or not isinstance(portfolio_structure, Mapping)
        ):
            raise ValueError("judge evidence lacks a structured candidate portfolio")
        transformation = candidate.get("strategy_transformation", {})
        families = [str(row.get("corner_family", "")) for row in portfolio]
        mechanisms = [str(row.get("mechanism", "")) for row in portfolio]
        ontology_primitives = [
            str(row.get("ontology_delta", {}).get("new_primitive", ""))
            if isinstance(row.get("ontology_delta"), Mapping)
            else ""
            for row in portfolio
        ]
        premortems = [str(row.get("premortem", "")) for row in portfolio]
        decisive_questions = [str(row.get("decisive_question", "")) for row in portfolio]
        branch_falsifiers = [str(row.get("falsifier", "")) for row in portfolio]
        all_risk_rows = [
            axis
            for row in portfolio
            for axis in [*row.get("risk_axes", []), *row.get("reward_axes", [])]
            if isinstance(axis, Mapping)
        ]
        anchor_preserved = projection.get("semantic_anchor") in task_invariants
        falsifier_preserved = (
            len(portfolio) == 10
            and set(branch_falsifiers) == {task.get("falsifier")}
            and task.get("falsifier") in correction_obligations
        )
        carrier_preserved = (
            task.get("physical_carrier") is None
            or (
                isinstance(handback, Mapping)
                and handback.get("physical_carrier") == task.get("physical_carrier")
            )
        )
        mechanism_preserved = (
            bool(_text(candidate.get("mechanism")))
            and task_invariants.issubset(semantic_anchors)
        )
        portfolio_target_alignment = (
            len(portfolio) == 10
            and all(row.get("target_pressure") == task.get("pressure") for row in portfolio)
            and all(
                set(row.get("protected_invariants", [])) == task_invariants
                for row in portfolio
            )
        )
        structural_diversity = (
            len(set(families)) >= 6
            and len(set(mechanisms)) >= 8
            and len(set(ontology_primitives)) >= 8
            and all(_text(value) for value in [*mechanisms, *ontology_primitives])
        )
        portfolio_controls = (
            sum(int(row.get("is_wildcard") is True) for row in portfolio) >= 2
            and sum(int(row.get("is_control") is True) for row in portfolio) == 1
        )
        branch_independence = (
            portfolio_structure.get("structural_branch_count") == 10
            and portfolio_structure.get("all_branch_barriers_complete") is True
            and len(set(portfolio_structure.get("mechanism_signatures", []))) >= 8
        )
        transformation_valid = (
            isinstance(transformation, Mapping)
            and all(
                _text(transformation.get(field))
                for field in (
                    "operator",
                    "new_primitive",
                    "new_relation",
                    "mechanism_delta",
                    "preserved_invariant",
                    "decisive_question",
                )
            )
            and transformation.get("preserved_invariant") in task_invariants
            and isinstance(transformation.get("mechanism_chain"), list)
            and len(transformation["mechanism_chain"]) == 3
        )
        risk_content_valid = (
            len(all_risk_rows) == 40
            and all(_text(row.get("rationale")) for row in all_risk_rows)
            and len(set(premortems)) >= 8
            and all(_text(value) for value in decisive_questions)
        )
        valid_edges = sum(
            isinstance(row, Mapping)
            and bool(_text(row.get("source_anchor")))
            and bool(_text(row.get("target_anchor")))
            and bool(_text(row.get("preserved_difference")))
            for row in edges
        )
        changed_decision = _text(projection.get("changed_next_decision"))
        burden = _text(projection.get("localized_burden"))
        scores = {
            "relevance": min(
                4,
                int(anchor_preserved)
                + int(falsifier_preserved)
                + int(carrier_preserved)
                + int(mechanism_preserved and portfolio_target_alignment),
            ),
            "depth": min(
                4,
                int(complete_rounds >= 3)
                + int(transformation_valid)
                + int(structural_diversity)
                + int(len(set(premortems)) >= 8),
            ),
            "unification": min(
                4,
                int(valid_edges >= 3)
                + int(task_invariants.issubset(semantic_anchors))
                + int(structural_diversity)
                + int(branch_independence),
            ),
            "risk_reward": min(
                4,
                int(risk_content_valid)
                + int(falsifier_preserved)
                + int(portfolio_controls)
                + int(len(corrections) >= 3),
            ),
            "burden_localization": min(
                4,
                int(anchor_preserved)
                + int(falsifier_preserved)
                + int(bool(burden))
                + int(bool(changed_decision)),
            ),
        }
        hard_gate = (
            "hold"
            if reflection.get("convergence_status") == "quarantined_source_authority"
            else "pass_internal_structure_only"
        )
        records.append(
            {
                "opaque_candidate_id": str(packet["opaque_candidate_id"]),
                "task_token": str(packet["task_token"]),
                "dimension_scores": scores,
                "hard_gate": hard_gate,
                "semantic_diagnostics": {
                    "candidate_mechanism_signature": _digest(
                        {
                            "mechanism": candidate.get("mechanism"),
                            "transformation": transformation,
                        }
                    ),
                    "portfolio_signature": _digest(
                        [
                            {
                                "corner_family": row.get("corner_family"),
                                "mechanism": row.get("mechanism"),
                                "ontology_delta": row.get("ontology_delta"),
                                "risk_axes": row.get("risk_axes"),
                                "reward_axes": row.get("reward_axes"),
                                "premortem": row.get("premortem"),
                            }
                            for row in portfolio
                        ]
                    ),
                    "portfolio_target_alignment": portfolio_target_alignment,
                    "structural_diversity": structural_diversity,
                    "risk_content_valid": risk_content_valid,
                    "branch_independence": branch_independence,
                    "formal_task_delta_present": bool(
                        projection.get("task_derived_formal_delta")
                    ),
                },
                "reasons": [
                    "Scores are a task-anchored rule-based content screen under a blinded local process.",
                    "Substantive mechanisms, task translations, risks, and corrections matter; slot counts, invocation, arm identity, and status do not.",
                    "They do not measure creativity, philosophical depth, truth, or physics value.",
                ],
                "opportunity_count": 1,
            }
        )
    return {
        "output_kind": "blind_judgment",
        "records": records,
        "judge_authority": {
            "status": "internal_process_blind_only",
            "condition_labels_withheld": True,
            "strategy_labels_withheld": True,
            "arm_labels_withheld": True,
            "authority_distinct_status": "unavailable",
            "cognitive_independence_authorized": False,
        },
    }


def _convergence(payload: Mapping[str, Any]) -> dict[str, Any]:
    judgments = payload.get("judgments")
    if not isinstance(judgments, list) or not judgments:
        raise ValueError("convergence requires blind judgments")
    records = []
    for row in judgments:
        if not isinstance(row, Mapping):
            raise ValueError("judgment row must be an object")
        decision = (
            "revise_all"
            if row.get("hard_gate") == "hold"
            else "plural_incubation"
        )
        records.append(
            {
                "task_token": str(row["task_token"]),
                "preference_set": (
                    [] if decision == "revise_all" else [str(row["opaque_candidate_id"])]
                ),
                "decision": decision,
                "reason": (
                    "Source authority is insufficient; revise before investment."
                    if decision == "revise_all"
                    else "Retain the structurally admissible candidate as an incubating member of a plural set."
                ),
                "promotion_authorized": False,
                "truth_authorized": False,
                "opportunity_count": 1,
            }
        )
    return {"output_kind": "convergence", "records": records}


def _isolation_probe(payload: Mapping[str, Any]) -> dict[str, Any]:
    read_path = Path(str(payload.get("read_path", "/nonexistent")))
    write_path = Path(str(payload.get("write_path", "/nonexistent")))
    secret_name = _text(payload.get("secret_name"))
    network_host = _text(payload.get("network_host")) or "127.0.0.1"
    network_port = int(payload.get("network_port", 9))
    if not 1 <= network_port <= 65535:
        raise ValueError("isolation probe network_port is outside the TCP range")
    read_succeeded = False
    write_succeeded = False
    socket_succeeded = False
    errors: list[str] = []
    try:
        read_path.read_bytes()
        read_succeeded = True
    except OSError as exc:
        errors.append(f"read:{type(exc).__name__}")
    try:
        write_path.write_text("isolation-probe", encoding="utf-8")
        write_succeeded = True
    except OSError as exc:
        errors.append(f"write:{type(exc).__name__}")
    try:
        connection = socket.create_connection((network_host, network_port), timeout=0.2)
        connection.close()
        socket_succeeded = True
    except OSError as exc:
        errors.append(f"network:{type(exc).__name__}")
    return {
        "output_kind": "isolation_probe",
        "read_succeeded": read_succeeded,
        "write_succeeded": write_succeeded,
        "network_connection_succeeded": socket_succeeded,
        "secret_environment_present": bool(secret_name and os.environ.get(secret_name)),
        "errors": sorted(errors),
    }


def _dispatch(role: str, operation: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    expected_roles = {
        "candidate_generation": {"candidate"},
        "high_risk_generation": {"high_risk"},
        "parallel_maturation": {"candidate", "high_risk"},
        "formal_lens": {"formal_lens"},
        "reflection": {"candidate"},
        "blind_judgment": {"judge"},
        "convergence": {"judge"},
        "isolation_probe": ROLES,
    }
    if role not in expected_roles[operation]:
        raise ValueError(f"role {role!r} cannot execute {operation!r}")
    handlers = {
        "candidate_generation": _candidate_generation,
        "high_risk_generation": _high_risk_generation,
        "parallel_maturation": _parallel_maturation,
        "formal_lens": _formal_lens,
        "reflection": _reflection,
        "blind_judgment": _blind_judgment,
        "convergence": _convergence,
        "isolation_probe": _isolation_probe,
    }
    return handlers[operation](payload)


def _validate_isolation_requirement(raw: Any) -> None:
    required = {
        "schema_version",
        "kernel_isolation_required",
        "minimum_accepted_status",
        "selected_backend",
        "selected_backend_probe_status",
        "content_digest",
    }
    if not isinstance(raw, Mapping) or set(raw) != required:
        raise ValueError("worker isolation requirement must be a closed object")
    kernel_required = raw["kernel_isolation_required"]
    expected_minimum = (
        "kernel_policy_enforced" if kernel_required is True else "strongest_available"
    )
    core = {key: value for key, value in raw.items() if key != "content_digest"}
    if (
        raw["schema_version"] != 1
        or not isinstance(kernel_required, bool)
        or raw["minimum_accepted_status"] != expected_minimum
        or raw["selected_backend"]
        not in {"macos_sandbox_exec", "linux_bubblewrap", "process_group_only"}
        or raw["selected_backend_probe_status"]
        not in {"passed", "unavailable", "failed"}
        or raw["content_digest"] != _digest(core)
    ):
        raise ValueError("worker isolation requirement is invalid")


def main() -> int:
    try:
        request = json.load(sys.stdin)
        required = {
            "schema_version",
            "study_id",
            "role",
            "operation",
            "request_nonce",
            "invocation_context",
            "payload",
            "payload_digest",
            "isolation_requirement",
            "fault_mode",
        }
        if not isinstance(request, Mapping) or set(request) != required:
            raise ValueError("worker request must have the exact closed envelope")
        if request["schema_version"] != 1:
            raise ValueError("unsupported worker request version")
        role = _text(request["role"])
        operation = _text(request["operation"])
        if role not in ROLES or operation not in OPERATIONS:
            raise ValueError("unknown worker role or operation")
        payload = request["payload"]
        if not isinstance(payload, Mapping) or request["payload_digest"] != _digest(payload):
            raise ValueError("worker payload digest mismatch")
        if not isinstance(request["invocation_context"], Mapping):
            raise ValueError("worker invocation context must be an object")
        _validate_isolation_requirement(request["isolation_requirement"])
        fault_mode = request["fault_mode"]
        if fault_mode not in {None, "exit_nonzero", "invalid_json", "hang"}:
            raise ValueError("unknown fault mode")
        if fault_mode == "exit_nonzero":
            return 17
        if fault_mode == "invalid_json":
            sys.stdout.write("{")
            return 0
        if fault_mode == "hang":
            # The parent resource governor must terminate the entire isolated
            # process group; this branch exists solely for deterministic
            # deadline and immutable failure-receipt regressions.
            time.sleep(60.0)
        output = _dispatch(role, operation, payload)
        environment = {name: os.environ[name] for name in sorted(os.environ)}
        response = {
            "schema_version": 1,
            "role": role,
            "operation": operation,
            "request_nonce": str(request["request_nonce"]),
            "environment_observation": {
                "names": sorted(environment),
                "values_digest": _digest(environment),
                "working_directory": str(Path.cwd().resolve()),
            },
            "output": output,
        }
        sys.stdout.buffer.write(_canonical_json(response) + b"\n")
        return 0
    except Exception as exc:
        error = {
            "status": "worker_protocol_error",
            "error_type": type(exc).__name__,
            "message": str(exc),
        }
        sys.stderr.buffer.write(_canonical_json(error) + b"\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
