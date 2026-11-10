# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Run publication-disabled matched studies over the discovery workflow.

This module turns the Cycle-600 study design into an executable causal object.
It runs three independent-cluster families: eight synthetic literature
descriptors, four internal generation-strategy descriptors, and seven
Category/HoTT/control arms.  These are structural calibration treatments, not
executions of the production source-authority or discovery-operator chain.
Every
condition receives the same tasks, frozen ancestor, eight-stage schedule,
generation opportunities, literature slots, and resource profile.

The eight stages are not a flat checklist.  Candidate and high-risk proposals
are generated first, their two maturation branches execute concurrently behind
an explicit barrier, and formalization, reflection, blind local judgment, and
convergence run only after both branches succeed.  A failed branch never erases
its sibling receipt or another cell.  Re-running a partial study reuses exact
successful receipts and creates a distinct immutable attempt for the repaired
request.

The judge receives only opaque task/candidate tokens plus sanitized reflection
and formal handback fields.  This is process blinding, not cognitive or
authority-distinct independence.  Statistics are deterministic descriptive
means over task clusters and only over *matched-complete repetitions*—a
repetition is excluded for every condition in a family if any condition is
incomplete.  PID, timestamps, command paths, workspaces, and resource telemetry
are absent from the scientific projection.  No study output authorizes
publication, truth, theorem status, creativity, depth, unification, physics
value, advantage, or population generalization.
"""

from __future__ import annotations

import copy
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Mapping, Sequence

from .benchmark_process import _load_json_object, _top_level_content_digest, _write_immutable_json
from .budgets import contained_path
from .contracts import (
    bytes_digest,
    canonical_digest,
    canonical_json,
    file_digest,
    stable_identifier,
    validate_identifier,
    validate_payload,
)
from .research_worker_isolation import (
    ResearchWorkerAdapter,
    ResearchWorkerIntegrityError,
    receipt_summary,
    validate_research_worker_receipt,
)
from skills.common.abstraction_formal_reasoning import (
    run_condition_forger,
    validate_condition_forger_result,
)
from .hypotheses import structural_corner_descriptors


STUDY_SCHEMA = "matched_discovery_study.schema.json"
DIMENSIONS = (
    "relevance",
    "depth",
    "unification",
    "risk_reward",
    "burden_localization",
)
ARMS = (
    "incumbent",
    "categorical",
    "hott",
    "combined",
    "no_abstraction",
    "decorative",
    "restatement",
)
LITERATURE_WORLD_IDS = (
    "current_v3",
    "historical_v2",
    "no_literature",
    "version_naive",
    "surveillance_only",
    "lane_drop",
    "ambiguous_lineage",
    "target_mismatch",
)
STRATEGY_IDS = (
    "incumbent_systematic",
    "mechanism_inversion",
    "boundary_object_transfer",
    "failure_first_counterfactual",
)
STAGE_SCHEDULE = (
    ("candidate_generation", "candidate", "candidate_generation"),
    ("high_risk_generation", "high_risk", "high_risk_generation"),
    ("candidate_maturation", "candidate", "parallel_maturation"),
    ("high_risk_maturation", "high_risk", "parallel_maturation"),
    ("formal_lens", "formal_lens", "formal_lens"),
    ("reflection", "candidate", "reflection"),
    ("blind_judgment", "judge", "blind_judgment"),
    ("convergence", "judge", "convergence"),
)
STAGE_BY_ROLE_OPERATION = {
    (role, operation): stage_id for stage_id, role, operation in STAGE_SCHEDULE
}
OPERATIONAL_PROJECTION_FIELDS = (
    "command",
    "completed_at",
    "elapsed_seconds",
    "environment_observation",
    "pid",
    "resource_receipt",
    "started_at",
    "workspace",
)


def _corner_descriptor_catalog() -> list[dict[str, Any]]:
    """Replay the production high-risk corner vocabulary as a closed input."""

    rows = structural_corner_descriptors()
    if len(rows) != 10:
        raise MatchedStudyIntegrityError(
            "matched high-risk calibration requires the exact ten-corner production catalog"
        )
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
    families: set[str] = set()
    controls = 0
    wildcards = 0
    for row in rows:
        if set(row) != required:
            raise MatchedStudyIntegrityError("conceptual-corner descriptor fields drifted")
        core = {key: copy.deepcopy(value) for key, value in row.items() if key != "descriptor_digest"}
        if row["descriptor_digest"] != canonical_digest(core):
            raise MatchedStudyIntegrityError("conceptual-corner descriptor digest drifted")
        families.add(str(row["corner_family"]))
        controls += int(row["is_control"] is True)
        wildcards += int(row["is_wildcard"] is True)
    if len(families) < 6 or controls != 1 or wildcards < 2:
        raise MatchedStudyIntegrityError(
            "conceptual-corner catalog lost diversity, its capable control, or wildcards"
        )
    return copy.deepcopy(rows)


class MatchedStudyIntegrityError(ResearchWorkerIntegrityError):
    """Raised when a matched plan, receipt chain, or report fails closed."""


def _require_exact_keys(raw: Mapping[str, Any], keys: set[str], label: str) -> None:
    if set(raw) != keys:
        raise MatchedStudyIntegrityError(f"{label} does not have its exact closed fields")


def _require_nonempty_text(value: Any, label: str) -> str:
    text = " ".join(str(value or "").strip().split())
    if not text:
        raise MatchedStudyIntegrityError(f"{label} must be substantive text")
    return text


def _require_unique_text_list(value: Any, label: str, *, minimum: int = 1) -> list[str]:
    if not isinstance(value, list) or len(value) < minimum:
        raise MatchedStudyIntegrityError(f"{label} must contain at least {minimum} rows")
    rows = [_require_nonempty_text(item, label) for item in value]
    if len(rows) != len(set(rows)):
        raise MatchedStudyIntegrityError(f"{label} must be unique")
    return rows


def load_matched_study_fixture(path: Path | str) -> dict[str, Any]:
    """Load the exact independent-cluster fixture without inferring authority.

    The fixture is repository-authored.  Validation proves its closed study
    design and equal scheduled opportunities; it cannot establish hidden-task,
    external-human, cognitive-independence, or population authority.
    """

    fixture_path = Path(path).resolve(strict=True)
    if fixture_path.is_symlink() or not fixture_path.is_file():
        raise MatchedStudyIntegrityError("matched-study fixture is not a regular file")
    fixture = _load_json_object(fixture_path)
    _require_exact_keys(
        fixture,
        {
            "schema_version",
            "fixture_id",
            "authorship",
            "default_repetitions",
            "blinding_salt_id",
            "stage_schedule",
            "budget_profile",
            "tasks",
            "literature_worlds",
            "study_authority",
            "descriptor_artifacts",
            "strategies",
            "arms",
        },
        "matched-study fixture",
    )
    if fixture["schema_version"] != 2:
        raise MatchedStudyIntegrityError("unsupported matched-study fixture version")
    validate_identifier(str(fixture["fixture_id"]), "fixture_id")
    validate_identifier(str(fixture["blinding_salt_id"]), "blinding_salt_id")
    if not isinstance(fixture["default_repetitions"], int) or fixture["default_repetitions"] < 1:
        raise MatchedStudyIntegrityError("default repetitions must be positive")

    authorship = fixture["authorship"]
    if not isinstance(authorship, Mapping):
        raise MatchedStudyIntegrityError("fixture authorship must be an object")
    _require_exact_keys(
        authorship,
        {
            "status",
            "external_human_authority_status",
            "held_out_population_status",
            "independence_boundary",
        },
        "fixture authorship",
    )
    if (
        authorship["status"] != "repository_authored_independent_cluster_design"
        or authorship["external_human_authority_status"] != "unavailable"
        or authorship["held_out_population_status"] != "unavailable"
    ):
        raise MatchedStudyIntegrityError("fixture overstates authorship or external authority")
    _require_nonempty_text(authorship["independence_boundary"], "independence boundary")

    if fixture["study_authority"] != {
        "mode": "synthetic_structural_descriptor_calibration",
        "production_source_authority_executed": False,
        "production_discovery_operators_executed": False,
        "external_provider_plurality_status": "unavailable",
        "causal_effect_authorized": False,
    }:
        raise MatchedStudyIntegrityError("fixture overstates production treatment authority")
    artifacts = fixture["descriptor_artifacts"]
    if not isinstance(artifacts, list) or len(artifacts) != 1:
        raise MatchedStudyIntegrityError("fixture must bind one checked-in descriptor artifact")
    artifact = artifacts[0]
    if not isinstance(artifact, Mapping):
        raise MatchedStudyIntegrityError("descriptor artifact must be an object")
    _require_exact_keys(
        artifact,
        {
            "artifact_id",
            "repository_path",
            "file_sha256",
            "byte_length",
            "declared_content_digest",
            "use",
            "production_chain_executed",
        },
        "descriptor artifact",
    )
    relative = Path(str(artifact["repository_path"]))
    if relative.is_absolute() or ".." in relative.parts:
        raise MatchedStudyIntegrityError("descriptor artifact path escapes the repository")
    artifact_path = contained_path(Path(__file__).resolve().parents[2], *relative.parts)
    artifact_payload = _load_json_object(artifact_path)
    if (
        artifact_path.is_symlink()
        or not artifact_path.is_file()
        or artifact["file_sha256"] != file_digest(artifact_path)
        or artifact["byte_length"] != artifact_path.stat().st_size
        or artifact["declared_content_digest"] != artifact_payload.get("content_digest")
        or artifact["use"] != "immutable_descriptor_context_only_not_executed"
        or artifact["production_chain_executed"] is not False
    ):
        raise MatchedStudyIntegrityError("descriptor artifact authority or bytes changed")

    expected_schedule = [
        {"stage_id": stage_id, "role": role, "operation": operation}
        for stage_id, role, operation in STAGE_SCHEDULE
    ]
    if fixture["stage_schedule"] != expected_schedule:
        raise MatchedStudyIntegrityError("fixture does not declare the exact eight-stage schedule")
    if fixture["budget_profile"] != ResearchWorkerAdapter.default_budget():
        raise MatchedStudyIntegrityError("fixture worker budget differs from the matched profile")

    tasks = fixture["tasks"]
    if not isinstance(tasks, list) or len(tasks) != 6:
        raise MatchedStudyIntegrityError("fixture must contain exactly six independent tasks")
    task_fields = {
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
    task_ids: list[str] = []
    cluster_ids: list[str] = []
    for index, task in enumerate(tasks):
        if not isinstance(task, Mapping):
            raise MatchedStudyIntegrityError("fixture task must be an object")
        _require_exact_keys(task, task_fields, f"fixture task {index}")
        task_id = validate_identifier(str(task["task_id"]), "task_id")
        cluster_id = validate_identifier(str(task["cluster_id"]), "cluster_id")
        task_ids.append(task_id)
        cluster_ids.append(cluster_id)
        for field in ("domain", "pressure", "formal_pressure", "falsifier"):
            _require_nonempty_text(task[field], f"task {task_id} {field}")
        _require_unique_text_list(task["protected_invariants"], "protected invariants")
        _require_unique_text_list(task["incumbent_primitives"], "incumbent primitives")
        if task["physical_carrier"] is not None:
            _require_nonempty_text(task["physical_carrier"], "physical carrier")
    if len(task_ids) != len(set(task_ids)) or len(cluster_ids) != len(set(cluster_ids)):
        raise MatchedStudyIntegrityError("tasks and clusters must be one-to-one and unique")

    worlds = fixture["literature_worlds"]
    if not isinstance(worlds, list) or [row.get("world_id") for row in worlds] != list(
        LITERATURE_WORLD_IDS
    ):
        raise MatchedStudyIntegrityError("fixture literature worlds are not exact and ordered")
    world_fields = {
        "world_id",
        "label",
        "scheduled_lane_count",
        "admitted_source_count",
        "route_status",
        "intervention",
        "descriptor_artifact_ids",
        "production_chain_executed",
        "causal_effect_authorized",
    }
    for world in worlds:
        if not isinstance(world, Mapping):
            raise MatchedStudyIntegrityError("literature world must be an object")
        _require_exact_keys(world, world_fields, "literature world")
        if world["scheduled_lane_count"] != 6:
            raise MatchedStudyIntegrityError("every literature world must schedule six lanes")
        if not isinstance(world["admitted_source_count"], int) or not 0 <= world[
            "admitted_source_count"
        ] <= 6:
            raise MatchedStudyIntegrityError("admitted source count is outside the six-lane design")
        for field in ("label", "route_status", "intervention"):
            _require_nonempty_text(world[field], f"literature world {field}")
        if (
            not isinstance(world["descriptor_artifact_ids"], list)
            or not set(world["descriptor_artifact_ids"]).issubset({artifact["artifact_id"]})
            or world["production_chain_executed"] is not False
            or world["causal_effect_authorized"] is not False
        ):
            raise MatchedStudyIntegrityError("literature descriptor overstates causal authority")

    strategies = fixture["strategies"]
    if not isinstance(strategies, list) or [row.get("strategy_id") for row in strategies] != list(
        STRATEGY_IDS
    ):
        raise MatchedStudyIntegrityError("fixture strategy descriptors are not exact and ordered")
    strategy_fields = {
        "strategy_id",
        "strategy_kind",
        "strategy",
        "external_provider_authority_status",
        "provider_plurality_authorized",
    }
    for strategy in strategies:
        if not isinstance(strategy, Mapping):
            raise MatchedStudyIntegrityError("strategy descriptor must be an object")
        _require_exact_keys(strategy, strategy_fields, "strategy descriptor")
        if (
            strategy["strategy_kind"] != "synthetic_internal_deterministic_descriptor"
            or strategy["external_provider_authority_status"] != "unavailable"
            or strategy["provider_plurality_authorized"] is not False
        ):
            raise MatchedStudyIntegrityError("strategy descriptor was relabelled as provider plurality")
        _require_nonempty_text(strategy["strategy"], "strategy descriptor")
    if fixture["arms"] != list(ARMS):
        raise MatchedStudyIntegrityError("fixture formal arms are not exact and ordered")
    return copy.deepcopy(fixture)


def _fixture_record(path: Path, fixture: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "fixture_id": fixture["fixture_id"],
        "fixture_path": str(path),
        "file_sha256": file_digest(path),
        "semantic_digest": canonical_digest(fixture),
        "task_count": len(fixture["tasks"]),
        "task_cluster_count": len({row["cluster_id"] for row in fixture["tasks"]}),
        "authorship_status": fixture["authorship"]["status"],
        "external_human_authority_status": "unavailable",
        "calibration_mode": fixture["study_authority"]["mode"],
        "descriptor_artifact_count": len(fixture["descriptor_artifacts"]),
        "production_chain_execution_status": "not_executed",
    }


def _condition(
    *, family_id: str, world_id: str, strategy_id: str, arm: str, ancestor_digest: str
) -> dict[str, Any]:
    core = {
        "family_id": family_id,
        "literature_world_id": world_id,
        "strategy_id": strategy_id,
        "arm": arm,
        "frozen_ancestor_digest": ancestor_digest,
    }
    return {
        "condition_id": stable_identifier("matched-condition", core),
        "literature_world_id": world_id,
        "strategy_id": strategy_id,
        "arm": arm,
        "frozen_ancestor_digest": ancestor_digest,
        "descriptor_digest": canonical_digest(core),
    }


def _formal_case(task: Mapping[str, Any], lens: str) -> dict[str, Any]:
    """Bind the shared finite formal engine to one complete task descriptor."""

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


def _build_typed_formal_catalog(
    fixture: Mapping[str, Any],
) -> dict[tuple[str, str], dict[str, Any]]:
    """Build and replay task-bound artifacts with the repository's shared engine.

    The isolated worker is deliberately standard-library-only.  Formal
    semantics therefore execute at this trusted parent boundary; their exact
    artifacts cross the subprocess request, and report reopening regenerates
    and revalidates them from the live transitive dependency authority.
    """

    catalog: dict[tuple[str, str], dict[str, Any]] = {}
    for lens in ("categorical", "hott"):
        cases = [_formal_case(task, lens) for task in fixture["tasks"]]
        result = run_condition_forger(lens, cases)
        validate_condition_forger_result(result, lens, cases)
        artifacts = result["artifacts"]
        if len(artifacts) != len(cases):
            raise MatchedStudyIntegrityError(
                "shared formal engine did not return one artifact per task"
            )
        for artifact in artifacts:
            key = (str(artifact["target_id"]), lens)
            if key in catalog:
                raise MatchedStudyIntegrityError(
                    "shared formal engine duplicated a task/lens artifact"
                )
            catalog[key] = copy.deepcopy(dict(artifact))
    expected = {
        (str(task["task_id"]), lens)
        for task in fixture["tasks"]
        for lens in ("categorical", "hott")
    }
    if set(catalog) != expected:
        raise MatchedStudyIntegrityError("shared formal artifact catalog is not task-total")
    return catalog


def _formal_artifacts_for_arm(
    fixture: Mapping[str, Any],
    arm: str,
    catalog: Mapping[tuple[str, str], Mapping[str, Any]],
) -> list[dict[str, Any]]:
    selected_lenses = (
        ("categorical", "hott")
        if arm == "combined"
        else (arm,)
        if arm in {"categorical", "hott"}
        else ()
    )
    return [
        copy.deepcopy(dict(catalog[(str(task["task_id"]), lens)]))
        for task in fixture["tasks"]
        for lens in selected_lenses
    ]


def _candidate_generation_arm(
    family: Mapping[str, Any], condition: Mapping[str, Any]
) -> str:
    """Hold candidate framing fixed when the intervention is formalization."""

    if family["family_id"] == "formal_lens_structural_calibration":
        return "incumbent"
    return str(condition["arm"])


def build_matched_study_plan(
    fixture: Mapping[str, Any], *, repetitions: int
) -> list[dict[str, Any]]:
    """Build the exact 8+4+7 condition plan before any worker executes."""

    if not isinstance(repetitions, int) or repetitions < 1:
        raise MatchedStudyIntegrityError("matched-study repetitions must be positive")
    ancestor_digest = canonical_digest(
        {
            "fixture_id": fixture["fixture_id"],
            "tasks": fixture["tasks"],
            "stage_schedule": fixture["stage_schedule"],
            "budget_profile": fixture["budget_profile"],
        }
    )
    literature_conditions = [
        _condition(
            family_id="synthetic_literature_descriptor_calibration",
            world_id=world_id,
            strategy_id="incumbent_systematic",
            arm="incumbent",
            ancestor_digest=ancestor_digest,
        )
        for world_id in LITERATURE_WORLD_IDS
    ]
    strategy_conditions = [
        _condition(
            family_id="synthetic_strategy_descriptor_calibration",
            world_id="current_v3",
            strategy_id=strategy_id,
            arm="no_abstraction",
            ancestor_digest=ancestor_digest,
        )
        for strategy_id in STRATEGY_IDS
    ]
    formal_conditions = [
        _condition(
            family_id="formal_lens_structural_calibration",
            world_id="current_v3",
            strategy_id="incumbent_systematic",
            arm=arm,
            ancestor_digest=ancestor_digest,
        )
        for arm in ARMS
    ]
    return [
        {
            "family_id": "synthetic_literature_descriptor_calibration",
            "intervention_axis": "synthetic_literature_descriptor",
            "conditions": literature_conditions,
            "repetitions": repetitions,
        },
        {
            "family_id": "synthetic_strategy_descriptor_calibration",
            "intervention_axis": "synthetic_generation_strategy_descriptor",
            "conditions": strategy_conditions,
            "repetitions": repetitions,
        },
        {
            "family_id": "formal_lens_structural_calibration",
            "intervention_axis": "finite_formalization_arm",
            "conditions": formal_conditions,
            "repetitions": repetitions,
        },
    ]


def _by_id(rows: Sequence[Mapping[str, Any]], field: str, value: str) -> dict[str, Any]:
    matches = [dict(row) for row in rows if row.get(field) == value]
    if len(matches) != 1:
        raise MatchedStudyIntegrityError(f"expected one {field}={value!r}")
    return matches[0]


def _cell_base(
    fixture: Mapping[str, Any], family: Mapping[str, Any], condition: Mapping[str, Any], repetition: int
) -> dict[str, Any]:
    task_ids = [row["task_id"] for row in fixture["tasks"]]
    cluster_ids = [row["cluster_id"] for row in fixture["tasks"]]
    world = _by_id(fixture["literature_worlds"], "world_id", condition["literature_world_id"])
    strategy = _by_id(fixture["strategies"], "strategy_id", condition["strategy_id"])
    return {
        "cell_key": stable_identifier(
            "matched-cell",
            fixture["fixture_id"],
            family["family_id"],
            condition["descriptor_digest"],
            repetition,
        ),
        "family_id": family["family_id"],
        "condition_id": condition["condition_id"],
        "repetition": repetition,
        "task_ids": task_ids,
        "task_cluster_ids": cluster_ids,
        "frozen_ancestor_digest": condition["frozen_ancestor_digest"],
        "literature_descriptor_digest": canonical_digest(world),
        "strategy_descriptor_digest": canonical_digest(strategy),
        "arm": condition["arm"],
        "stage_schedule_digest": canonical_digest(fixture["stage_schedule"]),
        "budget_profile_digest": canonical_digest(fixture["budget_profile"]),
        "scheduled_stage_count": 8,
    }


def study_fault_key(cell: Mapping[str, Any], stage_id: str) -> str:
    """Return the stable key used to inject one recoverable worker fault."""

    if stage_id not in {row[0] for row in STAGE_SCHEDULE}:
        raise MatchedStudyIntegrityError("fault plan names an unknown stage")
    return f"{cell['family_id']}/{cell['condition_id']}/r{cell['repetition']}/{stage_id}"


def _invocation_context(
    *, fixture: Mapping[str, Any], cell: Mapping[str, Any], stage_id: str
) -> dict[str, Any]:
    common = {
        "stage_id": stage_id,
        "repetition": cell["repetition"],
        "fixture_semantic_digest": canonical_digest(fixture),
        "stage_schedule_digest": cell["stage_schedule_digest"],
    }
    if stage_id in {"blind_judgment", "convergence"}:
        return {
            **common,
            "opaque_cell_token": stable_identifier(
                "matched-blind-cell", fixture["blinding_salt_id"], cell["cell_key"]
            ),
        }
    return {
        **common,
        "cell_key": cell["cell_key"],
        "family_id": cell["family_id"],
        "condition_id": cell["condition_id"],
        "frozen_ancestor_digest": cell["frozen_ancestor_digest"],
    }


def _sanitized_blind_packets(
    *, fixture: Mapping[str, Any], cell: Mapping[str, Any], reflections: Sequence[Mapping[str, Any]], formal_rows: Sequence[Mapping[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, str]]:
    formal_by_task = {str(row["task_id"]): row for row in formal_rows}
    task_by_id = {str(row["task_id"]): row for row in fixture["tasks"]}
    packets: list[dict[str, Any]] = []
    mapping_rows: list[dict[str, str]] = []
    token_to_task: dict[str, str] = {}
    for reflection in reflections:
        task_id = str(reflection["task_id"])
        formal = formal_by_task.get(task_id)
        task = task_by_id.get(task_id)
        if formal is None or task is None:
            raise MatchedStudyIntegrityError("blind projection is not task-total")
        task_token = stable_identifier(
            "matched-task-token", fixture["blinding_salt_id"], task_id
        )
        opaque_candidate_id = stable_identifier(
            "matched-opaque-candidate",
            fixture["blinding_salt_id"],
            cell["cell_key"],
            task_id,
            reflection["reflection_id"],
        )
        mapping_rows.append(
            {
                "task_id": task_id,
                "task_token": task_token,
                "opaque_candidate_id": opaque_candidate_id,
            }
        )
        token_to_task[task_token] = task_id
        packets.append(
            {
                "opaque_candidate_id": opaque_candidate_id,
                "task_token": task_token,
                "task_rubric": {
                    "pressure": task["pressure"],
                    "protected_invariants": copy.deepcopy(task["protected_invariants"]),
                    "incumbent_primitives": copy.deepcopy(task["incumbent_primitives"]),
                    "physical_carrier": task["physical_carrier"],
                    "formal_pressure": task["formal_pressure"],
                    "falsifier": task["falsifier"],
                },
                "reflection": {
                    "rounds": copy.deepcopy(reflection["rounds"]),
                    "synthesis": reflection["synthesis"],
                    "unification_edges": copy.deepcopy(reflection["unification_edges"]),
                    "correction_conditions": copy.deepcopy(reflection["correction_conditions"]),
                    "convergence_status": reflection["convergence_status"],
                    "conceptual_content": copy.deepcopy(reflection["conceptual_content"]),
                },
                "formal": {
                    "content_projection": copy.deepcopy(formal["content_projection"]),
                },
            }
        )
    blinding = {
        "status": "internal_process_blind_only",
        "condition_labels_withheld": True,
        "strategy_labels_withheld": True,
        "arm_labels_withheld": True,
        "mapping_digest": canonical_digest(mapping_rows),
        "authority_distinct_status": "unavailable",
        "cognitive_independence_authorized": False,
    }
    return packets, blinding, token_to_task


def _score_projection(judgments: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "task_token": row["task_token"],
            **{dimension: row["dimension_scores"][dimension] for dimension in DIMENSIONS},
            "hard_gate": row["hard_gate"],
            "semantic_diagnostics": copy.deepcopy(row["semantic_diagnostics"]),
        }
        for row in judgments
    ]


def scientific_cell_projection(
    cell: Mapping[str, Any], receipts: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Return scientific content with operational identity and telemetry removed."""

    stages: list[dict[str, Any]] = []
    for receipt in receipts:
        stage_id = STAGE_BY_ROLE_OPERATION[(receipt["role"], receipt["operation"])]
        response = receipt.get("response_payload")
        failure = receipt.get("failure")
        stages.append(
            {
                "stage_id": stage_id,
                "role": receipt["role"],
                "operation": receipt["operation"],
                "request_payload": copy.deepcopy(receipt["request_payload"]["payload"]),
                "outcome_status": receipt["outcome_status"],
                "output": (
                    copy.deepcopy(response["output"])
                    if isinstance(response, Mapping)
                    else None
                ),
                "failure": (
                    {"stage": failure["stage"], "error_type": failure["error_type"]}
                    if isinstance(failure, Mapping)
                    else None
                ),
            }
        )
    return {
        "family_id": cell["family_id"],
        "condition_id": cell["condition_id"],
        "repetition": cell["repetition"],
        "task_ids": list(cell["task_ids"]),
        "task_cluster_ids": list(cell["task_cluster_ids"]),
        "frozen_ancestor_digest": cell["frozen_ancestor_digest"],
        "literature_descriptor_digest": cell["literature_descriptor_digest"],
        "strategy_descriptor_digest": cell["strategy_descriptor_digest"],
        "arm": cell["arm"],
        "stage_schedule_digest": cell["stage_schedule_digest"],
        "budget_profile_digest": cell["budget_profile_digest"],
        "stages": stages,
    }


