# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Open-world invention and non-saturating conceptual-merit foundations.

The existing high-risk portfolio begins from a useful authored corner atlas.
This module adds the logically earlier operation that the discovery programme
was missing: invent raw conceptual possibilities while the known taxonomy is
withheld, freeze their exact bytes, and expose the taxonomy only to a separate
classifier.  Maturation then requires relation-bearing semantic cores, six
deep reflection lenses, branch-local intent/manifests/terminal receipts, and
pairwise content nonredundancy.

Conceptual merit is deliberately a second artifact.  Hard integrity is checked
before judging; judges see counterbalanced aliases and content only; outcomes
are pairwise categorical comparisons rather than capped scores.  The result is
a typed Pareto frontier with a protected high-upside wildcard rule.  Every
artifact states the central epistemic boundary: these deterministic controls
authorize internal exploration only, never creativity, truth, physics value,
or evaluator independence.
"""

from __future__ import annotations

import copy
import datetime as dt
import itertools
import re
import unicodedata
from collections import Counter
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path, PurePosixPath
from typing import Any

from .benchmark_process import (
    BenchmarkIntegrityError,
    _load_json_object,
    _write_immutable_json,
)
from .budgets import contained_path
from .contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_digest,
    validate_identifier,
    validate_instance,
)
from .research_worker_isolation import (
    ResearchWorkerAdapter,
    ResearchWorkerIntegrityError,
    build_isolation_requirement,
    receipt_summary,
    strongest_available_isolation,
    validate_isolation_requirement,
    validate_research_worker_receipt,
)


FREEZE_SCHEMA = "pre_taxonomy_invention_freeze.schema.json"
CLASSIFICATION_SCHEMA = "post_freeze_taxonomy_classification.schema.json"
PORTFOLIO_SCHEMA = "open_world_maturation_portfolio.schema.json"
MERIT_SCHEMA = "non_saturating_conceptual_merit.schema.json"
INTEGRITY_SCHEMA = "open_world_hard_integrity_receipt.schema.json"

DEEP_REFLECTION_LENSES = (
    "ontological",
    "dialectical",
    "genealogical",
    "modal_explanatory",
    "unification",
    "philosophy_of_physics",
)
MERIT_DIMENSIONS = (
    "essential_relevance",
    "explanatory_compression",
    "unification_with_preserved_differences",
    "conceptual_depth",
    "philosophical_understanding",
    "correction_quality",
    "high_risk_upside",
    "physics_decision_relevance",
)
BASE_DOMINANCE_DIMENSIONS = tuple(
    dimension for dimension in MERIT_DIMENSIONS if dimension != "high_risk_upside"
)
CONTROL_KINDS = frozenset({"capable", "restatement", "sham"})

_RAW_INVENTION_FIELDS = frozenset(
    {
        "invention_id",
        "conjecture",
        "primitive_hunches",
        "relation_hunches",
        "mechanism_hunch",
        "root_tension_contact",
        "counterfactual_world",
        "protected_successes",
        "risk_if_wrong",
        "upside_if_right",
        "first_falsifier",
        "correction_path",
    }
)
_TAXONOMY_LEAK_FIELDS = frozenset(
    {
        "atlas",
        "category_lens",
        "control_kind",
        "corner",
        "corner_family",
        "exploration_role",
        "hott_lens",
        "known_corner",
        "proposal_type",
        "strategy",
        "taxonomy",
        "taxonomy_id",
    }
)
_REFLECTION_FIELDS = frozenset(
    {
        "named_relation",
        "relation_before",
        "relation_operation",
        "mutation_status",
        "relation_after",
        "exposed_assumption",
        "strongest_opposition",
        "conceptual_mutation",
        "consequence",
        "boundary_or_correction",
        "semantic_core_correction_link",
        "physics_handback_link",
    }
)
_SEMANTIC_CORE_FIELDS = frozenset(
    {
        "primitives",
        "relations",
        "mechanism_steps",
        "protected_differences",
        "boundary_regimes",
        "counterfactual_consequence",
        "falsifier",
        "correction_condition",
    }
)
_MATURED_FIELDS = frozenset(
    {
        "invention_id",
        "branch_id",
        "exploration_role",
        "statement",
        "semantic_core",
        "deep_reflection",
        "risk_reward",
        "physics_handback",
    }
)
_CONTENT_FIELDS = frozenset(
    {
        "statement",
        "semantic_core",
        "deep_reflection",
        "risk_reward",
        "physics_handback",
    }
)
_FORBIDDEN_MERIT_KEYS = re.compile(
    r"(^|_)(aggregate_score|average|mean|rating|scalar|score|total|weighted_sum)($|_)",
    re.I,
)
_SPACE = re.compile(r"[^a-z0-9]+")

_SEMANTIC_STOPWORDS = frozenset(
    {
        "a", "an", "and", "as", "at", "be", "before", "by", "for", "from",
        "if", "in", "into", "is", "it", "of", "on", "only", "or", "that",
        "the", "then", "this", "to", "under", "when", "where", "which", "with",
    }
)
_SEMANTIC_EQUIVALENTS = {
    "bounds": "constraint",
    "bounded": "constraint",
    "constrain": "constraint",
    "constrains": "constraint",
    "constrained": "constraint",
    "constraints": "constraint",
    "limit": "constraint",
    "limits": "constraint",
    "restrict": "constraint",
    "restricts": "constraint",
    "carrier": "mediator",
    "carriers": "mediator",
    "mediate": "mediator",
    "mediates": "mediator",
    "obstructions": "obstruction",
    "regimes": "regime",
    "relations": "relation",
    "worlds": "world",
    "histories": "history",
    "transports": "transport",
    "reconstructions": "reconstruction",
}
_LENS_OPERATIONS = {
    "ontological": frozenset({"retype_source", "retype_target", "invert_dependence"}),
    "dialectical": frozenset({"negate_relation", "reverse_relation", "sublate_opposition"}),
    "genealogical": frozenset({"trace_origin", "expose_contingency", "replace_inheritance"}),
    "modal_explanatory": frozenset(
        {"vary_modality", "separate_necessity_sufficiency", "counterfactualize_relation"}
    ),
    "unification": frozenset(
        {"factor_common_structure", "preserve_difference", "expose_unification_cost"}
    ),
    "philosophy_of_physics": frozenset(
        {"identify_physical_carrier", "separate_model_reality", "locate_explanatory_commitment"}
    ),
}
_OPEN_WORLD_WORKER_AUTHORITY_BOUNDARY = (
    "caller_supplied_theory_material_validated_in_one_local_branch; no creativity, "
    "truth, physics-value, hidden-input, cognitive-independence, or semantic-"
    "independence authority"
)
_NO_ACCESS_OBSERVATION = {
    "sibling_read_attempted": False,
    "sibling_read_succeeded": None,
    "sibling_read_error": None,
    "sibling_write_attempted": False,
    "sibling_write_succeeded": None,
    "sibling_write_error": None,
    "late_descendant_spawned": False,
}


class OpenWorldCreativityError(ContractError):
    """Carry a stable failure reason for creativity and merit boundaries."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"open_world_creativity[{reason_code}]: {message}")


def _fail(reason_code: str, message: str) -> None:
    raise OpenWorldCreativityError(reason_code, message)


def _exact_fields(value: Mapping[str, Any], expected: frozenset[str], context: str) -> None:
    actual = set(value)
    if actual != set(expected):
        _fail(
            "closed_contract_violation",
            f"{context} fields differ: missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}",
        )


def _text(value: Any, context: str, *, minimum: int = 8) -> str:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        _fail("insubstantive_content", f"{context} must contain substantive text")
    return value.strip()


def _text_list(value: Any, context: str, *, minimum_items: int = 1) -> list[str]:
    if not isinstance(value, list) or len(value) < minimum_items:
        _fail("insubstantive_content", f"{context} must be a nonempty list")
    rows = [_text(item, f"{context}[{index}]", minimum=2) for index, item in enumerate(value)]
    if len(rows) != len(set(rows)):
        _fail("duplicate_content", f"{context} contains duplicates")
    return rows


