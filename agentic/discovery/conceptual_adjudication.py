# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Blind, content-warranted, plural adjudication of conceptual systems.

The deterministic structural evaluator is a useful integrity screen, but graph
shape and field counts cannot by themselves judge philosophical depth.  This
module supplies the missing semantic review protocol: every candidate is
pseudonymized and deterministically counterbalanced, every judge must cover every
candidate and every non-compensatory dimension, and every judgment must cite a
dimension-appropriate content path whose digest is verified.  Aggregation retains
a Pareto set and never receives a preferred ID.

Local callable judges support reproducible target-specific review.  Reports bind
callable, module, and declared dependency bytes, but judges sharing executable
authority are an explicitly correlated panel rather than independent evidence.
They can authorize only an internal conceptual preference.  External-human or
provider generalization remains unavailable unless a separate trusted boundary is
added; locally authored metadata is never relabelled as external evidence.

Parent-to-synthesis improvement is likewise content-bearing: a typed semantic
patch is recomputed from the two blind packets, and materiality requires a new
objection-bearing round to cite every changed content path.  A new row, a higher
ordinal, or equal-shape padding is never sufficient by itself.
"""

from __future__ import annotations

import copy
import hashlib
import inspect
import re
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from .contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    utc_now,
    validate_instance,
)
from .semantic_identity import semantic_signature_closure


DIMENSIONS = (
    "essential_relevance",
    "explanatory_mediation",
    "conceptual_depth",
    "unification_power",
    "preserved_difference",
    "generativity",
    "reflective_resilience",
    "truth_aptness",
)
RATINGS = {"unknown": 0, "weak": 1, "adequate": 2, "strong": 3}
Judge = Callable[[Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any]]
_WORD = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")

# These fields either state the answer or carry process/identity metadata that a
# content judge must not see.  Structural identity is still recomputed over the
# exact unblinded systems in the evidence closure; removing its stable IDs from
# the blind view prevents genealogy labels from defeating anonymity.  The
# theoretical ``relation`` field is deliberately retained because rival versus
# synthesis polarity is conceptual content, not disposable transport metadata.
_STRIPPED_BLIND_FIELDS = frozenset(
    {
        "system_id",
        "preferred_system_id",
        "lifecycle_state",
        "structural_identity",
        "claimed_score",
        "self_assessment",
        "round_id",
    }
)
_REJECTED_BLIND_FIELDS = frozenset(
    {
        "adjudicator_id",
        "evaluation_score",
        "expected_winner",
        "preferred_candidate",
        "producer_identity",
        "proposer_identity",
        "selected_candidate_alias",
        "selected_system_id",
        "winner",
    }
)
_INDEPENDENCE_CLAIMS = frozenset({"correlated_internal", "independent_internal"})
DEEP_LENS_FAMILIES = frozenset(
    {
        "ontological",
        "dialectical",
        "explanatory",
        "counterfactual",
        "genealogical",
        "phenomenological",
        "philosophy_of_physics",
        "categorical",
        "hott_coherence",
    }
)
REQUIRED_DEEP_LENSES = frozenset({"ontological", "dialectical"})
UNIFICATION_KINDS = frozenset(
    {
        "common_cause",
        "bridge_law",
        "regime_indexed_mediation",
        "categorical_transport",
        "limit_or_descent",
        "conflict_preserving_duality",
        "explanatory_compression",
    }
)
UNIFICATION_NODE_KINDS = frozenset(
    {
        "source_case",
        "primitive",
        "mediator",
        "mechanism",
        "regime",
        "observable",
        "obligation",
        "failure_mode",
    }
)
UNIFICATION_RELATION_KINDS = frozenset(
    {
        "causes",
        "constrains",
        "corrects",
        "depends_on",
        "distinguishes",
        "enables",
        "instantiates",
        "maps_to",
        "mediates",
        "obstructs",
        "precedes",
        "preserves",
        "transports",
    }
)
UNIFICATION_MAPPING_KINDS = frozenset(
    {
        "comparison",
        "correspondence",
        "descent",
        "embedding",
        "interpretation",
        "limit",
        "mediation",
        "production",
        "projection",
        "reduction",
        "transport",
    }
)
_GRAPH_NODE_FIELDS = frozenset({"node_id", "node_kind", "label", "content_paths"})
_GRAPH_EDGE_FIELDS = frozenset(
    {
        "edge_id",
        "source_node_id",
        "relation_kind",
        "target_node_id",
        "statement",
        "warrant_paths",
    }
)
_MAPPING_FIELDS = frozenset(
    {
        "mapping_id",
        "source_case_id",
        "target_node_id",
        "map_kind",
        "bridge_statement",
        "warrant_paths",
    }
)
_DIFFERENCE_FIELDS = frozenset(
    {
        "difference_id",
        "source_case_ids",
        "statement",
        "preservation_witness_paths",
        "witness_node_ids",
        "witness_edge_ids",
    }
)
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class ConceptualAdjudicationError(ContractError):
    """Stable typed failure at the conceptual-preference authority boundary."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"conceptual_adjudication[{reason_code}]: {message}")


def _adjudication_fail(reason_code: str, message: str) -> None:
    raise ConceptualAdjudicationError(reason_code, message)

# A warrant is dimension-specific only if its cited content belongs to a
# semantically relevant part of the candidate.  This blocks the former pattern in
# which one generic mechanism field warranted all eight dimensions.
_DIMENSION_WARRANT_PREFIXES: dict[str, tuple[str, ...]] = {
    "essential_relevance": ("/target_pressures_addressed", "/relevance"),
    "explanatory_mediation": (
        "/mechanism_or_principle",
        "/relations_operations_and_dynamics",
        "/explanatory_dependencies",
    ),
    "conceptual_depth": (
        "/primitives",
        "/ontology",
        "/relations_operations_and_dynamics",
        "/mechanism_or_principle",
    ),
    "unification_power": (
        "/unification_claims/unified_cases_or_routes",
        "/unification_claims/source_case_ids",
        "/unification_claims/mappings",
        "/unification_claims/explanatory_graph_transition",
        "/unification_map",
    ),
    "preserved_difference": (
        "/unification_claims/differences_preserved",
        "/unification_claims/preserved_differences",
        "/identities_and_differences",
    ),
    "generativity": (
        "/formalization_seeds",
        "/implications_and_new_questions",
        "/new_questions",
        "/obligations",
        "/predictions",
    ),
    "reflective_resilience": (
        "/correction_conditions",
        "/residual_contradictions",
        "/falsifiers",
    ),
    "truth_aptness": (
        "/correction_conditions",
        "/residual_contradictions",
        "/formalization_seeds",
        "/falsifiers",
        "/consistency",
    ),
}

_SEMANTIC_COMPONENT_FIELDS: dict[str, tuple[str, ...]] = {
    "claims": (
        "target_pressures_addressed",
        "mechanism_or_principle",
        "identities_and_differences",
        "unification_claims",
        "implications_and_new_questions",
        "formalization_seeds",
        "residual_contradictions",
        "non_claims",
    ),
    "primitives": ("primitives", "ontology"),
    "relations": ("relations_operations_and_dynamics",),
    "dependencies": (
        "mechanism_or_principle",
        "explanatory_dependencies",
        "unification_claims",
        "dependencies",
    ),
    "corrections": ("correction_conditions", "falsifiers"),
}


def _meaningful(value: Any, minimum: int = 6) -> bool:
    return len(_WORD.findall(str(value or ""))) >= minimum


