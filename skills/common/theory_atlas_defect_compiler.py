# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Compile source-bounded theory atlases into executable categorical defect packets.

The attached higher-abductive archive contributes a vocabulary, repair order,
reflection lenses, and redescription operators.  It contributes no runtime or
mathematical authority.  This module rebuilds those useful ideas as a strict,
deterministic local pre-forge contract and replays only finite obligations.
"""

from __future__ import annotations

import copy
import hashlib
from itertools import product
import json
from pathlib import Path
import stat
from typing import Any, Mapping, Sequence

from agentic.discovery.contracts import (
    ContractError,
    canonical_digest,
    stable_identifier,
    validate_instance,
)


SCHEMA = "theory_atlas_defect_packet.schema.json"
SCHEMA_VERSION = "2.0.0"
REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT_PATH = "agentic/external/higher_abductive_theory_discovery/2026-07-22"
SOURCE_ARCHIVE_PATH = f"{SOURCE_ROOT_PATH}/source_archives/higher_abductive_theory_discovery_system.zip"
SOURCE_ARCHIVE_SHA256 = "sha256:906700d6680d31b904120f9fd4f0ba63512037ad94bb17bac95c52204c780be0"
SOURCE_MANIFEST_PATH = f"{SOURCE_ROOT_PATH}/source_manifest.json"
SOURCE_MANIFEST_DIGEST = "sha256:da18ea5b5816e20f7eb39bec3ecc957942999a853208418c16f13a0ad2f62c47"
SOURCE_MANIFEST_FILE_SHA256 = "sha256:f6601072aa0e7afeb45ed29d08cf1610c4e421b75b32a9b8a6b05d53e8e39bb1"
SOURCE_MEMBER_MANIFEST_PATH = f"{SOURCE_ROOT_PATH}/archive_member_manifest.json"
SOURCE_MEMBER_MANIFEST_DIGEST = "sha256:2dcd63cab59dd82b719b7422c7130fd213570c5e39cedfe133428a1ab2c77844"
SOURCE_MEMBER_MANIFEST_FILE_SHA256 = "sha256:f9a427c46dec1a00771b08c3c8aa2eb3fc3cfaf056c72a77f6f239c1ac3cb0d2"
SOURCE_ACTIVE_INDEX_PATH = f"{SOURCE_ROOT_PATH}/active_index.json"
SOURCE_ACTIVE_INDEX_DIGEST = "sha256:4be0e320a00d2ea3089e9deb101867080b9426f3a278480deb103410be75dd6d"
SOURCE_ACTIVE_INDEX_FILE_SHA256 = "sha256:929d7f2945c5a6b1a239fd2ee2459c7f5ed75bd3219dfde9f4578daa91f5650f"
SOURCE_CAPABILITY_MAP_PATH = f"{SOURCE_ROOT_PATH}/capability_map.json"
SOURCE_CAPABILITY_MAP_DIGEST = "sha256:c64b7a995056965a09607f5427ab566ca5a5872b174b564592ab67a24a6f59fe"
SOURCE_CAPABILITY_MAP_FILE_SHA256 = "sha256:27ae5a71ea10827381c11548c544b4a449b53ca197ef96703c5553b2eae7877a"
SOURCE_CHECKSUM_REPORT_PATH = f"{SOURCE_ROOT_PATH}/checksum_report.json"
SOURCE_CHECKSUM_REPORT_DIGEST = "sha256:3b0b2c093b411a6cc9d58a72d59976a4354fe337d1a35024478e05d812d849cf"
SOURCE_CHECKSUM_REPORT_FILE_SHA256 = "sha256:69b3bd108f0642de92ce3e083777e8660c870079d5d3fa104044edaeeda2d1ff"

MEANING_DIMENSIONS = (
    "referential_role",
    "inferential_commitments",
    "identity_criteria",
    "modal_commitments",
    "operational_anchors",
    "scale_and_scope",
    "explanatory_role",
    "pragmatic_uses",
    "protected_distinctions",
)
REPAIR_LADDER = (
    "lexical_normalization",
    "unit_and_notation_alignment",
    "definitional_extension",
    "known_equivalence",
    "conservative_interpretation",
    "scope_restriction",
)
REFLECTION_LENSES = (
    "hermeneutic",
    "phenomenological_operational",
    "constitutive",
    "dialectical_immanent",
    "genealogical",
    "pragmatic",
    "structural_realist",
    "modal_counterfactual",
)
REDESCRIPTION_OPERATORS = (
    "suspend",
    "primitive_shift",
    "dependency_invert",
    "context_internalize",
    "level_shift",
    "identity_revise",
    "invariant_extract",
    "obstruction_reify",
    "dualize",
    "boundary_probe",
    "counterworld",
    "operational_reanchor",
)
DEFECT_COMPLETION_REGISTRY = {
    "representability": ("finite_representability",),
    "coherence": ("pushout", "adjunction_naturality"),
    "descent": ("descent_gluing",),
    "factorization": ("factorization",),
    "adjunction": ("adjunction_naturality",),
    "obstruction": ("lifting_obstruction",),
    "meta_theory": ("pushout",),
}
COMPLETION_KINDS = (
    "factorization",
    "finite_representability",
    "descent_gluing",
    "pushout",
    "adjunction_naturality",
    "lifting_obstruction",
)
AUTHORITY_BOUNDARY = (
    "Finite pre-forge structural replay only; categorical vocabulary, higher cells, "
    "and successful local checks establish no theorem, homotopy type, univalence "
    "principle, truth, conceptual value, physics value, or investment case."
)


class TheoryAtlasDefectError(ValueError):
    """Typed failure of compilation or cross-artifact replay."""

    def __init__(self, reason_code: str, detail: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"{reason_code}: {detail}")


def _fail(reason_code: str, detail: str) -> None:
    raise TheoryAtlasDefectError(reason_code, detail)


def _normalize(value: Any) -> str:
    return " ".join(str(value or "").casefold().split())


def _source_file(relative_path: str) -> Path:
    """Resolve one preserved source file without permitting path or link escape."""

    candidate = REPO_ROOT / relative_path
    try:
        metadata = candidate.lstat()
    except OSError as exc:
        _fail("ATLAS_PROVENANCE_INVALID", f"cannot read preserved source {relative_path}: {exc}")
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        _fail("ATLAS_PROVENANCE_INVALID", f"preserved source is not a regular no-follow file: {relative_path}")
    try:
        candidate.resolve(strict=True).relative_to(REPO_ROOT.resolve(strict=True))
    except (OSError, ValueError) as exc:
        _fail("ATLAS_PROVENANCE_INVALID", f"preserved source escapes the repository: {relative_path}: {exc}")
    return candidate


def _load_source_json(
    relative_path: str,
    expected_declared_digest: str,
    expected_file_sha256: str,
    *,
    self_hashed: bool = False,
) -> dict[str, Any]:
    """Load one byte-sealed JSON surface and, where promised, replay its self-hash."""

    path = _source_file(relative_path)
    try:
        raw_bytes = path.read_bytes()
        payload = json.loads(raw_bytes.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail("ATLAS_PROVENANCE_INVALID", f"invalid preserved JSON {relative_path}: {exc}")
    if not isinstance(payload, dict):
        _fail("ATLAS_PROVENANCE_INVALID", f"preserved JSON is not an object: {relative_path}")
    if "sha256:" + hashlib.sha256(raw_bytes).hexdigest() != expected_file_sha256:
        _fail("ATLAS_PROVENANCE_INVALID", f"preserved JSON bytes changed: {relative_path}")
    if payload.get("content_digest") != expected_declared_digest:
        _fail("ATLAS_PROVENANCE_INVALID", f"preserved JSON declares the wrong digest: {relative_path}")
    if self_hashed and canonical_digest(payload, exclude_keys=("content_digest",)) != expected_declared_digest:
        _fail("ATLAS_PROVENANCE_INVALID", f"preserved JSON bytes do not replay their digest: {relative_path}")
    return payload


def _validate_preserved_source(source: Mapping[str, Any]) -> None:
    """Replay the preserved archive and every manifest named by the packet."""

    expected = {
        "source_root_path": SOURCE_ROOT_PATH,
        "archive_path": SOURCE_ARCHIVE_PATH,
        "archive_sha256": SOURCE_ARCHIVE_SHA256,
        "source_manifest_path": SOURCE_MANIFEST_PATH,
        "source_manifest_digest": SOURCE_MANIFEST_DIGEST,
        "source_manifest_file_sha256": SOURCE_MANIFEST_FILE_SHA256,
        "member_manifest_path": SOURCE_MEMBER_MANIFEST_PATH,
        "member_manifest_digest": SOURCE_MEMBER_MANIFEST_DIGEST,
        "member_manifest_file_sha256": SOURCE_MEMBER_MANIFEST_FILE_SHA256,
        "active_index_path": SOURCE_ACTIVE_INDEX_PATH,
        "active_index_digest": SOURCE_ACTIVE_INDEX_DIGEST,
        "active_index_file_sha256": SOURCE_ACTIVE_INDEX_FILE_SHA256,
        "capability_map_path": SOURCE_CAPABILITY_MAP_PATH,
        "capability_map_digest": SOURCE_CAPABILITY_MAP_DIGEST,
        "capability_map_file_sha256": SOURCE_CAPABILITY_MAP_FILE_SHA256,
        "checksum_report_path": SOURCE_CHECKSUM_REPORT_PATH,
        "checksum_report_digest": SOURCE_CHECKSUM_REPORT_DIGEST,
        "checksum_report_file_sha256": SOURCE_CHECKSUM_REPORT_FILE_SHA256,
    }
    for field, value in expected.items():
        if source.get(field) != value:
            _fail("ATLAS_PROVENANCE_INVALID", f"source binding changed field {field}")

    archive = _source_file(SOURCE_ARCHIVE_PATH)
    archive_digest = "sha256:" + hashlib.sha256(archive.read_bytes()).hexdigest()
    if archive_digest != SOURCE_ARCHIVE_SHA256:
        _fail("ATLAS_PROVENANCE_INVALID", "preserved source archive bytes changed")

    manifest = _load_source_json(
        SOURCE_MANIFEST_PATH, SOURCE_MANIFEST_DIGEST, SOURCE_MANIFEST_FILE_SHA256
    )
    member_manifest = _load_source_json(
        SOURCE_MEMBER_MANIFEST_PATH,
        SOURCE_MEMBER_MANIFEST_DIGEST,
        SOURCE_MEMBER_MANIFEST_FILE_SHA256,
    )
    active_index = _load_source_json(
        SOURCE_ACTIVE_INDEX_PATH,
        SOURCE_ACTIVE_INDEX_DIGEST,
        SOURCE_ACTIVE_INDEX_FILE_SHA256,
    )
    capability_map = _load_source_json(
        SOURCE_CAPABILITY_MAP_PATH,
        SOURCE_CAPABILITY_MAP_DIGEST,
        SOURCE_CAPABILITY_MAP_FILE_SHA256,
        self_hashed=True,
    )
    checksum_report = _load_source_json(
        SOURCE_CHECKSUM_REPORT_PATH,
        SOURCE_CHECKSUM_REPORT_DIGEST,
        SOURCE_CHECKSUM_REPORT_FILE_SHA256,
    )

    archive_row = manifest.get("archive", {})
    member_row = manifest.get("archive_member_manifest", {})
    snapshot_row = manifest.get("active_snapshot", {})
    if archive_row.get("repo_path") != SOURCE_ARCHIVE_PATH or "sha256:" + str(archive_row.get("sha256")) != SOURCE_ARCHIVE_SHA256:
        _fail("ATLAS_PROVENANCE_INVALID", "source manifest does not bind the preserved archive")
    if member_row.get("repo_path") != SOURCE_MEMBER_MANIFEST_PATH or member_row.get("content_digest") != SOURCE_MEMBER_MANIFEST_DIGEST:
        _fail("ATLAS_PROVENANCE_INVALID", "source manifest does not bind the member manifest")
    if snapshot_row.get("repo_path") != f"{SOURCE_ROOT_PATH}/active_snapshot" or snapshot_row.get("content_digest") != SOURCE_ACTIVE_INDEX_DIGEST:
        _fail("ATLAS_PROVENANCE_INVALID", "source manifest does not bind the active snapshot")
    if member_manifest.get("content_digest") != checksum_report.get("member_manifest_content_digest"):
        _fail("ATLAS_PROVENANCE_INVALID", "member manifest and checksum report disagree")
    if active_index.get("content_digest") != checksum_report.get("active_snapshot_content_digest"):
        _fail("ATLAS_PROVENANCE_INVALID", "active index and checksum report disagree")
    if capability_map.get("source_archive_sha256") != SOURCE_ARCHIVE_SHA256.removeprefix("sha256:"):
        _fail("ATLAS_PROVENANCE_INVALID", "capability map does not bind the preserved archive")
    if checksum_report.get("status") != "passed" or checksum_report.get("archive_sha256_verified") is not True:
        _fail("ATLAS_PROVENANCE_INVALID", "preserved checksum report is not passed")


def _unique(rows: Sequence[Mapping[str, Any]], field: str, reason: str) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        key = str(row.get(field, ""))
        if not key or key in result:
            _fail(reason, f"{field} values must be non-empty and unique")
        result[key] = row
    return result


def _path_error(square: Mapping[str, Any]) -> float:
    try:
        abstract = square["abstract_path"]
        concrete = square["concrete_path"]
        left = abstract[-1]["output_values"]
        right = concrete[-1]["output_values"]
    except (KeyError, IndexError, TypeError) as exc:
        _fail("ATLAS_INPUT_INVALID", f"malformed return square: {exc}")
    if len(left) != len(right) or not left:
        _fail("ATLAS_INPUT_INVALID", "return-square outputs must have the same non-zero dimension")
    return round(max(abs(float(a) - float(b)) for a, b in zip(left, right, strict=True)), 12)


def compile_theory_atlas_defect_packet(spec: Mapping[str, Any]) -> dict[str, Any]:
    """Compile a generative atlas specification and validate the sealed packet."""

    if not isinstance(spec, Mapping):
        _fail("ATLAS_INPUT_INVALID", "compiler input must be a mapping")
    raw = copy.deepcopy(dict(spec))
    reserved = {
        "schema_version", "packet_id", "source_archive", "repair_ladder",
        "reflection_sweep", "redescription_operator_sweep",
        "registered_defect_taxonomy", "completion_candidates",
        "authority_boundaries", "content_digest",
    }
    overlap = reserved & raw.keys()
    if overlap:
        _fail("ATLAS_INPUT_INVALID", f"compiler-owned fields supplied: {sorted(overlap)}")
    try:
        repair_attempts = raw.pop("repair_attempts")
        reflection_mutations = raw.pop("reflection_mutations")
        operator_decisions = raw.pop("operator_decisions")
        completion_specs = raw.pop("completion_specs")
        target_id = raw["target_id"]
    except KeyError as exc:
        _fail("ATLAS_INPUT_INVALID", f"missing compiler input {exc.args[0]!r}")

    if not isinstance(repair_attempts, Mapping):
        _fail("ATLAS_INPUT_INVALID", "repair_attempts must be keyed by the exact repair ladder")
    repair_ladder = []
    for index, kind in enumerate(REPAIR_LADDER, start=1):
        if kind not in repair_attempts:
            _fail("ATLAS_INPUT_INVALID", f"missing repair attempt {kind}")
        row = copy.deepcopy(dict(repair_attempts[kind]))
        repair_ladder.append({"step_index": index, "repair_kind": kind, **row})

    if not isinstance(reflection_mutations, Mapping):
        _fail("ATLAS_INPUT_INVALID", "reflection_mutations must be keyed by lens")
    reflection_sweep = []
    for lens in REFLECTION_LENSES:
        if lens not in reflection_mutations:
            _fail("ATLAS_INPUT_INVALID", f"missing reflection lens {lens}")
        row = copy.deepcopy(dict(reflection_mutations[lens]))
        source = row.get("source_statement", "")
        mutation = row.get("mutated_statement", "")
        commitments = row.get("changed_commitments", [])
        row["non_restatement_check"] = {
            "normalized_source": _normalize(source),
            "normalized_mutation": _normalize(mutation),
            "is_restatement": _normalize(source) == _normalize(mutation),
            "new_commitment_count": len(commitments) if isinstance(commitments, list) else 0,
        }
        reflection_sweep.append({"lens_id": lens, **row})

    if not isinstance(operator_decisions, Mapping):
        _fail("ATLAS_INPUT_INVALID", "operator_decisions must be keyed by operator")
    operator_sweep = []
    for operator in REDESCRIPTION_OPERATORS:
        if operator not in operator_decisions:
            _fail("ATLAS_INPUT_INVALID", f"missing redescription operator {operator}")
        operator_sweep.append({"operator_id": operator, **copy.deepcopy(dict(operator_decisions[operator]))})

    completion_candidates = []
    for row in completion_specs:
        candidate = copy.deepcopy(dict(row))
        kind = str(candidate.pop("completion_kind"))
        candidate_id = str(candidate["candidate_id"])
        if "obligation" not in candidate:
            _fail(
                "ATLAS_INPUT_INVALID",
                f"completion {candidate_id} must supply a source-bound finite obligation",
            )
        if "replay" in candidate or "epistemic_status" in candidate:
            _fail(
                "ATLAS_INPUT_INVALID",
                f"completion {candidate_id} supplied compiler-owned replay authority",
            )
        try:
            declared_observed = bool(candidate["obligation"]["checks"][0]["observed"])
        except (KeyError, IndexError, TypeError) as exc:
            _fail("ATLAS_INPUT_INVALID", f"completion {candidate_id} has no executable check: {exc}")
        completion_candidates.append({
            **candidate,
            "completion_kind": kind,
            "replay": {
                "status": "passed" if declared_observed else "failed",
                "derived_observed": declared_observed,
                "finite_scope_only": True,
                "source_bound_not_forge_evidence": True,
            },
            "epistemic_status": "concept_candidate",
        })

    return_squares = copy.deepcopy(raw.get("return_squares", []))
    for square in return_squares:
        error = _path_error(square)
        bound = float(square.get("error_bound", 0.0))
        square["metric"] = "linf"
        square["observed_error"] = error
        square["within_bound"] = error <= bound + 1e-12
        square["trace_authority"] = "declared_numeric_trace_only_not_execution_or_physics_evidence"
    raw["return_squares"] = return_squares

    packet: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        **raw,
        "source_archive": {
            "source_root_path": SOURCE_ROOT_PATH,
            "archive_path": SOURCE_ARCHIVE_PATH,
            "archive_sha256": SOURCE_ARCHIVE_SHA256,
            "source_manifest_path": SOURCE_MANIFEST_PATH,
            "source_manifest_digest": SOURCE_MANIFEST_DIGEST,
            "source_manifest_file_sha256": SOURCE_MANIFEST_FILE_SHA256,
            "member_manifest_path": SOURCE_MEMBER_MANIFEST_PATH,
            "member_manifest_digest": SOURCE_MEMBER_MANIFEST_DIGEST,
            "member_manifest_file_sha256": SOURCE_MEMBER_MANIFEST_FILE_SHA256,
            "active_index_path": SOURCE_ACTIVE_INDEX_PATH,
            "active_index_digest": SOURCE_ACTIVE_INDEX_DIGEST,
            "active_index_file_sha256": SOURCE_ACTIVE_INDEX_FILE_SHA256,
            "capability_map_path": SOURCE_CAPABILITY_MAP_PATH,
            "capability_map_digest": SOURCE_CAPABILITY_MAP_DIGEST,
            "capability_map_file_sha256": SOURCE_CAPABILITY_MAP_FILE_SHA256,
            "checksum_report_path": SOURCE_CHECKSUM_REPORT_PATH,
            "checksum_report_digest": SOURCE_CHECKSUM_REPORT_DIGEST,
            "checksum_report_file_sha256": SOURCE_CHECKSUM_REPORT_FILE_SHA256,
            "integration_boundary": "source_taxonomies_and_redescription_operators_only_no_upstream_runtime_authority",
            "runtime_imported": False,
            "runtime_executed": False,
        },
        "repair_ladder": repair_ladder,
        "reflection_sweep": reflection_sweep,
        "redescription_operator_sweep": operator_sweep,
        "registered_defect_taxonomy": [
            {"defect_type": defect, "registered_completion_kinds": list(kinds)}
            for defect, kinds in DEFECT_COMPLETION_REGISTRY.items()
        ],
        "completion_candidates": completion_candidates,
        "authority_boundaries": {
            "epistemic_status": "concept_candidate",
            "finite_replay_scope_only": True,
            "theorem_proved": False,
            "truth_authorized": False,
            "homotopy_authorized": False,
            "univalence_authorized": False,
            "conceptual_value_authorized": False,
            "physics_value_authorized": False,
            "investment_authorized": False,
            "boundary_statement": AUTHORITY_BOUNDARY,
        },
    }
    packet["packet_id"] = stable_identifier("atlas-packet", target_id, canonical_digest(packet))
    packet["content_digest"] = canonical_digest(packet)
    validate_theory_atlas_defect_packet(packet)
    return packet


def _mapping(row: Mapping[str, Any]) -> dict[str, str]:
    return {str(pair["source"]): str(pair["target"]) for pair in row["pairs"]}


def _compose(first: Mapping[str, str], second: Mapping[str, str]) -> dict[str, str]:
    return {source: second[target] for source, target in first.items()}


def _all_total_maps(domain: Sequence[str], codomain: Sequence[str]) -> list[dict[str, str]]:
    if not domain:
        return [{}]
    if not codomain:
        return []
    return [dict(zip(domain, choices, strict=True)) for choices in product(codomain, repeat=len(domain))]


def _validate_obligation(candidate: Mapping[str, Any]) -> bool:
    reason = "ATLAS_COMPLETION_INVALID"
    kind = str(candidate["completion_kind"])
    obligation = candidate["obligation"]
    if obligation["obligation_type"] != kind:
        _fail(reason, "completion and obligation types differ")
    for field in ("subject_fragment_id", "structure_id", "diagram_id"):
        if obligation[field] != candidate[field]:
            _fail(reason, f"finite obligation changes source binding {field}")
    sets = _unique(obligation["sets"], "set_id", reason)
    maps = _unique(obligation["maps"], "map_id", reason)
    for row in maps.values():
        domain_id, codomain_id = row["domain_set_id"], row["codomain_set_id"]
        if domain_id not in sets or codomain_id not in sets:
            _fail(reason, f"map {row['map_id']} names an unknown finite set")
        domain = list(sets[domain_id]["elements"])
        codomain = set(sets[codomain_id]["elements"])
        pairs = row["pairs"]
        sources = [pair["source"] for pair in pairs]
        if len(sources) != len(set(sources)) or set(sources) != set(domain):
            _fail(reason, f"map {row['map_id']} is not a total single-valued finite map")
        if any(pair["target"] not in codomain for pair in pairs):
            _fail(reason, f"map {row['map_id']} has an out-of-carrier target")

    look = {map_id: _mapping(row) for map_id, row in maps.items()}
    checks = obligation["checks"]
    if len(checks) != 1 or checks[0]["check_kind"] != kind:
        _fail(reason, "each completion requires one same-kind executable check")
    check = checks[0]
    if set(check["map_ids"]) != set(maps) or set(check["set_ids"]) != set(sets):
        _fail(reason, "executable check does not bind the exact finite structure")

    if kind == "factorization":
        required = {"D", "M", "C"}, {"f", "g", "h"}
        if set(sets) != required[0] or set(maps) != required[1]:
            _fail(reason, "factorization requires exact D/M/C and f/g/h finite data")
        mediators = [
            mediator
            for mediator in _all_total_maps(sets["M"]["elements"], sets["C"]["elements"])
            if _compose(look["f"], mediator) == look["h"]
        ]
        derived = (
            _compose(look["f"], look["g"]) == look["h"]
            and len(mediators) == 1
            and look["g"] == mediators[0]
        )
    elif kind == "finite_representability":
        required_sets = {"HomX", "NatX", "HomY", "NatY"}
        required_maps = {
            "phi_x", "phi_x_inverse", "phi_y", "phi_y_inverse",
            "hom_reindex", "nat_reindex",
        }
        if set(sets) != required_sets or set(maps) != required_maps:
            _fail(
                reason,
                "finite representability requires two hom/natural-family fibers, bijections, and reindexing maps",
            )
        derived = (
            _compose(look["phi_x"], look["phi_x_inverse"])
            == {x: x for x in sets["HomX"]["elements"]}
            and _compose(look["phi_x_inverse"], look["phi_x"])
            == {x: x for x in sets["NatX"]["elements"]}
            and _compose(look["phi_y"], look["phi_y_inverse"])
            == {x: x for x in sets["HomY"]["elements"]}
            and _compose(look["phi_y_inverse"], look["phi_y"])
            == {x: x for x in sets["NatY"]["elements"]}
            and _compose(look["phi_x"], look["nat_reindex"])
            == _compose(look["hom_reindex"], look["phi_y"])
        )
    elif kind == "descent_gluing":
        required_sets = {"Global", "LocalU", "LocalV", "Overlap", "CompatiblePairs"}
        required_maps = {
            "res_u", "res_v", "res_u_overlap", "res_v_overlap",
            "pair_left", "pair_right", "restrict_pair", "glue",
        }
        if set(sets) != required_sets or set(maps) != required_maps:
            _fail(reason, "descent requires cover restrictions, overlap maps, compatible pairs, and gluing")
        encoded_pairs = {
            (look["pair_left"][pair_id], look["pair_right"][pair_id])
            for pair_id in sets["CompatiblePairs"]["elements"]
        }
        compatible_pairs = {
            (left, right)
            for left in sets["LocalU"]["elements"]
            for right in sets["LocalV"]["elements"]
            if look["res_u_overlap"][left] == look["res_v_overlap"][right]
        }
        derived = (
            len(encoded_pairs) == len(sets["CompatiblePairs"]["elements"])
            and encoded_pairs == compatible_pairs
            and _compose(look["restrict_pair"], look["pair_left"]) == look["res_u"]
            and _compose(look["restrict_pair"], look["pair_right"]) == look["res_v"]
            and _compose(look["restrict_pair"], look["glue"])
            == {x: x for x in sets["Global"]["elements"]}
            and _compose(look["glue"], look["restrict_pair"])
            == {x: x for x in sets["CompatiblePairs"]["elements"]}
        )
    elif kind == "pushout":
        if set(sets) != {"C", "A", "B", "P", "Q"} or set(maps) != {
            "c_to_a", "c_to_b", "a_to_p", "b_to_p", "a_to_q", "b_to_q", "p_to_q"
        }:
            _fail(reason, "pushout replay requires the exact tested span, cocone, and mediator")
        square = _compose(look["c_to_a"], look["a_to_p"]) == _compose(look["c_to_b"], look["b_to_p"])
        cocone = _compose(look["c_to_a"], look["a_to_q"]) == _compose(look["c_to_b"], look["b_to_q"])
        mediators = [
            mediator for mediator in _all_total_maps(sets["P"]["elements"], sets["Q"]["elements"])
            if _compose(look["a_to_p"], mediator) == look["a_to_q"]
            and _compose(look["b_to_p"], mediator) == look["b_to_q"]
        ]
        derived = square and cocone and len(mediators) == 1 and look["p_to_q"] == mediators[0]
    elif kind == "adjunction_naturality":
        required_sets = {"LH00", "RH00", "LH10", "RH10", "LH01", "RH01"}
        required_maps = {
            "adj00", "adj00_inverse", "adj10", "adj10_inverse",
            "adj01", "adj01_inverse", "left_domain", "right_domain",
            "left_codomain", "right_codomain",
        }
        if set(sets) != required_sets or set(maps) != required_maps:
            _fail(reason, "adjunction replay requires hom-bijections natural in both finite arguments")
        derived = (
            _compose(look["adj00"], look["adj00_inverse"])
            == {x: x for x in sets["LH00"]["elements"]}
            and _compose(look["adj00_inverse"], look["adj00"])
            == {x: x for x in sets["RH00"]["elements"]}
            and _compose(look["adj10"], look["adj10_inverse"])
            == {x: x for x in sets["LH10"]["elements"]}
            and _compose(look["adj10_inverse"], look["adj10"])
            == {x: x for x in sets["RH10"]["elements"]}
            and _compose(look["adj01"], look["adj01_inverse"])
            == {x: x for x in sets["LH01"]["elements"]}
            and _compose(look["adj01_inverse"], look["adj01"])
            == {x: x for x in sets["RH01"]["elements"]}
            and _compose(look["left_domain"], look["adj10"])
            == _compose(look["adj00"], look["right_domain"])
            and _compose(look["left_codomain"], look["adj01"])
            == _compose(look["adj00"], look["right_codomain"])
        )
    elif kind == "lifting_obstruction":
        if set(sets) != {"A", "B", "X", "Y"} or set(maps) != {"i", "u", "p", "v"}:
            _fail(reason, "lifting obstruction replay requires the exact tested square")
        square = _compose(look["i"], look["v"]) == _compose(look["u"], look["p"])
        lifts = [
            lift for lift in _all_total_maps(sets["B"]["elements"], sets["X"]["elements"])
            if _compose(look["i"], lift) == look["u"] and _compose(lift, look["p"]) == look["v"]
        ]
        derived = square and not lifts
    else:  # schema should make this unreachable
        _fail(reason, f"unregistered completion {kind}")
    if bool(check["observed"]) != derived or bool(check["expected"]) is not True:
        _fail(reason, f"{kind} replay result is not derived from its finite structure")
    replay = candidate["replay"]
    if (
        replay["derived_observed"] != derived
        or replay["status"] != ("passed" if derived else "failed")
        or replay.get("source_bound_not_forge_evidence") is not True
    ):
        _fail(reason, f"{kind} completion replay receipt is stale")
    return derived


def validate_theory_atlas_defect_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the packet and return a deterministic finite-scope receipt."""

    try:
        validate_instance(packet, SCHEMA)
    except ContractError as exc:
        _fail("ATLAS_SCHEMA_INVALID", str(exc))
    packet_without_digest = copy.deepcopy(dict(packet))
    packet_without_digest.pop("content_digest", None)
    if packet["content_digest"] != canonical_digest(packet_without_digest):
        _fail("ATLAS_DIGEST_INVALID", "content_digest does not bind the exact packet")
    packet_without_identity = copy.deepcopy(packet_without_digest)
    packet_id = str(packet_without_identity.pop("packet_id", ""))
    expected_packet_id = stable_identifier(
        "atlas-packet",
        str(packet["target_id"]),
        canonical_digest(packet_without_identity),
    )
    if packet_id != expected_packet_id:
        _fail("ATLAS_IDENTITY_INVALID", "packet_id is not derived from the exact pre-ID packet")
    source = packet["source_archive"]
    _validate_preserved_source(source)

    evidence = _unique(packet["evidence_registry"], "evidence_id", "ATLAS_EVIDENCE_INVALID")
    evidence_ids = set(evidence)
    for evidence_id, row in evidence.items():
        if row["content_digest"] != canonical_digest(row, exclude_keys=("content_digest",)):
            _fail("ATLAS_EVIDENCE_INVALID", f"evidence {evidence_id} has a stale content digest")

    def bind_evidence(refs: Sequence[str], context: str, allowed: set[str] | None = None) -> None:
        ref_set = set(refs)
        if not ref_set or not ref_set <= evidence_ids:
            _fail("ATLAS_EVIDENCE_INVALID", f"{context} has unknown or empty evidence references")
        if allowed is not None and not ref_set <= allowed:
            _fail("ATLAS_EVIDENCE_INVALID", f"{context} escapes its source fragment evidence")

    fragments = _unique(packet["theory_fragments"], "fragment_id", "ATLAS_FRAGMENT_INVALID")
    fragment_symbols: dict[str, dict[str, set[str]]] = {}
    fragment_morphisms: dict[str, dict[str, Mapping[str, Any]]] = {}
    for fragment_id, fragment in fragments.items():
        bind_evidence(fragment["evidence_refs"], f"fragment {fragment_id}")
        signature = fragment["signature"]
        objects = set(signature["objects"])
        morphisms = _unique(signature["morphisms"], "symbol", "ATLAS_FRAGMENT_INVALID")
        predicates = set(signature["predicates"])
        if objects & set(morphisms) or objects & predicates or set(morphisms) & predicates:
            _fail("ATLAS_FRAGMENT_INVALID", f"fragment {fragment_id} reuses symbols across types")
        if any(row["source_object"] not in objects or row["target_object"] not in objects for row in morphisms.values()):
            _fail("ATLAS_FRAGMENT_INVALID", f"fragment {fragment_id} has an ill-typed morphism")
        source_evidence = set(fragment["evidence_refs"])
        if tuple(fragment["meaning_profile"].keys()) != MEANING_DIMENSIONS:
            _fail("ATLAS_FRAGMENT_INVALID", f"fragment {fragment_id} meaning dimensions are not exact and ordered")
        for dimension in MEANING_DIMENSIONS:
            bind_evidence(fragment["meaning_profile"][dimension]["evidence_refs"], f"{fragment_id}.{dimension}", source_evidence)
        fragment_symbols[fragment_id] = {"object": objects, "morphism": set(morphisms), "predicate": predicates}
        fragment_morphisms[fragment_id] = morphisms

    relations = _unique(packet["relations"], "relation_id", "ATLAS_RELATION_INVALID")
    if {row["relation_kind"] for row in relations.values()} != {"horizontal", "vertical", "partial"}:
        _fail("ATLAS_RELATION_INVALID", "horizontal, vertical, and partial relations are all required")
    for relation_id, relation in relations.items():
        source_id, target_id = relation["source_fragment_id"], relation["target_fragment_id"]
        if source_id not in fragments or target_id not in fragments:
            _fail("ATLAS_RELATION_INVALID", f"relation {relation_id} names an unknown fragment")
        bind_evidence(relation["evidence_refs"], f"relation {relation_id}")
        mapped_sources: set[str] = set()
        object_map: dict[str, str] = {}
        morphism_pairs: list[tuple[str, str]] = []
        for entry in relation["symbol_map"]:
            kind = entry["symbol_kind"]
            source_symbol, target_symbol = entry["source_symbol"], entry["target_symbol"]
            if source_symbol in mapped_sources:
                _fail("ATLAS_RELATION_INVALID", f"relation {relation_id} maps a source symbol twice")
            mapped_sources.add(source_symbol)
            if source_symbol not in fragment_symbols[source_id][kind] or target_symbol not in fragment_symbols[target_id][kind]:
                _fail("ATLAS_RELATION_INVALID", f"relation {relation_id} contains a symbol type swap")
            if kind == "object":
                object_map[source_symbol] = target_symbol
            elif kind == "morphism":
                morphism_pairs.append((source_symbol, target_symbol))
        for source_symbol, target_symbol in morphism_pairs:
            source_morphism = fragment_morphisms[source_id][source_symbol]
            target_morphism = fragment_morphisms[target_id][target_symbol]
            if (
                object_map.get(source_morphism["source_object"])
                != target_morphism["source_object"]
                or object_map.get(source_morphism["target_object"])
                != target_morphism["target_object"]
            ):
                _fail(
                    "ATLAS_RELATION_INVALID",
                    f"relation {relation_id} does not preserve mapped morphism endpoints",
                )
        source_all = set().union(*fragment_symbols[source_id].values())
        unmapped = set(relation["unmapped_source_symbols"])
        if relation["relation_kind"] == "partial":
            if relation["total"] or not mapped_sources or not unmapped or mapped_sources & unmapped or mapped_sources | unmapped != source_all:
                _fail("ATLAS_RELATION_INVALID", f"partial relation {relation_id} was totalized or has incomplete coverage")
        elif not relation["total"] or unmapped or mapped_sources != source_all:
            _fail("ATLAS_RELATION_INVALID", f"{relation['relation_kind']} relation {relation_id} must be explicitly total")

    diagrams = _unique(packet["diagrams"], "diagram_id", "ATLAS_DIAGRAM_INVALID")
    for diagram_id, diagram in diagrams.items():
        nodes = _unique(diagram["nodes"], "node_id", "ATLAS_DIAGRAM_INVALID")
        arrows = _unique(diagram["arrows"], "arrow_id", "ATLAS_DIAGRAM_INVALID")
        for node_id, node in nodes.items():
            if node["fragment_id"] not in fragments or node["object_symbol"] not in fragment_symbols[node["fragment_id"]]["object"]:
                _fail("ATLAS_DIAGRAM_INVALID", f"diagram node {node_id} is not a typed fragment object")
        for arrow_id, arrow in arrows.items():
            if arrow["source_node_id"] not in nodes or arrow["target_node_id"] not in nodes:
                _fail("ATLAS_DIAGRAM_INVALID", f"arrow {arrow_id} has an unknown endpoint")
            left, right = nodes[arrow["source_node_id"]], nodes[arrow["target_node_id"]]
            if arrow["arrow_type"] == "intra_fragment_morphism":
                if left["fragment_id"] != right["fragment_id"]:
                    _fail("ATLAS_DIAGRAM_INVALID", f"intra-fragment arrow {arrow_id} crosses fragments")
                morphism = fragment_morphisms[left["fragment_id"]].get(arrow["symbol_ref"])
                if not morphism or morphism["source_object"] != left["object_symbol"] or morphism["target_object"] != right["object_symbol"]:
                    _fail("ATLAS_DIAGRAM_INVALID", f"arrow {arrow_id} endpoints do not match its morphism")
            else:
                relation = relations.get(arrow["symbol_ref"])
                if not relation or relation["source_fragment_id"] != left["fragment_id"] or relation["target_fragment_id"] != right["fragment_id"]:
                    _fail("ATLAS_DIAGRAM_INVALID", f"inter-fragment arrow {arrow_id} does not match its relation")
                object_pairs = {(row["source_symbol"], row["target_symbol"]) for row in relation["symbol_map"] if row["symbol_kind"] == "object"}
                if (left["object_symbol"], right["object_symbol"]) not in object_pairs:
                    _fail("ATLAS_DIAGRAM_INVALID", f"inter-fragment arrow {arrow_id} endpoints are not mapped")

        def path_endpoints(path: Sequence[str]) -> tuple[str, str]:
            if any(arrow_id not in arrows for arrow_id in path):
                _fail("ATLAS_DIAGRAM_INVALID", "higher-cell path names an unknown arrow")
            rows = [arrows[arrow_id] for arrow_id in path]
            if any(left["target_node_id"] != right["source_node_id"] for left, right in zip(rows, rows[1:])):
                _fail("ATLAS_DIAGRAM_INVALID", "higher-cell path is not composable")
            return rows[0]["source_node_id"], rows[-1]["target_node_id"]

        _unique(diagram["higher_cells"], "cell_id", "ATLAS_DIAGRAM_INVALID")
        for cell in diagram["higher_cells"]:
            bind_evidence(cell["evidence_refs"], f"higher cell {cell['cell_id']}")
            source_endpoints = path_endpoints(cell["source_path"])
            target_endpoints = path_endpoints(cell["target_path"])
            declared = (cell["source_node_id"], cell["target_node_id"])
            if source_endpoints != target_endpoints or source_endpoints != declared:
                _fail("ATLAS_DIAGRAM_INVALID", f"higher cell {cell['cell_id']} does not compare parallel paths")
            if cell["status"] != "open":
                _fail(
                    "ATLAS_HIGHER_CELL_UNEXECUTED",
                    f"higher cell {cell['cell_id']} is typed but not independently replayed by the atlas",
                )

    if tuple(row["repair_kind"] for row in packet["repair_ladder"]) != REPAIR_LADDER or any(row["outcome"] != "failed" for row in packet["repair_ladder"]):
        _fail("ATLAS_REPAIR_LADDER_INVALID", "all six cheap repairs must be attempted in exact order and fail before defect completion")
    for row in packet["repair_ladder"]:
        bind_evidence(row["evidence_refs"], f"repair {row['repair_kind']}")

    operators = _unique(packet["redescription_operator_sweep"], "operator_id", "ATLAS_OPERATOR_SWEEP_INVALID")
    if tuple(operators) != REDESCRIPTION_OPERATORS:
        _fail("ATLAS_OPERATOR_SWEEP_INVALID", "the twelve-operator sweep is missing or reordered")
    applied_operators = set()
    operator_candidate_refs: dict[str, set[str]] = {}
    for operator_id, row in operators.items():
        refs = set(row["candidate_refs"])
        operator_candidate_refs[operator_id] = refs
        if row["status"] == "applied":
            if not refs:
                _fail("ATLAS_OPERATOR_SWEEP_INVALID", f"applied operator {operator_id} has no candidate reference")
            applied_operators.add(operator_id)
        elif refs:
            _fail("ATLAS_OPERATOR_SWEEP_INVALID", f"not-applicable operator {operator_id} carries candidates")
    if tuple(row["lens_id"] for row in packet["reflection_sweep"]) != REFLECTION_LENSES:
        _fail("ATLAS_REFLECTION_INVALID", "all eight reflection lenses are required in exact order")
    for row in packet["reflection_sweep"]:
        check = row["non_restatement_check"]
        source, mutation = _normalize(row["source_statement"]), _normalize(row["mutated_statement"])
        if source == mutation or check != {
            "normalized_source": source,
            "normalized_mutation": mutation,
            "is_restatement": False,
            "new_commitment_count": len(row["changed_commitments"]),
        }:
            _fail("ATLAS_REFLECTION_INVALID", f"lens {row['lens_id']} is a restatement or has a stale mutation receipt")
        if not set(row["operator_refs"]) <= applied_operators:
            _fail("ATLAS_REFLECTION_INVALID", f"lens {row['lens_id']} cites an unapplied redescription operator")
        if _normalize(row["new_question"]) in {source, mutation} or _normalize(row["new_failure_mode"]) in {source, mutation}:
            _fail("ATLAS_REFLECTION_INVALID", f"lens {row['lens_id']} did not generate a new question and failure mode")

    expected_taxonomy = [
        {"defect_type": defect, "registered_completion_kinds": list(kinds)}
        for defect, kinds in DEFECT_COMPLETION_REGISTRY.items()
    ]
    if packet["registered_defect_taxonomy"] != expected_taxonomy:
        _fail("ATLAS_DEFECT_INVALID", "defect taxonomy or registered completion mapping changed")
    defects = _unique(packet["defects"], "defect_id", "ATLAS_DEFECT_INVALID")
    for defect_id, defect in defects.items():
        if defect["subject_fragment_id"] not in fragments or defect["diagram_id"] not in diagrams:
            _fail("ATLAS_DEFECT_INVALID", f"defect {defect_id} is not bound to a fragment and typed diagram")
        if defect["completion_kind"] not in DEFECT_COMPLETION_REGISTRY[defect["defect_type"]]:
            _fail("ATLAS_DEFECT_INVALID", f"defect {defect_id} uses an unregistered completion")
        if defect["structure_id"] not in fragment_symbols[defect["subject_fragment_id"]].get(
            defect["structure_kind"], set()
        ):
            _fail(
                "ATLAS_DEFECT_INVALID",
                f"defect {defect_id} structure is not a typed symbol of its subject fragment",
            )
        bind_evidence(defect["evidence_refs"], f"defect {defect_id}")

    candidates = _unique(packet["completion_candidates"], "candidate_id", "ATLAS_COMPLETION_INVALID")
    if {row["completion_kind"] for row in candidates.values()} != set(COMPLETION_KINDS):
        _fail("ATLAS_COMPLETION_INVALID", "all six executable completion families are required")
    for candidate_id, candidate in candidates.items():
        defect = defects.get(candidate["defect_id"])
        if not defect:
            _fail("ATLAS_COMPLETION_INVALID", f"candidate {candidate_id} names an unknown defect")
        for field in ("completion_kind", "subject_fragment_id", "structure_id", "diagram_id"):
            if candidate[field] != defect[field]:
                _fail("ATLAS_COMPLETION_INVALID", f"candidate {candidate_id} changes defect field {field}")
        bind_evidence(
            candidate["obligation"]["evidence_refs"],
            f"completion obligation {candidate_id}",
            set(defect["evidence_refs"]),
        )
        _validate_obligation(candidate)
    candidate_ids = set(candidates)
    referenced_candidates = set().union(*operator_candidate_refs.values())
    if referenced_candidates != candidate_ids:
        _fail(
            "ATLAS_OPERATOR_SWEEP_INVALID",
            "applied operator candidate references must close exactly over completion candidates",
        )

    failures = _unique(packet["structured_failures"], "failure_id", "ATLAS_MUTATION_GATE_INVALID")
    for failure_id, failure in failures.items():
        defect = defects.get(failure["defect_id"])
        if not defect or failure["structure_id"] != defect["structure_id"]:
            _fail("ATLAS_MUTATION_GATE_INVALID", f"structured failure {failure_id} is not bound to its defect structure")
        bind_evidence(failure["evidence_refs"], f"structured failure {failure_id}")
    mutation = packet["representation_mutation"]
    trigger_rows = [failures.get(failure_id) for failure_id in mutation["trigger_failure_ids"]]
    if len(trigger_rows) < 2 or any(row is None for row in trigger_rows):
        _fail("ATLAS_MUTATION_GATE_INVALID", "representation mutation requires at least two registered failures")
    if len({row["attempt"] for row in trigger_rows if row}) < 2 or len({(row["defect_id"], row["structure_id"]) for row in trigger_rows if row}) != 1:
        _fail("ATLAS_MUTATION_GATE_INVALID", "mutation triggers are not repeated failures of the same structured defect")
    source_grammar, target_grammar = mutation["source_grammar"], mutation["proposed_grammar"]
    source_types = {symbol: kind for kind in ("object", "morphism", "rule") for symbol in source_grammar[f"{kind}s"]}
    target_types = {symbol: kind for kind in ("object", "morphism", "rule") for symbol in target_grammar[f"{kind}s"]}
    migration = mutation["migration_map"]
    if [row["source_symbol"] for row in migration] != list(dict.fromkeys(row["source_symbol"] for row in migration)) or set(row["source_symbol"] for row in migration) != set(source_types):
        _fail("ATLAS_MUTATION_GATE_INVALID", "migration map must cover every source grammar symbol exactly once")
    if any(source_types.get(row["source_symbol"]) != row["symbol_kind"] or target_types.get(row["target_symbol"]) != row["symbol_kind"] for row in migration):
        _fail("ATLAS_MUTATION_GATE_INVALID", "migration map contains a type swap or unknown target")

    if {row["mode"] for row in packet["return_squares"]} != {"exact", "approximate"}:
        _fail("ATLAS_RETURN_SQUARE_INVALID", "both exact and approximate return-square replays are required")
    # Every registered completion must retain a concrete return burden. Checking
    # only that each square names an existing candidate lets a rehashed splice
    # duplicate one candidate's coverage and silently drop another's.
    _unique(packet["return_squares"], "square_id", "ATLAS_RETURN_SQUARE_INVALID")
    if {row["completion_candidate_id"] for row in packet["return_squares"]} != set(candidates):
        _fail("ATLAS_RETURN_SQUARE_INVALID", "return squares must cover every registered completion candidate")
    for square in packet["return_squares"]:
        if square["subject_fragment_id"] not in fragments or square["completion_candidate_id"] not in candidates:
            _fail("ATLAS_RETURN_SQUARE_INVALID", f"return square {square['square_id']} has an unknown subject")
        selected_candidate = candidates[square["completion_candidate_id"]]
        if square["subject_fragment_id"] != selected_candidate["subject_fragment_id"]:
            _fail(
                "ATLAS_RETURN_SQUARE_INVALID",
                f"return square {square['square_id']} splices a candidate across subject fragments",
            )
        subject_structure_ids = set().union(
            *fragment_symbols[square["subject_fragment_id"]].values()
        )
        if not set(square["changed_structure_ids"]) <= subject_structure_ids:
            _fail(
                "ATLAS_RETURN_SQUARE_INVALID",
                f"return square {square['square_id']} names an unknown changed structure",
            )
        for path_name in ("abstract_path", "concrete_path"):
            path = square[path_name]
            if any(left["output_values"] != right["input_values"] for left, right in zip(path, path[1:])):
                _fail("ATLAS_RETURN_SQUARE_INVALID", f"{square['square_id']} {path_name} is not composable")
        if square["abstract_path"][0]["input_values"] != square["concrete_path"][0]["input_values"]:
            _fail("ATLAS_RETURN_SQUARE_INVALID", f"return square {square['square_id']} has different sources")
        error = _path_error(square)
        bound = float(square["error_bound"])
        within = error <= bound + 1e-12
        if float(square["observed_error"]) != error or bool(square["within_bound"]) != within or not within:
            _fail("ATLAS_RETURN_SQUARE_INVALID", f"return square {square['square_id']} has a stale or failed error receipt")
        if square["mode"] == "exact" and (bound != 0.0 or error != 0.0):
            _fail("ATLAS_RETURN_SQUARE_INVALID", "exact return square must have zero error and zero bound")
        if square["mode"] == "approximate" and bound <= 0.0:
            _fail("ATLAS_RETURN_SQUARE_INVALID", "approximate return square requires a positive declared bound")

    boundary = packet["authority_boundaries"]
    forbidden = (
        "theorem_proved", "truth_authorized", "homotopy_authorized",
        "univalence_authorized", "conceptual_value_authorized",
        "physics_value_authorized", "investment_authorized",
    )
    if any(boundary[field] for field in forbidden) or boundary["boundary_statement"] != AUTHORITY_BOUNDARY:
        _fail("ATLAS_AUTHORITY_BOUNDARY_INVALID", "finite pre-forge output was promoted beyond its authority")

    receipt: dict[str, Any] = {
        "status": "validated",
        "packet_id": packet["packet_id"],
        "packet_digest": packet["content_digest"],
        "validation_receipt_id": stable_identifier(
            "atlas-validation", packet["packet_id"], packet["content_digest"]
        ),
        "authority_class": "finite_pre_forge_structural_pressure_only",
    }
    receipt["content_digest"] = canonical_digest(receipt)
    return receipt


__all__ = [
    "AUTHORITY_BOUNDARY",
    "COMPLETION_KINDS",
    "DEFECT_COMPLETION_REGISTRY",
    "MEANING_DIMENSIONS",
    "REDESCRIPTION_OPERATORS",
    "REFLECTION_LENSES",
    "REPAIR_LADDER",
    "SOURCE_ARCHIVE_PATH",
    "SOURCE_ARCHIVE_SHA256",
    "TheoryAtlasDefectError",
    "compile_theory_atlas_defect_packet",
    "validate_theory_atlas_defect_packet",
]
