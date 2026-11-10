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
"""Preserve and index the user-supplied higher-abductive reference archive.

The upstream runtime is deliberately *not* installed or executed.  This importer
copies the exact archive, performs a safe read-only extraction without the
byte-identical ``build/lib`` duplicate, and records which conceptual structures
may be adapted by Abducer.  The resulting snapshot is reference material, not a
proof, literature, novelty, or execution authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping
from zipfile import ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
VERSION = "2026-07-22"
SOURCE_ARCHIVE_NAME = "higher_abductive_theory_discovery_system.zip"
IMPORT_ROOT = (
    ROOT / "agentic" / "external" / "higher_abductive_theory_discovery" / VERSION
)
ARCHIVE_DESTINATION = IMPORT_ROOT / "source_archives" / SOURCE_ARCHIVE_NAME
DEFAULT_SOURCE_ARCHIVE = ARCHIVE_DESTINATION
SNAPSHOT_ROOT = IMPORT_ROOT / "active_snapshot"
EXPECTED_ARCHIVE_SHA256 = (
    "906700d6680d31b904120f9fd4f0ba63512037ad94bb17bac95c52204c780be0"
)
EXPECTED_ARCHIVE_SIZE = 814_812
EXPECTED_MEMBER_COUNT = 469
EXPECTED_UNCOMPRESSED_BYTES = 1_018_135
ARCHIVE_PREFIX = "higher_abductive_theory_discovery_system/"
MAX_MEMBER_BYTES = 2_000_000
MAX_COMPRESSION_RATIO = 100.0

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
CHEAP_REPAIR_LADDER = (
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
    "Suspend",
    "PrimitiveShift",
    "DependencyInvert",
    "ContextInternalize",
    "LevelShift",
    "IdentityRevise",
    "InvariantExtract",
    "ObstructionReify",
    "Dualize",
    "BoundaryProbe",
    "Counterworld",
    "OperationalReanchor",
)


class ArchiveIntegrationError(ValueError):
    """Raised when the archive or a preserved projection violates its contract."""


def canonical_digest(value: Any) -> str:
    """Hash one JSON value with the repository's sorted compact encoding."""

    encoded = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _member_mode(info: ZipInfo) -> int:
    return (info.external_attr >> 16) & 0o170000


def _relative_member_path(name: str) -> PurePosixPath:
    """Return a safe path below the single expected archive root."""

    if "\\" in name:
        raise ArchiveIntegrationError(f"backslash archive path is forbidden: {name!r}")
    candidate = PurePosixPath(name)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ArchiveIntegrationError(f"unsafe archive path: {name!r}")
    if not name.startswith(ARCHIVE_PREFIX):
        raise ArchiveIntegrationError(f"member is outside the expected archive root: {name!r}")
    relative = PurePosixPath(name.removeprefix(ARCHIVE_PREFIX))
    if relative.parts and ":" in relative.parts[0]:
        raise ArchiveIntegrationError(f"drive-qualified archive path is forbidden: {name!r}")
    return relative


def _validate_zip_info(info: ZipInfo) -> PurePosixPath:
    relative = _relative_member_path(info.filename)
    if info.flag_bits & 1:
        raise ArchiveIntegrationError(f"encrypted archive member is forbidden: {info.filename}")
    if _member_mode(info) == stat.S_IFLNK:
        raise ArchiveIntegrationError(f"symlink archive member is forbidden: {info.filename}")
    if info.file_size > MAX_MEMBER_BYTES:
        raise ArchiveIntegrationError(f"archive member is unexpectedly large: {info.filename}")
    if info.file_size and info.compress_size == 0:
        raise ArchiveIntegrationError(f"nonempty member has zero compressed size: {info.filename}")
    if info.compress_size and info.file_size / info.compress_size > MAX_COMPRESSION_RATIO:
        raise ArchiveIntegrationError(f"archive member compression ratio is unsafe: {info.filename}")
    return relative