def _field_name(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _distinctive_marker(marker: str) -> bool:
    """Avoid treating ordinary short words such as ``deep`` as leaked IDs."""

    return len(marker) >= 8 or any(character in marker for character in "-_0123456789")


def _replace_marker(text: str, marker: str, alias: str) -> str:
    if text == marker:
        return alias
    if not _distinctive_marker(marker):
        return text
    return re.sub(
        rf"(?<![A-Za-z0-9]){re.escape(marker)}(?![A-Za-z0-9])",
        alias,
        text,
    )


def _blind_project(value: Any, aliases: Mapping[str, str], *, path: str = "$") -> Any:
    """Remove allowed process metadata and reject direct preference leakage."""

    if isinstance(value, Mapping):
        projected: dict[str, Any] = {}
        for raw_key, item in value.items():
            key = str(raw_key)
            normalized = _field_name(key)
            if normalized in _REJECTED_BLIND_FIELDS:
                raise ContractError(f"blind projection rejects forbidden field at {path}.{key}")
            if normalized in _STRIPPED_BLIND_FIELDS:
                continue
            projected[key] = _blind_project(item, aliases, path=f"{path}.{key}")
        return projected
    if isinstance(value, list):
        return [
            _blind_project(item, aliases, path=f"{path}[{index}]")
            for index, item in enumerate(value)
        ]
    if isinstance(value, str):
        rewritten = value
        for system_id, alias in sorted(aliases.items(), key=lambda row: -len(row[0])):
            rewritten = _replace_marker(rewritten, system_id, alias)
        return rewritten
    return copy.deepcopy(value)


def _find_blind_leak(
    value: Any,
    *,
    raw_markers: Sequence[str],
    path: str = "$",
) -> str | None:
    """Return the first forbidden field or unresolved distinctive marker."""

    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = str(raw_key)
            if _field_name(key) in _STRIPPED_BLIND_FIELDS | _REJECTED_BLIND_FIELDS:
                return f"forbidden field {path}.{key}"
            leak = _find_blind_leak(item, raw_markers=raw_markers, path=f"{path}.{key}")
            if leak:
                return leak
        return None
    if isinstance(value, list):
        for index, item in enumerate(value):
            leak = _find_blind_leak(item, raw_markers=raw_markers, path=f"{path}[{index}]")
            if leak:
                return leak
        return None
    if isinstance(value, str):
        for marker in raw_markers:
            if value == marker:
                return f"unresolved identity marker at {path}"
            if _distinctive_marker(marker) and re.search(
                rf"(?<![A-Za-z0-9]){re.escape(marker)}(?![A-Za-z0-9])", value
            ):
                return f"unresolved identity marker at {path}"
    return None


def _counterbalance_seed_digest(
    *,
    target_id: str,
    target_charter: Mapping[str, Any],
    counterbalance_seed: str | None,
) -> tuple[str, str]:
    if counterbalance_seed is not None:
        if not isinstance(counterbalance_seed, str) or not counterbalance_seed.strip():
            raise ContractError("counterbalance seed must be a non-empty string")
        return canonical_digest({"sealed_counterbalance_seed": counterbalance_seed}), "caller_sealed"
    return (
        canonical_digest(
            {
                "target_id": target_id,
                "target_charter_digest": canonical_digest(dict(target_charter)),
                "purpose": "deterministic blind candidate counterbalancing",
            }
        ),
        "deterministically_derived",
    )


def build_blind_packet(
    *,
    target_id: str,
    stage_id: str,
    target_charter: Mapping[str, Any],
    systems: Sequence[Mapping[str, Any]],
    reflection_rounds: Sequence[Mapping[str, Any]],
    proposer_identity: str,
    source_bindings: Mapping[str, Any],
    counterbalance_seed: str | None = None,
) -> tuple[dict[str, Any], dict[str, str]]:
    """Return a leak-checked, counterbalanced packet and private identity map.

    The seed itself is never exposed.  Its digest deterministically permutes
    candidate identities, so input order and content quality do not determine the
    presentation order.  The proposer identity is also represented only by a
    digest; it remains available for self-attestation checks without being shown
    to the judge.
    """

    if not target_id or not stage_id or not proposer_identity:
        raise ContractError("blind adjudication requires target, stage, and proposer identities")
    by_id: dict[str, dict[str, Any]] = {}
    for raw in systems:
        row = copy.deepcopy(dict(raw))
        system_id = str(row.get("system_id", ""))
        if not system_id or system_id in by_id:
            raise ContractError("conceptual systems require unique non-empty system IDs")
        by_id[system_id] = row
    if len(by_id) < 2:
        raise ContractError("plural adjudication requires at least two conceptual systems")

    marker_aliases = {system_id: "candidate-reference" for system_id in by_id}
    projected_charter = _blind_project(dict(target_charter), marker_aliases)
    projected_bindings = _blind_project(dict(source_bindings), marker_aliases)
    seed_digest, seed_mode = _counterbalance_seed_digest(
        target_id=target_id,
        target_charter=projected_charter,
        counterbalance_seed=counterbalance_seed,
    )
    ordered_ids = sorted(
        by_id,
        key=lambda system_id: canonical_digest(
            {
                "counterbalance_seed_digest": seed_digest,
                "private_identity_digest": canonical_digest(system_id),
            }
        ),
    )
    aliases = {system_id: f"candidate-{index:02d}" for index, system_id in enumerate(ordered_ids, 1)}
    candidate_rows = []
    for system_id in ordered_ids:
        content = _blind_project(by_id[system_id], aliases)
        candidate_rows.append(
            {
                "candidate_alias": aliases[system_id],
                "content": content,
                "content_digest": canonical_digest(content),
            }
        )

    rounds = []
    for index, raw in enumerate(reflection_rounds, 1):
        content = _blind_project(dict(raw), aliases)
        rounds.append(
            {
                "round_alias": f"reflection-{index:02d}",
                "content": content,
                "content_digest": canonical_digest(content),
            }
        )
    raw_markers = [*by_id, proposer_identity]
    blind_surface = {
        "target_charter": projected_charter,
        "source_bindings": projected_bindings,
        "candidates": candidate_rows,
        "reflection_rounds": rounds,
    }
    leak = _find_blind_leak(blind_surface, raw_markers=raw_markers)
    if leak:
        raise ContractError(f"blind projection retained identity/preference material: {leak}")
    packet = {
        "schema_version": "2.0.0",
        "target_id": target_id,
        "stage_id": stage_id,
        "proposer_identity_digest": canonical_digest(proposer_identity),
        "target_charter": projected_charter,
        "source_bindings": projected_bindings,
        "candidates": candidate_rows,
        "reflection_rounds": rounds,
        "counterbalancing": {
            "seed_digest": seed_digest,
            "seed_mode": seed_mode,
            "candidate_order_digest": canonical_digest(
                [row["content_digest"] for row in candidate_rows]
            ),
            "input_order_independent": True,
        },
        "blinding_audit": {
            "status": "passed",
            "forbidden_marker_set_digest": canonical_digest(sorted(raw_markers)),
            "recursive_field_check": True,
            "recursive_marker_check": True,
        },
        "blinding_boundary": (
            "Candidate aliases are deterministically counterbalanced from a sealed seed digest. "
            "Raw candidate/proposer identities, preference and lifecycle labels, self-assessments, "
            "claimed scores, and unresolved identity markers are absent from the judge surface."
        ),
    }
    packet["blind_packet_digest"] = canonical_digest(packet)
    private_map = {alias: system_id for system_id, alias in aliases.items()}
    return packet, private_map


def _pointer(payload: Any, pointer: str) -> Any:
    if not pointer.startswith("/"):
        raise ContractError("content warrant path must be an absolute JSON pointer")
    current = payload
    for encoded in pointer[1:].split("/"):
        token = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(current, Mapping) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
            current = current[int(token)]
        else:
            raise ContractError(f"content warrant path does not exist: {pointer}")
    return current


def _sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _file_authority(path: Path) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise ContractError(f"judge authority dependency is not a file: {resolved}")
    return {
        "path": str(resolved),
        "sha256": _sha256_file(resolved),
        "size_bytes": resolved.stat().st_size,
    }


def _callable_fingerprint(judge: Judge) -> dict[str, str]:
    try:
        source = inspect.getsource(judge)
    except (OSError, TypeError):
        source = ""
    code = getattr(judge, "__code__", None)
    code_digest = (
        canonical_digest(
            {
                # ``marshal.dumps(code)`` includes interpreter specialization
                # state on supported runtimes and can change after the first
                # invocation.  Public code bytes and structural metadata remain
                # stable across execution while still distinguishing callables.
                "bytecode": code.co_code.hex(),
                "names": list(code.co_names),
                "variable_names": list(code.co_varnames),
                "argument_counts": [
                    code.co_argcount,
                    code.co_posonlyargcount,
                    code.co_kwonlyargcount,
                ],
                "constants": [
                    (
                        {
                            "nested_bytecode": value.co_code.hex(),
                            "nested_names": list(value.co_names),
                        }
                        if inspect.iscode(value)
                        else repr(value)
                    )
                    for value in code.co_consts
                ],
            }
        )
        if code is not None
        else canonical_digest(
            {
                "callable_type": f"{type(judge).__module__}.{type(judge).__qualname__}",
                "representation": repr(judge),
            }
        )
    )
    return {
        "module": str(getattr(judge, "__module__", "")),
        "qualname": str(getattr(judge, "__qualname__", type(judge).__qualname__)),
        "source_digest": canonical_digest(source),
        "code_digest": code_digest,
    }


def _judge_authority(
    judge: Judge,
    *,
    dependency_paths: Sequence[str | Path] = (),
) -> dict[str, Any]:
    """Bind executable evidence without using a nominal adjudicator identity.

    The module file covers helper functions used by a thin wrapper.  Callers can
    additionally declare configuration, prompt, rubric, or library files whose
    bytes materially determine the judgment.  Undeclared transitive imports and
    external services remain outside this local authority boundary.
    """

    fingerprint = _callable_fingerprint(judge)
    module_file = inspect.getsourcefile(judge)
    module_authority: dict[str, Any] | None = None
    if module_file and Path(module_file).is_file():
        module_authority = _file_authority(Path(module_file))
    dependencies = sorted(
        (_file_authority(Path(path)) for path in dependency_paths),
        key=lambda row: (row["path"], row["sha256"]),
    )
    core = {
        "schema_version": "1.0.0",
        "callable": fingerprint,
        "module_file": module_authority,
        "dependency_files": dependencies,
        "coverage": {
            "bound": [
                "callable source and code object",
                "defining module bytes when inspectable",
                "explicitly declared dependency bytes",
            ],
            "excluded": [
                "undeclared transitive imports",
                "dynamic imports",
                "ambient process state",
                "external model or human identity without a trusted receipt",
            ],
        },
    }
    # Judges from one module are correlated even when thin wrappers differ.  An
    # explicit shared dependency also contributes to the group, making this a
    # conservative independence test rather than a user-authored label.
    correlation_material = {
        "module_digest": (
            module_authority["sha256"] if module_authority else fingerprint["module"]
        ),
        "dependency_digests": [row["sha256"] for row in dependencies],
    }
    authority = {
        **core,
        "correlation_group_digest": canonical_digest(correlation_material),
    }
    authority["authority_digest"] = canonical_digest(authority)
    return authority


def _validate_recorded_authority(
    authority: Mapping[str, Any],
    *,
    judge: Judge | None = None,
) -> None:
    if authority.get("schema_version") != "1.0.0":
        raise ContractError("conceptual judge authority schema drift")
    expected = canonical_digest(
        {key: value for key, value in authority.items() if key != "authority_digest"}
    )
    if authority.get("authority_digest") != expected:
        raise ContractError("conceptual judge authority digest mismatch")
    for descriptor in [authority.get("module_file"), *authority.get("dependency_files", [])]:
        if descriptor is None:
            continue
        if not isinstance(descriptor, Mapping):
            raise ContractError("conceptual judge authority file descriptor is malformed")
        path = Path(str(descriptor.get("path", "")))
        if not path.is_file() or _file_authority(path) != dict(descriptor):
            raise ContractError("conceptual judge authority bytes no longer match the report")
    if judge is not None:
        dependency_paths = [
            Path(str(row["path"])) for row in authority.get("dependency_files", [])
        ]
        current = _judge_authority(judge, dependency_paths=dependency_paths)
        if current.get("authority_digest") != authority.get("authority_digest"):
            raise ContractError("conceptual judge callable does not match recorded authority")


def _normalize_dimension_warrants(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Add the protocol's explicit dimension tag without inventing a warrant."""

    normalized = copy.deepcopy(dict(raw))
    for dimension, finding in normalized.items():
        if dimension not in DIMENSIONS or not isinstance(finding, Mapping):
            continue
        warrants = finding.get("warrants")
        if not isinstance(warrants, list):
            continue
        for warrant in warrants:
            if isinstance(warrant, dict):
                warrant.setdefault("dimension", dimension)
    return normalized


def build_judge_report(
    packet: Mapping[str, Any],
    *,
    adjudicator_id: str,
    perspective: str,
    version: str,
    judge: Judge,
    created_at: str | None = None,
    independence_claim: str = "correlated_internal",
    dependency_paths: Sequence[str | Path] = (),
    lens_family: str | None = None,
) -> dict[str, Any]:
    """Run one identified content judge over all blind candidates.

    ``independence_claim`` is evidence-bearing rather than rhetorical.  The
    aggregator accepts ``independent_internal`` only when callable/module/
    dependency authorities are pairwise distinct and non-overlapping.  The
    practical default is an honestly labelled correlated local critic.
    """

    if canonical_digest(adjudicator_id) == packet.get("proposer_identity_digest"):
        raise ContractError("conceptual adjudicator must differ from the proposer")
    if not all(isinstance(value, str) and value.strip() for value in (adjudicator_id, perspective, version)):
        raise ContractError("adjudicator identity, perspective, and version are required")
    if independence_claim not in _INDEPENDENCE_CLAIMS:
        raise ContractError("conceptual adjudicator independence claim is unsupported")
    authority = _judge_authority(judge, dependency_paths=dependency_paths)
    if lens_family is not None and lens_family not in DEEP_LENS_FAMILIES:
        raise ContractError(f"unsupported conceptual deep lens: {lens_family}")
    findings = []
    for candidate in packet.get("candidates", []):
        raw = judge(copy.deepcopy(candidate), copy.deepcopy(dict(packet)))
        if not isinstance(raw, Mapping):
            raise ContractError("conceptual judge must return an object")
        raw_finding = copy.deepcopy(dict(raw))
        if isinstance(raw_finding.get("dimensions"), Mapping):
            raw_dimensions = dict(raw_finding.pop("dimensions"))
            deep_lens = raw_finding.pop("deep_lens_analysis", None)
            if raw_finding:
                raise ContractError(
                    "conceptual judge envelope has unknown fields: "
                    f"{sorted(raw_finding)}"
                )
        else:
            raw_dimensions = raw_finding
            deep_lens = None
        finding = {
            "candidate_alias": candidate["candidate_alias"],
            "dimensions": _normalize_dimension_warrants(raw_dimensions),
        }
        if deep_lens is not None:
            if not isinstance(deep_lens, Mapping):
                raise ContractError("deep lens analysis must be an object")
            normalized_lens = copy.deepcopy(dict(deep_lens))
            normalized_lens.setdefault("lens_family", lens_family)
            lens_core = {
                key: value
                for key, value in normalized_lens.items()
                if key != "analysis_digest"
            }
            normalized_lens["analysis_digest"] = canonical_digest(lens_core)
            finding["deep_lens_analysis"] = normalized_lens
        findings.append(finding)
    report = {
        "schema_version": "2.0.0",
        "report_id": "pending",
        "adjudicator": {
            "adjudicator_id": adjudicator_id,
            "version": version,
            "perspective": perspective,
            **({"lens_family": lens_family} if lens_family is not None else {}),
            "evidence_class": "deterministic_internal_content_judge",
            "independence_claim": independence_claim,
            "executable_digest": authority["authority_digest"],
            "authority": authority,
        },
        "blind_packet_digest": packet["blind_packet_digest"],
        "candidate_findings": findings,
        "external_authentication": {
            "status": "unavailable",
            "reason": "No trusted external-human/provider receipt was supplied to this local judge.",
        },
        "created_at": created_at or utc_now(),
    }
    content_digest = canonical_digest(
        report, exclude_keys=("report_id", "report_digest", "created_at")
    )
    report["report_id"] = stable_identifier(
        "conceptual-judge-report", adjudicator_id, packet["blind_packet_digest"], content_digest
    )
    report["report_digest"] = canonical_digest(
        report, exclude_keys=("report_digest", "created_at")
    )
    validate_judge_report(report, packet, judge=judge)
    return report


def validate_judge_report(
    report: Mapping[str, Any],
    packet: Mapping[str, Any],
    *,
    judge: Judge | None = None,
) -> None:
    """Verify coverage, authority bytes, and dimension-specific warrants."""

    expected_digest = canonical_digest(report, exclude_keys=("report_digest", "created_at"))
    if report.get("report_digest") != expected_digest:
        raise ContractError("conceptual judge report digest mismatch")
    if report.get("blind_packet_digest") != packet.get("blind_packet_digest"):
        raise ContractError("conceptual judge report crossed its blind packet")
    adjudicator = report.get("adjudicator", {})
    if canonical_digest(adjudicator.get("adjudicator_id")) == packet.get(
        "proposer_identity_digest"
    ):
        raise ContractError("conceptual judgment is self-attested by the proposer")
    if adjudicator.get("independence_claim") not in _INDEPENDENCE_CLAIMS:
        raise ContractError("conceptual judge lacks an honest independence claim")
    authority = adjudicator.get("authority")
    if not isinstance(authority, Mapping):
        raise ContractError("conceptual judge lacks executable authority material")
    _validate_recorded_authority(authority, judge=judge)
    if adjudicator.get("executable_digest") != authority.get("authority_digest"):
        raise ContractError("conceptual judge executable/authority digest mismatch")
    expected_aliases = [row["candidate_alias"] for row in packet.get("candidates", [])]
    rows = report.get("candidate_findings", [])
    if [row.get("candidate_alias") for row in rows] != expected_aliases:
        raise ContractError("conceptual judge did not cover every blind candidate in order")
    by_alias = {row["candidate_alias"]: row for row in packet["candidates"]}
    for row in rows:
        dimensions = row.get("dimensions")
        if not isinstance(dimensions, Mapping) or set(dimensions) != set(DIMENSIONS):
            raise ContractError("conceptual judge dimensions are incomplete or unknown")
        candidate = by_alias[row["candidate_alias"]]
        for dimension in DIMENSIONS:
            finding = dimensions[dimension]
            if not isinstance(finding, Mapping) or finding.get("rating") not in RATINGS:
                raise ContractError(f"invalid conceptual rating for {dimension}")
            warrants = finding.get("warrants", [])
            if finding["rating"] != "unknown" and not warrants:
                raise ContractError(f"non-unknown conceptual rating lacks warrants: {dimension}")
            for warrant in warrants:
                if warrant.get("dimension") != dimension:
                    raise ContractError(f"conceptual warrant is not dimension-specific: {dimension}")
                warrant_path = str(warrant.get("path", ""))
                if not any(
                    warrant_path == prefix or warrant_path.startswith(prefix + "/")
                    for prefix in _DIMENSION_WARRANT_PREFIXES[dimension]
                ):
                    raise ContractError(
                        f"conceptual warrant path is not relevant to {dimension}: {warrant_path}"
                    )
                value = _pointer(candidate["content"], warrant_path)
                if warrant.get("value_digest") != canonical_digest(value):
                    raise ContractError(f"conceptual warrant digest mismatch: {dimension}")
                if not _meaningful(warrant.get("explanation"), 6):
                    raise ContractError(f"conceptual warrant explanation is empty: {dimension}")
            if not _meaningful(finding.get("strongest_objection"), 6):
                raise ContractError(f"conceptual finding lacks a substantive objection: {dimension}")
            if not _meaningful(finding.get("correction_test"), 6):
                raise ContractError(f"conceptual finding lacks a substantive correction test: {dimension}")


def _lens_content_digest(analysis: Mapping[str, Any]) -> str:
    """Detect one analysis relabelled as several allegedly different lenses."""

    return canonical_digest(
        {
            key: value
            for key, value in analysis.items()
            if key not in {"lens_family", "analysis_digest"}
        }
    )


def _validate_deep_lens_panel(
    packet: Mapping[str, Any], reports: Sequence[Mapping[str, Any]]
) -> list[str]:
    """Require ontological, dialectical, and one additional content-bearing lens."""

    lens_families: list[str] = []
    aliases = [str(row["candidate_alias"]) for row in packet.get("candidates", [])]
    candidate_by_alias = {
        str(row["candidate_alias"]): row for row in packet.get("candidates", [])
    }
    content_digests_by_alias: dict[str, set[str]] = {
        alias: set() for alias in aliases
    }
    for report in reports:
        adjudicator = report.get("adjudicator", {})
        lens_family = str(adjudicator.get("lens_family", ""))
        if lens_family not in DEEP_LENS_FAMILIES:
            _adjudication_fail(
                "adjudication_lens_floor_unmet",
                "every authoritative judge report must declare a supported deep lens",
            )
        lens_families.append(lens_family)
        rows = report.get("candidate_findings", [])
        if [str(row.get("candidate_alias", "")) for row in rows] != aliases:
            _adjudication_fail(
                "adjudication_lens_floor_unmet",
                "every deep lens must cover every blind candidate in packet order",
            )
        for row in rows:
            alias = str(row["candidate_alias"])
            analysis = row.get("deep_lens_analysis")
            if not isinstance(analysis, Mapping):
                _adjudication_fail(
                    "adjudication_lens_floor_unmet",
                    f"{lens_family} lacks a deep analysis for {alias}",
                )
            if analysis.get("lens_family") != lens_family:
                _adjudication_fail(
                    "adjudication_lens_floor_unmet",
                    f"deep analysis/report lens mismatch for {alias}",
                )
            expected_digest = canonical_digest(
                {key: value for key, value in analysis.items() if key != "analysis_digest"}
            )
            if analysis.get("analysis_digest") != expected_digest:
                _adjudication_fail(
                    "adjudication_digest_mismatch",
                    f"deep lens analysis digest mismatch for {alias}",
                )
            for field in (
                "focal_question",
                "root_aporia_or_tension",
                "inherited_assumption_exposed",
                "candidate_specific_analysis",
                "strongest_objection",
                "correction_test",
            ):
                if not _meaningful(analysis.get(field), 6):
                    _adjudication_fail(
                        "adjudication_lens_floor_unmet",
                        f"{lens_family} analysis is not substantive at {alias}/{field}",
                    )
            candidate_content = candidate_by_alias[alias]["content"]
            warrants = analysis.get("content_warrants", [])
            paths = [str(warrant.get("path", "")) for warrant in warrants if isinstance(warrant, Mapping)]
            if len(warrants) < 2 or len(set(paths)) < 2:
                _adjudication_fail(
                    "adjudication_lens_floor_unmet",
                    f"{lens_family} must cite at least two distinct candidate paths for {alias}",
                )
            for warrant in warrants:
                if not isinstance(warrant, Mapping):
                    _adjudication_fail(
                        "adjudication_lens_floor_unmet",
                        f"malformed deep-lens warrant for {alias}",
                    )
                path = str(warrant.get("path", ""))
                try:
                    value = _pointer(candidate_content, path)
                except ContractError as exc:
                    _adjudication_fail(
                        "adjudication_candidate_content_mismatch", str(exc)
                    )
                if warrant.get("value_digest") != canonical_digest(value):
                    _adjudication_fail(
                        "adjudication_candidate_content_mismatch",
                        f"deep-lens warrant digest mismatch for {alias}{path}",
                    )
                if not _meaningful(warrant.get("explanation"), 6):
                    _adjudication_fail(
                        "adjudication_lens_floor_unmet",
                        f"deep-lens warrant is not substantive for {alias}{path}",
                    )
            consequence = analysis.get("conceptual_consequence", {})
            if not isinstance(consequence, Mapping) or not _meaningful(
                consequence.get("statement"), 6
            ):
                _adjudication_fail(
                    "adjudication_lens_floor_unmet",
                    f"deep lens lacks a typed conceptual consequence for {alias}",
                )
            for path in consequence.get("changed_paths", []):
                try:
                    _pointer(candidate_content, str(path))
                except ContractError as exc:
                    _adjudication_fail(
                        "adjudication_candidate_content_mismatch", str(exc)
                    )
            handback = analysis.get("physics_value_handback", {})
            if not isinstance(handback, Mapping):
                _adjudication_fail(
                    "adjudication_lens_floor_unmet",
                    f"deep lens lacks a physics-value handback for {alias}",
                )
            pressure_paths = handback.get("target_pressure_paths", [])
            if not pressure_paths:
                _adjudication_fail(
                    "adjudication_lens_floor_unmet",
                    f"deep lens does not return to a target pressure for {alias}",
                )
            for path in pressure_paths:
                path = str(path)
                if not path.startswith("/target_pressures_addressed"):
                    _adjudication_fail(
                        "adjudication_lens_floor_unmet",
                        f"physics handback leaves the target-pressure surface for {alias}",
                    )
                try:
                    _pointer(candidate_content, path)
                except ContractError as exc:
                    _adjudication_fail(
                        "adjudication_candidate_content_mismatch", str(exc)
                    )
            if not _meaningful(handback.get("changed_theory_question"), 6) or not _meaningful(
                handback.get("relevance_limit"), 6
            ):
                _adjudication_fail(
                    "adjudication_lens_floor_unmet",
                    f"physics handback is not substantive for {alias}",
                )
            content_digest = _lens_content_digest(analysis)
            if content_digest in content_digests_by_alias[alias]:
                _adjudication_fail(
                    "adjudication_duplicate_lens_analysis",
                    f"one deep analysis was relabelled for {alias}",
                )
            content_digests_by_alias[alias].add(content_digest)
    lens_set = set(lens_families)
    if (
        len(reports) < 3
        or len(lens_set) < 3
        or not REQUIRED_DEEP_LENSES.issubset(lens_set)
    ):
        _adjudication_fail(
            "adjudication_lens_floor_unmet",
            "authoritative adjudication requires ontological, dialectical, and at least one additional deep lens",
        )
    return sorted(lens_set)


def _authority_overlap_tokens(authority: Mapping[str, Any]) -> set[str]:
    callable_material = authority.get("callable", {})
    tokens = {
        str(authority.get("authority_digest", "")),
        str(authority.get("correlation_group_digest", "")),
        str(callable_material.get("code_digest", "")),
    }
    source_digest = str(callable_material.get("source_digest", ""))
    if source_digest and source_digest != canonical_digest(""):
        tokens.add(source_digest)
    module_file = authority.get("module_file")
    if isinstance(module_file, Mapping):
        tokens.add(str(module_file.get("sha256", "")))
    for dependency in authority.get("dependency_files", []):
        if isinstance(dependency, Mapping):
            tokens.add(str(dependency.get("sha256", "")))
    return {token for token in tokens if token}


def _panel_authority(reports: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    claims = [
        str(report.get("adjudicator", {}).get("independence_claim", ""))
        for report in reports
    ]
    if len(set(claims)) != 1:
        raise ContractError("conceptual panel cannot mix correlated and independent claims")
    authorities = [report["adjudicator"]["authority"] for report in reports]
    independent = claims[0] == "independent_internal"
    if independent:
        for left_index, left in enumerate(authorities):
            for right in authorities[left_index + 1 :]:
                if _authority_overlap_tokens(left) & _authority_overlap_tokens(right):
                    raise ContractError(
                        "conceptual judges claimed independence but share callable, module, or dependency authority"
                    )
    return {
        "plural_independent_perspectives": independent,
        "panel_evidence_class": (
            "independent_internal_judgment"
            if independent
            else "correlated_internal_critique"
        ),
        "judge_authority_digests": sorted(
            {str(authority["authority_digest"]) for authority in authorities}
        ),
        "correlation_group_digests": sorted(
            {str(authority["correlation_group_digest"]) for authority in authorities}
        ),
    }


def _pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _semantic_kind(path: str) -> str:
    root = path.lstrip("/").split("/", 1)[0].replace("~1", "/").replace("~0", "~")
    if root in {"primitives", "ontology"}:
        return "primitive"
    if root == "relations_operations_and_dynamics":
        return "relation"
    if root in {"mechanism_or_principle", "explanatory_dependencies", "dependencies"}:
        return "dependency"
    if root in {"correction_conditions", "falsifiers"}:
        return "correction"
    return "claim"


def _semantic_changes(before: Any, after: Any, *, path: str = "") -> list[dict[str, Any]]:
    """Return an exact deterministic JSON-pointer diff for conceptual content."""

    if isinstance(before, Mapping) and isinstance(after, Mapping):
        changes: list[dict[str, Any]] = []
        for key in sorted(set(before) | set(after), key=str):
            child = f"{path}/{_pointer_token(str(key))}"
            if key not in before:
                changes.append(
                    {
                        "path": child,
                        "operation": "added",
                        "semantic_kind": _semantic_kind(child),
                        "before_digest": None,
                        "after_digest": canonical_digest(after[key]),
                    }
                )
            elif key not in after:
                changes.append(
                    {
                        "path": child,
                        "operation": "removed",
                        "semantic_kind": _semantic_kind(child),
                        "before_digest": canonical_digest(before[key]),
                        "after_digest": None,
                    }
                )
            else:
                changes.extend(_semantic_changes(before[key], after[key], path=child))
        return changes
    # Lists are treated as semantic units.  This avoids pretending that an index
    # is a stable conceptual identity while still binding the exact before/after.
    if canonical_digest(before) == canonical_digest(after):
        return []
    pointer = path or "/"
    return [
        {
            "path": pointer,
            "operation": "modified",
            "semantic_kind": _semantic_kind(pointer),
            "before_digest": canonical_digest(before),
            "after_digest": canonical_digest(after),
        }
    ]


def _contains_exact(value: Any, token: str) -> bool:
    if isinstance(value, Mapping):
        return any(_contains_exact(item, token) for item in value.values())
    if isinstance(value, list):
        return any(_contains_exact(item, token) for item in value)
    return value == token


def _relevant_round_contents(packet: Mapping[str, Any], alias: str | None) -> list[dict[str, Any]]:
    if not alias:
        return []
    return [
        dict(row.get("content", {}))
        for row in packet.get("reflection_rounds", [])
        if _contains_exact(row.get("content", {}), alias)
    ]


def _round_objections_and_corrections(
    packet: Mapping[str, Any], alias: str | None
) -> tuple[list[str], list[str]]:
    objections: list[str] = []
    corrections: list[str] = []
    for content in _relevant_round_contents(packet, alias):
        objections.extend(
            str(item) for item in content.get("strongest_objections", []) if str(item)
        )
        corrections.extend(
            str(item) for item in content.get("correction_tests", []) if str(item)
        )
    return objections, corrections


def _component_digests(
    *,
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    previous_packet: Mapping[str, Any],
    packet: Mapping[str, Any],
    previous_alias: str | None,
    current_alias: str | None,
) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for component, fields in _SEMANTIC_COMPONENT_FIELDS.items():
        prior_value = {field: before[field] for field in fields if field in before}
        current_value = {field: after[field] for field in fields if field in after}
        rows[component] = {
            "before_digest": canonical_digest(prior_value),
            "after_digest": canonical_digest(current_value),
            "changed": canonical_digest(prior_value) != canonical_digest(current_value),
        }
    prior_objections, prior_round_corrections = _round_objections_and_corrections(
        previous_packet, previous_alias
    )
    current_objections, current_round_corrections = _round_objections_and_corrections(
        packet, current_alias
    )
    rows["objections"] = {
        "before_digest": canonical_digest(prior_objections),
        "after_digest": canonical_digest(current_objections),
        "changed": canonical_digest(prior_objections) != canonical_digest(current_objections),
    }
    prior_corrections = [*before.get("correction_conditions", []), *prior_round_corrections]
    current_corrections = [*after.get("correction_conditions", []), *current_round_corrections]
    rows["corrections"] = {
        "before_digest": canonical_digest(prior_corrections),
        "after_digest": canonical_digest(current_corrections),
        "changed": canonical_digest(prior_corrections) != canonical_digest(current_corrections),
    }
    return rows


def _build_semantic_patch(
    *,
    packet: Mapping[str, Any],
    previous_packet: Mapping[str, Any],
    previous: Mapping[str, Any],
    selected_alias: str | None,
    selected_system: str | None,
) -> dict[str, Any]:
    previous_consensus = next(
        (
            row
            for row in previous.get("candidate_consensus", [])
            if row.get("system_id") == selected_system
        ),
        None,
    )
    previous_alias = (
        str(previous_consensus["candidate_alias"]) if previous_consensus else None
    )
    previous_row = next(
        (
            row
            for row in previous_packet.get("candidates", [])
            if row.get("candidate_alias") == previous_alias
        ),
        None,
    )
    current_row = next(
        (
            row
            for row in packet.get("candidates", [])
            if row.get("candidate_alias") == selected_alias
        ),
        None,
    )
    before = dict(previous_row.get("content", {})) if previous_row else {}
    after = dict(current_row.get("content", {})) if current_row else {}
    changes = _semantic_changes(before, after)
    changed_paths = {row["path"] for row in changes}

    prior_rounds = list(previous_packet.get("reflection_rounds", []))
    current_rounds = list(packet.get("reflection_rounds", []))
    prefix_preserved = len(current_rounds) >= len(prior_rounds) and [
        row.get("content_digest") for row in current_rounds[: len(prior_rounds)]
    ] == [row.get("content_digest") for row in prior_rounds]
    new_rounds = current_rounds[len(prior_rounds) :] if prefix_preserved else []

    verified_links: list[dict[str, Any]] = []
    invalid_reasons: list[str] = []
    linked_paths: set[str] = set()
    for round_row in new_rounds:
        round_alias = str(round_row.get("round_alias", ""))
        content = round_row.get("content", {})
        if not isinstance(content, Mapping):
            invalid_reasons.append(f"{round_alias}: round content is not an object")
            continue
        objections = [str(item) for item in content.get("strongest_objections", [])]
        corrections = [str(item) for item in content.get("correction_tests", [])]
        links = content.get("semantic_patch_links", [])
        if not isinstance(links, list):
            invalid_reasons.append(f"{round_alias}: semantic_patch_links is not an array")
            continue
        for index, raw_link in enumerate(links):
            label = f"{round_alias}/link-{index + 1}"
            if not isinstance(raw_link, Mapping):
                invalid_reasons.append(f"{label}: link is not an object")
                continue
            candidate_ref = str(raw_link.get("candidate_ref", ""))
            objection = str(raw_link.get("objection", ""))
            correction = str(raw_link.get("correction_test", ""))
            paths = sorted({str(item) for item in raw_link.get("changed_paths", [])})
            if candidate_ref != selected_alias:
                invalid_reasons.append(f"{label}: candidate reference does not match selection")
                continue
            if objection not in objections or not _meaningful(objection, 6):
                invalid_reasons.append(f"{label}: objection is absent or not substantive")
                continue
            if correction not in corrections or not _meaningful(correction, 6):
                invalid_reasons.append(f"{label}: correction test is absent or not substantive")
                continue
            if not paths or not set(paths).issubset(changed_paths):
                invalid_reasons.append(f"{label}: changed paths do not match the exact semantic diff")
                continue
            link = {
                "round_alias": round_alias,
                "candidate_alias": candidate_ref,
                "objection_digest": canonical_digest(objection),
                "correction_digest": canonical_digest(correction),
                "changed_paths": paths,
            }
            link["link_digest"] = canonical_digest(link)
            verified_links.append(link)
            linked_paths.update(paths)

    unlinked_paths = sorted(changed_paths - linked_paths)
    component_digests = _component_digests(
        before=before,
        after=after,
        previous_packet=previous_packet,
        packet=packet,
        previous_alias=previous_alias,
        current_alias=selected_alias,
    )
    core = {
        "schema_version": "1.0.0",
        "system_id": selected_system,
        "parent_candidate_alias": previous_alias,
        "synthesis_candidate_alias": selected_alias,
        "parent_content_digest": canonical_digest(before),
        "synthesis_content_digest": canonical_digest(after),
        "content_changed": bool(changes),
        "changes": changes,
        "component_digests": component_digests,
        "round_history_prefix_preserved": prefix_preserved,
        "new_round_aliases": [str(row.get("round_alias", "")) for row in new_rounds],
        "objection_links": verified_links,
        "unlinked_change_paths": unlinked_paths,
        "all_changes_objection_linked": bool(changes) and not unlinked_paths,
        "invalid_link_reasons": invalid_reasons,
    }
    core["patch_digest"] = canonical_digest(core)
    return core


def validate_material_system_transition(
    *,
    previous_evidence: Mapping[str, Any],
    current_evidence: Mapping[str, Any],
    before_system: Mapping[str, Any],
    after_system: Mapping[str, Any],
) -> None:
    """Authorize a stable-ID system mutation from exact blind-stage evidence.

    Canonical cycles normally reject two different records under one conceptual
    system ID.  A reflective maturation is the narrow exception: the bound
    adjudication must preserve selection and round history, expose an exact
    objection-linked semantic patch, improve a noncompensatory dimension, and
    bind both blind candidate contents.  This validator also recomputes the raw
    system diff so an evidence packet cannot authorize undeclared changes.
    """

    system_id = str(before_system.get("system_id", ""))
    if not system_id or after_system.get("system_id") != system_id:
        raise ContractError("material system transition must preserve one stable system ID")
    if current_evidence.get("input_binding", {}).get(
        "previous_evidence_digest"
    ) != previous_evidence.get("evidence_digest"):
        raise ContractError("material system transition is not bound to the prior evidence")
    comparison = current_evidence.get("stage_comparison", {})
    patch = comparison.get("semantic_patch", {})
    if (
        comparison.get("applicability") != "applicable"
        or comparison.get("material") is not True
        or comparison.get("prior_selected_system_id") != system_id
        or comparison.get("current_selected_system_id") != system_id
        or patch.get("system_id") != system_id
        or patch.get("content_changed") is not True
        or patch.get("all_changes_objection_linked") is not True
        or patch.get("round_history_prefix_preserved") is not True
        or patch.get("unlinked_change_paths")
        or patch.get("invalid_link_reasons")
        or not patch.get("objection_links")
        or comparison.get("nondegrading_dimension_floors") is not True
        or comparison.get("reflective_resilience_increased") is not True
    ):
        raise ContractError("stable-ID conceptual mutation lacks a material stage transition")

    previous_alias = str(patch.get("parent_candidate_alias", ""))
    current_alias = str(patch.get("synthesis_candidate_alias", ""))
    if (
        previous_evidence.get("private_candidate_bindings", {}).get(previous_alias)
        != system_id
        or current_evidence.get("private_candidate_bindings", {}).get(current_alias)
        != system_id
    ):
        raise ContractError("material system transition aliases do not bind the stable system")

    def blind_content(evidence: Mapping[str, Any], alias: str) -> Mapping[str, Any]:
        rows = [
            row
            for row in evidence.get("blind_packet", {}).get("candidates", [])
            if row.get("candidate_alias") == alias
        ]
        if len(rows) != 1 or not isinstance(rows[0].get("content"), Mapping):
            raise ContractError("material system transition lacks one bound blind candidate")
        return rows[0]["content"]

    previous_content = blind_content(previous_evidence, previous_alias)
    current_content = blind_content(current_evidence, current_alias)
    if (
        canonical_digest(previous_content) != patch.get("parent_content_digest")
        or canonical_digest(current_content) != patch.get("synthesis_content_digest")
    ):
        raise ContractError("material system transition content digests do not match blind evidence")

    raw_changes = _semantic_changes(dict(before_system), dict(after_system))
    recorded_changes = patch.get("changes", [])
    if raw_changes != recorded_changes:
        raise ContractError("stable-ID conceptual mutation contains undeclared semantic changes")
    changed_paths = {row["path"] for row in raw_changes}
    linked_paths = {
        path
        for link in patch.get("objection_links", [])
        for path in link.get("changed_paths", [])
    }
    if not changed_paths or linked_paths != changed_paths:
        raise ContractError("stable-ID conceptual mutation is not exactly objection linked")


def _dominates(left: Mapping[str, int], right: Mapping[str, int]) -> bool:
    return all(left[name] >= right[name] for name in DIMENSIONS) and any(
        left[name] > right[name] for name in DIMENSIONS
    )


def aggregate_adjudication(
    packet: Mapping[str, Any],
    reports: Sequence[Mapping[str, Any]],
    *,
    candidate_bindings: Mapping[str, str],
    previous: Mapping[str, Any] | None = None,
    previous_packet: Mapping[str, Any] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Aggregate judges without inflating correlated critique into independence."""

    if len(reports) < 3:
        raise ContractError("conceptual adjudication requires at least three judge reports")
    # Canonical report order makes the result invariant to transport or scheduler
    # order and gives each consensus rating/warrant vector a stable interpretation.
    reports = sorted(
        (dict(report) for report in reports),
        key=lambda report: (
            str(report.get("adjudicator", {}).get("adjudicator_id", "")),
            str(report.get("report_id", "")),
        ),
    )
    identities = [row.get("adjudicator", {}).get("adjudicator_id") for row in reports]
    perspectives = [row.get("adjudicator", {}).get("perspective") for row in reports]
    if len(set(identities)) != len(identities) or len(set(perspectives)) < 3:
        raise ContractError("conceptual adjudication requires distinct identities and perspectives")
    for report in reports:
        validate_judge_report(report, packet)
    panel_authority = _panel_authority(reports)
    aliases = [row["candidate_alias"] for row in packet["candidates"]]
    if set(candidate_bindings) != set(aliases) or len(set(candidate_bindings.values())) != len(aliases):
        raise ContractError("private candidate bindings are not an exact bijection")

    finding_by_report = [
        {row["candidate_alias"]: row["dimensions"] for row in report["candidate_findings"]}
        for report in reports
    ]
    consensus_rows = []
    floor_vectors: dict[str, dict[str, int]] = {}
    qualified = []
    for alias in aliases:
        dimension_rows: dict[str, Any] = {}
        floor_vector: dict[str, int] = {}
        clears = True
        for dimension in DIMENSIONS:
            ratings = [view[alias][dimension]["rating"] for view in finding_by_report]
            values = [RATINGS[rating] for rating in ratings]
            floor = min(values)
            floor_vector[dimension] = floor
            clears = clears and floor >= RATINGS["adequate"]
            dimension_rows[dimension] = {
                "ratings": ratings,
                "minimum_rating": next(name for name, value in RATINGS.items() if value == floor),
                "unanimous_adequate_or_strong": floor >= RATINGS["adequate"],
                "warrant_digests": [
                    canonical_digest(view[alias][dimension]["warrants"])
                    for view in finding_by_report
                ],
            }
        floor_vectors[alias] = floor_vector
        if clears:
            qualified.append(alias)
        consensus_rows.append(
            {
                "candidate_alias": alias,
                "system_id": candidate_bindings[alias],
                "dimensions": dimension_rows,
                "clears_noncompensatory_floor": clears,
            }
        )
    nondominated = [
        alias
        for alias in aliases
        if not any(
            other != alias and _dominates(floor_vectors[other], floor_vectors[alias])
            for other in aliases
        )
    ]
    dominance_witnesses = []
    for alias in aliases:
        dominators = sorted(
            other
            for other in aliases
            if other != alias and _dominates(floor_vectors[other], floor_vectors[alias])
        )
        if not dominators:
            continue
        witness = {
            "dominated_candidate_alias": alias,
            "dominating_candidate_aliases": dominators,
            "strict_dimensions": sorted(
                {
                    dimension
                    for other in dominators
                    for dimension in DIMENSIONS
                    if floor_vectors[other][dimension] > floor_vectors[alias][dimension]
                }
            ),
        }
        witness["witness_digest"] = canonical_digest(witness)
        dominance_witnesses.append(witness)
    eligible = sorted(set(qualified) & set(nondominated))
    selected_alias = eligible[0] if len(eligible) == 1 else None
    if selected_alias:
        decision = "prefer_unique"
    elif eligible:
        decision = "retain_plural_nondominated"
    else:
        decision = "revise_all"

    comparison: dict[str, Any] | None = None
    if previous is not None:
        if previous_packet is None:
            raise ContractError("stage comparison requires the previous blind packet")
        prior_selected = previous.get("selected_system_id")
        selected_system = candidate_bindings.get(selected_alias) if selected_alias else None
        semantic_patch = _build_semantic_patch(
            packet=packet,
            previous_packet=previous_packet,
            previous=previous,
            selected_alias=selected_alias,
            selected_system=selected_system,
        )
        new_rounds = len(semantic_patch["new_round_aliases"])
        current_consensus = next(
            (row for row in consensus_rows if row["candidate_alias"] == selected_alias),
            None,
        )
        previous_consensus = next(
            (
                row
                for row in previous.get("candidate_consensus", [])
                if row.get("system_id") == selected_system
            ),
            None,
        )
        resilience_increased = False
        nondegrading_floors = False
        improved_dimensions: list[str] = []
        if current_consensus and previous_consensus:
            current_values = {
                dimension: RATINGS[
                    current_consensus["dimensions"][dimension]["minimum_rating"]
                ]
                for dimension in DIMENSIONS
            }
            previous_values = {
                dimension: RATINGS[
                    previous_consensus["dimensions"][dimension]["minimum_rating"]
                ]
                for dimension in DIMENSIONS
            }
            nondegrading_floors = all(
                current_values[dimension] >= previous_values[dimension]
                for dimension in DIMENSIONS
            )
            improved_dimensions = [
                dimension
                for dimension in DIMENSIONS
                if current_values[dimension] > previous_values[dimension]
            ]
            resilience_increased = "reflective_resilience" in improved_dimensions
        objection_linked_change = (
            semantic_patch["content_changed"]
            and semantic_patch["all_changes_objection_linked"]
            and bool(semantic_patch["objection_links"])
            and semantic_patch["component_digests"]["objections"]["changed"]
            and semantic_patch["component_digests"]["corrections"]["changed"]
        )
        material = (
            selected_system is not None
            and selected_system == prior_selected
            and new_rounds > 0
            and semantic_patch["round_history_prefix_preserved"]
            and objection_linked_change
            and nondegrading_floors
            and resilience_increased
        )
        comparison = {
            "applicability": "applicable",
            "prior_adjudication_id": previous.get("adjudication_id"),
            "prior_selected_system_id": prior_selected,
            "current_selected_system_id": selected_system,
            "new_reflection_rounds": new_rounds,
            "round_history_prefix_preserved": semantic_patch[
                "round_history_prefix_preserved"
            ],
            "reflective_resilience_increased": resilience_increased,
            "nondegrading_dimension_floors": nondegrading_floors,
            "improved_dimensions": improved_dimensions,
            "semantic_patch": semantic_patch,
            "material": material,
            "reason": (
                "a new objection-bearing round is exactly linked to a nondegrading content patch and increased reflective resilience"
                if material
                else "selection continuity, round history, exact objection-linked content change, nondegradation, or resilience improvement was not established"
            ),
        }

    preference_system_ids = sorted(candidate_bindings[alias] for alias in eligible)
    preference_set_core = {
        "decision": decision,
        "preferred_candidate_aliases": eligible,
        "preferred_system_ids": preference_system_ids,
        "nondominated_candidate_aliases": sorted(nondominated),
        "nondominated_system_ids": sorted(
            candidate_bindings[alias] for alias in nondominated
        ),
    }
    core = {
        "schema_version": "2.0.0",
        "target_id": packet["target_id"],
        "stage_id": packet["stage_id"],
        "blind_packet_digest": packet["blind_packet_digest"],
        "candidate_bindings_digest": canonical_digest(dict(candidate_bindings)),
        "report_ids": [report["report_id"] for report in reports],
        "candidate_consensus": consensus_rows,
        "nondominated_candidate_aliases": sorted(nondominated),
        "qualified_candidate_aliases": eligible,
        "preferred_candidate_aliases": eligible,
        "preferred_system_ids": preference_system_ids,
        "dominance_witnesses": dominance_witnesses,
        "preference_set_digest": canonical_digest(preference_set_core),
        "selected_candidate_alias": selected_alias,
        "selected_system_id": candidate_bindings.get(selected_alias) if selected_alias else None,
        "decision": decision,
        "authority": {
            "blind_to_preferred_answer": True,
            "content_warrants_verified": True,
            **panel_authority,
            "conceptual_preference_authorized": bool(eligible),
            "claim_scope": "internal_target_specific_conceptual_preference",
            "external_human_evidence_available": False,
            "external_human_evidence_status": "unavailable",
            "external_generalization_authorized": False,
        },
        "authority_boundary": (
            "This is a reproducible internal, target-specific, content-warranted conceptual preference from "
            + (
                "pairwise authority-distinct internal judges. "
                if panel_authority["plural_independent_perspectives"]
                else "an explicitly correlated internal critic panel. "
            )
            + "External human evidence is unavailable; this is not empirical efficacy evidence, mathematical proof, or truth authority."
        ),
        "created_at": created_at or utc_now(),
    }
    if comparison is not None:
        core["stage_comparison"] = comparison
    core["adjudication_id"] = stable_identifier(
        "conceptual-adjudication",
        core["target_id"],
        core["stage_id"],
        core["blind_packet_digest"],
        core["report_ids"],
    )
    core["adjudication_digest"] = canonical_digest(
        core, exclude_keys=("adjudication_digest", "created_at")
    )
    validate_instance(core, "conceptual_adjudication.schema.json")
    return core


def _substantive_string_list(value: Any, *, minimum: int = 1) -> list[str]:
    if not isinstance(value, list):
        return []
    rows = [str(item) for item in value if isinstance(item, str) and _meaningful(item, 4)]
    return rows if len(rows) >= minimum else []


def _graph_members(value: Any, field: str) -> list[Any]:
    if not isinstance(value, Mapping) or not isinstance(value.get(field), list):
        return []
    return list(value[field])


def _exact_multiset_difference(after: Sequence[Any], before: Sequence[Any]) -> list[Any]:
    """Return a deterministic canonical multiset difference."""

    remaining = Counter(canonical_digest(item) for item in before)
    rows: list[Any] = []
    for item in after:
        digest = canonical_digest(item)
        if remaining[digest]:
            remaining[digest] -= 1
        else:
            rows.append(copy.deepcopy(item))
    return sorted(rows, key=canonical_digest)


def _closed_fields(
    value: Mapping[str, Any], expected: frozenset[str], *, label: str
) -> None:
    """Reject both missing and invented fields in semantic graph records."""

    observed = set(value)
    if observed != expected:
        _adjudication_fail(
            "adjudication_unification_graph_open",
            f"{label} fields are not closed; missing={sorted(expected - observed)} "
            f"unknown={sorted(observed - expected)}",
        )


def _content_paths(
    system: Mapping[str, Any], value: Any, *, label: str
) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(item, str) and item.startswith("/") for item in value)
        or len(set(value)) != len(value)
    ):
        _adjudication_fail(
            "adjudication_unification_graph_open",
            f"{label} requires distinct absolute content paths",
        )
    paths = [str(item) for item in value]
    for path in paths:
        try:
            _pointer(system, path)
        except ContractError as exc:
            _adjudication_fail("adjudication_unification_graph_open", str(exc))
    return paths


def _typed_explanatory_graph(
    system: Mapping[str, Any], graph: Any, *, graph_label: str
) -> dict[str, Any]:
    """Validate one finite explanatory graph as a closed typed structure."""

    if not isinstance(graph, Mapping) or set(graph) != {"nodes", "edges"}:
        _adjudication_fail(
            "adjudication_unification_graph_open",
            f"{graph_label} must contain exactly nodes and edges",
        )
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or not nodes or not isinstance(edges, list):
        _adjudication_fail(
            "adjudication_unification_graph_open",
            f"{graph_label} requires a nonempty node list and an edge list",
        )

    nodes_by_id: dict[str, dict[str, Any]] = {}
    for index, raw_node in enumerate(nodes, 1):
        if not isinstance(raw_node, Mapping):
            _adjudication_fail(
                "adjudication_unification_graph_open",
                f"{graph_label} node {index} is malformed",
            )
        _closed_fields(raw_node, _GRAPH_NODE_FIELDS, label=f"{graph_label} node {index}")
        node_id = str(raw_node.get("node_id", ""))
        if not _IDENTIFIER.fullmatch(node_id) or node_id in nodes_by_id:
            _adjudication_fail(
                "adjudication_unification_graph_open",
                f"{graph_label} has a missing, invalid, or duplicate node identity",
            )
        if raw_node.get("node_kind") not in UNIFICATION_NODE_KINDS:
            _adjudication_fail(
                "adjudication_unification_graph_open",
                f"{graph_label} node {node_id!r} has an unknown node kind",
            )
        if not _meaningful(raw_node.get("label"), 2):
            _adjudication_fail(
                "adjudication_unification_graph_open",
                f"{graph_label} node {node_id!r} lacks a substantive label",
            )
        _content_paths(
            system,
            raw_node.get("content_paths"),
            label=f"{graph_label} node {node_id!r}",
        )
        nodes_by_id[node_id] = copy.deepcopy(dict(raw_node))

    edges_by_id: dict[str, dict[str, Any]] = {}
    relation_kinds: set[str] = set()
    for index, raw_edge in enumerate(edges, 1):
        if not isinstance(raw_edge, Mapping):
            _adjudication_fail(
                "adjudication_unification_graph_open",
                f"{graph_label} edge {index} is malformed",
            )
        _closed_fields(raw_edge, _GRAPH_EDGE_FIELDS, label=f"{graph_label} edge {index}")
        edge_id = str(raw_edge.get("edge_id", ""))
        if not _IDENTIFIER.fullmatch(edge_id) or edge_id in edges_by_id:
            _adjudication_fail(
                "adjudication_unification_graph_open",
                f"{graph_label} has a missing, invalid, or duplicate edge identity",
            )
        source = str(raw_edge.get("source_node_id", ""))
        target = str(raw_edge.get("target_node_id", ""))
        if source not in nodes_by_id or target not in nodes_by_id:
            _adjudication_fail(
                "adjudication_unification_graph_dangling_edge",
                f"{graph_label} edge {edge_id!r} has an endpoint outside the graph",
            )
        relation_kind = str(raw_edge.get("relation_kind", ""))
        if relation_kind not in UNIFICATION_RELATION_KINDS:
            _adjudication_fail(
                "adjudication_unification_relation_unknown",
                f"{graph_label} edge {edge_id!r} has an unknown relation kind",
            )
        if not _meaningful(raw_edge.get("statement"), 4):
            _adjudication_fail(
                "adjudication_unification_graph_open",
                f"{graph_label} edge {edge_id!r} lacks explanatory content",
            )
        _content_paths(
            system,
            raw_edge.get("warrant_paths"),
            label=f"{graph_label} edge {edge_id!r}",
        )
        relation_kinds.add(relation_kind)
        edges_by_id[edge_id] = copy.deepcopy(dict(raw_edge))
    return {
        "nodes_by_id": nodes_by_id,
        "edges_by_id": edges_by_id,
        "relation_kinds": relation_kinds,
    }


def _typed_unification_assessment(system: Mapping[str, Any]) -> dict[str, Any]:
    """Validate unification as a typed explanatory graph transition."""

    system_id = str(system.get("system_id", ""))
    unification = system.get("unification_claims")
    if not isinstance(unification, Mapping):
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} lacks typed unification claims",
        )
    kind = str(unification.get("unification_kind", ""))
    if kind not in UNIFICATION_KINDS:
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} has no supported unification kind",
        )
    source_case_ids = unification.get("source_case_ids")
    if (
        not isinstance(source_case_ids, list)
        or len(source_case_ids) < 2
        or not all(isinstance(item, str) and item for item in source_case_ids)
        or len(set(source_case_ids)) != len(source_case_ids)
    ):
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} must name at least two distinct source cases",
        )
    source_set = set(source_case_ids)
    mediator = unification.get("mediator")
    if (
        not isinstance(mediator, Mapping)
        or not _meaningful(mediator.get("statement"), 6)
        or not _substantive_string_list(mediator.get("primitive_refs"))
        or not _substantive_string_list(mediator.get("relation_refs"))
        or not isinstance(mediator.get("node_ids"), list)
        or not mediator.get("node_ids")
    ):
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} lacks a typed, substantive mediator",
        )

    mappings = unification.get("mappings")
    if not isinstance(mappings, list) or len(mappings) < 2:
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} lacks explicit bridge mappings",
        )
    mapped_sources: set[str] = set()
    mapping_ids: set[str] = set()
    for index, mapping in enumerate(mappings, 1):
        if not isinstance(mapping, Mapping):
            _adjudication_fail(
                "adjudication_unification_untyped",
                f"conceptual system {system_id!r} mapping {index} is malformed",
            )
        _closed_fields(mapping, _MAPPING_FIELDS, label=f"mapping {index}")
        mapping_id = str(mapping.get("mapping_id", ""))
        if not _IDENTIFIER.fullmatch(mapping_id) or mapping_id in mapping_ids:
            _adjudication_fail(
                "adjudication_unification_untyped",
                f"conceptual system {system_id!r} has a duplicate or invalid mapping ID",
            )
        source_case_id = str(mapping.get("source_case_id", ""))
        if source_case_id not in source_set:
            _adjudication_fail(
                "adjudication_unification_untyped",
                f"conceptual system {system_id!r} mapping {index} has an unknown source case",
            )
        if (
            not _meaningful(mapping.get("bridge_statement"), 6)
            or not str(mapping.get("target_node_id", "")).strip()
            or mapping.get("map_kind") not in UNIFICATION_MAPPING_KINDS
        ):
            _adjudication_fail(
                "adjudication_unification_untyped",
                f"conceptual system {system_id!r} mapping {index} lacks bridge semantics",
            )
        warrant_paths = mapping.get("warrant_paths", [])
        if not isinstance(warrant_paths, list) or not warrant_paths:
            _adjudication_fail(
                "adjudication_unification_untyped",
                f"conceptual system {system_id!r} mapping {index} lacks content warrants",
            )
        for path in warrant_paths:
            try:
                _pointer(system, str(path))
            except ContractError as exc:
                _adjudication_fail("adjudication_unification_untyped", str(exc))
        mapped_sources.add(source_case_id)
        mapping_ids.add(mapping_id)
    if mapped_sources != source_set:
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} does not map every source case",
        )

    differences = unification.get("preserved_differences")
    if not isinstance(differences, list) or not differences:
        _adjudication_fail(
            "adjudication_unification_erases_difference",
            f"conceptual system {system_id!r} records no preserved differences",
        )
    difference_coverage: set[str] = set()
    difference_ids: set[str] = set()
    for index, difference in enumerate(differences, 1):
        if not isinstance(difference, Mapping):
            _adjudication_fail(
                "adjudication_unification_erases_difference",
                f"conceptual system {system_id!r} difference {index} is malformed",
            )
        _closed_fields(difference, _DIFFERENCE_FIELDS, label=f"difference {index}")
        difference_id = str(difference.get("difference_id", ""))
        if not _IDENTIFIER.fullmatch(difference_id) or difference_id in difference_ids:
            _adjudication_fail(
                "adjudication_unification_erases_difference",
                f"conceptual system {system_id!r} has a duplicate or invalid difference ID",
            )
        source_ids = difference.get("source_case_ids")
        if (
            not isinstance(source_ids, list)
            or not source_ids
            or not set(source_ids).issubset(source_set)
            or not _meaningful(difference.get("statement"), 6)
        ):
            _adjudication_fail(
                "adjudication_unification_erases_difference",
                f"conceptual system {system_id!r} difference {index} is not source-bound",
            )
        witness_paths = difference.get("preservation_witness_paths")
        if not isinstance(witness_paths, list) or not witness_paths:
            _adjudication_fail(
                "adjudication_unification_erases_difference",
                f"conceptual system {system_id!r} difference {index} lacks a preservation witness",
            )
        for path in witness_paths:
            try:
                _pointer(system, str(path))
            except ContractError as exc:
                _adjudication_fail(
                    "adjudication_unification_erases_difference", str(exc)
                )
        difference_coverage.update(str(item) for item in source_ids)
        difference_ids.add(difference_id)
    if difference_coverage != source_set:
        _adjudication_fail(
            "adjudication_unification_erases_difference",
            f"conceptual system {system_id!r} does not preserve a distinction for every source case",
        )

    transition = unification.get("explanatory_graph_transition")
    if not isinstance(transition, Mapping):
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} lacks an explanatory graph transition",
        )
    before_graph = transition.get("before_graph")
    after_graph = transition.get("after_graph")
    if not isinstance(before_graph, Mapping) or not isinstance(after_graph, Mapping):
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} graph transition lacks before/after graphs",
        )
    before_typed = _typed_explanatory_graph(
        system, before_graph, graph_label=f"{system_id} before graph"
    )
    after_typed = _typed_explanatory_graph(
        system, after_graph, graph_label=f"{system_id} after graph"
    )
    for node_id, before_node in before_typed["nodes_by_id"].items():
        if after_typed["nodes_by_id"].get(node_id) != before_node:
            _adjudication_fail(
                "adjudication_unification_graph_open",
                f"conceptual system {system_id!r} changes or drops preexisting node {node_id!r}",
            )
    for edge_id, before_edge in before_typed["edges_by_id"].items():
        if after_typed["edges_by_id"].get(edge_id) != before_edge:
            _adjudication_fail(
                "adjudication_unification_graph_open",
                f"conceptual system {system_id!r} changes or drops preexisting edge {edge_id!r}",
            )
    after_nodes = after_typed["nodes_by_id"]
    after_edges = after_typed["edges_by_id"]
    for source_case_id in source_case_ids:
        if after_nodes.get(source_case_id, {}).get("node_kind") != "source_case":
            _adjudication_fail(
                "adjudication_unification_graph_open",
                f"conceptual system {system_id!r} source case {source_case_id!r} is not a typed graph node",
            )
    for mediator_node_id in mediator["node_ids"]:
        if after_nodes.get(str(mediator_node_id), {}).get("node_kind") != "mediator":
            _adjudication_fail(
                "adjudication_unification_graph_open",
                f"conceptual system {system_id!r} mediator node {mediator_node_id!r} is not typed",
            )
    for mapping in mappings:
        if str(mapping["target_node_id"]) not in after_nodes:
            _adjudication_fail(
                "adjudication_unification_graph_dangling_edge",
                f"conceptual system {system_id!r} mapping target is outside the graph",
            )
    for difference in differences:
        witness_nodes = difference.get("witness_node_ids")
        witness_edges = difference.get("witness_edge_ids")
        if (
            not isinstance(witness_nodes, list)
            or not isinstance(witness_edges, list)
            or not witness_nodes
            or len(set(witness_nodes)) != len(witness_nodes)
            or len(set(witness_edges)) != len(witness_edges)
            or not set(difference["source_case_ids"]).issubset(set(witness_nodes))
            or not set(witness_nodes).issubset(after_nodes)
            or not set(witness_edges).issubset(after_edges)
        ):
            _adjudication_fail(
                "adjudication_unification_erases_difference",
                f"conceptual system {system_id!r} difference {difference['difference_id']!r} has an open witness",
            )
    before_digest = canonical_digest(dict(before_graph))
    after_digest = canonical_digest(dict(after_graph))
    if (
        transition.get("before_graph_digest") != before_digest
        or transition.get("after_graph_digest") != after_digest
    ):
        _adjudication_fail(
            "adjudication_digest_mismatch",
            f"conceptual system {system_id!r} graph-transition digest mismatch",
        )
    if before_digest == after_digest:
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} claims unification without an explanatory graph change",
        )
    expected_added_nodes = _exact_multiset_difference(
        _graph_members(after_graph, "nodes"), _graph_members(before_graph, "nodes")
    )
    expected_added_edges = _exact_multiset_difference(
        _graph_members(after_graph, "edges"), _graph_members(before_graph, "edges")
    )
    if sorted(transition.get("added_nodes", []), key=canonical_digest) != expected_added_nodes:
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} added-node delta is not exact",
        )
    if sorted(transition.get("added_edges", []), key=canonical_digest) != expected_added_edges:
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} added-edge delta is not exact",
        )
    if not _substantive_string_list(
        transition.get("new_explanatory_dependencies")
    ):
        _adjudication_fail(
            "adjudication_unification_untyped",
            f"conceptual system {system_id!r} graph transition adds no explanatory dependency",
        )
    for field in (
        "scope_conditions",
        "transfer_obligations",
        "erasure_risks",
        "failure_conditions",
    ):
        if not _substantive_string_list(unification.get(field)):
            _adjudication_fail(
                "adjudication_unification_untyped",
                f"conceptual system {system_id!r} lacks substantive {field}",
            )
    return {
        "system_id": system_id,
        "unification_kind": kind,
        "source_case_ids": sorted(source_set),
        "covered_source_case_ids": sorted(mapped_sources & difference_coverage),
        "mapping_ids": sorted(mapping_ids),
        "difference_ids": sorted(difference_ids),
        "node_ids": sorted(after_nodes),
        "edge_ids": sorted(after_edges),
        "relation_kinds": sorted(after_typed["relation_kinds"]),
        "unification_digest": canonical_digest(dict(unification)),
        "before_graph_digest": before_digest,
        "after_graph_digest": after_digest,
        "graph_closed": True,
        "valid": True,
    }


def _typed_unification_closure(
    systems: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    assessments = [
        _typed_unification_assessment(system)
        for system in sorted(systems, key=lambda row: str(row.get("system_id", "")))
    ]
    core = {"schema_version": "1.0.0", "assessments": assessments}
    return {**core, "closure_digest": canonical_digest(core)}


def _candidate_set_digest(
    systems: Sequence[Mapping[str, Any]], signature_closure: Mapping[str, Any]
) -> str:
    signatures = {
        str(row["system_id"]): row["semantic_signature"]["signature_digest"]
        for row in signature_closure.get("candidate_signatures", [])
    }
    return canonical_digest(
        [
            {
                "system_id": str(system["system_id"]),
                "system_digest": canonical_digest(dict(system)),
                "semantic_signature_digest": signatures[str(system["system_id"])],
            }
            for system in sorted(systems, key=lambda row: str(row["system_id"]))
        ]
    )


def build_adjudication_source_bindings(
    *,
    run_id: str,
    state_version: int,
    theory_state_digest: str,
    literature_snapshot_digest: str,
    high_risk_portfolio_digest: str,
    systems: Sequence[Mapping[str, Any]],
    reflection_rounds: Sequence[Mapping[str, Any]],
    frozen_genealogy: Sequence[Mapping[str, Any]],
    proposer_receipt_ids: Sequence[str],
) -> dict[str, Any]:
    """Build the exact source binding that a blind packet must expose."""

    signatures = semantic_signature_closure(systems, frozen_genealogy)
    return {
        "run_id": run_id,
        "state_version": state_version,
        "theory_state_digest": theory_state_digest,
        "literature_snapshot_digest": literature_snapshot_digest,
        "high_risk_portfolio_digest": high_risk_portfolio_digest,
        "conceptual_systems_digest": canonical_digest([dict(row) for row in systems]),
        "reflection_rounds_digest": canonical_digest(
            [dict(row) for row in reflection_rounds]
        ),
        "frozen_genealogy_digest": canonical_digest(
            [dict(row) for row in frozen_genealogy]
        ),
        "candidate_set_digest": _candidate_set_digest(systems, signatures),
        "proposer_receipt_ids": sorted(set(str(item) for item in proposer_receipt_ids)),
    }


def _panel_seal(
    packet: Mapping[str, Any], reports: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    ordered = sorted(reports, key=lambda row: str(row["report_id"]))
    core = {
        "schema_version": "1.0.0",
        "blind_packet_digest": packet["blind_packet_digest"],
        "report_ids": [str(row["report_id"]) for row in ordered],
        "report_digests": [str(row["report_digest"]) for row in ordered],
        "lens_families": sorted(
            {str(row["adjudicator"]["lens_family"]) for row in ordered}
        ),
        "sealed": True,
    }
    return {**core, "panel_seal_digest": canonical_digest(core)}


def _unblinding_receipt(
    panel_seal: Mapping[str, Any], candidate_bindings: Mapping[str, str]
) -> dict[str, Any]:
    rows = [
        {"candidate_alias": alias, "system_id": str(candidate_bindings[alias])}
        for alias in sorted(candidate_bindings)
    ]
    core = {
        "schema_version": "1.0.0",
        "panel_seal_digest": panel_seal["panel_seal_digest"],
        "candidate_bindings": rows,
        "candidate_bindings_digest": canonical_digest(rows),
        "post_seal_unblinding": True,
    }
    return {**core, "receipt_digest": canonical_digest(core)}


def _preference_set(
    adjudication: Mapping[str, Any], candidate_bindings: Mapping[str, str]
) -> dict[str, Any]:
    preferred_aliases = sorted(adjudication.get("preferred_candidate_aliases", []))
    nondominated_aliases = sorted(
        adjudication.get("nondominated_candidate_aliases", [])
    )
    core = {
        "decision": adjudication["decision"],
        "preferred_candidate_aliases": preferred_aliases,
        "preferred_system_ids": sorted(
            str(candidate_bindings[alias]) for alias in preferred_aliases
        ),
        "nondominated_candidate_aliases": nondominated_aliases,
        "nondominated_system_ids": sorted(
            str(candidate_bindings[alias]) for alias in nondominated_aliases
        ),
    }
    return {**core, "preference_set_digest": canonical_digest(core)}


def _validate_blind_packet_binding(
    *,
    packet: Mapping[str, Any],
    systems: Sequence[Mapping[str, Any]],
    reflection_rounds: Sequence[Mapping[str, Any]],
    candidate_bindings: Mapping[str, str],
    expected_source_bindings: Mapping[str, Any],
    target_id: str,
    stage_id: str,
) -> None:
    unsigned = {key: value for key, value in packet.items() if key != "blind_packet_digest"}
    if packet.get("blind_packet_digest") != canonical_digest(unsigned):
        _adjudication_fail(
            "adjudication_digest_mismatch", "blind packet digest mismatch"
        )
    if packet.get("target_id") != target_id or packet.get("stage_id") != stage_id:
        _adjudication_fail(
            "adjudication_input_binding_mismatch",
            "blind packet crossed its target or stage",
        )
    if dict(packet.get("source_bindings", {})) != dict(expected_source_bindings):
        _adjudication_fail(
            "adjudication_input_binding_mismatch",
            "blind packet source bindings do not equal the frozen adjudication inputs",
        )
    aliases = [str(row.get("candidate_alias", "")) for row in packet.get("candidates", [])]
    if (
        set(candidate_bindings) != set(aliases)
        or len(set(candidate_bindings.values())) != len(aliases)
        or set(candidate_bindings.values())
        != {str(system.get("system_id", "")) for system in systems}
    ):
        _adjudication_fail(
            "adjudication_candidate_set_mismatch",
            "candidate unblinding is not an exact system-set bijection",
        )
    aliases_by_system = {
        str(system_id): str(alias) for alias, system_id in candidate_bindings.items()
    }
    packet_by_alias = {
        str(row["candidate_alias"]): row for row in packet.get("candidates", [])
    }
    for system in systems:
        system_id = str(system["system_id"])
        alias = aliases_by_system[system_id]
        expected_content = _blind_project(dict(system), aliases_by_system)
        actual = packet_by_alias.get(alias)
        if (
            actual is None
            or actual.get("content") != expected_content
            or actual.get("content_digest") != canonical_digest(expected_content)
        ):
            _adjudication_fail(
                "adjudication_candidate_content_mismatch",
                f"blind candidate content does not bind conceptual system {system_id}",
            )
    expected_rounds = []
    for index, row in enumerate(reflection_rounds, 1):
        content = _blind_project(dict(row), aliases_by_system)
        expected_rounds.append(
            {
                "round_alias": f"reflection-{index:02d}",
                "content": content,
                "content_digest": canonical_digest(content),
            }
        )
    if packet.get("reflection_rounds") != expected_rounds:
        _adjudication_fail(
            "adjudication_candidate_content_mismatch",
            "blind reflection rounds do not equal the frozen reflection input",
        )
    leak = _find_blind_leak(packet, raw_markers=list(aliases_by_system))
    if leak:
        _adjudication_fail("adjudication_blindness_violation", leak)


def _previous_adjudication_parts(
    previous_evidence: Mapping[str, Any] | None,
) -> tuple[Mapping[str, Any] | None, Mapping[str, Any] | None, str | None]:
    if previous_evidence is None:
        return None, None, None
    expected = canonical_digest(
        previous_evidence, exclude_keys=("evidence_digest", "created_at")
    )
    if previous_evidence.get("evidence_digest") != expected:
        _adjudication_fail(
            "adjudication_digest_mismatch", "previous adjudication evidence digest mismatch"
        )
    adjudication = previous_evidence.get("content_adjudication")
    packet = previous_evidence.get("blind_packet")
    if not isinstance(adjudication, Mapping) or not isinstance(packet, Mapping):
        _adjudication_fail(
            "adjudication_input_binding_mismatch",
            "previous evidence lacks its adjudication or blind packet",
        )
    return adjudication, packet, str(previous_evidence["evidence_digest"])


def build_adjudication_evidence(
    *,
    packet: Mapping[str, Any],
    reports: Sequence[Mapping[str, Any]],
    candidate_bindings: Mapping[str, str],
    systems: Sequence[Mapping[str, Any]],
    reflection_rounds: Sequence[Mapping[str, Any]],
    frozen_genealogy: Sequence[Mapping[str, Any]],
    run_id: str,
    state_version: int,
    theory_state_digest: str,
    literature_snapshot_digest: str,
    high_risk_portfolio_digest: str,
    proposer_receipt_ids: Sequence[str],
    previous_evidence: Mapping[str, Any] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Seal one blind panel, unblind only after sealing, and derive its preference set."""

    ordered_reports = sorted(
        (copy.deepcopy(dict(row)) for row in reports),
        key=lambda row: str(row["report_id"]),
    )
    for report in ordered_reports:
        validate_judge_report(report, packet)
    _validate_deep_lens_panel(packet, ordered_reports)
    signatures = semantic_signature_closure(systems, frozen_genealogy)
    unification = _typed_unification_closure(systems)
    source_bindings = build_adjudication_source_bindings(
        run_id=run_id,
        state_version=state_version,
        theory_state_digest=theory_state_digest,
        literature_snapshot_digest=literature_snapshot_digest,
        high_risk_portfolio_digest=high_risk_portfolio_digest,
        systems=systems,
        reflection_rounds=reflection_rounds,
        frozen_genealogy=frozen_genealogy,
        proposer_receipt_ids=proposer_receipt_ids,
    )
    _validate_blind_packet_binding(
        packet=packet,
        systems=systems,
        reflection_rounds=reflection_rounds,
        candidate_bindings=candidate_bindings,
        expected_source_bindings=source_bindings,
        target_id=str(packet["target_id"]),
        stage_id=str(packet["stage_id"]),
    )
    seal = _panel_seal(packet, ordered_reports)
    unblinding = _unblinding_receipt(seal, candidate_bindings)
    previous_adjudication, previous_packet, previous_digest = _previous_adjudication_parts(
        previous_evidence
    )
    timestamp = created_at or utc_now()
    adjudication = aggregate_adjudication(
        packet,
        ordered_reports,
        candidate_bindings=candidate_bindings,
        previous=previous_adjudication,
        previous_packet=previous_packet,
        created_at=timestamp,
    )
    preference = _preference_set(adjudication, candidate_bindings)
    input_binding = {
        "theory_state_digest": theory_state_digest,
        "literature_snapshot_digest": literature_snapshot_digest,
        "high_risk_portfolio_digest": high_risk_portfolio_digest,
        "conceptual_systems_digest": source_bindings["conceptual_systems_digest"],
        "reflection_rounds_digest": source_bindings["reflection_rounds_digest"],
        "frozen_genealogy_digest": source_bindings["frozen_genealogy_digest"],
        "candidate_set_digest": source_bindings["candidate_set_digest"],
        "semantic_signature_closure_digest": signatures["closure_digest"],
        "blind_packet_digest": packet["blind_packet_digest"],
        "proposer_receipt_ids": source_bindings["proposer_receipt_ids"],
        "previous_evidence_digest": previous_digest,
    }
    core = {
        "schema_version": "3.0.0",
        "evidence_id": stable_identifier(
            "conceptual-adjudication-evidence",
            packet["target_id"],
            run_id,
            state_version,
            packet["stage_id"],
            seal["panel_seal_digest"],
        ),
        "target_id": packet["target_id"],
        "run_id": run_id,
        "state_version": state_version,
        "stage_id": packet["stage_id"],
        "input_binding": input_binding,
        "blind_packet": copy.deepcopy(dict(packet)),
        "judge_reports": ordered_reports,
        "panel_seal": seal,
        "unblinding_receipt": unblinding,
        "semantic_signature_closure": signatures,
        "typed_unification_closure": unification,
        "content_adjudication": adjudication,
        "preference_set": preference,
        "authority": {
            "sole_conceptual_preference_authority": True,
            "blind_panel_sealed_before_unblinding": True,
            "semantic_signatures_recomputed": True,
            "typed_unification_recomputed": True,
            "deep_lens_floor_met": True,
            "structural_scores_authorize_preference": False,
        },
        "authority_boundary": (
            "This receipt authorizes only an internal target-specific, set-valued conceptual preference. "
            "Structural scores, generator priors, experiments, proof status, and source prestige grant no preference."
        ),
        "created_at": timestamp,
    }
    core["evidence_digest"] = canonical_digest(
        core, exclude_keys=("evidence_digest", "created_at")
    )
    validate_adjudication_evidence(
        core,
        systems=systems,
        reflection_rounds=reflection_rounds,
        frozen_genealogy=frozen_genealogy,
        candidate_bindings=candidate_bindings,
        theory_state_digest=theory_state_digest,
        literature_snapshot_digest=literature_snapshot_digest,
        high_risk_portfolio_digest=high_risk_portfolio_digest,
        proposer_receipt_ids=proposer_receipt_ids,
        previous_evidence=previous_evidence,
    )
    return core


def validate_adjudication_evidence(
    evidence: Mapping[str, Any],
    *,
    systems: Sequence[Mapping[str, Any]],
    reflection_rounds: Sequence[Mapping[str, Any]],
    frozen_genealogy: Sequence[Mapping[str, Any]],
    candidate_bindings: Mapping[str, str],
    theory_state_digest: str,
    literature_snapshot_digest: str,
    high_risk_portfolio_digest: str,
    proposer_receipt_ids: Sequence[str],
    previous_evidence: Mapping[str, Any] | None = None,
) -> None:
    """Recompute the sealed panel, unblinding, semantics, unification, and preference."""

    expected_evidence_digest = canonical_digest(
        evidence, exclude_keys=("evidence_digest", "created_at")
    )
    if evidence.get("evidence_digest") != expected_evidence_digest:
        _adjudication_fail(
            "adjudication_digest_mismatch", "adjudication evidence digest mismatch"
        )
    packet = evidence.get("blind_packet")
    reports = evidence.get("judge_reports")
    if not isinstance(packet, Mapping) or not isinstance(reports, list):
        _adjudication_fail(
            "adjudication_evidence_missing",
            "adjudication evidence lacks its blind packet or judge reports",
        )
    for report in reports:
        try:
            validate_judge_report(report, packet)
        except ContractError as exc:
            _adjudication_fail("adjudication_judge_report_invalid", str(exc))
    _validate_deep_lens_panel(packet, reports)
    try:
        validate_instance(dict(evidence), "conceptual_adjudication_evidence.schema.json")
    except ContractError as exc:
        _adjudication_fail("adjudication_schema_invalid", str(exc))

    # Validate the typed explanatory claim before its derived whole-system
    # signature.  Otherwise a precise erasure/dangling-edge defect is obscured
    # by the necessarily broader semantic-closure mismatch it also causes.
    unification = _typed_unification_closure(systems)
    if evidence.get("typed_unification_closure") != unification:
        _adjudication_fail(
            "adjudication_unification_untyped",
            "typed unification closure does not recompute from conceptual systems",
        )
    signatures = semantic_signature_closure(systems, frozen_genealogy)
    if evidence.get("semantic_signature_closure") != signatures:
        _adjudication_fail(
            "adjudication_semantic_signature_mismatch",
            "semantic signature closure does not recompute from candidates and genealogy",
        )
    source_bindings = build_adjudication_source_bindings(
        run_id=str(evidence.get("run_id", "")),
        state_version=int(evidence.get("state_version", -1)),
        theory_state_digest=theory_state_digest,
        literature_snapshot_digest=literature_snapshot_digest,
        high_risk_portfolio_digest=high_risk_portfolio_digest,
        systems=systems,
        reflection_rounds=reflection_rounds,
        frozen_genealogy=frozen_genealogy,
        proposer_receipt_ids=proposer_receipt_ids,
    )
    _validate_blind_packet_binding(
        packet=packet,
        systems=systems,
        reflection_rounds=reflection_rounds,
        candidate_bindings=candidate_bindings,
        expected_source_bindings=source_bindings,
        target_id=str(evidence.get("target_id", "")),
        stage_id=str(evidence.get("stage_id", "")),
    )
    expected_seal = _panel_seal(packet, reports)
    if evidence.get("panel_seal") != expected_seal:
        _adjudication_fail(
            "adjudication_panel_unsealed",
            "panel seal does not bind the complete blind report set",
        )
    expected_unblinding = _unblinding_receipt(expected_seal, candidate_bindings)
    if evidence.get("unblinding_receipt") != expected_unblinding:
        _adjudication_fail(
            "adjudication_unblinding_order_invalid",
            "unblinding receipt is not a post-panel-seal binding",
        )
    previous_adjudication, previous_packet, previous_digest = _previous_adjudication_parts(
        previous_evidence
    )
    expected_input = {
        "theory_state_digest": theory_state_digest,
        "literature_snapshot_digest": literature_snapshot_digest,
        "high_risk_portfolio_digest": high_risk_portfolio_digest,
        "conceptual_systems_digest": source_bindings["conceptual_systems_digest"],
        "reflection_rounds_digest": source_bindings["reflection_rounds_digest"],
        "frozen_genealogy_digest": source_bindings["frozen_genealogy_digest"],
        "candidate_set_digest": source_bindings["candidate_set_digest"],
        "semantic_signature_closure_digest": signatures["closure_digest"],
        "blind_packet_digest": packet["blind_packet_digest"],
        "proposer_receipt_ids": source_bindings["proposer_receipt_ids"],
        "previous_evidence_digest": previous_digest,
    }
    if evidence.get("input_binding") != expected_input:
        _adjudication_fail(
            "adjudication_input_binding_mismatch",
            "adjudication input binding differs from the frozen source closure",
        )
    expected_id = stable_identifier(
        "conceptual-adjudication-evidence",
        evidence.get("target_id"),
        evidence.get("run_id"),
        evidence.get("state_version"),
        evidence.get("stage_id"),
        expected_seal["panel_seal_digest"],
    )
    if evidence.get("evidence_id") != expected_id:
        _adjudication_fail(
            "adjudication_digest_mismatch", "adjudication evidence ID mismatch"
        )
    recorded_adjudication = evidence.get("content_adjudication")
    if not isinstance(recorded_adjudication, Mapping):
        _adjudication_fail(
            "adjudication_evidence_missing", "content adjudication is absent"
        )
    recomputed_adjudication = aggregate_adjudication(
        packet,
        reports,
        candidate_bindings=candidate_bindings,
        previous=previous_adjudication,
        previous_packet=previous_packet,
        created_at=str(recorded_adjudication.get("created_at") or evidence["created_at"]),
    )
    if dict(recorded_adjudication) != recomputed_adjudication:
        _adjudication_fail(
            "adjudication_pareto_derivation_mismatch",
            "content adjudication does not equal blind panel recomputation",
        )
    expected_preference = _preference_set(recomputed_adjudication, candidate_bindings)
    if evidence.get("preference_set") != expected_preference:
        _adjudication_fail(
            "adjudication_preference_set_mismatch",
            "recorded conceptual preference set does not equal the recomputed nondominated set",
        )
    if recomputed_adjudication.get("preference_set_digest") != expected_preference.get(
        "preference_set_digest"
    ):
        _adjudication_fail(
            "adjudication_preference_set_mismatch",
            "adjudication and evidence preference-set digests differ",
        )


def validate_sealed_preference_authority(
    evidence: Mapping[str, Any],
    *,
    target_id: str,
    run_id: str,
    state_version: int,
    system_ids: Sequence[str],
    stage_id: str | None = None,
    systems: Sequence[Mapping[str, Any]] | None = None,
    reflection_rounds: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Verify the self-contained seal consumed by downstream control surfaces.

    Full producer validation additionally replays the original unblinded systems,
    genealogy, and typed unification graph.  Once that evidence is sealed as one
    immutable canonical role, downstream workflow, scheduler, reducer, and gate
    consumers use this verifier: it rechecks schema closure, the complete judge
    panel, pre-unblinding seal, exact alias bijection, content-adjudication digest,
    and set-valued preference derivation.  A receipt ID, structural score, caller
    winner, or lone aggregate can never substitute for this object.
    """

    expected_digest = canonical_digest(
        evidence, exclude_keys=("evidence_digest", "created_at")
    )
    if evidence.get("evidence_digest") != expected_digest:
        _adjudication_fail(
            "adjudication_digest_mismatch", "sealed preference evidence digest mismatch"
        )
    try:
        validate_instance(dict(evidence), "conceptual_adjudication_evidence.schema.json")
    except ContractError as exc:
        _adjudication_fail("adjudication_schema_invalid", str(exc))
    if (
        evidence.get("target_id") != target_id
        or evidence.get("run_id") != run_id
        or evidence.get("state_version") != state_version
        or (stage_id is not None and evidence.get("stage_id") != stage_id)
    ):
        _adjudication_fail(
            "adjudication_input_binding_mismatch",
            "sealed preference evidence crossed target, run, state, or stage identity",
        )
    consumed_system_ids = [str(system_id) for system_id in system_ids]
    if len(consumed_system_ids) != len(set(consumed_system_ids)):
        _adjudication_fail(
            "adjudication_input_binding_mismatch",
            "the downstream conceptual-system set contains duplicate identities",
        )
    input_binding = evidence.get("input_binding")
    if not isinstance(input_binding, Mapping):
        _adjudication_fail(
            "adjudication_input_binding_mismatch",
            "sealed preference evidence lacks its exact input binding",
        )
    if systems is not None:
        consumed_systems = [dict(system) for system in systems]
        bound_ids = [str(system.get("system_id", "")) for system in consumed_systems]
        if bound_ids != consumed_system_ids:
            _adjudication_fail(
                "adjudication_input_binding_mismatch",
                "downstream system identities and ordered system content disagree",
            )
        if input_binding.get("conceptual_systems_digest") != canonical_digest(
            consumed_systems
        ):
            _adjudication_fail(
                "adjudication_input_binding_mismatch",
                "downstream conceptual-system content differs from the sealed candidate set",
            )
    if reflection_rounds is not None and input_binding.get(
        "reflection_rounds_digest"
    ) != canonical_digest([dict(row) for row in reflection_rounds]):
        _adjudication_fail(
            "adjudication_input_binding_mismatch",
            "downstream reflection content differs from the sealed reflection input",
        )
    authority = evidence.get("authority")
    if not isinstance(authority, Mapping) or authority.get(
        "sole_conceptual_preference_authority"
    ) is not True or authority.get("structural_scores_authorize_preference") is not False:
        _adjudication_fail(
            "adjudication_authority_invalid",
            "sealed evidence does not declare the exclusive non-structural authority boundary",
        )
    packet = evidence.get("blind_packet")
    reports = evidence.get("judge_reports")
    if not isinstance(packet, Mapping) or not isinstance(reports, list):
        _adjudication_fail(
            "adjudication_evidence_missing", "sealed evidence lacks packet or reports"
        )
    for report in reports:
        try:
            validate_judge_report(report, packet)
        except ContractError as exc:
            _adjudication_fail("adjudication_judge_report_invalid", str(exc))
    _validate_deep_lens_panel(packet, reports)
    expected_seal = _panel_seal(packet, reports)
    if evidence.get("panel_seal") != expected_seal:
        _adjudication_fail(
            "adjudication_panel_unsealed", "sealed evidence does not bind the full panel"
        )
    receipt = evidence.get("unblinding_receipt")
    if not isinstance(receipt, Mapping):
        _adjudication_fail(
            "adjudication_unblinding_order_invalid", "unblinding receipt is absent"
        )
    binding_rows = receipt.get("candidate_bindings")
    if not isinstance(binding_rows, list):
        _adjudication_fail(
            "adjudication_unblinding_order_invalid", "candidate bindings are absent"
        )
    bindings = {
        str(row.get("candidate_alias", "")): str(row.get("system_id", ""))
        for row in binding_rows
        if isinstance(row, Mapping)
    }
    if len(bindings) != len(binding_rows) or set(bindings.values()) != set(
        consumed_system_ids
    ):
        _adjudication_fail(
            "adjudication_input_binding_mismatch",
            "sealed candidate bindings are not a bijection over the consumed systems",
        )
    if receipt != _unblinding_receipt(expected_seal, bindings):
        _adjudication_fail(
            "adjudication_unblinding_order_invalid",
            "candidate identities were not unblinded from the already sealed panel",
        )
    adjudication = evidence.get("content_adjudication")
    if not isinstance(adjudication, Mapping):
        _adjudication_fail(
            "adjudication_evidence_missing", "sealed content adjudication is absent"
        )
    expected_adjudication_digest = canonical_digest(
        adjudication, exclude_keys=("adjudication_digest", "created_at")
    )
    if adjudication.get("adjudication_digest") != expected_adjudication_digest:
        _adjudication_fail(
            "adjudication_digest_mismatch", "sealed content adjudication digest mismatch"
        )
    expected_preference = _preference_set(adjudication, bindings)
    if evidence.get("preference_set") != expected_preference:
        _adjudication_fail(
            "adjudication_preference_set_mismatch",
            "sealed preference set does not equal the content-adjudication Pareto set",
        )
    preferred = expected_preference["preferred_system_ids"]
    if not set(preferred).issubset(set(consumed_system_ids)):
        _adjudication_fail(
            "adjudication_preference_set_mismatch",
            "sealed preference escapes the consumed conceptual-system set",
        )
    return copy.deepcopy(expected_preference)


__all__ = [
    "ConceptualAdjudicationError",
    "DEEP_LENS_FAMILIES",
    "DIMENSIONS",
    "RATINGS",
    "REQUIRED_DEEP_LENSES",
    "aggregate_adjudication",
    "build_adjudication_evidence",
    "build_adjudication_source_bindings",
    "build_blind_packet",
    "build_judge_report",
    "validate_adjudication_evidence",
    "validate_material_system_transition",
    "validate_judge_report",
    "validate_sealed_preference_authority",
]