def _output(receipt: Mapping[str, Any]) -> dict[str, Any]:
    response = receipt.get("response_payload")
    if receipt.get("outcome_status") != "accepted" or not isinstance(response, Mapping):
        raise MatchedStudyIntegrityError("dependent stage lacks an accepted worker output")
    output = response.get("output")
    if not isinstance(output, Mapping):
        raise MatchedStudyIntegrityError("accepted worker output is not an object")
    return dict(output)


def _finalize_cell(
    *, cell: Mapping[str, Any], receipts: Sequence[Mapping[str, Any]], blinding: Mapping[str, Any] | None, scores: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    stage_ids = [STAGE_BY_ROLE_OPERATION[(row["role"], row["operation"])] for row in receipts]
    failures = [
        stage_id
        for stage_id, receipt in zip(stage_ids, receipts)
        if receipt["outcome_status"] != "accepted"
    ]
    maturity_rows = [
        receipt
        for stage_id, receipt in zip(stage_ids, receipts)
        if stage_id in {"candidate_maturation", "high_risk_maturation"}
    ]
    maturity_completed = sum(row["outcome_status"] == "accepted" for row in maturity_rows)
    barrier_status = (
        "not_reached"
        if len(maturity_rows) != 2
        else ("complete" if maturity_completed == 2 else "partial")
    )
    complete = len(receipts) == len(STAGE_SCHEDULE) and not failures
    projection = scientific_cell_projection(cell, receipts)
    return {
        **copy.deepcopy(dict(cell)),
        "attempted_stage_count": len(receipts),
        "completed_stage_count": sum(row["outcome_status"] == "accepted" for row in receipts),
        "complete": complete,
        "partial_failure": not complete,
        "failure_stages": failures,
        "receipts": [receipt_summary(row) for row in receipts],
        "parallel_maturation": {
            "scheduled_branch_count": 2,
            "completed_branch_count": maturity_completed,
            "barrier_status": barrier_status,
        },
        "blinding": copy.deepcopy(dict(blinding)) if blinding is not None else None,
        "internal_judge_scores": copy.deepcopy([dict(row) for row in scores]),
        "scientific_projection_digest": canonical_digest(projection),
        "publication_authorized": False,
    }


def _run_cell(
    *, adapter: ResearchWorkerAdapter, fixture: Mapping[str, Any], family: Mapping[str, Any], condition: Mapping[str, Any], repetition: int, fault_plan: Mapping[str, str], formal_catalog: Mapping[tuple[str, str], Mapping[str, Any]]
) -> dict[str, Any]:
    cell = _cell_base(fixture, family, condition, repetition)
    world = _by_id(fixture["literature_worlds"], "world_id", condition["literature_world_id"])
    strategy = _by_id(fixture["strategies"], "strategy_id", condition["strategy_id"])
    budget = fixture["budget_profile"]
    receipts: list[dict[str, Any]] = []
    blinding: dict[str, Any] | None = None
    scores: list[dict[str, Any]] = []

    def invoke(stage_id: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        stage = [row for row in STAGE_SCHEDULE if row[0] == stage_id][0]
        fault_mode = fault_plan.get(study_fault_key(cell, stage_id))
        receipt = adapter.invoke(
            role=stage[1],
            operation=stage[2],
            invocation_context=_invocation_context(
                fixture=fixture, cell=cell, stage_id=stage_id
            ),
            payload=payload,
            budget=budget,
            fault_mode=fault_mode,
        )
        return receipt

    candidate = invoke(
        "candidate_generation",
        {
            "tasks": fixture["tasks"],
            "arm": _candidate_generation_arm(family, condition),
            "strategy": strategy,
            "literature_world": world,
        },
    )
    receipts.append(candidate)
    if candidate["outcome_status"] != "accepted":
        return _finalize_cell(cell=cell, receipts=receipts, blinding=None, scores=[])

    high_risk = invoke(
        "high_risk_generation",
        {
            "tasks": fixture["tasks"],
            "candidates": _output(candidate)["records"],
            "strategy": strategy,
            "corner_descriptors": _corner_descriptor_catalog(),
        },
    )
    receipts.append(high_risk)
    if high_risk["outcome_status"] != "accepted":
        return _finalize_cell(cell=cell, receipts=receipts, blinding=None, scores=[])

    maturation_payloads = {
        "candidate_maturation": {
            "branch_kind": "candidate",
            "proposals": _output(candidate)["records"],
        },
        "high_risk_maturation": {
            "branch_kind": "high_risk",
            "proposals": _output(high_risk)["records"],
        },
    }
    with ThreadPoolExecutor(max_workers=2) as branch_pool:
        futures = {
            stage_id: branch_pool.submit(invoke, stage_id, payload)
            for stage_id, payload in maturation_payloads.items()
        }
        matured = {stage_id: future.result() for stage_id, future in futures.items()}
    candidate_maturation = matured["candidate_maturation"]
    high_risk_maturation = matured["high_risk_maturation"]
    receipts.extend([candidate_maturation, high_risk_maturation])
    if any(
        row["outcome_status"] != "accepted"
        for row in (candidate_maturation, high_risk_maturation)
    ):
        return _finalize_cell(cell=cell, receipts=receipts, blinding=None, scores=[])

    formal = invoke(
        "formal_lens",
        {
            "tasks": fixture["tasks"],
            "lens": condition["arm"],
            "typed_artifacts": _formal_artifacts_for_arm(
                fixture, str(condition["arm"]), formal_catalog
            ),
        },
    )
    receipts.append(formal)
    if formal["outcome_status"] != "accepted":
        return _finalize_cell(cell=cell, receipts=receipts, blinding=None, scores=[])

    reflection = invoke(
        "reflection",
        {
            "candidate_maturation": _output(candidate_maturation)["records"],
            "high_risk_maturation": _output(high_risk_maturation)["records"],
            "formal_rows": _output(formal)["records"],
            "route_status": world["route_status"],
        },
    )
    receipts.append(reflection)
    if reflection["outcome_status"] != "accepted":
        return _finalize_cell(cell=cell, receipts=receipts, blinding=None, scores=[])

    packets, blinding, _token_to_task = _sanitized_blind_packets(
        fixture=fixture,
        cell=cell,
        reflections=_output(reflection)["records"],
        formal_rows=_output(formal)["records"],
    )
    judgment = invoke("blind_judgment", {"blinded_packets": packets})
    receipts.append(judgment)
    if judgment["outcome_status"] != "accepted":
        return _finalize_cell(cell=cell, receipts=receipts, blinding=blinding, scores=[])
    scores = _score_projection(_output(judgment)["records"])

    convergence = invoke(
        "convergence", {"judgments": _output(judgment)["records"]}
    )
    receipts.append(convergence)
    return _finalize_cell(
        cell=cell, receipts=receipts, blinding=blinding, scores=scores
    )


def _mean_scores(rows: Sequence[Mapping[str, Any]]) -> dict[str, float | None]:
    if not rows:
        return {dimension: None for dimension in DIMENSIONS}
    return {
        dimension: round(
            sum(float(row[dimension]) for row in rows) / len(rows), 6
        )
        for dimension in DIMENSIONS
    }


def _descriptive_results(
    *, fixture: Mapping[str, Any], conditions: Sequence[Mapping[str, Any]], cells: Sequence[Mapping[str, Any]], matched_repetitions: Sequence[int]
) -> list[dict[str, Any]]:
    task_to_cluster = {row["task_id"]: row["cluster_id"] for row in fixture["tasks"]}
    token_to_task = {
        stable_identifier("matched-task-token", fixture["blinding_salt_id"], task_id): task_id
        for task_id in task_to_cluster
    }
    clusters = [row["cluster_id"] for row in fixture["tasks"]]
    results: list[dict[str, Any]] = []
    for condition in conditions:
        selected_cells = [
            cell
            for cell in cells
            if cell["condition_id"] == condition["condition_id"]
            and cell["repetition"] in matched_repetitions
        ]
        scores = [score for cell in selected_cells for score in cell["internal_judge_scores"]]
        cluster_results = []
        for cluster_id in clusters:
            cluster_scores = [
                score
                for score in scores
                if task_to_cluster.get(token_to_task.get(score["task_token"], "")) == cluster_id
            ]
            cluster_results.append(
                {
                    "cluster_id": cluster_id,
                    "task_count": sum(value == cluster_id for value in task_to_cluster.values()),
                    "observation_count": len(cluster_scores),
                    "mean_scores": _mean_scores(cluster_scores),
                }
            )
        results.append(
            {
                "condition_id": condition["condition_id"],
                "matched_repetitions": list(matched_repetitions),
                "complete_cells": len(selected_cells),
                "score_observations": len(scores),
                "mean_scores": _mean_scores(scores),
                "task_cluster_results": cluster_results,
                "interpretation": "internal_descriptive_structure_only_no_advantage_inference",
            }
        )
    return results


def _family_report(
    *, fixture: Mapping[str, Any], family: Mapping[str, Any], cells: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    conditions = family["conditions"]
    repetitions = family["repetitions"]
    matched_repetitions = [
        repetition
        for repetition in range(1, repetitions + 1)
        if all(
            any(
                cell["condition_id"] == condition["condition_id"]
                and cell["repetition"] == repetition
                and cell["complete"]
                for cell in cells
            )
            for condition in conditions
        )
    ]
    matched_keys = [
        cell["cell_key"]
        for cell in cells
        if cell["repetition"] in matched_repetitions
    ]
    return {
        "family_id": family["family_id"],
        "intervention_axis": family["intervention_axis"],
        "conditions": copy.deepcopy(conditions),
        "repetitions": repetitions,
        "task_ids": [row["task_id"] for row in fixture["tasks"]],
        "task_cluster_ids": [row["cluster_id"] for row in fixture["tasks"]],
        "cells": copy.deepcopy([dict(row) for row in cells]),
        "equal_opportunity_certificate": {
            "status": "passed_schedule_level",
            "scheduled_tasks_matched": True,
            "scheduled_stages_matched": True,
            "generation_opportunities_matched": True,
            "literature_slots_matched": True,
            "scheduled_resource_profile_matched": True,
            "realized_resource_equivalence_status": (
                "unavailable_operational_telemetry_excluded"
            ),
            "frozen_ancestor_matched": True,
            "frozen_ancestor_digest": conditions[0]["frozen_ancestor_digest"],
            "complete_cell_count": sum(cell["complete"] for cell in cells),
            "scheduled_cell_count": len(cells),
            "authority_distinct_evaluation_status": "unavailable",
            "advantage_inference_authorized": False,
        },
        "matched_complete_repetitions": matched_repetitions,
        "matched_complete_cell_keys": matched_keys,
        "partial_failure": any(not cell["complete"] for cell in cells),
        "descriptive_results": _descriptive_results(
            fixture=fixture,
            conditions=conditions,
            cells=cells,
            matched_repetitions=matched_repetitions,
        ),
        "advantage_inference_authorized": False,
        "publication_authorized": False,
    }


def _authority_outcomes() -> dict[str, Any]:
    return {
        "external_human_evidence_status": "unavailable",
        "authority_distinct_evaluation_status": "unavailable",
        "external_provider_status": "unavailable",
        "strategy_execution_status": "synthetic_internal_descriptors_only",
        "provider_plurality_authorized": False,
        "production_chain_executed": False,
        "population_generalization_authorized": False,
        "literature_benefit_authorized": False,
        "high_risk_advantage_authorized": False,
        "abstraction_value_authorized": False,
        "creativity_authorized": False,
        "relevance_authorized": False,
        "conceptual_depth_authorized": False,
        "unification_power_authorized": False,
        "physics_value_authorized": False,
        "truth_authorized": False,
        "theorem_authorized": False,
        "continuum_authorized": False,
        "efficacy_authorized": False,
        "publication_authorized": False,
    }


def _deterministic_projection(families: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rows = [
        {"cell_key": cell["cell_key"], "digest": cell["scientific_projection_digest"]}
        for family in families
        for cell in family["cells"]
    ]
    return {
        "status": "deterministic_replayable_internal_projection",
        "cell_projection_digests": rows,
        "projection_digest": canonical_digest(rows),
        "operational_metadata_excluded": True,
        "excluded_operational_fields": list(OPERATIONAL_PROJECTION_FIELDS),
        "projection_basis": "worker_request_scientific_payload_output_and_typed_failure_class_only",
    }


def _study_isolation_requirement(require_kernel_isolation: bool) -> dict[str, Any]:
    core = {
        "schema_version": 1,
        "kernel_isolation_required": bool(require_kernel_isolation),
        "minimum_accepted_status": (
            "kernel_policy_enforced"
            if require_kernel_isolation
            else "strongest_available"
        ),
    }
    return {**core, "content_digest": canonical_digest(core)}


def _validate_study_isolation_requirement(raw: Mapping[str, Any]) -> dict[str, Any]:
    requirement = copy.deepcopy(dict(raw))
    required = {
        "schema_version",
        "kernel_isolation_required",
        "minimum_accepted_status",
        "content_digest",
    }
    if set(requirement) != required:
        raise MatchedStudyIntegrityError("matched-study isolation requirement is not closed")
    if (
        requirement["schema_version"] != 1
        or not isinstance(requirement["kernel_isolation_required"], bool)
        or requirement["minimum_accepted_status"]
        != (
            "kernel_policy_enforced"
            if requirement["kernel_isolation_required"]
            else "strongest_available"
        )
        or requirement["content_digest"]
        != canonical_digest(
            {
                key: value
                for key, value in requirement.items()
                if key != "content_digest"
            }
        )
    ):
        raise MatchedStudyIntegrityError("matched-study isolation requirement is invalid")
    return requirement


def run_matched_discovery_study(
    *, fixture_path: Path | str, run_root: Path | str, run_id: str, repetitions: int | None = None, study_id: str | None = None, max_workers: int = 4, require_kernel_isolation: bool = False, fault_plan: Mapping[str, str] | None = None
) -> dict[str, Any]:
    """Execute every planned cell and return one validated internal report.

    Reusing the same ``run_id``, fixture semantics, and repetition count is an
    exact resume operation.  Successful request receipts reopen byte-for-byte;
    a changed fault mode creates a distinct request receipt; and downstream
    stages missing from a partial prefix execute only after their dependencies
    are repaired.  Callers should persist each returned content-addressed
    report if both the failed attempt and the repaired chain must remain
    independently reopenable.
    """

    validate_identifier(run_id, "run_id")
    if not isinstance(max_workers, int) or max_workers < 1:
        raise MatchedStudyIntegrityError("cell max_workers must be positive")
    fixture_file = Path(fixture_path).resolve(strict=True)
    fixture = load_matched_study_fixture(fixture_file)
    effective_repetitions = (
        fixture["default_repetitions"] if repetitions is None else repetitions
    )
    plan = build_matched_study_plan(fixture, repetitions=effective_repetitions)
    formal_catalog = _build_typed_formal_catalog(fixture)
    isolation_requirement = _study_isolation_requirement(require_kernel_isolation)
    expected_study_id = stable_identifier(
        "matched-study",
        run_id,
        canonical_digest(fixture),
        effective_repetitions,
        isolation_requirement,
    )
    if study_id is not None and study_id != expected_study_id:
        raise MatchedStudyIntegrityError("caller-supplied study_id is not content-derived")
    faults = dict(fault_plan or {})
    valid_fault_modes = {"exit_nonzero", "invalid_json", "hang"}
    if any(value not in valid_fault_modes for value in faults.values()):
        raise MatchedStudyIntegrityError("fault plan contains an unsupported mode")

    scheduled: list[tuple[dict[str, Any], dict[str, Any], int]] = []
    for family in plan:
        for condition in family["conditions"]:
            for repetition in range(1, effective_repetitions + 1):
                scheduled.append((family, condition, repetition))
    allowed_fault_keys = {
        study_fault_key(_cell_base(fixture, family, condition, repetition), stage_id)
        for family, condition, repetition in scheduled
        for stage_id, _role, _operation in STAGE_SCHEDULE
    }
    unknown_fault_keys = sorted(set(faults) - allowed_fault_keys)
    if unknown_fault_keys:
        raise MatchedStudyIntegrityError(
            f"fault plan names an unscheduled cell or stage: {unknown_fault_keys[0]}"
        )

    # Constructing the adapter creates the study directory, so all caller-only
    # plan validation happens first and malformed fault plans have no runtime
    # side effects.
    adapter = ResearchWorkerAdapter(
        study_id=expected_study_id,
        run_root=run_root,
        require_kernel_isolation=require_kernel_isolation,
    )
    completed: dict[str, dict[str, Any]] = {}
    worker_count = min(max_workers, len(scheduled))
    with ThreadPoolExecutor(max_workers=worker_count) as cell_pool:
        futures = {}
        for family, condition, repetition in scheduled:
            base = _cell_base(fixture, family, condition, repetition)
            futures[
                cell_pool.submit(
                    _run_cell,
                    adapter=adapter,
                    fixture=fixture,
                    family=family,
                    condition=condition,
                    repetition=repetition,
                    fault_plan=faults,
                    formal_catalog=formal_catalog,
                )
            ] = base["cell_key"]
        for future in as_completed(futures):
            result = future.result()
            completed[result["cell_key"]] = result

    family_reports = []
    for family in plan:
        ordered_cells = [
            completed[_cell_base(fixture, family, condition, repetition)["cell_key"]]
            for condition in family["conditions"]
            for repetition in range(1, effective_repetitions + 1)
        ]
        family_reports.append(
            _family_report(fixture=fixture, family=family, cells=ordered_cells)
        )
    partial = any(family["partial_failure"] for family in family_reports)
    core = {
        "schema_version": 3,
        "study_id": expected_study_id,
        "run_id": run_id,
        "run_directory": str(adapter.run_directory),
        "fixture": _fixture_record(fixture_file, fixture),
        "isolation_requirement": isolation_requirement,
        "status": (
            "partial_failure_internal_calibration_only"
            if partial
            else "protocol_complete_internal_calibration_only"
        ),
        "publication_control": {
            "mode": "publication_disabled_study",
            "canonical_publication_authorized": False,
            "binding_update_authorized": False,
            "reason": "Matched studies are internal protocol calibration and cannot update canonical discovery authority.",
        },
        "parallel_execution": {
            "cell_max_workers": worker_count,
            "cell_parallelism": "thread_orchestrated_isolated_subprocess_cells",
            "within_cell_parallel_maturation": True,
            "shared_mutable_worker_state": False,
            "partial_failure_preserved": True,
            "high_risk_corner_catalog_digest": canonical_digest(
                _corner_descriptor_catalog()
            ),
            "high_risk_variants_per_task": len(_corner_descriptor_catalog()),
            "high_risk_variant_parallelism": (
                "thread_orchestrated_inside_isolated_worker"
            ),
            "high_risk_variant_barrier": True,
            "high_risk_variant_shared_mutable_state": False,
        },
        "families": family_reports,
        "deterministic_projection": _deterministic_projection(family_reports),
        "authority_outcomes": _authority_outcomes(),
    }
    report = {**core, "content_digest": canonical_digest(core)}
    return validate_matched_discovery_study(report)


def _validate_cell_chain(
    *, fixture: Mapping[str, Any], family: Mapping[str, Any], condition: Mapping[str, Any], cell: Mapping[str, Any], run_directory: Path, study_id: str, required_kernel_isolation: bool | None, formal_catalog: Mapping[tuple[str, str], Mapping[str, Any]]
) -> dict[str, Any]:
    expected_base = _cell_base(fixture, family, condition, int(cell["repetition"]))
    for key, value in expected_base.items():
        if cell.get(key) != value:
            raise MatchedStudyIntegrityError(f"cell {key} differs from its matched plan")
    summaries = cell["receipts"]
    receipts: list[dict[str, Any]] = []
    for summary in summaries:
        receipt_path = contained_path(run_directory, *Path(summary["receipt_ref"]).parts)
        receipt_bytes = receipt_path.read_bytes()
        if (
            len(receipt_bytes) != summary["receipt_byte_length"]
            or bytes_digest(receipt_bytes) != summary["receipt_file_sha256"]
        ):
            raise MatchedStudyIntegrityError("receipt summary file bytes changed")
        receipt = validate_research_worker_receipt(
            _load_json_object(receipt_path),
            receipt_path=receipt_path,
            require_live_authority=summary["outcome_status"] == "accepted",
            required_kernel_isolation=required_kernel_isolation,
        )
        if receipt["study_id"] != study_id or receipt_summary(
            receipt, receipt_path=receipt_path
        ) != summary:
            raise MatchedStudyIntegrityError("receipt summary lacks exact transitive membership")
        receipts.append(receipt)

    stage_ids = [STAGE_BY_ROLE_OPERATION.get((row["role"], row["operation"])) for row in receipts]
    expected_stage_ids = [row[0] for row in STAGE_SCHEDULE]
    if stage_ids != expected_stage_ids[: len(stage_ids)]:
        raise MatchedStudyIntegrityError("cell receipts are not an exact stage prefix")
    failures = [index for index, row in enumerate(receipts) if row["outcome_status"] != "accepted"]
    if failures:
        first = failures[0]
        permitted_length = 4 if first == 2 else first + 1
        if len(receipts) != permitted_length:
            raise MatchedStudyIntegrityError("cell executed a dependent stage after failure")

    world = _by_id(fixture["literature_worlds"], "world_id", condition["literature_world_id"])
    strategy = _by_id(fixture["strategies"], "strategy_id", condition["strategy_id"])
    outputs: dict[str, dict[str, Any]] = {}
    computed_blinding: dict[str, Any] | None = None
    token_to_task: dict[str, str] = {}
    for stage_id, receipt in zip(stage_ids, receipts):
        if receipt["request_payload"]["invocation_context"] != _invocation_context(
            fixture=fixture, cell=expected_base, stage_id=str(stage_id)
        ):
            raise MatchedStudyIntegrityError("worker invocation context differs from its stage")
        if stage_id == "candidate_generation":
            expected_payload = {
                "tasks": fixture["tasks"],
                "arm": _candidate_generation_arm(family, condition),
                "strategy": strategy,
                "literature_world": world,
            }
        elif stage_id == "high_risk_generation":
            expected_payload = {
                "tasks": fixture["tasks"],
                "candidates": outputs["candidate_generation"]["records"],
                "strategy": strategy,
                "corner_descriptors": _corner_descriptor_catalog(),
            }
        elif stage_id == "candidate_maturation":
            expected_payload = {
                "branch_kind": "candidate",
                "proposals": outputs["candidate_generation"]["records"],
            }
        elif stage_id == "high_risk_maturation":
            expected_payload = {
                "branch_kind": "high_risk",
                "proposals": outputs["high_risk_generation"]["records"],
            }
        elif stage_id == "formal_lens":
            expected_payload = {
                "tasks": fixture["tasks"],
                "lens": condition["arm"],
                "typed_artifacts": _formal_artifacts_for_arm(
                    fixture, str(condition["arm"]), formal_catalog
                ),
            }
        elif stage_id == "reflection":
            expected_payload = {
                "candidate_maturation": outputs["candidate_maturation"]["records"],
                "high_risk_maturation": outputs["high_risk_maturation"]["records"],
                "formal_rows": outputs["formal_lens"]["records"],
                "route_status": world["route_status"],
            }
        elif stage_id == "blind_judgment":
            packets, computed_blinding, token_to_task = _sanitized_blind_packets(
                fixture=fixture,
                cell=expected_base,
                reflections=outputs["reflection"]["records"],
                formal_rows=outputs["formal_lens"]["records"],
            )
            expected_payload = {"blinded_packets": packets}
        elif stage_id == "convergence":
            expected_payload = {"judgments": outputs["blind_judgment"]["records"]}
        else:  # pragma: no cover - exact prefix check makes this unreachable
            raise MatchedStudyIntegrityError("unknown study stage")
        if receipt["request_payload"]["payload"] != expected_payload:
            raise MatchedStudyIntegrityError(f"{stage_id} did not consume exact prior outputs")
        if receipt["outcome_status"] == "accepted":
            outputs[str(stage_id)] = _output(receipt)

    expected_scores = (
        _score_projection(outputs["blind_judgment"]["records"])
        if "blind_judgment" in outputs
        else []
    )
    if cell["blinding"] != computed_blinding or cell["internal_judge_scores"] != expected_scores:
        raise MatchedStudyIntegrityError("cell blind mapping or scores are not exact")
    # A failed blind-judgment attempt still has an authoritative, replayable
    # request-side blinding map.  It has no accepted score rows, however, so
    # task-total score coverage is meaningful only after the stage produced an
    # accepted output.  Keeping these predicates separate preserves failed-
    # stage blinding validation without inventing judgments from a failure.
    if "blind_judgment" in outputs:
        if set(token_to_task) != {row["task_token"] for row in expected_scores}:
            raise MatchedStudyIntegrityError("blind scores are not task-total")

    recomputed = _finalize_cell(
        cell=expected_base,
        receipts=receipts,
        blinding=computed_blinding,
        scores=expected_scores,
    )
    if recomputed != dict(cell):
        raise MatchedStudyIntegrityError("cell summary differs from exact receipt replay")
    return recomputed


def validate_matched_discovery_study(
    raw: Mapping[str, Any], *, report_path: Path | str | None = None
) -> dict[str, Any]:
    """Replay a study from its fixture and every immutable worker receipt."""

    validate_payload(raw, STUDY_SCHEMA)
    report = copy.deepcopy(dict(raw))
    if report["content_digest"] != _top_level_content_digest(report):
        raise MatchedStudyIntegrityError("matched-study content digest mismatch")
    run_directory = Path(report["run_directory"])
    if (
        not run_directory.is_absolute()
        or run_directory.resolve() != run_directory
        or run_directory.name != report["study_id"]
        or run_directory.is_symlink()
        or not run_directory.is_dir()
    ):
        raise MatchedStudyIntegrityError("matched-study run directory is not canonical")
    fixture_path = Path(report["fixture"]["fixture_path"])
    fixture = load_matched_study_fixture(fixture_path)
    if report["fixture"] != _fixture_record(fixture_path, fixture):
        raise MatchedStudyIntegrityError("matched-study fixture bytes or semantics changed")
    repetitions = report["families"][0]["repetitions"]
    if report["schema_version"] == 3:
        isolation_requirement = _validate_study_isolation_requirement(
            report["isolation_requirement"]
        )
        required_kernel_isolation: bool | None = isolation_requirement[
            "kernel_isolation_required"
        ]
        expected_study_id = stable_identifier(
            "matched-study",
            report["run_id"],
            canonical_digest(fixture),
            repetitions,
            isolation_requirement,
        )
    else:
        isolation_requirement = None
        required_kernel_isolation = None
        expected_study_id = stable_identifier(
            "matched-study", report["run_id"], canonical_digest(fixture), repetitions
        )
    if report["study_id"] != expected_study_id:
        raise MatchedStudyIntegrityError("matched-study identity is not content-derived")
    if any(family["repetitions"] != repetitions for family in report["families"]):
        raise MatchedStudyIntegrityError("matched-study families use different repetitions")
    plan = build_matched_study_plan(fixture, repetitions=repetitions)
    formal_catalog = _build_typed_formal_catalog(fixture)
    if len(report["families"]) != len(plan):
        raise MatchedStudyIntegrityError("matched-study family cardinality changed")

    validated_families = []
    for planned, family in zip(plan, report["families"]):
        if (
            family["family_id"] != planned["family_id"]
            or family["intervention_axis"] != planned["intervention_axis"]
            or family["conditions"] != planned["conditions"]
        ):
            raise MatchedStudyIntegrityError("matched-study family plan changed")
        expected_cell_keys = [
            _cell_base(fixture, planned, condition, repetition)["cell_key"]
            for condition in planned["conditions"]
            for repetition in range(1, repetitions + 1)
        ]
        if [cell["cell_key"] for cell in family["cells"]] != expected_cell_keys:
            raise MatchedStudyIntegrityError("matched-study cell grid is incomplete or reordered")
        validated_cells = []
        for cell in family["cells"]:
            condition = _by_id(
                planned["conditions"], "condition_id", cell["condition_id"]
            )
            validated_cells.append(
                _validate_cell_chain(
                    fixture=fixture,
                    family=planned,
                    condition=condition,
                    cell=cell,
                    run_directory=run_directory,
                    study_id=report["study_id"],
                    required_kernel_isolation=required_kernel_isolation,
                    formal_catalog=formal_catalog,
                )
            )
        expected_family = _family_report(
            fixture=fixture, family=planned, cells=validated_cells
        )
        if expected_family != family:
            raise MatchedStudyIntegrityError("matched-study family summary is not replay-derived")
        validated_families.append(expected_family)

    expected_partial = any(family["partial_failure"] for family in validated_families)
    expected_status = (
        "partial_failure_internal_calibration_only"
        if expected_partial
        else "protocol_complete_internal_calibration_only"
    )
    if report["status"] != expected_status:
        raise MatchedStudyIntegrityError("matched-study status differs from cell outcomes")
    if report["deterministic_projection"] != _deterministic_projection(validated_families):
        raise MatchedStudyIntegrityError("matched-study scientific projection mismatch")
    if report["authority_outcomes"] != _authority_outcomes():
        raise MatchedStudyIntegrityError("matched-study report invented epistemic authority")
    if report_path is not None:
        path = Path(report_path)
        expected_report_id = stable_identifier(
            "matched-study-report", report["content_digest"]
        )
        expected_path = contained_path(
            run_directory, "reports", f"{expected_report_id}.json"
        )
        if path.resolve() != expected_path or path.is_symlink():
            raise MatchedStudyIntegrityError("matched-study report path is not content-addressed")
        if path.read_bytes() != canonical_json(report) + b"\n":
            raise MatchedStudyIntegrityError("matched-study report file bytes changed")
    return report


def write_matched_discovery_study_report(report: Mapping[str, Any]) -> Path:
    """Write one immutable, content-addressed internal study report."""

    validated = validate_matched_discovery_study(report)
    report_id = stable_identifier("matched-study-report", validated["content_digest"])
    path = contained_path(
        Path(validated["run_directory"]), "reports", f"{report_id}.json"
    )
    _write_immutable_json(path, validated)
    validate_matched_discovery_study(
        _load_json_object(path), report_path=path
    )
    return path


def load_matched_discovery_study_report(path: Path | str) -> dict[str, Any]:
    """Reopen one immutable report against its receipts and live checkout.

    A report is portable only as an identity record: accepted worker receipts
    deliberately re-check the currently installed executable and dependency
    bytes.  Reopening therefore proves that the content-addressed report and
    receipt chain are unchanged *and* that the current checkout still matches
    the authority under which accepted stages ran.  It is not a claim of
    checkout-independent archival replay.
    """

    report_path = Path(path).resolve(strict=True)
    if report_path.is_symlink() or not report_path.is_file():
        raise MatchedStudyIntegrityError("matched-study report is not a regular file")
    return validate_matched_discovery_study(
        _load_json_object(report_path), report_path=report_path
    )


__all__ = [
    "MatchedStudyIntegrityError",
    "build_matched_study_plan",
    "load_matched_discovery_study_report",
    "load_matched_study_fixture",
    "run_matched_discovery_study",
    "scientific_cell_projection",
    "study_fault_key",
    "validate_matched_discovery_study",
    "write_matched_discovery_study_report",
]