def _atomic_write(path: Path, data: bytes, *, mode: int = 0o444) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    _atomic_write(
        path,
        (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode(),
    )


def _active_member(relative: PurePosixPath, info: ZipInfo) -> bool:
    if info.is_dir() or not relative.parts:
        return False
    if relative.parts[0] == "build":
        return False
    if "__pycache__" in relative.parts or relative.suffix in {".pyc", ".pyo"}:
        return False
    return relative.name not in {".DS_Store"}


def _source_class(path: PurePosixPath) -> str:
    if not path.parts:
        return "source_provenance"
    return {
        "src": "reference_runtime_not_imported",
        "tests": "reference_tests_not_authority",
        "skills": "reference_prompt_contracts_not_installed",
        "adapters": "availability_or_dry_run_reference_only",
        "schemas": "loose_upstream_contract_reference_only",
        "docs": "conceptual_source_material",
        "benchmarks": "upstream_self_evaluation_reference_only",
        "examples": "illustrative_reference_only",
        "scripts": "external_runtime_entrypoints_not_executed",
    }.get(path.parts[0], "source_provenance")


def inspect_archive(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Validate the ZIP and return a byte-addressed member manifest."""

    if not path.is_file():
        raise ArchiveIntegrationError(f"source archive does not exist: {path}")
    if path.stat().st_size != EXPECTED_ARCHIVE_SIZE:
        raise ArchiveIntegrationError("source archive size differs from the approved attachment")
    if _sha256_file(path) != EXPECTED_ARCHIVE_SHA256:
        raise ArchiveIntegrationError("source archive digest differs from the approved attachment")

    rows: list[dict[str, Any]] = []
    names: set[str] = set()
    with ZipFile(path) as archive:
        infos = archive.infolist()
        if len(infos) != EXPECTED_MEMBER_COUNT:
            raise ArchiveIntegrationError("archive member count differs from the approved attachment")
        if sum(info.file_size for info in infos) != EXPECTED_UNCOMPRESSED_BYTES:
            raise ArchiveIntegrationError("archive uncompressed size differs from the approved attachment")
        for info in infos:
            relative = _validate_zip_info(info)
            normalized = str(PurePosixPath(info.filename))
            if normalized in names:
                raise ArchiveIntegrationError(f"duplicate normalized archive path: {normalized}")
            names.add(normalized)
            data = b"" if info.is_dir() else archive.read(info)
            rows.append(
                {
                    "archive_path": info.filename,
                    "relative_path": str(relative),
                    "is_directory": info.is_dir(),
                    "byte_size": info.file_size,
                    "compressed_size": info.compress_size,
                    "crc32": f"{info.CRC:08x}",
                    "content_sha256": _sha256_bytes(data),
                    "member_datetime": "%04d-%02d-%02dT%02d:%02d:%02d"
                    % info.date_time,
                    "active_snapshot": _active_member(relative, info),
                    "source_class": _source_class(relative),
                }
            )

    file_rows = [row for row in rows if not row["is_directory"]]
    src = {
        row["relative_path"].removeprefix("src/"): row["content_sha256"]
        for row in file_rows
        if row["relative_path"].startswith("src/")
    }
    built = {
        row["relative_path"].removeprefix("build/lib/"): row["content_sha256"]
        for row in file_rows
        if row["relative_path"].startswith("build/lib/")
    }
    if src != built:
        raise ArchiveIntegrationError("src and build/lib are not exact duplicate trees")
    duplicate_report = {
        "status": "byte_identical_build_duplicate_excluded",
        "src_file_count": len(src),
        "build_lib_file_count": len(built),
        "matched_relative_paths": sorted(src),
        "content_digest": canonical_digest(src),
    }
    return rows, duplicate_report


def _capability_map() -> dict[str, Any]:
    rows = [
        {
            "capability_id": "scoped_theory_atlas",
            "disposition": "adapt",
            "local_route": "theory-atlas-defect-compiler",
            "boundary": "Source-addressed signatures, axioms, models, observables, scope, and evidence remain staged rather than accepted theory.",
        },
        {
            "capability_id": "directional_partial_theory_relations",
            "disposition": "adapt",
            "local_route": "theory-atlas-defect-compiler",
            "boundary": "Horizontal translation, vertical refinement, and partiality are typed; no map is totalized by prose.",
        },
        {
            "capability_id": "meaning_profile_and_repair_ladder",
            "disposition": "adapt",
            "local_route": "theory-atlas-defect-compiler -> reflective-theory-synthesizer",
            "boundary": "All nine dimensions and the ordered six-repair ladder require source/evidence bindings; token distance is rejected.",
        },
        {
            "capability_id": "plural_reflection_and_redescription",
            "disposition": "adapt",
            "local_route": "reflective-theory-synthesizer -> theory-atlas-defect-compiler",
            "boundary": "Eight lenses and twelve operators must cause a typed structural delta or record not-applicable; templates carry no authority.",
        },
        {
            "capability_id": "defect_to_completion_taxonomy",
            "disposition": "adapt",
            "local_route": "theory-atlas-defect-compiler -> categorical-concept-forger/hott-equivalence-coherence-forger",
            "boundary": "Every selected defect needs a typed diagram and structure-specific executable obligation; labels alone are metaphorical.",
        },
        {
            "capability_id": "representation_mutation",
            "disposition": "adapt",
            "local_route": "theory-atlas-defect-compiler -> reflective-conceptual-discovery",
            "boundary": "Mutation requires repeated structured failures, exhausted cheap repairs, a migration map, loss/new-expressivity accounting, and acceptance review.",
        },
        {
            "capability_id": "abstract_concrete_return_square",
            "disposition": "adapt",
            "local_route": "theory-atlas-defect-compiler -> physical-relevance-impact-auditor -> ym-categorical-hott-physics-bridge",
            "boundary": "Exact squares replay actions; approximate squares state a metric, norm, error object, and bound. Physics value and investment remain false.",
        },
        {
            "capability_id": "tdr_runtime_and_http_api",
            "disposition": "external_only_rejected_as_authority",
            "local_route": "none",
            "boundary": "The lexical/template runtime, unauthenticated API, mutable persistence, loose schemas, and dry-run adapters are not installed or executed.",
        },
        {
            "capability_id": "seventeen_upstream_skills",
            "disposition": "source_reference_only_maximize_existing_reuse",
            "local_route": "reflective-conceptual-discovery and existing specialist skills",
            "boundary": "Overlapping upstream wrappers are not duplicated; only the distinct compiler handoff is added locally.",
        },
    ]
    return {
        "map_version": "1.0.0",
        "source_archive_sha256": EXPECTED_ARCHIVE_SHA256,
        "capabilities": rows,
        "meaning_dimensions": list(MEANING_DIMENSIONS),
        "cheap_repair_ladder": list(CHEAP_REPAIR_LADDER),
        "reflection_lenses": list(REFLECTION_LENSES),
        "redescription_operators": list(REDESCRIPTION_OPERATORS),
        "authority_boundary": (
            "This map selects conceptual design material only. It does not validate the "
            "external runtime, its generated claims, category theory, HoTT, physics, or value."
        ),
    }


def _readme_text() -> str:
    return f"""# Higher Abductive Theory Discovery — preserved reference

This directory preserves the user-supplied `{SOURCE_ARCHIVE_NAME}` attachment.
The exact archive has SHA-256 `{EXPECTED_ARCHIVE_SHA256}` and remains the source
authority. `active_snapshot/` is a safe extraction that excludes only the
byte-identical `build/lib` duplicate and generated bytecode/cache files.

The source is MIT-licensed, but it supplies no upstream URL, commit, signature,
dependency lock, SBOM, or internal checksum manifest. It is therefore recorded
as a user-supplied local reference. Its `tdr` runtime and HTTP API are not
installed, imported, or executed by Abducer.

`capability_map.json` records the narrow reuse decision. Abducer adapts scoped
theory atlases, directional/partial theory relations, nine-dimensional meaning
profiles, the ordered cheap-repair ladder, plural reflection/redescription,
typed defect-to-completion selection, representation-migration accounting, and
abstract-to-concrete return squares. The upstream lexical diagnostician,
template generation, loose schemas, stub-like tests, unchecked proof adapters,
and mutable persistence grant no proof, truth, novelty, value, or physics
authority.
"""


def _iter_active_rows(rows: Iterable[Mapping[str, Any]]) -> Iterable[Mapping[str, Any]]:
    return (row for row in rows if row["active_snapshot"] and not row["is_directory"])


def integrate(source_archive: Path = DEFAULT_SOURCE_ARCHIVE) -> dict[str, Any]:
    """Create the immutable source copy, active snapshot, and typed disposition."""

    rows, duplicate_report = inspect_archive(source_archive)
    IMPORT_ROOT.mkdir(parents=True, exist_ok=True)

    _atomic_write(ARCHIVE_DESTINATION, source_archive.read_bytes())
    active_rows: list[dict[str, Any]] = []
    with ZipFile(source_archive) as archive:
        for row in _iter_active_rows(rows):
            relative = PurePosixPath(str(row["relative_path"]))
            destination = SNAPSHOT_ROOT.joinpath(*relative.parts)
            data = archive.read(str(row["archive_path"]))
            if _sha256_bytes(data) != row["content_sha256"]:
                raise ArchiveIntegrationError(f"member changed during extraction: {relative}")
            _atomic_write(destination, data)
            active_rows.append(
                {
                    "path": str(relative),
                    "byte_size": len(data),
                    "content_sha256": _sha256_bytes(data),
                    "source_class": row["source_class"],
                }
            )

    active_rows.sort(key=lambda row: row["path"])
    active_index = {
        "index_version": "1.0.0",
        "source_archive_sha256": EXPECTED_ARCHIVE_SHA256,
        "excluded_prefixes": ["build/"],
        "excluded_generated_kinds": ["__pycache__", ".pyc", ".pyo", ".DS_Store"],
        "files": active_rows,
        "file_count": len(active_rows),
        "content_digest": canonical_digest(active_rows),
        "authority_boundary": "Safe source projection only; no external code was executed or installed.",
    }
    member_manifest = {
        "manifest_version": "1.0.0",
        "source_archive_sha256": EXPECTED_ARCHIVE_SHA256,
        "members": rows,
        "member_count": len(rows),
        "content_digest": canonical_digest(rows),
    }
    capability_map = _capability_map()
    capability_map["content_digest"] = canonical_digest(capability_map)
    source_manifest = {
        "manifest_version": "1.0.0",
        "source_kind": "user_supplied_local_archive",
        "version_label": VERSION,
        "archive": {
            "filename": SOURCE_ARCHIVE_NAME,
            "repo_path": str(ARCHIVE_DESTINATION.relative_to(ROOT)),
            "byte_size": EXPECTED_ARCHIVE_SIZE,
            "sha256": EXPECTED_ARCHIVE_SHA256,
        },
        "archive_member_manifest": {
            "repo_path": str((IMPORT_ROOT / "archive_member_manifest.json").relative_to(ROOT)),
            "content_digest": member_manifest["content_digest"],
        },
        "active_snapshot": {
            "repo_path": str(SNAPSHOT_ROOT.relative_to(ROOT)),
            "file_count": active_index["file_count"],
            "content_digest": active_index["content_digest"],
        },
        "license": {"kind": "MIT", "member_path": "LICENSE", "present": True},
        "provenance_unknowns": [
            "upstream_url",
            "upstream_commit",
            "publisher_signature",
            "dependency_lock",
            "software_bill_of_materials",
            "internal_checksum_manifest",
        ],
        "runtime_status": "not_installed_not_imported_not_executed",
        "adaptation_status": "design_primitives_only_through_local_strict_contracts",
        "proof_authority": False,
        "truth_authority": False,
        "novelty_authority": False,
        "conceptual_value_authority": False,
        "physics_value_authority": False,
    }
    source_manifest["content_digest"] = canonical_digest(source_manifest)
    checksum_report = {
        "status": "passed",
        "archive_sha256_verified": True,
        "safe_paths_verified": True,
        "symlink_free": True,
        "encryption_free": True,
        "duplicate_paths_absent": True,
        "compression_bounds_verified": True,
        "src_build_duplicate_report": duplicate_report,
        "active_snapshot_content_digest": active_index["content_digest"],
        "member_manifest_content_digest": member_manifest["content_digest"],
    }
    checksum_report["content_digest"] = canonical_digest(checksum_report)

    _write_json(IMPORT_ROOT / "archive_member_manifest.json", member_manifest)
    _write_json(IMPORT_ROOT / "active_index.json", active_index)
    _write_json(IMPORT_ROOT / "capability_map.json", capability_map)
    _write_json(IMPORT_ROOT / "source_manifest.json", source_manifest)
    _write_json(IMPORT_ROOT / "checksum_report.json", checksum_report)
    _atomic_write(IMPORT_ROOT / "README.md", _readme_text().encode())
    return source_manifest


def validate_preserved_import(import_root: Path = IMPORT_ROOT) -> dict[str, Any]:
    """Replay the preserved archive, snapshot, and provenance joins."""

    manifest = json.loads((import_root / "source_manifest.json").read_text())
    archive_path = ROOT / manifest["archive"]["repo_path"]
    if _sha256_file(archive_path) != EXPECTED_ARCHIVE_SHA256:
        raise ArchiveIntegrationError("preserved archive digest mismatch")
    rows, duplicate_report = inspect_archive(archive_path)
    member_manifest = json.loads((import_root / "archive_member_manifest.json").read_text())
    if member_manifest["members"] != rows or member_manifest["content_digest"] != canonical_digest(rows):
        raise ArchiveIntegrationError("archive member manifest does not replay")
    active_index = json.loads((import_root / "active_index.json").read_text())
    expected_active = sorted(
        (row for row in rows if row["active_snapshot"] and not row["is_directory"]),
        key=lambda row: row["relative_path"],
    )
    if [row["path"] for row in active_index["files"]] != [
        row["relative_path"] for row in expected_active
    ]:
        raise ArchiveIntegrationError("active snapshot path set differs from the source projection")
    for indexed, source in zip(active_index["files"], expected_active, strict=True):
        path = import_root / "active_snapshot" / indexed["path"]
        if not path.is_file() or _sha256_file(path) != source["content_sha256"]:
            raise ArchiveIntegrationError(f"active snapshot byte mismatch: {indexed['path']}")
        if indexed["path"].startswith("build/"):
            raise ArchiveIntegrationError("build duplicate entered the active snapshot")
    if active_index["content_digest"] != canonical_digest(active_index["files"]):
        raise ArchiveIntegrationError("active index digest mismatch")
    if manifest["archive_member_manifest"]["content_digest"] != member_manifest["content_digest"]:
        raise ArchiveIntegrationError("source manifest does not bind the member manifest")
    if manifest["active_snapshot"]["content_digest"] != active_index["content_digest"]:
        raise ArchiveIntegrationError("source manifest does not bind the active snapshot")
    if duplicate_report != json.loads((import_root / "checksum_report.json").read_text())["src_build_duplicate_report"]:
        raise ArchiveIntegrationError("src/build duplicate report does not replay")
    capability_map = json.loads((import_root / "capability_map.json").read_text())
    stored = capability_map.pop("content_digest")
    if stored != canonical_digest(capability_map):
        raise ArchiveIntegrationError("capability disposition digest mismatch")
    if manifest["runtime_status"] != "not_installed_not_imported_not_executed":
        raise ArchiveIntegrationError("external runtime boundary was weakened")
    if any(
        manifest[field]
        for field in (
            "proof_authority",
            "truth_authority",
            "novelty_authority",
            "conceptual_value_authority",
            "physics_value_authority",
        )
    ):
        raise ArchiveIntegrationError("external source was granted unsupported authority")
    return {
        "status": "valid",
        "archive_sha256": EXPECTED_ARCHIVE_SHA256,
        "member_count": len(rows),
        "active_file_count": len(active_index["files"]),
        "active_snapshot_content_digest": active_index["content_digest"],
        "capability_map_status": "design_primitives_only",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE_ARCHIVE)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    result = validate_preserved_import() if args.validate_only else integrate(args.source)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
