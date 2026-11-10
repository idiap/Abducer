# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Parallel, provider-backed search for genuinely open conceptual families.

This module is a narrow production seam between the current-literature
projection and the existing open-world creativity machinery.  It deliberately
does not contain an authored programme atlas.  Instead it:

* transitively reopens the bounded literature bundle at governed use time;
* precommits eight to twelve provider slots, including two protected wildcard
  opportunities and one equal-budget capable conservative control;
* authors and then matures candidates in two killable process waves;
* freezes inventions before maturation or family reconstruction;
* reconstructs typed family cells from complete, label-blind content;
* quarantines exact or high-similarity copies of a caller-precommitted template
  corpus; and
* admits fewer than six families only when a target-predeclared finite coverage
  problem has a replayable minimal UNSAT core and countermodel.

The process and receipt boundaries establish local chronology, terminal
partial-failure accounting, and exact replay only.  Provider/model/human,
cognitive, semantic, evaluator, creativity, merit, truth, literature-benefit,
and physics-value independence or authority remain explicitly unavailable.
"""

from __future__ import annotations

import copy
import itertools
import re
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from .conceptual_ancestry_v3 import (
    build_conceptual_ancestry_literature_projection,
)
from .contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    utc_now,
    validate_identifier,
    validate_payload,
)
from .open_world_creativity import (
    _validate_matured as _validate_open_world_matured,
    _validate_raw_invention as _validate_open_world_raw_invention,
    build_pre_taxonomy_invention_freeze,
    known_taxonomy_commitment,
    validate_pre_taxonomy_invention_freeze,
)
from .parallel import run_bounded_killable_request_wave


SCHEMA_VERSION = "1.0.0"
SCHEMA_NAME = "aggressive_provider_search_execution_v1.schema.json"
MIN_DISTINCT_FAMILIES = 6
MIN_AUTHOR_SLOTS = 8
MAX_AUTHOR_SLOTS = 12
COPY_SIMILARITY_THRESHOLD = 0.95
ProviderWorker = Callable[[Mapping[str, Any]], Mapping[str, Any]]

AUTHORITY_NULLS = {
    "source_truth_authority": None,
    "global_latestness_authority": None,
    "semantic_entailment_authority": None,
    "novelty_authority": None,
    "creativity_authority": None,
    "conceptual_merit_authority": None,
    "relevance_authority": None,
    "conceptual_depth_authority": None,
    "philosophical_understanding_authority": None,
    "unification_power_authority": None,
    "literature_benefit_authority": None,
    "physics_value_authority": None,
    "truth_authority": None,
    "proof_or_theorem_authority": None,
    "provider_independence_authority": None,
    "model_independence_authority": None,
    "human_independence_authority": None,
    "cognitive_independence_authority": None,
    "semantic_independence_authority": None,
    "evaluator_independence_authority": None,
}
AUTHORITY_BOUNDARY = (
    "The execution proves exact bounded-literature reopening, a precommitted "
    "provider-plural schedule, two killable process waves, terminal partial-"
    "failure receipts, pre-taxonomy freezing, label-blind typed family "
    "reconstruction, copy controls, and finite coverage replay. It grants no "
    "source-truth, global-latestness, novelty, creativity, conceptual merit, "
    "relevance, depth, philosophical understanding, unification, literature "
    "benefit, physics value, provider/model/human/cognitive/semantic/evaluator "
    "independence, proof, theorem, or truth authority."
)

_SIGNATURE_FIELDS = frozenset(
    {
        "intervention_kind",
        "prediction_direction",
        "correction_kind",
        "mechanism_topology",
        "relation_polarity",
        "physics_handback_status",
    }
)
_INTERVENTION_KINDS = frozenset(
    {
        "add",
        "remove",
        "reverse",
        "hold_fixed",
        "localize",
        "quotient",
        "couple",
        "decouple",
    }
)
_PREDICTION_DIRECTIONS = frozenset(
    {"increase", "decrease", "invariant", "bifurcate", "permit", "obstruct"}
)
_CORRECTION_KINDS = frozenset(
    {
        "abandon",
        "retype",
        "change_relation",
        "split_scope",
        "add_mediator",
        "retract",
    }
)
_MECHANISM_TOPOLOGIES = frozenset(
    {"chain", "branch", "merge", "feedback", "network"}
)
_RELATION_POLARITIES = frozenset(
    {"positive", "negative", "constraint", "dual", "constitutive", "emergent"}
)
_PHYSICS_STATUSES = frozenset(
    {"decision_changed", "quarantined_no_physics_delta"}
)
_SLOT_ROLES = frozenset(
    {"aggressive_candidate", "protected_wildcard", "capable_conservative_control"}
)
_GENERATION_OUTPUT_FIELDS = frozenset(
    {"output_kind", "request_digest", "raw_invention"}
)
_MATURATION_OUTPUT_FIELDS = frozenset(
    {
        "output_kind",
        "request_digest",
        "matured_invention",
        "typed_family_evidence",
    }
)
_FAMILY_EVIDENCE_FIELDS = frozenset(
    {
        "mechanism_graph",
        "relation_polarity",
        "intervention",
        "prediction",
        "correction",
        "falsifier",
        "physics_return",
    }
)
_TOKEN = re.compile(r"[A-Za-z0-9]+")


class AggressiveProviderSearchError(ContractError):
    """Stable fail-closed error for provider search production and replay."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"aggressive_provider_search[{reason_code}]: {message}")


def _fail(reason_code: str, message: str) -> None:
    raise AggressiveProviderSearchError(reason_code, message)


def _exact(value: Mapping[str, Any], fields: frozenset[str], label: str) -> None:
    if not isinstance(value, Mapping) or set(value) != fields:
        _fail("contract_shape_invalid", f"{label} has an open or incomplete shape")


def _text(value: Any, field: str) -> str:
    normalized = " ".join(str(value or "").split())
    if not normalized:
        _fail("request_invalid", f"{field} must be nonempty")
    return normalized


def _text_list(value: Any, field: str) -> list[str]:
    if (
        not isinstance(value, Sequence)
        or isinstance(value, (str, bytes, bytearray))
    ):
        _fail("request_invalid", f"{field} must be a sequence")
    rows = [_text(item, field) for item in value]
    if not rows or len(rows) != len(set(rows)):
        _fail("request_invalid", f"{field} must be nonempty and unique")
    return rows


def _seal(core: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(core))
    return {**value, "content_digest": canonical_digest(value)}


def _verify_seal(value: Mapping[str, Any], label: str) -> None:
    expected = canonical_digest(
        {key: child for key, child in value.items() if key != "content_digest"}
    )
    if value.get("content_digest") != expected:
        _fail("digest_mismatch", f"{label} digest changed")


def _without(value: Mapping[str, Any], *fields: str) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    for field in fields:
        result.pop(field, None)
    return result


def target_constraint_identifiers(
    root_contradictions: Sequence[str],
    protected_successes: Sequence[str],
) -> list[str]:
    """Return the finite target atoms that coverage must predeclare.

    Identifiers are structural positions, not semantic family labels.  The
    request separately binds the exact text at each position.
    """

    roots = _text_list(root_contradictions, "root_contradictions")
    protected = _text_list(protected_successes, "protected_successes")
    return [
        "target-pressure",
        *(f"root-contradiction-{index}" for index in range(len(roots))),
        *(f"protected-success-{index}" for index in range(len(protected))),
    ]


def _validate_signature(value: Mapping[str, Any]) -> dict[str, str]:
    _exact(value, _SIGNATURE_FIELDS, "semantic family signature")
    signature = {key: str(value[key]) for key in sorted(_SIGNATURE_FIELDS)}
    allowed = {
        "intervention_kind": _INTERVENTION_KINDS,
        "prediction_direction": _PREDICTION_DIRECTIONS,
        "correction_kind": _CORRECTION_KINDS,
        "mechanism_topology": _MECHANISM_TOPOLOGIES,
        "relation_polarity": _RELATION_POLARITIES,
        "physics_handback_status": _PHYSICS_STATUSES,
    }
    for field, values in allowed.items():
        if signature[field] not in values:
            _fail(
                "coverage_problem_invalid",
                f"semantic family signature has invalid {field}",
            )
    return signature


def _cell_id(
    signature: Mapping[str, Any], covers_constraint_ids: Sequence[str]
) -> str:
    return stable_identifier(
        "semantic-family-cell",
        dict(signature),
        sorted(str(item) for item in covers_constraint_ids),
    )