def _normal_term(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return _SPACE.sub(" ", value).strip()


def _semantic_tokens(value: Any) -> frozenset[str]:
    """Return a conservative presentation-normalized lexical concept set.

    This is intentionally not advertised as semantic equivalence.  It catches
    exact containment, common inflections, and a small set of theory-neutral
    paraphrases so that a one-token decoration cannot satisfy nonredundancy.
    """

    texts: list[str] = []

    def collect(child: Any) -> None:
        if isinstance(child, Mapping):
            for key, item in sorted(child.items()):
                texts.append(str(key))
                collect(item)
        elif isinstance(child, list):
            for item in child:
                collect(item)
        elif isinstance(child, str):
            texts.append(child)

    collect(value)
    tokens: set[str] = set()
    for token in _normal_term(" ".join(texts)).split():
        if token in _SEMANTIC_STOPWORDS or token.isdigit():
            continue
        normalized = _SEMANTIC_EQUIVALENTS.get(token, token)
        if normalized.endswith("ies") and len(normalized) > 5:
            normalized = normalized[:-3] + "y"
        elif normalized.endswith("s") and len(normalized) > 4:
            normalized = normalized[:-1]
        tokens.add(_SEMANTIC_EQUIVALENTS.get(normalized, normalized))
    return frozenset(tokens)


def _set_overlap(left: frozenset[str], right: frozenset[str]) -> tuple[float, float]:
    if not left or not right:
        return 0.0, 0.0
    overlap = len(left & right)
    return overlap / len(left | right), overlap / min(len(left), len(right))


def _relation_name(relation: Mapping[str, Any]) -> str:
    return f"{relation['source']} --{relation['polarity']}--> {relation['target']}"


def _normal_semantic_value(value: Any) -> Any:
    """Normalize presentation while retaining typed theoretical polarity."""

    if isinstance(value, Mapping):
        return {
            str(key): _normal_semantic_value(child)
            for key, child in sorted(value.items())
        }
    if isinstance(value, list):
        rows = [_normal_semantic_value(child) for child in value]
        return sorted(rows, key=canonical_digest)
    if isinstance(value, str):
        return _normal_term(value)
    return value


def _record_digest(record: Mapping[str, Any], digest_field: str) -> str:
    return canonical_digest({key: value for key, value in record.items() if key != digest_field})


def _seal(record: Mapping[str, Any], digest_field: str) -> dict[str, Any]:
    sealed = copy.deepcopy(dict(record))
    sealed[digest_field] = canonical_digest(sealed)
    return sealed


def _verify_seal(record: Mapping[str, Any], digest_field: str, context: str) -> None:
    if record.get(digest_field) != _record_digest(record, digest_field):
        _fail("digest_mismatch", f"{context} digest mismatch")


def _recursive_items(value: Any, path: str = "$") -> list[tuple[str, str | None, Any]]:
    rows: list[tuple[str, str | None, Any]] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}/{key}"
            rows.append((child_path, str(key), child))
            rows.extend(_recursive_items(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            rows.extend(_recursive_items(child, f"{path}/{index}"))
    return rows


def _canonical_taxonomy(known_taxonomy: Mapping[str, Any]) -> list[dict[str, str]]:
    if not isinstance(known_taxonomy, Mapping) or not known_taxonomy:
        _fail("taxonomy_invalid", "known taxonomy must be a nonempty mapping")
    rows: list[dict[str, str]] = []
    for corner_id, raw in known_taxonomy.items():
        validate_identifier(str(corner_id), "corner_id")
        if not isinstance(raw, Mapping):
            _fail("taxonomy_invalid", f"taxonomy row {corner_id!r} is not an object")
        _exact_fields(raw, frozenset({"name", "definition"}), f"taxonomy {corner_id}")
        rows.append(
            {
                "corner_id": str(corner_id),
                "name": _text(raw["name"], f"taxonomy {corner_id} name", minimum=3),
                "definition": _text(raw["definition"], f"taxonomy {corner_id} definition"),
            }
        )
    return sorted(rows, key=lambda row: row["corner_id"])


def known_taxonomy_commitment(known_taxonomy: Mapping[str, Any]) -> str:
    """Commit the withheld vocabulary without exposing it to invention workers."""

    return canonical_digest(_canonical_taxonomy(known_taxonomy))


def _assert_pre_taxonomy_hidden(value: Any, taxonomy: Sequence[Mapping[str, str]]) -> None:
    forbidden_terms = {
        _normal_term(str(row[field]))
        for row in taxonomy
        for field in ("corner_id", "name")
    }
    for path, key, child in _recursive_items(value):
        if key is not None and _normal_term(key).replace(" ", "_") in _TAXONOMY_LEAK_FIELDS:
            _fail("pre_freeze_taxonomy_leak", f"taxonomy-bearing field leaked at {path}")
        if isinstance(child, str):
            normalized = f" {_normal_term(child)} "
            for term in forbidden_terms:
                if term and f" {term} " in normalized:
                    _fail(
                        "pre_freeze_taxonomy_leak",
                        f"withheld taxonomy term leaked at {path}",
                    )


def _validate_raw_invention(raw: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(raw, _RAW_INVENTION_FIELDS, "raw invention")
    validate_identifier(str(raw["invention_id"]), "invention_id")
    for field in (
        "conjecture",
        "mechanism_hunch",
        "root_tension_contact",
        "counterfactual_world",
        "risk_if_wrong",
        "upside_if_right",
        "first_falsifier",
        "correction_path",
    ):
        _text(raw[field], f"raw invention {raw['invention_id']} {field}")
    for field in ("primitive_hunches", "relation_hunches", "protected_successes"):
        _text_list(raw[field], f"raw invention {raw['invention_id']} {field}")
    return copy.deepcopy(dict(raw))


def build_pre_taxonomy_invention_freeze(
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    target_pressure: str,
    root_contradictions: Sequence[str],
    protected_successes: Sequence[str],
    raw_inventions: Sequence[Mapping[str, Any]],
    known_taxonomy: Mapping[str, Any],
    generator_authority_digest: str,
) -> dict[str, Any]:
    """Freeze raw inventions while the known conceptual atlas is withheld.

    ``known_taxonomy`` is used only by this verifier.  The returned invention
    request and raw records contain only its commitment digest, so a downstream
    classifier can prove it ran after the freeze without supplying known-corner
    vocabulary to the invention payload.
    """

    validate_identifier(target_id, "target_id")
    validate_identifier(run_id, "run_id")
    if isinstance(state_version, bool) or not isinstance(state_version, int) or state_version < 0:
        _fail("namespace_invalid", "state_version must be a nonnegative integer")
    validate_digest(generator_authority_digest)
    taxonomy = _canonical_taxonomy(known_taxonomy)
    inventions = [_validate_raw_invention(row) for row in raw_inventions]
    if len(inventions) < 3:
        _fail("portfolio_too_small", "open-world invention requires at least three raw inventions")
    ids = [row["invention_id"] for row in inventions]
    if len(ids) != len(set(ids)):
        _fail("duplicate_invention", "raw invention identities must be unique")
    inventions.sort(key=lambda row: row["invention_id"])
    request = {
        "target_pressure": _text(target_pressure, "target pressure"),
        "root_contradictions": _text_list(list(root_contradictions), "root contradictions"),
        "protected_successes": _text_list(list(protected_successes), "protected successes"),
        "requested_invention_count": len(inventions),
        "generation_question": (
            "Invent a relation-bearing conceptual worldview that changes what can be "
            "asked or explained while preserving the stated target successes."
        ),
    }
    _assert_pre_taxonomy_hidden({"request": request, "raw_inventions": inventions}, taxonomy)
    core = {
        "schema_version": "1.0.0",
        "artifact_kind": "pre_taxonomy_invention_freeze",
        "freeze_id": stable_identifier(
            "invention-freeze", target_id, run_id, state_version, request, inventions
        ),
        "namespace": {
            "target_id": target_id,
            "run_id": run_id,
            "state_version": state_version,
        },
        "invention_request": request,
        "taxonomy_visibility": {
            "phase": "pre_taxonomy",
            "exposure_status": "withheld_by_commitment_only",
            "known_taxonomy_commitment_digest": canonical_digest(taxonomy),
        },
        "generator_authority_digest": generator_authority_digest,
        "raw_inventions": inventions,
        "raw_invention_set_digest": canonical_digest(inventions),
        "authority_nulls": {
            "taxonomy_hiddenness_scope": "artifact_payload_only",
            "generator_cognitive_independence": "unavailable",
            "creativity_authority": "unavailable",
            "truth_authority": "unavailable",
            "physics_value_authority": "unavailable",
        },
    }
    artifact = _seal(core, "content_digest")
    validate_pre_taxonomy_invention_freeze(artifact, known_taxonomy=known_taxonomy)
    return artifact


def validate_pre_taxonomy_invention_freeze(
    artifact: Mapping[str, Any], *, known_taxonomy: Mapping[str, Any]
) -> None:
    """Replay the freeze and its exact withheld-vocabulary audit."""

    validate_instance(artifact, FREEZE_SCHEMA)
    _verify_seal(artifact, "content_digest", "pre-taxonomy freeze")
    taxonomy = _canonical_taxonomy(known_taxonomy)
    if artifact["taxonomy_visibility"]["known_taxonomy_commitment_digest"] != canonical_digest(taxonomy):
        _fail("taxonomy_commitment_mismatch", "freeze binds a different withheld taxonomy")
    inventions = [_validate_raw_invention(row) for row in artifact["raw_inventions"]]
    if inventions != sorted(inventions, key=lambda row: row["invention_id"]):
        _fail("noncanonical_order", "raw inventions must be ordered by invention_id")
    if artifact["raw_invention_set_digest"] != canonical_digest(inventions):
        _fail("digest_mismatch", "raw invention set digest mismatch")
    _assert_pre_taxonomy_hidden(
        {"request": artifact["invention_request"], "raw_inventions": inventions},
        taxonomy,
    )


def _validate_taxonomy_extension_warrant(
    warrant: Mapping[str, Any],
    *,
    taxonomy: Sequence[Mapping[str, str]],
    raw_invention: Mapping[str, Any],
) -> dict[str, Any]:
    _exact_fields(
        warrant,
        frozenset(
            {
                "proposed_corner_id",
                "proposed_name",
                "insufficiency_of_known_taxonomy",
                "distinguishing_relations",
                "admission_test",
                "failure_condition",
            }
        ),
        "taxonomy extension warrant",
    )
    validate_identifier(str(warrant["proposed_corner_id"]), "proposed_corner_id")
    known_ids = {row["corner_id"] for row in taxonomy}
    if warrant["proposed_corner_id"] in known_ids:
        _fail("taxonomy_extension_invalid", "extension reuses a known corner identity")
    for field in (
        "proposed_name",
        "insufficiency_of_known_taxonomy",
        "admission_test",
        "failure_condition",
    ):
        _text(warrant[field], f"extension warrant {field}")
    _text_list(warrant["distinguishing_relations"], "extension distinguishing relations")

    proposed_name = _semantic_tokens(warrant["proposed_name"])
    proposed_substance = _semantic_tokens(
        {
            "name": warrant["proposed_name"],
            "relations": warrant["distinguishing_relations"],
        }
    )
    for known in taxonomy:
        name_jaccard, name_containment = _set_overlap(
            proposed_name, _semantic_tokens(known["name"])
        )
        known_substance = _semantic_tokens(
            {"name": known["name"], "definition": known["definition"]}
        )
        _jaccard, substance_containment = _set_overlap(
            proposed_substance, known_substance
        )
        if name_containment >= 0.8 and name_jaccard >= 0.6:
            _fail(
                "taxonomy_extension_renaming",
                "extension name is a presentation variant of a known corner",
            )
        if proposed_substance and substance_containment >= 0.9:
            _fail(
                "taxonomy_extension_subsumed",
                "extension relations are lexically subsumed by a known corner",
            )

    raw_relation_tokens = _semantic_tokens(
        {
            "relation_hunches": raw_invention["relation_hunches"],
            "mechanism_hunch": raw_invention["mechanism_hunch"],
            "counterfactual_world": raw_invention["counterfactual_world"],
        }
    )
    distinguishing_tokens = _semantic_tokens(warrant["distinguishing_relations"])
    if not distinguishing_tokens.intersection(raw_relation_tokens):
        _fail(
            "taxonomy_extension_ungrounded",
            "extension warrant is not grounded in the frozen invention relations",
        )
    return copy.deepcopy(dict(warrant))


def classify_frozen_inventions(
    freeze: Mapping[str, Any],
    *,
    known_taxonomy: Mapping[str, Any],
    decisions: Sequence[Mapping[str, Any]],
    classifier_authority_digest: str,
) -> dict[str, Any]:
    """Classify only frozen inventions or issue a typed taxonomy extension."""

    validate_pre_taxonomy_invention_freeze(freeze, known_taxonomy=known_taxonomy)
    validate_digest(classifier_authority_digest)
    taxonomy = _canonical_taxonomy(known_taxonomy)
    known_ids = {row["corner_id"] for row in taxonomy}
    invention_ids = [row["invention_id"] for row in freeze["raw_inventions"]]
    raw_by_id = {row["invention_id"]: row for row in freeze["raw_inventions"]}
    by_id: dict[str, dict[str, Any]] = {}
    for raw in decisions:
        if not isinstance(raw, Mapping):
            _fail("classification_invalid", "classification decision must be an object")
        _exact_fields(
            raw,
            frozenset({"invention_id", "status", "known_corner_id", "extension_warrant"}),
            "classification decision",
        )
        invention_id = str(raw["invention_id"])
        if invention_id not in invention_ids or invention_id in by_id:
            _fail("classification_bijection_invalid", "classifications must cover frozen inventions once")
        status = raw["status"]
        decision = copy.deepcopy(dict(raw))
        if status == "mapped_known_corner":
            if raw["known_corner_id"] not in known_ids or raw["extension_warrant"] is not None:
                _fail("known_corner_mapping_invalid", f"invalid known-corner mapping for {invention_id}")
        elif status == "taxonomy_extension_warranted":
            if raw["known_corner_id"] is not None or not isinstance(raw["extension_warrant"], Mapping):
                _fail("taxonomy_extension_invalid", f"missing extension warrant for {invention_id}")
            decision["extension_warrant"] = _validate_taxonomy_extension_warrant(
                raw["extension_warrant"],
                taxonomy=taxonomy,
                raw_invention=raw_by_id[invention_id],
            )
        else:
            _fail("classification_invalid", f"unknown classification status {status!r}")
        by_id[invention_id] = decision
    if set(by_id) != set(invention_ids):
        _fail("classification_bijection_invalid", "every frozen invention requires one decision")
    ordered = [by_id[invention_id] for invention_id in sorted(invention_ids)]
    extensions = [
        row["extension_warrant"]
        for row in ordered
        if row["status"] == "taxonomy_extension_warranted"
    ]
    if len({row["proposed_corner_id"] for row in extensions}) != len(extensions) or len(
        {_normal_term(row["proposed_name"]) for row in extensions}
    ) != len(extensions):
        _fail("taxonomy_extension_duplicate", "extension identities and names must be unique")
    core = {
        "schema_version": "1.0.0",
        "artifact_kind": "post_freeze_taxonomy_classification",
        "classification_id": stable_identifier(
            "invention-classification", freeze["content_digest"], ordered
        ),
        "freeze_id": freeze["freeze_id"],
        "freeze_digest": freeze["content_digest"],
        "known_taxonomy_commitment_digest": canonical_digest(taxonomy),
        "known_corner_ids": sorted(known_ids),
        "classifier_authority_digest": classifier_authority_digest,
        "phase_order": ["pre_taxonomy_frozen", "post_freeze_classified"],
        "decisions": ordered,
        "authority_nulls": {
            "classification_truth_authority": "unavailable",
            "taxonomy_exhaustiveness_authority": "unavailable",
            "creativity_authority": "unavailable",
        },
    }
    artifact = _seal(core, "content_digest")
    validate_post_freeze_taxonomy_classification(
        artifact, freeze=freeze, known_taxonomy=known_taxonomy
    )
    return artifact


def validate_post_freeze_taxonomy_classification(
    artifact: Mapping[str, Any],
    *,
    freeze: Mapping[str, Any],
    known_taxonomy: Mapping[str, Any],
) -> None:
    validate_instance(artifact, CLASSIFICATION_SCHEMA)
    _verify_seal(artifact, "content_digest", "post-freeze classification")
    validate_pre_taxonomy_invention_freeze(freeze, known_taxonomy=known_taxonomy)
    if artifact["freeze_id"] != freeze["freeze_id"] or artifact["freeze_digest"] != freeze["content_digest"]:
        _fail("freeze_binding_mismatch", "classification does not bind the exact freeze")
    if artifact["known_taxonomy_commitment_digest"] != known_taxonomy_commitment(known_taxonomy):
        _fail("taxonomy_commitment_mismatch", "classification taxonomy differs from freeze")
    known_ids = {row["corner_id"] for row in _canonical_taxonomy(known_taxonomy)}
    taxonomy = _canonical_taxonomy(known_taxonomy)
    invention_ids = {row["invention_id"] for row in freeze["raw_inventions"]}
    raw_by_id = {row["invention_id"]: row for row in freeze["raw_inventions"]}
    if (
        {row["invention_id"] for row in artifact["decisions"]} != invention_ids
        or len(artifact["decisions"]) != len(invention_ids)
    ):
        _fail("classification_bijection_invalid", "classification is not invention-total")
    for row in artifact["decisions"]:
        if row["status"] == "mapped_known_corner":
            if row["known_corner_id"] not in known_ids or row["extension_warrant"] is not None:
                _fail("known_corner_mapping_invalid", "known-corner replay failed")
        elif row["status"] == "taxonomy_extension_warranted":
            warrant = row["extension_warrant"]
            if row["known_corner_id"] is not None or not isinstance(warrant, Mapping):
                _fail("taxonomy_extension_invalid", "extension replay failed")
            _validate_taxonomy_extension_warrant(
                warrant,
                taxonomy=taxonomy,
                raw_invention=raw_by_id[row["invention_id"]],
            )
        else:
            _fail("classification_invalid", "unknown classification status")
    ordered = sorted(
        [copy.deepcopy(dict(row)) for row in artifact["decisions"]],
        key=lambda row: row["invention_id"],
    )
    extensions = [
        row["extension_warrant"]
        for row in ordered
        if row["status"] == "taxonomy_extension_warranted"
    ]
    if len({row["proposed_corner_id"] for row in extensions}) != len(extensions) or len(
        {_normal_term(row["proposed_name"]) for row in extensions}
    ) != len(extensions):
        _fail("taxonomy_extension_duplicate", "extension replay contains duplicates")
    rebuilt = _seal(
        {
            "schema_version": "1.0.0",
            "artifact_kind": "post_freeze_taxonomy_classification",
            "classification_id": stable_identifier(
                "invention-classification", freeze["content_digest"], ordered
            ),
            "freeze_id": freeze["freeze_id"],
            "freeze_digest": freeze["content_digest"],
            "known_taxonomy_commitment_digest": known_taxonomy_commitment(known_taxonomy),
            "known_corner_ids": sorted(known_ids),
            "classifier_authority_digest": artifact["classifier_authority_digest"],
            "phase_order": ["pre_taxonomy_frozen", "post_freeze_classified"],
            "decisions": ordered,
            "authority_nulls": {
                "classification_truth_authority": "unavailable",
                "taxonomy_exhaustiveness_authority": "unavailable",
                "creativity_authority": "unavailable",
            },
        },
        "content_digest",
    )
    if dict(artifact) != rebuilt:
        _fail("classification_replay_mismatch", "classification is not deterministic")


def _validate_semantic_core(raw: Mapping[str, Any], context: str) -> dict[str, Any]:
    _exact_fields(raw, _SEMANTIC_CORE_FIELDS, f"{context} semantic core")
    for field in ("primitives", "mechanism_steps", "protected_differences", "boundary_regimes"):
        _text_list(raw[field], f"{context} semantic core {field}")
    relations = raw["relations"]
    if not isinstance(relations, list) or not relations:
        _fail("semantic_core_invalid", f"{context} requires typed relations")
    for relation in relations:
        if not isinstance(relation, Mapping):
            _fail("semantic_core_invalid", f"{context} relation must be an object")
        _exact_fields(relation, frozenset({"source", "polarity", "target"}), f"{context} relation")
        for field in ("source", "polarity", "target"):
            _text(relation[field], f"{context} relation {field}", minimum=2)
    for field in ("counterfactual_consequence", "falsifier", "correction_condition"):
        _text(raw[field], f"{context} semantic core {field}")
    return copy.deepcopy(dict(raw))


def _validate_deep_reflection(
    raw: Mapping[str, Any],
    *,
    semantic_core: Mapping[str, Any],
    physics_handback: Mapping[str, Any],
    context: str,
) -> dict[str, Any]:
    _exact_fields(raw, frozenset(DEEP_REFLECTION_LENSES), f"{context} deep reflection")
    semantic_relations = [copy.deepcopy(dict(row)) for row in semantic_core["relations"]]
    relation_names = {_relation_name(row): row for row in semantic_relations}
    correction_targets = {
        semantic_core["correction_condition"],
        semantic_core["falsifier"],
    }
    handback_targets = {
        value
        for field in (
            "physical_carrier",
            "regime_and_quantifiers",
            "proposed_next_decision",
            "decision_rationale",
            "correction_or_falsifier",
        )
        if isinstance((value := physics_handback[field]), str) and value.strip()
    }
    observed_mutations: set[tuple[str, str, str]] = set()
    for lens in DEEP_REFLECTION_LENSES:
        analysis = raw[lens]
        if not isinstance(analysis, Mapping):
            _fail("deep_reflection_incomplete", f"{context} {lens} reflection is absent")
        _exact_fields(analysis, _REFLECTION_FIELDS, f"{context} {lens} reflection")
        for field in (
            "named_relation",
            "exposed_assumption",
            "strongest_opposition",
            "conceptual_mutation",
            "consequence",
            "boundary_or_correction",
            "semantic_core_correction_link",
            "physics_handback_link",
        ):
            _text(analysis[field], f"{context} {lens} {field}", minimum=12)
        if analysis["named_relation"] not in relation_names:
            _fail(
                "deep_reflection_relation_unbound",
                f"{context} {lens} does not name an exact semantic-core relation",
            )
        before = analysis["relation_before"]
        if not isinstance(before, Mapping):
            _fail("deep_reflection_relation_unbound", f"{context} {lens} lacks relation_before")
        _exact_fields(before, frozenset({"source", "polarity", "target"}), f"{context} {lens} relation_before")
        if dict(before) != relation_names[analysis["named_relation"]]:
            _fail(
                "deep_reflection_relation_unbound",
                f"{context} {lens} relation_before differs from the named relation",
            )
        operation = analysis["relation_operation"]
        if operation not in _LENS_OPERATIONS[lens]:
            _fail(
                "deep_reflection_lens_mismatch",
                f"{context} {lens} uses an operation outside its conceptual lens",
            )
        if analysis["mutation_status"] not in {"changed", "challenged"}:
            _fail("deep_reflection_mutation_invalid", f"{context} {lens} has unknown mutation status")
        after = analysis["relation_after"]
        if analysis["mutation_status"] == "changed":
            if not isinstance(after, Mapping):
                _fail("deep_reflection_mutation_invalid", f"{context} {lens} lacks relation_after")
            _exact_fields(after, frozenset({"source", "polarity", "target"}), f"{context} {lens} relation_after")
            for field in ("source", "polarity", "target"):
                _text(after[field], f"{context} {lens} relation_after {field}", minimum=2)
            if _normal_semantic_value(after) == _normal_semantic_value(before):
                _fail(
                    "deep_reflection_mutation_invalid",
                    f"{context} {lens} claims a change but preserves the relation",
                )
            after_digest = canonical_digest(_normal_semantic_value(after))
        else:
            if after is not None:
                _fail(
                    "deep_reflection_mutation_invalid",
                    f"{context} {lens} challenge must not smuggle an undeclared replacement",
                )
            after_digest = "challenged"
        if analysis["semantic_core_correction_link"] not in correction_targets:
            _fail(
                "deep_reflection_correction_unbound",
                f"{context} {lens} is not linked to the semantic correction/falsifier",
            )
        if analysis["physics_handback_link"] not in handback_targets:
            _fail(
                "deep_reflection_handback_unbound",
                f"{context} {lens} is not linked to an exact physics handback field",
            )
        mutation_key = (analysis["named_relation"], operation, after_digest)
        if mutation_key in observed_mutations:
            _fail(
                "deep_reflection_duplicate_mutation",
                f"{context} repeats one mutation under multiple lens labels",
            )
        observed_mutations.add(mutation_key)
    return copy.deepcopy(dict(raw))


def _validate_risk_reward(raw: Mapping[str, Any], context: str) -> dict[str, Any]:
    expected = frozenset(
        {"risk_case", "high_upside_case", "learning_if_false", "cost_of_unification", "wildcard_reason"}
    )
    _exact_fields(raw, expected, f"{context} risk/reward")
    for field in expected - {"wildcard_reason"}:
        _text(raw[field], f"{context} risk/reward {field}")
    if raw["wildcard_reason"] is not None:
        _text(raw["wildcard_reason"], f"{context} wildcard reason")
    return copy.deepcopy(dict(raw))


def _validate_physics_handback(raw: Mapping[str, Any], context: str) -> dict[str, Any]:
    expected = frozenset(
        {
            "status",
            "physical_carrier",
            "regime_and_quantifiers",
            "decision_before",
            "proposed_next_decision",
            "decision_rationale",
            "untouched_physics_gates",
            "correction_or_falsifier",
        }
    )
    _exact_fields(raw, expected, f"{context} physics handback")
    if raw["status"] not in {"decision_changed", "quarantined_no_physics_delta"}:
        _fail("physics_handback_invalid", f"{context} has unknown handback status")
    _text_list(raw["untouched_physics_gates"], f"{context} untouched physics gates")
    _text(raw["decision_rationale"], f"{context} decision rationale")
    _text(raw["correction_or_falsifier"], f"{context} correction or falsifier")
    if raw["status"] == "decision_changed":
        for field in (
            "physical_carrier",
            "regime_and_quantifiers",
            "decision_before",
            "proposed_next_decision",
        ):
            _text(raw[field], f"{context} physics handback {field}")
        if _normal_term(raw["decision_before"]) == _normal_term(raw["proposed_next_decision"]):
            _fail("physics_handback_invalid", f"{context} claims an unchanged decision as changed")
    elif any(raw[field] is not None for field in ("proposed_next_decision", "physical_carrier")):
        _fail("physics_handback_invalid", f"{context} quarantine carries a promoted physics decision")
    return copy.deepcopy(dict(raw))


def _validate_matured(raw: Mapping[str, Any]) -> dict[str, Any]:
    _exact_fields(raw, _MATURED_FIELDS, "matured invention")
    validate_identifier(str(raw["invention_id"]), "invention_id")
    validate_identifier(str(raw["branch_id"]), "branch_id")
    if raw["exploration_role"] not in {"candidate", "wildcard"}:
        _fail("exploration_role_invalid", "matured invention role must be candidate or wildcard")
    _text(raw["statement"], f"matured {raw['invention_id']} statement")
    semantic_core = _validate_semantic_core(
        raw["semantic_core"], f"matured {raw['invention_id']}"
    )
    risk = _validate_risk_reward(raw["risk_reward"], f"matured {raw['invention_id']}")
    if raw["exploration_role"] == "wildcard" and risk["wildcard_reason"] is None:
        _fail("wildcard_unwarranted", "wildcard requires an explicit protection reason")
    physics_handback = _validate_physics_handback(
        raw["physics_handback"], f"matured {raw['invention_id']}"
    )
    _validate_deep_reflection(
        raw["deep_reflection"],
        semantic_core=semantic_core,
        physics_handback=physics_handback,
        context=f"matured {raw['invention_id']}",
    )
    return copy.deepcopy(dict(raw))


def _semantic_core_digest(matured: Mapping[str, Any]) -> str:
    return canonical_digest(_normal_semantic_value(matured["semantic_core"]))


def build_branch_intent_manifest(
    freeze: Mapping[str, Any],
    classification: Mapping[str, Any],
    *,
    invention_id: str,
    workspace_ref: str,
    maturation_question: str,
    isolation_requirement: Mapping[str, Any],
) -> dict[str, Any]:
    """Build a branch-local intent and manifest before isolated maturation."""

    validate_instance(freeze, FREEZE_SCHEMA)
    validate_instance(classification, CLASSIFICATION_SCHEMA)
    requirement = validate_isolation_requirement(isolation_requirement)
    raw_by_id = {row["invention_id"]: row for row in freeze["raw_inventions"]}
    if invention_id not in raw_by_id:
        _fail("branch_bijection_invalid", "branch refers to an unknown frozen invention")
    path = PurePosixPath(workspace_ref)
    if path.is_absolute() or ".." in path.parts or len(path.parts) < 2:
        _fail("branch_workspace_invalid", "branch workspace must be a contained relative path")
    own_digest = canonical_digest(raw_by_id[invention_id])
    sibling_digests = sorted(
        canonical_digest(row) for key, row in raw_by_id.items() if key != invention_id
    )
    allowed = sorted([freeze["content_digest"], classification["content_digest"], own_digest])
    branch_id = stable_identifier("open-world-branch", freeze["freeze_id"], invention_id)
    intent = _seal(
        {
            "intent_id": stable_identifier("branch-intent", branch_id, own_digest),
            "branch_id": branch_id,
            "invention_id": invention_id,
            "own_raw_invention_digest": own_digest,
            "maturation_question": _text(maturation_question, "maturation question"),
            "allowed_input_digests": allowed,
        },
        "intent_digest",
    )
    manifest = _seal(
        {
            "manifest_id": stable_identifier("branch-manifest", intent["intent_digest"], workspace_ref),
            "branch_id": branch_id,
            "intent_digest": intent["intent_digest"],
            "workspace_ref": str(path),
            "allowed_input_digests": allowed,
            "forbidden_sibling_invention_digests": sibling_digests,
            "isolation_requirement": requirement,
        },
        "manifest_digest",
    )
    return {"intent": intent, "manifest": manifest}


def bind_branch_terminal_receipt(
    intent_manifest: Mapping[str, Any],
    *,
    research_worker_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind one branch to an on-disk registered research-worker receipt.

    The receipt remains local integrity evidence, not cognitive independence.
    No caller-supplied status string is trusted: the registered receipt is reopened
    from its contained run-directory reference, fully replayed, and required to
    describe a successfully reaped process group before any branch record exists.
    """

    _exact_fields(intent_manifest, frozenset({"intent", "manifest"}), "intent manifest")
    intent = copy.deepcopy(dict(intent_manifest["intent"]))
    manifest = copy.deepcopy(dict(intent_manifest["manifest"]))
    _verify_seal(intent, "intent_digest", "branch intent")
    _verify_seal(manifest, "manifest_digest", "branch manifest")
    requirement = validate_isolation_requirement(manifest["isolation_requirement"])
    supplied_receipt = copy.deepcopy(dict(research_worker_receipt))
    try:
        run_directory = Path(str(supplied_receipt["workspace"]["run_directory"]))
        receipt_ref = str(supplied_receipt["receipt_ref"])
        receipt_path = contained_path(run_directory, *Path(receipt_ref).parts)
        disk_receipt = _load_json_object(receipt_path)
        registered = validate_research_worker_receipt(
            disk_receipt,
            receipt_path=receipt_path,
            required_kernel_isolation=bool(requirement["kernel_isolation_required"]),
        )
        summary = receipt_summary(registered, receipt_path=receipt_path)
    except (BenchmarkIntegrityError, ResearchWorkerIntegrityError, ContractError, OSError, KeyError) as exc:
        _fail("terminal_receipt_binding_mismatch", f"registered worker receipt failed replay: {exc}")
    if registered != supplied_receipt:
        _fail(
            "terminal_receipt_binding_mismatch",
            "caller receipt mapping differs from the immutable registered receipt",
        )
    event = registered["process_event"]
    if (
        registered["role"] != "high_risk"
        or registered["operation"] != "parallel_maturation"
        or registered["process_status"] != "succeeded"
        or registered["protocol_status"] != "accepted"
        or registered["outcome_status"] != "accepted"
        or event["event"] != "process_terminal"
        or event["status"] != "succeeded"
        or event["returncode"] != 0
        or event["descendant_leak_detected"] is not False
        or event["termination"] is not None
    ):
        _fail(
            "terminal_receipt_invalid",
            "branch requires one accepted, normally exited, descendant-free terminal process receipt",
        )

    request = {"intent": intent, "manifest": manifest}
    registered_request = registered["request_payload"]
    expected_context = {
        "branch_id": intent["branch_id"],
        "invention_id": intent["invention_id"],
        "intent_digest": intent["intent_digest"],
        "manifest_digest": manifest["manifest_digest"],
    }
    payload = registered_request["payload"]
    expected_payload_fields = {
        "branch_request",
        "matured_response",
        "minimum_residency_seconds",
        "adversarial_probe",
    }
    if (
        registered_request["invocation_context"] != expected_context
        or set(payload) != expected_payload_fields
        or payload["branch_request"] != request
        or payload["adversarial_probe"] is not None
        or registered_request["isolation_requirement"] != requirement
        or registered_request["fault_mode"] is not None
    ):
        _fail(
            "worker_payload_binding_mismatch",
            "registered worker request is not the exact non-probe branch request",
        )
    residency = payload["minimum_residency_seconds"]
    if (
        not isinstance(residency, (int, float))
        or isinstance(residency, bool)
        or not 0.02 <= float(residency) <= 1.0
    ):
        _fail("worker_payload_binding_mismatch", "branch concurrency residency is invalid")
    response = _validate_matured(payload["matured_response"])
    if (
        response["invention_id"] != intent["invention_id"]
        or response["branch_id"] != intent["branch_id"]
    ):
        _fail("worker_response_binding_mismatch", "worker response belongs to another branch")
    registered_response = registered["response_payload"]
    expected_output = {
        "output_kind": "parallel_maturation",
        "branch_request_digest": canonical_digest(request),
        "matured_response": response,
        "matured_response_digest": canonical_digest(response),
        "access_observation": _NO_ACCESS_OBSERVATION,
        "authority_boundary": _OPEN_WORLD_WORKER_AUTHORITY_BOUNDARY,
    }
    if registered_response["output"] != expected_output:
        _fail(
            "worker_response_binding_mismatch",
            "registered worker output differs from the exact branch response",
        )

    evidence_root = f"evidence/high_risk/{registered['invocation_id']}"
    request_ref = f"{evidence_root}/request.json"
    response_ref = f"{evidence_root}/response.json"
    request_path = contained_path(run_directory, *Path(request_ref).parts)
    response_path = contained_path(run_directory, *Path(response_ref).parts)
    try:
        _write_immutable_json(request_path, registered_request)
        _write_immutable_json(response_path, registered_response)
    except (BenchmarkIntegrityError, OSError) as exc:
        _fail("worker_payload_binding_mismatch", f"immutable branch evidence conflict: {exc}")
    request_file_bytes = canonical_json(registered_request) + b"\n"
    response_file_bytes = canonical_json(registered_response) + b"\n"
    if (
        request_path.is_symlink()
        or response_path.is_symlink()
        or request_path.read_bytes() != request_file_bytes
        or response_path.read_bytes() != response_file_bytes
    ):
        _fail("worker_payload_binding_mismatch", "branch evidence files changed after publication")

    branch_request_bytes = canonical_json(request) + b"\n"
    matured_response_bytes = canonical_json(response) + b"\n"
    isolation = registered["isolation_assurance"]
    channels = isolation["channels"]
    sibling_read_policy = (
        "kernel_run_sibling_read_denied"
        if channels["filesystem_read"]
        == "kernel_sibling_run_data_denied_host_read_scope_unrestricted"
        else "not_kernel_denied"
    )
    sibling_write_policy = (
        "kernel_run_sibling_write_denied"
        if channels["filesystem_write"] == "kernel_workspace_only"
        else "protocol_only_not_kernel_denied"
    )
    terminal_receipt = {
        "worker_receipt_id": registered["receipt_id"],
        "worker_receipt_ref": registered["receipt_ref"],
        "worker_receipt_digest": registered["content_digest"],
        "worker_receipt_file_sha256": summary["receipt_file_sha256"],
        "worker_receipt_byte_length": summary["receipt_byte_length"],
        "run_directory": str(run_directory),
        "registered_workspace_ref": registered["workspace"]["workspace_ref"],
        "role": registered["role"],
        "operation": registered["operation"],
        "process_status": registered["process_status"],
        "protocol_status": registered["protocol_status"],
        "outcome_status": registered["outcome_status"],
        "process_started_at": event["started_at"],
        "process_completed_at": event["completed_at"],
        "process_group_status": "terminal_no_descendants",
        "isolation_status": isolation["status"],
        "isolation_backend": isolation["mechanism"]["backend"],
        "network_policy_status": (
            "kernel_denied"
            if channels["network"] == "kernel_denied"
            else "not_kernel_denied"
        ),
        "workspace_policy_status": (
            "kernel_write_confined"
            if channels["filesystem_write"] == "kernel_workspace_only"
            else "protocol_only_not_kernel_confined"
        ),
        "sibling_read_policy_status": sibling_read_policy,
        "sibling_write_policy_status": sibling_write_policy,
        "request_evidence": {
            "ref": request_ref,
            "sha256": bytes_digest(request_file_bytes),
            "byte_length": len(request_file_bytes),
        },
        "response_evidence": {
            "ref": response_ref,
            "sha256": bytes_digest(response_file_bytes),
            "byte_length": len(response_file_bytes),
        },
        "request_sha256": registered["request_sha256"],
        "request_byte_length": registered["request_byte_length"],
        "response_sha256": registered["response_sha256"],
        "response_byte_length": registered["response_byte_length"],
        "branch_request_sha256": bytes_digest(branch_request_bytes),
        "branch_request_byte_length": len(branch_request_bytes),
        "matured_response_sha256": bytes_digest(matured_response_bytes),
        "matured_response_byte_length": len(matured_response_bytes),
        "branch_intent_digest": intent["intent_digest"],
        "branch_manifest_digest": manifest["manifest_digest"],
    }
    return _seal(
        {
            "branch_id": intent["branch_id"],
            "invention_id": intent["invention_id"],
            "intent": intent,
            "manifest": manifest,
            "worker_request": request,
            "worker_response": response,
            "terminal_receipt": terminal_receipt,
            "execution_authority_scope": (
                "registered_subprocess_exact_byte_and_namespace_integrity_only"
            ),
        },
        "record_digest",
    )


def _registered_receipt_from_terminal(terminal: Mapping[str, Any]) -> dict[str, Any]:
    """Resolve the immutable registered receipt named by a branch projection."""

    try:
        run_directory = Path(str(terminal["run_directory"]))
        receipt_path = contained_path(
            run_directory, *Path(str(terminal["worker_receipt_ref"])).parts
        )
        return _load_json_object(receipt_path)
    except (BenchmarkIntegrityError, OSError, KeyError) as exc:
        _fail("terminal_receipt_binding_mismatch", f"registered receipt is unavailable: {exc}")


def run_isolated_parallel_maturation_branches(
    freeze: Mapping[str, Any],
    classification: Mapping[str, Any],
    *,
    known_taxonomy: Mapping[str, Any],
    matured_inventions: Sequence[Mapping[str, Any]],
    maturation_questions: Mapping[str, str],
    run_root: Path | str,
    require_kernel_isolation: bool = False,
    max_workers: int = 3,
    minimum_residency_seconds: float = 0.08,
    budget: Mapping[str, Any] | None = None,
    fault_plan: Mapping[str, str] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Run all maturation branches concurrently and close a receipt barrier.

    The subprocess is an operational isolation/replay boundary around supplied
    theory material, not an author or an independent evaluator.  Every future is
    joined before branch evidence is bound and before the terminal barrier can be
    constructed.
    """

    validate_post_freeze_taxonomy_classification(
        classification, freeze=freeze, known_taxonomy=known_taxonomy
    )
    matured = [_validate_matured(row) for row in matured_inventions]
    raw_ids = {row["invention_id"] for row in freeze["raw_inventions"]}
    if len(matured) != len(raw_ids) or {row["invention_id"] for row in matured} != raw_ids:
        _fail("maturation_bijection_invalid", "every frozen invention must have one worker proposal")
    if set(maturation_questions) != raw_ids:
        _fail("branch_bijection_invalid", "maturation questions must cover every invention exactly")
    questions = {
        invention_id: _text(question, f"{invention_id} maturation question")
        for invention_id, question in maturation_questions.items()
    }
    if not isinstance(max_workers, int) or isinstance(max_workers, bool) or max_workers < 2:
        _fail("parallelism_invalid", "isolated maturation requires at least two workers")
    if (
        not isinstance(minimum_residency_seconds, (int, float))
        or isinstance(minimum_residency_seconds, bool)
        or not 0.02 <= float(minimum_residency_seconds) <= 1.0
    ):
        _fail("parallelism_invalid", "worker residency must remain in [0.02, 1.0] seconds")
    faults = dict(fault_plan or {})
    if set(faults) - raw_ids or any(
        value not in {"exit_nonzero", "invalid_json", "hang"} for value in faults.values()
    ):
        _fail("branch_fault_plan_invalid", "fault plan names an unknown branch or mode")

    backend = strongest_available_isolation()
    requirement = build_isolation_requirement(
        backend, require_kernel_isolation=require_kernel_isolation
    )
    intent_manifests: dict[str, dict[str, Any]] = {}
    response_by_id = {row["invention_id"]: row for row in matured}
    for invention_id in sorted(raw_ids):
        branch_id = stable_identifier("open-world-branch", freeze["freeze_id"], invention_id)
        intent_manifests[invention_id] = build_branch_intent_manifest(
            freeze,
            classification,
            invention_id=invention_id,
            workspace_ref=f"branches/{branch_id}",
            maturation_question=questions[invention_id],
            isolation_requirement=requirement,
        )
    study_id = stable_identifier(
        "open-world-maturation-study",
        freeze["content_digest"],
        classification["content_digest"],
        intent_manifests,
        matured,
        requirement,
    )
    worker_script = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "run_open_world_maturation_worker.py"
    )
    adapter = ResearchWorkerAdapter(
        study_id=study_id,
        run_root=run_root,
        worker_script=worker_script,
        require_kernel_isolation=require_kernel_isolation,
    )
    if build_isolation_requirement(
        adapter.backend, require_kernel_isolation=require_kernel_isolation
    ) != requirement:
        _fail("isolation_selection_changed", "worker backend changed after branch precommitment")

    def invoke(invention_id: str) -> dict[str, Any]:
        intent_manifest = intent_manifests[invention_id]
        intent = intent_manifest["intent"]
        manifest = intent_manifest["manifest"]
        return adapter.invoke(
            role="high_risk",
            operation="parallel_maturation",
            invocation_context={
                "branch_id": intent["branch_id"],
                "invention_id": invention_id,
                "intent_digest": intent["intent_digest"],
                "manifest_digest": manifest["manifest_digest"],
            },
            payload={
                "branch_request": intent_manifest,
                "matured_response": response_by_id[invention_id],
                "minimum_residency_seconds": float(minimum_residency_seconds),
                "adversarial_probe": None,
            },
            budget=budget,
            fault_mode=faults.get(invention_id),
        )

    registered_receipts: dict[str, dict[str, Any]] = {}
    worker_count = min(max_workers, len(raw_ids))
    with ThreadPoolExecutor(max_workers=worker_count) as pool:
        futures = {
            pool.submit(invoke, invention_id): invention_id
            for invention_id in sorted(raw_ids)
        }
        for future in as_completed(futures):
            invention_id = futures[future]
            registered_receipts[invention_id] = future.result()
    failures = [
        invention_id
        for invention_id, receipt in sorted(registered_receipts.items())
        if receipt["outcome_status"] != "accepted"
    ]
    if failures:
        _fail(
            "branch_execution_failed",
            "all worker processes terminated but no barrier is authorized; failed branches="
            + ",".join(failures),
        )
    records = [
        bind_branch_terminal_receipt(
            intent_manifests[invention_id],
            research_worker_receipt=registered_receipts[invention_id],
        )
        for invention_id in sorted(raw_ids)
    ]
    barrier = build_parallel_maturation_barrier_receipt(
        freeze,
        classification,
        known_taxonomy=known_taxonomy,
        branch_execution_records=records,
    )
    return records, barrier


def _validate_branch_record(
    record: Mapping[str, Any], freeze: Mapping[str, Any], classification: Mapping[str, Any]
) -> None:
    _exact_fields(
        record,
        frozenset(
            {
                "branch_id",
                "invention_id",
                "intent",
                "manifest",
                "worker_request",
                "worker_response",
                "terminal_receipt",
                "execution_authority_scope",
                "record_digest",
            }
        ),
        "branch execution record",
    )
    _verify_seal(record, "record_digest", "branch execution record")
    rebuilt = build_branch_intent_manifest(
        freeze,
        classification,
        invention_id=str(record["invention_id"]),
        workspace_ref=str(record["manifest"]["workspace_ref"]),
        maturation_question=str(record["intent"]["maturation_question"]),
        isolation_requirement=record["manifest"]["isolation_requirement"],
    )
    if record["intent"] != rebuilt["intent"] or record["manifest"] != rebuilt["manifest"]:
        _fail("branch_cross_read", "branch manifest contains non-own or sibling inputs")
    if record["worker_request"] != rebuilt:
        _fail("worker_payload_binding_mismatch", "stored worker request differs from intent/manifest")
    rebound = bind_branch_terminal_receipt(
        rebuilt,
        research_worker_receipt=_registered_receipt_from_terminal(
            record["terminal_receipt"]
        ),
    )
    if dict(record) != rebound:
        _fail("terminal_receipt_binding_mismatch", "branch terminal record cannot be replayed")


def _expected_parallel_barrier(
    *,
    freeze_digest: str,
    classification_digest: str,
    branch_execution_records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    intervals: list[tuple[dt.datetime, int]] = []
    for row in branch_execution_records:
        terminal = row["terminal_receipt"]
        try:
            started = dt.datetime.fromisoformat(terminal["process_started_at"])
            completed = dt.datetime.fromisoformat(terminal["process_completed_at"])
        except (TypeError, ValueError) as exc:
            _fail("barrier_nonterminal", f"worker interval is invalid: {exc}")
        if started.tzinfo is None or completed.tzinfo is None or completed < started:
            _fail("barrier_nonterminal", "worker interval is not ordered and timezone-explicit")
        if terminal["process_group_status"] != "terminal_no_descendants":
            _fail("barrier_nonterminal", "worker process group is not terminal")
        intervals.extend([(started, 1), (completed, -1)])
    active = 0
    peak_parallelism = 0
    for _timestamp, delta in sorted(intervals, key=lambda item: (item[0], item[1])):
        active += delta
        peak_parallelism = max(peak_parallelism, active)
    if peak_parallelism < 2:
        _fail("barrier_not_parallel", "fewer than two registered workers overlapped")
    members = [
        {
            "branch_id": row["branch_id"],
            "invention_id": row["invention_id"],
            "record_digest": row["record_digest"],
            "worker_receipt_digest": row["terminal_receipt"]["worker_receipt_digest"],
            "worker_receipt_file_sha256": row["terminal_receipt"][
                "worker_receipt_file_sha256"
            ],
            "registered_response_sha256": row["terminal_receipt"]["response_sha256"],
            "matured_response_sha256": row["terminal_receipt"][
                "matured_response_sha256"
            ],
            "process_completed_at": row["terminal_receipt"]["process_completed_at"],
        }
        for row in sorted(branch_execution_records, key=lambda item: item["branch_id"])
    ]
    payload = {
        "schema_version": "1.0.0",
        "artifact_kind": "parallel_maturation_terminal_barrier",
        "barrier_id": stable_identifier(
            "parallel-maturation-barrier", freeze_digest, classification_digest, members
        ),
        "freeze_digest": freeze_digest,
        "classification_digest": classification_digest,
        "status": "all_terminal_before_merge",
        "scheduled_branch_count": len(members),
        "terminal_branch_count": len(members),
        "observed_peak_parallelism": peak_parallelism,
        "lifecycle_verification": "all_registered_process_groups_terminal_no_descendants",
        "terminal_members": members,
        "merge_authority": "local_terminal_receipt_integrity_only",
    }
    payload_bytes = canonical_json(payload) + b"\n"
    return {
        **payload,
        "barrier_receipt_digest": bytes_digest(payload_bytes),
        "barrier_receipt_file_sha256": bytes_digest(payload_bytes),
        "barrier_receipt_byte_length": len(payload_bytes),
    }


def build_parallel_maturation_barrier_receipt(
    freeze: Mapping[str, Any],
    classification: Mapping[str, Any],
    *,
    known_taxonomy: Mapping[str, Any],
    branch_execution_records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Seal one terminal barrier only after every isolated branch is accepted."""

    validate_post_freeze_taxonomy_classification(
        classification, freeze=freeze, known_taxonomy=known_taxonomy
    )
    records = [copy.deepcopy(dict(row)) for row in branch_execution_records]
    expected_ids = {row["invention_id"] for row in freeze["raw_inventions"]}
    if (
        len(records) != len(expected_ids)
        or {row.get("invention_id") for row in records} != expected_ids
        or len({row.get("branch_id") for row in records}) != len(records)
    ):
        _fail("barrier_incomplete", "terminal barrier requires every distinct frozen branch")
    for record in records:
        _validate_branch_record(record, freeze, classification)
    return _expected_parallel_barrier(
        freeze_digest=freeze["content_digest"],
        classification_digest=classification["content_digest"],
        branch_execution_records=records,
    )


def _pairwise_nonredundancy(matured: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for left, right in itertools.combinations(sorted(matured, key=lambda row: row["invention_id"]), 2):
        left_core = _normal_semantic_value(left["semantic_core"])
        right_core = _normal_semantic_value(right["semantic_core"])
        differing = [
            field
            for field in sorted(_SEMANTIC_CORE_FIELDS)
            if canonical_digest(left_core[field]) != canonical_digest(right_core[field])
        ]
        if not differing:
            _fail(
                "matured_semantic_duplicate",
                f"{left['invention_id']} and {right['invention_id']} differ only in presentation",
            )
        mechanism_fields = {
            "relations",
            "mechanism_steps",
            "counterfactual_consequence",
            "falsifier",
            "correction_condition",
        }
        if len(differing) < 2 or not mechanism_fields.intersection(differing):
            _fail(
                "matured_semantic_subsumption",
                f"{left['invention_id']} and {right['invention_id']} differ only trivially",
            )
        left_tokens = _semantic_tokens(left_core)
        right_tokens = _semantic_tokens(right_core)
        token_jaccard, token_containment = _set_overlap(left_tokens, right_tokens)
        left_relations = {
            tuple(sorted(_semantic_tokens(relation))) for relation in left["semantic_core"]["relations"]
        }
        right_relations = {
            tuple(sorted(_semantic_tokens(relation))) for relation in right["semantic_core"]["relations"]
        }
        relation_overlap = bool(left_relations & right_relations) or left_relations == right_relations
        if relation_overlap and token_containment >= 0.9 and token_jaccard >= 0.72:
            _fail(
                "matured_semantic_subsumption",
                f"{left['invention_id']} and {right['invention_id']} are paraphrase/subsumption variants",
            )
        rows.append(
            {
                "left_invention_id": left["invention_id"],
                "right_invention_id": right["invention_id"],
                "left_semantic_core_digest": canonical_digest(left_core),
                "right_semantic_core_digest": canonical_digest(right_core),
                "differing_semantic_components": differing,
                "status": "content_nonredundant",
            }
        )
    return rows


def build_open_world_maturation_portfolio(
    freeze: Mapping[str, Any],
    classification: Mapping[str, Any],
    *,
    known_taxonomy: Mapping[str, Any],
    matured_inventions: Sequence[Mapping[str, Any]],
    branch_execution_records: Sequence[Mapping[str, Any]],
    parallel_barrier_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind matured semantic content to frozen inventions and isolated receipts."""

    validate_post_freeze_taxonomy_classification(
        classification, freeze=freeze, known_taxonomy=known_taxonomy
    )
    matured = [_validate_matured(row) for row in matured_inventions]
    raw_ids = {row["invention_id"] for row in freeze["raw_inventions"]}
    if {row["invention_id"] for row in matured} != raw_ids or len(matured) != len(raw_ids):
        _fail("maturation_bijection_invalid", "every frozen invention must mature exactly once")
    records = [copy.deepcopy(dict(row)) for row in branch_execution_records]
    for record in records:
        _validate_branch_record(record, freeze, classification)
    if {row["invention_id"] for row in records} != raw_ids or len(records) != len(raw_ids):
        _fail("branch_bijection_invalid", "every invention requires one terminal branch record")
    record_by_invention = {row["invention_id"]: row for row in records}
    if any(row["branch_id"] != record_by_invention[row["invention_id"]]["branch_id"] for row in matured):
        _fail("branch_bijection_invalid", "matured content is bound to the wrong branch")
    for row in matured:
        if row != record_by_invention[row["invention_id"]]["worker_response"]:
            _fail(
                "worker_response_binding_mismatch",
                "matured concept differs from the exact isolated worker response",
            )
    workspaces = [
        row["terminal_receipt"]["registered_workspace_ref"] for row in records
    ]
    if len(workspaces) != len(set(workspaces)):
        _fail("branch_workspace_invalid", "branches must use distinct workspace namespaces")
    matured.sort(key=lambda row: row["invention_id"])
    records.sort(key=lambda row: row["invention_id"])
    expected_barrier = _expected_parallel_barrier(
        freeze_digest=freeze["content_digest"],
        classification_digest=classification["content_digest"],
        branch_execution_records=records,
    )
    if dict(parallel_barrier_receipt) != expected_barrier:
        _fail("barrier_binding_mismatch", "portfolio barrier does not cover exact terminal records")
    enriched = [
        {
            **row,
            "semantic_core_digest": _semantic_core_digest(row),
            "content_digest": canonical_digest(row),
            "worker_response_sha256": record_by_invention[row["invention_id"]]["terminal_receipt"][
                "matured_response_sha256"
            ],
            "branch_record_digest": record_by_invention[row["invention_id"]]["record_digest"],
            "barrier_receipt_digest": expected_barrier["barrier_receipt_digest"],
        }
        for row in matured
    ]
    nonredundancy = _pairwise_nonredundancy(matured)
    core = {
        "schema_version": "1.0.0",
        "artifact_kind": "open_world_maturation_portfolio",
        "portfolio_id": stable_identifier(
            "open-world-portfolio", freeze["content_digest"], classification["content_digest"], enriched
        ),
        "target_id": freeze["namespace"]["target_id"],
        "freeze_id": freeze["freeze_id"],
        "freeze_digest": freeze["content_digest"],
        "classification_id": classification["classification_id"],
        "classification_digest": classification["content_digest"],
        "phase_order": [
            "pre_taxonomy_frozen",
            "post_freeze_classified",
            "isolated_parallel_maturation",
            "content_nonredundancy_checked",
            "deep_reflection_completed",
            "terminal_barrier_closed",
        ],
        "matured_inventions": enriched,
        "pairwise_nonredundancy": nonredundancy,
        "branch_execution_records": records,
        "parallel_barrier_receipt": expected_barrier,
        "branch_separation": {
            "status": "terminal_barrier_and_namespace_separation_validated",
            "authority_scope": "sealed_declared_channels_and_exact_byte_bindings_only",
            "workspace_refs": sorted(workspaces),
        },
        "authority_nulls": {
            "hidden_input_independence": "unavailable",
            "cognitive_independence": "unavailable",
            "semantic_independence": "unavailable",
            "external_creativity_authority": "unavailable",
            "truth_authority": "unavailable",
            "physics_value_authority": "unavailable",
        },
    }
    artifact = _seal(core, "content_digest")
    validate_open_world_maturation_portfolio(
        artifact,
        freeze=freeze,
        classification=classification,
        known_taxonomy=known_taxonomy,
    )
    return artifact


def _validate_branch_record_internal(record: Mapping[str, Any]) -> None:
    _exact_fields(
        record,
        frozenset(
            {
                "branch_id",
                "invention_id",
                "intent",
                "manifest",
                "worker_request",
                "worker_response",
                "terminal_receipt",
                "execution_authority_scope",
                "record_digest",
            }
        ),
        "branch execution record",
    )
    _verify_seal(record, "record_digest", "branch execution record")
    request = {"intent": record["intent"], "manifest": record["manifest"]}
    if record["worker_request"] != request:
        _fail("worker_payload_binding_mismatch", "branch worker request is not exact")
    rebound = bind_branch_terminal_receipt(
        {"intent": record["intent"], "manifest": record["manifest"]},
        research_worker_receipt=_registered_receipt_from_terminal(
            record["terminal_receipt"]
        ),
    )
    if dict(record) != rebound:
        _fail("terminal_receipt_binding_mismatch", "branch byte binding cannot be replayed")


def _validate_portfolio_internal_integrity(artifact: Mapping[str, Any]) -> None:
    validate_instance(artifact, PORTFOLIO_SCHEMA)
    _verify_seal(artifact, "content_digest", "open-world maturation portfolio")
    records = [copy.deepcopy(dict(row)) for row in artifact["branch_execution_records"]]
    if len(records) < 3:
        _fail("branch_bijection_invalid", "portfolio requires at least three terminal branches")
    for record in records:
        _validate_branch_record_internal(record)
    record_by_invention = {row["invention_id"]: row for row in records}
    if len(record_by_invention) != len(records) or len({row["branch_id"] for row in records}) != len(records):
        _fail("branch_bijection_invalid", "branch/invention identities are not bijective")
    own_digests = {row["intent"]["own_raw_invention_digest"] for row in records}
    if len(own_digests) != len(records):
        _fail("branch_cross_read", "raw invention commitments are not branch-distinct")
    for record in records:
        own = record["intent"]["own_raw_invention_digest"]
        expected_allowed = sorted(
            [artifact["freeze_digest"], artifact["classification_digest"], own]
        )
        expected_forbidden = sorted(own_digests - {own})
        if (
            record["intent"]["allowed_input_digests"] != expected_allowed
            or record["manifest"]["allowed_input_digests"] != expected_allowed
            or record["manifest"]["forbidden_sibling_invention_digests"]
            != expected_forbidden
        ):
            _fail("branch_cross_read", "branch allowed/forbidden inputs do not replay")
    expected_barrier = _expected_parallel_barrier(
        freeze_digest=artifact["freeze_digest"],
        classification_digest=artifact["classification_digest"],
        branch_execution_records=records,
    )
    if artifact["parallel_barrier_receipt"] != expected_barrier:
        _fail("barrier_binding_mismatch", "terminal barrier does not replay")

    matured_inputs: list[dict[str, Any]] = []
    expected_enriched_fields = set(_MATURED_FIELDS) | {
        "semantic_core_digest",
        "content_digest",
        "worker_response_sha256",
        "branch_record_digest",
        "barrier_receipt_digest",
    }
    for row in artifact["matured_inventions"]:
        if set(row) != expected_enriched_fields:
            _fail("closed_contract_violation", "matured artifact row is not closed")
        base = {key: copy.deepcopy(value) for key, value in row.items() if key in _MATURED_FIELDS}
        _validate_matured(base)
        record = record_by_invention.get(base["invention_id"])
        if record is None or record["worker_response"] != base:
            _fail("worker_response_binding_mismatch", "matured concept lacks its exact worker response")
        if (
            row["semantic_core_digest"] != _semantic_core_digest(base)
            or row["content_digest"] != canonical_digest(base)
            or row["worker_response_sha256"]
            != record["terminal_receipt"]["matured_response_sha256"]
            or row["branch_record_digest"] != record["record_digest"]
            or row["barrier_receipt_digest"] != expected_barrier["barrier_receipt_digest"]
        ):
            _fail("digest_mismatch", "matured invention byte bindings differ")
        matured_inputs.append(base)
    if len(matured_inputs) != len(records) or {
        row["invention_id"] for row in matured_inputs
    } != set(record_by_invention):
        _fail("maturation_bijection_invalid", "matured inventions and branches are not bijective")
    if artifact["pairwise_nonredundancy"] != _pairwise_nonredundancy(matured_inputs):
        _fail("nonredundancy_replay_mismatch", "pairwise semantic distinctions cannot be replayed")
    workspaces = sorted(
        row["terminal_receipt"]["registered_workspace_ref"] for row in records
    )
    if len(workspaces) != len(set(workspaces)) or artifact["branch_separation"] != {
        "status": "terminal_barrier_and_namespace_separation_validated",
        "authority_scope": "sealed_declared_channels_and_exact_byte_bindings_only",
        "workspace_refs": workspaces,
    }:
        _fail("branch_workspace_invalid", "branch separation receipt does not replay")
    expected_nulls = {
        "hidden_input_independence": "unavailable",
        "cognitive_independence": "unavailable",
        "semantic_independence": "unavailable",
        "external_creativity_authority": "unavailable",
        "truth_authority": "unavailable",
        "physics_value_authority": "unavailable",
    }
    if artifact["authority_nulls"] != expected_nulls:
        _fail("external_authority_forgery", "portfolio overstates creativity/independence authority")


def validate_open_world_maturation_portfolio(
    artifact: Mapping[str, Any],
    *,
    freeze: Mapping[str, Any],
    classification: Mapping[str, Any],
    known_taxonomy: Mapping[str, Any],
) -> None:
    _validate_portfolio_internal_integrity(artifact)
    validate_post_freeze_taxonomy_classification(
        classification, freeze=freeze, known_taxonomy=known_taxonomy
    )
    if (
        artifact["freeze_digest"] != freeze["content_digest"]
        or artifact["classification_digest"] != classification["content_digest"]
    ):
        _fail("portfolio_source_mismatch", "portfolio does not bind freeze/classification")
    for record in artifact["branch_execution_records"]:
        _validate_branch_record(record, freeze, classification)


_HARD_INTEGRITY_CHECKS = (
    "portfolio_schema_closed",
    "portfolio_content_digest_replayed",
    "matured_worker_response_bytes_replayed",
    "worker_receipt_bytes_replayed",
    "terminal_barrier_bytes_replayed",
    "branch_namespace_and_sibling_inputs_replayed",
    "content_nonredundancy_replayed",
    "authority_nulls_replayed",
)


def _expected_hard_integrity_receipt(portfolio: Mapping[str, Any]) -> dict[str, Any]:
    _validate_portfolio_internal_integrity(portfolio)
    records = portfolio["branch_execution_records"]
    core = {
        "schema_version": "1.0.0",
        "artifact_kind": "open_world_hard_integrity_receipt",
        "receipt_id": stable_identifier("open-world-integrity", portfolio["content_digest"]),
        "portfolio_id": portfolio["portfolio_id"],
        "portfolio_digest": portfolio["content_digest"],
        "freeze_digest": portfolio["freeze_digest"],
        "classification_digest": portfolio["classification_digest"],
        "checked_branch_record_digests": sorted(row["record_digest"] for row in records),
        "checked_worker_request_sha256s": sorted(
            row["terminal_receipt"]["request_sha256"] for row in records
        ),
        "checked_worker_response_sha256s": sorted(
            row["terminal_receipt"]["response_sha256"] for row in records
        ),
        "barrier_receipt_digest": portfolio["parallel_barrier_receipt"][
            "barrier_receipt_digest"
        ],
        "checks": list(_HARD_INTEGRITY_CHECKS),
        "status": "passed",
        "integrity_authority": "local_exact_byte_replay_only",
        "authority_nulls": {
            "worker_cognitive_independence": "unavailable",
            "semantic_independence": "unavailable",
            "truth_authority": "unavailable",
            "physics_value_authority": "unavailable",
            "conceptual_merit_authority": "unavailable",
        },
    }
    return _seal(core, "content_digest")


def build_open_world_hard_integrity_receipt(
    portfolio: Mapping[str, Any],
    *,
    freeze: Mapping[str, Any],
    classification: Mapping[str, Any],
    known_taxonomy: Mapping[str, Any],
) -> dict[str, Any]:
    """Issue a merit-free receipt after exact portfolio and worker-byte replay."""

    validate_open_world_maturation_portfolio(
        portfolio,
        freeze=freeze,
        classification=classification,
        known_taxonomy=known_taxonomy,
    )
    receipt = _expected_hard_integrity_receipt(portfolio)
    validate_instance(receipt, INTEGRITY_SCHEMA)
    return receipt


def validate_open_world_hard_integrity_receipt(
    receipt: Mapping[str, Any], *, portfolio: Mapping[str, Any]
) -> None:
    validate_instance(receipt, INTEGRITY_SCHEMA)
    _verify_seal(receipt, "content_digest", "open-world hard-integrity receipt")
    if dict(receipt) != _expected_hard_integrity_receipt(portfolio):
        _fail("hard_integrity_replay_mismatch", "hard-integrity receipt cannot be replayed")


_BLIND_AUTHORITY_BOUNDARY = (
    "The blind packet supports internally correlated categorical pairwise and "
    "best-worst conceptual comparison only; it carries no truth, creativity, "
    "physics-value, external-merit, or evaluator-independence authority."
)


def _candidate_content(matured: Mapping[str, Any]) -> dict[str, Any]:
    return {key: copy.deepcopy(matured[key]) for key in sorted(_CONTENT_FIELDS)}


def _blind_candidate_content(content: Mapping[str, Any]) -> dict[str, Any]:
    """Remove role-bearing metadata while preserving assessable risk substance."""

    blind = copy.deepcopy(dict(content))
    risk = copy.deepcopy(dict(blind["risk_reward"]))
    risk.pop("wildcard_reason", None)
    blind["risk_reward"] = risk
    return blind


def _validate_control(
    raw: Mapping[str, Any],
    candidate_by_id: Mapping[str, Mapping[str, Any]],
    *,
    target_id: str,
) -> dict[str, Any]:
    _exact_fields(
        raw,
        frozenset(
            {"control_id", "control_kind", "source_invention_id", "target_id", "content"}
        ),
        "merit control",
    )
    validate_identifier(str(raw["control_id"]), "control_id")
    if raw["target_id"] != target_id:
        _fail("control_target_mismatch", "control is not bound to the same target task")
    if raw["control_kind"] not in CONTROL_KINDS:
        _fail("control_invalid", "unknown merit control kind")
    if set(raw["content"]) != set(_CONTENT_FIELDS):
        _fail("control_invalid", "control content does not match candidate content")
    synthetic = {
        "invention_id": f"control-{raw['control_kind']}",
        "branch_id": f"control-{raw['control_kind']}",
        "exploration_role": "candidate",
        **copy.deepcopy(dict(raw["content"])),
    }
    _validate_matured(synthetic)
    source_id = raw["source_invention_id"]
    if raw["control_kind"] == "capable":
        if source_id is not None:
            _fail("control_invalid", "capable control must be an independent baseline")
        if raw["content"]["physics_handback"]["status"] != "decision_changed":
            _fail("capable_control_invalid", "capable control must change a named task decision")
        for candidate in candidate_by_id.values():
            candidate_base = {
                key: copy.deepcopy(candidate[key]) for key in _MATURED_FIELDS
            }
            try:
                _pairwise_nonredundancy([candidate_base, synthetic])
            except OpenWorldCreativityError as exc:
                if exc.reason_code in {
                    "matured_semantic_duplicate",
                    "matured_semantic_subsumption",
                }:
                    _fail(
                        "capable_control_invalid",
                        "capable control is a candidate duplicate rather than an independent baseline",
                    )
                raise
    else:
        if source_id not in candidate_by_id:
            _fail("control_invalid", "sham/restatement control lacks a source candidate")
        source_content = _candidate_content(candidate_by_id[str(source_id)])
        source_core = canonical_digest(
            _normal_semantic_value(source_content["semantic_core"])
        )
        control_core = canonical_digest(
            _normal_semantic_value(raw["content"]["semantic_core"])
        )
        if raw["control_kind"] == "restatement":
            if control_core != source_core:
                _fail("restatement_control_invalid", "restatement changes semantic core")
            source_nonstatement = {
                key: value for key, value in source_content.items() if key != "statement"
            }
            control_nonstatement = {
                key: value for key, value in raw["content"].items() if key != "statement"
            }
            if _normal_semantic_value(source_nonstatement) != _normal_semantic_value(
                control_nonstatement
            ):
                _fail(
                    "restatement_control_invalid",
                    "restatement changes reflection, risk, correction, or physics content",
                )
            if _normal_term(source_content["statement"]) == _normal_term(
                raw["content"]["statement"]
            ):
                _fail("restatement_control_invalid", "restatement did not change presentation")
        else:
            if control_core == source_core:
                _fail("sham_control_invalid", "sham fails to corrupt semantic content")
            if raw["content"]["physics_handback"]["status"] != "quarantined_no_physics_delta":
                _fail(
                    "sham_control_invalid",
                    "sham must be quarantined rather than claim a task decision change",
                )
    return copy.deepcopy(dict(raw))


def _validate_control_set(
    controls: Sequence[Mapping[str, Any]],
    candidate_by_id: Mapping[str, Mapping[str, Any]],
    *,
    target_id: str,
) -> list[dict[str, Any]]:
    checked = [
        _validate_control(row, candidate_by_id, target_id=target_id) for row in controls
    ]
    kinds = [row["control_kind"] for row in checked]
    ids = [row["control_id"] for row in checked]
    if (
        len(checked) != len(CONTROL_KINDS)
        or set(kinds) != CONTROL_KINDS
        or len(ids) != len(set(ids))
        or set(ids).intersection(candidate_by_id)
    ):
        _fail(
            "control_incomplete",
            "exactly one disjoint capable, restatement, and sham control is required",
        )
    return sorted(checked, key=lambda row: row["control_id"])


def _merit_source_rows(
    portfolio: Mapping[str, Any], controls: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in portfolio["matured_inventions"]:
        content = _candidate_content(candidate)
        rows.append(
            {
                "source_kind": "invention",
                "source_id": candidate["invention_id"],
                "source_invention_id": None,
                "target_id": portfolio["target_id"],
                "exploration_role": candidate["exploration_role"],
                "control_kind": None,
                "content": content,
            }
        )
    for control in controls:
        rows.append(
            {
                "source_kind": "control",
                "source_id": control["control_id"],
                "source_invention_id": control["source_invention_id"],
                "target_id": control["target_id"],
                "exploration_role": None,
                "control_kind": control["control_kind"],
                "content": copy.deepcopy(control["content"]),
            }
        )
    return sorted(rows, key=lambda row: (row["source_kind"], row["source_id"]))


def _expected_blind_rows(
    source_rows: Sequence[Mapping[str, Any]], *, counterbalance_seed_digest: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    prepared: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for source in source_rows:
        blind_content = _blind_candidate_content(source["content"])
        source_digest = canonical_digest(source["content"])
        blind_digest = canonical_digest(blind_content)
        alias = stable_identifier(
            "merit-candidate",
            counterbalance_seed_digest,
            blind_digest,
            source["source_id"],
        )
        prepared.append(
            (
                {
                    "candidate_alias": alias,
                    "content": blind_content,
                    "content_digest": blind_digest,
                },
                {
                    "candidate_alias": alias,
                    "source_kind": source["source_kind"],
                    "source_id": source["source_id"],
                    "source_invention_id": source["source_invention_id"],
                    "target_id": source["target_id"],
                    "exploration_role": source["exploration_role"],
                    "control_kind": source["control_kind"],
                    "source_content_digest": source_digest,
                    "blind_content_digest": blind_digest,
                },
            )
        )
    prepared.sort(
        key=lambda pair: canonical_digest(
            [counterbalance_seed_digest, pair[0]["candidate_alias"]]
        )
    )
    return [row[0] for row in prepared], [row[1] for row in prepared]


def _blind_markers(source_rows: Sequence[Mapping[str, Any]]) -> list[str]:
    return sorted(
        {
            *(str(row["source_id"]) for row in source_rows),
            *(str(row["source_invention_id"]) for row in source_rows if row["source_invention_id"]),
            *CONTROL_KINDS,
            "wildcard",
        }
    )


def _assert_no_blind_markers(value: Any, markers: Sequence[str]) -> None:
    normalized_markers = {_normal_term(marker) for marker in markers if marker}
    forbidden_keys = {
        "control_kind",
        "exploration_role",
        "source_invention_id",
        "invention_id",
        "wildcard_reason",
    }
    for path, key, child in _recursive_items(value):
        if key and key in forbidden_keys:
            _fail("blind_packet_leak", f"treatment field leaked at {path}")
        if isinstance(child, str):
            normalized = f" {_normal_term(child)} "
            if any(marker and f" {marker} " in normalized for marker in normalized_markers):
                _fail("blind_packet_leak", f"identity or treatment marker leaked at {path}")


def prepare_blinded_conceptual_merit_packet(
    portfolio: Mapping[str, Any],
    *,
    controls: Sequence[Mapping[str, Any]],
    hard_integrity_receipt: Mapping[str, Any],
    counterbalance_nonce: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Prepare a content-only judge packet and separately sealed exact source map."""

    _validate_portfolio_internal_integrity(portfolio)
    validate_open_world_hard_integrity_receipt(
        hard_integrity_receipt, portfolio=portfolio
    )
    _text(counterbalance_nonce, "counterbalance nonce", minimum=3)
    candidates = [copy.deepcopy(dict(row)) for row in portfolio["matured_inventions"]]
    candidate_by_id = {row["invention_id"]: row for row in candidates}
    checked_controls = _validate_control_set(
        controls, candidate_by_id, target_id=portfolio["target_id"]
    )
    source_rows = _merit_source_rows(portfolio, checked_controls)
    seed = canonical_digest(
        {
            "portfolio_digest": portfolio["content_digest"],
            "hard_integrity_receipt_digest": hard_integrity_receipt["content_digest"],
            "counterbalance_nonce": counterbalance_nonce,
        }
    )
    blind_candidates, bindings = _expected_blind_rows(
        source_rows, counterbalance_seed_digest=seed
    )
    markers = _blind_markers(source_rows)
    _assert_no_blind_markers(blind_candidates, markers)
    packet = _seal(
        {
            "schema_version": "1.0.0",
            "packet_id": stable_identifier(
                "blind-merit-packet",
                portfolio["content_digest"],
                hard_integrity_receipt["content_digest"],
                seed,
            ),
            "target_id": portfolio["target_id"],
            "portfolio_digest": portfolio["content_digest"],
            "hard_integrity_receipt_digest": hard_integrity_receipt["content_digest"],
            "candidate_order": [
                row["candidate_alias"] for row in blind_candidates
            ],
            "candidates": blind_candidates,
            "dimensions": list(MERIT_DIMENSIONS),
            "counterbalance_seed_digest": seed,
            "blinding_audit": {
            "status": "identity_treatment_role_and_protected_flag_fields_removed",
                "marker_set_digest": canonical_digest(markers),
            },
            "integrity_screen": {
                "status": "passed_before_merit",
                "hard_integrity_receipt_digest": hard_integrity_receipt[
                    "content_digest"
                ],
                "candidate_aliases": sorted(
                    row["candidate_alias"] for row in blind_candidates
                ),
                "merit_authority": "none",
            },
            "authority_boundary": _BLIND_AUTHORITY_BOUNDARY,
        },
        "packet_digest",
    )
    private = _seal(
        {"packet_digest": packet["packet_digest"], "bindings": bindings},
        "binding_digest",
    )
    _validate_blind_source_replay(
        portfolio,
        controls=checked_controls,
        hard_integrity_receipt=hard_integrity_receipt,
        blind_packet=packet,
        private_binding=private,
    )
    return packet, private


def _validate_blind_source_replay(
    portfolio: Mapping[str, Any],
    *,
    controls: Sequence[Mapping[str, Any]],
    hard_integrity_receipt: Mapping[str, Any],
    blind_packet: Mapping[str, Any],
    private_binding: Mapping[str, Any],
) -> None:
    _validate_portfolio_internal_integrity(portfolio)
    validate_open_world_hard_integrity_receipt(
        hard_integrity_receipt, portfolio=portfolio
    )
    candidate_by_id = {
        row["invention_id"]: row for row in portfolio["matured_inventions"]
    }
    checked_controls = _validate_control_set(
        controls, candidate_by_id, target_id=portfolio["target_id"]
    )
    _exact_fields(
        blind_packet,
        frozenset(
            {
                "schema_version",
                "packet_id",
                "target_id",
                "portfolio_digest",
                "hard_integrity_receipt_digest",
                "candidate_order",
                "candidates",
                "dimensions",
                "counterbalance_seed_digest",
                "blinding_audit",
                "integrity_screen",
                "authority_boundary",
                "packet_digest",
            }
        ),
        "blind merit packet",
    )
    _verify_seal(blind_packet, "packet_digest", "blind merit packet")
    _exact_fields(
        private_binding,
        frozenset({"packet_digest", "bindings", "binding_digest"}),
        "private merit binding",
    )
    _verify_seal(private_binding, "binding_digest", "private merit binding")
    validate_digest(str(blind_packet["counterbalance_seed_digest"]))
    if (
        blind_packet["schema_version"] != "1.0.0"
        or blind_packet["target_id"] != portfolio["target_id"]
        or blind_packet["portfolio_digest"] != portfolio["content_digest"]
        or blind_packet["hard_integrity_receipt_digest"]
        != hard_integrity_receipt["content_digest"]
        or private_binding["packet_digest"] != blind_packet["packet_digest"]
        or blind_packet["dimensions"] != list(MERIT_DIMENSIONS)
        or blind_packet["authority_boundary"] != _BLIND_AUTHORITY_BOUNDARY
    ):
        _fail("blind_packet_binding_mismatch", "blind packet source binding differs")
    source_rows = _merit_source_rows(portfolio, checked_controls)
    expected_candidates, expected_bindings = _expected_blind_rows(
        source_rows,
        counterbalance_seed_digest=blind_packet["counterbalance_seed_digest"],
    )
    if (
        blind_packet["candidates"] != expected_candidates
        or blind_packet["candidate_order"]
        != [row["candidate_alias"] for row in expected_candidates]
        or private_binding["bindings"] != expected_bindings
    ):
        _fail(
            "blind_packet_binding_mismatch",
            "blind content, aliases, roles, or controls do not replay from sources",
        )
    markers = _blind_markers(source_rows)
    expected_audit = {
        "status": "identity_treatment_role_and_protected_flag_fields_removed",
        "marker_set_digest": canonical_digest(markers),
    }
    expected_screen = {
        "status": "passed_before_merit",
        "hard_integrity_receipt_digest": hard_integrity_receipt["content_digest"],
        "candidate_aliases": sorted(
            row["candidate_alias"] for row in expected_candidates
        ),
        "merit_authority": "none",
    }
    if (
        blind_packet["blinding_audit"] != expected_audit
        or blind_packet["integrity_screen"] != expected_screen
    ):
        _fail("blind_packet_binding_mismatch", "blind audit or integrity receipt differs")
    _assert_no_blind_markers(expected_candidates, markers)


def _json_pointer(value: Any, pointer: str) -> Any:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        _fail("merit_warrant_invalid", f"invalid JSON pointer {pointer!r}")
    current = value
    for raw in pointer.split("/")[1:]:
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, Mapping) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
            current = current[int(token)]
        else:
            _fail("merit_warrant_invalid", f"warrant path does not exist: {pointer}")
    return current


def _expected_merit_keys(aliases: Sequence[str]) -> set[tuple[str, str, str]]:
    return {
        (left, right, dimension)
        for left, right in itertools.combinations(sorted(aliases), 2)
        for dimension in MERIT_DIMENSIONS
    }


def seal_merit_evaluator_report(
    blind_packet: Mapping[str, Any],
    *,
    evaluator_id: str,
    evaluator_authority_digest: str,
    comparisons: Sequence[Mapping[str, Any]],
    best_worst_choices: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Seal one total pairwise and per-dimension best-worst blinded report."""

    validate_identifier(evaluator_id, "evaluator_id")
    validate_digest(evaluator_authority_digest)
    report = _seal(
        {
            "evaluator_id": evaluator_id,
            "evaluator_authority_digest": evaluator_authority_digest,
            "authority_status": "internally_correlated",
            "blind_packet_digest": blind_packet["packet_digest"],
            "comparisons": [copy.deepcopy(dict(row)) for row in comparisons],
            "best_worst_choices": [
                copy.deepcopy(dict(row)) for row in best_worst_choices
            ],
        },
        "report_digest",
    )
    _validate_merit_report(report, blind_packet)
    return report


def _pair_outcome_from_rows(
    comparison_by_key: Mapping[tuple[str, str, str], Mapping[str, Any]],
    first: str,
    second: str,
    dimension: str,
) -> str:
    left, right = sorted((first, second))
    verdict = comparison_by_key[(left, right, dimension)]["verdict"]
    if verdict in {"tie", "insufficient"}:
        return verdict
    winner = left if verdict == "left" else right
    return "first" if winner == first else "second"


def _validate_warrant_paths(
    paths: Any, *, content: Mapping[str, Any], context: str
) -> None:
    _text_list(paths, context)
    for path in paths:
        warranted = _json_pointer(content, path)
        if warranted is None or warranted == "" or warranted == [] or warranted == {}:
            _fail("merit_warrant_invalid", f"empty warrant at {path}")


def _validate_merit_report(
    report: Mapping[str, Any], blind_packet: Mapping[str, Any]
) -> None:
    _exact_fields(
        report,
        frozenset(
            {
                "evaluator_id",
                "evaluator_authority_digest",
                "authority_status",
                "blind_packet_digest",
                "comparisons",
                "best_worst_choices",
                "report_digest",
            }
        ),
        "merit evaluator report",
    )
    _verify_seal(report, "report_digest", "merit evaluator report")
    if report["authority_status"] != "internally_correlated":
        _fail("external_authority_forgery", "local merit report claimed external authority")
    if report["blind_packet_digest"] != blind_packet["packet_digest"]:
        _fail("blind_packet_binding_mismatch", "merit report binds a different blind packet")
    candidates = blind_packet["candidates"]
    candidate_by_alias = {row["candidate_alias"]: row for row in candidates}
    if len(candidate_by_alias) != len(candidates):
        _fail("blind_packet_binding_mismatch", "blind aliases are not unique")
    for candidate in candidates:
        if candidate["content_digest"] != canonical_digest(candidate["content"]):
            _fail("blind_packet_binding_mismatch", "blind candidate content digest differs")
    observed: set[tuple[str, str, str]] = set()
    comparison_by_key: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    for comparison in report["comparisons"]:
        expected_fields = frozenset(
            {
                "left_alias",
                "right_alias",
                "dimension",
                "verdict",
                "left_warrant_paths",
                "right_warrant_paths",
                "rationale",
                "strongest_objection",
                "correction_test",
            }
        )
        _exact_fields(comparison, expected_fields, "pairwise merit comparison")
        left = comparison["left_alias"]
        right = comparison["right_alias"]
        if left not in candidate_by_alias or right not in candidate_by_alias or left >= right:
            _fail("pairwise_coverage_invalid", "comparison aliases must be canonical and distinct")
        if comparison["dimension"] not in MERIT_DIMENSIONS:
            _fail("pairwise_coverage_invalid", "comparison has an unknown merit dimension")
        if comparison["verdict"] not in {"left", "right", "tie", "insufficient"}:
            _fail("pairwise_coverage_invalid", "comparison has an unknown verdict")
        for side in ("left", "right"):
            _validate_warrant_paths(
                comparison[f"{side}_warrant_paths"],
                content=candidate_by_alias[comparison[f"{side}_alias"]]["content"],
                context=f"{side} merit warrants",
            )
        for field in ("rationale", "strongest_objection", "correction_test"):
            _text(comparison[field], f"comparison {field}", minimum=12)
        key = (left, right, comparison["dimension"])
        if key in observed:
            _fail("pairwise_coverage_invalid", "duplicate pairwise merit comparison")
        observed.add(key)
        comparison_by_key[key] = comparison
    if observed != _expected_merit_keys(list(candidate_by_alias)):
        _fail("pairwise_coverage_invalid", "merit report is not pair/dimension total")

    seen_dimensions: set[str] = set()
    aliases = sorted(candidate_by_alias)
    for choice in report["best_worst_choices"]:
        _exact_fields(
            choice,
            frozenset(
                {
                    "dimension",
                    "best_alias",
                    "worst_alias",
                    "best_warrant_paths",
                    "worst_warrant_paths",
                    "rationale",
                    "strongest_objection",
                    "correction_test",
                }
            ),
            "best-worst merit choice",
        )
        dimension = choice["dimension"]
        best = choice["best_alias"]
        worst = choice["worst_alias"]
        if (
            dimension not in MERIT_DIMENSIONS
            or dimension in seen_dimensions
            or best not in candidate_by_alias
            or worst not in candidate_by_alias
            or best == worst
        ):
            _fail("best_worst_coverage_invalid", "best-worst choice is not dimension-total")
        _validate_warrant_paths(
            choice["best_warrant_paths"],
            content=candidate_by_alias[best]["content"],
            context="best merit warrants",
        )
        _validate_warrant_paths(
            choice["worst_warrant_paths"],
            content=candidate_by_alias[worst]["content"],
            context="worst merit warrants",
        )
        for field in ("rationale", "strongest_objection", "correction_test"):
            _text(choice[field], f"best-worst {field}", minimum=12)
        for other in aliases:
            if other == best:
                continue
            if (
                _pair_outcome_from_rows(
                    comparison_by_key, best, other, dimension
                )
                == "second"
            ):
                _fail(
                    "best_worst_pairwise_inconsistent",
                    "selected best loses a direct pairwise comparison",
                )
        for other in aliases:
            if other == worst:
                continue
            if (
                _pair_outcome_from_rows(
                    comparison_by_key, worst, other, dimension
                )
                == "first"
            ):
                _fail(
                    "best_worst_pairwise_inconsistent",
                    "selected worst wins a direct pairwise comparison",
                )
        seen_dimensions.add(dimension)
    if seen_dimensions != set(MERIT_DIMENSIONS):
        _fail("best_worst_coverage_invalid", "one best-worst choice is required per dimension")
    _assert_no_scalar_keys(report)


def _assert_no_scalar_keys(value: Any, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if _FORBIDDEN_MERIT_KEYS.search(str(key)):
                _fail(
                    "aggregate_scalar_forbidden",
                    f"scalar merit field is forbidden at {path}/{key}",
                )
            _assert_no_scalar_keys(child, f"{path}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_no_scalar_keys(child, f"{path}/{index}")


def _aggregate_reports(reports: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_key: dict[tuple[str, str, str], Counter[str]] = {}
    for report in reports:
        for row in report["comparisons"]:
            key = (row["left_alias"], row["right_alias"], row["dimension"])
            by_key.setdefault(key, Counter())[row["verdict"]] += 1
    consensus: list[dict[str, Any]] = []
    for (left, right, dimension), votes in sorted(by_key.items()):
        ordered = votes.most_common()
        verdict = (
            ordered[0][0]
            if len(ordered) == 1 or ordered[0][1] > ordered[1][1]
            else "insufficient"
        )
        consensus.append(
            {
                "left_alias": left,
                "right_alias": right,
                "dimension": dimension,
                "verdict": verdict,
                "verdict_counts": {
                    key: votes.get(key, 0)
                    for key in ("left", "right", "tie", "insufficient")
                },
            }
        )
    return consensus


def _plurality_alias(
    counts: Counter[str], *, evaluator_count: int
) -> tuple[str | None, str]:
    ordered = counts.most_common()
    if not ordered or (len(ordered) > 1 and ordered[0][1] == ordered[1][1]):
        return None, "unresolved_tie"
    status = "unanimous" if ordered[0][1] == evaluator_count else "plurality_with_dissent"
    return ordered[0][0], status


def _aggregate_best_worst(
    reports: Sequence[Mapping[str, Any]], aliases: Sequence[str]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    evaluator_count = len(reports)
    for dimension in MERIT_DIMENSIONS:
        best_counts: Counter[str] = Counter()
        worst_counts: Counter[str] = Counter()
        for report in reports:
            choice = next(
                row
                for row in report["best_worst_choices"]
                if row["dimension"] == dimension
            )
            best_counts[choice["best_alias"]] += 1
            worst_counts[choice["worst_alias"]] += 1
        best, best_status = _plurality_alias(
            best_counts, evaluator_count=evaluator_count
        )
        worst, worst_status = _plurality_alias(
            worst_counts, evaluator_count=evaluator_count
        )
        rows.append(
            {
                "dimension": dimension,
                "consensus_best_alias": best,
                "consensus_worst_alias": worst,
                "dissent_status": (
                    "unresolved_tie"
                    if "unresolved_tie" in {best_status, worst_status}
                    else (
                        "unanimous"
                        if best_status == worst_status == "unanimous"
                        else "plurality_with_dissent"
                    )
                ),
                "candidate_votes": [
                    {
                        "candidate_alias": alias,
                        "best_selections": best_counts.get(alias, 0),
                        "worst_selections": worst_counts.get(alias, 0),
                    }
                    for alias in sorted(aliases)
                ],
            }
        )
    return rows


def _pair_verdict(
    consensus_by_key: Mapping[tuple[str, str, str], str],
    first: str,
    second: str,
    dimension: str,
) -> str:
    left, right = sorted((first, second))
    verdict = consensus_by_key[(left, right, dimension)]
    if verdict in {"tie", "insufficient"}:
        return verdict
    winner = left if verdict == "left" else right
    return "first" if winner == first else "second"


def _discrimination_evidence(
    consensus: Sequence[Mapping[str, Any]],
    best_worst_consensus: Sequence[Mapping[str, Any]],
    invention_aliases: Sequence[str],
) -> list[dict[str, Any]]:
    invention_set = set(invention_aliases)
    pair_count = len(list(itertools.combinations(sorted(invention_set), 2)))
    required = max(1, (pair_count + 1) // 2)
    best_worst_by_dimension = {
        row["dimension"]: row for row in best_worst_consensus
    }
    evidence: list[dict[str, Any]] = []
    for dimension in MERIT_DIMENSIONS:
        decisive = sum(
            1
            for row in consensus
            if row["dimension"] == dimension
            and row["left_alias"] in invention_set
            and row["right_alias"] in invention_set
            and row["verdict"] in {"left", "right"}
        )
        best_worst = best_worst_by_dimension[dimension]
        resolved = (
            best_worst["consensus_best_alias"] is not None
            and best_worst["consensus_worst_alias"] is not None
            and best_worst["consensus_best_alias"]
            != best_worst["consensus_worst_alias"]
        )
        if decisive < required or not resolved:
            _fail(
                "merit_dimension_non_discriminating",
                f"{dimension} does not meet pairwise and best-worst discrimination floors",
            )
        evidence.append(
            {
                "dimension": dimension,
                "decisive_invention_pairs": decisive,
                "required_decisive_invention_pairs": required,
                "best_worst_consensus_resolved": "yes",
                "status": "passed",
            }
        )
    return evidence


def _strongly_connected_cycles(
    aliases: Sequence[str], edges: Mapping[str, set[str]]
) -> list[dict[str, Any]]:
    index = 0
    stack: list[str] = []
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    on_stack: set[str] = set()
    components: list[list[str]] = []

    def visit(alias: str) -> None:
        nonlocal index
        indices[alias] = index
        lowlinks[alias] = index
        index += 1
        stack.append(alias)
        on_stack.add(alias)
        for target in sorted(edges.get(alias, set())):
            if target not in indices:
                visit(target)
                lowlinks[alias] = min(lowlinks[alias], lowlinks[target])
            elif target in on_stack:
                lowlinks[alias] = min(lowlinks[alias], indices[target])
        if lowlinks[alias] == indices[alias]:
            component: list[str] = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == alias:
                    break
            if len(component) > 1:
                components.append(sorted(component))

    for alias in sorted(aliases):
        if alias not in indices:
            visit(alias)
    return [
        {
            "cycle_id": stable_identifier("merit-dominance-cycle", members),
            "member_aliases": members,
            "status": "dominance_cycle_incomparable",
        }
        for members in sorted(components)
    ]


def _derive_merit_outcomes(
    consensus: Sequence[Mapping[str, Any]],
    private_bindings: Sequence[Mapping[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    by_alias = {row["candidate_alias"]: row for row in private_bindings}
    consensus_by_key = {
        (row["left_alias"], row["right_alias"], row["dimension"]): row["verdict"]
        for row in consensus
    }
    profiles: list[dict[str, Any]] = []
    for alias, binding in sorted(by_alias.items()):
        dimension_outcomes: dict[str, dict[str, int]] = {}
        for dimension in MERIT_DIMENSIONS:
            counts = Counter()
            for other in by_alias:
                if other == alias:
                    continue
                outcome = _pair_verdict(
                    consensus_by_key, alias, other, dimension
                )
                counts[{"first": "win", "second": "loss"}.get(outcome, outcome)] += 1
            dimension_outcomes[dimension] = {
                key: counts.get(key, 0)
                for key in ("win", "loss", "tie", "insufficient")
            }
        profiles.append(
            {
                "candidate_alias": alias,
                "source_kind": binding["source_kind"],
                "source_id": binding["source_id"],
                "dimension_outcomes": dimension_outcomes,
            }
        )

    invention_aliases = sorted(
        alias
        for alias, binding in by_alias.items()
        if binding["source_kind"] == "invention"
    )
    dominators: dict[str, list[str]] = {alias: [] for alias in invention_aliases}
    tradeoffs: dict[str, list[str]] = {alias: [] for alias in invention_aliases}
    uncertain: dict[str, list[str]] = {alias: [] for alias in invention_aliases}
    edges: dict[str, set[str]] = {alias: set() for alias in invention_aliases}
    relations: list[dict[str, Any]] = []
    for left, right in itertools.combinations(invention_aliases, 2):
        outcomes = {
            dimension: _pair_verdict(
                consensus_by_key, left, right, dimension
            )
            for dimension in BASE_DOMINANCE_DIMENSIONS
        }
        blocking = sorted(
            dimension
            for dimension, outcome in outcomes.items()
            if outcome == "insufficient"
        )
        if blocking:
            status = "uncertainty_incomparable"
            uncertain[left].append(right)
            uncertain[right].append(left)
        elif "first" in outcomes.values() and "second" in outcomes.values():
            status = "tradeoff_incomparable"
            tradeoffs[left].append(right)
            tradeoffs[right].append(left)
        elif "first" in outcomes.values():
            status = "left_dominates"
            dominators[right].append(left)
            edges[left].add(right)
        elif "second" in outcomes.values():
            status = "right_dominates"
            dominators[left].append(right)
            edges[right].add(left)
        else:
            status = "equivalent_on_base_dimensions"
        relations.append(
            {
                "left_alias": left,
                "right_alias": right,
                "status": status,
                "blocking_dimensions": blocking,
            }
        )
    cycles = _strongly_connected_cycles(invention_aliases, edges)
    cycle_ids_by_alias: dict[str, list[str]] = {
        alias: [] for alias in invention_aliases
    }
    for cycle in cycles:
        for alias in cycle["member_aliases"]:
            cycle_ids_by_alias[alias].append(cycle["cycle_id"])

    dispositions: list[dict[str, Any]] = []
    for alias in invention_aliases:
        binding = by_alias[alias]
        dominated_by = (
            [] if uncertain[alias] else sorted(dominators[alias])
        )
        high_upside_against_dominator = any(
            _pair_verdict(
                consensus_by_key, alias, dominator, "high_risk_upside"
            )
            == "first"
            for dominator in dominated_by
        )
        if cycle_ids_by_alias[alias]:
            status = "dominance_cycle_incomparable"
        elif uncertain[alias]:
            status = "uncertainty_incomparable"
        elif dominated_by:
            status = (
                "protected_high_upside_wildcard"
                if binding["exploration_role"] == "wildcard"
                and high_upside_against_dominator
                else "dominated_internal_merit"
            )
        else:
            status = "pareto_frontier"
        dispositions.append(
            {
                "candidate_alias": alias,
                "invention_id": binding["source_id"],
                "exploration_role": binding["exploration_role"],
                "status": status,
                "dominated_by_aliases": dominated_by,
                "tradeoff_with_aliases": sorted(tradeoffs[alias]),
                "uncertain_against_aliases": sorted(uncertain[alias]),
                "dominance_cycle_ids": sorted(cycle_ids_by_alias[alias]),
                "high_upside_against_a_dominator": (
                    "yes" if high_upside_against_dominator else "no"
                ),
                "investment_authority": "none_internal_exploration_only",
            }
        )
    return profiles, relations, cycles, dispositions


def _validate_control_calibration(
    consensus: Sequence[Mapping[str, Any]],
    private_bindings: Sequence[Mapping[str, Any]],
    controls: Sequence[Mapping[str, Any]],
) -> None:
    by_source = {row["source_id"]: row for row in private_bindings}
    consensus_by_key = {
        (row["left_alias"], row["right_alias"], row["dimension"]): row["verdict"]
        for row in consensus
    }
    control_inputs = {row["control_id"]: row for row in controls}
    control_bindings = [
        row for row in private_bindings if row["source_kind"] == "control"
    ]
    for control in control_bindings:
        control_input = control_inputs[control["source_id"]]
        if control["control_kind"] == "capable":
            sham = next(
                row
                for row in control_bindings
                if row["control_kind"] == "sham"
            )
            probe_dimensions = (
                "essential_relevance",
                "conceptual_depth",
                "physics_decision_relevance",
            )
            against_sham = [
                _pair_verdict(
                    consensus_by_key,
                    control["candidate_alias"],
                    sham["candidate_alias"],
                    dimension,
                )
                for dimension in probe_dimensions
            ]
            if against_sham.count("first") < 2 or "second" in against_sham:
                _fail(
                    "capable_control_sensitivity_failed",
                    "capable same-task baseline was not distinguished from the sham",
                )
            invention_bindings = [
                row
                for row in private_bindings
                if row["source_kind"] == "invention"
            ]
            capable_outcomes = [
                _pair_verdict(
                    consensus_by_key,
                    control["candidate_alias"],
                    invention["candidate_alias"],
                    dimension,
                )
                for invention in invention_bindings
                for dimension in BASE_DOMINANCE_DIMENSIONS
            ]
            if not any(outcome in {"first", "tie"} for outcome in capable_outcomes):
                _fail(
                    "capable_control_sensitivity_failed",
                    "capable baseline is universally treated as noncompetitive",
                )
            continue
        source = by_source[control_input["source_invention_id"]]
        outcomes = {
            dimension: _pair_verdict(
                consensus_by_key,
                source["candidate_alias"],
                control["candidate_alias"],
                dimension,
            )
            for dimension in MERIT_DIMENSIONS
        }
        if control["control_kind"] == "restatement" and set(
            outcomes.values()
        ) != {"tie"}:
            _fail(
                "paraphrase_invariance_failed",
                "restatement changed blinded conceptual merit",
            )
        if control["control_kind"] == "sham":
            source_wins = [
                dimension
                for dimension, outcome in outcomes.items()
                if outcome == "first"
            ]
            required_sensitive = {
                "essential_relevance",
                "conceptual_depth",
                "physics_decision_relevance",
            }
            if (
                len(source_wins) < 4
                or not required_sensitive.intersection(source_wins)
                or "second" in outcomes.values()
            ):
                _fail(
                    "sham_sensitivity_failed",
                    "semantic sham was not substantively distinguished from its source",
                )


def build_non_saturating_conceptual_merit_evaluation(
    portfolio: Mapping[str, Any],
    *,
    controls: Sequence[Mapping[str, Any]],
    hard_integrity_receipt: Mapping[str, Any],
    blind_packet: Mapping[str, Any],
    private_binding: Mapping[str, Any],
    evaluator_reports: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Aggregate categorical pairwise and best-worst merit without a scalar."""

    _validate_portfolio_internal_integrity(portfolio)
    candidate_by_id = {
        row["invention_id"]: row for row in portfolio["matured_inventions"]
    }
    checked_controls = _validate_control_set(
        controls, candidate_by_id, target_id=portfolio["target_id"]
    )
    _validate_blind_source_replay(
        portfolio,
        controls=checked_controls,
        hard_integrity_receipt=hard_integrity_receipt,
        blind_packet=blind_packet,
        private_binding=private_binding,
    )
    reports = [copy.deepcopy(dict(row)) for row in evaluator_reports]
    if len(reports) < 3 or len(
        {row.get("evaluator_id") for row in reports}
    ) != len(reports):
        _fail(
            "evaluator_panel_incomplete",
            "at least three distinct internally correlated evaluator reports are required",
        )
    for report in reports:
        _validate_merit_report(report, blind_packet)
    consensus = _aggregate_reports(reports)
    aliases = [row["candidate_alias"] for row in private_binding["bindings"]]
    best_worst_consensus = _aggregate_best_worst(reports, aliases)
    invention_aliases = [
        row["candidate_alias"]
        for row in private_binding["bindings"]
        if row["source_kind"] == "invention"
    ]
    discrimination = _discrimination_evidence(
        consensus, best_worst_consensus, invention_aliases
    )
    _validate_control_calibration(
        consensus, private_binding["bindings"], checked_controls
    )
    profiles, relations, cycles, dispositions = _derive_merit_outcomes(
        consensus, private_binding["bindings"]
    )
    core = {
        "schema_version": "1.0.0",
        "artifact_kind": "non_saturating_conceptual_merit",
        "evaluation_id": stable_identifier(
            "conceptual-merit",
            blind_packet["packet_digest"],
            [row["report_digest"] for row in reports],
        ),
        "source_portfolio": copy.deepcopy(dict(portfolio)),
        "control_set": checked_controls,
        "hard_integrity_receipt": copy.deepcopy(dict(hard_integrity_receipt)),
        "blind_packet": copy.deepcopy(dict(blind_packet)),
        "unblinding_receipt": copy.deepcopy(dict(private_binding)),
        "evaluator_reports": reports,
        "pairwise_consensus": consensus,
        "best_worst_consensus": best_worst_consensus,
        "discrimination_evidence": discrimination,
        "dimension_profiles": profiles,
        "pareto_relations": relations,
        "dominance_cycles": cycles,
        "exploration_dispositions": dispositions,
        "merit_protocol": {
            "dimensions": list(MERIT_DIMENSIONS),
            "base_dominance_dimensions": list(BASE_DOMINANCE_DIMENSIONS),
            "aggregation": "categorical_pairwise_and_best_worst_plurality_without_scalar",
            "integrity_and_merit_separated": "yes",
            "restatement_invariance_required": "yes",
            "sham_sensitivity_required": "yes",
            "capable_same_task_control_required": "yes",
            "discrimination_floor": "majority_of_invention_pairs_per_dimension_and_resolved_best_worst",
            "uncertainty_rule": "insufficient_blocks_dominance",
            "cycle_rule": "dominance_cycles_are_incomparable_not_frontier_authority",
            "wildcard_rule": "retain_if_base_dominated_but_high_upside_beats_a_dominator",
        },
        "authority_nulls": {
            "external_merit_authority": "unavailable",
            "evaluator_independence": "unavailable",
            "creativity_efficacy_authority": "unavailable",
            "truth_authority": "unavailable",
            "physics_value_authority": "unavailable",
            "generalization_authority": "unavailable",
            "selection_scope": "internal_exploration_only",
        },
    }
    artifact = _seal(core, "content_digest")
    validate_non_saturating_conceptual_merit_evaluation(artifact)
    return artifact


def validate_non_saturating_conceptual_merit_evaluation(
    artifact: Mapping[str, Any],
) -> None:
    """Replay sources, blinding, controls, judgments, plural orders, and nulls."""

    validate_instance(artifact, MERIT_SCHEMA)
    _verify_seal(
        artifact, "content_digest", "non-saturating conceptual merit"
    )
    _assert_no_scalar_keys(artifact)
    portfolio = artifact["source_portfolio"]
    controls = artifact["control_set"]
    hard_integrity = artifact["hard_integrity_receipt"]
    blind = artifact["blind_packet"]
    private = artifact["unblinding_receipt"]
    _validate_portfolio_internal_integrity(portfolio)
    candidate_by_id = {
        row["invention_id"]: row for row in portfolio["matured_inventions"]
    }
    checked_controls = _validate_control_set(
        controls, candidate_by_id, target_id=portfolio["target_id"]
    )
    if controls != checked_controls:
        _fail("control_replay_mismatch", "control set is not in canonical exact order")
    _validate_blind_source_replay(
        portfolio,
        controls=checked_controls,
        hard_integrity_receipt=hard_integrity,
        blind_packet=blind,
        private_binding=private,
    )
    reports = artifact["evaluator_reports"]
    if len(reports) < 3 or len(
        {row.get("evaluator_id") for row in reports}
    ) != len(reports):
        _fail("evaluator_panel_incomplete", "evaluator panel cannot be replayed")
    for report in reports:
        _validate_merit_report(report, blind)
    consensus = _aggregate_reports(reports)
    if consensus != artifact["pairwise_consensus"]:
        _fail("merit_consensus_mismatch", "pairwise consensus cannot be replayed")
    aliases = [row["candidate_alias"] for row in private["bindings"]]
    best_worst_consensus = _aggregate_best_worst(reports, aliases)
    if best_worst_consensus != artifact["best_worst_consensus"]:
        _fail(
            "merit_consensus_mismatch",
            "best-worst consensus and dissent cannot be replayed",
        )
    invention_aliases = [
        row["candidate_alias"]
        for row in private["bindings"]
        if row["source_kind"] == "invention"
    ]
    discrimination = _discrimination_evidence(
        consensus, best_worst_consensus, invention_aliases
    )
    if discrimination != artifact["discrimination_evidence"]:
        _fail(
            "merit_discrimination_mismatch",
            "per-dimension discrimination evidence cannot be replayed",
        )
    _validate_control_calibration(
        consensus, private["bindings"], checked_controls
    )
    profiles, relations, cycles, dispositions = _derive_merit_outcomes(
        consensus, private["bindings"]
    )
    if (
        profiles != artifact["dimension_profiles"]
        or relations != artifact["pareto_relations"]
        or cycles != artifact["dominance_cycles"]
        or dispositions != artifact["exploration_dispositions"]
    ):
        _fail(
            "merit_frontier_mismatch",
            "profiles, incomparability, cycles, or Pareto dispositions cannot be replayed",
        )
    expected_nulls = {
        "external_merit_authority": "unavailable",
        "evaluator_independence": "unavailable",
        "creativity_efficacy_authority": "unavailable",
        "truth_authority": "unavailable",
        "physics_value_authority": "unavailable",
        "generalization_authority": "unavailable",
        "selection_scope": "internal_exploration_only",
    }
    if artifact["authority_nulls"] != expected_nulls:
        _fail(
            "external_authority_forgery",
            "conceptual merit artifact overstates authority",
        )


__all__ = [
    "BASE_DOMINANCE_DIMENSIONS",
    "CONTROL_KINDS",
    "DEEP_REFLECTION_LENSES",
    "MERIT_DIMENSIONS",
    "OpenWorldCreativityError",
    "bind_branch_terminal_receipt",
    "build_branch_intent_manifest",
    "build_non_saturating_conceptual_merit_evaluation",
    "build_open_world_hard_integrity_receipt",
    "build_open_world_maturation_portfolio",
    "build_parallel_maturation_barrier_receipt",
    "build_pre_taxonomy_invention_freeze",
    "classify_frozen_inventions",
    "known_taxonomy_commitment",
    "prepare_blinded_conceptual_merit_packet",
    "run_isolated_parallel_maturation_branches",
    "seal_merit_evaluator_report",
    "validate_non_saturating_conceptual_merit_evaluation",
    "validate_open_world_hard_integrity_receipt",
    "validate_open_world_maturation_portfolio",
    "validate_post_freeze_taxonomy_classification",
    "validate_pre_taxonomy_invention_freeze",
]