def build_target_predeclared_coverage_problem(
    *,
    target_id: str,
    required_constraint_ids: Sequence[str],
    admissible_cells: Sequence[Mapping[str, Any]],
    minimum_distinct_family_count: int = MIN_DISTINCT_FAMILIES,
) -> dict[str, Any]:
    """Seal a finite, output-independent family-coverage search space.

    Every cell is specified only by typed intervention/prediction/correction,
    mechanism topology, relation polarity, physics-return status, and target
    atoms.  No programme name or worker family label is accepted.
    """

    validate_identifier(target_id, "target_id")
    required = sorted(
        _text_list(required_constraint_ids, "required_constraint_ids")
    )
    if (
        isinstance(minimum_distinct_family_count, bool)
        or not isinstance(minimum_distinct_family_count, int)
        or not 1 <= minimum_distinct_family_count <= MIN_DISTINCT_FAMILIES
    ):
        _fail(
            "coverage_problem_invalid",
            "minimum distinct family count must be in [1, 6]",
        )
    if (
        not isinstance(admissible_cells, Sequence)
        or isinstance(admissible_cells, (str, bytes, bytearray))
        or not 1 <= len(admissible_cells) <= MAX_AUTHOR_SLOTS
    ):
        _fail(
            "coverage_problem_invalid",
            "finite coverage requires one through twelve admissible cells",
        )
    cells: list[dict[str, Any]] = []
    for raw in admissible_cells:
        _exact(
            raw,
            frozenset({"signature", "covers_constraint_ids"}),
            "admissible family cell",
        )
        signature = _validate_signature(raw["signature"])
        covers = _text_list(
            raw["covers_constraint_ids"], "cell covers_constraint_ids"
        )
        if not set(covers).issubset(required):
            _fail(
                "coverage_problem_invalid",
                "admissible cell covers an unknown target constraint",
            )
        cells.append(
            {
                "cell_id": _cell_id(signature, covers),
                "signature": signature,
                "covers_constraint_ids": sorted(covers),
            }
        )
    cells.sort(key=lambda row: row["cell_id"])
    if len({row["cell_id"] for row in cells}) != len(cells):
        _fail(
            "coverage_problem_invalid",
            "predeclared semantic family cells must be distinct",
        )
    return _seal(
        {
            "schema_version": SCHEMA_VERSION,
            "artifact_kind": "target_predeclared_family_coverage_problem",
            "problem_id": stable_identifier(
                "target-family-coverage-problem",
                target_id,
                required,
                cells,
                minimum_distinct_family_count,
            ),
            "target_id": target_id,
            "required_constraint_ids": sorted(required),
            "minimum_distinct_family_count": minimum_distinct_family_count,
            "admissible_cells": cells,
            "output_independent_precommitment": True,
            "caller_family_labels": False,
        }
    )


def _validate_coverage_problem(
    problem: Mapping[str, Any], *, expected_constraint_ids: Sequence[str]
) -> dict[str, Any]:
    value = copy.deepcopy(dict(problem))
    _verify_seal(value, "target coverage problem")
    expected = build_target_predeclared_coverage_problem(
        target_id=str(value["target_id"]),
        required_constraint_ids=value["required_constraint_ids"],
        admissible_cells=[
            {
                "signature": row["signature"],
                "covers_constraint_ids": row["covers_constraint_ids"],
            }
            for row in value["admissible_cells"]
        ],
        minimum_distinct_family_count=int(
            value["minimum_distinct_family_count"]
        ),
    )
    if value != expected:
        _fail(
            "coverage_problem_replay_mismatch",
            "target-predeclared finite coverage problem changed",
        )
    if set(value["required_constraint_ids"]) != set(expected_constraint_ids):
        _fail(
            "coverage_problem_target_mismatch",
            "coverage problem omits or adds target constraints",
        )
    return value


def _selection_covers(
    cells: Sequence[Mapping[str, Any]],
    *,
    required_constraint_ids: Sequence[str],
    minimum_count: int,
) -> bool:
    return len(cells) >= minimum_count and set(required_constraint_ids).issubset(
        {
            constraint_id
            for cell in cells
            for constraint_id in cell["covers_constraint_ids"]
        }
    )


def _first_cell_witness(
    cells: Sequence[Mapping[str, Any]],
    *,
    required_constraint_ids: Sequence[str],
    minimum_count: int,
) -> list[dict[str, Any]] | None:
    ordered = sorted(
        [copy.deepcopy(dict(row)) for row in cells],
        key=lambda row: row["cell_id"],
    )
    for size in range(max(0, minimum_count), len(ordered) + 1):
        for subset in itertools.combinations(ordered, size):
            if _selection_covers(
                subset,
                required_constraint_ids=required_constraint_ids,
                minimum_count=minimum_count,
            ):
                return [copy.deepcopy(dict(row)) for row in subset]
    return None


def _problem_is_satisfiable(
    cells: Sequence[Mapping[str, Any]],
    obligations: Sequence[Mapping[str, Any]],
) -> bool:
    minimum = 0
    required: list[str] = []
    for obligation in obligations:
        if obligation["kind"] == "minimum_distinct_family_count":
            minimum = int(obligation["value"])
        else:
            required.append(str(obligation["constraint_id"]))
    return (
        _first_cell_witness(
            cells,
            required_constraint_ids=required,
            minimum_count=minimum,
        )
        is not None
    )


def _minimal_unsat_core(
    cells: Sequence[Mapping[str, Any]],
    obligations: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    for size in range(1, len(obligations) + 1):
        for subset in itertools.combinations(obligations, size):
            if _problem_is_satisfiable(cells, subset):
                continue
            if all(
                _problem_is_satisfiable(
                    cells, [item for index, item in enumerate(subset) if index != drop]
                )
                for drop in range(len(subset))
            ):
                return [copy.deepcopy(dict(row)) for row in subset]
    _fail(
        "coverage_solver_internal_error",
        "finite UNSAT problem lacks an inclusion-minimal core",
    )


def solve_target_predeclared_coverage(
    problem: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic SAT witness or minimal UNSAT countermodel."""

    value = _validate_coverage_problem(
        problem, expected_constraint_ids=problem["required_constraint_ids"]
    )
    cells = value["admissible_cells"]
    required = value["required_constraint_ids"]
    minimum = int(value["minimum_distinct_family_count"])
    witness = _first_cell_witness(
        cells,
        required_constraint_ids=required,
        minimum_count=minimum,
    )
    if witness is not None:
        assignment = {
            constraint_id: next(
                cell["cell_id"]
                for cell in witness
                if constraint_id in cell["covers_constraint_ids"]
            )
            for constraint_id in required
        }
        return _seal(
            {
                "solver_kind": "finite_exhaustive_family_coverage_v1",
                "problem_digest": value["content_digest"],
                "status": "sat",
                "sat_witness": {
                    "selected_cell_ids": [
                        cell["cell_id"] for cell in witness
                    ],
                    "constraint_assignment": assignment,
                },
                "minimal_unsat_core": None,
                "countermodel": None,
                "enumeration_bound": 2 ** len(cells),
            }
        )

    obligations: list[dict[str, Any]] = [
        {
            "obligation_id": "minimum-distinct-family-count",
            "kind": "minimum_distinct_family_count",
            "value": minimum,
        },
        *[
            {
                "obligation_id": f"cover-{constraint_id}",
                "kind": "cover_constraint",
                "constraint_id": constraint_id,
            }
            for constraint_id in required
        ],
    ]
    core = _minimal_unsat_core(cells, obligations)
    best: list[dict[str, Any]] = []
    for size in range(len(cells) + 1):
        for subset in itertools.combinations(cells, size):
            covered = {
                item
                for cell in subset
                for item in cell["covers_constraint_ids"]
            }
            best_covered = {
                item
                for cell in best
                for item in cell["covers_constraint_ids"]
            }
            if (len(subset), len(covered), sorted(cell["cell_id"] for cell in subset)) > (
                len(best),
                len(best_covered),
                sorted(cell["cell_id"] for cell in best),
            ):
                best = [copy.deepcopy(dict(row)) for row in subset]
    covered = {
        item for cell in best for item in cell["covers_constraint_ids"]
    }
    return _seal(
        {
            "solver_kind": "finite_exhaustive_family_coverage_v1",
            "problem_digest": value["content_digest"],
            "status": "unsat",
            "sat_witness": None,
            "minimal_unsat_core": core,
            "countermodel": {
                "available_cell_ids": [row["cell_id"] for row in cells],
                "maximum_distinct_family_count": len(cells),
                "maximal_selection_cell_ids": [
                    row["cell_id"] for row in best
                ],
                "covered_constraint_ids": sorted(covered),
                "uncovered_constraint_ids": sorted(set(required) - covered),
            },
            "enumeration_bound": 2 ** len(cells),
        }
    )


def verify_target_predeclared_coverage_certificate(
    problem: Mapping[str, Any], certificate: Mapping[str, Any]
) -> dict[str, Any]:
    """Recompute the complete finite certificate and reject caller prose."""

    value = copy.deepcopy(dict(certificate))
    _verify_seal(value, "finite coverage certificate")
    expected = solve_target_predeclared_coverage(problem)
    if value != expected:
        _fail(
            "coverage_certificate_replay_mismatch",
            "SAT witness or minimal UNSAT countermodel changed",
        )
    return value


def _reopen_literature_authority(
    *,
    literature_projection: Mapping[str, Any],
    literature_bundle: Mapping[str, Any],
    governed_present_use_at: str,
) -> dict[str, Any]:
    projection = copy.deepcopy(dict(literature_projection))
    bundle = copy.deepcopy(dict(literature_bundle))
    try:
        expected = build_conceptual_ancestry_literature_projection(
            literature_bundle=bundle,
            semantic_snapshot=projection["semantic_snapshot"],
            literature_snapshot_capture_bridge=projection["semantic_bridge"],
            present_use_at=_text(
                governed_present_use_at, "governed_present_use_at"
            ),
        )
    except (KeyError, ContractError) as exc:
        raise AggressiveProviderSearchError(
            "literature_authority_reopen_failed",
            "raw capture, bridge, snapshot, bundle, or currentness failed replay",
        ) from exc
    if projection != expected:
        _fail(
            "literature_authority_replay_mismatch",
            "literature projection is detached from its exact current bundle",
        )
    literature_input = copy.deepcopy(
        dict(expected["literature_derived_invention_input"])
    )
    _verify_seal(literature_input, "literature-derived invention input")
    return _seal(
        {
            "authority_kind": "transitively_reopened_bounded_literature_v1",
            "governed_present_use_at": governed_present_use_at,
            "literature_bundle": bundle,
            "literature_bundle_digest": bundle["content_digest"],
            "literature_projection": expected,
            "literature_projection_digest": expected["content_digest"],
            "literature_input": literature_input,
            "literature_input_digest": literature_input["content_digest"],
            "global_latestness_authority": None,
            "source_truth_authority": None,
            "literature_benefit_authority": None,
            "clock_attestation_authority": None,
        }
    )


def _validate_provider_authorities(
    authorities: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    if (
        not isinstance(authorities, Sequence)
        or isinstance(authorities, (str, bytes, bytearray))
        or len(authorities) < 2
    ):
        _fail(
            "provider_authority_invalid",
            "provider-plural search requires at least two authority descriptors",
        )
    rows: list[dict[str, Any]] = []
    fields = frozenset(
        {
            "authority_id",
            "provider_id",
            "model_id",
            "human_operator_id",
            "declared_channel_id",
        }
    )
    for raw in authorities:
        _exact(raw, fields, "provider authority")
        row = copy.deepcopy(dict(raw))
        for field in (
            "authority_id",
            "provider_id",
            "model_id",
            "declared_channel_id",
        ):
            validate_identifier(str(row[field]), field)
        if row["human_operator_id"] is not None:
            validate_identifier(
                str(row["human_operator_id"]), "human_operator_id"
            )
        rows.append(row)
    if len({row["authority_id"] for row in rows}) != len(rows):
        _fail("provider_authority_invalid", "authority IDs must be unique")
    if len({row["provider_id"] for row in rows}) < 2:
        _fail(
            "provider_plurality_absent",
            "at least two declared provider identities must receive slots",
        )
    if len({row["model_id"] for row in rows}) < 2:
        _fail(
            "model_plurality_absent",
            "at least two declared model identities must receive slots",
        )
    return rows


def _validate_template_corpus(
    templates: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    if (
        not isinstance(templates, Sequence)
        or isinstance(templates, (str, bytes, bytearray))
        or not templates
    ):
        _fail(
            "template_corpus_invalid",
            "at least one precommitted known-template attack is required",
        )
    fields = frozenset({"template_id", "semantic_core", "typed_family_evidence"})
    rows: list[dict[str, Any]] = []
    for raw in templates:
        _exact(raw, fields, "known template")
        validate_identifier(str(raw["template_id"]), "template_id")
        evidence = copy.deepcopy(dict(raw["typed_family_evidence"]))
        _exact(evidence, _FAMILY_EVIDENCE_FIELDS, "template family evidence")
        rows.append(
            {
                "template_id": str(raw["template_id"]),
                "semantic_core": copy.deepcopy(dict(raw["semantic_core"])),
                "typed_family_evidence": evidence,
            }
        )
    rows.sort(key=lambda row: row["template_id"])
    if len({row["template_id"] for row in rows}) != len(rows):
        _fail("template_corpus_invalid", "template identities repeat")
    return rows


def _slot_roles(requested_count: int) -> list[str]:
    return [
        "capable_conservative_control",
        "protected_wildcard",
        "protected_wildcard",
        *(["aggressive_candidate"] * (requested_count - 3)),
    ]


def build_aggressive_provider_search_request(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    target_pressure: str,
    root_contradictions: Sequence[str],
    protected_successes: Sequence[str],
    literature_projection: Mapping[str, Any],
    literature_bundle: Mapping[str, Any],
    governed_present_use_at: str,
    known_taxonomy: Mapping[str, Any],
    coverage_problem: Mapping[str, Any],
    known_template_corpus: Sequence[Mapping[str, Any]],
    provider_authorities: Sequence[Mapping[str, Any]],
    requested_count: int = 10,
    max_workers: int = 4,
    branch_wall_seconds: float = 2.0,
    phase_wall_seconds: float = 8.0,
) -> dict[str, Any]:
    """Precommit every author opportunity before any provider output exists."""

    validate_identifier(target_id, "target_id")
    validate_identifier(run_id, "run_id")
    if (
        isinstance(state_version, bool)
        or not isinstance(state_version, int)
        or state_version < 0
    ):
        _fail("request_invalid", "state_version must be nonnegative")
    if (
        isinstance(requested_count, bool)
        or not isinstance(requested_count, int)
        or not MIN_AUTHOR_SLOTS <= requested_count <= MAX_AUTHOR_SLOTS
    ):
        _fail("request_invalid", "provider search requires eight to twelve slots")
    if (
        isinstance(max_workers, bool)
        or not isinstance(max_workers, int)
        or not 2 <= max_workers <= requested_count
    ):
        _fail("request_invalid", "provider search max_workers must be in [2, slots]")
    if (
        isinstance(branch_wall_seconds, bool)
        or not isinstance(branch_wall_seconds, (int, float))
        or isinstance(phase_wall_seconds, bool)
        or not isinstance(phase_wall_seconds, (int, float))
        or not 0 < float(branch_wall_seconds) <= float(phase_wall_seconds) <= 3600
    ):
        _fail("request_invalid", "provider wave deadlines are invalid")

    roots = _text_list(root_contradictions, "root_contradictions")
    protected = _text_list(protected_successes, "protected_successes")
    constraint_ids = target_constraint_identifiers(roots, protected)
    problem = _validate_coverage_problem(
        coverage_problem, expected_constraint_ids=constraint_ids
    )
    if problem["target_id"] != target_id:
        _fail("coverage_problem_target_mismatch", "coverage problem crossed targets")
    if problem["minimum_distinct_family_count"] != MIN_DISTINCT_FAMILIES:
        _fail(
            "coverage_problem_invalid",
            "canonical provider search precommits an exact six-family minimum",
        )
    templates = _validate_template_corpus(known_template_corpus)
    authorities = _validate_provider_authorities(provider_authorities)
    literature_authority = _reopen_literature_authority(
        literature_projection=literature_projection,
        literature_bundle=literature_bundle,
        governed_present_use_at=governed_present_use_at,
    )
    literature_input = literature_authority["literature_input"]
    if literature_input.get("target_id") != target_id:
        _fail("literature_identity_mismatch", "literature input crossed targets")
    constraints = {
        "target_pressure": _text(target_pressure, "target_pressure"),
        "root_contradictions": roots,
        "protected_successes": protected,
        "constraint_ids": constraint_ids,
    }
    template_digest = canonical_digest(templates)
    slots: list[dict[str, Any]] = []
    for index, role in enumerate(_slot_roles(requested_count)):
        authority = authorities[index % len(authorities)]
        slots.append(
            {
                "slot_id": stable_identifier(
                    "aggressive-author-slot",
                    target_id,
                    run_id,
                    state_version,
                    index,
                    role,
                    authority,
                    literature_input["content_digest"],
                    problem["content_digest"],
                    template_digest,
                ),
                "slot_index": index,
                "exploration_role": role,
                "provider_authority": copy.deepcopy(authority),
                "equal_opportunity_budget": {
                    "wall_seconds": float(branch_wall_seconds)
                },
            }
        )
    core = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "aggressive_provider_search_request",
        "request_id": stable_identifier(
            "aggressive-provider-search-request",
            target_id,
            run_id,
            state_version,
            constraints,
            literature_input["content_digest"],
            problem["content_digest"],
            template_digest,
            slots,
        ),
        "namespace": {
            "target_id": target_id,
            "run_id": run_id,
            "state_version": state_version,
        },
        "target_constraints": constraints,
        "literature_authority": literature_authority,
        "literature_input_digest": literature_input["content_digest"],
        "known_taxonomy_commitment_digest": known_taxonomy_commitment(
            known_taxonomy
        ),
        "taxonomy_visibility": "withheld_by_commitment_only",
        "coverage_problem": problem,
        "coverage_problem_digest": problem["content_digest"],
        "known_template_corpus": templates,
        "known_template_corpus_digest": template_digest,
        "requested_count": requested_count,
        "minimum_distinct_family_count": MIN_DISTINCT_FAMILIES,
        "slot_schedule": slots,
        "process_budget": {
            "max_workers": max_workers,
            "branch_wall_seconds": float(branch_wall_seconds),
            "phase_wall_seconds": float(phase_wall_seconds),
        },
        "caller_supplied_inventions": False,
        "caller_supplied_family_labels": False,
        "fixed_programme_or_template_atlas": False,
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
    }
    return _seal(core)


def _generation_requests(request: Mapping[str, Any]) -> list[dict[str, Any]]:
    shared = {
        "namespace": request["namespace"],
        "target_constraints": request["target_constraints"],
        "literature_input": request["literature_authority"]["literature_input"],
        "literature_input_digest": request["literature_input_digest"],
        "known_taxonomy_commitment_digest": request[
            "known_taxonomy_commitment_digest"
        ],
        "coverage_problem_digest": request["coverage_problem_digest"],
        "known_template_corpus_digest": request[
            "known_template_corpus_digest"
        ],
        "caller_supplied_inventions": False,
        "caller_supplied_family_labels": False,
        "fixed_programme_or_template_atlas": False,
    }
    rows: list[dict[str, Any]] = []
    for slot in request["slot_schedule"]:
        core = {
            "phase": "pre_taxonomy_generation",
            "branch_id": stable_identifier(
                "aggressive-generation-branch", slot["slot_id"]
            ),
            "parent_request_digest": request["content_digest"],
            "slot": copy.deepcopy(slot),
            "expected_invention_id": stable_identifier(
                "aggressive-invention", slot["slot_id"]
            ),
            **copy.deepcopy(shared),
            "output_contract": "aggressive-provider-generation.v1",
            "budget": copy.deepcopy(slot["equal_opportunity_budget"]),
        }
        rows.append({**core, "request_digest": canonical_digest(core)})
    return rows


def _validate_generation_output(
    raw: Mapping[str, Any], request: Mapping[str, Any]
) -> dict[str, Any]:
    _exact(raw, _GENERATION_OUTPUT_FIELDS, "generation worker output")
    if (
        raw["output_kind"] != "aggressive_provider_generation"
        or raw["request_digest"] != request["request_digest"]
    ):
        _fail(
            "worker_output_binding_mismatch",
            "generation output does not bind its exact precommitted request",
        )
    invention = _validate_open_world_raw_invention(raw["raw_invention"])
    if invention["invention_id"] != request["expected_invention_id"]:
        _fail(
            "worker_output_binding_mismatch",
            "provider changed its precommitted invention identity",
        )
    return {
        "output_kind": "aggressive_provider_generation",
        "request_digest": request["request_digest"],
        "raw_invention": invention,
    }


def _terminal_receipt(
    request: Mapping[str, Any],
    *,
    started_at: str,
    elapsed_seconds: float,
    status: str,
    output: Mapping[str, Any] | None,
    failure_class: str | None,
    failure_detail: str | None,
) -> dict[str, Any]:
    core = {
        "receipt_id": stable_identifier(
            "aggressive-provider-terminal-receipt",
            request["request_digest"],
            status,
            output,
            failure_class,
            failure_detail,
        ),
        "phase": request["phase"],
        "branch_id": request["branch_id"],
        "slot_id": request["slot"]["slot_id"],
        "request_digest": request["request_digest"],
        "provider_authority": copy.deepcopy(
            request["slot"]["provider_authority"]
        ),
        "started_at": started_at,
        "completed_at": utc_now(),
        "elapsed_seconds": round(max(0.0, float(elapsed_seconds)), 6),
        "status": status,
        "output": copy.deepcopy(dict(output)) if output is not None else None,
        "output_digest": (
            canonical_digest(dict(output)) if output is not None else None
        ),
        "failure_class": failure_class,
        "failure_detail": failure_detail,
        "terminal_process_group_status": "reaped_no_background_authority",
        "isolation_scope": "deep_copy_and_killable_process_session_only",
    }
    return _seal(core)


def _receipts_from_outcomes(
    requests: Sequence[Mapping[str, Any]],
    outcomes: Sequence[Mapping[str, Any]],
    *,
    validator: Callable[[Mapping[str, Any], Mapping[str, Any]], dict[str, Any]],
) -> list[dict[str, Any]]:
    by_branch = {
        str(row["request"]["branch_id"]): row for row in outcomes
    }
    receipts: list[dict[str, Any]] = []
    for request in requests:
        outcome = by_branch[request["branch_id"]]
        message = outcome["message"]
        if message.get("kind") != "ok":
            status = (
                "timeout" if message.get("kind") == "timeout" else "failed"
            )
            receipts.append(
                _terminal_receipt(
                    request,
                    started_at=outcome["started_at"],
                    elapsed_seconds=float(outcome["elapsed"]),
                    status=status,
                    output=None,
                    failure_class=str(
                        message.get("error_class") or "worker_failure"
                    ),
                    failure_detail=str(message.get("detail") or "worker failed"),
                )
            )
            continue
        raw_output = message.get("payload")
        try:
            if not isinstance(raw_output, Mapping):
                _fail("worker_output_invalid", "worker returned a non-object")
            output = validator(raw_output, request)
        except (ContractError, KeyError, TypeError, ValueError) as exc:
            receipts.append(
                _terminal_receipt(
                    request,
                    started_at=outcome["started_at"],
                    elapsed_seconds=float(outcome["elapsed"]),
                    status="invalid",
                    output=(
                        copy.deepcopy(dict(raw_output))
                        if isinstance(raw_output, Mapping)
                        else None
                    ),
                    failure_class=type(exc).__name__,
                    failure_detail=str(exc),
                )
            )
            continue
        receipts.append(
            _terminal_receipt(
                request,
                started_at=outcome["started_at"],
                elapsed_seconds=float(outcome["elapsed"]),
                status="accepted",
                output=output,
                failure_class=None,
                failure_detail=None,
            )
        )
    return receipts


def _maturation_requests(
    request: Mapping[str, Any],
    *,
    generation_receipts: Sequence[Mapping[str, Any]],
    freeze: Mapping[str, Any],
) -> list[dict[str, Any]]:
    receipt_by_slot = {row["slot_id"]: row for row in generation_receipts}
    accepted_inventions = [
        copy.deepcopy(row["output"]["raw_invention"])
        for row in generation_receipts
        if row["status"] == "accepted"
    ]
    rows: list[dict[str, Any]] = []
    for slot in request["slot_schedule"]:
        author_receipt = receipt_by_slot[slot["slot_id"]]
        raw_invention = (
            copy.deepcopy(author_receipt["output"]["raw_invention"])
            if author_receipt["status"] == "accepted"
            else None
        )
        dependency_status = (
            "ready" if raw_invention is not None else "author_not_accepted"
        )
        core = {
            "phase": "post_freeze_parallel_maturation",
            "branch_id": stable_identifier(
                "aggressive-maturation-branch",
                slot["slot_id"],
                freeze["content_digest"],
            ),
            "parent_request_digest": request["content_digest"],
            "slot": copy.deepcopy(slot),
            "author_receipt_digest": author_receipt["content_digest"],
            "dependency_status": dependency_status,
            "raw_invention": raw_invention,
            "pre_taxonomy_freeze_digest": freeze["content_digest"],
            "target_constraints": request["target_constraints"],
            "literature_input": request["literature_authority"][
                "literature_input"
            ],
            "literature_input_digest": request["literature_input_digest"],
            "known_taxonomy_commitment_digest": request[
                "known_taxonomy_commitment_digest"
            ],
            "coverage_problem_digest": request["coverage_problem_digest"],
            "known_template_corpus_digest": request[
                "known_template_corpus_digest"
            ],
            "sibling_invention_digests": sorted(
                canonical_digest(row)
                for row in accepted_inventions
                if raw_invention is None
                or row["invention_id"] != raw_invention["invention_id"]
            ),
            "caller_supplied_family_labels": False,
            "output_contract": "aggressive-provider-maturation.v1",
            "budget": copy.deepcopy(slot["equal_opportunity_budget"]),
        }
        rows.append({**core, "request_digest": canonical_digest(core)})
    return rows


def _graph_topology(graph: Mapping[str, Any]) -> str:
    nodes = [str(item) for item in graph["nodes"]]
    edges = [dict(row) for row in graph["edges"]]
    adjacency = {node: [] for node in nodes}
    indegree = {node: 0 for node in nodes}
    for edge in edges:
        adjacency[edge["source"]].append(edge["target"])
        indegree[edge["target"]] += 1

    visiting: set[str] = set()
    visited: set[str] = set()

    def has_cycle(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for child in adjacency[node]:
            if has_cycle(child):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    if any(has_cycle(node) for node in nodes):
        return "feedback"
    if any(len(children) > 1 for children in adjacency.values()):
        return "branch"
    if any(value > 1 for value in indegree.values()):
        return "merge"
    undirected = {node: set() for node in nodes}
    for edge in edges:
        undirected[edge["source"]].add(edge["target"])
        undirected[edge["target"]].add(edge["source"])
    reachable: set[str] = set()
    frontier = [nodes[0]]
    while frontier:
        node = frontier.pop()
        if node in reachable:
            continue
        reachable.add(node)
        frontier.extend(undirected[node] - reachable)
    if len(reachable) == len(nodes) and len(edges) == len(nodes) - 1:
        return "chain"
    return "network"


def _validate_family_evidence(
    raw: Mapping[str, Any],
    *,
    matured: Mapping[str, Any],
    target_constraint_ids: Sequence[str],
) -> tuple[dict[str, Any], dict[str, str], list[str]]:
    _exact(raw, _FAMILY_EVIDENCE_FIELDS, "typed family evidence")
    evidence = copy.deepcopy(dict(raw))
    graph = evidence["mechanism_graph"]
    _exact(
        graph,
        frozenset({"nodes", "edges"}),
        "typed family mechanism graph",
    )
    nodes = _text_list(graph["nodes"], "mechanism graph nodes")
    if len(nodes) < 2:
        _fail("family_evidence_invalid", "mechanism graph needs at least two nodes")
    edges = graph["edges"]
    if not isinstance(edges, list) or not edges:
        _fail("family_evidence_invalid", "mechanism graph needs typed edges")
    normalized_edges: list[dict[str, str]] = []
    for edge in edges:
        _exact(
            edge,
            frozenset({"source", "relation", "target"}),
            "mechanism graph edge",
        )
        row = {
            "source": _text(edge["source"], "edge source"),
            "relation": _text(edge["relation"], "edge relation"),
            "target": _text(edge["target"], "edge target"),
        }
        if row["source"] not in nodes or row["target"] not in nodes:
            _fail(
                "family_evidence_invalid",
                "mechanism edge endpoint is outside the declared graph",
            )
        normalized_edges.append(row)
    if len({canonical_digest(row) for row in normalized_edges}) != len(
        normalized_edges
    ):
        _fail("family_evidence_invalid", "mechanism graph edges repeat")
    graph = {"nodes": nodes, "edges": normalized_edges}
    mechanism_text = " ".join(matured["semantic_core"]["mechanism_steps"]).lower()
    if any(node.lower() not in mechanism_text for node in nodes):
        _fail(
            "family_evidence_unbound",
            "typed mechanism nodes are absent from complete semantic content",
        )

    relation_polarity = str(evidence["relation_polarity"])
    if relation_polarity not in _RELATION_POLARITIES or relation_polarity not in {
        str(row["polarity"]).lower()
        for row in matured["semantic_core"]["relations"]
    }:
        _fail(
            "family_evidence_unbound",
            "typed relation polarity is absent from the semantic core",
        )
    intervention = evidence["intervention"]
    _exact(
        intervention,
        frozenset({"kind", "operation", "target_constraint_ids"}),
        "typed intervention",
    )
    intervention_kind = str(intervention["kind"])
    if intervention_kind not in _INTERVENTION_KINDS:
        _fail("family_evidence_invalid", "unknown intervention kind")
    _text(intervention["operation"], "intervention operation")
    covered = _text_list(
        intervention["target_constraint_ids"],
        "intervention target_constraint_ids",
    )
    if not set(covered).issubset(target_constraint_ids):
        _fail("family_evidence_invalid", "intervention names an unknown target atom")

    prediction = evidence["prediction"]
    _exact(
        prediction,
        frozenset(
            {
                "observable",
                "direction",
                "regime",
                "mechanism_step_index",
            }
        ),
        "typed prediction",
    )
    direction = str(prediction["direction"])
    if direction not in _PREDICTION_DIRECTIONS:
        _fail("family_evidence_invalid", "unknown prediction direction")
    _text(prediction["observable"], "prediction observable")
    _text(prediction["regime"], "prediction regime")
    step_index = prediction["mechanism_step_index"]
    if (
        isinstance(step_index, bool)
        or not isinstance(step_index, int)
        or not 0 <= step_index < len(matured["semantic_core"]["mechanism_steps"])
    ):
        _fail(
            "family_evidence_unbound",
            "prediction does not point to an exact mechanism step",
        )

    correction = evidence["correction"]
    _exact(
        correction,
        frozenset({"kind", "trigger", "revision"}),
        "typed correction",
    )
    correction_kind = str(correction["kind"])
    if correction_kind not in _CORRECTION_KINDS:
        _fail("family_evidence_invalid", "unknown correction kind")
    if correction["trigger"] != matured["semantic_core"]["correction_condition"]:
        _fail(
            "family_evidence_unbound",
            "typed correction trigger differs from the semantic core",
        )
    _text(correction["revision"], "correction revision")

    falsifier = evidence["falsifier"]
    _exact(
        falsifier,
        frozenset({"countermodel", "implicated_mechanism_step_indices"}),
        "typed falsifier",
    )
    if falsifier["countermodel"] != matured["semantic_core"]["falsifier"]:
        _fail(
            "family_evidence_unbound",
            "typed countermodel differs from the semantic core falsifier",
        )
    implicated = falsifier["implicated_mechanism_step_indices"]
    if (
        not isinstance(implicated, list)
        or not implicated
        or len(implicated) != len(set(implicated))
        or any(
            isinstance(index, bool)
            or not isinstance(index, int)
            or not 0
            <= index
            < len(matured["semantic_core"]["mechanism_steps"])
            for index in implicated
        )
    ):
        _fail(
            "family_evidence_unbound",
            "countermodel does not identify exact mechanism steps",
        )

    physics = evidence["physics_return"]
    _exact(
        physics,
        frozenset(
            {
                "carrier",
                "decision_delta",
                "protected_success_constraint_ids",
            }
        ),
        "typed physics return",
    )
    handback = matured["physics_handback"]
    if (
        physics["carrier"] != handback["physical_carrier"]
        or physics["decision_delta"] != handback["proposed_next_decision"]
    ):
        _fail(
            "family_evidence_unbound",
            "typed physics return differs from the complete physics handback",
        )
    protected_ids = _text_list(
        physics["protected_success_constraint_ids"],
        "physics protected_success_constraint_ids",
    )
    expected_protected = {
        item
        for item in target_constraint_ids
        if item.startswith("protected-success-")
    }
    if not set(protected_ids).issubset(expected_protected):
        _fail(
            "family_evidence_unbound",
            "physics return names a non-protected target atom",
        )

    topology = _graph_topology(graph)
    signature = {
        "intervention_kind": intervention_kind,
        "prediction_direction": direction,
        "correction_kind": correction_kind,
        "mechanism_topology": topology,
        "relation_polarity": relation_polarity,
        "physics_handback_status": str(handback["status"]),
    }
    evidence["mechanism_graph"] = graph
    return evidence, signature, sorted(covered)


def _validate_maturation_output(
    raw: Mapping[str, Any], request: Mapping[str, Any]
) -> dict[str, Any]:
    _exact(raw, _MATURATION_OUTPUT_FIELDS, "maturation worker output")
    if (
        raw["output_kind"] != "aggressive_provider_maturation"
        or raw["request_digest"] != request["request_digest"]
    ):
        _fail(
            "worker_output_binding_mismatch",
            "maturation output does not bind its exact branch request",
        )
    matured = _validate_open_world_matured(raw["matured_invention"])
    expected_role = (
        "wildcard"
        if request["slot"]["exploration_role"] == "protected_wildcard"
        else "candidate"
    )
    if (
        matured["invention_id"] != request["raw_invention"]["invention_id"]
        or matured["branch_id"] != request["branch_id"]
        or matured["exploration_role"] != expected_role
    ):
        _fail(
            "worker_output_binding_mismatch",
            "matured content changed precommitted identity or exploration role",
        )
    if (
        request["slot"]["exploration_role"] != "protected_wildcard"
        and matured["risk_reward"]["wildcard_reason"] is not None
    ):
        _fail(
            "role_forgery",
            "non-wildcard output cannot self-award wildcard protection",
        )
    if (
        request["slot"]["exploration_role"]
        == "capable_conservative_control"
        and matured["physics_handback"]["status"] != "decision_changed"
    ):
        _fail(
            "capable_control_invalid",
            "conservative control must produce a task-specific decision handback",
        )
    evidence, _signature, _covered = _validate_family_evidence(
        raw["typed_family_evidence"],
        matured=matured,
        target_constraint_ids=request["target_constraints"]["constraint_ids"],
    )
    return {
        "output_kind": "aggressive_provider_maturation",
        "request_digest": request["request_digest"],
        "matured_invention": matured,
        "typed_family_evidence": evidence,
    }


def _normal_content(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): _normal_content(child)
            for key, child in sorted(value.items(), key=lambda row: str(row[0]))
            if str(key)
            not in {
                "invention_id",
                "branch_id",
                "slot_id",
                "candidate_alias",
                "provider_authority",
            }
        }
    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        return sorted(
            [_normal_content(child) for child in value], key=canonical_digest
        )
    if isinstance(value, str):
        return " ".join(value.lower().split())
    return value


def _content_words(value: Any) -> set[str]:
    strings: list[str] = []

    def collect(item: Any) -> None:
        if isinstance(item, Mapping):
            for child in item.values():
                collect(child)
        elif isinstance(item, Sequence) and not isinstance(
            item, (str, bytes, bytearray)
        ):
            for child in item:
                collect(child)
        elif isinstance(item, str):
            strings.append(item)

    collect(_normal_content(value))
    return {
        token.lower()
        for token in _TOKEN.findall(" ".join(strings))
        if len(token) > 2
    }


def _assess_families(
    matured_outputs: Sequence[Mapping[str, Any]],
    *,
    coverage_problem: Mapping[str, Any],
    target_constraint_ids: Sequence[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    cells = {
        row["cell_id"]: row for row in coverage_problem["admissible_cells"]
    }
    assessments: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []
    blind_inputs: list[dict[str, Any]] = []
    for output in matured_outputs:
        matured = output["matured_invention"]
        evidence, signature, covered = _validate_family_evidence(
            output["typed_family_evidence"],
            matured=matured,
            target_constraint_ids=target_constraint_ids,
        )
        complete_content = {
            "statement": matured["statement"],
            "semantic_core": matured["semantic_core"],
            "deep_reflection": matured["deep_reflection"],
            "risk_reward": matured["risk_reward"],
            "physics_handback": matured["physics_handback"],
            "typed_family_evidence": evidence,
        }
        complete_digest = canonical_digest(_normal_content(complete_content))
        alias = stable_identifier(
            "label-blind-family-candidate", complete_digest
        )
        cell_id = _cell_id(signature, covered)
        matched_cell_id = cell_id if cell_id in cells else None
        blind_inputs.append(
            {
                "candidate_alias": alias,
                "complete_content": complete_content,
                "complete_content_digest": complete_digest,
            }
        )
        assessments.append(
            {
                "candidate_alias": alias,
                "complete_content_digest": complete_digest,
                "family_signature": signature,
                "family_signature_digest": canonical_digest(signature),
                "target_constraint_ids": covered,
                "predeclared_cell_id": matched_cell_id,
                "worker_family_label_consumed": False,
                "slot_or_role_metadata_consumed": False,
            }
        )
        bindings.append(
            {
                "candidate_alias": alias,
                "invention_id": matured["invention_id"],
                "branch_id": matured["branch_id"],
                "complete_content_digest": complete_digest,
            }
        )
    assessments.sort(key=lambda row: row["candidate_alias"])
    bindings.sort(key=lambda row: row["candidate_alias"])
    blind_inputs.sort(key=lambda row: row["candidate_alias"])
    if len({row["candidate_alias"] for row in assessments}) != len(assessments):
        _fail(
            "complete_content_duplicate",
            "two provider outputs collapse to identical complete content",
        )
    assessment = _seal(
        {
            "assessor_kind": "label_blind_complete_content_family_reconstructor_v1",
            "coverage_problem_digest": coverage_problem["content_digest"],
            "blind_input_digest": canonical_digest(blind_inputs),
            "candidate_assessments": assessments,
            "distinct_typed_family_count": len(
                {
                    row["predeclared_cell_id"]
                    for row in assessments
                    if row["predeclared_cell_id"] is not None
                }
            ),
            "worker_family_labels_consumed": False,
            "slot_role_provider_metadata_consumed": False,
            "conceptual_merit_authorized": False,
        }
    )
    binding = _seal(
        {
            "assessment_digest": assessment["content_digest"],
            "bindings": bindings,
        }
    )
    return assessment, binding


def _copy_projection(
    semantic_core: Mapping[str, Any],
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    return _normal_content(
        {
            "semantic_core": semantic_core,
            "typed_family_evidence": evidence,
        }
    )


def _copy_control(
    matured_outputs: Sequence[Mapping[str, Any]],
    assessment: Mapping[str, Any],
    *,
    templates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    alias_by_digest = {
        row["complete_content_digest"]: row["candidate_alias"]
        for row in assessment["candidate_assessments"]
    }
    template_rows = [
        {
            "template_id": row["template_id"],
            "projection": _copy_projection(
                row["semantic_core"], row["typed_family_evidence"]
            ),
        }
        for row in templates
    ]
    results: list[dict[str, Any]] = []
    for output in matured_outputs:
        matured = output["matured_invention"]
        complete_digest = canonical_digest(
            _normal_content(
                {
                    "statement": matured["statement"],
                    "semantic_core": matured["semantic_core"],
                    "deep_reflection": matured["deep_reflection"],
                    "risk_reward": matured["risk_reward"],
                    "physics_handback": matured["physics_handback"],
                    "typed_family_evidence": output[
                        "typed_family_evidence"
                    ],
                }
            )
        )
        alias = alias_by_digest[complete_digest]
        projection = _copy_projection(
            matured["semantic_core"], output["typed_family_evidence"]
        )
        words = _content_words(projection)
        comparisons: list[tuple[float, str, bool]] = []
        for template in template_rows:
            template_words = _content_words(template["projection"])
            union = words | template_words
            similarity = len(words & template_words) / len(union) if union else 1.0
            comparisons.append(
                (
                    similarity,
                    template["template_id"],
                    projection == template["projection"],
                )
            )
        similarity, template_id, exact_copy = max(
            comparisons, key=lambda row: (row[0], row[1])
        )
        detected = exact_copy or similarity >= COPY_SIMILARITY_THRESHOLD
        results.append(
            {
                "candidate_alias": alias,
                "nearest_template_id": template_id,
                "nearest_similarity": round(similarity, 6),
                "exact_identity_erased_projection_copy": exact_copy,
                "copy_detected": detected,
            }
        )
    results.sort(key=lambda row: row["candidate_alias"])
    return _seal(
        {
            "control_kind": "precommitted_known_template_copy_attack_v1",
            "known_template_corpus_digest": canonical_digest(list(templates)),
            "similarity_threshold": COPY_SIMILARITY_THRESHOLD,
            "candidate_results": results,
            "eligible_candidate_aliases": [
                row["candidate_alias"]
                for row in results
                if not row["copy_detected"]
            ],
            "quarantined_copy_aliases": [
                row["candidate_alias"] for row in results if row["copy_detected"]
            ],
            "semantic_copy_implies_merit": False,
        }
    )


def _candidate_coverage_witness(
    assessment: Mapping[str, Any],
    binding: Mapping[str, Any],
    copy_control: Mapping[str, Any],
    *,
    slot_by_invention: Mapping[str, Mapping[str, Any]],
    coverage_problem: Mapping[str, Any],
) -> dict[str, Any] | None:
    binding_by_alias = {
        row["candidate_alias"]: row for row in binding["bindings"]
    }
    eligible = set(copy_control["eligible_candidate_aliases"])
    rows: list[dict[str, Any]] = []
    for row in assessment["candidate_assessments"]:
        source = binding_by_alias[row["candidate_alias"]]
        role = slot_by_invention[source["invention_id"]]["exploration_role"]
        if (
            row["candidate_alias"] not in eligible
            or role == "capable_conservative_control"
            or row["predeclared_cell_id"] is None
        ):
            continue
        rows.append(copy.deepcopy(dict(row)))
    rows.sort(key=lambda row: row["candidate_alias"])
    required = coverage_problem["required_constraint_ids"]
    minimum = int(coverage_problem["minimum_distinct_family_count"])
    for size in range(minimum, len(rows) + 1):
        for subset in itertools.combinations(rows, size):
            cell_ids = [row["predeclared_cell_id"] for row in subset]
            if len(cell_ids) != len(set(cell_ids)):
                continue
            covered = {
                constraint_id
                for row in subset
                for constraint_id in row["target_constraint_ids"]
            }
            if not set(required).issubset(covered):
                continue
            return {
                "selected_candidate_aliases": [
                    row["candidate_alias"] for row in subset
                ],
                "selected_cell_ids": cell_ids,
                "constraint_assignment": {
                    constraint_id: next(
                        row["candidate_alias"]
                        for row in subset
                        if constraint_id in row["target_constraint_ids"]
                    )
                    for constraint_id in required
                },
            }
    return None


def _validate_receipt(receipt: Mapping[str, Any], request: Mapping[str, Any]) -> None:
    _verify_seal(receipt, "terminal provider receipt")
    if (
        receipt["branch_id"] != request["branch_id"]
        or receipt["slot_id"] != request["slot"]["slot_id"]
        or receipt["request_digest"] != request["request_digest"]
        or receipt["provider_authority"]
        != request["slot"]["provider_authority"]
        or receipt["phase"] != request["phase"]
        or receipt["terminal_process_group_status"]
        != "reaped_no_background_authority"
        or receipt["isolation_scope"]
        != "deep_copy_and_killable_process_session_only"
    ):
        _fail("receipt_binding_mismatch", "terminal provider receipt changed")
    if receipt["status"] == "accepted":
        if receipt["output"] is None or receipt["output_digest"] != canonical_digest(
            receipt["output"]
        ):
            _fail("receipt_binding_mismatch", "accepted receipt lacks exact output")
        if receipt["failure_class"] is not None or receipt["failure_detail"] is not None:
            _fail("receipt_binding_mismatch", "accepted receipt claims a failure")
    elif receipt["status"] in {
        "invalid",
        "failed",
        "timeout",
        "dependency_blocked",
    }:
        if receipt["failure_class"] is None or receipt["failure_detail"] is None:
            _fail("receipt_binding_mismatch", "failure receipt lacks typed reason")
    else:
        _fail("receipt_binding_mismatch", "unknown terminal receipt status")


def _validate_execution_internal(
    packet: Mapping[str, Any], *, known_taxonomy: Mapping[str, Any]
) -> None:
    request = packet["request"]
    _verify_seal(request, "aggressive provider request")
    rebuilt_request = build_aggressive_provider_search_request(
        target_id=request["namespace"]["target_id"],
        run_id=request["namespace"]["run_id"],
        state_version=request["namespace"]["state_version"],
        target_pressure=request["target_constraints"]["target_pressure"],
        root_contradictions=request["target_constraints"]["root_contradictions"],
        protected_successes=request["target_constraints"]["protected_successes"],
        literature_projection=request["literature_authority"][
            "literature_projection"
        ],
        literature_bundle=request["literature_authority"]["literature_bundle"],
        governed_present_use_at=request["literature_authority"][
            "governed_present_use_at"
        ],
        known_taxonomy=known_taxonomy,
        coverage_problem=request["coverage_problem"],
        known_template_corpus=request["known_template_corpus"],
        provider_authorities=[
            row["provider_authority"]
            for row in request["slot_schedule"]
            if row["slot_index"]
            < len(
                {
                    item["provider_authority"]["authority_id"]
                    for item in request["slot_schedule"]
                }
            )
        ],
        requested_count=request["requested_count"],
        max_workers=request["process_budget"]["max_workers"],
        branch_wall_seconds=request["process_budget"]["branch_wall_seconds"],
        phase_wall_seconds=request["process_budget"]["phase_wall_seconds"],
    )
    if rebuilt_request != request:
        _fail("request_replay_mismatch", "provider search request changed")
    expected_author_requests = _generation_requests(request)
    if packet["author_requests"] != expected_author_requests:
        _fail("request_replay_mismatch", "author slot requests changed")
    if len(packet["author_receipts"]) != len(expected_author_requests):
        _fail("receipt_bijection_invalid", "author receipts are not slot-total")
    accepted_raw: list[dict[str, Any]] = []
    for author_request, receipt in zip(
        expected_author_requests, packet["author_receipts"], strict=True
    ):
        _validate_receipt(receipt, author_request)
        if receipt["status"] == "accepted":
            output = _validate_generation_output(
                receipt["output"], author_request
            )
            accepted_raw.append(output["raw_invention"])
    expected_freeze = build_pre_taxonomy_invention_freeze(
        target_id=request["namespace"]["target_id"],
        run_id=request["namespace"]["run_id"],
        state_version=request["namespace"]["state_version"],
        target_pressure=request["target_constraints"]["target_pressure"],
        root_contradictions=request["target_constraints"]["root_contradictions"],
        protected_successes=request["target_constraints"]["protected_successes"],
        raw_inventions=accepted_raw,
        known_taxonomy=known_taxonomy,
        generator_authority_digest=canonical_digest(
            packet["author_receipts"]
        ),
    )
    if packet["pre_taxonomy_freeze"] != expected_freeze:
        _fail("freeze_replay_mismatch", "pre-taxonomy provider freeze changed")
    validate_pre_taxonomy_invention_freeze(
        expected_freeze, known_taxonomy=known_taxonomy
    )
    expected_maturation_requests = _maturation_requests(
        request,
        generation_receipts=packet["author_receipts"],
        freeze=expected_freeze,
    )
    if packet["maturation_requests"] != expected_maturation_requests:
        _fail("request_replay_mismatch", "maturation branch requests changed")
    if len(packet["maturation_receipts"]) != len(expected_maturation_requests):
        _fail("receipt_bijection_invalid", "maturation receipts are not slot-total")
    matured_outputs: list[dict[str, Any]] = []
    for maturation_request, receipt in zip(
        expected_maturation_requests,
        packet["maturation_receipts"],
        strict=True,
    ):
        _validate_receipt(receipt, maturation_request)
        if maturation_request["dependency_status"] != "ready":
            if receipt["status"] != "dependency_blocked":
                _fail(
                    "dependency_receipt_invalid",
                    "unaccepted author branch entered maturation",
                )
            continue
        if receipt["status"] == "accepted":
            matured_outputs.append(
                _validate_maturation_output(receipt["output"], maturation_request)
            )
    if packet["matured_outputs"] != matured_outputs:
        _fail("maturation_replay_mismatch", "accepted matured outputs changed")
    assessment, binding = _assess_families(
        matured_outputs,
        coverage_problem=request["coverage_problem"],
        target_constraint_ids=request["target_constraints"]["constraint_ids"],
    )
    if (
        packet["family_assessment"] != assessment
        or packet["family_private_binding"] != binding
    ):
        _fail("family_assessment_replay_mismatch", "family reconstruction changed")
    copy_control = _copy_control(
        matured_outputs,
        assessment,
        templates=request["known_template_corpus"],
    )
    if packet["copy_control"] != copy_control:
        _fail("copy_control_replay_mismatch", "template copy control changed")
    target_certificate = verify_target_predeclared_coverage_certificate(
        request["coverage_problem"],
        packet["coverage_verification"]["target_problem_certificate"],
    )
    invention_to_slot = {
        stable_identifier("aggressive-invention", slot["slot_id"]): slot
        for slot in request["slot_schedule"]
    }
    candidate_witness = _candidate_coverage_witness(
        assessment,
        binding,
        copy_control,
        slot_by_invention=invention_to_slot,
        coverage_problem=request["coverage_problem"],
    )
    if target_certificate["status"] == "sat":
        if (
            packet["coverage_verification"]["status"]
            != "candidate_sat_witness_verified"
            or packet["coverage_verification"]["candidate_sat_witness"]
            != candidate_witness
            or candidate_witness is None
            or packet["coverage_verification"]["under_six_route_authorized"]
            is not False
        ):
            _fail(
                "candidate_coverage_incomplete",
                "target-feasible search lacks an exact six-family candidate witness",
            )
    else:
        if (
            packet["coverage_verification"]["status"]
            != "target_predeclared_unsat_countermodel_verified"
            or packet["coverage_verification"]["candidate_sat_witness"] is not None
            or packet["coverage_verification"]["under_six_route_authorized"]
            is not True
        ):
            _fail(
                "under_six_route_invalid",
                "under-six acceptance lacks target-predeclared finite UNSAT",
            )

    binding_by_alias = {
        row["candidate_alias"]: row for row in binding["bindings"]
    }
    slot_by_alias = {
        alias: invention_to_slot[row["invention_id"]]
        for alias, row in binding_by_alias.items()
    }
    wildcards = sorted(
        alias
        for alias, slot in slot_by_alias.items()
        if slot["exploration_role"] == "protected_wildcard"
    )
    controls = sorted(
        alias
        for alias, slot in slot_by_alias.items()
        if slot["exploration_role"] == "capable_conservative_control"
    )
    if len(wildcards) != 2 or len(controls) != 1:
        _fail(
            "protected_route_missing",
            "both wildcards and the capable conservative control must terminate accepted",
        )
    expected_retention = _seal(
        {
            "policy": "conflict_preserving_no_merit_pruning_v1",
            "eligible_candidate_aliases": copy_control[
                "eligible_candidate_aliases"
            ],
            "protected_wildcard_aliases": wildcards,
            "capable_conservative_control_alias": controls[0],
            "retained_candidate_aliases": sorted(
                {
                    *copy_control["eligible_candidate_aliases"],
                    *wildcards,
                    controls[0],
                }
            ),
            "merit_or_truth_selection_authorized": False,
        }
    )
    if packet["retention"] != expected_retention:
        _fail("retention_replay_mismatch", "wildcard/control retention changed")
    all_receipts = [
        *packet["author_receipts"],
        *packet["maturation_receipts"],
    ]
    expected_process = {
        "actual_killable_process_waves": 2,
        "scheduled_author_slots": request["requested_count"],
        "accepted_author_slots": sum(
            row["status"] == "accepted" for row in packet["author_receipts"]
        ),
        "accepted_maturation_slots": sum(
            row["status"] == "accepted"
            for row in packet["maturation_receipts"]
        ),
        "terminal_receipt_count": len(all_receipts),
        "partial_failure": any(row["status"] != "accepted" for row in all_receipts),
        "max_workers": request["process_budget"]["max_workers"],
        "overlap_measurement_authority": None,
    }
    if packet["process_summary"] != expected_process:
        _fail("process_summary_replay_mismatch", "process summary changed")
    if packet["authority_nulls"] != AUTHORITY_NULLS:
        _fail("authority_forgery", "provider search authority nulls changed")


def run_aggressive_provider_search(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    target_pressure: str,
    root_contradictions: Sequence[str],
    protected_successes: Sequence[str],
    literature_projection: Mapping[str, Any],
    literature_bundle: Mapping[str, Any],
    governed_present_use_at: str,
    known_taxonomy: Mapping[str, Any],
    coverage_problem: Mapping[str, Any],
    known_template_corpus: Sequence[Mapping[str, Any]],
    provider_authorities: Sequence[Mapping[str, Any]],
    generation_worker: ProviderWorker,
    maturation_worker: ProviderWorker,
    requested_count: int = 10,
    max_workers: int = 4,
    branch_wall_seconds: float = 2.0,
    phase_wall_seconds: float = 8.0,
) -> dict[str, Any]:
    """Execute one two-phase provider-plural aggressive conceptual search."""

    request = build_aggressive_provider_search_request(
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        target_pressure=target_pressure,
        root_contradictions=root_contradictions,
        protected_successes=protected_successes,
        literature_projection=literature_projection,
        literature_bundle=literature_bundle,
        governed_present_use_at=governed_present_use_at,
        known_taxonomy=known_taxonomy,
        coverage_problem=coverage_problem,
        known_template_corpus=known_template_corpus,
        provider_authorities=provider_authorities,
        requested_count=requested_count,
        max_workers=max_workers,
        branch_wall_seconds=branch_wall_seconds,
        phase_wall_seconds=phase_wall_seconds,
    )
    author_requests = _generation_requests(request)
    author_outcomes = run_bounded_killable_request_wave(
        author_requests,
        generation_worker,
        max_workers=max_workers,
        portfolio_wall_seconds=phase_wall_seconds,
    )
    author_receipts = _receipts_from_outcomes(
        author_requests,
        author_outcomes,
        validator=_validate_generation_output,
    )
    accepted_raw = [
        row["output"]["raw_invention"]
        for row in author_receipts
        if row["status"] == "accepted"
    ]
    if len(accepted_raw) < 3:
        _fail(
            "insufficient_accepted_authors",
            "fewer than three provider authors survived the terminal wave",
        )
    freeze = build_pre_taxonomy_invention_freeze(
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        target_pressure=target_pressure,
        root_contradictions=root_contradictions,
        protected_successes=protected_successes,
        raw_inventions=accepted_raw,
        known_taxonomy=known_taxonomy,
        generator_authority_digest=canonical_digest(author_receipts),
    )
    maturation_requests = _maturation_requests(
        request, generation_receipts=author_receipts, freeze=freeze
    )
    ready_requests = [
        row for row in maturation_requests if row["dependency_status"] == "ready"
    ]
    maturation_outcomes = run_bounded_killable_request_wave(
        ready_requests,
        maturation_worker,
        max_workers=max_workers,
        portfolio_wall_seconds=phase_wall_seconds,
    )
    ready_receipts = _receipts_from_outcomes(
        ready_requests,
        maturation_outcomes,
        validator=_validate_maturation_output,
    )
    ready_by_branch = {row["branch_id"]: row for row in ready_receipts}
    maturation_receipts: list[dict[str, Any]] = []
    for maturation_request in maturation_requests:
        if maturation_request["dependency_status"] == "ready":
            maturation_receipts.append(
                ready_by_branch[maturation_request["branch_id"]]
            )
        else:
            maturation_receipts.append(
                _terminal_receipt(
                    maturation_request,
                    started_at=utc_now(),
                    elapsed_seconds=0.0,
                    status="dependency_blocked",
                    output=None,
                    failure_class="author_not_accepted",
                    failure_detail=(
                        "maturation was not launched because its author receipt "
                        "was not accepted"
                    ),
                )
            )
    matured_outputs = [
        copy.deepcopy(row["output"])
        for row in maturation_receipts
        if row["status"] == "accepted"
    ]
    assessment, binding = _assess_families(
        matured_outputs,
        coverage_problem=request["coverage_problem"],
        target_constraint_ids=request["target_constraints"]["constraint_ids"],
    )
    copy_control = _copy_control(
        matured_outputs,
        assessment,
        templates=request["known_template_corpus"],
    )
    target_certificate = solve_target_predeclared_coverage(
        request["coverage_problem"]
    )
    invention_to_slot = {
        stable_identifier("aggressive-invention", slot["slot_id"]): slot
        for slot in request["slot_schedule"]
    }
    candidate_witness = _candidate_coverage_witness(
        assessment,
        binding,
        copy_control,
        slot_by_invention=invention_to_slot,
        coverage_problem=request["coverage_problem"],
    )
    if target_certificate["status"] == "sat" and candidate_witness is None:
        _fail(
            "candidate_coverage_incomplete",
            "target-feasible search did not return six eligible typed families",
        )
    coverage_verification = {
        "status": (
            "candidate_sat_witness_verified"
            if target_certificate["status"] == "sat"
            else "target_predeclared_unsat_countermodel_verified"
        ),
        "target_problem_certificate": target_certificate,
        "candidate_sat_witness": candidate_witness,
        "under_six_route_authorized": target_certificate["status"] == "unsat",
    }
    binding_by_alias = {
        row["candidate_alias"]: row for row in binding["bindings"]
    }
    slot_by_alias = {
        alias: invention_to_slot[row["invention_id"]]
        for alias, row in binding_by_alias.items()
    }
    wildcards = sorted(
        alias
        for alias, slot in slot_by_alias.items()
        if slot["exploration_role"] == "protected_wildcard"
    )
    controls = sorted(
        alias
        for alias, slot in slot_by_alias.items()
        if slot["exploration_role"] == "capable_conservative_control"
    )
    if len(wildcards) != 2 or len(controls) != 1:
        _fail(
            "protected_route_missing",
            "both wildcards and capable conservative control must survive",
        )
    retention = _seal(
        {
            "policy": "conflict_preserving_no_merit_pruning_v1",
            "eligible_candidate_aliases": copy_control[
                "eligible_candidate_aliases"
            ],
            "protected_wildcard_aliases": wildcards,
            "capable_conservative_control_alias": controls[0],
            "retained_candidate_aliases": sorted(
                {
                    *copy_control["eligible_candidate_aliases"],
                    *wildcards,
                    controls[0],
                }
            ),
            "merit_or_truth_selection_authorized": False,
        }
    )
    all_receipts = [*author_receipts, *maturation_receipts]
    process_summary = {
        "actual_killable_process_waves": 2,
        "scheduled_author_slots": requested_count,
        "accepted_author_slots": sum(
            row["status"] == "accepted" for row in author_receipts
        ),
        "accepted_maturation_slots": sum(
            row["status"] == "accepted" for row in maturation_receipts
        ),
        "terminal_receipt_count": len(all_receipts),
        "partial_failure": any(row["status"] != "accepted" for row in all_receipts),
        "max_workers": max_workers,
        "overlap_measurement_authority": None,
    }
    core = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "aggressive_provider_search_execution",
        "execution_id": stable_identifier(
            "aggressive-provider-search-execution",
            request["content_digest"],
            [row["content_digest"] for row in all_receipts],
            assessment["content_digest"],
            target_certificate["content_digest"],
        ),
        "request": request,
        "request_digest": request["content_digest"],
        "author_requests": author_requests,
        "author_receipts": author_receipts,
        "pre_taxonomy_freeze": freeze,
        "maturation_requests": maturation_requests,
        "maturation_receipts": maturation_receipts,
        "matured_outputs": matured_outputs,
        "family_assessment": assessment,
        "family_private_binding": binding,
        "copy_control": copy_control,
        "coverage_verification": coverage_verification,
        "retention": retention,
        "process_summary": process_summary,
        "causal_order": [
            "current_literature_transitively_reopened",
            "author_slots_precommitted",
            "parallel_authors_terminal",
            "pre_taxonomy_inventions_frozen",
            "parallel_maturation_terminal",
            "label_blind_complete_content_families_reconstructed",
            "template_copy_attacks_applied",
            "finite_target_coverage_solved_and_verified",
            "wildcards_and_capable_control_retained",
        ],
        "direct_theory_preference_proof_schedule_experiment_effect": False,
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
    packet = _seal(core)
    validate_payload(packet, SCHEMA_NAME)
    _validate_execution_internal(packet, known_taxonomy=known_taxonomy)
    return packet


def validate_aggressive_provider_search_execution(
    packet: Mapping[str, Any], *, known_taxonomy: Mapping[str, Any]
) -> dict[str, Any]:
    """Reopen currentness, receipts, freezes, families, copies, and coverage."""

    value = copy.deepcopy(dict(packet))
    validate_payload(value, SCHEMA_NAME)
    _verify_seal(value, "aggressive provider search execution")
    _validate_execution_internal(value, known_taxonomy=known_taxonomy)
    return value


__all__ = [
    "AUTHORITY_NULLS",
    "AggressiveProviderSearchError",
    "build_aggressive_provider_search_request",
    "build_target_predeclared_coverage_problem",
    "run_aggressive_provider_search",
    "solve_target_predeclared_coverage",
    "target_constraint_identifiers",
    "validate_aggressive_provider_search_execution",
    "verify_target_predeclared_coverage_certificate",
]
